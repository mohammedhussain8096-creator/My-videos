"""Soundtrack: owner's narration (tightened to 59.3 s) + 'Cool Vibes' (Kevin MacLeod, CC-BY 4.0) + Kenney CC0 action sounds. No ambience beds."""
import sys, json, re, numpy as np, librosa, soundfile as sf
SR = 44100; END = float(sys.argv[1]) if len(sys.argv) > 1 else None
T = json.load(open('timing.json')); Ls = T['lines']; DUR = END or 59.2; N = int(DUR * SR); K = '../dlsfx/'; rng = np.random.default_rng(3)
def wf(i, s, nth=1):
    n = 0
    for w in Ls[i]['words']:
        if re.sub(r"[^a-z0-9']", '', w['w'].lower()).startswith(s):
            n += 1
            if n == nth: return w['s']
    return Ls[i]['s']
CUT = lambda i: 0 if i == 0 else Ls[i]['s'] - 0.1
def load(p, rate=1.0):
    a, sr = librosa.load(K + p, sr=SR, mono=True)
    if rate != 1.0: a = librosa.resample(a, orig_sr=int(SR * rate), target_sr=SR)
    return a / (np.abs(a).max() + 1e-9)
def lp(x, k): c = np.cumsum(np.concatenate([np.zeros(k), x])); return (c[k:] - c[:-k]) / k
sfx = np.zeros(N)
def add(t, x, g=1.0):
    i = int(t * SR)
    if 0 <= i < N: x = x[:N - i]; sfx[i:i + len(x)] += x * g
hit = lambda n, r=1.0: load('impact-sounds/Audio/%s.ogg' % n, r)
def whoomp(d=0.9):
    n = int(d * SR); x = rng.standard_normal(n); x = lp(x, 30) - lp(x, 300); tt = np.arange(n) / SR; e = np.minimum(tt / 0.08, 1) * np.exp(-tt * 3.5); return x / (np.abs(x).max() + 1e-9) * e
ui = lambda n: load('interface-sounds/Audio/%s.ogg' % n); sci = lambda n: load('sci-fi-sounds/Audio/%s.ogg' % n)
ta = wf(0, 'and') - 0.1
add(0.05, ui('click_002'), 0.15)                                                   # flashlight on
for q in range(int((ta - 0.2) / 0.42)): add(0.2 + q * 0.42, hit('footstep_wood_00%d' % (q % 5)), 0.22)   # boots on the lab floor
for q in range(int((CUT(3) - CUT(2)) / 0.33)): add(CUT(2) + 0.05 + q * 0.33, hit('impactMetal_heavy_00%d' % (q % 5), 1.3), 0.07)   # tank tracks
if not END:
    add(wf(5, 'finished') - 0.15 + 0.35, hit('impactMetal_heavy_001'), 0.3)                        # cell bars slam
    add(wf(6, 'soldiers') - 0.1 + 0.3, hit('impactSoft_medium_002'), 0.4)                           # shovel bites the dirt
    for q in range(3): add(CUT(7) + 0.3 + q * 0.12, hit('impactPlank_medium_00%d' % q, 1.3), 0.1)   # bricks slid back in
    ts = wf(7, 'smash') - 0.05; add(ts, hit('impactWood_heavy_002'), 0.45); add(ts + 0.02, hit('impactPlate_heavy_001'), 0.25)   # SMASH
    add(wf(8, 'grabbed') + 0.05, hit('impactGlass_light_001'), 0.2)                                 # grabs the bottle
    td = CUT(10) + 0.35; add(td + 0.42, ui('drop_002'), 0.35); add(td + 0.54, ui('drop_003'), 0.3)   # PLOP, PLOP
    add(wf(11, 'on', 1) - 0.1, hit('impactGlass_light_003'), 0.18)                                   # jar set on the shelf
    add(CUT(12) + 0.08, hit('impactWood_heavy_000'), 0.5)                                            # door BANG
    for q in range(4): add(CUT(12) + 0.3 + q * 0.3, hit('footstep_wood_00%d' % q), 0.2)
    order = [4, 7, 1, 10, 3, 9, 0, 6, 11, 2, 8, 5]
    for o in range(12): add(CUT(13) + 0.18 + o * 0.11, hit('impactWood_light_00%d' % (o % 5)), 0.12)   # drawers yanked
    tw = wf(14, 'walked') - 0.25
    for q in range(3): add(tw + 0.3 + q * 0.4, hit('footstep_wood_00%d' % (q + 1)), 0.16)           # walks away
    tsg = wf(17, 'sugar') - 0.1; add(tsg + 0.42, ui('drop_003'), 0.3)                                  # sugar drops in
    for q in range(3): add(tsg + 0.9 + q * 0.42, hit('impactGlass_light_00%d' % q, 1.2), 0.06)      # spoon clinks
    add(wf(18, 'brand') - 0.1, hit('impactBell_heavy_000'), 0.14)                                     # new medals
    for q in range(4): add(CUT(19) + 0.1 + q * 0.45, hit('footstep_wood_00%d' % q), 0.14)
m, _ = librosa.load('../dlmusic/Cool_Vibes.mp3', sr=SR, mono=True); m = m[:N] if len(m) >= N else np.pad(m, (0, N - len(m)))
i = int(0.5 * SR); m[:i] *= np.linspace(0, 1, i); o = int(1.0 * SR); m[-o:] *= np.linspace(1, 0, o)
v, _ = librosa.load('vo.wav', sr=SR, mono=True); vo = np.zeros(N); vo[:min(N, len(v))] = v[:N]
rms = lambda x: np.sqrt((x[np.abs(x) > 1e-3] ** 2).mean()); mg = rms(vo) / rms(m) * 10 ** (-19 / 20)
env = lp(np.abs(vo), int(0.1 * SR)); duck = 1 - 0.3 * np.clip(env / 0.08, 0, 1)
mix = vo + m * mg * duck + sfx * 0.35 * rms(vo) / 0.1; o = int(0.3 * SR); mix[-o:] *= np.linspace(1, 0, o)
mix *= 0.89 / np.abs(mix).max(); sf.write('mix.wav', mix, SR); print('ok', DUR)
