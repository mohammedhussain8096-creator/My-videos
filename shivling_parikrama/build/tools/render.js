const { chromium } = require('playwright'); const fs=require('fs');
(async () => {
  const [,, html, outdir, fpsS, W, NW] = process.argv; const fps=+fpsS, w=+W, nw=+NW;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + html); await p.waitForFunction(() => window.READY === true);
  const cues = await p.evaluate(() => window.CUES); if (w===0) fs.writeFileSync(outdir+'/../cues.json', JSON.stringify(cues));
  const n = Math.ceil(cues.end * fps);
  for (let i = w; i < n; i += nw) {
    const f = `${outdir}/${String(i).padStart(5,'0')}.jpg`; if (fs.existsSync(f)) continue;
    await p.evaluate(t => render(t), i / fps);
    await p.screenshot({ path: f, type: 'jpeg', quality: 92 });
    if (i % 300 === w) console.log(`w${w} ${i}/${n}`);
  }
  await b.close(); console.log(`w${w} done`);
})();
