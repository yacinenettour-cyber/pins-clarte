"""Mise en ligne YouTube par l'API Composio (même clé que Pinterest, secret COMPOSIO_API_KEY).
- `envoyer <slug>` : vidéo et Short en « non répertorié », miniature, sous-titres, playlist.
- `rendre_publiques` : passe en public les vidéos dont l'heure prévue est passée, sauf si le plan dit "bloquee": true.
Phase de rodage (proposée à l'utilisateur le 20/10/2026) : non répertorié d'abord, public le soir prévu."""
import datetime, hashlib, json, mimetypes, os, sys, time
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import dossier_plan, dossier_travail, lire_plan, ecrire_plan, DEPOT
import metadonnees

API = "https://backend.composio.dev/api"
CLE = os.environ.get("COMPOSIO_API_KEY", "")
# même utilisateur Composio que la publication Pinterest (projet « Aire de jeux »)
UTILISATEUR = os.environ.get("COMPOSIO_UTILISATEUR", "pg-test-a2a2217a-e3a1-439a-aabd-cc16b6182094")


def entetes():
    return {"x-api-key": CLE, "Content-Type": "application/json"}


def fichier(chemin, outil):
    """Envoie un fichier dans le stockage Composio (même protocole que le SDK officiel) et renvoie sa référence."""
    nom = os.path.basename(chemin)
    mime = {".srt": "application/octet-stream"}.get(os.path.splitext(nom)[1], mimetypes.guess_type(nom)[0] or "application/octet-stream")
    md5 = hashlib.md5(open(chemin, "rb").read()).hexdigest()
    r = requests.post(f"{API}/v3/files/upload/request", headers=entetes(), timeout=60,
                      json={"md5": md5, "filename": nom, "mimetype": mime, "tool_slug": outil, "toolkit_slug": "youtube"})
    r.raise_for_status()
    rep = r.json()
    with open(chemin, "rb") as f:
        p = requests.put(rep["new_presigned_url"], data=f, headers={"Content-Type": mime}, timeout=1800)
    if p.status_code != 200:
        raise RuntimeError(f"envoi du fichier refusé ({p.status_code})")
    return {"name": nom, "mimetype": mime, "s3key": rep["key"]}


def executer(outil, arguments):
    r = requests.post(f"{API}/v3.1/tools/execute/{outil}", headers=entetes(), timeout=1800,
                      json={"arguments": arguments, "entity_id": UTILISATEUR})
    print(outil, r.status_code, r.text[:600])
    r.raise_for_status()
    rep = r.json()
    if rep.get("successful") is False or rep.get("error"):
        raise RuntimeError(f"{outil} : {rep.get('error')}")
    return rep.get("data") or {}


def id_video(data):
    for cle in ("id", "videoId", "video_id"):
        if isinstance(data.get(cle), str):
            return data[cle]
    for v in data.values():
        if isinstance(v, dict):
            x = id_video(v)
            if x:
                return x
    return None


def url_publique(chemin_depot):
    """Adresse publique d'un fichier du dépôt (dépôt public, servi par jsDelivr comme pour les carrousels Pinterest)."""
    sha = os.popen(f"git -C {DEPOT} rev-parse HEAD").read().strip()
    return f"https://cdn.jsdelivr.net/gh/{os.environ.get('GITHUB_REPOSITORY', 'yacinenettour-cyber/pins-clarte')}@{sha}/{chemin_depot}"


def envoyer(slug):
    plan, trav = lire_plan(slug), dossier_travail(slug)
    y = plan["youtube"]
    data = executer("YOUTUBE_UPLOAD_VIDEO", {
        "title": y["titre"], "description": metadonnees.description(plan, metadonnees.timeline(slug)), "tags": y["tags"],
        "categoryId": y.get("categorie", "26"), "privacyStatus": "unlisted",
        "videoFilePath": fichier(os.path.join(trav, "video.mp4"), "YOUTUBE_UPLOAD_VIDEO")})
    vid = id_video(data)
    if not vid:
        raise RuntimeError("identifiant de la vidéo introuvable dans la réponse")
    pub = {"video_id": vid, "video_url": f"https://youtu.be/{vid}", "etat": "non_repertoriee",
           "envoyee_le": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="minutes")}
    plan["publication"] = pub
    plan["statut"] = "en_ligne_non_repertoriee"
    ecrire_plan(slug, plan)
    # le reste ne doit pas faire échouer la mise en ligne : chaque étape est notée
    try:
        executer("YOUTUBE_UPDATE_THUMBNAIL", {"videoId": vid, "thumbnailUrl": url_publique(f"videos_youtube/{slug}/miniature.jpg")})
        pub["miniature"] = "ok"
    except Exception as e:
        pub["miniature"] = f"échec : {e}"[:300]
    try:
        executer("YOUTUBE_UPLOAD_CAPTION_TRACK", {"videoId": vid, "language": "fr", "name": "Français",
                                                  "file": fichier(os.path.join(dossier_plan(slug), "sous-titres.srt"),
                                                                  "YOUTUBE_UPLOAD_CAPTION_TRACK")})
        pub["sous_titres"] = "ok"
    except Exception as e:
        pub["sous_titres"] = f"échec : {e}"[:300]
    if y.get("playlist_id"):
        try:
            executer("YOUTUBE_ADD_VIDEO_TO_PLAYLIST", {"playlistId": y["playlist_id"], "videoId": vid})
            pub["playlist"] = "ok"
        except Exception as e:
            pub["playlist"] = f"échec : {e}"[:300]
    sh = plan.get("short", {})
    if os.path.exists(os.path.join(trav, "short.mp4")):
        try:
            d = executer("YOUTUBE_UPLOAD_VIDEO", {
                "title": sh.get("titre", "Respire avec moi pour t'endormir #sommeil #respiration")[:100],
                "description": sh.get("description", "") + f"\n\nLa méditation complète : https://youtu.be/{vid}\n"
                               "Plus d'exercices gratuits : https://www.contactapaisement-mental.fr/",
                "tags": y["tags"][:8], "categoryId": y.get("categorie", "26"), "privacyStatus": "unlisted",
                "videoFilePath": fichier(os.path.join(trav, "short.mp4"), "YOUTUBE_UPLOAD_VIDEO")})
            pub["short_id"] = id_video(d)
        except Exception as e:
            pub["short"] = f"échec : {e}"[:300]
    plan["publication"] = pub
    ecrire_plan(slug, plan)
    print(json.dumps(pub, ensure_ascii=False, indent=1))


def actualiser(slug):
    """Réapplique titre, description et mots-clés du plan à la vidéo déjà en ligne (sans la refabriquer)."""
    plan = lire_plan(slug)
    y, pub = plan["youtube"], plan.get("publication") or {}
    executer("YOUTUBE_UPDATE_VIDEO", {"video_id": pub["video_id"], "title": y["titre"], "tags": y["tags"],
                                      "category_id": y.get("categorie", "26"),
                                      "description": metadonnees.description(plan, metadonnees.timeline(slug))})
    pub["metadonnees"] = "à jour " + datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="minutes")
    plan["publication"] = pub
    ecrire_plan(slug, plan)


def connexion_youtube():
    """Vrai si un compte YouTube actif est connecté pour l'utilisateur Composio du robot."""
    global UTILISATEUR
    r = requests.get(f"{API}/v3/connected_accounts", headers=entetes(), timeout=60,
                     params={"toolkit_slugs": "youtube", "statuses": "ACTIVE"})
    print("connexion YouTube :", r.status_code)
    items = r.json().get("items", []) if r.ok else []
    if not items:
        return False
    # l'identifiant d'utilisateur Composio est relu à chaque fois (une reconnexion ne casse rien, cf. Pinterest)
    UTILISATEUR = items[0].get("user_id") or UTILISATEUR
    return True


def rendre_publiques():
    maintenant = datetime.datetime.now(datetime.timezone.utc)
    racine = os.path.join(DEPOT, "videos_youtube")
    for slug in sorted(os.listdir(racine)):
        if not os.path.exists(os.path.join(racine, slug, "plan.json")):
            continue
        plan = lire_plan(slug)
        pub = plan.get("publication") or {}
        if plan.get("statut") != "en_ligne_non_repertoriee" or plan.get("bloquee"):
            continue
        prevue = datetime.datetime.fromisoformat(plan["publication_prevue"].replace("Z", "+00:00"))
        if maintenant < prevue:
            continue
        try:  # dernières retouches du plan (description, mots-clés) appliquées avant le passage en public
            actualiser(slug)
            plan = lire_plan(slug)
            pub = plan.get("publication") or {}
        except Exception as e:
            print("métadonnées non actualisées :", e)
        for cle in ("video_id", "short_id"):
            if pub.get(cle):
                executer("YOUTUBE_UPDATE_VIDEO", {"video_id": pub[cle], "privacy_status": "public"})
        pub["etat"] = "publique"
        pub["publiee_le"] = maintenant.isoformat(timespec="minutes")
        plan["publication"] = pub
        plan["statut"] = "publiee"
        ecrire_plan(slug, plan)
        print("publiée :", slug, pub.get("video_url"))


if __name__ == "__main__":
    if not CLE:
        sys.exit("COMPOSIO_API_KEY manquant")
    if sys.argv[1] == "connexion":
        sys.exit(0 if connexion_youtube() else 1)
    if not connexion_youtube():
        print("aucun compte YouTube actif connecté dans Composio")
        sys.exit(0 if sys.argv[1] == "rendre_publiques" else 1)
    if sys.argv[1] == "envoyer":
        envoyer(sys.argv[2])
    elif sys.argv[1] == "actualiser":
        actualiser(sys.argv[2])
    else:
        rendre_publiques()
