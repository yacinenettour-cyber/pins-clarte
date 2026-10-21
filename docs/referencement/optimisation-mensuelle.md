# Optimisation mensuelle des pages « presque visibles » (depuis le 21/10/2026)

Demande de l'utilisateur (21/10/2026) : « Améliorer chaque mois les articles déjà presque visibles. Google montre ton
site sur certaines recherches, mais en 2e ou 3e page, là où personne ne clique. Chaque mois, je regarde ces recherches
et je retouche l'article concerné pour qu'il réponde exactement à la question. Le but est qu'il remonte en 1re page. »

Complète le suivi hebdomadaire des positions (`mots-cles.md`) : ici, une passe par mois, centrée sur les couples
(requête, page) déjà proches de la 1re page. Gratuit de bout en bout (Search Console, Composio, PubMed).

## Étapes

1. **Données.** Google Search Console via Composio (`COMPOSIO_MULTI_EXECUTE_TOOL`, session_id `"wait"`),
   outil `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY` : `site_url` = `sc-domain:contactapaisement-mental.fr`,
   `dimensions` = `["query", "page"]`, du 1er jour du mois précédent (ou du 09/10/2026 pour la 1re passe) jusqu'à
   hier, `row_limit` 5000.
2. **Sélection.** Garder les couples en **position moyenne de 8 à 40** avec **au moins 2 impressions**. S'il y en a trop
   peu, descendre à 1 impression et le noter dans le tableau. Classer par impressions. Ignorer les requêtes parasites
   (« verifie tout ») et celles qui ne relèvent pas du site.
3. **Lecture.** Au plus 6 pages par passe. Pour chacune, lire l'article et se demander : la requête, telle qu'elle est
   tapée, trouve-t-elle une réponse claire et directe ? Vérifier aussi qu'une passe précédente ne l'a pas déjà traitée
   (tableau ci-dessous) : dans ce cas, attendre un mois de données avant de retoucher.
4. **Retouches, uniquement ce qui sert la requête, sans bourrage :**
   - un intertitre (H2/H3) ou une question fréquente qui reprend la formulation réelle de la requête ;
   - une réponse directe de 1 à 3 phrases en tête de cette partie ;
   - si la requête principale manque à l'en-tête : `titre_seo` (60 caractères maximum) ou `description` (70 à 160),
     uniques sur le site, en gardant le mot-clé principal (`mot_cle`) ;
   - `maj` mis à la date du jour.
5. **Contrôles.** `python3 site/outils/construire.py` ; titres et descriptions uniques ; 0 lien interne cassé ;
   `git diff` relu article par article (aucun fait existant altéré, chaque [n] attaché à la bonne affirmation).
6. **Mise en ligne.** Fusionner `origin/main` d'abord (sinon `publier.sh` efface de gh-pages les pages publiées par une
   autre session), puis `site/outils/publier.sh`, IndexNow pour les adresses modifiées (clé `indexnow` de
   `site/contenu/site.json`, POST `https://api.indexnow.org/indexnow`, via `COMPOSIO_REMOTE_BASH_TOOL` si le réseau
   local bloque), vérification en ligne : code 200 et nouveau texte présent.
7. **Suivi.** Une ligne par couple traité dans le tableau ci-dessous, puis journal (`04-journal-decisions.md`) et
   commit avec `site/outils/dates-contenu.json`. Le mois suivant, relever la nouvelle position des mêmes couples
   (colonne « Position le mois suivant »).

## Garde-fous

- **Le slug ne change jamais.** Une seule page par recherche : si la requête relève d'un autre article, renforcer le
  lien interne vers lui plutôt que de créer une 2e page sur le même sujet.
- **Aucun fait nouveau sans source.** Toute phrase factuelle ajoutée s'appuie sur une source déjà présente dans la page
  (même numéro [n]). Sinon, vérifier la source dans PubMed ou sur le site officiel et l'ajouter proprement à la liste,
  ou s'abstenir.
- Style : `style-humain.md` (pas de tics d'IA, pas d'anglais). Vécu : `vecu-auteur.md` (rien d'inventé, jamais de
  métier). Prudence santé : aucune promesse, « Quand consulter ? » et numéros d'urgence intacts.
- Ne pas retoucher la même page chaque mois sur la même requête : Google met plusieurs semaines à réévaluer une page.
- Les positions sur quelques impressions sont très instables : une requête à 1 ou 2 impressions est un indice, pas une
  mesure.

## Tableau de suivi

| Date | Requête | Page | Position avant | Impressions avant | Modification faite | Position le mois suivant |
|---|---|---|---|---|---|---|
| 21/10/2026 | technique respiration pour dormir 4 7 8 | /respiration-pour-dormir/ | 24,2 | 5 | H3 « Comment faire la technique de respiration 4-7-8 pour dormir ? » déjà ajoutée le 18/10 ; description : « la technique 4-7-8 pas à pas » | |
| 21/10/2026 | réveil nocturne 4h | /reveil-4h-du-matin/ | 35,8 | 4 (1 clic) | description, 1re phrase de l'introduction et H2 « Que faire en cas de réveil nocturne à 4h du matin ? » | |
| 21/10/2026 | respiration guidée | /respiration-guidee/ | 37,3 | 4 | « respiration guidée » dans la 1re phrase (titre SEO et question « Qu'est-ce que la respiration guidée ? » déjà présents depuis le 18/10) | |
| 21/10/2026 | numéro vert 24 24 | /ressources-urgence/ | 39,5 | 2 | question fréquente « Existe-t-il un numéro vert gratuit 24 h/24 ? » (3114, 15/112, 3919, 119, SOS Amitié, Fil Santé Jeunes, sources [1][2][3][5] déjà présentes) | |
| 21/10/2026 | toujours reveille a 4 heures (1 impr.) | /reveil-4h-du-matin/ | 19 | 1 | rien : question fréquente déjà ajoutée le 18/10 | |
| 21/10/2026 | réveil précoce (1 impr.) | /reveil-4h-du-matin/ | 27 | 1 | rien : question fréquente déjà ajoutée le 18/10 | |
| 21/10/2026 | adrenaline cortisol (1 impr.) | /cortisol-hormone-du-stress/ | 34 | 1 | rien : tableau adrénaline/cortisol et question fréquente déjà présents | |
| 21/10/2026 | se reveiller a 4 heures (1 impr.) | /reveil-4h-du-matin/ | 38 | 1 | rien : question « Est-ce normal de se réveiller à 4 heures du matin ? » déjà présente | |

Données de la 1re passe : 09/10 au 20/10/2026, 57 couples (requête, page) au total ; 4 seulement remplissent le seuil
de 2 impressions, d'où l'ajout des 4 couples à 1 impression (notés « 1 impr. »). Les autres requêtes du site sont au-delà
de la 40e position (ex. « symptomes stress » 91, « cortisol définition » 78, « procrastination du sommeil causes » 58).
