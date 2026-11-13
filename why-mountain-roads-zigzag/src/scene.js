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
// ===== Why Mountain Roads Zigzag — cast and sets =====
const FT = []; function ftex(w, h, d) { const t = ctex(w, h, d); t.userData.draw = d; FT.push(t); return t; }
window.afterFonts = () => FT.forEach(t => { t.userData.draw(t.userData.g, t.userData.c.width, t.userData.c.height); t.needsUpdate = true; });
Object.assign(sun.shadow.camera, { left: -45, right: 45, top: 45, bottom: -45, near: 1, far: 200 }); sun.shadow.camera.updateProjectionMatrix(); sun.shadow.mapSize.set(4096, 4096); sun.shadow.bias = -0.0006;
const rnd = (seed => () => (seed = (seed * 16807) % 2147483647) / 2147483647)(91);
const glowTex = ctex(128, 128, g => { const r = g.createRadialGradient(64, 64, 0, 64, 64, 64); r.addColorStop(0, 'rgba(255,240,190,1)'); r.addColorStop(0.35, 'rgba(255,190,90,0.45)'); r.addColorStop(1, 'rgba(255,160,60,0)'); g.fillStyle = r; g.fillRect(0, 0, 128, 128); });
function glow(parent, x, y, z, s = 1.2, op = 0.9) { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: op })); sp.position.set(x, y, z); sp.scale.set(s, s, 1); parent.add(sp); return sp; }
const puffTex = ctex(128, 128, g => { const r = g.createRadialGradient(64, 64, 0, 64, 64, 64); r.addColorStop(0, 'rgba(255,255,255,0.8)'); r.addColorStop(0.6, 'rgba(255,255,255,0.3)'); r.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = r; g.fillRect(0, 0, 128, 128); });
function puffs(parent, n, col = 0xffffff) { const arr = []; for (let i = 0; i < n; i++) { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: puffTex, color: col, depthWrite: false, transparent: true, opacity: 0.6 })); parent.add(sp); arr.push(sp); } return arr; }

const T2s = {
  wood: rep_(ctex(512, 512, (g, w, h) => { g.fillStyle = '#8a5a34'; g.fillRect(0, 0, w, h); for (let i = 0; i < 8; i++) { g.fillStyle = `rgba(${rnd() < 0.5 ? '50,25,10' : '255,215,160'},${0.05 + rnd() * 0.09})`; g.fillRect(0, i * 64, w, 64); g.fillStyle = '#3d2414'; g.fillRect(0, i * 64, w, 4); g.strokeStyle = 'rgba(60,30,15,0.35)'; g.lineWidth = 2; for (let k = 0; k < 6; k++) { const y = i * 64 + 8 + rnd() * 48; g.beginPath(); g.moveTo(0, y); g.bezierCurveTo(w * 0.3, y + (rnd() - 0.5) * 16, w * 0.65, y + (rnd() - 0.5) * 16, w, y); g.stroke(); } g.fillStyle = '#3d2414'; g.beginPath(); g.ellipse(rnd() * w, i * 64 + 32, 7, 4, 0, 0, 7); g.fill(); } }), 3, 3),
  panel: rep_(ctex(512, 512, (g, w, h) => { g.fillStyle = '#6b3f22'; g.fillRect(0, 0, w, h); for (const [x, y] of [[20, 20], [266, 20], [20, 266], [266, 266]]) { g.fillStyle = '#7d4c2a'; g.fillRect(x, y, 226, 226); g.strokeStyle = '#3d2414'; g.lineWidth = 8; g.strokeRect(x, y, 226, 226); g.strokeStyle = 'rgba(255,220,170,0.18)'; g.lineWidth = 4; g.strokeRect(x + 14, y + 14, 198, 198); } }), 6, 2),
  tiles: rep_(ctex(256, 256, (g, w, h) => { for (let y = 0; y < 4; y++) for (let x = 0; x < 4; x++) { g.fillStyle = (x + y) % 2 ? '#e8dcc0' : '#5a3a2a'; g.fillRect(x * 64, y * 64, 64, 64); g.fillStyle = 'rgba(0,0,0,0.06)'; g.fillRect(x * 64, y * 64 + 58, 64, 6); } }), 10, 10),
  stone: rep_(ctex(256, 256, (g, w, h) => { g.fillStyle = '#6a6070'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 42) for (let x = (y / 42 % 2) * 40 - 80; x < w; x += 80) { g.fillStyle = `hsl(${250 + rnd() * 30},${6 + rnd() * 8}%,${44 + rnd() * 14}%)`; g.fillRect(x + 3, y + 3, 74, 36); } }), 3, 3),
  brickW: rep_(ctex(256, 256, (g, w, h) => { g.fillStyle = '#5a3a30'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 32) for (let x = (y / 32 % 2) * 32 - 64; x < w; x += 64) { g.fillStyle = `hsl(${10 + rnd() * 12},${36 + rnd() * 16}%,${32 + rnd() * 12}%)`; g.fillRect(x + 3, y + 3, 58, 26); } }), 4, 3),
  cobble: rep_(ctex(256, 256, (g, w, h) => { g.fillStyle = '#3d3a48'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 32) for (let x = (y / 32 % 2) * 20 - 40; x < w; x += 40) { g.fillStyle = `hsl(${240 + rnd() * 20},${8 + rnd() * 6}%,${36 + rnd() * 14}%)`; g.beginPath(); g.ellipse(x + 20, y + 16, 17, 13, 0, 0, 7); g.fill(); g.strokeStyle = 'rgba(0,0,0,0.3)'; g.lineWidth = 2; g.stroke(); } }), 10, 10),
  plaster: ctex(512, 512, (g, w, h) => { g.fillStyle = '#e9d6ad'; g.fillRect(0, 0, w, h); for (let i = 0; i < 160; i++) { g.fillStyle = `rgba(110,80,40,${0.03 + rnd() * 0.05})`; g.beginPath(); g.ellipse(rnd() * w, rnd() * h, 10 + rnd() * 40, 6 + rnd() * 20, rnd() * 3, 0, 7); g.fill(); } g.fillStyle = '#3d2718'; for (const x of [0, 248, 494]) g.fillRect(x, 0, 18, h); g.fillRect(0, 0, w, 18); g.fillRect(0, 250, w, 16); g.fillRect(0, 494, w, 18); }),
};


// ---------- terrain: a steep mountainside falling toward the village (down-slope = +z) ----------
const TOPZ = -62, BOTZ = 0, TOPH = 42;
function hBase(z) { const k = cl((z - TOPZ) / (BOTZ - TOPZ)); return TOPH * (1 - k) + (z < TOPZ ? (TOPZ - z) * 0.25 : 0); }
function hT(x, z) { return Math.max(0, hBase(z) + (z < BOTZ ? 1.6 * Math.sin(x * 0.18 + z * 0.07) * Math.sin(x * 0.05) * cl((BOTZ - z) / 8) : 0) + (Math.abs(x) > 34 ? (Math.abs(x) - 34) * 0.8 : 0)); }
const world = new THREE.Group(); root.add(world);
const T3 = {
  grass: (() => { const t = ctex(512, 512, (g, w, h) => { g.fillStyle = '#6fa548'; g.fillRect(0, 0, w, h); for (let i = 0; i < 2200; i++) { g.strokeStyle = `rgba(${rnd() < 0.5 ? '60,110,40' : '150,200,90'},${0.25 + rnd() * 0.35})`; g.lineWidth = 2; const x = rnd() * w, y = rnd() * h; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (rnd() - 0.5) * 6, y - 8 - rnd() * 10); g.stroke(); } for (let i = 0; i < 40; i++) { g.fillStyle = `rgba(120,110,100,${0.5 + rnd() * 0.3})`; g.beginPath(); g.ellipse(rnd() * w, rnd() * h, 6 + rnd() * 10, 4 + rnd() * 6, rnd() * 3, 0, 7); g.fill(); } }); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(14, 14); return t; })(),
  dirt: (() => { const t = ctex(256, 512, (g, w, h) => { g.fillStyle = '#a07a52'; g.fillRect(0, 0, w, h); for (let i = 0; i < 500; i++) { g.fillStyle = `rgba(${rnd() < 0.5 ? '70,50,30' : '200,170,130'},${0.15 + rnd() * 0.25})`; g.beginPath(); g.ellipse(rnd() * w, rnd() * h, 2 + rnd() * 6, 2 + rnd() * 4, 0, 0, 7); g.fill(); } g.strokeStyle = 'rgba(60,40,25,0.45)'; g.lineWidth = 10; for (const x of [0.3, 0.7]) { g.beginPath(); g.moveTo(w * x, 0); g.lineTo(w * x, h); g.stroke(); } g.fillStyle = 'rgba(90,140,60,0.8)'; for (let y = 0; y < h; y += 6) { g.fillRect(rnd() * 14, y, 6, 4); g.fillRect(w - rnd() * 14, y, 6, 4); } }); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t; })(),
  rock: (() => { const t = ctex(256, 256, (g, w, h) => { g.fillStyle = '#8a8a96'; g.fillRect(0, 0, w, h); for (let i = 0; i < 60; i++) { g.fillStyle = `rgba(${rnd() < 0.5 ? '60,60,70' : '190,190,200'},${0.2 + rnd() * 0.3})`; g.beginPath(); g.moveTo(rnd() * w, rnd() * h); for (let k = 0; k < 4; k++) g.lineTo(rnd() * w, rnd() * h); g.fill(); } }); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(3, 3); return t; })(),
};
const terrainM = toon(0xffffff, { map: T3.grass });
{
  const geo = new THREE.PlaneGeometry(110, 150, 160, 220); geo.rotateX(-Math.PI / 2); const p = geo.attributes.position;
  for (let i = 0; i < p.count; i++) { const x = p.getX(i), z = p.getZ(i) - 40; p.setZ(i, z); p.setY(i, hT(x, z)); }
  geo.computeVertexNormals(); const terr = M(geo, terrainM, { recv: true, cast: false, to: world }); world.userData.terr = terr;
  // snowy peaks behind
  for (const [x, z, h, r] of [[-30, -110, 60, 30], [10, -125, 75, 36], [45, -105, 55, 28], [-60, -95, 45, 26], [70, -120, 62, 30]]) { M(new THREE.ConeGeometry(r, h, 7), toon(0x7d7f94), { ol: 0.25, p: [x, h / 2 + TOPH - 6, z], to: world, cast: false }); M(new THREE.ConeGeometry(r * 0.42, h * 0.42, 7), toon(0xf4f6fb), { p: [x, h * 0.79 + TOPH - 6, z], to: world, cast: false }); }
  // rocks
  for (let i = 0; i < 26; i++) { const x = (rnd() - 0.5) * 70, z = TOPZ + rnd() * 55; if (Math.abs(x) < 3) continue; M(new THREE.DodecahedronGeometry(0.6 + rnd() * 1.4, 0), toon(0xffffff, { map: T3.rock }), { ol: 0.06, p: [x, hT(x, z) + 0.3, z], r: [rnd() * 3, rnd() * 3, 0], to: world }); }
}
// pines
const pineM = toon(0x2f6b3f), pineM2 = toon(0x3f8a4f), trunkM = toon(0x5a3a22);
function pine(parent, x, y, z, s) { const g = new THREE.Group(); g.position.set(x, y, z); g.scale.setScalar(s); parent.add(g); M(cyl(0.15, 0.2, 0.9, 8), trunkM, { ol: 0.03, p: [0, 0.45, 0], to: g }); for (let i = 0; i < 3; i++) M(new THREE.ConeGeometry(1.1 - i * 0.28, 1.4, 9), i % 2 ? pineM2 : pineM, { ol: 0.05, p: [0, 1.3 + i * 0.75, 0], to: g }); g.userData.snow = []; for (let i = 0; i < 3; i++) { const sn = M(new THREE.ConeGeometry(0.5 - i * 0.12, 0.35, 9), toon(0xf4f6fb), { p: [0, 1.85 + i * 0.75, 0], to: g, cast: false }); sn.visible = false; g.userData.snow.push(sn); } return g; }
const pines = [];
// ---------- roads ----------
function ribbon(pts, width, mat, lift = 0.06) { const curve = new THREE.CatmullRomCurve3(pts.map(p => V(p[0], hT(p[0], p[1]) + lift, p[1])), false, 'centripetal'); const n = Math.max(40, Math.floor(curve.getLength() * 2)); const pos = [], uv = [], idx = []; let acc = 0, prev = null;
  for (let i = 0; i <= n; i++) { const u = i / n, c = curve.getPointAt(u), tng = curve.getTangentAt(u); const side = V(-tng.z, 0, tng.x).normalize().multiplyScalar(width / 2); if (prev) acc += c.distanceTo(prev); prev = c; for (const sgn of [-1, 1]) { const q = c.clone().addScaledVector(side, sgn); q.y = hT(q.x, q.z) + lift; pos.push(q.x, q.y, q.z); uv.push(sgn < 0 ? 0 : 1, acc / 6); } if (i < n) { const a = i * 2; idx.push(a, a + 2, a + 1, a + 1, a + 2, a + 3); } }
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); geo.setIndex(idx); geo.computeVertexNormals(); const m = new THREE.Mesh(geo, mat); m.receiveShadow = true; m.userData.curve = curve; return m; }
const dirtM = toon(0xffffff, { map: T3.dirt, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: -2 });
const STRAIGHT = [[0, TOPZ + 1], [0, -40], [0, -20], [0, BOTZ + 1], [0, 5]];
const ZZ = (() => { const pts = [[-14, TOPZ + 1]]; const n = 8; for (let i = 0; i < n; i++) { const z = TOPZ + 1 + (i + 1) * (BOTZ - TOPZ - 1) / (n + 0.4); pts.push([i % 2 ? -14 : -30, z]); } pts.push([-20, 2], [-8, 9]); return pts; })();
const roadS = ribbon(STRAIGHT, 3.0, dirtM); world.add(roadS); const roadZ = ribbon(ZZ, 2.6, dirtM); world.add(roadZ);
// fence posts along the bends; little milestone signs
for (let i = 1; i < ZZ.length - 2; i++) { const [x, z] = ZZ[i]; for (let k = -2; k <= 2; k++) { const zz = z + k * 0.9, xx = x + (i % 2 ? 1.8 : -1.8); M(box(0.14, 0.7, 0.14), toon(0x7a5232), { ol: 0.02, p: [xx, hT(xx, zz) + 0.35, zz], to: world }); } }
// pines scattered away from roads
for (let i = 0; i < 160; i++) { const x = (rnd() - 0.5) * 90, z = TOPZ - 8 + rnd() * 66; if (Math.abs(x) < 3.5 || (Math.abs(x) < 10 && z < -48) || (Math.abs(x) < 9 && z > -8)) continue; const nearZ = ZZ.some(([a, b], j) => j < ZZ.length - 1 && distSeg(x, z, a, b, ZZ[j + 1][0], ZZ[j + 1][1]) < 2.8); if (nearZ) continue; pines.push(pine(world, x, hT(x, z), z, 0.8 + rnd() * 0.9)); }
function distSeg(px, pz, ax, az, bx, bz) { const dx = bx - ax, dz = bz - az, t = cl(((px - ax) * dx + (pz - az) * dz) / (dx * dx + dz * dz + 1e-9)); return Math.hypot(px - ax - dx * t, pz - az - dz * t); }
// road signs
const signS = ftex(512, 200, g => { g.fillStyle = '#e9d6ad'; g.fillRect(0, 0, 512, 200); g.strokeStyle = '#3d2718'; g.lineWidth = 12; g.strokeRect(6, 6, 500, 188); g.fillStyle = '#b3272d'; g.font = '62px Pop'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText("RUDOLF'S ROAD", 256, 72); g.fillStyle = '#1b1522'; g.font = '50px Pop'; g.fillText('1 HOUR ⬇', 256, 145); });
const signZ = ftex(512, 200, g => { g.fillStyle = '#e9d6ad'; g.fillRect(0, 0, 512, 200); g.strokeStyle = '#3d2718'; g.lineWidth = 12; g.strokeRect(6, 6, 500, 188); g.fillStyle = '#2f6b4f'; g.font = '62px Pop'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('OLD ROAD', 256, 72); g.fillStyle = '#1b1522'; g.font = '50px Pop'; g.fillText('40 BENDS · 3 HRS', 256, 145); });
function signpost(x, z, tex, ry) { const g = new THREE.Group(); g.position.set(x, hT(x, z), z); g.rotation.y = ry; world.add(g); M(cyl(0.08, 0.1, 2.4, 8), toon(0x6b4326), { ol: 0.025, p: [0, 1.2, 0], to: g }); M(box(1.9, 0.75, 0.08), toon(0xffffff, { map: tex }), { ol: 0.03, p: [0, 2.2, 0.06], to: g }); return g; }
signpost(4.6, TOPZ + 2.2, signS, -0.5); signpost(-11.5, TOPZ + 3, signZ, 0.3);

// ---------- top of the mountain: Rudolf's lookout ----------
const top = new THREE.Group(); world.add(top); top.position.set(0, hT(0, TOPZ), TOPZ);


// ---------- village at the bottom ----------
const village = new THREE.Group(); world.add(village);
const roofM = toon(0x9a4a3a);
function house(x, z, ry, seed, col, w = 4.4, ht = 4.6) { const h = new THREE.Group(); h.position.set(x, hT(x, z), z); h.rotation.y = ry; village.add(h); const m = toon(0xffffff, { map: houseTex(seed, col) }); M(box(w, ht, 4), [m, m, roofM, roofM, m, m], { ol: 0.05, p: [0, ht / 2, 0], to: h }); const tri = new THREE.Shape(); tri.moveTo(-w / 2 - 0.4, 0); tri.lineTo(w / 2 + 0.4, 0); tri.lineTo(0, 2.4); tri.closePath(); M(new THREE.ExtrudeGeometry(tri, { depth: 4.6, bevelEnabled: false }), roofM, { ol: 0.05, p: [0, ht, -2.3], to: h }); M(box(0.6, 1.6, 0.6), toon(0x6b4636), { ol: 0.03, p: [w * 0.25, ht + 1.7, -0.6], to: h }); h.userData.snow = M(box(w + 1.0, 0.25, 4.8), toon(0xf4f6fb), { p: [0, ht + 1.25, 0], to: h, cast: false }); h.userData.snow.visible = false; return h; }
const houses = []; [[-12, 12, 0.4, 3, '#efe2c4'], [-17, 8, 0.6, 5, '#e3c9a0'], [10, 13, -0.4, 7, '#f1dfb4'], [15, 8.5, -0.6, 9, '#e2c594'], [-6, 18, 0.1, 11, '#ead9b4'], [6, 19, -0.1, 13, '#e8cfa0'], [-22, 15, 0.8, 15, '#dcc59a'], [21, 16, -0.7, 17, '#efe2c4']].forEach(a => houses.push(house(...a)));
// church with a steeple
{ const c = new THREE.Group(); c.position.set(-2, 0, 26); village.add(c); M(box(5, 6, 7), toon(0xffffff, { map: T2s.stone }), { ol: 0.05, p: [0, 3, 0], to: c }); M(box(2.4, 9, 2.4), toon(0xffffff, { map: T2s.stone }), { ol: 0.05, p: [0, 4.5, 4], to: c }); M(new THREE.ConeGeometry(1.9, 4, 4), toon(0x5a3a3a), { ol: 0.05, p: [0, 11, 4], r: [0, Math.PI / 4, 0], to: c }); }
// Rudolf's warehouse at the very bottom of the straight road: doors open, barrels stacked
const ware = new THREE.Group(); village.add(ware); ware.position.set(0, 0, 9.5);
const wareDoors = [];
{ const wood = toon(0xffffff, { map: T2s.wood }); for (const x of [-3.9, 3.9]) M(box(0.2, 5.2, 6), wood, { ol: 0.05, p: [x, 2.6, 2.6], to: ware }); M(box(8, 5.2, 0.2), wood, { ol: 0.05, p: [0, 2.6, 5.6], to: ware }); for (const x of [-3.0, 3.0]) M(box(1.8, 5.2, 0.2), wood, { ol: 0.05, p: [x, 2.6, -0.4], to: ware }); M(box(8, 1.0, 0.2), wood, { ol: 0.05, p: [0, 4.7, -0.4], to: ware }); M(box(8.6, 0.3, 6.6), toon(0x5a3a22), { ol: 0.04, p: [0, 5.3, 2.6], to: ware });
  const tri = new THREE.Shape(); tri.moveTo(-4.6, 0); tri.lineTo(4.6, 0); tri.lineTo(0, 2.6); tri.closePath(); M(new THREE.ExtrudeGeometry(tri, { depth: 6.6, bevelEnabled: false }), roofM, { ol: 0.06, p: [0, 5.4, -0.7], to: ware });
  M(box(7.6, 4.8, 0.1), flat(0x2a1a12), { p: [0, 2.5, 5.5], to: ware, cast: false }); M(box(4.0, 0.1, 5.6), toon(0x5a3a22), { p: [0, 0.05, 2.6], to: ware, cast: false });
  for (const s of [-1, 1]) { const d = new THREE.Group(); d.position.set(s * 2, 0, -0.45); ware.add(d); M(box(2.0, 4.0, 0.16), toon(0x6b4326), { ol: 0.035, p: [-s * 1.0, 2.0, 0], to: d }); M(box(1.6, 0.14, 0.06), toon(0x3d2414), { p: [-s * 1.0, 1.0, -0.1], r: [0, 0, s * 0.6], to: d, cast: false }); d.rotation.y = s * 1.2; wareDoors.push(d); }
  const nb = ftex(1024, 160, g => { g.fillStyle = '#3d2414'; g.fillRect(0, 0, 1024, 160); g.strokeStyle = '#ffd34d'; g.lineWidth = 10; g.strokeRect(8, 8, 1008, 144); g.fillStyle = '#ffd34d'; g.font = '96px Pop'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('RUDOLF & CO.', 512, 86); }); M(box(5.6, 0.85, 0.1), toon(0xffffff, { map: nb }), { ol: 0.035, p: [0, 4.6, -0.5], to: ware });
  ware.userData.barrels = []; for (let r = 0; r < 3; r++) for (let i = 0; i < 5 - r; i++) for (let d = 0; d < 3; d++) { const b = new THREE.Group(); b.position.set(-1.6 + i * 0.8 + r * 0.4, 0.45 + r * 0.82, 0.8 + d * 1.0); ware.add(b); M(cyl(0.38, 0.34, 0.85, 14), toon(0x8a5a34), { ol: 0.03, to: b }); for (const y of [-0.25, 0.25]) M(new THREE.TorusGeometry(0.39, 0.025, 6, 16), toon(0x2a2530), { p: [0, y, 0], r: [Math.PI / 2, 0, 0], to: b, cast: false }); ware.userData.barrels.push(b); }
  const wl = new THREE.PointLight(0xffc070, 6, 8, 1.6); wl.position.set(0, 3.5, 1.2); ware.add(wl); }
// lamp posts and a well in the square
for (const [x, z] of [[-5, 6], [5, 6], [-9, 20], [9, 20]]) { M(cyl(0.07, 0.09, 3.2, 10), flat(INK), { p: [x, 1.6, z], to: village }); M(box(0.45, 0.55, 0.45), flat(0xffd27a), { ol: 0.03, p: [x, 3.45, z], to: village, cast: false }); }
const sky = (() => { const t = ctex(16, 256, g => { const r = g.createLinearGradient(0, 0, 0, 256); r.addColorStop(0, '#3f7fd8'); r.addColorStop(0.6, '#8fc4f0'); r.addColorStop(1, '#d8ecf8'); g.fillStyle = r; g.fillRect(0, 0, 16, 256); }); const m = M(new THREE.SphereGeometry(190, 32, 16), new THREE.MeshBasicMaterial({ map: t, side: THREE.BackSide, fog: false }), { cast: false }); root.add(m); m.userData.t = t; return m; })();
const clouds = new THREE.Group(); root.add(clouds); for (let i = 0; i < 14; i++) { const c = new THREE.Group(); c.position.set(-90 + rnd() * 180, 45 + rnd() * 20, -150 + rnd() * 80); clouds.add(c); for (let k = 0; k < 5; k++) M(sph(3 + rnd() * 3, 14, 10), toon(0xffffff), { ol: 0.2, p: [k * 3.5 - 7, rnd() * 2, rnd() * 2], to: c, cast: false }); }
function skyAt(top, mid, bot) { const g = sky.userData.t.userData.g; const r = g.createLinearGradient(0, 0, 0, 256); r.addColorStop(0, top); r.addColorStop(0.6, mid); r.addColorStop(1, bot); g.fillStyle = r; g.fillRect(0, 0, 16, 256); sky.userData.t.needsUpdate = true; }

// ---------- carts and horses ----------
function makeHorse(col = 0x8a5a34) { const h = new THREE.Group(), m = toon(col), dark = toon(0x3a2416); M(new THREE.CapsuleGeometry(0.45, 1.2, 6, 14), m, { ol: 0.04, p: [0, 1.4, 0], r: [Math.PI / 2, 0, 0], to: h }); const neck = new THREE.Group(); neck.position.set(0, 1.7, 0.75); h.add(neck); M(new THREE.CapsuleGeometry(0.22, 0.6, 4, 10), m, { ol: 0.035, p: [0, 0.35, 0.15], r: [0.6, 0, 0], to: neck }); M(new THREE.CapsuleGeometry(0.22, 0.45, 4, 10), m, { ol: 0.035, p: [0, 0.7, 0.45], r: [1.4, 0, 0], to: neck }); M(box(0.1, 0.5, 0.5), dark, { ol: 0.02, p: [0, 0.65, 0.05], to: neck }); for (const s of [-1, 1]) { M(new THREE.ConeGeometry(0.07, 0.22, 6), m, { ol: 0.02, p: [s * 0.12, 0.98, 0.38], to: neck }); M(sph(0.05, 8, 6), flat(INK), { p: [s * 0.2, 0.82, 0.55], to: neck, cast: false }); } h.userData.neck = neck; h.userData.legs = []; for (const [x, z] of [[-0.25, 0.6], [0.25, 0.6], [-0.25, -0.6], [0.25, -0.6]]) { const l = new THREE.Group(); l.position.set(x, 1.15, z); h.add(l); M(cyl(0.09, 0.08, 1.1, 8), m, { ol: 0.03, p: [0, -0.55, 0], to: l }); M(cyl(0.11, 0.11, 0.12, 8), dark, { p: [0, -1.1, 0], to: l }); h.userData.legs.push(l); } M(new THREE.ConeGeometry(0.16, 0.8, 8), dark, { ol: 0.025, p: [0, 1.5, -1.05], r: [-0.8, 0, 0], to: h }); return h; }
function makeCart(load = 6) { const c = new THREE.Group(), wood = toon(0xffffff, { map: T2s.wood }); M(box(1.8, 0.5, 2.6), wood, { ol: 0.04, p: [0, 0.95, 0], to: c }); c.userData.wheels = []; for (const z of [-0.75, 0.75]) for (const s of [-1, 1]) { const w = new THREE.Group(); w.position.set(s * 1.0, 0.55, z); c.add(w); M(cyl(0.55, 0.55, 0.12, 20), toon(0x4a2e1c), { ol: 0.03, r: [0, 0, Math.PI / 2], to: w }); for (let i = 0; i < 4; i++) M(box(0.06, 1.0, 0.05), toon(0xd9b36a), { r: [i * Math.PI / 4, 0, 0], to: w, cast: false }); c.userData.wheels.push(w); } for (const s of [-1, 1]) M(box(0.08, 0.08, 2.0), toon(0x6b4326), { p: [s * 0.55, 1.0, 2.2], to: c });
  c.userData.barrels = []; for (let i = 0; i < load; i++) { const b = new THREE.Group(); b.position.set(-0.45 + (i % 2) * 0.9, 1.6 + Math.floor(i / 4) * 0.8, -0.8 + (Math.floor(i / 2) % 2) * 0.8 + (i >= 4 ? 0.4 : 0)); c.add(b); M(cyl(0.35, 0.31, 0.8, 12), toon(0x8a5a34), { ol: 0.03, to: b }); for (const y of [-0.22, 0.22]) M(new THREE.TorusGeometry(0.36, 0.022, 6, 14), toon(0x2a2530), { p: [0, y, 0], r: [Math.PI / 2, 0, 0], to: b, cast: false }); c.userData.barrels.push(b); }
  const horse = makeHorse(); horse.position.set(0, 0, 3.3); c.add(horse); c.userData.horse = horse; return c; }
const cartR = makeCart(8); root.add(cartR); const cartH = makeCart(4); root.add(cartH); const cartsBg = [makeCart(3), makeCart(4), makeCart(2)]; cartsBg.forEach(c => root.add(c));
const steamH = puffs(root, 8, 0xffffff); const brakeSmoke = puffs(root, 14, 0xdddddd); const snowDust = puffs(root, 16, 0xffffff);
function placeOnCurve(obj, curve, u, back = false) { u = cl(u); const p = curve.getPointAt(u), tg = curve.getTangentAt(u); if (back) tg.negate(); obj.position.copy(p); obj.lookAt(p.clone().add(tg)); obj.rotateX(0); }
function trot(c, t, speed = 1) { const h = c.userData.horse; h.userData.legs.forEach((l, i) => l.rotation.x = 0.5 * Math.sin(t * 9 * speed + (i % 2 ? 0 : Math.PI) + (i > 1 ? Math.PI / 2 : 0))); h.userData.neck.rotation.x = 0.06 * Math.sin(t * 9 * speed); c.userData.wheels.forEach(w => w.rotation.x = -t * 4 * speed); }

// ---------- cast (skin-coloured heads like TheOddTrick) ----------
const SKINS = ['#f6c9a0', '#f0b98c', '#e9b07e', '#f8d2ac'];
const furHat = hg => { const m = flat(0x5a3a2a); M(cyl(0.5, 0.56, 0.6, 28), m, { ol: 0.045, p: [0, 0.7, 0], to: hg }); M(new THREE.TorusGeometry(0.56, 0.12, 10, 28), flat(0x8a6a4a), { ol: 0.035, p: [0, 0.42, 0], r: [Math.PI / 2, 0, 0], to: hg }); };
const flatCap = (col) => hg => { const m = flat(col); M(new THREE.SphereGeometry(0.62, 32, 16, 0, Math.PI * 2, 0, Math.PI * 0.36), m, { ol: 0.045, p: [0, 0.1, -0.03], s: [1.06, 0.72, 1.1], to: hg }); M(cyl(0.38, 0.4, 0.06, 24), m, { ol: 0.04, p: [0, 0.3, 0.52], s: [1.1, 1, 0.6], r: [0.12, 0, 0], to: hg }); };
const rudolf = makeChar3({ skin: '#f6c9a0', stache: true, shoe: 0x1b1522, scarf: 0xb3272d, belt3d: 0x3a2416, buttons3d: 0xffd34d, body: (g, w, h) => { g.fillStyle = '#4a2f6b'; g.fillRect(0, 0, w, h); g.fillStyle = '#8a6a4a'; g.fillRect(0, 0, w, h * 0.12); g.fillRect(w * 0.44, 0, w * 0.12, h); for (let i = 0; i < 90; i++) { g.fillStyle = 'rgba(60,40,25,0.35)'; g.fillRect(w * (0.44 + Math.random() * 0.12), Math.random() * h, 3, 9); g.fillRect(Math.random() * w, Math.random() * h * 0.12, 3, 9); } g.fillStyle = '#ffd34d'; g.beginPath(); g.arc(w * 0.3, h * 0.42, 14, 0, 7); g.fill(); g.strokeStyle = '#ffd34d'; g.lineWidth = 5; g.beginPath(); g.moveTo(w * 0.3, h * 0.42); g.quadraticCurveTo(w * 0.36, h * 0.55, w * 0.44, h * 0.48); g.stroke(); }, hat: furHat });
const hans = makeChar3({ skin: '#f0b98c', beard: '#d9d4c8', wrinkles: true, shoe: 0x3a2416, scarf: 0x2f6b4f, belt3d: 0x5a3a22, body: (g, w, h) => { g.fillStyle = '#7a5232'; g.fillRect(0, 0, w, h); g.strokeStyle = 'rgba(40,20,10,0.35)'; g.lineWidth = 4; for (let x = 0; x < w; x += 40) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, h); g.stroke(); } for (let y = 0; y < h; y += 40) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); } g.fillStyle = '#3a5a3a'; g.fillRect(w * 0.3, h * 0.35, w * 0.4, h * 0.55); }, hat: flatCap(0x5a6a3a) });
const folk = ['#c98a2a', '#3f8f8a', '#b0567a', '#5a6ab0', '#2f6b4f', '#d9a23a'].map((c, i) => makeChar3({ skin: SKINS[i % 4], freckles: i % 3 === 0, stache: i % 3 === 1, collar: i % 2 ? 0xf3efe6 : null, belt3d: i % 2 ? 0x3a2416 : null, shoe: 0x3a2416, body: bodyTex(c, '#1b1522', { buttons: i % 3 === 1, apron: i % 4 === 2 }), hat: i % 2 ? hoodHat([0xd9b36a, 0x57b0aa, 0xd9869f][i % 3]) : flatCap([0x5a3a2a, 0x2a3552, 0x6a2f3a][i % 3]) }));
const mug = new THREE.Group(); root.add(mug); M(cyl(0.11, 0.09, 0.22, 14), toon(0xf3efe6), { ol: 0.02, to: mug }); M(new THREE.TorusGeometry(0.07, 0.02, 6, 12), toon(0xf3efe6), { p: [0.13, 0, 0], to: mug });
const CAST = [rudolf, hans, ...folk]; CAST.forEach(c => root.add(c.g));
const SETS = [world, cartR, cartH, ...cartsBg, mug, sky, clouds, ...CAST.map(c => c.g)];
function hideAll() { SETS.forEach(g => g.visible = false); [...steamH, ...brakeSmoke, ...snowDust].forEach(s => s.visible = false); }
function hold(c, hand, obj, off = V(0, 0, 0), rot = [0, 0, 0]) { c.g.updateMatrixWorld(true); const p = V(...hand); c.up.localToWorld(p); obj.visible = true; obj.position.copy(p).add(off); obj.rotation.set(...rot); }
function seat(c, cart, side = 0, h = 0.32) { c.g.visible = true; cart.updateMatrixWorld(true); const p = V(side, h, 0.7); cart.localToWorld(p); c.g.position.copy(p); c.g.quaternion.copy(cart.quaternion); c.g.scale.setScalar(SC * 0.8); c.legs.forEach(l => { l.a.visible = false; l.f.visible = false; }); }
function summer(t) { world.visible = true; sky.visible = true; clouds.visible = true; skyAt('#3f7fd8', '#8fc4f0', '#d8ecf8'); bg(0x8fc4f0); light(0.85, 1.9, [-30, 45, 25], 0xfff2d8, 0x6a8a5a); terrainM.color.set(0xffffff); pines.forEach(p => p.userData.snow.forEach(s => s.visible = false)); houses.forEach(h => h.userData.snow.visible = false); LOOK.grade = ['#ffd9a0', 0.12]; LOOK.bloom = 0.16; }
// ===== detail pass: haze, vegetation, stones, fences, stream and bridges, sheep, birds, jagged peaks, house and cart dressing =====
root.fog = new THREE.Fog(0xcfe6f5, 55, 210); sky.material.fog = false; clouds.children.forEach(c => c.children.forEach(m => { if (m.material) m.material.fog = false; }));
const dummy = new THREE.Object3D(), tmpC = new THREE.Color();
function nearRoad(x, z, pad) { if (Math.abs(x) < 1.6 + pad && z < 6) return true; for (let j = 0; j < ZZ.length - 1; j++) if (distSeg(x, z, ZZ[j][0], ZZ[j][1], ZZ[j + 1][0], ZZ[j + 1][1]) < 1.4 + pad) return true; return false; }
// grass tufts (instanced) and wildflowers
{ const geo = new THREE.ConeGeometry(0.09, 0.42, 4); geo.translate(0, 0.21, 0); const n = 9000; const im = new THREE.InstancedMesh(geo, toon(0xffffff), n); let k = 0;
  for (let i = 0; i < n * 3 && k < n; i++) { const x = (rnd() - 0.5) * 84, z = TOPZ - 4 + rnd() * 92; if (nearRoad(x, z, 0.1) || (z > 0 && Math.abs(x) < 26 && z < 24 && rnd() < 0.6)) continue; dummy.position.set(x, hT(x, z), z); dummy.rotation.set((rnd() - 0.5) * 0.4, rnd() * 6.28, (rnd() - 0.5) * 0.4); dummy.scale.setScalar(0.6 + rnd() * 1.2); dummy.updateMatrix(); im.setMatrixAt(k, dummy.matrix); im.setColorAt(k, tmpC.set(rnd() < 0.5 ? 0x5f9a3c : 0x86c25e)); k++; }
  im.count = k; im.receiveShadow = true; world.add(im); world.userData.grass = im;
  const fg = new THREE.SphereGeometry(0.075, 6, 4); fg.translate(0, 0.34, 0); const fn = 2600; const fm = new THREE.InstancedMesh(fg, flat(0xffffff), fn); let q = 0; const fc = [0xe2553d, 0xf2c230, 0xffffff, 0xd9869f, 0x7f8fd0];
  for (let i = 0; i < fn * 3 && q < fn; i++) { const x = (rnd() - 0.5) * 80, z = TOPZ - 2 + rnd() * 88; if (nearRoad(x, z, 0.3)) continue; dummy.position.set(x, hT(x, z), z); dummy.rotation.set(0, 0, 0); dummy.scale.setScalar(0.8 + rnd() * 0.6); dummy.updateMatrix(); fm.setMatrixAt(q, dummy.matrix); fm.setColorAt(q, tmpC.set(fc[Math.floor(rnd() * fc.length)])); q++; }
  fm.count = q; world.add(fm); world.userData.flowers = fm; }
// roadside stones along both roads
{ const geo = new THREE.DodecahedronGeometry(0.22, 0); const n = 1400; const im = new THREE.InstancedMesh(geo, toon(0xffffff, { map: T3.rock }), n); let k = 0;
  for (const [road, w] of [[roadS, 1.65], [roadZ, 1.45]]) { const c = road.userData.curve, L = c.getLength(); for (let d = 0; d < L && k < n; d += 0.55) { const u = d / L, p = c.getPointAt(u), tg = c.getTangentAt(u), side = V(-tg.z, 0, tg.x).normalize(); for (const s of [-1, 1]) { if (rnd() < 0.35) continue; const q = p.clone().addScaledVector(side, s * (w + rnd() * 0.25)); dummy.position.set(q.x, hT(q.x, q.z) + 0.05, q.z); dummy.rotation.set(rnd() * 3, rnd() * 3, rnd() * 3); dummy.scale.set(0.6 + rnd() * 0.9, 0.4 + rnd() * 0.5, 0.6 + rnd() * 0.9); dummy.updateMatrix(); im.setMatrixAt(k, dummy.matrix); im.setColorAt(k, tmpC.setHSL(0.6, 0.05, 0.55 + rnd() * 0.2)); k++; } } }
  im.count = k; im.castShadow = true; world.add(im); }
// wooden fence with rails along the downhill side of every bend of the old road
{ const c = roadZ.userData.curve, L = c.getLength(), postM = toon(0x7a5232), railM = toon(0x8a6a44); let prev = null;
  for (let d = 2; d < L - 8; d += 1.6) { const u = d / L, p = c.getPointAt(u), tg = c.getTangentAt(u); let side = V(-tg.z, 0, tg.x).normalize(); if (side.z < 0) side.negate(); const q = p.clone().addScaledVector(side, 1.7); q.y = hT(q.x, q.z); M(box(0.14, 0.9, 0.14), postM, { ol: 0.02, p: [q.x, q.y + 0.45, q.z], to: world }); if (prev && prev.distanceTo(q) < 2.2) for (const hh of [0.4, 0.75]) { const a = prev.clone().add(V(0, hh, 0)), b = q.clone().add(V(0, hh, 0)), mid = a.clone().lerp(b, 0.5), rail = M(box(0.06, 0.07, a.distanceTo(b)), railM, { to: world, cast: false }); rail.position.copy(mid); rail.lookAt(b); } prev = q; } }
// stream across the village plain, with two wooden bridges
const water = (() => { const t = ctex(256, 256, (g, w, h) => { g.fillStyle = '#3f8fd0'; g.fillRect(0, 0, w, h); g.strokeStyle = 'rgba(255,255,255,0.55)'; g.lineWidth = 4; g.lineCap = 'round'; for (let i = 0; i < 26; i++) { const x = rnd() * w, y = rnd() * h; g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + 12, y - 5, x + 26, y); g.stroke(); } }); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(1, 6); return t; })();
{ const pts = []; for (let x = -60; x <= 60; x += 6) pts.push([x, 3.2 + 1.2 * Math.sin(x * 0.12)]); const geo = ribbon(pts, 2.6, toon(0xffffff, { map: water }), 0.03).geometry; const st = new THREE.Mesh(geo, toon(0xffffff, { map: water })); world.add(st); world.userData.water = water;
  const bankG = new THREE.DodecahedronGeometry(0.35, 0), bank = new THREE.InstancedMesh(bankG, toon(0xffffff, { map: T3.rock }), 260); let k = 0; for (let x = -58; x <= 58 && k < 260; x += 0.9) for (const s of [-1, 1]) { const z = 3.2 + 1.2 * Math.sin(x * 0.12) + s * (1.45 + rnd() * 0.2); dummy.position.set(x + rnd() * 0.3, 0.08, z); dummy.rotation.set(rnd() * 3, rnd() * 3, 0); dummy.scale.set(0.8 + rnd() * 0.6, 0.5, 0.8 + rnd() * 0.6); dummy.updateMatrix(); bank.setMatrixAt(k, dummy.matrix); bank.setColorAt(k, tmpC.setHSL(0.6, 0.06, 0.5 + rnd() * 0.2)); k++; } bank.count = k; world.add(bank);
  function bridge(x, z, ry) { const b = new THREE.Group(); b.position.set(x, 0, z); b.rotation.y = ry; world.add(b); for (let i = -6; i <= 6; i++) M(box(3.2, 0.12, 0.34), toon(i % 2 ? 0x8a5a34 : 0x7a4a2c), { ol: 0.015, p: [0, 0.35 + 0.12 * Math.cos(i / 6 * 1.5), i * 0.36], to: b }); for (const s of [-1, 1]) { for (const zz of [-2.2, 0, 2.2]) M(box(0.14, 1.0, 0.14), toon(0x6b4326), { ol: 0.02, p: [s * 1.55, 0.75, zz], to: b }); M(box(0.08, 0.08, 4.6), toon(0x8a6a44), { ol: 0.015, p: [s * 1.55, 1.15, 0], to: b }); } }
  bridge(0, 3.2 + 1.2 * Math.sin(0), 0); bridge(-17.8, 3.2 + 1.2 * Math.sin(-17.8 * 0.12), 0.55); }
// foothills on both sides to close the horizon, with their own pines
for (const [x, z, r, sy] of [[-75, -30, 38, 0.55], [78, -26, 40, 0.5], [-70, 30, 30, 0.35], [72, 34, 28, 0.35], [0, 70, 50, 0.22]]) { M(new THREE.SphereGeometry(r, 28, 16), toon(0x6aa84f), { p: [x, -r * 0.25, z], s: [1, sy, 1], to: world, cast: false, recv: true }); for (let i = 0; i < 14; i++) { const a = rnd() * 6.28, rr = r * (0.3 + rnd() * 0.5), px = x + Math.cos(a) * rr, pz = z + Math.sin(a) * rr * 0.6; const top = -r * 0.25 + r * sy * Math.sqrt(Math.max(0, 1 - (rr / r) ** 2)); pines.push(pine(world, px, top - 0.3, pz, 1.2 + rnd())); } }
// jagged snow-capped peaks (vertex-coloured: rock below, snow above)
for (const [x, z, h, r] of [[-28, -128, 78, 34], [12, -140, 92, 40], [48, -122, 70, 32], [-62, -112, 60, 30], [78, -134, 74, 34], [-95, -130, 66, 32]]) {
  const geo = new THREE.ConeGeometry(r, h, 12, 8); const p = geo.attributes.position, col = []; for (let i = 0; i < p.count; i++) { const y = p.getY(i), fr = (y + h / 2) / h; if (fr < 0.98) { const a = Math.atan2(p.getZ(i), p.getX(i)); const n = 1 + 0.18 * Math.sin(a * 5 + x) + 0.12 * Math.sin(a * 11 + z); p.setX(i, p.getX(i) * n); p.setZ(i, p.getZ(i) * n); p.setY(i, y + Math.sin(a * 7 + x) * 2.2 * (1 - fr)); } const snow = fr > 0.62 + 0.08 * Math.sin(Math.atan2(p.getZ(i), p.getX(i)) * 6); tmpC.set(snow ? 0xf4f6fb : (fr > 0.35 ? 0x8a8a9e : 0x6f7486)); col.push(tmpC.r, tmpC.g, tmpC.b); } geo.setAttribute('color', new THREE.Float32BufferAttribute(col, 3)); geo.computeVertexNormals();
  M(geo, new THREE.MeshToonMaterial({ vertexColors: true, gradientMap: grad, flatShading: true }), { ol: 0.3, p: [x, h / 2 + TOPH - 10, z], to: world, cast: false }); }
world.children.forEach(m => { if (m.geometry && m.geometry.type === 'ConeGeometry' && m.geometry.parameters.radialSegments === 7) m.visible = false; });  // retire the old smooth cones
// grazing sheep on the slopes
const sheep = []; for (let i = 0; i < 10; i++) { const x = 9 + rnd() * 22, z = -44 + rnd() * 36; if (nearRoad(x, z, 1)) continue; const s = new THREE.Group(); s.position.set(x, hT(x, z), z); s.rotation.y = rnd() * 6.28; world.add(s); for (const [px, py, pz, r] of [[0, 0.75, 0, 0.42], [0.3, 0.8, 0.1, 0.32], [-0.3, 0.8, -0.1, 0.32], [0, 0.95, 0.25, 0.3], [0, 0.95, -0.25, 0.3]]) M(sph(r, 12, 10), toon(0xf6f3ec), { ol: 0.035, p: [px, py, pz], to: s }); const head = M(sph(0.2, 12, 10), toon(0x2a2530), { ol: 0.025, p: [0.55, 0.78, 0], s: [1.3, 1, 0.9], to: s }); for (const [lx, lz] of [[0.25, 0.2], [0.25, -0.2], [-0.25, 0.2], [-0.25, -0.2]]) M(cyl(0.05, 0.05, 0.5, 6), toon(0x2a2530), { p: [lx, 0.25, lz], to: s }); s.userData.head = head; sheep.push(s); }
// birds
const birds = []; for (let i = 0; i < 9; i++) { const b = new THREE.Group(); world.add(b); const wm = flat(0x2a2530, { side: THREE.DoubleSide }); for (const s of [-1, 1]) { const w = new THREE.Group(); b.add(w); M(box(0.9, 0.04, 0.3), wm, { p: [s * 0.45, 0, 0], to: w, cast: false }); w.userData.s = s; } b.userData = { x0: -40 + rnd() * 30, y: 66 + rnd() * 10, z: -105 + rnd() * 25, sp: 2 + rnd(), ph: rnd() * 6 }; birds.push(b); }
// house dressing: window boxes with flowers, shutters, garden fences, hay bales, washing line
houses.forEach((h, i) => { const fb = new THREE.Group(); fb.position.set(0, 2.2, 2.05); h.add(fb); M(box(1.3, 0.25, 0.35), toon(0x8a5a34), { ol: 0.02, to: fb }); for (let j = 0; j < 5; j++) M(sph(0.11, 8, 6), flat([0xe2553d, 0xf2c230, 0xd9869f][(i + j) % 3]), { p: [-0.5 + j * 0.25, 0.2, 0], to: fb, cast: false }); for (const s of [-1, 1]) M(box(0.42, 1.0, 0.06), toon([0x2f6b4f, 0x3a5a8a, 0x8a3a3a][i % 3]), { ol: 0.018, p: [s * 0.95, 0.75, 0.0], to: fb });
  for (let j = -3; j <= 3; j++) M(box(0.1, 0.6, 0.1), toon(0xd9c9a0), { ol: 0.015, p: [j * 0.7, 0.3, 3.4], to: h }); M(box(4.4, 0.08, 0.06), toon(0xd9c9a0), { p: [0, 0.48, 3.4], to: h, cast: false }); });
for (const [x, z] of [[8, 4.5], [9.4, 5.2], [-7, 5]]) { M(cyl(0.7, 0.7, 1.2, 16), toon(0xe2c26a), { ol: 0.03, p: [x, 0.7, z], r: [0, 0, Math.PI / 2], to: world }); M(new THREE.TorusGeometry(0.7, 0.04, 6, 18), toon(0xb79a50), { p: [x, 0.7, z], r: [0, Math.PI / 2, 0], to: world, cast: false }); }
// cart dressing: side boards, rope over the load, lantern on a pole; horse mane, tail, harness
function dressCart(c) { const wood = toon(0xffffff, { map: T2s.wood }); for (const s of [-1, 1]) M(box(0.08, 0.45, 2.6), wood, { ol: 0.02, p: [s * 0.9, 1.4, 0], to: c }); M(box(1.8, 0.45, 0.08), wood, { ol: 0.02, p: [0, 1.4, -1.3], to: c }); for (const z of [-0.5, 0.5]) M(new THREE.TorusGeometry(0.75, 0.025, 6, 20, Math.PI), toon(0xd9b36a), { p: [0, 1.6, z], to: c, cast: false });
  const lp = new THREE.Group(); lp.position.set(0.85, 1.2, -1.2); c.add(lp); M(cyl(0.03, 0.03, 1.4, 6), flat(INK), { p: [0, 0.7, 0], to: lp }); M(box(0.2, 0.26, 0.2), flat(0xffd27a), { ol: 0.02, p: [0, 1.45, 0.08], to: lp, cast: false });
  const h = c.userData.horse, n = h.userData.neck; for (let i = 0; i < 6; i++) M(box(0.08, 0.18, 0.12), toon(0x3a2416), { p: [0, 0.25 + i * 0.1, 0.0 + i * 0.07], r: [0.6, 0, 0], to: n, cast: false }); M(new THREE.TorusGeometry(0.3, 0.05, 6, 16), toon(0x2a2530), { ol: 0.015, p: [0, 1.5, 0.55], r: [0.2, 0, 0], to: h }); for (const s of [-1, 1]) M(box(0.04, 0.06, 2.2), toon(0x2a2530), { p: [s * 0.46, 1.45, -0.4], to: h, cast: false }); M(box(0.06, 0.14, 0.14), flat(0x2a2530), { p: [0.18, 0.78, 0.45], to: n, cast: false }); M(box(0.06, 0.14, 0.14), flat(0x2a2530), { p: [-0.18, 0.78, 0.45], to: n, cast: false }); }
[cartR, cartH, ...cartsBg].forEach(dressCart);
// Rudolf's cane
const cane = new THREE.Group(); root.add(cane); M(cyl(0.035, 0.035, 1.6, 8), toon(0x2a2530), { ol: 0.015, p: [0, -0.8, 0], to: cane }); M(sph(0.08, 10, 8), toon(0xffd34d), { ol: 0.015, to: cane });
// per-frame animation of the living details
function detailTick(t) { if (world.userData.water) world.userData.water.offset.y = -t * 0.25; sheep.forEach((s, i) => { s.userData.head.position.y = 0.72 + 0.08 * Math.sin(t * 1.5 + i * 2); });
  birds.forEach(b => { const d = b.userData; b.position.set(d.x0 + ((t * d.sp + d.ph * 10) % 80), d.y + Math.sin(t * 0.8 + d.ph) * 2, d.z); b.rotation.y = -Math.PI / 2; b.children.forEach(w => w.rotation.z = w.userData.s * 0.5 * Math.sin(t * 9 + d.ph)); }); }
const hideAllBase = hideAll; hideAll = function () { hideAllBase(); cane.visible = false; };
// ===== second half: winter, blast, explainer props, playground, crash =====
T3.snow = (() => { const t = ctex(512, 512, (g, w, h) => { g.fillStyle = '#eef3fb'; g.fillRect(0, 0, w, h); for (let i = 0; i < 700; i++) { g.fillStyle = `rgba(${rnd() < 0.5 ? '150,170,210' : '255,255,255'},${0.15 + rnd() * 0.3})`; g.beginPath(); g.ellipse(rnd() * w, rnd() * h, 3 + rnd() * 14, 2 + rnd() * 6, rnd() * 3, 0, 7); g.fill(); } }); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(14, 14); return t; })();
T3.ice = (() => { const t = ctex(256, 512, (g, w, h) => { g.fillStyle = '#b9cde6'; g.fillRect(0, 0, w, h); g.strokeStyle = 'rgba(255,255,255,0.7)'; g.lineWidth = 3; for (let i = 0; i < 40; i++) { const x = rnd() * w, y = rnd() * h; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (rnd() - 0.5) * 40, y + 30 + rnd() * 50); g.stroke(); } g.strokeStyle = 'rgba(90,110,150,0.4)'; g.lineWidth = 10; for (const x of [0.3, 0.7]) { g.beginPath(); g.moveTo(w * x, 0); g.lineTo(w * x, h); g.stroke(); } }); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t; })();
function winter(t) { world.visible = true; sky.visible = true; clouds.visible = true; skyAt('#8a96b0', '#c9d2e2', '#eef1f6'); bg(0xc9d2e2); root.fog.color.set(0xdfe5ee); light(0.95, 1.4, [-30, 40, 25], 0xe8eeff, 0x8a90a8);
  terrainM.map = T3.snow; dirtM.map = T3.ice; terrainM.needsUpdate = dirtM.needsUpdate = true; if (world.userData.grass) world.userData.grass.visible = false; if (world.userData.flowers) world.userData.flowers.visible = false; sheep.forEach(s => s.visible = false); birds.forEach(b => b.visible = false);
  pines.forEach(p => p.userData.snow.forEach(s => s.visible = true)); houses.forEach(h => h.userData.snow.visible = true); if (world.userData.water) world.userData.water.offset.y = 0; LOOK.grade = ['#9fb4ff', 0.14]; LOOK.bloom = 0.2; }
const summer0 = summer; summer = function (t) { summer0(t); root.fog.color.set(0xcfe6f5); terrainM.map = T3.grass; dirtM.map = T3.dirt; terrainM.needsUpdate = dirtM.needsUpdate = true; if (world.userData.grass) world.userData.grass.visible = true; if (world.userData.flowers) world.userData.flowers.visible = true; sheep.forEach(s => s.visible = true); birds.forEach(b => b.visible = true); };
function snowfall(t, n = 80) { ctx.save(); ctx.fillStyle = 'rgba(255,255,255,0.92)'; for (let i = 0; i < n; i++) { const p = ((t * 0.09 + i * 0.0613) % 1), x = ((i * 977) % W) + 50 * Math.sin(t * 1.3 + i), y = p * H, r = 4 + (i % 4) * 2.5; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill(); } ctx.restore(); }
// blasting plunger and dust
const plunger = new THREE.Group(); root.add(plunger); M(box(0.7, 0.5, 0.5), toon(0xb3272d), { ol: 0.03, p: [0, 0.25, 0], to: plunger }); plunger.userData.rod = M(cyl(0.05, 0.05, 0.6, 8), toon(0x2a2530), { ol: 0.015, p: [0, 0.75, 0], to: plunger }); M(box(0.6, 0.08, 0.08), toon(0x2a2530), { ol: 0.015, p: [0, 1.05, 0], to: plunger.userData.rod.parent }); plunger.userData.handle = plunger.children[plunger.children.length - 1];
const blast = puffs(root, 36, 0xc9a77a); const rocksFly = []; for (let i = 0; i < 18; i++) { const r = M(new THREE.DodecahedronGeometry(0.4, 0), toon(0xffffff, { map: T3.rock }), { ol: 0.04 }); root.add(r); rocksFly.push(r); }
// explainer arrows: one long hard pull on the straight road, small gentle ones on the bends
function arrowMesh(col, len) { const g = new THREE.Group(), m = flat(col); M(cyl(0.35, 0.35, len, 14), m, { ol: 0.08, p: [0, len / 2, 0], to: g, cast: false }); M(new THREE.ConeGeometry(0.85, 1.6, 16), m, { ol: 0.08, p: [0, len + 0.8, 0], to: g, cast: false }); return g; }
const arrowBig = arrowMesh(0xe2372d, 22); root.add(arrowBig); const arrowSmall = [0, 1, 2, 3].map(() => { const a = arrowMesh(0x35c46a, 4.5); root.add(a); return a; });
function aimArrow(a, from, to, sc) { a.visible = true; a.position.copy(from); a.quaternion.setFromUnitVectors(UP, to.clone().sub(from).normalize()); a.scale.setScalar(sc); }
// playground in the square: stairs and a slide
const play = new THREE.Group(); world.add(play); play.position.set(24, 0, 22); play.rotation.y = -0.5;
{ const wood = toon(0xffffff, { map: T2s.wood }); for (let i = 0; i < 7; i++) M(box(1.4, 0.4, 0.6), wood, { ol: 0.025, p: [-2.2, 0.2 + i * 0.4, -1.8 + i * 0.6], to: play }); for (const s of [-1, 1]) M(box(0.1, 3.2, 0.1), toon(0x6b4326), { p: [-2.2 + s * 0.7, 1.6, 1.8], to: play });
  M(box(2.2, 0.2, 1.6), wood, { ol: 0.03, p: [-1.4, 2.9, 2.2], to: play }); const sl = M(box(1.3, 0.12, 6.6), toon(0xe2553d), { ol: 0.035, p: [1.6, 1.5, 2.2], r: [0, 0, 0], to: play }); sl.rotation.set(0, Math.PI / 2, 0); sl.rotateX(-0.45); for (const s of [-1, 1]) { const rail = M(box(0.12, 0.3, 6.6), toon(0xf2c230), { ol: 0.02, p: [1.6, 1.68, 2.2 + s * 0.6], to: play }); rail.rotation.set(0, Math.PI / 2, 0); rail.rotateX(-0.45); } }
const kidA = makeChar3({ skin: '#f6c9a0', freckles: true, shoe: 0x3a2416, scarf: 0x3b5bd9, body: bodyTex('#e2553d', '#1b1522', {}), hat: hoodHat(0xf2c230) });
const kidB = makeChar3({ skin: '#e9b07e', shoe: 0x3a2416, scarf: 0xe2553d, body: bodyTex('#3f8f8a', '#1b1522', {}), hat: hoodHat(0x5a6ab0) });
[kidA, kidB].forEach(c => root.add(c.g));
// crash debris
const planks = []; for (let i = 0; i < 10; i++) { const p = M(box(0.25, 2.2, 0.08), toon(0x6b4326), { ol: 0.02 }); root.add(p); planks.push(p); }
const SETS3 = [plunger, arrowBig, ...arrowSmall, kidA.g, kidB.g, ...rocksFly, ...planks];
const hideAllW = hideAll; hideAll = function () { hideAllW(); SETS3.forEach(g => g.visible = false); blast.forEach(s => s.visible = false); cartR.userData.horse.visible = true; ware.userData.barrels.forEach(b => b.visible = true); wareDoors.forEach(d => d.visible = true); };
// physics for flying things: deterministic arcs with a bounce
function flyArc(p0, v, t, gy = -9.8) { const p = V(p0.x + v.x * t, p0.y + v.y * t + 0.5 * gy * t * t, p0.z + v.z * t); if (p.y < 0.3) { const tl = (v.y + Math.sqrt(v.y * v.y - 2 * gy * (p0.y - 0.3))) / -gy; const dt = t - tl; p.x = p0.x + v.x * tl + v.x * 0.35 * dt; p.z = p0.z + v.z * tl + v.z * 0.35 * dt; p.y = 0.3 + Math.max(0, -v.y * 0.25 * dt + 0.5 * gy * dt * dt); } return p; }
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
  LOOK.grade = ['#ffc98a', 0.1]; LOOK.bloom = 0.14; LOOK.dof = null; detailTick(t);
  const RS = roadS.userData.curve, RZ = roadZ.userData.curve;

  if (li === 0) { // HOOK: Rudolf at the top of his straight road, then a drone dive down it to the warehouse
    summer(t); const tf = wf(0, 'and') - 0.15;
    if (t < tf) { const p0 = RS.getPointAt(0.02); show(rudolf, p0.x + 0.6, p0.z + 0.8, 0.25); rudolf.g.position.y = p0.y - 0.05; rudolf.g.updateMatrixWorld(true); rudolf.face('happy');
      rudolf.pose({ rh: [0.55, 2.2, 0.95], lh: [-0.6, 2.9, 0.3], hx: 0.12, bob: 0.02 * Math.sin(t * 3) });
      hold(rudolf, [0.55, 2.2, 0.95], cane, V(0, 0.05, 0), [0.1, 0, 0.1]); const u = sub(0, tf), hp = rudolf.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + lerp(1.8, 2.6, u), hp.y - lerp(1.6, 0.4, u), hp.z + lerp(5.2, 6.4, u)], [hp.x + 0.2, hp.y - lerp(0.2, 1.4, u), hp.z], 52, t, 0, -0.05);
    } else { const u = ss(0, 1, sub(tf, s1 - 0.2)), uu = lerp(0.05, 0.93, u); const p = RS.getPointAt(uu), ahead = RS.getPointAt(Math.min(1, uu + 0.08));
      wareDoors.forEach((d, i) => d.rotation.y = (i ? 1 : -1) * 1.2);
      setCam([p.x + 0.6, p.y + lerp(5.0, 2.6, u), p.z - 2], [ahead.x, ahead.y + lerp(0.5, 1.4, u), ahead.z + 2], lerp(60, 50, u), t, 0.01 * (1 - u), 0.03);
      overlay = () => { ctx.save(); ctx.globalAlpha = 0.35 * (1 - u); ctx.strokeStyle = '#fff'; ctx.lineCap = 'round'; for (let i = 0; i < 18; i++) { const a = i / 18 * 6.283 + 0.3, r0 = 260 + (i * 53) % 120, r1 = r0 + 260; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(W / 2 + Math.cos(a) * r0, H * 0.45 + Math.sin(a) * r0); ctx.lineTo(W / 2 + Math.cos(a) * r1, H * 0.45 + Math.sin(a) * r1); ctx.stroke(); } ctx.restore(); };
    }
  }
  else if (li === 1) { // every cart took the old road
    summer(t); const u = sub(s0, s1);
    cartsBg.forEach((c, i) => { c.visible = true; placeOnCurve(c, RZ, 0.15 + i * 0.22 + u * 0.03); trot(c, t + i, 0.5); });
    cartH.visible = true; placeOnCurve(cartH, RZ, 0.84 + u * 0.02); trot(cartH, t, 0.5); seat(hans, cartH, 0.3); hans.face('happy'); hans.pose({ rh: [0.5, 2.0, 0.6], lh: [-0.5, 1.6, 0.6], hx: -0.15 });
    hold(hans, [0.5, 2.0, 0.6], mug, V(0, 0.1, 0.05)); mug.scale.setScalar(0.8); steamAt2(t, mug.position);
    const cp = cartH.position; setCam([cp.x + lerp(3.0, 2.2, u), cp.y + 3.0, cp.z + lerp(7.5, 6.5, u)], [cp.x, cp.y + 2.0, cp.z], 52, t, 0, 0.03); LOOK.dof = [700, 1500, 3];
  }
  else if (li === 2) { // forty bends, three hours
    summer(t); const u = sub(s0, s1);
    cartsBg.forEach((c, i) => { c.visible = true; placeOnCurve(c, RZ, 0.15 + i * 0.22 + (t - s0) * 0.01); trot(c, t + i, 0.5); });
    setCam([lerp(30, 24, u), lerp(46, 42, u), lerp(-24, -18, u)], [-20, 18, -30], 50, t, 0, 0.0);
  }
  else if (li === 3) { // Rudolf calls the old road a waste of a mountain
    summer(t); const p0 = RS.getPointAt(0.02); show(rudolf, p0.x - 4.5, p0.z + 1.0, 0.5); rudolf.g.position.y = hT(p0.x - 4.5, p0.z + 1.0) - 0.05; rudolf.g.updateMatrixWorld(true);
    rudolf.face(t > wf(3, 'waste') - 0.1 ? 'sneaky' : 'neutral'); rudolf.pose({ lh: [-0.95, 2.6, 0.4], rh: [0.5, 2.05, 0.05], hy: 0.25 * Math.sin((t - s0) * 5) * (t > wf(3, 'waste') ? 1 : 0), hx: 0.1 });
    const hp = rudolf.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 2.0, hp.y + 0.1, hp.z + lerp(4.0, 3.4, k)], [hp.x - 0.7, hp.y - 0.9, hp.z], 52, t, 0, 0.05);
  }
  else if (li === 4) { // he blasted his own road, straight down
    summer(t); const tb = wf(4, 'blasted') + 0.15, u = t - tb; const p0 = RS.getPointAt(0.02);
    show(rudolf, p0.x - 1.8, p0.z + 0.6, 0.3); rudolf.g.position.y = hT(p0.x - 1.8, p0.z + 0.6) - 0.05; rudolf.g.updateMatrixWorld(true); rudolf.face(u > 0 ? 'happy' : 'sneaky');
    plunger.visible = true; plunger.position.set(p0.x - 1.3, hT(p0.x - 1.3, p0.z + 1.4), p0.z + 1.4); const press = ss(tb - 0.4, tb, t); plunger.userData.rod.position.y = 0.75 - 0.35 * press;
    const hd = V(0, 1.05 - 0.35 * press, 0); plunger.localToWorld(hd); rudolf.pose({ rh: toLocal(rudolf, hd.clone().add(V(0.15, 0, 0))), lh: toLocal(rudolf, hd.clone().add(V(-0.15, 0, 0))), pitch: 0.25 });
    if (u > 0) blast.forEach((s, i) => { const d = (i % 12) / 12, z = lerp(TOPZ + 6, BOTZ - 2, d), te = u - d * 0.9; s.visible = te > 0; if (te <= 0) return; s.position.set((i % 3 - 1) * 1.2, hT(0, z) + 1 + te * 3, z); const sc = 3 + te * 6; s.scale.set(sc, sc, 1); s.material.opacity = Math.max(0, 0.8 - te * 0.45); });
    rocksFly.forEach((r, i) => { const d = (i % 9) / 9, te = u - d * 0.9; r.visible = te > 0 && te < 2.2; if (!r.visible) return; const z = lerp(TOPZ + 6, BOTZ - 2, d); const p = V((i % 2 ? 1 : -1) * (1.5 + te * 4), hT(0, z) + 1 + te * 9 - 4.9 * te * te, z + (i % 3 - 1) * te * 2); r.position.copy(p); r.rotation.set(te * 5, te * 3, 0); });
    if (t < tb + 0.3) { const hp = rudolf.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 1.6, hp.y + 0.2, hp.z + 5.4], [hp.x + 0.3, hp.y - 1.0, hp.z + 0.8], 50, t, 0, -0.05); }
    else setCam([lerp(26, 22, sub(tb, s1)), 40, lerp(-38, -34, sub(tb, s1))], [0, 20, -28], 56, t, 0.06 * Math.exp(-u * 2), 0.0);
    overlay = () => { if (u > 0 && u < 0.9) burst('BOOM!', 540, 420, 220, t, tb, tb + 0.9, -0.08); };
  }
  else if (li === 5) { // the warehouse full of barrels at the bottom
    summer(t); const u = sub(s0, s1); show(rudolf, 1.2, 8.2, 0.4); rudolf.face('happy'); rudolf.pose({ lh: [-0.4, 2.0, 0.6], rh: [0.7, 2.8, 0.3], bob: 0.02 * Math.sin(t * 4) }); hold(rudolf, [-0.4, 2.0, 0.6], cane, V(0, 0.05, 0), [0.1, 0, 0.1]);
    wareDoors.forEach((d, i) => d.rotation.y = (i ? 1 : -1) * 1.2);
    setCam([lerp(-4.5, -3.5, u), lerp(2.8, 3.2, u), lerp(1.0, 0.0, u)], [0.8, 2.2, 9.5], 52, t, 0, 0.04);
  }
  else if (li === 6) { // Hans keeps driving the bends, sipping coffee
    summer(t); const u = sub(s0, s1); cartH.visible = true; placeOnCurve(cartH, RZ, 0.42 + u * 0.03); trot(cartH, t, 0.45); seat(hans, cartH, 0.3); hans.face('happy');
    const sip = Math.max(0, Math.sin((t - s0) * 2.2)); hans.pose({ rh: [0.35, 2.1 + 0.4 * sip, 0.55], lh: [-0.5, 1.6, 0.6], hx: -0.25 * sip }); hold(hans, [0.35, 2.1 + 0.4 * sip, 0.55], mug, V(0, 0.1, 0.05)); mug.scale.setScalar(0.8); steamAt2(t, mug.position);
    const cp = cartH.position; setCam([cp.x + lerp(3.6, 3.0, u), cp.y + 2.4, cp.z + lerp(6.0, 5.2, u)], [cp.x, cp.y + 2.0, cp.z], 50, t, 0, 0.03); LOOK.dof = [500, 1450, 4];
  }
  else if (li === 7) { // the village calls him the snail of the mountain
    summer(t); const u = sub(s0, s1); cartH.visible = true; placeOnCurve(cartH, RZ, 0.93); trot(cartH, t, 0.3); seat(hans, cartH, 0.3); hans.face('happy'); hans.pose({ rh: [0.35, 2.1, 0.55], lh: [-0.5, 1.6, 0.6] }); hold(hans, [0.35, 2.1, 0.55], mug, V(0, 0.1, 0.05));
    folk.slice(0, 4).forEach((c, i) => { show(c, -7.5 + i * 1.2, 2.0 + (i % 2) * 0.7, -1.9); const lf = Math.abs(Math.sin(t * 7 + i)); c.face('happy'); c.pose({ pitch: 0.2 * lf, hx: -0.3 + 0.2 * lf, bob: 0.05 * lf, rh: i % 2 ? [0.7, 2.4, 0.6] : [0.5, 1.95, 0.05], lh: [-0.5, 1.95 + 0.3 * lf, 0.2] }); });
    setCam([lerp(3.5, 2.8, u), 3.6, lerp(6.0, 5.4, u)], [-11, 2.2, 1.5], 56, t, 0, 0.04);
    overlay = () => { burst('HA HA HA!', 320, 450, 170, t, s0 + 0.2, s1 - 0.03, -0.1); };
  }
  else if (li === 8) { // first month: twice as fast
    summer(t); const u = sub(s0, s1); cartR.visible = true; placeOnCurve(cartR, RS, lerp(0.35, 0.75, u)); trot(cartR, t, 1.8);
    const cp = cartR.position; setCam([cp.x + 4.5, cp.y + 3.0, cp.z + 7.0], [cp.x, cp.y + 1.2, cp.z - 2], 54, t, 0.012, -0.05);
    overlay = () => { speedLines2(t); popText('2× FASTER', W / 2, 1150, 120, '#ffd23e', t, wf(8, 'twice') - 0.05, s1 - 0.02); };
  }
  else if (li === 9) { // second month: brakes burned
    summer(t); cartR.visible = true; placeOnCurve(cartR, RS, 0.6); trot(cartR, t, 1.2); cartR.updateMatrixWorld(true);
    const wp = V(1.0, 0.55, -0.75); cartR.localToWorld(wp); brakeSmoke.forEach((s, i) => { s.visible = true; const q = ((t * 0.9 + i / brakeSmoke.length) % 1); s.position.set(wp.x + 0.3 + q * 0.6, wp.y + q * 1.6, wp.z - q * 0.8); const sc = 0.4 + q * 1.4; s.scale.set(sc, sc, 1); s.material.color.set(0x9a9a9a); s.material.opacity = 0.7 * Math.sin(q * Math.PI); });
    setCam([wp.x + 4.0, wp.y + 1.8, wp.z + 3.4], [wp.x - 0.8, wp.y + 0.8, wp.z + 0.5], 50, t, 0.005, 0.06);
    overlay = () => popText('BURNED BRAKES', W / 2, 270, 112, '#ff5a4a', t, wf(9, 'burned') - 0.05, s1 - 0.02);
  }
  else if (li === 10) { // the first ice of winter
    winter(t); const u = sub(s0, s1); setCam([lerp(20, 14, u), lerp(52, 46, u), lerp(-8, -4, u)], [-8, 16, -30], 54, t, 0, 0.0);
    overlay = () => snowfall(t, 100);
  }
  else if (li === 11) { // Rudolf loads his biggest cart and sends it straight down
    winter(t); const tsend = wf(11, 'sent') - 0.1, v = Math.max(0, t - tsend); const p0 = RS.getPointAt(0.03);
    cartR.visible = true; cartR.userData.horse.visible = false; placeOnCurve(cartR, RS, 0.03 + 0.012 * v * v);
    show(rudolf, p0.x + 0.2, p0.z - 1.8 + 0.6 * ss(tsend - 0.3, tsend + 0.2, t), 0); rudolf.g.position.y = hT(p0.x + 0.2, p0.z - 1.5); rudolf.g.updateMatrixWorld(true); rudolf.face(v > 0 ? 'happy' : 'neutral');
    rudolf.pose(v > 0.05 ? { rh: [0.4, 2.2, 0.9], lh: [-0.4, 2.2, 0.9], pitch: 0.25, lean: 0 } : { rh: [0.5, 2.6, 0.3], lh: [-0.5, 2.05, 0.05] });
    const cp = cartR.position; setCam([cp.x + 7.0, cp.y + 2.6, cp.z + 2.0], [cp.x - 0.3, cp.y + 2.0, cp.z - 1.4], 52, t, 0, -0.05);
    overlay = () => snowfall(t, 70);
  }
  else if (li === 12) { // explainer on the mountain: the steeper, the harder the pull
    winter(t); const u = sub(s0, s1), pulse = 1 + 0.08 * Math.sin(t * 8);
    aimArrow(arrowBig, RS.getPointAt(0.12).add(V(2.8, 2.5, 0)), RS.getPointAt(0.8).add(V(2.8, 2.5, 0)), pulse);
    arrowSmall.forEach((a, i) => { const j = 1 + i * 2, A = ZZ[j], B = ZZ[j + 1]; const pa = V(A[0], hT(A[0], A[1]) + 2.5, A[1]), pb = V(B[0], hT(B[0], B[1]) + 2.5, B[1]); aimArrow(a, pa.clone().lerp(pb, 0.15), pa.clone().lerp(pb, 0.85), 0.5 * pulse); });
    setCam([lerp(42, 38, u), lerp(44, 40, u), lerp(-24, -20, u)], [-6, 16, -30], 56, t, 0, 0.0);
    overlay = () => { snowfall(t, 40); popText('STEEP = STRONG PULL', W / 2, 260, 92, '#ff5a4a', t, wf(12, 'steeper') - 0.05, s1 - 0.02); };
  }
  else if (li === 13) { // a zigzag is the same mountain, cut into gentle slices
    winter(t); const u = sub(s0, s1), pulse = 1 + 0.08 * Math.sin(t * 8);
    arrowSmall.forEach((a, i) => { const j = 1 + i * 2, A = ZZ[j], B = ZZ[j + 1]; const pa = V(A[0], hT(A[0], A[1]) + 2.5, A[1]), pb = V(B[0], hT(B[0], B[1]) + 2.5, B[1]); aimArrow(a, pa.clone().lerp(pb, 0.15), pa.clone().lerp(pb, 0.85), 0.5 * pulse); });
    setCam([lerp(-4, -10, u), lerp(52, 46, u), lerp(-10, -6, u)], [-21, 14, -30], 52, t, 0, 0.0);
    overlay = () => { snowfall(t, 40); popText('GENTLE SLICES', W / 2, 260, 112, '#4be08a', t, wf(13, 'gentle') - 0.05, s1 - 0.02); };
  }
  else if (li === 14) { // stairs vs slide, with two kids in the square
    winter(t); const tS = wf(14, 'on') - 0.05, tL = wf(14, 'on', 2) - 0.05;
    play.updateMatrixWorld(true); const stepTop = V(-2.2, 2.6, 1.5), slTop = V(0.2, 2.9, 2.2), slBot = V(3.2, 0.2, 2.2);
    show(kidA, 0, 0, 0); kidA.g.scale.setScalar(SC * 0.55); const sa = play.localToWorld(V(-2.2, 1.0 + 0.4 * Math.floor(ss(tS, tS + 1.2, t) * 3), -0.6 + 0.6 * Math.floor(ss(tS, tS + 1.2, t) * 3))); kidA.g.position.copy(sa); kidA.g.rotation.y = play.rotation.y; kidA.face(t > tS + 1.0 ? 'happy' : 'neutral'); kidA.pose({ lh: [-0.5, 2.1, 0.3], rh: t > tS + 1.0 ? [0.6, 2.9, 0.2] : [0.5, 2.1, 0.3] });
    show(kidB, 0, 0, 0); kidB.g.scale.setScalar(SC * 0.55); const v = ss(tL, tL + 0.9, t); const sb = play.localToWorld(slTop.clone().lerp(slBot, v)); kidB.g.position.copy(sb); kidB.g.rotation.y = play.rotation.y + Math.PI / 2; kidB.face(t > tL ? 'shock' : 'happy'); kidB.pose({ lh: [-0.7, 2.6, 0.2], rh: [0.7, 2.6, 0.2], pitch: -0.3 * (v > 0 && v < 1 ? 1 : 0) });
    const c0 = play.localToWorld(V(0, 1.6, 1.0)); setCam([c0.x + 3.5, c0.y + 1.8, c0.z + 9.5], [c0.x, c0.y + 0.3, c0.z], 50, t, 0, 0.03);
    overlay = () => { snowfall(t, 40); popText('STAIRS: STOP', W / 2, 250, 112, '#4be08a', t, tS, tL - 0.02); popText("SLIDE: CAN'T", W / 2, 250, 112, '#ff5a4a', t, tL, s1 - 0.02); };
  }
  else if (li >= 15 && li <= 17) { // the slide down the ice and the crash
    winter(t); cartR.visible = true; cartR.userData.horse.visible = false; const tc = wf(17, 'went') - 0.25;
    const uMid = li === 15 ? lerp(0.45, 0.6, k) : (li === 16 ? lerp(0.6, 0.95, ss(0, 1, k)) : 0.95);
    if (li < 17 || t < tc) { placeOnCurve(cartR, RS, li === 17 ? lerp(0.95, 1.0, sub(s0, tc)) : uMid); cartR.userData.wheels.forEach(w => w.rotation.x = 0); cartR.rotation.z += li === 16 ? 0.12 * Math.sin(t * 6) : 0; }
    cartR.updateMatrixWorld(true); const wp = V(1.0, 0.55, -0.75); cartR.localToWorld(wp); const cp = cartR.position.clone();
    if (li === 15) { brakeSmoke.forEach((s, i) => { s.visible = true; const q = ((t * 1.2 + i / brakeSmoke.length) % 1); s.position.set(wp.x + 0.3 + q * 0.4, wp.y + q * 2.0, wp.z - q * 1.2); const sc = 0.5 + q * 2.2; s.scale.set(sc, sc, 1); s.material.color.set(0x8a8a8a); s.material.opacity = 0.75 * Math.sin(q * Math.PI); });
      setCam([wp.x + 4.2, wp.y + 2.0, wp.z + 3.8], [wp.x - 0.8, wp.y + 0.8, wp.z + 0.5], 50, t, 0.01, 0.06); overlay = () => { snowfall(t, 50); burst('SCREECH!', 760, 450, 160, t, s0 + 0.5, s1 - 0.03, 0.1); }; }
    else if (li === 16) { snowDust.forEach((s, i) => { s.visible = true; const q = ((t * 2.0 + i / snowDust.length) % 1); s.position.set(cp.x + (i % 2 ? 1 : -1) * (0.8 + q * 1.5), cp.y + 0.3 + q * 0.8, cp.z - 1.4 - q * 2.5); const sc = 0.6 + q * 1.8; s.scale.set(sc, sc, 1); s.material.opacity = 0.8 * (1 - q); });
      setCam([cp.x + 2.6, cp.y + 3.2, cp.z + 7.5], [cp.x, cp.y + 1.0, cp.z - 1], 56, t, 0.03, -0.06); overlay = () => { snowfall(t, 60); speedLines2(t); }; }
    else { const v = t - tc; if (v > 0) { const sh = ware.position.clone().add(V(0, 0, -1.2)); cartR.position.set(0, 0.05, lerp(5, sh.z + 1.5, cl(v / 0.25))); cartR.rotation.set(0, 0, v > 0.25 ? 0.4 * cl((v - 0.25) / 0.4) : 0); }
      const hitT = v - 0.25; wareDoors.forEach((d, i) => { if (hitT > 0) { d.visible = hitT < 1.5; d.rotation.y = (i ? 1 : -1) * (1.2 + hitT * 4); d.position.y = hitT * 2 - 4.9 * hitT * hitT * 0.4; } else d.rotation.y = 0; });
      if (hitT > 0) { const base = ware.position.clone(); ware.userData.barrels.forEach((b, i) => { b.visible = false; }); planks.forEach((p, i) => { p.visible = true; const a = i / planks.length * 6.28; p.position.copy(flyArc(base.clone().add(V(Math.cos(a) * 1.2, 2.2, 0)), V(Math.cos(a) * 5, 5 + (i % 3) * 2, 3 + (i % 4)), hitT)); p.rotation.set(hitT * (4 + i), hitT * 3, hitT * 2); });
        cartR.userData.barrels.forEach((b, i) => { const a = i * 2.4; b.parent === cartR || 0; }); }
      setCam([lerp(7, 9, sub(tc, s1)), lerp(3.2, 4.2, sub(tc, s1)), lerp(-2, -4, sub(tc, s1))], [0, 2.2, 8], 56, t, hitT > 0 ? 0.08 * Math.exp(-hitT * 3) : 0, 0.05);
      overlay = () => { snowfall(t, 40); if (hitT > 0 && hitT < 1.2) burst('CRASH!', 540, 420, 240, t, tc + 0.25, tc + 1.45, -0.06); };
      if (hitT > 0) flyingBarrels(hitT);
    }
  }
  else if (li === 18) { // Hans rolls in hours later, not a drop spilled
    winter(t); const u = sub(s0, s1); cartH.visible = true; placeOnCurve(cartH, RZ, lerp(0.94, 0.99, u)); trot(cartH, t, 0.4); seat(hans, cartH, 0.3); hans.face('happy');
    hans.pose({ rh: [0.35, 2.4, 0.55], lh: [-0.6, 2.4, 0.4] }); hold(hans, [0.35, 2.4, 0.55], mug, V(0, 0.1, 0.05)); mug.scale.setScalar(0.8); steamAt2(t, mug.position);
    const cp = cartH.position; setCam([cp.x + 3.8, cp.y + 4.2, cp.z - 7.0], [cp.x, cp.y + 2.3, cp.z], 52, t, 0, 0.03);
    overlay = () => { snowfall(t, 40); popText('3 HOURS LATER', W / 2, 250, 108, '#fff', t, s0 + 0.1, s1 - 0.02); popText('NOT A DROP SPILLED', W / 2, 1150, 92, '#4be08a', t, wf(18, 'not') - 0.05, s1 - 0.02); };
  }
  else { // callback: the road delivered his fortune in one morning
    winter(t); const u = sub(s0, s1); wareDoors.forEach(d => d.visible = false); ware.userData.barrels.forEach(b => b.visible = false); flyingBarrels(9, true);
    show(rudolf, 1.0, 6.2, 0.2); rudolf.face('sad'); rudolf.pose({ lh: [-0.5, 1.95, 0.05], rh: [0.5, 1.95, 0.05], bob: -0.05, hx: 0.2 }); hold(rudolf, [0.5, 1.95, 0.05], cane, V(0, 0.05, 0), [0.15, 0, 0.1]);
    if (u < 0.45) { const hp = rudolf.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 0.8, hp.y + 0.1, hp.z + 3.6], [hp.x, hp.y - 0.5, hp.z], 46, t, 0, -0.05); }
    else { const v = ss(0.45, 1, u); setCam([lerp(3, 6, v), lerp(3.5, 22, v), lerp(4, -6, v)], [0, lerp(2, 8, v), lerp(9, -20, v)], 54, t, 0, 0.0); }
    overlay = () => { snowfall(t, 40); popText('HIS WHOLE FORTUNE', W / 2, 250, 100, '#fff', t, wf(19, 'whole') - 0.1, DUR + 1); popText('ONE MORNING', W / 2, 390, 120, '#ffd23e', t, wf(19, 'one') - 0.05, DUR + 1); };
  }
}
function speedLines2(t) { ctx.save(); ctx.strokeStyle = 'rgba(255,255,255,0.45)'; ctx.lineCap = 'round'; for (let i = 0; i < 16; i++) { const a = i / 16 * 6.283 + 0.2, r0 = 300 + (i * 53) % 140, r1 = r0 + 300 + (t * 900 + i * 97) % 200; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(W / 2 + Math.cos(a) * r0, H * 0.45 + Math.sin(a) * r0); ctx.lineTo(W / 2 + Math.cos(a) * r1, H * 0.45 + Math.sin(a) * r1); ctx.stroke(); } ctx.restore(); }
// barrels bursting out of the warehouse (and lying broken afterwards)
const flyers = []; for (let i = 0; i < 16; i++) { const b = new THREE.Group(); root.add(b); M(cyl(0.38, 0.34, 0.85, 14), toon(0x8a5a34), { ol: 0.03, to: b }); for (const y of [-0.25, 0.25]) M(new THREE.TorusGeometry(0.39, 0.025, 6, 16), toon(0x2a2530), { p: [0, y, 0], r: [Math.PI / 2, 0, 0], to: b, cast: false }); b.visible = false; flyers.push(b); }
const hideAllF = hideAll; hideAll = function () { hideAllF(); flyers.forEach(b => b.visible = false); };
function flyingBarrels(tt, rest = false) { const base = ware.position.clone().add(V(0, 1.2, 1.5)); flyers.forEach((b, i) => { b.visible = true; const a = (i / flyers.length) * Math.PI * 2; const v = V(Math.cos(a) * (3 + (i % 3)), 4 + (i % 4) * 1.5, Math.sin(a) * (3 + (i % 3)) - 1.5); const p = flyArc(base, v, rest ? 3 : tt); b.position.copy(p); b.rotation.set(rest ? 1.57 : tt * (3 + i % 4), (i * 0.7), rest ? 0.3 * i : tt * 2); }); }

function steamAt2(t, p) { steamH.forEach((s, i) => { s.visible = true; const q = ((t * 0.5 + i / steamH.length) % 1); s.position.set(p.x + 0.08 * Math.sin(t * 2 + i), p.y + 0.15 + q * 0.7, p.z); s.scale.setScalar(0.15 + q * 0.35); s.material.opacity = 0.6 * Math.sin(q * Math.PI); }); }
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
