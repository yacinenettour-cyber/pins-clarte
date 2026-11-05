"""Logo HestiaAura (05/11/2026, « fais un effort pour le logo ») : flamme de foyer (Hestia, déesse du foyer) dans une arche,
entourée d'un halo (l'aura), terracotta et or, nom « Hestia » en Playfair et « Aura » en Dancing Script. Dessiné en SVG par
programme (aucune IA, rien de payant) puis rendu en PNG 2000 px par Chromium (Playwright), réduit à 500 px.
Usage : python3 outils/etsy/logo_hestiaaura.py écrit hestiaaura-mark.svg/.html et hestiaaura-nom.svg/.html dans le dossier courant ;
ouvrir chaque .html dans Chromium à 1000 × 1000 (facteur d'échelle 2) et capturer l'écran ; les fichiers finaux sont dans etsy/boutique/.
Les polices sont lues dans polices/ (OFL), chemin relatif au dossier de travail à adapter si besoin."""
import sys, json
POL="file://../../polices/"
BG1,BG2="#9a4c37","#6f3223"   # terracotta (dégradé radial)
OR="#e6c48f"; OR2="#c99c5c"; CREME="#f7f0e4"
def flamme(cx,cy,s,fill_ext,fill_int):
    # flamme à deux lobes, dessinée dans une boîte de ~200 x 330 centrée sur (cx,cy), échelle s
    ext=("M0,-165 C14,-118 70,-78 84,-8 C98,66 54,150 0,165 C-54,150 -98,66 -84,-8 C-76,-46 -48,-70 -34,-104 "
         "C-22,-80 -10,-72 2,-72 C-8,-104 -8,-136 0,-165 Z")
    inte=("M0,-28 C10,-2 40,22 40,62 C40,104 18,132 0,142 C-18,132 -40,104 -40,62 C-40,32 -16,14 -8,-6 C-4,6 -2,8 2,8 C-2,-8 -4,-16 0,-28 Z")
    return (f'<g transform="translate({cx},{cy}) scale({s})">'
            f'<path d="{ext}" fill="{fill_ext}"/><path d="{inte}" fill="{fill_int}"/></g>')
def halo(cx,cy):
    out=[]
    # arcs de halo : 3 cercles partiels, de plus en plus fins et discrets
    import math
    for r,w,o,gap in ((338,4.2,0.95,0),(372,2.8,0.75,0),(404,2.0,0.5,0)):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{OR}" stroke-width="{w}" opacity="{o}"/>')
    # petits points de lumière sur le halo
    for ang,r,rad in ((-60,372,6),(-120,372,6),(-90,404,5),(-35,338,4.5),(-145,338,4.5),(20,404,4),(160,404,4),(-12,372,4),(192,372,4)):
        x=cx+r*math.cos(math.radians(ang)); y=cy+r*math.sin(math.radians(ang))
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="{OR}"/>')
    return "".join(out)
def arche(cx,top,bas,larg,col,w):
    r=larg/2
    return f'<path d="M{cx-r},{bas} L{cx-r},{top+r} A{r},{r} 0 0 1 {cx+r},{top+r} L{cx+r},{bas}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
def svg(variante):
    cx=500
    icone=(halo(cx,500)+arche(cx,252,742,330,CREME,9)+arche(cx,276,742,288,OR,3)
           +f'<circle cx="{cx}" cy="560" r="190" fill="url(#lueur)"/>'
           +flamme(cx,548,1.12,"url(#feu)",CREME)
           +f'<path d="M{cx-205},742 L{cx+205},742" stroke="{CREME}" stroke-width="9" stroke-linecap="round"/>'
           +f'<path d="M{cx-125},774 L{cx+125},774" stroke="{OR}" stroke-width="3" stroke-linecap="round"/>')
    if variante=="mark":   # icône seule, plus grande
        corps=f'<g transform="translate(500,500) scale(1.0) translate(-500,-500)">{icone}</g>'
    else:                  # avec nom
        corps=(f'<g transform="translate(500,462) scale(0.86) translate(-500,-500)">{icone}</g>'
               f'<text x="500" y="884" text-anchor="middle" font-family="PF" font-size="92" letter-spacing="6" fill="{CREME}">Hestia<tspan font-family="DS" font-size="112" fill="{OR}" dx="8">Aura</tspan></text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" viewBox="0 0 1000 1000">
<defs>
<radialGradient id="bg" cx="50%" cy="42%" r="75%"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></radialGradient>
<radialGradient id="lueur"><stop offset="0" stop-color="#f6d9a0" stop-opacity="0.55"/><stop offset="1" stop-color="#f6d9a0" stop-opacity="0"/></radialGradient>
<linearGradient id="feu" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{OR2}"/><stop offset="1" stop-color="#f1d9ab"/></linearGradient>
<style>
@font-face{{font-family:PF;src:url({POL}PlayfairDisplay-Bold.ttf)}}
@font-face{{font-family:DS;src:url({POL}DancingScript-Bold.ttf)}}
</style></defs>
<rect width="1000" height="1000" fill="url(#bg)"/>
{corps}
</svg>'''
for v in ("mark","nom"):
    open(f"hestiaaura-{v}.html","w").write(f"<html><body style='margin:0;background:#fff'>{svg(v)}</body></html>")
    open(f"hestiaaura-{v}.svg","w").write(svg(v))
print("ok")
