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
| Ancienne page de vente, remplacée le 30/09 (37 €, sans faux avis) | https://lp.contactapaisement-mental.fr/accesformation | 22061104 / 36308944 | `page-vente-v2.json` (ancienne version : `../archives/page-vente-v1-accesformation/`) |
| Paiement 37 € (tu, garantie, CGV) — offre 5383492 | https://lp.contactapaisement-mental.fr/689e4290 | 25635389 / 45142825 | `page-paiement-v2.json` |
| Merci pour ton achat (suit la page ci-dessus) | https://lp.contactapaisement-mental.fr/0401c87c | 25635439 / 45143273 | `page-merci-achat-v2.json` |

## Pages de paiement (29/09/2026)

- Type `offer-form` : même principe (`page-schema` puis `save`), avec un bloc `Checkout` natif. Les sections du corps (feature, plain…) doivent précéder le groupe de fin (faq, pricing, order, guarantee), sinon erreur 422.
- Une nouvelle étape `offer-form` crée automatiquement une offre **sans produit** : la rattacher avec `PATCH /api/payment/offers/{id}` `{"digitalProductId": 3196087}`. Vérification : dans le HTML de la page, `"offer":"{\"id\":…,\"pricePlans\":[…3700…]` et `checkedPlanId` non vide.
- **L'ancienne page `/paiement-anti-stress` (offre 4583959) n'avait aucun tarif rattaché** (`pricePlans: []`, `checkedPlanId` vide) : produit 3196087 rattaché le 29/09, tarif 37 € vérifié dans le HTML. Retour arrière : `{"digitalProductId": null}`.
- Le bloc `Checkout` généré impose un formulaire de facturation complet (prénom, nom, e-mail, téléphone, pays, adresse, code postal, textes indicatifs en anglais) : non réglable par l'API, à alléger dans l'éditeur.
- Après l'achat, systeme.io renvoie vers l'étape suivante par position (`nextStepUrl` dans le HTML) : l'étape de remerciement doit être créée juste après la page de paiement.
- Le texte de CGV par défaut du compte (champ `agreement` de la page de paiement) est encore le modèle « Conditions générales de vente (NOMSOCIETE) » : à remplacer par le texte de `../pages-legales.md` avant d'activer la case à cocher des CGV.

## Leçons ajoutées à la formation (29/09/2026)

`POST /api/school/modules/{moduleId}/classic-lectures` crée une leçon **désactivée** et renvoie son `pageId`. Son contenu s'écrit avec le même `page-editor/pages/{pageId}/save` (type `lecture` : une seule section, blocs Headline, Text, BulletList, Image, References ; une image doit suivre un Text ou une BulletList). On l'active ensuite avec `POST /api/school/lectures/{id}/activate`.

| Leçon | Module | Leçon / page | Contenu |
|---|---|---|---|
| 👋 COMMENCE ICI — COMMENT SUIVRE LE PROGRAMME | Bonus (1er module), position 2 | 11128710 / 45141870 | `lecon-commence-ici.json` : ordre conseillé des modules (compense le module « Sortir des ruminations » rangé en dernier), mode d'emploi, garantie, contact |
| 🗓️ TON PLAN DES 4 PROCHAINES SEMAINES | Consolider le sommeil, position 3 | 11128711 / 45141871 | `lecon-plan-4-semaines.json` : un module par semaine, conseils pour tenir |

Les deux ont été activées le 29/09 (0 élève à cette date).

## 14 leçons ajoutées le 30/09/2026 (formation passée de 9 à 23 leçons)

Contenu : `lecons-v2/*.json`, généré par `lecons-v2/gen_lecons.py`. Publiées via `POST /api/school/modules/{id}/classic-lectures` (**`delayBeforePreviousLecture: 0` obligatoire**, sinon 422), `save`, puis `activate`. Vérifié : 23 leçons actives, aucun doublon (`modules-with-lectures?limit=100` : sans `limit`, la réponse s'arrête à 10 leçons). Le serveur valide réellement le contenu (une version invalide est refusée en 422, sans rien modifier). Premier module renommé « 🌙 BIEN DÉMARRER + AUDIO EXPRESS (SOIR TRÈS DIFFICILE) ». « Commence ici » et « Plan des 4 semaines » renvoient vers les nouvelles leçons et le kit.

| Module | Leçons ajoutées (id) |
|---|---|
| Bien démarrer (2160235) | Où en es-tu ? auto-évaluation (11132883), Ton kit à imprimer (11132884) |
| Apaiser le système nerveux (2160281) | Soupir physiologique (11129719), Relâchement musculaire (11132872), Scan corporel (11132873) |
| Rituel du soir (2169485) | Préparer le corps (11132878), Rituel en 3 versions (11132879) |
| Consolider (2177956) | Réveillé à 3 h (11132880), Le matin compte (11132881), Quand consulter (11132882) |
| Sortir des ruminations (2161517) | Rendez-vous des soucis (11132874), Liste de demain (11132875), Mélange cognitif (11132876), Prendre de la distance (11132877) |

Les fiches PDF du kit (`medias/formation/kit/`) sont liées par des blocs `References` (jsDelivr épinglé sur `22e9e84`). Le contenu des leçons existantes n'est pas lisible par l'API : les nouvelles leçons ne décrivent les modules qu'à partir de la page de vente.
