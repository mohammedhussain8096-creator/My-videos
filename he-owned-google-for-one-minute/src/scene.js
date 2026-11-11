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
let TM, Ls, DUR = 57;
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
// ===== The Man Who Owned Google for One Minute — cast, sets, timeline =====
const FT = []; function ftex(w, h, d) { const t = ctex(w, h, d); t.userData.draw = d; FT.push(t); return t; }
window.afterFonts = () => FT.forEach(t => { t.userData.draw(t.userData.g, t.userData.c.width, t.userData.c.height); t.needsUpdate = true; });

// ---------- cast ----------
const hairCap = (col, fringe = true) => hg => { const m = flat(col); M(sph(0.485, 32, 16, 0, 6.3, 0, Math.PI * 0.43), m, { ol: 0.035, p: [0, 0.04, -0.04], to: hg }); if (fringe) M(sph(0.2, 16, 10), m, { ol: 0.03, p: [-0.16, 0.36, 0.3], s: [1.5, 0.5, 0.8], r: [0, 0, 0.25], to: hg }); };
const sanmay = makeChar2({ skin: '#c98f66', leg: 0x2a3552, shoe: 0xf3efe6,
  body: (g, w, h) => { g.fillStyle = '#1f9c8f'; g.fillRect(0, 0, w, h); g.fillStyle = '#17786e'; g.fillRect(w * 0.36, h * 0.42, w * 0.28, h * 0.16); g.strokeStyle = '#f3efe6'; g.lineWidth = 6; for (const x of [0.46, 0.54]) { g.beginPath(); g.moveTo(w * x, 0); g.lineTo(w * x, h * 0.26); g.stroke(); g.fillStyle = '#f3efe6'; g.beginPath(); g.arc(w * x, h * 0.27, 7, 0, 7); g.fill(); } g.fillStyle = '#2a3552'; g.fillRect(0, h * 0.72, w, h * 0.28); },
  hat: hg => { hairCap(0x1b1522)(hg); const gm = flat(0x1b1522); for (const s of [-1, 1]) M(new THREE.TorusGeometry(0.115, 0.022, 8, 20), gm, { p: [s * 0.15, 0.03, 0.43], r: [0, s * 0.3, 0], to: hg, cast: false }); M(box(0.08, 0.025, 0.02), gm, { p: [0, 0.04, 0.46], to: hg, cast: false }); } });
const mkPerson = (shirt, pants, hair, skin, extra = {}) => makeChar2({ skin, leg: 0x1b1522, shoe: 0x3a2416, ...extra, body: (g, w, h) => { g.fillStyle = shirt; g.fillRect(0, 0, w, h); g.fillStyle = 'rgba(0,0,0,0.2)'; g.fillRect(w * 0.49, 0, w * 0.02, h * 0.7); g.fillStyle = pants; g.fillRect(0, h * 0.72, w, h * 0.28); if (extra.lanyard) { g.strokeStyle = '#ffd34d'; g.lineWidth = 6; g.beginPath(); g.moveTo(w * 0.42, 0); g.lineTo(w * 0.5, h * 0.36); g.lineTo(w * 0.58, 0); g.stroke(); g.fillStyle = '#f3efe6'; g.fillRect(w * 0.45, h * 0.36, w * 0.1, h * 0.12); } }, hat: hairCap(hair, !extra.bald) });
const sec = [mkPerson('#3b5bd9', '#2a2f45', 0x5a3a2a, '#f3c79c', { lanyard: true }), mkPerson('#e2553d', '#2a2f45', 0x1b1522, '#e9b78a', { lanyard: true, stache: true })];
const kids = [mkPerson('#f3efe6', '#2a4f8f', 0x1b1522, '#c98f66'), mkPerson('#f3efe6', '#2a4f8f', 0x3a2416, '#b97f58', { freckles: true }), mkPerson('#f3efe6', '#2a4f8f', 0x1b1522, '#d9a47a'), mkPerson('#f3efe6', '#2a4f8f', 0x1b1522, '#c98f66')];
const teacher = mkPerson('#d9468a', '#8a2a5a', 0x1b1522, '#c98f66');
const CAST = [sanmay, ...sec, ...kids, teacher]; CAST.forEach(c => root.add(c.g));

// ---------- bedroom / desk ----------
const room = new THREE.Group(); root.add(room);
const DESK = { x: 0.5, y: 1.55, z: -0.55 };
const winNight = flat(0x141c44), lidGlow = new THREE.PointLight(0x9fc4ff, 6, 6, 1.5), lampLight = new THREE.PointLight(0xffc98a, 9, 8, 1.5);
const laptop = new THREE.Group(), phone = new THREE.Group(), mug = new THREE.Group();
const phoneTex = ctex(256, 512, g => { }); const moon = M(sph(0.22), flat(0xfff4c2), { cast: false });
function drawPhone(k) { const g = phoneTex.userData.g; g.fillStyle = '#10131f'; g.fillRect(0, 0, 256, 512); g.fillStyle = '#8f98a8'; g.font = '34px Pop'; g.textAlign = 'center'; g.fillText('1:20', 128, 70); if (k > 0) { g.save(); g.translate(128, 230); g.scale(k, k); g.fillStyle = '#f3efe6'; g.beginPath(); g.roundRect(-112, -90, 224, 180, 22); g.fill(); g.fillStyle = '#2f8f5b'; g.beginPath(); g.arc(-70, -44, 22, 0, 7); g.fill(); g.fillStyle = '#fff'; g.font = '30px Pop'; g.fillText('$', -70, -33); g.fillStyle = '#1b1522'; g.font = '24px Pop'; g.textAlign = 'left'; g.fillText('YOUR CARD', -38, -36); g.textAlign = 'center'; g.fillStyle = '#d63b2f'; g.font = '52px Pop'; g.fillText('-$12.00', 0, 40); g.restore(); } phoneTex.needsUpdate = true; }
{
  M(box(9, 0.2, 7), toon(0xffffff, { map: TX.planks }), { p: [0, -0.1, 0.5], recv: true, to: room, cast: false });
  const wallT = paintTex('#2f5a66', { blot: 200, seed: 31 }); M(new THREE.PlaneGeometry(9, 5.8), toon(0xffffff, { map: wallT }), { p: [0, 2.9, -2.4], recv: true, to: room, cast: false });
  M(box(9, 0.3, 0.1), toon(0xf3efe6), { p: [0, 0.15, -2.35], to: room, cast: false });
  // window
  M(box(1.7, 2.0, 0.1), toon(0xf3efe6), { ol: 0.03, p: [-1.9, 3.5, -2.36], to: room }); M(box(1.46, 1.76, 0.12), winNight, { p: [-1.9, 3.5, -2.35], to: room, cast: false }); moon.position.set(-1.6, 4.0, -2.27); room.add(moon);
  for (let i = 0; i < 9; i++) M(box(0.12 + (i % 3) * 0.05, 0.3 + ((i * 7) % 5) * 0.14, 0.02), flat(0x0c1030), { p: [-2.55 + i * 0.16, 2.78 + ((i * 7) % 5) * 0.07, -2.27], to: room, cast: false });
  M(box(0.06, 1.76, 0.14), toon(0xf3efe6), { p: [-1.9, 3.5, -2.3], to: room, cast: false }); M(box(1.46, 0.06, 0.14), toon(0xf3efe6), { p: [-1.9, 3.5, -2.3], to: room, cast: false });
  // desk
  const wood = toon(0xffffff, { map: TX.planks }); M(box(3.2, 0.12, 1.4), wood, { ol: 0.03, p: [DESK.x, DESK.y, DESK.z], recv: true, to: room });
  for (const [dx, dz] of [[-1.5, -0.6], [1.5, -0.6], [-1.5, 0.6], [1.5, 0.6]]) M(box(0.12, DESK.y, 0.12), wood, { ol: 0.02, p: [DESK.x + dx, DESK.y / 2, DESK.z + dz], to: room });
  M(box(1.0, 0.9, 1.2), toon(0x8a5a36), { ol: 0.025, p: [DESK.x + 1.0, 1.0, DESK.z], to: room });
  // laptop (lid faces the camera, screen faces Sanmay)
  laptop.position.set(DESK.x, DESK.y + 0.07, DESK.z - 0.1); room.add(laptop);
  M(box(1.0, 0.05, 0.66), toon(0xb9bfca), { ol: 0.02, p: [0, 0, 0], to: laptop }); const lid = M(box(1.0, 0.5, 0.04), toon(0xb9bfca), { ol: 0.02, p: [0, 0.22, 0.42], r: [0.6, 0, 0], to: laptop }); M(cyl(0.07, 0.07, 0.01, 20), flat(0xf3efe6), { p: [0, 0.235, 0.445], r: [Math.PI / 2 + 0.6, 0, 0], to: laptop, cast: false });
  lidGlow.position.set(DESK.x, DESK.y + 0.6, DESK.z - 0.5); room.add(lidGlow);
  // lamp, mug, phone, books, clock, poster, plant
  const lamp = new THREE.Group(); lamp.position.set(DESK.x - 1.25, DESK.y + 0.06, DESK.z - 0.3); room.add(lamp); M(cyl(0.18, 0.2, 0.05, 16), toon(0x2a2530), { ol: 0.02, to: lamp }); M(cyl(0.025, 0.025, 0.8, 8), flat(0x1b1522), { p: [0.1, 0.4, 0], r: [0, 0, -0.25], to: lamp }); M(cyl(0.12, 0.26, 0.3, 16, true), toon(0xf2c230, { side: THREE.DoubleSide }), { ol: 0.02, p: [0.28, 0.8, 0], r: [0, 0, -0.7], to: lamp });
  lampLight.position.set(DESK.x - 0.8, DESK.y + 0.9, DESK.z + 0.3); room.add(lampLight);
  mug.position.set(DESK.x + 0.95, DESK.y + 0.17, DESK.z + 0.2); room.add(mug); M(cyl(0.11, 0.09, 0.22, 16), toon(0xe2553d), { ol: 0.02, to: mug }); M(new THREE.TorusGeometry(0.07, 0.02, 6, 12), toon(0xe2553d), { p: [0.13, 0, 0], to: mug });
  phone.position.set(DESK.x - 0.55, DESK.y + 0.075, DESK.z + 0.35); room.add(phone); M(box(0.3, 0.03, 0.56), toon(0x1b1522), { ol: 0.018, to: phone }); M(new THREE.PlaneGeometry(0.26, 0.52), flat(0xffffff, { map: phoneTex }), { p: [0, 0.017, 0], r: [-Math.PI / 2, 0, 0], to: phone, cast: false });
  M(box(2.2, 0.08, 0.4), wood, { ol: 0.025, p: [1.9, 3.6, -2.2], to: room }); [[0x3b5bd9, 0.5], [0xe2553d, 0.42], [0xf2c230, 0.55], [0x2f8f5b, 0.46], [0x7b4a9c, 0.5]].forEach(([c, h], i) => M(box(0.14, h, 0.3), toon(c), { ol: 0.02, p: [1.1 + i * 0.17, 3.64 + h / 2, -2.2], to: room }));
  M(cyl(0.16, 0.12, 0.24, 12), toon(0xb9773a), { ol: 0.02, p: [2.6, 3.76, -2.2], to: room }); for (let i = 0; i < 5; i++) M(sph(0.13, 10, 8), toon(0x2f8f5b), { ol: 0.02, p: [2.6 + Math.cos(i * 1.3) * 0.14, 4.02 + (i % 2) * 0.12, -2.2 + Math.sin(i * 1.3) * 0.1], to: room });
  const clockT = ctex(256, 256, g => { g.fillStyle = '#f3efe6'; g.beginPath(); g.arc(128, 128, 120, 0, 7); g.fill(); g.strokeStyle = '#1b1522'; g.lineWidth = 12; g.stroke(); g.lineCap = 'round'; g.lineWidth = 10; g.beginPath(); g.moveTo(128, 128); g.lineTo(162, 80); g.stroke(); g.lineWidth = 7; g.beginPath(); g.moveTo(128, 128); g.lineTo(196, 164); g.stroke(); for (let i = 0; i < 12; i++) { const a = i / 12 * 6.283; g.fillStyle = '#1b1522'; g.beginPath(); g.arc(128 + Math.cos(a) * 98, 128 + Math.sin(a) * 98, 5, 0, 7); g.fill(); } });
  M(new THREE.CircleGeometry(0.42, 32), flat(0xffffff, { map: clockT }), { p: [0.3, 4.35, -2.37], to: room, cast: false });
}
const key = new THREE.Group(), crown = new THREE.Group(), plane = new THREE.Group(); root.add(key); root.add(plane); sanmay.headG.add(crown);
{ const gm = flat(0xffd34d); M(new THREE.TorusGeometry(0.2, 0.06, 10, 24), gm, { ol: 0.03, p: [0, 0.75, 0], to: key }); M(cyl(0.05, 0.05, 0.9, 12), gm, { ol: 0.03, p: [0, 0.2, 0], to: key }); for (const y of [-0.05, -0.2]) M(box(0.2, 0.08, 0.07), gm, { ol: 0.03, p: [0.1, y, 0], to: key });
  M(cyl(0.34, 0.34, 0.16, 20, true), flat(0xffd34d, { side: THREE.DoubleSide }), { ol: 0.03, p: [0, 0.5, -0.02], to: crown }); for (let i = 0; i < 6; i++) { const a = i / 6 * 6.283; M(new THREE.ConeGeometry(0.09, 0.2, 4), flat(0xffd34d), { ol: 0.025, p: [Math.cos(a) * 0.32, 0.67, Math.sin(a) * 0.32 - 0.02], to: crown }); }
  const pm = flat(0xf3efe6, { side: THREE.DoubleSide }); const tri = (pts) => { const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pts.flat(), 3)); g.computeVertexNormals(); return g; };
  M(tri([[0.35, 0, 0], [-0.25, 0, 0.22], [-0.25, 0.02, 0]]), pm, { to: plane, cast: false }); M(tri([[0.35, 0, 0], [-0.25, 0, -0.22], [-0.25, 0.02, 0]]), pm, { to: plane, cast: false }); M(tri([[0.35, 0, 0], [-0.25, 0.02, 0], [-0.25, -0.14, 0]]), flat(0xd9d4c8, { side: THREE.DoubleSide }), { to: plane, cast: false }); }

// ---------- laptop screen as a full-frame UI ----------
const ui = new THREE.Group(); root.add(ui);
const uiTex = ctex(1080, 1920, g => { }); M(new THREE.PlaneGeometry(4.7, 8.36), flat(0xffffff, { map: uiTex }), { to: ui, cast: false });
function uiBase(g, title) { g.fillStyle = '#f4f6fb'; g.fillRect(0, 0, 1080, 1920); g.fillStyle = '#dfe4ee'; g.fillRect(0, 0, 1080, 150); g.fillStyle = '#fff'; g.beginPath(); g.roundRect(60, 40, 960, 72, 36); g.fill(); for (const [x, c] of [[110, '#e2553d'], [160, '#f2c230'], [210, '#2f8f5b']]) { g.fillStyle = c; g.beginPath(); g.arc(x - 20, 76, 12, 0, 7); g.fill(); } g.fillStyle = '#8f98a8'; g.font = '34px Pop'; g.textAlign = 'left'; g.textBaseline = 'middle'; g.fillText('domainshop.example/search', 250, 78); g.fillStyle = '#1b1522'; g.font = '86px Pop'; g.textAlign = 'center'; g.fillText(title, 540, 290); }
function uiSearchBox(g, text, caret) { g.fillStyle = '#fff'; g.strokeStyle = '#3b5bd9'; g.lineWidth = 8; g.beginPath(); g.roundRect(80, 400, 920, 150, 75); g.fill(); g.stroke(); g.fillStyle = '#1b1522'; g.font = '78px Pop'; g.textAlign = 'left'; g.textBaseline = 'middle'; g.fillText(text, 150, 480); if (caret) { const w = g.measureText(text).width; g.fillRect(158 + w, 436, 8, 88); } }
function uiCursor(g, x, y, down) { g.save(); g.translate(x, y); g.scale(down ? 0.86 : 1, down ? 0.86 : 1); g.fillStyle = '#1b1522'; g.strokeStyle = '#fff'; g.lineWidth = 8; g.lineJoin = 'round'; g.beginPath(); g.moveTo(0, 0); g.lineTo(0, 110); g.lineTo(28, 84); g.lineTo(50, 134); g.lineTo(74, 122); g.lineTo(52, 74); g.lineTo(88, 72); g.closePath(); g.stroke(); g.fill(); g.restore(); }
function drawUI(mode, o) {
  const g = uiTex.userData.g; g.setTransform(1, 0, 0, 1, 0, 0);
  if (mode === 'search' || mode === 'result' || mode === 'success' || mode === 'cancel') {
    uiBase(g, 'DOMAIN SHOP'); uiSearchBox(g, o.text, o.caret);
    if (mode === 'search') { g.textAlign = 'left'; g.font = '50px Pop'; [['pizzaparty.net', '$12'], ['catsincapes.org', '$9'], ['mondaysareok.com', '$12'], ['bestbananabread.com', '$15']].forEach(([n, p], i) => { g.fillStyle = '#b6bcc9'; g.fillText(n, 110, 700 + i * 130); g.textAlign = 'right'; g.fillText(p, 970, 700 + i * 130); g.textAlign = 'left'; g.fillStyle = '#e3e7ef'; g.fillRect(100, 760 + i * 130, 880, 4); }); }
    else { const a = back((o.card ?? 1)); g.save(); g.translate(540, 960); g.scale(a, a); g.fillStyle = '#fff'; g.shadowColor = 'rgba(30,40,80,0.25)'; g.shadowBlur = 40; g.beginPath(); g.roundRect(-460, -300, 920, 640, 40); g.fill(); g.shadowBlur = 0;
      g.fillStyle = '#1b1522'; g.font = '112px Pop'; g.textAlign = 'center'; g.fillText('google.com', 0, -170);
      if (mode === 'result') { const b = back(o.badge || 0); if (b > 0) { g.save(); g.translate(0, -20); g.scale(b, b); g.fillStyle = '#2fb36a'; g.beginPath(); g.roundRect(-250, -62, 500, 124, 62); g.fill(); g.fillStyle = '#fff'; g.font = '72px Pop'; g.fillText('AVAILABLE', 0, 6); g.restore(); }
        const p = back(o.price || 0); if (p > 0) { g.save(); g.translate(0, 190); g.scale(p, p); g.fillStyle = o.down ? '#2a47b3' : '#3b5bd9'; g.beginPath(); g.roundRect(-300, -84 + (o.down ? 8 : 0), 600, 168, 84); g.fill(); g.fillStyle = '#fff'; g.font = '92px Pop'; g.fillText('BUY  $12', 0, 8 + (o.down ? 8 : 0)); g.restore(); } }
      else if (mode === 'success') { g.fillStyle = '#2fb36a'; g.beginPath(); g.arc(0, 0, 90, 0, 7); g.fill(); g.strokeStyle = '#fff'; g.lineWidth = 22; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); g.moveTo(-42, 4); g.lineTo(-10, 38); g.lineTo(46, -32); g.stroke(); g.fillStyle = '#1b1522'; g.font = '64px Pop'; g.fillText('ORDER SUCCESSFUL', 0, 170); g.fillStyle = '#8f98a8'; g.font = '48px Pop'; g.fillText('You paid $12.00', 0, 250); }
      else { g.fillStyle = '#8f98a8'; g.font = '56px Pop'; g.fillText('Order #0012', 0, -20); g.fillText('Refunded: $12.00', 0, 80); const s = o.stamp || 0; if (s > 0) { const sc = 1 + 2.2 * (1 - cl(s / 0.18)); g.save(); g.translate(0, 40); g.rotate(-0.16); g.scale(sc, sc); g.globalAlpha = cl(s / 0.1); g.strokeStyle = '#d63b2f'; g.fillStyle = '#d63b2f'; g.lineWidth = 16; g.beginPath(); g.roundRect(-400, -105, 800, 210, 24); g.stroke(); g.font = '128px Pop'; g.fillText('CANCELLED', 0, 10); g.restore(); } }
      g.restore();
      if (mode === 'success') for (let i = 0; i < 40; i++) { const p = ((o.t * 0.5 + i * 0.137) % 1); g.fillStyle = ['#e2553d', '#f2c230', '#3b5bd9', '#2fb36a'][i % 4]; g.save(); g.translate((i * 277) % 1080, p * 1920); g.rotate(o.t * 4 + i); g.fillRect(-14, -7, 28, 14); g.restore(); } }
  } else if (mode === 'inbox') {
    g.fillStyle = '#f4f6fb'; g.fillRect(0, 0, 1080, 1920); g.fillStyle = '#3b5bd9'; g.fillRect(0, 0, 1080, 190); g.fillStyle = '#fff'; g.font = '84px Pop'; g.textAlign = 'left'; g.textBaseline = 'middle'; g.fillText('Inbox', 70, 100); const n = Math.floor(o.n); g.textAlign = 'right'; g.font = '60px Pop'; g.fillStyle = '#ffd34d'; g.fillText(n + ' new', 1010, 104);
    const subj = ['New owner: google.com', 'Message for the Google team', 'Webmaster alert', 'Site settings changed', 'Owner tools unlocked', 'Search report: google.com', 'Message for the Google team', 'Security notice', 'New owner: google.com', 'Webmaster alert', 'Site settings changed'];
    for (let i = 0; i < Math.min(n + 1, 11); i++) { const age = o.n - i, sl = i === n ? back(o.n % 1 / 0.5) : 1, y = 230 + (Math.min(n, 10) - i) * 152; if (i === n && n > 10) continue; g.save(); g.translate(1080 * (1 - sl), y); g.fillStyle = '#fff'; g.beginPath(); g.roundRect(40, 0, 1000, 136, 22); g.fill(); g.fillStyle = age < 2 ? '#e2553d' : '#c7cddb'; g.beginPath(); g.arc(100, 68, 18, 0, 7); g.fill(); g.textAlign = 'left'; g.fillStyle = '#1b1522'; g.font = '46px Pop'; g.fillText(subj[i % subj.length], 150, 46); g.fillStyle = '#8f98a8'; g.font = '36px Pop'; g.fillText('To: site owner', 150, 100); g.restore(); }
  }
  uiTex.needsUpdate = true;
}

// ---------- security room ----------
const secRoom = new THREE.Group(); root.add(secRoom); const alarm = M(sph(0.22), flat(0xff3b30), { ol: 0.03, cast: false });
{ M(box(9, 0.2, 7), toon(0x2a2f45), { p: [0, -0.1, 0.5], recv: true, to: secRoom, cast: false }); M(new THREE.PlaneGeometry(9, 5.8), toon(0x1c2440), { p: [0, 2.9, -2.4], to: secRoom, cast: false });
  const scr = (seed, col) => ctex(256, 160, g => { g.fillStyle = '#0c1030'; g.fillRect(0, 0, 256, 160); g.strokeStyle = col; g.lineWidth = 5; g.beginPath(); let sd = seed; for (let x = 0; x <= 256; x += 16) { sd = (sd * 16807) % 2147483647; const y = 40 + (sd / 2147483647) * 90; x ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke(); g.fillStyle = col; g.fillRect(12, 12, 90, 10); });
  [[-1.9, 3.5, '#4be08a', 5], [0, 3.8, '#6fc3ff', 9], [1.9, 3.5, '#ffd34d', 14]].forEach(([x, y, c, sd]) => { M(box(1.6, 1.05, 0.1), toon(0x10131f), { ol: 0.03, p: [x, y, -2.3], to: secRoom }); M(new THREE.PlaneGeometry(1.44, 0.9), flat(0xffffff, { map: scr(sd, c) }), { p: [x, y, -2.24], to: secRoom, cast: false }); });
  M(box(5.2, 0.14, 1.2), toon(0x3a4060), { ol: 0.03, p: [0, 1.5, -0.4], to: secRoom }); M(box(5.0, 1.45, 1.0), toon(0x2f3550), { p: [0, 0.72, -0.4], to: secRoom });
  alarm.position.set(0, 4.95, -2.2); secRoom.add(alarm); M(cyl(0.26, 0.3, 0.12, 16), toon(0x10131f), { p: [0, 5.15, -2.2], to: secRoom });
  const l = new THREE.PointLight(0x9fc4ff, 10, 10, 1.4); l.position.set(0, 3.2, 1.5); secRoom.add(l); }

// ---------- blue void props ----------
const voidG = new THREE.Group(); root.add(voidG); const bug = new THREE.Group(), coin = new THREE.Group(), glass = new THREE.Group(), cheque = new THREE.Group();
const chequeTex = ctex(1024, 460, g => { });
function drawCheque(amount) { const g = chequeTex.userData.g; g.fillStyle = '#fbf6e4'; g.fillRect(0, 0, 1024, 460); g.strokeStyle = '#2f8f5b'; g.lineWidth = 14; g.strokeRect(14, 14, 996, 432); g.fillStyle = '#2f8f5b'; g.font = '50px Pop'; g.textAlign = 'left'; g.textBaseline = 'middle'; g.fillText('BUG FINDER REWARD', 50, 76); g.fillStyle = '#8f98a8'; g.font = '36px Pop'; g.fillText('PAY TO', 50, 170); g.fillStyle = '#1b1522'; g.font = '62px Pop'; g.fillText('Sanmay', 50, 236); g.fillRect(50, 280, 420, 4); g.fillStyle = '#1b1522'; g.font = '124px Pop'; g.textAlign = 'right'; g.fillText(amount, 980, 350); chequeTex.needsUpdate = true; }
{ M(new THREE.PlaneGeometry(16, 26), flat(0x2b2aa8), { p: [0, 2, -3], to: voidG, cast: false });
  voidG.add(bug); M(sph(0.6, 28, 16, 0, 6.3, 0, Math.PI / 2), flat(0xe2372d), { ol: 0.045, s: [1, 0.75, 1.25], to: bug }); M(sph(0.3, 20, 14), flat(0x1b1522), { p: [0, 0.1, 0.72], to: bug }); M(box(0.03, 0.02, 1.45), flat(0x1b1522), { p: [0, 0.455, 0], to: bug, cast: false }); for (const [x, z] of [[0.28, 0.3], [-0.28, 0.3], [0.32, -0.25], [-0.32, -0.25], [0.12, -0.55], [-0.12, -0.55]]) M(sph(0.1, 10, 8), flat(0x1b1522), { p: [x, 0.36 - Math.abs(x) * 0.25, z], s: [1, 0.4, 1], to: bug, cast: false }); for (const s of [-1, 1]) for (const z of [-0.4, 0, 0.4]) M(cyl(0.025, 0.025, 0.5, 6), flat(0x1b1522), { p: [s * 0.72, 0.05, z], r: [0, 0, s * 1.1], to: bug, cast: false });
  voidG.add(coin); const ct = ctex(256, 256, g => { g.fillStyle = '#ffd34d'; g.fillRect(0, 0, 256, 256); g.strokeStyle = '#d9a53a'; g.lineWidth = 14; g.beginPath(); g.arc(128, 128, 100, 0, 7); g.stroke(); g.fillStyle = '#b3811f'; g.font = '150px Pop'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('$', 128, 138); }); FT.push(Object.assign(ct, {})); ct.userData.draw = g => { g.fillStyle = '#ffd34d'; g.fillRect(0, 0, 256, 256); g.strokeStyle = '#d9a53a'; g.lineWidth = 14; g.beginPath(); g.arc(128, 128, 100, 0, 7); g.stroke(); g.fillStyle = '#b3811f'; g.font = '150px Pop'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('$', 128, 138); };
  const cm = [flat(0xd9a53a), flat(0xffffff, { map: ct }), flat(0xffffff, { map: ct })]; M(cyl(0.8, 0.8, 0.14, 40), cm, { ol: 0.045, r: [Math.PI / 2, 0, 0], to: coin });
  voidG.add(glass); M(new THREE.TorusGeometry(0.95, 0.09, 10, 36), flat(0xf3efe6), { ol: 0.04, to: glass }); M(cyl(0.09, 0.09, 1.2, 10), flat(0x8a5a36), { ol: 0.04, p: [0.95, -1.15, 0], r: [0, 0, 0.7], to: glass }); M(new THREE.CircleGeometry(0.9, 32), flat(0xbfe3ff, { transparent: true, opacity: 0.28 }), { to: glass, cast: false });
  root.add(cheque); M(box(3.0, 1.35, 0.04), [flat(0xfbf6e4), flat(0xfbf6e4), flat(0xfbf6e4), flat(0xfbf6e4), flat(0xffffff, { map: chequeTex }), flat(0xfbf6e4)], { ol: 0.035, to: cheque }); }

// ---------- school ----------
const school = new THREE.Group(); root.add(school);
{ M(box(40, 0.2, 30), toon(0xffffff, { map: rep_(paintTex('#e2b877', { blot: 300, seed: 41 }), 8, 6) }), { p: [0, -0.1, -4], recv: true, to: school, cast: false });
  const wallT = paintTex('#f6e7c1', { blot: 160, seed: 43 }); M(box(8.4, 4.2, 3), toon(0xffffff, { map: wallT }), { ol: 0.04, p: [0, 2.1, -4.5], to: school }); M(box(9.0, 0.5, 3.6), toon(0xc9473a), { ol: 0.04, p: [0, 4.45, -4.5], to: school });
  M(box(1.3, 2.5, 0.12), toon(0x2a6f8f), { ol: 0.03, p: [0, 1.25, -2.96], to: school }); for (const x of [-2.6, 2.6]) { M(box(1.5, 1.3, 0.1), toon(0x3d2718), { ol: 0.03, p: [x, 2.4, -2.97], to: school }); M(box(1.3, 1.1, 0.12), flat(0x8fd0ff), { p: [x, 2.4, -2.96], to: school, cast: false }); }
  const st = ftex(512, 128, g => { g.fillStyle = '#2a6f8f'; g.fillRect(0, 0, 512, 128); g.fillStyle = '#fff'; g.font = '92px Pop'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('SCHOOL', 256, 70); }); M(box(3.0, 0.75, 0.1), toon(0xffffff, { map: st }), { ol: 0.03, p: [0, 3.5, -2.95], to: school });
  for (let i = 0; i < 13; i++) { const x = -4.2 + i * 0.7; M(new THREE.ConeGeometry(0.2, 0.36, 3), flat([0xe2553d, 0xf2c230, 0x3b5bd9, 0x2fb36a][i % 4]), { p: [x, 4.95 - Math.sin(i / 12 * Math.PI) * 0.45, -2.6], r: [Math.PI, 0, 0], s: [1, 1, 0.2], to: school, cast: false }); }
  for (const x of [-6.2, 6.4]) { M(cyl(0.22, 0.28, 2.4, 10), toon(0x7a5232), { ol: 0.03, p: [x, 1.2, -5], to: school }); for (let i = 0; i < 5; i++) M(sph(1.0, 12, 10), toon(0x4f9f4a), { ol: 0.04, p: [x + Math.cos(i * 1.3) * 0.8, 3.2 + (i % 2) * 0.6, -5 + Math.sin(i * 1.3) * 0.5], to: school }); }
  for (const [x, z, s] of [[-12, -22, 7], [6, -24, 9], [16, -20, 6]]) M(sph(s, 20, 12), flat(0x9fcf7a), { p: [x, -s * 0.5, z], s: [1.8, 1, 1], to: school, cast: false }); }
const SETS = [room, ui, secRoom, voidG, school, key, plane, cheque, ...CAST.map(c => c.g)];
function hideAll() { SETS.forEach(g => g.visible = false); crown.visible = false; bug.visible = coin.visible = glass.visible = false; }
function roomLook(night = true) { room.visible = true; if (night) { bg(0x10162e); light(0.5, 0.55, [-3, 6, 6], 0xbfd0ff, 0x2a3350); winNight.color.set(0x141c44); moon.visible = true; lidGlow.intensity = 6; lampLight.intensity = 9; LOOK.grade = ['#5a7ad0', 0.14]; LOOK.bloom = 0.22; } else { bg(0xffc98a); light(0.95, 1.4, [-5, 6, 4], 0xffe2bd, 0x6a5a50); winNight.color.set(0xffb86b); moon.visible = false; lidGlow.intensity = 2; lampLight.intensity = 0; LOOK.grade = ['#ffb060', 0.2]; LOOK.bloom = 0.25; } }
const NIGHT = 0xd6e2ff;
const SIT = 0.42;
function atDesk(t, face, pose = {}, tint = NIGHT) { show(sanmay, DESK.x, DESK.z - 1.15, 0, tint); sanmay.g.position.y = SIT; sanmay.g.updateMatrixWorld(true); sanmay.face(face); sanmay.pose({ lh: [-0.3, 1.45, 0.8], rh: [0.3, 1.45, 0.8], bob: 0.012 * Math.sin(t * 3), ...pose }); }
function uiLook(t, zoom = 1, cx = 0, cy = 0, roll = 0) { ui.visible = true; bg(0x10131f); LOOK.grade = null; LOOK.bloom = 0.12; setCam([cx + 0.12 * Math.sin(t * 0.7), cy, 10.9 / zoom], [cx, cy, 0], 42, t, 0, roll); }
function tile(x, y, w, h, ch, flip, hot) { const sy = Math.abs(Math.cos(flip * Math.PI)); ctx.save(); ctx.translate(x, y); ctx.scale(1 + 0.12 * hot, (1 + 0.12 * hot) * Math.max(0.02, sy)); ctx.fillStyle = INK; ctx.beginPath(); ctx.roundRect(-w / 2 - 8, -h / 2 - 8, w + 16, h + 16, 26); ctx.fill(); ctx.fillStyle = hot > 0.5 ? '#ffd23e' : '#f3efe6'; ctx.beginPath(); ctx.roundRect(-w / 2, -h / 2, w, h, 20); ctx.fill(); ctx.fillStyle = 'rgba(0,0,0,0.12)'; ctx.fillRect(-w / 2, -3, w, 6); ctx.fillStyle = INK; ctx.font = `${h * 0.74}px Pop`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(ch, 0, 8); ctx.restore(); }
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
  LOOK.grade = ['#ffc98a', 0.1]; LOOK.bloom = 0.14; drawPhone(0);

  if (li === 0) { // HOOK
    const tb = wf(0, 'belonged') - 0.08;
    if (t < tb) { roomLook(); atDesk(t, t > 0.9 ? 'shock' : 'neutral', { hx: 0.05 });
      const hp = sanmay.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + lerp(0.9, 0.4, k * 2), hp.y + 0.1, hp.z + lerp(5.2, 3.9, ss(0, 1, k * 2))], [hp.x, hp.y - 0.3, hp.z], 42, t, 0, -0.05);
      overlay = () => { popText('ONE MINUTE', W / 2, 270, 136, '#ffd23e', t, 0.3, tb - 0.02); };
    } else { drawUI('result', { text: 'google.com', badge: 1, price: sub(tb + 0.2, tb + 0.5), card: 1 }); uiLook(t, lerp(1.0, 1.25, sub(tb, s1)), 0, -0.2, 0.03);
      
    }
  }
  else if (li === 1) { // 2015, ex-Googler, browsing late at night
    const tb = wf(1, 'sanmay') - 0.08, tc = wf(1, 'and') - 0.08; roomLook();
    if (t < tb) { atDesk(t, 'neutral'); setCam([lerp(-1.6, -0.6, k * 3), lerp(3.2, 2.6, k * 3), lerp(8.6, 7.6, k * 3)], [0.2, 2.3, -1.2], 46, t, 0, 0.03);
      overlay = () => popText('2015', W / 2, 290, 180, '#ffd23e', t, wf(1, '2015') - 0.08, tb - 0.02);
    } else if (t < tc) { atDesk(t, 'happy', { rh: [0.55, 2.5 + 0.06 * Math.sin(t * 9), 0.3], hz: 0.06 });
      const hp = sanmay.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x - 0.5, hp.y + 0.1, hp.z + lerp(4.8, 4.2, sub(tb, tc))], [hp.x, hp.y - 0.35, hp.z], 42, t, 0, 0.05);
      overlay = () => { popText('SANMAY', W / 2, 250, 136, '#fff', t, tb + 0.05, tc - 0.02); popText('EX-GOOGLER', W / 2, 395, 112, '#ffd23e', t, wf(1, 'used') - 0.05, tc - 0.02); };
    } else { const u = sub(tc, s1); atDesk(t, 'neutral', { lh: [-0.3, 1.45 + 0.04 * Math.sin(t * 16), 0.8], rh: [0.3, 1.45 + 0.04 * Math.cos(t * 13), 0.8], hx: 0.12 });
      setCam([lerp(1.8, 1.2, u), lerp(3.6, 3.0, u), lerp(6.6, 5.4, u)], [0.2, 2.3, -1.2], 46, t, 0, -0.04);
      overlay = () => { popText('1:20 AM', W / 2, 250, 124, '#fff', t, wf(1, 'late') - 0.05, s1 - 0.02); popText('JUST FOR FUN', W / 2, 395, 108, '#ffd23e', t, wf(1, 'just') - 0.05, s1 - 0.02); };
    }
  }
  else if (li === 2) { // typing google.com
    const tg = wf(2, 'google') - 0.5, word = 'google.com', n = Math.floor(cl((t - tg) / 1.3) * word.length + 0.001);
    drawUI('search', { text: word.slice(0, n), caret: Math.floor(t * 3) % 2 === 0 || n < word.length }); uiLook(t, lerp(1.0, 1.5, ss(0, 1, sub(tg - 0.3, s1))), 0, lerp(0, 1.9, ss(0, 1, sub(tg - 0.3, s1))), -0.03);
    overlay = () => popText('THE BIGGEST ONE', W / 2, 1180, 100, '#ffd23e', t, wf(2, 'biggest') - 0.05, tg);
  }
  else if (li === 3) { // available, $12
    const ta = wf(3, 'available') - 0.1, tp = wf(3, 'twelve') - 0.1;
    drawUI('result', { text: 'google.com', card: sub(s0, s0 + 0.3), badge: sub(ta, ta + 0.3), price: sub(tp, tp + 0.3) }); uiLook(t, lerp(1.05, 1.35, k), 0, lerp(0.2, -0.3, k), 0.03);
    overlay = () => { if (t > ta && t < ta + 0.5) { ctx.fillStyle = `rgba(255,255,255,${0.35 * (1 - (t - ta) / 0.5)})`; ctx.fillRect(0, 0, W, H); } };
  }
  else if (li === 4) { // glitch? buys anyway
    const tb = wf(4, 'he') - 0.08;
    if (t < tb) { roomLook(); atDesk(t, 'think', { rh: [0.2, 2.3, 0.44], hz: 0.1 * Math.sin(t * 2.5) });
      const hp = sanmay.headG.getWorldPosition(V(0, 0, 0)); setCam([hp.x + 0.5, hp.y + 0.1, hp.z + lerp(4.2, 3.7, sub(s0, tb))], [hp.x, hp.y - 0.3, hp.z], 42, t, 0, 0.06);
      overlay = () => { popText('A GLITCH?', W / 2, 290, 140, '#fff', t, wf(4, 'glitch') - 0.3, tb - 0.02, { rot: -0.04 }); };
    } else { const tc = wf(4, 'buy') - 0.05, u = sub(tb, tc), done = t > tc + 0.45;
      if (!done) { drawUI('result', { text: 'google.com', badge: 1, price: 1, down: t > tc && t < tc + 0.2 }); const g = uiTex.userData.g; uiCursor(g, lerp(900, 640, ss(0, 1, u)), lerp(1500, 1170, ss(0, 1, u)), t > tc && t < tc + 0.2); uiTex.needsUpdate = true; }
      else drawUI('success', { text: 'google.com', t });
      uiLook(t, lerp(1.2, 1.45, sub(tb, s1)), 0, -0.6, -0.03);
      overlay = () => { if (t > tc && t < tc + 0.35) burst('CLICK!', 780, 1250, 150, t, tc, tc + 0.35, 0.1); };
    }
  }
  else if (li === 5) { // card charged, inbox floods
    const tb = wf(5, 'his', 2) - 0.08;
    if (t < tb) { roomLook(); atDesk(t, 'shock'); const pk = back(sub(s0 + 0.25, s0 + 0.5)); drawPhone(pk); phone.position.x = DESK.x - 0.55 + (pk > 0.1 ? 0.012 * Math.sin(t * 90) * (1 - sub(s0 + 0.5, s0 + 1.1)) : 0);
      setCam([DESK.x - 0.5, DESK.y + lerp(1.7, 1.25, sub(s0, tb)), DESK.z + 0.75], [DESK.x - 0.55, DESK.y, DESK.z + 0.33], 40, t, 0, 0.06); LOOK.dof = null;
      overlay = () => { burst('BZZT!', 800, 520, 150, t, s0 + 0.3, s0 + 0.9, 0.1); popText('CHARGED', W / 2, 290, 150, '#ff5a4a', t, wf(5, 'charged') - 0.05, tb - 0.02); };
    } else { const n = sub(tb + 0.1, s1 - 0.3) * 14; drawUI('inbox', { n }); uiLook(t, 1.02, 0, 0, 0.03);
      overlay = () => { popText("GOOGLE'S OWN", W / 2, 1050, 112, '#fff', t, wf(5, 'google') - 0.3, s1 - 0.02); popText('MAIL', W / 2, 1190, 150, '#ffd23e', t, wf(5, 'google') - 0.05, s1 - 0.02); };
    }
  }
  else if (li === 6 || li === 7 && t < wf(7, 'order') - 0.1) { // sixty seconds as king
    roomLook(); const t0 = CUT(6), tEnd = wf(7, 'order') - 0.1, u = cl((t - t0) / (tEnd - t0));
    atDesk(t, li === 6 ? 'happy' : 'shock', li === 6 ? { rh: [0.62, 2.9 + 0.05 * Math.sin(t * 7), 0.2], lh: [-0.5, 1.5, 0.6], bob: 0.03 * Math.abs(Math.sin(t * 6)) } : { rh: [0.62, 2.3, 0.2], lh: [-0.5, 1.5, 0.6] });
    crown.visible = li === 6 || t < wf(7, 'one') + 0.2; if (li === 7) { const v = t - CUT(7); crown.position.y = -v * v * 3; crown.rotation.z = v * 2; } else { crown.position.y = 0; crown.rotation.z = 0.12; }
    key.visible = true; const hp = V(0.62, li === 6 ? 2.9 + 0.05 * Math.sin(t * 7) : 2.3, 0.2); sanmay.g.updateMatrixWorld(true); sanmay.up.localToWorld(hp); key.position.copy(hp).add(V(0, 0.15, 0)); key.rotation.set(0, t * 2, 0.15);
    const hd = sanmay.headG.getWorldPosition(V(0, 0, 0)); setCam([hd.x + lerp(-0.6, 0.3, u), hd.y - 0.3, hd.z + lerp(6.4, 5.4, u)], [hd.x + 0.15, hd.y + 0.2, hd.z], 44, t, 0, lerp(-0.07, 0.04, u));
    overlay = () => { const secs = Math.max(0, Math.ceil(60 * (1 - u * 1.02))); const txt = '0:' + String(secs).padStart(2, '0'); ctx.save(); ctx.translate(W / 2, 300); const pul = 1 + 0.04 * Math.sin(t * 20); ctx.scale(pul, pul); ctx.fillStyle = INK; ctx.beginPath(); ctx.roundRect(-250, -110, 500, 220, 30); ctx.fill(); ctx.fillStyle = secs <= 10 ? '#ff5a4a' : '#ffd23e'; ctx.font = '170px Pop'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(txt, 0, 12); ctx.restore();
      if (li === 6) popText('THE KEYS', W / 2, 1090, 124, '#ffd23e', t, wf(6, 'keys') - 0.05, CUT(7) - 0.02); };
  }
  else if (li === 7) { // order cancelled
    const tcn = wf(7, 'order') - 0.1; drawUI('cancel', { text: 'google.com', stamp: t - (wf(7, 'cancelled') - 0.05) }); uiLook(t, lerp(1.1, 1.3, sub(tcn, s1)), 0, -0.5, 0.03 + (t > wf(7, 'cancelled') - 0.05 ? 0.02 * Math.exp(-(t - wf(7, 'cancelled')) * 8) * Math.sin(t * 60) : 0));
  }
  else if (li === 8) { // he reported it
    const tb = wf(8, 'he', 2) - 0.08, tc = wf(8, 'exactly') - 0.2;
    if (t < tc) { roomLook(); const typing = t > tb; atDesk(t, typing ? 'happy' : 'neutral', typing ? { lh: [-0.3, 1.45 + 0.05 * Math.sin(t * 22), 0.8], rh: [0.3, 1.45 + 0.05 * Math.cos(t * 19), 0.8], hx: 0.1 } : { hy: 0.45 * Math.sin((t - s0) * 6), lh: [-0.6, 2.0, 0.3], rh: [0.6, 2.0, 0.3] });
      const v = sub(tb + 0.9, tc + 0.3); if (t > tb + 0.9) { plane.visible = true; plane.position.set(lerp(DESK.x, -1.9, v), lerp(DESK.y + 0.8, 3.6, v) + Math.sin(v * Math.PI) * 0.6, lerp(DESK.z, -2.2, v)); plane.rotation.set(0, Math.PI - 0.5, 0.4 - v * 0.6); plane.scale.setScalar(1.3 - v * 0.6); }
      setCam([lerp(0.6, 0.0, k), 2.5, lerp(6.6, 6.0, k)], [0.1, 2.4, -1.2], 46, t, 0, 0.04);
      overlay = () => { popText("DIDN'T HIDE IT", W / 2, 280, 112, '#fff', t, s0 + 0.15, tb - 0.02); popText('TOLD GOOGLE', W / 2, 280, 124, '#ffd23e', t, wf(8, 'told') - 0.05, tc - 0.02); };
    } else { secRoom.visible = true; bg(0x10131f); const calm = ss(tc + 0.5, tc + 0.9, t); light(0.6, 0.6, [0, 6, 6], 0xbfd0ff, 0x2a3350); alarm.material.color.set(calm > 0.5 ? 0x2fb36a : (Math.floor(t * 8) % 2 ? 0xff3b30 : 0x8a1a14)); LOOK.grade = [calm > 0.5 ? '#4be08a' : '#ff3b30', 0.16]; LOOK.bloom = 0.25;
      sec.forEach((c, i) => { show(c, i ? 1.0 : -1.0, -1.5, i ? -0.25 : 0.25, NIGHT); c.face(calm > 0.5 ? 'happy' : 'shock'); c.pose(calm > 0.5 ? { lh: [-0.44, 1.5, 0.3], rh: [0.44, 1.5, 0.3], bob: -0.04 } : { lh: [-0.6, 2.7, 0.2], rh: [0.6, 2.7, 0.2], bob: 0.03 * Math.sin(t * 25 + i) }); });
      setCam([0.2, 2.5, lerp(7.4, 6.8, sub(tc, s1))], [0, 2.7, -1.5], 46, t, calm > 0.5 ? 0 : 0.01, -0.04);
      overlay = () => { burst('ALERT!', 300, 520, 170, t, tc + 0.05, tc + 0.5, -0.1); popText('PHEW', W / 2, 330, 150, '#4be08a', t, tc + 0.9, s1 - 0.02); };
    }
  }
  else if (li === 9) { // bug bounty explainer
    voidG.visible = true; bg(0x2b2aa8); light(1.2, 1.4, [3, 5, 8], 0xffffff, 0x5a5ac0); LOOK.grade = null; LOOK.bloom = 0.12;
    const tp = wf(9, 'pays') - 0.1, v = sub(tp, tp + 0.5), isCoin = v > 0.5;
    bug.visible = !isCoin; coin.visible = isCoin; glass.visible = t < tp + 0.3;
    bug.position.set(0.25 * Math.sin(t * 3), 2.2, 0); bug.rotation.set(1.1, 0, 0.2 * Math.sin(t * 5)); bug.scale.setScalar(1.5 * (1 - 0.9 * cl(v * 2)));
    coin.position.set(0, 2.3 + 0.15 * Math.sin(t * 4), 0); coin.rotation.set(0, t * 4, 0); coin.scale.setScalar(1.6 * back((v - 0.5) * 2));
    const gk = sub(s0 + 0.3, s0 + 1.0); glass.position.set(lerp(3.5, 0.2, ss(0, 1, gk)), lerp(4.5, 2.4, ss(0, 1, gk)), 1.2); glass.scale.setScalar(1.6);
    setCam([lerp(0.6, 0, k), 2.6, lerp(11, 9.5, k)], [0, 2.4, 0], 42, t, 0, 0.03);
    overlay = () => { popText('FIND A MISTAKE', W / 2, 260, 104, '#fff', t, s0 + 0.5, s1 - 0.02); popText('GET PAID', W / 2, 400, 150, '#ffd23e', t, tp, s1 - 0.02); };
  }
  else if (li === 10 || li === 11) { // the cheque, and what the number spells
    voidG.visible = true; bg(0x2b2aa8); light(1.2, 1.4, [3, 5, 8], 0xffffff, 0x5a5ac0); LOOK.grade = null; LOOK.bloom = 0.12;
    cheque.visible = true; drawCheque('$6,006.13'); const inn = back(sub(wf(10, 'six') - 0.4, wf(10, 'six') - 0.1));
    cheque.position.set(0, li === 10 ? 2.4 : lerp(2.4, 4.3, ss(0, 0.5, k * 3)), 0); cheque.rotation.set(0, 0.25 * Math.sin(t * 1.3), 0.05 * Math.sin(t * 2)); cheque.scale.setScalar((li === 10 ? 1.25 : lerp(1.25, 0.95, ss(0, 0.5, k * 3))) * Math.max(0.001, inn));
    setCam([0, 2.5, 10.5], [0, 2.4, 0], 42, t, 0, li === 10 ? -0.03 : 0.02);
    if (li === 10) overlay = () => { popText('HIS REWARD', W / 2, 280, 124, '#fff', t, s0 + 0.1, s1 - 0.02); };
    else { const ts = [wf(11, 'six'), wf(11, 'zero'), wf(11, 'zero', 2), wf(11, 'six', 2), wf(11, 'one'), wf(11, 'three')], tf = wf(11, 'it') - 0.1, dig = '600613', let_ = 'GOOGLE';
      overlay = () => { for (let i = 0; i < 6; i++) { const ap = back((t - (s0 + 0.25 + i * 0.05)) / 0.2); if (ap <= 0) continue; const fl = cl((t - tf - i * 0.09) / 0.3), hot = t < tf ? cl(1 - Math.abs(t - ts[i] - 0.15) / 0.3) : (fl >= 1 ? 0.6 + 0.4 * Math.sin(t * 6 + i) : 0); ctx.save(); ctx.translate(0, (1 - ap) * 200); tile(128 + i * 165, 1120, 148, 210, fl < 0.5 ? dig[i] : let_[i], fl, t < tf ? hot : (fl >= 1 ? 1 : 0)); ctx.restore(); }
        popText('LOOK CLOSELY', W / 2, 760, 96, '#fff', t, s0 + 0.1, tf - 0.02); popText('IT SPELLS GOOGLE', W / 2, 760, 96, '#ffd23e', t, tf, s1 - 0.02); };
    }
  }
  else if (li === 12 || li === 13) { // the school; Google doubles it
    school.visible = true; bg(0x8fd0ff); light(1.05, 1.7, [5, 9, 7], 0xfff6e0, 0x8a7a5a); LOOK.grade = ['#ffd27a', 0.14]; LOOK.bloom = 0.2;
    const dbl = li === 13, v = dbl ? sub(s0 + 0.25, s0 + 0.85) : 0, amt = 6006.13 * (1 + ss(0, 1, v));
    drawCheque('$' + amt.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }));
    show(sanmay, -0.95, 0.4, 0.2); sanmay.face('happy'); show(teacher, 0.95, 0.4, -0.2); teacher.face('happy');
    const cy = 1.75 + (dbl ? 0.15 * Math.sin(v * Math.PI) : 0); sanmay.pose({ rh: [0.5, 1.7, 0.6], lh: [-0.44, 1.42, 0.05], bob: 0.03 * Math.abs(Math.sin(t * 5)) }); teacher.pose({ lh: [-0.5, 1.7, 0.6], rh: [0.44, 1.42, 0.05], bob: 0.03 * Math.abs(Math.cos(t * 5)) });
    cheque.visible = true; cheque.position.set(0, cy - 0.35, 1.0); cheque.rotation.set(0, 0, 0.03 * Math.sin(t * 3)); cheque.scale.setScalar(dbl ? 0.6 + 0.08 * Math.sin(v * Math.PI) : 0.6);
    kids.forEach((c, i) => { show(c, [-2.3, -1.55, 1.6, 2.35][i], 1.3 + (i % 2) * 0.5, [0.4, 0.25, -0.25, -0.4][i]); c.g.scale.setScalar(0.5); c.face('happy'); const j = Math.abs(Math.sin(t * (dbl ? 9 : 6) + i * 1.3)) * (dbl ? 0.5 : 0.28); c.g.position.y = j; c.pose({ lh: [-0.6, 2.6, 0.1], rh: [0.6, 2.6, 0.1] }); });
    if (!dbl) setCam([lerp(1.6, 0.4, ss(0, 1, k)), lerp(4.0, 2.2, ss(0, 1, k)), lerp(12, 8.4, ss(0, 1, k))], [0, 2.2, -0.5], 46, t, 0, 0.03);
    else setCam([0.1, 1.9, lerp(7.2, 6.4, k)], [0, 1.85, 0.8], 44, t, 0.006 * Math.sin(v * Math.PI), -0.03);
    overlay = () => { if (!dbl) { popText('EVERY CENT', W / 2, 250, 124, '#fff', t, wf(12, 'every') - 0.05, s1 - 0.02); popText('TO SCHOOLS', W / 2, 395, 124, '#ffd23e', t, wf(12, 'schools') - 0.05, s1 - 0.02); } else { burst('DOUBLED!', 540, 330, 200, t, wf(13, 'doubled') - 0.1, s1 - 0.02, -0.06); } };
  }
  else { // ending: sunrise at the desk
    roomLook(false); const tb = wf(14, 'and') - 0.08; show(sanmay, DESK.x, DESK.z - 1.15, 0); sanmay.g.position.y = SIT; sanmay.g.updateMatrixWorld(true); sanmay.face('happy');
    sanmay.pose(t < tb ? { lh: [-0.3, 1.45, 0.8], rh: [0.4, 2.2, 0.5], bob: 0.02 * Math.sin(t * 3) } : { lh: [-0.75, 2.9, 0.1], rh: [0.75, 2.9, 0.1], hx: -0.25, bob: 0.04 * Math.abs(Math.sin(t * 4)) });
    setCam([lerp(-1.2, 0.2, ss(0, 1, k)), lerp(3.1, 2.8, k), lerp(8.4, 6.4, ss(0, 1, k))], [0.3, 2.7, -1.2], 46, t, 0, 0.03);
    overlay = () => { popText('1 MINUTE', W / 2, 250, 130, '#fff', t, s0 + 0.1, tb - 0.02); popText('$12', W / 2, 410, 170, '#ffd23e', t, wf(14, 'twelve') - 0.05, tb - 0.02); popText('BEST MISTAKE', W / 2, 250, 120, '#fff', t, wf(14, 'best') - 0.05, DUR + 1); popText('EVER MADE', W / 2, 395, 130, '#4be08a', t, wf(14, 'ever') - 0.05, DUR + 1); };
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
