# Style « humain » des articles du site (21/10/2026)

Consigne de l'utilisateur (21/10/2026) : « Regarde tous les articles du site, je veux que tu les humanises plus, que ça
fasse moins IA. » Contexte : un blog a refusé un lien parce que le site « a du contenu généré par l'IA » (prospection,
20/10). Le site reste honnête sur ses outils (page /methode-editoriale/) : il ne s'agit pas de cacher quoi que ce soit,
mais d'écrire mieux, comme une personne qui parle à une autre.

## Ce qui trahit un texte de machine (à faire disparaître)

- Chaque paragraphe bâti pareil : **phrase en gras.** + « Selon une étude de l'Université X, publiée en 20XX dans
  *Revue* (Auteur et al.), … [n] ». Répété dix fois, ça sonne comme un rapport généré.
- Les deux-points partout (« Le résultat : … », « Autrement dit : … ») et les points-virgules en série.
- Les formules toutes faites : « Voici ce que l'on sait », « Autrement dit », « Il est important de noter », « En
  résumé », « Que tu sois… ou… », « Bonne nouvelle : », « Le point clé », « Surtout, ».
- Les listes de trois adjectifs ou de trois idées à chaque phrase, les symétries parfaites (« pas X, mais Y » en boucle).
- Les phrases toutes de la même longueur. Les transitions qui annoncent ce qui suit au lieu de le dire.
- Les tirets cadratins (—) en série.

## Ce qu'on cherche

- Des phrases de longueurs variées : une courte, sèche. Puis une plus longue qui prend le temps d'expliquer.
- Des scènes concrètes et ordinaires au tutoiement, présentées comme des exemples, jamais comme un vécu de l'auteur :
  « Il est 6 h 40, le réveil n'a pas encore sonné et tu penses déjà à la réunion de 10 h. »
- Des questions que le lecteur se pose vraiment, et des réponses franches (« Non, pas forcément. »).
- Des études racontées naturellement, en gardant **université et année** dans le texte et la revue décrite en français (règle du 09/10/2026 adaptée le 21/10 : le nom exact de la revue reste dans la liste des sources), mais avec des
  tournures variées : « En 2006, des chercheurs de l'Université Northwestern, aux États-Unis, ont suivi 156 personnes
  pendant trois jours [4]. », « En 2009, deux chercheurs de l'UCL, à Londres, ont regroupé 147 études dans une revue de
  biologie et de psychologie [5]. »
- Un peu de chaleur et de bon sens, sans familiarité forcée ni humour déplacé (sujet santé).
- Chaque partie commence toujours par une réponse directe (règle GEO), mais formulée comme on la dirait à voix haute.

## Pas d'anglais dans le texte (consigne de l'utilisateur, 21/10/2026 : « Par contre, on a de l'anglais »)

- Dans le corps des articles, plus aucun mot ni titre anglais : le nom anglais d'une revue (*Nature and Science of
  Sleep*, *Journal of…*) est remplacé par une description en français (« une revue scientifique consacrée au
  sommeil », « une revue de médecine du sommeil ») ; le nom exact reste dans la liste des sources, qui ne change pas.
  L'université et l'année restent dans le texte, en français (« l'Université Northwestern, aux États-Unis »,
  « l'University College London » → « l'UCL, à Londres »).
- Les termes anglais (« bedtime procrastination », « hyperarousal », « mindfulness »…) sont remplacés par leur
  équivalent français ; seuls restent les mots passés dans le français courant (stress, burn-out).

## Autres tics de dialogue d'IA à supprimer

« Et si… ? », « Pas de panique », « Bonne nouvelle », « Le hic », « Concrètement », « En clair », « C'est là
qu'intervient… », « Le secret ? », les questions rhétoriques suivies de leur réponse immédiate à répétition, les
séries de trois, les tirets cadratins, les points d'exclamation, les phrases d'annonce (« Voyons… », « Passons à… »),
les conclusions qui résument ce qui vient d'être dit.

## Ce qui ne change JAMAIS

- Aucun fait, chiffre, étude, source, numéro de citation [n] ou lien ajouté, retiré ou modifié dans son sens. Chaque
  phrase sourcée garde sa ou ses citations. Aucune nouvelle affirmation sans source déjà présente.
- Aucun vécu, aucune anecdote, aucun diplôme ni métier attribué à l'auteur (il n'est pas professionnel de santé ; son
  métier n'est jamais cité). Les exemples restent des exemples (« imagine », « par exemple », « peut-être que tu… »).
- Structure : en-tête (front matter) intact, « L'essentiel », titres des parties (on peut les rendre plus naturels,
  mais ils restent des questions ou des titres clairs avec le mot-clé), tableaux (contenu identique, phrasé plus simple
  permis), « Quand consulter ? », questions fréquentes, liste des sources intacte.
- Prudence : aucune promesse, les conseils de consultation et numéros d'urgence identiques.
- Longueur à peu près identique (± 10 %).

## Exercices : une illustration dessinée et un schéma (consignes de l'utilisateur, 22/10/2026)

« Quand tu mets des exercices, faut faire des schémas, faut mettre des schémas aussi, des dessins. » puis « Il faut
mettre des illustrations, je veux dire. » Tout exercice décrit sur le site (page, article, fiche PDF) a donc :

- **une illustration dessinée** d'une personne qui fait l'exercice, dans le style des épingles illustrées du compte
  (aquarelle douce, silhouette vert sauge, pull et pantalon amples, fond crème, aucun texte) : outil gratuit Hugging Face
  uniquement (quota gratuit, rien de payant), image regardée avant usage (pose exacte de la consigne, anatomie correcte,
  personne jamais dénudée, aucun texte), propre à un seul exercice, jamais réutilisée, inscrite dans
  `photos_utilisees_hors_historique.json`, WebP léger, texte alternatif descriptif en français. Si la pose dessinée ne
  correspond pas à la consigne, on regénère ou on adapte la consigne de position, jamais le contenu sourcé ;
- **un schéma du rythme** dessiné en SVG dans le code (`SCHEMAS` de `site/outils/construire.py`, lignes `{{SCHEMA:nom}}`
  ou `{{VISUEL:nom}}` dans le texte d'une page) : mêmes durées et même ordre que la consigne écrite, libellés en
  français, `role="img"` avec un titre accessible, `currentColor` et variables du thème (clair et sombre), lisible en noir
  et blanc (motif et libellé par phase, jamais la couleur seule).

## 2e passe (29/10/2026) : formules répétées d'un article à l'autre

Demande de l'utilisateur : « Analyse tout le site […] fais en sorte que même les logiciels qui détectent l'IA ne
repèrent pas. » Mesure avant/après (script d'audit : tics par 1 000 mots, longueur des phrases, deux-points, gras,
formules) : les tics de vocabulaire étaient déjà rares depuis le 21/10 ; ce qui restait, c'était la répétition **entre
les articles** :

- « En 20XX, une équipe de l'Université X, [pays], a … dans une revue de … » : 52 phrases ouvertes par « En 20XX, »,
  ramenées à 13 ; tournures variées (année au milieu ou en fin, parenthèse « (étude de 2013, parue dans une revue de…) »,
  sujet = l'université), sans rien retirer : université, revue décrite en français et année restent dans le texte.
  Phrases bancales corrigées (« a interrogé 13 000 personnes, dans une revue de médecine respiratoire »).
- Le paragraphe « Le médecin n'est pas ta seule porte d'entrée… » était identique dans 11 articles : une version par
  article, adaptée au sujet, mêmes faits (psychologue en accès direct, TCC en exemple, Mon soutien psy, annuaire).
- Intertitres en série (« Parce que… » ×5 dans Sommeil léger) et puces identiques entre articles variés.
- Accueil : le haut de page parle à la première personne avec le vécu déjà validé (vecu-auteur.md), photo et lien
  « Mon histoire » ; formules publicitaires retirées (« l'anti-stress naturel le plus simple », « Ce que la science
  mesure vraiment »). Méthode éditoriale réécrite à la première personne, gras réduit.

**Limites dites à l'utilisateur** : aucun outil ne peut garantir qu'un détecteur d'IA ne signalera rien (ces
logiciels se trompent souvent, y compris sur des textes écrits à la main) ; pas d'astuces destinées à tromper les
détecteurs (fautes volontaires, caractères invisibles, synonymes au hasard) : elles abîment la lecture et le
référencement. La page /methode-editoriale/ continue de dire que des outils d'IA aident à la recherche et à la
rédaction. Le seul vrai levier restant : du vécu réel de l'auteur, qu'on ne peut pas inventer.
