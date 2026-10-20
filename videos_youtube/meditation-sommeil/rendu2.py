"""Version 2 : une photo par partie (zoom lent + léger déplacement, fondus enchaînés), particules lumineuses,
brume qui passe, cercle de respiration, titres et sous-titres animés.
Usage : python3 rendu2.py t sortie.jpg   (une image)   |   seg.py appelle image(t)."""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
POL = "/home/user/pins-clarte/polices/"
PHOTOS = json.load(open(f"{ICI}/photos.json"))  # {"intro": "chemin", "S'installer": ..., "fin": ...}
W, H, FPS = 1920, 1080, 24
TL = json.load(open(f"{ICI}/timeline.json"))
DUREE, FIN_VOIX = TL["duree"], TL["fin_voix"]
rng = np.random.default_rng(20261020)
FONDU = 5.0


def police(nom, t):
    return ImageFont.truetype(POL + nom, t)


def lisse(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def fondu(t, d, f, e=1.2):
    return lisse((t - d) / e) * lisse((f - t) / e)


# ---------- scènes : une photo par partie ----------
SCENES = [("intro", 0.0)] + [(ti["texte"], ti["debut"] - 1.0) for ti in TL["titres"]] + [("fin", FIN_VOIX + 4)]
SCENES = [(nom, d0, (SCENES[i + 1][1] if i + 1 < len(SCENES) else DUREE + 1)) for i, (nom, d0) in enumerate(SCENES)]
# mouvement propre à chaque scène : zoom avant ou arrière, et direction du glissement
MOUV = [(1.0, 1.13, -0.4, 0.2), (1.12, 1.0, 0.5, 0.0), (1.0, 1.10, 0.0, -0.4), (1.10, 1.0, -0.5, 0.3),
        (1.0, 1.12, 0.6, 0.0), (1.0, 1.15, 0.0, 0.5), (1.12, 1.0, -0.3, -0.2), (1.0, 1.08, 0.3, 0.0)]
SRC = {}
for nom, _, _ in SCENES:
    im = Image.open(os.path.join(ICI, "photos", PHOTOS[nom])).convert("RGB")
    # recadrage 16:9 couvrant, avec marge pour le zoom ; étalonnage de nuit (plus sombre, un peu plus froid)
    r = max(W * 1.18 / im.width, H * 1.18 / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    a = np.asarray(im, np.float32)
    a = a * np.array([0.80, 0.84, 0.95], np.float32) * PHOTOS.get("_lum", {}).get(nom, 0.82)
    SRC[nom] = Image.fromarray(a.clip(0, 255).astype(np.uint8))

yy, xx = np.mgrid[0:H, 0:W]
VIGNETTE = (1 - 0.55 * (((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)).clip(0.35, 1).astype(np.float32)[..., None]


def plan(nom, i, t, d0, d1):
    z0, z1, px, py = MOUV[i % len(MOUV)]
    u = lisse((t - d0) / max(1, d1 - d0 + FONDU)) if True else 0
    z = z0 + (z1 - z0) * u
    src = SRC[nom]
    cw, ch = W * 1.18 / z, H * 1.18 / z
    cx = src.width / 2 + px * (src.width - cw) / 2 * (u - 0.5) * 2 * 0.9
    cy = src.height / 2 + py * (src.height - ch) / 2 * (u - 0.5) * 2 * 0.9
    box = (cx - cw / 2 * W / (W * 1.18) * 1.18, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    return np.asarray(src.resize((W, H), Image.BILINEAR, box=box), np.float32)


# ---------- particules lumineuses (poussière dorée qui monte lentement) ----------
NP = 70
P_X, P_Y = rng.uniform(0, W, NP), rng.uniform(0, H, NP)
P_V, P_S = rng.uniform(6, 18, NP), rng.uniform(1.5, 4.5, NP)
P_PH, P_A = rng.uniform(0, 2 * math.pi, NP), rng.uniform(0.25, 0.8, NP)
SPRITES = {}
for s in (2, 3, 4, 5):
    k = 8 * s + 1
    g = np.mgrid[0:k, 0:k] - k // 2
    SPRITES[s] = np.exp(-(g[0] ** 2 + g[1] ** 2) / (2 * (0.9 * s) ** 2)).astype(np.float32)
P_COUL = np.array([255, 226, 170], np.float32)


def particules(img, t, force):
    if force <= 0.01:
        return
    for i in range(NP):
        x = (P_X[i] + 25 * math.sin(t * 0.13 + P_PH[i])) % W
        y = (P_Y[i] - P_V[i] * t) % (H + 60) - 30
        s = int(round(P_S[i]))
        s = min(5, max(2, s))
        sp = SPRITES[s]; k = sp.shape[0]
        x0, y0 = int(x) - k // 2, int(y) - k // 2
        if 0 <= x0 < W - k and 0 <= y0 < H - k:
            a = P_A[i] * (0.55 + 0.45 * math.sin(t * 0.9 + P_PH[i] * 3)) * force
            img[y0:y0 + k, x0:x0 + k] += sp[..., None] * P_COUL * a


# ---------- brume qui passe (pensées comme des nuages) ----------
bw = W * 2
brume = rng.random((H // 16, bw // 16)).astype(np.float32)
brume = np.asarray(Image.fromarray((brume * 255).astype(np.uint8)).resize((bw, H), Image.BICUBIC)
                   .filter(ImageFilter.GaussianBlur(60)), np.float32) / 255.0
brume = ((brume - brume.mean()) * 3.2 + 0.5).clip(0, 1) * np.linspace(0.3, 1, H, dtype=np.float32)[:, None]
B_COUL = np.array([190, 200, 230], np.float32)

# ---------- textes ----------
CACHE = {}


def calque(cle, fab):
    if cle not in CACHE:
        CACHE[cle] = fab()
    return CACHE[cle]


def sous_titre(txt):
    f = police("Lora-Regular.ttf", 46)
    mots, lignes, cur = txt.split(), [], ""
    for m in mots:
        e = (cur + " " + m).strip()
        if f.getlength(e) > 1500 and cur:
            lignes.append(cur); cur = m
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


INTRO = grand_titre("Méditation guidée pour le sommeil", 88, "11 minutes · voix douce · musique relaxante")
CREDIT = petit("Musique : « Deep Relaxation », Kevin MacLeod (incompetech.com) · CC BY 4.0 · photos Unsplash · voix de synthèse")
MARQUE = petit("Clarté Mentale · contactapaisement-mental.fr", 30, H - 110)


def image(t):
    # photo(s) de la scène, avec fondu enchaîné
    img = None
    for i, (nom, d0, d1) in enumerate(SCENES):
        if d0 - FONDU <= t < d1 + 0.01 or (i == 0 and t < d1):
            a = 1.0 if i == 0 else lisse((t - (d0 - FONDU)) / FONDU)
            p = plan(nom, i, t, d0 - FONDU, d1)
            img = p if img is None or a >= 1 else img * (1 - a) + p * a
    img = img * VIGNETTE
    # brume qui dérive pendant « Laisser passer les pensées » et « Le ciel étoilé »
    for ti in TL["titres"]:
        if ti["texte"] == "Laisser passer les pensées":
            fin = next((x["debut"] for x in TL["titres"] if x["debut"] > ti["debut"]), DUREE)
            fb = fondu(t, ti["debut"] - 2, fin + 4, 6)
            if fb > 0.01:
                dx = int((t * 22) % W)
                m = brume[:, dx:dx + W][..., None] * 0.30 * fb
                img = img * (1 - m) + B_COUL * m
    # particules (moins nombreuses pendant la respiration, presque éteintes à la fin)
    so = TL["souffles"]
    resp = any(s["debut"] - 3 < t < s["debut"] + s["cycles"] * 10 + 3 for s in so)
    particules(img, t, (0.45 if resp else 1.0) * (1 - 0.8 * lisse((t - FIN_VOIX) / 40)))
    # intro
    a = fondu(t, 1.5, 13.0, 2.2)
    poser(img, INTRO, a, dy=(1 - lisse((t - 1.5) / 3)) * 24)
    poser(img, CREDIT, fondu(t, 2.5, 13.0, 2.0))
    # titres de partie : apparaissent en montant doucement
    for ti in TL["titres"]:
        if ti["debut"] - 1 < t < ti["fin"] + 1:
            poser(img, calque(("t", ti["texte"]), lambda: grand_titre(ti["texte"], 76)), fondu(t, ti["debut"], ti["fin"], 1.8),
                  dy=(1 - lisse((t - ti["debut"]) / 2.5)) * 30)
    # cercle de respiration
    for s in so:
        cyc = TL["insp"] + TL["exp"]
        fin = s["debut"] + s["cycles"] * cyc
        if s["debut"] - 2 < t < fin + 2:
            al = fondu(t, s["debut"] - 1.5, fin + 1.5, 1.5)
            u = (t - s["debut"]) % cyc if t >= s["debut"] else 0
            if t < s["debut"]:
                r, txt = 110, ""
            elif u < TL["insp"]:
                r, txt = 110 + 150 * lisse(u / TL["insp"]), "Inspire"
            else:
                r, txt = 260 - 150 * lisse((u - TL["insp"]) / TL["exp"]), "Expire"
            if t > fin:
                txt = ""
            poser(img, cercle(int(r), txt), al)
    # sous-titres : fondu et légère montée
    for c in TL["cues"]:
        if c["debut"] - 0.5 < t < c["fin"] + 1.0 and c["texte"] not in ("Inspire…", "Expire…"):
            poser(img, calque(("s", c["texte"]), lambda: sous_titre(c["texte"])), fondu(t, c["debut"] - 0.25, c["fin"] + 0.7, 0.4),
                  dy=(1 - lisse((t - c["debut"] + 0.25) / 0.6)) * 12)
    # après la voix : l'image s'assombrit doucement
    if t > FIN_VOIX:
        img = img * (1 - 0.55 * lisse((t - FIN_VOIX) / 45))
    # adresse du site : pendant l'intro (au-dessus des crédits) puis à la toute fin
    poser(img, MARQUE, max(fondu(t, 3.0, 13.0, 2.0), fondu(t, DUREE - 22, DUREE - 1, 3)) * 0.9)
    img = img * (min(1.0, t / 2.0) * min(1.0, (DUREE - t) / 3.0))
    return img.clip(0, 255).astype(np.uint8)


if __name__ == "__main__":
    Image.fromarray(image(float(sys.argv[1]))).save(sys.argv[2], quality=88)
