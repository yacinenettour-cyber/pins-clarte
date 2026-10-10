/* Sources repliées en bas de page : un lien vers une source (exposant [1], « 8 sources » en haut de page) ouvre la liste
   avant que la page n'y descende, pour que la source visée soit visible. */
(function () {
  "use strict";
  var repli = document.querySelector(".repli-sources");
  if (!repli) return;
  function ouvrirPour(hash) {
    if (!hash || hash.charAt(0) !== "#") return;
    var cible = document.getElementById(decodeURIComponent(hash.slice(1)));
    if (cible && (cible.contains(repli) || repli.contains(cible))) repli.open = true;
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (a) ouvrirPour(a.getAttribute("href"));
  });
  window.addEventListener("hashchange", function () { ouvrirPour(location.hash); });
  ouvrirPour(location.hash);
})();
