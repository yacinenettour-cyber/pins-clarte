# Architecture technique — pipeline de publication

## Deux flux de contenu, non connectés entre eux

### Flux actif : texte → image (`pins.yml`, `videos.yml`)

C'est le flux réellement utilisé aujourd'hui. Le texte (titre, description, phrase d'accroche) est déjà écrit à l'avance dans `pins.json` / `videos.json`. À chaque exécution, le script choisit le prochain élément non publié, lui associe une image (fond existant, fond généré par IA, ou image prête fournie), et publie.

### Flux préparé mais pas encore branché : image → texte (`prompts/system-prompt-pin-seo.md`)

Un prompt système a été rédigé pour un futur module IA dans un scénario Make.com séparé : Make enverrait une image reçue, et l'IA analyserait l'image pour générer titre/description/mots-clés/hashtags/nom de fichier/texte alt/tableau en JSON. Ce flux n'est pas relié au flux actif — avant de les connecter (les faire cohabiter, ou basculer l'un vers l'autre), il faut une décision explicite du propriétaire du compte.

## Déclenchement

- **Pins** : `.github/workflows/pins.yml`, déclenché 7×/jour (6h07, 8h07, 10h07, 12h07, 14h07, 16h07, 18h07 UTC) par un appel API externe (cron-job.org, gratuit) vers l'endpoint `workflow_dispatch` de GitHub Actions. Le déclencheur natif `schedule` de GitHub Actions n'est **pas** utilisé (retards/oublis possibles sous charge).
- **Vidéos** : `.github/workflows/videos.yml`, prévu pour 1×/jour (~19h37 UTC), même mécanisme cron-job.org, endpoint différent.
- **Mode test** disponible sur les deux workflows (input `mode: test` au lancement manuel) : génère l'image/vidéo sans publier ni consommer d'élément de la banque.

## Étapes du pipeline pins (`pins.yml`)

1. Charge `pins.json` et `historique.json` ; sélectionne le premier pin de `pins.json` dont le titre n'est pas dans `historique.json` (`restants = [p for p in banque if p["titre"] not in faits]`, prend `restants[0]`).
2. **Devine le thème** à partir du **premier hashtag** de la description (fonction `deviner_theme()`), via une table d'alias `THEME_ALIASES` qui fait correspondre des dizaines de hashtags spécifiques aux 9 thèmes officiels. Cas particulier : si le premier hashtag est `#stress` ET que `#travail` figure dans les 3 premiers hashtags → thème `posturesantistress` (sinon `#stress` seul retombe sur `systemenerveux`).
3. Si le pin a un champ `image_prete`, utilise cette image telle quelle (recadrée, sans texte ajouté). Sinon : génère un fond par IA (si `OPENAI_API_KEY` est configuré, modèle `gpt-image-1.5`) ou choisit un fond dans `fonds/` filtré par thème via `fonds_themes.json` (rotation basée sur le nombre de fois où ce thème a déjà utilisé un fond, pour ne pas répéter trop vite), puis incruste la phrase d'accroche (`texte_image`) sur l'image (1000×1500, police Poppins).
4. Génère aussi une courte vidéo (zoom lent + fondu, ffmpeg) à partir de l'image fixe, en plus de l'image — envoyée à Make comme `video_url` si elle est bien accessible en ligne.
5. Tronque la description au besoin (troncature intelligente à une fin de phrase quand possible) pour respecter la limite Pinterest de ~495-500 caractères, en réservant de la place pour les hashtags et, une fois sur deux, une phrase d'enregistrement aléatoire tirée de `PHRASES_ENREGISTRER`.
6. Commit l'image (et la vidéo) dans le dépôt, récupère son URL publique via jsDelivr (CDN qui sert le contenu GitHub), attend qu'elle soit effectivement accessible en ligne avant de continuer.
7. **Détermine le lien de destination** : vide (`""`) si le thème est dans `THEMES_SANS_LIEN` (`alimentation`, `procrastination`), sinon `LIEN_PAGE`.
8. Envoie titre / description / URL image / URL vidéo / lien / thème / ID du tableau Pinterest à `MAKE_WEBHOOK_URL` (webhook Make.com), qui publie réellement sur Pinterest.
9. Ajoute l'entrée à `historique.json` (anti-répétition) et purge les images/vidéos de plus de 30 jours du dépôt.

Le pipeline vidéo (`videos.yml`) suit la même logique avec ses propres fichiers (`videos.json`, `historique_videos.json`, `videos_fonds/`), son propre webhook (`MAKE_WEBHOOK_URL_VIDEO`, scénario Make séparé pour ne pas perturber le scénario image existant), et la même règle `THEMES_SANS_LIEN`.

## Fichiers du dépôt

| Fichier / dossier | Rôle |
|---|---|
| `pins.json` | Banque de textes de pins (titre, texte_image, description, éventuellement image_prete) |
| `historique.json` | Journal des pins déjà publiés (anti-répétition, par titre exact) |
| `videos.json` | Scripts de Video Pins (id, thème, titre, description, beats avec image/texte/durée) |
| `historique_videos.json` | Journal des vidéos déjà publiées (anti-répétition, par id) |
| `fonds/` | Banque de photos de fond réutilisables, triées par thème |
| `fonds_themes.json` | Association fichier de fond → thème |
| `videos_fonds/` | Fonds dédiés aux vidéos (format plus grand) |
| `images/` | Images de pins déjà générées et publiées (purgées après 30 jours) |
| `videos/` | Vidéos de pins déjà générées (à partir d'images fixes, purgées après 30 jours) |
| `images_manuelles/` | Images prêtes fournies directement par l'utilisateur, utilisées telles quelles |
| `videopins/` | Video Pins déjà générées (image de couverture + .mp4) |
| `.github/workflows/pins.yml` | Workflow de publication des pins classiques |
| `.github/workflows/videos.yml` | Workflow de publication des Video Pins |
| `prompts/system-prompt-pin-seo.md` | Prompt système pour un futur module IA Make (flux image→texte, non connecté) |
| `CLAUDE.md` | Résumé opérationnel des règles, chargé automatiquement par Claude Code sur ce dépôt |
| `README.md` | Documentation complète et détaillée du fonctionnement et des règles |

## Secrets GitHub requis

- `MAKE_WEBHOOK_URL` — webhook Make.com pour les pins classiques (mode image)
- `MAKE_WEBHOOK_URL_VIDEO` — webhook Make.com séparé pour les Video Pins (mode vidéo)
- `LIEN_PAGE` — URL de la page de capture de la formation
- `OPENAI_API_KEY` *(optionnel)* — génération de fonds inédits par IA, ~0,05 $/image en qualité `medium`

## Formats

- **Pins classiques** : image verticale 1000×1500 (ratio 2:3)
- **Video Pins** : format 9:16, 1080×1920
- **Descriptions** : corps de texte visé 380-450 caractères, total (corps + hashtags, + éventuelle phrase d'enregistrement) toujours ≤ ~495-500 caractères (limite Pinterest ; troncature automatique intelligente au-delà)
- **Titres** : maximum 100 caractères (troncature stricte dans le script si dépassement)
