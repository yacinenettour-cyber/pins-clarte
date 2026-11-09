"""Contrôle de style « humain » d'un article du site (09/11/2026), d'après docs/referencement/style-humain.md.

Repère les tics qui font « texte généré » : formules toutes faites, tirets cadratins, points d'exclamation, mots anglais,
phrases toutes de la même longueur, deux-points et points-virgules en série, paragraphes bâtis sur le même moule
(« Selon une étude… »). Ne juge ni les faits ni les sources (voir verifier_humanisation.py et la relecture des études).

Usage : python3 outils/controle_style_article.py site/contenu/articles/<slug>.md [autre.md ...]
Sortie : une ligne par alerte, puis « OK » ou « À REPRENDRE ». Code de sortie 1 si au moins un article est à reprendre.
Seuils calibrés le 09/11/2026 sur les 26 articles existants (voir docs/referencement/style-humain.md)."""
import re, statistics, sys

FORMULES = [
    "voici ce que l'on sait", "autrement dit", "il est important de noter", "en résumé", "que tu sois", "bonne nouvelle",
    "le point clé", "pas de panique", "le hic", "concrètement", "en clair", "c'est là qu'intervient", "le secret ?",
    "voyons ", "passons à", "il convient de", "n'hésite pas à", "en conclusion", "force est de constater",
    "dans un monde où", "à l'ère de", "plongeons", "découvrons", "sans plus attendre",
]
ANGLAIS = [
    "mindfulness", "bedtime procrastination", "hyperarousal", "coaching", "feedback", "insight", "tips", "boost",
    "self-care", "mindset", "burnout", "routine morning", "wellness", "workflow", "lifestyle", "deadline", "must-have",
]


def corps_lisible(txt):
    """Texte courant : sans en-tête, tableaux, listes de sources, titres, code ni liens (le texte des liens est gardé)."""
    m = re.match(r"---\n.*?\n---\n(.*)", txt, re.S)
    t = m.group(1) if m else txt
    i = t.find("## Sources")
    if i >= 0:
        t = t[:i]
    lignes = []
    for l in t.splitlines():
        s = l.strip()
        if not s or s.startswith(("|", "#", ">", "```", "<")) or re.match(r"^[-*]\s", s) or re.match(r"^\d+\.\s", s):
            continue
        lignes.append(s)
    t = "\n".join(lignes)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"\[\d+(?:,\s*\d+)*\]", "", t)
    t = re.sub(r"[*_`]", "", t)
    return t


def phrases(t):
    return [p.strip() for p in re.split(r"(?<=[.!?…])\s+", t.replace("\n", " ")) if len(p.split()) >= 2]


def controler(chemin):
    brut = open(chemin, encoding="utf-8").read()
    t = corps_lisible(brut)
    bas = t.lower()
    mots = len(t.split())
    alertes = []
    for f in FORMULES:
        n = bas.count(f)
        if n:
            alertes.append(f"formule toute faite « {f.strip()} » ×{n}")
    for a in ANGLAIS:
        if re.search(rf"\b{re.escape(a)}\b", bas):
            alertes.append(f"mot anglais « {a} »")
    tirets = t.count("—")
    if tirets > 2:
        alertes.append(f"{tirets} tirets cadratins (2 au plus)")
    if t.count("!") > 0:
        alertes.append(f"{t.count('!')} point(s) d'exclamation")
    if re.search(r"(?:^|[.!?]\s)Et si [^.?!]*\?", t.replace("\n", " ")):
        alertes.append("question rhétorique « Et si… ? » (tic de dialogue d'IA)")
    trans = len(re.findall(r"(?:^|[.!?]\s)Et si (?:c'est|ce sont|tu|ton|ta|tes)\b", t.replace("\n", " ")))
    if trans >= 2:
        alertes.append(f"transition « Et si c'est… » répétée ×{trans} (varier les renvois entre articles)")
    ph = phrases(t)
    if len(ph) >= 12:
        lg = [len(p.split()) for p in ph]
        cv = statistics.pstdev(lg) / statistics.mean(lg)
        courtes = sum(1 for x in lg if x <= 7)
        if cv < 0.45:
            alertes.append(f"phrases trop régulières (variation de longueur {cv:.2f}, 0,45 au moins)")
        if courtes / len(lg) < 0.08:
            alertes.append(f"presque aucune phrase courte ({courtes} sur {len(lg)} font 7 mots ou moins)")
        if max(lg) > 55:
            alertes.append(f"phrase de {max(lg)} mots (55 au plus)")
    if mots:
        dp = t.count(":") / mots * 1000
        pv = t.count(";") / mots * 1000
        if dp > 9:
            alertes.append(f"deux-points en série ({dp:.1f} pour 1000 mots, 9 au plus)")
        if pv > 3:
            alertes.append(f"points-virgules en série ({pv:.1f} pour 1000 mots, 3 au plus)")
    selon = len(re.findall(r"(?i)\bselon (?:une|l'|la|des)\s+(?:étude|enquête|revue|équipe)", t))
    if selon >= 4:
        alertes.append(f"« Selon une étude… » ×{selon} : varier la façon de raconter les études")
    # débuts de phrase : on ignore les noms d'institutions (NHS, INRS, INSV, Inserm…), qui reviennent naturellement
    debuts = []
    for p in ph:
        brut = re.sub(r"[^\w' ]+", " ", p).replace("'", " ").split()[:2]
        if len(brut) == 2 and (brut[1].isupper() or brut[1] in ("Inserm", "Ameli", "OMS", "HAS")):
            continue
        debuts.append([w.lower() for w in brut])
    repet = {}
    for d in debuts:
        if len(d) == 2:
            repet[" ".join(d)] = repet.get(" ".join(d), 0) + 1
    for d, n in repet.items():
        if n >= 6 and d not in ("tu peux", "tu as", "il y", "c est", "ça "):
            alertes.append(f"{n} phrases commencent par « {d} »")
    return mots, len(ph), alertes


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    reprendre = 0
    for c in sys.argv[1:]:
        mots, nph, al = controler(c)
        print(f"{c} : {mots} mots, {nph} phrases")
        for a in al:
            print("  -", a)
        print("  ", "OK" if not al else "À REPRENDRE")
        reprendre += bool(al)
    sys.exit(1 if reprendre else 0)
