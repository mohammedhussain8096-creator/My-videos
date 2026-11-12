import * as THREE from 'three';

const W = 1080, H = 1920, INK = '#1b1522';
const out = document.getElementById('out'), ctx = out.getContext('2d');
const glc = document.createElement('canvas'); glc.width = W; glc.height = H;
const renderer = new THREE.WebGLRenderer({ canvas: glc, antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H, false);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFShadowMap;
const root = new THREE.Scene();
const cam = new THREE.PerspectiveCamera(40, W / H, 0.1, 100);

// ---------- helpers ----------
const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, k) => a + (b - a) * k;
const ss = (a, b, x) => { const k = cl((x - a) / (b - a)); return k * k * (3 - 2 * k); };
const back = k => { k = cl(k); const c = 1.9; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); };
const V = (x, y, z) => new THREE.Vector3(x, y, z);

const grad = new THREE.DataTexture(new Uint8Array([95, 95, 95, 255, 175, 175, 175, 255, 255, 255, 255, 255, 255, 255, 255, 255]), 4, 1);
grad.minFilter = grad.magFilter = THREE.NearestFilter; grad.needsUpdate = true;
const toon = (color, o = {}) => new THREE.MeshToonMaterial({ color, gradientMap: grad, ...o });
const flat = (color, o = {}) => new THREE.MeshBasicMaterial({ color, ...o });
const BOIL = { value: 0 };
const outlineMat = th => new THREE.ShaderMaterial({
  side: THREE.BackSide, uniforms: { th: { value: th * 1.25 }, bt: BOIL },
  vertexShader: 'uniform float th; uniform float bt; void main(){ vec3 p = position; float n = sin(p.x*9.0+bt*2.1)*sin(p.y*7.0-bt*1.7)*sin(p.z*8.0+bt*1.3); gl_Position = projectionMatrix*modelViewMatrix*vec4(p+normal*th*(1.0+0.18*n),1.0); }',
  fragmentShader: 'void main(){ gl_FragColor = vec4(0.085,0.065,0.11,1.0); }'
});
function M(geo, mat, o = {}) {
  const m = new THREE.Mesh(geo, mat);
  m.castShadow = o.cast !== false; m.receiveShadow = !!o.recv;
  if (o.ol) { const ol = new THREE.Mesh(geo, outlineMat(o.ol)); m.add(ol); m.userData.ol = ol; }
  if (o.p) m.position.set(...o.p); if (o.r) m.rotation.set(...o.r); if (o.s) m.scale.set(...o.s);
  if (o.to) o.to.add(m);
  return m;
}
const box = (w, h, d) => new THREE.BoxGeometry(w, h, d);
const cyl = (a, b, h, n = 24, open = false) => new THREE.CylinderGeometry(a, b, h, n, 1, open);
const sph = (r, a = 32, b = 20) => new THREE.SphereGeometry(r, a, b);
function ctex(w, h, draw) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d'); draw(g, w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; t.userData = { c, g }; return t;
}
const UNIT = cyl(1, 1, 1, 8); UNIT.translate(0, 0.5, 0);
const UP = V(0, 1, 0);
function seg(mesh, a, b, r) {
  const d = b.clone().sub(a), L = d.length();
  mesh.position.copy(a); mesh.quaternion.setFromUnitVectors(UP, d.normalize()); mesh.scale.set(r, L, r);
}

// ---------- character ----------
function drawFace(g, e, o) {
  const cx = 512, cy = 262;
  g.fillStyle = o.skin; g.fillRect(0, 0, 1024, 512);
  g.lineCap = 'round'; g.lineJoin = 'round'; g.strokeStyle = INK; g.fillStyle = INK;
  // cheeks
  g.fillStyle = 'rgba(235,120,100,0.28)';
  for (const s of [-1, 1]) { g.beginPath(); g.arc(cx + s * 92, cy + 34, 20, 0, 7); g.fill(); }
  if (o.mask) { g.fillStyle = '#17131c'; g.fillRect(cx - 420, cy - 52, 840, 78); }
  const ex = 54, ey = cy - 14;
  for (const s of [-1, 1]) {
    const x = cx + s * ex;
    g.lineWidth = 11; g.strokeStyle = o.mask ? '#fff' : INK; g.fillStyle = o.mask ? '#fff' : INK;
    if (e === 'happy') { g.beginPath(); g.arc(x, ey + 12, 22, Math.PI * 1.12, Math.PI * 1.88); g.stroke(); }
    else if (e === 'shock') {
      g.fillStyle = '#fff'; g.strokeStyle = INK; g.lineWidth = 9; g.beginPath(); g.arc(x, ey, 31, 0, 7); g.fill(); g.stroke();
      g.fillStyle = INK; g.beginPath(); g.arc(x + 3, ey + 2, 10, 0, 7); g.fill();
    }
    else if (e === 'sneaky') {
      g.beginPath(); g.moveTo(x - 24, ey - 6); g.lineTo(x + 24, ey - 6); g.stroke();
      g.beginPath(); g.arc(x + s * -6, ey + 8, 10, 0, 7); g.fill();
    }
    else if (e === 'angry') {
      g.beginPath(); g.arc(x, ey + 6, 11, 0, 7); g.fill();
      g.lineWidth = 13; g.strokeStyle = o.mask ? '#fff' : INK; g.beginPath(); g.moveTo(x - s * 30, ey - 34); g.lineTo(x + s * 22, ey - 14); g.stroke();
    }
    else if (e === 'sad') {
      g.beginPath(); g.arc(x, ey + 6, 10, 0, 7); g.fill();
      g.lineWidth = 11; g.beginPath(); g.moveTo(x - s * 26, ey - 18); g.lineTo(x + s * 22, ey - 34); g.stroke();
    }
    else if (e === 'think') {
      g.beginPath(); g.arc(x + 9, ey - 6, 10, 0, 7); g.fill();
      g.lineWidth = 11; g.beginPath(); g.moveTo(x - 24, ey - 36 - (s > 0 ? 10 : 0)); g.lineTo(x + 24, ey - 36 - (s > 0 ? 10 : 0)); g.stroke();
    }
    else if (e === 'sleep') { g.beginPath(); g.arc(x, ey - 10, 20, 0.12 * Math.PI, 0.88 * Math.PI); g.stroke(); }
    else { g.beginPath(); g.arc(x, ey, 11, 0, 7); g.fill(); }
  }
  // mouth
  g.strokeStyle = INK; g.fillStyle = INK; g.lineWidth = 10; const my = cy + 52;
  if (e === 'happy') { g.fillStyle = '#7a1f2b'; g.beginPath(); g.arc(cx, my - 8, 34, 0.08 * Math.PI, 0.92 * Math.PI); g.closePath(); g.fill(); g.stroke(); }
  else if (e === 'shock') { g.fillStyle = '#7a1f2b'; g.beginPath(); g.ellipse(cx, my + 6, 17, 23, 0, 0, 7); g.fill(); g.stroke(); }
  else if (e === 'sneaky') { g.beginPath(); g.moveTo(cx - 30, my + 2); g.quadraticCurveTo(cx + 8, my + 18, cx + 38, my - 12); g.stroke(); }
  else if (e === 'angry') {
    g.fillStyle = '#fff'; g.beginPath(); g.roundRect(cx - 40, my - 10, 80, 34, 9); g.fill(); g.stroke();
    g.lineWidth = 5; for (let i = -1; i <= 1; i++) { g.beginPath(); g.moveTo(cx + i * 20, my - 10); g.lineTo(cx + i * 20, my + 24); g.stroke(); }
    g.beginPath(); g.moveTo(cx - 40, my + 7); g.lineTo(cx + 40, my + 7); g.stroke();
  }
  else if (e === 'sad') { g.beginPath(); g.arc(cx, my + 30, 30, 1.2 * Math.PI, 1.8 * Math.PI); g.stroke(); }
  else if (e === 'think') { g.beginPath(); g.moveTo(cx - 14, my + 4); g.lineTo(cx + 26, my - 4); g.stroke(); }
  else { g.beginPath(); g.moveTo(cx - 22, my); g.lineTo(cx + 22, my); g.stroke(); }
  if (o.stache) {
    g.fillStyle = '#3a2416'; g.strokeStyle = INK; g.lineWidth = 6;
    for (const s of [-1, 1]) { g.beginPath(); g.moveTo(cx, cy + 22); g.quadraticCurveTo(cx + s * 40, cy + 6, cx + s * 78, cy + 36); g.quadraticCurveTo(cx + s * 36, cy + 48, cx, cy + 36); g.closePath(); g.fill(); g.stroke(); }
  }
  if (o.stubble) { g.fillStyle = 'rgba(40,30,40,0.35)'; for (let i = 0; i < 60; i++) { const a = (i * 2.4) % 6.28, r = 40 + (i * 37) % 60; g.fillRect(cx + Math.cos(a) * r * 1.3, cy + 70 + Math.abs(Math.sin(a)) * r * 0.5, 4, 4); } }
}
function makeChar(o) {
  const c = { g: new THREE.Group(), o, expr: null };
  const up = new THREE.Group(); c.g.add(up); c.up = up;
  const bt = ctex(512, 512, o.body);
  c.body = M(new THREE.CapsuleGeometry(0.3, 0.5, 10, 28), toon(0xffffff, { map: bt }), { ol: 0.035, p: [0, 1.25, 0], r: [0, Math.PI, 0], to: up });
  c.headG = new THREE.Group(); c.headG.position.set(0, 2.16, 0); up.add(c.headG);
  c.ft = ctex(1024, 512, g => drawFace(g, 'neutral', o));
  c.head = M(sph(0.46, 48, 32), toon(0xffffff, { map: c.ft }), { ol: 0.035, r: [0, -Math.PI / 2, 0], to: c.headG });
  c.hatG = new THREE.Group(); c.headG.add(c.hatG); if (o.hat) o.hat(c.hatG);
  const lm = flat(INK), sk = toon(o.skin);
  c.arms = [-1, 1].map(s => ({ s, a: M(UNIT, lm, { cast: true, to: up }), b: M(UNIT, lm, { to: up }), h: M(sph(0.085, 16, 12), sk, { ol: 0.025, to: up }) }));
  c.legs = [-1, 1].map(s => ({ s, a: M(UNIT, lm, { to: c.g }), f: M(sph(0.11, 16, 12), toon(o.shoe || 0x2a2230), { ol: 0.025, s: [1, 0.6, 1.5], to: c.g }) }));
  c.face = e => { if (c.expr !== e) { c.expr = e; drawFace(c.ft.userData.g, e, o); c.ft.needsUpdate = true; } };
  c.pose = (p = {}) => {
    const bob = p.bob || 0; up.position.y = bob; up.rotation.z = p.lean || 0; up.rotation.x = p.pitch || 0;
    c.headG.rotation.set(p.hx || 0, p.hy || 0, p.hz || 0);
    const hands = [p.lh || [-0.5, 1.02, 0.08], p.rh || [0.5, 1.02, 0.08]];
    c.arms.forEach((A, i) => {
      const sh = V(A.s * 0.27, 1.62, 0), hd = V(...hands[i]);
      const mid = sh.clone().lerp(hd, 0.5).add(V(A.s * 0.1, -0.1, -0.06));
      seg(A.a, sh, mid, 0.034); seg(A.b, mid, hd, 0.034); A.h.position.copy(hd);
    });
    const feet = [p.lf || [-0.15, 0, 0], p.rf || [0.15, 0, 0]];
    c.legs.forEach((Lg, i) => {
      const hip = V(Lg.s * 0.13, 0.78 + bob, 0), ft = V(feet[i][0], feet[i][1] + 0.07, feet[i][2]);
      seg(Lg.a, ft, hip, 0.034); Lg.f.position.copy(ft).add(V(0, 0, 0.06));
    });
  };
  c.walk = (ph, amp = 0.22) => ({ lf: [-0.15, Math.max(0, Math.sin(ph)) * 0.16, Math.cos(ph) * amp], rf: [0.15, Math.max(0, -Math.sin(ph)) * 0.16, -Math.cos(ph) * amp], bob: Math.abs(Math.sin(ph)) * 0.05 });
  c.face('neutral'); c.pose();
  return c;
}
const SKIN = '#f6c9a0', SKIN2 = '#f0b98c';
const thiefOpts = {
  skin: SKIN, mask: true, stubble: true, shoe: 0x2a2230,
  body: (g, w, h) => { for (let i = 0; i < 9; i++) { g.fillStyle = i % 2 ? '#f3efe6' : '#23202b'; g.fillRect(0, i * h / 9, w, h / 9 + 1); } g.fillStyle = '#3b4a7a'; g.fillRect(0, h * 0.74, w, h * 0.26); },
  hat: hg => {
    const m = toon(0x4a4f63);
    M(sph(0.47, 32, 16), m, { ol: 0.035, p: [0, 0.2, -0.02], s: [1.06, 0.48, 1.08], to: hg });
    M(cyl(0.3, 0.3, 0.05, 24), m, { ol: 0.03, p: [0, 0.2, 0.42], s: [1.1, 1, 0.8], r: [0.25, 0, 0], to: hg });
    M(sph(0.05), m, { ol: 0.02, p: [0, 0.44, -0.02], to: hg });
  }
};
const engOpts = {
  skin: SKIN2, stache: true, shoe: 0x3a2416,
  body: (g, w, h) => {
    g.fillStyle = '#f3efe6'; g.fillRect(0, 0, w, h); g.fillStyle = '#2f6b4f'; g.fillRect(w * 0.12, 0, w * 0.76, h * 0.72);
    g.fillStyle = '#f3efe6'; g.beginPath(); g.moveTo(w * 0.42, 0); g.lineTo(w * 0.5, h * 0.3); g.lineTo(w * 0.58, 0); g.fill();
    g.fillStyle = '#b3272d'; g.beginPath(); g.moveTo(w * 0.47, h * 0.02); g.lineTo(w * 0.53, h * 0.02); g.lineTo(w * 0.515, h * 0.26); g.lineTo(w * 0.485, h * 0.26); g.fill();
    g.fillStyle = '#f2c230'; for (let i = 0; i < 3; i++) { g.beginPath(); g.arc(w * 0.5, h * (0.38 + i * 0.11), 9, 0, 7); g.fill(); }
    g.fillStyle = '#3a3345'; g.fillRect(0, h * 0.72, w, h * 0.28);
  },
  hat: hg => {
    const m = toon(0x2a2530);
    M(sph(0.36, 32, 16, 0, 6.3, 0, Math.PI / 2), m, { ol: 0.035, p: [0, 0.3, 0], s: [1, 1.05, 1], to: hg });
    M(cyl(0.56, 0.56, 0.05, 32), m, { ol: 0.03, p: [0, 0.3, 0], to: hg });
    M(cyl(0.365, 0.365, 0.09, 32), toon(0xb3272d), { p: [0, 0.37, 0], to: hg });
  }
};

// ---------- lights ----------
const hemi = new THREE.HemisphereLight(0xffffff, 0x554433, 1); root.add(hemi);
const sun = new THREE.DirectionalLight(0xffffff, 2); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, { left: -8, right: 8, top: 9, bottom: -3, near: 0.5, far: 40 }); sun.shadow.bias = -0.0015;
root.add(sun); root.add(sun.target);
function light(h, s, pos, hc = 0xfff1dc, gc = 0x4a3a44) { hemi.intensity = h; hemi.color.set(hc); hemi.groundColor.set(gc); sun.intensity = s; sun.position.set(...pos); sun.target.position.set(0, 1.5, 0); }

// ---------- overlay text ----------
function popText(text, x, y, size, col, t, t0, t1, o = {}) {
  if (t < t0 || t > t1) return;
  const s = back((t - t0) / 0.2) * (1 - ss(t1 - 0.1, t1, t)) * (1 + 0.025 * Math.sin((t - t0) * 9));
  ctx.save(); ctx.translate(x, y); ctx.rotate((o.rot || 0) + 0.02 * Math.sin((t - t0) * 6)); ctx.scale(s, s);
  ctx.font = `${size}px ${o.font || 'Pop'}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.lineJoin = 'round';
  ctx.strokeStyle = INK; ctx.lineWidth = size * 0.24; ctx.strokeText(text, 5, 9); ctx.strokeText(text, 0, 0);
  ctx.fillStyle = col; ctx.fillText(text, 0, 0);
  ctx.restore();
}
function burst(text, x, y, r, t, t0, t1, rot = -0.12) {
  if (t < t0 || t > t1) return;
  const s = back((t - t0) / 0.16) * (1 - ss(t1 - 0.08, t1, t));
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot + 0.04 * Math.sin(t * 30)); ctx.scale(s, s);
  ctx.beginPath(); const n = 14; for (let i = 0; i < n * 2; i++) { const a = i / (n * 2) * Math.PI * 2, rr = i % 2 ? r * 0.68 : r * (0.95 + 0.12 * ((i * 7) % 3)); ctx.lineTo(Math.cos(a) * rr * 1.25, Math.sin(a) * rr * 0.8); } ctx.closePath();
  ctx.fillStyle = '#e42a2a'; ctx.strokeStyle = '#fff'; ctx.lineWidth = 12; ctx.lineJoin = 'round'; ctx.stroke(); ctx.fill();
  ctx.font = `${r * 0.6}px Pop`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.strokeStyle = INK; ctx.lineWidth = 16; ctx.strokeText(text, 0, 6); ctx.fillStyle = '#fff'; ctx.fillText(text, 0, 6);
  ctx.restore();
}
function proj(v) { const p = v.clone().project(cam); return [(p.x + 1) / 2 * W, (1 - p.y) / 2 * H]; }
function drops(c, u) { const [hx, hy] = proj(c.headG.getWorldPosition(V(0, 0, 0))); ctx.fillStyle = '#8fd8ff'; ctx.strokeStyle = INK; ctx.lineWidth = 6; for (let i = 0; i < 3; i++) { const p = ((u * 2.2 + i * 0.33) % 1); const a = -2.5 + i * 0.5; const x = hx + Math.cos(a) * (190 + p * 150), y = hy + Math.sin(a) * (190 + p * 150) + p * p * 120; ctx.beginPath(); ctx.ellipse(x, y, 13, 21, a + 1.57, 0, 7); ctx.fill(); ctx.stroke(); } }
function caption(t) {
  for (const L of TM.lines) for (const w of L.words) if (t >= w.s && t < w.e) {
    const s = 0.84 + 0.16 * back((t - w.s) / 0.09);
    ctx.save(); ctx.translate(W / 2, H * 0.695); ctx.scale(s, s);
    ctx.font = '62px Pop'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.lineJoin = 'round';
    ctx.strokeStyle = '#0d0a12'; ctx.lineWidth = 15; ctx.strokeText(w.w, 0, 4); ctx.strokeText(w.w, 0, 0);
    ctx.fillStyle = '#fff'; ctx.fillText(w.w, 0, 0); ctx.restore(); return;
  }
}

// ---------- painterly textures ----------
function paintTex(base, opts = {}) {
  return ctex(512, 512, (g, w, h) => {
    g.fillStyle = base; g.fillRect(0, 0, w, h); let sd = opts.seed || 11; const r = () => (sd = (sd * 16807) % 2147483647) / 2147483647;
    for (let i = 0; i < (opts.blot || 260); i++) { g.fillStyle = `rgba(${r() < 0.5 ? '0,0,0' : '255,255,255'},${0.03 + r() * 0.05})`; g.beginPath(); g.ellipse(r() * w, r() * h, 8 + r() * 40, 4 + r() * 18, r() * 3, 0, 7); g.fill(); }
    if (opts.strokes) { g.strokeStyle = opts.strokes; g.lineCap = 'round'; for (let i = 0; i < (opts.n || 140); i++) { const x = r() * w, y = r() * h, a = (opts.ang ?? -1.4) + (r() - 0.5) * 0.6, L = 6 + r() * (opts.len || 18); g.lineWidth = 1.5 + r() * 2.5; g.globalAlpha = 0.25 + r() * 0.35; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * L, y + Math.sin(a) * L); g.stroke(); } g.globalAlpha = 1; }
    if (opts.cracks) { g.strokeStyle = 'rgba(27,21,34,0.45)'; g.lineWidth = 2.5; for (let i = 0; i < opts.cracks; i++) { let x = r() * w, y = r() * h; g.beginPath(); g.moveTo(x, y); for (let k = 0; k < 4; k++) { x += (r() - 0.5) * 50; y += (r() - 0.5) * 50; g.lineTo(x, y); } g.stroke(); } }
    if (opts.weave) { g.strokeStyle = 'rgba(0,0,0,0.12)'; g.lineWidth = 2; for (let i = 0; i < w; i += 10) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); } }
  });
}
const rep_ = (t, a, b) => { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(a, b); return t; };
const TX = {
  grass: rep_(paintTex('#86c25e', { strokes: '#5f9a3f', n: 420, len: 22, blot: 200 }), 30, 30),
  asphalt: rep_(paintTex('#55525e', { blot: 420, cracks: 6, seed: 5 }), 24, 1.2),
  wall: rep_(paintTex('#f1e6cf', { blot: 160, seed: 7 }), 3, 1),
  carpet: rep_(paintTex('#7a3b4a', { weave: true, blot: 120, seed: 3 }), 6, 2),
  seat: rep_(paintTex('#2f6fb0', { weave: true, blot: 80, seed: 9 }), 1, 1),
  hangar: rep_(paintTex('#9aa3b5', { strokes: 'rgba(27,21,34,0.25)', ang: 1.57, n: 90, len: 60, seed: 13 }), 4, 2),
};
let TM, Ls, DUR = 54;
let overlay = () => { };
// ---------- textures ----------
TX.planks = rep_(ctex(512, 512, (g, w, h) => { g.fillStyle = '#9a6a3c'; g.fillRect(0, 0, w, h); let sd = 5; const r = () => (sd = (sd * 16807) % 2147483647) / 2147483647; for (let i = 0; i < 8; i++) { g.fillStyle = `rgba(${r() < 0.5 ? '60,30,10' : '255,220,170'},${0.05 + r() * 0.1})`; g.fillRect(0, i * 64, w, 64); g.fillStyle = '#4a2e18'; g.fillRect(0, i * 64, w, 4); g.strokeStyle = 'rgba(70,40,20,0.35)'; g.lineWidth = 2; for (let k = 0; k < 5; k++) { const y = i * 64 + 10 + r() * 46; g.beginPath(); g.moveTo(0, y); g.bezierCurveTo(w * 0.3, y + (r() - 0.5) * 14, w * 0.6, y + (r() - 0.5) * 14, w, y); g.stroke(); } g.fillStyle = '#4a2e18'; g.fillRect(r() * w, i * 64, 4, 64); } }), 3, 3);
TX.plaster = ctex(1024, 640, (g, w, h) => { g.fillStyle = '#ead9b4'; g.fillRect(0, 0, w, h); let sd = 9; const r = () => (sd = (sd * 16807) % 2147483647) / 2147483647; for (let i = 0; i < 240; i++) { g.fillStyle = `rgba(${r() < 0.5 ? '120,90,50' : '255,255,240'},${0.03 + r() * 0.05})`; g.beginPath(); g.ellipse(r() * w, r() * h, 10 + r() * 50, 6 + r() * 24, r() * 3, 0, 7); g.fill(); } g.fillStyle = '#4a2e1c'; for (const x of [0, 250, 510, 770, 1000]) g.fillRect(x, 0, 24, h); g.fillRect(0, 0, w, 26); g.fillRect(0, 300, w, 22); g.fillRect(0, h - 70, w, 70); g.save(); g.translate(130, 160); g.rotate(-0.7); g.fillRect(-190, -9, 380, 18); g.restore(); g.save(); g.translate(890, 160); g.rotate(0.7); g.fillRect(-190, -9, 380, 18); g.restore(); });
TX.brick = rep_(ctex(256, 256, (g, w, h) => { g.fillStyle = '#6b4636'; g.fillRect(0, 0, w, h); let sd = 3; const r = () => (sd = (sd * 16807) % 2147483647) / 2147483647; for (let y = 0; y < h; y += 32) for (let x = (y / 32 % 2) * 32 - 64; x < w; x += 64) { g.fillStyle = `hsl(${12 + r() * 10},${38 + r() * 14}%,${34 + r() * 12}%)`; g.fillRect(x + 3, y + 3, 58, 26); } }), 4, 3);
TX.cobble = rep_(ctex(256, 256, (g, w, h) => { g.fillStyle = '#5b5560'; g.fillRect(0, 0, w, h); let sd = 13; const r = () => (sd = (sd * 16807) % 2147483647) / 2147483647; for (let y = 0; y < h; y += 32) for (let x = (y / 32 % 2) * 20 - 40; x < w; x += 40) { g.fillStyle = `hsl(${260 + r() * 20},8%,${44 + r() * 16}%)`; g.beginPath(); g.ellipse(x + 20, y + 16, 17, 13, 0, 0, 7); g.fill(); } }), 5, 14);
TX.earth = rep_(ctex(256, 256, (g, w, h) => { g.fillStyle = '#6a4a30'; g.fillRect(0, 0, w, h); let sd = 23; const r = () => (sd = (sd * 16807) % 2147483647) / 2147483647; for (let i = 0; i < 60; i++) { g.fillStyle = `rgba(${r() < 0.5 ? '40,25,15' : '150,120,90'},${0.25 + r() * 0.3})`; g.beginPath(); g.ellipse(r() * w, r() * h, 5 + r() * 16, 4 + r() * 10, r() * 3, 0, 7); g.fill(); } }), 2, 3);
function houseTex(seed, plaster) { return ctex(512, 640, (g, w, h) => { g.fillStyle = plaster; g.fillRect(0, 0, w, h); let sd = seed; const r = () => (sd = (sd * 16807) % 2147483647) / 2147483647; for (let i = 0; i < 120; i++) { g.fillStyle = `rgba(90,60,30,${0.03 + r() * 0.05})`; g.beginPath(); g.ellipse(r() * w, r() * h, 10 + r() * 40, 6 + r() * 20, r() * 3, 0, 7); g.fill(); } g.fillStyle = '#3d2718'; for (const x of [0, 160, 336, 494]) g.fillRect(x, 0, 18, h); for (const y of [0, 210, 420, 622]) g.fillRect(0, y, w, 18); for (const [cx, cy, a] of [[88, 115, -0.8], [424, 115, 0.8], [88, 520, 0.8], [424, 520, -0.8]]) { g.save(); g.translate(cx, cy); g.rotate(a); g.fillRect(-130, -7, 260, 14); g.restore(); }
  for (const [x, y] of [[196, 60], [196, 262]]) { g.fillStyle = '#3d2718'; g.fillRect(x, y, 124, 124); g.fillStyle = r() < 0.6 ? '#ffd27a' : '#31405e'; g.fillRect(x + 10, y + 10, 104, 104); g.fillStyle = '#3d2718'; g.fillRect(x + 58, y, 8, 124); g.fillRect(x, y + 58, 124, 8); }
  g.fillStyle = '#3d2718'; g.fillRect(200, 452, 116, 188); g.fillStyle = '#6b4326'; g.fillRect(210, 462, 96, 178); g.fillStyle = '#d9a53a'; g.beginPath(); g.arc(290, 556, 7, 0, 7); g.fill(); }); }

// ---------- reference-style flat characters ----------
function eggGeo() { const pts = []; for (let i = 0; i <= 18; i++) { const s = i / 18, y = s * 1.08; const r = 0.36 * Math.pow(Math.sin(Math.PI * Math.pow(s, 0.72)), 0.62) * (1 - 0.18 * s); pts.push(new THREE.Vector2(Math.max(0.001, r), y)); } return new THREE.LatheGeometry(pts, 32); }
const EGG = eggGeo();
function drawFace2(g, e, o) {
  drawFace(g, e, o);
  // soft baked shading instead of scene lighting
  const sh = g.createRadialGradient(440, 200, 60, 512, 262, 330); sh.addColorStop(0, 'rgba(255,255,255,0.10)'); sh.addColorStop(0.6, 'rgba(0,0,0,0)'); sh.addColorStop(1, 'rgba(60,20,40,0.22)'); g.fillStyle = sh; g.fillRect(256, 0, 512, 512);
  if (o.freckles) { g.fillStyle = 'rgba(190,100,60,0.75)'; for (const s of [-1, 1]) for (const [dx, dy] of [[0, 0], [14, 8], [-12, 10], [4, 20]]) { g.beginPath(); g.arc(512 + s * 96 + dx, 300 + dy, 4.5, 0, 7); g.fill(); } }
}
function makeChar2(o) {
  const c = { g: new THREE.Group(), o, expr: null }; const up = new THREE.Group(); c.g.add(up); c.up = up;
  const HIP = 1.18, HEADY = HIP + 1.08 + 0.36;
  const bt = ctex(512, 512, (g, w, h) => { o.body(g, w, h); const sh = g.createLinearGradient(0, 0, w, 0); sh.addColorStop(0, 'rgba(40,10,40,0.20)'); sh.addColorStop(0.35, 'rgba(0,0,0,0)'); sh.addColorStop(0.6, 'rgba(255,255,255,0.06)'); sh.addColorStop(0.85, 'rgba(0,0,0,0)'); sh.addColorStop(1, 'rgba(40,10,40,0.20)'); g.fillStyle = sh; g.fillRect(0, 0, w, h); });
  c.bodyM = flat(0xffffff, { map: bt }); c.body = M(EGG, c.bodyM, { ol: 0.04, p: [0, HIP - 0.04, 0], r: [0, Math.PI, 0], to: up });
  c.headG = new THREE.Group(); c.headG.position.set(0, HEADY, 0); up.add(c.headG);
  c.ft = ctex(1024, 512, g => drawFace2(g, 'neutral', o)); c.headM = flat(0xffffff, { map: c.ft });
  c.head = M(sph(0.46, 48, 32), c.headM, { ol: 0.042, r: [0, -Math.PI / 2, 0], to: c.headG });
  c.hatG = new THREE.Group(); c.headG.add(c.hatG); if (o.hat) o.hat(c.hatG);
  const armM = flat(o.arm ?? 0x1b1522), legM = flat(o.leg ?? 0x1b1522), sk = flat(new THREE.Color(o.skin).multiplyScalar(0.96));
  c.arms = [-1, 1].map(s => ({ s, a: M(UNIT, armM, { to: up }), b: M(UNIT, armM, { to: up }), h: M(sph(0.055, 12, 10), sk, { ol: 0.022, to: up }) }));
  c.legs = [-1, 1].map(s => ({ s, a: M(UNIT, legM, { to: c.g }), f: M(sph(0.1, 14, 10), flat(o.shoe || 0x3a2416), { ol: 0.022, s: [1, 0.5, 1.6], to: c.g }) }));
  c.mats = [c.bodyM, c.headM, sk];
  c.tint = hex => c.mats.forEach(m => m.color.set(hex));
  c.face = e => { if (c.expr !== e) { c.expr = e; drawFace2(c.ft.userData.g, e, o); c.ft.needsUpdate = true; } };
  c.pose = (p = {}) => {
    const bob = p.bob || 0; up.position.y = bob; up.rotation.z = p.lean || 0; up.rotation.x = p.pitch || 0;
    c.headG.rotation.set(p.hx || 0, p.hy || 0, p.hz || 0);
    const hands = [p.lh || [-0.44, 1.42, 0.05], p.rh || [0.44, 1.42, 0.05]];
    c.arms.forEach((A, i) => { const sh = V(A.s * 0.25, HIP + 0.86, 0), hd = V(...hands[i]); const mid = sh.clone().lerp(hd, 0.5).add(V(A.s * 0.08, -0.08, -0.05)); seg(A.a, sh, mid, 0.026); seg(A.b, mid, hd, 0.026); A.h.position.copy(hd); });
    const feet = [p.lf || [-0.13, 0, 0], p.rf || [0.13, 0, 0]];
    c.legs.forEach((Lg, i) => { const hip = V(Lg.s * 0.12, HIP + 0.05 + bob, 0), ft = V(feet[i][0], feet[i][1] + 0.05, feet[i][2]); seg(Lg.a, ft, hip, 0.03); Lg.f.position.copy(ft).add(V(0, 0, 0.07)); });
  };
  c.walk = (ph, amp = 0.26) => ({ lf: [-0.13, Math.max(0, Math.sin(ph)) * 0.2, Math.cos(ph) * amp], rf: [0.13, Math.max(0, -Math.sin(ph)) * 0.2, -Math.cos(ph) * amp], bob: Math.abs(Math.sin(ph)) * 0.05 });
  c.HEADY = HEADY; c.face('neutral'); c.pose(); return c;
}
const flatHat = (col, brim) => hg => { const m = flat(col); M(sph(0.475, 32, 16, 0, 6.3, 0, Math.PI * 0.36), m, { ol: 0.035, p: [0, 0.1, -0.03], s: [1.08, 0.8, 1.1], to: hg }); M(cyl(0.3, 0.32, 0.05, 24), flat(brim), { ol: 0.03, p: [0, 0.27, 0.4], s: [1.05, 1, 0.6], r: [0.1, 0, 0], to: hg }); M(sph(0.045), m, { ol: 0.02, p: [0, 0.42, -0.03], to: hg }); };
// ---------- reference-style characters: big white heads, heavy outline, tall coat bodies ----------
function drawFace3(g, e, o) {
  drawFace(g, e, { ...o, skin: '#fcfbf6' });
  const cx = 512, cy = 262, ey = cy - 14; g.strokeStyle = INK; g.lineCap = 'round'; g.lineWidth = 16;
  if (['happy', 'neutral', 'shock', 'sneaky'].includes(e)) for (const s of [-1, 1]) { const x = cx + s * 54, lift = e === 'shock' ? 22 : 0; g.beginPath(); g.moveTo(x - 30, ey - 48 - lift + (e === 'sneaky' ? -s * 10 : 0)); g.quadraticCurveTo(x, ey - 64 - lift, x + 30, ey - 48 - lift + (e === 'sneaky' ? s * 10 : 0)); g.stroke(); }
  if (o.wrinkles) { g.lineWidth = 7; g.strokeStyle = 'rgba(27,21,34,0.55)'; for (const s of [-1, 1]) { g.beginPath(); g.moveTo(cx + s * 120, cy + 40); g.lineTo(cx + s * 150, cy + 70); g.stroke(); } g.beginPath(); g.moveTo(cx - 40, cy - 110); g.lineTo(cx + 40, cy - 110); g.stroke(); }
  if (o.beard) { g.fillStyle = o.beard; g.strokeStyle = INK; g.lineWidth = 10; g.beginPath(); g.moveTo(cx - 120, cy + 60); g.quadraticCurveTo(cx - 90, cy + 190, cx, cy + 215); g.quadraticCurveTo(cx + 90, cy + 190, cx + 120, cy + 60); g.quadraticCurveTo(cx + 60, cy + 95, cx, cy + 92); g.quadraticCurveTo(cx - 60, cy + 95, cx - 120, cy + 60); g.closePath(); g.fill(); g.stroke(); }
  if (o.freckles) { g.fillStyle = 'rgba(190,110,70,0.8)'; for (const s of [-1, 1]) for (const [dx, dy] of [[0, 0], [14, 8], [-12, 10], [4, 20]]) { g.beginPath(); g.arc(cx + s * 100 + dx, cy + 40 + dy, 4.5, 0, 7); g.fill(); } }
}
const TUBE = (() => { const pts = []; for (let i = 0; i <= 20; i++) { const s = i / 20, y = s * 1.5; const r = 0.34 * Math.min(1, Math.pow(Math.sin(Math.PI * Math.pow(s, 0.6)), 0.35) * 1.15) * (1 - 0.12 * s); pts.push(new THREE.Vector2(Math.max(0.001, r), y)); } return new THREE.LatheGeometry(pts, 32); })();
function makeChar3(o) {
  const c = { g: new THREE.Group(), o, expr: null }; const up = new THREE.Group(); c.g.add(up); c.up = up;
  const HIP = 1.5, HEADY = HIP + 1.5 + 0.44;
  const bt = ctex(512, 512, (g, w, h) => { o.body(g, w, h); const sh = g.createLinearGradient(0, 0, w, 0); sh.addColorStop(0, 'rgba(40,10,40,0.18)'); sh.addColorStop(0.3, 'rgba(0,0,0,0)'); sh.addColorStop(0.7, 'rgba(0,0,0,0)'); sh.addColorStop(1, 'rgba(40,10,40,0.18)'); g.fillStyle = sh; g.fillRect(0, 0, w, h); });
  c.bodyM = flat(0xffffff, { map: bt }); c.body = M(TUBE, c.bodyM, { ol: 0.05, p: [0, HIP - 0.04, 0], r: [0, Math.PI, 0], to: up });
  c.headG = new THREE.Group(); c.headG.position.set(0, HEADY, 0); up.add(c.headG);
  c.ft = ctex(1024, 512, g => drawFace3(g, 'neutral', o)); c.headM = flat(0xffffff, { map: c.ft });
  c.head = M(sph(0.58, 48, 32), c.headM, { ol: 0.055, r: [0, -Math.PI / 2, 0], to: c.headG });
  c.hatG = new THREE.Group(); c.headG.add(c.hatG); if (o.hat) o.hat(c.hatG);
  const armM = flat(o.arm ?? 0x1b1522), legM = flat(0x1b1522), hand = flat(0xfcfbf6);
  c.arms = [-1, 1].map(s => ({ s, a: M(UNIT, armM, { to: up }), b: M(UNIT, armM, { to: up }), h: M(sph(0.065, 12, 10), hand, { ol: 0.028, to: up }) }));
  c.legs = [-1, 1].map(s => ({ s, a: M(UNIT, legM, { to: c.g }), f: M(sph(0.11, 14, 10), flat(o.shoe || 0x2a2530), { ol: 0.028, s: [1, 0.5, 1.6], to: c.g }) }));
  c.mats = [c.bodyM, c.headM, hand]; c.tint = hex => c.mats.forEach(m => m.color.set(hex));
  c.face = e => { if (c.expr !== e) { c.expr = e; drawFace3(c.ft.userData.g, e, o); c.ft.needsUpdate = true; } };
  c.pose = (p = {}) => {
    const bob = p.bob || 0; up.position.y = bob; up.rotation.z = p.lean || 0; up.rotation.x = p.pitch || 0; c.headG.rotation.set(p.hx || 0, p.hy || 0, p.hz || 0);
    const hands = [p.lh || [-0.5, HIP + 0.55, 0.05], p.rh || [0.5, HIP + 0.55, 0.05]];
    c.arms.forEach((A, i) => { const sh = V(A.s * 0.3, HIP + 1.2, 0), hd = V(...hands[i]); const mid = sh.clone().lerp(hd, 0.5).add(V(A.s * 0.1, -0.1, -0.05)); seg(A.a, sh, mid, 0.03); seg(A.b, mid, hd, 0.03); A.h.position.copy(hd); });
    const feet = [p.lf || [-0.15, 0, 0], p.rf || [0.15, 0, 0]];
    c.legs.forEach((Lg, i) => { const hip = V(Lg.s * 0.13, HIP + 0.1 + bob, 0), ft = V(feet[i][0], feet[i][1] + 0.05, feet[i][2]); seg(Lg.a, ft, hip, 0.034); Lg.f.position.copy(ft).add(V(0, 0, 0.08)); });
  };
  c.walk = (ph, amp = 0.3) => ({ lf: [-0.15, Math.max(0, Math.sin(ph)) * 0.22, Math.cos(ph) * amp], rf: [0.15, Math.max(0, -Math.sin(ph)) * 0.22, -Math.cos(ph) * amp], bob: Math.abs(Math.sin(ph)) * 0.05 });
  c.HIP = HIP; c.HEADY = HEADY; c.face('neutral'); c.pose(); return c;
}
const bodyTex = (coat, trim, o = {}) => (g, w, h) => { g.fillStyle = coat; g.fillRect(0, 0, w, h); if (o.belt) { g.fillStyle = o.belt; g.fillRect(0, h * 0.5, w, h * 0.07); g.fillStyle = '#ffd34d'; g.fillRect(w * 0.47, h * 0.49, w * 0.06, h * 0.09); } if (o.ermine) { g.fillStyle = '#f6f3ec'; g.fillRect(w * 0.38, 0, w * 0.24, h); g.fillStyle = '#1b1522'; for (let i = 0; i < 7; i++) { g.beginPath(); g.ellipse(w * (0.44 + (i % 2) * 0.12), h * (0.08 + i * 0.13), 6, 10, 0, 0, 7); g.fill(); } } if (o.buttons) { g.fillStyle = trim; for (let i = 0; i < 4; i++) { g.beginPath(); g.arc(w * 0.5, h * (0.2 + i * 0.16), 9, 0, 7); g.fill(); } } if (o.apron) { g.fillStyle = trim; g.fillRect(w * 0.3, h * 0.35, w * 0.4, h * 0.6); } if (o.stripes) { g.fillStyle = trim; for (let i = 0; i < 6; i++) g.fillRect(0, h * (0.1 + i * 0.15), w, h * 0.05); } };
const crownHat = hg => { const gm = flat(0xffd34d); M(cyl(0.4, 0.4, 0.2, 20, true), flat(0xffd34d, { side: THREE.DoubleSide }), { ol: 0.04, p: [0, 0.5, -0.02], to: hg }); for (let i = 0; i < 7; i++) { const a = i / 7 * 6.283; M(new THREE.ConeGeometry(0.1, 0.24, 4), gm, { ol: 0.035, p: [Math.cos(a) * 0.38, 0.7, Math.sin(a) * 0.38 - 0.02], to: hg }); M(sph(0.045), flat([0xe2372d, 0x2f8f5b, 0x3b5bd9][i % 3]), { p: [Math.cos(a) * 0.38, 0.84, Math.sin(a) * 0.38 - 0.02], to: hg, cast: false }); } M(sph(0.52, 24, 12, 0, 6.3, 0, 0.9), flat(0xb3272d), { p: [0, 0.2, -0.02], to: hg, cast: false }); };
const capHat = (col) => hg => { const m = flat(col); M(sph(0.6, 32, 16, 0, 6.3, 0, Math.PI * 0.36), m, { ol: 0.045, p: [0, 0.1, -0.03], s: [1.06, 0.7, 1.08], to: hg }); M(cyl(0.36, 0.38, 0.06, 24), m, { ol: 0.04, p: [0, 0.3, 0.5], s: [1.1, 1, 0.6], r: [0.1, 0, 0], to: hg }); };
const tallHat = hg => { const m = flat(0x2a2530); hg.userData.top = M(cyl(0.42, 0.46, 1.1, 24), m, { ol: 0.045, p: [0, 0.95, 0], to: hg }); M(cyl(0.72, 0.72, 0.06, 32), m, { ol: 0.04, p: [0, 0.4, 0], to: hg }); M(cyl(0.465, 0.465, 0.12, 24), flat(0xb3272d), { p: [0, 0.5, 0], to: hg, cast: false }); };
const hoodHat = (col) => hg => { const m = flat(col); M(sph(0.63, 32, 16, 0, 6.3, 0, Math.PI * 0.55), m, { ol: 0.045, p: [0, 0.02, -0.08], to: hg }); };
const braidHair = hg => { const m = flat(0x3a2416); M(sph(0.6, 32, 16, 0, 6.3, 0, Math.PI * 0.42), m, { ol: 0.045, p: [0, 0.06, -0.03], to: hg }); for (const s of [-1, 1]) { M(cyl(0.09, 0.07, 0.7, 10), m, { ol: 0.035, p: [s * 0.5, -0.3, -0.1], r: [0, 0, s * 0.15], to: hg }); M(box(0.12, 0.08, 0.12), flat(0xe2553d), { ol: 0.02, p: [s * 0.55, -0.62, -0.1], to: hg }); } };

// ===== The Cook Who Got Paid in Noise — high-detail cast and sets =====
const FT = []; function ftex(w, h, d) { const t = ctex(w, h, d); t.userData.draw = d; FT.push(t); return t; }
window.afterFonts = () => FT.forEach(t => { t.userData.draw(t.userData.g, t.userData.c.width, t.userData.c.height); t.needsUpdate = true; });
Object.assign(sun.shadow.camera, { left: -12, right: 12, top: 14, bottom: -4, near: 0.5, far: 60 }); sun.shadow.camera.updateProjectionMatrix(); sun.shadow.mapSize.set(4096, 4096); sun.shadow.bias = -0.0008;
const rnd = (seed => () => (seed = (seed * 16807) % 2147483647) / 2147483647)(77);
const glowTex = ctex(128, 128, g => { const r = g.createRadialGradient(64, 64, 0, 64, 64, 64); r.addColorStop(0, 'rgba(255,240,190,1)'); r.addColorStop(0.35, 'rgba(255,190,90,0.45)'); r.addColorStop(1, 'rgba(255,160,60,0)'); g.fillStyle = r; g.fillRect(0, 0, 128, 128); });
function glow(parent, x, y, z, s = 1.2, op = 0.9) { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: op })); sp.position.set(x, y, z); sp.scale.set(s, s, 1); parent.add(sp); return sp; }
const steamTex = ctex(128, 128, g => { const r = g.createRadialGradient(64, 64, 0, 64, 64, 64); r.addColorStop(0, 'rgba(255,255,255,0.75)'); r.addColorStop(0.6, 'rgba(255,255,255,0.25)'); r.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = r; g.fillRect(0, 0, 128, 128); });
function steamCloud(parent, n) { const arr = []; for (let i = 0; i < n; i++) { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: steamTex, depthWrite: false, transparent: true, opacity: 0.6 })); parent.add(sp); arr.push(sp); } return arr; }
function steamAt(arr, t, x, y, z, rise = 2.4, spread = 0.5, size = 0.9) { arr.forEach((s, i) => { const p = ((t * 0.32 + i / arr.length) % 1); s.position.set(x + Math.sin(i * 2.3 + t * 1.3 + p * 4) * spread * (0.4 + p), y + p * rise, z + Math.cos(i * 1.7 + t) * spread * 0.4); const sc = size * (0.4 + p * 1.4); s.scale.set(sc, sc, 1); s.material.opacity = 0.7 * Math.sin(p * Math.PI); }); }

// ---------- textures ----------
const T2 = {
  wood: rep_(ctex(512, 512, (g, w, h) => { g.fillStyle = '#8a5a34'; g.fillRect(0, 0, w, h); for (let i = 0; i < 8; i++) { g.fillStyle = `rgba(${rnd() < 0.5 ? '50,25,10' : '255,215,160'},${0.05 + rnd() * 0.09})`; g.fillRect(0, i * 64, w, 64); g.fillStyle = '#3d2414'; g.fillRect(0, i * 64, w, 4); g.strokeStyle = 'rgba(60,30,15,0.35)'; g.lineWidth = 2; for (let k = 0; k < 6; k++) { const y = i * 64 + 8 + rnd() * 48; g.beginPath(); g.moveTo(0, y); g.bezierCurveTo(w * 0.3, y + (rnd() - 0.5) * 16, w * 0.65, y + (rnd() - 0.5) * 16, w, y); g.stroke(); } g.fillStyle = '#3d2414'; g.beginPath(); g.ellipse(rnd() * w, i * 64 + 32, 7, 4, 0, 0, 7); g.fill(); } }), 3, 3),
  panel: rep_(ctex(512, 512, (g, w, h) => { g.fillStyle = '#6b3f22'; g.fillRect(0, 0, w, h); for (const [x, y] of [[20, 20], [266, 20], [20, 266], [266, 266]]) { g.fillStyle = '#7d4c2a'; g.fillRect(x, y, 226, 226); g.strokeStyle = '#3d2414'; g.lineWidth = 8; g.strokeRect(x, y, 226, 226); g.strokeStyle = 'rgba(255,220,170,0.18)'; g.lineWidth = 4; g.strokeRect(x + 14, y + 14, 198, 198); } }), 6, 2),
  tiles: rep_(ctex(256, 256, (g, w, h) => { for (let y = 0; y < 4; y++) for (let x = 0; x < 4; x++) { g.fillStyle = (x + y) % 2 ? '#e8dcc0' : '#5a3a2a'; g.fillRect(x * 64, y * 64, 64, 64); g.fillStyle = 'rgba(0,0,0,0.06)'; g.fillRect(x * 64, y * 64 + 58, 64, 6); } }), 10, 10),
  stone: rep_(ctex(256, 256, (g, w, h) => { g.fillStyle = '#6a6070'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 42) for (let x = (y / 42 % 2) * 40 - 80; x < w; x += 80) { g.fillStyle = `hsl(${250 + rnd() * 30},${6 + rnd() * 8}%,${44 + rnd() * 14}%)`; g.fillRect(x + 3, y + 3, 74, 36); } }), 3, 3),
  brickW: rep_(ctex(256, 256, (g, w, h) => { g.fillStyle = '#5a3a30'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 32) for (let x = (y / 32 % 2) * 32 - 64; x < w; x += 64) { g.fillStyle = `hsl(${10 + rnd() * 12},${36 + rnd() * 16}%,${32 + rnd() * 12}%)`; g.fillRect(x + 3, y + 3, 58, 26); } }), 4, 3),
  cobble: rep_(ctex(256, 256, (g, w, h) => { g.fillStyle = '#3d3a48'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 32) for (let x = (y / 32 % 2) * 20 - 40; x < w; x += 40) { g.fillStyle = `hsl(${240 + rnd() * 20},${8 + rnd() * 6}%,${36 + rnd() * 14}%)`; g.beginPath(); g.ellipse(x + 20, y + 16, 17, 13, 0, 0, 7); g.fill(); g.strokeStyle = 'rgba(0,0,0,0.3)'; g.lineWidth = 2; g.stroke(); } }), 10, 10),
  plaster: ctex(512, 512, (g, w, h) => { g.fillStyle = '#e9d6ad'; g.fillRect(0, 0, w, h); for (let i = 0; i < 160; i++) { g.fillStyle = `rgba(110,80,40,${0.03 + rnd() * 0.05})`; g.beginPath(); g.ellipse(rnd() * w, rnd() * h, 10 + rnd() * 40, 6 + rnd() * 20, rnd() * 3, 0, 7); g.fill(); } g.fillStyle = '#3d2718'; for (const x of [0, 248, 494]) g.fillRect(x, 0, 18, h); g.fillRect(0, 0, w, 18); g.fillRect(0, 250, w, 16); g.fillRect(0, 494, w, 18); }),
};

// ---------- cast ----------
const chefHat = hg => { const m = flat(0xfbfaf4); M(cyl(0.5, 0.42, 0.34, 28), m, { ol: 0.045, p: [0, 0.48, 0], to: hg }); for (let i = 0; i < 7; i++) { const a = i / 7 * 6.283; M(sph(0.3, 16, 12), m, { ol: 0.04, p: [Math.cos(a) * 0.3, 0.98, Math.sin(a) * 0.3], to: hg }); } M(sph(0.36, 16, 12), m, { ol: 0.04, p: [0, 1.1, 0], to: hg }); };
const wigHat = hg => { const m = flat(0xf3efe6); M(sph(0.6, 32, 16, 0, 6.3, 0, Math.PI * 0.5), m, { ol: 0.045, p: [0, 0.06, -0.04], to: hg }); for (const s of [-1, 1]) for (let r = 0; r < 4; r++) M(new THREE.TorusGeometry(0.13, 0.065, 8, 16), m, { ol: 0.03, p: [s * 0.6, 0.1 - r * 0.22, -0.05], r: [0, Math.PI / 2, 0], to: hg }); for (let i = 0; i < 5; i++) M(new THREE.TorusGeometry(0.11, 0.06, 8, 16), m, { ol: 0.03, p: [-0.4 + i * 0.2, 0.55, -0.05], r: [Math.PI / 2, 0, 0], to: hg }); };
const raggedHat = hg => { const m = flat(0x5a6a3a); M(sph(0.61, 32, 16, 0, 6.3, 0, Math.PI * 0.4), m, { ol: 0.045, p: [0, 0.07, -0.03], to: hg }); M(box(0.2, 0.18, 0.05), flat(0xb79a70), { ol: 0.02, p: [0.25, 0.42, 0.42], r: [-0.6, 0, 0.3], to: hg }); M(new THREE.TorusGeometry(0.56, 0.07, 8, 28), flat(0x4a5a30), { ol: 0.03, p: [0, 0.1, -0.03], r: [Math.PI / 2 - 0.12, 0, 0], to: hg }); };
const cook = makeChar3({ stache: true, shoe: 0x3a2416, body: (g, w, h) => { g.fillStyle = '#d64a3a'; g.fillRect(0, 0, w, h); g.fillStyle = '#fbfaf4'; g.fillRect(w * 0.2, h * 0.22, w * 0.6, h * 0.78); g.fillStyle = '#fbfaf4'; g.fillRect(w * 0.43, 0, w * 0.14, h * 0.22); g.fillStyle = 'rgba(214,74,58,0.35)'; for (const [x, y] of [[0.35, 0.5], [0.6, 0.62], [0.45, 0.78]]) { g.beginPath(); g.arc(w * x, h * y, 14, 0, 7); g.fill(); } g.fillStyle = '#ffd34d'; for (let i = 0; i < 3; i++) { g.beginPath(); g.arc(w * 0.12, h * (0.25 + i * 0.12), 9, 0, 7); g.fill(); g.beginPath(); g.arc(w * 0.88, h * (0.25 + i * 0.12), 9, 0, 7); g.fill(); } }, hat: chefHat });
const pip = makeChar3({ freckles: true, shoe: 0x4a3a2a, body: (g, w, h) => { g.fillStyle = '#7a6a52'; g.fillRect(0, 0, w, h); g.fillStyle = '#5a4a3a'; for (let i = 0; i < 7; i++) g.fillRect(0, h * (0.1 + i * 0.13), w, h * 0.025); for (const [x, y, c] of [[0.3, 0.35, '#b3472d'], [0.65, 0.6, '#3f7f8a'], [0.4, 0.8, '#d9a23a']]) { g.fillStyle = c; g.fillRect(w * x, h * y, w * 0.14, h * 0.12); g.strokeStyle = '#1b1522'; g.lineWidth = 3; g.setLineDash([6, 5]); g.strokeRect(w * x, h * y, w * 0.14, h * 0.12); g.setLineDash([]); } g.fillStyle = '#3a2f22'; g.beginPath(); g.moveTo(0, h); for (let x = 0; x <= w; x += 32) g.lineTo(x, h - (x / 32 % 2) * 26); g.lineTo(w, h); g.fill(); }, hat: raggedHat });
const judge = makeChar3({ wrinkles: true, shoe: 0x1b1522, body: (g, w, h) => { g.fillStyle = '#1c1a26'; g.fillRect(0, 0, w, h); g.fillStyle = '#fbfaf4'; g.beginPath(); g.moveTo(w * 0.42, 0); g.lineTo(w * 0.47, h * 0.16); g.lineTo(w * 0.53, h * 0.16); g.lineTo(w * 0.58, 0); g.fill(); g.fillStyle = '#b3272d'; g.fillRect(0, h * 0.05, w * 0.18, h * 0.95); g.fillRect(w * 0.82, h * 0.05, w * 0.18, h * 0.95); g.strokeStyle = 'rgba(255,255,255,0.12)'; g.lineWidth = 4; for (let x = 0.25; x < 0.8; x += 0.1) { g.beginPath(); g.moveTo(w * x, h * 0.2); g.lineTo(w * x, h); g.stroke(); } }, hat: wigHat });
const townsfolk = [['#c98a2a', 0xd9b36a], ['#3f8f8a', 0x57b0aa], ['#b0567a', 0xd9869f], ['#5a6ab0', 0x7f8fd0], ['#7a4a2c', 0xb07a50], ['#2f6b4f', 0x4f9a70], ['#d9a23a', 0xe8c060], ['#8a3a5a', 0xc0607a]].map(([c, h], i) => makeChar3({ freckles: i % 3 === 0, stache: i % 4 === 1, beard: i === 5 ? '#8a8f99' : null, wrinkles: i === 5, shoe: 0x3a2416, body: bodyTex(c, '#1b1522', { belt: i % 2 ? '#3a2416' : null, buttons: i % 3 === 1, apron: i % 4 === 2 ? '#e9d6ad' : null }), hat: i % 3 === 2 ? capHat(h) : hoodHat(h) }));
const CAST = [cook, pip, judge, ...townsfolk]; CAST.forEach(c => root.add(c.g));

// ---------- props ----------
const bread = new THREE.Group(); root.add(bread); M(sph(0.2, 16, 12), toon(0xc98a3a), { ol: 0.025, s: [1.6, 0.7, 0.8], to: bread }); for (const x of [-0.12, 0, 0.12]) M(box(0.025, 0.02, 0.18), flat(0x7a4a1c), { p: [x, 0.13, 0], r: [0, 0.5, 0], to: bread, cast: false });
const coin = new THREE.Group(); root.add(coin); M(cyl(0.16, 0.16, 0.035, 20), toon(0xffd34d), { ol: 0.02, r: [Math.PI / 2, 0, 0.25], to: coin }); M(box(0.06, 0.02, 0.04), toon(0xd9a53a), { p: [0.1, 0.1, 0], r: [0, 0, 0.7], to: coin, cast: false });
const gavel = new THREE.Group(); root.add(gavel); M(cyl(0.11, 0.11, 0.4, 16), toon(0x6b3f22), { ol: 0.025, r: [0, 0, Math.PI / 2], to: gavel }); M(cyl(0.035, 0.035, 0.6, 10), toon(0x8a5a34), { ol: 0.02, p: [0, -0.3, 0], to: gavel });
const ladle = new THREE.Group(); root.add(ladle); M(cyl(0.03, 0.03, 1.3, 8), toon(0x8a5a34), { ol: 0.02, p: [0, 0.65, 0], to: ladle }); M(sph(0.15, 14, 10, 0, 6.3, Math.PI / 2, Math.PI / 2), toon(0xb9bfca, { side: THREE.DoubleSide }), { ol: 0.02, to: ladle });

// ---------- COURTROOM ----------
const court = new THREE.Group(); root.add(court); const BENCH = { x: 0, z: -4.2 }; const shafts = [];
{
  M(box(16, 0.2, 16), toon(0xffffff, { map: T2.tiles }), { p: [0, -0.1, 0], recv: true, to: court, cast: false });
  M(new THREE.PlaneGeometry(16, 9), toon(0xffffff, { map: T2.panel }), { p: [0, 4.5, -6.5], recv: true, to: court, cast: false });
  for (const s of [-1, 1]) M(new THREE.PlaneGeometry(16, 9), toon(0xffffff, { map: T2.panel }), { p: [s * 7.5, 4.5, 0], r: [0, -s * Math.PI / 2, 0], recv: true, to: court, cast: false });
  M(box(16, 0.4, 0.3), toon(0x3d2414), { p: [0, 7.5, -6.4], to: court, cast: false }); M(box(16, 0.25, 0.25), toon(0x3d2414), { p: [0, 1.2, -6.4], to: court, cast: false });
  // tall arched windows with light shafts
  for (const x of [-5, 5]) { M(box(1.8, 3.6, 0.15), toon(0x3d2414), { ol: 0.03, p: [x, 4.6, -6.42], to: court }); M(box(1.5, 3.3, 0.18), flat(0xffe2a8), { p: [x, 4.6, -6.4], to: court, cast: false }); M(cyl(0.75, 0.75, 0.18, 24, false, 0, Math.PI), flat(0xffe2a8), { p: [x, 6.25, -6.4], r: [Math.PI / 2, 0, 0], to: court, cast: false }); M(box(0.06, 3.3, 0.2), toon(0x3d2414), { p: [x, 4.6, -6.38], to: court, cast: false }); M(box(1.5, 0.06, 0.2), toon(0x3d2414), { p: [x, 4.9, -6.38], to: court, cast: false });
    const sh = M(new THREE.PlaneGeometry(2.0, 9), new THREE.MeshBasicMaterial({ color: 0xffe9b8, transparent: true, opacity: 0.12, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }), { p: [x * 0.8, 2.6, -3.0], r: [-0.55, x > 0 ? -0.25 : 0.25, 0], to: court, cast: false }); shafts.push(sh); }
  // crest + banners
  const crest = ftex(256, 300, g => { g.fillStyle = '#b3272d'; g.beginPath(); g.moveTo(20, 10); g.lineTo(236, 10); g.lineTo(236, 170); g.quadraticCurveTo(236, 270, 128, 295); g.quadraticCurveTo(20, 270, 20, 170); g.closePath(); g.fill(); g.strokeStyle = '#ffd34d'; g.lineWidth = 12; g.stroke(); g.fillStyle = '#ffd34d'; g.font = '130px Pop'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('⚖', 128, 140); });
  M(new THREE.PlaneGeometry(1.4, 1.65), flat(0xffffff, { map: crest, transparent: true }), { p: [0, 6.2, -6.38], to: court, cast: false });
  for (const s of [-1, 1]) { M(box(0.9, 2.6, 0.04), toon(0x6a2f6b), { ol: 0.02, p: [s * 2.0, 5.7, -6.36], to: court, cast: false }); M(box(0.9, 0.12, 0.06), toon(0xffd34d), { p: [s * 2.0, 4.42, -6.35], to: court, cast: false }); }
  // judge's bench: raised, panelled front, steps
  const wood = toon(0xffffff, { map: T2.wood });
  M(box(5.2, 2.0, 1.6), toon(0xffffff, { map: T2.panel }), { ol: 0.05, p: [BENCH.x, 1.0, BENCH.z], to: court }); M(box(5.6, 0.18, 2.0), wood, { ol: 0.04, p: [BENCH.x, 2.08, BENCH.z], to: court });
  M(box(5.6, 0.9, 1.2), wood, { ol: 0.04, p: [BENCH.x, 0.45, BENCH.z - 1.4], to: court });
  M(box(1.2, 2.2, 0.15), toon(0x6a2f22), { ol: 0.03, p: [BENCH.x, 3.0, BENCH.z - 1.9], to: court });
  M(cyl(0.18, 0.18, 0.1, 16), toon(0x3d2414), { ol: 0.02, p: [BENCH.x + 1.5, 2.22, BENCH.z + 0.3], to: court }); // gavel block
  for (let i = 0; i < 6; i++) M(box(0.12 + (i % 3) * 0.03, 0.55, 0.4), toon([0x8a2a2a, 0x2a4a8a, 0x3a6a3a, 0x7a5a2a][i % 4]), { ol: 0.015, p: [BENCH.x - 2.3 + i * 0.16, 2.45, BENCH.z - 0.4], to: court });
  // candles on the bench with glows
  for (const x of [-2.2, 2.2]) { M(cyl(0.12, 0.15, 0.08, 12), toon(0xd9a53a), { ol: 0.015, p: [BENCH.x + x, 2.21, BENCH.z + 0.5], to: court }); M(cyl(0.05, 0.05, 0.4, 10), toon(0xfbf6e4), { ol: 0.015, p: [BENCH.x + x, 2.45, BENCH.z + 0.5], to: court }); M(new THREE.ConeGeometry(0.04, 0.12, 8), flat(0xffc040), { p: [BENCH.x + x, 2.72, BENCH.z + 0.5], to: court, cast: false }); glow(court, BENCH.x + x, 2.75, BENCH.z + 0.5, 0.9); const pl = new THREE.PointLight(0xffb060, 3, 4, 1.6); pl.position.set(BENCH.x + x, 2.8, BENCH.z + 0.6); court.add(pl); }
  // wall sconces
  for (const x of [-6.6, 6.6]) for (const z of [-3, 2]) { M(box(0.2, 0.5, 0.2), toon(0xd9a53a), { ol: 0.02, p: [x, 4.2, z], to: court }); glow(court, x * 0.98, 4.6, z, 1.1); const pl = new THREE.PointLight(0xffb060, 2.5, 5, 1.6); pl.position.set(x * 0.95, 4.6, z); court.add(pl); }
  // railing between bench area and gallery
  M(box(12, 0.12, 0.16), wood, { ol: 0.025, p: [0, 1.0, 0.6], to: court }); for (let x = -6; x <= 6; x += 0.5) M(cyl(0.05, 0.06, 1.0, 8), toon(0x8a5a34), { ol: 0.015, p: [x, 0.5, 0.6], to: court });
  // gallery benches (rows behind the railing)
  for (let r = 0; r < 3; r++) for (const s of [-1, 1]) { const z = 2.0 + r * 1.4, x = s * 3.4; M(box(5.0, 0.12, 0.6), wood, { ol: 0.025, p: [x, 0.65, z], to: court }); M(box(5.0, 0.7, 0.1), wood, { ol: 0.025, p: [x, 1.05, z + 0.32], to: court }); for (const dx of [-2.3, 2.3]) M(box(0.1, 0.65, 0.5), wood, { p: [x + dx, 0.33, z], to: court }); }
  // dust motes
  court.userData.dust = []; for (let i = 0; i < 70; i++) { const d = M(sph(0.018, 6, 4), flat(0xfff2c8), { cast: false }); court.add(d); court.userData.dust.push(d); }
}
function courtLook(t) { court.visible = true; bg(0x3a2214); light(0.55, 1.6, [-5, 9, -2], 0xffe2b8, 0x4a3020); court.userData.dust.forEach((d, i) => { const a = i * 2.399; d.position.set(-4 + ((i * 37) % 80) / 10 + 0.2 * Math.sin(t * 0.5 + i), 1.0 + ((i * 53) % 60) / 10 + 0.15 * Math.sin(t * 0.7 + a), -3 + ((i * 29) % 50) / 10); }); shafts.forEach((s, i) => s.material.opacity = 0.1 + 0.025 * Math.sin(t * 1.2 + i)); LOOK.grade = ['#ffb060', 0.18]; LOOK.bloom = 0.3; }

// ---------- KITCHEN ----------
const kitchen = new THREE.Group(); root.add(kitchen); const POT = { x: 0, y: 0, z: -1.2 }; const flames = [];
const kSteam = steamCloud(kitchen, 22);
{
  M(box(12, 0.2, 10), toon(0xffffff, { map: T2.stone }), { p: [0, -0.1, 0], recv: true, to: kitchen, cast: false });
  M(new THREE.PlaneGeometry(12, 7), toon(0xffffff, { map: T2.brickW }), { p: [0, 3.5, -3.4], recv: true, to: kitchen, cast: false });
  for (const s of [-1, 1]) M(new THREE.PlaneGeometry(10, 7), toon(0xffffff, { map: T2.plaster }), { p: [s * 5.5, 3.5, 0], r: [0, -s * Math.PI / 2, 0], recv: true, to: kitchen, cast: false });
  for (let x = -5; x <= 5; x += 2.5) M(box(0.3, 0.3, 10), toon(0x3d2414), { ol: 0.02, p: [x, 6.5, 0], to: kitchen, cast: false });
  // hearth with arch, fire, giant cauldron on a hook
  const hearth = new THREE.Group(); hearth.position.set(POT.x, 0, -2.6); kitchen.add(hearth);
  M(box(4.2, 3.6, 1.4), toon(0xffffff, { map: T2.stone }), { ol: 0.05, p: [0, 1.8, -0.2], to: hearth }); M(box(2.8, 2.2, 1.5), flat(0x120c10), { p: [0, 1.1, 0], to: hearth, cast: false }); M(cyl(1.4, 1.4, 1.5, 24, false, 0, Math.PI), flat(0x120c10), { p: [0, 2.2, 0], r: [Math.PI / 2, 0, 0], s: [1, 1, 0.55], to: hearth, cast: false });
  M(box(4.6, 0.3, 1.7), toon(0x6a4a30), { ol: 0.035, p: [0, 3.65, -0.1], to: hearth }); M(box(2.4, 3.4, 1.2), toon(0xffffff, { map: T2.stone }), { ol: 0.04, p: [0, 5.3, -0.3], to: hearth });
  for (let i = 0; i < 4; i++) M(cyl(0.12, 0.12, 1.2, 10), toon(0x5a3a22), { ol: 0.02, p: [-0.5 + i * 0.33, 0.12, 0.25], r: [Math.PI / 2, 0, 0.3 * (i - 1.5)], to: hearth });
  for (let i = 0; i < 7; i++) { const f = M(new THREE.ConeGeometry(0.22 - (i % 3) * 0.04, 0.8, 8), flat(i % 2 ? 0xffb030 : 0xff6a20), { p: [-0.6 + i * 0.2, 0.55, 0.25], to: hearth, cast: false }); flames.push(f); }
  glow(hearth, 0, 0.8, 0.5, 3.2, 0.8); kitchen.userData.fire = new THREE.PointLight(0xff8a30, 18, 9, 1.4); kitchen.userData.fire.position.set(0, 1.0, -1.6); kitchen.add(kitchen.userData.fire);
  const pot = new THREE.Group(); pot.position.set(POT.x, 1.25, POT.z); kitchen.add(pot); kitchen.userData.pot = pot;
  const SG = (r) => new THREE.SphereGeometry(r, 32, 20, 0, Math.PI * 2, Math.PI * 0.32, Math.PI * 0.68); M(SG(1.0), toon(0x3a3542), { to: pot }); M(SG(0.97), flat(0x2a2028, { side: THREE.BackSide }), { to: pot, cast: false }); M(SG(1.05), flat(0x1b1522, { side: THREE.BackSide }), { to: pot, cast: false }); M(new THREE.TorusGeometry(0.86, 0.08, 10, 36), toon(0x3a3542), { ol: 0.03, p: [0, 0.48, 0], r: [Math.PI / 2, 0, 0], to: pot });
  kitchen.userData.soup = M(new THREE.CircleGeometry(0.84, 36), flat(0xe8742a), { p: [0, 0.5, 0], r: [-Math.PI / 2, 0, 0], to: pot, cast: false });
  kitchen.userData.bubbles = []; for (let i = 0; i < 9; i++) { const b = M(sph(0.06, 10, 8), flat(0xffa05a), { ol: 0.012, cast: false }); pot.add(b); kitchen.userData.bubbles.push(b); }
  for (const [x, z, r] of [[0.3, 0.2, 0.09], [-0.25, -0.3, 0.07], [0.1, -0.15, 0.08]]) M(sph(r, 10, 8), flat(0xd63b2f), { ol: 0.015, p: [x, 0.53, z], to: pot, cast: false });
  M(new THREE.TorusGeometry(0.9, 0.035, 6, 24, Math.PI), flat(0x1b1522), { p: [0, 0.5, 0], r: [0, 0, 0], to: pot, cast: false }); M(cyl(0.03, 0.03, 1.4, 6), flat(0x1b1522), { p: [0, 1.85, 0], to: pot, cast: false });
  // hanging copper pans + garlic + herbs from a rail
  M(cyl(0.04, 0.04, 6, 8), toon(0x3d2414), { p: [0, 4.6, -1.6], r: [0, 0, Math.PI / 2], to: kitchen });
  for (let i = 0; i < 6; i++) { const x = -2.6 + i * 1.04, r = 0.28 + (i % 3) * 0.07; if (x > -1 && x < 1) continue; const g = new THREE.Group(); g.position.set(x, 4.55, -1.6); kitchen.add(g); M(cyl(0.012, 0.012, 0.3, 4), flat(INK), { p: [0, -0.15, 0], to: g, cast: false }); M(cyl(r, r * 0.8, 0.14, 24), toon(0xd9773a), { ol: 0.025, p: [0, -0.62 - r, 0], r: [Math.PI / 2, 0, 0], to: g }); M(box(0.07, 0.4, 0.04), toon(0xb05a2a), { ol: 0.015, p: [0, -0.4, 0], to: g }); }
  for (const x of [-0.6, 0.6]) for (let i = 0; i < 5; i++) M(sph(0.1, 10, 8), toon(0xf3efe6), { ol: 0.015, p: [x + (i % 2) * 0.08, 4.4 - i * 0.16, -1.6], to: kitchen });
  // shelves with jars, sacks, tomatoes basket, bread, table with knife and onions
  const wood = toon(0xffffff, { map: T2.wood });
  for (const y of [3.4, 4.4]) { M(box(2.2, 0.1, 0.5), wood, { ol: 0.02, p: [-3.8, y, -3.1], to: kitchen }); for (let i = 0; i < 5; i++) { const h = 0.3 + (i % 3) * 0.1; M(cyl(0.12, 0.12, h, 12), toon([0x8fd0c0, 0xe8c060, 0xc0607a, 0x8fa0e0, 0xd9a23a][(i + y * 10) % 5]), { ol: 0.015, p: [-4.6 + i * 0.4, y + 0.05 + h / 2, -3.1], to: kitchen }); M(cyl(0.13, 0.13, 0.05, 12), toon(0x8a5a34), { p: [-4.6 + i * 0.4, y + 0.08 + h, -3.1], to: kitchen, cast: false }); } }
  for (const [x, z] of [[-4.2, -1.6], [-4.6, -0.9]]) { M(sph(0.42, 14, 10), toon(0xc9b08a), { ol: 0.03, p: [x, 0.38, z], s: [1, 1.2, 1], to: kitchen }); M(cyl(0.18, 0.24, 0.2, 10), toon(0xc9b08a), { ol: 0.02, p: [x, 0.88, z], to: kitchen }); }
  const table = new THREE.Group(); table.position.set(3.4, 0, -0.8); kitchen.add(table); M(box(2.6, 0.16, 1.3), wood, { ol: 0.035, p: [0, 1.25, 0], to: table, recv: true }); for (const [dx, dz] of [[-1.15, -0.5], [1.15, -0.5], [-1.15, 0.5], [1.15, 0.5]]) M(box(0.14, 1.25, 0.14), wood, { ol: 0.02, p: [dx, 0.62, dz], to: table });
  M(cyl(0.45, 0.35, 0.3, 16, true), toon(0xb07a50, { side: THREE.DoubleSide }), { ol: 0.025, p: [-0.6, 1.48, 0], to: table }); for (let i = 0; i < 9; i++) M(sph(0.12, 12, 10), toon(0xd63b2f), { ol: 0.015, p: [-0.6 + Math.cos(i * 2.3) * 0.22, 1.58 + (i % 3) * 0.06, Math.sin(i * 2.3) * 0.22], to: table });
  M(box(0.7, 0.06, 0.4), toon(0xb07a50), { ol: 0.02, p: [0.5, 1.36, 0.1], to: table }); M(box(0.5, 0.02, 0.08), toon(0xc9ced6), { ol: 0.012, p: [0.55, 1.4, 0.1], r: [0, 0.3, 0], to: table }); for (const [x, z] of [[0.95, -0.3], [0.8, -0.1]]) M(sph(0.1, 10, 8), toon(0xe8d8a0), { ol: 0.012, p: [x, 1.42, z], to: table });
  for (const [x, z, r] of [[0.9, 0.4, 0.2], [0.2, -0.35, 0.18]]) { M(sph(r, 14, 10), toon(0xc98a3a), { ol: 0.02, p: [x, 1.38 + r * 0.3, z], s: [1.6, 0.7, 0.8], to: table }); }
  // window with night outside
  M(box(1.6, 1.6, 0.12), toon(0x3d2414), { ol: 0.03, p: [5.44, 3.4, -0.5], r: [0, -Math.PI / 2, 0], to: kitchen }); M(box(1.35, 1.35, 0.14), flat(0x1c2550), { p: [5.43, 3.4, -0.5], r: [0, -Math.PI / 2, 0], to: kitchen, cast: false });
}
function kitchenLook(t) { kitchen.visible = true; bg(0x1a1014); light(0.4, 0.6, [3, 8, 6], 0xffc890, 0x3a2420); const f = kitchen.userData.fire; f.intensity = 16 + 4 * Math.sin(t * 13) + 3 * Math.sin(t * 29); flames.forEach((fl, i) => { fl.scale.set(1, 0.8 + 0.35 * Math.abs(Math.sin(t * (9 + i) + i)), 1); fl.rotation.z = 0.15 * Math.sin(t * 7 + i); });
  kitchen.userData.bubbles.forEach((b, i) => { const p = ((t * 0.9 + i * 0.137) % 1); b.position.set(Math.cos(i * 2.4) * 0.5 * ((i % 3) / 3 + 0.3), 0.52, Math.sin(i * 2.4) * 0.5 * ((i % 3) / 3 + 0.3)); b.scale.setScalar(p < 0.85 ? 0.4 + p : Math.max(0.01, (1 - p) * 8)); });
  steamAt(kSteam, t, POT.x, POT.y + 1.8, POT.z, 3.0, 0.6, 1.1); LOOK.grade = ['#ff9a4a', 0.22]; LOOK.bloom = 0.32; }

// ---------- STREET outside the cook's window, night ----------
const street = new THREE.Group(); root.add(street); const WIN = { x: 0, y: 2.2, z: -1.9 }; const sSteam = steamCloud(street, 16); const lanternGlows = [];
{
  M(box(30, 0.2, 30), toon(0xffffff, { map: T2.cobble }), { p: [0, -0.1, 3], recv: true, to: street, cast: false });
  // the inn facade: plaster and timber upper floor, brick ground floor, bay window, door, sign
  const inn = new THREE.Group(); inn.position.set(0, 0, -2.4); street.add(inn);
  M(box(9, 3.4, 1), toon(0xffffff, { map: T2.brickW }), { ol: 0.04, p: [0, 1.7, 0], to: inn }); const up = T2.plaster.clone(); up.needsUpdate = true; up.wrapS = up.wrapT = THREE.RepeatWrapping; up.repeat.set(2, 1);
  M(box(9.6, 3.2, 1.3), toon(0xffffff, { map: up }), { ol: 0.045, p: [0, 5.0, 0.15], to: inn }); const tri = new THREE.Shape(); tri.moveTo(-5.2, 0); tri.lineTo(5.2, 0); tri.lineTo(0, 3.0); tri.closePath(); M(new THREE.ExtrudeGeometry(tri, { depth: 1.6, bevelEnabled: false }), toon(0x8a3b2c), { ol: 0.045, p: [0, 6.6, -0.65], to: inn });
  M(box(0.7, 2.0, 0.7), toon(0x6b4636), { ol: 0.03, p: [3, 9.0, 0], to: inn }); street.userData.chimney = steamCloud(inn, 10);
  // big glowing kitchen window
  M(box(2.6, 1.9, 0.3), toon(0x3d2414), { ol: 0.035, p: [WIN.x, WIN.y, 0.5], to: inn }); M(box(2.3, 1.6, 0.32), flat(0xffc070), { p: [WIN.x, WIN.y, 0.5], to: inn, cast: false }); M(box(0.07, 1.6, 0.35), toon(0x3d2414), { p: [WIN.x, WIN.y, 0.52], to: inn, cast: false }); M(box(2.3, 0.07, 0.35), toon(0x3d2414), { p: [WIN.x, WIN.y, 0.52], to: inn, cast: false });
  M(box(2.9, 0.16, 0.6), toon(0x6a4a30), { ol: 0.03, p: [WIN.x, WIN.y - 1.0, 0.7], to: inn }); for (const s of [-1, 1]) M(box(0.5, 1.9, 0.05), toon(0x2f6b4f), { ol: 0.02, p: [WIN.x + s * 1.6, WIN.y, 0.68], r: [0, s * 0.35, 0], to: inn });
  M(box(2.5, 0.6, 0.5), toon(0x6a4a30), { ol: 0.025, p: [WIN.x, WIN.y - 1.38, 0.86], to: inn }); for (let i = 0; i < 5; i++) M(sph(0.16, 10, 8), toon([0xe2553d, 0xf2c230, 0xd9869f][i % 3]), { ol: 0.015, p: [WIN.x - 0.9 + i * 0.45, WIN.y - 0.98, 0.86], to: inn });
  glow(inn, WIN.x, WIN.y, 1.0, 4.5, 0.55); street.userData.winLight = new THREE.PointLight(0xffa850, 14, 8, 1.4); street.userData.winLight.position.set(WIN.x, WIN.y, 1.4); inn.add(street.userData.winLight);
  // door + steps
  M(box(1.4, 2.6, 0.2), toon(0x5a3a22), { ol: 0.03, p: [3.0, 1.3, 0.55], to: inn }); M(sph(0.07), toon(0xd9a53a), { p: [3.5, 1.3, 0.68], to: inn }); M(box(2.0, 0.2, 0.8), toon(0xffffff, { map: T2.stone }), { ol: 0.025, p: [3.0, 0.1, 0.9], to: inn });
  // upper windows
  for (const x of [-2.8, 0, 2.8]) { M(box(1.1, 1.3, 0.2), toon(0x3d2718), { ol: 0.03, p: [x, 5.0, 0.85], to: inn }); M(box(0.9, 1.1, 0.22), flat(x === 0 ? 0xffd27a : 0x2a3552), { p: [x, 5.0, 0.86], to: inn, cast: false }); }
  // hanging sign
  const sg = new THREE.Group(); sg.position.set(-3.2, 3.9, 1.5); inn.add(sg); street.userData.sign = sg; M(box(0.12, 0.12, 1.4), toon(0x3d2414), { ol: 0.02, p: [0, 0.25, -0.6], to: inn.children[0].parent }); M(box(0.12, 0.12, 1.4), toon(0x3d2414), { ol: 0.02, p: [-3.2, 4.15, 0.9], to: inn });
  const st = ftex(512, 300, g => { g.fillStyle = '#2f4a3a'; g.beginPath(); g.roundRect(10, 10, 492, 280, 40); g.fill(); g.strokeStyle = '#ffd34d'; g.lineWidth = 12; g.stroke(); g.fillStyle = '#ffd34d'; g.font = '60px Pop'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText("BARTHOLOMEW'S", 256, 100); g.fillStyle = '#f3efe6'; g.font = '84px Pop'; g.fillText('SOUP', 256, 200); });
  for (const s of [-0.5, 0.5]) M(cyl(0.012, 0.012, 0.4, 4), flat(INK), { p: [s, -0.2, 0], to: sg, cast: false }); M(box(1.6, 0.95, 0.07), toon(0xffffff, { map: st }), { ol: 0.025, p: [0, -0.85, 0], to: sg });
  // street dressing: lanterns, barrels, crates, a cart wheel, neighbouring houses
  for (const [x, z] of [[-4.6, 1.6], [4.6, 2.4]]) { M(cyl(0.07, 0.09, 3.2, 10), flat(INK), { p: [x, 1.6, z], to: street }); M(box(0.45, 0.55, 0.45), flat(0xffd27a), { ol: 0.03, p: [x, 3.45, z], to: street, cast: false }); M(new THREE.ConeGeometry(0.4, 0.3, 4), toon(0x2a2530), { ol: 0.02, p: [x, 3.85, z], r: [0, Math.PI / 4, 0], to: street }); lanternGlows.push(glow(street, x, 3.45, z, 2.2, 0.7)); const pl = new THREE.PointLight(0xffc070, 6, 7, 1.6); pl.position.set(x, 3.4, z); street.add(pl); }
  for (const [x, z] of [[-3.4, -1.3], [-2.8, -1.0]]) { M(cyl(0.42, 0.38, 1.0, 16), toon(0x8a5a34), { ol: 0.03, p: [x, 0.5, z], to: street }); for (const y of [0.25, 0.75]) M(new THREE.TorusGeometry(0.43, 0.03, 6, 18), toon(0x2a2530), { p: [x, y, z], r: [Math.PI / 2, 0, 0], to: street, cast: false }); }
  M(box(0.8, 0.6, 0.8), toon(0xb79a70), { ol: 0.03, p: [4.6, 0.3, -1.0], to: street }); M(box(0.6, 0.5, 0.6), toon(0xb79a70), { ol: 0.03, p: [4.5, 0.85, -1.0], r: [0, 0.4, 0], to: street });
  M(box(0.5, 2.6, 0.5), toon(0x5a3a22), { ol: 0.03, p: [-1.9, 1.3, 1.2], to: street }); // the post people walk into
  for (const s of [-1, 1]) { const h = new THREE.Group(); h.position.set(s * 9.4, 0, -2.6); street.add(h); const tex = houseTex(31 + (s > 0 ? 7 : 0), s > 0 ? '#d9c290' : '#cdb48a'); const m = toon(0xffffff, { map: tex }); M(box(4.6, 6.2, 4), [m, m, toon(0x8a3b2c), toon(0x8a3b2c), m, m], { ol: 0.04, p: [0, 3.1, 0], to: h }); }
  // night sky: gradient dome, moon, stars
  const skyT = ctex(16, 256, g => { const r = g.createLinearGradient(0, 0, 0, 256); r.addColorStop(0, '#0a0f2e'); r.addColorStop(0.6, '#1f2a5a'); r.addColorStop(1, '#4a3a6a'); g.fillStyle = r; g.fillRect(0, 0, 16, 256); });
  M(new THREE.SphereGeometry(60, 32, 16), new THREE.MeshBasicMaterial({ map: skyT, side: THREE.BackSide }), { to: street, cast: false }); M(sph(1.6, 24, 16), flat(0xfff4c2), { p: [-8, 14, -30], to: street, cast: false }); glow(street, -8, 14, -29, 7, 0.4);
  for (let i = 0; i < 90; i++) { const a = rnd() * 6.283, e = 0.25 + rnd() * 0.9; M(sph(0.08 + rnd() * 0.08, 4, 3), flat(0xffffff), { p: [Math.cos(a) * 50 * Math.cos(e), 50 * Math.sin(e), Math.sin(a) * 50 * Math.cos(e) - 10], to: street, cast: false }); }
}
// a golden "smell ribbon" that drifts out of the window and curls like a beckoning finger
const smell = new THREE.Group(); root.add(smell); const smellM = new THREE.MeshBasicMaterial({ color: 0xffe08a, transparent: true, opacity: 0.55, depthWrite: false });
let smellMesh = null;
function smellAt(t, from, to, amp = 0.5) { smell.visible = true; if (smellMesh) { smell.remove(smellMesh); smellMesh.geometry.dispose(); } const pts = []; for (let i = 0; i <= 24; i++) { const k = i / 24, p = from.clone().lerp(to, k); p.y += Math.sin(k * Math.PI) * 0.6 + Math.sin(k * 12 - t * 4) * amp * 0.35; p.x += Math.cos(k * 10 - t * 3) * amp * 0.2; pts.push(p); } smellMesh = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 60, 0.09, 8), smellM); smell.add(smellMesh); }
function streetLook(t) { street.visible = true; bg(0x0a0f2e); light(0.42, 0.6, [-6, 14, -10], 0xa8b8ff, 0x2a2440); street.userData.winLight.intensity = 13 + 1.5 * Math.sin(t * 9); lanternGlows.forEach((g, i) => g.material.opacity = 0.62 + 0.08 * Math.sin(t * 7 + i)); street.userData.sign.rotation.x = 0.08 * Math.sin(t * 1.6);
  steamAt(sSteam, t, WIN.x, WIN.y + 0.9, -1.3, 2.4, 0.7, 0.9); steamAt(street.userData.chimney, t, 3, 10.2, 0, 3.0, 0.4, 1.3); LOOK.grade = ['#6a7ad0', 0.16]; LOOK.bloom = 0.32; }

const SETS = [court, kitchen, street, smell, bread, coin, gavel, ladle, ...CAST.map(c => c.g)];
function hideAll() { SETS.forEach(g => g.visible = false); }
function hold(c, hand, obj, off = V(0, 0, 0), rot = [0, 0, 0]) { c.g.updateMatrixWorld(true); const p = V(...hand); c.up.localToWorld(p); obj.visible = true; obj.position.copy(p).add(off); obj.rotation.set(...rot); }
// ---------- second-half props ----------
const voidG = new THREE.Group(); root.add(voidG);
{ M(new THREE.PlaneGeometry(20, 30), flat(0x2b2aa8), { p: [0, 3, -4], to: voidG, cast: false });
  const pts = []; for (let i = 0; i <= 12; i++) { const s = i / 12; pts.push(new THREE.Vector2(0.15 + 1.05 * Math.sin(s * Math.PI / 2), -0.55 + s * 0.6)); } const bowl = M(new THREE.LatheGeometry(pts, 40), toon(0xf3efe6, { side: THREE.DoubleSide }), { ol: 0.05, p: [0, 1.2, 0], to: voidG }); voidG.userData.bowl = bowl;
  M(new THREE.CircleGeometry(1.1, 36), flat(0xe8742a), { p: [0, 1.22, 0], r: [-Math.PI / 2, 0, 0], to: voidG, cast: false }); M(cyl(0.45, 0.55, 0.15, 24), toon(0xf3efe6), { ol: 0.04, p: [0, 0.6, 0], to: voidG });
  for (const [x, z] of [[0.35, 0.2], [-0.3, -0.25], [0.05, 0.4]]) M(sph(0.12, 10, 8), flat(0xd63b2f), { ol: 0.015, p: [x, 1.25, z], to: voidG, cast: false }); }
const vSteam = steamCloud(voidG, 14);
const fist = new THREE.Group(); root.add(fist);
{ const m = flat(0xfcfbf6); M(sph(0.38, 20, 14), m, { ol: 0.04, s: [1, 0.9, 0.8], to: fist }); fist.userData.f = []; for (let i = 0; i < 4; i++) { const f = new THREE.Group(); f.position.set(-0.24 + i * 0.16, 0.25, 0.18); fist.add(f); M(new THREE.CapsuleGeometry(0.07, 0.28, 4, 8), m, { ol: 0.03, p: [0, 0.2, 0], to: f }); fist.userData.f.push(f); } const th = new THREE.Group(); th.position.set(0.32, 0.0, 0.15); fist.add(th); M(new THREE.CapsuleGeometry(0.075, 0.22, 4, 8), m, { ol: 0.03, p: [0, 0.16, 0], to: th }); th.rotation.z = -0.9; fist.userData.th = th; M(cyl(0.3, 0.32, 0.6, 16), flat(0xd64a3a), { ol: 0.04, p: [0, -0.55, 0], to: fist }); }
function fistPose(k) { fist.userData.f.forEach(f => f.rotation.x = k * 1.9); fist.userData.th.rotation.z = -0.9 + k * 0.9; }
const SETS2 = [voidG, fist];
const hideAll0 = hideAll; hideAll = function () { hideAll0(); SETS2.forEach(g => g.visible = false); CAST.forEach(c => c.tint(0xffffff)); };
function dawnLook(t) { street.visible = true; bg(0xf2b07a); light(0.85, 1.6, [8, 6, 20], 0xffd9b0, 0x6a5a70); street.userData.winLight.intensity = 3; lanternGlows.forEach(g => g.material.opacity = 0.2); street.userData.sign.rotation.x = 0.06 * Math.sin(t * 1.6); steamAt(street.userData.chimney, t, 3, 10.2, 0, 3.0, 0.4, 1.3); LOOK.grade = ['#ffb070', 0.2]; LOOK.bloom = 0.22; }
function soundRings(t, x, y, t0, n = 3, col = '#ffd23e') { if (t < t0) return; ctx.save(); ctx.lineCap = 'round'; for (let i = 0; i < n; i++) { const p = ((t - t0) * 1.6 + i / n) % 1, r = 60 + p * 240, a = 1 - p; for (const s of [-1, 1]) for (const [lw, c] of [[22, `rgba(27,21,34,${a})`], [11, col]]) { ctx.strokeStyle = c; ctx.globalAlpha = c === col ? a : 1; ctx.lineWidth = lw; ctx.beginPath(); ctx.arc(x, y, r, s > 0 ? -0.6 : Math.PI - 0.6, s > 0 ? 0.6 : Math.PI + 0.6); ctx.stroke(); } } ctx.restore(); }
// ---------- helpers ----------
const S = i => Ls[i].s, CUT = i => i === 0 ? 0 : Ls[i].s - 0.1;
function wf(i, str, nth = 1) { let n = 0; for (const w of Ls[i].words) if (w.w.toLowerCase().replace(/[^a-z0-9']/g, '').startsWith(str)) { if (++n === nth) return w.s; } console.log('word not found', i, str); return Ls[i].s; }
function setCam(p, l, fov, t, shake = 0, roll = 0) { cam.fov = fov; cam.position.set(p[0] + 0.02 * Math.sin(t * 1.3) + shake * Math.sin(t * 61), p[1] + 0.015 * Math.sin(t * 1.7 + 1) + shake * Math.sin(t * 53), p[2]); cam.lookAt(l[0], l[1], l[2]); cam.rotateZ(roll); cam.updateProjectionMatrix(); }
const bg = c => { root.background = new THREE.Color(c); };
const SC = 0.86;
function show(c, x, z, ry = 0, tint = 0xffffff) { if (c.g.parent !== root) root.add(c.g); c.g.visible = true; c.g.position.set(x, 0, z); c.g.rotation.set(0, ry, 0); c.g.scale.setScalar(SC); c.tint(tint); c.hatG.position.set(0, 0, 0); c.hatG.rotation.set(0, 0, 0); c.g.updateMatrixWorld(true); }
function toLocal(c, w) { const p = w.clone(); c.up.worldToLocal(p); return [p.x, p.y, p.z]; }
function wisps(t, pts, col = '#8fd04a') { ctx.save(); ctx.lineCap = 'round'; pts.forEach(([x, y], i) => { for (const [lw, c] of [[20, INK], [11, col]]) { ctx.strokeStyle = c; ctx.lineWidth = lw; ctx.beginPath(); for (let k = 0; k <= 12; k++) { const yy = y - k * 16 - ((t * 60 + i * 37) % 60), xx = x + Math.sin(k * 0.7 + t * 4 + i) * 22; k ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); } ctx.stroke(); } }); ctx.restore(); }

// ---------- timeline ----------
function update(t) {
  hideAll(); overlay = () => { };
  let li = 0; for (let i = 0; i < Ls.length; i++) if (t >= CUT(i)) li = i;
  const s0 = CUT(li), s1 = li + 1 < Ls.length ? CUT(li + 1) : DUR, k = (t - s0) / (s1 - s0);
  const sub = (a, b) => cl((t - a) / (b - a));
  LOOK.grade = ['#ffc98a', 0.1]; LOOK.bloom = 0.14; LOOK.dof = null;

  if (li === 0) { // HOOK: the cook points at the beggar in court; the judge lifts a coin
    const tb = wf(0, 'breathing') - 0.05, tj = wf(0, 'and') - 0.08; courtLook(t);
    show(judge, BENCH.x, BENCH.z - 0.4, 0); judge.g.position.y = 0.9; judge.g.updateMatrixWorld(true);
    show(cook, -1.7, -1.1, 0.5); show(pip, 1.5, -1.0, -0.45); pip.g.scale.setScalar(SC * 0.85);
    townsfolk.forEach((c, i) => { const r = Math.floor(i / 4), j = i % 4; show(c, -1.35 + j * 0.9 + r * 0.45, 1.7 + r * 1.3, Math.PI + (j - 1.5) * 0.08); c.g.scale.setScalar(SC * 0.82); c.g.position.y = -1.35 + r * 0.2; c.legs.forEach(l => { l.a.visible = false; l.f.visible = false; }); c.face(t > tj ? 'shock' : 'neutral'); c.pose({ lh: [-0.5, 2.05, 0.05], rh: [0.5, 2.05, 0.05], hx: 0.05 }); });
    cook.face('angry'); cook.pose({ rh: [0.9, 2.8, 0.6], lh: [-0.5, 1.9, 0.2], lean: -0.06, bob: 0.03 * Math.abs(Math.sin(t * 8)) });
    pip.face(t < tb ? 'neutral' : 'shock'); pip.pose({ lh: [-0.4, 1.9, 0.5], rh: [0.4, 1.9, 0.5], hx: 0.1 }); hold(pip, [0.4, 1.9, 0.5], bread, V(-0.15, 0.05, 0.1), [0, 0.3, 0.2]);
    if (t < tj) { judge.face('neutral'); judge.pose({ lh: [-0.4, 1.95, 0.6], rh: [0.6, 2.1, 0.6] }); hold(judge, [0.6, 2.1, 0.6], gavel, V(0, 0.25, 0), [0, 0.2, 0.3]);
      const u = sub(0, tj); setCam([lerp(0.5, 0.2, u), lerp(4.2, 3.7, u), lerp(10.5, 8.8, ss(0, 1, u))], [0, 2.3, -2.2], 52, t, 0, lerp(-0.05, 0.02, u));
      overlay = () => { popText('SUED A BEGGAR', W / 2, 250, 112, '#fff', t, wf(0, 'sued') - 0.05, tj - 0.02); popText('FOR BREATHING', W / 2, 390, 112, '#ffd23e', t, tb, tj - 0.02); };
    } else { judge.face('sneaky'); const v = sub(tj, tj + 0.5); judge.pose({ lh: [-0.4, 1.95, 0.6], rh: [0.5, lerp(2.1, 3.1, ss(0, 1, v)), 0.6], hx: -0.15 }); hold(judge, [0.5, lerp(2.1, 3.1, ss(0, 1, v)), 0.6], coin, V(0, 0.2, 0.05), [0, t * 3, 0]);
      const hp = judge.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 0.9, hp.y - 0.2, hp.z + lerp(5.0, 4.0, sub(tj, s1))], [hp.x + 0.2, hp.y + 0.2, hp.z], 44, t, 0, -0.05); LOOK.dof = [380, 1350, 5];
      overlay = () => { popText('PAID WITH', W / 2, 250, 130, '#fff', t, wf(0, 'paid') - 0.05, s1 - 0.02); popText('NOISE', W / 2, 400, 170, '#ffd23e', t, wf(0, 'noise') - 0.05, s1 - 0.02); };
    }
  }
  else if (li === 1) { // the soup, then people walking into walls
    const tw = wf(1, 'people') - 0.1;
    if (t < tw) { kitchenLook(t); show(cook, POT.x - 1.25, POT.z + 0.6, 0.7); cook.face('happy'); const st = t * 3; cook.pose({ rh: [0.55 + 0.15 * Math.cos(st), 2.15, 0.7 + 0.15 * Math.sin(st)], lh: [-0.4, 1.9, 0.4], hx: 0.2, hy: 0.3, bob: 0.02 * Math.sin(st * 2) });
      cook.g.updateMatrixWorld(true); const hp = V(0.55 + 0.15 * Math.cos(st), 2.15, 0.7 + 0.15 * Math.sin(st)); cook.up.localToWorld(hp); ladle.visible = true; ladle.position.set(hp.x + 0.15, 1.6, hp.z); ladle.rotation.set(0.2 * Math.sin(st), 0, -0.35);
      const u = sub(s0, tw); setCam([lerp(1.4, 0.9, u), lerp(3.0, 3.8, u), lerp(6.8, 5.0, ss(0, 1, u))], [POT.x - 0.4, lerp(2.0, 1.6, u), POT.z], 50, t, 0, 0.05); LOOK.dof = [500, 1450, 4];
      overlay = () => popText("BARTHOLOMEW'S", W / 2, 260, 112, '#ffd23e', t, s0 + 0.1, tw - 0.02);
    } else { streetLook(t); const v = sub(tw, s1), walker = townsfolk[2];
      const wz = lerp(4.5, 1.25, ss(0, 0.8, v)), bonk = v > 0.8; show(walker, -1.9, wz, Math.PI); walker.face(bonk ? 'shock' : 'happy'); walker.pose(bonk ? { lean: 0.25 * Math.exp(-(v - 0.8) * 8) * Math.sin((v - 0.8) * 40), pitch: -0.25, hx: -0.3 } : { ...walker.walk(t * 6, 0.22), hx: -0.35, hy: -0.4, pitch: 0.08 });
      smellAt(t, V(WIN.x, WIN.y, -1.3), V(-1.9, 3.3, wz - 0.1), 0.6);
      show(townsfolk[4], 2.4, lerp(5.5, 2.6, ss(0, 1, v)), Math.PI + 0.5); townsfolk[4].face('happy'); townsfolk[4].pose({ ...townsfolk[4].walk(t * 6 + 1, 0.22), hx: -0.35 });
      setCam([lerp(-0.4, -0.9, v), 2.6, lerp(8.4, 7.4, v)], [-1.0, 2.2, 0.5], 52, t, bonk ? 0.01 : 0, -0.04);
      overlay = () => { if (bonk) burst('BONK!', 290, 520, 170, t, tw + 0.8 * (s1 - tw), s1 - 0.02, -0.1); popText('INTO WALLS', W / 2, 260, 130, '#fff', t, wf(1, 'walls') - 0.1, s1 - 0.02); };
    }
  }
  else if (li === 2) { // Pip under the window with dry bread, sniffing
    streetLook(t); const tp = wf(2, 'pip') - 0.1, ts = wf(2, 'sniffing') - 0.15;
    show(pip, WIN.x + 0.3, WIN.z + 0.9, 0.15); pip.g.scale.setScalar(SC * 0.85); const sn = t > ts ? Math.abs(Math.sin((t - ts) * 9)) : 0;
    pip.face(t > ts ? 'happy' : 'neutral'); pip.pose({ bob: -0.75, lf: [-0.25, 0, 0.5], rf: [0.25, 0, 0.5], lh: [-0.4, 1.75, 0.55], rh: [0.35, 1.7, 0.55], hx: -0.25 - 0.08 * sn, hy: -0.2 });
    hold(pip, [0.35, 1.7, 0.55], bread, V(-0.05, 0.1, 0.1), [0, 0.3, 0.3]); smellAt(t, V(WIN.x, WIN.y + 0.3, -1.3), V(WIN.x + 0.3, 2.35, WIN.z + 1.3), 0.45);
    if (t < tp) setCam([lerp(2.6, 1.8, k * 3), lerp(4.8, 3.4, k * 3), lerp(8.6, 6.8, k * 3)], [WIN.x, 2.0, -1.2], 50, t, 0, 0.03);
    else { const hp = pip.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 1.0, hp.y + 0.3, hp.z + lerp(4.8, 4.0, sub(tp, s1))], [hp.x - 0.1, hp.y + 0.2, hp.z - 0.3], 46, t, 0, 0.05); LOOK.dof = [450, 1400, 5]; }
    overlay = () => { popText('PIP', W / 2, 270, 160, '#ffd23e', t, tp, wf(2, 'sat') - 0.02); popText('DRY BREAD', W / 2, 270, 130, '#fff', t, wf(2, 'dry') - 0.05, ts - 0.02); popText('SNIFF', W / 2, 270, 160, '#ffd23e', t, ts + 0.1, s1 - 0.02); };
  }
  else if (li === 3) { // one sniff, two sniffs, a whole bowl of smell
    streetLook(t); const t1 = wf(3, 'one') - 0.05, t2 = wf(3, 'two') - 0.05, tb = wf(3, 'a') - 0.08;
    show(pip, WIN.x + 0.3, WIN.z + 0.9, 0.15); pip.g.scale.setScalar(SC * 0.85); const sn = Math.abs(Math.sin((t - s0) * 9));
    pip.face(t > tb ? 'happy' : 'sneaky'); pip.pose({ bob: -0.75, lf: [-0.25, 0, 0.5], rf: [0.25, 0, 0.5], lh: [-0.4, 1.75, 0.55], rh: [0.35, t > tb ? 2.05 : 1.7, 0.55], hx: -0.3 - 0.1 * sn, hy: -0.2 + (t > tb ? 0.2 : 0) });
    hold(pip, [0.35, t > tb ? 2.05 : 1.7, 0.55], bread, V(-0.05, 0.1, 0.1), [0, 0.3, 0.3]);
    const hp = pip.headG.getWorldPosition(V(0, 0, 0)); smellAt(t, V(WIN.x, WIN.y + 0.3, -1.3), hp.clone().add(V(0, 0.05, 0.55)), 0.4 + 0.3 * sn);
    if (t < tb) setCam([hp.x + 0.8, hp.y + 0.3, hp.z + lerp(4.0, 3.4, sub(s0, tb))], [hp.x, hp.y - 0.1, hp.z], 44, t, 0, 0.06);
    else setCam([hp.x - 1.4, hp.y + 0.5, hp.z + lerp(3.8, 3.2, sub(tb, s1))], [hp.x, hp.y - 0.1, hp.z - 0.3], 46, t, 0, -0.05);
    LOOK.dof = [420, 1350, 5];
    overlay = () => { popText('1 SNIFF', W / 2, 270, 150, '#fff', t, t1, t2 - 0.02); popText('2 SNIFFS', W / 2, 270, 150, '#ffd23e', t, t2, tb - 0.02); popText('A WHOLE BOWL', W / 2, 250, 120, '#fff', t, tb, s1 - 0.02); popText('FOR FREE', W / 2, 395, 136, '#ffd23e', t, wf(3, 'free') - 0.05, s1 - 0.02); };
  }
  else if (li === 4) { // the cook bursts out and grabs Pip by the collar
    streetLook(t); const tg = wf(4, 'grabbed') - 0.1, ty = wf(4, 'you') - 0.08, u = sub(s0, tg);
    const cx = lerp(3.0, 1.15, ss(0, 1, u)), cz = lerp(-1.4, -0.7, ss(0, 1, u)); show(cook, cx, cz, -1.1); cook.face('angry');
    const lift = t > tg ? ss(tg, tg + 0.35, t) : 0; show(pip, WIN.x + 0.3, WIN.z + 0.9, 0.6); pip.g.scale.setScalar(SC * 0.85); pip.g.position.y = lift * 0.85; pip.g.updateMatrixWorld(true);
    pip.face(lift > 0.3 ? 'shock' : 'neutral'); pip.pose(lift > 0.01 ? { lf: [-0.2, 0.15 * Math.sin(t * 14), 0.15], rf: [0.2, -0.15 * Math.sin(t * 14), 0.15], lh: [-0.7, 2.0, 0.2], rh: [0.7, 2.0, 0.2] } : { bob: -0.75, lf: [-0.25, 0, 0.5], rf: [0.25, 0, 0.5], lh: [-0.4, 1.75, 0.55], rh: [0.35, 1.7, 0.55], hy: 0.6 });
    if (lift < 0.5) hold(pip, [0.35, 1.7, 0.55], bread, V(-0.05, 0.1, 0.1), [0, 0.3, 0.3]);
    const neck = pip.headG.getWorldPosition(V(0, 0, 0)).add(V(0.35, -0.55, 0)); cook.pose(t > tg - 0.15 ? { rh: toLocal(cook, neck), lh: [-0.5, 2.4, 0.5], lean: 0.08, bob: 0.02 * Math.sin(t * 20) } : { ...cook.walk(t * 9, 0.3), lh: [-0.6, 2.2, 0.4], rh: [0.6, 2.2, 0.4] });
    if (t < tg) setCam([2.6, 2.4, 6.6], [1.6, 1.9, -1.2], 52, t, 0, 0.04);
    else { const ch = cook.headG.getWorldPosition(V(0, 0, 0)); setCam([ch.x - 2.2, ch.y - 0.2, ch.z + lerp(4.4, 3.8, sub(tg, s1))], [(ch.x + neck.x) / 2, ch.y - 0.3, ch.z], 46, t, t > ty ? 0.008 : 0, -0.06); }
    overlay = () => { burst('YOU ATE MY SMELL!', 540, 330, 220, t, ty, wf(4, 'pay') - 0.03, -0.05); burst('PAY UP!', 540, 330, 200, t, wf(4, 'pay') - 0.03, s1 - 0.02, 0.06); };
  }
  else if (li === 5) { // Pip has nothing except one bent coin
    streetLook(t); const tc = wf(5, 'except') - 0.1; show(pip, 0.6, -0.4, 0.2); pip.g.scale.setScalar(SC * 0.85); pip.g.position.y = 0.5; pip.g.updateMatrixWorld(true); pip.face(t < tc ? 'sad' : 'neutral');
    pip.pose(t < tc ? { lh: [-0.62, 1.4, 0.15], rh: [0.62, 1.4, 0.15], lf: [-0.2, 0.1, 0.1], rf: [0.2, 0, 0.1] } : { rh: [0.3, 2.0, 0.75], lh: [-0.5, 1.6, 0.3], hx: 0.35, lf: [-0.2, 0.1, 0.1], rf: [0.2, 0, 0.1] });
    if (t > tc) { hold(pip, [0.3, 2.0, 0.75], coin, V(0, 0.12, 0.05), [0.3, 0.2 * Math.sin(t * 2), 0]); coin.scale.setScalar(1.5); } else coin.scale.setScalar(1);
    const hp = pip.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 0.5, hp.y - 0.3, hp.z + lerp(3.2, 2.6, k)], [hp.x, hp.y - 0.7, hp.z + 0.3], 44, t, 0, 0.05); LOOK.dof = [450, 1450, 5];
    overlay = () => { popText('NOTHING', W / 2, 270, 160, '#fff', t, wf(5, 'nothing') - 0.05, tc - 0.02); popText('1 BENT COIN', W / 2, 270, 130, '#ffd23e', t, wf(5, 'bent') - 0.05, s1 - 0.02); };
  }
  else if (li === 6) { // marched to court, the whole town followed (dawn)
    dawnLook(t); const u = sub(s0, s1), z0 = lerp(3.5, -6, u);
    show(cook, -0.4, z0, Math.PI); cook.face('angry'); cook.pose({ ...cook.walk(t * 8, 0.3), rh: [0.7, 2.0, -0.4], lh: [-0.6, 2.0, 0.2] });
    show(pip, 0.5, z0 + 0.5, Math.PI); pip.g.scale.setScalar(SC * 0.85); pip.face('sad'); pip.pose({ ...pip.walk(t * 8 + 1, 0.28), lh: [-0.7, 2.6, 0.3], rh: [0.7, 2.6, 0.3] });
    townsfolk.forEach((c, i) => { show(c, -1.6 + (i % 4) * 1.05 + 0.3 * Math.sin(i), z0 + 2.2 + Math.floor(i / 4) * 1.5 + (i % 2) * 0.4, Math.PI); c.face(i % 3 ? 'happy' : 'neutral'); c.pose({ ...c.walk(t * 8 + i, 0.26), rh: i % 3 === 0 ? [0.6, 2.7, 0.2] : [0.5, 1.95, 0.05] }); });
    setCam([lerp(2.2, 1.0, u), lerp(5.5, 4.5, u), lerp(12, 4, u)], [0, 1.6, lerp(0, -9, u)], 56, t, 0, 0.03);
    overlay = () => popText('THE WHOLE TOWN', W / 2, 260, 104, '#fff', t, wf(6, 'whole') - 0.05, s1 - 0.02);
  }
  else if (li >= 7 && li <= 12) { // ===== the courtroom =====
    courtLook(t); show(judge, BENCH.x - 0.5, BENCH.z - 0.4, 0); judge.g.position.y = 0.9; judge.g.updateMatrixWorld(true);
    townsfolk.forEach((c, i) => { const r = Math.floor(i / 4), j = i % 4; show(c, -1.35 + j * 0.9 + r * 0.45, 1.7 + r * 1.3, Math.PI + (j - 1.5) * 0.08); c.g.scale.setScalar(SC * 0.82); c.g.position.y = -1.35 + r * 0.2; c.legs.forEach(l => { l.a.visible = false; l.f.visible = false; }); const laugh = li === 12; c.face(laugh ? 'happy' : 'neutral'); const lf = laugh ? Math.abs(Math.sin(t * 7 + i)) : 0; c.pose({ bob: 0.12 * lf, lh: [-0.5, 2.05 + 0.4 * lf, 0.05], rh: [0.5, 2.05 + 0.4 * lf, 0.05], lean: laugh ? 0.08 * Math.sin(t * 7 + i) : 0 }); });
    show(pip, 1.2, -1.6, -0.4); pip.g.scale.setScalar(SC * 0.85); pip.face(li >= 11 ? 'happy' : 'sad'); pip.pose({ lh: [-0.4, 1.9, 0.5], rh: [0.4, 1.9, 0.5] });
    const near = li >= 9; show(cook, near ? -0.6 : -1.5, near ? -2.7 : -1.6, near ? 0.15 : 0.5);
    if (li === 7) { const tn = wf(7, 'he') - 0.08, ta = wf(7, 'then') - 0.08;
      cook.face('angry'); cook.pose({ rh: [0.8 + 0.2 * Math.sin(t * 9), 2.7, 0.6], lh: [-0.7, 2.4 + 0.2 * Math.cos(t * 8), 0.4], bob: 0.03 * Math.abs(Math.sin(t * 9)) });
      judge.face('neutral'); judge.pose({ lh: [-0.4, 1.95, 0.6], rh: t > ta ? [0.6, 2.3, 0.9] : [0.4, 1.95, 0.6], hx: t > tn && t < ta ? 0.25 * Math.abs(Math.sin((t - tn) * 7)) : 0 });
      if (t < ta) setCam([lerp(0.2, -0.3, sub(s0, ta)), 3.6, 8.2], [-0.5, 2.6, -2.5], 50, t, 0, -0.03);
      else { const hp = judge.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 0.6, hp.y - 0.2, hp.z + 4.2], [hp.x + 0.2, hp.y - 0.4, hp.z], 44, t, 0, 0.05); }
      overlay = () => { popText('LISTENED', W / 2, 260, 140, '#fff', t, s0 + 0.05, tn - 0.02); popText('NODDED', W / 2, 260, 150, '#fff', t, tn, ta - 0.02); popText("PIP'S COIN", W / 2, 260, 136, '#ffd23e', t, wf(7, 'coin') - 0.3, s1 - 0.02); };
    } else if (li === 8) { cook.face('happy'); cook.pose({ rh: [0.55, 1.9, 0.85], lh: [-0.5, 1.95, 0.05], hx: -0.1 }); judge.face('neutral'); judge.pose({ lh: [-0.4, 1.95, 0.6], rh: [0.6, 2.2, 0.8] }); hold(judge, [0.6, 2.2, 0.8], coin, V(0, 0.12, 0.05), [0.3, t * 2, 0]);
      const hp = cook.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x - 0.4, hp.y + 0.1, hp.z + lerp(3.6, 3.0, k)], [hp.x + 0.3, hp.y - 0.5, hp.z], 44, t, 0, -0.05); LOOK.dof = [400, 1400, 5];
      overlay = () => popText('GRINNED', W / 2, 270, 150, '#ffd23e', t, wf(8, 'grinned') - 0.05, s1 - 0.02);
    } else if (li === 9 || li === 10) { const tc = wf(9, 'clink') - 0.05, shake = li === 9 && t > wf(9, 'shook') - 0.1 ? Math.sin(t * 30) * 0.08 : 0;
      cook.face(li === 9 ? 'happy' : 'shock'); cook.pose({ rh: [0.55, 1.9, 0.85], lh: [-0.5, 1.95, 0.05], hy: li === 10 ? 0.3 : 0 });
      const ear = cook.headG.getWorldPosition(V(0, 0, 0)).add(V(-0.75, 0.05, 0.1)); judge.face('sneaky'); judge.pose({ pitch: 0.28, lh: [-0.4, 1.95, 0.6], rh: toLocal(judge, ear.clone().add(V(0, shake, 0))) });
      coin.visible = true; coin.scale.setScalar(1.3); coin.position.copy(ear).add(V(0, 0.15 + shake, 0)); coin.rotation.set(0.2, 0, shake * 4);
      if (li === 9) setCam([ear.x - 1.0, ear.y + 0.3, ear.z + lerp(3.6, 3.0, k)], [ear.x + 0.4, ear.y - 0.2, ear.z], 46, t, 0, 0.05);
      else { const jp = judge.headG.getWorldPosition(V(0, 0, 0)); setCam([jp.x + 0.5, jp.y - 0.3, jp.z + lerp(3.8, 3.3, k)], [jp.x, jp.y - 0.35, jp.z], 42, t, 0, -0.05); }
      overlay = () => { if (li === 9) { const [x, y] = proj(coin.position); soundRings(t, x, y, wf(9, 'shook') + 0.1); burst('CLINK!', 300, 450, 150, t, tc, wf(9, 'clink', 2) - 0.03, -0.1); burst('CLINK!', 780, 480, 150, t, wf(9, 'clink', 2), s1 - 0.02, 0.1); } else { popText('THAT IS', W / 2, 250, 130, '#fff', t, wf(10, "that's") - 0.05, s1 - 0.02); popText('YOUR PAYMENT', W / 2, 395, 120, '#ffd23e', t, wf(10, 'payment') - 0.05, s1 - 0.02); popText('HEAR THAT?', W / 2, 270, 136, '#fff', t, s0 + 0.05, wf(10, "that's") - 0.05); } };
    } else if (li === 11) { const te = wf(11, 'even') - 0.1; cook.face('shock'); cook.pose({ lh: [-0.5, 1.95, 0.05], rh: [0.5, 1.95, 0.05] }); judge.face('happy');
      const bang = t > te ? Math.exp(-(t - te) * 10) : 0; judge.pose({ lh: [-0.4, 1.95, 0.6], rh: [0.6, 2.5 - 0.5 * ss(te - 0.15, te, t), 0.6] }); hold(judge, [0.6, 2.5 - 0.5 * ss(te - 0.15, te, t), 0.6], gavel, V(0, 0.25, 0), [0, 0.2, 0.3]);
      setCam([lerp(0.6, 0.2, k), 3.6, lerp(8.0, 7.2, k)], [-0.3, 2.6, -2.5], 50, t, bang * 0.03, 0.03);
      overlay = () => { popText('HE SMELLED', W / 2, 250, 120, '#8fd04a', t, s0 + 0.05, wf(11, 'you') - 0.05); popText('YOU HEARD', W / 2, 250, 120, '#ffd23e', t, wf(11, 'you') - 0.05, te - 0.02); popText("YOU'RE EVEN", W / 2, 270, 140, '#fff', t, te, s1 - 0.02); burst('BANG!', 780, 1050, 150, t, te, te + 0.5, 0.1); };
    } else { const tr = wf(12, 'bartholomew') - 0.1, red = ss(tr, tr + 0.9, t); cook.face('angry'); cook.tint(new THREE.Color(0xffffff).lerp(new THREE.Color(0xff5a46), red).getHex()); cook.pose({ lh: [-0.5, 1.95, 0.05], rh: [0.5, 1.95, 0.05], bob: -0.04 * red });
      judge.face('happy'); judge.pose({ lh: [-0.4, 1.95, 0.6], rh: [0.4, 1.95, 0.6], bob: 0.03 * Math.abs(Math.sin(t * 7)) });
      if (t < tr) setCam([0, 3.0, lerp(10, 9.2, sub(s0, tr))], [0, 2.0, -1], 54, t, 0, -0.03);
      else { const hp = cook.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 0.5, hp.y, hp.z + lerp(3.6, 3.0, sub(tr, s1))], [hp.x, hp.y - 0.35, hp.z], 42, t, 0, 0.05); }
      overlay = () => { if (t < tr) { burst('HA HA HA!', 300, 520, 170, t, s0 + 0.1, tr - 0.02, -0.1); burst('HA HA!', 780, 620, 140, t, s0 + 0.4, tr - 0.02, 0.12); } popText('RED AS', W / 2, 250, 124, '#fff', t, wf(12, 'red') - 0.05, s1 - 0.02); popText('HIS TOMATOES', W / 2, 395, 116, '#ff5a4a', t, wf(12, 'tomatoes') - 0.05, s1 - 0.02); };
    }
  }
  else if (li === 13) { // "You see," explainer on blue: you can't hold a smell
    voidG.visible = true; bg(0x2b2aa8); light(1.2, 1.4, [3, 5, 8], 0xffffff, 0x5a5ac0); LOOK.grade = null; LOOK.bloom = 0.12;
    steamAt(vSteam, t, 0, 1.5, 0, 3.2, 0.5, 1.0); const tg = wf(13, 'charge') - 0.1, v = sub(tg, tg + 0.5), clench = ss(tg + 0.35, tg + 0.6, t), open = ss(tg + 1.2, tg + 1.5, t);
    fist.visible = true; fist.position.set(lerp(2.2, 0.15, ss(0, 1, v)), 3.4, 0.4); fist.rotation.set(0, 0, 0.3); fistPose(clench * (1 - open));
    smellAt(t, V(0, 1.3, 0), V(0.1, 5.2, 0.2), 0.5);
    setCam([lerp(0.6, 0.1, k), 2.9, lerp(9.5, 8.4, k)], [0, 2.7, 0], 44, t, 0, 0.03);
    overlay = () => { popText("CAN'T CHARGE", W / 2, 250, 120, '#fff', t, wf(13, 'charge') - 0.3, s1 - 0.02); popText('NOBODY CAN HOLD', W / 2, 395, 100, '#ffd23e', t, wf(13, 'nobody') - 0.05, s1 - 0.02); if (open > 0.5) popText('NOTHING!', W / 2, 1150, 130, '#ff5a4a', t, tg + 1.3, s1 - 0.02, { rot: -0.05 }); };
  }
  else { // ending: Pip flips his coin at dawn; the cook gets paid in noise (callback to the hook)
    const tb = wf(14, 'and') - 0.08;
    if (t < tb) { dawnLook(t); show(pip, 0.4, lerp(1.5, 0.2, sub(s0, tb)), 0.25); pip.g.scale.setScalar(SC * 0.85); pip.face('happy'); const fl = ((t - s0) * 1.4) % 1; pip.pose({ ...pip.walk(t * 6, 0.22), rh: [0.45, 2.0, 0.55], lh: [-0.5, 1.75, 0.4] }); hold(pip, [-0.5, 1.75, 0.4], bread, V(0.1, 0.05, 0.1), [0, 0.3, 0.2]);
      pip.g.updateMatrixWorld(true); const hp = V(0.45, 2.0, 0.55); pip.up.localToWorld(hp); coin.visible = true; coin.scale.setScalar(1.3); coin.position.copy(hp).add(V(0, 0.2 + Math.sin(fl * Math.PI) * 1.0, 0)); coin.rotation.set(fl * 14, 0, 0);
      const ph = pip.headG.getWorldPosition(V(0, 0, 0)); setCam([ph.x + 1.2, ph.y - 0.1, ph.z + 5.0], [ph.x, ph.y - 0.1, ph.z], 46, t, 0, 0.04);
      overlay = () => popText('PIP KEPT HIS COIN', W / 2, 260, 100, '#ffd23e', t, s0 + 0.1, tb - 0.02);
    } else { courtLook(t); show(judge, BENCH.x, BENCH.z - 0.4, 0); judge.g.position.y = 0.9; judge.g.updateMatrixWorld(true); judge.face('sneaky'); judge.pose({ lh: [-0.4, 1.95, 0.6], rh: [0.5, 3.1, 0.6], hx: -0.15 });
      hold(judge, [0.5, 3.1 + 0.06 * Math.sin(t * 30), 0.6], coin, V(0, 0.2, 0.05), [0, t * 3, 0]); coin.scale.setScalar(1.0);
      show(cook, -1.7, -1.1, 0.5); cook.face('sad'); cook.tint(0xffb8a8); cook.pose({ lh: [-0.5, 1.95, 0.05], rh: [0.5, 1.95, 0.05], bob: -0.05 });
      townsfolk.forEach((c, i) => { const r = Math.floor(i / 4), j = i % 4; show(c, -1.35 + j * 0.9 + r * 0.45, 1.7 + r * 1.3, Math.PI + (j - 1.5) * 0.08); c.g.scale.setScalar(SC * 0.82); c.g.position.y = -1.35 + r * 0.2; c.legs.forEach(l => { l.a.visible = false; l.f.visible = false; }); c.face('happy'); c.pose({}); });
      const u = sub(tb, s1); setCam([lerp(0.2, 0.5, u), lerp(3.7, 4.2, u), lerp(8.8, 10.5, ss(0, 1, u))], [0, 2.3, -2.2], 52, t, 0, lerp(0.02, -0.05, u));
      overlay = () => { const [x, y] = proj(coin.position); soundRings(t, x, y, tb + 0.2); popText('PAID IN', W / 2, 250, 140, '#fff', t, wf(14, 'paid') - 0.05, DUR + 1); popText('NOISE', W / 2, 400, 170, '#ffd23e', t, wf(14, 'noise') - 0.05, DUR + 1); };
    }
  }
}

const tmp = document.createElement('canvas'); tmp.width = W; tmp.height = H; const tctx = tmp.getContext('2d');
const small = document.createElement('canvas'); small.width = W / 4; small.height = H / 4; const sctx = small.getContext('2d');
const grains = [0, 1, 2, 3].map(k => { const c = document.createElement('canvas'); c.width = 540; c.height = 960; const g = c.getContext('2d'), d = g.createImageData(540, 960); let sd = 17 + k * 101; for (let i = 0; i < d.data.length; i += 4) { sd = (sd * 16807) % 2147483647; const v = 128 + ((sd / 2147483647) - 0.5) * 120; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; } g.putImageData(d, 0, 0); return c; });
let LOOK = { grade: null, dof: null, bloom: 0.22 };
function cutAge(t) { let a = 99; for (let i = 0; i < Ls.length; i++) { const c = CUT(i); if (t >= c) a = t - c; } return a; }
function renderFrame(t) {
  BOIL.value = Math.floor(t * 8) * 1.7;
  LOOK = { grade: ['#ffcf8a', 0.14], dof: null, bloom: 0.22 };
  update(t); root.updateMatrixWorld(true); renderer.render(root, cam);
  // depth of field: blurred copy everywhere, sharp copy inside the focus band
  if (LOOK.dof) { const [y0, y1, px] = LOOK.dof; ctx.filter = `blur(${px}px)`; ctx.drawImage(glc, 0, 0); ctx.filter = 'none';
    tctx.clearRect(0, 0, W, H); tctx.globalCompositeOperation = 'source-over'; tctx.drawImage(glc, 0, 0); tctx.globalCompositeOperation = 'destination-in';
    const g = tctx.createLinearGradient(0, 0, 0, H); const a = cl(y0 / H), b = cl(y1 / H); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(cl(a - 0.12), 'rgba(0,0,0,0)'); g.addColorStop(a, 'rgba(0,0,0,1)'); g.addColorStop(b, 'rgba(0,0,0,1)'); g.addColorStop(cl(b + 0.12), 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,0)');
    tctx.fillStyle = g; tctx.fillRect(0, 0, W, H); tctx.globalCompositeOperation = 'source-over'; ctx.drawImage(tmp, 0, 0); }
  else ctx.drawImage(glc, 0, 0);
  // zoom-blur punch on every cut (the references' whip/zoom transitions)
  const ca = cutAge(t); if (false) { const k = 1 - ca / 0.16; for (let i = 1; i <= 5; i++) { const s = 1 + 0.035 * i * k; ctx.globalAlpha = 0.16 * k; ctx.drawImage(glc, W / 2 - W * s / 2, H / 2 - H * s / 2, W * s, H * s); } ctx.globalAlpha = 1; }
  // bloom on bright areas
  if (LOOK.bloom) { sctx.filter = 'brightness(0.85) contrast(2.4) blur(10px)'; sctx.drawImage(out, 0, 0, W / 4, H / 4); sctx.filter = 'none'; ctx.globalCompositeOperation = 'screen'; ctx.globalAlpha = LOOK.bloom; ctx.drawImage(small, 0, 0, W, H); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; }
  // colour grade
  if (LOOK.grade) { ctx.globalCompositeOperation = 'soft-light'; ctx.globalAlpha = LOOK.grade[1]; ctx.fillStyle = LOOK.grade[0]; ctx.fillRect(0, 0, W, H); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; }
  const v = ctx.createRadialGradient(W / 2, H / 2, H * 0.3, W / 2, H / 2, H * 0.72); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(20,8,20,0.42)'); ctx.fillStyle = v; ctx.fillRect(0, 0, W, H);
  // film grain
  ctx.globalCompositeOperation = 'overlay'; ctx.globalAlpha = 0.03; ctx.drawImage(grains[Math.floor(t * 24) % 4], 0, 0, W, H); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
  overlay(); caption(t);
  const f = 1 - ss(0, 0.15, t); if (f > 0) { ctx.fillStyle = `rgba(0,0,0,${f})`; ctx.fillRect(0, 0, W, H); }
}
window.renderFrame = t => { renderFrame(t); return out.toDataURL('image/jpeg', 0.94); };
(async () => {
  TM = await (await fetch('timing.json?' + Date.now())).json(); Ls = TM.lines; DUR = TM.voEnd + 0.9;
  await document.fonts.load('92px Pop'); if (window.afterFonts) window.afterFonts(); window.DUR = DUR; renderFrame(0); window.ready = true;
})();
