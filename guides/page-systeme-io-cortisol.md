# Page de capture « Plan anti-cortisol en 7 jours » — systeme.io

## État au 07/10/2026 : page créée et en ligne (par Claude, via l'API publique systeme.io)

- **Page de capture** : https://lp.contactapaisement-mental.fr/63d489c7 (tunnel « optin » 7680510, étape 25727831, page 45404514).
- **Page de remerciement** : https://lp.contactapaisement-mental.fr/e7346dbb (étape 25727832, page 45404515) : bouton « Télécharger mon plan » vers le PDF (`guides/guide-cortisol-7-jours.pdf` servi par jsDelivr, sha complet `452f338f6c75461db20b2e8367fd534cfbc24c4d` — jamais un sha court : erreur 403 « Package size exceeded ») + bouton secondaire vers le guide sommeil (`/tonguide?utm_source=plan-cortisol&utm_medium=merci`).
- **Livraison par téléchargement immédiat, pas par e-mail** : le plan gratuit systeme.io bloque la création de tags (422), de campagnes (403) et de nouvelles règles d'automatisation (« Automation rules limit reached »). Les textes de la page promettent donc un téléchargement immédiat, jamais un e-mail. L'e-mail de livraison est prêt dans systeme.io (e-mail d'automatisation 13068257, texte ci-dessous) mais n'est relié à rien. La règle existante 2045419 (guide sommeil) n'a pas été modifiée pour ne pas mélanger les deux listes d'inscrits.
- **Limites de l'API publique** : le bloc Image n'accepte qu'une description en anglais (image générée par systeme.io), pas d'image envoyée par nos soins ; la couleur de la page est tirée au hasard à chaque enregistrement ; pas de réglage de l'adresse (slug), du texte du champ e-mail ni du SEO de la page. Les blocs « IconFeature » n'affichaient pas leur texte : remplacés par des blocs « Card » (`cardLayout: icon-top`). L'image du haut (photo lumière du matin + tisane, sans texte) n'apparaît que sur ordinateur ; sur mobile le formulaire arrive directement après la liste.
- **Retouches possibles à la main dans l'éditeur systeme.io** (facultatives) : texte du champ e-mail « Your email address » → « Ton adresse e-mail » ; image du haut → `couverture-guide-cortisol.png` ; réglages SEO (titre, description, image de partage, voir plus bas). **Ne pas changer l'adresse de la page une fois les pins branchés** : les épingles déjà publiées garderaient l'ancienne adresse (modification des épingles impossible par l'API).

## Textes de la page

Proposition d'origine ; la page en ligne reprend ces textes, enrichis (section douleur, 7 cartes « Jour 1 » à « Jour 7 », FAQ, appel final), avec une livraison par téléchargement.

**Titre principal**
Le plan anti-cortisol en 7 jours

**Sous-titre**
7 gestes simples, 10 à 15 minutes par jour, pour aider ton corps à sortir du mode alerte.

**Liste (sous l'image)**
- Comprendre le rythme du cortisol en une minute
- Un geste concret par jour : lumière, respiration, assiette, mouvement, pauses, soirée, sommeil
- Un tableau de suivi à cocher sur 7 jours
- Sans matériel, sans régime

**Champ e-mail — texte au-dessus**
Téléchargement immédiat après ton inscription. Aucun spam. (Ne pas promettre d'e-mail tant que la livraison par e-mail n'est pas reliée.)

**Bouton**
Recevoir mon plan gratuit

**Sous le bouton**
🔒 100 % gratuit • Aucun spam • Désinscription en 1 clic

**Mention en petit**
Repères de bien-être, pas un avis médical.

## Réglages SEO de la page

- Titre : `Plan anti-cortisol en 7 jours — guide gratuit | Clarté Mentale`
- Description : `7 gestes simples pour aider ton corps à sortir du mode alerte : lumière, respiration, assiette, pauses et sommeil. Guide gratuit avec tableau de suivi.`
- Image de partage : `couverture-guide-cortisol.png`

## E-mail de livraison

Prêt dans systeme.io (e-mail d'automatisation 13068257), non relié : à brancher sur l'inscription au formulaire du tunnel 7680510 si le compte passe à un plan payant (ou si la règle existante est modifiée), puis remettre la promesse « dans ta boîte mail » sur la page.

**Objet** : Ton plan anti-cortisol en 7 jours est là

Bonjour,

Voici ton plan anti-cortisol en 7 jours : [lien / pièce jointe du PDF].

Mon conseil pour démarrer : commence demain matin par le jour 1, 10 minutes de lumière dans l'heure qui suit ton lever. C'est le geste le plus simple et souvent celui qu'on sent le plus vite.

Coche ta journée dans le tableau de la page 10, et garde les 3 gestes qui te font le plus de bien.

À très vite,
Clarté Mentale

## Pour le pipeline (actif depuis le 07/10/2026)

- `pins.yml` : `LIEN_GUIDE_CORTISOL = "https://lp.contactapaisement-mental.fr/63d489c7"` (activé avec l'accord de l'utilisateur ; vider l'adresse pour désactiver). Simulation du 07/10 avec cette adresse : 34 pins à venir vers le plan, 68 visuels avec la carte cortisol, 0 sans photo, 0 chevauchement, descriptions ≤ 495 caractères ; poids de rotation energie/alimentation passés à 1,0.
- Thèmes reliés : `energie` et `alimentation`, plus 4 pins cortisol d'autres thèmes ; 24 pins ont déjà leur fin de description « plan » (`description_guide_cortisol`), 5 pins hors sujet restent sans lien (`"guide": "aucun"`).
- Carte sur l'image : « PLAN GRATUIT · lien dans l'épingle / « Le plan anti-cortisol en 7 jours » : / 7 gestes simples + tableau de suivi ». Si le titre de la page change, adapter `LIGNES_CARTE_CORTISOL`.
- Les vidéos (`videos.yml`) ne sont pas encore reliées au plan.
