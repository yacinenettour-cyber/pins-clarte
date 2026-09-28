# pins-clarte

Publication automatique de pins Pinterest pour "Clarté Mentale | Stress & Énergie", via GitHub Actions + Make.com.

## Fonctionnement

Le workflow `.github/workflows/pins.yml` est déclenché 7 fois par jour (6h07, 8h07, 10h07, 12h07, 14h07, 16h07, 18h07 UTC) par un service externe gratuit (cron-job.org), qui appelle l'API GitHub pour lancer le workflow. On n'utilise plus le déclencheur `schedule` natif de GitHub Actions, qui peut être retardé ou complètement sauté pendant les pics de charge — voir la section **Déclenchement (cron-job.org)** plus bas.

À chaque exécution :

1. Il choisit un pin (titre + description + phrase d'accroche) dans une banque de textes déjà écrits, en évitant les répétitions récentes (voir `historique.json`).
2. Il devine le thème du pin (sommeil, système nerveux, fatigue mentale, alimentation, procrastination, somatisation, énergie, blocage mental, postures anti-stress) à partir du premier hashtag de la description, puis choisit une photo de fond du même thème dans `fonds/` (voir `fonds_themes.json`) — pour que l'image corresponde toujours au texte, par exemple pas de photo de petit-déjeuner sur un pin qui parle de réveil nocturne.
3. Il génère une image verticale (1000x1500) avec la phrase d'accroche posée sur ce fond (si `fonds/` est vide, un fond dégradé par défaut est utilisé).
4. Il commit l'image dans le dépôt et récupère son URL publique.
5. Il envoie titre / description / URL de l'image / lien vers un webhook Make.com, qui publie le pin sur Pinterest.

## Génération d'images via les connecteurs Claude (Claude_image / Hugging Face / Canva)

Cette session dispose de plusieurs connecteurs de génération/édition d'images, indépendants du système `OPENAI_API_KEY` décrit plus bas (qui reste le seul utilisé par le pipeline automatique en production) :

- **Claude_image** (payant, crédits limités) — vérifier le solde avec `get_credits` avant toute génération ; `quote_generation` donne le coût exact par modèle avant de lancer. Un appel qui time out peut quand même consommer le crédit.
- **Hugging Face** (`gr1_z_image_turbo_generate`, gratuit) — supporte nativement la résolution `1024x1536 (2:3)`, exactement le format des pins du compte. Quota gratuit journalier limité (ZeroGPU) : peut s'épuiser en cours de session, message d'erreur explicite ("ZeroGPU quota exceeded").
- **Canva** (`generate-image`) — testé et validé le 28/09/2026. **Consigne permanente de l'utilisateur : toujours basculer sur Canva quand Claude_image n'a plus de crédit** (et plus généralement, c'est la solution de repli à essayer si Hugging Face est aussi à quota épuisé).

**Ordre de priorité** : Hugging Face (gratuit) → Claude_image (si `get_credits` > 0) → Canva (repli systématique, sans redemander confirmation à l'utilisateur).

**Limite technique connue de Canva** : l'export en pleine résolution (`export-design`) télécharge depuis `export-download.canva.com`, qui n'est pas sur la liste des hôtes autorisés par le proxy réseau du sandbox (`curl` échoue avec une erreur 403 de la passerelle). Contournement qui fonctionne : récupérer le meilleur aperçu inline disponible via `read-design` (filter `thumbnails`) ou le thumbnail retourné par `edit-design` (~335-340px de large), recadrer au ratio 2:3 si besoin, puis agrandir en `1024x1536` avec `PIL` (`Image.LANCZOS` + `ImageFilter.UnsharpMask(radius=2, percent=120, threshold=2)` pour compenser le flou de l'agrandissement). Qualité un cran en dessous d'une génération native HF/Claude_image mais utilisable — toujours vérifier par un zoom sur un détail (visage, texte) avant d'intégrer. Si cette limitation réseau est un jour levée, préférer un export direct en pleine résolution.

**Règles à appliquer, quel que soit le connecteur** :

1. **Ne jamais faire générer le texte par l'IA à l'intérieur de l'image.** Un premier essai avec la consigne explicite "no text" a quand même produit du texte incohérent ("Row Slow Deepestharg"). Générer uniquement le visuel (photo + illustration/schéma), sans aucun texte, et laisser le pipeline existant (`dessiner_image()` dans `pins.yml`) poser le texte — rendu fiable et déjà éprouvé, zéro risque de coupure.
2. **Supprimer immédiatement tout ce qui n'est pas exploitable** (texte halluciné, résultat hors-sujet, mauvaise qualité, artefact visible) — ne jamais committer un essai raté dans le dépôt, même temporairement. Un artefact localisé (ex. bloc de pixels aberrant dans un coin) peut parfois être recadré/corrigé plutôt que jeter toute l'image — vérifier au cas par cas.
3. **Rester cohérent avec l'identité visuelle du compte** : photographie éditoriale réaliste, palette bleu nuit/doré chaude, ambiance calme, personnage toujours habillé/cadrage pudique, un éventuel schéma illustratif discret en surimpression (voir `PROMPTS_THEME_IA` dans `pins.yml` pour le ton déjà établi par thème).
4. **Format cible** : `1024x1536` ou équivalent 2:3, sauvegardé en `.jpg` dans `fonds/` avec le prochain numéro disponible, puis répertorié dans `fonds_themes.json` avec le thème correspondant.

## Prompt système SEO pour un futur scénario Make (image → métadonnées via IA)

`prompts/system-prompt-pin-seo.md` contient un prompt système fourni par l'utilisateur, à utiliser dans un module IA d'un scénario Make.com : Make envoie une image + l'URL de destination + la liste des tableaux Pinterest, l'IA analyse l'image et renvoie un JSON (titre, description, mots-clés, hashtags, nom de fichier, texte alt, tableau...) exploitable automatiquement par Make.

**Ce flux est distinct du fonctionnement actuel décrit ci-dessus** : aujourd'hui, `pins.yml` part d'un texte déjà écrit dans `pins.json` et choisit/génère une image en conséquence (texte → image). Le prompt image→métadonnées part au contraire d'une image déjà reçue et fait générer le texte à partir d'elle (image → texte). Les deux logiques ne sont pas encore reliées dans ce dépôt — avant de les connecter (ou de basculer l'un vers l'autre), clarifier avec l'utilisateur si ce nouveau flux doit remplacer `pins.json`, s'y ajouter, ou rester un scénario Make séparé.

## Cohérence du contenu (vérification obligatoire avant d'ajouter un pin)

Le compte est centré sur **le stress, la procrastination et le sommeil**, avec ses thèmes établis (`sommeil`, `systemenerveux`, `fatiguementale`, `alimentation`, `procrastination`, `somatisation`, `blocagemental`, `posturesantistress`, `energie` — voir `TABLEAUX` dans `.github/workflows/pins.yml`, chaque thème a son propre board Pinterest). Le script de publication ne fait **aucun contrôle de pertinence** : il publie tel quel le premier pin non encore publié de `pins.json`, dans l'ordre. Toute la responsabilité de cohérence repose donc sur ce qui est ajouté à la banque.

**Avant d'ajouter un nouveau pin à `pins.json` (texte + `image_prete` le cas échéant), vérifier systématiquement :**

1. **Le texte** (titre, texte_image, description) doit se rattacher clairement à un des thèmes ci-dessus, toujours à travers l'angle stress/mental — pas de contenu générique (recette, déco, organisation domestique...) sans lien explicite avec le sommeil, le stress ou le système nerveux. Exemple déjà rencontré à éviter : un pin "rangez votre frigo" sans lien avec le stress ne convient pas ; "ce que le désordre du frigo dit de ta charge mentale" convient.
   - **Cas particulier du thème `alimentation` (board "Alimentation et stress")** : ce board sert uniquement à montrer comment l'alimentation **diminue le stress**, pas le sommeil ni l'énergie en général (ces angles-là existent déjà via les thèmes `sommeil` et `energie`). Un pin alimentation dont le bénéfice mis en avant est l'endormissement ou l'énergie, sans mention explicite du stress/tension/nervosité, ne va pas sur ce board.
   - **Les recettes/préparations sont autorisées, mais seulement si elles sont explicitement anti-stress ou pensées pour favoriser un sommeil réparateur** — jamais des recettes génériques de gain de temps/organisation sans lien avec le mental (c'est exactement ce qui a été retiré en septembre 2026, voir plus bas). Exemple qui convient : une tisane/recette du soir présentée pour son effet apaisant ou son rôle dans l'endormissement (angle `sommeil`, ou `alimentation` si l'angle mis en avant est la baisse du stress/cortisol). Exemple qui ne convient toujours pas : une recette présentée pour "gagner du temps le matin" ou "varier ses repas", sans aucun lien avec le stress ou le sommeil.
2. **L'image** (`fonds/`, fond généré par IA, ou `image_prete`) doit correspondre au sujet réel du texte, pas seulement au thème détecté automatiquement par mot-clé.
3. **Le thème détecté dépend du premier hashtag de la description** (voir `deviner_theme()` dans `.github/workflows/pins.yml`) — pas seulement de la présence du mot-clé du thème quelque part dans le texte. Toujours placer en premier hashtag celui qui correspond au vrai board visé, même si d'autres hashtags thématiques apparaissent aussi dans la description.
4. En cas de lot d'images/textes reçu en bloc (infographies fournies par l'utilisateur, etc.), trier avant l'ajout : écarter ce qui ne rentre pas dans le périmètre plutôt que tout ajouter par défaut.

Un audit a retiré en septembre 2026 onze pins "recette/organisation cuisine" sans lien avec le stress qui avaient été ajoutés par erreur (dont certains déjà publiés), et recentré le board `alimentation` en réordonnant les hashtags de 5 pins dont le vrai sujet était le sommeil ou l'énergie, pas le stress — voir l'historique Git pour référence.

## Lien de destination (uniquement sur les thèmes liés à la formation)

`LIEN_PAGE` pointe vers la page de capture d'une formation systeme.io dont le contenu ne couvre que **le sommeil et les mécanismes du stress au sens large** (nervosité, tensions physiques, blocages, postures) — pas tous les thèmes du compte. Pour éviter d'envoyer des clics non qualifiés (visiteurs intéressés par un sujet que la formation ne traite pas), le champ `lien` envoyé à Make est vide (`""`) pour les thèmes hors périmètre — voir `THEMES_SANS_LIEN` dans `.github/workflows/pins.yml` et `videos.yml`.

- **Thèmes avec lien** (couverts par la formation) : `sommeil`, `systemenerveux`, `posturesantistress`, `blocagemental`, `somatisation`.
- **Thèmes sans lien** (hors périmètre de la formation, à ce jour) : `alimentation`, `procrastination`, `energie`, `fatiguementale`.

**Incident du 28/09/2026** : le pin "Le trou d'énergie de 11h..." (premier hashtag `#energie`, contenu 100 % petit-déjeuner/alimentation) a été publié avec un lien vers le guide, qui ne traite pourtant pas ce sujet — `energie` n'était pas encore dans `THEMES_SANS_LIEN`. Root cause : le **thème/premier hashtag** ne garantit pas que le **contenu réel** du pin correspond à ce que couvre la formation — un pin peut légitimement parler d'alimentation tout en étant tagué `#energie` en tête pour éviter la restriction du board `alimentation` (règle "Cohérence du contenu" ci-dessus), sans que personne ne revérifie ensuite si ce thème a un lien. `energie` et `fatiguementale` ont été ajoutés à `THEMES_SANS_LIEN` en conséquence, et les CTA "guide gratuit" des pins concernés réécrits (11 pins corrigés le 28/09/2026).

**Conséquence pour la rédaction** : un pin sur un thème sans lien ne doit jamais promettre un contenu à découvrir "dans le guide gratuit" ou inviter à "cliquer sur cette épingle" pour en savoir plus — il n'y a rien derrière. Adapter le CTA de ces pins (ou ne pas en mettre du tout) : fin informative, ou invitation à enregistrer l'épingle sur Pinterest (ça reste possible sans lien de destination), jamais une promesse de contenu accessible par clic. **Avant d'ajouter un pin avec un CTA "guide gratuit", vérifier que son contenu réel (pas seulement son premier hashtag) correspond à ce que la formation couvre vraiment.**

Si le périmètre de la formation change (nouveau module couvrant l'alimentation, la procrastination, l'énergie ou la fatigue mentale, par exemple), mettre à jour `THEMES_SANS_LIEN` dans les deux workflows en conséquence.

## Varier les CTA de fin de description

Ne jamais réutiliser systématiquement la même formule de fin d'un pin à l'autre. Viser une grande diversité de CTA (au minimum une quinzaine de formulations distinctes dans la banque, largement dépassé à ce jour) et ne pas mettre de CTA explicite sur tous les pins — environ un quart des pins doivent se terminer sur une phrase informative plutôt que sur une invitation à l'action, pour que ça reste naturel et ne sonne pas comme un script répété.

## Images fournies en planche (plusieurs visuels dans une seule image)

L'utilisateur envoie parfois une planche composite (grille de 5×2 ou similaire) regroupant plusieurs visuels d'infographie à intégrer comme pins `image_prete`. Avant d'ajouter ce type de contenu à la banque :

1. **Découper chaque visuel individuellement** (crop précis par cellule de la grille).
2. **Retirer une marge intérieure** (10-20 px selon la résolution) sur les bords communs avec la cellule voisine : les planches contiennent souvent un fin liseré/gouttière entre les visuels qui, sans ce retrait, laisse une bordure parasite visible sur le pin final.
3. **Remplir tout le cadre de l'épingle sans aucune bordure noire ou padding** : mettre à l'échelle puis recadrer (jamais scale-to-fit-and-pad) pour obtenir exactement le format cible (1000×1500 comme le reste du compte), quitte à perdre une partie du contenu vertical si le visuel source a un ratio très différent (ces planches produisent souvent des visuels très hauts et étroits, ratio ~1:3.8, bien au-delà du 2:3 visé).
4. **Ancrer le recadrage sur le titre + le début du contenu par défaut**, sauf si le titre/l'information essentielle est visible ailleurs (ex. liste à cocher placée en bas de l'image plutôt qu'en haut, transition avant/après répartie sur toute la hauteur) — dans ce cas, vérifier visuellement où se trouve le texte réellement utile avant de choisir le point d'ancrage, plutôt que d'appliquer un recadrage identique partout.
5. **Vérifier visuellement au moins un échantillon par lot** après recadrage (pas seulement les dimensions en pixels) : un recadrage géométriquement correct peut quand même couper un titre ou une liste au mauvais endroit.

Limite à connaître : certains visuels ont leur texte tronqué **dans le fichier fourni par l'utilisateur lui-même**, avant tout traitement (texte qui déborde du cadre de sa propre cellule dans la planche source) — ce n'est pas corrigible par recadrage, à signaler plutôt qu'à essayer de réparer.

## Stratégie des titres

**Mise à jour du 28/09/2026 basée sur les vraies données Pinterest Analytics** (voir la section "Pinterest Analytics" plus bas et `docs/pinterest-projet/04-journal-decisions.md` section 9) — remplace la recommandation précédente "70% problème/curiosité", qui n'était qu'une hypothèse de bonnes pratiques génériques jamais vérifiée sur ce compte.

- **Jamais le même titre sur plusieurs pins/images.** Pinterest recommande du contenu original et pénalise les doublons répétés — chaque titre ajouté à `pins.json` doit être unique (vérifié régulièrement : aucun doublon à ce jour).
- **Privilégier un titre à chiffre / listicle quand le contenu s'y prête** (ex. *"5 Clés pour Vaincre la Procrastination"*, *"Les 9 signes d'un cortisol élevé"*, *"6 étapes pour débloquer ton mental"*) : c'est le format des 8 pins les plus performants du compte (jusqu'à 286 saves, 22k+ impressions), tous antérieurs à cette session. Le style narratif/question reste valable quand il correspond mieux au contenu, mais le chiffre doit redevenir un réflexe par défaut.
- **Continuer à surveiller Pinterest Analytics** au fil du temps pour affiner cette règle avec plus de données qu'un échantillon de 8 pins.
- **Varier les structures d'ouverture.** Éviter qu'un même gabarit revienne trop souvent d'un titre à l'autre — alterner listicles, questions, heures précises, affirmations directes.

## Descriptions

- **Corps du texte (hors hashtags) visé entre 380 et 450 caractères.** Nettement plus riche qu'une description minimaliste, avec des détails concrets et actionnables plutôt que du remplissage. Toujours vérifier avec `len()` en Python, pas à l'œil.
- **Description totale (corps + hashtags) toujours ≤ 495-500 caractères** (limite Pinterest ; le script de publication tronque automatiquement au-delà, ce qui peut couper une phrase au milieu — mieux vaut écrire directement dans la limite).
- **Mots-clés SEO intégrés naturellement**, jamais en bourrage : 2-3 expressions qu'une personne concernée chercherait réellement sur Pinterest, insérées dans des phrases utiles à lire pour un humain.
- **Structurer avec des puces emoji quand le contenu s'y prête** (📌 👉 •), comme les meilleurs pins historiques du compte — reste optionnel, à juger au cas par cas.
- **Varier les CTA de fin de description.** Ne pas répéter systématiquement "Clique sur cette épingle pour le découvrir" ou la même formule d'un pin à l'autre — alterner impératifs ("Enregistre cette épingle...", "Garde-la sous la main..."), questions, affirmations, et parfois aucun CTA explicite (le texte se termine sur le conseil lui-même).
- **8 à 10 hashtags par pin** (mise à jour du 28/09/2026 — auparavant 5), **dans la limite du plafond de 495-500 caractères ci-dessus**. Les meilleurs pins historiques du compte en utilisent jusqu'à 14 mais dépassent largement ce plafond (642 caractères mesurés sur un exemple) — voir la note dans `docs/pinterest-projet/03-regles-editoriales.md` section 7 avant d'envisager de lever cette limite. **Le premier hashtag reste le seul mécanisme de routage vers un board Pinterest** (voir `deviner_theme()` dans `.github/workflows/pins.yml`), inchangé — les hashtags ajoutés viennent après, plus génériques (`#bienetre`, `#developpementpersonnel`, `#selfcare`...). Ne jamais modifier le premier hashtag en même temps qu'on retravaille le corps du texte, sauf intention explicite de changer le board cible.

## Pinterest Analytics (accès en lecture depuis le 28/09/2026)

Un connecteur Composio (toolkit `pinterest`) donne un accès en lecture aux vraies statistiques du compte (analytics, top pins, boards, profil) — connexion OAuth établie le 28/09/2026, à ne pas confondre avec le webhook Make.com (publication uniquement, aucune lecture). Voir `docs/pinterest-projet/01-architecture-technique.md` pour le détail des outils disponibles (`PINTEREST_GET_ACCOUNT_ANALYTICS`, `PINTEREST_GET_TOP_PINS`, `PINTEREST_LIST_BOARDS`, `PINTEREST_GET_PIN`...) et `04-journal-decisions.md` section 9 pour le diagnostic complet réalisé ce jour-là. Cet accès n'a **aucun droit d'écriture** — impossible de supprimer/modifier un pin déjà publié depuis cet environnement, ça reste une action manuelle utilisateur dans l'app Pinterest.

## Déclenchement (cron-job.org)

Le workflow n'a plus de programmation automatique intégrée (`schedule` a été retiré du fichier `.github/workflows/pins.yml` pour éviter les retards/oublis de GitHub). À la place, un compte gratuit sur [cron-job.org](https://cron-job.org) appelle l'API GitHub 7 fois par jour pour lancer le workflow. Configuration :

1. Crée un **token GitHub** dédié : sur GitHub, **Settings** (ton profil, pas le dépôt) → **Developer settings** → **Personal access tokens** → **Fine-grained tokens** → **Generate new token**. Limite-le au dépôt `pins-clarte` uniquement, et donne-lui la permission **Actions : Read and write** (rien d'autre). Copie le token une fois généré (il ne sera plus jamais affiché).
2. Crée un cronjob sur cron-job.org, avec :
   - **URL** : `https://api.github.com/repos/yacinenettour-cyber/pins-clarte/actions/workflows/pins.yml/dispatches`
   - **Méthode** : `POST`
   - **En-têtes (headers)** :
     - `Authorization: Bearer TON_TOKEN`
     - `Accept: application/vnd.github+json`
     - `Content-Type: application/json`
   - **Corps de la requête (body)** : `{"ref":"main"}`
   - **Planning** : tous les jours à 6h07, 8h07, 10h07, 12h07, 14h07, 16h07 et 18h07, **en UTC** (bien vérifier le fuseau horaire choisi sur cron-job.org).

Le token ne doit jamais être collé ailleurs que dans le champ "headers" de cron-job.org.

## Secrets GitHub requis

Dans **Settings → Secrets and variables → Actions** de ce dépôt :

- `MAKE_WEBHOOK_URL` : l'URL du webhook du scénario Make.com (pins classiques, image)
- `MAKE_WEBHOOK_URL_VIDEO` : l'URL du webhook d'un **second** scénario Make.com, dédié aux Video Pins — voir section **Video Pins** ci-dessous
- `LIEN_PAGE` : le lien vers lequel chaque pin doit renvoyer
- `OPENAI_API_KEY` *(optionnel)* : voir section **Génération de fonds par IA** ci-dessous

## Ajouter des images de fond

Dépose n'importe quelle image `.png` / `.jpg` / `.jpeg` dans le dossier `fonds/`. Sans image dans ce dossier, un fond dégradé nuit étoilée est généré automatiquement.

Pour que l'image reste cohérente avec le texte du pin, ajoute aussi une ligne dans `fonds_themes.json` du type `"fond-101.jpg": "sommeil"` (thèmes possibles : `sommeil`, `systemenerveux`, `fatiguementale`, `alimentation`, `procrastination`, `somatisation`, `energie`, `blocagemental`, `posturesantistress`). Une image non répertoriée dans ce fichier reste utilisable, mais seulement en dernier recours si aucune image du bon thème n'est disponible.

Comme les fonds sont réutilisés par thème (pas globalement), un thème très publié avec peu de photos repasse vite sur les mêmes images. Pour viser un nombre de jours minimum sans répétition sur un thème donné, vise environ `(pins de ce thème par jour) × (jours voulus)` photos dans ce thème.

## Génération de fonds par IA (optionnel)

Si le secret `OPENAI_API_KEY` est renseigné, chaque pin génère automatiquement une photo de fond inédite via l'API OpenAI (`gpt-image-1.5`), adaptée au thème détecté — **plus aucune répétition possible**, la banque `fonds/` devient un simple filet de sécurité (utilisée seulement si la clé est absente ou si l'appel échoue).

- **Coût estimé** : ~0,05 $/image en qualité `medium` (réglable via le secret optionnel `OPENAI_IMAGE_QUALITY` : `low`, `medium` ou `high`), soit environ 0,50 $/jour pour 10 pins → ~15 $/mois. En `low`, environ 4 $/mois.
- **Avant d'activer** : les modèles `gpt-image-*` demandent parfois une vérification d'identité de l'organisation OpenAI (dans les paramètres de ton compte platform.openai.com) avant de fonctionner — si le premier appel échoue, vérifie ça en premier.
- Sans ce secret, rien ne change : le système continue d'utiliser `fonds/` comme aujourd'hui.

## Video Pins (`.github/workflows/videos.yml`)

Un second workflow, séparé du premier, génère des **Video Pins** (format 9:16, 1080×1920) à partir de scripts en plusieurs scènes définis dans `videos.json` — chaque script décrit une suite de beats (image + texte + durée) qui racontent une info concrète (ex. une technique de respiration avec un chiffre précis), pas juste une ambiance. Les images de fond viennent soit de `fonds/`, soit de `videos_fonds/` (assets dédiés aux vidéos, plus grand format).

À chaque exécution : choisit le prochain script non encore publié dans `videos.json` (suivi dans `historique_videos.json`, même logique que `pins.json`/`historique.json`), assemble les scènes avec zoom lent + fondus doux (ffmpeg), incruste le texte, commit la vidéo + une image de couverture dans `videopins/`, puis envoie le tout au webhook `MAKE_WEBHOOK_URL_VIDEO` (secret séparé, plus `LIEN_PAGE`).

**Important : ce workflow utilise un webhook Make.com différent de celui des pins classiques**, exprès — pour que le scénario Make existant (pins quotidiens, mode image) reste inchangé, et que seul le nouveau scénario dédié aux vidéos soit réglé en mode vidéo. Pas besoin de jongler entre les deux réglages.

**Deux étapes manuelles restent nécessaires avant que ça publie vraiment sur Pinterest :**

1. **Dans Make.com**, dupliquer ton scénario Pinterest existant (clic droit dessus → Dupliquer, ou "Créer une copie"), puis sur cette copie : ouvrir son module **Webhook** et créer un **nouveau** webhook dédié (ne pas réutiliser celui des pins classiques) — copie son URL, elle servira pour le secret `MAKE_WEBHOOK_URL_VIDEO`. Ensuite, sur le module **Pinterest** de cette copie, changer le champ **"Type de source"** de "URL de l'image" à **"Vidéo"**, mapper `video_url` sur le nouveau champ vidéo, et garder `image_url` comme image de couverture. Active ce nouveau scénario. Le scénario d'origine (pins classiques) reste tel quel, en mode image, avec son webhook d'origine.
2. **Sur cron-job.org**, ajouter un deuxième cronjob (même méthode que celui de `pins.yml`, voir plus haut) pointant vers `https://api.github.com/repos/yacinenettour-cyber/pins-clarte/actions/workflows/videos.yml/dispatches`, réglé pour se déclencher **tous les jours (7 vidéos par semaine)**, par exemple à 19h37 UTC — à une minute différente des pins (`:07`) pour que les deux robots ne poussent pas dans le dépôt en même temps.

**Ajouter de nouveaux scripts vidéo** : compléter `videos.json` avec un nouvel objet `{id, theme, titre, description, beats}` — `id` doit être unique (sert au suivi anti-répétition), et chaque beat a `image` (chemin dans le dépôt), `texte` (max 2 lignes courtes) et `duree` (secondes). À 7 vidéos par semaine, la banque (30 scripts au départ) tient environ 4 semaines. Sans nouveaux scripts, la banque s'épuise — prévoir d'en ajouter régulièrement, comme pour `pins.json`.

## Lancer un test manuel

- Pins classiques : onglet **Actions** → workflow **Pins Pinterest** → bouton **Run workflow** → choisir **test** dans le menu **Mode**.
- Video Pins : onglet **Actions** → workflow **Pins Pinterest - Videos** → bouton **Run workflow** → choisir **test** dans le menu **Mode**.

En mode **test**, le script s'arrête juste après avoir généré l'image/la vidéo (visible dans les logs), sans rien publier sur Pinterest ni consommer de pin/script dans la banque — utile pour vérifier qu'une modification du code fonctionne sans gâcher un vrai pin. Le mode **publier** (par défaut) fait une vraie publication, exactement comme le déclenchement automatique de cron-job.org, qui n'envoie pas d'inputs et reste donc toujours en mode publier.
