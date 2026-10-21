"""Bannière de la chaîne YouTube @ClarteMentaleFR (2560×1440, texte dans la zone visible partout : 1546×423 au centre).
Même univers que la photo de profil (avatar.py) : ciel à nébuleuse, pleine lune texturée, personne en méditation
sur une colline. Tout est dessiné (aucune photo), polices OFL du dépôt. Usage : python3 youtube/banniere.py"""
import math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import POLICES, DEPOT
from avatar import forme_meditation

W, H = 2560, 1440
ZX, ZY, ZW, ZH = (W - 1546) // 2, (H - 423) // 2, 1546, 423   # zone visible sur mobile, ordinateur et TV
LUNE = (ZX + ZW - 270, ZY + 205, 178)                          # centre et rayon, entièrement dans la zone visible
SORTIE = os.path.join(DEPOT, "videos_youtube", "banniere-chaine.jpg")


def police(nom, taille):
    return ImageFont.truetype(os.path.join(POLICES, nom), taille)


def bruit(h, w, octaves=5, graine=1):
    """Bruit fractal normalisé 0-1 (même principe que avatar.bruit, en rectangle)."""
    rnd = np.random.default_rng(graine)
    out = np.zeros((h, w))
    for o in range(octaves):
        c = 4 * 2 ** o
        g = rnd.random((c, int(c * w / h) + 1))
        out += np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), float) / 255 / 2 ** o
    out -= out.min()
    return out / out.max()


def ciel():
    y, x = np.mgrid[0:H, 0:W]
    cx, cy, r = LUNE
    d = np.sqrt(((x - cx) / H) ** 2 + ((y - cy) / H) ** 2)
    v = y / H
    fond = np.array([6, 8, 26]) + (np.array([22, 26, 70]) - np.array([6, 8, 26])) * (v ** 1.2)[..., None]
    fond = fond + np.array([20, 18, 40]) * np.clip(1 - d * 1.3, 0, 1)[..., None] ** 2
    neb = (np.array([80, 45, 120]) * (bruit(H, W, 5, 4)[..., None] ** 3) * 0.28
           + np.array([25, 85, 135]) * (bruit(H, W, 4, 9)[..., None] ** 4) * 0.32)
    img = fond + neb
    for rayon, force in [(r * 2.6, 0.08), (r * 1.6, 0.15), (r * 1.12, 0.40)]:      # halos de la lune
        dd = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        img += np.array([255, 225, 170]) * (np.exp(-(dd / rayon) ** 2) * force)[..., None]
    return img


def lune(img):
    """Pleine lune texturée (mers, cratères, limbe), calculée seulement autour du disque."""
    cx, cy, r = LUNE
    x0, y0, x1, y1 = int(cx - r - 3), int(cy - r - 3), int(cx + r + 4), int(cy + r + 4)
    y, x = np.mgrid[y0:y1, x0:x1]
    d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    mers = bruit(y1 - y0, x1 - x0, 4, 21)
    rnd = random.Random(5)
    crat = np.zeros(d.shape)
    for _ in range(28):
        a, rr = rnd.uniform(0, 2 * math.pi), r * math.sqrt(rnd.random()) * 0.92
        px, py, cr = cx + rr * math.cos(a), cy + rr * math.sin(a), rnd.uniform(r * 0.02, r * 0.09)
        dd = np.sqrt((x - px) ** 2 + (y - py) ** 2)
        crat += np.clip(1 - dd / cr, 0, 1) * 0.5 - np.clip(1 - np.abs(dd - cr) / (cr * 0.25), 0, 1) * 0.15
    limbe = np.sqrt(np.clip(1 - (d / r) ** 2, 0, 1)) ** 0.35
    teinte = np.array([255, 246, 222]) * (1.0 - 0.16 * np.clip((mers[..., None] - 0.5) * 2.2, 0, 1)
                                          - 0.10 * crat[..., None]) * (0.55 + 0.45 * limbe[..., None])
    bord = (np.clip(r - d, 0, 1.5) / 1.5)[..., None]
    img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - bord) + np.clip(teinte, 0, 255) * bord
    return img


def etoiles(im):
    d = ImageDraw.Draw(im)
    rnd = random.Random(7)
    for _ in range(1100):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H * 0.78)
        if ZX - 30 < x < ZX + 1000 and ZY - 20 < y < ZY + ZH + 20 and rnd.random() < 0.75:
            continue                                   # moins d'étoiles derrière le texte
        r = rnd.choice([0.8, 1, 1, 1.3, 1.7, 2.2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 250, 235, rnd.randint(90, 230)))
    for (x, y, l) in [(ZX + ZW - 520, ZY + 40, 26), (ZX + ZW - 40, ZY + 60, 20), (ZX + ZW - 60, ZY + 330, 14),
                      (ZX + 1060, ZY + 300, 12), (330, 300, 22), (2260, 380, 24), (520, 1010, 14)]:
        calque = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dc = ImageDraw.Draw(calque)
        dc.polygon([(x, y - l), (x + l * 0.16, y), (x, y + l), (x - l * 0.16, y)], fill=(255, 246, 222, 255))
        dc.polygon([(x - l, y), (x, y + l * 0.16), (x + l, y), (x, y - l * 0.16)], fill=(255, 246, 222, 255))
        im.alpha_composite(calque.filter(ImageFilter.GaussianBlur(2)))
        im.alpha_composite(calque)
    return im


def paysage(im):
    """Collines en couches avec brume, puis la personne en méditation au sommet, devant la lune."""
    cx, cy, r = LUNE
    sommet = ZY + ZH - 42                           # le bas de la silhouette reste dans la zone visible
    rnd = random.Random(3)
    for i, (base, coul, amp) in enumerate([(0.74, (20, 22, 52), 34), (0.80, (15, 16, 40), 46), (0.88, (10, 11, 28), 40)]):
        c = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ph = rnd.uniform(0, 6)
        pts = []
        for x in range(0, W + 20, 16):
            yv = H * base + amp * math.sin(x / (360 + 90 * i) + ph) + 14 * math.sin(x / 93 + ph * 2)
            if i == 1:                              # colline principale qui monte jusqu'à la personne
                yv = min(yv, sommet + 6 + ((x - cx) / 520) ** 2 * 260)
            pts.append((x, yv))
        ImageDraw.Draw(c).polygon(pts + [(W, H), (0, H)], fill=coul + (255,))
        im.alpha_composite(c)
        brume = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(brume).rectangle([0, H * base - 20, W, H * base + 60], fill=(170, 180, 230, 20))
        im.alpha_composite(brume.filter(ImageFilter.GaussianBlur(45)))
    # personne : dessinée en 3× dans sa boîte puis réduite, contour souple + liseré lunaire
    K, u = 3, 0.7
    bw, bh = int(420 * u), int(420 * u)
    m = Image.new("L", (bw * K, bh * K), 0)
    forme_meditation(ImageDraw.Draw(m), bw * K / 2, (bh - 40 * u) * K, u * K)
    m = m.filter(ImageFilter.GaussianBlur(7 * u * K)).point(lambda v: 255 if v > 118 else 0)
    m = m.filter(ImageFilter.GaussianBlur(0.8 * K)).resize((bw, bh), Image.LANCZOS)
    pos = (int(cx - bw / 2), int(sommet - (bh - 40 * u)))
    contour = m.filter(ImageFilter.MaxFilter(3))
    liser = Image.new("RGBA", (bw, bh), (255, 230, 180, 0))
    liser.putalpha(Image.fromarray(np.clip(np.asarray(contour, float) - np.asarray(m, float), 0, 255).astype(np.uint8) // 2))
    calque = Image.new("RGBA", (bw, bh), (8, 9, 22, 255))
    calque.putalpha(m)
    im.alpha_composite(liser.filter(ImageFilter.GaussianBlur(1.2)), pos)
    im.alpha_composite(calque, pos)
    return im


def textes(im):
    gauche = ZX + 30
    voile = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(voile).rounded_rectangle([ZX - 60, ZY - 20, ZX + 990, ZY + ZH + 20], 80, fill=(6, 8, 24, 120))
    im.alpha_composite(voile.filter(ImageFilter.GaussianBlur(60)))
    d = ImageDraw.Draw(im)
    titre, ft = "Clarté Mentale", police("PlayfairDisplay-Bold.ttf", 136)
    ombre = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(ombre).text((gauche + 4, ZY + 22), titre, font=ft, fill=(0, 0, 0, 160))
    im.alpha_composite(ombre.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(im)
    d.text((gauche, ZY + 16), titre, font=ft, fill=(255, 247, 228))
    tw = d.textlength(titre, font=ft)
    d.line([(gauche + 6, ZY + 192), (gauche + 6 + tw * 0.32, ZY + 192)], fill=(232, 192, 120), width=4)   # filet doré
    fs = police("Lora-SemiBold.ttf", 56)
    d.text((gauche + 6, ZY + 214), "Méditations guidées pour dormir", font=fs, fill=(240, 200, 130))
    d.text((gauche + 6, ZY + 280), "et calmer les pensées du soir", font=fs, fill=(240, 200, 130))
    pastille = "Voix douce  ·  musique calme  ·  une nouvelle méditation chaque semaine"
    f = police("Lora-Regular.ttf", 30)
    pw = d.textlength(pastille, font=f)
    x0, y0 = gauche, ZY + 360
    calque = Image.new("RGBA", im.size, (0, 0, 0, 0))   # transparence réelle (ImageDraw seul ne mélange pas)
    ImageDraw.Draw(calque).rounded_rectangle([x0, y0, x0 + pw + 52, y0 + 54], 27, fill=(255, 255, 255, 30),
                                             outline=(232, 192, 120, 150), width=2)
    im.alpha_composite(calque)
    ImageDraw.Draw(im).text((x0 + 26, y0 + 9), pastille, font=f, fill=(235, 238, 250))
    return im


def fabriquer():
    img = lune(ciel())
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
    im = etoiles(im)
    im = paysage(im)
    im = textes(im)
    im.convert("RGB").save(SORTIE, quality=93, optimize=True)
    return SORTIE


if __name__ == "__main__":
    print(fabriquer(), round(os.path.getsize(SORTIE) / 1e6, 2), "Mo")
