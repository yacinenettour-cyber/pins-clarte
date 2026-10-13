# Audit complet du site (13/10/2026)

Demande de l'utilisateur : « Analyse tout mon site, prends le temps de bien réfléchir et regarde les points faibles ».
Quatre analyses en lecture seule (technique, contenu et confiance santé, design et mobile, parcours et conversion),
plus les données réelles (Search Console, Cloudflare, en-têtes du site en ligne). Les constats graves ont été revérifiés
à la main avant d'être retenus. Captures : scratchpad de la session (non conservées dans le dépôt).

## Bilan général

Le site est techniquement sain : 0 erreur HTML (W3C), 0 erreur axe-core dans les deux thèmes, aucun débordement de
320 à 1366 px, LCP mobile 1,0 à 1,7 s, CLS 0, pages de 137 à 338 Ko, canonicals, sitemap, robots, redirections
http → https et sans-www → www correctes. Rien de technique n'empêche l'indexation : la lenteur vient de l'âge du domaine
(4 jours), de l'absence de liens externes et du sujet santé.

## Points faibles retenus (du plus grave au moins grave)

| # | Gravité | Point | Preuve | Correction |
|---|---|---|---|---|
| 1 | Haute | Des épingles mènent à un article qui ne traite pas leur sujet | « Massage des pieds », « 3 lignes de gratitude » → routine du soir ; « Collation 17h » → alimentation ; « recherches au lit », « soucis d'argent » → ruminations : mots absents des articles | Contrôle par script ; retirer `article` ou compléter l'article |
| 2 | Haute | Test GAD-7 de 10 à 14 : le guide reste proposé, or il ouvre la séquence d'e-mails qui présente la formation | `test.js` : seul « severe » masque l'offre | Ne plus proposer le guide dès 10 (décision utilisateur) |
| 3 | Haute | Les articles ne disent pas qui écrit (électricien, non relu) | « électricien » absent des 14 articles | Ligne sous la signature de chaque article |
| 4 | Moyenne-haute | Accueil centré sur le cortisol (H1, H2, FAQ, « 7 leviers validés », tuile « alimentation anti-cortisol » non sourcée), alors que l'offre est un guide sommeil et que l'article dédié vise ce mot-clé | `accueil.html:317`, `:357`, `:499` | Recentrer sur le soir / le mental, « étudiés » au lieu de « validés », lien vers l'article |
| 5 | Moyenne | Délai « Quand consulter » différent selon les articles (1 mois / 3 mois / 3-4 semaines) | `routine-du-soir:74`, `cortisol-et-sommeil:93`, `baisser-son-cortisol:144` | Une seule formulation vérifiée sur ameli |
| 6 | Moyenne | L'accueil ne relie que 6 articles sur 14 | `construire.py:744` | Relier les 14 |
| 7 | Moyenne | Outils (minuteur, audios, test) sous plus d'un écran de texte sur téléphone | minuteur : bouton « Commencer » à ~1 690 px | Outil en premier, explications ensuite |
| 8 | Moyenne | Premier écran d'article sur téléphone : titre + pastilles, photo à ~1 000 px | capture `/angoisse-le-soir/` à 360 px | Photo sous le titre, une seule pastille |
| 9 | Moyenne | Origine Pinterest perdue quand le visiteur clique vers le guide | liens guide réécrits en `utm_source=site` | Recopier l'origine dans les liens guide |
| 10 | Moyenne | Appel complet au guide après la FAQ (à ~80 % de la page) | mesures à 360 px | Le placer avant la FAQ |
| 11 | Moyenne | Guide gratuit et formation portent le même nom ; page formation qui promet un peu trop | `site.json` bloc formation | Noms distincts, verbes prudents |
| 12 | Moyenne | Activité physique : « intense = plus de bénéfices » d'un côté, « douce les jours tendus » de l'autre | `calmer-son-systeme-nerveux:93` | Phrase de pont |
| 13 | Moyenne | Passages répétés d'un article à l'autre (Balban 2023 dans 5 articles) ; sujets à venir n° 6 et 7 qui recoupent des articles existants | comparaison de phrases | Un article « propriétaire » par étude ; revoir les sujets 6 et 7 |
| 14 | Basse | 4 études citées sans le nom de la revue ; phrases longues ; quelques nuances à ajouter (nerf vague « une minute », tableau alimentation) | voir rapport | Corrections ponctuelles |
| 15 | Basse | Pages carrefour peu originales (/articles/, charge mentale et burn-out, guides gratuits) | 40-48 % de texte repris | Introduction propre à chaque page |
| 16 | Basse | Données structurées : `hasPart` incomplet sur /articles/, `courseWorkload` faux ; dates du plan du site décalées sur 7 pages | `construire.py:866`, `:1004` | ItemList ; une seule source de date |
| 17 | Basse | Petits défauts mobiles : renvois de sources minuscules à toucher, « GAD- / 7 » coupé, textes à 11-13 px, bouton « haut de page » qui recouvre une carte, focus peu visible sur les pastilles, miniature d'épingle trop lourde | captures et mesures | Ajustements CSS |
| 18 | Basse | Épingles « cortisol » vers une page sans suite d'e-mails ; contact en adresse Hotmail | `historique.json`, mentions légales | Décisions de l'utilisateur |
