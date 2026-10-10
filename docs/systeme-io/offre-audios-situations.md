# Offre après achat : pack « Audios par situation » (projet, 10/10/2026)

Idée de l'utilisateur (10/10/2026) : proposer une offre à 67 € juste après l'achat de la formation « Quand le cerveau refuse de dormir » (37 €). Contenu choisi : **des audios guidés par situation, enregistrés avec la voix de l'utilisateur**. État : **projet, rien n'est en vente**. À la date du 10/10, la formation n'a encore aucune vente : cette offre ne rapportera qu'après les premières ventes à 37 €.

## Règles à respecter

- **Contenu réel et différent de la formation.** La formation contient déjà un audio par module et l'audio express de 3 minutes. Le pack apporte autre chose : un audio pour **un moment précis**, à écouter **pendant** ce moment, sans rien lire.
- **Aucune promesse de soin.** L'auteur n'est pas professionnel de santé : outils de bien-être, jamais « thérapie », « traitement » ni « guérir ». Chaque audio reprend uniquement des techniques déjà sourcées sur le site (colonne « Base » ci-dessous).
- **Sécurité.** Dans la fiche du pack et dans l'audio « crise d'angoisse » : en cas de douleur dans la poitrine, de malaise ou de pensées suicidaires, appeler le 15, le 112 ou le 3114. Rappel « Quand consulter » dans la fiche du pack.
- **Gratuit uniquement.** Enregistrement avec un téléphone (dans un placard rempli de vêtements ou sous une couette, pour étouffer l'écho), montage et fond musical faits avec les outils gratuits du dépôt (`site/outils/audios_respiration.py` sait déjà mélanger musique et bols chantants libres de droits ; la musique « Deep Relaxation » demande un crédit visible).

## Les 12 audios proposés

| N° | Titre | Le moment | Durée | Ce qu'on y fait | Base (sources déjà utilisées sur le site) |
|---|---|---|---|---|---|
| 1 | Réveillé en pleine nuit | Réveil à 3 ou 4 h, impossible de se rendormir | 9 min | Ne pas regarder l'heure, respiration 4-6, images mentales, se lever si l'éveil dure | Tang 2007 (horloge), Harvey & Payne 2002 (images), INSV (se lever après 20 min) |
| 2 | Quand l'angoisse monte au lit | Cœur qui bat, peur qui monte au coucher | 8 min | Rappel que la vague redescend, respiration lente par le ventre, ancrage 5-4-3-2-1 | Assurance maladie (trouble panique), URMC (5-4-3-2-1) |
| 3 | Le sas en rentrant du travail | En arrivant chez soi, encore « en mode travail » | 6 min | Respiration, relâcher les épaules, liste des tâches de demain posée par écrit | Scullin 2018 (liste de tâches), Balban 2023 (respiration) |
| 4 | Après une dispute | Soirée tendue, colère ou tristesse qui reste | 8 min | Respiration lente, nommer l'émotion, relâchement musculaire | Muhammad Khir 2024 (relaxation musculaire), Balban 2023 |
| 5 | La veille d'un grand jour | Examen, entretien, rendez-vous important | 10 min | Rendez-vous des soucis guidé, plan en 3 lignes, respiration 4-6 | Carney & Waters 2006, Balban 2023 |
| 6 | Le dimanche soir | L'anxiété de la semaine qui arrive | 8 min | Écrire la première action de lundi, lâcher le reste, respiration | Scullin 2018, Carney & Waters 2006 |
| 7 | Je n'arrive pas à dormir et ça m'angoisse | La peur de ne pas dormir | 12 min | Arrêter de « vouloir » dormir, attention sur le souffle, images mentales | Harvey 2002 (modèle cognitif), Harvey & Payne 2002 |
| 8 | Rendormir le parent | Après un réveil d'enfant ou un biberon | 5 min | Lumière basse, respiration courte, retour au lit sans relancer la journée | INSV, Réseau Morphée |
| 9 | Dormir après une nuit de travail | Coucher le matin, en horaires décalés | 10 min | Obscurité, calme, relâchement musculaire progressif | INSV, Muhammad Khir 2024 |
| 10 | Le corps crispé | Mâchoire, épaules, ventre tendus le soir | 15 min | Relaxation musculaire progressive complète | Muhammad Khir 2024 |
| 11 | Le mélange des mots | Pensées qui tournent au lit | 12 min | Mots à partir d'un mot neutre, chaque mot imaginé quelques secondes (guidé à voix lente) | Harvey & Payne 2002 |
| 12 | Le matin après une mauvaise nuit | Réveil fatigué, peur de la journée | 6 min | Lumière du jour, respiration, garder l'heure de lever, pas de rattrapage au lit | Inserm, INSV |

Total : environ 1 h 50 d'écoute.

## Prix

L'utilisateur pense à 67 €. Avis donné le 10/10 (opinion, pas une donnée) : c'est presque le double de la formation, alors que celle-ci contient déjà des audios ; un pack d'audios se vend plus facilement autour de 27 à 37 €. À trancher par l'utilisateur.

## Technique (systeme.io, forfait gratuit)

- Vente proposée comme **étape « upsell en un clic »** ajoutée au tunnel « Page de vente » existant (pas de 4e tunnel : le forfait gratuit en compte 3, tous utilisés).
- **À vérifier dans le compte** (Paramètres → Abonnement) : nombre d'upsells autorisés par le forfait gratuit (sites tiers : 1 upsell et 1 order bump, non confirmé sur la page officielle des tarifs, qui n'affiche ses valeurs qu'avec un navigateur) et nombre de formations (si le pack devient une 2e formation).
- Livraison possible sans 2e formation : audios en téléchargement sur la page de remerciement de l'upsell.
- Conditions générales de vente (`/0f1d6dac`) à compléter : produit, prix, contenu, accès immédiat et renonciation au droit de rétractation pour un contenu numérique, garantie, « TVA non applicable, article 293 B du CGI ».

## Exemple complet : audio n° 1 « Réveillé en pleine nuit » (≈ 9 min)

Consignes de lecture : voix basse et lente, environ 100 mots par minute. Les indications entre crochets ne se lisent pas.

[Fond musical très bas. Un bol chantant.]

Tu viens de te réveiller, en pleine nuit. Peut-être que ton cœur bat un peu vite, peut-être que tes pensées sont déjà reparties. Ce n'est pas grave. On va simplement laisser la nuit reprendre sa place.

Pour commencer, ne cherche pas à savoir quelle heure il est. Si ton réveil est tourné vers toi, tourne-le vers le mur. Laisse ton téléphone là où il est. L'heure n'a aucune importance pour les dix minutes qui viennent.

[pause 5 s]

Installe-toi sur le dos ou sur le côté, comme tu préfères. Laisse ta tête s'enfoncer un peu plus dans l'oreiller.

[pause 5 s]

On va respirer ensemble, lentement. Inspire par le nez… deux… trois… quatre. Et expire doucement, plus longtemps… deux… trois… quatre… cinq… six.

[pause 3 s]

Encore une fois. Inspire… deux… trois… quatre. Expire… deux… trois… quatre… cinq… six.

[Répéter le compte encore quatre fois, puis :]

Maintenant, tu n'as plus besoin de compter. Garde simplement ce rythme : une inspiration tranquille, une expiration un peu plus longue.

[pause 10 s]

Pose ton attention sur ton front. Laisse-le se détendre, comme si quelqu'un passait doucement la main dessus.

[pause 5 s]

Tes mâchoires. Laisse un petit espace entre tes dents.

[pause 5 s]

Tes épaules. Laisse-les descendre vers le matelas.

[pause 5 s]

Tes mains. Tes bras. Ils deviennent lourds et chauds.

[pause 5 s]

Ton ventre se soulève quand tu inspires, et redescend quand tu expires.

[pause 10 s]

Si une pensée arrive, un souci, une chose à faire demain, tu n'as pas à la chasser. Dis-toi simplement : « je verrai ça demain ». Et reviens à ta respiration.

[pause 10 s]

Maintenant, on va donner à ton esprit autre chose à faire. Imagine un endroit calme que tu aimes. Une plage tôt le matin, un chemin dans la forêt, une cuisine qui sent le pain chaud. Choisis-en un.

[pause 5 s]

Regarde les couleurs autour de toi. Le ciel, la lumière, les ombres.

[pause 8 s]

Écoute les sons de cet endroit. Le vent, l'eau, des oiseaux peut-être.

[pause 8 s]

Sens la température de l'air sur ta peau. Le sol sous tes pieds.

[pause 8 s]

Avance doucement dans cet endroit. Rien ne presse. Chaque pas est plus lent que le précédent.

[pause 15 s]

Si tu sens le sommeil revenir, laisse-le venir. Tu n'as rien à faire.

[pause 15 s]

Et si, malgré tout, tu te sens bien réveillé, tendu, et que le temps te paraît long, tu as le droit de te lever. Va dans une autre pièce, sous une lumière douce, fais quelque chose de calme : lire quelques pages sur papier, écouter une musique tranquille. Et reviens te coucher quand tu sentiras tes yeux devenir lourds. Ce n'est pas un échec : c'est ce qui aide ton lit à rester l'endroit où l'on dort.

[pause 10 s]

Pour l'instant, reste avec ton souffle. Inspire… et expire, un peu plus longtemps.

[pause 15 s]

Je vais me taire maintenant. La musique va continuer encore un peu, puis s'éteindre. Bonne nuit.

[Musique seule 1 min, fondu, un dernier bol.]
