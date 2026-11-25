// Render every SVG in avatars/svg and avatars/svg-transparent to PNG (1024px) and build a preview sheet.
// Usage: node avatars/tools/render.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const SIZE = 1024;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: SIZE, height: SIZE } });
  for (const [src, dst] of [['svg', 'png'], ['svg-transparent', 'png-transparent']]) {
    fs.mkdirSync(path.join(root, dst), { recursive: true });
    for (const f of fs.readdirSync(path.join(root, src)).filter(f => f.endsWith('.svg')).sort()) {
      const svg = fs.readFileSync(path.join(root, src, f), 'utf8').replace('width="512" height="512"', `width="${SIZE}" height="${SIZE}"`);
      await page.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
      await page.locator('svg').screenshot({ path: path.join(root, dst, f.replace('.svg', '.png')), omitBackground: true });
    }
  }
  // preview sheet
  const cast = fs.readFileSync(path.join(root, 'cast.tsv'), 'utf8').trim().split('\n').map(l => l.split('\t'));
  const cells = cast.map(([n, slug, name]) => {
    const svg = fs.readFileSync(path.join(root, 'svg', `${n}-${slug}.svg`), 'utf8').replace('width="512" height="512"', 'width="200" height="200"');
    return `<div class="c">${svg}<b>${n} · ${name}</b></div>`;
  }).join('');
  const sheet = `<html dir="rtl"><body style="margin:0;background:#1d3249;font-family:Arial,sans-serif">
  <div style="display:grid;grid-template-columns:repeat(8,200px);gap:18px;padding:24px">${cells}</div>
  <style>.c{text-align:center;color:#fff;font-size:17px}.c b{display:block;margin-top:6px}</style></body></html>`;
  await page.setViewportSize({ width: 8 * 218 + 30, height: 800 });
  await page.setContent(sheet);
  await page.screenshot({ path: path.join(root, 'preview.png'), fullPage: true });
  await browser.close();
  console.log('rendered');
})();
