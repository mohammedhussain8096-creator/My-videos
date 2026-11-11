"""Soundtrack: narration + 'Investigations' (Kevin MacLeod, CC-BY 4.0) + Kenney CC0 effects."""
import json, re, sys, wave, numpy as np, librosa, soundfile as sf
SR = 44100; END = float(sys.argv[1]) if len(sys.argv) > 1 else None
T = json.load(open('timing.json')); Ls = T['lines']; DUR = END or T['voEnd'] + 0.9; N = int(DUR * SR); K = '../dlsfx/'; rng = np.random.default_rng(3)
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
def bubbles(d):
    m = int(d * SR); out = np.zeros(m)
    for k in range(int(d * 7)):
        t0 = rng.random() * (d - 0.15); f0 = 250 + rng.random() * 500; n = int(0.09 * SR); tt = np.arange(n) / SR
        b = np.sin(2 * np.pi * (f0 + f0 * 1.5 * tt / 0.09) * tt) * np.sin(np.pi * tt / 0.09) ** 2; i = int(t0 * SR); out[i:i + n] += b * (0.4 + 0.6 * rng.random())
    return out / (np.abs(out).max() + 1e-9)
t0 = wf(0, 'bent') - 0.25
add(t0, load('sci-fi-sounds/Audio/doorOpen_001.ogg', 0.5), 0.6)                         # pipe creaks as it bends
add(t0 + 0.95, load('impact-sounds/Audio/impactMetal_light_001.ogg', 0.8), 0.45)        # settles
tb = wf(0, 'and') - 0.08; add(tb + 0.15, load('interface-sounds/Audio/error_004.ogg', 0.7), 0.3)  # sad peg honk
s1 = CUT(1)
for q in range(6): add(s1 + 0.2 + q * 0.39, load(f'impact-sounds/Audio/footstep_concrete_00{q % 5}.ogg'), 0.4)
tc = wf(1, 'where') - 0.1; add(tc + 0.9, bubbles(1.8), 0.35)
if len(Ls) > 2: tu = wf(2, 'and') - 0.1; add(tu - 0.3, bubbles(2.6), 0.4)

def tone_sweep(f0, f1, d, vib=0, vr=0):
    n = int(d * SR); tt = np.arange(n) / SR; f = f0 * (f1 / f0) ** (tt / d) + vib * np.sin(2 * np.pi * vr * tt) * np.exp(-tt * 3)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) ** 0.6
def hiss(d, rise=True):
    n = int(d * SR); x = rng.standard_normal(n); x = x - lp(x, 4); e = np.linspace(0.1, 1, n) if rise else np.linspace(1, 0, n) ** 2; return x / (np.abs(x).max() + 1e-9) * e
def signdrop(t):
    add(t, load('impact-sounds/Audio/footstep_wood_002.ogg', 0.6), 0.7)
    for q in range(3): add(t + 0.12 + q * 0.16, load('impact-sounds/Audio/impactMetal_light_00%d.ogg' % q, 1.3), 0.25 - q * 0.06)
if len(Ls) > 14 and not END:
    add(wf(3, 'fish') - 0.08, load('impact-sounds/Audio/impactGeneric_light_001.ogg'), 0.5)
    tcat = wf(3, 'cat') - 0.1; add(tcat + 0.25, tone_sweep(820, 520, 0.45, 30, 9) * 0.8 + tone_sweep(1640, 1040, 0.45) * 0.25, 0.35)       # offended meow
    add(wf(4, 'wiggle') - 0.05, tone_sweep(300, 300, 0.6, 120, 11), 0.3)                                                               # springy wiggle
    ts = wf(4, 'like') - 0.08
    for q in range(2): add(ts + 0.3 + q * 0.6, tone_sweep(150, 105, 0.45), 0.3)                                                        # snore
    add(CUT(5) + 0.3, hiss(0.9), 0.3)                                                                                                  # boss steaming
    add(wf(5, 'bent') - 0.25, load('impact-sounds/Audio/impactMetal_heavy_001.ogg'), 0.45)
    add(wf(6, 'fired') - 0.08, load('impact-sounds/Audio/impactMetal_heavy_003.ogg', 0.8), 0.5)
    for q in range(4): add(wf(6, 'fired') + 0.45 + q * 0.42, load(f'impact-sounds/Audio/footstep_concrete_00{q}.ogg', 0.85), 0.3)
    signdrop(wf(6, 'and') - 0.08 + 0.3)
    add(CUT(7) + 0.2, bubbles(3.2), 0.4); add(CUT(7) + 0.3, hiss(2.6) * 0.5, 0.18)
    add(wf(8, 'reeked') - 0.05, load('interface-sounds/Audio/error_004.ogg', 0.7), 0.3); add(wf(8, 'even') + 0.5, load('interface-sounds/Audio/error_006.ogg', 0.6), 0.28)
    add(wf(9, 'albie') - 0.05, load('interface-sounds/Audio/confirmation_002.ogg'), 0.35)
    add(CUT(10) + 0.3, bubbles(2.0), 0.3)
    add(wf(11, 'keeps') - 0.2, bubbles(1.2), 0.3); add(wf(11, 'water') + 0.1, load('interface-sounds/Audio/drop_002.ogg'), 0.45)
    add(wf(12, "can't") + 0.1, load('interface-sounds/Audio/drop_001.ogg'), 0.4); add(wf(12, 'cork') - 0.02, load('interface-sounds/Audio/pluck_001.ogg'), 0.5)
    add(wf(13, 'right') - 0.05, load('interface-sounds/Audio/select_002.ogg'), 0.35)
    signdrop(wf(14, 'bent') - 0.45 + 0.05); add(wf(14, 'only') + 0.3, load('interface-sounds/Audio/confirmation_001.ogg'), 0.4)
m, _ = librosa.load('../dlmusic/Bass_Walker.mp3', sr=SR, mono=True); m = m[:N] if len(m) >= N else np.pad(m, (0, N - len(m)))
i = int(0.5 * SR); m[:i] *= np.linspace(0, 1, i); o = int(0.8 * SR); m[-o:] *= np.linspace(1, 0, o)
w = wave.open('vo.wav'); v = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
v = np.interp(np.arange(0, len(v), 22050 / SR), np.arange(len(v)), v); vo = np.zeros(N); vo[:min(N, len(v))] = v[:N]; vo /= np.abs(vo).max()
rms = lambda x: np.sqrt((x[np.abs(x) > 1e-3] ** 2).mean()); mg = rms(vo) / rms(m) * 10 ** (-19 / 20)
env = lp(np.abs(vo), int(0.1 * SR)); duck = 1 - 0.35 * np.clip(env / 0.08, 0, 1)
mix = vo * 0.9 + m * mg * duck + sfx * 0.42; o = int(0.3 * SR); mix[-o:] *= np.linspace(1, 0, o)
mix = np.tanh(mix * 1.1) / np.tanh(1.1); mix *= 0.95 / np.abs(mix).max(); sf.write('mix.wav', mix, SR); print('ok', DUR)
