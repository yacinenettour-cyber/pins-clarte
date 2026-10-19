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
