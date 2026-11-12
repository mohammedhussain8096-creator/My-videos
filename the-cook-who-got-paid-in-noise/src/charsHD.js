// ===== High-detail reference-style characters: crisp 2K faces, big outlined eyes, 3D cartoon hands, clothing details =====
BOIL.value = 0;
function drawFaceHD(g, e, o) {
  const S = 2, cx = 512 * S, cy = 262 * S, W2 = 1024 * S, H2 = 512 * S;
  g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = '#fbfaf5'; g.fillRect(0, 0, W2, H2);
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
  const armM = flat(o.arm ?? 0x15111b), legM = flat(0x15111b), handM = flat(0xfbfaf5);
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
