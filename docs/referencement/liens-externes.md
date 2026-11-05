# Liens externes (backlinks) : plan gratuit et textes prêts à l'emploi (12/10/2026)

Pourquoi : le site est neuf et traite de santé. Google indexe plus vite et fait davantage confiance à un site
cité par d'autres sites. Aujourd'hui, les seuls liens externes viennent des épingles Pinterest : ils amènent
des visites et aident Google à découvrir les pages, mais ce sont des liens « nofollow » (sans crédit de
référencement).

Règles : rien de payant ; aucun lien acheté, échangé en masse ni posté à la chaîne (Google le sanctionne,
surtout en santé) ; un lien seulement quand il apporte vraiment quelque chose à la personne ; ne jamais
présenter l'auteur comme professionnel de santé (dire qu'il ne l'est pas, sans citer son métier : consigne du 18/10) ; rappeler de consulter un
médecin quand c'est utile.

Ce qui est déjà fait automatiquement : épingles Pinterest vers les articles (3 nouvelles le 12/10, part des
articles relevée), liens internes renforcés, plan du site et robots.txt corrects.

## À faire par l'utilisateur (les seules actions qui demandent ton compte)

Par ordre d'impact, environ 30 minutes au total, une seule fois :

1. ~~**Profil Pinterest → site du profil**~~ : **fait** (vérifié le 21/10 par `PINTEREST_GET_PROFILE` :
   `www.contactapaisement-mental.fr`).
2. ~~**Bing Webmaster Tools**~~ : **fait par l'utilisateur le 25/10/2026** (import depuis la Search Console). Pour mémoire : (3 min, gratuit) : https://www.bing.com/webmasters → « Importer depuis Google
   Search Console ». Le site devient visible dans Bing, DuckDuckGo et les recherches de ChatGPT, et l'envoi
   IndexNow déjà en place y est pris en compte.
3. **Search Console → Demander une indexation** (Inspection de l'URL → « Demander une indexation ») : au 21/10,
   31 pages sur 34 sont indexées. Il ne reste que `/guides-gratuits/`, `/la-formation/` et `/journal-humeur/`
   (journal section 77).
4. **Publier 1 réponse par semaine** parmi celles ci-dessous, sur un forum ou un réseau où la question est
   réellement posée (Quora en français, groupes Facebook sur le sommeil ou le stress) : seulement dans les
   communautés dont le sujet correspond, et jamais deux fois le même texte.
5. **Envoyer le message aux sites ressources** (modèle plus bas) à 2 ou 3 sites par semaine, pas plus.

## Réponses prêtes à publier

Les adapter à la question exacte. Ne jamais les coller telles quelles à plusieurs endroits.

### « Je n'arrive pas à dormir, mon cerveau ne s'arrête pas le soir »

> Ce que tu décris a un nom : les ruminations du soir. Le cerveau profite du calme pour repasser les
> problèmes de la journée. Deux choses ont été testées sérieusement : écrire, avant de te coucher, la liste
> précise de ce que tu as à faire le lendemain (dans une étude de l'université Baylor publiée en 2018, les
> personnes qui le faisaient s'endormaient plus vite), et occuper ton esprit avec une scène calme et détaillée plutôt que
> d'essayer de « ne plus penser ». J'ai rassemblé les études et les gestes ici, avec les signes qui doivent
> amener à consulter : https://www.contactapaisement-mental.fr/ruminations-le-soir/

### « Je me réveille toutes les nuits vers 4 h et je ne me rendors pas »

> En fin de nuit, le sommeil devient naturellement plus léger : c'est le moment où l'on se réveille le plus
> facilement, surtout en période de stress ou après de l'alcool le soir. Sur le moment : ne regarde pas l'heure,
> respire lentement avec une expiration plus longue, et si ça dure, lève-toi faire quelque chose de calme sous
> une lumière douce. Si ça revient au moins trois nuits par semaine depuis plus d'un mois, parles-en à ton
> médecin. Plus de détails ici : https://www.contactapaisement-mental.fr/reveil-4h-du-matin/

### « Le cocktail anti-cortisol, ça marche ? »

> D'après une endocrinologue de la Cleveland Clinic, aucune preuve ne montre que ce mélange (jus d'orange, eau
> de coco, sel) fasse baisser le cortisol. Ce qui a le plus de preuves : un lever à heure fixe, la lumière du
> jour le matin, une activité douce et du temps avec des proches. J'ai fait le tri entre ce qui marche et ce
> qui ne marche pas ici : https://www.contactapaisement-mental.fr/baisser-son-cortisol-naturellement/

### « Comment savoir si je suis en burn-out ? »

> Pour l'OMS, le burn-out repose sur trois dimensions : un épuisement profond, une mise à distance du travail
> et le sentiment de ne plus être efficace. Les signes s'installent souvent sans bruit. Le plus important :
> en parler à ton médecin traitant ou au médecin du travail, ce sont les deux bons interlocuteurs. J'ai
> résumé les repères ici : https://www.contactapaisement-mental.fr/signes-du-burn-out/

## Message aux sites « ressources » (blogs bien-être, associations, pages de liens utiles)

À envoyer uniquement à des sites dont le sujet correspond (sommeil, stress, santé au travail) et qui ont une
page de ressources ou d'outils. Jamais à des sites qui vendent des remèdes miracles.

> Objet : Une ressource gratuite pour votre page « [nom de leur page] »
>
> Bonjour [prénom],
>
> Je lis [nom du site] et votre page « [titre] » m'a été utile. Je tiens un site gratuit, sans publicité,
> sur le stress et le sommeil : chaque article cite ses sources (Inserm, HAS, études publiées) et se termine
> par une section « Quand consulter ? ». J'y ai mis des outils gratuits : des audios de respiration guidée
> sans voix (https://www.contactapaisement-mental.fr/respiration-guidee/), un test de stress et d'anxiété
> basé sur le questionnaire GAD-7 (https://www.contactapaisement-mental.fr/test-stress-anxiete/) et un journal
> d'humeur qui reste dans le navigateur.
>
> Si l'un d'eux peut servir à vos lecteurs, je serais ravi qu'il figure dans votre page. Et si vous voyez une
> erreur sur le site, dites-le-moi, je corrige.
>
> Bonne journée,
> Yacine — www.contactapaisement-mental.fr

## Prospection automatique (depuis le 12/10/2026)

Les e-mails aux sites ressources partent maintenant automatiquement depuis le Gmail de l'utilisateur : au plus 5 par jour ouvré, une relance après 10 jours. Suivi dans `prospection-liens.json` (même dossier), journal section 56. L'utilisateur n'a plus à envoyer le message ci-dessus lui-même.

## Nouvelle approche (29/10/2026) : offrir des ressources réutilisables

Bilan au 29/10 : 44 e-mails envoyés depuis le 12/10, **0 lien obtenu** (9 refus polis, 4 réponses sans lien ;
une blogueuse a refusé un site qu'elle juge « généré par l'IA »). Les institutions ne relient presque jamais un
site personnel tout neuf. Changement de méthode, décidé avec l'utilisateur (« je te laisse choisir le mieux ») :

1. **Page `/ressources-libres/`** : les 3 audios de respiration (CC BY 4.0) et la fiche PDF (CC BY-ND 4.0) sont
   réutilisables librement, à condition de citer la source avec un lien. Texte et code de crédit prêts sur la page.
   Chaque reprise sur un site crée un lien.
2. **Kit de profils** (`kit-profils.md`) : YouTube « À propos », Quora, Reddit, Medium, LinkedIn, page Facebook,
   à faire par l'utilisateur (environ 1 h, une seule fois).
3. **Cibles du message ci-dessous** : personnes qui ont l'usage concret d'un audio ou d'une fiche et un site avec
   une page « ressources » ou « outils » : sophrologues, relaxologues, professeurs de yoga, infirmières scolaires,
   enseignants, animateurs d'ateliers, blogs sur le sommeil. Pas les grandes institutions.

### Message « ressources à réutiliser » (envoyé automatiquement depuis le 29/10/2026, toujours personnalisé)

> Objet : Des audios de respiration gratuits pour vos séances (libres de droits)
>
> Bonjour [prénom],
>
> Je suis tombé sur votre page « [titre] ». Je propose gratuitement trois audios de respiration guidée sans voix
> (3, 5 et 10 minutes, rythme 4-6, bols chantants et musique douce) et une fiche à imprimer de 5 exercices de
> respiration. Vous pouvez les utiliser en séance, en atelier, en classe ou sur votre site, y compris dans un cadre
> professionnel (licence Creative Commons) ; la seule condition est de citer la source avec un lien :
> https://www.contactapaisement-mental.fr/ressources-libres/
>
> J'ai moi-même traversé deux ans de nuits difficiles, et la cohérence cardiaque m'a aidé. Je ne suis pas
> professionnel de santé : les consignes s'appuient sur les études et les sources
> officielles citées sur le site. Si vous y voyez une erreur, dites-le-moi, je corrige.
>
> Bonne journée,
> Yacine — www.contactapaisement-mental.fr

## Style des e-mails : rien ne doit faire IA (consigne de l'utilisateur, 29/10/2026)

« Attention, les emails, quand tu vas envoyer les emails, ça doit pas faire IA. » Chaque e-mail doit se lire comme un
message écrit à la main par Yacine, à une seule personne :

- **Court** : 70 à 130 mots, 3 ou 4 petits paragraphes. Texte brut, sans gras, sans liste à puces, sans emoji, sans
  tiret long (—), sans point d'exclamation en série.
- **Un détail vrai et précis** lu sur leur site dans la première ou la deuxième phrase (le titre d'un article, un
  exercice qu'ils proposent, un atelier), jamais un compliment vague (« votre super contenu »).
- **Vouvoiement simple**, phrases de longueurs variées, mots de tous les jours. Une seule demande, à la fin.
- **Jamais ces formules** : « J'espère que ce message vous trouve bien », « Je me permets de vous contacter »,
  « N'hésitez pas », « Je serais ravi de », « Dans un monde où », « Voici », « En effet », « Par ailleurs »,
  « Ainsi », « Il est essentiel », « véritable », « incontournable », « ressource précieuse », « valeur ajoutée »,
  « synergie », « collaboration gagnant-gagnant », « Bien cordialement » suivi d'un long bloc de signature.
- **Objet** court et banal, comme entre deux personnes : « Vos ateliers de sophrologie », « Une question sur votre page
  sommeil », « Des audios pour vos séances ? ». Jamais de majuscule à chaque mot ni d'accroche marketing.
- **Chaque e-mail est différent** : ne jamais réutiliser la même ouverture ni la même phrase d'un e-mail à l'autre ;
  le modèle ci-dessus donne le fond, pas le texte à recopier.
- **Signature** : « Yacine » seul, puis l'adresse du site sur la ligne suivante. PS « Si ça ne vous intéresse pas, dites-le
  moi simplement et je ne vous écrirai plus. » (cohérent avec la relance unique : un « non » arrête tout) (formulation variée d'un e-mail à l'autre).
- **Avant chaque envoi**, relire le texte en se demandant « est-ce que Yacine écrirait ça ? » et le passer au crible
  de la liste ci-dessus ; en cas de doute, raccourcir.

Exemple du ton visé (à ne pas recopier) :

> Objet : Des audios pour vos séances ?
>
> Bonjour Claire,
>
> J'ai lu votre article sur la respiration avant le coucher, en particulier le passage sur l'expiration plus longue.
> C'est exactement ce que j'essaie de transmettre de mon côté.
>
> J'ai traversé deux ans de nuits difficiles, et la cohérence cardiaque m'a aidé. J'ai fait trois audios de
> respiration 4-6 sans voix (3, 5 et 10 minutes) et une fiche à imprimer. Vous pouvez les utiliser en séance ou sur
> votre site, gratuitement, en citant simplement la source :
> https://www.contactapaisement-mental.fr/ressources-libres/
>
> Je ne suis pas professionnel de santé, donc si vous voyez quelque chose à corriger, ça m'intéresse.
>
> Yacine
> www.contactapaisement-mental.fr
>
> PS : si ce n'est pas pour vous, dites-le moi et je ne vous écrirai plus.

### Plus humain encore (consigne du 01/11/2026 : « Humanise les emails, ça doit pas faire IA »)

Relecture des 6 e-mails du 01/11 : ils suivaient tous le même moule. On y trouvait un article cité, puis le vécu, les
ressources détaillées entre parenthèses, « Je ne suis pas professionnel de santé », la signature et un PS. Le moule se
voyait d'un e-mail à l'autre, et c'est ce qui fait « machine ». À partir de maintenant :

- **Plus court : 40 à 90 mots.** Une personne pressée écrit 4 ou 5 phrases, pas un dossier.
- **Une seule idée par message.** Soit les audios, soit une proposition d'article, jamais les deux. Pas de liste de
  formats ni de durées entre parenthèses (« 3, 5 et 10 minutes », « CC BY 4.0 »). La page du lien le dit.
- **L'ordre change à chaque fois.** Parfois une question pour commencer, parfois le vécu, parfois directement l'article
  lu. Pas toujours de PS. « Je ne suis pas professionnel de santé » (formule imposée, mot pour mot) se glisse dans une
  phrase naturelle (« Je ne suis pas professionnel de santé, juste quelqu'un qui a cherché pendant ses nuits
  blanches ») au lieu d'une ligne seule. Le métier n'est jamais cité.
- **Une réaction vraie à l'article**, comme on en a quand on lit : un passage qui a fait tilt, une question qu'il
  pose. Pas un résumé de l'article.
- **Des mots de tous les jours.** Pas de « ressources libres de droits », « contenus QVCT », « sourcé », « inédit »,
  « lectorat », « pertinent ». On dit « des audios gratuits », « un texte rien que pour vous », « avec les études
  citées ».
- **Phrases imparfaites autorisées** : une phrase courte sans verbe, un « bref », un « du coup », une tournure orale.
  Jamais de fautes d'orthographe.
- **Objet** en minuscules, comme un message entre deux personnes : « votre article du dimanche soir », « une petite
  question ».
- **Relance** : deux phrases au plus, sans rappeler tout le premier message.
- **Avant l'envoi**, relire à voix haute. Si la phrase ne pourrait pas être dite au téléphone, la réécrire.

Exemple (à ne pas recopier) :

> Objet : votre article du dimanche soir
>
> Bonjour,
>
> Le passage sur la gorge serrée le dimanche soir m'a parlé. J'ai eu deux ans de nuits comme ça, par périodes.
>
> Ce qui m'a aidé, c'est de respirer lentement quelques minutes au lit. J'ai mis des audios gratuits en ligne pour
> ça. Si un jour ça peut servir à vos lecteurs, ils sont là : https://www.contactapaisement-mental.fr/ressources-libres/
>
> Je ne suis pas professionnel de santé, alors si votre équipe voit une erreur, ça m'intéresse.
>
> Yacine

## Ce que je surveille

Le bilan du 21/10 regarde aussi les visites venues d'autres sites (Cloudflare Web Analytics, « Referrers »)
pour savoir si ces liens apportent du trafic.

## Articles invités (05/11/2026, accord de l'utilisateur « Ok »)

Bilan au 05/11 : 49 e-mails « ressources » envoyés depuis le 12/10, 8 réponses, **0 lien** (site trop jeune pour les
institutions, aucune contrepartie pour les blogs, un refus « site généré par l'IA », une demande de 50 € refusée).
La tâche du matin (« Prospection liens : articles invités », du lundi au vendredi à 9 h 58, jusqu'à 10 envois)
propose désormais **des articles invités gratuits et inédits** à des blogs francophones qui publient déjà des
contributions extérieures : 2 ou 3 sujets précis, utiles à leur public, sans demande de lien dans le premier
message ; le lien vient dans la présentation de l'auteur une fois l'article accepté. Chaque article accepté est écrit
puis montré à l'utilisateur avant tout envoi (`docs/referencement/articles-invites/<domaine>.md`). Premières pistes :
habitudes-zen.net, leblogdesrapportshumains.fr, coachrelax.fr, secrets-du-sommeil.com, atypiqueworld.com.
Pistes ouvertes suivies : Ma Cohérence (échange proposé le 30/10), Même Plus Peur (relance du 03/11), Phobies-Zéro
(page Références à vérifier à partir du 11/11). Indexation vérifiée le 05/11 (Search Console, inspection page par
page) : 45 pages indexées sur 46, seule `/videos/` « détectée, non indexée ».
