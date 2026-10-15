"""Épingle « exercices illustrés » (15/10/2026) : illustrations sans texte (Hugging Face gratuit, triées à l'œil) + texte dessiné par PIL. Exemple d'appel en bas du fichier (kit 8)."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

POL = "/home/user/pins-clarte/polices/"
W, H = 1000, 1500
CREME = (250, 247, 238)
CARTE = (253, 251, 245)
VERT = (62, 98, 74)
VERT_CLAIR = (126, 156, 130)
TEXTE = (52, 58, 52)


def police(nom, t):
    return ImageFont.truetype(POL + nom, t)


def lignes(draw, texte, f, largeur):
    mots, out, cur = texte.split(), [], ""
    for m in mots:
        essai = (cur + " " + m).strip()
        if draw.textlength(essai, font=f) <= largeur:
            cur = essai
        else:
            out.append(cur)
            cur = m
    out.append(cur)
    return out


def recadrer(chemin, taille):
    im = Image.open(chemin).convert("RGB")
    gris = im.convert("L")
    # pixels nettement plus sombres que le papier = l'illustration
    masque = gris.point(lambda v: 255 if v < 215 else 0).filter(ImageFilter.MaxFilter(9))
    x0, y0, x1, y1 = masque.getbbox()
    c = max(x1 - x0, y1 - y0) * 1.12
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    im = im.crop((int(cx - c / 2), int(cy - c / 2), int(cx + c / 2), int(cy + c / 2)))
    im = im.resize((taille, taille), Image.LANCZOS)
    # fondre le papier de l'illustration dans la couleur de la carte
    fond = Image.new("RGB", im.size, CARTE)
    m = im.convert("L").point(lambda v: 255 if v < 238 else int(max(0, (250 - v)) * 20))
    return Image.composite(im, fond, m.filter(ImageFilter.GaussianBlur(1.2)))


def dessiner(donnees, sortie):
    img = Image.new("RGB", (W, H), CREME)
    d = ImageDraw.Draw(img)
    # léger lavis vert en haut et en bas
    lavis = Image.new("L", (W, H), 0)
    dl = ImageDraw.Draw(lavis)
    dl.ellipse((-250, -260, 520, 260), fill=70)
    dl.ellipse((560, 1260, 1300, 1800), fill=70)
    lavis = lavis.filter(ImageFilter.GaussianBlur(90))
    img = Image.composite(Image.new("RGB", (W, H), (214, 230, 214)), img, lavis)
    d = ImageDraw.Draw(img)

    y = 70
    f_acc = police("DancingScript-Bold.ttf", 46)
    t = donnees["accroche"]
    d.text(((W - d.textlength(t, font=f_acc)) / 2, y), t, font=f_acc, fill=VERT_CLAIR)
    y += 72
    f_tit = police("PlayfairDisplay-Bold.ttf", 66)
    for l in [x for p in donnees["titre_image"].split("\n") for x in lignes(d, p, f_tit, W - 140)]:
        d.text(((W - d.textlength(l, font=f_tit)) / 2, y), l, font=f_tit, fill=VERT)
        y += 80
    y += 18
    f_sous = police("Lora-Regular.ttf", 30)
    t = donnees["sous_titre"]
    d.text(((W - d.textlength(t, font=f_sous)) / 2, y), t, font=f_sous, fill=TEXTE)
    y += 66

    n = len(donnees["etapes"])
    bas = H - 150
    gap = 26
    hc = int((bas - y - gap * (n - 1)) / n)
    f_num = police("PlayfairDisplay-Bold.ttf", 34)
    f_lab = police("Lora-SemiBold.ttf", 38)
    f_txt = police("Lora-Regular.ttf", 29)
    for i, e in enumerate(donnees["etapes"]):
        x0, x1 = 60, W - 60
        d.rounded_rectangle((x0, y, x1, y + hc), radius=34, fill=CARTE, outline=(226, 232, 220), width=2)
        taille = hc - 30
        img.paste(recadrer(e["image"], taille), (x0 + 15, y + 15))
        d = ImageDraw.Draw(img)
        tx = x0 + 15 + taille + 30
        larg = x1 - 30 - tx
        cx, cy, r = tx + 26, y + 58, 26
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=VERT)
        num = str(i + 1)
        d.text((cx - d.textlength(num, font=f_num) / 2, cy - 24), num, font=f_num, fill=CARTE)
        ls = lignes(d, e["label"], f_lab, larg - 70)
        ty = y + 34
        for l in ls:
            d.text((tx + 66, ty), l, font=f_lab, fill=VERT)
            ty += 46
        ty = max(ty, y + 100) + 10
        for l in lignes(d, e["texte"], f_txt, larg):
            d.text((tx, ty), l, font=f_txt, fill=TEXTE)
            ty += 40
        assert ty <= y + hc - 8, ("texte trop long", e["label"])
        y += hc + gap

    f_pied = police("Lora-Regular.ttf", 28)
    t = donnees["prudence"]
    d.text(((W - d.textlength(t, font=f_pied)) / 2, H - 132), t, font=f_pied, fill=VERT_CLAIR)
    f_cta = police("DancingScript-Bold.ttf", 44)
    t = donnees["cta"]
    d.text(((W - d.textlength(t, font=f_cta)) / 2, H - 86), t, font=f_cta, fill=VERT)
    img.save(sortie, quality=92)


if __name__ == "__main__":
    S = "/tmp/claude-0/-home-user-pins-clarte/f6e3b31f-001c-4d3f-a940-fd7ac5cfb999/scratchpad/illus/"
    dessiner({
        "accroche": "Pause épaules",
        "titre_image": "3 exercices pour\nrelâcher tes épaules",
        "sous_titre": "Sur une chaise · 2 minutes · sans matériel",
        "etapes": [
            {"image": S + "epaules-1-relacher.webp", "label": "Laisser tomber les épaules",
             "texte": "Mains sur les cuisses, inspire. En soufflant, laisse les épaules descendre loin des oreilles. 5 fois."},
            {"image": S + "epaules-2-coudes.webp", "label": "Ouvrir les coudes",
             "texte": "Mains derrière la tête, ouvre doucement les coudes vers l'arrière. Garde 5 respirations lentes."},
            {"image": S + "epaules-3-ciel.webp", "label": "S'étirer vers le haut",
             "texte": "Bras tendus au-dessus de la tête, mains jointes, grandis-toi sans creuser le dos. 3 respirations."},
        ],
        "prudence": "Sans forcer : arrête si un geste fait mal.",
        "cta": "À enregistrer pour ta prochaine pause",
    }, S + "prototype-epaules.jpg")
    print("ok")
