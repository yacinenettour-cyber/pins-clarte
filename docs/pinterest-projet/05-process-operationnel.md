# Process opérationnel — compte Pinterest "Clarté Mentale | Stress & Énergie"

Ce document décrit le fonctionnement réel du compte au quotidien : ce qui tourne seul, ce qui déclenche une intervention, et qui fait quoi. Mis à jour le 28 septembre 2026, suite à deux incidents corrigés ce jour-là (voir section 4).

---

## 1. Vue d'ensemble du cycle

```
cron-job.org (toutes les 2h)
        │
        ▼
GitHub Actions (pins.yml / videos.yml) sur la branche "main"
        │
        ├─ choisit un pin/vidéo (rotation par thème, voir §2)
        ├─ génère ou choisit l'image
        ├─ commit dans le dépôt + push
        └─ envoie à Make.com → publication sur Pinterest
```

Rien de tout cela ne dépend d'une session Claude Code active. Le compte publie 7×/jour pour les pins et vise 1×/jour pour les vidéos, **du moment que `main` contient une banque propre**.

## 2. Ce qui est désormais 100 % automatique

- **Publication** : cron-job.org déclenche le workflow, aucune action humaine requise.
- **Rotation par thème** (nouveau, 28/09/2026) : le script ne prend plus le premier pin du tableau dans l'ordre — il choisit le **thème dont la dernière publication est la plus ancienne**, puis le premier pin disponible de ce thème. Avant ce correctif, la banque étant remplie par lots thématiques, un même thème pouvait enchaîner des dizaines de pins d'affilée (observé le 27-28/09 : 9 pins sommeil consécutifs). Voir `choisir_pin_equilibre()` dans `pins.yml` et `choisir_video_equilibree()` dans `videos.yml`.
- **Anti-répétition** : un pin/vidéo déjà publié (par titre/id exact dans `historique.json`/`historique_videos.json`) n'est jamais repris.
- **Choix de l'image** : fond thématique dans `fonds/`, génération IA via `OPENAI_API_KEY` si configuré, ou `image_prete` si le pin en fournit une.
- **Lien de destination conditionnel** : vide sur les thèmes hors périmètre de la formation (`alimentation`, `procrastination`), voir `03-regles-editoriales.md`.
- **Purge** : les images/vidéos de plus de 30 jours sont supprimées du dépôt automatiquement.

## 3. Processus d'ajout de nouveau contenu

Déclenché par l'utilisateur (nouvelle idée, lot d'images, retour d'expérience) ou par Claude en session. Toujours dans cet ordre :

1. **Trier** — écarter ce qui ne correspond pas au périmètre du compte (voir `03-regles-editoriales.md`, règles 1-4 et le cas particulier recettes anti-stress/sommeil).
2. **Rédiger** — titre travaillé, description 380-450 caractères de corps, mots-clés naturels, CTA varié et adapté au thème (règles 5-6, voir aussi le prompt SEO dans `prompts/system-prompt-pin-seo.md` pour le detail par champ).
3. **Image** — vérifier la cohérence avec le texte ; pour un lot d'images composite, suivre la procédure de découpe/recadrage plein cadre du README (section "Images fournies en planche") ; pour une génération IA, suivre les règles du README (section "Génération d'images") — jamais de texte incrusté par l'IA, toujours vérifier le résultat avant de le garder, supprimer ce qui n'est pas exploitable.
4. **Vérifier par script** (jamais à l'œil) : 0 doublon exact, 0 quasi-doublon (`difflib.SequenceMatcher > 0.72`), longueurs dans les limites, premier hashtag cohérent avec le thème visé, pins déjà publiés intacts, images `image_prete` toutes présentes sur disque.
5. **Committer et pousser — directement sur `main`, ou fusionner immédiatement** (voir règle critique ci-dessous). Ne jamais laisser une correction sur une branche non fusionnée : elle n'a aucun effet tant qu'elle n'est pas sur `main`.

## 4. Règle critique : toujours synchroniser avec `main`

**Incident du 27/09/2026** : une session entière de nettoyage (retrait de 11 pins hors-sujet, recentrage du board alimentation, réécriture de 188 pins) a été faite sur une branche de travail jamais fusionnée dans `main`. Le pipeline de production publie depuis `main`, pas depuis la branche de session — résultat : le compte a continué à publier l'ancienne banque non corrigée pendant toute la journée (8 pins hors-sujet publiés avant que l'erreur soit détectée et corrigée en urgence).

**Incident du 28/09/2026** (mineur) : un `git push` vers `main` a été rejeté le lendemain matin car le pipeline automatique avait continué à committer (`historique.json`, `images/`, `videos/`) pendant la nuit — `main` avait avancé sans que la session le sache.

**Conséquence pour toute session future sur ce dépôt** :
- Avant de commencer à travailler, faire `git fetch origin main` et vérifier où en est `main` — le pipeline y committe en continu, 24h/24.
- Travailler directement sur `main`, ou fusionner sa branche dans `main` **avant la fin de la session**, jamais "à la prochaine fois".
- Avant de pousser vers `main`, toujours fusionner d'abord les commits automatiques récents (`git fetch origin main && git merge origin/main`) pour éviter un rejet et repartir sur une base à jour.
- Ne jamais considérer une correction "faite" tant qu'elle n'est pas visible sur `origin/main` — vérifier avec `git log origin/main` ou en recomptant les publications du jour dans `historique.json` côté `main`.

## 5. Sourcing et génération d'images — arbre de décision

1. **L'utilisateur fournit une image prête** → vérifier la cohérence texte/image, l'ajouter en `image_prete`.
2. **L'utilisateur fournit une planche composite** → découper, recadrer plein cadre (voir README), trier, écarter ce qui a du texte tronqué à la source ou qui est inexploitable.
3. **Besoin d'un fond réutilisable classique** (`fonds/`) → génération IA via un connecteur disponible en session (Hugging Face en priorité, gratuit ; Claude_image si crédits disponibles ; Canva non testé à ce jour) — jamais de texte incrusté par l'IA, laisser `dessiner_image()` gérer le texte.
4. **Rien de tout ça disponible** → le pipeline retombe sur un fond dégradé par défaut (comportement existant, pas idéal mais fonctionnel).

## 6. Seuils d'alerte — quand intervenir

| Signal | Seuil | Action |
|---|---|---|
| Pins restants dans la banque | < 50 (≈ 1 semaine à 7/jour) | Ajouter du nouveau contenu avant pénurie |
| Un thème à < 5 pins restants | Sous ce seuil | Prioriser l'ajout de contenu sur ce thème specifiquement |
| Vidéos restantes | < 7 (≈ 1 semaine) | Ajouter de nouveaux scripts dans `videos.json` |
| `main` en avance sur la dernière session connue | Toujours vérifier en début de session | `git fetch origin main` avant toute action |
| Crédits Claude_image | Vérifier avec `get_credits` avant de générer | Basculer sur Hugging Face (gratuit) si épuisés |

État au 28/09/2026 pour référence : 207 pins restants (~30 jours de réserve globale), répartition 42 % sommeil / 15 % système nerveux / 5-10 % chacun des 7 autres thèmes — désormais lissée dans le temps par la rotation automatique plutôt que consommée dans l'ordre.

## 7. Ce qui reste manuel (côté utilisateur, hors de portée de Claude Code)

- **Supprimer un pin déjà publié sur Pinterest** — aucun accès à l'API Pinterest depuis cet environnement ; à faire directement dans l'app (••• → Supprimer).
- **Vérifier/ajuster les scénarios Make.com** (webhooks, mapping des champs).
- **Fournir les statistiques Pinterest Analytics** (enregistrements, clics par pin/board) — jamais reçues à ce jour ; sans elles, toutes les décisions de contenu reposent sur les bonnes pratiques génériques, pas sur la performance réelle du compte.
- **Gérer les secrets GitHub** (`LIEN_PAGE`, `MAKE_WEBHOOK_URL`, `OPENAI_API_KEY`...).
- **Recharger les crédits Claude_image** si le volume de génération d'images dépasse ce que Hugging Face peut couvrir.

## 8. Boucle de rétroaction analytics (à activer dès que possible)

Dès que des données réelles sont disponibles :
1. Identifier les titres/formulations qui génèrent le plus d'enregistrements et de clics par board.
2. Orienter les prochains titres vers ces formulations gagnantes (voir `03-regles-editoriales.md`, règle 6 : passer du test à l'aveugle à l'optimisation par la donnée).
3. Réévaluer la répartition cible par thème (actuellement dictée par le contenu disponible, pas par la performance).
4. Réévaluer le périmètre du board `alimentation` et des thèmes sans lien de destination si la formation évolue.

## 9. Fréquence de contrôle recommandée

- **À chaque session Claude Code sur ce dépôt** : `git fetch origin main`, vérifier les publications du jour, vérifier qu'aucun rejet de push n'est resté en suspens.
- **Hebdomadaire** (recommandé, pas encore automatisé) : vérifier les seuils du §6, ajouter du contenu si besoin.
- **Dès que disponibles** : intégrer les données Pinterest Analytics (§8).
