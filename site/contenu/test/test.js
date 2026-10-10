/* Test stress et anxiété : GAD-7 (Spitzer et al., 2006 ; version française du Département de médecine de famille
   de l'Université de Montréal, reproduite mot pour mot) + 6 questions d'orientation propres à Clarté Mentale.
   Tout se calcule dans le navigateur : aucune réponse n'est envoyée ni enregistrée. */
(function () {
  var racine = document.getElementById("test-stress");
  if (!racine) return;
  var B = "{{B}}";
  /*@DONNEES*/
  var reduit = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var ecran = document.getElementById("test-ecran"), compteur = document.getElementById("test-compteur"), barre = document.getElementById("test-barre");
  var ECHELLE = ["Jamais", "Plusieurs jours", "Plus de la moitié des jours", "Presque tous les jours"];
  var CONSIGNE_GAD = "Au cours des 14 derniers jours, à quelle fréquence avez-vous été dérangé(e) par les problèmes suivants ?";
  var CONSIGNE_PROFIL = "Ces 14 derniers jours, à quelle fréquence est-ce que c'était ton cas ?";
  var QUESTIONS = [
    { partie: 1, texte: "Sentiment de nervosité, d'anxiété ou de tension" },
    { partie: 1, texte: "Incapable d'arrêter de vous inquiéter ou de contrôler vos inquiétudes" },
    { partie: 1, texte: "Inquiétudes excessives à propos de tout et de rien" },
    { partie: 1, texte: "Difficulté à se détendre" },
    { partie: 1, texte: "Agitation telle qu'il est difficile de rester tranquille" },
    { partie: 1, texte: "Devenir facilement contrarié(e) ou irritable" },
    { partie: 1, texte: "Avoir peur que quelque chose d'épouvantable puisse arriver" },
    { partie: 2, axe: "nuit", texte: "Au lit, tes pensées tournent en boucle et retardent ton endormissement" },
    { partie: 2, axe: "nuit", texte: "Tu te réveilles la nuit ou très tôt le matin, sans arriver à te rendormir" },
    { partie: 2, axe: "travail", texte: "Ton travail (ou tes études) te vide de ton énergie, même après un jour de repos" },
    { partie: 2, axe: "travail", texte: "Tu prends de la distance avec ton travail : moins d'envie, plus de cynisme ou de négativité à son égard" },
    { partie: 2, axe: "corps", texte: "Ton corps reste tendu : mâchoire serrée, épaules ou nuque nouées" },
    { partie: 2, axe: "corps", texte: "Dans les moments de stress, ton ventre se noue ou ton cœur s'accélère" }
  ];
  var NB = QUESTIONS.length;

  /* Seuils du manuel officiel PHQ/GAD-7 : 5, 10 et 15 = symptômes légers, modérés, sévères ;
     10 ou plus = seuil recommandé pour une évaluation par un professionnel. */
  function niveau(score) {
    if (score >= 15) return { cle: "severe", nom: "Symptômes d'anxiété sévères", couleur: "var(--t-severe)",
      texte: "Ton score atteint 15 ou plus : c'est le seuil des symptômes sévères, que les auteurs du questionnaire considèrent comme un signal d'alerte." };
    if (score >= 10) return { cle: "modere", nom: "Symptômes d'anxiété modérés", couleur: "var(--t-modere)",
      texte: "Ton score atteint 10 ou plus : c'est le seuil à partir duquel les auteurs du questionnaire recommandent d'en parler à un professionnel." };
    if (score >= 5) return { cle: "leger", nom: "Symptômes d'anxiété légers", couleur: "var(--t-moyen)",
      texte: "Ton score se situe entre 5 et 9 : des symptômes d'anxiété légers ces deux dernières semaines, fréquents en période chargée." };
    return { cle: "faible", nom: "Peu de symptômes d'anxiété", couleur: "var(--t-leger)",
      texte: "Ton score est sous le premier seuil du questionnaire (5) : tes réponses ne montrent pas de symptômes d'anxiété marqués ces deux dernières semaines." };
  }

  var PROFILS = {
    nuit: {
      nom: "Nuits et ruminations",
      resume: "Ton stress se manifeste surtout la nuit : les pensées tournent au moment de dormir, ou te réveillent avant l'heure.",
      explication: "Quand l'axe du stress reste actif le soir, le sommeil devient plus fragile. Et le manque de sommeil entretient le stress : une nuit écourtée fait monter le cortisol du lendemain soir de 37 % (Université de Chicago, 1997). L'objectif est de casser ce cercle, soir après soir.",
      gestes: [
        "Avant d'éteindre, prends 5 minutes pour écrire la liste précise de ce que tu dois faire demain : dans une étude de l'Université Baylor (2018), ceux qui écrivaient leurs tâches à venir s'endormaient plus vite que ceux qui notaient ce qu'ils avaient déjà fait.",
        "Au lit, ne regarde pas l'heure : surveiller le réveil augmente l'inquiétude et retarde le sommeil (King's College de Londres, 2007).",
        "Réveillé(e) depuis plus de 20 minutes ? L'Institut national du sommeil et de la vigilance conseille alors de te lever et de faire autre chose."
      ],
      articles: ["ruminations-le-soir", "reveil-4h-du-matin", "cortisol-et-sommeil"],
      guide: "sommeil"
    },
    travail: {
      nom: "Épuisement lié au travail",
      resume: "Tes réponses évoquent une fatigue et une prise de distance liées à ton travail.",
      explication: "L'Organisation mondiale de la santé décrit le burn-out comme un phénomène lié au travail, qui résulte d'un stress chronique au travail qui n'a pas été correctement géré. Il a trois dimensions : l'épuisement, la prise de distance ou le cynisme envers son travail, et une baisse de l'efficacité professionnelle. Ce test ne peut pas dire si c'est ton cas, mais ces signes méritent d'être pris au sérieux.",
      gestes: [
        "Parles-en à ton médecin traitant : il peut faire le point avec toi et, si besoin, t'orienter.",
        "Si tu es salarié(e), tu peux aussi contacter le médecin du travail : selon l'INRS, il évalue le besoin d'une prise en charge et peut envisager un aménagement de poste.",
        "Chaque soir, 5 minutes de respiration lente pour marquer la fin de la journée de travail : inspire 4 secondes, expire 6 secondes. Autour de 6 respirations par minute, la variabilité cardiaque liée au nerf vague augmente (synthèse de 223 études, 2022). <a href=\"" + B + "/respiration-guidee/\">Écouter l'audio guidé</a>"
      ],
      articles: ["signes-du-burn-out", "charge-mentale", "calmer-son-systeme-nerveux"],
      guide: "sommeil", complement: true, pont: "Si le travail te suit jusqu'au lit"
    },
    corps: {
      nom: "Corps en alerte",
      resume: "Ton stress se loge dans le corps : tensions, ventre noué, cœur qui s'accélère.",
      explication: "Face au stress, le système nerveux autonome prépare le corps à réagir : le cœur accélère, les muscles se tendent. Quand cette alerte dure, le corps a du mal à revenir au repos. Les gestes qui sollicitent le nerf vague, principal nerf de la branche qui ramène le corps au calme, l'aident à redescendre.",
      gestes: [
        "Deux fois par jour, 5 minutes de respiration lente : inspire 4 secondes, expire 6 secondes. Autour de 6 respirations par minute, la variabilité cardiaque liée au nerf vague augmente (synthèse de 223 études, Université allemande du sport de Cologne, 2022). <a href=\"" + B + "/respiration-guidee/\">Écouter l'audio guidé</a>",
        "Le soir, essaie la relaxation musculaire progressive : contracter un groupe de muscles quelques secondes, puis le relâcher. Une revue de 46 publications (2024) conclut qu'elle aide à réduire le stress et l'anxiété.",
        "Bouge chaque jour, même en marchant : une synthèse de 97 revues (Université d'Australie-Méridionale, 2023) montre que l'activité physique réduit l'anxiété et la détresse psychologique."
      ],
      articles: ["calmer-son-systeme-nerveux", "nerf-vague", "baisser-son-cortisol-naturellement"],
      guide: "sommeil", pont: "Si cette tension te suit jusqu'au lit",
      prudence: "Une douleur dans la poitrine, un essoufflement inhabituel ou un malaise ne doivent pas être mis d'office sur le compte du stress : appelle le 15 ou le 112."
    },
    equilibre: {
      nom: "Pas d'axe dominant",
      resume: "Tes réponses ne font pas ressortir de domaine plus touché que les autres ces deux dernières semaines.",
      explication: "Ton sommeil, ton travail et ton corps ne montrent pas de signal marqué dans ce test. Le plus utile est de garder les repères qui aident le cortisol à suivre son rythme naturel : haut le matin, bas le soir.",
      gestes: [
        "Garde des horaires de coucher et de lever réguliers, même le week-end, comme le recommande l'Assurance maladie.",
        "Quand la pression monte, 5 minutes de respiration lente (inspire 4 secondes, expire 6 secondes) aident le corps à redescendre (synthèse de 223 études, 2022).",
        "Refais ce test dans un mois, ou après une période chargée, pour suivre ton évolution."
      ],
      articles: ["routine-du-soir-anti-stress", "cortisol-hormone-du-stress", "baisser-son-cortisol-naturellement"],
      guide: "sommeil"
    }
  };
  var ORDRE_AXES = ["travail", "nuit", "corps"];

  var reponses = [], etape = 0, aRepondu = false;

  /* Typographie française : espace insécable avant « : ; ? ! » et dans les guillemets. */
  function typo(html) { return html.replace(/ ([:;?!»])/g, "\u00a0$1").replace(/« /g, "«\u00a0"); }

  function lien(slug) {
    var a = ARTICLES[slug];
    return a ? '<li><a href="' + B + '/' + slug + '/">' + a + '</a></li>' : "";
  }
  function utm(url, contenu) {
    return url + "?utm_source=site&utm_medium=test&utm_campaign=test-stress&utm_content=" + contenu;
  }

  function afficherQuestion() {
    var q = QUESTIONS[etape];
    compteur.textContent = "Question " + (etape + 1) + " sur " + NB;
    barre.style.width = ((etape + 1) / NB * 100) + "%";
    var html = '<div class="etape">' +
      '<p class="test-partie">' + (q.partie === 1 ? "Partie 1 sur 2 · Questionnaire GAD-7" : "Partie 2 sur 2 · Ton profil") + '</p>' +
      '<p class="test-consigne">' + (q.partie === 1 ? CONSIGNE_GAD : CONSIGNE_PROFIL) + '</p>' +
      (etape === 0 ? '<p class="test-aide">Chaque réponse fait passer à la question suivante ; tu pourras revenir en arrière.</p>' : '') +
      '<h2 tabindex="-1" id="test-question">' + q.texte + '</h2><div class="choix" role="group" aria-labelledby="test-question">';
    ECHELLE.forEach(function (libelle, i) {
      html += '<button class="option" type="button" data-i="' + i + '" aria-pressed="' + (reponses[etape] === i) + '"><span class="puce" aria-hidden="true">' + i + '</span><span>' + libelle + '</span></button>';
    });
    html += '</div>' + (etape > 0 ? '<button class="retour" type="button" id="test-retour">← Question précédente</button>' : '<p class="test-prive">Tes réponses restent sur ton appareil : rien n\'est envoyé ni enregistré.</p>') + '</div>';
    ecran.innerHTML = typo(html);
    if (aRepondu) document.getElementById("test-question").focus({ preventScroll: true });
    ecran.querySelectorAll(".option").forEach(function (b) {
      b.addEventListener("click", function () {
        reponses[etape] = Number(b.dataset.i);
        aRepondu = true;
        b.setAttribute("aria-pressed", "true");
        setTimeout(function () { if (etape < NB - 1) { etape++; afficherQuestion(); } else { afficherResultat(); } }, reduit ? 0 : 220);
      });
    });
    var retour = document.getElementById("test-retour");
    if (retour) retour.addEventListener("click", function () { etape--; afficherQuestion(); });
  }

  /* Une seule offre (consigne du 10/10/2026) : le guide sommeil, relié aux e-mails ; jamais la formation dans le résultat. */
  function blocOffre(cleProfil, p, n) {
    if (n.cle === "severe") return "";
    var g = GUIDES[p.guide];
    if (!g) return "";
    var contenu = "profil-" + cleProfil + "-" + n.cle;
    var detail = g.rappel.split(" : ").slice(1).join(" : ");
    var texte = p.pont && detail
      ? p.pont + " : <strong>" + g.titre + "</strong> (" + g.type.toLowerCase() + "), " + detail
      : "<strong>" + g.titre + "</strong> (" + g.type.toLowerCase() + "), " + g.rappel.charAt(0).toLowerCase() + g.rappel.slice(1);
    var avant = p.complement || n.cle === "modere"
      ? "<p><strong>En complément, jamais à la place d'un avis médical.</strong> " + texte + "</p>"
      : "<p>" + texte + "</p>";
    return '<div class="deblocage">' + avant +
      '<a class="test-cta" href="' + utm(g.url, contenu) + '">' + g.bouton + ' <span aria-hidden="true">→</span></a>' +
      '<small>Gratuit. Tu laisses ton e-mail sur une page sécurisée (systeme.io) et tu reçois le guide tout de suite, puis quelques conseils pour tes soirées. Désinscription en un clic.</small></div>';
  }

  function afficherResultat() {
    var gad = 0, axes = { nuit: 0, travail: 0, corps: 0 };
    QUESTIONS.forEach(function (q, i) { if (q.partie === 1) gad += reponses[i]; else axes[q.axe] += reponses[i]; });
    var n = niveau(gad);
    var tries = ORDRE_AXES.slice().sort(function (a, b) { return axes[b] - axes[a]; });
    var cle = axes[tries[0]] >= 3 ? tries[0] : "equilibre";
    var second = cle !== "equilibre" && axes[tries[1]] >= 3 ? tries[1] : null;
    var p = PROFILS[cle];
    var date = new Date().toLocaleDateString("fr-FR");

    var conseilMedical = n.cle === "severe"
      ? "<p><strong>Prends rendez-vous rapidement avec ton médecin traitant, dans les prochains jours.</strong> Montre-lui ce score : ce questionnaire ne pose pas de diagnostic, mais il l'aidera à faire le point avec toi.</p>"
      : n.cle === "modere"
      ? "<p><strong>Prends rendez-vous avec ton médecin traitant pour en parler.</strong> Ce questionnaire ne pose pas de diagnostic : seul un professionnel peut le faire, et des solutions efficaces existent.</p>"
      : "<p>Si tes symptômes durent, s'aggravent ou te gênent au quotidien, parles-en à ton médecin traitant : il est difficile de juger seul de son état.</p>";

    compteur.textContent = "Ton résultat";
    barre.style.width = "100%";
    var circ = 2 * Math.PI * 60;
    var html =
      '<div class="resultat">' +
        '<div class="jauge-ligne">' +
          '<div class="jauge"><svg viewBox="0 0 140 140" aria-hidden="true"><circle cx="70" cy="70" r="60" fill="none" stroke="rgba(223,213,198,.1)" stroke-width="10"/><circle id="test-arc" cx="70" cy="70" r="60" fill="none" stroke="' + n.couleur + '" stroke-width="10" stroke-linecap="round" stroke-dasharray="' + circ.toFixed(1) + '" stroke-dashoffset="' + circ.toFixed(1) + '" style="transition: stroke-dashoffset 1.2s cubic-bezier(.2,.8,.2,1)"/></svg>' +
            '<div class="valeur"><div><b id="test-chiffre">' + (reduit ? gad : 0) + '</b><small>sur 21</small></div></div></div>' +
          '<div class="jauge-texte"><span class="niveau" style="color:' + n.couleur + '">' + n.nom + '</span><h2>Ton score au GAD-7 : ' + gad + ' sur 21</h2><p>' + n.texte + '</p></div>' +
        '</div>' +
        '<div class="test-bloc' + (n.cle === "severe" || n.cle === "modere" ? " test-alerte" : "") + '">' + conseilMedical +
          '<p>Note ton score pour en parler : <strong>GAD-7 = ' + gad + '/21, le ' + date + '</strong>.</p></div>' +
        '<div class="test-bloc test-profil"><p class="test-etiquette">Ton profil</p><h3>' + p.nom + '</h3><p>' + p.resume + '</p><p>' + p.explication + '</p></div>' +
        '<div><p class="test-etiquette" style="margin-bottom:12px">Tes 3 priorités</p><ol class="priorites">' +
          p.gestes.map(function (g, i) { return '<li><b>' + (i + 1) + '</b><span>' + g + '</span></li>'; }).join("") +
        '</ol></div>' +
        (p.prudence ? '<p class="test-prive">' + p.prudence + '</p>' : '') +
        '<div class="test-bloc"><p class="test-etiquette">À lire pour toi</p><ul class="test-liens">' + p.articles.map(lien).join("") + '</ul></div>' +
        (second ? '<div class="test-bloc"><p class="test-etiquette">Ton deuxième axe</p><h3>' + PROFILS[second].nom + '</h3><p>' + PROFILS[second].resume + '</p><ul class="test-liens">' + PROFILS[second].articles.slice(0, 2).map(lien).join("") + '</ul></div>' : '') +
        blocOffre(cle, p, n) +
        '<div class="test-bloc"><p>Si tu as des pensées suicidaires, appelle le <strong>3114</strong> (gratuit, 24 h/24 et 7 j/7). En cas d\'urgence, appelle le <strong>15</strong> ou le <strong>112</strong>.</p></div>' +
        '<div class="test-pied"><button class="retour" type="button" id="test-refaire">↺ Refaire le test</button><a href="' + B + '/test-stress-anxiete/#comment-fonctionne-ce-test">Comment fonctionne ce test</a></div>' +
        '<p class="test-prive">Repère, pas un diagnostic. Tes réponses n\'ont été ni envoyées ni enregistrées.</p>' +
      '</div>';
    ecran.innerHTML = typo(html);
    var haut = racine.getBoundingClientRect().top;
    if (haut < 0) racine.scrollIntoView({ block: "start", behavior: reduit ? "auto" : "smooth" });
    var arc = document.getElementById("test-arc"), chiffre = document.getElementById("test-chiffre");
    requestAnimationFrame(function () { requestAnimationFrame(function () { arc.style.strokeDashoffset = (circ * (1 - gad / 21)).toFixed(1); }); });
    if (!reduit) {
      var debut = performance.now();
      (function compter(t) { var k = Math.min(1, (t - debut) / 1200); chiffre.textContent = Math.round(gad * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(compter); })(debut);
    }
    document.getElementById("test-refaire").addEventListener("click", function () { reponses = []; etape = 0; afficherQuestion(); });
  }

  afficherQuestion();
})();
