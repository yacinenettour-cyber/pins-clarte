# Génère le contenu des nouvelles leçons de la formation (format aiContentSchema « lecture » de systeme.io).
# Une leçon = une section « hero », une colonne de taille 12, blocs dans l'ordre de lecture.
import json, os

KIT = "https://cdn.jsdelivr.net/gh/yacinenettour-cyber/pins-clarte@22e9e84/medias/formation/kit/"
KIT2 = "https://cdn.jsdelivr.net/gh/yacinenettour-cyber/pins-clarte@9d8d4f2/medias/formation/kit/"  # fiche 7 + kit complet à 7 fiches (30/09)
OUT = os.path.dirname(os.path.abspath(__file__))
PALETTE = {"requestedColor": "#3D4F8F", "cornerStyle": "soft", "fontPair": "editorial", "cardLayout": None}


def H1(t): return {"type": "Headline", "text": t, "level": "h1"}
def H2(t): return {"type": "Headline", "text": t, "level": "h2"}
def T(h): return {"type": "Text", "textAlign": None, "html": h}
def BL(items, icon): return {"type": "BulletList", "items": items, "icon": icon}
def IMG(desc, alt): return {"type": "Image", "imageDescription": desc, "altText": alt}
def REF(*items, base=KIT): return {"type": "References", "items": [{"title": t, "url": base + f} for t, f in items]}


KIT_COMPLET = ("Le kit complet à imprimer, 6 fiches (PDF)", "kit-complet-clarte-mentale.pdf")
KIT_COMPLET_7 = ("Le kit complet à imprimer, 7 fiches (PDF)", "kit-complet-clarte-mentale.pdf")


def lecon(blocks):
    return {"palette": PALETTE, "sections": [{"tone": "hero", "backgroundImageDescription": None,
                                               "rows": [{"columns": [{"size": 12, "blocks": blocks}]}]}]}


LECONS = []


def add(slug, module, nom, blocks):
    LECONS.append({"slug": slug, "module": module, "nom": nom, "contenu": lecon(blocks)})


# ---------------- Apaiser le système nerveux ----------------

add("soupir-physiologique", "systeme-nerveux", "LE SOUPIR PHYSIOLOGIQUE : CALMER LE CORPS EN UNE MINUTE", [
    H1("Le soupir physiologique : calmer le corps en une minute"),
    T("<p>Quand le stress monte, ta respiration devient courte et haute, dans le haut de la poitrine. Ton corps comprend : « danger ». Le soupir physiologique fait l'inverse : c'est l'un des moyens les plus rapides de dire à ton système nerveux qu'il peut relâcher.</p>"
      "<p>Tu le fais déjà sans le savoir : c'est le grand soupir qui t'échappe après avoir pleuré, ou juste avant de t'endormir. Ici, tu vas simplement apprendre à le déclencher volontairement.</p>"),
    H2("Pourquoi ça marche"),
    T("<p>À l'inspiration, le cœur accélère légèrement. À l'expiration, il ralentit : c'est le nerf vague, le « frein » naturel de ton corps, qui entre en jeu. En rendant l'expiration plus longue que l'inspiration, tu appuies doucement sur ce frein.</p>"
      "<p>La double inspiration a un rôle précis : la deuxième petite bouffée d'air rouvre les minuscules alvéoles des poumons qui se sont affaissées quand tu respirais court. L'expiration qui suit vide mieux l'air, et le calme arrive plus vite.</p>"
      "<p>En 2023, une étude de l'université Stanford a comparé plusieurs exercices de respiration pratiqués 5 minutes par jour pendant un mois : c'est ce « soupir cyclique » qui a le plus amélioré l'humeur des participants.</p>"),
    IMG("person breathing calmly eyes closed evening", "Respiration calme, les yeux fermés, le soir"),
    H2("L'exercice pas à pas"),
    T("<ol><li><strong>Inspire par le nez</strong>, lentement, jusqu'à ce que tes poumons soient bien remplis.</li>"
      "<li><strong>Sans expirer, ajoute une deuxième petite inspiration</strong> par le nez, comme pour finir de remplir le haut des poumons.</li>"
      "<li><strong>Expire longuement par la bouche</strong>, lèvres entrouvertes, comme un long soupir, jusqu'à ce que l'air soit sorti sans forcer.</li>"
      "<li>Recommence <strong>3 à 5 fois</strong>. Pour un effet plus profond, continue jusqu'à 5 minutes.</li></ol>"
      "<p>L'expiration dure environ deux fois plus longtemps que l'inspiration. Ne force pas : si la tête te tourne, reprends une respiration normale quelques instants.</p>"),
    H2("Quand l'utiliser"),
    BL(["Au lit, quand tu sens le corps encore « en alerte »",
        "Lors d'un réveil nocturne (c'est l'étape 3 de la fiche SOS du kit)",
        "Juste avant un moment qui te stresse dans la journée",
        "Dès que tu remarques que tu retiens ta respiration"], "wind"),
    T("<p><strong>Ce soir :</strong> fais 5 soupirs physiologiques allongé(e), avant d'éteindre la lumière. Remarque simplement ce qui change dans tes épaules et ta mâchoire.</p>"),
])

add("relachement-musculaire", "systeme-nerveux", "LE RELÂCHEMENT MUSCULAIRE PROGRESSIF (VERSION DU SOIR)", [
    H1("Le relâchement musculaire progressif, version du soir"),
    T("<p>Le stress ne reste pas dans la tête : il s'installe dans les muscles. Mâchoire serrée, épaules remontées, ventre noué… Souvent, on ne sent même plus ces tensions, parce qu'elles sont devenues notre « normal ».</p>"
      "<p>Le relâchement musculaire progressif, mis au point par le médecin américain Edmund Jacobson dans la première moitié du XXe siècle, est l'une des techniques de relaxation les plus étudiées pour l'endormissement. Son principe surprend : pour mieux relâcher un muscle, on commence par le contracter.</p>"),
    H2("Pourquoi contracter pour relâcher ?"),
    T("<p>Après une contraction volontaire, le muscle se relâche plus profondément qu'avant. Surtout, le contraste t'apprend à <strong>sentir la différence</strong> entre tension et détente. Avec l'habitude, tu repères plus vite les tensions dans la journée, et tu sais les lâcher.</p>"),
    IMG("person lying in bed relaxing soft evening light", "Personne allongée qui relâche son corps"),
    H2("La version du soir : 7 zones, 5 minutes"),
    T("<p>Allongé(e) sur le dos. Pour chaque zone, <strong>contracte environ 5 secondes</strong> (fermement, sans douleur), puis <strong>relâche d'un coup</strong> et reste 15 à 20 secondes à sentir la détente.</p>"
      "<ol><li><strong>Mains et avant-bras</strong> : serre les poings.</li>"
      "<li><strong>Bras</strong> : plie les coudes et contracte les biceps.</li>"
      "<li><strong>Visage</strong> : plisse le front et ferme fort les yeux.</li>"
      "<li><strong>Mâchoire</strong> : serre les dents, puis laisse la bouche s'entrouvrir.</li>"
      "<li><strong>Épaules</strong> : monte-les vers les oreilles, puis laisse-les tomber.</li>"
      "<li><strong>Ventre</strong> : rentre et durcis le ventre, puis laisse-le s'arrondir.</li>"
      "<li><strong>Jambes et pieds</strong> : tends les jambes et tire les orteils vers toi.</li></ol>"
      "<p>Termine par trois respirations lentes en sentant ton corps entier, plus lourd, plus posé.</p>"),
    H2("Pour que ça marche"),
    BL(["Contracte à environ la moitié de ta force, jamais jusqu'à la douleur",
        "Zone douloureuse, blessée ou sujette aux crampes : relâche-la seulement, sans la contracter",
        "Le relâchement compte plus que la contraction : prends ton temps",
        "Les premiers soirs, ça peut sembler mécanique : l'effet vient avec la répétition"], "circle-check"),
    T("<p>C'est l'étape « relâchement musculaire court » de la version 10 minutes du rituel du soir.</p>"),
])

add("scan-corporel", "systeme-nerveux", "LE SCAN CORPOREL POUR GLISSER VERS LE SOMMEIL", [
    H1("Le scan corporel pour glisser vers le sommeil"),
    T("<p>Quand le mental tourne, il a besoin d'un endroit où se poser. Le scan corporel lui en donne un : ton propre corps, parcouru lentement, des pieds jusqu'à la tête. Ce n'est pas une technique pour « réussir » à dormir : c'est une façon de rester au lit sans lutter, et c'est souvent dans cet état que le sommeil arrive.</p>"),
    H2("Le principe"),
    T("<p>Tu promènes ton attention, comme le faisceau d'une lampe douce, sur chaque partie du corps. Tu n'as rien à changer : tu remarques simplement ce qui est là (chaleur, contact du drap, poids, picotements, tension). Si une tension est présente, imagine que ton expiration la traverse et l'adoucit.</p>"
      "<p>Quand ton esprit part ailleurs, et il partira, c'est normal : ramène-le gentiment là où tu t'étais arrêté(e). Chaque retour fait partie de l'exercice.</p>"),
    IMG("calm person lying in bed eyes closed dim bedroom", "Personne allongée les yeux fermés dans une chambre calme"),
    H2("Le parcours, 10 minutes environ"),
    T("<ol><li>Installe-toi sur le dos ou dans ta position d'endormissement. Trois respirations lentes.</li>"
      "<li><strong>Les pieds</strong> : les orteils, la plante, les talons posés sur le matelas.</li>"
      "<li><strong>Les jambes</strong> : les mollets, les genoux, les cuisses qui s'alourdissent.</li>"
      "<li><strong>Le bassin et le bas du dos</strong> : le poids qui s'enfonce dans le lit.</li>"
      "<li><strong>Le ventre</strong> : il se soulève et redescend, tout seul.</li>"
      "<li><strong>La poitrine et le dos</strong> : les côtes qui s'ouvrent et se referment.</li>"
      "<li><strong>Les mains, les bras, les épaules</strong> : laisse les épaules s'éloigner des oreilles.</li>"
      "<li><strong>La nuque, la mâchoire, le visage</strong> : la langue se détend, le front s'élargit.</li>"
      "<li>Pour finir, sens <strong>le corps entier</strong>, d'un seul bloc, qui respire.</li></ol>"),
    H2("Si tu t'endors avant la fin"),
    T("<p>C'est parfait. Le scan n'a pas besoin d'être terminé pour avoir fait son travail. Si tu arrives au bout encore éveillé(e), recommence depuis les pieds, plus lentement, ou pose simplement ton attention sur ta respiration.</p>"),
    BL(["À faire au lit, lumière éteinte",
        "Idéal les soirs d'agitation (version 20 minutes du rituel)",
        "Utile aussi lors d'un réveil nocturne"], "moon"),
])

# ---------------- Sortir des ruminations ----------------

add("rendez-vous-soucis", "ruminations", "LE RENDEZ-VOUS DES SOUCIS", [
    H1("Le rendez-vous des soucis"),
    T("<p>Pourquoi les soucis attendent-ils toujours le moment où tu poses la tête sur l'oreiller ? Parce que c'est souvent le <strong>premier moment de la journée</strong> où rien d'autre ne les occupe. Ton cerveau profite du calme pour « faire le point », au pire moment.</p>"
      "<p>Le rendez-vous des soucis consiste à lui offrir ce moment plus tôt, à une heure choisie, pour qu'il n'ait plus besoin de le réclamer la nuit.</p>"),
    H2("Pourquoi ça marche"),
    T("<p>Une préoccupation revient tant que le cerveau a l'impression qu'elle n'est « pas traitée ». L'écrire, et surtout noter <strong>une prochaine petite étape</strong>, lui envoie le signal inverse : c'est pris en charge. Des chercheurs en psychologie du sommeil ont observé que cet exercice, fait en début de soirée, réduisait l'agitation mentale au moment du coucher chez des personnes qui avaient du mal à s'endormir.</p>"),
    IMG("notebook pen table late afternoon light", "Carnet et stylo sur une table en fin d'après-midi"),
    H2("L'exercice : 15 minutes, en fin d'après-midi"),
    T("<ol><li><strong>Choisis ton heure</strong>, idéalement entre 17 h et 20 h, et jamais au lit. Assieds-toi avec la fiche « Le rendez-vous des soucis » du kit, ou une simple feuille.</li>"
      "<li><strong>Écris tout ce qui te préoccupe</strong>, en vrac : gros et petits soucis.</li>"
      "<li>Pour chacun, demande-toi : <strong>puis-je agir ?</strong> Oui, non, ou en partie.</li>"
      "<li>Si oui, note <strong>la prochaine petite étape</strong> (pas la solution complète) et quand tu la feras.</li>"
      "<li>Si non, écris « je laisse ça de côté pour l'instant », et ce qui pourrait t'aider à le porter (en parler à quelqu'un, attendre une information…).</li>"
      "<li><strong>Ferme la feuille</strong> et range-la. Le rendez-vous est terminé.</li></ol>"),
    H2("Et si ça revient au lit ?"),
    T("<p>Ça arrivera, surtout au début. Ne discute pas avec la pensée. Dis-toi simplement : <strong>« C'est noté. J'y reviendrai demain, à mon rendez-vous. »</strong> Puis ramène ton attention sur ta respiration ou ton corps. Avec les jours, ton cerveau apprend que les soucis ont leur place, et que ce n'est pas la nuit.</p>"),
    BL(["Fais-le au moins 5 jours d'affilée avant de juger",
        "15 minutes maximum : c'est un rendez-vous, pas une réunion de crise",
        "Les jours calmes, une liste de 3 lignes suffit"], "calendar-check"),
    REF(("Fiche à imprimer : le rendez-vous des soucis (PDF)", "03-rendez-vous-des-soucis.pdf"), KIT_COMPLET),
])

add("liste-de-demain", "ruminations", "LA LISTE DE DEMAIN : 5 MINUTES D'ÉCRITURE AVANT DE DORMIR", [
    H1("La liste de demain : 5 minutes d'écriture avant de dormir"),
    T("<p>Tu connais ce moment : lumière éteinte, et soudain, « il ne faut pas que j'oublie d'appeler… », « demain je dois… ». Les tâches à venir font partie des pensées qui tiennent le plus éveillé, parce que le cerveau essaie de les garder en mémoire pour ne pas les perdre.</p>"),
    H2("Ce qu'a montré une étude"),
    T("<p>En 2018, des chercheurs de l'université Baylor, aux États-Unis, ont demandé à des volontaires d'écrire pendant 5 minutes avant de dormir. Un groupe notait ce qu'il avait accompli dans la journée, l'autre ce qu'il devait faire les jours suivants. Résultat : ceux qui écrivaient leur liste de choses à faire <strong>s'endormaient plus vite</strong>, et d'autant plus vite que leur liste était précise.</p>"
      "<p>L'explication la plus probable : une fois écrite, la tâche n'a plus besoin d'être « maintenue » dans ta tête.</p>"),
    IMG("handwritten to do list notebook bedside lamp", "Liste écrite à la main sur une table de nuit"),
    H2("L'exercice, juste avant de dormir"),
    T("<ol><li>Prends la fiche « La liste de demain » ou une feuille, et un stylo (pas ton téléphone).</li>"
      "<li>Écris <strong>tout ce que tu dois faire demain</strong>, puis les jours suivants.</li>"
      "<li>Sois <strong>précis(e)</strong> : « appeler le garagiste à 9 h pour le rendez-vous » plutôt que « voiture ».</li>"
      "<li>Pas besoin de trier ni de trouver de solutions : tu poses, c'est tout.</li>"
      "<li>Laisse la feuille et le stylo sur ta table de nuit. Si une idée revient dans la nuit, note-la en deux mots.</li></ol>"),
    H2("La différence avec le rendez-vous des soucis"),
    T("<p>Le rendez-vous des soucis se fait plus tôt et s'occupe des <strong>préoccupations</strong> (ce qui t'inquiète). La liste de demain se fait au coucher et vide les <strong>tâches</strong> (ce que tu dois faire). Les deux se complètent très bien.</p>"),
    BL(["Stylo et papier, pas d'écran",
        "5 minutes, pas plus",
        "Plus la liste est précise, mieux c'est"], "pen"),
    REF(("Fiche à imprimer : la liste de demain (PDF)", "04-liste-de-demain.pdf"), KIT_COMPLET),
])

add("melange-cognitif", "ruminations", "LE MÉLANGE COGNITIF : QUAND LES PENSÉES TOURNENT AU LIT", [
    H1("Le mélange cognitif : quand les pensées tournent au lit"),
    T("<p>Parfois, les pensées tournent si vite qu'aucune respiration ne suffit. Il existe alors une astuce étonnante, imaginée par le chercheur canadien Luc Beaudoin : occuper ton esprit avec des images <strong>sans lien entre elles</strong>, un peu comme le cerveau le fait naturellement juste avant de s'endormir.</p>"),
    H2("Pourquoi ça marche"),
    T("<p>Au moment de l'endormissement, les pensées deviennent décousues : des images sans logique se succèdent. Les ruminations, elles, sont l'inverse : logiques, enchaînées, tournées vers un problème. Le mélange cognitif imite l'état d'endormissement et prend la place des ruminations, sans effort ni émotion.</p>"),
    IMG("soft abstract floating objects dreamlike night", "Images douces et flottantes, comme dans un demi-sommeil"),
    H2("L'exercice"),
    T("<ol><li>Choisis un mot neutre d'au moins 5 lettres, sans charge émotionnelle, par exemple <strong>JARDIN</strong>.</li>"
      "<li>Prends la première lettre, J. Pense à un mot qui commence par J (jonquille) et <strong>imagine-le quelques secondes</strong> : sa couleur, sa forme.</li>"
      "<li>Passe à un autre mot en J, sans lien avec le précédent (jouet, jumelles, jus d'orange…), et imagine-le aussi.</li>"
      "<li>Quand tu n'as plus d'idées, passe à la lettre suivante, A (ananas, avion, arrosoir…).</li>"
      "<li>Continue tranquillement. Si tu perds le fil, reprends où tu veux : il n'y a aucun score.</li></ol>"),
    H2("Les règles d'or"),
    BL(["Choisis des objets neutres ou agréables, jamais liés à tes soucis",
        "Prends le temps d'imaginer chaque image, ne récite pas une liste",
        "Si une rumination revient, retourne simplement à ta lettre",
        "Change de mot chaque soir pour ne pas t'ennuyer"], "shuffle"),
])

add("distance-pensee", "ruminations", "PRENDRE DE LA DISTANCE AVEC UNE PENSÉE", [
    H1("Prendre de la distance avec une pensée"),
    T("<p>« Je n'arriverai jamais à dormir. » « Demain sera une catastrophe. » La nuit, certaines pensées paraissent absolument vraies. Le problème n'est pas d'avoir ces pensées : tout le monde en a. Le problème, c'est de <strong>se coller à elles</strong>, comme si elles étaient des faits.</p>"
      "<p>Cette leçon t'apprend à les regarder passer plutôt qu'à les suivre. C'est une approche issue de la thérapie d'acceptation et d'engagement, très utile contre les ruminations.</p>"),
    H2("Pourquoi lutter ne marche pas"),
    T("<p>Essaie de ne pas penser à un éléphant rose… Plus on repousse une pensée, plus elle revient. La nuit, c'est pareil : « arrête de penser ! » garde le mental en alerte. L'idée n'est pas de chasser la pensée, mais de <strong>changer ta relation avec elle</strong>.</p>"),
    IMG("autumn leaves floating on calm stream", "Feuilles qui flottent sur un ruisseau calme"),
    H2("3 façons de prendre de la distance"),
    T("<p><strong>1. Ajouter « j'ai la pensée que… »</strong><br>Au lieu de « je vais être épuisé demain », dis-toi : « <strong>je remarque que j'ai la pensée</strong> que je vais être épuisé demain ». La phrase n'a pas changé, mais tu n'es plus dedans : tu la regardes.</p>"
      "<p><strong>2. Nommer ce qui se passe</strong><br>Donne un nom simple à ce qui tourne : « tiens, le scénario catastrophe », « ah, la liste des choses à faire ». Nommer, c'est déjà reprendre un peu de recul.</p>"
      "<p><strong>3. Les feuilles sur le ruisseau</strong><br>Les yeux fermés, imagine un petit ruisseau où flottent des feuilles. Chaque fois qu'une pensée arrive, pose-la sur une feuille et regarde-la s'éloigner au fil de l'eau. Tu n'as ni à la pousser, ni à la retenir.</p>"),
    H2("Ce qui compte vraiment"),
    BL(["Le but n'est pas de faire disparaître la pensée, mais de ne plus la suivre",
        "Sois doux(ce) avec toi : se faire happer est normal, revenir est l'exercice",
        "Quelques minutes suffisent, au lit ou dans la journée",
        "Plus tu t'entraînes le jour, plus c'est facile la nuit"], "feather"),
    T("<p>Si une pensée revient sans cesse sur un vrai problème à régler, note-la pour ton prochain <strong>rendez-vous des soucis</strong> : elle y sera mieux traitée qu'à 2 h du matin.</p>"),
])

# ---------------- Rituel du soir ----------------

add("preparer-le-corps", "rituel", "PRÉPARER LE CORPS : LUMIÈRE, CHALEUR, ÉCRANS, CAFÉINE", [
    H1("Préparer le corps : lumière, chaleur, écrans, caféine"),
    T("<p>Le sommeil ne commence pas au moment où tu te couches : il se prépare dans les heures qui précèdent. Quelques réglages simples aident ton corps à comprendre que la nuit arrive. Pas besoin de tout appliquer : choisis ce qui est facile pour toi.</p>"),
    H2("1. La lumière : baisser pour préparer"),
    T("<p>La lumière est le signal le plus puissant pour ton horloge interne. Une lumière forte le soir retarde la mélatonine, l'hormone qui prépare au sommeil. <strong>Une heure avant le coucher</strong>, passe en lumières douces et basses : lampe d'appoint plutôt que plafonnier, lumière chaude plutôt que blanche.</p>"),
    H2("2. La chaleur : une douche chaude, une chambre fraîche"),
    T("<p>Pour s'endormir, la température interne du corps doit baisser un peu. Paradoxalement, une <strong>douche ou un bain chaud 1 à 2 heures avant le coucher</strong> aide : le sang afflue vers la peau, puis le corps se refroidit plus vite ensuite. Côté chambre, vise une pièce <strong>fraîche, autour de 18 °C</strong>, avec une couette adaptée.</p>"),
    IMG("cozy dim bedroom warm lamp evening", "Chambre tamisée avec une lampe chaude le soir"),
    H2("3. Les écrans : moins pour la lumière que pour le mental"),
    T("<p>Le problème des écrans le soir n'est pas seulement leur lumière : c'est surtout ce qu'ils contiennent. Messages, actualités et réseaux sociaux relancent le mental au moment où il devrait ralentir. Si tu ne peux pas t'en passer, choisis un contenu calme et connu, et fixe une <strong>heure de fin</strong>, par exemple 30 minutes avant de te coucher. Le téléphone dort mieux <strong>hors de la chambre</strong>, ou au moins hors de portée de main.</p>"),
    H2("4. Caféine, alcool, repas, sport"),
    BL(["Caféine (café, thé, cola, boissons énergisantes) : plutôt avant 14 h, ses effets durent plusieurs heures",
        "Alcool : il aide parfois à s'endormir, mais rend la seconde partie de la nuit plus agitée",
        "Dîner : ni trop copieux ni trop tard, idéalement 2 à 3 heures avant le coucher",
        "Sport : excellent pour le sommeil, mais plutôt pas dans l'heure qui précède le coucher"], "mug-hot"),
    T("<p><strong>Cette semaine :</strong> choisis <strong>un seul</strong> de ces réglages et tiens-le 7 jours. Les petits changements tenus dans le temps valent mieux qu'une révolution abandonnée au bout de trois jours.</p>"),
])

add("rituel-3-versions", "rituel", "TON RITUEL EN 3 VERSIONS : 3, 10 OU 20 MINUTES", [
    H1("Ton rituel en 3 versions : 3, 10 ou 20 minutes"),
    T("<p>Un rituel du soir fonctionne par la <strong>répétition</strong> : à force, ton cerveau associe ces gestes à l'arrivée du sommeil, et commence à ralentir dès les premières étapes. Le piège, c'est de construire un rituel parfait… que tu abandonnes les soirs de fatigue, justement ceux où tu en aurais le plus besoin.</p>"
      "<p>La solution : <strong>trois versions du même rituel</strong>, pour que tu aies toujours une option possible.</p>"),
    H2("Version 3 minutes : les soirs d'épuisement"),
    T("<ul><li>Lumières baissées, téléphone hors de la chambre</li>"
      "<li>5 soupirs physiologiques, allongé(e)</li>"
      "<li>Une phrase, à voix basse ou dans ta tête : « Je n'ai rien à réussir cette nuit. »</li></ul>"),
    H2("Version 10 minutes : les soirs ordinaires"),
    T("<ul><li>1 heure avant : lumières douces, écrans en pause</li>"
      "<li>La liste de demain (3 minutes)</li>"
      "<li>Relâchement musculaire progressif, version courte (4 minutes)</li>"
      "<li>Au lit : respiration lente, 4 temps d'inspiration et 6 d'expiration (3 minutes)</li></ul>"),
    IMG("calm evening ritual herbal tea book soft light", "Rituel du soir calme avec une tisane et un livre"),
    H2("Version 20 minutes : les soirs agités"),
    T("<ul><li>Une douche chaude, 1 à 2 heures avant le coucher</li>"
      "<li>Le rendez-vous des soucis, si tu ne l'as pas fait dans la journée</li>"
      "<li>5 minutes d'étirements doux (nuque, épaules, dos)</li>"
      "<li>Au lit : le scan corporel (10 minutes)</li></ul>"),
    H2("Comment t'y tenir"),
    BL(["Décide le matin quelle version tu vises, ajuste le soir selon ton énergie",
        "Garde toujours le même début (par exemple baisser les lumières) : c'est le signal",
        "Coche chaque soir sur la fiche du kit, quelle que soit la version",
        "Crée ta propre version : c'est la tienne qui marchera le mieux"], "list-check"),
    REF(("Fiche à imprimer : ton rituel en 3 versions + suivi 4 semaines (PDF)", "06-rituel-du-soir-3-versions.pdf"), KIT_COMPLET),
])

# ---------------- Consolider le sommeil dans le temps ----------------

add("reveil-3h", "consolider", "RÉVEILLÉ À 3 H DU MATIN : QUE FAIRE ?", [
    H1("Réveillé à 3 h du matin : que faire ?"),
    T("<p>Tu ouvres les yeux, il fait nuit, et tu sais déjà que tu ne vas pas te rendormir facilement. Le mental s'allume, les calculs commencent : « s'il est 3 h et que je me lève à 7 h… ». C'est l'un des moments les plus difficiles, et l'un de ceux où quelques bons réflexes changent le plus les choses.</p>"),
    H2("D'abord : se réveiller la nuit est normal"),
    T("<p>Une nuit est faite de plusieurs cycles de sommeil d'environ 90 minutes. Entre deux cycles, il est normal de se réveiller brièvement, souvent sans s'en souvenir. Ce qui transforme ce micro-réveil en longue insomnie, c'est surtout <strong>l'inquiétude</strong> qui s'y accroche : regarder l'heure, calculer, se dire que la journée est fichue.</p>"),
    IMG("bedside table alarm clock turned away night", "Table de nuit la nuit, réveil tourné vers le mur"),
    H2("Le protocole, dans l'ordre"),
    T("<ol><li><strong>Ne regarde pas l'heure.</strong> Tourne ton réveil vers le mur, laisse ton téléphone loin du lit.</li>"
      "<li><strong>Dédramatise :</strong> « Je me suis réveillé(e), ça arrive. Je peux me reposer, même sans dormir tout de suite. »</li>"
      "<li><strong>5 soupirs physiologiques</strong>, puis relâche la mâchoire, les épaules, le ventre et les mains.</li>"
      "<li><strong>Si les pensées tournent :</strong> le mélange cognitif, ou « c'est noté, j'y penserai demain ». Si c'est une tâche, note-la en deux mots sur ta liste.</li>"
      "<li><strong>Si tu es bien réveillé(e) et agacé(e) depuis un long moment :</strong> lève-toi. Va dans une autre pièce, lumière douce, activité calme (lecture papier, respiration). <strong>Reviens te coucher quand tes paupières sont lourdes.</strong></li></ol>"),
    H2("Pourquoi se lever ?"),
    T("<p>Rester des heures au lit à lutter apprend à ton cerveau que le lit est un lieu d'éveil et d'agacement. Te lever quand tu n'y arrives plus, puis revenir quand la somnolence est là, lui réapprend peu à peu que le lit, c'est pour dormir. C'est l'un des piliers des approches recommandées contre l'insomnie. Au début, tu te lèveras peut-être souvent : c'est normal, et ça diminue avec les semaines.</p>"),
    BL(["Pas d'écran pendant ce temps : la lumière et le contenu réveillent",
        "Le lendemain, pas de longue sieste pour « rattraper » (20 minutes maximum, avant 15 h)",
        "Lève-toi à ton heure habituelle, même après une mauvaise nuit",
        "Garde la fiche SOS du kit sur ta table de nuit"], "moon"),
    REF(("Fiche SOS à garder sur la table de nuit (PDF)", "05-sos-reveil-nocturne.pdf"), KIT_COMPLET),
])

add("le-matin", "consolider", "LE MATIN COMPTE AUTANT QUE LE SOIR", [
    H1("Le matin compte autant que le soir"),
    T("<p>On pense souvent que le sommeil se joue le soir. En réalité, <strong>ta nuit commence le matin</strong> : c'est au réveil que ton horloge interne se règle pour la journée, et donc pour l'heure à laquelle tu auras sommeil le soir.</p>"),
    H2("1. Une heure de lever régulière"),
    T("<p>C'est le réglage le plus efficace, et le plus sous-estimé. Te lever à peu près <strong>à la même heure chaque jour, week-end compris</strong> (à une heure près), stabilise ton horloge interne. Après une mauvaise nuit, la tentation est de rester au lit : résiste, c'est justement ce qui prépare une meilleure nuit suivante.</p>"),
    H2("2. La lumière du jour, le plus tôt possible"),
    T("<p>La lumière naturelle du matin est le signal qui dit à ton corps « la journée commence ». Elle lance aussi le compte à rebours vers le sommeil du soir. Vise <strong>10 à 30 minutes dehors</strong>, ou près d'une fenêtre, dans l'heure qui suit ton lever, même par temps gris : la lumière extérieure reste bien plus forte que celle d'une pièce.</p>"),
    IMG("morning sunlight window calm person coffee", "Lumière du matin près d'une fenêtre"),
    H2("3. Bouger dans la journée"),
    T("<p>Une activité physique régulière aide à s'endormir plus facilement et à mieux dormir. Pas besoin de sport intensif : une marche de 20 à 30 minutes compte. Idéalement en journée, et plutôt pas dans l'heure qui précède le coucher.</p>"),
    H2("4. Les siestes, avec modération"),
    T("<p>Une courte sieste peut aider, mais une sieste longue ou tardive « consomme » la pression de sommeil dont tu as besoin le soir. Si tu fais la sieste : <strong>20 minutes maximum, avant 15 h</strong>.</p>"),
    H2("Ton journal du sommeil"),
    T("<p>Pour voir ce qui marche pour toi, remplis le journal du sommeil du kit <strong>chaque matin, en une minute</strong>, pendant 14 jours. Au bout d'une semaine, regarde les soirs où tu étais le plus calme : qu'avais-tu fait ? C'est souvent là que se trouve ta meilleure piste.</p>"),
    REF(("Fiche à imprimer : journal du sommeil, 14 jours (PDF)", "02-journal-sommeil-14-jours.pdf"), KIT_COMPLET),
])

add("quand-consulter", "consolider", "QUAND EN PARLER À UN PROFESSIONNEL DE SANTÉ", [
    H1("Quand en parler à un professionnel de santé"),
    T("<p>Ce programme propose des outils de bien-être pour apaiser le stress et le mental du soir. Il ne remplace pas un avis médical. Certaines situations méritent d'en parler à ton médecin traitant, et ce n'est ni un échec ni une exagération : c'est prendre soin de toi.</p>"),
    H2("Les signaux qui justifient une consultation"),
    BL(["Des nuits difficiles au moins 3 fois par semaine depuis plus de 3 mois, avec de la fatigue ou de l'irritabilité dans la journée",
        "Un ronflement fort avec des pauses de respiration remarquées par quelqu'un, ou des réveils en manquant d'air",
        "Une somnolence importante dans la journée, surtout au volant",
        "Des sensations désagréables dans les jambes le soir, qui obligent à bouger",
        "Un moral durablement bas, une perte d'envie, ou une anxiété qui envahit tes journées"], "user-doctor"),
    T("<p>Parles-en aussi si ton sommeil a changé depuis la prise d'un traitement, ou si ton score d'auto-évaluation ne baisse pas après 4 semaines de pratique.</p>"),
    IMG("calm conversation doctor patient office", "Échange calme avec un professionnel de santé"),
    H2("Ce qui existe"),
    T("<p>Pour l'insomnie qui dure, les recommandations médicales placent en première intention la <strong>thérapie cognitive et comportementale de l'insomnie (TCC-I)</strong>, pratiquée par des professionnels formés. Plusieurs techniques de ce programme s'en inspirent : se lever quand on n'arrive pas à dormir, une heure de lever régulière, le travail sur les pensées du soir. Ton médecin peut t'orienter vers un professionnel ou un centre du sommeil.</p>"),
    H2("Si tu vas vraiment mal"),
    T("<p>Si tu as des idées noires ou des pensées de mort, n'attends pas : en France, le <strong>3114</strong>, numéro national de prévention du suicide, est joignable gratuitement, 24 h sur 24 et 7 jours sur 7. En cas d'urgence, appelle le <strong>15</strong> ou le <strong>112</strong>.</p>"),
])

# ---------------- Bien démarrer (1er module) ----------------

add("auto-evaluation", "demarrer", "📊 OÙ EN ES-TU ? TON AUTO-ÉVALUATION", [
    H1("Où en es-tu ? Ton auto-évaluation"),
    T("<p>Avant de commencer, ou maintenant si tu as déjà commencé, prends 2 minutes pour faire une photo de tes soirées. Dans quelques semaines, tu pourras comparer et voir le chemin parcouru, même quand ton impression du moment est floue.</p>"),
    H2("Les 6 questions"),
    T("<p>Pense aux <strong>7 derniers jours</strong> et note chaque phrase de 0 à 4 : <strong>0</strong> jamais, <strong>1</strong> rarement, <strong>2</strong> parfois, <strong>3</strong> souvent, <strong>4</strong> presque toujours.</p>"
      "<ol><li>Le temps pour m'endormir me paraît long.</li>"
      "<li>Je me réveille la nuit et j'ai du mal à me rendormir.</li>"
      "<li>Les pensées tournent en boucle quand je me couche.</li>"
      "<li>Je sens mon corps tendu le soir (mâchoire, épaules, ventre).</li>"
      "<li>J'appréhende le moment d'aller me coucher.</li>"
      "<li>Je me sens fatigué(e) ou irritable dans la journée.</li></ol>"
      "<p>Additionne tes points : tu obtiens un score sur 24. Note-le avec la date.</p>"),
    IMG("notebook checklist pencil calm morning", "Carnet, check-list et crayon"),
    H2("Quand la refaire"),
    BL(["Aujourd'hui : c'est ton point de départ",
        "Au jour 14 : à mi-parcours du plan des 4 semaines",
        "Au jour 28 : pour mesurer le chemin parcouru"], "calendar"),
    H2("Comment lire ton score"),
    T("<p>Ce score est un <strong>repère personnel</strong>, pas un diagnostic. Ce qui compte, c'est son évolution : s'il baisse, tes soirées s'apaisent, même si certaines nuits restent difficiles. Le sommeil progresse rarement en ligne droite.</p>"
      "<p>Si ton score reste élevé après 4 semaines, ou si tes nuits sont difficiles au moins 3 fois par semaine depuis plus de 3 mois, lis la leçon « Quand en parler à un professionnel de santé », dans le module « Consolider le sommeil dans le temps ».</p>"),
    REF(("Fiche à imprimer : l'auto-évaluation, jours 1, 14 et 28 (PDF)", "01-auto-evaluation.pdf"), KIT_COMPLET),
])

add("kit-a-imprimer", "demarrer", "🖨️ TON KIT À IMPRIMER (7 FICHES)", [
    H1("Ton kit à imprimer : 7 fiches"),
    T("<p>Pour t'accompagner au quotidien, voici 7 fiches à imprimer. Elles sont faites pour être remplies au crayon, posées sur ta table de nuit ou collées sur le frigo, pas pour être parfaites.</p>"),
    H2("Ce que contient le kit"),
    T("<ol><li><strong>Où en es-tu ?</strong> L'auto-évaluation, à refaire aux jours 1, 14 et 28.</li>"
      "<li><strong>Journal du sommeil, 14 jours</strong> : une minute chaque matin pour repérer ce qui t'aide.</li>"
      "<li><strong>Le rendez-vous des soucis</strong> : le tableau pour poser tes préoccupations en fin d'après-midi.</li>"
      "<li><strong>La liste de demain</strong> : 5 minutes d'écriture avant de dormir.</li>"
      "<li><strong>Réveillé(e) en pleine nuit ?</strong> La fiche SOS à garder sur ta table de nuit.</li>"
      "<li><strong>Ton rituel du soir en 3 versions</strong>, avec un suivi sur 4 semaines.</li>"
      "<li><strong>Mes 28 soirs</strong> : le parcours soir par soir, une ligne à cocher chaque soir.</li></ol>"),
    IMG("printed worksheets pencil desk calm", "Fiches imprimées et crayon sur un bureau"),
    H2("Comment t'en servir"),
    BL(["Imprime le kit complet une fois, puis réimprime le journal et la liste quand ils sont remplis",
        "Pas d'imprimante ? Recopie-les dans un carnet : ça marche aussi bien",
        "Commence par l'auto-évaluation, la fiche SOS et « Mes 28 soirs »",
        "Tu peux aussi les remplir sur une tablette avec une application d'annotation PDF"], "print"),
    T("<p>Chaque fiche est aussi proposée seule, à la fin de la leçon qui l'explique.</p>"),
    REF(KIT_COMPLET_7, ("Fiche 7 : mes 28 soirs (PDF)", "07-parcours-28-soirs.pdf"), base=KIT2),
])

SOIRS_LECON = [
    ("Semaine 1 : apaiser le corps", [
        "fais ton auto-évaluation (leçon « Où en es-tu ? »), puis 5 soupirs lents au lit.",
        "le soupir physiologique, 3 fois une minute.",
        "le relâchement musculaire progressif, version du soir (5 minutes).",
        "le scan corporel au lit (10 minutes).",
        "refais l'exercice qui t'a le plus apaisé. Dès demain matin, remplis ton journal du sommeil (1 minute).",
        "une heure avant le coucher, passe en lumières douces (leçon « Préparer le corps »).",
        "petit bilan : qu'est-ce qui t'a le plus apaisé cette semaine ? Garde cet exercice comme base."]),
    ("Semaine 2 : laisser passer les pensées", [
        "la liste de demain (5 minutes), puis ton exercice du corps.",
        "ton premier rendez-vous des soucis, en fin d'après-midi (15 minutes).",
        "le mélange cognitif au lit, avec le mot JARDIN.",
        "prendre de la distance : « je remarque que j'ai la pensée que… ».",
        "rendez-vous des soucis dans l'après-midi, liste de demain au coucher.",
        "les feuilles sur le ruisseau (5 minutes).",
        "refais ton auto-évaluation (jour 14) et garde la technique contre les pensées qui te convient le mieux."]),
    ("Semaine 3 : installer ton rituel", [
        "lis « Ton rituel en 3 versions » et choisis la version du soir selon ton énergie.",
        "la version 10 minutes.",
        "une douche chaude 1 à 2 heures avant le coucher et une chambre fraîche.",
        "fixe une heure de fin pour les écrans, 30 minutes avant de te coucher.",
        "la version 3 minutes, même si tu as de l'énergie : c'est le réflexe des soirs difficiles.",
        "la version 20 minutes, idéalement un soir agité ou le week-end.",
        "écris ta version à toi sur la fiche du rituel, et fais le bilan de la semaine."]),
    ("Semaine 4 : consolider", [
        "lis « Réveillé à 3 h du matin » et pose la fiche SOS sur ta table de nuit.",
        "décide ton heure de lever fixe, et prends la lumière du jour demain matin.",
        "ton rituel, plus un exercice contre les pensées si elles tournent.",
        "soir sans effort : la version 3 minutes seulement, et observe ce qui se passe.",
        "relis ton journal : qu'avaient en commun tes 3 meilleurs soirs ?",
        "choisis ton rituel « de base » pour les semaines à venir.",
        "refais ton auto-évaluation (jour 28) et compare avec le jour 1."]),
]


def blocs_soirs():
    blocs, n = [], 0
    for semaine, soirs in SOIRS_LECON:
        items = []
        for action in soirs:
            n += 1
            items.append(f"<li><strong>Soir {n}</strong> : {action}</li>")
        blocs += [H2(semaine), T("<ul>" + "".join(items) + "</ul>")]
    return blocs


add("parcours-28-soirs", "demarrer", "🗓️ TON PARCOURS 28 SOIRS, SOIR PAR SOIR", [
    H1("Ton parcours 28 soirs, soir par soir"),
    T("<p>Tu as maintenant beaucoup d'outils. Pour ne plus te demander chaque soir « qu'est-ce que je fais ce soir ? », voici un chemin tout tracé : <strong>une seule action par soir, 5 à 10 minutes</strong>, dans l'ordre. Chaque semaine s'appuie sur la précédente.</p>"
      "<p>Imprime la fiche « Mes 28 soirs » pour cocher au fur et à mesure et noter ton calme au coucher.</p>"),
    IMG("calendar notebook bedside evening calm", "Carnet et calendrier sur une table de nuit, le soir"),
    *blocs_soirs(),
    H2("Si tu rates un soir"),
    BL(["Reprends simplement le lendemain, sans chercher à rattraper",
        "Soir très difficile : lance l'audio express, et c'est tout pour ce soir",
        "Semaine chargée ? Étale-la sur 10 jours : l'ordre compte plus que la vitesse",
        "Au soir 28, compare ton auto-évaluation avec celle du soir 1"], "calendar-check"),
    T("<p>À la fin du parcours, écris-moi à yavo88@hotmail.com pour me dire ce qui a changé : ton retour m'aide à améliorer le programme.</p>"),
    REF(("Fiche 7 : mes 28 soirs, à cocher (PDF)", "07-parcours-28-soirs.pdf"), KIT_COMPLET_7, base=KIT2),
])

if __name__ == "__main__":
    for l in LECONS:
        json.dump(l, open(os.path.join(OUT, l["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(LECONS), "leçons")
