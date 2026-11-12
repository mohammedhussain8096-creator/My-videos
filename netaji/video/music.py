"""Original background score for the Partition documentary (composed in code, no samples, free to use).

Mood: sombre and reflective. A slow string-like pad in D minor (Dm - Bb - Gm - A, then Dm - F - C - A),
a low drone, and sparse piano-like notes on top, ~60 BPM. A slightly brighter variation follows so the
piece does not feel like a short loop. Writes OUT_DIR/music.wav at least MUSIC_SECONDS long."""
import os, wave
import numpy as np

OUT = os.environ.get('OUT_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build'))
SR = 32000
BAR = 4.0                     # 60 BPM, 4 beats per bar
rng = np.random.default_rng(11)

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

def strings(notes, dur):
    n = int(dur * SR); t = np.arange(n) / SR; out = np.zeros(n, np.float32)
    for m in notes:
        for det in (-0.09, 0.0, 0.08):
            f = hz(m) * 2 ** (det / 12)
            vib = 1 + 0.0025 * np.sin(2 * np.pi * 5.1 * t + m)
            ph = 2 * np.pi * np.cumsum(f * vib) / SR
            for k, a in ((1, 1.0), (2, 0.35), (3, 0.18), (4, 0.08), (5, 0.04)):
                out += a * np.sin(k * ph + det * 7)
    env = np.minimum(1, t / 1.8) * np.minimum(1, (dur - t) / 1.6)
    swell = 0.8 + 0.2 * np.sin(np.pi * t / dur)
    return out * env * swell / (len(notes) * 3)

def piano(m, dur, vel=1.0):
    n = int(dur * SR); t = np.arange(n) / SR; out = np.zeros(n, np.float32); f = hz(m)
    for k in range(1, 7):
        out += (1 / k ** 1.4) * np.sin(2 * np.pi * f * k * 1.0008 ** k * t) * np.exp(-t * (0.9 + 0.7 * k))
    a = min(n, int(0.006 * SR)); out[:a] *= np.linspace(0, 1, a)
    return out * vel

def drone(m, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * hz(m) * t) + 0.3 * np.sin(2 * np.pi * hz(m + 7) * t) + 0.2 * np.sin(2 * np.pi * hz(m) * 2 * t)
    return s * (0.7 + 0.3 * np.sin(2 * np.pi * 0.05 * t))

PROG_A = [[50, 57, 62, 65], [46, 58, 62, 65], [43, 55, 62, 70], [45, 57, 61, 64]]       # Dm Bb Gm A
PROG_B = [[50, 57, 62, 65], [41, 57, 60, 65], [48, 55, 60, 64], [45, 57, 61, 64]]       # Dm F C A
MEL_A = [[(0, 74), (2, 72), (3, 69)], [(0, 70), (2, 69)], [(0, 67), (1, 70), (2, 74)], [(0, 73), (2, 76)]]
MEL_B = [[(0, 77), (2, 76), (3, 74)], [(0, 72), (2, 69)], [(0, 72), (1, 71), (2, 67)], [(0, 69), (2, 73)]]

def section(prog, mel, bars_per_chord=2, melody=True, tr=0):
    prog = [[m + tr for m in ch] for ch in prog]; mel = [[(b, m + tr) for b, m in bar] for bar in mel]
    L = int(len(prog) * bars_per_chord * BAR * SR) + SR * 6
    out = np.zeros(L, np.float32)
    for i, ch in enumerate(prog):
        t0 = i * bars_per_chord * BAR; d = bars_per_chord * BAR + 1.6
        s = strings(ch, d) * 0.55; a = int(t0 * SR); out[a:a + len(s)] += s
        dr = drone(ch[0] - 12, d) * 0.12 * np.minimum(1, np.arange(int(d * SR)) / SR / 1.5) * np.minimum(1, (d - np.arange(int(d * SR)) / SR) / 1.5)
        out[a:a + len(dr)] += dr
        if melody:
            for beat, m in mel[i]:
                p = piano(m, 4.0, 0.22 + 0.06 * rng.random()); b = int((t0 + beat * 2.0) * SR); out[b:b + len(p)] += p
    return out, int(len(prog) * bars_per_chord * BAR * SR)

def main():
    need = float(os.environ.get('MUSIC_SECONDS', 1200))
    def parts_for(tr):
        return [section(PROG_A, MEL_A, melody=False, tr=tr), section(PROG_A, MEL_A, tr=tr), section(PROG_B, MEL_B, tr=tr),
                section(PROG_A, MEL_A, tr=tr), section(PROG_B, MEL_B, melody=False, tr=tr)]
    parts = parts_for(0)
    piece_len = sum(p[1] for p in parts)
    L = int((need + 8) * SR) + parts[-1][0].shape[0]
    out = np.zeros(L, np.float32); pos = 0
    cycle = 0
    while pos < need * SR:
        if cycle: parts = parts_for([0, -2, 3, -4, 1, -1, 2][cycle % 7])     # each pass in a new key
        cycle += 1
        for buf, adv in parts:
            e = min(L, pos + len(buf)); out[pos:e] += buf[:e - pos]; pos += adv
            if pos >= need * SR: break
    out = out[:int((need + 4) * SR)]
    # gentle room: two short echoes
    for dly, g in ((0.11, 0.25), (0.23, 0.15)):
        k = int(dly * SR); out[k:] += g * out[:-k]
    out /= np.max(np.abs(out)) + 1e-9; out *= 0.8
    os.makedirs(OUT, exist_ok=True)
    with wave.open(os.path.join(OUT, 'music.wav'), 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
        wf.writeframes((out * 32767).astype(np.int16).tobytes())
    print('music', round(len(out) / SR, 1), 's, piece', round(piece_len / SR, 1), 's')

if __name__ == '__main__':
    main()
