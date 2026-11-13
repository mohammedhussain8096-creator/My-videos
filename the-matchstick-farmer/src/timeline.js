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
