"""Épingle « clés » (15/10/2026) : cadre doré + personnage central (illustrations sans texte, Hugging Face gratuit, propres à chaque épingle) + 5 clés numérotées ; texte dessiné par PIL, icônes = police libre Noto Color Emoji (OFL) du système. Exemple d'appel en bas du fichier (première épingle)."""
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
POL = "/home/user/pins-clarte/polices/"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
W, H = 1000, 1500
OR = (176, 128, 52); BRUN = (74, 52, 36); TXT = (60, 52, 44)
f = lambda n, t: ImageFont.truetype(POL + n, t)

def emoji(c, taille):
    fe = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((6, 6), c, font=fe, embedded_color=True)
    im = im.crop(im.getbbox())
    return im.resize((taille, int(taille * im.height / im.width)), Image.LANCZOS)

def lignes(d, t, fo, l):
    out, cur = [], ""
    for m in t.split(" "):
        e = (cur + " " + m).strip()
        if d.textlength(e, font=fo) <= l: cur = e
        else: out.append(cur); cur = m
    out = out + [cur]
    assert all(d.textlength(x, font=fo) <= l + 1 for x in out), ("texte trop large", out)
    return out

def centre(d, y, t, fo, fill, x0=0, x1=W):
    d.text((x0 + (x1 - x0 - d.textlength(t, font=fo)) / 2, y), t, font=fo, fill=fill)

def cle(img, d, x0, x1, y, i, c):
    cx = x0 + 32
    d.ellipse((x0, y, x0 + 60, y + 60), fill=OR)
    centre(d, y + 4, str(i), f("PlayfairDisplay-Bold.ttf", 40), (255, 250, 238), x0, x0 + 60)
    fl = f("PlayfairDisplay-Bold.ttf", 36)
    ty = y + 8
    for l in lignes(d, c["label"], fl, x1 - x0 - 75):
        d.text((x0 + 74, ty), l, font=fl, fill=BRUN); ty += 42
    ic = emoji(c["icone"], 66)
    ty += 8
    img.paste(ic, (int(x0 + (x1 - x0 - ic.width) / 2), int(ty)), ic); ty += ic.height + 10
    ft = f("Lora-Regular.ttf", 26)
    for l in lignes(d, c["texte"], ft, x1 - x0):
        centre(d, ty, l, ft, TXT, x0, x1); ty += 33
    fp = f("Lora-SemiBold.ttf", 25)
    for l in lignes(d, c["pour"], fp, x1 - x0):
        centre(d, ty + 4, l, fp, BRUN, x0, x1); ty += 31
    return ty

def dessiner(D, sortie):
    img = Image.open(D["fond"]).convert("RGB").resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    # personnage central en « produit » (le papier clair disparaît)
    p = Image.open(D["centre"]).convert("RGB")
    sombre = p.convert("L").point(lambda v: 255 if v < 200 else 0).filter(ImageFilter.MaxFilter(25)).filter(ImageFilter.MinFilter(25))
    p = p.crop(sombre.getbbox()); sombre = sombre.crop(sombre.getbbox())
    h = 470; w = int(p.width * h / p.height)
    p = p.resize((w, h), Image.LANCZOS); m = sombre.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.5))
    img.paste(p, (int((W - w) / 2), 440), m); d = ImageDraw.Draw(img)
    # titre
    f1 = f("PlayfairDisplay-Bold.ttf", 74); f5 = f("PlayfairDisplay-Bold.ttf", 120)
    a, b = D["titre1"]
    wa = d.textlength(a + " ", font=f1); w5 = d.textlength(D["chiffre"] + " ", font=f5); wb = d.textlength(b, font=f1)
    x = (W - wa - w5 - wb) / 2
    d.text((x, 118), a + " ", font=f1, fill=BRUN); d.text((x + wa, 80), D["chiffre"], font=f5, fill=OR)
    d.text((x + wa + w5, 118), b, font=f1, fill=BRUN)
    centre(d, 205, D["titre2"], f("PlayfairDisplay-Bold.ttf", 64), OR)
    fs = f("Lora-SemiBold.ttf", 30); ws = d.textlength(D["sous_titre"], font=fs)
    d.rounded_rectangle(((W - ws) / 2 - 34, 296, (W + ws) / 2 + 34, 350), radius=27, fill=(250, 236, 205), outline=OR, width=2)
    centre(d, 304, D["sous_titre"], fs, BRUN)
    C = D["cles"]
    b1 = cle(img, d, 78, 338, 395, 1, C[0]); b2 = cle(img, d, 662, 922, 395, 2, C[1])
    y34 = max(b1, b2) + 18
    b3 = cle(img, d, 78, 338, y34, 3, C[2]); b4 = cle(img, d, 662, 922, y34, 4, C[3])
    assert max(b3, b4) < 1075 and 440 + 470 < 1075, (b1, b2, b3, b4)
    # 5e clé en bas, sur toute la largeur
    y = 1085
    ic = emoji(C[4]["icone"], 78); img.paste(ic, (200, y + 10), ic)
    d.ellipse((300, y, 356, y + 56), fill=OR); centre(d, y + 2, "5", f("PlayfairDisplay-Bold.ttf", 38), (255, 250, 238), 300, 356)
    d.text((372, y + 6), C[4]["label"], font=f("PlayfairDisplay-Bold.ttf", 36), fill=BRUN)
    ty = y + 62
    for l in lignes(d, C[4]["texte"], f("Lora-Regular.ttf", 26), 500):
        d.text((300, ty), l, font=f("Lora-Regular.ttf", 26), fill=TXT); ty += 33
    d.text((300, ty + 2), C[4]["pour"], font=f("Lora-SemiBold.ttf", 25), fill=BRUN)
    assert ty + 34 < 1262, ty
    # bandeau final
    fc = f("DancingScript-Bold.ttf", 46)
    d.rounded_rectangle((130, 1268, 870, 1352), radius=40, fill=(231, 196, 120))
    centre(d, 1282, D["cta"], fc, (255, 251, 240))
    img.save(sortie, quality=92)

if __name__ == "__main__":
    S = "/tmp/claude-0/-home-user-pins-clarte/f6e3b31f-001c-4d3f-a940-fd7ac5cfb999/scratchpad/illus/"
    dessiner({"fond": S + "cadre-dore.webp", "centre": S + "calme-centre.webp",
      "titre1": ("Top", "clés pour"), "chiffre": "5", "titre2": "garder ton calme",
      "sous_titre": "Quand la journée s'emballe",
      "cles": [
        {"icone": "🌬️", "label": "Expirer plus long", "texte": "Inspire 4\u00a0s, souffle 6\u00a0s, pendant 1\u00a0minute.", "pour": "Pour calmer le corps"},
        {"icone": "🎯", "label": "Une seule tâche", "texte": "Finis une tâche avant la suivante.", "pour": "Pour moins te disperser"},
        {"icone": "🔕", "label": "Couper les alertes", "texte": "Notifications en pause 1\u00a0heure.", "pour": "Pour garder ton attention"},
        {"icone": "👟", "label": "Bouger 5\u00a0minutes", "texte": "Marche ou étire-toi entre deux tâches.", "pour": "Pour relâcher la tension"},
        {"icone": "📝", "label": "Noter ce qui traîne", "texte": "Écris ce qui t'encombre pour y revenir plus tard.", "pour": "Pour alléger ta tête"}],
      "cta": "Enregistre ces clés pour demain"}, S + "prototype-cles.jpg")
    print("ok")
