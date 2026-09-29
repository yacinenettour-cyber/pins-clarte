# Pages systeme.io créées par l'API (29/09/2026)

Le forfait gratuit bloque l'ajout de pages dans l'interface, mais l'API l'accepte :

1. `POST /api/funnels/{funnelId}/steps` avec un type (`info_page`, `sales_page`…).
2. `PUT /api/page-editor/pages/{pageId}/save` avec `{"aiContentSchema": <contenu JSON ci-dessous>}`. Le constructeur de systeme.io génère la mise en page.

Pièges constatés :
- Le constructeur **retire les liens `<a>` des blocs Text** : pour un lien, utiliser un bloc Button avec l'action `openUrl`.
- Les noms de palette ne correspondent pas aux couleurs affichées (« linen-blue » donne du jaune et vert, « iris-mist » du rouge). **« deep-ocean » donne un bleu nuit : c'est la palette retenue.**
- L'image d'en-tête est régénérée par le constructeur à chaque enregistrement.
- Chaque enregistrement remplace la page entière : pour modifier, éditer le JSON puis renvoyer tout le contenu.

| Page | URL | Étape / page (tunnel « Page de vente », 6646405) | Contenu |
|---|---|---|---|
| Mentions légales, CGV et confidentialité | https://lp.contactapaisement-mental.fr/0f1d6dac | 25634497 / 45140167 | `page-legale.json` (reste : médiateur) |
| Page de vente sans témoignages | https://lp.contactapaisement-mental.fr/0e9ef918 | 25634641 / 45140579 | `page-vente-v2.json` |
