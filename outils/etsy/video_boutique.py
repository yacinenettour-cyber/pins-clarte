"""Vidéo de présentation de la boutique Etsy HestiaAura (05/11/2026, Etsy demande une vidéo de présentation).
Fabriquée par programme (PIL + ffmpeg), sans IA ni outil payant : logo et bannière de l'utilisateur (faits avec ChatGPT), pages du planner
(etsy/planner-charge-mentale/fiche-*.jpg), vrais bols chantants CC0 (site/sources-audio/bols). Aucun lien ni adresse dans l'image.
Sortie : etsy/boutique/video-hestiaaura-presentation.mp4 (1920 × 1080, 25 images/s, ~30 s, audio AAC)."""
import os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
P = lambda *a: os.path.join(RACINE, *a)
W, H, FPS = 1920, 1080, 25
CREME = (247, 240, 228); BRUN = (74, 52, 36); ROSE = (196, 120, 116); TERRA = (146, 70, 52); OR = (226, 196, 150)
f = lambda n, t: ImageFont.truetype(P("polices", n), t)

def fond_flou(img):
    r = max(W / img.width, H / img.height)
    b = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
    b = b.crop(((b.width - W) // 2, (b.height - H) // 2, (b.width - W) // 2 + W, (b.height - H) // 2 + H))
    b = b.filter(ImageFilter.GaussianBlur(40))
    return Image.blend(b, Image.new("RGB", (W, H), CREME), 0.45)

def scene_fiche(chemin):
    img = Image.open(chemin).convert("RGB")
    bg = fond_flou(img)
    hh = 1000; ww = int(img.width * hh / img.height)
    fg = img.resize((ww, hh), Image.LANCZOS)
    ombre = Image.new("L", (W, H), 0); x0 = (W - ww) // 2; y0 = (H - hh) // 2
    ImageDraw.Draw(ombre).rectangle((x0 + 8, y0 + 14, x0 + ww + 8, y0 + hh + 14), fill=110)
    bg.paste((90, 70, 55), (0, 0), ombre.filter(ImageFilter.GaussianBlur(22)))
    bg.paste(fg, (x0, y0))
    return bg

def centre(d, y, t, fo, fill, x0=0, x1=W):
    d.text((x0 + (x1 - x0 - d.textlength(t, font=fo)) / 2, y), t, font=fo, fill=fill)

def scene_ouverture():
    logo = Image.open(P("etsy", "boutique", "logo-hestiaaura-chatgpt-2000.png")).convert("RGB")
    bg = Image.new("RGB", (W, H), TERRA)
    # fond dégradé terracotta
    import numpy as np
    yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W * 0.3) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.8)) ** 2)
    a = np.clip(np.array([166, 82, 58]) * (1 - 0.45 * np.clip(r - 0.15, 0, 1.2))[..., None], 0, 255).astype("uint8"); bg = Image.fromarray(a)
    t = 860; lg = logo.resize((t, t), Image.LANCZOS)
    m = Image.new("L", (t * 3, t * 3), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, t * 3 - 1, t * 3 - 1), 90, fill=255); m = m.resize((t, t), Image.LANCZOS)
    ombre = Image.new("L", (W, H), 0); ImageDraw.Draw(ombre).rounded_rectangle((150 + 6, 110 + 16, 150 + t + 6, 110 + t + 16), 45, fill=150)
    bg.paste((50, 20, 12), (0, 0), ombre.filter(ImageFilter.GaussianBlur(26))); bg.paste(lg, (150, 110), m)
    d = ImageDraw.Draw(bg); x0 = 1060
    d.text((x0, 300), "HestiaAura", font=f("PlayfairDisplay-Bold.ttf", 118), fill=CREME)
    d.line((x0 + 4, 450, x0 + 360, 450), fill=OR, width=3)
    d.text((x0, 490), "Poser ce qui tourne dans la tête,", font=f("DancingScript-Bold.ttf", 68), fill=OR)
    d.text((x0, 570), "et mieux le partager.", font=f("DancingScript-Bold.ttf", 68), fill=OR)
    d.text((x0 + 4, 720), "Planners à imprimer, en français", font=f("Lora-Regular.ttf", 40), fill=(240, 220, 205))
    return bg

def scene_fin():
    ban = Image.open(P("etsy", "boutique", "banniere-hestiaaura-chatgpt-3360x840.jpg")).convert("RGB")
    bg = fond_flou(ban); d = ImageDraw.Draw(bg)
    bw = W; bh = int(ban.height * bw / ban.width)
    bg.paste(ban.resize((bw, bh), Image.LANCZOS), (0, 130))
    centre(d, 700, "Planners à imprimer : la charge mentale, enfin partagée", f("PlayfairDisplay-Bold.ttf", 62), BRUN)
    centre(d, 800, "Téléchargement immédiat  ·  PDF en français  ·  prêt pour le classeur", f("Lora-Regular.ttf", 40), (110, 85, 70))
    return bg

SCENES = [
    (scene_ouverture(), 5.0),
    (scene_fiche(P("etsy", "planner-charge-mentale", "fiche-01-couverture.jpg")), 4.6),
    (scene_fiche(P("etsy", "planner-charge-mentale", "fiche-02-volet-a-deux.jpg")), 4.6),
    (scene_fiche(P("etsy", "planner-charge-mentale", "fiche-04-kit-frigo.jpg")), 4.6),
    (scene_fiche(P("etsy", "planner-charge-mentale", "fiche-05-tablette-cliquable.jpg")), 4.6),
    (scene_fiche(P("etsy", "planner-charge-mentale", "fiche-06-exemple-rempli.jpg")), 4.6),
    (scene_fin(), 5.4),
]
XF = 0.8  # fondu enchaîné

def fabriquer(sortie):
    tmp = tempfile.mkdtemp(); cmd = ["ffmpeg", "-y", "-loglevel", "error"]; filtres = []; n = len(SCENES)
    for i, (img, dur) in enumerate(SCENES):
        img.save(os.path.join(tmp, f"s{i}.png"))
        cmd += ["-loop", "1", "-t", f"{dur + XF:.2f}", "-i", os.path.join(tmp, f"s{i}.png")]
        # lent zoom avant (ouverture et fin : plus discret)
        z = 0.0005 if i in (0, n - 1) else 0.0009
        filtres.append(f"[{i}:v]scale=2400:-1,zoompan=z='min(1+{z}*on,1.09)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},format=yuv420p[v{i}]")
    # enchaînement xfade
    cur = "v0"; t = SCENES[0][1]
    for i in range(1, n):
        filtres.append(f"[{cur}][v{i}]xfade=transition=fade:duration={XF}:offset={t - XF + XF:.2f}[x{i}]" if False else f"[{cur}][v{i}]xfade=transition=fade:duration={XF}:offset={t:.2f}[x{i}]")
        cur = f"x{i}"; t += SCENES[i][1]
    total = t + XF
    cmd += ["-i", P("site", "sources-audio", "bols", "bol-tibetain-long_itinerantmonk108_553049.ogg"),
            "-i", P("site", "sources-audio", "bols", "bol-maillet-doux_steffcaffrey_449951.ogg")]
    filtres.append(f"[{n}:a]atrim=0:7,afade=t=out:st=4:d=3,volume=0.55,aformat=sample_rates=44100:channel_layouts=stereo[a0]")
    filtres.append(f"[{n+1}:a]atrim=0:6,afade=t=out:st=3:d=3,volume=0.6,adelay={int((total-6.4)*1000)}|{int((total-6.4)*1000)},aformat=sample_rates=44100:channel_layouts=stereo[a1]")
    filtres.append("[a0][a1]amix=inputs=2:duration=longest:normalize=0,afade=t=in:st=0:d=0.4[a]")
    cmd += ["-filter_complex", ";".join(filtres), "-map", f"[{cur}]", "-map", "[a]", "-t", f"{total:.2f}",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", sortie]
    subprocess.run(cmd, check=True)
    return total

if __name__ == "__main__":
    out = P("etsy", "boutique", "video-hestiaaura-presentation.mp4")
    print("durée :", round(fabriquer(out), 1), "s ->", out)
