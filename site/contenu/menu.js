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

/* Bouton « retour en haut » : apparaît après un écran et demi de lecture ; au clic, la page remonte et le focus va au
   titre principal (utile au clavier et aux lecteurs d'écran). */
(function () {
  "use strict";
  var bouton = document.createElement("button");
  bouton.type = "button";
  bouton.className = "haut-page";
  bouton.hidden = true;
  bouton.setAttribute("aria-label", "Revenir en haut de la page");
  bouton.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>';
  document.body.appendChild(bouton);
  var visible = false;
  function majBouton() {
    var v = window.scrollY > window.innerHeight * 1.5;
    if (v !== visible) { visible = v; bouton.hidden = !v; }
  }
  window.addEventListener("scroll", majBouton, { passive: true });
  majBouton();
  bouton.addEventListener("click", function () {
    var doux = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    window.scrollTo({ top: 0, behavior: doux ? "smooth" : "auto" });
    var titre = document.querySelector("h1");
    if (titre) { titre.setAttribute("tabindex", "-1"); titre.focus({ preventScroll: true }); }
  });
})();

/* Mode clair / sombre : suit le réglage de l'appareil, ou le choix fait avec le bouton (gardé sur cet appareil). */
(function () {
  "use strict";
  var racine = document.documentElement, clairAppareil = window.matchMedia("(prefers-color-scheme: light)");
  function theme() { return racine.dataset.theme || (clairAppareil.matches ? "clair" : "sombre"); }
  function majTheme() {
    var t = theme(), action = t === "clair" ? "Passer en mode sombre" : "Passer en mode clair";
    document.querySelectorAll(".theme-bascule").forEach(function (b) { b.setAttribute("aria-label", action); b.title = action; });
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", t === "clair" ? "#F4F0E8" : "#0F1724");
    document.dispatchEvent(new CustomEvent("cm-theme", { detail: t }));
  }
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".theme-bascule")) return;
    var t = theme() === "clair" ? "sombre" : "clair";
    racine.dataset.theme = t;
    try { localStorage.setItem("cm-theme", t); } catch (err) {}
    majTheme();
  });
  if (clairAppareil.addEventListener) clairAppareil.addEventListener("change", majTheme);
  majTheme();
})();
/* Barre de lecture des articles (13/10/2026) : un fin trait vert sous l'en-tête montre la part de l'article déjà lue.
   Décorative (aria-hidden) ; sans JavaScript, rien ne s'affiche. */
(function () {
  "use strict";
  var article = document.querySelector("main#contenu > .etroit > article:not([class])");
  if (!article) return;
  var barre = document.createElement("div");
  barre.className = "barre-lecture";
  barre.setAttribute("aria-hidden", "true");
  document.body.appendChild(barre);
  var attente = false;
  function maj() {
    attente = false;
    var r = article.getBoundingClientRect(), parcours = r.height - window.innerHeight;
    var part = parcours > 0 ? Math.min(1, Math.max(0, -r.top / parcours)) : 1;
    barre.style.transform = "scaleX(" + part.toFixed(4) + ")";
  }
  function demander() { if (!attente) { attente = true; requestAnimationFrame(maj); } }
  window.addEventListener("scroll", demander, { passive: true });
  window.addEventListener("resize", demander);
  maj();
})();

/* Origine de la visite (audit du 13/10/2026) : quand la page est ouverte depuis une épingle (adresse avec
   utm_source=pinterest…), les liens vers le guide gardent cette origine, pour savoir dans systeme.io quels inscrits
   viennent de Pinterest. Rien n'est enregistré : seule l'adresse de la page ouverte est lue. */
(function () {
  "use strict";
  var ici = new URLSearchParams(window.location.search), source = ici.get("utm_source");
  if (!source || source === "site") return;
  var epingle = (ici.get("utm_content") || ici.get("utm_campaign") || "").slice(0, 80);
  // Au moment du clic (et non au chargement) : couvre aussi les liens créés ensuite, comme le résultat du test.
  function marquer(ev) {
    var a = ev.target.closest && ev.target.closest('a[href^="https://lp.contactapaisement-mental.fr/"]');
    if (!a) return;
    try {
      var u = new URL(a.href);
      u.searchParams.set("utm_source", source);
      if (epingle) u.searchParams.set("utm_term", epingle);
      a.href = u.toString();
    } catch (err) { /* adresse inattendue : lien laissé tel quel */ }
  }
  document.addEventListener("click", marquer, true);
  document.addEventListener("auxclick", marquer, true);
})();
