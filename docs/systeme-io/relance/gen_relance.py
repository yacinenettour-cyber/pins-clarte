# Génère les e-mails 11 à 13 de la « Séquence Lead Magnet » (relance 14 jours après l'e-mail 10)
# et la nouvelle version de l'e-mail 10, au format HTML des e-mails existants.
# Sortie : relance.json (lu par le script de publication dans le bac à sable).
import json, os

URL = "https://lp.contactapaisement-mental.fr/689e4290"
P = '<p style="margin:0 0 14px 0;font-size:15px;line-height:1.55;">'
UL = '<ul style="margin:0 0 14px 0;padding-left:22px;font-size:15px;line-height:1.55;">'
LI = '<li style="margin-bottom:6px;">'
PS = '<p style="margin:18px 0 0 0;font-size:13px;line-height:1.5;color:#777777;">'
PS_CLIENT = PS + "P.S. Si tu as déjà rejoint le programme, merci pour ta confiance : tu peux simplement ignorer ce message.</p>"


def para(t): return P + t + "</p>"
def liste(items): return UL + "".join(LI + i + "</li>" for i in items) + "</ul>"
def bouton(label): return ('<p style="margin:22px 0;text-align:center;"><a href="' + URL + '" target="_blank" style="display:inline-block;'
                           'background:#3d4f8f;color:#ffffff;padding:13px 24px;border-radius:8px;text-decoration:none;font-weight:bold;font-size:16px;">'
                           + label + "</a></p>")
def corps(*blocs): return '<div style="font-family:Arial,Helvetica,sans-serif;color:#222222;max-width:600px;">' + "".join(blocs) + "</div>"


E11 = {"subject": "3 gestes pour ce soir 🌙", "previewText": "Même si le guide dort au fond de ta boîte mail.", "html": corps(
    para("Bonjour,"),
    para("Ça fait un moment que je ne t'ai pas écrit. Tu avais téléchargé le guide « Quand le cerveau refuse de dormir » : il est peut-être au fond de ta boîte mail aujourd'hui. Ce n'est pas grave."),
    para("Voici 3 gestes simples pour ce soir, même sans relire le guide :"),
    liste(["<strong>Vider ta tête sur papier</strong>, une heure avant le coucher : tâches, soucis, idées. Une fois écrit, ça tourne moins dans la tête.",
           "<strong>Allonger l'expiration</strong> : inspire sur 4 temps, expire sur 6 à 8 temps, pendant 2 minutes. C'est un signal simple pour dire au corps qu'il peut relâcher.",
           "<strong>Ne pas lutter</strong> : si le sommeil ne vient pas au bout de 20 minutes, lève-toi, reste en lumière douce, et reviens au lit quand la tension baisse."]),
    para("Tu n'as pas besoin de tout faire. Un seul geste ce soir, c'est suffisant."),
    para("Une question, si tu as 10 secondes : <strong>qu'est-ce qui t'empêche le plus de dormir en ce moment ?</strong> Les pensées qui tournent, les réveils la nuit, la tension dans le corps ? Réponds simplement à cet e-mail, je lis tous les messages."),
    para("Prends soin de toi,<br>Yacine — Clarté Mentale"),
    PS + "P.S. Dans quelques jours, je t'écris à propos d'un réveil qui revient chez beaucoup de gens : celui de 4 h du matin.</p>")}

E12 = {"subject": "Réveillé(e) vers 4 h, presque chaque nuit ?", "previewText": "Pourquoi ce réveil s'installe, et comment le faire reculer.", "html": corps(
    para("Bonjour,"),
    para("Comme promis, parlons de ce réveil qui revient vers 4 ou 5 h du matin, les yeux grands ouverts, avec le mental qui démarre."),
    para("<strong>Pourquoi le petit matin est fragile.</strong> La seconde moitié de la nuit contient moins de sommeil profond : on se réveille plus facilement. Et en fin de nuit, l'hormone qui prépare l'éveil commence naturellement à remonter. Chez quelqu'un de stressé, ça suffit parfois à rallumer les pensées. Puis l'habitude s'installe : le cerveau finit par <em>attendre</em> ce réveil."),
    para("<strong>3 choses à vérifier :</strong>"),
    liste(["<strong>Tu te couches tôt pour « compenser » ?</strong> Couché(e) à 21 h 30 avec 7 heures de besoin, se réveiller vers 4 h 30 est logique. Recule ton coucher de 15 à 30 minutes.",
           "<strong>Un verre le soir ?</strong> L'alcool aide à s'endormir, puis rend la fin de nuit plus agitée.",
           "<strong>Ta chambre s'éclaire tôt ?</strong> Rideaux occultants ou masque de nuit, jusqu'à ton heure de lever."]),
    para("<strong>Et à 4 h :</strong> ne regarde pas l'heure, fais quelques longues expirations, relâche la mâchoire et les épaules. Si tu es bien réveillé(e) et agacé(e), lève-toi en lumière douce et reviens quand tes paupières sont lourdes."),
    para("Si ce réveil s'accompagne d'un moral bas qui dure, parles-en à ton médecin : ça se soigne."),
    para("C'est l'une des leçons de mon programme « Quand le cerveau refuse de dormir », avec un plan sur deux semaines pour faire reculer ce réveil. Je t'en parle plus en détail dans quelques jours."),
    bouton("Découvrir le programme — 37 €"),
    para("Bonne soirée,<br>Yacine — Clarté Mentale"),
    PS_CLIENT)}

E13 = {"subject": "Ce qu'il y a dans le programme (dernier e-mail sur le sujet)", "previewText": "37 €, garantie 7 jours, et je te dis tout honnêtement.", "html": corps(
    para("Bonjour,"),
    para("Voici ce que contient le programme « Quand le cerveau refuse de dormir » :"),
    liste(["<strong>Apaiser le système nerveux</strong> : soupir physiologique, relâchement musculaire, scan corporel, pour faire redescendre la pression le soir même.",
           "<strong>Sortir des ruminations</strong> sans lutter contre tes pensées : rendez-vous des soucis, liste de demain, mélange cognitif.",
           "<strong>Ton rituel du soir</strong> en 3 versions (3, 10 ou 20 minutes) selon ton énergie.",
           "<strong>Consolider le sommeil</strong> : les réveils nocturnes, le matin qui prépare la nuit, et quand en parler à un professionnel.",
           "<strong>Et si c'est ton cas ?</strong> : le travail qui te suit jusqu'au lit, les nuits hachées de parent, les horaires décalés, le réveil de 4 h, les périodes de gros stress.",
           "<strong>Un parcours de 28 soirs</strong> (une seule action par soir, déjà choisie pour toi), des audios guidés et un kit de 7 fiches à imprimer."]),
    para("<strong>37 €</strong>, en une seule fois, sans abonnement. Accès immédiat depuis ton téléphone, et à vie."),
    para("Je préfère être honnête : le programme est récent, je n'ai pas encore d'avis de clients à te montrer. C'est pour ça qu'il y a une <strong>garantie de 7 jours</strong> : si tu ne ressens aucune amélioration, un simple e-mail suffit et tu es remboursé(e), sans justification."),
    bouton("Rejoindre le programme — 37 €, garantie 7 jours"),
    para("Ce n'est pas un traitement médical et ça ne remplace pas l'avis d'un professionnel de santé : ce sont des outils de bien-être, à ton rythme."),
    para("C'est le dernier e-mail où je t'en parle. Et si ce n'est pas le bon moment, c'est très bien aussi : garde les 3 gestes du premier e-mail pour les soirs difficiles."),
    para("Prends soin de toi,<br>Yacine — Clarté Mentale"),
    PS_CLIENT)}

# E-mail 10 : il annonçait « le dernier e-mail où je te parle du programme », faux avec les relances 11 à 13.
E10_AVANT = ("C'est le dernier e-mail où je te parle du programme « Quand le cerveau refuse de dormir ». "
             "Ensuite, tu recevras seulement des conseils gratuits sur le sommeil et le stress, de temps en temps.")
E10_APRES = "Voici l'essentiel sur le programme « Quand le cerveau refuse de dormir », en quelques lignes."
E10 = {"subject": "Si tu hésites encore", "previewText": "L'essentiel sur le programme, en 3 lignes.", "avant": E10_AVANT, "apres": E10_APRES}

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "relance.json")
    json.dump({"e11": E11, "e12": E12, "e13": E13, "e10": E10, "delais_jours": [14, 3, 3], "heure": "19:30"},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ok", out)
