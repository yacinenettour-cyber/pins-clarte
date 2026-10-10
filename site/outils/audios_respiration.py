#!/usr/bin/env python3
"""Sons de respiration du site, sans voix.

1. Audios de respiration guidée 4-6 (inspirer 4 s, expirer 6 s : 6 respirations par minute), page /respiration-guidee/ :
   - une musique de détente : extrait de « Deep Relaxation », Kevin MacLeod (incompetech.com),
     licence Creative Commons Attribution 4.0 (crédit obligatoire et visible : voir CREDIT et la page
     /respiration-guidee/) — source dans site/sources-audio/ ;
   - de vrais bols chantants enregistrés (Freesound, licence CC0, voir site/sources-audio/bols/CREDITS.txt) :
     un bol frappé au maillet doux pour inspirer, un bol plus grave pour expirer, un bol à longue résonance à la fin.
2. Pour le minuteur de /exercices-respiration/ (exercices.js) :
   - les mêmes bols réunis dans un seul fichier (bols-minuteur.mp3), avec un petit bol de 8 cm pour « retiens »,
     et leur position dans bols-minuteur.json (lu par construire.py) ;
   - la musique seule (musique-detente-minuteur.mp3), au même niveau que dans les audios guidés.

Usage : python3 site/outils/audios_respiration.py            -> tout
        python3 site/outils/audios_respiration.py minuteur   -> seulement les deux fichiers du minuteur
"""
import json
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
BOLS = os.path.join(RACINE, "sources-audio", "bols")
CREDIT = ("Musique : Deep Relaxation, Kevin MacLeod (incompetech.com), licence Creative Commons Attribution 4.0 "
          "(https://creativecommons.org/licenses/by/4.0/) ; extrait mixé avec des repères de respiration par Clarté Mentale ; "
          "bols chantants : steffcaffrey, dersinnsspace, Truthiswithin, itinerantmonk108 (freesound.org, CC0)")
NIVEAU_MUSIQUE_DB = -23.0  # volume moyen (RMS) visé pour la musique, avant le réglage final des crêtes

# Repères : ([(fichier, accord en cents, volume relatif en dB), ...], durée gardée (s), volume du repère en dB).
# Timbres mesurés : inspirer 583 Hz (ré), expirer 276 + 779 Hz (sol), retenir 969 Hz (si), fin 428 + 1198 + 2222 Hz.
REPERES = {
    "inspire": ([("bol-maillet-doux_steffcaffrey_449951.ogg", 0, 0.0)], 9.0, 0.0),
    "expire": ([("bol-tibetain-centre_dersinnsspace_421829.ogg", 0, 0.0)], 12.0, 0.0),
    "retiens": ([("bol-tibetain-frappe_Truthiswithin_193022.ogg", 0, 0.0)], 6.0, -7.0),
    "fin": ([("bol-tibetain-long_itinerantmonk108_553049.ogg", 0, 0.0)], 18.0, 1.0),
}
# Volume de référence : celui de l'ancienne clochette « sol » de synthèse (crête 0,16), réglée à l'oreille avec la
# musique le 09/10, mesuré comme volume_percu() ; chaque repère est ramené à ce volume.
VOLUME_REFERENCE = 0.0551
PREROULE = 0.010  # le son commence 10 ms avant la frappe
ATTAQUE = 0.020   # montée de 20 ms : la frappe reste nette, sans le claquement du maillet


def volume_percu(x):
    """Volume moyen de la première seconde, graves sous 300 Hz atténués comme sur un haut-parleur de téléphone :
    un bol grave et un bol aigu au même chiffre s'entendent à peu près aussi fort sur un téléphone."""
    x = x[:SR] if x.ndim == 2 else x[:SR, None]
    f = np.fft.rfftfreq(len(x), 1 / SR)
    r = (f / 300) ** 2
    y = np.fft.irfft(np.fft.rfft(x, axis=0) * (r / np.sqrt(1 + r ** 2))[:, None], len(x), axis=0)
    return float(np.sqrt(np.mean(y ** 2)))  # moyenne des deux canaux


def frappe(fichier, cents, duree):
    """Un enregistrement (stéréo) coupé 10 ms avant la frappe, grondements sous 60 Hz filtrés, accordé."""
    sr_source = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=sample_rate",
                                    "-of", "csv=p=0", os.path.join(BOLS, fichier)], capture_output=True, text=True, check=True).stdout)
    rapport = 2 ** (cents / 1200)
    brut = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", os.path.join(BOLS, fichier),
                           "-af", f"highpass=f=60:poles=2,asetrate={sr_source * rapport:.3f},aresample={SR}",
                           "-f", "f32le", "-ac", "2", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(brut, dtype="<f4").reshape(-1, 2).copy()
    # Frappe principale : premier passage au-dessus de 30 % de la crête (un frôlement avant la frappe est ignoré),
    # puis retour en arrière jusqu'au début de la montée (sous 2 % de la crête, 150 ms au plus).
    mono = np.abs(x).mean(axis=1)
    lisse = np.convolve(mono, np.ones(int(0.002 * SR)) / int(0.002 * SR), mode="same")
    fort = int(np.argmax(lisse > 0.30 * lisse.max()))
    avant = lisse[max(0, fort - int(0.15 * SR)):fort]
    calmes = np.where(avant < 0.02 * lisse.max())[0]
    debut = fort - len(avant) + (int(calmes[-1]) if len(calmes) else 0)
    x = x[max(0, debut - int(PREROULE * SR)):][: int(duree * SR)]
    if len(x) < int(duree * SR):
        x = np.vstack([x, np.zeros((int(duree * SR) - len(x), 2), np.float32)])
    return x


def bol(nom):
    """Un repère prêt à l'emploi : enregistrement(s) mélangé(s), fondu de sortie progressif sur le dernier tiers,
    ramené au volume de référence."""
    couches, duree, db = REPERES[nom]
    # Chaque couche d'abord ramenée au même volume (sur téléphone), puis dosée en dB.
    x = sum(y * np.float32(10 ** (d / 20) / volume_percu(y)) for y, d in ((frappe(f, c, duree), d) for f, c, d in couches))
    n = len(x)
    t = np.arange(n) / SR
    x *= (np.sin(np.pi / 2 * np.minimum(1.0, t / ATTAQUE)) ** 2)[:, None]  # frappe adoucie (moins de « clac »)
    fondu = np.clip((n / SR - t) / (duree / 3), 0, 1)
    x *= (np.sin(np.pi / 2 * fondu) ** 2)[:, None]
    x *= np.float32(VOLUME_REFERENCE * 10 ** (db / 20) / volume_percu(x))
    return x.astype(np.float32)


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


def ajouter(x, son, debut, gain=1.0):
    d = int(debut * SR) - int(PREROULE * SR)
    fin = min(len(x), d + len(son))
    x[d:fin] += gain * son[: fin - d]


def reperes(cycles, n):
    """Bols de la piste guidée (stéréo) : inspiration, expiration, puis le grand bol de fin."""
    x = np.zeros((n, 2), np.float32)
    sons = {k: bol(k) for k in ("inspire", "expire", "fin")}
    for k in range(cycles):
        debut = INTRO + k * CYCLE
        # Sur la piste longue (endormissement), les repères s'adoucissent dans le dernier tiers.
        douceur = 1.0 if k < cycles * 2 / 3 or cycles < 40 else 1.0 - 0.45 * (k - cycles * 2 / 3) / (cycles / 3)
        ajouter(x, sons["inspire"], debut, douceur)
        ajouter(x, sons["expire"], debut + INSPIRE, douceur)
    ajouter(x, sons["fin"], INTRO + cycles * CYCLE + 1.0)
    return x


def piste(cycles):
    duree = INTRO + cycles * CYCLE + OUTRO
    n = int(duree * SR)
    mix = musique(duree) + reperes(cycles, n)
    t = np.arange(n, dtype=np.float32) / SR
    mix *= np.clip((duree - t) / 4.0, 0, 1)[:, None]      # fondu général des 4 dernières secondes
    mix = np.tanh(1.2 * mix) / np.tanh(1.2)               # léger limiteur
    return mix / np.max(np.abs(mix)) * 0.70                # crête vers -3 dB


def ecrire_mp3(x, chemin, debit, titre, artiste, commentaire):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2").tobytes()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ac", "2", "-ar", str(SR), "-i", "-",
                    "-codec:a", "libmp3lame", "-b:a", debit, "-metadata", f"title={titre}", "-metadata", f"artist={artiste}",
                    "-metadata", f"comment={commentaire}", chemin], input=pcm, check=True)


MUSIQUE_MINUTEUR = "musique-detente-minuteur.mp3"
BOLS_MINUTEUR = "bols-minuteur.mp3"
DUREE_MINUTEUR = 330.0  # exercice le plus long du minuteur : 5 min arrondies à des cycles entiers (304 s), plus la fin
BLANC = 0.25            # silence entre deux bols dans le fichier du minuteur


def minuteur():
    """Fichiers du minuteur de /exercices-respiration/ : musique seule et bols, au même équilibre que les audios guidés."""
    m = musique(DUREE_MINUTEUR)
    gain = 0.70 / float(np.max(np.abs(m)))                # crête vers -3 dB, comme les audios guidés
    ecrire_mp3(m * np.float32(gain), os.path.join(SORTIE, MUSIQUE_MINUTEUR), "112k",
               "Musique de détente pour les exercices de respiration", "Kevin MacLeod",
               CREDIT.split(" ; bols")[0].replace("mixé avec des repères de respiration", "mis en forme (fondus)"))
    # Bols bout à bout ; positions (début du son, 10 ms avant la frappe) et durées dans le JSON lu par la page.
    morceaux, positions, t = [np.zeros((int(BLANC * SR), 2), np.float32)], {}, BLANC
    for nom in ("inspire", "expire", "retiens", "fin"):
        son = bol(nom) * np.float32(gain)
        positions[nom] = [round(t, 4), round(len(son) / SR, 4)]
        morceaux += [son, np.zeros((int(BLANC * SR), 2), np.float32)]
        t += len(son) / SR + BLANC
    tout = np.vstack(morceaux)
    ecrire_mp3(tout, os.path.join(SORTIE, BOLS_MINUTEUR), "160k", "Bols chantants pour les exercices de respiration",
               "steffcaffrey, dersinnsspace, Truthiswithin, itinerantmonk108 (freesound.org, CC0)",
               "Bols chantants enregistrés, domaine public (CC0), préparés par Clarté Mentale")
    json.dump({"fichier": "/audio/" + BOLS_MINUTEUR, "preroule": PREROULE, "sons": positions},
              open(os.path.join(RACINE, "outils", "bols-minuteur.json"), "w"), indent=1)
    for f in (MUSIQUE_MINUTEUR, BOLS_MINUTEUR):
        print(os.path.join(SORTIE, f), f"{os.path.getsize(os.path.join(SORTIE, f)) / 1e6:.2f} Mo")
    print("crête des bols :", round(float(np.max(np.abs(tout))), 3), "| positions :", positions)


def main(seulement=None):
    os.makedirs(SORTIE, exist_ok=True)
    minuteur()
    if seulement == "minuteur":
        return
    for minutes in (3, 5, 10):
        cycles = int(minutes * 60 / CYCLE)
        x = piste(cycles)
        chemin = os.path.join(SORTIE, f"respiration-4-6-{minutes}-min.mp3")
        ecrire_mp3(x, chemin, "128k", f"Respiration guidée 4-6 — {minutes} minutes", "Clarté Mentale", CREDIT)
        print(chemin, f"{len(x) / SR:.0f} s", f"{os.path.getsize(chemin) / 1e6:.1f} Mo")


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else None)
