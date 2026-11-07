"""Documentary renderer for the Hindi Partition video.

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
FPS = int(os.environ.get('FPS', 25))
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
    return (1 - 0.42 * np.clip(r - 0.55, 0, 1) ** 1.5 * 1.6).clip(0.45, 1)[..., None]

@lru_cache(None)
def grain(i):
    g = np.random.default_rng(i).normal(0, 1, (H // 2 + 1, W // 2 + 1)).astype(np.float32)
    g = np.asarray(Image.fromarray(((g * 40) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32) - 128
    return (g / 40 * 7.0)[..., None]

def finish(arr, t, amt=1.0):
    a = arr.astype(np.float32) * vignette()
    a += grain(int(t * FPS) % 6) * amt
    return a.clip(0, 255).astype(np.uint8)

# ------------------------------------------------------------------ photos
CROP = {'amritsar': (0.05, 0.08, 0.98, 0.875)}

@lru_cache(8)
def photo(name, grade):
    im = Image.open(os.path.join(ASSETS, 'photos', name + '.jpg'))
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
        x0 = min(max(0, x0), im.width - cw); y0 = min(max(0, y0), im.height - ch)
        out = im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
        return out
    # framed: the whole photo on a blurred copy, slowly scaling
    bg = blur_bg(name, grade).copy()
    hmax = sp.get('h', 0.84) * H; wmax = sp.get('w', 0.84) * W
    s = min(hmax / im.height, wmax / im.width) * lerp(1.0, z / sp.get('z0', 1.0), 1) ** 0.35
    pw, ph = int(im.width * s), int(im.height * s)
    p = im.resize((pw, ph), Image.BILINEAR)
    px = int(W * sp.get('px', 0.5) - pw / 2); py = int(H * sp.get('py', 0.5) - ph / 2)
    sh = Image.new('L', (pw + 80, ph + 80), 0); ImageDraw.Draw(sh).rectangle([40, 40, 40 + pw, 40 + ph], fill=200)
    sh = sh.filter(ImageFilter.GaussianBlur(18 * U))
    bg.paste((0, 0, 0), (px - 40 + int(6 * U), py - 40 + int(10 * U)), sh)
    border = int(7 * U)
    bg.paste((236, 228, 210), (px - border, py - border, px + pw + border, py + ph + border))
    bg.paste(p, (px, py))
    return bg

# ------------------------------------------------------------------ map
M_LON0, M_LON1, M_LAT0, M_LAT1 = 55.0, 105.0, 0.0, 42.0
MPX = 3200                                         # base map width in px
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
MY0, MY1 = merc(M_LAT1), merc(M_LAT0)
MPY = int(MPX * (MY0 - MY1) / math.radians(M_LON1 - M_LON0))
def ll(lat, lon):
    return (lon - M_LON0) / (M_LON1 - M_LON0) * MPX, (MY0 - merc(lat)) / (MY0 - MY1) * MPY

@lru_cache(None)
def countries():
    return json.load(open(os.path.join(ASSETS, 'countries.json')))

def rings(name):
    return [[ll(la, lo) for lo, la in r] for r in countries()[name]]

LAND = (205, 186, 148); SEA = (34, 52, 60); INK = (60, 45, 30)
@lru_cache(None)
def map_base():
    rng = np.random.default_rng(3)
    im = Image.new('RGB', (MPX, MPY), SEA)
    d = ImageDraw.Draw(im)
    for n, rs in countries().items():
        for r in rs:
            pts = [ll(la, lo) for lo, la in r]
            xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
            if max(xs) < -50 or min(xs) > MPX + 50 or max(ys) < -50 or min(ys) > MPY + 50: continue
            d.polygon(pts, fill=LAND)
    # coast glow + paper texture
    land = np.asarray(im, np.float32)
    mask = (np.abs(land - np.array(LAND)).sum(axis=2) < 3).astype(np.float32)
    edge = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10)), np.float32) / 255
    sea_glow = (1 - mask) * edge * 0.35
    land[..., :] += sea_glow[..., None] * np.array([70, 70, 55])
    tex = np.asarray(Image.fromarray((rng.normal(128, 40, (MPY // 4, MPX // 4))).clip(0, 255).astype(np.uint8)).resize((MPX, MPY), Image.BICUBIC), np.float32) - 128
    land += tex[..., None] * 0.18
    im = Image.fromarray(land.clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for n, rs in countries().items():
        for r in rs:
            pts = [ll(la, lo) for lo, la in r]
            xs = [p[0] for p in pts]
            if max(xs) < -50 or min(xs) > MPX + 50: continue
            d.line(pts + [pts[0]], fill=(150, 130, 100), width=2)
    return im

FILL = {'raj': (186, 70, 70), 'india': (226, 128, 40), 'pak': (40, 120, 70), 'gray': (120, 110, 100)}
GROUP = {'raj': ['India', 'Pakistan', 'Bangladesh'], 'india': ['India'], 'pak': ['Pakistan', 'Bangladesh'],
         'wpak': ['Pakistan'], 'epak': ['Bangladesh']}

@lru_cache(None)
def group_mask(g):
    m = Image.new('L', (MPX, MPY), 0); d = ImageDraw.Draw(m)
    for n in GROUP[g]:
        for r in rings(n): d.polygon(r, fill=255)
    return m

@lru_cache(None)
def border_paths():
    """India-Pakistan and India-Bangladesh land borders (the Radcliffe lines), as ordered point lists"""
    ind = np.concatenate([np.array(r) for r in rings('India')])
    out = []
    for n in ('Pakistan', 'Bangladesh'):
        for r in rings(n):
            a = np.array(r)
            if len(a) < 30: continue
            dmin = np.array([np.min(np.hypot(*(ind - p).T)) for p in a])
            near = dmin < 6
            # longest run of near points (ring is closed: rotate to start at a far point)
            if near.all() or not near.any(): continue
            st = int(np.argmin(near)); idx = np.roll(np.arange(len(a)), -st); nr = near[idx]
            runs, cur = [], []
            for i, v in zip(idx, nr):
                if v: cur.append(i)
                elif cur: runs.append(cur); cur = []
            if cur: runs.append(cur)
            for run in runs:
                if len(run) > 20: out.append([tuple(a[i]) for i in run])
    return out

def view_box(v):
    lat, lon, wdeg = v
    cx, cy = ll(lat, lon); w = wdeg / (M_LON1 - M_LON0) * MPX
    return cx, cy, w

def draw_map(sp, t, dur):
    k = ease(t / dur)
    v0 = view_box(sp.get('view', (24, 80, 40))); v1 = view_box(sp.get('view1', sp.get('view', (24, 80, 40))))
    cx, cy, w = (lerp(a, b, k) for a, b in zip(v0, v1))
    h = w * H / W
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    base = map_base().copy()
    s = W / w
    for f in sp.get('fill', []):
        g, col = f[0], f[1]; at = f[2] if len(f) > 2 else 0.0
        a = ease((t - at) / 0.8) if at is not None else 1.0
        if f[3:] and f[3] is not None: a *= 1 - ease((t - f[3]) / 0.8)
        if a <= 0: continue
        layer = Image.new('RGB', base.size, FILL[col])
        base.paste(Image.blend(base, layer, 0.55), (0, 0), group_mask(g).point(lambda v: int(v * a)))
    out = base.resize((W, H), Image.BILINEAR, box=box).convert('RGBA')
    d = ImageDraw.Draw(out)
    def scr(lat, lon):
        x, y = ll(lat, lon); return (x - box[0]) * s, (y - box[1]) * s
    if sp.get('line') is not None:                   # Radcliffe line drawing on
        at, dl = sp['line'] if isinstance(sp['line'], tuple) else (sp['line'], 2.5)
        p = ease((t - at) / dl)
        for path in border_paths():
            n = max(2, int(len(path) * p))
            pts = [((x - box[0]) * s, (y - box[1]) * s) for x, y in path[:n]]
            if len(pts) > 1:
                d.line(pts, fill=(120, 0, 0, 255), width=int(9 * U), joint='curve')
                d.line(pts, fill=(235, 40, 30, 255), width=int(5 * U), joint='curve')
    for a in sp.get('arrows', []):                   # (lat0, lon0, lat1, lon1, colour, at)
        la0, lo0, la1, lo1, col, at = a
        p = ease((t - at) / 1.6)
        if p <= 0: continue
        x0, y0 = scr(la0, lo0); x1, y1 = scr(la1, lo1)
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - 0.18 * abs(x1 - x0)
        pts = [((1 - u) ** 2 * x0 + 2 * (1 - u) * u * mx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * my + u * u * y1)
               for u in np.linspace(0, p, 40)]
        c = FILL[col] + (255,)
        d.line(pts, fill=(20, 15, 10, 200), width=int(20 * U)); d.line(pts, fill=c, width=int(13 * U))
        (xa, ya), (xb, yb) = pts[-2], pts[-1]; ang = math.atan2(yb - ya, xb - xa); L = 30 * U
        tri = [(xb + math.cos(ang) * L * 0.6, yb + math.sin(ang) * L * 0.6),
               (xb + math.cos(ang + 2.5) * L, yb + math.sin(ang + 2.5) * L), (xb + math.cos(ang - 2.5) * L, yb + math.sin(ang - 2.5) * L)]
        d.polygon(tri, fill=c, outline=(20, 15, 10, 220))
    for c in sp.get('cities', []):                    # (hindi name, lat, lon, at, dx, dy)
        name, la, lo, at = c[:4]; dx, dy = (c[4], c[5]) if len(c) > 5 else (0, -1)
        a = ease((t - at) / 0.5)
        if a <= 0: continue
        x, y = scr(la, lo); r = 9 * U
        d.ellipse([x - r - 3, y - r - 3, x + r + 3, y + r + 3], fill=(30, 20, 10, int(255 * a)))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(250, 240, 220, int(255 * a)))
        ti = text_img(name, 'bold', 48, fill=(255, 248, 235), stroke=0)
        ti.putalpha(ti.getchannel('A').point(lambda v: int(v * a)))
        out.alpha_composite(ti, (int(x - ti.width / 2 + dx * 60 * U), int(y - ti.height / 2 + dy * 48 * U)))
    for lab in sp.get('labels', []):                  # (hindi text, lat, lon, at, size)
        txt, la, lo, at = lab[:4]; size = lab[4] if len(lab) > 4 else 56
        a = ease((t - at) / 0.6)
        if a <= 0: continue
        x, y = scr(la, lo)
        ti = text_img(txt, 'bold', size, fill=(255, 250, 240))
        ti.putalpha(ti.getchannel('A').point(lambda v: int(v * a)))
        out.alpha_composite(ti, (int(x - ti.width / 2), int(y - ti.height / 2)))
    return out.convert('RGB')

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

def draw_card(sp, t, dur):
    if sp.get('bgimg'):
        img = blur_bg(sp['bgimg'], sp.get('grade', 'bw')).copy()
    else:
        img = card_bg(sp.get('tone', 'dark')).copy()
    if sp.get('clock'): draw_clock(img, t, sp)
    return img

# ------------------------------------------------------------------ overlays
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
        n = len([s for s in TIMING['scenes'] if s['start'] < lim]); name = 'Partition_Preview.mp4'
    else:
        name = 'Bharat_Ka_Batwara_1947.mp4'
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
