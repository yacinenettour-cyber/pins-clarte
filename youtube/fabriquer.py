"""Fabrique une vidéo de bout en bout et la contrôle. Rien n'est publié si un contrôle échoue.
Usage : python3 youtube/fabriquer.py <slug>"""
import difflib, json, os, re, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import SITE, CHAINE, MODELES, SR, dossier_plan, dossier_travail, lire_plan, ecrire_plan
import audio, rendu, extras

# Règles de contenu (CLAUDE.md : sujet santé, aucune promesse, auteur non professionnel de santé)
INTERDITS = ["guérir", "guérison", "guérit", "garanti", "miracle", "remède", "traitement", "médicament", "soigner",
             "100 %", "à coup sûr", "en quelques secondes", "thérapeute", "psychologue que je"]


def controler_texte(plan):
    erreurs = []
    dits = " ".join(e[1] for e in plan["script"] if e[0] == "dire").lower()
    desc = description(plan, None).lower()
    for mot in INTERDITS:
        if mot in dits or mot in plan["youtube"]["titre"].lower():
            erreurs.append(f"mot interdit : « {mot} »")
    if "conduisant" not in dits:
        erreurs.append("le rappel « jamais en conduisant » manque dans la voix")
    if "je ne suis pas professionnel de santé" not in desc:
        erreurs.append("la mention « Je ne suis pas professionnel de santé » manque dans la description")
    if "contactapaisement-mental.fr" not in desc:
        erreurs.append("le lien du site manque dans la description")
    if len(plan["youtube"]["titre"]) > 100:
        erreurs.append("titre YouTube de plus de 100 caractères")
    if len(desc.encode()) > 4900:
        erreurs.append("description trop longue (5000 octets maximum)")
    return erreurs


def description(plan, tl):
    y = plan["youtube"]
    morceaux = [y["description"].strip()]
    if tl:
        from extras import chapitres
        morceaux.append("\n".join(chapitres(tl)))
    morceaux.append(y.get("rappel", "À écouter allongé, au calme, jamais en conduisant. Cette vidéo ne remplace pas un avis médical : "
                                    "si tes difficultés de sommeil durent ou pèsent sur tes journées, parles-en à ton médecin. "
                                    "Je ne suis pas professionnel de santé."))
    if y.get("sources"):
        morceaux.append("Sources :\n" + "\n".join("· " + s for s in y["sources"]))
    photographes = ", ".join(dict.fromkeys(p["photographe"] for p in plan["photos"] if p.get("photographe")))
    morceaux.append("Voix : voix de synthèse (Kokoro, licence Apache 2.0 ; voix « ff_siwis » issue du corpus SIWIS, CC BY 4.0).\n"
                    "Musique : « Deep Relaxation », Kevin MacLeod (incompetech.com), licence Creative Commons Attribution 4.0 "
                    "http://creativecommons.org/licenses/by/4.0/\n"
                    f"Photos : Unsplash ({photographes}). Bols chantants : Freesound, domaine public (CC0).")
    morceaux.append(" ".join(y.get("hashtags", ["#méditation", "#sommeil", "#méditationguidée"])))
    return "\n\n".join(morceaux)


def controler_voix(slug, tl):
    """Transcrit chaque phrase (Whisper small, gratuit, local) et la compare au texte prévu."""
    import sherpa_onnx, soundfile as sf
    import scipy.signal as ss
    d = os.path.join(MODELES, "sherpa-onnx-whisper-small")
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{d}/small-encoder.int8.onnx", decoder=f"{d}/small-decoder.int8.onnx",
                                                    tokens=f"{d}/small-tokens.txt", language="fr", task="transcribe",
                                                    num_threads=os.cpu_count() or 2)
    v, sr = sf.read(os.path.join(dossier_travail(slug), "voix.wav"), dtype="float32")
    # comparaison lettre à lettre, homophones neutralisés (Whisper confond « tes » et « des », « pied » et « pieds »)
    def norm(s):
        mots = re.sub(r"[^a-zàâçéèêëîïôûùüœ ]", "", s.lower().replace("’", "'").replace("'", " ")).split()
        return "".join({"tes": "des", "ta": "da", "ton": "don"}.get(m, m).rstrip("sx") for m in mots)
    scores, faibles = [], []
    for c in tl["cues"]:
        if c["texte"] in ("Inspire…", "Expire…"):
            continue
        seg = v[int((c["debut"] - 0.2) * sr): int((c["fin"] + 0.4) * sr)]
        seg = ss.resample_poly(seg, 1, 3).astype(np.float32)
        s = rec.create_stream()
        s.accept_waveform(16000, seg)
        rec.decode_stream(s)
        q = difflib.SequenceMatcher(None, norm(c["texte"]), norm(s.result.text)).ratio()
        scores.append(q)
        if q < 0.6:
            faibles.append({"texte": c["texte"], "entendu": s.result.text, "score": round(q, 2)})
    return float(np.mean(scores)), faibles


def duree(chemin):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", chemin],
                                capture_output=True, text=True, check=True).stdout)


def fabriquer(slug):
    plan = lire_plan(slug)
    rapport = {"slug": slug, "erreurs": []}
    err = controler_texte(plan)
    if err:
        rapport["erreurs"] += err
        return rapport
    extras.telecharger_photos(slug)
    tl = audio.fabriquer(slug)
    moy, faibles = controler_voix(slug, tl)
    rapport.update(voix_score=round(moy, 3), phrases_douteuses=faibles)
    if moy < 0.85 or len(faibles) > 2:
        rapport["erreurs"].append(f"voix peu compréhensible (score {moy:.2f}, {len(faibles)} phrases douteuses)")
        return rapport
    video = rendu.fabriquer(slug)
    sh = extras.short(slug)
    extras.miniature(slug)
    extras.sous_titres(slug)
    d = duree(video)
    rapport.update(duree_video=round(d, 1), duree_short=round(duree(sh), 1) if sh else None,
                   chapitres=extras.chapitres(tl), description=description(plan, tl))
    if abs(d - tl["duree"]) > 1.0:
        rapport["erreurs"].append(f"durée vidéo {d:.1f} s au lieu de {tl['duree']:.1f} s")
    # contrôle visuel automatique : aucune image noire pendant la voix
    trav = dossier_travail(slug)
    for t in np.linspace(5, tl["fin_voix"] - 5, 8):
        img = os.path.join(trav, "_controle.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.1f}", "-i", video, "-frames:v", "1", "-vf", "scale=192:108", img], check=True)
        from PIL import Image
        if np.asarray(Image.open(img).convert("L")).mean() < 8:
            rapport["erreurs"].append(f"image presque noire à {t:.0f} s")
    json.dump({k: v for k, v in json.load(open(os.path.join(trav, "timeline.json"))).items()},
              open(os.path.join(dossier_plan(slug), "timeline.json"), "w"), ensure_ascii=False, indent=1)
    return rapport


if __name__ == "__main__":
    slug = sys.argv[1]
    r = fabriquer(slug)
    json.dump(r, open(os.path.join(dossier_plan(slug), "rapport.json"), "w"), ensure_ascii=False, indent=1)
    plan = lire_plan(slug)
    plan["statut"] = "erreur_fabrication" if r["erreurs"] else "fabriquee"
    ecrire_plan(slug, plan)
    print(json.dumps(r, ensure_ascii=False, indent=1)[:3000])
    sys.exit(1 if r["erreurs"] else 0)
