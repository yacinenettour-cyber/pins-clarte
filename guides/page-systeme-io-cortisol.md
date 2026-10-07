# Page de capture « Plan anti-cortisol en 7 jours » — à créer dans systeme.io

Fichiers à importer dans systeme.io :
- `guide-cortisol-7-jours.pdf` : le guide envoyé par e-mail (10 pages).
- `couverture-guide-cortisol.png` : l'image de la page.

## Création (5 à 10 minutes, depuis un ordinateur de préférence)

1. Dans systeme.io, ouvre le tunnel de ton guide actuel (« Quand le cerveau refuse de dormir ») et **duplique-le**.
2. Dans la copie, remplace l'image par `couverture-guide-cortisol.png` et les textes par ceux ci-dessous.
3. Dans l'étape de remerciement et l'e-mail automatique, remplace le PDF par `guide-cortisol-7-jours.pdf`.
4. Donne à la page une adresse courte, par exemple `lp.contactapaisement-mental.fr/cortisol`.
5. Dans les réglages SEO de la page : titre, description et image de partage (textes ci-dessous). Ta page actuelle n'a ni titre ni image de partage : à remplir aussi, c'est ce que Pinterest affiche quand on ouvre le lien.
6. **Envoie l'adresse de la page à Claude** : il branche les pins concernés dessus.

## Textes de la page

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
Entre ton e-mail : le plan arrive dans ta boîte mail en 2 minutes.

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

**Objet** : Ton plan anti-cortisol en 7 jours est là

Bonjour,

Voici ton plan anti-cortisol en 7 jours : [lien / pièce jointe du PDF].

Mon conseil pour démarrer : commence demain matin par le jour 1, 10 minutes de lumière dans l'heure qui suit ton lever. C'est le geste le plus simple et souvent celui qu'on sent le plus vite.

Coche ta journée dans le tableau de la page 10, et garde les 3 gestes qui te font le plus de bien.

À très vite,
Clarté Mentale

## Pour le pipeline (déjà préparé le 07/10/2026, inactif)

- `pins.yml` : il suffit de remplir `LIEN_GUIDE_CORTISOL = "https://…"` avec l'adresse de la page, puis de pousser sur `main`.
- Thèmes reliés : `energie` et `alimentation`, plus 4 pins cortisol d'autres thèmes ; 24 pins ont déjà leur fin de description « plan » (`description_guide_cortisol`), 5 pins hors sujet restent sans lien (`"guide": "aucun"`).
- Carte sur l'image : « PLAN GRATUIT · lien dans l'épingle / « Le plan anti-cortisol en 7 jours » : / 7 gestes simples + tableau de suivi ». Si le titre de la page change, adapter `LIGNES_CARTE_CORTISOL`.
- Les vidéos (`videos.yml`) ne sont pas encore reliées au plan.
