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
