# Les 9 tableaux (boards) Pinterest

Chaque thème du compte a son propre tableau Pinterest, identifié par un ID fixe utilisé par le pipeline (`TABLEAUX` dans `.github/workflows/pins.yml` et `videos.yml`). Le tableau cible est déterminé automatiquement par le **thème détecté à partir du premier hashtag** de la description (voir `01-architecture-technique.md`).

**Légende "Lien formation"** : ✅ = le pin redirige vers la page de capture de la formation (thème couvert par son contenu). ❌ = pas de lien de destination (thème hors périmètre de la formation, voir `03-regles-editoriales.md`).

---

## Sommeil — ID `600175156531998232`

- **Lien formation** : ✅
- **Sujet** : endormissement, insomnie, réveils nocturnes, routine du soir, hygiène de sommeil, environnement de la chambre.
- **Volume** : 112 pins dans la banque (22 déjà publiés, 90 en attente) — de loin le thème le plus fourni, ~51 % de toute la banque. 8 Video Pins (3 publiées). 58 photos de fond dédiées.
- **Premiers hashtags qui routent vers ce board** : `#sommeil`, `#insomnie`, `#reveilnocturne`, `#reveil`, `#sieste`, `#routinedusoir`, `#dimanchesoir`, `#rythmecircadien`, `#lumiere`, `#ecrans`, `#ruminations`.
- **Exemples de titres actuels** :
  - "Ton cerveau ne s'arrête pas la nuit ? 3 gestes simples pour l'apaiser"
  - "Réveil à 3h du matin la tête pleine : quoi faire sur le moment"
  - "Écrans le soir : ce qui compte vraiment pour ton endormissement"

## Système nerveux / cortisol — ID `600175156531995384`

- **Lien formation** : ✅
- **Sujet** : régulation du cortisol, respiration, cohérence cardiaque, anxiété, détente physiologique. C'est aussi le **thème par défaut** quand aucun hashtag reconnu n'est trouvé.
- **Volume** : 27 pins (4 publiés, 23 en attente). 7 Video Pins (1 publiée). 28 photos de fond.
- **Premiers hashtags** : `#cortisol`, `#systemenerveux`, `#respiration`, `#coherencecardiaque`, `#anxiete`, `#detente`.
- **Exemples de titres actuels** :
  - "Respiration lente au lit : l'exercice quand le mental s'emballe"
  - "Scan corporel en 5 minutes pour relâcher les tensions avant de dormir"
  - "Cohérence cardiaque le soir : mode d'emploi simple pour débuter"

## Fatigue mentale — ID `600175156531997290`

- **Lien formation** : ❌ *(changé le 28/09/2026 — voir `04-journal-decisions.md` section 8 ; la formation ne couvre pas l'énergie/fatigue en général)*
- **Sujet** : charge mentale, fatigue chronique, épuisement cognitif.
- **Volume** : 14 pins (4 publiés, 10 en attente). 3 Video Pins (0 publiée). 15 photos de fond.
- **Premiers hashtags** : `#fatiguementale`, `#chargementale`, `#fatigue`, `#fatiguechronique`.
- **Exemples de titres actuels** :
  - "La liste du lendemain : le geste qui coupe les ruminations du soir"
  - "Épuisé la journée mais bien réveillé le soir : pourquoi ce décalage"
  - "Se coucher fatigué et se réveiller épuisé : 4 causes fréquentes"

## Postures anti-stress (au travail) — ID `600175156532003400`

- **Lien formation** : ✅
- **Sujet** : gestes et postures anti-stress réalisables au bureau/en réunion. Routage spécial : détecté quand le premier hashtag est `#stress` ET que `#travail` figure dans les 3 premiers hashtags (sinon `#stress` seul route vers `systemenerveux`).
- **Volume** : 11 pins (1 publié, 10 en attente). 1 Video Pin (0 publiée). 9 photos de fond.
- **Exemples de titres actuels** :
  - "Le sas de décompression : couper avec le travail avant de rentrer"
  - "Boule au ventre en pleine journée de bureau ? Le geste de 30 secondes qui fait retomber la pression"
  - "Tu enchaînes les dossiers sans respirer ? 3 gestes assis pour relâcher avant que ça déborde"

## Blocage mental — ID `600175156532029245`

- **Lien formation** : ✅
- **Sujet** : clarté mentale, décisions bloquées, surcharge cognitive, procrastination liée au blocage (distinct de la procrastination "pure", voir ci-dessous).
- **Volume** : 11 pins (1 publié, 10 en attente). 2 Video Pins (0 publiée). 9 photos de fond.
- **Premiers hashtags** : `#blocagemental`, `#clarte`, `#ecriture`.
- **Exemples de titres actuels** :
  - "Écrire ses inquiétudes : l'exercice des 10 minutes en début de soirée"
  - "Ton écran est ouvert depuis ce matin, pourtant rien n'a bougé : ce blocage a un nom"
  - "Ton esprit saute d'une pensée à l'autre sans jamais se poser, et voici pourquoi"

## Somatisation — ID `600175156532027560`

- **Lien formation** : ✅
- **Sujet** : douleurs physiques liées au stress accumulé (dos, mâchoire, maux de tête, tensions).
- **Volume** : 10 pins (0 publié, 10 en attente). 1 Video Pin (0 publiée). 8 photos de fond.
- **Premiers hashtags** : `#somatisation`, `#douleurs`.
- **Exemples de titres actuels** :
  - "Ce mal de dos du soir qui n'a rien à voir avec ta posture"
  - "Mâchoire douloureuse au réveil : ce que ton corps serre pendant que tu dors"
  - "Encore mal à la tête en fin de journée : la piste que tu n'as pas encore explorée"

## Énergie — ID `600175156532025122`

- **Lien formation** : ❌ *(changé le 28/09/2026 — voir `04-journal-decisions.md` section 8 ; la formation ne couvre pas l'énergie/fatigue en général)*
- **Sujet** : fatigue énergétique (distincte de la fatigue mentale), récupération, coups de barre, vraie/fausse récupération.
- **Volume** : 17 pins (0 publié, 17 en attente). 3 Video Pins (0 publiée). 19 photos de fond.
- **Premiers hashtags** : `#energie`, `#recuperation`.
- **Exemples de titres actuels** :
  - "Le trou d'énergie de 11h se joue souvent dans ton assiette du matin"
  - "Pourquoi ce coup de barre arrive presque toujours à la même heure"
  - "Ces pauses censées te recharger qui vident ton énergie en réalité"

## Alimentation et stress — ID `600175156532001498`

- **Lien formation** : ❌ *(voir `03-regles-editoriales.md` pour la règle complète)*
- **Sujet — règle stricte** : uniquement l'alimentation **comme levier pour réduire le stress** (cortisol, tension nerveuse, nervosité). Jamais l'alimentation pour le sommeil ou l'énergie seuls — ces angles vont sur les boards `sommeil`/`energie`. Jamais de contenu recette/organisation cuisine sans lien avec le stress (11 pins de ce type ont été retirés de la banque le 27/09/2026, voir `04-journal-decisions.md`).
- **Volume** : 8 pins (0 publié, 8 en attente) — délibérément restreint par la règle ci-dessus. 3 Video Pins (0 publiée). 37 photos de fond (banque plus large que nécessaire vu le faible volume de pins).
- **Premiers hashtags** : `#alimentation`, `#cafeine`, `#alcool`, `#digestion` — **attention** : un pin peut mentionner l'alimentation sans que ce soit son premier hashtag ; c'est le premier hashtag qui route réellement vers ce board.
- **Pas de lien de destination** → les CTA ne doivent jamais promettre un contenu "dans le guide gratuit" ou inviter à cliquer.
- **Exemples de titres actuels** :
  - "Irritable en fin de journée : ton assiette y est peut-être pour beaucoup"
  - "Repousser le déjeuner pour tenir la réunion fait grimper ton stress en silence"
  - "Ce mal de tête de 17h n'est peut-être pas seulement une question de stress"

## Procrastination — ID `600175156532025119`

- **Lien formation** : ❌ *(voir `03-regles-editoriales.md` pour la règle complète)*
- **Sujet** : mécanismes de la procrastination, blocage au démarrage, peur de l'échec, discipline qui s'effondre.
- **Volume** : 10 pins (0 publié, 10 en attente). 2 Video Pins (0 publiée). 9 photos de fond.
- **Pas de lien de destination** → mêmes règles de CTA que le board alimentation.
- **Exemples de titres actuels** :
  - "Il y a une heure précise, chaque jour, où ta motivation s'effondre : laquelle ?"
  - "La phrase automatique que ton cerveau te souffle juste avant l'ordinateur"
  - "Et si tu ne remettais pas ce projet par manque de temps, mais par peur du résultat ?"

---

## Récapitulatif chiffré

| Board | ID | Lien formation | Pins (total/publiés/restants) | Vidéos (total/publiées) | Fonds |
|---|---|---|---|---|---|
| Sommeil | 600175156531998232 | ✅ | 112 / 22 / 90 | 8 / 3 | 58 |
| Système nerveux | 600175156531995384 | ✅ | 27 / 4 / 23 | 7 / 1 | 28 |
| Énergie | 600175156532025122 | ❌ *(depuis le 28/09)* | 17 / 0 / 17 | 3 / 0 | 19 |
| Fatigue mentale | 600175156531997290 | ❌ *(depuis le 28/09)* | 14 / 4 / 10 | 3 / 0 | 15 |
| Postures anti-stress | 600175156532003400 | ✅ | 11 / 1 / 10 | 1 / 0 | 9 |
| Blocage mental | 600175156532029245 | ✅ | 11 / 1 / 10 | 2 / 0 | 9 |
| Somatisation | 600175156532027560 | ✅ | 10 / 0 / 10 | 1 / 0 | 8 |
| Procrastination | 600175156532025119 | ❌ | 10 / 0 / 10 | 2 / 0 | 9 |
| Alimentation et stress | 600175156532001498 | ❌ | 8 / 0 / 8 | 3 / 0 | 37 |
| **Total** | | | **220 / 32 / 179*** | **30 / 4*** | **192** |

*Nombres de pins/vidéos publiés en légère évolution continue, le pipeline publie automatiquement 7×/jour ; chiffres à jour au 27/09/2026 en fin de session d'audit (voir aussi `00-vue-ensemble.md` pour un état légèrement antérieur, 41 pins publiés). Colonne "Lien formation" mise à jour le 28/09/2026 pour `energie`/`fatiguementale` (voir `04-journal-decisions.md` section 8) ; le reste du tableau (volumes) n'a pas été recalculé depuis et est donné à titre indicatif — se fier à `pins.json`/`fonds_themes.json` pour les chiffres exacts.

**Déséquilibre à surveiller** : le board Sommeil concentre à lui seul ~51 % de la banque de pins. Ce n'est pas une erreur (c'est le cœur du compte), mais ça mérite un regard si l'objectif devient de développer davantage les autres boards.
