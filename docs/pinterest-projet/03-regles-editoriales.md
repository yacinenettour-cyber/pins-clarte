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

- **Jamais le même titre sur plusieurs pins.**
- **Composition ~70 % problème/curiosité, 30 % solution** pour maximiser les impressions (ex. *"Pourquoi tu te réveilles à 3h du matin (et ce que ça dit de ton système nerveux)"* plutôt que *"3 astuces pour arrêter de te réveiller la nuit"*).
- **Varier les structures d'ouverture** : questions, chiffres, heures précises, affirmations directes, tournures négatives — éviter qu'un même gabarit ("X : ce que tu...", "la question à te poser...") revienne trop souvent.
- **Maximum 100 caractères** (le script tronque strictement au-delà).
- **À terme, se fier à Pinterest Analytics** une fois assez de données accumulées : repérer les formulations qui génèrent le plus d'enregistrements et de clics, orienter les prochains titres en conséquence plutôt que de tester à l'aveugle indéfiniment.

## 7. Standards de description (longueur, SEO, structure)

- **Corps du texte (hors hashtags) visé entre 380 et 450 caractères.** Nettement plus riche qu'une description minimaliste, avec des détails concrets et actionnables plutôt que du remplissage. Toujours vérifier avec `len()` en Python.
- **Description totale (corps + hashtags) toujours ≤ 495-500 caractères** — limite Pinterest ; au-delà, le script tronque automatiquement (parfois au milieu d'une phrase), donc mieux vaut écrire directement dans la limite.
- **Mots-clés SEO intégrés naturellement**, jamais en bourrage : 2-3 expressions qu'une personne concernée chercherait réellement sur Pinterest, insérées dans des phrases utiles à lire pour un humain d'abord, pour l'algorithme ensuite.
- **5 hashtags par pin**, le premier déterminant le board (règle n°3). Ne jamais modifier les hashtags en même temps qu'on retravaille le corps du texte, sauf intention explicite de changer le board cible.

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
