# Campagne de liens gratuits (novembre 2026 à janvier 2027)

Mission de l'utilisateur du 01/11/2026 : obtenir 5 à 10 liens éditoriaux gratuits en 90 jours, budget 0 €, sans
aucun envoi sans son accord. Objectif de travail, pas une garantie.

## Fichiers

| N° | Fichier | État |
|---|---|---|
| 1 | `1-audit-100-sites.xlsx` (+ `.json`), produit par `outils/campagne_backlinks_audit.py` | fait le 01/11 |
| 2 | Nouveaux prospects | à faire |
| 3 | Top 30 | à faire |
| 4 | Messages et relances (aucun envoi sans validation) | à faire |
| 5 | Plan d'action sur 90 jours | à faire |
| 6 | Suivi des liens obtenus | à faire |

Données sources : `historique-prospection.json` (contacts déjà faits sur ces domaines, tirés de
`../prospection-liens.json`) et `tranco-2026-10-31.json` (rangs Tranco).

## Étape 1 : audit des 100 sites (01/11/2026)

**Méthode.** Chaque domaine a été ouvert par une requête HTTP directe. Pour chacun, on a relevé :
- le code de réponse et l'adresse finale ;
- le titre et la date la plus récente du plan du site ;
- les liens « contact », « contribution » et « partenariat » de l'accueil.

Ensuite, environ 70 pages de contact ou de contribution ont été lues pour y chercher des preuves (citations dans la
colonne « Preuve »). Les sites protégés par un contrôle anti-robot sont marqués comme tels, sans conclusion
inventée.

**Indicateurs de trafic et d'autorité.** Ahrefs et Semrush sont payants. Le trafic, le Domain Rating, l'Authority
Score et les domaines référents sont donc indiqués « Non disponible ».

Seule mesure gratuite et datée : le rang Tranco (liste 7462X du 31/10/2026). C'est une popularité mondiale, pas un
trafic. Elle sert seulement à approcher les notes « audience » et « potentiel SEO ».

**Résultats.**

| Indicateur | Nombre |
|---|---|
| Domaines vérifiés | 100 |
| Actifs et lisibles | 82 |
| Actifs mais protégés par un contrôle anti-robot ou trop lents (à ouvrir à la main) | 8 |
| Inaccessibles (nom de domaine introuvable, délai dépassé, certificat, page vide) | 7 |
| Domaines repris par un site sans rapport (à exclure) | 2 : `institut-sommeil-vigilance.com`, `france-depression.org` |
| Ancien site disparu | 1 : `sommeil.univ-lyon1.fr`, qui redirige vers l'accueil de l'université |
| Hors sujet | 22 : centres médicaux, annuaires, maladies rares, emploi, lignes d'urgence, site en anglais |
| Procédure publique de contribution ou de proposition repérée | 3 : Voie du Bien-Être, Esprit Yoga, Culture RH |
| Rubriques « tribunes » ouvertes à l'extérieur, conditions non publiées | 4 : My Happy Job, Parlons RH, Focus RH, Le Monde |
| Rubriques réservées à des profils que l'auteur n'a pas | 3 : PasseportSanté (praticiens), revue Santé Mentale (cliniciens), The Conversation (universitaires) |
| Opportunité gratuite explicitement confirmée | 1 : Voie du Bien-Être, qui invite à proposer des sujets et refuse tout contenu payant |
| À exclure | 4 : les 2 domaines repris, un blog de compléments alimentaires et un site de médecines alternatives |
| Classement | A : 2 ; B : 33 ; C : 53 ; exclus : 12 |
| Déjà contactés avant cette campagne | 8, à ne pas relancer trop tôt (colonne « Commentaires ») |

**Ce qu'on en retient.** La liste de départ contient surtout :
- de grands médias, qui ont une rédaction interne et vendent leurs contenus partenaires ;
- des institutions, qui ne publient rien venant de l'extérieur ;
- des centres médicaux.

Un média très connu n'est donc pas un bon prospect. Les vraies portes d'entrée sont rares : Voie du Bien-Être, Esprit
Yoga, Culture RH et My Happy Job. On peut y ajouter, plus incertains, la FNAPSY, Happinez, Yoga Magazine et
FemininBio. L'étape 5 (nouveaux prospects) doit viser des médias et associations de taille moyenne qui publient des
contributions extérieures.

## Ce qu'on apporte aux prospects (pas seulement une demande de lien)

Consigne : « propose une valeur ajoutée aux prospects ». Ce qu'on peut offrir, seulement si c'est vrai et gratuit :
1. **Ressources libres de droits, prêtes à l'emploi.** Trois audios de respiration 4-6 (3, 5 et 10 min) et une fiche
   de 5 exercices, sous licence CC BY 4.0 ou CC BY-ND 4.0. Page : `/ressources-libres/`. Un média ou une association
   peut les intégrer tels quels à un article ou à un atelier.
2. **Une ressource adaptée à leur public.** Par exemple une version « avant un examen » pour un service étudiant, ou
   « avant de dormir après une journée de travail » pour un média QVT. On ne promet rien sans l'avoir fabriquée.
3. **Un article inédit et sourcé**, écrit pour leur ligne éditoriale (jamais le même texte deux fois). Chaque étude y
   est nommée et vérifiée, avec une section « Quand consulter » et aucune promesse de soin.
4. **Un service rendu.** Signaler un lien mort ou une source périmée trouvés sur leur page, avant toute proposition.
5. **Un témoignage limité au vécu réel**, celui de `../vecu-auteur.md` : deux ans de nuits difficiles, et la cohérence
   cardiaque qui a aidé. Jamais rien de plus, jamais de titre ni de métier.
6. **Des données propres au site**, plus tard, quand il y aura assez de visites. Exemple : les recherches qui amènent
   des lecteurs sur « ruminations le soir ». Ce sont des chiffres anonymes et agrégés, à citer seulement s'ils sont
   solides.

Règles : aucun achat, aucun échange de liens, aucune ancre répétée, aucun contenu dupliqué. Un lien « nofollow » ou
« sponsored » reste possible, mais il est noté comme tel dans le suivi. Aucun envoi sans validation de l'utilisateur.
