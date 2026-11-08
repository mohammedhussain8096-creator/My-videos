// Render 3D shots to JPEG frame folders.  Usage: node render3d.js jobs.json
// jobs.json = [{ "out": "dir", "shot": "core", "params": {...}, "t0": 0, "D": 5.0, "frames": 120, "fps": 30 }, ...]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('console', m => { if (m.type() === 'error') console.log('console:', m.text()); });
  page.on('pageerror', e => console.log('pageerror:', e.message));
  await page.goto('file://' + path.join(__dirname, 'chernobyl3d.html'));
  await page.waitForFunction('window.ready===true', { timeout: 120000 });
  for (const j of jobs) {
    fs.mkdirSync(j.out, { recursive: true });
    for (let f = 0; f < j.frames; f++) {
      const file = path.join(j.out, String(f).padStart(4, '0') + '.jpg');
      if (fs.existsSync(file)) continue;
      const t = j.t0 + f / j.fps;
      await page.evaluate(([n, t, D, p]) => window.renderShot(n, t, D, p), [j.shot, t, j.D, j.params]);
      const data = await page.evaluate(() => document.getElementById('c').toDataURL('image/jpeg', 0.93));
      fs.writeFileSync(file, Buffer.from(data.split(',')[1], 'base64'));
    }
    console.log('done', j.out, j.frames);
  }
  await browser.close();
})();
