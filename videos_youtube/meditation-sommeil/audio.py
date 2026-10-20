"""Voix (Piper), musique et bols : produit piste.wav (48 kHz stéréo) et timeline.json (sous-titres, titres, respiration)."""
import json, os, subprocess, sys, wave
import numpy as np
from piper import PiperVoice, SynthesisConfig
from script import SCRIPT

ICI = os.path.dirname(os.path.abspath(__file__))
DEPOT = "/home/user/pins-clarte"
SR = 48000
VOIX = sys.argv[1] if len(sys.argv) > 1 else "siwis"
if VOIX == "siwis":
    d = f"{ICI}/voix/vits-piper-fr_FR-siwis-medium/fr_FR-siwis-medium.onnx"; spk = None
else:
    d = f"{ICI}/voix/vits-piper-fr_FR-upmc-medium/fr_FR-upmc-medium.onnx"; spk = 0
voix = PiperVoice.load(d, config_path=d + ".json")
CFG = SynthesisConfig(speaker_id=spk, length_scale=1.32, noise_scale=0.55, noise_w_scale=0.7)
# Voix « B » choisie par l'utilisateur le 20/10 : Kokoro ff_siwis (plus naturelle), ralentie puis adoucie
KOKORO = len(sys.argv) > 2 and sys.argv[2] == "kokoro"
if KOKORO:
    import soundfile as sf
    from kokoro_onnx import Kokoro
    kok = Kokoro(f"{ICI}/kokoro/kokoro-v1.0.onnx", f"{ICI}/kokoro/voices-v1.0.bin")
DOUX = ("highpass=f=90,lowpass=f=7500,equalizer=f=220:t=q:w=1:g=2.5,equalizer=f=3200:t=q:w=1.4:g=-3.5,deesser=i=0.4,"
        "acompressor=threshold=-22dB:ratio=2.2:attack=25:release=300,aecho=0.85:0.55:45|85:0.14|0.09")
INSP, EXP = 4.0, 6.0


def charger(chemin, duree=None):
    cmd = ["ffmpeg", "-v", "error", "-i", chemin]
    if duree:
        cmd += ["-t", str(duree)]
    cmd += ["-f", "f32le", "-ac", "2", "-ar", str(SR), "-"]
    a = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32)
    return a.reshape(-1, 2).copy()


def tts(texte):
    tmp = f"{ICI}/_tts.wav"
    if KOKORO:
        # « ... » final : évite que la dernière syllabe soit coupée ; mots que le phonétiseur lit en anglais corrigés
        ph = kok.tokenizer.phonemize(texte.rstrip(".…") + "...", "fr-fr")
        ph = ph.replace("(en)dˈɒs(fr)", "dˈo").replace("(en)ɹˈɪθm(fr)", "ʁˈitm")
        assert "(en)" not in ph, (texte, ph)
        k, sr = kok.create(ph, voice="ff_siwis", speed=0.82, lang="fr-fr", is_phonemes=True)
        sf.write(tmp, k, sr)
    else:
        with wave.open(tmp, "wb") as w:
            voix.synthesize_wav(texte, w, syn_config=CFG)
    a = charger(tmp)
    # coupe les silences de bord et adoucit attaque / fin
    env = np.abs(a).max(axis=1)
    idx = np.where(env > 0.01)[0]
    a = a[max(0, idx[0] - 800): idx[-1] + 4000]
    f = min(len(a) // 4, 1200)
    a[:f] *= np.linspace(0, 1, f)[:, None]
    a[-f:] *= np.linspace(1, 0, f)[:, None]
    return a


morceaux, cues, titres, souffles = [], [], [], []
t = 0.0
for el in SCRIPT:
    if el[0] == "pause":
        t += el[1]
    elif el[0] == "titre":
        titres.append({"debut": t, "fin": t + 9, "texte": el[1]})
        t += el[2]
    elif el[0] == "dire":
        a = tts(el[1])
        morceaux.append((t, a))
        cues.append({"debut": t, "fin": t + len(a) / SR, "texte": el[1]})
        t += len(a) / SR + el[2]
    elif el[0] == "souffle":
        n, guide = el[1], el[2]
        souffles.append({"debut": t, "cycles": n})
        for i in range(n):
            if guide:
                for mot, decal in (("Inspire…", 0.15), ("Expire…", INSP + 0.15)):
                    # un mot seul est mal prononcé par Kokoro : « Inspire doucement », « Expire lentement »
                    a = tts({"Inspire…": "Inspire doucement", "Expire…": "Expire lentement"}[mot] if KOKORO else mot.replace("…", ""))
                    morceaux.append((t + decal, a))
                    cues.append({"debut": t + decal, "fin": t + decal + max(len(a) / SR, 2.5), "texte": mot})
            t += INSP + EXP
        t += 1.0
duree = t
print("durée totale", round(duree, 1), "s =", round(duree / 60, 2), "min")

N = int(duree * SR)
voixp = np.zeros((N, 2), np.float32)
for d0, a in morceaux:
    i = int(d0 * SR); voixp[i:i + len(a)] += a[: N - i]
if KOKORO:
    brut_v = f"{ICI}/_voix.f32"
    voixp.astype(np.float32).tofile(brut_v)
    voixp = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", brut_v,
                                          "-af", DOUX, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                                         capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)[:N].copy()
    os.remove(brut_v)
voixp *= 0.80 / max(1e-6, np.abs(voixp).max())

# Musique « Deep Relaxation » (Kevin MacLeod, CC BY 4.0) : 11 min ; bouclée avec fondu si la vidéo est plus longue
mus = charger(f"{DEPOT}/site/sources-audio/deep-relaxation-extrait.mp3")
while len(mus) < N:
    x = 8 * SR
    fond = np.linspace(0, 1, x)[:, None]
    mus = np.concatenate([mus[:-x], mus[-x:] * (1 - fond) + mus[:x] * fond, mus[x:]])
mus = mus[:N] / max(1e-6, np.abs(mus).max())
# volume : plus bas sous la voix (« ducking » doux), fondu d'entrée et longue sortie
env_voix = np.convolve(np.abs(voixp[::480, 0]), np.ones(150) / 150, mode="same")  # 10 ms par pas, ~1,5 s
parle = np.convolve((env_voix > 0.01).astype(float), np.ones(200) / 200, mode="same").clip(0, 1)
duck = np.interp(np.arange(N) / 480, np.arange(len(parle)), parle)
vol = 0.30 - 0.12 * duck
vol[: 6 * SR] *= np.linspace(0, 1, 6 * SR)
fin = 45 * SR
vol[-fin:] *= np.linspace(1, 0, fin) ** 1.5
mus *= vol[:, None]

# Bols chantants (CC0) : ouverture, chaque partie, et fin de la voix
bol_long = charger(f"{DEPOT}/site/sources-audio/bols/bol-tibetain-long_itinerantmonk108_553049.ogg", 14)
bol_doux = charger(f"{DEPOT}/site/sources-audio/bols/bol-maillet-doux_steffcaffrey_449951.ogg", 10)
for b in (bol_long, bol_doux):
    b /= max(1e-6, np.abs(b).max())
    f = int(1.5 * SR); b[-f:] *= np.linspace(1, 0, f)[:, None]
bols = np.zeros((N, 2), np.float32)
def poser(b, t0, g):
    i = int(t0 * SR); bols[i:i + len(b)] += g * b[: N - i]
poser(bol_long, 1.0, 0.35)
for ti in titres:
    poser(bol_doux, ti["debut"], 0.18)
poser(bol_long, cues[-1]["fin"] + 2, 0.22)

piste = voixp + mus + bols
piste *= 0.89 / np.abs(piste).max()
brut = f"{ICI}/_piste.f32"
piste.astype(np.float32).tofile(brut)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", brut,
                "-af", "loudnorm=I=-20:TP=-2:LRA=11", "-ar", str(SR), f"{ICI}/piste.wav"], check=True)
os.remove(brut)
json.dump({"duree": duree, "cues": cues, "titres": titres, "souffles": souffles, "insp": INSP, "exp": EXP,
           "fin_voix": cues[-1]["fin"]}, open(f"{ICI}/timeline.json", "w"), ensure_ascii=False, indent=1)
print(len(cues), "sous-titres,", len(titres), "titres")
