"""Shorts « Pourquoi… ? » (série lancée le 08/11/2026) : plans filmés libres (Mixkit), voix ElevenLabs déjà générée,
sous-titres très gros mot par mot (libass), question d'accroche géante pendant les 2 premières secondes,
bandeau « POURQUOI ? n° X », coupe toutes les 2-3 s avec léger zoom, étalonnage chaud, voix à −14 LUFS.
Usage : python3 youtube/shorts_pourquoi.py <dossier videos_youtube/pourquoi-…> <dossier des clips> <sortie.mp4>
Le dossier contient voix.mp3 et short.json (numero, accroche, phrases [{texte, clips}], mots_cles, vitesse).
Minutage des mots : silences réels de la voix (silencedetect) pour les fins de phrase, puis partage de chaque
phrase selon la longueur des mots (pas de Whisper hors ligne dans le conteneur)."""
import json, os, re, subprocess, sys, tempfile

W, H, FPS = 1080, 1920, 30
POL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "polices")
MUSIQUE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site", "sources-audio", "deep-relaxation-extrait.mp3")
FIN = 1.2  # secondes d'image après la voix


def sh(*a):
    subprocess.run(a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def duree(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))


def voix(src, vitesse, dst):
    sh("ffmpeg", "-y", "-i", src, "-af", f"atempo={vitesse},loudnorm=I=-14:TP=-1.5:LRA=7", "-ar", "48000", dst)


def silences(f):
    err = subprocess.run(["ffmpeg", "-i", f, "-af", "silencedetect=noise=-38dB:d=0.12", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    deb = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    fin = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(deb, fin))


def minutage(phrases, f):
    """Début et fin de chaque phrase : on prend les plus longs silences comme frontières, dans l'ordre."""
    total = duree(f)
    sil = [s for s in silences(f) if 0.05 < s[0] < total - 0.3]
    n = len(phrases) - 1
    longs = sorted(sorted(sil, key=lambda s: s[1] - s[0], reverse=True)[:n])
    assert len(longs) == n, (len(longs), n)
    bornes, t0 = [], next((s[1] for s in silences(f) if s[0] < 0.05), 0.0)
    for (a, b) in longs:
        bornes.append((t0, a)); t0 = b
    fin_voix = max((s[0] for s in silences(f) if s[1] >= total - 0.05), default=total)
    bornes.append((t0, fin_voix))
    return bornes, total


def mots(texte):
    return texte.split()


def poids(m):
    return max(2, len(re.sub(r"[^\wÀ-ÿ']", "", m))) + (3 if re.search(r"[,:;.?!]$", m) else 0)


def morceaux(texte, t0, t1):
    """Groupes de 2 à 4 mots avec leur temps, partagés selon la longueur des mots."""
    ms = mots(texte); p = [poids(m) for m in ms]; tot = sum(p); t = t0; temps = []
    for m, q in zip(ms, p):
        d = (t1 - t0) * q / tot; temps.append((m, t, t + d)); t += d
    groupes, cur = [], []
    for (m, a, b) in temps:
        cur.append((m, a, b))
        long_ = sum(len(x[0]) for x in cur)
        if len(cur) >= 4 or long_ >= 16 or (len(cur) >= 2 and re.search(r"[,:;.?!]$", m)):
            groupes.append(cur); cur = []
    if cur:
        if groupes and len(cur) == 1 and sum(len(x[0]) for x in groupes[-1]) < 14:
            groupes[-1] += cur
        else:
            groupes.append(cur)
    return groupes


def ass_t(s):
    h = int(s // 3600); m = int(s % 3600 // 60); se = s % 60
    return f"{h}:{m:02d}:{se:05.2f}"


def echap(t):
    return t.replace("{", "(").replace("}", ")")


def fichier_ass(cfg, bornes, total, chemin):
    cles = [c.lower() for c in cfg["mots_cles"]]
    dur = total + FIN
    s = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 0", "",
         "[V4+ Styles]",
         "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
         "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
         "MarginR, MarginV, Encoding",
         # sous-titres : centrés, très gros, contour net ; 150 px libres à droite et à gauche, bien au-dessus des 250 px du bas
         "Style: Sous,Jost,92,&H00FFFFFF,&H00FFFFFF,&H00141414,&H64000000,-1,0,0,0,100,100,0,0,1,7,2,5,150,150,0,1",
         "Style: Accroche,Playfair Display,104,&H00FFFFFF,&H00FFFFFF,&H00101010,&H78000000,-1,0,0,0,100,100,0,0,1,8,3,8,120,120,330,1",
         "Style: Bandeau,Jost,42,&H0022262A,&H00FFFFFF,&H0083C8F2,&H0083C8F2,-1,0,0,0,100,100,6,0,3,14,0,8,150,150,190,1",
         "Style: Fin,Playfair Display,86,&H00FFFFFF,&H00FFFFFF,&H00101010,&H78000000,-1,0,0,0,100,100,0,0,1,7,2,5,130,130,0,1",
         "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    s.append(f"Dialogue: 2,{ass_t(0)},{ass_t(dur)},Bandeau,,0,0,0,,POURQUOI ? N° {cfg['numero']}")
    s.append(f"Dialogue: 3,{ass_t(0)},{ass_t(2.2)},Accroche,,0,0,0,,{{\\fad(0,250)}}{echap(cfg['accroche'])}")
    for ph, (a, b) in zip(cfg["phrases"], bornes):
        for g in morceaux(ph["texte"], a, b):
            deb, fin = g[0][1], g[-1][2]
            if fin <= 2.25:
                continue
            deb = max(deb, 2.25 if deb < 2.25 else deb)
            txt = []
            for (m, _, _) in g:
                nu = re.sub(r"[^\wÀ-ÿ'-]", "", m).lower()
                if any(nu == c or nu.startswith(c) for c in cles):
                    txt.append("{\\c&H0047C8FF&}" + echap(m) + "{\\c&H00FFFFFF&}")
                else:
                    txt.append(echap(m))
            s.append(f"Dialogue: 1,{ass_t(deb)},{ass_t(fin)},Sous,,0,0,0,,{{\\fscx92\\fscy92\\t(0,90,\\fscx100\\fscy100)}}" + " ".join(txt))
    s.append(f"Dialogue: 3,{ass_t(total + 0.05)},{ass_t(dur)},Fin,,0,0,0,,{{\\fad(150,0)}}Abonne-toi\\N{{\\fs58\\c&H0047C8FF&}}la série continue")
    open(chemin, "w").write("\n".join(s) + "\n")


def plans(cfg, bornes, total, clips, travail):
    """Un segment par plan : chaque phrase est partagée entre ses clips, tranches de 1,6 à 3,2 s."""
    seg = []
    for ph, (a, b) in zip(cfg["phrases"], bornes):
        cl = ph["clips"]; d = b - a; n = max(len(cl), round(d / 2.6))
        for k in range(n):
            seg.append([cl[k % len(cl)], d / n])
    seg[0][1] += bornes[0][0]
    seg[-1][1] += (total - bornes[-1][1]) + FIN
    deja = {}
    sorties = []
    for i, (c, d) in enumerate(seg):
        f = os.path.join(clips, f"{c}.mp4"); dc = duree(f)
        off = deja.get(c, 0.0)
        if off + d > dc - 0.1:
            off = 0.0
        deja[c] = off + d
        zin = i % 2 == 0  # alternance zoom avant / arrière
        z = f"(1.0+0.06*t/{d:.3f})" if zin else f"(1.06-0.06*t/{d:.3f})"
        vf = (f"scale={W}*{1.08}:{H}*{1.08}:force_original_aspect_ratio=increase,"
              f"crop={W}*{1.08}:{H}*{1.08},"
              f"scale=w='trunc({W}*1.08*{z}/2)*2':h=-2:eval=frame,crop={W}:{H},"
              "eq=brightness=-0.035:contrast=1.06:saturation=0.86,"
              "colorbalance=rs=0.05:gs=0.01:bs=-0.06:rm=0.04:bm=-0.04,vignette=PI/5,"
              f"fps={FPS},format=yuv420p")
        o = os.path.join(travail, f"p{i:02d}.mp4")
        sh("ffmpeg", "-y", "-ss", f"{off:.3f}", "-t", f"{d:.3f}", "-i", f, "-an", "-vf", vf, "-c:v", "libx264",
           "-preset", "medium", "-crf", "17", "-t", f"{d:.3f}", o)
        sorties.append(o)
    liste = os.path.join(travail, "liste.txt")
    open(liste, "w").write("".join(f"file '{o}'\n" for o in sorties))
    fond = os.path.join(travail, "fond.mp4")
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", liste, "-c", "copy", fond)
    return fond, seg


def fabriquer(dossier, clips, sortie):
    cfg = json.load(open(os.path.join(dossier, "short.json")))
    travail = tempfile.mkdtemp()
    v = os.path.join(travail, "voix.wav")
    voix(os.path.join(dossier, "voix.mp3"), cfg.get("vitesse", 1.18), v)
    bornes, total = minutage(cfg["phrases"], v)
    fond, seg = plans(cfg, bornes, total, clips, travail)
    a = os.path.join(travail, "s.ass")
    fichier_ass(cfg, bornes, total, a)
    dur = total + FIN
    musique = ["-stream_loop", "-1", "-i", MUSIQUE] if os.path.exists(MUSIQUE) else []
    filt = (f"[0:v]ass={a}:fontsdir={POL}[v];"
            f"[1:a]apad=pad_dur={FIN}[vo];")
    if musique:
        filt += f"[2:a]volume=0.05,afade=t=in:d=1,afade=t=out:st={dur - 1:.2f}:d=1[mu];[vo][mu]amix=inputs=2:duration=first:normalize=0[a]"
    else:
        filt += "[vo]anull[a]"
    sh("ffmpeg", "-y", "-i", fond, "-i", v, *musique, "-filter_complex", filt, "-map", "[v]", "-map", "[a]",
       "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", sortie)
    return {"duree": round(dur, 2), "plans": len(seg), "bornes": [(round(a, 2), round(b, 2)) for a, b in bornes]}


if __name__ == "__main__":
    print(json.dumps(fabriquer(*sys.argv[1:4]), ensure_ascii=False))
