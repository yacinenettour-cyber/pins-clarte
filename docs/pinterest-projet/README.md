# Documentation de projet — Compte Pinterest "Clarté Mentale | Stress & Énergie"

Ensemble de fichiers autoportants, pensés pour être chargés comme connaissance de projet (Claude Project ou équivalent) indépendamment de toute conversation Claude Code particulière. Mis à jour le 27 septembre 2026.

## Sommaire

1. **[00-vue-ensemble.md](00-vue-ensemble.md)** — Identité du compte, objectif business (formation systeme.io), tunnel de conversion, chiffres clés, les deux périmètres (éditorial vs formation) à ne pas confondre.
2. **[01-architecture-technique.md](01-architecture-technique.md)** — Comment le pipeline de publication fonctionne : déclenchement, étapes, fichiers, secrets, formats.
3. **[02-tableaux-pinterest.md](02-tableaux-pinterest.md)** — Détail des 9 tableaux Pinterest (ID, sujet, volume, exemples de titres, lien formation oui/non).
4. **[03-regles-editoriales.md](03-regles-editoriales.md)** — Toutes les règles à appliquer avant d'ajouter du contenu, avec checklist de vérification.
5. **[04-journal-decisions.md](04-journal-decisions.md)** — Historique et raisonnement des décisions prises, pour comprendre le "pourquoi" de chaque règle sans avoir à tout redemander.
6. **[05-process-operationnel.md](05-process-operationnel.md)** — Le mode opératoire complet : cycle de publication, rotation par thème, règle critique de synchronisation avec `main`, seuils d'alerte, qui fait quoi (automatique / Claude / utilisateur).
7. **[liens-anciens-pins.md](liens-anciens-pins.md)** — Les 31 anciens pins sans lien à relier au guide à la main (l'API ne peut pas modifier un pin), avec le lien exact et une consigne pour l'extension Claude.

## À lire en premier

Pour une nouvelle conversation qui découvre ce projet : lire dans l'ordre 00 → 03 suffit pour travailler correctement sur ce compte. Le 04 est utile en complément pour comprendre le contexte, mais pas indispensable au quotidien.

## Autres fichiers de référence dans ce dépôt (pas dans ce dossier)

- `/CLAUDE.md` — résumé condensé de `03-regles-editoriales.md`, chargé automatiquement par Claude Code au démarrage d'une session sur ce dépôt Git.
- `/README.md` — documentation technique complète du fonctionnement du dépôt (recoupe largement `01-architecture-technique.md` et `03-regles-editoriales.md`, avec quelques détails de configuration supplémentaires — ex. déclenchement cron-job.org pas à pas).
- `/prompts/system-prompt-pin-seo.md` — prompt système pour le futur module IA Make.com (flux image → texte).

## Point à retenir sur les données de performance

Ces fichiers ne contiennent **aucune donnée réelle de Pinterest Analytics** (impressions, enregistrements, clics) — elle n'a jamais été fournie. Toutes les règles de contenu reposent sur les bonnes pratiques Pinterest génériques, pas sur des chiffres réels de performance de ce compte. Voir la fin de `04-journal-decisions.md`.
