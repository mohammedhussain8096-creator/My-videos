"""Procedural 3D-style renderer for the Hindi Tehran explainer.

Every scene is drawn from scratch (noise terrain, perspective city street,
particle mushroom cloud, etc). No text, captions, counters or watermarks are
ever drawn on screen.

Usage: python render.py <timings.json> <out_dir> [scene_id ...]
"""
import json
import math
import subprocess
import sys
from functools import lru_cache

import cv2
import numpy as np

W, H, FPS = 720, 1280, 30
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


def radial(cx, cy, r):
    return np.exp(-(((_xx - cx) ** 2 + (_yy - cy) ** 2) / (2 * r * r)))[..., None]


def bloom(img, thresh=0.75, strength=0.8, k=61):
    bright = np.clip(img - thresh, 0, None)
    small = cv2.resize(bright, (W // 4, H // 4))
    small = cv2.GaussianBlur(small, (0, 0), k / 8)
    return img + strength * cv2.resize(small, (W, H))


def finish(img, f, grade=(1.03, 1.0, 0.94), grain=0.025, vig=True):
    img = img * np.array(grade, np.float32)
    lum = img.mean(axis=2, keepdims=True)
    img = lerp(lum, img, 0.82)  # slight desaturation, cinematic
    if vig:
        img = img * VIGNETTE
    if grain:
        g = RNG(f * 7 + 1).standard_normal((H // 2, W // 2)).astype(np.float32)
        img = img + grain * cv2.resize(g, (W, H))[..., None]
    img = img / (1 + np.clip(img - 1, 0, None) * 0.6)  # soft highlight roll-off
    return np.clip(img, 0, 1)


def shake(img, amt, f):
    if amt <= 0:
        return img
    r = RNG(f)
    dx, dy = r.uniform(-amt, amt, 2)
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
    r = int(max(2, min(r, 420)))
    q = int(r ** 0.5 * 3)  # quantise radius for caching
    r = max(2, int((q / 3) ** 2))
    a, sh = puff_sprite(r, seed % 3)
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
    for i in range(70):
        t = r.random()
        y = lerp(gy, top + capw * 0.2, t)
        w = s * (0.12 + 0.05 * t) * (0.6 + 0.4 * ph)
        puffs.append((gx + r.normal(0, w * 0.5), y, w * r.uniform(0.6, 1.1), t * 0.6))
    # base skirt / ground dust ring
    for i in range(40):
        a = r.uniform(0, 2 * math.pi)
        rr = s * (0.4 + 1.1 * ph) * r.uniform(0.6, 1.1)
        puffs.append((gx + math.cos(a) * rr, gy + math.sin(a) * rr * 0.18, s * 0.22 * r.uniform(0.6, 1.2), 0.0))
    # cap: torus + dome
    for i in range(150):
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
    if fire > 0:
        img += fire * 0.9 * radial(gx, top + capw * 0.1, capw * 0.8) * col(1.0, 0.45, 0.15)


# ---------------------------------------------------------------- textures
@lru_cache(maxsize=None)
def terrain_tex(size=2048, seed=11, sea=False):
    h = fbm(size, size, seed, octaves=8, base=3)
    detail = fbm(size, size, seed + 1, octaves=4, base=16)
    hgt = 0.85 * h + 0.15 * detail
    hs = cv2.GaussianBlur(hgt, (0, 0), 2)
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
def city_tex(size=2048, seed=5):
    base = terrain_tex(size, seed) * 0.3 + col(0.70, 0.66, 0.60) * 0.7
    img = (np.clip(base, 0, 1) * 255).astype(np.uint8)
    shadow = np.zeros((size, size), np.uint8)
    r = RNG(seed)
    cx = cy = size // 2
    road = (104, 102, 98)
    blk = 64
    for bx in range(0, size, blk):
        for by in range(0, size, blk):
            x0, y0 = bx + 5, by + 5
            dist = math.hypot(bx - cx, by - cy) / size
            if r.random() < 0.05:
                cv2.rectangle(img, (x0, y0), (x0 + blk - 10, y0 + blk - 10), (88, 112, 74), -1)
                for _ in range(8):
                    tx, ty = r.integers(x0 + 3, x0 + blk - 13, 2)
                    cv2.circle(img, (int(tx), int(ty)), 4, (60, 86, 52), -1, cv2.LINE_AA)
                continue
            # subdivide block into 2-4 buildings per side
            nx, ny = int(r.integers(2, 4)), int(r.integers(2, 4))
            ws, hs = (blk - 10) / nx, (blk - 10) / ny
            for i in range(nx):
                for j in range(ny):
                    a = (int(x0 + i * ws + 1), int(y0 + j * hs + 1))
                    b = (int(x0 + (i + 1) * ws - 2), int(y0 + (j + 1) * hs - 2))
                    ht = int(r.integers(2, 9) * (1.5 - dist * 1.5))
                    cv2.rectangle(shadow, (a[0] + ht, a[1] + ht), (b[0] + ht, b[1] + ht), 255, -1)
                    tone = int(r.integers(178, 236))
                    roof = (tone, tone - int(r.integers(2, 14)), tone - int(r.integers(10, 32)))
                    cv2.rectangle(img, a, b, roof, -1)
                    cv2.rectangle(img, a, b, (tone - 40, tone - 45, tone - 55), 1)
    # boulevards and ring roads drawn over
    for a in np.linspace(0, math.pi, 4, endpoint=False):
        dx, dy = int(math.cos(a) * size), int(math.sin(a) * size)
        cv2.line(img, (cx - dx, cy - dy), (cx + dx, cy + dy), road, 12, cv2.LINE_AA)
    for rr in (320, 700):
        cv2.circle(img, (cx, cy), rr, road, 12, cv2.LINE_AA)
    out = img.astype(np.float32) / 255
    sh = cv2.GaussianBlur(shadow, (0, 0), 1.5).astype(np.float32)[..., None] / 255
    road_mask = (np.abs(out - np.array(road, np.float32) / 255).sum(2, keepdims=True) < 0.02)
    out = out * (1 - 0.4 * sh * ~road_mask)
    return out


@lru_cache(maxsize=None)
def rubble_tex(size=1024, seed=9):
    n = fbm(size, size, seed, octaves=7, base=8)
    img = lerp(col(0.28, 0.27, 0.26), col(0.62, 0.60, 0.57), n[..., None])
    u8 = (img * 255).astype(np.uint8)
    r = RNG(seed)
    for _ in range(1600):
        x, y = r.integers(0, size, 2)
        pts = (np.array([[x, y]]) + r.integers(-14, 14, (5, 2))).astype(np.int32)
        t = int(r.integers(40, 150))
        cv2.fillConvexPoly(u8, cv2.convexHull(pts), (t, t, t - 5), cv2.LINE_AA)
    for _ in range(25):  # cracks
        p = r.integers(0, size, 2).astype(float)
        a = r.uniform(0, 6.28)
        for _ in range(40):
            a += r.normal(0, 0.4)
            q = p + 14 * np.array([math.cos(a), math.sin(a)])
            cv2.line(u8, tuple(p.astype(int)), tuple(q.astype(int)), (20, 20, 20), 2, cv2.LINE_AA)
            p = q
    return u8.astype(np.float32) / 255


# ---------------------------------------------------------------- tilted ground view
SKY_TOP, SKY_HZ = col(0.55, 0.60, 0.66), col(0.86, 0.84, 0.80)


def tilt_view(tex, cx, cy, span, hz=0.30, depth=2.2, haze=col(0.82, 0.78, 0.72), rot=0.0, mountains=True):
    """Map a top-down texture onto a tilted ground plane. Returns (img, M)."""
    S = tex.shape[0]
    hzy = H * hz
    near_w, far_w = span, span * depth
    c, s = math.cos(rot), math.sin(rot)

    def tp(dx, dy):
        return [cx + dx * c - dy * s, cy + dx * s + dy * c]

    src = np.float32([tp(-far_w / 2, -span * 1.2), tp(far_w / 2, -span * 1.2),
                      tp(near_w / 2, span * 0.5), tp(-near_w / 2, span * 0.5)])
    dst = np.float32([[-W * 0.1, hzy], [W * 1.1, hzy], [W * 1.0, H], [0, H]])
    M = cv2.getPerspectiveTransform(src, dst)
    img = cv2.warpPerspective(tex, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    t = np.clip((_yy - hzy) / (H - hzy), 0, 1)[..., None]
    sky = lerp(SKY_TOP, SKY_HZ, np.clip(_yy / hzy, 0, 1)[..., None])
    img = np.where(_yy[..., None] < hzy, sky, lerp(haze, img, smooth(t * 1.6) ** 0.8))
    if mountains:
        my = hzy - 10 - ridge(77, 60)
        mask = (_yy > my[None, :]) & (_yy < hzy + 2)
        mcol = lerp(col(0.60, 0.58, 0.56), haze, 0.35)
        img = np.where(mask[..., None], mcol, img)
        img = lerp(img, haze, (radial(W / 2, hzy, 160) * 0.0 + np.exp(-((_yy - hzy) / 40) ** 2)[..., None]) * 0.6)
    return img.astype(np.float32), M


def project(M, pts):
    p = cv2.perspectiveTransform(np.float32(pts).reshape(-1, 1, 2), M)
    return p.reshape(-1, 2)


def ground_ring(img, M, cx, cy, rad, color, thick=3, glow=0.6):
    a = np.linspace(0, 2 * math.pi, 180)
    pts = project(M, np.stack([cx + rad * np.cos(a), cy + rad * np.sin(a)], 1))
    layer = np.zeros_like(img)
    cv2.polylines(layer, [pts.astype(np.int32)], True, tuple(float(v) for v in color), thick, cv2.LINE_AA)
    img += layer + glow * cv2.GaussianBlur(layer, (0, 0), 9)


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

    def render(self, camz, camx=0.0, camh=1.7, f=640.0, hz=0.43, collapse=None, dust_z=None,
               dust_col=col(0.62, 0.52, 0.44), fog=col(0.84, 0.82, 0.78), fogd=260.0, sky=None, people=()):
        hzy = H * hz
        img = np.empty((H, W, 3), np.float32)
        top, bot = (sky or (col(0.62, 0.68, 0.74), col(0.88, 0.86, 0.82)))
        img[:] = lerp(top, bot, np.clip(_yy / hzy, 0, 1)[..., None])
        # distant mountains
        my = hzy - 4 - ridge(31, 45)
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

        items = []
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
                    poly([P(xa, ya, za), P(xa, ya, zb), P(xa, yb, zb), P(xa, yb, za)], c * 0.42 + col(0.02, 0.04, 0.07), (za + zb) / 2)

    def _person(self, img, p, P, fogc, camz):
        x, z, green = p['x'], p['z'], p.get('green', 0.0)
        sc = 640.0 / max(z - camz, 0.3)
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
            m = cv2.GaussianBlur(m, (0, 0), 1.2)[..., None] if m.ndim == 2 else cv2.GaussianBlur(m, (0, 0), 1.2).reshape(H, W, 1)
            g = col(0.35, 1.0, 0.6)
            mixed = lerp(layer, g * 0.8, green)
            img[:] = img * (1 - m * (1 - 0.25 * green)) + mixed * m
            img += green * 0.5 * cv2.GaussianBlur(m * g, (0, 0), 14)


# ---------------------------------------------------------------- dead tree
def dead_tree(img, x, y, h, seed, color=(0.12, 0.11, 0.10)):
    r = RNG(seed)

    def br(x, y, a, l, w, d):
        if d == 0 or l < 3:
            return
        x2, y2 = x + l * math.cos(a), y - l * math.sin(a)
        cv2.line(img, (int(x), int(y)), (int(x2), int(y2)), color, max(1, int(w)), cv2.LINE_AA)
        for _ in range(2):
            br(x2, y2, a + r.normal(0, 0.55), l * r.uniform(0.6, 0.8), w * 0.65, d - 1)
    br(x, y, math.pi / 2 + r.normal(0, 0.1), h * 0.4, h * 0.05, 7)


# ---------------------------------------------------------------- scenes
def sc_map_intro(t, T, f):
    tex = terrain_tex(2048, 21, True)
    p = smooth(t / T)
    span = lerp(1000, 300, p)
    img, M = tilt_view(tex, 1100, 950, span, hz=lerp(0.04, 0.2, p), depth=1.35, mountains=False,
                       haze=col(0.70, 0.74, 0.80), rot=lerp(-0.12, 0.04, p))
    # drifting clouds
    cl = fbm(H // 4, W // 4, 3, octaves=5, base=3)
    cl = np.roll(cl, int(t * 12), axis=1)
    cl = cv2.resize(cl, (W, H))[..., None]
    img = lerp(img, col(0.95, 0.95, 0.97), smooth((cl - 0.55) * 3) * 0.55 * (1 - p * 0.6))
    (tx, ty), = project(M, [(1100, 950)])
    pulse = 0.5 + 0.5 * math.sin(t * 6)
    img += radial(tx, ty, 10 + 8 * pulse) * col(1.0, 0.25, 0.15) * 1.2
    img += radial(tx, ty, 3) * 1.0
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
    sx, sy = W / 2, H * 0.43 - 30
    k = smooth((t - 0.6) / 1.2)
    img += radial(sx, sy, lerp(8, 110, k)) * col(1.0, 0.95, 0.85) * (0.5 + 2.5 * k)
    img += radial(sx, sy, lerp(4, 30, k)) * 3.0 * k
    white = smooth((t - (T - 2.2)) / 1.6)
    img = lerp(img, col(1.0, 0.98, 0.95), white * 0.92)
    return finish(bloom(img, 0.8, 1.2), f)


def sc_top_fireball(t, T, f):
    tex = city_tex()
    img, M = tilt_view(tex, 1024, 1024, 560, hz=0.24, depth=2.1)
    (cx, cy), = project(M, [(1024, 980)])
    k = smooth(t / (T * 0.8))
    rad = lerp(10, 140, k)
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
    img += radial(W / 2, hzy - 120, lerp(60, 520, k)) * col(1.0, 0.9, 0.75) * (1 + 3 * k)
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
    for i in range(220):
        x = r.uniform(-40, 40)
        y = r.uniform(0, 1) ** 1.6 * 55
        zz = dust_z + r.uniform(0, 25)
        sx, sy = P(x, y, zz)
        rr = 640 * r.uniform(3, 7) / max(zz - camz, 0.3)
        draw_puff(img, sx + math.sin(t * 2 + i) * 6, sy, rr, col(0.66, 0.54, 0.44) * r.uniform(0.8, 1.1), 0.85, i)
    return finish(shake(img, 3 + 10 * smooth(k), f), f)


def ruins(t, f, green=0.0, dust=0.0, person=True, warm=False):
    tex = rubble_tex()
    img, M = tilt_view(tex, 512, 512 + t * 6, 300, hz=0.33, depth=2.6, haze=col(0.58, 0.56, 0.54), mountains=False)
    hzy = H * 0.33
    img = np.where(_yy[..., None] < hzy, lerp(col(0.42, 0.40, 0.39), col(0.66, 0.62, 0.58), (_yy / hzy)[..., None]), img)
    u8 = img  # draw ruins silhouettes
    r = RNG(12)
    for i in range(10):  # broken building stubs on horizon
        x = r.uniform(0, W)
        w, h = r.uniform(30, 90), r.uniform(30, 120)
        pts = np.array([[x, hzy + 5], [x + w, hzy + 5], [x + w, hzy - h * r.uniform(0.3, 1)], [x + w * 0.6, hzy - h],
                        [x + w * 0.3, hzy - h * 0.5], [x, hzy - h * 0.8]], np.int32)
        cv2.fillPoly(u8, [pts], (0.40, 0.38, 0.37), cv2.LINE_AA)
    for i, (x, h) in enumerate(((90, 300), (600, 380), (420, 160), (230, 120))):
        dead_tree(img, x + math.sin(t * 0.4) * 6, H * 0.62 + h * 0.4, h, 40 + i)
    if person:
        st = Street(1)
        st._person(img, dict(x=0.0, z=4.2, green=green), lambda x, y, z: (W / 2 + 640 * x / z, H * 0.43 - 640 * (y - 1.7) / z),
                   None, 0.0)
    if dust > 0:
        rr = RNG(3)
        for i in range(260):
            x = rr.uniform(0, W)
            y = (rr.uniform(0, H) + t * rr.uniform(30, 90)) % H
            cv2.circle(img, (int(x), int(y)), int(rr.uniform(1, 3)), (0.85, 0.83, 0.78), -1, cv2.LINE_AA)
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
        img += radial(sx, sy, 640 * 5 / z) * col(1.2, 0.5, 0.15) * fl
    for i in range(60):  # smoke drifting sideways
        x = (r.uniform(-200, W + 200) + t * r.uniform(120, 260)) % (W + 400) - 200
        y = r.uniform(H * 0.1, H * 0.5)
        draw_puff(img, x, y, r.uniform(60, 140), col(0.42, 0.36, 0.33), 0.35, i)
    for i in range(160):  # flying debris streaks
        x = (r.uniform(0, W) + t * r.uniform(500, 900)) % W
        y = r.uniform(H * 0.3, H)
        cv2.line(img, (int(x), int(y)), (int(x - 25), int(y + 3)), (0.75, 0.68, 0.6), 1, cv2.LINE_AA)
    return finish(shake(bloom(img, 0.85, 0.6), 3, f), f)


def sc_skin_burn(t, T, f):
    img = np.empty((H, W, 3), np.float32)
    p = t / T
    base = H * 0.55 - p * 60
    y = _yy - base
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
        x = 40 + i * 48 + r.uniform(-10, 10)
        pts = [(x, base + 150)]
        for j in range(8):
            px, py = pts[-1]
            pts.append((px + r.normal(0, 6), py - 18))
        cv2.polylines(glow, [np.array(pts, np.int32)], False, (1.6 * k, 1.1 * k, 0.6 * k), 2, cv2.LINE_AA)
        top = pts[-1]
        cv2.ellipse(glow, (int(top[0]), int(top[1]) + 6), (14, 6), 0, 180, 360, (1.5 * k, 0.9 * k, 0.4 * k), 2, cv2.LINE_AA)
    img += glow + cv2.GaussianBlur(glow, (0, 0), 12) * 1.5
    # heat embers above surface
    for i in range(90):
        ex = r.uniform(0, W)
        ey = base - ((r.uniform(0, 400) + t * r.uniform(40, 100)) % 400)
        cv2.circle(img, (int(ex), int(ey)), 2, (1.4 * k, 0.6 * k, 0.2 * k), -1, cv2.LINE_AA)
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
        m = cv2.GaussianBlur(m, (0, 0), 25)[..., None]
        img = lerp(img, c, m * alpha * heat)
    ring_r = lerp(60, 380, smooth(p / 0.35))
    ground_ring(img, M, 1024, 1000, ring_r, col(1.0, 0.95, 0.85), 3, 0.8)
    for i, rr in enumerate((120, 240, 380)):
        ground_ring(img, M, 1024, 1000, rr, col(0.9, 0.88, 0.82) * smooth((p - 0.3 - i * 0.1) / 0.1) * 0.6, 2, 0.3)
    mushroom(img, cx, cy, 120, 0.55 + 0.3 * p, seed=5)
    return finish(img, f)


def sc_cloud_tall(t, T, f):
    tex = terrain_tex(2048, 13)
    img, M = tilt_view(tex, 1024, 1024, 900, hz=0.66, depth=3.0, haze=col(0.80, 0.78, 0.75))
    p = t / T
    # Everest-like peak for scale on the right
    pk = np.array([[W * 0.62, H * 0.66], [W * 0.80, H * 0.50], [W * 0.86, H * 0.53], [W * 1.05, H * 0.66]], np.int32)
    cv2.fillPoly(img, [pk], (0.70, 0.70, 0.72), cv2.LINE_AA)
    snow = np.array([[W * 0.74, H * 0.545], [W * 0.80, H * 0.50], [W * 0.86, H * 0.53], [W * 0.88, H * 0.55]], np.int32)
    cv2.fillPoly(img, [snow], (0.95, 0.95, 0.97), cv2.LINE_AA)
    mushroom(img, W * 0.42, H * 0.665, 150, 0.45 + 0.55 * p, seed=7, fire=max(0, 0.35 - p) * 1.5)
    return finish(img, f)


def sc_ruins_dust(t, T, f):
    return finish(ruins(t, f, person=False, dust=smooth(t / 2)), f, grade=(1.0, 1.0, 0.97))


def sc_map_plume(t, T, f):
    tex = terrain_tex(2048, 21, True)
    img, M = tilt_view(tex, 1100, 1050, 650, hz=0.2, depth=1.5, mountains=False, haze=col(0.72, 0.74, 0.78))
    (tx, ty), = project(M, [(1100, 950)])
    p = smooth(t / T)
    ln = lerp(30, 520, p)
    ang = math.radians(-18)
    m = np.exp(-(((_xx - tx) * math.cos(ang) + (_yy - ty) * math.sin(ang) - ln / 2) / (ln / 2 + 1)) ** 2
               - ((-(_xx - tx) * math.sin(ang) + (_yy - ty) * math.cos(ang)) / (20 + 70 * p)) ** 2)
    n = cv2.resize(fbm(H // 4, W // 4, 9, 5, 4), (W, H))
    m = np.clip(m * (0.6 + 0.8 * n), 0, 1)[..., None]
    img = lerp(img, col(0.55, 0.50, 0.45), m * 0.85)
    img += radial(tx, ty, 9) * col(1.0, 0.3, 0.2)
    mushroom(img, tx, ty, 26, 1.0, seed=2)
    return finish(img, f)


def sc_street_green(t, T, f):
    st = street()
    camz = t * 0.6
    img, P = st.render(camz, sky=(col(0.58, 0.58, 0.55), col(0.80, 0.78, 0.72)), fog=col(0.74, 0.72, 0.66), fogd=120,
                       people=[dict(x=0.2, z=camz + 5.5, green=smooth((t - 0.8) / 1.0))])
    r = RNG(5)
    for i in range(300):
        x = r.uniform(0, W)
        y = (r.uniform(0, H) + t * r.uniform(40, 120)) % H
        cv2.circle(img, (int(x), int(y)), int(r.uniform(1, 3)), (0.86, 0.84, 0.78), -1, cv2.LINE_AA)
    return finish(img, f, grade=(0.98, 1.02, 0.96))


def sc_cells(t, T, f):
    img = np.empty((H, W, 3), np.float32)
    img[:] = lerp(col(0.25, 0.04, 0.05), col(0.10, 0.01, 0.02), np.clip(_yy / H, 0, 1)[..., None])
    r = RNG(6)
    cells = sorted([(r.uniform(-50, W + 50), r.uniform(-50, H + 50), r.uniform(0.3, 1.0)) for _ in range(70)], key=lambda c: c[2])
    for i, (x, y, d) in enumerate(cells):
        rad = 40 + 110 * d
        x += math.sin(t * 0.5 + i) * 15 * d
        y += -t * 20 * d
        layer = np.zeros((H, W, 3), np.float32)
        cv2.circle(layer, (int(x), int(y) % (H + 200) - 100), int(rad), (1, 1, 1), -1, cv2.LINE_AA)
        m = layer[..., :1]
        if d < 0.6:
            m = cv2.GaussianBlur(m, (0, 0), (0.6 - d) * 25).reshape(H, W, 1)
        sh = radial(x - rad * 0.3, (int(y) % (H + 200) - 100) - rad * 0.35, rad * 0.9)
        c = col(0.75, 0.10, 0.12) * (0.4 + 0.9 * sh) * (0.5 + 0.5 * d)
        img = img * (1 - m) + c * m
    # mutating cell in focus
    k = smooth((t - 1.0) / 2.0)
    cx, cy, rr = W / 2, H * 0.5, 150
    m = np.zeros((H, W), np.float32)
    pts = [(cx + (rr + 18 * math.sin(a * 5 + t * 2) * k) * math.cos(a), cy + (rr + 18 * math.sin(a * 5 + t * 2) * k) * math.sin(a))
           for a in np.linspace(0, 2 * math.pi, 120)]
    cv2.fillPoly(m, [np.array(pts, np.int32)], 1.0, cv2.LINE_AA)
    m = m[..., None]
    sh = radial(cx - 50, cy - 60, 140)
    c = lerp(col(0.85, 0.15, 0.15), col(0.25, 0.05, 0.08), k) * (0.4 + 0.9 * sh)
    img = img * (1 - m) + c * m
    img += radial(cx, cy, 30) * col(0.9, 0.2, 0.3) * (0.4 + 0.4 * math.sin(t * 4)) * k
    return finish(bloom(img, 0.7, 0.4), f, grade=(1.0, 1.0, 1.0))


def sc_history(t, T, f):
    tex = terrain_tex(2048, 15)
    img, M = tilt_view(tex, 1024, 1024, 900, hz=0.62, depth=3.0, haze=col(0.82, 0.78, 0.72))
    mushroom(img, W / 2, H * 0.625, 170, 0.75 + 0.25 * t / T, seed=9)
    sep = 1 - smooth((t - T * 0.35) / (T * 0.3))
    lum = img.mean(axis=2, keepdims=True)
    sepia = lum * col(1.05, 0.92, 0.75)
    img = lerp(img, sepia, sep)
    # old film scratches during the 1945 part
    r = RNG(f)
    if sep > 0.05:
        for _ in range(3):
            x = int(r.uniform(0, W))
            cv2.line(img, (x, 0), (x, H), (0.9 * sep, 0.85 * sep, 0.75 * sep), 1)
    return finish(img, f, grain=0.025 + 0.04 * sep)


def sc_ending(t, T, f):
    img = sc_history(T * 0.9 + t * 0.2, T, f)
    r = RNG(1)
    for i in range(80):
        x = r.uniform(0, W) + math.sin(t + i) * 10
        y = H - ((r.uniform(0, H) + t * r.uniform(30, 80)) % H)
        cv2.circle(img, (int(x), int(y)), 2, (1.0, 0.6, 0.25), -1, cv2.LINE_AA)
    return np.clip(img * (1 - smooth(t / T) * 0.95), 0, 1)


SCENES = {k[3:]: v for k, v in globals().items() if k.startswith('sc_')}


def render_scene(sid, scene, dur, out, fade_in=0.35):
    n = int(round(dur * FPS))
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
           '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    fn = SCENES[scene]
    for i in range(n):
        t = i / FPS
        img = fn(t, dur, i + hash(sid) % 1000)
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
        render_scene(s['id'], s['scene'], s['dur'], f"{outdir}/{s['id']}.mp4")
