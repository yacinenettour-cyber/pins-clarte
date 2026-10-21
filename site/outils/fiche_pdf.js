#!/usr/bin/env node
/* Fabrique le PDF de la fiche « 5 exercices de respiration » à partir de la page construite (site/_build/), avec la
   feuille de style d'impression de la page (A4). Appelé par construire.py quand la fiche change (empreinte dans
   site/contenu/fiche/fiche-respiration.empreinte) ; on peut aussi le lancer à la main après construire.py :

     node site/outils/fiche_pdf.js [dossier-captures]

   Écrit site/contenu/fiche/fiche-respiration.pdf (versionné, copié dans le site à chaque construction). Avec un
   dossier en argument, enregistre aussi une capture PNG de chaque page du PDF (page-1.png, page-2.png…, avec
   pdftoppm) pour vérifier le rendu à l'œil. Gratuit : Playwright et Chromium installés sur la machine (aucun service en ligne).
   Chromium : variable CHROMIUM, sinon /opt/pw-browsers/chromium, sinon celui de Playwright. */
const http = require("http");
const fs = require("fs");
const path = require("path");
let playwright;
try { playwright = require("playwright"); } catch (e) {
  playwright = require(path.join(path.dirname(process.execPath), "..", "lib", "node_modules", "playwright"));
}

const SITE = path.resolve(__dirname, "..");
const BUILD = path.join(SITE, "_build");
const SORTIE = path.join(SITE, "contenu", "fiche", "fiche-respiration.pdf");
const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".woff2": "font/woff2",
  ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp", ".json": "application/json",
  ".pdf": "application/pdf", ".mp3": "audio/mpeg" };

function serveur() {
  return http.createServer((req, res) => {
    let p = decodeURIComponent(new URL(req.url, "http://x").pathname);
    if (p.endsWith("/")) p += "index.html";
    const f = path.join(BUILD, path.normalize(p));
    if (!f.startsWith(BUILD) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" });
    fs.createReadStream(f).pipe(res);
  });
}

(async () => {
  if (!fs.existsSync(path.join(BUILD, "fiche-respiration", "index.html"))) {
    console.error("Lancer d'abord python3 site/outils/construire.py");
    process.exit(1);
  }
  const srv = serveur();
  await new Promise((ok) => srv.listen(0, "127.0.0.1", ok));
  const base = `http://127.0.0.1:${srv.address().port}`;
  const chemin = process.env.CHROMIUM || (fs.existsSync("/opt/pw-browsers/chromium") ? "/opt/pw-browsers/chromium" : undefined);
  const navigateur = await playwright.chromium.launch(chemin ? { executablePath: chemin } : {});
  try {
    const page = await navigateur.newPage();
    // Thème clair pour l'impression ; la feuille d'impression met de toute façon tout en noir sur blanc.
    await page.emulateMedia({ colorScheme: "light" });
    await page.goto(`${base}/fiche-respiration/`, { waitUntil: "networkidle" });
    await page.evaluate(async () => {
      document.querySelectorAll("details").forEach((d) => { d.open = true; });
      await document.fonts.ready;
    });
    fs.mkdirSync(path.dirname(SORTIE), { recursive: true });
    await page.pdf({ path: SORTIE, format: "A4", printBackground: false, preferCSSPageSize: true, tagged: true, outline: true });
    console.log(`PDF écrit : ${path.relative(path.dirname(SITE), SORTIE)} (${(fs.statSync(SORTIE).size / 1024).toFixed(0)} Ko)`);
    const dossier = process.argv[2];
    if (dossier) {
      // Une capture PNG par page du PDF (pdftoppm, paquet poppler-utils), pour regarder le rendu imprimé.
      fs.mkdirSync(dossier, { recursive: true });
      require("child_process").execFileSync("pdftoppm", ["-png", "-r", "110", SORTIE, path.join(dossier, "page")]);
      console.log(`Captures : ${fs.readdirSync(dossier).filter((f) => f.startsWith("page")).map((f) => path.join(dossier, f)).join(", ")}`);
    }
  } finally {
    await navigateur.close();
    srv.close();
  }
})().catch((e) => { console.error(e); process.exit(1); });
