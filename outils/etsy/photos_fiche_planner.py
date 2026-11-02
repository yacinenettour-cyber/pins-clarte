"""Photos de la fiche Etsy du planner « Alléger sa charge mentale » (02/11/2026, demande de l'utilisateur :
« des images de présentation hautement qualitatives qui se démarquent de la concurrence »).

Tout est dessiné par programme (PIL) à partir des vraies pages du PDF : aucune image générée par IA, aucune photo
payante. Format 3000 × 2250 (4:3, conseillé par Etsy), sujet centré pour rester lisible en vignette carrée.
Usage : python3 outils/etsy/photos_fiche_planner.py   → etsy/planner-charge-mentale/fiche-XX-*.jpg
"""
import glob, math, os, random, subprocess, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
DEPOT = os.path.abspath(os.path.join(ICI, "..", ".."))
POL = os.path.join(DEPOT, "polices") + "/"
DOSSIER = os.path.join(DEPOT, "etsy", "planner-charge-mentale")
PDF_C = os.path.join(DOSSIER, "planner-alleger-charge-mentale-A4.pdf")
PDF_E = os.path.join(DOSSIER, "planner-alleger-charge-mentale-A4-econome-encre.pdf")
PDF_T = os.path.join(DOSSIER, "planner-alleger-charge-mentale-tablette.pdf")
PDF_K = os.path.join(DOSSIER, "kit-frigo-famille-A4.pdf")
PERS = [(184, 92, 64), (64, 104, 138), (110, 140, 100), (176, 140, 72)]
CREME_TXT = (240, 232, 214)
W, H = 3000, 2250

CREME = (250, 245, 236); SAUGE = (124, 146, 118); SAUGE_C = (226, 233, 221); ROSE = (196, 120, 116)
ROSE_C = (244, 226, 220); BRUN = (74, 52, 36); TXT = (88, 76, 66); OR = (176, 128, 52)
LAVANDE = (140, 120, 160); BRUME = (110, 138, 160); SABLE = (190, 150, 100)

f = lambda nom, t: ImageFont.truetype(POL + nom, t)
TITRE = lambda t: f("PlayfairDisplay-Bold.ttf", t)
MAIN = lambda t: f("DancingScript-Bold.ttf", t)
TEXTE = lambda t: f("Lora-Regular.ttf", t)
GRAS = lambda t: f("Lora-SemiBold.ttf", t)

random.seed(7)
np.random.seed(7)


# ---------------------------------------------------------------- pages du PDF
_PAGES = {}


def rendre_pages():
    t = tempfile.mkdtemp()
    subprocess.run(["pdftoppm", "-r", "200", "-png", PDF_C, os.path.join(t, "c")], check=True)
    subprocess.run(["pdftoppm", "-r", "200", "-png", PDF_E, os.path.join(t, "e")], check=True)
    subprocess.run(["pdftoppm", "-r", "200", "-png", PDF_T, os.path.join(t, "t")], check=True)
    subprocess.run(["pdftoppm", "-r", "200", "-png", PDF_K, os.path.join(t, "k")], check=True)
    for p in glob.glob(os.path.join(t, "*.png")):
        b = os.path.basename(p)
        _PAGES[(b[0], int(b.split("-")[1].split(".")[0]))] = p


def page(n, largeur, version="c"):
    im = Image.open(_PAGES[(version, n)]).convert("RGB")
    h = round(largeur * im.height / im.width)
    im = im.resize((largeur, h), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, largeur - 1, h - 1], outline=(222, 212, 196), width=2)  # tranche du papier
    return im


# ---------------------------------------------------------------- décor
def fond(base=(236, 232, 222), grain=7, vignette=0.10):
    """Fond « lin » : grain fin, fibres horizontales et verticales légères, vignettage doux."""
    a = np.ones((H, W, 3), np.float32) * np.array(base, np.float32)
    a += np.random.normal(0, grain, (H, W, 1)).astype(np.float32)
    fib_h = np.random.normal(0, 1.8, (H, 1, 1)).astype(np.float32)
    fib_v = np.random.normal(0, 1.4, (1, W, 1)).astype(np.float32)
    a += fib_h + fib_v
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    a *= (1 - vignette * np.clip(r - 0.35, 0, None))[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return im.filter(ImageFilter.GaussianBlur(0.6))


def coller(fond_im, im, centre, angle=0.0, ombre=1.0, eleve=1.0):
    """Colle une image tournée, avec une ombre portée douce en deux couches (contact + diffuse)."""
    rgba = im.convert("RGBA")
    rot = rgba.rotate(angle, resample=Image.BICUBIC, expand=True)
    x, y = round(centre[0] - rot.width / 2), round(centre[1] - rot.height / 2)
    alpha = rot.split()[3]
    for flou, decal, force in ((60 * eleve, (18 * eleve, 34 * eleve), 0.30), (14, (4, 8), 0.28)):
        pad = int(flou * 3)
        o = Image.new("L", (rot.width + 2 * pad, rot.height + 2 * pad), 0)
        o.paste(alpha, (pad, pad))
        o = o.filter(ImageFilter.GaussianBlur(flou)).point(lambda v: int(v * force * ombre))
        noir = Image.new("RGBA", o.size, (60, 42, 30, 0))
        noir.putalpha(o)
        fond_im.alpha_composite(noir, (int(x - pad + decal[0]), int(y - pad + decal[1]))) if fond_im.mode == "RGBA" else \
            fond_im.paste(noir, (int(x - pad + decal[0]), int(y - pad + decal[1])), noir)
    fond_im.paste(rot, (x, y), rot)
    return (x, y, x + rot.width, y + rot.height)


def brin(d, x, y, taille, angle_deg, couleur=SAUGE, couleur2=(150, 170, 140)):
    """Brin d'eucalyptus stylisé (tige + feuilles ovales), dessiné en vectoriel."""
    a = math.radians(angle_deg)
    ux, uy = math.cos(a), math.sin(a)
    x2, y2 = x + ux * taille, y + uy * taille
    d.line([(x, y), (x2, y2)], fill=(110, 128, 100), width=max(3, taille // 120))
    n = 7
    for i in range(1, n + 1):
        t = i / (n + 1)
        px, py = x + ux * taille * t, y + uy * taille * t
        for cote in (-1, 1):
            r = taille * (0.10 - 0.04 * t)
            nx, ny = -uy * cote, ux * cote
            cx, cy = px + nx * r * 0.9 + ux * r * 0.3, py + ny * r * 0.9 + uy * r * 0.3
            feuille = Image.new("RGBA", (int(r * 2.6), int(r * 1.6)), (0, 0, 0, 0))
            ImageDraw.Draw(feuille).ellipse([0, 0, feuille.width - 1, feuille.height - 1],
                                            fill=(couleur if (i + cote) % 2 else couleur2) + (235,))
            ang = -math.degrees(math.atan2(ny, nx))
            feuille = feuille.rotate(ang, expand=True, resample=Image.BICUBIC)
            d._image.paste(feuille, (int(cx - feuille.width / 2), int(cy - feuille.height / 2)), feuille)


def crayon(im, x, y, longueur, angle):
    """Crayon de bois vu de dessus, avec ombre."""
    L, e = longueur, 38
    c = Image.new("RGBA", (L, e), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    d.rectangle([0, 0, int(L * 0.80), e - 1], fill=(222, 196, 150))           # corps
    d.rectangle([0, 0, int(L * 0.80), e // 3], fill=(234, 212, 170))          # reflet
    d.rectangle([0, 0, 70, e - 1], fill=(205, 170, 160))                      # gomme
    d.rectangle([70, 0, 120, e - 1], fill=(190, 178, 160))                    # virole
    for k in range(78, 118, 10):
        d.line([(k, 0), (k, e)], fill=(160, 150, 136), width=2)
    d.polygon([(int(L * 0.80), 0), (int(L * 0.95), e // 2 - 4), (int(L * 0.95), e // 2 + 4), (int(L * 0.80), e - 1)],
              fill=(236, 214, 178))
    d.polygon([(int(L * 0.93), e // 2 - 6), (L - 1, e // 2), (int(L * 0.93), e // 2 + 6)], fill=(70, 62, 58))
    coller(im, c, (x, y), angle, ombre=0.8, eleve=0.25)


def tasse(im, cx, cy, r):
    """Tasse de tisane vue de dessus (soucoupe, bord, liquide)."""
    s = Image.new("RGBA", (int(r * 3.2), int(r * 3.2)), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    c = s.width / 2
    d.ellipse([c - r * 1.55, c - r * 1.55, c + r * 1.55, c + r * 1.55], fill=(246, 242, 234))
    d.ellipse([c - r * 1.5, c - r * 1.5, c + r * 1.5, c + r * 1.5], outline=(226, 218, 204), width=4)
    d.ellipse([c - r, c - r, c + r, c + r], fill=(250, 248, 244))
    d.ellipse([c - r * 0.84, c - r * 0.84, c + r * 0.84, c + r * 0.84], fill=(196, 160, 104))
    d.ellipse([c - r * 0.80, c - r * 0.80, c + r * 0.80, c + r * 0.80], fill=(204, 170, 116))
    d.ellipse([c - r * 0.5, c - r * 0.62, c - r * 0.1, c - r * 0.4], fill=(222, 196, 150))  # reflet
    d.rounded_rectangle([c + r * 0.95, c - r * 0.18, c + r * 1.45, c + r * 0.18], radius=int(r * 0.17),
                        fill=(250, 248, 244), outline=(226, 218, 204), width=3)
    coller(im, s, (cx, cy), 0, ombre=0.9, eleve=0.35)


# ---------------------------------------------------------------- texte
def largeur(d, t, police):
    return d.textlength(t, font=police)


def centre(d, t, police, y, x0=0, x1=W, couleur=BRUN):
    d.text(((x0 + x1 - largeur(d, t, police)) / 2, y), t, font=police, fill=couleur)


def lignes(d, t, police, lmax):
    mots, out, cur = t.split(), [], ""
    for m in mots:
        essai = (cur + " " + m).strip()
        if largeur(d, essai, police) <= lmax:
            cur = essai
        else:
            out.append(cur); cur = m
    out.append(cur)
    return out


def bloc(d, t, police, x, y, lmax, couleur=TXT, interligne=1.35, centrer=False):
    for l in lignes(d, t, police, lmax):
        if centrer:
            d.text((x + (lmax - largeur(d, l, police)) / 2, y), l, font=police, fill=couleur)
        else:
            d.text((x, y), l, font=police, fill=couleur)
        y += police.size * interligne
    return y


def pastille(d, x, y, t, police, fond_c=ROSE, texte_c=(255, 255, 255), pad=(36, 18)):
    w = largeur(d, t, police)
    d.rounded_rectangle([x, y, x + w + 2 * pad[0], y + police.size + 2 * pad[1]], radius=(police.size + 2 * pad[1]) // 2,
                        fill=fond_c)
    d.text((x + pad[0], y + pad[1] - police.size * 0.08), t, font=police, fill=texte_c)
    return x + w + 2 * pad[0]


def rond(d, cx, cy, r, t1, t2, fond_c=ROSE):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fond_c)
    d.ellipse([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10], outline=(255, 255, 255), width=3)
    p1, p2 = TITRE(int(r * 0.62)), GRAS(int(r * 0.24))
    centre(d, t1, p1, cy - r * 0.62, cx - r, cx + r, (255, 255, 255))
    centre(d, t2, p2, cy + r * 0.12, cx - r, cx + r, (255, 255, 255))


def entete(d, sur_titre, titre, sous_titre=None, y=120, couleur_sur=ROSE):
    centre(d, sur_titre.upper(), GRAS(44), y, couleur=couleur_sur)
    centre(d, titre, TITRE(124), y + 70)
    if sous_titre:
        centre(d, sous_titre, MAIN(78), y + 230, couleur=ROSE)


def bulle(d, x, y, titre, texte, lmax=560, couleur=SAUGE):
    """Encart explicatif : pastille numérotée ou point de couleur + titre + texte, sur carte crème."""
    pt, ptx = GRAS(50), TEXTE(40)
    hl = len(lignes(d, texte, ptx, lmax - 80)) * ptx.size * 1.35
    h = 60 + pt.size + 20 + hl + 40
    d.rounded_rectangle([x, y, x + lmax, y + h], radius=34, fill=(252, 249, 243), outline=(228, 218, 202), width=3)
    d.ellipse([x + 40, y + 52, x + 66, y + 78], fill=couleur)
    d.text((x + 86, y + 38), titre, font=pt, fill=BRUN)
    bloc(d, texte, ptx, x + 40, y + 60 + pt.size + 18, lmax - 80)
    return y + h


def loupe(im, src, boite, centre_xy, r, zoom=1.0):
    """Cercle grossissant : montre le détail `boite` (coordonnées dans src) dans un rond cerclé."""
    cx, cy = (boite[0] + boite[2]) / 2, (boite[1] + boite[3]) / 2
    c = max(boite[2] - boite[0], boite[3] - boite[1]) / 2
    cx = min(max(cx, c), src.width - c); cy = min(max(cy, c), src.height - c)
    taille = int(2 * r)
    morceau = src.crop((int(cx - c), int(cy - c), int(cx + c), int(cy + c))).resize((taille, taille), Image.LANCZOS)
    masque = Image.new("L", (taille, taille), 0)
    ImageDraw.Draw(masque).ellipse([0, 0, taille - 1, taille - 1], fill=255)
    rondi = Image.new("RGBA", (taille + 24, taille + 24), (0, 0, 0, 0))
    ImageDraw.Draw(rondi).ellipse([0, 0, taille + 23, taille + 23], fill=(255, 255, 255, 255))
    rondi.paste(morceau, (12, 12), masque)
    ImageDraw.Draw(rondi).ellipse([4, 4, taille + 19, taille + 19], outline=OR, width=5)
    coller(im, rondi, centre_xy, 0, ombre=1.0, eleve=0.6)


def fleche(d, x, y, longueur=110, couleur=OR):
    d.line([(x, y), (x + longueur, y)], fill=couleur, width=8)
    d.polygon([(x + longueur + 20, y), (x + longueur - 12, y - 20), (x + longueur - 12, y + 20)], fill=couleur)


def signature(d, y=H - 110, couleur=(150, 132, 116)):
    centre(d, "Clarté Mentale  ·  planner à imprimer en français", TEXTE(40), y, couleur=couleur)


def enregistrer(im, nom):
    chemin = os.path.join(DOSSIER, nom)
    im.convert("RGB").save(chemin, quality=92, optimize=True, progressive=True)
    return chemin


# ---------------------------------------------------------------- les 10 photos
def photo_01_couverture():
    im = fond((244, 236, 226), vignette=0.12).convert("RGBA")
    d = ImageDraw.Draw(im)
    # éventail de pages derrière la couverture
    coller(im, page(28, 700), (1180, 1040), 3, eleve=0.6)
    coller(im, page(6, 700), (1370, 1090), 9, eleve=0.7)
    coller(im, page(7, 700), (1540, 1160), 15, eleve=0.8)
    coller(im, page(1, 940), (760, 1160), -3, eleve=1.2)
    brin(d, 120, 2080, 520, -68)
    brin(d, 230, 2160, 420, -52, couleur=(150, 170, 140), couleur2=SAUGE)
    crayon(im, 1350, 2030, 700, -12)
    d = ImageDraw.Draw(im)
    # panneau de droite
    x0 = 1990
    d.text((x0, 260), "PLANNER EN FRANÇAIS", font=GRAS(48), fill=ROSE)
    d.text((x0, 340), "Alléger sa", font=MAIN(140), fill=ROSE)
    d.text((x0, 500), "charge", font=TITRE(176), fill=BRUN)
    d.text((x0, 690), "mentale", font=TITRE(176), fill=BRUN)
    d.text((x0, 940), "seul(e) et à deux", font=MAIN(96), fill=(150, 72, 54))
    y = 1110
    for t, c in (("Volet couple en 2 couleurs", PERS[0]), ("Version tablette cliquable", PERS[1]),
                 ("Bonus : kit frigo famille", (176, 140, 72)), ("Semaine d'exemple remplie", (140, 120, 160))):
        pastille(d, x0, y, t, GRAS(46), fond_c=c)
        y += 122
    d.text((x0, y + 40), "32 pages A4  ·  3 versions", font=TEXTE(52), fill=TXT)
    d.text((x0, y + 120), "prêt pour le classeur", font=TEXTE(52), fill=TXT)
    return enregistrer(im, "fiche-01-couverture.jpg")


def photo_02_a_deux():
    im = fond((236, 230, 238)).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "le volet à deux", "Qui pense à quoi, à la maison ?", "rendre visible ce qui ne l'est pas")
    coller(im, page(28, 820), (980, 1390), -4, eleve=1.0)
    coller(im, page(30, 820), (1700, 1420), 4, eleve=1.0)
    d = ImageDraw.Draw(im)
    p28 = page(28, 1654)
    loupe(im, p28, (900, 540, 1500, 1140), (470, 1660), 260)
    d = ImageDraw.Draw(im)
    x = 2230
    y = bulle(d, x, 620, "3 colonnes", "Penser, organiser, faire : c'est souvent « y penser » qui épuise.", 640, LAVANDE)
    y = bulle(d, x, y + 50, "Chacun sa page", "Vous remplissez chacun votre côté, puis vous comparez.", 640, ROSE)
    bulle(d, x, y + 50, "20 minutes à deux", "5 questions pour choisir ensemble, sans compter les points.", 640, SAUGE)
    signature(d)
    return enregistrer(im, "fiche-02-volet-a-deux.jpg")


def photo_mois_a_deux():
    im = fond((236, 230, 238)).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "nouveau : version couple", "Une couleur chacun", "et la répartition qui bouge, mois après mois")
    coller(im, page(31, 860), (1050, 1330), -3, eleve=1.0)
    p = page(31, 1654)
    loupe(im, p, (300, 560, 1100, 1360), (420, 1720), 250)
    d = ImageDraw.Draw(im)
    x = 1700
    y = bulle(d, x, 560, "Ta couleur, la sienne", "Chaque case se coche dans la couleur de celui qui porte la tâche.", 1100, PERS[0])
    y = bulle(d, x, y + 50, "Notre mois à deux", "Chaque dimanche, on colorie qui a porté chaque domaine. En 4 semaines, on voit ce qui change.", 1100, PERS[1])
    bulle(d, x, y + 50, "Sans compter les points", "Un rendez-vous de 20 minutes, 5 questions, pour choisir ensemble.", 1100, (110, 140, 100))
    signature(d)
    return enregistrer(im, "fiche-03-mois-a-deux.jpg")


def aimant(im, cx, cy, couleur):
    a = Image.new("RGBA", (90, 90), (0, 0, 0, 0))
    dd = ImageDraw.Draw(a)
    dd.ellipse([2, 2, 87, 87], fill=couleur)
    dd.ellipse([18, 14, 46, 38], fill=tuple(min(255, c + 50) for c in couleur))
    coller(im, a, (cx, cy), 0, ombre=1.0, eleve=0.3)


def photo_kit_frigo():
    im = fond((226, 232, 234), vignette=0.12).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "bonus inclus", "Le kit frigo pour toute la famille", "3 pages à afficher, un prénom par couleur", couleur_sur=PERS[1])
    for i, (n, x, ang) in enumerate(((1, 720, -2), (2, 1500, 1), (3, 2280, 2.5))):
        coller(im, page(n, 700, "k"), (x, 1300), ang, eleve=0.5)
        aimant(im, x - 10, 1300 - 495, PERS[i])
    d = ImageDraw.Draw(im)
    centre(d, "Qui fait quoi cette semaine  ·  Notre semaine  ·  Chacun son domaine", GRAS(56), 2030, couleur=BRUN)
    return enregistrer(im, "fiche-04-kit-frigo.jpg")


def photo_tablette():
    im = fond((232, 234, 238)).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "version tablette incluse", "Onglets et sommaire cliquables", "GoodNotes, Notability, Xodo… et toute appli de PDF",
           couleur_sur=PERS[1])
    coller(im, tablette(page(2, 820, "t"), 820), (1000, 1330), -3, eleve=1.2)
    coller(im, tablette(page(12, 640, "t"), 640), (1880, 1420), 5, eleve=1.0)
    stylet(im, 2350, 2000, 560, -60)
    d = ImageDraw.Draw(im)
    x = 2330
    y = bulle(d, x, 600, "Sommaire", "Une ligne touchée, tu y es.", 600, PERS[1])
    y = bulle(d, x, y + 40, "Onglets", "Exemple, semaines 1 à 4, à deux.", 600, PERS[0])
    bulle(d, x, y + 40, "Retour", "Le bas de chaque page ramène au sommaire.", 600, (110, 140, 100))
    return enregistrer(im, "fiche-05-tablette-cliquable.jpg")


def photo_03_exemple():
    im = fond((234, 236, 228)).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "pas de page blanche", "Une semaine d'exemple déjà remplie", "pour voir tout de suite comment faire", couleur_sur=SAUGE)
    coller(im, page(4, 780), (740, 1200), -6, eleve=0.8)
    coller(im, page(5, 780), (1500, 1180), 0, eleve=0.9)
    coller(im, page(6, 780), (2260, 1200), 6, eleve=0.8)
    p6 = page(6, 1654)
    loupe(im, p6, (110, 330, 860, 1080), (2700, 1700), 250)
    p5 = page(5, 1654)
    loupe(im, p5, (100, 330, 850, 1080), (330, 1700), 250)
    d = ImageDraw.Draw(im)
    for i, (t, x) in enumerate((("Vide-tête", 980), ("Tri", 1500), ("Ma semaine", 2020))):
        centre(d, t, GRAS(64), 1990, x - 300, x + 300, BRUN)
    fleche(d, 1180, 2032, 170)
    fleche(d, 1600, 2032, 190)
    return enregistrer(im, "fiche-06-exemple-rempli.jpg")


def photo_04_parcours():
    im = fond((240, 234, 224)).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "chaque semaine, 4 étapes", "Sortir tout de ta tête, puis trier")
    etapes = [(8, "Vide-tête", "tout ce qui tourne, sans trier"), (9, "Le tri", "je m'en occupe, je délègue, plus tard, je lâche"),
              (10, "Ma semaine", "3 priorités par jour, pas plus"), (11, "Le bilan", "ce qui a allégé ta semaine")]
    xs = [420, 1140, 1860, 2580]
    for i, ((n, t, s), x) in enumerate(zip(etapes, xs)):
        coller(im, page(n, 560), (x, 1060), [-3, 2, -2, 3][i], eleve=0.7)
        d = ImageDraw.Draw(im)
        d.ellipse([x - 62, 1500, x + 62, 1624], fill=[SAUGE, ROSE, (176, 140, 92), BRUME][i])
        centre(d, str(i + 1), TITRE(86), 1506, x - 62, x + 62, (255, 255, 255))
        centre(d, t, TITRE(76), 1660, x - 330, x + 330)
        bloc(d, s, TEXTE(44), x - 300, 1780, 600, centrer=True)
        if i < 3:
            fleche(d, x + 290, 1562, 100)
    signature(d)
    return enregistrer(im, "fiche-07-parcours-semaine.jpg")


def photo_05_onglets():
    im = fond((238, 234, 226)).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "un vrai classeur", "4 semaines, 4 couleurs, des onglets", "et une intention au début de chaque semaine",
           couleur_sur=(176, 140, 92))
    for i, (n, ang) in enumerate(zip((7, 12, 17, 22), (-7, -2.5, 2.5, 7))):
        coller(im, page(n, 780), (720 + i * 520, 1200 + abs(i - 1.5) * 40), ang, eleve=0.6 + 0.15 * i)
    d = ImageDraw.Draw(im)
    centre(d, "Exemple  ·  Semaine 1 à 4  ·  À deux", GRAS(58), 2050, couleur=BRUN)
    return enregistrer(im, "fiche-08-onglets-couleurs.jpg")


def photo_06_contenu():
    im = fond((240, 236, 228)).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "tout ce que tu reçois", "32 pages + le kit frigo", y=90)
    cols, lw = 11, 236
    x0 = (W - cols * lw - (cols - 1) * 26) // 2
    for i in range(32):
        r, c = divmod(i, cols)
        x = x0 + c * (lw + 26) + lw // 2
        y = 640 + r * 410
        coller(im, page(i + 1, lw), (x, y), 0, ombre=0.7, eleve=0.25)
    d = ImageDraw.Draw(im)
    items = ["Mode d'emploi + « Pourquoi ça marche »", "Semaine d'exemple remplie", "4 semaines × 5 pages",
             "Les tâches invisibles", "Volet couple (4 pages)", "Bonus : kit frigo (3 pages)"]
    y = 1880
    for k, t in enumerate(items):
        col = k % 2
        x = 520 + col * 1180
        d.ellipse([x, y + 18, x + 26, y + 44], fill=[SAUGE, ROSE][col])
        d.text((x + 50, y), t, font=TEXTE(50), fill=TXT)
        if col == 1:
            y += 90
    return enregistrer(im, "fiche-09-contenu-complet.jpg")


def photo_07_versions():
    im = fond((236, 234, 230)).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "inclus dans ton achat", "3 versions + le kit frigo", "imprime ou annote, comme tu préfères", couleur_sur=SAUGE)
    coller(im, page(9, 720), (640, 1250), -3, eleve=1.0)
    coller(im, page(9, 720, "e"), (1500, 1250), 0, eleve=1.0)
    coller(im, tablette(page(10, 640, "t"), 640), (2360, 1250), 3, eleve=1.1)
    d = ImageDraw.Draw(im)
    for x, lib, c in ((640, "Couleur", ROSE), (1500, "Économe en encre", (120, 116, 110)), (2360, "Tablette", PERS[1])):
        w = largeur(d, lib, GRAS(56)) + 72
        pastille(d, x - w / 2, 1980, lib, GRAS(56), fond_c=c)
    return enregistrer(im, "fiche-10-trois-versions.jpg")


def tablette(page_im, largeur_ecran):
    """Tablette dessinée (bords arrondis, écran, caméra), sans marque."""
    ew, eh = largeur_ecran, round(largeur_ecran * page_im.height / page_im.width)
    b = 54
    t = Image.new("RGBA", (ew + 2 * b, eh + 2 * b), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rounded_rectangle([0, 0, t.width - 1, t.height - 1], radius=90, fill=(48, 48, 52))
    d.rounded_rectangle([6, 6, t.width - 7, t.height - 7], radius=86, outline=(90, 90, 96), width=3)
    t.paste(page_im.resize((ew, eh), Image.LANCZOS), (b, b))
    d.ellipse([t.width // 2 - 9, 20, t.width // 2 + 9, 38], fill=(30, 30, 34))
    return t


def stylet(im, x, y, longueur, angle):
    s = Image.new("RGBA", (longueur, 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    d.rounded_rectangle([0, 0, longueur - 60, 29], radius=14, fill=(245, 245, 243))
    d.polygon([(longueur - 62, 2), (longueur - 1, 15), (longueur - 62, 27)], fill=(225, 225, 222))
    d.line([(20, 8), (longueur - 90, 8)], fill=(255, 255, 255), width=4)
    coller(im, s, (x, y), angle, ombre=0.8, eleve=0.25)


def photo_09_methode():
    im = fond((242, 236, 228)).convert("RGBA")
    d = ImageDraw.Draw(im)
    coller(im, page(3, 900), (760, 1130), -3, eleve=1.0)
    brin(d, 1250, 2180, 460, -100)
    d = ImageDraw.Draw(im)
    x = 1460
    d.text((x, 230), "UNE MÉTHODE, PAS DES SLOGANS", font=GRAS(46), fill=ROSE)
    d.text((x, 300), "Pourquoi ça marche", font=TITRE(130), fill=BRUN)
    y = bulle(d, x, 560, "Penser à tout est un travail",
              "La sociologue Monique Haicault l'a décrit dès 1984 : prévoir, organiser, se souvenir, en plus de faire.",
              1340, ROSE)
    y = bulle(d, x, y + 50, "Un plan écrit libère la tête",
              "Florida State University, 2011 : noter un plan précis pour une tâche en suspens réduit les pensées qui y reviennent.",
              1340, SAUGE)
    bulle(d, x, y + 50, "Expliqué dans le planner",
          "Une page simple, avec les sources, pour comprendre à quoi sert chaque étape.", 1340, (176, 140, 92))
    centre(d, "« Pas besoin de tout faire. Juste de tout poser. »", MAIN(84), 1830, 1460, 2800, ROSE)
    return enregistrer(im, "fiche-11-pourquoi-ca-marche.jpg")


def photo_10_comment():
    im = fond((238, 234, 226)).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "téléchargement immédiat", "Comment ça marche ?", "aucun envoi postal : tout est en PDF")
    etapes = [("1", "Achète", "le planner sur Etsy"), ("2", "Télécharge", "les PDF, tout de suite"),
              ("3", "Imprime", "en A4, perfore, range dans ton classeur"), ("4", "Allège", "une semaine après l'autre")]
    for i, (n, t, s) in enumerate(etapes):
        x = 450 + i * 700
        d.rounded_rectangle([x - 290, 700, x + 290, 1500], radius=50, fill=(252, 249, 243), outline=(228, 218, 202), width=3)
        d.ellipse([x - 110, 790, x + 110, 1010], fill=[SAUGE, ROSE, (176, 140, 92), LAVANDE][i])
        centre(d, n, TITRE(150), 800, x - 110, x + 110, (255, 255, 255))
        centre(d, t, TITRE(84), 1100, x - 290, x + 290)
        bloc(d, s, TEXTE(46), x - 250, 1240, 500, centrer=True)
    bloc(d, "Pour ton usage personnel. Outil d'organisation, pas un soin : si tu te sens épuisé(e) depuis des semaines, "
            "parles-en à ton médecin.", TEXTE(44), 500, 1700, 2000, couleur=(130, 116, 104), centrer=True)
    signature(d, y=1950)
    return enregistrer(im, "fiche-12-comment-ca-marche.jpg")


if __name__ == "__main__":
    rendre_pages()
    for vieux in glob.glob(os.path.join(DOSSIER, "fiche-*.jpg")):
        os.remove(vieux)
    for fn in (photo_01_couverture, photo_02_a_deux, photo_mois_a_deux, photo_kit_frigo, photo_tablette, photo_03_exemple,
               photo_04_parcours, photo_05_onglets, photo_06_contenu, photo_07_versions, photo_09_methode, photo_10_comment):
        print(fn())
