# pins-clarte

Publication automatique de pins Pinterest pour "Clarté Mentale | Stress & Énergie", via GitHub Actions + Make.com.

## Fonctionnement

Le workflow `.github/workflows/pins.yml` tourne automatiquement 7 fois par jour (6h07, 8h07, 10h07, 12h07, 14h07, 16h07, 18h07 UTC — décalé de l'heure pile pour éviter les ralentissements de GitHub aux heures de forte charge) :

1. Il choisit un pin (titre + description + phrase d'accroche) dans une banque de textes déjà écrits, en évitant les répétitions récentes (voir `historique.json`).
2. Il devine le thème du pin (sommeil, système nerveux, fatigue mentale, alimentation, procrastination, somatisation, énergie, blocage mental, postures anti-stress) à partir du premier hashtag de la description, puis choisit une photo de fond du même thème dans `fonds/` (voir `fonds_themes.json`) — pour que l'image corresponde toujours au texte, par exemple pas de photo de petit-déjeuner sur un pin qui parle de réveil nocturne.
3. Il génère une image verticale (1000x1500) avec la phrase d'accroche posée sur ce fond (si `fonds/` est vide, un fond dégradé par défaut est utilisé).
4. Il commit l'image dans le dépôt et récupère son URL publique.
5. Il envoie titre / description / URL de l'image / lien vers un webhook Make.com, qui publie le pin sur Pinterest.

## Secrets GitHub requis

Dans **Settings → Secrets and variables → Actions** de ce dépôt :

- `MAKE_WEBHOOK_URL` : l'URL du webhook du scénario Make.com
- `LIEN_PAGE` : le lien vers lequel chaque pin doit renvoyer

## Ajouter des images de fond

Dépose n'importe quelle image `.png` / `.jpg` / `.jpeg` dans le dossier `fonds/`. Sans image dans ce dossier, un fond dégradé nuit étoilée est généré automatiquement.

Pour que l'image reste cohérente avec le texte du pin, ajoute aussi une ligne dans `fonds_themes.json` du type `"fond-101.jpg": "sommeil"` (thèmes possibles : `sommeil`, `systemenerveux`, `fatiguementale`, `alimentation`, `procrastination`, `somatisation`, `energie`, `blocagemental`, `posturesantistress`). Une image non répertoriée dans ce fichier reste utilisable, mais seulement en dernier recours si aucune image du bon thème n'est disponible.

## Lancer un test manuel

Onglet **Actions** → workflow **Pins Pinterest** → bouton **Run workflow**.
