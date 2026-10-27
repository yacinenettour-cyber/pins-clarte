"""Bande-son : voix Kokoro « B » (choisie par l'utilisateur le 20/10/2026), musique « Deep Relaxation »
(Kevin MacLeod, CC BY 4.0) baissée sous la voix, bols chantants CC0, puis musique seule jusqu'à la durée visée.
Produit travail/<slug>/piste.wav, voix.wav (voix seule, pour le contrôle) et timeline.json."""
import difflib, json, os, subprocess, sys
import numpy as np
import soundfile as sf
from commun import DEPOT, SR, normaliser, reconnaissance, transcrire, MUSIQUE, BOLS, MODELES, charger_audio, dossier_travail, lire_plan

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
    # Voix Chatterbox Multilingual (Resemble AI, licence MIT, gratuite), réglage « E — posée » choisi à l'oreille par
    # l'utilisateur le 26/10/2026 (essais_voix/E-chatterbox-posee.mp3) : même réglages, aucun filtre ajouté.
    "chatterbox_posee": {"moteur": "chatterbox", "expressivite": 0.35, "rythme": 0.3, "temperature": 0.7, "graine": 42,
                         "filtre": "highpass=f=70", "niveau": 0.80},
    # Même voix, imitant une voix de référence française (youtube/voix/reference-francaise.wav, faite avec la voix
    # ff_siwis de Kokoro, corpus SIWIS CC BY 4.0) et rythme 0 (réglage conseillé contre l'accent de la référence) :
    # extrait « H » choisi à l'oreille par l'utilisateur le 26/10/2026, qui trouvait un ton anglais aux deux vidéos.
    "chatterbox_francais": {"moteur": "chatterbox", "expressivite": 0.35, "rythme": 0.0, "temperature": 0.7, "graine": 42,
                            "reference": "youtube/voix/reference-francaise.wav", "filtre": "highpass=f=70", "niveau": 0.80},
    # Voix ElevenLabs « Mila » (voix féminine douce, plan gratuit, 2 vidéos par mois), choisie par l'utilisateur le 27/10/2026
    "elevenlabs_mila": {"moteur": "elevenlabs", "filtre": "highpass=f=70", "niveau": 0.80},
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


class VoixChatterbox:
    """Même usage que Voix ; chaque phrase est générée une fois (les mots de la respiration reviennent souvent).
    Chatterbox invente parfois des sons ou des syllabes qui ne sont pas dans le texte (constaté par l'utilisateur le
    27/10/2026) : chaque phrase est donc réécoutée par Whisper et régénérée avec une autre graine si le texte entendu
    s'écarte du texte prévu, contient des mots en trop, ou si la phrase dure anormalement longtemps."""
    ESSAIS = 6
    VITESSE_MIN = 11.0  # caractères par seconde ; la médiane de cette voix est d'environ 14,5 (vidéo du 26/10)

    def __init__(self, reglage):
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
        self.r, self.cache, self.douteuses = reglage, {}, []
        self.m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
        self.rec = reconnaissance()

    def _generer(self, texte, tmp, graine):
        import torch, torchaudio
        torch.manual_seed(graine)
        ref = os.path.join(DEPOT, self.r["reference"]) if self.r.get("reference") else None
        w = self.m.generate(texte, language_id="fr", exaggeration=self.r["expressivite"], cfg_weight=self.r["rythme"],
                            temperature=self.r["temperature"], audio_prompt_path=ref)
        torchaudio.save(tmp, w, self.m.sr)
        a = charger_audio(tmp)
        env = np.abs(a).max(axis=1)
        idx = np.where(env > 0.01)[0]
        a = a[max(0, idx[0] - 800): idx[-1] + 4000]
        f = min(len(a) // 4, 1200)
        a[:f] *= np.linspace(0, 1, f)[:, None]
        a[-f:] *= np.linspace(1, 0, f)[:, None]
        return a

    def _verifier(self, texte, a):
        prevu, entendu = normaliser(texte), normaliser(transcrire(self.rec, a))
        sim = difflib.SequenceMatcher(None, prevu, entendu).ratio()
        longueur = len(entendu) / max(1, len(prevu))
        vitesse = len(texte) / (len(a) / SR)
        # Longueur juste (aucun mot en trop) : un écart de transcription léger est toléré.
        texte_ok = (sim >= 0.85 and 0.8 <= longueur <= 1.15) or (sim >= 0.8 and 0.9 <= longueur <= 1.1)
        ok = texte_ok and (len(texte) < 20 or vitesse >= self.VITESSE_MIN)
        note = sim - abs(1 - longueur) - max(0, self.VITESSE_MIN - vitesse) / 10
        return ok, texte_ok, note, (round(sim, 2), round(longueur, 2), round(vitesse, 1))

    def dire(self, texte, tmp):
        if texte not in self.cache:
            meilleur = None
            for k in range(self.ESSAIS):
                a = self._generer(texte, tmp, self.r["graine"] + k)
                ok, texte_ok, note, mesures = self._verifier(texte, a)
                # un essai au texte juste passe toujours avant un essai au texte faux, même plus rapide
                if meilleur is None or (texte_ok, note) > (meilleur[3], meilleur[0]):
                    meilleur = (note, a, mesures, texte_ok)
                if ok:
                    break
            # une phrase seulement lente (pause naturelle) est gardée ; un texte faux ou des mots en trop arrêtent la vidéo
            if not meilleur[3]:
                self.douteuses.append({"texte": texte, "mesures (similarité, longueur, car/s)": meilleur[2]})
            print(f"voix : {texte[:50]!r} essai {k + 1}, mesures {meilleur[2]}")
            self.cache[texte] = meilleur[1]
        return self.cache[texte].copy()


class VoixElevenLabs:
    """Voix ElevenLabs « Mila » (choix de l'utilisateur, 27/10/2026) : les phrases sont générées et réécoutées pendant
    une session Claude (youtube/voix_elevenlabs.py), rangées dans videos_youtube/<slug>/voix_elevenlabs/ ; ici on ne
    fait que les relire. Une phrase absente arrête la fabrication (le robot n'a pas accès à ElevenLabs)."""

    def __init__(self, slug):
        from voix_elevenlabs import chemin
        self.chemin = lambda texte: chemin(slug, texte)

    def dire(self, texte, tmp):
        f = self.chemin(texte)
        if not os.path.exists(f):
            raise FileNotFoundError(f"Phrase ElevenLabs absente, à générer pendant une session Claude : {texte!r}")
        a = charger_audio(f)
        env = np.abs(a).max(axis=1)
        idx = np.where(env > 0.01)[0]
        a = a[max(0, idx[0] - 800): idx[-1] + 4000]
        n = min(len(a) // 4, 1200)
        a[:n] *= np.linspace(0, 1, n)[:, None]
        a[-n:] *= np.linspace(1, 0, n)[:, None]
        return a


def fabriquer(slug):
    plan = lire_plan(slug)
    trav = dossier_travail(slug)
    tmp = os.path.join(trav, "_tts.wav")
    reglage = REGLAGES_VOIX[plan.get("voix", "standard")]
    if reglage.get("moteur") == "elevenlabs":
        voix = VoixElevenLabs(slug)
    elif reglage.get("moteur") == "chatterbox":
        voix = VoixChatterbox(reglage)
    else:
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
    # Mémoire (27/10/2026, vidéo d'1 h) : la voix et les bols n'occupent que le début ; la musique et le mélange final
    # sont traités par morceaux (le mélange d'1 h en un bloc dépassait la mémoire de la machine).
    Nv = min(N, int((fin_voix + 30) * SR))

    voixp = np.zeros((Nv, 2), np.float32)
    for d0, a in morceaux:
        i = int(d0 * SR)
        voixp[i:i + len(a)] += a[: Nv - i]
    brut = os.path.join(trav, "_voix.f32")
    voixp.tofile(brut)
    voixp = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", brut,
                                          "-af", reglage["filtre"], "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                                         capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)[:Nv].copy()
    os.remove(brut)
    voixp *= reglage["niveau"] / max(1e-6, np.abs(voixp).max())
    sf.write(os.path.join(trav, "voix.wav"), voixp.mean(axis=1), SR)

    # musique bouclée avec fondu enchaîné de 8 s aussi longtemps que nécessaire
    mus0 = charger_audio(MUSIQUE)
    mus0 /= max(1e-6, np.abs(mus0).max())
    x, L = 8 * SR, len(mus0)
    fond = np.linspace(0, 1, x, dtype=np.float32)[:, None]
    mus = np.empty((N, 2), np.float32)
    mus[:min(N, L)] = mus0[:min(N, L)]
    s0 = L - x
    while s0 < N:
        k = min(x, N - s0)
        mus[s0:s0 + k] = mus[s0:s0 + k] * (1 - fond[:k]) + mus0[:k] * fond[:k]
        k2 = min(L, N - s0)
        if k2 > x:
            mus[s0 + x:s0 + k2] = mus0[x:k2]
        s0 += L - x
    # volume de la musique calculé toutes les 480 échantillons (100 par seconde), puis appliqué morceau par morceau
    K = 480
    nb = (N + K - 1) // K
    tk = np.arange(nb) * K / SR
    env = np.convolve(np.abs(voixp[::K, 0]), np.ones(150) / 150, mode="same")
    parle = np.convolve((env > 0.01).astype(float), np.ones(200) / 200, mode="same").clip(0, 1)
    duck = np.zeros(nb)
    duck[:len(parle)] = parle[:nb]
    vol = 0.30 - 0.12 * duck
    vol *= np.clip(tk / 6, 0, 1)
    # après la voix, la musique baisse lentement d'un tiers (sommeil), puis fondu final de 60 s
    vol *= 1 - 0.33 * np.clip((tk - fin_voix) / 120, 0, 1)
    vol *= np.clip((duree - tk) / min(duree, 60), 0, 1) ** 1.5

    bol_long = charger_audio(os.path.join(BOLS, "bol-tibetain-long_itinerantmonk108_553049.ogg"), 14)
    bol_doux = charger_audio(os.path.join(BOLS, "bol-maillet-doux_steffcaffrey_449951.ogg"), 10)
    for b in (bol_long, bol_doux):
        b /= max(1e-6, np.abs(b).max())
        f = int(1.5 * SR)
        b[-f:] *= np.linspace(1, 0, f)[:, None]
    bols = np.zeros((Nv, 2), np.float32)

    def poser(b, t0, g):
        i = int(t0 * SR)
        bols[i:i + len(b)] += g * b[: Nv - i]
    # cloche de départ : 0,35 → 0,12 avec une montée de 2 s (« la cloche au démarrage est trop forte », 27/10/2026)
    debut = bol_long.copy()
    debut[: 2 * SR] *= np.linspace(0, 1, 2 * SR)[:, None]
    poser(debut, 1.0, 0.12)
    for ti in titres:
        poser(bol_doux, ti["debut"], 0.18)
    poser(bol_long, fin_voix + 2, 0.22)

    brut = os.path.join(trav, "_piste.f32")
    piste = np.memmap(brut, np.float32, "w+", shape=(N, 2))
    pic, M = 0.0, 600 * SR
    for a in range(0, N, M):
        b = min(N, a + M)
        v = np.repeat(vol[a // K: (b + K - 1) // K], K)[: b - a].astype(np.float32)[:, None]
        m = mus[a:b] * v
        if a < Nv:
            c = min(b, Nv)
            m[: c - a] += voixp[a:c] + bols[a:c]
        piste[a:b] = m
        pic = max(pic, float(np.abs(m).max()))
    for a in range(0, N, M):
        piste[a:a + M] *= 0.89 / pic
    piste.flush()
    del piste, mus
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", brut,
                    "-af", "loudnorm=I=-20:TP=-2:LRA=11", "-ar", str(SR), os.path.join(trav, "piste.wav")], check=True)
    os.remove(brut)
    tl = {"duree": duree, "fin_voix": fin_voix, "cues": cues, "titres": titres, "souffles": souffles,
          "voix_douteuses": getattr(voix, "douteuses", []),
          "insp": INSP, "exp": EXP}
    json.dump(tl, open(os.path.join(trav, "timeline.json"), "w"), ensure_ascii=False, indent=1)
    print(f"bande-son : {duree / 60:.1f} min, voix jusqu'à {fin_voix / 60:.1f} min, {len(cues)} sous-titres")
    return tl


if __name__ == "__main__":
    fabriquer(sys.argv[1])
