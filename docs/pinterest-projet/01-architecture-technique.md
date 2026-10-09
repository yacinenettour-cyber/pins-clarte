# Architecture technique — pipeline de publication

## Deux flux de contenu, non connectés entre eux

### Flux actif : texte → image (`pins.yml`, `videos.yml`)

C'est le flux réellement utilisé aujourd'hui. Le texte (titre, description, phrase d'accroche) est déjà écrit à l'avance dans `pins.json` / `videos.json`. À chaque exécution, le script choisit le prochain élément non publié, lui associe une image (fond existant, fond généré par IA, ou image prête fournie), et publie.

### Flux préparé mais pas encore branché : image → texte (`prompts/system-prompt-pin-seo.md`)

Un prompt système a été rédigé pour un futur module IA dans un scénario Make.com séparé : Make enverrait une image reçue, et l'IA analyserait l'image pour générer titre/description/mots-clés/hashtags/nom de fichier/texte alt/tableau en JSON. Ce flux n'est pas relié au flux actif — avant de les connecter (les faire cohabiter, ou basculer l'un vers l'autre), il faut une décision explicite du propriétaire du compte.

## Déclenchement

- **Pins** : `.github/workflows/pins.yml`, déclenché 10×/jour (constaté dans les exécutions Make du 26 au 29/09/2026 : 5h07, 6h07, 7h07, 8h07, 10h07, 12h07, 14h07, 16h07, 18h07, 20h07 UTC) par un appel API externe (cron-job.org, gratuit) vers l'endpoint `workflow_dispatch` de GitHub Actions. Le déclencheur natif `schedule` de GitHub Actions n'est **pas** utilisé (retards/oublis possibles sous charge).
- **Vidéos** : `.github/workflows/videos.yml`, 1×/jour à 18h30 heure de Paris — tâche cron-job.org « Vidéo Pinterest 18h30 » (id 8537376, fuseau Europe/Paris, créée le 29/09/2026 ; avant cette date aucune tâche vidéo n'existait). Le workflow ne publie jamais 2 vidéos le même jour. cron-job.org gère le fuseau `Europe/Paris` directement sur la tâche si l'option est disponible (bascule CEST/CET automatique) ; sinon, régler manuellement 16h30 UTC en été (CEST) et 17h30 UTC en hiver (CET).
- **Mode test** disponible sur les deux workflows (input `mode: test` au lancement manuel) : génère l'image/vidéo sans publier ni consommer d'élément de la banque.

## Étapes du pipeline pins (`pins.yml`) — version du 29/09/2026

1. Charge `pins.json` et `historique.json` ; choisit le **thème dont la dernière publication est la plus ancienne** (`choisir_pin_equilibre()`) et prend le premier pin disponible de ce thème.
2. **Devine le thème** à partir du **premier hashtag** de la description (`deviner_theme()`, table `THEME_ALIASES` ; `#stress` + `#travail` dans les 3 premiers → `posturesantistress`).
3. Image : `image_prete` utilisée telle quelle ; sinon fond IA (si `OPENAI_API_KEY`) ou fond de `fonds/` filtré par thème, puis **test A/B** : alternance stricte visuel **clair** (`dessiner_clair_infographie()` / `dessiner_clair_phrase()`, fonds d'au moins 800 px de large, recadrage sur la zone la plus nette) / visuel **sombre** historique (`dessiner_infographie()` / `dessiner_image()`). Texte toujours dessiné par PIL (Poppins).
4. Tronque la description (limite ~495-500 caractères, phrase d'enregistrement aléatoire une fois sur deux).
5. Commit + push de l'image (rebase et nouvelle tentative si `main` a avancé), revérifie que le pin n'a pas été publié entre-temps, attend que l'image soit servie par jsDelivr.
6. Lien (`guide_du_pin()`) : plan anti-cortisol (`LIEN_GUIDE_CORTISOL`) pour `energie`, `alimentation` et les pins `"guide": "cortisol"` ; aucun lien pour les autres thèmes de `THEMES_SANS_LIEN` et les pins `"guide": "aucun"` ; sinon `LIEN_PAGE` (guide sommeil). Depuis le 09/10/2026, un pin qui porte `"article"` peut mener à l'article correspondant du site (`article_du_pin()` : toujours s'il n'a pas de guide, sinon tant que les articles font moins de 40 % des pins avec lien des 14 derniers jours ; `description_article`, carte « ARTICLE COMPLET », `lien_du_pin()`). Paramètres UTM avec `utm_content` propre à chaque pin. Rotation (étape 1) pondérée : thème sommeil ×3 depuis le 08/10/2026 (`POIDS_THEME`), thèmes sans lien ×0,5.
7. **Publie via l'API Composio** (`PINTEREST_CREATE_PIN`, `source_type: image_url`) avec titre, description, lien éventuel et **texte alternatif** (`texte_alternatif()`). Plus de passage par Make depuis le 29/09/2026 (le scénario Make images, qui fonctionnait, ne reçoit plus rien).
8. Seulement si Pinterest renvoie un id de pin : inscrit l'entrée dans `historique.json` (`design`, `pin_id`) avec nouvelle tentative sur `main` à jour, et purge les images de plus de 30 jours. La petite vidéo générée auparavant pour chaque pin est supprimée : Make ne l'a jamais utilisée.

Le pipeline carousel (`carousel.yml`, créé le 29/09/2026 comme substitut Idea Pin ; **plus de déclenchement quotidien depuis la décision du même jour : 10 pins + 1 vidéo/jour uniquement**, lancement manuel seulement) ne passe **pas** par Make : il publie directement via l'API REST Composio (`PINTEREST_CREATE_PIN`, secret `COMPOSIO_API_KEY`), choisit un pin non publié ayant `points_image`, génère une couverture + une slide par point (fond différent par slide), vérifie que Composio renvoie bien un id de pin, puis inscrit l'entrée dans `historique.json` avec rebase/nouvelle tentative (évite la republication par `pins.yml`). Détail : `04-journal-decisions.md` section 15.

Le pipeline vidéo (`videos.yml`) utilise ses propres fichiers (`videos.json`, `historique_videos.json`, `videos_fonds/`) et le même choix de guide que `pins.yml` depuis le 08/10/2026 (plan anti-cortisol pour `energie`/`alimentation`/`"guide": "cortisol"`, `description_guide_cortisol`, `utm_content` = id de la vidéo, dernière scène remplacée par `fin_avec_lien` seulement si la vidéo a un lien). **Depuis le 29/09/2026, il ne passe plus par Make** (le scénario Make « Pinterest Video Pins » n'a jamais publié une seule vidéo : formules invalides, désactivé par Make le 26/09 — voir `04-journal-decisions.md` section 16) : il publie via l'API REST Composio comme `carousel.yml` — `PINTEREST_REGISTER_MEDIA` → envoi du .mp4 en multipart vers `upload_url` avec `upload_parameters` → `PINTEREST_GET_MEDIA` jusqu'au statut `succeeded` → `PINTEREST_CREATE_PIN` (`source_type: video_id`, couverture envoyée en base64). L'entrée n'est inscrite dans `historique_videos.json` qu'une fois l'id du pin reçu.

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
| `.github/workflows/carousel.yml` | Workflow carousel (substitut Idea Pin, via Composio) — lancement manuel uniquement, pas de cron |
| `prompts/system-prompt-pin-seo.md` | Prompt système pour un futur module IA Make (flux image→texte, non connecté) |
| `CLAUDE.md` | Résumé opérationnel des règles, chargé automatiquement par Claude Code sur ce dépôt |
| `README.md` | Documentation complète et détaillée du fonctionnement et des règles |

## Secrets GitHub requis

- `MAKE_WEBHOOK_URL` — ancien webhook Make.com des pins classiques, **plus utilisé depuis le 29/09/2026**
- `MAKE_WEBHOOK_URL_VIDEO` — ancien webhook Make.com des Video Pins, **plus utilisé depuis le 29/09/2026** (remplacé par `COMPOSIO_API_KEY`)
- `LIEN_PAGE` — URL de la page de capture de la formation
- `COMPOSIO_API_KEY` — clé API Composio pour `pins.yml`, `videos.yml` et `carousel.yml` (projet `yacinenettour_workspace_first_project`, où la connexion Pinterest doit exister)
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

**Accès en écriture confirmé le 29/09/2026** (correction : on pensait qu'aucun n'existait) — `PINTEREST_CREATE_PIN` (image, carousel 2-5 images, ou vidéo enregistrée ; ne couvre pas explicitement le format natif "Idea Pin"/`creative_type: IDEA` observé sur les meilleurs pins historiques, à vérifier), `PINTEREST_UPDATE_PIN` (déplacer un pin, modifier titre/description/lien — **refusé en pratique le 29/09/2026 : « Your application does not have access to this restricted feature: pin_edit » ; modifier un pin existant se fait à la main dans l'appli**), `PINTEREST_DELETE_BOARD`. Notes : `PINTEREST_CREATE_PIN` précise que l'écriture en production nécessite un accès Pinterest "Standard" (un accès "Trial" est explicitement bloqué) — à vérifier avant de compter dessus. Ces actions n'ont jamais été utilisées pour publier/modifier quoi que ce soit sur le compte réel — toute utilisation reste une décision explicite de l'utilisateur (compte avec de vrais abonnés), jamais une exécution automatique en session.

**Mécanique de connexion** : `COMPOSIO_SEARCH_TOOLS` (découvre les tools et leur statut de connexion) → `COMPOSIO_MANAGE_CONNECTIONS` (action `add`, génère un lien d'authentification OAuth à transmettre à l'utilisateur, puis action `list` pour vérifier que la connexion est passée à `active` avant d'exécuter quoi que ce soit) → `COMPOSIO_MULTI_EXECUTE_TOOL` (exécute les tools Pinterest par leur slug, ex. `PINTEREST_GET_ACCOUNT_ANALYTICS`) ; les réponses volumineuses sont sauvegardées dans un fichier distant à traiter avec `COMPOSIO_REMOTE_BASH_TOOL`. La connexion est probablement propre à la session — à revérifier (`action: "list"`) en début de session future avant de supposer qu'elle est toujours active.
