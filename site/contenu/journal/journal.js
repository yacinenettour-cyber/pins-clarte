/* Journal d'humeur (page /journal-humeur/) : les notes restent dans le navigateur (localStorage), rien n'est envoyé. */
(function () {
  "use strict";
  var zone = document.getElementById("journal");
  if (!zone) return;
  var CLE = "cm-journal";
  var ECHELLES = {
    h: ["Très difficile", "Difficile", "Moyenne", "Bonne", "Très bonne"],
    t: ["Très calme", "Calme", "Moyen", "Tendu", "Très tendu"],
    s: ["Très mauvaise", "Mauvaise", "Moyenne", "Bonne", "Très bonne"]
  };
  var choix = { h: 0, t: 0, s: 0 };
  var $ = function (sel) { return zone.querySelector(sel); };
  var message = $(".jr-message"), date = $("#jr-date"), note = $("#jr-note"), liste = $(".jr-liste"), courbe = $(".jr-courbe"), alerte = $(".jr-repere");

  function lire() {
    try { var v = JSON.parse(localStorage.getItem(CLE) || "[]"); return Array.isArray(v) ? v : []; } catch (e) { return []; }
  }
  function ecrire(notes) {
    try { localStorage.setItem(CLE, JSON.stringify(notes)); return true; } catch (e) { return false; }
  }
  function stockageDisponible() {
    try { localStorage.setItem("cm-test", "1"); localStorage.removeItem("cm-test"); return true; } catch (e) { return false; }
  }
  function aujourdhui() { var d = new Date(); d.setMinutes(d.getMinutes() - d.getTimezoneOffset()); return d.toISOString().slice(0, 10); }
  function dateFr(iso) { var p = iso.split("-"); return p[2] + "/" + p[1] + "/" + p[0]; }
  function afficherMessage(texte) { message.textContent = texte; message.hidden = !texte; }
  function echapper(t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  /* Boutons de note (1 à 5) */
  zone.querySelectorAll("[data-echelle]").forEach(function (groupe) {
    var cle = groupe.dataset.echelle;
    groupe.querySelectorAll("button").forEach(function (b) {
      b.addEventListener("click", function () {
        choix[cle] = Number(b.dataset.valeur);
        groupe.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
      });
    });
  });

  function remplirFormulaire(n) {
    ["h", "t", "s"].forEach(function (cle) {
      choix[cle] = n ? n[cle] : 0;
      zone.querySelectorAll('[data-echelle="' + cle + '"] button').forEach(function (b) { b.setAttribute("aria-pressed", String(n && Number(b.dataset.valeur) === n[cle])); });
    });
    note.value = n ? (n.n || "") : "";
  }
  date.addEventListener("change", function () {
    var n = lire().filter(function (x) { return x.d === date.value; })[0];
    remplirFormulaire(n);
  });

  $(".jr-enregistrer").addEventListener("click", function () {
    if (!date.value) { afficherMessage("Choisis une date."); return; }
    if (!choix.h || !choix.t || !choix.s) { afficherMessage("Choisis une note pour ton humeur, ton stress et ta nuit."); return; }
    var notes = lire().filter(function (x) { return x.d !== date.value; });
    var remplace = notes.length !== lire().length;
    notes.push({ d: date.value, h: choix.h, t: choix.t, s: choix.s, n: note.value.trim().slice(0, 300) });
    notes.sort(function (a, b) { return a.d < b.d ? -1 : 1; });
    if (!ecrire(notes)) { afficherMessage("Ton navigateur bloque l'enregistrement (navigation privée ?) : la note n'a pas été gardée."); return; }
    afficherMessage((remplace ? "Note du " + dateFr(date.value) + " remplacée." : "Note du " + dateFr(date.value) + " enregistrée sur cet appareil."));
    afficher();
  });

  /* Courbe des 14 derniers jours (humeur et stress) : décorative, le tableau donne les mêmes informations. */
  function dessinerCourbe(notes) {
    var jours = [], fin = new Date(aujourdhui() + "T12:00:00");
    for (var i = 13; i >= 0; i--) { var d = new Date(fin); d.setDate(d.getDate() - i); jours.push(d.toISOString().slice(0, 10)); }
    var parJour = {}; notes.forEach(function (n) { parJour[n.d] = n; });
    var L = 320, H = 120, x = function (i) { return 14 + i * (L - 28) / 13; }, y = function (v) { return H - 14 - (v - 1) * (H - 28) / 4; };
    function trace(cle) {
      var pts = jours.map(function (j, i) { return parJour[j] ? [x(i), y(parJour[j][cle])] : null; });
      var d = "", ouvert = false;
      pts.forEach(function (p) { if (p) { d += (ouvert ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1); ouvert = true; } else { ouvert = false; } });
      var ronds = pts.filter(Boolean).map(function (p) { return '<circle cx="' + p[0].toFixed(1) + '" cy="' + p[1].toFixed(1) + '" r="3.5"/>'; }).join("");
      return '<g class="jr-' + cle + '"><path d="' + d + '"/>' + ronds + "</g>";
    }
    var grille = [1, 2, 3, 4, 5].map(function (v) { return '<line x1="8" x2="' + (L - 8) + '" y1="' + y(v) + '" y2="' + y(v) + '"/>'; }).join("");
    courbe.innerHTML = '<svg viewBox="0 0 ' + L + " " + H + '" aria-hidden="true"><g class="jr-grille">' + grille + "</g>" + trace("t") + trace("h") + "</svg>" +
      '<p class="jr-legende"><span class="jr-puce-h"></span>Humeur <span class="jr-puce-t"></span>Stress · 14 derniers jours, du plus ancien au plus récent</p>';
  }

  /* Repère : humeur basse presque tous les jours sur 14 jours (au moins 7 notes, 80 % à « difficile » ou moins). */
  function repere(notes) {
    var limite = new Date(aujourdhui() + "T12:00:00"); limite.setDate(limite.getDate() - 13);
    var recentes = notes.filter(function (n) { return new Date(n.d + "T12:00:00") >= limite; });
    var basses = recentes.filter(function (n) { return n.h <= 2; }).length;
    alerte.hidden = !(recentes.length >= 7 && basses / recentes.length >= 0.8);
  }

  function afficher() {
    var notes = lire();
    zone.classList.toggle("jr-vide", !notes.length);
    dessinerCourbe(notes);
    repere(notes);
    var lignes = notes.slice().reverse().slice(0, 60).map(function (n) {
      return '<tr><td data-label="Date">' + dateFr(n.d) + '</td><td data-label="Humeur">' + n.h + " · " + ECHELLES.h[n.h - 1] +
        '</td><td data-label="Stress">' + n.t + " · " + ECHELLES.t[n.t - 1] + '</td><td data-label="Nuit">' + n.s + " · " + ECHELLES.s[n.s - 1] +
        '</td><td data-label="' + (n.n ? "Note" : "") + '">' + echapper(n.n || "") + "</td></tr>";
    }).join("");
    liste.innerHTML = notes.length
      ? '<p class="jr-titre-liste" id="jr-titre-liste">Tes notes, de la plus récente à la plus ancienne</p><div class="tableau"><table aria-labelledby="jr-titre-liste"><thead><tr><th scope="col">Date</th><th scope="col">Humeur</th><th scope="col">Stress</th><th scope="col">Nuit</th><th scope="col">Note</th></tr></thead><tbody>' + lignes + "</tbody></table></div>"
      : '<p class="jr-rien">Aucune note pour l\'instant : ta première note apparaîtra ici.</p>';
  }

  /* Copie de sauvegarde (fichier JSON), reprise d'une copie, effacement */
  $(".jr-exporter").addEventListener("click", function () {
    var notes = lire();
    if (!notes.length) { afficherMessage("Aucune note à enregistrer pour l'instant."); return; }
    var lien = document.createElement("a");
    lien.href = URL.createObjectURL(new Blob([JSON.stringify({ journal: "Clarté Mentale", notes: notes }, null, 1)], { type: "application/json" }));
    lien.download = "journal-humeur-" + aujourdhui() + ".json";
    document.body.appendChild(lien); lien.click(); lien.remove();
    afficherMessage("Copie enregistrée dans tes téléchargements.");
  });
  var fichier = $("#jr-fichier");
  $(".jr-importer").addEventListener("click", function () { fichier.click(); });
  fichier.addEventListener("change", function () {
    var f = fichier.files && fichier.files[0];
    if (!f) return;
    f.text().then(function (texte) {
      var donnees = JSON.parse(texte), notes = lire(), parDate = {};
      notes.forEach(function (n) { parDate[n.d] = n; });
      var ajoutees = 0;
      (donnees.notes || []).forEach(function (n) {
        var ok = /^\d{4}-\d{2}-\d{2}$/.test(n.d) && [n.h, n.t, n.s].every(function (v) { return v >= 1 && v <= 5 && v % 1 === 0; });
        if (ok && !parDate[n.d]) { parDate[n.d] = { d: n.d, h: n.h, t: n.t, s: n.s, n: String(n.n || "").slice(0, 300) }; ajoutees++; }
      });
      var toutes = Object.keys(parDate).sort().map(function (k) { return parDate[k]; });
      if (!ecrire(toutes)) { afficherMessage("Ton navigateur bloque l'enregistrement : la copie n'a pas pu être reprise."); return; }
      afficherMessage(ajoutees + " note(s) ajoutée(s) depuis la copie.");
      afficher();
    }).catch(function () { afficherMessage("Ce fichier n'est pas une copie du journal."); });
    fichier.value = "";
  });
  $(".jr-effacer").addEventListener("click", function () {
    if (!lire().length) { afficherMessage("Il n'y a aucune note à effacer."); return; }
    if (!window.confirm("Effacer toutes tes notes de cet appareil ? Cette action est définitive.")) return;
    try { localStorage.removeItem(CLE); } catch (e) {}
    remplirFormulaire(null);
    afficherMessage("Toutes tes notes ont été effacées de cet appareil.");
    afficher();
  });

  date.value = aujourdhui();
  date.max = aujourdhui();
  if (!stockageDisponible()) afficherMessage("Ton navigateur bloque l'enregistrement (navigation privée ?) : tes notes ne pourront pas être gardées.");
  remplirFormulaire(lire().filter(function (x) { return x.d === date.value; })[0]);
  afficher();
})();
