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
hit = lambda n, r=1.0: load('impact-sounds/Audio/%s.ogg' % n, r)
def whoomp(d=0.9):
    n = int(d * SR); x = rng.standard_normal(n); x = lp(x, 30) - lp(x, 300); tt = np.arange(n) / SR; e = np.minimum(tt / 0.08, 1) * np.exp(-tt * 3.5); return x / (np.abs(x).max() + 1e-9) * e
add(1.8, whoomp(1.2), 0.6)
for q in range(int((CUT(2) - CUT(1)) / 0.22)): add(CUT(1) + 0.05 + q * 0.22, hit('footstep_grass_00%d' % (q % 5), 1.1), 0.22)
for q in range(int((CUT(2) - CUT(1)) / 0.5)): add(CUT(1) + 0.2 + q * 0.5, hit('impactMetal_light_00%d' % (q % 5), 1.4), 0.08)
for q in range(4): add(CUT(2) + 0.1 + q * 0.42, hit('footstep_grass_00%d' % q), 0.25)
if not END:
    ui = lambda n: load('interface-sounds/Audio/%s.ogg' % n); sci = lambda n: load('sci-fi-sounds/Audio/%s.ogg' % n)
    add(CUT(5) + 0.2, whoomp(1.0), 0.4)                                   # strip lit
    for q in range(3): add(wf(5, 'raked') + 0.05 + q * 0.38, ui('scratch_00%d' % (q + 1)), 0.18)   # raking the ash
    add(wf(6, 'not') + 0.6, hit('impactWood_light_001'), 0.22)            # last stalk falls
    add(CUT(13) + 0.1, sci('lowFrequency_explosion_000'), 0.45); add(CUT(13) + 0.1, whoomp(1.6), 0.5)   # fire reaches the farms
    add(CUT(14) + 0.15, whoomp(2.0), 0.4)                                 # roars through the wheat
    add(CUT(18) + 0.12 + 0.3, hit('impactSoft_heavy_001'), 0.45)          # CHOMP
    for j in range(4): add(CUT(19) + 0.5 + j * 0.42 + 0.28, hit('impactSoft_medium_00%d' % j), 0.3)   # eating the meal
    add(CUT(20) + 0.15, hit('impactPlate_light_002'), 0.25)               # plate pulled away
    tr = wf(21, 'runs') - 0.1; e = sci('engineCircular_001'); e = np.tile(e, 4)[:int((tr + 0.4 - CUT(21)) * SR)]; f = np.minimum(1, np.linspace(0, 6, len(e))) * np.minimum(1, np.linspace(5, 0, len(e))); add(CUT(21), e * f, 0.12)
    add(tr + 0.45, hit('impactMetal_light_002'), 0.22)                    # car clunks to a stop
m, _ = librosa.load('../dlmusic/Cool_Vibes.mp3', sr=SR, mono=True); m = m[:N] if len(m) >= N else np.pad(m, (0, N - len(m)))
i = int(0.5 * SR); m[:i] *= np.linspace(0, 1, i); o = int(1.0 * SR); m[-o:] *= np.linspace(1, 0, o)
v, _ = librosa.load('vo.wav', sr=SR, mono=True); vo = np.zeros(N); vo[:min(N, len(v))] = v[:N]
rms = lambda x: np.sqrt((x[np.abs(x) > 1e-3] ** 2).mean()); mg = rms(vo) / rms(m) * 10 ** (-19 / 20)
env = lp(np.abs(vo), int(0.1 * SR)); duck = 1 - 0.3 * np.clip(env / 0.08, 0, 1)
mix = vo + m * mg * duck + sfx * 0.35 * rms(vo) / 0.1; o = int(0.3 * SR); mix[-o:] *= np.linspace(1, 0, o)
mix *= 0.89 / np.abs(mix).max(); sf.write('mix.wav', mix, SR); print('ok', DUR)
