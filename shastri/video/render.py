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
def map_level(lv, nob=False):
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(os.path.join(ASSETS, 'asia_merc_nob.jpg' if nob else 'asia_merc.jpg')).convert('RGB')
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
         'mongolia': ['Mongolia'], 'uzbek': ['Uzbekistan'], 'pakistan': ['Pakistan'], 'india1': ['India'], 'ussr': ['Russia', 'Ukraine', 'Belarus', 'Kazakhstan', 'Uzbekistan', 'Turkmenistan', 'Kyrgyzstan', 'Tajikistan', 'Georgia', 'Armenia', 'Azerbaijan', 'Lithuania', 'Latvia', 'Estonia', 'Moldova']}

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

def ground(cam, nob=False):
    gpp = cam.w / W                                        # ground px per screen px at the centre
    lv = 0 if gpp < 1.6 else 1 if gpp < 3.2 else 2 if gpp < 6.4 else 3
    base = map_level(lv, nob); sc = 1 / (1 << lv)
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

# ------------------------------------------------------------------ Sikander extras: custom regions, rivers, battle board, units
def _plan():
    return sys.modules.get('plan')

def custom_rings(g):
    P = _plan()
    if P is None or g not in getattr(P, 'CUSTOM', {}): return None
    return [np.array([ll(la, lo) for la, lo in ring]) for ring in P.CUSTOM[g]]

def draw_rivers(out, cam, sp, t, w):
    P = _plan(); d = ImageDraw.Draw(out)
    for rv in sp.get('rivers', []):                       # (key, at[, dur, colour, width])
        key, at = rv[0], rv[1]; dur = rv[2] if len(rv) > 2 else 1.5
        col = rv[3] if len(rv) > 3 else (90, 190, 255); wd = rv[4] if len(rv) > 4 else 7
        p = ease((t - at) / dur) if dur > 0 else (1.0 if t >= at else 0)
        if p <= 0: continue
        pts = P.RIVERS[key]; dense = []
        for (a0, b0), (a1, b1) in zip(pts, pts[1:]):
            for u in np.linspace(0, 1, 12, endpoint=False): dense.append(ll(a0 + (a1 - a0) * u, b0 + (b1 - b0) * u))
        dense.append(ll(*pts[-1])); n = max(2, int(len(dense) * p))
        sc = [tuple(q) for q in cam.proj_many(dense[:n])]
        glow = Image.new('RGBA', out.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        gd.line(sc, fill=col + (200,), width=int(wd * 3 * U), joint='curve')
        out.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10 * U)))
        d = ImageDraw.Draw(out); d.line(sc, fill=(20, 40, 70, 230), width=int((wd + 4) * U), joint='curve'); d.line(sc, fill=col + (255,), width=int(wd * U), joint='curve')

def elephant_icon(size, col=(70, 60, 55)):
    im = Image.new('RGBA', (size * 4, size * 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = size * 2; k = size / 10
    o = (235, 225, 200, 255); f = col + (255,)
    for lx in (-5.5, -2.5, 2.5, 5.5): d.rectangle([c + lx * k - 1.2 * k, c + 1 * k, c + lx * k + 1.2 * k, c + 7 * k], fill=f, outline=o, width=max(1, int(k / 2)))
    d.ellipse([c - 8 * k, c - 5 * k, c + 6 * k, c + 3.5 * k], fill=f, outline=o, width=max(1, int(k / 2)))
    d.ellipse([c + 3 * k, c - 7 * k, c + 10 * k, c + 0 * k], fill=f, outline=o, width=max(1, int(k / 2)))
    d.line([(c + 9 * k, c - 2 * k), (c + 11 * k, c + 3 * k), (c + 10 * k, c + 7 * k)], fill=f, width=int(2.2 * k))
    d.line([(c + 8.5 * k, c - 1 * k), (c + 12 * k, c - 1.5 * k)], fill=(250, 245, 230, 255), width=max(1, int(k * 0.8)))   # tusk
    d.rectangle([c - 4 * k, c - 8 * k, c + 2 * k, c - 4.5 * k], fill=(200, 60, 40, 255), outline=o)                         # howdah
    return im

def boat_icon(size, col=(110, 80, 50)):
    im = Image.new('RGBA', (size * 4, size * 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = size * 2; k = size / 10
    d.polygon([(c - 9 * k, c - 1 * k), (c + 9 * k, c - 1 * k), (c + 6 * k, c + 3 * k), (c - 6 * k, c + 3 * k)], fill=col + (255,), outline=(240, 230, 210, 255))
    for x in (-5, -2, 1, 4): d.ellipse([c + x * k - 1.2 * k, c - 3.4 * k, c + x * k + 1.2 * k, c - 1 * k], fill=(200, 200, 210, 255))
    return im
def chariot_icon(size, col=(150, 90, 40)):
    im = Image.new('RGBA', (size * 4, size * 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = size * 2; k = size / 10; o = (240, 230, 210, 255)
    d.ellipse([c - 9 * k, c - 4 * k, c + 1 * k, c + 2 * k], fill=(90, 60, 40, 255), outline=o)                    # horse body
    d.line([(c - 8 * k, c - 2 * k), (c - 11 * k, c - 6 * k)], fill=(90, 60, 40, 255), width=int(2.5 * k))           # neck
    for lx in (-7, -3): d.line([(c + lx * k, c + 1 * k), (c + lx * k, c + 6 * k)], fill=(90, 60, 40, 255), width=int(1.4 * k))
    d.line([(c + 1 * k, c - 1 * k), (c + 4 * k, c - 1 * k)], fill=o, width=int(k))
    d.rectangle([c + 3 * k, c - 4 * k, c + 9 * k, c + 1 * k], fill=col + (255,), outline=o)
    d.ellipse([c + 3.5 * k, c - 1 * k, c + 8.5 * k, c + 6 * k], outline=o, width=int(1.2 * k))
    return im
ICONS.update({'elephant': elephant_icon, 'boat': boat_icon, 'chariot': chariot_icon})

# --- battle board: a stylised 3D terrain (texture px coordinates), river, rain-soaked fields, moving unit blocks
BT_W, BT_H = 6400, 4600
BT_OFF = (1200, 1000)          # plan coordinates (0..4000, 0..2600) sit inside a bigger texture so its edge never shows
@lru_cache(None)
def battle_tex():
    rng = np.random.default_rng(11)
    n1 = np.asarray(Image.fromarray(rng.normal(128, 50, (BT_H // 40, BT_W // 40)).clip(0, 255).astype(np.uint8)).resize((BT_W, BT_H), Image.BICUBIC), np.float32) / 255
    n2 = np.asarray(Image.fromarray(rng.normal(128, 60, (BT_H // 6, BT_W // 6)).clip(0, 255).astype(np.uint8)).resize((BT_W, BT_H), Image.BICUBIC), np.float32) / 255
    base = np.array([96, 112, 62], np.float32) * (0.75 + 0.35 * n1[..., None]) + (n2[..., None] - 0.5) * 30
    base += np.array([30, 10, -10]) * np.clip(n1 - 0.6, 0, 1)[..., None] * 2          # muddy patches
    im = Image.fromarray(base.clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    P = _plan(); river = [(x + BT_OFF[0], y + BT_OFF[1]) for x, y in P.BATTLE_RIVER]
    river = [(river[0][0] + 300, river[0][1] - 1600)] + river + [(river[-1][0] - 300, river[-1][1] + 1600)]
    for _ in range(260):                                                            # tree clumps and field strips
        x, y = rng.random() * BT_W, rng.random() * BT_H; r = 18 + rng.random() * 40
        d.ellipse([x - r + 14, y - r * 0.6 + 18, x + r + 14, y + r * 0.6 + 18], fill=(48, 58, 34))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(52 + int(rng.random() * 20), 78 + int(rng.random() * 25), 40))
    for _ in range(60):
        x, y = rng.random() * BT_W, rng.random() * BT_H; w_, h_ = 200 + rng.random() * 300, 120 + rng.random() * 200
        d.rectangle([x, y, x + w_, y + h_], outline=(120, 120, 72), width=4)
    d.line(river, fill=(70, 80, 60), width=300, joint='curve')                        # wet banks
    d.line(river, fill=(48, 86, 110), width=210, joint='curve')
    d.line(river, fill=(64, 112, 140), width=120, joint='curve')
    for isl in getattr(P, 'BATTLE_ISLANDS', []): d.ellipse([isl[0] + BT_OFF[0], isl[1] + BT_OFF[1], isl[2] + BT_OFF[0], isl[3] + BT_OFF[1]], fill=(92, 104, 60), outline=(70, 80, 50), width=8)
    im = im.filter(ImageFilter.GaussianBlur(2)).filter(ImageFilter.UnsharpMask(4, 60, 2))
    return im

class TexCam(Cam):
    pass

def draw_battle(sp, t, dur):
    k = ease(t / dur)
    (x0, y0, w0) = sp.get('view', (2000, 1300, 3600)); (x1, y1, w1) = sp.get('view1', sp.get('view', (2000, 1300, 3600)))
    cx, cy = lerp(x0, x1, k), lerp(y0, y1, k); w = math.exp(lerp(math.log(w0), math.log(w1), k))
    pitch = lerp(sp.get('pitch', 50), sp.get('pitch1', sp.get('pitch', 50)), k)
    yaw = lerp(sp.get('yaw0', -4.0), sp.get('yaw1', 4.0), t / dur)
    cam = Cam(cx + BT_OFF[0], cy + BT_OFF[1], w, pitch, yaw)
    _proj = cam.proj; cam.proj = lambda X, Y, Z=0.0: _proj(X + BT_OFF[0], Y + BT_OFF[1], Z)
    Hl = np.linalg.inv(cam.Hs); Hl = Hl / Hl[2, 2]
    co = (Hl[0, 0], Hl[0, 1], Hl[0, 2], Hl[1, 0], Hl[1, 1], Hl[1, 2], Hl[2, 0], Hl[2, 1])
    img = battle_tex().transform((W, H), Image.PERSPECTIVE, co, resample=Image.BICUBIC, fillcolor=(70, 84, 52))
    a = np.asarray(img, np.float32); hz = haze_mask()
    a = a * (1 - hz) + np.array([150, 160, 165], np.float32) * hz
    out = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(out)
    COL = {'greek': (60, 110, 220), 'indian': (230, 120, 30), 'gray': (120, 120, 120)}
    for un in sorted(sp.get('units', []), key=lambda u: -u.get('xy0', (0, 0))[1]):
        at = un.get('at', 0.0); al = ease((t - at) / 0.5)
        if al <= 0: continue
        if 'off' in un: al *= 1 - ease((t - un['off']) / 0.6)
        if al <= 0: continue
        m = ease((t - un.get('mv', at)) / un.get('dur', 2.0)) if 'xy1' in un else 0.0
        (ax, ay) = un['xy0']; (bx, by) = un.get('xy1', un['xy0'])
        ux, uy = lerp(ax, bx, m), lerp(ay, by, m)
        uw, uh = un.get('w', 260), un.get('h', 80)
        col = COL[un['side']]; hgt = un.get('z', 18)
        corners = [(ux - uw / 2, uy - uh / 2), (ux + uw / 2, uy - uh / 2), (ux + uw / 2, uy + uh / 2), (ux - uw / 2, uy + uh / 2)]
        shp = [tuple(cam.proj(px + hgt * 0.8, py + hgt * 0.6, 0)[:2]) for px, py in corners]
        sh = Image.new('RGBA', out.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).polygon(shp, fill=(0, 0, 0, int(110 * al)))
        out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6 * U))); d = ImageDraw.Draw(out)
        for j, zz in enumerate((0, hgt * 0.5, hgt)):
            pts = [tuple(cam.proj(px, py, zz)[:2]) for px, py in corners]
            shade = (0.5, 0.7, 1.0)[j]
            d.polygon(pts, fill=tuple(int(c * shade) for c in col) + (int(240 * al),), outline=(250, 245, 235, int(220 * al)) if j == 2 else None)
        top = [cam.proj(px, py, hgt)[:2] for px, py in corners]
        kind = un.get('kind', 'inf')
        if kind == 'inf':                                  # rows of spear ticks
            for r in range(3):
                v = (r + 1) / 4
                p0 = (top[0][0] + (top[3][0] - top[0][0]) * v, top[0][1] + (top[3][1] - top[0][1]) * v)
                p1 = (top[1][0] + (top[2][0] - top[1][0]) * v, top[1][1] + (top[2][1] - top[1][1]) * v)
                for s in np.linspace(0.06, 0.94, 12):
                    x = p0[0] + (p1[0] - p0[0]) * s; y = p0[1] + (p1[1] - p0[1]) * s
                    d.line([(x, y), (x, y - 14 * U)], fill=(240, 235, 220, int(230 * al)), width=max(1, int(2 * U)))
        elif kind == 'cav':                                # chevrons
            cxs = sum(p[0] for p in top) / 4; cys = sum(p[1] for p in top) / 4
            for dx in (-40, 0, 40):
                d.line([(cxs + dx * U - 14 * U, cys - 8 * U), (cxs + dx * U, cys + 6 * U), (cxs + dx * U + 14 * U, cys - 8 * U)], fill=(250, 245, 235, int(240 * al)), width=int(4 * U))
        if kind in ('eleph', 'chariot', 'boat'):
            n = un.get('n', 3); ic = {'eleph': 'elephant', 'chariot': 'chariot', 'boat': 'boat'}[kind]
            for s in np.linspace(0.18, 0.82, n):
                x = top[0][0] + (top[1][0] - top[0][0]) * s; y = (top[0][1] + top[3][1]) / 2 + (top[1][1] - top[0][1]) * s
                im = ICONS[ic](int(un.get('size', 26) * U))
                im.putalpha(im.getchannel('A').point(lambda v: int(v * al)))
                out.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2 - 10 * U)))
            d = ImageDraw.Draw(out)
        if un.get('label'):
            tx, ty, _ = cam.proj(ux, uy - uh / 2, hgt + 40)
            ti = text_img(un['label'], 'bold', un.get('ls', 40), fill=(255, 250, 240), stroke=3)
            ti.putalpha(ti.getchannel('A').point(lambda v: int(v * al)))
            out.alpha_composite(ti, (int(tx - ti.width / 2), int(ty - ti.height)))
            d = ImageDraw.Draw(out)
    for ar in sp.get('barrows', []):                      # (x0, y0, x1, y1, side, at[, dur]) arrows on the ground
        bx0, by0, bx1, by1, side, at = ar[:6]; dd = ar[6] if len(ar) > 6 else 1.4
        p = ease((t - at) / dd)
        if p <= 0: continue
        L = math.hypot(bx1 - bx0, by1 - by0)
        pts = [cam.proj(bx0 + (bx1 - bx0) * u, by0 + (by1 - by0) * u, 0.12 * L * math.sin(math.pi * u))[:2] for u in np.linspace(0, p, 30)]
        c = COL[side] + (255,)
        d.line(pts, fill=(15, 12, 10, 210), width=int(22 * U), joint='curve'); d.line(pts, fill=c, width=int(13 * U), joint='curve')
        (xa, ya), (xb, yb) = pts[-2], pts[-1]; ang = math.atan2(yb - ya, xb - xa); Lh = 34 * U
        d.polygon([(xb + math.cos(ang) * Lh * 0.6, yb + math.sin(ang) * Lh * 0.6), (xb + math.cos(ang + 2.5) * Lh, yb + math.sin(ang + 2.5) * Lh), (xb + math.cos(ang - 2.5) * Lh, yb + math.sin(ang - 2.5) * Lh)], fill=c, outline=(15, 12, 10, 230))
    for lab in sp.get('blabels', []):                     # (text, x, y, at, size)
        txt, lx, ly, at = lab[:4]; size = lab[4] if len(lab) > 4 else 52
        a_ = ease((t - at) / 0.6)
        if a_ <= 0: continue
        x, y, _ = cam.proj(lx, ly, 0)
        ti = text_img(txt, 'bold', size, fill=lab[5] if len(lab) > 5 else (255, 250, 240), stroke=3); ti.putalpha(ti.getchannel('A').point(lambda v: int(v * a_)))
        out.alpha_composite(ti, (int(x - ti.width / 2), int(y - ti.height / 2)))
    return out.convert('RGB')

# --- weather overlays
def rain_layer(t, a, dens=1.0):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); r = np.random.default_rng(5)
    n = int(420 * dens)
    xs = r.random(n) * (W + 400) - 200; sp_ = 1400 + r.random(n) * 900; ph = r.random(n) * H; ln = (30 + r.random(n) * 50) * U
    for i in range(n):
        y = (ph[i] + t * sp_[i] * U) % (H + 200) - 100; x = xs[i] - (y * 0.18)
        d.line([(x, y), (x - ln[i] * 0.18, y + ln[i])], fill=(200, 215, 235, int(110 * a)), width=max(1, int(2 * U)))
    return lay

def lightning_alpha(t, at):
    dt = t - at
    if dt < 0 or dt > 0.9: return 0.0
    return max(math.exp(-dt * 14), 0.75 * math.exp(-max(0, dt - 0.18) * 9) * (dt > 0.18))

def draw_map(sp, t, dur):
    if sp.get('ground') == 'battle': return draw_battle(sp, t, dur)
    k = ease(t / dur)
    (la0, lo0, w0) = sp.get('view', (24, 80, 40)); (la1, lo1, w1) = sp.get('view1', sp.get('view', (24, 80, 40)))
    x0, y0 = ll(la0, lo0); x1, y1 = ll(la1, lo1)
    cx, cy = lerp(x0, x1, k), lerp(y0, y1, k)
    w = math.exp(lerp(math.log(w0), math.log(w1), k)) * MJ['pxd']
    pitch = lerp(sp.get('pitch', 48), sp.get('pitch1', sp.get('pitch', 48)), k)
    yaw = lerp(sp.get('yaw0', -5.0), sp.get('yaw1', 5.0), t / dur)        # slow linear orbit
    cam = Cam(cx, cy, w, pitch, yaw)
    out = ground(cam, sp.get('noborders', False))
    H3 = w * 0.014                                                        # block height (ground px) scales with the view
    for f in sp.get('fill', []):                                          # raised country blocks
        g, col = f[0], f[1]; at = f[2] if len(f) > 2 and f[2] is not None else -9
        a = ease((t - at) / 0.8)
        if len(f) > 3 and f[3] is not None: a *= 1 - ease((t - f[3]) / 0.8)
        if a <= 0: continue
        rs = custom_rings(g) or [np.array([ll(la, lo) for lo, la in r]) for n in GROUP[g] for r in countries().get(n, [])]
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
    draw_rivers(out, cam, sp, t, w)
    if sp.get('india_outline'):                                            # India's official boundary of J&K and Ladakh (dashed)
        jk = [(32.5, 74.0), (33.0, 73.6), (33.9, 73.4), (34.4, 72.8), (35.1, 72.0), (35.9, 71.6), (36.8, 72.4), (37.1, 74.6), (36.5, 76.0),
              (35.9, 77.6), (35.6, 78.3), (35.7, 79.3), (35.3, 80.3), (34.3, 80.1), (33.4, 79.5), (32.6, 78.9)]
        pts = cam.proj_many([ll(la, lo) for la, lo in jk]); dd = ImageDraw.Draw(out)
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            L = math.hypot(xb - xa, yb - ya); n = max(1, int(L / (26 * U)))
            for k in range(0, n, 2):
                u0, u1 = k / n, min(1, (k + 1) / n)
                dd.line([(xa + (xb - xa) * u0, ya + (yb - ya) * u0), (xa + (xb - xa) * u1, ya + (yb - ya) * u1)], fill=(255, 150, 40, 235), width=int(5 * U))
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
        d.line(shp, fill=(0, 0, 0, 45), width=int(5 * U), joint='curve')                 # ground shadow
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

# ------------------------------------------------------------------ modern card backgrounds (BG_STYLE env)
#   navy      deep navy gradient, soft bokeh lights, faint news-grid lines
#   cinema    teal-and-amber cinematic gradient with slow light rays and floating dust
#   dotmap    dark slate with a dotted map of Asia (India highlighted) and a soft spotlight
#   aurora    dark mesh-gradient of glowing colour blobs (blue / violet / amber), glassy
#   desh      near-black with saffron and green glows in the corners and fine diagonal lines
# Each is built once on a canvas 12% larger than the frame and drifts slowly (pan + breathing light) every frame.
# 'red' cards get a crimson tint, 'paper' cards a warm tint, so tone changes still read.
BG_STYLE = os.environ.get('BG_STYLE', 'dotmap')
FILES_STYLE = os.environ.get('FILES_STYLE', 'modern')
BG_PAD = 1.12
TONE_TINT = {'dark': None, 'red': (150, 20, 25), 'paper': (150, 110, 60)}

def _soft_blobs(w, h, blobs, seed=0):
    yy_, xx_ = np.mgrid[0:h, 0:w].astype(np.float32); a = np.zeros((h, w, 3), np.float32)
    for (cx, cy, r, col, k) in blobs:
        d2 = ((xx_ / w - cx) ** 2 + (yy_ / h - cy) ** 2) / (r * r)
        a += np.exp(-d2)[..., None] * np.array(col, np.float32) * k
    return a

@lru_cache(8)
def bg_canvas(style, tone):
    w, h = int(W * BG_PAD), int(H * BG_PAD); yy_, xx_ = np.mgrid[0:h, 0:w].astype(np.float32); rng = np.random.default_rng(21)
    if style == 'navy':
        a = np.array([8, 14, 32], np.float32) + _soft_blobs(w, h, [(0.3, 0.35, 0.55, (30, 60, 130), 1.0), (0.8, 0.75, 0.5, (20, 40, 100), 0.8)])
        grid = ((np.abs(((xx_ / (W / 24)) % 1) - 0.5) > 0.48) | (np.abs(((yy_ / (W / 24)) % 1) - 0.5) > 0.48)).astype(np.float32)
        a += grid[..., None] * np.array([40, 70, 120]) * 0.10
        im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA'); d = ImageDraw.Draw(im)
        for _ in range(40):
            x, y, r = rng.random() * w, rng.random() * h, (10 + rng.random() * 60) * U
            d.ellipse([x - r, y - r, x + r, y + r], fill=(120, 170, 255, int(20 + rng.random() * 40)))
        im = Image.alpha_composite(Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA'), im.filter(ImageFilter.GaussianBlur(10 * U)))
    elif style == 'cinema':
        t_ = np.clip(xx_ / w * 0.8 + yy_ / h * 0.4, 0, 1)[..., None]
        a = np.array([6, 30, 36], np.float32) * (1 - t_) + np.array([60, 32, 10], np.float32) * t_
        a += _soft_blobs(w, h, [(0.85, 0.15, 0.35, (255, 170, 80), 0.35), (0.1, 0.9, 0.45, (20, 120, 130), 0.4)])
        ang = np.arctan2(yy_ - h * -0.1, xx_ - w * 0.85); rays = (np.sin(ang * 22) * 0.5 + 0.5) ** 8
        a += (rays * np.clip(1 - np.sqrt(((xx_ - w * 0.85) / w) ** 2 + ((yy_ + h * 0.1) / h) ** 2), 0, 1))[..., None] * np.array([255, 200, 140]) * 0.12
        im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')
    elif style == 'dotmap':
        a = np.array([14, 17, 22], np.float32) + _soft_blobs(w, h, [(0.62, 0.45, 0.45, (60, 70, 90), 0.8)])
        im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA'); d = ImageDraw.Draw(im)
        land = Image.new('L', (w, h), 0); dl = ImageDraw.Draw(land); ind = Image.new('L', (w, h), 0); di = ImageDraw.Draw(ind)
        def pr(lat, lon): return (lon - 40) / 80 * w * 0.95 + w * 0.15, (45 - lat) / 50 * h * 0.95 + h * 0.03
        for n, rs in countries().items():
            for r in rs:
                pts = [pr(la, lo) for lo, la in r]
                if max(p[0] for p in pts) < 0 or min(p[0] for p in pts) > w: continue
                dl.polygon(pts, fill=255)
                if n == 'India': di.polygon(pts, fill=255)
        jk = [(32.5, 74.0), (33.0, 73.6), (33.9, 73.4), (34.4, 72.8), (35.1, 72.0), (35.9, 71.6), (36.8, 72.4), (37.1, 74.6), (36.5, 76.0),
              (35.9, 77.6), (35.6, 78.3), (35.7, 79.3), (35.3, 80.3), (34.3, 80.1), (33.4, 79.5), (32.6, 78.9), (32.8, 77.0), (32.3, 75.6)]
        di.polygon([pr(la, lo) for la, lo in jk], fill=255); dl.polygon([pr(la, lo) for la, lo in jk], fill=255)   # India's official map of J&K and Ladakh
        L = np.asarray(land); I = np.asarray(ind); step = int(16 * U); r = 3.2 * U
        for y in range(step // 2, h, step):
            for x in range(step // 2, w, step):
                if L[y, x]:
                    col = (240, 180, 60, 230) if I[y, x] else (110, 125, 150, 150)
                    d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    elif style == 'aurora':
        a = np.array([6, 6, 14], np.float32) + _soft_blobs(w, h, [(0.2, 0.25, 0.35, (40, 80, 220), 0.9), (0.75, 0.3, 0.32, (140, 50, 200), 0.8),
                                                                (0.55, 0.85, 0.38, (230, 140, 40), 0.55), (0.95, 0.85, 0.3, (30, 160, 180), 0.5)])
        im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(30 * U)).convert('RGBA')
    else:  # desh
        a = np.array([10, 10, 12], np.float32) + _soft_blobs(w, h, [(0.0, 0.0, 0.45, (255, 120, 20), 0.55), (1.0, 1.0, 0.45, (20, 140, 60), 0.55),
                                                                 (0.5, 0.5, 0.5, (40, 40, 60), 0.5)])
        lines = (((xx_ + yy_) / (22 * U)) % 1 < 0.06).astype(np.float32)
        a += lines[..., None] * np.array([255, 255, 255]) * 0.025
        im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')
    n = _noise(w, h, 31, 2)                                                  # fine grain so gradients never band
    g = np.asarray(im.convert('RGB'), np.float32) + (n[..., None] - 0.5) * 10
    tint = TONE_TINT.get(tone)
    if tint is not None:
        lum = g.mean(axis=2, keepdims=True) / 255; g = g * 0.55 + np.array(tint, np.float32) * (0.25 + lum) * 0.75
    v = np.sqrt(((xx_ / w - 0.5) / 0.6) ** 2 + ((yy_ / h - 0.5) / 0.6) ** 2); g *= (1 - 0.45 * np.clip(v - 0.55, 0, 1))[..., None]
    return Image.fromarray(g.clip(0, 255).astype(np.uint8))

def card_bg_modern(tone, t, seed=0):
    big = bg_canvas(BG_STYLE, tone)
    mx, my = big.width - W, big.height - H
    ph = seed * 1.7
    x = int(mx * (0.5 + 0.45 * math.sin(t * 0.06 + ph))); y = int(my * (0.5 + 0.45 * math.cos(t * 0.05 + ph)))
    im = big.crop((x, y, x + W, y + H))
    k = 1.0 + 0.04 * math.sin(t * 0.8 + ph)                                  # breathing light
    return ImageEnhance.Brightness(im).enhance(k)

# vintage 1960s wall clock: wooden case, brass bezel, aged cream dial with Roman numerals, spade hands, ticking red
# second hand, glass glare, warm lamp light on a dark wall. Drawn at 2x and downsampled for smooth edges.
CLK_R = 300
@lru_cache(2)
def clock_static():
    S2 = 2; R = int(CLK_R * U * S2); size = int(R * 2.7); c = size / 2
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    yy_, xx_ = np.mgrid[0:size, 0:size].astype(np.float32); r = np.sqrt((xx_ - c) ** 2 + (yy_ - c) ** 2) / R
    ang = np.arctan2(yy_ - c, xx_ - c)
    light = (0.75 + 0.25 * np.cos(ang + 2.3))                                    # light from the top-left
    def ring(r0, r1, col, shade=True, tex=0.0):
        m = (r >= r0) & (r < r1)
        a = np.zeros((size, size, 4), np.float32); col = np.array(col, np.float32)
        k = light if shade else 1.0
        if tex:
            grain = np.sin(xx_ * 0.05 + np.sin(yy_ * 0.013) * 6) * tex
            k = k * (1 + grain)
        a[..., :3] = col * (k[..., None] if isinstance(k, np.ndarray) else k)
        a[..., 3] = m * 255
        lay = Image.fromarray(a.clip(0, 255).astype(np.uint8), 'RGBA'); im.alpha_composite(lay)
    ring(1.13, 1.30, (92, 52, 26), tex=0.08)                                     # wooden case
    ring(1.11, 1.13, (40, 22, 10), shade=False)
    ring(1.02, 1.11, (196, 150, 70))                                             # brass bezel
    bev = np.clip(1 - np.abs(r - 1.065) / 0.045, 0, 1) * (0.5 + 0.5 * np.cos(ang + 2.3))
    hl = np.zeros((size, size, 4), np.float32); hl[..., :3] = 255; hl[..., 3] = bev * 120 * ((r > 1.02) & (r < 1.11))
    im.alpha_composite(Image.fromarray(hl.astype(np.uint8), 'RGBA'))
    dial = np.zeros((size, size, 4), np.float32)                                 # aged cream dial
    rng = np.random.default_rng(4); n = np.asarray(Image.fromarray(rng.normal(128, 50, (size // 8, size // 8)).clip(0, 255).astype(np.uint8)).resize((size, size), Image.BICUBIC), np.float32) / 255
    base = np.array([236, 224, 196], np.float32) * (0.92 + 0.1 * n[..., None]) * (1 - 0.18 * np.clip(r - 0.6, 0, 1)[..., None])
    dial[..., :3] = base; dial[..., 3] = (r < 1.02) * 255
    im.alpha_composite(Image.fromarray(dial.clip(0, 255).astype(np.uint8), 'RGBA'))
    d = ImageDraw.Draw(im)
    for rr, wd in ((0.97, 3), (0.88, 2)): d.ellipse([c - rr * R, c - rr * R, c + rr * R, c + rr * R], outline=(60, 40, 25), width=int(wd * S2 * U))
    for i in range(60):                                                          # minute track
        a_ = math.radians(i * 6); r0 = 0.88 if i % 5 == 0 else 0.905
        d.line([c + math.sin(a_) * r0 * R, c - math.cos(a_) * r0 * R, c + math.sin(a_) * 0.97 * R, c - math.cos(a_) * 0.97 * R], fill=(45, 30, 20), width=int((5 if i % 5 == 0 else 2) * S2 * U))
    f = ImageFont.truetype(os.path.join(ASSETS, 'fonts', FONTS['serif']), int(R * 0.15))
    for i, num in enumerate(['XII', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI']):
        a_ = math.radians(i * 30); x, y = c + math.sin(a_) * 0.72 * R, c - math.cos(a_) * 0.72 * R
        d.text((x, y), num, font=f, fill=(35, 25, 18), anchor='mm')
    f2 = ImageFont.truetype(os.path.join(ASSETS, 'fonts', FONTS['serif']), int(R * 0.07))
    d.text((c, c + 0.36 * R), 'ताशकंद', font=f2, fill=(90, 70, 50), anchor='mm')
    return im.resize((size // S2, size // S2), Image.LANCZOS), R / S2

@lru_cache(1)
def clock_wall():
    yy_, xx_ = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx_ - W * 0.5) / (W * 0.55)) ** 2 + ((yy_ - H * 0.42) / (H * 0.75)) ** 2)
    k = np.clip(1.1 - r, 0.12, 1)[..., None]
    rng = np.random.default_rng(9); n = np.asarray(Image.fromarray(rng.normal(128, 40, (H // 3, W // 3)).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32)[..., None] / 255
    stripes = (np.sin(xx_ / (W / 34) * math.pi) * 0.03)[..., None]                # old wallpaper stripes
    a = np.array([72, 58, 44], np.float32) * k * (0.9 + 0.2 * n + stripes)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')

def draw_clock(img, t, sp):
    face, R = clock_static(); cx, cy = W * 0.5, H * 0.47
    wall = clock_wall().copy()
    sh = Image.new('RGBA', face.size, (0, 0, 0, 0)); sh.putalpha(face.getchannel('A').filter(ImageFilter.GaussianBlur(22 * U)).point(lambda v: int(v * 0.75)))
    wall.alpha_composite(sh, (int(cx - face.width / 2 + 26 * U), int(cy - face.height / 2 + 34 * U)))
    wall.alpha_composite(face, (int(cx - face.width / 2), int(cy - face.height / 2)))
    S2 = 2; hs = Image.new('RGBA', (face.width * S2, face.height * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(hs); c = hs.width / 2; RR = R * S2
    sec_f = sp.get('sec0', 50) + t
    tick = math.floor(sec_f) + min(1.0, (sec_f % 1) / 0.12) + 0.06 * math.sin(min(1, (sec_f % 1) / 0.25) * math.pi) * (sec_f % 1 < 0.25)
    h0, m0 = sp.get('hm', (11, 59)); mins = m0 + tick / 60; hrs = h0 + mins / 60
    def hand(angle, L, wd, tail=0.12, col=(18, 14, 12), spade=False):
        a_ = math.radians(angle); s, co = math.sin(a_), math.cos(a_)
        px, py = -co, -s                                           # perpendicular
        tip = (c + s * L * RR, c - co * L * RR); back = (c - s * tail * RR, c + co * tail * RR)
        w_ = wd * S2 * U
        d.polygon([(back[0] + px * w_, back[1] + py * w_), (tip[0] + px * w_ * 0.25, tip[1] + py * w_ * 0.25), tip,
                   (tip[0] - px * w_ * 0.25, tip[1] - py * w_ * 0.25), (back[0] - px * w_, back[1] - py * w_)], fill=col)
        if spade:
            sx, sy = c + s * L * 0.78 * RR, c - co * L * 0.78 * RR; rs = w_ * 2.4
            d.ellipse([sx - rs, sy - rs, sx + rs, sy + rs], fill=col)
    shadow_off = 8 * S2 * U
    hs_sh = Image.new('RGBA', hs.size, (0, 0, 0, 0)); d_sh = d
    d = ImageDraw.Draw(hs_sh)
    hand(hrs * 30, 0.50, 9, spade=True, col=(0, 0, 0)); hand(mins * 6, 0.80, 6, spade=True, col=(0, 0, 0))
    hs_sh = hs_sh.filter(ImageFilter.GaussianBlur(5 * S2 * U)); hs_sh.putalpha(hs_sh.getchannel('A').point(lambda v: int(v * 0.45)))
    hs.alpha_composite(hs_sh, (int(shadow_off), int(shadow_off)))
    d = ImageDraw.Draw(hs)
    hand(hrs * 30, 0.50, 9, spade=True); hand(mins * 6, 0.80, 6, spade=True)
    hand((tick % 60) * 6, 0.88, 2.2, tail=0.22, col=(180, 28, 22))
    d.ellipse([c - 16 * S2 * U, c - 16 * S2 * U, c + 16 * S2 * U, c + 16 * S2 * U], fill=(180, 140, 60), outline=(40, 25, 10), width=int(3 * S2 * U))
    hs = hs.resize(face.size, Image.LANCZOS)
    wall.alpha_composite(hs, (int(cx - face.width / 2), int(cy - face.height / 2)))
    gl = Image.new('L', face.size, 0); ImageDraw.Draw(gl).pieslice([face.width * 0.2, face.height * 0.18, face.width * 0.8, face.height * 0.62], 200, 300, fill=70)
    gl = gl.filter(ImageFilter.GaussianBlur(30 * U)); glare = Image.new('RGBA', face.size, (255, 255, 255, 0)); glare.putalpha(gl)
    wall.alpha_composite(glare, (int(cx - face.width / 2), int(cy - face.height / 2)))
    img.paste(wall.convert('RGB'))

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

# ------------------------------------------------------------------ document card styles (DOC_STYLE env or sp['docstyle'])
#   classic   aged paper (original)
#   govfile   Indian government file sheet: header, file number, margin line, ruled lines, punch holes, paper clip, coffee stain
#   dossier   manila folder with the page inside, photo clipped on, red "गोपनीय" band, redaction bars
#   telegram  yellow 1960s telegram form with the text on pasted strips
#   modern    dark glass panel, gold accent bar, document icon, white text with bullets, badge instead of a stamp
#   evidence  corkboard: notebook page pinned with a red pushpin and tape, red string to a small note
DOC_STYLE = os.environ.get('DOC_STYLE', 'headline')

def _typed(txt, at, t):
    return txt[:max(1, int(len(txt) * min(1, (t - at) / 0.9)))] if t >= at else None

@lru_cache(8)
def _noise(w, h, seed, scale=6):
    rng = np.random.default_rng(seed)
    return np.asarray(Image.fromarray(rng.normal(128, 50, (max(2, h // scale), max(2, w // scale))).clip(0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255

def _page(w, h, col, seed=1, vign=0.25, grain=0.18):
    n = _noise(w, h, seed); a = np.ones((h, w, 3), np.float32) * np.array(col, np.float32) + (n[..., None] - 0.5) * 255 * grain
    y, x = np.mgrid[0:h, 0:w].astype(np.float32); r = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2)
    a *= (1 - vign * np.clip(r - 0.7, 0, 1))[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')

def _shadowed(full, pg, x0, y0, blur=20, alpha=200, off=(10, 16)):
    sh = Image.new('RGBA', (pg.width + 80, pg.height + 80), (0, 0, 0, 0))
    m = Image.new('L', sh.size, 0); m.paste(pg.getchannel('A').point(lambda v: alpha if v > 10 else 0), (40, 40))
    sh.putalpha(m.filter(ImageFilter.GaussianBlur(blur * U)))
    full.alpha_composite(sh, (x0 - 40 + int(off[0] * U), y0 - 40 + int(off[1] * U))); full.alpha_composite(pg, (x0, y0))

def _paperclip(d, x, y, s):
    for k, wd in ((0, 7), (0, 3)):
        col = (110, 115, 125, 255) if wd == 7 else (200, 205, 215, 255)
        d.rounded_rectangle([x, y, x + 34 * s, y + 120 * s], radius=int(17 * s), outline=col, width=int(wd * s))
        d.rounded_rectangle([x + 9 * s, y + 18 * s, x + 25 * s, y + 98 * s], radius=int(8 * s), outline=col, width=int(wd * s))

def doc_govfile(doc, t, pw, ph):
    pg = _page(pw, ph, (232, 222, 192), seed=2); d = ImageDraw.Draw(pg)
    for i in range(14):                                                     # faint ruled lines
        y = int((250 + i * 46) * U)
        if y < ph - 40 * U: d.line([int(60 * U), y, pw - int(50 * U), y], fill=(150, 170, 190, 90), width=max(1, int(2 * U)))
    d.line([int(150 * U), int(120 * U), int(150 * U), ph - int(20 * U)], fill=(200, 80, 80, 160), width=int(3 * U))   # margin
    for yy in (0.3, 0.7): d.ellipse([int(50 * U), int(ph * yy - 14 * U), int(78 * U), int(ph * yy + 14 * U)], fill=(70, 60, 50, 255))
    d.rectangle([0, 0, pw, int(100 * U)], fill=(214, 200, 165, 255)); d.line([0, int(100 * U), pw, int(100 * U)], fill=(120, 95, 60, 255), width=int(3 * U))
    hdr = text_img('भारत सरकार', 'bold', 36, fill=(70, 45, 25), shadow=False); pg.alpha_composite(hdr, (int(170 * U), int(14 * U)))
    fno = text_img('फ़ाइल सं. 2(67)/66', 'med', 30, fill=(90, 60, 35), shadow=False); pg.alpha_composite(fno, (pw - fno.width - int(40 * U), int(18 * U)))
    ti = text_img(doc['title'], 'bold', 54, fill=(25, 30, 60), shadow=False); pg.alpha_composite(ti, (int(175 * U), int(115 * U)))
    y = int(236 * U)
    for txt, at in doc['lines']:
        s = _typed(txt, at, t)
        if s: li = text_img(s, 'serif', 46, fill=(28, 32, 70), shadow=False); pg.alpha_composite(li, (int(175 * U), y - int(40 * U)))
        y += int(92 * U)
    st = Image.new('RGBA', (pw, ph), (0, 0, 0, 0)); ds = ImageDraw.Draw(st)        # coffee ring
    cx, cy, r = pw * 0.86, ph * 0.3, 85 * U
    ds.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(150, 100, 50, 70), width=int(10 * U))
    pg.alpha_composite(st.filter(ImageFilter.GaussianBlur(3 * U)))
    _paperclip(ImageDraw.Draw(pg), int(pw * 0.06), -int(30 * U), U)
    return pg, (0.74, 0.82)

def doc_dossier(doc, t, pw, ph):
    fw, fh = int(pw * 1.08), int(ph * 1.12)
    folder = _page(fw, fh, (205, 160, 92), seed=3, vign=0.35)
    fo = Image.new('RGBA', (fw, fh + int(60 * U)), (0, 0, 0, 0)); fo.alpha_composite(folder, (0, int(60 * U)))
    ImageDraw.Draw(fo).rounded_rectangle([int(40 * U), 0, int(380 * U), int(90 * U)], radius=int(16 * U), fill=(198, 152, 86, 255))
    tab = text_img('गोपनीय फ़ाइल', 'bold', 34, fill=(90, 50, 20), shadow=False); fo.alpha_composite(tab, (int(70 * U), int(4 * U)))
    pg = _page(pw, ph, (240, 234, 218), seed=4, vign=0.15, grain=0.1); d = ImageDraw.Draw(pg)
    ti = text_img(doc['title'], 'bold', 54, fill=(30, 25, 20), shadow=False); pg.alpha_composite(ti, (int(60 * U), int(40 * U)))
    d.line([int(60 * U), int(145 * U), pw - int(300 * U), int(145 * U)], fill=(30, 25, 20, 255), width=int(3 * U))
    y = int(170 * U)
    for txt, at in doc['lines']:
        s = _typed(txt, at, t)
        if s: li = text_img(s, 'serif', 44, fill=(25, 22, 20), shadow=False); pg.alpha_composite(li, (int(60 * U), y))
        y += int(84 * U)
    rng = np.random.default_rng(7)                                          # redaction bars
    for i in range(3):
        yy = y + int(i * 46 * U) + int(10 * U)
        if yy < ph - 60 * U: d.rectangle([int(60 * U), yy, int(60 * U + (300 + rng.random() * 500) * U), yy + int(26 * U)], fill=(15, 15, 15, 255))
    try:                                                                    # clipped photo
        ph_im = Image.open(os.path.join(ASSETS, 'photos_hd', 'shastri_kbr.jpg')).convert('L')
        ph_im = ph_im.crop((int(ph_im.width * 0.42), int(ph_im.height * 0.0), int(ph_im.width * 0.95), int(ph_im.height * 0.45)))
        pw2 = int(230 * U); ph_im = ImageOps.fit(ph_im, (pw2, int(pw2 * 1.2))).convert('RGBA')
        card = Image.new('RGBA', (pw2 + int(24 * U), int(pw2 * 1.2) + int(24 * U)), (250, 248, 240, 255)); card.alpha_composite(ph_im, (int(12 * U), int(12 * U)))
        card = card.rotate(4, expand=True, resample=Image.BICUBIC)
        pg.alpha_composite(card, (pw - card.width - int(40 * U), int(30 * U)))
        _paperclip(ImageDraw.Draw(pg), pw - int(150 * U), int(5 * U), U * 0.9)
    except Exception:
        pass
    band = Image.new('RGBA', (int(560 * U), int(70 * U)), (200, 25, 25, 230))
    bt = text_img('गोपनीय', 'bold', 44, fill=(255, 245, 235), shadow=False); band.alpha_composite(bt, ((band.width - bt.width) // 2, int(-6 * U)))
    band = band.rotate(-28, expand=True, resample=Image.BICUBIC)
    pg.alpha_composite(band, (pw - band.width + int(60 * U), ph - band.height + int(20 * U)))
    fo.alpha_composite(pg, (int((fw - pw) / 2) + int(20 * U), int(60 * U) + int((fh - ph) / 2)))
    return fo, (0.3, 0.8)

def doc_telegram(doc, t, pw, ph):
    pg = _page(pw, ph, (238, 214, 140), seed=5, vign=0.3, grain=0.14); d = ImageDraw.Draw(pg)
    d.rectangle([int(24 * U), int(24 * U), pw - int(24 * U), ph - int(24 * U)], outline=(110, 70, 20, 255), width=int(4 * U))
    hdr = text_img('तार  •  TELEGRAM', 'bold', 52, fill=(110, 50, 20), shadow=False); pg.alpha_composite(hdr, ((pw - hdr.width) // 2, int(36 * U)))
    for i, lab in enumerate(['प्रेषक', 'तारीख़', 'स्थान']):
        x = int((60 + i * 360) * U); d.rectangle([x, int(130 * U), x + int(330 * U), int(190 * U)], outline=(110, 70, 20, 255), width=int(2 * U))
        lt = text_img(lab, 'med', 26, fill=(110, 70, 20), shadow=False); pg.alpha_composite(lt, (x + int(8 * U), int(128 * U)))
    strip_y = int(230 * U)
    ti = text_img(doc['title'], 'bold', 46, fill=(20, 20, 20), shadow=False)
    strip = Image.new('RGBA', (ti.width + int(30 * U), ti.height - int(16 * U)), (250, 250, 245, 255)); strip.alpha_composite(ti, (int(15 * U), int(-8 * U)))
    pg.alpha_composite(strip, (int(60 * U), strip_y)); strip_y += strip.height + int(24 * U)
    for txt, at in doc['lines']:
        s = _typed(txt, at, t)
        if s:
            li = text_img(s, 'bold', 42, fill=(25, 25, 25), shadow=False)
            strip = Image.new('RGBA', (li.width + int(30 * U), li.height - int(16 * U)), (250, 250, 245, 255)); strip.alpha_composite(li, (int(15 * U), int(-8 * U)))
            pg.alpha_composite(strip, (int(60 * U), strip_y))
        strip_y += int(86 * U)
    return pg, (0.75, 0.8)

def doc_modern(doc, t, pw, ph, bg=None):
    pg = Image.new('RGBA', (pw, ph), (0, 0, 0, 0))
    if bg is not None:                                                     # frosted glass of what lies behind
        x0, y0 = (W - pw) // 2, (H - ph) // 2
        g = bg.crop((x0, y0, x0 + pw, y0 + ph)).filter(ImageFilter.GaussianBlur(24 * U)).convert('RGBA'); pg.alpha_composite(g)
    m = Image.new('L', (pw, ph), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, pw - 1, ph - 1], radius=int(34 * U), fill=255)
    tint = Image.new('RGBA', (pw, ph), (18, 22, 32, 205)); pg.alpha_composite(tint)
    d = ImageDraw.Draw(pg)
    d.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=int(34 * U), outline=(255, 255, 255, 60), width=int(2 * U))
    d.rounded_rectangle([int(50 * U), int(60 * U), int(62 * U), ph - int(60 * U)], radius=int(6 * U), fill=(240, 180, 60, 255))
    cx, cy, r = int(150 * U), int(125 * U), int(48 * U)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 180, 60, 255))
    d.rectangle([cx - 18 * U, cy - 26 * U, cx + 18 * U, cy + 26 * U], fill=(18, 22, 32, 255))
    for k in (-12, 0, 12): d.line([cx - 10 * U, cy + k * U, cx + 10 * U, cy + k * U], fill=(240, 180, 60, 255), width=int(3 * U))
    ti = text_img(doc['title'], 'bold', 58, fill=(255, 255, 255), shadow=False); pg.alpha_composite(ti, (int(220 * U), int(85 * U)))
    d.line([int(220 * U), int(190 * U), pw - int(80 * U), int(190 * U)], fill=(255, 255, 255, 50), width=int(2 * U))
    y = int(230 * U)
    for txt, at in doc['lines']:
        s = _typed(txt, at, t)
        if s:
            d.ellipse([int(225 * U), y + int(24 * U), int(243 * U), y + int(42 * U)], fill=(240, 180, 60, 255))
            li = text_img(s, 'med', 48, fill=(235, 238, 245), shadow=False); pg.alpha_composite(li, (int(260 * U), y - int(14 * U)))
        y += int(90 * U)
    pg.putalpha(Image.fromarray(np.minimum(np.asarray(pg.getchannel('A')), np.asarray(m))))
    return pg, None

def doc_evidence(doc, t, pw, ph):
    pg = _page(pw, ph, (246, 244, 232), seed=6, vign=0.12, grain=0.08); d = ImageDraw.Draw(pg)
    for i in range(16):
        y = int((150 + i * 44) * U)
        if y < ph - 20 * U: d.line([0, y, pw, y], fill=(120, 160, 210, 140), width=max(1, int(2 * U)))
    d.line([int(110 * U), 0, int(110 * U), ph], fill=(220, 90, 90, 180), width=int(3 * U))
    ti = text_img(doc['title'], 'bold', 54, fill=(20, 40, 110), shadow=False); pg.alpha_composite(ti, (int(140 * U), int(40 * U)))
    y = int(185 * U)
    for txt, at in doc['lines']:
        s = _typed(txt, at, t)
        if s: li = text_img(s, 'med', 46, fill=(20, 35, 95), shadow=False); pg.alpha_composite(li, (int(140 * U), y - int(30 * U)))
        y += int(88 * U)
    for (tx, ty, ang) in ((0.12, 0.0, -8), (0.88, 0.0, 10)):               # tape strips
        tp = Image.new('RGBA', (int(190 * U), int(54 * U)), (240, 230, 190, 170)).rotate(ang, expand=True, resample=Image.BICUBIC)
        pg.alpha_composite(tp, (int(pw * tx - tp.width / 2), int(-tp.height * 0.35)))
    return pg, (0.74, 0.8)

# ------------------------------------------------------------------ modern document variants + modern folders
GOLD = (240, 180, 60)

def _glass(pw, ph, bg, x0, y0, tint=(18, 22, 32, 205), radius=34, blur=24):
    pg = Image.new('RGBA', (pw, ph), (0, 0, 0, 0))
    if bg is not None:
        g = bg.crop((int(x0), int(y0), int(x0) + pw, int(y0) + ph)).filter(ImageFilter.GaussianBlur(blur * U)).convert('RGBA'); pg.alpha_composite(g)
    pg.alpha_composite(Image.new('RGBA', (pw, ph), tint))
    m = Image.new('L', (pw, ph), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, pw - 1, ph - 1], radius=int(radius * U), fill=255)
    return pg, m

def _finish(pg, m, outline=(255, 255, 255, 60)):
    ImageDraw.Draw(pg).rounded_rectangle([0, 0, pg.width - 1, pg.height - 1], radius=int(34 * U), outline=outline, width=int(2 * U))
    pg.putalpha(Image.fromarray(np.minimum(np.asarray(pg.getchannel('A')), np.asarray(m)))); return pg

def doc_glass(doc, t, pw, ph, bg=None):                                   # light frosted glass, dark text, blue header chip
    x0, y0 = (W - pw) // 2, (H - ph) // 2
    pg, m = _glass(pw, ph, bg, x0, y0, tint=(235, 240, 248, 215)); d = ImageDraw.Draw(pg)
    chip = text_img('दस्तावेज़', 'bold', 32, fill=(255, 255, 255), shadow=False); cb = chip.getchannel('A').getbbox(); chip = chip.crop(cb)
    d.rounded_rectangle([int(60 * U), int(50 * U), int(60 * U) + chip.width + int(44 * U), int(50 * U) + chip.height + int(24 * U)], radius=int(26 * U), fill=(40, 90, 200, 255))
    pg.alpha_composite(chip, (int(82 * U), int(62 * U)))
    ti = text_img(doc['title'], 'bold', 60, fill=(20, 30, 50), shadow=False); pg.alpha_composite(ti, (int(55 * U), int(118 * U)))
    y = int(260 * U)
    for txt, at in doc['lines']:
        s = _typed(txt, at, t)
        if s:
            d.rounded_rectangle([int(60 * U), y, pw - int(60 * U), y + int(70 * U)], radius=int(14 * U), fill=(255, 255, 255, 170))
            li = text_img(s, 'med', 44, fill=(25, 35, 60), shadow=False); pg.alpha_composite(li, (int(85 * U), y - int(22 * U)))
        y += int(90 * U)
    return _finish(pg, m, outline=(255, 255, 255, 160)), None

def doc_split(doc, t, pw, ph, bg=None):                                   # coloured left column with icon + numbered rows
    x0, y0 = (W - pw) // 2, (H - ph) // 2
    pg, m = _glass(pw, ph, bg, x0, y0); d = ImageDraw.Draw(pg); cw = int(330 * U)
    col = Image.new('RGBA', (cw, ph), (0, 0, 0, 0)); a_ = np.zeros((ph, cw, 4), np.float32)
    yy_ = np.linspace(0, 1, ph)[:, None]; a_[..., 0] = 240 - 60 * yy_; a_[..., 1] = 170 - 90 * yy_; a_[..., 2] = 50; a_[..., 3] = 255
    pg.alpha_composite(Image.fromarray(a_.astype(np.uint8), 'RGBA'))
    cx, cy, r = cw // 2, int(ph * 0.33), int(70 * U)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(18, 22, 32, 255))
    d.rectangle([cx - 24 * U, cy - 34 * U, cx + 24 * U, cy + 34 * U], outline=GOLD + (255,), width=int(5 * U))
    for k in (-14, 0, 14): d.line([cx - 12 * U, cy + k * U, cx + 12 * U, cy + k * U], fill=GOLD + (255,), width=int(4 * U))
    tl = text_img(doc['title'], 'bold', 44, fill=(20, 15, 10), shadow=False, maxw=280); pg.alpha_composite(tl, (cw // 2 - tl.width // 2, int(ph * 0.5)))
    y = int(110 * U)
    for i, (txt, at) in enumerate(doc['lines']):
        s = _typed(txt, at, t)
        if s:
            ox = cw + int(60 * U); d.ellipse([ox, y + int(8 * U), ox + int(58 * U), y + int(66 * U)], outline=GOLD + (255,), width=int(4 * U))
            nt = text_img(str(i + 1), 'bold', 34, fill=GOLD, shadow=False); pg.alpha_composite(nt, (ox + int(29 * U) - nt.width // 2, y - int(14 * U)))
            li = text_img(s, 'med', 46, fill=(240, 242, 248), shadow=False, maxw=700); pg.alpha_composite(li, (ox + int(80 * U), y - int(16 * U)))
            d.line([ox, y + int(92 * U), pw - int(50 * U), y + int(92 * U)], fill=(255, 255, 255, 40), width=int(2 * U))
        y += int(120 * U)
    return _finish(pg, m), None

def doc_viewer(doc, t, pw, ph, bg=None):                                  # file-viewer window: title bar, tab, highlighted lines
    x0, y0 = (W - pw) // 2, (H - ph) // 2
    pg, m = _glass(pw, ph, bg, x0, y0, tint=(14, 16, 22, 225)); d = ImageDraw.Draw(pg)
    d.rectangle([0, 0, pw, int(80 * U)], fill=(32, 36, 46, 255))
    for k, c in enumerate([(240, 90, 80), (240, 190, 60), (90, 200, 110)]):
        cx = int((45 + k * 40) * U); d.ellipse([cx - 12 * U, int(28 * U), cx + 12 * U, int(52 * U)], fill=c + (255,))
    tab = text_img('📄 ' + doc['title'] if False else doc['title'], 'med', 34, fill=(220, 225, 235), shadow=False)
    d.rounded_rectangle([int(190 * U), int(14 * U), int(190 * U) + tab.width + int(40 * U), int(80 * U)], radius=int(10 * U), fill=(18, 22, 30, 255))
    pg.alpha_composite(tab, (int(210 * U), int(12 * U)))
    ti = text_img(doc['title'], 'bold', 58, fill=GOLD, shadow=False); pg.alpha_composite(ti, (int(60 * U), int(110 * U)))
    y = int(230 * U)
    for i, (txt, at) in enumerate(doc['lines']):
        s = _typed(txt, at, t)
        if s:
            ln = text_img(f'{i + 1:02d}', 'med', 34, fill=(110, 120, 140), shadow=False); pg.alpha_composite(ln, (int(60 * U), y - int(4 * U)))
            k = min(1, (t - at) / 0.9); d.rectangle([int(130 * U), y + int(8 * U), int(130 * U + (pw - 200 * U) * k), y + int(68 * U)], fill=(240, 180, 60, 40))
            li = text_img(s, 'med', 46, fill=(235, 238, 245), shadow=False); pg.alpha_composite(li, (int(140 * U), y - int(14 * U)))
        y += int(88 * U)
    return _finish(pg, m), None

def doc_headline(doc, t, pw, ph, bg=None):                                 # news-style: red label, big headline, quote rows
    x0, y0 = (W - pw) // 2, (H - ph) // 2
    pg, m = _glass(pw, ph, bg, x0, y0, tint=(12, 12, 16, 220)); d = ImageDraw.Draw(pg)
    lab = text_img('रिपोर्ट', 'bold', 36, fill=(255, 255, 255), shadow=False)
    d.rectangle([int(60 * U), int(55 * U), int(60 * U) + lab.width + int(20 * U), int(55 * U) + lab.height - int(16 * U)], fill=(210, 30, 35, 255))
    pg.alpha_composite(lab, (int(70 * U), int(47 * U)))
    ti = text_img(doc['title'], 'bold', 72, fill=(255, 255, 255), shadow=False); pg.alpha_composite(ti, (int(50 * U), int(120 * U)))
    d.rectangle([int(60 * U), int(245 * U), int(260 * U), int(253 * U)], fill=(210, 30, 35, 255))
    y = int(290 * U)
    for txt, at in doc['lines']:
        li = typed_highlight(txt, 'med', 46, t, at, fill=(225, 228, 235))
        if li is not None:
            d.rectangle([int(60 * U), y, int(68 * U), y + int(60 * U)], fill=(255, 255, 255, 120))
            pg.alpha_composite(li, (int(90 * U), y - int(20 * U)))
        y += int(86 * U)
    return _finish(pg, m), None

MODERN_DOCS = {'modern': doc_modern, 'glass': doc_glass, 'split': doc_split, 'viewer': doc_viewer, 'headline': doc_headline}

def draw_files_modern(img, sp, t):
    fs = sp['files']; n = len(fs); fw, fh = 440 * U, 520 * U; gap = 60 * U
    x_start = W / 2 - (n * fw + (n - 1) * gap) / 2; yb = H * 0.54
    base = img.convert('RGB')
    for i, (year, name, at) in enumerate(fs):
        a = ease((t - at) / 0.5)
        if a <= 0: continue
        x = x_start + i * (fw + gap); y = yb - fh / 2 + (1 - a) * 70 * U
        dimmed = sp.get('dim_others') and sp['dim_others'][0] != i and t >= sp['dim_others'][1]
        pg, m = _glass(int(fw), int(fh), base, x, y)
        d = ImageDraw.Draw(pg)
        d.rounded_rectangle([0, 0, int(fw), int(12 * U)], radius=int(6 * U), fill=GOLD + (255,))
        cx, cy = int(fw / 2), int(115 * U)                                  # folder glyph
        d.rounded_rectangle([cx - 58 * U, cy - 44 * U, cx - 8 * U, cy - 26 * U], radius=int(6 * U), fill=GOLD + (255,))
        d.rounded_rectangle([cx - 58 * U, cy - 32 * U, cx + 58 * U, cy + 40 * U], radius=int(10 * U), fill=GOLD + (255,))
        ty = text_img(year, 'bold', 56, fill=GOLD, shadow=False); pg.alpha_composite(ty, (int(fw / 2 - ty.width / 2), int(175 * U)))
        d.line([int(50 * U), int(270 * U), int(fw - 50 * U), int(270 * U)], fill=(255, 255, 255, 50), width=int(2 * U))
        tn = typed_highlight(name, 'bold', 44, t, at + 0.25, fill=(245, 246, 250), maxw=390)
        if tn is not None: pg.alpha_composite(tn, (int(fw / 2 - tn.width / 2), int(272 * U)))
        pg = _finish(pg, m)
        full = Image.new('RGBA', img.size, (0, 0, 0, 0)); _shadowed(full, pg, int(x), int(y), alpha=150)
        for st in sp.get('stamps', []):                                     # badge pill instead of a rubber stamp
            if st[0] == i and t >= st[3]:
                k = ease((t - st[3]) / 0.3); bt = text_img(st[1], 'bold', 34, fill=(255, 255, 255), shadow=False, maxw=360)
                bb = bt.getchannel('A').getbbox() or (0, 0, bt.width, bt.height); tw, th_ = bb[2] - bb[0], bb[3] - bb[1]
                bw, bh = tw + int(56 * U), th_ + int(30 * U); badge = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
                ImageDraw.Draw(badge).rounded_rectangle([0, 0, bw - 1, bh - 1], radius=bh // 2, fill=FILL[st[2]] + (255,))
                badge.alpha_composite(bt.crop(bb), (int(28 * U), int(15 * U)))
                sc = 1.25 - 0.25 * k; badge = badge.resize((max(1, int(bw * sc)), max(1, int(bh * sc))), Image.BICUBIC)
                badge.putalpha(badge.getchannel('A').point(lambda v: int(v * k)))
                full.alpha_composite(badge, (int(x + fw / 2 - badge.width / 2), int(y + fh - 80 * U - badge.height / 2)))
        if dimmed:
            dm = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(dm).rounded_rectangle([x, y, x + fw, y + fh], radius=int(34 * U), fill=(0, 0, 0, 150))
            full.alpha_composite(dm)
        full.putalpha(full.getchannel('A').point(lambda v: int(v * a))); img.alpha_composite(full)

# ------------------------------------------------------------------ typing + highlight (HL_STYLE env)
# Points (document lines, folder names, checklist items) and the lower-corner captions are written as if typed while they
# are spoken, and a highlighter band sweeps behind them. Main texts (photo text, dates, quotes, big words) are typed only.
HL = {'gold': ((255, 200, 30), (20, 18, 12)), 'saffron': ((255, 128, 24), (20, 14, 8)), 'cyan': ((40, 210, 255), (8, 20, 30)),
      'red': ((225, 35, 45), (255, 255, 255)), 'lime': ((140, 230, 60), (12, 24, 8))}
HL_STYLE = os.environ.get('HL_STYLE', 'gold')

def type_dur(txt): return min(2.4, max(0.6, len(txt) * 0.05))

def reveal(im, frac, soft=None):
    """show the left `frac` of a text image with a soft edge (keeps Devanagari shaping intact)"""
    if frac >= 1: return im
    if frac <= 0: return None
    soft = soft or 30 * U; w = im.width; edge = frac * (w + soft)
    ramp = np.clip((edge - np.arange(w, dtype=np.float32)) / soft, 0, 1)
    out = im.copy(); out.putalpha(Image.fromarray((np.asarray(im.getchannel('A'), np.float32) * ramp[None, :]).astype(np.uint8)))
    return out

@lru_cache(256)
def _text2(txt, kind, size, maxw, fill, fill_hl):
    a = text_img(txt, kind, size, fill=fill, shadow=False, maxw=maxw)
    b = text_img(txt, kind, size, fill=fill_hl, shadow=False, maxw=maxw)
    return a, b

def typed_highlight(txt, kind, size, t, at, fill=(240, 242, 248), maxw=None, highlight=True, dur=None):
    """RGBA image of `txt` typed in from time `at`, with a highlighter band behind the typed part"""
    if t < at: return None
    dur = dur or type_dur(txt); frac = min(1.0, (t - at) / dur)
    col, ink = HL[HL_STYLE]
    a, b = _text2(txt, kind, size, maxw, fill, ink if highlight else fill)
    bb = a.getchannel('A').getbbox() or (0, 0, a.width, a.height)
    if not highlight: return reveal(a, frac)
    hk = ease(min(1.0, (t - at) / (dur + 0.25)))                      # the band trails the typing a little
    band = Image.new('RGBA', a.size, (0, 0, 0, 0)); d = ImageDraw.Draw(band)
    x1 = bb[0] + (bb[2] - bb[0] + 16 * U) * hk
    if x1 > bb[0]:
        d.rounded_rectangle([bb[0] - 10 * U, bb[1] - 4 * U, x1, bb[3] + 8 * U], radius=int(8 * U), fill=col + (235,))
    band.alpha_composite(reveal(b, frac) or Image.new('RGBA', a.size, (0, 0, 0, 0)))
    cover = Image.new('L', a.size, 0); ImageDraw.Draw(cover).rectangle([0, 0, int(x1), a.height], fill=255)
    rest = reveal(a, frac)
    if rest is not None:
        r = rest.copy(); ra = np.asarray(r.getchannel('A'), np.float32) * (1 - np.asarray(cover, np.float32) / 255)
        r.putalpha(Image.fromarray(ra.astype(np.uint8))); band.alpha_composite(r)
    return band

@lru_cache(1)
def cork_bg():
    n = _noise(W, H, 11, 2); n2 = _noise(W, H, 12, 14)
    a = np.array([150, 104, 62], np.float32) * (0.72 + 0.35 * n[..., None]) * (0.85 + 0.25 * n2[..., None])
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')

def draw_doc(img, sp, t):
    doc = sp['doc']; style = sp.get('docstyle', DOC_STYLE); pw, ph = int(1180 * U), int(800 * U)
    a = ease(t / 0.6); rot = sp.get('rot', -2.0)
    full = Image.new('RGBA', img.size, (0, 0, 0, 0))
    if style == 'evidence':
        img.alpha_composite(cork_bg())
        note = _page(int(330 * U), int(240 * U), (250, 230, 120), seed=8, vign=0.1, grain=0.05)
        nt = text_img('?', 'bold', 120, fill=(160, 30, 30), shadow=False); note.alpha_composite(nt, ((note.width - nt.width) // 2, (note.height - nt.height) // 2))
        note = note.rotate(7, expand=True, resample=Image.BICUBIC); _shadowed(img, note, int(W * 0.8), int(H * 0.07), blur=10, alpha=160)
    if style in MODERN_DOCS:
        pg, spos = MODERN_DOCS[style](doc, t, pw, ph, bg=img.convert('RGB')); rot = 0
    else:
        pg, spos = {'govfile': doc_govfile, 'dossier': doc_dossier, 'telegram': doc_telegram, 'evidence': doc_evidence}.get(style, None)(doc, t, pw, ph) \
            if style in ('govfile', 'dossier', 'telegram', 'evidence') else (None, None)
    if pg is None:                                                          # classic
        pg = paper(pw, ph).copy(); d = ImageDraw.Draw(pg)
        d.rectangle([int(30 * U), int(30 * U), pw - int(30 * U), ph - int(30 * U)], outline=(120, 90, 60, 255), width=int(3 * U))
        ti = text_img(doc['title'], 'bold', 58, fill=(60, 35, 20), shadow=False); pg.alpha_composite(ti, ((pw - ti.width) // 2, int(40 * U)))
        d.line([int(90 * U), int(170 * U), pw - int(90 * U), int(170 * U)], fill=(120, 90, 60, 255), width=int(3 * U))
        y = int(200 * U)
        for txt, at in doc['lines']:
            s = _typed(txt, at, t)
            if s: li = text_img(s, 'serif', 50, fill=(40, 28, 18), shadow=False); pg.alpha_composite(li, (int(90 * U), y))
            y += int(92 * U)
        spos = (0.72, 0.8)
    x0, y0 = (W - pg.width) // 2, (H - pg.height) // 2 + int((1 - a) * 60 * U)
    _shadowed(full, pg, x0, y0, alpha=200 if style not in MODERN_DOCS else 140)
    if style == 'evidence':                                                 # pushpin and red string
        dd = ImageDraw.Draw(full); px, py = x0 + pg.width // 2, y0 + int(26 * U)
        dd.line([(px, py), (W * 0.8 + 150 * U, H * 0.07 + 40 * U)], fill=(200, 20, 20, 255), width=int(4 * U))
        dd.ellipse([px - 24 * U, py - 24 * U, px + 24 * U, py + 24 * U], fill=(210, 30, 30, 255), outline=(90, 10, 10, 255), width=int(3 * U))
        dd.ellipse([px - 9 * U, py - 14 * U, px + 3 * U, py - 2 * U], fill=(255, 160, 160, 255))
    if doc.get('stamp'):
        txt, at, col = doc['stamp']
        if style in MODERN_DOCS:                                            # badge
            if t >= at:
                k = ease((t - at) / 0.3); bt = text_img(txt, 'bold', 42, fill=(255, 255, 255), shadow=False); bb = bt.getchannel('A').getbbox(); bt = bt.crop(bb)
                bw, bh = bt.width + int(64 * U), bt.height + int(34 * U); badge = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
                ImageDraw.Draw(badge).rounded_rectangle([0, 0, bw - 1, bh - 1], radius=bh // 2, fill=FILL[col] + (255,)); badge.alpha_composite(bt, (int(32 * U), int(17 * U)))
                badge.putalpha(badge.getchannel('A').point(lambda v: int(v * k)))
                full.alpha_composite(badge, (int(x0 + pg.width - bw - 60 * U), int(y0 + pg.height - bh - 50 * U + (1 - k) * 20 * U)))
        else:
            put_stamp(full, txt, FILL[col], x0 + pg.width * spos[0], y0 + pg.height * spos[1], t, at, 70)
    if rot: full = full.rotate(rot, resample=Image.BICUBIC, center=(W / 2, H / 2))
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
        if p > 0 and sp.get('tick'):                       # gold tick instead of a red cross
            c = (240, 190, 70, 255)
            d.line([(x + 14 * U, y), (x + 14 * U + (b - 14 * U) * min(1, p * 2), y + (b - 20 * U) * min(1, p * 2))], fill=c, width=int(11 * U))
            if p > 0.5: q = (p - 0.5) * 2; d.line([(x + b, y + b - 20 * U), (x + b + (b - 14 * U) * q, y + b - 20 * U - (2 * b - 10 * U) * q)], fill=c, width=int(11 * U))
        elif p > 0:
            c = (220, 40, 30, 255)
            d.line([x + 10 * U, y - b + 10 * U, x + 10 * U + (2 * b - 20 * U) * min(1, p * 2), y - b + 10 * U + (2 * b - 20 * U) * min(1, p * 2)], fill=c, width=int(11 * U))
            if p > 0.5: q = (p - 0.5) * 2; d.line([x + 2 * b - 10 * U, y - b + 10 * U, x + 2 * b - 10 * U - (2 * b - 20 * U) * q, y - b + 10 * U + (2 * b - 20 * U) * q], fill=c, width=int(11 * U))
        ti = typed_highlight(txt, 'bold', 70 if n < 4 else 62, t, at + 0.15, fill=(250, 244, 232))
        if ti is not None: lay.alpha_composite(ti, (int(x + 2 * b + 30 * U), int(y - ti.height / 2)))
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
        img = (card_bg_modern(sp.get('tone', 'dark'), t, hash(str(sp.get('files') or sp.get('doc') or sp.get('check') or ''))%7) if BG_STYLE != 'classic' else card_bg(sp.get('tone', 'dark')).copy())
    if sp.get('clock'): draw_clock(img, t, sp)
    img = img.convert('RGBA')
    if sp.get('doc'): draw_doc(img, sp, t)
    if sp.get('check'): draw_check(img, sp, t)
    if sp.get('files'): (draw_files_modern if FILES_STYLE == 'modern' else draw_files)(img, sp, t)
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
        if kind == 'tint':
            c = opt.get('col', (10, 20, 45)); img.alpha_composite(Image.new('RGBA', img.size, tuple(c) + (int(255 * opt.get('k', 0.45) * a),))); continue
        if kind == 'rain':
            img.alpha_composite(rain_layer(t, a, opt.get('dens', 1.0))); continue
        if kind == 'lightning':
            al = max([lightning_alpha(t, b) for b in opt.get('times', [at])] + [0])
            if al > 0.01: img.alpha_composite(Image.new('RGBA', img.size, (220, 230, 255, int(200 * al))))
            continue
        if kind == 'caption':
            ti = typed_highlight(txt, 'med', 46, t, at, fill=(250, 245, 235))
            if ti is None: continue
            bb = ti.getchannel('A').getbbox() or (0, 0, 10, 10)
            bx = Image.new('RGBA', (bb[2] + int(40 * U), ti.height - int(20 * U)), (0, 0, 0, 0)); bd = ImageDraw.Draw(bx)
            bd.rectangle([0, 0, bx.width, bx.height], fill=(10, 10, 14, 185)); bd.rectangle([0, 0, int(8 * U), bx.height], fill=HL[HL_STYLE][0] + (255,))
            bx.alpha_composite(ti, (int(16 * U), -int(10 * U)))
            img.alpha_composite(fade_alpha(bx, a), (int(80 * U), H - bx.height - int(90 * U))); continue
        if kind in ('big', 'quote', 'date'):
            im = ov_img(kind, txt, opt.get('sub', ''))
            if kind == 'big' and opt.get('sub'):                         # main line first, then the sub line
                main = ov_img(kind, txt, ''); frac = min(1, (t - at) / type_dur(txt))
                subf = min(1, max(0, (t - at - type_dur(txt) * 0.8) / type_dur(opt['sub'])))
                im2 = Image.new('RGBA', im.size, (0, 0, 0, 0)); top = im.crop((0, 0, im.width, main.height - int(50 * U))); bot = im.crop((0, main.height - int(50 * U), im.width, im.height))
                r1 = reveal(top, frac); r2 = reveal(bot, subf)
                if r1 is not None: im2.alpha_composite(r1)
                if r2 is not None: im2.alpha_composite(r2, (0, main.height - int(50 * U)))
                im_t = im2
            else:
                im_t = reveal(im, min(1, (t - at) / type_dur(txt))) or Image.new('RGBA', im.size, (0, 0, 0, 0))
            if kind in ('quote', 'big') and opt.get('dim', True):
                img.alpha_composite(Image.new('RGBA', img.size, (0, 0, 0, int((165 if kind == 'quote' else 120) * a))))
            if kind == 'date': x, y = int(70 * U), int(60 * U)
            else: x, y = int(opt.get('x', 0.5) * W - im.width / 2), int(opt.get('y', 0.5) * H - im.height / 2)
            img.alpha_composite(fade_alpha(im_t, min(1, a * 2)), (x, y)); continue
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
        n = len([s for s in TIMING['scenes'] if s['start'] < lim]); name = 'Shastri_Preview.mp4'
    else:
        name = 'Shastri_Tashkent_Ki_Raat.mp4'
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
