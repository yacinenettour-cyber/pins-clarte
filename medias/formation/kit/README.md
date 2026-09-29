# Kit à imprimer de la formation (29/09/2026)

Six fiches A4 qui accompagnent le programme « Quand le cerveau refuse de dormir », plus le kit complet (couverture + 6 fiches). Elles sont liées depuis les leçons systeme.io via jsDelivr, épinglé sur un commit (voir `docs/systeme-io/pages/README.md`).

| Fichier | Contenu | Leçon qui la présente |
|---|---|---|
| `01-auto-evaluation.pdf` | 6 questions notées 0-4, jour 1 / 14 / 28, quand consulter | Auto-évaluation |
| `02-journal-sommeil-14-jours.pdf` | Journal du matin, 1 minute | Le matin compte autant que le soir |
| `03-rendez-vous-des-soucis.pdf` | Tableau souci / action / prochaine étape | Le rendez-vous des soucis |
| `04-liste-de-demain.pdf` | Liste des tâches à venir, avant de dormir | La liste de demain |
| `05-sos-reveil-nocturne.pdf` | Fiche de table de nuit, 6 étapes | Réveillé à 3 h du matin |
| `06-rituel-du-soir-3-versions.pdf` | Rituel en 3, 10 ou 20 minutes + suivi 4 semaines | 3 versions du rituel |
| `kit-complet-clarte-mentale.pdf` | Les 6 fiches + couverture | Ton kit à imprimer |

Régénérer : `source/gen_kit.py` écrit les pages HTML (dossier `html/` à côté du script, polices Lora et Poppins de `@fontsource` dans `fonts/`, obtenues avec `npm pack @fontsource/lora @fontsource/poppins`), puis `NODE_PATH=$(npm root -g) node source/print.js <dossier_pdf>` imprime les PDF avec Chromium et affiche la marge restante de chaque page (négative = débordement).

Attention : le dépôt est public, ces PDF sont donc accessibles à toute personne qui a le lien.
