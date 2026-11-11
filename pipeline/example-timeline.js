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
