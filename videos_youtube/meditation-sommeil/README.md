# Vidéo YouTube : méditation guidée pour le sommeil (test du 20/10/2026)

Demande de l'utilisateur : une vidéo de méditation guidée pour le sommeil d'au moins 10 minutes, avec animations,
sous-titres et vraie musique de détente, qui amène du trafic vers le site. Tout est gratuit.

- **Texte** : `script.py` (tutoiement, aucune promesse de soin, rappel « jamais en conduisant »).
- **Voix** : Piper, voix française « siwis » (CC BY 4.0), modèle récent qui prononce les voyelles nasales
  (le modèle ancien `voice-fr-siwis-medium` de rhasspy/piper v0.0.2 les supprime). À télécharger dans `voix/` :
  `https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-fr_FR-siwis-medium.tar.bz2`,
  puis `pip install piper-tts`. Vérification : `verif_voix.py` (transcription Whisper small de sherpa-onnx, 94 %).
- **Son** : `audio.py` → `piste.wav` et `timeline.json`. Musique « Deep Relaxation » (Kevin MacLeod, CC BY 4.0,
  `site/sources-audio/`), bols chantants CC0 (`site/sources-audio/bols/`), musique baissée sous la voix.
- **Image** : `rendu2.py` (une photo Unsplash par partie, zoom lent, fondus enchaînés, particules, brume, cercle de
  respiration 4-6, titres et sous-titres animés, adresse du site au début et à la fin) ; `seg.py` rend un morceau ;
  rendu en 4 morceaux parallèles puis assemblage avec `ffmpeg -f concat` et la piste audio.
- **Short** : `short.py` (1080 × 1920, 61 s, exercice de respiration, renvoie vers la vidéo complète).
- **Publication** : `youtube.md` (titre, description avec le lien du site, chapitres, tags, commentaire épinglé,
  réglages), `miniature-youtube.jpg`, `meditation-sommeil.srt`.
- **Photos** : `photos/` (8 photos Unsplash gratuites, inscrites dans `photos_sources.json` avec le statut
  « gardée (vidéo YouTube) ») ; réservées à cette vidéo.
- Les fichiers vidéo (228 Mo et 12 Mo) ne sont pas dans le dépôt : ils ont été envoyés à l'utilisateur.
