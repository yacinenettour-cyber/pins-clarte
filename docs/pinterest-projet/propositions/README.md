# Version du robot prête à mettre en ligne (12/10/2026)

`pins-2026-10-12.yml` est le fichier **complet** qui doit remplacer `.github/workflows/pins.yml`
(`pins-2026-10-12.diff` montre les seules différences). Accord de l'utilisateur le 12/10 (« Fais tout toi même ») ;
la mise en ligne depuis la session a été bloquée par une protection automatique : à coller en entier dans l'éditeur
GitHub, ou à pousser depuis une session autorisée. Journal : section 53.

Changements :
1. Plus aucune carte (guide, plan, article) ni pastille « À GARDER » sur l'image ; la photo récupère la place.
   Lien, description et appel au guide dans le texte inchangés.
2. Au moins 3 h 50 entre deux épingles (environ 5 par jour au lieu de 10).
3. Jamais deux épingles du même thème à la suite.
4. Article « Angoisse le soir et la nuit » ajouté à `ARTICLES_SITE` ; part maximale des articles 0,4 → 0,6.

Vérifications : YAML valide, script Python compilé ; rendu de 258 épingles à venir × 2 visuels × 2 formats
(2 064 images) : 0 chevauchement, 0 image sans photo ; simulation de 70 publications : 0 répétition de thème
(18 avec la version actuelle) ; règle de rythme testée (pause à 1,9 h, publication à 3,9 h et 6 h).
Base : `.github/workflows/pins.yml` de main au 12/10/2026 — si `pins.yml` a changé depuis, refaire le diff.

## Visuel « fiche » (12/10/2026, en attente de validation de l'utilisateur)

`pins-fiche-2026-10-12.yml` = robot en ligne + visuel « fiche » pour toutes les épingles à étapes (fin du test
clair/sombre) : papier pastel par thème, accroche manuscrite (Dancing Script), titre Playfair Display, étapes
numérotées en cartes (Lora), photo encadrée sous le texte, invitation discrète à enregistrer, variée.
Polices libres (OFL) dans `polices/`. Aperçu : `apercu-fiche.jpg`.
Vérifications : 253 épingles à venir rendues, 0 chevauchement, 0 ligne trop large, 0 image sans photo,
0 ponctuation seule en début de ligne ; exécution complète du robot en mode test sur une copie du dépôt (code 0).

## Lignes équilibrées sur le visuel « fiche » (18/10/2026, en attente d'autorisation)

`pins-2026-10-18.yml` = `pins.yml` de main au 18/10/2026 + une seule modification : `_couper()` garde le même
nombre de lignes mais cherche la largeur la plus étroite possible (lignes équilibrées). Défaut constaté sur les
22 premières fiches publiées : un mot seul en dernière ligne d'une étape ou du titre (« … sans pouvoir / agir »,
« … qui cherche une / sortie », « … hors de portée du / lit »).
Vérifications : 257 fiches rendues avec les deux versions (fiches déjà publiées et épingles à étapes à venir) : mots seuls en fin de bloc
212 → 7, 0 image sans photo, 0 chevauchement dans les deux versions ; 5 mises en page changent de taille de
titre ou de hauteur de photo, sans dépassement. À coller en entier dans l'éditeur GitHub à la place de
`.github/workflows/pins.yml`, avec l'accord de l'utilisateur ; refaire le diff si `pins.yml` a changé depuis.
