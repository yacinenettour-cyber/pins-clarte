"""Télécharge les photos libres de droits listées dans photos_a_importer.json vers photos_attente/.

Lancé par .github/workflows/photos.yml (le conteneur des sessions Claude n'atteint pas les banques
d'images). photos_attente/ est une zone d'attente : le pipeline n'y pioche jamais. Chaque photo y
est regardée à la main ; celles qui ne sont pas hors sujet passent dans fonds/ (classées dans
fonds_themes.json, cadrées avec outils/cadrage_fonds.py), les autres sont supprimées. Le registre
photos_sources.json garde pour chaque photo sa source, sa licence et son statut (« à trier »,
« gardée », « refusée »), pour ne jamais la retélécharger.
"""
import io, json, os, sys, time

import requests
from PIL import Image

LISTE = "photos_a_importer.json"
DOSSIER = "photos_attente"
REGISTRE = "photos_sources.json"
LARGEUR_MAX = 1400
ENTETES = {"User-Agent": "Mozilla/5.0 (compatible; pins-clarte/1.0)"}


def main():
    liste = json.load(open(LISTE, encoding="utf-8"))["photos"]
    registre = json.load(open(REGISTRE, encoding="utf-8")) if os.path.exists(REGISTRE) else {}
    os.makedirs(DOSSIER, exist_ok=True)
    ok = echecs = 0
    for p in liste:
        nom = p["nom"]
        if nom in registre or os.path.exists(os.path.join("fonds", nom)):
            continue
        try:
            # Referer : certaines banques (Pixabay) refusent le téléchargement direct sans lui.
            r = requests.get(p["url"], headers=dict(ENTETES, Referer=p["page"]) if p.get("page") else ENTETES, timeout=60)
            r.raise_for_status()
            img = Image.open(io.BytesIO(r.content)).convert("RGB")
        except Exception as e:
            print("Échec :", nom, "→", str(e)[:200])
            registre[nom] = {k: p[k] for k in ("theme", "source", "url") if k in p}
            registre[nom]["statut"] = "échec du téléchargement"
            echecs += 1
            continue
        if img.width > LARGEUR_MAX:
            img = img.resize((LARGEUR_MAX, round(img.height * LARGEUR_MAX / img.width)), Image.LANCZOS)
        img.save(os.path.join(DOSSIER, nom), "JPEG", quality=88, optimize=True)
        registre[nom] = {k: p[k] for k in ("theme", "description", "source", "page", "photographe", "licence", "url") if k in p}
        registre[nom].update({"largeur": img.width, "hauteur": img.height, "statut": "à trier"})
        ok += 1
        time.sleep(0.3)
    json.dump(registre, open(REGISTRE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{ok} photo(s) téléchargée(s) dans {DOSSIER}/, {echecs} échec(s) (notés dans {REGISTRE}, pas retentés).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
