# Site Clarté Mentale — contactapaisement-mental.fr

Site statique francophone sur le stress, le sommeil et le système nerveux, hébergé gratuitement par **GitHub Pages** depuis la branche **`gh-pages`** du dépôt `pins-clarte` (sources ici, dans `site/`).

## Construire le site

```
pip install markdown pillow
python3 site/outils/construire.py   # construit site/_build/ (ignoré par git)
site/outils/publier.sh              # construit puis met en ligne sur la branche gh-pages
```

Le script régénère entièrement `site/_build/` à partir de :

- `contenu/site.json` : nom, adresse, guides gratuits, catégories, photo + texte alternatif + crédit de chaque article ;
- `contenu/articles/<slug>.md` : un article par fichier (en-tête entre `---`, puis Markdown ; sections reconnues : `## L'essentiel`, `## Questions fréquentes`, `## Pour aller plus loin`, `## Sources`) ;
- `contenu/pages/*.md` : À propos, Mentions légales ;
- `contenu/style.css` ; photos d'origine prises dans `fonds/` du dépôt (converties en WebP par le script).

Après une modification : relancer `construire.py`, vérifier, committer `site/` sur `main`, puis lancer `publier.sh`.

## Référencement

- **Google** : balises title/description/canonical, Open Graph, données structurées schema.org (Article avec auteur, éditeur et sources citées, FAQPage, BreadcrumbList, WebSite, Organization), `sitemap.xml`, `feed.xml`, pages légères sans script ni cookie.
- **Assistants IA** : `robots.txt` ouvert aux robots IA (GPTBot, ClaudeBot, PerplexityBot, Google-Extended…), `llms.txt` (résumé du site au format llmstxt.org) et `llms-full.txt` (texte intégral des articles), réponse directe en tête de chaque article, encadré « L'essentiel », FAQ autonome.
- **Bing / IndexNow** : fichier `<clé>.txt` à la racine du site (clé dans `contenu/site.json`).
- **Pinterest** : balise `p:domain_verify` sur l'accueil pour revendiquer le domaine.

## Règles éditoriales

Sujet santé : chaque affirmation importante est sourcée (Inserm, HAS, Ameli, Santé publique France, études publiées), aucune promesse médicale, une section « Quand consulter » par article, auteur non professionnel de santé (dit clairement). Photos : Pexels / Unsplash (licences gratuites), aucune image payante.
