"""Épingles Pinterest vers la fiche Etsy du planner (05/11/2026, demande « Fais-moi des épingles Pinterest vers la fiche »).
1000 × 1500, texte en haut, vraies pages du planner en dessous (zones séparées, vérifiées), aucune IA, rien de payant.
Usage : python3 outils/etsy/epingles_etsy.py → etsy/epingles-etsy/*.jpg"""
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = pathlib.Path(__file__).resolve().parents[2]
P = R / "etsy" / "planner-charge-mentale"; S = R / "etsy" / "epingles-etsy"; POL = R / "polices"
PF = lambda s: ImageFont.truetype(str(POL / "PlayfairDisplay-Bold.ttf"), s)
LO = lambda s: ImageFont.truetype(str(POL / "Lora-SemiBold.ttf"), s)
DS = lambda s: ImageFont.truetype(str(POL / "DancingScript-Bold.ttf"), s)
CREME, BRUN, TERRA, OR = (246, 239, 228), (74, 52, 38), (150, 72, 58), (190, 145, 80)
W, H = 1000, 1500

EPINGLES = [
    ("couple", "LE VOLET À DEUX", ["Charge mentale en couple :", "qui fait quoi", "à la maison ?"],
     "penser, organiser, faire : chacun sa couleur", ["apercu-28.jpg", "apercu-31.jpg"]),
    ("invisibles", "PLANNER À IMPRIMER", ["Tâches invisibles :", "la liste de la", "charge mentale"],
     "les voir, c'est déjà pouvoir les partager", ["apercu-27.jpg", "apercu-04.jpg"]),
    ("frigo", "BONUS À AFFICHER", ["Kit frigo famille :", "qui fait quoi", "cette semaine ?"],
     "un prénom et une couleur par personne", ["apercu-kit-1.jpg", "apercu-kit-3.jpg"]),
]

def page(nom, larg, angle):
    im = Image.open(P / nom).convert("RGB"); im = im.resize((larg, int(larg * im.height / im.width)), Image.LANCZOS)
    im = im.rotate(angle, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0, 0)) if False else im
    rgba = im.convert("RGBA").rotate(angle, expand=True, resample=Image.BICUBIC)
    ombre = Image.new("RGBA", (rgba.width + 60, rgba.height + 60), (0, 0, 0, 0))
    a = rgba.split()[3].point(lambda v: int(v * 0.35))
    o = Image.new("RGBA", rgba.size, (60, 40, 30, 255)); o.putalpha(a)
    ombre.paste(o, (38, 42), o); ombre = ombre.filter(ImageFilter.GaussianBlur(14))
    ombre.paste(rgba, (30, 30), rgba); return ombre

def epingle(slug, etiquette, titre, sous, pages):
    im = Image.new("RGB", (W, H), CREME); d = ImageDraw.Draw(im)
    def centre(y, t, f, c):
        w = d.textlength(t, font=f); d.text(((W - w) / 2, y), t, font=f, fill=c); return d.textbbox(((W - w) / 2, y), t, font=f)
    zones = [centre(70, etiquette, LO(30), TERRA)]
    y = 125
    for ligne in titre:
        taille = 74
        while d.textlength(ligne, font=PF(taille)) > W - 110: taille -= 2
        zones.append(centre(y, ligne, PF(taille), BRUN)); y += 92
    zones.append(centre(y + 10, sous, DS(46), TERRA)); bas_texte = max(z[3] for z in zones)
    d.line((W / 2 - 160, bas_texte + 30, W / 2 + 160, bas_texte + 30), fill=OR, width=3)
    haut_img = bas_texte + 60
    a = page(pages[1], 520, -5); b = page(pages[0], 560, 4)
    pied = 1385
    place = pied - 30 - haut_img
    for p in (a, b):
        if p.height > place:
            f = place / p.height; p.thumbnail((int(p.width * f), int(p.height * f)))
    a = a if a.height <= place else a; 
    ax, bx = W - a.width - 10, 10
    im.paste(a, (ax, haut_img + 20), a); im.paste(b, (bx, haut_img), b)
    zone_img = (min(ax, bx), haut_img, max(ax + a.width, bx + b.width), max(haut_img + 20 + a.height, haut_img + b.height))
    zp = centre(pied + 20, "Clarté Mentale  ·  PDF A4 et version tablette", LO(30), BRUN)
    assert zone_img[1] > bas_texte + 30 and zone_img[3] < zp[1] - 5, (slug, zone_img, bas_texte, zp)
    im.save(S / f"epingle-etsy-{slug}.jpg", quality=92)
    return zone_img, bas_texte, zp

if __name__ == "__main__":
    for e in EPINGLES: print(e[0], epingle(*e))
