const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [a, b, dir, mode] = process.argv.slice(2);
  const br = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await br.newPage({ viewport: { width: 600, height: 1000 } });
  pg.on('console', m => console.log('[page]', m.text())); pg.on('pageerror', e => console.log('[err]', e.message));
  await pg.goto('http://localhost:8773/index.html'); await pg.waitForFunction('window.ready', null, { timeout: 60000 });
  fs.mkdirSync(dir, { recursive: true });
  if (mode === 'times') { for (const t of a.split(',')) { const d = await pg.evaluate(t => window.renderFrame(t), +t); fs.writeFileSync(`${dir}/t${(+t).toFixed(2)}.jpg`, Buffer.from(d.split(',')[1], 'base64')); } }
  else for (let i = +a; i < +b; i++) { const d = await pg.evaluate(t => window.renderFrame(t), i / 30); fs.writeFileSync(`${dir}/f${String(i).padStart(5, '0')}.jpg`, Buffer.from(d.split(',')[1], 'base64')); }
  await br.close();
})();
