# Génère les fiches HTML du kit à imprimer (une par fiche + le kit complet).
import os, html

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "html")
os.makedirs(OUT, exist_ok=True)

FONTS = "".join(
    f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{w};src:url('../fonts/{f}.woff2') format('woff2');}}\n"
    for fam, f, w, style in [
        ("Lora", "lora-latin-400-normal", 400, "normal"),
        ("Lora", "lora-latin-ext-400-normal", 400, "normal"),
        ("Lora", "lora-latin-400-italic", 400, "italic"),
        ("Lora", "lora-latin-600-normal", 600, "normal"),
        ("Lora", "lora-latin-ext-600-normal", 600, "normal"),
        ("Lora", "lora-latin-700-normal", 700, "normal"),
        ("Poppins", "poppins-latin-400-normal", 400, "normal"),
        ("Poppins", "poppins-latin-ext-400-normal", 400, "normal"),
        ("Poppins", "poppins-latin-500-normal", 500, "normal"),
        ("Poppins", "poppins-latin-ext-500-normal", 500, "normal"),
        ("Poppins", "poppins-latin-600-normal", 600, "normal"),
        ("Poppins", "poppins-latin-ext-600-normal", 600, "normal"),
    ]
)

CSS = FONTS + """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; font-family: 'Poppins', sans-serif; color: #26324F; font-size: 10.5pt; line-height: 1.45; }
.page { width: 210mm; height: 297mm; padding: 16mm 16mm 14mm; position: relative; page-break-after: always; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.tag { display: inline-block; font-size: 8pt; letter-spacing: .12em; text-transform: uppercase; color: #3D4F8F; background: #EEF2FA; padding: 3px 10px; border-radius: 20px; font-weight: 500; }
h1 { font-family: 'Lora', serif; font-weight: 600; font-size: 25pt; line-height: 1.15; margin: 8px 0 6px; color: #1F2A44; }
h2 { font-family: 'Lora', serif; font-weight: 600; font-size: 14pt; margin: 14px 0 6px; color: #1F2A44; }
.lead { font-size: 11pt; color: #4A5578; margin: 0 0 10px; }
.box { background: #F6F1E9; border-radius: 10px; padding: 10px 14px; margin: 10px 0; }
.box.blue { background: #EEF2FA; }
.box p { margin: 3px 0; }
table { width: 100%; border-collapse: collapse; margin-top: 8px; }
th { background: #3D4F8F; color: #fff; font-weight: 500; font-size: 8.5pt; padding: 6px 5px; text-align: left; }
th:first-child { border-top-left-radius: 6px; } th:last-child { border-top-right-radius: 6px; }
td { border-bottom: 1px solid #D5DBEA; padding: 5px; font-size: 9.5pt; vertical-align: top; }
td.c { text-align: center; }
.foot { position: absolute; left: 16mm; right: 16mm; bottom: 8mm; font-size: 7.5pt; color: #8A93AD; display: flex; justify-content: space-between; border-top: 1px solid #E3E7F1; padding-top: 5px; }
.steps { counter-reset: s; list-style: none; padding: 0; margin: 6px 0; }
.big .steps li { font-size: 12.5pt; padding: 10px 0 10px 44px; } .big .steps li::before { top: 10px; }
.steps li { counter-increment: s; position: relative; padding: 7px 0 7px 40px; border-bottom: 1px dashed #D5DBEA; }
.steps li::before { content: counter(s); position: absolute; left: 0; top: 6px; width: 27px; height: 27px; border-radius: 50%; background: #3D4F8F; color: #fff; font-weight: 600; text-align: center; line-height: 27px; font-size: 11pt; }
.steps li b { color: #1F2A44; }
.lines div { border-bottom: 1px solid #C9D0E2; height: 9.5mm; }
.cols { display: flex; gap: 10px; } .cols > div { flex: 1; }
.card { border: 1.5px solid #D5DBEA; border-radius: 10px; padding: 10px 12px; }
.card h3 { font-family: 'Lora', serif; font-size: 12.5pt; margin: 0 0 2px; color: #1F2A44; }
.card .dur { font-size: 8.5pt; color: #3D4F8F; font-weight: 600; text-transform: uppercase; letter-spacing: .08em; }
.card ul { padding-left: 16px; margin: 6px 0 0; } .card li { margin: 4px 0; font-size: 10.5pt; }
.grid td { text-align: center; height: 11mm; font-size: 12pt; }
.q td { height: 9.5mm; vertical-align: middle; }
.small { font-size: 8.5pt; color: #5A6484; }
.cover { background: #1F2A44; color: #fff; display: flex; flex-direction: column; justify-content: center; }
.cover h1 { color: #fff; font-size: 34pt; }
.cover .lead { color: #C9D3EE; font-size: 13pt; }
.cover ol { font-size: 12pt; line-height: 2; color: #E9EDF7; }
.compact td { padding: 2px 6px; font-size: 9.5pt; }
.quote { font-family: 'Lora', serif; font-style: italic; font-size: 12.5pt; color: #3D4F8F; margin: 10px 0; }
"""

FOOT = ('<div class="foot"><span>Clarté Mentale · « Quand le cerveau refuse de dormir »</span>'
        '<span>Outil de bien-être · ne remplace pas un avis médical</span></div>')


import re as _re
NBSP = lambda t: _re.sub(r'(\d) (min|h|°C|jours|semaines|mois|fois|zones|soupirs)', r'\1&nbsp;\2', t).replace(' ?', '&nbsp;?').replace(' :', '&nbsp;:').replace('« ', '«&nbsp;').replace(' »', '&nbsp;»')


def page(inner, cls=""):
    inner = NBSP(inner)
    return f'<section class="page {cls}">{inner}{FOOT if "cover" not in cls else ""}</section>'


def e(t):
    return html.escape(t, quote=False)


# ---------- Fiches ----------

def auto_evaluation():
    qs = [
        "Le temps pour m'endormir me paraît long.",
        "Je me réveille la nuit et j'ai du mal à me rendormir.",
        "Les pensées tournent en boucle quand je me couche.",
        "Je sens mon corps tendu le soir (mâchoire, épaules, ventre).",
        "J'appréhende le moment d'aller me coucher.",
        "Je me sens fatigué(e) ou irritable dans la journée.",
    ]
    rows = "".join(f"<tr class='q'><td>{i+1}. {e(q)}</td><td class='c'>…… / 4</td><td class='c'>…… / 4</td><td class='c'>…… / 4</td></tr>" for i, q in enumerate(qs))
    rows += "<tr class='q'><td><b>Total</b></td><td class='c'><b>…… / 24</b></td><td class='c'><b>…… / 24</b></td><td class='c'><b>…… / 24</b></td></tr>"
    return page(f"""
<span class="tag">Fiche 1 · À faire au début</span>
<h1>Où en es-tu ?</h1>
<p class="lead">Une photo de tes soirées aujourd'hui, pour voir le chemin parcouru dans 2 et 4 semaines. Réponds en pensant aux <b>7 derniers jours</b>, sans chercher la « bonne » réponse.</p>
<div class="box blue"><p><b>Barème :</b> 0 = jamais · 1 = rarement · 2 = parfois · 3 = souvent · 4 = presque toujours</p></div>
<table>
<tr><th style="width:55%">Sur les 7 derniers jours…</th><th>Jour 1</th><th>Jour 14</th><th>Jour 28</th></tr>
{rows}
</table>
<h2>Comment lire ton score</h2>
<p>Ce score est un <b>repère personnel</b>, pas un diagnostic. Ce qui compte, c'est son évolution : s'il baisse, tes soirées s'apaisent, même si certaines nuits restent difficiles. Le sommeil progresse rarement en ligne droite.</p>
<div class="box"><p><b>Parles-en à ton médecin</b> si tes nuits sont difficiles au moins 3 fois par semaine depuis plus de 3 mois, si ton score ne bouge pas après 4 semaines, si l'on t'a vu ronfler fort avec des pauses de respiration, ou si ton moral est durablement bas.</p></div>
<h2>Ce que je remarque</h2>
<div class="lines"><div></div><div></div><div></div><div></div></div>
""")


def journal():
    rows = "".join(f"<tr style='height:11mm'><td class='c'><b>{d}</b></td><td></td><td></td><td class='c'>R · M · L</td><td></td><td></td><td></td><td class='c'>…/10</td><td class='c'>…/10</td></tr>" for d in range(1, 15))
    return page(f"""
<span class="tag">Fiche 2 · 1 minute chaque matin</span>
<h1>Journal du sommeil · 14 jours</h1>
<p class="lead">Remplis-le <b>le matin</b>, en une minute, avec des estimations. La nuit, ne regarde pas l'heure : l'objectif est de repérer des tendances, pas de tout mesurer. <b>Endormissement :</b> entoure R (rapide), M (moyen) ou L (long).</p>
<table>
<tr><th style="width:6%">Jour</th><th style="width:10%">Date</th><th style="width:9%">Couché&nbsp;à</th><th style="width:14%">Endormis&shy;sement</th><th style="width:8%">Réveils</th><th style="width:9%">Levé&nbsp;à</th><th style="width:20%">Exercice du soir</th><th style="width:12%">Calme au coucher</th><th style="width:12%">Forme au réveil</th></tr>
{rows}
</table>
<div class="cols" style="margin-top:10px">
<div class="box blue"><p><b>Au bout de 7 jours, regarde :</b></p><p>· les soirs où tu étais le plus calme : qu'avais-tu fait ?</p><p>· ton heure de lever : est-elle régulière ?</p></div>
<div class="box"><p><b>Ce que je remarque cette semaine</b></p><p>…………………………………………………………</p><p>…………………………………………………………</p></div>
</div>
""")


def soucis():
    rows = "".join("<tr style='height:21mm'><td></td><td class='c'>oui · non · en partie</td><td></td><td></td></tr>" for _ in range(7))
    return page(f"""
<span class="tag">Fiche 3 · 15 minutes, en fin d'après-midi</span>
<h1>Le rendez-vous des soucis</h1>
<p class="lead">Donne à tes préoccupations un vrai moment dans la journée, pour qu'elles ne viennent plus le réclamer au moment de dormir. À faire assis, <b>pas au lit</b>, idéalement entre 17 h et 20 h.</p>
<table>
<tr><th style="width:34%">Ce qui me préoccupe</th><th style="width:16%">Puis-je agir ?</th><th style="width:34%">Ma prochaine petite étape</th><th>Quand ?</th></tr>
{rows}
</table>
<div class="box blue" style="margin-top:12px"><p><b>Si je ne peux pas agir :</b> j'écris « je laisse ça de côté pour l'instant » et je note ce qui m'aiderait à l'accepter (en parler à quelqu'un, attendre une information…).</p></div>
<p class="quote">Si le souci revient au lit : « C'est noté. J'y reviendrai demain, à mon rendez-vous. »</p>
<p class="small">Quand tu fermes la feuille, fais-le vraiment : range-la, et passe à autre chose.</p>
""")


def liste_demain():
    return page(f"""
<span class="tag">Fiche 4 · 5 minutes avant de dormir</span>
<h1>La liste de demain</h1>
<p class="lead">Écris tout ce que tu dois faire demain et les jours suivants, <b>le plus précisément possible</b>. Ta tête n'a plus besoin de le garder en mémoire pendant la nuit.</p>
<div class="cols">
<div><h2>Demain</h2><div class="lines">{'<div></div>' * 13}</div></div>
<div><h2>Les jours suivants</h2><div class="lines">{'<div></div>' * 13}</div></div>
</div>
<h2>Une chose qui s'est bien passée aujourd'hui <span class="small">(facultatif)</span></h2>
<div class="lines"><div></div><div></div><div></div></div>
<div class="box blue" style="margin-top:12px"><p>Pas besoin de tout organiser ni de trouver des solutions : il suffit de <b>poser</b> les choses sur le papier. Garde la feuille et un stylo à côté du lit : si une idée revient pendant la nuit, note-la en deux mots et laisse-la là.</p></div>
""")


def sos():
    return page("""
<span class="tag">Fiche 5 · À garder sur la table de nuit</span>
<h1>Réveillé(e) en pleine nuit ?</h1>
<p class="lead">Se réveiller la nuit est normal : chaque nuit compte plusieurs micro-réveils entre les cycles de sommeil. Ce qui entretient l'éveil, c'est surtout la lutte. Voici quoi faire, dans l'ordre.</p>
<ol class="steps">
<li><b>Ne regarde pas l'heure.</b> Tourne ton réveil, laisse ton téléphone loin du lit. Calculer les heures qui restent réveille le mental.</li>
<li><b>Rappelle-toi que c'est normal.</b> « Je me suis réveillé(e), ça arrive. Je peux me reposer même sans dormir tout de suite. »</li>
<li><b>5 soupirs lents.</b> Deux inspirations par le nez (une longue, puis une petite en plus), puis une longue expiration par la bouche.</li>
<li><b>Relâche 4 zones.</b> La mâchoire, les épaules, le ventre, les mains. Laisse ton poids s'enfoncer dans le matelas.</li>
<li><b>Si les pensées tournent :</b> le mélange cognitif (choisis un mot, imagine un objet pour chaque lettre) ou « c'est noté, j'y penserai demain ».</li>
<li><b>Si tu es bien réveillé(e) et agacé(e) depuis un long moment :</b> lève-toi, lumière douce, activité calme (lecture papier, respiration). Reviens te coucher quand les paupières sont lourdes.</li>
</ol>
<div class="box"><p><b>À éviter :</b> les écrans, le frigo « pour se calmer », faire des comptes d'heures de sommeil, te forcer à dormir.</p></div>
<p class="quote">Une nuit plus courte n'est pas une catastrophe. Demain, lève-toi à l'heure habituelle : c'est ce qui prépare la nuit suivante.</p>
<div class="box blue"><p><b>Ma phrase apaisante, à relire la nuit :</b></p><div class="lines"><div></div><div></div></div></div>
""", "big")


def rituel():
    days = "".join(f"<th>{d}</th>" for d in ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"])
    rows = "".join(f"<tr><td><b>Semaine {s}</b></td>" + "<td>☐</td>" * 7 + "</tr>" for s in range(1, 5))
    return page(f"""
<span class="tag">Fiche 6 · À adapter à ton énergie du soir</span>
<h1>Ton rituel du soir, en 3 versions</h1>
<p class="lead">Le meilleur rituel est celui que tu fais vraiment. Choisis chaque soir la version qui correspond à ton énergie : une version courte faite régulièrement vaut mieux qu'une longue abandonnée.</p>
<div class="cols">
<div class="card"><span class="dur">3 minutes</span><h3>Soir d'épuisement</h3><ul>
<li>Lumières baissées, téléphone hors de la chambre</li>
<li>5 soupirs lents, allongé(e)</li>
<li>Une phrase : « Je n'ai rien à réussir cette nuit »</li></ul></div>
<div class="card"><span class="dur">10 minutes</span><h3>Soir ordinaire</h3><ul>
<li>1 h avant : lumières douces, écrans en pause</li>
<li>La liste de demain (3 min)</li>
<li>Relâchement musculaire court (4 min)</li>
<li>Au lit : respiration 4-6 (3 min)</li></ul></div>
<div class="card"><span class="dur">20 minutes</span><h3>Soir agité</h3><ul>
<li>Douche chaude 1 à 2 h avant</li>
<li>Rendez-vous des soucis, si pas fait</li>
<li>Étirements doux (5 min)</li>
<li>Au lit : scan corporel (10 min)</li></ul></div>
</div>
<h2>Mon suivi sur 4 semaines</h2>
<p class="small">Coche chaque soir où tu as fait une version, quelle qu'elle soit. Tu peux noter 3, 10 ou 20 dans la case.</p>
<table class="grid"><tr><th></th>{days}</tr>{rows}</table>
<h2>Ma version à moi</h2><div class="lines"><div></div><div></div><div></div></div>
<div class="box blue" style="margin-top:12px"><p><b>Repères utiles :</b> caféine plutôt avant 14 h · chambre fraîche, autour de 18 °C · même heure de lever chaque jour, week-end compris (à une heure près).</p></div>
""")


SOIRS = [
    ("Semaine 1 · Apaiser le corps", [
        "Auto-évaluation (jour 1) + 5 soupirs lents au lit",
        "Soupir physiologique : 3 fois 1 minute",
        "Relâchement musculaire, version du soir (5 min)",
        "Scan corporel au lit (10 min)",
        "Ton exercice préféré + journal du sommeil le matin",
        "Lumières douces 1 h avant le coucher",
        "Bilan : qu'est-ce qui t'a le plus apaisé ?"]),
    ("Semaine 2 · Laisser passer les pensées", [
        "La liste de demain (5 min) + ton exercice du corps",
        "Premier rendez-vous des soucis (15 min, en fin d'après-midi)",
        "Le mélange cognitif au lit (mot : JARDIN)",
        "« J'ai la pensée que… » : prendre de la distance",
        "Rendez-vous des soucis + liste de demain",
        "Les feuilles sur le ruisseau (5 min)",
        "Auto-évaluation (jour 14) + bilan"]),
    ("Semaine 3 · Installer ton rituel", [
        "Choisis ta version du rituel : 3, 10 ou 20 min",
        "Rituel, version 10 minutes",
        "Douche chaude 1 à 2 h avant + chambre fraîche",
        "Écrans : heure de fin 30 min avant le coucher",
        "Rituel, version 3 minutes (le réflexe du soir)",
        "Rituel, version 20 minutes",
        "Écris ta version à toi + bilan de la semaine"]),
    ("Semaine 4 · Consolider", [
        "Fiche SOS posée sur la table de nuit",
        "Heure de lever fixe + lumière du jour le matin",
        "Ton rituel + un exercice contre les pensées",
        "Soir sans effort : version 3 minutes seulement",
        "Relis ton journal : tes 3 meilleurs soirs",
        "Choisis ton rituel « de base » pour la suite",
        "Auto-évaluation (jour 28) : compare avec le jour 1"]),
]


def parcours():
    rows, n = "", 0
    for semaine, soirs in SOIRS:
        rows += f"<tr><td colspan='4' style='background:#EEF2FA;font-weight:600;color:#1F2A44;padding:4px 6px'>{e(semaine)}</td></tr>"
        for action in soirs:
            n += 1
            rows += f"<tr style='height:5.7mm'><td class='c'><b>{n}</b></td><td>{e(action)}</td><td class='c'>☐</td><td class='c'>…/10</td></tr>"
    return page(f"""
<span class="tag">Fiche 7 · Une ligne par soir</span>
<h1>Mes 28 soirs</h1>
<p class="lead" style="margin-bottom:4px">Chaque soir, une seule action de 5 à 10 minutes, dans l'ordre. Coche quand c'est fait et note ton calme au coucher. Un soir raté ? Reprends simplement le lendemain.</p>
<table class="compact" style="margin-top:4px">
<tr><th style="width:8%">Soir</th><th>Ce soir</th><th style="width:9%">Fait</th><th style="width:13%">Calme</th></tr>
{rows}
</table>
""")


def cover():
    return page("""
<div style="padding:0 6mm">
<span class="tag" style="background:#3D4F8F;color:#fff">Kit à imprimer</span>
<h1>Quand le cerveau refuse de dormir</h1>
<p class="lead">Les 7 fiches qui accompagnent le programme. Imprime-les, garde-les près de toi, et remplis-les au crayon : elles sont faites pour être utilisées, pas pour être parfaites.</p>
<ol>
<li>Où en es-tu ? · l'auto-évaluation (jour 1, 14 et 28)</li>
<li>Journal du sommeil · 14 jours</li>
<li>Le rendez-vous des soucis</li>
<li>La liste de demain</li>
<li>Réveillé(e) en pleine nuit ? · la fiche SOS</li>
<li>Ton rituel du soir, en 3 versions + suivi</li>
<li>Mes 28 soirs · le parcours soir par soir</li>
</ol>
<p class="lead" style="margin-top:18mm">Clarté Mentale · Yacine</p>
<p class="small" style="color:#9FAACB">Outils de bien-être : ils ne remplacent pas un avis médical. Si tes troubles du sommeil durent, parles-en à un professionnel de santé.</p>
</div>
""", "cover")


FICHES = [
    ("01-auto-evaluation", auto_evaluation),
    ("02-journal-sommeil-14-jours", journal),
    ("03-rendez-vous-des-soucis", soucis),
    ("04-liste-de-demain", liste_demain),
    ("05-sos-reveil-nocturne", sos),
    ("06-rituel-du-soir-3-versions", rituel),
    ("07-parcours-28-soirs", parcours),
]


def doc(pages, title):
    return f"<!doctype html><html lang='fr'><head><meta charset='utf-8'><title>{e(title)}</title><style>{CSS}</style></head><body>{pages}</body></html>"


for name, fn in FICHES:
    open(os.path.join(OUT, name + ".html"), "w", encoding="utf-8").write(doc(fn(), name))
open(os.path.join(OUT, "kit-complet-clarte-mentale.html"), "w", encoding="utf-8").write(
    doc(cover() + "".join(fn() for _, fn in FICHES), "Kit complet"))
print("ok", len(FICHES) + 1)
