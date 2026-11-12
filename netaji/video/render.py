"""Documentary renderer for the Hindi Netaji video (built on the Partition renderer).

Scene kinds (see plan.py):
  photo  real archive photo with a slow Ken Burns move, archive grading, film grain and vignette;
         small photos sit framed on a blurred copy of themselves
  map    vintage map of South Asia: British India, India / Pakistan fills, the Radcliffe line drawn on,
         migration arrows, city dots and Hindi labels
  card   dark textured card: chapter titles, big numbers, quotes, a clock
Overlays on any scene: date stamp, lower-third caption, quote, big number.
Every scene dissolves in from the previous one. Audio: narration + ducked music + a few soft hits.

Usage: python3 render.py preview [seconds] | full | still N.  Env: RES, FPS, CRF, PRESET, OUT_DIR, KEEP."""
import json, math, os, subprocess, sys, wave
from functools import lru_cache
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'assets')
OUT = os.environ.get('OUT_DIR', os.path.join(HERE, 'build'))
W, H = map(int, os.environ.get('RES', '1920x1080').split('x'))
U = H / 1080
FPS = int(os.environ.get('FPS', 30))
CRF = os.environ.get('CRF', '18'); PRESET = os.environ.get('PRESET', 'medium')
TIMING = json.load(open(os.path.join(OUT, 'timing.json')))
XFADE = 0.45

# ------------------------------------------------------------------ text
FONTS = {'bold': 'Mukta-ExtraBold.ttf', 'med': 'Mukta-Medium.ttf', 'serif': 'TiroDevanagariHindi.ttf'}
@lru_cache(None)
def font(kind, size):
    return ImageFont.truetype(os.path.join(ASSETS, 'fonts', FONTS[kind]), int(size * U), layout_engine=ImageFont.Layout.RAQM)

def text_img(txt, kind, size, fill=(255, 255, 255), shadow=True, stroke=0, maxw=None, spacing=1.15):
    f = font(kind, size)
    lines = wrap(txt, f, maxw) if maxw else txt.split('\n')
    asc, desc = f.getmetrics(); lh = int((asc + desc) * spacing)
    ws = [int(f.getlength(l)) for l in lines]
    pad = int(30 * U)
    im = Image.new('RGBA', (max(ws) + 2 * pad, lh * len(lines) + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        x = pad + (max(ws) - ws[i]) // 2
        d.text((x, pad + i * lh), l, font=f, fill=fill, stroke_width=int(stroke * U), stroke_fill=(0, 0, 0))
    if shadow:
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel('A').filter(ImageFilter.GaussianBlur(8 * U)).point(lambda v: int(v * 0.85)))
        base = Image.new('RGBA', im.size, (0, 0, 0, 0)); base.alpha_composite(sh, (int(3 * U), int(4 * U))); base.alpha_composite(im); im = base
    return im

def wrap(txt, f, maxw):
    out = []
    for para in txt.split('\n'):
        cur = ''
        for w in para.split(' '):
            t = (cur + ' ' + w).strip()
            if f.getlength(t) <= maxw * U or not cur: cur = t
            else: out.append(cur); cur = w
        out.append(cur)
    return out

# ------------------------------------------------------------------ helpers
def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def lerp(a, b, k): return a + (b - a) * k

@lru_cache(None)
def vignette():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    return (1 - 0.3 * np.clip(r - 0.6, 0, 1) ** 1.5 * 1.6).clip(0.6, 1)[..., None]

@lru_cache(None)
def grain(i):
    g = np.random.default_rng(i).normal(0, 1, (H // 2 + 1, W // 2 + 1)).astype(np.float32)
    g = np.asarray(Image.fromarray(((g * 40) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32) - 128
    return (g / 40 * 1.6)[..., None]

def finish(arr, t, amt=1.0):
    a = arr.astype(np.float32) * vignette()
    a += grain(int(t * FPS) % 6) * amt
    return a.clip(0, 255).astype(np.uint8)

# ------------------------------------------------------------------ photos
FALLBACK = {}
CROP = {'taihoku2': (0.02, 0.03, 0.98, 0.9), 'taihoku': (0.02, 0.02, 0.98, 0.97), 'wang_bose': (0.0, 0.0, 1.0, 0.98)}

@lru_cache(8)
def photo(name, grade):
    p = os.path.join(ASSETS, 'photos', name + '.jpg')
    hd = os.path.join(ASSETS, 'photos_hd', name + '.jpg')
    if os.path.exists(hd): p = hd                       # AI-upscaled copy (Real-ESRGAN) of a small original
    if not os.path.exists(p) and name in FALLBACK:
        print('  (fallback photo for', name, ')', flush=True); p = os.path.join(ASSETS, 'photos', FALLBACK[name] + '.jpg')
    im = Image.open(p)
    im = ImageOps.exif_transpose(im).convert('RGB')
    if name in CROP:                                      # keep only the photograph (no printed captions)
        l, t, r, bt = CROP[name]; im = im.crop((int(l * im.width), int(t * im.height), int(r * im.width), int(bt * im.height)))
    g = np.asarray(im.convert('L'), np.float32)          # trim black scan borders
    rows = np.where(g.mean(axis=1) > 28)[0]; cols = np.where(g.mean(axis=0) > 28)[0]
    if len(rows) > g.shape[0] * 0.5 and len(cols) > g.shape[1] * 0.5:
        im = im.crop((int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1))
    if grade == 'bw':
        g = ImageOps.autocontrast(im.convert('L'), cutoff=1)
        im = Image.merge('RGB', [g.point(lambda v: min(255, int(v * 1.04 + 6))), g.point(lambda v: int(v * 0.98 + 3)), g.point(lambda v: int(v * 0.88))])
    elif grade == 'color':
        im = ImageEnhance.Color(ImageOps.autocontrast(im, cutoff=0.5)).enhance(0.8)
    else:                                                  # paintings / maps: keep colour, light warm tone
        im = ImageEnhance.Color(im).enhance(0.92)
    # pre-scale so per-frame crops stay cheap
    k = min(1.0, (1.45 * max(W, H)) / max(im.size))
    if k < 1: im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=70, threshold=2))   # crisper detail
    return im

@lru_cache(8)
def blur_bg(name, grade):
    im = photo(name, grade)
    k = max(W / im.width, H / im.height) * 1.1
    b = im.resize((int(im.width * k), int(im.height * k)), Image.BILINEAR)
    b = b.crop(((b.width - W) // 2, (b.height - H) // 2, (b.width - W) // 2 + W, (b.height - H) // 2 + H))
    b = b.filter(ImageFilter.GaussianBlur(28 * U))
    return ImageEnhance.Brightness(b).enhance(0.42)

def draw_photo(sp, t, dur):
    name, grade = sp['img'], sp.get('grade', 'bw')
    im = photo(name, grade)
    k = ease(t / dur) if sp.get('ease', True) else t / dur
    z = lerp(sp.get('z0', 1.0), sp.get('z1', 1.12), k)
    fx = lerp(sp.get('fx0', 0.5), sp.get('fx1', sp.get('fx0', 0.5)), k)
    fy = lerp(sp.get('fy0', 0.5), sp.get('fy1', sp.get('fy0', 0.5)), k)
    frame = sp.get('frame')
    if frame is None:                          # fill the screen if the photo is big enough and close to 16:9
        cover = max(W / im.width, H / im.height)
        frame = cover > 2.1 or abs(im.width / im.height - W / H) > 0.55
    if not frame:
        cw, ch = W / z, H / z
        s = max(W / im.width, H / im.height)
        cw, ch = cw / s, ch / s
        x0 = fx * im.width - cw / 2; y0 = fy * im.height - ch / 2
        cw, ch = min(cw, im.width), min(ch, im.height)
        x0 = max(0, min(x0, im.width - cw)); y0 = max(0, min(y0, im.height - ch))
        out = im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
        return out
    # framed: the whole photo on a blurred copy, slowly scaling
    bg = blur_bg(name, grade).copy()
    hmax = sp.get('h', 0.84) * H; wmax = sp.get('w', 0.84) * W
    s = min(hmax / im.height, wmax / im.width, 1.8) * lerp(1.0, z / sp.get('z0', 1.0), 1) ** 0.35   # never blow a small photo up past 1.8x
    pw, ph = int(im.width * s), int(im.height * s)
    p = im.resize((pw, ph), Image.LANCZOS)
    px = int(W * sp.get('px', 0.5) - pw / 2); py = int(H * sp.get('py', 0.5) - ph / 2)
    sh = Image.new('L', (pw + 80, ph + 80), 0); ImageDraw.Draw(sh).rectangle([40, 40, 40 + pw, 40 + ph], fill=200)
    sh = sh.filter(ImageFilter.GaussianBlur(18 * U))
    bg.paste((0, 0, 0), (px - 40 + int(6 * U), py - 40 + int(10 * U)), sh)
    border = int(7 * U)
    bg.paste((236, 228, 210), (px - border, py - border, px + pw + border, py + ph + border))
    bg.paste(p, (px, py))
    return bg

# ------------------------------------------------------------------ 3D map
# The relief map is a ground plane seen by a tilted, slowly orbiting perspective camera. Country fills are raised as
# glowing 3D blocks, pins stand on stalks with shadows, flight routes rise as arcs above their ground shadow, and the
# far distance fades into haze. Spec: view=(lat, lon, width_deg) [+ view1], pitch (deg from straight down, default 48),
# yaw0/yaw1 (deg, slow orbit), plus fill, routes, pulse, cities, labels, arrows as before.
MJ = json.load(open(os.path.join(ASSETS, 'asia_merc.json')))
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(max(-85, min(85, lat))) / 2))
def ll(lat, lon): return (lon - MJ['lon0']) * MJ['pxd'], (merc(MJ['lat1']) - merc(lat)) * MJ['ky']
SEA_RGB = (30, 52, 62); HAZE = (214, 200, 170)

@lru_cache(None)
def map_level(lv):
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(os.path.join(ASSETS, 'asia_merc.jpg')).convert('RGB')
    if lv: im = im.resize((im.width >> lv, im.height >> lv), Image.LANCZOS)
    return im

@lru_cache(None)
def countries():
    return json.load(open(os.path.join(ASSETS, 'countries.json')))

FILL = {'red': (200, 40, 30), 'india': (226, 128, 40), 'gold': (230, 180, 60), 'blue': (60, 120, 200), 'green': (50, 140, 80),
        'gray': (120, 110, 100), 'purple': (150, 90, 190), 'white': (245, 240, 230)}
GROUP = {'india': ['India', 'Pakistan', 'Bangladesh'], 'taiwan': ['Taiwan'], 'japan': ['Japan'], 'russia': ['Russia'],
         'china': ['China'], 'germany': ['Germany'], 'afghan': ['Afghanistan'], 'burma': ['Myanmar'], 'singapore': ['Singapore', 'Malaysia'],
         'vietnam': ['Vietnam'], 'thailand': ['Thailand'], 'uk': ['United Kingdom'], 'austria': ['Austria'], 'indonesia': ['Indonesia'],
         'mongolia': ['Mongolia']}

class Cam:
    def __init__(s, cx, cy, w, pitch, yaw):
        s.w = w; D = w * 1.15; s.F = W * D / w
        ph, ps = math.radians(pitch), math.radians(yaw)
        Rz = np.array([[math.cos(ps), -math.sin(ps), 0], [math.sin(ps), math.cos(ps), 0], [0, 0, 1]])
        T = np.array([cx, cy, 0.0])
        s.C = T + Rz @ np.array([0, D * math.sin(ph), D * math.cos(ph)])
        f = (T - s.C) / D; r = Rz @ np.array([1.0, 0, 0]); d = np.cross(r, f)
        s.A = np.stack([r, d, f])
        K = np.array([[s.F, 0, W / 2], [0, s.F, H / 2], [0, 0, 1]])
        s.Hs = K @ np.stack([s.A[:, 0], s.A[:, 1], -s.A @ s.C], axis=1)
    def proj(s, X, Y, Z=0.0):
        c = s.A @ (np.array([X, Y, Z]) - s.C)
        z = max(c[2], 1e-3); return W / 2 + s.F * c[0] / z, H / 2 + s.F * c[1] / z, z
    def proj_many(s, pts, Z=0.0):
        P = np.asarray(pts, np.float64); P3 = np.column_stack([P, np.full(len(P), Z)])
        c = (P3 - s.C) @ s.A.T; z = np.maximum(c[:, 2], 1e-3)
        return np.column_stack([W / 2 + s.F * c[:, 0] / z, H / 2 + s.F * c[:, 1] / z])

@lru_cache(None)
def haze_mask():
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    return np.repeat(np.clip(1 - y / 0.42, 0, 1) ** 1.8 * 0.5, W, axis=1)[..., None]

def ground(cam):
    gpp = cam.w / W                                        # ground px per screen px at the centre
    lv = 0 if gpp < 1.6 else 1 if gpp < 3.2 else 2 if gpp < 6.4 else 3
    base = map_level(lv); sc = 1 / (1 << lv)
    Hl = np.diag([sc, sc, 1.0]) @ np.linalg.inv(cam.Hs)  # screen -> level pixel
    Hl = Hl / Hl[2, 2]
    co = (Hl[0, 0], Hl[0, 1], Hl[0, 2], Hl[1, 0], Hl[1, 1], Hl[1, 2], Hl[2, 0], Hl[2, 1])
    img = base.transform((W, H), Image.PERSPECTIVE, co, resample=Image.BICUBIC, fillcolor=SEA_RGB)
    a = np.asarray(img, np.float32)
    a = a * (1 - haze_mask()) + np.array(HAZE, np.float32) * haze_mask()   # aerial perspective
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')

def plane_icon(size, col=(250, 245, 235)):
    im = Image.new('RGBA', (size * 4, size * 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = size * 2; k = size / 10
    body = [(c + 9 * k, c), (c + 6 * k, c - 1.1 * k), (c - 7 * k, c - 0.9 * k), (c - 9 * k, c), (c - 7 * k, c + 0.9 * k), (c + 6 * k, c + 1.1 * k)]
    wing = [(c + 2 * k, c - 0.8 * k), (c - 2 * k, c - 9 * k), (c - 4 * k, c - 9 * k), (c - 2 * k, c), (c - 4 * k, c + 9 * k), (c - 2 * k, c + 9 * k), (c + 2 * k, c + 0.8 * k)]
    tail = [(c - 6 * k, c), (c - 8.5 * k, c - 3.5 * k), (c - 9.5 * k, c - 3.5 * k), (c - 8.5 * k, c), (c - 9.5 * k, c + 3.5 * k), (c - 8.5 * k, c + 3.5 * k)]
    for poly in (wing, tail, body): d.polygon(poly, fill=col + (255,), outline=(30, 20, 10, 255))
    return im

def sub_icon(size, col=(70, 75, 80)):
    im = Image.new('RGBA', (size * 4, size * 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = size * 2; k = size / 10
    d.ellipse([c - 9 * k, c - 1.6 * k, c + 9 * k, c + 1.6 * k], fill=col + (255,), outline=(240, 235, 220, 255), width=max(1, int(k / 2)))
    d.rectangle([c - 1 * k, c - 3.4 * k, c + 2.5 * k, c - 1.2 * k], fill=col + (255,), outline=(240, 235, 220, 255))
    return im

def car_icon(size, col=(40, 40, 40)):
    im = Image.new('RGBA', (size * 4, size * 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = size * 2; k = size / 10
    d.rounded_rectangle([c - 8 * k, c - 2 * k, c + 8 * k, c + 2.5 * k], radius=int(k), fill=col + (255,), outline=(240, 235, 220, 255))
    d.rounded_rectangle([c - 4 * k, c - 5 * k, c + 4 * k, c - 1.5 * k], radius=int(k), fill=col + (255,), outline=(240, 235, 220, 255))
    for x in (-5, 5): d.ellipse([c + x * k - 2 * k, c + 1 * k, c + x * k + 2 * k, c + 5 * k], fill=(20, 20, 20, 255), outline=(240, 235, 220, 255))
    return im
ICONS = {'plane': plane_icon, 'sub': sub_icon, 'car': car_icon, 'train': car_icon}

def _visible(pts):
    xs, ys = pts[:, 0], pts[:, 1]
    return not (xs.max() < -100 or xs.min() > W + 100 or ys.max() < -100 or ys.min() > H + 100)

def draw_map(sp, t, dur):
    k = ease(t / dur)
    (la0, lo0, w0) = sp.get('view', (24, 80, 40)); (la1, lo1, w1) = sp.get('view1', sp.get('view', (24, 80, 40)))
    x0, y0 = ll(la0, lo0); x1, y1 = ll(la1, lo1)
    cx, cy = lerp(x0, x1, k), lerp(y0, y1, k)
    w = math.exp(lerp(math.log(w0), math.log(w1), k)) * MJ['pxd']
    pitch = lerp(sp.get('pitch', 48), sp.get('pitch1', sp.get('pitch', 48)), k)
    yaw = lerp(sp.get('yaw0', -5.0), sp.get('yaw1', 5.0), t / dur)        # slow linear orbit
    cam = Cam(cx, cy, w, pitch, yaw)
    out = ground(cam)
    H3 = w * 0.014                                                        # block height (ground px) scales with the view
    for f in sp.get('fill', []):                                          # raised country blocks
        g, col = f[0], f[1]; at = f[2] if len(f) > 2 and f[2] is not None else -9
        a = ease((t - at) / 0.8)
        if len(f) > 3 and f[3] is not None: a *= 1 - ease((t - f[3]) / 0.8)
        if a <= 0: continue
        rs = [np.array([ll(la, lo) for lo, la in r]) for n in GROUP[g] for r in countries().get(n, [])]
        h = H3 * a
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        C = np.array(FILL[col], np.float32)
        steps = 7
        for j in range(steps + 1):                                         # walls: stacked slices, darker below
            zz = h * j / steps; shade = 0.45 + 0.35 * j / steps
            for r in rs:
                p = cam.proj_many(r, zz)
                if len(p) < 3 or not _visible(p): continue
                if j < steps: dl.polygon([tuple(q) for q in p], fill=tuple(int(c * shade) for c in C) + (int(235 * a),))
                else:
                    dl.polygon([tuple(q) for q in p], fill=tuple(int(c) for c in C) + (int(150 * a),))
                    dl.line([tuple(q) for q in p] + [tuple(p[0])], fill=tuple(min(255, int(c * 1.3) + 40) for c in C) + (int(255 * a),), width=int(4 * U))
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)      # soft drop shadow on the ground
        for r in rs:
            p = cam.proj_many(r + np.array([h * 0.6, h * 0.4]), 0)
            if len(p) >= 3 and _visible(p): ds.polygon([tuple(q) for q in p], fill=(0, 0, 0, int(110 * a)))
        out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10 * U)))
        out.alpha_composite(lay)
    d = ImageDraw.Draw(out)
    for rt in sp.get('routes', []):                  # dict(pts=[(lat, lon)...], at, dur, col, icon, arc)
        p = ease((t - rt.get('at', 0)) / rt.get('dur', 2.5))
        if p <= 0: continue
        g = []
        for (a0, b0), (a1, b1) in zip(rt['pts'], rt['pts'][1:]):
            X0, Y0 = ll(a0, b0); X1, Y1 = ll(a1, b1); L = math.hypot(X1 - X0, Y1 - Y0)
            hmax = rt.get('arc', 0.22 if rt.get('icon', 'plane') == 'plane' else 0.0) * L
            for u in np.linspace(0, 1, 40, endpoint=False): g.append((X0 + (X1 - X0) * u, Y0 + (Y1 - Y0) * u, hmax * math.sin(math.pi * u)))
        Xe, Ye = ll(*rt['pts'][-1]); g.append((Xe, Ye, 0.0))
        g = np.array(g); n = max(2, int(len(g) * p))
        g = g[:n]
        gr = [cam.proj(*q) for q in g]
        shp = [tuple(cam.proj(q[0], q[1], 0)[:2]) for q in g]
        col = FILL[rt.get('col', 'red')] + (255,)
        d.line(shp, fill=(0, 0, 0, 110), width=int(7 * U), joint='curve')                 # ground shadow
        air = [(q[0], q[1]) for q in gr]
        d.line(air, fill=(20, 12, 8, 200), width=int(12 * U), joint='curve'); d.line(air, fill=col, width=int(6 * U), joint='curve')
        ic = rt.get('icon')
        if ic and len(air) > 1:
            (xa, ya), (xb, yb) = air[-2], air[-1]
            ang = math.degrees(math.atan2(yb - ya, xb - xa))
            im = ICONS[ic](int(rt.get('size', 28) * U)).rotate(-ang, resample=Image.BICUBIC)
            out.alpha_composite(im, (int(xb - im.width / 2), int(yb - im.height / 2))); d = ImageDraw.Draw(out)
    for a_ in sp.get('arrows', []):                   # (lat0, lon0, lat1, lon1, colour, at): raised arcs
        la0_, lo0_, la1_, lo1_, col, at = a_
        p = ease((t - at) / 1.6)
        if p <= 0: continue
        X0, Y0 = ll(la0_, lo0_); X1, Y1 = ll(la1_, lo1_); L = math.hypot(X1 - X0, Y1 - Y0)
        us = np.linspace(0, p, 40)
        pts = [cam.proj(X0 + (X1 - X0) * u, Y0 + (Y1 - Y0) * u, 0.25 * L * math.sin(math.pi * u))[:2] for u in us]
        c = FILL[col] + (255,)
        d.line(pts, fill=(20, 15, 10, 200), width=int(20 * U)); d.line(pts, fill=c, width=int(13 * U))
        (xa, ya), (xb, yb) = pts[-2], pts[-1]; ang = math.atan2(yb - ya, xb - xa); Lh = 30 * U
        d.polygon([(xb + math.cos(ang) * Lh * 0.6, yb + math.sin(ang) * Lh * 0.6), (xb + math.cos(ang + 2.5) * Lh, yb + math.sin(ang + 2.5) * Lh),
                   (xb + math.cos(ang - 2.5) * Lh, yb + math.sin(ang - 2.5) * Lh)], fill=c, outline=(20, 15, 10, 220))
    for pl in sp.get('pulse', []):                    # ground rings (drawn in perspective) + a standing pin
        la, lo, at = pl[:3]; col = FILL[pl[3] if len(pl) > 3 else 'red']
        if t < at: continue
        X, Y = ll(la, lo); R0 = w * 0.006
        ang = np.linspace(0, 2 * math.pi, 48)
        for j in range(3):
            ph = ((t - at) * 0.7 + j / 3) % 1.0
            R = R0 * (1 + 7 * ph); al = int(230 * (1 - ph) * min(1, (t - at) / 0.4))
            ring = cam.proj_many(np.column_stack([X + R * np.cos(ang), Y + R * np.sin(ang)]))
            d.line([tuple(q) for q in ring] + [tuple(ring[0])], fill=col + (al,), width=int(5 * U))
        draw_pin(out, cam, X, Y, w, col, min(1, (t - at) / 0.4))
        d = ImageDraw.Draw(out)
    for c in sp.get('cities', []):                    # (hindi name, lat, lon, at, dx, dy[, size]): pins with labels
        name, la, lo, at = c[:4]; dx, dy = (c[4], c[5]) if len(c) > 5 else (0, -1)
        a = ease((t - at) / 0.5)
        if a <= 0: continue
        X, Y = ll(la, lo)
        top = draw_pin(out, cam, X, Y, w, (250, 240, 220), a, small=True)
        ti = text_img(name, 'bold', c[6] if len(c) > 6 else 48, fill=(255, 248, 235), stroke=3)
        ti.putalpha(ti.getchannel('A').point(lambda v: int(v * a)))
        out.alpha_composite(ti, (int(top[0] - ti.width / 2 + dx * 60 * U), int(top[1] - ti.height / 2 + dy * 44 * U)))
    for lab in sp.get('labels', []):                  # (hindi text, lat, lon, at, size[, colour]) floating over the ground
        txt, la, lo, at = lab[:4]; size = lab[4] if len(lab) > 4 else 56
        a = ease((t - at) / 0.6)
        if a <= 0: continue
        x, y, _ = cam.proj(*ll(la, lo))
        ti = text_img(txt, 'bold', size, fill=lab[5] if len(lab) > 5 else (255, 250, 240), stroke=3)
        ti.putalpha(ti.getchannel('A').point(lambda v: int(v * a)))
        out.alpha_composite(ti, (int(x - ti.width / 2), int(y - ti.height / 2 - (1 - a) * 20 * U)))
    return out.convert('RGB')

def draw_pin(out, cam, X, Y, w, col, a, small=False):
    hp = w * (0.035 if small else 0.06)
    gx, gy, _ = cam.proj(X, Y, 0); tx, ty, tz = cam.proj(X, Y, hp * min(1, a * 1.5))
    d = ImageDraw.Draw(out)
    d.ellipse([gx - 16 * U, gy - 6 * U, gx + 16 * U, gy + 6 * U], fill=(0, 0, 0, int(120 * a)))
    d.line([(gx, gy), (tx, ty)], fill=(30, 20, 10, int(255 * a)), width=int(5 * U))
    r = (11 if small else 16) * U
    d.ellipse([tx - r - 3 * U, ty - r - 3 * U, tx + r + 3 * U, ty + r + 3 * U], fill=(30, 20, 10, int(255 * a)))
    d.ellipse([tx - r, ty - r, tx + r, ty + r], fill=tuple(col) + (int(255 * a),))
    d.ellipse([tx - r * 0.45, ty - r * 0.6, tx - r * 0.05, ty - r * 0.2], fill=(255, 255, 255, int(150 * a)))
    return tx, ty - r

# ------------------------------------------------------------------ cards
@lru_cache(None)
def card_bg(tone):
    rng = np.random.default_rng(5)
    base = {'dark': (22, 20, 18), 'red': (40, 10, 10), 'paper': (60, 50, 38)}[tone]
    a = np.ones((H, W, 3), np.float32) * np.array(base, np.float32)
    n = np.asarray(Image.fromarray(rng.normal(128, 50, (H // 8, W // 8)).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) - 128
    a += n[..., None] * 0.12
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))

def draw_clock(img, t, sp):
    d = ImageDraw.Draw(img); cx, cy, R = W * 0.5, H * 0.47, 250 * U
    d.ellipse([cx - R - 14 * U, cy - R - 14 * U, cx + R + 14 * U, cy + R + 14 * U], fill=(70, 55, 35))
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(232, 220, 195))
    for i in range(60):
        a = math.radians(i * 6); r0 = R * (0.86 if i % 5 == 0 else 0.92)
        d.line([cx + math.sin(a) * r0, cy - math.cos(a) * r0, cx + math.sin(a) * R * 0.97, cy - math.cos(a) * R * 0.97],
               fill=(40, 30, 20), width=int((6 if i % 5 == 0 else 2) * U))
    sec = sp.get('sec0', 50) + t * 1.0
    mins = 59 + sec / 60; hrs = 11 + mins / 60
    for ang, L, wd in ((hrs * 30, 0.5, 14), (mins * 6, 0.78, 9)):
        a = math.radians(ang); d.line([cx, cy, cx + math.sin(a) * R * L, cy - math.cos(a) * R * L], fill=(30, 20, 15), width=int(wd * U))
    a = math.radians((sec % 60) * 6)
    d.line([cx - math.sin(a) * R * 0.15, cy + math.cos(a) * R * 0.15, cx + math.sin(a) * R * 0.85, cy - math.cos(a) * R * 0.85], fill=(170, 30, 25), width=int(4 * U))
    d.ellipse([cx - 14 * U, cy - 14 * U, cx + 14 * U, cy + 14 * U], fill=(30, 20, 15))

@lru_cache(64)
def stamp_img(txt, col, size=70):
    a = text_img(txt, 'bold', size, fill=col + (255,), shadow=False)
    pad = int(26 * U); im = Image.new('RGBA', (a.width + pad * 2, a.height + pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([int(8 * U), int(8 * U), im.width - int(8 * U), im.height - int(8 * U)], radius=int(14 * U), outline=col + (255,), width=int(7 * U))
    d.rounded_rectangle([int(20 * U), int(20 * U), im.width - int(20 * U), im.height - int(20 * U)], radius=int(8 * U), outline=col + (255,), width=int(3 * U))
    im.alpha_composite(a, (pad, int(-8 * U)))
    noise = np.random.default_rng(len(txt)).random((im.height, im.width))       # worn ink
    al = np.asarray(im.getchannel('A'), np.float32) * np.where(noise < 0.13, 0.25, 0.92)
    im.putalpha(Image.fromarray(al.clip(0, 255).astype(np.uint8)))
    return im.rotate(11, expand=True, resample=Image.BICUBIC)

def put_stamp(img, txt, col, cx, cy, t, at, size=70):
    if t < at: return
    k = ease((t - at) / 0.22); sc = 1.9 - 0.9 * k
    st = stamp_img(txt, col, size)
    st = st.resize((max(1, int(st.width * sc)), max(1, int(st.height * sc))), Image.BICUBIC)
    st.putalpha(st.getchannel('A').point(lambda v: int(v * k)))
    img.alpha_composite(st, (int(cx - st.width / 2), int(cy - st.height / 2)))

@lru_cache(4)
def paper(w, h, seed=1):
    rng = np.random.default_rng(seed)
    a = np.ones((h, w, 3), np.float32) * np.array([226, 210, 172], np.float32)
    n = np.asarray(Image.fromarray(rng.normal(128, 50, (h // 6, w // 6)).clip(0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) - 128
    a += n[..., None] * 0.18
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2)
    a *= (1 - 0.25 * np.clip(r - 0.7, 0, 1))[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')

def draw_doc(img, sp, t):
    doc = sp['doc']; pw, ph = int(1180 * U), int(800 * U)
    pg = paper(pw, ph).copy(); d = ImageDraw.Draw(pg)
    d.rectangle([int(30 * U), int(30 * U), pw - int(30 * U), ph - int(30 * U)], outline=(120, 90, 60, 255), width=int(3 * U))
    ti = text_img(doc['title'], 'bold', 58, fill=(60, 35, 20), shadow=False); pg.alpha_composite(ti, ((pw - ti.width) // 2, int(40 * U)))
    d.line([int(90 * U), int(170 * U), pw - int(90 * U), int(170 * U)], fill=(120, 90, 60, 255), width=int(3 * U))
    y = int(200 * U)
    for txt, at in doc['lines']:
        if t >= at:
            n = max(1, int(len(txt) * min(1, (t - at) / 0.9)))         # typewriter
            li = text_img(txt[:n], 'serif', 50, fill=(40, 28, 18), shadow=False); pg.alpha_composite(li, (int(90 * U), y))
        y += int(92 * U)
    a = ease(t / 0.6)
    sh = Image.new('RGBA', (pw + 80, ph + 80), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([40, 40, 40 + pw, 40 + ph], fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(20 * U))
    rot = sp.get('rot', -2.0)
    full = Image.new('RGBA', img.size, (0, 0, 0, 0))
    x0, y0 = (W - pw) // 2, (H - ph) // 2 + int((1 - a) * 60 * U)
    full.alpha_composite(sh, (x0 - 40 + int(10 * U), y0 - 40 + int(16 * U))); full.alpha_composite(pg, (x0, y0))
    if doc.get('stamp'):
        txt, at, col = doc['stamp']; put_stamp(full, txt, FILL[col], x0 + pw * 0.7, y0 + ph * 0.72, t, at, 78)
    full = full.rotate(rot, resample=Image.BICUBIC, center=(W / 2, H / 2))
    full.putalpha(full.getchannel('A').point(lambda v: int(v * a)))
    img.alpha_composite(full)

def draw_check(img, sp, t):
    rows = sp['check']; n = len(rows); y0 = H / 2 - (n * 150 * U) / 2 + 20 * U
    for i, (txt, at) in enumerate(rows):
        a = ease((t - at) / 0.5)
        if a <= 0: continue
        y = y0 + i * 150 * U; x = W * 0.16
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        b = 46 * U
        d.rectangle([x, y - b, x + 2 * b, y + b], outline=(235, 225, 205, 255), width=int(5 * U))
        p = ease((t - at - 0.25) / 0.35)
        if p > 0:
            c = (220, 40, 30, 255)
            d.line([x + 10 * U, y - b + 10 * U, x + 10 * U + (2 * b - 20 * U) * min(1, p * 2), y - b + 10 * U + (2 * b - 20 * U) * min(1, p * 2)], fill=c, width=int(11 * U))
            if p > 0.5: q = (p - 0.5) * 2; d.line([x + 2 * b - 10 * U, y - b + 10 * U, x + 2 * b - 10 * U - (2 * b - 20 * U) * q, y - b + 10 * U + (2 * b - 20 * U) * q], fill=c, width=int(11 * U))
        ti = text_img(txt, 'bold', 70, fill=(250, 244, 232)); lay.alpha_composite(ti, (int(x + 2 * b + 30 * U), int(y - ti.height / 2)))
        lay.putalpha(lay.getchannel('A').point(lambda v: int(v * a))); img.alpha_composite(lay, (int((1 - a) * -40 * U), 0))

def draw_files(img, sp, t):
    fs = sp['files']; n = len(fs); fw, fh = 470 * U, 560 * U; gap = 70 * U
    x_start = W / 2 - (n * fw + (n - 1) * gap) / 2; yb = H * 0.53
    for i, (year, name, at) in enumerate(fs):
        a = ease((t - at) / 0.5)
        if a <= 0: continue
        x = x_start + i * (fw + gap); y = yb - fh / 2 + (1 - a) * 80 * U
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle([x + 12 * U, y + 18 * U, x + fw + 12 * U, y + fh + 18 * U], radius=int(14 * U), fill=(0, 0, 0, 120))
        d.rounded_rectangle([x, y - 50 * U, x + fw * 0.45, y + 20 * U], radius=int(12 * U), fill=(196, 160, 100, 255))
        d.rounded_rectangle([x, y, x + fw, y + fh], radius=int(14 * U), fill=(214, 180, 118, 255), outline=(120, 90, 50, 255), width=int(3 * U))
        ty = text_img(year, 'bold', 64, fill=(70, 40, 20), shadow=False); lay.alpha_composite(ty, (int(x + fw / 2 - ty.width / 2), int(y + 40 * U)))
        tn = text_img(name, 'bold', 52, fill=(60, 35, 18), shadow=False, maxw=420); lay.alpha_composite(tn, (int(x + fw / 2 - tn.width / 2), int(y + 150 * U)))
        d.line([x + 40 * U, y + 140 * U, x + fw - 40 * U, y + 140 * U], fill=(120, 90, 50, 255), width=int(3 * U))
        for st in sp.get('stamps', []):
            if st[0] == i: put_stamp(lay, st[1], FILL[st[2]], x + fw / 2, y + fh * 0.72, t, st[3], 54)
        lay.putalpha(lay.getchannel('A').point(lambda v: int(v * a))); img.alpha_composite(lay)
    hl = sp.get('dim_others')
    if hl:
        idx, at = hl; a = ease((t - at) / 0.5) * 0.45
        if a > 0:
            for i in range(n):
                if i == idx: continue
                x = x_start + i * (fw + gap)
                ov_ = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(ov_).rounded_rectangle([x - 6 * U, yb - fh / 2 - 56 * U, x + fw + 20 * U, yb + fh / 2 + 26 * U], radius=int(16 * U), fill=(12, 10, 8, int(255 * a))); img.alpha_composite(ov_)

def draw_card(sp, t, dur):
    if sp.get('bgimg'):
        img = blur_bg(sp['bgimg'], sp.get('grade', 'bw')).copy()
    else:
        img = card_bg(sp.get('tone', 'dark')).copy()
    img = img.convert('RGBA')
    if sp.get('doc'): draw_doc(img, sp, t)
    if sp.get('check'): draw_check(img, sp, t)
    if sp.get('files'): draw_files(img, sp, t)
    return img.convert('RGB')

# ------------------------------------------------------------------ overlays
@lru_cache(None)
def fire_grad():
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    return np.clip((y - 0.35) / 0.65, 0, 1) ** 1.6

def fire_layer(t, a):
    rng = np.random.default_rng(int(t * FPS))
    fl = 0.75 + 0.25 * math.sin(t * 13) * math.sin(t * 7.3 + 1)
    n = np.asarray(Image.fromarray(rng.normal(128, 60, (9, 16)).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255
    al = np.clip(fire_grad() * (0.55 + 0.6 * n) * fl * a, 0, 0.85)
    lay = np.zeros((H, W, 4), np.uint8); lay[..., 0] = 255; lay[..., 1] = (90 + 80 * n).astype(np.uint8); lay[..., 2] = 20
    lay[..., 3] = (al * 255).astype(np.uint8)
    im = Image.fromarray(lay, 'RGBA'); d = ImageDraw.Draw(im)
    r2 = np.random.default_rng(7)
    for i in range(70):                                   # rising embers
        x0 = r2.random() * W; sp_ = 120 + r2.random() * 260; ph = r2.random() * 10
        y = H - ((t * sp_ + ph * 200) % (H * 0.9)); x = x0 + 30 * math.sin(t * 2 + i)
        r = (2 + r2.random() * 4) * U; al2 = int(255 * a * min(1, (y - H * 0.1) / (H * 0.4)))
        if al2 > 0: d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 190 + int(60 * r2.random()), 90, al2))
    return im

def fade_alpha(im, a):
    if a >= 1: return im
    im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * a))); return im

@lru_cache(64)
def ov_img(kind, txt, sub=''):
    if kind == 'title':
        a = text_img(txt, 'bold', 108, fill=(250, 240, 225), maxw=1500)
        if not sub: return a
        b = text_img(sub, 'med', 58, fill=(225, 175, 120))
        im = Image.new('RGBA', (max(a.width, b.width), a.height + b.height - int(30 * U)), (0, 0, 0, 0))
        im.alpha_composite(b, ((im.width - b.width) // 2, 0)); im.alpha_composite(a, ((im.width - a.width) // 2, b.height - int(40 * U)))
        return im
    if kind == 'big':
        a = text_img(txt, 'bold', 150, fill=(255, 214, 120))
        if not sub: return a
        b = text_img(sub, 'bold', 62, fill=(245, 235, 220), maxw=1300)
        im = Image.new('RGBA', (max(a.width, b.width), a.height + b.height - int(50 * U)), (0, 0, 0, 0))
        im.alpha_composite(a, ((im.width - a.width) // 2, 0)); im.alpha_composite(b, ((im.width - b.width) // 2, a.height - int(50 * U)))
        return im
    if kind == 'quote':
        return text_img('“' + txt + '”', 'serif', 80, fill=(255, 248, 235), maxw=1400, spacing=1.35)
    if kind == 'date':
        a = text_img(txt, 'bold', 64, fill=(255, 250, 240), shadow=True)
        im = Image.new('RGBA', (a.width, a.height + int(12 * U)), (0, 0, 0, 0)); im.alpha_composite(a)
        ImageDraw.Draw(im).rectangle([int(30 * U), a.height - int(26 * U), a.width - int(30 * U), a.height - int(18 * U)], fill=(200, 40, 30, 255))
        return im
    if kind == 'caption':
        a = text_img(txt, 'med', 46, fill=(250, 245, 235), shadow=False)
        im = Image.new('RGBA', (a.width + int(30 * U), a.height - int(20 * U)), (0, 0, 0, 0))
        ImageDraw.Draw(im).rectangle([0, 0, im.width, im.height], fill=(10, 8, 6, 170))
        ImageDraw.Draw(im).rectangle([0, 0, int(8 * U), im.height], fill=(200, 40, 30, 255))
        im.alpha_composite(a, (int(16 * U), -int(10 * U)))
        return im
    raise ValueError(kind)

def overlays(img, sp, t, dur):
    img = img.convert('RGBA')
    for o in sp.get('ov', []):
        kind, txt = o[0], o[1]; opt = o[2] if len(o) > 2 else {}
        at = opt.get('at', 0.3); a = ease((t - at) / 0.6)
        if 'off' in opt: a *= 1 - ease((t - opt['off']) / 0.5)
        if a <= 0: continue
        if kind == 'flash':
            dt = t - at; al = math.exp(-dt * 4.5) if dt >= 0 else 0
            if al > 0.01: img.alpha_composite(Image.new('RGBA', img.size, (255, 236, 200, int(255 * al))))
            continue
        if kind == 'fire':
            img.alpha_composite(fire_layer(t, a)); continue
        im = ov_img(kind, txt, opt.get('sub', ''))
        if kind in ('quote', 'big', 'title') and opt.get('dim', True):
            dim = Image.new('RGBA', img.size, (0, 0, 0, int((165 if kind == 'quote' else 120) * a))); img.alpha_composite(dim)
        if kind == 'date': x, y = int(70 * U), int(60 * U)
        elif kind == 'caption': x, y = int(80 * U), H - im.height - int(90 * U)
        else:
            x, y = int(opt.get('x', 0.5) * W - im.width / 2), int(opt.get('y', 0.5) * H - im.height / 2)
            if kind in ('title', 'big'):            # gentle rise
                y += int((1 - a) * 30 * U)
        img.alpha_composite(fade_alpha(im, a), (x, y))
    return img.convert('RGB')

# ------------------------------------------------------------------ scenes
import plan
SCENES = plan.resolve(TIMING)

def frame_of(i, t):
    sc = TIMING['scenes'][i]; sp = SCENES[i]; dur = sc['end'] - sc['start']
    tt = t + sp.get('_t0', 0.0)
    D = dur + sp.get('_t0', 0.0) + sp.get('_tail', 0.0)
    kind = sp['kind']
    if kind == 'photo': img = draw_photo(sp, tt, D)
    elif kind == 'map': img = draw_map(sp, tt, D)
    else: img = draw_card(sp, tt, D)
    for o in sp.get('ov', []):
        if o[0] == 'flash':
            dt = t - o[2].get('at', 0)
            if 0 <= dt < 0.9:
                amp = 26 * U * (1 - dt / 0.9) ** 2
                img = img.transform(img.size, Image.AFFINE, (1, 0, amp * math.sin(dt * 61), 0, 1, amp * math.cos(dt * 47)), resample=Image.BILINEAR)
    img = overlays(img, sp, t, dur)
    return np.asarray(img)

def render_scene(i):
    sc = TIMING['scenes'][i]; dur = sc['end'] - sc['start']
    path = os.path.join(OUT, 'scenes', f'{i + 1:03d}.mp4')
    if os.path.exists(path) and os.environ.get('KEEP'): return path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    nf = int(round(sc['end'] * FPS)) - int(round(sc['start'] * FPS))
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', PRESET, '-crf', CRF, '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    prev_last = None
    if i > 0 and not SCENES[i].get('cut'):
        ps = TIMING['scenes'][i - 1]
        prev_last = frame_of(i - 1, ps['end'] - ps['start'] - 0.5 / FPS).astype(np.float32)
    for f in range(nf):
        t = f / FPS
        a = frame_of(i, t).astype(np.float32)
        if prev_last is not None and t < XFADE:
            k = ease(t / XFADE); a = prev_last * (1 - k) + a * k
        if i == 0 and t < 1.0: a *= ease(t / 1.0)
        if SCENES[i].get('fadeout'): a *= 1 - ease((t - (nf / FPS - 2.0)) / 1.8)
        p.stdin.write(finish(a, sc['start'] + t, SCENES[i].get('grain', 1.0)).tobytes())
    p.stdin.close(); p.wait()
    print(f'scene {i + 1} done ({nf} frames)', flush=True)
    return path

def hits_track(n_scenes, total, sr=48000):
    out = np.zeros(int(total * sr) + sr, np.float32)
    def boom():
        n = int(2.5 * sr); t = np.arange(n) / sr
        s = np.sin(2 * np.pi * (42 + 30 * np.exp(-t * 6)) * t) * np.exp(-t * 2.2)
        s += np.random.default_rng(2).normal(0, 1, n) * np.exp(-t * 30) * 0.08
        return (s * 0.30).astype(np.float32)
    B = boom()
    for i in range(n_scenes):
        sp = SCENES[i]
        if sp.get('boom') is not None:
            k = int((TIMING['scenes'][i]['start'] + sp['boom']) * sr); e = min(len(out), k + len(B)); out[k:e] += B[:e - k]
    return out

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'preview'
    n = len(TIMING['scenes'])
    if mode == 'still':
        i = int(sys.argv[2]) - 1; sc = TIMING['scenes'][i]; tt = float(sys.argv[3]) if len(sys.argv) > 3 else (sc['end'] - sc['start']) * 0.7
        Image.fromarray(finish(frame_of(i, tt).astype(np.float32), tt)).save(os.path.join(OUT, f'still_{i + 1:03d}.jpg'), quality=90)
        return
    if mode == 'preview':
        lim = float(sys.argv[2]) if len(sys.argv) > 2 else 1e9
        n = len([s for s in TIMING['scenes'] if s['start'] < lim]); name = 'Netaji_Preview.mp4'
    else:
        name = 'Netaji_Rahasyamayi_Maut.mp4'
    total = TIMING['scenes'][n - 1]['end']
    with Pool(int(os.environ.get('WORKERS', 4))) as pool:
        paths = pool.map(render_scene, range(n), chunksize=1)
    lst = os.path.join(OUT, 'concat.txt')
    open(lst, 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in paths))
    hits = hits_track(n, total)
    with wave.open(os.path.join(OUT, 'hits.wav'), 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(48000); wf.writeframes((np.clip(hits, -1, 1) * 32767).astype(np.int16).tobytes())
    out = os.path.join(OUT, name)
    fc = (f'[1:a]atrim=0:{total},asplit=2[v][vk];[2:a]atrim=0:{total}[s];'
          f'[3:a]atrim=0:{total},volume=0.32[m0];[m0][vk]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=600[m];'
          f'[v][s][m]amix=inputs=3:normalize=0:duration=first,afade=t=out:st={total - 2}:d=2,alimiter=limit=0.95[a]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-i', os.path.join(OUT, 'narration.wav'),
                    '-i', os.path.join(OUT, 'hits.wav'), '-i', os.path.join(OUT, 'music.wav'), '-filter_complex', fc,
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', str(total), '-movflags', '+faststart', out], check=True)
    print('wrote', out, round(total, 1), 's')

if __name__ == '__main__':
    main()
