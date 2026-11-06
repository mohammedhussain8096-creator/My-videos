"""Build the soundtrack (voice + synthesized drone + blast SFX) and mux the final video.

Usage: python mix.py <timings.json> <clips_dir> <work_dir> <out.mp4>
"""
import json
import subprocess
import sys

import numpy as np

SR = 48000


def load_mp3(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, np.float32).copy()


def fft_lowpass(x, cutoff):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x)).astype(np.float32)


def boom(dur, rng, cutoff=120, decay=1.6):
    n = int(dur * SR)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n).astype(np.float32)
    body = fft_lowpass(noise, cutoff) * 6
    env = (1 - np.exp(-t * 60)) * np.exp(-t / decay)
    sub = np.sin(2 * np.pi * (45 * np.exp(-t * 0.6)) * t) * np.exp(-t / (decay * 0.8))
    return (body * env + 0.6 * sub).astype(np.float32)


def rumble(dur, rng, rise=0.3):
    n = int(dur * SR)
    t = np.arange(n) / SR
    noise = fft_lowpass(rng.standard_normal(n).astype(np.float32), 300) * 3
    env = np.clip(t / (dur * rise), 0, 1) * np.clip((dur - t) / 0.8, 0, 1)
    return (noise * env).astype(np.float32)


def wind(dur, rng):
    n = int(dur * SR)
    noise = rng.standard_normal(n).astype(np.float32)
    w = fft_lowpass(noise, 900) - fft_lowpass(noise, 200)
    t = np.arange(n) / SR
    return (w * (0.6 + 0.4 * np.sin(t * 1.3)) * np.clip(t / 0.5, 0, 1) * np.clip((dur - t) / 0.5, 0, 1) * 2).astype(np.float32)


def drone(total, rng):
    n = int(total * SR)
    t = np.arange(n) / SR
    x = np.zeros(n, np.float32)
    for f, a in ((55, 0.5), (82.4, 0.3), (110, 0.18), (164.8, 0.08)):
        x += a * np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 0.07 * t)).astype(np.float32)
    x *= (0.75 + 0.25 * np.sin(2 * np.pi * 0.05 * t)).astype(np.float32)
    pad = fft_lowpass(rng.standard_normal(n).astype(np.float32), 400) * 1.5
    x += pad
    # slow heartbeat-like pulse
    beat = np.zeros(n, np.float32)
    for s in np.arange(0, total, 1.6):
        i = int(s * SR)
        k = boom(0.6, rng, 80, 0.15)
        beat[i:i + len(k)] += k[: n - i] * 0.35
    x += beat
    fade = np.clip(t / 2, 0, 1) * np.clip((total - t) / 3, 0, 1)
    return (x * fade * 0.12).astype(np.float32)


def _at(starts, k):
    v = starts.get(k)
    return v if v is not None else float("nan")


def main(timings, clips, work, out, *only):
    T = json.load(open(timings))
    if only:
        T = [s for s in T if s["id"] in only]
    rng = np.random.default_rng(1)
    total = sum(s["dur"] for s in T)
    n = int(total * SR) + SR
    voice = np.zeros(n, np.float32)
    sfx = np.zeros(n, np.float32)
    starts = {}
    t0 = 0.0
    for s in T:
        starts[s["id"]] = t0
        v = load_mp3(s["voice"])
        i = int((t0 + 0.08) * SR)
        voice[i:i + len(v)] += v[: n - i]
        t0 += s["dur"]

    def put(sig, at, gain):
        if at is None or at != at:  # missing scene (nan)
            return
        i = int(at * SR)
        sfx[i:i + len(sig)] += gain * sig[: n - i]

    d = {s["id"]: s["dur"] for s in json.load(open(timings))}
    starts = {k: starts.get(k) for k in d}
    put(rumble(d["s03_flash"], rng, 0.8), starts["s03_flash"], 0.25)
    put(boom(6, rng, 140, 2.0), _at(starts, "s04_fireball") + 0.1, 0.9)
    put(rumble(d["s05_vapor"], rng, 0.2), starts["s05_vapor"], 0.35)
    put(boom(5, rng, 160, 1.4), _at(starts, "s06_wave") + d["s06_wave"] * 0.55, 0.8)
    put(rumble(d["s06_wave"], rng, 0.9), starts["s06_wave"], 0.45)
    put(wind(d["s08_wind"], rng), starts["s08_wind"], 0.5)
    put(rumble(d["s08_wind"], rng, 0.1), starts["s08_wind"], 0.25)
    put(boom(6, rng, 90, 2.5), starts["s10_rings"], 0.6)
    put(rumble(d["s11_cloud"], rng, 0.5), starts["s11_cloud"], 0.3)
    put(wind(d["s12_fallout"] + d["s13_plume"], rng), starts["s12_fallout"], 0.25)
    put(boom(7, rng, 70, 3.0), _at(starts, "s16_history") + 0.2, 0.45)

    bed = drone(total + 1, rng)[:n]
    # duck the bed under the voice
    env = np.abs(voice)
    k = int(0.25 * SR)
    env = np.convolve(env, np.ones(k, np.float32) / k, mode="same")
    duck = 1 - 0.45 * np.clip(env * 8, 0, 1)
    mixd = voice * 1.0 + bed * duck + sfx * 0.55 * (1 - 0.35 * np.clip(env * 8, 0, 1))
    mixd = mixd[: int(total * SR)]
    mixd = np.tanh(mixd * 1.1) / np.tanh(1.1)
    wav = f"{work}/mix.f32"
    mixd.astype(np.float32).tofile(wav)

    lst = f"{work}/clips.txt"
    with open(lst, "w") as fh:
        for s in T:
            fh.write(f"file '{clips}/{s['id']}.mp4'\n")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                           "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", wav,
                           "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium",
                           "-b:v", "70M", "-maxrate", "90M", "-bufsize", "140M", "-pix_fmt", "yuv420p",
                           "-profile:v", "high", "-level", "5.2", "-x264-params", "aq-mode=3",
                           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(SR),
                           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out])
    print("wrote", out, total)


if __name__ == "__main__":
    main(*sys.argv[1:])
