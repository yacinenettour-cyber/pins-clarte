# Journal des décisions — session d'audit du 27 septembre 2026

Ce fichier retrace le contexte et le raisonnement derrière chaque règle établie dans `03-regles-editoriales.md`, pour qu'une future session comprenne le "pourquoi" sans avoir à tout redemander à l'utilisateur.

## 1. Audit initial anti-duplicata

**Demande** : "je veux 0 duplicata Pinterest ne tolère pas les copies."

**Constat** : aucun doublon exact dans les 231 pins de départ, mais 4 paires de titres au gabarit quasi-identique (un seul mot changé), ex. *"Somatisation du stress : ce mal de dos..."* vs *"...ce mal de tête..."*. Corrigées par reformulation. Aucun des titres concernés n'était encore publié.

**Limite reconnue** : pas d'accès aux vraies statistiques Pinterest (impressions/enregistrements/clics) depuis cet environnement — aucun connecteur Pinterest disponible. La demande initiale de "regarder ce qui marche pour s'en inspirer" n'a donc jamais pu être satisfaite avec de vraies données de performance ; les stats n'ont jamais été fournies par l'utilisateur malgré la demande.

## 2. Retrait de 11 pins "recette/organisation cuisine"

**Déclencheur** : l'utilisateur a partagé une capture d'écran de son compte Pinterest réel montrant des pins publiés (meal prep, eaux infusées, légumes rôtis, mijoteuse, jus frais, petit-déjeuner la veille...) et a signalé qu'ils "ne correspondent pas à [son] compte" (compte centré sur stress/procrastination/sommeil).

**Analyse** : distinction faite entre deux types de contenu "alimentation" dans la banque — (a) 11 pins purement recette/organisation sans aucun lien avec le stress, (b) 11 autres pins alimentation avec un vrai lien stress/système nerveux. L'utilisateur a choisi de retirer uniquement (a) et de garder (b), à condition qu'ils soient réellement centrés sur le stress.

**Action** : suppression des 11 pins et de leurs images associées (`images_manuelles/`). 3 d'entre eux étaient déjà publiés sur le compte réel — suppression manuelle nécessaire par l'utilisateur directement sur Pinterest (hors de portée du dépôt).

## 3. Recentrage strict du board "Alimentation et stress"

**Déclencheur** : "Mon tableau c'est alimentation et stress donc tu dois utiliser l'alimentation juste pour diminuer le stress."

**Constat** : parmi les pins routés vers ce board (via premier hashtag), 5 avaient en réalité pour sujet le sommeil ou l'énergie, pas le stress (ex. "Alimentation sommeil : ces aliments du soir...", "Café : jusqu'à quelle heure en boire quand on dort mal"). Le premier hashtag de leur description (`#alimentation`, `#cafeine`, `#alcool`) les routait à tort vers le board alimentation alors que leur contenu parlait de sommeil.

**Action** : réordonnancement des hashtags de ces 5 pins pour qu'ils routent vers `sommeil`/`energie`, là où leur contenu correspond réellement. Le board alimentation ne contient plus que 8 pins, tous explicitement liés au stress.

## 4. Réécriture complète de 188 pins (titres, descriptions, SEO, CTA)

**Déclencheur** : "Je veux que les titres soient plus travaillé et les descriptions plus longue et seo pour chaque épingles pinterest dorénavant" — puis confirmation de retravailler aussi les 220 pins existants, pas seulement les futurs ajouts. Suivi de "Et tu me varie les cta."

**Méthode** : travail réparti sur 8 agents en parallèle, un par lot thématique, avec consignes strictes (préserver les hashtags à l'identique, ne jamais toucher aux pins déjà publiés, corps de description 380-450 caractères, titres variés non-templatés, CTA variés). Résultat fusionné et revérifié dans son intégralité (0 doublon, 0 quasi-doublon, longueurs, routage de thème préservé).

**Résultat** : corps de description moyen passé de ~300 à ~420 caractères sur les pins non publiés. Les 32 (puis 41, le pipeline continuant de publier en parallèle) pins déjà en ligne sur Pinterest n'ont pas été touchés.

## 5. Sauvegarde du prompt système SEO pour Make.com

**Déclencheur** : l'utilisateur a fourni un prompt système complet destiné à un futur module IA dans un scénario Make.com (analyse d'image → génération de métadonnées Pinterest en JSON), avec l'instruction "Enregistre cela c'est important."

**Action** : sauvegardé verbatim dans `prompts/system-prompt-pin-seo.md`. Signalé que ce flux (image → texte) est l'inverse du flux actuellement actif (texte → image via `pins.json`), et que les deux ne sont pas connectés — une décision explicite de l'utilisateur sera nécessaire avant de les relier.

## 6. Lien de destination conditionnel selon le périmètre réel de la formation

**Déclencheur** : "tu ne mets pas de lien de destination sur les épingles qui n'ont pas de point commun avec ma formation systeme.io genre certaines épingles sur l'alimentation, la procrastination."

**Clarification obtenue** (les 9 thèmes n'ont pas tous été présumés) : la formation couvre `sommeil`, `systemenerveux`, `fatiguementale`, `posturesantistress`, `blocagemental`, `somatisation`, `energie` — mais **pas** `alimentation` ni `procrastination`, malgré le fait que la procrastination soit un des piliers éditoriaux du compte. Distinction importante : le périmètre éditorial (ce que le compte publie pour construire son audience) est plus large que le périmètre commercial (ce que la formation vend réellement).

**Action** : ajout de `THEMES_SANS_LIEN = {"alimentation", "procrastination"}` dans `pins.yml` et `videos.yml` — le champ `lien` envoyé à Make devient vide pour ces thèmes. Réécriture des 18 descriptions concernées pour retirer toute mention de "guide gratuit"/"clique sur cette épingle" (incohérent sans lien de destination), remplacée par des CTA adaptés (enregistrement Pinterest ou fin purement informative).

## 7. Mise en place de la mémoire de projet (CLAUDE.md + docs/pinterest-projet/)

**Déclencheur** : "depuis claude code a tu accès au projet car je veux que tu garde en mémoire cela quand je ferme cette conversation" puis "génère-moi tous les fichiers .md que tu juges utiles... pour créer un projet Pinterest."

**Clarification apportée** : pas de mémoire de conversation à conversation, mais deux mécanismes de persistance distincts et complémentaires :
- `CLAUDE.md` (racine du dépôt) : résumé opérationnel des règles, chargé automatiquement par Claude Code au démarrage de toute session future **sur ce dépôt**.
- `docs/pinterest-projet/` (ce dossier) : documentation complète et autoportante (vue d'ensemble, architecture, tableaux, règles éditoriales, ce journal), pensée pour être chargée comme connaissance de projet indépendamment du dépôt Git ou d'une conversation Claude Code spécifique — utilisable dans un Claude Project ou toute autre conversation qui a besoin du contexte complet.

## 8. Correction du périmètre du lien : `energie` et `fatiguementale` exclus (28/09/2026)

**Déclencheur** : l'utilisateur a partagé une capture d'écran d'un pin publié sur le compte réel, "Le trou d'énergie de 11h se joue souvent dans ton assiette du matin", avec un bouton "Visiter" actif vers la page de capture, et a signalé : "le guide ne parle que de stress et de sommeil, pourquoi tu as mis un lien sur cette épingle ?"

**Root cause identifiée** : ce pin a pour premier hashtag `#energie` (theme = `energie`, pas encore dans `THEMES_SANS_LIEN` à ce moment-là), mais son contenu réel est 100 % alimentation/petit-déjeuner (composition du repas du matin pour stabiliser l'attention) — exactement le type de contenu que la règle du board `alimentation` interdit d'habitude, sauf qu'ici il avait été tagué `#energie` en premier au lieu de `#alimentation`, ce qui lui a fait éviter cette restriction tout en récupérant un lien vers un guide qui ne traite pas ce sujet. Deux angles morts cumulés : (a) le premier hashtag ne garantit pas la cohérence du contenu réel avec le thème déclaré, (b) le périmètre `THEMES_SANS_LIEN` présumé (`alimentation`, `procrastination` seuls hors périmètre) était trop étroit.

**Clarification obtenue** : la formation ne couvre en réalité que **le sommeil et les mécanismes du stress au sens large** (nervosité, tensions physiques, blocages mentaux, postures) — pas l'énergie/fatigue en général, même si ces thèmes sont adjacents au stress dans l'esprit du compte. Option retenue parmi 3 proposées : "Sommeil + stress au sens large" — `sommeil`, `systemenerveux`, `somatisation`, `blocagemental`, `posturesantistress` gardent le lien ; `energie` et `fatiguementale` rejoignent `alimentation`/`procrastination` dans les thèmes sans lien.

**Action** :
- `THEMES_SANS_LIEN` mis à jour dans `pins.yml` et `videos.yml` : `{"alimentation", "procrastination", "energie", "fatiguementale"}`.
- Audit de `pins.json` (regex sur "guide gratuit", "à un clic", "dans le guide"...) : 11 pins thème `energie`/`fatiguementale` trouvés avec un CTA promettant un accès au guide — tous réécrits avec une fin informative ou un rappel actionnable, sans promesse de clic. `videos.json` audité, aucun cas trouvé.
- Le pin déjà publié ("Le trou d'énergie de 11h...") a aussi été corrigé dans `pins.json` par cohérence de la banque, mais **sans effet sur la publication Pinterest déjà en ligne** (texte jamais relu une fois publié, règle 7 de `03-regles-editoriales.md`) — sa suppression/correction sur Pinterest reste une action manuelle pour l'utilisateur s'il le souhaite.

**Leçon retenue pour la suite** : avant d'accepter un CTA "guide gratuit" sur un nouveau pin, vérifier que son **contenu réel** correspond à ce que la formation couvre vraiment, pas seulement son thème/premier hashtag — un pin peut être maquillé (hashtag de tête changé) pour échapper à une règle de board tout en gardant un problème de fond.

## Point ouvert à ce jour

**Pas de données Pinterest Analytics réelles disponibles.** Toutes les décisions de contenu de cette session reposent sur les bonnes pratiques Pinterest génériques et la logique déjà en place, pas sur des chiffres réels de performance (enregistrements, clics, impressions par pin/board). Dès que l'utilisateur peut fournir un export ou une liste des pins/thèmes qui performent le mieux, une vraie passe d'optimisation basée sur des données réelles reste à faire.
