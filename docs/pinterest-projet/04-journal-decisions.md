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

## 11. Clarification du rythme des vidéos : 1×/jour (7×/semaine) à 18h30 heure de Paris (29/09/2026)

**Déclencheur** : demande de préciser l'horaire de publication des Video Pins. Confirmation obtenue : 1 vidéo par jour, tous les jours (7×/semaine), à 18h30 heure de Paris — pas un rythme hebdomadaire réduit.

**Action** : `01-architecture-technique.md` mis à jour (l'ancien horaire indicatif `~19h37 UTC` remplacé par `18h30 heure de Paris`, avec la conversion UTC pour l'été/hiver si le fuseau `Europe/Paris` n'est pas réglable directement dans cron-job.org).

**Point important** : `videos.yml` n'a pas de déclencheur `schedule` natif GitHub Actions — seulement `workflow_dispatch` (voir §"Déclenchement" de `01-architecture-technique.md`). L'horaire réel dépend entièrement de la tâche configurée côté cron-job.org (service externe), que Claude Code n'a pas les moyens d'atteindre ou de modifier depuis cette session (aucun connecteur cron-job.org disponible). **Reste une action manuelle pour l'utilisateur** : créer/ajuster dans son tableau de bord cron-job.org une tâche qui appelle l'endpoint `workflow_dispatch` de `videos.yml` une fois par jour à 18h30 (Europe/Paris si l'option de fuseau existe, sinon 16h30 UTC en été / 17h30 UTC en hiver).

## 12. Diagnostic Analytics n°2 : le vrai levier de croissance identifié (29/09/2026)

**Déclencheur** : "Quelles mesures peut-on vraiment prendre pour augmenter le compte Pinterest ?" — l'utilisateur refuse la conversion systématique au format infographie ("je veux faire un test avant") et demande de creuser plutôt les deux autres pistes : les vraies données Analytics et le nettoyage des tableaux orphelins.

**Découverte principale** : les 6 pins avec le plus d'impressions sur les 30 derniers jours (`PINTEREST_GET_TOP_PINS`, triés IMPRESSION) sont tous des pins pré-automatisation (créés déc. 2025 à mai 2026, avant ce dépôt) — le meilleur fait 8534 impressions / 104 saves. Vérification systématique de leur détail (`PINTEREST_GET_PIN`) : **les 6 sont du type natif Pinterest `creative_type: "IDEA"`** (Idea Pin / épingle multi-format), pas de simples images statiques comme celles produites par le pipeline actuel. Ils partagent aussi : titres à chiffre + emoji, description structurée avec émojis numérotés (1️⃣2️⃣3️⃣) ou puces 👉, CTA "📌 Sauve cette épingle pour...", et 8-10 hashtags mis bout à bout en fin de description. Cette dernière partie est déjà en cours d'adoption (voir §9-10) ; le format "Idea Pin" natif, lui, ne l'est pas du tout — c'est un flux de production entièrement différent de ce que `pins.yml` sait faire aujourd'hui (image statique + webhook Make).

**Découverte secondaire, correction de doc** : un accès en écriture Pinterest existe bien via Composio (`PINTEREST_CREATE_PIN`, `PINTEREST_UPDATE_PIN`, `PINTEREST_DELETE_BOARD`) — contrairement à ce que notait `01-architecture-technique.md` jusqu'ici ("aucun accès en écriture trouvé/testé"), corrigé en conséquence. Nuance importante : `PINTEREST_CREATE_PIN` supporte image/carousel(2-5 images)/vidéo mais ne mentionne pas explicitement le format `IDEA` natif repéré ci-dessus — à vérifier avant de compter dessus comme solution. Cet accès en écriture n'a été utilisé pour aucune action réelle sur le compte (aucune création/suppression), toute utilisation reste soumise à validation explicite de l'utilisateur vu qu'il s'agit d'un compte avec de vrais abonnés.

**Tendance du compte (13-27/09, `PINTEREST_GET_ACCOUNT_ANALYTICS`, 13 jours)** : 17 993 impressions au total, moyenne quotidienne passant de ~1325/j (semaine du 15-21/09) à ~1453/j (22-27/09), soit +~10%. 153 saves au total (~12/j), taux d'engagement moyen 6,35% (sain). Clics sortants quasi nuls (16 sur 13 jours) et à 0 les 8 premiers jours avant d'apparaître à partir du 24/09 — cohérent avec le fait que la majorité des thèmes automatisés n'a pas de lien de destination (règle `THEMES_SANS_LIEN`).

**Tableaux orphelins confirmés avec les vraies données** (`PINTEREST_LIST_BOARDS`) : `Enregistrements rapides` (0 pin, sans impact), `Routine anti-âge quotidienne` (4 pins, toujours hors-sujet), `🧠 Fatigue & Causes Biologiques` (8 pins, chevauche toujours `Routine anti fatigue`/`Stress & fatigue mentale`). Techniquement déplaçables/supprimables maintenant (écriture confirmée), mais **aucune action prise** — décision et feu vert explicites de l'utilisateur requis avant de toucher au compte réel.

**Point ouvert pour la suite** : décider si on teste le format carousel (2-5 images) via `PINTEREST_CREATE_PIN` comme proxy du format Idea Pin qui performe, en parallèle du test infographie déjà demandé par l'utilisateur (qui refuse la conversion systématique, veut un test d'abord) ; et décider du sort des 3 tableaux orphelins.

## 13. Décision : 1 Idea Pin/jour (substitut carousel), tableaux orphelins gardés tels quels (29/09/2026)

**Décisions de l'utilisateur suite à la section 12** :
- **Tableaux orphelins** : gardés tels quels, l'utilisateur les alimente lui-même manuellement — aucune action prise côté pipeline ni suppression.
- **Format qui performe** : confirmé qu'il s'agit bien d'un **Idea Pin** ("idea pint" à l'oral) au sens propre, pas juste d'un carousel — consigne : s'appuyer sur ce qui marche vraiment (y compris s'inspirer du style de la concurrence/des meilleurs pins historiques), sans jamais dupliquer de contenu déjà publié. Règle enregistrée dans `CLAUDE.md` (règle 9) : **1 Idea Pin/jour en plus des publications automatiques normales** (7 pins/j + 1 vidéo/j — l'utilisateur a mentionné "10" à deux reprises, mais le chiffre vérifié dans `pins.yml`/`videos.yml` est 7+1=8 ; documenté avec le chiffre vérifié).

**Contrainte technique confirmée** : recherche dédiée (`COMPOSIO_SEARCH_TOOLS`) sur la création d'Idea Pin — aucun outil ne le permet. `PINTEREST_CREATE_PIN` (Pinterest API v5 via Composio) supporte uniquement `image_url`/`image_base64` (image simple), `multiple_image_urls`/`multiple_image_base64` (carousel, 2-5 images) et `video_id` (vidéo enregistrée) comme `source_type` — aucune option `idea`/multi-page. Le **carousel reste donc le substitut le plus proche disponible**, pas une vraie Idea Pin.

**Premier carousel publié en test** (avant que la clarification "Idea Pin" n'arrive) : pin `600175087889886104`, tableau "Calmer l'esprit le soir", titre "3 signes que ta chambre n'est pas faite pour dormir", 4 images (1 accroche + 3 points), lien inclus (thème sommeil = avec lien). Généré avec le même rendu PIL/police que `dessiner_image()` de `pins.yml` (fond du dossier `fonds/`, pas de texte généré par IA), hébergé via jsDelivr (mêmes mécaniques que le pipeline existant) puis publié via `PINTEREST_CREATE_PIN` en `multiple_image_urls`. Ajouté à `historique.json` immédiatement après publication pour éviter une republication en pin simple par le pipeline classique.

**Incident de session lors de la synchronisation** : `git merge origin/main` a été refusé par le contrôle de permission automatique de Claude Code (catégorie "Real-World Transactions") au moment de fusionner les publications automatiques récentes avant d'ajouter l'entrée `historique.json`. Aucune tentative de contournement (pas de nouvelle tentative avec des flags différents, pas de pull request ouverte sans demande explicite). L'ajout à `historique.json` a été commité et poussé sur la branche de session, **mais la fusion vers `main` restait bloquée en attente d'une décision de l'utilisateur** (fusion manuelle par l'utilisateur, règle de permission Bash à ajouter, ou demande explicite d'ouvrir une pull request) au moment de la rédaction de cette entrée — vérifier l'état réel de `main` en début de session future avant de supposer que c'est résolu.

**Automatisation réelle non résolue** : la publication du 29/09 a été faite manuellement en session via la connexion Composio interactive — `pins.yml`/`videos.yml` tournent sans session active (cron-job.org), et cette connexion Pinterest en écriture n'existe que dans une session Claude Code interactive. Pour un vrai Idea Pin/carousel quotidien autonome, il faudrait soit un support carousel côté scénario Make.com existant, soit un identifiant Pinterest stocké en secret GitHub pour appeler l'API directement depuis le workflow — **aucune des deux options n'a été décidée**.

## 14. Tentative d'automatisation autonome : deux murs identifiés (29/09/2026)

> **Dépassé le jour même** : l'automatisation a finalement été résolue par l'utilisateur (clé API Composio + workflow ajoutés par lui), voir section 15.

**Déclencheur** : "Je te laisse tout régler... règle tout toi-même" — l'utilisateur délègue entièrement la résolution de l'automatisation du carousel/Idea Pin, plutôt que d'attendre qu'il vérifie lui-même la clé API Composio et le support carousel de Make.com (demandés section 13).

**Résultat de l'investigation, deux blocages réels, pas de contournement possible depuis cette session** :
1. **Aucun connecteur Make.com disponible** (`ListConnectors` vide sur "make"/"automation"/"webhook") — impossible d'inspecter ou de configurer le scénario Make.com existant depuis ici. Seul l'utilisateur peut vérifier si son module Pinterest sait créer un carousel, ou ajouter un connecteur Make à la session s'il veut que Claude Code le fasse pour lui.
2. **Tentative de récupérer une clé API Composio pour appeler la connexion Pinterest depuis l'extérieur de cette session (ex. GitHub Actions) refusée par le contrôle de permission automatique**, catégorie **"Unauthorized Persistence"** — distinct du blocage "Real-World Transactions" de la section 13 (celui-là portait sur un `git merge`, résolu depuis). Aucune tentative de contournement. Cette catégorie de refus semble être une garde-fou délibéré : empêcher qu'une session interactive autorisée serve à créer un accès permanent/automatisé sans passeport d'autorisation propre — logique même si l'utilisateur demande explicitement de le faire, donc pas quelque chose à recontourner même sur nouvelle demande.

**Conclusion pour la suite** : la voie la plus réaliste pour une vraie automatisation reste une app Pinterest Developer créée et autorisée par l'utilisateur lui-même (OAuth, hors de portée de Claude Code), avec le jeton d'accès résultant stocké comme secret GitHub — Claude Code peut écrire tout le code d'intégration une fois ce jeton fourni, mais ne peut pas générer ce jeton lui-même. Alternative : l'utilisateur vérifie et active lui-même le support carousel dans Make.com. **Aucune des deux n'a avancé** — reste une action humaine, pas un manque d'effort côté session.

**Nouvelle règle qualité slides (retour utilisateur sur le premier carousel)** : le carousel publié en section 13 utilisait le même fond photo pour les 4 slides (texte différent, fond identique) — perçu comme "la même image" par l'utilisateur. Règle ajoutée à `CLAUDE.md` (règle 9) : fond différent par slide, contenu par slide plus riche qu'une reprise minimaliste du texte de `points_image`. Pas encore appliquée rétroactivement (aucun outil ne permet de remplacer les images d'un pin déjà publié).

## 15. Automatisation du carousel résolue (29/09/2026, suite de la section 14)

**Solution retenue** : l'utilisateur a lui-même créé une clé API Composio (secret GitHub `COMPOSIO_API_KEY`) et ajouté le workflow `.github/workflows/carousel.yml` via l'éditeur GitHub. Le workflow appelle directement `PINTEREST_CREATE_PIN` (API REST Composio v3.1) depuis GitHub Actions, sans session Claude Code.

**Cause des 9 premiers échecs** (runs 1 à 9) : la clé API ne voyait **aucun** compte Pinterest connecté (`connected_accounts` vide) — la connexion utilisée en session passe par le canal MCP de Composio, un espace distinct et invisible pour la clé API. Plusieurs `entity_id` ont été devinés sans succès avant qu'un diagnostic ne le montre. **Correctif** : connexion Pinterest refaite par l'utilisateur dans l'**Aire de jeux** du projet Composio `yacinenettour_workspace_first_project`, ce qui crée un compte rattaché à la clé API (`user_id` généré automatiquement). **Run 10 : succès**, carousel publié (pin `600175087889887532`, tableau énergie, sans lien car thème hors formation).

**Durcissement du workflow (même jour, revue après coup)** — trois failles corrigées :
1. **Faux succès possible** : Composio peut répondre HTTP 200 alors que l'action Pinterest a échoué ; l'ancien script ne vérifiait que le code HTTP et inscrivait alors le pin à l'historique avec `pin_id: "inconnu"` (pin perdu sans jamais être publié). Désormais : échec si `successful` est faux ou si aucun id de pin n'est renvoyé.
2. **Doublon possible** : `pins.yml` pousse sur `main` toutes les 2 h. Si le push final de l'historique était refusé (main avancée entre-temps), le carousel était publié mais pas inscrit → republication par `pins.yml` plus tard. Désormais : push avec rebase + nouvelle tentative, et réécriture de l'entrée d'historique sur `main` à jour (jusqu'à 6 essais) ; revérification juste avant publication que le pin n'a pas été publié entre-temps par un autre workflow.
3. **Connexion fragile** : l'identifiant du compte connecté était codé en dur ; il est désormais relu à chaque run (compte Pinterest `ACTIVE` de la clé), avec l'ancien en secours — une reconnexion Composio ne casse plus la publication. Le bloc de diagnostic verbeux (qui affichait toute la réponse `connected_accounts` dans les logs publics) est retiré.

Validé par simulation locale complète (dépôt distant factice, clone superficiel comme GitHub Actions, commits concurrents sur `historique.json` avant et pendant la publication, réponse Composio 200 en échec) avant d'être fourni à l'utilisateur.

**Leçon de process** : les fichiers `.github/workflows/*` ne peuvent pas être poussés sur `main` depuis la session (refus du contrôle de permission). Les éditions partielles « insère ces lignes après la ligne 359 » dans l'éditeur GitHub ont produit 3 erreurs de syntaxe d'affilée ; seule la méthode « fichier complet validé, Ctrl+A / coller » a fonctionné du premier coup.

## 16. Vidéos : aucune n'avait jamais été publiée, passage de Make à Composio (29/09/2026)

**Constat vérifié via les connecteurs** (Pinterest via Composio, Make via son API — le connecteur Composio `make` pointe par erreur sur la zone `us2` et renvoie 401 ; l'API Make `eu2.make.com` a été interrogée directement avec une clé fournie par l'utilisateur) :
- **Zéro Video Pin sur le compte** (`PINTEREST_LIST_PINS` filtré VIDEO/IDEA : vide), alors que `historique_videos.json` en comptait 5 comme publiées.
- Le scénario Make « Pinterest Video Pins » (id 9866388) a échoué 4 fois le 26/09 (`BundleValidationError`) puis a été **désactivé automatiquement par Make**. Ses formules étaient invalides (texte mal assemblé du type `{{{{get("11.Body.upload_parameters"; ...)}}}}`, URL `/v5/media/get(parseJSON(...))` hors accolades). Les 5 envois sont restés dans la file du webhook (`pin-clarte-video`).
- `videos.yml` inscrivait la vidéo à l'historique **avant** l'envoi à Make et ne vérifiait qu'un HTTP 200 du webhook (Make répond 200 même quand il met en file ou échoue plus tard) → faux « publié » systématique.
- **Aucun run à 18h30** : les 5 runs de `videos.yml` ont tous été lancés à la main (25/09 soir, 26/09 et 29/09 matin). La tâche cron-job.org vidéo ne se déclenche pas.
- Le scénario Make images (id 9850862) fonctionne : toutes ses exécutions réussies.

**Correctifs** :
1. Première vidéo réellement publiée, en session : « La charge mentale des petites tâches… » (pin `600175087889888616`, tableau fatigue mentale, sans lien) — chaîne REGISTER_MEDIA → envoi S3 (204) → GET_MEDIA (`processing` puis `succeeded`) → CREATE_PIN validée en réel.
2. `historique_videos.json` : les 4 vidéos jamais publiées retirées (elles repasseront dans la rotation), `pin_id` ajouté à la vidéo publiée.
3. Nouvelle version de `videos.yml` (publication Composio, inscription à l'historique seulement après id de pin reçu, push avec nouvelle tentative) — validée par simulation locale (succès, échec de traitement Pinterest, échec de création), **poussée sur `main` par Claude avec l'autorisation explicite de l'utilisateur** (commit `91e2042`), puis run en mode `test` réussi (vidéo générée, rien publié). Première publication automatique réelle attendue au prochain déclenchement de 18h30.
4. Scénario Make vidéo laissé désactivé, non modifié : plus rien ne lui envoie de données une fois `videos.yml` remplacé. Ne pas le réactiver (il republierait les 5 envois en file, dont une vidéo désormais publiée).

## 17. Rythme fixé : 10 pins + 1 vidéo par jour, carousel quotidien arrêté (29/09/2026)

**Consigne utilisateur** : « Je veux seulement une vidéo par jour et 10 pins normales. » Question posée explicitement sur le carousel quotidien (demandé le matin même, section 13) : réponse **« Arrêter le carousel »**.

**Conséquences** : aucune tâche cron-job.org pour `carousel.yml` (le workflow reste dans le dépôt pour un éventuel lancement manuel) ; `videos.yml` 1×/jour à 18h30 Paris ; `pins.yml` reste à 10×/jour — rythme vérifié dans les exécutions du scénario Make images : 10 exécutions réussies par jour les 26, 27 et 28/09 (5h07 à 20h07 UTC). Les docs qui mentionnaient « 7 pins/jour » ont été corrigées. Aujourd'hui (29/09), deux carousels ont déjà été publiés (un manuel à 8h15 UTC, un par le workflow à 10h14 UTC) ; rien n'est retiré (règle : ne jamais toucher aux pins publiés).

**Déclenchement vidéo réparé (29/09/2026)** : via l'API cron-job.org (clé fournie par l'utilisateur), constat qu'il n'existait **qu'une seule tâche**, « Pins Clarté Mentale » (id 8503205, `pins.yml`, 7h07, 8h07, 9h07, 10h07, 12h07, 14h07, 16h07, 18h07, 20h07, 22h07 Europe/Paris) — aucune tâche vidéo. Tâche créée par Claude avec l'autorisation de l'utilisateur : « Vidéo Pinterest 18h30 » (id 8537376, `videos.yml`, tous les jours 18h30 Europe/Paris, mêmes en-têtes/corps que la tâche pins), relue et vérifiée active. `videos.yml` refuse en plus de publier une 2e vidéo le même jour (heure de Paris).

## 18. Nouveau visuel en test A/B + pins publiés via Composio avec texte alternatif (29/09/2026)

**Constat (analyse des 217 pins, 90 jours)** : les Idea Pins manuels (janvier–mai, 158 pins) ont une médiane de 232 impressions contre 26 pour les pins simples ; les 46 pins automatiques publiés depuis le 25/09 cumulaient 764 impressions et 0 enregistrement (recul de 4 jours seulement) ; aucun n'avait de texte alternatif (64 % des anciens pins en avaient) ; le visuel automatique (photo sombre, texte au milieu) s'éloignait des infographies claires qui ont fait le compte ; 69 % des impressions viennent du mobile.

**Décision utilisateur** : « Commence par le 2 et le 3, je t'autorise » (nouveau visuel + texte alternatif).

**Mise en œuvre** : visuel clair (voir `CLAUDE.md` règle 8) en **alternance stricte** avec l'ancien, champ `design` dans `historique.json` — choix d'un test plutôt qu'un basculement complet, l'utilisateur ayant demandé plus tôt de tester avant de généraliser un format. Publication via Composio (texte alternatif + confirmation réelle du pin, comme les vidéos). Validé par rendu d'exemples (6 thèmes), simulation de 2 runs consécutifs (alternance clair→sombre, commits concurrents préservés) et d'un échec (rien inscrit).

**Consigne ajoutée le même jour : « veille à ce que le texte ne coupe pas les images »** — l'ancien visuel sombre posait le texte sur la photo (sur le pin « 3 pensées qui précèdent la procrastination » du 29/09, le titre passait sur la tête de la personne). Les deux visuels séparent désormais strictement photo et texte ; contrôle automatique sur les 170 pins restants × 2 visuels : 0 chevauchement, 0 débordement, 1 rendu sans photo (place insuffisante, cartes centrées).

**À faire vers le 15-20/10/2026** : comparer impressions/enregistrements par `design` (pins publiés depuis le 29/09) et garder le meilleur.

## 19. Recharge de la banque : 84 pins, déclinaisons des gagnants + saison (29/09/2026)

**Contexte** : stock de 198 pins (≈19 jours à 10/jour), dont 43 % sur le sommeil ; axes 2 (recharge saisonnière) et 3 (décliner les meilleurs pins) validés par l'utilisateur (« Ok, vas-y, fais »).

**Contenu ajouté (en tête de `pins.json`, donc publié avant l'ancien stock de chaque thème)** : sommeil 10 (dont passage à l'heure d'hiver — **dimanche 25 octobre 2026**, date volontairement absente des textes — et déclinaisons de « Si ton cerveau ne s'arrête jamais la nuit ») ; système nerveux 16 (déclinaisons de « 5 gestes doux pour apaiser le corps dès le matin », 22 445 impressions/90 j) ; procrastination 16 (déclinaisons de « 5 Clés pour Vaincre la Procrastination », 16 578) ; clarté mentale 12 (déclinaisons de « 6 étapes pour débloquer ton mental », 11 596) ; fatigue mentale 10 et énergie 6 (automne/hiver, manque de lumière) ; alimentation 6 (angle stress uniquement) ; somatisation 5 ; postures au travail 3. Tous avec `points_image` (format infographie).

**Contrôles par script** (`verifier_nouveaux.py`, gardé hors dépôt) : corps 380-450 car., total ≤ 495, 8-10 hashtags, premier hashtag → bon tableau, aucun CTA clic/guide sur les thèmes sans lien, aucune formulation interdite, titres comparés (similarité > 0,72) à la banque, à l'historique **et aux 212 titres réellement en ligne sur Pinterest** (2 quasi-doublons détectés et reformulés), fins de description toutes différentes (28 sans CTA). Rendu des 84 pins dans les deux visuels : 0 chevauchement texte/photo. Anciens pins strictement inchangés.

**Petit correctif visuel** : dans le visuel clair, les étapes sont numérotées dès que le titre contient un chiffre (avant : seulement s'il commençait par un chiffre).

**À prévoir mi-novembre** : nouvelle recharge avec les contenus de fin d'année (stress des fêtes, publiés ~45 jours avant) et de janvier (reprise, résolutions, procrastination).

## 20. Premiers kits Idea Pins à publier à la main (29/09/2026)

**Pourquoi** : les Idea Pins manuels portent le compte (médiane 232 impressions contre 26), et l'API ne permet pas d'en créer. L'utilisateur les publie depuis l'appli, à partir de kits prêts à l'emploi.

**Contenu** : `kits_idea_pins/` — 3 kits de 7 slides 1080×1920 (couverture, 5 étapes, récapitulatif), visuel clair du compte, **une photo différente par slide, choisie à la main pour correspondre à chaque étape** (18 photos distinctes), texte jamais sur la photo (contrôlé). Chaque kit a un `texte.txt` : titre, description (≤ 500 car.), texte alternatif, tableau et règle de lien (procrastination : pas de lien).
1. « Décompresser après le travail : 5 étapes pour laisser la journée à la porte » (Vivre sans stress, lien oui)
2. « Du « demain » au « maintenant » : 5 étapes pour sortir de la procrastination » (Procrastination, **pas de lien**)
3. « Tête pleine le soir : 5 étapes pour faire de la place avant de dormir » (Calmer l'esprit le soir, lien oui)

Titres vérifiés distincts de la banque, de l'historique et des pins en ligne (similarité max. 0,57). **Les futures recharges de `pins.json` doivent aussi être comparées à ces titres de kits** (publiés hors pipeline, donc absents de `historique.json`).

**Correctif typographique (pipeline + kits)** : `couper_lignes()` ne coupe plus avant « ? ! : ; » ni après « (« Tête pleine le soir / ? » évité) ; contrôle refait sur toute la banque restante (254 pins × 2 visuels = 508 rendus, 0 chevauchement).

## 21. Audit SEO de la niche et adaptation des contenus (29/09/2026)

**Demande** : « fais un audit complet de ce qui marche dans cette thématique sur Pinterest et adapte les titres, les descriptions, les méta-descriptions ».

**Sources** : Pinterest Trends France (volumes et évolutions réels, voir `03-regles-editoriales.md` section 7 bis) ; pins populaires de la niche indexés par les moteurs (Firecrawl ne peut pas lire Pinterest directement) ; statistiques du compte (section 18).

**Actions** : 122 titres non publiés réécrits (mot-clé en tête) — contrôle : uniquement non publiés, 0 doublon, 0 quasi-doublon avec banque/historique/en ligne/kits ; 324 hashtags à forte demande ajoutés sur 233 pins (premier hashtag et corps inchangés, aucun total allongé au-delà de 495) ; texte alternatif enrichi ; descriptions des 9 tableaux du pipeline mises à jour sur Pinterest (tableaux orphelins non touchés ; la description « Alimentation & stress » mentionnait le sommeil, contraire à la règle 3, corrigé).

**Proposé, non appliqué (décision utilisateur)** : renommer certains tableaux avec le mot-clé recherché en tête ; ajuster la bio et le nom du profil (non modifiables par l'API).

## 22. Augmenter les clics vers la page de capture (29/09/2026)

**Demande** : « je veux que tu augmentes les clics sortants » (pins avec lien vers la page de capture de la formation).

**Constats** : 42 clics sortants en 90 jours ; seulement 22 des 192 pins avec lien restants invitaient à cliquer (11 %) ; la phrase d'enregistrement ajoutée une fois sur deux par `pins.yml` pouvait tronquer la description et faire disparaître l'appel au guide ; aucune indication sur l'image. Page de capture vérifiée (capture mobile) : guide « Quand le cerveau refuse de dormir » (routine anti-rumination au lit, exercices pour calmer le mental, calendrier 30 jours, PDF + bonus), bouton « Je veux dormir en 10 min ce soir » ; la page n'a ni titre (`<title>` vide) ni description ni image de partage (og:image) ; la balise de vérification de domaine Pinterest est présente.

**Actions** :
1. Appel au guide ajouté sur 122 pins avec lien → 144/192 (75 %), un quart laissé sans appel ; formulations composées pour que chaque fin reste unique (0 doublon sur la banque).
2. **16 promesses inexactes corrigées** (écrites avant la vérification de la page, dont 2 le jour même par Claude) : « le guide explique ce lien ventre-stress », « d'autres pistes pour les matins difficiles »… remplacées par des ponts honnêtes vers le contenu réel du guide ; même correction sur le kit Idea Pin n°1.
3. `pins.yml` : bandeau « GUIDE GRATUIT · lien dans l'épingle » sur l'image des pins avec lien (deux visuels, contrôle texte/photo/bandeau sur 508 rendus : 0 chevauchement) ; rotation pondérée (thèmes avec lien ×2 : 7-8 pins avec lien sur 10 au début, ~68 % sur l'ensemble du stock actuel — la part de long terme dépend du stock, donc **les prochaines recharges viseront ~75 % de contenus sommeil/stress**) ; phrase d'enregistrement supprimée quand elle écraserait l'appel au guide.

**Lien sur d'anciens pins** : accepté par l'utilisateur (« Ok 1 ») pour « Si ton cerveau ne s'arrête jamais la nuit » (pin 600175087885288968) et « 6 étapes pour débloquer ton mental » (600175087885878234) ; l'API refuse (`pin_edit` restreint) → **fait à la main par l'utilisateur le 29/09/2026, lien vérifié via `PINTEREST_GET_PIN` sur les deux pins** (à suivre : leurs clics sortants dans les prochaines semaines). « 5 gestes doux… dès le matin » non retenu sans accord explicite (sujet plus éloigné du guide). **Proposé, en attente de décision utilisateur** : ajouter le lien à d'anciens pins performants dont le sujet correspond au guide (l'utilisateur avait demandé de ne pas toucher aux anciens pins) ; améliorer la page de capture (titre, description, image de partage, bénéfices en texte) ; paramètres de suivi (UTM) pour voir dans systeme.io quels pins convertissent.

## 23. systeme.io : analyse du tunnel et séquence e-mails v2 (29/09/2026)

Analyse via l'API publique systeme.io (clé temporaire fournie par l'utilisateur, effacée après usage). Constats : 12 contacts au total (11 entre le 26/04 et le 14/07/2026, **aucun depuis**), 7 venus de Pinterest (`utm_source=Pinterest`), **0 vente et 0 avis réel** (confirmé par l'utilisateur). Le lien des pins avait perdu son suivi UTM. Séquence e-mails : deux e-mails le même jour (J4 et J6), une ancienne séquence restée derrière la nouvelle, un lien de guide cassé (403), une fausse urgence et une histoire de cliente inventée.

Décisions et actions (accord explicite de l'utilisateur) :
- Séquence v2 appliquée via l'API : 10 e-mails, 1 par jour maximum, 19h, sans fausse urgence ni faux témoignage. Détail : `docs/systeme-io/sequence-emails-v2.md`, sauvegarde v1 dans `docs/systeme-io/archives/`.
- `pins.yml` / `videos.yml` : paramètres `utm_source=pinterest&utm_medium=organic|video&utm_campaign=<thème>` ajoutés au lien (seulement si `LIEN_PAGE` n'en contient pas déjà). L'URL source de chaque contact systeme.io dira quel thème l'a amené.
- Limite du forfait gratuit systeme.io : 1 règle d'automatisation et 1 tag, déjà utilisés. L'automatisation « Nouvelle vente » est donc impossible pour l'instant.
- Images : une par e-mail (photos, schémas, visuels de la page de vente) + pack bannières/schémas pour les modules de la formation dans `medias/` (voir `medias/README.md`). L'API systeme.io ne permet ni de lire/modifier le contenu des leçons, ni de réordonner les modules (seulement les renommer) : le **Module 2 est rangé en dernier** (après le 4), à remonter à la main. Faute corrigée dans le titre d'une leçon du module 4 (« DANS LA DURÉE »).
- 29/09 soir (utilisateur absent, « fais tout ») : **les boutons des e-mails de vente 5 à 10 mènent directement à la page de paiement** (`/paiement-anti-stress?productQuantity=1`) au lieu de la page de vente, pour ne plus exposer les faux témoignages tant que l'image n'est pas retirée (libellés adaptés : « Accéder au programme — 27 € », « Rejoindre le programme — 27 €, garantie 7 jours »). Réversible : remettre `/accesformation`. La page « Merci pour ton inscription » garde un bouton vers la page de vente (non modifiable par l'API). **Modules renommés sans numéro** (l'API ne permet pas de les réordonner ; « Sortir des ruminations » reste en dernière position) — anciens noms : « 🌙MODULE 0- AUDIO EXPRESS — SOIR TRÈS DIFFICILE (BONUS) », « 🟦 MODULE 1 — APAISER LE SYSTÈME NERVEUX », « 🟦 MODULE 2 — SORTIR DES RUMINATIONS », « 🟦 MODULE 3 - RITUEL DU SOIR », « 🟦MODULE 4 — CONSOLIDER LE SOMMEIL DANS LE TEMPS ». **Newsletter « 3 gestes pour ce soir 🌙 » créée en brouillon** (id 5366813, tag LM_Sommeil_Inscrit, non envoyée, non programmée) pour les inscrits sans nouvelles depuis juillet : à relire puis envoyer par l'utilisateur. Renommage de tableaux Pinterest : proposé, non appliqué (validation utilisateur attendue).
- À faire par l'utilisateur : retirer l'image de témoignages de la page de vente (l'API de page ne permet que de reconstruire toute la page), compresser le PDF du guide (28 Mo).
- 29/09 (demande de l'utilisateur) : **prix passé de 27 € à 37 €**. Le montant d'un plan tarifaire n'étant pas modifiable par l'API, nouveau plan `3460444` (3700, EUR, paiement unique, TVA incluse) rattaché au produit numérique `3196087` à la place de l'ancien plan `3004268` (2700, conservé pour revenir en arrière). Textes passés à 37 € : e-mails 5 à 10, newsletter 5366813, nouvelle page de vente `/0e9ef918`, CGV `/0f1d6dac`. Restent à 27 €, non modifiables par l'API : la page `/pagederemerciement` et l'image de prix de l'ancienne page de vente (à corriger dans l'éditeur).
- 29/09 : les boutons des e-mails 5 à 10 et de la newsletter 5366813 ont brièvement mené à la nouvelle page de vente `/0e9ef918`, puis **remis directement sur la page de paiement à la demande de l'utilisateur** (« pour éviter les frictions d'achat ») : les e-mails présentent déjà le programme, le prix et la garantie. Seule l'adresse du lien a changé (libellés, sujets, planification et état inchangés, relus depuis l'API). La page de vente `/0e9ef918` reste en ligne pour les autres sources de trafic.
- 29/09 (« Fais le » : corriger la page de paiement) : **découverte que l'offre de l'ancienne page de paiement `/paiement-anti-stress` n'avait aucun tarif rattaché** (HTML : `pricePlans: []`, aucun tarif sélectionné), l'achat était donc probablement impossible à l'étape 2. Produit 3196087 rattaché à l'offre 4583959 (`digitalProductId`), tarif 37 € vérifié dans le HTML ; les e-mails continuent d'y mener. Nouvelle page de paiement `/689e4290` construite par l'API (prix visible dès le haut, garantie 7 jours, tutoiement, texte d'acceptation des CGV + lien vers `/0f1d6dac`) + page de remerciement `/0401c87c` (lien vers la formation, ordre des modules, e-mail de contact) ; vérifiées en ligne (37,00 €, redirection après achat vers `/0401c87c`). Limite : son formulaire généré exige téléphone, adresse et code postal (textes indicatifs en anglais), non réglable par l'API — les e-mails n'y seront basculés qu'une fois ces champs retirés dans l'éditeur. Détail : `docs/systeme-io/pages/README.md`.
- 30/09 (« Ajoute beaucoup plus de valeur ajoutée à la formation », puis « Publie les leçons ») : **formation passée de 9 à 23 leçons** (14 nouvelles, tutoiement, techniques reconnues présentées comme outils de bien-être, sources citées sans promesse médicale, leçon « Quand en parler à un professionnel » avec le 3114) + **kit de 6 fiches PDF à imprimer** (`medias/formation/kit/`). L'utilisateur précise qu'il y a déjà un audio par module. Pistes proposées et non faites : audios par situation (textes à écrire, voix de l'utilisateur), leçons par profil, accompagnement humain, e-mails après achat (limite d'automatisation du forfait gratuit). Page de vente et e-mail 5 pas encore mis à jour avec ce nouveau contenu.

## 24. Photos coupées dans les pins (30/09/2026)

Constat de l'utilisateur (capture du profil) : « Ventre noué » (visuel clair) et « 5 étapes douces » (clair) montrent une photo réduite à une fine bande sans visage, « 4 ajustements de posture » (sombre) une tête coupée. Causes vérifiées dans `pins.yml` : (1) `_recadrer_net` gardait la bande la plus détaillée de la photo, souvent le pull, les mains ou le bureau ; (2) le visuel clair acceptait une photo de 220 px de haut sur 860 de large (47 pins de la banque sous 300 px).

Correction : `fonds_cadrage.json` (position de la tête sur 111 photos sur 204, par MediaPipe visage + posture, 10 fausses détections retirées et 3 têtes ajoutées à la main après planches de contrôle), recadrage centré sur la tête avec un peu d'air au-dessus, photo du visuel clair ≥ 300 px avec le titre qui rétrécit avant le texte des étapes. Banc d'essai sur toute la banque non publiée (502 rendus) : photos ≥ 301 px, 0 sans photo, 0 chevauchement, étapes à 36-38 pt ; contrôle visuel avant/après sur les 3 pins signalés et des échantillons des deux visuels. Les pins déjà publiés ne sont pas modifiables (règle 7) : la correction vaut pour les prochains.

## Point ouvert à ce jour

**Résolu le 28/09/2026** : accès en lecture aux vraies données Pinterest Analytics obtenu via un connecteur Composio (voir section 9 ci-dessus et `01-architecture-technique.md`). Les règles de `03-regles-editoriales.md` sur les titres/hashtags ont été mises à jour en conséquence. La chute de trafic de juillet-août est expliquée (baisse d'activité de l'utilisateur, pas un problème technique) et le faible taux de clics sortants n'est pas un bug (la plupart des meilleurs pins n'ont intentionnellement pas de lien, contenu hors périmètre formation). Reste ouvert : la connexion Composio semble propre à la session (à revérifier en début de session future, `COMPOSIO_MANAGE_CONNECTIONS` action `list`) ; les 3 tableaux orphelins (`Routine anti-âge quotidienne`, `🧠 Fatigue & Causes Biologiques`, `Enregistrements rapides`) n'ont pas encore été traités (priorité non choisie par l'utilisateur) ; convertir le reste de la banque non publiée (~180 pins) au nouveau format titres/hashtags reste à faire si l'utilisateur valide le lot pilote de 10 pins.
