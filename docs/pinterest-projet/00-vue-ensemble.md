# Vue d'ensemble — Compte Pinterest "Clarté Mentale | Stress & Énergie"

Document de référence à jour au 27 septembre 2026. Fait partie d'un ensemble de fichiers dans `docs/pinterest-projet/` destinés à être chargés comme connaissance de projet (Claude Project ou équivalent), indépendamment de toute conversation particulière.

## Identité du compte

- **Nom de marque** : Clarté Mentale | Stress & Énergie
- **Langue** : français
- **Bio Pinterest** (partielle, capturée par l'utilisateur) : "...nerveux. Je décrypte les mécan[ismes]... [du stress]" — se termine par un lien vers `lp.contactapaisement-mental.fr`
- **Site / page de capture** : URL fournie via le secret GitHub `LIEN_PAGE`, gérée sur systeme.io

## Objectif business

Le compte vend une **formation** hébergée sur systeme.io, accessible via une page de capture. L'objectif n'est pas la simple visibilité : c'est la génération de **clics qualifiés** qui se convertissent en inscriptions.

**Tunnel visé** :
```
IMPRESSION → INTÉRÊT → ENREGISTREMENT/CLIC → PAGE DE CAPTURE → INSCRIPTION
```

Conséquence directe sur la stratégie de contenu : un pin qui génère des impressions mais attire un public hors-cible (intéressé par un sujet que la formation ne couvre pas) est une perte, pas un gain — d'où la règle du lien conditionnel (voir plus bas et `03-regles-editoriales.md`).

## Les deux périmètres du compte (important, source de confusion possible)

Le compte publie du contenu sur **9 thèmes** pour construire son audience et sa présence organique sur Pinterest, mais la **formation elle-même ne couvre que 7 de ces 9 thèmes**. Ne pas confondre les deux :

| | Thèmes concernés |
|---|---|
| **Périmètre éditorial du compte** (tous les thèmes publiés) | sommeil, système nerveux/cortisol, fatigue mentale, alimentation, procrastination, somatisation, blocage mental, postures anti-stress, énergie |
| **Périmètre de la formation** (thèmes avec lien vers la page de capture) | sommeil, système nerveux/cortisol, fatigue mentale, postures anti-stress, blocage mental, somatisation, énergie |
| **Hors périmètre de la formation** (contenu du compte, mais sans lien de destination) | alimentation *(uniquement sous l'angle "réduit le stress")*, procrastination |

Voir `02-tableaux-pinterest.md` pour le détail board par board, et `03-regles-editoriales.md` pour la règle complète sur le lien conditionnel.

## Chiffres clés (état au 27/09/2026)

- **220 pins** dans la banque de textes (`pins.json`), dont **41 déjà publiés** sur Pinterest, **179 en attente**.
- **30 scripts de Video Pins** (`videos.json`), dont **4 déjà publiées**, **26 en attente**.
- **192 photos de fond** réparties par thème (`fonds/` + `fonds_themes.json`).
- **9 tableaux (boards) Pinterest**, un par thème, chacun avec son propre ID Pinterest (voir `02-tableaux-pinterest.md`).
- **9 pins** utilisent une image prête fournie par l'utilisateur (`image_prete`) plutôt qu'une image générée automatiquement.

## Fonctionnement en une phrase

Un workflow GitHub Actions (déclenché 10×/jour pour les pins, 1×/jour pour les vidéos par un service cron externe) prend le prochain pin non publié dans `pins.json`, génère ou choisit son image, l'envoie à un webhook Make.com qui publie sur Pinterest — sans aucune vérification de pertinence automatique, d'où l'importance des règles éditoriales appliquées **avant** l'ajout de tout contenu à la banque. Détail complet dans `01-architecture-technique.md`.

## Historique de ce projet

Ce document et les fichiers associés ont été créés après une session d'audit et de nettoyage importante (voir `04-journal-decisions.md`) : retrait de contenu hors-sujet déjà publié, recentrage du board alimentation, réécriture complète de 188 pins (titres, descriptions SEO, CTA variés), et mise en place du lien conditionnel selon le périmètre réel de la formation.
