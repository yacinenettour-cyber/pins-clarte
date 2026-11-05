"""Logo et bannière de la boutique Etsy « Clarté Mentale ».
02/11/2026 : demande « il me faut un nom, etc. », puis « fais plus un truc qualitatif et ne marque pas planner » :
monogramme CM dans une arche (rappel de la couverture), botanique au trait fin, filets dorés, aucune mention « planner ».
Dessiné par programme (polices OFL de polices/), rendu à 2× puis réduit pour des traits nets ; aucune IA, rien de payant.
Usage : python3 outils/etsy/boutique_visuels.py → etsy/boutique/logo-500.png, banniere-3360x840.jpg
"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import sys
# 05/11/2026 : la boutique s'appelle finalement « HestiaAura » (choix de l'utilisateur à l'inscription). Usage :
#   python3 outils/etsy/boutique_visuels.py            → Clarté Mentale (logo-500.png, banniere-3360x840.jpg)
#   python3 outils/etsy/boutique_visuels.py hestiaaura → logo-hestiaaura-500.png, banniere-hestiaaura-3360x840.jpg
MARQUES = {"clarte": ("CM", "CLARTÉ MENTALE", ""), "hestiaaura": ("HA", "HESTIA AURA", "-hestiaaura")}
CLE = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in MARQUES else "clarte"
MONO, NOM, SUFFIXE = MARQUES[CLE]
ICI = os.path.dirname(os.path.abspath(__file__))
POL = os.path.join(ICI, "..", "..", "polices") + "/"
SORTIE = os.path.join(ICI, "..", "..", "etsy", "boutique")
MARQUE = (146, 70, 52); MARQUE_F = (118, 54, 40); CREME = (247, 240, 228); OR = (196, 156, 96)
OR_C = (226, 196, 150); BRUN = (74, 52, 36); SAUGE = (128, 146, 120)
f = lambda n, t: ImageFont.truetype(POL + n, t)
TITRE = lambda t: f("PlayfairDisplay-Bold.ttf", t)
MAIN = lambda t: f("DancingScript-Bold.ttf", t)
TEXTE = lambda t: f("Lora-Regular.ttf", t)
GRAS = lambda t: f("Lora-SemiBold.ttf", t)


def papier(w, h, base, force=4, vignette=0.0, seed=3):
    rng = np.random.default_rng(seed)
    a = np.ones((h, w, 3), np.float32) * np.array(base, np.float32) + rng.normal(0, force, (h, w, 1))
    if vignette:
        yy, xx = np.mgrid[0:h, 0:w]
        r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
        a *= (1 - vignette * np.clip(r - 0.4, 0, None))[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))


def texte_espace(d, x_centre, y, t, fo, fill, pas):
    w = sum(d.textlength(c, font=fo) for c in t) + pas * (len(t) - 1)
    x = x_centre - w / 2
    for c in t:
        d.text((x, y), c, font=fo, fill=fill); x += d.textlength(c, font=fo) + pas
    return w


def feuille_trait(d, x, y, ang, lg, larg, couleur, ep):
    ux, uy = math.cos(ang), math.sin(ang); vx, vy = -uy, ux
    a, b = [], []
    for k in range(25):
        t = k / 24; w = math.sin(math.pi * t) ** 0.85 * larg
        px, py = x + ux * lg * t, y + uy * lg * t
        a.append((px + vx * w, py + vy * w)); b.append((px - vx * w, py - vy * w))
    d.line(a + b[::-1] + [a[0]], fill=couleur, width=ep, joint="curve")
    d.line([(x, y), (x + ux * lg * 0.85, y + uy * lg * 0.85)], fill=couleur, width=max(1, ep // 2))


def brin_trait(d, x, y, hauteur, courbe, couleur, ep, n=6, taille=1.0):
    """Branche au trait fin : tige courbe et feuilles en contour, alternées."""
    pts = [(x + courbe * math.sin(t / 40 * 2.2), y - hauteur * t / 40) for t in range(41)]
    d.line(pts, fill=couleur, width=ep, joint="curve")
    for i in range(n):
        k = 6 + i * (32 // n)
        px, py = pts[k]; cote = 1 if i % 2 else -1; t = k / 40
        ang = -math.pi / 2 + cote * (1.0 - 0.35 * t)
        feuille_trait(d, px, py, ang, (hauteur * 0.30) * (1 - 0.4 * t) * taille, (hauteur * 0.075) * (1 - 0.3 * t) * taille,
                      couleur, ep)
    feuille_trait(d, pts[-1][0], pts[-1][1], -math.pi / 2, hauteur * 0.2 * taille, hauteur * 0.055 * taille, couleur, ep)


def arche(d, x0, y0, x1, y1, couleur, ep):
    r = (x1 - x0) / 2
    d.arc((x0, y0, x1, y0 + 2 * r), 180, 360, fill=couleur, width=ep)
    d.line((x0, y0 + r, x0, y1), fill=couleur, width=ep)
    d.line((x1, y0 + r, x1, y1), fill=couleur, width=ep)
    d.line((x0, y1, x1, y1), fill=couleur, width=ep)


def monogramme(d, cx, cy, taille, couleur):
    """Deux initiales entrelacées (« CM » ou « HA ») en Playfair, la 2e légèrement décalée sous la 1re."""
    fo = TITRE(taille)
    wc, wm = d.textlength(MONO[0], font=fo), d.textlength(MONO[1], font=fo)
    chev = taille * 0.05
    x = cx - (wc + wm - chev) / 2
    hauteur = fo.getbbox("M")[3] - fo.getbbox("M")[1]
    yb = cy - hauteur / 2 - fo.getbbox("M")[1]
    d.text((x + wc - chev, yb), MONO[1], font=fo, fill=couleur)
    d.text((x, yb), MONO[0], font=fo, fill=couleur)


def losange(d, cx, cy, r, couleur):
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=couleur)


def logo():
    n = 2000
    im = papier(n, n, MARQUE, force=5, vignette=0.25)
    d = ImageDraw.Draw(im)
    d.ellipse([90, 90, n - 90, n - 90], outline=OR_C, width=6)
    d.ellipse([130, 130, n - 130, n - 130], outline=OR_C, width=2)
    arche(d, 600, 380, n - 600, 1440, CREME, 5)
    brin_trait(d, n / 2 - 30, 790, 300, -40, OR_C, 5, n=5, taille=0.9)
    brin_trait(d, n / 2 + 30, 790, 270, 40, OR_C, 5, n=5, taille=0.9)
    monogramme(d, n / 2, 1080, 380, CREME)
    losange(d, n / 2, 1500, 16, OR_C)
    texte_espace(d, n / 2, 1560, NOM, GRAS(92), CREME, 26)
    return im.resize((500, 500), Image.LANCZOS)


def banniere():
    w, h = 3360 * 2, 840 * 2
    im = papier(w, h, CREME, force=4, vignette=0.12)
    d = ImageDraw.Draw(im)
    cx = w / 2
    # cadre fin
    d.rectangle([60, 60, w - 60, h - 60], outline=OR_C, width=4)
    # botanique au trait de part et d'autre
    for x, c, s in ((700, 140, 1), (1050, -120, 1), (w - 700, -140, -1), (w - 1050, 120, -1)):
        brin_trait(d, x, h - 160, 1050 if abs(x - cx) > 2700 else 820, c, MARQUE if abs(c) == 140 else SAUGE, 6)
    # titre
    texte_espace(d, cx, 300, NOM, TITRE(250), MARQUE, 30)
    yl = 640
    d.line((cx - 520, yl, cx - 40, yl), fill=OR, width=4); d.line((cx + 40, yl, cx + 520, yl), fill=OR, width=4)
    losange(d, cx, yl, 16, OR)
    t = "Poser ce qui tourne dans la tête, et mieux le partager"
    d.text((cx - d.textlength(t, font=MAIN(150)) / 2, 720), t, font=MAIN(150), fill=BRUN)
    texte_espace(d, cx, 1000, "SEUL(E)  ·  À DEUX  ·  EN FAMILLE", GRAS(70), (150, 120, 100), 18)
    return im.resize((3360, 840), Image.LANCZOS)


if __name__ == "__main__":
    os.makedirs(SORTIE, exist_ok=True)
    logo().save(os.path.join(SORTIE, f"logo{SUFFIXE}-500.png"))
    banniere().save(os.path.join(SORTIE, f"banniere{SUFFIXE}-3360x840.jpg"), quality=93)
    print(SORTIE)
