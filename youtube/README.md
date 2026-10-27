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
