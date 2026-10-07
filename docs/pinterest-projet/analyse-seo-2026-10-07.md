# Analyse SEO du compte — 07/10/2026

Données lues via Composio (Pinterest API v5) : profil, 11 tableaux, **436 pins** avec statistiques 90 jours et cumulées, statistiques du compte sur 90 jours, tendances de recherche Pinterest **France** (`PINTEREST_GET_KEYWORD_TRENDS`).

## 1. Chiffres du compte (90 jours, 09/07 → 06/10)

- 157 526 impressions, 9 318 clics sur les pins, 1 423 enregistrements, **49 clics sortants**.
- Impressions par semaine : ~22-24 k mi-juillet → ~7 k début septembre → **11-12 k** les deux dernières semaines (reprise avec le pipeline).
- Profil : 200 abonnés, 40 031 vues mensuelles. **Site `lp.contactapaisement-mental.fr/tonguide` déclaré mais non vérifié** (statut vide).

## 2. Constat principal : le format

| Pins | Nombre | Impressions cumulées (médiane) | Enregistrements (moyenne) |
|---|---|---|---|
| Anciens pins natifs `IDEA` (déc. → juil., faits à la main) | 304 | **3 160** | 70 |
| Pins automatiques `REGULAR` (depuis le 24/09) | 118 | **24** | 0 |
| Vidéos automatiques | 8 | 18 | 0 |

Réserve : les pins automatiques ont 1 à 13 jours, et le référencement Pinterest met plusieurs semaines à démarrer. Mais les plus anciens (24/09) plafonnent à ~50 impressions et **aucun des 128 pins récents n'a été enregistré** : c'est un signal faible d'engagement, à surveiller fin octobre. Les impressions actuelles viennent encore surtout des anciens Idea Pins.

## 3. Tableaux (impressions 90 jours)

| Tableau | Pins | Impressions | Moy./pin |
|---|---|---|---|
| Système nerveux & gestion du stress | 103 | 59 661 | 579 |
| Fatigue mentale, charge mentale & burn-out | 81 | 28 639 | 354 |
| Procrastination & fatigue mentale | 20 | 21 710 | **1 086** |
| Énergie & fatigue | 31 | 13 208 | 426 |
| Alimentation & stress | 45 | 10 443 | 232 |
| Sommeil : mieux dormir & routine du soir | 66 | 9 231 | **140** |
| Somatisation & signaux du corps | 32 | 4 914 | 154 |
| 🧠 Fatigue & Causes Biologiques | 8 | 4 558 | 570 |
| Postures anti-stress au travail | 26 | 1 447 | **56** |
| Blocages mentaux & clarté mentale | 21 | 1 337 | **64** |

Le sommeil, thème le plus poussé par le pipeline (thème avec lien, rotation ×2), est l'un des moins vus.

## 4. Mots des titres qui marchent (anciens pins, impressions médianes)

- **Forts** : cortisol (élevé), procrastination, émotions, « clés », « étapes », énergie, surcharge mentale, retrouver, endormir, respiration, causes, erreurs, signes, corps.
- **Faibles** : soir, dormir, esprit, calme, phrases, mental, quotidien, journée, alerte.
- Titres des meilleurs pins : **~44 caractères** en médiane ; titres automatiques récents : **~66**. Pinterest n'affiche qu'environ 40 caractères dans le fil : le mot-clé doit être au début.
- Chiffre en tête : léger avantage (médiane 3 313 contre 2 983).

## 5. Tendances de recherche Pinterest France

| Mot-clé | Sur un an | Sur un mois |
|---|---|---|
| cortisol | **+300 %** | +4 % |
| « high cortisol » / « low cortisol » (recherchés en anglais en France) | +6 000 % / +10 000 % | — |
| système nerveux | +30 à +80 % | **+100 %** |
| routine du soir | +30 % | +9 % |
| charge mentale | +20 % | +40 % |
| gestion des émotions | −50 % | **+90 %** |
| burn out | −4 % | +50 % |
| nerf vague | −40 % | +80 % |
| énergie | +10 % | +50 % |
| fatigue | +20 % | +30 % |
| sommeil | +20 % | +6 % |
| respiration | +10 % | +10 % |
| procrastination | −5 % | +20 % |
| fatigue mentale | **−40 %** | −20 % |
| motivation | −20 % | +6 % |

**Absents des classements Pinterest France** (volume trop faible pour y figurer) : somatisation, insomnie, cohérence cardiaque, magnésium, angoisse, anxiété, mieux dormir, ashwagandha. « anti stress » renvoie surtout à des balles anti-stress à fabriquer (hors sujet).

## 6. Recommandations

1. **Tableaux** (renommage sans risque : le pipeline utilise les identifiants) — mettre le mot-clé recherché en tête :
   - « Somatisation & signaux du corps » → « Stress et corps : tensions, douleurs & signaux » (somatisation n'est pas recherché) ;
   - « 🧠 Fatigue & Causes Biologiques » → « Cortisol & fatigue : causes biologiques » ;
   - « Blocages mentaux & clarté mentale » → « Gestion des émotions & blocages mentaux » ;
   - « Postures anti-stress au travail » → « Stress au travail : postures & pauses » ;
   - « Fatigue mentale, charge mentale & burn-out » → « Charge mentale & burn-out : fatigue mentale » ;
   - descriptions des tableaux : y intégrer cortisol, système nerveux, routine du soir, charge mentale, gestion des émotions.
2. **Titres des prochains pins** : 40-55 caractères, mot-clé en premier (« Cortisol : … », « Système nerveux : … », « Routine du soir : … »), garder chiffre + liste.
3. **Sujets à renforcer** : cortisol, système nerveux / nerf vague, routine du soir, charge mentale, gestion des émotions, burn-out. Ne plus utiliser « somatisation », « cohérence cardiaque », « insomnie » comme mot principal d'un titre.
4. **Hashtags** : Pinterest ne s'en sert presque plus pour classer les pins ; 3-5 suffisent, l'espace libéré sert mieux à des mots-clés en phrases (le premier hashtag reste nécessaire au routage du pipeline).
5. **Vérifier le site** sur Pinterest (balise meta dans l'en-tête de la page systeme.io) : attribution des pins au domaine et meilleure confiance.
6. **Format** : refaire le point fin octobre sur les pins automatiques ; si l'écart avec les Idea Pins reste aussi grand, publier à la main un Idea Pin par semaine (kits prêts dans `kits_idea_pins/`).
