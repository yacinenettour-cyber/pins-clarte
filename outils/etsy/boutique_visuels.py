"""Logo et bannière de la boutique Etsy (02/11/2026, demande de l'utilisateur : « J'ai pas encore de boutique Etsy,
il me faut un nom, etc. »). Dessinés par programme (polices OFL de polices/), couleur de marque terracotta brique,
aucune image générée par IA, rien de payant.
Usage : python3 outils/etsy/boutique_visuels.py → etsy/boutique/logo-500.png, banniere-3360x840.jpg
"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
POL = os.path.join(ICI, "..", "..", "polices") + "/"
SORTIE = os.path.join(ICI, "..", "..", "etsy", "boutique")
MARQUE = (150, 72, 54); CREME = (248, 241, 230); BRUN = (74, 52, 36); ROSE = (196, 120, 116); SAUGE = (124, 146, 118)
f = lambda n, t: ImageFont.truetype(POL + n, t)
TITRE = lambda t: f("PlayfairDisplay-Bold.ttf", t)
MAIN = lambda t: f("DancingScript-Bold.ttf", t)
TEXTE = lambda t: f("Lora-Regular.ttf", t)


def grain(w, h, base, force=5):
    np.random.seed(3)
    a = np.ones((h, w, 3), np.float32) * np.array(base, np.float32) + np.random.normal(0, force, (h, w, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))


def brin(d, x, y, taille, angle, couleur):
    a = math.radians(angle); ux, uy = math.cos(a), math.sin(a)
    d.line([(x, y), (x + ux * taille, y + uy * taille)], fill=couleur, width=max(3, taille // 60))
    for i in range(1, 6):
        t = i / 6; px, py = x + ux * taille * t, y + uy * taille * t; r = taille * (0.13 - 0.05 * t)
        for cote in (-1, 1):
            nx, ny = -uy * cote, ux * cote
            cx, cy = px + nx * r * 0.8 + ux * r * 0.4, py + ny * r * 0.8 + uy * r * 0.4
            d.ellipse([cx - r * 0.85, cy - r * 0.5, cx + r * 0.85, cy + r * 0.5], fill=couleur)


def centre(d, y, t, fo, fill, w):
    d.text(((w - d.textlength(t, font=fo)) / 2, y), t, font=fo, fill=fill)


def logo():
    n = 1000
    im = grain(n, n, MARQUE)
    d = ImageDraw.Draw(im)
    d.ellipse([70, 70, n - 70, n - 70], outline=(232, 196, 170), width=6)
    brin(d, n / 2 - 40, 330, 190, -110, (236, 214, 196))
    brin(d, n / 2 + 40, 330, 170, -70, (236, 214, 196))
    centre(d, 390, "Clarté", TITRE(170), CREME, n)
    centre(d, 590, "Mentale", MAIN(140), (240, 200, 180), n)
    return im.resize((500, 500), Image.LANCZOS)


def banniere():
    w, h = 3360, 840
    im = grain(w, h, CREME, 4)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 1060, h], fill=MARQUE)
    centre_g = lambda y, t, fo, c: d.text(((1060 - d.textlength(t, font=fo)) / 2, y), t, font=fo, fill=c)
    centre_g(250, "Clarté", TITRE(170), CREME)
    centre_g(450, "Mentale", MAIN(140), (240, 200, 180))
    x = 1240
    d.text((x, 230), "Planners à imprimer pour", font=TEXTE(84), fill=BRUN)
    d.text((x, 345), "alléger la charge mentale", font=TITRE(120), fill=MARQUE)
    d.text((x, 530), "seul(e), à deux et en famille  ·  en français", font=MAIN(78), fill=ROSE)
    brin(d, 3150, 760, 320, -105, SAUGE)
    brin(d, 3240, 790, 260, -80, (150, 170, 140))
    return im


if __name__ == "__main__":
    os.makedirs(SORTIE, exist_ok=True)
    logo().save(os.path.join(SORTIE, "logo-500.png"))
    banniere().save(os.path.join(SORTIE, "banniere-3360x840.jpg"), quality=92)
    print(SORTIE)
