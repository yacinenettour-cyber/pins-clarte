# Réenregistre une page systeme.io (via l'API) jusqu'à obtenir une palette bleu nuit + crème.
#
# Constat du 30/09/2026 : le constructeur de pages de systeme.io ignore « palettePreset » et tire
# les couleurs au hasard à chaque enregistrement (même réglage : bleu roi, puis violet, puis orange).
# Les couleurs réellement appliquées se lisent dans le HTML de la page (__PRELOADED_STATE__).
# Chaque essai peut créer 2-3 images IA dans la médiathèque (réutilisées si le contenu ne change pas).
#
# Usage (clé API dans la variable SIO_KEY, jamais dans le dépôt) :
#   SIO_KEY=... python3 outils/couleurs_systemeio.py <pageId> <contenu.json> <url publique> [essais max]
# <contenu.json> = contenu aiContentSchema (ex. docs/systeme-io/pages/page-vente-v2.json).
import json, os, re, subprocess, sys, time, colorsys, random

K = os.environ["SIO_KEY"]
page_id, fichier, url = sys.argv[1], sys.argv[2], sys.argv[3]
maxi = int(sys.argv[4]) if len(sys.argv) > 4 else 10
open("b.json", "w").write(json.dumps({"aiContentSchema": json.load(open(fichier))}, ensure_ascii=False))


def hsl(hexa):
    r, g, b = (int(hexa[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s, l


def palette():
    html = subprocess.run(["curl", "-s", f"{url}?v={random.randint(1, 10**9)}"], capture_output=True, text=True).stdout
    m = re.search(r"window\.__PRELOADED_STATE__=(\{.*?\})</script>", html, re.S)
    s = m.group(1) if m else ""
    return sorted(set(c.upper() for c in re.findall(r'"(?:background(?:Color)?|textColor|color|buttonColor)":"(#[0-9a-fA-F]{6})"', s)))


def verdict(cols):
    hs = [(c,) + hsl(c) for c in cols]
    navy = any(195 <= h <= 245 and l <= 0.37 and s >= 0.2 for c, h, s, l in hs)
    fonds = [x for x in hs if x[3] >= 0.85]
    fonds_ok = bool(fonds) and all(s < 0.15 or 20 <= h <= 60 for c, h, s, l in fonds)
    creme = any(20 <= h <= 60 and l >= 0.88 for c, h, s, l in fonds) or any(s < 0.15 and l >= 0.93 for c, h, s, l in fonds)
    vives = [c for c, h, s, l in hs if s >= 0.35 and 0.2 < l < 0.85 and not (195 <= h <= 245 or 28 <= h <= 55)]
    strict = navy and fonds_ok and creme and not vives
    bleus = [c for c, h, s, l in hs if s >= 0.3 and 0.15 < l < 0.85]
    fonds_bleus_ok = bool(fonds) and all(s < 0.2 or l >= 0.96 or 20 <= h <= 60 or 195 <= h <= 235 for c, h, s, l in fonds)
    proche = navy and not vives and fonds_bleus_ok and all(195 <= hsl(c)[0] <= 245 or 28 <= hsl(c)[0] <= 55 for c in bleus)
    return strict, proche


for essai in range(1, maxi + 1):
    code = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "60", "-X", "PUT",
                           "-H", "X-API-Key: " + K, "-H", "Content-Type: application/json", "-H", "Accept: application/json",
                           "--data", "@b.json", f"https://api.systeme.io/api/page-editor/pages/{page_id}/save"],
                          capture_output=True, text=True).stdout
    time.sleep(2)
    cols = palette()
    strict, proche = verdict(cols)
    print(f"essai {essai} HTTP {code} | {' '.join(cols)} | strict={strict} proche={proche}", flush=True)
    if strict or proche:
        print("RETENU", "strict" if strict else "proche")
        break
else:
    print("AUCUN ESSAI RETENU (la dernière palette reste en place)")
