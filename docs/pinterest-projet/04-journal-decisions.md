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

## 9. Connexion à Pinterest Analytics et diagnostic de performance (28/09/2026)

**Déclencheur** : "mon compte Pinterest ne s'est pas amélioré, mes stats n'augmentent pas, fais quelque chose" — suivi de "connecte-toi à mon compte Pinterest" après que Claude a d'abord (à tort) répondu ne disposer d'aucun moyen de connexion. Un connecteur Composio avec un toolkit `pinterest` existait bien et a permis une vraie connexion OAuth (voir `01-architecture-technique.md` pour le détail technique).

**Diagnostic obtenu avec les vraies données (profil, analytics 90 jours, top pins, tableaux)** :

1. **Chute de ~70% des impressions entre fin juillet et début septembre 2026** (26 600/semaine au pic du 30/06-27/07, jusqu'à 6 800/semaine fin août-début septembre), **entièrement antérieure à ce dépôt Git** (premier commit le 25/09/2026) et aux premières entrées de `historique.json` (22/09/2026). **Cause confirmée par l'utilisateur** : simple baisse d'activité de sa part sur le compte durant cette période (moins de publications manuelles), pas un problème algorithmique ni une pénalité Pinterest. Cohérent avec la reprise observée dès la mise en place de l'automatisation (15/09 → 21/09 : +35%).
2. **Tendance des 2 dernières semaines pleines positive** (+20% impressions, +19% enregistrements) mais partant d'un niveau très bas — loin d'avoir rattrapé le pic de juillet. Donc "les stats n'augmentent pas" est partiellement faux à très court terme, mais l'écart avec le pic reste massif.
3. **Les 8 pins avec le plus d'enregistrements du compte sont tous antérieurs à cette session** (créés décembre 2025 à juin 2026) et partagent un format qu'on n'utilise plus depuis la grande réécriture SEO : titres à chiffre/listicle ("5 Clés pour Vaincre la Procrastination", "Les 9 signes d'un cortisol élevé"), 8-14 hashtags avec emojis, structure infographie plutôt que prose narrative. **Décision de l'utilisateur** : adapter le format des futurs pins à ce gabarit (voir `03-regles-editoriales.md` section 6-7, mis à jour en conséquence).
4. **Quasiment aucun clic sortant vers la formation** : 40 clics sur 90 jours (taux 0,02%) sur 177 016 impressions. **Explication de l'utilisateur, pas un bug** : la plupart des meilleurs pins historiques n'ont pas de lien parce que leur contenu n'a justement pas de rapport avec la formation — même logique que `THEMES_SANS_LIEN`, mais appliquée par l'utilisateur au cas par cas sur le contenu réel de chaque pin à l'époque, pas seulement par thème/board. Sur les 8 pins les mieux enregistrés : les 3 sur les boards `procrastination`/`alimentation` sans lien collent à la règle actuelle ; mais certains pins sans lien sont aussi sur des boards qu'on considère aujourd'hui "avec lien" (`systemenerveux`, `fatiguementale`) — confirme que la décision lien/pas-de-lien est fondamentalement une question de **contenu**, le thème n'étant qu'un proxy imparfait (déjà observé le 28/09 avec le pin `energie` déguisé en alimentation). Le faible taux de clic global n'est donc pas anormal, c'est en grande partie voulu.
5. **12 tableaux existent réellement sur le compte, le pipeline n'en gère que 9.** Les 3 tableaux orphelins : `Routine anti-âge quotidienne` (4 pins, complètement hors-sujet), `🧠 Fatigue & Causes Biologiques` (8 pins, chevauche fatiguementale/energie), `Enregistrements rapides` (0 pin, probablement le tableau par défaut Pinterest). Point ouvert, pas encore traité.
6. **368 pins au total sur le compte réel, contre 58 publiés par ce pipeline automatisé** depuis le 22/09/2026 — confirme qu'environ 310 pins pré-existaient à cette automatisation, issus d'un processus antérieur inconnu (pas de trace dans ce dépôt).

**Action immédiate** : mise à jour de `03-regles-editoriales.md` (titres à chiffre privilégiés, 8-12 hashtags au lieu de 5, structure avec puces emoji optionnelle) et de `README.md`/`CLAUDE.md` en miroir. Reste à faire : rédiger un lot pilote de pins au nouveau format pour validation, puis décider si on convertit le reste de la banque non publiée ou si la nouvelle règle s'applique seulement aux ajouts futurs.

**Leçon retenue** : ne jamais affirmer l'absence d'un accès/outil sans l'avoir activement recherché — Claude a d'abord dit ne pas pouvoir se connecter à Pinterest sans avoir vérifié le connecteur Composio déjà actif dans la session, alors que celui-ci proposait bien un toolkit Pinterest fonctionnel.

## 10. Ajout du format infographie (`points_image`, 28/09/2026)

**Déclencheur** : "N'oublie pas de faire des infographies ça marche bien" — suite au diagnostic Analytics (section 9), qui avait identifié que les 8 pins historiques les plus performants du compte sont des infographies (titre + liste numérotée visible sur l'image), pas de simples photos avec une phrase. Le pipeline ne savait dessiner qu'une seule ligne de texte (`dessiner_image()`).

**Action** : ajout de `dessiner_infographie()` dans `pins.yml`, appelée automatiquement quand un pin a un champ `points_image` (liste de 2-4 points courts) — sinon le rendu simple habituel reste utilisé, aucune régression sur les pins existants. Toujours un rendu texte PIL/Poppins fiable, jamais de texte généré par une IA d'image (règle déjà établie, voir README section "Génération d'images"). L'assombrissement du fond démarre plus haut (y≈250 au lieu de y≈430) pour laisser la place à la liste.

**Peuplement** : `points_image` extrait automatiquement des puces 👉 déjà présentes dans les descriptions réécrites le 28/09/2026 (section 9) — 124 pins concernés sur les 205 déjà au nouveau format texte. Choix délibéré de ne pas forcer ce champ sur tous les pins : uniquement là où un vrai contenu de liste (2-4 éléments courts, 5-85 caractères chacun) existait déjà, pour éviter une infographie avec des points trop longs ou mal coupés.

**Vérification avant déploiement** : rendu réel testé (pas juste le prototype) à partir du code exact de `pins.yml`, sur plusieurs fonds (sombre et clair) et plusieurs thèmes (posturesantistress, systemenerveux, procrastination, alimentation) — lisible et cohérent avec la charte dans tous les cas testés.

## Point ouvert à ce jour

**Résolu le 28/09/2026** : accès en lecture aux vraies données Pinterest Analytics obtenu via un connecteur Composio (voir section 9 ci-dessus et `01-architecture-technique.md`). Les règles de `03-regles-editoriales.md` sur les titres/hashtags ont été mises à jour en conséquence. La chute de trafic de juillet-août est expliquée (baisse d'activité de l'utilisateur, pas un problème technique) et le faible taux de clics sortants n'est pas un bug (la plupart des meilleurs pins n'ont intentionnellement pas de lien, contenu hors périmètre formation). Reste ouvert : la connexion Composio semble propre à la session (à revérifier en début de session future, `COMPOSIO_MANAGE_CONNECTIONS` action `list`) ; les 3 tableaux orphelins (`Routine anti-âge quotidienne`, `🧠 Fatigue & Causes Biologiques`, `Enregistrements rapides`) n'ont pas encore été traités (priorité non choisie par l'utilisateur) ; convertir le reste de la banque non publiée (~180 pins) au nouveau format titres/hashtags reste à faire si l'utilisateur valide le lot pilote de 10 pins.
