/* Minuteur visuel des exercices de respiration (page /exercices-respiration/). Rien n'est envoyé ni enregistré. */
(function () {
  "use strict";
  var zone = document.getElementById("exercice");
  if (!zone) return;
  var MOTIFS = {
    coherence: { rythme: "Inspire 5 s · expire 5 s", phases: [["Inspire", 5, "in"], ["Expire", 5, "out"]] },
    carree: { rythme: "Inspire 4 s · retiens 4 s · expire 4 s · retiens 4 s", phases: [["Inspire", 4, "in"], ["Retiens", 4, "haut"], ["Expire", 4, "out"], ["Retiens", 4, "bas"]] },
    "478": { rythme: "Inspire 4 s · retiens 7 s · expire 8 s", phases: [["Inspire", 4, "in"], ["Retiens", 7, "haut"], ["Expire", 8, "out"]] }
  };
  var reduit = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var motif = "coherence", minutes = 3, enCours = false, debut = 0, raf = 0, phaseAffichee = -1, total = 0, verrou = null;
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

  function boucle(t) {
    var e = (t - debut) / 1000;
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
    enCours = true; total = dureeTotale(); phaseAffichee = -1; debut = performance.now();
    bouton.textContent = "Arrêter"; bouton.setAttribute("aria-pressed", "true");
    zone.classList.add("en-cours");
    garderEcranAllume();
    raf = requestAnimationFrame(boucle);
  }
  function arreter(fini) {
    enCours = false; cancelAnimationFrame(raf);
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
