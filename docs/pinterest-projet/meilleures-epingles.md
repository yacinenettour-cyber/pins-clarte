# Épingles qui marchent le mieux : modèles à suivre sans copier (15/10/2026)

**Consigne de l'utilisateur (15/10/2026)** : « Tu regardes les épingles qui fonctionnent le mieux et tu produis des épingles similaires sans copier. »

Source : statistiques Pinterest réelles (Composio `PINTEREST_LIST_PINS`, `include_metrics`, durée de vie), lues le 15/10/2026. À relire chaque mois.

## Constat

| Épingles | Nombre | Impressions (médiane) | Enregistrements moyens |
|---|---|---|---|
| Idea Pins illustrées faites à la main (déc. 2025 – juin 2026) | 153 | 3 775 | 84 |
| Épingles du robot (photo + texte) depuis le 24/09/2026 | 130 | 11 | 0 (3 au total) |

## Top 20 (enregistrements)

| Enr. | Impressions | Titre | Famille |
|---|---|---|---|
| 1 678 | 243 609 | 6 étapes pour débloquer ton mental | méthode |
| 909 | 60 330 | 5 gestes doux pour apaiser le corps dès le matin | exercices |
| 670 | 59 570 | 5 Clés pour Vaincre la Procrastination | méthode (« clés ») |
| 580 | 57 892 | 5 clés pour élever ton énergie | méthode (« clés ») |
| 433 | 50 401 | La formule anti-fatigue mentale pour retrouver ton énergie | méthode |
| 353 | 42 563 | 7 signes d'une glycémie trop élevée | signes |
| 298 | 29 006 | Cortisol élevé : 7 aliments à privilégier | aliments |
| 277 | 73 235 | Si ton cerveau ne s'arrête jamais la nuit | sommeil |
| 276 | 24 507 | 3 postures simples pour calmer le stress en quelques minutes | exercices |
| 258 | 18 175 | 3 gouttes d'huile essentielle pour s'endormir vite | sommeil |
| 256 | 26 558 | Les priorités essentielles pour aller mieux | méthode |
| 255 | 18 482 | Cortisol élevé : 7 aliments anti-stress | aliments |
| 243 | 22 802 | 9 priorités essentielles pour aller mieux au quotidien | méthode |
| 198 | 18 126 | Les aliments qui calment le système nerveux naturellement | aliments |
| 194 | 15 405 | Technique 4-6 : calme le cœur en 2 min | exercices |
| 183 | 24 586 | 5 douleurs du corps causées par le stress | signes |
| 181 | 22 955 | Quand ton corps dit stop : rééquilibrer l'essentiel | méthode |
| 175 | 17 893 | 9 habitudes qui sabotent ton énergie | signes |
| 170 | 12 359 | 30 min de soleil : ce que ça change vraiment | méthode |
| 160 | 11 635 | 5 étapes pour calmer un mental le soir | méthode |

## Ce qui revient

- **Titre à chiffre et liste** : « 5 clés », « 6 étapes », « 7 signes », « 9 habitudes ».
- **Visuel illustré doux**, jamais une photo : aquarelle ou illustration, une icône ou un pictogramme par point, un cadre décoratif, une invitation à enregistrer en bas (« Sauvegarde ces clés… », « À sauvegarder… »).
- **Description** : commence souvent par « Sauve cette épingle pour… ».
- **Familles** : exercices et gestes, méthodes (clés, étapes, priorités), signes (du corps, de la fatigue), aliments.

## Règles pour produire des épingles similaires sans copier

1. Garder la **forme** (famille, structure à chiffre, visuel illustré), jamais le **sujet** d'une épingle publiée : `outils/anti_doublons.py` + relecture des sujets à la main.
2. Contenu exact et prudent (règles du CLAUDE.md) : pas de promesse médicale, les « signes » renvoient à un professionnel ; pour les aliments, ne rien affirmer que les sources ne soutiennent pas (l'article du site sur le cortisol rappelle que les preuves sur l'alimentation sont limitées).
3. Formats disponibles :
   - `exercices` : `outils/planche_exercices.py` (cartes avec pictogramme, consigne précise, phrase de prudence) ;
   - `cles` : `outils/planche_cles.py` (cadre doré, personnage central, 5 clés numérotées avec icône, consigne et « Pour… »). Convient aussi aux « étapes », « priorités » et « signes ».
4. Illustrations : Hugging Face gratuit uniquement, triées à l'œil, propres à chaque épingle (jamais réutilisées).

## Sujets retenus, en attente d'illustrations

15/10/2026 : quota gratuit Hugging Face épuisé (aucune image générée ce jour-là). Sujets vérifiés (anti_doublons.py + relecture
de l'historique, des titres en ligne, de pins.json et des kits), à fabriquer au prochain passage :

- `exercices` — « Yeux fatigués par l'écran : 3 exercices de repos » (thème fatiguementale, sans lien) : regarder au loin
  20 secondes toutes les 20 minutes (règle 20-20-20 de l'American Academy of Ophthalmology), paumes en creux sur les yeux
  fermés 30 secondes sans appuyer, yeux fermés + front et mâchoire relâchés pendant 5 respirations lentes ; prudence :
  « Gêne qui dure ? Parles-en à ton médecin. »
- `cles` — « Lâcher prise : 5 clés pour arrêter de tout contrôler » (thème blocagemental, lien guide avec pont honnête) :
  trier ce qui dépend de toi, viser « bien » plutôt que « parfait », expirer avant de répondre, déléguer une tâche
  entière, donner 10 minutes à un souci puis passer à autre chose.

Écartés car déjà traités : étirements du soir au sol, réveil / matin, couper avec le travail, chambre, colère, dimanche soir.

**18/10/2026** : « Lâcher prise : 5 clés pour arrêter de tout contrôler » fabriquée (`images_cles/lacher-prise-5-cles.jpg`).
Le sujet « yeux fatigués par l'écran » est abandonné : il double « Stress et écrans : 3 techniques oculaires apaisantes »
(non publiée, déjà dans pins.json, « regarder au loin » en commun). Remplacé par « Bas du dos raide : 3 étirements assis
au bureau » (`images_exercices/bas-du-dos-3-etirements-assis.jpg`). `planche_cles.py` accepte maintenant `seuil_centre`
(garder une peau claire : mains, visage) et `hauteur_centre` (rétrécir un personnage aux bras écartés qui toucherait
les colonnes de texte) ; valeurs par défaut inchangées. Quota Hugging Face de nouveau épuisé après 8 images.

**19/10/2026** : stock à 0 épingle illustrée non publiée (« Bas du dos » publiée le 18/10 à 18 h 07, « Lâcher prise »
le 19/10 à 5 h 07, toutes deux vérifiées en ligne sur Pinterest, pas encore de statistiques). Quota gratuit Hugging Face
épuisé dès le premier appel : rien fabriqué. Sujets vérifiés (anti_doublons.py + relecture : « nuque », « mâchoire »,
« mains », « front », « dire non », « hanches », « charge mentale », « hypervigilance » écartés car déjà traités), à fabriquer
au prochain passage :

- `exercices` — « Poignets tendus : 3 étirements au clavier » (posturesantistress, #stress puis #travail) : bras tendu
  devant, paume vers l'avant, tirer doucement les doigts vers soi 15 s ; même bras, paume vers le bas, doigts vers le sol
  15 s ; secouer les mains détendues 10 s ; prudence : « Douleur ou fourmillements ? Parles-en à ton médecin. »
- `cles` — « Pensées négatives : 5 clés pour prendre du recul » (blocagemental, lien guide avec pont vers les ruminations
  du soir) : nommer la pensée (« je remarque que je pense que… »), l'écrire 5 minutes, chercher un fait qui la nuance,
  te parler comme à un ami, changer d'activité 5 minutes. Description : si ces pensées durent ou pèsent, en parler à un
  professionnel.
- Le cadre doré de chaque épingle « clés » doit changer de description (fleurs, feuilles, couleurs) : avec la même graine
  681678, la même description redonnerait exactement le même cadre.

**20/10/2026** : stock à 0. « Poignets tendus : 3 étirements au clavier » fabriquée
(`images_exercices/poignets-3-etirements-clavier.jpg`, posturesantistress, lien guide avec pont vers le soir). Les gestes
prévus (tirer les doigts avec l'autre main, doigts vers le sol) ont été remplacés : le modèle n'arrive pas à dessiner une main
qui en tire une autre ni un poignet plié vers le bas. Gestes retenus, décrits exactement comme sur les images : bras tendus
paumes vers l'avant, paumes jointes devant la poitrine coudes écartés, doigts grands ouverts puis relâchés. Images écartées :
une main posée sur l'épaule sans raison, bras écartés en croix, index pointé, et une silhouette dont le haut des cuisses
paraissait dénudé. Quota Hugging Face de nouveau épuisé après 8 images, avant le cadre doré : l'épingle « clés »
« Pensées négatives : 5 clés pour prendre du recul » (blocagemental, sujet vérifié le 19/10 et revérifié le 20/10 avec
anti_doublons.py) reste à fabriquer au prochain passage. Description de cadre prévue (jamais utilisée) : « Elegant vertical
poster background, warm cream and soft gold watercolor paper, delicate golden ornamental frame border with thin double
lines, small lavender sprigs and pale eucalyptus leaves in the corners, soft peach watercolor blush near the edges,
completely empty center area, no people, no text ».
Vérification Pinterest du 20/10 (PINTEREST_LIST_PINS, chiffres mis à jour le 20/10 à 5 h 09 UTC) : « Lâcher prise »
(600175087890231482) et « Bas du dos » (600175087890222984) sont en ligne, avec 0 impression, 0 enregistrement, 0 clic
pour l'instant (comme toutes les épingles des 18-19/10 : délai habituel des statistiques).

**21/10/2026** : stock à 0. Deux épingles fabriquées avec 6 images Hugging Face (quota gratuit, graine 681678, une seule
image écartée ; quota non épuisé) :

- `cles` — « Pensées négatives : 5 clés pour prendre du recul » (`images_cles/pensees-negatives-5-cles.jpg`, blocagemental,
  lien guide avec pont vers les ruminations du soir, renvoi à un professionnel si les pensées durent ou pèsent). Cadre doré
  avec la description prévue (lavande, eucalyptus, lavis pêche) ; personnage central : femme en pull et pantalon verts,
  assise en tailleur, qui écrit dans un carnet. Le sujet recoupe en partie « Mieux dormir : la technique du nommage des
  pensées » (une clé sur cinq) : accepté, angle de jour et 4 autres clés différentes.
- `exercices` — « Souffle court par le stress : 3 gestes assis » (`images_exercices/souffle-court-3-gestes-assis.jpg`,
  posturesantistress, #stress puis #travail, lien guide avec pont vers le soir). Sujet nouveau (aucune épingle sur le
  souffle court ni les côtes ; proches relus à la main : « Poitrine serrée par le stress : 3 gestes qui desserrent » =
  mains derrière la tête + respiration ventrale, « Respiration et nerf vague : 3 corrections de posture » = posture debout ;
  gestes différents). Gestes décrits exactement comme sur les images : assise, une main sur la cuisse et l'autre bras levé
  bien haut ; mains sur les côtés de la taille, coudes ouverts ; bras croisés, mains sur le haut des bras. Prudence :
  « Gêne qui dure ou douleur ? Parles-en à un médecin. » Image écartée : une première version des bras croisés où la
  silhouette sans encolure ni poignets paraissait dénudée. Le modèle n'a pas dessiné l'inclinaison latérale demandée
  (seulement un bras levé) : la consigne a été adaptée à l'image.
- Contrôles : anti_doublons.py (charger_references + est_doublon) sans doublon pour les deux titres avant insertion ;
  titres 48 et 44 caractères, corps 416 et 417, totaux 493 et 488, 8 hashtags ; visuels relus, aucun texte qui déborde ou
  chevauche. `verifier_banque.py` : 0 doublon pour pins.json, mais 1 doublon ancien dans **videos.json** (« Énergie : 10
  minutes d'escaliers plutôt qu'un café », non publiée, à 0,97 de « Énergie : 2 minutes d'escaliers plutôt qu'un café »
  publiée le 18/10) : le robot la refusera de toute façon ; son retrait de videos.json a été bloqué par les permissions de la
  session et reste à faire (décision de l'utilisateur).
- Vérification Pinterest (PINTEREST_LIST_PINS du tableau « stress au travail », chiffres mis à jour le 21/10 à 13 h 05 UTC) :
  « Poignets tendus : 3 étirements au clavier » (600175087890251207) est en ligne depuis le 20/10 à 10 h 07 UTC, avec le
  lien guide ; 0 impression, 0 clic, 0 enregistrement pour l'instant. Pour comparaison : « Bas du dos » 5 impressions,
  2 clics sur l'épingle ; « Épaules tendues » 5 impressions, 5 clics ; 0 enregistrement et 0 clic sortant partout.

**23-25/10/2026** : rien fabriqué les 23 et 24/10 (limite hebdomadaire d'utilisation de Claude atteinte), stock à 0 depuis le
23/10. Le 25/10 au soir, quota Hugging Face revenu : 3 illustrations faites pour la fiche respiration du site, puis 4 essais
pour les épingles avant un nouvel épuisement du quota. Sujets vérifiés (anti_doublons.py sans doublon ; relecture des titres :
« Épaules tendues », « Dos tendu (sac) », « Bas du dos », « Fin de journée au travail » ont d'autres gestes ; « besoin de
repos » et « dire non sans culpabiliser » ont un autre angle), à terminer au prochain passage :

- `exercices` — « Haut du dos tendu : 3 étirements assis » (posturesantistress, #stress puis #travail, lien guide avec pont
  vers le soir). Images gardées dans le bloc-notes de la session (illus_2510/) : `hautdos-bras-ouverts.webp` (assise, bras
  tendus sur les côtés à hauteur d'épaules, paumes ouvertes → « Ouvrir les bras » : rapprocher doucement les omoplates,
  5 respirations) et `hautdos-torsion-dossier.webp` (assise, un bras posé sur le dossier, l'autre main sur le genou opposé →
  « Tourner vers le dossier » : tourner doucement le buste, 5 respirations de chaque côté). Il manque le 3e geste (essayé :
  « dos rond bras devant » → bras en croix ; « se serrer dans ses bras » → silhouette qui paraît effondrée, écartée ;
  « bras tendus paumes jointes » → index pointé, écarté). Prochain essai : bouts des doigts sur les épaules, coudes levés
  devant (cercles d'épaules). Prudence : « Douleur qui dure ? Parles-en à ton médecin. »
- `cles` — « Culpabilité de se reposer : 5 clés pour souffler » (fatiguementale, sans lien : aucune promesse de guide) :
  noter la pause dans l'agenda ; se rappeler que récupérer fait partie de l'effort ; commencer par 10 minutes sans rien
  produire ; remarquer le « je devrais… » sans lui obéir ; choisir un repos qui recharge (marche, lecture) plutôt que
  l'écran. Cadre doré à décrire autrement que les précédents ; personnage central : femme habillée en vert, assise dans un
  fauteuil avec une tasse.

**26/10/2026** : stock à 0 ; quota gratuit Hugging Face épuisé dès le premier appel (« 0s left ») : rien fabriqué.
Les images du 25/10 (silhouettes aquarelle, `illus_2510/`) ne respectent plus la règle de la personne réaliste : à
refaire. Sujet « Culpabilité de se reposer : 5 clés pour souffler » revérifié (anti_doublons.py : aucun doublon) ; la clé
« choisir un repos qui recharge plutôt que l'écran » recoupe « 3 fausses pauses qui épuisent ton énergie » (publiée) : à
remplacer par « Annoncer ta pause » (« je fais une pause, je reviens à 15 h » ; pour assumer sans te justifier). Prévu :
titre2 « souffler sans culpabiliser » en écriture manuscrite ; personnage central réaliste (« Realistic soft painted
portrait of a woman in her thirties sitting relaxed in a cozy cream armchair, holding a warm cup of tea with both hands,
eyes gently closed… sage green knit sweater… long beige trousers… ») ; cadre doré avec poudre rose et fleurs séchées.

**27/10/2026** : stock à 0 ; quota Hugging Face revenu. « Culpabilité de se reposer : 5 clés pour souffler » fabriquée
(`images_cles/culpabilite-repos-5-cles.jpg`, fatiguementale, sans lien) avec le nouvel outil `outils/planche_riche.py`,
premier visuel qui suit l'analyse du 25/10 : **personne réaliste au centre** (portrait peint réaliste : femme en pull vert
dans un fauteuil crème, tasse de thé, yeux fermés), une vignette aquarelle par clé (agenda, arrosoir et pousse, sablier,
plume, tasse de thé), titre à deux niveaux (capitales Playfair + « 5 clés pour souffler » en Dancing Script), fond papier
crème avec voiles rose poudré et sauge, bandeau sauge « Sauvegarde cette épingle pour… », signature du compte. 6 images
Hugging Face (graine 681678), aucune écartée ; l'horloge de la 5e vignette affichait des chiffres : seule la tasse a été
gardée (recadrage). Format `cles` dans pins.json (le robot ne connaît que `exercices` et `cles` : `riche` demanderait de
modifier pins.yml). Contrôles : anti_doublons.py sans doublon, titre 48 caractères, corps 387, total 465, 8 hashtags ;
`planche_riche.py` vérifie lui-même les débordements et chevauchements (assertions) ; image relue.
Statistiques relues le 27/10 (PINTEREST_GET_PIN_ANALYTICS, 27/09 → 26/10) : chiffres identiques à ceux du 26/10 ci-dessous
(Journée chargée 48 impressions, Bas du dos 7, Pensées négatives 5, Lâcher prise 3, Poignets 3, Souffle court 2 ;
0 enregistrement, 0 clic sortant) : pas encore de données nouvelles.

**28/10/2026** : stock à 0 ; le matin, outil d'images Hugging Face hors service (connecteur déconnecté), épingle faite l'après-midi à la demande de l'utilisateur. « Gestion des émotions : 5 clés pour retrouver ton calme » (`images_cles/gestion-emotions-5-cles.jpg`, systemenerveux, sans lien : aucun article du site ne traite ce sujet, aucune mention du guide), mot-clé en forte hausse sur Pinterest France (+200 % sur un mois, analyse du 27/10). Format `riche` (`planche_riche.py`) déclaré `cles` dans pins.json comme la précédente. Personne réaliste : femme en pull rose poudré, assise, mains sur la poitrine, yeux fermés ; vignettes : cœur avec étiquette vierge, plume, carnet ouvert vierge, baskets sauge, deux tasses de thé. 6 images Hugging Face (graine 681678), aucune écartée. Sujet relu à la main : deux épingles « Gestion des émotions » non publiées (règle des 90 secondes, gestes contre la colère, format photo que le robot ne publie plus) ont une seule clé en commun (« nommer l'émotion ») : accepté. Contrôles : anti_doublons.py sans doublon, titre 54 caractères, corps 392, total 477, 8 hashtags, verifier_banque.py 0 doublon ; visuel relu.

**29/10/2026** : stock à 0. Sujet retenu, relié à l'article le plus vu du site sur Google (`/angoisse-le-matin/`, un tiers
des impressions Search Console) : `cles` (format `riche`) — « Anxiété matinale : 5 clés pour apaiser tes réveils »
(anti_doublons.py : aucun doublon ; relecture à la main : « Angoisse le matin : le rôle de la veille au soir » a un autre
angle ; « Sommeil léger… » écarté, sujet déjà couvert par 4 épingles). Thème `systemenerveux`, champ `article` :
`angoisse-le-matin`. Clés, toutes tirées de l'article (sources Assurance maladie et essai de l'Université de l'Illinois) :
souffle lent (expirer plus longtemps) ; te lever et ouvrir les volets ; bouger quelques minutes ; noter le souci et lui
donner rendez-vous plus tard ; moins de café, pas à jeun. Bandeau : « Sauvegarde cette épingle pour les matins où
l'angoisse se lève avant toi ». Quota Hugging Face épuisé après 2 images, gardées dans le dépôt
(`photos_attente/riche-anxiete-matinale/`, jamais lu par le robot) : `portrait-homme-main-poitrine.webp` (homme assis au
bord du lit, main à plat sur la poitrine, yeux fermés, pyjama vert sauge et beige ; vérifié : mains correctes, habillé,
aucun texte) et `v1-pissenlit.webp` (vignette de la clé « souffle lent »). Restent 4 vignettes à générer au prochain
passage (graine 681678) : « window with wooden shutters wide open and soft golden morning sunlight », « rolled sage green
yoga mat », « closed dusty pink notebook with a pencil lying on top », « white cup of coffee on a saucer with a little
steam » (toutes « Small watercolor illustration of …, isolated on cream paper, no text »).
Statistiques (PINTEREST_GET_PIN_ANALYTICS, 01/10 → 28/10, jours 27-28 encore en traitement) : Bas du dos 14 impressions,
2 clics sur l'épingle ; Pensées négatives 5 / 2 ; Lâcher prise 3 / 1 ; Poignets 3 / 0 ; Souffle court 2 / 1 ;
Culpabilité de se reposer (27/10) et Gestion des émotions (28/10) : pas encore de chiffres. 0 enregistrement et 0 clic
sortant partout.

Statistiques des épingles illustrées du robot (PINTEREST_GET_PIN_ANALYTICS, 27/09 → 25/10, lues le 26/10) :

| Épingle | Publiée | Impressions | Clics sur l'épingle | Enregistrements | Clics sortants |
|---|---|---|---|---|---|
| Journée chargée : 5 clés pour garder ton calme | 15/10 | 48 | 8 | 0 | 0 |
| Bas du dos raide : 3 étirements assis au bureau | 18/10 | 7 | 2 | 0 | 0 |
| Épaules tendues : 3 exercices assis pour les relâcher | 15/10 | 6 | 6 | 0 | 0 |
| Pensées négatives : 5 clés pour prendre du recul | 21/10 | 5 | 2 | 0 | 0 |
| Lâcher prise : 5 clés pour arrêter de tout contrôler | 19/10 | 3 | 1 | 0 | 0 |
| Poignets tendus : 3 étirements au clavier | 20/10 | 3 | 0 | 0 | 0 |
| Souffle court par le stress : 3 gestes assis | 22/10 | 2 | 1 | 0 | 0 |

Top 10 (enregistrements) relu le lundi 26/10 (PINTEREST_GET_TOP_PINS) — 30 jours (26/09 → 25/10) : « 5 gestes doux
pour apaiser le corps dès le matin » 109 enr. / 7 266 impr., « 5 Clés pour Vaincre la Procrastination » 45 / 3 523,
« 6 étapes pour débloquer ton mental » 19 / 1 390, « Cortisol élevé : 7 aliments à privilégier » 16 / 1 061, « La formule
anti-fatigue mentale » 10 / 694, « 9 gestes simples pour retrouver le moral » 9 / 501, « 6 étapes… » (2e version) 8 / 1 269,
« Cortisol élevé ? 8 aliments clés après 40 ans » 8 / 565, « Technique 4-6 » 7 / 422, « 7 signes d'une glycémie trop
élevée » 7 / 477. 90 jours : même tête (327 / 23 727 ; 128 / 10 391 ; 63 / 7 299), puis « Cortisol élevé : 7 aliments à
privilégier », « 9 gestes simples… », « La formule anti-fatigue… », « Technique 4-6 », « Cortisol élevé : 7 aliments
anti-stress », « Cortisol élevé ? 8 aliments clés après 40 ans ». Toutes sont des épingles `IDEA` faites à la main ;
aucune épingle du robot dans le top 10. Le constat du 25/10 tient toujours.

## Statistiques du compte sur 90 jours (lues le 25/10/2026, nouvelles fonctions Composio)

Source : `PINTEREST_GET_ACCOUNT_ANALYTICS` (28/07 → 24/10/2026) et `PINTEREST_GET_TOP_PINS`.

| Quinzaine | Impressions | Enregistrements | Clics sur l'épingle | Clics vers le site |
|---|---|---|---|---|
| fin juillet | 9 380 | 104 | 579 | 4 |
| 1-15 août | 21 584 | 199 | 1 162 | 1 |
| 16-31 août | 20 815 | 198 | 1 137 | 2 |
| 1-15 sept. | 14 484 | 125 | 856 | 2 |
| 16-30 sept. | 21 398 | 187 | 1 224 | 20 |
| 1-15 oct. | 21 702 | 200 | 1 224 | 27 |
| 16-24 oct. (9 j) | 9 556 | 103 | 572 | 8 |

Total 90 jours : 119 479 impressions, 1 116 enregistrements, 65 clics vers le site (vidéos : 560 impressions).

Constats :
- **Presque toutes les impressions et tous les enregistrements viennent des anciennes épingles faites à la main dans
  l'application** (type `IDEA`, déc. 2025 – juin 2026). Top 3 sur 90 jours : « 5 gestes doux pour apaiser le corps dès
  le matin » (23 578 impressions, 324 enregistrements), « 5 Clés pour Vaincre la Procrastination » (10 294 ; 126),
  « 6 étapes pour débloquer ton mental » (7 299 ; 63). Suivent : « Si ton cerveau ne s'arrête jamais la nuit », « La
  formule anti-fatigue mentale », « Cortisol élevé : 7 aliments à privilégier », « Stress et libido », « Comment vaincre
  la procrastination : le guide complet en 5 étapes », « 7 signes d'une glycémie trop élevée », « Fatigue mentale :
  7 signaux que tu ignores », « 7 signes physiques du stress chronique », « Stress qui monte ? 5 gestes rapides »,
  « Cortisol élevé : 5 leviers alimentaires clés », « Les 9 signes d'un cortisol élevé », « 9 gestes simples pour
  retrouver le moral ».
- **Les épingles du robot (type `REGULAR`, publiées par l'API) ne sont presque pas diffusées** : la meilleure des
  30 derniers jours a 48 impressions, 0 enregistrement. Les épingles illustrées du robot ne font pas mieux : « Lâcher
  prise » 2 impressions en une semaine, « Bas du dos » 6, « Poignets tendus » 2.
- **Mais le robot apporte les clics vers le site** : 2 clics par quinzaine avant le 24/09, 20 à 27 depuis (liens vers
  le guide et les articles). La meilleure source de clics est « Réveil à 3h du matin la tête pleine » (4 clics pour
  68 impressions).
- Hypothèse la plus probable (non prouvée) : Pinterest diffuse beaucoup plus les épingles créées dans l'application que
  celles publiées par l'API, quel que soit le visuel. Test proposé à l'utilisateur le 25/10 : publier à la main, dans
  l'application, quelques épingles préparées dans le format gagnant, et comparer au bout de 2 semaines.

**Règle de l'utilisateur (25/10/2026)** : « quand tu crées des épingles infographie, il faut une personne réaliste au
milieu ». Le personnage central des infographies (formats `cles`, `exercices` et tout nouveau format) est désormais
une personne réaliste, façon photo (image générée gratuitement sur Hugging Face, ou photo libre de droits inédite),
et non plus une silhouette aquarelle ou un pictogramme. Toujours habillée, rien de suggestif, pose exacte de ce que
dit le texte, jamais réutilisée d'une épingle à l'autre.

## Ce que montrent les images des 8 meilleures épingles (regardées le 25/10/2026)

Images de référence dans `photos_attente/ref-top*.jpg` (jamais publiées, seulement pour l'analyse).

- **Une personne au centre ou en haut, réaliste et expressive** (portrait peint, visage détaillé, émotion lisible :
  main sur le front, regard pensif, posture assurée). Jamais une silhouette plate, sauf « 5 étirements » (pictogrammes).
- **Une petite vignette illustrée pour chaque point** (tomate Pomodoro, chronomètre, grenouille, check-list, lit, forêt,
  carnet…), à côté du texte du point. Beaucoup de détails : l'image « se lit » en la regardant.
- **Titre sur deux niveaux** : une partie en grandes capitales ou en serif, et le mot-clé en écriture manuscrite ou en
  couleur (« stress chronique », « procrastination », « anti-fatigue », « Glycémie élevée »).
- **Mises en page qui reviennent** : liste numérotée verticale reliée par des flèches ; deux colonnes « Ce que tu
  ressens / Solutions » (✗ et ✓) ; 4 clés autour du personnage + 1 en bas.
- **Palette chaude et douce** (crème, rose poudré, sauge, doré), fond texturé papier ou aquarelle.
- **Bandeau final « Sauvegarde cette épingle pour… »** avec une punaise ou un signet, et souvent « Clarté Mentale |
  Stress & Énergie » en signature.
- À ne pas reprendre : le chiffre « -30 % de cortisol en 5 jours » de l'épingle aliments (promesse non sourcée).

Conséquence pour la fabrication (avec la règle de l'utilisateur du même jour) : personnage central réaliste (portrait
peint réaliste, habillé), une vignette illustrée par point, titre à deux niveaux avec mot-clé manuscrit, bandeau
« Sauvegarde cette épingle pour… » et signature du compte ; texte toujours dessiné par PIL (règle 8 du CLAUDE.md).

**30/10/2026** : « Anxiété matinale : 5 clés pour apaiser tes réveils » terminée (`images_cles/anxiete-matinale-5-cles.jpg`,
systemenerveux, article `angoisse-le-matin`). Les 4 vignettes manquantes (fenêtre aux volets ouverts, tapis de yoga sauge,
carnet rose et crayon, tasse de café) ont été faites avec **Canva** (`mcp__Canva__generate-image`, quota IA mensuel gratuit du
compte Canva Free, rien de payé) après l'épuisement du quota Hugging Face, à la demande de l'utilisateur (« Il n'y a pas que
Hugging Face… regarde les autres connecteurs »). Le connecteur ne rend qu'un aperçu de 200 × 200 px (fichier dans
tool-results) : suffisant pour les vignettes (128 px), pas pour le portrait. Autres connecteurs vérifiés le 30/10 : Claude
Imagine 0 crédit (payant), Higgsfield 0,92 crédit, HeyGen gratuit sans crédit, Figma et OpenAI exclus (CLAUDE.md),
ElevenLabs réservé à la voix. Ordre à suivre : Hugging Face, puis Canva pour les vignettes ; portrait : Hugging Face, sinon
photo libre Unsplash (personne réelle, habillée, licence Unsplash). Titre « 5 clés pour des réveils doux » sur l'image (la
première version ne tenait pas en largeur), corps 395 / 398 caractères, anti_doublons sans doublon, verifier_banque.py
0 doublon, visuel relu.

**30/10/2026 (tâche du matin)** : « Respiration pour dormir : 5 étapes à faire au lit » (`images_cles/respiration-dormir-5-etapes.jpg`,
sommeil, article `respiration-pour-dormir`, format `riche` déclaré `cles`). Étapes reprises de la routine de l'article
(lumière éteinte et main sur le ventre ; respiration 4-6 pendant 5 minutes ; relâcher le corps zone par zone ; scène calme
précise ; encore éveillé après 20 minutes : se lever, conseil INSV cité par l'article). Hugging Face de nouveau disponible :
6 images (graine 681678), aucune écartée : femme allongée en pyjama rose poudré, mains sur le ventre, yeux fermés ;
vignettes lampe de chevet et croissant de lune, plume, couverture sauge pliée, crique, fauteuil avec livre et lampe
(images gardées dans `photos_attente/riche-respiration-dormir/`). Contrôles : anti_doublons.py sans doublon, titre
49 caractères, corps 390 / 381, verifier_banque.py 0 doublon, visuel relu. Stock d'épingles illustrées : 2.

**31/10/2026** : stock à 0. « Fatigue nerveuse : 5 clés pour recharger » (`images_cles/fatigue-nerveuse-5-cles.jpg`, fatiguementale, format `riche` déclaré `cles`), reliée au nouvel article `/fatigue-nerveuse/` (champ `article` + `description_article`), clés reprises de l'article : pauses courtes environ toutes les heures (méta-analyse de Timișoara), au moins 7 heures de sommeil à horaires réguliers (Inserm), marche régulière (méta-analyse de l'université de Géorgie), alléger la charge mentale, consulter si la fatigue dure plusieurs semaines (NHS). Tant que `fatigue-nerveuse` n'est pas dans `ARTICLES_SITE` de `pins.yml` (modification du workflow : accord de l'utilisateur nécessaire), le robot la publiera sans lien avec sa description principale, qui ne promet rien. Hugging Face (graine 681678) : 8 images ; portrait d'une femme en pull rose poudré, assise à un bureau, tasse de thé, yeux fermés ; vignettes verre d'eau citronnée, oreiller et masque de nuit, chemin dans un parc, bateau en papier, porte entrouverte. Écartés : deux stéthoscopes dessinés avec deux paires d'embouts (remplacés par la porte). Images gardées dans `photos_attente/riche-fatigue-nerveuse/`. Contrôles : anti_doublons.py sans doublon (proches relus : « 5 signaux à reconnaître avant l'épuisement nerveux », « 5 signes que ton stress t'épuise » = signes, pas solutions), titre 40 caractères, corps 391 / 403, totaux 475 / 487, verifier_banque.py 0 doublon, visuel relu.
Statistiques (PINTEREST_GET_PIN_ANALYTICS, 01/10 → 30/10, 29-30 encore en traitement) : Culpabilité de se reposer 7 impressions, 2 clics sur l'épingle ; Gestion des émotions 1 / 1 ; 0 enregistrement, 0 clic sortant.

**01/11/2026** : stock à 0 (tâche du matin reprise l'après-midi). « Procrastination du coucher : 5 clés pour aller au lit » (`images_cles/procrastination-coucher-5-cles.jpg`, sommeil, article `procrastination-du-coucher`, clés reprises des 6 solutions de l'article : moment à soi plus tôt, fin d'écran une heure avant (Assurance Maladie), alarme du coucher, rituel court, remplacer le fil d'actualité). Hugging Face (graine 681678) : 6 images, aucune écartée (homme en sweat bleu marine au bord du lit, téléphone en main, lumière de lampe ; vignettes fauteuil et plaid, téléphone retourné et plante, cloche, lampe de chevet, pile de livres), gardées dans `photos_attente/riche-procrastination-coucher/`. Bandeau reformulé (un guillemet se retrouvait seul en début de ligne). Contrôles : anti_doublons.py sans doublon (proche relu : « Heure du coucher : 4 signes que tu dors trop tard », autre angle), titre 53 caractères, corps 407 / 385, totaux 492 / 470, verifier_banque.py 0 doublon, visuel relu. Statistiques Pinterest non relues ce jour (déjà relues le 31/10).

**02/11/2026** : stock à 0. « Charge mentale à deux : 5 clés pour mieux partager » (`images_cles/charge-mentale-deux-5-cles.jpg`, fatiguementale, sans lien de guide, article `charge-mentale` + `description_article`, format `riche` déclaré `cles`). Clés reprises de l'article (lister ensemble ce qui fait tourner le foyer, confier un domaine entier avec ses étapes, accepter la façon de faire de l'autre, rendre la charge visible avec une liste partagée ou un tableau sur le frigo, menus types et choix par défaut). Images : portrait réaliste Hugging Face (graine 681678 : couple à une table, elle en pull rose poudré écrit, lui en pull bleu marine montre la page ; mains correctes, habillés) et vignette carnet ; quota Hugging Face épuisé ensuite, 4 vignettes faites avec Canva (quota gratuit : clés avec étiquette sauge, deux tasses rose et bleue, frigo avec feuille et aimants, bol de légumes). Images gardées dans `photos_attente/riche-charge-mentale-deux/`. `planche_riche.py` corrigé : le filet doré sous le titre manuscrit traversait les jambages (« p », « g ») ; il se place maintenant sous le titre. Contrôles : anti_doublons.py sans doublon (proche relu : « Charge mentale de Noël : 4 tâches à partager tôt », non publiée, angle Noël), titre 50 caractères, corps 393 / 390, totaux 491 / 488, verifier_banque.py 0 doublon, visuel relu.
Statistiques (PINTEREST_GET_PIN_ANALYTICS, jusqu'au 31/10, 01/11 encore en traitement) : Culpabilité de se reposer 16 impressions, 4 clics sur l'épingle ; Gestion des émotions 10 / 4 ; Respiration pour dormir 5 impressions, 3 clics sur l'épingle, **3 clics sortants** ; Anxiété matinale 6 / 3 ; Fatigue nerveuse 4 impressions, 3 clics, **1 clic sortant** ; 0 enregistrement partout. Les épingles reliées à un article commencent à envoyer des visiteurs vers le site.
Top 10 relu le lundi 02/11 (PINTEREST_GET_TOP_PINS, enregistrements) — 30 jours (03/10 → 01/11) : 600175087885208935 (« 5 gestes doux… ») 89 enr. / 6 479 impr. ; 600175087887334540 (« 5 Clés pour Vaincre la Procrastination ») 37 / 3 435 ; 600175087885878234 20 / 1 429 ; puis 14 / 1 070, 10 / 593, 10 / 953, 9 / 391, 9 / 510, 6 / 271, 6 / 463 (anciennes épingles `IDEA`). 90 jours : même tête (313 / 23 528 ; 116 / 9 794 ; 51 / 6 418). Aucune épingle du robot dans le top 10 : le constat du 25/10 tient toujours.

## Analyse de la baisse (03/11/2026, 20 épingles les plus vues, Composio)

Compte : impressions par jour 1 593 (20-30/09) → 1 003 (27-31/10), soit -37 % ; enregistrements -42 %. Début de la baisse vers le 11/10, pas le 27/10.
Comparaison des 30 jours du 02/10 au 31/10 avec ceux du 02/09 au 01/10 (`PINTEREST_GET_TOP_PINS`, 54 épingles, 29 433 → 23 284 impressions) :
- Les 9 anciens Idea Pins qui ont un lien : 6 509 → 2 523 (-61 %), soit 65 % de la baisse de ces épingles : « 6 étapes pour débloquer ton mental » 2 568 → 629, « Si ton cerveau ne s'arrête jamais la nuit » 1 492 → 729, « La formule anti-fatigue mentale » 1 049 → 318, « Stress qui monte ? 5 gestes rapides » 760 → 133.
- Anciens Idea Pins sans lien : 22 924 → 20 497 (-11 %), dont « 5 gestes doux pour apaiser le corps dès le matin » 9 141 → 6 775 (-26 %) ; les autres sont stables (« 5 Clés pour Vaincre la Procrastination » +28 %, « Cortisol élevé : 7 aliments » +38 %).
- Épingles du robot (depuis le 22/09) : 2 seulement dans le haut du classement, 264 impressions ; elles ne pèsent pas dans la baisse.
- Hypothèse non démontrée : l'ajout d'un lien sur un ancien Idea Pin réduit sa diffusion. À confirmer avec la date exacte où chaque lien a été ajouté (l'analyse jour par jour de l'API est incohérente avec ces totaux pour ces épingles).

**Nouvelle épingle à publier à la main (03/11/2026)** : `kits_idea_pins/9-automassage-visage-nuque/` (`pin.jpg` 1000 × 1780 + `texte.txt`). Même format que le n° 1 du compte (infographie illustrée numérotée, vert sauge, « à enregistrer ») sur un sujet sans doublon : « Auto-massage anti-stress : 5 gestes doux » (visage et nuque ; aucun titre proche dans `pins.json`, `historique.json`, `titres_en_ligne.json` ni les kits). Version avec lien vers la page de capture proposée le 03/11 (objectif : trafic Pinterest vers la page de capture) ; l'utilisateur a choisi de publier sans lien : cette épingle ne peut donc pas amener de clics sortants, elle sert à mesurer la diffusion du format. Illustrations Hugging Face gratuites dans `images_exercices/automassage-*.webp`. À suivre à 7 et 14 jours (impressions, enregistrements).

**Publiée le 03/11/2026 à 04 h 35 UTC** : « Auto-massage anti-stress : 5 gestes doux », pin `600175087890491617` (type IDEA, tableau « Stress et corps : tensions, douleurs & signaux », sans lien, description conforme au kit ; texte alternatif non renseigné). Suivi programmé les 10/11 et 17/11 (impressions, enregistrements, clics).

**Relevé du 03/11/2026 (épingles illustrées du robot, 28/10 → 02/11, `PINTEREST_GET_PIN_ANALYTICS` ; les deux dernières ne sont pas encore comptées par Pinterest)** : Gestion des émotions 10 impressions, 4 clics, 0 enregistrement ; Respiration pour dormir 5 impressions, 3 clics sur l'épingle, **3 clics sortants** (probablement des clics de l'éditeur) ; Anxiété matinale 6 / 3 / 0 ; Fatigue nerveuse 4 / 3 / 1 clic sortant ; Procrastination du coucher et Charge mentale à deux : 0 (données en cours de traitement). Diffusion toujours très faible : 4 à 10 impressions par épingle dans les 3 premiers jours.
**Épingle « Mâchoire serrée : 5 clés pour relâcher » commencée le 03/11** (portrait et 4 vignettes prêts dans `photos_attente/riche-machoire-serree/`, vignette « soupe » à générer le 04/11 : quotas gratuits de Canva et de Hugging Face épuisés le 03/11).

**03/11/2026, décision de l'utilisateur** : l'épingle « Mâchoire serrée : 5 clés qui soulagent » (portrait Hugging Face, 4 vignettes Canva, vignette soupe ElevenLabs) remplace dans la banque « Mâchoire crispée au travail : 3 gestes pour la relâcher » (non publiée, même rang). Elle mène à l'article `machoire-serree-stress` (ou au guide si la part d'articles dépasse 40 %).

**04/11/2026** : stock à 0 (les 15 épingles « clés » sont publiées). Une seule épingle fabriquée, à la demande de l'utilisateur :
`cles` (format `riche`) — « Réveil fatigué : 5 clés pour des matins plus légers » (`images_cles/reveil-fatigue-5-cles.jpg`,
thème `sommeil`, champ `article` : `reveil-fatigue-le-matin`, article tout neuf du même jour). Clés toutes tirées de
l'article : au moins 7 heures de sommeil (Inserm) ; horaires de coucher et de lever proches (NHS) ; pas d'alcool juste avant
de dormir (revue de 2013, seconde moitié de nuit plus agitée) ; reports de réveil sans drame (étude de Stockholm, 31
personnes, 30 min de reports sans effet sur les tests de réflexion) ; poser ses pensées sur papier avant le coucher.
Sujets **écartés** car déjà couverts par une épingle publiée ou en banque : écrans avant de dormir (« Écrans le soir : ce
qui compte vraiment », « Téléphone dans la chambre »…), gestion des émotions (« 5 clés pour retrouver ton calme », « règle
des 90 secondes »), alcool (« Alcool pour décompresser »), décalage du week-end (« Jet lag social »). Rappel : avec
« Cortisol du matin : pourquoi tu te réveilles fatigué » (publiée), le sujet « réveil fatigué » est proche mais l'angle
(leviers du soir) est différent.
Images : portrait Hugging Face (femme en pyjama vert sauge qui s'étire, assise sur le lit, graine 681678 ; vérifié :
habillée, mains correctes, aucun texte) ; 4 vignettes Hugging Face (oreiller et plaid, soleil sur les collines, verre de
vin, masque de sommeil) ; 5e vignette (bougie et carnet) faite avec Canva gratuit, le quota Hugging Face étant épuisé après
5 images. Une vignette écartée : un réveil rose dont le cadran affichait des chiffres. Crédits ElevenLabs : aucun utilisé
(les 4 000 crédits d'images du mois restent intacts : 48 dépensés le 03/11). Images gardées dans
`photos_attente/riche-reveil-fatigue/`.
Contrôles : anti_doublons.py (aucun doublon), titre 51 caractères, corps 403, total 483, 8 hashtags, `verifier_banque.py` :
0 doublon (237 titres) ; image relue, aucun texte qui déborde ni chevauche. Au passage, une phrase de l'article, non
sourcée (« la nuit raccourcit… »), a été remplacée par une formulation neutre.

**05/11/2026** : stock à 0 (l'épingle « Réveil fatigué : 5 clés pour des matins plus légers » a été publiée par le robot le
04/11 à 9 h 08 UTC, avec son lien vers l'article). Une épingle fabriquée : `cles` (format `riche`) — « Hypervigilance : 5 signes
d'un corps en alerte » (`images_cles/hypervigilance-5-signes.jpg`, thème `systemenerveux`, champ `article` :
`hypervigilance`, qui renvoie à l'article et à son pont honnête vers le guide sommeil). Forme « N signes avec renvoi à un
professionnel » plutôt que « clés » : l'article aborde le stress post-traumatique, il ne faut pas proposer de gestes à suivre seul.
Les 5 signes viennent du tableau de l'article (attention qui scrute, sursauts, corps qui s'emballe, irritabilité, sommeil
difficile) ; la description et le bandeau rappellent que ces signes ne suffisent pas à poser un diagnostic.
Sujets **écartés** : « Boule au ventre » (3 épingles déjà publiées : « Ventre noué par le stress », « Ventre noué avant un
rendez-vous », « Boule au ventre au bureau »), Jacobson (« Relaxation au lit : la méthode Jacobson en 4 zones »), burn-out
(« Burn-out : 3 dimensions pour repérer les signes »), symptômes physiques du stress (même sujet qu'un titre publié).
L'épingle de la banque « Système nerveux : 4 exercices contre l'hypervigilance » reste, mais mène à un autre article
(`calmer-son-systeme-nerveux`) avec 4 exercices : angle différent.
Images : portrait Hugging Face (femme en pull rose poudré sur un canapé, regard en alerte, graine 681678 ; vérifié :
habillée, mains correctes, aucun texte) et 5 vignettes Hugging Face (loupe, mésange, cœur, bouilloire, lampe), aucune écartée ;
une petite trace de signature illisible sur la lampe a été effacée pixel par pixel (le contour du pied est intact). Aucun
crédit ElevenLabs ni Canva utilisé. Images gardées dans `photos_attente/riche-hypervigilance/`.
Contrôles : anti_doublons.py (aucun doublon), titre 46 caractères, corps 385, total 469, 8 hashtags ; description d'article 430 ;
`verifier_banque.py` : 0 doublon (237 titres) ; image relue, rien ne déborde ni ne chevauche.
Statistiques relevées le 05/11 (PINTEREST_GET_PIN_ANALYTICS, 03/11 → 04/11, le 04/11 encore en traitement) : « Réveil fatigué :
5 clés pour des matins plus légers » (600175087890511362, publiée le 04/11) : 0 impression, 0 enregistrement, 0 clic ; épingle
faite à la main « Auto-massage anti-stress : 5 gestes doux » (600175087890491617, publiée le 03/11, sans lien) : 1 impression,
1 clic sur l'épingle, 0 enregistrement. Trop tôt pour conclure ; suivis à 7 et 14 jours déjà programmés pour l'auto-massage.

**12/11/2026** : stock à 1 (« Week-end cocooning : 8 idées pour recharger », fiche-mémo non publiée). Une épingle fabriquée :
`cles` (format `riche`) — « Crise d'angoisse la nuit : 5 étapes pour la traverser » (`images_cles/crise-angoisse-nuit-5-etapes.jpg`,
thème `sommeil`, champ `article` : `angoisse-le-soir` + `description_article`). Les 5 étapes reprennent la section « Que faire
pendant une crise d'angoisse la nuit ? » de l'article (sources Assurance maladie, INSV, modèle d'Oxford) : une crise dure en
moyenne 20 à 30 minutes ; respirer lentement par le ventre (4 puis 6) ; lumière douce, changer de pièce si besoin ; ancrage
(nommer ce qu'on voit, entend, touche) ; ne pas bloquer les pensées. Bandeau : « … 1re crise ou douleur dans la poitrine :
appelle le 15 », repris dans les deux descriptions ; description principale (si l'article n'est pas choisi) : pont honnête
vers le guide sommeil. Sujets **écartés** : café (« Café : jusqu'à quelle heure en boire… » publiée, « Café et sommeil :
3 repères » en banque), angoisse du soir en général (anti_doublons : même sujet que « Angoisse du dimanche soir… »), syndrome
de l'imposteur (0,78 de « 3 signes qu'il te freine »), perfectionnisme (« viser 80 % » déjà dans une épingle publiée),
déconnecter du travail, sommeil léger, réveil à 4 h, ruminations (déjà couverts). Proches relus à la main : « Angoisse
nocturne : pourquoi tout paraît plus grave » (publiée, explications), « Fatigue après une crise d'angoisse » (banque, après la
crise), « Sommeil : le geste en 2 temps quand ton cœur cogne » (banque, un seul geste) : angles différents.
Images : 7 appels Hugging Face (graine 681678, quota non épuisé) ; premier portrait (pyjama vert, main sur le ventre) écarté
car le ventre arrondi pouvait faire penser à une grossesse, gardé dans `photos_attente/riche-crise-angoisse-nuit/` sous
`non-utilise-…` ; portrait retenu : femme en pyjama rose poudré, assise en tailleur sur le lit, mains sur la poitrine, yeux
fermés (habillée, mains correctes, aucun texte) ; vignettes vague, moulin à vent, lampe de chevet, galets empilés, nuage.
Aucune image identique à une image existante (empreintes md5). Aucun crédit ElevenLabs ni Canva utilisé.
Contrôles : anti_doublons.py (aucun doublon), titre 53 caractères, corps 400 / 387, totaux 487 / 474, 8 hashtags ;
`verifier_banque.py` : 0 doublon (326 titres) ; image relue, rien ne déborde ni ne chevauche (assertions de `planche_riche.py`).

Statistiques relevées le 12/11 (PINTEREST_GET_PIN_ANALYTICS, compte Composio `pinterest_fluty-blues` — l'autre compte
connecté, `pinterest_caroba-pectic`, répond 401 ; du 01/11 au 11/11, les 10 et 11/11 encore en traitement) :

| Épingle | Publiée | Impressions | Clics sur l'épingle | Enregistrements | Clics sortants |
|---|---|---|---|---|---|
| Auto-compassion : 8 phrases douces à te dire | 08/11 | 37 | 5 | 0 | 0 |
| Fêtes de fin d'année : 8 façons de rester zen | 07/11 | 35 | 4 | 0 | 0 |
| Journaling : 8 questions pour mieux te comprendre | 07/11 | 24 | 4 | 0 | 3 |
| Nature et stress : 8 façons de te reconnecter dehors | 06/11 | 22 | 4 | 0 | 0 |
| Gestion des émotions : ce que chaque émotion te dit | 05/11 | 17 | 5 | 0 | 1 |
| Repos : les 7 types de repos dont tu as besoin | 06/11 | 17 | 3 | 0 | 0 |
| Hypervigilance : 5 signes d'un corps en alerte | 05/11 | 16 | 0 | 0 | 0 |
| Charge mentale à deux : 5 clés pour mieux partager | 02/11 | 14 | 2 | 0 | 0 |
| Réveil fatigué : 5 clés pour des matins plus légers | 04/11 | 14 | 2 | 0 | 1 |
| Procrastination du coucher : 5 clés pour aller au lit | 01/11 | 10 | 2 | 0 | 0 |
| Mâchoire serrée : 5 clés qui soulagent | 03/11 | 9 | 0 | 0 | 0 |
| Calmer le stress par les 5 sens : 8 gestes simples | 09/11 | 1 | 0 | 0 | 0 |
| Confiance en soi : 8 petits gestes pour la nourrir | 10/11 | 0 (pas encore compté) | 0 | 0 | 0 |

Les fiches-mémo à 8 points font un peu mieux que les épingles « 5 clés » dans leurs premiers jours (22 à 37 impressions contre
9 à 17), mais tout reste très faible et sans aucun enregistrement : le constat du 25/10 tient toujours.
