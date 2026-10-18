# Tâches automatiques indépendantes : à créer dans claude.ai

> **Abandonné le 18/10/2026** à la demande de l'utilisateur (« On laisse tomber cela ») : rien n'a été créé. Fichier gardé pour mémoire, au cas où.

**Pourquoi** (18/10/2026, journal section 71) : les tâches programmées actuelles sont rattachées à la conversation « Analyse compte Pinterest ». Elles ne tournent que lorsque cette conversation est active. Du 15 au 18/10, rien ne s'est fait : ni article, ni e-mail, ni épingle illustrée. Une tâche créée depuis la conversation, avec une nouvelle session à chaque passage, démarre **sans le dépôt et sans connecteur** (test du 18/10). Il faut donc créer les tâches depuis l'interface de claude.ai, qui permet de choisir le dépôt et les connecteurs.

## Comment faire (une fois par tâche)

1. Ouvre **claude.ai/code** (ou l'app Claude, onglet Code), puis la page des **tâches programmées** (*Routines* / *Scheduled tasks*), puis **Nouvelle tâche**.
2. **Dépôt** : `yacinenettour-cyber/pins-clarte`, branche `main`.
3. **Environnement** : le même que d'habitude (celui de la conversation « Analyse compte Pinterest »).
4. **Connecteurs** : coche **Composio**, **Firecrawl**, **Hugging Face Images** et **Unsplash**.
5. **Horaire** : celui indiqué ci-dessous (heure de Paris).
6. **Consigne** : copie le bloc de texte de la tâche, en entier.
7. **Notifications** : active-les si tu veux un résumé sur ton téléphone après chaque passage.

Quand les 4 tâches sont créées, dis-le dans la conversation : l'ancienne version de chacune sera désactivée, pour éviter les doublons.

---

## 1. Prospection liens — du lundi au vendredi à 9 h 58

```
Tu démarres dans une session neuve : le dépôt yacinenettour-cyber/pins-clarte est cloné dans le dossier de travail. Lis d'abord CLAUDE.md à la racine (règles impératives du projet). Réponds toujours en français.

Prospection quotidienne de liens externes, autorisée par l'utilisateur le 12/10 (« Oui pour l'envoi automatique tous les jours »). Seulement des liens de qualité AVEC DU TRAFIC (« je veux que des liens de qualité avec du trafic » ; journal sections 56 et 58 de docs/pinterest-projet/04-journal-decisions.md).

1) git fetch origin main et se placer sur main à jour. Lire docs/referencement/prospection-liens.json : le champ « regles » et, pour chaque site, le champ « audience ».
2) Lire les réponses Gmail via Composio (GMAIL_FETCH_EMAILS sur les thread_id des statuts envoye/relance, plus les retours mailer-daemon). Le connecteur Gmail de claude.ai répond « Forbidden » : passer par Composio.
   - Mettre à jour le statut : repondu ; stop si refus ou « non merci » ; erreur si l'adresse est rejetée. Noter la réponse.
   - Si une réponse demande une action (question, accord, demande de modification), ne rien répondre seul : résumer et proposer une réponse dans le compte rendu final.
   - Si un lien est annoncé, le vérifier sur la page et noter lien_obtenu.
3) Relance unique, courte et polie, dans le même fil, pour les e-mails envoyés depuis 10 jours ou plus sans réponse. Seulement pour les sites d'audience A ou B ; jamais deux relances.
4) Compléter jusqu'à 5 envois au total ce jour, relances comprises, avec les prospects a_verifier : audience A en priorité, puis B. Jamais un site d'audience C.
   - Nouveau site : mesurer son audience avec le classement Tranco top 1 million (tranco-list.eu).
   - Vérifier sur le site lui-même (curl, au besoin via l'atelier Composio si le réseau bloque) que la page existe, que le site est actif et que l'adresse e-mail y est affichée ; sinon statut formulaire.
   - Tester les liens sortants de la page visée ; un lien vraiment mort (404, 410, domaine inexistant, confirmé par un second essai) est signalé en premier dans l'e-mail comme un service rendu. Noter les liens cassés dans le registre.
   - E-mail personnalisé (modèle : les envois du 18/10 dans le registre) : citer la page réellement lue ; proposer 1 ou 2 pages existantes de www.contactapaisement-mental.fr ; dire « Je ne suis pas professionnel de santé » SANS JAMAIS citer le métier de l'auteur ; rien de payant ; aucun vécu inventé ; signé Yacine ; PS « non merci ». Envoyer avec GMAIL_SEND_EMAIL, include_signature false, puis vérifier dans les Envoyés.
5) Committer le registre (message en français) et pousser sur main (git fetch + merge origin/main avant de pousser).
6) Compte rendu final en français, en quelques lignes : réponses reçues, envois faits, liens obtenus, problèmes.

Quand il ne reste plus aucun prospect A ou B à contacter ni de relance à faire, lancer une nouvelle recherche de sites francophones avec un vrai signal d'audience (mêmes critères), et le dire dans le compte rendu.
```

## 2. Article du site — lundi, mercredi et vendredi à 14 h 53

```
Tu démarres dans une session neuve : le dépôt yacinenettour-cyber/pins-clarte est cloné dans le dossier de travail. Lis d'abord CLAUDE.md à la racine (règles impératives du projet). Réponds toujours en français.

Article du site www.contactapaisement-mental.fr : 3 par semaine (lundi, mercredi, vendredi), à la demande de l'utilisateur (journal sections 57, 61, 64 et 70 de docs/pinterest-projet/04-journal-decisions.md).

Règle de sécurité : la qualité passe avant le rythme. Si le sujet du jour n'a pas assez de sources fiables vérifiables, ou s'il recoupe un article existant, ne rien publier ce jour-là, le noter dans la liste et le dire dans le compte rendu. Jamais plus d'un article par jour.

1) git fetch origin main, se placer sur main à jour. Prendre le premier sujet « à écrire » de docs/referencement/articles-a-ecrire.md. Vérifier avec les suggestions Google qu'il n'empiète sur aucun article existant (une seule page par recherche).
2) Écrire l'article dans site/contenu/articles/, sur le modèle de « angoisse-le-soir » et « respiration-pour-dormir » :
   - chaque partie commence par une réponse directe ou une définition ; un tableau comparatif ;
   - toutes les affirmations sourcées ; chaque étude nommée avec son université, sa revue et son année, vérifiée une par une dans PubMed (Firecrawl) ou sur la source officielle ; ne jamais deviner une affiliation ni citer un chiffre non lu dans la source ;
   - une section « Quand consulter ? » et des questions fréquentes ; tutoiement ; aucune promesse ;
   - l'auteur n'est pas professionnel de santé : ne jamais le présenter comme soignant et ne jamais citer son métier ;
   - le guide seulement si le sujet est dans son périmètre réel (CLAUDE.md, règle 4) ;
   - photo gratuite et inédite (Unsplash ou Pexels) : comparer son empreinte aux photos existantes, la réserver dans photos_utilisees_hors_historique.json et l'inscrire dans photos_sources.json (indentation 1, fin de ligne conservées) ;
   - 2 à 4 liens internes vers et depuis les articles proches et la page thème ; ajouter l'article dans docs/referencement/mots-cles.md.
3) python3 site/outils/construire.py ; vérifier : titre ≤ 60 caractères et description 70-160 uniques, 0 lien cassé, validateur W3C, axe-core dans les deux thèmes, affichage à 320 px.
4) site/outils/publier.sh puis IndexNow ; ajouter l'article à ARTICLES_SITE dans .github/workflows/pins.yml (tester avec le harnais) ; marquer le sujet « fait » (compléter la liste s'il reste moins de 8 sujets) ; vérifier la page en ligne ; relier à l'article les épingles non publiées qui traitent vraiment son sujet, puis python3 outils/verifier_banque.py doit afficher 0 doublon.
5) Ajouter une ligne au journal, committer (dont site/outils/dates-contenu.json), pousser sur main (fetch + merge origin/main avant). Compte rendu final en français avec le lien de l'article à faire indexer dans la Search Console.
```

## 3. Épingles illustrées — tous les jours à 6 h 41

```
Tu démarres dans une session neuve : le dépôt yacinenettour-cyber/pins-clarte est cloné dans le dossier de travail. Lis d'abord CLAUDE.md à la racine (règles 1 à 8, ne rien payer). Réponds toujours en français.

Fabrication d'épingles illustrées publiées par le robot (consignes de l'utilisateur du 15/10 : « des épingles avec des exercices utiles, informatifs », « 1 à 2 épingles de ce type par jour », « regarde les épingles qui fonctionnent le mieux et produis des épingles similaires sans copier »). Lire docs/pinterest-projet/meilleures-epingles.md et la section 67 du journal.

1) git fetch origin main, se placer sur main à jour. Compter les épingles "format" in ("exercices", "cles") non publiées dans pins.json (titre absent de historique.json). S'il y en a 4 ou plus, ne rien fabriquer.
2) Sinon, fabriquer 2 épingles : 1 au format exercices (outils/planche_exercices.py) et 1 au format cles (outils/planche_cles.py). Famille et forme d'après le top 20, JAMAIS le sujet d'une épingle publiée : outils/anti_doublons.py (charger_references + est_doublon) puis relecture à la main (historique, titres_en_ligne.json, pins.json, kits). Titre 35-55 caractères, mot-clé en tête. Contenu exact et prudent, aucune promesse médicale.
   - Illustrations : Hugging Face Images, gr1_z_image_turbo_generate (quota gratuit, jamais d'abonnement), une par une, seed 681678, random_seed false ; prompts de la section 67 du journal ; personnage toujours habillé ; regarder chaque image et écarter pose fausse, anatomie ratée, texte. La consigne de chaque exercice décrit exactement l'image. Si le quota s'épuise, s'arrêter et le dire.
   - Regarder l'image finale : aucun texte qui déborde ou chevauche.
   - Entrée en tête de pins.json (indentation 1, sans retour à la ligne final) : titre, texte_image, points_image, description (corps 380-450 caractères, total ≤ 495, premier hashtag = tableau ; postures : #stress puis #travail ; règle 4 du CLAUDE.md), theme, image_prete, format.
   - python3 outils/verifier_banque.py doit afficher 0 doublon.
3) Committer (message en français) et pousser sur main (fetch + merge origin/main avant).
4) Vérifier sur Pinterest (Composio PINTEREST_LIST_PINS) que les épingles illustrées publiées la veille sont en ligne. Compte rendu final en français : titres créés ou raison de ne rien créer, problèmes.
```

## 4. Suivi des positions Google — le vendredi à 11 h 52

```
Tu démarres dans une session neuve : le dépôt yacinenettour-cyber/pins-clarte est cloné dans le dossier de travail. Lis d'abord CLAUDE.md à la racine. Réponds toujours en français.

Suivi hebdomadaire des positions Google du site www.contactapaisement-mental.fr. Objectif de l'utilisateur : être dans les 3 premières pages (positions 1 à 30) sur ses sujets. Voir docs/referencement/mots-cles.md et la section 60 du journal.

1) git fetch origin main, se placer sur main à jour.
2) Search Console via Composio (google_search_console, propriété sc-domain:contactapaisement-mental.fr) : SEARCH_ANALYTICS_QUERY sur 28 jours (query, page, query+page) ; INSPECT_URL sur les pages non indexées au dernier relevé.
3) Pages prioritaires : position moyenne 11 à 40 avec des impressions, ou recherches réelles dont la formulation n'apparaît pas dans la page. Au plus 3 pages : reprendre la formulation exacte cherchée dans un intertitre ou une question fréquente, compléter seulement avec des sources vérifiées, ajouter des liens internes, revoir le titre seulement si le taux de clic est très bas. Ne jamais changer l'adresse d'une page ; ne jamais citer le métier de l'auteur.
4) Pages non indexées plus de 3 semaines après publication : chercher la cause et corriger.
5) Après modification : python3 site/outils/construire.py ; vérifier (W3C, axe-core deux thèmes, 320 px) ; site/outils/publier.sh puis IndexNow.
6) Ajouter une ligne au tableau des relevés de mots-cles.md, committer (dont site/outils/dates-contenu.json) et pousser sur main (fetch + merge origin/main avant).
7) Compte rendu final en français, 4 à 6 lignes : progrès, recherches entrées dans les 3 premières pages, pages améliorées, une seule action utile de l'utilisateur s'il y en a une.
```
