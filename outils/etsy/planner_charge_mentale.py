"""Produit Etsy n° 1 (31/10/2026) : planner « Alléger sa charge mentale », 4 semaines, A4 à imprimer.
Version 2 (même jour, pour se démarquer) : volet à deux (qui pense, organise, fait), semaine d'exemple remplie,
page « Pourquoi ça marche » sourcée, version économe en encre.
Texte dessiné par PIL (polices OFL de polices/), pages A4 à 200 dpi, PDF multipage + aperçus pour la fiche Etsy.
Appel : python3 outils/etsy/planner_charge_mentale.py  : etsy/planner-charge-mentale/"""
import os
from PIL import Image, ImageDraw, ImageFont

POL = os.path.join(os.path.dirname(__file__), "..", "..", "polices") + "/"
SORTIE = os.path.join(os.path.dirname(__file__), "..", "..", "etsy", "planner-charge-mentale")
W, H = 1654, 2339  # A4, 200 dpi
NB_PAGES = 27
M = 130  # marge
CREME = (250, 245, 236); SAUGE = (124, 146, 118); SAUGE_C = (226, 233, 221); ROSE = (196, 120, 116)
ROSE_C = (244, 226, 220); BRUN = (74, 52, 36); TXT = (70, 62, 54); TRAIT = (205, 194, 178); OR = (176, 128, 52)
ENCRE = (38, 62, 112)  # « stylo » des pages d'exemple
f = lambda n, t: ImageFont.truetype(POL + n, t)
TITRE = lambda t: f("PlayfairDisplay-Bold.ttf", t)
MAIN = lambda t: f("DancingScript-Bold.ttf", t)
TEXTE = lambda t: f("Lora-Regular.ttf", t)
GRAS = lambda t: f("Lora-SemiBold.ttf", t)


def page():
    img = Image.new("RGB", (W, H), CREME)
    return img, ImageDraw.Draw(img)


def lignes(d, t, fo, l):
    # espace insécable avant « ? : ! » : jamais de ponctuation seule en début de ligne
    t = t.replace(" ?", "\u00a0?").replace(" :", "\u00a0:").replace(" !", "\u00a0!")
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


def centre(d, y, t, fo, fill, x0=0, x1=W):
    w = d.textlength(t, font=fo)
    assert w <= x1 - x0, ("trop large", t)
    d.text((x0 + (x1 - x0 - w) / 2, y), t, font=fo, fill=fill)


def entete(d, sur_titre, titre, num):
    centre(d, M - 20, sur_titre, MAIN(56), ROSE)
    centre(d, M + 60, titre, TITRE(84), BRUN)
    d.line((W / 2 - 120, M + 175, W / 2 + 120, M + 175), fill=OR, width=4)
    pied(d, num)
    return M + 230


def pied(d, num):
    centre(d, H - 95, f"Alléger sa charge mentale  ·  {num}", TEXTE(26), (150, 138, 124))


def lignes_ecriture(d, x0, y0, x1, y1, pas=78):
    y = y0 + pas
    while y <= y1:
        d.line((x0, y, x1, y), fill=TRAIT, width=2); y += pas


def cadre(d, x0, y0, x1, y1, fond=None, contour=TRAIT, r=28):
    d.rounded_rectangle((x0, y0, x1, y1), r, fill=fond, outline=contour, width=3)


def paragraphe(d, x, y, t, fo, l, fill=TXT, inter=1.45):
    for li in lignes(d, t, fo, l):
        d.text((x, y), li, font=fo, fill=fill); y += int(fo.size * inter)
    return y


def couverture():
    img, d = page()
    d.rectangle((0, 0, W, H), fill=SAUGE_C)
    cadre(d, 110, 110, W - 110, H - 110, fond=CREME, contour=OR, r=40)
    d.rounded_rectangle((140, 140, W - 140, H - 140), 30, outline=OR, width=2)
    # brins de feuilles dessinés (formes simples, pas d'image générée)
    for cx, cy, s in ((330, 520, 1), (W - 330, 520, -1)):
        d.line((cx, cy - 170, cx, cy + 170), fill=SAUGE, width=6)
        for k in range(-3, 4):
            y = cy + k * 48
            d.ellipse((cx + (8 if s > 0 else -78), y - 18, cx + (78 if s > 0 else -8), y + 18), fill=SAUGE)
            d.ellipse((cx - (78 if s > 0 else -8), y - 4, cx - (8 if s > 0 else -78), y + 32), fill=(150, 170, 142))
    centre(d, 760, "Planner de 4 semaines", MAIN(92), ROSE)
    centre(d, 930, "ALLÉGER SA", TITRE(128), BRUN)
    centre(d, 1090, "CHARGE MENTALE", TITRE(128), BRUN)
    d.line((W / 2 - 200, 1300, W / 2 + 200, 1300), fill=OR, width=5)
    y = 1380
    for t in ("Vider sa tête, trier, déléguer,", "et retrouver un peu d'air", "dans sa semaine."):
        centre(d, y, t, TEXTE(58), TXT); y += 84
    centre(d, 1800, "avec un volet à deux et une semaine d'exemple", MAIN(54), ROSE)
    centre(d, 1910, "À imprimer · format A4 · 27 pages", GRAS(42), SAUGE)
    centre(d, 1980, "Clarté Mentale | Stress & Énergie", TEXTE(38), (140, 126, 110))
    return img


def mode_emploi():
    img, d = page()
    y = entete(d, "avant de commencer", "Mode d'emploi", 2)
    fo = TEXTE(40)
    y = paragraphe(d, M, y + 20, "La charge mentale, c'est le travail invisible qui consiste à penser à tout : anticiper, "
                   "organiser, se souvenir, vérifier. Ce planner t'aide à la sortir de ta tête et à la poser sur le "
                   "papier, une semaine à la fois.", fo, W - 2 * M)
    etapes = [("1", "Vide ta tête", "En début de semaine, note tout ce qui te trotte dans la tête, sans trier."),
              ("2", "Trie", "Range chaque élément : je m'en occupe, je délègue, plus tard, je lâche."),
              ("3", "Planifie léger", "Trois priorités par jour, pas plus, et une chose rien que pour toi."),
              ("4", "Fais le bilan", "Le dimanche, cinq minutes pour voir ce qui a allégé ta semaine.")]
    y += 50
    for n, t, txt in etapes:
        cadre(d, M, y, W - M, y + 230, fond=SAUGE_C)
        d.ellipse((M + 40, y + 50, M + 160, y + 170), fill=ROSE)
        centre(d, y + 62, n, TITRE(76), CREME, M + 40, M + 160)
        d.text((M + 210, y + 40), t, font=GRAS(50), fill=BRUN)
        paragraphe(d, M + 210, y + 110, txt, TEXTE(38), W - 2 * M - 250)
        y += 270
    y += 30
    cadre(d, M, y, W - M, y + 250, fond=ROSE_C, contour=ROSE_C)
    paragraphe(d, M + 50, y + 40, "Ce planner est un outil d'organisation personnelle, pas un soin. Si tu te sens "
               "épuisé(e) depuis des semaines, si tu dors mal ou si tout te paraît trop lourd, parles-en à ton "
               "médecin. En cas d'idées noires : 3114, gratuit, 24 h/24.", TEXTE(36), W - 2 * M - 100)
    return img


def ecrire(d, x, y_ligne, t, l):
    """Texte « à la main » posé sur une ligne d'écriture."""
    fo = MAIN(40)
    assert d.textlength(t, font=fo) <= l, ("exemple trop long", t)
    d.text((x, y_ligne - 50), t, font=fo, fill=ENCRE)


def vide_tete(s, num, ex=None):
    img, d = page()
    y = entete(d, "exemple rempli" if ex else f"semaine {s}", "Vide-tête", num)
    y = paragraphe(d, M, y, "Tout ce qui tourne dans ta tête : tâches, rendez-vous, soucis, choses à ne pas oublier. "
                   "Sans trier, sans juger.", TEXTE(38), W - 2 * M) + 30
    cadre(d, M, y, W - M, H - 200)
    lignes_ecriture(d, M + 40, y + 10, W - M - 40, H - 240)
    for k, t in enumerate(ex or []):
        ecrire(d, M + 60, y + 10 + 78 * (k + 1), t, W - 2 * M - 120)
    return img


def tri(s, num, ex=None):
    img, d = page()
    y = entete(d, "exemple rempli" if ex else f"semaine {s}", "Le tri", num)
    cases = [("Je m'en occupe", "cette semaine", SAUGE_C), ("Je délègue", "à qui ?", ROSE_C),
             ("Plus tard", "pas cette semaine", ROSE_C), ("Je lâche", "ce n'est pas si important", SAUGE_C)]
    g = 40; lw = (W - 2 * M - g) / 2; lh = (H - 200 - y - g) / 2
    for k, (t, st, fond) in enumerate(cases):
        x0 = M + (k % 2) * (lw + g); y0 = y + (k // 2) * (lh + g)
        cadre(d, x0, y0, x0 + lw, y0 + lh, fond=fond, contour=fond)
        centre(d, y0 + 35, t, GRAS(50), BRUN, x0, x0 + lw)
        centre(d, y0 + 105, st, MAIN(44), ROSE, x0, x0 + lw)
        lignes_ecriture(d, x0 + 40, y0 + 170, x0 + lw - 40, y0 + lh - 30, pas=74)
        for i, t in enumerate((ex or [[]] * 4)[k]):
            ecrire(d, x0 + 50, y0 + 170 + 74 * (i + 1), t, lw - 100)
    return img


def semaine(s, num, ex=None):
    img, d = page()
    y = entete(d, "exemple rempli" if ex else f"semaine {s}", "Ma semaine", num)
    jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    g = 26; lw = (W - 2 * M - g) / 2; lh = (H - 200 - y - 3 * g) / 4
    for k, j in enumerate(jours):
        x0 = M + (k % 2) * (lw + g); y0 = y + (k // 2) * (lh + g)
        cadre(d, x0, y0, x0 + lw, y0 + lh)
        d.text((x0 + 30, y0 + 22), j, font=GRAS(44), fill=BRUN)
        yy = y0 + 95
        jx = (ex or {}).get(j, [])
        for i in range(3):
            d.rounded_rectangle((x0 + 30, yy + 8, x0 + 62, yy + 40), 6, outline=SAUGE, width=3)
            d.line((x0 + 80, yy + 40, x0 + lw - 30, yy + 40), fill=TRAIT, width=2)
            if i < len(jx) - 1:
                ecrire(d, x0 + 85, yy + 42, jx[i], lw - 120)
            yy += 66
        d.text((x0 + 30, yy + 4), "Pour moi :", font=MAIN(38), fill=ROSE)
        d.line((x0 + 200, yy + 44, x0 + lw - 30, yy + 44), fill=TRAIT, width=2)
        if jx:
            ecrire(d, x0 + 210, yy + 46, jx[-1], lw - 245)
    x0 = M + lw + g; y0 = y + 3 * (lh + g)
    cadre(d, x0, y0, x0 + lw, y0 + lh, fond=SAUGE_C, contour=SAUGE_C)
    centre(d, y0 + 40, "Trois priorités par jour,", GRAS(40), BRUN, x0, x0 + lw)
    centre(d, y0 + 100, "pas plus.", GRAS(40), BRUN, x0, x0 + lw)
    centre(d, y0 + 190, "Le reste peut attendre.", MAIN(48), ROSE, x0, x0 + lw)
    return img


def bilan(s, num):
    img, d = page()
    y = entete(d, f"semaine {s}", "Bilan du dimanche", num)
    qs = ["Ce que j'ai réussi à lâcher cette semaine :", "Ce que j'ai délégué (et comment ça s'est passé) :",
          "Le moment où je me suis senti(e) le plus léger(e) :", "Ce qui m'a pesé le plus :",
          "Une chose que je veux faire autrement la semaine prochaine :"]
    lh = (H - 200 - y) / len(qs)
    for k, q in enumerate(qs):
        y0 = y + k * lh
        d.text((M, y0 + 10), q, font=GRAS(40), fill=BRUN)
        lignes_ecriture(d, M, y0 + 60, W - M, y0 + lh - 20, pas=70)
    return img


def taches_invisibles(num):
    img, d = page()
    y = entete(d, "pour repérer", "Les tâches invisibles", num)
    y = paragraphe(d, M, y, "Coche celles que tu portes souvent seul(e). Les voir écrites aide à en parler, et à "
                   "en déléguer une partie.", TEXTE(38), W - 2 * M) + 30
    items = ["Penser aux rendez-vous médicaux", "Prévoir les repas de la semaine", "Remarquer ce qui manque à la maison",
             "Se souvenir des anniversaires", "Suivre les papiers et factures", "Organiser les vacances",
             "Gérer les imprévus des enfants", "Prévoir les cadeaux", "Penser aux réparations à faire",
             "Rappeler aux autres ce qu'ils oublient", "Préparer les sacs, les affaires, les tenues",
             "Garder le lien avec la famille", "Anticiper les fins de mois", "Tout vérifier « au cas où »"]
    lw = (W - 2 * M - 40) / 2
    for k, it in enumerate(items):
        x0 = M + (k % 2) * (lw + 40); y0 = y + (k // 2) * 175
        cadre(d, x0, y0, x0 + lw, y0 + 145, fond=SAUGE_C if (k // 2) % 2 == 0 else ROSE_C, contour=CREME)
        d.rounded_rectangle((x0 + 30, y0 + 52, x0 + 70, y0 + 92), 8, outline=BRUN, width=3)
        yy = y0 + 72 - 24 * len(lignes(d, it, TEXTE(36), lw - 130))
        paragraphe(d, x0 + 95, yy, it, TEXTE(36), lw - 130, inter=1.3)
    y0 = y + 7 * 175 + 30
    d.text((M, y0), "La tâche que je pourrais confier en premier, et à qui :", font=GRAS(40), fill=BRUN)
    lignes_ecriture(d, M, y0 + 50, W - M, H - 220, pas=74)
    return img


def notes(num):
    img, d = page()
    y = entete(d, "pour finir", "Notes", num)
    cadre(d, M, y, W - M, H - 200)
    lignes_ecriture(d, M + 40, y + 10, W - M - 40, H - 240)
    return img


def pourquoi(num):
    img, d = page()
    y = entete(d, "ce que disent les recherches", "Pourquoi ça marche", num)
    blocs = [
        ("Penser à tout, c'est un travail", "Dès 1984, la sociologue Monique Haicault a décrit ce travail invisible de "
         "gestion du quotidien : prévoir, organiser, se souvenir, en plus de faire. C'est souvent cette partie "
         "« penser » qui épuise, parce qu'elle ne s'arrête jamais. D'où les trois colonnes « penser, organiser, "
         "faire » du volet à deux."),
        ("Une tâche en suspens revient en tête", "Dans une série d'expériences publiées en 2011 (Masicampo et Baumeister, "
         "Florida State University, Journal of Personality and Social Psychology), une tâche non terminée revenait "
         "sans cesse à l'esprit des participants. Ceux qui écrivaient un plan précis pour la réaliser étaient beaucoup "
         "moins dérangés par ces pensées."),
        ("Ce que ça change pour toi", "Le vide-tête sort tout de ta tête. Le tri décide de ce qui reste à toi. Et pour "
         "chaque tâche « je m'en occupe », note quand et comment tu vas la faire : c'est ce petit plan qui laisse "
         "ta tête tranquille en attendant."),
    ]
    for t, txt in blocs:
        d.text((M, y), t, font=GRAS(50), fill=BRUN)
        y = paragraphe(d, M, y + 75, txt, TEXTE(38), W - 2 * M) + 60
    cadre(d, M, y, W - M, y + 170, fond=SAUGE_C, contour=SAUGE_C)
    centre(d, y + 50, "Pas besoin de tout faire. Juste de tout poser.", MAIN(58), ROSE)
    return img


TACHES_FOYER = ["Repas de la semaine", "Courses", "Linge", "Ménage", "Rendez-vous médicaux", "Papiers et factures",
                "Budget du mois", "École, devoirs, réunions", "Activités des enfants", "Anniversaires et cadeaux",
                "Vacances et week-ends", "Réparations, artisans", "Voiture, assurances", "Liens avec la famille",
                "Animaux", "Imprévus (malade, grève…)", "Stock de la maison", "Sorties et invitations",
                "Démarches administratives", "Tri, rangement, saisons", "Calendrier commun", "Autre :"]


def qui_fait_quoi(num, part):
    img, d = page()
    y = entete(d, "le volet à deux", "Qui fait quoi ?", num)
    if part == 1:
        y = paragraphe(d, M, y, "Pour chaque domaine, coche qui s'en charge vraiment aujourd'hui : qui y pense, qui "
                       "organise, qui fait. Remplissez-le chacun de votre côté, puis comparez.", TEXTE(36), W - 2 * M) + 20
    taches = TACHES_FOYER[:11] if part == 1 else TACHES_FOYER[11:]
    cols = ["Penser", "Organiser", "Faire"]
    xt = M; xc = M + 560; cw = (W - M - xc) / 3
    for i, c in enumerate(cols):
        centre(d, y, c, GRAS(42), BRUN, xc + i * cw, xc + (i + 1) * cw)
        centre(d, y + 58, "moi · l'autre", MAIN(34), ROSE, xc + i * cw, xc + (i + 1) * cw)
    y += 120
    rh = min(140, (H - 230 - y) / len(taches))
    for k, t in enumerate(taches):
        y0 = y + k * rh
        if k % 2 == 0:
            d.rounded_rectangle((M - 10, y0, W - M + 10, y0 + rh - 8), 16, fill=SAUGE_C)
        assert d.textlength(t, font=TEXTE(36)) < xc - xt - 30, t
        d.text((xt + 10, y0 + rh / 2 - 30), t, font=TEXTE(36), fill=TXT)
        if t == "Autre :":
            d.line((xt + 140, y0 + rh / 2 + 14, xc - 30, y0 + rh / 2 + 14), fill=TRAIT, width=2)
        for i in range(3):
            cx = xc + i * cw + cw / 2
            for dx in (-48, 22):
                d.rounded_rectangle((cx + dx, y0 + rh / 2 - 26, cx + dx + 30, y0 + rh / 2 + 4), 6, outline=SAUGE, width=3)
    return img


def rendez_vous(num):
    img, d = page()
    y = entete(d, "le volet à deux", "Le rendez-vous à deux", num)
    y = paragraphe(d, M, y, "20 minutes, une fois par mois, au calme. Le but n'est pas de compter les points, mais de "
                   "rendre visible ce qui ne l'est pas, et de choisir ensemble.", TEXTE(38), W - 2 * M) + 40
    qs = ["1. Comparez vos deux pages « Qui fait quoi ». Où vos réponses diffèrent-elles ?",
          "2. Quel domaine pèse le plus en ce moment, et pour qui ?",
          "3. Quel domaine l'autre peut-il prendre en entier : y penser, l'organiser et le faire ?",
          "4. Qu'est-ce qu'on peut faire moins bien, moins souvent, ou plus du tout ?",
          "5. Notre prochain rendez-vous : le … à … h."]
    lh = (H - 230 - y) / len(qs)
    for k, q in enumerate(qs):
        y0 = y + k * lh
        yy = paragraphe(d, M, y0, q, GRAS(38), W - 2 * M, fill=BRUN, inter=1.35)
        lignes_ecriture(d, M, yy - 20, W - M, y0 + lh - 25, pas=66)
    centre(d, H - 170, "Une tâche confiée en entier soulage plus que dix coups de main.", MAIN(44), ROSE)
    return img


EX_VIDE = ["Rendez-vous dentiste de Léo", "Racheter du liquide vaisselle", "Répondre au mot de la maîtresse",
           "Cadeau pour l'anniversaire de maman (samedi)", "Appeler le plombier : fuite sous l'évier",
           "Finir le dossier pour jeudi", "Les vêtements d'hiver sont trop petits", "Réserver les vacances de février",
           "Payer la cantine", "Et moi ? Reprendre la marche"]
EX_TRI = [["Finir le dossier pour jeudi", "Cadeau de maman", "Payer la cantine"],
          ["Plombier : Karim, en entier", "Liquide vaisselle : drive"],
          ["Vacances : dimanche 8", "Vêtements d'hiver : le 14"],
          ["Repasser les draps", "Gâteau maison : acheté"]]
EX_SEM = {"Lundi": ["Dossier : partie 1 (9 h)", "Appeler le dentiste", "10 min de marche"],
          "Mardi": ["Payer la cantine", "Dossier : partie 2", "Un épisode, sans culpabiliser"],
          "Mercredi": ["Mot de la maîtresse", "Commander le cadeau", "Appeler Sophie"],
          "Jeudi": ["Rendre le dossier", "Coucher tôt"],
          "Vendredi": ["Courses du drive", "Bain long"],
          "Samedi": ["Anniversaire de maman", "Marche au parc"],
          "Dimanche": ["Bilan + vide-tête (10 min)", "Rien de prévu, exprès"]}


def encre_econome(img):
    """Version pour imprimer en noir : niveaux de gris, aplats éclaircis (moins d'encre)."""
    g = img.convert("L").point(lambda v: int(255 - (255 - v) * 0.55) if v > 150 else v)
    return g.convert("RGB")


def fabriquer():
    os.makedirs(SORTIE, exist_ok=True)
    pages = [couverture(), mode_emploi(), pourquoi(3),
             vide_tete(0, 4, EX_VIDE), tri(0, 5, EX_TRI), semaine(0, 6, EX_SEM)]
    n = 7
    for s in range(1, 5):
        for fn in (vide_tete, tri, semaine, bilan):
            pages.append(fn(s, n)); n += 1
    pages.append(taches_invisibles(n)); n += 1
    pages.append(qui_fait_quoi(n, 1)); n += 1
    pages.append(qui_fait_quoi(n, 2)); n += 1
    pages.append(rendez_vous(n)); n += 1
    pages.append(notes(n))
    assert len(pages) == NB_PAGES, len(pages)
    pdf = os.path.join(SORTIE, "planner-alleger-charge-mentale-A4.pdf")
    pages[0].save(pdf, "PDF", resolution=200, save_all=True, append_images=pages[1:])
    nb = [encre_econome(p) for p in pages]
    nb[0].save(os.path.join(SORTIE, "planner-alleger-charge-mentale-A4-econome-encre.pdf"), "PDF", resolution=200,
               save_all=True, append_images=nb[1:])
    for k, p in enumerate(pages):
        p.resize((W // 2, H // 2), Image.LANCZOS).save(os.path.join(SORTIE, f"apercu-{k + 1:02d}.jpg"), quality=85)
    return pdf


if __name__ == "__main__":
    print(fabriquer())
