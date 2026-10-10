/* Menu mobile commun à l'accueil et aux autres pages (injecté à la construction). */
(function () {
  "use strict";
  var burger = document.getElementById("burger"), menu = document.getElementById("menu-mobile");
  if (!burger || !menu) return;
  function estOuvert() { return burger.getAttribute("aria-expanded") === "true"; }
  function basculer(ouvrir, instant) {
    var ouvert = typeof ouvrir === "boolean" ? ouvrir : !estOuvert();
    if (instant) menu.classList.add("instant");
    burger.setAttribute("aria-expanded", String(ouvert));
    burger.setAttribute("aria-label", ouvert ? "Fermer le menu" : "Ouvrir le menu");
    menu.classList.toggle("ouvert", ouvert);
    menu.setAttribute("aria-hidden", String(!ouvert));
    menu.querySelectorAll("a").forEach(function (a) { a.tabIndex = ouvert ? 0 : -1; });
    document.documentElement.classList.toggle("menu-ouvert", ouvert);
    if (instant) { void menu.offsetWidth; menu.classList.remove("instant"); }
    if (ouvert) { var premier = menu.querySelector("a"); if (premier) premier.focus({ preventScroll: true }); }
  }
  burger.addEventListener("click", function () { basculer(); });
  menu.addEventListener("click", function (e) {
    var a = e.target.closest("a");
    if (!a) return;
    var cible = a.hash && a.pathname === location.pathname ? document.getElementById(decodeURIComponent(a.hash.slice(1))) : null;
    /* Lien vers une autre page : le menu reste affiché jusqu'à l'arrivée de la nouvelle page (rien ne bouge entre-temps). */
    if (!cible) return;
    /* Partie de la même page : le menu se ferme d'un coup, puis la page défile jusqu'à la partie, sous l'en-tête. */
    e.preventDefault();
    basculer(false, true);
    if (history.pushState) history.pushState(null, "", a.hash);
    var doux = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    requestAnimationFrame(function () { cible.scrollIntoView({ behavior: doux ? "smooth" : "auto", block: "start" }); });
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && estOuvert()) { basculer(false); burger.focus(); } });
  window.addEventListener("resize", function () { if (window.innerWidth > 860 && estOuvert()) basculer(false, true); });
  /* Retour arrière : la page revient du cache telle qu'on l'a quittée, menu ouvert ; on le referme sans animation. */
  window.addEventListener("pageshow", function (e) { if (e.persisted && estOuvert()) basculer(false, true); });
})();
