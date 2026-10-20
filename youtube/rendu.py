"""Images de la vidéo (1920×1080, 24 i/s) : une photo par partie (zoom lent, léger glissement, fondus enchaînés),
particules lumineuses, brume sur les parties choisies, cercle de respiration, titres et sous-titres animés,
adresse du site au début et à la fin. Rendu en morceaux parallèles puis assemblage avec la piste audio."""
import json, math, os, subprocess, sys
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from commun import W, H, FPS, POLICES, SITE, CHAINE, dossier_travail, lire_plan, lisse, fondu

FONDU = 5.0
MOUV = [(1.0, 1.13, -0.4, 0.2), (1.12, 1.0, 0.5, 0.0), (1.0, 1.10, 0.0, -0.4), (1.10, 1.0, -0.5, 0.3),
        (1.0, 1.12, 0.6, 0.0), (1.0, 1.15, 0.0, 0.5), (1.12, 1.0, -0.3, -0.2), (1.0, 1.08, 0.3, 0.0)]
ETAT = {}


def police(nom, t):
    return ImageFont.truetype(os.path.join(POLICES, nom), t)


def preparer(slug):
    """Charge tout ce qui ne dépend pas du temps (appelé une fois par processus)."""
    if ETAT.get("slug") == slug:
        return
    plan, trav = lire_plan(slug), dossier_travail(slug)
    tl = json.load(open(os.path.join(trav, "timeline.json")))
    rng = np.random.default_rng(20261020)
    noms = ["intro"] + [t["texte"] for t in tl["titres"]] + ["fin"]
    photos = plan["photos"]
    assert len(photos) == len(noms), f"{len(photos)} photos pour {len(noms)} scènes ({noms})"
    debuts = [0.0] + [t["debut"] - 1.0 for t in tl["titres"]] + [tl["fin_voix"] + 4]
    scenes = [(noms[i], debuts[i], debuts[i + 1] if i + 1 < len(debuts) else tl["duree"] + 1) for i in range(len(noms))]
    src = {}
    for (nom, _, _), ph in zip(scenes, photos):
        im = Image.open(os.path.join(trav, "photos", ph["nom"])).convert("RGB")
        r = max(W * 1.18 / im.width, H * 1.18 / im.height)
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        a = np.asarray(im, np.float32) * np.array([0.80, 0.84, 0.95], np.float32) * ph.get("lum", 0.85)
        src[nom] = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    yy, xx = np.mgrid[0:H, 0:W]
    vignette = (1 - 0.55 * (((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)).clip(0.35, 1).astype(np.float32)[..., None]
    # particules dorées qui montent lentement
    n = 70
    part = dict(x=rng.uniform(0, W, n), y=rng.uniform(0, H, n), v=rng.uniform(6, 18, n), s=rng.uniform(1.5, 4.5, n),
                ph=rng.uniform(0, 2 * math.pi, n), a=rng.uniform(0.25, 0.8, n))
    sprites = {}
    for s in (2, 3, 4, 5):
        k = 8 * s + 1
        g = np.mgrid[0:k, 0:k] - k // 2
        sprites[s] = np.exp(-(g[0] ** 2 + g[1] ** 2) / (2 * (0.9 * s) ** 2)).astype(np.float32)
    # brume qui dérive (parties listées dans plan["brume"])
    bw = W * 2
    br = rng.random((H // 16, bw // 16)).astype(np.float32)
    br = np.asarray(Image.fromarray((br * 255).astype(np.uint8)).resize((bw, H), Image.BICUBIC)
                    .filter(ImageFilter.GaussianBlur(60)), np.float32) / 255.0
    br = ((br - br.mean()) * 3.2 + 0.5).clip(0, 1) * np.linspace(0.3, 1, H, dtype=np.float32)[:, None]
    brume = []
    for i, ti in enumerate(tl["titres"]):
        if ti["texte"] in plan.get("brume", []):
            fin = tl["titres"][i + 1]["debut"] if i + 1 < len(tl["titres"]) else tl["fin_voix"]
            brume.append((ti["debut"], fin))
    ecran = plan["ecran"]
    ETAT.update(slug=slug, plan=plan, tl=tl, scenes=scenes, src=src, vignette=vignette, part=part, sprites=sprites,
                brume_tex=br, brume=brume, cache={},
                intro=grand_titre(ecran["titre"], 88, ecran.get("sous_titre")),
                credit=petit(ecran.get("credit", "Musique : « Deep Relaxation », Kevin MacLeod (incompetech.com) · CC BY 4.0 · "
                                                  "photos Unsplash · voix de synthèse"), 24, 46),
                marque_debut=petit(f"Clarté Mentale · {SITE.split('//')[1].strip('/').replace('www.', '')} · {CHAINE}", 28, 84),
                marque=petit(f"Clarté Mentale · {SITE.split('//')[1].strip('/').replace('www.', '')} · {CHAINE}", 30, H - 110))


def sous_titre(txt):
    f = police("Lora-Regular.ttf", 46)
    mots, lignes, cur = txt.split(), [], ""
    for m in mots:
        e = (cur + " " + m).strip()
        if f.getlength(e) > 1500 and cur:
            lignes.append(cur)
            cur = m
        else:
            cur = e
    lignes.append(cur)
    lh = 62
    larg = int(max(f.getlength(l) for l in lignes)) + 80
    ht = lh * len(lignes) + 40
    im = Image.new("RGBA", (larg, ht), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, larg - 1, ht - 1], radius=26, fill=(6, 8, 24, 160))
    for i, l in enumerate(lignes):
        d.text((larg / 2, 20 + lh * i + lh / 2), l, font=f, fill=(246, 242, 232, 255), anchor="mm")
    return np.array(im, np.float32), (W - larg) // 2, H - 90 - ht


def grand_titre(txt, taille=84, sous=None):
    f = police("PlayfairDisplay-Bold.ttf", taille)
    while f.getlength(txt) > W - 160:
        taille -= 4
        f = police("PlayfairDisplay-Bold.ttf", taille)
    im = Image.new("RGBA", (W, 400), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((W / 2, 150), txt, font=f, fill=(250, 244, 226, 255), anchor="mm")
    d.line([(W / 2 - 60, 232), (W / 2 + 60, 232)], fill=(222, 196, 140, 220), width=2)
    if sous:
        d.text((W / 2, 288), sous, font=police("Lora-Regular.ttf", 38), fill=(220, 226, 248, 235), anchor="mm")
    ombre = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ombre.putalpha(im.getchannel("A").filter(ImageFilter.GaussianBlur(18)).point(lambda v: v * 0.8))
    return np.array(Image.alpha_composite(ombre, im), np.float32), 0, H // 2 - 260


def petit(txt, taille=26, y=H - 54):
    f = police("Lora-Regular.ttf", taille)
    im = Image.new("RGBA", (W, 50), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((W / 2, 25), txt, font=f, fill=(210, 214, 236, 215), anchor="mm")
    return np.array(im, np.float32), 0, y - 25


def poser(img, c, alpha, dy=0):
    arr, x, y0 = c
    y0 = int(y0 + dy)
    if alpha <= 0.003:
        return
    h, w = arr.shape[:2]
    zone = img[y0:y0 + h, x:x + w]
    a = arr[..., 3:4] / 255.0 * alpha
    zone *= 1 - a
    zone += arr[..., :3] * a


def cercle(rayon, txt):
    Z = 820
    im = Image.new("RGBA", (Z, Z), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = Z // 2
    d.ellipse([c - rayon - 30, c - rayon - 30, c + rayon + 30, c + rayon + 30], fill=(150, 170, 255, 80))
    im = im.filter(ImageFilter.GaussianBlur(34))
    d = ImageDraw.Draw(im)
    d.ellipse([c - rayon, c - rayon, c + rayon, c + rayon], fill=(150, 165, 240, 46), outline=(232, 236, 255, 225), width=3)
    if txt:
        d.text((c, c), txt, font=police("PlayfairDisplay-Bold.ttf", 54), fill=(252, 248, 236, 240), anchor="mm")
    return np.array(im, np.float32), W // 2 - c, H // 2 - 40 - c


def plan_photo(nom, i, t, d0, d1):
    z0, z1, px, py = MOUV[i % len(MOUV)]
    u = lisse((t - d0) / max(1, d1 - d0 + FONDU))
    z = z0 + (z1 - z0) * u
    src = ETAT["src"][nom]
    cw, ch = min(W * 1.18 / z, src.width), min(H * 1.18 / z, src.height)
    cx = src.width / 2 + px * (src.width - cw) / 2 * (u - 0.5) * 2 * 0.9
    cy = src.height / 2 + py * (src.height - ch) / 2 * (u - 0.5) * 2 * 0.9
    x0 = min(max(0.0, cx - cw / 2), src.width - cw)
    y0 = min(max(0.0, cy - ch / 2), src.height - ch)
    return np.asarray(src.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)), np.float32)


def particules(img, t, force):
    if force <= 0.01:
        return
    p, sp = ETAT["part"], ETAT["sprites"]
    coul = np.array([255, 226, 170], np.float32)
    for i in range(len(p["x"])):
        x = (p["x"][i] + 25 * math.sin(t * 0.13 + p["ph"][i])) % W
        y = (p["y"][i] - p["v"][i] * t) % (H + 60) - 30
        s = min(5, max(2, int(round(p["s"][i]))))
        k = sp[s].shape[0]
        x0, y0 = int(x) - k // 2, int(y) - k // 2
        if 0 <= x0 < W - k and 0 <= y0 < H - k:
            a = p["a"][i] * (0.55 + 0.45 * math.sin(t * 0.9 + p["ph"][i] * 3)) * force
            img[y0:y0 + k, x0:x0 + k] += sp[s][..., None] * coul * a


def calque(cle, fab):
    c = ETAT["cache"]
    if cle not in c:
        c[cle] = fab()
    return c[cle]


def image(t):
    tl = ETAT["tl"]
    duree, fin_voix = tl["duree"], tl["fin_voix"]
    img = None
    for i, (nom, d0, d1) in enumerate(ETAT["scenes"]):
        if d0 - FONDU <= t < d1 + 0.01 or (i == 0 and t < d1):
            a = 1.0 if i == 0 else lisse((t - (d0 - FONDU)) / FONDU)
            p = plan_photo(nom, i, t, d0 - FONDU, d1)
            img = p if img is None or a >= 1 else img * (1 - a) + p * a
    img = img * ETAT["vignette"]
    for d0, d1 in ETAT["brume"]:
        fb = fondu(t, d0 - 2, d1 + 4, 6)
        if fb > 0.01:
            dx = int((t * 22) % W)
            m = ETAT["brume_tex"][:, dx:dx + W][..., None] * 0.30 * fb
            img = img * (1 - m) + np.array([190, 200, 230], np.float32) * m
    so = tl["souffles"]
    cyc = tl["insp"] + tl["exp"]
    resp = any(s["debut"] - 3 < t < s["debut"] + s["cycles"] * cyc + 3 for s in so)
    particules(img, t, (0.45 if resp else 1.0) * (1 - 0.8 * lisse((t - fin_voix) / 40)))
    poser(img, ETAT["intro"], fondu(t, 1.0, 12.0, 2.0), dy=(1 - lisse((t - 1.0) / 3)) * 24)
    poser(img, ETAT["credit"], fondu(t, 2.0, 12.0, 2.0))
    for ti in tl["titres"]:
        if ti["debut"] - 1 < t < ti["fin"] + 1:
            poser(img, calque(("t", ti["texte"]), lambda: grand_titre(ti["texte"], 76)), fondu(t, ti["debut"], ti["fin"], 1.8),
                  dy=(1 - lisse((t - ti["debut"]) / 2.5)) * 30)
    for s in so:
        fin = s["debut"] + s["cycles"] * cyc
        if s["debut"] - 2 < t < fin + 2:
            al = fondu(t, s["debut"] - 1.5, fin + 1.5, 1.5)
            u = (t - s["debut"]) % cyc if t >= s["debut"] else 0
            if t < s["debut"] or t > fin:
                r, txt = 110, ""
            elif u < tl["insp"]:
                r, txt = 110 + 150 * lisse(u / tl["insp"]), "Inspire"
            else:
                r, txt = 260 - 150 * lisse((u - tl["insp"]) / tl["exp"]), "Expire"
            poser(img, cercle(int(r), txt), al)
    for c in tl["cues"]:
        if c["debut"] - 0.5 < t < c["fin"] + 1.0 and c["texte"] not in ("Inspire…", "Expire…"):
            poser(img, calque(("s", c["texte"]), lambda: sous_titre(c["texte"])), fondu(t, c["debut"] - 0.25, c["fin"] + 0.7, 0.4),
                  dy=(1 - lisse((t - c["debut"] + 0.25) / 0.6)) * 12)
    if t > fin_voix:
        img = img * (1 - 0.6 * lisse((t - fin_voix) / 60))
    # au début, crédits et adresse en haut (les sous-titres occupent le bas) ; à la fin, adresse en bas
    poser(img, ETAT["marque_debut"], fondu(t, 2.5, 12.0, 2.0) * 0.9)
    poser(img, ETAT["marque"], fondu(t, duree - 25, duree - 1, 3) * 0.9)
    img = img * (min(1.0, t / 1.5) * min(1.0, (duree - t) / 3.0))
    return img.clip(0, 255).astype(np.uint8)


def _morceau(args):
    slug, i0, i1, sortie = args
    preparer(slug)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                          "-tune", "film", "-threads", "1", sortie], stdin=subprocess.PIPE)
    for i in range(i0, i1):
        p.stdin.write(image(i / FPS).tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError(f"ffmpeg a échoué sur {sortie}")
    return sortie


def fabriquer(slug, processus=None):
    trav = dossier_travail(slug)
    tl = json.load(open(os.path.join(trav, "timeline.json")))
    n = math.ceil(tl["duree"] * FPS)
    k = processus or max(1, os.cpu_count() or 1)
    b = [round(n * i / k) for i in range(k + 1)]
    parts = [os.path.join(trav, f"_part{i}.mp4") for i in range(k)]
    with Pool(k) as pool:
        pool.map(_morceau, [(slug, b[i], b[i + 1], parts[i]) for i in range(k)])
    liste = os.path.join(trav, "_liste.txt")
    open(liste, "w").write("".join(f"file '{p}'\n" for p in parts))
    sortie = os.path.join(trav, "video.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", liste, "-i", os.path.join(trav, "piste.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                    "-shortest", sortie], check=True)
    for p in parts:
        os.remove(p)
    print("vidéo :", sortie)
    return sortie


if __name__ == "__main__":
    if len(sys.argv) > 3:  # python3 rendu.py slug t image.jpg : une image de contrôle
        preparer(sys.argv[1])
        Image.fromarray(image(float(sys.argv[2]))).save(sys.argv[3], quality=88)
    else:
        fabriquer(sys.argv[1])
