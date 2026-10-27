"""Épingle « riche » (27/10/2026) : personne réaliste au centre (portrait peint réaliste, Hugging Face gratuit), une vignette
aquarelle par point, titre à deux niveaux avec le mot-clé en écriture manuscrite, fond papier crème, bandeau « Sauvegarde
cette épingle pour… » et signature du compte (analyse des meilleures épingles du 25/10, meilleures-epingles.md).
Texte toujours dessiné par PIL ; chaque zone est contrôlée (aucun débordement, aucun chevauchement).
Appel : dessiner(D, sortie) avec D = {"titre1", "titre2", "portrait", "cles": [5 × {"vignette", "label", "texte"}], "bandeau"}."""
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

POL = "/home/user/pins-clarte/polices/"
W, H = 1000, 1500
CREME = (247, 240, 228); OR = (176, 128, 52); BRUN = (74, 52, 36); TXT = (62, 54, 46)
ROSE = (196, 120, 116); SAUGE = (124, 146, 118)
f = lambda n, t: ImageFont.truetype(POL + n, t)


def lignes(d, t, fo, l):
    out, cur = [], ""
    for m in t.split(" "):
        e = (cur + " " + m).strip()
        if d.textlength(e, font=fo) <= l:
            cur = e
        else:
            out.append(cur); cur = m
    out.append(cur)
    assert all(d.textlength(x, font=fo) <= l + 1 for x in out), ("texte trop large", out)
    return out


def centre(d, y, t, fo, fill, x0=0, x1=W):
    d.text((x0 + (x1 - x0 - d.textlength(t, font=fo)) / 2, y), t, font=fo, fill=fill)


def papier():
    random.seed(681678)
    img = Image.new("RGB", (W, H), CREME)
    bruit = Image.effect_noise((W, H), 18).convert("RGB").filter(ImageFilter.GaussianBlur(0.8))
    img = ImageChops.blend(img, ImageChops.multiply(img, bruit.point(lambda v: 225 + v // 8)), 0.35)
    # léger voile rose poudré en haut et sauge en bas
    voile = Image.new("RGB", (W, H), CREME); dv = ImageDraw.Draw(voile)
    dv.ellipse((-300, -350, 700, 420), fill=(240, 218, 210)); dv.ellipse((450, 1150, 1350, 1800), fill=(222, 230, 214))
    return Image.blend(img, voile.filter(ImageFilter.GaussianBlur(140)), 0.55)


def vignette(chemin, taille):
    v = Image.open(chemin).convert("RGB")
    fond = v.getpixel((4, 4))
    diff = ImageChops.difference(v, Image.new("RGB", v.size, fond)).convert("L").point(lambda x: 255 if x > 28 else 0)
    x0, y0, x1, y1 = diff.getbbox()
    c = max(x1 - x0, y1 - y0) * 1.18; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    marge = int(c)  # papier ajouté autour : jamais de coin noir quand on recadre au-delà de l'image
    grand = Image.new("RGB", (v.width + 2 * marge, v.height + 2 * marge), fond); grand.paste(v, (marge, marge))
    v, cx, cy = grand, cx + marge, cy + marge
    v = v.crop((int(cx - c / 2), int(cy - c / 2), int(cx + c / 2), int(cy + c / 2))).resize((taille, taille), Image.LANCZOS)
    m = Image.new("L", (taille * 4, taille * 4), 0); ImageDraw.Draw(m).ellipse((0, 0, taille * 4 - 1, taille * 4 - 1), fill=255)
    return v, m.resize((taille, taille), Image.LANCZOS)


def portrait(img, chemin, boite):
    x0, y0, x1, y1 = boite; w, h = x1 - x0, y1 - y0
    p = Image.open(chemin).convert("RGB")
    r = max(w / p.width, h / p.height); p = p.resize((int(p.width * r) + 1, int(p.height * r) + 1), Image.LANCZOS)
    p = p.crop(((p.width - w) // 2, 0, (p.width - w) // 2 + w, h))  # garder la tête en haut
    ombre = Image.new("L", (W, H), 0); ImageDraw.Draw(ombre).rounded_rectangle((x0 + 6, y0 + 12, x1 + 6, y1 + 12), 36, fill=90)
    img.paste((120, 96, 70), (0, 0), ombre.filter(ImageFilter.GaussianBlur(16)))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 36, fill=255)
    img.paste(p, (x0, y0), m)
    ImageDraw.Draw(img).rounded_rectangle((x0, y0, x1, y1), 36, outline=OR, width=3)


def cle(img, d, x0, x1, y, i, c, taille=128):
    """Vignette ronde + numéro, puis label et texte centrés dans la colonne ; renvoie le bas de la zone."""
    v, m = vignette(c["vignette"], taille)
    vx = int((x0 + x1 - taille) / 2)
    img.paste(v, (vx, y), m); d.ellipse((vx - 2, y - 2, vx + taille + 2, y + taille + 2), outline=OR, width=3)
    d.ellipse((vx - 10, y - 6, vx + 34, y + 38), fill=ROSE); centre(d, y - 4, str(i), f("PlayfairDisplay-Bold.ttf", 30), (255, 250, 240), vx - 10, vx + 34)
    ty = y + taille + 10
    fl = f("PlayfairDisplay-Bold.ttf", 32)
    for l in lignes(d, c["label"], fl, x1 - x0):
        centre(d, ty, l, fl, BRUN, x0, x1); ty += 39
    ft = f("Lora-Regular.ttf", 25)
    for l in lignes(d, c["texte"], ft, x1 - x0):
        centre(d, ty + 2, l, ft, TXT, x0, x1); ty += 32
    return ty + 4


def dessiner(D, sortie):
    img = papier(); d = ImageDraw.Draw(img)
    zones = []
    # titre à deux niveaux
    f1 = f("PlayfairDisplay-Bold.ttf", 52)
    y = 52
    for l in lignes(d, D["titre1"].upper(), f1, W - 120):
        centre(d, y, l, f1, BRUN); y += 62
    f2 = f("DancingScript-Bold.ttf", 86)
    assert d.textlength(D["titre2"], font=f2) <= W - 100, "titre manuscrit trop large"
    centre(d, y - 6, D["titre2"], f2, ROSE); y += 100
    d.line((W / 2 - 90, y, W / 2 + 90, y), fill=OR, width=3); y += 4
    zones.append(("titre", 40, y))
    # portrait au centre, 2 clés à gauche, 2 à droite
    py0, py1 = y + 30, y + 30 + 660
    portrait(img, D["portrait"], (310, py0, 690, py1)); d = ImageDraw.Draw(img)
    cols = [(34, 290), (710, 966)]
    bas = []
    for k, (x0, x1) in enumerate(cols):
        yy = py0 + 4
        for j in range(2):
            n = k * 2 + j
            yy = cle(img, d, x0, x1, yy, n + 1, D["cles"][n]) + 40
        bas.append(yy)
    assert max(bas) <= py1 + 60, ("colonnes trop hautes", bas, py1)
    # bandeau final (calculé d'abord), puis 5e clé centrée dans l'espace entre le portrait et le bandeau
    fb = f("Lora-SemiBold.ttf", 27)
    lb = lignes(d, D["bandeau"], fb, W - 200)
    hb = 30 + 34 * len(lb)
    by0 = H - 62 - hb - 20
    haut = max(py1, max(bas))
    essai = img.copy()
    h5 = cle(essai, ImageDraw.Draw(essai), 260, 740, 0, 5, D["cles"][4], taille=120)
    y5 = int(haut + (by0 - haut - h5) / 2)
    assert y5 >= haut + 20, ("pas assez de place pour la 5e clé", y5, haut)
    fin5 = cle(img, d, 260, 740, y5, 5, D["cles"][4], taille=120)
    zones.append(("clés", py0, fin5))
    assert by0 >= fin5 + 14, ("le bandeau chevauche la 5e clé", by0, fin5)
    d.rounded_rectangle((70, by0, W - 70, by0 + hb), 26, fill=(214, 224, 206), outline=SAUGE, width=2)
    ty = by0 + 15
    for l in lb:
        centre(d, ty, l, fb, BRUN); ty += 34
    centre(d, H - 58, "Clarté Mentale | Stress & Énergie", f("Lora-Regular.ttf", 24), (120, 100, 80))
    img.save(sortie, quality=92)
    return {"titre": zones[0], "clés": zones[1], "bandeau": (by0, by0 + hb)}


if __name__ == "__main__":
    import sys
    B = sys.argv[1]
    D = {
        "titre1": "Culpabilité de se reposer",
        "titre2": "5 clés pour souffler",
        "portrait": B + "/repos-portrait.webp",
        "cles": [
            {"vignette": B + "/v1-agenda.webp", "label": "Inscris ta pause", "texte": "Note-la dans ton agenda, comme un vrai rendez-vous."},
            {"vignette": B + "/v2-pousse.webp", "label": "Le repos compte", "texte": "Récupérer fait partie de l'effort, pas du temps perdu."},
            {"vignette": B + "/v3-sablier.webp", "label": "Commence petit", "texte": "10 minutes sans rien produire, pour t'y habituer."},
            {"vignette": B + "/v4-plume.webp", "label": "Le « je devrais »", "texte": "Remarque-le passer, sans lui obéir tout de suite."},
            {"vignette": B + "/v5-the.webp", "label": "Annonce ta pause", "texte": "« Je fais une pause, je reviens à 15 h. » Sans te justifier."},
        ],
        "bandeau": "Sauvegarde cette épingle pour les jours où tu n'oses pas t'arrêter",
    }
    print(dessiner(D, sys.argv[2]))
