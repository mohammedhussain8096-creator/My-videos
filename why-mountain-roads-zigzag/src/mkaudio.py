"""Soundtrack: owner's narration (tightened to 59.3 s) + 'Cool Vibes' (Kevin MacLeod, CC-BY 4.0) + Kenney CC0 action sounds. No ambience beds."""
import sys, json, re, numpy as np, librosa, soundfile as sf
SR = 44100; END = float(sys.argv[1]) if len(sys.argv) > 1 else None
T = json.load(open('timing.json')); Ls = T['lines']; DUR = END or 60.0; N = int(DUR * SR); K = '../dlsfx/'; rng = np.random.default_rng(3)
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
def whoosh(d=0.9):
    n = int(d * SR); x = rng.standard_normal(n); return (lp(x, 6) - lp(x, 60)) * np.sin(np.linspace(0, np.pi, n)) ** 2 * 4
clop = lambda q: load('impact-sounds/Audio/footstep_wood_00%d.ogg' % (q % 5), 1.5)
tf = wf(0, 'and') - 0.15; add(tf - 0.1, whoosh(1.4), 0.25)                                        # drone dive
add(wf(0, 'morning') - 0.1, load('impact-sounds/Audio/impactWood_light_002.ogg') if False else load('impact-sounds/Audio/footstep_wood_002.ogg', 0.7), 0.5)  # barrels thud
for q in range(int((CUT(3) - CUT(1)) / 0.38)): add(CUT(1) + 0.1 + q * 0.38, clop(q), 0.22)       # slow hoofbeats on the old road
if not END:
    hit = lambda n, r=1.0: load('impact-sounds/Audio/%s.ogg' % n, r)
    tb = wf(4, 'blasted') + 0.15; add(tb, hit('impactMining_003', 0.6), 0.9); add(tb + 0.25, hit('impactMining_001', 0.7), 0.6)
    for q in range(5): add(tb + 0.3 + q * 0.18, hit('impactMining_00%d' % (q % 5), 1.1), 0.25)
    for q in range(int((CUT(8) - CUT(6)) / 0.42)): add(CUT(6) + 0.1 + q * 0.42, clop(q), 0.18)
    for q in range(int((CUT(9) - CUT(8)) / 0.2)): add(CUT(8) + q * 0.2, clop(q), 0.22)
    add(wf(9, 'burned') - 0.05, hit('impactMetal_medium_001', 0.7), 0.35)
    for q in range(4): add(CUT(11) + 0.2 + q * 0.45, hit('footstep_snow_00%d' % q), 0.3)
    add(wf(11, 'sent') - 0.05, hit('impactWood_medium_002', 0.8), 0.5)
    ts = wf(14, 'on', 2) - 0.05; add(ts + 0.1, whoosh(0.9), 0.12)
    for q in range(3): add(wf(14, 'on') + 0.1 + q * 0.35, hit('footstep_wood_00%d' % q), 0.3)
    sc = CUT(15) + 0.5; n = int(1.6 * SR); tt = np.arange(n) / SR; screech = np.sin(2 * np.pi * (2200 + 300 * np.sin(2 * np.pi * 7 * tt)) * tt) * np.sin(np.pi * tt / 1.6) ** 0.5; screech += (rng.standard_normal(n) - lp(rng.standard_normal(n), 3)) * 0.3; add(sc, screech / np.abs(screech).max(), 0.18)
    add(CUT(16) + 0.1, whoosh(2.2), 0.2)
    tc = wf(17, 'went') - 0.25 + 0.25; add(tc, hit('impactWood_heavy_000'), 1.0); add(tc + 0.05, hit('impactPlank_medium_002'), 0.8); add(tc + 0.12, hit('impactWood_heavy_003', 0.8), 0.7)
    for q in range(8): add(tc + 0.5 + q * 0.17, hit('impactWood_medium_00%d' % (q % 5), 0.9 + q * 0.03), 0.4)
    for q in range(int((CUT(19) - CUT(18)) / 0.5)): add(CUT(18) + 0.1 + q * 0.5, hit('footstep_snow_00%d' % (q % 5)), 0.18)
m, _ = librosa.load('../dlmusic/Cool_Vibes.mp3', sr=SR, mono=True); m = m[:N] if len(m) >= N else np.pad(m, (0, N - len(m)))
i = int(0.5 * SR); m[:i] *= np.linspace(0, 1, i); o = int(1.0 * SR); m[-o:] *= np.linspace(1, 0, o)
v, _ = librosa.load('vo.wav', sr=SR, mono=True); vo = np.zeros(N); vo[:min(N, len(v))] = v[:N]
rms = lambda x: np.sqrt((x[np.abs(x) > 1e-3] ** 2).mean()); mg = rms(vo) / rms(m) * 10 ** (-19 / 20)
env = lp(np.abs(vo), int(0.1 * SR)); duck = 1 - 0.3 * np.clip(env / 0.08, 0, 1)
mix = vo + m * mg * duck + sfx * 0.35 * rms(vo) / 0.1; o = int(0.3 * SR); mix[-o:] *= np.linspace(1, 0, o)
mix *= 0.89 / np.abs(mix).max(); sf.write('mix.wav', mix, SR); print('ok', DUR)
