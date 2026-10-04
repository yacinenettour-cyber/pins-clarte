"""Génère des épingles de qualité (design sombre + clair) depuis les nouvelles entrées de
pins.json, sans coût OpenAI. Réutilise les fonctions de dessin du workflow (pins.yml)."""
import json, os, re, io, glob, random
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageStat

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)

MARQUE = "Clarté Mentale | Stress & Énergie"

def charger_police(c, taille):
    if c and os.path.exists(c):
        return ImageFont.truetype(c, taille)
    return ImageFont.load_default(size=taille)

def couper_lignes(d, texte, police, largeur_max):
    lignes, ligne = [], ""
    for mot in re.split(r"(?<!«)\s+(?![?!:;»])", texte.strip()):
        essai = (ligne + " " + mot).strip()
        if d.textlength(essai, font=police) <= largeur_max:
            ligne = essai
        else:
            if ligne:
                lignes.append(ligne)
            ligne = mot
    if ligne:
        lignes.append(ligne)
    return lignes

def ajuster_sans_rogner(img, L, H, fond=(10, 10, 14)):
    r = min(L / img.width, H / img.height)
    img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    toile = Image.new("RGB", (L, H), fond)
    x, y = (L - img.width) // 2, (H - img.height) // 2
    toile.paste(img, (x, y))
    return toile

# --- Palettes & thèmes (copiés du workflow) ---
THEME_ALIASES = {
    "sommeil": "sommeil", "insomnie": "sommeil", "reveilnocturne": "sommeil",
    "reveil": "sommeil", "routinedusoir": "sommeil", "rythmecircadien": "sommeil",
    "ecrans": "sommeil", "cortisol": "systemenerveux", "systemenerveux": "systemenerveux",
    "respiration": "systemenerveux", "coherencecardiaque": "systemenerveux",
    "anxiete": "systemenerveux", "detente": "systemenerveux",
    "fatiguementale": "fatiguementale", "chargementale": "fatiguementale", "fatigue": "fatiguementale",
    "alimentation": "alimentation", "procrastination": "procrastination",
    "somatisation": "somatisation", "energie": "energie", "recuperation": "energie",
    "blocagemental": "blocagemental", "clarte": "blocagemental",
    "posturesantistress": "posturesantistress",
}
def deviner_theme(description):
    tags = re.findall(r"#(\w+)", description)
    if not tags:
        return "systemenerveux"
    premier = tags[0].lower()
    if premier == "stress" and "travail" in [t.lower() for t in tags[:3]]:
        return "posturesantistress"
    return THEME_ALIASES.get(premier, "systemenerveux")

AC = {
    "sommeil": (72, 88, 158), "systemenerveux": (74, 132, 112), "fatiguementale": (190, 106, 78),
    "alimentation": (112, 140, 62), "procrastination": (214, 106, 84), "somatisation": (48, 128, 140),
    "blocagemental": (122, 84, 148), "posturesantistress": (62, 118, 170), "energie": (200, 138, 40),
}
LIBELLES = {
    "sommeil": "Sommeil", "systemenerveux": "Système nerveux", "fatiguementale": "Fatigue mentale",
    "alimentation": "Alimentation & stress", "procrastination": "Procrastination",
    "somatisation": "Signaux du corps", "blocagemental": "Clarté mentale",
    "posturesantistress": "Anti-stress au travail", "energie": "Énergie",
}
NUIT = (12, 18, 36)
CREME, ENCRE, CARTE, OMBRE = (247, 243, 236), (31, 41, 64), (255, 255, 255), (228, 221, 209)
TEXTE_BANDEAU = "GUIDE GRATUIT · lien dans l'épingle"
THEMES_SANS_LIEN = {"alimentation", "procrastination", "energie", "fatiguementale"}

def dessiner_bandeau_guide(d, L, y, fond_couleur, texte_couleur, police_grasse):
    police = charger_police("Poppins-Bold.ttf", 30)
    w = d.textlength(TEXTE_BANDEAU, font=police)
    x0 = (L - w) / 2 - 30
    d.rounded_rectangle([x0, y, x0 + w + 60, y + 54], radius=27, fill=fond_couleur)
    d.text((x0 + 30, y + 9), TEXTE_BANDEAU, font=police, fill=texte_couleur)

def dessiner_marqueur(d, style, x_centre, y_centre, rayon, num, accent, police_num):
    if style == "coche":
        d.ellipse([x_centre - rayon, y_centre - rayon, x_centre + rayon, y_centre + rayon], fill=accent)
        d.line([(x_centre - rayon * 0.45, y_centre + rayon * 0.05),
                (x_centre - rayon * 0.1, y_centre + rayon * 0.4),
                (x_centre + rayon * 0.5, y_centre - rayon * 0.35)],
               fill=(20, 20, 30), width=6, joint="curve")
    elif style == "fleche":
        lc, hc, pointe = rayon * 0.9, rayon * 0.5, rayon * 0.7
        pts = [(x_centre - lc, y_centre - hc / 2), (x_centre, y_centre - hc / 2),
               (x_centre, y_centre - rayon * 0.55), (x_centre + pointe, y_centre),
               (x_centre, y_centre + rayon * 0.55), (x_centre, y_centre + hc / 2),
               (x_centre - lc, y_centre + hc / 2)]
        d.polygon(pts, fill=accent)
    elif style == "puce":
        r2 = rayon * 0.55
        d.ellipse([x_centre - r2, y_centre - r2, x_centre + r2, y_centre + r2], fill=accent)
    else:
        d.ellipse([x_centre - rayon, y_centre - rayon, x_centre + rayon, y_centre + rayon], fill=accent)
        t = str(num)
        w = d.textlength(t, font=police_num)
        d.text((x_centre - w / 2, y_centre - rayon + 4), t, font=police_num, fill=(20, 20, 30))

def dessiner_infographie(titre, points, chemin, fond, avec_lien, style):
    L, H = 1000, 1500
    img = Image.new("RGB", (L, H), NUIT)
    d = ImageDraw.Draw(img)
    marge = 90
    largeur = L - 2 * marge
    rayon = 26
    x_num_centre = marge + rayon
    x_texte = marge + 2 * rayon + 22
    espace_entre_points, espace_titre_points = 22, 46
    bas_contenu, haut_min = (1225 if avec_lien else 1295), 290
    for taille_titre, taille_point in [(78, 42), (70, 40), (64, 38), (58, 36), (54, 34), (50, 32), (48, 30)]:
        pt = charger_police("Poppins-Bold.ttf", taille_titre)
        lt = couper_lignes(d, titre, pt, largeur)
        hlt = int(taille_titre * 1.2)
        ppo = charger_police("Poppins-Regular.ttf", taille_point)
        pno = charger_police("Poppins-Bold.ttf", taille_point)
        lpp = [couper_lignes(d, p, ppo, largeur - 70) for p in points]
        hlpp = int(taille_point * 1.32)
        hp = sum(len(lp) * hlpp for lp in lpp) + espace_entre_points * (len(points) - 1)
        ht = hlt * len(lt) + espace_titre_points + hp
        if len(lt) <= 3 and bas_contenu - ht >= haut_min:
            break
    haut_texte = max(bas_contenu - ht, haut_min)
    # photo en haut si fond
    h_photo = haut_texte - 50 if fond else 0
    if h_photo >= 250:
        imgf = ajuster_sans_rogner(Image.open(fond).convert("RGB"), L, H)
        bande = imgf.crop((0, 0, L, h_photo)).convert("RGBA")
        # fondu vers le bas (transparent en bas)
        fondu = Image.new("L", (L, h_photo), 255)
        fd = ImageDraw.Draw(fondu)
        fd.rectangle([0, h_photo - 180, L, h_photo], fill=0)
        fondu = fondu.filter(ImageFilter.GaussianBlur(60))
        # voile sombre pour la lisibilité du titre, avec fondu
        voile = Image.new("RGBA", (L, h_photo), (10, 14, 30, 130))
        voile.putalpha(fondu)
        bande = Image.alpha_composite(bande, voile)
        img.paste(bande, (0, 0), bande)
    else:
        h_photo = 0
        haut, bas = (22, 30, 58), (58, 70, 120)
        for y in range(H):
            t = y / H
            d.line([(0, y), (L, y)], fill=tuple(int(haut[i] + (bas[i] - haut[i]) * t) for i in range(3)))
    y = haut_texte
    for ligne in lt:
        w = d.textlength(ligne, font=pt)
        x = (L - w) / 2
        d.text((x + 3, y + 3), ligne, font=pt, fill=(8, 12, 26))
        d.text((x, y), ligne, font=pt, fill=(255, 255, 255))
        y += hlt
    y += espace_titre_points
    accent = (236, 196, 120)
    for i, lp in enumerate(lpp, start=1):
        y_cc = y + hlpp / 2 - 6
        dessiner_marqueur(d, style, x_num_centre, y_cc, rayon, i, accent, pno)
        for ligne in lp:
            d.text((x_texte + 2, y + 2), ligne, font=ppo, fill=(8, 12, 26))
            d.text((x_texte, y), ligne, font=ppo, fill=(255, 255, 255))
            y += hlpp
        y += espace_entre_points
    d.line([(L / 2 - 70, y + 10), (L / 2 + 70, y + 10)], fill=(236, 230, 205), width=5)
    if avec_lien:
        dessiner_bandeau_guide(d, L, H - 165, (236, 196, 120), (20, 20, 30), "Poppins-Bold.ttf")
    pp = charger_police("Poppins-Regular.ttf", 34)
    w = d.textlength(MARQUE, font=pp)
    d.text(((L - w) / 2, H - 92), MARQUE, font=pp, fill=(232, 235, 245))
    img.save(chemin, "JPEG", quality=90, optimize=True, progressive=True)

def _etiquette_et_titre(d, theme, titre, marge, largeur):
    accent = AC.get(theme, AC["systemenerveux"])
    pep = charger_police("Poppins-Bold.ttf", 26)
    etq = LIBELLES.get(theme, "Bien-être").upper()
    w = d.textlength(etq, font=pep)
    clair = tuple(int(c + (255 - c) * 0.82) for c in accent)
    d.rounded_rectangle([marge, 70, marge + w + 44, 70 + 50], radius=25, fill=clair)
    d.text((marge + 22, 70 + 9), etq, font=pep, fill=accent)
    y = 70 + 50 + 38
    taille = 78
    while taille > 52:
        police = charger_police("Poppins-Bold.ttf", taille)
        lignes = couper_lignes(d, titre, police, largeur)
        if len(lignes) <= 3:
            break
        taille -= 4
    hl = int(taille * 1.16)
    for ligne in lignes:
        d.text((marge, y), ligne, font=police, fill=ENCRE)
        y += hl
    y += 22
    d.rounded_rectangle([marge, y, marge + 120, y + 9], radius=5, fill=accent)
    return y + 9, accent

def dessiner_clair_infographie(titre, points, chemin, fond, theme, avec_lien):
    L, H, marge = 1000, 1500, 70
    img = Image.new("RGB", (L, H), CREME)
    d = ImageDraw.Draw(img)
    style = "numero" if re.search(r"\d", titre) else "coche"
    r, bas, pad = 30, H - (200 if avec_lien else 120), 26
    largeur = L - 2 * marge
    def mise_en_page(tt, tp, esp):
        y_haut, accent = _etiquette_et_titre(d, theme, titre, marge, largeur)
        y_haut += 44
        x_txt = marge + pad + 2 * r + 24
        ppt = charger_police("Poppins-Regular.ttf", tp)
        hl = int(tp * 1.3)
        cartes = []
        for p in points:
            lignes = couper_lignes(d, p, ppt, L - marge - pad - x_txt)
            cartes.append((lignes, max(2 * r, len(lignes) * hl) + 2 * pad))
        h_c = sum(h for _, h in cartes) + esp * (len(cartes) - 1)
        return (tt, tp, esp, x_txt, ppt, hl, cartes, bas - y_haut - h_c), accent
    choix = None
    for tt in (78, 70, 64):
        for tp in (36, 34, 32, 30, 28):
            for esp in (20, 14):
                m, accent = mise_en_page(tt, tp, esp)
                if m[-1] - 40 >= 300:
                    choix = m
                    break
            if choix:
                break
        if choix:
            break
    if choix is None:
        m, accent = mise_en_page(64, 30, 14)
        choix = m
    tt, tp, esp, x_txt, ppt, hl, cartes, reste = choix
    y, accent = _etiquette_et_titre(d, theme, titre, marge, largeur)
    y += 44
    h_photo = min(reste - 40, 430)
    if h_photo < 300:
        h_photo = 0
    if not h_photo:
        y += max(0, reste // 2)
    for i, (lignes, h) in enumerate(cartes, start=1):
        d.rounded_rectangle([marge + 3, y + 6, L - marge + 3, y + h + 6], radius=26, fill=OMBRE)
        d.rounded_rectangle([marge, y, L - marge, y + h], radius=26, fill=CARTE)
        pno = charger_police("Poppins-Bold.ttf", 34)
        d.ellipse([marge + pad, y + h / 2 - r, marge + pad + 2 * r, y + h / 2 + r], fill=accent)
        t = str(i)
        w = d.textlength(t, font=pno)
        d.text((marge + pad + r - w / 2, y + h / 2 - r + 4), t, font=pno, fill=(255, 255, 255))
        yt = y + (h - len(lignes) * hl) / 2 - 4
        for ligne in lignes:
            d.text((x_txt, yt), ligne, font=ppt, fill=ENCRE)
            yt += hl
        y += h + esp
    if h_photo:
        imgp = ajuster_sans_rogner(Image.open(fond).convert("RGB"), L - 2 * marge, h_photo)
        masque = Image.new("L", imgp.size, 0)
        ImageDraw.Draw(masque).rounded_rectangle([0, 0, imgp.width - 1, imgp.height - 1], radius=30, fill=255)
        img.paste(imgp, (marge, bas - h_photo), masque)
    if avec_lien:
        dessiner_bandeau_guide(d, L, H - 160, accent, (255, 255, 255), "Poppins-Bold.ttf")
    pp = charger_police("Poppins-Regular.ttf", 30)
    w = d.textlength(MARQUE, font=pp)
    d.text(((L - w) / 2, H - 78), MARQUE, font=pp, fill=(110, 116, 132))
    img.save(chemin, "JPEG", quality=90, optimize=True, progressive=True)

# --- Sélection des pins à transformer en image_prete ---
banque = json.load(open("pins.json", encoding="utf-8"))
hist = json.load(open("historique.json", encoding="utf-8")) if os.path.exists("historique.json") else []
faits = {h["titre"] for h in hist}
deja_prete = {p["titre"] for p in banque if p.get("image_prete")}

# Sélectionner les pins SANS image_prete, non publiés, avec points_image (infographies lisibles)
candidats = [p for p in banque if p["titre"] not in faits and p["titre"] not in deja_prete
             and p.get("points_image")]
print(f"Candidats sans image_prete: {len(candidats)}")

os.makedirs("images_manuelles", exist_ok=True)
styles = ["numero", "coche", "fleche", "puce"]
fonds_themes = json.load(open("fonds_themes.json", encoding="utf-8"))
fonds_doux = {k: v for k, v in fonds_themes.items() if k.startswith("doux_")}

gen_count = 0
for pin in candidats[:12]:  # lot initial
    theme = deviner_theme(pin["description"])
    avec_lien = theme not in THEMES_SANS_LIEN
    # choix d'un fond doux du même thème (en rotant)
    theme_fonds = [k for k, v in fonds_doux.items() if v == theme]
    fond = None
    if theme_fonds:
        idx = candidats.index(pin) % len(theme_fonds)
        fond = os.path.join("fonds", theme_fonds[idx])
    slug = re.sub(r"[^a-z0-9]+", "-", pin["titre"].lower())[:48].strip("-")
    chemin = os.path.join("images_manuelles", f"manu_{slug}.jpg")
    design = "clair" if gen_count % 2 == 0 else "sombre"
    style = random.choice(styles)
    try:
        if design == "clair":
            dessiner_clair_infographie(pin["texte_image"], pin["points_image"], chemin, fond, theme, avec_lien)
        else:
            dessiner_infographie(pin["texte_image"], pin["points_image"], chemin, fond, avec_lien, style)
        # Décorer la référence image_prete dans pistes.json (fichier local temporaire)
        pin["image_prete"] = f"images_manuelles/manu_{slug}.jpg"
        gen_count += 1
        print(f"  [{theme:18s}] {design:6s} {chemin}")
    except Exception as e:
        print(f"  ERR {pin['titre'][:40]}: {str(e)[:70]}")

# Sauvegarder le nouvel état de pins.json localement
with open("pins.json", "w", encoding="utf-8") as f:
    json.dump(banque, f, ensure_ascii=False, indent=1)
print(f"\nGénérées: {gen_count} épingles -> référencées en image_prete dans pins.json")
