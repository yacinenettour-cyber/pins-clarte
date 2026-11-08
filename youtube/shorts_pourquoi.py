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
    """Alignement mot par mot : les passages parlés entre deux silences réels sont attribués, dans l'ordre, à des suites
    de mots qui finissent sur une ponctuation ; on minimise l'écart entre la durée parlée et la durée attendue
    (programmation dynamique). Renvoie les bornes de chaque phrase, la durée totale et le temps de chaque mot."""
    total = duree(f)
    tous = silences(f)
    t0 = next((s[1] for s in tous if s[0] < 0.05), 0.0)
    fin_voix = max((s[0] for s in tous if s[1] >= total - 0.05), default=total)
    sil = [s for s in tous if t0 + 0.15 < s[0] < fin_voix - 0.15]
    blocs, deb = [], t0
    for (a, b) in sil:
        blocs.append((deb, a)); deb = b
    blocs.append((deb, fin_voix))
    ms, phr = [], []
    for k, p in enumerate(phrases):
        for m in mots(p["texte"]):
            ms.append(m); phr.append(k)
    w = [poids(m) for m in ms]
    pause = [bool(re.search(r"[,:;.?!]$", m)) for m in ms]
    pause[-1] = True
    debit = sum(b - a for a, b in blocs) / sum(w)
    N, B = len(ms), len(blocs)
    INF = float("inf")
    cout = [[INF] * (N + 1) for _ in range(B + 1)]
    prec = [[None] * (N + 1) for _ in range(B + 1)]
    cout[0][0] = 0.0
    pref = [0]
    for x in w:
        pref.append(pref[-1] + x)
    for i in range(1, B + 1):
        d = blocs[i - 1][1] - blocs[i - 1][0]
        for j in range(1, N + 1):
            for k in range(0, j):
                if cout[i - 1][k] == INF:
                    continue
                att = (pref[j] - pref[k]) * debit
                c = cout[i - 1][k] + ((d - att) / max(att, 0.4)) ** 2 + (0 if pause[j - 1] else 0.8)
                if c < cout[i][j]:
                    cout[i][j] = c; prec[i][j] = k
    assert cout[B][N] < INF, "alignement impossible"
    coupes, j = [], N
    for i in range(B, 0, -1):
        k = prec[i][j]; coupes.append((k, j)); j = k
    coupes.reverse()
    temps = [None] * N
    for (k, j), (a, b) in zip(coupes, blocs):
        tot = pref[j] - pref[k]; t = a
        for q in range(k, j):
            dd = (b - a) * w[q] / tot; temps[q] = (ms[q], t, t + dd); t += dd
    bornes = []
    for k in range(len(phrases)):
        idx = [q for q in range(N) if phr[q] == k]
        bornes.append((temps[idx[0]][1], temps[idx[-1]][2]))
    return bornes, total, temps, phr


def mots(texte):
    """Mots du texte ; la ponctuation isolée (« : », « ? ») reste collée au mot précédent."""
    out = []
    for m in texte.split():
        if out and re.fullmatch(r"[:;?!.,»]+", m):
            out[-1] += "\u00a0" + m
        else:
            out.append(m)
    return out


def poids(m):
    return max(2, len(re.sub(r"[^\wÀ-ÿ']", "", m))) + (3 if re.search(r"[,:;.?!]$", m) else 0)


def morceaux(temps):
    """Groupes de 1 à 3 mots (14 lettres environ) ; coupe après une ponctuation."""
    groupes, cur = [], []
    for (m, a, b) in temps:
        cur.append((m, a, b))
        long_ = sum(len(x[0]) for x in cur)
        if len(cur) >= 3 or long_ >= 14 or (len(cur) >= 2 and re.search(r"[,:;.?!]$", m)):
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


def fichier_ass(cfg, bornes, total, temps, phr, chemin):
    cles = [c.lower() for c in cfg["mots_cles"]]
    dur = total + FIN
    s = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 0", "",
         "[V4+ Styles]",
         "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
         "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
         "MarginR, MarginV, Encoding",
         # sous-titres : centrés, très gros, contour net ; 150 px libres à droite et à gauche, bien au-dessus des 250 px du bas
         "Style: Sous,Jost,138,&H00FFFFFF,&H00FFFFFF,&H00080808,&H90000000,-1,0,0,0,100,100,0,0,1,11,5,5,150,150,0,1",
         "Style: Accroche,Playfair Display,138,&H00FFFFFF,&H00FFFFFF,&H00101010,&H80000000,-1,0,0,0,100,100,0,0,1,10,5,5,110,150,0,1",
         "Style: Bandeau,Jost,56,&H0022262A,&H00FFFFFF,&H0083C8F2,&H0083C8F2,-1,0,0,0,100,100,6,0,3,18,0,8,150,150,200,1",
         "Style: Fin,Playfair Display,110,&H00FFFFFF,&H00FFFFFF,&H00101010,&H78000000,-1,0,0,0,100,100,0,0,1,7,2,5,130,130,0,1",
         "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    s.append(f"Dialogue: 2,{ass_t(0)},{ass_t(dur)},Bandeau,,0,0,0,,POURQUOI ? N° {cfg['numero']}")
    s.append(f"Dialogue: 3,{ass_t(0)},{ass_t(2.2)},Accroche,,0,0,0,,{{\\fad(0,250)}}{echap(cfg['accroche'])}")
    for k in range(len(cfg["phrases"])):
        for g in morceaux([t for t, p in zip(temps, phr) if p == k]):
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
    s.append(f"Dialogue: 3,{ass_t(total + 0.05)},{ass_t(dur)},Fin,,0,0,0,,{{\\fad(150,0)}}Abonne-toi\\N{{\\fs84\\c&H0047C8FF&}}la série continue")
    open(chemin, "w").write("\n".join(s) + "\n")


def plans(cfg, bornes, total, clips, travail):
    """Un segment par plan : chaque phrase est partagée entre ses clips, tranches de 1,6 à 3,2 s."""
    seg = []
    debuts = [0.0] + [a for a, _ in bornes[1:]] + [total + FIN]
    for k, ph in enumerate(cfg["phrases"]):
        cl = ph["clips"]; d = debuts[k + 1] - debuts[k]; n = max(len(cl), round(d / 2.6))
        for q in range(n):
            seg.append([cl[q % len(cl)], d / n])
    deja = {}
    sorties = []
    t_cum = 0.0
    for i, (c, d) in enumerate(seg):
        f = os.path.join(clips, f"{c}.mp4"); dc = duree(f)
        off = deja.get(c, 0.0)
        if off + d > dc - 0.1:
            off = 0.0
        deja[c] = off + d
        nb = max(1, round((t_cum + d) * FPS) - round(t_cum * FPS)); t_cum += d
        z = f"1.0+0.07*on/{nb}" if i % 2 == 0 else f"1.07-0.07*on/{nb}"  # alternance zoom avant / arrière
        vf = (f"fps={FPS},scale={W * 3 // 2}:{H * 3 // 2}:force_original_aspect_ratio=increase,"
              f"crop={W * 3 // 2}:{H * 3 // 2},"
              f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
              "eq=brightness=-0.035:contrast=1.06:saturation=0.86,"
              "colorbalance=rs=0.05:gs=0.01:bs=-0.06:rm=0.04:bm=-0.04,vignette=PI/5,format=yuv420p")
        o = os.path.join(travail, f"p{i:02d}.mp4")
        sh("ffmpeg", "-y", "-stream_loop", "-1", "-ss", f"{off:.3f}", "-i", f, "-an", "-vf", vf, "-c:v", "libx264",
           "-preset", "medium", "-crf", "17", "-frames:v", str(nb), "-r", str(FPS), o)
        assert abs(duree(o) - nb / FPS) < 0.05, ("plan trop court", c, duree(o), nb / FPS)
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
    bornes, total, temps, phr = minutage(cfg["phrases"], v)
    fond, seg = plans(cfg, bornes, total, clips, travail)
    a = os.path.join(travail, "s.ass")
    fichier_ass(cfg, bornes, total, temps, phr, a)
    dur = total + FIN
    musique = ["-stream_loop", "-1", "-i", MUSIQUE] if os.path.exists(MUSIQUE) else []
    filt = (f"[0:v]drawbox=x=0:y=0:w=iw:h=ih:color=black@0.45:t=fill:enable='lt(t,2.2)+gte(t,{total:.2f})',"
            f"ass={a}:fontsdir={POL}[v];"
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
