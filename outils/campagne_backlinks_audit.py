"""Audit des 100 sites fournis par l'utilisateur (campagne de liens gratuits, 01/11/2026).

Données relevées le 01/11/2026 par requêtes HTTP directes (atelier Composio, Python requests) : code HTTP, adresse
finale, titre, dernière date <lastmod> du plan du site, liens « contact / contribution / partenariat » de la page
d'accueil, puis lecture des pages contact ou contribution repérées. Popularité : liste publique Tranco (identifiant
7462X, 1 million de domaines, période du 02/10 au 31/10/2026, https://tranco-list.eu/) : c'est un rang mondial
de popularité, pas un trafic. Ahrefs et Semrush sont payants : DR, Authority Score, trafic et domaines référents
sont indiqués « Non disponible » (consigne « ne rien payer », aucune donnée inventée).

Notes : pertinence /30, qualité /20 et collaboration gratuite /20 sont des jugements argumentés dans la colonne
Commentaires ; audience française /15 et potentiel SEO /15 sont déduits du rang Tranco (barème plus bas), faute de
mesure de trafic gratuite et fiable. Lancer : python3 outils/campagne_backlinks_audit.py
"""
import json, os
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

DOSSIER = os.path.join(os.path.dirname(__file__), "..", "docs", "referencement", "campagne-backlinks-2026-11")
DATE = "01/11/2026"
TRANCO = json.load(open(os.path.join(DOSSIER, "tranco-2026-10-31.json")))
ND = "Non disponible"

# n: (nom, url initiale, url finale, fonctionnel, activité, contribution gratuite, preuve, contact,
#     pertinence/30, qualité/20, collaboration/20, statut, commentaire, domaine Tranco)
S = {
 1: ("Réseau Morphée", "https://www.reseau-morphee.fr/", "https://reseau-morphee.fr/", "Oui", "Oui (plan du site : 11/09/2026 ; blog, forum)", "Non annoncée", "https://reseau-morphee.fr/ (page Ressources, blog du réseau)", "contact@reseau-morphee.fr", 28, 18, 7, "Actif mais opportunité non confirmée", "Réseau de santé du sommeil reconnu. Déjà contacté (voir l'historique), sans réponse : pas de nouveau message avant 2 mois. Angle possible : proposer les audios CC BY pour leur page Ressources.", "reseau-morphee.fr"),
 2: ("Institut National du Sommeil et de la Vigilance (INSV)", "https://institut-sommeil-vigilance.org/", "https://institut-sommeil-vigilance.org/", "Oui", "Oui (plan du site : 19/10/2026)", "Non (mécénat et partenariats institutionnels)", "https://institut-sommeil-vigilance.org/contact/", "contact@insv.org", 28, 20, 4, "Actif mais opportunité non confirmée", "Référence nationale (Journée du sommeil). Écarté le 12/10 : pas de contenus externes. Seule piste : participation aux enquêtes ou relais de la Journée du sommeil (mars 2027) avec une ressource, sans attente de lien.", "institut-sommeil-vigilance.org"),
 3: ("Société Française de Recherche et Médecine du Sommeil (SFRMS)", "https://www.sfrms.org/", "https://www.sfrms-sommeil.org/", "Oui (https sur sfrms.org en échec, redirection depuis http vers sfrms-sommeil.org, même société savante)", "Oui (actualités 2026)", "Non (société savante de médecins et chercheurs)", "https://www.sfrms-sommeil.org/", "contact@sfrms.org", 28, 20, 1, "Hors sujet", "Public de professionnels du sommeil ; aucun contenu grand public externe. Pas une cible pour un site non professionnel de santé.", None),
 4: ("Association Sommeil et Santé", "https://www.sommeilsante.asso.fr/", "https://www.sommeilsante.asso.fr/", "Oui", "Non : dernière actualité annoncée en mars 2023, pas de plan du site", "Non annoncée", "https://www.sommeilsante.asso.fr/", "contact@sommeilsante.asso.fr", 26, 10, 4, "Actif mais opportunité non confirmée", "Site en ligne mais figé depuis 2023 : faible intérêt, réponse peu probable.", None),
 5: ("Sommeil.org", "https://www.sommeil.org/", "https://www.sommeil.org/", "Oui", "Oui (plan du site : 08/04/2026)", "Non annoncée", "https://www.sommeil.org/contact/", "Formulaire https://www.sommeil.org/contact/", 27, 10, 8, "Contact à rechercher", "Site d'information grand public sans éditeur clairement identifié sur l'accueil (à vérifier dans les mentions légales avant tout contact). Sujet très proche.", None),
 6: ("Sommeil-MG (médecine générale)", "https://www.sommeil-mg.net/", "https://sommeil-mg.net/", "Protégé (code 429, contrôle anti-robot)", "Non vérifiable automatiquement", "Non vérifiée", "", "", 22, 14, 2, "Contact à rechercher", "Page bloquée par un contrôle anti-robot : à ouvrir à la main. Public de médecins généralistes : faible chance pour un site non professionnel.", None),
 7: ("France Insomnie", "https://www.franceinsomnie.fr/", "https://www.franceinsomnie.fr/", "Oui", "Oui (plan du site : 22/09/2026)", "Non annoncée (association de patients, page témoignages)", "https://franceinsomnie.fr/contacts/", "contact@franceinsomnie.fr", 30, 17, 8, "Actif mais opportunité non confirmée", "Association nationale de patients (conseil scientifique SFRMS). Contactée le 12/10, relancée le 22/10, sans réponse. Nouvelle approche possible dans 2 mois : la fiche et les audios pour leurs adhérents.", None),
 8: ("IDEAS (sommeil de l'enfant et de l'adolescent)", "https://ideas-asso.org/", "https://ideas-asso.org/", "Oui", "À confirmer (pas de plan du site lu)", "Non annoncée", "https://ideas-asso.org/contact/", "Formulaire https://ideas-asso.org/contact/", 18, 15, 4, "Actif mais opportunité non confirmée", "Sommeil de l'enfant : public différent du nôtre (adultes).", None),
 9: ("Hypersomnie.fr", "https://www.hypersomnie.fr/", "", "Non (délai dépassé sur toutes les variantes)", "Inaccessible", "", "", "", 15, 0, 0, "Inactif ou inaccessible", "Aucune réponse du serveur le 01/11 (https et http).", None),
 10: ("ANC Narcolepsie-Cataplexie", "https://www.anc-narcolepsie.com/", "https://www.anc-narcolepsie.com/", "Oui", "Oui (plan du site : 26/10/2026)", "Non", "https://www.anc-narcolepsie.com/formulaire-general-sans-region", "Formulaire", 10, 15, 2, "Hors sujet", "Maladie rare du sommeil : sans rapport avec nos sujets (stress, ruminations).", None),
 11: ("Université Lyon 1, sommeil", "https://sommeil.univ-lyon1.fr/", "https://www.univ-lyon1.fr", "Oui, mais le sous-domaine redirige vers l'accueil de l'université : l'ancien site sommeil n'existe plus", "Université active", "Non", "", "", 8, 18, 1, "Inactif ou inaccessible", "Le site sommeil a disparu (redirection vers la page d'accueil de l'université).", "univ-lyon1.fr"),
 12: ("Centre Sommeil (centre-sommeil.fr)", "https://www.centre-sommeil.fr/", "https://www.centre-sommeil.fr/", "Oui", "À confirmer", "Non annoncée", "https://www.centre-sommeil.fr/", "Aucun contact trouvé sur l'accueil", 20, 5, 3, "À exclure", "Blog qui met en avant des compléments alimentaires sommeil, sans éditeur identifié : risque de site commercial ou d'affiliation, à éviter pour un site santé.", None),
 13: ("Actis Sommeil Santé", "https://actis-sommeil-sante.fr/", "", "Non (erreur de certificat sur toutes les variantes)", "Inaccessible", "", "", "", 20, 0, 0, "Inactif ou inaccessible", "Erreur TLS le 01/11.", None),
 14: ("CMVS, Centre Médical Veille Sommeil (Paris)", "https://www.cmvs.fr/", "https://cmvs.fr/", "Oui", "Oui (plan du site : 26/02/2026)", "Non (centre médical)", "https://cmvs.fr/contact/", "secretariat@cmvs.fr", 18, 14, 2, "Hors sujet", "Cabinet médical (rendez-vous, examens) : pas de publication externe.", None),
 15: ("Somnology (centre du sommeil, Paris 15)", "https://www.somnology.fr/", "https://somnology.fr/", "Oui", "Oui (plan du site : 29/10/2026)", "Non (centre médical)", "https://somnology.fr/adulte/contact/", "accueil@somnology.fr", 18, 14, 2, "Hors sujet", "Centre médical, pas de média.", None),
 16: ("Somnum (réseau de centres du sommeil)", "https://www.somnum.fr/", "https://somnum.fr/", "Oui", "Oui (plan du site : 31/03/2026)", "Non (centres médicaux)", "https://somnum.fr/", "contact@somnum.fr", 18, 14, 2, "Hors sujet", "Réseau de centres médicaux.", None),
 17: ("Matelas Experience", "https://www.matelas-experience.com/", "https://www.matelas-experience.com/", "Oui", "Oui (plan du site : 06/10/2026)", "Payant (« Contenu sponsorisé », kit média)", "https://www.matelas-experience.com/kit-media-rp", "Page kit média", 16, 10, 3, "Actif mais opportunité non confirmée", "Média literie commercial : partenariats payants. Piste gratuite incertaine : citation de nos ressources respiration dans un article sommeil, à proposer sans rien acheter.", None),
 18: ("Lonasante.com", "https://www.lonasante.com/", "https://www.lonasante.com/", "Oui", "Oui (plan du site : 01/11/2026)", "Non (réseau de partenaires commerciaux)", "https://www.lonasante.com/partenariat/", "Formulaire partenaire", 6, 10, 1, "Hors sujet", "Formations et outils pour soignants (AFGSU, logiciels) : hors sujet.", None),
 19: ("PROSOM", "https://www.prosom.org/", "https://prosom.org/", "Oui", "À confirmer (aucune date lue)", "Non annoncée", "https://prosom.org/contact", "Formulaire https://prosom.org/contact", 26, 15, 5, "Actif mais opportunité non confirmée", "Association de promotion des connaissances sur le sommeil, outils pédagogiques. Piste : proposer la fiche respiration pour leurs interventions.", None),
 20: ("institut-sommeil-vigilance.com", "https://www.institut-sommeil-vigilance.com/", "https://www.institut-sommeil-vigilance.com/", "Oui, mais contenu étranger sans rapport (domaine repris, page en indonésien)", "Sans objet", "", "", "", 0, 0, 0, "À exclure", "Ancien domaine repris par un site sans rapport : un lien depuis ce domaine nuirait au site.", None),
 21: ("Blooming You", "https://www.bloomingyou.fr/", "https://www.bloomingyou.fr/", "Protégé (code 403, page « Just a moment »)", "Non vérifiable automatiquement", "Non vérifiée", "", "", 20, 10, 3, "Contact à rechercher", "Bloqué par une protection anti-robot : à ouvrir à la main.", None),
 22: ("Psychologies.com", "https://www.psychologies.com/", "https://www.psychologies.com/", "Oui", "Oui (plan du site : 01/11/2026)", "Non (rédaction de journalistes et experts)", "https://www.psychologies.com/auteurs/", "Pas d'adresse rédaction affichée sur l'accueil", 25, 16, 3, "Actif mais opportunité non confirmée", "Grand média psycho. Aucun appel à contributions. Seule piste réaliste : être cité comme ressource dans un dossier sommeil, très incertain.", "psychologies.com"),
 23: ("Cerveau & Psycho", "https://www.cerveauetpsycho.fr/", "https://www.cerveauetpsycho.fr/", "Oui", "Oui (plan du site : 28/10/2026)", "Payant (« Contenus sponsorisés »)", "https://www.cerveauetpsycho.fr/p/contenus-sponsorises/", "", 22, 19, 1, "Actif mais opportunité non confirmée", "Magazine scientifique : articles par des chercheurs ou journalistes ; les partenariats sont payants. Pas de collaboration gratuite réaliste.", "cerveauetpsycho.fr"),
 24: ("Santé Mentale (revue)", "https://www.santementale.fr/", "https://www.santementale.fr/", "Oui", "Oui (plan du site : 30/10/2026)", "Oui, mais réservée aux soignants : « Reçus à la rédaction » publie des articles inédits « qui témoignent d'expériences cliniques de terrain »", "https://www.santementale.fr/recus-a-la-redaction/", "Page contact du site", 24, 18, 3, "Actif mais opportunité non confirmée", "Revue professionnelle, déjà contactée (voir l'historique). La rubrique ouverte vise des cliniciens : ne pas proposer d'article (l'auteur n'est pas professionnel de santé).", "santementale.fr"),
 25: ("Psycom", "https://www.psycom.org/", "https://www.psycom.org/", "Oui", "Oui (plan du site : 29/10/2026)", "Non (partenariats institutionnels, co-construction)", "https://www.psycom.org/nous-connaitre/nos-partenariats/", "Formulaire (envoyé par l'utilisateur le 27/10)", 28, 20, 5, "Actif mais opportunité non confirmée", "Référence publique de l'information en santé mentale. Contact envoyé le 27/10 (voir l'historique), en attente : ne pas relancer avant mi-novembre.", "psycom.org"),
 26: ("Doctissimo", "https://www.doctissimo.fr/", "https://www.doctissimo.fr/", "Oui", "Oui (plan du site : 31/10/2026)", "Payant (« publirédactionnels identifiés »)", "https://www.doctissimo.fr/equipe/charte/charte-editoriale-redaction-doctissimo", "", 22, 14, 1, "Actif mais opportunité non confirmée", "Rédaction interne, contenus partenaires payants. Pas de piste gratuite.", "doctissimo.fr"),
 27: ("PasseportSanté", "https://www.passeportsante.net/", "https://www.passeportsante.net/", "Oui", "Oui (plan du site : 01/11/2026)", "Réservée à des experts (« Tribunes » signées par médecin, réflexologue, nutritionniste…)", "https://www.passeportsante.net/portail/tribune", "", 25, 15, 3, "Actif mais opportunité non confirmée", "Tribunes ouvertes à des praticiens : l'auteur n'en est pas un. Piste faible.", "passeportsante.net"),
 28: ("Santé Psy Jeunes (projet PsyCARE)", "https://www.santepsyjeunes.fr/", "https://www.santepsyjeunes.fr/", "Oui", "Oui (plan du site : 28/10/2026)", "Non", "https://www.santepsyjeunes.fr/", "Adresses de services hospitaliers (pas une rédaction)", 18, 18, 2, "Hors sujet", "Site de repérage des troubles psychiques des jeunes, porté par des hôpitaux : pas de place pour un site comme le nôtre.", None),
 29: ("Santé mentale Info Service (Santé publique France)", "https://www.santementale-info-service.fr/", "https://www.santementale-info-service.fr/", "Oui", "Oui (plan du site : 29/10/2026)", "Non (site public)", "", "", 26, 20, 1, "Actif mais opportunité non confirmée", "Site public : il ne publie pas de contenus externes.", "santementale-info-service.fr"),
 30: ("Anxiete.fr (Santé sur le Net)", "https://www.anxiete.fr/", "https://www.anxiete.fr/", "Oui", "Oui (plan du site : 03/08/2026)", "Non annoncée (rédacteurs salariés : pharmaciens, étudiants en santé)", "https://www.anxiete.fr/redacteurs/", "Formulaire https://www.sante-sur-le-net.com/contact/", 28, 14, 4, "Contact éditorial à tenter", "Site très proche de nos sujets (anxiété). Rédaction interne. Piste : signaler une ressource libre utile à un article précis.", None),
 31: ("FNAPSY (fédération d'associations de psychologie)", "https://www.fnapsy.org/", "https://www.fnapsy.org/", "Oui", "Oui (actualités récentes, dont « Dépression : pourquoi se sent-on mieux le soir ? »)", "À vérifier (formulaire : « informations, adhésion, partenariats, presse »)", "https://www.fnapsy.org/contact/", "contact@fnapsy.org", 24, 13, 7, "Contact éditorial à tenter", "Publie des articles de bien-être psychologique (sommeil, bonheur…). Le formulaire prévoit « Partenariat » : piste à tenter avec une proposition de ressource.", None),
 32: ("Unafam", "https://www.unafam.org/", "https://www.unafam.org/", "Oui", "Oui (plan du site : 31/10/2026)", "Non", "https://www.unafam.org/contact", "Formulaire", 14, 18, 2, "Hors sujet", "Familles de personnes atteintes de troubles psychiques sévères : public trop éloigné.", "unafam.org"),
 33: ("france-depression.org", "https://www.france-depression.org/", "https://www.france-depression.org/", "Oui, mais blog sans rapport (beauté, minceur, « puissance »)", "Sans objet", "", "", "", 0, 0, 0, "À exclure", "Ancien domaine d'association repris par un blog commercial : à exclure absolument.", None),
 34: ("Nightline France", "https://www.nightline.fr/", "https://www.nightline.fr/", "Oui", "Oui", "Non (partenariats = mécénat, dons, pro bono)", "https://www.nightline.fr/partenariats", "Formulaire (au registre : contact par formulaire seulement, aucun envoi tracé)", 22, 18, 3, "Actif mais opportunité non confirmée", "Écoute étudiante. Partenariats = mécénat et dons ; aucune piste éditoriale.", "nightline.fr"),
 35: ("3114 (prévention du suicide)", "https://www.3114.fr/", "https://3114.fr/", "Oui", "Oui (plan du site : 20/10/2026)", "Non", "https://3114.fr/je-suis-professionnel/espace-presse/", "", 12, 20, 0, "Hors sujet", "Ligne nationale d'urgence : on la cite, on ne la sollicite pas.", "3114.fr"),
 36: ("SOS Amitié", "https://www.sos-amitie.com/", "https://www.sosamitie.org/", "Oui (sos-amitie.com en https en échec, redirection depuis http vers sosamitie.org, même association)", "Oui (2026)", "Non", "https://www.sosamitie.org/", "", 12, 18, 0, "Hors sujet", "Ligne d'écoute : pas de contenus externes.", "sos-amitie.com"),
 37: ("Médiagora", "https://www.mediagora.fr/", "https://www.mediagora.fr/", "Oui", "À confirmer", "Non annoncée", "https://www.mediagora.fr/contact", "Formulaire", 24, 12, 4, "Actif mais opportunité non confirmée", "Entraide anxiété et phobies. Écartée auparavant (audience jugée faible). Piste ressource possible.", None),
 38: ("La Maison Perchée", "https://www.lamaisonperchee.org/", "", "Non (nom de domaine introuvable)", "Inaccessible", "", "", "", 10, 0, 0, "Inactif ou inaccessible", "Le nom de domaine ne répond plus (vérifier à la main si l'association a changé d'adresse).", None),
 39: ("Collectif Schizophrénies", "https://www.collectif-schizophrenies.com/", "https://www.collectif-schizophrenies.com/", "Oui", "Oui (plan du site : 23/09/2026)", "Non", "https://www.collectif-schizophrenies.com/", "Formulaire", 5, 16, 1, "Hors sujet", "Hors de nos sujets.", None),
 40: ("Fondation FondaMental", "https://www.fondation-fondamental.org/", "https://www.fondation-fondamental.org/", "Oui", "Oui (plan du site : 29/10/2026)", "Non (recherche, mécénat)", "https://www.fondation-fondamental.org/nous-contacter", "Formulaire", 12, 19, 1, "Hors sujet", "Fondation de recherche en psychiatrie.", "fondation-fondamental.org"),
 41: ("FemininBio", "https://www.femininbio.com/", "https://www.femininbio.com/", "Oui", "Douteux : plan du site daté du 13/02/2023 (à confirmer à la main)", "À tenter (« Vous souhaitez écrire à la rédaction »)", "https://www.femininbio.com/contact", "redaction@femininbio.com", 16, 12, 7, "Contact éditorial à tenter", "Bien-être grand public ; adresse rédaction publique. Vérifier d'abord que le site publie encore.", "femininbio.com"),
 42: ("Happinez", "https://www.happinez.fr/", "https://www.happinez.fr/", "Oui", "Oui (plan du site : 29/10/2026)", "À tenter (formulaire « Contacter la rédaction »)", "https://www.happinez.fr/contact/", "Formulaire, choix « Contacter la rédaction »", 18, 14, 6, "Contact éditorial à tenter", "Magazine « mindstyle » (méditation, bien-être). Contact rédaction possible.", None),
 43: ("Inexploré (INREES)", "https://www.inexplore.com/", "https://www.inexplore.com/", "Oui", "Oui (plan du site : 01/11/2026)", "Non", "https://www.inrees.com/Contact", "contact@inexplore.com", 8, 8, 2, "Hors sujet", "Spiritualité et paranormal : incompatible avec un site sourcé.", None),
 44: ("Alternative Santé", "https://www.alternativesante.fr/", "https://www.alternativesante.fr/", "Oui", "Oui (plan du site : 05/10/2026)", "Non annoncée", "https://www.alternativesante.fr/", "Aucun contact sur l'accueil", 15, 8, 2, "À exclure", "Médecines alternatives, rubrique « Polémiques » : ligne éditoriale peu compatible avec un site sourcé.", "alternativesante.fr"),
 45: ("Rebelle-Santé", "https://www.rebelle-sante.com/", "https://www.rebelle-sante.com/", "Oui", "Oui (plan du site : 01/11/2026)", "À tenter (« joindre le secrétariat de rédaction »)", "https://www.rebelle-sante.com/nous-contacter/", "contact@rebelle-sante.com", 16, 9, 4, "Actif mais opportunité non confirmée", "Santé naturelle, ligne parfois éloignée des données scientifiques. Prudence.", None),
 46: ("Plantes & Santé", "https://www.plantes-et-sante.fr/", "https://www.plantes-et-sante.fr/", "Oui", "Oui (plan du site : 07/10/2026)", "Non annoncée", "https://www.plantes-et-sante.fr/", "Aucun contact sur l'accueil", 8, 10, 2, "Hors sujet", "Phytothérapie : hors de nos sujets.", None),
 47: ("Esprit Yoga", "https://www.esprityoga.fr/", "https://www.esprityoga.fr/", "Oui", "Oui (plan du site : 01/11/2026 ; numéro de sept.-oct. 2026)", "Oui, explicite : « Proposer un article, une idée, un projet, un service » (conditions de publication non précisées : gratuité et lien à confirmer)", "https://www.esprityoga.fr/contact/", "Formulaire, choix « Proposer un article »", 17, 14, 14, "Actif mais opportunité non confirmée", "Procédure publique de proposition d'article, mais gratuité et lien non précisés : à confirmer. Une proposition d'article est explicitement prévue. Angle respiration et sommeil adapté au yoga. Le caractère gratuit et la présence d'un lien restent à confirmer.", None),
 48: ("Mindful.org", "https://www.mindful.org/", "https://www.mindful.org/", "Oui", "Oui (plan du site : 01/11/2026)", "Non (site américain en anglais)", "https://www.mindful.org/contact/", "mindful@mindful.org", 10, 18, 1, "Hors sujet", "Site en anglais, public américain : un lien serait peu utile à un site français.", "mindful.org"),
 49: ("Petit BamBou", "https://www.petitbambou.com/", "https://www.petitbambou.com/fr", "Oui", "Oui (plan du site : 28/10/2026)", "Non (contributeurs = auteurs et voix de l'application)", "https://www.petitbambou.com/fr/contributors", "presse@petitbambou.com", 20, 17, 1, "Actif mais opportunité non confirmée", "Concurrent direct (application de méditation) : pas d'intérêt à nous citer.", "petitbambou.com"),
 50: ("Medoucine", "https://www.medoucine.com/", "https://www.medoucine.com/", "Protégé (code 403, page « Just a moment »)", "Non vérifiable automatiquement", "Non annoncée", "", "Formulaire (au registre : aucun envoi tracé)", 15, 12, 2, "Actif mais opportunité non confirmée", "Annuaire de praticiens : contact par formulaire seulement. Pas de piste gratuite connue.", "medoucine.com"),
 51: ("Therapeutes.com", "https://www.therapeutes.com/", "https://therapeutes.com/", "Oui", "À confirmer", "Non (annuaire payant pour praticiens)", "https://therapeutes.com/contrat-de-partenariat", "Formulaire", 10, 8, 1, "Hors sujet", "Annuaire commercial de praticiens.", "therapeutes.com"),
 52: ("Resalib", "https://www.resalib.fr/", "https://www.resalib.fr/", "Oui", "Oui (plan du site : 01/11/2026)", "Non (plateforme de réservation)", "https://www.resalib.fr/presse", "contact@resalib.com", 10, 10, 1, "Hors sujet", "Plateforme de rendez-vous.", "resalib.fr"),
 53: ("Psychologue.net", "https://www.psychologue.net/", "https://www.psychologue.net/", "Oui", "À confirmer", "Non (annuaire de psychologues)", "https://www.psychologue.net/politique-publicitaire", "", 12, 10, 1, "Hors sujet", "Annuaire : réservé aux psychologues.", "psychologue.net"),
 54: ("Voie du Bien-Être", "https://www.voiedubienetre.fr/", "https://www.voiedubienetre.fr/", "Oui", "Oui (plan du site : 28/10/2026)", "Oui pour proposer un sujet ou un partenariat éditorial ; non pour tout contenu payant (« On ne fait pas d'article sponsorisé […] liens payants ou échange d'articles : c'est non »)", "https://www.voiedubienetre.fr/contact/", "Formulaire de la page contact (« Proposer un sujet », « Presse et partenariats éditoriaux »)", 28, 15, 13, "Opportunité gratuite explicitement confirmée", "Magazine bien-être avec rubriques Sommeil, Mental et Souffle, ligne exigeante (sources, correction des erreurs). La page invite à proposer des sujets et parle volontiers « de méthodologie, de données » : proposer la méthode sourcée et les ressources libres, jamais un échange de liens.", None),
 55: ("My Little Nature", "https://www.mylittlenature.fr/", "", "Non (nom de domaine introuvable)", "Inaccessible", "", "", "", 10, 0, 0, "Inactif ou inaccessible", "Domaine qui ne répond plus.", None),
 56: ("Goalmap", "https://www.goalmap.com/", "https://goalmap.com/", "Oui (page « Redirection… » sans contenu)", "Aucun contenu lisible", "", "", "", 3, 2, 0, "Hors sujet", "Aucun contenu éditorial visible.", None),
 57: ("Yoga Magazine", "https://www.yoga-magazine.fr/", "https://www.yoga-magazine.fr/", "Oui", "Oui (plan du site : 21/10/2026)", "À tenter (formulaire « Contacter la rédaction »)", "https://www.yoga-magazine.fr/contact/", "Formulaire, choix « Contacter la rédaction »", 16, 13, 6, "Contact éditorial à tenter", "Rubriques « Comment faire », « Le yoga & moi » : une respiration du soir peut y trouver place.", None),
 58: ("ELLE", "https://www.elle.fr/", "https://www.elle.fr/", "Protégé (code 405, vérification humaine)", "Actif (média national)", "Non (rédaction de journalistes)", "", "", 10, 15, 1, "Actif mais opportunité non confirmée", "Grand média féminin : aucune contribution externe ; piste unique = être cité par une journaliste, très improbable.", "elle.fr"),
 59: ("Marie Claire", "https://www.marieclaire.fr/", "https://www.marieclaire.fr/", "Oui", "Oui (plan du site : 01/11/2026)", "Non", "", "", 10, 15, 1, "Actif mais opportunité non confirmée", "Même constat qu'ELLE.", "marieclaire.fr"),
 60: ("Femme Actuelle", "https://www.femmeactuelle.fr/", "https://www.femmeactuelle.fr/", "Oui", "Oui (articles récents en psycho)", "Non", "https://www.femmeactuelle.fr/pages/contact", "Formulaire « Aide et Contact »", 12, 14, 1, "Actif mais opportunité non confirmée", "Rubrique psycho active, mais rédaction de journalistes.", "femmeactuelle.fr"),
 61: ("Anact", "https://www.anact.fr/", "https://www.anact.fr/", "Oui (contrôle anti-robot à l'ouverture)", "Oui (plan du site : 30/10/2026)", "Non (agence publique)", "", "", 16, 19, 1, "Actif mais opportunité non confirmée", "Agence publique des conditions de travail : pas de contenus externes.", "anact.fr"),
 62: ("INRS", "https://www.inrs.fr/", "https://www.inrs.fr/", "Oui", "Oui (plan du site : 12/10/2026)", "Non (institut public)", "https://www.inrs.fr/", "", 14, 20, 1, "Actif mais opportunité non confirmée", "Référence santé au travail : source à citer chez nous, pas une cible de lien.", "inrs.fr"),
 63: ("My Happy Job", "https://www.myhappyjob.fr/", "https://www.myhappyjob.fr/", "Oui", "Oui (chroniques récentes : heure d'hiver, surcharge mentale)", "Oui, rubrique « Tribunes » : « Des acteurs engagés dans la qualité de vie au travail partagent un point de vue » (conditions non publiées)", "https://www.myhappyjob.fr/category/quoi-de-neuf/tribunes/", "À rechercher (pas d'adresse sur la page lue)", 20, 13, 12, "Contact éditorial à tenter", "Média QVT qui publie des tribunes extérieures et traite fatigue et surcharge mentale : bon angle « charge mentale et sommeil des salariés ». Gratuité à confirmer.", None),
 64: ("Parlons RH", "https://www.parlonsrh.com/", "https://www.parlonsrh.com/", "Oui", "Oui (plan du site : 30/10/2026)", "Tribunes publiées (thème « QVCT et santé au travail »), mais l'agence propose aussi « Devenir partenaire » : gratuité incertaine", "https://www.parlonsrh.com/format/tribunes/", "Formulaire (au registre : aucun envoi tracé)", 15, 12, 6, "Actif mais opportunité non confirmée", "Public RH ; tribunes thème QVCT.", "parlonsrh.com"),
 65: ("Culture RH", "https://www.culture-rh.com/", "https://culture-rh.com/", "Oui", "Oui (plan du site : 30/10/2026)", "Oui, explicite : page « Devenir auteur » pour les experts RH, freelances et cabinets (gratuité et liens non précisés sur la page)", "https://culture-rh.com/devenir-auteur/", "Formulaire de la page « Devenir auteur »", 14, 12, 14, "Actif mais opportunité non confirmée", "Procédure publique « Devenir auteur », gratuité et liens non précisés. Ouverture explicite aux auteurs, rubrique « Risques psychosociaux ». Public RH : angle « sommeil et risques psychosociaux ». Ligne éloignée de notre cœur (sommeil) ; gratuité à confirmer.", "culture-rh.com"),
 66: ("Focus RH", "https://www.focusrh.com/", "https://www.focusrh.com/", "Oui", "Oui (plan du site : 31/10/2026)", "Tribunes publiées (conditions non publiées)", "https://www.focusrh.com/tribunes/tribunes-20697.html", "Contacts du groupe Studyrama", 13, 12, 6, "Contact éditorial à tenter", "Tribunes d'experts RH ; notre profil y est peu attendu.", "focusrh.com"),
 67: ("Manager GO!", "https://www.manager-go.com/", "https://www.manager-go.com/", "Oui", "Oui (plan du site : 29/10/2026)", "Non annoncée", "https://www.manager-go.com/contactez-nous", "Formulaire", 10, 12, 3, "Actif mais opportunité non confirmée", "Management : lien faible avec nos sujets.", "manager-go.com"),
 68: ("Welcome to the Jungle", "https://www.welcometothejungle.com/fr", "https://www.welcometothejungle.com/fr", "Oui", "Oui (média emploi actif)", "Non", "https://press.welcometothejungle.com/", "", 10, 15, 1, "Actif mais opportunité non confirmée", "Rédaction interne, pas de contributions externes.", "welcometothejungle.com"),
 69: ("QVT.fr", "https://www.qvt.fr/", "", "Non (certificat invalide, puis échec de connexion)", "Inaccessible", "", "", "", 15, 0, 0, "Inactif ou inaccessible", "", None),
 70: ("Les Ateliers Durables", "https://www.lesateliersdurables.com/", "", "Non (nom de domaine introuvable)", "Inaccessible", "", "", "", 10, 0, 0, "Inactif ou inaccessible", "", None),
 71: ("Moka.Care", "https://www.moka.care/", "https://www.moka.care/", "Oui", "Oui (plan du site : 29/10/2026)", "Non (entreprise de santé mentale au travail)", "https://www.moka.care/contact", "Formulaire commercial", 15, 14, 2, "Actif mais opportunité non confirmée", "Concurrent commercial, ressources maison.", None),
 72: ("teale", "https://www.teale.io/", "https://www.teale.io/", "Oui", "Oui (plan du site : 28/10/2026)", "Non", "https://www.teale.io/presse", "Formulaire", 15, 14, 2, "Actif mais opportunité non confirmée", "Entreprise de santé mentale au travail.", None),
 73: ("Alan", "https://www.alan.com/fr", "https://alan.com/fr", "Oui", "Oui", "Non", "", "", 10, 15, 1, "Actif mais opportunité non confirmée", "Assureur santé : rédaction interne.", "alan.com"),
 74: ("Malakoff Humanis", "https://www.malakoffhumanis.com/", "https://www.malakoffhumanis.com/", "Oui", "Oui (plan du site : 29/06/2026)", "Non", "https://newsroom.malakoffhumanis.com/", "", 8, 15, 1, "Actif mais opportunité non confirmée", "Groupe de protection sociale : plus de demandes aux grandes institutions (règle du 29/10).", "malakoffhumanis.com"),
 75: ("Harmonie Mutuelle", "https://www.harmonie-mutuelle.fr/", "https://www.harmonie-mutuelle.fr/", "Oui", "Oui (plan du site : 30/10/2026)", "Non", "https://www.harmonie-mutuelle.fr/marque/a-propos/espace-presse", "", 10, 15, 1, "Actif mais opportunité non confirmée", "Grande mutuelle (média Harmonie Santé avec l'Inserm) : pas de contributions externes.", "harmonie-mutuelle.fr"),
 76: ("Apec", "https://www.apec.fr/", "https://www.apec.fr/", "Protégé (code 403)", "Actif", "Non", "", "", 5, 14, 0, "Hors sujet", "Emploi des cadres.", "apec.fr"),
 77: ("Hellowork", "https://www.hellowork.com/", "https://www.hellowork.com/fr-fr/", "Oui", "Oui", "Non", "", "", 4, 12, 0, "Hors sujet", "Site d'offres d'emploi.", "hellowork.com"),
 78: ("Preventica", "https://www.preventica.com/", "https://www.preventica.com/", "Oui", "Oui (plan du site : 01/11/2026)", "« Contribuer » renvoie à une demande de participation aux salons (exposants, en principe payant) ; interviews d'auteurs dans le magazine", "https://www.preventica.com/", "preventica@preventica.com", 14, 13, 4, "Actif mais opportunité non confirmée", "Salons et magazine santé-sécurité au travail. Pas de piste gratuite claire.", "preventica.com"),
 79: ("sante-travail.fr", "https://www.sante-travail.fr/", "http://www.sante-travail.fr/", "Répond en http seulement, page vide", "Aucun contenu lisible", "", "", "", 10, 0, 0, "Inactif ou inaccessible", "Page vide le 01/11.", None),
 80: ("Santé publique France", "https://www.santepubliquefrance.fr/", "https://www.santepubliquefrance.fr/", "Oui", "Oui (plan du site : 29/10/2026)", "Non (agence publique)", "https://www.santepubliquefrance.fr/presse", "presse@santepubliquefrance.fr (réservé aux journalistes)", 18, 20, 0, "Actif mais opportunité non confirmée", "Source à citer, pas une cible.", "santepubliquefrance.fr"),
 81: ("Top Santé", "https://www.topsante.com/", "https://www.topsante.com/", "Oui", "Oui (plan du site : 01/11/2026)", "Non (rédaction interne)", "https://www.topsante.com/", "", 18, 13, 1, "Actif mais opportunité non confirmée", "Rédaction de journalistes.", "topsante.com"),
 82: ("Medisite", "https://www.medisite.fr/", "https://www.medisite.fr/", "Oui", "Oui (plan du site : 01/11/2026)", "Non", "", "", 18, 13, 2, "Actif mais opportunité non confirmée", "Les journalistes interrogent des médecins : nous ne sommes pas une source qu'ils citeraient.", "medisite.fr"),
 83: ("Santé Magazine", "https://www.santemagazine.fr/", "https://www.santemagazine.fr/", "Oui", "Oui (plan du site : 01/11/2026)", "Non", "https://www.santemagazine.fr/contactez-nous-1109170", "Formulaire", 18, 13, 1, "Actif mais opportunité non confirmée", "Rédaction interne.", "santemagazine.fr"),
 84: ("Journal des Femmes", "https://www.journaldesfemmes.fr/", "https://www.journaldesfemmes.fr/", "Oui", "Oui (plan du site : 01/11/2026)", "Non", "", "", 12, 13, 1, "Actif mais opportunité non confirmée", "Rédaction interne.", "journaldesfemmes.fr"),
 85: ("aufeminin", "https://www.aufeminin.com/", "https://www.aufeminin.com/", "Oui", "Oui", "Non", "", "", 8, 10, 1, "Actif mais opportunité non confirmée", "Rédaction interne.", "aufeminin.com"),
 86: ("Madame Figaro", "https://madame.lefigaro.fr/", "https://madame.lefigaro.fr/", "Oui", "Oui (plan du site : 01/11/2026)", "Non", "", "", 8, 14, 1, "Actif mais opportunité non confirmée", "Rédaction interne.", None),
 87: ("Futura", "https://www.futura-sciences.com/", "https://www.futura-sciences.com/", "Oui", "Oui", "Non (rédaction scientifique)", "", "", 12, 15, 1, "Actif mais opportunité non confirmée", "Rédaction interne.", "futura-sciences.com"),
 88: ("The Conversation France", "https://www.theconversation.com/fr", "https://theconversation.com/fr", "Oui", "Oui (plan du site : 01/11/2026)", "Réservé aux chercheurs et universitaires (auteurs académiques uniquement)", "https://theconversation.com/fr", "", 14, 20, 0, "Hors sujet", "Le site ne publie que des universitaires : l'auteur n'est pas éligible.", "theconversation.com"),
 89: ("Sciences Humaines", "https://www.scienceshumaines.com/", "https://www.scienceshumaines.com/", "Oui", "Oui (plan du site : 01/11/2026)", "Non", "https://www.scienceshumaines.com/contacts", "Page contacts", 10, 17, 1, "Actif mais opportunité non confirmée", "Magazine de sciences humaines : rédaction et chercheurs.", "scienceshumaines.com"),
 90: ("Ça m'intéresse", "https://www.caminteresse.fr/", "https://www.caminteresse.fr/", "Oui", "Oui (plan du site : 12/06/2026)", "Non", "", "", 8, 13, 1, "Actif mais opportunité non confirmée", "Rédaction interne.", "caminteresse.fr"),
 91: ("La Dépêche", "https://www.ladepeche.fr/", "https://www.ladepeche.fr/", "Oui", "Oui", "Non", "", "", 5, 14, 1, "Actif mais opportunité non confirmée", "Quotidien régional : seulement si une actualité locale existe.", "ladepeche.fr"),
 92: ("Ouest-France", "https://www.ouest-france.fr/", "https://www.ouest-france.fr/", "Protégé (code 403)", "Actif", "Non", "", "", 5, 15, 1, "Actif mais opportunité non confirmée", "Quotidien : sans actualité locale, aucune piste.", "ouest-france.fr"),
 93: ("franceinfo", "https://www.francetvinfo.fr/", "https://www.franceinfo.fr/ (redirection)", "Délai dépassé le 01/11 (site national, sans doute un blocage des robots)", "Actif (média national)", "Non", "", "", 5, 17, 0, "Actif mais opportunité non confirmée", "Média d'information : aucune contribution externe.", "francetvinfo.fr"),
 94: ("RTL", "https://www.rtl.fr/", "https://www.rtl.fr/", "Oui", "Oui", "Non", "", "", 5, 14, 0, "Actif mais opportunité non confirmée", "Radio nationale.", "rtl.fr"),
 95: ("France Bleu (devenu ICI)", "https://www.francebleu.fr/", "https://www.ici.fr/", "Oui (redirection vers ici.fr, même réseau de Radio France)", "Oui", "Non", "", "", 5, 15, 1, "Actif mais opportunité non confirmée", "Radio locale : piste seulement avec une actualité locale.", "ici.fr"),
 96: ("Radio France", "https://www.radiofrance.fr/", "https://www.radiofrance.fr/", "Oui", "Oui", "Non", "", "", 6, 17, 0, "Actif mais opportunité non confirmée", "Groupe de radios.", "radiofrance.fr"),
 97: ("Slate.fr", "https://www.slate.fr/", "https://www.slate.fr/", "Oui", "Oui (plan du site : 01/11/2026)", "Non annoncée", "", "", 8, 14, 1, "Actif mais opportunité non confirmée", "Rédaction interne.", "slate.fr"),
 98: ("L'Obs", "https://www.nouvelobs.com/", "https://www.nouvelobs.com/", "Oui", "Oui", "Non", "", "", 5, 15, 0, "Actif mais opportunité non confirmée", "Rédaction interne.", "nouvelobs.com"),
 99: ("Le Monde", "https://www.lemonde.fr/", "https://www.lemonde.fr/", "Oui", "Oui (plan du site : 01/11/2026)", "Tribunes publiées (« Idées et tribunes »), très sélectives, procédure non publiée sur la page lue", "https://www.lemonde.fr/tribunes/", "", 5, 19, 1, "Actif mais opportunité non confirmée", "Une tribune d'un auteur sans titre ni étude originale n'a quasiment aucune chance.", "lemonde.fr"),
 100: ("L'Express", "https://www.lexpress.fr/", "https://www.lexpress.fr/", "Oui", "Oui", "Non", "", "", 5, 15, 0, "Actif mais opportunité non confirmée", "Rédaction interne.", "lexpress.fr"),
}

CAT = {}
for n in range(1, 101):
    CAT[n] = ("Sommeil et insomnie" if n <= 20 else "Stress, psychologie et santé mentale" if n <= 40 else
              "Bien-être et santé naturelle" if n <= 60 else "Bien-être au travail et prévention du stress" if n <= 80 else
              "Médias et magazines généralistes")


def rang(dom):
    return TRANCO.get(dom) if dom else None


def points_rang(r):
    """Audience /15 et potentiel SEO /15 déduits du rang Tranco (mondial) : approximation, pas une mesure."""
    if r is None:
        return 3
    return 15 if r <= 20000 else 12 if r <= 100000 else 9 if r <= 400000 else 6


def classe(note, statut, collab):
    """A : site pertinent ET collaboration gratuite réaliste (≥ 10/20) ; B : intéressant mais collaboration incertaine
    (≥ 5/20) ou site de forte valeur sans porte d'entrée connue ; C : le reste. Un grand média n'est pas A pour autant."""
    if statut in ("À exclure", "Inactif ou inaccessible"):
        return "Exclu"
    if statut == "Hors sujet":
        return "C"
    if collab >= 10 and note >= 55:
        return "A"
    if collab >= 5 or note >= 55:
        return "B"
    return "C"


def lignes():
    hist = json.load(open(os.path.join(DOSSIER, "historique-prospection.json")))
    out = []
    for n, s in S.items():
        nom, u0, uf, ok, act, contrib, preuve, contact, pert, qual, collab, statut, com, dom = s
        r = rang(dom)
        aud = seo = points_rang(r)
        if statut in ("Inactif ou inaccessible", "À exclure"):
            aud = seo = 0
        note = pert + qual + aud + seo + collab
        h = hist.get(str(n))
        if h:
            com += " Historique : " + " ; ".join(f"{x['statut']} le {x.get('date_envoi') or '?'}" for x in h) + "."
        out.append([n, nom, u0, uf, CAT[n], ok, act, ND, ND, ND, ND, ND, ND,
                    (f"Rang Tranco {r} (liste 7462X du 31/10/2026, popularité mondiale, pas un trafic)" if r else
                     "Absent du top 1 million Tranco (liste 7462X du 31/10/2026) ; requêtes HTTP directes"),
                    DATE, contrib, preuve, contact, f"{pert}/30", note, classe(note, statut, collab), statut + ". " + com])
    return out


ENTETES = ["N°", "Nom du site", "URL initiale", "URL finale après redirection", "Catégorie", "Site fonctionnel",
           "Activité récente", "Trafic mensuel estimé", "Trafic organique estimé", "Part du trafic français",
           "Domain Rating (Ahrefs)", "Authority Score (Semrush)", "Domaines référents", "Source des données",
           "Date de vérification", "Articles invités gratuits", "Preuve de possibilité de contribution", "Contact",
           "Pertinence SEO (thématique /30)", "Note sur 100", "Classement A/B/C", "Statut et commentaires"]


def ecrire(chemin, rows, titre):
    wb = Workbook()
    ws = wb.active
    ws.title = titre
    ws.append(ENTETES)
    for r in rows:
        ws.append(r)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="3B4A6B")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    larg = [5, 26, 30, 30, 22, 22, 26, 14, 14, 14, 14, 14, 14, 34, 12, 40, 40, 30, 12, 9, 9, 70]
    for i, w in enumerate(larg, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = ws.dimensions
    m = wb.create_sheet("Méthode")
    for ligne in __doc__.strip().splitlines() + ["", "Barème : pertinence thématique /30, qualité éditoriale /20, audience "
                                                  "française /15, potentiel SEO /15, collaboration gratuite /20.",
                                                  "Audience et potentiel SEO (approximation par le rang Tranco) : top 20 000 = 15 ; "
                                                  "top 100 000 = 12 ; top 400 000 = 9 ; top 1 million = 6 ; absent = 3 ; "
                                                  "site inactif ou à exclure = 0.",
                                                  "Classement : A = collaboration gratuite réaliste (≥ 10/20) et note ≥ 55 ; B = collaboration possible (≥ 5/20) "
                                                  "ou note ≥ 55 sans porte d'entrée connue ; C = le reste ; « Hors sujet » = C ; « Inactif » et « À exclure » = Exclu.",
                                                  "Ahrefs et Semrush n'ont pas été utilisés : outils payants (consigne : ne rien payer)."]:
        m.append([ligne])
    m.column_dimensions["A"].width = 140
    wb.save(chemin)


if __name__ == "__main__":
    rows = lignes()
    ecrire(os.path.join(DOSSIER, "1-audit-100-sites.xlsx"), rows, "Audit 100 sites")
    json.dump(rows, open(os.path.join(DOSSIER, "1-audit-100-sites.json"), "w"), ensure_ascii=False, indent=1)
    from collections import Counter
    print(Counter(r[20] for r in rows), Counter(r[21].split(". ")[0] for r in rows))
    for r in sorted(rows, key=lambda r: -r[19])[:20]:
        print(r[19], r[20], r[1], "|", r[21][:70])
