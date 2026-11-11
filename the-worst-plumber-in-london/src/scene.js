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
// ===== The Worst Plumber in London — scenes =====
let TM, Ls, DUR = 53;
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
const albie = makeChar2({ skin: '#f8cfa4', stubble: true, freckles: true, leg: 0x2c5a6b, shoe: 0x3a2416,
  body: (g, w, h) => { g.fillStyle = '#d9a23a'; g.fillRect(0, 0, w, h); g.fillStyle = '#2c5a6b'; g.fillRect(0, h * 0.52, w, h * 0.48); g.fillRect(w * 0.37, h * 0.2, w * 0.26, h * 0.4); g.fillRect(w * 0.37, 0, w * 0.045, h * 0.3); g.fillRect(w * 0.585, 0, w * 0.045, h * 0.3); g.strokeStyle = '#1b1522'; g.lineWidth = 5; g.strokeRect(w * 0.37, h * 0.2, w * 0.26, h * 0.34); g.strokeRect(w * 0.45, h * 0.3, w * 0.1, h * 0.12); g.fillStyle = '#ffd34d'; for (const x of [0.39, 0.61]) { g.beginPath(); g.arc(w * x, h * 0.215, 8, 0, 7); g.fill(); } },
  hat: flatHat(0x7a5232, 0x5d3d24) });
const townOpts = (robe, sash, hatCol, skin, extra = {}) => ({ skin, leg: 0x1b1522, shoe: 0x3a2416, ...extra,
  body: (g, w, h) => { g.fillStyle = robe; g.fillRect(0, 0, w, h); g.fillStyle = sash; g.fillRect(0, h * 0.5, w, h * 0.06); g.fillStyle = 'rgba(0,0,0,0.18)'; g.beginPath(); g.moveTo(w * 0.44, h); g.lineTo(w * 0.5, h * 0.72); g.lineTo(w * 0.56, h); g.fill(); },
  hat: hg => { const m = flat(hatCol); M(sph(0.49, 32, 16, 0, 6.3, 0, Math.PI * 0.5), m, { ol: 0.035, p: [0, 0.02, -0.04], to: hg }); M(new THREE.TorusGeometry(0.47, 0.06, 8, 28), m, { ol: 0.025, p: [0, 0.02, -0.02], r: [Math.PI / 2 - 0.25, 0, 0], to: hg }); } });
const town = [makeChar2(townOpts('#c98a2a', '#7a4a1c', 0xd9b040, '#f3c79c')), makeChar2(townOpts('#3f8f8a', '#1f5450', 0x57b0aa, '#e9b78a', { stache: true })), makeChar2(townOpts('#b0567a', '#6e2f48', 0xd9869f, '#f8cfa4', { freckles: true }))];
const pegs = town.map(tc => { const p = M(box(0.09, 0.26, 0.09), flat(0xc99a5a), { ol: 0.018, p: [0, -0.02, 0.47], r: [0.15, 0, 0] }); tc.headG.add(p); return p; });
[albie, ...town].forEach(c => root.add(c.g));

// ---------- tools ----------
const wrench = new THREE.Group(); root.add(wrench);
{ const m = toon(0xaab2bf); M(box(0.07, 0.85, 0.05), m, { ol: 0.02, p: [0, 0, 0], to: wrench }); M(box(0.26, 0.16, 0.06), m, { ol: 0.02, p: [0, 0.48, 0], to: wrench }); M(box(0.1, 0.12, 0.07), flat(0x1b1522), { p: [0.02, 0.5, 0], to: wrench, cast: false }); }

// ---------- kitchen ----------
const kitchen = new THREE.Group(); root.add(kitchen);
const PIPE_X = 1.15, PIPE_Z = -1.35, PIPE_TOP = 1.72;
let pipeMesh = null; const pipeMat = toon(0x8f98a8);
class PipeCurve extends THREE.Curve { constructor(k, top) { super(); this.k = k; this.top = top; } getPoint(s) { const y = this.top * (1 - s); const win = Math.sin(Math.PI * cl((s - 0.12) / 0.76)); return V(this.k * 0.34 * Math.sin(Math.PI * 2 * cl((s - 0.12) / 0.76)) * win, y, 0); } }
function setPipe(parent, k, top = PIPE_TOP, x = PIPE_X, z = PIPE_Z, r = 0.085) {
  if (pipeMesh) { pipeMesh.parent.remove(pipeMesh); pipeMesh.geometry.dispose(); pipeMesh.userData.ol.geometry = null; }
  pipeMesh = M(new THREE.TubeGeometry(new PipeCurve(k, top), 40, r, 12), pipeMat, { ol: 0.022, p: [x, 0, z] }); parent.add(pipeMesh);
}
{
  M(box(9, 0.2, 7), toon(0xffffff, { map: TX.planks }), { p: [0, -0.1, 0.5], recv: true, to: kitchen, cast: false });
  M(new THREE.PlaneGeometry(9, 5.6), toon(0xffffff, { map: TX.plaster }), { p: [0, 2.8, -2.2], recv: true, to: kitchen, cast: false });
  // sink bench: stone basin on a timber frame, open underneath
  const wood = toon(0xffffff, { map: TX.planks });
  M(box(2.5, 0.16, 1.3), wood, { ol: 0.03, p: [PIPE_X, 1.8, PIPE_Z], to: kitchen });
  for (const [dx, dz] of [[-1.15, -0.5], [1.15, -0.5], [-1.15, 0.5], [1.15, 0.5]]) M(box(0.14, 1.75, 0.14), wood, { ol: 0.025, p: [PIPE_X + dx, 0.87, PIPE_Z + dz], to: kitchen });
  M(box(1.5, 0.42, 1.0), toon(0xb9b3a8), { ol: 0.035, p: [PIPE_X, 2.08, PIPE_Z], to: kitchen }); M(box(1.24, 0.1, 0.76), flat(0x4a6f8a), { p: [PIPE_X, 2.26, PIPE_Z], to: kitchen, cast: false });
  // hand pump
  M(cyl(0.09, 0.11, 0.9, 12), toon(0x3d5a4a), { ol: 0.025, p: [PIPE_X + 0.95, 2.32, PIPE_Z - 0.35], to: kitchen }); M(cyl(0.035, 0.035, 0.5, 8), toon(0x3d5a4a), { ol: 0.02, p: [PIPE_X + 0.72, 2.6, PIPE_Z - 0.35], r: [0, 0, 1.2], to: kitchen }); M(cyl(0.03, 0.03, 0.7, 8), flat(0x1b1522), { p: [PIPE_X + 1.2, 2.86, PIPE_Z - 0.35], r: [0, 0, -0.9], to: kitchen });
  // window, shelf, pots
  M(box(1.5, 1.7, 0.08), toon(0x4a2e1c), { ol: 0.03, p: [-2.1, 3.3, -2.15], to: kitchen }); M(box(1.3, 1.5, 0.1), flat(0xffc98a), { p: [-2.1, 3.3, -2.14], to: kitchen, cast: false }); M(box(0.07, 1.5, 0.12), toon(0x4a2e1c), { p: [-2.1, 3.3, -2.12], to: kitchen, cast: false }); M(box(1.3, 0.07, 0.12), toon(0x4a2e1c), { p: [-2.1, 3.3, -2.12], to: kitchen, cast: false });
  M(box(2.4, 0.1, 0.45), wood, { ol: 0.025, p: [PIPE_X, 3.75, -1.95], to: kitchen });
  [[-0.8, 0x3f8f8a, 0.2], [-0.25, 0xc98a2a, 0.26], [0.35, 0xb0567a, 0.18], [0.85, 0x6a8f3f, 0.22]].forEach(([dx, col, r]) => { M(sph(r, 16, 12), toon(col), { ol: 0.025, p: [PIPE_X + dx, 3.8 + r, -1.95], s: [1, 1.15, 1], to: kitchen }); M(cyl(r * 0.5, r * 0.6, 0.12, 12), toon(col), { ol: 0.02, p: [PIPE_X + dx, 3.86 + r * 2.1, -1.95], to: kitchen }); });
  M(cyl(0.34, 0.26, 0.5, 16), toon(0x7a5232), { ol: 0.03, p: [-1.0, 0.25, -1.4], to: kitchen });  // bucket
  M(box(0.5, 0.22, 0.32), toon(0x7a4a2c), { ol: 0.025, p: [-0.2, 0.11, -0.2], r: [0, 0.4, 0], to: kitchen }); // toolbox
  const kl = new THREE.PointLight(0xffc98a, 10, 9, 1.5); kl.position.set(-1.6, 3.2, -0.8); kitchen.add(kl);
  const kl2 = new THREE.PointLight(0xffe2b0, 5, 6, 1.6); kl2.position.set(1.4, 0.9, 0.9); kitchen.add(kl2);
}

// ---------- street ----------
const street = new THREE.Group(); root.add(street);
{
  M(box(9, 0.2, 60), toon(0xffffff, { map: TX.cobble }), { p: [0, -0.1, -18], recv: true, to: street, cast: false });
  const roofM = toon(0x8a3b2c), cols = ['#ead9b4', '#e3c9a0', '#efe2c4', '#dcc59a'];
  for (let i = 0; i < 7; i++) for (const s of [-1, 1]) {
    const h = new THREE.Group(), w = 4.4, ht = 5.2 + ((i * 7 + (s > 0 ? 3 : 0)) % 3) * 0.7, z = 4 - i * 4.7; h.position.set(s * 6.3, 0, z); street.add(h);
    const tex = houseTex(11 + i * 3 + (s > 0 ? 50 : 0), cols[(i + (s > 0 ? 1 : 0)) % 4]);
    const mats = [toon(0xffffff, { map: tex }), toon(0xffffff, { map: tex }), roofM, roofM, toon(0xffffff, { map: tex }), toon(0xffffff, { map: tex })];
    M(box(w, ht, 4.4), mats, { ol: 0.04, p: [0, ht / 2, 0], to: h });
    const tri = new THREE.Shape(); tri.moveTo(-2.5, 0); tri.lineTo(2.5, 0); tri.lineTo(0, 2.3); tri.closePath();
    const roof = M(new THREE.ExtrudeGeometry(tri, { depth: 4.8, bevelEnabled: false }), roofM, { ol: 0.04, to: h }); roof.rotation.y = Math.PI / 2; roof.position.set(-2.4, ht, 0); roof.rotation.y = 0; roof.position.set(0, ht, -2.4);
    M(box(0.6, 1.6, 0.6), toon(0x6b4636), { ol: 0.03, p: [s * 1.2, ht + 1.6, -0.6], to: h });
    if (i % 2 === 0) { M(cyl(0.03, 0.03, 0.9, 6), flat(0x1b1522), { p: [-s * 2.5, 3.6, 1.2], r: [0, 0, Math.PI / 2], to: h }); const lan = M(box(0.3, 0.4, 0.3), flat(0xffd27a), { ol: 0.02, p: [-s * 2.9, 3.35, 1.2], to: h, cast: false }); }
  }
  M(new THREE.PlaneGeometry(60, 30), flat(0xf2a36a), { p: [0, 10, -36], to: street, cast: false });
  M(sph(3.2, 24, 16), flat(0xffe2a0), { p: [1.5, 5.5, -35.5], to: street, cast: false });
}

// ---------- cutaway (house -> earth -> sewer) ----------
const cut = new THREE.Group(); root.add(cut);
const stink = [];
{
  M(new THREE.PlaneGeometry(14, 24), flat(0x2b2aa8), { p: [0, -4, -3], to: cut, cast: false });
  M(box(5.2, 0.24, 2.2), toon(0xffffff, { map: TX.planks }), { ol: 0.03, p: [0, 0, 0], to: cut });
  M(box(1.6, 0.16, 1.1), toon(0xffffff, { map: TX.planks }), { ol: 0.03, p: [0, 1.5, 0], to: cut }); for (const dx of [-0.7, 0.7]) M(box(0.12, 1.4, 0.12), toon(0x7a5232), { ol: 0.02, p: [dx, 0.75, 0.4], to: cut });
  M(box(1.2, 0.36, 0.8), toon(0xb9b3a8), { ol: 0.03, p: [0, 1.74, 0], to: cut }); M(box(0.96, 0.08, 0.56), flat(0x4a6f8a), { p: [0, 1.9, 0], to: cut, cast: false });
  M(box(5.2, 6.2, 1.8), toon(0xffffff, { map: TX.earth }), { ol: 0.03, p: [0, -3.22, -0.2], to: cut });
  // sewer tunnel
  M(box(5.2, 2.4, 1.8), toon(0xffffff, { map: TX.brick }), { ol: 0.03, p: [0, -7.5, -0.2], to: cut });
  const arch = new THREE.Shape(); arch.moveTo(-1.9, -0.9); arch.lineTo(-1.9, 0); arch.absarc(0, 0, 1.9, Math.PI, 0, true); arch.lineTo(1.9, -0.9); arch.closePath();
  M(new THREE.ShapeGeometry(arch), flat(0x1a1420), { p: [0, -7.55, 0.72], s: [1, 0.55, 1], to: cut, cast: false });
  M(box(3.8, 0.5, 0.05), flat(0x6fae3a), { p: [0, -8.2, 0.74], to: cut, cast: false });
  const sm = flat(0x8fd04a, { transparent: true, opacity: 0.85 }); for (let i = 0; i < 14; i++) { const s = M(sph(0.16, 12, 8), sm, { cast: false }); cut.add(s); stink.push(s); }
}
const cutPipe = M(cyl(0.11, 0.11, 9.0, 14), toon(0x8f98a8), { ol: 0.025, p: [0, -3.0, 0.78] }); cut.add(cutPipe);

// ---------- extra cast & props ----------
const boss = makeChar2({ skin: '#f3c79c', stache: true, leg: 0x2a2530, shoe: 0x1b1522,
  body: (g, w, h) => { g.fillStyle = '#f3efe6'; g.fillRect(0, 0, w, h); g.fillStyle = '#6a2f6b'; g.fillRect(w * 0.1, 0, w * 0.8, h * 0.58); g.fillStyle = '#f3efe6'; g.beginPath(); g.moveTo(w * 0.43, 0); g.lineTo(w * 0.5, h * 0.26); g.lineTo(w * 0.57, 0); g.fill(); g.fillStyle = '#ffd34d'; for (let i = 0; i < 3; i++) { g.beginPath(); g.arc(w * 0.5, h * (0.32 + i * 0.09), 8, 0, 7); g.fill(); } g.strokeStyle = '#ffd34d'; g.lineWidth = 5; g.beginPath(); g.moveTo(w * 0.5, h * 0.36); g.quadraticCurveTo(w * 0.58, h * 0.5, w * 0.64, h * 0.4); g.stroke(); g.fillStyle = '#2a2530'; g.fillRect(0, h * 0.58, w, h * 0.42); },
  hat: hg => { const m = flat(0x2a2530); M(sph(0.37, 32, 16, 0, 6.3, 0, Math.PI / 2), m, { ol: 0.035, p: [0, 0.3, 0], s: [1, 1.1, 1], to: hg }); M(cyl(0.58, 0.58, 0.05, 32), m, { ol: 0.03, p: [0, 0.3, 0], to: hg }); M(cyl(0.375, 0.375, 0.09, 32), flat(0xb3272d), { p: [0, 0.37, 0], to: hg, cast: false }); } });
root.add(boss.g);
const bossPeg = M(box(0.09, 0.26, 0.09), flat(0xc99a5a), { ol: 0.018, p: [0, -0.02, 0.47], r: [0.15, 0, 0] }); boss.headG.add(bossPeg);
const table = new THREE.Group(); kitchen.add(table); table.position.set(-1.7, 0, 0.2);
{ const wood = toon(0xffffff, { map: TX.planks }); M(cyl(0.8, 0.8, 0.1, 28), wood, { ol: 0.03, p: [0, 1.3, 0], to: table }); M(cyl(0.09, 0.14, 1.3, 12), toon(0x7a5232), { ol: 0.02, p: [0, 0.65, 0], to: table }); M(cyl(0.42, 0.36, 0.04, 24), toon(0xf3efe6), { ol: 0.02, p: [0, 1.38, 0], to: table }); }
const fish = new THREE.Group(); root.add(fish);
{ const m = flat(0x9fb6c9); M(sph(0.2, 20, 14), m, { ol: 0.025, s: [1.7, 0.75, 0.5], to: fish }); M(new THREE.ConeGeometry(0.16, 0.24, 4), m, { ol: 0.02, p: [-0.42, 0, 0], r: [0, 0, -Math.PI / 2], s: [1, 1, 0.4], to: fish }); M(sph(0.035), flat(0x1b1522), { p: [0.2, 0.04, 0.09], to: fish, cast: false }); for (const s of [-1, 1]) M(box(0.07, 0.012, 0.012), flat(0x1b1522), { p: [0.2, 0.04, 0.1], r: [0, 0, s * 0.8], to: fish, cast: false }); }
const cat = new THREE.Group(); root.add(cat);
{ const m = flat(0xe8943a), d = flat(0xc9742a); M(sph(0.36, 24, 16), m, { ol: 0.035, p: [0, 0.34, 0], s: [0.9, 1, 0.85], to: cat });
  const ct = ctex(512, 256, g => { g.fillStyle = '#e8943a'; g.fillRect(0, 0, 512, 256); g.fillStyle = '#c9742a'; for (const x of [216, 256, 296]) g.fillRect(x - 6, 0, 12, 60); g.strokeStyle = '#1b1522'; g.lineWidth = 9; g.lineCap = 'round'; for (const s of [-1, 1]) { g.beginPath(); g.moveTo(256 + s * 22, 112); g.lineTo(256 + s * 62, 104); g.stroke(); g.fillStyle = '#1b1522'; g.beginPath(); g.arc(256 + s * 42, 122, 8, 0, 7); g.fill(); } g.beginPath(); g.moveTo(240, 160); g.lineTo(256, 152); g.lineTo(272, 160); g.stroke(); g.fillStyle = '#ff9aa8'; g.beginPath(); g.arc(256, 144, 7, 0, 7); g.fill(); });
  cat.userData.head = new THREE.Group(); cat.userData.head.position.set(0, 0.86, 0.06); cat.add(cat.userData.head);
  M(sph(0.28, 28, 18), flat(0xffffff, { map: ct }), { ol: 0.035, r: [0, -Math.PI / 2, 0], to: cat.userData.head });
  cat.userData.ears = [-1, 1].map(s => M(new THREE.ConeGeometry(0.1, 0.2, 4), d, { ol: 0.025, p: [s * 0.17, 0.26, 0], to: cat.userData.head }));
  M(new THREE.TorusGeometry(0.3, 0.05, 8, 20, Math.PI * 1.1), m, { ol: 0.025, p: [0.38, 0.3, -0.1], r: [0, 0.4, 1.2], to: cat }); }
const loaf = new THREE.Group(); root.add(loaf);
{ M(sph(0.22, 20, 14), flat(0xc98a3a), { ol: 0.03, s: [1.9, 0.8, 0.9], to: loaf }); for (const x of [-0.18, 0, 0.18]) M(box(0.03, 0.02, 0.26), flat(0x7a4a1c), { p: [x, 0.165, 0], r: [0, 0.5, 0], to: loaf, cast: false }); }

// ---------- shop front with hanging sign ----------
const shop = new THREE.Group(); root.add(shop);
const FT = []; function ftex(w, h, d) { const t = ctex(w, h, d); t.userData.draw = d; FT.push(t); return t; }
window.afterFonts = () => FT.forEach(t => { t.userData.draw(t.userData.g, t.userData.c.width, t.userData.c.height); t.needsUpdate = true; });
function signTex(a, b, col) { return ftex(512, 220, g => { g.fillStyle = '#efe2c4'; g.fillRect(0, 0, 512, 220); g.strokeStyle = '#3d2718'; g.lineWidth = 14; g.strokeRect(7, 7, 498, 206); g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = col; g.font = '86px Pop'; g.fillText(a, 256, 78); g.fillStyle = '#1b1522'; g.font = '58px Pop'; g.fillText(b, 256, 158); }); }
const signA = signTex('STRAIGHT', 'PIPES ONLY', '#b3272d'), signB = signTex('BENT', 'PIPES ONLY', '#2f8f5b');
const signG = new THREE.Group(); shop.add(signG); const signM = toon(0xffffff, { map: signA });
{
  M(box(11, 0.2, 9), toon(0xffffff, { map: TX.cobble }), { p: [0, -0.1, 2], recv: true, to: shop, cast: false });
  const upper = TX.plaster.clone(); upper.needsUpdate = true;
  M(new THREE.PlaneGeometry(11, 4.2), toon(0xffffff, { map: upper }), { p: [0, 5.5, -1.4], to: shop, cast: false, recv: true });
  const bt = TX.brick.clone(); bt.needsUpdate = true; bt.wrapS = bt.wrapT = THREE.RepeatWrapping; bt.repeat.set(6, 2);
  M(new THREE.PlaneGeometry(11, 3.4), toon(0xffffff, { map: bt }), { p: [0, 1.7, -1.4], to: shop, cast: false, recv: true });
  M(box(3.4, 2.2, 0.16), toon(0x3d2718), { ol: 0.03, p: [-1.9, 1.9, -1.34], to: shop }); M(box(3.1, 1.9, 0.18), flat(0x2a3552), { p: [-1.9, 1.9, -1.33], to: shop, cast: false });
  for (let i = 0; i < 5; i++) M(cyl(0.09, 0.09, 1.3 + (i % 2) * 0.3, 10), toon(0x8f98a8), { ol: 0.02, p: [-3.0 + i * 0.55, 1.6 + (i % 2) * 0.15, -1.2], to: shop });
  M(box(1.5, 3.0, 0.14), toon(0x6b4326), { ol: 0.03, p: [2.4, 1.5, -1.34], to: shop }); M(sph(0.07), toon(0xd9a53a), { p: [2.9, 1.5, -1.24], to: shop });
  const nb = ftex(1024, 128, g => { g.fillStyle = '#1f3a2f'; g.fillRect(0, 0, 1024, 128); g.fillStyle = '#ffd34d'; g.font = '80px Pop'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('GRIMBLE & SON · PIPES', 512, 68); }); shop.userData.nb = nb;
  M(box(7.6, 0.75, 0.12), toon(0xffffff, { map: nb }), { ol: 0.03, p: [0, 3.75, -1.3], to: shop });
  M(box(0.16, 0.16, 2.4), toon(0x3d2718), { ol: 0.025, p: [0.2, 6.6, -0.2], to: shop });
  signG.position.set(0.2, 6.52, 0.7); M(box(2.7, 1.16, 0.09), signM, { ol: 0.03, p: [0, -1.25, 0], to: signG }); for (const s of [-1, 1]) M(cyl(0.02, 0.02, 0.7, 6), flat(0x1b1522), { p: [s * 1.05, -0.35, 0], to: signG, cast: false });
}

// ---------- river ----------
const river = new THREE.Group(); root.add(river); const riverBubbles = [];
{
  M(new THREE.PlaneGeometry(60, 40), toon(0x7d8f3c), { p: [0, 0, -8], r: [-Math.PI / 2, 0, 0], to: river, cast: false, recv: true });
  M(box(60, 1.6, 2), toon(0xffffff, { map: TX.brick }), { ol: 0.03, p: [0, 0.2, 4.4], to: river });
  M(new THREE.PlaneGeometry(80, 40), flat(0xf58a4a), { p: [0, 14, -30], to: river, cast: false }); M(sph(5.5, 28, 18), flat(0xfff0b0), { p: [-2, 9.5, -29.5], to: river, cast: false });
  for (let i = 0; i < 14; i++) { const h = 3 + ((i * 7) % 5); M(box(3.2, h, 2), flat(0x5a2f3a), { p: [-22 + i * 3.4, h / 2, -24], to: river, cast: false }); M(new THREE.ConeGeometry(2.3, 1.8, 4), flat(0x5a2f3a), { p: [-22 + i * 3.4, h + 0.9, -24], r: [0, Math.PI / 4, 0], to: river, cast: false }); }
  M(box(40, 0.8, 1.6), flat(0x3d2030), { p: [0, 3.2, -16], to: river, cast: false }); for (let i = 0; i < 7; i++) M(box(1.0, 3.2, 1.6), flat(0x3d2030), { p: [-15 + i * 5, 1.6, -16], to: river, cast: false });
  for (let i = 0; i < 18; i++) { const b = M(sph(0.3, 14, 10), toon(0xa6b85a), { ol: 0.03, cast: false }); river.add(b); riverBubbles.push(b); }
}

// ---------- explainer pipes (cross-section on blue) ----------
const exp = new THREE.Group(); root.add(exp);
class Sub extends THREE.Curve { constructor(c, a, b) { super(); this.c = c; this.a = a; this.b = b; } getPoint(t) { return this.c.getPoint(this.a + (this.b - this.a) * t); } }
const trapCurve = new THREE.CatmullRomCurve3([V(-1.5, 7, 0), V(-1.5, 4.6, 0), V(-1.5, 2.0, 0), V(-0.75, 1.05, 0), V(0, 2.0, 0), V(0, 3.2, 0), V(0.75, 4.0, 0), V(1.5, 3.2, 0), V(1.5, 0.5, 0), V(1.5, -3, 0)], false, 'catmullrom', 0.5);
function findU(y, lo, hi) { let best = lo, d = 1e9; for (let i = 0; i <= 400; i++) { const u = lo + (hi - lo) * i / 400, e = Math.abs(trapCurve.getPoint(u).y - y); if (e < d) { d = e; best = u; } } return best; }
const U_BOT = findU(1.05, 0.25, 0.42), WL = 3.25, U_L = findU(WL, 0.1, U_BOT), U_R = findU(WL, U_BOT, 0.6);
const expStraight = new THREE.Group(), expTrap = new THREE.Group(); exp.add(expStraight); exp.add(expTrap); const waterHalves = []; const blobs = [];
{
  M(new THREE.PlaneGeometry(16, 26), flat(0x2b2aa8), { p: [0, 2, -3], to: exp, cast: false });
  const wall = toon(0x8f98a8), inner = flat(0x3d4460);
  const sg = new THREE.TubeGeometry(new THREE.LineCurve3(V(0, 8, 0), V(0, -4, 0)), 8, 0.62, 20); M(sg, wall, { ol: 0.045, s: [1, 1, 0.14], to: expStraight }); M(new THREE.TubeGeometry(new THREE.LineCurve3(V(0, 8, 0), V(0, -4, 0)), 8, 0.47, 20), inner, { p: [0, 0, 0.05], s: [1, 1, 0.14], to: expStraight, cast: false });
  M(new THREE.TubeGeometry(trapCurve, 160, 0.62, 20), wall, { ol: 0.045, s: [1, 1, 0.14], to: expTrap }); M(new THREE.TubeGeometry(trapCurve, 160, 0.47, 20), inner, { p: [0, 0, 0.05], s: [1, 1, 0.14], to: expTrap, cast: false });
  for (const end of [U_L, U_R]) { const w = M(new THREE.TubeGeometry(new Sub(trapCurve, U_BOT, end), 60, 0.47, 20), flat(0x4fb4ff), { p: [0, 0, 0.1], s: [1, 1, 0.14], to: expTrap, cast: false }); waterHalves.push(w); }
  for (let i = 0; i < 9; i++) { const b = M(sph(0.24, 16, 12), flat(0x8fd04a), { ol: 0.03, cast: false }); exp.add(b); blobs.push(b); }
}
const SETS = [kitchen, street, cut, shop, river, exp, wrench, fish, cat, loaf, albie.g, boss.g, ...town.map(c => c.g)];

// ---------- helpers ----------
const S = i => Ls[i].s, CUT = i => i === 0 ? 0 : Ls[i].s - 0.1;
function wf(i, str, nth = 1) { let n = 0; for (const w of Ls[i].words) if (w.w.toLowerCase().replace(/[^a-z0-9']/g, '').startsWith(str)) { if (++n === nth) return w.s; } console.log('word not found', i, str); return Ls[i].s; }
function setCam(p, l, fov, t, shake = 0, roll = 0) { cam.fov = fov; cam.position.set(p[0] + 0.02 * Math.sin(t * 1.3) + shake * Math.sin(t * 61), p[1] + 0.015 * Math.sin(t * 1.7 + 1) + shake * Math.sin(t * 53), p[2]); cam.lookAt(l[0], l[1], l[2]); cam.rotateZ(roll); cam.updateProjectionMatrix(); }
const bg = c => { root.background = new THREE.Color(c); };
const SC = 0.86;
function show(c, x, z, ry = 0, tint = 0xffffff) { if (c.g.parent !== root) root.add(c.g); c.g.visible = true; c.g.position.set(x, 0, z); c.g.rotation.set(0, ry, 0); c.g.scale.setScalar(SC); c.tint(tint); c.hatG.position.set(0, 0, 0); c.hatG.rotation.set(0, 0, 0); c.g.updateMatrixWorld(true); }
function toLocal(c, w) { const p = w.clone(); c.up.worldToLocal(p); return [p.x, p.y, p.z]; }
const STINKM = flat(0x8fd04a), WATERM = flat(0x4fb4ff);
function kitchenLook() { bg(0x3a2a22); light(0.85, 1.2, [-3, 6, 6], 0xffe2bd, 0x5a4034); }
function shopLook() { shop.visible = true; bg(0xf2a36a); light(0.95, 1.5, [4, 9, 7], 0xffd9a8, 0x6a5560); }
function hideAll() { SETS.forEach(g => g.visible = false); pegs.forEach(p => p.visible = false); bossPeg.visible = false; table.visible = false; blobs.forEach(b => b.visible = false); }
function wisps(t, pts, col = '#8fd04a') { ctx.save(); ctx.lineCap = 'round'; pts.forEach(([x, y], i) => { for (const [lw, c] of [[20, INK], [11, col]]) { ctx.strokeStyle = c; ctx.lineWidth = lw; ctx.beginPath(); for (let k = 0; k <= 12; k++) { const yy = y - k * 16 - ((t * 60 + i * 37) % 60), xx = x + Math.sin(k * 0.7 + t * 4 + i) * 22; k ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); } ctx.stroke(); } }); ctx.restore(); }

// ---------- timeline ----------
function update(t) {
  hideAll(); overlay = () => { };
  let li = 0; for (let i = 0; i < Ls.length; i++) if (t >= CUT(i)) li = i;
  const s0 = CUT(li), s1 = li + 1 < Ls.length ? CUT(li + 1) : DUR, k = (t - s0) / (s1 - s0);
  const sub = (a, b) => cl((t - a) / (b - a));
  LOOK.grade = ['#ffc98a', 0.12]; LOOK.bloom = 0.14;

  if (li === 0) {
    const tb = wf(0, 'and') - 0.08;
    if (t < tb) { // ===== hook: Albie bends the pipe under the sink =====
      kitchen.visible = true; bg(0x3a2a22); light(0.85, 1.2, [-3, 6, 6], 0xffe2bd, 0x5a4034);
      const t0 = wf(0, 'bent') - 0.25, kb = ss(t0, t0 + 0.9, t), wob = t > t0 + 0.9 ? Math.exp(-(t - t0 - 0.9) * 7) * Math.sin((t - t0 - 0.9) * 30) * 0.08 : 0;
      setPipe(kitchen, kb + wob);
      show(albie, PIPE_X - 1.0, PIPE_Z + 0.75, 0.5); albie.face(kb > 0.95 ? 'happy' : 'think');
      const grip = V(PIPE_X - 0.02 + 0.3 * Math.sin(Math.PI * 2 * 0.3) * kb, 1.25, PIPE_Z + 0.1), g2 = V(PIPE_X, 0.8, PIPE_Z + 0.1);
      const strain = kb < 0.95 ? 0.02 * Math.sin(t * 40) : 0;
      albie.pose({ pitch: 0.16, hx: 0.12, hy: 0.25, bob: -0.1 + strain, rh: toLocal(albie, grip), lh: toLocal(albie, g2) });
      albie.g.updateMatrixWorld(true); albie.pose({ pitch: 0.16, hx: 0.12, hy: 0.25, bob: -0.1 + strain, rh: toLocal(albie, grip), lh: toLocal(albie, g2) });
      wrench.visible = true; wrench.position.copy(grip).add(V(-0.3, 0.12, 0.08)); wrench.rotation.set(0, 0.2, 1.2 - kb * 0.9);
      const kk = sub(0, tb); setCam([lerp(0.0, 0.4, kk), lerp(1.3, 1.5, kk), lerp(5.6, 4.6, ss(0, 1, kk))], [PIPE_X - 0.45, 1.55, PIPE_Z], 44, t, kb > 0.02 && kb < 0.98 ? 0.006 : 0, -0.05);
      overlay = () => { popText('WORST PLUMBER', W / 2, 250, 112, '#fff', t, 0.3, t0 - 0.02); popText('IN LONDON', W / 2, 385, 112, '#ffd23e', t, 0.75, t0 - 0.02); burst('CREEEAK!', 760, 1090, 180, t, t0 + 0.05, tb - 0.03, 0.08); };
    } else { // ===== the city's noses =====
      street.visible = true; bg(0xf2a36a); light(0.95, 1.5, [5, 9, 6], 0xffd9a8, 0x6a5560);
      town.forEach((c, i) => { show(c, -1.05 + i * 1.05, 1.5 + (i % 2) * 0.6, (1 - i) * 0.25); c.face('sad'); pegs[i].visible = true; c.pose({ lh: [-0.44, 1.42, 0.05], rh: i === 1 ? [0.2, 2.45, 0.42] : [0.44, 1.42, 0.05], hz: 0.08 * Math.sin(t * 3 + i), bob: 0.02 * Math.sin(t * 4 + i) }); });
      const kk = sub(tb, s1); setCam([lerp(0.4, 0.1, kk), lerp(1.6, 1.9, kk), lerp(9.6, 8.6, kk)], [0, 1.9, 1.5], 42, t, 0, 0.04);
      overlay = () => { wisps(t, [[110, 1560], [400, 1680], [700, 1600], [960, 1700], [90, 760], [990, 800]]); popText("THE CITY'S", W / 2, 250, 124, '#fff', t, wf(0, 'city') - 0.25, s1 - 0.02); popText('NOSES', W / 2, 400, 160, '#ffd23e', t, wf(0, 'noses') - 0.05, s1 - 0.02); };
    }
  }
  else if (li === 1) {
    const tb = wf(1, 'where') - 0.1;
    if (t < tb) { // ===== old London street, Albie walks to work =====
      street.visible = true; bg(0xf2a36a); light(0.95, 1.5, [5, 9, 6], 0xffd9a8, 0x6a5560);
      const u = sub(s0, tb), ph = t * 8; show(albie, lerp(-0.4, 0.2, u), lerp(-6, 0.5, u), 0.05); albie.face('happy');
      const P = { ...albie.walk(ph), lh: [-0.44, 1.42 + 0.06 * Math.sin(ph), 0.05 + 0.2 * Math.sin(ph)], rh: [0.36, 2.05, 0.25] }; albie.pose(P);
      albie.g.updateMatrixWorld(true); const hp = V(0.36, 2.05, 0.25); albie.up.localToWorld(hp); wrench.visible = true; wrench.position.copy(hp).add(V(0.02, 0.32, -0.12)); wrench.rotation.set(-0.5, 0, -0.25);
      show(town[0], -2.6, -3.5, 0.9); town[0].face('neutral'); town[0].pose({}); show(town[2], 2.7, -8, -0.8); town[2].face('happy'); town[2].pose({ rh: [0.5, 2.3 + 0.08 * Math.sin(t * 9), 0.2] });
      setCam([lerp(1.6, 0.9, u), lerp(4.6, 2.6, ss(0, 1, u)), lerp(11, 6.6, ss(0, 1, u))], [0, lerp(2.6, 2.1, u), lerp(-8, -1, u)], 46, t, 0, -0.03);
      overlay = () => popText('OLD LONDON', W / 2, 300, 96, '#ffd23e', t, wf(1, 'old') - 0.08, tb - 0.02);
    } else { // ===== cutaway: straight pipe down to the sewer =====
      cut.visible = true; bg(0x2b2aa8); light(1.15, 1.4, [3, 5, 8], 0xffffff, 0x5a5ac0); LOOK.grade = null;
      const u = sub(tb, s1), cy = lerp(1.2, -6.6, ss(0.05, 0.8, u));
      stink.forEach((s, i) => { const p = ((t * 0.35 + i / stink.length) % 1); s.visible = false; });
      setCam([lerp(1.2, 0.6, u), cy + 1.0, 9.5], [0, cy, 0], 44, t);
      overlay = () => { popText('STRAIGHT', W / 2, 250, 130, '#fff', t, wf(1, 'straight') - 0.05, s1 - 0.02); popText('DOWN', W / 2, 395, 150, '#ff9a3a', t, wf(1, 'down') - 0.05, s1 - 0.02);
        const a0 = wf(1, 'down') - 0.05; if (t > a0) { const kk = back((t - a0) / 0.25); ctx.save(); ctx.translate(820, 1060); ctx.scale(kk, kk); for (const [lw, c] of [[44, INK], [24, '#ff9a3a']]) { ctx.strokeStyle = c; ctx.fillStyle = c; ctx.lineWidth = lw; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.beginPath(); ctx.moveTo(0, -170); ctx.lineTo(0, 110); ctx.stroke(); ctx.beginPath(); ctx.moveTo(-70, 70); ctx.lineTo(0, 170); ctx.lineTo(70, 70); ctx.closePath(); ctx.fill(); ctx.stroke(); } ctx.restore(); } };
    }
  }
  else if (li === 2) { // ===== straight lets the sewer breathe back up (first seconds only, for the preview) =====
    cut.visible = true; bg(0x2b2aa8); light(1.15, 1.4, [3, 5, 8], 0xffffff, 0x5a5ac0); LOOK.grade = null;
    const tu = wf(2, 'and') - 0.1, u = sub(tu, s1), cy = t < tu ? -6.6 : lerp(-6.6, 1.0, ss(0, 0.85, u));
    stink.forEach((s, i) => { const p = ((t * 0.45 + i / stink.length) % 1); s.visible = t > tu - 0.4; s.position.set(0.1 * Math.sin(i * 2 + t * 5), -8.0 + p * 10.4, 0.98); s.scale.setScalar(0.7 + 0.6 * Math.sin(p * Math.PI)); });
    setCam([0.6, cy + 1.0, 9.5], [0, cy, 0], 44, t);
    overlay = () => { popText('CHEAP', W / 2, 300, 150, '#fff', t, wf(2, 'cheap') - 0.05, wf(2, 'straight', 2) - 0.05); popText('FAST', W / 2, 300, 160, '#ffd23e', t, wf(2, 'fast') - 0.05, tu - 0.02); popText('STINK', W / 2, 300, 170, '#8fd04a', t, wf(2, 'breathe') - 0.05, s1 - 0.02); };
  }
  else if (li === 3) {
    kitchen.visible = true; table.visible = true; kitchenLook(); setPipe(kitchen, 0);
    const tp = wf(3, 'people') - 0.08, tc = wf(3, 'cat') - 0.5, w = town[2];
    fish.visible = true; fish.scale.setScalar(1); fish.position.set(-1.7, 1.47, 0.2); fish.rotation.set(0, 0.3, 0);
    cat.visible = true; cat.position.set(0.1, 0, 0.7); cat.rotation.set(0, -0.4, 0); cat.userData.ears.forEach(e => e.rotation.z = 0); cat.userData.head.rotation.y = 0;
    if (t < tp) { show(w, -0.5, -0.3, 0.25); w.face('sad'); w.pose({ rh: [0.12, 2.5, 0.44], lh: [-0.44, 1.42, 0.05], hz: 0.08 * Math.sin(t * 5), lean: -0.06 });
      setCam([lerp(-0.6, -0.2, k * 2.5), 1.9, lerp(6.4, 5.6, k * 2.5)], [0.3, 1.9, -1], 44, t, 0, 0.04);
      overlay = () => { const [x, y] = proj(V(PIPE_X, 2.4, PIPE_Z)); wisps(t, [[x - 40, y], [x + 50, y - 40], [x, y - 140]]); popText('SMELLS LIKE', W / 2, 250, 112, '#fff', t, wf(3, 'smelled') - 0.05, tp - 0.02); popText('THE RIVER', W / 2, 385, 124, '#8fd04a', t, wf(3, 'river') - 0.05, tp - 0.02); };
    } else if (t < tc) { show(w, -0.55, 0.35, -0.75); w.face('angry'); w.pose({ rh: [0.55, 1.75, 0.5], lh: [-0.44, 1.42, 0.05], pitch: 0.1, bob: 0.02 * Math.sin(t * 14) });
      setCam([-1.0, 2.3, lerp(4.6, 4.1, sub(tp, tc))], [-1.2, 1.75, 0.2], 42, t, 0, -0.05);
      overlay = () => burst('THE FISH!', 760, 430, 170, t, wf(3, 'fish') - 0.08, tc - 0.03, 0.1);
    } else { show(w, -1.0, 0.9, 0.9); w.face('angry'); w.pose({ rh: [0.5, 1.3, 0.55], lh: [-0.44, 1.42, 0.05], pitch: 0.2 });
      const v = t - tc; cat.userData.ears.forEach((e, i) => e.rotation.z = (i ? -1 : 1) * 0.9 * ss(0.15, 0.4, v)); cat.userData.head.rotation.y = -0.6 * ss(0.5, 0.9, v);
      setCam([0.5, 1.0, lerp(3.8, 3.3, sub(tc, s1))], [-0.1, 0.8, 0.7], 42, t, 0, 0.05);
      overlay = () => burst('THE CAT!', 780, 430, 170, t, wf(3, 'cat') - 0.08, s1 - 0.03, 0.1);
    }
  }
  else if (li === 4) {
    kitchen.visible = true; kitchenLook(); setPipe(kitchen, 1 + 0.06 * Math.sin(t * 9)); const ts = wf(4, 'like') - 0.08;
    show(albie, PIPE_X - 1.15, PIPE_Z + 0.9, 0.35); albie.face('happy'); albie.pose({ rh: [0.6, 1.7 + 0.04 * Math.sin(t * 6), 0.35], lh: [-0.44, 1.42, 0.05], hy: 0.3, bob: 0.03 * Math.abs(Math.sin(t * 5)) });
    if (t < ts) setCam([lerp(-0.2, 0.2, k), 1.5, lerp(5.6, 4.8, k)], [PIPE_X - 0.5, 1.55, PIPE_Z], 44, t, 0, -0.04);
    else setCam([PIPE_X + 0.4, 1.05, lerp(2.9, 2.5, sub(ts, s1))], [PIPE_X + 0.1, 0.95, PIPE_Z], 44, t, 0, 0.06);
    overlay = () => { popText('A WIGGLE', W / 2, 300, 140, '#ffd23e', t, wf(4, 'wiggle') - 0.05, ts - 0.02); if (t > ts) { const [x, y] = proj(V(PIPE_X + 0.35, 1.3, PIPE_Z)); for (let i = 0; i < 3; i++) popText('Z', x + 60 + i * 80, y - 80 - i * 110 - 15 * Math.sin(t * 3 + i), 80 + i * 30, '#fff', t, ts + 0.15 + i * 0.2, s1); } };
  }
  else if (li === 5) {
    kitchen.visible = true; kitchenLook(); setPipe(kitchen, 1);
    const tq = wf(5, 'bent') - 0.3, td = wf(5, 'did') - 0.08, red = ss(s0 + 0.2, s0 + 1.1, t), tint = new THREE.Color(0xffffff).lerp(new THREE.Color(0xff6a52), red);
    if (t < tq) { show(boss, -0.4, 0.2, 0.1); boss.headM.color.copy(tint); boss.face('angry'); boss.pose({ lh: [-0.5, 1.5, 0.2], rh: [0.5, 1.5, 0.2], bob: 0.02 * Math.sin(t * 30) * red, hx: -0.05 });
      const hp = boss.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 0.3, hp.y + 0.05, hp.z + lerp(4.6, 3.6, sub(s0, tq))], [hp.x, hp.y - 0.2, hp.z], 40, t, 0.004 * red, -0.05);
      overlay = () => { popText('RED AS', W / 2, 250, 124, '#fff', t, wf(5, 'red') - 0.05, tq - 0.02); popText('A BRICK', W / 2, 395, 140, '#ff5a4a', t, wf(5, 'brick') - 0.05, tq - 0.02); if (red > 0.6) { const [x, y] = proj(hp); wisps(t, [[x - 250, y - 60], [x + 250, y - 60]], '#ffffff'); } };
    } else { show(boss, -0.5, 0.1, 0.55); boss.headM.color.copy(tint); boss.face('angry'); boss.pose({ rh: [0.7, 1.9, 0.5], lh: [-0.44, 1.42, 0.05], bob: 0.03 * Math.abs(Math.sin(t * 12)), pitch: 0.08 });
      show(albie, PIPE_X + 0.75, PIPE_Z + 1.5, -0.5); albie.face('happy'); albie.pose({ lh: [-0.6, 1.75, 0.1], rh: [0.6, 1.75, 0.1], hz: 0.1 });
      setCam([lerp(0.3, 0.6, sub(tq, s1)), 1.6, lerp(7.6, 7.0, sub(tq, s1))], [0.65, 1.7, -0.6], 44, t, 0, 0.04);
      overlay = () => { burst('A BENT PIPE?!', 540, 400, 200, t, tq + 0.05, td - 0.03, -0.06); popText('DID YOU', W / 2, 250, 130, '#fff', t, td, s1 - 0.02); popText('SIT ON IT?', W / 2, 395, 136, '#ffd23e', t, wf(5, 'sit') - 0.05, s1 - 0.02); };
    }
  }
  else if (li === 6) {
    shopLook(); signM.map = signA; const ta = wf(6, 'and') - 0.08;
    if (t < ta) { signG.visible = false; show(boss, -0.7, 1.2, 0.5); boss.headM.color.set(0xff8a72); boss.face('angry'); boss.pose({ rh: [0.75, 2.1, 0.3], lh: [-0.44, 1.42, 0.05] });
      const u = sub(s0 + 0.5, ta); show(albie, lerp(0.9, 3.2, u), 1.6, 1.2); albie.face('sad'); albie.pose({ ...albie.walk(t * 7, 0.2), hx: 0.3 });
      setCam([0.6, 1.8, lerp(9.6, 9.0, k)], [0.6, 2.2, 1], 44, t, 0, -0.04);
      overlay = () => burst('FIRED!', 540, 420, 200, t, wf(6, 'fired') - 0.08, ta - 0.03, -0.08);
    } else { signG.visible = true; const v = t - ta - 0.25, drop = v < 0 ? 1 : Math.exp(-v * 5) * Math.abs(Math.cos(v * 9)); signG.position.y = 6.52 + (v < 0 ? 4 : drop * 1.2); signG.rotation.z = v < 0 ? 0 : 0.25 * Math.exp(-v * 2.2) * Math.sin(v * 7);
      show(boss, -1.9, 1.3, 0.45); boss.face('happy'); boss.pose({ lh: [-0.44, 1.42, 0.05], rh: [0.5, 2.3, 0.2], hx: -0.4 });
      setCam([lerp(1.4, 1.0, sub(ta, s1)), lerp(2.4, 2.8, sub(ta, s1)), lerp(8.0, 7.0, sub(ta, s1))], [0.1, 4.4, 0], 44, t, 0, 0.05);
    }
  }
  else if (li === 7) {
    river.visible = true; bg(0xf58a4a); light(1.0, 1.6, [-3, 8, -6], 0xffc98a, 0x7a5a3a); LOOK.grade = ['#ff8a3a', 0.25]; LOOK.bloom = 0.3;
    riverBubbles.forEach((b, i) => { const p = ((t * 0.7 + i * 0.137) % 1), x = -5 + ((i * 37) % 100) / 10, z = -1 - ((i * 53) % 90) / 10; b.visible = true; b.position.set(x, -0.2 + p * 0.35, z); b.scale.setScalar(p < 0.85 ? 0.4 + p * 1.2 : Math.max(0.01, (1 - p) * 8)); });
    fish.visible = true; fish.position.set(1.2, 0.12 + 0.05 * Math.sin(t * 3), 1.0); fish.rotation.set(Math.PI, 0.4, 0.1 * Math.sin(t * 2)); fish.scale.setScalar(1.6);
    setCam([lerp(-0.8, 0.2, k), lerp(2.8, 2.4, k), lerp(9.5, 8.2, k)], [0, 1.8, -6], 46, t, 0, 0.03);
    overlay = () => { wisps(t, [[160, 1250], [420, 1180], [700, 1260], [930, 1200], [300, 1000], [820, 960]], '#ffffff'); popText('SO HOT', W / 2, 280, 170, '#ff9a3a', t, wf(7, 'hot') - 0.3, wf(7, 'river') - 0.05); popText('RIVER SOUP', W / 2, 280, 130, '#8fd04a', t, wf(7, 'river') - 0.03, s1 - 0.02); };
  }
  else if (li === 8) {
    const te = wf(8, 'even') - 0.08;
    if (t < te) { street.visible = true; bg(0xc9b06a); light(0.9, 1.3, [5, 9, 6], 0xe8e0a0, 0x5a6a40); LOOK.grade = ['#8fd04a', 0.3];
      town.forEach((c, i) => { show(c, -1.05 + i * 1.05, 1.2 + (i % 2) * 0.7, (1 - i) * 0.3); c.face('sad'); pegs[i].visible = true; c.pose({ lean: 0.12 * Math.sin(t * 3 + i * 2), hz: 0.1 * Math.sin(t * 3 + i), lh: [-0.5, 1.6 + 0.2 * Math.sin(t * 4 + i), 0.2], rh: [0.5, 1.6 + 0.2 * Math.cos(t * 4 + i), 0.2] }); });
      setCam([lerp(-0.5, 0.3, k), lerp(2.6, 2.0, k), lerp(10, 8.8, k)], [0, 1.9, 1.5], 44, t, 0, -0.04);
      overlay = () => { wisps(t, [[110, 1560], [400, 1680], [700, 1600], [960, 1700], [90, 760], [990, 800], [250, 1100], [850, 1150]]); popText('REEKED', W / 2, 300, 170, '#8fd04a', t, wf(8, 'reeked') - 0.08, te - 0.02); };
    } else { shopLook(); LOOK.grade = ['#8fd04a', 0.25]; signM.map = signA; signG.visible = true; signG.position.y = 6.52; signG.rotation.z = 0.05 * Math.sin(t * 2);
      show(boss, 0.2, 1.6, 0); boss.face('sad'); bossPeg.visible = true; boss.pose({ hz: 0.06 * Math.sin(t * 3), bob: -0.03 });
      const hp = boss.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 0.4, hp.y, hp.z + lerp(4.8, 4.0, sub(te, s1))], [hp.x, hp.y - 0.25, hp.z], 40, t, 0, 0.05);
      overlay = () => { const [x, y] = proj(hp); wisps(t, [[x - 320, y + 300], [x + 320, y + 250]]); popText('EVEN THE BOSS', W / 2, 280, 104, '#fff', t, te + 0.05, s1 - 0.02); };
    }
  }
  else if (li === 9) {
    street.visible = true; bg(0xf2a36a); light(1.05, 1.6, [5, 9, 6], 0xffe2b0, 0x6a5560); LOOK.grade = ['#ffc060', 0.2]; LOOK.bloom = 0.25; const ta = wf(9, 'albie') - 0.08;
    if (t < ta) { setCam([lerp(2.0, 0.8, k * 2), lerp(7, 4.2, ss(0, 1, k * 2)), lerp(13, 10, k * 2)], [0, 2.4, -6], 46, t, 0, 0.03);
      town.forEach((c, i) => { show(c, -2.2 + i * 2.2, -2 - i * 1.5, 0); c.face('happy'); c.pose(c.walk(t * 6 + i, 0.2)); });
      overlay = () => { popText('EXCEPT', W / 2, 250, 124, '#fff', t, s0 + 0.1, ta - 0.02); popText('ONE STREET', W / 2, 395, 130, '#ffd23e', t, wf(9, 'one') - 0.05, ta - 0.02); };
    } else { town.forEach((c, i) => { show(c, [-1.25, 1.25, 2.1][i], [1.3, 1.4, 0.2][i], [0.3, -0.3, -0.5][i]); c.face('happy'); c.pose({ hx: -0.25, bob: 0.04 * Math.abs(Math.sin(t * 5 + i)), rh: i === 0 ? [0.5, 2.4, 0.3] : [0.44, 1.42, 0.05] }); });
      const hp = V(0.5, 2.4, 0.3); town[0].g.updateMatrixWorld(true); town[0].up.localToWorld(hp); loaf.visible = true; loaf.position.copy(hp).add(V(0, 0.2, 0)); loaf.rotation.set(0, 0.3, 0.1);
      show(albie, 0, 1.9, 0); albie.face('happy'); albie.pose({ rh: [0.6, 2.5 + 0.1 * Math.sin(t * 10), 0.2], lh: [-0.44, 1.42, 0.05], bob: 0.03 * Math.abs(Math.sin(t * 5)) });
      setCam([lerp(0.3, 0, sub(ta, s1)), 1.9, lerp(9.0, 8.2, sub(ta, s1))], [0.1, 2.0, 1.5], 44, t, 0, -0.03);
      overlay = () => { const [x, y] = proj(loaf.position); wisps(t, [[x - 30, y - 40], [x + 40, y - 60]], '#fff3d0'); popText('FRESH BREAD', W / 2, 280, 124, '#ffd23e', t, wf(9, 'fresh') - 0.05, s1 - 0.02); };
    }
  }
  else if (li >= 10 && li <= 12) {
    exp.visible = true; bg(0x2b2aa8); light(1.2, 1.4, [3, 5, 8], 0xffffff, 0x5a5ac0); LOOK.grade = null; LOOK.bloom = 0.1; expStraight.visible = li === 10; expTrap.visible = li > 10;
    if (li === 10) { blobs.forEach((b, i) => { b.material = STINKM; const p = ((t * 0.4 + i / blobs.length) % 1); b.visible = true; b.position.set(0.18 * Math.sin(i * 2 + t * 4), -4 + p * 12, 0.2); b.scale.setScalar(1); });
      setCam([lerp(0.8, 0, k), 2.4, lerp(12.5, 11.5, k)], [0, 2.2, 0], 42, t);
      overlay = () => { popText('STRAIGHT PIPE', W / 2, 250, 110, '#fff', t, wf(10, 'straight') - 0.05, s1 - 0.02); popText('= OPEN DOOR', W / 2, 390, 118, '#ff9a3a', t, wf(10, 'open') - 0.05, s1 - 0.02); };
    } else if (li === 11) { const f = ss(wf(11, 'keeps') - 0.2, wf(11, 'water') + 0.1, t);
      waterHalves.forEach(w => { w.visible = f > 0.01; const n = w.geometry.index.count; w.geometry.setDrawRange(0, Math.floor(n * f / 6) * 6); });
      blobs.forEach((b, i) => { b.material = WATERM; const p = ((t * 0.9 + i / 5) % 1); b.visible = i < 5 && f < 0.98; b.position.copy(trapCurve.getPoint(lerp(0, U_BOT * 0.9, p))).add(V(0, 0, 0.2)); b.scale.setScalar(0.6); });
      setCam([lerp(-0.6, 0, k), 2.6, lerp(12.5, 11, k)], [0, 2.4, 0], 42, t, 0, 0.03);
      overlay = () => { popText('A BEND', W / 2, 250, 130, '#fff', t, wf(11, 'bend') - 0.05, s1 - 0.02); popText('KEEPS WATER', W / 2, 395, 116, '#6fc3ff', t, wf(11, 'keeps') - 0.05, s1 - 0.02); };
    } else { waterHalves.forEach(w => { w.visible = true; w.geometry.setDrawRange(0, Infinity); });
      blobs.forEach((b, i) => { b.material = STINKM; const p = ((t * 0.45 + i / blobs.length) % 1), tri = p < 0.5 ? p * 2 : 2 - p * 2, u = lerp(1, U_R + 0.035, ss(0, 1, tri)); b.visible = true; b.position.copy(trapCurve.getPoint(u)).add(V(0.12 * Math.sin(i * 3 + t * 5), 0, 0.2)); b.scale.setScalar(1 - 0.25 * ss(0.8, 1, tri)); });
      const tc2 = wf(12, "it's") - 0.08;
      setCam([lerp(0.5, 0.2, k), lerp(2.2, 2.9, k), lerp(11.5, 9.8, k)], [lerp(0.3, 0.4, k), lerp(2.2, 3.0, k), 0], 42, t, 0, -0.03);
      overlay = () => { popText('SMELL', W / 2, 250, 130, '#8fd04a', t, wf(12, 'smell') - 0.05, tc2 - 0.02); popText("CAN'T SWIM", W / 2, 395, 124, '#fff', t, wf(12, "can't") - 0.05, tc2 - 0.02); popText('A CORK', W / 2, 250, 130, '#fff', t, tc2, s1 - 0.02); popText('MADE OF WATER', W / 2, 395, 104, '#6fc3ff', t, wf(12, 'made') - 0.05, s1 - 0.02); };
    }
  }
  else if (li === 13) {
    kitchen.visible = true; kitchenLook(); setPipe(kitchen, 1); const e = ss(0, 1, k);
    setCam([lerp(-0.6, PIPE_X - 0.2, e), lerp(1.9, 1.05, e), lerp(6.2, 3.0, e)], [PIPE_X, lerp(1.6, 0.95, e), PIPE_Z], 44, t, 0, 0.04);
    overlay = () => { const [x, y] = proj(V(PIPE_X, 0.95, PIPE_Z)), pul = 1 + 0.06 * Math.sin(t * 10); ctx.save(); ctx.translate(x, y); ctx.scale(pul, pul); for (const [lw, c] of [[26, INK], [13, '#ffd23e']]) { ctx.strokeStyle = c; ctx.lineWidth = lw; ctx.beginPath(); ctx.ellipse(0, 0, lerp(70, 200, e), lerp(100, 290, e), 0, 0, 7); ctx.stroke(); } ctx.restore();
      popText('UNDER YOUR SINK', W / 2, 250, 104, '#fff', t, wf(13, 'under') - 0.05, s1 - 0.02); popText('RIGHT NOW', W / 2, 385, 124, '#ffd23e', t, wf(13, 'right') - 0.05, s1 - 0.02); };
  }
  else {
    shopLook(); LOOK.grade = ['#ff9a4a', 0.22]; signM.map = signB; signG.visible = true; const ta = wf(14, 'bent') - 0.45, v = t - ta, drop = v < 0 ? 1 : Math.exp(-v * 5) * Math.abs(Math.cos(v * 9)); signG.position.y = 6.52 + (v < 0 ? 4 : drop * 1.2); signG.rotation.z = v < 0 ? 0 : 0.25 * Math.exp(-v * 2.2) * Math.sin(v * 7);
    show(boss, -1.15, 1.5, 0.4); boss.face(v > 0.3 ? 'happy' : 'sad'); boss.pose({ lh: [-0.44, 1.42, 0.05], rh: [0.5, 2.3, 0.2], hx: -0.4 });
    show(albie, 1.25, 1.6, -0.4); albie.face('happy'); albie.pose({ lh: [-0.3, 1.75, 0.3], rh: [0.3, 1.7, 0.3], hx: -0.3, bob: 0.03 * Math.abs(Math.sin(t * 4)) });
    setCam([lerp(1.2, 0.4, k), lerp(1.6, 2.0, k), lerp(12.5, 11.0, ss(0, 1, k))], [0.1, lerp(3.2, 3.5, k), 0], 46, t, 0, 0.03);
    overlay = () => { ctx.save(); for (let i = 0; i < 14; i++) { const p = ((t * 0.22 + i * 0.071) % 1), x = (i * 211) % W + 60 * Math.sin(t * 2 + i), y = p * H; ctx.setTransform(1, 0, 0, 1, x, y); ctx.rotate(t * 2 + i); ctx.fillStyle = ['#e8742a', '#d9a23a', '#b3472d'][i % 3]; ctx.strokeStyle = INK; ctx.lineWidth = 5; ctx.beginPath(); ctx.ellipse(0, 0, 26, 13, 0, 0, 7); ctx.fill(); ctx.stroke(); } ctx.restore(); popText('BY AUTUMN', W / 2, 260, 110, '#ffd23e', t, s0 + 0.1, ta - 0.02); };
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
