"""Extraits d'essai de voix (26/10/2026, demande de l'utilisateur : voix plus naturelle que Kokoro).
Lit essais_voix/demande.json et produit un MP3 par variante dans essais_voix/ : la voix Chatterbox Multilingual
(Resemble AI, licence MIT, gratuite) sur la musique de la chaîne, au même niveau que dans les vidéos.
Rien n'est publié : ces extraits servent seulement à choisir la voix à l'oreille."""
import json, os, subprocess, sys
import numpy as np
import torch, torchaudio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import DEPOT, MUSIQUE, SR, charger_audio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

D = os.path.join(DEPOT, "essais_voix")
demande = json.load(open(os.path.join(D, "demande.json"), encoding="utf-8"))
modele = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
for v in demande["variantes"]:
    morceaux = []
    for phrase in demande["phrases"]:
        torch.manual_seed(v.get("graine", 42))
        w = modele.generate(phrase, language_id="fr", exaggeration=v["expressivite"], cfg_weight=v["rythme"],
                            temperature=v.get("temperature", 0.8))
        tmp = os.path.join(D, "_tmp.wav")
        torchaudio.save(tmp, w, modele.sr)
        morceaux.append(charger_audio(tmp))
        os.remove(tmp)
    silence = np.zeros((int(demande.get("pause", 2.5) * SR), 2), np.float32)
    voix = np.concatenate([silence[:SR]] + [x for m in morceaux for x in (m, silence)])
    voix *= 0.80 / max(1e-6, np.abs(voix).max())
    mus = charger_audio(MUSIQUE)
    mus = np.resize(mus, voix.shape)  # répète la musique si l'extrait est plus long
    mus = mus / max(1e-6, np.abs(mus).max()) * 0.20
    piste = voix + mus
    piste *= 0.89 / np.abs(piste).max()
    brut = os.path.join(D, "_p.f32")
    piste.astype(np.float32).tofile(brut)
    sortie = os.path.join(D, f"{v['nom']}.mp3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", brut,
                    "-af", "loudnorm=I=-20:TP=-2:LRA=11", "-b:a", "160k", sortie], check=True)
    os.remove(brut)
    print("extrait :", sortie)
