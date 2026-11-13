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
