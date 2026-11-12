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
let TM, Ls, DUR = 68;
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
// ===== The Girl Who Outsmarted a Greedy King With a String — cast and sets =====
const FT = []; function ftex(w, h, d) { const t = ctex(w, h, d); t.userData.draw = d; FT.push(t); return t; }
window.afterFonts = () => FT.forEach(t => { t.userData.draw(t.userData.g, t.userData.c.width, t.userData.c.height); t.needsUpdate = true; });
// long shadows are the story: widen the shadow camera
Object.assign(sun.shadow.camera, { left: -16, right: 16, top: 16, bottom: -6, near: 0.5, far: 70 }); sun.shadow.camera.updateProjectionMatrix(); sun.shadow.mapSize.set(4096, 4096); sun.shadow.bias = -0.0008;

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

const king = makeChar3({ beard: '#d9d4c8', wrinkles: true, shoe: 0x6a2f1a, body: bodyTex('#b3272d', '#ffd34d', { ermine: true, belt: '#6a2f1a' }), hat: crownHat });
const collector = makeChar3({ stache: true, shoe: 0x2a2530, body: bodyTex('#2f6b4f', '#1b1522', { belt: '#3a2416', buttons: true }), hat: capHat(0x1f3a2f) });
const collector2 = makeChar3({ shoe: 0x2a2530, body: bodyTex('#5a4a8a', '#1b1522', { belt: '#3a2416', buttons: true }), hat: capHat(0x3a2f5a) });
const tallMan = makeChar3({ stache: true, shoe: 0x2a2530, body: bodyTex('#7a4a2c', '#3a2416', { belt: '#2a2530', buttons: true }), hat: tallHat });
const townA = makeChar3({ shoe: 0x3a2416, body: bodyTex('#c98a2a', '#7a4a1c', { apron: true }), hat: hoodHat(0xd9b36a) });
const townB = makeChar3({ beard: '#8a8f99', wrinkles: true, shoe: 0x3a2416, body: bodyTex('#3f8f8a', '#1f5450', { stripes: true }), hat: hoodHat(0x57b0aa) });
const townC = makeChar3({ freckles: true, shoe: 0x3a2416, body: bodyTex('#b0567a', '#6e2f48', { belt: '#3a2416' }), hat: hoodHat(0xd9869f) });
const girl = makeChar3({ freckles: true, shoe: 0x6a2f1a, body: bodyTex('#f2c230', '#b3272d', { apron: true }), hat: braidHair });
const CAST = [king, collector, collector2, tallMan, townA, townB, townC, girl]; CAST.forEach(c => root.add(c.g));

// ---------- town square at the foot of the palace ----------
const town = new THREE.Group(); root.add(town);
const PAL_Z = -16, BALC = { x: 0, y: 6.2, z: PAL_Z + 3.0 }, TOWER = { x: 3.6, z: PAL_Z - 2, h: 22 };
TX.cobble2 = rep_(ctex(256, 256, (g, w, h) => { g.fillStyle = '#8a7a66'; g.fillRect(0, 0, w, h); let sd = 13; const r = () => (sd = (sd * 16807) % 2147483647) / 2147483647; for (let y = 0; y < h; y += 32) for (let x = (y / 32 % 2) * 20 - 40; x < w; x += 40) { g.fillStyle = `hsl(${30 + r() * 20},${18 + r() * 10}%,${52 + r() * 16}%)`; g.beginPath(); g.ellipse(x + 20, y + 16, 17, 13, 0, 0, 7); g.fill(); g.strokeStyle = 'rgba(40,30,20,0.35)'; g.lineWidth = 2; g.stroke(); } }), 12, 12);
TX.stone = rep_(ctex(256, 256, (g, w, h) => { g.fillStyle = '#c9b89a'; g.fillRect(0, 0, w, h); let sd = 7; const r = () => (sd = (sd * 16807) % 2147483647) / 2147483647; for (let y = 0; y < h; y += 42) for (let x = (y / 42 % 2) * 40 - 80; x < w; x += 80) { g.fillStyle = `hsl(${36 + r() * 10},${24 + r() * 10}%,${66 + r() * 10}%)`; g.fillRect(x + 3, y + 3, 74, 36); } }), 4, 6);
const tower = new THREE.Group(); town.add(tower);
{
  M(box(70, 0.2, 70), toon(0xffffff, { map: TX.cobble2 }), { p: [0, -0.1, -10], recv: true, to: town, cast: false });
  // houses on both sides, same build as the London street but warmer plaster
  const roofM = toon(0x9a4a3a), cols = ['#f1dfb4', '#e8cfa0', '#f4e4c2', '#e2c594'];
  for (let i = 0; i < 4; i++) for (const s of [-1, 1]) { const h = new THREE.Group(), ht = 5.0 + ((i * 7 + (s > 0 ? 3 : 0)) % 3) * 0.6, z = 6 - i * 5.2; h.position.set(s * 7.2, 0, z); town.add(h); const tex = houseTex(21 + i * 3 + (s > 0 ? 50 : 0), cols[(i + (s > 0 ? 1 : 0)) % 4]); const m = toon(0xffffff, { map: tex }); M(box(4.6, ht, 4.6), [m, m, roofM, roofM, m, m], { ol: 0.04, p: [0, ht / 2, 0], to: h }); const tri = new THREE.Shape(); tri.moveTo(-2.6, 0); tri.lineTo(2.6, 0); tri.lineTo(0, 2.3); tri.closePath(); const roof = M(new THREE.ExtrudeGeometry(tri, { depth: 5.0, bevelEnabled: false }), roofM, { ol: 0.04, to: h }); roof.position.set(0, ht, -2.5); M(box(0.6, 1.5, 0.6), toon(0x6b4636), { ol: 0.03, p: [s * 1.2, ht + 1.6, -0.6], to: h }); }
  // palace: wide stone front with a balcony, arched door, flags, tall tower
  const stone = toon(0xffffff, { map: TX.stone });
  M(box(24, 9, 6), stone, { ol: 0.05, p: [0, 4.5, PAL_Z], recv: true, to: town }); M(box(25, 0.8, 7), toon(0x6a2f3a), { ol: 0.04, p: [0, 9.4, PAL_Z], to: town });
  for (let i = -3; i <= 3; i++) M(box(1.6, 1.2, 1.4), stone, { ol: 0.035, p: [i * 3.4, 10.3, PAL_Z], to: town });
  M(box(3.0, 4.6, 0.3), toon(0x4a2e1c), { ol: 0.04, p: [-5.5, 2.3, PAL_Z + 3.0], to: town }); M(cyl(1.5, 1.5, 0.3, 24, false, 0, Math.PI), toon(0x4a2e1c), { ol: 0.04, p: [-5.5, 4.6, PAL_Z + 3.0], r: [Math.PI / 2, 0, 0], to: town });
  for (const x of [-9, 9]) for (const y of [3, 7]) { M(box(1.3, 1.9, 0.3), toon(0x3d2718), { ol: 0.035, p: [x, y, PAL_Z + 3.0], to: town }); M(box(1.0, 1.6, 0.32), flat(0x31405e), { p: [x, y, PAL_Z + 3.0], to: town, cast: false }); }
  // balcony
  M(box(6.0, 0.5, 2.6), stone, { ol: 0.04, p: [BALC.x, BALC.y - 0.25, BALC.z + 0.3], to: town }); for (let i = -5; i <= 5; i++) M(cyl(0.1, 0.13, 1.1, 10), toon(0xe9dcc0), { ol: 0.025, p: [BALC.x + i * 0.55, BALC.y + 0.55, BALC.z + 1.5], to: town }); M(box(6.2, 0.18, 0.3), stone, { ol: 0.03, p: [BALC.x, BALC.y + 1.15, BALC.z + 1.5], to: town });
  M(box(3.2, 4.2, 0.4), toon(0x4a2e1c), { ol: 0.04, p: [BALC.x, BALC.y + 2.1, BALC.z - 1.0], to: town }); M(box(2.6, 3.6, 0.42), flat(0x5a2f3a), { p: [BALC.x, BALC.y + 2.1, BALC.z - 1.0], to: town, cast: false });
  for (const s of [-1, 1]) { const fl = new THREE.Group(); fl.position.set(s * 3.9, BALC.y + 1.2, BALC.z + 1.4); town.add(fl); M(cyl(0.05, 0.05, 2.4, 8), flat(INK), { p: [0, 1.2, 0], to: fl }); M(box(1.2, 0.8, 0.04), flat(0xb3272d), { ol: 0.02, p: [s * 0.6, 2.0, 0], to: fl, cast: false }); }
  // tower
  tower.position.set(TOWER.x, 0, TOWER.z); M(cyl(2.2, 2.6, TOWER.h, 28), stone, { ol: 0.05, p: [0, TOWER.h / 2, 0], to: tower }); for (let i = 0; i < 10; i++) { const a = i / 10 * 6.283; M(box(1.0, 0.9, 1.0), stone, { ol: 0.03, p: [Math.cos(a) * 2.3, TOWER.h + 0.45, Math.sin(a) * 2.3], to: tower }); }
  tower.userData.cap = new THREE.Group(); tower.userData.cap.position.y = TOWER.h; tower.add(tower.userData.cap);
  M(new THREE.ConeGeometry(2.5, 4.5, 28), toon(0x6a2f3a), { ol: 0.05, p: [0, 2.95, 0], to: tower.userData.cap }); M(cyl(0.05, 0.05, 1.6, 8), flat(INK), { p: [0, 5.9, 0], to: tower.userData.cap }); M(box(1.0, 0.6, 0.04), flat(0xffd34d), { p: [0.5, 6.4, 0], to: tower.userData.cap, cast: false });
  for (const y of [6, 11, 16]) { M(box(0.7, 1.3, 0.3), toon(0x3d2718), { ol: 0.03, p: [0, y, 2.4], to: tower }); M(box(0.5, 1.1, 0.32), flat(0x31405e), { p: [0, y, 2.4], to: tower, cast: false }); }
  // well, market stall, barrels, lamp posts, a tree
  M(cyl(1.1, 1.1, 0.9, 20), toon(0xffffff, { map: TX.stone }), { ol: 0.04, p: [-4.5, 0.45, -4], to: town }); M(cyl(0.9, 0.9, 1.0, 20, true), toon(0x3a3345, { side: THREE.DoubleSide }), { p: [-4.5, 0.5, -4], to: town, cast: false }); for (const s of [-1, 1]) M(box(0.14, 2.2, 0.14), toon(0x7a5232), { ol: 0.025, p: [-4.5 + s * 1.0, 1.9, -4], to: town }); M(new THREE.ConeGeometry(1.5, 0.9, 4), toon(0x9a4a3a), { ol: 0.04, p: [-4.5, 3.3, -4], r: [0, Math.PI / 4, 0], to: town });
  const stall = new THREE.Group(); stall.position.set(4.6, 0, -2.5); town.add(stall); M(box(2.6, 0.9, 1.2), toon(0x7a5232), { ol: 0.035, p: [0, 0.45, 0], to: stall }); M(box(3.0, 0.1, 1.6), toon(0xf1dfb4), { ol: 0.03, p: [0, 2.6, 0], r: [0.15, 0, 0], to: stall }); for (const x of [-1.3, 1.3]) M(cyl(0.06, 0.06, 2.6, 8), toon(0x7a5232), { p: [x, 1.3, 0.6], to: stall }); [[-0.8, 0xe2553d], [-0.3, 0x2f8f5b], [0.3, 0xf2c230], [0.8, 0xe8943a]].forEach(([x, c]) => { for (let i = 0; i < 4; i++) M(sph(0.16, 12, 8), toon(c), { ol: 0.02, p: [x + (i % 2) * 0.15 - 0.07, 1.05 + Math.floor(i / 2) * 0.22, (i % 2) * 0.2 - 0.1], to: stall }); });
  for (const [x, z] of [[6.0, 2.2], [6.6, 1.6]]) { M(cyl(0.42, 0.38, 1.0, 16), toon(0x8a5a36), { ol: 0.03, p: [x, 0.5, z], to: town }); for (const y of [0.25, 0.75]) M(new THREE.TorusGeometry(0.43, 0.03, 6, 18), toon(0x2a2530), { p: [x, y, z], r: [Math.PI / 2, 0, 0], to: town, cast: false }); }
  for (const [x, z] of [[-3.5, 4], [3.5, -9]]) { M(cyl(0.08, 0.1, 3.6, 10), flat(INK), { p: [x, 1.8, z], to: town }); M(box(0.5, 0.6, 0.5), flat(0xffd27a), { ol: 0.03, p: [x, 3.8, z], to: town, cast: false }); }
  M(cyl(0.25, 0.32, 3.0, 10), toon(0x6b4326), { ol: 0.03, p: [-7.5, 1.5, -11], to: town }); for (let i = 0; i < 6; i++) M(sph(1.1, 12, 10), toon(0x5fa14a), { ol: 0.04, p: [-7.5 + Math.cos(i * 1.1) * 0.9, 3.8 + (i % 2) * 0.7, -11 + Math.sin(i * 1.1) * 0.7], to: town });
  // the girl's tiny garden: a fenced patch by the near houses, in the tower's sunset shadow path
  const gard = new THREE.Group(); gard.position.set(3.2, 0, 7.5); town.add(gard); town.userData.garden = gard;
  M(box(2.6, 0.12, 2.0), toon(0x5a3a22), { ol: 0.03, p: [0, 0.06, 0], to: gard, recv: true }); for (const [x, z, c] of [[-0.8, -0.5, 0xe2553d], [0, -0.5, 0xf2c230], [0.8, -0.5, 0xe2553d], [-0.8, 0.5, 0x5fa14a], [0, 0.5, 0x5fa14a], [0.8, 0.5, 0xe8943a]]) { M(cyl(0.03, 0.03, 0.5, 6), toon(0x2f8f5b), { p: [x, 0.35, z], to: gard }); M(sph(0.16, 10, 8), toon(c), { ol: 0.02, p: [x, 0.65, z], to: gard }); } for (let i = 0; i < 9; i++) for (const s of [-1, 1]) M(box(0.08, 0.6, 0.08), toon(0xd9b36a), { ol: 0.02, p: [-1.3 + i * 0.325, 0.3, s * 1.0], to: gard }); for (const s of [-1, 1]) M(box(2.7, 0.08, 0.06), toon(0xd9b36a), { p: [0, 0.45, s * 1.0], to: gard, cast: false });
  M(box(2.2, 1.6, 1.8), toon(0xffffff, { map: houseTex(99, '#e8cfa0') }), { ol: 0.035, p: [3.2, 0.8, 12.0], to: town }); M(new THREE.ConeGeometry(1.7, 1.2, 4), roofM, { ol: 0.035, p: [3.2, 2.2, 12.0], r: [0, Math.PI / 4, 0], to: town });
}
M(box(7, 0.03, 0.12), flat(0xf3efe6), { p: [-0.5, 0.02, -2.2], to: town, cast: false });
// props
const coins = new THREE.Group(); root.add(coins); const coinGeo = cyl(0.14, 0.14, 0.035, 18), coinM = toon(0xffd34d);
const coinList = []; for (let i = 0; i < 140; i++) { const c = M(coinGeo, coinM, { ol: 0.015, to: coins }); c.visible = false; coinList.push(c); }
const rod = new THREE.Group(); root.add(rod); M(box(0.07, 0.07, 3.0), toon(0xd9b36a), { ol: 0.025, to: rod }); for (let i = 0; i <= 10; i++) M(box(0.1, 0.12, 0.02), flat(INK), { p: [0, 0.04, -1.5 + i * 0.3], to: rod, cast: false }); for (let i = 1; i < 10; i += 3) M(box(0.12, 0.2, 0.03), flat(0xb3272d), { p: [0, 0.06, -1.5 + i * 0.3], to: rod, cast: false });
const ledger = new THREE.Group(); root.add(ledger);
const ledgerTex = ftex(512, 640, g => { g.fillStyle = '#fbf6e4'; g.fillRect(0, 0, 512, 640); g.strokeStyle = '#1b1522'; g.lineWidth = 8; g.strokeRect(6, 6, 500, 628); g.fillStyle = '#1b1522'; g.textAlign = 'center'; g.font = '82px Pop'; g.fillText('SHADOW', 256, 120); g.fillText('TAX', 256, 210); g.fillStyle = '#b3272d'; g.font = '64px Pop'; g.fillText('1 COIN', 256, 350); g.fillText('A FOOT', 256, 430); g.fillStyle = '#1b1522'; g.font = '40px serif'; g.fillText('by order of the King', 256, 560); });
M(box(0.9, 1.15, 0.08), [flat(0x6a2f1a), flat(0x6a2f1a), flat(0x6a2f1a), flat(0x6a2f1a), flat(0xffffff, { map: ledgerTex }), flat(0x6a2f1a)], { ol: 0.03, to: ledger });
const sack = new THREE.Group(); root.add(sack); M(sph(0.42, 16, 12), toon(0xb79a70), { ol: 0.035, s: [1, 1.15, 1], to: sack }); M(cyl(0.16, 0.22, 0.25, 12), toon(0xb79a70), { ol: 0.03, p: [0, 0.52, 0], to: sack }); M(new THREE.TorusGeometry(0.18, 0.035, 6, 14), toon(0x8a5a36), { p: [0, 0.48, 0], r: [Math.PI / 2, 0, 0], to: sack, cast: false });
const sunDisc = M(sph(1.6, 24, 16), flat(0xfff0b0), { cast: false }); root.add(sunDisc);
const SETS = [town, coins, rod, ledger, sack, sunDisc, ...CAST.map(c => c.g)];
function hideAll() { SETS.forEach(g => g.visible = false); coinList.forEach(c => c.visible = false); }
// lighting presets: the sun position sets the shadow length
function sunset(t, az = -1) { town.visible = true; sunDisc.visible = true; bg(0xf7a05a); light(0.45, 2.4, [az * 8, 12, 34], 0xffd9a8, 0x6a4a50); sunDisc.position.set(az * 12, 10, 40); LOOK.grade = ['#ff9a4a', 0.2]; LOOK.bloom = 0.25; }
function noon(t) { town.visible = true; bg(0x8fd0ff); light(1.15, 1.9, [2, 40, 8], 0xffffff, 0x8a7a5a); sunDisc.visible = false; LOOK.grade = ['#fff0c0', 0.1]; LOOK.bloom = 0.18; }
function coinPile(n, cx, cz, spread = 1.2) { for (let i = 0; i < coinList.length; i++) { const c = coinList[i]; c.visible = i < n; if (!c.visible) continue; const a = i * 2.399, r = spread * Math.sqrt(i / coinList.length); const layer = Math.floor(i / 18); c.position.set(cx + Math.cos(a) * r * (1 - layer * 0.08), 0.02 + layer * 0.05 + (i % 3) * 0.012, cz + Math.sin(a) * r * (1 - layer * 0.08)); c.rotation.set(0.1 * Math.sin(i), a, 0.08 * Math.cos(i * 3)); } }
function hold(c, hand, obj, off = V(0, 0, 0), rot = [0, 0, 0]) { c.g.updateMatrixWorld(true); const p = V(...hand); c.up.localToWorld(p); obj.visible = true; obj.position.copy(p).add(off); obj.rotation.set(...rot); }
// ---------- props for the second half ----------
const stringM = toon(0xf1e4c8), knotM = toon(0xd9b36a);
function makeString(pts, knots = true) { const g = new THREE.Group(); const curve = new THREE.CatmullRomCurve3(pts.map(p => V(...p))); M(new THREE.TubeGeometry(curve, 60, 0.03, 6), stringM, { ol: 0.012, to: g, cast: false }); if (knots) { const L = curve.getLength(); for (let d = 0.3; d < L; d += 0.3) { const p = curve.getPointAt(d / L); M(sph(0.065, 10, 8), knotM, { ol: 0.015, p: [p.x, p.y, p.z], to: g, cast: false }); } } return g; }
const strShadow = makeString([[0, 1.3, 0], [0, 0.08, -2.5], [0, 0.08, -6], [0, 0.08, -9.5]]); root.add(strShadow);
const strLong = makeString([[3.2, 0.1, 7.0], [3.0, 0.08, 0], [3.4, 0.08, -8], [3.6, 0.08, -15.5]], true); root.add(strLong);
const coil = new THREE.Group(); root.add(coil); for (let i = 0; i < 7; i++) M(new THREE.TorusGeometry(0.16 + 0.01 * (i % 2), 0.03, 6, 14), stringM, { ol: 0.012, p: [0, i * 0.065, 0], r: [Math.PI / 2, 0, 0], to: coil, cast: false });
function ball(r) { const g = new THREE.Group(); M(sph(r, 16, 12), stringM, { ol: 0.03, to: g }); for (let i = 0; i < 9; i++) M(new THREE.TorusGeometry(r * 0.98, 0.028, 6, 24), knotM, { r: [i * 0.7, i * 1.1, 0], to: g, cast: false }); return g; }
const barrow = new THREE.Group(); root.add(barrow);
{ const w = toon(0x7a5232); M(box(1.1, 0.5, 0.8), w, { ol: 0.03, p: [0, 0.6, 0], to: barrow }); M(cyl(0.3, 0.3, 0.1, 18), toon(0x2a2530), { ol: 0.025, p: [0.6, 0.3, 0], r: [0, 0, Math.PI / 2], to: barrow }); for (const z of [-0.3, 0.3]) { M(box(1.2, 0.07, 0.07), w, { p: [-0.5, 0.7, z], r: [0, 0, 0.15], to: barrow }); M(box(0.07, 0.4, 0.07), w, { p: [-0.4, 0.2, z], to: barrow }); } const b = ball(0.42); b.position.set(0, 1.05, 0); barrow.add(b); }
const cart = new THREE.Group(); root.add(cart);
{ const w = toon(0x7a5232); M(box(2.4, 0.8, 1.4), w, { ol: 0.035, p: [0, 1.0, 0], to: cart }); for (const s of [-1, 1]) { M(cyl(0.55, 0.55, 0.12, 20), toon(0x4a2e1c), { ol: 0.03, p: [0, 0.55, s * 0.78], r: [Math.PI / 2, 0, 0], to: cart }); for (let i = 0; i < 6; i++) M(box(0.06, 1.0, 0.04), toon(0xd9b36a), { p: [0, 0.55, s * 0.78], r: [0, 0, i * Math.PI / 6], to: cart, cast: false }); } M(box(1.6, 0.08, 0.08), w, { p: [-1.9, 0.9, 0], to: cart }); for (const [x, y, z, r] of [[-0.5, 1.7, -0.2, 0.55], [0.4, 1.75, 0.3, 0.6], [0.2, 2.2, -0.3, 0.45], [-0.6, 1.5, 0.45, 0.4]]) { const b = ball(r); b.position.set(x, y, z); cart.add(b); } }
const saw = new THREE.Group(); root.add(saw); { M(box(1.5, 0.26, 0.03), toon(0xc9ced6), { ol: 0.025, p: [0.75, 0, 0], to: saw }); for (let i = 0; i < 14; i++) M(new THREE.ConeGeometry(0.05, 0.1, 4), toon(0xc9ced6), { p: [0.1 + i * 0.1, -0.17, 0], r: [Math.PI, 0, 0], to: saw, cast: false }); M(box(0.3, 0.45, 0.1), toon(0x7a5232), { ol: 0.025, p: [-0.1, 0.05, 0], to: saw }); }
const snow = M(box(70, 0.06, 70), toon(0xf4f6fb), { p: [0, 0.03, -10], recv: true, cast: false }); root.add(snow);
const snowCaps = new THREE.Group(); root.add(snowCaps);
const flowers = new THREE.Group(); root.add(flowers); for (let i = 0; i < 16; i++) { const x = -6 + (i * 1.7) % 12, z = 2 + (i * 2.3) % 6; M(cyl(0.02, 0.02, 0.3, 5), toon(0x2f8f5b), { p: [x, 0.15, z], to: flowers, cast: false }); M(sph(0.09, 8, 6), toon([0xe2553d, 0xf2c230, 0xd9869f][i % 3]), { p: [x, 0.33, z], to: flowers, cast: false }); }
const SETS2 = [strShadow, strLong, coil, barrow, cart, saw, snow, flowers];
const hideAll0 = hideAll; hideAll = function () { hideAll0(); SETS2.forEach(g => g.visible = false); };
function sunsetBehindTower(t, elev = 0.78) { town.visible = true; sunDisc.visible = true; bg(0xf7a05a); const d = 34; light(0.45, 2.4, [1.5, Math.sin(elev) * d, -Math.cos(elev) * d], 0xffd9a8, 0x6a4a50); sunDisc.position.set(6, 9, -46); LOOK.grade = ['#ff9a4a', 0.2]; LOOK.bloom = 0.25; }
function winterLook(t) { town.visible = true; snow.visible = true; sunDisc.visible = true; bg(0xd9c9d8); light(0.7, 1.6, [-6, 7, 30], 0xe8e0ff, 0x7a7a90); sunDisc.position.set(-10, 6, 40); LOOK.grade = ['#8fa0ff', 0.12]; LOOK.bloom = 0.22; }
function flakes(t, n = 60) { ctx.save(); ctx.fillStyle = 'rgba(255,255,255,0.9)'; for (let i = 0; i < n; i++) { const p = ((t * 0.12 + i * 0.0613) % 1), x = ((i * 977) % W) + 40 * Math.sin(t * 1.5 + i), y = p * H, r = 4 + (i % 4) * 2; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill(); } ctx.restore(); }
function leaves(t, n = 14) { ctx.save(); for (let i = 0; i < n; i++) { const p = ((t * 0.2 + i * 0.071) % 1), x = (i * 211) % W + 60 * Math.sin(t * 2 + i), y = p * H; ctx.setTransform(1, 0, 0, 1, x, y); ctx.rotate(t * 2 + i); ctx.fillStyle = ['#e8742a', '#d9a23a', '#b3472d'][i % 3]; ctx.strokeStyle = INK; ctx.lineWidth = 5; ctx.beginPath(); ctx.ellipse(0, 0, 26, 13, 0, 0, 7); ctx.fill(); ctx.stroke(); } ctx.restore(); }
function qmarks(t, c, n = 3) { const [x, y] = proj(c.headG.getWorldPosition(V(0, 0, 0))); for (let i = 0; i < n; i++) popText('?', x + (i - 1) * 140, y - 330 - 20 * Math.sin(t * 3 + i), 120 + 20 * (i % 2), '#fff', t, 0, 999, { rot: (i - 1) * 0.2 }); }
function girlWalk(t, x, z, ry, back = false) { show(girl, x, z, ry); girl.g.scale.setScalar(SC * 0.78); girl.face('happy'); const P = girl.walk(t * 7 * (back ? -1 : 1), 0.26); girl.pose({ ...P, rh: [0.55, 1.9, 0.6], lh: [-0.5, 1.5, 0.4] }); }
// ---------- helpers ----------
const S = i => Ls[i].s, CUT = i => i === 0 ? 0 : Ls[i].s - 0.1;
function wf(i, str, nth = 1) { let n = 0; for (const w of Ls[i].words) if (w.w.toLowerCase().replace(/[^a-z0-9']/g, '').startsWith(str)) { if (++n === nth) return w.s; } console.log('word not found', i, str); return Ls[i].s; }
function setCam(p, l, fov, t, shake = 0, roll = 0) { cam.fov = fov; cam.position.set(p[0] + 0.02 * Math.sin(t * 1.3) + shake * Math.sin(t * 61), p[1] + 0.015 * Math.sin(t * 1.7 + 1) + shake * Math.sin(t * 53), p[2]); cam.lookAt(l[0], l[1], l[2]); cam.rotateZ(roll); cam.updateProjectionMatrix(); }
const bg = c => { root.background = new THREE.Color(c); };
const SC = 0.86;
function show(c, x, z, ry = 0, tint = 0xffffff) { if (c.g.parent !== root) root.add(c.g); c.g.visible = true; c.g.position.set(x, 0, z); c.g.rotation.set(0, ry, 0); c.g.scale.setScalar(SC); c.tint(tint); c.hatG.position.set(0, 0, 0); c.hatG.rotation.set(0, 0, 0); c.g.updateMatrixWorld(true); }
function toLocal(c, w) { const p = w.clone(); c.up.worldToLocal(p); return [p.x, p.y, p.z]; }
function wisps(t, pts, col = '#8fd04a') { ctx.save(); ctx.lineCap = 'round'; pts.forEach(([x, y], i) => { for (const [lw, c] of [[20, INK], [11, col]]) { ctx.strokeStyle = c; ctx.lineWidth = lw; ctx.beginPath(); for (let k = 0; k <= 12; k++) { const yy = y - k * 16 - ((t * 60 + i * 37) % 60), xx = x + Math.sin(k * 0.7 + t * 4 + i) * 22; k ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); } ctx.stroke(); } }); ctx.restore(); }

// the tax scene: a man near the camera, his long shadow running down the street over the chalk line, a collector measuring it, the owner waiting
function stageRule(t, slide, paying = false) {
  show(townA, -0.9, 1.6, 0.35); townA.face(paying ? 'shock' : 'sad'); townA.pose({ lh: [-0.5, 1.9, 0.2], rh: paying ? [0.6, 1.7, 0.7] : [0.5, 1.9, 0.2], hx: 0.25, hy: -0.3 });
  show(collector, 0.2, -3.6, 1.1); collector.face('happy'); collector.pose({ pitch: 0.4, hx: 0.25, rh: [0.5, 1.0, 0.6], lh: [-0.4, 1.3, 0.55] }); hold(collector, [-0.4, 1.3, 0.55], ledger, V(0, 0.45, 0.1), [0, 0.6, 0]);
  show(townC, -2.3, -4.6, 0.3); townC.face(paying ? 'happy' : 'neutral'); townC.pose({ rh: [0.6, 1.5, 0.7], lh: [-0.5, 2.05, 0.05] }); if (paying) hold(townC, [0.6, 1.5, 0.7], sack, V(0, -0.25, 0.1));
  rod.visible = true; rod.position.set(-0.9, 0.08, lerp(-1.6, -3.8, slide)); rod.rotation.set(0, 0, 0);
}
// ---------- timeline ----------
function update(t) {
  hideAll(); overlay = () => { };
  let li = 0; for (let i = 0; i < Ls.length; i++) if (t >= CUT(i)) li = i;
  const s0 = CUT(li), s1 = li + 1 < Ls.length ? CUT(li + 1) : DUR, k = (t - s0) / (s1 - s0);
  const sub = (a, b) => cl((t - a) / (b - a));
  LOOK.grade = ['#ffc98a', 0.1]; LOOK.bloom = 0.14;

  if (li === 0) { // HOOK: the king on his balcony, pointing down at a shadow
    const tb = wf(0, 'tax') - 0.1;
    if (t < tb) { sunset(t, -1); show(king, BALC.x + 0.4, BALC.z + 0.4, 0.15); king.g.position.y = BALC.y; king.g.updateMatrixWorld(true); king.face('sneaky'); king.pose({ rh: [0.75, 1.5, 0.75], lh: [-0.5, 2.05, 0.05], hx: 0.3, pitch: 0.12, bob: 0.02 * Math.sin(t * 3) });
      const hp = king.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 1.0, hp.y - 0.1, hp.z + lerp(5.0, 4.2, sub(0, tb))], [hp.x, hp.y - 0.65, hp.z], 42, t, 0, -0.06);
    } else { sunset(t, -1); stageRule(t, 0); setCam([0.6, lerp(3.6, 3.2, sub(tb, s1)), lerp(7.6, 6.8, sub(tb, s1))], [-0.9, 0.6, -4.5], 58, t, 0, 0.04);
      overlay = () => popText('SHADOW TAX', W / 2, 270, 124, '#ffd23e', t, tb + 0.05, s1 - 0.02);
    }
  }
  else if (li === 1) { // the rule: one coin a foot
    const tp = wf(1, 'paid') - 0.1; sunset(t, -1); const slide = ss(s0, tp, t); stageRule(t, slide, t >= tp);
    if (t < tp) { setCam([lerp(0.2, -0.2, k * 1.6), lerp(1.4, 1.1, k * 1.6), lerp(3.4, 2.2, k * 1.6)], [-0.9, 0.1, -5.0], 58, t, 0, 0.06); }
    else { const n = Math.floor(sub(tp, s1 - 0.2) * 6); for (let i = 0; i < n; i++) { const c = coinList[i]; c.visible = true; const v = cl((t - tp - i * 0.33) / 0.35); c.position.set(lerp(-0.6, -2.0, v), 1.9 + 1.6 * Math.sin(v * Math.PI), lerp(1.0, -4.3, v)); c.rotation.set(v * 9, 0, 0.3); }
      setCam([lerp(2.6, 2.2, sub(tp, s1)), 3.0, lerp(2.6, 1.8, sub(tp, s1))], [-1.3, 1.0, -3.0], 58, t, 0, -0.05); }
    overlay = () => { if (t > tp) { for (let i = 0; i < 3; i++) { const a0 = tp + 0.35 + i * 0.66; if (t > a0 && t < a0 + 0.6) burst('CLINK!', 300 + i * 240, 560 + (i % 2) * 120, 130, t, a0, a0 + 0.6, -0.1 + i * 0.1); } } popText('1 COIN', W / 2, 250, 140, '#fff', t, wf(1, 'one') - 0.05, s1 - 0.02); popText('A FOOT', W / 2, 400, 140, '#ffd23e', t, wf(1, 'foot') - 0.05, s1 - 0.02); };
  }
  else if (li === 2) { // the king owned every street; coin pile grows
    const tr = wf(2, 'so') - 0.1; sunset(t, -1);
    if (t < tr) { show(king, BALC.x + 0.4, BALC.z + 0.4, 0.1); king.g.position.y = BALC.y; king.g.updateMatrixWorld(true); king.face('happy'); king.pose({ lh: [-0.9, 2.4, 0.5], rh: [0.9, 2.4, 0.5], hx: -0.15, bob: 0.02 * Math.sin(t * 3) });
      [[townA, -2.5, -6, 0.2], [townB, 1.5, -8.5, -0.4], [townC, -0.5, -3, 0.6], [tallMan, 3.5, -5.5, -0.2]].forEach(([c, x, z, ry]) => { show(c, x, z, ry); c.face('neutral'); c.pose(c.walk(t * 5 + x, 0.25)); });
      const u = sub(s0, tr); setCam([lerp(1.5, 1.0, u), lerp(2.0, 5.0, u), lerp(12, 0, u)], [BALC.x, lerp(3.0, BALC.y + 1.6, u), PAL_Z + 2], 56, t, 0, 0.04);
      overlay = () => popText('EVERY STREET', W / 2, 280, 112, '#ffd23e', t, wf(2, 'every') - 0.05, tr - 0.02);
    } else { const u = sub(tr, s1 - 0.1), n = Math.floor(ss(0, 1, u) * 140); coinPile(n, 0, -1.5, 2.2); coins.visible = true;
      show(king, 0, -1.5, 0); king.g.position.y = 0.02 + Math.floor(n / 18) * 0.05; king.face('happy'); king.pose({ lh: [-0.7, 2.2 + 0.1 * Math.sin(t * 8), 0.4], rh: [0.7, 2.2 + 0.1 * Math.cos(t * 8), 0.4], hx: -0.2, bob: 0.03 * Math.abs(Math.sin(t * 6)) });
      for (let i = 0; i < 6; i++) { const c = coinList[139 - i]; const p = ((t * 1.1 + i * 0.17) % 1); c.visible = true; c.position.set(-1.5 + i * 0.6 + 0.2 * Math.sin(i), 6.5 - p * 6.2, -1.5 + 0.5 * Math.cos(i * 2)); c.rotation.set(t * 7 + i, 0, 0.4); }
      setCam([lerp(0.5, 1.5, u), lerp(2.4, 3.6, u), lerp(6.0, 9.5, u)], [0, lerp(2.2, 2.4, u), -1.5], 52, t, 0, -0.04);
      overlay = () => { popText('VERY RICH', W / 2, 250, 124, '#fff', t, wf(2, 'rich') - 0.05, s1 - 0.02); popText('VERY FAST', W / 2, 395, 124, '#ffd23e', t, wf(2, 'fast') - 0.05, s1 - 0.02); };
    }
  }
  else if (li === 3) { // noon: tiny shadows; slouching; sawing the hat
    noon(t); const ts = wf(3, 'tall') - 0.1, th = wf(3, 'one') - 0.1;
    if (t < ts) { [[townA, -2.2, -2, 0.3], [townB, 0.4, -4, 0.1], [townC, 2.4, -1, -0.3]].forEach(([c, x, z, ry]) => { show(c, x, z, ry); c.face('neutral'); c.pose({ ...c.walk(t * 6 + x, 0.12), hx: 0.35 }); });
      setCam([lerp(-1, 1, k * 2), 6.0, lerp(6.5, 5.0, k * 2)], [0, 0.6, -2.5], 50, t, 0, 0.02);
      overlay = () => popText('NOON', W / 2, 280, 160, '#fff', t, wf(3, 'noon') - 0.05, ts - 0.02);
    } else if (t < th) { show(tallMan, 0, -1, 0.1); tallMan.face('sad'); const sl = ss(ts, ts + 1.0, t); tallMan.pose({ pitch: 0.45 * sl, hx: 0.3 * sl, bob: -0.25 * sl, lh: [-0.5, 1.6 - 0.4 * sl, 0.3], rh: [0.5, 1.6 - 0.4 * sl, 0.3] });
      setCam([2.2, 2.6, lerp(5.5, 4.6, sub(ts, th))], [0, 2.3, -1], 44, t, 0, -0.05);
      overlay = () => popText('SLOUCH', W / 2, 280, 150, '#ffd23e', t, wf(3, 'slouch') - 0.05, th - 0.02);
    } else { show(tallMan, 0, -1, 0.1); tallMan.face('neutral'); const v = sub(th + 0.3, th + 1.3), cut = t > th + 1.4; tallMan.pose({ rh: [0.7, 3.4 + 0.1 * Math.sin(t * 30) * (v > 0 && !cut ? 1 : 0), 0.3], lh: [-0.5, 1.6, 0.3], hx: -0.1 });
      const top = tallMan.hatG.userData.top; top.position.y = 0.95 + (cut ? (t - th - 1.4) * 2 : 0); top.rotation.z = cut ? (t - th - 1.4) * 3 : 0; top.visible = !(cut && t - th - 1.4 > 0.6);
      const hp = tallMan.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 0.8, hp.y + 0.6, hp.z + lerp(3.6, 3.0, sub(th, s1))], [hp.x, hp.y + 0.3, hp.z], 42, t, 0, 0.06);
      overlay = () => { if (v > 0 && !cut) burst('SAW SAW', 300, 450, 150, t, th + 0.3, th + 1.4, -0.1); popText('HIS OWN HAT', W / 2, 1100, 110, '#ffd23e', t, wf(3, 'hat') - 0.05, s1 - 0.02); };
    }
  }
  else if (li === 4) { // one girl, a tiny garden, out at sunset
    const tg = wf(4, 'kept') - 0.1, tn = wf(4, 'nobody') - 0.1; const G = town.userData.garden;
    if (t < tg) { sunset(t, -1); flowers.visible = false; show(girl, G.position.x - 0.3, G.position.z + 1.7, 0.2); girl.g.scale.setScalar(SC * 0.78); girl.face('happy'); girl.pose({ pitch: 0.3, hx: 0.2, rh: [0.4, 1.0, 0.7], lh: [-0.4, 1.2, 0.6], bob: -0.08 });
      setCam([G.position.x - 3.6, 2.6, G.position.z + lerp(4.8, 4.0, sub(s0, tg))], [G.position.x, 0.8, G.position.z + 0.5], 50, t, 0, -0.05);
      overlay = () => { popText('ONE GIRL', W / 2, 250, 140, '#fff', t, wf(4, 'one') - 0.05, wf(4, 'tiny') - 0.05); popText('A TINY GARDEN', W / 2, 250, 110, '#ffd23e', t, wf(4, 'tiny') - 0.05, tg - 0.02); };
    } else if (t < tn) { sunset(t, -1); girlWalk(t, -0.9, lerp(3.0, -1.0, sub(tg, tn)), Math.PI); setCam([0.8, 3.4, 7.8], [-0.9, 0.6, -4.5], 58, t, 0, 0.04);
      overlay = () => popText('AT SUNSET', W / 2, 270, 130, '#ffd23e', t, wf(4, 'sunset') - 0.05, tn - 0.02);
    } else { sunset(t, -1); [[townA, -1.6, -1.5, 0.3], [townB, 1.6, -1.2, -0.3]].forEach(([c, x, z, ry]) => { show(c, x, z, ry); c.face('think'); c.pose({ rh: [0.3, 2.9, 0.5], lh: [-0.5, 2.05, 0.05], hz: 0.15 * Math.sin(t * 2 + x) }); });
      setCam([0, 2.8, lerp(6.2, 5.4, sub(tn, s1))], [0, 2.4, -1.4], 50, t, 0, -0.04); overlay = () => { qmarks(t, townA, 2); qmarks(t, townB, 2); };
    }
  }
  else if (li === 5) { // the knot, walking backwards, refusing to tell
    const tw = wf(5, 'walked') - 0.1, tr = wf(5, 'refused') - 0.1; sunset(t, -1);
    if (t < tw) { show(girl, -0.9, 0.2, 0); girl.g.scale.setScalar(SC * 0.78); girl.face('neutral'); const kk = sub(s0 + 0.2, tw - 0.2); girl.pose({ rh: [0.35 + 0.1 * Math.sin(kk * 12), 1.7, 0.75], lh: [-0.35 - 0.1 * Math.sin(kk * 12), 1.7, 0.75], hx: 0.4, pitch: 0.15 });
      strShadow.visible = true; girl.g.updateMatrixWorld(true); const hp = V(0, 1.7, 0.75); girl.up.localToWorld(hp); strShadow.position.set(hp.x, hp.y - 1.3, hp.z); const kn = Math.floor(kk * 4);
      const hd = girl.headG.getWorldPosition(V(0, 0, 0)); setCam([hd.x + 0.6, hd.y - 0.9, hd.z + lerp(2.4, 2.0, kk)], [hd.x, hd.y - 1.2, hd.z + 0.4], 44, t, 0, 0.08);
      overlay = () => popText('A KNOT', W / 2, 270, 150, '#ffd23e', t, wf(5, 'knot') - 0.05, tw - 0.02);
    } else if (t < tr) { const u = sub(tw, tr); girlWalk(t, -0.9, lerp(0.5, -5.5, u), 0, true); strShadow.visible = true; strShadow.position.set(-0.9, 0, lerp(0.5, -5.5, u)); strShadow.rotation.y = Math.PI;
      setCam([lerp(1.8, 1.2, u), 2.2, lerp(3.5, -1.5, u)], [-0.9, 0.8, lerp(-1.5, -7.5, u)], 54, t, 0, -0.05);
      overlay = () => popText('BACKWARDS', W / 2, 270, 136, '#fff', t, wf(5, 'backwards') - 0.05, tr - 0.02);
    } else { show(girl, -0.9, -1.0, 0.4); girl.g.scale.setScalar(SC * 0.78); girl.face('sneaky'); girl.pose({ hy: 0.35 * Math.sin((t - tr) * 9), rh: [0.3, 1.9, 0.75], lh: [-0.5, 1.5, 0.4] });
      show(collector, 0.9, -2.2, -0.9); collector.face('think'); collector.pose({ rh: [0.3, 2.9, 0.5], lh: [-0.5, 2.05, 0.05], pitch: 0.1 });
      setCam([1.6, 2.4, 2.0], [-0.2, 1.7, -1.6], 48, t, 0, 0.05); overlay = () => { qmarks(t, collector, 1); popText('MEASURING?', W / 2, 270, 124, '#ffd23e', t, wf(5, 'measuring') - 0.05, s1 - 0.02); };
    }
  }
  else if (li === 6) { // collectors laugh, forget to charge
    sunset(t, -1); [[collector, -1.1, -1.2, 0.5], [collector2, 1.1, -1.0, -0.5]].forEach(([c, x, z, ry], i) => { show(c, x, z, ry); c.face('happy'); const lf = Math.abs(Math.sin(t * 7 + i)); c.pose({ pitch: 0.3 * lf, hx: -0.3 + 0.2 * lf, bob: 0.05 * lf, lh: [-0.5, 1.6 + 0.3 * lf, 0.3], rh: [0.5, 1.6 + 0.3 * lf, 0.3], lean: (i ? -1 : 1) * 0.08 * Math.sin(t * 7) }); });
    ledger.visible = true; ledger.position.set(0, 0.6, 0.3); ledger.rotation.set(-1.3, 0.3, 0.2);
    girlWalk(t, -0.9, lerp(-3, -7, k), 0, true); strShadow.visible = true; strShadow.position.set(-0.9, 0, lerp(-3, -7, k)); strShadow.rotation.y = Math.PI;
    setCam([lerp(0.6, 0.2, k), 2.6, lerp(4.8, 4.2, k)], [0, 2.2, -1.5], 50, t, 0, -0.04);
    overlay = () => { burst('HA HA HA!', 300, 450, 170, t, s0 + 0.3, s1 - 0.03, -0.1); burst('HA HA!', 790, 560, 140, t, s0 + 0.7, s1 - 0.03, 0.12); popText('FORGOT TO CHARGE', W / 2, 1120, 96, '#ffd23e', t, wf(6, 'forgot') - 0.05, s1 - 0.02); };
  }
  else if (li === 7 || li === 8) { // the king shouts from the balcony
    sunset(t, -1); show(king, BALC.x + 0.4, BALC.z + 0.4, 0.1); king.g.position.y = BALC.y; king.g.updateMatrixWorld(true); king.face('angry'); const sh = li === 8 ? 0.04 * Math.sin(t * 28) : 0;
    king.pose({ pitch: 0.35 + sh, hx: 0.15, rh: [0.55, 2.6, 0.75], lh: [-0.7, 2.3, 0.6], bob: 0.03 * Math.abs(Math.sin(t * 9)) });
    girlWalk(t, -0.9, -8 - 1.5 * k, 0, true); strShadow.visible = true; strShadow.position.set(-0.9, 0, -8 - 1.5 * k); strShadow.rotation.y = Math.PI;
    if (li === 7) { const u = sub(s0, s1); setCam([lerp(-3, -1.5, u), lerp(BALC.y + 1.2, BALC.y + 0.6, u), BALC.z + lerp(7, 5.5, u)], [BALC.x + 0.4, BALC.y + 2.2, BALC.z + 0.4], 46, t, 0, 0.05); overlay = () => popText('EVEN THE KING', W / 2, 270, 112, '#fff', t, s0 + 0.1, s1 - 0.02); }
    else { const hp = king.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 0.6, hp.y + 0.1, hp.z + lerp(4.4, 3.6, k)], [hp.x, hp.y - 0.4, hp.z], 42, t, 0.004, -0.06);
      overlay = () => { burst('THE ONLY THING', 540, 1080, 200, t, wf(8, 'only') - 0.08, wf(8, "you'll") - 0.05, -0.05); burst("YOU'LL EVER OWN!", 540, 1080, 210, t, wf(8, "you'll") - 0.05, s1 - 0.03, 0.05); }; }
  }
  else if (li === 9) { // summer: string around her arm
    sunset(t, -1); flowers.visible = true; show(girl, -0.9, 0.3, 0.2); girl.g.scale.setScalar(SC * 0.78); girl.face('happy'); girl.pose({ rh: [0.7, 2.2, 0.5], lh: [-0.5, 1.5, 0.4], hz: 0.08 * Math.sin(t * 3) });
    hold(girl, [0.7, 2.2, 0.5], coil, V(-0.05, -0.55, 0), [0, 0, 0.2]); coil.scale.setScalar(1.6);
    const hp = girl.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 0.9, hp.y - 0.3, hp.z + lerp(3.6, 3.0, k)], [hp.x + 0.2, hp.y - 0.8, hp.z], 44, t, 0, 0.05);
    overlay = () => popText('SUMMER', W / 2, 270, 150, '#ffd23e', t, wf(9, 'summer') - 0.05, s1 - 0.02);
  }
  else if (li === 10) { // autumn: a wheelbarrow
    sunset(t, -1); barrow.visible = true; barrow.position.set(-0.2, 0, -0.6); barrow.rotation.y = 0.3; show(girl, -1.6, -0.3, 0.6); girl.g.scale.setScalar(SC * 0.78); girl.face('happy'); girl.pose({ pitch: 0.15, rh: [0.55, 1.35, 0.6], lh: [-0.3, 1.35, 0.6] });
    setCam([lerp(2.4, 2.0, k), 2.4, lerp(3.8, 3.2, k)], [-0.6, 1.0, -0.6], 50, t, 0, -0.05); overlay = () => { leaves(t); popText('AUTUMN', W / 2, 270, 150, '#ff9a3a', t, wf(10, 'autumn') - 0.05, s1 - 0.02); };
  }
  else if (li === 11) { // winter: a cart to the palace doors, shortest day
    const tb = wf(11, 'brought') - 0.1, ts = wf(11, 'shortest') - 0.1; winterLook(t); cart.visible = true;
    if (t < ts) { const u = sub(tb, ts); cart.position.set(-3.0, 0, lerp(2, -9.5, ss(0, 1, u))); cart.rotation.y = Math.PI / 2; const gz = cart.position.z - 2.6; girlWalk(t, -3.0, gz, Math.PI); girl.pose({ ...girl.walk(t * 7, 0.26), lean: -0.25, rh: [0.6, 1.4, -0.4], lh: [-0.6, 1.4, -0.4] });
      setCam([lerp(2.5, 1.5, u), lerp(2.6, 3.2, u), lerp(3, -4, u)], [-3.0, 1.4, lerp(-1, -11, u)], 52, t, 0, 0.04);
      overlay = () => { flakes(t); popText('WINTER', W / 2, 270, 150, '#fff', t, wf(11, 'winter') - 0.05, tb - 0.02); popText('A CART', W / 2, 270, 150, '#ffd23e', t, wf(11, 'cart') - 0.05, ts - 0.02); };
    } else { cart.position.set(-3.0, 0, -10); cart.rotation.y = Math.PI / 2; show(girl, -3.0, -12, Math.PI); girl.g.scale.setScalar(SC * 0.78); girl.face('neutral'); girl.pose({ hx: -0.3, rh: [0.6, 2.4, 0.3], lh: [-0.5, 1.5, 0.4] });
      sunDisc.scale.setScalar(2.2); sunDisc.position.set(-14, 4.5, 40); const u = sub(ts, s1); setCam([lerp(-2.2, -1.6, u), lerp(1.2, 1.8, u), lerp(-6, -4, u)], [lerp(-8, -10, u), 4.0, 30], 50, t, 0, -0.04);
      overlay = () => { flakes(t); popText('SHORTEST DAY', W / 2, 270, 112, '#fff', t, ts, wf(11, 'sun') - 0.05); popText('SUN LOWEST', W / 2, 270, 124, '#ffd23e', t, wf(11, 'sun') - 0.05, s1 - 0.02); };
    }
  }
  else if (li === 12) { // she points out of the window, the king turns
    const tt = wf(12, 'king') - 0.1; winterLook(t); sunsetBehindTower(t, 0.78); snow.visible = true;
    show(king, BALC.x - 1.0, BALC.z + 0.2, lerp(2.6, 0.3, ss(tt, tt + 0.6, t))); king.g.position.y = BALC.y; king.g.updateMatrixWorld(true); king.face(t > tt + 0.4 ? 'shock' : 'neutral'); king.pose({ lh: [-0.5, 2.05, 0.05], rh: [0.5, 2.05, 0.05] });
    show(girl, BALC.x + 1.2, BALC.z + 0.4, -0.3); girl.g.position.y = BALC.y; girl.g.scale.setScalar(SC * 0.78); girl.face('neutral'); girl.pose({ rh: [0.9, 2.3, 0.9], lh: [-0.5, 1.5, 0.4], hy: -0.3 });
    setCam([BALC.x - 3.4, BALC.y + 1.6, BALC.z + 1.0], [BALC.x + 0.6, BALC.y + 1.5, BALC.z + 0.3], 52, t, 0, 0.04);
    overlay = () => { popText('SHE POINTED', W / 2, 270, 124, '#fff', t, s0 + 0.1, tt - 0.02); popText('HE TURNED', W / 2, 270, 136, '#ffd23e', t, tt, s1 - 0.02); };
  }
  else if (li === 13) { // the tower's shadow across town onto her garden
    sunsetBehindTower(t, 0.78); snow.visible = true; const G = town.userData.garden, u = ss(0, 1, k);
    setCam([lerp(TOWER.x + 3, G.position.x - 2, u), lerp(30, 10, u), lerp(TOWER.z + 1, G.position.z + 4, u)], [lerp(TOWER.x, G.position.x, u), lerp(1, 0.5, u), lerp(TOWER.z + 12, G.position.z, u)], 58, t, 0, -0.04);
    overlay = () => { popText("THE TOWER'S", W / 2, 250, 120, '#fff', t, wf(13, 'tower') - 0.05, wf(13, 'landed') - 0.05); popText('SHADOW', W / 2, 395, 150, '#ffd23e', t, wf(13, 'shadow') - 0.05, wf(13, 'landed') - 0.05); popText('HER GARDEN', W / 2, 270, 130, '#ffd23e', t, wf(13, 'garden') - 0.3, s1 - 0.02); };
  }
  else if (li === 14 || li === 15) { // "That's my garden. I measured every foot."
    sunsetBehindTower(t, 0.78); snow.visible = true; const G = town.userData.garden;
    if (li === 14) { show(girl, G.position.x - 1.6, G.position.z + 1.2, 0.6); girl.g.scale.setScalar(SC * 0.78); girl.face('angry'); girl.pose({ rh: [0.8, 1.6, 0.9], lh: [-0.5, 1.5, 0.4], hx: 0.1 });
      const hp = girl.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 0.8, hp.y + 0.1, hp.z + lerp(3.4, 2.9, k)], [hp.x, hp.y - 0.4, hp.z], 42, t, 0, 0.06); overlay = () => burst("THAT'S MY GARDEN", 540, 1060, 210, t, s0 + 0.05, s1 - 0.03, -0.05); }
    else { strLong.visible = true; show(girl, 2.0, 6.5, 0.4); girl.g.scale.setScalar(SC * 0.78); girl.face('neutral'); girl.pose({ rh: [0.7, 1.1, 0.8], lh: [-0.5, 1.5, 0.4], pitch: 0.2 });
      const u = ss(0, 1, k); setCam([lerp(0.6, 0.2, u), lerp(3.0, 9, u), lerp(11, 5, u)], [3.2, 0.3, lerp(4, -5, u)], 54, t, 0, -0.04);
      overlay = () => { popText('EVERY FOOT', W / 2, 270, 136, '#ffd23e', t, wf(15, 'measured') - 0.05, s1 - 0.02); }; }
  }
  else if (li === 16) { // the king stopped smiling
    sunsetBehindTower(t, 0.78); snow.visible = true; show(king, BALC.x + 0.4, BALC.z + 0.4, 0.15); king.g.position.y = BALC.y; king.g.updateMatrixWorld(true); king.face(t > s0 + 0.5 ? 'sad' : 'happy'); king.pose({ lh: [-0.5, 2.05, 0.05], rh: [0.5, 2.05, 0.05], hx: t > s0 + 0.5 ? 0.15 : -0.1, bob: -0.04 * ss(s0 + 0.5, s0 + 0.9, t) });
    const hp = king.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 0.5, hp.y + 0.05, hp.z + lerp(3.4, 2.9, k)], [hp.x, hp.y - 0.3, hp.z], 40, t, 0, 0.05);
  }
  else if (li === 17) { // the whole town came to watch
    sunsetBehindTower(t, 0.72); snow.visible = true; [[townA, -3.5, 2, 0], [townB, -1.8, 3, 0], [townC, 0.2, 2.5, 0], [tallMan, 2.4, 3.2, 0], [collector, -2.6, 0.5, 0], [collector2, 1.4, 0.8, 0]].forEach(([c, x, z], i) => { show(c, x, z, 0); c.face('neutral'); c.pose({ hx: -0.6, lh: [-0.5, 2.05, 0.05], rh: [0.5, 2.05, 0.05], bob: 0.01 * Math.sin(t * 3 + i) }); });
    show(girl, -0.6, 4.2, 0); girl.g.scale.setScalar(SC * 0.78); girl.face('happy'); girl.pose({ hx: -0.6 });
    const u = ss(0, 1, k); setCam([lerp(-1, 0.5, u), lerp(1.6, 3.0, u), lerp(9, 7, u)], [0, lerp(2.4, 9, u), -8], 56, t, 0, 0.03);
    overlay = () => popText('THE WHOLE TOWN', W / 2, 270, 104, '#fff', t, wf(17, 'whole') - 0.05, s1 - 0.02);
  }
  else if (li === 18) { // he sawed the top off his own tower
    sunsetBehindTower(t, 0.72); snow.visible = true; const ts = wf(18, 'sawed') - 0.1, cut = t > ts + 1.1, v = t - ts - 1.1;
    show(king, TOWER.x + 0.4, TOWER.z + 1.2, 0.3); king.g.position.y = TOWER.h + 0.9; king.g.updateMatrixWorld(true); king.face(cut ? 'sad' : 'angry'); king.pose({ pitch: 0.3, hx: 0.2, rh: [0.6, 1.5 + (cut ? 0 : 0.12 * Math.sin(t * 28)), 0.7], lh: [-0.4, 1.6, 0.6] });
    hold(king, [0.6, 1.5 + (cut ? 0 : 0.12 * Math.sin(t * 28)), 0.7], saw, V(0, 0.1, 0.1), [0, -0.3, -0.4]);
    const cap = tower.userData.cap; cap.position.y = TOWER.h + (cut ? -v * v * 4 : 0); cap.position.x = cut ? v * 1.2 : 0; cap.rotation.z = cut ? -v * 1.6 : 0;
    const top = V(TOWER.x, TOWER.h + 2, TOWER.z); setCam([top.x + 4, lerp(top.y - 6, top.y + 1, ss(0, 1, k)), top.z + lerp(10, 7, k)], [top.x, top.y - 1, top.z], 48, t, 0, -0.05);
    overlay = () => { if (!cut && t > ts) burst('SAW SAW', 300, 450, 150, t, ts, ts + 1.1, -0.1); if (cut && v < 0.6) burst('CRACK!', 760, 560, 170, t, ts + 1.1, ts + 1.7, 0.1); popText('HIS OWN TOWER', W / 2, 1120, 104, '#ffd23e', t, wf(18, 'tower') - 0.05, s1 - 0.02); };
  }
  else { // "And he paid one coin a foot." loops back into the hook framing
    sunsetBehindTower(t, 0.72); snow.visible = true; tower.userData.cap.visible = false; show(king, BALC.x + 0.4, BALC.z + 0.4, 0.15); king.g.position.y = BALC.y; king.g.updateMatrixWorld(true); king.face('sad'); king.pose({ rh: [0.75, 1.5, 0.75], lh: [-0.5, 2.05, 0.05], hx: 0.3, pitch: 0.12 });
    for (let i = 0; i < 10; i++) { const c = coinList[i], p = ((t * 0.9 + i * 0.1) % 1); c.visible = true; c.position.set(BALC.x + 1.0 + 0.2 * Math.sin(i), BALC.y + 1.6 - p * 7, BALC.z + 1.9 + 0.2 * Math.cos(i)); c.rotation.set(t * 8 + i, 0, 0.3); } coins.visible = true;
    const hp = king.headG.getWorldPosition(V(0, 0, 0)); const u = ss(0, 1, k); setCam([hp.x + 1.0, hp.y - 0.1, hp.z + lerp(6.0, 5.0, u)], [hp.x, hp.y - 0.65, hp.z], 42, t, 0, -0.06);
    overlay = () => { popText('1 COIN', W / 2, 250, 140, '#fff', t, wf(19, 'one') - 0.05, DUR + 1); popText('A FOOT', W / 2, 400, 140, '#ffd23e', t, wf(19, 'foot') - 0.05, DUR + 1); };
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
