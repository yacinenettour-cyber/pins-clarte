"""Photos (téléchargement), miniature, Short vertical et sous-titres d'une vidéo."""
import io, json, math, os, subprocess, sys
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from commun import POLICES, SITE, FPS, dossier_plan, dossier_travail, lire_plan, lisse, fondu, mmss


def police(nom, t):
    return ImageFont.truetype(os.path.join(POLICES, nom), t)


def telecharger_photos(slug):
    """Photos libres de droits listées dans le plan (Unsplash : usage gratuit), en 2400 px au plus."""
    plan, trav = lire_plan(slug), dossier_travail(slug)
    d = os.path.join(trav, "photos")
    os.makedirs(d, exist_ok=True)
    for ph in plan["photos"]:
        chemin = os.path.join(d, ph["nom"])
        if os.path.exists(chemin):
            continue
        r = requests.get(ph["url"], timeout=90, headers={"User-Agent": "Mozilla/5.0 (compatible; pins-clarte/1.0)"})
        r.raise_for_status()
        im = Image.open(io.BytesIO(r.content)).convert("RGB")
        if im.width > 2400:
            im = im.resize((2400, round(im.height * 2400 / im.width)), Image.LANCZOS)
        assert im.width >= 1600, f"photo trop petite : {ph['nom']} ({im.size})"
        im.save(chemin, "JPEG", quality=90)
    print(len(plan["photos"]), "photos prêtes")


def miniature(slug):
    """1280×720 : photo choisie, texte en 3 lignes à gauche, pastille dorée."""
    plan, trav = lire_plan(slug), dossier_travail(slug)
    m = plan["miniature"]
    W, H = 1280, 720
    im = Image.open(os.path.join(trav, "photos", m["photo"])).convert("RGB")
    r = max(W * m.get("zoom", 1.0) / im.width, H * m.get("zoom", 1.0) / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x0 = int((im.width - W) * m.get("cadrage_x", 0.5))
    y0 = int((im.height - H) * m.get("cadrage_y", 0.5))
    im = im.crop((x0, y0, x0 + W, y0 + H))
    a = np.asarray(im, np.float32) * np.array([0.85, 0.88, 1.0])
    a *= 1 - 0.62 * (np.linspace(1, 0, W)[None, :, None] ** 1.6)
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    txt = Image.new("RGBA", (W, H))
    t = ImageDraw.Draw(txt)

    def ajuste(texte, nom, taille, largeur=640):
        f = police(nom, taille)
        while f.getlength(texte) > largeur:
            taille -= 4
            f = police(nom, taille)
        return f
    t.text((70, 150), m["ligne1"], font=ajuste(m["ligne1"], "PlayfairDisplay-Bold.ttf", 104), fill=(255, 248, 228, 255))
    t.text((70, 268), m["ligne2"], font=ajuste(m["ligne2"], "PlayfairDisplay-Bold.ttf", 104), fill=(255, 214, 140, 255))
    t.text((74, 400), m["ligne3"], font=ajuste(m["ligne3"], "PlayfairDisplay-Bold.ttf", 64), fill=(236, 238, 255, 255))
    f3 = ajuste(m["pastille"], "Lora-SemiBold.ttf", 40, 520)
    lp = int(f3.getlength(m["pastille"])) + 70
    t.rounded_rectangle([70, 520, 70 + lp, 590], radius=34, fill=(255, 214, 140, 235))
    t.text((70 + lp / 2, 555), m["pastille"], font=f3, fill=(20, 22, 48, 255), anchor="mm")
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh.putalpha(txt.getchannel("A").filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.85)))
    im = Image.alpha_composite(Image.alpha_composite(im.convert("RGBA"), sh), txt).convert("RGB")
    sortie = os.path.join(dossier_plan(slug), "miniature.jpg")
    im.save(sortie, quality=90)
    assert os.path.getsize(sortie) < 2_000_000
    return sortie


def sous_titres(slug):
    trav = dossier_travail(slug)
    tl = json.load(open(os.path.join(trav, "timeline.json")))

    def ts(s):
        ms = int(round(s * 1000))
        h, ms = divmod(ms, 3600000)
        m, ms = divmod(ms, 60000)
        se, ms = divmod(ms, 1000)
        return f"{h:02d}:{m:02d}:{se:02d},{ms:03d}"
    sortie = os.path.join(dossier_plan(slug), "sous-titres.srt")
    with open(sortie, "w", encoding="utf-8") as f:
        for i, c in enumerate(tl["cues"], 1):
            f.write(f"{i}\n{ts(c['debut'])} --> {ts(c['fin'] + 0.6)}\n{c['texte']}\n\n")
    return sortie


from metadonnees import chapitres  # noqa: E402 (défini une seule fois, dans metadonnees.py)


# ---------- Short vertical (1080×1920, 30 i/s) : la première respiration guidée ----------
SW, SH, SFPS = 1080, 1920, 30


def short(slug):
    """Short principal : la première respiration guidée (travail/<slug>/short.mp4)."""
    plan, trav = lire_plan(slug), dossier_travail(slug)
    tl = json.load(open(os.path.join(trav, "timeline.json")))
    if not tl["souffles"]:
        print("pas de respiration guidée : pas de Short")
        return None
    s = tl["souffles"][0]
    cyc = tl["insp"] + tl["exp"]
    d0 = max(0.0, s["debut"] - 16.5)
    d1 = s["debut"] + s["cycles"] * cyc + 5
    ph = next((p for p in plan["photos"] if p.get("short")), plan["photos"][1])
    return _short(trav, tl, plan.get("short", {}), ph, d0, d1, s, os.path.join(trav, "short.mp4"))


def shorts_extra(slug):
    """Shorts supplémentaires (27/10/2026, 3 Shorts par vidéo : le meilleur moyen pour une chaîne sans abonnés d'être
    découverte) : un extrait d'une partie de la pratique (plan["shorts_extra"] = [{"partie": titre de la partie,
    "haut1", "haut2", "bas1", "titre", "description"}]), 60 s au plus, avec la photo de cette partie.
    Fichiers : travail/<slug>~short2/short.mp4, ~short3… (même motif que le Short principal pour l'artefact du run)."""
    plan, trav = lire_plan(slug), dossier_travail(slug)
    tl = json.load(open(os.path.join(trav, "timeline.json")))
    sorties = []
    for k, sp in enumerate(plan.get("shorts_extra", []), 2):
        i = next(j for j, t in enumerate(tl["titres"]) if t["texte"] == sp["partie"])
        t0 = tl["titres"][i]["debut"]
        suivant = tl["titres"][i + 1]["debut"] if i + 1 < len(tl["titres"]) else tl["fin_voix"] + 6
        d0 = max(0.0, t0 - 0.5)
        # finir après la dernière phrase entièrement dite avant 60 s, avec le temps de relâcher
        fins = [c["fin"] for c in tl["cues"] if t0 <= c["debut"] and c["fin"] < min(suivant, d0 + 54)]
        d1 = min(suivant - 0.3, (max(fins) if fins else t0 + 30) + 6, d0 + 60)
        ph = plan["photos"][i + 1]
        d = os.path.join(os.path.dirname(trav), f"{slug}~short{k}")
        os.makedirs(d, exist_ok=True)
        sorties.append(_short(trav, tl, sp, ph, d0, d1, None, os.path.join(d, "short.mp4")))
    return sorties


def _short(trav, tl, sh, ph, d0, d1, s, sortie):
    """Short vertical entre d0 et d1 ; s = respiration guidée à animer (cercle), ou None."""
    src = Image.open(os.path.join(trav, "photos", ph["nom"])).convert("RGB")
    r = SH * 1.12 / src.height
    src = src.resize((max(round(src.width * r), int(SW * 1.2)), round(src.height * r)), Image.LANCZOS)
    a = np.asarray(src, np.float32) * np.array([0.80, 0.84, 0.95]) * ph.get("lum", 0.85)
    src = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    yy, xx = np.mgrid[0:SH, 0:SW]
    vig = (1 - 0.5 * (((xx - SW / 2) / (SW * 0.7)) ** 2 + ((yy - SH / 2) / (SH * 0.62)) ** 2)).clip(0.35, 1).astype(np.float32)[..., None]

    def bloc(lignes, tailles, couleurs, polices_, fond_=None):
        hs = [int(t * 1.35) for t in tailles]
        im = Image.new("RGBA", (SW, sum(hs) + 40), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        if fond_:
            d.rounded_rectangle([60, 0, SW - 60, im.height - 1], radius=30, fill=fond_)
        y = 20
        for l, t, c, p, h in zip(lignes, tailles, couleurs, polices_, hs):
            f = police(p, t)
            while f.getlength(l) > SW - 140:
                t -= 2
                f = police(p, t)
            d.text((SW / 2, y + h / 2), l, font=f, fill=c, anchor="mm")
            y += h
        om = Image.new("RGBA", im.size, (0, 0, 0, 0))
        om.putalpha(im.getchannel("A").filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.7)))
        return np.array(Image.alpha_composite(om, im), np.float32)
    haut = bloc([sh.get("haut1", "Respire avec moi"), sh.get("haut2", "pour t'endormir")], [86, 86],
                [(255, 248, 230, 255), (255, 214, 140, 255)], ["PlayfairDisplay-Bold.ttf"] * 2)
    bas = bloc([sh.get("bas1", "Méditation complète sur la chaîne"), "contactapaisement-mental.fr"], [42, 34],
               [(250, 246, 236, 255), (255, 214, 140, 240)], ["Lora-SemiBold.ttf", "Lora-Regular.ttf"], fond_=(8, 10, 30, 170))
    cache = {}

    def sous(txt):
        if txt in cache:
            return cache[txt]
        f = police("Lora-Regular.ttf", 50)
        mots, lignes, cur = txt.split(), [], ""
        for m in mots:
            e = (cur + " " + m).strip()
            if f.getlength(e) > 880 and cur:
                lignes.append(cur)
                cur = m
            else:
                cur = e
        lignes.append(cur)
        lh = 68
        larg = int(max(f.getlength(l) for l in lignes)) + 70
        ht = lh * len(lignes) + 36
        im = Image.new("RGBA", (larg, ht), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, larg - 1, ht - 1], radius=26, fill=(6, 8, 24, 165))
        for i, l in enumerate(lignes):
            d.text((larg / 2, 18 + lh * i + lh / 2), l, font=f, fill=(246, 242, 232, 255), anchor="mm")
        cache[txt] = np.array(im, np.float32)
        return cache[txt]

    def poser(img, arr, x, y, al):
        if al <= 0.003:
            return
        h, w = arr.shape[:2]
        z = img[y:y + h, x:x + w]
        aa = arr[..., 3:4] / 255 * al
        z *= 1 - aa
        z += arr[..., :3] * aa

    def cercle(r, txt):
        Z = 900
        im = Image.new("RGBA", (Z, Z), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        c = Z // 2
        d.ellipse([c - r - 34, c - r - 34, c + r + 34, c + r + 34], fill=(150, 170, 255, 85))
        im = im.filter(ImageFilter.GaussianBlur(36))
        d = ImageDraw.Draw(im)
        d.ellipse([c - r, c - r, c + r, c + r], fill=(150, 165, 240, 48), outline=(232, 236, 255, 230), width=4)
        if txt:
            d.text((c, c), txt, font=police("PlayfairDisplay-Bold.ttf", 64), fill=(252, 248, 236, 245), anchor="mm")
        return np.array(im, np.float32)

    def image(t):
        u = (t - d0) / (d1 - d0)
        z = 1.0 + 0.08 * u
        cw, ch = min(SW * 1.12 / z, src.width), min(SH * 1.12 / z, src.height)
        cx = src.width * 0.5 + (src.width - cw) * 0.35 * (u - 0.5)
        x0 = min(max(0.0, cx - cw / 2), src.width - cw)
        y0 = min(max(0.0, src.height / 2 - ch / 2), src.height - ch)
        img = np.asarray(src.resize((SW, SH), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)), np.float32) * vig
        poser(img, haut, 0, 90, fondu(t, d0 + 0.2, d1 + 9, 0.8))
        if s:
            cyc = tl["insp"] + tl["exp"]
            uu = (t - s["debut"]) % cyc if t >= s["debut"] else 0
            fin = s["debut"] + s["cycles"] * cyc
            if t < s["debut"] or t > fin:
                r, txt = 130, ""
            elif uu < tl["insp"]:
                r, txt = 130 + 170 * lisse(uu / tl["insp"]), "Inspire"
            else:
                r, txt = 300 - 170 * lisse((uu - tl["insp"]) / tl["exp"]), "Expire"
            poser(img, cercle(int(r), txt), (SW - 900) // 2, 760 - 450, fondu(t, d0 + 1, d1 + 9, 1.2))
        for c in tl["cues"]:
            if d0 - 1 < c["debut"] < d1 and c["texte"] not in ("Inspire…", "Expire…") and c["debut"] - 0.3 < t < c["fin"] + 0.9:
                arr = sous(c["texte"])
                poser(img, arr, (SW - arr.shape[1]) // 2, 1110, fondu(t, c["debut"] - 0.2, c["fin"] + 0.7, 0.35))
        poser(img, bas, 0, 1440, fondu(t, d0 + 1.5, d1 + 9, 0.8))
        img *= min(1, (t - d0) / 0.6) * min(1, (d1 - t) / 1.0)
        return img.clip(0, 255).astype(np.uint8)

    dur = d1 - d0
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{SW}x{SH}", "-r", str(SFPS),
                          "-i", "-", "-ss", f"{d0:.3f}", "-t", f"{dur:.3f}", "-i", os.path.join(trav, "piste.wav"),
                          "-af", f"afade=t=in:d=0.6,afade=t=out:st={dur - 1.5:.3f}:d=1.5",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", sortie], stdin=subprocess.PIPE)
    for i in range(int(dur * SFPS)):
        p.stdin.write(image(d0 + i / SFPS).tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError("ffmpeg a échoué sur le Short")
    print("Short :", sortie, f"{dur:.1f} s")
    return sortie


if __name__ == "__main__":
    {"photos": telecharger_photos, "miniature": miniature, "short": short, "shorts_extra": shorts_extra,
     "srt": sous_titres}[sys.argv[1]](sys.argv[2])
