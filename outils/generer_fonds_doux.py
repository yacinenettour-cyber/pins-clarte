"""Génère des fonds dégradés doux et soignés par thème (usage image_prete et fallback)."""
import json, os
from PIL import Image, ImageDraw, ImageFilter

OUT = "fonds"
os.makedirs(OUT, exist_ok=True)

# Palette par thème (couleur d'accent -> déclinaison pour un dégradé doux élégant)
ACCENTS = {
    "sommeil":            (72, 88, 158),
    "systemenerveux":     (74, 132, 112),
    "fatiguementale":     (190, 106, 78),
    "alimentation":       (112, 140, 62),
    "procrastination":    (214, 106, 84),
    "somatisation":       (48, 128, 140),
    "blocagemental":      (122, 84, 148),
    "posturesantistress": (62, 118, 170),
    "energie":            (200, 138, 40),
}

def melanger(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def gen_fond(nom, accent, variante):
    L, H = 1000, 1500
    # Dégradé vertical doux clair -> légèrement plus soutenu en bas
    haut = melanger((255, 252, 247), tuple(int(c + (255 - c) * 0.82) for c in accent), 0.5)
    bas = melanger(haut, accent, 0.22)
    img = Image.new("RGB", (L, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (L, y)], fill=melanger(haut, bas, y / H))
    # Halo radial très doux (éclat focal) pour donner de la profondeur
    if variante % 3 == 0:
        overlay = Image.new("L", (L, H), 0)
        od = ImageDraw.Draw(overlay)
        cx, cy = L * (0.5 + (variante % 5 * 0.18 - 0.36)), H * (variante % 7 * 0.12 - 0.05)
        r = int(L * 0.9)
        od.ellipse([cx - r, cy - r, cx + r, cy + r], fill=90)
        overlay = overlay.filter(ImageFilter.GaussianBlur(220))
        fondl = img.convert("L")
        img = Image.composite(
            Image.new("RGB", (L, H), accent),
            img, overlay
        )
    nom_fichier = f"doux_{nom}_{variante}.jpg"
    img = img.filter(ImageFilter.GaussianBlur(1))
    img.save(os.path.join(OUT, nom_fichier), "JPEG", quality=92, optimize=True)
    return nom_fichier

entries = json.load(open("fonds_themes.json", encoding="utf-8")) if os.path.exists("fonds_themes.json") else {}
for theme, accent in ACCENTS.items():
    for v in range(3):  # 3 variations par thème
        nom = gen_fond(theme, accent, v)
        entries[nom] = theme

with open("fonds_themes.json", "w", encoding="utf-8") as f:
    json.dump(entries, f, indent=1)
print("Fonds doux générés -> fonds_themes.json:", len(entries), "entrées")
