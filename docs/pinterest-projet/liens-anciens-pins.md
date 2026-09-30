# Ajouter le lien du guide sur 31 anciens pins (30/09/2026)

**Pourquoi** : sur les 90 derniers jours au 30/09/2026 (métriques `90d` de `PINTEREST_LIST_PINS`, 225 pins listés), 75 % des vues du compte (98 908 sur 131 714) tombent sur d'anciens Idea Pins **sans lien** : aucun clic vers le guide n'y est possible. Les 31 pins ci-dessous sont ceux dont le **contenu réel** (description lue en entier, pas seulement le titre) correspond au périmètre du lien : sommeil et mécanismes du stress (système nerveux, tensions du corps, respiration, postures). Ensemble : 35 550 vues sur 90 jours. Les 10 premiers en font 88 %, le n°1 à lui seul 63 %.

**Pourquoi à la main** : l'API Pinterest via Composio refuse toute modification de pin (`PINTEREST_UPDATE_PIN` → 401 « restricted feature: pin_edit »), constaté le 29/09 puis de nouveau le 30/09. Le pin de test (n°20) est resté inchangé.

**Accord de l'utilisateur** : donné le 30/09/2026 pour cette liste (option « Lien sur 33 anciens pins », ramenée à 31 après relecture des descriptions).

## Le lien à coller (identique pour les 31 pins)

```
https://lp.contactapaisement-mental.fr/tonguide?utm_source=pinterest&utm_medium=organic&utm_campaign=anciens-pins
```

Même format que les pins automatiques (`pins.yml`), avec `utm_campaign=anciens-pins` : dans systeme.io, l'URL source d'un nouvel inscrit dira s'il vient de ces anciens pins.

## Comment faire (1 minute par pin)

Ouvrir le pin → icône crayon (ou « … » → « Modifier l'épingle ») → champ **Lien** : coller le lien ci-dessus → **Enregistrer**. Ne rien changer d'autre (titre, description, tableau, texte alternatif).

Si le champ Lien n'apparaît pas sur un pin : le noter et passer au suivant.

## La liste, par nombre de vues (90 jours)

| # | Pin | Vues 90 j | Adresse |
|---|---|---|---|
| 1 | 🌿 5 gestes doux pour apaiser le corps dès le matin | 22 543 | https://www.pinterest.com/pin/600175087885208935/ |
| 2 | 7 signes physiques du stress chronique | 1 593 | https://www.pinterest.com/pin/600175087886740080/ |
| 3 | 5 exercices de respiration anti-stress efficaces | 1 531 | https://www.pinterest.com/pin/600175087886922103/ |
| 4 | 4 erreurs qui épuisent ton système nerveux | 1 217 | https://www.pinterest.com/pin/600175087886779579/ |
| 5 | Technique 4-6 : Calme le cœur en 2 min | 1 153 | https://www.pinterest.com/pin/600175087885898482/ |
| 6 | 3 postures simples pour calmer le stress en quelques minutes | 939 | https://www.pinterest.com/pin/600175087885294130/ |
| 7 | 5 étapes pour calmer un mental le soir | 740 | https://www.pinterest.com/pin/600175087886071865/ |
| 8 | 5 postures de yoga pour réduire le stress | 675 | https://www.pinterest.com/pin/600175087886867911/ |
| 9 | Sommeil difficile ? 6 infusions qui aident vraiment | 564 | https://www.pinterest.com/pin/600175087885585019/ |
| 10 | 3 gestes simples pour baisser le cortisol | 397 | https://www.pinterest.com/pin/600175087885922045/ |
| 11 | Boule dans la gorge : ce que ton système nerveux signale | 359 | https://www.pinterest.com/pin/600175087886257448/ |
| 12 | 5 effets du stress sur l’estomac le soir | 329 | https://www.pinterest.com/pin/600175087884937437/ |
| 13 | Comment diminuer le stress au travail naturellement ? | 318 | https://www.pinterest.com/pin/600175087884496637/ |
| 14 | 4 gestes simples pour calmer ton stress rapidement | 305 | https://www.pinterest.com/pin/600175087885672669/ |
| 15 | Si tu rumines la nuit  ton cerveau cherche à se protéger | 276 | https://www.pinterest.com/pin/600175087886257379/ |
| 16 | Système nerveux saturé ? Fais ça | 267 | https://www.pinterest.com/pin/600175087886575183/ |
| 17 | 5 signes que ton stress t’épuise | 260 | https://www.pinterest.com/pin/600175087886552068/ |
| 18 | 6 actions simples contre le cortisol | 227 | https://www.pinterest.com/pin/600175087886050525/ |
| 19 | 6 zones du corps où la pression s’accumule | 195 | https://www.pinterest.com/pin/600175087885585653/ |
| 20 | 5 erreurs qui sabotent ton sommeil | 173 | https://www.pinterest.com/pin/600175087884980450/ |
| 21 | 6 leviers pour calmer le système nerveux | 170 | https://www.pinterest.com/pin/600175087885606881/ |
| 22 | 7 signes d’un système nerveux saturé | 166 | https://www.pinterest.com/pin/600175087886006486/ |
| 23 | 5 gestes ultra-simples pour calmer le stress | 162 | https://www.pinterest.com/pin/600175087885053079/ |
| 24 | 5 plantes qui détendent le système nerveux (sans somnifère) | 149 | https://www.pinterest.com/pin/600175087885004280/ |
| 25 | 5 façons douces de faire redescendre le stress | 148 | https://www.pinterest.com/pin/600175087885138108/ |
| 26 | 6 astuces pour calmer le stress au travail | 141 | https://www.pinterest.com/pin/600175087885675021/ |
| 27 | 5 étapes pour décharger sa journée | 138 | https://www.pinterest.com/pin/600175087885920840/ |
| 28 | 5 techniques anti-stress à faire avant 9 h | 136 | https://www.pinterest.com/pin/600175087884958702/ |
| 29 | Corps épuisé  cerveau éveillé : 4 étapes | 112 | https://www.pinterest.com/pin/600175087885115875/ |
| 30 | Quand le corps est épuisé mais que le cerveau refuse de s’éteindre | 84 | https://www.pinterest.com/pin/600175087884686915/ |
| 31 | Les signaux discrets d’un corps sous pression constante | 83 | https://www.pinterest.com/pin/600175087884725608/ |

## Exclus volontairement

- **Hors périmètre du guide** (règle `THEMES_SANS_LIEN`) : procrastination (dont « 5 Clés pour Vaincre la Procrastination », 16 195 vues), alimentation / cortisol par l'alimentation, énergie, fatigue mentale, anti-âge, hormones, libido.
- **Retirés après lecture complète** : « 4 solutions pout apaiser ton système nerveux. » (600175087886513407 : contenu procrastination / fatigue mentale) et « 5 alternatives simples pour calmer le stress » (600175087885497866 : surtout des remplacements alimentaires).
- Déjà faits le 29/09 : « Si ton cerveau ne s'arrête jamais la nuit » et « 6 étapes pour débloquer ton mental ».

## Consigne pour l'extension Claude (Chrome), si l'utilisateur préfère la déléguer

```
Sur Pinterest (compte clartementale, déjà connecté), pour chacun des pins de la liste ci-dessous, dans l'ordre :
1. Ouvre l'adresse du pin.
2. Clique sur l'icône crayon (ou « … » puis « Modifier l'épingle »).
3. Dans le champ « Lien », colle exactement :
https://lp.contactapaisement-mental.fr/tonguide?utm_source=pinterest&utm_medium=organic&utm_campaign=anciens-pins
4. Clique sur « Enregistrer ». Ne modifie rien d'autre : ni le titre, ni la description, ni le tableau, ni le texte alternatif.
5. Si le champ « Lien » n'existe pas ou si l'enregistrement échoue, note le numéro du pin et passe au suivant.
À la fin, donne-moi la liste des numéros réussis et des numéros en échec.

1. https://www.pinterest.com/pin/600175087885208935/
2. https://www.pinterest.com/pin/600175087886740080/
3. https://www.pinterest.com/pin/600175087886922103/
4. https://www.pinterest.com/pin/600175087886779579/
5. https://www.pinterest.com/pin/600175087885898482/
6. https://www.pinterest.com/pin/600175087885294130/
7. https://www.pinterest.com/pin/600175087886071865/
8. https://www.pinterest.com/pin/600175087886867911/
9. https://www.pinterest.com/pin/600175087885585019/
10. https://www.pinterest.com/pin/600175087885922045/
11. https://www.pinterest.com/pin/600175087886257448/
12. https://www.pinterest.com/pin/600175087884937437/
13. https://www.pinterest.com/pin/600175087884496637/
14. https://www.pinterest.com/pin/600175087885672669/
15. https://www.pinterest.com/pin/600175087886257379/
16. https://www.pinterest.com/pin/600175087886575183/
17. https://www.pinterest.com/pin/600175087886552068/
18. https://www.pinterest.com/pin/600175087886050525/
19. https://www.pinterest.com/pin/600175087885585653/
20. https://www.pinterest.com/pin/600175087884980450/
21. https://www.pinterest.com/pin/600175087885606881/
22. https://www.pinterest.com/pin/600175087886006486/
23. https://www.pinterest.com/pin/600175087885053079/
24. https://www.pinterest.com/pin/600175087885004280/
25. https://www.pinterest.com/pin/600175087885138108/
26. https://www.pinterest.com/pin/600175087885675021/
27. https://www.pinterest.com/pin/600175087885920840/
28. https://www.pinterest.com/pin/600175087884958702/
29. https://www.pinterest.com/pin/600175087885115875/
30. https://www.pinterest.com/pin/600175087884686915/
31. https://www.pinterest.com/pin/600175087884725608/
```

## Vérification

Après modification : `PINTEREST_GET_PIN` sur chaque identifiant (champ `link`), puis suivi des clics sortants de ces pins (`PINTEREST_GET_PIN_ANALYTICS`, métrique `OUTBOUND_CLICK`) vers le 14/10/2026.
