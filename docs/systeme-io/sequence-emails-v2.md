# Séquence e-mails v2 — « Quand le cerveau refuse de dormir »

Rédigée le 29/09/2026 à partir de la lecture (API systeme.io) de la campagne « Séquence Lead Magnet » (13 e-mails).

**État : appliquée le 29/09/2026 via l'API systeme.io, avec l'accord de l'utilisateur.** Les 10 e-mails remplacent les positions 1 à 10 (mêmes identifiants d'étapes), éditeur classique, envoi à 19h (sauf le 1er : immédiat), expéditeur « Yacine – Clarté Mentale ». Les anciens 11 (Sophie), 12 et 13 ont été désactivés puis **supprimés** le 29/09/2026 à la demande de l'utilisateur (contenu conservé dans `archives/sequence-v1-2026-09-29.json`) : la campagne compte exactement 10 e-mails, tous actifs. L'ancien e-mail d'automatisation « Voici ton guide… » (id 12943008) n'est utilisé par aucune règle ; l'API ne permet pas de le supprimer. Sauvegarde intégrale de la v1 : `archives/sequence-v1-2026-09-29.json`. Relu depuis l'API après écriture : jours J0-1-2-3-4-5-6-8-10-12, aucune mention « minuit », « Sophie », « vidéo ». **Automatisation « Nouvelle vente » impossible** : le forfait gratuit est limité à 1 règle et 1 tag, déjà utilisés par l'inscription au guide. Elle est remplacée par un P.S. « si tu as déjà rejoint le programme, ignore ce message » dans les e-mails 6 à 10. À créer dès le passage à un forfait payant. **Images (29/09/2026)** : une image par e-mail (photos de `fonds/` recadrées, schémas dessinés par script, visuels de la page de vente pour les e-mails 5 et 10), hébergées via jsDelivr épinglé sur le commit `3424ba9` (`medias/emails/`), texte alternatif sur chacune, vérifiées en ligne (HTTP 200). **Reste à faire par l'utilisateur** (impossible sans risque via l'API) : retirer l'image de témoignages de la page de vente, et compresser le PDF du guide.

## 1. Ce qui ne va pas dans la séquence actuelle (vérifié)

**Deux e-mails le même jour — deux fois.** Délais relevés dans systeme.io (délai = jours après l'e-mail précédent) :

| Position | Objet actuel | Délai | Jour d'envoi |
|---|---|---|---|
| 1 | Ton guide « Quand le cerveau refuse de dormir » est prêt 🌙 | 0 | J0 |
| 2 | J'ajoute quelque chose au programme cette semaine | 2 | J2 |
| 3 | Ce que ce programme fait différemment | 1 | J3 |
| 4 | La dernière fois que tu as vraiment bien dormi… | 1 | **J4** |
| 5 | Le bonus disparaît demain à minuit | **0** | **J4** ← même jour que le 4 |
| 6 | Ce soir à minuit, c'est terminé | 2 | **J6** |
| 7 | Ton guide + Une chose importante | **0** | **J6** ← même jour que le 6 |
| 8 → 13 | … | 1-2 | J8 → J16 |

Autres problèmes :
- L'e-mail 6 annonce « c'est mon dernier e-mail sur le sujet », puis 7 autres suivent (dont 4 qui reparlent du programme). Les positions 7 à 13 sont une ancienne séquence restée derrière la nouvelle.
- L'e-mail 7 renvoie le guide comme à un nouvel inscrit, avec un **lien PDF cassé (erreur 403)**.
- Le PDF du guide (e-mail 1) pèse **28 Mo** : long à ouvrir sur mobile, or l'audience Pinterest est surtout sur mobile. Viser moins de 5 Mo (compression PDF).
- La vente commence dès J2, avant d'avoir apporté de la valeur ; les e-mails de valeur (8-9) arrivent après la fin de l'argumentaire.
- **Fausse urgence** : « le bonus disparaît à minuit / sera vendu séparément » est envoyé à chaque inscrit, alors que la page de vente affiche le bonus en permanence (et sous un autre nom : « Audio express 3 min » sur la page, « Protocole des 10 minutes » dans les e-mails). En France, c'est une pratique commerciale trompeuse.
- **Témoignages inventés** : 0 vente à ce jour, donc les avis « Marie, Thomas, Sophie » de la page de vente et l'histoire de Sophie (e-mail 11) ne sont pas de vrais clients. Les faux avis sont interdits (Code de la consommation) et, s'ils sont repérés, détruisent la confiance. À retirer (image « Ce qu'ils ressentent » de la page de vente + e-mail 11).
- Promesses absentes de la page de vente : « vidéos » (e-mail 10), « accompagnement personnalisé, je reste disponible à tout moment » (e-mail 12).
- Aucun texte d'aperçu (preview text) renseigné : c'est la 2e ligne visible dans la boîte mail, elle compte autant que l'objet.
- Trois noms de marque : Clarté Mentale (Pinterest, page de vente), Vivre sans stress (signature), Apaisement Mental (expéditeur).
- Fautes : « Si tu hésite », « ciblént », « personalisé », « desponible ».

## 2. Principes de la v2

- **Un seul e-mail par jour maximum**, jamais deux le même jour.
- **Valeur d'abord** (J0 → J3), présentation du programme ensuite (J4 → J6), puis relances espacées (J8, J10, J12).
- **Zéro fausse urgence, zéro faux témoignage.** Quand on débute, l'honnêteté est un argument : « programme récent, pas encore d'avis, donc garantie 7 jours ».
- **Inviter à répondre** aux e-mails : les réponses améliorent la délivrabilité (moins de spam) et te donnent tes premiers vrais retours.
- Une seule promesse, alignée sur la page de vente : 6 modules, près de 30 leçons courtes, un parcours guidé de 28 soirs, un kit de 7 fiches et des audios guidés ; 37 € en paiement unique, accès à vie, garantie 7 jours (mis à jour le 30/09/2026).
- Signature unique : **Yacine — Clarté Mentale** (même nom que le compte Pinterest et la page de vente). Expéditeur : « Yacine – Clarté Mentale ».

## 3. Calendrier v2 (10 e-mails sur 12 jours)

| # | Jour | Délai à régler | Rôle | Reprend l'actuel |
|---|---|---|---|---|
| 1 | J0 | 0 (immédiat) | Livraison du guide | 1 |
| 2 | J1 | 1 jour | Valeur : le calme instable | 8 |
| 3 | J2 | 1 jour | Valeur : ne pas forcer le sommeil | 10 (sans la vente) |
| 4 | J3 | 1 jour | Transition : pourquoi un guide ne suffit pas | 9 |
| 5 | J4 | 1 jour | Présentation du programme | 12 (corrigé) |
| 6 | J5 | 1 jour | « J'ai déjà tout essayé » | 3 |
| 7 | J6 | 1 jour | Transparence : programme récent + garantie | nouveau |
| 8 | J8 | 2 jours | Émotion : la dernière bonne nuit | 4 |
| 9 | J10 | 2 jours | Rien à forcer | 13 |
| 10 | J12 | 2 jours | Dernier e-mail sur le programme (vrai) | nouveau |

À **désactiver/supprimer** : actuels 2, 5, 6 (fausse urgence), 7 (doublon + lien cassé), 11 (Sophie, témoignage inventé).

Lien de tous les boutons (e-mails 5 à 10 et newsletter 5366813) : **directement la page de paiement** `https://lp.contactapaisement-mental.fr/paiement-anti-stress?productQuantity=1`, choix de l'utilisateur du 29/09/2026 pour limiter les frictions d'achat (les e-mails présentent déjà le programme, le prix et la garantie). Historique : `/accesformation` à l'origine, puis la nouvelle page de vente `/0e9ef918` quelques minutes le 29/09, remis sur le paiement le jour même.

---

## 4. Les 10 e-mails

### E-mail 1 — J0 (immédiat)

**Objet :** Ton guide « Quand le cerveau refuse de dormir » est prêt 🌙
**Aperçu :** Commence par un seul exercice ce soir, pas plus.

Bonjour,

Merci pour ton inscription. Ton guide est prêt :

👉 **[Télécharger le guide]** (lien du PDF)

À l'intérieur : une routine simple pour calmer les ruminations du soir, des exercices pour relâcher la tension, et un calendrier de 30 jours pour installer tout ça sans effort.

Un conseil : n'essaie pas de tout appliquer d'un coup. Ce soir, choisis **un seul exercice**. C'est suffisant pour commencer.

Petite question, si tu as 10 secondes : **qu'est-ce qui t'empêche le plus de dormir en ce moment ?** Les pensées qui tournent, les réveils la nuit, la tension dans le corps ? Réponds simplement à cet e-mail, je lis tous les messages.

Bonne soirée,
Yacine — Clarté Mentale

---

### E-mail 2 — J1

**Objet :** Si le mental s'est agité encore hier soir…
**Aperçu :** Ce n'est pas un échec. Voici pourquoi.

Bonjour,

Peut-être que cette nuit a été plus calme. Ou peut-être que le mental s'est agité à nouveau.

Dans les deux cas, c'est normal.

Quand le stress est installé depuis longtemps, le système nerveux peut se relâcher un soir… puis redevenir agité le lendemain. Ce n'est pas un échec, et ce n'est pas toi qui « fais mal ».

Au début, le calme est souvent instable. Comme un feu qu'on vient d'allumer : il vacille avant de tenir.

L'erreur la plus fréquente, c'est d'essayer de contrôler le sommeil. Se dire « il faut que je dorme » suffit à maintenir le corps en alerte.

Pour ce soir : reprends **une seule étape du guide**, et laisse-la agir sans rien attendre.

À demain,
Yacine — Clarté Mentale

---

### E-mail 3 — J2

**Objet :** Pourquoi forcer le sommeil aggrave tout
**Aperçu :** Le piège dans lequel presque tout le monde tombe.

Bonjour,

Quand le sommeil ne vient pas, le réflexe est presque toujours le même : on essaie plus fort.

« Il faut que je dorme. » « Demain je vais être épuisé. » « Pourquoi mon cerveau ne s'arrête pas ? »

Mais forcer le sommeil envoie au corps un **message de danger**. Le système nerveux comprend : « il y a un problème, reste en alerte ». Et plus le corps reste en alerte, plus le mental s'active.

C'est un cercle très fréquent : la fatigue augmente, la pression monte, le sommeil recule. Ce n'est pas un manque de volonté, c'est une réaction biologique normale.

La sortie n'est pas de forcer le sommeil, mais de **calmer le système nerveux**. Le sommeil suit.

Ce soir, si tu ne dors pas au bout d'un moment : ne lutte pas. Allume une lumière douce, reprends un exercice du guide, et retourne au lit quand la tension baisse.

À demain,
Yacine — Clarté Mentale

---

### E-mail 4 — J3

**Objet :** Pourquoi le calme repart parfois
**Aperçu :** Ce que le guide peut faire… et ce qu'il ne peut pas faire.

Bonjour,

Le guide que tu as reçu est volontairement simple. Il est fait pour ralentir le mental le soir et envoyer au corps un premier signal de sécurité. Pour beaucoup de personnes, ça apporte déjà un vrai soulagement.

Mais il y a une chose importante à comprendre : **un guide seul ne suffit pas toujours à stabiliser le calme.**

Pas parce qu'il est mal fait, ni parce que tu fais mal les choses. Mais parce que le système nerveux a besoin de **répétition, de structure et de continuité**. Un apaisement ponctuel aide ce soir ; sans cadre, le mental reprend souvent le dessus les soirs plus chargés.

C'est pour ça que j'ai construit un programme complet : une structure douce, qui s'applique soir après soir, sans effort.

Demain, je te montre exactement ce qu'il contient, sans détour.

À demain,
Yacine — Clarté Mentale

---

### E-mail 5 — J4

**Objet :** Ce qu'il y a exactement dans le programme
**Aperçu :** Près de 30 leçons courtes, 37 €, et ce que ça change le soir.

Bonjour,

Comme promis, voici ce que contient le programme « Quand le cerveau refuse de dormir » :

- **Apaiser le système nerveux** : respirations anti-stress, soupir physiologique, relâchement musculaire et scan corporel, pour faire redescendre la pression le soir même.
- **Sortir des ruminations sans lutter** : rendez-vous des soucis, liste de demain, mélange cognitif, prendre de la distance avec une pensée.
- **Rituel du soir stabilisant** : préparer le corps (lumière, chaleur, écrans) et ton rituel en 3 versions, 3, 10 ou 20 minutes selon ton énergie.
- **Consolider le sommeil dans le temps** : que faire quand tu te réveilles à 3 h, le matin qui prépare la nuit, et quand en parler à un professionnel.
- **Bien démarrer** : un parcours guidé de 28 soirs (une action par soir, déjà choisie pour toi), ton auto-évaluation et un kit de 7 fiches à imprimer.
- **Et si c'est ton cas ?** : des conseils adaptés si le travail te suit jusqu'au lit, si tu es parent avec des nuits hachées, en horaires décalés, réveillé(e) à 4 h chaque nuit ou dans une période de gros stress.
- **Des audios guidés**, dont l'audio express de 3 minutes pour les soirs de forte pression.

**37 €**, paiement unique. Accès immédiat depuis ton téléphone, accès à vie. Et une **garantie de 7 jours** : si tu ne ressens aucune amélioration, tu es remboursé sans justification.

👉 **[Découvrir le programme]**

Ce n'est pas un traitement médical et ça ne remplace pas l'avis d'un professionnel de santé. C'est une méthode naturelle, à ton rythme.

À demain,
Yacine — Clarté Mentale

---

### E-mail 6 — J5

**Objet :** « J'ai déjà tout essayé »
**Aperçu :** Tisanes, applis, cohérence cardiaque… et pourtant.

Bonjour,

C'est la phrase que j'entends le plus souvent : « J'ai déjà essayé beaucoup de choses. Les tisanes, les applis, la cohérence cardiaque, le sport le soir. Rien ne tient. »

Je comprends cette fatigue.

Ce que j'observe, c'est que la plupart des solutions ciblent les **symptômes** (le mental agité, les pensées en boucle) sans s'occuper de la **cause** : un système nerveux resté bloqué en mode alerte.

Tant qu'on ne s'adresse pas directement à lui, les techniques de surface aident un soir, mais ne stabilisent pas le calme.

C'est ce que le programme fait différemment : il commence par le corps et le système nerveux (module 1), puis seulement les ruminations (module 2), puis il installe un rituel qui tient dans le temps (modules 3 et 4).

👉 **[Voir le programme — 37 €, garantie 7 jours]**

À demain,
Yacine — Clarté Mentale

---

### E-mail 7 — J6

**Objet :** Je préfère être honnête avec toi
**Aperçu :** Pas de faux avis ici. Juste une garantie.

Bonjour,

Je vais être transparent : ce programme est récent. Je n'ai pas encore de témoignages à te montrer, et je préfère te le dire plutôt que d'inventer des avis comme on en voit partout.

C'est justement pour ça que la **garantie de 7 jours** existe. Tu testes le programme chez toi, le soir, à ton rythme. Si tu ne ressens aucune amélioration, même légère, tu m'écris et tu es remboursé. Sans justification, sans discussion.

Le risque est de mon côté, pas du tien.

Et si tu le suis, ton retour m'intéresse vraiment : ce qui t'a aidé, ce qui t'a manqué. C'est comme ça que le programme va s'améliorer.

👉 **[Accéder au programme — 37 €]**

À bientôt,
Yacine — Clarté Mentale

> [Option, uniquement si tu t'engages à le faire] Ajouter : « Pour les premières personnes qui rejoignent le programme, je réponds personnellement à chaque question par e-mail pendant 30 jours. »

---

### E-mail 8 — J8

**Objet :** La dernière fois que tu as vraiment bien dormi…
**Aperçu :** C'était quand ? Ce souvenir est important.

Bonjour,

Une question simple : la dernière fois que tu as vraiment bien dormi, que tu t'es réveillé reposé, sans cette lourdeur dans la tête… c'était quand ?

Il y a longtemps ?

Ce souvenir est important, parce qu'il prouve une chose : **ton corps sait le faire.** Il ne l'a pas oublié. Il est juste bloqué.

Et un système nerveux bloqué, ça se débloque. Pas avec de la volonté, pas en forçant. Avec la bonne approche, répétée régulièrement.

C'est ce que le programme t'apporte, soir après soir.

👉 **[Je veux retrouver ce calme — 37 €]**

Tu mérites de dormir sans te battre.
Yacine — Clarté Mentale

---

### E-mail 9 — J10

**Objet :** Tu n'as rien à forcer
**Aperçu :** Ce qui fait vraiment la différence sur la durée.

Bonjour,

Depuis quelques jours, tu as découvert une autre manière d'aborder tes soirées. Moins de lutte, moins de pression. Un peu plus de calme, parfois fragile, mais réel.

Ce qui fait la différence sur la durée, ce n'est pas une technique isolée. C'est **un cadre simple et rassurant, qui revient chaque soir**.

Si tu sens que le guide seul commence à montrer ses limites, le programme est là, sans pression.

👉 **[Je veux aller plus loin — 37 €, garantie 7 jours]**

Quoi que tu décides, retiens ceci : ton corps sait déjà comment se calmer. Il a juste besoin d'un peu de régularité.

Prends soin de toi,
Yacine — Clarté Mentale

---

### E-mail 10 — J12

**Objet :** Dernier e-mail sur le programme
**Aperçu :** Ensuite, uniquement des conseils gratuits.

Bonjour,

C'est le dernier e-mail où je te parle du programme « Quand le cerveau refuse de dormir ». Ensuite, tu recevras seulement des conseils gratuits sur le sommeil et le stress, de temps en temps.

Pour résumer, si tu hésites encore :
- près de 30 leçons courtes et un parcours guidé de 28 soirs, 5 à 10 minutes par soir, même quand tu es épuisé ;
- 37 €, paiement unique, accès à vie ;
- garantie 7 jours, remboursement sans justification.

👉 **[Rejoindre le programme]**

Et si ce n'est pas le bon moment, c'est très bien aussi. Garde le guide sous la main et reviens-y les soirs difficiles.

Prends soin de toi,
Yacine — Clarté Mentale

---

## 5. Mise en place dans systeme.io (dans cet ordre)

1. **Campagne « Séquence Lead Magnet »** : pour chaque e-mail, régler le délai selon le tableau de la section 3 (aucun délai à 0 sauf l'e-mail 1). Personne n'est en cours de séquence (dernier inscrit le 14/07, séquence finie depuis fin juillet) : modifier sur place est sans risque.
2. Remplacer objet, **texte d'aperçu** et contenu de chaque e-mail ; désactiver ou supprimer les actuels 2, 5, 6, 7 et 11.
3. Expéditeur : « Yacine – Clarté Mentale » sur tous les e-mails.
4. **Automatisation « Nouvelle vente »** (à créer) : déclencheur « Nouvelle vente » sur l'offre à 37 € → action « Ajouter le tag Client » + « Désinscrire de la campagne Séquence Lead Magnet ». Sans ça, un acheteur continue de recevoir les e-mails de vente.
5. **Page de vente** : retirer l'image « Ce qu'ils ressentent » (témoignages) ; renommer le bonus pareil partout ; ajouter un bouton d'achat en haut et en bas de page.
6. Compresser le PDF du guide (< 5 Mo) et remplacer le lien dans l'e-mail 1.
7. S'envoyer un e-mail de test (« Envoyer un test ») pour chacun et cliquer tous les liens.
