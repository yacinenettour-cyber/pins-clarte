"""Construit le site statique Clarté Mentale dans site/_build/ (publié sur la branche gh-pages).

Usage : python3 site/outils/construire.py, puis site/outils/publier.sh pour mettre en ligne.
Dépendances : markdown, pillow.

Sources :
- contenu/site.json : réglages du site, guides gratuits, catégories, photo de chaque article ;
- contenu/articles/*.md : un article par fichier (en-tête entre --- puis Markdown) ;
- contenu/pages/*.md : pages fixes (à propos, mentions légales) ;
- contenu/style.css ; photos d'origine prises dans site/images/ ou, à défaut, dans fonds/ (redimensionnées ici en WebP).

Tout le HTML est écrit à la main ici (aucun thème ni service externe) : pages légères, données
structurées schema.org pour Google, et fichiers llms.txt / llms-full.txt pour les assistants IA.
"""
import datetime
import html
import json
import os
import re
from urllib.parse import quote
import shutil
import sys
from xml.sax.saxutils import escape as xml_escape

import markdown
from markdown.extensions.toc import slugify_unicode
from PIL import Image, ImageOps, ImageStat

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "_build")
DEPOT = os.path.dirname(RACINE)
SITE = json.load(open(os.path.join(RACINE, "contenu", "site.json"), encoding="utf-8"))
URL = SITE["url"].rstrip("/")
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre",
        "octobre", "novembre", "décembre"]
SECTIONS_SPECIALES = {"l'essentiel", "questions fréquentes", "pour aller plus loin", "sources"}

LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="15" fill="#080C10" stroke="#8FBF9A" stroke-width="1.5"/>'
        '<path d="M20.5 8.5a8.5 8.5 0 1 0 3 12.6 7 7 0 1 1-3-12.6z" fill="#DFD5C6"/></svg>')


def date_fr(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {MOIS[d.month - 1]} {d.year}"


def e(texte):
    return html.escape(texte or "", quote=True)


def etiqueter_cellules(table):
    """Ajoute à chaque cellule le titre de sa colonne (data-label) : sur mobile, le tableau s'affiche en fiches."""
    entetes = [texte_brut(h) for h in re.findall(r"<th[^>]*>(.*?)</th>", table, flags=re.S)]
    def ligne(m):
        cellules = iter(entetes)
        return re.sub(r"<td([^>]*)>", lambda c: f'<td{c.group(1)} data-label="{e(next(cellules, ""))}">', m.group(0))
    return re.sub(r"<tr>.*?</tr>", ligne, table, flags=re.S)


def md(texte):
    rendu = markdown.markdown(texte, extensions=["extra", "sane_lists"], output_format="html")
    rendu = re.sub(r"<table>.*?</table>", lambda m: etiqueter_cellules(m.group(0)), rendu, flags=re.S)
    # En-tête de première colonne vide (« | | A | B | ») : intitulé lu par les lecteurs d'écran seulement.
    rendu = re.sub(r"<th([^>]*)>\s*</th>", r'<th\1><span class="lecteur-ecran">Critère</span></th>', rendu)
    return rendu.replace("<table>", '<div class="tableau"><table>').replace("</table>", "</table></div>")


def texte_brut(html_txt):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", html_txt))).strip()


# ---------------------------------------------------------------- lecture des articles

def lire_entete(chemin):
    brut = open(chemin, encoding="utf-8").read().replace("\r\n", "\n")
    m = re.match(r"---\n(.*?)\n---\n(.*)", brut, re.S)
    if not m:
        sys.exit(f"En-tête manquant : {chemin}")
    entete = {}
    for ligne in m.group(1).split("\n"):
        if ":" in ligne:
            cle, val = ligne.split(":", 1)
            entete[cle.strip()] = val.strip()
    return entete, m.group(2).strip()


def decouper_sections(corps):
    """Renvoie [(titre H2 ou None, texte)] dans l'ordre."""
    morceaux = re.split(r"^## +(.+?)\s*$", corps, flags=re.M)
    sections = [(None, morceaux[0].strip())] if morceaux[0].strip() else []
    for i in range(1, len(morceaux), 2):
        sections.append((morceaux[i].strip(), morceaux[i + 1].strip()))
    return sections


def appels_de_source(html_txt, nb_sources):
    """[1] ou [1, 3] dans le texte -> exposants cliquables vers la liste des sources."""
    def remplacer(m):
        nums = [int(n) for n in re.findall(r"\d+", m.group(1))]
        if not nums or max(nums) > nb_sources:
            return m.group(0)
        liens = ", ".join(f'<a href="#source-{n}" aria-label="Source {n}">{n}</a>' for n in nums)
        return f"<sup>[{liens}]</sup>"
    return re.sub(r"\[(\d+(?:\s*[,;]\s*\d+)*)\](?!\()", remplacer, html_txt)


# Type de chaque source, affiché sous l'article (E-E-A-T) : (fin du domaine, famille, libellé).
TYPES_SOURCES = [
    ("inserm.fr", "officiel", "Inserm, institut public de recherche médicale"),
    ("has-sante.fr", "officiel", "Haute Autorité de santé"),
    ("ameli.fr", "officiel", "Assurance maladie"),
    ("sante.fr", "officiel", "Santé.fr, service public d'information en santé"),
    ("inrs.fr", "officiel", "INRS, prévention des risques professionnels"),
    ("who.int", "officiel", "Organisation mondiale de la santé"),
    ("service-public.gouv.fr", "officiel", "Service-Public.fr, site officiel de l'administration"),
    ("3114.fr", "officiel", "Numéro national de prévention du suicide"),
    ("mangerbouger.fr", "officiel", "Manger Bouger, Programme national nutrition santé"),
    ("efsa.europa.eu", "officiel", "Autorité européenne de sécurité des aliments"),
    ("ods.od.nih.gov", "officiel", "Instituts nationaux de la santé des États-Unis (NIH)"),
    ("institut-sommeil-vigilance.org", "reference", "Institut national du sommeil et de la vigilance"),
    ("msdmanuals.com", "reference", "Manuel médical de référence"),
    ("clevelandclinic.org", "reference", "Cleveland Clinic, centre médical américain"),
    ("urmc.rochester.edu", "reference", "Centre médical de l'Université de Rochester"),
    ("phqscreeners.com", "reference", "Manuel officiel du questionnaire"),
    ("umontreal.ca", "reference", "Université de Montréal"),
    ("cmu.edu", "reference", "Université Carnegie Mellon"),
    ("sleepfoundation.org", "information", "Site d'information spécialisé"),
]
FAMILLES_SOURCES = {"officiel": ("source officielle", "sources officielles"),
                    "reference": ("référence médicale", "références médicales"),
                    "etude": ("publication scientifique", "publications scientifiques"),
                    "information": ("site d'information", "sites d'information")}


def type_source(url):
    hote = re.sub(r"^https?://([^/]+).*$", r"\1", url).lower()
    for domaine, famille, libelle in TYPES_SOURCES:
        if hote == domaine or hote.endswith("." + domaine):
            return famille, libelle
    return "etude", "Publication scientifique"


def bilan_sources(sources):
    """« 8 sources : 3 organismes officiels de santé, 1 référence médicale, 4 études scientifiques »."""
    comptes = {}
    for _, u in sources:
        famille = type_source(u)[0]
        comptes[famille] = comptes.get(famille, 0) + 1
    morceaux = [f"{n} {FAMILLES_SOURCES[f][0 if n == 1 else 1]}" for f in FAMILLES_SOURCES for n in [comptes.get(f, 0)] if n]
    return f"{len(sources)} sources : " + ", ".join(morceaux)


def lire_article(chemin):
    entete, corps = lire_entete(chemin)
    slug = entete["slug"]
    sections = decouper_sections(corps)
    resume, intro, faq, suite, sources, corps_md = [], "", [], "", [], []
    for titre, texte in sections:
        cle = (titre or "").lower().replace("’", "'")
        if cle == "l'essentiel":
            lignes = texte.split("\n")
            puces = [l[2:].strip() for l in lignes if l.startswith("- ")]
            reste = "\n".join(l for l in lignes if not l.startswith("- ")).strip()
            resume, intro = puces, reste
        elif cle == "questions fréquentes":
            for q, r in re.findall(r"^### +(.+?)\s*\n(.*?)(?=^### |\Z)", texte, flags=re.M | re.S):
                faq.append((q.strip(), r.strip()))
        elif cle == "pour aller plus loin":
            suite = texte
        elif cle == "sources":
            # L'adresse peut contenir des parenthèses équilibrées (DOI du type S0006-3223(03)00465-7).
            for titre_s, url_s in re.findall(r"^\s*\d+\.\s*\[(.+?)\]\((https?://(?:[^()\s]|\([^()\s]*\))+)\)", texte, flags=re.M):
                sources.append((titre_s.strip(), url_s.strip()))
        elif titre is None:
            intro = (intro + "\n\n" + texte).strip()
        else:
            corps_md.append(f"## {titre}\n\n{texte}")
    reglages = SITE["articles"].get(slug, {})
    texte_compte = " ".join([intro, "\n".join(corps_md), suite, " ".join(resume)] + [q + " " + r for q, r in faq])
    mots = len(re.findall(r"\w+", texte_compte))
    return {
        "slug": slug, "titre": entete["titre"], "titre_seo": entete.get("titre_seo") or entete["titre"],
        "description": entete["description"], "mot_cle": entete.get("mot_cle", ""),
        "guide": entete.get("guide", "aucun"), "resume": resume, "intro": intro, "faq": faq,
        "suite": suite, "sources": sources, "corps_md": "\n\n".join(corps_md),
        "categorie": reglages.get("categorie", "stress"), "image": reglages.get("image", ""),
        "formation": reglages.get("formation", False),
        "credit": reglages.get("credit", ""), "alt": reglages.get("alt", entete.get("image", "")),
        "date": entete.get("date", SITE["date_publication"]),
        "maj": entete.get("maj", entete.get("date", SITE["date_publication"])),
        "mots": mots, "lecture": max(1, round(mots / 220)),
    }


# ---------------------------------------------------------------- images

def preparer_image(nom):
    """<nom> -> img/<base>-1200.webp, -640.webp et og-<base>.jpg (1200x630)."""
    if not nom:
        return None
    source = os.path.join(RACINE, "images", nom)
    if not os.path.exists(source):
        source = os.path.join(DEPOT, "fonds", nom)
    base = os.path.splitext(nom)[0]
    dossier = os.path.join(SORTIE, "img")
    os.makedirs(dossier, exist_ok=True)
    img = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    sorties = {}
    for largeur in (1200, 640):
        l = min(largeur, img.width)
        h = round(img.height * l / img.width)
        # Bandeau 3:2 centré sur le tiers haut (visages) pour l'article et les cartes.
        cible_h = round(l * 2 / 3)
        red = img.resize((l, h), Image.LANCZOS)
        if h > cible_h:
            haut = max(0, min(h - cible_h, round(h * 0.18)))
            red = red.crop((0, haut, l, haut + cible_h))
        chemin = os.path.join(dossier, f"{base}-{largeur}.webp")
        red.save(chemin, "WEBP", quality=78, method=6)
        sorties[largeur] = (f"/img/{base}-{largeur}.webp", red.width, red.height)
    # Photo déjà très sombre (luminosité moyenne < 50/255) : pas de teinte commune, elle la noircirait.
    sorties["sombre"] = ImageStat.Stat(img.convert("L")).mean[0] < 50
    og = ImageOps.fit(img, (1200, 630), Image.LANCZOS, centering=(0.5, 0.3))
    og.save(os.path.join(dossier, f"og-{base}.jpg"), "JPEG", quality=82, optimize=True)
    sorties["og"] = f"/img/og-{base}.jpg"
    return sorties


def image_epingle(a):
    """Image verticale 1000x1500 au format épingle : photo en haut, titre dans un bandeau sombre en dessous
    (le texte ne recouvre jamais la photo). Sert au bouton « Enregistrer sur Pinterest » de l'article."""
    from PIL import ImageDraw, ImageFont
    if not a.get("image"):
        return None
    source = os.path.join(RACINE, "images", a["image"])
    if not os.path.exists(source):
        source = os.path.join(DEPOT, "fonds", a["image"])
    W, H, H_PHOTO = 1000, 1500, 860
    toile = Image.new("RGB", (W, H), "#080C10")
    photo = ImageOps.fit(ImageOps.exif_transpose(Image.open(source)).convert("RGB"), (W, H_PHOTO), Image.LANCZOS, centering=(0.5, 0.35))
    if not a["images"].get("sombre"):
        # Même teinte douce que sur le site.
        photo = Image.blend(photo, Image.new("RGB", photo.size, "#3A5F43"), 0.10)
    toile.paste(photo, (0, 0))
    d = ImageDraw.Draw(toile)
    d.rectangle((0, H_PHOTO, W, H_PHOTO + 8), fill="#8FBF9A")
    marge, haut, bas = 70, H_PHOTO + 70, H - 150
    def couper(texte, police, largeur):
        lignes, ligne = [], ""
        for mot in texte.split():
            essai = (ligne + " " + mot).strip()
            if d.textlength(essai, font=police) <= largeur:
                ligne = essai
            else:
                lignes.append(ligne); ligne = mot
        return lignes + [ligne]
    titre = a["titre_seo"]
    for taille in range(72, 38, -2):
        police = ImageFont.truetype(os.path.join(DEPOT, "Poppins-Bold.ttf"), taille)
        lignes = couper(titre, police, W - 2 * marge)
        hauteur_ligne = int(taille * 1.22)
        if len(lignes) * hauteur_ligne <= bas - haut:
            break
    y = haut
    for ligne in lignes:
        d.text((marge, y), ligne, font=police, fill="#DFD5C6"); y += hauteur_ligne
    petite = ImageFont.truetype(os.path.join(DEPOT, "Poppins-Regular.ttf"), 30)
    d.text((marge, H - 100), "Clarté Mentale · contactapaisement-mental.fr", font=petite, fill="#8FBF9A")
    chemin = os.path.join(SORTIE, "img", f"epingle-{a['slug']}.jpg")
    toile.save(chemin, "JPEG", quality=86, optimize=True)
    return f"/img/epingle-{a['slug']}.jpg"


def bloc_epingle(a):
    """Bouton « Enregistrer sur Pinterest » : simple lien vers Pinterest, sans script ni cookie sur le site."""
    if not a.get("epingle"):
        return ""
    lien = ("https://www.pinterest.com/pin/create/button/?url=" + quote(f"{URL}/{a['slug']}/", safe="")
            + "&media=" + quote(URL + a["epingle"], safe="") + "&description=" + quote(f"{a['titre']} — {a['description']}"[:480], safe=""))
    return f"""<aside class="epingle" id="enregistrer" aria-label="Enregistrer sur Pinterest">
<img src="{a['epingle']}" width="1000" height="1500" alt="{e(a['titre_seo'])} : fiche à enregistrer sur Pinterest" loading="lazy" decoding="async">
<div>
<p class="type">À garder pour plus tard</p>
<p>Enregistre cet article sur Pinterest pour le retrouver le soir où tu en auras besoin.</p>
<a class="bouton-pinterest" href="{lien}" target="_blank" rel="noopener">Enregistrer sur Pinterest</a>
</div>
</aside>"""


# ---------------------------------------------------------------- gabarits

def balise_google(chemin):
    code = SITE.get("mesure", {}).get("google_verification")
    return f'<meta name="google-site-verification" content="{e(code)}">' if code and chemin == "/" else ""


def balise_mesure():
    """Cloudflare Web Analytics : mesure d'audience sans cookie, active seulement si un jeton est renseigné."""
    jeton = SITE.get("mesure", {}).get("cloudflare_jeton")
    if not jeton:
        return ""
    # Code fourni par Cloudflare (script de type module).
    return ("<script type=\"module\" src=\"https://static.cloudflareinsights.com/beacon.min.js\" "
            f"data-cf-beacon='{json.dumps({'token': jeton})}'></script>")


def theme_de(a):
    return SITE.get("themes", {}).get(a["categorie"])


def insecables(contenu):
    """Typographie française : espace insécable avant « : ; ? ! % », entre un nombre et son unité et à l'intérieur
    des guillemets, dans le texte seulement (ni les balises, ni les scripts, ni les styles), pour éviter un « : »
    ou un « g » seul en début de ligne."""
    def texte(m):
        t = re.sub(r" ([:;?!»%])", "\u00a0\\1", m.group(1))
        t = re.sub(r"(\d) (?=(?:g|mg|kg|ml|h|min)\b|€)", "\\1\u00a0", t)
        return ">" + t.replace("« ", "«\u00a0") + "<"
    morceaux = re.split(r"(<script.*?</script>|<style.*?</style>)", contenu, flags=re.S)
    return "".join(m if i % 2 else re.sub(r">([^<]+)<", texte, m) for i, m in enumerate(morceaux))


def page(titre, description, chemin, contenu, schemas=(), image_og=None, type_og="website", nav="", meta_article=None, tete=""):
    contenu = insecables(contenu)
    canon = URL + chemin
    image_og = URL + (image_og or "/img/og-defaut.jpg")
    verif = SITE.get("pinterest_verification")
    blocs_ld = "\n".join(
        f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False, separators=(",", ":"))}</script>'
        for s in schemas)
    def lien_nav(href, texte):
        courant = ' aria-current="page"' if href == nav else ""
        return f'<a href="{href}"{courant}>{texte}</a>'
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titre)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="{e(SITE['nom'])}">
<meta property="og:type" content="{type_og}">
<meta property="og:title" content="{e(titre)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{image_og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{meta_article or ""}
{f'<meta name="p:domain_verify" content="{verif}">' if verif and chemin == "/" else ""}
{balise_google(chemin)}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="{e(SITE['nom'])}" href="/feed.xml">
<meta name="theme-color" content="#080C10">
<link rel="preload" href="/polices/syne.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/polices/plus-jakarta-sans.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/style.css">
{tete}
{blocs_ld}
</head>
<body>
<a class="saut" href="#contenu">Aller au contenu</a>
<header class="entete"><div class="large">
<a class="marque" href="/">{LOGO}{e(SITE['nom'])}</a>
<nav class="nav" aria-label="Menu principal">{lien_nav('/articles/', 'Articles')}{lien_nav('/la-formation/', 'La formation')}{lien_nav('/guides-gratuits/', 'Guides gratuits')}{lien_nav('/a-propos/', 'À propos')}</nav>
</div></header>
<main id="contenu">
{contenu}
</main>
<footer class="pied"><div class="large">
<nav aria-label="Liens du pied de page"><a href="/articles/">Tous les articles</a><a href="/test-stress-anxiete/">Test stress et anxiété</a><a href="/respiration-guidee/">Respiration guidée</a>{"".join(f'<a href="/{th["slug"]}/">{e(th["nom"])}</a>' for th in SITE.get("themes", {}).values())}<a href="/la-formation/">La formation</a><a href="/guides-gratuits/">Guides gratuits</a><a href="/a-propos/">À propos</a><a href="/methode-editoriale/">Méthode éditoriale</a><a href="/mentions-legales/">Mentions légales et confidentialité</a><a href="{SITE['pinterest']}" rel="me">Pinterest</a></nav>
<p>Les contenus de ce site sont des informations de bien-être. Ils ne remplacent pas l'avis d'un médecin ou d'un psychologue. En cas d'urgence, appelle le 15 ou le 112 ; en cas de pensées suicidaires, le 3114 (gratuit, 24 h/24).</p>
<p>© {datetime.date.today().year} {e(SITE['nom'])}</p>
</div></footer>
{balise_mesure()}
</body>
</html>
"""


def carte_guide(cle, article=None, titre_niveau="h2"):
    g = SITE["guides"][cle]
    utm = f"utm_source=site&utm_medium={'article' if article else 'page'}&utm_campaign={article or 'site'}"
    if article:
        utm += "&utm_content=fin"
    points = "".join(f"<li>{e(p)}</li>" for p in g["points"])
    return f"""<aside class="guide" aria-label="{e(g['type'])}">
<div class="livret" aria-hidden="true">{e(g['titre'])}<span>{e(SITE['nom'])}</span></div>
<div>
<p class="type">{e(g['type'])}</p>
<{titre_niveau}>{e(g['titre'])}</{titre_niveau}>
<p>{e(g['accroche'])}</p>
<ul>{points}</ul>
<a class="bouton" href="{g['url']}?{utm}">{e(g['bouton'])}</a>
<small>Gratuit, sans engagement. Repères de bien-être, pas un avis médical.</small>
</div>
</aside>"""


def rappel_guide(cle, slug):
    """Rappel discret du guide gratuit au milieu d'un article (beaucoup de lecteurs n'arrivent pas à la fin)."""
    g = SITE["guides"][cle]
    lien = f"{g['url']}?utm_source=site&utm_medium=article&utm_campaign={slug}&utm_content=milieu"
    return f"""<aside class="rappel-guide" aria-label="{e(g['type'])}">
<p><span class="type">{e(g['type'])}</span><strong>{e(g['titre'])}</strong> · {e(g['rappel'])}</p>
<a href="{lien}">{e(g['bouton'])} <span aria-hidden="true">→</span></a>
</aside>"""


def encart_formation(slug):
    """Encart discret en fin d'article : renvoie vers la page de présentation de la formation."""
    f = SITE["formation"]
    return f"""<aside class="formation-encart" aria-label="La formation">
<p class="type">La formation complète</p>
<h3>28 soirs pour calmer ton mental au coucher</h3>
<p>Si les soirées difficiles reviennent souvent, le programme « {e(f['titre'])} » va plus loin que le guide gratuit : 6 modules de leçons courtes, des audios guidés à écouter au lit, le parcours des 28 soirs (une action par soir) et un kit de fiches à imprimer. {e(f['prix'])}, {e(f['prix_detail'])}, garantie de 7 jours.</p>
<a href="/la-formation/">Découvrir le programme</a>
</aside>"""


def teinte(img, a):
    """Enveloppe une photo d'article : teinte commune (verte et sourde) pour l'accorder aux couleurs du site."""
    sombre = " sombre" if a.get("images", {}).get("sombre") else ""
    return f'<span class="teinte{sombre}">{img}</span>'


def carte_article(a, niveau="h3"):
    img = ""
    if a.get("images"):
        src, l, h = a["images"][640]
        img = teinte(f'<img src="{src}" width="{l}" height="{h}" alt="" loading="lazy" decoding="async">', a)
    return f"""<article class="carte">{img}<div class="corps">
<p class="cat">{e(SITE["categories"][a["categorie"]])}</p>
<{niveau}><a href="/{a['slug']}/">{e(a['titre'])}</a></{niveau}>
<p>{e(a['description'])}</p>
</div></article>"""


def ariane(elements):
    lis = "".join(
        f'<li><a href="{href}">{e(nom)}</a></li>' if href else f'<li aria-current="page">{e(nom)}</li>'
        for nom, href in elements)
    schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": nom, **({"item": URL + href} if href else {})}
        for i, (nom, href) in enumerate(elements)]}
    return f'<nav class="ariane" aria-label="Fil d\'Ariane"><ol>{lis}</ol></nav>', schema


def editeur():
    return {"@type": "Organization", "@id": URL + "/#organisation", "name": SITE["nom"], "url": URL + "/",
            "logo": {"@type": "ImageObject", "url": URL + "/logo.png", "width": 512, "height": 512},
            "sameAs": [SITE["pinterest"]], "publishingPrinciples": URL + "/methode-editoriale/"}


def auteur():
    personne = {"@type": "Person", "@id": URL + "/a-propos/#auteur", "name": SITE["auteur"]["nom"],
                "jobTitle": SITE["auteur"]["role"], "url": URL + SITE["auteur"]["page"],
                "worksFor": {"@id": URL + "/#organisation"}}
    if SITE["auteur"].get("photo"):
        personne["image"] = URL + SITE["auteur"]["photo"]
    return personne


def avatar(taille, classe):
    photo = SITE["auteur"].get("photo")
    if not photo:
        return ""
    alt = "" if classe == "avatar" else e(SITE["auteur"].get("photo_alt", SITE["auteur"]["nom"]))
    return f'<img class="{classe}" src="{photo}" width="{taille}" height="{taille}" alt="{alt}">'


def liste_sources(sources, objet="l'article"):
    return ('<section class="sources"><h2 id="sources">Sources</h2><ol>'
            + "".join(f'<li id="source-{i + 1}"><a href="{e(u)}" rel="noopener">{e(t)}</a> '
                      f'<span class="type-source type-{type_source(u)[0]}">{e(type_source(u)[1])}</span></li>'
                      for i, (t, u) in enumerate(sources))
            + '</ol><p class="note-sources">Chaque source a été ouverte et relue pour vérifier qu\'elle dit bien '
            f'ce que {objet} lui attribue. <a href="/methode-editoriale/">Comment les contenus sont écrits et vérifiés</a></p></section>')


# ---------------------------------------------------------------- pages

def construire_article(a, tous):
    corps_html = md(a["corps_md"])
    # Ancres sur les H2 + sommaire.
    titres = []
    def ancre(m):
        texte = texte_brut(m.group(1))
        ident = slugify_unicode(texte, "-")
        titres.append((ident, texte))
        return f'<h2 id="{ident}">{m.group(1)}</h2>'
    corps_html = re.sub(r"<h2>(.*?)</h2>", ancre, corps_html)
    corps_html = appels_de_source(corps_html, len(a["sources"]))
    if a["guide"] in SITE["guides"] and len(titres) >= 3:
        # Après la 2e partie, avant le 3e intertitre.
        repere = f'<h2 id="{titres[2][0]}">'
        corps_html = corps_html.replace(repere, rappel_guide(a["guide"], a["slug"]) + "\n" + repere, 1)
    intro_html = appels_de_source(md(a["intro"]), len(a["sources"])).replace("<p>", '<p class="chapo">', 1)
    sommaire = ""
    if len(titres) >= 3:
        sommaire = ('<nav class="sommaire" aria-label="Sommaire"><h2>Sommaire</h2><ol>'
                    + "".join(f'<li><a href="#{i}">{e(t)}</a></li>' for i, t in titres) + "</ol></nav>")
    resume = ""
    if a["resume"]:
        resume = ('<section class="essentiel" aria-label="L\'essentiel"><h2>L\'essentiel en 30 secondes</h2><ul>'
                  + "".join(f"<li>{appels_de_source(md(p)[3:-4], len(a['sources']))}</li>" for p in a["resume"])
                  + "</ul></section>")
    faq_html = ""
    if a["faq"]:
        faq_html = ('<section class="faq"><h2 id="questions-frequentes">Questions fréquentes</h2>'
                    + "".join(f"<h3>{e(q)}</h3>{appels_de_source(md(r), len(a['sources']))}" for q, r in a["faq"])
                    + "</section>")
    suite_html = ""
    if a["suite"]:
        suite_html = f'<h2 id="pour-aller-plus-loin">Pour aller plus loin</h2>{appels_de_source(md(a["suite"]), len(a["sources"]))}'
    if a["guide"] in SITE["guides"]:
        suite_html += carte_guide(a["guide"], a["slug"], "h3")
    if a["formation"] and SITE.get("formation"):
        suite_html += encart_formation(a["slug"])
    sources_html = liste_sources(a["sources"]) if a["sources"] else ""
    photo = ""
    if a.get("images"):
        src, l, h = a["images"][1200]
        src_p = a["images"][640][0]
        credit = f"<figcaption>{e(a['credit'])}</figcaption>" if a["credit"] else ""
        photo = (f'<figure class="photo">' + teinte(f'<img src="{src}" srcset="{src_p} 640w, {src} 1200w" '
                 f'sizes="(max-width: 760px) 100vw, 740px" width="{l}" height="{h}" alt="{e(a["alt"])}" '
                 f'fetchpriority="high">', a) + f'{credit}</figure>')
    proches = sorted((b for b in tous if b["slug"] != a["slug"]),
                     key=lambda b: (b["categorie"] != a["categorie"], b["guide"] != a["guide"], b["titre"]))[:3]
    lies = ('<section><h2 id="a-lire-aussi">À lire aussi</h2><div class="grille">'
            + "".join(carte_article(b) for b in proches) + "</div></section>")
    th = theme_de(a)
    nav_html, schema_ariane = ariane([("Accueil", "/")] + ([(th["nom"], f"/{th['slug']}/")] if th else [("Articles", "/articles/")])
                                     + [(a["titre"], None)])
    contenu = f"""<div class="etroit">
{nav_html}
<article>
<h1>{e(a['titre'])}</h1>
<p class="meta">{avatar(28, "avatar")}Par <a href="/a-propos/" rel="author">{e(SITE['auteur']['nom'])}</a> · Mis à jour le <time datetime="{a["maj"]}">{date_fr(a['maj'])}</time> · {a['lecture']} min de lecture</p>
<p class="bilan-sources"><a href="#sources">{e(bilan_sources(a['sources']))}</a><a href="/methode-editoriale/">Méthode éditoriale</a>{'<a href="#enregistrer">Enregistrer sur Pinterest</a>' if a.get('epingle') else ''}</p>
{intro_html}
{photo}
{resume}
{sommaire}
{corps_html}
{faq_html}
{suite_html}
{bloc_epingle(a)}
{sources_html}
<p class="avertissement">Cet article donne des repères de bien-être fondés sur les sources citées. Il ne remplace pas une consultation : si tes symptômes durent, s'aggravent ou t'inquiètent, parles-en à ton médecin.</p>
</article>
{lies}
</div>"""
    schema_article = {
        "@context": "https://schema.org", "@type": "Article", "@id": f"{URL}/{a['slug']}/#article",
        "headline": a["titre"], "description": a["description"], "inLanguage": SITE["langue"],
        "datePublished": a["date"], "dateModified": a["maj"], "wordCount": a["mots"],
        "mainEntityOfPage": f"{URL}/{a['slug']}/", "author": auteur(), "publisher": editeur(),
        "about": a["mot_cle"], "isAccessibleForFree": True,
        "citation": [{"@type": "ScholarlyArticle" if type_source(u)[0] == "etude" else "CreativeWork", "name": t, "url": u}
                     for t, u in a["sources"]],
        "publishingPrinciples": URL + "/methode-editoriale/",
    }
    if a.get("images"):
        schema_article["image"] = [URL + a["images"][1200][0], URL + a["images"]["og"]]
    schemas = [schema_article, schema_ariane]
    if a["faq"]:
        schemas.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": texte_brut(md(r))}}
            for q, r in a["faq"]]})
    # Balises Open Graph « article » : lues par Pinterest pour les épingles enrichies (Rich Pins).
    meta_article = (f'<meta property="article:published_time" content="{a["date"]}">\n'
                    f'<meta property="article:modified_time" content="{a["maj"]}">\n'
                    f'<meta property="article:author" content="{e(SITE["auteur"]["nom"])}">\n'
                    f'<meta property="article:section" content="{e(SITE["categories"][a["categorie"]])}">')
    ecrire(f"{a['slug']}/index.html", page(a["titre_seo"], a["description"], f"/{a['slug']}/", contenu, schemas,
                                           a["images"]["og"] if a.get("images") else None, "article",
                                           meta_article=meta_article))


# Polices de l'accueil : les mêmes @font-face que style.css (polices du site et polices de secours mises à l'échelle).
POLICES_CSS = "\n".join(l.rstrip() for l in open(os.path.join(RACINE, "contenu", "style.css"), encoding="utf-8")
                        if l.startswith("@font-face"))
TITRE_ACCUEIL = "Baisser le cortisol : test anti-stress pour mieux dormir"
DESCRIPTION_ACCUEIL = ("Test stress et anxiété en 2 minutes (questionnaire validé GAD-7) et ton profil, puis les gestes "
                       "anti-stress naturels validés par la science pour mieux dormir.")


def cartes_lecture(articles, image_en_ligne=False):
    """Cartes d'articles de l'accueil (verre sombre). image_en_ligne : image intégrée (artefact)."""
    cartes = []
    for a in articles[:6]:
        img = ""
        if a.get("images"):
            src, l, h = a["images"][640]
            if image_en_ligne:
                import base64
                donnees = base64.b64encode(open(os.path.join(SORTIE, src.lstrip("/")), "rb").read()).decode()
                src = "data:image/webp;base64," + donnees
            img = teinte(f'<img src="{src}" width="{l}" height="{h}" alt="" loading="lazy" decoding="async">', a)
        lien = (URL if image_en_ligne else "") + f"/{a['slug']}/"
        cartes.append(f'<a class="carte-lecture" href="{lien}">{img}<div class="corps">'
                      f'<p class="etiquette">{e(SITE["categories"][a["categorie"]])}</p>'
                      f'<h3>{e(a["titre"])}</h3><p>{e(a["description"])}</p></div></a>')
    return "".join(cartes)


def faq_accueil(source):
    return [(texte_brut(q), texte_brut(r)) for q, r in
            re.findall(r"<summary><h3>(.*?)</h3></summary>\s*<p>(.*?)</p>", source, re.S)]


def construire_accueil(articles):
    """Accueil : page unique « biophilic dark » (contenu/accueil.html), reliée aux articles et à la formation."""
    source = open(os.path.join(RACINE, "contenu", "accueil.html"), encoding="utf-8").read()
    corps = (source.replace("/*@POLICES*/", POLICES_CSS).replace("/*@TEST_CSS*/", css_test()).replace("{{B}}", "")
             .replace("{{ARTICLES}}", cartes_lecture(articles)).replace("/*@TEST_JS*/", script_test(articles)))
    corps = insecables(corps)
    faq = faq_accueil(source)
    schemas = [
        {"@context": "https://schema.org", "@type": "WebSite", "@id": URL + "/#site", "name": SITE["nom"],
         "url": URL + "/", "inLanguage": SITE["langue"], "description": DESCRIPTION_ACCUEIL,
         "publisher": {"@id": URL + "/#organisation"}},
        {"@context": "https://schema.org", **editeur(), "description": SITE["description"], "founder": auteur()},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in faq]},
    ]
    blocs_ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False, separators=(",", ":"))}</script>'
                         for s in schemas)
    verif = SITE.get("pinterest_verification")
    html_page = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(TITRE_ACCUEIL)}</title>
<meta name="description" content="{e(DESCRIPTION_ACCUEIL)}">
<link rel="canonical" href="{URL}/">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#080C10">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="{e(SITE['nom'])}">
<meta property="og:type" content="website">
<meta property="og:title" content="Ton système nerveux mérite une trêve | {e(SITE['nom'])}">
<meta property="og:description" content="{e(DESCRIPTION_ACCUEIL)}">
<meta property="og:url" content="{URL}/">
<meta property="og:image" content="{URL}/img/og-defaut.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{f'<meta name="p:domain_verify" content="{verif}">' if verif else ""}
{balise_google("/")}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="{e(SITE['nom'])}" href="/feed.xml">
<link rel="preload" href="/polices/syne.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/polices/plus-jakarta-sans.woff2" as="font" type="font/woff2" crossorigin>
{blocs_ld}
</head>
<body>
{corps}
{balise_mesure()}
</body>
</html>
"""
    ecrire("index.html", html_page)
    if os.environ.get("ARTEFACT"):
        # Version artefact (aperçu claude.ai) : liens absolus, images intégrées, polices Google (seul hôte admis).
        polices = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700'
                   '&family=Syne:wght@500;600;700;800&display=swap">')
        artefact = (f"<title>{e(TITRE_ACCUEIL)}</title>\n"
                    f'<meta name="description" content="{e(DESCRIPTION_ACCUEIL)}">\n{polices}\n'
                    + source.replace("/*@POLICES*/", "").replace("/*@TEST_CSS*/", css_test()).replace("{{B}}", URL)
                    .replace("{{ARTICLES}}", cartes_lecture(articles, image_en_ligne=True))
                    .replace("/*@TEST_JS*/", script_test(articles, URL)))
        open(os.environ["ARTEFACT"], "w", encoding="utf-8").write(artefact)


def construire_liste(articles):
    blocs = []
    for cle, nom in SITE["categories"].items():
        lot = [a for a in articles if a["categorie"] == cle]
        if lot:
            th = SITE.get("themes", {}).get(cle)
            lien = f' <a class="voir-theme" href="/{th["slug"]}/">Voir le thème</a>' if th else ""
            blocs.append(f'<h2 id="{cle}">{e(nom)}{lien}</h2><div class="grille">'
                         + "".join(carte_article(a) for a in lot) + "</div>")
    nav_html, schema_ariane = ariane([("Accueil", "/"), ("Articles", None)])
    contenu = f"""<div class="large">{nav_html}
<h1>Tous les articles</h1>
<p class="chapo">Stress, système nerveux, sommeil, charge mentale : des articles complets, sourcés et mis à jour.</p>
{''.join(blocs)}</div>"""
    schema = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Tous les articles",
              "url": URL + "/articles/", "inLanguage": SITE["langue"],
              "hasPart": [{"@type": "Article", "headline": a["titre"], "url": f"{URL}/{a['slug']}/"} for a in articles]}
    ecrire("articles/index.html", page(f"Articles sur le stress et le sommeil | {SITE['nom']}",
                                       "Tous les articles de Clarté Mentale : ruminations du soir, réveils nocturnes, cortisol, nerf vague, charge mentale, burn-out.",
                                       "/articles/", contenu, [schema, schema_ariane], nav="/articles/"))


def construire_theme(cle, articles):
    """Page thème : définition, « par où commencer ? », articles du thème et guide adapté."""
    th = SITE["themes"][cle]
    lot = [a for a in articles if a["categorie"] == cle]
    par_slug = {a["slug"]: a for a in articles}
    lignes = "".join(f'<tr><td data-label="Ta situation">{e(sit)}</td><td data-label="À lire"><a href="/{s}/">{e(par_slug[s]["titre"])}</a></td></tr>'
                     for sit, s in th["par_ou_commencer"])
    tableau = ('<div class="tableau"><table><thead><tr><th scope="col">Ta situation</th><th scope="col">À lire</th></tr></thead>'
               f"<tbody>{lignes}</tbody></table></div>")
    autres = [t for k, t in SITE["themes"].items() if k != cle]
    nav_html, schema_ariane = ariane([("Accueil", "/"), (th["nom"], None)])
    contenu = f"""<div class="large">{nav_html}
<h1>{e(th['titre'])}</h1>
{''.join(f'<p class="chapo">{e(p)}</p>' if i == 0 else f'<p>{e(p)}</p>' for i, p in enumerate(th['intro']))}
<h2 id="par-ou-commencer">Par où commencer ?</h2>
{tableau}
<h2 id="articles">Les articles du thème</h2>
<div class="grille">{''.join(carte_article(a) for a in lot)}</div>
{carte_guide(th['guide'], None, "h2") if th.get('guide') in SITE['guides'] else ''}
<p class="autres-themes">Autres thèmes : {' · '.join(f'<a href="/{t["slug"]}/">{e(t["nom"])}</a>' for t in autres)} · <a href="/articles/">tous les articles</a></p>
</div>"""
    schema = {"@context": "https://schema.org", "@type": "CollectionPage", "name": th["titre"],
              "description": th["description"], "url": f"{URL}/{th['slug']}/", "inLanguage": SITE["langue"],
              "isPartOf": {"@id": URL + "/#site"}, "publisher": {"@id": URL + "/#organisation"},
              "mainEntity": {"@type": "ItemList", "itemListElement": [
                  {"@type": "ListItem", "position": i + 1, "url": f"{URL}/{a['slug']}/", "name": a["titre"]}
                  for i, a in enumerate(lot)]}}
    ecrire(f"{th['slug']}/index.html", page(f"{th['titre_seo']} | {SITE['nom']}", th["description"], f"/{th['slug']}/",
                                            contenu, [schema, schema_ariane]))


def construire_guides():
    nav_html, schema_ariane = ariane([("Accueil", "/"), ("Guides gratuits", None)])
    contenu = f"""<div class="etroit">{nav_html}
<h1>Les guides gratuits</h1>
<p class="chapo">Deux ressources gratuites, à télécharger, pour passer de la lecture à la pratique.</p>
{''.join(carte_guide(c, titre_niveau='h2') for c in SITE['guides'])}
<p>L'inscription se fait sur une page sécurisée hébergée par systeme.io. Tu peux te désinscrire en un clic à tout moment.</p>
</div>"""
    ecrire("guides-gratuits/index.html", page(f"Guides gratuits : sommeil et cortisol | {SITE['nom']}",
                                              "Deux guides gratuits : « Quand le cerveau refuse de dormir » pour les ruminations du soir, et « Le plan anti-cortisol en 7 jours ».",
                                              "/guides-gratuits/", contenu, [schema_ariane], nav="/guides-gratuits/"))


COMPARATIF_FORMATION = """| | Guide gratuit | Formation |
|---|---|---|
| Format | Un PDF à télécharger | 6 modules, près de 30 leçons courtes, des audios guidés et un kit de 7 fiches à imprimer |
| Ce qu'on y travaille | Une routine anti-rumination à faire au lit et des exercices pour calmer le mental le soir | Apaiser le système nerveux, sortir des ruminations sans lutter, un rituel du soir en 3 versions, les réveils nocturnes et les situations particulières (travail qui suit jusqu'au lit, nuits hachées de parent, horaires décalés) |
| Le rythme | Un calendrier de 30 jours | Le parcours des 28 soirs : une action par soir, avec une auto-évaluation aux jours 1, 14 et 28 |
| Les audios | Aucun | Des audios guidés à écouter au lit, dont un audio express de 3 minutes |
| Le prix | Gratuit | 37 €, paiement unique, garantie de 7 jours |"""


def construire_formation():
    f = SITE["formation"]
    achat = f"{f['url']}?utm_source=site&utm_medium=page&utm_campaign=la-formation"
    def liste(points, classe=""):
        return f'<ul class="{classe}">' + "".join(f"<li>{e(p)}</li>" for p in points) + "</ul>"
    modules = "".join(f'<div class="module"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in f["modules"])
    faq = "".join(f"<h3>{e(q)}</h3><p>{e(r)}</p>" for q, r in f["faq"])
    prix = f"""<div class="prix"><p class="montant">{e(f['prix'])}</p><p>{e(f['prix_detail'])}</p>
<a class="bouton" href="{achat}">{e(f['bouton'])}</a>
<p class="petit">{e(f['garantie'])}</p>
<p class="petit">Paiement sécurisé sur systeme.io (carte bancaire ou Apple Pay). <a href="{f['url_cgv']}">Conditions générales de vente</a>.</p></div>"""
    nav_html, schema_ariane = ariane([("Accueil", "/"), ("La formation", None)])
    contenu = f"""<div class="etroit">{nav_html}
<p class="surtitre">La formation Clarté Mentale</p>
<h1>{e(f['titre'])}</h1>
<p class="chapo">{e(f['sous_titre'])}</p>
{prix}
<h2>Tu te reconnais dans ces soirées ?</h2>
{liste(f['reconnais'])}
<p>Ce n'est pas un manque de volonté. Quand la journée a été lourde, le corps peut rester en mode alerte au moment de se coucher : le cœur bat un peu vite, la respiration reste haute, et le mental continue de « surveiller ». Chercher à forcer le sommeil entretient souvent cette alerte. Le programme part de là : aider le corps à se sentir en sécurité, soir après soir, pour que le sommeil puisse revenir. Pour comprendre ce mécanisme, tu peux lire <a href="/calmer-son-systeme-nerveux/">comment calmer son système nerveux</a> et <a href="/ruminations-le-soir/">pourquoi le cerveau s'emballe le soir</a>.</p>
<h2>Ce que contient le programme</h2>
<p>6 modules, près de 30 leçons courtes et sans jargon, des audios guidés et un kit de fiches à imprimer. Accès depuis ton téléphone, ta tablette ou ton ordinateur.</p>
<div class="modules">{modules}</div>
<h2>Guide gratuit ou formation : quelle différence ?</h2>
<p>Le guide gratuit est une première marche ; la formation reprend la même approche et va beaucoup plus loin. Voici ce qui change :</p>
{md(COMPARATIF_FORMATION)}
<div class="deux-listes">
<div><h2>C'est pour toi si…</h2>{liste(f['pour_toi'], 'oui')}</div>
<div><h2>Ce n'est pas pour toi si…</h2>{liste(f['pas_pour_toi'], 'non')}</div>
</div>
<h2>Pas de faux avis ici</h2>
<p>Le programme est récent : je n'ai pas encore de témoignages à te montrer, et je préfère te le dire plutôt que d'en inventer. C'est pour ça que la garantie de 7 jours existe : tu testes chez toi, le soir, sans risque. — {e(SITE['auteur']['nom'])}, <a href="/a-propos/">Clarté Mentale</a></p>
{prix}
<section class="faq"><h2>Questions fréquentes</h2>{faq}</section>
<h2>Pas encore prêt(e) ?</h2>
<p>Commence par le guide gratuit : une routine anti-rumination à faire au lit et un calendrier de 30 jours, pour voir si cette approche te convient.</p>
{carte_guide('sommeil', 'la-formation', 'h3')}
<p class="avertissement">Ce programme propose des outils de bien-être. Il ne constitue ni un traitement médical ni une thérapie et ne remplace pas l'avis d'un professionnel de santé. Si tes difficultés de sommeil durent depuis plusieurs mois ou s'accompagnent d'un moral très bas, parles-en à ton médecin.</p>
</div>"""
    schema_cours = {
        "@context": "https://schema.org", "@type": "Course", "@id": URL + "/la-formation/#formation",
        "name": f["titre"], "description": f["sous_titre"], "inLanguage": SITE["langue"],
        "provider": {"@id": URL + "/#organisation", "@type": "Organization", "name": SITE["nom"], "url": URL + "/"},
        "url": URL + "/la-formation/",
        "offers": {"@type": "Offer", "price": f["prix_valeur"], "priceCurrency": "EUR", "category": "Paid",
                   "availability": "https://schema.org/InStock", "url": f["url"]},
        "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Online", "courseWorkload": "PT10M"},
        "teaches": [t for t, _ in f["modules"]],
    }
    schema_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in f["faq"]]}
    ecrire("la-formation/index.html", page(f"Formation sommeil : {f['titre']} | {SITE['nom']}",
                                           "Programme en ligne pour calmer le mental le soir : 6 modules courts, audios guidés, parcours de 28 soirs, kit de fiches. 37 €, garantie 7 jours.",
                                           "/la-formation/", contenu, [schema_cours, schema_faq, schema_ariane],
                                           nav="/la-formation/"))


# ---------------------------------------------------------------- test stress et anxiété (GAD-7 + profil)

DOSSIER_TEST = os.path.join(RACINE, "contenu", "test")
INSTRUMENT_TEST = """<div class="instrument" id="test-stress" aria-live="polite">
<div class="progression"><span id="test-compteur">Question 1 sur 13</span><div class="barre" aria-hidden="true"><i id="test-barre"></i></div></div>
<div id="test-ecran"><noscript><p>Ce test a besoin de JavaScript pour calculer ton score dans ton navigateur.</p></noscript></div>
</div>"""


def css_test():
    return open(os.path.join(DOSSIER_TEST, "test.css"), encoding="utf-8").read()


def script_test(articles, base=""):
    """Moteur du test (contenu/test/test.js) avec les titres d'articles et les guides du site."""
    donnees = (f"var ARTICLES = {json.dumps({a['slug']: a['titre'] for a in articles}, ensure_ascii=False)};\n"
               f"  var GUIDES = {json.dumps({c: {k: g[k] for k in ('titre', 'type', 'rappel', 'bouton', 'url')} for c, g in SITE['guides'].items()}, ensure_ascii=False)};")
    js = open(os.path.join(DOSSIER_TEST, "test.js"), encoding="utf-8").read()
    return js.replace("/*@DONNEES*/", donnees.replace("</", "<\\/")).replace("{{B}}", base)


def construire_page_outil(fichier, chemin, nom_court, marqueurs, duree, tete="", script="", schemas_en_plus=()):
    """Page « outil » sourcée (test, audios) : texte en markdown avec des marqueurs {{…}} remplacés par l'outil,
    sections « Questions fréquentes » et « Sources » comme dans les articles."""
    entete, corps = lire_entete(os.path.join(RACINE, "contenu", "pages", fichier))
    intro, faq, sources, corps_md = "", [], [], []
    for titre, texte in decouper_sections(corps):
        cle = (titre or "").lower()
        if cle == "questions fréquentes":
            faq = [(q.strip(), r.strip()) for q, r in re.findall(r"^### +(.+?)\s*\n(.*?)(?=^### |\Z)", texte, flags=re.M | re.S)]
        elif cle == "sources":
            sources = [(a.strip(), b.strip()) for a, b in re.findall(r"^\s*\d+\.\s*\[(.+?)\]\((https?://(?:[^()\s]|\([^()\s]*\))+)\)", texte, flags=re.M)]
        elif titre is None:
            intro = texte
        else:
            corps_md.append(f"## {titre}\n\n{texte}")
    nb = len(sources)
    intro_html = appels_de_source(md(intro), nb).replace("<p>", '<p class="chapo">', 1)
    for marqueur, contenu_outil in marqueurs.items():
        intro_html = intro_html.replace(f"<p>{marqueur}</p>", contenu_outil)
    corps_html = appels_de_source(md("\n\n".join(corps_md)), nb)
    corps_html = re.sub(r"<h2>(.*?)</h2>", lambda m: f'<h2 id="{slugify_unicode(texte_brut(m.group(1)), "-")}">{m.group(1)}</h2>', corps_html)
    faq_html = ('<section class="faq"><h2 id="questions-frequentes">Questions fréquentes</h2>'
                + "".join(f"<h3>{e(q)}</h3>{appels_de_source(md(r), nb)}" for q, r in faq) + "</section>")
    nav_html, schema_ariane = ariane([("Accueil", "/"), (nom_court, None)])
    contenu = f"""<div class="etroit">{nav_html}
<h1>{e(entete['titre'])}</h1>
<p class="meta">{avatar(28, "avatar")}Par <a href="/a-propos/" rel="author">{e(SITE['auteur']['nom'])}</a> · Mis à jour le <time datetime="{entete['maj']}">{date_fr(entete['maj'])}</time> · {duree}</p>
<p class="bilan-sources"><a href="#sources">{e(bilan_sources(sources))}</a><a href="/methode-editoriale/">Méthode éditoriale</a></p>
{intro_html}
{corps_html}
{faq_html}
{liste_sources(sources, "la page")}
<p class="avertissement">Cette page donne des repères de bien-être, pas un diagnostic ni un traitement. Si tes symptômes durent, s'aggravent ou t'inquiètent, parles-en à ton médecin.</p>
</div>
{f"<script>{script}</script>" if script else ""}"""
    schemas = [
        {"@context": "https://schema.org", "@type": "WebPage", "@id": URL + chemin + "#page", "url": URL + chemin,
         "name": entete["titre"], "description": entete["description"], "inLanguage": SITE["langue"],
         "dateModified": entete["maj"], "author": auteur(), "publisher": editeur(), "isAccessibleForFree": True,
         "citation": [{"@type": "ScholarlyArticle" if type_source(u)[0] == "etude" else "CreativeWork", "name": t, "url": u}
                      for t, u in sources],
         "publishingPrinciples": URL + "/methode-editoriale/"},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": texte_brut(md(r))}} for q, r in faq]},
        schema_ariane, *schemas_en_plus,
    ]
    ecrire(chemin.strip("/") + "/index.html", page(entete["titre_seo"], entete["description"], chemin, contenu, schemas,
                                                   nav=chemin, tete=tete))
    return entete


def construire_test(articles):
    return construire_page_outil("test-stress-anxiete.md", "/test-stress-anxiete/", "Test stress et anxiété",
                                 {"{{TEST}}": INSTRUMENT_TEST}, "2 minutes", tete=f"<style>{css_test()}</style>",
                                 script=script_test(articles))


# ---------------------------------------------------------------- audios de respiration guidée

AUDIOS = [  # (minutes, moment conseillé) ; fichiers produits par outils/audios_respiration.py
    (3, "une pause dans la journée"),
    (5, "le soir, avant de te coucher"),
    (10, "au lit, pour t'endormir"),
]
DEBUT_CYCLES = 8  # secondes d'introduction avant la première inspiration (voir audios_respiration.py)
SCRIPT_AUDIO = """(function () {
  /* Affiche la phase (inspire / expire) d'après la position de lecture : 8 s d'introduction, puis des cycles de 10 s. */
  document.querySelectorAll(".audio").forEach(function (bloc) {
    var a = bloc.querySelector("audio"), p = bloc.querySelector(".phase"), fin = Number(bloc.dataset.cycles) * 10 + 8;
    function maj() {
      var t = a.currentTime;
      if (a.paused && t === 0) { p.textContent = "Appuie sur lecture, puis ferme les yeux si tu veux."; return; }
      if (t < 8) { p.textContent = "Installe-toi…"; return; }
      if (t >= fin) { p.textContent = "Reste au calme encore un instant."; return; }
      var c = (t - 8) % 10;
      p.textContent = c < 4 ? "Inspire… (4 s)" : "Expire… (6 s)";
    }
    ["timeupdate", "play", "pause", "seeked", "ended"].forEach(function (ev) { a.addEventListener(ev, maj); });
    /* Une seule piste à la fois. */
    a.addEventListener("play", function () { document.querySelectorAll(".audio audio").forEach(function (b) { if (b !== a) b.pause(); }); });
  });
})();"""


def lecteurs_audio():
    blocs = []
    for minutes, moment in AUDIOS:
        nom = f"respiration-4-6-{minutes}-min.mp3"
        taille = os.path.getsize(os.path.join(RACINE, "contenu", "audio", nom)) / 1e6
        cycles = minutes * 6
        blocs.append(f'<figure class="audio" data-cycles="{cycles}"><figcaption><span><strong>{minutes} minutes</strong> · {e(moment)}</span>'
                     f'<span class="nb">{cycles} respirations</span></figcaption>'
                     f'<audio controls preload="none" src="/audio/{nom}"></audio>'
                     f'<p class="phase">Appuie sur lecture, puis ferme les yeux si tu veux.</p>'
                     f'<a href="/audio/{nom}" download>Télécharger (MP3, {f"{taille:.1f}".replace(".", ",")} Mo)</a></figure>')
    credit = ('<p class="credit-audio">Musique : « Deep Relaxation », Kevin MacLeod '
              '(<a href="https://incompetech.com/">incompetech.com</a>), sous licence '
              '<a href="https://creativecommons.org/licenses/by/4.0/deed.fr">Creative Commons Attribution 4.0</a> ; '
              'extrait mixé avec des repères de respiration par Clarté Mentale.</p>')
    return '<div class="audios">' + "".join(blocs) + credit + "</div>"


def construire_respiration():
    objets = [{"@context": "https://schema.org", "@type": "AudioObject", "name": f"Respiration guidée 4-6 — {m} minutes",
               "description": f"Respiration lente guidée sur une musique de détente, sans voix : inspirer 4 secondes, expirer 6 secondes, {m * 6} respirations.",
               "contentUrl": f"{URL}/audio/respiration-4-6-{m}-min.mp3", "encodingFormat": "audio/mpeg",
               "duration": f"PT{m}M", "inLanguage": SITE["langue"], "isAccessibleForFree": True,
               "creator": {"@id": URL + "/#organisation"},
               "contributor": {"@type": "Person", "name": "Kevin MacLeod", "url": "https://incompetech.com/"},
               "license": "https://creativecommons.org/licenses/by/4.0/"} for m, _ in AUDIOS]
    return construire_page_outil("respiration-guidee.md", "/respiration-guidee/", "Respiration guidée",
                                 {"{{AUDIOS}}": lecteurs_audio()}, "3 à 10 minutes", script=SCRIPT_AUDIO,
                                 schemas_en_plus=objets)


def construire_page_fixe(nom_fichier, chemin, nav=""):
    entete, corps = lire_entete(os.path.join(RACINE, "contenu", "pages", nom_fichier))
    nav_html, schema_ariane = ariane([("Accueil", "/"), (entete["titre"], None)])
    corps_html = md(corps)
    if chemin == "/a-propos/":
        corps_html = re.sub(r"(<h2>Qui écrit[^<]*</h2>)", lambda m: m.group(1) + avatar(112, "portrait"), corps_html, count=1)
    contenu = f'<div class="etroit">{nav_html}<h1>{e(entete["titre"])}</h1>{corps_html}</div>'
    schemas = [schema_ariane]
    if chemin == "/a-propos/":
        schemas.append({"@context": "https://schema.org", "@type": "AboutPage", "url": URL + chemin,
                        "mainEntity": {**auteur(), "description": SITE["description"],
                                       "knowsAbout": ["stress", "cortisol", "sommeil", "système nerveux", "charge mentale"]}})
    ecrire(chemin.strip("/") + "/index.html",
           page(entete.get("titre_seo") or entete["titre"], entete["description"], chemin, contenu, schemas, nav=nav))


def construire_404():
    contenu = """<div class="etroit"><h1>Page introuvable</h1>
<p>Cette page n'existe pas ou a changé d'adresse.</p>
<p><a class="bouton" href="/articles/">Voir tous les articles</a></p></div>"""
    html_404 = page(f"Page introuvable | {SITE['nom']}", "Cette page n'existe pas.", "/404.html", contenu)
    ecrire("404.html", html_404.replace('content="index, follow', 'content="noindex, follow'))


# ---------------------------------------------------------------- fichiers techniques

def ecrire(rel, contenu, mode="w"):
    chemin = os.path.join(SORTIE, rel)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, mode, encoding="utf-8") as f:
        f.write(contenu)


def construire_fichiers_techniques(articles):
    pages = [("/", SITE["date_publication"]), ("/articles/", max(a["maj"] for a in articles)),
             ("/la-formation/", SITE["date_publication"]),
             ("/guides-gratuits/", SITE["date_publication"]), ("/test-stress-anxiete/", "2026-10-09"), ("/respiration-guidee/", "2026-10-09"), ("/a-propos/", "2026-10-09"), ("/methode-editoriale/", "2026-10-09"),
             ("/mentions-legales/", SITE["date_publication"])]
    pages += [(f"/{th['slug']}/", "2026-10-09") for th in SITE.get("themes", {}).values()]
    pages += [(f"/{a['slug']}/", a["maj"]) for a in articles]
    ecrire("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "".join(f"<url><loc>{URL}{p}</loc><lastmod>{d}</lastmod></url>\n" for p, d in pages)
           + "</urlset>\n")
    robots_ia = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot",
                 "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "CCBot",
                 "Bingbot", "Googlebot"]
    ecrire("robots.txt", "# Le site est ouvert aux moteurs de recherche et aux assistants IA.\n"
           + "".join(f"User-agent: {r}\nAllow: /\n\n" for r in robots_ia)
           + f"User-agent: *\nAllow: /\n\nSitemap: {URL}/sitemap.xml\n")
    # llms.txt (format llmstxt.org) : résumé du site pour les assistants IA.
    lignes = [f"# {SITE['nom']}", "", f"> {SITE['description']}", "",
              f"Site francophone écrit par {SITE['auteur']['nom']} ({SITE['auteur']['role'].lower()}), qui n'est pas "
              "professionnel de santé : chaque article cite ses sources (Inserm, HAS, Assurance maladie, études "
              "publiées) et indique quand consulter. Contenu libre d'accès, sans publicité.", "",
              "## Articles", ""]
    for cle, nom in SITE["categories"].items():
        for a in [a for a in articles if a["categorie"] == cle]:
            lignes.append(f"- [{a['titre']}]({URL}/{a['slug']}/): {a['description']}")
    lignes += ["", "## Thèmes", ""] + [f"- [{th['titre']}]({URL}/{th['slug']}/): {th['description']}"
                                        for th in SITE.get("themes", {}).values()]
    lignes += ["", "## Outils", "",
               f"- [Test de stress et d'anxiété]({URL}/test-stress-anxiete/): questionnaire GAD-7 (7 questions validées, "
               "score de 0 à 21, seuils 5, 10 et 15) suivi de 6 questions d'orientation (nuits, travail, corps) qui "
               "donnent un profil et des priorités. Calcul dans le navigateur, aucune donnée envoyée, pas un diagnostic.",
               f"- [Respiration guidée 4-6]({URL}/respiration-guidee/): trois audios gratuits sans voix (3, 5 et 10 minutes), "
               "sur la musique « Deep Relaxation » de Kevin MacLeod (CC BY 4.0), "
               "pour respirer à 6 respirations par minute (inspirer 4 s, expirer 6 s), avec les études qui fondent ce rythme."]
    lignes += ["", "## Guides gratuits", ""]
    for g in SITE["guides"].values():
        lignes.append(f"- [{g['titre']}]({g['url']}): {g['accroche']} " + " ; ".join(g["points"]) + ".")
    if SITE.get("formation"):
        f = SITE["formation"]
        lignes += ["", "## Formation payante", "",
                   f"- [{f['titre']}]({URL}/la-formation/): programme en ligne pour calmer le mental le soir — "
                   + "; ".join(t for t, _ in f["modules"]) + f". {f['prix']}, {f['prix_detail']}, garantie 7 jours."
                   " Outils de bien-être, pas un traitement médical."]
    lignes += ["", "## Optional", "",
               f"- [Texte intégral de tous les articles]({URL}/llms-full.txt)",
               f"- [À propos de l'auteur]({URL}/a-propos/)", f"- [Méthode éditoriale et choix des sources]({URL}/methode-editoriale/)", f"- [Mentions légales]({URL}/mentions-legales/)", ""]
    ecrire("llms.txt", "\n".join(lignes))
    complet = [f"# {SITE['nom']} — texte intégral des articles", "",
               f"Source : {URL} — chaque article ci-dessous est aussi publié à l'adresse indiquée.", ""]
    for a in articles:
        complet += ["---", "", f"# {a['titre']}", "", f"Adresse : {URL}/{a['slug']}/",
                    f"Mis à jour le {date_fr(a['maj'])} — par {SITE['auteur']['nom']}", "", a["intro"], ""]
        if a["resume"]:
            complet += ["## L'essentiel", ""] + [f"- {p}" for p in a["resume"]] + [""]
        complet += [a["corps_md"], ""]
        if a["faq"]:
            complet += ["## Questions fréquentes", ""] + [f"### {q}\n\n{r}\n" for q, r in a["faq"]]
        if a["sources"]:
            complet += ["## Sources", ""] + [f"{i + 1}. [{t}]({u.replace('(', '%28').replace(')', '%29')})" for i, (t, u) in enumerate(a["sources"])] + [""]
    ecrire("llms-full.txt", "\n".join(complet))
    # Flux RSS.
    items = "".join(
        f"<item><title>{xml_escape(a['titre'])}</title><link>{URL}/{a['slug']}/</link>"
        f"<guid>{URL}/{a['slug']}/</guid><description>{xml_escape(a['description'])}</description>"
        f"<pubDate>{datetime.datetime.fromisoformat(a['date']).strftime('%a, %d %b %Y 08:00:00 +0000')}</pubDate></item>"
        for a in articles)
    ecrire("feed.xml", f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel>'
           f"<title>{xml_escape(SITE['nom'])}</title><link>{URL}/</link><language>fr</language>"
           f"<description>{xml_escape(SITE['description'])}</description>{items}</channel></rss>\n")
    ecrire("CNAME", SITE["domaine"] + "\n")
    ecrire(".nojekyll", "")
    if SITE.get("indexnow"):
        ecrire(f"{SITE['indexnow']}.txt", SITE["indexnow"])
    shutil.copy(os.path.join(RACINE, "contenu", "style.css"), os.path.join(SORTIE, "style.css"))
    shutil.copytree(os.path.join(RACINE, "contenu", "polices"), os.path.join(SORTIE, "polices"))
    shutil.copytree(os.path.join(RACINE, "contenu", "audio"), os.path.join(SORTIE, "audio"))
    ecrire("favicon.svg", LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))
    # Logo PNG (données structurées) et image de partage par défaut.
    logo = Image.new("RGB", (512, 512), "#080C10")
    from PIL import ImageDraw
    d = ImageDraw.Draw(logo)
    d.ellipse((56, 56, 456, 456), fill="#DFD5C6")
    d.ellipse((150, 96, 470, 416), fill="#080C10")
    d.ellipse((40, 40, 472, 472), outline="#8FBF9A", width=10)
    logo.save(os.path.join(SORTIE, "logo.png"), optimize=True)
    defaut = Image.new("RGB", (1200, 630), "#080C10")
    d = ImageDraw.Draw(defaut)
    d.ellipse((80, 165, 380, 465), fill="#DFD5C6")
    d.ellipse((150, 140, 420, 410), fill="#080C10")
    d.ellipse((68, 153, 392, 477), outline="#3A5F43", width=8)
    try:
        from PIL import ImageFont
        police = ImageFont.truetype(os.path.join(DEPOT, "Poppins-Bold.ttf"), 72)
        police2 = ImageFont.truetype(os.path.join(DEPOT, "Poppins-Regular.ttf"), 34)
        d.text((470, 200), SITE["nom"], font=police, fill="#DFD5C6")
        d.text((472, 310), "Ton système nerveux mérite une trêve.", font=police2, fill="#8FBF9A")
    except OSError:
        pass
    os.makedirs(os.path.join(SORTIE, "img"), exist_ok=True)
    for nom in os.listdir(os.path.join(RACINE, "contenu", "img")):
        shutil.copy(os.path.join(RACINE, "contenu", "img", nom), os.path.join(SORTIE, "img", nom))
    defaut.save(os.path.join(SORTIE, "img", "og-defaut.jpg"), quality=85)


def main():
    if os.path.isdir(SORTIE):
        shutil.rmtree(SORTIE)
    os.makedirs(SORTIE)
    dossier = os.path.join(RACINE, "contenu", "articles")
    articles = [lire_article(os.path.join(dossier, f)) for f in sorted(os.listdir(dossier)) if f.endswith(".md")]
    ordre = list(SITE["articles"])
    articles.sort(key=lambda a: ordre.index(a["slug"]) if a["slug"] in ordre else len(ordre))
    for a in articles:
        a["images"] = preparer_image(a["image"])
        a["epingle"] = image_epingle(a) if a["images"] else None
    for a in articles:
        construire_article(a, articles)
    construire_accueil(articles)
    construire_liste(articles)
    for cle in SITE.get("themes", {}):
        construire_theme(cle, articles)
    construire_guides()
    construire_test(articles)
    construire_respiration()
    if SITE.get("formation"):
        construire_formation()
    construire_page_fixe("a-propos.md", "/a-propos/", nav="/a-propos/")
    construire_page_fixe("methode-editoriale.md", "/methode-editoriale/")
    mentions = open(os.path.join(RACINE, "contenu", "pages", "mentions-legales.md"), encoding="utf-8").read()
    if balise_mesure() and "n'utilise aucun outil de mesure d'audience" in mentions:
        sys.exit("Mesure d'audience activée : mettre d'abord à jour les mentions légales (elles disent « aucun outil de mesure d'audience »).")
    construire_page_fixe("mentions-legales.md", "/mentions-legales/")
    construire_404()
    construire_fichiers_techniques(articles)
    print(f"{len(articles)} articles construits dans site/_build/ :",
          ", ".join(f"{a['slug']} ({a['mots']} mots, {len(a['sources'])} sources)" for a in articles))


if __name__ == "__main__":
    main()
