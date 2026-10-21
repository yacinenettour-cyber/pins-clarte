"""Photo de profil de la chaîne YouTube @ClarteMentaleFR (800×800, affichée en rond jusqu'à 98 px).
Silhouette en méditation devant une pleine lune texturée, ciel de nuit à nébuleuse, anneau doré.
Tout est dessiné (aucune photo), en 3× puis réduit pour des bords nets. Usage : python3 youtube/avatar.py"""
import math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import DEPOT

T, K = 800, 3            # taille finale, facteur de suréchantillonnage
S = T * K
SORTIE = os.path.join(DEPOT, "videos_youtube", "photo-profil-chaine.png")


def bruit(n, octaves=5, graine=1):
    """Bruit fractal (somme de bruits lissés) normalisé 0-1."""
    rnd = np.random.default_rng(graine)
    out = np.zeros((n, n))
    for o in range(octaves):
        c = 4 * 2 ** o
        g = rnd.random((c, c))
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((n, n), Image.BICUBIC)
        out += np.asarray(im, float) / 255 / 2 ** o
    out -= out.min()
    return out / out.max()


def ciel():
    y, x = np.mgrid[0:S, 0:S] / S
    d = np.sqrt((x - 0.5) ** 2 + (y - 0.42) ** 2)
    fond = np.array([6, 8, 26]) + (np.array([26, 30, 84]) - np.array([6, 8, 26])) * np.clip(1 - d * 1.4, 0, 1)[..., None] ** 1.4
    n = bruit(S, 5, 4)[..., None]
    neb = np.array([80, 45, 120]) * (n ** 3) * 0.25 + np.array([25, 85, 135]) * (bruit(S, 4, 9)[..., None] ** 4) * 0.30
    return np.clip(fond + neb * np.clip(1.1 - d * 1.2, 0, 1)[..., None], 0, 255)


def lune(img, cx, cy, r):
    """Pleine lune : disque crème, mers sombres (bruit), cratères, assombrissement au bord ; halos superposés."""
    y, x = np.mgrid[0:S, 0:S]
    d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    for rayon, force in [(r * 2.4, 0.07), (r * 1.5, 0.14), (r * 1.12, 0.40)]:
        img += np.array([255, 225, 170]) * (np.exp(-(d / rayon) ** 2) * force)[..., None]
    dedans = d < r
    mers = bruit(S, 4, 21)
    rnd = random.Random(5)
    crat = np.zeros((S, S))
    for _ in range(28):
        a, rr = rnd.uniform(0, 2 * math.pi), r * math.sqrt(rnd.random()) * 0.92
        px, py, cr = cx + rr * math.cos(a), cy + rr * math.sin(a), rnd.uniform(r * 0.02, r * 0.09)
        dd = np.sqrt((x - px) ** 2 + (y - py) ** 2)
        crat += np.clip(1 - dd / cr, 0, 1) * 0.5 - np.clip(1 - np.abs(dd - cr) / (cr * 0.25), 0, 1) * 0.15
    limbe = np.sqrt(np.clip(1 - (d / r) ** 2, 0, 1)) ** 0.35
    teinte = np.array([255, 246, 222])[None, None, :] * (1.0 - 0.22 * np.clip((mers[..., None] - 0.5) * 2.2, 0, 1)
                                                           - 0.10 * crat[..., None]) * (0.55 + 0.45 * limbe[..., None])
    bord = np.clip(r - d, 0, 1.5) / 1.5          # anticrénelage du disque
    img[:] = img * (1 - bord[..., None]) + np.clip(teinte, 0, 255) * bord[..., None]
    return img


def forme_meditation(dm, bx, by, u):
    """Formes de la personne en méditation (bassin en bx, by ; u = échelle) ; partagé avec la bannière."""
    E = lambda x, y, rx, ry: dm.ellipse([bx + (x - rx) * u, by + (y - ry) * u, bx + (x + rx) * u, by + (y + ry) * u], fill=255)
    E(0, -262, 33, 39)                      # tête
    E(0, -306, 17, 15)                      # chignon
    dm.rectangle([bx - 13 * u, by - 230 * u, bx + 13 * u, by - 200 * u], fill=255)   # cou
    dm.polygon([(bx + x * u, by + y * u) for x, y in
                [(-66, -196), (-30, -212), (30, -212), (66, -196), (54, -130), (44, -80), (70, -20),
                 (-70, -20), (-44, -80), (-54, -130)]], fill=255)                      # buste, taille marquée
    for sg in (-1, 1):
        dm.line([(bx + sg * 62 * u, by - 192 * u), (bx + sg * 92 * u, by - 110 * u)], fill=255, width=int(30 * u))
        dm.line([(bx + sg * 92 * u, by - 110 * u), (bx + sg * 128 * u, by - 26 * u)], fill=255, width=int(25 * u))
        E(sg * 92, -110, 15, 15)            # coude
        E(sg * 130, -22, 19, 15)            # main posée sur le genou
        E(sg * 128, 0, 42, 30)              # genou
    E(0, 4, 150, 34)                        # jambes croisées


def silhouette(im):
    """Personne assise en tailleur, mains sur les genoux, sur une colline. Formes simples fondues entre elles
    (flou puis seuil) pour un contour souple, sans angles de robot."""
    u = S / 800
    d = ImageDraw.Draw(im)
    pts = [(x, S * 0.81 + 18 * u * math.sin(x / (110 * u)) - 34 * u * math.exp(-((x - S / 2) / (240 * u)) ** 2))
           for x in range(0, S + 10, 6)]
    d.polygon(pts + [(S, S), (0, S)], fill=(13, 14, 34, 255))
    m = Image.new("L", im.size, 0)
    forme_meditation(ImageDraw.Draw(m), S / 2, S * 0.765, u)
    m = m.filter(ImageFilter.GaussianBlur(7 * u)).point(lambda v: 255 if v > 118 else 0)
    m = m.filter(ImageFilter.GaussianBlur(0.8 * u))
    calque = Image.new("RGBA", im.size, (8, 9, 22, 255))
    calque.putalpha(m)
    # liseré de lumière lunaire sur le contour
    contour = m.filter(ImageFilter.MaxFilter(5)).point(lambda v: v)
    liser = Image.new("RGBA", im.size, (255, 230, 180, 0))
    liser.putalpha(Image.fromarray(np.clip(np.asarray(contour, float) - np.asarray(m, float), 0, 255).astype(np.uint8) // 2))
    im.alpha_composite(liser.filter(ImageFilter.GaussianBlur(2 * u)))
    im.alpha_composite(calque)
    return im


def etoiles(im):
    d = ImageDraw.Draw(im)
    rnd = random.Random(11)
    u = S / 800
    for _ in range(170):
        x, y = rnd.uniform(0, S), rnd.uniform(0, S * 0.72)
        r = rnd.choice([0.8, 1, 1.2, 1.6]) * u
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 250, 235, rnd.randint(110, 230)))
    for (x, y, l) in [(170, 205, 26), (640, 160, 20), (655, 470, 14), (150, 470, 12)]:   # étoiles scintillantes
        x, y, l = x * u, y * u, l * u
        calque = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dc = ImageDraw.Draw(calque)
        dc.polygon([(x, y - l), (x + l * 0.16, y), (x, y + l), (x - l * 0.16, y)], fill=(255, 246, 222, 255))
        dc.polygon([(x - l, y), (x, y + l * 0.16), (x + l, y), (x, y - l * 0.16)], fill=(255, 246, 222, 255))
        im.alpha_composite(calque.filter(ImageFilter.GaussianBlur(2 * u)))
        im.alpha_composite(calque)
    return im


def anneau(im):
    """Fin anneau doré dans le cercle affiché par YouTube."""
    calque = Image.new("RGBA", im.size, (0, 0, 0, 0))
    m = 22 * K
    ImageDraw.Draw(calque).ellipse([m, m, S - m, S - m], outline=(232, 192, 120, 210), width=5 * K)
    im.alpha_composite(calque.filter(ImageFilter.GaussianBlur(K)))
    return im


def fabriquer():
    img = ciel()
    img = lune(img, S * 0.5, S * 0.43, S * 0.255)
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
    im = etoiles(im)
    im = silhouette(im)
    im = anneau(im)
    im = im.convert("RGB").resize((T, T), Image.LANCZOS)
    im.save(SORTIE, optimize=True)
    return SORTIE


if __name__ == "__main__":
    print(fabriquer(), round(os.path.getsize(SORTIE) / 1e6, 2), "Mo")
