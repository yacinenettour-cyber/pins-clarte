"""Photos de la fiche Etsy du journal « Apprivoiser ses émotions » (05/11/2026), même méthode que le planner :
dessinées par programme à partir des vraies pages du PDF, aucune IA, rien de payant. 3000 × 2250 (4:3).
Usage : python3 outils/etsy/photos_fiche_journal.py → etsy/journal-emotions/fiche-XX-*.jpg"""
import glob, os, subprocess, tempfile
from PIL import Image, ImageDraw
import photos_fiche_planner as F
import journal_emotions as J
# 05/11/2026 (refonte « plus qualitative ») : même typographie que le journal (Cormorant Garamond + Jost), couleurs sourdes
F.TITRE = lambda t: J.SERIF(t, 600)
F.MAIN = lambda t: J.ITAL(t, 500)
F.TEXTE = lambda t: J.SANS(t, 350)
F.GRAS = lambda t: J.SANS(t, 500)
F.ROSE, F.SAUGE, F.LAVANDE, F.BRUME, F.BRUN, F.TXT = J.BLUSH[0], J.SAUGE[0], J.LILAS[0], J.BRUME[0], J.ENC, J.TXT
from photos_fiche_planner import (W, H, fond, coller, brin, crayon, tasse, centre, bloc, pastille, entete, bulle, loupe, fleche,
                                  tablette, stylet, largeur, TITRE, MAIN, TEXTE, GRAS, ROSE, SAUGE, BRUN, TXT, LAVANDE, BRUME,
                                  SABLE, OR)

F.DOSSIER = os.path.join(F.DEPOT, "etsy", "journal-emotions")
NOM = "journal-apprivoiser-ses-emotions"
VERT = (70, 96, 84)
FAM = [(196, 150, 70), SAUGE, BRUME, (184, 92, 64), LAVANDE, (140, 124, 112)]


def rendre_pages():
    t = tempfile.mkdtemp()
    for v, fichier in (("c", f"{NOM}-A4.pdf"), ("e", f"{NOM}-A4-econome-encre.pdf"), ("t", f"{NOM}-tablette.pdf"),
                       ("k", "aide-memoire-emotions-A4.pdf")):
        subprocess.run(["pdftoppm", "-r", "200", "-png", os.path.join(F.DOSSIER, fichier), os.path.join(t, v)], check=True)
    for p in glob.glob(os.path.join(t, "*.png")):
        b = os.path.basename(p)
        F._PAGES[(b[0], int(b.split("-")[1].split(".")[0]))] = p


page = F.page


def signature(d, y=H - 110):
    centre(d, "Clarté Mentale  ·  journal à imprimer en français", TEXTE(40), y, couleur=(150, 132, 116))


def p01_couverture():
    im = fond((236, 238, 232), vignette=0.12).convert("RGBA")
    coller(im, page(5, 700), (1180, 1040), 3, eleve=0.6)
    coller(im, page(8, 700), (1370, 1090), 9, eleve=0.7)
    coller(im, page(9, 700), (1540, 1160), 15, eleve=0.8)
    coller(im, page(1, 940), (760, 1160), -3, eleve=1.2)
    d = ImageDraw.Draw(im)
    brin(d, 120, 2080, 520, -68)
    crayon(im, 1350, 2030, 700, -12)
    d = ImageDraw.Draw(im)
    x0 = 1990
    J.esp(d, x0, 270, "JOURNAL EN FRANÇAIS", J.SANS(44, 500), VERT, pas=8)
    w = J.esp(d, x0, 360, "APPRIVOISER", J.SERIF(122, 500), BRUN, pas=6)
    assert x0 + w < W - 50, w
    d.text((x0, 520), "ses émotions", font=J.ITAL(170, 500), fill=BRUN)
    d.text((x0, 760), "pour adultes, 4 semaines", font=J.ITAL(80, 500), fill=VERT)
    d.line((x0, 900, x0 + 160, 900), fill=VERT, width=3)
    y = 990
    for t, c in (("Palette de 48 mots", J.SABLE[0]), ("Fiche émotion guidée", J.BLUSH[0]), ("Exemple déjà rempli", J.SAUGE[0]),
                 ("Version tablette cliquable", J.BRUME[0])):
        pastille(d, x0, y, t, GRAS(46), fond_c=c); y += 122
    assert largeur(d, "ses émotions", J.ITAL(170, 500)) + x0 < W - 40
    d.text((x0, y + 40), "40 pages A4  ·  3 versions", font=TEXTE(52), fill=TXT)
    d.text((x0, y + 120), "+ 3 pages bonus à découper", font=TEXTE(52), fill=TXT)
    assert largeur(d, "Version tablette cliquable", GRAS(46)) + 72 + x0 < W - 40
    return F.enregistrer(im, "fiche-01-couverture.jpg")


def p02_fiche():
    im = fond((240, 232, 226)).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "le cœur du journal", "Une fiche quand une émotion monte", "remarque, nomme, comprends, choisis")
    coller(im, page(9, 900), (1000, 1360), -3, eleve=1.0)
    p6 = page(9, 1654)
    loupe(im, p6, (110, 740, 900, 1530), (420, 1700), 270)
    d = ImageDraw.Draw(im)
    x = 1760
    y = bulle(d, x, 620, "Les faits, d'abord", "Comme une caméra : ce qui s'est passé, sans interprétation.", 1100, FAM[2])
    y = bulle(d, x, y + 40, "Le mot juste + l'intensité", "De 0 à 10, avant et après : tu vois ce qui t'aide.", 1100, FAM[3])
    y = bulle(d, x, y + 40, "Pensée et besoin", "Ce que tu t'es dit, et ce dont tu avais besoin.", 1100, LAVANDE)
    bulle(d, x, y + 40, "Une autre façon de voir", "Puis une réponse que tu choisis, au lieu de la subir.", 1100, SAUGE)
    signature(d)
    return F.enregistrer(im, "fiche-03-fiche-emotion.jpg")


def p03_palette():
    im = fond((238, 234, 240)).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "pour trouver le mot juste", "48 mots et une carte du corps", "plus le mot est précis, plus c'est clair",
           couleur_sur=LAVANDE)
    coller(im, page(4, 860), (1040, 1360), -4, eleve=1.0)
    coller(im, page(7, 860), (1960, 1380), 4, eleve=1.0)
    d = ImageDraw.Draw(im)
    signature(d)
    return F.enregistrer(im, "fiche-04-palette-corps.jpg")


def p04_mois():
    im = fond((236, 236, 230)).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "voir ce qui revient", "Ton mois en couleurs", "et un bilan chaque semaine, sommeil compris", couleur_sur=SAUGE)
    coller(im, page(10, 860), (1040, 1360), -3, eleve=1.0)
    coller(im, page(15, 860), (1960, 1380), 3, eleve=1.0)
    d = ImageDraw.Draw(im)
    signature(d)
    return F.enregistrer(im, "fiche-05-mois-bilan.jpg")


def p05_tablette():
    im = fond((232, 234, 238)).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "version tablette incluse", "Onglets et sommaire cliquables", "GoodNotes, Notability, Xodo… et toute appli de PDF",
           couleur_sur=BRUME)
    coller(im, tablette(page(2, 820, "t"), 820), (1000, 1330), -3, eleve=1.2)
    coller(im, tablette(page(10, 640, "t"), 640), (1880, 1420), 5, eleve=1.0)
    stylet(im, 2350, 2000, 560, -60)
    d = ImageDraw.Draw(im)
    x = 2330
    y = bulle(d, x, 600, "Sommaire", "Une ligne touchée, tu y es.", 600, BRUME)
    y = bulle(d, x, y + 40, "Onglets", "Exemple, semaines 1 à 4, outils.", 600, ROSE)
    bulle(d, x, y + 40, "Retour", "Le bas de chaque page ramène au sommaire.", 600, SAUGE)
    return F.enregistrer(im, "fiche-06-tablette-cliquable.jpg")


def p06_contenu():
    im = fond((240, 236, 228)).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "tout ce que tu reçois", "40 pages + 3 pages bonus", y=90)
    cols, lw = 10, 210
    x0 = (W - cols * lw - (cols - 1) * 26) // 2
    for i in range(40):
        r, c = divmod(i, cols)
        coller(im, page(i + 1, lw), (x0 + c * (lw + 26) + lw // 2, 500 + r * 330), 0, ombre=0.7, eleve=0.25)
    d = ImageDraw.Draw(im)
    items = ["Mode d'emploi + « Pourquoi ça marche »", "Palette, intensités, messages, carte du corps",
             "Méthode P.A.U.S.E. + audios offerts", "4 semaines : ouverture, 3 fiches, bilan",
             "9 outils : déclencheurs, le dire, bons moments…", "Bonus : cartes à découper (3 pages)"]
    y = 1820
    for k, t in enumerate(items):
        col = k % 2; x = 470 + col * 1180
        d.ellipse([x, y + 18, x + 26, y + 44], fill=[SAUGE, ROSE][col])
        assert x + 50 + largeur(d, t, TEXTE(50)) < W - 60, t
        d.text((x + 50, y), t, font=TEXTE(50), fill=TXT)
        if col == 1:
            y += 90
    return F.enregistrer(im, "fiche-07-contenu-complet.jpg")


def p07_versions():
    im = fond((236, 234, 230)).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "inclus dans ton achat", "3 versions + 3 pages bonus", "imprime ou annote, comme tu préfères", couleur_sur=SAUGE)
    coller(im, page(12, 640), (560, 1250), -3, eleve=1.0)
    coller(im, page(12, 640, "e"), (1240, 1250), 0, eleve=1.0)
    coller(im, tablette(page(13, 560, "t"), 560), (1920, 1250), 3, eleve=1.1)
    coller(im, page(1, 600, "k"), (2560, 1250), 4, eleve=1.0)
    d = ImageDraw.Draw(im)
    for x, lib, c in ((560, "Couleur", ROSE), (1240, "Économe en encre", (120, 116, 110)), (1920, "Tablette", BRUME),
                      (2560, "Bonus", (176, 140, 92))):
        w = largeur(d, lib, GRAS(52)) + 72
        pastille(d, x - w / 2, 1980, lib, GRAS(52), fond_c=c)
    return F.enregistrer(im, "fiche-08-trois-versions.jpg")


def p08_pourquoi():
    im = fond((242, 236, 228)).convert("RGBA")
    d = ImageDraw.Draw(im)
    coller(im, page(3, 900), (760, 1130), -3, eleve=1.0)
    brin(d, 1250, 2180, 460, -100)
    d = ImageDraw.Draw(im)
    x = 1460
    d.text((x, 230), "UNE MÉTHODE, PAS DES SLOGANS", font=GRAS(46), fill=ROSE)
    d.text((x, 300), "Pourquoi ça marche", font=TITRE(130), fill=BRUN)
    y = bulle(d, x, 560, "Mettre un mot apaise",
              "UCLA, 2007 : nommer l'émotion diminue la réaction de l'amygdale face à des images négatives.", 1340, ROSE)
    y = bulle(d, x, y + 50, "Changer de point de vue aide",
              "Université de Sheffield, 2012 : 306 comparaisons, la réévaluation parmi les stratégies les plus efficaces.",
              1340, SAUGE)
    bulle(d, x, y + 50, "Ruminer n'aide pas",
          "Université Yale, 2010 : la rumination, stratégie la plus liée à l'anxiété et à la dépression.", 1340, LAVANDE)
    centre(d, "« Pas de bonne ou de mauvaise émotion. Juste des signaux. »", MAIN(70), 1860, 1400, 2900, ROSE)
    return F.enregistrer(im, "fiche-09-pourquoi-ca-marche.jpg")


def p09_comment():
    im = fond((238, 234, 226)).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "téléchargement immédiat", "Comment ça marche ?", "aucun envoi postal : tout est en PDF")
    etapes = [("1", "Achète", "le journal sur Etsy"), ("2", "Télécharge", "les PDF, tout de suite"),
              ("3", "Imprime", "en A4, ou ouvre-le sur ta tablette"), ("4", "Remplis", "une fiche quand une émotion monte")]
    for i, (n, t, s) in enumerate(etapes):
        x = 450 + i * 700
        d.rounded_rectangle([x - 290, 700, x + 290, 1500], radius=50, fill=(252, 249, 243), outline=(228, 218, 202), width=3)
        d.ellipse([x - 110, 790, x + 110, 1010], fill=[SAUGE, ROSE, (176, 140, 92), LAVANDE][i])
        fo = TITRE(150); wn = d.textlength(n, font=fo, features=["lnum"])
        d.text((x - wn / 2, 800), n, font=fo, fill=(255, 255, 255), features=["lnum"])
        centre(d, t, TITRE(84), 1100, x - 290, x + 290)
        bloc(d, s, TEXTE(46), x - 250, 1240, 500, centrer=True)
    bloc(d, "Pour ton usage personnel. Outil pour mieux te connaître, pas un soin : si une émotion déborde souvent, "
            "parles-en à ton médecin ou à un psychologue.", TEXTE(44), 500, 1700, 2000, couleur=(130, 116, 104), centrer=True)
    signature(d, y=1950)
    return F.enregistrer(im, "fiche-10-comment-ca-marche.jpg")


def p10_plus():
    im = fond((240, 236, 230)).convert("RGBA")
    d = ImageDraw.Draw(im)
    entete(d, "ce que tu ne trouveras pas ailleurs", "Plus qu'un journal : une méthode complète",
           "créée par Clarté Mentale, en français")
    for i, (n, ang) in enumerate(zip((8, 5, 6, 34), (-6, -2, 2, 6))):
        coller(im, page(n, 620), (560 + i * 630, 1180 + abs(i - 1.5) * 30), ang, eleve=0.7 + 0.1 * i)
    d = ImageDraw.Draw(im)
    for x, lib, sous in ((560, "P.A.U.S.E.", "quand ça déborde + audios"), (1190, "Les intensités", "agir avant que ça déborde"),
                         (1820, "Le message", "de chaque émotion"), (2450, "Le dire", "en quatre temps")):
        centre(d, lib, J.SERIF(68, 600), 1880, x - 320, x + 320, BRUN)
        centre(d, sous, J.SANS(40, 350), 1970, x - 320, x + 320, TXT)
    return F.enregistrer(im, "fiche-02-methode-complete.jpg")


if __name__ == "__main__":
    rendre_pages()
    for vieux in glob.glob(os.path.join(F.DOSSIER, "fiche-*.jpg")):
        os.remove(vieux)
    for fn in (p01_couverture, p10_plus, p02_fiche, p03_palette, p04_mois, p05_tablette, p06_contenu, p07_versions, p08_pourquoi, p09_comment):
        print(fn())
