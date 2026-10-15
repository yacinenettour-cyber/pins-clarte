# Formulaires de contact à remplir (prospection de liens)

Préparé le 15/10/2026 pour les 25 prospects au statut `formulaire` de `prospection-liens.json`. Rien n'a été envoyé ni soumis.

**Mode d'emploi**

1. Ouvre le lien du formulaire (ou l'adresse e-mail indiquée quand le site n'a pas de formulaire).
2. Copie le message du bloc gris (tout le bloc, signature et PS compris) et colle-le dans le champ « Message ».
3. Remplis les champs listés (Prénom : Yacine ; Nom : le tien ; e-mail : yacinenettour@gmail.com ; objet donné quand le formulaire en a un ; ne coche jamais l'inscription à une lettre d'information).
4. Valide le captcha s'il y en a un, relis, puis envoie. Au plus 5 envois par jour ouvré (règle du registre).
5. Dis-moi « formulaire envoyé à X » (ou « e-mail envoyé à X ») pour que je mette le registre à jour.

Ordre : audience A d'abord (domaine du top 1 million Tranco), puis B ; à l'intérieur, les pages qui listent déjà des ressources externes ou qui ont un lien cassé passent devant. Les liens cassés ont été testés deux fois (Python puis curl, et pour les domaines disparus une double vérification DNS chez Google et Cloudflare) le 15/10/2026. Les erreurs 403 (sites qui bloquent les robots) et les erreurs de certificat ne sont pas comptées comme liens morts.

Nos pages proposées ont toutes été vérifiées en ligne (code 200) le 15/10/2026. Pour les sites hors de France (Québec, Suisse, Belgique), aucun message ne propose `/ressources-urgence/` (numéros français).

---

## 1. Psycom – Santé Mentale Info (audience A)

- **Audience** : A, psycom.org rang 280 094 (Tranco) ; organisme public national d'information en santé mentale.
- **Formulaire** : https://www.psycom.org/formulaire-de-contact/
- **Page lue** : https://www.psycom.org/sinformer/lauto-support/ce-quon-peut-faire-pour-sa-sante-mentale/ (« S'aider soi-même, des outils pour tous », mise à jour 29/09/2026). Liste d'outils gratuits par thème ; la partie « Avec la relaxation et les exercices de respiration » propose « Le mini-jeu du ballon pour apprendre la respiration profonde » et « L'exercice audio de 8 mn pour une relaxation musculaire progressive ».
- **Liens cassés (404, confirmés deux fois)** :
  - « Mon Agenda du Sommeil Antifatigue » (section sommeil) : https://sanpsy.u-bordeaux.fr/fr/article82/lancement-de-l-application-mon-agenda-du-sommeil-antifatigue
  - « plus facile à comprendre » (Violentomètre, section relations toxiques) : https://www.intimagir-occitanie.org/outils-lcv
- **Champs** : Nom* (le tien), Prénom* Yacine, Adresse email* yacinenettour@gmail.com, Téléphone (facultatif, laisser vide), Objet*, Message*, case « J'accepte la politique de confidentialité »* à cocher. Pas de captcha visible. Ne rien mettre dans un éventuel champ caché « Name ». Réponse annoncée sous 5 jours ouvrés.
- **Objet** : Deux liens morts et une ressource gratuite de respiration

```text
Bonjour,

En lisant votre page « S'aider soi-même, des outils pour tous » (mise à jour le 29/09/2026), j'ai remarqué deux liens qui renvoient aujourd'hui une erreur 404 :
– « Mon Agenda du Sommeil Antifatigue » (partie sommeil) : https://sanpsy.u-bordeaux.fr/fr/article82/lancement-de-l-application-mon-agenda-du-sommeil-antifatigue
– « plus facile à comprendre » (Violentomètre) : https://www.intimagir-occitanie.org/outils-lcv

Je tiens un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) et le site n'a pas encore été relu par un professionnel : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut compléter votre partie « Avec la relaxation et les exercices de respiration » : trois audios de respiration guidée sans voix (3, 5 et 10 minutes, inspiration 4 s, expiration 6 s, repères au bol chantant, transcription écrite), gratuits et sans inscription : https://www.contactapaisement-mental.fr/respiration-guidee/

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 2. Santé Québec – Capitale-Nationale, « Gestion du stress et de l'anxiété » (audience A, Québec)

- **Audience** : A, domaine parent gouv.qc.ca rang 16 860 (Tranco) ; établissement public.
- **Formulaire** : https://www.ciusss-capitalenationale.gouv.qc.ca/a-propos/nous-joindre (bloc « Commentaires, suggestions ou demande d'information » en bas de page). Le site refuse les requêtes automatiques : page et formulaire lus via Firecrawl.
- **Page lue** : https://www.ciusss-capitalenationale.gouv.qc.ca/services/vivre-sante/gestion-stress-anxiete (« Nous avons réunis dans cette page des ressources et des outils qui pourraient vous aider à mieux composer avec le stress et l'anxiété » ; rubriques Lignes d'écoute, Liens utiles, Applications avec RespiRelax+, Prezens, Petit BamBou… ; dernière mise à jour juillet 2025).
- **Liens cassés (confirmés deux fois)** :
  - « Troubles anxieux » (rubrique Liens utiles) : erreur 410 (page supprimée) : https://www.quebec.ca/sante/problemes-de-sante/sante-mentale-maladie-mentale/troubles-anxieux
  - « Top 10 des outils pour gérer l'anxiété chez les jeunes » : erreur 404 : https://www.miditrente.ca/fr/billet/top-10-des-outils-pour-gerer-l-anxiete-chez-les-jeunes
- **Champs** : Courriel (yacinenettour@gmail.com), Commentaire (le message), reCAPTCHA « Je ne suis pas un robot ». Pas de champ nom ni objet.
- **Objet** : (pas de champ objet)

```text
Bonjour,

Sur votre page « Gestion du stress et de l'anxiété » (Vivre en santé), deux liens de la rubrique « Liens utiles » ne fonctionnent plus :
– « Troubles anxieux » (Québec.ca) renvoie une erreur 410, page supprimée : https://www.quebec.ca/sante/problemes-de-sante/sante-mentale-maladie-mentale/troubles-anxieux
– « Top 10 des outils pour gérer l'anxiété chez les jeunes » renvoie une erreur 404 : https://www.miditrente.ca/fr/billet/top-10-des-outils-pour-gerer-l-anxiete-chez-les-jeunes
Pourriez-vous transmettre ce signalement à l'équipe qui tient la page ?

Je tiens en France un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources et se termine par une section « Quand consulter ? ».

Votre rubrique « Applications » cite RespiRelax+ et Prezens. Si cela peut servir, j'ai mis en ligne trois audios de respiration guidée sans voix (3, 5 et 10 minutes, inspiration 4 s, expiration 6 s), gratuits, sans inscription ni application à installer : https://www.contactapaisement-mental.fr/respiration-guidee/

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 3. Université Laval – Mon équilibre UL, page « Ressources » (audience A, Québec)

- **Audience** : A, ulaval.ca rang 11 963 (Tranco).
- **Formulaire** : aucun formulaire propre au programme. **Adresse affichée sur le site** (page d'accueil de Mon équilibre UL) : **monequilibre@ulaval.ca** → envoyer par e-mail. (Le formulaire général https://formulaireweb.ulaval.ca/Ha3Zfr vise les futurs étudiants, à éviter.)
- **Page lue** : https://www.ulaval.ca/mon-equilibre-ul/ressources (« Notre campus compte plusieurs ressources pour vous aider à maintenir ou à adopter de saines habitudes de vie » ; une vingtaine de liens « Site Web », dont une partie sommeil).
- **Lien cassé (domaine inexistant, confirmé par deux résolveurs DNS)** : « Site Web » du **Projet inspirant** (tabagisme et vapotage) : https://www.expandproject.ca/s/?language=fr
- **Champs** : e-mail ; objet ci-dessous.
- **Objet** : Page Ressources : un lien mort (Projet inspirant)

```text
Bonjour,

Sur la page « Ressources » de Mon équilibre UL, le lien « Site Web » du Projet inspirant (tabagisme et vapotage) ne fonctionne plus : le domaine n'existe plus. Adresse actuelle du lien : https://www.expandproject.ca/s/?language=fr

Je tiens en France un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Votre page rappelle que le sommeil est « un pilier fondamental de votre santé ». Si cela peut être utile à vos étudiants, deux outils gratuits, sans inscription, pourraient compléter vos ressources : trois audios de respiration guidée sans voix de 3, 5 et 10 minutes (https://www.contactapaisement-mental.fr/respiration-guidee/), et un minuteur de cohérence cardiaque et de respiration carrée (https://www.contactapaisement-mental.fr/exercices-respiration/).

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 4. Infirmiers.com – article « Troubles du sommeil : les infirmiers de santé au travail en première ligne » (audience A)

- **Audience** : A, infirmiers.com rang 180 995 (Tranco).
- **Formulaire** : https://www.infirmiers.com/contacts. **Adresse affichée sur le site** : redaction@infirmiers.com (indiquée dans les mentions légales pour les données personnelles ; le formulaire reste préférable).
- **Page lue** : https://www.infirmiers.com/profession-ide/troubles-du-sommeil-les-infirmiers-de-sante-au-travail-en-premiere-ligne (24/03/2022 : « Près d'un Français sur trois est concerné par un trouble du sommeil » ; outils de repérage : échelle d'Epworth, questionnaire de Berlin, typologie circadienne).
- **Lien cassé (404, confirmé deux fois)** : « l'échelle d'Epworth » : https://reseau-morphee.fr/wp-content/uploads/dlm_uploads/2016/11/Epworth.pdf
- **Champs** : Prénom* Yacine, Nom* (le tien), Email*, Fonction (choisir « Autre »), Objet de la demande* « Contacter la rédaction », Message*, case « Recevoir une copie du mail » (au choix), reCAPTCHA.
- **Objet** : (liste) Contacter la rédaction

```text
Bonjour,

Dans votre article « Troubles du sommeil : les infirmiers de santé au travail en première ligne », le lien vers « l'échelle d'Epworth » renvoie aujourd'hui une erreur 404 : https://reseau-morphee.fr/wp-content/uploads/dlm_uploads/2016/11/Epworth.pdf
Le Réseau Morphée a sans doute déplacé le fichier.

Je tiens un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut servir aux infirmiers de santé au travail qui reçoivent ces plaintes, une page gratuite fait le point sur les respirations proposées pour s'endormir (4-7-8, respiration carrée, respiration lente) et sur ce qu'en disent les études : https://www.contactapaisement-mental.fr/respiration-pour-dormir/
Elle renvoie vers un médecin en cas d'insomnie qui dure ou de suspicion d'apnées.

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 5. CIUSSS de la Mauricie-et-du-Centre-du-Québec – « Services d'aide en santé mentale jeunesse et adulte » (audience A, Québec)

- **Audience** : A, ciusssmcq.ca rang 395 665 (Tranco).
- **Formulaire** : https://ciusssmcq.ca/formulaires/40/vous-avez-une-question/ (trouvé via « Nous joindre » → « Êtes-vous satisfait ? » → « Question » ; la page « Nous joindre » elle-même n'a pas de formulaire).
- **Page lue** : https://ciusssmcq.ca/soins-et-services/sante-mentale/services-d-aide-en-sante-mentale-jeunesse-et-adulte/ (rubrique « Outils pour prendre soin de sa santé mentale » : Aller mieux à ma façon, MesOutils.ca, Petit BamBou, Namatata… ; renvoi vers une « Boîte à outils - Stress et anxiété »).
- **Liens cassés** : aucun dans le contenu de la page. Dans le pied de page commun du site, le lien « Québec » (http://www.gouv.qc.ca/FR/Pages/Accueil.aspx) vise un nom d'hôte qui n'a plus d'adresse (aucun enregistrement DNS A/AAAA) : signalé en fin de message, à titre secondaire.
- **Champs** : Votre adresse de courriel, Nom (Yacine + ton nom), Téléphone (laisser vide si facultatif), Ville ou secteur (écrire « France (hors territoire) »), Votre question (le message). Vérifier s'il y a un captcha au moment de l'envoi.
- **Objet** : (pas de champ objet)

```text
Bonjour,

Votre page « Services d'aide en santé mentale jeunesse et adulte » propose, dans « Outils pour prendre soin de sa santé mentale », des ressources comme Aller mieux à ma façon, Petit BamBou ou Namatata.

Je tiens en France un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut être utile aux usagers, deux outils gratuits, sans inscription ni application, pourraient compléter cette liste : un minuteur de cohérence cardiaque et de respiration carrée (https://www.contactapaisement-mental.fr/exercices-respiration/), et trois audios de respiration guidée sans voix de 3, 5 et 10 minutes (https://www.contactapaisement-mental.fr/respiration-guidee/).

Au passage : dans le pied de page du site, le lien « Québec » (http://www.gouv.qc.ca/FR/Pages/Accueil.aspx) ne mène plus nulle part.

Et si vous voyez une erreur sur mon site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 6. Université Grenoble Alpes – « Prendre soin de votre santé mentale » (audience A)

- **Audience** : A, univ-grenoble-alpes.fr rang 29 469 (Tranco).
- **Formulaire** : https://etudiant.univ-grenoble-alpes.fr/sante-et-bien-etre/vous-soigner/trouver-un-medecin/a-grenoble-le-service-de-sante-etudiante/contact/ (formulaire du Service de santé étudiante ; les seules adresses visibles sont dpo@ et webmaster@, à ne pas utiliser).
- **Page lue** : https://etudiant.univ-grenoble-alpes.fr/sante-et-bien-etre/prendre-soin-de-votre-sante-mentale/prendre-soin-de-votre-sante-mentale-1354888.kjsp (« des liens utiles pour vous aider » : Cnaé, Nightline, Alpaline, Etu'zen, SISM, Santé Psy Étudiant).
- **Liens cassés** : aucun (Santé Psy Étudiant répond bien ; seule une erreur de certificat dans notre outil de test).
- **Champs** : Votre adresse électronique*, Votre demande* (le message), pièce jointe (rien), « Validation de saisie »* (captcha à recopier). Ne rien mettre dans le champ « pour les robots ».
- **Objet** : (pas de champ objet)

```text
Bonjour,

Votre page « Prendre soin de votre santé mentale » rassemble des liens utiles pour les étudiants (Cnaé, Nightline, Alpaline, Etu'zen, Santé Psy Étudiant). Pourriez-vous transmettre ce message à la personne qui la met à jour ?

Je tiens un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Deux pages gratuites, sans inscription, pourraient compléter vos liens :
– un test d'anxiété en 2 minutes qui reprend le questionnaire GAD-7 mot pour mot ; à partir d'un score de 10, la page conseille d'abord de consulter, et elle ne propose aucun produit au-delà de 15 : https://www.contactapaisement-mental.fr/test-stress-anxiete/
– trois audios de respiration guidée sans voix de 3, 5 et 10 minutes : https://www.contactapaisement-mental.fr/respiration-guidee/

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 7. Ville de Meudon – page « Santé mentale » (audience A)

- **Audience** : A, meudon.fr rang 615 477 (Tranco).
- **Formulaire** : https://www.meudon.fr/contacter-la-mairie/ (formulaire par thèmes chargé par script : choisir un thème proche de « Solidarités / santé » ; les champs exacts n'ont pas pu être lus automatiquement ; captcha hCaptcha ; le site affiche parfois une page anti-robots, réessayer).
- **Page lue** : https://www.meudon.fr/mon-quotidien/solidarites-et-sante/la-sante-mentale/ (« Pas de santé sans santé mentale » ; conseil local de santé mentale ; renvois vers Psycom, Nightline, MyMood, « Mon soutien psy »).
- **Lien cassé (404, confirmé deux fois)** : dans le menu commun du site (pas dans le texte de la page), « Carte des îlots de fraîcheur » : https://atlas-sig.seineouest.fr/portal/apps/webappviewer/index.html?id=27e3bb4febb448db836039f995f3d067
- **Champs** : thème, Prénom Yacine, Nom (le tien), e-mail, message ; le reste selon ce qui s'affiche.
- **Objet** : Page Santé mentale : proposition pour le CLSM

```text
Bonjour,

Pourriez-vous transmettre ce message au service santé ou au conseil local de santé mentale ?

Votre page « Santé mentale » oriente les Meudonnais vers Psycom, Nightline, MyMood et « Mon soutien psy ». Au passage, le lien « Carte des îlots de fraîcheur » du menu du site renvoie une erreur 404 : https://atlas-sig.seineouest.fr/portal/apps/webappviewer/index.html?id=27e3bb4febb448db836039f995f3d067

Je tiens un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut être utile aux habitants, deux pages gratuites, sans inscription, pourraient compléter vos ressources : trois audios de respiration guidée sans voix de 3, 5 et 10 minutes (https://www.contactapaisement-mental.fr/respiration-guidee/), et un test d'anxiété qui reprend le questionnaire GAD-7 et conseille d'abord de consulter à partir d'un score de 10 (https://www.contactapaisement-mental.fr/test-stress-anxiete/).

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 8. Université de Lausanne – « Gérer le stress » (Réussir à l'Unil) (audience A, Suisse)

- **Audience** : A, unil.ch rang 15 229 (Tranco).
- **Formulaire** : aucun ; la page de contact (https://www.unil.ch/unil/fr/home/contact.html) donne des adresses par service. **Adresses affichées sur le site** : **Orientation@unil.ch** (Service d'orientation et carrières, cité sur la page « Gérer le stress ») ; pour signaler une page ou un lien en erreur : refonte-sites@unil.ch. Envoyer à Orientation@unil.ch (éventuellement en copie à refonte-sites@unil.ch).
- **Page lue** : https://www.unil.ch/unil/fr/home/menuinst/etudier/reussir-a-l-unil/gerer-le-stress.html (« Utilisez les méthodes de détente en pratiquant des activités qui engagent physiquement et mentalement comme la relaxation ou la méditation » ; sous-pages « Liens utiles » et « Sélection d'applications »).
- **Liens cassés** : aucun sur la page « Gérer le stress ». Sur la sous-page « Sélection d'applications » (https://www.unil.ch/unil/fr/home/menuinst/etudier/reussir-a-l-unil/selection-dapplications.html), le lien « 30/30 » vise un domaine qui n'existe plus : http://3030.binaryhammer.com (confirmé par deux résolveurs DNS). Le lien « iStudiez Pro » (http://istudentpro.com) répond par une erreur 522 (serveur injoignable) aux deux essais : non compté, mentionné prudemment.
- **Champs** : e-mail.
- **Objet** : Gérer le stress / Sélection d'applications : un lien mort

```text
Bonjour,

Sur la page « Sélection d'applications » de Réussir à l'Unil, le lien « 30/30 » (http://3030.binaryhammer.com) ne fonctionne plus : le domaine n'existe plus. Le lien « iStudiez Pro » (http://istudentpro.com) ne répondait pas non plus lors de mes deux essais.

Je tiens en France un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Votre page « Gérer le stress » conseille les méthodes de détente comme la relaxation. Si cela peut servir aux étudiants, un minuteur gratuit de cohérence cardiaque et de respiration carrée, utilisable sans inscription ni application, pourrait trouver sa place dans vos liens utiles : https://www.contactapaisement-mental.fr/exercices-respiration/
Il existe aussi en version audio guidée, sans voix : https://www.contactapaisement-mental.fr/respiration-guidee/

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 9. Association Française des aidants – « La santé des aidants » (audience A)

- **Audience** : A, aidants.fr rang 606 785 (Tranco).
- **Formulaire** : https://www.aidants.fr/contact/
- **Page lue** : https://www.aidants.fr/vous-etes-professionnel/orienter-aidants/sante-aidants/ (« 29% se sentent anxieux et stressés » ; « 25% déclarent ressentir une fatigue physique et morale », source DREES 2008 ; fiches et dépliant santé pour les professionnels).
- **Liens cassés** : aucun (HelloAsso répond 403 aux robots, pas mort).
- **Champs** (beaucoup d'obligatoires) : Vous êtes* « autre » ; Nom* (le tien) ; Prénom* Yacine ; E-mail* ; Raison sociale* « Site contactapaisement-mental.fr (particulier) » ; Fonction* « Auteur du site » ; Service* « Aucun » ; Téléphone* (obligatoire : ton numéro, ou renoncer) ; Département* (le tien) ; Destinataire* « Autre » ; Message* ; 2 cases RGPD (la 1re obligatoire, la 2de au choix) ; captcha (Turnstile ou reCAPTCHA).
- **Objet** : (pas de champ objet ; destinataire « Autre »)

```text
Bonjour,

Votre page « La santé des aidants » rappelle que 29 % des aidants se sentent anxieux et stressés, et 25 % ressentent une fatigue physique et morale (DREES). Elle propose aux professionnels des fiches et un dépliant santé à remettre aux aidants.

Je tiens un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut être utile aux professionnels qui orientent les aidants, deux pages gratuites, sans inscription, pourraient compléter ces supports : trois audios de respiration guidée sans voix de 3, 5 et 10 minutes, à écouter même avec très peu de temps (https://www.contactapaisement-mental.fr/respiration-guidee/), et une page des numéros d'urgence et lignes d'écoute en France, vérifiés sur les sites officiels (https://www.contactapaisement-mental.fr/ressources-urgence/).

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 10. Fédération Française des Diabétiques – « Quelles astuces pour bien dormir ? » (audience A)

- **Audience** : A, federationdesdiabetiques.org rang 214 168 (Tranco).
- **Formulaire** : https://www.federationdesdiabetiques.org/formulaire-je-contacte-la-federation (trouvé depuis « Je contacte la fédération » ; l'ancienne adresse « contact » du registre ne sert plus).
- **Page lue** : https://www.federationdesdiabetiques.org/diabete/complications/sommeil (« Bien dormir est essentiel pour votre santé et votre diabète » ; conseils préparés avec l'Institut national du sommeil et de la vigilance). Le libellé du lien en bas de page écrit « INVS » au lieu de « INSV » (le lien lui-même fonctionne) : non mentionné dans le message, pour rester bref.
- **Liens cassés** : aucun.
- **Champs** : Civilité (Monsieur), Prénom Yacine, Nom (le tien), Email, Téléphone, Adresse, Code postal, Ville (le formulaire les demande ; les marques d'obligation n'ont pas pu être lues), Objet du message « Vos sites web », Message ; **ne pas cocher** « J'accepte de recevoir les emails » ; reCAPTCHA.
- **Objet** : (liste) Vos sites web

```text
Bonjour,

Votre page « Quelles astuces pour bien dormir ? », préparée avec l'Institut national du sommeil et de la vigilance, rappelle que bien dormir est essentiel pour la santé et l'équilibre du diabète.

Je tiens un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) et je ne traite pas du diabète : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut compléter vos conseils, une page gratuite fait le point sur les respirations proposées pour s'endormir (4-7-8, respiration carrée, respiration lente) et sur ce qu'en disent les études : https://www.contactapaisement-mental.fr/respiration-pour-dormir/
Elle s'accompagne de trois audios de respiration guidée sans voix, gratuits et sans inscription : https://www.contactapaisement-mental.fr/respiration-guidee/
Ces exercices ne remplacent pas les conseils de l'équipe soignante.

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 11. ciao.ch (site d'information des 11-20 ans, Suisse romande) (audience A, Suisse)

- **Audience** : A, ciao.ch rang 649 723 (Tranco).
- **Formulaire** : https://www.ciao.ch/contacter-ciao/
- **Page lue** : https://www.ciao.ch/ (« Un espace où poser tes questions et t'informer anonymement » ; article mis en avant : « La cohérence cardiaque en pratique », https://www.ciao.ch/articles/la-coherence-cardiaque-en-pratique/).
- **Liens cassés** : aucun.
- **Champs** : Sujet* « Contacter les admins ciao.ch » (ou « Donner mon avis »), Courriel*, Message*, Captcha* (texte à recopier). Pas de champ nom : la signature suffit.
- **Objet** : (liste) Contacter les admins ciao.ch

```text
Bonjour,

Votre page d'accueil met en avant l'article « La cohérence cardiaque en pratique », qui présente la cohérence cardiaque comme un outil simple pour s'aider soi-même.

Je tiens en France un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut servir aux jeunes qui lisent cet article, deux outils gratuits, sans inscription ni compte, permettent de pratiquer tout de suite : un minuteur de cohérence cardiaque et de respiration carrée (https://www.contactapaisement-mental.fr/exercices-respiration/), et trois audios de respiration guidée sans voix de 3, 5 et 10 minutes, avec une transcription écrite (https://www.contactapaisement-mental.fr/respiration-guidee/).

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 12. Université de Fribourg – projet Happy? (Uni-Social) (audience A, Suisse)

- **Audience** : A, unifr.ch rang 21 321 (Tranco).
- **Formulaire** : aucun. **Adresse affichée sur le site** (page Uni-Social, https://www.unifr.ch/uni-social/fr/) : **uni-social@unifr.ch** → envoyer par e-mail. (rectorat@unifr.ch figure sur la page de la newsletter, à éviter.)
- **Page lue** : https://www.unifr.ch/uni/de/organisation/leitung/newsletter-interne/artikel/34410/focus-sur-le-bien-etre-a-l-unifr?cat=4 (« Le projet Happy?, développé par Uni-Social, met le bien-être et la santé mentale des étudiant·e·s au cœur de la vie universitaire » ; « 50 % évoquent des difficultés de gestion du stress », « 81 % déclarent ressentir une fatigue fréquente »).
- **Liens cassés** : aucun.
- **Champs** : e-mail.
- **Objet** : Projet Happy? : deux outils gratuits pour le stress et le sommeil

```text
Bonjour,

J'ai lu dans la newsletter interne l'article « Focus sur le bien-être à l'Unifr » : avec le projet Happy?, vous voulez valoriser les ressources existantes, alors que 50 % des étudiant·e·s évoquent des difficultés de gestion du stress et 81 % une fatigue fréquente.

Je tiens en France un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut enrichir les ressources de Happy?, deux outils gratuits, sans inscription : trois audios de respiration guidée sans voix de 3, 5 et 10 minutes (https://www.contactapaisement-mental.fr/respiration-guidee/), et un journal d'humeur, de stress et de sommeil dont les notes restent uniquement dans le navigateur, rien n'est envoyé (https://www.contactapaisement-mental.fr/journal-humeur/).

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 13. RoseUp Association (audience A ; adéquation moyenne, à envoyer en dernier parmi les A)

- **Audience** : A, rose-up.fr rang 344 904 (Tranco).
- **Formulaire** : https://www.rose-up.fr/nous-contacter/
- **Page lue** : https://www.rose-up.fr/ (« S'informer quand on a un cancer, c'est déjà se sentir moins seule » ; article « Reconnaître et soigner la dépression liée au cancer »). La page d'accueil n'a pas de liste de ressources externes.
- **Liens cassés** : aucun.
- **Champs** : Prénom* Yacine, Nom* (le tien), E-mail*, Téléphone* (obligatoire), Sujet (liste : choisir l'option la plus proche d'« Autre »), Message*, case newsletter (**ne pas cocher**), case d'acceptation de la politique de confidentialité*. Ne rien mettre dans le champ caché « Comments ».
- **Objet** : (liste) Autre

```text
Bonjour,

Sur votre site, j'ai lu « S'informer quand on a un cancer, c'est déjà se sentir moins seule », ainsi que votre article sur la dépression liée au cancer, qui rappelle que le stress et les nuits difficiles accompagnent souvent les traitements.

Je tiens un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) et je ne parle pas du cancer ni de ses traitements : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut être utile aux lectrices de la Maison RoseUp, une page propose trois audios de respiration guidée sans voix (3, 5 et 10 minutes, inspiration 4 s, expiration 6 s), gratuits et sans inscription, pour un moment de calme le soir : https://www.contactapaisement-mental.fr/respiration-guidee/
Ce n'est qu'un outil de détente : il ne soigne rien et ne remplace pas l'équipe soignante.

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 14. Fondation Sommeil – fiche « Insomnie » (audience B, Québec)

- **Audience** : B, fondation reconnue ; absent du top 1 million Tranco.
- **Formulaire** : https://fondationsommeil.com/contact/
- **Page lue** : https://fondationsommeil.com/troubles-du-sommeil/insomnie/ (types d'insomnie : initiale, intermittente, de fin de nuit ; section « Lectures recommandées et liens utiles »).
- **Lien cassé (404, confirmé deux fois)** : « Troubles du sommeil Ordre des psychologues du Québec » (section « Lectures recommandées et liens utiles ») : https://www.ordrepsy.qc.ca/-/introduction-troubles-du-sommeil (le site de l'Ordre répond, seule la page a disparu).
- **Champs** : Nom* (Yacine + ton nom), Adresse courriel*, Numéro de téléphone* (obligatoire : ton numéro, ou renoncer), Sujet*, Message, reCAPTCHA.
- **Objet** : Fiche Insomnie : un lien mort dans « Liens utiles »

```text
Bonjour,

Sur votre fiche « Insomnie », dans la section « Lectures recommandées et liens utiles », le lien « Troubles du sommeil – Ordre des psychologues du Québec » renvoie aujourd'hui une erreur 404 : https://www.ordrepsy.qc.ca/-/introduction-troubles-du-sommeil
Le site de l'Ordre fonctionne : la page a sans doute été déplacée.

Je tiens en France un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut être utile à vos lecteurs qui ont du mal à s'endormir (insomnie initiale), une page gratuite fait le point sur les respirations proposées pour s'endormir (4-7-8, respiration carrée, respiration lente) et sur ce qu'en disent les études : https://www.contactapaisement-mental.fr/respiration-pour-dormir/
Elle renvoie vers un professionnel quand l'insomnie dure.

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 15. Être parents en Vendée – dossier « La charge mentale : anticiper la fatigue psychique » (audience B)

- **Audience** : B, site public départemental (CAF et partenaires) ; absent du top 1 million Tranco.
- **Formulaire** : https://www.etreparent85.fr/fr/informations/contact/ (l'adresse ecoledesparents85@gmail.com affichée sur le site concerne l'École des parents : ne pas l'utiliser).
- **Page lue** : https://www.etreparent85.fr/fr/dossiers/aide-a-domicile/ (« Un poids psychologique qui engendre une fatigue physique et psychique qui peut conduire à l'épuisement » ; bibliographie, podcasts, lieux d'écoute : une vingtaine de liens externes).
- **Liens cassés (confirmés deux fois)** :
  - « Charge mentale : qui est plus préoccupé de bébé qui pleure » (podcast) : 404 : https://lilyfacilitelavie.info/charge-mentale-qui-est-plus-preoccupe-de-bebe-qui-pleure/
  - « MSA » (lieux d'écoute) : 404 : https://loire-atlantique-vendee.msa.fr/lfp/action-sociale-44-85
  - « Allo Ecoute Parent » (lieux d'écoute) : domaine inexistant : http://www.ecoute-parent-85.fr/allo-ecoute-parents/
  - (secondaire, bloc « Cela pourrait vous intéresser » en bas de page, logo des centres sociaux : 404 : https://paysdelaloire.centres-sociaux.fr/federation-des-centres-sociaux-de-vendee/centres-sociaux-et-socio-culturels-en-vendee/ ; non repris dans le message)
- **Champs** : Nom (le tien), Prénom Yacine, E-mail*, Téléphone (facultatif), Votre demande* (le message), case RGPD*, captcha à recopier*.
- **Objet** : (pas de champ objet)

```text
Bonjour,

En lisant votre dossier « La charge mentale : anticiper la fatigue psychique », j'ai remarqué trois liens qui ne fonctionnent plus :
– le podcast « Charge mentale : qui est plus préoccupé de bébé qui pleure » (erreur 404) : https://lilyfacilitelavie.info/charge-mentale-qui-est-plus-preoccupe-de-bebe-qui-pleure/
– « MSA » (erreur 404) : https://loire-atlantique-vendee.msa.fr/lfp/action-sociale-44-85
– « Allo Ecoute Parent » (le domaine n'existe plus) : http://www.ecoute-parent-85.fr/allo-ecoute-parents/

Je tiens un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut compléter votre bibliographie, une page gratuite explique la charge mentale (définition, signes qu'elle déborde, pistes concrètes pour l'alléger à la maison comme au travail) : https://www.contactapaisement-mental.fr/charge-mentale/

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 16. Union étudiante du Québec – « Santé psychologique étudiante » (audience B, Québec)

- **Audience** : B, association étudiante nationale ; absent du top 1 million Tranco.
- **Formulaire** : https://unionetudiante.ca/fr/contact
- **Page lue** : https://unionetudiante.ca/fr/sante-psychologique-etudiante (« nous avons regroupé pour vous les enjeux et ressources, sur la santé psychologique étudiante, disponibles au Québec » ; enquête « Sous ta façade », 23 881 répondants ; liens vers les services de chaque université).
- **Liens cassés** : aucun.
- **Champs** : Prénom Yacine, Nom (le tien), Courriel, Numéro de téléphone (facultatif), Message ; reCAPTCHA.
- **Objet** : (pas de champ objet)

```text
Bonjour,

Votre page « Santé psychologique étudiante » regroupe les ressources disponibles au Québec et rappelle les résultats de l'enquête « Sous ta façade » menée auprès de 23 881 membres.

Je tiens en France un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut être utile à la communauté étudiante, deux outils gratuits, sans inscription ni application, pourraient compléter vos ressources pour les périodes d'examens : un minuteur de cohérence cardiaque et de respiration carrée (https://www.contactapaisement-mental.fr/exercices-respiration/), et trois audios de respiration guidée sans voix de 3, 5 et 10 minutes (https://www.contactapaisement-mental.fr/respiration-guidee/). Ils ne remplacent pas les services d'aide des universités que vous listez.

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 17. Avec Nos Proches – « L'univers des aidants » (audience B)

- **Audience** : B, association nationale ; absent du top 1 million Tranco.
- **Formulaire** : https://www.avecnosproches.com/nous-contacter/
- **Page lue** : https://www.avecnosproches.com/lunivers-des-aidants/ (« Être aidant peut avoir un impact sur sa santé physique et psychique » ; ressources nationales : Ma Boussole Aidants, J'aide je m'évalue, Service-Public.fr…).
- **Liens cassés** : aucun (handicap.gouv.fr a répondu 503 une fois : erreur passagère, non comptée).
- **Champs** : Prénom* Yacine, Nom* (le tien), Adresse email*, Téléphone (facultatif), Vous êtes* « Autre », Votre demande* « Autre » (ou « Une information »), Votre message, case politique de confidentialité, reCAPTCHA.
- **Objet** : (listes) Vous êtes : Autre ; Votre demande : Autre

```text
Bonjour,

Votre page « L'univers des aidants » rappelle qu'être aidant peut avoir un impact sur la santé physique et psychique, et oriente vers des ressources nationales comme Ma Boussole Aidants.

Je tiens un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut être utile aux aidants qui vous appellent, deux pages gratuites, sans inscription, pourraient compléter ces ressources : une routine du soir en 7 gestes simples, en version 3, 10 ou 20 minutes selon le temps disponible (https://www.contactapaisement-mental.fr/routine-du-soir-anti-stress/), et trois audios de respiration guidée sans voix de 3, 5 et 10 minutes (https://www.contactapaisement-mental.fr/respiration-guidee/).

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 18. Santépsy.ch – « Liens utiles » (santé mentale et sommeil) (audience B, Suisse)

- **Audience** : B, campagne publique des cantons romands ; absent du top 1 million Tranco.
- **Formulaire** : https://santepsy.ch/contact/
- **Page lue** : https://santepsy.ch/sante-mentale-et-sommeil/liens-utiles/ (ressources générales : annuaire des spécialistes du sommeil, ligues pulmonaires cantonales, centres du sommeil des hôpitaux romands). Liste surtout institutionnelle et suisse : ajout peu probable.
- **Liens cassés** : aucun (les ligues pulmonaires répondent 403 aux robots, pas mortes).
- **Champs** : Nom* (le tien), Prénom* Yacine, E-mail*, Téléphone (facultatif), Canton* « Autre », Message*, case politique de confidentialité*, reCAPTCHA.
- **Objet** : (pas de champ objet)

```text
Bonjour,

Votre page « Liens utiles » de la rubrique Santé mentale et sommeil oriente vers les spécialistes du sommeil, les ligues pulmonaires et les centres du sommeil des hôpitaux romands.

Je tiens en France un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut compléter vos ressources générales, deux pages gratuites, sans inscription, s'adressent aux personnes dont les pensées tournent au coucher : six techniques étudiées contre les ruminations du soir, avec les cas où il faut consulter (https://www.contactapaisement-mental.fr/ruminations-le-soir/), et trois audios de respiration guidée sans voix de 3, 5 et 10 minutes (https://www.contactapaisement-mental.fr/respiration-guidee/).

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 19. Nouveau Souffle – « Aidant épuisé : que faire quand on n'en peut plus ? » (audience B)

- **Audience** : B, plateforme nationale reconnue par la CNSA ; absent du top 1 million Tranco.
- **Formulaire** : https://nouveausouffle-asso.com/contact/ (aucune adresse e-mail générale sur le site).
- **Page lue** : https://nouveausouffle-asso.com/contenu/aidant-epuise-que-faire-quand-on-nen-peut-plus/ (vidéo : « 1er conseil : mettez vous d'abord en mode survie (exercice de respiration selon la méthode Vittoz) » ; la transcription suggère « une application à télécharger gratuitement […] comme par exemple Respirelax »).
- **Liens cassés** : aucun.
- **Champs** : Nom (Yacine + ton nom), Adresse e-mail, « Je suis… » « Autre », Numéro de téléphone (facultatif), Message ; reCAPTCHA. Ne pas remplir le champ d'inscription à la lettre d'information.
- **Objet** : (pas de champ objet)

```text
Bonjour,

Dans votre vidéo « Aidant épuisé : que faire quand on n'en peut plus ? », le premier conseil est un exercice de respiration, et la transcription suggère de s'aider d'une application gratuite comme Respirelax.

Je tiens un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Pour les aidants qui n'ont ni le temps ni l'envie d'installer une application, une page propose trois audios de respiration guidée sans voix (3, 5 et 10 minutes, inspiration 4 s, expiration 6 s, repères au bol chantant), gratuits, sans inscription, à écouter directement dans le navigateur : https://www.contactapaisement-mental.fr/respiration-guidee/
Si cela vous semble utile, il pourrait trouver sa place à côté de cette suggestion.

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 20. Univers Santé (asbl de l'UCLouvain) – pack blocus (audience B, Belgique)

- **Audience** : B, association reconnue ; absent du top 1 million Tranco.
- **Formulaire** : https://www.univers-sante.be/contact/ (trouvé sur le site ; le registre n'en avait pas). **Adresse affichée sur le site** : univers-sante@uclouvain.be.
- **Page lue** : l'adresse du registre (https://www.univers-sante.be/pack-blocus-a-telecharger/) redirige désormais vers https://www.univers-sante.be/plannings-etude/ (« Organiser son étude : plannings à télécharger » : « on va te donner quelques trucs et astuces pour vivre un blocus sans stress » ; le pack blocus est sur https://www.univers-sante.be/outils/). À noter dans le registre.
- **Liens cassés** : aucun dans le texte. En pied de page (logos des partenaires), le lien http://www.cocof.be/ vise un nom d'hôte sans adresse (www.cocof.be n'existe plus dans le DNS ; cocof.be redirige vers https://ccf.brussels/). Signalé en fin de message.
- **Champs** : Nom* (le tien), Prénom* Yacine, E-mail*, Téléphone (facultatif), Sujet*, Message ; reCAPTCHA. Ne pas remplir le champ de lettre d'information.
- **Objet** : Blocus sans stress : deux outils de respiration gratuits

```text
Bonjour,

Votre page « Organiser son étude : plannings à télécharger » promet des « trucs et astuces pour vivre un blocus sans stress », avec le pack blocus à télécharger.

Je tiens en France un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut servir aux étudiant·e·s pendant leurs pauses, deux outils gratuits, sans inscription ni application, pourraient compléter le pack : un minuteur de cohérence cardiaque et de respiration carrée (https://www.contactapaisement-mental.fr/exercices-respiration/), et trois audios de respiration guidée sans voix de 3, 5 et 10 minutes (https://www.contactapaisement-mental.fr/respiration-guidee/).

Au passage : en bas de vos pages, le logo de la COCOF renvoie vers http://www.cocof.be/, une adresse qui ne répond plus (le site semble être devenu https://ccf.brussels/).

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 21. PSSM France (Premiers secours en santé mentale) (audience B)

- **Audience** : B, association nationale reconnue ; absent du top 1 million Tranco.
- **Formulaire** : https://www.pssmfrance.fr/contact/ (trouvé sur le site ; le registre n'en avait pas).
- **Page lue** : https://www.pssmfrance.fr/ (« Avoir une conversation peut tout changer. Sauriez-vous quoi dire ? » ; formation qui donne « les connaissances, les compétences et la confiance nécessaires pour soutenir un ami, un membre de la famille ou un collègue »).
- **Liens cassés** : aucun.
- **Champs** : Nom* (le tien), Prénom* Yacine, Entreprise (facultatif, vide), Email*, Téléphone* (obligatoire : ton numéro, ou renoncer), Objet* (aucune option ne correspond vraiment : prendre « Les contenus pédagogiques ou les projets de recherches scientifiques »), Message*, case de traitement des données*. Ne rien mettre dans le champ « Si vous êtes un humain, ne remplissez pas ce champ ».
- **Objet** : (liste) Les contenus pédagogiques ou les projets de recherches scientifiques

```text
Bonjour,

Votre page d'accueil le dit bien : « Avoir une conversation peut tout changer. » Après la formation, les secouristes en santé mentale ont souvent besoin de savoir vers qui orienter la personne qu'ils soutiennent.

Je tiens un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut être utile aux secouristes, deux pages gratuites, sans inscription : les numéros d'urgence et lignes d'écoute en France (15, 112, 114, 3114…), vérifiés sur les sites officiels (https://www.contactapaisement-mental.fr/ressources-urgence/), et un test d'anxiété qui reprend le questionnaire GAD-7 mot pour mot ; à partir d'un score de 10, il conseille d'abord de consulter (https://www.contactapaisement-mental.fr/test-stress-anxiete/).

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 22. Minds (promotion de la santé mentale, Genève) – campagne mindsUP (audience B, Suisse)

- **Audience** : B, association reconnue ; absent du top 1 million Tranco.
- **Formulaire** : https://minds-ge.ch/contact (trouvé sur le site). **Adresse affichée sur le site** : contact@minds-ge.ch.
- **Page lue** : https://minds-ge.ch/campagne-mindsup (collecte de fonds pour l'application gratuite mindsUP : « Pas d'abonnement. Pas de pub. Pas de profit. Juste l'envie de rendre la santé mentale accessible »). Page de collecte : peu de chances d'y obtenir un lien ; viser plutôt leurs dossiers.
- **Liens cassés** : aucun.
- **Champs** : Prénom* Yacine, Nom* (le tien), Email*, Téléphone* (obligatoire : ton numéro, ou passer par contact@minds-ge.ch), Message*, case politique de confidentialité*, captcha Cloudflare Turnstile. Ne pas remplir l'inscription à la lettre d'information.
- **Objet** : (pas de champ objet ; par e-mail : « Des outils gratuits de respiration, dans le même esprit que mindsUP »)

```text
Bonjour,

J'ai lu la page de campagne de mindsUP : « Pas d'abonnement. Pas de pub. Pas de profit. Juste l'envie de rendre la santé mentale accessible. » C'est le même esprit que mon petit projet, à une tout autre échelle.

Je tiens en France un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut compléter vos dossiers ou vos ateliers en attendant l'application, une page propose trois audios de respiration guidée sans voix (3, 5 et 10 minutes, inspiration 4 s, expiration 6 s), gratuits, sans inscription, avec une transcription écrite : https://www.contactapaisement-mental.fr/respiration-guidee/
Un minuteur de cohérence cardiaque l'accompagne : https://www.contactapaisement-mental.fr/exercices-respiration/

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 23. Mutualité Française Bretagne – « Réseaux prévention du suicide » (audience B)

- **Audience** : B, page d'un domaine du top Tranco (bretagne.mutualite.fr, rang 246 764) ; trafic propre de la page inconnu.
- **Formulaire** : aucun. La page « Contact » (https://bretagne.mutualite.fr/contact/) affiche des adresses : **accueil@bretagne.mutualite.fr** (accueil général) et, pour la prévention, la coordinatrice régionale **vdiabonda@bretagne.mutualite.fr**. Envoyer à accueil@ (ou à la coordinatrice prévention). Le site bloque les robots : pages lues via Firecrawl.
- **Page lue** : https://bretagne.mutualite.fr/outils/reseaux-prevention-du-suicide/ (« Le mal-être et les pensées suicidaires ne sont pas une fatalité… Vous pouvez trouver de l'aide ! » ; 5 réseaux Misaco ; dépliants « Ne restez pas seul-e » mis à jour le 23/07/2026). La page ne contient que des PDF du site, aucun lien externe ; elle ne parle pas du podcast cité dans le registre.
- **Liens cassés** : aucun.
- **Champs** : e-mail.
- **Objet** : Prévention du suicide : une page de numéros d'urgence vérifiés

```text
Bonjour,

Sur votre page « Réseaux prévention du suicide », j'ai lu : « Le mal-être et les pensées suicidaires ne sont pas une fatalité… Vous pouvez trouver de l'aide ! », avec les dépliants « Ne restez pas seul-e » des collectifs Misaco.

Je tiens un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut être utile aux personnes qui consultent la page ou aux membres des réseaux, j'ai rassemblé sur une page gratuite les numéros d'urgence et les lignes d'écoute en France (15, 112, 114, 3114, lignes anonymes, Mon soutien psy), vérifiés sur les sites officiels et faciles à lire sur téléphone : https://www.contactapaisement-mental.fr/ressources-urgence/
Elle ne remplace évidemment pas vos annuaires locaux.

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## 24. Présanse Pays de la Loire – « Charge de travail, fatigue, stress… Comment j'aide mon équipe ? » (audience B)

- **Audience** : B, fédération régionale des services de santé au travail ; absent du top 1 million Tranco.
- **Formulaire** : https://presanse-paysdelaloire.fr/contact/
- **Page lue** : https://presanse-paysdelaloire.fr/comment-jaide-mon-equipe/ (« Second risque professionnel en France, les risques psychosociaux constituent une problématique majeure en santé au travail » ; « Pour aller plus loin » ne renvoie qu'à des pages du site). Aucun lien externe : chance faible.
- **Liens cassés** : aucun.
- **Champs** : Votre e-mail* + Confirmez votre e-mail*, Vous êtes : « Autre », Nom, Prénom, Entreprise (vide), Téléphone (vide), Département (le tien), Objet de votre message, Votre message*, case de confirmation*, reCAPTCHA. Ne pas remplir le petit formulaire de lettre d'information.
- **Objet** : Deux ressources gratuites sur la charge mentale et le burn-out

```text
Bonjour,

Votre article « Charge de travail, fatigue, stress… Comment j'aide mon équipe ? » rappelle que les risques psychosociaux sont le second risque professionnel en France et que des situations courantes peuvent conduire au burn-out.

Je tiens un site gratuit, sans publicité, sur le stress et le sommeil. Je ne suis pas professionnel de santé (je suis électricien de métier) : chaque article cite ses sources (HAS, OMS, INRS, études publiées) et se termine par une section « Quand consulter ? ».

Si cela peut compléter votre rubrique « Pour aller plus loin », deux pages gratuites, sans inscription : les signes du burn-out (épuisement, cynisme, perte d'efficacité), la différence avec la dépression et qui consulter (https://www.contactapaisement-mental.fr/signes-du-burn-out/), et la charge mentale, avec des pistes concrètes pour l'alléger au travail comme à la maison (https://www.contactapaisement-mental.fr/charge-mentale/).

Et si vous voyez une erreur sur le site, dites-le-moi : je corrige.

Bonne journée,
Yacine
https://www.contactapaisement-mental.fr/

PS : si ce type de message ne vous intéresse pas, répondez simplement « non merci » et je ne vous écrirai plus.
```

---

## Sites sans moyen de contact

- **Essentiel Autonomie (Malakoff Humanis), article « 5 exercices respiratoires de sophrologie pour réduire son stress »** (audience A, rang 292 644) : la page existe (mise à jour le 02/04/2025, liens en bon état), mais **aucun moyen de contact trouvé** pour la rédaction : pas de page contact, pas d'adresse e-mail. Le seul formulaire du site est celui du service AUTONOMIE + (demande d'accompagnement pour une personne en perte d'autonomie, avec date de naissance et code postal du proche) : il n'est pas fait pour ce type de message. Les mentions légales ne donnent que le siège de Malakoff Humanis (21 rue Laffitte, Paris) et dpo@malakoffhumanis.com (données personnelles, à ne pas utiliser). Aucun message rédigé.

## Points à reporter dans le registre (pour la mise à jour)

- Fédération Française des Diabétiques : formulaire trouvé (https://www.federationdesdiabetiques.org/formulaire-je-contacte-la-federation).
- Univers Santé : page cible déplacée vers https://www.univers-sante.be/plannings-etude/ ; formulaire https://www.univers-sante.be/contact/ ; e-mail univers-sante@uclouvain.be.
- PSSM France : formulaire https://www.pssmfrance.fr/contact/. Minds : formulaire https://minds-ge.ch/contact et contact@minds-ge.ch. ciao.ch : https://www.ciao.ch/contacter-ciao/. RoseUp : https://www.rose-up.fr/nous-contacter/.
- Université Laval : monequilibre@ulaval.ca (pas de formulaire). Unifr : uni-social@unifr.ch (pas de formulaire). UNIL : Orientation@unil.ch (pas de formulaire). Mutualité Française Bretagne : accueil@bretagne.mutualite.fr (pas de formulaire).
- CIUSSS MCQ : formulaire https://ciusssmcq.ca/formulaires/40/vous-avez-une-question/.
- Essentiel Autonomie : aucun moyen de contact adapté.
