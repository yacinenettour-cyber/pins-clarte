"""Fabrique une vidéo de bout en bout et la contrôle. Rien n'est publié si un contrôle échoue.
Usage : python3 youtube/fabriquer.py <slug>"""
import difflib, json, os, re, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import normaliser, reconnaissance, transcrire, SITE, CHAINE, MODELES, SR, dossier_plan, dossier_travail, lire_plan, ecrire_plan, mots_normalises
import audio, rendu, extras
from metadonnees import description

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
    if len(desc.encode()) > 4600:  # les chapitres (~300 octets) s'ajoutent ensuite ; YouTube refuse au-delà de 5000
        erreurs.append("description trop longue (5000 octets maximum)")
    return erreurs


def controler_voix(slug, tl):
    """Transcrit chaque phrase (Whisper small, gratuit, local) et la compare au texte prévu. Depuis le 27/10/2026, une
    phrase où Whisper entend nettement plus que le texte (sons ou mots inventés par la voix) compte aussi comme douteuse."""
    import soundfile as sf
    rec = reconnaissance()
    v, sr = sf.read(os.path.join(dossier_travail(slug), "voix.wav"), dtype="float32")
    MOTS.clear(); HORS.clear(); TOTAL[0] = 0
    if v.ndim > 1:
        v = v.mean(axis=1)
    scores, faibles = [], []
    for c in tl["cues"]:
        if c["texte"] in ("Inspire…", "Expire…"):
            continue
        seg = v[max(0, int((c["debut"] - 0.2) * sr)): int((c["fin"] + 0.4) * sr)]
        if len(seg) < sr // 4:
            continue
        entendu = transcrire(rec, seg)
        prevu, ent = normaliser(c["texte"]), normaliser(entendu)
        q = difflib.SequenceMatcher(None, prevu, ent).ratio()
        scores.append(q)
        if q < 0.6 or len(ent) > 1.2 * len(prevu) + 3:
            faibles.append({"texte": c["texte"], "entendu": entendu, "score": round(q, 2)})
        # mot par mot (27/10/2026, demande de l'utilisateur) : chaque mot prévu doit être entendu tel quel
        mp, me = mots_normalises(c["texte"]), mots_normalises(entendu)
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, mp, me).get_opcodes():
            if op != "equal":
                MOTS.append({"debut": round(c["debut"], 1), "phrase": c["texte"], "prevu": " ".join(mp[i1:i2]),
                             "entendu": " ".join(me[j1:j2])})
        TOTAL[0] += len(mp)
    # silences entre les phrases, sur la piste de voix seule : aucune parole ne doit s'y trouver
    cues = [c for c in tl["cues"]]
    for c1, c2 in zip(cues, cues[1:]):
        a, b = c1["fin"] + 0.5, c2["debut"] - 0.3
        if b - a < 1.0:
            continue
        seg = v[int(a * sr): int(b * sr)]
        if len(seg) < sr // 2 or float(np.sqrt(np.mean(seg ** 2))) < 0.003:
            continue  # vrai silence
        entendu = transcrire(rec, seg)
        if len(mots_normalises(entendu)) >= 2:
            HORS.append({"de": round(a, 1), "a": round(b, 1), "entendu": entendu})
    return float(np.mean(scores)), faibles


MOTS, HORS, TOTAL = [], [], [0]


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
    if tl.get("voix_douteuses"):
        rapport["erreurs"].append(f"{len(tl['voix_douteuses'])} phrase(s) encore douteuse(s) après plusieurs essais de la voix")
        rapport["voix_douteuses"] = tl["voix_douteuses"]
        return rapport
    moy, faibles = controler_voix(slug, tl)
    faux = sum(len(m["prevu"].split()) for m in MOTS)
    rapport.update(voix_score=round(moy, 3), phrases_douteuses=faibles, mots_ecarts=MOTS, paroles_hors_sous_titres=HORS,
                   bilan_mots=f"{TOTAL[0] - faux}/{TOTAL[0]} mots entendus exactement")
    if HORS:
        rapport["erreurs"].append(f"{len(HORS)} passage(s) où la voix parle hors des sous-titres")
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
