# Cibles « top 20 Google » : une recherche précise par article (depuis le 25/10/2026)

Demande de l'utilisateur (22/10/2026) : « viser au moins les 10 ou 20 premières places Google », puis « Analyse les
mots-clés longue traîne etc. où il y a du volume de recherche ». Plan validé (« Oui ») : 15 recherches précises, une
par article, choisies là où il y a du volume ET une vraie chance d'entrer dans le top 20.

Complète `mots-cles.md` (mot-clé principal de chaque page, relevé du vendredi) et `optimisation-mensuelle.md` (passe
mensuelle sur les requêtes déjà proches de la 1re page). Une seule page par recherche, slug jamais changé.

## Honnêteté sur les chiffres

**Aucun volume exact n'est disponible.** Sans outil payant ni Google Keyword Planner (qui exige un compte publicitaire),
personne ne peut donner le nombre de recherches mensuelles d'une expression. Ce document classe donc les recherches en
volume **probable** fort, moyen ou faible, à partir de quatre signaux gratuits, et il le dit à chaque fois.

| Signal (gratuit) | Ce qu'il dit | Limite |
|---|---|---|
| Suggestions Google (`suggestqueries.google.com`, `hl=fr`, `gl=fr`, 22/10 et 25/10/2026 ; terme seul, « pourquoi », « comment », « que faire », « quel », et terme + une lettre) | Une suggestion = une recherche réelle et régulière. Google classe les suggestions à peu près par popularité. | Ne donne aucun chiffre. |
| Google Trends (API gratuite d'exploration, France, 12 derniers mois, lue le 22/10 et le 25/10/2026) | Intérêt relatif entre expressions, toujours comparé à une expression de référence : « angoisse le soir » = 1. | Les expressions trop rares tombent à 0. Quand la référence est très petite dans un groupe, le rapport n'est qu'un ordre de grandeur. |
| Search Console (Composio, du 09/10 au 24/10/2026, 97 couples requête/page) | Impressions et position réelles du site. | Site neuf : 1 à 6 impressions par requête, positions instables. |
| Pages de résultats gratuites | Qui occupe le top 10. | Approximation : voir ci-dessous. |

**Pages de résultats.** DuckDuckGo (version HTML) n'a répondu qu'à 2 requêtes puis a bloqué l'atelier Composio
(« anomalie » détectée) ; Bing renvoie aux scripts des résultats sans rapport avec la requête. Le top 10 a donc été lu
sur **Brave Search** (pages gratuites, sans compte, lues le 22/10 et le 25/10/2026 avec curl depuis l'atelier Composio),
complété par DuckDuckGo pour « angoisse le soir sans raison » et « angoisse la nuit que faire ». **Ce n'est pas le
classement Google**, seulement une approximation de la concurrence : Google donne en général plus de place aux grands
sites santé (Ameli, Doctissimo, Passeport Santé, Vidal, Inserm). La Search Console reste la seule mesure qui compte.

### Méthode de classement du volume probable

- **Fort** : Trends au moins 5 fois « angoisse le soir », ou expression courte dont toutes les suggestions restent dans
  le sujet.
- **Moyen** : Trends entre 0,5 et 5 fois la référence, ou expression proposée dans les 3 premières suggestions du
  terme seul, ou au moins 3 impressions Search Console en 16 jours pour un site de 2 semaines.
- **Faible** : sous le seuil de Trends (0), mais présente dans les suggestions Google (souvent après un préfixe ou une
  lettre).

### Méthode de classement de la difficulté

- **Faible** : top 10 tenu par des blogs, des marques de compléments ou de literie, des cabinets, des forums, aucun
  grand site santé public.
- **Moyenne** : 1 ou 2 grands sites santé ou médias nationaux, le reste en pages moyennes.
- **Élevée** : 3 grands sites santé ou institutions et plus (Ameli, Vidal, Inserm, OMS, Santé.fr, HAS, Doctissimo,
  Passeport Santé).

## Les 15 cibles

Place et impressions : Search Console du 09/10 au 24/10/2026 (« — » = aucune impression sur cette requête exacte).
Top 10 : Brave Search sauf mention, 22-25/10/2026. Colonnes de suivi : position Search Console de la requête exacte sur
les 28 derniers jours (ou « — »), notée par la tâche hebdomadaire du mardi.

| # | Recherche cible | Page | Place SC | Impr. | Volume probable | Qui occupe le top 10 | Pourquoi c'est gagnable | 27/10 | 03/11 | 10/11 | 17/11 | 24/11 | 01/12 | 08/12 | 15/12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | angoisse le soir sans raison | /angoisse-le-soir/ | — (voisine « angoisse soir » 71,5) | 0 | moyen (1re suggestion de « angoisse le soir ») | DuckDuckGo : sans-lendemain.fr, stress-zero.fr, psychologue.net, **notre page 4e**, cpositif, psy-92, morganemullerpsy, guerir-anxiete, Passeport Santé 10e. Brave : inicea, psychologue.net, sleepie, Santé Magazine, stress-zero, Top Santé, qare, dergam, thebalance.clinic, Passeport Santé | Blogs et cabinets de psy, un seul grand site santé, et la page est déjà 4e sur DuckDuckGo | | | | | | | | |
| 2 | angoisse matinale sans raison | /angoisse-le-matin/ | 86 | 2 | moyen (2e suggestion de « angoisse matinale » ; Trends « angoisse le matin » ≈ 3,7) | cliniclesalpes, psychologue.fr, stepyz, guerir-anxiete, laurentbonniec, vitanutrics, psychologue.net, psy-92, Santé Magazine, ecoute-psy | Aucun grand site santé ; la page, en ligne depuis le 21/10, a déjà 14 requêtes « matin » en impressions | | | | | | | | |
| 3 | comment arrêter de ruminer la nuit | /ruminations-le-soir/ | 79 | 3 | moyen (suggestion de « comment arrêter de ruminer », 3 impressions) | therasomnia, naturactive, Forté Pharma, RTL, equilli, handflow, Passeport Santé, monoreilleretmoi, L'Union, mentranova | Surtout des marques (compléments, literie) ; nos 6 techniques sourcées répondent mieux | | | | | | | | |
| 4 | technique respiration pour dormir 4 7 8 | /respiration-pour-dormir/ | 24,2 | 5 | moyen (Trends « respiration 4 7 8 » ≈ 6,4 ; suggestion de « technique respiration dormir ») | Fédération des diabétiques, Medium, dormeur.co, clinique Jacques-Cartier, Santé Magazine, Doctissimo, sleepie, artdelarespiration, monoreilleretmoi, Scribd | Déjà en 3e page ; un seul grand site santé ; pas-à-pas de l'étude Burapha déjà en place | | | | | | | | |
| 5 | réveil nocturne 4h | /reveil-4h-du-matin/ | 35,8 | 4 (1 clic) | moyen (suggestion de « réveil nocturne », Trends « réveil nocturne » ≈ 35) | Femme Actuelle, biocles, PiLeJe, Euphytose, viterapy, sleepdoctor, Top Santé, Journal des Femmes, Facebook, alternatif-bien-etre | Marques et magazines grand public, pas d'institution ; déjà 1 clic | | | | | | | | |
| 6 | procrastination du sommeil causes | /procrastination-du-coucher/ | 57,7 | 3 | moyen (suggestion de « procrastination du sommeil », 3 impressions) | Wikipédia, le-bon-dormeur, therasomnia, reachlink, lavilab, Psychologies, apollohospitals, cbd-coaching, swissflex, retrouver-le-sommeil | Wikipédia mis à part, des blogs ; peu de pages traitent vraiment les causes avec des études | | | | | | | | |
| 7 | routine du soir pour bien dormir | /routine-du-soir-anti-stress/ | — | 0 | moyen (1re suggestion de « routine du soir pour ») | Welcome to the Jungle, morphee.co, apnolab, sleepie, Forté Pharma, Santarome, anatae, romatic, Elle, papills | Marques et magazines, aucune source médicale ; notre page compare INSV et Assurance maladie | | | | | | | | |
| 8 | cortisol élevé la nuit | /cortisol-et-sommeil/ | — | 0 | faible à moyen (suggestion de « cortisol la nuit » ; « cortisol élevé » ≈ 240 mais écarté, trop disputé) | medecindirect, Nutri&Co, Passeport Santé, mcclinic, wellengo, Dynveo, sleepdoctor, blood-analysis, copmed, omum | Surtout des vendeurs de compléments ; les études de Chicago et de Pennsylvanie sont déjà dans la page | | | | | | | | |
| 9 | le cortisol et le stress | /cortisol-hormone-du-stress/ | 87,7 | 6 | moyen (6 impressions, la requête la plus vue du site avec « cortisol définition ») | Familiprix, Institut du Cerveau, vmmed, presse Inserm, solage, Nutri&Co, Wikipédia, Nutripure, Santé Magazine, medecindirect | Concurrence moyenne (2 institutions), mais Google montre déjà la page sur 30 requêtes « cortisol » | | | | | | | | |
| 10 | hypervigilance symptômes | /hypervigilance/ | — (« hypervigilance définition » 98) | 0 | moyen (suggestion du terme seul ; « hypervigilance » ≈ fort dans Trends, l'expression longue sous le seuil) | Wikipédia, reachlink, anxiete.fr, Doctissimo, couette-castex, pascalefarrugia, nervoussystemwealth, Refinery29, Passeport Santé, psychologue.net | 2 grands sites santé, le reste en blogs ; notre tableau des symptômes est sourcé (Inserm, MSD) | | | | | | | | |
| 11 | comment réguler son système nerveux | /calmer-son-systeme-nerveux/ | 68 | 1 | moyen (1re suggestion de « comment réguler », 3 requêtes « réguler » en impressions) | marionrocher, Calm, nervoussystemwealth, chezlosteo, Nike, namaka, Vogue, reachlink, jebreathwork, CK-12 | Aucun site santé français ; des applications et des coachs | | | | | | | | |
| 12 | activer le nerf vague par la respiration | /nerf-vague/ | — | 0 | faible à moyen (suggestion de « activer le nerf vague » ; « stimuler le nerf vague » ≈ 11) | spatiu, CSS (assureur suisse), laboratoires-unisson, artztneuro, cliniquehss, adeline-paolini, lifeplus, sarrasaidi, Wim Hof, sophrologue | Que des blogs et des marques ; notre intertitre reprend déjà la formulation | | | | | | | | |
| 13 | charge mentale symptômes physiques | /charge-mentale/ | — (« charge mentale définition » 97) | 0 | faible à moyen (suggestion de « charge mentale signes ») | terapiz, Carenity, laboratoire Hollis, la compagnie des lavandières, coachproperso, optimike, Solimut, charge-partagee, brunet.ca, Doctissimo | Un seul grand site santé ; personne ne relie ces signes aux repères de la HAS | | | | | | | | |
| 14 | symptômes physiques du stress chronique | /symptomes-physiques-du-stress/ | — (« symptomes stress » 91) | 0 | moyen (3e suggestion du terme principal) | theraserena, qare, OMS, medecindirect, psychologue.net, santepsy.ch, Dynveo, Monin-Chanteaud, copmed, Passeport Santé | Moyenne (OMS, Passeport Santé) ; la variante « … et de l'angoisse » est écartée (Ameli, Vidal, Inserm, Québec.ca en tête) | | | | | | | | |
| 15 | que manger contre le stress | /alimentation-anti-stress/ | — (« petit dejeuner anti stress » 92) | 0 | moyen (Trends ≈ 2, suggestion de « manger contre le stress ») | Forté Pharma, surlesentierdesbergers, LMDE, procure.ca, hife-coliving, Nutri&Co, physionorm, Darwin Nutrition, Mutualia, theraserena | Mutuelles et vendeurs de compléments ; notre page s'appuie sur les recommandations officielles | | | | | | | | |

**Pages non ciblées cette fois.** `/baisser-son-cortisol-naturellement/` : top 10 occupé par des marques de compléments
et des vidéos (jevaismieuxmerci, miye, YouTube, biogena, herboristeries…), recherche à la mode et très commerciale,
qui recoupe en plus « comment baisser le cortisol la nuit » (cortisol et sommeil). `/signes-du-burn-out/` : « burn out
symptômes » est déjà écarté pour concurrence (`articles-a-ecrire.md`), et « premiers signes burn out » mêle Santé.fr,
des plateformes de téléconsultation et une association ; Google y place en plus Ameli, la HAS et l'INRS. Elles restent
suivies dans `mots-cles.md`.

## Ce qui a été fait sur chaque page (25/10/2026)

Voir le journal (`04-journal-decisions.md`, section 84). En résumé : une partie ou une question fréquente qui reprend
la formulation exacte de la recherche, avec une réponse directe en tête et uniquement des sources déjà présentes ; titre
SEO ou description retouchés quand la recherche n'y figurait pas ; au moins 3 liens contextuels vers chaque page cible
depuis des articles proches. `/respiration-pour-dormir/` et `/reveil-4h-du-matin/` ont été retouchées les 18 et
21/10 : on n'y change rien (règle de `optimisation-mensuelle.md` : attendre un mois de données), seuls des liens
internes s'ajoutent.

## Suivi chaque semaine (tâche du mardi)

1. Search Console via Composio, `dimensions` = `["query", "page"]`, 28 derniers jours.
2. Pour chaque ligne : position de la **requête exacte** dans la colonne de la semaine (« — » si aucune impression),
   puis la meilleure requête proche de la même page si elle est plus haute (ex. « 24,2 / proche : technique 4 7 8 19 »).
3. Signal à surveiller : une cible qui passe sous 30 → vérifier que la page répond toujours en tête de partie ; une cible
   toujours à « — » au bout de 4 semaines → vérifier l'indexation de la page (inspection d'adresse), puis revoir la cible.
4. Ne pas retoucher une page plus d'une fois par mois sur la même requête.

## Longue traîne : volume et difficulté, par sujet

Trends = intérêt sur 12 mois par rapport à « angoisse le soir » (= 1), France, lu le 22/10/2026 (0 = sous le seuil).
« Sugg. » = présente dans les suggestions Google. Difficulté d'après le top 10 Brave quand il a été lu, sinon estimée.

### Angoisse le soir (`/angoisse-le-soir/`)
| Requête | Signaux | Volume | Difficulté |
|---|---|---|---|
| angoisse le soir sans raison | sugg. n° 1, Trends 0 | moyen | faible (notre page 4e sur DuckDuckGo) |
| stress la nuit / stress la nuit que faire | Trends ≈ 14 (référence fiable dans ce groupe), sugg. | fort | moyenne (estimée) |
| anxiété la nuit | Trends ≈ 3 | moyen | moyenne (estimée) |
| angoisse la nuit que faire | Trends « angoisse la nuit » ≈ 1,4, sugg. | moyen | faible (DuckDuckGo : psychologue.net, ecoute-psy, annuaires, literie) |
| crise d'angoisse la nuit que faire | Trends ≈ 0,2 à 0,3, sugg. | faible | moyenne |
| angoisse le soir avant de dormir | sugg. | faible | — |

### Angoisse le matin (`/angoisse-le-matin/`)
| Requête | Signaux | Volume | Difficulté |
|---|---|---|---|
| angoisse le matin (au réveil) | Trends ≈ 3,7, sugg., 14 requêtes « matin » en impressions | moyen | faible (blogs, cabinets) |
| angoisse matinale sans raison | sugg. n° 2, 2 impressions | moyen | faible |
| stress du matin / stress au réveil | sugg., 4 impressions | moyen | — |
| angoisse au réveil que faire | sugg., Trends 0 | faible | faible (vitanutrics, kaliora, Santé Magazine…) |
| angoisse matinale traitement | sugg., 1 impression | faible | — |

### Ruminations le soir (`/ruminations-le-soir/`)
| Requête | Signaux | Volume | Difficulté |
|---|---|---|---|
| rumination nocturne | Trends ≈ 1,7, 3 impressions, 1 clic | moyen | faible (equilli, therasomnia, Charente Libre…) |
| ruminer la nuit | Trends ≈ 1,7 | moyen | — |
| comment arrêter de ruminer la nuit | sugg., 3 impressions | moyen | faible |
| arrêter de ruminer le passé | sugg. (Trends « arrêter de ruminer » ≈ 0,1) | faible | — (sujet de journée, hors page) |
| pensées qui tournent en boucle | sugg. | faible | — |

### Respiration pour dormir (`/respiration-pour-dormir/`)
| Requête | Signaux | Volume | Difficulté |
|---|---|---|---|
| respiration carrée | Trends ≈ 9,8 | fort | — (voir nouveaux articles) |
| respiration 4 7 8 | Trends ≈ 6,4 | fort | — |
| respiration militaire pour dormir | Trends ≈ 3,7 | moyen | moyenne (Ouest-France, BBC, Vanity Fair, RTL…) |
| technique respiration pour dormir 4 7 8 | sugg., 5 impressions, place 24 | moyen | faible à moyenne |
| respiration 4 7 8 combien de fois par jour | sugg. | faible | — |
| respiration pour dormir | Trends ≈ 0,9 | moyen | — |

### Réveil à 4 h du matin (`/reveil-4h-du-matin/`)
| Requête | Signaux | Volume | Difficulté |
|---|---|---|---|
| réveil nocturne | Trends ≈ 35 | fort | élevée (terme court) |
| réveil 4h du matin | Trends ≈ 2,5 | moyen | — (suggestions dominées par « médecine chinoise », « spirituel ») |
| réveil nocturne 4h | sugg., 4 impressions, place 36 | moyen | faible à moyenne |
| réveil à 3h du matin | Trends ≈ 0,7 | moyen | — |
| se réveiller à 4h du matin que faire | sugg. | faible | — |

### Procrastination du coucher (`/procrastination-du-coucher/`)
| Requête | Signaux | Volume | Difficulté |
|---|---|---|---|
| se coucher tard (conséquences) | Trends ≈ 1,4 à 2,8, sugg. « conséquences », « danger » | moyen | — |
| procrastination du sommeil | Trends ≈ 0,3, 2 impressions | faible à moyen | — |
| procrastination du sommeil causes | sugg., 3 impressions, place 58 | moyen | faible |
| procrastination du coucher | Trends 0, 2 impressions | faible | moyenne (Wikipédia, Ouest-France, Le Figaro Madame, Elle) |
| procrastination du sommeil tdah | sugg. | faible | — (pas de source vérifiée sur le site) |

### Routine du soir (`/routine-du-soir-anti-stress/`)
| Requête | Signaux | Volume | Difficulté |
|---|---|---|---|
| routine du soir pour bien dormir | 1re sugg. de « routine du soir pour », Trends 0 | moyen | faible |
| rituel du soir adulte | sugg. | faible | — |
| routine du soir | sugg. dominées par enfant, bébé, peau | — | élevée et hors sujet |

### Cortisol et sommeil (`/cortisol-et-sommeil/`)
| Requête | Signaux | Volume | Difficulté |
|---|---|---|---|
| cortisol élevé la nuit | sugg., Trends 0 | faible à moyen | faible |
| cortisol et sommeil | Trends ≈ 0,3 | faible | — |
| comment baisser le cortisol la nuit | sugg. | faible | — |
| cortisol élevé symptômes | Trends ≈ 0,7 | moyen | élevée (écarté) |

### Cortisol, hormone du stress (`/cortisol-hormone-du-stress/`)
| Requête | Signaux | Volume | Difficulté |
|---|---|---|---|
| hormone du stress | Trends ≈ 45, 3 impressions (place 56) | fort | élevée |
| cortisol c'est quoi | Trends très haut (correspondance large de Trends, à prendre avec prudence), 4 impressions | fort | — |
| cortisol définition | 6 impressions, place 82 | moyen | — |
| le cortisol et le stress | 6 impressions, place 88 | moyen | moyenne |
| cortisol rôle | Trends ≈ 1,7 | moyen | — |

### Hypervigilance (`/hypervigilance/`)
| Requête | Signaux | Volume | Difficulté |
|---|---|---|---|
| hypervigilance | Trends très au-dessus de la référence | fort | moyenne à élevée |
| hypervigilance symptômes | sugg., Trends 0 | moyen | moyenne |
| hypervigilance comment en sortir / sortir de l'hypervigilance | sugg., 1 impression | faible | — |
| hypervigilance sommeil | sugg. | faible | — |

### Calmer son système nerveux (`/calmer-son-systeme-nerveux/`)
| Requête | Signaux | Volume | Difficulté |
|---|---|---|---|
| tension nerveuse | Trends ≈ 12 (référence petite dans ce groupe) | fort | — (question fréquente déjà dans la page) |
| comment réguler son système nerveux | sugg., 1 impression, place 68 | moyen | faible |
| réguler son système nerveux exercice | sugg., 1 impression | faible | — |
| calmer ses nerfs | Trends 0, sugg. (souvent mots fléchés) | faible | — |

### Nerf vague (`/nerf-vague/`)
| Requête | Signaux | Volume | Difficulté |
|---|---|---|---|
| nerf vague | Trends très haut | fort | élevée |
| stimuler le nerf vague | Trends ≈ 11 | fort | — |
| activer le nerf vague par la respiration | sugg. | faible à moyen | faible |
| comment activer le nerf vague pour dormir | sugg. | faible | — |

### Charge mentale (`/charge-mentale/`)
| Requête | Signaux | Volume | Difficulté |
|---|---|---|---|
| charge mentale | Trends très haut | fort | élevée |
| comment alléger sa charge mentale | sugg. | faible à moyen | — |
| charge mentale symptômes physiques | sugg. | faible à moyen | faible |
| charge mentale au travail | sugg. (« diminuer la charge mentale au travail ») | faible | — |

### Symptômes physiques du stress (`/symptomes-physiques-du-stress/`)
| Requête | Signaux | Volume | Difficulté |
|---|---|---|---|
| symptômes du stress | Trends ≈ 7, 9 impressions sur les variantes | fort | élevée |
| mal de ventre stress | Trends ≈ 14 | fort | — |
| palpitations stress | Trends ≈ 13 | fort | — (voir nouveaux articles) |
| douleur poitrine stress | Trends ≈ 5 à 7 | moyen | — |
| symptômes physiques du stress chronique | sugg. n° 3 | moyen | moyenne |
| symptômes physiques du stress et de l'angoisse | sugg. n° 2 | moyen | élevée (Ameli, Vidal, Inserm, Québec.ca) |

### Alimentation anti-stress (`/alimentation-anti-stress/`)
| Requête | Signaux | Volume | Difficulté |
|---|---|---|---|
| que manger contre le stress | Trends ≈ 2, sugg. | moyen | faible |
| aliments anti stress (angoisse) | sugg. n° 1, Trends 0 | moyen | faible (Nutri&Co, Forté Pharma, mutuelles) |
| petit déjeuner anti stress | 1 impression | faible | — |

### Signes du burn-out et baisser son cortisol (non ciblées)
| Requête | Signaux | Volume | Difficulté |
|---|---|---|---|
| symptômes burn out | Trends ≈ 33 | fort | élevée |
| premiers signes burn out | sugg., Trends 0 | faible à moyen | moyenne |
| comment baisser le cortisol | Trends très haut | fort | élevée (marques, vidéos) |
| baisser son cortisol naturellement | Trends ≈ 0,3, 1 impression voisine | faible à moyen | moyenne (marques) |

## Nouveaux articles possibles (requêtes à volume sans page, sans recouper un article)

Reportés dans `articles-a-ecrire.md`.

| Recherche | Signaux | Volume | Remarque |
|---|---|---|---|
| respiration carrée (bienfaits, combien de temps, anxiété) | Trends ≈ 9,8, 10 suggestions dans le sujet | fort | Angle « se calmer en journée », sans refaire la partie sommeil de `/respiration-pour-dormir/` (qui garderait la 4-7-8 et renverrait vers la nouvelle page) ; illustration dessinée et schéma obligatoires (règle du 22/10) ; ne jamais viser « cohérence cardiaque » |
| boule au ventre stress (angoisse permanente) | Trends « boule au ventre » ≈ 240, mais en partie une chanson ; suggestion « stress » en 3e | fort | Déjà n° 8 de la liste : viser « boule au ventre stress », jamais le terme seul |
| palpitations stress (que faire, angoisse) | Trends ≈ 13, 10 suggestions | fort | Sujet santé sensible : urgence cardiaque en tête, sources Ameli ; ne pas refaire la partie « cœur » de `/symptomes-physiques-du-stress/`, y renvoyer |
| sommeil léger | Trends ≈ 7 | moyen à fort | Déjà n° 10 de la liste |
| fatigue nerveuse | Trends ≈ 7 | moyen à fort | Déjà n° 9 de la liste |
| pensées intrusives (anxiété, exemples, causes) | Trends ≈ 5, 10 suggestions | moyen | Prudence : lien avec le TOC, sources psychiatriques solides obligatoires ; distinct des ruminations du soir |
| mâchoire serrée stress | Trends ≈ 0,2 | faible | Déjà n° 4 de la liste, volume plus faible qu'estimé |

## Top 15 des requêtes de longue traîne par volume probable

| # | Requête | Volume probable | Page visée |
|---|---|---|---|
| 1 | stress la nuit que faire | fort | /angoisse-le-soir/ (requête secondaire) |
| 2 | mal de ventre stress | fort | nouvel article (avec « boule au ventre stress ») |
| 3 | palpitations stress | fort | nouvel article |
| 4 | respiration carrée bienfaits | fort | nouvel article |
| 5 | stimuler le nerf vague | fort | /nerf-vague/ |
| 6 | respiration 4 7 8 pour dormir | fort | /respiration-pour-dormir/ |
| 7 | fatigue nerveuse symptômes | moyen à fort | nouvel article (déjà listé) |
| 8 | sommeil léger que faire | moyen à fort | nouvel article (déjà listé) |
| 9 | angoisse le matin au réveil | moyen | /angoisse-le-matin/ |
| 10 | respiration militaire pour dormir | moyen | /respiration-pour-dormir/ |
| 11 | anxiété la nuit | moyen | /angoisse-le-soir/ |
| 12 | réveil nocturne 4h | moyen | /reveil-4h-du-matin/ |
| 13 | rumination nocturne | moyen | /ruminations-le-soir/ |
| 14 | que manger contre le stress | moyen | /alimentation-anti-stress/ |
| 15 | pensées intrusives anxiété | moyen | nouvel article |
