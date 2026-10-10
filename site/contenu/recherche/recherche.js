/* Recherche interne (page /recherche/) : l'index des pages (/recherche/index.json) est fabriqué à la construction du
   site ; la recherche se fait dans le navigateur, sans service extérieur. */
(function () {
  "use strict";
  var form = document.getElementById("form-recherche");
  if (!form) return;
  var champ = document.getElementById("q"), etat = document.getElementById("recherche-etat"), liste = document.getElementById("recherche-resultats");
  var MOTS_VIDES = " le la les un une des de du d l au aux et ou en a à mon ma mes ton ta tes son sa ses ce cet cette pour par sur dans avec sans que qui quoi est sont comment pourquoi quand quel quelle quels quelles ne pas plus se je tu il elle on nous vous ";
  var index = null;
  function normaliser(t) { return String(t).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[’']/g, " "); }
  function mots(q) {
    return normaliser(q).split(/[^a-z0-9-]+/).filter(function (m) { return m.length > 1 && MOTS_VIDES.indexOf(" " + m + " ") < 0; });
  }
  function echapper(t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function compter(texte, m) { var n = 0, i = texte.indexOf(m); while (i >= 0 && n < 12) { n++; i = texte.indexOf(m, i + m.length); } return n; }

  function extrait(page, termes) {
    var brut = page.x, norm = normaliser(brut), pos = -1;
    termes.some(function (m) { pos = norm.indexOf(m); return pos >= 0; });
    if (pos < 0) return echapper(page.d);
    var debut = Math.max(0, pos - 90), fin = Math.min(brut.length, pos + 170);
    var morceau = (debut > 0 ? "…" : "") + brut.slice(debut, fin) + (fin < brut.length ? "…" : "");
    var html = echapper(morceau), normM = normaliser(morceau);
    /* Surligne les termes trouvés (positions calculées sur le texte sans accents, même longueur). */
    var marques = [];
    termes.forEach(function (m) { var i = normM.indexOf(m); while (i >= 0) { marques.push([i, i + m.length]); i = normM.indexOf(m, i + m.length); } });
    if (!marques.length) return html;
    marques.sort(function (a, b) { return a[0] - b[0]; });
    var res = "", dernier = 0;
    marques.forEach(function (r) { if (r[0] < dernier) return; res += echapper(morceau.slice(dernier, r[0])) + "<mark>" + echapper(morceau.slice(r[0], r[1])) + "</mark>"; dernier = r[1]; });
    return res + echapper(morceau.slice(dernier));
  }

  function chercher(q) {
    var termes = mots(q);
    if (!termes.length) { etat.textContent = "Tape un ou plusieurs mots, par exemple « cortisol » ou « réveil la nuit »."; liste.innerHTML = ""; return; }
    var resultats = index.map(function (p) {
      var t = normaliser(p.t), d = normaliser(p.d), h = normaliser(p.h.join(" ")), x = normaliser(p.x), score = 0, trouves = 0;
      termes.forEach(function (m) {
        var s = (t.indexOf(m) >= 0 ? 12 : 0) + (h.indexOf(m) >= 0 ? 5 : 0) + (d.indexOf(m) >= 0 ? 4 : 0) + compter(x, m);
        if (s) trouves++;
        score += s;
      });
      return { p: p, score: score + (trouves === termes.length ? 50 : 0), tous: trouves === termes.length, trouves: trouves };
    }).filter(function (r) { return r.trouves; });
    var complets = resultats.filter(function (r) { return r.tous; });
    if (complets.length) resultats = complets;
    resultats.sort(function (a, b) { return b.score - a.score; });
    resultats = resultats.slice(0, 12);
    etat.textContent = resultats.length
      ? resultats.length + (resultats.length > 1 ? " résultats" : " résultat") + " pour « " + q + " »" + (complets.length ? "" : " (certains mots seulement)")
      : "Aucun résultat pour « " + q + " ». Essaie un autre mot, ou parcours tous les articles.";
    liste.innerHTML = resultats.map(function (r) {
      return '<li><a href="' + r.p.u + '">' + echapper(r.p.t) + '</a><span class="type">' + echapper(r.p.k) + "</span><p>" + extrait(r.p, termes) + "</p></li>";
    }).join("");
  }

  function lancer(q) {
    if (index) { chercher(q); return; }
    etat.textContent = "Recherche en cours…";
    fetch("/recherche/index.json").then(function (r) { return r.json(); }).then(function (donnees) { index = donnees; chercher(q); })
      .catch(function () { etat.textContent = "La recherche n'a pas pu se charger. Vérifie ta connexion, puis réessaie."; });
  }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var q = champ.value.trim();
    if (history.replaceState) history.replaceState(null, "", q ? "?q=" + encodeURIComponent(q) : location.pathname);
    lancer(q);
  });
  var depart = new URLSearchParams(location.search).get("q");
  if (depart) { champ.value = depart; lancer(depart); }
})();
