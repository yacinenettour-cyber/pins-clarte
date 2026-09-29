// Imprime chaque fiche HTML en PDF A4 et en PNG (aperçu) avec Chromium.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const dir = path.join(__dirname, 'html');
  const out = process.argv[2];
  const prev = path.join(__dirname, 'preview');
  fs.mkdirSync(out, { recursive: true });
  fs.mkdirSync(prev, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort()) {
    await page.goto('file://' + path.join(dir, f));
    await page.evaluate(() => document.fonts.ready);
    const name = f.replace('.html', '');
    await page.pdf({ path: path.join(out, name + '.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
    // Contrôle : aucun contenu ne doit déborder de sa page A4
    const overflow = await page.evaluate(() => [...document.querySelectorAll('.page')].map((p, i) => {
      const r = p.getBoundingClientRect();
      const foot = p.querySelector('.foot');
      const limit = foot ? foot.getBoundingClientRect().top : r.bottom;
      let maxBottom = 0;
      p.querySelectorAll('*').forEach(el => {
        if (el.closest('.foot')) return;
        const b = el.getBoundingClientRect().bottom;
        if (b > maxBottom) maxBottom = b;
      });
      return { page: i + 1, marge_mm: Math.round((limit - maxBottom) / 3.78) };
    }));
    console.log(name, JSON.stringify(overflow));
    await page.screenshot({ path: path.join(prev, name + '.png'), fullPage: true });
  }
  await browser.close();
})();
