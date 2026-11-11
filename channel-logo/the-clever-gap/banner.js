const { chromium } = require('playwright'); const fs = require('fs');
const font = fs.readFileSync('font.b64', 'utf8'), logo = fs.readFileSync('out/the-clever-gap-1024.png').toString('base64');
const W = 2560, H = 1440, SY0 = 508, SY1 = 931;
// rail track across the desktop band, with glowing expansion gaps
let ties = '', rails = '', glows = '';
for (let x = -20; x < W; x += 46) ties += `<rect x="${x}" y="858" width="26" height="66" rx="4" fill="#5a3a26" stroke="#1b1522" stroke-width="5"/>`;
const seg = 300, gap = 22;
for (let x = -120; x < W; x += seg + gap) {
  for (const y of [870, 900]) rails += `<rect x="${x}" y="${y}" width="${seg}" height="16" rx="3" fill="#c9ced6" stroke="#1b1522" stroke-width="5"/>`;
  glows += `<rect x="${x + seg - 2}" y="856" width="${gap + 4}" height="70" fill="#ffc94d" opacity="0.55" filter="url(#g)"/>`;
}
// faint doodles: gears, hexes, bulbs
const gear = (cx, cy, r, n, op) => { let p = ''; for (let i = 0; i < n * 4; i++) { const a = i / (n * 4) * Math.PI * 2, rr = (i % 4 === 1 || i % 4 === 2) ? r * 1.18 : r; p += `${i ? 'L' : 'M'}${(cx + rr * Math.cos(a)).toFixed(1)},${(cy + rr * Math.sin(a)).toFixed(1)}`; } return `<path d="${p}Z" fill="none" stroke="#7ea2ff" stroke-width="10" opacity="${op}"/><circle cx="${cx}" cy="${cy}" r="${r * 0.35}" fill="none" stroke="#7ea2ff" stroke-width="10" opacity="${op}"/>`; };
const hex = (cx, cy, r, op) => `<path d="${[...Array(6)].map((_, i) => `${i ? 'L' : 'M'}${(cx + r * Math.cos(Math.PI / 6 + i * Math.PI / 3)).toFixed(1)},${(cy + r * Math.sin(Math.PI / 6 + i * Math.PI / 3)).toFixed(1)}`).join('')}Z" fill="none" stroke="#7ea2ff" stroke-width="10" opacity="${op}"/>`;
const bulb = (cx, cy, s, op) => `<g transform="translate(${cx},${cy}) scale(${s})" opacity="${op}" fill="none" stroke="#ffe08a" stroke-width="9"><circle r="46" cy="-10"/><path d="M-24 30 L-20 58 L20 58 L24 30"/><path d="M-20 70 L20 70 M-16 82 L16 82"/></g>`;
const doodles = gear(260, 640, 90, 10, 0.16) + hex(2330, 640, 100, 0.16) + bulb(2180, 760, 1.2, 0.22) + gear(2440, 780, 50, 8, 0.12) + bulb(140, 760, 1.0, 0.18) + hex(400, 790, 46, 0.14) + gear(1980, 590, 40, 8, 0.12) + hex(560, 600, 34, 0.12);
let stars = '', sd = 7; const rnd = () => (sd = (sd * 16807) % 2147483647) / 2147483647; for (let i = 0; i < 160; i++) { const x = rnd() * W, y = rnd() * 1300 + 60, r = 1.5 + (i % 3); stars += `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" opacity="${0.15 + (i % 5) * 0.08}"/>`; }
const html = `<style>@font-face{font-family:P;src:url(data:font/ttf;base64,${font})}html,body{margin:0}body{width:${W}px;height:${H}px;position:relative;overflow:hidden;
 background:radial-gradient(ellipse 1300px 520px at 50% 50%, #2a52c9 0%, #16307e 45%, #0a1640 80%, #060d27 100%)}
 svg.bg{position:absolute;inset:0}
 .logo{position:absolute;left:600px;top:${SY0 + 26}px;width:296px;height:296px;border-radius:50%;box-shadow:0 0 0 12px #1b1522,0 0 70px #ffc94d88}
 .t{position:absolute;left:950px;top:${SY0 + 52}px;font-family:P;letter-spacing:-3px;line-height:.9}
 .a{color:#fff;font-size:124px;text-shadow:8px 10px 0 #000}.a b{color:#ffc94d}
 .tag{font-family:P;font-size:41px;letter-spacing:0;color:#dfe7ff;margin-top:22px;text-shadow:4px 5px 0 #000}
 .tag i{font-style:normal;color:#ffc94d}</style>
 <svg class="bg" width="${W}" height="${H}"><defs><filter id="g" x="-200%" y="-50%" width="500%" height="200%"><feGaussianBlur stdDeviation="9"/></filter></defs>${stars}${doodles}${ties}${glows}${rails}</svg>
 <img class="logo" src="data:image/png;base64,${logo}">
 <div class="t"><div class="a">The Clever <b>Gap</b></div><div class="tag">Tiny fixes. <i>Big stories.</i> &nbsp;New Shorts every week</div></div>`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: W, height: H } });
  await p.setContent(html); await p.evaluate(() => document.fonts.ready); await p.screenshot({ path: 'out/banner-2560x1440.png' });
  await p.setContent(html + `<div style="position:absolute;left:0;right:0;top:${SY0}px;height:${SY1 - SY0}px;border:6px dashed #ff4d4d;box-sizing:border-box"></div><div style="position:absolute;left:${(W - 1546) / 2}px;width:1546px;top:${SY0}px;height:${SY1 - SY0}px;border:6px solid #4dff88;box-sizing:border-box"></div>`);
  await p.screenshot({ path: 'out/banner-safe-area-check.png' }); await b.close(); })();
