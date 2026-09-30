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
| Merci pour ton inscription (après le guide), remplacée le 30/09 (bouton à 37 €) | https://lp.contactapaisement-mental.fr/pagederemerciement | 21998130 / 36150516 (tunnel 6607794) | `page-merci-inscription-v2.json` (ancien texte : `../archives/page-merci-inscription-v1.md`). Le constructeur ajoute d'office un encadré « Produit / Prix » (type `order_thank_you_page`), vide sur cette page : à supprimer dans l'éditeur. |
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

## Module « 🧭 ET SI C'EST TON CAS ? SITUATIONS PARTICULIÈRES » (30/09/2026, formation passée à 29 leçons)

Module 2779629 créé par `POST /api/school/courses/542776/modules` (rangé en 6e et dernière position, ce qui convient : leçons à lire selon sa situation, sans audio). 5 leçons générées par `lecons-v2/gen_lecons.py` (préfixe `cas-`), publiées comme les précédentes (`classic-lectures` avec `delayBeforePreviousLecture: 0`, `save`, `activate`) : travail qui suit jusqu'au lit (11133518), parent épuisé (11133520), horaires décalés ou travail de nuit (11133521), réveil à 4 h qui revient (11133522), période de gros stress (11133523). Vérifié par `modules-with-lectures?limit=100` : 6 modules, 29 leçons actives, 0 doublon. L'inscription existante est en accès complet (`full_access`) : le nouveau module est visible sans rien changer.

Mis à jour le même jour : « Commence ici » (5e point de l'ordre des modules), page de vente (« 6 modules, près de 30 leçons », carte « Et si c'est ton cas ? », « un audio guidé dans chaque module » remplacé par « des audios guidés » puisque le nouveau module n'a pas d'audio), e-mails 5 et 10 et newsletter 5366813 (brouillon).

## Guide gratuit compressé (30/09/2026)

Le PDF du guide envoyé par l'e-mail 1 (`6ab51421ecfe18.21678028_Tonguide-3.pdf`, 28 pages) pesait **28 Mo**, dont 22,4 Mo pour 10 illustrations pleine page en PNG 1055×1491. Version allégée produite dans le bac à sable Composio (PyMuPDF : PNG → JPEG qualité 82 à résolution identique, polices réduites aux caractères utilisés, nettoyage) : **1,07 Mo**, 28 pages, texte identique, pages sans illustration identiques au pixel près, pages illustrées à 52-58 dB de PSNR (différence invisible). L'API `files` étant en lecture seule, le fichier doit être déposé par l'utilisateur dans la médiathèque ; il faudra ensuite remplacer le lien dans l'e-mail 1 (étape 6101669) et, par précaution, dans l'ancien e-mail d'automatisation 12943008 (non utilisé par la règle 2045419). Aucune autre page ni aucun autre e-mail ne pointe vers le PDF (vérifié le 30/09).

## Achat test (30/09/2026, terminé)

Code promo **100 %** (id 335496, 3 utilisations, expire le 03/10/2026 à 23 h 59, heure de Paris) rattaché à l'offre 5383492 de la nouvelle page de paiement `/689e4290`, où un bloc `Coupon` a été ajouté (réenregistrement de `page-paiement-v2.json` avec un bloc `Coupon` avant `Checkout`). Aucun paramètre d'adresse ne permet d'appliquer un code (aide systeme.io : il faut l'élément Coupon sur la page). La page vend le même produit (3196087) que l'ancienne page de paiement. **Après le test** : supprimer le code (`DELETE /api/payment/coupons/335496`), le retirer de l'offre (`coupons: []`) et réenregistrer `page-paiement-v2.json` tel quel (sans bloc `Coupon`).

**Résultat** : achat réel de l'utilisateur sur `/paiement-anti-stress` (le code n'y était pas utilisable, faute de champ), inscription créée, e-mail d'accès reçu, formation affichée correctement (« tout s'affiche correctement »). Nettoyage fait le 30/09 : code 335496 supprimé (plus aucun code sur le compte), retiré de l'offre 5383492, page `/689e4290` réenregistrée sans bloc `Coupon` (couleurs de nouveau bleues, vérifié).

## Couleurs des pages (30/09/2026)

**Le constructeur ignore `palettePreset` et tire la palette au hasard à chaque enregistrement** (même réglage « deep-ocean » : bleu, orange/jaune/vert, marron, turquoise ; « navy-flare » : bleu roi puis violet/menthe). Les couleurs appliquées se lisent dans le HTML (`__PRELOADED_STATE__`). Méthode retenue avec l'accord de l'utilisateur (« bleu nuit et crème ») : réenregistrer et vérifier la palette jusqu'à obtenir du bleu nuit + fonds crème/neutres, sans couleur vive hors bleu/doré — `outils/couleurs_systemeio.py`. Tout réenregistrement ultérieur (même pour changer un mot) retire au sort les couleurs : relancer l'outil.

| Page | Essais | Palette obtenue |
|---|---|---|
| `/accesformation` (vente) | 11, puis 153 le 30/09 après l'ajout du module 6 | 30/09 : #1C314A #345E91 #3F72AF · #DBE2EF #E8E0E0 #F9F7F7 (même palette que `/merci` et `/0f1d6dac`) ; avant : #35456E #363062 #42568A · crème #F5E8C7 #FBF6EA |
| `/merci` (après achat) | 6 | #1C314A #345E91 #3F72AF · #E8E0E0 #F9F7F7 |
| `/pagederemerciement` (après inscription au guide) | 20, puis 39 le 30/09 (texte « près de 30 leçons ») | 30/09 : #1C314A #345E91 #3F72AF · #F9F7F7 (même palette que `/merci`, la page de vente et la page légale ; aucune image sur la page, donc aucune image IA créée) ; avant : #3F56BB #424874 #5B6FC8 · #F4EEFF (bleu pervenche) |
| `/0f1d6dac` (légal) | 2 | #1C314A #3F72AF · #F9F7F7 |

Environ 44 enregistrements au total (dont 5 essais sur le doublon `/0e9ef918`), **20 images IA** créées dans la médiathèque (le constructeur réutilise ses images quand le contenu ne change pas). Non recolorées (pages d'origine de l'utilisateur, non reconstruites pour ne pas casser le formulaire en 2 étapes ni l'automatisation d'inscription) : `/paiement-anti-stress` et `/tonguide`.

**Réenregistrement du 30/09 (module 6 ajouté à la page de vente)** : le 1er tirage « strict » était bleu pétrole (#276486) avec des cartes pêche, jugé trop loin du bleu nuit. Critère resserré (bleu nuit de teinte 212-245°, fonds crème de teinte 32-60°) : la palette bleu nuit + crème d'origine n'est jamais revenue en 100 essais (environ 45 palettes différentes observées, l'ensemble paraît fini). Retenu au 19e essai suivant la palette #1C314A des pages `/merci` et légale, pour un tunnel homogène. **Coût constaté** : les images ne sont pas toujours réutilisées ; ces 153 enregistrements ont laissé environ 65 images « ai-… » orphelines dans la médiathèque (134 au total le 30/09 à 05:33 UTC, API `files` en lecture seule). Pour la suite : limiter les relances, et accepter directement la palette #1C314A quand elle sort.

**Doublons à supprimer par l'utilisateur dans l'éditeur** (l'API ne supprime pas les étapes de tunnel ; aucun lien n'y mène, vérifié le 30/09) : `/0e9ef918` (étape 25634641), `/689e4290` (25635389, offre 5383492), `/0401c87c` (25635439).
