# Architecture technique — pipeline de publication

## Deux flux de contenu, non connectés entre eux

### Flux actif : texte → image (`pins.yml`, `videos.yml`)

C'est le flux réellement utilisé aujourd'hui. Le texte (titre, description, phrase d'accroche) est déjà écrit à l'avance dans `pins.json` / `videos.json`. À chaque exécution, le script choisit le prochain élément non publié, lui associe une image (fond existant, fond généré par IA, ou image prête fournie), et publie.

### Flux préparé mais pas encore branché : image → texte (`prompts/system-prompt-pin-seo.md`)

Un prompt système a été rédigé pour un futur module IA dans un scénario Make.com séparé : Make enverrait une image reçue, et l'IA analyserait l'image pour générer titre/description/mots-clés/hashtags/nom de fichier/texte alt/tableau en JSON. Ce flux n'est pas relié au flux actif — avant de les connecter (les faire cohabiter, ou basculer l'un vers l'autre), il faut une décision explicite du propriétaire du compte.

## Déclenchement

- **Pins** : `.github/workflows/pins.yml`, déclenché 7×/jour (6h07, 8h07, 10h07, 12h07, 14h07, 16h07, 18h07 UTC) par un appel API externe (cron-job.org, gratuit) vers l'endpoint `workflow_dispatch` de GitHub Actions. Le déclencheur natif `schedule` de GitHub Actions n'est **pas** utilisé (retards/oublis possibles sous charge).
- **Vidéos** : `.github/workflows/videos.yml`, 1×/jour (7×/semaine) à 18h30 heure de Paris, même mécanisme cron-job.org, endpoint différent. cron-job.org gère le fuseau `Europe/Paris` directement sur la tâche si l'option est disponible (bascule CEST/CET automatique) ; sinon, régler manuellement 16h30 UTC en été (CEST) et 17h30 UTC en hiver (CET).
- **Mode test** disponible sur les deux workflows (input `mode: test` au lancement manuel) : génère l'image/vidéo sans publier ni consommer d'élément de la banque.

## Étapes du pipeline pins (`pins.yml`)

1. Charge `pins.json` et `historique.json` ; filtre les pins non encore publiés (`restants`), puis choisit le **thème dont la dernière publication est la plus ancienne** (`choisir_pin_equilibre()`, ajouté le 28/09/2026 — remplace l'ancienne sélection naïve `restants[0]` qui pouvait enchaîner des dizaines de pins du même thème quand la banque était remplie par lots thématiques) et prend le premier pin disponible de ce thème.
2. **Devine le thème** à partir du **premier hashtag** de la description (fonction `deviner_theme()`), via une table d'alias `THEME_ALIASES` qui fait correspondre des dizaines de hashtags spécifiques aux 9 thèmes officiels. Cas particulier : si le premier hashtag est `#stress` ET que `#travail` figure dans les 3 premiers hashtags → thème `posturesantistress` (sinon `#stress` seul retombe sur `systemenerveux`).
3. Si le pin a un champ `image_prete`, utilise cette image telle quelle (recadrée, sans texte ajouté). Sinon : génère un fond par IA (si `OPENAI_API_KEY` est configuré, modèle `gpt-image-1.5`) ou choisit un fond dans `fonds/` filtré par thème via `fonds_themes.json` (rotation basée sur le nombre de fois où ce thème a déjà utilisé un fond, pour ne pas répéter trop vite), puis incruste la phrase d'accroche (`texte_image`) sur l'image (1000×1500, police Poppins).
4. Génère aussi une courte vidéo (zoom lent + fondu, ffmpeg) à partir de l'image fixe, en plus de l'image — envoyée à Make comme `video_url` si elle est bien accessible en ligne.
5. Tronque la description au besoin (troncature intelligente à une fin de phrase quand possible) pour respecter la limite Pinterest de ~495-500 caractères, en réservant de la place pour les hashtags et, une fois sur deux, une phrase d'enregistrement aléatoire tirée de `PHRASES_ENREGISTRER`.
6. Commit l'image (et la vidéo) dans le dépôt, récupère son URL publique via jsDelivr (CDN qui sert le contenu GitHub), attend qu'elle soit effectivement accessible en ligne avant de continuer.
7. **Détermine le lien de destination** : vide (`""`) si le thème est dans `THEMES_SANS_LIEN` (`alimentation`, `procrastination`, `energie`, `fatiguementale` — mis à jour le 28/09/2026, voir `03-regles-editoriales.md` section 5), sinon `LIEN_PAGE`.
8. Envoie titre / description / URL image / URL vidéo / lien / thème / ID du tableau Pinterest à `MAKE_WEBHOOK_URL` (webhook Make.com), qui publie réellement sur Pinterest.
9. Ajoute l'entrée à `historique.json` (anti-répétition) et purge les images/vidéos de plus de 30 jours du dépôt.

Le pipeline carousel (`carousel.yml`, depuis le 29/09/2026, substitut Idea Pin 1×/jour) ne passe **pas** par Make : il publie directement via l'API REST Composio (`PINTEREST_CREATE_PIN`, secret `COMPOSIO_API_KEY`), choisit un pin non publié ayant `points_image`, génère une couverture + une slide par point (fond différent par slide), vérifie que Composio renvoie bien un id de pin, puis inscrit l'entrée dans `historique.json` avec rebase/nouvelle tentative (évite la republication par `pins.yml`). Détail : `04-journal-decisions.md` section 15.

Le pipeline vidéo (`videos.yml`) utilise ses propres fichiers (`videos.json`, `historique_videos.json`, `videos_fonds/`) et la même règle `THEMES_SANS_LIEN`. **Depuis le 29/09/2026, il ne passe plus par Make** (le scénario Make « Pinterest Video Pins » n'a jamais publié une seule vidéo : formules invalides, désactivé par Make le 26/09 — voir `04-journal-decisions.md` section 16) : il publie via l'API REST Composio comme `carousel.yml` — `PINTEREST_REGISTER_MEDIA` → envoi du .mp4 en multipart vers `upload_url` avec `upload_parameters` → `PINTEREST_GET_MEDIA` jusqu'au statut `succeeded` → `PINTEREST_CREATE_PIN` (`source_type: video_id`, couverture envoyée en base64). L'entrée n'est inscrite dans `historique_videos.json` qu'une fois l'id du pin reçu.

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
| `.github/workflows/carousel.yml` | Workflow de publication du carousel quotidien (substitut Idea Pin, via Composio) |
| `prompts/system-prompt-pin-seo.md` | Prompt système pour un futur module IA Make (flux image→texte, non connecté) |
| `CLAUDE.md` | Résumé opérationnel des règles, chargé automatiquement par Claude Code sur ce dépôt |
| `README.md` | Documentation complète et détaillée du fonctionnement et des règles |

## Secrets GitHub requis

- `MAKE_WEBHOOK_URL` — webhook Make.com pour les pins classiques (mode image)
- `MAKE_WEBHOOK_URL_VIDEO` — ancien webhook Make.com des Video Pins, **plus utilisé depuis le 29/09/2026** (remplacé par `COMPOSIO_API_KEY`)
- `LIEN_PAGE` — URL de la page de capture de la formation
- `COMPOSIO_API_KEY` — clé API Composio pour `carousel.yml` et `videos.yml` (projet `yacinenettour_workspace_first_project`, où la connexion Pinterest doit exister)
- `OPENAI_API_KEY` *(optionnel)* — génération de fonds inédits par IA, ~0,05 $/image en qualité `medium`

## Formats

- **Pins classiques** : image verticale 1000×1500 (ratio 2:3)
- **Video Pins** : format 9:16, 1080×1920
- **Descriptions** : corps de texte visé 380-450 caractères, total (corps + hashtags, + éventuelle phrase d'enregistrement) toujours ≤ ~495-500 caractères (limite Pinterest ; troncature automatique intelligente au-delà)
- **Titres** : maximum 100 caractères (troncature stricte dans le script si dépassement)

## Pinterest Analytics — accès en lecture (depuis le 28/09/2026)

Distinct du pipeline de publication ci-dessus (`MAKE_WEBHOOK_URL`, écriture seule, aucune lecture possible). Un connecteur **Composio** (toolkit `pinterest`) permet, une fois une connexion OAuth établie en session, d'interroger en lecture le vrai compte Pinterest :

- `PINTEREST_GET_PROFILE` — profil et compteurs globaux (abonnés, nombre de pins, nombre de tableaux, vues mensuelles).
- `PINTEREST_GET_ACCOUNT_ANALYTICS` — analytics agrégées du compte sur une plage de dates (max 90 jours), avec détail quotidien (`daily_metrics`) : impressions, enregistrements, clics, engagement.
- `PINTEREST_GET_TOP_PINS` — classement des pins par métrique (saves, impressions, clics...).
- `PINTEREST_GET_PIN_ANALYTICS` — analytics détaillées d'un pin précis par son ID.
- `PINTEREST_LIST_BOARDS` — liste réelle des tableaux du compte (ID, nom, nombre de pins, description) — **12 tableaux existent réellement, alors que le pipeline n'en gère que 9** (`TABLEAUX` dans `pins.yml`/`videos.yml`) ; 3 tableaux (`Routine anti-âge quotidienne`, `🧠 Fatigue & Causes Biologiques`, `Enregistrements rapides`) existent hors du système actuel — voir `04-journal-decisions.md` section 9.
- `PINTEREST_GET_PIN` — détail complet d'un pin par son ID (titre, description, image, tableau, lien).

**Accès en écriture confirmé le 29/09/2026** (correction : on pensait qu'aucun n'existait) — `PINTEREST_CREATE_PIN` (image, carousel 2-5 images, ou vidéo enregistrée ; ne couvre pas explicitement le format natif "Idea Pin"/`creative_type: IDEA` observé sur les meilleurs pins historiques, à vérifier), `PINTEREST_UPDATE_PIN` (déplacer un pin vers un autre tableau, modifier titre/description/lien), `PINTEREST_DELETE_BOARD`. Notes : `PINTEREST_CREATE_PIN` précise que l'écriture en production nécessite un accès Pinterest "Standard" (un accès "Trial" est explicitement bloqué) — à vérifier avant de compter dessus. Ces actions n'ont jamais été utilisées pour publier/modifier quoi que ce soit sur le compte réel — toute utilisation reste une décision explicite de l'utilisateur (compte avec de vrais abonnés), jamais une exécution automatique en session.

**Mécanique de connexion** : `COMPOSIO_SEARCH_TOOLS` (découvre les tools et leur statut de connexion) → `COMPOSIO_MANAGE_CONNECTIONS` (action `add`, génère un lien d'authentification OAuth à transmettre à l'utilisateur, puis action `list` pour vérifier que la connexion est passée à `active` avant d'exécuter quoi que ce soit) → `COMPOSIO_MULTI_EXECUTE_TOOL` (exécute les tools Pinterest par leur slug, ex. `PINTEREST_GET_ACCOUNT_ANALYTICS`) ; les réponses volumineuses sont sauvegardées dans un fichier distant à traiter avec `COMPOSIO_REMOTE_BASH_TOOL`. La connexion est probablement propre à la session — à revérifier (`action: "list"`) en début de session future avant de supposer qu'elle est toujours active.
