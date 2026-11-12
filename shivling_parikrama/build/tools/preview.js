const { chromium } = require('playwright');
(async () => {
  const [,, html, outdir, ...times] = process.argv;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const errs=[]; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
  await p.goto('file://' + html); await p.waitForFunction(() => window.READY === true, null, {timeout: 20000});
  for (const t of times) { await p.evaluate(t => render(+t), t); await p.screenshot({ path: `${outdir}/f_${String(t).padStart(6,'0')}.jpg`, type: 'jpeg', quality: 80 }); }
  console.log('errors:', errs.slice(0,5).join(' | ') || 'none'); await b.close();
})();
