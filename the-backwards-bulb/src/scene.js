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
const outlineMat = th => new THREE.ShaderMaterial({
  side: THREE.BackSide, uniforms: { th: { value: th } },
  vertexShader: 'uniform float th; void main(){ gl_Position = projectionMatrix*modelViewMatrix*vec4(position+normal*th,1.0); }',
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

// ---------- bulb ----------
class Helix extends THREE.Curve { constructor(r, h, n) { super(); this.r = r; this.h = h; this.n = n; } getPoint(t) { const a = t * this.n * Math.PI * 2; return V(Math.cos(a) * this.r, -t * this.h, Math.sin(a) * this.r); } }
const glowTex = ctex(256, 256, (g) => { const r = g.createRadialGradient(128, 128, 0, 128, 128, 128); r.addColorStop(0, 'rgba(255,236,150,0.95)'); r.addColorStop(0.35, 'rgba(255,200,80,0.35)'); r.addColorStop(1, 'rgba(255,180,60,0)'); g.fillStyle = r; g.fillRect(0, 0, 256, 256); });
function makeBulb() { // origin = top of screw base; glass hangs toward -y
  const b = { g: new THREE.Group() }, brass = toon(0xd9a53a);
  M(cyl(0.085, 0.1, 0.2, 20), brass, { ol: 0.018, p: [0, -0.1, 0], to: b.g });
  M(new THREE.TubeGeometry(new Helix(0.1, 0.17, 3.5), 80, 0.022, 6), toon(0xf2cf63), { ol: 0.012, p: [0, -0.015, 0], to: b.g });
  M(cyl(0.04, 0.06, 0.05, 12), toon(0x2a2530), { p: [0, 0.02, 0], to: b.g });
  b.glassOn = flat(0xffe98a); b.glassOff = toon(0xaab7c9);
  b.glass = M(sph(0.24, 32, 24), b.glassOn, { ol: 0.022, p: [0, -0.46, 0], s: [1, 1.12, 1], to: b.g });
  b.neck = M(cyl(0.1, 0.15, 0.16, 20), b.glassOn, { p: [0, -0.26, 0], to: b.g, cast: false });
  b.fil = M(new THREE.TorusGeometry(0.07, 0.012, 6, 16, Math.PI), flat(0xff8a1f), { p: [0, -0.5, 0], to: b.g, cast: false });
  b.glow = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true }));
  b.glow.position.set(0, -0.46, 0); b.glow.scale.set(1.5, 1.5, 1); b.g.add(b.glow);
  b.lit = (k) => { const on = k > 0.5; b.glass.material = on ? b.glassOn : b.glassOff; b.neck.material = b.glass.material; b.glow.visible = on; b.fil.material.color.set(on ? 0xff8a1f : 0x4a4050); };
  b.glass.castShadow = false;
  return b;
}

// ---------- lights ----------
const hemi = new THREE.HemisphereLight(0xffffff, 0x554433, 1); root.add(hemi);
const sun = new THREE.DirectionalLight(0xffffff, 2); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, { left: -8, right: 8, top: 9, bottom: -3, near: 0.5, far: 40 }); sun.shadow.bias = -0.0015;
root.add(sun); root.add(sun.target);
function light(h, s, pos, hc = 0xfff1dc, gc = 0x4a3a44) { hemi.intensity = h; hemi.color.set(hc); hemi.groundColor.set(gc); sun.intensity = s; sun.position.set(...pos); sun.target.position.set(0, 1.5, 0); }

// ---------- STATION ----------
const station = new THREE.Group(); root.add(station);
const BX = [-3.2, -1.6, 0, 1.6, 3.2];
const stBulbs = [], stLights = [];
{
  const tile = ctex(1024, 512, (g, w, h) => {
    g.fillStyle = '#e9e1cf'; g.fillRect(0, 0, w, h);
    g.strokeStyle = 'rgba(120,105,90,0.45)'; g.lineWidth = 3;
    for (let y = 0; y < h; y += 32) for (let x = (y / 32 % 2) * 32 - 32; x < w; x += 64) g.strokeRect(x, y, 64, 32);
    g.fillStyle = '#2f6b4f'; g.fillRect(0, 0, w, 44); g.fillStyle = '#b3272d'; g.fillRect(0, 44, w, 12);
    g.fillStyle = '#3d3542'; g.fillRect(0, h - 96, w, 96); g.fillStyle = '#b3272d'; g.fillRect(0, h - 108, w, 12);
  });
  tile.wrapS = THREE.RepeatWrapping; tile.repeat.set(2, 1);
  M(new THREE.PlaneGeometry(22, 5.4), toon(0xffffff, { map: tile }), { p: [0, 2.7, -2.4], recv: true, cast: false, to: station });
  const sign = ctex(512, 160, (g, w, h) => { g.fillStyle = '#f3efe6'; g.fillRect(0, 0, w, h); g.fillStyle = '#1f3a6b'; g.fillRect(12, 12, w - 24, h - 24); g.fillStyle = '#f3efe6'; g.font = '92px Pop'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('SUBWAY', w / 2, h / 2 + 6); });
  M(box(2.2, 0.7, 0.08), toon(0xffffff, { map: sign }), { p: [0, 4.62, -2.34], ol: 0.03, to: station });
  M(box(22, 0.5, 5), toon(0x8d8794), { p: [0, -0.25, -0.1], recv: true, to: station });
  M(box(22, 0.06, 0.35), toon(0xf2c230), { p: [0, 0.01, 2.2], to: station, cast: false });
  M(box(22, 1.6, 0.2), toon(0x4a4450), { p: [0, -1.0, 2.35], to: station });
  M(box(22, 0.2, 6), toon(0x2c2731), { p: [0, -1.75, 5], recv: true, to: station });
  for (const z of [3.3, 4.6]) M(box(22, 0.16, 0.14), toon(0xc9ced6), { p: [0, -1.55, z], to: station });
  for (let x = -10; x <= 10; x += 0.9) M(box(0.32, 0.1, 2.2), toon(0x5a4030), { p: [x, -1.64, 3.95], to: station, cast: false });
  M(box(22, 0.3, 9), toon(0x2a2530), { p: [0, 5.5, 1], to: station, cast: false });
  for (const x of [-4.6, 4.6]) { M(box(0.34, 5.4, 0.34), toon(0x2f6b4f), { p: [x, 2.7, 1.5], ol: 0.03, to: station }); }
  for (const x of BX) {
    M(box(0.1, 0.1, 0.6), toon(0x2a2530), { p: [x, 3.42, -2.1], to: station });
    M(cyl(0.2, 0.14, 0.26, 20), toon(0xf3efe6), { p: [x, 3.3, -1.85], ol: 0.02, to: station });
    const b = makeBulb(); b.g.position.set(x, 3.17, -1.85); station.add(b.g); stBulbs.push(b);
    const pl = new THREE.PointLight(0xffd27a, 6, 9, 1.6); pl.position.set(x, 2.7, -1.2); station.add(pl); stLights.push(pl);
  }
}
const thief = makeChar(thiefOpts); root.add(thief.g);
const eng = makeChar(engOpts); root.add(eng.g);
const heldBulb = makeBulb(); root.add(heldBulb.g);

// ---------- OFFICE ----------
const office = new THREE.Group(); root.add(office);
const props = [];
{
  M(new THREE.PlaneGeometry(14, 9), toon(0x9c6b4a), { p: [0, 3.5, -1.6], recv: true, cast: false, to: office });
  for (let x = -6; x <= 6; x += 1) M(box(0.05, 9, 0.03), toon(0x7d543a), { p: [x, 3.5, -1.58], cast: false, to: office });
  M(box(14, 1.1, 0.1), toon(0x5a3a2a), { p: [0, 0.4, -1.55], cast: false, to: office });
  const bp = ctex(512, 640, (g, w, h) => {
    g.fillStyle = '#1f4f8f'; g.fillRect(0, 0, w, h); g.strokeStyle = 'rgba(255,255,255,0.18)'; g.lineWidth = 2;
    for (let i = 0; i < w; i += 40) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); } for (let i = 0; i < h; i += 40) { g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); }
    g.strokeStyle = '#e8f1ff'; g.lineWidth = 7; g.beginPath(); g.arc(w / 2, 250, 120, 0.72 * Math.PI, 0.28 * Math.PI); g.lineTo(w / 2 + 55, 430); g.lineTo(w / 2 - 55, 430); g.closePath(); g.stroke();
    for (let i = 0; i < 4; i++) { g.beginPath(); g.moveTo(w / 2 - 58, 450 + i * 26); g.lineTo(w / 2 + 58, 462 + i * 26); g.stroke(); }
    g.beginPath(); g.moveTo(40, 590); g.lineTo(w - 40, 590); g.stroke();
  });
  M(box(1.9, 2.4, 0.06), toon(0xffffff, { map: bp }), { p: [1.15, 3.6, -1.52], ol: 0.03, r: [0, 0, -0.04], to: office });
  M(box(4.6, 0.16, 1.5), toon(0x7a4a2c), { p: [0, 1.0, 0.9], ol: 0.03, recv: true, to: office });
  M(box(4.3, 1.0, 1.3), toon(0x5d3722), { p: [0, 0.45, 0.9], to: office });
  M(box(14, 0.2, 8), toon(0x6b4a3a), { p: [0, -0.1, 1], recv: true, to: office });
  // props: padlock, guard cap, bell
  const lock = new THREE.Group(); M(box(0.5, 0.42, 0.2), toon(0xf2c230), { ol: 0.03, p: [0, 0.21, 0], to: lock }); M(new THREE.TorusGeometry(0.16, 0.045, 10, 24, Math.PI), toon(0xc9ced6), { ol: 0.02, p: [0, 0.42, 0], to: lock }); M(cyl(0.05, 0.05, 0.22, 12), flat(INK), { p: [0, 0.2, 0.02], r: [Math.PI / 2, 0, 0], to: lock });
  const capg = new THREE.Group(); M(cyl(0.3, 0.26, 0.26, 24), toon(0x1f3a6b), { ol: 0.03, p: [0, 0.2, 0], to: capg }); M(cyl(0.34, 0.34, 0.04, 24), toon(0x17131c), { ol: 0.025, p: [0, 0.06, 0.12], s: [1, 1, 0.9], to: capg }); M(sph(0.07), toon(0xf2c230), { ol: 0.015, p: [0, 0.22, 0.28], to: capg });
  const bell = new THREE.Group(); M(sph(0.3, 28, 16, 0, 6.3, 0, Math.PI / 2), toon(0xf2c230), { ol: 0.03, p: [0, 0.06, 0], s: [1, 1.15, 1], to: bell }); M(cyl(0.34, 0.34, 0.06, 24), toon(0xd9a53a), { ol: 0.025, p: [0, 0.05, 0], to: bell }); M(sph(0.06), toon(0xd9a53a), { ol: 0.015, p: [0, 0.44, 0], to: bell });
  [lock, capg, bell].forEach((p, i) => { p.position.set(-0.85 + i * 0.85, 1.08, 1.15); p.scale.setScalar(1.25); office.add(p); props.push(p); });
}
const ideaBulb = makeBulb(); ideaBulb.g.rotation.x = Math.PI; root.add(ideaBulb.g);
const officeLight = new THREE.PointLight(0xffc98a, 14, 12, 1.5); officeLight.position.set(-1.5, 4.2, 2.5); office.add(officeLight);

// ---------- MACRO ----------
const macro = new THREE.Group(); root.add(macro);
const mBulb = makeBulb(); const arrowG = new THREE.Group(), arrowR = new THREE.Group();
{
  const bp = ctex(512, 1024, (g, w, h) => { g.fillStyle = '#173a6e'; g.fillRect(0, 0, w, h); g.strokeStyle = 'rgba(255,255,255,0.13)'; g.lineWidth = 2; for (let i = 0; i < w; i += 32) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); } for (let i = 0; i < h; i += 32) { g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); } g.strokeStyle = 'rgba(255,255,255,0.22)'; g.lineWidth = 4; g.beginPath(); g.arc(w / 2, h / 2, 220, 0, 7); g.stroke(); });
  M(new THREE.PlaneGeometry(9, 18), flat(0xffffff, { map: bp }), { p: [0, 2, -3], cast: false, to: macro });
  M(box(0.5, 0.5, 3.4), toon(0x2a2530), { p: [0, 4.75, -1.6], ol: 0.03, to: macro });
  M(cyl(0.62, 0.42, 0.9, 32), toon(0xf3efe6), { p: [0, 4.15, 0], ol: 0.035, to: macro });
  M(cyl(0.36, 0.36, 0.5, 32, true), toon(0xd9a53a, { side: THREE.DoubleSide }), { p: [0, 3.55, 0], ol: 0.03, to: macro });
  mBulb.g.scale.setScalar(3); macro.add(mBulb.g);
  const mk = (grp, col, dir) => {
    const m = flat(col);
    const t = M(new THREE.TorusGeometry(1.0, 0.075, 10, 48, Math.PI * 1.35), m, { r: [Math.PI / 2, 0, 0], ol: 0.03, to: grp, cast: false });
    const a = dir > 0 ? Math.PI * 1.35 : 0;
    const cone = M(new THREE.ConeGeometry(0.22, 0.42, 16), m, { ol: 0.03, to: grp, cast: false });
    cone.position.set(Math.cos(a), 0, -Math.sin(a) * 1); // torus rotated: (cos, 0, -sin)?
    cone.position.set(Math.cos(a) * 1.0, 0, Math.sin(a) * 1.0);
    const tan = V(-Math.sin(a), 0, Math.cos(a)).multiplyScalar(dir);
    cone.quaternion.setFromUnitVectors(UP, tan);
    t.rotation.x = -Math.PI / 2; // lay flat so arc param a -> (cos a,0,sin a)... flip handled by scale
    t.scale.z = 1; t.rotation.x = Math.PI / 2; t.scale.y = -1;
    grp.position.set(0, 2.9, 0); macro.add(grp);
  };
  mk(arrowG, 0x35c46a, 1); mk(arrowR, 0xe23b3b, -1);
}

// ---------- HOME ----------
const home = new THREE.Group(); root.add(home);
const homeLight = new THREE.PointLight(0xffb86b, 10, 10, 1.6); homeLight.position.set(1.8, 3.6, 2.5); home.add(homeLight);
const SOCK = V(0.75, 2.02, 0.5);
{
  const wp = ctex(512, 512, (g, w, h) => { for (let i = 0; i < 8; i++) { g.fillStyle = i % 2 ? '#7c4a58' : '#8d5a66'; g.fillRect(i * w / 8, 0, w / 8 + 1, h); } });
  wp.wrapS = wp.wrapT = THREE.RepeatWrapping; wp.repeat.set(3, 1);
  M(new THREE.PlaneGeometry(14, 9), toon(0xffffff, { map: wp }), { p: [0, 3.9, -1.6], recv: true, cast: false, to: home });
  M(box(14, 1.0, 0.1), toon(0x4a2c33), { p: [0, 0.4, -1.55], cast: false, to: home });
  M(box(14, 0.2, 8), toon(0x6b4636), { p: [0, -0.1, 1], recv: true, to: home });
  // window with moon
  M(box(1.7, 2.1, 0.1), toon(0xf3efe6), { p: [-0.9, 3.9, -1.55], ol: 0.03, to: home });
  M(box(1.45, 1.85, 0.12), flat(0x1c2550), { p: [-0.9, 3.9, -1.54], cast: false, to: home });
  M(cyl(0.3, 0.3, 0.02, 32), flat(0xfff4c2), { p: [-0.65, 4.3, -1.46], r: [Math.PI / 2, 0, 0], cast: false, to: home });
  M(box(0.07, 1.85, 0.14), toon(0xf3efe6), { p: [-0.9, 3.9, -1.52], to: home, cast: false }); M(box(1.45, 0.07, 0.14), toon(0xf3efe6), { p: [-0.9, 3.9, -1.52], to: home, cast: false });
  // table + lamp
  M(cyl(0.85, 0.85, 0.1, 36), toon(0x8a5a36), { p: [0.75, 1.1, 0.5], ol: 0.03, recv: true, to: home });
  M(cyl(0.1, 0.16, 1.1, 16), toon(0x6b4326), { p: [0.75, 0.55, 0.5], to: home });
  M(cyl(0.3, 0.36, 0.14, 24), toon(0x2f6b4f), { p: [0.75, 1.22, 0.5], ol: 0.025, to: home });
  M(cyl(0.05, 0.05, 0.6, 12), toon(0xd9a53a), { p: [0.75, 1.58, 0.5], ol: 0.02, to: home });
  M(cyl(0.15, 0.12, 0.2, 20), toon(0xd9a53a), { p: [0.75, 1.93, 0.5], ol: 0.02, to: home });
  M(cyl(0.11, 0.11, 0.02, 20), flat(INK), { p: [0.75, 2.035, 0.5], cast: false, to: home });
}

// ---------- extra assets ----------
const BLUE = 0x2b2aa8;
macro.children[0].material = flat(BLUE);
class Arc extends THREE.Curve { constructor(r, a) { super(); this.r = r; this.a = a; } getPoint(t) { const a = t * this.a; return V(Math.cos(a) * this.r, 0, Math.sin(a) * this.r); } }
function buildArrow(grp, col, dir) {
  grp.clear(); const m = flat(col), A = Math.PI * 1.65 * dir;
  M(new THREE.TubeGeometry(new Arc(1.05, A), 48, 0.08, 10), m, { ol: 0.035, to: grp, cast: false });
  const cone = M(new THREE.ConeGeometry(0.24, 0.46, 16), m, { ol: 0.035, to: grp, cast: false });
  cone.position.set(Math.cos(A) * 1.05, 0, Math.sin(A) * 1.05);
  cone.quaternion.setFromUnitVectors(UP, V(-Math.sin(A), 0, Math.cos(A)).multiplyScalar(dir));
  grp.rotation.x = 0.0; grp.position.set(0, 3.0, 0); macro.add(grp);
}
buildArrow(arrowG, 0x35c46a, 1); buildArrow(arrowR, 0xe23b3b, -1);
const helix = mBulb.g.children[1];

const riderOpts = (shirt, pants, hair, skin, extra = {}) => ({
  skin, shoe: 0x2a2230, ...extra,
  body: (g, w, h) => { g.fillStyle = shirt; g.fillRect(0, 0, w, h); g.fillStyle = 'rgba(0,0,0,0.25)'; g.fillRect(w * 0.49, 0, w * 0.02, h * 0.7); g.fillStyle = pants; g.fillRect(0, h * 0.72, w, h * 0.28); },
  hat: hg => { M(sph(0.475, 32, 16, 0, 6.3, 0, Math.PI * 0.42), toon(hair), { ol: 0.03, p: [0, 0.03, -0.03], to: hg }); }
});
const riders = [
  makeChar(riderOpts('#7b4a9c', '#3a3345', 0x3a2416, '#f6c9a0')),
  makeChar(riderOpts('#c9773a', '#4a3a2a', 0xc9a13a, '#e8b48a')),
  makeChar(riderOpts('#3a8a8f', '#2a2a3a', 0x17131c, '#c98f68')),
];
riders.forEach(r => root.add(r.g));
const guard = makeChar({
  skin: '#f0b98c', stache: true, shoe: 0x17131c,
  body: (g, w, h) => { g.fillStyle = '#1f3a6b'; g.fillRect(0, 0, w, h); g.fillStyle = '#f2c230'; for (let i = 0; i < 4; i++) { g.beginPath(); g.arc(w * 0.5, h * (0.16 + i * 0.13), 9, 0, 7); g.fill(); } g.fillRect(0, h * 0.66, w, 14); g.fillStyle = '#17233f'; g.fillRect(0, h * 0.72, w, h * 0.28); },
  hat: hg => { const m = toon(0x1f3a6b); M(cyl(0.4, 0.36, 0.28, 28), m, { ol: 0.035, p: [0, 0.4, 0], to: hg }); M(cyl(0.44, 0.44, 0.04, 28), toon(0x17131c), { ol: 0.03, p: [0, 0.27, 0.16], s: [1, 1, 0.9], to: hg }); M(sph(0.08), toon(0xf2c230), { ol: 0.02, p: [0, 0.42, 0.37], to: hg }); }
});
root.add(guard.g);
const cage = new THREE.Group(); station.add(cage);
{ const m = flat(INK); for (let i = 0; i < 10; i++) { const a = i / 10 * 6.283; M(cyl(0.022, 0.022, 0.95, 6), m, { p: [Math.cos(a) * 0.36, -0.42, Math.sin(a) * 0.36], to: cage, cast: false }); } for (const y of [0.05, -0.42, -0.9]) M(new THREE.TorusGeometry(0.36, 0.025, 6, 28), m, { p: [0, y, 0], r: [Math.PI / 2, 0, 0], to: cage, cast: false }); }
const pliers = new THREE.Group(); root.add(pliers);
{ for (const s of [-1, 1]) { M(box(0.05, 0.42, 0.05), toon(0xc9ced6), { ol: 0.02, p: [s * 0.03, 0.2, 0], r: [0, 0, s * -0.16], to: pliers }); M(box(0.07, 0.36, 0.07), toon(0xe23b3b), { ol: 0.02, p: [s * 0.08, -0.16, 0], r: [0, 0, s * 0.3], to: pliers }); } }
const key = new THREE.Group(); macro.add(key);
{ const m = toon(0xf2c230); M(new THREE.TorusGeometry(0.42, 0.13, 12, 32), m, { ol: 0.04, p: [-1.3, 0, 0], to: key }); M(cyl(0.11, 0.11, 1.7, 16), m, { ol: 0.04, p: [-0.1, 0, 0], r: [0, 0, Math.PI / 2], to: key }); for (const x of [0.35, 0.65]) M(box(0.16, 0.36, 0.14), m, { ol: 0.04, p: [x, -0.24, 0], to: key }); }
const bigLock = new THREE.Group(); macro.add(bigLock);
const shackle = M(new THREE.TorusGeometry(0.48, 0.13, 12, 28, Math.PI), toon(0xc9ced6), { ol: 0.04, p: [0, 0.62, 0], to: bigLock });
{ M(box(1.5, 1.25, 0.6), toon(0xd9772b), { ol: 0.05, to: bigLock }); M(cyl(0.16, 0.16, 0.62, 20), flat(INK), { r: [Math.PI / 2, 0, 0], p: [0, 0.05, 0.02], to: bigLock, cast: false }); M(box(0.14, 0.34, 0.62), flat(INK), { p: [0, -0.18, 0.02], to: bigLock, cast: false }); }
const booth = new THREE.Group(); station.add(booth); booth.position.set(8.2, 0, -1.4);
{
  const g = toon(0x2f6b4f);
  M(box(2.5, 1.35, 1.2), g, { ol: 0.035, p: [0, 0.68, 0], to: booth }); M(box(2.7, 0.14, 1.45), toon(0x8a5a36), { ol: 0.03, p: [0, 1.4, 0.05], to: booth });
  for (const s of [-1, 1]) M(box(0.2, 2.1, 1.2), g, { ol: 0.035, p: [s * 1.15, 2.5, 0], to: booth });
  M(box(2.7, 0.75, 1.3), g, { ol: 0.035, p: [0, 3.85, 0], to: booth });
  M(box(2.1, 2.1, 0.05), flat(0x2a2028), { p: [0, 2.5, -0.5], to: booth, cast: false });
  const sg = ctex(512, 128, (c, w, h) => { c.fillStyle = '#f3efe6'; c.fillRect(0, 0, w, h); c.fillStyle = '#b3272d'; c.font = '84px Pop'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('TICKETS 5¢', w / 2, h / 2 + 6); });
  booth.userData.sign = sg; M(box(2.3, 0.56, 0.06), toon(0xffffff, { map: sg }), { p: [0, 3.85, 0.67], to: booth, cast: false });
  const pl = new THREE.PointLight(0xffd27a, 5, 8, 1.6); pl.position.set(0, 3, 2.2); booth.add(pl);
}
const coin = M(cyl(0.13, 0.13, 0.03, 20), toon(0xf2c230), { ol: 0.02 }); root.add(coin);

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
    ctx.font = '74px Pop'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.lineJoin = 'round';
    ctx.strokeStyle = '#0d0a12'; ctx.lineWidth = 18; ctx.strokeText(w.w, 0, 4); ctx.strokeText(w.w, 0, 0);
    ctx.fillStyle = '#fff'; ctx.fillText(w.w, 0, 0); ctx.restore(); return;
  }
}

// ---------- timeline ----------
let TM, Ls, DUR = 52;
const S = i => Ls[i].s, CUT = i => Ls[i].s - 0.1;
function wf(i, str, nth = 1) { let n = 0; for (const w of Ls[i].words) if (w.w.toLowerCase().replace(/[^a-z']/g, '').startsWith(str)) { if (++n === nth) return w.s; } console.log('word not found', i, str); return Ls[i].s; }
function setCam(p, l, fov, t) { cam.fov = fov; cam.position.set(p[0] + 0.025 * Math.sin(t * 1.3), p[1] + 0.02 * Math.sin(t * 1.7 + 1), p[2]); cam.lookAt(l[0], l[1], l[2]); cam.updateProjectionMatrix(); }
const bg = c => { root.background = new THREE.Color(c); };
function stationMode(mode, t, on = [1, 1, 1, 1, 1]) {
  station.visible = true; cage.visible = false;
  stBulbs.forEach((b, i) => { b.g.visible = !!on[i]; b.g.position.set(BX[i], 3.17, -1.85); b.g.rotation.set(0, 0, 0); b.lit(on[i] ? 1 : 0); stLights[i].intensity = on[i] ? 1.5 + 0.1 * Math.sin(t * 13 + i) : 0; });
  if (mode === 'night') { bg(0x15121a); light(0.42, 0.75, [3, 8, 7], 0xffe2b8, 0x3a2e3a); }
  else if (mode === 'dark') { bg(0x0c0b16); light(0.2, 0.3, [3, 8, 7], 0xaab6ff, 0x221c30); }
  else { bg(0x2a2530); light(0.62, 1.0, [3, 8, 7], 0xfff0d0, 0x5a4a50); }
}
function show(c, x, z, ry = 0) { c.g.visible = true; c.g.position.set(x, 0, z); c.g.rotation.set(0, ry, 0); c.g.scale.setScalar(1); c.hatG.position.set(0, 0, 0); c.hatG.rotation.set(0, 0, 0); c.g.updateMatrixWorld(true); }
function toLocal(c, w) { const p = w.clone(); c.up.worldToLocal(p); return [p.x, p.y, p.z]; }
function bulbAt(b, p, lit, flip, s = 1) { b.g.visible = true; b.lit(lit); b.g.position.copy(p); b.g.rotation.set(flip ? Math.PI : 0, 0, 0); b.g.scale.setScalar(s); }
// unscrew animation for a character under station bulb i; k 0..1
function unscrew(c, i, k, face = 'sneaky') {
  show(c, BX[i], -1.55); c.face(face);
  c.pose({ bob: 0.16, rh: [0.08, lerp(2.36, 2.04, k), -0.2], lh: [-0.5, 1.2, 0.15], hx: -0.3 });
  const b = stBulbs[i]; b.g.visible = true; b.g.position.y = lerp(3.17, 2.85, k); b.g.rotation.y = k * 14; const on = k < 0.6; b.lit(on ? 1 : 0); stLights[i].intensity = on ? 1.5 : 0;
}

let overlay = () => { };
const ALL = () => [station, office, macro, home, thief.g, eng.g, guard.g, heldBulb.g, ideaBulb.g, pliers, coin, ...riders.map(r => r.g)];
function update(t) {
  for (const g of ALL()) g.visible = false;
  overlay = () => { };
  let li = 0; for (let i = 0; i < Ls.length; i++) if (t >= CUT(i)) li = i;
  const s0 = li === 0 ? 0 : CUT(li), s1 = li + 1 < Ls.length ? CUT(li + 1) : DUR, k = (t - s0) / (s1 - s0), u = t - s0;
  const sub = (a, b) => cl((t - a) / (b - a));

  if (li === 0) { // HOOK
    const tb = wf(0, 'beaten') - 0.05;
    if (t < tb) {
      stationMode('night', t); show(thief, 0.4, -0.9); thief.face('sneaky');
      thief.pose({ lh: [-0.36, 1.2, 0.3], rh: [0.36, 1.25, 0.3], bob: 0.02 * Math.sin(t * 6), hz: 0.06 * Math.sin(t * 3) });
      setCam([lerp(0.9, 0.5, k * 2), 1.5, lerp(4.6, 3.7, sub(0, tb))], [0.4, 2.15, -0.9], 40, t);
      overlay = () => popText('BEST THIEF', W / 2, 300, 132, '#ffd23e', t, 0.35, tb - 0.03);
    } else {
      home.visible = true; bg(0x4a2c33); light(0.8, 1.3, [4, 7, 6], 0xffdcb0, 0x4a3038);
      show(thief, 0, 0.4); const v = t - tb, hit = 0.28;
      thief.face(v < hit ? 'neutral' : 'shock');
      const sq = v > hit ? 0.1 * Math.exp(-(v - hit) * 6) * Math.cos((v - hit) * 30) : 0;
      thief.pose({ bob: -sq, lh: [-0.62, v > hit ? 1.9 : 1.05, 0.15], rh: [0.62, v > hit ? 1.9 : 1.05, 0.15], hx: v > hit ? 0.12 : -0.3 });
      const by = v < hit ? lerp(5.2, 3.35, (v / hit) ** 2) : 3.35 + (v - hit) * 3.2 - (v - hit) ** 2 * 5;
      bulbAt(heldBulb, V((v > hit ? (v - hit) * 1.4 : 0), by, 0.45), 1, false, 1.15); heldBulb.g.rotation.z = v > hit ? -(v - hit) * 6 : 0;
      setCam([0.15, 2.2, lerp(4.6, 4.2, sub(tb, s1))], [0, 2.3, 0.4], 42, t);
      overlay = () => { burst('BONK!', 760, 420, 190, t, tb + hit, tb + hit + 0.7, 0.12); popText('A LIGHT BULB', W / 2, 250, 118, '#ffd23e', t, wf(0, 'light') - 0.05, s1 - 0.02); };
    }
  }
  else if (li === 1) {
    const tb = wf(1, 'and') - 0.05;
    stationMode('night', t);
    if (t < tb) {
      const kk = sub(s0, tb), ph = t * 9; show(thief, lerp(4.4, 0.6, ss(0, 1, kk)), -0.9); thief.face('sneaky');
      thief.pose({ ...thief.walk(ph, 0.2), lh: [-0.42, 1.5 + 0.05 * Math.sin(ph), 0.25], rh: [0.42, 1.5 - 0.05 * Math.sin(ph), 0.25], hy: -0.35, lean: 0.06, bob: 0.04 * Math.abs(Math.sin(ph)) - 0.08 });
      setCam([0.4, 1.5, lerp(11.6, 9.4, kk)], [0.3, 2.1, -1], 42, t);
      overlay = () => { popText('NEW YORK', W / 2, 235, 118, '#fff', t, s0 + 0.25, tb - 0.03); popText('1904', W / 2, 375, 128, '#ffd23e', t, s0 + 0.55, tb - 0.03); };
    } else {
      show(thief, 0, -1.2); thief.face('happy'); const kk = sub(tb, s1);
      thief.pose({ hx: -0.45, lh: [-0.3, lerp(1.5, 2.0, kk), 0.3], rh: [0.3, lerp(1.5, 2.0, kk), 0.3], bob: 0.03 * Math.sin(t * 6) });
      setCam([0.55, lerp(1.85, 2.05, kk), 1.7], [0, 2.95, -1.85], 44, t);
      overlay = () => popText('FREE LIGHT', W / 2, 1150, 124, '#ffd23e', t, wf(1, 'never') - 0.03, s1 - 0.02, { rot: -0.04 });
    }
  }
  else if (li === 2) { // one twist, one bulb, under his hat
    const t1 = wf(2, 'one', 2), t2 = wf(2, 'straight') - 0.05;
    stationMode('night', t); const kk = ss(s0 + 0.15, t2 - 0.1, t);
    if (t < t2) { unscrew(thief, 2, kk); }
    else {
      const v = sub(t2, s1 - 0.25); stBulbs[2].g.visible = false; stLights[2].intensity = 0;
      show(thief, 0, -1.55); thief.face('happy');
      const lift = Math.sin(cl(v * 1.15) * Math.PI) * 0.75; thief.hatG.position.y = lift; thief.hatG.rotation.z = -lift * 0.5;
      const hp = V(lerp(0.08, 0, v), lerp(2.2, 2.62, ss(0, 0.5, v)), lerp(-0.2, 0, v));
      thief.pose({ rh: [hp.x + 0.12, Math.min(hp.y, 2.5), hp.z], lh: [-0.42, 2.45 + lift, 0.1] });
      if (v < 0.72) bulbAt(heldBulb, V(hp.x, hp.y + 0.78 * lerp(1, 0.6, v), -1.55 + hp.z), 0, true, lerp(1, 0.6, v));
    }
    setCam([lerp(0.9, 0.3, k), 2.0, lerp(5.6, 4.8, k)], [0, 2.25, -1.5], 42, t);
    overlay = () => { popText('1 TWIST', W / 2, 250, 120, '#fff', t, s0 + 0.1, t2 + 0.25); popText('= 1 BULB', W / 2, 390, 120, '#ffd23e', t, t1, t2 + 0.25); popText('HAT TRICK', W / 2, 300, 124, '#ffd23e', t, t2 + 0.4, s1 - 0.02, { rot: 0.04 }); };
  }
  else if (li === 3) { // everybody
    stationMode('night', t, [1, 1, 0, 1, 1]); const tb = wf(3, 'half') - 0.05, kk = ss(tb - 0.2, s1 - 0.15, t);
    [[riders[0], 0], [riders[1], 1], [riders[2], 3], [thief, 4]].forEach(([c, i], n) => unscrew(c, i, cl(kk * 1.25 - n * 0.08), c === thief ? 'sneaky' : 'happy'));
    setCam([lerp(-1.6, 1.2, ss(0, 1, k)), 1.9, lerp(9.8, 11.2, k)], [lerp(-0.6, 0.4, k), 2.2, -1.5], 44, t);
    overlay = () => { popText('NOT ALONE', W / 2, 270, 120, '#fff', t, s0 + 0.3, tb - 0.03); popText('HALF THE CITY', W / 2, 270, 112, '#ffd23e', t, tb, s1 - 0.02); };
  }
  else if (li === 4) { // dark
    const n = 4 - Math.floor(cl(k * 1.5) * 4 + 0.001), ord = [3, 1, 9, 2, 0];
    stationMode(k > 0.62 ? 'dark' : 'night', t, ord.map(o => o < n ? 1 : 0));
    if (k <= 0.62) light(lerp(0.42, 0.22, k / 0.62), lerp(0.75, 0.3, k / 0.62), [3, 8, 7], 0xd8d0ff, 0x2a2436);
    show(riders[1], 0.3, -0.8); riders[1].face(k > 0.62 ? 'shock' : 'neutral'); riders[1].pose({ hy: 0.5 * Math.sin(t * 5), lh: [-0.6, 1.3, 0.2], rh: [0.6, 1.3, 0.2] });
    setCam([0, 1.7, lerp(9.6, 10.8, k)], [0, 2.2, -1], 42, t);
    overlay = () => popText('DARK', W / 2, 320, 190, '#8fa0ff', t, wf(4, 'dark') - 0.05, s1 - 0.02);
  }
  else if (li === 5) { // guards
    const tb = wf(5, 'lenny') - 0.05, tw = wf(5, 'and') - 0.05;
    stationMode('day', t); show(guard, 0, -1.3); show(thief, 1.75, -1.0, -0.4);
    const asleep = t > tw + 0.25; guard.face(asleep ? 'sleep' : 'angry');
    guard.pose(asleep ? { hx: 0.35, hz: 0.1 * Math.sin(t * 2), bob: -0.04 + 0.02 * Math.sin(t * 2), lh: [-0.4, 1.0, 0.1], rh: [0.4, 1.0, 0.1] } : { lh: [-0.36, 1.2, 0.3], rh: [0.36, 1.2, 0.3], hy: 0.4 * Math.sin(t * 3) });
    const tip = t > tb ? Math.sin(cl((t - tb) / 0.9) * Math.PI) : 0;
    thief.face(t > tb ? 'happy' : 'sneaky'); thief.hatG.position.y = tip * 0.6; thief.hatG.position.x = tip * 0.25; thief.hatG.rotation.z = -tip * 0.7;
    thief.pose({ rh: tip > 0.02 ? [0.45, 2.55 + tip * 0.45, 0.1] : [0.5, 1.05, 0.1], lh: [-0.5, 1.05, 0.1], bob: 0.02 * Math.sin(t * 4) });
    if (tip > 0.15) { const hp = thief.headG.getWorldPosition(V(0, 0, 0)); bulbAt(heldBulb, hp.add(V(0, 0.92, 0)), 1, true, 0.6); }
    if (t < tb) setCam([lerp(-0.5, -0.2, k), 1.8, lerp(5.2, 4.6, sub(s0, tb))], [0, 2.3, -1.3], 42, t);
    else setCam([lerp(1.3, 1.0, k), 2.0, lerp(6.6, 6.0, sub(tb, s1))], [0.9, 2.2, -1.2], 42, t);
    overlay = () => { popText('GUARDS', W / 2, 290, 150, '#fff', t, wf(5, 'guards') - 0.05, tb - 0.03); if (asleep) { const [x, y] = proj(guard.headG.getWorldPosition(V(0, 0, 0)).add(V(-0.5, 0.9, 0))); for (let i = 0; i < 3; i++) popText('Z', x - i * 60, y - i * 95 - 20 * Math.sin(t * 3 + i), 70 + i * 28, '#fff', t, tw + 0.3 + i * 0.18, s1); } };
  }
  else if (li === 6) { // cages / pliers
    const tb = wf(6, 'lenny') - 0.05, tp = wf(6, 'pliers') - 0.02;
    stationMode('day', t); cage.visible = true;
    if (t < tb) {
      const v = sub(s0 + 0.15, s0 + 0.6); const y = lerp(5.6, 3.3, v * v) + (v >= 1 ? 0.08 * Math.exp(-(t - s0 - 0.6) * 8) * Math.abs(Math.cos((t - s0 - 0.6) * 22)) : 0);
      cage.position.set(0, y, -1.85); cage.rotation.set(0, 0, 0);
      setCam([lerp(0.9, 0.6, k), 1.9, lerp(2.4, 2.0, k)], [0, 2.95, -1.85], 44, t);
      overlay = () => { burst('CLANG!', 300, 520, 180, t, s0 + 0.6, tb - 0.03); popText('CAGES', W / 2, 1150, 150, '#fff', t, wf(6, 'cages') - 0.05, tb - 0.03); };
    } else {
      const v = t - tp; show(thief, 0.25, -1.55); thief.face(v > 0 ? 'happy' : 'sneaky');
      const hp = V(0.3, 2.42 - 0.16, -0.15); thief.pose({ bob: 0.16, rh: [hp.x, hp.y, hp.z], lh: [-0.5, 1.2, 0.15], hx: -0.25 });
      pliers.visible = true; pliers.position.set(0.25 + 0.3, hp.y + 0.16 + 0.3, -1.55 - 0.15); pliers.rotation.z = 0.5 + (v > 0 ? 0 : 0.15 * Math.sin(t * 20));
      cage.position.set(v > 0 ? -v * 1.6 : 0, v > 0 ? 3.3 - v * v * 9 + v * 1.2 : 3.3, -1.85 + (v > 0 ? v * 1.5 : 0)); cage.rotation.z = v > 0 ? v * 4 : 0;
      setCam([lerp(0.7, 0.4, k), 2.1, 4.6], [0.1, 2.4, -1.6], 42, t);
      overlay = () => burst('SNIP!', 300, 470, 190, t, tp, s1 - 0.02);
    }
  }
  else if (li === 7) { // engineer
    office.visible = true; bg(0x6b4636); light(0.95, 1.5, [-3, 7, 6], 0xffe6c4, 0x6b4a3a); props.forEach(p => p.visible = false);
    show(eng, 0, -0.35); const idea = wf(7, 'changed') - 0.05, lit = t > idea;
    eng.face(lit ? 'happy' : 'think');
    eng.pose(lit ? { rh: [0.42, 2.75, 0.1], lh: [-0.5, 1.25, 0.2], bob: 0.1 * Math.abs(Math.sin((t - idea) * 9)) * (1 - ss(idea, idea + 0.6, t)) }
      : { rh: [0.16, 1.78, 0.34], lh: [-0.2, 1.2, 0.3], hz: 0.12 * Math.sin(t * 2.2), hx: -0.08, bob: 0.015 * Math.sin(t * 3) });
    if (lit) { bulbAt(ideaBulb, V(0, 3.3 + 0.05 * Math.sin(t * 6), -0.35), 1, true, 1.25 * back((t - idea) / 0.2)); }
    setCam([lerp(0.6, 0.1, k), lerp(2.2, 2.45, k), lerp(6.6, 5.2, k)], [0, 2.4, -0.3], 40, t);
    overlay = () => { popText('?', 290, 560, 220, '#fff', t, s0 + 0.5, idea, { rot: -0.2 }); popText('ONE TINY', W / 2, 250, 122, '#fff', t, wf(7, 'one') - 0.03, s1 - 0.02); popText('THING', W / 2, 395, 140, '#ffd23e', t, wf(7, 'thing') - 0.03, s1 - 0.02); };
  }
  else if (li === 8) { // takes bulb home
    home.visible = true; bg(0x4a2c33); light(0.8, 1.3, [4, 7, 6], 0xffdcb0, 0x4a3038);
    const x = lerp(-3.2, -0.35, ss(0, 0.8, k)); show(thief, x, 0.35, 0.35); thief.face('happy');
    const walking = k < 0.8; const P = { ...(walking ? thief.walk(u * 9, 0.22) : {}), rh: [0.45, 2.55, 0.2], lh: [-0.5, 1.15, 0.1] }; thief.pose(P);
    const hp = V(...P.rh); thief.g.updateMatrixWorld(true); thief.up.localToWorld(hp); bulbAt(heldBulb, hp.add(V(0, 0.75, 0)), 0, true, 1);
    setCam([lerp(-0.6, 0.5, k), 2.2, lerp(6.4, 5.4, k)], [lerp(-0.6, 0.2, k), 2.2, 0.4], 42, t);
    overlay = () => popText('LIKE ALWAYS', W / 2, 290, 118, '#ffd23e', t, wf(8, 'like') - 0.03, s1 - 0.02);
  }
  else if (li === 9) { // twist / wobble / harder / foot
    home.visible = true; bg(0x4a2c33); light(0.8, 1.3, [4, 7, 6], 0xffdcb0, 0x4a3038);
    const a = wf(9, 'it') - 0.05, b = wf(9, 'he', 2) - 0.05, c = wf(9, 'it', 2) - 0.05;
    show(thief, -0.35, 0.35, 0.35);
    const hold = (bp, extra = {}) => thief.pose({ rh: toLocal(thief, bp.clone().add(V(-0.04, 0.5, 0))), lh: [-0.5, 1.2, 0.15], hy: 0.3, ...extra });
    if (t < a) {
      thief.face('happy'); const bp = V(0.75, 2.14 + 0.03 * Math.abs(Math.sin(u * 14)), 0.5); bulbAt(heldBulb, bp, 0, true); heldBulb.g.rotation.y = u * 9; hold(bp);
      setCam([lerp(1.3, 1.0, k), 2.4, 4.3], [0.5, 2.2, 0.4], 42, t);
    } else if (t < b) {
      thief.face('neutral'); const v = t - a; const bp = V(0.75, 2.16, 0.5); bulbAt(heldBulb, bp, 0, true); heldBulb.g.rotation.z = 0.32 * Math.sin(v * 16); thief.pose({ rh: [0.75, 1.5, 0.2], lh: [-0.5, 1.2, 0.15], hy: 0.4, hz: 0.1 * Math.sin(v * 16) });
      setCam([0.9, 2.3, 3.3], [0.7, 2.35, 0.5], 42, t);
    } else if (t < c) {
      thief.face('angry'); const v = t - b; const bp = V(0.75, 2.14 + 0.07 * Math.abs(Math.sin(v * 22)), 0.5); bulbAt(heldBulb, bp, 0, true); heldBulb.g.rotation.y = Math.sin(v * 24) * 2.4;
      thief.pose({ rh: toLocal(thief, bp.clone().add(V(-0.04 + 0.08 * Math.sin(v * 24), 0.5, 0.08 * Math.cos(v * 24)))), lh: toLocal(thief, bp.clone().add(V(-0.22, 0.2, 0.15))), hy: 0.3 + 0.05 * Math.sin(v * 30), bob: 0.03 * Math.sin(v * 30), lean: -0.1 });
      setCam([lerp(0.1, 0.3, sub(b, c)), 2.35, lerp(4.3, 3.7, sub(b, c))], [0.2, 2.15, 0.4], 42, t);
    } else {
      const v = t - c, land = 0.42, q = cl(v / land); thief.face(v > land ? 'shock' : 'angry');
      const foot = V(-0.12, 0.2, 0.75); const st = V(0.75, 2.5, 0.5);
      const bp = v < land ? V(lerp(st.x, foot.x, q), lerp(st.y, foot.y, q * q) + Math.sin(q * Math.PI) * 0.9, lerp(st.z, foot.z, q)) : V(foot.x - (v - land) * 0.5, 0.26 + Math.abs(Math.sin((v - land) * 9)) * 0.25 * Math.exp(-(v - land) * 3), foot.z + (v - land) * 0.3);
      bulbAt(heldBulb, bp, 0, true); heldBulb.g.rotation.z = v * 7;
      const hop = v > land ? Math.abs(Math.sin((v - land) * 11)) * 0.22 : 0;
      thief.pose(v > land ? { bob: hop, lf: [-0.15, 0.35 + hop, 0.25], rf: [0.15, hop, 0], lh: [-0.7, 2.0, 0.1], rh: [0.7, 2.0, 0.1] } : { rh: [0.6, 1.9, 0.2], lh: [-0.5, 1.2, 0.15], hy: 0.3 });
      setCam([-0.3, lerp(1.5, 1.3, sub(c, s1)), lerp(6.2, 5.6, sub(c, s1))], [-0.1, 1.55, 0.4], 44, t);
    }
    overlay = () => {
      burst('TWIST!', 300, 430, 180, t, s0 + 0.1, a - 0.03); popText('WOBBLE', W / 2, 330, 130, '#fff', t, a + 0.05, b - 0.03, { rot: 0.07 * Math.sin(t * 16) });
      burst('TWIST!!', 780, 430, 190, t, b + 0.1, c - 0.03, 0.14); if (t > b && t < c) drops(thief, t - b);
      burst('BONK!', 330, 1090, 200, t, c + 0.42, s1 - 0.03);
    };
  }
  else if (li >= 10 && li <= 13) { // ===== blue explainer =====
    macro.visible = true; bg(BLUE); light(1.25, 1.6, [3, 6, 8], 0xffffff, 0x5a5ac0);
    const rig = v => { macro.children.forEach((c, i) => { if (i >= 1 && i <= 3) c.visible = v; }); mBulb.g.visible = v; };
    arrowG.visible = arrowR.visible = key.visible = bigLock.visible = false; rig(true); helix.scale.x = 1;
    const place = (ins, rot, lit) => { mBulb.g.position.set(0, lerp(2.45, 3.75, cl(ins)), 0); mBulb.g.rotation.set(0, rot, 0); mBulb.lit(lit ? 1 : 0); };
    if (li === 10) {
      const tr = wf(10, 'tightens') - 0.1, ins = ss(tr, s1 - 0.35, t); place(ins, ins * 9, ins > 0.95);
      arrowR.visible = t > tr; arrowR.rotation.y = -t * 2.4; arrowR.children.forEach(c => c.material.color.set(0xffffff));
      setCam([lerp(1.3, 0.2, k), lerp(3.6, 3.9, k), lerp(9.0, 8.0, k)], [0, 2.75, 0], 42, t);
      overlay = () => { popText('EVERY LAMP', W / 2, 250, 120, '#fff', t, wf(10, 'every') - 0.03, s1 - 0.02); popText('RIGHT = TIGHT', W / 2, 395, 112, '#ffd23e', t, wf(10, 'right') - 0.25, s1 - 0.02); };
    } else if (li === 11) {
      const tf = wf(11, 'backwards') - 0.08, f = sub(tf, tf + 0.3); place(0, 0.6 * Math.sin(t * 1.5), false);
      helix.scale.x = lerp(1, -1, ss(0, 1, f)); mBulb.g.scale.setScalar(3 * (1 + 0.12 * Math.sin(f * Math.PI)));
      setCam([lerp(0.9, 0.3, k), lerp(2.5, 2.3, k), lerp(5.6, 3.9, ss(0, 1, k))], [0, 2.25, 0], 42, t);
      overlay = () => { popText('THREADS', W / 2, 250, 118, '#fff', t, wf(11, 'threads') - 0.05, s1 - 0.02); popText('BACKWARDS', W / 2, 395, 132, '#ffd23e', t, tf, s1 - 0.02, { rot: -0.03 }); if (f > 0 && f < 1) { ctx.fillStyle = `rgba(255,255,255,${0.55 * Math.sin(f * Math.PI)})`; ctx.fillRect(0, 0, W, H); } };
    } else if (li === 12) {
      helix.scale.x = -1; mBulb.g.scale.setScalar(3);
      const tR = wf(12, 'right') - 0.08, ins = ss(s0 + 0.1, tR - 0.35, t), outk = sub(tR + 0.25, s1 - 0.1);
      if (t < tR) { place(ins, -ins * 9, ins > 0.95); arrowG.visible = true; arrowG.rotation.y = t * 2.4; }
      else { const un = ss(tR, tR + 0.3, t); place(1 - un, -9 + un * 9, false); mBulb.g.position.y -= outk * outk * 6; mBulb.g.rotation.z = outk * 1.2; arrowR.visible = true; arrowR.children.forEach(c => c.material.color.set(0xe23b3b)); arrowR.rotation.y = -t * 2.4; }
      setCam([lerp(-0.9, 0.6, k), 3.9, 8.4], [0, 2.7, 0], 42, t);
      overlay = () => { popText('LEFT = TIGHT', W / 2, 300, 124, '#4be08a', t, s0 + 0.05, tR - 0.02); popText('RIGHT =', W / 2, 250, 118, '#fff', t, tR, s1 - 0.02); popText('FALLS OUT', W / 2, 395, 128, '#ff5a4a', t, wf(12, 'fall') - 0.03, s1 - 0.02); };
    } else {
      rig(false); const tb = wf(13, 'and') - 0.05;
      if (t < tb) {
        key.visible = bigLock.visible = true; const v = ss(s0 + 0.2, s0 + 1.0, t), turn = ss(s0 + 1.1, s0 + 1.5, t);
        bigLock.position.set(0.9, 2.6, 0); bigLock.rotation.y = -0.25; shackle.position.y = 0.62 + turn * 0.3; shackle.rotation.y = turn * 0.9;
        key.position.set(lerp(-2.6, -0.55, v), 2.65, 0.75); key.rotation.x = turn * Math.PI / 2;
        setCam([lerp(-0.4, 0.2, k), 2.9, lerp(8.6, 7.6, k)], [0, 2.7, 0], 42, t);
        overlay = () => { popText('ONE KEY', W / 2, 250, 124, '#fff', t, wf(13, 'key') - 0.03, tb - 0.02); popText('ONE LOCK', W / 2, 395, 124, '#ff9a3a', t, wf(13, 'one') - 0.03, tb - 0.02); burst('CLICK!', 790, 620, 150, t, s0 + 1.45, tb - 0.03, 0.1); };
      } else {
        show(thief, 0, 0); thief.face('sad'); thief.pose({ rh: [0.45, 1.9, 0.25], lh: [-0.62, 1.5, 0.2], hy: 0.45 * Math.sin((t - tb) * 5), bob: 0.02 * Math.sin(t * 5) });
        const hp = V(0.45, 1.9, 0.25); thief.up.localToWorld(hp); bulbAt(heldBulb, hp.add(V(0, 0.75, 0)), 0, true);
        setCam([0.3, 2.0, lerp(7.0, 6.2, sub(tb, s1))], [0, 2.0, 0], 42, t);
        overlay = () => { popText('NO LOCK', W / 2, 300, 150, '#ff5a4a', t, wf(13, 'own') - 0.05, s1 - 0.02); popText('?', 800, 620, 200, '#fff', t, tb + 0.15, s1 - 0.02, { rot: 0.2 }); };
      }
    }
  }
  else if (li === 14) { // stealing stopped
    stationMode('day', t); show(eng, 0.2, -0.9); eng.face('happy');
    const tip = Math.sin(cl((u - 0.5) / 1.0) * Math.PI); eng.hatG.position.y = tip * 0.45; eng.hatG.rotation.z = -tip * 0.5;
    eng.pose({ rh: tip > 0.02 ? [0.5, 2.6 + tip * 0.4, 0.1] : [0.42, 1.15, 0.22], lh: [-0.42, 1.15, 0.22], bob: 0.03 * Math.sin(t * 5) });
    setCam([lerp(1.2, 0.5, k), lerp(1.6, 1.9, k), lerp(8.6, 7.0, ss(0, 1, k))], [0.15, 2.35, -1], 42, t);
    overlay = () => { popText('STEALING', W / 2, 250, 120, '#fff', t, wf(14, 'stealing') - 0.03, s1 - 0.02); popText('STOPPED', W / 2, 395, 136, '#4be08a', t, wf(14, 'stopped') - 0.03, s1 - 0.02); };
  }
  else if (li === 15) { // ticket
    const tb = wf(15, 'he') - 0.05; stationMode('day', t);
    if (t < tb) {
      show(thief, 0.3, -0.9); thief.face('sad'); thief.pose({ hx: -0.3, hz: 0.08 * Math.sin(t * 3), lh: [-0.5, 1.0, 0.05], rh: [0.5, 1.0, 0.05], bob: -0.04 });
      setCam([lerp(0.8, 0.5, k), 1.7, lerp(4.4, 3.9, sub(s0, tb))], [0.3, 2.3, -0.9], 40, t);
      overlay = () => popText('LENNY?', W / 2, 300, 150, '#fff', t, s0 + 0.12, tb - 0.02);
    } else {
      const v = sub(tb, s1), give = ss(0.25, 0.6, v);
      show(riders[2], 8.2, -1.75); riders[2].face('happy'); riders[2].pose({ rh: [0.3, 1.6, 0.4], lh: [-0.4, 1.3, 0.3], bob: 0.02 * Math.sin(t * 5) });
      show(thief, 6.95, -0.2, 2.3); thief.face('neutral'); const hand = [lerp(0.5, 0.25, give), lerp(1.05, 1.62, give), lerp(0.1, 0.75, give)]; thief.pose({ rh: hand, lh: [-0.5, 1.05, 0.1] });
      const hp = V(...hand); thief.up.localToWorld(hp); coin.visible = true; coin.position.copy(hp).add(V(0, 0.12, 0)); coin.rotation.set(Math.PI / 2, t * 6, 0);
      setCam([lerp(7.2, 7.6, v), 2.3, lerp(6.6, 5.6, v)], [7.9, 2.25, -1], 42, t);
      overlay = () => { popText('FIRST EVER', W / 2, 1010, 104, '#fff', t, wf(15, 'first') - 0.03, s1 - 0.02); popText('TICKET', W / 2, 1140, 128, '#ffd23e', t, wf(15, 'ticket') - 0.03, s1 - 0.02); burst('CLINK!', 300, 560, 160, t, tb + 0.6 * (s1 - tb), s1 - 0.02); };
    }
  }
  else { // finale
    stationMode('day', t); stLights.forEach((l, i) => l.intensity = 1.9 + 0.2 * Math.sin(t * 9 + i * 2));
    show(thief, 0, -0.9); thief.face('happy');
    thief.pose({ hx: -0.38, lh: [-0.75, 2.2 + 0.05 * Math.sin(t * 5), 0.1], rh: [0.75, 2.2 + 0.05 * Math.cos(t * 5), 0.1], bob: 0.04 * Math.sin(t * 5) });
    { const w = cl(u / 2.2), tp = Math.sin(cl((u - 2.3) / 0.9) * Math.PI); show(eng, lerp(-3.6, -1.25, ss(0, 1, w)), -1.7, 0.3); eng.face('happy'); eng.hatG.position.y = tp * 0.45; eng.hatG.rotation.z = -tp * 0.5; eng.pose({ ...(w < 1 ? eng.walk(u * 8, 0.18) : {}), lh: [-0.5, 1.05, 0.05], rh: tp > 0.02 ? [0.5, 2.6 + tp * 0.4, 0.1] : [0.5, 1.05, 0.05] }); }
    setCam([lerp(0.9, 0.3, k), lerp(1.5, 1.8, k), lerp(8.6, 6.2, ss(0, 1, k))], [-0.3, 2.4, -1.3], 42, t);
    overlay = () => { popText('HE PAID', W / 2, 250, 124, '#fff', t, wf(16, 'he') - 0.03, DUR + 1); popText('FOR LIGHT', W / 2, 395, 136, '#ffd23e', t, wf(16, 'light') - 0.05, DUR + 1); };
  }
}

function renderFrame(t) {
  update(t);
  root.updateMatrixWorld(true);
  renderer.render(root, cam);
  ctx.drawImage(glc, 0, 0);
  const v = ctx.createRadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 0.75); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(10,5,15,0.34)'); ctx.fillStyle = v; ctx.fillRect(0, 0, W, H);
  overlay(); caption(t);
  const f = 1 - ss(0, 0.15, t); if (f > 0) { ctx.fillStyle = `rgba(0,0,0,${f})`; ctx.fillRect(0, 0, W, H); }
}
window.renderFrame = t => { renderFrame(t); return out.toDataURL('image/jpeg', 0.94); };

(async () => {
  TM = await (await fetch('timing.json?' + Date.now())).json(); Ls = TM.lines; DUR = TM.voEnd + 0.9;
  await document.fonts.load('92px Pop');
  // redraw font-dependent textures now that the font is loaded
  const sg = booth.userData.sign, c = sg.userData.g; c.fillStyle = '#f3efe6'; c.fillRect(0, 0, 512, 128); c.fillStyle = '#b3272d'; c.font = '74px Pop'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('TICKETS 5¢', 256, 70); sg.needsUpdate = true;
  window.DUR = DUR; window.cuts = Ls.map((l, i) => CUT(i));
  renderFrame(0); window.ready = true;
})();
