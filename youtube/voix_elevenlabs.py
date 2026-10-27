"""Voix ElevenLabs « Mila » (27/10/2026, choix de l'utilisateur) : les phrases sont générées pendant une session Claude
(connecteur ElevenLabs, quota gratuit, 1 crédit par caractère), puis rangées dans videos_youtube/<slug>/voix_elevenlabs/
sous un nom tiré du texte. Le robot GitHub (audio.py) ne fait que les relire : il n'a pas accès à ElevenLabs.

Usage pendant la session :
  python3 youtube/voix_elevenlabs.py manquantes <slug>          → liste des phrases encore à générer
  python3 youtube/voix_elevenlabs.py ranger <slug> <texte> <url> → télécharge, réécoute (Whisper) et range la phrase
"""
import difflib, hashlib, json, os, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(__file__))
from commun import DEPOT, mots_normalises, normaliser

VOIX_ID = "hndZlkpVm5i9lXBY9CKj"  # « Mila - Soft Soothing Meditation & Sleep Voice »
MODELE = "eleven_multilingual_v2"
MOTS_SOUFFLE = {"Inspire…": "Inspire doucement", "Expire…": "Expire lentement"}


def cle(texte):
    return hashlib.sha1(texte.strip().encode("utf-8")).hexdigest()[:16]


def dossier(slug):
    d = os.path.join(DEPOT, "videos_youtube", slug, "voix_elevenlabs")
    os.makedirs(d, exist_ok=True)
    return d


def chemin(slug, texte):
    return os.path.join(dossier(slug), cle(texte) + ".mp3")


def phrases(slug):
    plan = json.load(open(os.path.join(DEPOT, "videos_youtube", slug, "plan.json"), encoding="utf-8"))
    out = []
    for el in plan["script"]:
        if el[0] == "dire" and el[1] not in out:
            out.append(el[1])
        elif el[0] == "souffle" and el[2]:
            for t in MOTS_SOUFFLE.values():
                if t not in out:
                    out.append(t)
    return out


def verifier(fichier, texte):
    """Réécoute la phrase avec Whisper : (ok, entendu, similarité, mots manquants ou en trop)."""
    import soundfile as sf
    from commun import reconnaissance
    with tempfile.TemporaryDirectory() as t:
        wav = os.path.join(t, "a.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", fichier, "-ac", "1", "-ar", "16000", wav], check=True)
        a, sr = sf.read(wav, dtype="float32")
    rec = reconnaissance()
    s = rec.create_stream()
    s.accept_waveform(sr, a)
    rec.decode_stream(s)
    entendu = s.result.text.strip()
    sim = difflib.SequenceMatcher(None, normaliser(texte), normaliser(entendu)).ratio()
    mp, me = mots_normalises(texte), mots_normalises(entendu)
    ecarts = [(" ".join(mp[i1:i2]), " ".join(me[j1:j2])) for op, i1, i2, j1, j2
              in difflib.SequenceMatcher(None, mp, me).get_opcodes() if op != "equal"]
    longueur = len(normaliser(entendu)) / max(1, len(normaliser(texte)))
    ok = (sim >= 0.85 or (sim >= 0.8 and 0.9 <= longueur <= 1.1)) and 0.8 <= longueur <= 1.15
    return ok, entendu, round(sim, 2), ecarts


if __name__ == "__main__":
    action, slug = sys.argv[1], sys.argv[2]
    if action == "manquantes":
        m = [p for p in phrases(slug) if not os.path.exists(chemin(slug, p))]
        print(json.dumps(m, ensure_ascii=False, indent=1))
        print(len(m), "phrases,", sum(len(p) for p in m), "caractères")
    elif action == "ranger":
        texte, url = sys.argv[3], sys.argv[4]
        f = chemin(slug, texte)
        subprocess.run(["curl", "-sSL", "-m", "60", "-o", f, url], check=True)
        ok, entendu, sim, ecarts = verifier(f, texte)
        print(json.dumps({"ok": ok, "texte": texte, "entendu": entendu, "sim": sim, "ecarts": ecarts}, ensure_ascii=False))
        if not ok:
            os.rename(f, f + ".douteuse")
