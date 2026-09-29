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

## Leçons ajoutées à la formation (29/09/2026)

`POST /api/school/modules/{moduleId}/classic-lectures` crée une leçon **désactivée** et renvoie son `pageId`. Son contenu s'écrit avec le même `page-editor/pages/{pageId}/save` (type `lecture` : une seule section, blocs Headline, Text, BulletList, Image, References ; une image doit suivre un Text ou une BulletList). On l'active ensuite avec `POST /api/school/lectures/{id}/activate`.

| Leçon | Module | Leçon / page | Contenu |
|---|---|---|---|
| 👋 COMMENCE ICI — COMMENT SUIVRE LE PROGRAMME | Bonus (1er module), position 2 | 11128710 / 45141870 | `lecon-commence-ici.json` : ordre conseillé des modules (compense le module « Sortir des ruminations » rangé en dernier), mode d'emploi, garantie, contact |
| 🗓️ TON PLAN DES 4 PROCHAINES SEMAINES | Consolider le sommeil, position 3 | 11128711 / 45141871 | `lecon-plan-4-semaines.json` : un module par semaine, conseils pour tenir |

Les deux ont été activées le 29/09 (0 élève à cette date). Le contenu des leçons existantes n'est pas lisible par l'API : les nouvelles leçons ne décrivent les modules qu'à partir de la page de vente.
