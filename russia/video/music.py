"""Original background music, composed in code (no samples; free to use).
Style target from the reference: a light, steady documentary pulse (~80 BPM) sitting quietly under the
voice. Flavour: Russian - D natural minor, low string pad, a plucked balalaika-like tremolo lead,
plucked bass and a soft low drum. Writes OUT_DIR/music.wav at least as long as the narration."""
import json, os, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('OUT_DIR', os.path.join(HERE, 'build'))
SR = 48000; BPM = 80.0; BEAT = 60 / BPM; BAR = 4 * BEAT
rng = np.random.default_rng(11)
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
SCALE = [0, 2, 3, 5, 7, 8, 10]; ROOT = 62           # D natural minor
def note(deg, octv=0):
    o, i = divmod(deg, 7); return ROOT + SCALE[i] + 12 * (o + octv)
PROG = [(0, 'm'), (5, 'M'), (2, 'M'), (6, 'M'), (0, 'm'), (3, 'm'), (4, 'M'), (4, 'M')]   # Dm Bb F C Dm Gm A A

def pad(freqs, dur):
    t = np.arange(int(dur * SR)) / SR; s = np.zeros_like(t)
    for f in freqs:
        for det in (-0.12, 0.0, 0.12):
            ph = rng.uniform(0, 6.28)
            s += np.sin(2 * np.pi * (f + det) * t + ph) * 0.5 + np.sin(2 * np.pi * 2 * (f + det) * t + ph) * 0.12
    env = np.minimum(1, t / 0.9) * np.minimum(1, (dur - t) / 0.9)
    return s * env * 0.05

def pluck(f, dur, vel=1.0):
    t = np.arange(int(dur * SR)) / SR; s = np.zeros_like(t)
    for h in range(1, 7): s += np.sin(2 * np.pi * f * h * t) * np.exp(-t * (3 + h * 2.5)) / h
    return s * vel * 0.16 * np.minimum(1, t / 0.003)

def trem(f, dur, vel=1.0):     # balalaika tremolo: fast repeated plucks
    out = np.zeros(int(dur * SR)); step = 0.09
    for k in range(int(dur / step)):
        p = pluck(f, min(0.4, dur - k * step), vel * (0.55 + 0.45 * (k % 2)))
        i = int(k * step * SR); out[i:i + len(p)] += p[: len(out) - i]
    return out * np.minimum(1, (dur - np.arange(len(out)) / SR) / 0.2).clip(0)

def drum(vel=1.0):
    t = np.arange(int(0.5 * SR)) / SR
    return np.sin(2 * np.pi * (48 + 40 * np.exp(-t * 25)) * t) * np.exp(-t * 7) * 0.35 * vel

def chord(deg, q):
    r = note(deg, -1)
    third = r + (3 if q == 'm' else 4)
    return [hz(r), hz(third), hz(r + 7)]

def section(bars, lead=True, drums=True, seed=0):
    n = int(bars * BAR * SR); mix = np.zeros(n)
    def put(sig, t):
        i = int(t * SR); j = min(n, i + len(sig))
        if i < n: mix[i:j] += sig[: j - i]
    r = np.random.default_rng(seed)
    for b in range(bars):
        deg, q = PROG[b % len(PROG)]
        t0 = b * BAR
        put(pad(chord(deg, q), BAR + 0.5), t0)
        put(pluck(hz(note(deg, -2)), 1.2, 1.2), t0); put(pluck(hz(note(deg, -2)), 1.0, 0.8), t0 + 2.5 * BEAT)
        if drums:
            put(drum(1.0), t0); put(drum(0.5), t0 + 1.5 * BEAT); put(drum(0.8), t0 + 2 * BEAT)
        if lead and b % 2 == 0:
            mel = [deg + r.choice([0, 2, 4]), deg + r.choice([1, 2, 4]), deg + r.choice([4, 2, 0])]
            for k, m in enumerate(mel):
                put(trem(hz(note(m, 0)), 1.6 * BEAT, 0.7), t0 + k * 1.33 * BEAT * 2)
    return mix

def main():
    total = json.load(open(os.path.join(OUT, 'timing.json')))['total'] + 3
    parts = [section(8, lead=False, drums=False, seed=1), section(16, seed=2), section(16, lead=False, seed=3), section(16, seed=4)]
    piece = np.concatenate(parts)
    loop = np.concatenate(parts[1:]); xs = [piece]
    while sum(len(x) for x in xs) < total * SR: xs.append(loop)
    out = np.concatenate(xs)[: int(total * SR)]
    out = out / (np.abs(out).max() + 1e-9) * 0.7
    fade = int(3 * SR); out[-fade:] *= np.linspace(1, 0, fade)
    with wave.open(os.path.join(OUT, 'music.wav'), 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
        wf.writeframes((out * 32767).astype(np.int16).tobytes())
    print('music', round(len(out) / SR, 1), 's')

if __name__ == '__main__':
    main()
