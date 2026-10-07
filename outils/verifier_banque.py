"""Vérifie pins.json et videos.json avant de pousser une recharge : aucun doublon autorisé.

Usage : python3 outils/verifier_banque.py
Compare chaque pin/vidéo non publié(e) (y compris pins_saisonniers.json) à tout ce qui existe
(historique, pins en ligne, kits, vidéos) ET aux autres entrées non publiées de la banque, avec les mêmes règles que le
pipeline (outils/anti_doublons.py). Code de sortie 1 s'il reste un doublon.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import anti_doublons as A

pub = {h["titre"] for h in json.load(open("historique.json", encoding="utf-8"))}
pub_v = {h.get("titre") for h in json.load(open("historique_videos.json", encoding="utf-8"))}
a_venir = [(p["titre"], "pin") for p in json.load(open("pins.json", encoding="utf-8")) if p["titre"] not in pub]
a_venir += [(v["titre"], "vidéo") for v in json.load(open("videos.json", encoding="utf-8")) if v["titre"] not in pub_v]
# Pins saisonniers mis de côté (à insérer plus tard dans pins.json) : comptés aussi, pour qu'une
# recharge n'en reprenne pas le sujet entre-temps.
if os.path.exists("pins_saisonniers.json"):
    a_venir += [(p["titre"], "pin saisonnier") for p in json.load(open("pins_saisonniers.json", encoding="utf-8"))["pins"]
                if p["titre"] not in pub]

references = A.charger_references()
problemes = 0
deja_vus = []
for titre, nature in a_venir:
    doublon, raison = A.est_doublon(titre, references + deja_vus)
    if doublon:
        problemes += 1
        print(f"DOUBLON ({nature}) : {titre}\n    → {raison}")
    deja_vus.append((titre, f"{nature} non publié(e) de la banque", A.normaliser(titre), A.mots_cles(titre)))

print(f"\n{len(a_venir)} titres à venir vérifiés : {problemes} doublon(s).")
print("Rappel : ce contrôle automatique ne voit que les titres. Relire aussi les sujets à la main.")
sys.exit(1 if problemes else 0)
