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
def trickle(d):
    n = int(d * SR); out = np.zeros(n)
    for k in range(int(d * 18)): f0 = 900 + rng.random() * 1400; m = int(0.05 * SR); tt = np.arange(m) / SR; b = np.sin(2 * np.pi * (f0 + f0 * 0.8 * tt / 0.05) * tt) * np.sin(np.pi * tt / 0.05) ** 2; i = int(rng.random() * (n - m)); out[i:i + m] += b * (0.3 + 0.7 * rng.random())
    return out / (np.abs(out).max() + 1e-9)
tw = wf(0, 'while') - 0.1; add(0.3, trickle(tw - 0.5), 0.25)                       # water pouring into a bowl
for q in range(6): add(CUT(1) + 0.15 + q * 0.18, hit('impactMetal_light_00%d' % (q % 5), 1.6), 0.18)   # sword on the grindstone
add(wf(1, 'he') + 0.2, trickle(1.2), 0.2)
if not END:
    for q in range(5): add(CUT(4) + 0.2 + q * 0.5, hit('impactPlate_light_00%d' % (q % 5), 1.2), 0.18)        # bowls set down
    add(wf(7, 'puddle') - 0.4, hit('impactGeneric_light_001'), 0.0)
    tj = wf(10, 'he') - 0.1; add(tj, hit('impactWood_medium_001', 0.8), 0.45)
    def shiver(d):
        n = int(d * SR); tt = np.arange(n) / SR; return np.sin(2 * np.pi * 520 * tt) * (0.5 + 0.5 * np.sin(2 * np.pi * 11 * tt)) * np.sin(np.pi * tt / d) ** 0.5
    add(CUT(11) + 0.2, shiver(CUT(13) - CUT(11) - 0.3), 0.07)
    for q in range(int((CUT(15) - CUT(13)) / 0.9)): add(CUT(13) + 0.3 + q * 0.9, hit('impactMining_00%d' % (q % 5), 0.9), 0.35)   # pickaxes
    add(CUT(15) + 0.2, shiver(1.8), 0.06)
    for q in range(3): add(CUT(16) + 0.6 + q * 0.5, hit('impactSoft_medium_00%d' % q, 0.7), 0.25)            # truck rumble
    tp = wf(17, 'and') - 0.1
    for q in range(int((tp - CUT(17)) / 0.35)): add(CUT(17) + 0.1 + q * 0.35, hit('impactMining_00%d' % (q % 5), 1.1), 0.35)    # digging
    add(tp + 0.2, trickle(CUT(18) - tp - 0.2), 0.35)
    add(CUT(18) + 0.4, trickle(1.8), 0.5); add(CUT(18) + 0.4, hit('impactSoft_heavy_001', 0.7), 0.5)
m, _ = librosa.load('../dlmusic/Cool_Vibes.mp3', sr=SR, mono=True); m = m[:N] if len(m) >= N else np.pad(m, (0, N - len(m)))
i = int(0.5 * SR); m[:i] *= np.linspace(0, 1, i); o = int(1.0 * SR); m[-o:] *= np.linspace(1, 0, o)
v, _ = librosa.load('vo.wav', sr=SR, mono=True); vo = np.zeros(N); vo[:min(N, len(v))] = v[:N]
rms = lambda x: np.sqrt((x[np.abs(x) > 1e-3] ** 2).mean()); mg = rms(vo) / rms(m) * 10 ** (-19 / 20)
env = lp(np.abs(vo), int(0.1 * SR)); duck = 1 - 0.3 * np.clip(env / 0.08, 0, 1)
mix = vo + m * mg * duck + sfx * 0.35 * rms(vo) / 0.1; o = int(0.3 * SR); mix[-o:] *= np.linspace(1, 0, o)
mix *= 0.89 / np.abs(mix).max(); sf.write('mix.wav', mix, SR); print('ok', DUR)
