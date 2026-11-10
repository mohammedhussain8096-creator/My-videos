import cv2, numpy as np, subprocess, sys, math

SRC, OUT = sys.argv[1], sys.argv[2]
W, H, FPS, DUR = 720, 1280, 30, 13.0

# segments: (out_start, out_end, src_start)
SEGS = [(0.00, 3.04, 1.00), (3.04, 6.18, 12.70), (6.18, 9.33, 16.20), (9.33, 13.0, 21.50)]
# effect timeline (all on music beats of the clip's own audio)
STREAK = 3.04; ZOOMHIT = 6.18; PUNCH = 7.76; FLASH = 9.33; WHIP = 10.01; SHRINK = 10.92
SMALL = [4.61, 6.85, 8.54, 12.2]

cap = cv2.VideoCapture(SRC)
frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
nsrc = len(frames)

def src_frame(t):
    for a, b, s in SEGS:
        if a <= t < b:
            return frames[min(nsrc - 1, int(round((s + t - a) * FPS)))]
    return frames[-1]

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
VIG = np.clip(1 - 0.35 * np.clip(r - 0.55, 0, None) ** 1.4, 0, 1)[..., None]

def grade(f):
    a = f.astype(np.float32) / 255
    a = np.clip((a - 0.5) * 1.08 + 0.51, 0, 1)                      # contrast
    a = a * np.array([0.99, 1.0, 1.02], np.float32)                  # warm (BGR)
    g = a.mean(-1, keepdims=True); a = g + (a - g) * 1.06            # saturation
    return np.clip(a * VIG, 0, 1)

def bloom(a, amt, k=41):
    hi = np.clip(a - 0.55, 0, 1) * 2
    b = cv2.GaussianBlur(hi, (k, k), 0)
    return np.clip(1 - (1 - a) * (1 - b * amt), 0, 1)                # screen

def scale(a, s, cx=0.5, cy=0.5, bg=0.0):
    M = np.float32([[s, 0, (1 - s) * W * cx], [0, s, (1 - s) * H * cy]])
    return cv2.warpAffine(a, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=(bg, bg, bg))

def radial(a, strength, n=8):
    acc = np.zeros_like(a)
    for i in range(n):
        acc += scale(a, 1 + strength * i / n)
    return acc / n

def rgbsplit(a, px):
    px = int(px)
    if px <= 0: return a
    o = a.copy()
    o[..., 2] = np.roll(a[..., 2], px, 1); o[..., 0] = np.roll(a[..., 0], -px, 1)
    return o

def disk(rad):
    rad = max(1, int(rad)); k = np.zeros((2 * rad + 1, 2 * rad + 1), np.float32)
    cv2.circle(k, (rad, rad), rad, 1, -1); return k / k.sum()

def bokeh(a, rad):
    if rad < 1: return a
    boosted = a + np.clip(a - 0.6, 0, 1) ** 2 * 4                    # highlights become glowing discs
    return np.clip(cv2.filter2D(boosted, -1, disk(rad)), 0, 1)

def env(t, t0, dur):  # 1 at t0 decaying to 0 over dur
    x = (t - t0) / dur
    return 0.0 if x < 0 or x > 1 else (1 - x) ** 2

rng = np.random.default_rng(5)
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                       "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", OUT],
                      stdin=subprocess.PIPE)
for n in range(int(DUR * FPS)):
    t = n / FPS
    a = grade(src_frame(t))
    a = bloom(a, 0.25)                                               # constant soft glow

    # 1) bokeh intro: defocused glowing discs pulling into focus + slow zoom-out
    if t < 2.6:
        p = t / 2.6
        a = scale(a, 1.15 - 0.15 * p)
        a = bokeh(a, 26 * (1 - p) ** 1.6)

    # 2) vertical streak glitch at the first cut
    k = (t - (STREAK - 0.07)) * FPS
    if 0 <= k < 5:
        st = cv2.blur(a, (1, 301)); st = cv2.blur(st, (1, 151))
        shift = int(rng.integers(-40, 40))
        a = np.roll(st, shift, 1) * 0.85 + a * 0.15

    # 3) zoom-blur hit with RGB split
    e = env(t, ZOOMHIT, 0.3)
    if e: a = rgbsplit(radial(a, 0.22 * e), 14 * e)

    # 4) zoom punch with shake
    e = env(t, PUNCH, 0.35)
    if e:
        a = scale(radial(a, 0.15 * e), 1 + 0.28 * e, 0.5 + rng.uniform(-.02, .02) * e, 0.5 + rng.uniform(-.02, .02) * e)

    # 5) white flash then dreamy glow
    e = env(t, FLASH, 0.12)
    if e: a = a * (1 - 0.9 * e) + 0.9 * e
    g = env(t, FLASH, 0.9)
    if g: a = np.clip(bloom(a, 1.6 * g, 81) + 0.12 * g, 0, 1)

    # 6) horizontal whip / motion blur that settles into glow
    e = env(t, WHIP, 0.45)
    if e:
        L = int(4 + 140 * e) | 1
        a = cv2.blur(a, (L, 1)); a = bloom(a, 0.9 * e, 61)

    # 7) shrink bounce (frame drops to 60% on black, springs back)
    x = (t - SHRINK) / 0.4
    if 0 <= x <= 1:
        s = 1 - 0.4 * math.exp(-5 * x) * abs(math.cos(4 * x))
        a = scale(radial(a, 0.08 * (1 - x)), s)

    # small beat pulses
    for b in SMALL:
        e = env(t, b, 0.18)
        if e: a = rgbsplit(scale(a, 1 + 0.05 * e), 6 * e)

    # fade out
    if t > DUR - 0.4: a = a * (DUR - t) / 0.4
    ff.stdin.write((np.clip(a, 0, 1) * 255).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait()
