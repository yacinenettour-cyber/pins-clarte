"""Logo et bannière Etsy « Clarté Mentale » (05/11/2026, retour de la boutique au nom Clarté Mentale).
Symbole : une fenêtre en arche où le soleil se lève sur une eau calme (la clarté qui revient dans une tête apaisée),
halo doré autour, terracotta et or comme le planner. Nom « Clarté » en Playfair et « Mentale » en Dancing Script.
Dessiné en SVG par programme (aucune IA, rien de payant), rendu en PNG/JPG par Chromium (Playwright).
Usage : python3 outils/etsy/logo_clarte_mentale.py  → etsy/boutique/logo-clarte-mentale-*.png/.svg, banniere-clarte-mentale-3360x840.jpg"""
import math, os, pathlib
import json, subprocess, tempfile

RACINE = pathlib.Path(__file__).resolve().parents[2]
SORTIE = RACINE / "etsy" / "boutique"
POL = (RACINE / "polices").as_uri() + "/"
BG1, BG2 = "#9a4c37", "#6f3223"
OR, OR2, CREME = "#e6c48f", "#c99c5c", "#f7f0e4"
TERRA, BRUN = "#96483a", "#5a3a2c"

def polices():
    return (f"@font-face{{font-family:PF;src:url({POL}PlayfairDisplay-Bold.ttf)}}"
            f"@font-face{{font-family:DS;src:url({POL}DancingScript-Bold.ttf)}}"
            f"@font-face{{font-family:LO;src:url({POL}Lora-SemiBold.ttf)}}")

def defs():
    return (f'<radialGradient id="bg" cx="50%" cy="42%" r="75%"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></radialGradient>'
            '<radialGradient id="lueur"><stop offset="0" stop-color="#f6d9a0" stop-opacity="0.6"/><stop offset="1" stop-color="#f6d9a0" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="soleil" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{OR2}"/><stop offset="1" stop-color="#f3dcae"/></linearGradient>'
            f'<style>{polices()}</style>')

def symbole(cx=500, cy=500, s=1.0, trait=CREME, dore=OR, halo=True):
    """Arche + soleil levant + rayons + eau calme, centré sur (cx, cy), dans une boîte d'environ 820 px à l'échelle 1."""
    o = []
    if halo:
        for r, w, op in ((338, 4.2, 0.95), (372, 2.8, 0.7), (404, 2.0, 0.45)):
            o.append(f'<circle cx="0" cy="0" r="{r}" fill="none" stroke="{dore}" stroke-width="{w}" opacity="{op}"/>')
        for ang, r, rad in ((-90, 404, 6), (-60, 372, 5), (-120, 372, 5), (-30, 338, 4.5), (-150, 338, 4.5), (15, 404, 4), (165, 404, 4)):
            o.append(f'<circle cx="{r*math.cos(math.radians(ang)):.1f}" cy="{r*math.sin(math.radians(ang)):.1f}" r="{rad}" fill="{dore}"/>')
    # arche (fenêtre)
    r, top, bas = 165, -248, 242
    o.append(f'<path d="M{-r},{bas} L{-r},{top+r} A{r},{r} 0 0 1 {r},{top+r} L{r},{bas}" fill="none" stroke="{trait}" stroke-width="9" stroke-linecap="round"/>')
    r2 = 144
    o.append(f'<path d="M{-r2},{bas} L{-r2},{top+21+r2} A{r2},{r2} 0 0 1 {r2},{top+21+r2} L{r2},{bas}" fill="none" stroke="{dore}" stroke-width="3" stroke-linecap="round"/>')
    hor = 70  # ligne d'horizon
    o.append(f'<circle cx="0" cy="{hor-10}" r="150" fill="url(#lueur)"/>')
    # rayons
    for a in range(-160, -15, 18):
        x1, y1 = 92 * math.cos(math.radians(a)), hor + 92 * math.sin(math.radians(a))
        x2, y2 = 128 * math.cos(math.radians(a)), hor + 128 * math.sin(math.radians(a))
        o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{dore}" stroke-width="5" stroke-linecap="round"/>')
    # soleil (demi-disque)
    o.append(f'<path d="M-72,{hor} A72,72 0 0 1 72,{hor} Z" fill="url(#soleil)"/>')
    o.append(f'<line x1="{-r2+6}" y1="{hor}" x2="{r2-6}" y2="{hor}" stroke="{trait}" stroke-width="6" stroke-linecap="round"/>')
    # eau calme : trois traits ondulés de plus en plus courts
    for i, (lg, y) in enumerate(((210, hor + 44), (150, hor + 84), (90, hor + 122))):
        h = lg / 2
        o.append(f'<path d="M{-h},{y} q{h/4},-12 {h/2},0 t{h/2},0 t{h/2},0 t{h/2},0" fill="none" stroke="{dore if i else trait}" '
                 f'stroke-width="{5 if i==0 else 4}" stroke-linecap="round" opacity="{1 - 0.2*i}"/>')
    # seuil
    o.append(f'<path d="M-205,{bas} L205,{bas}" stroke="{trait}" stroke-width="9" stroke-linecap="round"/>')
    o.append(f'<path d="M-125,{bas+32} L125,{bas+32}" stroke="{dore}" stroke-width="3" stroke-linecap="round"/>')
    return f'<g transform="translate({cx},{cy}) scale({s})">{"".join(o)}</g>'

def logo(variante):
    if variante == "icone":
        corps = symbole(500, 500, 1.0)
    else:
        corps = (symbole(500, 450, 0.84)
                 + f'<text x="500" y="890" text-anchor="middle" font-family="PF" font-size="92" letter-spacing="4" fill="{CREME}">Clarté'
                   f'<tspan font-family="DS" font-size="108" fill="{OR}" dx="18">Mentale</tspan></text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" viewBox="0 0 1000 1000"><defs>{defs()}</defs>'
            f'<rect width="1000" height="1000" fill="url(#bg)"/>{corps}</svg>')

def brin(x, y, sens, coul, n=6, h=300):
    """Brin de feuillage au trait fin (même famille que le planner)."""
    o = [f'<path d="M{x},{y} q{sens*40},{-h/2} {sens*10},{-h}" fill="none" stroke="{coul}" stroke-width="4" stroke-linecap="round"/>']
    for k in range(n):
        t = (k + 1) / (n + 1)
        px, py = x + sens * 40 * 2 * t * (1 - t) + sens * 10 * t * t, y - h * t
        for c in (-1, 1):
            ang = -90 + c * 48
            L = 70 - 30 * t
            ex, ey = px + L * math.cos(math.radians(ang)), py + L * math.sin(math.radians(ang))
            mx, my = (px + ex) / 2, (py + ey) / 2
            nx, ny = -(ey - py) * 0.28, (ex - px) * 0.28
            o.append(f'<path d="M{px:.1f},{py:.1f} Q{mx+nx:.1f},{my+ny:.1f} {ex:.1f},{ey:.1f} Q{mx-nx:.1f},{my-ny:.1f} {px:.1f},{py:.1f} Z" '
                     f'fill="none" stroke="{coul}" stroke-width="3.2"/>')
    return "".join(o)

def banniere():
    W, H = 3360, 840
    sauge = "#8fa38a"
    medaillon = (f'<circle cx="0" cy="0" r="300" fill="url(#bg)"/>' + symbole(0, 0, 0.62))
    corps = (f'<rect width="{W}" height="{H}" fill="url(#papier)"/>'
             f'<rect x="28" y="28" width="{W-56}" height="{H-56}" fill="none" stroke="{OR2}" stroke-width="3" opacity="0.6"/>'
             + brin(330, 760, 1, TERRA) + brin(400, 770, -1, sauge, h=260)
             + brin(W-330, 760, -1, TERRA) + brin(W-400, 770, 1, sauge, h=260)
             + f'<g transform="translate(830,420)">{medaillon}</g>'
             f'<text x="1180" y="380" font-family="PF" font-size="176" letter-spacing="6" fill="{TERRA}">Clarté'
             f'<tspan font-family="DS" font-size="196" fill="{OR2}" dx="34">Mentale</tspan></text>'
             f'<line x1="1190" y1="450" x2="2560" y2="450" stroke="{OR2}" stroke-width="3"/>'
             f'<path d="M1875,436 l14,14 l-14,14 l-14,-14 Z" fill="{OR2}"/>'
             f'<text x="1190" y="570" font-family="LO" font-size="62" fill="{BRUN}">Planners à imprimer : la charge mentale, enfin partagée</text>'
             f'<text x="1190" y="680" font-family="LO" font-size="46" letter-spacing="12" fill="#8a6a58">SEUL(E)  ·  À DEUX  ·  EN FAMILLE</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>{defs()}'
            f'<radialGradient id="papier" cx="45%" cy="45%" r="75%"><stop offset="0" stop-color="#fbf6ec"/><stop offset="1" stop-color="#efe5d5"/></radialGradient>'
            f'</defs>{corps}</svg>')

def rendre(svg, w, h, chemin, scale=1, qualite=None):
    """Rendu par Chromium via le Playwright de Node (préinstallé dans l'environnement)."""
    html = pathlib.Path(tempfile.mkdtemp()) / "page.html"
    html.write_text(f"<html><body style='margin:0'>{svg}</body></html>")
    opts = {"path": str(chemin), "clip": {"x": 0, "y": 0, "width": w, "height": h}}
    if qualite: opts.update(type="jpeg", quality=qualite)
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();"
          f"const p=await b.newPage({{viewport:{{width:{w},height:{h}}},deviceScaleFactor:{scale}}});"
          f"await p.goto({json.dumps(html.as_uri())});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);"
          f"await p.screenshot({json.dumps(opts)});await b.close();}})();")
    subprocess.run(["node", "-e", js], check=True)

if __name__ == "__main__":
    from PIL import Image
    for v in ("icone", "nom"):
        s = logo(v)
        (SORTIE / f"logo-clarte-mentale-{v}.svg").write_text(s)
        grand = SORTIE / f"logo-clarte-mentale-{v}-2000.png"
        rendre(s, 1000, 1000, grand, scale=2)
        Image.open(grand).resize((500, 500), Image.LANCZOS).save(SORTIE / f"logo-clarte-mentale-{v}-500.png")
    s = banniere()
    (SORTIE / "banniere-clarte-mentale.svg").write_text(s)
    rendre(s, 3360, 840, SORTIE / "banniere-clarte-mentale-3360x840.jpg", qualite=92)
    print("ok")
