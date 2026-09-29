# Règles éditoriales — à appliquer avant tout ajout de contenu

Ces règles ont toutes été établies suite à des problèmes réellement rencontrés sur ce compte (voir `04-journal-decisions.md` pour le contexte de chacune). Elles s'appliquent à tout nouveau pin ou vidéo ajouté à `pins.json` / `videos.json`, que ce soit par Claude ou manuellement.

**Point de départ essentiel : le script de publication ne fait aucun contrôle de pertinence.** Il publie tel quel le prochain élément non publié de la banque, dans l'ordre. Toute la responsabilité de qualité et de cohérence repose sur ce qui est ajouté en amont.

---

## 1. Zéro duplicata (exigence non négociable)

Pinterest pénalise le contenu dupliqué ou quasi-dupliqué.

- **Titres** : uniques à 100 %. Vérifier à la fois l'égalité stricte ET la quasi-similarité (ex. `difflib.SequenceMatcher(None, a, b).ratio() > 0.72` en Python) — un titre où un seul mot change par rapport à un autre reste un quasi-duplicata aux yeux de Pinterest.
- **Images** : jamais deux fichiers identiques au niveau binaire (vérifiable par hash MD5/SHA).
- **Descriptions** : pas de copier-coller d'une description à l'autre avec juste un mot changé.
- **Méthode de vérification recommandée** : toujours vérifier par script après tout ajout ou modification, jamais "à l'œil".

## 2. Cohérence entre le texte, l'image et le périmètre du compte

Avant d'ajouter un pin :

- Le texte (titre, texte_image, description) doit se rattacher clairement à un des 9 thèmes du compte, à travers l'angle stress/mental — jamais de contenu générique (recette, déco, organisation domestique...) sans lien explicite avec le sommeil, le stress ou le système nerveux.
  - *Exemple à éviter* : "Range ton frigo" sans lien avec le stress.
  - *Exemple qui convient* : "Ce que le désordre du frigo dit de ta charge mentale."
- L'image (fond choisi, généré, ou fournie) doit correspondre au sujet réel du texte, pas seulement au thème détecté automatiquement par mot-clé.
- En cas de lot de contenu reçu en bloc (infographies fournies par l'utilisateur, par exemple), trier avant l'ajout : écarter ce qui ne rentre pas dans le périmètre plutôt que tout ajouter par défaut.

## 3. Le thème est déterminé par le PREMIER hashtag, pas par le sujet apparent

Le routage vers le bon tableau Pinterest dépend uniquement du premier hashtag de la description (fonction `deviner_theme()`). Un pin peut sembler traiter du sommeil dans son texte mais partir sur le mauvais board si son premier hashtag n'est pas un alias de `sommeil`.

**Toujours placer en premier hashtag celui qui correspond au vrai board visé**, même si d'autres hashtags thématiques apparaissent aussi dans la description. Erreur déjà rencontrée : des pins sur le café/l'alcool et leur effet sur le sommeil routés par erreur vers le board alimentation parce que `#cafeine`/`#alcool` étaient en première position (ces alias pointent vers `alimentation`) — corrigés en réordonnant les hashtags.

## 4. Règle spécifique au board "Alimentation et stress"

Ce board sert **uniquement** à montrer comment l'alimentation **diminue le stress** (cortisol, tension nerveuse, nervosité). Jamais l'alimentation pour le sommeil ou l'énergie seuls — ces angles existent déjà via les boards `sommeil` et `energie`.

Un pin alimentation dont le bénéfice mis en avant est l'endormissement ou l'énergie, sans mention explicite du stress/tension/nervosité dans le texte, ne va pas sur ce board (soit on reformule pour ajouter l'angle stress, soit on route le pin vers le bon board en changeant son premier hashtag).

## 5. Lien de destination conditionnel selon le périmètre de la formation

`LIEN_PAGE` pointe vers la page de capture d'une formation dont le contenu ne couvre que **le sommeil et les mécanismes du stress au sens large** (nervosité, tensions physiques, blocages, postures) — pas tous les thèmes du compte. Envoyer ce lien sur un pin hors-sujet génère des clics non qualifiés (visiteurs intéressés par un sujet que la formation ne traite pas) — contre-productif pour l'objectif business (voir `00-vue-ensemble.md`).

- **Thèmes avec lien** (couverts par la formation) : `sommeil`, `systemenerveux`, `posturesantistress`, `blocagemental`, `somatisation`.
- **Thèmes sans lien** (hors périmètre, à ce jour) : `alimentation`, `procrastination`, `energie`, `fatiguementale`. Codé dans `THEMES_SANS_LIEN` (`pins.yml` et `videos.yml`).
- **Conséquence pour la rédaction** : un pin sur un thème sans lien ne doit **jamais** promettre un contenu "dans le guide gratuit" ni inviter à "cliquer sur cette épingle pour le découvrir" — il n'y a rien derrière. Le CTA doit être adapté : fin informative, ou invitation à enregistrer l'épingle sur Pinterest (ça reste possible sans lien de destination), jamais une promesse de contenu accessible par clic.
- **Piège identifié le 28/09/2026** : le thème/premier hashtag d'un pin ne garantit pas que son **contenu réel** correspond à ce que couvre la formation. Un pin peut être tagué `#energie` en tête (donc a priori "avec lien") tout en étant en fait un pin alimentation déguisé (contenu 100 % petit-déjeuner/nutrition) — vérifier le contenu, pas seulement le tag, avant d'accepter un CTA "guide gratuit".
- Si le périmètre de la formation change un jour, mettre à jour `THEMES_SANS_LIEN` dans les deux workflows en conséquence.

## 6. Stratégie des titres

**Mise à jour du 28/09/2026, basée sur les vraies données Pinterest Analytics** (connexion établie ce jour-là, voir `04-journal-decisions.md` section 9) — remplace la précédente recommandation "70% problème/curiosité" qui n'était qu'une hypothèse de bonnes pratiques génériques, jamais vérifiée sur ce compte.

**Constat** : les 8 pins avec le plus d'enregistrements du compte (jusqu'à 286 saves, 22 386 impressions sur un seul pin) sont tous antérieurs à cette session (créés entre décembre 2025 et juin 2026) et partagent un même gabarit :
- **Titre à chiffre / listicle** : *"5 Clés pour Vaincre la Procrastination"*, *"Les 9 signes d'un cortisol élevé"*, *"6 étapes pour débloquer ton mental"*, *"Cortisol élevé : 7 aliments à privilégier"*, *"5 façons naturelles de calmer ton système nerveux"*.
- **Format infographie/liste numérotée**, pas une phrase-accroche narrative unique.

**Règle actuelle** :
- **Privilégier un titre à chiffre quand le contenu s'y prête** (nombre d'étapes, de signes, de gestes, d'aliments...) — c'est le format qui a le mieux performé sur ce compte précis, pas une préférence générique.
- Garder de la variété : tous les titres n'ont pas à être des listicles (un pin peut légitimement rester narratif/question quand ça correspond mieux au contenu), mais le chiffre doit redevenir un réflexe par défaut plutôt qu'une exception.
- **Jamais le même titre sur plusieurs pins.**
- **Maximum 100 caractères** (le script tronque strictement au-delà).
- **Continuer à surveiller Pinterest Analytics** (accès disponible depuis le 28/09/2026 via le connecteur Composio, voir `01-architecture-technique.md`) pour affiner cette règle avec plus de données au fil du temps plutôt que de se fier à un échantillon de 8 pins indéfiniment.

## 7. Standards de description (longueur, SEO, structure)

- **Corps du texte (hors hashtags) visé entre 380 et 450 caractères.** Nettement plus riche qu'une description minimaliste, avec des détails concrets et actionnables plutôt que du remplissage. Toujours vérifier avec `len()` en Python.
- **Description totale (corps + hashtags) toujours ≤ 495-500 caractères** — limite Pinterest ; au-delà, le script tronque automatiquement (parfois au milieu d'une phrase), donc mieux vaut écrire directement dans la limite. *(Note : les meilleurs pins historiques du compte dépassent largement cette limite avec des descriptions très structurées — mais on ne peut pas savoir si c'est malgré ou grâce à leur longueur ; on garde la limite actuelle par prudence plutôt que de la lever sur une hypothèse non testée.)*
- **Mots-clés SEO intégrés naturellement**, jamais en bourrage : 2-3 expressions qu'une personne concernée chercherait réellement sur Pinterest, insérées dans des phrases utiles à lire pour un humain d'abord, pour l'algorithme ensuite.
- **Structure avec des puces emoji quand le contenu s'y prête** (📌 👉 •), à la manière des pins historiques les plus performants, plutôt qu'un bloc de prose uniforme — reste optionnel, à juger au cas par cas, ne pas systématiser au point de perdre en lisibilité.
- **8 à 10 hashtags par pin** (mise à jour du 28/09/2026 — auparavant 5), **dans la limite du plafond de 495-500 caractères ci-dessus, qui reste la contrainte prioritaire.** Les meilleurs pins historiques du compte en utilisent jusqu'à 14, mais leur description totale dépasse largement notre plafond (642 caractères mesurés sur un exemple) — on ne sait pas si ce plafond de 500 est une vraie limite Pinterest ou une prudence excessive de ce pipeline (ces pins historiques ont peut-être été créés par un autre moyen que le webhook Make actuel, jamais vérifié). **Ne pas lever le plafond sans avoir testé qu'un envoi > 500 caractères passe bien par `MAKE_WEBHOOK_URL` sans erreur ni troncature côté Pinterest** — en attendant, rester à 8-10 hashtags courts plutôt que d'aller jusqu'à 14 et dépasser 500. **Le premier hashtag reste strictement le déterminant du board (règle n°3, inchangé)** ; les hashtags ajoutés viennent après, plus génériques/découvrabilité (`#bienetre`, `#developpementpersonnel`, `#selfcare`...). Ne jamais modifier le premier hashtag en même temps qu'on retravaille le corps du texte, sauf intention explicite de changer le board cible.

## 7 bis. Mots-clés : ce que les gens cherchent vraiment (Pinterest Trends France, 29/09/2026)

Source : `PINTEREST_GET_KEYWORD_TRENDS` (région FR, via Composio) — données de recherche Pinterest, pas des suppositions. Évolution sur 1 an entre parenthèses.

- **En hausse, à privilégier** : « système nerveux » (+60 %), « cortisol » (+50 %), « bien-être mental » (+70 %), « routine du soir » (+30 %), « night routine » (+20 %), « sommeil » (+8 %), « journal intime » (+60 %), « cerveau » (+20 %), « discipline aesthetic » (+40 %). « Bien-être hivernal » : nouveau, pic en novembre ; « résolutions bien-être » : pic en janvier.
- **Gros volumes stables** : « calme », « fatigue », « burn out », « dormir », « motivation », « discipline », « organisation », « routine du matin », « charge mentale ».
- **En baisse** : « méditation », « relaxation », « respiration » (−30 %), « fatigue mentale » (−50 %), « productivité » (−40 %) → garder comme mots secondaires, pas en tête de titre.
- « Procrastination » existe mais pèse moins que « motivation » / « discipline » : les associer (« Procrastination : … », hashtags `#discipline #motivation`).
- « Anxiété », « insomnie » n'apparaissent pas dans les tendances : volume plus faible, utiles en mots secondaires.

**Formule de titre des pins populaires de la niche** (observée sur les pins indexés : « Mieux dormir : 17 choses à essayer dès ce soir », « 8 habitudes pour calmer son système nerveux », « Cohérence cardiaque : … ») : **mot-clé recherché en tête**, deux-points, puis promesse concrète (chiffre, durée courte, moment : « dès ce soir », « en 2 minutes »). Le 29/09/2026, 122 titres non publiés sans mot-clé ont été réécrits selon cette formule (le texte sur l'image n'a pas changé), et 324 hashtags à forte demande ajoutés (premier hashtag jamais modifié).

**Descriptions de tableaux** : réécrites le 29/09/2026 avec ces mots-clés (anciennes versions : `archives/descriptions-tableaux-avant-2026-09-29.json`). Le texte alternatif des pins reprend aussi ces expressions (`SUJETS_ALT` dans `pins.yml`).

## 8. Variété des CTA (appels à l'action)

- **Ne jamais répéter systématiquement la même formule de fin** d'un pin à l'autre ("Clique sur cette épingle pour le découvrir" etc.).
- **Viser une grande diversité** : au minimum une quinzaine de formulations distinctes dans l'ensemble de la banque (largement dépassé à ce jour : 218 fins de description uniques sur 220 pins).
- **Ne pas mettre de CTA explicite sur tous les pins** : environ un quart des pins doivent se terminer sur une phrase informative plutôt que sur une invitation à l'action, pour que ça reste naturel et ne sonne pas comme un script répété.
- **Adapter le CTA au lien** : voir règle n°5 — pas de CTA orienté clic/guide sur les thèmes sans lien de destination.

## 9. Interdits stricts (issus du prompt SEO Make.com, voir `prompts/system-prompt-pin-seo.md`)

- Ne jamais mentir sur les performances potentielles d'une épingle, ni prétendre connaître un volume de recherche réel sans données, ni qualifier un contenu de "viral" sans preuve.
- Ne jamais faire de promesse médicale ni de diagnostic. Éviter "guérir", "éliminer définitivement", "100 % efficace" et formulations médicales exagérées similaires.
- Le contenu doit rester crédible, professionnel, écrit pour un humain avant d'être écrit pour l'algorithme.

## 10. Ne jamais toucher un pin déjà publié

Un pin est considéré "déjà publié" si son titre exact apparaît dans `historique.json` (pins) ou `historique_videos.json` (vidéos, par id).

- **Modifier sa description est sans effet** : elle n'est jamais relue une fois publiée.
- **Modifier son titre est risqué** : le système anti-répétition fonctionne par correspondance exacte de titre — changer le titre d'un pin déjà publié le ferait apparaître comme "nouveau" et risquerait de le faire republier, créant un quasi-duplicata sur le compte réel.
- Toujours vérifier `historique.json`/`historique_videos.json` avant de modifier du contenu existant.

## Checklist avant de considérer une tâche terminée

1. JSON valide (`json.load` sans erreur).
2. 0 doublon exact de titre, 0 quasi-doublon (ratio de similarité).
3. Tous les titres ≤ 100 caractères.
4. Toutes les descriptions non publiées ≤ ~500 caractères, corps ~380-450 caractères.
5. Premier hashtag de chaque pin inchangé (sauf intention explicite de changer le board).
6. Pins déjà publiés (présents dans l'historique) strictement inchangés.
7. CTA variés, pas de répétition systématique.
8. Committer et pousser seulement après ces vérifications par script.
