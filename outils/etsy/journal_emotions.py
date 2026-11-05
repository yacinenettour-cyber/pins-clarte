"""Produit Etsy n° 2 (05/11/2026, choix de l'utilisateur : « Journal des émotions ») : « Apprivoiser ses émotions »,
journal de 4 semaines pour adultes, A4 à imprimer, en français. Même famille visuelle que le planner charge mentale
(papier texturé, arche, onglets de classeur), couleur de couverture propre (vert sauge profond).
Contenu : mode d'emploi en 4 étapes, page « Pourquoi ça marche » (études vérifiées, reprises de l'article
site/contenu/articles/gestion-des-emotions.md), palette de 48 mots, carte du corps, fiche d'exemple remplie, mois en couleurs,
4 semaines (ouverture, 3 fiches émotion, bilan), boîte à outils, mes repères, quand en parler, notes.
Bonus : aide-mémoire (cartes à découper + palette de poche). Version économe en encre et version tablette cliquable.
Hors périmètre de la formation (pas de sommeil ni de ruminations du soir comme sujet, docs/business/plan-revenus.md).
Texte dessiné par PIL (polices OFL), aucune IA, rien de payant. Appel : python3 outils/etsy/journal_emotions.py"""
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops
sys.path.insert(0, os.path.dirname(__file__))
import planner_charge_mentale as P
from planner_charge_mentale import (W, H, M, CREME, SAUGE, SAUGE_C, ROSE, ROSE_C, BRUN, TXT, TRAIT, OR, ENCRE, SABLE,
                                    SABLE_C, BRUME, BRUME_C, LAVANDE, LAVANDE_C, TITRE, MAIN, TEXTE, GRAS, texture, lignes,
                                    centre, centre_esp, ornement, lignes_ecriture, cadre, paragraphe, brin, encre_econome, liens_pdf)

SORTIE = os.path.join(os.path.dirname(__file__), "..", "..", "etsy", "journal-emotions")
NOM = "journal-apprivoiser-ses-emotions"
MARQUE = (70, 96, 84)  # vert sauge profond (couverture)
GRIS_C = (232, 226, 220); GRIS = (140, 124, 112)
# familles d'émotions : (nom, couleur forte, couleur claire, mots)
FAMILLES = [
    ("Joie", (196, 150, 70), SABLE_C, ["contentement", "enthousiasme", "fierté", "soulagement", "gratitude", "amusement",
                                       "confiance", "émerveillement"]),
    ("Calme", SAUGE, SAUGE_C, ["sérénité", "détente", "apaisement", "sécurité", "repos", "douceur", "tranquillité",
                                "légèreté"]),
    ("Tristesse", BRUME, BRUME_C, ["déception", "nostalgie", "solitude", "découragement", "abattement", "peine", "vide",
                                   "mélancolie"]),
    ("Colère", (184, 92, 64), ROSE_C, ["agacement", "frustration", "irritation", "contrariété", "indignation",
                                       "exaspération", "rancœur", "impatience"]),
    ("Peur", LAVANDE, LAVANDE_C, ["inquiétude", "tension", "nervosité", "anxiété", "appréhension", "méfiance", "angoisse",
                                  "panique"]),
    ("Honte et gêne", GRIS, GRIS_C, ["gêne", "culpabilité", "embarras", "malaise", "humiliation", "regret", "timidité",
                                     "honte"]),
]
NB_MOTS = sum(len(f[3]) for f in FAMILLES)
ACC = {0: (SAUGE, SAUGE_C), 1: (SAUGE, SAUGE_C), 2: (ROSE, ROSE_C), 3: (SABLE, SABLE_C), 4: (BRUME, BRUME_C),
       "outils": (LAVANDE, LAVANDE_C)}
ONGLETS = [(0, "Ex."), (1, "S1"), (2, "S2"), (3, "S3"), (4, "S4"), ("outils", "Outils")]
NB_PAGES = 31


def onglets(d, actif):
    h0, ht, g = 330, 150, 18
    for k, (cle, lib) in enumerate(ONGLETS):
        y0 = h0 + k * (ht + g); fort, clair = ACC[cle]
        x0 = W - 70 if cle == actif else W - 52
        d.rounded_rectangle((x0, y0, W - 8, y0 + ht), 18, fill=fort if cle == actif else clair)
        fo = GRAS(26 if len(lib) < 4 else 22)
        t = Image.new("RGBA", (ht, 40), (0, 0, 0, 0)); dt = ImageDraw.Draw(t)
        assert dt.textlength(lib, font=fo) < ht - 8, lib
        dt.text(((ht - dt.textlength(lib, font=fo)) / 2, 2), lib, font=fo, fill=(255, 250, 240) if cle == actif else fort)
        t = t.rotate(90, expand=True)
        d._image.paste(t, (int(x0 + 8), y0), t)


def page(onglet=None):
    img = texture(); d = ImageDraw.Draw(img)
    if onglet is not None:
        onglets(d, onglet)
    return img, d


def pied(d, num):
    centre(d, H - 95, f"Apprivoiser ses émotions  ·  {num}", TEXTE(26), (150, 138, 124))


def entete(d, sur_titre, titre, num, acc=ROSE):
    centre_esp(d, M - 30, sur_titre.upper(), GRAS(30), acc)
    centre(d, M + 25, titre, TITRE(88), BRUN)
    ornement(d, M + 160)
    pied(d, num)
    return M + 220


def ecrire(d, x, y_ligne, t, l, taille=40):
    fo = MAIN(taille)
    assert d.textlength(t, font=fo) <= l, ("exemple trop long", t)
    d.text((x, y_ligne - 50), t, font=fo, fill=ENCRE)


def fond_couverture(fonce=True):
    img = texture()
    return Image.blend(img, Image.new("RGB", (W, H), MARQUE), 0.9) if fonce else \
        Image.blend(img, Image.new("RGB", (W, H), BRUME_C), 0.65)


def couverture(fonce=True):
    img = fond_couverture(fonce); d = ImageDraw.Draw(img)
    ax0, ax1, ay0, ay1 = 230, W - 230, 260, H - 260
    r = (ax1 - ax0) / 2
    masque = Image.new("L", (W, H), 0); dm = ImageDraw.Draw(masque)
    dm.ellipse((ax0, ay0, ax1, ay0 + 2 * r), fill=255); dm.rectangle((ax0, ay0 + r, ax1, ay1), fill=255)
    arche = texture()
    lav = Image.new("RGB", (W, H), CREME); dl = ImageDraw.Draw(lav)
    random.seed(681678)
    for cx, cy, rr, c in ((W / 2 + 140, ay0 + 330, 250, (222, 230, 237)), (W / 2 - 150, ay0 + 420, 240, (240, 222, 206)),
                          (W / 2, ay0 + 250, 190, (226, 233, 221))):
        for _ in range(6):
            dx, dy = random.randint(-40, 40), random.randint(-40, 40)
            dl.ellipse((cx - rr + dx, cy - rr + dy, cx + rr + dx, cy + rr + dy), fill=c)
    lav = lav.filter(ImageFilter.GaussianBlur(70))
    bruit = Image.effect_noise((W, H), 40).filter(ImageFilter.GaussianBlur(3)).point(lambda v: 200 + v // 4)
    lav = ImageChops.multiply(lav, Image.merge("RGB", [bruit] * 3))
    zone = Image.new("L", (W, H), 0); ImageDraw.Draw(zone).rectangle((0, 0, W, ay0 + 900), fill=255)
    arche = Image.composite(Image.blend(arche, lav, 0.75), arche, zone.filter(ImageFilter.GaussianBlur(160)))
    ombre = masque.filter(ImageFilter.GaussianBlur(26))
    img.paste((30, 46, 40) if fonce else (140, 150, 160), (14, 22), ombre.point(lambda v: v // 3))
    img.paste(arche, (0, 0), masque)
    d = ImageDraw.Draw(img)
    d.arc((ax0 + 30, ay0 + 30, ax1 - 30, ay0 + 2 * r - 30), 180, 360, fill=OR, width=3)
    for x in (ax0 + 30, ax1 - 30):
        d.line((x, ay0 + r, x, ay1 - 30), fill=OR, width=3)
    d.line((ax0 + 30, ay1 - 30, ax1 - 30, ay1 - 30), fill=OR, width=3)
    # six pastilles de couleur en arc (les six familles), au-dessus d'un brin
    cx0, cy0, rr = W / 2, ay0 + 760, 330
    for k, (_, fort, _, _) in enumerate(FAMILLES):
        a = math.radians(205 + k * 26)
        x, y = cx0 + rr * math.cos(a), cy0 + rr * math.sin(a)
        d.ellipse((x - 42, y - 42, x + 42, y + 42), fill=fort)
    brin(d, W / 2 - 40, ay0 + 780, 300, 1, (SAUGE, (150, 170, 142)))
    centre_esp(d, 1090, "JOURNAL DE 4 SEMAINES", GRAS(34), MARQUE)
    centre(d, 1160, "Apprivoiser ses", MAIN(120), ROSE)
    centre(d, 1300, "ÉMOTIONS", TITRE(140), MARQUE if fonce else BRUN)
    ornement(d, 1490)
    y = 1545
    for t in ("Les remarquer, les nommer,", "les comprendre, et choisir quoi en faire."):
        centre(d, y, t, TEXTE(50), TXT); y += 72
    centre(d, 1775, f"avec une palette de {NB_MOTS} mots et un exemple rempli", MAIN(50), SAUGE)
    centre(d, 1900, "Clarté Mentale", TEXTE(36), (140, 126, 110))
    if fonce:
        centre_esp(d, H - 190, "POUR ADULTES  ·  EN FRANÇAIS", GRAS(34), (236, 226, 204))
    cx, cy, rp = ax1 - 30, ay1 - 40, 125
    d.ellipse((cx - rp, cy - rp, cx + rp, cy + rp), fill=ROSE)
    d.ellipse((cx - rp + 12, cy - rp + 12, cx + rp - 12, cy + rp - 12), outline=(250, 236, 228), width=2)
    centre(d, cy - 70, str(NB_PAGES), TITRE(70), (255, 250, 242), cx - rp, cx + rp)
    centre(d, cy + 10, "pages A4", GRAS(30), (255, 250, 242), cx - rp, cx + rp)
    centre(d, cy + 48, "3 versions", GRAS(30), (255, 250, 242), cx - rp, cx + rp)
    return img


def mode_emploi():
    img, d = page()
    y = entete(d, "avant de commencer", "Mode d'emploi", 2)
    y = paragraphe(d, M, y + 10, "Une émotion n'est ni bonne ni mauvaise : c'est un signal. Ce journal t'aide à le "
                   "remarquer, à mettre un mot dessus et à choisir ta réponse, plutôt que de la subir.", TEXTE(40), W - 2 * M)
    etapes = [("1", "Remarque", "Une réaction plus forte que d'habitude ? Note le moment et ce qui s'est passé."),
              ("2", "Nomme", "Cherche le mot juste dans la palette, puis note où tu le sens dans ton corps."),
              ("3", "Comprends", "Ce que tu t'es dit, ce dont tu avais besoin, et une autre façon de voir."),
              ("4", "Choisis", "Une réponse qui te ressemble. Le dimanche, le bilan montre ce qui t'aide.")]
    y += 40
    for n, t, txt in etapes:
        cadre(d, M, y, W - M, y + 230, fond=SAUGE_C)
        d.ellipse((M + 40, y + 50, M + 160, y + 170), fill=ROSE)
        centre(d, y + 62, n, TITRE(76), CREME, M + 40, M + 160)
        d.text((M + 210, y + 40), t, font=GRAS(50), fill=BRUN)
        paragraphe(d, M + 210, y + 110, txt, TEXTE(38), W - 2 * M - 250)
        y += 260
    y += 20
    cadre(d, M, y, W - M, y + 250, fond=ROSE_C, contour=ROSE_C)
    paragraphe(d, M + 50, y + 40, "Ce journal est un outil personnel, pas un soin. Si une émotion déborde souvent, si une "
               "tristesse ou une inquiétude ne te quitte plus, parles-en à ton médecin ou à un psychologue. En cas d'idées "
               "noires : 3114, gratuit, 24 h/24.", TEXTE(36), W - 2 * M - 100)
    paragraphe(d, M, y + 300, "Pour l'imprimer : A4, « taille réelle » (100 %), recto seul. Imprime les fiches émotion "
               "autant de fois que tu veux.", TEXTE(34), W - 2 * M, fill=(130, 116, 104))
    return img


def pourquoi(num):
    img, d = page()
    y = entete(d, "ce que disent les recherches", "Pourquoi ça marche", num)
    blocs = [
        ("Mettre un mot apaise", "En 2007, une équipe de l'Université de Californie à Los Angeles (Lieberman et al., "
         "Psychological Science) a observé que nommer l'émotion ressentie devant des images négatives diminuait la réaction "
         "de l'amygdale, une zone du cerveau qui réagit à ce qui inquiète. D'où la palette de mots."),
        ("Changer de point de vue aide", "En 2012, une équipe de l'Université de Sheffield (Webb et al., Psychological "
         "Bulletin) a regroupé 306 comparaisons issues d'expériences : changer sa façon de voir la situation faisait partie "
         "des stratégies qui marchaient le mieux. D'où la case « une autre façon de voir »."),
        ("Ruminer n'aide pas", "Une méta-analyse de l'Université Yale (Aldao et al., Clinical Psychology Review, 2010) a "
         "regroupé 114 études : la rumination était la stratégie la plus liée à l'anxiété et à la dépression. On écrit une "
         "fois, puis on choisit quoi faire."),
        ("Le sommeil compte", "En 2021, l'Université du Nebraska (Tomaso et al., Sleep) a regroupé 64 études : le manque de "
         "sommeil augmente l'humeur négative. D'où la case sommeil du bilan."),
    ]
    for t, txt in blocs:
        d.text((M, y), t, font=GRAS(48), fill=BRUN)
        y = paragraphe(d, M, y + 70, txt, TEXTE(36), W - 2 * M, inter=1.4) + 40
    assert y < H - 300, y
    cadre(d, M, y, W - M, y + 150, fond=SAUGE_C, contour=SAUGE_C)
    centre(d, y + 42, "Pas de bonne ou de mauvaise émotion. Juste des signaux.", MAIN(52), ROSE)
    assert y + 150 < H - 130
    return img


def palette(num):
    img, d = page(onglet="outils")
    y = entete(d, "pour trouver le mot juste", "La palette des émotions", num, LAVANDE)
    y = paragraphe(d, M, y, "Plus le mot est précis, plus il est facile de savoir quoi faire. Pars de la famille, puis "
                   "cherche la nuance.", TEXTE(36), W - 2 * M - 60) + 20
    g = 34; lw = (W - 2 * M - 60 - g) / 2; lh = (H - 200 - y - 2 * g) / 3
    for k, (nom, fort, clair, mots) in enumerate(FAMILLES):
        x0 = M + (k % 2) * (lw + g); y0 = y + (k // 2) * (lh + g)
        cadre(d, x0, y0, x0 + lw, y0 + lh, fond=clair, contour=clair)
        d.ellipse((x0 + 34, y0 + 38, x0 + 78, y0 + 82), fill=fort)
        d.text((x0 + 100, y0 + 28), nom, font=GRAS(48), fill=BRUN)
        for i, m in enumerate(mots):
            xx = x0 + 40 + (i % 2) * (lw / 2 - 14); yy = y0 + 135 + (i // 2) * 96
            assert d.textlength(m, font=TEXTE(39)) < lw / 2 - 30, m
            d.text((xx, yy), m, font=TEXTE(39), fill=TXT)
        assert y0 + 135 + 3 * 96 + 60 < y0 + lh, (nom, lh)
    return img


def carte_corps(num):
    img, d = page(onglet="outils")
    y = entete(d, "où je la sens", "La carte du corps", num, LAVANDE)
    y = paragraphe(d, M, y, "Une émotion se sent aussi dans le corps. Colorie les zones où tu la sens, et coche ce que "
                   "tu remarques.", TEXTE(36), W - 2 * M - 60) + 30
    # silhouette au trait
    cx, top = M + 330, y + 40
    c, w = BRUN, 5
    d.ellipse((cx - 85, top, cx + 85, top + 190), outline=c, width=w)
    d.line((cx - 40, top + 185, cx - 40, top + 240), fill=c, width=w); d.line((cx + 40, top + 185, cx + 40, top + 240), fill=c, width=w)
    d.rounded_rectangle((cx - 190, top + 240, cx + 190, top + 820), 90, outline=c, width=w)
    for s in (-1, 1):
        d.line([(cx + s * 190, top + 300), (cx + s * 270, top + 600), (cx + s * 285, top + 860)], fill=c, width=w, joint="curve")
        d.line([(cx + s * 170, top + 380), (cx + s * 215, top + 640), (cx + s * 225, top + 860)], fill=c, width=w, joint="curve")
        d.line([(cx + s * 30, top + 820), (cx + s * 50, top + 1450)], fill=c, width=w)
        d.line([(cx + s * 175, top + 780), (cx + s * 150, top + 1450)], fill=c, width=w)
        d.line([(cx + s * 50, top + 1450), (cx + s * 150, top + 1450)], fill=c, width=w)
    for yy in (top + 450, top + 640):  # repères poitrine / ventre en pointillés
        for x in range(int(cx - 170), int(cx + 170), 28):
            d.line((x, yy, x + 14, yy), fill=TRAIT, width=3)
    # sensations à cocher
    sens = ["Mâchoire serrée", "Gorge nouée", "Chaleur au visage", "Cœur qui s'accélère", "Souffle court",
            "Épaules lourdes", "Ventre noué", "Mains moites", "Jambes molles", "Fatigue soudaine", "Tête qui tourne vite",
            "Corps détendu", "Autre :"]
    x0 = M + 720; yy = y + 30
    for s in sens:
        d.rounded_rectangle((x0, yy + 8, x0 + 40, yy + 48), 8, outline=LAVANDE, width=3)
        assert d.textlength(s, font=TEXTE(38)) < W - M - 60 - x0 - 70, s
        d.text((x0 + 62, yy), s, font=TEXTE(38), fill=TXT)
        if s == "Autre :":
            d.line((x0 + 200, yy + 46, W - M - 60, yy + 46), fill=TRAIT, width=2)
        yy += 104
    assert yy < H - 200 and top + 1450 < H - 200
    return img


BESOINS = ["repos", "calme", "respect", "sécurité", "lien", "reconnaissance", "temps", "aide"]


def fiche(s, num, ex=None):
    """Fiche émotion : le cœur du journal. ex : dictionnaire de l'exemple rempli."""
    img, d = page(onglet=s)
    fort = ACC[s][0]
    y = entete(d, "exemple rempli" if ex else f"semaine {s} · fiche émotion", "Quand une émotion monte", num, fort)
    ex = ex or {}
    L = W - M - 60
    def ligne_titre(y, t, cle=None, n=1, pas=74):
        d.text((M, y), t, font=GRAS(40), fill=BRUN)
        yl = y + 52
        for i in range(n):
            d.line((M, yl + pas * (i + 1) - 10, L, yl + pas * (i + 1) - 10), fill=TRAIT, width=2)
            if cle and i < len(ex.get(cle, [])):
                ecrire(d, M + 20, yl + pas * (i + 1) - 8, ex[cle][i], L - M - 40)
        return yl + pas * n + 24
    def echelle(y, t, cle):
        d.text((M, y), t, font=GRAS(38), fill=BRUN)
        x = M + d.textlength(t, font=GRAS(38)) + 40
        pas = (L - x) / 11
        for i in range(11):
            cx = x + i * pas + pas / 2
            plein = ex.get(cle) == i
            d.ellipse((cx - 24, y + 4, cx + 24, y + 52), outline=fort, width=3, fill=fort if plein else None)
            centre(d, y + 8, str(i), TEXTE(28), CREME if plein else TXT, cx - 24, cx + 24)
        return y + 92
    y = ligne_titre(y, "Quand :", "quand", 1)
    y = ligne_titre(y, "Ce qui s'est passé (les faits, comme une caméra) :", "faits", 3)
    d.text((M, y), "Le mot juste :", font=GRAS(38), fill=BRUN)
    xm = M + d.textlength("Le mot juste :", font=GRAS(38)) + 20
    d.line((xm, y + 46, L, y + 46), fill=TRAIT, width=2)
    if "mot" in ex:
        ecrire(d, xm + 10, y + 48, ex["mot"], L - xm - 20)
    y += 96
    y = echelle(y, "Intensité :", "avant")
    y = ligne_titre(y, "Où je le sens dans mon corps :", "corps", 1)
    y = ligne_titre(y, "Ce que je me suis dit :", "pensee", 2)
    d.text((M, y), "Ce dont j'avais besoin :", font=GRAS(38), fill=BRUN)
    y += 62; x = M
    for b in BESOINS:
        w = d.textlength(b, font=TEXTE(34)) + 80
        if x + w > L:
            x = M; y += 62
        coche = b in ex.get("besoins", [])
        d.rounded_rectangle((x, y + 6, x + 34, y + 40), 7, outline=fort, width=3, fill=fort if coche else None)
        d.text((x + 46, y), b, font=TEXTE(34), fill=TXT); x += w + 20
    y += 92
    y = ligne_titre(y, "Une autre façon de voir la situation :", "autre", 2)
    y = ligne_titre(y, "Ce que je choisis de faire :", "choix", 2)
    y = echelle(y, "Intensité après :", "apres")
    assert y < H - 150, ("fiche trop haute", y)
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
    y = entete(d, "un coup d'œil sur le mois", "Mon mois en couleurs", num, LAVANDE)
    y = paragraphe(d, M + 6, y, "Chaque soir, colorie le rond avec la couleur de l'émotion qui a dominé ta journée. Au bout "
                   "du mois, ce qui revient saute aux yeux.", TEXTE(36), W - 2 * M - 60) + 20
    # légende
    x = M
    for k, (nom, fort, _, _) in enumerate(FAMILLES):
        if k == 3:
            x = M; y += 62
        d.ellipse((x, y + 6, x + 36, y + 42), fill=fort)
        d.text((x + 50, y), nom, font=TEXTE(34), fill=TXT); x += 450
    y += 90
    L = W - M - 60; cw = (L - M) / 7; rh = (H - 330 - (y + 60)) / 4
    for j, jour in enumerate(["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]):
        centre(d, y, jour, GRAS(34), BRUN, M + j * cw, M + (j + 1) * cw)
    y += 60
    for s in range(4):
        fort, clair = ACC[s + 1]
        for j in range(7):
            x0 = M + j * cw; y0 = y + s * rh
            cadre(d, x0 + 8, y0 + 8, x0 + cw - 8, y0 + rh - 16, fond=clair if j % 2 == 0 else CREME, contour=clair, r=20)
            d.text((x0 + 24, y0 + 18), str(s * 7 + j + 1), font=GRAS(30), fill=fort)
            cx = x0 + cw / 2
            cy = y0 + rh * 0.45
            d.ellipse((cx - 56, cy - 56, cx + 56, cy + 56), outline=TRAIT, width=3)
            for i in range(3):  # sommeil : 3 petits ronds (bien / moyen / difficile)
                xx = x0 + cw / 2 - 52 + i * 38
                d.ellipse((xx, y0 + rh - 70, xx + 26, y0 + rh - 44), outline=GRIS, width=2)
    y += 4 * rh + 10
    paragraphe(d, M, y, "Les trois petits ronds : ton sommeil de la nuit d'avant. Colorie-en un (bien), deux "
               "(moyen) ou trois (difficile).", TEXTE(32), W - 2 * M - 60, fill=(130, 116, 104))
    assert y + 120 < H - 130, y
    return img


def ouverture(s, num):
    img, d = page(onglet=s)
    fort, clair = ACC[s]
    d.rounded_rectangle((M, 300, W - M - 60, 1150), 40, fill=clair)
    cx = (M + W - M - 60) / 2
    brin(d, cx - 520, 1110, 330, 1, (fort, SAUGE))
    brin(d, cx + 520, 1110, 300, -1, (SAUGE, fort))
    centre_esp(d, 420, "SEMAINE", GRAS(40), fort, M, W - M - 60)
    centre(d, 480, str(s), TITRE(300), BRUN, M, W - M - 60)
    centre(d, 870, ["Remarquer, sans juger.", "Un mot à la fois.", "Écouter ce dont j'ai besoin.",
                    "Garder ce qui m'aide."][s - 1], MAIN(66), fort, M, W - M - 60)
    y = 1260
    for q in ("Ce que je veux observer cette semaine :", "Une situation qui me fait souvent réagir :",
              "Ce que je m'autorise à ressentir :"):
        d.text((M, y), q, font=GRAS(40), fill=BRUN)
        lignes_ecriture(d, M, y + 40, W - M - 60, y + 250, pas=70)
        y += 290
    pied(d, num)
    return img


def bilan(s, num):
    img, d = page(onglet=s)
    fort = ACC[s][0]
    y = entete(d, f"semaine {s} · bilan", "Bilan de la semaine", num, fort)
    qs = ["L'émotion qui est revenue le plus souvent :", "Ce qui l'a déclenchée (moments, situations) :",
          "Ce qui m'a aidé(e) à redescendre :", "Un moment agréable que je veux garder :",
          "La semaine prochaine, j'essaie :"]
    lh = (H - 200 - y - 150) / len(qs)
    for k, q in enumerate(qs):
        y0 = y + k * lh
        d.text((M, y0 + 10), q, font=GRAS(40), fill=BRUN)
        lignes_ecriture(d, M, y0 + 60, W - M - 60, y0 + lh - 20, pas=70)
    y0 = y + len(qs) * lh + 10
    d.text((M, y0), "Mon sommeil cette semaine :", font=GRAS(40), fill=BRUN)
    x = M + d.textlength("Mon sommeil cette semaine :", font=GRAS(40)) + 40
    for lib in ("bien", "moyen", "difficile"):
        d.rounded_rectangle((x, y0 + 8, x + 38, y0 + 46), 8, outline=fort, width=3)
        d.text((x + 52, y0 + 2), lib, font=TEXTE(38), fill=TXT); x += 80 + d.textlength(lib, font=TEXTE(38))
    assert x < W - M - 60, x
    centre(d, y0 + 80, "Une nuit trop courte, et tout paraît plus lourd.", MAIN(42), ROSE, M, W - M - 60)
    return img


def boite_outils(num):
    img, d = page(onglet="outils")
    y = entete(d, "des pistes à tester", "Ma boîte à outils", num, LAVANDE)
    y = paragraphe(d, M, y, "Coche ce que tu as essayé, puis ce qui t'aide vraiment. Tout ne marche pas pour tout le "
                   "monde : garde ce qui te ressemble.", TEXTE(36), W - 2 * M - 60) + 20
    L = W - M - 60
    centre(d, y, "essayé", GRAS(30), BRUN, L - 330, L - 170); centre(d, y, "ça m'aide", GRAS(30), BRUN, L - 170, L)
    y += 60
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
        if k % 2 == 0:
            d.rounded_rectangle((M - 10, y0, L + 10, y0 + rh - 10), 16, fill=LAVANDE_C)
        d.text((M + 10, y0 + 14), t, font=GRAS(38), fill=BRUN)
        assert d.textlength(st, font=TEXTE(32)) < L - 350 - M, st
        d.text((M + 10, y0 + 72), st, font=TEXTE(32), fill=TXT)
        for x in (L - 250, L - 85):
            d.rounded_rectangle((x - 20, y0 + 50, x + 20, y0 + 90), 8, outline=LAVANDE, width=3)
    y = y + len(outils) * rh + 20
    cadre(d, M, y, L, y + 230, fond=ROSE_C, contour=ROSE_C)
    d.text((M + 40, y + 26), "Ce qui ne m'aide pas, et que je repère :", font=GRAS(38), fill=BRUN)
    paragraphe(d, M + 40, y + 90, "ruminer en boucle, éviter tout ce qui dérange, tout garder pour moi. Les recherches les "
               "associent à plus de mal-être (Aldao et al., Université Yale, 2010).", TEXTE(32), L - M - 80)
    assert y + 230 < H - 130, y
    return img


def reperes(num):
    img, d = page(onglet="outils")
    y = entete(d, "à la fin du mois", "Mes repères", num, LAVANDE)
    qs = ["Les émotions que je ressens le plus souvent :", "Mes déclencheurs (moments, lieux, personnes) :",
          "Les signes de mon corps qui me préviennent :", "Mes besoins qui reviennent :",
          "Les outils qui m'aident le plus :", "Ce que je veux garder pour le mois prochain :"]
    lh = (H - 200 - y) / len(qs)
    for k, q in enumerate(qs):
        y0 = y + k * lh
        d.text((M, y0 + 10), q, font=GRAS(40), fill=BRUN)
        lignes_ecriture(d, M, y0 + 60, W - M - 60, y0 + lh - 20, pas=70)
    return img


def quand_en_parler(num):
    img, d = page()
    y = entete(d, "prendre soin de soi", "Quand en parler", num)
    y = paragraphe(d, M, y, "Ce journal t'aide à mieux te connaître. Il ne remplace pas un médecin ni un psychologue. "
                   "Parles-en à un professionnel si :", TEXTE(40), W - 2 * M) + 30
    for t in ("tes émotions débordent souvent ;", "tu as peur de tes propres réactions ;",
              "une tristesse ou une inquiétude ne te quitte plus ;",
              "tu évites de plus en plus de situations pour ne pas ressentir quelque chose."):
        d.ellipse((M + 10, y + 18, M + 34, y + 42), fill=ROSE)
        y = paragraphe(d, M + 60, y, t, TEXTE(40), W - 2 * M - 60) + 24
    y += 20
    y = paragraphe(d, M, y, "Tu peux consulter un psychologue directement, sans passer par ton médecin. Certaines séances "
                   "sont remboursées avec Mon soutien psy (liste sur monsoutienpsy.ameli.fr).", TEXTE(38), W - 2 * M) + 50
    cadre(d, M, y, W - M, y + 520, fond=ROSE_C, contour=ROSE_C)
    yy = y + 50
    for num_tel, lib in (("3114", "En cas d'idées noires : numéro national de prévention du suicide, gratuit, 24 h/24 et 7 j/7."),
                         ("15", "Urgence médicale : le SAMU."), ("112", "Numéro d'urgence européen, depuis n'importe quel téléphone.")):
        d.text((M + 50, yy), num_tel, font=TITRE(64), fill=ROSE)
        yy = max(yy + 110, paragraphe(d, M + 260, yy + 12, lib, TEXTE(36), W - 2 * M - 310) + 40)
    assert yy < y + 520, yy
    centre(d, y + 600, "Demander de l'aide, c'est aussi prendre soin de soi.", MAIN(50), SAUGE)
    return img


def notes(num):
    img, d = page()
    y = entete(d, "pour finir", "Notes", num)
    cadre(d, M, y, W - M, H - 200)
    lignes_ecriture(d, M + 40, y + 10, W - M - 40, H - 240)
    return img


# ------------------------------------------------------------- bonus : aide-mémoire (2 pages)
def bonus_cartes():
    img, d = page()
    y = entete(d, "à découper et à garder sur soi", "L'aide-mémoire", "bonus")
    g = 40; lw = (W - 2 * M - g) / 2; lh = (H - 230 - y - g) / 2
    cartes = [("1", "Remarque", "Qu'est-ce qui vient de se passer ? Les faits, juste les faits."),
              ("2", "Nomme", "Quel est le mot juste ? Où est-ce que je le sens ?"),
              ("3", "Comprends", "Qu'est-ce que je me dis ? De quoi ai-je besoin ?"),
              ("4", "Choisis", "Souffler 2 minutes, puis choisir une réponse qui me ressemble.")]
    for k, (n, t, txt) in enumerate(cartes):
        x0 = M + (k % 2) * (lw + g); y0 = y + (k // 2) * (lh + g)
        for x in range(int(x0), int(x0 + lw), 30):  # pointillés de découpe
            d.line((x, y0, x + 15, y0), fill=TRAIT, width=3); d.line((x, y0 + lh, x + 15, y0 + lh), fill=TRAIT, width=3)
        for yy in range(int(y0), int(y0 + lh), 30):
            d.line((x0, yy, x0, yy + 15), fill=TRAIT, width=3); d.line((x0 + lw, yy, x0 + lw, yy + 15), fill=TRAIT, width=3)
        fort = FAMILLES[[1, 2, 4, 0][k]][1]
        d.ellipse((x0 + lw / 2 - 70, y0 + 80, x0 + lw / 2 + 70, y0 + 220), fill=fort)
        centre(d, y0 + 92, n, TITRE(90), CREME, x0, x0 + lw)
        centre(d, y0 + 270, t, TITRE(70), BRUN, x0, x0 + lw)
        yy = y0 + 400
        for li in lignes(d, txt, TEXTE(40), lw - 120):
            centre(d, yy, li, TEXTE(40), TXT, x0, x0 + lw); yy += 58
        assert yy < y0 + lh - 30
    return img


def bonus_palette():
    img, d = page()
    y = entete(d, "à garder dans son sac ou son agenda", "La palette de poche", "bonus")
    # deux exemplaires A5 (moitié haute / moitié basse) : 6 familles en 3 × 2
    for e in range(2):
        y0 = y + e * (H - 230 - y) / 2 + (20 if e else 0)
        hh = (H - 230 - y) / 2 - 40
        lw = (W - 2 * M - 2 * 24) / 3; lh = (hh - 24) / 2
        for k, (nom, fort, clair, mots) in enumerate(FAMILLES):
            x0 = M + (k % 3) * (lw + 24); yy = y0 + (k // 3) * (lh + 24)
            cadre(d, x0, yy, x0 + lw, yy + lh, fond=clair, contour=clair, r=20)
            d.ellipse((x0 + 22, yy + 26, x0 + 52, yy + 56), fill=fort)
            d.text((x0 + 66, yy + 16), nom, font=GRAS(36), fill=BRUN)
            for i, m in enumerate(mots):
                assert d.textlength(m, font=TEXTE(29)) < lw - 50, m
                d.text((x0 + 26, yy + 80 + i * 39), m, font=TEXTE(29), fill=TXT)
            assert yy + 80 + 8 * 39 < yy + lh + 5, (nom, lh)
        if e == 0:
            ym = y0 + hh + 20
            for x in range(M, W - M, 30):
                d.line((x, ym, x + 15, ym), fill=TRAIT, width=3)
    return img


# ------------------------------------------------------------- impression, tablette, assemblage
ECHELLE, DX = P.ECHELLE, P.DX
DY = (H - round(H * ECHELLE)) // 2


def fond_page(couv=False):
    return fond_couverture(couv == "fonce") if couv else texture()


def mise_en_page_impression(img, couv=False):
    petit = img.resize((round(W * ECHELLE), round(H * ECHELLE)), Image.LANCZOS)
    masque = Image.new("L", petit.size, 0)
    ImageDraw.Draw(masque).rectangle((22, 22, petit.width - 22, petit.height - 22), fill=255)
    masque = masque.filter(ImageFilter.GaussianBlur(14))
    fond = fond_page(couv); fond.paste(petit, (DX, DY), masque)
    return fond


def controle_marges(img, couv=False):
    import numpy as np
    a = np.asarray(img, np.int16); b = np.asarray(fond_page(couv), np.int16)
    ecart = np.abs(a - b).max(axis=2)
    zones = {"gauche": ecart[:, :P.ZONE_TROUS], "droite": ecart[:, W - P.ZONE_IMPRIMANTE:],
             "haut": ecart[:P.ZONE_IMPRIMANTE, :], "bas": ecart[H - P.ZONE_IMPRIMANTE:, :]}
    return {k: int((z > 40).sum()) for k, z in zones.items()}


# (libellé, index de page dans le journal imprimable, section) ; +1 dans la version tablette
SOMMAIRE = [("Mode d'emploi", 1, None), ("Pourquoi ça marche", 2, None), ("La palette des émotions", 3, "outils"),
            ("La carte du corps", 4, "outils"), ("Exemple rempli", 5, 0), ("Mon mois en couleurs", 6, "outils"),
            ("Semaine 1", 7, 1), ("Semaine 2", 12, 2), ("Semaine 3", 17, 3), ("Semaine 4", 22, 4),
            ("Ma boîte à outils", 27, "outils"), ("Mes repères", 28, "outils"), ("Quand en parler", 29, None), ("Notes", 30, None)]
DEBUT_SECTION = {0: 5, 1: 7, 2: 12, 3: 17, 4: 22, "outils": 3}
SANS_ONGLET = {0, 1, 2, 29, 30}


def sommaire():
    img, d = page()
    y = entete(d, "pour s'y retrouver", "Sommaire", "sommaire")
    y = paragraphe(d, M, y, "Touche une ligne pour y aller. Les onglets du bord renvoient au début de chaque partie, et "
                   "le bas de chaque page ramène ici.", TEXTE(36), W - 2 * M) + 30
    rects = []
    for lib, cible, coul in SOMMAIRE:
        d.rounded_rectangle((M, y, W - M, y + 96), 22, fill=ACC[coul][1] if coul is not None else CREME, outline=TRAIT, width=2)
        d.text((M + 40, y + 22), lib, font=GRAS(40), fill=BRUN)
        n = str(cible + 1)
        d.text((W - M - 40 - d.textlength(n, font=TEXTE(38)), y + 24), n, font=TEXTE(38), fill=TXT)
        rects.append(((M, y, W - M, y + 96), cible)); y += 110
    assert y < H - 200, y
    return img, rects


def version_tablette(pages_brutes):
    som, rects = sommaire()
    pages = [pages_brutes[0], som] + pages_brutes[1:]
    chemin = os.path.join(SORTIE, f"{NOM}-tablette.pdf")
    pages[0].save(chemin, "PDF", resolution=200, save_all=True, append_images=pages[1:])
    liens = [(1, rect, cible + 1) for rect, cible in rects]
    for k in range(2, len(pages)):
        liens.append((k, (W / 2 - 420, H - 110, W / 2 + 420, H - 45), 1))
        if k - 1 not in SANS_ONGLET:
            for i, (cle, _) in enumerate(ONGLETS):
                y0 = 330 + i * 168
                liens.append((k, (W - 75, y0, W, y0 + 150), DEBUT_SECTION[cle] + 1))
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
    # cohérence du sommaire avec l'ordre réel des pages
    assert [SOMMAIRE[k][1] for k in range(len(SOMMAIRE))] == [1, 2, 3, 4, 5, 6, 7, 12, 17, 22, 27, 28, 29, 30]
    print("tablette :", version_tablette(pages))
    imp = [mise_en_page_impression(p, couv="fonce" if k == 0 else False) for k, p in enumerate(pages)]
    for k, p in enumerate(imp):
        m = controle_marges(p, couv="fonce" if k == 0 else False)
        assert all(v == 0 for v in m.values()), (k + 1, m)
    imp[0].save(os.path.join(SORTIE, f"{NOM}-A4.pdf"), "PDF", resolution=200, save_all=True, append_images=imp[1:])
    nb = [encre_econome(p) for p in [mise_en_page_impression(couverture(False), couv="clair")] + imp[1:]]
    nb[0].save(os.path.join(SORTIE, f"{NOM}-A4-econome-encre.pdf"), "PDF", resolution=200, save_all=True, append_images=nb[1:])
    bonus = [mise_en_page_impression(p) for p in (bonus_cartes(), bonus_palette())]
    for p in bonus:
        assert all(v == 0 for v in controle_marges(p).values())
    bonus[0].save(os.path.join(SORTIE, "aide-memoire-emotions-A4.pdf"), "PDF", resolution=200, save_all=True, append_images=bonus[1:])
    for k, p in enumerate(imp):
        p.resize((W // 2, H // 2), Image.LANCZOS).save(os.path.join(SORTIE, f"apercu-{k + 1:02d}.jpg"), quality=85)
    for k, p in enumerate(bonus):
        p.resize((W // 2, H // 2), Image.LANCZOS).save(os.path.join(SORTIE, f"apercu-bonus-{k + 1}.jpg"), quality=85)
    return len(imp)


if __name__ == "__main__":
    print(fabriquer())
