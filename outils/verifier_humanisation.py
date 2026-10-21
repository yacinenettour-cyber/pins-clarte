"""Contrôle d'une réécriture de style d'un article du site (docs/referencement/style-humain.md, 21/10/2026).
Compare la version réécrite à une version de référence (git) : en-tête, liens, citations, chiffres, sources, tableaux
et parties obligatoires doivent rester identiques ; la longueur ne doit pas varier de plus de 10 %.
Usage : python3 outils/verifier_humanisation.py <ref git, ex. origin/main> <article.md> [...]"""
import collections, re, subprocess, sys


def parties(txt):
    m = re.match(r"---\n(.*?)\n---\n(.*)", txt, re.S)
    return m.group(1), m.group(2)


def sources(corps):
    i = corps.find("## Sources")
    return corps[i:] if i >= 0 else ""


def sans_sources(corps):
    i = corps.find("## Sources")
    return corps[:i] if i >= 0 else corps


def nombres(t):
    # chiffres du texte (hors numéros de citation et adresses de liens)
    t = re.sub(r"\]\([^)]*\)", "]", t)
    t = re.sub(r"\[\d+\]", "", t)
    return collections.Counter(re.findall(r"\d+(?:[,.]\d+)?", t))


def controler(ref, chemin):
    avant = subprocess.run(["git", "show", f"{ref}:{chemin}"], capture_output=True, text=True, check=True).stdout
    apres = open(chemin, encoding="utf-8").read()
    (ea, ca), (eb, cb) = parties(avant), parties(apres)
    err = []
    if ea != eb:
        err.append("en-tête modifié")
    if sources(ca) != sources(cb):
        err.append("liste des sources modifiée")
    ta, tb = sans_sources(ca), sans_sources(cb)
    la_, lb_ = set(re.findall(r"\]\(([^)]+)\)", ta)), set(re.findall(r"\]\(([^)]+)\)", tb))
    if la_ != lb_:
        err.append(f"liens différents : {la_ ^ lb_}")
    ca_, cb_ = collections.Counter(re.findall(r"\[(\d+)\]", ta)), collections.Counter(re.findall(r"\[(\d+)\]", tb))
    if set(ca_) != set(cb_):
        err.append(f"citations différentes : {set(ca_) ^ set(cb_)}")
    na, nb = nombres(ta), nombres(tb)
    if set(na) != set(nb):
        err.append(f"chiffres différents : en moins {sorted(set(na) - set(nb))}, en plus {sorted(set(nb) - set(na))}")
    for titre in ("## L'essentiel", "Quand consulter", "## Questions fréquentes"):
        if (titre in ta) != (titre in tb):
            err.append(f"partie « {titre} » ajoutée ou retirée")
    if ta.count("\n|") != tb.count("\n|"):
        err.append(f"lignes de tableau : {ta.count(chr(10) + '|')} → {tb.count(chr(10) + '|')}")
    la, lb = len(ta.split()), len(tb.split())
    if abs(lb - la) > 0.10 * la:
        err.append(f"longueur {la} → {lb} mots")
    for mot in ("électricien", "Autrement dit", "Voici ce que l'on sait", "Il est important de noter"):
        if mot in tb:
            err.append(f"formule à éviter encore présente : « {mot} »")
    return err, la, lb


if __name__ == "__main__":
    ref, ok = sys.argv[1], True
    for chemin in sys.argv[2:]:
        err, la, lb = controler(ref, chemin)
        ok &= not err
        print(("OK " if not err else "ÉCHEC ") + f"{chemin} ({la} → {lb} mots)" + "".join("\n  - " + x for x in err))
    sys.exit(0 if ok else 1)
