# pins-clarte — contexte pour Claude Code

Ce fichier est chargé automatiquement au démarrage de chaque session Claude Code sur ce dépôt. Le README.md contient le détail complet et le pourquoi de chaque règle — ce fichier n'en est qu'un résumé opérationnel pour ne pas répéter les erreurs déjà corrigées.

## Le compte

"Clarté Mentale | Stress & Énergie" — compte Pinterest francophone centré sur **le stress, la procrastination et le sommeil**, et leurs thèmes associés : `sommeil`, `systemenerveux`, `fatiguementale`, `alimentation`, `procrastination`, `somatisation`, `blocagemental`, `posturesantistress`, `energie` (chacun a son propre board Pinterest — voir `TABLEAUX` dans `.github/workflows/pins.yml`).

Le pipeline (`pins.yml` + `videos.yml`, déclenchés par cron-job.org) publie automatiquement, **sans aucun contrôle de pertinence** : il envoie tel quel le prochain pin non publié de `pins.json` / script de `videos.json`. Toute la responsabilité de cohérence repose sur ce qui est ajouté à ces fichiers — voir la section "Cohérence du contenu" du README avant d'ajouter quoi que ce soit.

## Règles impératives (déjà appliquées, à ne pas régresser)

1. **Zéro duplicata.** Titres et quasi-titres uniques (vérifier avec `difflib.SequenceMatcher`, pas juste l'égalité stricte), images jamais réutilisées à l'identique. Pinterest pénalise le contenu dupliqué.
2. **Cohérence texte + image avec le périmètre du compte** avant tout ajout à `pins.json` — pas de contenu générique (recette, déco...) sans lien explicite avec stress/sommeil/mental. Le thème est déterminé par le **premier hashtag** de la description (`deviner_theme()`), pas par la présence du mot-clé ailleurs dans le texte.
3. **Board `alimentation` ("Alimentation et stress") : uniquement l'angle "l'alimentation diminue le stress".** Jamais sommeil ou énergie seuls sur ce board (ces angles existent déjà via les thèmes `sommeil`/`energie`).
4. **Lien de destination conditionnel.** `LIEN_PAGE` (page de capture d'une formation systeme.io) n'est envoyé à Make que pour les thèmes couverts par la formation. Voir `THEMES_SANS_LIEN` dans `pins.yml`/`videos.yml` : actuellement `alimentation` et `procrastination` sont hors périmètre → `lien` vide pour ces thèmes, et leur CTA ne doit jamais promettre un contenu "dans le guide gratuit" ou inviter à cliquer (rien derrière).
5. **Titres travaillés, descriptions longues et SEO.** Corps de description (hors hashtags) visé entre 380 et 450 caractères, total ≤ 495-500 (limite Pinterest, sinon troncature automatique par le script). Mots-clés naturels, pas de bourrage.
6. **CTA variés, pas systématiques.** Ne jamais répéter la même formule de fin d'un pin à l'autre. Environ un quart des pins peuvent se terminer sans CTA explicite (fin informative).
7. **Ne jamais toucher aux pins déjà publiés** (présents dans `historique.json` par titre exact) — modifier leur texte est sans effet (jamais relu) et changer leur titre risquerait de les faire republier comme "nouveaux".

## Fichiers clés

- `pins.json` : banque de pins (texte). `historique.json` : suivi anti-répétition (titres déjà publiés).
- `videos.json` / `historique_videos.json` : équivalent pour les Video Pins.
- `fonds/` + `fonds_themes.json` : photos de fond par thème.
- `prompts/system-prompt-pin-seo.md` : prompt système pour un futur module IA Make.com (image → métadonnées), flux distinct et pas encore connecté au pipeline actuel (texte → image).

## Avant de considérer une tâche terminée

Toujours revérifier avec un script Python (pas à l'œil) : 0 doublon exact, 0 quasi-doublon, longueurs de titre/description dans les limites, routage de thème/board préservé (premier hashtag inchangé sauf intention explicite), pins déjà publiés intacts. Committer et pousser sur la branche en cours seulement après ces vérifications.
