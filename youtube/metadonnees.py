"""Titre, description et chapitres YouTube. Module léger (sans dépendance lourde) : il sert à la fabrication,
à la mise en ligne et à la remise à jour des métadonnées juste avant le passage en public."""
import json, os
from commun import DEPOT, CHAINE, mmss

SITE_JSON = os.path.join(DEPOT, "site", "contenu", "site.json")


def chapitres(tl):
    ch = ["00:00 Introduction"] + [f"{mmss(t['debut'])} {t['texte']}" for t in tl["titres"]]
    ch.append(f"{mmss(tl['fin_voix'] + 3)} Musique seule pour s'endormir")
    return ch


def liens(plan):
    """Liens placés juste sous la première phrase (seule partie visible sans « Plus ») : article, guide, audios."""
    y, site = plan["youtube"], "https://www.contactapaisement-mental.fr"
    out = []
    if plan.get("article"):
        out.append(f"📖 {y.get('libelle_article', 'L’article complet, sources citées')} : {site}{plan['article']}")
    if y.get("guide") == "sommeil":
        # seule offre du site (CLAUDE.md) ; texte = contenu réel du guide
        g = json.load(open(SITE_JSON))["guides"]["sommeil"]
        out.append(f"🌙 Guide gratuit « {g['titre']} » : une routine anti-rumination à faire au lit, des exercices pour "
                   f"calmer le mental le soir, un calendrier de 30 jours → "
                   f"{g['url']}?utm_source=youtube&utm_medium=video&utm_campaign={plan['slug']}")
    out.append(f"🎧 Audios de respiration guidée gratuits : {site}/respiration-guidee/")
    return "\n".join(out)


def description(plan, tl):
    y = plan["youtube"]
    morceaux = []
    if y.get("accroche"):
        morceaux += [y["accroche"].strip(), liens(plan)]
    morceaux.append(y["description"].strip())
    if tl:
        morceaux.append("\n".join(chapitres(tl)))
    morceaux.append(y.get("rappel", "À écouter allongé, au calme, jamais en conduisant. Cette vidéo ne remplace pas un avis médical : "
                                    "si tes difficultés de sommeil durent ou pèsent sur tes journées, parles-en à ton médecin. "
                                    "Je ne suis pas professionnel de santé."))
    if y.get("accroche"):
        morceaux.append(f"🔔 Abonne-toi pour recevoir les prochaines méditations : https://www.youtube.com/{CHAINE}?sub_confirmation=1")
    if y.get("sources"):
        morceaux.append("Sources :\n" + "\n".join("· " + s for s in y["sources"]))
    photographes = ", ".join(dict.fromkeys(p["photographe"] for p in plan["photos"] if p.get("photographe")))
    voix = ("Voix : voix de synthèse ElevenLabs (elevenlabs.io), voix « Mila ».\n" if plan.get("voix") == "elevenlabs_mila" else
            "Voix : voix de synthèse (Chatterbox Multilingual, Resemble AI, licence MIT ; voix de référence française "
            "issue du corpus SIWIS, CC BY 4.0).\n" if plan.get("voix") == "chatterbox_francais" else
            "Voix : voix de synthèse (Chatterbox Multilingual, Resemble AI, licence MIT).\n"
            if str(plan.get("voix", "")).startswith("chatterbox") else
            "Voix : voix de synthèse (Kokoro, licence Apache 2.0 ; voix « ff_siwis » issue du corpus SIWIS, CC BY 4.0).\n")
    morceaux.append(voix +
                    "Musique : « Deep Relaxation », Kevin MacLeod (incompetech.com), licence Creative Commons Attribution 4.0 "
                    "http://creativecommons.org/licenses/by/4.0/\n"
                    f"Photos : Unsplash ({photographes}). Bols chantants : Freesound, domaine public (CC0).")
    morceaux.append(" ".join(y.get("hashtags", ["#méditation", "#sommeil", "#méditationguidée"])))
    return "\n\n".join(morceaux)


def timeline(slug):
    """Timeline gardée dans le dossier du plan par la fabrication (le dossier de travail n'existe plus après)."""
    p = os.path.join(DEPOT, "videos_youtube", slug, "timeline.json")
    return json.load(open(p)) if os.path.exists(p) else None
