"""Short vertical (1080×1920) : extrait « Respirer lentement » de la méditation, pour renvoyer vers la vidéo complète."""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
POL = "/home/user/pins-clarte/polices/"
W, H, FPS = 1080, 1920, 30
TL = json.load(open(f"{ICI}/timeline.json"))
S = TL["souffles"][0]
D0 = S["debut"] - 16.5          # « Puis, petit à petit, ralentis-la… » juste avant les cycles guidés
D1 = S["debut"] + S["cycles"] * 10 + 5
rng = np.random.default_rng(7)


def police(n, t):
    return ImageFont.truetype(POL + n, t)


def lisse(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


def fondu(t, d, f, e=0.5):
    return lisse((t - d) / e) * lisse((f - t) / e)


src = Image.open(os.path.join(ICI, "photos", "unsplash-ezBs5eD22UE.jpg")).convert("RGB")
r = H * 1.12 / src.height
src = src.resize((round(src.width * r), round(src.height * r)), Image.LANCZOS)
a = np.asarray(src, np.float32) * np.array([0.80, 0.84, 0.95]) * 0.9
src = Image.fromarray(a.clip(0, 255).astype(np.uint8))
yy, xx = np.mgrid[0:H, 0:W]
VIG = (1 - 0.5 * (((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)).clip(0.35, 1).astype(np.float32)[..., None]


def fond(t):
    u = (t - D0) / (D1 - D0)
    z = 1.0 + 0.08 * u
    cw, ch = min(W * 1.12 / z, src.width), min(H * 1.12 / z, src.height)
    cx = src.width * 0.5 + (src.width - cw) * 0.35 * (u - 0.5)
    cy = src.height / 2
    x0 = min(max(0.0, cx - cw / 2), src.width - cw); y0 = min(max(0.0, cy - ch / 2), src.height - ch)
    return np.asarray(src.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)), np.float32) * VIG


def bloc(lignes, tailles, couleurs, polices_, largeur=W, fond_=None):
    hs = [int(t * 1.35) for t in tailles]
    im = Image.new("RGBA", (largeur, sum(hs) + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if fond_:
        d.rounded_rectangle([60, 0, largeur - 60, im.height - 1], radius=30, fill=fond_)
    y = 20
    for l, t, c, p, h in zip(lignes, tailles, couleurs, polices_, hs):
        d.text((largeur / 2, y + h / 2), l, font=police(p, t), fill=c, anchor="mm"); y += h
    om = Image.new("RGBA", im.size, (0, 0, 0, 0)); om.putalpha(im.getchannel("A").filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.7)))
    return np.array(Image.alpha_composite(om, im), np.float32)


HAUT = bloc(["Respire avec moi", "pour t'endormir"], [86, 86], [(255, 248, 230, 255), (255, 214, 140, 255)],
            ["PlayfairDisplay-Bold.ttf"] * 2)
BAS = bloc(["Méditation sommeil complète (11 min)", "sur la chaîne", "contactapaisement-mental.fr"], [42, 36, 34],
           [(250, 246, 236, 255), (215, 222, 248, 255), (255, 214, 140, 240)], ["Lora-SemiBold.ttf", "Lora-Regular.ttf", "Lora-Regular.ttf"], fond_=(8, 10, 30, 170))
SITE = bloc(["contactapaisement-mental.fr"], [34], [(225, 228, 245, 230)], ["Lora-Regular.ttf"])


def sous(txt):
    f = police("Lora-Regular.ttf", 50)
    mots, lignes, cur = txt.split(), [], ""
    for m in mots:
        e = (cur + " " + m).strip()
        if f.getlength(e) > 880 and cur: lignes.append(cur); cur = m
        else: cur = e
    lignes.append(cur)
    lh = 68; larg = int(max(f.getlength(l) for l in lignes)) + 70; ht = lh * len(lignes) + 36
    im = Image.new("RGBA", (larg, ht), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, larg - 1, ht - 1], radius=26, fill=(6, 8, 24, 165))
    for i, l in enumerate(lignes):
        d.text((larg / 2, 18 + lh * i + lh / 2), l, font=f, fill=(246, 242, 232, 255), anchor="mm")
    return np.array(im, np.float32)


CACHE = {}


def poser(img, arr, x, y, al):
    if al <= 0.003: return
    h, w = arr.shape[:2]; z = img[y:y + h, x:x + w]; a = arr[..., 3:4] / 255 * al
    z *= 1 - a; z += arr[..., :3] * a


def cercle(r, txt):
    Z = 900; im = Image.new("RGBA", (Z, Z), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = Z // 2
    d.ellipse([c - r - 34, c - r - 34, c + r + 34, c + r + 34], fill=(150, 170, 255, 85)); im = im.filter(ImageFilter.GaussianBlur(36))
    d = ImageDraw.Draw(im)
    d.ellipse([c - r, c - r, c + r, c + r], fill=(150, 165, 240, 48), outline=(232, 236, 255, 230), width=4)
    if txt: d.text((c, c), txt, font=police("PlayfairDisplay-Bold.ttf", 64), fill=(252, 248, 236, 245), anchor="mm")
    return np.array(im, np.float32)


NP = 45
PX, PY, PV, PPH = rng.uniform(0, W, NP), rng.uniform(0, H, NP), rng.uniform(8, 22, NP), rng.uniform(0, 6.28, NP)
SP = np.exp(-((np.mgrid[0:25, 0:25] - 12) ** 2).sum(0) / (2 * 3.2 ** 2)).astype(np.float32)


def image(t):
    img = fond(t)
    for i in range(NP):
        x = int((PX[i] + 20 * math.sin(t * 0.15 + PPH[i])) % W); y = int((PY[i] - PV[i] * (t - D0)) % (H + 40) - 20)
        if 0 <= x < W - 25 and 0 <= y < H - 25:
            img[y:y + 25, x:x + 25] += SP[..., None] * np.array([255, 226, 170]) * 0.5 * (0.6 + 0.4 * math.sin(t + PPH[i] * 3))
    poser(img, HAUT, 0, 90, fondu(t, D0 + 0.2, D1 + 9, 0.8))
    cyc = 10.0; u = (t - S["debut"]) % cyc if t >= S["debut"] else 0
    fin = S["debut"] + S["cycles"] * cyc
    if t < S["debut"]: r, txt = 130, ""
    elif t > fin: r, txt = 130, ""
    elif u < 4: r, txt = 130 + 170 * lisse(u / 4), "Inspire"
    else: r, txt = 300 - 170 * lisse((u - 4) / 6), "Expire"
    poser(img, cercle(int(r), txt), (W - 900) // 2, 760 - 450, fondu(t, D0 + 1, D1 + 9, 1.2))
    for c in TL["cues"]:
        if D0 - 1 < c["debut"] < D1 and c["texte"] not in ("Inspire…", "Expire…") and c["debut"] - 0.3 < t < c["fin"] + 0.9:
            if c["texte"] not in CACHE: CACHE[c["texte"]] = sous(c["texte"])
            arr = CACHE[c["texte"]]
            poser(img, arr, (W - arr.shape[1]) // 2, 1110, fondu(t, c["debut"] - 0.2, c["fin"] + 0.7, 0.35))
    poser(img, BAS, 0, 1440, fondu(t, D0 + 1.5, D1 + 9, 0.8))
    img *= min(1, (t - D0) / 0.6) * min(1, (D1 - t) / 1.0)
    return img.clip(0, 255).astype(np.uint8)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        Image.fromarray(image(float(sys.argv[1]))).save(sys.argv[2], quality=88); sys.exit()
    dur = D1 - D0
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-ss", f"{D0:.3f}", "-t", f"{dur:.3f}", "-i", f"{ICI}/piste.wav",
                          "-af", f"afade=t=in:d=0.6,afade=t=out:st={dur - 1.5:.3f}:d=1.5",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", f"{ICI}/short-respiration.mp4"], stdin=subprocess.PIPE)
    for i in range(int(dur * FPS)):
        p.stdin.write(image(D0 + i / FPS).tobytes())
    p.stdin.close(); p.wait(); print("fini", dur)
