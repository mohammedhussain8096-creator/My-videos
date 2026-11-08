"""Documentary renderer for the English Chernobyl video (1080p30).

Scene kinds (see plan.py), all animated, never an empty background:
  photo     free-licence photo with a slow Ken Burns move, cold/warm grade, light grain + vignette
  map       night map of Europe/Ukraine: glowing plant pin, 30 km zone ring, spreading radioactive plume, cities
  reactor   RBMK cross-section: fuel channels, control rods with graphite tips, boiling water, power glow, explosion
  graph     the night's power curve drawing itself, with annotations
  dosimeter dial + LCD: needle pinned at 3.6, optional reveal of the real reading
  clock     red LED clock ticking (01:23:04 -> 01:23:40 ...)
  counter   big number counting up, optional icon grid (people / buses)
  bars      comparison bars (doses etc.)
  title     chapter title over a blurred, darkened photo
Overlays: date, caption, big, quote, label.  Transitions: fade (default), flash, glitch, push, dip, cut.
Audio: narration + ducked music + sfx (boom, geiger, whoosh, alarm, tick).
Usage: python3 render.py preview [seconds] | full | still N [t].  Env: RES, FPS, CRF, PRESET, OUT_DIR, KEEP, WORKERS."""
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
CRF = os.environ.get('CRF', '17'); PRESET = os.environ.get('PRESET', 'medium')
TIMING = json.load(open(os.path.join(OUT, 'timing.json')))
XF = 0.35
RED = (230, 45, 35); AMBER = (255, 176, 40); TOX = (190, 235, 70); WHITE = (245, 245, 240); STEEL = (150, 160, 165)

# ------------------------------------------------------------------ text
FONTS = {'head': 'BebasNeue.ttf', 'osw': 'Oswald-SemiBold.ttf', 'body': 'Inter-Medium.ttf', 'bold': 'Inter-ExtraBold.ttf',
         'serif': 'SourceSerif-Italic.ttf', 'mono': 'ShareTechMono.ttf'}
@lru_cache(None)
def font(kind, size):
    return ImageFont.truetype(os.path.join(ASSETS, 'fonts', FONTS[kind]), max(8, int(size * U)))

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

@lru_cache(256)
def text_img(txt, kind, size, fill=WHITE, maxw=None, spacing=1.12, track=0, shadow=True, align='center'):
    f = font(kind, size)
    lines = wrap(txt, f, maxw) if maxw else txt.split('\n')
    asc, desc = f.getmetrics(); lh = int((asc + desc) * spacing)
    def lw(l): return int(f.getlength(l) + track * U * max(0, len(l) - 1))
    ws = [lw(l) for l in lines]; pad = int(28 * U)
    im = Image.new('RGBA', (max(ws) + 2 * pad, lh * len(lines) + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        x = pad + ((max(ws) - ws[i]) // 2 if align == 'center' else 0)
        if track:
            for ch in l:
                d.text((x, pad + i * lh), ch, font=f, fill=fill); x += f.getlength(ch) + track * U
        else:
            d.text((x, pad + i * lh), l, font=f, fill=fill)
    if shadow:
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel('A').filter(ImageFilter.GaussianBlur(9 * U)).point(lambda v: int(v * 0.9)))
        base = Image.new('RGBA', im.size, (0, 0, 0, 0)); base.alpha_composite(sh, (int(2 * U), int(4 * U))); base.alpha_composite(im); im = base
    return im

def put(img, im, x, y, a=1.0):
    if a <= 0: return
    if a < 1: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * a)))
    img.alpha_composite(im, (int(x), int(y)))

# ------------------------------------------------------------------ helpers
def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def eout(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def lerp(a, b, k): return a + (b - a) * k

@lru_cache(None)
def vignette():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    return (1 - 0.38 * np.clip(r - 0.55, 0, 1) ** 1.4 * 1.6).clip(0.5, 1)[..., None]

@lru_cache(None)
def grain(i):
    g = np.random.default_rng(i).normal(0, 1, (H // 2 + 1, W // 2 + 1)).astype(np.float32)
    g = np.asarray(Image.fromarray(((g * 40) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32) - 128
    return (g / 40 * 2.0)[..., None]

def finish(a, t):
    a = a.astype(np.float32) * vignette() + grain(int(t * FPS) % 6)
    return a.clip(0, 255).astype(np.uint8)

@lru_cache(None)
def dark_bg(tone='steel'):
    rng = np.random.default_rng(4)
    base = {'steel': (16, 20, 22), 'red': (34, 10, 9), 'tox': (14, 22, 12)}[tone]
    a = np.ones((H, W, 3), np.float32) * np.array(base, np.float32)
    n = np.asarray(Image.fromarray(rng.normal(128, 50, (H // 8, W // 8)).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) - 128
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    glow = np.exp(-(((x - W * 0.5) / (W * 0.6)) ** 2 + ((y - H * 0.45) / (H * 0.6)) ** 2))[..., None]
    a = a + n[..., None] * 0.1 + glow * np.array(base, np.float32) * 1.2
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))

# ------------------------------------------------------------------ photos
CROP = {}
@lru_cache(10)
def photo(name, grade):
    p = os.path.join(ASSETS, 'photos_hd', name + '.jpg')
    if not os.path.exists(p): p = os.path.join(ASSETS, 'photos', name + '.jpg')
    im = ImageOps.exif_transpose(Image.open(p)).convert('RGB')
    if name in CROP:
        l, t, r, b = CROP[name]; im = im.crop((int(l * im.width), int(t * im.height), int(r * im.width), int(b * im.height)))
    if grade == 'cold':          # desaturated, slightly teal: the 'Chernobyl' look
        im = ImageEnhance.Color(ImageOps.autocontrast(im, cutoff=0.5)).enhance(0.55)
        a = np.asarray(im, np.float32); a = a * np.array([0.93, 1.0, 1.04]) + np.array([0, 3, 6]); im = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    elif grade == 'bw':
        g = ImageOps.autocontrast(im.convert('L'), cutoff=1)
        im = Image.merge('RGB', [g.point(lambda v: int(v * 0.97 + 4)), g, g.point(lambda v: min(255, int(v * 1.02 + 4)))])
    elif grade == 'warm':
        im = ImageEnhance.Color(ImageOps.autocontrast(im, cutoff=0.5)).enhance(0.85)
    else:
        im = ImageOps.autocontrast(im, cutoff=0.3)
    k = min(1.0, (1.45 * max(W, H)) / max(im.size))
    if k < 1: im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=60, threshold=2))

@lru_cache(10)
def blur_bg(name, grade):
    im = photo(name, grade); k = max(W / im.width, H / im.height) * 1.1
    b = im.resize((int(im.width * k), int(im.height * k)), Image.BILINEAR)
    b = b.crop(((b.width - W) // 2, (b.height - H) // 2, (b.width - W) // 2 + W, (b.height - H) // 2 + H))
    return ImageEnhance.Brightness(b.filter(ImageFilter.GaussianBlur(26 * U))).enhance(0.38)

def draw_photo(sp, t, D):
    name, grade = sp['img'], sp.get('grade', 'cold')
    im = photo(name, grade); k = ease(t / D)
    z = lerp(sp.get('z0', 1.0), sp.get('z1', 1.12), k)
    fx = lerp(sp.get('fx0', 0.5), sp.get('fx1', sp.get('fx0', 0.5)), k); fy = lerp(sp.get('fy0', 0.5), sp.get('fy1', sp.get('fy0', 0.5)), k)
    frame = sp.get('frame')
    if frame is None:
        cover = max(W / im.width, H / im.height); frame = cover > 2.0 or abs(im.width / im.height - W / H) > 0.6
    if not frame:
        s = max(W / im.width, H / im.height); cw, ch = min(W / z / s, im.width), min(H / z / s, im.height)
        x0 = max(0, min(fx * im.width - cw / 2, im.width - cw)); y0 = max(0, min(fy * im.height - ch / 2, im.height - ch))
        return im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
    bg = blur_bg(name, grade).copy()
    s = min(sp.get('h', 0.84) * H / im.height, sp.get('w', 0.84) * W / im.width, 1.8) * (z / sp.get('z0', 1.0)) ** 0.4
    pw, ph = int(im.width * s), int(im.height * s); p = im.resize((pw, ph), Image.LANCZOS)
    px = int(W * sp.get('px', 0.5) - pw / 2); py = int(H * sp.get('py', 0.5) - ph / 2)
    sh = Image.new('L', (pw + 80, ph + 80), 0); ImageDraw.Draw(sh).rectangle([40, 40, 40 + pw, 40 + ph], fill=210)
    bg.paste((0, 0, 0), (px - 40 + int(6 * U), py - 40 + int(10 * U)), sh.filter(ImageFilter.GaussianBlur(18 * U)))
    bd = int(5 * U); bg.paste((220, 222, 220), (px - bd, py - bd, px + pw + bd, py + ph + bd)); bg.paste(p, (px, py))
    return bg


def live_bg(sp, t, D, default, dark=0.5, grade=None):
    """real photo background with a slow Ken Burns move, darkened for text (never a plain colour)"""
    name = sp.get('bgimg') or default; g = grade or sp.get('grade', 'cold')
    ph = dict(img=name, grade=g, frame=False, z0=sp.get('bz0', 1.05), z1=sp.get('bz1', 1.18), fx0=sp.get('bfx', 0.5), fy0=sp.get('bfy', 0.5))
    im = draw_photo(ph, t, max(D, 0.1))
    a = np.asarray(im, np.float32); yy = np.linspace(0, 1, H)[:, None, None]
    a = a * (1 - dark) * (0.75 + 0.25 * (1 - np.abs(yy - 0.5) * 2))
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))

# ------------------------------------------------------------------ map (real satellite imagery, NASA GIBS, public domain)
M_LON0, M_LON1, M_LAT0, M_LAT1 = -14.0, 62.0, 30.0, 72.0
MPX = 8400
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
MY0, MY1 = merc(M_LAT1), merc(M_LAT0)
MPY = int(MPX * (MY0 - MY1) / math.radians(M_LON1 - M_LON0))
def ll(lat, lon): return (lon - M_LON0) / (M_LON1 - M_LON0) * MPX, (MY0 - merc(lat)) / (MY0 - MY1) * MPY
@lru_cache(None)
def countries(): return json.load(open(os.path.join(ASSETS, 'countries.json')))

def _grade_sat(im):
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(0.85)).enhance(1.12)
    return ImageEnhance.Brightness(im).enhance(0.82)

@lru_cache(None)
def map_base():
    """Europe: NASA Blue Marble Next Generation (500 m), Mercator, with thin country borders"""
    im = _grade_sat(Image.open(os.path.join(ASSETS, 'sat', 'europe_bmng.jpg')).convert('RGB')).resize((MPX, MPY), Image.LANCZOS)
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for n, rs in countries().items():
        for r in rs:
            pts = [ll(la, lo) for lo, la in r]; xs = [p[0] for p in pts]
            if max(xs) < -50 or min(xs) > MPX + 50: continue
            d.line(pts + [pts[0]], fill=(255, 255, 255, 70), width=3)
    im = im.convert('RGBA'); im.alpha_composite(lay); return im.convert('RGB')

Z_LON0, Z_LON1, Z_LAT0, Z_LAT1 = 26.0, 35.0, 48.5, 54.0
@lru_cache(None)
def zone_base():
    """northern Ukraine close-up: NASA MODIS Terra true colour, 9 Aug 2016 (250 m), Mercator, with borders"""
    im = _grade_sat(Image.open(os.path.join(ASSETS, 'sat', 'ukraine_modis.jpg')).convert('RGB'))
    zw, zh = im.size; zy0, zy1 = merc(Z_LAT1), merc(Z_LAT0)
    def zll(lat, lon): return (lon - Z_LON0) / (Z_LON1 - Z_LON0) * zw, (zy0 - merc(lat)) / (zy0 - zy1) * zh
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for n, rs in countries().items():
        for r in rs:
            pts = [zll(la, lo) for lo, la in r]; xs = [p[0] for p in pts]
            if max(xs) < -50 or min(xs) > zw + 50: continue
            d.line(pts + [pts[0]], fill=(255, 255, 255, 80), width=3)
    im = im.convert('RGBA'); im.alpha_composite(lay); return im.convert('RGB'), zll

def view_box(v):
    lat, lon, wdeg = v; cx, cy = ll(lat, lon); w = wdeg / (M_LON1 - M_LON0) * MPX; return cx, cy, w

def sat_frame(cx, cy, w):
    """real-imagery frame for a Europe-pixel view box; blends to the sharp MODIS image when zoomed in"""
    h = w * H / W; box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    wdeg = w / MPX * (M_LON1 - M_LON0)
    eu = map_base().resize((W, H), Image.BILINEAR, box=box) if wdeg > 5.5 else None
    if wdeg < 9.0:
        zim, zll = zone_base()
        # convert the box corners to lon/lat, then to zone pixels
        def inv(x, y):
            lon = M_LON0 + x / MPX * (M_LON1 - M_LON0); my_ = MY0 - y / MPY * (MY0 - MY1)
            lat = math.degrees(2 * math.atan(math.exp(my_)) - math.pi / 2); return lat, lon
        la0, lo0 = inv(box[0], box[1]); la1, lo1 = inv(box[2], box[3])
        x0, y0 = zll(la0, lo0); x1, y1 = zll(la1, lo1)
        if 0 <= x0 and 0 <= y0 and x1 <= zim.width and y1 <= zim.height:
            z = zim.resize((W, H), Image.BICUBIC, box=(x0, y0, x1, y1))
            if eu is None: return z
            k = ease((9.0 - wdeg) / 3.5); return Image.blend(eu, z, k)
    return eu if eu is not None else map_base().resize((W, H), Image.BILINEAR, box=box)

PLANT = (51.389, 30.099)
@lru_cache(64)
def plume_mask(key):
    """soft irregular blob field for the radioactive cloud, in map pixels (stage key = list of blobs)"""
    blobs = json.loads(key)
    m = Image.new('L', (MPX // 4, MPY // 4), 0); d = ImageDraw.Draw(m)
    rng = np.random.default_rng(9)
    nb = len(blobs)
    for bi, (la, lo, r_deg) in enumerate(blobs):
        x, y = ll(la, lo); r = r_deg / (M_LON1 - M_LON0) * MPX; dens = int(150 - 80 * bi / max(1, nb - 1))   # thicker near the source
        for k in range(18):
            ox, oy = rng.normal(0, r * 0.38, 2); rr = r * rng.uniform(0.35, 0.8)
            d.ellipse([(x + ox - rr) / 4, (y + oy - rr * 0.7) / 4, (x + ox + rr) / 4, (y + oy + rr * 0.7) / 4], fill=dens)
    m = m.filter(ImageFilter.GaussianBlur(14))
    a = np.asarray(m, np.float32) / 255                       # break it up with cloud noise
    nz = np.zeros_like(a)
    for oc, amp in ((8, 0.5), (24, 0.3), (64, 0.2)):
        g = rng.random((max(2, a.shape[0] // oc), max(2, a.shape[1] // oc))).astype(np.float32)
        nz += amp * np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize((a.shape[1], a.shape[0]), Image.BICUBIC), np.float32) / 255
    a = np.clip(a * (0.35 + 1.0 * nz), 0, 1)
    return Image.fromarray((a * 255).astype(np.uint8)).resize((MPX, MPY), Image.BILINEAR)

def draw_map(sp, t, D):
    k = ease(t / D)
    if sp.get('style', 'flat') == 'flat':                 # reference style: flat beige/blue map, glowing highlights
        import style
        va, vb = sp.get('view', (50, 25, 40)), sp.get('view1', sp.get('view', (50, 25, 40)))
        # zoom in log-space so big zooms feel even
        vw = math.exp(lerp(math.log(va[2]), math.log(vb[2]), k))
        vv = (lerp(va[0], vb[0], k), lerp(va[1], vb[1], k), vw)
        base, PJ, box = style.flat_frame(sp, t, D, vv); s = W / (box[2] - box[0])
        def scr(la, lo): x, y = PJ(la, lo); return (x - box[0]) * s, (y - box[1]) * s
        if PJ is not style.EU: sp = dict(sp, plume=[])
    else:
        v0 = view_box(sp.get('view', (50, 25, 40))); v1 = view_box(sp.get('view1', sp.get('view', (50, 25, 40))))
        cx, cy, w = (lerp(a, b, k) for a, b in zip(v0, v1)); h = w * H / W
        box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2); s = W / w
        base = sat_frame(cx, cy, w).convert('RGBA')
        def scr(la, lo): x, y = ll(la, lo); return (x - box[0]) * s, (y - box[1]) * s
    # plume: list of stages (at, blobs); each stage fades in over 1.5 s
    for st in sp.get('plume', []):
        at, blobs = st; a = ease((t - at) / 1.6)
        if a <= 0: continue
        m = plume_mask(json.dumps(blobs)).resize((W, H), Image.BILINEAR, box=box)
        pulse = 0.9 + 0.1 * math.sin(t * 1.7)
        glow = Image.new('RGBA', (W, H), (150, 230, 60, 0)); glow.putalpha(m.filter(ImageFilter.GaussianBlur(18 * U)).point(lambda v: int(min(255, v * a * 0.9))))
        core = Image.new('RGBA', (W, H), (215, 245, 110, 0)); core.putalpha(m.point(lambda v: int(min(255, v * a * pulse * 0.95))))
        base.alpha_composite(glow); base.alpha_composite(core)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for z in sp.get('zone', []):                      # (radius_km, at)
        r_km, at = z; a = ease((t - at) / 0.8)
        if a <= 0: continue
        x, y = scr(*PLANT); x2, _ = scr(PLANT[0], PLANT[1] + r_km / (111.3 * math.cos(math.radians(PLANT[0]))))
        R = abs(x2 - x) * eout((t - at) / 1.2)
        d.ellipse([x - R, y - R, x + R, y + R], fill=AMBER + (int(45 * a),), outline=AMBER + (int(235 * a),), width=int(4 * U))
    base.alpha_composite(lay); d = ImageDraw.Draw(base)
    for c in sp.get('cities', []):                    # (name, lat, lon, at, dx, dy)
        name, la, lo, at = c[:4]; dx, dy = (c[4], c[5]) if len(c) > 5 else (1, 0)
        a = ease((t - at) / 0.5)
        if a <= 0: continue
        x, y = scr(la, lo); r = 7 * U
        d.ellipse([x - r, y - r, x + r, y + r], fill=(235, 235, 230, int(255 * a)))
        ti = text_img(name.upper(), 'osw', 34, fill=WHITE if sp.get('style', 'flat') != 'flat' else (30, 30, 30), track=2, shadow=sp.get('style', 'flat') != 'flat')
        put(base, ti, x - ti.width / 2 + dx * (ti.width / 2 + 2 * U), y - ti.height / 2 + dy * 40 * U, a)
    if sp.get('pin', True):                           # the plant: pulsing red beacon
        a = ease((t - sp.get('pin_at', 0.2)) / 0.5)
        if a > 0:
            x, y = scr(*PLANT); rl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(rl)
            for k2 in range(3):
                ph = ((t * 0.8 + k2 / 3) % 1); R = (10 + 60 * ph) * U
                d.ellipse([x - R, y - R, x + R, y + R], outline=RED + (int(200 * (1 - ph) * a),), width=int(3 * U))
            base.alpha_composite(rl); d = ImageDraw.Draw(base)
            r = 11 * U; d.ellipse([x - r, y - r, x + r, y + r], fill=RED + (int(255 * a),), outline=(255, 220, 210, int(255 * a)), width=int(3 * U))
            if sp.get('pin_label', True):
                ti = text_img('CHERNOBYL', 'osw', 38, fill=(255, 210, 200) if sp.get('style', 'flat') != 'flat' else (170, 20, 15), track=3, shadow=sp.get('style', 'flat') != 'flat'); put(base, ti, x + 18 * U, y - ti.height / 2 - 2 * U, a)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for ar in sp.get('arrows', []):                   # wind arrows (lat0, lon0, lat1, lon1, at)
        la0, lo0, la1, lo1, at = ar; p = ease((t - at) / 1.8)
        if p <= 0: continue
        x0, y0 = scr(la0, lo0); x1, y1 = scr(la1, lo1); mx, my = (x0 + x1) / 2 + (y1 - y0) * 0.15, (y0 + y1) / 2 - (x1 - x0) * 0.15
        pts = [((1 - u) ** 2 * x0 + 2 * (1 - u) * u * mx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * my + u * u * y1) for u in np.linspace(0, p, 40)]
        d.line(pts, fill=TOX + (230,), width=int(6 * U))
        (xa, ya), (xb, yb) = pts[-2], pts[-1]; ang = math.atan2(yb - ya, xb - xa); L = 26 * U
        d.polygon([(xb + math.cos(ang) * L * 0.6, yb + math.sin(ang) * L * 0.6), (xb + math.cos(ang + 2.5) * L, yb + math.sin(ang + 2.5) * L),
                   (xb + math.cos(ang - 2.5) * L, yb + math.sin(ang - 2.5) * L)], fill=TOX + (240,))
    base.alpha_composite(lay)
    if sp.get('icons'):
        import style
        for ic in sp['icons']:                          # (kind, lat, lon, at, size)
            kind_, la, lo, at = ic[:4]; size = int((ic[4] if len(ic) > 4 else 180) * U)
            x, y = scr(la, lo); style.put_icon(base, style.radiation_icon(size) if kind_ == 'rad' else style.bolt_icon(size), x, y, t, at)
    return base.convert('RGB')

# ------------------------------------------------------------------ reactor cross-section
def anim(v, t):
    """v = number or (a, b, t0, t1): animate a->b between t0 and t1"""
    if isinstance(v, (int, float)): return v
    a, b, t0, t1 = v; return lerp(a, b, ease((t - t0) / max(0.01, t1 - t0)))

def draw_reactor(sp, t, D):
    img = dark_bg('steel').copy().convert('RGBA'); d = ImageDraw.Draw(img)
    cx = W * sp.get('cx', 0.5); top = H * 0.28; core_w = 760 * U; core_h = 430 * U
    x0, x1 = cx - core_w / 2, cx + core_w / 2; y0, y1 = top + 90 * U, top + 90 * U + core_h
    te = sp.get('explode')                                   # explosion time
    boom = 0 if te is None else eout((t - te) / 0.6)
    shake = (math.sin(t * 90) * 10 * U * (1 - boom) * (t > te)) if te is not None and t > te else 0
    power = anim(sp.get('power', 0.4), t)
    boil = anim(sp.get('boil', 0.2), t)
    rods = anim(sp.get('rods', 0.7), t)                       # 0 = all out, 1 = fully in
    # biological shield (concrete) and core
    d.rectangle([x0 - 40 * U + shake, y0 - 20 * U, x1 + 40 * U + shake, y1 + 40 * U], fill=(58, 60, 62))
    hot = min(1.0, power)
    core_col = tuple(int(lerp(a, b, hot)) for a, b in zip((40, 52, 70), (255, 140, 40)))
    d.rectangle([x0 + shake, y0, x1 + shake, y1], fill=(28, 30, 32))
    # fuel channels with water / steam
    n = 13; rng = np.random.default_rng(int(t * 12))
    for i in range(n):
        x = x0 + (i + 0.5) * core_w / n + shake
        d.rectangle([x - 9 * U, y0, x + 9 * U, y1], fill=(40, 70, 110))
        d.rectangle([x - 5 * U, y0 + 10 * U, x + 5 * U, y1 - 10 * U], fill=core_col)
        for b_ in range(int(boil * 7)):
            by = y1 - rng.uniform(0, 1) * core_h * min(1, boil + 0.2); br = rng.uniform(2, 5) * U
            d.ellipse([x + 11 * U - br, by - br, x + 11 * U + br, by + br], outline=(200, 230, 255, 200), width=1)
    # glow over the core
    if power > 0.05:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).rectangle([x0, y0, x1, y1], fill=(255, 120, 30, int(min(255, 140 * power))))
        img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(30 * U + 40 * U * min(power, 3))))
        d = ImageDraw.Draw(img)
    # control rods: absorber (dark) with a graphite tip (lighter) below it
    for i in range(n - 1):
        x = x0 + (i + 1) * core_w / n + shake
        ins = rods if i % 2 == 0 else rods * 0.92
        tip_y = y0 - 60 * U + (core_h + 40 * U) * ins
        d.rectangle([x - 7 * U, top - 40 * U, x + 7 * U, tip_y - 70 * U], fill=(150, 156, 160))
        d.rectangle([x - 7 * U, tip_y - 70 * U, x + 7 * U, tip_y], fill=(95, 95, 92) if not sp.get('tips_hot') else (255, 120, 40))
    # labels
    for lab in sp.get('labels', []):                         # (text, x_frac, y_frac, at, colour)
        txt, fx, fy, at = lab[:4]; col = lab[4] if len(lab) > 4 else WHITE
        put(img, text_img(txt, 'osw', 38, fill=col, track=2), W * fx, H * fy, ease((t - at) / 0.5))
    # power meter (top right)
    if sp.get('meter', True):
        mx, my = W * 0.82, H * 0.2; mw, mh = 46 * U, 520 * U
        d.rectangle([mx, my, mx + mw, my + mh], outline=STEEL, width=int(3 * U))
        f = min(1.0, power / 1.2); col = (90, 200, 120) if power < 0.6 else (AMBER if power < 1.0 else RED)
        d.rectangle([mx + 6 * U, my + mh - (mh - 12 * U) * f - 6 * U, mx + mw - 6 * U, my + mh - 6 * U], fill=col)
        put(img, text_img('POWER', 'osw', 30, fill=STEEL, track=3), mx - 40 * U, my + mh + 6 * U)
    # explosion: lid flips, debris, flash
    if te is not None and t > te:
        lid_y = y0 - 40 * U - 420 * U * boom; ang = 70 * boom
        lid = Image.new('RGBA', (int(core_w + 120 * U), int(50 * U)), (110, 112, 115, 255))
        lid = lid.rotate(ang, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(lid, (int(cx - lid.width / 2), int(lid_y - lid.height / 2)))
        rr = np.random.default_rng(3); d = ImageDraw.Draw(img)
        for _ in range(70):
            a_ = rr.uniform(-2.6, -0.5); v_ = rr.uniform(300, 900) * U; g_ = 600 * U
            tt = t - te; px = cx + math.cos(a_) * v_ * tt; py = y0 + math.sin(a_) * v_ * tt + 0.5 * g_ * tt * tt
            r_ = rr.uniform(3, 9) * U
            d.ellipse([px - r_, py - r_, px + r_, py + r_], fill=(255, int(rr.uniform(90, 200)), 30, 255))
        smoke = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(smoke); tt = t - te
        for k in range(26):                                       # rising smoke column
            u = (k / 26 + tt * 0.08) % 1; ry = y0 - 40 * U - u * 900 * U; rr2 = (60 + 260 * u) * U
            rx = cx + math.sin(k * 1.7 + tt * 0.6) * 60 * U * u
            g = int(40 + 30 * (1 - u)); sd.ellipse([rx - rr2, ry - rr2 * 0.8, rx + rr2, ry + rr2 * 0.8], fill=(g, g, g + 4, int(170 * (1 - u) * min(1, tt / 0.8))))
        img.alpha_composite(smoke.filter(ImageFilter.GaussianBlur(24 * U)))
        fire = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(fire).ellipse([cx - 300 * U, y0 - 260 * U, cx + 300 * U, y0 + 120 * U], fill=(255, 140, 40, int(200 * (1 - 0.5 * boom))))
        img.alpha_composite(fire.filter(ImageFilter.GaussianBlur(60 * U)))
        if sp.get('blue_glow'):
            bl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(bl).ellipse([cx - 120 * U, 0, cx + 120 * U, y0], fill=(110, 160, 255, 150))
            img.alpha_composite(bl.filter(ImageFilter.GaussianBlur(50 * U)))
    return img.convert('RGB')

# ------------------------------------------------------------------ graph
GRAPH = [(0.0, 1600), (0.10, 1600), (0.22, 720), (0.30, 30), (0.42, 160), (0.55, 200), (0.80, 200), (0.86, 260), (0.92, 380), (0.96, 3200), (1.0, 30000)]
GRAPH_T = ['23:10', '00:05', '00:28', '01:00', '01:23:04', '01:23:40']
def draw_graph(sp, t, D):
    img = live_bg(sp, t, D, 'cc0_30', dark=0.62).convert('RGBA'); d = ImageDraw.Draw(img)
    gx0, gy0, gx1, gy1 = W * 0.12, H * 0.16, W * 0.9, H * 0.8
    for i in range(6):
        y = lerp(gy1, gy0, i / 5); d.line([gx0, y, gx1, y], fill=(50, 60, 64), width=1)
        put(img, text_img(f'{int(3200 * i / 5)}', 'mono', 26, fill=STEEL, shadow=False), gx0 - 110 * U, y - 26 * U)
    d.line([gx0, gy0, gx0, gy1], fill=STEEL, width=int(3 * U)); d.line([gx0, gy1, gx1, gy1], fill=STEEL, width=int(3 * U))
    put(img, text_img('REACTOR POWER (MW)', 'osw', 30, fill=STEEL, track=3, shadow=False), gx0 - 30 * U, gy0 - 70 * U)
    upto = anim(sp.get('upto', (0, 1, 0, D * 0.8)), t)
    pts = []
    for (u, mw) in GRAPH:
        if u > upto + 1e-6: break
        pts.append((lerp(gx0, gx1, u), max(gy0 - 120 * U, lerp(gy1, gy0, min(mw, 3800) / 3200))))
    if pts and upto < 1:
        nxt = [g for g in GRAPH if g[0] > upto]
        if nxt:
            (u0, m0), (u1, m1) = [g for g in GRAPH if g[0] <= upto][-1], nxt[0]; f = (upto - u0) / max(1e-6, u1 - u0)
            mw = lerp(m0, m1, f); pts.append((lerp(gx0, gx1, upto), max(gy0 - 120 * U, lerp(gy1, gy0, min(mw, 3800) / 3200))))
    if len(pts) > 1:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).line(pts, fill=AMBER + (255,), width=int(14 * U), joint='curve')
        img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(10 * U))); d = ImageDraw.Draw(img)
        d.line(pts, fill=(255, 225, 150), width=int(5 * U), joint='curve')
        x, y = pts[-1]; d.ellipse([x - 9 * U, y - 9 * U, x + 9 * U, y + 9 * U], fill=WHITE)
    for note in sp.get('notes', []):                   # (u, text, at, colour, dy)
        u, txt, at = note[:3]; col = note[3] if len(note) > 3 else WHITE; dy = note[4] if len(note) > 4 else -1
        a = ease((t - at) / 0.5)
        if a <= 0: continue
        mw = dict(GRAPH).get(u, 200); x = lerp(gx0, gx1, u); y = max(gy0 - 100 * U, lerp(gy1, gy0, min(mw, 3800) / 3200))
        ti = text_img(txt, 'osw', 36, fill=col, track=1); put(img, ti, x - ti.width / 2, y + dy * 80 * U - ti.height / 2, a)
    return img.convert('RGB')

# ------------------------------------------------------------------ dosimeter
def draw_dosimeter(sp, t, D):
    img = live_bg(sp, t, D, 'cc0_36', dark=0.55).convert('RGBA'); d = ImageDraw.Draw(img)
    bx, by, bw, bh = W * 0.3, H * 0.14, W * 0.4, H * 0.72
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=int(30 * U), fill=(52, 66, 50), outline=(20, 26, 20), width=int(6 * U))
    cx, cy, R = bx + bw / 2, by + bh * 0.42, bw * 0.36
    d.pieslice([cx - R, cy - R, cx + R, cy + R], 200, 340, fill=(232, 228, 210))
    for i in range(10):
        a = math.radians(200 + 140 * i / 9)
        d.line([cx + math.cos(a) * R * 0.82, cy + math.sin(a) * R * 0.82, cx + math.cos(a) * R * 0.97, cy + math.sin(a) * R * 0.97], fill=(30, 30, 30), width=int(4 * U))
    for i, lab in enumerate(['0', '1.2', '2.4', '3.6']):
        a = math.radians(200 + 140 * i / 3); ti = text_img(lab, 'osw', 30, fill=(30, 30, 30), shadow=False)
        put(img, ti, cx + math.cos(a) * R * 0.66 - ti.width / 2, cy + math.sin(a) * R * 0.66 - ti.height / 2)
    reading = anim(sp.get('reading', (0, 3.6, 0.2, 1.4)), t)
    jit = math.sin(t * 40) * 0.6 if reading >= 3.55 else 0
    a = math.radians(200 + 140 * min(1, reading / 3.6) + jit)
    d.line([cx, cy, cx + math.cos(a) * R * 0.95, cy + math.sin(a) * R * 0.95], fill=RED, width=int(6 * U))
    d.ellipse([cx - 14 * U, cy - 14 * U, cx + 14 * U, cy + 14 * U], fill=(30, 30, 30))
    lx0, ly0 = bx + bw * 0.15, by + bh * 0.66; d.rectangle([lx0, ly0, bx + bw * 0.85, ly0 + bh * 0.18], fill=(18, 26, 18))
    rev = sp.get('reveal')
    txt = f'{min(reading, 3.6):.1f} R/h' if rev is None or t < rev else sp.get('real', 'THOUSANDS R/h')
    col = (120, 255, 120) if rev is None or t < rev else RED
    ti = text_img(txt, 'mono', 64, fill=col, shadow=False); put(img, ti, cx - ti.width / 2, ly0 + bh * 0.09 - ti.height / 2)
    if reading >= 3.55 and (rev is None or t < rev):
        tl = text_img('MAX', 'osw', 34, fill=RED); put(img, tl, bx + bw * 0.78, by + bh * 0.08, 0.5 + 0.5 * math.sin(t * 8))
    return img.convert('RGB')

# ------------------------------------------------------------------ clock / counter / bars / title
def draw_clock(sp, t, D):
    img = live_bg(sp, t, D, 'cc0_30', dark=0.6).convert('RGBA')
    h0, m0, s0 = sp.get('from', (1, 23, 4)); rate = sp.get('rate', 1.0); stop = sp.get('stop')
    secs = h0 * 3600 + m0 * 60 + s0 + (min(t, stop) if stop is not None else t) * rate
    txt = f'{int(secs // 3600) % 24:02d}:{int(secs // 60) % 60:02d}:{int(secs) % 60:02d}'
    f = font('mono', 230)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).text((W / 2, H * 0.47), txt, font=f, fill=RED + (255,), anchor='mm')
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(18 * U))); img.alpha_composite(lay)
    if sp.get('label'): ti = text_img(sp['label'], 'osw', 44, fill=(255, 200, 190), track=6); put(img, ti, W / 2 - ti.width / 2, H * 0.68, ease(t / 0.6))
    return img.convert('RGB')

def icon(kind, size, col):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im); s = size
    if kind == 'person':
        d.ellipse([s * .35, s * .05, s * .65, s * .35], fill=col); d.rounded_rectangle([s * .25, s * .38, s * .75, s * .95], radius=int(s * .15), fill=col)
    elif kind == 'bus':
        d.rounded_rectangle([s * .05, s * .25, s * .95, s * .75], radius=int(s * .08), fill=col)
        for k in range(4): d.rectangle([s * (.12 + .2 * k), s * .32, s * (.27 + .2 * k), s * .48], fill=(20, 20, 20, 255))
        d.ellipse([s * .18, s * .66, s * .34, s * .82], fill=(20, 20, 20, 255)); d.ellipse([s * .66, s * .66, s * .82, s * .82], fill=(20, 20, 20, 255))
    return im

def draw_counter(sp, t, D):
    img = live_bg(sp, t, D, 'pd_pripyat1984', dark=0.5).convert('RGBA')
    a, b = sp.get('count', (0, 100)); dur = sp.get('cdur', min(2.5, D * 0.6))
    v = lerp(a, b, eout((t - 0.2) / dur)); val = f"{int(round(v)):,}" + sp.get('suffix', '')
    ti = text_img(val, 'head', 250, fill=sp.get('col', AMBER), track=4)
    put(img, ti, W / 2 - ti.width / 2, H * (0.30 if sp.get('icons') else 0.36) - ti.height / 2)
    if sp.get('label'): tl = text_img(sp['label'], 'osw', 50, fill=WHITE, track=5); put(img, tl, W / 2 - tl.width / 2, H * (0.48 if sp.get('icons') else 0.6), ease((t - 0.4) / 0.5))
    if sp.get('icons'):
        kind, n = sp['icons']; cols = 20; size = int(64 * U); shown = int(n * eout((t - 0.3) / dur))
        gx = W / 2 - cols * size * 1.15 / 2
        for i in range(shown):
            r, c = divmod(i, cols); put(img, icon(kind, size, (235, 235, 230, 255)), gx + c * size * 1.15, H * 0.62 + r * size * 1.15)
    return img.convert('RGB')

def draw_bars(sp, t, D):
    img = live_bg(sp, t, D, 'cc0_33', dark=0.58).convert('RGBA'); d = ImageDraw.Draw(img)
    items = sp['bars']; mx = max(v for _, v, *_ in items)
    for i, it in enumerate(items):
        lab, v = it[:2]; col = it[2] if len(it) > 2 else AMBER; at = 0.3 + i * 0.7
        y = H * 0.25 + i * H * 0.2; p = eout((t - at) / 1.0)
        if p <= 0: continue
        bw = (W * 0.62) * (math.log10(v + 1) / math.log10(mx + 1) if sp.get('log') else v / mx) * p
        d.rounded_rectangle([W * 0.3, y, W * 0.3 + max(8 * U, bw), y + 70 * U], radius=int(10 * U), fill=col)
        put(img, text_img(lab, 'osw', 40, fill=WHITE, track=2), W * 0.3 - text_img(lab, 'osw', 40, track=2).width - 10 * U, y - 6 * U, p)
        put(img, text_img(it[3] if len(it) > 3 else f'{v:,}', 'mono', 40, fill=WHITE), W * 0.3 + max(8 * U, bw) + 10 * U, y - 4 * U, p)
    return img.convert('RGB')

def draw_title(sp, t, D):
    img = live_bg(sp, t, D, 'cc0_29', dark=0.5).convert('RGBA')
    a = ease((t - 0.15) / 0.7)
    num = text_img(sp.get('num', ''), 'osw', 40, fill=RED, track=10)
    title = text_img(sp['title'].upper(), 'head', 170, fill=WHITE, track=int(lerp(20, 8, eout(t / 1.5))))
    put(img, num, W / 2 - num.width / 2, H * 0.36 - num.height / 2, a)
    put(img, title, W / 2 - title.width / 2, H * 0.5 - title.height / 2 + (1 - a) * 30 * U, a)
    d = ImageDraw.Draw(img); L = W * 0.18 * eout((t - 0.3) / 0.8)
    d.line([W / 2 - L, H * 0.62, W / 2 + L, H * 0.62], fill=RED + (255,), width=int(4 * U))
    return img.convert('RGB')

# ------------------------------------------------------------------ overlays
def overlays(img, sp, t, dur):
    img = img.convert('RGBA')
    for o in sp.get('ov', []):
        kind, txt = o[0], o[1]; opt = o[2] if len(o) > 2 else {}
        at = opt.get('at', 0.25); a = ease((t - at) / 0.45)
        if kind == 'kw' and 'off' in opt and t > opt['off']: continue
        if kind == 'kw' and opt.get('y', 0.74) > 0.5:    # only the newest bottom keyword is on screen (like the reference)
            later = [o2 for o2 in sp.get('ov', []) if o2[0] == 'kw' and (o2[2] if len(o2) > 2 else {}).get('y', 0.74) > 0.5
                     and at < (o2[2] if len(o2) > 2 else {}).get('at', 0.25) <= t]
            if later: continue
        if 'off' in opt: a *= 1 - ease((t - opt['off']) / 0.4)
        if a <= 0: continue
        if kind in ('quote', 'big') and opt.get('dim', True):
            img.alpha_composite(Image.new('RGBA', img.size, (0, 0, 0, int((150 if kind == 'quote' else 110) * a))))
        if kind == 'kw':            # reference-style keyword: bold white, black outline, pops/types in
            import style
            img = img.convert('RGBA'); style.kw(img, txt, t, at, y=opt.get('y', 0.74), size=opt.get('size', 86), col=opt.get('col', (255, 255, 255)), x=opt.get('x', 0.5))
            continue
        if kind == 'date':          # typewriter date stamp, top-left
            n = int(len(txt) * min(1, (t - at) / 0.8)); ti = text_img(txt[:max(1, n)], 'mono', 46, fill=(255, 230, 200))
            put(img, ti, 60 * U, 50 * U, a)
        elif kind == 'caption':     # lower third with red bar
            ti = text_img(txt, 'body', 40, fill=WHITE, shadow=False)
            bar = Image.new('RGBA', (ti.width + int(24 * U), ti.height - int(20 * U)), (8, 10, 12, 190))
            ImageDraw.Draw(bar).rectangle([0, 0, int(7 * U), bar.height], fill=RED + (255,))
            bar.alpha_composite(ti, (int(18 * U), -int(10 * U)))
            put(img, bar, 70 * U - (1 - a) * 40 * U, H - bar.height - 80 * U, a)
        elif kind == 'label':       # small tag anywhere
            ti = text_img(txt.upper(), 'osw', opt.get('size', 40), fill=opt.get('col', WHITE), track=3)
            put(img, ti, W * opt.get('x', 0.5) - ti.width / 2, H * opt.get('y', 0.15) - ti.height / 2, a)
        elif kind == 'big':
            ti = text_img(txt, 'head', opt.get('size', 190), fill=opt.get('col', AMBER), track=4)
            y = H * opt.get('y', 0.45) - ti.height / 2 + (1 - a) * 26 * U; put(img, ti, W * opt.get('x', 0.5) - ti.width / 2, y, a)
            if opt.get('sub'):
                ts = text_img(opt['sub'].upper(), 'osw', 46, fill=WHITE, track=5, maxw=1500)
                put(img, ts, W * opt.get('x', 0.5) - ts.width / 2, y + ti.height - 60 * U, a)
        elif kind == 'quote':
            ti = text_img('“' + txt + '”', 'serif', 66, fill=WHITE, maxw=1400, spacing=1.3)
            put(img, ti, W / 2 - ti.width / 2, H * opt.get('y', 0.5) - ti.height / 2, a)
            if opt.get('by'):
                tb = text_img('— ' + opt['by'], 'osw', 38, fill=(255, 200, 190), track=3); put(img, tb, W / 2 - tb.width / 2, H * opt.get('y', 0.5) + ti.height / 2, a)
    return img.convert('RGB')

# ------------------------------------------------------------------ scenes
import plan
SCENES = plan.resolve(TIMING)
DRAW = {'photo': draw_photo, 'map': draw_map, 'reactor': draw_reactor, 'graph': draw_graph, 'dosimeter': draw_dosimeter,
        'clock': draw_clock, 'counter': draw_counter, 'bars': draw_bars, 'title': draw_title}

def frame_of(i, t):
    sc = TIMING['scenes'][i]; sp = SCENES[i]; dur = sc['end'] - sc['start']
    tt = t + sp.get('_t0', 0.0); D = dur + sp.get('_t0', 0.0) + sp.get('_tail', 0.0)
    if sp['kind'] == 'three':                                  # pre-rendered real-3D frames (three.js, see three/)
        d3 = os.path.join(OUT, 'three', f'{i + 1:03d}'); fr = sorted(os.listdir(d3)) if os.path.isdir(d3) else []
        k = min(len(fr) - 1, max(0, int(round(t * FPS)))) if fr else 0
        img = Image.open(os.path.join(d3, fr[k])).convert('RGB') if fr else live_bg(sp, tt, D, 'pd_reactor')
        if img.size != (W, H): img = img.resize((W, H), Image.LANCZOS)
    elif sp['kind'] == 'core3d':
        import core3d; img = core3d.draw_core3d(sp, tt, D)
    elif sp['kind'] in ('fire', 'plant'):
        import style; img = (style.draw_fire if sp['kind'] == 'fire' else style.draw_plant)(sp, tt, D)
    else:
        img = DRAW[sp['kind']](sp, tt, D)
    if sp.get('film'):
        import style; img = Image.fromarray(style.film(np.asarray(img, np.float32), tt).astype(np.uint8))
    out = overlays(img, sp, t, dur)
    if os.environ.get('CAPTIONS', '1') == '1':                  # word-by-word captions, bottom centre
        import captions; out = out.convert('RGBA'); captions.draw(out, sc['start'] + t); out = out.convert('RGB')
    return np.asarray(out)

def transition(i, t, a, prev):
    tr = SCENES[i].get('tr', 'fade')
    if prev is None or tr == 'cut': return a
    if tr == 'flash':
        k = t / 0.5
        if k < 1: return a + (255 - a) * (1 - ease(k)) ** 1.5
        return a
    if tr == 'dip':
        if t < 0.5: return a * ease(t / 0.5)
        return a
    if tr == 'glitch' and t < 0.35:
        k = 1 - t / 0.35; out = a.copy(); sh = int(26 * U * k)
        out[..., 0] = np.roll(a[..., 0], sh, axis=1); out[..., 2] = np.roll(a[..., 2], -sh, axis=1)
        rng = np.random.default_rng(int(t * 1000))
        for _ in range(6):
            y = rng.integers(0, H - 40); hh = rng.integers(8, 40); out[y:y + hh] = np.roll(out[y:y + hh], rng.integers(-80, 80), axis=1)
        return prev * (k * 0.5) + out * (1 - k * 0.5)
    if tr == 'push' and t < 0.4:
        k = ease(t / 0.4); return prev * (1 - k) + a * k
    if t < XF:
        k = ease(t / XF); return prev * (1 - k) + a * k
    return a

def render_scene(i):
    sc = TIMING['scenes'][i]
    path = os.path.join(OUT, 'scenes', f'{i + 1:03d}.mp4')
    if os.path.exists(path) and os.environ.get('KEEP'): return path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    nf = int(round(sc['end'] * FPS)) - int(round(sc['start'] * FPS))
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', PRESET, '-crf', CRF, '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    prev = None
    if i > 0 and SCENES[i].get('tr', 'fade') != 'cut':
        ps = TIMING['scenes'][i - 1]; prev = frame_of(i - 1, ps['end'] - ps['start'] - 0.5 / FPS).astype(np.float32)
    for f in range(nf):
        t = f / FPS; a = frame_of(i, t).astype(np.float32)
        a = transition(i, t, a, prev)
        if i == 0 and t < 1.0: a *= ease(t)
        if SCENES[i].get('fadeout'): a *= 1 - ease((t - (nf / FPS - 2.2)) / 2.0)
        p.stdin.write(finish(a, sc['start'] + t).tobytes())
    p.stdin.close(); p.wait()
    print(f'scene {i + 1} done ({nf} frames)', flush=True)
    return path

# ------------------------------------------------------------------ audio
def sfx_track(n, total, sr=48000):
    out = np.zeros(int(total * sr) + sr * 3, np.float32); rng = np.random.default_rng(1)
    def put_(sig, t):
        k = int(t * sr); e = min(len(out), k + len(sig))
        if k < len(out): out[k:e] += sig[:e - k]
    def boom():
        m = int(3.2 * sr); tt = np.arange(m) / sr
        s = np.sin(2 * np.pi * (38 + 50 * np.exp(-tt * 5)) * tt) * np.exp(-tt * 1.6)
        s += rng.normal(0, 1, m) * np.exp(-tt * 4) * 0.35
        return (s * 0.55).astype(np.float32)
    def whoosh():
        m = int(0.8 * sr); x = rng.normal(0, 1, m).astype(np.float32)
        from scipy.signal import butter, lfilter
        b, a = butter(2, [400 / (sr / 2), 3000 / (sr / 2)], 'band'); x = lfilter(b, a, x)
        return (x * np.sin(np.linspace(0, np.pi, m)) ** 2 * 0.12).astype(np.float32)
    def geiger(dur, rate):
        m = int(dur * sr); s = np.zeros(m, np.float32)
        for t0 in np.cumsum(rng.exponential(1 / rate, int(dur * rate * 2) + 5)):
            k = int(t0 * sr)
            if k >= m - 200: break
            s[k:k + 120] += (rng.normal(0, 1, 120) * np.exp(-np.arange(120) / 18)).astype(np.float32) * 0.22
        return s * np.minimum(1, np.minimum(np.arange(m) / (0.3 * sr), (m - np.arange(m)) / (0.3 * sr)))
    def alarm(dur):
        m = int(dur * sr); tt = np.arange(m) / sr
        f = 700 + 300 * (np.sin(2 * np.pi * 1.6 * tt) > 0)
        return (np.sign(np.sin(2 * np.pi * np.cumsum(f) / sr)) * 0.035 * np.minimum(1, tt / 0.2)).astype(np.float32)
    def tick():
        m = int(0.05 * sr); return (rng.normal(0, 1, m) * np.exp(-np.arange(m) / 60) * 0.15).astype(np.float32)
    B, Wh = boom(), whoosh()
    for i in range(n):
        sp = SCENES[i]; st = TIMING['scenes'][i]['start']; dur = TIMING['scenes'][i]['end'] - st
        if sp.get('_t0', 0) > 0: continue
        for s in sp.get('sfx', []):
            kind, at = s[0], s[1]
            if kind == 'boom': put_(B, st + at)
            elif kind == 'whoosh': put_(Wh, st + at)
            elif kind == 'geiger': put_(geiger(s[2] if len(s) > 2 else dur, s[3] if len(s) > 3 else 12), st + at)
            elif kind == 'alarm': put_(alarm(s[2] if len(s) > 2 else dur), st + at)
            elif kind == 'tick':
                for k in range(int(s[2] if len(s) > 2 else dur)): put_(tick(), st + at + k)
        if sp.get('tr') in ('push', 'glitch'): put_(Wh, max(0, st - 0.25))
        if sp.get('kind') == 'title': put_(Wh * 1.3, max(0, st - 0.2))
    return out

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'preview'
    n = len(TIMING['scenes'])
    if mode == 'still':
        i = int(sys.argv[2]) - 1; sc = TIMING['scenes'][i]; tt = float(sys.argv[3]) if len(sys.argv) > 3 else (sc['end'] - sc['start']) * 0.7
        Image.fromarray(finish(frame_of(i, tt).astype(np.float32), tt)).save(os.path.join(OUT, f'still_{i + 1:03d}.jpg'), quality=90); return
    if mode == 'preview':
        lim = float(sys.argv[2]) if len(sys.argv) > 2 else 125
        n = len([s for s in TIMING['scenes'] if s['start'] < lim]); name = 'Chernobyl_Preview.mp4'
    else:
        name = 'Chernobyl.mp4'
    total = TIMING['scenes'][n - 1]['end']
    with Pool(int(os.environ.get('WORKERS', 4))) as pool:
        paths = pool.map(render_scene, range(n), chunksize=1)
    lst = os.path.join(OUT, 'concat.txt'); open(lst, 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in paths))
    sfx = sfx_track(n, total)
    with wave.open(os.path.join(OUT, 'sfx.wav'), 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(48000); wf.writeframes((np.clip(sfx, -1, 1) * 32767).astype(np.int16).tobytes())
    out = os.path.join(OUT, name)
    fc = (f'[1:a]atrim=0:{total},asplit=2[v][vk];[2:a]atrim=0:{total}[s];'
          f'[3:a]atrim=0:{total},volume=0.30[m0];[m0][vk]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=500[m];'
          f'[v][s][m]amix=inputs=3:normalize=0:duration=first,afade=t=out:st={total - 2.5}:d=2.5,alimiter=limit=0.95[a]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-i', os.path.join(OUT, 'narration.wav'),
                    '-i', os.path.join(OUT, 'sfx.wav'), '-i', os.path.join(OUT, 'music.wav'), '-filter_complex', fc,
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', str(total), '-movflags', '+faststart', out], check=True)
    print('wrote', out, round(total, 1), 's')

if __name__ == '__main__':
    main()
