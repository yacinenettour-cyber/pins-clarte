"""Photo de profil de la chaîne YouTube @ClarteMentaleFR (800×800, affichée en rond jusqu'à 98 px).
Même univers que la bannière (banniere.py) : nuit, croissant de lune, étoiles ; rien de petit qui deviendrait illisible.
Usage : python3 youtube/avatar.py"""
import os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import POLICES, DEPOT

T = 800
SORTIE = os.path.join(DEPOT, "videos_youtube", "photo-profil-chaine.png")


def fabriquer():
    y, x = np.mgrid[0:T, 0:T] / T
    haut, bas = np.array([12, 16, 42]), np.array([40, 44, 88])
    img = haut + (bas - haut) * (y ** 1.2)[..., None]
    d = np.sqrt((x - 0.5) ** 2 + (y - 0.44) ** 2)
    img = img + np.array([95, 85, 62]) * np.exp(-(d / 0.30) ** 2)[..., None] * 0.5
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")

    # quelques étoiles, nettes et assez grosses pour rester visibles en petit
    calque = Image.new("RGBA", im.size, (0, 0, 0, 0))
    dc = ImageDraw.Draw(calque)
    for (sx, sy, r) in [(190, 210, 7), (600, 175, 5), (640, 330, 6), (225, 430, 4), (560, 520, 4), (300, 150, 3)]:
        dc.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 248, 225, 235))
    im.alpha_composite(calque.filter(ImageFilter.GaussianBlur(1)))

    # croissant de lune au centre, avec lueur
    cx, cy, r = 400, 350, 190
    lune = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(lune).ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 240, 200, 255))
    masque = Image.new("L", im.size, 0)
    ImageDraw.Draw(masque).ellipse([cx - r + 105, cy - r - 55, cx + r + 105, cy + r - 55], fill=255)
    lune.putalpha(Image.fromarray(np.minimum(np.array(lune.split()[3]), 255 - np.array(masque))))
    im.alpha_composite(lune.filter(ImageFilter.GaussianBlur(34)))
    im.alpha_composite(lune)

    # nom court, gros, sous la lune (lisible dès 98 px)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(os.path.join(POLICES, "PlayfairDisplay-Bold.ttf"), 112)
    texte = "Clarté"
    tw = d.textlength(texte, font=f)
    d.text(((T - tw) / 2, 560), texte, font=f, fill=(255, 247, 228))
    im.convert("RGB").save(SORTIE, optimize=True)
    return SORTIE


if __name__ == "__main__":
    print(fabriquer(), round(os.path.getsize(SORTIE) / 1e6, 2), "Mo")
