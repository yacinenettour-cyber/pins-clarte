# pins-clarte

Publication automatique de pins Pinterest pour "Clarté Mentale | Stress & Énergie", via GitHub Actions + Make.com.

## Fonctionnement

Le workflow `.github/workflows/pins.yml` tourne automatiquement 5 fois par jour (6h, 9h, 12h, 15h, 18h UTC) :

1. Il choisit un pin (titre + description + phrase d'accroche) dans une banque de textes déjà écrits, en évitant les répétitions récentes (voir `historique.json`).
2. Il génère une image verticale (1000x1500) avec cette phrase d'accroche, en piochant au hasard une photo de fond dans le dossier `fonds/` (si vide, un fond dégradé par défaut est utilisé).
3. Il commit l'image dans le dépôt et récupère son URL publique.
4. Il envoie titre / description / URL de l'image / lien vers un webhook Make.com, qui publie le pin sur Pinterest.

## Secrets GitHub requis

Dans **Settings → Secrets and variables → Actions** de ce dépôt :

- `MAKE_WEBHOOK_URL` : l'URL du webhook du scénario Make.com
- `LIEN_PAGE` : le lien vers lequel chaque pin doit renvoyer

## Ajouter des images de fond

Dépose n'importe quelle image `.png` / `.jpg` / `.jpeg` dans le dossier `fonds/`. Le script en choisit une au hasard à chaque exécution. Sans image dans ce dossier, un fond dégradé nuit étoilée est généré automatiquement.

## Lancer un test manuel

Onglet **Actions** → workflow **Pins Pinterest** → bouton **Run workflow**.
