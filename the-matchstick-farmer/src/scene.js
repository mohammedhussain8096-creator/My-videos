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
let TM, Ls, DUR = 60;
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

// ===== The Matchstick — wheat fields, village, wildfire =====
const FT = []; function ftex(w, h, d) { const t = ctex(w, h, d); t.userData.draw = d; FT.push(t); return t; }
window.afterFonts = () => FT.forEach(t => { t.userData.draw(t.userData.g, t.userData.c.width, t.userData.c.height); t.needsUpdate = true; });
Object.assign(sun.shadow.camera, { left: -40, right: 40, top: 40, bottom: -40, near: 1, far: 160 }); sun.shadow.camera.updateProjectionMatrix(); sun.shadow.mapSize.set(4096, 4096); sun.shadow.bias = -0.0006;
const glowTex = ctex(128, 128, g => { const r = g.createRadialGradient(64, 64, 0, 64, 64, 64); r.addColorStop(0, 'rgba(255,240,190,1)'); r.addColorStop(0.35, 'rgba(255,170,60,0.55)'); r.addColorStop(1, 'rgba(255,120,30,0)'); g.fillStyle = r; g.fillRect(0, 0, 128, 128); });
function glow(parent, x, y, z, s = 1.2, op = 0.9) { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: op })); sp.position.set(x, y, z); sp.scale.set(s, s, 1); parent.add(sp); return sp; }
const flameTex = ctex(128, 256, g => { const r = g.createRadialGradient(64, 190, 6, 64, 150, 120); r.addColorStop(0, 'rgba(255,250,200,1)'); r.addColorStop(0.25, 'rgba(255,200,60,0.95)'); r.addColorStop(0.55, 'rgba(255,110,20,0.75)'); r.addColorStop(1, 'rgba(200,40,0,0)'); g.fillStyle = r; g.beginPath(); g.moveTo(64, 0); g.bezierCurveTo(110, 90, 128, 160, 100, 230); g.quadraticCurveTo(64, 260, 28, 230); g.bezierCurveTo(0, 160, 18, 90, 64, 0); g.fill(); });
const smokeTex = ctex(128, 128, g => { const r = g.createRadialGradient(64, 64, 0, 64, 64, 64); r.addColorStop(0, 'rgba(70,60,60,0.75)'); r.addColorStop(0.6, 'rgba(70,60,60,0.35)'); r.addColorStop(1, 'rgba(70,60,60,0)'); g.fillStyle = r; g.fillRect(0, 0, 128, 128); });
function sprites(parent, n, tex, add = true) { const arr = []; for (let i = 0; i < n; i++) { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, blending: add ? THREE.AdditiveBlending : THREE.NormalBlending, depthWrite: false, transparent: true })); s.center.set(0.5, 0.05); parent.add(s); arr.push(s); } return arr; }
// fire line: sprites placed along a list of points, each flickering
function fireAt(arr, pts, t, h = 2.6, on = 1) { arr.forEach((s, i) => { const p = pts[i % pts.length]; s.visible = on > 0 && i < pts.length * 3; if (!s.visible) return; const k = Math.floor(i / pts.length); const fl = 0.7 + 0.35 * Math.sin(t * (9 + i % 5) + i) + 0.2 * Math.sin(t * 23 + i * 1.7); s.position.set(p.x + (k - 1) * 0.5, p.y, p.z + (k - 1) * 0.35); s.scale.set(h * 0.55 * fl * on, h * fl * on, 1); s.material.rotation = 0.15 * Math.sin(t * 3 + i); }); }
function smokeAt(arr, pts, t, rise = 14, size = 6) { arr.forEach((s, i) => { const p = pts[i % pts.length]; const q = ((t * 0.12 + i * 0.137) % 1); s.visible = true; s.position.set(p.x + q * 4 + Math.sin(i) * 2, p.y + 1 + q * rise, p.z - q * 2); const sc = size * (0.5 + q * 1.6); s.scale.set(sc, sc, 1); s.material.opacity = 0.8 * Math.sin(q * Math.PI); }); }

// ---------- ground: farm plain with hills behind (−z) ----------
const world = new THREE.Group(); root.add(world);
const T4 = {
  field: (() => { const t = ctex(256, 256, (g, w, h) => { g.fillStyle = '#c9a24a'; g.fillRect(0, 0, w, h); for (let i = 0; i < 900; i++) { g.strokeStyle = `rgba(${rnd() < 0.5 ? '150,110,40' : '240,210,120'},0.5)`; g.lineWidth = 2; const x = rnd() * w, y = rnd() * h; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (rnd() - 0.5) * 4, y - 8); g.stroke(); } }); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(20, 20); return t; })(),
  grass: (() => { const t = ctex(256, 256, (g, w, h) => { g.fillStyle = '#7fa848'; g.fillRect(0, 0, w, h); for (let i = 0; i < 900; i++) { g.strokeStyle = `rgba(${rnd() < 0.5 ? '70,110,40' : '150,190,90'},0.5)`; g.lineWidth = 2; const x = rnd() * w, y = rnd() * h; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (rnd() - 0.5) * 5, y - 7); g.stroke(); } }); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(40, 40); return t; })(),
  ash: (() => { const t = ctex(256, 256, (g, w, h) => { g.fillStyle = '#2a2224'; g.fillRect(0, 0, w, h); for (let i = 0; i < 500; i++) { g.fillStyle = `rgba(${rnd() < 0.5 ? '10,8,8' : '110,100,100'},${0.3 + rnd() * 0.4})`; g.fillRect(rnd() * w, rnd() * h, 2 + rnd() * 6, 1 + rnd() * 2); } for (let i = 0; i < 30; i++) { g.fillStyle = 'rgba(255,120,40,0.7)'; g.fillRect(rnd() * w, rnd() * h, 2, 2); } }); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(8, 1); return t; })(),
};
M(box(300, 0.2, 300), toon(0xffffff, { map: T4.grass }), { p: [0, -0.1, -40], recv: true, to: world, cast: false });
// fields: farmer's (x 2..26), neighbour's (x -26..-2), both from z 6 down to z -22
const FARM = { x0: 2, x1: 26 }, NEIGH = { x0: -26, x1: -2 }, Z0 = 6, Z1 = -22, BREAK = { z0: -22, z1: -17 };
M(box(24, 0.06, 28), toon(0xffffff, { map: T4.field }), { p: [14, 0.02, -8], recv: true, to: world, cast: false });
M(box(24, 0.06, 28), toon(0xffffff, { map: T4.field }), { p: [-14, 0.02, -8], recv: true, to: world, cast: false });
const ashStrip = M(box(24, 0.07, 5), toon(0xffffff, { map: T4.ash }), { p: [14, 0.04, -19.5], recv: true, to: world, cast: false }); ashStrip.visible = false;
// dirt road between the fields leading to the village
const roadT = ctex(64, 256, (g, w, h) => { g.fillStyle = '#a07a52'; g.fillRect(0, 0, w, h); for (let i = 0; i < 200; i++) { g.fillStyle = `rgba(${rnd() < 0.5 ? '70,50,30' : '200,170,130'},0.35)`; g.fillRect(rnd() * w, rnd() * h, 3, 3); } }); roadT.wrapT = THREE.RepeatWrapping; roadT.repeat.set(1, 8);
M(box(3, 0.08, 60), toon(0xffffff, { map: roadT }), { p: [0, 0.03, 0], recv: true, to: world, cast: false });
// wheat: instanced stalks with heads (farmer's field hides the strip that gets burned)
const wheatGeo = (() => { const g = new THREE.CylinderGeometry(0.02, 0.03, 1.1, 4); g.translate(0, 0.55, 0); return g; })(), headGeo = (() => { const g = new THREE.SphereGeometry(0.07, 6, 4); g.scale(1, 2.6, 1); g.translate(0, 1.18, 0); return g; })();
const dummy = new THREE.Object3D(), tmpC = new THREE.Color();
function wheatField(x0, x1, z0, z1, n, skip) { const st = new THREE.InstancedMesh(wheatGeo, toon(0xffffff), n), hd = new THREE.InstancedMesh(headGeo, toon(0xffffff), n); let k = 0; const pos = [];
  for (let i = 0; i < n * 2 && k < n; i++) { const x = x0 + rnd() * (x1 - x0), z = z1 + rnd() * (z0 - z1); if (skip && skip(x, z)) continue; dummy.position.set(x, 0, z); dummy.rotation.set((rnd() - 0.5) * 0.25, rnd() * 6.28, (rnd() - 0.5) * 0.25); dummy.scale.set(1, 0.85 + rnd() * 0.35, 1); dummy.updateMatrix(); st.setMatrixAt(k, dummy.matrix); hd.setMatrixAt(k, dummy.matrix); st.setColorAt(k, tmpC.setHSL(0.12, 0.55, 0.45 + rnd() * 0.1)); hd.setColorAt(k, tmpC.setHSL(0.11, 0.65, 0.55 + rnd() * 0.12)); pos.push([x, z]); k++; }
  st.count = hd.count = k; st.castShadow = true; world.add(st); world.add(hd); return { st, hd, pos }; }
const fieldF = wheatField(FARM.x0 + 0.5, FARM.x1, Z0, BREAK.z1, 9000), stripF = wheatField(FARM.x0 + 0.5, FARM.x1, BREAK.z1, BREAK.z0, 1800), fieldN = wheatField(NEIGH.x0, NEIGH.x1 - 0.5, Z0, Z1, 11000);
// fences round the fields
function fenceLine(ax, az, bx, bz) { const L = Math.hypot(bx - ax, bz - az), n = Math.floor(L / 2); for (let i = 0; i <= n; i++) { const x = ax + (bx - ax) * i / n, z = az + (bz - az) * i / n; M(box(0.14, 0.9, 0.14), toon(0x7a5232), { ol: 0.02, p: [x, 0.45, z], to: world }); } const mid = V((ax + bx) / 2, 0, (az + bz) / 2); for (const y of [0.4, 0.75]) { const r = M(box(0.06, 0.07, L), toon(0x8a6a44), { p: [mid.x, y, mid.z], to: world, cast: false }); r.lookAt(V(bx, y, bz)); } }
fenceLine(1.6, Z0, 1.6, Z1); fenceLine(-1.6, Z0, -1.6, Z1); fenceLine(26, Z0, 26, Z1); fenceLine(-26, Z0, -26, Z1);
// hay bales and a scarecrow
for (const [x, z] of [[20, 4], [22, 2.5], [-20, 3]]) M(cyl(0.7, 0.7, 1.2, 16), toon(0xe2c26a), { ol: 0.03, p: [x, 0.7, z], r: [0, 0, Math.PI / 2], to: world });
{ const sc = new THREE.Group(); sc.position.set(-12, 0, -6); world.add(sc); M(cyl(0.06, 0.06, 2.6, 6), toon(0x6b4326), { p: [0, 1.3, 0], to: sc }); M(cyl(0.05, 0.05, 1.8, 6), toon(0x6b4326), { p: [0, 1.9, 0], r: [0, 0, Math.PI / 2], to: sc }); M(sph(0.32, 12, 10), toon(0xe2c26a), { ol: 0.025, p: [0, 2.7, 0], to: sc }); M(cyl(0.5, 0.5, 0.05, 16), toon(0x8a6a44), { ol: 0.02, p: [0, 2.95, 0], to: sc }); M(box(0.7, 0.8, 0.3), toon(0x3b5bd9), { ol: 0.02, p: [0, 1.9, 0], to: sc }); }
// village at the near end (+z), with a windmill
const village = new THREE.Group(); world.add(village); const roofM = toon(0x9a4a3a);
function house(x, z, ry, seed, col, w = 4.4, ht = 4.4) { const h = new THREE.Group(); h.position.set(x, 0, z); h.rotation.y = ry; village.add(h); const m = toon(0xffffff, { map: houseTex(seed, col) }); M(box(w, ht, 4), [m, m, roofM, roofM, m, m], { ol: 0.05, p: [0, ht / 2, 0], to: h }); const tri = new THREE.Shape(); tri.moveTo(-w / 2 - 0.4, 0); tri.lineTo(w / 2 + 0.4, 0); tri.lineTo(0, 2.3); tri.closePath(); M(new THREE.ExtrudeGeometry(tri, { depth: 4.5, bevelEnabled: false }), roofM, { ol: 0.05, p: [0, ht, -2.25], to: h }); M(box(0.6, 1.5, 0.6), toon(0x6b4636), { ol: 0.03, p: [w * 0.25, ht + 1.6, -0.6], to: h }); return h; }
[[-6, 14, 0, 3, '#efe2c4'], [6, 14, 0, 5, '#e3c9a0'], [-6, 21, 0, 7, '#f1dfb4'], [6, 21, 0, 9, '#e2c594'], [-13, 17, 0.4, 11, '#ead9b4'], [13, 17, -0.4, 13, '#e8cfa0'], [-6, 28, 0, 15, '#dcc59a'], [6, 28, 0, 17, '#efe2c4']].forEach(a => house(...a));
const bakery = house(6, 9.5, 0, 19, '#f4e4c2', 4.6, 4.2); { const sg = ftex(256, 96, g => { g.fillStyle = '#6b4326'; g.fillRect(0, 0, 256, 96); g.fillStyle = '#ffd34d'; g.font = '56px Pop'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('BAKERY', 128, 52); }); M(box(2.4, 0.8, 0.1), toon(0xffffff, { map: sg }), { ol: 0.02, p: [0, 3.4, 2.06], to: bakery }); }
const mill = new THREE.Group(); mill.position.set(-16, 0, 8); village.add(mill); { M(cyl(1.4, 2.0, 7, 16), toon(0xf1e6cf), { ol: 0.05, p: [0, 3.5, 0], to: mill }); M(new THREE.ConeGeometry(1.8, 2.2, 16), roofM, { ol: 0.05, p: [0, 8.1, 0], to: mill }); const sails = new THREE.Group(); sails.position.set(0, 6.8, 1.6); mill.add(sails); mill.userData.sails = sails; for (let i = 0; i < 4; i++) { const a = new THREE.Group(); a.rotation.z = i * Math.PI / 2; sails.add(a); M(box(0.12, 4.0, 0.1), toon(0x6b4326), { p: [0, 2.0, 0], to: a }); M(box(0.9, 3.0, 0.04), toon(0xf3efe6), { ol: 0.02, p: [0.5, 2.3, 0], to: a }); } }
// barn by the farmer's field
const barn = new THREE.Group(); barn.position.set(20, 0, 9); world.add(barn); { M(box(6, 4, 5), toon(0xb3472d), { ol: 0.05, p: [0, 2, 0], to: barn }); const tri = new THREE.Shape(); tri.moveTo(-3.4, 0); tri.lineTo(3.4, 0); tri.lineTo(0, 2.6); tri.closePath(); M(new THREE.ExtrudeGeometry(tri, { depth: 5.6, bevelEnabled: false }), toon(0x5a3a2a), { ol: 0.05, p: [0, 4, -2.8], to: barn }); M(box(2.4, 3, 0.1), toon(0x7a2f2a), { ol: 0.03, p: [0, 1.5, 2.55], to: barn }); for (const s of [-1, 1]) M(box(0.12, 3.2, 0.12), toon(0xf3efe6), { p: [s * 0.6, 1.5, 2.62], r: [0, 0, s * 0.68], to: barn, cast: false }); }
// hills and forest behind the fields
for (const [x, z, r, sy] of [[-40, -70, 40, 0.45], [0, -80, 46, 0.5], [44, -72, 40, 0.42], [-90, -60, 50, 0.4], [90, -60, 50, 0.4]]) M(new THREE.SphereGeometry(r, 28, 16), toon(0x6a9a4a), { p: [x, -r * 0.2, z], s: [1, sy, 1], to: world, cast: false, recv: true });
const pineM = toon(0x2f6b3f), trunkM = toon(0x5a3a22); const forestPts = [];
for (let i = 0; i < 140; i++) { const x = -60 + rnd() * 120, z = -30 - rnd() * 22; const g = new THREE.Group(); g.position.set(x, 0, z); const s = 1.0 + rnd() * 0.9; g.scale.setScalar(s); world.add(g); M(cyl(0.15, 0.2, 0.9, 8), trunkM, { ol: 0.03, p: [0, 0.45, 0], to: g }); for (let k = 0; k < 3; k++) M(new THREE.ConeGeometry(1.1 - k * 0.28, 1.4, 9), pineM, { ol: 0.05, p: [0, 1.3 + k * 0.75, 0], to: g }); g.userData.tree = true; forestPts.push(g); }
// wildfire: points along the hills (far), the forest (mid) and the farm edge (near)
const hillLine = [], forestLine = [], farmLine = []; for (let i = 0; i < 40; i++) { const x = -60 + i * 3; hillLine.push(V(x, 6 + 3 * Math.sin(i * 0.5), -62 - 4 * Math.sin(i * 0.3))); forestLine.push(V(x, 0, -40 - 6 * Math.sin(i * 0.7))); }
const fireFar = sprites(root, 120, flameTex), fireMid = sprites(root, 120, flameTex), fireNear = sprites(root, 150, flameTex), smoke = sprites(root, 70, smokeTex, false), torchFl = sprites(root, 3, flameTex), stripFire = sprites(root, 150, flameTex);
const fireLights = [0, 1, 2].map(() => { const l = new THREE.PointLight(0xff7a20, 0, 40, 1.2); root.add(l); return l; });
// characters (white heads, Comicron style)
const strawHat = hg => { const m = flat(0xe2c26a); M(cyl(0.45, 0.55, 0.5, 24), m, { ol: 0.045, p: [0, 0.48, 0], to: hg }); M(cyl(1.0, 1.0, 0.05, 32), m, { ol: 0.04, p: [0, 0.24, 0], to: hg }); M(cyl(0.555, 0.555, 0.1, 24), flat(0xd63b2f), { p: [0, 0.3, 0], to: hg, cast: false }); };
const capF = (col) => hg => { const m = flat(col); M(new THREE.SphereGeometry(0.62, 32, 16, 0, Math.PI * 2, 0, Math.PI * 0.36), m, { ol: 0.045, p: [0, 0.1, -0.03], s: [1.06, 0.72, 1.1], to: hg }); M(cyl(0.38, 0.4, 0.06, 24), m, { ol: 0.04, p: [0, 0.3, 0.52], s: [1.1, 1, 0.6], r: [0.12, 0, 0], to: hg }); };
const chefHat = hg => { const m = flat(0xfbfaf4); M(cyl(0.5, 0.42, 0.34, 28), m, { ol: 0.045, p: [0, 0.48, 0], to: hg }); for (let i = 0; i < 7; i++) { const a = i / 7 * 6.283; M(sph(0.3, 16, 12), m, { ol: 0.04, p: [Math.cos(a) * 0.3, 0.98, Math.sin(a) * 0.3], to: hg }); } };
const farmer = makeChar3({ freckles: true, shoe: 0x3a2416, scarf: 0xd63b2f, belt3d: 0x5a3a22, body: (g, w, h) => { g.fillStyle = '#f2c230'; g.fillRect(0, 0, w, h); g.strokeStyle = 'rgba(160,110,20,0.45)'; g.lineWidth = 6; for (let x = 0; x < w; x += 44) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, h); g.stroke(); } for (let y = 0; y < h; y += 44) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); } g.fillStyle = '#3b5bd9'; g.fillRect(w * 0.28, h * 0.35, w * 0.44, h * 0.65); g.fillRect(w * 0.3, h * 0.1, w * 0.06, h * 0.3); g.fillRect(w * 0.64, h * 0.1, w * 0.06, h * 0.3); g.fillStyle = '#ffd34d'; for (const x of [0.33, 0.67]) { g.beginPath(); g.arc(w * x, h * 0.36, 9, 0, 7); g.fill(); } }, hat: strawHat });
const neighbour = makeChar3({ stache: true, shoe: 0x1b1522, belt3d: 0x3a2416, buttons3d: 0xf3efe6, body: (g, w, h) => { g.fillStyle = '#b3272d'; g.fillRect(0, 0, w, h); g.strokeStyle = 'rgba(40,10,10,0.35)'; g.lineWidth = 6; for (let x = 0; x < w; x += 40) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, h); g.stroke(); } for (let y = 0; y < h; y += 40) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); } g.fillStyle = '#3a3345'; g.fillRect(0, h * 0.72, w, h * 0.28); }, hat: capF(0x3a3345) });
const baker = makeChar3({ stache: true, beard: null, shoe: 0x3a2416, scarf: 0xf2c230, body: (g, w, h) => { g.fillStyle = '#f3efe6'; g.fillRect(0, 0, w, h); g.fillStyle = 'rgba(200,180,140,0.5)'; for (let i = 0; i < 30; i++) { g.beginPath(); g.arc(Math.random() * w, Math.random() * h, 6 + Math.random() * 10, 0, 7); g.fill(); } }, hat: chefHat });
const folkCols = ['#3f8f8a', '#b0567a', '#c98a2a', '#5a6ab0', '#2f6b4f', '#8a3a5a'];
const folk = folkCols.map((c, i) => makeChar3({ freckles: i % 3 === 0, stache: i % 3 === 1, shoe: 0x3a2416, belt3d: i % 2 ? 0x3a2416 : null, collar: i % 2 ? null : 0xf3efe6, body: bodyTex(c, '#1b1522', { apron: i % 3 === 2 }), hat: i % 2 ? hoodHat([0xd9b36a, 0x57b0aa, 0xd9869f][i % 3]) : capF([0x5a3a2a, 0x2a3552, 0x6a2f3a][i % 3]) }));
const CAST = [farmer, neighbour, baker, ...folk]; CAST.forEach(c => root.add(c.g));
// props: torch, buckets, bread basket, rake
const torch = new THREE.Group(); root.add(torch); M(cyl(0.05, 0.06, 1.2, 8), toon(0x6b4326), { ol: 0.015, p: [0, -0.5, 0], to: torch }); M(cyl(0.11, 0.08, 0.22, 10), toon(0x3a2416), { ol: 0.015, p: [0, 0.1, 0], to: torch });
const buckets = []; for (let i = 0; i < 6; i++) { const g = new THREE.Group(); M(new THREE.CylinderGeometry(0.22, 0.17, 0.36, 14, 1, true), toon(0x8a5a34, { side: THREE.DoubleSide }), { ol: 0.015, to: g }); M(new THREE.CircleGeometry(0.2, 14), flat(0x5fb4e6), { p: [0, 0.12, 0], r: [-Math.PI / 2, 0, 0], to: g, cast: false }); M(new THREE.TorusGeometry(0.22, 0.015, 6, 16, Math.PI), flat(INK), { p: [0, 0.18, 0], to: g, cast: false }); root.add(g); buckets.push(g); }
const basket = new THREE.Group(); root.add(basket); M(cyl(0.45, 0.35, 0.3, 16, true), toon(0xc98a3a, { side: THREE.DoubleSide }), { ol: 0.02, to: basket }); for (let i = 0; i < 5; i++) M(sph(0.16, 12, 8), toon(0xc98a3a), { ol: 0.015, p: [-0.25 + i * 0.12, 0.18, (i % 2) * 0.12 - 0.06], s: [1.8, 0.8, 0.9], to: basket }); M(new THREE.TorusGeometry(0.42, 0.03, 6, 16, Math.PI), toon(0x8a5a34), { p: [0, 0.15, 0], to: basket });
const rake = new THREE.Group(); root.add(rake); M(cyl(0.035, 0.035, 2.0, 8), toon(0x7a5232), { ol: 0.012, p: [0, 1.0, 0], to: rake }); M(box(0.8, 0.06, 0.06), toon(0x8a8a96), { ol: 0.012, p: [0, 0.02, 0], to: rake }); for (let i = 0; i < 8; i++) M(box(0.025, 0.16, 0.025), toon(0x8a8a96), { p: [-0.35 + i * 0.1, -0.06, 0], to: rake, cast: false });
const sky = (() => { const t = ctex(16, 256, g => { }); const m = M(new THREE.SphereGeometry(260, 32, 16), new THREE.MeshBasicMaterial({ map: t, side: THREE.BackSide, fog: false }), { cast: false }); root.add(m); m.userData.t = t; return m; })();
function skyAt(top, mid, bot) { const g = sky.userData.t.userData.g; const r = g.createLinearGradient(0, 0, 0, 256); r.addColorStop(0, top); r.addColorStop(0.6, mid); r.addColorStop(1, bot); g.fillStyle = r; g.fillRect(0, 0, 16, 256); sky.userData.t.needsUpdate = true; }
const sunDisc = M(sph(9, 24, 16), flat(0xffd27a, { fog: false }), { cast: false }); root.add(sunDisc);
root.fog = new THREE.Fog(0xe8b88a, 60, 230);
const SETS = [world, sky, sunDisc, torch, basket, rake, ...buckets, ...CAST.map(c => c.g)];
const FIRES = [...fireFar, ...fireMid, ...fireNear, ...smoke, ...torchFl, ...stripFire];
function hideAll() { SETS.forEach(g => g.visible = false); FIRES.forEach(s => s.visible = false); fireLights.forEach(l => l.intensity = 0); }
function hold(c, hand, obj, off = V(0, 0, 0), rot = [0, 0, 0]) { c.g.updateMatrixWorld(true); const p = V(...hand); c.up.localToWorld(p); obj.visible = true; obj.position.copy(p).add(off); obj.rotation.set(...rot); }
function torchIn(c, hand, t) { hold(c, hand, torch, V(0, 0.45, 0), [0, 0, 0.15]); torch.updateMatrixWorld(true); const tip = torch.localToWorld(V(0, 0.2, 0)); fireAt(torchFl, [tip], t, 0.9); fireLights[0].position.copy(tip).add(V(0, 0.4, 0.3)); fireLights[0].intensity = 6; }
// mood: smoky orange afternoon (danger approaching) → red-orange evening (fire arrives) → soft sunset
function farmLook(t, danger = 0.4) { world.visible = true; sky.visible = true; sunDisc.visible = true; skyAt(danger > 0.6 ? '#5a3a4a' : '#6a8ad0', danger > 0.6 ? '#c05a30' : '#e8b88a', '#ffd6a0'); bg(0xe8b88a); root.fog.color.set(danger > 0.6 ? 0xc08060 : 0xe8c8a0); sunDisc.position.set(-40, 26, -200); sunDisc.material.color.set(danger > 0.5 ? 0xff7a30 : 0xffe0a0);
  light(0.75, 1.6, [-30, 30, -40], 0xffe0b8, 0x6a5a4a); LOOK.grade = ['#ff9a4a', 0.12 + 0.12 * danger]; LOOK.bloom = 0.28; if (mill.userData.sails) mill.userData.sails.rotation.z = t * 0.6; }
// ===== detail pass: ground scatter, trees, house dressing, barn planks, village props, clouds, birds, chickens =====
const DT = { anim: [] };
const rep2 = (t, a, b) => { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(a, b); return t; };
// --- roof shingles on every roof ---
roofM.color.set(0xffffff); roofM.map = rep2(ctex(256, 256, (g, w, h) => { g.fillStyle = '#7a3428'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 28) for (let x = (y / 28 % 2) * 21 - 42; x < w; x += 42) { g.fillStyle = `hsl(${8 + rnd() * 10},${42 + rnd() * 14}%,${34 + rnd() * 12}%)`; g.beginPath(); g.roundRect(x + 2, y + 2, 38, 26, [0, 0, 10, 10]); g.fill(); g.fillStyle = 'rgba(0,0,0,0.25)'; g.fillRect(x + 2, y + 24, 38, 4); } }), 0.5, 0.5); roofM.needsUpdate = true;
// --- barn: vertical red planks with white trim, hayloft door, weathervane ---
{ const body = barn.children[0]; body.material = toon(0xffffff, { map: rep2(ctex(256, 256, (g, w, h) => { for (let x = 0; x < w; x += 32) { g.fillStyle = `hsl(${6 + rnd() * 6},${52 + rnd() * 10}%,${36 + rnd() * 8}%)`; g.fillRect(x, 0, 32, h); g.fillStyle = 'rgba(40,10,5,0.55)'; g.fillRect(x, 0, 3, h); for (let k = 0; k < 6; k++) { g.strokeStyle = 'rgba(60,20,10,0.25)'; g.lineWidth = 2; g.beginPath(); const xx = x + 6 + rnd() * 20; g.moveTo(xx, rnd() * h); g.lineTo(xx + (rnd() - 0.5) * 4, rnd() * h); g.stroke(); } g.fillStyle = '#2a1a14'; g.beginPath(); g.arc(x + 16, 30, 2.5, 0, 7); g.arc(x + 16, h - 30, 2.5, 0, 7); g.fill(); } }), 2, 1.5) });
  const tr = toon(0xf3efe6); for (const [x, y, z, w, h, d] of [[-3, 2, 2.52, 0.18, 4, 0.12], [3, 2, 2.52, 0.18, 4, 0.12], [0, 3.95, 2.52, 6.1, 0.18, 0.12], [0, 0.1, 2.52, 6.1, 0.18, 0.12], [-1.25, 1.55, 2.62, 0.14, 3.1, 0.1], [1.25, 1.55, 2.62, 0.14, 3.1, 0.1], [0, 3.05, 2.62, 2.6, 0.14, 0.1]]) M(box(w, h, d), tr, { ol: 0.015, p: [x, y, z], to: barn });
  M(box(1.2, 1.1, 0.1), toon(0x7a2f2a), { ol: 0.02, p: [0, 5.0, 2.62], to: barn }); for (const s of [-1, 1]) M(box(0.1, 1.4, 0.08), tr, { p: [s * 0.2, 5.0, 2.69], r: [0, 0, s * 0.72], to: barn, cast: false });
  for (let i = 0; i < 9; i++) M(box(0.06, 0.32 + rnd() * 0.2, 0.06), toon(0xe2c26a), { p: [-0.4 + i * 0.1, 4.45, 2.68], r: [0, 0, (rnd() - 0.5) * 0.8], to: barn, cast: false });
  const wv = new THREE.Group(); wv.position.set(0, 6.6, 0); barn.add(wv); const blk = toon(0x2a2430); M(cyl(0.03, 0.03, 1.0, 6), blk, { p: [0, 0.5, 0], to: wv }); M(box(0.9, 0.04, 0.04), blk, { p: [0, 0.75, 0], to: wv }); M(box(0.04, 0.04, 0.9), blk, { p: [0, 0.75, 0], to: wv }); const rooster = new THREE.Shape(); rooster.moveTo(-0.4, 0); rooster.lineTo(0.3, 0); rooster.lineTo(0.42, 0.25); rooster.lineTo(0.3, 0.32); rooster.lineTo(0.2, 0.15); rooster.lineTo(-0.1, 0.2); rooster.lineTo(-0.35, 0.45); rooster.lineTo(-0.45, 0.2); rooster.closePath(); M(new THREE.ExtrudeGeometry(rooster, { depth: 0.03, bevelEnabled: false }), blk, { p: [0, 1.0, 0], to: wv });
  // hay spilling out of the door and a pitchfork
  for (let i = 0; i < 40; i++) M(box(0.04, 0.02, 0.5), toon(0xe2c26a), { p: [(rnd() - 0.5) * 2.2, 0.03, 2.9 + rnd() * 0.9], r: [0, rnd() * 3, 0], to: barn, cast: false });
  const pf = new THREE.Group(); pf.position.set(2.0, 0, 2.8); pf.rotation.set(-0.25, 0, 0.12); barn.add(pf); M(cyl(0.03, 0.03, 1.8, 6), toon(0x7a5232), { ol: 0.01, p: [0, 0.9, 0], to: pf }); for (const x of [-0.12, 0, 0.12]) M(cyl(0.015, 0.008, 0.4, 5), toon(0x8a8a96), { p: [x, 1.95, 0], to: pf }); M(box(0.3, 0.03, 0.03), toon(0x8a8a96), { p: [0, 1.76, 0], to: pf }); }
// --- houses: 3D windows with shutters and flower boxes, doors with steps, chimneys with pots ---
const shutC = [0x3f7f6a, 0x2f5a9a, 0x9a3a3a, 0x5a7a2a, 0x2f6b8a];
village.children.forEach((h, hi) => { if (h === mill) return; const w = h === bakery ? 4.6 : 4.4, ht = h === bakery ? 4.2 : 4.4, sc = toon(shutC[hi % shutC.length]);
  for (const side of [1, -1]) { const z = side * 2.02, rz = side > 0 ? 0 : Math.PI; const fr = new THREE.Group(); fr.position.set(0, 0, z); fr.rotation.y = rz; h.add(fr);
    const wins = side > 0 ? [[-1.3, ht * 0.66], [1.3, ht * 0.66]] : [[-1.3, ht * 0.66], [1.3, ht * 0.66], [-1.3, ht * 0.24], [1.3, ht * 0.24]];
    for (const [x, y] of wins) { M(box(0.8, 0.9, 0.06), flat(0x2a3a52), { p: [x, y, 0.02], to: fr, cast: false }); M(box(0.7, 0.8, 0.02), toon(0xbfe0f0, { transparent: true, opacity: 0.55 }), { p: [x, y, 0.06], to: fr, cast: false }); M(box(0.06, 0.9, 0.08), toon(0xf3efe6), { p: [x, y, 0.07], to: fr, cast: false }); M(box(0.8, 0.06, 0.08), toon(0xf3efe6), { p: [x, y, 0.07], to: fr, cast: false });
      M(box(0.96, 0.1, 0.16), toon(0xf3efe6), { ol: 0.012, p: [x, y + 0.5, 0.08], to: fr }); for (const s of [-1, 1]) { M(box(0.38, 0.92, 0.06), sc, { ol: 0.012, p: [x + s * 0.62, y, 0.08], to: fr }); for (let k = 0; k < 4; k++) M(box(0.32, 0.03, 0.02), toon(0x1b1522), { p: [x + s * 0.62, y - 0.3 + k * 0.2, 0.12], to: fr, cast: false }); }
      if (y > ht * 0.5 || side > 0) { M(box(0.96, 0.22, 0.26), toon(0x7a5232), { ol: 0.012, p: [x, y - 0.56, 0.16], to: fr }); for (let k = 0; k < 7; k++) { M(sph(0.07, 8, 6), toon(0x4f8a3a), { p: [x - 0.38 + k * 0.127, y - 0.42, 0.18 + (k % 2) * 0.06], to: fr, cast: false }); M(sph(0.055, 8, 6), toon([0xe2453a, 0xf2c230, 0xf3efe6, 0xe07ab0][(k + hi) % 4]), { p: [x - 0.38 + k * 0.127, y - 0.36, 0.2 + (k % 2) * 0.06], to: fr, cast: false }); } } }
    if (side > 0) { M(box(1.0, 1.9, 0.08), toon(0xffffff, { map: T2s.panel }), { ol: 0.015, p: [0, 0.95, 0.05], to: fr }); M(box(1.2, 0.12, 0.14), toon(0xf3efe6), { ol: 0.012, p: [0, 1.96, 0.08], to: fr }); M(sph(0.05, 8, 6), toon(0xd9b36a), { p: [0.35, 0.95, 0.12], to: fr, cast: false }); M(box(1.4, 0.16, 0.6), toon(0xffffff, { map: T2s.stone }), { ol: 0.012, p: [0, 0.08, 0.3], to: fr }); M(sph(0.12, 10, 8), glowTex ? toon(0xffd27a) : toon(0xffd27a), { p: [0.75, 2.1, 0.14], to: fr, cast: false });
      for (const s of [-1, 1]) { M(cyl(0.18, 0.14, 0.3, 12), toon(0xb3672d), { ol: 0.012, p: [s * 0.9, 0.15, 0.4], to: fr }); M(sph(0.24, 10, 8), toon(0x4f8a3a), { ol: 0.012, p: [s * 0.9, 0.42, 0.4], to: fr }); } } }
  M(cyl(0.12, 0.12, 0.3, 8), toon(0xb3672d), { ol: 0.01, p: [w * 0.25, ht + 2.5, -0.6], to: h });
  // picket fence along the front garden
  if (h !== bakery) for (let i = -6; i <= 6; i++) { if (Math.abs(i) < 2) continue; M(box(0.1, 0.7, 0.05), toon(0xf3efe6), { ol: 0.008, p: [i * 0.36, 0.35, 3.4], to: h }); } if (h !== bakery) for (const y of [0.25, 0.55]) for (const s of [-1, 1]) M(box(1.6, 0.06, 0.04), toon(0xf3efe6), { p: [s * 1.45, y, 3.38], to: h, cast: false });
});
// --- windmill: door, small windows, stone base ---
{ M(box(0.9, 1.6, 0.1), toon(0xffffff, { map: T2s.panel }), { ol: 0.015, p: [0, 0.8, 1.98], r: [-0.08, 0, 0], to: mill }); for (const y of [3.2, 5.0]) M(box(0.5, 0.6, 0.1), flat(0x2a3a52), { p: [0, y, 1.62 - (y - 3.2) * 0.05], to: mill, cast: false }); M(cyl(2.1, 2.2, 0.6, 16), toon(0xffffff, { map: T2s.stone }), { ol: 0.02, p: [0, 0.3, 0], to: mill }); }
// --- bakery: striped awning, bread table, flour sacks, barrels ---
{ const aw = ctex(256, 64, (g, w, h) => { for (let x = 0; x < w; x += 32) { g.fillStyle = (x / 32) % 2 ? '#f3efe6' : '#c8402f'; g.fillRect(x, 0, 32, h); } }); M(box(4.0, 0.06, 1.2), toon(0xffffff, { map: aw }), { ol: 0.015, p: [0, 2.6, 2.6], r: [0.35, 0, 0], to: bakery }); for (let i = 0; i < 8; i++) M(new THREE.ConeGeometry(0.25, 0.25, 3), toon(i % 2 ? 0xf3efe6 : 0xc8402f), { p: [-1.75 + i * 0.5, 2.28, 3.2], r: [Math.PI, 0, 0], to: bakery, cast: false });
  const tb = new THREE.Group(); tb.position.set(1.1, 0, 3.0); bakery.add(tb); M(box(1.8, 0.08, 0.8), toon(0xffffff, { map: T2s.wood }), { ol: 0.015, p: [0, 0.9, 0], to: tb }); for (const [x, z] of [[-0.8, -0.32], [0.8, -0.32], [-0.8, 0.32], [0.8, 0.32]]) M(box(0.08, 0.9, 0.08), toon(0x6b4326), { p: [x, 0.45, z], to: tb });
  for (let i = 0; i < 6; i++) { const lf = M(sph(0.16, 14, 10), toon(0xc98a3a), { ol: 0.012, p: [-0.65 + i * 0.26, 1.02, (i % 2 ? 0.15 : -0.15)], s: [1.7, 0.75, 0.9], r: [0, 0.3 * (i % 3 - 1), 0], to: tb }); for (let k = -1; k <= 1; k++) M(box(0.03, 0.02, 0.18), toon(0xf3d9a0), { p: [-0.65 + i * 0.26 + k * 0.08, 1.13, (i % 2 ? 0.15 : -0.15)], to: tb, cast: false }); }
  for (let i = 0; i < 3; i++) M(sph(0.26, 12, 10), toon(0xefe6d2), { ol: 0.015, p: [-1.9 + i * 0.12, 0.3, 2.6 + i * 0.4], s: [1, 1.3, 0.9], to: bakery });
  for (const [x, z] of [[2.7, 2.4], [2.9, 3.2]]) { const b = M(cyl(0.34, 0.34, 0.9, 16), toon(0xffffff, { map: T2s.wood }), { ol: 0.015, p: [x, 0.45, z], to: bakery }); for (const y of [-0.3, 0.3]) M(cyl(0.355, 0.355, 0.05, 16, true), toon(0x3a3440), { p: [0, y, 0], to: b, cast: false }); } }
// --- village well (square between the houses) and a cart by the barn ---
{ const wl = new THREE.Group(); wl.position.set(-2.9, 0, 17.5); village.add(wl); M(cyl(0.9, 0.95, 0.9, 18), toon(0xffffff, { map: T2s.stone }), { ol: 0.02, p: [0, 0.45, 0], to: wl }); M(cyl(0.72, 0.72, 0.05, 18), flat(0x2a4a6a), { p: [0, 0.86, 0], to: wl, cast: false }); for (const s of [-1, 1]) M(box(0.12, 1.8, 0.12), toon(0x6b4326), { ol: 0.012, p: [s * 0.85, 1.6, 0], to: wl }); M(cyl(0.06, 0.06, 1.9, 8), toon(0x6b4326), { p: [0, 2.2, 0], r: [0, 0, Math.PI / 2], to: wl }); const rf = new THREE.Shape(); rf.moveTo(-1.2, 0); rf.lineTo(1.2, 0); rf.lineTo(0, 0.8); rf.closePath(); M(new THREE.ExtrudeGeometry(rf, { depth: 1.3, bevelEnabled: false }), roofM, { ol: 0.02, p: [0, 2.45, -0.65], to: wl }); M(cyl(0.18, 0.15, 0.3, 10), toon(0x8a5a34), { ol: 0.01, p: [0.4, 1.2, 0], to: wl }); M(cyl(0.006, 0.006, 1.0, 4), toon(0x3a2416), { p: [0.4, 1.75, 0], to: wl, cast: false }); }
{ const ct = new THREE.Group(); ct.position.set(24.2, 0, 13.2); ct.rotation.y = -0.5; world.add(ct); M(box(1.6, 0.12, 2.6), toon(0xffffff, { map: T2s.wood }), { ol: 0.02, p: [0, 0.9, 0], to: ct }); for (const s of [-1, 1]) M(box(0.08, 0.5, 2.6), toon(0xffffff, { map: T2s.wood }), { ol: 0.015, p: [s * 0.78, 1.2, 0], to: ct }); M(box(1.6, 0.5, 0.08), toon(0xffffff, { map: T2s.wood }), { ol: 0.015, p: [0, 1.2, -1.28], to: ct });
  for (const s of [-1, 1]) { const wh = new THREE.Group(); wh.position.set(s * 0.95, 0.62, 0.2); wh.rotation.z = Math.PI / 2; ct.add(wh); M(new THREE.TorusGeometry(0.55, 0.06, 8, 24), toon(0x5a3a22), { ol: 0.012, r: [Math.PI / 2, 0, 0], to: wh }); for (let k = 0; k < 6; k++) M(box(0.04, 1.05, 0.04), toon(0x6b4326), { r: [0, k * Math.PI / 6, 0], to: wh, cast: false }); M(cyl(0.1, 0.1, 0.14, 10), toon(0x3a2416), { to: wh }); }
  for (const s of [-1, 1]) M(cyl(0.04, 0.04, 2.2, 6), toon(0x6b4326), { p: [s * 0.4, 0.55, 2.2], r: [1.25, 0, 0], to: ct }); for (let i = 0; i < 3; i++) M(sph(0.3, 12, 10), toon(0xefe6d2), { ol: 0.012, p: [-0.4 + i * 0.4, 1.2, -0.5], s: [1, 0.8, 1.2], to: ct }); M(cyl(0.6, 0.6, 1.0, 16), toon(0xe2c26a), { ol: 0.02, p: [0.2, 1.4, 0.6], r: [0, 0, Math.PI / 2], to: ct }); }
// --- trees around the village and field edges (round leafy trees, two greens) ---
const leafM = [toon(0x4f8a3a), toon(0x3f7a34), toon(0x6a9a40)];
function leafTree(x, z, s) { const g = new THREE.Group(); g.position.set(x, 0, z); g.scale.setScalar(s); world.add(g); M(cyl(0.18, 0.28, 2.2, 8), trunkM, { ol: 0.02, p: [0, 1.1, 0], to: g }); for (const [dx, dy, dz, r] of [[0, 2.9, 0, 1.25], [0.8, 2.5, 0.2, 0.9], [-0.75, 2.6, -0.1, 0.95], [0.1, 3.6, 0.3, 0.8], [-0.2, 2.4, 0.75, 0.8]]) M(sph(r, 14, 10), leafM[Math.floor(rnd() * 3)], { ol: 0.03, p: [dx, dy, dz], to: g }); return g; }
for (const [x, z] of [[-10, 11], [10.5, 23.5], [-10.5, 24], [-2.5, 31], [10, 31], [-19, 13], [16, 21], [-20, 21], [28.5, 8], [28.5, -2], [29, -12], [-29, -1], [-29.5, -11], [-29, 7], [-23, 26], [21, 26], [27, 18], [-27, 16], [14.5, 29], [-14.5, 30]]) leafTree(x, z, 0.8 + rnd() * 0.45);
// --- ground scatter: grass tufts, wildflowers, stones along the road (instanced) ---
function inField(x, z) { return (z < Z0 + 0.4 && z > Z1 - 0.4 && Math.abs(x) > 1.4 && Math.abs(x) < 26.4); }
function blocked(x, z) { if (inField(x, z) || Math.abs(x) < 1.7) return true; for (const h of village.children) { const d = Math.hypot(x - h.position.x, z - h.position.z); if (d < 3.1) return true; } if (Math.abs(x - 20) < 3.4 && Math.abs(z - 9) < 2.9) return true; return false; }
{ const tuftG = new THREE.ConeGeometry(0.07, 0.42, 4); tuftG.translate(0, 0.2, 0); const tuft = new THREE.InstancedMesh(tuftG, toon(0xffffff), 14000), cA = new THREE.Color(0x5f8f3a), cB = new THREE.Color(0x8ab84f); let k = 0;
  for (let i = 0; i < 40000 && k < 14000; i++) { const x = -40 + rnd() * 80, z = -28 + rnd() * 66; if (blocked(x, z)) continue; for (let b = 0; b < 3 && k < 14000; b++) { dummy.position.set(x + (rnd() - 0.5) * 0.18, 0, z + (rnd() - 0.5) * 0.18); dummy.rotation.set((rnd() - 0.5) * 0.6, rnd() * 6, (rnd() - 0.5) * 0.6); dummy.scale.setScalar(0.6 + rnd() * 0.8); dummy.updateMatrix(); tuft.setMatrixAt(k, dummy.matrix); tuft.setColorAt(k, tmpC.copy(cA).lerp(cB, rnd())); k++; } }
  tuft.count = k; world.add(tuft);
  const flG = new THREE.SphereGeometry(0.07, 6, 4); flG.translate(0, 0.32, 0); const fl = new THREE.InstancedMesh(flG, flat(0xffffff), 3200); const fc = [0xe2453a, 0xf2c230, 0xffffff, 0xe07ab0, 0x7a8ae6]; k = 0;
  for (let i = 0; i < 20000 && k < 3200; i++) { const x = -40 + rnd() * 80, z = -28 + rnd() * 66; if (blocked(x, z)) continue; dummy.position.set(x, 0, z); dummy.rotation.set(0, 0, 0); dummy.scale.setScalar(0.8 + rnd() * 0.6); dummy.updateMatrix(); fl.setMatrixAt(k, dummy.matrix); fl.setColorAt(k, tmpC.set(fc[Math.floor(rnd() * 5)])); k++; } fl.count = k; world.add(fl);
  // poppies along the field edges
  const pp = new THREE.InstancedMesh(flG, flat(0xffffff), 260); k = 0; for (let i = 0; i < 260; i++) { const side = [-1.9, 1.9, -26.5, 26.5][i % 4]; dummy.position.set(side + (rnd() - 0.5) * 0.5, 0.25 + rnd() * 0.3, Z1 + rnd() * (Z0 - Z1)); dummy.scale.setScalar(0.9 + rnd() * 0.5); dummy.updateMatrix(); pp.setMatrixAt(k, dummy.matrix); pp.setColorAt(k, tmpC.set([0x7a8ae6, 0xffffff, 0xb07ad8][i % 3])); k++; } world.add(pp);
  const stG = new THREE.DodecahedronGeometry(0.12, 0); const st = new THREE.InstancedMesh(stG, toon(0xffffff), 1400); k = 0; for (let i = 0; i < 1400; i++) { const s = i % 2 ? 1 : -1; dummy.position.set(s * (1.45 + rnd() * 0.25), 0.03, -26 + rnd() * 62); dummy.rotation.set(rnd() * 3, rnd() * 3, rnd() * 3); dummy.scale.set(0.6 + rnd() * 1.4, 0.4 + rnd() * 0.5, 0.6 + rnd() * 1.4); dummy.updateMatrix(); st.setMatrixAt(k, dummy.matrix); st.setColorAt(k, tmpC.setHSL(0.08, 0.08, 0.45 + rnd() * 0.2)); k++; } world.add(st);
  // cart-wheel ruts on the dirt road
  for (const s of [-0.6, 0.6]) M(box(0.22, 0.02, 60), flat(0x7a5a3a, { transparent: true, opacity: 0.6 }), { p: [s, 0.075, 0], to: world, cast: false }); }
// --- clouds and pines on the hill tops ---
{ const cm = toon(0xfff3e6); for (const [x, y, z, s] of [[-60, 46, -150, 1.4], [20, 55, -170, 1.8], [80, 44, -140, 1.2], [-110, 50, -120, 1.5], [120, 52, -110, 1.3], [-20, 62, -190, 2.0]]) { const g = new THREE.Group(); g.position.set(x, y, z); g.scale.setScalar(s); world.add(g); for (const [dx, dy, r] of [[0, 0, 6], [6, -1.5, 4.5], [-6, -1.6, 4.6], [3, 2.8, 4.2], [-3, 2.2, 4], [10, -2.6, 3]]) M(sph(r, 16, 10), cm, { p: [dx, dy, 0], s: [1, 0.75, 0.6], to: g, cast: false }); } }
for (let i = 0; i < 60; i++) { const x = -90 + rnd() * 180, z = -58 - rnd() * 18; const g = new THREE.Group(); g.position.set(x, 4 + 6 * Math.max(0, 1 - Math.abs(x) / 90), z); g.scale.setScalar(1.6 + rnd()); world.add(g); M(new THREE.ConeGeometry(0.9, 2.2, 8), pineM, { p: [0, 1.6, 0], to: g, cast: false }); M(new THREE.ConeGeometry(0.7, 1.7, 8), pineM, { p: [0, 2.6, 0], to: g, cast: false }); }
// --- birds fleeing the fire (flapping V shapes) ---
{ const bg_ = new THREE.BufferGeometry(); bg_.setAttribute('position', new THREE.Float32BufferAttribute([-0.6, 0.15, 0, 0, 0, 0, 0, 0, 0.05, 0.6, 0.15, 0, 0, 0, 0, 0, 0, 0.05], 3)); const bm = flat(0x2a2430, { side: THREE.DoubleSide });
  const birds = []; for (let i = 0; i < 24; i++) { const b = new THREE.Mesh(bg_, bm); b.userData = { x: -40 + rnd() * 80, y: 14 + rnd() * 12, z: -50 + rnd() * 30, sp: 3 + rnd() * 2, ph: rnd() * 6 }; world.add(b); birds.push(b); }
  DT.anim.push(t => birds.forEach(b => { const u = b.userData; b.position.set(u.x + Math.sin(t * 0.3 + u.ph) * 3, u.y + Math.sin(t * 2 + u.ph) * 0.4, u.z + ((t * u.sp + u.ph * 10) % 90)); const f = Math.sin(t * 12 + u.ph * 5); b.scale.set(1.4, 1.4 * f, 1.4); })); }
// --- chickens pecking by the barn ---
{ const hens = []; for (let i = 0; i < 5; i++) { const c = new THREE.Group(); const x = 16 + rnd() * 6, z = 12 + rnd() * 2.5; c.position.set(x, 0, z); c.rotation.y = rnd() * 6; world.add(c); const col = i % 2 ? 0xf3efe6 : 0xb3672d; M(sph(0.22, 14, 10), toon(col), { ol: 0.012, p: [0, 0.32, 0], s: [1, 0.85, 1.3], to: c }); M(new THREE.ConeGeometry(0.12, 0.25, 8), toon(col), { p: [0, 0.48, -0.26], r: [-0.8, 0, 0], to: c }); const hd = new THREE.Group(); hd.position.set(0, 0.5, 0.22); c.add(hd); M(sph(0.11, 12, 8), toon(col), { ol: 0.01, to: hd }); M(new THREE.ConeGeometry(0.04, 0.1, 6), toon(0xf2a230), { p: [0, -0.01, 0.13], r: [Math.PI / 2, 0, 0], to: hd }); M(box(0.03, 0.08, 0.12), toon(0xd8322a), { p: [0, 0.11, 0], to: hd }); for (const s of [-1, 1]) { M(sph(0.018, 6, 4), flat(0x111111), { p: [s * 0.08, 0.03, 0.06], to: hd, cast: false }); M(cyl(0.012, 0.012, 0.2, 4), toon(0xf2a230), { p: [s * 0.07, 0.1, 0], to: c }); } hens.push([c, hd, rnd() * 6]); }
  DT.anim.push(t => hens.forEach(([c, hd, ph]) => { const p = Math.max(0, Math.sin(t * 3 + ph)); hd.position.set(0, 0.5 - 0.3 * p * p, 0.22 + 0.12 * p * p); })); }
// run the animated details inside the shared mood function
const _farmLook0 = farmLook; farmLook = function (t, d) { _farmLook0(t, d); DT.anim.forEach(f => f(t)); };
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

  if (li === 0) { // HOOK: he lights his own wheat; behind, a wildfire on the hills
    const tw = wf(0, 'while') - 0.1; farmLook(t, 0.5);
    fireAt(fireFar, hillLine, t, 9); smokeAt(smoke, hillLine, t, 30, 14);
    if (t < tw) { show(farmer, 10, -18.0, -0.35); farmer.face('neutral'); const low = ss(0.6, 1.8, t); farmer.pose({ pitch: 0.35 * low, rh: [0.55, lerp(2.3, 1.2, low), 0.7], lh: [-0.5, 1.95, 0.05], hx: 0.2 * low }); torchIn(farmer, [0.55, lerp(2.3, 1.2, low), 0.7], t);
      const ig = sub(1.8, tw), pts = []; for (let i = 0; i < 18; i++) pts.push(V(9.4 + (i % 6) * 0.5, 0, -16.6 + Math.floor(i / 6) * 0.45)); fireAt(stripFire, pts.slice(0, Math.floor(ig * 18)), t, 1.6 * ig + 0.4); fireLights[1].position.set(10.5, 1.5, -17.5); fireLights[1].intensity = 10 * ig;
      const hp = farmer.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x - 0.8, hp.y - 0.5, hp.z + lerp(6.0, 5.0, sub(0, tw))], [hp.x - 0.2, hp.y - 1.3, hp.z], 48, t, 0, -0.05);
    } else { const u = sub(tw, s1); setCam([lerp(-1, 1, u), lerp(10, 14, u), lerp(34, 28, u)], [0, lerp(4, 7, u), -60], 54, t, 0, 0.0);
      overlay = () => popText('WILDFIRE', W / 2, 260, 150, '#ff7a30', t, wf(0, 'wildfire') - 0.05, s1 - 0.02); }
  }
  else if (li === 1) { // the whole village runs out with buckets
    farmLook(t, 0.5); fireAt(fireFar, hillLine, t, 9); smokeAt(smoke, hillLine, t, 30, 14); const u = sub(s0, s1);
    folk.forEach((c, i) => { const z = lerp(17, 8, u) - (i % 3) * 1.6, x = (i % 2 ? 1 : -1) * (0.6 + (i % 3) * 0.5); show(c, x, z, Math.PI); c.face('shock'); c.pose({ ...c.walk(t * 10 + i, 0.32), rh: [0.55, 1.4, 0.25], lh: [-0.6, 2.4, 0.1], lean: 0.08 * Math.sin(t * 10 + i) }); hold(c, [0.55, 1.4, 0.25], buckets[i], V(0, -0.25, 0)); });
    setCam([lerp(2.5, 1.5, u), 2.6, lerp(3.0, 0.5, u)], [0, 2.2, 14], 52, t, 0.006, 0.04);
  }
  else if (li === 2) { // he walks out of the barn with a torch
    farmLook(t, 0.5); const u = sub(s0, s1); show(farmer, lerp(19.5, 17.0, u), 13.0, -Math.PI / 2 - 0.25); farmer.face('neutral'); farmer.pose({ ...farmer.walk(t * 6, 0.24), rh: [0.55, 2.6, 0.4], lh: [-0.5, 1.95, 0.05] }); torchIn(farmer, [0.55, 2.6, 0.4], t);
    const hp = farmer.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x - 5.2, hp.y - 0.6, hp.z - 1.4], [hp.x, hp.y - 1.3, hp.z], 52, t, 0, 0.06);
  }
  else if (li === 3) { // neighbour: are you trying to help it?
    farmLook(t, 0.5); show(neighbour, -3.2, -2, 0.5); const ty = wf(3, 'are') - 0.1; neighbour.face(t > ty ? 'angry' : 'shock'); neighbour.pose({ rh: [0.8, 2.9 + 0.1 * Math.sin(t * 9), 0.4], lh: [-0.8, 2.9 + 0.1 * Math.cos(t * 9), 0.4], bob: 0.03 * Math.abs(Math.sin(t * 9)) });
    const hp = neighbour.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 0.9, hp.y - 0.3, hp.z + lerp(4.4, 3.8, k)], [hp.x + 0.2, hp.y - 0.4, hp.z], 44, t, 0, -0.05); LOOK.dof = [380, 1400, 5];
    overlay = () => burst('HELP IT?!', 540, 360, 210, t, wf(3, 'help') - 0.1, s1 - 0.02, -0.06);
  }
  else if (li === 4) { // the baker just wants to know who's buying his bread now
    farmLook(t, 0.5); show(baker, 2.8, 11.6, -0.5); baker.face('sad'); baker.pose({ rh: [0.5, 1.95, 0.6], lh: [-0.5, 1.95, 0.6], hz: 0.1 * Math.sin(t * 3) }); hold(baker, [0, 1.95, 0.75], basket, V(0, -0.15, 0.25), [0, 0, 0]);
    const hp = baker.headG.getWorldPosition(V(0, 0, 0)); setCam([0.6, hp.y - 0.4, hp.z + lerp(4.2, 3.6, k)], [hp.x + 0.6, hp.y - 0.7, hp.z - 1], 48, t, 0, 0.04);
  }
  else lateShots(t, li, s0, s1, k, sub);
}
// ---------- lines 5–24 ----------
const fwd = ry => V(Math.sin(ry), 0, Math.cos(ry));
const headOf = c => c.headG.getWorldPosition(V(0, 0, 0));
const ROYAL = 0x2346c8;
function stripFlames(bx, t, w = 5) { const pts = []; for (let i = 0; i < 50; i++) { const x = bx - (i % 10) / 10 * w, z = -21.6 + Math.floor(i / 10) * 1.0; if (x > 2 && x < 26.2) pts.push(V(x, 0, z)); } fireAt(stripFire, pts.length ? pts : [V(-999, -99, 0)], t, 1.7, pts.length ? 1 : 0); return pts; }
function lineX(x0, x1, z, step, y = 0) { const a = []; for (let x = x0; x <= x1; x += step) a.push(V(x, y, z + 0.6 * Math.sin(x * 1.7))); return a; }
function rakeAt(c, ry, t, sw = 0) { const f = fwd(ry), p = c.g.position; rake.visible = true; const d = 1.05 + sw; rake.position.set(p.x + f.x * d, 0, p.z + f.z * d); rake.rotation.set(0, ry, 0); rake.rotateX(-0.55); }
function cheer(c, t, i) { c.face('happy'); c.pose({ rh: [0.8, 2.9 + 0.12 * Math.sin(t * 9 + i), 0.4], lh: [-0.8, 2.9 + 0.12 * Math.cos(t * 9 + i), 0.4], bob: 0.05 * Math.abs(Math.sin(t * 9 + i)) }); }
function sunsetLook(t) { farmLook(t, 0.3); skyAt('#3a3a7a', '#e8706a', '#ffc080'); bg(0xf0a080); root.fog.color.set(0xe8a088); sunDisc.position.set(70, 10, -200); sunDisc.material.color.set(0xffb070); sunDisc.scale.setScalar(1.8); light(0.7, 1.4, [60, 14, -60], 0xffc0a0, 0x5a4a6a); LOOK.grade = ['#ff7a8a', 0.16]; }
function explainerLook() { root.fog = null; bg(ROYAL); xp.visible = true; flameC.visible = plate.visible = car.visible = false; meal.forEach(s => s.visible = false); light(0.95, 1.3, [4, 10, 9], 0xffffff, 0x8a9ae6); LOOK.grade = ['#ffffff', 0.0]; LOOK.bloom = 0.1; }

function lateShots(t, li, s0, s1, k, sub) {
  if (li === 5) { // burns one long strip across the far edge, then rakes it flat
    farmLook(t, 0.5); fireAt(fireFar, hillLine, t, 9); smokeAt(smoke, hillLine, t, 30, 14);
    const bx = lastBX, tr = wf(5, 'right') - 0.1, tk = wf(5, 'raked') - 0.1;
    if (t < tr) { show(farmer, Math.min(bx + 0.9, 25), -19.6, Math.PI / 2 - 0.5); farmer.face('think'); farmer.pose({ ...farmer.walk(t * 6, 0.22), rh: [0.55, 1.5, 0.7], lh: [-0.5, 1.95, 0.05], pitch: 0.15 }); torchIn(farmer, [0.55, 1.5, 0.7], t); stripFlames(bx, t);
      const hp = headOf(farmer); setCam([hp.x + 1.2, hp.y - 0.3, hp.z + 7.6], [hp.x - 0.4, hp.y - 1.5, hp.z], 52, t, 0, 0.04);
      overlay = () => { popText('ONE LONG', W / 2, 250, 120, '#ffffff', t, wf(5, 'one') - 0.05, tr); popText('STRIP', W / 2, 390, 150, '#ffb02e', t, wf(5, 'strip') - 0.05, tr); };
    } else if (t < tk) { stripFlames(bx, t, 7); const u = sub(tr, tk); setCam([lerp(-0.5, 1.0, u), lerp(7, 8, u), -14.5], [20, 0, -20], 54, t, 0, 0.03);
    } else { show(farmer, 16, -19.4, 0.25); farmer.face('neutral'); const sw = 0.35 * Math.sin(t * 6); farmer.pose({ rh: [0.2, 2.0, 0.5 + sw * 0.6], lh: [-0.1, 1.65, 0.75 + sw * 0.6], pitch: 0.2, lean: 0.05 * sw }); rakeAt(farmer, 0.25, t, sw);
      const hp = headOf(farmer); setCam([hp.x + 0.8, hp.y - 0.6, hp.z + lerp(5.2, 4.4, sub(tk, s1))], [hp.x + 0.2, hp.y - 1.5, hp.z], 48, t, 0, -0.04); LOOK.dof = [380, 1400, 4]; }
  }
  else if (li === 6) { // black ash; the last stalk falls
    farmLook(t, 0.5); fireAt(fireFar, hillLine, t, 9); smokeAt(smoke, hillLine, t, 30, 14);
    show(farmer, 13.6, -18.7, -0.6); farmer.face('neutral'); farmer.pose({ rh: [0.2, 2.0, 0.5], lh: [-0.1, 1.65, 0.75] }); rakeAt(farmer, -0.6, t);
    const ep = []; for (let i = 0; i < 40; i++) ep.push(V(10.5 + (i * 0.37) % 4, 0.06, -21.5 + ((i * 0.61) % 4.2))); embersAt(ep, t, 0.3); smokeAt(smoke, ep.slice(0, 12), t * 2, 4, 1.4);
    lone.visible = true; lone.position.set(12.3, 0.04, -18.9); const fall = ss(0, 1, sub(wf(6, 'not') + 0.2, wf(6, 'not') + 0.7)); lone.rotation.set(-fall * 1.5, 0.4, 0);
    setCam([lerp(11.0, 11.3, k), 0.75, lerp(-17.0, -17.5, k)], [12.4, 0.35, -20.0], 46, t, 0, 0.05); LOOK.dof = [300, 1500, 3];
    overlay = () => { popText('BLACK', W / 2, 250, 140, '#ffffff', t, s0 + 0.05, s1); popText('ASH', W / 2, 400, 170, '#ffb02e', t, s0 + 0.2, s1); };
  }
  else if (li === 7) { // the village laughs: "the Matchstick"
    farmLook(t, 0.5); const u = sub(s0, s1); show(farmer, 0.1, lerp(10.0, 7.2, u), Math.PI); farmer.face('sad'); farmer.pose({ ...farmer.walk(t * 5, 0.18), rh: [0.2, 2.0, 0.5], lh: [-0.1, 1.65, 0.75] }); rakeAt(farmer, Math.PI, t);
    [[-2.3, 11.8, 0.9], [2.4, 11.4, -0.9], [-3.0, 13.0, 0.7], [3.1, 12.8, -0.7], [-2.0, 14.2, 0.5], [2.2, 14.0, -0.5]].forEach(([x, z, r], i) => { const c = folk[i]; show(c, x, z, r + Math.PI); c.face('happy'); const pt = i % 2 ? [-0.9, 2.5, 0.8] : [0.9, 2.5, 0.8]; c.pose({ rh: i % 2 ? [0.5, 1.6, 0.4] : pt, lh: i % 2 ? pt : [-0.5, 1.6, 0.4], bob: 0.05 * Math.abs(Math.sin(t * 12 + i)), lean: 0.06 * Math.sin(t * 12 + i) }); });
    show(baker, 4.6, 12.6, -2.2); baker.face('happy'); baker.pose({ rh: [0.5, 1.6, 0.5], lh: [-0.5, 1.6, 0.5], bob: 0.04 * Math.abs(Math.sin(t * 11)) });
    setCam([lerp(0.9, 0.6, u), 2.6, lerp(-0.5, 0.5, u)], [0.2, 2.2, 10], 52, t, 0, -0.03);
    overlay = () => { popText('THE', W / 2, 250, 110, '#ffffff', t, wf(7, 'matchstick') - 0.25, s1); popText('MATCHSTICK', W / 2, 380, 150, '#ffb02e', t, wf(7, 'matchstick') - 0.05, s1); };
  }
  else if (li === 8) { // and the wildfire kept coming
    farmLook(t, 0.75); fireAt(fireFar, hillLine, t, lerp(10, 13, k)); smokeAt(smoke, hillLine, t, 40, 18);
    show(farmer, 6.6, -4.5, Math.PI - 0.3); farmer.face('think'); farmer.pose({ rh: [0.2, 2.0, 0.5], lh: [-0.1, 1.65, 0.75] }); rakeAt(farmer, Math.PI - 0.3, t);
    setCam([lerp(8.2, 7.8, k), 3.2, lerp(3.4, 1.8, k)], [2, 7, -60], 52, t, 0, 0.02);
  }
  else if (li === 9) { // first the hills, then the forest
    farmLook(t, 0.8); const tt = wf(9, 'then') - 0.1; fireAt(fireFar, hillLine, t, 13); smokeAt(smoke, hillLine, t, 40, 18);
    if (t < tt) setCam([lerp(-4, -2, sub(s0, tt)), 11, -10], [-6, 9, -62], 30, t, 0, 0.02);
    else { const g = ss(0, 1, sub(tt, tt + 0.6)); fireAt(fireMid, forestLine, t, 8 * g + 0.5); fireLights[1].position.set(0, 5, -36); fireLights[1].intensity = 30 * g; setCam([lerp(2, 1, sub(tt, s1)), 3.2, -17], [0, 4.5, -42], 52, t, 0.01, -0.03); }
    overlay = () => { popText('HILLS', W / 2, 260, 150, '#ffffff', t, wf(9, 'hills') - 0.05, tt); popText('FOREST', W / 2, 260, 150, '#ffb02e', t, wf(9, 'forest') - 0.05, s1); };
  }
  else if (li === 10) { // the smoke turned the sun orange
    farmLook(t, 0.9); skyAt('#3a2830', '#8a3a28', '#c06030'); sunDisc.material.color.set(0xff6a1a); sunDisc.scale.setScalar(2.4); sunDisc.position.set(-14, 34, -110); sunDisc.scale.setScalar(1.3); sunDisc.material.transparent = true; sunDisc.material.depthTest = false; sunDisc.renderOrder = 999; fireAt(fireFar, hillLine, t, 13); fireAt(fireMid, forestLine, t, 8); smokeAt(smoke, hillLine, t, 40, 14); LOOK.grade = ['#ff6a2a', 0.3];
    setCam([lerp(2, 0, k), 2.0, -6], [-11, lerp(22, 25, k), -110], 40, t, 0, 0.0);
    overlay = () => { popText('ORANGE', W / 2, 1500, 160, '#ff7a30', t, wf(10, 'orange') - 0.05, s1); };
  }
  else if (li === 11) { // the neighbour's wheat, tall and golden
    farmLook(t, 0.6); fireAt(fireFar, hillLine, t, 13); smokeAt(smoke, hillLine, t, 40, 18); fireAt(fireMid, forestLine, t, 8);
    show(neighbour, -21.5, 7.3, 0.1); neighbour.face('happy'); neighbour.pose({ rh: [-0.25, 1.85, 0.62], lh: [0.25, 1.75, 0.66], pitch: -0.1, hy: 0.1 * Math.sin(t * 2) });
    const hp = headOf(neighbour); setCam([hp.x - 0.4, 1.3, hp.z + lerp(5.6, 4.8, k)], [hp.x, hp.y - 0.6, hp.z], 50, t, 0, 0.03); LOOK.dof = [420, 1500, 3];
    overlay = () => { popText('TALL &', W / 2, 250, 120, '#ffffff', t, wf(11, 'tall') - 0.05, s1); popText('GOLDEN', W / 2, 390, 160, '#ffd34d', t, wf(11, 'golden') - 0.05, s1); };
  }
  else if (li === 12) { // his own field: a burnt pancake
    farmLook(t, 0.6); fireAt(fireFar, hillLine, t, 13); smokeAt(smoke, hillLine, t, 40, 18); fireAt(fireMid, forestLine, t, 8);
    setCam([lerp(12, 13, k), lerp(24, 21, k), lerp(-5, -7, k)], [13, 0, -18.5], 52, t, 0, 0.0);
    overlay = () => { popText('BURNT', W / 2, 250, 130, '#ffffff', t, wf(12, 'burnt') - 0.05, s1); popText('PANCAKE', W / 2, 390, 160, '#ffb02e', t, wf(12, 'pancake') - 0.05, s1); };
  }
  else if (li === 13) { // then, the fire reached the farms
    farmLook(t, 0.85); fireAt(fireFar, hillLine, t, 9); smokeAt(smoke, hillLine, t, 40, 18); fireAt(fireMid, forestLine, t, 6);
    const g = ss(0, 1, sub(s0, s0 + 0.7)); fireAt(fireNear, lineX(-26, 26, -24.5, 1.05), t, 4.2 * g + 0.3); fireLights[2].position.set(0, 4, -20); fireLights[2].intensity = 20 * g; LOOK.bloom = 0.12;
    setCam([1.0, 2.1, lerp(-7, -9, k)], [0, 2.4, -30], 54, t, 0.015 * g, 0.03);
    overlay = () => burst('WHOOSH!', 540, 330, 220, t, s0 + 0.1, s0 + 1.2, -0.08);
  }
  else if (li === 14) { // it roared through the neighbour's wheat
    farmLook(t, 0.85); smokeAt(smoke, hillLine, t, 40, 18); const nf = lastNF; fireAt(fireNear, lineX(-26, -2.5, Math.min(nf, Z0), 0.5), t, 4, nf < Z0 + 1 ? 1 : 0); fireLights[2].position.set(-14, 4, nf + 2); fireLights[2].intensity = 20; LOOK.bloom = 0.12;
    fireAt(fireMid, lineX(-26, -2.5, Math.min(nf, Z0) - 4, 1.0), t, 2.4);
    setCam([lerp(-1.2, -1.6, k), lerp(9, 10, k), 12.5], [-13, 0, lerp(-10, -4, k)], 56, t, 0.01, 0.0);
    overlay = () => popText('IN SECONDS', W / 2, 260, 140, '#ffb02e', t, wf(14, 'seconds') - 0.1, s1);
  }
  else if (li === 15) { // it raced toward the village
    farmLook(t, 0.9); smokeAt(smoke, hillLine, t, 40, 18); const fz = lerp(-34, -23.4, ss(0, 1, sub(s0, s1 + 0.4))); fireAt(fireNear, lineX(2, 26, fz, 0.55), t, 4.5); fireLights[2].position.set(14, 4, fz + 3); fireLights[2].intensity = 22; LOOK.bloom = 0.12;
    setCam([14, 1.3, lerp(-17.6, -18.4, k)], [14, 2.4, -32], 58, t, 0.03, 0.05);
  }
  else if (li === 16) { // it hits the black strip — and just stops
    farmLook(t, 0.85); smokeAt(smoke, hillLine, t, 40, 18); const ts = wf(16, 'stopped') - 0.05, die = 1 - ss(0, 1, sub(ts, ts + 0.9)), fz = lerp(-24.5, -22.5, sub(s0, ts));
    fireAt(fireNear, lineX(2, 26, fz, 0.55), t, 4.5 * die + 0.01, die > 0.02 ? 1 : 0); fireLights[2].position.set(14, 4, fz + 3); fireLights[2].intensity = 22 * die; LOOK.bloom = 0.12;
    if (die < 0.9) { const ep = lineX(2, 26, -22.4, 0.5, 0.1); embersAt(ep, t, 0.4); smokeAt(smoke, lineX(4, 24, -23, 1.2), t * 1.5, 8, 4); }
    show(farmer, 13.4, -12.6, 0.15); farmer.face(t > ts + 0.4 ? 'happy' : 'sneaky'); farmer.pose({ rh: [0.2, 2.0, 0.5], lh: [-0.1, 1.65, 0.75], hz: 0.06 * Math.sin(t * 2) }); rakeAt(farmer, 0.15, t);
    const hp = headOf(farmer); setCam([hp.x + 1.0, hp.y - 0.5, hp.z + lerp(6.0, 5.0, k)], [hp.x + 0.2, hp.y - 1.2, hp.z - 4], 50, t, 0, -0.04);
    overlay = () => { popText('JUST', W / 2, 250, 120, '#ffffff', t, ts - 0.2, s1); popText('STOPPED', W / 2, 390, 160, '#8fd04a', t, ts, s1); };
  }
  // ---------- "You see," explainer on royal blue ----------
  else if (li >= 17 && li <= 21) { explainerLook(); const cm = [0, 1.55, lerp(8.8, 8.2, k)];
    if (li === 17) { flameC.visible = true; flameC.position.set(0, -0.2, 0); flameAnim(t, 0.25 + 0.15 * Math.abs(Math.sin(t * 8)), 1, [0, 0]); setCam(cm, [0, 1.4, 0], 45, t, 0, 0.03);
      overlay = () => { popText('YOU SEE,', W / 2, 260, 130, '#ffffff', t, s0 + 0.05, wf(17, 'fire') - 0.1); popText("CAN'T", W / 2, 250, 120, '#ffffff', t, wf(17, 'doesn') - 0.05, s1); popText('WALK', W / 2, 390, 160, '#ffd34d', t, wf(17, 'move') - 0.05, s1); }; }
    else if (li === 18) { flameC.visible = true; flameC.position.set(0, -0.2, 0); const te = s0 + 0.12, q = sub(te, te + 0.35); const s = meal[0]; s.visible = q < 1; s.position.set(lerp(2.4, 0, q), lerp(0.2, 0.25, q) + Math.sin(q * Math.PI) * 0.8, lerp(0.6, 1.1, q)); s.rotation.set(0, 0, lerp(0.3, Math.PI / 2, q)); s.scale.setScalar(0.62 * (1 - 0.6 * q));
      flameAnim(t, q < 1 ? 0.3 + 0.7 * q : 0.15 + 0.35 * Math.abs(Math.sin(t * 16)), 1.03, [0.6, -0.2]); setCam([0, 1.55, 7.4], [0, 1.4, 0], 45, t, 0, -0.03);
      overlay = () => burst('CHOMP!', 540, 340, 220, t, te + 0.25, s1 + 0.05, 0.08); }
    else if (li === 19) { flameC.visible = true; flameC.position.set(0, 0.1, -0.6); plate.visible = true; plate.position.set(0, -0.4, 1.0); const n = Math.floor(sub(s0 + 0.5, s0 + 0.5 + 4 * 0.42) * 4.001); let open = 0.2;
      meal.forEach((s, i) => { if (i === 0) return; const j = i - 1; const q = cl((t - (s0 + 0.5 + j * 0.42)) / 0.3); s.visible = q < 1; const qq = ss(0, 1, q); s.position.set(lerp(-0.85, 0.0, qq), lerp(-0.28, 0.6, qq) + Math.sin(q * Math.PI) * 0.5, lerp(0.55 + j * 0.24, 0.45, qq)); s.rotation.set(0, 0.12 * (j - 1.5), -Math.PI / 2 + q * 0.6); s.scale.setScalar(0.55 * (1 - 0.6 * q)); if (q > 0 && q < 1) open = 0.9; });
      flameAnim(t, open + 0.1 * Math.sin(t * 20), 1.0, [0, -0.6]); setCam([0, 2.2, 7.6], [0, 0.9, 0], 45, t, 0, 0.02);
      overlay = () => { popText('A MEAL', W / 2, 260, 160, '#ffd34d', t, wf(19, 'meal') - 0.05, s1); }; }
    else if (li === 20) { flameC.visible = true; const tf = wf(20, 'fire') - 0.1; plate.visible = true; plate.position.set(lerp(0, 4.5, ss(0, 1, sub(s0 + 0.1, s0 + 0.7))), -0.4, 1.0); const sh = ss(0, 1, sub(tf, s1 - 0.1)); flameC.position.set(0, 0.1 - 0.2 * sh, -0.6);
      flameAnim(t, 0.12, lerp(1, 0.32, sh), [1 - sh, -0.4], sh); setCam([0, 2.0, 7.6], [0, 0.9, 0], 45, t, 0, -0.02); puffAt(V(0, 1.1, -0.4), t, s1 - 0.5, 1.4);
      overlay = () => { popText('STARVES', W / 2, 260, 160, '#8fd04a', t, wf(20, 'starves') - 0.05, s1); }; }
    else { car.visible = true; const tr = wf(21, 'runs') - 0.1, ar = ss(0, 1, sub(s0, s0 + 0.9)), stop = ss(0, 1, sub(tr, tr + 0.5)); const x = lerp(-5.5, -0.4, ar) + 0.6 * stop; car.position.set(x, -0.2, 0); car.rotation.set(0, -0.35, 0.025 * Math.sin(t * 30) * (1 - stop) - 0.04 * Math.sin(stop * Math.PI)); car.userData.wheels.forEach(w => w.rotation.z = -x * 2.4);
      puffAt(V(x - 1.8, 0.4, -0.5), t, tr + 0.2, 1.0, 8); setCam([0, 1.9, 10.6], [0, 1.0, 0], 45, t, 0, 0.02);
      overlay = () => { gauge(t, lerp(0.22, 0, sub(s0 + 0.2, tr + 0.3)), W / 2, 520); popText('NO PETROL', W / 2, 220, 120, '#ffffff', t, wf(21, 'petrol') - 0.1, s1); }; }
  }
  else if (li === 22) { // firefighters still do this today
    farmLook(t, 0.4); truck.visible = true; const u = sub(s0, s1);
    ffs.forEach((c, i) => { const x = lerp(35.5, 38.0, u) - i * 2.4, z = -27.2 - i * 0.3; show(c, x, z, Math.PI / 2 - 0.55); c.face(i ? 'think' : 'neutral'); const hd = [0.6, 1.55, 0.55]; c.pose({ ...c.walk(t * 5 + i * 2, 0.18), rh: hd, lh: [-0.5, 1.9, 0.1] }); hold(c, hd, drips[i], V(0, -0.15, 0), [0, Math.PI / 2 - 0.55, 0]); });
    const pts = []; for (let i = 0; i < 24; i++) { const x = 31 + i * 0.3; if (x < lerp(35.5, 38, u) - 0.4) pts.push(V(x, 0, -27.4 + 0.15 * Math.sin(i))); } fireAt(dripFl, pts.length ? pts : [V(-999, -99, 0)], t, 1.1, pts.length ? 1 : 0);
    drips.forEach(d => { d.updateMatrixWorld(true); }); fireAt(torchFl, drips.map(d => d.localToWorld(d.userData.tip.clone())), t, 0.45);
    setCam([lerp(39.6, 39.2, u), 2.3, -21.2], [36.0, 1.5, -28], 50, t, 0, 0.03);
    overlay = () => { popText('STILL', W / 2, 250, 120, '#ffffff', t, wf(22, 'still') - 0.05, s1); popText('TODAY', W / 2, 390, 160, '#ffb02e', t, wf(22, 'today') - 0.05, s1); };
  }
  else if (li === 23) { // by sunset, every house still standing
    sunsetLook(t); smokeAt(smoke, hillLine.filter((_, i) => i % 4 === 0), t, 20, 8); const u = sub(s0, s1);
    [[-1.4, 18.6], [1.3, 18.9], [-2.2, 20.2], [2.4, 20.0], [0.0, 20.8], [-0.6, 19.3]].forEach(([x, z], i) => { const c = folk[i]; show(c, x, z, (x > 0 ? -0.3 : 0.3)); cheer(c, t, i); });
    setCam([lerp(1.5, 2.5, u), lerp(7, 11, u), lerp(31, 27, u)], [0, lerp(3, 1, u), lerp(10, 4, u)], 56, t, 0, 0.0);
  }
  else if (li === 24) { // the man who started a fire was the only one who stopped it
    sunsetLook(t); const tb = wf(24, 'stopped') - 0.05, out = ss(0, 1, sub(tb, tb + 0.5));
    show(farmer, 0.3, 16.6, 0.05); farmer.face(t > tb + 0.6 ? 'happy' : 'neutral'); farmer.pose({ rh: [0.55, 2.3, 0.75], lh: [-0.5, 1.95, 0.6], hx: -0.05 }); torchIn(farmer, [0.55, 2.3, 0.75], t); torchFl.forEach(s => s.scale.multiplyScalar(1 - out)); fireLights[0].intensity = 6 * (1 - out); if (out > 0) puffAt(torch.localToWorld(V(0, 0.4, 0)), t, tb + 0.2, 0.5, 8);
    [[-1.6, 14.4], [1.8, 14.2], [-2.8, 13.6], [2.9, 13.4], [-0.6, 13.2], [0.8, 12.9]].forEach(([x, z], i) => { const c = folk[i]; show(c, x, z, 0.0 + (x > 0 ? -0.25 : 0.25)); cheer(c, t, i); });
    show(baker, 1.8, 16.9, -0.7); baker.face('happy'); baker.pose({ rh: [0.5, 1.95, 0.6], lh: [-0.5, 1.95, 0.6] }); hold(baker, [0, 1.95, 0.75], basket, V(0, -0.15, 0.25), [0, 0, 0]);
    const hp = headOf(farmer), u = sub(s0, s1); setCam([hp.x + 0.6, hp.y - 0.5, hp.z + lerp(7.0, 4.2, ss(0, 1, u))], [hp.x + 0.1, hp.y - lerp(1.2, 0.8, u), hp.z], 48, t, 0, 0.03); LOOK.dof = [420, 1500, 3];
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
