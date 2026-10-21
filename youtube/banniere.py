"""Bannière de la chaîne YouTube @ClarteMentaleFR (2560×1440, texte dans la zone visible partout : 1546×423 au centre).
Ciel de nuit dessiné (aucune photo réutilisée), polices OFL du dépôt. Usage : python3 youtube/banniere.py"""
import math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import POLICES, DEPOT

W, H = 2560, 1440
ZX, ZY, ZW, ZH = (W - 1546) // 2, (H - 423) // 2, 1546, 423   # zone visible sur mobile, ordinateur et TV
LUNE = (ZX + ZW - 230, ZY + ZH // 2 - 10)   # entièrement dans la zone visible, à droite du texte
SORTIE = os.path.join(DEPOT, "videos_youtube", "banniere-chaine.jpg")


def police(nom, taille):
    return ImageFont.truetype(os.path.join(POLICES, nom), taille)


def ciel():
    y = np.linspace(0, 1, H)[:, None]
    x = np.linspace(0, 1, W)[None, :]
    haut, bas = np.array([10, 14, 38]), np.array([38, 42, 82])
    img = np.broadcast_to(haut + (bas - haut) * (y ** 1.3)[..., None], (H, W, 3)).astype(float)
    # halo de lune à droite de la zone de texte
    lx, ly = LUNE[0] / W, LUNE[1] / H
    d = np.sqrt(((x - lx) * W / H) ** 2 + (y - ly) ** 2)
    img += np.array([90, 80, 60]) * np.exp(-(d / 0.20) ** 2)[..., None] * 0.55
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def etoiles(im):
    rnd = random.Random(7)
    d = ImageDraw.Draw(im)
    for _ in range(900):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H * 0.78)
        r = rnd.choice([0.8, 1, 1, 1.4, 1.8, 2.4])
        a = rnd.randint(90, 235)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 250, 235, a))
    return im


def lune(im):
    (cx, cy), r = LUNE, 115
    calque = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(calque)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 242, 205, 255))
    # croissant : on retire un disque décalé
    masque = Image.new("L", im.size, 0)
    ImageDraw.Draw(masque).ellipse([cx - r + 62, cy - r - 30, cx + r + 62, cy + r - 30], fill=255)
    calque.putalpha(Image.fromarray(np.minimum(np.array(calque.split()[3]), 255 - np.array(masque))))
    lueur = calque.filter(ImageFilter.GaussianBlur(28))
    im.alpha_composite(lueur)
    im.alpha_composite(calque)
    return im


def collines(im):
    """Lignes de collines et brume en bas : profondeur, sans détail qui gêne le texte."""
    rnd = random.Random(3)
    for i, (base, coul, amp) in enumerate([(0.80, (24, 28, 58, 255), 40), (0.86, (17, 20, 44, 255), 55),
                                           (0.92, (10, 12, 30, 255), 45)]):
        c = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ph = rnd.uniform(0, 6)
        pts = [(x, H * base + amp * math.sin(x / (380 + 90 * i) + ph) + 18 * math.sin(x / 97 + ph * 2))
               for x in range(0, W + 20, 20)]
        ImageDraw.Draw(c).polygon(pts + [(W, H), (0, H)], fill=coul)
        im.alpha_composite(c)
        brume = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(brume).rectangle([0, H * base - 30, W, H * base + 50], fill=(180, 190, 230, 22))
        im.alpha_composite(brume.filter(ImageFilter.GaussianBlur(40)))
    return im


def textes(im):
    d = ImageDraw.Draw(im)
    gauche = ZX + 40
    # voile doux derrière le texte pour la lisibilité
    voile = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(voile).rounded_rectangle([ZX - 40, ZY - 10, ZX + 1000, ZY + ZH + 10], 60, fill=(8, 10, 28, 110))
    im.alpha_composite(voile.filter(ImageFilter.GaussianBlur(50)))
    d = ImageDraw.Draw(im)
    d.text((gauche, ZY + 20), "Clarté Mentale", font=police("PlayfairDisplay-Bold.ttf", 132), fill=(255, 247, 228))
    d.text((gauche + 6, ZY + 185), "Méditations guidées pour dormir", font=police("Lora-SemiBold.ttf", 58), fill=(240, 200, 130))
    d.text((gauche + 6, ZY + 255), "et calmer les pensées du soir", font=police("Lora-SemiBold.ttf", 58), fill=(240, 200, 130))
    pastille = "Voix douce · musique calme · nouvelle méditation chaque semaine"
    f = police("Lora-Regular.ttf", 34)
    tw = d.textlength(pastille, font=f)
    x0, y0 = gauche, ZY + 345
    calque = Image.new("RGBA", im.size, (0, 0, 0, 0))   # transparence réelle (ImageDraw seul ne mélange pas)
    ImageDraw.Draw(calque).rounded_rectangle([x0, y0, x0 + tw + 56, y0 + 62], 31, fill=(255, 255, 255, 34),
                                             outline=(255, 255, 255, 110), width=2)
    im.alpha_composite(calque)
    d = ImageDraw.Draw(im)
    d.text((x0 + 28, y0 + 11), pastille, font=f, fill=(235, 238, 250))
    return im


def fabriquer():
    im = ciel().convert("RGBA")
    im = etoiles(im)
    im = lune(im)
    im = collines(im)
    im = textes(im)
    im.convert("RGB").save(SORTIE, quality=92, optimize=True)
    return SORTIE


if __name__ == "__main__":
    print(fabriquer(), round(os.path.getsize(SORTIE) / 1e6, 2), "Mo")
