# Épingles Pinterest vers la fiche Etsy (05/11/2026)

Trois épingles à publier **à la main** (hors pipeline : `pins.json` n'est pas touché), lien vers
https://www.etsy.com/fr/listing/4610269767 avec un `utm_content` différent par épingle. Images : `python3 outils/etsy/epingles_etsy.py`
(vraies pages du planner, texte et images dans des zones séparées, vérifié par assertion). Textes, liens et tableau : `epingles.json`.
Contrôles : titres 49-54 caractères, corps 371-386, total ≤ 490 ; `outils/anti_doublons.py` : 0 doublon contre l'historique, les kits,
`titres_en_ligne.json` et `pins.json`. Les 3 titres ont été ajoutés à `titres_en_ligne.json` pour que le pipeline ne publie jamais un
titre proche. Conseil : une épingle par jour, pas les trois le même jour.
