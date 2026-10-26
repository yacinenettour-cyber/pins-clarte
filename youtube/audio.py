"""Bande-son : voix Kokoro « B » (choisie par l'utilisateur le 20/10/2026), musique « Deep Relaxation »
(Kevin MacLeod, CC BY 4.0) baissée sous la voix, bols chantants CC0, puis musique seule jusqu'à la durée visée.
Produit travail/<slug>/piste.wav, voix.wav (voix seule, pour le contrôle) et timeline.json."""
import json, os, subprocess, sys
import numpy as np
import soundfile as sf
from commun import SR, MUSIQUE, BOLS, MODELES, charger_audio, dossier_travail, lire_plan

INSP, EXP = 4.0, 6.0
VITESSE = 0.82
# voix adoucie : aigus et sifflantes réduits, son plus chaud, léger écho de pièce
DOUX = ("highpass=f=90,lowpass=f=7500,equalizer=f=220:t=q:w=1:g=2.5,equalizer=f=3200:t=q:w=1.4:g=-3.5,deesser=i=0.4,"
        "acompressor=threshold=-22dB:ratio=2.2:attack=25:release=300,aecho=0.85:0.55:45|85:0.14|0.09")
# Réglages de voix choisis par vidéo (plan["voix"] = nom du réglage) ; sans champ « voix » : réglage de la 1re vidéo.
# « plus_douce » et « tres_douce » (26/10/2026, demande de l'utilisateur : « une voix plus douce que dans la 1re vidéo ») :
# plus lente, un peu plus grave (hauteur -4 % / -6 % à durée égale), aigus et sifflantes plus atténués, voix un peu
# moins forte au-dessus de la musique.
REGLAGES_VOIX = {
    "standard": {"vitesse": VITESSE, "filtre": DOUX, "niveau": 0.80},
    "plus_douce": {"vitesse": 0.76, "niveau": 0.72, "filtre": (
        "highpass=f=80,lowpass=f=6000,equalizer=f=200:t=q:w=1:g=3.5,equalizer=f=3000:t=q:w=1.5:g=-5,"
        "equalizer=f=6500:t=q:w=1:g=-4,deesser=i=0.6,acompressor=threshold=-24dB:ratio=2:attack=30:release=400,"
        f"asetrate={int(SR * 0.96)},aresample={SR},atempo={1 / 0.96:.7f},aecho=0.85:0.6:50|95:0.16|0.10")},
    "tres_douce": {"vitesse": 0.72, "niveau": 0.68, "filtre": (
        "highpass=f=80,lowpass=f=5200,equalizer=f=180:t=q:w=1:g=4,equalizer=f=2800:t=q:w=1.5:g=-6,"
        "equalizer=f=6000:t=q:w=1:g=-6,deesser=i=0.7,acompressor=threshold=-26dB:ratio=2:attack=40:release=500,"
        f"asetrate={int(SR * 0.94)},aresample={SR},atempo={1 / 0.94:.7f},aecho=0.85:0.65:60|110:0.18|0.12")},
}
# mots que le phonétiseur lit en anglais (constaté le 20/10) : remplacés dans les phonèmes
CORRECTIONS = {"(en)dˈɒs(fr)": "dˈo", "(en)ɹˈɪθm(fr)": "ʁˈitm"}
MOTS_SOUFFLE = {"Inspire…": "Inspire doucement", "Expire…": "Expire lentement"}


class Voix:
    def __init__(self, vitesse=VITESSE):
        self.vitesse = vitesse
        from kokoro_onnx import Kokoro
        self.k = Kokoro(os.path.join(MODELES, "kokoro-v1.0.onnx"), os.path.join(MODELES, "voices-v1.0.bin"))

    def phonemes(self, texte):
        # « ... » final : sinon Kokoro coupe la dernière syllabe
        ph = self.k.tokenizer.phonemize(texte.rstrip(".…") + "...", "fr-fr")
        for a, b in CORRECTIONS.items():
            ph = ph.replace(a, b)
        if "(en)" in ph or "(" in ph:
            raise ValueError(f"Mot lu dans une autre langue, à reformuler : {texte!r} → {ph}")
        return ph

    def dire(self, texte, tmp):
        a, sr = self.k.create(self.phonemes(texte), voice="ff_siwis", speed=self.vitesse, lang="fr-fr", is_phonemes=True)
        sf.write(tmp, a, sr)
        a = charger_audio(tmp)
        env = np.abs(a).max(axis=1)
        idx = np.where(env > 0.01)[0]
        a = a[max(0, idx[0] - 800): idx[-1] + 4000]
        f = min(len(a) // 4, 1200)
        a[:f] *= np.linspace(0, 1, f)[:, None]
        a[-f:] *= np.linspace(1, 0, f)[:, None]
        return a


def fabriquer(slug):
    plan = lire_plan(slug)
    trav = dossier_travail(slug)
    tmp = os.path.join(trav, "_tts.wav")
    reglage = REGLAGES_VOIX[plan.get("voix", "standard")]
    voix = Voix(reglage["vitesse"])
    morceaux, cues, titres, souffles = [], [], [], []
    t = 0.0
    for el in plan["script"]:
        if el[0] == "pause":
            t += el[1]
        elif el[0] == "titre":
            titres.append({"debut": t, "fin": t + 9, "texte": el[1]})
            t += el[2]
        elif el[0] == "dire":
            a = voix.dire(el[1], tmp)
            morceaux.append((t, a))
            cues.append({"debut": t, "fin": t + len(a) / SR, "texte": el[1]})
            t += len(a) / SR + el[2]
        elif el[0] == "souffle":
            n, guide = el[1], el[2]
            souffles.append({"debut": t, "cycles": n})
            for _ in range(n):
                if guide:
                    for mot, decal in (("Inspire…", 0.15), ("Expire…", INSP + 0.15)):
                        a = voix.dire(MOTS_SOUFFLE[mot], tmp)
                        morceaux.append((t + decal, a))
                        cues.append({"debut": t + decal, "fin": t + decal + len(a) / SR, "texte": mot})
                t += INSP + EXP
            t += 1.0
        else:
            raise ValueError(f"Élément de script inconnu : {el}")
    fin_voix = cues[-1]["fin"]
    duree = max(t, plan.get("duree_totale_min", 0) * 60)
    N = int(duree * SR)

    voixp = np.zeros((N, 2), np.float32)
    for d0, a in morceaux:
        i = int(d0 * SR)
        voixp[i:i + len(a)] += a[: N - i]
    brut = os.path.join(trav, "_voix.f32")
    voixp.tofile(brut)
    voixp = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", brut,
                                          "-af", reglage["filtre"], "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                                         capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)[:N].copy()
    os.remove(brut)
    voixp *= reglage["niveau"] / max(1e-6, np.abs(voixp).max())
    sf.write(os.path.join(trav, "voix.wav"), voixp.mean(axis=1), SR)

    # musique bouclée avec fondu enchaîné de 8 s aussi longtemps que nécessaire
    mus0 = charger_audio(MUSIQUE)
    mus0 /= max(1e-6, np.abs(mus0).max())
    x = 8 * SR
    mus = mus0.copy()
    while len(mus) < N:
        fond = np.linspace(0, 1, x)[:, None]
        mus = np.concatenate([mus[:-x], mus[-x:] * (1 - fond) + mus0[:x] * fond, mus0[x:]])
    mus = mus[:N]
    env = np.convolve(np.abs(voixp[::480, 0]), np.ones(150) / 150, mode="same")
    parle = np.convolve((env > 0.01).astype(float), np.ones(200) / 200, mode="same").clip(0, 1)
    duck = np.interp(np.arange(N) / 480, np.arange(len(parle)), parle)
    vol = 0.30 - 0.12 * duck
    vol[: 6 * SR] *= np.linspace(0, 1, 6 * SR)
    # après la voix, la musique baisse lentement d'un tiers (sommeil), puis fondu final de 60 s
    apres = np.clip((np.arange(N) / SR - fin_voix) / 120, 0, 1)
    vol *= 1 - 0.33 * apres
    fin = min(N, 60 * SR)
    vol[-fin:] *= np.linspace(1, 0, fin) ** 1.5
    mus *= vol[:, None]

    bol_long = charger_audio(os.path.join(BOLS, "bol-tibetain-long_itinerantmonk108_553049.ogg"), 14)
    bol_doux = charger_audio(os.path.join(BOLS, "bol-maillet-doux_steffcaffrey_449951.ogg"), 10)
    for b in (bol_long, bol_doux):
        b /= max(1e-6, np.abs(b).max())
        f = int(1.5 * SR)
        b[-f:] *= np.linspace(1, 0, f)[:, None]
    bols = np.zeros((N, 2), np.float32)

    def poser(b, t0, g):
        i = int(t0 * SR)
        bols[i:i + len(b)] += g * b[: N - i]
    poser(bol_long, 1.0, 0.35)
    for ti in titres:
        poser(bol_doux, ti["debut"], 0.18)
    poser(bol_long, fin_voix + 2, 0.22)

    piste = voixp + mus + bols
    piste *= 0.89 / np.abs(piste).max()
    brut = os.path.join(trav, "_piste.f32")
    piste.astype(np.float32).tofile(brut)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", brut,
                    "-af", "loudnorm=I=-20:TP=-2:LRA=11", "-ar", str(SR), os.path.join(trav, "piste.wav")], check=True)
    os.remove(brut)
    tl = {"duree": duree, "fin_voix": fin_voix, "cues": cues, "titres": titres, "souffles": souffles,
          "insp": INSP, "exp": EXP}
    json.dump(tl, open(os.path.join(trav, "timeline.json"), "w"), ensure_ascii=False, indent=1)
    print(f"bande-son : {duree / 60:.1f} min, voix jusqu'à {fin_voix / 60:.1f} min, {len(cues)} sous-titres")
    return tl


if __name__ == "__main__":
    fabriquer(sys.argv[1])
