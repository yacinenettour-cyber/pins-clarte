"""Génère les kits Idea Pins (slides 1080x1920 + texte.txt) à publier à la main.

Même visuel que les kits du 29/09 : fond crème, étiquette, titre, photo arrondie sous le texte
(jamais de texte sur la photo), une photo différente par slide, slide récap sans photo.
Les photos des kits sont rangées dans kits_idea_pins/photos/ (hors de fonds/) pour que le pipeline
ne les réutilise jamais dans un pin automatique.
Usage : python3 outils/generer_kits_idea_pins.py  (régénère les kits définis dans KITS)
"""
import json, os, re
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)

L, H, M = 1080, 1920, 80
CREME, ENCRE, CARTE, OMBRE, GRIS = (247, 243, 236), (31, 41, 64), (255, 255, 255), (228, 221, 209), (110, 116, 132)
SOUS = (72, 80, 100)
MARQUE = "Clarté Mentale | Stress & Énergie"
ACCENTS = {"sommeil": (72, 88, 158), "systemenerveux": (74, 132, 112), "procrastination": (214, 106, 84),
           "somatisation": (48, 128, 140)}
LIBELLES = {"sommeil": "Sommeil", "systemenerveux": "Système nerveux", "procrastination": "Procrastination",
            "somatisation": "Signaux du corps"}
LIEN = "https://lp.contactapaisement-mental.fr/tonguide?utm_source=pinterest&utm_medium=organic&utm_campaign=idea-pins"

KITS = [
    {
        "dossier": "4-corps-tendu-au-coucher", "theme": "sommeil", "lien": True,
        "tableau": "Sommeil : mieux dormir & routine du soir",
        "titre": "Corps tendu au coucher : 5 gestes doux pour t'endormir plus détendu(e)",
        "couverture": ("5 gestes doux pour un corps détendu au coucher", "À faire directement au lit", "fond-101.jpg"),
        "etapes": [
            ("Relâcher la mâchoire", "Desserre les dents et laisse la langue se poser contre le palais. Une mâchoire détendue envoie un signal de calme au cerveau.", "fond-27.jpg"),
            ("Laisser tomber les épaules", "Monte les épaules vers les oreilles en inspirant, puis relâche-les d'un coup en expirant. Trois fois.", "fond-204.jpg"),
            ("Allonger l'expiration", "Inspire sur 4 temps, expire sur 6 à 8 temps. L'expiration longue aide le système nerveux à redescendre.", "fond-193.jpg"),
            ("Une main sur le ventre", "Sens-le monter et descendre sans rien forcer. L'attention quitte les pensées et revient au corps.", "fond-202.jpg"),
            ("Le scan des pieds à la tête", "Passe chaque zone en revue et relâche-la en expirant. Si une pensée revient, passe simplement à la zone suivante.", "fond-158.jpg"),
        ],
        "recap": ("Un corps détendu au coucher", "Enregistre cette épingle pour ce soir, au moment d'éteindre la lumière."),
        "description": "Le corps est fatigué mais reste tendu au coucher ? Mâchoire serrée, épaules hautes, souffle court : le système nerveux reste en alerte. 5 gestes doux à faire au lit : relâcher la mâchoire, laisser tomber les épaules, allonger l'expiration, une main sur le ventre, un scan du corps. Si c'est surtout ta tête qui t'empêche de dormir, le guide gratuit propose une routine anti-rumination au lit.",
        "hashtags": "#sommeil #endormissement #routinedusoir #systemenerveux #detente #stress #insomnie #relaxation",
        "alt": "Infographie en 7 slides : 5 gestes doux à faire au lit pour détendre le corps avant de dormir — relâcher la mâchoire, laisser tomber les épaules, allonger l'expiration, main sur le ventre, scan du corps.",
    },
    {
        "dossier": "5-tensions-de-stress-5-minutes", "theme": "somatisation", "lien": True,
        "tableau": "Somatisation & signaux du corps",
        "titre": "Mâchoire, épaules, ventre : 5 tensions de stress à relâcher en 5 minutes",
        "couverture": ("5 tensions de stress à relâcher en 5 minutes", "Mâchoire, épaules, nuque, ventre, mains", "fond-194.jpg"),
        "etapes": [
            ("La mâchoire serrée", "Ouvre légèrement la bouche et masse les joues en petits cercles pendant 30 secondes. On serre souvent sans s'en rendre compte.", "fond-nerfvague.jpg"),
            ("Les épaules remontées", "Laisse-les redescendre loin des oreilles, puis fais 5 grands cercles lents vers l'arrière.", "fond-48.jpg"),
            ("La nuque raide", "Incline doucement la tête vers une épaule, respire trois fois, puis change de côté. Sans à-coups.", "fond-60.jpg"),
            ("Le ventre noué", "Une main sur le ventre : gonfle-le en inspirant, relâche-le en expirant. Cinq respirations lentes.", "fond-66.jpg"),
            ("Les mains crispées", "Serre fort les poings pendant 5 secondes, puis ouvre grand les doigts. Sens la différence.", "fond-163.jpg"),
        ],
        "recap": ("5 tensions à relâcher", "Garde-la sous la main pour la prochaine fois que le stress monte."),
        "description": "Le stress s'installe dans la mâchoire, les épaules, la nuque, le ventre et les mains, souvent sans que tu t'en rendes compte. Ces 5 gestes relâchent chaque zone en moins de 5 minutes, au bureau comme à la maison, sans matériel. À faire dès que la pression monte. Si ces tensions te suivent jusqu'au lit, le guide gratuit propose une routine du soir pour calmer le mental avant de dormir.",
        "hashtags": "#somatisation #tensions #stress #systemenerveux #relaxation #corpsetesprit #gestiondustress #bienetre",
        "alt": "Infographie en 7 slides : 5 tensions de stress à relâcher en 5 minutes — mâchoire, épaules, nuque, ventre et mains, avec un geste simple pour chacune.",
    },
    {
        "dossier": "6-dormir-apres-une-dispute", "theme": "sommeil", "lien": True,
        "tableau": "Sommeil : mieux dormir & routine du soir",
        "titre": "Dormir après une dispute : 5 gestes quand ta tête rejoue la scène",
        "couverture": ("Dormir après une dispute", "5 gestes quand ta tête rejoue la scène", "fond-81.jpg"),
        "etapes": [
            ("Écrire ce que tu ressens", "Trois phrases sur papier, sans te relire. Ce qui est écrit n'a plus besoin de tourner en boucle.", "fond-79.jpg"),
            ("Fixer un moment pour en reparler", "Décide quand tu reprendras la discussion demain. Le cerveau lâche plus facilement ce qui a une suite prévue.", "fond-108.jpg"),
            ("Relâcher la mâchoire et les poings", "La colère se loge dans le corps : desserre les dents, ouvre les mains, laisse tomber les épaules.", "fond-174.jpg"),
            ("Expirer plus longtemps", "Inspire sur 4 temps, expire sur 6 à 8. Quelques cycles suffisent pour que le cœur ralentisse.", "fond-41.jpg"),
            ("Nommer la boucle", "Quand la scène revient, dis-toi simplement « je rejoue la dispute », puis reviens à ta respiration. Sans te juger.", "fond-26.jpg"),
        ],
        "recap": ("Dormir malgré une dispute", "Enregistre-la : elle servira le prochain soir où la tête refuse de lâcher."),
        "description": "Après une dispute, le corps se couche mais la tête rejoue la scène en boucle, cherche la bonne réplique et repousse le sommeil. Ces 5 gestes aident à poser la journée : écrire ce que tu ressens, fixer un moment pour en reparler, relâcher la mâchoire et les poings, allonger l'expiration et nommer la boucle quand elle revient. Le guide gratuit propose une routine anti-rumination à faire au lit.",
        "hashtags": "#sommeil #ruminations #insomnie #emotions #stress #routinedusoir #systemenerveux #bienetre",
        "alt": "Infographie en 7 slides : 5 gestes pour dormir après une dispute — écrire ce que l'on ressent, fixer un moment pour en reparler, relâcher mâchoire et poings, allonger l'expiration, nommer la boucle.",
    },
    {
        "dossier": "7-micro-pas-procrastination", "theme": "procrastination", "lien": False,
        "tableau": "Procrastination & fatigue mentale",
        "titre": "5 micro-pas pour lancer enfin la tâche que tu repousses",
        "couverture": ("5 micro-pas pour lancer la tâche que tu repousses", "Quand commencer paraît trop lourd", "fond-69.jpg"),
        "etapes": [
            ("Nommer la toute première action", "Pas « faire le dossier » mais « ouvrir le fichier ». Plus l'action est petite, plus elle se lance facilement.", "fond-32.jpg:0.75"),
            ("Un minuteur de 5 minutes", "Tu t'autorises à t'arrêter quand il sonne. Souvent, le plus dur est déjà fait.", "fond-37.jpg:0.62"),
            ("Éloigner le téléphone", "Dans une autre pièce ou en mode avion : chaque notification relance l'envie de fuir la tâche.", "fond-97.jpg"),
            ("Accepter un brouillon", "Vise « mal fait mais commencé » plutôt que parfait. On améliore plus facilement qu'on ne crée.", "fond-83.jpg"),
            ("Noter où tu t'arrêtes", "Une phrase pour la prochaine fois : reprendre devient beaucoup plus simple.", "fond-45.jpg:0.6"),
        ],
        "recap": ("5 micro-pas pour démarrer", "Choisis une tâche et teste le premier micro-pas maintenant."),
        "description": "Tu repousses la même tâche depuis des jours et rien que d'y penser te fatigue ? Le blocage vient rarement de la paresse : la tâche paraît trop grosse pour commencer. 5 micro-pas rendent le démarrage plus léger : nommer la première action, lancer un minuteur de 5 minutes, éloigner le téléphone, accepter un brouillon imparfait, noter où tu t'arrêtes. Le premier pas fait souvent le reste.",
        "hashtags": "#procrastination #motivation #passeralaction #organisation #productivite #focus #fatiguementale #bienetre",
        "alt": "Infographie en 7 slides : 5 micro-pas pour lancer une tâche repoussée — première action, minuteur de 5 minutes, téléphone éloigné, brouillon accepté, noter où l'on s'arrête.",
    },
]


def police(gras, taille):
    return ImageFont.truetype("Poppins-Bold.ttf" if gras else "Poppins-Regular.ttf", taille)


def couper(d, texte, pol, largeur):
    lignes, ligne = [], ""
    for mot in re.split(r"(?<!«)\s+(?![?!:;»])", texte.strip()):
        essai = (ligne + " " + mot).strip()
        if d.textlength(essai, font=pol) <= largeur:
            ligne = essai
        else:
            if ligne:
                lignes.append(ligne)
            ligne = mot
    if ligne:
        lignes.append(ligne)
    return lignes


CADRAGE = json.load(open("fonds_cadrage.json", encoding="utf-8")) if os.path.exists("fonds_cadrage.json") else {}


def recadrer(nom, w, h):
    # « fond-32.jpg:0.75 » : centre vertical choisi à la main (0 = haut, 1 = bas).
    nom, _, cy_force = nom.partition(":")
    img = Image.open(os.path.join("kits_idea_pins", "photos", nom)).convert("RGB")
    r = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    cx, cy = 0.5, 0.45
    if nom in CADRAGE:
        cx = CADRAGE[nom].get("x", cx)
        cy = CADRAGE[nom].get("tete", [cx, cy])[1]
    if cy_force:
        cy = float(cy_force)
    x = min(max(0, round(cx * img.width - w / 2)), img.width - w)
    y = min(max(0, round(cy * img.height - h / 2)), img.height - h)
    return img.crop((x, y, x + w, y + h))


def photo_arrondie(img, nom, y0, y1):
    ph = recadrer(nom, L - 2 * M, y1 - y0)
    masque = Image.new("L", ph.size, 0)
    ImageDraw.Draw(masque).rounded_rectangle([0, 0, ph.width - 1, ph.height - 1], radius=40, fill=255)
    img.paste(ph, (M, y0), masque)


def etiquette(d, texte, accent):
    pol = police(True, 30)
    w = d.textlength(texte, font=pol)
    clair = tuple(int(c + (255 - c) * 0.82) for c in accent)
    d.rounded_rectangle([M, 110, M + w + 50, 166], radius=28, fill=clair)
    d.text((M + 25, 120), texte, font=pol, fill=accent)


def pied(d):
    pol = police(False, 32)
    d.text(((L - d.textlength(MARQUE, font=pol)) / 2, H - 90), MARQUE, font=pol, fill=GRIS)


BAS_PHOTO = H - 160


def slide_couverture(kit, chemin):
    titre, sous, photo = kit["couverture"]
    accent = ACCENTS[kit["theme"]]
    img = Image.new("RGB", (L, H), CREME)
    d = ImageDraw.Draw(img)
    etiquette(d, LIBELLES[kit["theme"]].upper(), accent)
    for taille in (92, 84, 76, 68):
        pol = police(True, taille)
        lignes = couper(d, titre, pol, L - 2 * M)
        if len(lignes) <= 3:
            break
    y = 220
    for l in lignes:
        d.text((M, y), l, font=pol, fill=ENCRE)
        y += int(taille * 1.22)
    d.rounded_rectangle([M, y + 14, M + 140, y + 24], radius=5, fill=accent)
    y += 60
    pol_s = police(False, 44)
    for l in couper(d, sous, pol_s, L - 2 * M):
        d.text((M, y), l, font=pol_s, fill=SOUS)
        y += 58
    haut_photo = y + 40
    bas = H - 220
    photo_arrondie(img, photo, haut_photo, bas)
    pol_f = police(True, 38)
    t = "Fais défiler"
    w = d.textlength(t, font=pol_f)
    d.text((L - M - w - 70, H - 190), t, font=pol_f, fill=accent)
    d.line([(L - M - 50, H - 167), (L - M, H - 167)], fill=accent, width=5)
    d.polygon([(L - M, H - 167), (L - M - 16, H - 178), (L - M - 16, H - 156)], fill=accent)
    pied(d)
    img.save(chemin, "JPEG", quality=92, optimize=True)
    return y, haut_photo


def slide_etape(kit, i, etape, chemin):
    titre, texte, photo = etape
    accent = ACCENTS[kit["theme"]]
    n = len(kit["etapes"])
    img = Image.new("RGB", (L, H), CREME)
    d = ImageDraw.Draw(img)
    etiquette(d, f"ÉTAPE {i}/{n}", accent)
    d.ellipse([M, 280, M + 144, 424], fill=accent)
    pn = police(True, 76)
    d.text((M + 72 - d.textlength(str(i), font=pn) / 2, 300), str(i), font=pn, fill=(255, 255, 255))
    y = 480
    pt = police(True, 64)
    for l in couper(d, titre, pt, L - 2 * M):
        d.text((M, y), l, font=pt, fill=ENCRE)
        y += 78
    y += 14
    pc = police(False, 42)
    for l in couper(d, texte, pc, L - 2 * M):
        d.text((M, y), l, font=pc, fill=SOUS)
        y += 62
    haut_photo = y + 50
    photo_arrondie(img, photo, haut_photo, BAS_PHOTO)
    pied(d)
    img.save(chemin, "JPEG", quality=92, optimize=True)
    return y, haut_photo


def slide_recap(kit, chemin):
    titre, cta = kit["recap"]
    accent = ACCENTS[kit["theme"]]
    img = Image.new("RGB", (L, H), CREME)
    d = ImageDraw.Draw(img)
    etiquette(d, "RÉCAP", accent)
    pt = police(True, 72)
    y = 230
    for l in couper(d, titre, pt, L - 2 * M):
        d.text((M, y), l, font=pt, fill=ENCRE)
        y += 88
    y += 60
    pc = police(False, 44)
    for i, (t, _, _) in enumerate(kit["etapes"], 1):
        lignes = couper(d, t, pc, L - 2 * M - 180)
        h = max(150, 60 * len(lignes) + 70)
        d.rounded_rectangle([M + 3, y + 6, L - M + 3, y + h + 6], radius=30, fill=OMBRE)
        d.rounded_rectangle([M, y, L - M, y + h], radius=30, fill=CARTE)
        xc, yc = M + 72, y + h / 2
        d.ellipse([xc - 38, yc - 38, xc + 38, yc + 38], fill=accent)
        pn = police(True, 40)
        d.text((xc - d.textlength(str(i), font=pn) / 2, yc - 30), str(i), font=pn, fill=(255, 255, 255))
        yt = y + (h - 60 * len(lignes)) / 2 - 4
        for l in lignes:
            d.text((M + 145, yt), l, font=pc, fill=ENCRE)
            yt += 60
        y += h + 30
    y += 50
    pb = police(True, 52)
    for l in couper(d, cta, pb, L - 2 * M):
        d.text((M, y), l, font=pb, fill=accent)
        y += 68
    pied(d)
    img.save(chemin, "JPEG", quality=92, optimize=True)
    return y


def texte_kit(kit, n_slides):
    desc = kit["description"] + " " + kit["hashtags"]
    lien = f"OUI : {LIEN}" if kit["lien"] else "NON : laisser le champ Lien vide (thème hors du guide)"
    ordre = "\n".join(f"{i}. slide-{i}.jpg" for i in range(1, n_slides + 1))
    return f"""KIT IDEA PIN — {kit['titre']}

Tableau : {kit['tableau']}
Lien de destination : {lien}

TITRE (à copier)
{kit['titre']}

DESCRIPTION (à copier)
{desc}

TEXTE ALTERNATIF (à copier si l'appli le propose)
{kit['alt']}

ORDRE DES SLIDES
{ordre}

À FAIRE DANS L'APPLI PINTEREST
1. + (Créer) → Épingle → sélectionne les slides dans l'ordre 1 → {n_slides}
2. Colle le titre, la description, choisis le tableau indiqué
3. Ajoute le lien seulement si indiqué OUI ci-dessus
4. Publie
"""


def main():
    rapport = []
    for kit in KITS:
        dos = os.path.join("kits_idea_pins", kit["dossier"])
        os.makedirs(dos, exist_ok=True)
        zones = [slide_couverture(kit, os.path.join(dos, "slide-1.jpg"))]
        for i, e in enumerate(kit["etapes"], 1):
            zones.append(slide_etape(kit, i, e, os.path.join(dos, f"slide-{i + 1}.jpg")))
        n = len(kit["etapes"]) + 2
        fin_recap = slide_recap(kit, os.path.join(dos, f"slide-{n}.jpg"))
        with open(os.path.join(dos, "texte.txt"), "w", encoding="utf-8") as f:
            f.write(texte_kit(kit, n))
        rapport.append({"kit": kit["dossier"], "texte_bas_vs_photo_haut": [(a, b) for a, b in zones],
                        "photo_min_px": min(BAS_PHOTO - b for _, b in zones[1:]),
                        "recap_bas": fin_recap})
    print(json.dumps(rapport, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
