"""Photos jamais réutilisées (08/10/2026, consigne de l'utilisateur : aucun doublon d'image).

Une photo de fonds/ (ou de videos_fonds/) déjà publiée dans un pin, un carrousel ou une vidéo
n'est plus jamais reprise, même avec un autre texte. Appelé par pins.yml et videos.yml.

Photos considérées comme déjà publiées :
- historique.json : champ "fond" (et "photos" s'il existe) ;
- historique_videos.json : champ "photos", ou à défaut les scènes de la vidéo dans videos.json ;
- photos_utilisees_hors_historique.json : photos publiées dont l'historique ne garde pas la
  trace (ex. diapositives des carrousels du 29/09/2026, dont seule la 1re est notée).
Seules les photos classées sous le thème exact dans fonds_themes.json sont proposées ("dedie" et
les autres étiquettes ne sortent jamais par la rotation).
"""
import json, os

from PIL import Image

EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")
_largeurs = {}


def cle(chemin):
    """Forme unique d'un chemin de photo : « fonds/fond-16.jpg »."""
    return os.path.normpath(str(chemin)).replace(os.sep, "/")


def _json(chemin, defaut):
    if not os.path.exists(chemin):
        return defaut
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def photos_utilisees():
    vues = set()
    for h in _json("historique.json", []):
        fond = str(h.get("fond") or "")
        if fond.startswith(("fonds/", "videos_fonds/")):
            vues.add(cle(fond))
        for p in h.get("photos") or []:
            vues.add(cle(p))
    videos = {v["id"]: v for v in _json("videos.json", [])}
    for h in _json("historique_videos.json", []):
        photos = h.get("photos")
        if photos is None and h.get("id") in videos:
            photos = [b["image"] for b in videos[h["id"]]["beats"]]
        for p in photos or []:
            vues.add(cle(p))
    for p in _json("photos_utilisees_hors_historique.json", {}).get("photos", []):
        vues.add(cle(p))
    return vues


def largeur(chemin):
    if chemin not in _largeurs:
        _largeurs[chemin] = Image.open(chemin).width
    return _largeurs[chemin]


def photos_du_theme(theme):
    themes = _json("fonds_themes.json", {})
    if not os.path.isdir("fonds"):
        return []
    return sorted("fonds/" + f for f in os.listdir("fonds")
                  if f.lower().endswith(EXTENSIONS) and themes.get(f) == theme)


def choisir_photo(theme, exclues, min_largeur=0, aussi_exclues=()):
    """Première photo du thème jamais publiée (et assez large si demandé), sinon None."""
    for p in photos_du_theme(theme):
        if p in exclues or p in aussi_exclues:
            continue
        if min_largeur and largeur(p) < min_largeur:
            continue
        return p
    return None


def photo_dediee(pin, exclues, min_largeur=0):
    """Photo dédiée du pin (champ "photo"), si elle existe et n'a jamais été publiée."""
    if not pin.get("photo"):
        return None
    p = cle(os.path.join("fonds", pin["photo"]))
    if p in exclues or not os.path.exists(p):
        return None
    if min_largeur and largeur(p) < min_largeur:
        return None
    return p


def photos_pour_video(video, exclues, max_photos=3):
    """Photos des scènes d'une vidéo, toutes jamais publiées, ou None s'il en manque.

    Garde d'abord les photos prévues encore inédites, complète avec des photos inédites du
    thème, au plus max_photos par vidéo (économie de photos) ; chaque photo couvre un bloc de
    scènes consécutives. Il en faut au moins 2 (1 si la vidéo n'a qu'une scène).
    """
    libres = []
    for b in video["beats"]:
        p = cle(b["image"])
        if p not in exclues and p not in libres and os.path.exists(p):
            libres.append(p)
    for p in photos_du_theme(video["theme"]):
        if len(libres) >= max_photos:
            break
        if p not in exclues and p not in libres:
            libres.append(p)
    libres = libres[:max_photos]
    n = len(video["beats"])
    if not n or len(libres) < min(2, n):
        return None
    k = min(len(libres), n)
    return [libres[i * k // n] for i in range(n)]
