# Texte de la méditation guidée pour le sommeil (tutoiement, aucune promesse de soin).
# Chaque élément : ("dire", texte, silence après en secondes)
#                  ("souffle", nombre de cycles, guidé par la voix ?)  -> cycles 4 s inspiration / 6 s expiration
#                  ("pause", secondes)
#                  ("titre", texte affiché en grand, secondes)  -> titre de partie, sans voix
SCRIPT = [
    ("pause", 14),
    ("dire", "Bonsoir.", 2.5),
    ("dire", "Cette méditation t'accompagne vers le sommeil, pendant une douzaine de minutes.", 2.5),
    ("dire", "Écoute-la seulement allongé, au calme, jamais en conduisant.", 3),
    ("dire", "Tu n'as rien à réussir. Il suffit d'écouter, et de te laisser porter.", 5),

    ("titre", "S'installer", 4),
    ("dire", "Installe-toi confortablement dans ton lit.", 3),
    ("dire", "Laisse ta tête s'enfoncer un peu dans l'oreiller.", 3),
    ("dire", "Tes bras reposent le long du corps, ou sur ton ventre, comme tu préfères.", 4),
    ("dire", "Si tu le souhaites, ferme doucement les yeux.", 5),
    ("dire", "Remarque simplement les points où ton corps touche le matelas.", 3),
    ("dire", "L'arrière de la tête. Les épaules. Le dos. Les jambes. Les talons.", 4),
    ("dire", "Le matelas te porte. Tu n'as plus besoin de te tenir.", 7),

    ("titre", "Respirer lentement", 4),
    ("dire", "Maintenant, porte ton attention sur ta respiration, sans chercher à la changer.", 4),
    ("dire", "Puis, petit à petit, ralentis-la. Suis le cercle à l'écran, si tes yeux sont encore ouverts.", 4),
    ("dire", "Tu inspires doucement par le nez pendant quatre temps, et tu expires lentement pendant six temps.", 3),
    ("souffle", 4, True),
    ("dire", "Continue à ton rythme. L'expiration est un peu plus longue que l'inspiration.", 2),
    ("souffle", 6, False),
    ("dire", "Très bien. Laisse maintenant ta respiration redevenir naturelle.", 7),

    ("titre", "Détendre le corps", 4),
    ("dire", "Nous allons parcourir le corps, lentement, de la tête jusqu'aux pieds.", 4),
    ("dire", "Commence par ton front. Laisse-le devenir lisse, comme une eau calme.", 6),
    ("dire", "Tes paupières deviennent lourdes. Ta mâchoire se desserre. Ta langue se pose au fond de la bouche.", 7),
    ("dire", "Tes épaules descendent un peu, loin des oreilles.", 6),
    ("dire", "La détente coule dans tes bras, jusqu'au bout des doigts.", 7),
    ("dire", "Ta poitrine se soulève et redescend, toute seule.", 6),
    ("dire", "Ton ventre est souple. Rien à retenir.", 7),
    ("dire", "Ton dos s'étale sur le matelas, vertèbre après vertèbre.", 7),
    ("dire", "Tes hanches, tes cuisses, tes genoux deviennent lourds.", 6),
    ("dire", "Et la détente descend jusqu'à tes mollets, tes chevilles, tes pieds.", 8),
    ("dire", "Tout ton corps est posé. Lourd. Tranquille.", 10),

    ("titre", "Laisser passer les pensées", 4),
    ("dire", "Il est possible que des pensées arrivent. C'est normal.", 4),
    ("dire", "Une chose à faire demain. Un souvenir de la journée. Une inquiétude.", 4),
    ("dire", "Tu n'as pas besoin de les chasser, ni de les régler maintenant.", 4),
    ("dire", "Imagine que chaque pensée est un petit nuage dans un ciel de nuit.", 5),
    ("dire", "Tu le regardes arriver… puis s'éloigner, lentement, poussé par le vent.", 8),
    ("dire", "Et si une pensée revient, ce n'est pas grave. Tu la laisses repartir, une fois encore.", 10),
    ("dire", "Elle sera encore là demain, si elle est importante. Cette nuit, tu peux la poser.", 10),

    ("titre", "Le ciel étoilé", 4),
    ("dire", "Imagine maintenant un grand ciel étoilé, au-dessus de toi.", 5),
    ("dire", "L'air est doux. Tout est silencieux.", 6),
    ("dire", "À chaque expiration, une étoile s'allume, un peu plus loin.", 7),
    ("dire", "Tu n'as rien à faire. Seulement regarder, et respirer.", 10),
    ("dire", "Chaque souffle t'emmène un peu plus profondément dans le calme.", 12),
    ("dire", "Tu es en sécurité. Tu peux te reposer.", 14),

    ("titre", "Glisser vers le sommeil", 4),
    ("dire", "Bientôt, ma voix va se taire. La musique va continuer encore un moment.", 5),
    ("dire", "Si tu dors déjà, continue simplement de dormir.", 5),
    ("dire", "Et si tu es encore éveillé, ce n'est pas un problème. Le repos compte aussi.", 6),
    ("dire", "Laisse-toi glisser, doucement, vers le sommeil.", 8),
    ("dire", "Bonne nuit.", 4),
    ("pause", 100),
]
