# Pages légales — Clarté Mentale (systeme.io)

Rédigé le 29/09/2026. **Modèle à compléter, pas un avis juridique** : remplacer chaque `[À COMPLÉTER]`, et faire relire en cas de doute (CCI, avocat, ou un service de génération de CGV reconnu).

## Constat (vérifié le 29/09/2026)

- Page de paiement `/paiement-anti-stress` : seul « Mentions légales » est un lien. « Conditions générales de vente », « Politique de confidentialité » et « Contact » sont du texte simple, sans page derrière.
- Mentions légales `/mentions-lgales` : il manque le n° SIREN/SIRET, l'adresse complète, la mention « EI » (entrepreneur individuel) et l'adresse de l'hébergeur.
- Hébergeur (vérifié sur systeme.io/privacy-policy) : **ITACWT Limited, 2 Cruise Park Rise, Tyrrelstown, Dublin 15, Irlande**.
- Vente de contenu numérique à des particuliers : il faut des CGV accessibles avant l'achat, une politique de confidentialité (les e-mails sont collectés), un médiateur de la consommation, et une case à cocher de renonciation au droit de rétractation pour un accès immédiat.

## État (29/09/2026, soir)

**Page créée et remplie via l'API** (l'API accepte l'ajout d'une page d'information malgré la limite de l'interface du forfait gratuit) : https://lp.contactapaisement-mental.fr/0f1d6dac — étape « Mentions légales, CGV et confidentialité » (id 25634497, pageId 45140167) du tunnel « Page de vente ». Contenu = sections 1 à 3 ci-dessous, vérifié en ligne. Reste : remplacer les `[À COMPLÉTER]` (SIRET, adresse, médiateur, TVA) — renvoyer le contenu complet via `PUT /api/page-editor/pages/45140167/save` — puis relier la page depuis le pied de la page de paiement (éditeur uniquement) et activer la case à cocher.

## Où les mettre dans systeme.io (forfait gratuit : pas de nouvelle page)

Le forfait gratuit ne permet pas d'ajouter de page. On **regroupe tout dans la page « Mentions légales » existante** (`/mentions-lgales`), déjà reliée au pied de la page de paiement :

1. Ouvrir la page Mentions légales dans l'éditeur. Titre de la page : « Mentions légales, CGV et confidentialité ».
2. Remplacer son texte par les sections 1, 2 et 3 ci-dessous, à la suite, chacune avec son titre.
3. Dans le pied de la page de paiement (et de la page de capture), faire pointer « Conditions générales de vente » et « Politique de confidentialité » vers cette même page `https://lp.contactapaisement-mental.fr/mentions-lgales`, et « Contact » vers `mailto:yavo88@hotmail.com`.
4. Sur le formulaire de commande : activer la case à cocher d'acceptation des CGV, avec le texte de la section 4.

---

## 1. Mentions légales (texte complet à remplacer)

**Éditeur du site**
Yacine Nettour, entrepreneur individuel (EI), sous le nom commercial « Clarté Mentale »
Adresse : [À COMPLÉTER : adresse postale complète ou adresse de domiciliation]
SIREN : 822 033 577 — SIRET : 822 033 577 00021
N° de TVA intracommunautaire : FR00 822 033 577
E-mail : yavo88@hotmail.com
Directeur de la publication : Yacine Nettour

**Hébergement**
ITACWT Limited (systeme.io), 2 Cruise Park Rise, Tyrrelstown, Dublin 15, Irlande.

**Objet du site**
Vente de formations et de contenus numériques liés à la gestion du stress, au sommeil et au bien-être.

**Responsabilité**
Les informations proposées sur ce site ne remplacent pas un avis médical ou thérapeutique. En cas de troubles du sommeil persistants, consultez un professionnel de santé.

**Propriété intellectuelle**
Les textes, visuels, audios et vidéos de ce site et de la formation sont protégés. Toute reproduction ou diffusion sans autorisation écrite est interdite.

---

## 2. Conditions générales de vente (CGV)

**Article 1 — Vendeur**
Yacine Nettour, entrepreneur individuel (EI), nom commercial « Clarté Mentale », [adresse : À COMPLÉTER], SIRET 822 033 577 00021, e-mail : yavo88@hotmail.com.

**Article 2 — Objet**
Les présentes CGV s'appliquent à la vente en ligne du programme numérique « Quand le cerveau refuse de dormir » à des particuliers. Toute commande implique leur acceptation.

**Article 3 — Produit**
Programme en ligne composé de 4 modules et d'un bonus audio, accessible depuis un ordinateur, une tablette ou un téléphone. Ce programme propose des outils de bien-être. Il ne constitue ni un traitement médical ni une thérapie, et ne remplace pas l'avis d'un professionnel de santé.

**Article 4 — Prix**
27 € TTC (TVA incluse au taux applicable), paiement unique, sans abonnement. Le prix applicable est celui affiché au moment de la commande.

**Article 5 — Commande et paiement**
La commande se fait sur la page de paiement. Le paiement est effectué par carte bancaire ou Apple Pay via Stripe. Aucune donnée bancaire n'est conservée par le vendeur. La commande est confirmée par e-mail.

**Article 6 — Accès au programme**
L'accès est ouvert immédiatement après la confirmation du paiement, à vie, depuis l'espace membre. Les identifiants d'accès sont envoyés par e-mail.

**Article 7 — Droit de rétractation**
Conformément à l'article L221-28 13° du Code de la consommation, le droit de rétractation ne peut pas être exercé pour un contenu numérique fourni sans support matériel dont l'exécution a commencé, après accord préalable exprès du client et renoncement exprès à ce droit. En cochant la case prévue lors de la commande, le client demande l'accès immédiat au programme et reconnaît perdre son droit de rétractation dès le début de l'accès.

**Article 8 — Garantie « satisfait ou remboursé » de 7 jours**
Indépendamment de l'article 7, le vendeur accorde une garantie commerciale : si le client ne ressent aucune amélioration, il peut demander le remboursement intégral dans les 7 jours suivant l'achat, sans justification, par e-mail à yavo88@hotmail.com. Le remboursement est effectué avec le même moyen de paiement, et l'accès au programme est alors fermé.

**Article 9 — Garanties légales**
Le client bénéficie de la garantie légale de conformité des contenus numériques (articles L224-25-12 et suivants du Code de la consommation).

**Article 10 — Service client et réclamations**
Pour toute question ou réclamation : yavo88@hotmail.com.

**Article 11 — Médiation de la consommation**
En cas de litige non résolu avec le vendeur, le client peut recourir gratuitement au médiateur de la consommation : [À COMPLÉTER : nom, site web et adresse du médiateur auquel tu adhères, adhésion obligatoire pour vendre à des particuliers]. Le client peut aussi utiliser la plateforme européenne de règlement en ligne des litiges.

**Article 12 — Données personnelles**
Les données collectées lors de la commande sont traitées conformément à la Politique de confidentialité.

**Article 13 — Droit applicable**
Les présentes CGV sont soumises au droit français.

---

## 3. Politique de confidentialité

**Responsable du traitement**
Yacine Nettour, entrepreneur individuel (EI), « Clarté Mentale », [adresse : À COMPLÉTER], e-mail : yavo88@hotmail.com.

**Données collectées**
- Inscription au guide gratuit : adresse e-mail, prénom, pays.
- Achat : nom, prénom, adresse e-mail et informations nécessaires à la facturation. Les données de carte bancaire sont traitées directement par Stripe et ne sont jamais conservées par le vendeur.

**Finalités et bases légales**
- Envoyer le guide gratuit et les e-mails de conseils et d'information sur le programme : consentement donné lors de l'inscription, retirable à tout moment.
- Traiter les commandes, donner accès au programme, gérer la garantie et le service client : exécution du contrat.
- Respecter les obligations comptables et fiscales : obligation légale.

**Destinataires (sous-traitants)**
- systeme.io — ITACWT Limited, 2 Cruise Park Rise, Tyrrelstown, Dublin 15, Irlande : hébergement du site, des e-mails et de l'espace membre.
- Stripe : traitement des paiements.
Les données ne sont ni vendues ni louées. Si un sous-traitant transfère des données hors de l'Union européenne, ce transfert est encadré par les garanties prévues par le RGPD (clauses contractuelles types).

**Durée de conservation**
- Inscrits sans achat : jusqu'à la désinscription, et au plus 3 ans après le dernier contact.
- Clients : pendant la durée d'accès au programme. Les pièces comptables sont conservées 10 ans.

**Tes droits**
Tu disposes d'un droit d'accès, de rectification, d'effacement, d'opposition, de limitation et de portabilité de tes données. Pour les exercer : yavo88@hotmail.com. Chaque e-mail contient un lien de désinscription. Tu peux aussi adresser une réclamation à la CNIL (cnil.fr).

**Cookies**
Le site utilise les cookies techniques nécessaires à son fonctionnement (panier, connexion à l'espace membre). [À COMPLÉTER si tu ajoutes un outil de mesure d'audience ou publicitaire : bandeau de consentement obligatoire.]

---

## 4. Case à cocher du formulaire de commande

> J'accepte les conditions générales de vente. Je demande l'accès immédiat au programme et je reconnais perdre mon droit de rétractation dès le début de l'accès (art. L221-28 13° du Code de la consommation). La garantie « satisfait ou remboursé » de 7 jours reste valable.
