"""Épingle « fiche-mémo » (05/11/2026) : 6 à 8 éléments illustrés en grille sur une seule image, comme les épingles
concurrentes les plus enregistrées (pixeliazone, sobienetrenaturel : fiches denses, sans lien, une seule image).
Icônes : une grille 3 × 3 d'aquarelles générée en un seul appel (Hugging Face gratuit), découpée case par case.
Texte toujours dessiné par PIL ; chaque zone est contrôlée (aucun débordement, aucun chevauchement).
Appel : dessiner(D, sortie) avec D = {"etiquette", "titre1", "titre2", "grille", "items": [n × {"case", "label", "texte"}],
"bandeau"} ; "case" = numéro 0-8 de la case de la grille (ligne par ligne)."""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
sys.path.insert(0, "/home/user/pins-clarte/outils")
from planche_riche import W, H, OR, BRUN, TXT, ROSE, SAUGE, f, lignes, centre, papier


def icone(grille, case, taille):
    g = Image.open(grille).convert("RGB")
    cw, ch = g.width // 3, g.height // 3
    x, y = (case % 3) * cw, (case // 3) * ch
    m = int(min(cw, ch) * 0.05)
    v = g.crop((x + m, y + m, x + cw - m, y + ch - m))
    fond = v.getpixel((3, 3))
    diff = ImageChops.difference(v, Image.new("RGB", v.size, fond)).convert("L").point(lambda p: 255 if p > 22 else 0)
    diff = diff.filter(ImageFilter.MaxFilter(9))
    bb = diff.getbbox()
    assert bb, ("case vide", grille, case)
    v, diff = v.crop(bb), diff.crop(bb)
    r = taille / max(v.size)
    v = v.resize((max(1, int(v.width * r)), max(1, int(v.height * r))), Image.LANCZOS)
    masque = diff.resize(v.size, Image.LANCZOS).filter(ImageFilter.GaussianBlur(3))
    return v, masque


def insec(t):
    for a in (" :", " ?", " !", " °C", " ;", " …"):
        t = t.replace(a, "\u00a0" + a[1:])
    return t


def dessiner(D, sortie):
    img = papier()
    d = ImageDraw.Draw(img)
    zones = []
    fe = f("Lora-SemiBold.ttf", 22)
    et = "  ".join(D["etiquette"].upper())
    centre(d, 54, et, fe, SAUGE)
    ft1 = f("PlayfairDisplay-Bold.ttf", 66)
    while d.textlength(D["titre1"].upper(), font=ft1) > W - 110:
        ft1 = f("PlayfairDisplay-Bold.ttf", ft1.size - 2)
    centre(d, 92, D["titre1"].upper(), ft1, BRUN)
    ft2 = f("DancingScript-Bold.ttf", 60)
    while d.textlength(D["titre2"], font=ft2) > W - 110:
        ft2 = f("DancingScript-Bold.ttf", ft2.size - 2)
    y2 = 92 + ft1.size + 14
    centre(d, y2, D["titre2"], ft2, ROSE)
    yfin = y2 + ft2.size + 22
    d.line((W / 2 - 60, yfin, W / 2 + 60, yfin), fill=OR, width=3)
    zones.append((0, yfin))

    fb = f("Lora-SemiBold.ttf", 25)
    lb = lignes(d, insec(D["bandeau"]), fb, W - 200)
    hb = 26 + 34 * len(lb)
    by0 = H - 104 - hb
    items = D["items"]
    n = len(items)
    assert 6 <= n <= 8, n
    rangs = (n + 1) // 2
    haut, bas = yfin + 34, by0 - 26
    hc = (bas - haut) / rangs
    ic = int(min(150, hc - 40))
    flab, ftx = f("PlayfairDisplay-Bold.ttf", 29), f("Lora-Regular.ttf", 22)
    colw = (W - 90) // 2
    for i, it in enumerate(items):
        col, rg = i % 2, i // 2
        x0 = 45 + col * colw
        if n % 2 and i == n - 1:
            x0 = 45 + colw // 2
        y0 = haut + rg * hc
        v, mk = icone(D["grille"], it["case"], ic)
        img.paste(v, (int(x0 + (ic - v.width) / 2), int(y0 + (hc - v.height) / 2)), mk)
        tx0, tx1 = x0 + ic + 18, x0 + colw - 12
        ll = lignes(d, insec(it["label"]), flab, tx1 - tx0)
        lt = lignes(d, insec(it["texte"]), ftx, tx1 - tx0)
        assert len(ll) <= 2 and len(lt) <= 4, ("trop long", it["label"], ll, lt)
        bloc = len(ll) * 36 + 6 + len(lt) * 29
        ty = y0 + (hc - bloc) / 2
        assert ty >= y0 - 2 and ty + bloc <= y0 + hc + 2, ("élément trop haut", it["label"])
        num = f("PlayfairDisplay-Bold.ttf", 20)
        for k, l in enumerate(ll):
            d.text((tx0, ty + k * 36), l, font=flab, fill=BRUN)
        yy = ty + len(ll) * 36 + 6
        for k, l in enumerate(lt):
            d.text((tx0, yy + k * 29), l, font=ftx, fill=TXT)
        d.ellipse((x0 - 4, y0 + (hc - ic) / 2 - 4, x0 + 30, y0 + (hc - ic) / 2 + 30), fill=ROSE)
        centre(d, y0 + (hc - ic) / 2 - 1, str(i + 1), num, (255, 250, 244), x0 - 4, x0 + 30)
        zones.append((y0, y0 + hc))
    assert haut + rangs * hc <= by0 - 20

    d.rounded_rectangle((100, by0, W - 100, by0 + hb), radius=hb // 2, fill=(226, 234, 220), outline=SAUGE, width=2)
    for k, l in enumerate(lb):
        centre(d, by0 + 13 + k * 34, l, fb, BRUN)
    centre(d, H - 58, "Clarté Mentale | Stress & Énergie", f("Lora-Regular.ttf", 24), (120, 100, 80))
    img.save(sortie, "JPEG", quality=92)
    return zones
