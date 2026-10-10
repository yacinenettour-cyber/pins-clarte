/* Minuteur des exercices de respiration (page /exercices-respiration/). Rien n'est envoyé ni enregistré. */
(function () {
  "use strict";
  var zone = document.getElementById("exercice");
  if (!zone) return;
  var MOTIFS = {
    coherence: { rythme: "Inspire 5 s · expire 5 s", phases: [["Inspire", 5, "in"], ["Expire", 5, "out"]] },
    carree: { rythme: "Inspire 4 s · retiens 4 s · expire 4 s · retiens 4 s", phases: [["Inspire", 4, "in"], ["Retiens", 4, "haut"], ["Expire", 4, "out"], ["Retiens", 4, "bas"]] },
    "478": { rythme: "Inspire 4 s · retiens 7 s · expire 8 s", phases: [["Inspire", 4, "in"], ["Retiens", 7, "haut"], ["Expire", 8, "out"]] }
  };
  /* Vrais bols chantants (enregistrements CC0, site/sources-audio/bols/) réunis dans un seul fichier par
     site/outils/audios_respiration.py ; position et durée de chacun injectées à la construction (bols-minuteur.json). */
  var BOLS = /*@BOLS*/null;
  var REPERE = { "in": "inspire", out: "expire", haut: "retiens", bas: "retiens" };
  var MUSIQUE = "/audio/musique-detente-minuteur.mp3";
  var reduit = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var motif = "coherence", minutes = 3, son = "bols", enCours = false, debut = 0, raf = 0, phaseAffichee = -1, total = 0, verrou = null;
  var audio = null, jetonMusique = 0;
  var cercle = zone.querySelector(".ex-cercle"), etape = zone.querySelector(".ex-etape"), compte = zone.querySelector(".ex-compte"),
      barre = zone.querySelector(".ex-barre span"), bouton = zone.querySelector(".ex-lancer"), reste = zone.querySelector(".ex-reste"),
      rythme = zone.querySelector(".ex-rythme"), statut = zone.querySelector(".ex-statut");

  function dureeCycle() { return MOTIFS[motif].phases.reduce(function (a, p) { return a + p[1]; }, 0); }
  /* Durée arrondie à un nombre entier de cycles : l'exercice se termine toujours sur une expiration complète. */
  function dureeTotale() { var c = dureeCycle(); return Math.max(1, Math.round(minutes * 60 / c)) * c; }
  function mmss(s) { s = Math.max(0, Math.ceil(s)); return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); }
  function adoucir(x) { return 0.5 - 0.5 * Math.cos(Math.PI * x); }
  function infos() { rythme.textContent = MOTIFS[motif].rythme; reste.textContent = mmss(dureeTotale()); }

  function choisir(groupe, bouton) {
    zone.querySelectorAll("[data-" + groupe + "]").forEach(function (b) { b.setAttribute("aria-pressed", String(b === bouton)); });
  }
  zone.querySelectorAll("[data-motif]").forEach(function (b) {
    b.addEventListener("click", function () { if (enCours) arreter(false); motif = b.dataset.motif; choisir("motif", b); infos(); });
  });
  zone.querySelectorAll("[data-minutes]").forEach(function (b) {
    b.addEventListener("click", function () { if (enCours) arreter(false); minutes = Number(b.dataset.minutes); choisir("minutes", b); infos(); });
  });

  /* ---- Sons (facultatifs) : bols chantants, musique de détente en option ---- */
  function preparerAudio() {
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    try { if (navigator.audioSession) navigator.audioSession.type = "playback"; } catch (e) {}  // iPhone : jouer même en mode silencieux
    if (!audio) audio = { ctx: new AC(), sortie: null, musique: null, t0: 0, bols: null, decodage: null };
    if (audio.ctx.state === "suspended") audio.ctx.resume().catch(function () {});
    return audio;
  }
  function rampe(param, valeur, dans) {
    var t = audio.ctx.currentTime;
    param.cancelScheduledValues(t); param.setValueAtTime(param.value, t); param.linearRampToValueAtTime(valeur, t + dans);
  }
  /* Fichier des bols : téléchargé dès que le minuteur apparaît à l'écran (sauf en mode « économie de données »),
     décodé au premier lancement. */
  var telechargement = null;
  function telechargerBols() {
    if (!telechargement && BOLS && window.fetch) {
      telechargement = fetch(BOLS.fichier).then(function (r) { if (!r.ok) throw new Error(r.status); return r.arrayBuffer(); });
      telechargement.catch(function () { telechargement = null; });
    }
    return telechargement || Promise.reject(new Error("bols"));
  }
  if (window.IntersectionObserver && !(navigator.connection && navigator.connection.saveData)) {
    var guetteur = new IntersectionObserver(function (vus) {
      if (vus[0].isIntersecting) { guetteur.disconnect(); telechargerBols().catch(function () {}); }
    }, { rootMargin: "300px" });
    guetteur.observe(zone);
  }
  function preparerBols() {
    if (audio.bols) return Promise.resolve();
    if (!audio.decodage) {
      audio.decodage = telechargerBols().then(function (donnees) {
        return new Promise(function (ok, ko) {
          var p = audio.ctx.decodeAudioData(donnees, ok, ko);  // forme à rappels : anciens Safari
          if (p && p.then) p.then(ok, ko);
        });
      }).then(function (tampon) { audio.bols = tampon; });
      audio.decodage.catch(function () { audio.decodage = null; });
    }
    return audio.decodage;
  }
  function bol(ctx, sortie, t, nom) {
    var s = BOLS.sons[nom], src = ctx.createBufferSource();
    src.buffer = audio.bols; src.connect(sortie);
    src.start(t - BOLS.preroule, s[0], s[1]);  // le son commence 10 ms avant la frappe : la frappe tombe à l'heure
  }
  /* Tous les bols de la séance sont programmés au départ : ils restent à l'heure même si l'écran se met en veille. */
  function programmerSons(t0) {
    var ctx = audio.ctx, sortie = ctx.createGain(), phases = MOTIFS[motif].phases, cycle = dureeCycle(), n = Math.round(total / cycle);
    sortie.gain.value = son === "aucun" ? 0 : 1;
    sortie.connect(ctx.destination);
    for (var k = 0; k < n; k++) {
      for (var i = 0, acc = 0; i < phases.length; acc += phases[i][1], i++) bol(ctx, sortie, t0 + k * cycle + acc, REPERE[phases[i][2]]);
    }
    bol(ctx, sortie, t0 + total + 0.3, "fin");
    audio.sortie = sortie; audio.t0 = t0;
  }
  function demarrerMusique() {
    var ctx = audio.ctx, maintenant = ctx.currentTime, fin = audio.t0 + total, ecoule = Math.max(0, maintenant - audio.t0);
    if (fin - maintenant < 8) return;  // trop près de la fin pour lancer la musique
    if (!audio.musique) {
      var el = document.createElement("audio");
      el.src = MUSIQUE; el.preload = "none";
      var g = ctx.createGain();
      ctx.createMediaElementSource(el).connect(g); g.connect(ctx.destination);
      audio.musique = { el: el, gain: g };
    }
    var m = audio.musique, v = m.gain.gain;
    jetonMusique++;  // annule une mise en pause en attente
    v.cancelScheduledValues(maintenant);
    v.setValueAtTime(0, maintenant); v.linearRampToValueAtTime(1, maintenant + 4);
    v.setValueAtTime(1, fin); v.linearRampToValueAtTime(0, fin + 6);  // fondu de sortie avec le bol de fin
    try { m.el.currentTime = ecoule; } catch (e) {}
    var lecture = m.el.play();
    if (lecture && lecture.catch) lecture.catch(function () {});
  }
  function pauseMusiquePlusTard(ms) {
    var j = ++jetonMusique;
    setTimeout(function () { if (j === jetonMusique && audio.musique) audio.musique.el.pause(); }, ms);
  }
  function arreterMusique(dans) {
    if (!audio || !audio.musique) return;
    rampe(audio.musique.gain.gain, 0, dans);
    pauseMusiquePlusTard(dans * 1000 + 100);
  }
  function couperSons(fini) {
    if (!audio || !audio.sortie) return;
    var sortie = audio.sortie;
    audio.sortie = null;
    if (fini) {
      /* Fin normale : le bol de fin et le fondu de la musique sont déjà programmés. */
      setTimeout(function () { sortie.disconnect(); }, 8000);
      if (audio.musique) pauseMusiquePlusTard(7000);
    } else {
      rampe(sortie.gain, 0, 0.3);
      setTimeout(function () { sortie.disconnect(); }, 500);
      arreterMusique(1.2);
    }
  }
  zone.querySelectorAll("[data-son]").forEach(function (b) {
    b.addEventListener("click", function () {
      son = b.dataset.son; choisir("son", b);
      if (!enCours || !audio || !audio.sortie) return;
      rampe(audio.sortie.gain, son === "aucun" ? 0 : 1, 0.3);
      if (son === "musique") demarrerMusique(); else arreterMusique(1.5);
    });
  });

  /* ---- Minuteur ---- */
  function boucle(t) {
    var e = (t - debut) / 1000;
    if (e < 0) { raf = requestAnimationFrame(boucle); return; }
    if (e >= total) { arreter(true); return; }
    var phases = MOTIFS[motif].phases, c = e % dureeCycle(), acc = 0, i = 0;
    while (i < phases.length - 1 && c >= acc + phases[i][1]) { acc += phases[i][1]; i++; }
    var p = phases[i], dans = c - acc, f = Math.min(1, dans / p[1]);
    var echelle = p[2] === "in" ? 0.55 + 0.45 * adoucir(f) : p[2] === "out" ? 1 - 0.45 * adoucir(f) : p[2] === "haut" ? 1 : 0.55;
    if (!reduit) cercle.style.transform = "scale(" + echelle.toFixed(3) + ")";
    cercle.dataset.phase = p[2];
    if (i !== phaseAffichee) { phaseAffichee = i; etape.textContent = p[0]; }
    compte.textContent = Math.ceil(p[1] - dans);
    barre.style.width = (e / total * 100).toFixed(2) + "%";
    reste.textContent = mmss(total - e);
    raf = requestAnimationFrame(boucle);
  }
  function garderEcranAllume() {
    if (navigator.wakeLock && navigator.wakeLock.request) {
      navigator.wakeLock.request("screen").then(function (v) { verrou = v; }).catch(function () {});
    }
  }
  var lancement = 0;
  function lancer() {
    enCours = true; total = dureeTotale(); phaseAffichee = -1;
    var n = ++lancement;
    statut.hidden = true;
    bouton.textContent = "Arrêter"; bouton.setAttribute("aria-pressed", "true");
    zone.classList.add("en-cours");
    garderEcranAllume();
    function partir(avecSon) {
      if (n !== lancement || !enCours) return;
      var DELAI = 0.12;  // laisse au son le temps de démarrer : bols et cercle partent ensemble
      debut = performance.now() + DELAI * 1000;
      if (avecSon) {
        programmerSons(audio.ctx.currentTime + DELAI);
        if (son === "musique") demarrerMusique();
      }
      raf = requestAnimationFrame(boucle);
    }
    if (!preparerAudio() || !BOLS) { partir(false); return; }
    if (audio.bols) { partir(true); return; }
    if (son === "aucun") { partir(false); preparerBols().catch(function () {}); return; }  // pas d'attente sans son
    etape.textContent = "Préparation des sons…";
    /* Sons pas encore prêts : on attend 4 s au plus, sinon l'exercice démarre sans eux. */
    function sansSon() {
      clearTimeout(attente);
      if (n !== lancement || !enCours) return;
      statut.textContent = "Les sons n'ont pas pu être chargés : l'exercice continue sans son.";
      statut.hidden = false;
      partir(false);
    }
    var attente = setTimeout(sansSon, 4000);
    preparerBols().then(function () { clearTimeout(attente); partir(true); }, sansSon);
  }
  function arreter(fini) {
    enCours = false; lancement++; cancelAnimationFrame(raf);
    couperSons(fini);
    bouton.textContent = fini ? "Recommencer" : "Commencer"; bouton.setAttribute("aria-pressed", "false");
    zone.classList.remove("en-cours");
    cercle.style.transform = ""; cercle.dataset.phase = "";
    etape.textContent = fini ? "Terminé. Reste un instant immobile." : "Prêt";
    compte.textContent = ""; barre.style.width = fini ? "100%" : "0%";
    reste.textContent = fini ? "0:00" : mmss(dureeTotale());
    if (verrou) { verrou.release().catch(function () {}); verrou = null; }
  }
  bouton.addEventListener("click", function () { if (enCours) arreter(false); else lancer(); });
  document.addEventListener("visibilitychange", function () { if (!document.hidden && enCours) garderEcranAllume(); });
  infos();
})();
