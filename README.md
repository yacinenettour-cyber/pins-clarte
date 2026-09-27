# pins-clarte

Publication automatique de pins Pinterest pour "Clarté Mentale | Stress & Énergie", via GitHub Actions + Make.com.

## Fonctionnement

Le workflow `.github/workflows/pins.yml` est déclenché 7 fois par jour (6h07, 8h07, 10h07, 12h07, 14h07, 16h07, 18h07 UTC) par un service externe gratuit (cron-job.org), qui appelle l'API GitHub pour lancer le workflow. On n'utilise plus le déclencheur `schedule` natif de GitHub Actions, qui peut être retardé ou complètement sauté pendant les pics de charge — voir la section **Déclenchement (cron-job.org)** plus bas.

À chaque exécution :

1. Il choisit un pin (titre + description + phrase d'accroche) dans une banque de textes déjà écrits, en évitant les répétitions récentes (voir `historique.json`).
2. Il devine le thème du pin (sommeil, système nerveux, fatigue mentale, alimentation, procrastination, somatisation, énergie, blocage mental, postures anti-stress) à partir du premier hashtag de la description, puis choisit une photo de fond du même thème dans `fonds/` (voir `fonds_themes.json`) — pour que l'image corresponde toujours au texte, par exemple pas de photo de petit-déjeuner sur un pin qui parle de réveil nocturne.
3. Il génère une image verticale (1000x1500) avec la phrase d'accroche posée sur ce fond (si `fonds/` est vide, un fond dégradé par défaut est utilisé).
4. Il commit l'image dans le dépôt et récupère son URL publique.
5. Il envoie titre / description / URL de l'image / lien vers un webhook Make.com, qui publie le pin sur Pinterest.

## Cohérence du contenu (vérification obligatoire avant d'ajouter un pin)

Le compte est centré sur **le stress, la procrastination et le sommeil**, avec ses thèmes établis (`sommeil`, `systemenerveux`, `fatiguementale`, `alimentation`, `procrastination`, `somatisation`, `blocagemental`, `posturesantistress`, `energie` — voir `TABLEAUX` dans `.github/workflows/pins.yml`, chaque thème a son propre board Pinterest). Le script de publication ne fait **aucun contrôle de pertinence** : il publie tel quel le premier pin non encore publié de `pins.json`, dans l'ordre. Toute la responsabilité de cohérence repose donc sur ce qui est ajouté à la banque.

**Avant d'ajouter un nouveau pin à `pins.json` (texte + `image_prete` le cas échéant), vérifier systématiquement :**

1. **Le texte** (titre, texte_image, description) doit se rattacher clairement à un des thèmes ci-dessus, toujours à travers l'angle stress/mental — pas de contenu générique (recette, déco, organisation domestique...) sans lien explicite avec le sommeil, le stress ou le système nerveux. Exemple déjà rencontré à éviter : un pin "rangez votre frigo" sans lien avec le stress ne convient pas ; "ce que le désordre du frigo dit de ta charge mentale" convient.
   - **Cas particulier du thème `alimentation` (board "Alimentation et stress")** : ce board sert uniquement à montrer comment l'alimentation **diminue le stress**, pas le sommeil ni l'énergie en général (ces angles-là existent déjà via les thèmes `sommeil` et `energie`). Un pin alimentation dont le bénéfice mis en avant est l'endormissement ou l'énergie, sans mention explicite du stress/tension/nervosité, ne va pas sur ce board.
2. **L'image** (`fonds/`, fond généré par IA, ou `image_prete`) doit correspondre au sujet réel du texte, pas seulement au thème détecté automatiquement par mot-clé.
3. **Le thème détecté dépend du premier hashtag de la description** (voir `deviner_theme()` dans `.github/workflows/pins.yml`) — pas seulement de la présence du mot-clé du thème quelque part dans le texte. Toujours placer en premier hashtag celui qui correspond au vrai board visé, même si d'autres hashtags thématiques apparaissent aussi dans la description.
4. En cas de lot d'images/textes reçu en bloc (infographies fournies par l'utilisateur, etc.), trier avant l'ajout : écarter ce qui ne rentre pas dans le périmètre plutôt que tout ajouter par défaut.

Un audit a retiré en septembre 2026 onze pins "recette/organisation cuisine" sans lien avec le stress qui avaient été ajoutés par erreur (dont certains déjà publiés), et recentré le board `alimentation` en réordonnant les hashtags de 5 pins dont le vrai sujet était le sommeil ou l'énergie, pas le stress — voir l'historique Git pour référence.

## Stratégie des titres

- **Jamais le même titre sur plusieurs pins/images.** Pinterest recommande du contenu original et pénalise les doublons répétés — chaque titre ajouté à `pins.json` doit être unique (vérifié régulièrement : aucun doublon à ce jour).
- **Composition des titres : ~70 % problème/curiosité, 30 % solution.** C'est la version à privilégier en premier pour maximiser les impressions (ex. *"Pourquoi tu te réveilles à 3h du matin (et ce que ça dit de ton système nerveux)"* plutôt que *"3 astuces pour arrêter de te réveiller la nuit"*).
- **Ensuite, se fier à Pinterest Analytics.** Une fois assez de données accumulées, repérer les formulations qui génèrent le plus d'enregistrements (saves) et de clics, et orienter les prochains titres vers ces formulations gagnantes plutôt que de continuer à tester à l'aveugle.

## Déclenchement (cron-job.org)

Le workflow n'a plus de programmation automatique intégrée (`schedule` a été retiré du fichier `.github/workflows/pins.yml` pour éviter les retards/oublis de GitHub). À la place, un compte gratuit sur [cron-job.org](https://cron-job.org) appelle l'API GitHub 7 fois par jour pour lancer le workflow. Configuration :

1. Crée un **token GitHub** dédié : sur GitHub, **Settings** (ton profil, pas le dépôt) → **Developer settings** → **Personal access tokens** → **Fine-grained tokens** → **Generate new token**. Limite-le au dépôt `pins-clarte` uniquement, et donne-lui la permission **Actions : Read and write** (rien d'autre). Copie le token une fois généré (il ne sera plus jamais affiché).
2. Crée un cronjob sur cron-job.org, avec :
   - **URL** : `https://api.github.com/repos/yacinenettour-cyber/pins-clarte/actions/workflows/pins.yml/dispatches`
   - **Méthode** : `POST`
   - **En-têtes (headers)** :
     - `Authorization: Bearer TON_TOKEN`
     - `Accept: application/vnd.github+json`
     - `Content-Type: application/json`
   - **Corps de la requête (body)** : `{"ref":"main"}`
   - **Planning** : tous les jours à 6h07, 8h07, 10h07, 12h07, 14h07, 16h07 et 18h07, **en UTC** (bien vérifier le fuseau horaire choisi sur cron-job.org).

Le token ne doit jamais être collé ailleurs que dans le champ "headers" de cron-job.org.

## Secrets GitHub requis

Dans **Settings → Secrets and variables → Actions** de ce dépôt :

- `MAKE_WEBHOOK_URL` : l'URL du webhook du scénario Make.com (pins classiques, image)
- `MAKE_WEBHOOK_URL_VIDEO` : l'URL du webhook d'un **second** scénario Make.com, dédié aux Video Pins — voir section **Video Pins** ci-dessous
- `LIEN_PAGE` : le lien vers lequel chaque pin doit renvoyer
- `OPENAI_API_KEY` *(optionnel)* : voir section **Génération de fonds par IA** ci-dessous

## Ajouter des images de fond

Dépose n'importe quelle image `.png` / `.jpg` / `.jpeg` dans le dossier `fonds/`. Sans image dans ce dossier, un fond dégradé nuit étoilée est généré automatiquement.

Pour que l'image reste cohérente avec le texte du pin, ajoute aussi une ligne dans `fonds_themes.json` du type `"fond-101.jpg": "sommeil"` (thèmes possibles : `sommeil`, `systemenerveux`, `fatiguementale`, `alimentation`, `procrastination`, `somatisation`, `energie`, `blocagemental`, `posturesantistress`). Une image non répertoriée dans ce fichier reste utilisable, mais seulement en dernier recours si aucune image du bon thème n'est disponible.

Comme les fonds sont réutilisés par thème (pas globalement), un thème très publié avec peu de photos repasse vite sur les mêmes images. Pour viser un nombre de jours minimum sans répétition sur un thème donné, vise environ `(pins de ce thème par jour) × (jours voulus)` photos dans ce thème.

## Génération de fonds par IA (optionnel)

Si le secret `OPENAI_API_KEY` est renseigné, chaque pin génère automatiquement une photo de fond inédite via l'API OpenAI (`gpt-image-1.5`), adaptée au thème détecté — **plus aucune répétition possible**, la banque `fonds/` devient un simple filet de sécurité (utilisée seulement si la clé est absente ou si l'appel échoue).

- **Coût estimé** : ~0,05 $/image en qualité `medium` (réglable via le secret optionnel `OPENAI_IMAGE_QUALITY` : `low`, `medium` ou `high`), soit environ 0,50 $/jour pour 10 pins → ~15 $/mois. En `low`, environ 4 $/mois.
- **Avant d'activer** : les modèles `gpt-image-*` demandent parfois une vérification d'identité de l'organisation OpenAI (dans les paramètres de ton compte platform.openai.com) avant de fonctionner — si le premier appel échoue, vérifie ça en premier.
- Sans ce secret, rien ne change : le système continue d'utiliser `fonds/` comme aujourd'hui.

## Video Pins (`.github/workflows/videos.yml`)

Un second workflow, séparé du premier, génère des **Video Pins** (format 9:16, 1080×1920) à partir de scripts en plusieurs scènes définis dans `videos.json` — chaque script décrit une suite de beats (image + texte + durée) qui racontent une info concrète (ex. une technique de respiration avec un chiffre précis), pas juste une ambiance. Les images de fond viennent soit de `fonds/`, soit de `videos_fonds/` (assets dédiés aux vidéos, plus grand format).

À chaque exécution : choisit le prochain script non encore publié dans `videos.json` (suivi dans `historique_videos.json`, même logique que `pins.json`/`historique.json`), assemble les scènes avec zoom lent + fondus doux (ffmpeg), incruste le texte, commit la vidéo + une image de couverture dans `videopins/`, puis envoie le tout au webhook `MAKE_WEBHOOK_URL_VIDEO` (secret séparé, plus `LIEN_PAGE`).

**Important : ce workflow utilise un webhook Make.com différent de celui des pins classiques**, exprès — pour que le scénario Make existant (pins quotidiens, mode image) reste inchangé, et que seul le nouveau scénario dédié aux vidéos soit réglé en mode vidéo. Pas besoin de jongler entre les deux réglages.

**Deux étapes manuelles restent nécessaires avant que ça publie vraiment sur Pinterest :**

1. **Dans Make.com**, dupliquer ton scénario Pinterest existant (clic droit dessus → Dupliquer, ou "Créer une copie"), puis sur cette copie : ouvrir son module **Webhook** et créer un **nouveau** webhook dédié (ne pas réutiliser celui des pins classiques) — copie son URL, elle servira pour le secret `MAKE_WEBHOOK_URL_VIDEO`. Ensuite, sur le module **Pinterest** de cette copie, changer le champ **"Type de source"** de "URL de l'image" à **"Vidéo"**, mapper `video_url` sur le nouveau champ vidéo, et garder `image_url` comme image de couverture. Active ce nouveau scénario. Le scénario d'origine (pins classiques) reste tel quel, en mode image, avec son webhook d'origine.
2. **Sur cron-job.org**, ajouter un deuxième cronjob (même méthode que celui de `pins.yml`, voir plus haut) pointant vers `https://api.github.com/repos/yacinenettour-cyber/pins-clarte/actions/workflows/videos.yml/dispatches`, réglé pour se déclencher **tous les jours (7 vidéos par semaine)**, par exemple à 19h37 UTC — à une minute différente des pins (`:07`) pour que les deux robots ne poussent pas dans le dépôt en même temps.

**Ajouter de nouveaux scripts vidéo** : compléter `videos.json` avec un nouvel objet `{id, theme, titre, description, beats}` — `id` doit être unique (sert au suivi anti-répétition), et chaque beat a `image` (chemin dans le dépôt), `texte` (max 2 lignes courtes) et `duree` (secondes). À 7 vidéos par semaine, la banque (30 scripts au départ) tient environ 4 semaines. Sans nouveaux scripts, la banque s'épuise — prévoir d'en ajouter régulièrement, comme pour `pins.json`.

## Lancer un test manuel

- Pins classiques : onglet **Actions** → workflow **Pins Pinterest** → bouton **Run workflow** → choisir **test** dans le menu **Mode**.
- Video Pins : onglet **Actions** → workflow **Pins Pinterest - Videos** → bouton **Run workflow** → choisir **test** dans le menu **Mode**.

En mode **test**, le script s'arrête juste après avoir généré l'image/la vidéo (visible dans les logs), sans rien publier sur Pinterest ni consommer de pin/script dans la banque — utile pour vérifier qu'une modification du code fonctionne sans gâcher un vrai pin. Le mode **publier** (par défaut) fait une vraie publication, exactement comme le déclenchement automatique de cron-job.org, qui n'envoie pas d'inputs et reste donc toujours en mode publier.
