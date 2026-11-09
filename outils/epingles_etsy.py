"""Épingles « fiche » 09/11/2026 : 91 images fournies par l'utilisateur, chacune reliée à la bonne destination
(fiche Etsy du produit ou article du site, d'après le bouton dessiné sur l'image).
Usage : python3 outils/epingles_etsy.py [--ecrire]  (sans --ecrire : contrôle seulement).
Les images sont lues dans UPLOADS, converties en JPEG dans images_etsy/<slug>.jpg ; seules les épingles qui passent
le contrôle anti-doublons entrent dans pins.json, les autres restent en stock dans images_etsy/ (jamais publiées)."""
import json, os, re, sys, unicodedata, zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import anti_doublons as A
from PIL import Image

UPLOADS = "/root/.claude/uploads/52b1010b-100c-5085-8b52-481926932e64/"
ETSY = {
    "P": "https://www.etsy.com/fr/listing/4610269767/planner-charge-mentale-couple-qui-fait",
    "J": "https://www.etsy.com/fr/listing/4610325459/journal-des-emotions-adulte-fiche-guidee",
    "R": "https://www.etsy.com/fr/listing/4610355585/carnet-anti-ruminations-du-soir-pdf-o",
    "C": "https://www.etsy.com/fr/listing/4611081068/cahier-anti-procrastination-pdf-14",
    # Journal du sommeil : fiche visible dans la boutique (liste « More from this shop »), lien non donné par l'utilisateur.
    "S": "https://www.etsy.com/fr/listing/4610492753/sleep-diary-pdf-21-guided-evenings-and",
}
# id (8 premiers caractères du fichier) : (produit ou article, titre dessiné sur l'image)
T = {
 # Planner « charge mentale à deux » (bouton « Voir le planner »)
 "1475703a": ("P", "Partager une responsabilité"), "26bab911": ("P", "Déléguer sans garder tout le suivi"),
 "353b21b4": ("P", "Dire qu'une répartition ne convient plus"), "4e2ca435": ("P", "Le point du foyer à deux"),
 "562d04ff": ("P", "Notre accord pour la semaine"), "602cdfdf": ("P", "La tâche et ses rappels"),
 "7fd45b1f": ("P", "Faire une demande concrète"), "9dd394de": ("P", "Qui suit le stock à la maison ?"),
 "ab5f948c": ("P", "La responsabilité qui déborde"), "bbbf56d4": ("P", "Une semaine plus visible"),
 "c182f058": ("P", "Répartir les rendez-vous"), "c6da421b": ("P", "Le point avant le week-end"),
 "fd5ea544": ("P", "La liste avant les courses"),
 # Journal des émotions (« Utiliser le journal » + « Découvrir le carnet » côté émotions)
 "55e18105": ("J", "Ce que je voudrais exprimer"), "6260dc33": ("J", "Une pause avant la conversation"),
 "68846012": ("J", "Le carnet des nuances"), "dbef20d9": ("J", "L'émotion et la demande"),
 "fbdf169c": ("J", "Mettre un mot sur son émotion"), "14b64c1c": ("J", "Mon point émotion du soir"),
 "200b38bb": ("J", "Clarifier un besoin"), "2cd32c2c": ("J", "Écrire sans se juger"),
 "3257e4a9": ("J", "Ce moment m'a touché"), "4160f234": ("J", "Une place pour l'émotion agréable"),
 "446b0636": ("J", "Une émotion, plusieurs mots"), "77d05791": ("J", "Quand les mots ne viennent pas"),
 "7b9f4098": ("J", "Après une contrariété"), "7c256fa3": ("J", "La phrase qui parle de moi"),
 "89575e10": ("J", "Nuancer son « ça va »"), "945921f3": ("J", "Avant de répondre sous le coup d'une émotion"),
 "ceace16d": ("J", "L'émotion change au fil de la journée"), "d3919654": ("J", "La météo intérieure"),
 "f903e2f4": ("J", "Le fait et le ressenti"),
 # Journal du sommeil (« Découvrir le journal », notes de nuit et de réveil)
 "05924493": ("S", "Une nuit sans note"), "08fe9664": ("S", "L'énergie au réveil"),
 "14d80fbf": ("S", "Ce que mon journal peut montrer"), "3a1ce950": ("S", "La fiche des réveils ressentis"),
 "3bbce0c5": ("S", "Relire son journal du sommeil"), "3f79614a": ("S", "Mes repères de coucher"),
 "404e7346": ("S", "La soirée et le lendemain"), "5689f8c3": ("S", "Le point du matin"),
 "73f641f9": ("S", "Observer plusieurs nuits"), "756c202e": ("S", "Mon bilan de nuits à mon rythme"),
 "76188879": ("S", "L'environnement de ma soirée"), "999e36a3": ("S", "Préparer sa note du matin"),
 "9c64e949": ("S", "Un essai à observer le soir"), "bf96c8f4": ("S", "Une semaine de nuits différentes"),
 "f5244b63": ("S", "Mon rituel en version simple"),
 # Carnet anti-ruminations du soir (« Découvrir le carnet » côté pensées du soir)
 "37f26287": ("R", "Déposer une journée difficile"), "3f596948": ("R", "Ce qui peut attendre demain"),
 "6b6ea8b7": ("R", "Quand une conversation revient"), "88e6468d": ("R", "Fermer une boucle du soir"),
 "8b3895d1": ("R", "Une chose à la fois, ce soir"), "93df1b2e": ("R", "Une pensée, une prochaine étape"),
 "98528453": ("R", "Le tri des pensées du soir"), "b9e4914d": ("R", "La page du trop-plein"),
 "c72820e0": ("R", "Le parking des idées"),
 # Cahier anti-procrastination (« Découvrir le carnet » côté petits pas, reprise, victoires)
 "058b1886": ("C", "Quand une journée semble vide"), "09b21638": ("C", "Une difficulté, un apprentissage"),
 "0dd852ba": ("C", "Reprendre après une pause"), "0f5ab8ef": ("C", "L'effort derrière le résultat"),
 "26335d55": ("C", "Mon petit pas de demain"), "3dc47f06": ("C", "Le bilan des petits pas"),
 "420b7ec3": ("C", "La limite que j'ai respectée"), "4ee94709": ("C", "Ce qui m'a aidé à avancer"),
 "543d17c7": ("C", "La preuve de mon avancée"), "649df67e": ("C", "Distinguer un jour de tout le parcours"),
 "7eb97f2f": ("C", "Ma page de petites victoires"), "a62e708f": ("C", "Le carnet des essais"),
 "ac34f497": ("C", "Repérer une petite victoire"), "ba5af292": ("C", "Recevoir un retour positif"),
 "c1baa41f": ("C", "Reconnaître son courage discret"),
 # Articles du site (bouton « Lire l'article »)
 "2c06b386": ("charge-mentale", "Le support commun du foyer"), "489a56fc": ("charge-mentale", "Une tâche, toutes ses étapes"),
 "668e59ab": ("charge-mentale", "Mon inventaire de charge mentale"), "b355e347": ("charge-mentale", "La liste visible et la liste invisible"),
 "d6a493e6": ("charge-mentale", "Faire un peu de place dans sa journée"), "e1c75f08": ("charge-mentale", "Les activités qui me prennent de la place"),
 "fd1ccc74": ("charge-mentale", "Le sujet à clarifier ensemble"),
 "37504f18": ("routine-du-soir-anti-stress", "Relire sa routine du soir"), "6aefd5e0": ("routine-du-soir-anti-stress", "Le rituel des soirs chargés"),
 "a307d406": ("routine-du-soir-anti-stress", "Ma transition de fin de journée"), "acbd10d4": ("routine-du-soir-anti-stress", "La routine du soir en trois choix"),
 "46c9a2e4": ("fatigue-nerveuse", "Préparer une discussion sur sa fatigue"), "7f6ec464": ("fatigue-nerveuse", "Le point sur sa fatigue mentale"),
 "6ffa36cc": ("ruminations-le-soir", "Une note plutôt qu'une boucle"), "9f27c97b": ("ruminations-le-soir", "Reconnaître une pensée répétitive"),
 "d0930c42": ("ruminations-le-soir", "Mon rendez-vous avec une question"), "d127148f": ("ruminations-le-soir", "Passé, présent ou demain ?"),
 "f20521f5": ("ruminations-le-soir", "Ce soir, distinguer penser et agir"),
 "9f044997": ("ecran-avant-de-dormir", "Faire le point sur ses écrans le soir"),
 "87761970": ("calmer-son-systeme-nerveux", "Choisir une pause qui me convient"),
}

# Rubrique du titre d'épingle (mot recherché en tête) : plusieurs variantes par produit pour éviter les titres jumeaux.
RUBRIQUES = {
 "P": ["Charge mentale à deux", "Planner du foyer", "Répartition des tâches"],
 "J": ["Journal des émotions", "Gérer ses émotions", "Mettre des mots sur ses émotions"],
 "S": ["Journal du sommeil", "Suivi de ses nuits", "Mieux dormir"],
 "R": ["Pensées du soir", "Ruminations du soir", "Calmer son mental le soir"],
 "C": ["Procrastination", "Avancer sans pression", "Petits pas"],
 "charge-mentale": ["Charge mentale", "Charge mentale au quotidien"],
 "routine-du-soir-anti-stress": ["Routine du soir", "Rituel du soir"],
 "fatigue-nerveuse": ["Fatigue mentale", "Fatigue nerveuse"],
 "ruminations-le-soir": ["Ruminations le soir", "Pensées qui tournent"],
 "ecran-avant-de-dormir": ["Écrans le soir"],
 "calmer-son-systeme-nerveux": ["Système nerveux"],
}
HASH = {
 "P": "#chargementale #couple #organisation #foyer #partagedestaches #planner #imprimable #famille #equilibre",
 "J": "#gestiondesemotions #emotions #journaling #ressenti #bienetre #imprimable #santementale #carnet",
 "S": "#sommeil #journaldusommeil #mieuxdormir #nuit #routinedusoir #imprimable #bienetre #carnet",
 "R": "#ruminations #soir #pensees #sommeil #routinedusoir #calme #journaling #imprimable #carnet",
 "C": "#procrastination #motivation #petitspas #organisation #productivite #journaling #imprimable #carnet",
 "charge-mentale": "#chargementale #foyer #organisation #couple #equilibre #famille #bienetre",
 "routine-du-soir-anti-stress": "#routinedusoir #sommeil #soir #detente #mieuxdormir #bienetre #rituel",
 "fatigue-nerveuse": "#fatiguementale #fatigue #stress #recuperation #bienetre #mental #ecoutedesoi",
 "ruminations-le-soir": "#ruminations #soir #pensees #sommeil #calme #bienetre #mental",
 "ecran-avant-de-dormir": "#ecrans #sommeil #soir #routinedusoir #mieuxdormir #bienetre #deconnexion",
 "calmer-son-systeme-nerveux": "#systemenerveux #calme #pause #stress #bienetre #detente #mental",
}
THEME_DE = {"P": "fatiguementale", "J": "systemenerveux", "S": "sommeil", "R": "sommeil", "C": "procrastination",
            "charge-mentale": "fatiguementale", "routine-du-soir-anti-stress": "sommeil", "fatigue-nerveuse": "fatiguementale",
            "ruminations-le-soir": "sommeil", "ecran-avant-de-dormir": "sommeil", "calmer-son-systeme-nerveux": "systemenerveux"}

# Phrases : « {T} » = titre dessiné sur l'image. Plusieurs ouvertures, milieux et fins par destination.
OUV = [
 "La fiche « {T} » tient sur une page : trois repères, un crayon, quelques minutes.",
 "« {T} » : une fiche simple à remplir quand tu as un moment, sans te mettre la pression.",
 "Voici une fiche à garder pour « {T} » : trois cases, des mots à toi, pas de bonne réponse.",
 "Pour « {T} », une page guidée suffit : tu écris, tu relis, tu choisis la suite.",
 "Envie de poser « {T} » sur le papier ? Cette fiche t'y aide en trois étapes courtes.",
 "« {T} » : trois questions à remplir à ton rythme, quelques lignes suffisent.",
]
MIL = {
 "P": ["Elle vient du planner « charge mentale à deux » : qui fait quoi, qui y pense, qui suit, pour que la charge se voie enfin sur une même page.",
       "Le planner pour couples et foyers aide à rendre visible tout ce qu'on porte sans le dire, puis à répartir sans reproche.",
       "Dans le planner, chaque page sert à nommer une tâche, son suivi et ses rappels, pour en parler à deux calmement."],
 "J": ["Elle vient du journal des émotions : on décrit les faits, on cherche le bon mot parmi 48, on note ce dont on a besoin, puis on choisit quoi faire.",
       "Le journal des émotions propose une fiche guidée, une palette de 48 mots et des outils pour comprendre ce qui se passe en toi, une entrée à la fois.",
       "Ce journal pour adultes aide à mettre un mot sur ce qu'on ressent, sans chercher à le faire disparaître."],
 "S": ["Elle vient du journal du sommeil : 21 soirs et matins guidés pour observer tes nuits avec tes propres mots, sans te noter ni te juger.",
       "Le journal du sommeil se remplit en quelques lignes le soir et le matin : tu gardes une trace, puis tu relis pour repérer ce qui revient.",
       "Noter ses nuits aide à regarder plusieurs jours plutôt qu'une seule mauvaise nuit : c'est le principe de ce journal à imprimer."],
 "R": ["Elle vient du carnet anti-ruminations du soir : 14 soirs guidés pour déposer les pensées sur papier et terminer la journée plus légèrement.",
       "Le soir, sans boucle : un carnet de 57 pages pour trier ce qui peut attendre, mettre des mots sur ce qui tourne et fermer la journée.",
       "Ce carnet n'efface pas les pensées : il leur donne une place sur la page, pour qu'elles prennent moins de place dans ta soirée."],
 "C": ["Elle vient du cahier anti-procrastination : 14 ateliers pour repérer ce qui bloque, choisir un premier pas et reprendre sans repartir de zéro.",
       "Le cahier « Un pas, pas tout » aide à rendre un démarrage possible : une tâche, un geste accessible, un repère pour y revenir.",
       "Pas de course à la productivité : ce cahier de 60 pages propose des exercices concrets pour commencer, préparer ou reporter avec un repère."],
}
MIL_ART = [
 "Elle accompagne notre article sur ce sujet : explications simples, exemples du quotidien et sources, pour comprendre avant d'agir.",
 "L'article complet sur le site détaille le sujet pas à pas, avec des repères concrets et des études citées.",
 "Pour aller plus loin, l'article associé explique ce qui se joue et propose des pistes réalistes à tester ce soir.",
]
FIN = {
 "P": ["Le planner est sur ma boutique Etsy : lien dans l'épingle.", "Retrouve le planner complet sur Etsy via le lien de l'épingle.", "PDF A4 et version tablette à découvrir sur Etsy : lien dans l'épingle."],
 "J": ["Le journal complet est sur ma boutique Etsy : lien dans l'épingle.", "Retrouve le journal des émotions sur Etsy via le lien de l'épingle.", "PDF A4 et version tablette à découvrir sur Etsy : lien dans l'épingle."],
 "S": ["Le journal complet est sur ma boutique Etsy : lien dans l'épingle.", "Retrouve le journal du sommeil sur Etsy via le lien de l'épingle.", "PDF A4 imprimable à découvrir sur Etsy : lien dans l'épingle."],
 "R": ["Le carnet complet est sur ma boutique Etsy : lien dans l'épingle.", "Retrouve le carnet anti-ruminations sur Etsy via le lien de l'épingle.", "PDF imprimable et remplissable à découvrir sur Etsy : lien dans l'épingle."],
 "C": ["Le cahier complet est sur ma boutique Etsy : lien dans l'épingle.", "Retrouve le cahier anti-procrastination sur Etsy via le lien de l'épingle.", "PDF imprimable et remplissable à découvrir sur Etsy : lien dans l'épingle."],
}
FIN_ART = ["Article complet : lien dans l'épingle.", "Tu le lis gratuitement sur le site : lien dans l'épingle.", "À lire en entier via le lien de l'épingle."]
DET = [
 "Pas besoin de tout remplir : une seule page, un soir où tu y penses, et c'est déjà une trace utile.",
 "Tu peux l'imprimer ou l'annoter sur tablette, la remplir en cinq minutes et la reprendre plus tard.",
 "Elle ne cherche pas la bonne réponse : seulement un repère concret que tu retrouveras en la relisant.",
 "Écris trois lignes, pas un roman : l'idée est de rendre les choses plus claires, pas plus lourdes.",
 "Un stylo, une page, quelques minutes : c'est assez pour y voir un peu plus clair.",
 "Tu avances à ton rythme, sans objectif de perfection, et tu gardes seulement ce qui t'est utile.",
]
RAPPEL = ["Enregistre-la pour y revenir.", "Garde-la sous la main.", "Pratique à ressortir quand tu en as besoin.", "À retrouver dans ton tableau."]


def slug(s):
    s = unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode()
    return "-".join(re.findall(r"[a-z0-9]+", s))


def fichier(i8):
    return [f for f in os.listdir(UPLOADS) if f.startswith(i8) and f.endswith(".png")][0]


def construire(i8, rang=0):
    cle, titre_img = T[i8]
    h = zlib.crc32(i8.encode())
    art = cle not in ETSY
    rub = RUBRIQUES[cle]
    corps = None
    for essai in range(60):
        ouv = OUV[(h + essai) % len(OUV)].replace("{T}", titre_img)
        mil = (MIL_ART if art else MIL[cle])[(h // 7 + essai // 6) % (len(MIL_ART) if art else len(MIL[cle]))]
        fin = (FIN_ART if art else FIN[cle])[(h // 13 + essai // 18) % 3]
        rap = RAPPEL[(h // 5 + essai) % len(RAPPEL)]
        det = DET[(h // 3 + essai) % len(DET)]
        for parts in ([ouv, mil, det, fin], [ouv, mil, det, rap, fin], [ouv, mil, rap, fin]):
            c = " ".join(parts)
            if 380 <= len(c) <= min(450, 494 - len(HASH[cle])):
                corps = c
                break
        if corps:
            break
    assert corps, (i8, len(c))
    # Titre : rubrique recherchée en tête, 35-55 caractères ; repli sur le titre de l'image seul ou suffixé.
    t_min = titre_img[0].lower() + titre_img[1:]
    candidats = []
    for k in range(len(rub)):
        t0 = rub[(h + k) % len(rub)]
        if not any(m in t_min.lower() for m in re.findall(r"\w{6,}", t0.lower())):  # pas de répétition du mot-clé
            candidats += [f"{t0} : {t_min}"]
    for k in range(len(rub)):
        t0 = rub[(h + k) % len(rub)]
        candidats += [f"{titre_img} | {t0}"]
    candidats += [titre_img, f"{titre_img} : fiche à garder", f"{titre_img} – fiche à imprimer"]
    valides = []
    for c in candidats:
        if 35 <= len(c) <= 55 and c not in valides:
            valides.append(c)
    assert valides, (i8, titre_img)
    titre = valides[rang % len(valides)]
    pin = {"titre": titre, "description": f"{corps} {HASH[cle]}", "theme": THEME_DE[cle],
           "image_prete": f"images_etsy/{slug(titre_img)}.jpg", "format": "etsy", "guide": "aucun"}
    if art:
        pin["article"] = cle
        pin["description_article"] = pin["description"]
        # pas de lien Etsy ; le robot mène à l'article
    else:
        pin["lien_etsy"] = ETSY[cle]
    return pin


def main(ecrire):
    for k in HASH:
        HASH[k] = " ".join(HASH[k].split()[:8])
    assert len(T) == 91, len(T)
    fichiers = {i8: fichier(i8) for i8 in T}
    pins = [construire(i8, n) for n, i8 in enumerate(T)]
    noms = [p["image_prete"] for p in pins]
    assert len(set(noms)) == len(noms), "noms d'image en double"
    refs = A.charger_references()
    pub = {h["titre"] for h in json.load(open("historique.json", encoding="utf-8"))}
    existants = [p for p in json.load(open("pins.json", encoding="utf-8")) if p.get("format") != "etsy"]
    deja = [(p["titre"], "pin non publié", A.normaliser(p["titre"]), A.mots_cles(p["titre"])) for p in existants if p["titre"] not in pub]
    retenus, refuses = [], []
    for i8, p in zip(T, pins):
        assert 380 <= len(p["description"].rsplit(" #", 1)[0].split(" #")[0]) <= 450, p["titre"]
        assert len(p["description"]) <= 495, (p["titre"], len(p["description"]))
        assert 35 <= len(p["titre"]) <= 55, (p["titre"], len(p["titre"]))
        dbl, raison = A.est_doublon(p["titre"], refs + deja)
        for essai in range(1, 12):  # autre formulation du titre avant de renoncer
            if not dbl:
                break
            p = construire(i8, essai)
            pins[list(T).index(i8)] = p
            dbl, raison = A.est_doublon(p["titre"], refs + deja)
        if dbl:
            refuses.append((i8, p, raison))
        else:
            retenus.append((i8, p))
            deja.append((p["titre"], "épingle Etsy retenue", A.normaliser(p["titre"]), A.mots_cles(p["titre"])))
    print(len(retenus), "retenues,", len(refuses), "refusées (restent en stock)")
    for i8, p, r in refuses:
        print("  refusée :", p["titre"], "→", r)
    if not ecrire:
        return
    os.makedirs("images_etsy", exist_ok=True)
    for i8, p in zip(T, pins):
        dest = p["image_prete"]
        if not os.path.exists(dest):
            Image.open(UPLOADS + fichiers[i8]).convert("RGB").save(dest, "JPEG", quality=92)
    nouveaux = [p for _, p in retenus]
    # Les épingles « etsy » passent après les fiches-mémo déjà en tête et avant le reste de la banque.
    tete = [p for p in existants if p.get("image_prete", "").startswith("images_cles/fiche-memo") or p.get("format") == "etsy"]
    json.dump(existants[:0] + nouveaux + existants, open("pins.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({T[i8][1]: {"fichier": p["image_prete"], "destination": p.get("lien_etsy") or "article:" + p.get("article", ""),
                          "dans_pins_json": p in nouveaux} for i8, p in zip(T, pins)},
              open("images_etsy/registre.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Écrit :", len(nouveaux), "épingles dans pins.json,", len(pins), "images dans images_etsy/")


if __name__ == "__main__":
    main("--ecrire" in sys.argv)
