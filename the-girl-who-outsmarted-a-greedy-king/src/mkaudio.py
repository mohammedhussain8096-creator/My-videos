"""Soundtrack: the owner's own narration + 'Cool Vibes' (Kevin MacLeod, CC-BY 4.0) + Kenney CC0 effects."""
import sys, json, re, numpy as np, librosa, soundfile as sf
SR = 44100; END = float(sys.argv[1]) if len(sys.argv) > 1 else None
T = json.load(open('timing.json')); Ls = T['lines']; DUR = END or T['voEnd'] + 0.5; N = int(DUR * SR); K = '../dlsfx/'; rng = np.random.default_rng(3)
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
def saw(d=1.0):
    n = int(d * SR); tt = np.arange(n) / SR; x = rng.standard_normal(n); x = lp(x, 3) - lp(x, 12); e = np.abs(np.sin(2 * np.pi * 3.2 * tt)) ** 0.5; return x / (np.abs(x).max() + 1e-9) * e
def coinrain(d, dens=8):
    n = int(d * SR); out = np.zeros(n)
    for k in range(int(d * dens)): a = load('impact-sounds/Audio/impactGlass_light_00%d.ogg' % (k % 5), 0.8 + rng.random() * 0.5); i = int(rng.random() * (n - len(a) - 1)); out[i:i + len(a)] += a * (0.4 + 0.6 * rng.random())
    return out / (np.abs(out).max() + 1e-9)
clink = lambda r=1.0: load('impact-sounds/Audio/impactGlass_light_002.ogg', r)
# line 1: three coins
tp = wf(1, 'paid') - 0.1
for i in range(3): add(tp + 0.55 + i * 0.66, clink(1.0 + 0.1 * i), 0.5)
add(CUT(1) + 0.2, load('interface-sounds/Audio/scroll_002.ogg', 0.6), 0.3)        # rod slides
# line 2: whip to the palace, coin pile grows
tr = wf(2, 'so') - 0.1; add(tr - 0.15, load('sci-fi-sounds/Audio/forceField_000.ogg', 1.6)[:int(0.5 * SR)], 0.25)
add(tr + 0.1, coinrain(CUT(3) - tr - 0.2, 10), 0.45)
# line 3: noon; the saw
if len(Ls) > 3:
    th = wf(3, 'one') - 0.1; add(th + 0.3, saw(1.1), 0.45); add(th + 1.4, load('impact-sounds/Audio/impactWood_light_001.ogg') if False else load('impact-sounds/Audio/footstep_wood_003.ogg'), 0.5)
if len(Ls) > 6 and not END:
    def whoosh(d=0.6):
        n = int(d * SR); x = rng.standard_normal(n); return (lp(x, 6) - lp(x, 60)) * np.sin(np.linspace(0, np.pi, n)) ** 2 * 4
    def wind(d=3.0):
        n = int(d * SR); x = lp(rng.standard_normal(n), 300); e = np.sin(np.linspace(0, np.pi, n)) ** 0.7; return x / (np.abs(x).max() + 1e-9) * e
    def rumble(d=3.0):
        n = int(d * SR); x = lp(rng.standard_normal(n), 60); tt = np.arange(n) / SR; e = (0.6 + 0.4 * np.sin(2 * np.pi * 2.2 * tt)) * np.sin(np.linspace(0, np.pi, n)) ** 0.5; return x / (np.abs(x).max() + 1e-9) * e
    foot = lambda q, r=1.0: load('impact-sounds/Audio/footstep_concrete_00%d.ogg' % (q % 5), r)
    tk = wf(5, 'knot') - 0.05; add(tk + 0.2, load('interface-sounds/Audio/click_002.ogg'), 0.35)
    tw = wf(5, 'walked') - 0.1
    for q in range(5): add(tw + 0.1 + q * 0.42, foot(q, 1.15), 0.28)
    add(wf(6, 'forgot') - 0.05, load('impact-sounds/Audio/footstep_wood_001.ogg'), 0.4)                # ledger drops
    add(wf(9, 'wrapped') - 0.05, load('interface-sounds/Audio/scroll_004.ogg', 0.8), 0.3)
    add(CUT(10) + 0.3, load('sci-fi-sounds/Audio/doorOpen_001.ogg', 0.55), 0.3)                        # barrow squeak
    add(CUT(11) + 0.2, wind(5.0), 0.3); add(wf(11, 'brought') - 0.1, rumble(3.5), 0.35)
    add(wf(12, 'king') - 0.1, whoosh(0.5), 0.5)
    add(CUT(13) + 0.3, load('sci-fi-sounds/Audio/forceField_001.ogg', 1.4)[:int(1.6 * SR)], 0.25)   # the shadow reveal
    add(wf(16, 'stopped') + 0.1, load('interface-sounds/Audio/error_006.ogg', 0.7), 0.3)
    ts = wf(18, 'sawed') - 0.1; add(ts, saw(1.1), 0.5); add(ts + 1.15, load('impact-sounds/Audio/impactWood_heavy_001.ogg') if False else load('impact-sounds/Audio/impactMetal_heavy_001.ogg', 0.6), 0.5)
    add(wf(19, 'paid') - 0.05, coinrain(1.8, 9), 0.45)
m, _ = librosa.load('../dlmusic/Cool_Vibes.mp3', sr=SR, mono=True); m = m[:N] if len(m) >= N else np.pad(m, (0, N - len(m)))
i = int(0.5 * SR); m[:i] *= np.linspace(0, 1, i); o = int(1.0 * SR); m[-o:] *= np.linspace(1, 0, o)
v, _ = librosa.load('vo.wav', sr=SR, mono=True); vo = np.zeros(N); vo[:min(N, len(v))] = v[:N]; vo /= np.abs(vo).max()
rms = lambda x: np.sqrt((x[np.abs(x) > 1e-3] ** 2).mean()); mg = rms(vo) / rms(m) * 10 ** (-19 / 20)
env = lp(np.abs(vo), int(0.1 * SR)); duck = 1 - 0.3 * np.clip(env / 0.08, 0, 1)
mix = vo * 0.92 + m * mg * duck + sfx * 0.4; o = int(0.3 * SR); mix[-o:] *= np.linspace(1, 0, o)
mix = np.tanh(mix * 1.08) / np.tanh(1.08); mix *= 0.95 / np.abs(mix).max(); sf.write('mix.wav', mix, SR); print('ok', DUR)
