"""Produit Etsy n° 2 : journal « Apprivoiser ses émotions », 4 semaines, adultes, A4, en français.
Version 2 du design (05/11/2026, consigne de l'utilisateur : « améliore le design et enlève-moi l'arche. Je veux un design
plus qualitatif. Appuie-toi sur la concurrence d'Etsy ») : style éditorial des journaux les mieux notés d'Etsy
(MarrMarStudio, MorinotoStudio, MieksDesign, The Calm Mind Journal) : papier blanc chaud uni, beaucoup d'espace,
titres serif fins (Cormorant Garamond), étiquettes en petites capitales espacées (Jost), filets fins, couleurs sourdes,
aucun aplat lourd, couverture pleine couleur avec cadre fin et brin dessiné au trait. Plus d'arche.
Contenu : mode d'emploi, « Pourquoi ça marche » (études vérifiées de l'article site/contenu/articles/gestion-des-emotions.md),
palette de 48 mots, carte du corps, fiche d'exemple, mois en couleurs, 4 semaines (ouverture, 3 fiches, bilan), boîte à
outils, repères, quand en parler, notes ; bonus aide-mémoire. Version économe en encre et version tablette cliquable.
Polices OFL (polices/), aucune IA, rien de payant. Appel : python3 outils/etsy/journal_emotions.py"""
import os, sys, math
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import planner_charge_mentale as P
from planner_charge_mentale import encre_econome, liens_pdf

POL = os.path.join(os.path.dirname(__file__), "..", "..", "polices") + "/"
SORTIE = os.path.join(os.path.dirname(__file__), "..", "..", "etsy", "journal-emotions")
NOM = "journal-apprivoiser-ses-emotions"
W, H = 1654, 2339
M = 140                       # marge gauche
L = W - 150                   # bord droit du contenu (onglets au-delà)
PAPIER = (252, 250, 246)
ENC = (58, 52, 48)            # encre des titres
TXT = (92, 84, 78)
TAUPE = (150, 136, 124)
FILET = (222, 214, 204)
TEINTE = (246, 242, 236)
STYLO = (38, 62, 112)         # écriture des exemples
SAUGE = ((132, 150, 126), (232, 237, 228)); BLUSH = ((200, 150, 138), (245, 232, 227))
SABLE = ((196, 166, 120), (244, 236, 222)); BRUME = ((138, 158, 174), (230, 236, 240))
LILAS = ((156, 140, 170), (237, 232, 241)); GREGE = ((160, 148, 138), (238, 234, 230))
COUV = (140, 152, 132)        # sauge sourd de la couverture
FAMILLES = [
    ("Joie", SABLE, ["contentement", "enthousiasme", "fierté", "soulagement", "gratitude", "amusement", "confiance",
                     "émerveillement"]),
    ("Calme", SAUGE, ["sérénité", "détente", "apaisement", "sécurité", "repos", "douceur", "tranquillité", "légèreté"]),
    ("Tristesse", BRUME, ["déception", "nostalgie", "solitude", "découragement", "abattement", "peine", "vide", "mélancolie"]),
    ("Colère", BLUSH, ["agacement", "frustration", "irritation", "contrariété", "indignation", "exaspération", "rancœur",
                       "impatience"]),
    ("Peur", LILAS, ["inquiétude", "tension", "nervosité", "anxiété", "appréhension", "méfiance", "angoisse", "panique"]),
    ("Honte et gêne", GREGE, ["gêne", "culpabilité", "embarras", "malaise", "humiliation", "regret", "timidité", "honte"]),
]
NB_MOTS = sum(len(f[2]) for f in FAMILLES)
ACC = {0: SAUGE, 1: SAUGE, 2: BLUSH, 3: SABLE, 4: BRUME, "outils": LILAS}
ONGLETS = [(0, "Exemple"), (1, "Sem. 1"), (2, "Sem. 2"), (3, "Sem. 3"), (4, "Sem. 4"), ("outils", "Outils")]
NB_PAGES = 31


@lru_cache(maxsize=None)
def police(fichier, taille, poids=None):
    ft = ImageFont.truetype(POL + fichier, taille)
    if poids:
        ft.set_variation_by_axes([poids])
    return ft


SERIF = lambda t, w=500: police("CormorantGaramond-VF.ttf", t, w)
ITAL = lambda t, w=500: police("CormorantGaramond-Italic-VF.ttf", t, w)
SANS = lambda t, w=400: police("Jost-VF.ttf", t, w)
MAIN = lambda t: police("DancingScript-Bold.ttf", t)


# ------------------------------------------------------------------ outils de dessin
def lignes(d, t, fo, l):
    t = t.replace(" ?", " ?").replace(" :", " :").replace(" !", " !").replace(" ;", " ;")
    out, cur = [], ""
    for m in t.split(" "):
        e = (cur + " " + m).strip()
        if d.textlength(e, font=fo) <= l:
            cur = e
        else:
            out.append(cur); cur = m
    out.append(cur)
    assert all(d.textlength(x, font=fo) <= l + 1 for x in out), out
    return out


def para(d, x, y, t, fo, l, fill=TXT, inter=1.5, centrer=False):
    for li in lignes(d, t, fo, l):
        xx = x + (l - d.textlength(li, font=fo)) / 2 if centrer else x
        d.text((xx, y), li, font=fo, fill=fill); y += int(fo.size * inter)
    return y


def larg_esp(d, t, fo, pas):
    return sum(d.textlength(c, font=fo) for c in t) + pas * (len(t) - 1)


def esp(d, x, y, t, fo, fill, pas=6, centre_entre=None, droite=None):
    """Capitales espacées ; centre_entre=(x0, x1) pour centrer, droite=x pour aligner à droite."""
    w = larg_esp(d, t, fo, pas)
    if centre_entre:
        assert w <= centre_entre[1] - centre_entre[0], t
        x = centre_entre[0] + (centre_entre[1] - centre_entre[0] - w) / 2
    elif droite is not None:
        x = droite - w
    for c in t:
        d.text((x, y), c, font=fo, fill=fill); x += d.textlength(c, font=fo) + pas
    return w


def centre(d, y, t, fo, fill, x0=0, x1=W):
    w = d.textlength(t, font=fo)
    assert w <= x1 - x0, ("trop large", t)
    d.text((x0 + (x1 - x0 - w) / 2, y), t, font=fo, fill=fill)


def chiffres(d, xy, t, fo, fill):
    """Chiffres alignés (« 01 » et non « 0I » : Cormorant a des chiffres elzéviriens par défaut)."""
    d.text(xy, t, font=fo, fill=fill, features=["lnum"])


def centre_ch(d, y, t, fo, fill, x0=0, x1=W):
    w = d.textlength(t, font=fo, features=["lnum"])
    assert w <= x1 - x0, t
    chiffres(d, (x0 + (x1 - x0 - w) / 2, y), t, fo, fill)


def etiquette(d, x, y, t, couleur=TAUPE):
    return esp(d, x, y, t.upper(), SANS(25, 500), couleur, pas=5)


def ligne(d, x0, y, x1, couleur=FILET, ep=2):
    d.line((x0, y, x1, y), fill=couleur, width=ep)


def lignes_ecriture(d, x0, y0, x1, y1, pas=74):
    y = y0 + pas
    while y <= y1:
        ligne(d, x0, y, x1); y += pas


def boite(d, x0, y0, x1, y1, fond=None, contour=FILET, r=18, ep=2):
    d.rounded_rectangle((x0, y0, x1, y1), r, fill=fond, outline=contour, width=ep)


def feuille_trait(d, x, y, ang, lg, larg, couleur, ep=3):
    ux, uy = math.cos(ang), math.sin(ang); vx, vy = -uy, ux
    a, b = [], []
    for k in range(17):
        t = k / 16; w = math.sin(math.pi * t) ** 0.85 * larg
        px, py = x + ux * lg * t, y + uy * lg * t
        a.append((px + vx * w, py + vy * w)); b.append((px - vx * w, py - vy * w))
    d.line(a + b[::-1] + [a[0]], fill=couleur, width=ep, joint="curve")
    d.line((x, y, x + ux * lg * 0.8, y + uy * lg * 0.8), fill=couleur, width=max(1, ep - 1))


def brin_trait(d, x, y, h, sens, couleur, ep=3, taille=1.0):
    """Brin au trait fin (« line art », comme les illustrations des best-sellers)."""
    pts = [(x + sens * 40 * taille * math.sin(t / 30 * 2.2), y - h * t / 30) for t in range(31)]
    d.line(pts, fill=couleur, width=ep, joint="curve")
    for k in range(3, 30, 4):
        px, py = pts[k]; t = k / 30; cote = 1 if (k // 4) % 2 else -1
        feuille_trait(d, px, py, -math.pi / 2 + cote * (1.0 - 0.35 * t), (70 - 26 * t) * taille, (19 - 6 * t) * taille, couleur, ep)
    feuille_trait(d, pts[-1][0], pts[-1][1], -math.pi / 2 + sens * 0.15, 52 * taille, 15 * taille, couleur, ep)


# ------------------------------------------------------------------ gabarit de page
def onglets(d, actif):
    h0, ht, g = 330, 150, 18
    for k, (cle, lib) in enumerate(ONGLETS):
        y0 = h0 + k * (ht + g); fort, clair = ACC[cle]
        x0 = W - 66 if cle == actif else W - 50
        d.rounded_rectangle((x0, y0, W - 10, y0 + ht), 14, fill=fort if cle == actif else clair)
        fo = SANS(22, 500)
        t = Image.new("RGBA", (ht, 36), (0, 0, 0, 0)); dt = ImageDraw.Draw(t)
        lib = lib.upper()
        w = larg_esp(dt, lib, fo, 2)
        assert w < ht - 10, lib
        esp(dt, (ht - w) / 2, 4, lib, fo, PAPIER if cle == actif else fort, pas=2)
        t = t.rotate(90, expand=True)
        d._image.paste(t, (int(x0 + 6), y0), t)


def page(onglet=None):
    img = Image.new("RGB", (W, H), PAPIER); d = ImageDraw.Draw(img)
    if onglet is not None:
        onglets(d, onglet)
    return img, d


def pied(d, num):
    t = f"APPRIVOISER SES ÉMOTIONS  ·  {num}".upper()
    esp(d, 0, H - 100, t, SANS(21, 400), TAUPE, pas=4, centre_entre=(0, W))


def entete(d, label, titre, num, acc=SAUGE, date=True):
    etiquette(d, M, 118, label, acc[0])
    fo = SERIF(100, 500)
    lmax = L - M - (330 if date else 0)
    while d.textlength(titre, font=fo) > lmax:
        fo = SERIF(fo.size - 4, 500)
    d.text((M, 150), titre, font=fo, fill=ENC)
    if date:
        etiquette(d, L - 300, 214, "date")
        ligne(d, L - 210, 246, L)
    ligne(d, M, 304, L)
    ligne(d, M, 304, M + 90, acc[0], 4)
    pied(d, num)
    return 360


def ecrire(d, x, y_ligne, t, l, taille=40):
    fo = MAIN(taille)
    assert d.textlength(t, font=fo) <= l, ("exemple trop long", t)
    d.text((x, y_ligne - 52), t, font=fo, fill=STYLO)


# ------------------------------------------------------------------ pages
def couverture(fonce=True):
    fond = COUV if fonce else (246, 243, 237)
    img = Image.new("RGB", (W, H), fond)
    bruit = Image.effect_noise((W, H), 14).filter(ImageFilter.GaussianBlur(0.6))
    img = Image.blend(img, Image.merge("RGB", [bruit] * 3), 0.05)
    d = ImageDraw.Draw(img)
    clair = (246, 242, 234) if fonce else ENC
    doux = (226, 228, 216) if fonce else TAUPE
    d.rectangle((110, 110, W - 110, H - 110), outline=doux, width=2)
    d.rectangle((126, 126, W - 126, H - 126), outline=doux, width=1)
    esp(d, 0, 330, "JOURNAL  ·  4 SEMAINES", SANS(30, 400), doux, pas=9, centre_entre=(0, W))
    brin_trait(d, W / 2 - 10, 1010, 420, 1, clair, ep=3, taille=1.15)
    esp(d, 0, 1110, "APPRIVOISER", SERIF(132, 400), clair, pas=14, centre_entre=(0, W))
    centre(d, 1275, "ses émotions", ITAL(150, 400), clair)
    ligne(d, W / 2 - 120, 1500, W / 2 + 120, doux, 2)
    for k, t in enumerate(("les remarquer, les nommer,", "les comprendre, et choisir quoi en faire")):
        centre(d, 1550 + k * 62, t, SERIF(50, 400), clair)
    for k, (_, (fort, _), _) in enumerate(FAMILLES):
        cx = W / 2 + (k - 2.5) * 58
        d.ellipse((cx - 13, 1745, cx + 13, 1771), fill=None if fonce else fort, outline=clair if fonce else fort, width=2)
    esp(d, 0, H - 330, f"{NB_PAGES} PAGES A4  ·  3 VERSIONS  ·  EN FRANÇAIS", SANS(26, 400), doux, pas=6, centre_entre=(0, W))
    esp(d, 0, H - 260, "CLARTÉ MENTALE", SANS(26, 500), doux, pas=8, centre_entre=(0, W))
    return img


def mode_emploi():
    img, d = page()
    y = entete(d, "avant de commencer", "Mode d'emploi", 2, date=False) + 20
    y = para(d, M, y, "Une émotion n'est ni bonne ni mauvaise : c'est un signal. Ce journal t'aide à le remarquer, à mettre "
             "un mot dessus et à choisir ta réponse, plutôt que de la subir.", SANS(36, 350), L - M) + 40
    etapes = [("01", "Remarque", "Une réaction plus forte que d'habitude ? Note le moment et ce qui s'est passé."),
              ("02", "Nomme", "Cherche le mot juste dans la palette, puis note où tu le sens dans ton corps."),
              ("03", "Comprends", "Ce que tu t'es dit, ce dont tu avais besoin, et une autre façon de voir."),
              ("04", "Choisis", "Une réponse qui te ressemble. Le dimanche, le bilan montre ce qui t'aide.")]
    for n, t, txt in etapes:
        chiffres(d, (M, y - 14), n, SERIF(110, 400), SAUGE[0])
        d.text((M + 200, y), t, font=SERIF(64, 600), fill=ENC)
        para(d, M + 200, y + 88, txt, SANS(36, 350), L - M - 200)
        y += 300
        ligne(d, M, y - 50, L)
    y += 10
    boite(d, M, y, L, y + 250, fond=TEINTE, contour=TEINTE)
    etiquette(d, M + 50, y + 40, "à savoir", BLUSH[0])
    para(d, M + 50, y + 90, "Ce journal est un outil personnel, pas un soin. Si une émotion déborde souvent, si une "
         "tristesse ou une inquiétude ne te quitte plus, parles-en à ton médecin ou à un psychologue. En cas d'idées "
         "noires : 3114, gratuit, 24 h/24.", SANS(31, 350), L - M - 100)
    para(d, M, y + 300, "Impression : A4, « taille réelle » (100 %), recto seul. Imprime les fiches émotion autant de "
         "fois que tu veux.", SANS(29, 350), L - M, fill=TAUPE)
    return img


def pourquoi(num):
    img, d = page()
    y = entete(d, "ce que disent les recherches", "Pourquoi ça marche", num, date=False) + 30
    blocs = [
        ("Mettre un mot apaise", "Nommer l'émotion ressentie devant des images négatives diminuait la réaction de "
         "l'amygdale, une zone du cerveau qui réagit à ce qui inquiète. D'où la palette de mots.",
         "Lieberman et al., Université de Californie à Los Angeles, Psychological Science, 2007"),
        ("Changer de point de vue aide", "Sur 306 comparaisons issues d'expériences, changer sa façon de voir la situation "
         "faisait partie des stratégies qui marchaient le mieux. D'où la case « une autre façon de voir ».",
         "Webb et al., Université de Sheffield, Psychological Bulletin, 2012"),
        ("Ruminer n'aide pas", "Sur 114 études, la rumination était la stratégie la plus liée à l'anxiété et à la "
         "dépression. On écrit une fois, puis on choisit quoi faire.",
         "Aldao et al., Université Yale, Clinical Psychology Review, 2010"),
        ("Le sommeil compte", "Sur 64 études, le manque de sommeil augmente l'humeur négative. D'où la case sommeil du bilan.",
         "Tomaso et al., Université du Nebraska, Sleep, 2021"),
    ]
    for k, (t, txt, src) in enumerate(blocs):
        chiffres(d, (M, y - 4), f"0{k + 1}", SERIF(84, 400), SAUGE[0])
        d.text((M + 150, y + 6), t, font=SERIF(62, 600), fill=ENC)
        yy = para(d, M + 150, y + 96, txt, SANS(35, 350), L - M - 150)
        yy = para(d, M + 150, yy + 8, src, ITAL(35, 500), L - M - 150, fill=TAUPE, inter=1.3)
        y = yy + 80
        if k < 3:
            ligne(d, M + 150, y - 40, L)
    assert y < H - 340, y
    centre(d, y + 70, "Pas de bonne ou de mauvaise émotion.", ITAL(66, 500), BLUSH[0], M, L)
    centre(d, y + 150, "Juste des signaux.", ITAL(66, 500), BLUSH[0], M, L)
    return img


def palette(num):
    img, d = page(onglet="outils")
    y = entete(d, "pour trouver le mot juste", "La palette des émotions", num, LILAS, date=False)
    y = para(d, M, y, "Plus le mot est précis, plus il est facile de savoir quoi faire. Pars de la famille, puis cherche "
             "la nuance.", SANS(33, 350), L - M) + 20
    g = 36; lw = (L - M - g) / 2; lh = (H - 190 - y - 2 * g) / 3
    for k, (nom, (fort, clair), mots) in enumerate(FAMILLES):
        x0 = M + (k % 2) * (lw + g); y0 = y + (k // 2) * (lh + g)
        boite(d, x0, y0, x0 + lw, y0 + lh, fond=None, contour=FILET)
        d.rectangle((x0 + 1, y0 + 30, x0 + 7, y0 + lh - 30), fill=fort)
        d.text((x0 + 44, y0 + 26), nom, font=SERIF(58, 600), fill=ENC)
        ligne(d, x0 + 44, y0 + 112, x0 + lw - 40, FILET, 1)
        for i, m in enumerate(mots):
            xx = x0 + 44 + (i % 2) * (lw / 2 - 18); yy = y0 + 140 + (i // 2) * 88
            assert d.textlength(m, font=SANS(34, 350)) < lw / 2 - 40, m
            d.ellipse((xx, yy + 18, xx + 10, yy + 28), fill=clair, outline=fort, width=1)
            d.text((xx + 24, yy), m, font=SANS(34, 350), fill=TXT)
        assert y0 + 140 + 3 * 88 + 50 < y0 + lh, (nom, lh)
    return img


def silhouette(d, cx, top, h, couleur, ep=3):
    """Silhouette de face au trait, proportions simples (tête = 1/7,5 de la hauteur)."""
    u = h / 7.5
    d.ellipse((cx - 0.42 * u, top, cx + 0.42 * u, top + u), outline=couleur, width=ep)
    droite = [(0.17, 1.0), (0.18, 1.18), (0.95, 1.38), (1.08, 1.6), (1.22, 2.6), (1.32, 3.55), (1.36, 3.85),
              (1.2, 3.9), (1.1, 3.55), (0.98, 2.7), (0.92, 2.25), (0.86, 2.9), (0.9, 3.6), (0.78, 5.2), (0.7, 6.9),
              (0.74, 7.25), (0.28, 7.25), (0.3, 6.9), (0.18, 4.9), (0.06, 4.0), (0.0, 4.0)]
    pts = [(cx + x * u, top + y * u) for x, y in droite]
    gauche = [(cx - x * u, top + y * u) for x, y in reversed(droite)]
    d.line(pts + gauche[1:] + [pts[0]], fill=couleur, width=ep, joint="curve")
    for yy in (2.15, 2.95):
        y = top + yy * u
        x = cx - 0.75 * u
        while x < cx + 0.75 * u:
            d.line((x, y, x + 12, y), fill=FILET, width=2); x += 26


def carte_corps(num):
    img, d = page(onglet="outils")
    y = entete(d, "où je la sens", "La carte du corps", num, LILAS, date=False)
    y = para(d, M, y, "Une émotion se sent aussi dans le corps. Colorie les zones où tu la sens, et coche ce que tu "
             "remarques.", SANS(33, 350), L - M) + 30
    silhouette(d, M + 330, y + 30, 1500, ENC, 3)
    sens = ["Mâchoire serrée", "Gorge nouée", "Chaleur au visage", "Cœur qui s'accélère", "Souffle court",
            "Épaules lourdes", "Ventre noué", "Mains moites", "Jambes molles", "Fatigue soudaine", "Tête qui tourne vite",
            "Corps détendu", "Autre :"]
    x0 = M + 760; yy = y + 40
    for s in sens:
        d.ellipse((x0, yy + 10, x0 + 34, yy + 44), outline=LILAS[0], width=2)
        assert d.textlength(s, font=SANS(35, 350)) < L - x0 - 60, s
        d.text((x0 + 56, yy + 2), s, font=SANS(35, 350), fill=TXT)
        if s == "Autre :":
            ligne(d, x0 + 190, yy + 44, L)
        yy += 112
    assert yy < H - 180
    return img


BESOINS = ["repos", "calme", "respect", "sécurité", "lien", "reconnaissance", "temps", "aide"]


def fiche(s, num, ex=None):
    img, d = page(onglet=s)
    fort, clair = ACC[s]
    y = entete(d, "exemple rempli" if ex else f"semaine {s}  ·  fiche émotion", "Quand une émotion monte", num, ACC[s])
    ex = ex or {}

    def champ(y, t, cle=None, n=1, pas=72):
        etiquette(d, M, y, t)
        yl = y + 30
        for i in range(n):
            ligne(d, M, yl + pas * (i + 1), L)
            if cle and i < len(ex.get(cle, [])):
                ecrire(d, M + 16, yl + pas * (i + 1) - 2, ex[cle][i], L - M - 30)
        return yl + pas * n + 40

    def echelle(y, t, cle):
        etiquette(d, M, y + 16, t)
        x = M + 330; pas = (L - x) / 11
        for i in range(11):
            cx = x + i * pas + pas / 2
            plein = ex.get(cle) == i
            d.ellipse((cx - 25, y, cx + 25, y + 50), outline=fort, width=2, fill=fort if plein else None)
            centre(d, y + 8, str(i), SANS(26, 400), PAPIER if plein else TXT, cx - 25, cx + 25)
        return y + 96

    y = champ(y, "quand", "quand", 1)
    y = champ(y, "ce qui s'est passé (les faits, comme une caméra)", "faits", 3)
    etiquette(d, M, y, "le mot juste")
    ligne(d, M + 230, y + 30, L)
    if "mot" in ex:
        ecrire(d, M + 246, y + 28, ex["mot"], L - M - 260)
    y += 80
    y = echelle(y, "intensité avant", "avant")
    y = champ(y, "où je le sens dans mon corps", "corps", 1)
    y = champ(y, "ce que je me suis dit", "pensee", 2)
    etiquette(d, M, y, "ce dont j'avais besoin")
    y += 50; x = M
    for b in BESOINS:
        w = d.textlength(b, font=SANS(30, 400)) + 56
        if x + w > L:
            x = M; y += 66
        coche = b in ex.get("besoins", [])
        d.rounded_rectangle((x, y, x + w, y + 50), 25, outline=fort, width=2, fill=clair if coche else None)
        d.text((x + 28, y + 6), b, font=SANS(30, 500 if coche else 400), fill=ENC if coche else TXT)
        x += w + 16
    y += 96
    y = champ(y, "une autre façon de voir la situation", "autre", 2)
    y = champ(y, "ce que je choisis de faire", "choix", 2)
    y = echelle(y, "intensité après", "apres")
    assert y < H - 140, ("fiche trop haute", y)
    return img


EX_FICHE = {"quand": ["Mardi, 18 h 30, en rentrant du travail"],
            "faits": ["Réunion déplacée au dernier moment : j'ai annulé mon cours de sport.",
                      "En rentrant, la vaisselle de midi était encore dans l'évier."],
            "mot": "exaspération (famille colère)", "avant": 7,
            "corps": ["Mâchoire serrée, chaleur au visage, épaules hautes"],
            "pensee": ["« C'est toujours moi qui m'adapte. »", "« Personne ne pense à ce que je fais. »"],
            "besoins": ["repos", "reconnaissance"],
            "autre": ["Ce n'était pas contre moi : la journée a été lourde pour tout le monde.",
                      "J'ai le droit d'être à bout, et de le dire."],
            "choix": ["Cinq minutes au calme, à souffler lentement, puis demander", "de l'aide pour la vaisselle, sans reproche."],
            "apres": 4}


def mois_couleurs(num):
    img, d = page(onglet="outils")
    y = entete(d, "un coup d'œil sur le mois", "Mon mois en couleurs", num, LILAS, date=False)
    y = para(d, M, y, "Chaque soir, colorie le grand rond avec la couleur de l'émotion qui a dominé ta journée. Au bout du "
             "mois, ce qui revient saute aux yeux.", SANS(33, 350), L - M) + 20
    x = M
    for k, (nom, (fort, _), _) in enumerate(FAMILLES):
        if k == 3:
            x = M; y += 58
        d.ellipse((x, y + 8, x + 30, y + 38), fill=fort)
        d.text((x + 46, y), nom, font=SANS(31, 400), fill=TXT); x += 450
    y += 100
    cw = (L - M - 90) / 7; x0g = M + 90
    for j, jour in enumerate(["LUN", "MAR", "MER", "JEU", "VEN", "SAM", "DIM"]):
        esp(d, 0, y, jour, SANS(24, 500), TAUPE, pas=4, centre_entre=(x0g + j * cw, x0g + (j + 1) * cw))
    y += 60
    rh = (H - 330 - y) / 4
    for s in range(4):
        fort, clair = ACC[s + 1]; y0 = y + s * rh
        chiffres(d, (M, y0 + rh / 2 - 40), f"S{s + 1}", SERIF(56, 500), fort)
        if s:
            ligne(d, M, y0, L, FILET, 1)
        for j in range(7):
            cx = x0g + j * cw + cw / 2; cy = y0 + rh * 0.44; r = min(cw, rh) * 0.3
            d.text((cx - r - 8, y0 + 14), str(s * 7 + j + 1), font=SANS(22, 400), fill=TAUPE)
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=fort, width=2)
            for i in range(3):
                xx = cx - 34 + i * 26
                d.ellipse((xx, y0 + rh - 58, xx + 16, y0 + rh - 42), outline=TAUPE, width=2)
    y += 4 * rh + 10
    para(d, M, y, "Les trois petits ronds : ton sommeil de la nuit d'avant. Colorie-en un (bien), deux (moyen) ou trois "
         "(difficile).", SANS(29, 350), L - M, fill=TAUPE)
    return img


def ouverture(s, num):
    img, d = page(onglet=s)
    fort, clair = ACC[s]
    esp(d, 0, 300, "SEMAINE", SANS(34, 400), fort, pas=14, centre_entre=(M, L))
    centre_ch(d, 360, f"0{s}", SERIF(380, 300), fort, M, L)
    brin_trait(d, M + 150, 980, 360, 1, fort, ep=3)
    brin_trait(d, L - 150, 980, 330, -1, fort, ep=3)
    centre(d, 820, ["Remarquer, sans juger.", "Un mot à la fois.", "Écouter ce dont j'ai besoin.",
                    "Garder ce qui m'aide."][s - 1], ITAL(76, 500), ENC, M, L)
    ligne(d, W / 2 - 100, 950, W / 2 + 100, fort, 2)
    y = 1130
    for q in ("ce que je veux observer cette semaine", "une situation qui me fait souvent réagir",
              "ce que je m'autorise à ressentir"):
        etiquette(d, M, y, q)
        lignes_ecriture(d, M, y + 30, L, y + 290, pas=74)
        y += 330
    pied(d, num)
    return img


def bilan(s, num):
    img, d = page(onglet=s)
    fort, clair = ACC[s]
    y = entete(d, f"semaine {s}  ·  bilan", "Bilan de la semaine", num, ACC[s])
    qs = ["l'émotion qui est revenue le plus souvent", "ce qui l'a déclenchée (moments, situations)",
          "ce qui m'a aidé(e) à redescendre", "un moment agréable que je veux garder", "la semaine prochaine, j'essaie"]
    lh = (H - 190 - y - 180) / len(qs)
    for k, q in enumerate(qs):
        y0 = y + k * lh
        etiquette(d, M, y0 + 6, q)
        lignes_ecriture(d, M, y0 + 30, L, y0 + lh - 24, pas=72)
    y0 = y + len(qs) * lh + 10
    boite(d, M, y0, L, y0 + 150, fond=clair, contour=clair)
    etiquette(d, M + 40, y0 + 30, "mon sommeil cette semaine", ENC)
    x = M + 40
    for lib in ("bien", "moyen", "difficile"):
        d.ellipse((x, y0 + 86, x + 30, y0 + 116), outline=fort, width=2)
        d.text((x + 44, y0 + 78), lib, font=SANS(32, 400), fill=TXT); x += 90 + d.textlength(lib, font=SANS(32, 400))
    phrase = "Une nuit trop courte, et tout paraît plus lourd."
    wp = d.textlength(phrase, font=ITAL(36, 500))
    d.text((L - 40 - wp, y0 + 80), phrase, font=ITAL(36, 500), fill=TXT)
    assert L - 40 - wp > x + 20, (x, wp)
    return img


def boite_outils(num):
    img, d = page(onglet="outils")
    y = entete(d, "des pistes à tester", "Ma boîte à outils", num, LILAS, date=False)
    y = para(d, M, y, "Coche ce que tu as essayé, puis ce qui t'aide vraiment. Tout ne marche pas pour tout le monde : "
             "garde ce qui te ressemble.", SANS(33, 350), L - M) + 30
    esp(d, 0, y, "ESSAYÉ", SANS(22, 500), TAUPE, pas=3, centre_entre=(L - 290, L - 150))
    esp(d, 0, y, "ÇA M'AIDE", SANS(22, 500), TAUPE, pas=3, centre_entre=(L - 150, L))
    y += 50
    outils = [("Mettre un mot", "Chercher le mot juste dans la palette."),
              ("Souffler lentement", "Inspirer sur 4 temps, souffler sur 6, pendant 2 minutes."),
              ("Changer de point de vue", "Comment le verrais-je dans un an ?"),
              ("Prendre du recul", "Que dirais-je à un ami dans la même situation ?"),
              ("Bouger", "10 minutes de marche, d'étirements ou de danse."),
              ("En parler", "À une personne de confiance, sans chercher de solution."),
              ("Écrire sans filtre", "5 minutes, puis fermer le carnet."),
              ("Revenir au présent", "Nommer 5 choses que je vois, 4 que j'entends.")]
    rh = 150
    for k, (t, st) in enumerate(outils):
        y0 = y + k * rh
        ligne(d, M, y0, L, FILET, 1)
        d.text((M, y0 + 20), t, font=SERIF(48, 600), fill=ENC)
        assert d.textlength(st, font=SANS(29, 350)) < L - 320 - M, st
        d.text((M, y0 + 84), st, font=SANS(29, 350), fill=TXT)
        for cx in (L - 220, L - 75):
            d.ellipse((cx - 20, y0 + 55, cx + 20, y0 + 95), outline=LILAS[0], width=2)
    y = y + len(outils) * rh
    ligne(d, M, y, L, FILET, 1)
    y += 40
    boite(d, M, y, L, y + 230, fond=BLUSH[1], contour=BLUSH[1])
    etiquette(d, M + 40, y + 34, "ce qui ne m'aide pas, et que je repère", ENC)
    para(d, M + 40, y + 84, "ruminer en boucle, éviter tout ce qui dérange, tout garder pour moi. Les recherches les "
         "associent à plus de mal-être (Aldao et al., Université Yale, 2010).", SANS(30, 350), L - M - 80)
    assert y + 230 < H - 140, y
    return img


def reperes(num):
    img, d = page(onglet="outils")
    y = entete(d, "à la fin du mois", "Mes repères", num, LILAS)
    qs = ["les émotions que je ressens le plus souvent", "mes déclencheurs (moments, lieux, personnes)",
          "les signes de mon corps qui me préviennent", "mes besoins qui reviennent", "les outils qui m'aident le plus",
          "ce que je veux garder pour le mois prochain"]
    lh = (H - 190 - y) / len(qs)
    for k, q in enumerate(qs):
        y0 = y + k * lh
        etiquette(d, M, y0 + 6, q)
        lignes_ecriture(d, M, y0 + 30, L, y0 + lh - 24, pas=72)
    return img


def quand_en_parler(num):
    img, d = page()
    y = entete(d, "prendre soin de soi", "Quand en parler", num, BLUSH, date=False)
    y = para(d, M, y, "Ce journal t'aide à mieux te connaître. Il ne remplace pas un médecin ni un psychologue. Parles-en "
             "à un professionnel si :", SANS(35, 350), L - M) + 30
    for t in ("tes émotions débordent souvent ;", "tu as peur de tes propres réactions ;",
              "une tristesse ou une inquiétude ne te quitte plus ;",
              "tu évites de plus en plus de situations pour ne pas ressentir quelque chose."):
        d.ellipse((M + 6, y + 18, M + 22, y + 34), fill=BLUSH[0])
        y = para(d, M + 50, y, t, SANS(35, 350), L - M - 50) + 22
    y += 20
    y = para(d, M, y, "Tu peux consulter un psychologue directement, sans passer par ton médecin. Certaines séances sont "
             "remboursées avec Mon soutien psy (liste sur monsoutienpsy.ameli.fr).", SANS(33, 350), L - M) + 50
    boite(d, M, y, L, y + 540, fond=None, contour=BLUSH[0])
    etiquette(d, M + 50, y + 40, "numéros utiles", BLUSH[0])
    yy = y + 100
    for num_tel, lib in (("3114", "En cas d'idées noires : numéro national de prévention du suicide, gratuit, 24 h/24 et 7 j/7."),
                         ("15", "Urgence médicale : le SAMU."), ("112", "Numéro d'urgence européen, depuis n'importe quel téléphone.")):
        chiffres(d, (M + 50, yy - 14), num_tel, SERIF(84, 500), ENC)
        yy = max(yy + 120, para(d, M + 280, yy + 6, lib, SANS(32, 350), L - M - 330) + 50)
    assert yy < y + 540, yy
    centre(d, y + 620, "Demander de l'aide, c'est aussi prendre soin de soi.", ITAL(54, 500), SAUGE[0], M, L)
    return img


def notes(num):
    img, d = page()
    y = entete(d, "pour finir", "Notes", num, date=False)
    lignes_ecriture(d, M, y, L, H - 200, pas=76)
    return img


# ------------------------------------------------------------------ bonus
def bonus_cartes():
    img, d = page()
    y = entete(d, "à découper et à garder sur soi", "L'aide-mémoire", "bonus", date=False)
    g = 40; lw = (L - M - g) / 2; lh = (H - 230 - y - g) / 2
    cartes = [("01", "Remarque", "Qu'est-ce qui vient de se passer ? Les faits, juste les faits.", SAUGE),
              ("02", "Nomme", "Quel est le mot juste ? Où est-ce que je le sens ?", BRUME),
              ("03", "Comprends", "Qu'est-ce que je me dis ? De quoi ai-je besoin ?", LILAS),
              ("04", "Choisis", "Souffler 2 minutes, puis choisir une réponse qui me ressemble.", SABLE)]
    for k, (n, t, txt, (fort, clair)) in enumerate(cartes):
        x0 = M + (k % 2) * (lw + g); y0 = y + (k // 2) * (lh + g)
        for x in range(int(x0), int(x0 + lw), 26):
            d.line((x, y0, x + 12, y0), fill=FILET, width=2); d.line((x, y0 + lh, x + 12, y0 + lh), fill=FILET, width=2)
        for yy in range(int(y0), int(y0 + lh), 26):
            d.line((x0, yy, x0, yy + 12), fill=FILET, width=2); d.line((x0 + lw, yy, x0 + lw, yy + 12), fill=FILET, width=2)
        centre_ch(d, y0 + 90, n, SERIF(150, 300), fort, x0, x0 + lw)
        centre(d, y0 + 300, t, SERIF(74, 600), ENC, x0, x0 + lw)
        ligne(d, x0 + lw / 2 - 60, y0 + 410, x0 + lw / 2 + 60, fort, 2)
        yy = y0 + 450
        for li in lignes(d, txt, SANS(34, 350), lw - 120):
            centre(d, yy, li, SANS(34, 350), TXT, x0, x0 + lw); yy += 52
        assert yy < y0 + lh - 30
    return img


def bonus_palette():
    img, d = page()
    y = entete(d, "à garder dans son sac ou son agenda", "La palette de poche", "bonus", date=False)
    for e in range(2):
        hh = (H - 230 - y) / 2 - 40
        y0 = y + e * (hh + 80)
        lw = (L - M - 2 * 24) / 3; lh = (hh - 24) / 2
        for k, (nom, (fort, clair), mots) in enumerate(FAMILLES):
            x0 = M + (k % 3) * (lw + 24); yy = y0 + (k // 3) * (lh + 24)
            boite(d, x0, yy, x0 + lw, yy + lh, contour=FILET, r=14)
            d.rectangle((x0 + 1, yy + 20, x0 + 6, yy + lh - 20), fill=fort)
            d.text((x0 + 30, yy + 14), nom, font=SERIF(42, 600), fill=ENC)
            for i, m in enumerate(mots):
                assert d.textlength(m, font=SANS(27, 350)) < lw - 50, m
                d.text((x0 + 30, yy + 78 + i * 38), m, font=SANS(27, 350), fill=TXT)
            assert yy + 78 + 8 * 38 < yy + lh + 5, (nom, lh)
        if e == 0:
            ym = y0 + hh + 40
            for x in range(M, L, 26):
                d.line((x, ym, x + 12, ym), fill=FILET, width=2)
    return img


# ------------------------------------------------------------------ impression, tablette, assemblage
ECHELLE, DX = P.ECHELLE, P.DX
DY = (H - round(H * ECHELLE)) // 2


def fond_page(couv=False):
    if couv:
        return Image.new("RGB", (W, H), COUV if couv == "fonce" else (246, 243, 237))
    return Image.new("RGB", (W, H), PAPIER)


def mise_en_page_impression(img, couv=False):
    """Comme le planner : réduction à 93,5 % et décalage à droite (trous du classeur, bords non imprimables)."""
    petit = img.resize((round(W * ECHELLE), round(H * ECHELLE)), Image.LANCZOS)
    fond = fond_page(couv); fond.paste(petit, (DX, DY))
    return fond


def controle_marges(img, couv=False):
    import numpy as np
    a = np.asarray(img, np.int16); b = np.asarray(fond_page(couv), np.int16)
    ecart = np.abs(a - b).max(axis=2)
    zones = {"gauche": ecart[:, :P.ZONE_TROUS], "droite": ecart[:, W - P.ZONE_IMPRIMANTE:],
             "haut": ecart[:P.ZONE_IMPRIMANTE, :], "bas": ecart[H - P.ZONE_IMPRIMANTE:, :]}
    return {k: int((z > 40).sum()) for k, z in zones.items()}


SOMMAIRE = [("Mode d'emploi", 1, None), ("Pourquoi ça marche", 2, None), ("La palette des émotions", 3, "outils"),
            ("La carte du corps", 4, "outils"), ("Exemple rempli", 5, 0), ("Mon mois en couleurs", 6, "outils"),
            ("Semaine 1", 7, 1), ("Semaine 2", 12, 2), ("Semaine 3", 17, 3), ("Semaine 4", 22, 4),
            ("Ma boîte à outils", 27, "outils"), ("Mes repères", 28, "outils"), ("Quand en parler", 29, None), ("Notes", 30, None)]
DEBUT_SECTION = {0: 5, 1: 7, 2: 12, 3: 17, 4: 22, "outils": 3}
SANS_ONGLET = {0, 1, 2, 29, 30}


def sommaire():
    img, d = page()
    y = entete(d, "pour s'y retrouver", "Sommaire", "sommaire", date=False)
    y = para(d, M, y, "Touche une ligne pour y aller. Les onglets du bord renvoient au début de chaque partie, et le bas "
             "de chaque page ramène ici.", SANS(32, 350), L - M) + 30
    rects = []
    for lib, cible, coul in SOMMAIRE:
        if coul is not None:
            d.rectangle((M, y + 22, M + 6, y + 74), fill=ACC[coul][0])
        d.text((M + 34, y + 18), lib, font=SERIF(50, 500), fill=ENC)
        n = f"{cible + 1:02d}"
        d.text((L - d.textlength(n, font=SANS(32, 400)), y + 30), n, font=SANS(32, 400), fill=TAUPE)
        ligne(d, M, y + 96, L, FILET, 1)
        rects.append(((M, y, L, y + 96), cible)); y += 108
    assert y < H - 200, y
    return img, rects


def version_tablette(pages_brutes):
    som, rects = sommaire()
    pages = [pages_brutes[0], som] + pages_brutes[1:]
    chemin = os.path.join(SORTIE, f"{NOM}-tablette.pdf")
    pages[0].save(chemin, "PDF", resolution=200, save_all=True, append_images=pages[1:])
    liens = [(1, rect, cible + 1) for rect, cible in rects]
    for k in range(2, len(pages)):
        liens.append((k, (W / 2 - 420, H - 115, W / 2 + 420, H - 60), 1))
        if k - 1 not in SANS_ONGLET:
            for i, (cle, _) in enumerate(ONGLETS):
                y0 = 330 + i * 168
                liens.append((k, (W - 70, y0, W, y0 + 150), DEBUT_SECTION[cle] + 1))
    liens_pdf(chemin, liens)
    return chemin, len(pages), len(liens)


def fabriquer():
    os.makedirs(SORTIE, exist_ok=True)
    pages = [couverture(), mode_emploi(), pourquoi(3), palette(4), carte_corps(5), fiche(0, 6, EX_FICHE), mois_couleurs(7)]
    n = 8
    for s in range(1, 5):
        pages.append(ouverture(s, n)); n += 1
        for _ in range(3):
            pages.append(fiche(s, n)); n += 1
        pages.append(bilan(s, n)); n += 1
    for fn in (boite_outils, reperes, quand_en_parler, notes):
        pages.append(fn(n)); n += 1
    assert len(pages) == NB_PAGES, len(pages)
    print("tablette :", version_tablette(pages))
    imp = [mise_en_page_impression(p, couv="fonce" if k == 0 else False) for k, p in enumerate(pages)]
    for k, p in enumerate(imp[1:], start=1):
        m = controle_marges(p)
        assert all(v == 0 for v in m.values()), (k + 1, m)
    imp[0].save(os.path.join(SORTIE, f"{NOM}-A4.pdf"), "PDF", resolution=200, save_all=True, append_images=imp[1:])
    nb = [encre_econome(p) for p in [mise_en_page_impression(couverture(False), couv="clair")] + imp[1:]]
    nb[0].save(os.path.join(SORTIE, f"{NOM}-A4-econome-encre.pdf"), "PDF", resolution=200, save_all=True, append_images=nb[1:])
    bonus = [mise_en_page_impression(p) for p in (bonus_cartes(), bonus_palette())]
    for p in bonus:
        assert all(v == 0 for v in controle_marges(p).values())
    bonus[0].save(os.path.join(SORTIE, "aide-memoire-emotions-A4.pdf"), "PDF", resolution=200, save_all=True, append_images=bonus[1:])
    for k, p in enumerate(imp):
        p.resize((W // 2, H // 2), Image.LANCZOS).save(os.path.join(SORTIE, f"apercu-{k + 1:02d}.jpg"), quality=88)
    for k, p in enumerate(bonus):
        p.resize((W // 2, H // 2), Image.LANCZOS).save(os.path.join(SORTIE, f"apercu-bonus-{k + 1}.jpg"), quality=88)
    return len(imp)


if __name__ == "__main__":
    print(fabriquer())
