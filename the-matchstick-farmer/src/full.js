// ===== assets for the rest of the story: burning fields, embers, explainer (flame, plate, car), firefighters, truck =====
const FOG = root.fog;
// --- instanced wheat burn helpers ---
const origOf = f => [f.st.instanceMatrix.array.slice(), f.hd.instanceMatrix.array.slice()];
const stripOrig = origOf(stripF), nOrig = origOf(fieldN);
function burnInst(f, orig, test) { const a = f.st.instanceMatrix.array, b = f.hd.instanceMatrix.array; f.pos.forEach((p, i) => { const o = i * 16; if (test(p)) for (let j = 0; j < 16; j++) a[o + j] = b[o + j] = 0; else for (let j = 0; j < 16; j++) { a[o + j] = orig[0][o + j]; b[o + j] = orig[1][o + j]; } }); f.st.instanceMatrix.needsUpdate = f.hd.instanceMatrix.needsUpdate = true; }
const ashN = M(box(24, 0.07, 28), toon(0xffffff, { map: T4.ash }), { p: [-14, 0.045, -8], recv: true, to: world, cast: false }); ashN.visible = false;
let lastBX = null, lastNF = null;
function stripTo(bx) { bx = Math.round(bx * 20) / 20; if (bx === lastBX) return; lastBX = bx; burnInst(stripF, stripOrig, p => p[0] < bx); const s = cl((Math.min(bx, 26) - 2) / 24); ashStrip.visible = s > 0.002; ashStrip.scale.x = Math.max(s, 0.001); ashStrip.position.x = 2 + 12 * s; }
function neighTo(nf) { nf = Math.round(nf * 20) / 20; if (nf === lastNF) return; lastNF = nf; burnInst(fieldN, nOrig, p => p[1] < nf); const s = cl((Math.min(nf, Z0) - Z1) / 28); ashN.visible = s > 0.002; ashN.scale.z = Math.max(s, 0.001); ashN.position.z = Z1 + 14 * s; }
// pines on the hills and in the forest go black once the fire has passed
const PINE_G = new THREE.Color(0x2f6b3f), PINE_B = new THREE.Color(0x2b2622);
// --- extra sprite pools: embers, drip-torch flames, smoke puffs ---
const embers = sprites(root, 50, glowTex), dripFl = sprites(root, 40, flameTex), puff = sprites(root, 14, smokeTex, false);
FIRES.push(...embers, ...dripFl, ...puff);
function embersAt(pts, t, s = 0.35) { embers.forEach((e, i) => { if (i >= pts.length) return; const p = pts[i]; e.visible = true; e.center.set(0.5, 0.5); const fl = 0.6 + 0.4 * Math.sin(t * (5 + i % 4) + i * 2.1); e.position.copy(p); e.scale.set(s * fl, s * fl, 1); e.material.opacity = 0.9; }); }
function puffAt(p, t, t0, size = 1.2, n = 14) { const q = t - t0; if (q < 0 || q > 2.2) return; puff.forEach((s, i) => { if (i >= n) return; s.visible = true; s.center.set(0.5, 0.5); const a = i * 2.39, r = q * (0.6 + (i % 3) * 0.25); s.position.set(p.x + Math.cos(a) * r * 0.6, p.y + q * 0.9 + (i % 4) * 0.1, p.z + Math.sin(a) * r * 0.3); const sc = size * (0.4 + q * 0.7); s.scale.set(sc, sc, 1); s.material.opacity = 0.7 * (1 - q / 2.2); }); }
// lone charred stalk that topples in the ash
const lone = new THREE.Group(); world.add(lone); M(wheatGeo, toon(0xd9a43a), { ol: 0.01, to: lone }); M(headGeo, toon(0xe8b84a), { ol: 0.01, to: lone }); lone.scale.setScalar(1.25); lone.visible = false;
// --- explainer stage (flat royal blue) ---
const xp = new THREE.Group(); root.add(xp); SETS.push(xp);
// flame character: lathe teardrop with vertex colours (yellow core → orange → red tip)
const flameC = new THREE.Group(); xp.add(flameC);
{ const pts = []; for (let i = 0; i <= 28; i++) { const u = i / 28; const r = u < 0.33 ? Math.sin(u / 0.33 * Math.PI / 2) : Math.pow(1 - (u - 0.33) / 0.67, 1.25); pts.push(new THREE.Vector2(Math.max(r * 1.05, 0.001), u * 3.2)); }
  const lg = new THREE.LatheGeometry(pts, 40); const pos = lg.attributes.position, col = []; const cY = new THREE.Color(0xffd84a), cO = new THREE.Color(0xff8a24), cR = new THREE.Color(0xe8402a);
  for (let i = 0; i < pos.count; i++) { const y = pos.getY(i) / 3.2; const c = y < 0.45 ? cY.clone().lerp(cO, y / 0.45) : cO.clone().lerp(cR, (y - 0.45) / 0.55); col.push(c.r, c.g, c.b); } lg.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
  const fm = toon(0xffffff, { vertexColors: true }); flameC.userData.body = M(lg, fm, { ol: 0.05, to: flameC });
  for (const s of [-1, 1]) { const tg = M(lg, fm, { ol: 0.04, p: [s * 0.75, 0.2, -0.1], s: [0.42, 0.55, 0.42], r: [0, 0, -s * 0.45], to: flameC }); tg.userData.side = s; (flameC.userData.tongues = flameC.userData.tongues || []).push(tg); }
  const eyes = new THREE.Group(); eyes.position.set(0, 1.25, 0.9); flameC.add(eyes); flameC.userData.pup = [];
  for (const s of [-1, 1]) { M(sph(0.24, 20, 14), toon(0xffffff), { ol: 0.03, p: [s * 0.33, 0, 0], s: [1, 1.2, 0.6], to: eyes }); flameC.userData.pup.push(M(sph(0.11, 16, 10), flat(0x1b1522), { p: [s * 0.33, -0.02, 0.15], to: eyes })); M(box(0.34, 0.07, 0.05), flat(0x1b1522), { p: [s * 0.33, 0.36, 0.08], r: [0, 0, s * -0.18], to: eyes }); }
  flameC.userData.brows = eyes.children.filter(m => m.geometry.type === 'BoxGeometry');
  const mouth = M(new THREE.CircleGeometry(0.3, 32), flat(0x5a1420), { p: [0, 0.68, 1.03], r: [-0.25, 0, 0], to: flameC, cast: false }); M(new THREE.CircleGeometry(0.16, 24), flat(0xf08a96), { p: [0, -0.12, 0.005], s: [1, 0.6, 1], to: mouth, cast: false }); flameC.userData.mouth = mouth; }
function flameAnim(t, open = 0.25, sc = 1, look = [0, 0], sad = 0) { const f = flameC.userData; flameC.scale.set(sc * (1 + 0.03 * Math.sin(t * 9)), sc * (1 + 0.05 * Math.sin(t * 7 + 1)), sc); f.body.rotation.z = 0.04 * Math.sin(t * 5); f.tongues.forEach((g, i) => { g.rotation.z = -g.userData.side * (0.45 + 0.12 * Math.sin(t * 8 + i * 2)); g.scale.y = 0.55 + 0.08 * Math.sin(t * 10 + i); });
  f.mouth.scale.set(1 - 0.2 * open + 0.1 * sad, Math.max(0.12, open * 1.6), 1); f.pup.forEach(p => { p.position.x = (p.position.x > 0 ? 0.33 : -0.33) + look[0] * 0.08; p.position.y = -0.02 + look[1] * 0.08 - sad * 0.06; }); f.brows.forEach(b => { const s = b.position.x > 0 ? 1 : -1; b.rotation.z = s * (-0.18 + sad * 0.55); b.position.y = 0.36 - sad * 0.06; }); }
// big wheat stalks (food) and a dinner plate with fork and knife
function bigStalk() { const g = new THREE.Group(); M(cyl(0.045, 0.06, 2.2, 8), toon(0xd9a43a), { ol: 0.02, p: [0, 1.1, 0], to: g }); for (let i = 0; i < 12; i++) { const y = 2.25 + (i >> 1) * 0.13, s = i % 2 ? 1 : -1; M(sph(0.085, 10, 8), toon(0xe8b84a), { ol: 0.015, p: [s * 0.07, y, 0], s: [0.8, 1.5, 0.8], r: [0, 0, -s * 0.35], to: g }); } M(cyl(0.012, 0.004, 0.7, 4), toon(0xe8c86a), { p: [0, 3.2, 0], to: g, cast: false }); g.scale.setScalar(0.62); return g; }
const meal = [0, 1, 2, 3, 4].map(() => { const s = bigStalk(); xp.add(s); return s; });
const plate = new THREE.Group(); xp.add(plate); M(cyl(1.45, 1.15, 0.1, 40), toon(0xf6f4ee), { ol: 0.03, to: plate }); M(new THREE.TorusGeometry(1.2, 0.05, 8, 40), toon(0xd8e4f0), { p: [0, 0.06, 0], r: [Math.PI / 2, 0, 0], to: plate, cast: false });
{ const fk = new THREE.Group(); fk.position.set(-1.75, 0, 0.1); plate.add(fk); M(box(0.1, 0.03, 1.3), toon(0xc8ccd6), { ol: 0.012, to: fk }); for (const x of [-0.08, 0, 0.08]) M(box(0.03, 0.03, 0.4), toon(0xc8ccd6), { p: [x, 0, -0.8], to: fk }); const kn = new THREE.Group(); kn.position.set(1.75, 0, 0.1); plate.add(kn); M(box(0.1, 0.03, 0.8), toon(0x6b4326), { ol: 0.012, p: [0, 0, 0.3], to: kn }); M(box(0.16, 0.02, 0.9), toon(0xc8ccd6), { ol: 0.012, p: [0, 0, -0.55], to: kn }); }
// cartoon car (and a fuel gauge drawn in 2D)
function makeCar(col, len = 3.2, truck = false) { const g = new THREE.Group(); const m = toon(col); M(box(len, 0.8, 1.6), m, { ol: 0.04, p: [0, 0.85, 0], to: g }); M(box(truck ? 1.1 : len * 0.55, 0.75, 1.5), m, { ol: 0.04, p: [truck ? len * 0.36 : -0.1, 1.6, 0], to: g });
  for (const s of [-1, 1]) M(box(truck ? 0.6 : len * 0.2, 0.5, 0.02), flat(0x9ad0f0), { p: [truck ? len * 0.36 : -0.1 + s * len * 0.13, 1.62, 0.76], to: g, cast: false }); M(box(truck ? 0.6 : len * 0.2, 0.5, 0.02), flat(0x9ad0f0), { p: [truck ? len * 0.36 : -0.1, 1.62, -0.76], to: g, cast: false });
  M(box(len + 0.04, 0.12, 1.64), toon(0xf3efe6), { p: [0, 0.75, 0], to: g, cast: false }); for (const s of [-1, 1]) M(sph(0.13, 12, 8), toon(0xffe68a), { ol: 0.012, p: [len / 2, 0.95, s * 0.5], to: g }); M(cyl(0.06, 0.06, 0.3, 8), toon(0x6a6a72), { p: [-len / 2 - 0.1, 0.55, 0.45], r: [0, 0, Math.PI / 2], to: g });
  g.userData.wheels = []; for (const x of [-len * 0.32, len * 0.32]) for (const z of [-0.8, 0.8]) { const w = new THREE.Group(); w.position.set(x, 0.42, z); g.add(w); M(cyl(0.42, 0.42, 0.3, 24), toon(0x1b1522), { ol: 0.02, r: [Math.PI / 2, 0, 0], to: w }); M(cyl(0.2, 0.2, 0.32, 16), toon(0xc8ccd6), { r: [Math.PI / 2, 0, 0], to: w }); M(box(0.06, 0.34, 0.33), toon(0x8a8a96), { to: w, cast: false }); g.userData.wheels.push(w); }
  if (truck) { M(box(len * 0.6, 0.1, 0.5), toon(0xc8ccd6), { ol: 0.015, p: [-0.3, 1.38, 0], to: g }); for (let i = 0; i < 6; i++) M(box(0.05, 0.12, 0.5), toon(0xc8ccd6), { p: [-0.3 - len * 0.27 + i * len * 0.11, 1.45, 0], to: g, cast: false }); M(box(0.5, 0.15, 0.3), toon(0x2f6bd8), { p: [len * 0.36, 2.05, 0], to: g }); }
  return g; }
const car = makeCar(0xd63b2f); xp.add(car);
const truck = makeCar(0xc8302a, 5.0, true); truck.position.set(32.5, 0, -31.5); truck.rotation.y = 0.35; truck.scale.setScalar(0.95); world.add(truck); truck.visible = false;
function gauge(t, v, x = W / 2, y = 470) { ctx.save(); ctx.translate(x, y); ctx.lineWidth = 16; ctx.strokeStyle = INK; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(0, 0, 170, Math.PI, 0); ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.lineWidth = 22; ctx.strokeStyle = '#e8402a'; ctx.beginPath(); ctx.arc(0, 0, 135, Math.PI, Math.PI * 1.22); ctx.stroke(); ctx.strokeStyle = INK; ctx.lineWidth = 8; for (let i = 0; i <= 4; i++) { const a = Math.PI + i * Math.PI / 4; ctx.beginPath(); ctx.moveTo(Math.cos(a) * 150, Math.sin(a) * 150); ctx.lineTo(Math.cos(a) * 118, Math.sin(a) * 118); ctx.stroke(); }
  ctx.font = '64px Pop'; ctx.fillStyle = INK; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('E', -112, -40); ctx.fillText('F', 112, -40); const a = Math.PI + (Math.PI * 0.9) * v + 0.05 * Math.PI + 0.015 * Math.sin(t * 30) * (v > 0.02 ? 1 : 0); ctx.strokeStyle = '#e8402a'; ctx.lineWidth = 12; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.cos(a) * 125, Math.sin(a) * 125); ctx.stroke(); ctx.fillStyle = INK; ctx.beginPath(); ctx.arc(0, 0, 20, 0, 7); ctx.fill(); ctx.restore(); }
// --- firefighters with drip torches (modern) ---
const helmet = hg => { const m = flat(0xd63b2f); M(new THREE.SphereGeometry(0.66, 32, 16, 0, Math.PI * 2, 0, Math.PI * 0.5), m, { ol: 0.045, p: [0, 0.12, -0.03], s: [1.08, 0.82, 1.12], to: hg }); M(cyl(0.95, 0.95, 0.05, 32), m, { ol: 0.035, p: [0, 0.14, -0.12], s: [1, 1, 1.15], to: hg }); M(box(0.08, 0.32, 1.25), m, { ol: 0.02, p: [0, 0.62, -0.05], to: hg }); M(box(0.3, 0.3, 0.05), flat(0xf2c230), { ol: 0.015, p: [0, 0.45, 0.66], r: [-0.4, 0, 0], to: hg }); };
const ffBody = (g, w, h) => { g.fillStyle = '#e8b830'; g.fillRect(0, 0, w, h); for (const y of [0.62, 0.8]) { g.fillStyle = '#c8ccd6'; g.fillRect(0, h * y, w, h * 0.06); g.fillStyle = 'rgba(255,255,255,0.6)'; g.fillRect(0, h * y + 4, w, 4); } g.fillStyle = '#1b1522'; g.fillRect(w * 0.49, 0, w * 0.02, h); };
const ffs = [0, 1].map(i => makeChar3({ stache: i === 1, shoe: 0x1b1522, belt3d: 0x1b1522, body: ffBody, hat: helmet })); ffs.forEach(c => { root.add(c.g); SETS.push(c.g); });
function dripTorch() { const g = new THREE.Group(); M(cyl(0.16, 0.16, 0.5, 16), toon(0xd63b2f), { ol: 0.015, to: g }); M(new THREE.TorusGeometry(0.14, 0.03, 6, 16, Math.PI), toon(0x1b1522), { p: [0, 0.27, 0], to: g }); const sp = M(cyl(0.025, 0.025, 0.8, 6), toon(0x8a8a96), { ol: 0.01, p: [0.3, 0.1, 0.3], r: [0.9, 0, -0.6], to: g }); g.userData.tip = V(0.62, -0.2, 0.62); root.add(g); SETS.push(g); return g; }
const drips = [dripTorch(), dripTorch()];
// full-story field state, mood and forest colour, called from farmLook
function fieldState(t) { const c5 = CUT(5), c14 = CUT(14), c15 = CUT(15);
  stripTo(t < c5 ? 2 : t < CUT(6) ? lerp(2, 27, cl((t - c5 - 0.15) / (wf(5, 'raked') - 0.2 - c5 - 0.15))) : 27);
  neighTo(t < c14 ? -100 : t < c15 ? lerp(Z1 - 1, Z0 + 1.5, cl((t - c14 - 0.15) / (c15 - c14 - 0.3))) : 100);
  pineM.color.copy(t > CUT(13) + 0.8 && t < CUT(22) || t > CUT(23) ? PINE_B : PINE_G); sunDisc.scale.setScalar(1); sunDisc.material.depthTest = true; sunDisc.material.transparent = false; sunDisc.renderOrder = 0; lone.visible = false; truck.visible = false; }
const _farmLook1 = farmLook; farmLook = function (t, d) { root.fog = FOG; _farmLook1(t, d); fieldState(t); };
