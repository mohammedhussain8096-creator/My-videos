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

// ===== The Puddle General — Comicron-style castle, cellar, camp =====
const FT = []; function ftex(w, h, d) { const t = ctex(w, h, d); t.userData.draw = d; FT.push(t); return t; }
window.afterFonts = () => FT.forEach(t => { t.userData.draw(t.userData.g, t.userData.c.width, t.userData.c.height); t.needsUpdate = true; });
Object.assign(sun.shadow.camera, { left: -30, right: 30, top: 30, bottom: -30, near: 1, far: 120 }); sun.shadow.camera.updateProjectionMatrix(); sun.shadow.mapSize.set(4096, 4096); sun.shadow.bias = -0.0006;
const glowTex = ctex(128, 128, g => { const r = g.createRadialGradient(64, 64, 0, 64, 64, 64); r.addColorStop(0, 'rgba(255,240,190,1)'); r.addColorStop(0.35, 'rgba(255,180,80,0.5)'); r.addColorStop(1, 'rgba(255,150,50,0)'); g.fillStyle = r; g.fillRect(0, 0, 128, 128); });
function glow(parent, x, y, z, s = 1.2, op = 0.9) { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: op })); sp.position.set(x, y, z); sp.scale.set(s, s, 1); parent.add(sp); return sp; }
const flames = [];
function candle(parent, x, y, z, h = 0.35) { M(cyl(0.06, 0.07, h, 10), toon(0xfbf6e4), { ol: 0.012, p: [x, y + h / 2, z], to: parent }); const f = M(new THREE.ConeGeometry(0.045, 0.14, 8), flat(0xffc040), { p: [x, y + h + 0.07, z], to: parent, cast: false }); flames.push(f); glow(parent, x, y + h + 0.08, z, 0.9, 0.85); }
function torch(parent, x, y, z) { M(box(0.1, 0.5, 0.1), toon(0x5a3a22), { ol: 0.015, p: [x, y, z], to: parent }); for (let i = 0; i < 3; i++) { const f = M(new THREE.ConeGeometry(0.12 - i * 0.03, 0.4, 8), flat(i ? 0xffb030 : 0xff6a20), { p: [x, y + 0.42, z], to: parent, cast: false }); flames.push(f); } glow(parent, x, y + 0.45, z, 2.0, 0.85); const pl = new THREE.PointLight(0xffa040, 5, 7, 1.6); pl.position.set(x, y + 0.5, z + 0.2); parent.add(pl); }
const sparkTex = ctex(32, 32, g => { const r = g.createRadialGradient(16, 16, 0, 16, 16, 16); r.addColorStop(0, 'rgba(255,255,220,1)'); r.addColorStop(0.4, 'rgba(255,190,60,0.9)'); r.addColorStop(1, 'rgba(255,120,0,0)'); g.fillStyle = r; g.fillRect(0, 0, 32, 32); });
const sparks = []; for (let i = 0; i < 40; i++) { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: sparkTex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true })); s.scale.setScalar(0.12); root.add(s); sparks.push(s); }

// ---------- props ----------
const bowlGeo = (() => { const pts = []; for (let i = 0; i <= 10; i++) { const s = i / 10; pts.push(new THREE.Vector2(0.12 + 0.2 * Math.sin(s * Math.PI / 2), s * 0.16)); } return new THREE.LatheGeometry(pts, 24); })();
const clayM = toon(0xb8673e, { side: THREE.DoubleSide }), waterM = flat(0x5fb4e6);
function makeBowl() { const g = new THREE.Group(); M(bowlGeo, clayM, { ol: 0.018, to: g }); const w = M(new THREE.CircleGeometry(0.3, 24), waterM, { p: [0, 0.13, 0], r: [-Math.PI / 2, 0, 0], to: g, cast: false }); w.material = waterM; g.userData.rings = [0, 1, 2].map(() => { const r = M(new THREE.TorusGeometry(1, 0.06, 4, 32), flat(0xffffff, { transparent: true, opacity: 0.9 }), { p: [0, 0.14, 0], r: [Math.PI / 2, 0, 0], to: g, cast: false }); r.visible = false; return r; }); M(box(0.06, 0.012, 0.18), flat(0xffffff, { transparent: true, opacity: 0.5 }), { p: [-0.08, 0.135, -0.06], r: [0, 0.6, 0], to: g, cast: false }); return g; }
function ripple(b, t, on, speed = 1) { b.userData.rings.forEach((r, i) => { r.visible = on; if (!on) return; const p = ((t * 1.6 * speed + i / 3) % 1); const s = 0.04 + p * 0.25; r.scale.set(s, s, s * 0.4); r.material.opacity = 0.9 * (1 - p); }); }
const sword = new THREE.Group(); root.add(sword); M(box(0.08, 1.1, 0.02), toon(0xd8dee8), { ol: 0.012, p: [0, 0.6, 0], to: sword }); M(box(0.36, 0.06, 0.06), toon(0xd9a53a), { ol: 0.012, p: [0, 0.04, 0], to: sword }); M(cyl(0.03, 0.03, 0.26, 8), toon(0x5a3a22), { p: [0, -0.12, 0], to: sword });
const jug = new THREE.Group(); root.add(jug); { const pts = []; for (let i = 0; i <= 12; i++) { const s = i / 12; pts.push(new THREE.Vector2(0.09 + 0.12 * Math.sin(s * Math.PI) - (s > 0.85 ? 0.05 : 0), s * 0.42)); } M(new THREE.LatheGeometry(pts, 20), toon(0x9a5a34, { side: THREE.DoubleSide }), { ol: 0.018, to: jug }); M(new THREE.TorusGeometry(0.08, 0.02, 6, 12, Math.PI), toon(0x9a5a34), { p: [0.18, 0.25, 0], r: [0, 0, -Math.PI / 2], to: jug }); }
const pour = M(cyl(0.025, 0.04, 1, 8), flat(0x8fd0ff, { transparent: true, opacity: 0.85 }), { cast: false }); root.add(pour);
const ladle = new THREE.Group(); root.add(ladle); M(cyl(0.03, 0.03, 1.1, 8), toon(0x8a5a34), { ol: 0.015, p: [0, 0.55, 0], to: ladle }); M(new THREE.SphereGeometry(0.13, 12, 8, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), toon(0xb9bfca, { side: THREE.DoubleSide }), { ol: 0.015, to: ladle });

// ---------- characters (white heads, like Comicron) ----------
const kettleHat = (col, brim) => hg => { const m = flat(col); M(new THREE.SphereGeometry(0.62, 32, 16, 0, Math.PI * 2, 0, Math.PI * 0.5), m, { ol: 0.045, p: [0, 0.08, -0.02], s: [1, 0.85, 1], to: hg }); M(cyl(0.82, 0.82, 0.05, 36), flat(brim), { ol: 0.04, p: [0, 0.22, -0.05], r: [-0.18, 0, 0], to: hg }); M(new THREE.TorusGeometry(0.62, 0.035, 6, 32), flat(0xd9a53a), { p: [0, 0.14, -0.02], r: [Math.PI / 2, 0, 0], to: hg, cast: false }); };
const plumeHelm = hg => { const m = flat(0xb9c2d0); M(new THREE.SphereGeometry(0.64, 32, 16, 0, Math.PI * 2, 0, Math.PI * 0.55), m, { ol: 0.045, p: [0, 0.04, -0.03], to: hg });  for (let i = 0; i < 5; i++) M(sph(0.16, 10, 8), flat(0xd63b2f), { ol: 0.025, p: [0, 0.72 + i * 0.05, -0.15 - i * 0.16], to: hg }); };
const knightHelm = hg => { const m = flat(0x9aa3b5); M(cyl(0.6, 0.62, 0.9, 28), m, { ol: 0.045, p: [0, 0.2, -0.02], to: hg }); M(new THREE.SphereGeometry(0.6, 28, 12, 0, Math.PI * 2, 0, Math.PI / 2), m, { ol: 0.04, p: [0, 0.64, -0.02], to: hg }); M(box(0.9, 0.06, 0.05), flat(0x15111b), { p: [0, 0.18, 0.6], to: hg, cast: false }); };
const chefHat = hg => { const m = flat(0xfbfaf4); M(cyl(0.5, 0.42, 0.34, 28), m, { ol: 0.045, p: [0, 0.48, 0], to: hg }); for (let i = 0; i < 7; i++) { const a = i / 7 * 6.283; M(sph(0.3, 16, 12), m, { ol: 0.04, p: [Math.cos(a) * 0.3, 0.98, Math.sin(a) * 0.3], to: hg }); } M(sph(0.36, 16, 12), m, { ol: 0.04, p: [0, 1.1, 0], to: hg }); };
const quilt = (base, line) => (g, w, h) => { g.fillStyle = base; g.fillRect(0, 0, w, h); g.strokeStyle = line; g.lineWidth = 5; for (let x = -h; x < w + h; x += 48) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x + h * 0.6, h); g.stroke(); g.beginPath(); g.moveTo(x + h * 0.6, 0); g.lineTo(x, h); g.stroke(); } };
const otto = makeChar3({ beard: '#d9d4c8', wrinkles: true, shoe: 0x3a2416, belt3d: 0x5a3a22, scarf: 0x6a2f3a, body: quilt('#9a7a52', 'rgba(70,45,25,0.5)'), hat: kettleHat(0x7d8496, 0x6a7182) });
const captain = makeChar3({ stache: true, shoe: 0x1b1522, belt3d: 0x2a2530, body: (g, w, h) => { g.fillStyle = '#b9c2d0'; g.fillRect(0, 0, w, h); g.fillStyle = '#d63b2f'; g.fillRect(w * 0.18, 0, w * 0.64, h); g.fillStyle = '#f3efe6'; g.fillRect(w * 0.44, h * 0.1, w * 0.12, h * 0.5); g.fillRect(w * 0.3, h * 0.25, w * 0.4, h * 0.1); }, hat: plumeHelm });
const knights = [0, 1].map(i => makeChar3({ stache: i === 1, shoe: 0x1b1522, belt3d: 0x3a2416, body: (g, w, h) => { g.fillStyle = '#9aa3b5'; g.fillRect(0, 0, w, h); g.strokeStyle = 'rgba(40,40,60,0.35)'; g.lineWidth = 3; for (let y = 0; y < h; y += 16) for (let x = (y / 16 % 2) * 8; x < w; x += 16) { g.beginPath(); g.arc(x, y, 7, 0, Math.PI); g.stroke(); } g.fillStyle = i ? '#2f6b4f' : '#3b5bd9'; g.fillRect(w * 0.25, h * 0.05, w * 0.5, h * 0.75); }, hat: kettleHat(0x9aa3b5, 0x8a92a4) }));
const cook = makeChar3({ stache: true, shoe: 0x3a2416, scarf: 0xd64a3a, belt3d: 0x8a5a34, body: (g, w, h) => { g.fillStyle = '#d64a3a'; g.fillRect(0, 0, w, h); g.fillStyle = '#fbfaf4'; g.fillRect(w * 0.2, h * 0.22, w * 0.6, h * 0.78); g.fillStyle = 'rgba(214,74,58,0.35)'; for (const [x, y] of [[0.35, 0.5], [0.6, 0.62], [0.45, 0.78]]) { g.beginPath(); g.arc(w * x, h * y, 14, 0, 7); g.fill(); } }, hat: chefHat });
const CAST = [otto, captain, ...knights, cook]; CAST.forEach(c => root.add(c.g));

// ---------- CASTLE + COURTYARD ----------
const castle = new THREE.Group(); root.add(castle);
const stoneM = toon(0xffffff, { map: T2s.stone }); const WALLH = 7;
{
  const grass = (() => { const t = ctex(256, 256, (g, w, h) => { g.fillStyle = '#5f8f45'; g.fillRect(0, 0, w, h); for (let i = 0; i < 900; i++) { g.strokeStyle = `rgba(${rnd() < 0.5 ? '50,90,35' : '130,180,90'},0.5)`; g.lineWidth = 2; const x = rnd() * w, y = rnd() * h; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (rnd() - 0.5) * 5, y - 6 - rnd() * 6); g.stroke(); } }); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(40, 40); return t; })();
  M(box(240, 0.2, 240), toon(0xffffff, { map: grass }), { p: [0, -0.1, -60], recv: true, to: castle, cast: false });
  M(box(44, 0.04, 22), toon(0xffffff, { map: T2s.cobble }), { p: [0, 0.02, 11], recv: true, to: castle, cast: false });
  // walls with battlements on four sides
  for (const [x, z, w, d] of [[0, 0, 40, 2.5], [0, 22, 40, 2.5], [-20, 11, 2.5, 22], [20, 11, 2.5, 22]]) { M(box(w, WALLH, d), stoneM, { ol: 0.06, p: [x, WALLH / 2, z], to: castle, recv: true }); const n = Math.floor(Math.max(w, d) / 1.6); for (let i = 0; i <= n; i++) { const k = i / n - 0.5; M(box(w > d ? 0.9 : d === 2.5 ? 1 : 0.9, 1.0, w > d ? 0.9 : 0.9), stoneM, { ol: 0.035, p: [x + (w > d ? k * w : (z === 11 ? 0 : 0)), WALLH + 0.5, z + (w > d ? -0.8 : k * d)], to: castle }); } }
  for (const [x, z] of [[-20, 0], [20, 0], [-20, 22], [20, 22]]) { M(cyl(3, 3.3, 11, 24), stoneM, { ol: 0.06, p: [x, 5.5, z], to: castle }); M(new THREE.ConeGeometry(3.6, 4.5, 24), toon(0x3b4a8a), { ol: 0.06, p: [x, 13.25, z], to: castle }); for (let i = 0; i < 4; i++) { const a = i * Math.PI / 2 + 0.5; M(box(0.6, 1.0, 0.3), flat(0x1a1420), { p: [x + Math.cos(a) * 3.05, 8, z + Math.sin(a) * 3.05], r: [0, -a + Math.PI / 2, 0], to: castle, cast: false }); } M(cyl(0.05, 0.05, 2.5, 6), flat(INK), { p: [x, 16.6, z], to: castle }); M(box(1.4, 0.8, 0.04), flat(0xd63b2f), { ol: 0.02, p: [x + 0.7, 17.4, z], to: castle, cast: false }); }
  // gate
  M(box(5, 5.5, 3), flat(0x15111b), { p: [0, 2.75, 0], to: castle, cast: false }); M(box(5.6, 0.6, 3.2), stoneM, { ol: 0.04, p: [0, 5.8, 0], to: castle }); for (let i = 0; i < 7; i++) M(box(0.12, 5.2, 0.12), toon(0x3a3542), { p: [-2.1 + i * 0.7, 2.7, -1.2], to: castle }); for (let i = 0; i < 6; i++) M(box(4.8, 0.12, 0.12), toon(0x3a3542), { p: [0, 0.4 + i * 0.9, -1.2], to: castle });
  // banners on the inner wall
  for (const x of [-10, -5, 5, 10]) { M(box(1.2, 3.0, 0.05), flat(x % 10 ? 0x3b4a8a : 0xd63b2f), { ol: 0.02, p: [x, 4.4, 1.3], to: castle, cast: false }); M(box(0.5, 0.5, 0.06), flat(0xffd34d), { p: [x, 4.8, 1.32], r: [0, 0, Math.PI / 4], to: castle, cast: false }); }
  // courtyard dressing: well, grindstone, barrels, crates, hay, cart, weapon rack, buildings
  const well = new THREE.Group(); well.position.set(6, 0, 9); castle.add(well); M(cyl(1.1, 1.1, 1.0, 20), stoneM, { ol: 0.04, p: [0, 0.5, 0], to: well }); M(cyl(0.9, 0.9, 1.02, 20, true), toon(0x2a2530, { side: THREE.DoubleSide }), { p: [0, 0.51, 0], to: well, cast: false }); for (const s of [-1, 1]) M(box(0.15, 2.2, 0.15), toon(0x6b4326), { ol: 0.02, p: [s * 1.0, 2.0, 0], to: well }); M(new THREE.ConeGeometry(1.6, 1.0, 4), toon(0x8a3b2c), { ol: 0.04, p: [0, 3.5, 0], r: [0, Math.PI / 4, 0], to: well }); M(cyl(0.08, 0.08, 2.2, 8), toon(0x6b4326), { p: [0, 2.6, 0], r: [0, 0, Math.PI / 2], to: well });
  const gs = new THREE.Group(); gs.position.set(-5, 0, 8); castle.add(gs); for (const s of [-1, 1]) M(box(0.15, 1.1, 0.15), toon(0x6b4326), { ol: 0.02, p: [0, 0.55, s * 0.35], to: gs }); castle.userData.wheel = M(cyl(0.55, 0.55, 0.2, 24), toon(0x8a8a96), { ol: 0.03, p: [0, 1.1, 0], r: [Math.PI / 2, 0, 0], to: gs }); M(box(0.6, 0.5, 0.6), toon(0x6b4326), { ol: 0.02, p: [0.6, 0.25, 0], to: gs });
  const wood = toon(0xffffff, { map: T2s.wood });
  for (const [x, z] of [[-12, 4], [-11.2, 4.4], [-11.6, 5.1], [12, 18], [12.8, 18.4]]) { M(cyl(0.42, 0.38, 1.0, 14), toon(0x8a5a34), { ol: 0.03, p: [x, 0.5, z], to: castle }); for (const y of [0.25, 0.75]) M(new THREE.TorusGeometry(0.43, 0.03, 6, 16), toon(0x2a2530), { p: [x, y, z], r: [Math.PI / 2, 0, 0], to: castle, cast: false }); }
  for (const [x, z, s] of [[-14, 6, 1], [-13.8, 7.2, 0.8], [14, 5, 1]]) M(box(s, s, s), wood, { ol: 0.03, p: [x, s / 2, z], r: [0, 0.3, 0], to: castle });
  for (const [x, z] of [[15, 9], [15.6, 10.3]]) M(cyl(0.7, 0.7, 1.2, 16), toon(0xe2c26a), { ol: 0.03, p: [x, 0.7, z], r: [0, 0, Math.PI / 2], to: castle });
  const rack = new THREE.Group(); rack.position.set(-9, 0, 2.2); castle.add(rack); M(box(3, 0.12, 0.15), toon(0x6b4326), { ol: 0.02, p: [0, 1.6, 0], to: rack }); for (const s of [-1, 1]) M(box(0.12, 1.7, 0.12), toon(0x6b4326), { p: [s * 1.4, 0.85, 0], to: rack }); for (let i = 0; i < 6; i++) { M(cyl(0.025, 0.025, 2.4, 6), toon(0x7a5232), { p: [-1.2 + i * 0.48, 1.3, 0.1], r: [0.12, 0, 0], to: rack }); M(new THREE.ConeGeometry(0.06, 0.25, 6), toon(0xc9ced6), { p: [-1.2 + i * 0.48, 2.55, 0.25], to: rack }); }
  for (const [x, ry, seed, col] of [[-12, 0, 41, '#e8cfa0'], [-4, 0, 43, '#efe2c4'], [4, 0, 45, '#e2c594'], [12, 0, 47, '#ead9b4']]) { const h = new THREE.Group(); h.position.set(x, 0, 19.5); castle.add(h); const m = toon(0xffffff, { map: houseTex(seed, col) }); M(box(6, 5, 3), [m, m, toon(0x8a3b2c), toon(0x8a3b2c), m, m], { ol: 0.05, p: [0, 2.5, 0], to: h }); M(box(6.6, 0.4, 3.6), toon(0x8a3b2c), { ol: 0.04, p: [0, 5.2, 0], to: h }); }
  // the cart of borrowed bowls by the well
  const cart = new THREE.Group(); cart.position.set(3.8, 0, 11.4); cart.rotation.y = 0.5; castle.add(cart); castle.userData.cart = cart; M(box(1.8, 0.4, 1.2), wood, { ol: 0.03, p: [0, 0.7, 0], to: cart }); for (const s of [-1, 1]) M(cyl(0.45, 0.45, 0.1, 18), toon(0x4a2e1c), { ol: 0.025, p: [s * 0.6, 0.45, 0.66], r: [Math.PI / 2, 0, 0], to: cart }); for (let i = 0; i < 12; i++) { const b = makeBowl(); b.position.set(-0.6 + (i % 4) * 0.4, 0.92 + Math.floor(i / 4) * 0.09, -0.3 + Math.floor(i / 4) * 0.3); b.scale.setScalar(0.85); b.children[1].visible = false; cart.add(b); }
  for (const [x, z] of [[-17, 3], [17, 3], [-17, 19], [17, 19], [-1.8, 2.6], [1.8, 2.6]]) torch(castle, x, 2.6, z);
}
// ---------- ARMY CAMP outside (z < 0) ----------
const camp = new THREE.Group(); castle.add(camp); const fires = [];
{ const tentCols = [0xe9dcc0, 0xd63b2f, 0x3b5bd9, 0xe9dcc0, 0x2f6b4f];
  for (let i = 0; i < 70; i++) { const x = -60 + rnd() * 120, z = -28 - rnd() * 70; const s = 1.6 + rnd() * 1.2; M(new THREE.ConeGeometry(s, s * 1.6, 8), toon(tentCols[i % 5]), { ol: 0.06, p: [x, s * 0.8, z], to: camp }); M(cyl(0.04, 0.04, 0.8, 6), flat(INK), { p: [x, s * 1.6 + 0.3, z], to: camp }); if (i % 3 === 0) M(box(0.6, 0.35, 0.03), flat(0xd63b2f), { p: [x + 0.3, s * 1.6 + 0.55, z], to: camp, cast: false }); }
  for (let i = 0; i < 26; i++) { const x = -55 + rnd() * 110, z = -24 - rnd() * 70; const f = new THREE.Group(); f.position.set(x, 0, z); camp.add(f); for (let k = 0; k < 3; k++) { const c = M(new THREE.ConeGeometry(0.4 - k * 0.1, 1.0, 8), flat(k ? 0xffb030 : 0xff6a20), { p: [0, 0.5, 0], to: f, cast: false }); flames.push(c); } glow(f, 0, 0.8, 0, 6, 0.9); fires.push(f); }
  // soldiers: instanced bodies and heads
  const n = 520, bodyG = new THREE.CapsuleGeometry(0.32, 0.9, 4, 10), headG = new THREE.SphereGeometry(0.4, 14, 10), helmG = new THREE.SphereGeometry(0.42, 14, 8, 0, Math.PI * 2, 0, Math.PI / 2);
  const ib = new THREE.InstancedMesh(bodyG, toon(0xffffff), n), ih = new THREE.InstancedMesh(headG, toon(0xfbfaf5), n), im = new THREE.InstancedMesh(helmG, toon(0x8a92a4), n); const d = new THREE.Object3D(), col = new THREE.Color();
  for (let i = 0; i < n; i++) { const x = -58 + rnd() * 116, z = -22 - rnd() * 72; d.position.set(x, 0.95, z); d.rotation.set(0, rnd() * 6.28, 0); d.scale.setScalar(1); d.updateMatrix(); ib.setMatrixAt(i, d.matrix); ib.setColorAt(i, col.set([0x6a2f3a, 0x3a3542, 0x7a4a2c][i % 3])); d.position.y = 2.05; d.updateMatrix(); ih.setMatrixAt(i, d.matrix); d.position.y = 2.12; d.updateMatrix(); im.setMatrixAt(i, d.matrix); }
  [ib, ih, im].forEach(m => { m.castShadow = true; camp.add(m); });
  for (let i = 0; i < 9; i++) { const x = -30 + i * 7.5, z = -24; M(cyl(0.06, 0.06, 5, 6), flat(INK), { p: [x, 2.5, z], to: camp }); M(box(1.6, 1.0, 0.04), flat(0x6a2f3a), { ol: 0.02, p: [x + 0.8, 4.5, z], to: camp, cast: false }); }
}
const sky = (() => { const t = ctex(16, 256, g => { const r = g.createLinearGradient(0, 0, 0, 256); r.addColorStop(0, '#1a1a4a'); r.addColorStop(0.55, '#6a3a7a'); r.addColorStop(1, '#ff9a5a'); g.fillStyle = r; g.fillRect(0, 0, 16, 256); }); const m = M(new THREE.SphereGeometry(230, 32, 16), new THREE.MeshBasicMaterial({ map: t, side: THREE.BackSide }), { cast: false }); root.add(m); return m; })();
const stars = new THREE.Group(); root.add(stars); for (let i = 0; i < 120; i++) { const a = rnd() * 6.283, e = 0.35 + rnd() * 0.9; M(sph(0.25 + rnd() * 0.2, 4, 3), flat(0xffffff), { p: [Math.cos(a) * 200 * Math.cos(e), 200 * Math.sin(e), Math.sin(a) * 200 * Math.cos(e)], to: stars, cast: false }); }
M(sph(6, 24, 16), flat(0xfff4c2), { p: [-60, 70, -170], to: stars, cast: false }); glow(stars, -60, 70, -168, 40, 0.35);

// ---------- CELLAR (placed away from the castle) ----------
const cellar = new THREE.Group(); root.add(cellar); cellar.position.set(200, 0, 0); const bowls = [];
{ const brick = toon(0xffffff, { map: T2s.brickW }), stoneC = toon(0xffffff, { map: T2s.stone });
  M(box(8, 0.2, 18), toon(0xffffff, { map: T2s.cobble }), { p: [0, -0.1, 7], recv: true, to: cellar, cast: false });
  for (const s of [-1, 1]) M(box(0.4, 3.2, 18), stoneC, { p: [s * 3.2, 1.6, 7], recv: true, to: cellar, cast: false });
  M(box(8, 6, 0.4), stoneC, { p: [0, 3, -1.8], recv: true, to: cellar, cast: false });
  M(box(8, 0.3, 18), toon(0xffffff, { map: T2s.brickW }), { p: [0, 3.55, 7], to: cellar, cast: false });
  for (let i = 0; i < 6; i++) { const z = i * 3 + 0.5; for (const sx of [-1, 1]) M(box(0.35, 3.4, 0.35), stoneC, { ol: 0.03, p: [sx * 2.85, 1.7, z], to: cellar }); M(box(6.0, 0.35, 0.35), stoneC, { ol: 0.03, p: [0, 3.25, z], to: cellar }); }
  // the row of bowls along the outer wall (the wall faces the enemy)
  for (let i = 0; i < 16; i++) { const b = makeBowl(); b.position.set(-2.6, 0.02, 0.4 + i * 1.0); cellar.add(b); bowls.push(b); }
  // candles in niches, barrels, sacks, shelf with jars, a stool for the watcher
  for (let i = 0; i < 6; i++) { M(box(0.6, 0.6, 0.3), flat(0x1a1420), { p: [-3.0, 1.8, 1 + i * 3], to: cellar, cast: false }); candle(cellar, -2.95, 1.5, 1 + i * 3, 0.3); }
  for (let i = 0; i < 6; i++) candle(cellar, 2.8, 1.5, 2 + i * 3, 0.25);
  for (let i = 0; i < 6; i++) { const x = 2.4, z = 3 + i * 2.3; M(cyl(0.45, 0.4, 1.1, 14), toon(0x8a5a34), { ol: 0.03, p: [x, 0.55, z], to: cellar }); for (const y of [0.28, 0.82]) M(new THREE.TorusGeometry(0.46, 0.03, 6, 16), toon(0x2a2530), { p: [x, y, z], r: [Math.PI / 2, 0, 0], to: cellar, cast: false }); }
  for (const z of [1.2, 1.9]) { M(sph(0.45, 14, 10), toon(0xc9b08a), { ol: 0.03, p: [2.2, 0.4, z], s: [1, 1.2, 1], to: cellar }); }
  M(box(0.5, 0.45, 0.5), toon(0x6b4326), { ol: 0.025, p: [-1.4, 0.23, 3.6], to: cellar });
  const cl = new THREE.PointLight(0xffa850, 10, 12, 1.5); cl.position.set(0, 2.6, 4); cellar.add(cl); const cl2 = new THREE.PointLight(0xffa850, 8, 12, 1.5); cl2.position.set(0, 2.6, 12); cellar.add(cl2);
  cellar.userData.dust = []; for (let i = 0; i < 50; i++) { const d = M(sph(0.015, 5, 4), flat(0xfff2c8), { cast: false }); cellar.add(d); cellar.userData.dust.push(d); }
}
const SETS = [castle, cellar, sky, stars, sword, jug, pour, ladle, ...CAST.map(c => c.g)];
function hideAll() { SETS.forEach(g => g.visible = false); sparks.forEach(s => s.visible = false); }
function hold(c, hand, obj, off = V(0, 0, 0), rot = [0, 0, 0]) { c.g.updateMatrixWorld(true); const p = V(...hand); c.up.localToWorld(p); obj.visible = true; obj.position.copy(p).add(off); obj.rotation.set(...rot); }
function nightLook(t) { castle.visible = true; sky.visible = true; stars.visible = true; bg(0x1a1a4a); light(0.42, 0.7, [-40, 60, -60], 0x9fb0ff, 0x2a2440); LOOK.grade = ['#ff9a4a', 0.12]; LOOK.bloom = 0.32; tick(t); }
function cellarLook(t) { cellar.visible = true; bg(0x120c10); light(0.25, 0.15, [3, 8, 6], 0xffc890, 0x2a1a14); cellar.userData.dust.forEach((d, i) => { d.position.set(-2.5 + ((i * 37) % 50) / 10 + 0.15 * Math.sin(t * 0.6 + i), 0.5 + ((i * 53) % 25) / 10 + 0.1 * Math.sin(t * 0.8 + i), ((i * 29) % 160) / 10); }); LOOK.grade = ['#ff9a4a', 0.2]; LOOK.bloom = 0.35; tick(t); }
function tick(t) { flames.forEach((f, i) => { f.scale.set(1, 0.8 + 0.35 * Math.abs(Math.sin(t * (9 + i % 5) + i)), 1); f.rotation.z = 0.12 * Math.sin(t * 7 + i); }); }
// ===== three town looks to choose from =====
const stoneL = (() => { const t = ctex(256, 256, (g, w, h) => { g.fillStyle = '#9a9488'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 32) for (let x = (y / 32 % 2) * 32 - 64; x < w; x += 64) { g.fillStyle = `hsl(${30 + rnd() * 20},${6 + rnd() * 10}%,${78 + rnd() * 14}%)`; g.fillRect(x + 3, y + 3, 58, 26); } }); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(4, 2); return t; })();
stoneM.map = stoneL; stoneM.needsUpdate = true;
const town = new THREE.Group(); castle.add(town);
const roofMats = [], wallMats = [];
// a fuller town inside the walls: two rows of houses along the sides, a church, market stalls, bunting
function townHouse(x, z, ry, seed, col, w = 4, ht = 4.6) { const h = new THREE.Group(); h.position.set(x, 0, z); h.rotation.y = ry; town.add(h); const m = toon(0xffffff, { map: houseTex(seed, col) }); wallMats.push(m); const rm = toon(0x8a3b2c); roofMats.push(rm); M(box(w, ht, 3.6), [m, m, rm, rm, m, m], { ol: 0.05, p: [0, ht / 2, 0], to: h }); const tri = new THREE.Shape(); tri.moveTo(-w / 2 - 0.35, 0); tri.lineTo(w / 2 + 0.35, 0); tri.lineTo(0, 2.2); tri.closePath(); M(new THREE.ExtrudeGeometry(tri, { depth: 4.0, bevelEnabled: false }), rm, { ol: 0.05, p: [0, ht, -2.0], to: h }); M(box(0.5, 1.4, 0.5), toon(0x6b4636), { ol: 0.03, p: [w * 0.25, ht + 1.5, -0.5], to: h }); h.userData.snow = M(box(w + 0.9, 0.25, 4.3), toon(0xf4f6fb), { p: [0, ht + 1.15, 0], to: h, cast: false }); h.userData.snow.visible = false; return h; }
const tHouses = []; [[-15.5, 5, Math.PI / 2, 61, '#efe2c4'], [-15.5, 10, Math.PI / 2, 63, '#e3c9a0'], [-15.5, 15, Math.PI / 2, 65, '#f1dfb4'], [15.5, 13.5, -Math.PI / 2, 67, '#e2c594'], [15.5, 18, -Math.PI / 2, 69, '#ead9b4']].forEach(a => tHouses.push(townHouse(...a)));
const church = new THREE.Group(); church.position.set(-8, 0, 16); town.add(church); { const m = toon(0xffffff, { map: T2s.stone }); wallMats.push(m); M(box(4, 5, 5), m, { ol: 0.05, p: [0, 2.5, 0], to: church }); M(box(2, 9, 2), m, { ol: 0.05, p: [0, 4.5, -2.2], to: church }); const rm = toon(0x3b4a8a); roofMats.push(rm); M(new THREE.ConeGeometry(1.6, 3.6, 4), rm, { ol: 0.05, p: [0, 10.8, -2.2], r: [0, Math.PI / 4, 0], to: church }); M(box(1.0, 1.4, 0.1), flat(0xffd27a), { p: [0, 6.5, -1.15], to: church, cast: false }); }
const stalls = new THREE.Group(); town.add(stalls); [[9, 6, 0xd63b2f], [11.5, 7.5, 0x2f6b4f], [8.5, 15, 0xd9a23a]].forEach(([x, z, c]) => { const s = new THREE.Group(); s.position.set(x, 0, z); s.rotation.y = -0.4; stalls.add(s); M(box(2.2, 0.9, 1.0), toon(0x7a5232), { ol: 0.03, p: [0, 0.45, 0], to: s }); for (const sx of [-1, 1]) M(cyl(0.05, 0.05, 2.4, 6), toon(0x6b4326), { p: [sx, 1.2, 0.45], to: s }); const aw = ctex(256, 64, g => { for (let i = 0; i < 8; i++) { g.fillStyle = i % 2 ? '#f3efe6' : '#' + c.toString(16).padStart(6, '0'); g.fillRect(i * 32, 0, 32, 64); } }); M(box(2.6, 0.08, 1.5), toon(0xffffff, { map: aw }), { ol: 0.03, p: [0, 2.4, 0.1], r: [0.2, 0, 0], to: s }); for (let i = 0; i < 6; i++) M(sph(0.14, 10, 8), toon([0xe2553d, 0xf2c230, 0x5fa14a][i % 3]), { ol: 0.015, p: [-0.8 + i * 0.32, 1.0, 0], to: s }); });
const bunting = new THREE.Group(); town.add(bunting); for (const [a, b] of [[[-15, 5.5, 5], [6, 5.5, 9]], [[-15, 5.5, 13], [15, 5.5, 15]]]) { const A = V(...a), B = V(...b); for (let i = 0; i < 18; i++) { const p = A.clone().lerp(B, i / 17); p.y -= Math.sin(i / 17 * Math.PI) * 1.0; M(new THREE.ConeGeometry(0.18, 0.4, 3), flat([0xd63b2f, 0xf2c230, 0x3b5bd9, 0x5fa14a][i % 4]), { p: [p.x, p.y - 0.2, p.z], r: [Math.PI, 0, 0], s: [1, 1, 0.2], to: bunting, cast: false }); } }
// theme-only extras
const snowSet = new THREE.Group(); castle.add(snowSet); { const sm = toon(0xf4f6fb); M(box(240, 0.05, 240), sm, { p: [0, 0.04, -60], to: snowSet, cast: false, recv: true }); for (const [x, z, w, d] of [[0, 0, 40, 2.5], [0, 22, 40, 2.5], [-20, 11, 2.5, 22], [20, 11, 2.5, 22]]) M(box(w + 0.3, 0.25, d + 0.3), sm, { p: [x, WALLH + 0.05, z], to: snowSet, cast: false }); for (const [x, z] of [[-20, 0], [20, 0], [-20, 22], [20, 22]]) M(new THREE.ConeGeometry(2.6, 2.2, 24), sm, { p: [x, 14.7, z], to: snowSet, cast: false }); for (let i = 0; i < 60; i++) { const x = -58 + (i * 37 % 116), z = -26 - (i * 53 % 70); M(new THREE.ConeGeometry(1.4, 0.7, 8), sm, { p: [x, 2.9, z], to: snowSet, cast: false }); } }
const desertSet = new THREE.Group(); castle.add(desertSet); { const sand = ctex(256, 256, (g, w, h) => { g.fillStyle = '#e2c27a'; g.fillRect(0, 0, w, h); for (let i = 0; i < 600; i++) { g.fillStyle = `rgba(${rnd() < 0.5 ? '190,150,80' : '250,225,160'},0.4)`; g.beginPath(); g.ellipse(rnd() * w, rnd() * h, 2 + rnd() * 6, 1 + rnd() * 3, 0, 0, 7); g.fill(); } }); sand.wrapS = sand.wrapT = THREE.RepeatWrapping; sand.repeat.set(40, 40); M(box(240, 0.05, 240), toon(0xffffff, { map: sand }), { p: [0, 0.04, -60], to: desertSet, cast: false, recv: true });
  function palm(x, z, s) { const g = new THREE.Group(); g.position.set(x, 0, z); g.scale.setScalar(s); desertSet.add(g); for (let i = 0; i < 6; i++) M(cyl(0.22 - i * 0.02, 0.25 - i * 0.02, 0.9, 10), toon(0x8a6a44), { ol: 0.03, p: [i * 0.08, 0.45 + i * 0.85, 0], r: [0, 0, -0.06], to: g }); for (let i = 0; i < 7; i++) { const a = i / 7 * 6.28; const leaf = M(box(0.5, 0.06, 2.6), toon(0x4f9a40), { ol: 0.03, p: [0.5 + Math.cos(a) * 1.1, 5.3, Math.sin(a) * 1.1], r: [0, -a + Math.PI / 2, 0], to: g }); leaf.rotateX(0.5); } }
  for (const [x, z, s] of [[-12, 8, 1], [12, 4, 0.9], [4, 16, 1.1], [-30, -10, 1.3], [30, -12, 1.2], [-44, -30, 1.4], [46, -40, 1.3], [-22, -60, 1.2]]) palm(x, z, s);
  for (const [x, z, r] of [[-8, 16, 2.0], [15.5, 13.5, 1.6]]) { M(new THREE.SphereGeometry(r, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), toon(0x2fa8a0), { ol: 0.05, p: [x, x === -8 ? 9 : 6.8, z - (x === -8 ? 2.2 : 0)], to: desertSet }); } }
const THEMES = {
  A: { name: 'Golden harvest town', sky: ['#2a3a8a', '#d0608a', '#ffb060'], bg: 0x8a5a7a, light: [0.6, 1.2, [-40, 25, -60], 0xffd0a0, 0x5a3a4a], grade: ['#ff9a4a', 0.2], stone: 0xd9c0a0, roof: 0xb3472d, tower: 0x8a3b2c, grass: true },
  B: { name: 'Snowy winter fortress', sky: ['#0a1030', '#2a3a7a', '#6a7ab0'], bg: 0x1a2250, light: [0.5, 0.8, [-40, 60, -60], 0xb0c4ff, 0x3a4060], grade: ['#7a9aff', 0.16], stone: 0xb8c0d4, roof: 0x5a3a5a, tower: 0x3b4a8a, snow: true },
  C: { name: 'Desert sandstone citadel', sky: ['#1a4a9a', '#5aa0e0', '#ffd8a0'], bg: 0x5aa0e0, light: [0.85, 1.8, [40, 50, -30], 0xfff0d0, 0xa08060], grade: ['#ffd27a', 0.18], stone: 0xe8c890, roof: 0xd9773a, tower: 0x2fa8a0, desert: true },
};
let THEME = null;
function applyTheme(k) { const th = THEMES[k]; THEME = th; const g = sky.material.map.userData.g; const r = g.createLinearGradient(0, 0, 0, 256); r.addColorStop(0, th.sky[0]); r.addColorStop(0.55, th.sky[1]); r.addColorStop(1, th.sky[2]); g.fillStyle = r; g.fillRect(0, 0, 16, 256); sky.material.map.needsUpdate = true;
  stoneM.color.set(th.stone); wallMats.forEach(m => { if (m.map === T2s.stone) m.color.set(th.stone); }); roofMats.forEach(m => m.color.set(th.roof)); castle.children.forEach(c => { if (c.geometry && c.geometry.type === 'ConeGeometry' && c.geometry.parameters.radius === 3.6) c.material.color.set(th.tower); });
  snowSet.visible = !!th.snow; desertSet.visible = !!th.desert; tHouses.forEach(h => h.userData.snow.visible = !!th.snow); stars.visible = !th.desert; bunting.visible = !th.snow; stalls.visible = !th.snow; }
function themeLook(t) { const th = THEME; castle.visible = true; sky.visible = true; bg(th.bg); light(...th.light); LOOK.grade = th.grade; LOOK.bloom = 0.3; tick(t); }
window.showcase = (k, view) => { applyTheme(k); hideAll(); themeLook(1.0); stars.visible = !THEMES[k].desert; LOOK.dof = null; overlay = () => { };
  if (view === 0) setCam([24, 32, 52], [0, 0, 4], 50, 1.0, 0, 0);
  else { show(otto, 5.2, 10.6, 0.7); otto.face('happy'); otto.pose({ pitch: 0.15, rh: [0.45, 1.85, 0.65], lh: [-0.45, 1.85, 0.65], hx: -0.05 }); hold(otto, [0.45, 1.85, 0.65], jug, V(-0.05, 0.05, 0.15), [0, 0, 0.9]); show(captain, 1.0, 8.6, 0.3); captain.face('sneaky'); captain.pose({ rh: [0.75, 2.5, 0.6], lh: [-0.5, 1.95, 0.05] }); setCam([7.5, 3.0, 17.5], [1.5, 3.2, 4], 58, 1.0, 0, 0.0); }
  root.updateMatrixWorld(true); renderer.render(root, cam); ctx.drawImage(glc, 0, 0); const v = ctx.createRadialGradient(W / 2, H / 2, H * 0.3, W / 2, H / 2, H * 0.72); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(20,8,20,0.42)'); ctx.fillStyle = v; ctx.fillRect(0, 0, W, H); return out.toDataURL('image/jpeg', 0.92); };
applyTheme('C');
// desert day (courtyard, camp) and desert night (the long watch, the digging)
function dayLook(t) { themeLook(t); }
function desertNight(t) { castle.visible = true; sky.visible = true; stars.visible = true; const g = sky.material.map.userData.g; const r = g.createLinearGradient(0, 0, 0, 256); r.addColorStop(0, '#0a1440'); r.addColorStop(0.55, '#1f3a7a'); r.addColorStop(1, '#5a6aa0'); g.fillStyle = r; g.fillRect(0, 0, 16, 256); sky.material.map.needsUpdate = true; bg(0x1f3a7a); light(0.45, 0.7, [-40, 60, -60], 0x9fb0ff, 0x3a3050); LOOK.grade = ['#ff9a4a', 0.12]; LOOK.bloom = 0.32; tick(t); }
// ===== second half: enemies, cross-section, coffee comparison, buckets =====
const enemyBody = (g, w, h) => { g.fillStyle = '#7a2f2a'; g.fillRect(0, 0, w, h); g.fillStyle = '#3a2416'; g.fillRect(0, h * 0.55, w, h * 0.08); g.fillStyle = '#d9a23a'; g.beginPath(); g.arc(w * 0.5, h * 0.3, 26, 0, 7); g.fill(); };
const enemies = [0, 1, 2].map(i => makeChar3({ stache: i === 1, freckles: i === 2, shoe: 0x2a2530, belt3d: 0x3a2416, body: enemyBody, hat: kettleHat(0x5a5f70, 0x4a4f60) }));
enemies.forEach(c => root.add(c.g));
const pick = () => { const g = new THREE.Group(); root.add(g); M(cyl(0.035, 0.035, 1.0, 8), toon(0x7a5232), { ol: 0.012, p: [0, -0.5, 0], to: g }); M(box(0.75, 0.08, 0.08), toon(0xb9bfca), { ol: 0.015, p: [0, 0.0, 0], to: g }); return g; };
const picks = [pick(), pick(), pick()];
const bucketGeo = new THREE.CylinderGeometry(0.22, 0.17, 0.36, 16, 1, true);
function makeBucket() { const g = new THREE.Group(); M(bucketGeo, toon(0x8a5a34, { side: THREE.DoubleSide }), { ol: 0.015, to: g }); M(cyl(0.17, 0.17, 0.02, 16), toon(0x6b4326), { p: [0, -0.17, 0], to: g }); M(new THREE.CircleGeometry(0.2, 16), waterM, { p: [0, 0.12, 0], r: [-Math.PI / 2, 0, 0], to: g, cast: false }); M(new THREE.TorusGeometry(0.22, 0.015, 6, 16, Math.PI), flat(INK), { p: [0, 0.18, 0], to: g, cast: false }); root.add(g); return g; }
const buckets = [0, 1, 2, 3].map(makeBucket);
const chain = [0, 1, 2].map(i => makeChar3({ stache: i === 1, shoe: 0x1b1522, belt3d: 0x3a2416, body: (g, w, h) => { g.fillStyle = '#9aa3b5'; g.fillRect(0, 0, w, h); g.fillStyle = ['#3b5bd9', '#2f6b4f', '#d63b2f'][i]; g.fillRect(w * 0.25, h * 0.05, w * 0.5, h * 0.75); }, hat: kettleHat(0x9aa3b5, 0x8a92a4) }));
chain.forEach(c => root.add(c.g));
// the hole Otto digs in the cellar floor
const hole = M(new THREE.CircleGeometry(0.9, 28), flat(0x0d0a0c), { r: [-Math.PI / 2, 0, 0], cast: false }); cellar.add(hole); hole.position.set(-1.2, 0.035, 7.5);
const holeRim = M(new THREE.TorusGeometry(0.95, 0.12, 6, 28), toon(0x8a6a44), { ol: 0.02, r: [Math.PI / 2, 0, 0], cast: false }); cellar.add(holeRim); holeRim.position.set(-1.2, 0.05, 7.5);
const stream = M(cyl(0.06, 0.1, 1, 10), flat(0x8fd0ff, { transparent: true, opacity: 0.85 }), { cast: false }); root.add(stream);

// ---------- CROSS-SECTION (side view of wall, ground, cellar and tunnel) ----------
const sect = new THREE.Group(); root.add(sect); sect.position.set(400, 0, 0); const SX = 400;
const earth = (() => { const t = ctex(512, 512, (g, w, h) => { g.fillStyle = '#8a5a34'; g.fillRect(0, 0, w, h); for (let i = 0; i < 220; i++) { g.fillStyle = `rgba(${rnd() < 0.5 ? '60,35,20' : '180,130,80'},${0.25 + rnd() * 0.3})`; g.beginPath(); g.ellipse(rnd() * w, rnd() * h, 4 + rnd() * 14, 3 + rnd() * 9, rnd() * 3, 0, 7); g.fill(); } for (let i = 0; i < 40; i++) { g.fillStyle = `rgba(150,140,130,0.9)`; g.strokeStyle = 'rgba(40,30,30,0.7)'; g.lineWidth = 2; g.beginPath(); g.ellipse(rnd() * w, rnd() * h, 6 + rnd() * 10, 5 + rnd() * 7, rnd() * 3, 0, 7); g.fill(); g.stroke(); } }); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(3, 1.5); return t; })();
const tunnelLen = [];
{ const sandTop = toon(0xe2c27a);
  M(box(30, 9, 4), toon(0xffffff, { map: earth }), { ol: 0.04, p: [0, -4.5, 0], to: sect }); M(box(30, 0.3, 4.05), sandTop, { p: [0, -0.15, 0], to: sect, cast: false });
  M(new THREE.PlaneGeometry(120, 60), flat(0x1f3a7a), { p: [0, 20, -12], to: sect, cast: false }); for (let i = 0; i < 60; i++) M(sph(0.06, 4, 3), flat(0xffffff), { p: [-30 + rnd() * 60, 4 + rnd() * 16, -11.5], to: sect, cast: false });
  M(sph(1.4, 20, 14), flat(0xfff4c2), { p: [-9, 13, -11.5], to: sect, cast: false });
  // castle wall above ground with battlements, and the inner cellar dug under the courtyard
  M(box(3, 8, 4), toon(0xe8c890, { map: stoneL }), { ol: 0.05, p: [3.5, 4, 0], to: sect }); for (let i = 0; i < 3; i++) M(box(0.7, 0.8, 4), toon(0xe8c890, { map: stoneL }), { ol: 0.03, p: [2.4 + i * 1.1, 8.4, 0], to: sect });
  M(box(8, 3.2, 0.2), flat(0x2a1a14), { p: [10, -1.6, 2.02], to: sect, cast: false }); M(box(8, 0.2, 0.25), toon(0xe8c890, { map: stoneL }), { p: [10, -3.1, 2.05], to: sect, cast: false });
  for (const x of [6.2, 13.8]) M(box(0.3, 3.2, 0.25), toon(0xe8c890, { map: stoneL }), { p: [x, -1.6, 2.05], to: sect, cast: false });
  candle(sect, 12.5, -3.0, 2.1, 0.3); candle(sect, 7.0, -3.0, 2.1, 0.3);
  sect.userData.bowl = makeBowl(); sect.userData.bowl.position.set(8.2, -3.0, 2.2); sect.userData.bowl.scale.setScalar(1.6); sect.add(sect.userData.bowl);
  // tents outside on the left
  for (const [x, c] of [[-12, 0xe9dcc0], [-9, 0xd63b2f], [-14.5, 0x3b5bd9]]) M(new THREE.ConeGeometry(1.5, 2.6, 8), toon(c), { ol: 0.05, p: [x, 1.3, -0.5], to: sect });
  const camp2 = new THREE.Group(); camp2.position.set(-6, 0, 0.5); sect.add(camp2); for (let k = 0; k < 3; k++) { const f = M(new THREE.ConeGeometry(0.35 - k * 0.08, 0.9, 8), flat(k ? 0xffb030 : 0xff6a20), { p: [0, 0.45, 0], to: camp2, cast: false }); flames.push(f); } glow(camp2, 0, 0.7, 0, 3, 0.9);
  // the tunnel: a dark slot with timber frames, growing toward the cellar
  sect.userData.tunnel = M(box(1, 1.8, 0.2), flat(0x140c0a), { p: [0, -5, 2.02], to: sect, cast: false });
  sect.userData.water = M(box(1, 1.8, 0.22), flat(0x3f9fe0, { transparent: true, opacity: 0.9 }), { p: [0, -5, 2.03], to: sect, cast: false });
  sect.userData.frames = []; for (let i = 0; i < 9; i++) { const f = new THREE.Group(); f.position.set(-12 + i * 2.2, -5, 2.1); sect.add(f); for (const s of [-1, 1]) M(box(0.18, 1.8, 0.1), toon(0x7a5232), { p: [s * 0.55, 0, 0], to: f }); M(box(1.3, 0.18, 0.1), toon(0x7a5232), { p: [0, 0.85, 0], to: f }); sect.userData.frames.push(f); }
  M(box(0.6, 3.3, 0.22), flat(0x140c0a), { p: [-13, -3.4, 2.02], to: sect, cast: false }); // entrance shaft in the camp
}
function tunnelTo(x1, flood = 0) { const x0 = -13, L = Math.max(0.1, x1 - x0); const tu = sect.userData.tunnel; tu.scale.x = L; tu.position.x = x0 + L / 2; sect.userData.frames.forEach(f => f.visible = f.position.x < x1 - 0.5); const w = sect.userData.water; w.visible = flood > 0; w.scale.set(L, Math.max(0.01, flood), 1); w.position.set(x0 + L / 2, -5 - 0.9 + 0.9 * flood, 2.03); }

// ---------- COFFEE comparison (flat colour backdrop like Comicron's explainer cards) ----------
const coffee = new THREE.Group(); root.add(coffee); coffee.position.set(600, 0, 0);
{ M(new THREE.PlaneGeometry(40, 40), flat(0xd9773a), { p: [0, 5, -6], to: coffee, cast: false }); M(box(14, 0.4, 6), toon(0xffffff, { map: T2s.wood }), { ol: 0.04, p: [0, 0.8, 0], to: coffee });
  const mug = new THREE.Group(); mug.position.set(0, 1.0, 0.5); coffee.add(mug); M(cyl(0.7, 0.62, 1.4, 28, true), toon(0xf3efe6, { side: THREE.DoubleSide }), { ol: 0.04, p: [0, 0.7, 0], to: mug }); M(cyl(0.62, 0.62, 0.05, 28), toon(0xf3efe6), { p: [0, 0.02, 0], to: mug }); M(new THREE.TorusGeometry(0.35, 0.09, 8, 16, Math.PI), toon(0xf3efe6), { ol: 0.03, p: [0.75, 0.75, 0], r: [0, 0, -Math.PI / 2], to: mug });
  coffee.userData.cup = new THREE.Group(); coffee.userData.cup.position.set(0, 1.25, 0); mug.add(coffee.userData.cup); M(new THREE.CircleGeometry(0.66, 28), flat(0x6a3a1c), { r: [-Math.PI / 2, 0, 0], to: coffee.userData.cup, cast: false }); coffee.userData.rings = [0, 1, 2].map(() => { const r = M(new THREE.TorusGeometry(1, 0.03, 4, 32), flat(0xc9a07a, { transparent: true }), { r: [Math.PI / 2, 0, 0], to: coffee.userData.cup, cast: false }); return r; });
  const truck = new THREE.Group(); coffee.add(truck); coffee.userData.truck = truck; M(box(2.4, 1.0, 1.0), toon(0xd63b2f), { ol: 0.04, p: [0, 0.9, 0], to: truck }); M(box(0.9, 0.8, 1.0), toon(0x3b5bd9), { ol: 0.04, p: [1.6, 0.8, 0], to: truck }); M(box(0.5, 0.4, 1.02), flat(0x9fd8ff), { p: [1.7, 0.95, 0], to: truck, cast: false }); for (const x of [-0.8, 0.6, 1.6]) for (const s of [-1, 1]) M(cyl(0.3, 0.3, 0.15, 16), toon(0x2a2530), { ol: 0.02, p: [x, 0.35, s * 0.5], r: [Math.PI / 2, 0, 0], to: truck });
}
const SETS2 = [sect, coffee, stream, ...enemies.map(c => c.g), ...picks, ...buckets, ...chain.map(c => c.g)];
const hideAllP = hideAll; hideAll = function () { hideAllP(); SETS2.forEach(g => g.visible = false); hole.visible = holeRim.visible = false; bowls.forEach(b => ripple(b, 0, false)); };
function pickSwing(c, t, ph) { const a = Math.sin(t * 7 + ph); return { rh: [0.35, 2.0 + 0.5 * a, 0.6], lh: [-0.1, 1.9 + 0.5 * a, 0.6], pitch: 0.2 + 0.1 * a }; }
function shakeRings(t, from, to, t0) { if (t < t0) return; const [x0, y0] = proj(from), [x1, y1] = proj(to); ctx.save(); ctx.lineCap = 'round'; for (let i = 0; i < 4; i++) { const p = ((t - t0) * 0.8 + i / 4) % 1; const x = lerp(x0, x1, p), y = lerp(y0, y1, p), r = 40 + p * 60; for (const [lw, c] of [[16, `rgba(27,21,34,${1 - p})`], [8, `rgba(255,224,120,${1 - p})`]]) { ctx.strokeStyle = c; ctx.lineWidth = lw; ctx.beginPath(); ctx.arc(x, y, r, Math.PI * 1.15, Math.PI * 1.85); ctx.stroke(); } } ctx.restore(); }
function drips(c, t) { const [hx, hy] = proj(c.headG.getWorldPosition(V(0, 0, 0))); ctx.save(); ctx.fillStyle = '#8fd8ff'; ctx.strokeStyle = INK; ctx.lineWidth = 5; for (let i = 0; i < 5; i++) { const p = ((t * 1.3 + i * 0.21) % 1), x = hx - 90 + i * 45, y = hy - 40 + p * 260; ctx.globalAlpha = 1 - p; ctx.beginPath(); ctx.ellipse(x, y, 10, 16, 0, 0, 7); ctx.fill(); ctx.stroke(); } ctx.restore(); }

castle.userData.heroBowl = makeBowl(); root.add(castle.userData.heroBowl); SETS2.push(castle.userData.heroBowl);
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
const CX = 200;
function update(t) {
  hideAll(); overlay = () => { };
  let li = 0; for (let i = 0; i < Ls.length; i++) if (t >= CUT(i)) li = i;
  const s0 = CUT(li), s1 = li + 1 < Ls.length ? CUT(li + 1) : DUR, k = (t - s0) / (s1 - s0);
  const sub = (a, b) => cl((t - a) / (b - a));
  LOOK.grade = ['#ffc98a', 0.1]; LOOK.bloom = 0.14; LOOK.dof = null;

  if (li === 0) { // HOOK: bowls along the cellar wall, then the army outside
    const tw = wf(0, 'while') - 0.1;
    if (t < tw) { cellarLook(t); const u = sub(0, tw);
      show(otto, CX - 1.6, 3.4, 0.35); otto.face('think'); otto.pose({ pitch: 0.12, hx: 0.12, hy: -0.4, lh: [-0.75, 1.85, 0.35], rh: [0.45, 1.6, 0.4] });
      hold(otto, [-0.75, 1.85, 0.35], jug, V(0, -0.05, 0), [0, 0, 1.3]); const b = bowls[3]; pour.visible = true; const sp = jug.position.clone().add(V(-0.2, -0.05, 0)), bp = cellar.localToWorld(b.position.clone()).add(V(0, 0.14, 0)); pour.position.copy(sp.clone().lerp(bp, 0.5)); pour.scale.set(1, sp.distanceTo(bp), 1); pour.quaternion.setFromUnitVectors(UP, sp.clone().sub(bp).normalize());
      setCam([CX + 0.6, lerp(1.3, 1.7, u), lerp(11.5, 9.0, u)], [CX - 2.0, lerp(0.7, 1.4, u), lerp(2.5, 3.4, u)], 50, t, 0, -0.04); LOOK.dof = [700, 1600, 3];
    } else { dayLook(t); const u = sub(tw, s1);
      setCam([lerp(-6, -2, u), lerp(12.5, 14, u), lerp(6, 3.5, u)], [-4, lerp(4, 2, u), -40], 58, t, 0, 0.0);
      overlay = () => popText('10,000 MEN', W / 2, 260, 140, '#ffd23e', t, wf(0, '10') - 0.05, s1 - 0.02);
    }
  }
  else if (li === 1) { // knights sharpen swords; he fills bowls
    dayLook(t); const tb = wf(1, 'he') - 0.1;
    if (t < tb) { const kn = knights[0]; show(kn, -5.9, 8.6, 1.4); kn.face('angry'); kn.pose({ rh: [0.55, 2.05, 0.75], lh: [-0.2, 2.05, 0.75], pitch: 0.15 });
      castle.userData.wheel.rotation.y = t * 12; const tip = V(-5.2, 1.6, 8.15); sword.visible = true; sword.position.copy(tip).add(V(-0.55, 0.0, 0.1)); sword.rotation.set(0, 0, -1.25);
      sparks.forEach((s, i) => { s.visible = true; const p = ((t * 2.2 + i / sparks.length) % 1); s.position.set(-4.75 + p * 1.4 + 0.2 * Math.sin(i), 1.62 + p * 0.8 - p * p * 1.6, 8.0 + (i % 5 - 2) * 0.08 * p * 4); s.material.opacity = 1 - p; s.scale.setScalar(0.1 * (1 - p * 0.5)); });
      show(knights[1], -8, 10.5, 0.8); knights[1].face('neutral'); knights[1].pose({ rh: [0.6, 2.4, 0.4], lh: [-0.5, 1.95, 0.05] });
      setCam([-2.4, 2.9, 12.6], [-5.6, 2.2, 8.4], 50, t, 0, 0.05);
    } else { show(otto, 5.2, 10.6, 0.7); otto.face('happy'); otto.pose({ pitch: 0.15, rh: [0.45, 1.85, 0.65], lh: [-0.45, 1.85, 0.65], hx: -0.05 });
      hold(otto, [0.45, 1.85, 0.65], jug, V(-0.05, 0.05, 0.15), [0, 0, 0.9]); const b = castle.userData.cart;
      const hp = otto.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 3.0, hp.y - 1.0, hp.z + 4.6], [hp.x - 0.5, hp.y - 0.6, hp.z - 0.5], 48, t, 0, -0.05);
    }
  }
  else if (li === 2) { // the captain's joke
    dayLook(t); show(captain, 1.0, 9.0, -0.3); captain.face(t > wf(2, 'giving') - 0.1 ? 'happy' : 'sneaky'); const lf = t > wf(2, 'bath') ? Math.abs(Math.sin(t * 8)) : 0;
    captain.pose({ rh: [0.75, 2.5, 0.6], lh: [-0.5, 1.95, 0.05], pitch: 0.12 * lf, hx: -0.2 * lf, bob: 0.03 * lf });
    show(otto, 5.2, 10.6, 0.7); otto.face('neutral'); otto.pose({ pitch: 0.15, rh: [0.45, 1.85, 0.65], lh: [-0.45, 1.85, 0.65], hx: -0.05 }); hold(otto, [0.45, 1.85, 0.65], jug, V(-0.05, 0.05, 0.15), [0, 0, 0.9]);
    const hp = captain.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x - 0.6, hp.y - 0.1, hp.z + lerp(4.4, 3.6, k)], [hp.x + 0.4, hp.y - 0.5, hp.z], 44, t, 0, 0.05); LOOK.dof = [380, 1400, 5];
    overlay = () => { if (t > wf(2, 'bath') - 0.1) burst('A BATH?!', 760, 520, 160, t, wf(2, 'bath') - 0.1, s1 - 0.02, 0.1); };
  }
  else if (li === 3) { // the cook wants his soup bowls back
    dayLook(t); show(cook, 2.0, 12.6, 0.6); cook.face('sad'); cook.pose({ rh: [0.8, 2.2, 0.6], lh: [-0.5, 1.95, 0.2], hz: 0.1 * Math.sin(t * 3), lean: -0.05 }); hold(cook, [-0.5, 1.95, 0.2], ladle, V(0, -0.1, 0.05), [0, 0, 0.3]);
    show(otto, 5.2, 10.6, 0.7); otto.face('neutral'); otto.pose({ pitch: 0.15, rh: [0.45, 1.85, 0.65], lh: [-0.45, 1.85, 0.65], hx: -0.05 }); hold(otto, [0.45, 1.85, 0.65], jug, V(-0.05, 0.05, 0.15), [0, 0, 0.9]);
    setCam([lerp(0.2, 0.6, k), 2.9, lerp(17.5, 16.6, k)], [3.6, 2.0, 11], 50, t, 0, -0.03);
  }
  else if (li === 4) { // lines the bowls, then sits in the dark and stares. All night.
    cellarLook(t); const ts = wf(4, 'then') - 0.1;
    if (t < ts) { const u = sub(s0, ts), z = lerp(6, 12, u); show(otto, CX - 1.6, z, 0.1); otto.face('happy'); otto.pose({ ...otto.walk(t * 6, 0.18), pitch: 0.35, lh: [-0.55, 1.5, 0.5], rh: [0.3, 1.9, 0.5], hx: 0.2 }); const b = bowls[Math.min(15, Math.floor(z))]; setCam([CX + 0.4, 1.9, z + 4.2], [CX - 1.7, 1.3, z - 0.5], 52, t, 0, 0.04);
    } else { show(otto, CX - 1.3, 2.4, 0.1); otto.g.position.y = 0.0; otto.face('neutral'); otto.pose({ bob: -0.95, lf: [-0.2, 0, 0.7], rf: [0.2, 0, 0.7], lh: [-0.4, 1.35, 0.55], rh: [0.4, 1.35, 0.55], hx: 0.25 });
      const u = sub(ts, s1); setCam([CX + lerp(0.6, 0.2, u), 1.6, lerp(8.0, 6.8, u)], [CX - 1.5, 1.0, 2.6], 50, t, 0, -0.04); LOOK.dof = [600, 1500, 3];
      overlay = () => popText('ALL NIGHT', W / 2, 260, 140, '#ffd23e', t, wf(4, 'all') - 0.05, s1 - 0.02); }
  }
  else if (li === 5 || li === 6) { // first night, nothing; second night, nothing
    cellarLook(t); const b = bowls[5]; const bp = cellar.localToWorld(b.position.clone());
    if (li === 5) setCam([bp.x + 0.8, bp.y + 0.7, bp.z + 1.1], [bp.x, bp.y + 0.1, bp.z], 44, t, 0, 0.05);
    else { show(otto, CX - 1.3, 2.4, 0.1); otto.face('sleep'); otto.pose({ bob: -0.95, lf: [-0.2, 0, 0.7], rf: [0.2, 0, 0.7], lh: [-0.4, 1.35, 0.55], rh: [0.4, 1.35, 0.55], hx: 0.4 + 0.1 * Math.sin(t * 2), hz: 0.15 }); const hp = otto.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 1.0, hp.y + 0.1, hp.z + 3.4], [hp.x, hp.y - 0.4, hp.z], 44, t, 0, 0.05); }
    overlay = () => { popText(li === 5 ? 'NIGHT 1' : 'NIGHT 2', W / 2, 260, 150, '#fff', t, s0 + 0.05, s1 - 0.02); popText('NOTHING', W / 2, 400, 130, '#8fa0ff', t, wf(li, 'nothing') - 0.05, s1 - 0.02); };
  }
  else if (li === 7) { // the castle calls him the Puddle General
    desertNight(t); [captain, knights[0], knights[1], cook].forEach((c, i) => { show(c, -2.4 + i * 1.5, 8.5 + (i % 2) * 0.6, 0.2); const lf = Math.abs(Math.sin(t * 7 + i)); c.face('happy'); c.pose({ pitch: 0.25 * lf, hx: -0.3 + 0.2 * lf, bob: 0.05 * lf, lh: [-0.5, 1.95 + 0.4 * lf, 0.2], rh: i === 0 ? [0.8, 2.6, 0.6] : [0.5, 1.95 + 0.4 * lf, 0.2] }); });
    setCam([lerp(0.0, 0.4, k), 3.0, lerp(15.5, 14.5, k)], [-0.2, 2.4, 8.6], 54, t, 0, -0.04);
    overlay = () => { burst('HA HA HA!', 320, 450, 170, t, s0 + 0.2, wf(7, 'puddle') - 0.1, -0.1); popText('THE PUDDLE', W / 2, 250, 140, '#fff', t, wf(7, 'puddle') - 0.05, s1 - 0.02); popText('GENERAL', W / 2, 400, 150, '#5fd0ff', t, wf(7, 'general') - 0.05, s1 - 0.02); };
  }
  else if (li === 8 || li === 9) { // outside: no attack. No ladders. No arrows. Just quiet.
    desertNight(t);
    if (li === 8) { const u = sub(s0, s1); setCam([lerp(-8, -3, u), lerp(12.5, 11.5, u), lerp(5, 2, u)], [-4, 2, -40], 58, t, 0, 0.0); }
    else { show(captain, -3, 0.2, Math.PI); captain.g.position.y = WALLH; captain.g.updateMatrixWorld(true); captain.face('think'); captain.pose({ rh: [0.4, 3.0, 0.5], lh: [-0.5, 1.95, 0.05], hy: 0.4 * Math.sin(t * 1.5) });
      const hp = captain.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 2.6, hp.y + 0.3, hp.z - 2.4], [hp.x - 0.2, hp.y - 0.4, hp.z], 50, t, 0, 0.04);
      overlay = () => { popText('NO LADDERS', W / 2, 250, 120, '#fff', t, s0 + 0.05, wf(9, 'no', 2) - 0.03); popText('NO ARROWS', W / 2, 250, 120, '#fff', t, wf(9, 'no', 2) - 0.03, wf(9, 'just') - 0.03); popText('JUST QUIET', W / 2, 250, 130, '#8fa0ff', t, wf(9, 'just') - 0.03, s1 - 0.02); }; }
  }
  else if (li === 10) { // the fifth night he jumps up and screams for buckets
    cellarLook(t); const tj = wf(10, 'he') - 0.1, j = t > tj ? Math.exp(-(t - tj) * 3) * Math.abs(Math.sin((t - tj) * 9)) : 0;
    show(otto, CX - 1.3, 2.4, 0.1); otto.face(t > tj ? 'shock' : 'sleep'); otto.pose(t > tj ? { bob: 0.35 * j, lh: [-0.8, 2.9, 0.3], rh: [0.8, 2.9, 0.3], hx: -0.2 } : { bob: -0.95, lf: [-0.2, 0, 0.7], rf: [0.2, 0, 0.7], lh: [-0.4, 1.35, 0.55], rh: [0.4, 1.35, 0.55], hx: 0.4 });
    setCam([CX - 0.3, 2.3, 6.8], [CX - 1.3, 1.9, 2.4], 50, t, t > tj ? 0.01 : 0, 0.05);
    overlay = () => { popText('NIGHT 5', W / 2, 260, 150, '#fff', t, s0 + 0.05, tj - 0.02); burst('BUCKETS!', 540, 380, 230, t, wf(10, 'buckets') - 0.1, s1 - 0.02, -0.06); };
  }
  else if (li === 11 || li === 12 || li === 15) { // the shivering bowl
    cellarLook(t); const b = bowls[11]; ripple(b, t, true, li === 12 ? 1.4 : 1); b.position.y = 0.02 + 0.004 * Math.sin(t * 60); const bp = cellar.localToWorld(b.position.clone());
    if (li === 11) setCam([bp.x + 1.6, bp.y + 1.2, bp.z + 2.4], [bp.x, bp.y + 0.1, bp.z], 46, t, 0, -0.05);
    else if (li === 12) setCam([bp.x + 0.15, bp.y + 1.2, bp.z + 0.5], [bp.x, bp.y, bp.z], 40, t, 0, 0.0);
    else { show(otto, CX - 1.6, bp.z - 1.2, 0.2); otto.face('sneaky'); otto.pose({ pitch: 0.3, hx: 0.25, bob: -0.35, rh: [0.15, 2.55, 0.5], lh: [-0.5, 1.6, 0.4] }); const hp = otto.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 0.6, hp.y - 0.4, hp.z + 4.4], [hp.x - 0.3, hp.y - 1.0, hp.z + 0.6], 48, t, 0, 0.05); }
    overlay = () => { if (li === 11) popText('EAST CELLAR', W / 2, 260, 120, '#ffd23e', t, wf(11, 'east') - 0.05, s1 - 0.02); if (li === 12) popText('NOBODY TOUCHING IT', W / 2, 1150, 92, '#fff', t, wf(12, 'nobody') - 0.05, s1 - 0.02); };
  }
  else if (li === 13 || li === 14) { // You see: the cross-section, diggers, the shake
    sect.visible = true; bg(0x1f3a7a); light(0.8, 1.0, [5, 10, 20], 0xd0d8ff, 0x5a4a50); LOOK.grade = ['#ff9a4a', 0.12]; LOOK.bloom = 0.3; tick(t);
    const tunEnd = li === 13 ? lerp(-6, 4.5, ss(0, 1, sub(s0, s1))) : 5.5; tunnelTo(tunEnd);
    enemies.forEach((c, i) => { show(c, 0, 0, 0); c.g.position.set(SX + tunEnd - 0.6 - i * 1.4, -5.9, 2.25); c.g.rotation.y = Math.PI / 2; c.g.scale.setScalar(0.42); c.face('angry'); c.pose(pickSwing(c, t, i * 2)); hold(c, pickSwing(c, t, i * 2).rh, picks[i], V(0, 0.15, 0), [0, Math.PI / 2, 1.2 + 0.7 * Math.sin(t * 7 + i * 2)]); picks[i].scale.setScalar(0.5); });
    const bowl = sect.userData.bowl; ripple(bowl, t, li === 14, 1.2);
    if (li === 13) { const u = sub(s0, s1); setCam([SX + lerp(-2, 2, u), lerp(4, -1, u), lerp(26, 20, u)], [SX + lerp(0, 2, u), lerp(1, -3, u), 0], 50, t, 0, 0.0);
      overlay = () => { popText('NOT CLIMBING', W / 2, 250, 120, '#fff', t, s0 + 0.1, wf(13, 'they') - 0.05); popText('DIGGING UNDER', W / 2, 250, 116, '#ffd23e', t, wf(13, 'they') - 0.05, s1 - 0.02); }; }
    else { setCam([SX + 5, -2.8, 15], [SX + 5.5, -3.6, 0], 50, t, 0, 0.0); const from = V(SX + tunEnd - 0.2, -4.6, 2.3), to = V(SX + 8.2, -2.8, 2.3);
      overlay = () => { shakeRings(t, from, to, s0 + 0.3); popText('EVERY SWING', W / 2, 250, 120, '#fff', t, s0 + 0.05, s1 - 0.02); popText('= A TINY SHAKE', W / 2, 390, 110, '#ffd23e', t, wf(14, 'tiny') - 0.05, s1 - 0.02); }; }
  }
  else if (li === 16) { // like your coffee trembling when a truck drives past
    coffee.visible = true; bg(0xd9773a); light(1.1, 1.4, [3, 6, 8], 0xffffff, 0x8a5a3a); LOOK.grade = null; LOOK.bloom = 0.12;
    const u = sub(s0 + 0.2, s1 - 0.2), tx = lerp(-12, 12, u); coffee.userData.truck.position.set(tx, 1.0, -2.2); const near = Math.exp(-Math.pow(tx / 4, 2));
    coffee.userData.rings.forEach((r, i) => { const p = ((t * 2 + i / 3) % 1); const s = 0.05 + p * 0.55; r.scale.set(s, s, s); r.material.opacity = near * (1 - p); }); coffee.userData.cup.position.y = 1.25 + 0.01 * near * Math.sin(t * 50);
    setCam([600 + 0.3, 3.6, 6.2], [600, 1.8, 0], 46, t, 0, 0.0);
    overlay = () => popText('COFFEE + TRUCK', W / 2, 260, 112, '#fff', t, wf(16, 'coffee') - 0.05, s1 - 0.02);
  }
  else if (li === 17) { // dig down to meet it; the whole castle pours in their buckets
    cellarLook(t); hole.visible = holeRim.visible = true; const tp = wf(17, 'and') - 0.1;
    if (t < tp) { show(otto, CX - 1.2, 8.7, Math.PI); otto.face('angry'); const a = Math.sin(t * 9); otto.pose({ pitch: 0.45, bob: -0.2, rh: [0.3, 1.4 + 0.5 * a, 0.6], lh: [-0.1, 1.3 + 0.5 * a, 0.6] }); hold(otto, [0.3, 1.4 + 0.5 * a, 0.6], picks[0], V(0, 0.15, 0), [0, 0, 1.2 + 0.7 * a]); picks[0].scale.setScalar(1);
      setCam([CX + 1.6, 2.4, 3.6], [CX - 1.2, 1.0, 8.0], 50, t, 0.006, 0.04); }
    else { chain.forEach((c, i) => { show(c, CX + 0.2 + i * 0.9, 7.5 + i * 1.6, -1.2); c.face('happy'); c.pose({ rh: [0.5, 1.9, 0.6], lh: [-0.5, 1.9, 0.6] }); });
      show(otto, CX - 1.3, 9.0, Math.PI); otto.face('happy'); otto.pose({ pitch: 0.35, rh: [0.4, 1.9, 0.7], lh: [-0.4, 1.9, 0.7] });
      buckets.forEach((bk, i) => { if (i < 3) { const ph = ((t * 1.2 + i * 0.33) % 1); const c = chain[i]; c.g.updateMatrixWorld(true); const p = V(0.5, 1.9, 0.6); c.up.localToWorld(p); bk.visible = true; bk.position.copy(p).add(V(-0.3 * ph, 0, -0.4 * ph)); bk.rotation.set(0, 0, 0); } });
      const hp = cellar.localToWorld(V(-1.2, 0, 7.5)); otto.g.updateMatrixWorld(true); const op = V(0.4, 1.9, 0.7); otto.up.localToWorld(op); const bk = buckets[3]; bk.visible = true; bk.position.copy(op); bk.rotation.set(0, 0, 1.9); stream.visible = true; const a = op.clone().add(V(-0.25, 0, 0)); stream.position.copy(a.clone().lerp(hp, 0.5)); stream.scale.set(1, a.distanceTo(hp), 1); stream.quaternion.setFromUnitVectors(UP, a.clone().sub(hp).normalize());
      setCam([CX + 0.4, 2.8, 3.2], [CX - 0.4, 1.3, 8.6], 54, t, 0, -0.04); }
    overlay = () => { if (t > tp) popText('EVERY BUCKET', W / 2, 260, 120, '#5fd0ff', t, tp + 0.05, s1 - 0.02); };
  }
  else if (li === 18) { // by sunrise the tunnel is a river; 10,000 soaked men
    const tm = wf(18, 'and') - 0.1;
    if (t < tm) { sect.visible = true; bg(0x1f3a7a); light(0.8, 1.0, [5, 10, 20], 0xd0d8ff, 0x5a4a50); LOOK.grade = ['#5fb4e6', 0.14]; LOOK.bloom = 0.3; tick(t); const f = ss(s0, tm - 0.3, t); tunnelTo(5.5, f);
      enemies.forEach((c, i) => { show(c, 0, 0, 0); c.g.position.set(SX + 4 - i * 1.6 - f * 7, -5.9 + f * 0.8 + 0.1 * Math.sin(t * 5 + i), 2.25); c.g.rotation.y = -Math.PI / 2; c.g.scale.setScalar(0.42); c.face('shock'); c.pose({ lh: [-0.7, 2.7, 0.2], rh: [0.7, 2.7, 0.2] }); });
      setCam([SX + 0, -2.5, 19], [SX + 0, -4.2, 0], 50, t, 0, 0.0);
      overlay = () => { burst('SPLASH!', 540, 1050, 200, t, s0 + 0.4, tm - 0.03, 0.06); popText('A RIVER', W / 2, 260, 150, '#5fd0ff', t, wf(18, 'river') - 0.1, tm - 0.02); };
    } else { dayLook(t); enemies.forEach((c, i) => { show(c, -1.5 + i * 1.5, -22 - (i % 2) * 0.8, 0.15 * (1 - i)); c.g.scale.setScalar(SC); c.face('sad'); c.pose({ lh: [-0.6, 1.4, 0.2], rh: [0.6, 1.4, 0.2], bob: -0.06, hx: 0.2 }); c.tint(0xd0e8ff); });
      setCam([0, 2.6, lerp(-15, -16, sub(tm, s1))], [0, 2.3, -22], 50, t, 0, 0.03); overlay = () => { enemies.forEach(c => drips(c, t)); popText('SOAKING WET', W / 2, 260, 130, '#5fd0ff', t, wf(18, 'soaking') - 0.05, s1 - 0.02); };
    }
  }
  else { // They lost the war to a bowl of water.
    dayLook(t); show(otto, -4, 1.2, 0.3); otto.g.position.y = WALLH; otto.g.updateMatrixWorld(true); otto.face('happy'); otto.pose({ rh: [0.35, 2.05, 0.75], lh: [-0.35, 2.05, 0.75], hx: 0.15 });
    const bw = castle.userData.heroBowl; bw.visible = true; otto.g.updateMatrixWorld(true); const p = V(0, 2.0, 0.8); otto.up.localToWorld(p); bw.position.copy(p); bw.scale.setScalar(1.3); ripple(bw, t, false);
    const u = sub(s0, s1); const hp = otto.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + lerp(1.6, 3.5, u), hp.y + lerp(-0.2, 2.5, u), hp.z + lerp(3.2, 8, u)], [hp.x + lerp(-0.2, -2, u), hp.y - lerp(0.6, 2.0, u), hp.z - lerp(0, 10, u)], 52, t, 0, -0.03);
    overlay = () => { popText('LOST THE WAR', W / 2, 250, 120, '#fff', t, wf(19, 'lost') - 0.05, DUR + 1); popText('TO A BOWL OF WATER', W / 2, 385, 82, '#5fd0ff', t, wf(19, 'bowl') - 0.05, DUR + 1); };
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
