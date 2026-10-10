# Grille d'audit RGAA 4.1 — www.contactapaisement-mental.fr

Audit interne du 10 octobre 2026, fait par l'éditeur du site (pas par un auditeur indépendant), avec des outils automatiques et des vérifications manuelles.

**Résultat : 70 critères conformes, 2 non conformes, 34 non applicables — taux de conformité 97 % (70 / 72 critères applicables).** Les 2 critères non conformes ne sont pas des défauts constatés : ce sont les critères qui demandent un test avec un vrai lecteur d'écran, pas encore fait ; ils sont comptés non conformes tant que ce test manque.

## Échantillon

Accueil, Tous les articles, articles « Nerf vague » et « Alimentation anti-stress », page thème « Mieux dormir », test de stress et d'anxiété, exercices de respiration, respiration guidée (audios), journal d'humeur, recherche, glossaire, questions fréquentes, ressources d'urgence, la formation, guide gratuit, À propos, mentions légales, accessibilité (18 pages). Les tests automatiques (axe-core, validation HTML, zoom, 320 px) ont porté sur les 31 à 33 pages du site.

## Environnement et outils

- Chromium (moteur de Google Chrome), écran d'ordinateur 1 280 px et téléphone 390 px / 320 px, mode clair et mode sombre.
- axe-core (règles WCAG 2.1 A et AA) : 0 violation sur 124 analyses (31 pages × 2 thèmes × 2 tailles d'écran).
- Validateur HTML du W3C (Nu Html Checker) : 0 erreur de balisage sur 33 pages.
- Mesure des contrastes au pixel (16 694 lignes de texte), parcours au clavier, arbre d'accessibilité du navigateur, tests d'espacement du texte, de zoom et de largeur 320 px.
- **Pas de test avec un lecteur d'écran** (NVDA, JAWS, VoiceOver, TalkBack) ni avec Firefox ou Safari : c'est la prochaine étape.

## Critères


### 1. Images

| Critère | Niveau | Statut | Constat |
|---|---|---|---|
| 1.1 Chaque image porteuse d’information a-t-elle une alternative textuelle ? | A | C | Photos d'articles, aperçu d'épingle, photo de l'auteur (À propos) et schéma du cortisol (SVG role=img) ont une alternative. |
| 1.2 Chaque image de décoration est-elle correctement ignorée par les technologies d’assistance ? | A | C | Vignettes des cartes et avatar à côté du nom : alt vide ; icônes SVG en aria-hidden ; canvas animé de l'accueil en aria-hidden. |
| 1.3 Pour chaque image porteuse d’information ayant une alternative textuelle, cette alternative est-elle pertinente (hors cas particuliers) ? | A | C | Alternatives relues : elles décrivent la photo ou reprennent le texte de l'image. |
| 1.4 Pour chaque image utilisée comme CAPTCHA ou comme image-test, ayant une alternative textuelle, cette alternative permet-elle d’identifier la nature et la fonction de l’image ? | A | NA | Aucun CAPTCHA ni image-test. |
| 1.5 Pour chaque image utilisée comme CAPTCHA, une solution d’accès alternatif au contenu ou à la fonction du CAPTCHA est-elle présente ? | A | NA | Aucun CAPTCHA. |
| 1.6 Chaque image porteuse d’information a-t-elle, si nécessaire, une description détaillée ? | A | C | Schéma du cortisol décrit en détail dans le texte adjacent ; texte de l'aperçu d'épingle = titre de la page. |
| 1.7 Pour chaque image porteuse d’information ayant une description détaillée, cette description est-elle pertinente ? | A | C | Descriptions pertinentes. |
| 1.8 Chaque image texte porteuse d’information, en l’absence d’un mécanisme de remplacement, doit si possible être remplacée par du texte stylé. Cette règle est-elle respectée (hors cas particuliers) ? | AA | C | Seule image texte : l'aperçu de l'épingle Pinterest, dont la présentation est essentielle (c'est l'image enregistrée). Maquettes du guide en texte HTML stylé. |
| 1.9 Chaque légende d’image est-elle, si nécessaire, correctement reliée à l’image correspondante ? | A | NA | Aucune image légendée (le crédit photo est dans le texte de l'article). |

### 2. Cadres

| Critère | Niveau | Statut | Constat |
|---|---|---|---|
| 2.1 Chaque cadre a-t-il un titre de cadre ? | A | NA | Aucun cadre (iframe). |
| 2.2 Pour chaque cadre ayant un titre de cadre, ce titre de cadre est-il pertinent ? | A | NA | Aucun cadre. |

### 3. Couleurs

| Critère | Niveau | Statut | Constat |
|---|---|---|---|
| 3.1 Dans chaque page web, l’ information ne doit pas être donnée uniquement par la couleur. Cette règle est-elle respectée ? | A | C | Choix sélectionnés : coche dessinée + bordure (corrigé ce jour) ; champs obligatoires indiqués par écrit ; liens du texte soulignés. |
| 3.2 Dans chaque page web, le contraste entre la couleur du texte et la couleur de son arrière-plan est-il suffisamment élevé (hors cas particuliers) ? | AA | C | Mesure au pixel de 16 694 lignes de texte (15 pages, 2 thèmes, téléphone et ordinateur) + axe-core. Corrigés ce jour : texte indicatif des champs (3,6:1 → 6,4:1), mot en dégradé du titre de l'accueil, maquette du guide en mode clair. |
| 3.3 Dans chaque page web, les couleurs utilisées dans les composants d’interface ou les éléments graphiques porteurs d’informations sont-elles suffisamment contrastées (hors cas particuliers) ? | AA | C | Contour de focus 9,4:1 (sombre) et 5,7:1 (clair) ; bordures des champs ≥ 3,4:1 ; état sélectionné ; icônes des boutons ; courbe du schéma 9:1 et 5,7:1. |

### 4. Multimédia

| Critère | Niveau | Statut | Constat |
|---|---|---|---|
| 4.1 Chaque média temporel pré-enregistré a-t-il, si nécessaire, une transcription textuelle ou une audiodescription (hors cas particuliers) ? | A | C | Audios de respiration sans voix : transcription dépliable sous chaque audio (ajoutée ce jour). |
| 4.2 Pour chaque média temporel pré-enregistré ayant une transcription textuelle ou une audiodescription synchronisée, celles-ci sont-elles pertinentes (hors cas particuliers) ? | A | C | Transcriptions fidèles au montage (8 s d'introduction, bols d'inspiration et d'expiration, fin). |
| 4.3 Chaque média temporel synchronisé pré-enregistré a-t-il, si nécessaire, des sous-titres synchronisés (hors cas particuliers) ? | A | NA | Aucune vidéo ni média synchronisé. |
| 4.4 Pour chaque média temporel synchronisé pré-enregistré ayant des sous-titres synchronisés, ces sous-titres sont-ils pertinents ? | A | NA | Aucune vidéo. |
| 4.5 Chaque média temporel pré-enregistré a-t-il, si nécessaire, une audiodescription synchronisée (hors cas particuliers) ? | AA | NA | Aucune vidéo. |
| 4.6 Pour chaque média temporel pré-enregistré ayant une audiodescription synchronisée, celle-ci est-elle pertinente ? | AA | NA | Aucune vidéo. |
| 4.7 Chaque média temporel est-il clairement identifiable (hors cas particuliers) ? | A | C | Chaque audio a un titre visible et un nom accessible (« Respiration guidée 4-6, 3 minutes »…). |
| 4.8 Chaque média non temporel a-t-il, si nécessaire, une alternative (hors cas particuliers) ? | A | NA | Aucun média non temporel. |
| 4.9 Pour chaque média non temporel ayant une alternative, cette alternative est-elle pertinente ? | A | NA | Aucun média non temporel. |
| 4.10 Chaque son déclenché automatiquement est-il contrôlable par l’utilisateur ? | A | NA | Aucun son déclenché automatiquement (les sons du minuteur démarrent avec le bouton Commencer ; option « Sans son »). |
| 4.11 La consultation de chaque média temporel est-elle, si nécessaire, contrôlable par le clavier et tout dispositif de pointage ? | A | C | Lecteurs audio natifs, utilisables au clavier et à la souris. |
| 4.12 La consultation de chaque média non temporel est-elle contrôlable par le clavier et tout dispositif de pointage ? | A | NA | Aucun média non temporel. |
| 4.13 Chaque média temporel et non temporel est-il compatible avec les technologies d’assistance (hors cas particuliers) ? | A | C | Lecteurs natifs (<audio controls>) avec nom accessible. |

### 5. Tableaux

| Critère | Niveau | Statut | Constat |
|---|---|---|---|
| 5.1 Chaque tableau de données complexe a-t-il un résumé ? | A | NA | Aucun tableau complexe. |
| 5.2 Pour chaque tableau de données complexe ayant un résumé, celui-ci est-il pertinent ? | A | NA | Aucun tableau complexe. |
| 5.3 Pour chaque tableau de mise en forme, le contenu linéarisé reste-t-il compréhensible ? | A | NA | Aucun tableau de mise en forme. |
| 5.4 Pour chaque tableau de données ayant un titre, le titre est-il correctement associé au tableau de données ? | A | C | Tableaux qui ont un titre (comparatif de l'accueil, notes du journal) : titre associé par aria-labelledby. Les autres tableaux n'ont pas de titre visible. |
| 5.5 Pour chaque tableau de données ayant un titre, celui-ci est-il pertinent ? | A | C | Titres pertinents. |
| 5.6 Pour chaque tableau de données, chaque en-tête de colonne et chaque en-tête de ligne sont-ils correctement déclarés ? | A | C | 64 tableaux : en-têtes de colonnes et de lignes déclarés (th + scope). |
| 5.7 Pour chaque tableau de données, la technique appropriée permettant d’associer chaque cellule avec ses en-têtes est-elle utilisée (hors cas particuliers) ? | A | C | Association par scope col/row. |
| 5.8 Chaque tableau de mise en forme ne doit pas utiliser d’éléments propres aux tableaux de données. Cette règle est-elle respectée ? | A | NA | Aucun tableau de mise en forme. |

### 6. Liens

| Critère | Niveau | Statut | Constat |
|---|---|---|---|
| 6.1 Chaque lien est-il explicite (hors cas particuliers) ? | A | C | Liens explicites ; appels de sources nommés « Source n » ; numéros d'urgence explicites par leur phrase. |
| 6.2 Dans chaque page web, chaque lien a-t-il un intitulé ? | A | C | Aucun lien vide (relevé automatique sur 18 pages). |

### 7. Scripts

| Critère | Niveau | Statut | Constat |
|---|---|---|---|
| 7.1 Chaque script est-il, si nécessaire, compatible avec les technologies d’assistance ? | A | NC | Composants vérifiés dans l'arbre d'accessibilité du navigateur (noms, rôles, états, déplacement du focus) mais PAS ENCORE avec un vrai lecteur d'écran (NVDA, VoiceOver, TalkBack) : compté non conforme tant que ce n'est pas fait. |
| 7.2 Pour chaque script ayant une alternative, cette alternative est-elle pertinente ? | A | C | Sans JavaScript : version papier du test (GAD-7 + barème), lien « Menu » vers la navigation du pied de page. |
| 7.3 Chaque script est-il contrôlable par le clavier et par tout dispositif de pointage (hors cas particuliers) ? | AA | C | Parcours complet au clavier sur 6 pages (téléphone et ordinateur), menu mobile fermé par Échap avec retour du focus. |
| 7.4 Pour chaque script qui initie un changement de contexte, l’utilisateur est-il averti ou en a-t-il le contrôle ? | A | C | Le passage à la question suivante du test est annoncé avant la première question ; aucun changement de contexte sans action. |
| 7.5 Dans chaque page web, les messages de statut sont-ils correctement restitués par les technologies d’assistance ? | AA | NC | Messages de statut en role=status / aria-live (test, minuteur, journal, recherche) mais restitution PAS ENCORE vérifiée avec un vrai lecteur d'écran : compté non conforme tant que ce n'est pas fait. |

### 8. Éléments obligatoires

| Critère | Niveau | Statut | Constat |
|---|---|---|---|
| 8.1 Chaque page web est-elle définie par un type de document ? | A | C | Doctype HTML5 sur chaque page. |
| 8.2 Pour chaque page web, le code source généré est-il valide selon le type de document spécifié ? | A | C | Validateur W3C (Nu) : 0 erreur de balisage sur les 33 pages (les messages restants concernent le CSS moderne, hors critère). |
| 8.3 Dans chaque page web, la langue par défaut est-elle présente ? | A | C | lang="fr" sur chaque page. |
| 8.4 Pour chaque page web ayant une langue par défaut, le code de langue est-il pertinent ? | A | C | Code de langue pertinent. |
| 8.5 Chaque page web a-t-elle un titre de page ? | A | C | Titre de page sur chaque page. |
| 8.6 Pour chaque page web ayant un titre de page, ce titre est-il pertinent ? | A | C | Titres de page pertinents et uniques. |
| 8.7 Dans chaque page web, chaque changement de langue est-il indiqué dans le code source (hors cas particuliers) ? | AA | C | Titres de sources en anglais et « Deep Relaxation » balisés lang="en" ; noms de revues et d'organismes = noms propres. |
| 8.8 Dans chaque page web, le code de langue de chaque changement de langue est-il valide et pertinent ? | AA | C | Code « en » valide. |
| 8.9 Dans chaque page web, les balises ne doivent pas être utilisées uniquement à des fins de présentation. Cette règle est-elle respectée ? | A | C | Balise <i> détournée en barre de progression remplacée par <span> (corrigé ce jour). |
| 8.10 Dans chaque page web, les changements du sens de lecture sont-ils signalés ? | A | NA | Aucun changement de sens de lecture. |

### 9. Structuration de l'information

| Critère | Niveau | Statut | Constat |
|---|---|---|---|
| 9.1 Dans chaque page web, l’information est-elle structurée par l’utilisation appropriée de titres ? | AA | C | Un seul h1 par page, aucun saut de niveau (18 pages relevées). |
| 9.2 Dans chaque page web, la structure du document est-elle cohérente (hors cas particuliers) ? | A | C | En-tête, navigation (nommée), contenu principal et pied de page balisés sur chaque page. |
| 9.3 Dans chaque page web, chaque liste est-elle correctement structurée ? | A | C | Listes balisées (ul/ol), y compris grilles de cartes ; aucune fausse liste relevée. |
| 9.4 Dans chaque page web, chaque citation est-elle correctement indiquée ? | A | C | Les deux vraies citations (HAS, mention de reproduction du GAD-7) balisées <q> (corrigé ce jour). |

### 10. Présentation de l'information

| Critère | Niveau | Statut | Constat |
|---|---|---|---|
| 10.1 Dans le site web, des feuilles de styles sont-elles utilisées pour contrôler la présentation de l’information ? | A | C | Présentation en CSS ; aucun attribut de présentation dans le HTML. |
| 10.2 Dans chaque page web, le contenu visible porteur d’information reste-t-il présent lorsque les feuilles de styles sont désactivées ? | A | C | Contenus générés en CSS uniquement décoratifs (séparateurs, flèches, coche doublée d'un état aria-pressed). |
| 10.3 Dans chaque page web, l’information reste-t-elle compréhensible lorsque les feuilles de styles sont désactivées ? | A | C | Ordre du code logique ; contenu compréhensible sans CSS. |
| 10.4 Dans chaque page web, le texte reste-t-il lisible lorsque la taille des caractères est augmentée jusqu’à 200 %, au moins (hors cas particuliers) ? | AA | C | Zoom 200 % (640 px de large) : aucun débordement ni texte coupé sur 31 pages. |
| 10.5 Dans chaque page web, les déclarations CSS de couleurs de fond d’élément et de police sont-elles correctement utilisées ? | AA | C | Couleurs de texte et de fond déclarées ensemble (corps de page et composants), dans les deux thèmes. |
| 10.6 Dans chaque page web, chaque lien dont la nature n’est pas évidente est-il visible par rapport au texte environnant ? | A | C | Liens du texte soulignés, y compris appels de sources (corrigé ce jour). |
| 10.7 Dans chaque page web, pour chaque élément recevant le focus, la prise de focus est-elle visible ? | AA | C | Contour de focus visible sur tous les éléments au clavier, y compris le champ date (corrigé ce jour), dans les deux thèmes. |
| 10.8 Pour chaque page web, les contenus cachés ont-ils vocation à être ignorés par les technologies d’assistance ? | A | C | Menu mobile fermé masqué (visibility hidden) ; aucun focus dans une zone masquée. |
| 10.9 Dans chaque page web, l’information ne doit pas être donnée uniquement par la forme, taille ou position. Cette règle est-elle respectée ? | A | C | Aucune consigne qui repose uniquement sur la forme, la taille ou la position (« ci-dessous » renvoie à l'ordre du texte). |
| 10.10 Dans chaque page web, l’information ne doit pas être donnée par la forme, taille ou position uniquement. Cette règle est-elle implémentée de façon pertinente ? | A | C | Idem 10.9. |
| 10.11 Pour chaque page web, les contenus peuvent-ils être présentés sans perte d’information ou de fonctionnalité et sans avoir recours soit à un défilement vertical pour une fenêtre ayant une hauteur de 256 px, soit à un défilement horizontal pour une fenêtre ayant une largeur de 320 px (hors cas particuliers) ? | AA | C | 320 px de large et téléphone en paysage : aucun défilement horizontal sur 31 pages. |
| 10.12 Dans chaque page web, les propriétés d’espacement du texte peuvent-elles être redéfinies par l’utilisateur sans perte de contenu ou de fonctionnalité (hors cas particuliers) ? | AA | C | Espacements du texte augmentés : aucun texte coupé ni débordement (11 pages, 2 tailles). |
| 10.13 Dans chaque page web, les contenus additionnels apparaissant à la prise de focus ou au survol d’un composant d’interface sont-ils contrôlables par l’utilisateur (hors cas particuliers) ? | AA | NA | Aucun contenu additionnel au survol ou au focus (hors infobulles natives du navigateur). |
| 10.14 Dans chaque page web, les contenus additionnels apparaissant via les styles CSS uniquement peuvent-ils être rendus visibles au clavier et par tout dispositif de pointage ? | A | NA | Aucun contenu révélé uniquement en CSS. |

### 11. Formulaires

| Critère | Niveau | Statut | Constat |
|---|---|---|---|
| 11.1 Chaque champ de formulaire a-t-il une étiquette ? | AA | C | Champs du journal et de la recherche étiquetés ; groupes de boutons nommés. |
| 11.2 Chaque étiquette associée à un champ de formulaire est-elle pertinente (hors cas particuliers) ? | AA | C | Étiquettes pertinentes. |
| 11.3 Dans chaque formulaire, chaque étiquette associée à un champ de formulaire ayant la même fonction et répétée plusieurs fois dans une même page ou dans un ensemble de pages est-elle cohérente ? | AA | NA | Pas de champ de même fonction répété. |
| 11.4 Dans chaque formulaire, chaque étiquette de champ et son champ associé sont-ils accolés (hors cas particuliers) ? | A | C | Étiquettes accolées à leur champ. |
| 11.5 Dans chaque formulaire, les champs de même nature sont-ils regroupés, si nécessaire ? | A | C | Échelles du journal et choix du minuteur regroupés (role=group). |
| 11.6 Dans chaque formulaire, chaque regroupement de champs de même nature a-t-il une légende ? | A | C | Chaque regroupement a une légende (aria-labelledby). |
| 11.7 Dans chaque formulaire, chaque légende associée à un regroupement de champs de même nature est-elle pertinente ? | A | C | Légendes pertinentes (« Mon humeur », « Durée de l'exercice »…). |
| 11.8 Dans chaque formulaire, les items de même nature d’une liste de choix sont-ils regroupés de manière pertinente ? | A | NA | Aucune liste de choix (select). |
| 11.9 Dans chaque formulaire, l’intitulé de chaque bouton est-il pertinent (hors cas particuliers) ? | A | C | Intitulés de boutons pertinents ; boutons à icône nommés. |
| 11.10 Dans chaque formulaire, le contrôle de saisie est-il utilisé de manière pertinente (hors cas particuliers) ? | A | C | Champs obligatoires du journal indiqués par écrit et par aria-required ; message d'erreur en role=status. |
| 11.11 Dans chaque formulaire, le contrôle de saisie est-il accompagné, si nécessaire, de suggestions facilitant la correction des erreurs de saisie ? | AA | C | Le message d'erreur nomme ce qui manque (« Il manque une note pour ton stress et ta nuit… ») (corrigé ce jour). |
| 11.12 Pour chaque formulaire qui modifie ou supprime des données, ou qui transmet des réponses à un test ou à un examen, ou dont la validation a des conséquences financières ou juridiques, les données saisies peuvent-elles être modifiées, mises à jour ou récupérées par l’utilisateur ? | AA | C | Journal : confirmation avant de remplacer une note et avant de tout effacer ; test : retour à la question précédente possible. |
| 11.13 La finalité d’un champ de saisie peut-elle être déduite pour faciliter le remplissage automatique des champs avec les données de l’utilisateur ? | AA | NA | Aucun champ de donnée personnelle (nom, e-mail…) sur le site. |

### 12. Navigation

| Critère | Niveau | Statut | Constat |
|---|---|---|---|
| 12.1 Chaque ensemble de pages dispose-t-il de deux systèmes de navigation différents, au moins (hors cas particuliers) ? | AA | C | Menu de navigation + moteur de recherche. |
| 12.2 Dans chaque ensemble de pages, le menu et les barres de navigation sont-ils toujours à la même place (hors cas particuliers) ? | AA | C | En-tête et menu identiques sur toutes les pages (menus harmonisés). |
| 12.3 La page « plan du site » est-elle pertinente ? | AA | NA | Pas de page « plan du site ». |
| 12.4 Dans chaque ensemble de pages, la page « plan du site » est-elle accessible à partir d’une fonctionnalité identique ? | AA | NA | Pas de page « plan du site ». |
| 12.5 Dans chaque ensemble de pages, le moteur de recherche est-il atteignable de manière identique ? | AA | C | Lien « Rechercher » au même endroit sur toutes les pages (pied de page, menu mobile). |
| 12.6 Les zones de regroupement de contenus présentes dans plusieurs pages web (zones d’ en-tête, de navigation principale, de contenu principal, de pied de page et de moteur de recherche ) peuvent-elles être atteintes ou évitées ? | A | C | Zones header / nav / main / footer balisées. |
| 12.7 Dans chaque page web, un lien d’évitement ou d’accès rapide à la zone de contenu principal est-il présent (hors cas particuliers) ? | AA | C | Lien « Aller au contenu » en premier sur chaque page, cible présente. |
| 12.8 Dans chaque page web, l’ ordre de tabulation est-il cohérent ? | A | C | Ordre de tabulation cohérent (parcours relevé). |
| 12.9 Dans chaque page web, la navigation ne doit pas contenir de piège au clavier. Cette règle est-elle respectée ? | A | C | Aucun piège au clavier (le parcours revient au premier élément). |
| 12.10 Dans chaque page web, les raccourcis clavier n’utilisant qu’une seule touche (lettre minuscule ou majuscule, ponctuation, chiffre ou symbole) sont-ils contrôlables par l’utilisateur ? | A | NA | Aucun raccourci clavier à une touche (seule la touche Échap ferme le menu). |
| 12.11 Dans chaque page web, les contenus additionnels apparaissant au survol, à la prise de focus ou à l’activation d’un composant d’interface sont-ils si nécessaire atteignables au clavier ? | A | C | Menu mobile et sections repliables atteignables au clavier. |

### 13. Consultation

| Critère | Niveau | Statut | Constat |
|---|---|---|---|
| 13.1 Pour chaque page web, l’utilisateur a-t-il le contrôle de chaque limite de temps modifiant le contenu (hors cas particuliers) ? | A | NA | Aucune limite de temps ni rafraîchissement automatique. |
| 13.2 Dans chaque page web, l’ouverture d’une nouvelle fenêtre ne doit pas être déclenchée sans action de l’utilisateur. Cette règle est-elle respectée ? | A | C | Seul le bouton Pinterest ouvre une nouvelle fenêtre, au clic, et le signale. |
| 13.3 Dans chaque page web, chaque document bureautique en téléchargement possède-t-il, si nécessaire, une version accessible (hors cas particuliers) ? | A | NA | Le site ne propose aucun document bureautique à télécharger ; les PDF cités en source sont des documents de tiers (voir la déclaration). |
| 13.4 Pour chaque document bureautique ayant une version accessible, cette version offre-t-elle la même information ? | A | NA | Idem 13.3. |
| 13.5 Dans chaque page web, chaque contenu cryptique (art ASCII, émoticône, syntaxe cryptique) a-t-il une alternative ? | A | NA | Aucun contenu cryptique (émoticône, art ASCII). |
| 13.6 Dans chaque page web, pour chaque contenu cryptique (art ASCII, émoticône, syntaxe cryptique) ayant une alternative, cette alternative est-elle pertinente ? | A | NA | Idem 13.5. |
| 13.7 Dans chaque page web, les changements brusques de luminosité ou les effets de flash sont-ils correctement utilisés ? | A | NA | Aucun flash ni changement brusque de luminosité. |
| 13.8 Dans chaque page web, chaque contenu en mouvement ou clignotant est-il contrôlable par l’utilisateur ? | A | C | Animations automatiques de l'accueil (aurore, réseau) arrêtables avec le bouton pause ; réduites si l'appareil le demande ; compteurs de moins de 5 s. |
| 13.9 Dans chaque page web, le contenu proposé est-il consultable quelle que soit l’orientation de l’écran (portrait ou paysage) (hors cas particuliers) ? | AA | C | Consultable en portrait et en paysage. |
| 13.10 Dans chaque page web, les fonctionnalités utilisables ou disponibles au moyen d’un geste complexe peuvent-elles être également disponibles au moyen d’un geste simple (hors cas particuliers) ? | A | NA | Aucun geste complexe. |
| 13.11 Dans chaque page web, les actions déclenchées au moyen d’un dispositif de pointage sur un point unique de l’écran peuvent-elles faire l’objet d’une annulation (hors cas particuliers) ? | A | C | Actions déclenchées au relâchement (clic), aucune action au simple appui. |
| 13.12 Dans chaque page web, les fonctionnalités qui impliquent un mouvement de l’appareil ou vers l’appareil peuvent-elles être satisfaites de manière alternative (hors cas particuliers) ? | A | NA | Aucune fonction liée au mouvement de l'appareil. |
