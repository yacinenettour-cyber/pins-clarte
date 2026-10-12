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
