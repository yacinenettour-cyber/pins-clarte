# Robot vidéo YouTube (chaîne @ClarteMentaleFR)

Mis en place le 20/10/2026 à la demande de l'utilisateur (« je veux tout automatiser », puis « Oui, automatise »).

1. **Chaque semaine, la tâche Claude « Vidéo YouTube »** écrit `videos_youtube/<slug>/plan.json` (statut `a_fabriquer`) :
   un sujet tiré d'un article du site, une courte partie « Comprendre » qui reprend les sources vérifiées de l'article,
   puis la pratique guidée ; photos Unsplash (URL directes), titre, description, tags, miniature, Short.
2. **`.github/workflows/youtube.yml`** (à chaque nouveau plan, et toutes les heures) :
   `youtube/fabriquer.py` → photos, voix Kokoro « B » + musique + bols (`audio.py`), contrôle de la voix par
   transcription (Whisper small, score ≥ 0,85), images animées (`rendu.py`, morceaux parallèles), Short, miniature,
   sous-titres, contrôles (durée, images non noires, mots interdits, mentions obligatoires). Si un contrôle échoue :
   statut `erreur_fabrication`, rien n'est publié, détail dans `rapport.json`.
3. **Mise en ligne** (`publier.py`, API Composio, même clé que Pinterest) : vidéo et Short en « non répertorié »,
   miniature (adresse jsDelivr du dépôt), sous-titres ; puis passage en public à `publication_prevue`, sauf si le
   plan contient `"bloquee": true` (phase de rodage proposée à l'utilisateur). Sans compte YouTube connecté dans
   Composio : statut `attente_connexion_youtube` (remettre `a_fabriquer` une fois la connexion faite).

**Voix (26/10/2026)** : champ `voix` du plan, réglages dans `REGLAGES_VOIX` (`audio.py`). Sans ce champ : Kokoro « B » (1re vidéo). L'utilisateur trouve Kokoro peu naturel ; après écoute d'extraits (`essais_voix/`, workflow `essai-voix.yml`), il a choisi `chatterbox_posee` : Chatterbox Multilingual (Resemble AI, licence MIT, gratuit), expressivité 0,35, rythme 0,3, température 0,7. Le crédit de la description suit la voix utilisée. **26/10, 2e choix** : l'utilisateur entend un ton anglais aux deux vidéos (Kokoro et Chatterbox voix par défaut) ; après un 2e essai (`essais_voix/G-H-I`), il choisit **H** = réglage `chatterbox_francais` : Chatterbox imite une voix de référence française (`youtube/voix/reference-francaise.wav`, faite avec la voix ff_siwis de Kokoro, corpus SIWIS CC BY 4.0, crédité dans la description), rythme 0 (contre l'accent de la référence), expressivité 0,35, température 0,7.

**Voix ElevenLabs « Mila » et 2 vidéos par mois (27/10/2026, choix de l'utilisateur)** : « Change la voix de Chatterbox et remplace-la par celle d'Eleven Labs, une voix féminine, douce » ; plan gratuit sans carte (10 000 caractères par mois, soit 2 vidéos), réglage `elevenlabs_mila`. Le robot GitHub n'a pas accès à ElevenLabs : les phrases sont générées pendant une session Claude (connecteur ElevenLabs, voix `hndZlkpVm5i9lXBY9CKj`, modèle `eleven_multilingual_v2`, une seule prise par phrase, jamais de nouvel appel pour « réessayer »), puis `python3 youtube/voix_elevenlabs.py ranger <slug> <texte> <url>` les télécharge, les réécoute (Whisper) et les range dans `videos_youtube/<slug>/voix_elevenlabs/` (nom tiré du texte) ; `manquantes <slug>` liste ce qui reste. Une phrase où Whisper entend autre chose est réécoutée avec la transcription ElevenLabs (Scribe), plus fiable : le 27/10, « Tends maintenant tes bras » était entendu « En maintenant » par les deux, la phrase a été reformulée (« Maintenant, tends tes bras… ») ; « Serre tes cuisses » et « Sens ta nuque » étaient justes (erreur de Whisper). Une phrase absente arrête la fabrication. Crédit dans la description : « voix de synthèse ElevenLabs (elevenlabs.io), voix « Mila » » (attribution demandée par le plan gratuit). **Plan gratuit = usage non commercial** : pas de monétisation de la chaîne avec ces voix sans passer à une offre payante (que l'utilisateur ne veut pas).

**30/10/2026 : abonnement ElevenLabs Starter pris par l'utilisateur** (« C'est bon, j'ai pris l'offre starter d'Eleven Labs », 1 $ le premier mois puis 6 $ par mois, après ma recommandation qu'il avait demandée) : 30 000 crédits par mois et usage commercial autorisé (monétisation possible plus tard). Rythme passé à **1 vidéo par semaine** (tâche « Vidéo YouTube », le dimanche à 10 h 06, heure de Paris), script de 2 000 à 5 000 caractères. Le crédit « voix de synthèse ElevenLabs » reste dans les descriptions (transparence sur la voix de synthèse).

**Format des vidéos (27/10/2026, demande de l'utilisateur : « fais mieux que la première vidéo », 35 vues)** — analyse des résultats YouTube France (« relaxation jacobson pour dormir », « méditation pour dormir », « méditation guidée sommeil ») : les vidéos qui dominent durent 45 min à 3 h (le spectateur s'endort et laisse tourner) et commencent la pratique tout de suite. Donc : **1 heure** (`duree_totale_min: 60` ; voix ~10-12 min puis musique), **pas de partie « Comprendre »** (au plus 2-3 phrases courtes sur la méthode juste après les consignes de sécurité ; études et sources dans la description et l'article), titre avec le mot-clé en tête, un bénéfice concret et la durée (« … (1 h) »), miniature 3 lignes courtes. Le mélange audio est fait par morceaux (`audio.py`) : 4 Go de mémoire au plus pour 1 h (plus de 14 Go avant).

**3 Shorts par vidéo (27/10/2026, accord de l'utilisateur)** : le Short de la respiration guidée, plus un Short par entrée de `shorts_extra` dans le plan (`partie` = titre d'une partie de la pratique, `haut1`, `haut2`, `bas1`, `titre`, `description`) : extrait de 60 s au plus, coupé après une phrase entière, photo de cette partie (`extras.shorts_extra`). Fichiers `travail/<slug>~short2/short.mp4`, `~short3` : même motif que le Short principal, donc dans l'artefact du run sans changer le workflow.

**Envoi manuel (26/10/2026)** : avec `"envoi_manuel": true` dans le plan, la vidéo est fabriquée et contrôlée mais rien n'est envoyé (l'envoi par Composio échoue, voir le journal du 22/10) : statut `fabriquee`, vidéo et Short dans l'artefact du run (onglet Actions, 7 jours), miniature et sous-titres dans le dossier du plan ; l'utilisateur met en ligne à la main.

**Voix Chatterbox réécoutée phrase par phrase (27/10/2026)** : l'utilisateur a entendu des sons « qui ne veulent rien dire » et absents des sous-titres. Chaque phrase est transcrite par Whisper dès sa création ; elle est régénérée (graine suivante, 6 essais au plus) si le texte entendu s'écarte du texte (similarité < 0,85), contient des mots en trop (longueur > 115 %) ou si elle est anormalement lente (< 11 caractères/s). Une phrase encore fausse après 6 essais arrête la fabrication (`voix_douteuses` dans `rapport.json`) ; une phrase seulement lente est gardée. Le contrôle final compte aussi les mots en trop. Cloche de départ ramenée de 0,35 à 0,12 avec une montée de 2 s (« trop forte »).

Statuts : `a_fabriquer` → `fabriquee` → `en_ligne_non_repertoriee` → `publiee` (ou `erreur_fabrication`,
`attente_connexion_youtube`, `attente_quota_youtube`). **Quota YouTube** (constaté le 20/10/2026 : erreur 429 « Video
Uploads per day », quota du projet Google partagé de Composio) : statut `attente_quota_youtube` et `reessai_apres` =
prochain 08:30 UTC (après la remise à zéro, minuit heure du Pacifique) ; à cette heure, `rendre_publiques` remet
`a_fabriquer` et le passage horaire suivant refabrique puis envoie la vidéo. La vidéo et le Short restent 7 jours dans l'onglet Actions (artefact `videos-youtube`).

Règles de contenu (contrôlées par `fabriquer.py`) : aucune promesse de soin, rappel « jamais en conduisant » dans la
voix, « Je ne suis pas professionnel de santé » et lien du site dans la description, études citées seulement si elles
sont dans un article du site (déjà vérifiées). Un nom propre lu en anglais par la voix bloque la fabrication :
reformuler la phrase. Tout est gratuit (voix Kokoro, Whisper, photos Unsplash, musique CC BY, GitHub Actions).

**Description orientée trafic (20/10/2026, `metadonnees.py`)** : si `youtube.accroche` est rempli, la description
commence par cette phrase (mot-clé recherché en tête), puis, dans la partie visible sans « Plus », les liens :
article du site (`article` du plan, libellé `youtube.libelle_article`), guide sommeil si `youtube.guide` = `"sommeil"`
(seule offre, texte = contenu réel du guide, lien avec `utm_source=youtube`), audios de respiration ; puis le texte,
les chapitres, le rappel santé, l'invitation à s'abonner, les sources et les crédits. Les 3 premiers hashtags
s'affichent au-dessus du titre. Titre, description et mots-clés du plan sont **réappliqués juste avant le passage en
public** (`publier.py actualiser`, appelé par `rendre_publiques`) : on peut donc retoucher le plan après la mise en
ligne sans refabriquer la vidéo.

**Chiffres relevés le 29/10/2026 à 8 h 20 (API YouTube)** : chaîne 2 abonnés. Vidéos longues : « Ruminations le soir ?
30 min… » (SCUS59y5kNs, publique depuis le 24/10) 37 vues, 2 j'aime ; « Relaxation guidée pour dormir : … Jacobson
(1 h) » (PbuSSZlDu1c, déjà publique) 2 vues. Shorts du 28/10 : « Détends ton visage… » 202 vues, 6 j'aime ;
« Respire avec moi… » 133 vues, 6 j'aime ; « Relâche tes bras… » 45 vues, 2 j'aime. 0 commentaire. Les Shorts n'ont
aucune description (pas de lien vers la vidéo complète) ; aucune des deux vidéos longues n'a de sous-titres envoyés.

**Mis à jour le 29/10/2026 vers 9 h (accord de l'utilisateur « Oui fais A, B et C »), vérifié par l'API** :
- les 3 Shorts ont une description (une phrase propre à chaque Short, lien vers la relaxation complète
  PbuSSZlDu1c, lien vers l'article `/relaxation-jacobson/`, rappel « jamais en conduisant », crédits voix et
  musique) ; titres inchangés ; langue de la vidéo et de l'audio remise sur `fr` (la mise à jour l'avait passée en
  `en-US`, corrigé : toujours envoyer `defaultLanguage` et `defaultAudioLanguage` dans un `videos.update`) ;
- sous-titres français envoyés (piste « Français », statut `serving`) sur PbuSSZlDu1c et SCUS59y5kNs ;
- description « À propos » de la chaîne : **l'API YouTube répond OK mais ne l'enregistre pas** (essayé par
  `brandingSettings` puis `localizations`, relu après chaque envoi). À coller à la main dans YouTube Studio
  (texte dans `docs/referencement/kit-profils.md`, section 1). À faire aussi à la main : « Vidéo similaire »
  sur chaque Short (Studio → le Short → Vidéo similaire → la relaxation complète).

## Décision du 31/10/2026 : pas d'avatar HeyGen

L'utilisateur a décidé de ne pas utiliser son avatar HeyGen pour la chaîne (« je vais pas utiliser mon avatar pour cette chaîne YouTube »). Raisons : un avatar se repère vite (bouche, mains, regard), ce qui contredit la règle « rien ne doit faire IA » sur un sujet où la confiance compte ; le format méditation s'écoute les yeux fermés ; YouTube demande de signaler un visage réaliste généré ; pas de crédit HeyGen (rien à payer). Ne pas proposer d'avatar (HeyGen ou autre) pour cette chaîne. Pistes possibles si un visage est un jour voulu : l'utilisateur filmé au téléphone, ou des images réelles sans visage.

## Concurrence (01/11/2026) : règles pour les prochaines vidéos

Analyse complète : `docs/referencement/concurrence-youtube.md` (65 vidéos, 23 chaînes françaises en tête sur nos mots-clés). À appliquer par la tâche vidéo hebdomadaire :
- Titre : mot-clé recherché en tête (« Méditation du soir », « Méditation guidée pour dormir »), bénéfice concret sans promesse, durée entre parenthèses ; jamais « soigner », « somnifère », « puissante », « en moins de X minutes », « loi de l'attraction ».
- À partir de la vidéo du 8 novembre : série numérotée « Méditation du soir n° 1, 2, 3… » pour les vidéos d'endormissement (les plus grosses vidéos de Cédric Michel sont numérotées).
- Sujet prioritaire : pensées du soir et ruminations (occupé surtout par l'hypnose ; relié au guide gratuit).
- ~~Alterner 10 minutes et 30 à 60 minutes.~~ Remplacé le 01/11 par le format long ci-dessous.
- Shorts : description avec, en 2e ligne, le lien du guide gratuit quand le sujet est le sommeil ou les ruminations (fait le 01/11 pour les 3 Shorts ruminations).

**Ajout du 03/11/2026 (accord « Oui ajoute-les aux prochains Shorts ») : question et abonnement dans chaque Short.**
Constat (Analytics au 31/10) : 0 commentaire, 8 abonnés pour 2 737 vues de Shorts (0,3 %). À écrire dans `plan.json` pour chacun des 5 Shorts : un champ `"question"` (une question simple, liée au geste du Short, à laquelle on répond en une phrase, par exemple « Où sens-tu la chaleur en premier : les mains ou les pieds ? » ; jamais de question médicale ni intime). `metadonnees.description_short(sh, vid)` (utilisé par `publier.py`) ajoute alors, sous la phrase du Short, « 💬 <question> » puis « 🔔 Abonne-toi pour une méditation du soir chaque semaine : <lien d'abonnement> » ; le kit de mise en ligne (`kit-mise-en-ligne.md`) reprend ces deux lignes dans la description de chaque Short. Pas de lien vers la vidéo dans les descriptions des Shorts écrites à la main (consigne du 01/11). Appliqué à la Méditation du soir n° 1.

## Décisions du 02/11/2026 : Shorts qui accrochent, public de 55 ans et plus (accord de l'utilisateur « Applique 3 4 »)

Chiffres (YouTube Analytics au 30/10, `docs/referencement/concurrence-youtube.md`) : les Shorts font 96 % des vues mais
on en regarde 18 s en moyenne (28 à 33 % de Shorts de 50 à 60 s) ; 49 % du public a 65 ans et plus, 18 % 55-64 ans.

**Fait dans le robot** (`youtube/extras.py`, `youtube/rendu.py`) :
- Shorts de **35 s au plus** (`DUREE_SHORT`) ; Short respiration : une phrase entière puis **2 cycles** (`CYCLES_SHORT`).
- **Accroche visible dès la 1re image** (plus de fondu au noir, `haut1`/`haut2` affichés tout de suite, son en 0,15 s).
- **Textes plus gros** : accroche 100 pt (86 avant), sous-titres des Shorts 60 pt en demi-gras (50), bas 48/38 pt,
  sous-titres de la vidéo longue 54 pt en demi-gras (46).

**À appliquer par la tâche vidéo hebdomadaire** (écriture du plan) :
- `haut1` + `haut2` = **l'accroche** : une question ou une situation vécue, en 2 à 4 mots par ligne, qui se comprend
  sans le son (« Réveillé à 3 h ? » / « Essaie ceci », « Angoisse au lit ? » / « Ralentis ton souffle ») ; jamais une
  promesse de résultat.
- Les 4 `shorts_extra` : une partie qui contient un geste concret dès les premières secondes (le Short coupe à 35 s).
- **Public de 55 ans et plus** : phrases courtes, vocabulaire simple, sans anglicismes ; des `pause` plus nombreuses
  (la voix paraît plus lente) ; sujets qui les concernent en priorité : réveils nocturnes (3 h, 4 h), sommeil qui
  change avec l'âge, angoisse du soir, ruminations, tensions du corps au coucher, retour au calme après un réveil.
  Toujours sourcé et prudent (aucune promesse de soin, rappel « parles-en à ton médecin » quand c'est utile).
  Garder le tutoiement de la chaîne.

## Décisions du 01/11/2026 (accord de l'utilisateur « Oui pour les 3 propositions »)

Après le 2e passage sur la concurrence (`docs/referencement/concurrence-youtube.md`, section du 01/11) :
1. **Format long « voix + plusieurs heures de musique »** à partir de « Méditation du soir n° 1 » (8/11) : voix de 15 à
   20 minutes (script de 4 000 à 5 000 caractères), puis musique ; `"duree_totale_min": 180` (3 h) pour commencer
   (fichier d'environ 500 Mo, à téléverser à la main). Titre avec la durée réelle, par exemple « … (20 min + 3 h de
   musique) ». Technique (`youtube/rendu.py`) : 5 min après la fin de la voix, l'image se fige ; ce plan fixe est encodé
   une fois par bloc de 10 min (3 min de calcul) et répété, puis les 30 dernières secondes sont rendues normalement ;
   la musique est calculée par morceaux (`youtube/audio.py`), pour ne pas dépasser la mémoire. Essai local du 01/11 :
   durée exacte, décodage sans erreur, raccords invisibles (écart moyen entre deux images < 1 niveau de gris).
   **Plusieurs images pendant la musique (02/11/2026, demande de l'utilisateur)** : champ optionnel
   `"photos_musique"` du plan (photos Unsplash inédites, jamais déjà utilisées ailleurs ; `lum` règle chaque photo pour
   que toutes aient la luminosité du plan figé). La partie musique est partagée à parts égales entre le plan figé et ces
   photos, reliées par un fondu enchaîné de 8 s ; chaque plan fixe est encodé par morceaux de 60 s répétés ; les
   30 dernières secondes gardent la dernière photo. Contrôle : 12 images prises pendant la musique, aucune noire
   (`luminosite_musique` dans `rapport.json`). Essai local du 02/11 : durée exacte (200 s, 4 800 images), fondus et fin vérifiés à l'œil.
2. **5 Shorts par vidéo** (le Short respiration + 4 `shorts_extra`, chacun un geste concret d'une partie différente),
   titres vérifiés par `outils/anti_doublons.py`. Aucun crédit ElevenLabs de plus : ce sont des extraits de la voix.
3. **Shorts « pourquoi »** à tester : 30 à 45 secondes d'explication sourcée (une étude de l'article relié), par exemple
   « pourquoi les pensées tournent quand tu te couches », avec le lien du guide gratuit en 2e ligne de la description.
   Ils demandent des phrases de voix en plus (environ 500 caractères chacun) et un format de Short à ajouter au robot.


## Décisions du 09/11/2026 : vidIQ branché, statistiques réelles (délégation de l'utilisateur : « Fais ce qui est le mieux pour améliorer ma chaîne »)

**Outil** : connecteur vidIQ (plan gratuit, 150 crédits par mois, renouvelés le 9 de chaque mois ; 5 crédits par analyse ; compte yacinenettour@gmail.com ; chaîne `UCHDMGJxrRYnRwGZZFJNBpfg` reliée le 09/11). Usage : **recherche et mesure seulement** (`vidiq_channel_analytics`, `vidiq_outliers`, `vidiq_score_title`). Ne pas utiliser `generate_video`, `generate_script`, `generate_music`, `voiceover_generate` : ils consomment les crédits en quelques appels (20 crédits ou plus pour 8 secondes) et produisent du contenu qui se reconnaît comme généré ; consigne « rien ne doit faire IA » et « ne rien payer ».

**Chiffres réels du 01/10 au 09/11 (YouTube Analytics via vidIQ)** :
- 6 762 vues dont **6 098 par le fil des Shorts (90 %)**, 265 par les vidéos suggérées (4 %), 200 par la recherche (3 %, 62 s regardées en moyenne). 14 abonnés gagnés, soit 0,2 % des vues.
- Les 4 vidéos longues cumulent **378 vues** : 10 min (q0ucVBKNMjM) 112 vues, 4 min 22 s regardées (44 %) ; Jacobson 1 h (PbuSSZlDu1c) 168 vues, 9 min (15 %) ; ruminations 30 min (SCUS59y5kNs) 63 vues, 5 min (17 %) ; méditation de 3 h (BdW872_POhs) 35 vues, **24 min 44 s regardées par vue** (865 minutes au total, plus que tous les Shorts réunis : 490).
- Meilleur Short « respiration » (Son6Xv9kRTE, 1 116 vues) : 90 % des spectateurs encore là à 10 % de la durée, **53 % à 20 %** (c'est là que la perte est la plus forte), 36 % à 50 %, 23 % à la fin.
- **Attention à la lecture** : pour une vidéo d'endormissement, le pourcentage regardé est trompeur (le spectateur s'endort). Juger sur les **minutes regardées par vue** et sur les vues à 7 jours. Sur ce critère, la vidéo de 3 h reste la meilleure, mais avec seulement 35 vues : trop peu pour trancher.
- Petites chaînes françaises qui décollent (recherche vidIQ du 09/11, 15 vidéos) : durées de 15 à 60 minutes, jamais plus d'une heure ; sujets « système nerveux », « charge mentale », « anxiété », « ruminations », « pression » (exemples : 46 200 vues pour une méditation de 20 min d'une chaîne de 4 500 abonnés ; 6 900 vues pour une méditation anxiété d'1 h à 2 500 abonnés ; 3 200 vues pour « Faire taire les ruminations » à 197 abonnés). Chez les Shorts, deux accroches « situation vécue » à imiter sans copier : « La peur d'aller au lit », « Tu peux aller dormir si… ».

**À appliquer** :
1. **Test de format** : la vidéo « Méditation du soir n° 2 » dure **30 minutes au total** (voix 15 à 20 min, puis musique jusqu'à 30 min : `"duree_totale_min": 30`, titre « … (xx min) ») au lieu de 3 h ; garder la 3 h pour une vidéo suivante. Comparer ensuite, à 7 jours : vues, minutes regardées par vue, abonnés. Sujet : système nerveux / ruminations du soir, mot-clé en tête.
2. **Accroche des Shorts** (perte à 10-20 % de la durée) : `haut1`/`haut2` = situation vécue lisible sans le son, geste concret dans les 3 premières secondes, pas de salutation ni de présentation.
3. **Relier les Shorts à la vidéo longue** (aujourd'hui 90 % des vues sans chemin vers les vidéos longues) : à la main dans YouTube Studio, « Vidéo similaire » sur chaque Short (impossible par l'API) ; commentaire épinglé avec la question du Short.
4. **Régularité** : une vidéo par semaine sans trou (la tâche « Vidéo YouTube » est désactivée depuis le 06/11 : la réactiver avant le dimanche suivant).
5. **Mesure chaque lundi** (10 crédits) : `top_videos` et `traffic_sources` depuis la dernière mesure ; noter ici les vues, minutes regardées et abonnés.

## Vidéos en pause (09/11/2026, consigne de l'utilisateur : « priorise la création d'articles de qualité humanisés pour mon site et mets en stand-by les vidéos »)

- La tâche hebdomadaire « Vidéo YouTube » est désactivée : plus de nouveau plan ni de nouvelle voix ElevenLabs tant que l'utilisateur ne relance pas les vidéos.
- La « Méditation du soir n° 2 » (`meditation-du-soir-2-systeme-nerveux`, test de 30 minutes) a été écrite et sa voix contrôlée avant la pause ; sa fabrication par `youtube.yml` va à son terme (aucun envoi automatique : `envoi_manuel`).
- **À reprendre à la relance** : appliquer à la n° 2 le titre « Relaxation pour dormir : calmer son système nerveux (n° 2, 30 min) », les tags « sommeil profond » et « relaxation guidée pour dormir », écrire `kit-mise-en-ligne.md`, envoyer la miniature et les Shorts à l'utilisateur, régler « Vidéo similaire » à la main. Analyse des mots-clés : `docs/referencement/concurrence-youtube.md` (section du 09/11/2026).
- Les workflows `youtube.yml` (cron horaire) et `videos.yml` ne sont pas modifiés.
- **Résultat de la fabrication de la n° 2 (run n° 131, 09/11/2026)** : le workflow s'affiche « réussi » mais la vidéo est en `erreur_fabrication` (rien n'est publié ni envoyé) : « image presque noire à 129 s » (seuil : luminosité moyenne ≥ 8 pendant la voix). Voix : score 0,979, aucune phrase douteuse, aucune parole hors sous-titres ; durée 1 800 s exacte ; Shorts de 34,7 s, 25,4 s, 25,4 s, 21,9 s et 30,2 s. Cause : la photo de la bougie de « Le long soupir » (`unsplash-AaZlf5FgUws.jpg`, `lum` 1,0) est trop sombre ; les 4 photos de la musique sont aussi sombres (luminosités 4,8 à 5,0, contre 14 à 18 pour la n° 1). **À la reprise** : remplacer cette photo par une plus claire ou monter son `lum` (environ 2,5), monter les `lum` des photos de musique (environ ×3), puis remettre le statut `a_fabriquer` (la voix est déjà dans le dépôt, aucun crédit ElevenLabs à redépenser).
