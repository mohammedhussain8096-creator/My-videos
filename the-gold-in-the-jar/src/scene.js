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
let TM, Ls, DUR = 59.2;
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
const bodyTex = (coat, trim, o = {}) => (g, w, h) => { g.fillStyle = coat; g.fillRect(0, 0, w, h); if (o.belt) { g.fillStyle = o.belt; g.fillRect(0, h * 0.5, w, h * 0.07); g.fillStyle = '#ffd34d'; g.fillRect(w * 0.47, h * 0.49, w * 0.06, h * 0.09); } if (o.ermine) { g.fillStyle = '#f6f3ec'; g.fillRect(w * 0.38, 0, w * 0.24, h); g.fillStyle = '#1b1522'; for (let i = 0; i < 7; i++) { g.beginPath(); g.ellipse(w * (0.44 + (i % 2) * 0.12), h * (0.08 + i * 0.13), 6, 10, 0, 0, 7); g.fill(); } } if (o.buttons) { g.fillStyle = trim; for (let i = 0; i < 4; i++) { g.beginPath(); g.arc(w * 0.5, h * (0.2 + i * 0.16), 9, 0, 7); g.fill(); } } if (o.apron) { g.fillStyle = trim; g.fillRect(w * 0.3, h * 0.35, w * 0.4, h * 0.6); } if (o.stripes) { g.fillStyle = trim; for (let i = 0; i < 6; i++) g.fillRect(0, h * (0.1 + i * 0.15), w, h * 0.05); } };
const crownHat = hg => { const gm = flat(0xffd34d); M(cyl(0.4, 0.4, 0.2, 20, true), flat(0xffd34d, { side: THREE.DoubleSide }), { ol: 0.04, p: [0, 0.5, -0.02], to: hg }); for (let i = 0; i < 7; i++) { const a = i / 7 * 6.283; M(new THREE.ConeGeometry(0.1, 0.24, 4), gm, { ol: 0.035, p: [Math.cos(a) * 0.38, 0.7, Math.sin(a) * 0.38 - 0.02], to: hg }); M(sph(0.045), flat([0xe2372d, 0x2f8f5b, 0x3b5bd9][i % 3]), { p: [Math.cos(a) * 0.38, 0.84, Math.sin(a) * 0.38 - 0.02], to: hg, cast: false }); } M(sph(0.52, 24, 12, 0, 6.3, 0, 0.9), flat(0xb3272d), { p: [0, 0.2, -0.02], to: hg, cast: false }); };
const capHat = (col) => hg => { const m = flat(col); M(sph(0.6, 32, 16, 0, 6.3, 0, Math.PI * 0.36), m, { ol: 0.045, p: [0, 0.1, -0.03], s: [1.06, 0.7, 1.08], to: hg }); M(cyl(0.36, 0.38, 0.06, 24), m, { ol: 0.04, p: [0, 0.3, 0.5], s: [1.1, 1, 0.6], r: [0.1, 0, 0], to: hg }); };
const tallHat = hg => { const m = flat(0x2a2530); hg.userData.top = M(cyl(0.42, 0.46, 1.1, 24), m, { ol: 0.045, p: [0, 0.95, 0], to: hg }); M(cyl(0.72, 0.72, 0.06, 32), m, { ol: 0.04, p: [0, 0.4, 0], to: hg }); M(cyl(0.465, 0.465, 0.12, 24), flat(0xb3272d), { p: [0, 0.5, 0], to: hg, cast: false }); };
const hoodHat = (col) => hg => { const m = flat(col); M(sph(0.63, 32, 16, 0, 6.3, 0, Math.PI * 0.55), m, { ol: 0.045, p: [0, 0.02, -0.08], to: hg }); };
const braidHair = hg => { const m = flat(0x3a2416); M(sph(0.6, 32, 16, 0, 6.3, 0, Math.PI * 0.42), m, { ol: 0.045, p: [0, 0.06, -0.03], to: hg }); for (const s of [-1, 1]) { M(cyl(0.09, 0.07, 0.7, 10), m, { ol: 0.035, p: [s * 0.5, -0.3, -0.1], r: [0, 0, s * 0.15], to: hg }); M(box(0.12, 0.08, 0.12), flat(0xe2553d), { ol: 0.02, p: [s * 0.55, -0.62, -0.1], to: hg }); } };

// ===== High-detail reference-style characters: crisp 2K faces, big outlined eyes, 3D cartoon hands, clothing details =====
BOIL.value = 0;
function drawFaceHD(g, e, o) {
  const S = 2, cx = 512 * S, cy = 262 * S, W2 = 1024 * S, H2 = 512 * S;
  g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = o.skin || '#fbfaf5'; g.fillRect(0, 0, W2, H2);
  // soft form shading: lighter front-left, cool grey towards the right side and the chin
  const sh = g.createRadialGradient(cx - 120, cy - 120, 80, cx, cy, 760); sh.addColorStop(0, 'rgba(255,255,255,0)'); sh.addColorStop(0.55, 'rgba(0,0,0,0)'); sh.addColorStop(1, 'rgba(70,60,95,0.20)'); g.fillStyle = sh; g.fillRect(0, 0, W2, H2);
  const sh2 = g.createLinearGradient(cx + 120, 0, cx + 520, 0); sh2.addColorStop(0, 'rgba(70,60,95,0)'); sh2.addColorStop(1, 'rgba(70,60,95,0.14)'); g.fillStyle = sh2; g.fillRect(cx + 120, 0, 400, H2);
  g.lineCap = 'round'; g.lineJoin = 'round'; const INKc = '#15111b';
  const ex = 116, ey = cy - 30;
  // cheeks
  g.fillStyle = 'rgba(240,120,110,0.30)'; for (const s of [-1, 1]) { g.beginPath(); g.ellipse(cx + s * 200, cy + 92, 52, 32, 0, 0, 7); g.fill(); }
  if (o.freckles) { g.fillStyle = 'rgba(180,100,70,0.85)'; for (const s of [-1, 1]) for (const [dx, dy] of [[0, 0], [26, 14], [-22, 18], [8, 36]]) { g.beginPath(); g.arc(cx + s * 200 + dx, cy + 74 + dy, 8, 0, 7); g.fill(); } }
  const eyeOval = (x, y, rx, ry, px, py, pr, lid = 0) => { g.fillStyle = '#ffffff'; g.strokeStyle = INKc; g.lineWidth = 15; g.beginPath(); g.ellipse(x, y, rx, ry, 0, 0, 7); g.fill(); g.stroke(); g.save(); g.beginPath(); g.ellipse(x, y, rx - 4, ry - 4, 0, 0, 7); g.clip(); g.fillStyle = INKc; g.beginPath(); g.arc(x + px, y + py, pr, 0, 7); g.fill(); g.fillStyle = '#fff'; g.beginPath(); g.arc(x + px - pr * 0.35, y + py - pr * 0.4, pr * 0.3, 0, 7); g.fill(); if (lid) { g.fillStyle = '#ece9e2'; g.fillRect(x - rx, y - ry, rx * 2, ry * 2 * lid); g.strokeStyle = INKc; g.lineWidth = 13; g.beginPath(); g.moveTo(x - rx, y - ry + ry * 2 * lid); g.lineTo(x + rx, y - ry + ry * 2 * lid); g.stroke(); } g.restore(); };
  const brow = (x, y, a, len = 92, w = 30) => { g.strokeStyle = INKc; g.lineWidth = w; g.beginPath(); g.moveTo(x - len / 2 * Math.cos(a), y - len / 2 * Math.sin(a)); g.lineTo(x + len / 2 * Math.cos(a), y + len / 2 * Math.sin(a)); g.stroke(); };
  for (const s of [-1, 1]) {
    const x = cx + s * ex;
    if (e === 'happy') { g.strokeStyle = INKc; g.lineWidth = 22; g.beginPath(); g.arc(x, ey + 22, 46, Math.PI * 1.12, Math.PI * 1.88); g.stroke(); brow(x, ey - 92, s * -0.12, 80, 24); }
    else if (e === 'sleep') { g.strokeStyle = INKc; g.lineWidth = 20; g.beginPath(); g.arc(x, ey - 10, 42, 0.15 * Math.PI, 0.85 * Math.PI); g.stroke(); }
    else if (e === 'shock') { eyeOval(x, ey - 4, 56, 70, 0, 4, 16); brow(x, ey - 120, s * 0.12, 84, 24); }
    else if (e === 'angry') { eyeOval(x, ey + 6, 44, 46, -s * 6, 6, 20, 0.28); brow(x, ey - 62, s * 0.42, 104, 32); }
    else if (e === 'sad') { eyeOval(x, ey + 6, 42, 50, 0, 14, 20, 0.12); brow(x, ey - 76, -s * 0.38, 92, 26); }
    else if (e === 'sneaky') { eyeOval(x, ey + 4, 46, 44, 22, 6, 20, 0.42); brow(x, ey - 64, s * 0.18, 96, 28); }
    else if (e === 'think') { eyeOval(x, ey, 42, 50, 16, -14, 20); brow(x, ey - (s > 0 ? 104 : 80), s > 0 ? -0.18 : 0.06, 92, 26); }
    else { eyeOval(x, ey, 42, 52, 0, 2, 21); brow(x, ey - 86, s * -0.05, 88, 26); }
  }
  // nose
  g.strokeStyle = INKc; g.lineWidth = 12; g.beginPath(); g.moveTo(cx - 8, cy + 36); g.quadraticCurveTo(cx + 26, cy + 58, cx - 4, cy + 74); g.stroke();
  // mouth
  const my = cy + 138; g.lineWidth = 16; g.strokeStyle = INKc;
  const openMouth = (w, h, tongue = true, teeth = true) => { g.fillStyle = '#6e1d2a'; g.beginPath(); g.moveTo(cx - w, my - 10); g.quadraticCurveTo(cx, my - 22, cx + w, my - 10); g.quadraticCurveTo(cx + w * 0.8, my + h, cx, my + h); g.quadraticCurveTo(cx - w * 0.8, my + h, cx - w, my - 10); g.closePath(); g.fill(); g.save(); g.clip(); if (teeth) { g.fillStyle = '#fff'; g.fillRect(cx - w, my - 30, w * 2, 34); } if (tongue) { g.fillStyle = '#f08a96'; g.beginPath(); g.ellipse(cx, my + h - 4, w * 0.55, h * 0.42, 0, 0, 7); g.fill(); } g.restore(); g.beginPath(); g.moveTo(cx - w, my - 10); g.quadraticCurveTo(cx, my - 22, cx + w, my - 10); g.quadraticCurveTo(cx + w * 0.8, my + h, cx, my + h); g.quadraticCurveTo(cx - w * 0.8, my + h, cx - w, my - 10); g.closePath(); g.stroke(); };
  if (e === 'happy') openMouth(96, 96);
  else if (e === 'shock') { g.fillStyle = '#6e1d2a'; g.beginPath(); g.ellipse(cx, my + 24, 44, 60, 0, 0, 7); g.fill(); g.save(); g.clip(); g.fillStyle = '#f08a96'; g.beginPath(); g.ellipse(cx, my + 66, 34, 26, 0, 0, 7); g.fill(); g.restore(); g.beginPath(); g.ellipse(cx, my + 24, 44, 60, 0, 0, 7); g.stroke(); }
  else if (e === 'angry') { g.fillStyle = '#fff'; g.beginPath(); g.roundRect(cx - 86, my - 16, 172, 64, 18); g.fill(); g.stroke(); g.lineWidth = 8; for (let i = -2; i <= 2; i++) { g.beginPath(); g.moveTo(cx + i * 30, my - 16); g.lineTo(cx + i * 30, my + 48); g.stroke(); } g.beginPath(); g.moveTo(cx - 86, my + 16); g.lineTo(cx + 86, my + 16); g.stroke(); }
  else if (e === 'sad') { g.beginPath(); g.arc(cx, my + 62, 64, 1.18 * Math.PI, 1.82 * Math.PI); g.stroke(); }
  else if (e === 'sneaky') { g.beginPath(); g.moveTo(cx - 70, my + 4); g.quadraticCurveTo(cx + 10, my + 40, cx + 84, my - 26); g.stroke(); }
  else if (e === 'think') { g.beginPath(); g.moveTo(cx - 30, my + 10); g.lineTo(cx + 56, my - 6); g.stroke(); }
  else if (e === 'sleep') { g.beginPath(); g.ellipse(cx, my + 10, 22, 16, 0, 0, 7); g.stroke(); }
  else { g.beginPath(); g.moveTo(cx - 50, my + 4); g.quadraticCurveTo(cx, my + 22, cx + 50, my + 4); g.stroke(); }
  if (o.stache) { g.fillStyle = '#4a2c1c'; g.strokeStyle = INKc; g.lineWidth = 12; for (const s of [-1, 1]) { g.beginPath(); g.moveTo(cx, my - 46); g.quadraticCurveTo(cx + s * 80, my - 82, cx + s * 160, my - 30); g.quadraticCurveTo(cx + s * 80, my - 10, cx, my - 20); g.closePath(); g.fill(); g.stroke(); } }
  if (o.beard) { g.fillStyle = o.beard; g.strokeStyle = INKc; g.lineWidth = 16; g.beginPath(); g.moveTo(cx - 250, cy + 110); g.quadraticCurveTo(cx - 190, cy + 380, cx, cy + 420); g.quadraticCurveTo(cx + 190, cy + 380, cx + 250, cy + 110); g.quadraticCurveTo(cx + 120, cy + 200, cx, cy + 196); g.quadraticCurveTo(cx - 120, cy + 200, cx - 250, cy + 110); g.closePath(); g.fill(); g.stroke(); }
  if (o.wrinkles) { g.strokeStyle = 'rgba(21,17,27,0.55)'; g.lineWidth = 10; for (const s of [-1, 1]) { g.beginPath(); g.moveTo(cx + s * 196, ey - 20); g.lineTo(cx + s * 230, ey + 6); g.stroke(); g.beginPath(); g.moveTo(cx + s * 170, my - 30); g.quadraticCurveTo(cx + s * 196, my, cx + s * 176, my + 30); g.stroke(); } g.beginPath(); g.moveTo(cx - 70, ey - 170); g.lineTo(cx + 70, ey - 170); g.stroke(); }
}
// 3D cartoon hand: palm + three fingers + thumb, outlined; points along the forearm
function makeHand(mat) { const h = new THREE.Group(); M(sph(0.085, 14, 10), mat, { ol: 0.026, s: [1, 1.1, 0.8], to: h }); for (let i = 0; i < 3; i++) M(new THREE.CapsuleGeometry(0.032, 0.07, 4, 8), mat, { ol: 0.022, p: [-0.045 + i * 0.045, 0.11, 0.0], r: [0, 0, (i - 1) * 0.18], to: h }); M(new THREE.CapsuleGeometry(0.03, 0.05, 4, 8), mat, { ol: 0.022, p: [0.075, 0.03, 0.03], r: [0, 0, -1.0], to: h }); return h; }
function makeChar3(o) {
  const c = { g: new THREE.Group(), o, expr: null }; const up = new THREE.Group(); c.g.add(up); c.up = up;
  const HIP = 1.5, HEADY = HIP + 1.5 + 0.44;
  const bt = ctex(1024, 1024, (g, w, h) => { o.body(g, w, h); // fabric folds and form shading
    g.strokeStyle = 'rgba(20,10,30,0.16)'; g.lineWidth = 6; g.lineCap = 'round'; for (const [x0, x1] of [[0.28, 0.24], [0.42, 0.40], [0.6, 0.62], [0.74, 0.78]]) { g.beginPath(); g.moveTo(w * x0, h * 0.58); g.quadraticCurveTo(w * (x0 + x1) / 2 + 8, h * 0.8, w * x1, h); g.stroke(); }
    const sh = g.createLinearGradient(0, 0, w, 0); sh.addColorStop(0, 'rgba(40,15,50,0.24)'); sh.addColorStop(0.28, 'rgba(0,0,0,0)'); sh.addColorStop(0.45, 'rgba(255,255,255,0.07)'); sh.addColorStop(0.72, 'rgba(0,0,0,0)'); sh.addColorStop(1, 'rgba(40,15,50,0.24)'); g.fillStyle = sh; g.fillRect(0, 0, w, h);
    const sv = g.createLinearGradient(0, 0, 0, h); sv.addColorStop(0, 'rgba(0,0,0,0.10)'); sv.addColorStop(0.15, 'rgba(0,0,0,0)'); sv.addColorStop(0.9, 'rgba(0,0,0,0)'); sv.addColorStop(1, 'rgba(0,0,0,0.12)'); g.fillStyle = sv; g.fillRect(0, 0, w, h); });
  bt.anisotropy = 8; c.bodyM = flat(0xffffff, { map: bt }); c.body = M(TUBE, c.bodyM, { ol: 0.05, p: [0, HIP - 0.04, 0], r: [0, Math.PI, 0], to: up });
  // 3D clothing details
  if (o.collar) { M(new THREE.TorusGeometry(0.2, 0.06, 10, 28), flat(o.collar), { ol: 0.025, p: [0, HIP + 1.42, 0], r: [Math.PI / 2, 0, 0], to: up }); }
  if (o.belt3d) { M(new THREE.TorusGeometry(0.335, 0.045, 10, 36), flat(o.belt3d), { ol: 0.022, p: [0, HIP + 0.62, 0], r: [Math.PI / 2, 0, 0], s: [1, 1, 1], to: up }); M(box(0.14, 0.12, 0.04), flat(0xffd34d), { ol: 0.018, p: [0, HIP + 0.62, 0.36], to: up }); }
  if (o.buttons3d) for (let i = 0; i < 3; i++) M(sph(0.035, 10, 8), flat(o.buttons3d), { ol: 0.012, p: [0, HIP + 1.1 - i * 0.2, 0.33 - i * 0.004], to: up, cast: false });
  if (o.scarf) { M(new THREE.TorusGeometry(0.22, 0.075, 10, 28), flat(o.scarf), { ol: 0.028, p: [0, HIP + 1.38, 0], r: [Math.PI / 2, 0, 0], to: up }); M(new THREE.ConeGeometry(0.1, 0.25, 4), flat(o.scarf), { ol: 0.022, p: [0.08, HIP + 1.2, 0.27], r: [0.2, 0, 0.3], to: up }); }
  if (o.bands) { for (const s of [-1, 1]) M(box(0.07, 0.24, 0.02), flat(0xfbfaf4), { ol: 0.012, p: [s * 0.045, HIP + 1.26, 0.33], to: up, cast: false }); }
  c.headG = new THREE.Group(); c.headG.position.set(0, HEADY, 0); up.add(c.headG);
  c.ft = ctex(2048, 1024, g => drawFaceHD(g, 'neutral', o)); c.ft.anisotropy = 8; c.headM = flat(0xffffff, { map: c.ft });
  c.head = M(sph(0.58, 64, 40), c.headM, { ol: 0.05, r: [0, -Math.PI / 2, 0], to: c.headG });
  c.hatG = new THREE.Group(); c.headG.add(c.hatG); if (o.hat) o.hat(c.hatG);
  const armM = flat(o.arm ?? 0x15111b), legM = flat(0x15111b), handM = flat(new THREE.Color(o.skin || '#fbfaf5'));
  c.arms = [-1, 1].map(s => { const h = makeHand(handM); up.add(h); return { s, a: M(UNIT, armM, { to: up }), b: M(UNIT, armM, { to: up }), h }; });
  c.legs = [-1, 1].map(s => { const f = new THREE.Group(); c.g.add(f); M(sph(0.12, 16, 12), flat(o.shoe || 0x2a2530), { ol: 0.026, s: [1, 0.55, 1.7], p: [0, 0, 0.03], to: f }); M(box(0.2, 0.03, 0.34), flat(0x15111b), { p: [0, -0.06, 0.03], to: f, cast: false }); return { s, a: M(UNIT, legM, { to: c.g }), f }; });
  c.mats = [c.bodyM, c.headM, handM]; c.tint = hex => c.mats.forEach(m => m.color.set(hex));
  c.face = e => { if (c.expr !== e) { c.expr = e; drawFaceHD(c.ft.userData.g, e, o); c.ft.needsUpdate = true; } };
  const tmpQ = new THREE.Quaternion();
  c.pose = (p = {}) => {
    const bob = p.bob || 0; up.position.y = bob; up.rotation.z = p.lean || 0; up.rotation.x = p.pitch || 0; c.headG.rotation.set(p.hx || 0, p.hy || 0, p.hz || 0);
    const hands = [p.lh || [-0.5, HIP + 0.55, 0.05], p.rh || [0.5, HIP + 0.55, 0.05]];
    c.arms.forEach((A, i) => { const sh = V(A.s * 0.3, HIP + 1.2, 0), hd = V(...hands[i]); const mid = sh.clone().lerp(hd, 0.5).add(V(A.s * 0.1, -0.1, -0.05)); seg(A.a, sh, mid, 0.032); seg(A.b, mid, hd, 0.032);
      A.h.position.copy(hd); const dir = hd.clone().sub(mid).normalize(); A.h.quaternion.setFromUnitVectors(UP, dir); A.h.rotateY(A.s * 0.6); });
    const feet = [p.lf || [-0.15, 0, 0], p.rf || [0.15, 0, 0]];
    c.legs.forEach((Lg, i) => { const hip = V(Lg.s * 0.13, HIP + 0.1 + bob, 0), ft = V(feet[i][0], feet[i][1] + 0.06, feet[i][2]); seg(Lg.a, ft, hip, 0.036); Lg.f.position.copy(ft).add(V(0, 0, 0.06)); });
  };
  c.walk = (ph, amp = 0.3) => ({ lf: [-0.15, Math.max(0, Math.sin(ph)) * 0.22, Math.cos(ph) * amp], rf: [0.15, Math.max(0, -Math.sin(ph)) * 0.22, -Math.cos(ph) * amp], bob: Math.abs(Math.sin(ph)) * 0.05 });
  c.HIP = HIP; c.HEADY = HEADY; c.face('neutral'); c.pose(); return c;
}
const rnd = (seed => () => (seed = (seed * 16807) % 2147483647) / 2147483647)(57);
const T2s = {
  wood: rep_(ctex(512, 512, (g, w, h) => { g.fillStyle = '#8a5a34'; g.fillRect(0, 0, w, h); for (let i = 0; i < 8; i++) { g.fillStyle = `rgba(${rnd() < 0.5 ? '50,25,10' : '255,215,160'},${0.05 + rnd() * 0.09})`; g.fillRect(0, i * 64, w, 64); g.fillStyle = '#3d2414'; g.fillRect(0, i * 64, w, 4); g.strokeStyle = 'rgba(60,30,15,0.35)'; g.lineWidth = 2; for (let k = 0; k < 6; k++) { const y = i * 64 + 8 + rnd() * 48; g.beginPath(); g.moveTo(0, y); g.bezierCurveTo(w * 0.3, y + (rnd() - 0.5) * 16, w * 0.65, y + (rnd() - 0.5) * 16, w, y); g.stroke(); } g.fillStyle = '#3d2414'; g.beginPath(); g.ellipse(rnd() * w, i * 64 + 32, 7, 4, 0, 0, 7); g.fill(); } }), 3, 3),
  panel: rep_(ctex(512, 512, (g, w, h) => { g.fillStyle = '#6b3f22'; g.fillRect(0, 0, w, h); for (const [x, y] of [[20, 20], [266, 20], [20, 266], [266, 266]]) { g.fillStyle = '#7d4c2a'; g.fillRect(x, y, 226, 226); g.strokeStyle = '#3d2414'; g.lineWidth = 8; g.strokeRect(x, y, 226, 226); g.strokeStyle = 'rgba(255,220,170,0.18)'; g.lineWidth = 4; g.strokeRect(x + 14, y + 14, 198, 198); } }), 6, 2),
  tiles: rep_(ctex(256, 256, (g, w, h) => { for (let y = 0; y < 4; y++) for (let x = 0; x < 4; x++) { g.fillStyle = (x + y) % 2 ? '#e8dcc0' : '#5a3a2a'; g.fillRect(x * 64, y * 64, 64, 64); g.fillStyle = 'rgba(0,0,0,0.06)'; g.fillRect(x * 64, y * 64 + 58, 64, 6); } }), 10, 10),
  stone: rep_(ctex(256, 256, (g, w, h) => { g.fillStyle = '#6a6070'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 42) for (let x = (y / 42 % 2) * 40 - 80; x < w; x += 80) { g.fillStyle = `hsl(${250 + rnd() * 30},${6 + rnd() * 8}%,${44 + rnd() * 14}%)`; g.fillRect(x + 3, y + 3, 74, 36); } }), 3, 3),
  brickW: rep_(ctex(256, 256, (g, w, h) => { g.fillStyle = '#5a3a30'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 32) for (let x = (y / 32 % 2) * 32 - 64; x < w; x += 64) { g.fillStyle = `hsl(${10 + rnd() * 12},${36 + rnd() * 16}%,${32 + rnd() * 12}%)`; g.fillRect(x + 3, y + 3, 58, 26); } }), 4, 3),
  cobble: rep_(ctex(256, 256, (g, w, h) => { g.fillStyle = '#3d3a48'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 32) for (let x = (y / 32 % 2) * 20 - 40; x < w; x += 40) { g.fillStyle = `hsl(${240 + rnd() * 20},${8 + rnd() * 6}%,${36 + rnd() * 14}%)`; g.beginPath(); g.ellipse(x + 20, y + 16, 17, 13, 0, 0, 7); g.fill(); g.strokeStyle = 'rgba(0,0,0,0.3)'; g.lineWidth = 2; g.stroke(); } }), 10, 10),
  plaster: ctex(512, 512, (g, w, h) => { g.fillStyle = '#e9d6ad'; g.fillRect(0, 0, w, h); for (let i = 0; i < 160; i++) { g.fillStyle = `rgba(110,80,40,${0.03 + rnd() * 0.05})`; g.beginPath(); g.ellipse(rnd() * w, rnd() * h, 10 + rnd() * 40, 6 + rnd() * 20, rnd() * 3, 0, 7); g.fill(); } g.fillStyle = '#3d2718'; for (const x of [0, 248, 494]) g.fillRect(x, 0, 18, h); g.fillRect(0, 0, w, 18); g.fillRect(0, 250, w, 16); g.fillRect(0, 494, w, 18); }),
};

// ===== The Gold the Nazis Couldn't See — Copenhagen lab 1940, canal street, explainer =====
const FT = []; function ftex(w, h, d) { const t = ctex(w, h, d); t.userData.draw = d; FT.push(t); return t; }
window.afterFonts = () => FT.forEach(t => { t.userData.draw(t.userData.g, t.userData.c.width, t.userData.c.height); t.needsUpdate = true; });
sun.shadow.mapSize.set(4096, 4096); sun.shadow.bias = -0.0005;
function shadowBox(r, far = 80) { Object.assign(sun.shadow.camera, { left: -r, right: r, top: r, bottom: -r, near: 1, far }); sun.shadow.camera.updateProjectionMatrix(); }
const glowTex = ctex(128, 128, g => { const r = g.createRadialGradient(64, 64, 0, 64, 64, 64); r.addColorStop(0, 'rgba(255,245,210,1)'); r.addColorStop(0.35, 'rgba(255,200,110,0.5)'); r.addColorStop(1, 'rgba(255,170,60,0)'); g.fillStyle = r; g.fillRect(0, 0, 128, 128); });
const smokeTex = ctex(128, 128, g => { const r = g.createRadialGradient(64, 64, 0, 64, 64, 64); r.addColorStop(0, 'rgba(255,190,90,0.7)'); r.addColorStop(0.6, 'rgba(240,170,80,0.3)'); r.addColorStop(1, 'rgba(240,170,80,0)'); g.fillStyle = r; g.fillRect(0, 0, 128, 128); });
function glow(parent, x, y, z, s = 1.2, op = 0.9) { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: op })); sp.position.set(x, y, z); sp.scale.set(s, s, 1); parent.add(sp); return sp; }
const outlineInst = th => new THREE.ShaderMaterial({ side: THREE.BackSide, uniforms: { th: { value: th } }, vertexShader: 'uniform float th; void main(){ vec4 p = instanceMatrix * vec4(position + normal * th, 1.0); gl_Position = projectionMatrix * modelViewMatrix * p; }', fragmentShader: 'void main(){ gl_FragColor = vec4(0.085,0.065,0.11,1.0); }' });
const dummy = new THREE.Object3D(), tmpC = new THREE.Color();
const tc = (t, a, b) => { const c = t.clone(); c.needsUpdate = true; return rep_(c, a, b); };
const glassM = (c = 0xd8eef4, op = 0.35) => toon(c, { transparent: true, opacity: op, depthWrite: false });

// ---------------- the lab ----------------
const lab = new THREE.Group(); root.add(lab);
const LX = 7, LZ = 6, LH = 5.6;
M(box(2 * LX, 0.2, 2 * LZ), toon(0xffffff, { map: tc(T2s.wood, 4, 4) }), { p: [0, -0.1, 0], recv: true, to: lab, cast: false });
const plasterLab = ctex(512, 512, (g, w, h) => { g.fillStyle = '#d9cfb4'; g.fillRect(0, 0, w, h); for (let i = 0; i < 220; i++) { g.fillStyle = `rgba(110,90,60,${0.03 + rnd() * 0.05})`; g.beginPath(); g.ellipse(rnd() * w, rnd() * h, 10 + rnd() * 40, 6 + rnd() * 20, rnd() * 3, 0, 7); g.fill(); } });
const wallM = toon(0xffffff, { map: rep_(plasterLab, 3, 1) }), wainM = toon(0xffffff, { map: tc(T2s.panel, 3, 1) });
function wallPiece(w, h, x, y, z, ry) { const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; lab.add(g); M(box(w, h, 0.25), wallM, { recv: true, to: g }); return g; }
// back wall (z = -LZ) and right wall (x = +LX) solid; plaster above, panelled wainscot below
wallPiece(2.2 + LZ, LH, LX, LH / 2, (-LZ + 2.2) / 2, -Math.PI / 2); wallPiece(LZ - 3.8, LH, LX, LH / 2, (LZ + 3.8) / 2, -Math.PI / 2); wallPiece(1.6, LH - 4.0, LX, (LH + 4.0) / 2, 3.0, -Math.PI / 2); M(new THREE.PlaneGeometry(3, 5), flat(0xfff2d8), { p: [LX + 1.2, 2.2, 3.0], r: [0, -Math.PI / 2, 0], to: lab, cast: false });
for (const [w, x, z, ry] of [[2 * LX, 0, -LZ, 0], [2 * LZ, LX, 0, -Math.PI / 2]]) { if (x === 0) wallPiece(w, LH, x, LH / 2, z, ry); const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry; lab.add(g); M(box(w, 1.3, 0.1), wainM, { p: [0, 0.65, 0.17], recv: true, to: g, cast: false }); M(box(w, 0.12, 0.16), toon(0x5a3a22), { p: [0, 1.33, 0.19], to: g, cast: false }); M(box(w, 0.25, 0.14), toon(0x4a2e1c), { p: [0, LH - 0.13, 0.19], to: g, cast: false }); }
// left wall (x = -LX) built around two tall windows so the sun pours through
{ const wins = [[-3.0, 1.7], [2.4, 1.7]], y0 = 1.3, y1 = 4.3; let zc = -LZ;
  for (const [zw, ww] of wins) { const a = zw - ww / 2; if (a > zc) wallPiece(a - zc, LH, -LX, LH / 2, (a + zc) / 2, Math.PI / 2); wallPiece(ww, y0, -LX, y0 / 2, zw, Math.PI / 2); wallPiece(ww, LH - y1, -LX, (LH + y1) / 2, zw, Math.PI / 2); zc = zw + ww / 2;
    const fr = new THREE.Group(); fr.position.set(-LX + 0.05, 0, zw); fr.rotation.y = Math.PI / 2; lab.add(fr); const wm = toon(0xf3efe6);
    for (const [w, h, x, y] of [[ww + 0.2, 0.14, 0, y0], [ww + 0.2, 0.14, 0, y1], [0.14, y1 - y0, -ww / 2, (y0 + y1) / 2], [0.14, y1 - y0, ww / 2, (y0 + y1) / 2], [0.07, y1 - y0, 0, (y0 + y1) / 2], [ww, 0.07, 0, y0 + (y1 - y0) * 0.36], [ww, 0.07, 0, y0 + (y1 - y0) * 0.68]]) M(box(w, h, 0.16), wm, { ol: 0.012, p: [x, y, 0], to: fr });
    M(box(ww + 0.5, 0.1, 0.5), toon(0xf3efe6), { ol: 0.015, p: [0, y0 - 0.02, 0.2], to: fr }); for (const s of [-1, 1]) M(box(0.5, y1 - y0 + 0.6, 0.08), toon(0x7a2f2a), { ol: 0.012, p: [s * (ww / 2 + 0.35), (y0 + y1) / 2 + 0.2, 0.22], to: fr }); }
  if (zc < LZ) wallPiece(LZ - zc, LH, -LX, LH / 2, (LZ + zc) / 2, Math.PI / 2);
  // what you see through the windows: Copenhagen rooftops and a copper spire
  const view = ftex(1024, 512, (g, w, h) => { const s = g.createLinearGradient(0, 0, 0, h); s.addColorStop(0, '#9cc0e0'); s.addColorStop(1, '#e8eef0'); g.fillStyle = s; g.fillRect(0, 0, w, h); const cols = ['#c8604a', '#e0b050', '#d88a5a', '#b8b0a0', '#c87a4a']; for (let i = 0; i < 18; i++) { const x = i * 60 - 20, ht = 140 + (i * 37) % 120; g.fillStyle = cols[i % 5]; g.fillRect(x, h - ht, 58, ht); g.fillStyle = '#8a4a3a'; g.beginPath(); g.moveTo(x - 4, h - ht); g.lineTo(x + 29, h - ht - 50); g.lineTo(x + 62, h - ht); g.fill(); g.fillStyle = 'rgba(40,50,70,0.55)'; for (let r = 0; r < 4; r++) for (let c = 0; c < 2; c++) g.fillRect(x + 10 + c * 24, h - ht + 20 + r * 34, 12, 18); } g.fillStyle = '#5aa08a'; g.beginPath(); g.moveTo(600, 40); g.lineTo(625, 260); g.lineTo(575, 260); g.fill(); g.fillRect(570, 260, 60, 200); });
  M(new THREE.PlaneGeometry(34, 14), flat(0xffffff, { map: view }), { p: [-LX - 4, 4.0, 0], r: [0, Math.PI / 2, 0], to: lab, cast: false }); }
M(box(2 * LX, 0.2, 2 * LZ), toon(0xe8dcc0), { p: [0, LH + 0.1, 0], to: lab });
// pendant lamps
const lampLights = []; for (const x of [-3.2, 0.2, 3.6]) { const g = new THREE.Group(); g.position.set(x, LH, -0.6); lab.add(g); M(cyl(0.015, 0.015, 1.2, 6), toon(0x1b1522), { p: [0, -0.6, 0], to: g, cast: false }); M(cyl(0.12, 0.55, 0.42, 24, true), toon(0x2f5a4a, { side: THREE.DoubleSide }), { ol: 0.02, p: [0, -1.35, 0], to: g, cast: false }); M(sph(0.13, 12, 8), flat(0xfff2c8), { p: [0, -1.5, 0], to: g, cast: false }); glow(g, 0, -1.5, 0, 1.3, 0.6); const l = new THREE.PointLight(0xffd9a0, 6, 9, 1.5); l.position.set(0, -1.7, 0); g.add(l); lampLights.push(l); }

// ---- the great shelf of bottles (back wall) ----
const SHX0 = -6.4, SHX1 = 2.6, SHZ = -LZ + 0.42, BOARDS = [0.35, 1.05, 1.75, 2.45, 3.15, 3.85, 4.55];
{ const wm = toon(0xffffff, { map: tc(T2s.wood, 3, 0.25) }); for (const y of BOARDS) M(box(SHX1 - SHX0, 0.08, 0.62), wm, { ol: 0.015, p: [(SHX0 + SHX1) / 2, y, SHZ], recv: true, to: lab });
  for (let x = SHX0; x <= SHX1 + 0.01; x += (SHX1 - SHX0) / 4) M(box(0.12, BOARDS[6] + 0.15, 0.64), toon(0x6b4326), { ol: 0.015, p: [x, (BOARDS[6] + 0.15) / 2, SHZ], to: lab }); M(box(SHX1 - SHX0 + 0.2, 0.18, 0.7), toon(0x5a3a22), { ol: 0.015, p: [(SHX0 + SHX1) / 2, BOARDS[6] + 0.2, SHZ], to: lab }); }
// labels: one cream label texture with "handwriting"
const labelTex = ctex(128, 96, (g, w, h) => { g.fillStyle = '#f2ead2'; g.fillRect(0, 0, w, h); g.strokeStyle = '#3a2a1a'; g.lineWidth = 5; g.strokeRect(4, 4, w - 8, h - 8); g.lineWidth = 4; for (let i = 0; i < 3; i++) { g.beginPath(); let x = 14; g.moveTo(x, 30 + i * 22); while (x < w - 16) { x += 6 + rnd() * 8; g.lineTo(x, 30 + i * 22 + (rnd() - 0.5) * 7); } g.stroke(); } });
const glassCols = [0x8a4a1a, 0x9a5a20, 0x3f7a4a, 0x2f5a8a, 0x5a3a2a, 0xb8d8e0, 0xe8e4d8, 0x7a2a3a, 0xc87a2a, 0x4a6a3a];
const BOT = { tall: [], jar: [], flask: [] }; const JAR_SLOT = { board: 3, x: -1.0 };
for (let b = 1; b < 6; b++) for (let x = SHX0 + 0.3; x < SHX1 - 0.2; x += 0.3 + rnd() * 0.12) { if (b === JAR_SLOT.board && Math.abs(x - JAR_SLOT.x) < 0.3) continue; if (b === 2 && Math.abs(x - 1.6) < 0.32) continue; const k = rnd(); const kind = k < 0.5 ? 'tall' : k < 0.8 ? 'jar' : 'flask'; BOT[kind].push([x, BOARDS[b] + 0.04, SHZ + (rnd() - 0.5) * 0.18, 0.8 + rnd() * 0.45, glassCols[Math.floor(rnd() * glassCols.length)]]); }
// loose bottles on the bench and desk too
const botGeo = { tall: (() => { const g = new THREE.CylinderGeometry(0.11, 0.12, 0.42, 16); g.translate(0, 0.21, 0); return g; })(), jar: (() => { const g = new THREE.CylinderGeometry(0.14, 0.14, 0.3, 18); g.translate(0, 0.15, 0); return g; })(), flask: (() => { const g = new THREE.SphereGeometry(0.15, 16, 12); g.translate(0, 0.15, 0); return g; })() };
const capGeo = { tall: (() => { const g = new THREE.CylinderGeometry(0.045, 0.06, 0.16, 10); g.translate(0, 0.5, 0); return g; })(), jar: (() => { const g = new THREE.CylinderGeometry(0.15, 0.15, 0.06, 18); g.translate(0, 0.33, 0); return g; })(), flask: (() => { const g = new THREE.CylinderGeometry(0.04, 0.05, 0.2, 10); g.translate(0, 0.36, 0); return g; })() };
const labGeo = { tall: (() => { const g = new THREE.PlaneGeometry(0.17, 0.14); g.translate(0, 0.2, 0.122); return g; })(), jar: (() => { const g = new THREE.PlaneGeometry(0.19, 0.12); g.translate(0, 0.15, 0.143); return g; })(), flask: (() => { const g = new THREE.PlaneGeometry(0.14, 0.1); g.translate(0, 0.15, 0.152); return g; })() };
for (const kind of ['tall', 'jar', 'flask']) { const L = BOT[kind], n = L.length; const body = new THREE.InstancedMesh(botGeo[kind], toon(0xffffff), n), ol = new THREE.InstancedMesh(botGeo[kind], outlineInst(0.014), n), cap = new THREE.InstancedMesh(capGeo[kind], toon(0xffffff), n), lb = new THREE.InstancedMesh(labGeo[kind], toon(0xffffff, { map: labelTex }), n);
  L.forEach(([x, y, z, s, c], i) => { dummy.position.set(x, y, z); dummy.rotation.set(0, (rnd() - 0.5) * 0.5, 0); dummy.scale.set(s, s * (0.9 + rnd() * 0.3), s); dummy.updateMatrix(); for (const m of [body, ol, cap, lb]) m.setMatrixAt(i, dummy.matrix); body.setColorAt(i, tmpC.set(c)); cap.setColorAt(i, tmpC.set(kind === 'jar' ? [0x2a2420, 0x6b4326, 0xc8ccd6][i % 3] : 0x8a6a4a)); lb.setColorAt(i, tmpC.setHSL(0.11, 0.3, 0.85 + rnd() * 0.12)); });
  body.castShadow = true; for (const m of [body, ol, cap, lb]) lab.add(m); }
// THE jar: plain glass jar of orange liquid, cork lid, small label "No. 47"
const jar = new THREE.Group(); jar.position.set(JAR_SLOT.x, BOARDS[JAR_SLOT.board] + 0.04, SHZ + 0.05); lab.add(jar);
{ M(cyl(0.17, 0.17, 0.42, 28, true), glassM(0xe0f0f4, 0.3), { ol: 0.016, p: [0, 0.21, 0], to: jar, cast: false }); jar.userData.liq = M(cyl(0.155, 0.155, 0.32, 28), toon(0xf08a2a), { p: [0, 0.165, 0], to: jar }); M(cyl(0.13, 0.12, 0.09, 20), toon(0xb07a4a), { ol: 0.012, p: [0, 0.45, 0], to: jar });
  const lt = ftex(128, 96, g => { g.fillStyle = '#f2ead2'; g.fillRect(0, 0, 128, 96); g.strokeStyle = '#3a2a1a'; g.lineWidth = 5; g.strokeRect(4, 4, 120, 88); g.fillStyle = '#3a2a1a'; g.font = '40px Pop'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('No. 47', 64, 50); }); M(new THREE.PlaneGeometry(0.2, 0.15), toon(0xffffff, { map: lt }), { p: [0, 0.22, 0.172], to: jar, cast: false });
  jar.userData.sp = []; for (let i = 0; i < 14; i++) { const s = glow(jar, (rnd() - 0.5) * 0.22, 0.05 + rnd() * 0.28, (rnd() - 0.5) * 0.22, 0.05, 0); jar.userData.sp.push(s); } }
// lab bench with glassware
const bench = new THREE.Group(); bench.position.set(-2.2, 0, -1.6); lab.add(bench);
{ const tw = toon(0xffffff, { map: tc(T2s.wood, 2, 0.6) }); M(box(5.2, 0.12, 1.5), tw, { ol: 0.02, p: [0, 1.38, 0], recv: true, to: bench }); M(box(5.0, 1.2, 1.3), toon(0xffffff, { map: tc(T2s.panel, 3, 1) }), { ol: 0.02, p: [0, 0.68, 0], to: bench });
  for (let i = 0; i < 5; i++) M(sph(0.04, 8, 6), toon(0xd9b36a), { p: [-2 + i, 0.95, 0.66], to: bench, cast: false });
  // beakers, flasks, test-tube rack, retort stand, bunsen burner, microscope, notebook
  for (const [x, z, r, h, c] of [[-1.9, 0.2, 0.18, 0.4, 0x5fb4e6], [-1.4, -0.3, 0.14, 0.32, 0x8fd04a], [2.3, 0.3, 0.13, 0.3, 0xf2c230]]) { const g = new THREE.Group(); g.position.set(x, 1.44, z); bench.add(g); M(cyl(r, r, h, 20, true), glassM(), { ol: 0.012, p: [0, h / 2, 0], to: g, cast: false }); M(cyl(r * 0.92, r * 0.92, h * 0.55, 20), toon(c), { p: [0, h * 0.28, 0], to: g }); for (let k = 1; k < 4; k++) M(box(r * 0.5, 0.012, 0.01), flat(0x1b1522), { p: [-r * 0.3, h * k / 4, r + 0.002], to: g, cast: false }); }
  for (const [x, z, c] of [[-0.6, 0.3, 0x5fb4e6], [0.9, 0.35, 0x8fd04a]]) { const g = new THREE.Group(); g.position.set(x, 1.44, z); bench.add(g); M(new THREE.ConeGeometry(0.24, 0.42, 20, 1, true), glassM(), { ol: 0.012, p: [0, 0.21, 0], to: g, cast: false }); M(new THREE.ConeGeometry(0.2, 0.2, 20), toon(c), { p: [0, 0.1, 0], to: g }); M(cyl(0.06, 0.06, 0.2, 10, true), glassM(), { ol: 0.01, p: [0, 0.5, 0], to: g, cast: false }); }
  { const g = new THREE.Group(); g.position.set(0.2, 1.44, -0.35); bench.add(g); M(box(0.8, 0.06, 0.25), toon(0x7a5232), { ol: 0.012, p: [0, 0.3, 0], to: g }); M(box(0.8, 0.06, 0.25), toon(0x7a5232), { ol: 0.012, p: [0, 0.02, 0], to: g }); for (let i = 0; i < 6; i++) { M(cyl(0.035, 0.035, 0.5, 10, true), glassM(), { ol: 0.008, p: [-0.3 + i * 0.12, 0.27, 0], to: g, cast: false }); M(cyl(0.03, 0.03, 0.22, 10), toon([0xe2453a, 0x5fb4e6, 0xf2c230, 0x8fd04a, 0xe07ab0, 0xf08a2a][i]), { p: [-0.3 + i * 0.12, 0.13, 0], to: g }); } }
  { const g = new THREE.Group(); g.position.set(-0.4, 1.44, -0.3); bench.add(g); M(box(0.5, 0.05, 0.35), toon(0x2a2430), { ol: 0.01, to: g }); M(cyl(0.025, 0.025, 1.4, 8), toon(0x6a6a72), { ol: 0.008, p: [0, 0.7, -0.1], to: g }); M(new THREE.TorusGeometry(0.16, 0.02, 6, 20), toon(0x6a6a72), { p: [0.15, 0.85, -0.1], r: [Math.PI / 2, 0, 0], to: g }); M(sph(0.17, 18, 14), glassM(0xe8f4f8, 0.4), { ol: 0.01, p: [0.15, 1.02, -0.1], to: g, cast: false }); M(sph(0.12, 14, 10), toon(0xb05aa0), { p: [0.15, 0.97, -0.1], to: g }); M(cyl(0.04, 0.05, 0.4, 8), toon(0x8a8a96), { ol: 0.008, p: [0.15, 0.25, -0.1], to: g }); g.userData.flame = glow(g, 0.15, 0.5, -0.1, 0.35, 0.8); g.userData.flame.material.color.set(0x7ab0ff); }
  { const g = new THREE.Group(); g.position.set(1.0, 1.44, -0.35); bench.add(g); M(box(0.4, 0.06, 0.4), toon(0x1b1522), { ol: 0.01, to: g }); M(box(0.08, 0.6, 0.12), toon(0x2a2430), { ol: 0.01, p: [0, 0.3, -0.12], r: [0.25, 0, 0], to: g }); M(cyl(0.07, 0.07, 0.45, 12), toon(0x2a2430), { ol: 0.01, p: [0, 0.62, 0], r: [0.35, 0, 0], to: g }); M(box(0.24, 0.03, 0.24), toon(0x6a6a72), { p: [0, 0.28, 0.02], to: g }); }
  { const nb = ctex(256, 192, g => { g.fillStyle = '#f6f0dc'; g.fillRect(0, 0, 256, 192); g.strokeStyle = '#2a3a6a'; g.lineWidth = 3; for (let i = 0; i < 9; i++) { g.beginPath(); let x = 16; g.moveTo(x, 20 + i * 19); while (x < 240) { x += 5 + rnd() * 9; g.lineTo(x, 20 + i * 19 + (rnd() - 0.5) * 5); } g.stroke(); } }); M(box(0.6, 0.03, 0.45), toon(0xffffff, { map: nb }), { ol: 0.01, p: [-1.0, 1.46, 0.35], r: [0, 0.2, 0], to: bench }); } }
// big beaker for the dissolving (sits at the bench's right end)
const beaker = new THREE.Group(); beaker.position.set(-0.35, 1.44, -1.55); lab.add(beaker);
{ M(cyl(0.38, 0.38, 0.8, 32, true), glassM(0xe8f6fa, 0.28), { ol: 0.018, p: [0, 0.4, 0], to: beaker, cast: false }); M(new THREE.TorusGeometry(0.38, 0.02, 6, 32), glassM(0xe8f6fa, 0.6), { p: [0, 0.8, 0], r: [Math.PI / 2, 0, 0], to: beaker, cast: false });
  beaker.userData.liq = M(cyl(0.36, 0.36, 0.55, 32), toon(0xf2d27a, { transparent: true, opacity: 0.75 }), { p: [0, 0.28, 0], to: beaker, cast: false }); for (let k = 1; k < 5; k++) M(box(0.12, 0.012, 0.01), flat(0x1b1522), { p: [-0.18, k * 0.15, 0.381], to: beaker, cast: false });
  beaker.userData.bub = []; for (let i = 0; i < 26; i++) { const b = M(sph(0.025 + rnd() * 0.02, 8, 6), toon(0xfff2c8, { transparent: true, opacity: 0.85 }), { to: beaker, cast: false }); b.userData.ph = rnd(); b.userData.x = (rnd() - 0.5) * 0.5; b.userData.z = (rnd() - 0.5) * 0.5; beaker.userData.bub.push(b); }
  beaker.userData.fumes = []; for (let i = 0; i < 10; i++) { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: smokeTex, depthWrite: false, transparent: true, opacity: 0 })); beaker.add(s); beaker.userData.fumes.push(s); } }
// acid bottle with an in-world label
const acid = new THREE.Group(); lab.add(acid);
{ M(cyl(0.2, 0.22, 0.62, 20), toon(0x6a3a1a), { ol: 0.016, p: [0, 0.31, 0], to: acid }); M(cyl(0.07, 0.11, 0.18, 14), toon(0x6a3a1a), { ol: 0.012, p: [0, 0.7, 0], to: acid }); M(cyl(0.08, 0.06, 0.1, 12), toon(0xd8d4c8), { ol: 0.01, p: [0, 0.83, 0], to: acid });
  const lt = ftex(256, 224, g => { g.fillStyle = '#f2ead2'; g.fillRect(0, 0, 256, 224); g.strokeStyle = '#7a1a1a'; g.lineWidth = 8; g.strokeRect(6, 6, 244, 212); g.fillStyle = '#1b1522'; g.font = '44px Pop'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('AQUA', 128, 52); g.fillText('REGIA', 128, 100); g.fillStyle = '#7a1a1a'; g.beginPath(); g.arc(128, 160, 30, 0, 7); g.fill(); g.fillStyle = '#f2ead2'; g.beginPath(); g.arc(117, 156, 8, 0, 7); g.arc(139, 156, 8, 0, 7); g.fill(); g.fillRect(118, 176, 20, 8); });
  M(new THREE.CylinderGeometry(0.205, 0.215, 0.36, 24, 1, true, -0.9, 1.8), toon(0xffffff, { map: lt }), { p: [0, 0.32, 0], to: acid, cast: false }); acid.position.set(1.6, BOARDS[2] + 0.04, SHZ + 0.05); acid.userData.home = acid.position.clone(); }
// cabinet with drawers (right wall)
const cab = new THREE.Group(); cab.position.set(LX - 0.55, 0, -2.4); cab.rotation.y = -Math.PI / 2; lab.add(cab); const drawers = [];
{ M(box(3.2, 2.6, 0.8), toon(0xffffff, { map: tc(T2s.wood, 2, 1) }), { ol: 0.02, p: [0, 1.3, 0], to: cab }); M(box(3.4, 0.12, 0.9), toon(0x5a3a22), { ol: 0.015, p: [0, 2.66, 0], to: cab });
  for (let r = 0; r < 4; r++) for (let c = 0; c < 3; c++) { const d = new THREE.Group(); d.position.set(-1.05 + c * 1.05, 0.38 + r * 0.6, 0.0); cab.add(d); M(box(0.98, 0.54, 0.76), toon(0xffffff, { map: T2s.panel }), { ol: 0.012, p: [0, 0, 0.03], to: d }); M(box(0.3, 0.05, 0.06), toon(0xd9b36a), { ol: 0.008, p: [0, 0.05, 0.44], to: d }); M(box(0.2, 0.1, 0.01), toon(0xf2ead2), { p: [0, -0.12, 0.42], to: d, cast: false }); for (let k = 0; k < 4; k++) M(box(0.7, 0.01, 0.5), toon(0xf6f0dc), { p: [0, 0.2 + k * 0.012, 0], r: [0, (k - 2) * 0.05, 0], to: d, cast: false }); drawers.push(d); } }
// chalkboard (back wall, right of the shelf)
{ const cb = ftex(1024, 640, (g, w, h) => { g.fillStyle = '#26382e'; g.fillRect(0, 0, w, h); g.fillStyle = 'rgba(255,255,255,0.05)'; for (let i = 0; i < 40; i++) g.fillRect(rnd() * w, rnd() * h, 120, 30); g.fillStyle = '#f2f2ea'; g.font = '58px Pop'; g.fillText('Au + HNO₃ + 4HCl', 50, 120); g.fillText('→ HAuCl₄ + NO + 2H₂O', 90, 210); g.font = '44px Pop'; g.fillText('E = hν', 70, 330); g.fillText('λ = h / p', 70, 410); g.strokeStyle = '#f2f2ea'; g.lineWidth = 5; g.beginPath(); g.arc(760, 420, 110, 0, 7); g.stroke(); g.beginPath(); g.ellipse(760, 420, 110, 40, 0.5, 0, 7); g.stroke(); g.beginPath(); g.ellipse(760, 420, 110, 40, -0.5, 0, 7); g.stroke(); g.beginPath(); g.arc(760, 420, 16, 0, 7); g.fill(); });
  M(box(3.4, 2.2, 0.08), toon(0xffffff, { map: cb }), { ol: 0.02, p: [4.8, 2.6, -LZ + 0.17], to: lab }); M(box(3.6, 0.12, 0.2), toon(0x6b4326), { ol: 0.015, p: [4.8, 1.45, -LZ + 0.2], to: lab }); }
// door (right wall) on a hinge
const door = new THREE.Group(); door.position.set(LX - 0.14, 0, 3.0 - 0.8); door.rotation.y = 0; lab.add(door);
{ M(box(0.1, 3.9, 1.6), toon(0xffffff, { map: T2s.panel }), { ol: 0.02, p: [0, 1.95, 0.8], to: door }); M(sph(0.07, 10, 8), toon(0xd9b36a), { p: [-0.1, 1.8, 1.4], to: door, cast: false }); const fm = toon(0x4a2e1c); for (const [w, h, z, y] of [[0.2, 4.1, 2.2 - 0.02, 2.05], [0.2, 4.1, 3.8 + 0.02, 2.05], [0.2, 0.2, 3.0, 4.05]]) M(box(0.22, h, w), fm, { ol: 0.015, p: [LX - 0.16, y, z], to: lab }); }
const doorLight = new THREE.PointLight(0xfff0d0, 0, 12, 1.2); doorLight.position.set(LX + 1.5, 2.2, 3.0); lab.add(doorLight);
// Hevesy's desk: lamp, name plate, papers, velvet medal box
const desk = new THREE.Group(); desk.position.set(3.4, 0, 2.0); desk.rotation.y = -0.25; lab.add(desk);
{ const dw = toon(0xffffff, { map: tc(T2s.wood, 2, 0.7) }); M(box(2.8, 0.12, 1.4), dw, { ol: 0.02, p: [0, 1.36, 0], recv: true, to: desk }); for (const s of [-1, 1]) M(box(0.8, 1.3, 1.3), toon(0xffffff, { map: T2s.panel }), { ol: 0.015, p: [s * 0.95, 0.65, 0], to: desk });
  const lp = new THREE.Group(); lp.position.set(-1.0, 1.42, -0.35); desk.add(lp); M(cyl(0.18, 0.2, 0.05, 16), toon(0x2f5a4a), { ol: 0.01, to: lp }); M(cyl(0.025, 0.025, 0.6, 8), toon(0xd9b36a), { p: [0, 0.3, 0], to: lp }); M(cyl(0.1, 0.25, 0.22, 18, true), toon(0x2f7a4a, { side: THREE.DoubleSide }), { ol: 0.012, p: [0.12, 0.6, 0], r: [0, 0, 0.5], to: lp, cast: false }); glow(lp, 0.16, 0.52, 0, 0.6, 0.7);
  const np = ftex(512, 112, g => { g.fillStyle = '#2a1a12'; g.fillRect(0, 0, 512, 112); g.strokeStyle = '#d9b36a'; g.lineWidth = 8; g.strokeRect(8, 8, 496, 96); g.fillStyle = '#e8c870'; g.font = '50px Pop'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('G. de HEVESY', 256, 60); }); M(box(0.95, 0.2, 0.08), toon(0xffffff, { map: np }), { ol: 0.01, p: [0.2, 1.52, 0.55], r: [-0.3, 0, 0], to: desk });
  for (let i = 0; i < 4; i++) M(box(0.5, 0.01, 0.65), toon(0xf6f0dc), { p: [0.75 + i * 0.03, 1.43 + i * 0.012, -0.1], r: [0, 0.2 * i - 0.2, 0], to: desk, cast: false }); M(cyl(0.07, 0.08, 0.1, 12), toon(0x1b1522), { ol: 0.01, p: [-0.3, 1.47, -0.4], to: desk }); }
// medals and their velvet box
function medalTex(name) { return ftex(512, 512, (g, w, h) => { const r = g.createRadialGradient(200, 180, 30, 256, 256, 260); r.addColorStop(0, '#fff2a8'); r.addColorStop(0.5, '#e8b83a'); r.addColorStop(1, '#a8741a'); g.fillStyle = r; g.fillRect(0, 0, w, h); g.strokeStyle = '#8a5a10'; g.lineWidth = 14; g.beginPath(); g.arc(256, 256, 236, 0, 7); g.stroke(); g.lineWidth = 5; g.beginPath(); g.arc(256, 256, 160, 0, 7); g.stroke();
  // engraved profile
  g.fillStyle = 'rgba(140,90,20,0.55)'; g.beginPath(); g.ellipse(262, 250, 70, 88, 0, 0, 7); g.fill(); g.beginPath(); g.moveTo(200, 240); g.lineTo(178, 270); g.lineTo(204, 276); g.fill(); g.beginPath(); g.ellipse(240, 330, 56, 40, 0.2, 0, 7); g.fill(); g.fillRect(232, 330, 70, 70);
  g.fillStyle = '#7a4a08'; g.font = '46px Pop'; g.textAlign = 'center'; g.textBaseline = 'middle'; const txt = name.split(''); const span = 2.4; txt.forEach((ch, i) => { const a = -Math.PI / 2 - span / 2 + span * (i + 0.5) / txt.length; g.save(); g.translate(256 + Math.cos(a) * 198, 256 + Math.sin(a) * 198); g.rotate(a + Math.PI / 2); g.fillText(ch, 0, 0); g.restore(); }); }); }
const goldSide = toon(0xd9a63a);
function makeMedal(name) { const g = new THREE.Group(); const ft = toon(0xffffff, { map: medalTex(name) }); const m = M(cyl(0.34, 0.34, 0.05, 48), [goldSide, ft, ft], { ol: 0.012, r: [Math.PI / 2, 0, 0], to: g }); m.rotation.y = Math.PI / 2; g.userData.sh = glow(g, 0.1, 0.1, 0.08, 0.5, 0); return g; }
const medals = [makeMedal('MAX v. LAUE'), makeMedal('JAMES FRANCK')]; medals.forEach(m => root.add(m));
const mbox = new THREE.Group(); root.add(mbox);
{ M(box(1.7, 0.22, 0.95), toon(0x6a1a2a), { ol: 0.015, p: [0, 0.11, 0], to: mbox }); M(box(1.56, 0.04, 0.82), toon(0xb02a3a), { p: [0, 0.22, 0], to: mbox, cast: false }); const lid = new THREE.Group(); lid.position.set(0, 0.22, -0.47); mbox.add(lid); M(box(1.7, 0.16, 0.95), toon(0x6a1a2a), { ol: 0.015, p: [0, 0.08, 0.47], to: lid }); M(box(1.56, 0.02, 0.82), toon(0xd8c8a8), { p: [0, -0.005, 0.47], to: lid, cast: false }); lid.rotation.x = -1.9; mbox.userData.lid = lid; }

// ---------------- Copenhagen canal street ----------------
const city = new THREE.Group(); root.add(city);
{ const water = ctex(256, 256, (g, w, h) => { g.fillStyle = '#3f6a8a'; g.fillRect(0, 0, w, h); g.strokeStyle = 'rgba(200,230,250,0.35)'; g.lineWidth = 3; for (let i = 0; i < 70; i++) { const x = rnd() * w, y = rnd() * h; g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + 10, y - 4, x + 22, y); g.stroke(); } }); city.userData.water = M(box(7, 0.1, 120), toon(0xffffff, { map: rep_(water, 2, 30) }), { p: [0, -0.6, -40], recv: true, to: city, cast: false });
  for (const s of [-1, 1]) { M(box(7, 0.4, 120), toon(0xffffff, { map: tc(T2s.cobble, 5, 70) }), { p: [s * 6.5, -0.2, -40], recv: true, to: city, cast: false }); M(box(0.5, 1.0, 120), toon(0xffffff, { map: tc(T2s.stone, 1, 40) }), { p: [s * 3.25, -0.5, -40], to: city, cast: false }); for (let z = 15; z > -95; z -= 4.5) { M(cyl(0.09, 0.09, 0.6, 8), toon(0x2a2430), { ol: 0.01, p: [s * 3.35, 0.3, z], to: city }); } }
  // gabled canal houses, Nyhavn colours
  const hc = ['#e8a83a', '#c8402f', '#3f6a9a', '#e8703a', '#f2d06a', '#5a9a8a', '#ece4d0', '#b05a3a', '#7a8ac0', '#d8b090'];
  function facade(col, seed, w, ht) { return ctex(256, 512, (g, W2, H2) => { let sd = seed; const r = () => (sd = (sd * 16807) % 2147483647) / 2147483647; g.fillStyle = col; g.fillRect(0, 0, W2, H2); for (let i = 0; i < 80; i++) { g.fillStyle = `rgba(80,50,30,${0.03 + r() * 0.04})`; g.beginPath(); g.ellipse(r() * W2, r() * H2, 10 + r() * 30, 5 + r() * 15, 0, 0, 7); g.fill(); } const cols = 3, rows = 4; for (let rr = 0; rr < rows; rr++) for (let c = 0; c < cols; c++) { const x = 30 + c * 76, y = 40 + rr * 104; g.fillStyle = '#f6f2ea'; g.fillRect(x - 6, y - 6, 52, 78); g.fillStyle = '#2a3a52'; g.fillRect(x, y, 40, 66); g.fillStyle = '#f6f2ea'; g.fillRect(x + 18, y, 4, 66); g.fillRect(x, y + 30, 40, 4); if (rr === 0) { g.fillStyle = 'rgba(255,255,255,0.4)'; g.fillRect(x - 8, y - 14, 56, 6); } } g.fillStyle = '#4a2e1c'; g.fillRect(100, 450, 56, 62); g.fillStyle = 'rgba(0,0,0,0.2)'; g.fillRect(0, 438, W2, 6); }); }
  let z = 12; let i = 0; while (z > -90) { for (const s of [-1, 1]) { const w = 3.4 + ((i * 7) % 5) * 0.25, ht = 8 + ((i * 13) % 5) * 0.8, col = hc[(i * 3 + (s > 0 ? 1 : 0)) % hc.length]; const h = new THREE.Group(); h.position.set(s * 12, 0, z - w / 2); h.rotation.y = -s * Math.PI / 2; city.add(h); const fm = toon(0xffffff, { map: facade(col, 11 + i * 2 + (s > 0 ? 1 : 0), w, ht) }), pm = toon(new THREE.Color(col).multiplyScalar(0.9));
      M(box(w, ht, 4), [pm, pm, pm, pm, fm, pm], { ol: 0.04, p: [0, ht / 2, 0], to: h }); const sh = new THREE.Shape(); if ((i + (s > 0 ? 1 : 0)) % 2) { const st = 3, sw = w / (2 * st + 1), sh0 = 0.7; sh.moveTo(-w / 2, 0); for (let k = 0; k < st; k++) { sh.lineTo(-w / 2 + k * sw, (k + 1) * sh0); sh.lineTo(-w / 2 + (k + 1) * sw, (k + 1) * sh0); } sh.lineTo(-w / 2 + st * sw, (st + 1) * sh0); sh.lineTo(w / 2 - st * sw, (st + 1) * sh0); for (let k = st - 1; k >= 0; k--) { sh.lineTo(w / 2 - (k + 1) * sw, (k + 1) * sh0); sh.lineTo(w / 2 - k * sw, (k + 1) * sh0); } sh.lineTo(w / 2, 0); } else { sh.moveTo(-w / 2, 0); sh.lineTo(0, 2.4); sh.lineTo(w / 2, 0); } sh.closePath();
      M(new THREE.ExtrudeGeometry(sh, { depth: 0.3, bevelEnabled: false }), pm, { ol: 0.03, p: [0, ht, 1.7], to: h }); const rf = new THREE.Shape(); rf.moveTo(-w / 2, 0); rf.lineTo(0, 2.2); rf.lineTo(w / 2, 0); rf.closePath(); M(new THREE.ExtrudeGeometry(rf, { depth: 3.6, bevelEnabled: false }), toon(0x7a3a2a), { ol: 0.03, p: [0, ht, -1.9], to: h }); M(box(0.5, 1.4, 0.5), toon(0x6b4636), { ol: 0.02, p: [w * 0.25, ht + 1.6, -0.5], to: h });
      // little shop awning on some ground floors
      if (i % 3 === 0) M(box(w * 0.7, 0.08, 0.9), toon(s > 0 ? 0x2f6b4a : 0xc8402f), { ol: 0.012, p: [0, 2.6, 2.35], r: [0.3, 0, 0], to: h }); }
    z -= 3.4 + ((i * 7) % 5) * 0.25 + 0.05; i++; }
  // boats with masts in the canal
  for (const [x, z, c] of [[-1.6, 2, 0x2f5a8a], [1.7, -8, 0xc8402f], [-1.4, -20, 0xece4d0], [1.5, -33, 0x2f6b4a], [-1.6, -46, 0xe8a83a]]) { const b = new THREE.Group(); b.position.set(x, -0.5, z); city.add(b); M(box(1.6, 0.6, 5.2), toon(c), { ol: 0.03, p: [0, 0.3, 0], to: b }); M(box(1.4, 0.1, 4.8), toon(0xffffff, { map: T2s.wood }), { p: [0, 0.62, 0], to: b, cast: false }); M(cyl(0.07, 0.09, 7, 8), toon(0x6b4326), { ol: 0.015, p: [0, 4, -0.5], to: b }); M(cyl(0.04, 0.04, 3, 6), toon(0x6b4326), { p: [0, 2.2, 0.8], r: [Math.PI / 2, 0, 0], to: b }); M(box(1.1, 0.8, 1.2), toon(0xece4d0), { ol: 0.02, p: [0, 1.0, 1.4], to: b }); }
  // street lamps
  for (let zz = 6; zz > -70; zz -= 11) for (const s of [-1, 1]) { const l = new THREE.Group(); l.position.set(s * 9.3, 0, zz); city.add(l); M(cyl(0.07, 0.1, 4, 8), toon(0x1b1522), { ol: 0.01, p: [0, 2, 0], to: l }); M(cyl(0.2, 0.28, 0.5, 6), toon(0x1b1522), { ol: 0.012, p: [0, 4.2, 0], to: l }); M(cyl(0.16, 0.16, 0.36, 6), flat(0xfff0c0), { p: [0, 4.15, 0], to: l, cast: false }); } }
// the tank: generic grey-green WWII-style, number on the turret, no insignia
const tank = new THREE.Group(); city.add(tank);
{ const tm = toon(0x5a6050), dm = toon(0x3f4438); const treadT = ctex(64, 256, (g, w, h) => { g.fillStyle = '#2a2a2a'; g.fillRect(0, 0, w, h); g.fillStyle = '#4a4a48'; for (let y = 0; y < h; y += 16) g.fillRect(0, y, w, 10); }); treadT.wrapS = treadT.wrapT = THREE.RepeatWrapping; treadT.repeat.set(1, 6); tank.userData.tread = treadT;
  M(box(3.0, 1.1, 6.4), tm, { ol: 0.04, p: [0, 1.45, 0], to: tank }); M(box(2.8, 0.8, 1.6), tm, { ol: 0.035, p: [0, 1.25, 3.4], r: [-0.5, 0, 0], to: tank }); M(box(3.6, 0.12, 6.6), dm, { ol: 0.02, p: [0, 2.0, 0], to: tank });
  for (const s of [-1, 1]) { M(box(0.7, 1.1, 6.8), toon(0xffffff, { map: treadT }), { ol: 0.03, p: [s * 1.6, 0.6, 0], to: tank }); for (let k = 0; k < 6; k++) { const w = M(cyl(0.42, 0.42, 0.3, 18), dm, { ol: 0.015, p: [s * 2.0, 0.55, -2.6 + k * 1.04], r: [0, 0, Math.PI / 2], to: tank }); M(cyl(0.18, 0.18, 0.32, 12), toon(0x8a8a80), { p: [0, 0, 0], to: w, cast: false }); } }
  const tur = new THREE.Group(); tur.position.set(0, 2.05, -0.4); tank.add(tur); tank.userData.tur = tur; M(cyl(1.3, 1.45, 1.0, 8), tm, { ol: 0.035, p: [0, 0.5, 0], to: tur }); M(cyl(0.6, 0.6, 0.3, 16), dm, { ol: 0.02, p: [0, 1.1, -0.3], to: tur }); M(cyl(0.12, 0.14, 3.2, 12), dm, { ol: 0.02, p: [0, 0.55, 2.6], r: [Math.PI / 2, 0, 0], to: tur }); M(box(0.6, 0.5, 0.4), tm, { ol: 0.02, p: [0, 0.55, 1.2], to: tur });
  const num = ftex(256, 128, g => { g.clearRect(0, 0, 256, 128); g.fillStyle = '#f2f2ea'; g.font = '96px Pop'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('121', 128, 70); }); for (const s of [-1, 1]) M(new THREE.PlaneGeometry(1.2, 0.6), flat(0xffffff, { map: num, transparent: true }), { p: [s * 1.38, 0.5, 0], r: [0, s * Math.PI / 2, 0], to: tur, cast: false });
  tank.userData.exh = []; }

// ---------------- characters ----------------
const helmet = hg => { const pts = []; for (let i = 0; i <= 14; i++) { const u = i / 14; pts.push(new THREE.Vector2(0.001 + Math.sin(u * Math.PI / 2) * 0.66, 0.62 - u * 0.62)); } pts.push(new THREE.Vector2(0.7, -0.08)); pts.push(new THREE.Vector2(0.82, -0.2)); M(new THREE.LatheGeometry(pts, 40), flat(0x4f5548, { side: THREE.DoubleSide }), { ol: 0.04, p: [0, 0.4, -0.06], s: [1.06, 0.88, 1.1], to: hg }); M(box(0.04, 0.3, 0.02), flat(0x2a2420), { p: [0.5, -0.2, 0.2], r: [0, 0, -0.3], to: hg, cast: false }); };
const hair = col => hg => M(new THREE.SphereGeometry(0.61, 36, 18, 0, Math.PI * 2, 0, Math.PI * 0.42), flat(col), { ol: 0.045, p: [0, 0.03, -0.06], r: [-0.42, 0, 0], to: hg });
const glasses = hg => { const m = flat(0x1b1522); for (const s of [-1, 1]) { M(new THREE.TorusGeometry(0.15, 0.022, 8, 24), m, { p: [s * 0.2, 0.08, 0.56], to: hg }); M(new THREE.CircleGeometry(0.14, 20), flat(0xdff0ff, { transparent: true, opacity: 0.18 }), { p: [s * 0.2, 0.08, 0.565], to: hg, cast: false }); M(box(0.2, 0.025, 0.025), m, { p: [s * 0.42, 0.1, 0.42], r: [0, s * 0.9, 0], to: hg }); } M(box(0.1, 0.025, 0.025), m, { p: [0, 0.1, 0.58], to: hg }); };
const both = (...fs) => hg => fs.forEach(f => f(hg));
const uniformBody = (g, w, h) => { g.fillStyle = '#5f6650'; g.fillRect(0, 0, w, h); g.fillStyle = '#4a5040'; g.fillRect(0, 0, w, h * 0.1); g.strokeStyle = '#3a4032'; g.lineWidth = 8; for (const s of [-1, 1]) { g.beginPath(); g.moveTo(w / 2 + s * 30, 0); g.lineTo(w / 2 + s * 4, h * 0.36); g.stroke(); g.strokeRect(w / 2 + s * 150 - 50, h * 0.3, 100, 70); g.strokeRect(w / 2 + s * 150 - 55, h * 0.66, 110, 90); } g.fillStyle = '#c8ccb8'; for (let i = 0; i < 4; i++) { g.beginPath(); g.arc(w / 2, h * (0.18 + i * 0.13), 12, 0, 7); g.fill(); } g.fillStyle = '#1b1522'; g.fillRect(0, h * 0.57, w, h * 0.06); };
const suitBody = (jacket, tie, bow) => (g, w, h) => { g.fillStyle = jacket; g.fillRect(0, 0, w, h); g.fillStyle = '#f6f4ee'; g.beginPath(); g.moveTo(w / 2 - 90, 0); g.lineTo(w / 2, h * 0.38); g.lineTo(w / 2 + 90, 0); g.fill(); g.fillStyle = tie; if (bow) { g.beginPath(); g.moveTo(w / 2, 40); g.lineTo(w / 2 - 70, 10); g.lineTo(w / 2 - 70, 70); g.closePath(); g.moveTo(w / 2, 40); g.lineTo(w / 2 + 70, 10); g.lineTo(w / 2 + 70, 70); g.closePath(); g.fill(); g.beginPath(); g.arc(w / 2, 40, 18, 0, 7); g.fill(); } else { g.beginPath(); g.moveTo(w / 2 - 22, 20); g.lineTo(w / 2 + 22, 20); g.lineTo(w / 2 + 30, h * 0.34); g.lineTo(w / 2, h * 0.4); g.lineTo(w / 2 - 30, h * 0.34); g.fill(); }
  g.strokeStyle = 'rgba(0,0,0,0.35)'; g.lineWidth = 8; for (const s of [-1, 1]) { g.beginPath(); g.moveTo(w / 2 + s * 90, 0); g.lineTo(w / 2 + s * 10, h * 0.45); g.lineTo(w / 2, h); g.stroke(); g.strokeRect(w / 2 + s * 170 - 50, h * 0.62, 100, 16); } g.fillStyle = '#1b1522'; for (let i = 0; i < 2; i++) { g.beginPath(); g.arc(w / 2 + 22, h * (0.55 + i * 0.12), 11, 0, 7); g.fill(); } g.fillStyle = '#f6f4ee'; g.fillRect(w / 2 + 130, h * 0.28, 60, 14); };
const coatBody = (g, w, h) => { g.fillStyle = '#eef0ee'; g.fillRect(0, 0, w, h); g.fillStyle = '#3a4a6a'; g.beginPath(); g.moveTo(w / 2 - 70, 0); g.lineTo(w / 2, h * 0.3); g.lineTo(w / 2 + 70, 0); g.fill(); g.fillStyle = '#8a2a2a'; g.beginPath(); g.moveTo(w / 2 - 18, 10); g.lineTo(w / 2 + 18, 10); g.lineTo(w / 2 + 24, h * 0.26); g.lineTo(w / 2, h * 0.3); g.lineTo(w / 2 - 24, h * 0.26); g.fill();
  g.strokeStyle = '#a8b0b8'; g.lineWidth = 10; for (const s of [-1, 1]) { g.beginPath(); g.moveTo(w / 2 + s * 70, 0); g.lineTo(w / 2 + s * 8, h * 0.36); g.lineTo(w / 2 + s * 8, h); g.stroke(); } g.strokeRect(w / 2 + 120, h * 0.28, 110, 90); g.fillStyle = '#2a5ab0'; g.fillRect(w / 2 + 140, h * 0.22, 12, 70); g.fillStyle = '#c8302a'; g.fillRect(w / 2 + 165, h * 0.24, 12, 60); g.fillStyle = '#c8ccd6'; for (let i = 0; i < 4; i++) { g.beginPath(); g.arc(w / 2 + 30, h * (0.42 + i * 0.13), 12, 0, 7); g.fill(); } g.strokeStyle = 'rgba(160,170,180,0.6)'; g.lineWidth = 5; g.strokeRect(w / 2 - 230, h * 0.62, 120, 110); g.fillStyle = 'rgba(240,138,42,0.35)'; g.beginPath(); g.ellipse(w / 2 - 260, h * 0.8, 26, 16, 0.4, 0, 7); g.fill(); };
const soldiers = [0, 1, 2].map(i => makeChar3({ shoe: 0x1b1522, belt3d: 0x1b1522, collar: 0x3a4032, arm: 0x4a5040, body: uniformBody, hat: helmet, stache: i === 1 }));
const hev = makeChar3({ stache: true, shoe: 0x2a1a12, collar: null, arm: 0xd8dcd8, body: coatBody, hat: both(hair(0x3a2a22), glasses) });
const laue = makeChar3({ stache: true, shoe: 0x1b1522, arm: 0x2a3552, body: suitBody('#2a3552', '#c8302a', true), hat: hair(0x6a6a6a) });
const franck = makeChar3({ shoe: 0x2a1a12, arm: 0x6a4a32, body: suitBody('#6a4a32', '#2f5a4a', false), hat: both(hair(0x2a2420), glasses) });
const CAST = [...soldiers, hev, laue, franck]; CAST.forEach(c => root.add(c.g));
// flashlight with a soft beam cone and a spot light
const flash = new THREE.Group(); root.add(flash);
{ M(cyl(0.07, 0.06, 0.42, 12), toon(0x2a2430), { ol: 0.01, p: [0, 0, 0], r: [Math.PI / 2, 0, 0], to: flash }); M(cyl(0.1, 0.07, 0.12, 14), toon(0x6a6a72), { ol: 0.01, p: [0, 0, 0.26], r: [Math.PI / 2, 0, 0], to: flash }); M(new THREE.CircleGeometry(0.09, 16), flat(0xfff6d0), { p: [0, 0, 0.325], to: flash, cast: false });
  const bm = new THREE.ConeGeometry(1.4, 6, 32, 1, true); bm.translate(0, -3, 0); bm.rotateX(-Math.PI / 2); flash.userData.beam = M(bm, new THREE.MeshBasicMaterial({ color: 0xfff2c0, transparent: true, opacity: 0.1, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }), { p: [0, 0, 0.33], to: flash, cast: false }); 
  const sl = new THREE.SpotLight(0xfff2c0, 40, 14, 0.32, 0.5, 1.2); sl.position.set(0, 0, 0.3); flash.add(sl); const tg = new THREE.Object3D(); tg.position.set(0, 0, 5); flash.add(tg); sl.target = tg; flash.userData.spot = sl; glow(flash, 0, 0, 0.36, 0.5, 0.9); }

// ---------------- explainer props (royal blue stage) ----------------
const xp = new THREE.Group(); root.add(xp);
const bigBeaker = new THREE.Group(); xp.add(bigBeaker);
{ M(cyl(1.3, 1.3, 2.8, 48, true), glassM(0xe8f6fa, 0.12), { ol: 0.04, p: [0, 1.4, 0], to: bigBeaker, cast: false }); M(new THREE.TorusGeometry(1.3, 0.06, 8, 48), glassM(0xe8f6fa, 0.7), { p: [0, 2.8, 0], r: [Math.PI / 2, 0, 0], to: bigBeaker, cast: false }); bigBeaker.userData.liq = M(cyl(1.24, 1.24, 2.0, 48), flat(0xf59a3a, { transparent: true, opacity: 0.9 }), { p: [0, 1.02, 0], to: bigBeaker, cast: false });
  bigBeaker.userData.sp = []; for (let i = 0; i < 60; i++) { const s = glow(bigBeaker, 0, 0, 0, 0.3, 0); s.userData.p = [(rnd() - 0.5) * 2, 0.15 + rnd() * 1.8, (rnd() - 0.5) * 2, rnd() * 6]; bigBeaker.userData.sp.push(s); } }
const bigMedal = makeMedal('THE NOBEL PRIZE'); xp.add(bigMedal);
const disguise = new THREE.Group(); bigMedal.add(disguise);
{ const m = flat(0x1b1522); for (const s of [-1, 1]) { M(new THREE.TorusGeometry(0.09, 0.016, 8, 20), m, { p: [s * 0.11, 0.07, 0.04], to: disguise }); M(new THREE.CircleGeometry(0.085, 16), flat(0xffffff), { p: [s * 0.11, 0.07, 0.035], to: disguise, cast: false }); M(sph(0.035, 10, 8), m, { p: [s * 0.11, 0.06, 0.045], to: disguise, cast: false }); M(box(0.12, 0.03, 0.03), m, { p: [s * 0.1, 0.17, 0.045], r: [0, 0, s * 0.2], to: disguise }); }
  M(sph(0.07, 12, 10), toon(0xf0b0a0), { ol: 0.01, p: [0, -0.03, 0.07], s: [1, 1.2, 1], to: disguise }); M(box(0.24, 0.05, 0.03), m, { ol: 0.006, p: [0, -0.12, 0.05], to: disguise }); }
const teacup = new THREE.Group(); xp.add(teacup);
{ const pts = []; for (let i = 0; i <= 16; i++) { const u = i / 16; pts.push(new THREE.Vector2(0.75 + 0.75 * Math.sin(u * Math.PI / 2), u * 1.5)); } M(new THREE.LatheGeometry(pts, 48), toon(0xf6f4ee, { side: THREE.DoubleSide }), { ol: 0.035, to: teacup }); M(cyl(1.0, 0.8, 0.12, 40), toon(0xf6f4ee), { ol: 0.02, p: [0, 0.02, 0], to: teacup });
  M(new THREE.TorusGeometry(0.42, 0.09, 12, 30, Math.PI * 1.2), toon(0xf6f4ee), { ol: 0.02, p: [1.6, 0.8, 0], r: [0, 0, -Math.PI * 0.6], to: teacup }); M(new THREE.TorusGeometry(1.48, 0.05, 8, 48), toon(0x2f6bd8), { p: [0, 1.36, 0], r: [Math.PI / 2, 0, 0], to: teacup, cast: false });
  teacup.userData.tea = M(cyl(1.42, 1.42, 0.06, 48), toon(0xa8642a), { p: [0, 1.32, 0], to: teacup, cast: false }); M(cyl(2.1, 1.6, 0.14, 48), toon(0xf6f4ee), { ol: 0.03, p: [0, -0.05, 0], to: teacup }); }
const sugar = M(box(0.42, 0.42, 0.42), toon(0xffffff), { ol: 0.015, to: xp }); { const t = ctex(64, 64, g => { g.fillStyle = '#ffffff'; g.fillRect(0, 0, 64, 64); g.fillStyle = 'rgba(200,210,230,0.6)'; for (let i = 0; i < 90; i++) g.fillRect(Math.random() * 64, Math.random() * 64, 3, 3); }); sugar.material.map = t; sugar.material.needsUpdate = true; }
const spoon = new THREE.Group(); xp.add(spoon); M(cyl(0.04, 0.05, 2.0, 10), toon(0xc8ccd6), { ol: 0.01, p: [0, 1.0, 0], to: spoon }); M(sph(0.16, 14, 10), toon(0xc8ccd6), { ol: 0.01, p: [0, 0, 0], s: [1, 0.35, 1.4], to: spoon });
// recasting: crucible of molten gold and a medal mould
const crucible = new THREE.Group(); xp.add(crucible); M(cyl(0.5, 0.36, 0.7, 24, true), toon(0x4a4a52, { side: THREE.DoubleSide }), { ol: 0.02, p: [0, 0.35, 0], to: crucible }); crucible.userData.melt = M(cyl(0.46, 0.46, 0.05, 24), flat(0xffb02e), { p: [0, 0.6, 0], to: crucible, cast: false }); glow(crucible, 0, 0.7, 0, 1.4, 0.8);
const pour = M(cyl(0.06, 0.04, 1, 10), flat(0xffc040), { to: xp, cast: false });
const mould = new THREE.Group(); xp.add(mould); M(box(2.4, 0.3, 1.2), toon(0x8a8a90), { ol: 0.02, to: mould }); mould.userData.fill = [-0.55, 0.55].map(x => M(cyl(0.38, 0.38, 0.05, 32), flat(0xffb02e), { p: [x, 0.14, 0], to: mould, cast: false }));

// ---------------- helpers ----------------
const SETS = [lab, city, xp, flash, mbox, ...medals, ...CAST.map(c => c.g)];
function hideAll() { SETS.forEach(g => g.visible = false); }
function hold(c, hand, obj, off = V(0, 0, 0), rot = [0, 0, 0]) { c.g.updateMatrixWorld(true); const p = V(...hand); c.up.localToWorld(p); obj.visible = true; obj.position.copy(p).add(off); obj.rotation.set(...rot); }
function aimFlash(c, hand, target, on = 1) { hold(c, hand, flash); flash.lookAt(target); flash.userData.spot.intensity = 40 * on; flash.userData.beam.material.opacity = 0.1 * on; }
function labLook(t, dark = 0) { lab.visible = true; root.fog = null; bg(0x2a2026); shadowBox(10, 60); light(lerp(0.85, 0.35, dark), lerp(2.0, 0.6, dark), [-16, 7, 3], 0xfff1dc, 0x5a4a44); sun.target.position.set(0, 1, 0); lampLights.forEach(l => l.intensity = lerp(6, 2.5, dark)); doorLight.intensity = 0; LOOK.grade = ['#ffc98a', 0.1 + 0.1 * dark]; LOOK.bloom = 0.18; }
function cityLook(t) { city.visible = true; bg(0xbcd4e8); root.fog = new THREE.Fog(0xc8d8e4, 30, 95); shadowBox(30, 120); light(0.8, 1.7, [18, 26, 12], 0xf0f4ff, 0x6a5a5a); sun.target.position.set(0, 0, -10); LOOK.grade = ['#c8d8ff', 0.1]; LOOK.bloom = 0.12; city.userData.water.material.map.offset.y = -t * 0.02; }
function xpLook() { xp.visible = true; root.fog = null; bg(0x2346c8); xp.children.forEach(c => c.visible = false); shadowBox(8, 40); light(0.95, 1.3, [4, 10, 9], 0xffffff, 0x8a9ae6); sun.target.position.set(0, 1, 0); LOOK.grade = ['#ffffff', 0.0]; LOOK.bloom = 0.1; }
// ===== extra assets for the rest of the story =====
jar.userData.home = jar.position.clone();
// gold settling at the bottom of the beaker, the pour stream, flying papers
beaker.userData.goldBed = M(cyl(0.355, 0.355, 0.04, 32), toon(0xffc83a), { p: [0, 0.03, 0], to: beaker, cast: false }); beaker.userData.goldBed.visible = false;
const pourS = M(cyl(0.025, 0.02, 1, 8), toon(0xf2d27a, { transparent: true, opacity: 0.85 }), { to: lab, cast: false }); pourS.visible = false;
const papers = []; for (let i = 0; i < 12; i++) { const p = M(new THREE.PlaneGeometry(0.42, 0.56), toon(0xf6f0dc, { side: THREE.DoubleSide }), { to: lab, cast: false }); p.visible = false; p.userData = { ph: rnd() * 6, dx: (rnd() - 0.5) * 2.4, dz: (rnd() - 0.5) * 1.6 }; papers.push(p); }
function beakerLevel(h, col) { const L = beaker.userData.liq; L.scale.y = Math.max(h, 0.001) / 0.55; L.position.y = h / 2 + 0.01; L.visible = h > 0.005; if (col !== undefined) L.material.color.set(col); }
function bubbles(t, on, h) { beaker.userData.bub.forEach(b => { const q = (t * 0.6 + b.userData.ph) % 1; b.visible = on > 0 && h > 0.05; b.position.set(b.userData.x * 0.9, 0.05 + q * Math.max(h - 0.08, 0.02), b.userData.z * 0.9); b.scale.setScalar(on); }); beaker.userData.fumes.forEach((f, i) => { const q = (t * 0.35 + i / 10) % 1; f.visible = on > 0; f.position.set(Math.sin(i * 2.1) * 0.2, 0.75 + q * 1.2, Math.cos(i * 1.7) * 0.15); const sc = 0.4 + q * 0.9; f.scale.set(sc, sc, 1); f.material.opacity = 0.45 * on * Math.sin(q * Math.PI); }); }
// ---- the yard behind the lab: lawn, brick wall with a loose patch, a dug hole ----
const yard = new THREE.Group(); root.add(yard); SETS.push(yard);
{ const grassT = ctex(256, 256, (g, w, h) => { g.fillStyle = '#6f9a48'; g.fillRect(0, 0, w, h); for (let i = 0; i < 900; i++) { g.strokeStyle = `rgba(${rnd() < 0.5 ? '60,100,40' : '150,190,90'},0.5)`; g.lineWidth = 2; const x = rnd() * w, y = rnd() * h; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (rnd() - 0.5) * 4, y - 6 - rnd() * 6); g.stroke(); } });
  M(box(40, 0.2, 40), toon(0xffffff, { map: rep_(grassT, 10, 10) }), { p: [0, -0.1, 0], recv: true, to: yard, cast: false });
  const bm = toon(0xffffff, { map: tc(T2s.brickW, 2, 1) }), bm2 = toon(0xffffff, { map: tc(T2s.brickW, 6, 2.5) });
  // wall with a 1.1 x 0.7 recess at x 1.2, y 1.4
  const HX = 1.2, HY = 1.4, HW = 1.1, HH = 0.7, WZ = -3;
  M(box(14, 4.4, 0.6), bm2, { p: [-5.75 + (HX - HW / 2 - 7) / 2 + 3.5, 2.2, WZ], s: [1, 1, 1], to: yard, recv: true }).visible = false;
  M(box(HX - HW / 2 + 7, 4.4, 0.6), toon(0xffffff, { map: tc(T2s.brickW, 3, 2.5) }), { ol: 0.02, p: [(-7 + HX - HW / 2) / 2, 2.2, WZ], recv: true, to: yard });
  M(box(7 - HX - HW / 2, 4.4, 0.6), toon(0xffffff, { map: tc(T2s.brickW, 3, 2.5) }), { ol: 0.02, p: [(7 + HX + HW / 2) / 2, 2.2, WZ], recv: true, to: yard });
  M(box(HW, HY - HH / 2, 0.6), bm, { p: [HX, (HY - HH / 2) / 2, WZ], recv: true, to: yard }); M(box(HW, 4.4 - HY - HH / 2, 0.6), bm, { p: [HX, (4.4 + HY + HH / 2) / 2, WZ], recv: true, to: yard });
  M(box(HW, HH, 0.1), toon(0x3a2620), { p: [HX, HY, WZ - 0.25], to: yard, cast: false }); M(box(14.4, 0.25, 0.8), toon(0x8a8478), { ol: 0.02, p: [0, 4.5, WZ], to: yard });
  yard.userData.hole = { x: HX, y: HY, z: WZ };
  yard.userData.loose = []; for (let r = 0; r < 3; r++) for (let c = 0; c < 4; c++) { const b = M(box(0.26, 0.21, 0.16), toon(new THREE.Color().setHSL(0.03 + rnd() * 0.03, 0.45, 0.38 + rnd() * 0.08)), { ol: 0.01, to: yard }); b.userData.home = V(HX - 0.4 + c * 0.27 + (r % 2) * 0.06 - 0.03, HY - 0.23 + r * 0.23, WZ + 0.24); b.userData.v = V((rnd() - 0.5) * 3, 1.5 + rnd() * 2.5, 2.5 + rnd() * 2.5); b.userData.w = V(rnd() * 8, rnd() * 8, rnd() * 8); yard.userData.loose.push(b); }
  // dirt patch with hole and mound
  M(cyl(1.5, 1.5, 0.04, 32), toon(0x7a5232), { p: [-3, 0.02, 0.5], recv: true, to: yard, cast: false }); M(cyl(0.7, 0.62, 0.05, 24), flat(0x2a1a12), { p: [-3, 0.04, 0.5], to: yard, cast: false }); M(sph(0.9, 16, 10), toon(0x8a5a34), { ol: 0.02, p: [-4.4, 0, 0.0], s: [1, 0.5, 1], to: yard });
  for (let i = 0; i < 16; i++) M(new THREE.DodecahedronGeometry(0.08 + rnd() * 0.08), toon(0x7a5232), { p: [-3 + (rnd() - 0.5) * 2.6, 0.05, 0.5 + (rnd() - 0.5) * 2.4], to: yard, cast: false });
  yard.userData.clods = []; for (let i = 0; i < 10; i++) { const c = M(new THREE.DodecahedronGeometry(0.1 + rnd() * 0.06), toon(0x6a4528), { to: yard, cast: false }); c.userData.v = V((rnd() - 0.5) * 2, 2.5 + rnd() * 1.5, (rnd() - 0.2) * 1.5); yard.userData.clods.push(c); }
  // bushes, a bench, a lantern on the wall, an old bicycle
  for (const [x, z, s] of [[-6, -2.2, 1.1], [5.6, -2.3, 1.2], [-6.6, 2.5, 0.9]]) for (let k = 0; k < 3; k++) M(sph(0.7 * s, 14, 10), toon([0x3f7a34, 0x4f8a3a, 0x6a9a40][k]), { ol: 0.02, p: [x + (k - 1) * 0.5 * s, 0.55 * s + (k % 2) * 0.3, z], to: yard });
  { const l = new THREE.Group(); l.position.set(-1.5, 3.0, WZ + 0.35); yard.add(l); M(box(0.3, 0.45, 0.3), toon(0x1b1522), { ol: 0.01, to: l }); M(box(0.22, 0.32, 0.22), flat(0xfff0c0), { to: l, cast: false }); }
  { const bk = new THREE.Group(); bk.position.set(4.2, 0, -2.3); bk.rotation.y = 0.15; yard.add(bk); for (const x of [-0.65, 0.65]) M(new THREE.TorusGeometry(0.42, 0.04, 8, 24), toon(0x1b1522), { p: [x, 0.44, 0], to: bk }); M(cyl(0.03, 0.03, 1.4, 6), toon(0x2f5a8a), { p: [0, 0.75, 0], r: [0, 0, 1.2], to: bk }); M(cyl(0.03, 0.03, 0.8, 6), toon(0x2f5a8a), { p: [0.35, 0.8, 0], r: [0, 0, -0.3], to: bk }); M(box(0.28, 0.06, 0.14), toon(0x3a2416), { p: [-0.2, 1.15, 0], to: bk }); } }
// box copy for the yard and a shovel and sledgehammer
const ybox = new THREE.Group(); yard.add(ybox); M(box(0.9, 0.22, 0.55), toon(0x6a1a2a), { ol: 0.015, p: [0, 0.11, 0], to: ybox }); M(box(0.9, 0.12, 0.55), toon(0x6a1a2a), { ol: 0.015, p: [0, 0.28, 0], to: ybox }); M(box(0.12, 0.08, 0.04), toon(0xd9b36a), { p: [0, 0.24, 0.28], to: ybox, cast: false });
const shovel = new THREE.Group(); root.add(shovel); SETS.push(shovel); M(cyl(0.035, 0.035, 1.9, 8), toon(0x7a5232), { ol: 0.01, p: [0, 0, 0], to: shovel }); M(box(0.36, 0.42, 0.04), toon(0x8a8a96), { ol: 0.012, p: [0, -1.15, 0.02], to: shovel }); M(box(0.3, 0.06, 0.06), toon(0x1b1522), { p: [0, 0.95, 0], to: shovel });
const hammer = new THREE.Group(); root.add(hammer); SETS.push(hammer); M(cyl(0.04, 0.04, 1.8, 8), toon(0x7a5232), { ol: 0.01, p: [0, -0.9, 0], to: hammer }); M(box(0.5, 0.26, 0.26), toon(0x4a4a52), { ol: 0.015, p: [0, -1.85, 0], to: hammer });
function yardLook() { yard.visible = true; root.fog = new THREE.Fog(0xc8d8e4, 30, 90); bg(0xb8cce0); shadowBox(12, 60); light(0.85, 1.7, [10, 18, 12], 0xf0f4ff, 0x6a5a5a); sun.target.position.set(0, 1, 0); LOOK.grade = ['#d8e0ff', 0.08]; LOOK.bloom = 0.1; }
// prison-bar overlay
function bars(t, t0) { const q = cl((t - t0) / 0.35); if (q <= 0) return; const y = -H + H * (q < 1 ? 1 - Math.pow(1 - q, 3) : 1) + Math.sin(Math.max(0, t - t0 - 0.35) * 18) * 12 * Math.exp(-Math.max(0, t - t0 - 0.35) * 6); ctx.save(); ctx.translate(0, y); for (let i = 0; i < 6; i++) { const x = 90 + i * 180; ctx.fillStyle = INK; ctx.fillRect(x - 24, 0, 48, H); ctx.fillStyle = '#5a5a66'; ctx.fillRect(x - 16, 0, 32, H); ctx.fillStyle = 'rgba(255,255,255,0.25)'; ctx.fillRect(x - 10, 0, 7, H); } ctx.fillStyle = INK; ctx.fillRect(0, 380, W, 46); ctx.fillStyle = '#5a5a66'; ctx.fillRect(0, 388, W, 30); ctx.restore(); }
function ring(p, t, t0, t1) { if (t < t0 || t > t1) return; const [x, y] = proj(p); const a = Math.min(1, (t - t0) / 0.2) * (1 - ss(t1 - 0.2, t1, t)); ctx.save(); ctx.globalAlpha = a; ctx.lineWidth = 16; ctx.strokeStyle = INK; ctx.beginPath(); ctx.arc(x, y, 95 + 6 * Math.sin(t * 8), 0, 7); ctx.stroke(); ctx.lineWidth = 9; ctx.strokeStyle = '#ffd34d'; ctx.stroke(); ctx.restore(); }
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
const headOf = c => c.headG.getWorldPosition(V(0, 0, 0));
const jarW = () => jar.getWorldPosition(V(0, 0, 0));
const CROSS = { lh: [0.3, 1.95, 0.5], rh: [-0.3, 1.9, 0.52] };
function medalsInBox(open = 1) { mbox.visible = true; mbox.position.set(3.25, 1.42, 2.1); mbox.rotation.set(0, -0.25, 0); mbox.userData.lid.rotation.x = lerp(0, -1.9, open); mbox.updateMatrixWorld(true); medals.forEach((m, i) => { m.visible = true; m.scale.setScalar(1); m.position.copy(mbox.localToWorld(V(i ? 0.42 : -0.42, 0.27, 0.02))); m.rotation.set(-Math.PI / 2, 0, -0.25 + (i ? 0.2 : -0.15)); }); }
function update(t) {
  hideAll(); overlay = () => { };
  let li = 0; for (let i = 0; i < Ls.length; i++) if (t >= CUT(i)) li = i;
  const s0 = CUT(li), s1 = li + 1 < Ls.length ? CUT(li + 1) : DUR, k = (t - s0) / (s1 - s0);
  const sub = (a, b) => cl((t - a) / (b - a));
  LOOK.grade = ['#ffc98a', 0.1]; LOOK.bloom = 0.14; LOOK.dof = null;
  const sol = soldiers[0];

  if (li === 0) { // HOOK: a soldier searches the lab for gold — and stares right at it
    labLook(t, 0.75); const ta = wf(0, 'and') - 0.1;
    if (t < ta) { const u = sub(0, ta), sx = lerp(1.9, 0.3, u); show(sol, sx, -4.0, Math.PI + 0.9); sol.face('angry'); const hd = [0.5, 2.15, 0.6]; sol.pose({ ...sol.walk(t * 5, 0.16), rh: hd, lh: [-0.5, 1.6, 0.1] });
      aimFlash(sol, hd, V(sx - 0.8 + Math.sin(t * 2.2) * 1.2, 2.2 + Math.sin(t * 1.7) * 0.8, SHZ));
      setCam([sx - 3.0, 2.6, -2.7], [sx - 0.5, 2.55, -4.7], 54, t, 0, 0.03);
      overlay = () => popText('GOLD?', W / 2, 260, 170, '#ffd34d', t, wf(0, 'gold') - 0.05, ta);
    } else { const u = sub(ta, s1); show(sol, -0.55, lerp(-4.2, -4.45, ss(0, 1, u)), Math.PI + 0.8); sol.face('think'); const hd = [0.5, 2.25, 0.6]; sol.pose({ rh: hd, lh: [-0.5, 1.6, 0.1], pitch: 0.06, hx: 0.02 }); aimFlash(sol, hd, jarW().add(V(0, 0.2, 0)));
      jar.userData.sp.forEach((s, i) => { s.material.opacity = 0.6 * Math.max(0, Math.sin(t * 5 + i * 1.7)); });
      setCam([lerp(-3.5, -3.1, u), 2.85, lerp(-3.9, -4.1, u)], [-1.0, 2.8, -5.0], 54, t, 0, -0.02); }
  }
  else if (li === 1) { // Copenhagen, 1940
    cityLook(t); tank.visible = false; const u = sub(s0, s1);
    setCam([0.6, lerp(10, 8, u), lerp(18, 15, u)], [0, lerp(3.5, 3, u), -30], 56, t, 0, 0.0);
    overlay = () => { popText('COPENHAGEN', W / 2, 250, 130, '#ffffff', t, s0 + 0.05, s1); popText('1940', W / 2, 400, 170, '#ffd34d', t, s0 + 0.25, s1); };
  }
  else if (li === 2) { // German tanks rolled into the city
    cityLook(t); tank.visible = true; const u = sub(s0, s1), tz = lerp(-16, -7, u); tank.position.set(6.4, 0, tz); tank.rotation.set(0, 0, 0.01 * Math.sin(t * 25)); tank.userData.tread.offset.y = tz * 0.6; tank.userData.tur.rotation.y = 0.15 * Math.sin(t * 0.8);
    setCam([4.3, 1.0, 2.5], [6.4, 2.3, tz], 54, t, 0.012, 0.06);
  }
  else if (li === 3) { // two gold Nobel Prizes, owned by scientists who defied Hitler
    labLook(t, 0.2); const to = wf(3, 'owned') - 0.1;
    if (t < to) { medalsInBox(1); medals.forEach((m, i) => m.userData.sh.material.opacity = 0.7 * Math.max(0, Math.sin(t * 3 + i * 2))); const u = sub(s0, to);
      setCam([lerp(3.0, 3.15, u), lerp(3.3, 2.85, u), lerp(4.2, 3.5, u)], [3.25, 1.6, 2.1], 46, t, 0, 0.03); LOOK.dof = [300, 1200, 3];
      overlay = () => { popText('TWO NOBEL', W / 2, 250, 120, '#ffffff', t, wf(3, 'two') - 0.05, to); popText('PRIZES', W / 2, 390, 160, '#ffd34d', t, wf(3, 'nobel') - 0.05, to); };
    } else { show(laue, 4.2, -4.0, 0.15); show(franck, 5.6, -3.9, -0.15); const td = wf(3, 'defied') - 0.1; [laue, franck].forEach((c, i) => { c.face(t > td ? 'angry' : 'neutral'); c.pose({ ...CROSS, hz: 0.04 * Math.sin(t * 2 + i) }); });
      const u = sub(to, s1); setCam([4.9, 2.4, lerp(1.2, 0.4, u)], [4.9, 2.6, -4], 48, t, 0, -0.03);
      overlay = () => popText('DEFIED', W / 2, 260, 170, '#ff7a30', t, td, s1); }
  }
  else lateShots(t, li, s0, s1, k, sub);
}
// ---------- lines 4–20 ----------
function resetLab() { jar.position.copy(jar.userData.home); jar.userData.sp.forEach(s => s.material.opacity = 0); acid.position.copy(acid.userData.home); acid.rotation.set(0, 0, 0); beakerLevel(0.0); bubbles(0, 0, 0); beaker.userData.goldBed.visible = false; pourS.visible = false; papers.forEach(p => p.visible = false); drawers.forEach(d => d.position.z = 0); door.rotation.y = 0; }
const _labLook0 = labLook; labLook = function (t, d) { _labLook0(t, d); resetLab(); };
function sweep(c, i, t, hd) { const tg = V(Math.sin(t * 1.3 + i * 2) * 3, 1.5 + Math.sin(t * 1.9 + i) * 1.2, -5.5); aimFlash(c, hd, tg); }
function lateShots(t, li, s0, s1, k, sub) {
  const sol = soldiers[0];
  if (li === 4) { // their names were engraved on the front
    labLook(t, 0.2); medalsInBox(1); const tf = wf(4, 'front') - 0.1, u = sub(s0, s1); const m = medals[ss(0, 1, sub(tf - 0.3, tf + 0.2)) > 0.5 ? 1 : 0]; const p = m.position;
    medals.forEach((mm, i) => mm.userData.sh.material.opacity = 0.6 * Math.max(0, Math.sin(t * 4 + i * 2)));
    const mp = medals[0].position.clone().lerp(medals[1].position, ss(0, 1, sub(s0 + 0.3, s1 - 0.2))); setCam([mp.x + 0.05, mp.y + 1.25, mp.z + 0.75], [mp.x, mp.y, mp.z - 0.02], 42, t, 0, lerp(0.08, -0.05, u)); LOOK.dof = [150, 700, 2];
    overlay = () => { popText('NAMES', W / 2, 250, 130, '#ffffff', t, wf(4, 'names') - 0.05, s1); popText('ENGRAVED', W / 2, 390, 150, '#ffd34d', t, wf(4, 'engraved') - 0.05, s1); };
  }
  else if (li === 5) { // if soldiers found them, both men were finished
    labLook(t, 0.4); const tb = wf(5, 'both') - 0.1;
    if (t < tb) { show(sol, 1.2, 0.6, 0.15); sol.face('sneaky'); const hd = [0.42, 2.75, 0.75]; sol.pose({ rh: hd, lh: [-0.4, 1.7, 0.2], hx: 0.08 }); hold(sol, hd, medals[0], V(0, 0.2, 0.06), [0, 0.15, 0]); medals[0].userData.sh.material.opacity = 0.6;
      const hp = headOf(sol); setCam([hp.x + 0.2, hp.y - 0.2, hp.z + lerp(4.2, 3.6, sub(s0, tb))], [hp.x + 0.15, hp.y - 0.25, hp.z], 46, t, 0, 0.04);
    } else { show(laue, 4.2, -4.0, 0.15); show(franck, 5.6, -3.9, -0.15); [laue, franck].forEach((c, i) => { c.face('shock'); c.pose({ rh: [0.6, 2.9, 0.4], lh: [-0.6, 2.9, 0.4], bob: 0.03 * Math.abs(Math.sin(t * 9 + i)) }); });
      setCam([4.9, 2.5, lerp(1.0, 0.6, sub(tb, s1))], [4.9, 2.7, -4], 48, t, 0, 0.02); const tbars = wf(5, 'finished') - 0.15;
      overlay = () => { bars(t, tbars); popText('FINISHED', W / 2, 300, 160, '#ff5a4a', t, tbars + 0.15, s1); }; }
  }
  else if (li === 6) { // bury them? soldiers dig.
    yardLook(); const ts = wf(6, 'soldiers') - 0.1, h = yard.userData; ybox.visible = true; const up = ss(0, 1, sub(ts + 0.35, ts + 0.7)); ybox.position.set(-3, lerp(-0.25, 0.4, up) + 0.25 * Math.sin(up * Math.PI), 0.5); ybox.rotation.set(0.4 * up, 0.3, 0.2 * up);
    if (t >= ts) { show(sol, -1.9, 1.6, -2.3); sol.face('angry'); const dig = ss(0, 1, sub(ts, ts + 0.35)); const hd = [0.3, lerp(2.6, 1.9, dig), 0.6]; sol.pose({ rh: hd, lh: [-0.1, lerp(2.0, 1.4, dig), 0.7], pitch: 0.25 * dig, lean: -0.05 }); hold(sol, hd, shovel, V(0, -0.2, 0), [-0.6 * dig - 0.3, -2.3, 0]);
      h.clods.forEach((c, i) => { const q = t - ts - 0.3; c.visible = q > 0 && q < 1.2; c.position.set(-3 + c.userData.v.x * q, Math.max(0.05, 0.1 + c.userData.v.y * q - 4.9 * q * q), 0.5 + c.userData.v.z * q); }); }
    else h.clods.forEach(c => c.visible = false);
    setCam([-0.9, 2.9, 6.6], [-2.6, 1.3, 0.5], 50, t, t > ts + 0.3 && t < ts + 0.6 ? 0.02 : 0, 0.03);
    overlay = () => popText('BURY?', W / 2, 260, 170, '#ffffff', t, s0 + 0.05, ts);
  }
  else if (li === 7) { // hide them in a wall? soldiers smash walls.
    yardLook(); const h = yard.userData, ts = wf(7, 'smash') - 0.05; ybox.visible = true; ybox.position.set(h.hole.x, h.hole.y - 0.3, h.hole.z + 0.05); ybox.rotation.set(0, 0, 0);
    h.loose.forEach((b, i) => { const q = t - ts; const p = b.userData.home; if (q < 0) { const ins = ss(0, 1, sub(s0 + 0.2 + i * 0.05, s0 + 0.5 + i * 0.05)); b.position.set(p.x, p.y, p.z + (1 - ins) * 0.8); b.visible = ins > 0; b.rotation.set(0, 0, 0); } else { b.visible = true; const v = b.userData.v; b.position.set(p.x + v.x * q, Math.max(0.1, p.y + v.y * q - 4.9 * q * q), p.z + v.z * q); b.rotation.set(b.userData.w.x * q, b.userData.w.y * q, b.userData.w.z * q); } });
    if (t > wf(7, 'soldiers') - 0.2) { show(sol, h.hole.x + 1.5, h.hole.z + 1.5, -2.4); sol.face('angry'); const sw = ss(0, 1, sub(ts - 0.35, ts)); const hd = [0.2, lerp(3.2, 2.0, sw), lerp(0.2, 0.8, sw)]; sol.pose({ rh: hd, lh: [0.0, lerp(2.9, 1.9, sw), lerp(0.2, 0.7, sw)], pitch: 0.2 * sw }); hold(sol, hd, hammer, V(0, 0, 0), [lerp(2.6, 1.2, sw), -2.6, 0]); }
    setCam([h.hole.x - 0.9, 2.5, h.hole.z + 6.6], [h.hole.x + 0.3, 1.8, h.hole.z], 50, t, t > ts && t < ts + 0.3 ? 0.03 : 0, -0.03);
    overlay = () => { popText('A WALL?', W / 2, 260, 150, '#ffffff', t, s0 + 0.05, ts - 0.1); burst('SMASH!', 540, 360, 220, t, ts, s1, -0.1); };
  }
  else if (li === 8) { // Then, a chemist named George de Hevesy grabbed a bottle of acid
    labLook(t, 0.1); const tg = wf(8, 'grabbed') - 0.1;
    if (t < tg) { show(hev, 3.55, 0.55, -0.25); hev.face(t > wf(8, 'george') ? 'sneaky' : 'think'); hev.pose({ rh: [0.35, 2.75, 0.55], lh: [-0.45, 1.9, 0.5], hz: 0.05 * Math.sin(t * 2) }); medalsInBox(1);
      setCam([lerp(2.7, 2.9, sub(s0, tg)), 2.25, lerp(5.6, 5.0, sub(s0, tg))], [3.45, 2.2, 1.2], 46, t, 0, 0.03);
    } else { const turn = ss(0, 1, sub(tg + 0.35, tg + 0.95)); show(hev, 1.75, -4.45, lerp(Math.PI, 2 * Math.PI - 0.5, turn)); hev.face('sneaky'); const hd = turn > 0.01 ? [0.42, 2.3, 0.7] : [0.3, 2.1, 0.95]; hev.pose({ rh: hd, lh: [-0.45, 1.9, 0.3] }); if (t > tg + 0.15) hold(hev, hd, acid, V(0, -0.4, 0), [0, 0, 0]);
      setCam([0.3, 2.5, -1.6], [1.6, 2.2, -4.9], 50, t, 0, 0.03); }
  }
  else if (li === 9) { // aqua regia, one of the few liquids that can eat gold — he pours it into the beaker
    labLook(t, 0.1); show(hev, -0.1, -2.5, 0); hev.face(t > wf(9, 'eat') ? 'sneaky' : 'think'); const pour = ss(0, 1, sub(s0 + 0.2, s0 + 0.7)); acid.position.set(0.45, 2.75, -1.6); acid.rotation.set(0, 0, lerp(0.2, 1.9, pour)); hev.pose({ rh: [0.15, 3.0, 0.95], lh: [-0.3, 2.0, 0.6] });
    const lv = 0.05 + 0.45 * sub(s0 + 0.6, s1); beakerLevel(lv, 0xf2d27a); bubbles(t, 0.4, lv); if (pour > 0.95) { const mouth = V(0.45 - 0.86 * Math.sin(1.9), 2.75 + 0.86 * Math.cos(1.9), -1.6); const sy = 1.44 + lv; pourS.visible = true; pourS.position.set(mouth.x, (mouth.y + sy) / 2, -1.6); pourS.scale.set(1, mouth.y - sy, 1); }
    setCam([0.7, 2.6, lerp(1.1, 0.7, k)], [-0.2, 2.25, -1.8], 46, t, 0, 0.03);
    overlay = () => { popText('EATS', W / 2, 250, 130, '#ffffff', t, wf(9, 'eat') - 0.05, s1); popText('GOLD', W / 2, 390, 170, '#ffd34d', t, wf(9, 'gold') - 0.05, s1); };
  }
  else if (li === 10) { // he dropped both medals in, and watched them disappear
    labLook(t, 0.1); show(hev, -0.35, -2.75, 0); const ta = wf(10, 'and') - 0.1, td = s0 + 0.35; hev.face(t > ta ? 'shock' : 'neutral'); hev.pose({ rh: [0.25, 2.6, 0.6], lh: [-0.25, 2.6, 0.6], hx: 0.15 });
    const dis = ss(0, 1, sub(ta, s1 - 0.15)); beakerLevel(0.5, new THREE.Color(0xf2d27a).lerp(new THREE.Color(0xf08a2a), dis)); bubbles(t, 0.4 + 0.8 * dis, 0.5);
    medals.forEach((m, i) => { m.visible = dis < 0.99; const q = cl((t - td - i * 0.12) / 0.45); const y = q < 1 ? lerp(2.8, 1.6, q * q) : lerp(1.6, 1.49, sub(td + 0.6, ta + 0.6)); m.position.set(-0.35 + (i ? 0.1 : -0.1), y, -1.55 + (i ? 0.05 : -0.05)); m.rotation.set(-Math.PI / 2 + (q < 1 ? q * 2.5 : 0.3), i * 0.6, 0.2); m.scale.setScalar(Math.max(0.001, 0.72 * (1 - dis))); m.userData.sh.material.opacity = 0; });
    if (t < ta) setCam([-0.1, 2.75, 0.4], [-0.35, 2.0, -1.6], 44, t, 0, 0.02);
    else setCam([-0.35, 2.05, lerp(-0.35, -0.55, sub(ta, s1))], [-0.35, 1.85, -1.6], 44, t, 0, -0.02);
    overlay = () => burst('PLOP!', 540, 340, 200, t, td + 0.4, td + 1.0, 0.08);
  }
  else if (li === 11) { // an orange liquid, in a jar, on a shelf
    labLook(t, 0.15); const tj = wf(11, 'in') - 0.1, ts = wf(11, 'on', 1) - 0.1; medals.forEach(m => { m.visible = false; m.scale.setScalar(1); });
    if (t < tj) { beakerLevel(0.5, 0xf08a2a); bubbles(t, 0.3, 0.5); setCam([-0.35, 2.15, lerp(0.2, -0.3, sub(s0, tj))], [-0.35, 1.75, -1.6], 44, t, 0, 0.03); }
    else if (t < ts) { beakerLevel(0.0); jar.position.set(-1.0, 1.44, -1.35); jar.userData.sp.forEach((s, i) => s.material.opacity = 0.4 * Math.max(0, Math.sin(t * 5 + i))); show(hev, -1.0, -2.6, 0); hev.face('happy'); hev.pose({ rh: [0.3, 2.0, 0.7], lh: [-0.3, 2.0, 0.7] }); setCam([-0.9, 2.2, 0.0], [-1.0, 1.75, -1.4], 40, t, 0, -0.02); }
    else { const u = ss(0, 1, sub(ts, s1)), jp = jarW(); jar.userData.sp.forEach((s, i) => s.material.opacity = 0.4 * Math.max(0, Math.sin(t * 5 + i))); setCam([lerp(jp.x + 0.1, -1.6, u), lerp(jp.y + 0.35, 2.6, u), lerp(jp.z + 1.3, 3.6, u)], [lerp(jp.x, -1.6, u), lerp(jp.y + 0.2, 2.4, u), -5.5], lerp(40, 58, u), t, 0, 0.0);
      overlay = () => ring(jarW().add(V(0, 0.22, 0)), t, ts + 0.1, s1); }
  }
  else if (li === 12) { // the soldiers came
    labLook(t, 0.8); const op = ss(0, 1, sub(s0 + 0.05, s0 + 0.3)); door.rotation.y = -1.5 * op; doorLight.intensity = 30 * op;
    soldiers.forEach((c, i) => { const x = lerp(8.4, 6.0, sub(s0 + 0.2 + i * 0.15, s1)) + i * 0.9; show(c, x, 3.0 + (i - 1) * 0.55, -Math.PI / 2); c.face('angry'); const hd = [0.5, 2.15, 0.6]; c.pose({ ...c.walk(t * 6 + i, 0.2), rh: hd, lh: [-0.5, 1.6, 0.1] }); if (i === 0) aimFlash(c, hd, V(0, 1.5, 3)); });
    setCam([2.2, 2.3, 3.8], [7, 2.1, 3.0], 52, t, t < s0 + 0.4 ? 0.03 : 0, 0.04);
    overlay = () => burst('BANG!', 540, 340, 200, t, s0 + 0.08, s0 + 0.75, -0.1);
  }
  else if (li === 13) { // they opened every drawer
    labLook(t, 0.6); doorLight.intensity = 20; door.rotation.y = -1.5;
    drawers.forEach((d, i) => { const order = [4, 7, 1, 10, 3, 9, 0, 6, 11, 2, 8, 5].indexOf(i); d.position.z = 0.6 * ss(0, 1, sub(s0 + 0.05 + order * 0.11, s0 + 0.2 + order * 0.11)); });
    papers.forEach((p, i) => { const q = t - s0 - 0.2 - i * 0.08; p.visible = q > 0; if (q <= 0) return; p.position.set(LX - 1.2 - q * 1.6 + p.userData.dx * q * 0.5, 1.8 + 2.2 * q - 2.0 * q * q + 0.1 * Math.sin(t * 5 + i), -2.4 + p.userData.dz * q); p.rotation.set(t * 3 + i, t * 2 + i * 0.5, i); });
    [[1, 5.0, -3.6], [2, 5.1, -1.1]].forEach(([j, x, z], n) => { const c = soldiers[j]; show(c, x, z, Math.PI / 2 - (n ? -0.7 : 0.7)); c.face('angry'); c.pose({ rh: [0.5, 1.9 + 0.3 * Math.sin(t * 8 + n), 0.8], lh: [-0.4, 2.2 + 0.3 * Math.cos(t * 8 + n), 0.8], lean: 0.05 * Math.sin(t * 8 + n) }); });
    setCam([1.0, 2.9, -2.0], [6.0, 1.7, -2.4], 56, t, 0, -0.03);
  }
  else if (li === 14) { // they looked right at the jar, and walked away
    labLook(t, 0.75); const tw = wf(14, 'walked') - 0.25, turn = ss(0, 1, sub(tw, tw + 0.4)); const z = -4.4 + 1.2 * ss(0, 1, sub(tw + 0.2, s1)); show(sol, -0.55 + 0.8 * ss(0, 1, sub(tw + 0.2, s1)), z, lerp(Math.PI + 0.8, 0.4, turn)); sol.face(t < tw ? 'think' : 'neutral'); const hd = [0.5, 2.25, 0.6]; sol.pose({ ...(turn > 0.5 ? sol.walk(t * 5, 0.18) : {}), rh: hd, lh: [-0.5, 1.6, 0.1] }); aimFlash(sol, hd, turn < 0.5 ? jarW().add(V(0, 0.2, 0)) : V(3, 1, 4), 1 - turn);
    jar.userData.sp.forEach((s, i) => { s.material.opacity = 0.5 * Math.max(0, Math.sin(t * 5 + i * 1.7)); });
    show(hev, -3.3, -0.2, 0.5); hev.face(turn > 0.6 ? 'happy' : 'sneaky'); hev.pose({ rh: [0.3, 1.95, 0.5], lh: [-0.3, 1.95, 0.5] });
    setCam([lerp(-3.3, -3.0, k), 2.85, lerp(-4.0, -4.2, k)], [-1.0, 2.8, -5.0], 54, t, 0, -0.02);
  }
  // ---------- "You see," explainer on royal blue ----------
  else if (li === 15) { xpLook(); bigBeaker.visible = true; bigBeaker.position.set(0, -0.6, 0); bigBeaker.rotation.y = t * 0.2;
    bigBeaker.userData.sp.forEach((s, i) => { const [x, y, z, ph] = s.userData.p; const a = t * 0.8 + ph; s.position.set(Math.cos(a) * Math.hypot(x, z) * 0.55, y + 0.1 * Math.sin(t * 2 + ph), Math.sin(a) * Math.hypot(x, z) * 0.55); s.material.opacity = 0.9 * Math.max(0, Math.sin(t * 4 + ph * 3)); s.material.color.set(0xffe070); });
    setCam([0, 1.5, lerp(6.6, 5.9, k)], [0, 0.85, 0], 45, t, 0, 0.02);
    overlay = () => { popText('YOU SEE,', W / 2, 260, 130, '#ffffff', t, s0 + 0.05, wf(15, 'the') - 0.1); popText('NEVER', W / 2, 250, 120, '#ffffff', t, wf(15, 'never') - 0.05, s1); popText('LEFT', W / 2, 390, 170, '#ffd34d', t, wf(15, 'left') - 0.05, s1); };
  }
  else if (li === 16) { xpLook(); bigMedal.visible = true; const tsd = wf(16, 'stopped') - 0.05, d = ss(0, 1, sub(tsd, tsd + 0.25)); bigMedal.position.set(0, 1.0 + 0.05 * Math.sin(t * 3), 0); bigMedal.scale.setScalar(4.2); bigMedal.rotation.set(0, 0.25 * Math.sin(t * 1.5), 0.08 * Math.sin(t * 2)); disguise.visible = d > 0.01; disguise.scale.setScalar(Math.max(0.001, d * (1 + 0.15 * Math.sin(Math.max(0, t - tsd) * 14) * Math.exp(-Math.max(0, t - tsd) * 4)))); bigMedal.userData.sh.material.opacity = 0.5;
    setCam([0, 1.1, lerp(7.2, 6.6, k)], [0, 1.0, 0], 45, t, 0, -0.02);
    overlay = () => popText('IN DISGUISE', W / 2, 260, 140, '#ffd34d', t, tsd + 0.15, s1);
  }
  else if (li === 17) { xpLook(); teacup.visible = true; teacup.position.set(0, -0.6, 0); teacup.rotation.y = -0.3; const tsg = wf(17, 'sugar') - 0.1, dl = ss(0, 1, sub(wf(17, 'still') - 0.4, wf(17, 'there'))); const fq = cl((t - tsg) / 0.45);
    sugar.visible = dl < 0.99; sugar.position.set(0.2, fq < 1 ? lerp(3.4, 0.8, fq * fq) : 0.7 - 0.12 * dl, 0.1); sugar.rotation.set(fq * 1.5, fq * 0.8, 0.3); sugar.scale.setScalar(Math.max(0.001, 1 - dl));
    spoon.visible = t > tsg + 0.5; const a = t * 5; spoon.position.set(0.45 * Math.cos(a), 0.65, 0.45 * Math.sin(a)); spoon.rotation.set(0.25 * Math.sin(a), 0, 0.25 * Math.cos(a));
    teacup.userData.tea.material.color.set(new THREE.Color(0xa8642a).lerp(new THREE.Color(0xb87a3a), 0.3 * Math.sin(t * 3) * dl));
    setCam([0, lerp(3.4, 3.7, k), lerp(8.0, 7.2, k)], [0, 0.5, 0], 45, t, 0, 0.02);
    overlay = () => { popText('SUGAR', W / 2, 250, 130, '#ffffff', t, wf(17, 'sugar') - 0.05, s1); popText('IN TEA', W / 2, 390, 160, '#ffd34d', t, wf(17, 'tea') - 0.05, s1); if (t > tsg + 0.42 && t < tsg + 0.9) burst('PLOP!', 300, 700, 140, t, tsg + 0.42, tsg + 0.9, 0.1); };
  }
  else if (li === 18) { // after the war: gold back out, recast into new medals
    const tn = wf(18, 'and') - 0.1;
    if (t < tn) { labLook(t, 0.0); light(1.0, 2.4, [-16, 7, 3], 0xfff6e0, 0x5a4a44); show(hev, -0.35, -2.75, 0); hev.face('happy'); hev.pose({ rh: [0.3, 2.2, 0.7], lh: [-0.3, 2.2, 0.7] }); const g = ss(0, 1, sub(s0 + 0.3, tn)); beakerLevel(0.5, new THREE.Color(0xf08a2a).lerp(new THREE.Color(0xf6eedc), g)); beaker.userData.goldBed.visible = true; beaker.userData.goldBed.scale.y = 0.2 + 2.5 * g; beaker.userData.goldBed.position.y = 0.02 + 0.05 * g; bubbles(t, 0, 0);
      setCam([-0.2, 2.7, lerp(1.6, 1.0, sub(s0, tn))], [-0.35, 2.15, -1.9], 44, t, 0, 0.03);
      overlay = () => { popText('AFTER', W / 2, 250, 130, '#ffffff', t, s0 + 0.05, tn); popText('THE WAR', W / 2, 390, 160, '#ffd34d', t, s0 + 0.2, tn); };
    } else { xpLook(); bg(0x2a1a1c); crucible.visible = mould.visible = true; const tb = wf(18, 'brand') - 0.1; const pq = ss(0, 1, sub(tn, tn + 0.3)); crucible.position.set(-1.2, 1.4 + 0.3 * pq, 0); crucible.rotation.set(0, 0, -1.1 * pq); mould.position.set(0.3, 0, 0);
      pour.visible = pq > 0.9 && t < tb; pour.position.set(-0.55, 0.85, 0); pour.scale.set(1, 1.3, 1); pour.rotation.set(0, 0, 0.15); const fl = ss(0, 1, sub(tn + 0.3, tb)); mould.userData.fill.forEach((f, i) => { f.scale.set(1, 1, 1); f.material.color.set(new THREE.Color(0xffb02e).lerp(new THREE.Color(0xffd84a), ss(0, 1, sub(tb, tb + 0.4)))); f.visible = fl > i * 0.4; });
      const rise = ss(0, 1, sub(tb, tb + 0.5)); medals.forEach((m, i) => { m.visible = rise > 0; m.scale.setScalar(1.4); m.position.set(0.3 + (i ? 0.55 : -0.55), 0.2 + 1.4 * rise, 0.1); m.rotation.set(0, Math.sin(t * 2 + i) * 0.3, 0); m.userData.sh.material.opacity = 0.9 * rise; });
      setCam([0, 1.8, lerp(6.6, 5.8, sub(tn, s1))], [-0.2, 0.9, 0], 45, t, 0, 0.02); LOOK.bloom = 0.3;
      overlay = () => { popText('BRAND', W / 2, 250, 130, '#ffffff', t, tb, s1); popText('NEW', W / 2, 390, 170, '#ffd34d', t, tb + 0.1, s1); }; }
  }
  else if (li === 19) { // the Nazis were hunting for gold
    labLook(t, 0.85); door.rotation.y = -1.5; doorLight.intensity = 15;
    soldiers.forEach((c, i) => { const x = [-1.1, 0.7, 2.1][i], z = [0.6, -0.9, 0.3][i]; show(c, x + 0.3 * Math.sin(t * 0.8 + i), z, 0.9 * Math.sin(t * 0.7 + i * 2)); c.face('angry'); const hd = [0.5, 2.15, 0.6]; c.pose({ ...c.walk(t * 4 + i * 2, 0.12), rh: hd, lh: [-0.5, 1.6, 0.1] }); });
    hold(soldiers[1], [0.5, 2.15, 0.6], flash); flash.userData.spot.intensity = 40; flash.userData.beam.material.opacity = 0.1; flash.lookAt(V(Math.sin(t * 1.3) * 4, 0.6, 3));
    setCam([lerp(0.0, 0.6, k), 3.0, 6.8], [0.5, 2.3, -2], 54, t, 0, 0.0);
    overlay = () => { popText('HUNTING', W / 2, 250, 130, '#ffffff', t, wf(19, 'hunting') - 0.05, s1); popText('FOR GOLD', W / 2, 390, 150, '#ffd34d', t, wf(19, 'gold') - 0.05, s1); };
  }
  else if (li === 20) { // it sat on a shelf the whole time
    labLook(t, 0.55); const u = ss(0, 1, sub(s0, DUR - 0.3)), jp = jarW(); jar.userData.sp.forEach((s, i) => s.material.opacity = (0.3 + 0.5 * u) * Math.max(0, Math.sin(t * 5 + i * 1.7)));
    setCam([lerp(-1.6, jp.x + 0.05, u), lerp(2.7, jp.y + 0.3, u), lerp(-1.6, jp.z + 1.25, u)], [jp.x, jp.y + 0.22, jp.z], lerp(54, 40, u), t, 0, 0.0); LOOK.dof = [250, 1200, 2.5 * u];
    overlay = () => { popText('THE WHOLE', W / 2, 250, 120, '#ffffff', t, wf(20, 'whole') - 0.1, DUR); popText('TIME', W / 2, 390, 170, '#ffd34d', t, wf(20, 'time') - 0.05, DUR); };
  }
  else bg(0x111111);
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
