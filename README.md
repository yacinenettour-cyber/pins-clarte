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

- `MAKE_WEBHOOK_URL` : l'URL du webhook du scénario Make.com
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

## Lancer un test manuel

Onglet **Actions** → workflow **Pins Pinterest** → bouton **Run workflow**.
