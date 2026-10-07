"""Contrôle anti-doublons appelé par les workflows avant toute publication (pins.yml, videos.yml).

Un titre est refusé s'il ressemble à un titre déjà publié ou prévu ailleurs :
- même titre une fois normalisé (casse, accents, ponctuation, émojis) ;
- titre très proche (difflib.SequenceMatcher >= SEUIL_TEXTE, règle n°1 du CLAUDE.md) ;
- même sujet : au moins MOTS_COMMUNS_MIN mots importants en commun et
  recouvrement >= SEUIL_SUJET (repère les reformulations du même sujet).

Références : historique.json, historique_videos.json, titres des kits Idea Pins,
titres_en_ligne.json (instantané des pins en ligne) et, si la clé Composio est fournie,
la liste réelle des pins du compte lue au moment du run (pins publiés par un autre moyen).
Une image finale identique (md5) à une image déjà publiée est aussi refusée.
"""
import difflib, glob, hashlib, json, os, re, unicodedata

SEUIL_TEXTE = 0.72
SEUIL_SUJET = 0.6
MOTS_COMMUNS_MIN = 3

MOTS_VIDES = set("""le la les un une des de du d l a au aux et ou en pour par sur sans avec ce ces cet cette
ton ta tes son sa ses te tu toi qui que quoi quand dans est sont pas plus moins ne n se s y il elle on
vraiment simple simples comment pourquoi ca c qu j m t mon ma mes vous votre vos nous meme tout tous toute
fait faire avant apres entre jamais trop tres bien vrai vraie ce quel quelle quels quelles ici voici
geste gestes facon facons astuce astuces technique techniques methode methodes exercice exercices etape etapes
cle cles levier leviers conseil conseils secret secrets habitude habitudes chose choses moyen moyens idee idees
reflexe reflexes outil outils action actions solution solutions minute minutes seconde secondes jour jours
quotidien naturellement naturel naturelle rapide rapidement express efficace efficaces concret concrets
concretes simple facile faciles doux douce douces petit petite petits petites vite enfin encore
toujours souvent sait sais saches remarques remarque realise ignores ignore cache caches cachee cachees""".split())

# Variantes d'un même mot ramenées à une seule forme (repère les reformulations d'un même sujet).
SYNONYMES = {
    "signaux": "signe", "signal": "signe", "symptome": "signe", "symptomes": "signe", "indice": "signe",
    "indices": "signe", "signes": "signe",
    "stimuler": "activer", "stimule": "activer", "reveiller": "activer", "active": "activer",
    "apaiser": "calmer", "apaise": "calmer", "apaisent": "calmer", "detendre": "calmer", "calme": "calmer",
    "calment": "calmer", "relacher": "calmer", "redescendre": "calmer", "baisser": "calmer", "reduire": "calmer",
    "stresse": "stress", "stressee": "stress", "stres": "stress", "stresses": "stress", "anxiete": "stress",
    "dormir": "sommeil", "endormir": "sommeil", "endormissement": "sommeil", "nuit": "sommeil", "nuits": "sommeil",
    "coucher": "soir", "soiree": "soir", "lit": "soir",
    "rumination": "ruminer", "ruminations": "ruminer", "rumines": "ruminer", "boucle": "ruminer",
    "pensees": "ruminer", "penser": "ruminer",
    "epuise": "fatigue", "epuisement": "fatigue", "fatigues": "fatigue", "vide": "fatigue", "lessive": "fatigue",
    "sature": "surcharge", "saturation": "surcharge", "deborde": "surcharge", "plein": "surcharge",
    "procrastiner": "procrastination", "procrastines": "procrastination", "repousser": "procrastination",
    "reporter": "procrastination", "repousses": "procrastination",
    "cerveau": "mental", "tete": "mental", "esprit": "mental",
    "respirations": "respiration", "respirer": "respiration", "respire": "respiration", "expiration": "respiration",
    "aliment": "alimentation", "aliments": "alimentation", "manger": "alimentation", "assiette": "alimentation",
    "repas": "alimentation", "diner": "alimentation", "nutriments": "alimentation",
    "ecran": "ecrans", "telephone": "ecrans", "scroll": "ecrans", "scroller": "ecrans",
    "reveil": "matin", "reveiller": "matin", "matinee": "matin",
}


def normaliser(titre):
    t = unicodedata.normalize("NFD", (titre or "").lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return " ".join(re.findall(r"[a-z0-9]+", t))


def mots_cles(titre):
    mots = set()
    for m in normaliser(titre).split():
        if m.isdigit() or m in MOTS_VIDES or len(m) < 3:
            continue
        m = SYNONYMES.get(m, m)
        if m in MOTS_VIDES:
            continue
        mots.add(SYNONYMES.get(m[:-1], m[:-1]) if m.endswith("s") and len(m) > 4 and m not in SYNONYMES.values() else m)
    return mots


def _titres_json(chemin, cle="titre"):
    if not os.path.exists(chemin):
        return []
    try:
        donnees = json.load(open(chemin, encoding="utf-8"))
    except Exception:
        return []
    if isinstance(donnees, dict):
        donnees = donnees.get("titres", [])
    return [d.get(cle) if isinstance(d, dict) else d for d in donnees if (d.get(cle) if isinstance(d, dict) else d)]


def titres_kits():
    titres = []
    for f in sorted(glob.glob("kits_idea_pins/*/texte.txt")):
        premiere = open(f, encoding="utf-8").readline().strip()
        titres.append(premiere.replace("KIT IDEA PIN — ", "", 1))
    return titres


def entite_composio(cle):
    """Identifiant du compte Pinterest connecté dans Composio (même logique que les workflows)."""
    import requests
    entite = "pg-test-a2a2217a-e3a1-439a-aabd-cc16b6182094"
    try:
        comptes = requests.get(
            "https://backend.composio.dev/api/v3/connected_accounts",
            headers={"x-api-key": cle}, params={"toolkit_slugs": "pinterest"}, timeout=30,
        ).json().get("items", [])
        actifs = [c for c in comptes if c.get("status") == "ACTIVE" and c.get("user_id")]
        if actifs:
            entite = actifs[0]["user_id"]
    except Exception as e:
        print("Anti-doublons : lecture des comptes connectés impossible :", e)
    return entite


def filtrer(candidats, references, cle_titre="titre", deja_utilisees=()):
    """Garde les candidats sans doublon ; affiche chaque candidat écarté et la raison."""
    gardes = []
    for c in candidats:
        doublon, raison = est_doublon(c[cle_titre], references)
        if not doublon and c.get("image_prete") and c["image_prete"] in deja_utilisees:
            doublon, raison = True, "image déjà publiée : " + c["image_prete"]
        if doublon:
            print("Écarté (doublon) :", c[cle_titre], "→", raison)
        else:
            gardes.append(c)
    return gardes


def titres_en_ligne_live(cle, entite, max_pages=8):
    """Titres réellement en ligne, lus via Composio. Liste vide si la lecture échoue."""
    import requests
    titres, signet = [], None
    for _ in range(max_pages):
        arguments = {"page_size": 250}
        if signet:
            arguments["bookmark"] = signet
        r = requests.post(
            "https://backend.composio.dev/api/v3.1/tools/execute/PINTEREST_LIST_PINS",
            headers={"x-api-key": cle, "Content-Type": "application/json"},
            json={"arguments": arguments, "entity_id": entite}, timeout=60,
        )
        donnee = (r.json() or {}).get("data") or {}
        elements = donnee.get("items") or []
        titres += [e.get("title") for e in elements if e.get("title")]
        signet = donnee.get("next_cursor") or donnee.get("bookmark")
        if not signet or not elements:
            break
    return titres


def charger_references(cle_composio=None, entite=None, exclure_kits=False):
    refs = [(t, "historique pins") for t in _titres_json("historique.json")]
    refs += [(t, "historique vidéos") for t in _titres_json("historique_videos.json")]
    refs += [(t, "pins en ligne (instantané)") for t in _titres_json("titres_en_ligne.json")]
    if not exclure_kits:
        refs += [(t, "kit Idea Pin") for t in titres_kits()]
    if cle_composio and entite:
        try:
            en_ligne = titres_en_ligne_live(cle_composio, entite)
            print(f"Anti-doublons : {len(en_ligne)} titres lus en direct sur Pinterest.")
            refs += [(t, "pins en ligne (lecture directe)") for t in en_ligne]
        except Exception as e:
            print("Anti-doublons : lecture directe de Pinterest impossible, instantané utilisé :", e)
    vus, uniques = set(), []
    for t, s in refs:
        if (t, s) not in vus:
            vus.add((t, s))
            uniques.append((t, s, normaliser(t), mots_cles(t)))
    return uniques


def est_doublon(titre, references, ignorer=None):
    """Renvoie (True, raison) si le titre double une référence, sinon (False, "")."""
    n, mots = normaliser(titre), mots_cles(titre)
    for t, source, n_ref, mots_ref in references:
        if ignorer and t == ignorer:
            continue
        if n == n_ref:
            return True, f"titre identique à « {t} » ({source})"
        sm = difflib.SequenceMatcher(None, n, n_ref)
        if sm.real_quick_ratio() >= SEUIL_TEXTE and sm.quick_ratio() >= SEUIL_TEXTE:
            ratio = sm.ratio()
            if ratio >= SEUIL_TEXTE:
                return True, f"titre trop proche ({ratio:.2f}) de « {t} » ({source})"
        communs = mots & mots_ref
        if mots and mots_ref and len(communs) >= MOTS_COMMUNS_MIN:
            recouvrement = len(communs) / min(len(mots), len(mots_ref))
            if recouvrement >= SEUIL_SUJET and len(communs) / len(mots | mots_ref) >= 0.5:
                return True, f"même sujet que « {t} » ({source}) : {', '.join(sorted(communs))}"
    return False, ""


def empreinte(chemin):
    return hashlib.md5(open(chemin, "rb").read()).hexdigest()


def image_deja_publiee(chemin, historique):
    """True si une image identique (même fichier, octet pour octet) a déjà été publiée."""
    if not os.path.exists(chemin):
        return False
    e = empreinte(chemin)
    for h in historique:
        if h.get("md5") == e:
            return True
        ancienne = h.get("image") or h.get("cover")
        if ancienne and os.path.exists(ancienne) and ancienne != chemin and empreinte(ancienne) == e:
            return True
    return False
