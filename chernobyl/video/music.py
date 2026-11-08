"""Original tense ambient score for the Chernobyl documentary (composed in code, no samples, free to use).

Layers: dark drone pad (D minor / Bb / Gm / A), sub pulse like a slow heartbeat (~62 BPM), sparse high piano,
and an airy 'radiation' shimmer. Each pass changes key and intensity so 25 minutes never feels like one loop.
Writes OUT_DIR/music.wav (MUSIC_SECONDS long)."""
import os, wave
import numpy as np
OUT = os.environ.get('OUT_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build'))
SR = 32000; BEAT = 60 / 62; BAR = 4 * BEAT
rng = np.random.default_rng(21)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

def pad(notes, dur, bright=0.3):
    n = int(dur * SR); t = np.arange(n) / SR; out = np.zeros(n, np.float32)
    for m in notes:
        for det in (-0.07, 0.0, 0.06):
            ph = 2 * np.pi * hz(m) * 2 ** (det / 12) * t
            out += np.sin(ph) + bright * 0.3 * np.sin(2 * ph) + bright * 0.12 * np.sin(3 * ph)
    env = np.minimum(1, t / 2.5) * np.minimum(1, (dur - t) / 2.0)
    return out * env / (len(notes) * 3)

def pulse(dur, root, level):
    n = int(dur * SR); out = np.zeros(n, np.float32); k = 0
    while k * BEAT < dur - 0.6:
        for off, amp in ((0, 1.0), (0.28, 0.6)):          # lub-dub
            s = int((k * BEAT + off) * SR); m = int(0.5 * SR); tt = np.arange(m) / SR
            hit = np.sin(2 * np.pi * (hz(root - 24) + 30 * np.exp(-tt * 20)) * tt) * np.exp(-tt * 9) * amp
            e = min(n, s + m); out[s:e] += hit[:e - s] * level
        k += 1
    return out

def piano(m, dur, vel):
    n = int(dur * SR); t = np.arange(n) / SR; out = np.zeros(n, np.float32)
    for k in range(1, 6): out += (1 / k ** 1.5) * np.sin(2 * np.pi * hz(m) * k * t) * np.exp(-t * (0.8 + 0.8 * k))
    return out * vel

def shimmer(dur, level):
    n = int(dur * SR); x = rng.normal(0, 1, n).astype(np.float32)
    from scipy.signal import butter, lfilter
    b, a = butter(2, [5000 / (SR / 2), 9000 / (SR / 2)], 'band'); x = lfilter(b, a, x)
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * np.arange(n) / SR)
    return (x * lfo * level).astype(np.float32)

PROG = [[50, 57, 62, 65], [46, 53, 58, 62], [43, 50, 55, 58], [45, 52, 57, 61]]
MEL = [74, 72, 69, 70, 67, 69, 73, 74]

def section(tr, intensity):
    bars_per = 3; L = int(len(PROG) * bars_per * BAR * SR) + SR * 4; out = np.zeros(L, np.float32)
    for i, ch in enumerate(PROG):
        t0 = i * bars_per * BAR; d = bars_per * BAR + 2.0; a = int(t0 * SR)
        s = pad([m + tr for m in ch], d, 0.2 + 0.4 * intensity) * 0.5; out[a:a + len(s)] += s
        if intensity > 0.3:
            p = pulse(bars_per * BAR, ch[0] + tr, 0.35 * intensity); out[a:a + len(p)] += p
        if intensity > 0.15:
            for k in range(2):
                m = MEL[(i * 2 + k + tr) % len(MEL)] + tr; pn = piano(m, 5.0, 0.16 + 0.05 * rng.random())
                b = int((t0 + k * 1.5 * BAR) * SR); out[b:b + len(pn)] += pn
    out[:L] += shimmer(L / SR, 0.05 + 0.06 * intensity)
    return out, int(len(PROG) * bars_per * BAR * SR)

def main():
    need = float(os.environ.get('MUSIC_SECONDS', 1500))
    plan = [(0, 0.5), (0, 0.8), (-2, 0.4), (3, 0.7), (-4, 0.3), (1, 0.9), (-1, 0.5), (2, 0.6), (0, 0.4), (-3, 0.8)]
    L = int((need + 30) * SR); out = np.zeros(L, np.float32); pos = 0; k = 0
    while pos < need * SR:
        tr, inten = plan[k % len(plan)]; buf, adv = section(tr, inten); k += 1
        e = min(L, pos + len(buf)); out[pos:e] += buf[:e - pos]; pos += adv
    out = out[:int((need + 3) * SR)]
    for dly, g in ((0.13, 0.28), (0.29, 0.16)):
        kk = int(dly * SR); out[kk:] += g * out[:-kk]
    out /= np.max(np.abs(out)) + 1e-9; out *= 0.8
    os.makedirs(OUT, exist_ok=True)
    with wave.open(os.path.join(OUT, 'music.wav'), 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((out * 32767).astype(np.int16).tobytes())
    print('music', round(len(out) / SR, 1), 's')

if __name__ == '__main__':
    main()
