#!/usr/bin/env python3
"""Audios de respiration guidée 4-6 (inspirer 4 s, expirer 6 s : 6 respirations par minute), sans voix.

Sons entièrement synthétisés ici (aucune banque de sons, aucun service payant) :
- un souffle doux (bruit filtré) qui monte pendant l'inspiration et redescend pendant l'expiration ;
- une clochette aiguë au début de chaque inspiration, une clochette plus grave au début de chaque expiration ;
- un fond très discret (accord tenu), qui s'installe au début et s'éteint à la fin.

Usage : python3 site/outils/audios_respiration.py  -> site/contenu/audio/respiration-4-6-{3,5,10}-min.mp3
"""
import os
import subprocess
import tempfile
import wave

import numpy as np

SR = 44100
INSPIRE, EXPIRE = 4.0, 6.0
CYCLE = INSPIRE + EXPIRE
INTRO, OUTRO = 8.0, 14.0
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "contenu", "audio")
rng = np.random.default_rng(46)


def souffle_brut(n):
    """Bruit « rose » adouci (pente 1/f, coupé au-delà de 1,6 kHz) : un souffle, pas un grésillement."""
    spectre = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    filtre = 1 / np.sqrt(np.maximum(f, 40.0)) / (1 + (f / 1600.0) ** 4)
    filtre[f < 60] *= (f[f < 60] / 60.0) ** 2
    x = np.fft.irfft(spectre * filtre, n)
    return x / np.max(np.abs(x))


def clochette(freq, duree, niveau):
    """Clochette douce (partiels de bol chantant, attaque de 8 ms, décroissance lente)."""
    t = np.arange(int(duree * SR)) / SR
    son = np.zeros_like(t)
    for rapport, poids, amort in ((1.0, 1.0, 1.6), (2.76, 0.32, 3.2), (5.40, 0.10, 5.5)):
        son += poids * np.sin(2 * np.pi * freq * rapport * t) * np.exp(-amort * t / duree * 2.2)
    attaque = np.minimum(1.0, t / 0.008)
    return niveau * son * attaque / 1.42


def fond(n):
    """Accord tenu très discret (la-mi-la-si), chaque note respirant lentement."""
    t = np.arange(n) / SR
    x = np.zeros(n)
    for freq, phase in ((110.0, 0.0), (164.81, 1.3), (220.0, 2.1), (246.94, 4.0)):
        lfo = 0.6 + 0.4 * np.sin(2 * np.pi * (0.021 + freq / 40000) * t + phase)
        x += lfo * (np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * (freq + 0.25) * t))
    return x / 6.0


def enveloppe_cycle():
    """Montée douce sur 4 s (inspiration), descente plus lente sur 6 s (expiration)."""
    t = np.arange(int(CYCLE * SR)) / SR
    env = np.empty_like(t)
    i = t < INSPIRE
    env[i] = np.sin(np.pi / 2 * t[i] / INSPIRE) ** 2
    env[~i] = np.cos(np.pi / 2 * (t[~i] - INSPIRE) / EXPIRE) ** 2
    return 0.12 + 0.88 * env


def piste(cycles):
    duree = INTRO + cycles * CYCLE + OUTRO
    n = int(duree * SR)
    mix = np.zeros(n)
    # Fond : s'installe pendant l'introduction, s'éteint pendant la fin.
    t = np.arange(n) / SR
    gain_fond = np.clip(t / INTRO, 0, 1) * np.clip((duree - t) / (OUTRO - 2), 0, 1)
    mix += 0.06 * fond(n) * gain_fond
    env = enveloppe_cycle()
    lc = len(env)
    for k in range(cycles):
        debut = int((INTRO + k * CYCLE) * SR)
        # Sur la piste longue (endormissement), les repères s'adoucissent dans le dernier tiers.
        douceur = 1.0 if k < cycles * 2 / 3 or cycles < 40 else 1.0 - 0.45 * (k - cycles * 2 / 3) / (cycles / 3)
        mix[debut:debut + lc] += 0.30 * douceur * souffle_brut(lc) * env
        aigue = clochette(659.25, 3.2, 0.16 * douceur)
        grave = clochette(392.0, 5.0, 0.15 * douceur)
        mix[debut:debut + len(aigue)] += aigue
        d2 = debut + int(INSPIRE * SR)
        mix[d2:d2 + len(grave)] += grave
    # Clochette finale, puis silence.
    fin = int((INTRO + cycles * CYCLE + 1.0) * SR)
    derniere = clochette(329.63, 7.0, 0.14)
    mix[fin:fin + len(derniere)] += derniere[: n - fin]
    # Fondu de sortie général sur les 4 dernières secondes et léger limiteur.
    mix *= np.clip((duree - t) / 4.0, 0, 1)
    mix = np.tanh(1.2 * mix) / np.tanh(1.2)
    return mix / np.max(np.abs(mix)) * 0.70  # crête vers -3 dB


def ecrire_mp3(x, chemin):
    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, "a.wav")
        with wave.open(wav, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((x * 32767).astype("<i2").tobytes())
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-codec:a", "libmp3lame", "-b:a", "64k",
                        "-ac", "1", "-metadata", "title=" + os.path.basename(chemin)[:-4].replace("-", " "),
                        "-metadata", "artist=Clarté Mentale", chemin], check=True)


def main():
    os.makedirs(SORTIE, exist_ok=True)
    for minutes in (3, 5, 10):
        cycles = int(minutes * 60 / CYCLE)
        x = piste(cycles)
        chemin = os.path.join(SORTIE, f"respiration-4-6-{minutes}-min.mp3")
        ecrire_mp3(x, chemin)
        print(chemin, f"{len(x) / SR:.0f} s", f"{os.path.getsize(chemin) / 1e6:.1f} Mo")


if __name__ == "__main__":
    main()
