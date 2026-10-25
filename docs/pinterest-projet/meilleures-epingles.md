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
