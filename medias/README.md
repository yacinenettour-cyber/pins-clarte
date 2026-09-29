# medias/

Images hors pipeline Pinterest (le nettoyage automatique de `pins.yml` ne touche que `images/` et `videos/`).

- `emails/` : illustrations de la séquence e-mails systeme.io (`docs/systeme-io/sequence-emails-v2.md`), servies via jsDelivr **épinglé sur un commit** (`cdn.jsdelivr.net/gh/yacinenettour-cyber/pins-clarte@<sha>/medias/emails/...`) : ne pas renommer ni supprimer ces fichiers.
- `formation/` : bannières et schémas pour les modules de la formation « Quand le cerveau refuse de dormir », à insérer à la main dans les leçons systeme.io (l'API ne donne pas accès au contenu des leçons).

Tout le texte est dessiné par script (PIL, police Poppins), jamais par une IA d'image. Photos : `fonds/`.

## Où placer les images de `formation/` (à faire dans systeme.io, éditeur de chaque leçon → bloc Image)

| Image | Leçon conseillée | Emplacement |
|---|---|---|
| `banniere-bonus-audio-express.jpg` | Bonus — « Accorde-toi un moment » | tout en haut |
| `banniere-module-1.jpg` + `schema-module-1-alerte-repos.jpg` | Module 1 — « Apaiser le système nerveux » | bannière en haut, schéma après l'explication du mode alerte |
| `banniere-module-2.jpg` + `schema-module-2-lutter-ou-laisser-passer.jpg` | Module 2 — « Sortir des ruminations » | bannière en haut, schéma avant l'exercice |
| `banniere-module-3.jpg` + `schema-module-3-pourquoi-un-rituel.jpg` | Module 3 — « Rituel du soir » | bannière en haut, schéma avant le déroulé du rituel |
| `banniere-module-4.jpg` + `schema-module-4-progression.jpg` | Module 4 — « Stabiliser le sommeil progressivement » | bannière en haut, schéma à la fin |

Les schémas reprennent les promesses de la page de vente (le contenu des leçons n'est pas lisible par l'API) : les relire avant de les insérer et ne garder que ceux qui collent au contenu réel.
