"""Soundtrack: narration + 'Cool Vibes' (Kevin MacLeod, CC-BY 4.0) + Kenney CC0 effects + synthesized ambience."""
import sys, json, re, wave, numpy as np, librosa, soundfile as sf
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
def seg(t0, t1, x):  # place a looped bed between t0 and t1 with fades
    n = int((t1 - t0) * SR); x = np.tile(x, n // len(x) + 1)[:n].copy(); f = int(0.15 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f); add(t0, x, 1.0)
def murmur(d):
    n = int(d * SR); x = lp(rng.standard_normal(n), 25) - lp(rng.standard_normal(n), 140); tt = np.arange(n) / SR; e = 0.7 + 0.3 * np.sin(2 * np.pi * 0.7 * tt) * np.sin(2 * np.pi * 1.9 * tt); return x / (np.abs(x).max() + 1e-9) * e
def crackle(d):
    n = int(d * SR); x = np.zeros(n); idx = rng.integers(0, n, int(d * 40)); x[idx] = rng.standard_normal(len(idx)); x = x - lp(x, 4); y = lp(rng.standard_normal(n), 200); return (x / (np.abs(x).max() + 1e-9)) * 0.7 + y / (np.abs(y).max() + 1e-9) * 0.4
def bubbles(d):
    m = int(d * SR); out = np.zeros(m)
    for k in range(int(d * 6)):
        t0 = rng.random() * (d - 0.15); f0 = 180 + rng.random() * 300; n = int(0.1 * SR); tt = np.arange(n) / SR; b = np.sin(2 * np.pi * (f0 + f0 * 1.4 * tt / 0.1) * tt) * np.sin(np.pi * tt / 0.1) ** 2; i = int(t0 * SR); out[i:i + n] += b * (0.4 + 0.6 * rng.random())
    return out / (np.abs(out).max() + 1e-9)
def crickets(d):
    n = int(d * SR); tt = np.arange(n) / SR; c = np.sin(2 * np.pi * 4300 * tt) * (np.sin(2 * np.pi * 28 * tt) > 0.6) * (np.sin(2 * np.pi * 0.9 * tt) > -0.1); return c * 0.5
def sniff():
    n = int(0.22 * SR); x = rng.standard_normal(n); x = x - lp(x, 3); e = np.sin(np.linspace(0, np.pi, n)) ** 2; return x / (np.abs(x).max() + 1e-9) * e
tw = wf(1, 'people') - 0.1; s2 = CUT(2); s1 = CUT(1)
add(wf(0, 'and') + 0.3, load('impact-sounds/Audio/impactGlass_light_002.ogg'), 0.4)   # coin glint
add(s1 + 0.1, bubbles(tw - s1), 0.35)
add(tw + 0.8 * (s2 - tw), load('impact-sounds/Audio/impactWood_heavy_000.ogg') if False else load('impact-sounds/Audio/footstep_wood_002.ogg', 0.7), 0.7)   # bonk into the post
for q in range(3): add(tw + 0.15 + q * 0.42, load('impact-sounds/Audio/footstep_concrete_00%d.ogg' % q), 0.25)
ts = wf(2, 'sniffing') - 0.15
for q in range(3): add(ts + 0.1 + q * 0.34, sniff(), 0.35)
if not END:
    clink = lambda r=1.0: load('impact-sounds/Audio/impactGlass_light_002.ogg', r)
    for q in range(2): add(wf(3, 'one') + q * 0.35, sniff(), 0.35); add(wf(3, 'two') + q * 0.35, sniff(), 0.35)
    add(CUT(4) + 0.1, load('sci-fi-sounds/Audio/doorOpen_000.ogg'), 0.45)
    for q in range(4): add(CUT(4) + 0.3 + q * 0.3, load('impact-sounds/Audio/footstep_wood_00%d.ogg' % q, 1.1), 0.35)
    add(wf(4, 'grabbed') - 0.05, load('impact-sounds/Audio/impactGeneric_light_002.ogg', 0.8), 0.5)
    add(wf(5, 'bent') - 0.05, clink(1.2), 0.35)
    for q in range(int((CUT(7) - CUT(6)) / 0.33)): add(CUT(6) + 0.1 + q * 0.33, load('impact-sounds/Audio/footstep_concrete_00%d.ogg' % (q % 5)), 0.22)
    add(wf(7, 'then') + 0.2, clink(1.0), 0.3)
    add(wf(9, 'clink') - 0.05, clink(0.95), 0.6); add(wf(9, 'clink', 2) - 0.05, clink(1.05), 0.6)
    add(wf(11, 'even') - 0.1, load('impact-sounds/Audio/impactWood_heavy_002.ogg') if False else load('impact-sounds/Audio/footstep_wood_003.ogg', 0.6), 0.8)
    add(wf(12, 'red') - 0.05, load('interface-sounds/Audio/error_006.ogg', 0.7), 0.3)
    add(CUT(13) + 0.2, bubbles(1.5), 0.25); add(wf(13, 'charge') + 0.3, load('interface-sounds/Audio/pluck_002.ogg'), 0.45)
    tb = wf(14, 'and') - 0.08
    add(CUT(14) + 0.3, clink(1.1), 0.3); add(CUT(14) + 1.0, clink(1.15), 0.3)
    for q in range(3): add(tb + 0.3 + q * 0.4, clink(0.9 + q * 0.08), 0.45)
m, _ = librosa.load('../dlmusic/Cool_Vibes.mp3', sr=SR, mono=True); m = m[:N] if len(m) >= N else np.pad(m, (0, N - len(m)))
i = int(0.5 * SR); m[:i] *= np.linspace(0, 1, i); o = int(1.0 * SR); m[-o:] *= np.linspace(1, 0, o)
w = wave.open('vo.wav'); v = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
v = np.interp(np.arange(0, len(v), 22050 / SR), np.arange(len(v)), v); vo = np.zeros(N); vo[:min(N, len(v))] = v[:N]; vo /= np.abs(vo).max()
rms = lambda x: np.sqrt((x[np.abs(x) > 1e-3] ** 2).mean()); mg = rms(vo) / rms(m) * 10 ** (-19 / 20)
env = lp(np.abs(vo), int(0.1 * SR)); duck = 1 - 0.3 * np.clip(env / 0.08, 0, 1)
mix = vo * 0.9 + m * mg * duck + sfx * 0.4; o = int(0.3 * SR); mix[-o:] *= np.linspace(1, 0, o)
mix = np.tanh(mix * 1.08) / np.tanh(1.08); mix *= 0.95 / np.abs(mix).max(); sf.write('mix.wav', mix, SR); print('ok', DUR)
