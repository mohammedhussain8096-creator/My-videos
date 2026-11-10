"""(Spain video: an original piece composed in code. E Phrygian dominant, the flamenco scale, over the Andalusian cadence
Am-G-F-E, with a plucked guitar-like lead and a soft rumba-style hand-drum pattern.)
Original background music for the video (composed in code, no samples, free to use).

Style target taken from the reference video's music: a light, steady pulse (~78 BPM), mid-range,
sitting quietly under the narration. Flavour: Egyptian, using the Hijaz scale on D with a plucked
oud-like lead, a soft pad, a plucked bass and a frame-drum rhythm (dum / tak).

Writes OUT_DIR/music.wav, long enough for the narration (the ~6-minute piece is varied and looped)."""
import os, wave
import numpy as np

OUT = os.environ.get('OUT_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build'))
SR = 32000
BPM = 84.0
BEAT = 60.0 / BPM
BAR = 4 * BEAT
rng_master = np.random.default_rng(7)

def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)

# E Phrygian dominant: E F G# A B C D
SCALE = [0, 1, 4, 5, 7, 8, 10]
ROOT = 64  # E4

def scale_note(deg, octave=0):
    o, i = divmod(deg, len(SCALE))
    return ROOT + SCALE[i] + 12 * (o + octave)

def pluck(f, dur, bright=1.0, vel=1.0):
    """oud-like pluck: harmonics that decay faster the higher they are, plus a tiny pick noise"""
    n = int(dur * SR); t = np.arange(n) / SR
    out = np.zeros(n, np.float32)
    for k in range(1, 9):
        if f * k > SR / 2.2: break
        amp = (1.0 / k ** 1.1) * (bright if k > 2 else 1.0)
        out += amp * np.sin(2 * np.pi * f * k * t + k) * np.exp(-t * (2.2 + 1.6 * k))
    a = min(n, int(0.004 * SR)); out[:a] *= np.linspace(0, 1, a)
    noise = np.random.default_rng(int(f)).normal(0, 1, min(n, int(0.01 * SR))) * 0.08
    out[:len(noise)] += noise * np.linspace(1, 0, len(noise))
    return out * vel

def pad(freqs, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    out = np.zeros(n, np.float32)
    for f in freqs:
        for det in (-0.12, 0.0, 0.11):
            ff = f * 2 ** (det / 12)
            # soft triangle-ish tone (odd harmonics, falling fast)
            for k, a in ((1, 1.0), (3, 0.11), (5, 0.04)):
                out += a * np.sin(2 * np.pi * ff * k * t + det * 10)
    env = np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.2)
    lfo = 0.85 + 0.15 * np.sin(2 * np.pi * 0.11 * t)
    return out * env * lfo / (len(freqs) * 3)

def dum(vel=1.0):
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 95 * np.exp(-t * 6) + 55
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 9)
    s[:int(0.006 * SR)] += np.random.default_rng(1).normal(0, 0.4, int(0.006 * SR))
    return s.astype(np.float32) * vel

def tak(vel=1.0):
    n = int(0.12 * SR); t = np.arange(n) / SR
    nz = np.random.default_rng(2).normal(0, 1, n)
    nz = nz - np.concatenate([[0], nz[:-1]]) * 0.6           # brighten
    s = nz * np.exp(-t * 55) * 0.5 + np.sin(2 * np.pi * 420 * t) * np.exp(-t * 40) * 0.4
    return s.astype(np.float32) * vel

def bell(f, dur=2.5):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 3) + 0.25 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 6)
    return (s * np.exp(-t * 1.6)).astype(np.float32)

def add(buf, x, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(x)); buf[i:j] += x[: j - i] * gain

# chord per bar (scale degree of the root, chord tones as semitone offsets from D)
PROG = [(5, [5, 8, 12]), (3, [3, 7, 10]), (1, [1, 5, 8]), (0, [0, 4, 8 - 1]),        # Am G F E
        (5, [5, 8, 12]), (3, [3, 7, 10]), (1, [1, 5, 8]), (0, [0, 4, 7])]          # Am G F E

def section(kind, seed, bars=16):
    """kind: intro | groove | full | break"""
    rng = np.random.default_rng(seed)
    n = int(bars * BAR * SR) + SR * 3
    buf = np.zeros(n, np.float32)
    for b in range(bars):
        t0 = b * BAR
        rootsemi, chord = PROG[b % 8]
        # pad
        add(buf, pad([hz(ROOT - 12 + c) for c in chord], BAR + 1.2), t0, 0.22 if kind != 'break' else 0.30)
        # bass pluck on 1 and 3 (and the 'and' of 4 in fuller parts)
        if kind in ('groove', 'full'):
            for bt in (0, 2) + ((3.5,) if kind == 'full' else ()):
                add(buf, pluck(hz(ROOT - 24 + rootsemi), BEAT * 1.6, bright=0.5), t0 + bt * BEAT, 0.42)
            if kind == 'full':   # strummed chord on beat 1, like a guitar rasgueado
                for j, c in enumerate(chord): add(buf, pluck(hz(ROOT - 12 + c), BEAT * 1.2, bright=1.1), t0 + j * 0.018, 0.12)
        # frame drum: maqsum-like  D T . T D . T .
        if kind in ('groove', 'full'):
            pat = [('D', 0), ('T', 1), ('t', 1.5), ('D', 2), ('T', 3)] + ([('t', 2.5), ('t', 3.5), ('t', 0.75)] if kind == 'full' else [])
            for typ, bt in pat:
                v = 0.9 + 0.1 * rng.random()
                add(buf, dum(v) if typ == 'D' else tak(v * (0.55 if typ == 't' else 0.8)), t0 + bt * BEAT, 0.32)
        # lead: short plucked phrases in Hijaz, every other bar in calm parts
        play = kind == 'full' or (kind == 'groove' and b % 2 == 0) or (kind == 'intro' and b % 4 == 1)
        if play:
            deg = rng.choice([0, 2, 4, 7])
            tt = 0.0
            while tt < 4.0:
                step = rng.choice([0.5, 0.5, 1.0, 1.0, 1.5]) if kind != 'full' else rng.choice([0.25, 0.5, 0.5, 1.0])
                if rng.random() < 0.18: tt += step; continue
                deg = int(np.clip(deg + rng.choice([-2, -1, -1, 1, 1, 2, 0]), -3, 9))
                add(buf, pluck(hz(scale_note(deg)), BEAT * 1.4, bright=0.9, vel=0.8 + 0.2 * rng.random()), t0 + tt * BEAT, 0.20)
                tt += step
        if kind == 'break' and b % 4 == 0:
            add(buf, bell(hz(scale_note(rng.choice([4, 7, 9]), 1))), t0 + BEAT, 0.08)
    return buf

def reverb(x):
    """small room: a few feedback-free echoes, enough to glue the parts"""
    y = x.copy()
    for d, g in ((0.031, 0.32), (0.047, 0.26), (0.071, 0.2), (0.113, 0.14), (0.173, 0.09)):
        k = int(d * SR); y[k:] += x[:-k] * g
    return y

def main():
    plan = [('intro', 1, 8), ('groove', 2, 16), ('full', 3, 16), ('break', 4, 8), ('groove', 5, 16), ('full', 6, 16),
            ('break', 7, 8), ('groove', 8, 16)]
    parts = [section(k, s, b) for k, s, b in plan]
    # crossfade sections into one ~6 min piece
    xf = int(1.0 * SR)
    piece = parts[0]
    for p in parts[1:]:
        cut = len(piece) - SR * 3 + 0       # the 3 s tail overlaps the next section
        head = piece[:cut]; tail = piece[cut:]
        nxt = p.copy(); nxt[:len(tail)] += tail
        piece = np.concatenate([head, nxt])
    piece = reverb(piece)
    total = float(os.environ.get('MUSIC_SECONDS', 0)) or 1900
    loops = int(np.ceil(total * SR / (len(piece) - xf))) + 1
    out = piece.copy()
    for _ in range(loops - 1):
        fade = np.linspace(0, 1, xf, dtype=np.float32)
        out[-xf:] = out[-xf:] * (1 - fade) + piece[:xf] * fade
        out = np.concatenate([out, piece[xf:]])
    out = out[: int(total * SR)]
    fo = int(4 * SR); out[-fo:] *= np.linspace(1, 0, fo)
    out = out / (np.abs(out).max() + 1e-6) * 0.8
    os.makedirs(OUT, exist_ok=True)
    with wave.open(os.path.join(OUT, 'music.wav'), 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
        wf.writeframes((out * 32767).astype(np.int16).tobytes())
    print('music.wav', round(len(out) / SR, 1), 's; piece length', round(len(piece) / SR, 1), 's')

if __name__ == '__main__':
    main()
