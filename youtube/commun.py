"""Outils partagés du robot vidéo YouTube (consigne de l'utilisateur du 20/10/2026 : « je veux tout automatiser »).

Une vidéo = un dossier videos_youtube/<slug>/ avec plan.json (écrit par la tâche Claude hebdomadaire).
Les fichiers fabriqués (vidéo, Short, voix) restent dans travail/<slug>/, jamais commités ;
seuls miniature.jpg, sous-titres.srt, timeline.json et rapport.json sont commités dans le dossier du plan.
"""
import json, os, subprocess
import numpy as np

DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POLICES = os.path.join(DEPOT, "polices")
MUSIQUE = os.path.join(DEPOT, "site/sources-audio/deep-relaxation-extrait.mp3")
BOLS = os.path.join(DEPOT, "site/sources-audio/bols")
MODELES = os.path.join(DEPOT, "modeles")  # Kokoro et Whisper, téléchargés par le workflow (cache), jamais commités
SR = 48000
W, H, FPS = 1920, 1080, 24
SITE = "https://www.contactapaisement-mental.fr/"
CHAINE = "@ClarteMentaleFR"


def dossier_plan(slug):
    return os.path.join(DEPOT, "videos_youtube", slug)


def dossier_travail(slug):
    d = os.path.join(DEPOT, "travail", slug)
    os.makedirs(d, exist_ok=True)
    return d


def lire_plan(slug):
    return json.load(open(os.path.join(dossier_plan(slug), "plan.json"), encoding="utf-8"))


def ecrire_plan(slug, plan):
    with open(os.path.join(dossier_plan(slug), "plan.json"), "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
        f.write("\n")


def charger_audio(chemin, duree=None, canaux=2):
    cmd = ["ffmpeg", "-v", "error", "-i", chemin]
    if duree:
        cmd += ["-t", str(duree)]
    cmd += ["-f", "f32le", "-ac", str(canaux), "-ar", str(SR), "-"]
    a = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32)
    return a.reshape(-1, canaux).copy() if canaux > 1 else a.copy()


def lisse(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def fondu(t, d, f, e=1.2):
    return lisse((t - d) / e) * lisse((f - t) / e)


def mmss(s):
    return f"{int(s // 60):02d}:{int(s % 60):02d}"
