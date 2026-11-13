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
