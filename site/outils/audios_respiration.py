#!/usr/bin/env python3
"""Audios de respiration guidée 4-6 (inspirer 4 s, expirer 6 s : 6 respirations par minute), sans voix.

Mélange :
- une musique de détente : extrait de « Deep Relaxation », Kevin MacLeod (incompetech.com),
  licence Creative Commons Attribution 4.0 (crédit obligatoire et visible : voir CREDIT et la page
  /respiration-guidee/) — source dans site/sources-audio/ ;
- des repères synthétisés ici : une clochette au début de chaque inspiration (sol) et de chaque expiration (do),
  accordées sur la tonalité de la musique (centrée sur do), et un souffle très doux qui monte pendant
  l'inspiration et redescend pendant l'expiration.

Usage : python3 site/outils/audios_respiration.py  -> site/contenu/audio/respiration-4-6-{3,5,10}-min.mp3
        (+ musique seule du minuteur de /exercices-respiration/ ; « minuteur » en argument : elle seule)
"""
import os
import subprocess

import numpy as np

SR = 44100
INSPIRE, EXPIRE = 4.0, 6.0
CYCLE = INSPIRE + EXPIRE
INTRO, OUTRO = 8.0, 14.0
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "contenu", "audio")
MUSIQUE = os.path.join(RACINE, "sources-audio", "deep-relaxation-extrait.mp3")
CREDIT = ("Musique : Deep Relaxation, Kevin MacLeod (incompetech.com), licence Creative Commons Attribution 4.0 "
          "(https://creativecommons.org/licenses/by/4.0/) ; extrait mixé avec des repères de respiration par Clarté Mentale")
NIVEAU_MUSIQUE_DB = -23.0  # volume moyen (RMS) visé pour la musique, avant le réglage final des crêtes
rng = np.random.default_rng(46)


def souffle_brut(n):
    """Bruit adouci (pente 1/f, coupé au-delà de 900 Hz) : un souffle feutré, pas un grésillement."""
    spectre = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    filtre = 1 / np.sqrt(np.maximum(f, 40.0)) / (1 + (f / 900.0) ** 4)
    filtre[f < 60] *= (f[f < 60] / 60.0) ** 2
    x = np.fft.irfft(spectre * filtre, n)
    return (x / np.max(np.abs(x))).astype(np.float32)


def clochette(freq, duree, niveau):
    """Clochette douce (partiels de bol chantant atténués, attaque de 10 ms, décroissance lente)."""
    t = np.arange(int(duree * SR)) / SR
    son = np.zeros_like(t)
    for rapport, poids, amort in ((1.0, 1.0, 1.6), (2.0, 0.18, 2.6), (2.76, 0.12, 3.2)):
        son += poids * np.sin(2 * np.pi * freq * rapport * t) * np.exp(-amort * t / duree * 2.2)
    attaque = np.minimum(1.0, t / 0.010)
    return (niveau * son * attaque / 1.30).astype(np.float32)


def enveloppe_cycle():
    """Montée douce sur 4 s (inspiration), descente plus lente sur 6 s (expiration)."""
    t = np.arange(int(CYCLE * SR)) / SR
    env = np.empty_like(t)
    i = t < INSPIRE
    env[i] = np.sin(np.pi / 2 * t[i] / INSPIRE) ** 2
    env[~i] = np.cos(np.pi / 2 * (t[~i] - INSPIRE) / EXPIRE) ** 2
    return (0.12 + 0.88 * env).astype(np.float32)


def musique(duree):
    """Extrait stéréo de la musique, au volume visé, avec fondu d'entrée (6 s) et fondu de sortie (fin)."""
    brut = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", MUSIQUE, "-t", f"{duree:.2f}", "-f", "f32le",
                           "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    m = np.frombuffer(brut, dtype="<f4").reshape(-1, 2).copy()
    n = int(duree * SR)
    if len(m) < n:
        m = np.vstack([m, np.zeros((n - len(m), 2), np.float32)])
    m = m[:n]
    rms = np.sqrt(np.mean(m[: SR * 120] ** 2))
    m *= np.float32(10 ** (NIVEAU_MUSIQUE_DB / 20) / rms)
    t = np.arange(n, dtype=np.float32) / SR
    fondu = np.clip(t / 6.0, 0, 1) * np.clip((duree - t) / (OUTRO - 2), 0, 1)
    m *= (np.sin(np.pi / 2 * fondu) ** 2)[:, None]
    return m


def reperes(cycles, n):
    """Clochettes et souffle (mono)."""
    x = np.zeros(n, np.float32)
    env = enveloppe_cycle()
    lc = len(env)
    for k in range(cycles):
        debut = int((INTRO + k * CYCLE) * SR)
        # Sur la piste longue (endormissement), les repères s'adoucissent dans le dernier tiers.
        douceur = 1.0 if k < cycles * 2 / 3 or cycles < 40 else 1.0 - 0.45 * (k - cycles * 2 / 3) / (cycles / 3)
        x[debut:debut + lc] += 0.05 * douceur * souffle_brut(lc) * env
        aigue = clochette(783.99, 3.2, 0.16 * douceur)   # sol : inspirer
        grave = clochette(523.25, 5.0, 0.15 * douceur)   # do : expirer
        x[debut:debut + len(aigue)] += aigue
        d2 = debut + int(INSPIRE * SR)
        x[d2:d2 + len(grave)] += grave
    fin = int((INTRO + cycles * CYCLE + 1.0) * SR)
    derniere = clochette(261.63, 7.0, 0.14)              # do grave : fin de l'exercice
    x[fin:fin + len(derniere)] += derniere[: n - fin]
    return x


def piste(cycles):
    duree = INTRO + cycles * CYCLE + OUTRO
    n = int(duree * SR)
    mix = musique(duree) + reperes(cycles, n)[:, None]
    t = np.arange(n, dtype=np.float32) / SR
    mix *= np.clip((duree - t) / 4.0, 0, 1)[:, None]      # fondu général des 4 dernières secondes
    mix = np.tanh(1.2 * mix) / np.tanh(1.2)               # léger limiteur
    return mix / np.max(np.abs(mix)) * 0.70                # crête vers -3 dB


def ecrire_mp3(x, chemin, minutes):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2").tobytes()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ac", "2", "-ar", str(SR), "-i", "-",
                    "-codec:a", "libmp3lame", "-b:a", "96k",
                    "-metadata", f"title=Respiration guidée 4-6 — {minutes} minutes",
                    "-metadata", "artist=Clarté Mentale",
                    "-metadata", f"comment={CREDIT}", chemin], input=pcm, check=True)


MUSIQUE_MINUTEUR = "musique-detente-minuteur.mp3"
DUREE_MINUTEUR = 330.0  # exercice le plus long du minuteur : 5 min arrondies à des cycles entiers (304 s), plus la fin


def musique_minuteur():
    """Musique seule pour le minuteur de /exercices-respiration/ : les clochettes sont jouées par la page (exercices.js).
    Même musique et même niveau que dans les audios guidés ; la page règle le volume des clochettes par rapport à elle
    (affiche le rapport à reporter dans exercices.js si on change le niveau)."""
    m = musique(DUREE_MINUTEUR)
    rms = float(np.sqrt(np.mean(m[: SR * 120] ** 2)))
    gain = 0.70 / float(np.max(np.abs(m)))                # crête vers -3 dB, comme les audios guidés
    m *= np.float32(gain)
    chemin = os.path.join(SORTIE, MUSIQUE_MINUTEUR)
    pcm = (np.clip(m, -1, 1) * 32767).astype("<i2").tobytes()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ac", "2", "-ar", str(SR), "-i", "-",
                    "-codec:a", "libmp3lame", "-b:a", "80k",
                    "-metadata", "title=Musique de détente pour les exercices de respiration",
                    "-metadata", "artist=Kevin MacLeod",
                    "-metadata", f"comment={CREDIT.replace('mixé avec des repères de respiration', 'mis en forme (fondus)')}",
                    chemin], input=pcm, check=True)
    print(chemin, f"{os.path.getsize(chemin) / 1e6:.1f} Mo",
          f"| clochette « sol » à {0.16 * gain:.3f} de crête (musique : {rms * gain:.4f} RMS)")


def main(seulement=None):
    os.makedirs(SORTIE, exist_ok=True)
    musique_minuteur()
    if seulement == "minuteur":
        return
    for minutes in (3, 5, 10):
        cycles = int(minutes * 60 / CYCLE)
        x = piste(cycles)
        chemin = os.path.join(SORTIE, f"respiration-4-6-{minutes}-min.mp3")
        ecrire_mp3(x, chemin, minutes)
        print(chemin, f"{len(x) / SR:.0f} s", f"{os.path.getsize(chemin) / 1e6:.1f} Mo")


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else None)
