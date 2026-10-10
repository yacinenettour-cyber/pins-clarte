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
  /* Clochettes accordées comme dans les audios guidés (site/outils/audios_respiration.py) : sol pour inspirer,
     do pour expirer, mi (plus discret) pour retenir, do grave à la fin. [fréquence, durée, crête] ; crêtes réglées
     par rapport à la musique du minuteur (rapport affiché par audios_respiration.py). */
  var NOTES = { "in": [783.99, 3.2, 0.181], out: [523.25, 5.0, 0.170], haut: [659.25, 2.4, 0.124], bas: [659.25, 2.4, 0.124], fin: [261.63, 7.0, 0.158] };
  var MUSIQUE = "/audio/musique-detente-minuteur.mp3";
  var reduit = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var motif = "coherence", minutes = 3, son = "clochettes", enCours = false, debut = 0, raf = 0, phaseAffichee = -1, total = 0, verrou = null;
  var audio = null, jetonMusique = 0;
  var cercle = zone.querySelector(".ex-cercle"), etape = zone.querySelector(".ex-etape"), compte = zone.querySelector(".ex-compte"),
      barre = zone.querySelector(".ex-barre span"), bouton = zone.querySelector(".ex-lancer"), reste = zone.querySelector(".ex-reste"),
      rythme = zone.querySelector(".ex-rythme");

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

  /* ---- Sons (facultatifs) : clochettes jouées par le navigateur, musique de détente en option ---- */
  function preparerAudio() {
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    try { if (navigator.audioSession) navigator.audioSession.type = "playback"; } catch (e) {}  // iPhone : jouer même en mode silencieux
    if (!audio) audio = { ctx: new AC(), sortie: null, musique: null, t0: 0 };
    if (audio.ctx.state === "suspended") audio.ctx.resume().catch(function () {});
    return audio;
  }
  function rampe(param, valeur, dans) {
    var t = audio.ctx.currentTime;
    param.cancelScheduledValues(t); param.setValueAtTime(param.value, t); param.linearRampToValueAtTime(valeur, t + dans);
  }
  function clochette(ctx, sortie, t, note) {
    [[1, 1, 1.6], [2, 0.18, 2.6], [2.76, 0.12, 3.2]].forEach(function (p) {  // partiels de bol chantant, attaque de 10 ms
      var o = ctx.createOscillator(), g = ctx.createGain();
      o.frequency.value = note[0] * p[0];
      g.gain.setValueAtTime(0, t);
      g.gain.linearRampToValueAtTime(note[2] * p[1] / 1.3, t + 0.01);
      g.gain.setTargetAtTime(0, t + 0.01, note[1] / (p[2] * 2.2));
      o.connect(g); g.connect(sortie);
      o.start(t); o.stop(t + note[1]);
    });
  }
  /* Toutes les clochettes de la séance sont programmées au départ : elles restent à l'heure même si l'écran se met en veille. */
  function programmerSons(t0) {
    var ctx = audio.ctx, sortie = ctx.createGain(), phases = MOTIFS[motif].phases, cycle = dureeCycle(), n = Math.round(total / cycle);
    sortie.gain.value = son === "aucun" ? 0 : 1;
    sortie.connect(ctx.destination);
    for (var k = 0; k < n; k++) {
      for (var i = 0, acc = 0; i < phases.length; acc += phases[i][1], i++) clochette(ctx, sortie, t0 + k * cycle + acc, NOTES[phases[i][2]]);
    }
    clochette(ctx, sortie, t0 + total + 0.3, NOTES.fin);
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
    v.setValueAtTime(1, fin); v.linearRampToValueAtTime(0, fin + 6);  // fondu de sortie avec la clochette de fin
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
      /* Fin normale : la clochette de fin et le fondu de la musique sont déjà programmés. */
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
  function lancer() {
    enCours = true; total = dureeTotale(); phaseAffichee = -1;
    var DELAI = 0.12;  // laisse au son le temps de démarrer : clochettes et cercle partent ensemble
    debut = performance.now() + DELAI * 1000;
    if (preparerAudio()) {
      programmerSons(audio.ctx.currentTime + DELAI);
      if (son === "musique") demarrerMusique();
    }
    bouton.textContent = "Arrêter"; bouton.setAttribute("aria-pressed", "true");
    zone.classList.add("en-cours");
    garderEcranAllume();
    raf = requestAnimationFrame(boucle);
  }
  function arreter(fini) {
    enCours = false; cancelAnimationFrame(raf);
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
