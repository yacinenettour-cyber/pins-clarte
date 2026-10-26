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

**Envoi manuel (26/10/2026)** : avec `"envoi_manuel": true` dans le plan, la vidéo est fabriquée et contrôlée mais rien n'est envoyé (l'envoi par Composio échoue, voir le journal du 22/10) : statut `fabriquee`, vidéo et Short dans l'artefact du run (onglet Actions, 7 jours), miniature et sous-titres dans le dossier du plan ; l'utilisateur met en ligne à la main.

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
