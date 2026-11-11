"""Soundtrack: narration + 'Carefree' (Kevin MacLeod, CC-BY 4.0) + Kenney CC0 effects."""
import sys, json, re, wave, numpy as np, librosa, soundfile as sf
SR = 44100; T = json.load(open('timing.json')); Ls = T['lines']; DUR = T['voEnd'] + 0.9; N = int(DUR * SR); K = '../dlsfx/'; rng = np.random.default_rng(3)
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
I = lambda n: 'interface-sounds/Audio/' + n + '.ogg'
def lp(x, k): c = np.cumsum(np.concatenate([np.zeros(k), x])); return (c[k:] - c[:-k]) / k
sfx = np.zeros(N)
def add(t, x, g=1.0):
    i = int(t * SR)
    if 0 <= i < N: x = x[:N - i]; sfx[i:i + len(x)] += x * g
def buzz(d=0.5):
    n = int(d * SR); tt = np.arange(n) / SR; return np.sign(np.sin(2 * np.pi * 150 * tt)) * (np.sin(2 * np.pi * 9 * tt) > -0.2) * np.sin(np.pi * tt / d) ** 0.3 * 0.5
def beep(f, d=0.14): n = int(d * SR); tt = np.arange(n) / SR; return np.sin(2 * np.pi * f * tt) * np.sin(np.pi * tt / d) ** 0.5
def whoosh(d=0.6): n = int(d * SR); x = rng.standard_normal(n); return (lp(x, 6) - lp(x, 60)) * np.sin(np.linspace(0, np.pi, n)) ** 2 * 4
add(wf(0, 'belonged') - 0.08, load(I('confirmation_002')), 0.3)
tg = wf(2, 'google') - 0.5
for q in range(10): add(tg + q * 0.13, load(I('click_00%d' % (1 + q % 5)), 0.9 + 0.05 * (q % 3)), 0.4)
add(wf(3, 'available') - 0.1, load(I('confirmation_002')), 0.45); add(wf(3, 'twelve') - 0.1, load(I('select_003')), 0.35)
add(wf(4, 'glitch') - 0.3, load(I('question_002')), 0.3)
tc = wf(4, 'buy') - 0.05; add(tc, load(I('click_003')), 0.6); add(tc + 0.45, load(I('confirmation_004')), 0.45)
add(CUT(5) + 0.3, buzz(0.55), 0.35)
tb = wf(5, 'his', 2) - 0.08; d = (CUT(6) - 0.3) - (tb + 0.1)
for q in range(13): add(tb + 0.1 + q * d / 14, load(I('select_00%d' % (1 + q % 6)), 1.0 + 0.04 * q), 0.28)
t0 = CUT(6); t1 = wf(7, 'order') - 0.1
for q in range(int((t1 - t0) / 0.25)): add(t0 + q * 0.25, load(I('tick_00%d' % (1 if q % 2 else 2))), 0.3)
add(wf(6, 'keys') - 0.05, load('impact-sounds/Audio/impactBell_heavy_000.ogg', 1.6), 0.25)
ts = wf(7, 'cancelled') - 0.05; add(ts, load('impact-sounds/Audio/impactMetal_heavy_002.ogg', 0.8), 0.55); add(ts + 0.2, load(I('error_003'), 0.8), 0.35)
tb8 = wf(8, 'he', 2) - 0.08
for q in range(7): add(tb8 + q * 0.11, load(I('click_00%d' % (1 + q % 5))), 0.3)
add(tb8 + 0.9, whoosh(0.7), 0.6)
tc8 = wf(8, 'exactly') - 0.2
for q in range(3): add(tc8 + 0.05 + q * 0.16, beep(880 if q % 2 == 0 else 660), 0.22)
add(tc8 + 0.9, load(I('confirmation_001')), 0.4)
tp = wf(9, 'pays') - 0.1; add(CUT(9) + 0.4, load(I('scroll_003')), 0.3); add(tp + 0.25, load(I('pluck_001')), 0.5); add(tp + 0.35, load(I('glass_002')), 0.4)
add(wf(10, 'six') - 0.4, load(I('maximize_003')), 0.4)
for q, w in enumerate([wf(11, 'six'), wf(11, 'zero'), wf(11, 'zero', 2), wf(11, 'six', 2), wf(11, 'one'), wf(11, 'three')]): add(w + 0.05, load(I('tick_004'), 0.9 + q * 0.05), 0.4)
tf = wf(11, 'it') - 0.1
for q in range(6): add(tf + q * 0.09 + 0.12, load(I('switch_00%d' % (1 + q)), 1.0), 0.4)
add(tf + 0.9, load(I('confirmation_003')), 0.4)
add(CUT(12) + 0.4, load(I('confirmation_002'), 1.1), 0.3)
td = CUT(13) + 0.25; add(td, load(I('maximize_006')), 0.45)
for q in range(5): add(td + 0.3 + q * 0.09, load(I('glass_00%d' % (1 + q)), 1.2), 0.3)
add(wf(14, 'and') - 0.08, load(I('confirmation_001')), 0.4)
m, _ = librosa.load('../dlmusic/' + sys.argv[1] + '.mp3', sr=SR, mono=True, offset=float(sys.argv[3]) if len(sys.argv) > 3 else 0); m = m[:N] if len(m) >= N else np.pad(m, (0, N - len(m)))
i = int(0.5 * SR); m[:i] *= np.linspace(0, 1, i); o = int(1.0 * SR); m[-o:] *= np.linspace(1, 0, o)
w = wave.open('vo.wav'); v = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
v = np.interp(np.arange(0, len(v), 22050 / SR), np.arange(len(v)), v); vo = np.zeros(N); vo[:min(N, len(v))] = v[:N]; vo /= np.abs(vo).max()
rms = lambda x: np.sqrt((x[np.abs(x) > 1e-3] ** 2).mean()); mg = rms(vo) / rms(m) * 10 ** (-19 / 20)
env = lp(np.abs(vo), int(0.1 * SR)); duck = 1 - 0.35 * np.clip(env / 0.08, 0, 1)
mix = vo * 0.9 + m * mg * duck + sfx * 0.4; o = int(0.3 * SR); mix[-o:] *= np.linspace(1, 0, o)
mix = np.tanh(mix * 1.1) / np.tanh(1.1); mix *= 0.95 / np.abs(mix).max(); sf.write(sys.argv[2], mix, SR); print('ok', DUR)
