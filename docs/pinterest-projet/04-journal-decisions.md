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

**Déclencheur** : "Je te laisse tout régler... règle tout toi-même" — l'utilisateur délègue entièrement la résolution de l'automatisation du carousel/Idea Pin, plutôt que d'attendre qu'il vérifie lui-même la clé API Composio et le support carousel de Make.com (demandés section 13).

**Résultat de l'investigation, deux blocages réels, pas de contournement possible depuis cette session** :
1. **Aucun connecteur Make.com disponible** (`ListConnectors` vide sur "make"/"automation"/"webhook") — impossible d'inspecter ou de configurer le scénario Make.com existant depuis ici. Seul l'utilisateur peut vérifier si son module Pinterest sait créer un carousel, ou ajouter un connecteur Make à la session s'il veut que Claude Code le fasse pour lui.
2. **Tentative de récupérer une clé API Composio pour appeler la connexion Pinterest depuis l'extérieur de cette session (ex. GitHub Actions) refusée par le contrôle de permission automatique**, catégorie **"Unauthorized Persistence"** — distinct du blocage "Real-World Transactions" de la section 13 (celui-là portait sur un `git merge`, résolu depuis). Aucune tentative de contournement. Cette catégorie de refus semble être une garde-fou délibéré : empêcher qu'une session interactive autorisée serve à créer un accès permanent/automatisé sans passeport d'autorisation propre — logique même si l'utilisateur demande explicitement de le faire, donc pas quelque chose à recontourner même sur nouvelle demande.

**Conclusion pour la suite** : la voie la plus réaliste pour une vraie automatisation reste une app Pinterest Developer créée et autorisée par l'utilisateur lui-même (OAuth, hors de portée de Claude Code), avec le jeton d'accès résultant stocké comme secret GitHub — Claude Code peut écrire tout le code d'intégration une fois ce jeton fourni, mais ne peut pas générer ce jeton lui-même. Alternative : l'utilisateur vérifie et active lui-même le support carousel dans Make.com. **Aucune des deux n'a avancé** — reste une action humaine, pas un manque d'effort côté session.

**Nouvelle règle qualité slides (retour utilisateur sur le premier carousel)** : le carousel publié en section 13 utilisait le même fond photo pour les 4 slides (texte différent, fond identique) — perçu comme "la même image" par l'utilisateur. Règle ajoutée à `CLAUDE.md` (règle 9) : fond différent par slide, contenu par slide plus riche qu'une reprise minimaliste du texte de `points_image`. Pas encore appliquée rétroactivement (aucun outil ne permet de remplacer les images d'un pin déjà publié).

## Point ouvert à ce jour

**Résolu le 28/09/2026** : accès en lecture aux vraies données Pinterest Analytics obtenu via un connecteur Composio (voir section 9 ci-dessus et `01-architecture-technique.md`). Les règles de `03-regles-editoriales.md` sur les titres/hashtags ont été mises à jour en conséquence. La chute de trafic de juillet-août est expliquée (baisse d'activité de l'utilisateur, pas un problème technique) et le faible taux de clics sortants n'est pas un bug (la plupart des meilleurs pins n'ont intentionnellement pas de lien, contenu hors périmètre formation). Reste ouvert : la connexion Composio semble propre à la session (à revérifier en début de session future, `COMPOSIO_MANAGE_CONNECTIONS` action `list`) ; les 3 tableaux orphelins (`Routine anti-âge quotidienne`, `🧠 Fatigue & Causes Biologiques`, `Enregistrements rapides`) n'ont pas encore été traités (priorité non choisie par l'utilisateur) ; convertir le reste de la banque non publiée (~180 pins) au nouveau format titres/hashtags reste à faire si l'utilisateur valide le lot pilote de 10 pins.
