# Repère la tête du sujet principal de chaque photo de fonds/ et écrit fonds_cadrage.json,
# utilisé par pins.yml pour recadrer la photo sur le visage (30/09/2026 : têtes coupées).
# À relancer après tout ajout de photo dans fonds/ (sinon la nouvelle photo garde l'ancien
# recadrage « zone la plus nette »), puis vérifier le résultat à l'œil.
#
# Prérequis (une fois) : pip install mediapipe ; bibliothèque système libEGL (apt-get install libegl1) ;
# modèles dans le dossier MODELES (par défaut ./modeles) :
#   face.tflite : https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite
#   pose.task   : https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/latest/pose_landmarker_full.task
# Lancer depuis la racine du dépôt : python3 outils/cadrage_fonds.py
# Méthode : visage (score le plus élevé) recoupé avec la posture du corps ; en cas de désaccord, la posture l'emporte.
import os, json, mediapipe as mp, collections
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
M = os.environ.get("MODELES", "modeles") + "/"
fd = vision.FaceDetector.create_from_options(vision.FaceDetectorOptions(
    base_options=mpt.BaseOptions(model_asset_path=M + "face.tflite"), min_detection_confidence=0.5))
pl = vision.PoseLandmarker.create_from_options(vision.PoseLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=M + "pose.task"), num_poses=3, min_pose_detection_confidence=0.5))
res = {}
for f in sorted(os.listdir("fonds")):
    if not f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")): continue
    im = mp.Image.create_from_file("fonds/" + f)
    W, H = im.width, im.height
    visage = posture = None
    faces = [d for d in fd.detect(im).detections if d.categories[0].score >= 0.6]
    if faces:
        d = max(faces, key=lambda d: d.categories[0].score); b = d.bounding_box
        visage = {"tete": [max(0, (b.origin_y - 0.45 * b.height) / H), min(1, (b.origin_y + 1.05 * b.height) / H)],
                  "x": (b.origin_x + b.width / 2) / W, "score": d.categories[0].score}
    poses = pl.detect(im).pose_landmarks
    if poses:
        def taille(p): ys = [l.y for l in p]; return max(ys) - min(ys)
        p = max(poses, key=taille)
        pts = [p[i] for i in range(11) if p[i].visibility > 0.3] or [p[i] for i in range(11)]
        ys = [l.y for l in pts]; xs = [l.x for l in pts]
        larg = abs(p[7].x - p[8].x) * W / H
        h_tete = max(larg * 1.4, (max(ys) - min(ys)) * 2.2, 0.06)
        yc = sum(ys) / len(ys)
        posture = {"tete": [max(0, yc - 0.6 * h_tete), min(1, yc + 0.5 * h_tete)], "x": sum(xs) / len(xs)}
    choix = None
    if visage and posture:
        vc = sum(visage["tete"]) / 2
        d0, d1 = posture["tete"]
        choix = (visage, "visage") if d0 - 0.08 <= vc <= d1 + 0.08 else (posture, "posture")
    elif visage and visage["score"] >= 0.7:
        choix = (visage, "visage")
    elif posture:
        choix = (posture, "posture")
    res[f] = {"tete": [round(choix[0]["tete"][0], 3), round(choix[0]["tete"][1], 3)], "x": round(min(1, max(0, choix[0]["x"])), 3),
              "source": choix[1]} if choix else None
# Corrections vérifiées à l'œil le 30/09/2026 (planches de contrôle) : fausses détections
# (objets pris pour un visage ou une posture) et têtes manquées.
SANS_TETE = ["fond-14.jpg", "fond-15.jpg", "fond-20.jpg", "fond-25.jpg", "fond-45.jpg", "fond-51.jpg",
             "fond-69.jpg", "fond-163.jpg", "fond-189.jpg", "fond-196.jpg"]
AJOUTS = {"fond-145.jpg": {"tete": [0.04, 0.5], "x": 0.4}, "fond-195.jpg": {"tete": [0.42, 0.62], "x": 0.5},
          "fond-48.jpg": {"tete": [0.53, 0.78], "x": 0.45}}
for f in SANS_TETE:
    res[f] = None
for f, v in AJOUTS.items():
    res[f] = dict(v, source="manuel")
sortie = {f: v for f, v in sorted(res.items()) if v}
json.dump(sortie, open("fonds_cadrage.json", "w", encoding="utf-8"), indent=1)
print(collections.Counter(v["source"] if v else "aucune" for v in res.values()))
print("têtes repérées :", len(sortie), "/", len(res))
