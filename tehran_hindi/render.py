"""Procedural 3D-style renderer for the Hindi Tehran explainer.

Every scene is drawn from scratch (noise terrain, perspective city street,
particle mushroom cloud, etc). No text, captions, counters or watermarks are
ever drawn on screen.

Usage: python render.py <timings.json> <out_dir> [scene_id ...]
"""
import json
import math
import os
import subprocess
import sys
from functools import lru_cache

import cv2
import numpy as np

S = float(os.environ.get('SCALE', '1'))      # 1 -> 720x1280, 3 -> 2160x3840 (4K)
W, H = int(round(720 * S)), int(round(1280 * S))
FPS = int(os.environ.get('FPS', '30'))
TEX = int(os.environ.get('TEX', '2048'))       # texture resolution (detail level)
DETAIL = S >= 2


def u(v):
    """design units (720-wide frame) -> pixels"""
    return v * S
RNG = np.random.default_rng


# ---------------------------------------------------------------- utilities
def fbm(h, w, seed, octaves=6, base=4, persistence=0.55):
    r = RNG(seed)
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        s = base * 2 ** o
        small = r.random((s, s * w // h + 1 if w > h else s), dtype=np.float32)
        out += amp * cv2.resize(small, (w, h), interpolation=cv2.INTER_CUBIC)
        tot += amp
        amp *= persistence
    out /= tot
    out -= out.min()
    out /= out.max() + 1e-6
    return out


def lerp(a, b, t):
    return a + (b - a) * t


def smooth(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


def col(*rgb):
    return np.array(rgb, np.float32)


_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIGNETTE = 1 - 0.55 * np.clip(((_xx - W / 2) / (W * 0.75)) ** 2 + ((_yy - H / 2) / (H * 0.62)) ** 2, 0, 1)
VIGNETTE = VIGNETTE[..., None]
VIGNETTE3 = np.ascontiguousarray(np.repeat(VIGNETTE, 3, axis=2))
ONE3 = np.ones((H, W, 3), np.float32)
ZERO3 = np.zeros((H, W, 3), np.float32)


def fblur(img, sigma):
    """Fast large-radius Gaussian blur (downsample -> blur -> upsample)."""
    h, w = img.shape[:2]
    shp = img.shape
    if sigma < 4:
        return cv2.GaussianBlur(img, (0, 0), sigma).reshape(shp)
    k = int(min(16, max(2, sigma / 2)))
    small = cv2.resize(img, (max(1, w // k), max(1, h // k)), interpolation=cv2.INTER_AREA)
    small = cv2.GaussianBlur(small, (0, 0), sigma / k)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_LINEAR).reshape(shp)


def radial(cx, cy, r):
    return np.exp(-(((_xx - cx) ** 2 + (_yy - cy) ** 2) / (2 * r * r)))[..., None]


def add_glow(img, cx, cy, r, color):
    """img += gaussian glow, computed only inside a 4-sigma window."""
    m = int(4 * r) + 2
    x0, y0, x1, y1 = max(0, int(cx) - m), max(0, int(cy) - m), min(W, int(cx) + m), min(H, int(cy) + m)
    if x1 <= x0 or y1 <= y0:
        return
    e = np.exp(-(((_xx[y0:y1, x0:x1] - cx) ** 2 + (_yy[y0:y1, x0:x1] - cy) ** 2) / (2 * r * r)))[..., None]
    img[y0:y1, x0:x1] += e * np.asarray(color, np.float32)


def bloom(img, thresh=0.75, strength=0.8, k=61):
    bright = np.clip(img - thresh, 0, None)
    small = cv2.resize(bright, (W // 4, H // 4))
    small = cv2.GaussianBlur(small, (0, 0), k / 8 * S)  # already downsampled
    return img + strength * cv2.resize(small, (W, H))


def finish(img, f, grade=(1.03, 1.0, 0.94), grain=0.025, vig=True):
    img = np.ascontiguousarray(img, dtype=np.float32)
    g = np.array(grade, np.float32)
    # grade + 18% desaturation in one 3x3 colour matrix
    M = 0.82 * np.diag(g) + 0.18 * np.tile(g / 3, (3, 1))
    img = cv2.transform(img, M)
    if vig:
        img = cv2.multiply(img, VIGNETTE3)
    if grain:
        gr = RNG(f * 7 + 1).standard_normal((int(H / max(1.5, S)), int(W / max(1.5, S)))).astype(np.float32)
        gr = cv2.resize(gr, (W, H)) * np.float32(grain)
        img = cv2.add(img, cv2.merge([gr, gr, gr]))
    over = cv2.max(cv2.subtract(img, ONE3), ZERO3)
    img = cv2.divide(img, cv2.scaleAdd(over, 0.6, ONE3))  # soft highlight roll-off
    return np.clip(img, 0, 1, out=img)


def shake(img, amt, f):
    if amt <= 0:
        return img
    r = RNG(f)
    dx, dy = r.uniform(-amt, amt, 2) * S
    M = np.float32([[1.02, 0, dx - W * 0.01], [0, 1.02, dy - H * 0.01]])
    return cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REFLECT)


def ridge(seed, amp=1.0):
    r = fbm(64, 64, seed, octaves=5, base=2)[32]
    r = cv2.resize(r[None, :], (W, 1), interpolation=cv2.INTER_CUBIC)[0]
    return (r - r.min()) / (r.max() - r.min() + 1e-6) * amp


# ---------------------------------------------------------------- puffs
@lru_cache(maxsize=None)
def puff_sprite(r, seed=0):
    r = max(2, int(r))
    s = 2 * r + 1
    yy, xx = np.mgrid[0:s, 0:s].astype(np.float32) - r
    d = np.sqrt(xx ** 2 + yy ** 2) / r
    n = fbm(s, s, seed + r, octaves=3, base=3) if s > 8 else np.ones((s, s), np.float32) * 0.5
    a = np.clip(1 - d ** 2, 0, 1) ** 1.4 * (0.55 + 0.6 * n)
    a = np.clip(a, 0, 1)
    shade = np.clip(1.08 - 0.45 * (yy / r) - 0.15 * (xx / r) + 0.2 * (n - 0.5), 0.45, 1.25)
    return a[..., None], shade[..., None]


def draw_puff(img, x, y, r, color, alpha=1.0, seed=0):
    r = int(max(2, min(r, 420 * S)))
    q = int(r ** 0.5 * 3)  # quantise radius for caching
    r = max(2, int((q / 3) ** 2))
    if r <= 260:
        a, sh = puff_sprite(r, seed % 3)
    else:
        a0, sh0 = puff_sprite(260, seed % 3)
        a = cv2.resize(a0[..., 0], (2 * r + 1, 2 * r + 1))[..., None]
        sh = cv2.resize(sh0[..., 0], (2 * r + 1, 2 * r + 1))[..., None]
    x0, y0 = int(x) - r, int(y) - r
    x1, y1 = x0 + a.shape[1], y0 + a.shape[0]
    sx0, sy0 = max(0, -x0), max(0, -y0)
    sx1, sy1 = a.shape[1] - max(0, x1 - W), a.shape[0] - max(0, y1 - H)
    if sx1 <= sx0 or sy1 <= sy0:
        return
    roi = img[y0 + sy0:y0 + sy1, x0 + sx0:x0 + sx1]
    aa = a[sy0:sy1, sx0:sx1] * alpha
    roi[:] = roi * (1 - aa) + (color * sh[sy0:sy1, sx0:sx1]) * aa


def mushroom(img, gx, gy, s, phase, seed=3, fire=0.0, palette=None):
    """Particle mushroom cloud. gx,gy ground point, s px scale (cap radius),
    phase 0..1 growth."""
    r = RNG(seed)
    pal = palette or (col(0.62, 0.55, 0.50), col(0.86, 0.80, 0.74))
    ph = smooth(phase)
    top = gy - s * (0.6 + 2.0 * ph)
    capw = s * (0.45 + 0.55 * ph)
    puffs = []
    # stem
    for i in range(110 if DETAIL else 70):
        t = r.random()
        y = lerp(gy, top + capw * 0.2, t)
        w = s * (0.12 + 0.05 * t) * (0.6 + 0.4 * ph)
        puffs.append((gx + r.normal(0, w * 0.5), y, w * r.uniform(0.6, 1.1), t * 0.6))
    # base skirt / ground dust ring
    for i in range(70 if DETAIL else 40):
        a = r.uniform(0, 2 * math.pi)
        rr = s * (0.4 + 1.1 * ph) * r.uniform(0.6, 1.1)
        puffs.append((gx + math.cos(a) * rr, gy + math.sin(a) * rr * 0.18, s * 0.22 * r.uniform(0.6, 1.2), 0.0))
    # cap: torus + dome
    for i in range(260 if DETAIL else 150):
        a = r.uniform(0, 2 * math.pi)
        rad = capw * r.uniform(0.2, 1.0)
        x = gx + math.cos(a) * rad
        z = math.sin(a) * rad
        y = top + z * 0.25 - capw * 0.35 * (1 - (rad / capw) ** 2) * r.uniform(0.4, 1.0)
        puffs.append((x, y, capw * r.uniform(0.2, 0.38), 1.0 + z / capw * 0.01))
    puffs.sort(key=lambda p: p[1])  # draw top to bottom so lower (closer) overlaps
    for (x, y, w, h) in puffs:
        c = lerp(pal[0], pal[1], np.clip(h, 0, 1))
        if fire > 0:
            c = lerp(c, col(1.6, 0.75, 0.25), fire * (1 - np.clip(h, 0, 1) * 0.5))
        draw_puff(img, x, y, w, c, 0.9, int(x * 7 + y))
    if DETAIL:  # fine billows on the cap surface
        for i in range(160):
            a = r.uniform(math.pi, 2 * math.pi)
            x = gx + math.cos(a) * capw * r.uniform(0.3, 1.05)
            y = top - capw * 0.25 + math.sin(a) * capw * 0.45 * r.uniform(0.5, 1.0)
            draw_puff(img, x, y, capw * r.uniform(0.06, 0.13), pal[1] * r.uniform(0.92, 1.08), 0.55, i)
    if fire > 0:
        img += fire * 0.9 * radial(gx, top + capw * 0.1, capw * 0.8) * col(1.0, 0.45, 0.15)


# ---------------------------------------------------------------- textures
@lru_cache(maxsize=None)
def terrain_tex(size=None, seed=11, sea=False):
    size = size or TEX
    h = fbm(size, size, seed, octaves=9 if size > 2048 else 8, base=3)
    detail = fbm(size, size, seed + 1, octaves=4, base=16)
    hgt = 0.85 * h + 0.15 * detail
    hs = cv2.GaussianBlur(hgt, (0, 0), 2 * size / 2048)
    gx = cv2.Sobel(hs, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(hs, cv2.CV_32F, 0, 1, ksize=3)
    sl = -(gx * 0.8 + gy * 0.6)
    sl = sl / (3 * sl.std() + 1e-6)
    shade = np.clip(0.92 + 0.45 * sl, 0.55, 1.3)[..., None]
    veg = fbm(size, size, seed + 2, octaves=5, base=6)[..., None]
    sand, rock, green = col(0.80, 0.70, 0.54), col(0.52, 0.44, 0.36), col(0.42, 0.47, 0.32)
    c = lerp(sand, rock, np.clip((hgt[..., None] - 0.35) * 2.2, 0, 1))
    c = lerp(c, green, np.clip((veg - 0.62) * 3, 0, 0.6))
    c = c * shade
    if sea:
        yy, xx = np.mgrid[0:size, 0:size].astype(np.float32) / size
        # gulf in the south-west, sea in the north
        m = 0.6 * h + 0.4 * (np.clip(1.2 - ((xx - 0.15) ** 2 + (yy - 1.0) ** 2) * 3.2, 0, 1)
                             + np.clip(1.0 - ((xx - 0.55) ** 2 * 6 + (yy - 0.02) ** 2 * 30), 0, 1))
        water = smooth((m - 0.62) * 12)[..., None]
        wcol = lerp(col(0.10, 0.25, 0.38), col(0.05, 0.13, 0.25), h[..., None])
        c = lerp(c, wcol, water)
    return np.clip(c, 0, 1).astype(np.float32)


@lru_cache(maxsize=None)
def city_tex(size=None, seed=5):
    size = size or TEX
    k = size / 2048
    base = terrain_tex(size, seed) * 0.3 + col(0.70, 0.66, 0.60) * 0.7
    img = (np.clip(base, 0, 1) * 255).astype(np.uint8)
    shadow = np.zeros((size, size), np.uint8)
    r = RNG(seed)
    cx = cy = size // 2
    road = (104, 102, 98)
    blk = int(64 * k)
    pad = int(5 * k)
    for bx in range(0, size, blk):
        for by in range(0, size, blk):
            x0, y0 = bx + pad, by + pad
            dist = math.hypot(bx - cx, by - cy) / size
            if r.random() < 0.05:
                cv2.rectangle(img, (x0, y0), (x0 + blk - 2 * pad, y0 + blk - 2 * pad), (88, 112, 74), -1)
                for _ in range(int(8 * k * k)):
                    tx, ty = r.integers(x0 + 3, x0 + blk - 2 * pad - 3, 2)
                    cv2.circle(img, (int(tx), int(ty)), int(4 * k), (60, 86, 52), -1, cv2.LINE_AA)
                continue
            # subdivide block into 2-4 buildings per side
            nx, ny = int(r.integers(2, 4)), int(r.integers(2, 4))
            ws, hs = (blk - 2 * pad) / nx, (blk - 2 * pad) / ny
            for i in range(nx):
                for j in range(ny):
                    a = (int(x0 + i * ws + 1), int(y0 + j * hs + 1))
                    b = (int(x0 + (i + 1) * ws - 2), int(y0 + (j + 1) * hs - 2))
                    ht = int(r.integers(2, 9) * (1.5 - dist * 1.5) * k)
                    cv2.rectangle(shadow, (a[0] + ht, a[1] + ht), (b[0] + ht, b[1] + ht), 255, -1)
                    tone = int(r.integers(178, 236))
                    roof = (tone, tone - int(r.integers(2, 14)), tone - int(r.integers(10, 32)))
                    cv2.rectangle(img, a, b, roof, -1)
                    cv2.rectangle(img, a, b, (tone - 40, tone - 45, tone - 55), max(1, int(k)))
                    if k > 1:  # rooftop clutter: water tanks, AC units, stair huts
                        for _ in range(int(r.integers(1, 5))):
                            px = int(r.integers(a[0] + 2, max(a[0] + 3, b[0] - 6)))
                            py = int(r.integers(a[1] + 2, max(a[1] + 3, b[1] - 6)))
                            sz = int(r.integers(2, 6))
                            tt = int(r.integers(120, 250))
                            cv2.rectangle(img, (px, py), (px + sz, py + sz), (tt, tt, tt - 8), -1)
                            cv2.rectangle(shadow, (px + 2, py + 2), (px + sz + 2, py + sz + 2), 160, -1)
    # boulevards and ring roads drawn over
    for a in np.linspace(0, math.pi, 4, endpoint=False):
        dx, dy = int(math.cos(a) * size), int(math.sin(a) * size)
        cv2.line(img, (cx - dx, cy - dy), (cx + dx, cy + dy), road, int(12 * k), cv2.LINE_AA)
    for rr in (320, 700):
        cv2.circle(img, (cx, cy), int(rr * k), road, int(12 * k), cv2.LINE_AA)
    if k > 1:  # cars on the boulevards
        for _ in range(1400):
            a = r.choice(np.linspace(0, math.pi, 4, endpoint=False))
            d = r.uniform(-size * 0.7, size * 0.7)
            off = r.choice([-3, 3]) * k
            px = cx + math.cos(a) * d - math.sin(a) * off
            py = cy + math.sin(a) * d + math.cos(a) * off
            g_ = int(r.integers(50, 230))
            cc = (g_, g_, g_) if r.random() < 0.75 else (int(r.integers(120, 200)), 60, 50)
            cv2.rectangle(img, (int(px - k), int(py - 0.6 * k)), (int(px + k), int(py + 0.6 * k)), cc, -1)
    out = img.astype(np.float32) / 255
    sh = cv2.GaussianBlur(shadow, (0, 0), 1.5 * k).astype(np.float32)[..., None] / 255
    road_mask = (np.abs(out - np.array(road, np.float32) / 255).sum(2, keepdims=True) < 0.02)
    out = out * (1 - 0.28 * sh * ~road_mask)
    return out


@lru_cache(maxsize=None)
def rubble_tex(size=None, seed=9):
    size = size or TEX // 2
    k = size / 1024
    n = fbm(size, size, seed, octaves=8 if k > 1 else 7, base=8)
    img = lerp(col(0.28, 0.27, 0.26), col(0.62, 0.60, 0.57), n[..., None])
    u8 = (img * 255).astype(np.uint8)
    r = RNG(seed)
    for _ in range(int(1600 * k * k * (1.5 if k > 1 else 1))):
        x, y = r.integers(0, size, 2)
        pts = (np.array([[x, y]]) + r.integers(-14, 14, (5, 2)) * k * r.uniform(0.4, 1.0)).astype(np.int32)
        t = int(r.integers(40, 150))
        cv2.fillConvexPoly(u8, cv2.convexHull(pts), (t, t, t - 5), cv2.LINE_AA)
    for _ in range(25):  # cracks
        p = r.integers(0, size, 2).astype(float)
        a = r.uniform(0, 6.28)
        for _ in range(40):
            a += r.normal(0, 0.4)
            q = p + 14 * k * np.array([math.cos(a), math.sin(a)])
            cv2.line(u8, tuple(p.astype(int)), tuple(q.astype(int)), (20, 20, 20), max(2, int(2 * k)), cv2.LINE_AA)
            p = q
    return u8.astype(np.float32) / 255


# ---------------------------------------------------------------- tilted ground view
SKY_TOP, SKY_HZ = col(0.55, 0.60, 0.66), col(0.86, 0.84, 0.80)


def tilt_view(tex, cx, cy, span, hz=0.30, depth=2.2, haze=col(0.82, 0.78, 0.72), rot=0.0, mountains=True, base=2048):
    """Map a top-down texture onto a tilted ground plane. Coordinates are in
    `base` texture units regardless of the real texture size. Returns (img, M)."""
    kt = tex.shape[0] / base
    hzy = H * hz
    near_w, far_w = span, span * depth
    c, s = math.cos(rot), math.sin(rot)

    def tp(dx, dy):
        return [cx + dx * c - dy * s, cy + dx * s + dy * c]

    src = np.float32([tp(-far_w / 2, -span * 1.2), tp(far_w / 2, -span * 1.2),
                      tp(near_w / 2, span * 0.5), tp(-near_w / 2, span * 0.5)])
    dst = np.float32([[-W * 0.1, hzy], [W * 1.1, hzy], [W * 1.0, H], [0, H]])
    M = cv2.getPerspectiveTransform(src * kt, dst)
    y0 = max(0, int(hzy) - 2)
    Mg = np.float64([[1, 0, 0], [0, 1, -y0], [0, 0, 1]]) @ M
    img = np.empty((H, W, 3), np.float32)
    img[y0:] = cv2.warpPerspective(tex, Mg, (W, H - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    t = np.clip((_yy - hzy) / (H - hzy), 0, 1)[..., None]
    sky = lerp(SKY_TOP, SKY_HZ, np.clip(_yy / hzy, 0, 1)[..., None])
    img = np.where(_yy[..., None] < hzy, sky, lerp(haze, img, smooth(t * 1.6) ** 0.8))
    if not mountains and hzy > 1:  # soft atmospheric horizon
        img = lerp(img, SKY_HZ, np.exp(-((_yy - hzy) / u(70)) ** 2)[..., None] * 0.85)
    if mountains:
        my = hzy - u(10) - ridge(77, u(60))
        mask = (_yy > my[None, :]) & (_yy < hzy + 2)
        mcol = lerp(col(0.60, 0.58, 0.56), haze, 0.35)
        img = np.where(mask[..., None], mcol, img)
        img = lerp(img, haze, np.exp(-((_yy - hzy) / u(40)) ** 2)[..., None] * 0.6)
    M = M @ np.diag([kt, kt, 1.0])
    return img.astype(np.float32), M


def project(M, pts):
    p = cv2.perspectiveTransform(np.float32(pts).reshape(-1, 1, 2), np.float64(M))
    return p.reshape(-1, 2)


def ground_ring(img, M, cx, cy, rad, color, thick=3, glow=0.6):
    a = np.linspace(0, 2 * math.pi, 360)
    pts = project(M, np.stack([cx + rad * np.cos(a), cy + rad * np.sin(a)], 1))
    layer = np.zeros_like(img)
    cv2.polylines(layer, [pts.astype(np.int32)], True, tuple(float(v) for v in color), max(1, int(thick * S)), cv2.LINE_AA)
    img += layer + glow * fblur(layer, 9 * S)


# ---------------------------------------------------------------- 3D street
class Street:
    def __init__(self, seed=1):
        r = RNG(seed)
        self.blds = []
        for side in (-1, 1):
            z = 6.0
            while z < 420:
                ln = r.uniform(14, 30)
                ht = r.uniform(14, 42)
                tone = r.uniform(0.62, 0.86)
                tint = col(tone, tone * r.uniform(0.94, 1.0), tone * r.uniform(0.86, 0.98))
                self.blds.append(dict(side=side, z0=z, z1=z + ln, h=ht, c=tint, x0=11.0, x1=26.0,
                                      shop=lerp(col(*r.uniform(0.2, 0.8, 3)), col(0.5, 0.45, 0.4), 0.55), cols=int(ln / 3.2), seed=int(r.integers(1e6))))
                z += ln + r.uniform(0.0, 3.0)
        self.trees = [(s, z) for s in (-1, 1) for z in np.arange(4, 400, 9.0)]
        self.cars = [(r.uniform(-5, 5), r.uniform(20, 300), col(*r.uniform(0.3, 0.95, 3))) for _ in range(6)]

    def render(self, camz, camx=0.0, camh=1.7, f=None, hz=0.43, collapse=None, dust_z=None,
               dust_col=col(0.62, 0.52, 0.44), fog=col(0.84, 0.82, 0.78), fogd=260.0, sky=None, people=()):
        f = f or 640.0 * S
        hzy = H * hz
        img = np.empty((H, W, 3), np.float32)
        top, bot = (sky or (col(0.62, 0.68, 0.74), col(0.88, 0.86, 0.82)))
        img[:] = lerp(top, bot, np.clip(_yy / hzy, 0, 1)[..., None])
        # distant mountains
        my = hzy - u(4) - ridge(31, u(45))
        img = np.where(((_yy > my[None, :]) & (_yy <= hzy))[..., None], lerp(col(0.66, 0.64, 0.62), fog, 0.4), img)
        # ground
        g = _yy > hzy
        t = np.clip((_yy - hzy) / (H - hzy), 0, 1)[..., None]
        ground = lerp(fog, col(0.36, 0.36, 0.37), smooth(t * 3))
        img = np.where(g[..., None], ground, img)

        def P(x, y, z):
            z = max(z - camz, 0.3)
            return (W / 2 + f * (x - camx) / z, hzy - f * (y - camh) / z)

        def fogc(c, z):
            k = 1 - math.exp(-max(z - camz, 0) / fogd)
            c = lerp(c, fog, k)
            if dust_z is not None and z > dust_z:
                c = lerp(c, dust_col, min(1.0, 0.85 + (z - dust_z) / 40))
            return tuple(float(v) for v in c)

        def poly(pts, c, z):
            cv2.fillPoly(img, [np.array(pts, np.int32)], fogc(c, z), cv2.LINE_AA)

        # sidewalks + lane lines
        for s in (-1, 1):
            poly([P(7 * s, 0, camz + 0.5), P(11 * s, 0, camz + 0.5), P(11 * s, 0, 600), P(7 * s, 0, 600)], col(0.6, 0.58, 0.55), 30)
        for z in np.arange(math.floor(camz / 8) * 8, 400, 8.0):
            if z + 4 < camz + 0.5:
                continue
            for x in (-0.15, 0.15):
                poly([P(x - 0.1, 0, z), P(x + 0.1, 0, z), P(x + 0.1, 0, z + 4), P(x - 0.1, 0, z + 4)], col(0.85, 0.75, 0.35), z)
            for x in (-3.5, 3.5):
                poly([P(x - 0.08, 0, z), P(x + 0.08, 0, z), P(x + 0.08, 0, z + 3), P(x - 0.08, 0, z + 3)], col(0.85, 0.85, 0.85), z)

        if DETAIL:  # curbs and street lamps
            for s_ in (-1, 1):
                poly([P(7 * s_, 0, camz + 0.5), P(7.15 * s_, 0.15, camz + 0.5), P(7.15 * s_, 0.15, 600), P(7 * s_, 0.15, 600)], col(0.75, 0.73, 0.70), 30)
        items = []
        if DETAIL:
            for s_ in (-1, 1):
                for z in np.arange(10, 400, 25.0):
                    if z > camz + 1:
                        items.append((z + 0.1, 'l', (s_, z)))
        for b in self.blds:
            if b['z1'] < camz + 0.5:
                continue
            items.append((b['z1'] + 1000, 'b', b))
        for s, z in self.trees:
            if z > camz + 1:
                items.append((z, 't', (s, z)))
        for x, z, c in self.cars:
            if z > camz + 2:
                items.append((z, 'c', (x, z, c)))
        for p in people:
            items.append((p['z'], 'p', p))
        items.sort(key=lambda it: -it[0])
        for z, kind, d in items:
            if kind == 'b':
                self._building(d, P, poly, fogc, collapse, camz)
            elif kind == 't':
                s, z = d
                x = 8.8 * s
                if collapse and z < collapse[0]:
                    continue
                a, b2 = P(x, 0, z), P(x, 3.2, z)
                cv2.line(img, tuple(map(int, a)), tuple(map(int, b2)), fogc(col(0.25, 0.2, 0.16), z), max(1, int(f * 0.3 / max(z - camz, 0.3))), cv2.LINE_AA)
                rr = f * 2.2 / max(z - camz, 0.3)
                cx_, cy_ = P(x, 4.2, z)
                for k, (ox, oy) in enumerate(((0, 0), (-0.5, 0.3), (0.5, 0.2), (0, -0.4))):
                    cv2.circle(img, (int(cx_ + ox * rr), int(cy_ + oy * rr)), max(1, int(rr * 0.75)),
                               fogc(col(0.30 + 0.04 * k, 0.45 + 0.03 * k, 0.24), z), -1, cv2.LINE_AA)
            elif kind == 'c':
                x, z, c = d
                if collapse and z < collapse[0]:
                    continue
                poly([P(x - 0.9, 0.2, z), P(x + 0.9, 0.2, z), P(x + 0.9, 1.1, z), P(x - 0.9, 1.1, z)], c, z)
                poly([P(x - 0.7, 1.1, z), P(x + 0.7, 1.1, z), P(x + 0.6, 1.6, z), P(x - 0.6, 1.6, z)], c * 0.7, z)
            elif kind == 'p':
                self._person(img, d, P, fogc, camz)
            elif kind == 'l':
                s_, z = d
                if collapse and z < collapse[0]:
                    continue
                a, b2, c2 = P(7.4 * s_, 0, z), P(7.4 * s_, 7.5, z), P(6.2 * s_, 7.5, z)
                w_ = max(1, int(f * 0.12 / max(z - camz, 0.3)))
                lc = fogc(col(0.22, 0.22, 0.24), z)
                cv2.line(img, tuple(map(int, a)), tuple(map(int, b2)), lc, w_, cv2.LINE_AA)
                cv2.line(img, tuple(map(int, b2)), tuple(map(int, c2)), lc, w_, cv2.LINE_AA)
        return img, P

    def _building(self, b, P, poly, fogc, collapse, camz):
        s, z0, z1, h = b['side'], max(b['z0'], camz + 0.5), b['z1'], b['h']
        if collapse and b['z0'] < collapse[0]:
            h = max(2.5, h * collapse[1])
        xa, xb = b['x0'] * s, b['x1'] * s
        c = b['c']
        # end face toward camera
        poly([P(xa, 0, z0), P(xb, 0, z0), P(xb, h, z0), P(xa, h, z0)], c * 0.78, z0)
        # road facing facade
        poly([P(xa, 0, z0), P(xa, 0, z1), P(xa, h, z1), P(xa, h, z0)], c, (z0 + z1) / 2)
        # shop band
        poly([P(xa, 0, z0), P(xa, 0, z1), P(xa, 3.2, z1), P(xa, 3.2, z0)], b['shop'] * 0.8, (z0 + z1) / 2)
        # windows
        if (z0 - camz) < 160:
            floors = int((h - 4) / 3.2)
            zs = np.linspace(b['z0'], z1, b['cols'] + 1)
            for i in range(b['cols']):
                za, zb = zs[i] + 0.7, zs[i + 1] - 0.7
                if za < camz + 0.6:
                    continue
                for k in range(floors):
                    ya, yb = 4.5 + k * 3.2, 4.5 + k * 3.2 + 1.8
                    wr = ((b['seed'] * 31 + i * 7 + k * 13) % 17) / 17.0
                    wc = c * (0.32 + 0.2 * wr) + col(0.02, 0.04, 0.07)
                    if DETAIL:  # window frame + sill
                        poly([P(xa, ya - 0.15, za - 0.15), P(xa, ya - 0.15, zb + 0.15), P(xa, yb + 0.15, zb + 0.15), P(xa, yb + 0.15, za - 0.15)], c * 0.9, (za + zb) / 2)
                    poly([P(xa, ya, za), P(xa, ya, zb), P(xa, yb, zb), P(xa, yb, za)], wc, (za + zb) / 2)
                    if DETAIL and (z0 - camz) < 70:
                        zm = (za + zb) / 2
                        poly([P(xa, ya, zm - 0.04), P(xa, ya, zm + 0.04), P(xa, yb, zm + 0.04), P(xa, yb, zm - 0.04)], c * 0.85, zm)

    def _person(self, img, p, P, fogc, camz):
        x, z, green = p['x'], p['z'], p.get('green', 0.0)
        sc = 640.0 * S / max(z - camz, 0.3)
        fx, fy = P(x, 0, z)
        body = col(0.30, 0.24, 0.20)
        layer = np.zeros_like(img) if green > 0 else None
        tgt = layer if layer is not None else img
        def C(c):
            return tuple(float(v) for v in c)
        # legs
        for o in (-0.12, 0.12):
            cv2.line(tgt, (int(fx + o * sc), int(fy)), (int(fx + o * sc * 0.8), int(fy - 0.85 * sc)), C(col(0.18, 0.18, 0.2)), max(1, int(0.16 * sc)), cv2.LINE_AA)
        # torso
        cv2.ellipse(tgt, (int(fx), int(fy - 1.2 * sc)), (max(1, int(0.25 * sc)), max(1, int(0.42 * sc))), 0, 0, 360, C(body), -1, cv2.LINE_AA)
        for o in (-1, 1):
            cv2.line(tgt, (int(fx + o * 0.24 * sc), int(fy - 1.5 * sc)), (int(fx + o * 0.3 * sc), int(fy - 0.95 * sc)), C(body * 0.9), max(1, int(0.11 * sc)), cv2.LINE_AA)
        cv2.circle(tgt, (int(fx), int(fy - 1.75 * sc)), max(1, int(0.13 * sc)), C(col(0.16, 0.12, 0.1)), -1, cv2.LINE_AA)
        if layer is not None:
            m = (layer.sum(2, keepdims=True) > 0).astype(np.float32)
            m = cv2.GaussianBlur(m, (0, 0), 1.2 * S).reshape(H, W, 1)
            g = col(0.35, 1.0, 0.6)
            mixed = lerp(layer, g * 0.8, green)
            img[:] = img * (1 - m * (1 - 0.25 * green)) + mixed * m
            img += green * 0.5 * fblur(m * g, 14 * S)


# ---------------------------------------------------------------- dead tree
def dead_tree(img, x, y, h, seed, color=(0.12, 0.11, 0.10)):
    r = RNG(seed)
    x, y, h = u(x), u(y), u(h)

    def br(x, y, a, l, w, d):
        if d == 0 or l < 3 * S:
            return
        x2, y2 = x + l * math.cos(a), y - l * math.sin(a)
        cv2.line(img, (int(x), int(y)), (int(x2), int(y2)), color, max(1, int(w)), cv2.LINE_AA)
        for _ in range(2):
            br(x2, y2, a + r.normal(0, 0.55), l * r.uniform(0.6, 0.8), w * 0.65, d - 1)
    br(x, y, math.pi / 2 + r.normal(0, 0.1), h * 0.4, h * 0.05, 8 if DETAIL else 7)


# ---------------------------------------------------------------- scenes
@lru_cache(maxsize=None)
def cloud_layer():
    return fbm(320, 360, 3, octaves=5, base=3)


def sc_map_intro(t, T, f):
    tex = terrain_tex(None, 21, True)
    p = smooth(t / T)
    span = lerp(760, 300, p)
    img, M = tilt_view(tex, 1100, 1180 - 230 * p, span, hz=lerp(0.0, 0.2, p), depth=1.3, mountains=False,
                       haze=col(0.70, 0.74, 0.80), rot=lerp(-0.12, 0.04, p))
    # drifting clouds
    cl = cloud_layer()
    off = int(t * 3)  # slow drift, no wrap-around seam
    cl = cv2.resize(cl[:, off:off + 180], (W, H))[..., None]
    img = lerp(img, col(0.95, 0.95, 0.97), smooth((cl - 0.55) * 3) * 0.55 * (1 - p * 0.6))
    (tx, ty), = project(M, [(1100, 950)])
    pulse = 0.5 + 0.5 * math.sin(t * 6)
    add_glow(img, tx, ty, u(10 + 8 * pulse), col(1.0, 0.25, 0.15) * 1.2)
    add_glow(img, tx, ty, u(3), col(1, 1, 1))
    return finish(img, f, grade=(0.98, 1.0, 1.04))


def sc_city_aerial(t, T, f):
    tex = city_tex()
    p = smooth(t / T)
    img, M = tilt_view(tex, 1024, 1024 + lerp(200, 0, p), lerp(900, 500, p), hz=0.26, depth=2.3, rot=lerp(0.2, -0.05, p))
    return finish(bloom(img, 0.9, 0.3), f)


STREET = None


def street():
    global STREET
    if STREET is None:
        STREET = Street(4)
    return STREET


def sc_street_flash(t, T, f):
    st = street()
    camz = t * 0.8
    person = [dict(x=0.6, z=camz + 5.5)]
    img, P = st.render(camz, camx=math.sin(t * 0.5) * 0.3, people=person)
    sx, sy = W / 2, H * 0.43 - u(30)
    k = smooth((t - 0.6) / 1.2)
    img += radial(sx, sy, u(lerp(8, 110, k))) * col(1.0, 0.95, 0.85) * (0.5 + 2.5 * k)
    img += radial(sx, sy, u(lerp(4, 30, k))) * 3.0 * k
    white = smooth((t - (T - 2.2)) / 1.6)
    img = lerp(img, col(1.0, 0.98, 0.95), white * 0.92)
    return finish(bloom(img, 0.8, 1.2), f)


def sc_top_fireball(t, T, f):
    tex = city_tex()
    img, M = tilt_view(tex, 1024, 1024, 560, hz=0.24, depth=2.1)
    (cx, cy), = project(M, [(1024, 980)])
    k = smooth(t / (T * 0.8))
    rad = u(lerp(10, 140, k))
    ground_ring(img, M, 1024, 980, lerp(20, 330, k), col(1.0, 0.85, 0.6), 3, 1.0)
    img = lerp(img, col(0.85, 0.76, 0.65), radial(cx, cy, rad * 2.2) * 0.6 * k)
    img += radial(cx, cy - rad * 0.3, rad) * col(1.6, 1.0, 0.55) * 1.4
    img += radial(cx, cy - rad * 0.3, rad * 0.45) * 2.0
    # fireball churning surface
    for i in range(18):
        a = i * 2.4 + t * 1.5
        draw_puff(img, cx + math.cos(a) * rad * 0.7, cy - rad * 0.3 + math.sin(a) * rad * 0.5, rad * 0.35,
                  col(1.4, 0.75, 0.35), 0.35 * k, i)
    return finish(shake(bloom(img, 0.85, 1.0), 4 * k, f), f)


def sc_street_vapor(t, T, f):
    st = street()
    camz = 2 + t * 1.2
    img, P = st.render(camz, people=[dict(x=-2, z=40), dict(x=3, z=70)])
    k = smooth(t / (T * 0.45))
    hzy = H * 0.43
    img += radial(W / 2, hzy - u(120), u(lerp(60, 520, k))) * col(1.0, 0.9, 0.75) * (1 + 3 * k)
    w2 = smooth((t - T * 0.4) / (T * 0.25))
    img = lerp(img, col(1.0, 0.97, 0.92), w2 * 0.95)
    o = smooth((t - T * 0.65) / (T * 0.3))
    orange = lerp(col(0.95, 0.62, 0.38), col(0.75, 0.42, 0.25), np.clip(_yy / H, 0, 1)[..., None])
    img = lerp(img, orange, o)
    return finish(bloom(img, 0.85, 0.8), f)


def sc_street_wave(t, T, f):
    st = street()
    camz = 0.5
    k = t / T
    dust_z = lerp(320, camz + 3, smooth(k ** 0.8))
    img, P = st.render(camz, collapse=(dust_z + 30, lerp(1.0, 0.2, k)), dust_z=dust_z,
                       sky=(col(0.70, 0.50, 0.36), col(0.86, 0.66, 0.48)), fog=col(0.80, 0.64, 0.50),
                       people=[dict(x=1.5, z=30), dict(x=-1, z=55)])
    r = RNG(7)
    for i in range(320 if DETAIL else 220):
        x = r.uniform(-40, 40)
        y = r.uniform(0, 1) ** 1.6 * 55
        zz = dust_z + r.uniform(0, 25)
        sx, sy = P(x, y, zz)
        rr = u(640) * r.uniform(3, 7) / max(zz - camz, 0.3)
        draw_puff(img, sx + math.sin(t * 2 + i) * u(6), sy, rr, col(0.66, 0.54, 0.44) * r.uniform(0.8, 1.1), 0.85, i)
    return finish(shake(img, 3 + 10 * smooth(k), f), f)


def ruins(t, f, green=0.0, dust=0.0, person=True, warm=False):
    tex = rubble_tex()
    img, M = tilt_view(tex, 512, 512 + t * 6, 300, hz=0.33, depth=2.6, haze=col(0.58, 0.56, 0.54), mountains=False, base=1024)
    hzy = H * 0.33
    img = np.where(_yy[..., None] < hzy, lerp(col(0.42, 0.40, 0.39), col(0.66, 0.62, 0.58), (_yy / hzy)[..., None]), img)
    u8 = img  # draw ruins silhouettes
    r = RNG(12)
    for i in range(10):  # broken building stubs on horizon
        x = r.uniform(0, W)
        w, h = u(r.uniform(30, 90)), u(r.uniform(30, 120))
        pts = np.array([[x, hzy + u(5)], [x + w, hzy + u(5)], [x + w, hzy - h * r.uniform(0.3, 1)], [x + w * 0.6, hzy - h],
                        [x + w * 0.3, hzy - h * 0.5], [x, hzy - h * 0.8]], np.int32)
        cv2.fillPoly(u8, [pts], (0.40, 0.38, 0.37), cv2.LINE_AA)
    for i, (x, h) in enumerate(((90, 300), (600, 380), (420, 160), (230, 120))):
        dead_tree(img, x + math.sin(t * 0.4) * 6, 1280 * 0.62 + h * 0.4, h, 40 + i)
    if person:
        st = Street(1)
        st._person(img, dict(x=0.0, z=4.2, green=green), lambda x, y, z: (W / 2 + u(640) * x / z, H * 0.43 - u(640) * (y - 1.7) / z),
                   None, 0.0)
    if dust > 0:
        rr = RNG(3)
        for i in range(260):
            x = rr.uniform(0, W)
            y = (rr.uniform(0, H) + t * u(rr.uniform(30, 90))) % H
            cv2.circle(img, (int(x), int(y)), int(u(rr.uniform(1, 3))), (0.85, 0.83, 0.78), -1, cv2.LINE_AA)
        img = lerp(img, col(0.62, 0.60, 0.56), dust * 0.25)
    return img


def sc_ruins_rad(t, T, f):
    g = smooth((t - 1.0) / 1.5)
    return finish(ruins(t, f, green=g), f, grade=(0.98, 1.02, 0.98))


def sc_street_wind(t, T, f):
    st = street()
    camz = 1 + t * 0.5
    img, P = st.render(camz, collapse=(400, 0.75), sky=(col(0.48, 0.40, 0.36), col(0.80, 0.62, 0.48)),
                       fog=col(0.72, 0.60, 0.50), fogd=90, people=[dict(x=1.2, z=camz + 7)])
    r = RNG(11)
    for i in range(14):  # fires along the street
        z = r.uniform(25, 200)
        sx, sy = P(r.choice([-11, 11]), r.uniform(4, 20), z)
        fl = 0.7 + 0.3 * math.sin(t * 9 + i)
        add_glow(img, sx, sy, u(640) * 5 / z, col(1.2, 0.5, 0.15) * fl)
    for i in range(60):  # smoke drifting sideways
        x = (r.uniform(-u(200), W + u(200)) + t * u(r.uniform(120, 260))) % (W + u(400)) - u(200)
        y = r.uniform(H * 0.1, H * 0.5)
        draw_puff(img, x, y, u(r.uniform(60, 140)), col(0.42, 0.36, 0.33), 0.35, i)
    for i in range(160):  # flying debris streaks
        x = (r.uniform(0, W) + t * u(r.uniform(500, 900))) % W
        y = r.uniform(H * 0.3, H)
        cv2.line(img, (int(x), int(y)), (int(x - u(25)), int(y + u(3))), (0.75, 0.68, 0.6), max(1, int(S)), cv2.LINE_AA)
    return finish(shake(bloom(img, 0.85, 0.6), 3, f), f)


def sc_skin_burn(t, T, f):
    img = np.empty((H, W, 3), np.float32)
    p = t / T
    base = H * 0.55 - u(p * 60)
    y = (_yy - base) / S
    img[:] = col(0.05, 0.04, 0.04)
    layers = [(-1e9, 0, col(0.10, 0.08, 0.07)), (0, 40, col(0.40, 0.20, 0.12)), (40, 160, col(0.62, 0.30, 0.20)),
              (160, 1e9, col(0.45, 0.22, 0.18))]
    n = fbm(H // 2, W // 2, 8, 6, 6)
    n = cv2.resize(n, (W, H))[..., None]
    for a, b, c in layers:
        m = ((y >= a) & (y < b))[..., None]
        img = np.where(m, c * (0.7 + 0.6 * n), img)
    k = smooth(p * 1.4)
    # glowing burned surface + nerve endings
    glow = np.zeros_like(img)
    surf = np.exp(-((y - 4) / 10) ** 2)[..., None]
    glow += surf * col(1.4, 0.6, 0.2) * k
    r = RNG(4)
    for i in range(14):
        x = u(40 + i * 48 + r.uniform(-10, 10))
        pts = [(x, base + u(150))]
        for j in range(16 if DETAIL else 8):
            px, py = pts[-1]
            pts.append((px + u(r.normal(0, 6 if not DETAIL else 4)), py - u(18 if not DETAIL else 9)))
        cv2.polylines(glow, [np.array(pts, np.int32)], False, (1.6 * k, 1.1 * k, 0.6 * k), max(2, int(u(2))), cv2.LINE_AA)
        top = pts[-1]
        cv2.ellipse(glow, (int(top[0]), int(top[1] + u(6))), (int(u(14)), int(u(6))), 0, 180, 360, (1.5 * k, 0.9 * k, 0.4 * k), max(2, int(u(2))), cv2.LINE_AA)
    img += glow + fblur(glow, u(12)) * 1.5
    # heat embers above surface
    for i in range(90):
        ex = r.uniform(0, W)
        ey = base - u((r.uniform(0, 400) + t * r.uniform(40, 100)) % 400)
        cv2.circle(img, (int(ex), int(ey)), int(u(2)), (1.4 * k, 0.6 * k, 0.2 * k), -1, cv2.LINE_AA)
    img = img * (0.9 + 0.1 * math.sin(t * 7))
    return finish(bloom(img, 0.8, 0.8), f)


def sc_top_rings(t, T, f):
    tex = city_tex()
    img, M = tilt_view(tex, 1024, 1024, 760, hz=0.22, depth=2.2)
    (cx, cy), = project(M, [(1024, 1000)])
    p = t / T
    # damage heat-map
    heat = smooth((p - 0.35) / 0.3)
    a = np.linspace(0, 2 * math.pi, 90)
    for rad, c, alpha in ((300, col(0.9, 0.2, 0.15), 0.35), (160, col(1.0, 0.3, 0.2), 0.45)):
        pts = project(M, np.stack([1024 + rad * np.cos(a), 1000 + rad * np.sin(a)], 1)).astype(np.int32)
        m = np.zeros((H, W), np.float32)
        cv2.fillPoly(m, [pts], 1.0, cv2.LINE_AA)
        m = fblur(m, u(25))[..., None]
        img = lerp(img, c, m * alpha * heat)
    ring_r = lerp(60, 380, smooth(p / 0.35))
    ground_ring(img, M, 1024, 1000, ring_r, col(1.0, 0.95, 0.85), 3, 0.8)
    for i, rr in enumerate((120, 240, 380)):
        ground_ring(img, M, 1024, 1000, rr, col(0.9, 0.88, 0.82) * smooth((p - 0.3 - i * 0.1) / 0.1) * 0.6, 2, 0.3)
    mushroom(img, cx, cy, u(120), 0.55 + 0.3 * p, seed=5)
    return finish(img, f)


def sc_cloud_tall(t, T, f):
    tex = terrain_tex(None, 13)
    img, M = tilt_view(tex, 1024, 1024, 900, hz=0.66, depth=3.0, haze=col(0.80, 0.78, 0.75))
    p = t / T
    # Everest-like peak for scale on the right
    pk = np.array([[W * 0.62, H * 0.66], [W * 0.80, H * 0.50], [W * 0.86, H * 0.53], [W * 1.05, H * 0.66]], np.int32)
    cv2.fillPoly(img, [pk], (0.70, 0.70, 0.72), cv2.LINE_AA)
    snow = np.array([[W * 0.74, H * 0.545], [W * 0.80, H * 0.50], [W * 0.86, H * 0.53], [W * 0.88, H * 0.55]], np.int32)
    cv2.fillPoly(img, [snow], (0.95, 0.95, 0.97), cv2.LINE_AA)
    mushroom(img, W * 0.42, H * 0.665, u(150), 0.45 + 0.55 * p, seed=7, fire=max(0, 0.35 - p) * 1.5)
    return finish(img, f)


def sc_ruins_dust(t, T, f):
    return finish(ruins(t, f, person=False, dust=smooth(t / 2)), f, grade=(1.0, 1.0, 0.97))


def sc_map_plume(t, T, f):
    tex = terrain_tex(None, 21, True)
    img, M = tilt_view(tex, 1100, 1050, 650, hz=0.2, depth=1.5, mountains=False, haze=col(0.72, 0.74, 0.78))
    (tx, ty), = project(M, [(1100, 950)])
    p = smooth(t / T)
    ln = u(lerp(30, 520, p))
    ang = math.radians(-18)
    m = np.exp(-(((_xx - tx) * math.cos(ang) + (_yy - ty) * math.sin(ang) - ln / 2) / (ln / 2 + 1)) ** 2
               - ((-(_xx - tx) * math.sin(ang) + (_yy - ty) * math.cos(ang)) / u(20 + 70 * p)) ** 2)
    n = cv2.resize(fbm(H // 4, W // 4, 9, 5, 4), (W, H))
    m = np.clip(m * (0.6 + 0.8 * n), 0, 1)[..., None]
    img = lerp(img, col(0.55, 0.50, 0.45), m * 0.85)
    add_glow(img, tx, ty, u(9), col(1.0, 0.3, 0.2))
    mushroom(img, tx, ty, u(26), 1.0, seed=2)
    return finish(img, f)


def sc_street_green(t, T, f):
    st = street()
    camz = t * 0.6
    img, P = st.render(camz, sky=(col(0.58, 0.58, 0.55), col(0.80, 0.78, 0.72)), fog=col(0.74, 0.72, 0.66), fogd=120,
                       people=[dict(x=0.2, z=camz + 5.5, green=smooth((t - 0.8) / 1.0))])
    r = RNG(5)
    for i in range(300):
        x = r.uniform(0, W)
        y = (r.uniform(0, H) + t * u(r.uniform(40, 120))) % H
        cv2.circle(img, (int(x), int(y)), int(u(r.uniform(1, 3))), (0.86, 0.84, 0.78), -1, cv2.LINE_AA)
    return finish(img, f, grade=(0.98, 1.02, 0.96))


def sc_cells(t, T, f):
    img = np.empty((H, W, 3), np.float32)
    img[:] = lerp(col(0.25, 0.04, 0.05), col(0.10, 0.01, 0.02), np.clip(_yy / H, 0, 1)[..., None])
    r = RNG(6)
    cells = sorted([(r.uniform(-50, 770), r.uniform(-50, 1330), r.uniform(0.3, 1.0)) for _ in range(70)], key=lambda c: c[2])
    for i, (x, y, d) in enumerate(cells):
        rad = u(40 + 110 * d)
        x = u(x + math.sin(t * 0.5 + i) * 15 * d)
        y = u((y - t * 20 * d) % 1480 - 100)
        blur = u((0.6 - d) * 25) if d < 0.6 else 0
        mg = int(rad + 3 * blur + 4)
        x0, y0, x1, y1 = max(0, int(x) - mg), max(0, int(y) - mg), min(W, int(x) + mg), min(H, int(y) + mg)
        if x1 <= x0 or y1 <= y0:
            continue
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        m = np.zeros((y1 - y0, x1 - x0), np.float32)
        cv2.circle(m, (int(x) - x0, int(y) - y0), int(rad), 1.0, -1, cv2.LINE_AA)
        if blur:
            m = fblur(m, blur)
        m = m[..., None]
        sh = np.exp(-(((xx - (x - rad * 0.3)) ** 2 + (yy - (y - rad * 0.35)) ** 2) / (2 * (rad * 0.9) ** 2)))[..., None]
        c = col(0.75, 0.10, 0.12) * (0.4 + 0.9 * sh) * (0.5 + 0.5 * d)
        if DETAIL and d > 0.6:  # membrane texture
            c = c * (0.92 + 0.16 * cv2.resize(fbm(16, 16, i, 3, 2), (x1 - x0, y1 - y0))[..., None])
        roi = img[y0:y1, x0:x1]
        roi[:] = roi * (1 - m) + c * m
    # mutating cell in focus
    k = smooth((t - 1.0) / 2.0)
    cx, cy, rr = W / 2, H * 0.5, u(150)
    m = np.zeros((H, W), np.float32)
    pts = [(cx + (rr + u(18) * math.sin(a * 5 + t * 2) * k) * math.cos(a), cy + (rr + u(18) * math.sin(a * 5 + t * 2) * k) * math.sin(a))
           for a in np.linspace(0, 2 * math.pi, 240)]
    cv2.fillPoly(m, [np.array(pts, np.int32)], 1.0, cv2.LINE_AA)
    m = m[..., None]
    sh = radial(cx - u(50), cy - u(60), u(140))
    c = lerp(col(0.85, 0.15, 0.15), col(0.25, 0.05, 0.08), k) * (0.4 + 0.9 * sh)
    img = img * (1 - m) + c * m
    add_glow(img, cx, cy, u(30), col(0.9, 0.2, 0.3) * (0.4 + 0.4 * math.sin(t * 4)) * k)
    return finish(bloom(img, 0.7, 0.4), f, grade=(1.0, 1.0, 1.0))


def sc_history(t, T, f):
    tex = terrain_tex(None, 15)
    img, M = tilt_view(tex, 1024, 1024, 900, hz=0.62, depth=3.0, haze=col(0.82, 0.78, 0.72))
    mushroom(img, W / 2, H * 0.625, u(170), 0.75 + 0.25 * t / T, seed=9)
    sep = 1 - smooth((t - T * 0.35) / (T * 0.3))
    lum = img.mean(axis=2, keepdims=True)
    sepia = lum * col(1.05, 0.92, 0.75)
    img = lerp(img, sepia, sep)
    # old film scratches during the 1945 part
    r = RNG(f)
    if sep > 0.05:
        for _ in range(3):
            x = int(r.uniform(0, W))
            cv2.line(img, (x, 0), (x, H), (0.9 * sep, 0.85 * sep, 0.75 * sep), max(1, int(S)))
    return finish(img, f, grain=0.025 + 0.04 * sep)


def sc_ending(t, T, f):
    img = sc_history(T * 0.9 + t * 0.2, T, f)
    r = RNG(1)
    for i in range(80):
        x = r.uniform(0, W) + u(math.sin(t + i) * 10)
        y = H - ((r.uniform(0, H) + t * u(r.uniform(30, 80))) % H)
        cv2.circle(img, (int(x), int(y)), int(u(2)), (1.0, 0.6, 0.25), -1, cv2.LINE_AA)
    return np.clip(img * (1 - smooth(t / T) * 0.95), 0, 1)


# ============================================================================
# TRUE 3D LAYER: perspective camera, extruded city, ray-marched terrain,
# textured 3D solids, lit spheres, shaded people.  Later definitions of sc_*
# override the earlier 2.5D versions.
# ============================================================================
SUN = np.array([-0.45, -0.62, 0.64])
SUN /= np.linalg.norm(SUN)


class Cam:
    """Pinhole camera. World: x east, y north, z up (metres)."""

    def __init__(self, pos, yaw, pitch, fov=50.0, cy=0.5):
        self.pos = np.array(pos, np.float64)
        self.f = (W / 2) / math.tan(math.radians(fov) / 2)
        cyw, syw, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch)
        fwd = np.array([syw * cp, cyw * cp, -sp])
        right = np.array([cyw, -syw, 0.0])
        up = np.cross(right, fwd)
        self.R = np.stack([right, -up, fwd])  # rows: cam x (right), cam y (down), cam z (forward)
        self.cx, self.cy = W / 2, H * cy

    def project(self, P):
        c = (np.asarray(P, np.float64) - self.pos) @ self.R.T
        z = c[..., 2]
        zs = np.maximum(z, 1e-6)
        return np.stack([self.cx + self.f * c[..., 0] / zs, self.cy + self.f * c[..., 1] / zs], -1), z

    def ground_h(self):
        K = np.array([[self.f, 0, self.cx], [0, self.f, self.cy], [0, 0, 1.0]])
        t = -self.R @ self.pos
        return K @ np.stack([self.R[:, 0], self.R[:, 1], t], 1)

    def horizon_y(self):
        if abs(self.R[1, 2]) < 1e-9:
            return -1e9
        return self.cy - self.f * self.R[2, 2] / self.R[1, 2]

    def rays(self, w, h):
        ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
        a = ((xs + 0.5) * (W / w) - self.cx) / self.f
        b = ((ys + 0.5) * (H / h) - self.cy) / self.f
        R_ = self.R.astype(np.float32)
        return [a * R_[0, i] + b * R_[1, i] + R_[2, i] for i in range(3)]


def look_at(pos, target, fov=50.0, cy=0.5):
    d = np.array(target, float) - np.array(pos, float)
    return Cam(pos, math.atan2(d[0], d[1]), math.atan2(-d[2], math.hypot(d[0], d[1])), fov, cy)


def sky_fill(img, cam, top, hz):
    hy = cam.horizon_y()
    rows = np.arange(H, dtype=np.float32)
    k = smooth(np.clip((rows - (hy - H * 0.7)) / (H * 0.7), 0, 1))[:, None, None]
    img[:] = lerp(top, hz, k)


_MIPS = {}


def get_mips(name, tex):
    if name not in _MIPS:
        lv = [tex]
        while min(lv[-1].shape[:2]) > 128 and len(lv) < 7:
            lv.append(cv2.pyrDown(lv[-1]))
        _MIPS[name] = lv
    return _MIPS[name]


def ground_view(img, cam, name, tex, mpp, origin, haze, fogd):
    """Perspective-correct, mip-mapped textured ground plane z=0."""
    lv = get_mips(name, tex)
    Hg = cam.ground_h()
    hy = cam.horizon_y()
    y0 = int(np.clip(math.ceil(hy) + 1, 0, H))
    if y0 >= H:
        return
    rows = np.arange(y0, H, dtype=np.float64)
    b = (rows - cam.cy) / cam.f
    dz = cam.R[1, 2] * b + cam.R[2, 2]
    depth = cam.pos[2] / np.maximum(-dz, 1e-9)
    obl = np.sqrt(1 + b * b) / np.maximum(-dz, 1e-9)
    lod = np.log2(np.maximum(depth / cam.f / mpp * np.sqrt(np.clip(obl, 1, 40)), 1e-6))
    lod = np.clip(lod, 0, len(lv) - 1)
    out = np.zeros((H - y0, W, 3), np.float32)
    for k in range(len(lv)):
        w = np.clip(1 - np.abs(lod - k), 0, 1)
        nz = np.nonzero(w > 0)[0]
        if len(nz) == 0:
            continue
        r0, r1 = nz[0], nz[-1] + 1
        A = np.array([[mpp * 2 ** k, 0, origin[0]], [0, mpp * 2 ** k, origin[1]], [0, 0, 1]])
        T = np.array([[1, 0, 0], [0, 1, -(y0 + r0)], [0, 0, 1.0]])
        seg = cv2.warpPerspective(lv[k], T @ Hg @ A, (W, int(r1 - r0)), flags=cv2.INTER_LINEAR,
                                  borderMode=cv2.BORDER_CONSTANT, borderValue=tuple(float(v) * 255 for v in haze))
        out[r0:r1] += seg.astype(np.float32) * (w[r0:r1, None, None] / 255.0).astype(np.float32)
    fk = (1 - np.exp(-depth / fogd)).astype(np.float32)[:, None, None]
    img[y0:] = lerp(out, haze, fk)
    hb = np.exp(-((np.arange(H, dtype=np.float32) - hy) / u(50)) ** 2)[:, None, None] * 0.8
    img[:] = lerp(img, haze, hb)


def horizon_ridge(img, cam, seed=77, amp=60, color=col(0.62, 0.60, 0.58), haze=None):
    hy = cam.horizon_y()
    if not (0 < hy < H):
        return
    my = hy - u(6) - ridge(seed, u(amp))
    mask = (_yy > my[None, :]) & (_yy < hy + 1)
    c = lerp(color, haze, 0.45) if haze is not None else color
    img[mask] = c


# ---------------------------------------------------------------- city world
CITY_EXT = 10000.0  # city texture spans [-EXT, EXT] metres


def city_palette(r):
    pal = [col(0.82, 0.76, 0.66), col(0.74, 0.68, 0.59), col(0.69, 0.57, 0.47), col(0.86, 0.85, 0.81),
           col(0.63, 0.60, 0.56), col(0.78, 0.70, 0.56)]
    return pal[int(r.integers(len(pal)))] * r.uniform(0.92, 1.06)


@lru_cache(maxsize=None)
def city_world():
    r = RNG(5)
    P, road, RC = 110.0, 16.0, 9500.0
    B = {k: [] for k in ('x0', 'y0', 'x1', 'y1', 'h', 'c')}
    parks = []
    for bx in np.arange(-RC, RC, P):
        for by in np.arange(-RC, RC, P):
            cx_, cy_ = bx + P / 2, by + P / 2
            rr = math.hypot(cx_, cy_)
            if rr > RC or abs(rr - 2600) < 75 or abs(rr - 5200) < 75:
                continue
            if abs(cx_ - cy_) / 1.414 < 62 or abs(cx_ + cy_) / 1.414 < 62:
                continue
            if r.random() < max(0.0, (rr - 6500) / 4500):
                continue
            x0, y0 = bx + road / 2, by + road / 2
            span = P - road
            if r.random() < 0.06:
                parks.append((x0, y0, x0 + span, y0 + span))
                continue
            nx, ny = int(r.integers(2, 4)), int(r.integers(2, 4))
            ws, hs = span / nx, span / ny
            tall = 1.6 - min(rr / 7000, 1.2)
            for i in range(nx):
                for j in range(ny):
                    ins = r.uniform(1.5, 4.5)
                    floors = r.integers(2, 8) * tall + 1
                    if r.random() < 0.015 * tall:
                        floors = r.integers(14, 32)
                    B['x0'].append(x0 + i * ws + ins)
                    B['y0'].append(y0 + j * hs + ins)
                    B['x1'].append(x0 + (i + 1) * ws - ins)
                    B['y1'].append(y0 + (j + 1) * hs - ins)
                    B['h'].append(float(floors) * 3.2 + 1.0)
                    B['c'].append(city_palette(r))
    B = {k: np.array(v, np.float64) for k, v in B.items()}
    B['cx'] = (B['x0'] + B['x1']) / 2
    B['cy'] = (B['y0'] + B['y1']) / 2
    B['rad'] = np.hypot(B['x1'] - B['x0'], B['y1'] - B['y0']) / 2 + B['h'] / 2
    B['dmg'] = RNG(9).uniform(0.12, 0.45, len(B['h']))
    B['parks'] = parks
    return B


@lru_cache(maxsize=None)
def city_ground():
    n = 8192 if DETAIL else 4096
    mpp = 2 * CITY_EXT / n
    Bw = city_world()

    def px(v):
        return (np.asarray(v) + CITY_EXT) / mpp

    noise = cv2.resize(fbm(1024, 1024, 41, 7, 4), (n, n))[..., None]
    desert = lerp(col(0.70, 0.62, 0.50), col(0.80, 0.72, 0.58), noise)
    img = (np.clip(desert, 0, 1) * 255).astype(np.uint8)
    yy, xx = np.ogrid[0:n, 0:n]
    city = ((xx * mpp - CITY_EXT) ** 2 + (yy * mpp - CITY_EXT) ** 2) < 9600 ** 2
    asphalt = (np.clip(lerp(col(0.40, 0.39, 0.38), col(0.47, 0.46, 0.44), noise), 0, 1) * 255).astype(np.uint8)
    img[city] = asphalt[city]
    r = RNG(3)
    lot = []
    P, road = 110.0, 16.0
    for bx in np.arange(-9500, 9500, P):
        for by in np.arange(-9500, 9500, P):
            if math.hypot(bx + P / 2, by + P / 2) > 9500:
                continue
            a = (int(px(bx + road / 2)), int(px(by + road / 2)))
            b = (int(px(bx + P - road / 2)), int(px(by + P - road / 2)))
            t = int(r.integers(150, 180))
            cv2.rectangle(img, a, b, (t + 18, t + 10, t - 4), -1)
    for x0, y0, x1, y1 in Bw['parks']:
        cv2.rectangle(img, (int(px(x0)), int(px(y0))), (int(px(x1)), int(px(y1))), (92, 112, 70), -1)
        for _ in range(40):
            tx, ty = r.uniform(x0 + 4, x1 - 4), r.uniform(y0 + 4, y1 - 4)
            cv2.circle(img, (int(px(tx)), int(px(ty))), max(1, int(3.5 / mpp)), (58, 84, 48), -1, cv2.LINE_AA)
    # boulevards + rings
    c0 = int(px(0))
    for ang in (math.pi / 4, 3 * math.pi / 4, 0, math.pi / 2):
        dx, dy = int(math.cos(ang) * n), int(math.sin(ang) * n)
        cv2.line(img, (c0 - dx, c0 - dy), (c0 + dx, c0 + dy), (98, 96, 94), max(2, int(34 / mpp)), cv2.LINE_AA)
    for rr in (2600, 5200):
        cv2.circle(img, (c0, c0), int(rr / mpp), (98, 96, 94), max(2, int(40 / mpp)), cv2.LINE_AA)
    # building shadows (sun) then roofs
    shadow = np.zeros((n, n), np.uint8)
    sx, sy = -SUN[0] / SUN[2], -SUN[1] / SUN[2]
    X0, Y0, X1, Y1, Hh = px(Bw['x0']), px(Bw['y0']), px(Bw['x1']), px(Bw['y1']), Bw['h'] / mpp
    for i in range(len(Hh)):
        ox, oy = sx * Hh[i], sy * Hh[i]
        pts = np.array([[X0[i], Y0[i]], [X1[i], Y0[i]], [X1[i], Y1[i]], [X0[i], Y1[i]],
                        [X0[i] + ox, Y0[i] + oy], [X1[i] + ox, Y0[i] + oy], [X1[i] + ox, Y1[i] + oy], [X0[i] + ox, Y1[i] + oy]])
        cv2.fillConvexPoly(shadow, cv2.convexHull((pts * 4).astype(np.int32)), 255, cv2.LINE_AA, 2)
    sh = cv2.GaussianBlur(shadow, (0, 0), 0.8).astype(np.float32)[..., None] / 255
    img = (img.astype(np.float32) * (1 - 0.42 * sh)).astype(np.uint8)
    roof = (np.clip(Bw['c'] * 1.05 + 0.04, 0, 1) * 255).astype(np.int32)
    for i in range(len(Hh)):
        cv2.rectangle(img, (int(X0[i]), int(Y0[i])), (int(X1[i]), int(Y1[i])), tuple(int(v) for v in roof[i]), -1)
    return img, mpp


def draw_boxes(img, cam, Bw, haze, fogd, maxd=3000.0, light=None, damage=None, detail_d=450.0, idx=None):
    """Painter's-algorithm renderer for axis-aligned extruded boxes."""
    cxs, cys, hs = Bw['cx'], Bw['cy'], Bw['h']
    if idx is None:
        d = np.stack([cxs - cam.pos[0], cys - cam.pos[1], hs / 2 - cam.pos[2]], 1)
        dist = np.sqrt((d ** 2).sum(1))
        c = d @ cam.R.T
        zc = np.maximum(c[:, 2], 1.0)
        rad = Bw['rad']
        lx = (W / 2) / cam.f
        ly = max(cam.cy, H - cam.cy) / cam.f
        keep = (dist < maxd) & (c[:, 2] > -rad) & (np.abs(c[:, 0]) < lx * zc + rad * 1.5) & (np.abs(c[:, 1]) < ly * zc + rad * 1.5)
        idx = np.nonzero(keep)[0]
        idx = idx[np.argsort(-dist[idx])]
    else:
        dist = np.sqrt((cxs - cam.pos[0]) ** 2 + (cys - cam.pos[1]) ** 2 + (hs / 2 - cam.pos[2]) ** 2)
    if len(idx) == 0:
        return
    x0, y0, x1, y1 = Bw['x0'][idx], Bw['y0'][idx], Bw['x1'][idx], Bw['y1'][idx]
    h = hs[idx].copy()
    base = Bw['c'][idx].copy()
    if damage is not None:
        dcx, dcy, drad = damage
        dd = np.hypot(cxs[idx] - dcx, cys[idx] - dcy)
        hit = dd < drad
        h[hit] = np.maximum(1.5, h[hit] * Bw['dmg'][idx][hit])
        base[hit] = base[hit] * 0.45 + col(0.30, 0.26, 0.22) * 0.55
    z0 = np.zeros_like(h)
    C = np.stack([np.stack([x0, y0, z0], 1), np.stack([x1, y0, z0], 1), np.stack([x1, y1, z0], 1), np.stack([x0, y1, z0], 1),
                  np.stack([x0, y0, h], 1), np.stack([x1, y0, h], 1), np.stack([x1, y1, h], 1), np.stack([x0, y1, h], 1)], 1)
    pr, zz = cam.project(C)
    ok = (zz > 0.5).all(1)
    faces = {'t': ([4, 5, 6, 7], (0, 0, 1)), 's': ([0, 1, 5, 4], (0, -1, 0)), 'n': ([3, 2, 6, 7], (0, 1, 0)),
             'w': ([0, 3, 7, 4], (-1, 0, 0)), 'e': ([1, 2, 6, 5], (1, 0, 0))}
    px_, py_, pz_ = cam.pos
    vis = {'t': pz_ > h, 's': py_ < y0, 'n': py_ > y1, 'w': px_ < x0, 'e': px_ > x1}
    fk = 1 - np.exp(-dist[idx] / fogd)
    cols = {}
    for k, (_, nrm) in faces.items():
        nrm = np.array(nrm, float)
        shade = 0.50 + 0.62 * max(0.0, float(nrm @ SUN))
        c = base * shade * (1.04 if k == 't' else 1.0)
        if light is not None:
            lp, lc, li, lr = light
            ctr = np.stack([(x0 + x1) / 2, (y0 + y1) / 2, h / 2], 1)
            v = lp - ctr
            dl = np.linalg.norm(v, axis=1)
            ndl = np.maximum(0, (v @ nrm) / np.maximum(dl, 1e-6))
            c = c + lc[None, :] * (li * ndl / (1 + (dl / lr) ** 2))[:, None]
        c = lerp(c, haze[None, :], fk[:, None])
        cols[k] = c.tolist()
    sub = 16.0
    prs = (pr * sub).astype(np.int32)
    vis_l = {k: v.tolist() for k, v in vis.items()}
    okl = ok.tolist()
    dl_ = dist[idx].tolist()
    for i in range(len(idx)):
        if not okl[i]:
            continue
        for k, (fi, _) in faces.items():
            if vis_l[k][i]:
                cv2.fillConvexPoly(img, prs[i, fi], cols[k][i], cv2.LINE_AA, 4)
        if dl_[i] < detail_d and h[i] > 6:  # floor lines + window bands on near buildings
            floors = int(h[i] / 3.2)
            for k in ('s', 'n', 'w', 'e'):
                if not vis_l[k][i]:
                    continue
                fi = faces[k][0]
                a, b = C[i, fi[0]], C[i, fi[1]]
                zs_ = np.arange(1, floors) * 3.2
                pts = np.concatenate([np.c_[np.full(len(zs_), a[0]), np.full(len(zs_), a[1]), zs_],
                                      np.c_[np.full(len(zs_), b[0]), np.full(len(zs_), b[1]), zs_ ]])
                pp, _ = cam.project(pts)
                lc_ = tuple(float(v) * 0.72 for v in cols[k][i])
                th = max(1, int(cam.f * 1.0 / max(dl_[i], 1)))
                for j in range(len(zs_)):
                    cv2.line(img, tuple((pp[j] * sub).astype(int)), tuple((pp[j + len(zs_)] * sub).astype(int)), lc_, th, cv2.LINE_AA, 4)


def city_scene(cam, t, f, haze=col(0.80, 0.78, 0.73), fogd=9000.0, light=None, damage=None, maxd=3200.0):
    img = np.empty((H, W, 3), np.float32)
    sky_fill(img, cam, col(0.56, 0.62, 0.70), col(0.86, 0.84, 0.80))
    horizon_ridge(img, cam, 77, 70, haze=haze)
    tex, mpp = city_ground()
    ground_view(img, cam, 'city', tex, mpp, (-CITY_EXT, -CITY_EXT), haze, fogd)
    draw_boxes(img, cam, city_world(), haze, fogd, maxd=maxd, light=light, damage=damage)
    return img


def ground_circle(img, cam, r, color, thick=3, glow=0.8, z=1.0):
    a = np.linspace(0, 2 * math.pi, 400)
    P = np.stack([r * np.cos(a), r * np.sin(a), np.full_like(a, z)], 1)
    pp, zz = cam.project(P)
    pp = pp[zz > 1]
    if len(pp) < 2:
        return
    layer = np.zeros_like(img)
    cv2.polylines(layer, [(pp * 16).astype(np.int32)], False, tuple(float(v) for v in color), max(1, int(thick * S)), cv2.LINE_AA, 4)
    img += layer + glow * fblur(layer, 9 * S)


def world_puff(img, cam, P, R, color, alpha, seed=0):
    (sx, sy), z = cam.project(np.array(P, float))
    if z < 1:
        return
    draw_puff(img, sx, sy, cam.f * R / z, color, alpha, seed)


def world_mushroom(img, cam, ground, top_h, phase, seed=5, fire=0.0, palette=None):
    (gx, gy), z = cam.project(np.array(ground, float))
    if z < 1:
        return
    s = cam.f * top_h / z / 2.6
    mushroom(img, gx, gy, s, phase, seed=seed, fire=fire, palette=palette)


# ---------------------------------------------------------------- terrain
@lru_cache(maxsize=None)
def terrain_world(kind):
    n = 4096 if DETAIL else 2048
    if kind == 'iran':
        ext = 700e3
    elif kind == 'plain':
        ext = 160e3
    else:
        ext = 240.0
    mpp = ext / n
    org = (-ext / 2, -ext / 2)
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    X = xx * mpp + org[0]
    Y = yy * mpp + org[1]
    base = fbm(n, n, 21 if kind == 'iran' else 33, octaves=9, base=3)
    hi = fbm(n, n, 22, octaves=6, base=24)
    ridged = 1 - np.abs(2 * fbm(n, n, 23, octaves=7, base=6) - 1)
    water = np.zeros((n, n), np.float32)
    if kind == 'iran':
        alb = np.exp(-((Y - 42e3 - 15e3 * np.sin(X / 90e3)) / 28e3) ** 2) * np.clip(1 - np.abs(X) / 300e3, 0, 1)
        zag = np.exp(-(((X + Y) * 0.707 + 170e3) / 70e3) ** 2)
        zag = np.exp(-(((X + Y) * 0.707 + 170e3) / 110e3) ** 2)
        r2 = (1 - np.abs(2 * fbm(n, n, 28, 7, 12) - 1)) ** 2
        hgt = (1300 * base ** 1.5 + 1500 * r2 * (0.4 + base) + 4200 * alb * (0.5 + 0.7 * ridged)
               + 2300 * zag * (0.45 + 0.7 * ridged) + 160 * hi)
        casp = Y - (120e3 + 25e3 * np.sin(X / 70e3) + 30e3 * (base - 0.5))
        gulf = ((X - 160e3) * -0.55 + (Y + 330e3) * -0.83) - 10e3 * (base - 0.5) * 6
        water = np.clip(np.maximum(casp / 6e3, gulf / 6e3), 0, 1)
        hgt = hgt * (1 - water) * 3.5  # vertical exaggeration so relief reads from orbit
        snow_h = 4600 * 3.5
    elif kind == 'plain':
        rng_ = np.exp(-((Y - 30e3) / 9e3) ** 2) * (0.5 + 0.8 * ridged) * np.clip((X + 10e3) / 30e3, 0, 1)
        peak = np.exp(-(((X - 18e3) / 6e3) ** 2 + ((Y - 24e3) / 5e3) ** 2))
        hills = fbm(n, n, 26, 6, 20)
        hgt = 500 * base + 260 * hills + 3600 * rng_ + 6500 * peak * (0.8 + 0.2 * ridged) + 60 * hi
        snow_h = 4200
    else:  # rubble field
        hgt = 0.35 * base + 0.25 * hi
        hm = np.zeros((n, n), np.float32)
        r = RNG(17)
        for _ in range(int(14000 if DETAIL else 5000)):
            x, y = r.integers(0, n, 2)
            sz = r.uniform(0.15, 1.2) / mpp
            pts = (np.array([[x, y]]) + r.normal(0, sz, (6, 2))).astype(np.int32)
            cv2.fillConvexPoly(hm, cv2.convexHull(pts), float(r.uniform(0.1, 0.9)), cv2.LINE_AA)
        hgt = hgt + cv2.GaussianBlur(hm, (0, 0), 1.0)
        snow_h = 1e9
    hgt = hgt.astype(np.float32)
    gy, gx = np.gradient(hgt, mpp)
    nrm = np.stack([-gx, -gy, np.ones_like(gx)], -1)
    nrm /= np.linalg.norm(nrm, axis=-1, keepdims=True)
    shade = np.clip(0.42 + 0.78 * np.maximum(0, nrm @ SUN.astype(np.float32)), 0, 1.4)[..., None]
    veg = fbm(n, n, 24, octaves=6, base=5)[..., None]
    if kind == 'rubble':
        c = lerp(col(0.30, 0.29, 0.28), col(0.66, 0.64, 0.60), np.clip(hgt[..., None] * 0.9 + 0.2 * veg, 0, 1))
    else:
        hn = hgt[..., None]
        hs_ = 3.5 if kind == 'iran' else 1.0
        tint = (0.6 * fbm(n, n, 27, 5, 4) + 0.4 * fbm(n, n, 29, 5, 40))[..., None]
        c = lerp(col(0.82, 0.72, 0.55), col(0.70, 0.52, 0.40), tint)
        c = lerp(c, col(0.50, 0.43, 0.36), np.clip(hn / (2500 * hs_), 0, 1))
        c = lerp(c, col(0.42, 0.47, 0.31), np.clip((veg - 0.58) * 3, 0, 0.6) * np.clip(1 - hn / (2500 * hs_), 0, 1))
        c = lerp(c, col(0.94, 0.95, 0.97), np.clip((hn - snow_h) / 600, 0, 1) * np.clip(nrm[..., 2:3] * 1.3, 0, 1))
    c = c * shade
    if kind == 'iran':
        wcol = lerp(col(0.12, 0.27, 0.40), col(0.06, 0.15, 0.27), base[..., None])
        c = lerp(c, wcol, water[..., None])
    tex = (np.clip(c, 0, 1) * 255).astype(np.uint8)
    return dict(h=hgt, tex=tex, mpp=mpp, org=org, hmax=float(hgt.max()) + 1, name='ter_' + kind)


def terrain_view(img, cam, kind, haze, fogd, tfar, tnear=1.0, steps=40, sky=None):
    T_ = terrain_world(kind)
    hm, mpp, (ox, oy), hmax = T_['h'], T_['mpp'], T_['org'], T_['hmax']
    if sky is None:
        sky_fill(img, cam, col(0.55, 0.61, 0.70), haze)
    else:
        sky_fill(img, cam, *sky)
    w2, h2 = W // 2, H // 2
    dx, dy, dz = cam.rays(w2, h2)
    px, py, pz = (float(v) for v in cam.pos)
    with np.errstate(divide='ignore', invalid='ignore'):
        if pz > hmax:
            t_lo = np.where(dz < 0, (pz - hmax) / -dz, np.inf)
        else:
            t_lo = np.zeros_like(dz)
        t_hi = np.where(dz < 0, pz / -dz, np.inf)
    t_lo = np.maximum(t_lo, tnear).astype(np.float32)
    t_hi = np.minimum(t_hi, tfar).astype(np.float32)
    valid = t_hi > t_lo
    t_lo = np.where(valid, t_lo, 1.0).astype(np.float32)
    ratio = np.where(valid, t_hi / t_lo, 1.0).astype(np.float32)

    def hsample(t):
        mx = ((px + t * dx) - ox) / mpp
        my = ((py + t * dy) - oy) / mpp
        return cv2.remap(hm, mx.astype(np.float32), my.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

    found = np.zeros(dz.shape, bool)
    lo = t_lo.copy()
    hi = t_lo.copy()
    prev = t_lo.copy()
    lr = np.log(ratio)
    for i in range(1, steps + 1):
        t = t_lo * np.exp(lr * (i / steps))
        hit = (~found) & valid & ((pz + t * dz) <= hsample(t) + 1e-3 * t)
        if i == steps:  # rays that reach sea level inside the range hit the ground plane
            hit |= (~found) & valid & (t_hi < tfar * 0.999)
        lo[hit] = prev[hit]
        hi[hit] = t[hit]
        found |= hit
        prev = t
    for _ in range(6):
        mid = (lo + hi) * 0.5
        below = (pz + mid * dz) <= hsample(mid)
        hi = np.where(below, mid, hi)
        lo = np.where(below, lo, mid)
    th = np.where(found, hi, tfar).astype(np.float32)
    mx = (((px + th * dx) - ox) / mpp).astype(np.float32)
    my = (((py + th * dy) - oy) / mpp).astype(np.float32)
    mxf = cv2.resize(mx, (W, H), interpolation=cv2.INTER_LINEAR)
    myf = cv2.resize(my, (W, H), interpolation=cv2.INTER_LINEAR)
    tf = cv2.resize(th, (W, H), interpolation=cv2.INTER_LINEAR)
    fm = cv2.resize(found.astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
    lv = get_mips(T_['name'], T_['tex'])
    lod = np.clip(np.log2(np.maximum(tf / cam.f / mpp, 1e-6)) + 0.3, 0, len(lv) - 1)
    out = np.zeros((H, W, 3), np.float32)
    for k in range(len(lv)):
        w = np.clip(1 - np.abs(lod - k), 0, 1)
        if not (w > 0).any():
            continue
        sc_ = 2.0 ** -k
        c = cv2.remap(lv[k], mxf * sc_, myf * sc_, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        out += c.astype(np.float32) * (w / 255.0)[..., None]
    dscale = {'iran': 1500.0, 'plain': 45.0, 'rubble': 0.35}[kind]
    dt = detail_tex()
    dn = dt.shape[0]
    wx = mxf * (mpp / dscale * dn / 8)
    wy = myf * (mpp / dscale * dn / 8)
    d1 = cv2.remap(dt, wx, wy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
    d2 = cv2.remap(dt, wy * 0.37 + 91.0, wx * -0.37 + 17.0, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
    fade = np.clip(1.6 - lod / 2.5, 0, 1)  # fade detail with distance
    out *= (1 + ((d1 - 0.5) * 0.22 + (d2 - 0.5) * 0.3)[..., None] * fade[..., None])
    fk = (1 - np.exp(-tf / fogd))[..., None]
    out = lerp(out, haze, fk)
    img[:] = lerp(img, out, fm)
    return tf


@lru_cache(maxsize=None)
def detail_tex():
    d = fbm(1024, 1024, 61, octaves=7, base=8)
    d = 0.5 * (d + np.roll(np.roll(d, 512, 0), 512, 1))
    return ((d - d.min()) / (d.max() - d.min())).astype(np.float32)


# ---------------------------------------------------------------- textured solids
def draw_textured_quad(img, quad, tex, shade=1.0):
    q = np.asarray(quad, np.float32)
    x0, y0 = int(max(0, math.floor(q[:, 0].min()))), int(max(0, math.floor(q[:, 1].min())))
    x1, y1 = int(min(W, math.ceil(q[:, 0].max()) + 1)), int(min(H, math.ceil(q[:, 1].max()) + 1))
    if x1 <= x0 or y1 <= y0:
        return
    th, tw = tex.shape[:2]
    src = np.float32([[0, 0], [tw, 0], [tw, th], [0, th]])
    dst = q - np.float32([x0, y0])
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(tex, M, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    m = np.zeros((y1 - y0, x1 - x0), np.float32)
    cv2.fillConvexPoly(m, (dst * 16).astype(np.int32), 1.0, cv2.LINE_AA, 4)
    m = m[..., None]
    roi = img[y0:y1, x0:x1]
    roi[:] = roi * (1 - m) + warped * shade * m


# ---------------------------------------------------------------- shaded person
def draw_person(img, fx, fy, sc, green=0.0, fog=None):
    """Volumetrically shaded person seen from behind. fx,fy = feet (px), sc = px per metre."""
    if sc < 2:
        return
    w2, hgt = int(0.55 * sc) + 4, int(1.95 * sc) + 4
    x0, y0 = int(fx) - w2, int(fy) - hgt
    lw, lh = 2 * w2, hgt + 4

    def P(x, y):  # metres relative to feet -> local px (x right, y up)
        return (int((w2 + x * sc) * 16), int((hgt - y * sc) * 16))

    parts = []
    m = np.zeros((lh, lw), np.float32)
    lg = np.zeros_like(m)
    for o in (-0.11, 0.11):
        cv2.line(lg, P(o, 0.05), P(o * 0.8, 0.9), 1.0, max(1, int(0.17 * sc)), cv2.LINE_AA, 4)
    parts.append((lg, col(0.17, 0.17, 0.20)))
    sh = np.zeros_like(m)
    for o in (-0.11, 0.11):
        cv2.ellipse(sh, P(o, 0.05), (max(1, int(0.08 * sc * 16)), max(1, int(0.04 * sc * 16))), 0, 0, 360, 1.0, -1, cv2.LINE_AA, 4)
    parts.append((sh, col(0.10, 0.09, 0.09)))
    to = np.zeros_like(m)
    cv2.ellipse(to, P(0, 1.22), (int(0.24 * sc * 16), int(0.40 * sc * 16)), 0, 0, 360, 1.0, -1, cv2.LINE_AA, 4)
    for o in (-1, 1):
        cv2.line(to, P(o * 0.24, 1.48), P(o * 0.30, 0.95), 1.0, max(1, int(0.11 * sc)), cv2.LINE_AA, 4)
    parts.append((to, col(0.33, 0.26, 0.21)))
    hd = np.zeros_like(m)
    cv2.circle(hd, P(0, 1.74), int(0.12 * sc * 16), 1.0, -1, cv2.LINE_AA, 4)
    cv2.line(hd, P(0, 1.55), P(0, 1.64), 1.0, max(1, int(0.08 * sc)), cv2.LINE_AA, 4)
    parts.append((hd, col(0.14, 0.11, 0.09)))
    full = np.clip(sum(p for p, _ in parts), 0, 1)
    if full.max() <= 0:
        return
    dist = cv2.distanceTransform((full > 0.5).astype(np.uint8), cv2.DIST_L2, 3)
    dn = np.sqrt(np.clip(dist / (0.12 * sc + 1e-6), 0, 1))
    xs = (np.arange(lw, dtype=np.float32) - w2) / (0.3 * sc)
    side = np.clip(1.0 - 0.35 * xs, 0.6, 1.3)[None, :]
    shade = (0.45 + 0.75 * dn) * side
    colr = np.zeros((lh, lw, 3), np.float32)
    acc = np.zeros((lh, lw, 1), np.float32)
    for pm, pc in parts:
        a = pm[..., None] * (1 - acc)
        colr += a * pc
        acc += a
    colr = colr / np.maximum(acc, 1e-6) * shade[..., None]
    if fog is not None:
        f0, f1 = fog
        colr = f0 + colr * (f1 - f0)
    a = full[..., None]
    if green > 0:
        g = col(0.35, 1.0, 0.6)
        colr = lerp(colr, g * (0.5 + 0.6 * dn[..., None]), green)
        a = a * (1 - 0.2 * green)
    X0, Y0 = max(0, x0), max(0, y0)
    X1, Y1 = min(W, x0 + lw), min(H, y0 + lh)
    if X1 <= X0 or Y1 <= Y0:
        return
    sl = (slice(Y0 - y0, Y1 - y0), slice(X0 - x0, X1 - x0))
    roi = img[Y0:Y1, X0:X1]
    roi[:] = roi * (1 - a[sl]) + colr[sl] * a[sl]
    if green > 0:
        gl = fblur(full[..., None] * col(0.35, 1.0, 0.6), 0.12 * sc + 2)
        roi += green * 0.6 * gl[sl]


def _street_person(self, img, p, P, fogc, camz):
    x, z, green = p['x'], p['z'], p.get('green', 0.0)
    sc = 640.0 * S / max(z - camz, 0.3) * 1.0
    fx, fy = P(x, 0, z)
    fog = None
    if fogc is not None:
        fog = (np.array(fogc(col(0, 0, 0), z), np.float32), np.array(fogc(col(1, 1, 1), z), np.float32))
    draw_person(img, fx, fy, sc, green, fog)


Street._person = _street_person


# ---------------------------------------------------------------- 3D scenes
def sc_map_intro(t, T, f):
    p = smooth(t / T)
    pos = (lerp(-20e3, 0, p), lerp(-60e3, -95e3, p), lerp(420e3, 42e3, p ** 0.8))
    tgt = (0, lerp(-20e3, 0, p), 0)
    cam = look_at(pos, tgt, 50)
    img = np.empty((H, W, 3), np.float32)
    haze = col(0.70, 0.75, 0.82)
    terrain_view(img, cam, 'iran', haze, fogd=900e3, tfar=1.2e6, tnear=100.0, steps=36,
                 sky=(col(0.30, 0.40, 0.56), col(0.78, 0.82, 0.88)))
    r = RNG(8)
    cl = []
    for _ in range(55):
        cx_, cy_, cz_ = r.uniform(-260e3, 260e3), r.uniform(-320e3, 260e3), r.uniform(18e3, 24e3)
        if abs(cx_) < 70e3 and -140e3 < cy_ < 30e3:  # keep the camera's flight path clear
            continue
        for j in range(4):
            cl.append((cx_ + r.normal(0, 7e3), cy_ + r.normal(0, 5e3), cz_ + r.normal(0, 800), r.uniform(5e3, 11e3)))
    cl.sort(key=lambda c: -np.linalg.norm(np.array(c[:3]) - cam.pos))
    for i, (x, y, z, R_) in enumerate(cl):
        world_puff(img, cam, (x + t * 900, y, z), R_, col(0.97, 0.97, 0.99), 0.33, i)
    (tx, ty), tz = cam.project(np.array([0, 0, 4000.0]))
    pulse = 0.5 + 0.5 * math.sin(t * 6)
    add_glow(img, tx, ty, max(u(10), cam.f * 3500 / tz) * (1 + 0.5 * pulse), col(1.0, 0.25, 0.15) * 1.3)
    add_glow(img, tx, ty, max(u(3), cam.f * 900 / tz), col(1, 1, 1))
    return finish(img, f, grade=(0.98, 1.0, 1.04))


def sc_city_aerial(t, T, f):
    p = smooth(t / T)
    cam = look_at((lerp(-1100, -350, p), lerp(-3600, -2300, p), lerp(1000, 620, p)), (lerp(250, 0, p), lerp(-200, 300, p), 0), 52)
    img = city_scene(cam, t, f)
    return finish(bloom(img, 0.9, 0.3), f)


def sc_top_fireball(t, T, f):
    p = t / T
    cam = look_at((-520 + 40 * p, -3650 + 120 * p, 720), (0, 0, 260), 50)
    k = smooth(t / (T * 0.8))
    R_ = lerp(30, 380, k)
    ctr = np.array([0, 0, R_ * 0.75])
    light = (ctr, col(1.0, 0.72, 0.42), 2.6 * k + 0.3, 900.0)
    ring = lerp(60, 2300, k)
    img = city_scene(cam, t, f, light=light, damage=(0, 0, ring * 0.85))
    ground_circle(img, cam, ring, col(1.0, 0.88, 0.65), 3, 1.0)
    (cx, cy), cz = cam.project(ctr)
    rad = cam.f * R_ / cz
    gx, gy = cam.project(np.array([0, 0, 0.0]))[0]
    add_glow(img, gx, gy, rad * 3.0, col(0.9, 0.6, 0.35) * 0.7 * k)
    add_glow(img, cx, cy, rad, col(1.6, 1.0, 0.55) * 1.5)
    add_glow(img, cx, cy, rad * 0.45, col(2.0, 2.0, 2.0))
    for i in range(24):
        a = i * 2.4 + t * 1.5
        draw_puff(img, cx + math.cos(a) * rad * 0.7, cy + math.sin(a) * rad * 0.5, rad * 0.38, col(1.4, 0.75, 0.35), 0.35 * k, i)
    img = lerp(img, col(1.0, 0.95, 0.88), 0.12 * k)
    return finish(shake(bloom(img, 0.85, 1.0), 4 * k, f), f)


def sc_top_rings(t, T, f):
    p = t / T
    ang = lerp(-0.25, 0.05, p)
    cam = look_at((14500 * math.sin(ang), -14500 * math.cos(ang), 5600), (0, 600, 0), 50)
    heat = smooth((p - 0.35) / 0.3)
    img = city_scene(cam, t, f, damage=(0, 0, 3500), fogd=40000.0, maxd=1.0)
    a = np.linspace(0, 2 * math.pi, 200)
    for rad, c, alpha in ((7000, col(0.9, 0.25, 0.15), 0.30), (3500, col(1.0, 0.3, 0.2), 0.42), (2000, col(1.0, 0.35, 0.25), 0.3)):
        pp, _ = cam.project(np.stack([rad * np.cos(a), rad * np.sin(a), np.zeros_like(a)], 1))
        m = np.zeros((H, W), np.float32)
        cv2.fillPoly(m, [(pp * 16).astype(np.int32)], 1.0, cv2.LINE_AA, 4)
        img = lerp(img, c, fblur(m, u(25))[..., None] * alpha * heat)
    ground_circle(img, cam, lerp(400, 9000, smooth(p / 0.35)), col(1.0, 0.95, 0.85), 3, 0.8)
    for i, rr in enumerate((2000, 3500, 7000, 9000)):
        ground_circle(img, cam, rr, col(0.9, 0.88, 0.82) * smooth((p - 0.3 - i * 0.08) / 0.1) * 0.6, 2, 0.3)
    r = RNG(4)
    for i in range(70):  # low dust over the destroyed core
        aa, rr = r.uniform(0, 6.28), 3200 * math.sqrt(r.random())
        world_puff(img, cam, (rr * math.cos(aa), rr * math.sin(aa), r.uniform(50, 400)), r.uniform(250, 600),
                   col(0.62, 0.56, 0.50), 0.35, i)
    world_mushroom(img, cam, (0, 0, 0), lerp(9000, 13000, p), 0.6 + 0.3 * p, seed=5)
    return finish(img, f)


def sc_cloud_tall(t, T, f):
    p = t / T
    cam = look_at((lerp(-2000, 2000, p), -52e3, 1400), (4e3, 0, 5200), 52)
    img = np.empty((H, W, 3), np.float32)
    terrain_view(img, cam, 'plain', col(0.80, 0.78, 0.75), fogd=140e3, tfar=260e3, tnear=20.0, steps=40,
                 sky=(col(0.50, 0.58, 0.68), col(0.84, 0.82, 0.79)))
    world_mushroom(img, cam, (-6000, 0, 0), lerp(8000, 17000, smooth(0.35 + 0.65 * p)), 0.45 + 0.55 * p, seed=7,
                   fire=max(0, 0.35 - p) * 1.5)
    return finish(img, f)


def sc_history(t, T, f):
    p = t / T
    cam = look_at((lerp(-800, 800, p), -36e3, 1200), (0, 0, 5600), 50)
    img = np.empty((H, W, 3), np.float32)
    terrain_view(img, cam, 'plain', col(0.82, 0.78, 0.72), fogd=120e3, tfar=220e3, tnear=20.0, steps=36,
                 sky=(col(0.52, 0.56, 0.62), col(0.86, 0.82, 0.76)))
    world_mushroom(img, cam, (0, 0, 0), 12500, 0.75 + 0.25 * p, seed=9)
    sep = 1 - smooth((t - T * 0.35) / (T * 0.3))
    lum = img.mean(axis=2, keepdims=True)
    img = lerp(img, lum * col(1.05, 0.92, 0.75), sep)
    r = RNG(f)
    if sep > 0.05 and r.random() < 0.5:
        for _ in range(1):
            x = int(r.uniform(0, W))
            cv2.line(img, (x, 0), (x, H), (0.9 * sep, 0.85 * sep, 0.75 * sep), max(1, int(S)))
    return finish(img, f, grain=0.025 + 0.04 * sep)


def sc_map_plume(t, T, f):
    p = smooth(t / T)
    cam = look_at((-90e3, -330e3, 210e3), (80e3, -20e3, 0), 50)
    img = np.empty((H, W, 3), np.float32)
    terrain_view(img, cam, 'iran', col(0.70, 0.75, 0.82), fogd=900e3, tfar=1.2e6, tnear=100.0, steps=36,
                 sky=(col(0.30, 0.40, 0.56), col(0.78, 0.82, 0.88)))
    L = lerp(10e3, 380e3, p)
    wd = np.array([0.95, -0.31])
    nrm_ = np.array([0.31, 0.95])
    r = RNG(12)
    pts = []
    for i in range(240):
        s = r.random() ** 0.8
        d = s * L
        lat = r.normal(0, 6e3 + 0.22 * d)
        x, y = wd * d + nrm_ * lat
        pts.append((x, y, r.uniform(1.5e3, 6e3) + 4e3 * s, 5e3 + 0.08 * d * r.uniform(0.6, 1.4), 0.55 - 0.3 * s))
    pts.sort(key=lambda q: -np.linalg.norm(np.array(q[:3]) - cam.pos))
    for i, (x, y, z, R_, al) in enumerate(pts):
        world_puff(img, cam, (x, y, z), R_, col(0.52, 0.47, 0.42), al, i)
    (tx, ty), tz = cam.project(np.array([0, 0, 1000.0]))
    add_glow(img, tx, ty, max(u(9), cam.f * 3000 / tz), col(1.0, 0.3, 0.2))
    world_mushroom(img, cam, (0, 0, 0), 15000, 1.0, seed=2)
    return finish(img, f)


# ruins: ray-marched rubble field + 3D broken buildings + 3D-placed trees/person
@lru_cache(maxsize=None)
def ruin_blocks():
    r = RNG(21)
    B = {k: [] for k in ('x0', 'y0', 'x1', 'y1', 'h', 'c')}
    for i in range(34):
        x, y = r.uniform(-90, 90), r.uniform(35, 140)
        if abs(x) < 8:
            continue
        w, d = r.uniform(8, 22), r.uniform(8, 18)
        hh = r.uniform(3, 16)
        for j in range(int(r.integers(2, 5))):  # jagged: several partial boxes
            fx0, fx1 = sorted(r.uniform(0, 1, 2))
            B['x0'].append(x + w * fx0 * 0.6)
            B['x1'].append(x + w * (0.4 + fx1 * 0.6))
            B['y0'].append(y)
            B['y1'].append(y + d * r.uniform(0.4, 1.0))
            B['h'].append(hh * r.uniform(0.3, 1.0))
            g = r.uniform(0.38, 0.55)
            B['c'].append(col(g, g * 0.97, g * 0.93))
    B = {k: np.array(v, np.float64) for k, v in B.items()}
    B['cx'] = (B['x0'] + B['x1']) / 2
    B['cy'] = (B['y0'] + B['y1']) / 2
    B['rad'] = np.hypot(B['x1'] - B['x0'], B['y1'] - B['y0']) / 2 + B['h'] / 2
    B['dmg'] = np.ones_like(B['h'])
    return B


def ruins(t, f, green=0.0, dust=0.0, person=True, warm=False):
    cam = Cam((0.0, -20 + t * 0.5, 1.7), 0.04 * math.sin(t * 0.2), math.radians(4), 55, cy=0.45)
    img = np.empty((H, W, 3), np.float32)
    haze = col(0.60, 0.58, 0.55)
    terrain_view(img, cam, 'rubble', haze, fogd=420.0, tfar=220.0, tnear=0.3, steps=40,
                 sky=(col(0.40, 0.39, 0.38), col(0.66, 0.62, 0.58)))
    Bw = ruin_blocks()
    d = np.hypot(Bw['cx'] - cam.pos[0], Bw['cy'] - cam.pos[1])
    order = np.argsort(-d)
    order = order[(Bw['cy'][order] > cam.pos[1] + 5)]
    draw_boxes(img, cam, Bw, haze, 420.0, idx=order, detail_d=300)
    for i, (x, y, h) in enumerate(((-9, 14, 7), (11, 22, 9), (5, 9, 4), (-6, 30, 6), (14, 40, 8))):
        (bx, by), z = cam.project(np.array([x, y, 0.0]))
        if z > 1:
            dead_tree(img, bx / S, by / S, cam.f * h / z / S, 40 + i)
    if person:
        (fx, fy), z = cam.project(np.array([0.3, cam.pos[1] + 4.6, 0.25]))
        draw_person(img, fx, fy, cam.f / z, green)
    if dust > 0:
        rr = RNG(3)
        for i in range(320):
            x = rr.uniform(0, W)
            y = (rr.uniform(0, H) + t * u(rr.uniform(30, 90))) % H
            cv2.circle(img, (int(x), int(y)), int(u(rr.uniform(1, 3.2))), (0.85, 0.83, 0.78), -1, cv2.LINE_AA)
        img = lerp(img, col(0.62, 0.60, 0.56), dust * 0.22)
    return img


def sc_ruins_rad(t, T, f):
    return finish(ruins(t, f, green=smooth((t - 1.0) / 1.5)), f, grade=(0.98, 1.02, 0.98))


def sc_ruins_dust(t, T, f):
    return finish(ruins(t, f, person=False, dust=smooth(t / 2)), f, grade=(1.0, 1.0, 0.97))


# skin: 3D tissue block with textured layer faces
@lru_cache(maxsize=None)
def skin_textures():
    tw, th = (1600, 930) if DETAIL else (800, 465)
    k = tw / 800
    v = np.arange(th, dtype=np.float32)[:, None] / th * 1.4  # depth below surface
    n = cv2.resize(fbm(64, 128, 8, 5, 4), (tw, th))[..., None]
    lay = [(0.0, 0.08, col(0.85, 0.62, 0.52)), (0.08, 0.35, col(0.78, 0.36, 0.32)),
           (0.35, 0.75, col(0.95, 0.82, 0.45)), (0.75, 9, col(0.62, 0.16, 0.14))]
    front = np.zeros((th, tw, 3), np.float32)
    for a, b, c in lay:
        m = ((v >= a) & (v < b))[..., None]
        front = np.where(m, c * (0.8 + 0.4 * n), front)
    r = RNG(4)
    u8 = front
    for _ in range(int(160 * k)):  # fat lobules
        x, y = r.uniform(0, tw), r.uniform(0.38, 0.72) * th / 1.4
        cv2.circle(u8, (int(x), int(y)), int(r.uniform(6, 16) * k), (0.85, 0.70, 0.36), max(1, int(k)), cv2.LINE_AA)
    for _ in range(int(60 * k)):  # muscle striations
        y = r.uniform(0.78, 1.38) * th / 1.4
        cv2.line(u8, (0, int(y)), (tw, int(y + r.uniform(-20, 20))), (0.45, 0.10, 0.10), max(1, int(k)), cv2.LINE_AA)
    glow = np.zeros_like(front)
    for i in range(18):  # nerves rising to the surface
        x = (i + 0.5) * tw / 18 + r.uniform(-10, 10) * k
        y = 0.7 * th / 1.4
        pts = [(x, y)]
        while y > 0.06 * th / 1.4:
            y -= 6 * k
            x += r.normal(0, 2.5) * k
            pts.append((x, y))
        cv2.polylines(glow, [np.array(pts, np.int32)], False, (1.6, 1.1, 0.6), max(2, int(2 * k)), cv2.LINE_AA)
        tx, ty = pts[-1]
        cv2.ellipse(glow, (int(tx), int(ty) + int(5 * k)), (int(12 * k), int(5 * k)), 0, 180, 360, (1.5, 0.9, 0.4), max(2, int(2 * k)), cv2.LINE_AA)
    for i in range(10):  # vessels
        pts = [(r.uniform(0, tw), r.uniform(0.12, 0.3) * th / 1.4)]
        for j in range(30):
            px, py = pts[-1]
            pts.append((px + 8 * k, py + r.normal(0, 3) * k))
        cv2.polylines(front, [np.array(pts, np.int32)], False, (0.55, 0.05, 0.08), max(2, int(2.5 * k)), cv2.LINE_AA)
    glow = glow + fblur(glow, 8 * k) * 1.4
    ts = 1024 if DETAIL else 512
    tn = fbm(ts, ts, 13, 7, 6)[..., None]
    skin = col(0.86, 0.64, 0.54) * (0.9 + 0.2 * tn)
    char = lerp(col(0.06, 0.04, 0.03), col(0.22, 0.12, 0.08), tn)
    cracks = np.zeros((ts, ts), np.float32)
    for _ in range(40):
        p0 = r.uniform(0, ts, 2)
        a = r.uniform(0, 6.28)
        for _ in range(30):
            a += r.normal(0, 0.5)
            p1 = p0 + 10 * (ts / 512) * np.array([math.cos(a), math.sin(a)])
            cv2.line(cracks, tuple(p0.astype(int)), tuple(p1.astype(int)), 1.0, max(1, int(ts / 512)), cv2.LINE_AA)
            p0 = p1
    cracks = (cracks + fblur(cracks, 3 * ts / 512) * 1.5)[..., None]
    return front.astype(np.float32), glow.astype(np.float32), skin.astype(np.float32), char.astype(np.float32), cracks.astype(np.float32)


def sc_skin_burn(t, T, f):
    p = t / T
    k = smooth(p * 1.4)
    a = lerp(-0.45, 0.30, p)
    cam = look_at((3.3 * math.sin(a), -3.3 * math.cos(a), 1.45), (0, 0, -0.55), 42, cy=0.5)
    img = np.empty((H, W, 3), np.float32)
    img[:] = lerp(col(0.10, 0.07, 0.06), col(0.03, 0.02, 0.02), np.clip(_yy / H, 0, 1)[..., None])
    front, glow, skin, char, cracks = skin_textures()
    xa, xb, ya, yb, za, zb = -1.2, 1.2, -0.8, 0.8, -1.4, 0.0
    flick = 0.9 + 0.1 * math.sin(t * 7)
    ftex = front + glow * k * flick
    top = lerp(skin, char, k) + cracks * col(1.5, 0.6, 0.18) * k * flick
    faces = [  # corners TL,TR,BR,BL in texture orientation, normal
        ([(xa, ya, zb), (xb, ya, zb), (xb, ya, za), (xa, ya, za)], (0, -1, 0), ftex),
        ([(xb, ya, zb), (xb, yb, zb), (xb, yb, za), (xb, ya, za)], (1, 0, 0), ftex),
        ([(xa, yb, zb), (xa, ya, zb), (xa, ya, za), (xa, yb, za)], (-1, 0, 0), ftex),
        ([(xa, yb, zb), (xb, yb, zb), (xb, ya, zb), (xa, ya, zb)], (0, 0, 1), top),
    ]
    for corners, nrm, tex in faces:
        ctr = np.mean(corners, 0)
        if np.dot(np.array(nrm, float), cam.pos - ctr) <= 0:
            continue
        pp, zz = cam.project(np.array(corners, float))
        shade = 0.55 + 0.6 * max(0.0, float(np.dot(nrm, np.array([-0.3, -0.5, 0.8]) / 1.0)))
        draw_textured_quad(img, pp, tex, shade)
    r = RNG(4)
    for i in range(140):  # embers rising from the surface in 3D
        x, y = r.uniform(xa, xb), r.uniform(ya, yb)
        z = (r.uniform(0, 1.2) + t * r.uniform(0.1, 0.3)) % 1.2
        (sx, sy), zz = cam.project(np.array([x, y, z]))
        if zz > 0.1:
            cv2.circle(img, (int(sx), int(sy)), max(1, int(cam.f * 0.008 / zz)), (1.4 * k, 0.6 * k, 0.2 * k), -1, cv2.LINE_AA)
    (hx, hy), hz_ = cam.project(np.array([0, 0, 0.05]))
    add_glow(img, hx, hy, cam.f * 1.0 / hz_, col(0.8, 0.3, 0.08) * 0.35 * k)
    return finish(bloom(img, 0.8, 0.8), f)


@lru_cache(maxsize=None)
def cell_noise(seed):
    return fbm(24, 24, seed, 3, 3)


def sc_cells(t, T, f):
    img = np.empty((H, W, 3), np.float32)
    img[:] = lerp(col(0.22, 0.03, 0.04), col(0.08, 0.01, 0.02), np.clip(_yy / H, 0, 1)[..., None])
    cam = Cam((0.0, t * 1.1, 0.0), 0.0, 0.0, 55)
    r = RNG(6)
    cells = [(r.uniform(-7, 7), r.uniform(1, 34), r.uniform(-11, 11), r.uniform(0.8, 1.5), i) for i in range(150)]
    cz = cam.pos[1]
    cells = [c for c in cells if c[1] - cz > 2.6 and not (abs(c[0]) < 2.2 and abs(c[2]) < 2.2 and c[1] - cz < 9)]
    cells.sort(key=lambda c: -(c[1] - cz))
    L = np.array([-0.45, -0.55, -0.70])
    L /= np.linalg.norm(L)
    Hh = L + np.array([0, 0, -1.0])
    Hh /= np.linalg.norm(Hh)
    focus = 6.0

    def sphere(cx_, cy_, rad, depth, base, bump=0.0, seed=0):
        blur = min(u(28), u(abs(depth - focus) * 2.0))
        mg = int(rad * (1.2 if bump else 1.0) + 3 * blur + 3)
        x0, y0, x1, y1 = max(0, int(cx_) - mg), max(0, int(cy_) - mg), min(W, int(cx_) + mg), min(H, int(cy_) + mg)
        if x1 <= x0 or y1 <= y0 or rad < 1:
            return
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        dx_, dy_ = (xx - cx_) / rad, (yy - cy_) / rad
        rr = np.sqrt(dx_ ** 2 + dy_ ** 2)
        if bump:
            ang = np.arctan2(dy_, dx_)
            rlim = 1 + bump * (0.08 * np.sin(5 * ang + t * 2) + 0.05 * np.sin(9 * ang - t * 3))
        else:
            rlim = 1.0
        q = np.clip(rr / rlim, 0, 1)
        nz = np.sqrt(np.clip(1 - q ** 2, 0, 1))
        nx, ny = dx_ / np.maximum(rlim, 1e-3), dy_ / np.maximum(rlim, 1e-3)
        dif = np.clip(nx * L[0] + ny * L[1] - nz * L[2], 0, 1)
        spec = np.clip(nx * Hh[0] + ny * Hh[1] - nz * Hh[2], 0, 1) ** 40
        rim = (1 - nz) ** 2.5
        tex = 1.0
        if DETAIL:
            tex = 0.9 + 0.2 * cv2.resize(cell_noise(seed % 16), (x1 - x0, y1 - y0))
        c = base * (0.22 + 0.95 * dif * tex)[..., None] + rim[..., None] * col(0.9, 0.25, 0.25) * 0.45 + spec[..., None] * 0.55
        a = np.clip((rlim - rr) * rad, 0, 1)
        if blur > 0.5:
            c = fblur(c, blur)
            a = fblur(a, blur)
        a = a[..., None]
        roi = img[y0:y1, x0:x1]
        roi[:] = roi * (1 - a) + c * a

    for (x, y, z, rad, i) in cells:
        (sx, sy), zz = cam.project(np.array([x, y, z]))
        if zz <= 0.5:
            continue
        sphere(sx, sy, cam.f * rad / zz, zz, col(0.78, 0.10, 0.12) * (0.75 + 0.25 * math.exp(-zz / 20)), seed=i)
    k = smooth((t - 1.0) / 2.0)
    (sx, sy), zz = cam.project(np.array([0.0, cz + 5.0, 0.0]))
    sphere(sx, sy, cam.f * 1.5 / zz, focus, lerp(col(0.85, 0.15, 0.15), col(0.22, 0.04, 0.10), k), bump=k, seed=99)
    add_glow(img, sx, sy, u(30), col(0.9, 0.2, 0.3) * (0.4 + 0.4 * math.sin(t * 4)) * k)
    return finish(bloom(img, 0.7, 0.4), f, grade=(1.0, 1.0, 1.0))


def sc_ending(t, T, f):
    img = sc_history(T * 0.9 + t * 0.2, T, f)
    r = RNG(1)
    for i in range(80):
        x = r.uniform(0, W) + u(math.sin(t + i) * 10)
        y = H - ((r.uniform(0, H) + t * u(r.uniform(30, 80))) % H)
        cv2.circle(img, (int(x), int(y)), int(u(2)), (1.0, 0.6, 0.25), -1, cv2.LINE_AA)
    return np.clip(img * (1 - smooth(t / T) * 0.95), 0, 1)


SCENES = {k[3:]: v for k, v in globals().items() if k.startswith('sc_')}


def render_scene(sid, scene, dur, out, fade_in=0.35):
    n = int(round(dur * FPS))
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
           '-i', '-', '-c:v', 'libx264', '-preset', os.environ.get('PRESET', 'medium'), '-crf', os.environ.get('CRF', '18'),
           '-pix_fmt', 'yuv420p', '-threads', '2'] + (['-level', '5.2'] if S >= 2 else []) + [out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    fn = SCENES[scene]
    for i in range(n):
        t = i / FPS
        img = fn(t, dur, i + sum(map(ord, sid)))
        if t < fade_in and scene not in ('street_vapor',):
            img = img * (0.4 + 0.6 * smooth(t / fade_in))
        p.stdin.write((np.clip(img, 0, 1) * 255).astype(np.uint8).tobytes())
    p.stdin.close()
    p.wait()
    print('done', sid, n, flush=True)


if __name__ == '__main__':
    timings = json.load(open(sys.argv[1]))
    outdir = sys.argv[2]
    only = set(sys.argv[3:])
    for s in timings:
        if only and s['id'] not in only:
            continue
        dur = s['dur']
        if os.environ.get('MAXDUR'):
            dur = min(dur, float(os.environ['MAXDUR']))
        render_scene(s['id'], s['scene'], dur, f"{outdir}/{s['id']}.mp4")
