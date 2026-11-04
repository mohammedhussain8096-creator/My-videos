"""Renders the Russia video in the reference video's style: dark satellite map, orange-red country fills
with a glowing edge, year tag top-left, drifting cartoon clouds, small icons/pins dropping onto places,
progressive army arrows and big yellow punch captions; the user's character stands bottom-right as the guide.

python3 render.py                 -> build/Russia_Most_Powerful_Nation.mp4 (every scene)
python3 render.py preview 125     -> build/Russia_Preview.mp4 (scenes that start before 125 s)
Env: RES=1280x720, WORKERS=4"""
import json, math, os, subprocess, sys, wave
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import icons
from render_text import text_img, font
from plan import SCENES, PLACES, VIEWS, GROUPS

ASSETS = os.environ.get('RU_ASSETS', os.path.join(HERE, 'assets'))
OUT = os.environ.get('OUT_DIR', os.path.join(HERE, 'build'))
W, H = map(int, os.environ.get('RES', '1920x1080').split('x'))
U = W / 1920.0
FPS = 24
Image.MAX_IMAGE_PIXELS = None

COLORS = {'red': (226, 74, 30), 'blue': (40, 112, 232), 'grey': (160, 160, 165), 'green': (60, 170, 80),
          'yellow': (240, 190, 40), 'dark': (50, 50, 55), 'purple': (140, 80, 190), 'white': (235, 235, 235)}
YELLOW_TOP, YELLOW_BOT = (255, 232, 92), (250, 168, 28)
CAP_STROKE = (74, 38, 8)

# ---------------------------------------------------------------- map projection
MJ = json.load(open(os.path.join(ASSETS, 'world_merc.json')))
PXD = MJ['W'] / (MJ['lon1'] - MJ['lon0'])

def merc(lat):
    lat = max(-85, min(85, lat))
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))

def ll2m(lat, lon):
    """lat/lon -> map image pixel"""
    if lon < MJ['lon0']: lon += 360
    return (lon - MJ['lon0']) * PXD, (merc(MJ['lat1']) - merc(lat)) * MJ['ky']

def place(p):
    if isinstance(p, str): return PLACES[p]
    return p

def view_of(v):
    """view name or (lat, lon, width_deg) -> (cx, cy, width_px) in map pixels"""
    if isinstance(v, str): v = VIEWS[v]
    lat, lon, wd = v
    cx, cy = ll2m(lat, lon)
    return (cx, cy, wd * PXD)

_MAPS = None
def maps():
    global _MAPS
    if _MAPS is None:
        m = Image.open(os.path.join(ASSETS, 'world_merc.jpg')); m.load()
        lv = [m]
        for _ in range(3):
            lv.append(lv[-1].resize((lv[-1].width // 2, lv[-1].height // 2), Image.BILINEAR))
        _MAPS = lv
    return _MAPS

def crop_map(cx, cy, wpx):
    hpx = wpx * H / W
    lv = maps()
    k = 0
    while k + 1 < len(lv) and wpx / 2 ** (k + 1) > W * 1.15: k += 1
    m, f = lv[k], 2 ** k
    box = ((cx - wpx / 2) / f, (cy - hpx / 2) / f, (cx + wpx / 2) / f, (cy + hpx / 2) / f)
    return m.resize((W, H), Image.BICUBIC if k == 0 else Image.BILINEAR, box=box)

# ---------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_back(x):
    x = clamp(x); c = 1.9
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

# ---------------------------------------------------------------- timing helpers
TIMING = json.load(open(os.path.join(OUT, 'timing.json')))
ENV = TIMING['envelope']

def syl(w):
    import re
    w = re.sub(r'[^a-z0-9]', '', w.lower())
    if not w: return 1
    if w.isdigit(): return max(2, len(w))
    g = len(re.findall(r'[aeiouy]+', w))
    if w.endswith('e') and g > 1: g -= 1
    return max(1, g)

def word_times(sc):
    """[(word, t_rel)] for the words of a scene, from phrase timings (syllable-weighted)."""
    out = []
    for ph in TIMING['phrases']:
        if ph['start'] < sc['start'] - 0.05 or ph['start'] >= sc['end'] - 0.05: continue
        ws = ph['text'].split(); ss = [syl(w) for w in ws]; tot = sum(ss); acc = 0
        for w, s in zip(ws, ss):
            out.append((w, ph['start'] + (ph['end'] - ph['start']) * acc / tot - sc['start']))
            acc += s
    return out

def resolve_t(at, sc, wt):
    """at: None | float (0..1 = fraction, >1 = seconds) | 'word' (first word starting with it)"""
    dur = sc['end'] - sc['start']
    if at is None: return 0.25
    if isinstance(at, (int, float)): return at * dur if at <= 1 else float(at)
    key = at.lower()
    nth = 1
    if '#' in key: key, nth = key.split('#'); nth = int(nth)
    for w, t in wt:
        if w.lower().strip('.,;:!?"\'').startswith(key.strip('.,;:!?"\'')):
            nth -= 1
            if nth == 0: return max(0.0, t - 0.05)
    print('  ! word not found:', at, 'in scene', sc['scene']); return 0.3 * dur

# ---------------------------------------------------------------- static layers
_STATIC = {}
def vignette():
    if 'vig' not in _STATIC:
        y, x = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
        _STATIC['vig'] = np.clip(1.0 - 0.38 * np.clip(r - 0.55, 0, None) ** 1.5, 0.45, 1)[..., None]
    return _STATIC['vig']

def cloud_sprite(i):
    key = ('cloud', i)
    if key not in _STATIC:
        rng = np.random.default_rng(i + 3)
        cw, ch = int(360 * U), int(170 * U)
        im = Image.new('RGBA', (cw * 2, ch * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        blobs = [(0.18, 0.66, 0.16), (0.36, 0.5, 0.24), (0.58, 0.42, 0.28), (0.78, 0.6, 0.18), (0.5, 0.68, 0.2), (0.9, 0.74, 0.1), (0.06, 0.8, 0.07)]
        for bx, by, br in blobs:
            bx += rng.uniform(-0.03, 0.03); r = br * cw * 2 * 0.55
            d.ellipse([bx * cw * 2 - r, by * ch * 2 - r * 0.9, bx * cw * 2 + r, by * ch * 2 + r * 0.9], fill=(255, 255, 255, 255))
        a = im.getchannel('A')
        # shading: grey underside
        y = np.linspace(0, 1, ch * 2)[:, None]
        sh = (np.asarray(a, np.float32) / 255)
        col = np.zeros((ch * 2, cw * 2, 4), np.float32)
        tone = 255 - 70 * np.clip((y - 0.45) / 0.5, 0, 1)
        col[..., 0] = tone; col[..., 1] = tone; col[..., 2] = tone + 8 * (y > 0.5)
        col[..., 3] = sh * 255
        im = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8), 'RGBA').resize((cw, ch), Image.LANCZOS)
        shadow = Image.new('RGBA', (cw + 30, ch + 40), (0, 0, 0, 0))
        shadow.paste((0, 0, 0, 90), (12, 26), im.getchannel('A'))
        shadow = shadow.filter(ImageFilter.GaussianBlur(10 * U)); shadow.alpha_composite(im, (0, 0))
        _STATIC[key] = shadow
    return _STATIC[key]

CLOUDS = [  # (sprite, y fraction, speed px/s, phase px, scale)
    (0, 0.83, 9, 100, 0.85), (1, 0.9, 12, 900, 1.0), (2, 0.12, 7, 1500, 0.6), (0, 0.6, 5, 2300, 0.55), (1, 0.95, 10, 1900, 0.7)]

def draw_clouds(fr, gt, amount=1.0):
    if amount <= 0: return
    span = W + 800 * U
    for i, (sp, yf, spd, ph, sc) in enumerate(CLOUDS[: max(1, int(round(len(CLOUDS) * amount)))]):
        im = cloud_sprite(sp)
        if sc != 1: im = scaled(im, sc)
        x = (ph * U + spd * U * gt) % span - 400 * U
        fr.alpha_composite(im, (int(x), int(yf * H - im.height / 2)))

_SCALED = {}
def scaled(im, k):
    key = (id(im), round(k, 3))
    if key not in _SCALED:
        if len(_SCALED) > 2000: _SCALED.clear()
        _SCALED[key] = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
    return _SCALED[key]

def guide_img():
    if 'guide' not in _STATIC:
        g = Image.open(os.path.join(ASSETS, 'guide.png')).convert('RGBA')
        h = int(400 * U)
        _STATIC['guide'] = g.resize((int(g.width * h / g.height), h), Image.LANCZOS)
    return _STATIC['guide']

def year_tag(text):
    key = ('year', text)
    if key not in _STATIC:
        f = font('nunito', int(34 * U))
        l, t, r, b = f.getbbox(text)
        pw, ph = r - l + int(36 * U), int(56 * U)
        im = Image.new('RGBA', (pw + 8, ph + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([3, 3, pw + 3, ph + 3], radius=int(12 * U), fill=(28, 28, 30, 225), outline=(235, 235, 235, 255), width=max(2, int(3 * U)))
        d.text((3 + (pw - (r - l)) / 2 - l, 3 + (ph - (b - t)) / 2 - t), text, font=f, fill=(255, 255, 255))
        _STATIC[key] = im
    return _STATIC[key]

def label_img(text, size=30, color=(255, 255, 255)):
    return text_img(text, 'nunito', int(size * U), color, (25, 20, 18), max(2, int(5 * U)))

def pill_img(text, size=22):
    key = ('pill', text, size)
    if key not in _STATIC:
        f = font('nunito', int(size * U))
        l, t, r, b = f.getbbox(text)
        pw, ph = r - l + int(24 * U), b - t + int(14 * U)
        im = Image.new('RGBA', (pw + 4, ph + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([2, 2, pw + 2, ph + 2], radius=ph // 2, fill=(25, 25, 30, 235), outline=(240, 240, 240, 255), width=max(2, int(2 * U)))
        d.text((2 + int(12 * U) - l, 2 + int(7 * U) - t), text, font=f, fill=(255, 255, 255))
        _STATIC[key] = im
    return _STATIC[key]

# ---------------------------------------------------------------- country polygons
_POLY = None
def polys(name):
    global _POLY
    if _POLY is None: _POLY = json.load(open(os.path.join(ASSETS, 'countries.json')))
    out = []
    for n in GROUPS.get(name, [name]):
        if n not in _POLY: print('  ! unknown country', n); continue
        for ring in _POLY[n]:
            out.append([ll2m(lat, lon) for lon, lat in ring])
    return out

_PROJ = {}
def proj_rings(name):
    if name not in _PROJ: _PROJ[name] = [np.array(r, np.float64) for r in polys(name)]
    return _PROJ[name]

def to_screen_arr(a, cam):
    cx, cy, w = cam; s = W / w
    return (a[:, 0] - cx) * s + W / 2, (a[:, 1] - cy) * s + H / 2

def to_screen(p, cam):
    mx, my = ll2m(*place(p))
    cx, cy, w = cam; s = W / w
    return (mx - cx) * s + W / 2, (my - cy) * s + H / 2

def draw_fills(fr, cam, fills):
    """fills: list of (country/group, colour name, alpha 0..1). Fill shows the terrain through it,
    with a light glowing edge (reference style)."""
    if not fills: return fr
    hw, hh = W // 2, H // 2
    arr = np.asarray(fr).astype(np.float32)
    lum = arr.mean(axis=2, keepdims=True) / 255.0
    bycol = {}
    for name, col, a in fills:
        if a <= 0.001: continue
        m = Image.new('L', (hw, hh), 0); d = ImageDraw.Draw(m)
        for r in proj_rings(name):
            x, y = to_screen_arr(r, cam)
            if x.max() < -50 or x.min() > W + 50 or y.max() < -50 or y.min() > H + 50: continue
            if len(x) > 3: d.polygon(list(zip((x / 2).tolist(), (y / 2).tolist())), fill=255)
        bycol.setdefault((col, round(a, 3)), []).append(m)
    for (col, a), ms in bycol.items():
        m = ms[0]
        for o in ms[1:]: m = ImageChops.lighter(m, o)
        edge = ImageChops.subtract(m.filter(ImageFilter.MaxFilter(3)), m.filter(ImageFilter.MinFilter(3)))
        glow = edge.filter(ImageFilter.GaussianBlur(5))
        mf = np.asarray(m.resize((W, H), Image.BILINEAR), np.float32)[..., None] / 255.0 * a
        ef = np.asarray(edge.resize((W, H), Image.BILINEAR), np.float32)[..., None] / 255.0 * a
        gf = np.asarray(glow.resize((W, H), Image.BILINEAR), np.float32)[..., None] / 255.0 * a
        c = np.array(COLORS[col], np.float32)
        tinted = c * (0.62 + 0.75 * lum)
        arr = arr * (1 - 0.82 * mf) + tinted * 0.82 * mf
        light = np.minimum(c * 0.5 + 150, 255)
        arr = arr * (1 - 0.9 * ef) + light * 0.9 * ef
        arr = arr + gf * c * 0.9
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

# ---------------------------------------------------------------- arrows
def catmull(pts, n=24):
    if len(pts) < 3:
        (x0, y0), (x1, y1) = pts[0], pts[-1]
        return [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n + 1)]
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in range(2)))
    out.append(pts[-1])
    return out

def partial(path, p):
    if p >= 1: return path
    L = [0.0]
    for a, b in zip(path, path[1:]): L.append(L[-1] + math.dist(a, b))
    tgt = L[-1] * p
    out = [path[0]]
    for i in range(1, len(path)):
        if L[i] <= tgt: out.append(path[i])
        else:
            a, b = path[i - 1], path[i]; k = (tgt - L[i - 1]) / max(1e-6, L[i] - L[i - 1])
            out.append((a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)); break
    return out

def point_at(path, p):
    pp = partial(path, clamp(p))
    a, b = pp[-2] if len(pp) > 1 else pp[0], pp[-1]
    return b, math.atan2(b[1] - a[1], b[0] - a[0])

def draw_arrow(layer, path, p, col, width=26, alpha=215):
    if p <= 0.001 or len(path) < 2: return
    pp = partial(path, p)
    if len(pp) < 2: return
    d = ImageDraw.Draw(layer)
    w = int(width * U)
    c = COLORS[col]
    tip, ang = pp[-1], math.atan2(pp[-1][1] - pp[-2][1], pp[-1][0] - pp[-2][0])
    hl = w * 1.6
    body = partial(pp, 1) if len(pp) < 3 else pp
    # shorten body under the head
    bx = (tip[0] - math.cos(ang) * hl * 0.6, tip[1] - math.sin(ang) * hl * 0.6)
    body = body[:-1] + [bx]
    head = [(tip[0] + math.cos(ang) * hl * 0.4, tip[1] + math.sin(ang) * hl * 0.4),
            (bx[0] + math.cos(ang + 1.75) * w * 1.15, bx[1] + math.sin(ang + 1.75) * w * 1.15),
            (bx[0] + math.cos(ang - 1.75) * w * 1.15, bx[1] + math.sin(ang - 1.75) * w * 1.15)]
    d.line(body, fill=(255, 255, 255, 235), width=w + int(8 * U), joint='curve')
    d.polygon(head, fill=(255, 255, 255, 235))
    head_in = [(tip[0] + math.cos(ang) * hl * 0.26, tip[1] + math.sin(ang) * hl * 0.26),
               (bx[0] + math.cos(ang + 1.9) * w * 0.92, bx[1] + math.sin(ang + 1.9) * w * 0.92),
               (bx[0] + math.cos(ang - 1.9) * w * 0.92, bx[1] + math.sin(ang - 1.9) * w * 0.92)]
    d.line(body, fill=c + (alpha,), width=w, joint='curve')
    d.polygon(head_in, fill=c + (alpha,))
    for q in (body[0], body[-1]):
        r = w / 2; d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=c + (alpha,))

# ---------------------------------------------------------------- caption / title
def caption_imgs(small, big):
    sm = text_img(small, 'luckiest', int(44 * U), (255, 255, 255), CAP_STROKE, max(3, int(6 * U))) if small else None
    bg = text_img(big, 'luckiest', int(104 * U), None, CAP_STROKE, max(4, int(9 * U)), gradient=(YELLOW_TOP, YELLOW_BOT)) if big else None
    return sm, bg

def paste_center(fr, im, cx, cy, k=1.0, alpha=1.0):
    if im is None: return
    if abs(k - 1) > 0.01: im = scaled(im, k)
    if alpha < 0.999:
        im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * alpha)))
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

def fmt_count(big, p):
    import re
    m = re.search(r'\d[\d,]*', big)
    if not m or p >= 1: return big
    n = int(m.group(0).replace(',', ''))
    v = int(n * ease_out(p))
    s = f'{v:,}' if ',' in m.group(0) else str(v)
    return big[:m.start()] + s + big[m.end():]

# ---------------------------------------------------------------- scene planning
class Scene:
    def __init__(self, sc, spec, prev):
        self.sc, self.spec, self.prev = sc, spec, prev
        self.dur = sc['end'] - sc['start']
        self.wt = word_times(sc)
        T = lambda at: resolve_t(at, sc, self.wt)
        self.T = T
        v = spec.get('view', prev.spec.get('view', 'europe') if prev else 'europe')
        self.target = view_of(v)
        z = spec.get('zoom', 0.05)
        self.cam_end = (self.target[0], self.target[1], self.target[2] * (1 - z))
        self.cam_from = prev.cam_end if prev else self.target
        moves = spec.get('moves', [])   # [(at, view, zoom)] camera moves inside the scene
        self.moves = [(T(at), view_of(vv)) for at, vv in moves]
        if self.moves: self.cam_end = (self.moves[-1][1][0], self.moves[-1][1][1], self.moves[-1][1][2] * (1 - z * 0.5))
        same = self.cam_from == self.target
        self.cam_in = 0.0 if same else min(1.3, 0.35 * self.dur)
        self.year = spec.get('year', prev.year_end if prev else None)
        self.years = [(T(at), y) for at, y in spec.get('years', [])]
        self.year_end = self.years[-1][1] if self.years else self.year
        self.snow_t = T(spec['snow_at']) if 'snow_at' in spec else -9
        self.bg = spec.get('bg', 'map')
        # fills carry over without re-animating if the previous scene had them
        prev_f = {f[0]: f for f in (prev.fills if prev else [])} if (prev and prev.bg == 'map') else {}
        self.fills = []
        for f in spec.get('fill', []):
            name, col = f[0], f[1]
            at = f[2] if len(f) > 2 else None
            t0 = -9 if (name in prev_f and prev_f[name][1] == col and at is None) else T(at if at is not None else 0.05)
            self.fills.append((name, col, t0))
        for f in spec.get('unfill', []):     # fade out a carried fill
            self.fills = [(x[0], x[1], x[2], T(f[1])) if x[0] == f[0] else x for x in self.fills]
        prev_items = {it.get('id') for it in (prev.items if prev else []) if it.get('id')}
        self.items = []
        for it in spec.get('items', []):
            it = dict(it)
            it['t0'] = -9 if (it.get('id') in prev_items and 'at' not in it) else T(it.get('at'))
            if 'to' in it: it['t1'] = T(it['to'])
            if 'off' in it: it['toff'] = T(it['off'])
            self.items.append(it)
        self.caps = []
        for c in spec.get('cap', []):
            small, big = c[0], c[1]
            at = c[2] if len(c) > 2 else None
            opt = c[3] if len(c) > 3 else {}
            self.caps.append({'small': small, 'big': big, 't0': T(at if at is not None else 0.12), 'opt': opt})
        for i, c in enumerate(self.caps):
            c['t1'] = self.caps[i + 1]['t0'] if i + 1 < len(self.caps) else self.dur + 1
        self.title = spec.get('title')
        self.tint = spec.get('tint')
        self.guide = spec.get('guide', True)
        self.clouds = spec.get('clouds', 1.0 if self.bg == 'map' else 0)
        self.sfx = []
        if self.cam_in > 0: self.sfx.append(('whoosh', 0.0))
        for it in self.items:
            if it['t0'] >= 0: self.sfx.append(('pop' if it['k'] not in ('arrow', 'move') else 'swish', it['t0']))
        for c in self.caps: self.sfx.append(('hit', c['t0']))
        for ty, _ in self.years: self.sfx.append(('pop', ty))
        if self.title: self.sfx.append(('hit', T(self.title.get('at', 0.05))))

    def cam(self, t):
        a = self.cam_from; b = self.target
        if self.cam_in > 0 and t < self.cam_in:
            k = ease(t / self.cam_in)
            wl = math.exp(math.log(a[2]) * (1 - k) + math.log(b[2]) * k)
            # zoom out a little mid-flight when travelling far
            dist = math.hypot(b[0] - a[0], b[1] - a[1]) / max(a[2], b[2])
            wl *= 1 + 0.35 * clamp(dist - 0.3) * math.sin(math.pi * k)
            return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, wl)
        cur = b
        for tm, v in self.moves:
            if t >= tm:
                k = ease((t - tm) / 1.4)
                cur = (cur[0] + (v[0] - cur[0]) * k, cur[1] + (v[1] - cur[1]) * k, math.exp(math.log(cur[2]) * (1 - k) + math.log(v[2]) * k))
        z = self.spec.get('zoom', 0.05)
        p = clamp((t - self.cam_in) / max(0.1, self.dur - self.cam_in))
        return (cur[0], cur[1], cur[2] * (1 - z * ease(p) * (0.5 if self.moves else 1)))

    # -------------------------------------------------------------- frame
    def frame(self, t):
        gt = self.sc['start'] + t
        cam = self.cam(t)
        if self.bg == 'black':
            fr = Image.new('RGB', (W, H), (8, 8, 10))
        else:
            fr = crop_map(*cam)
            fills = []
            for f in self.fills:
                name, col, t0 = f[:3]
                a = ease((t - t0) / 0.6)
                if len(f) > 3: a *= 1 - ease((t - f[3]) / 0.6)
                fills.append((name, col, a))
            fr = draw_fills(fr, cam, fills)
            arr = np.asarray(fr).astype(np.float32)
            if self.tint == 'night':
                arr *= np.array([0.42, 0.48, 0.7])
            elif self.tint == 'fire':
                arr = arr * np.array([0.65, 0.5, 0.42]) + np.array([40, 12, 0])
            elif self.tint == 'winter':
                g = arr.mean(axis=2, keepdims=True); arr = (arr * 0.35 + g * 0.65) * np.array([0.95, 1.0, 1.1]) + 18
            arr *= vignette()
            fr = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        fr = fr.convert('RGBA')
        layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        for it in self.items:
            if it['k'] == 'arrow':
                path = catmull([to_screen(p, cam) for p in it['path']])
                t1 = it.get('t1', it['t0'] + 1.6)
                p = 1.0 if it['t0'] < 0 else ease((t - it['t0']) / max(0.1, t1 - it['t0']))
                a = 1.0
                if 'toff' in it: a = 1 - ease((t - it['toff']) / 0.5)
                if a > 0: draw_arrow(layer, path, p, it.get('color', 'blue'), it.get('w', 26), int(215 * a))
        fr.alpha_composite(layer)
        if self.tint == 'night' or self.spec.get('stars'):
            self.stars(fr, gt)
        for it in self.items:
            if it['k'] != 'arrow': self.draw_item(fr, it, t, cam, gt)
        if self.spec.get('snow') and t >= self.snow_t: self.snow(fr, gt, self.spec['snow'] * clamp((t - self.snow_t) / 1.0))
        draw_clouds(fr, gt, self.clouds)
        yr = self.year
        for ty, y in self.years:
            if t >= ty: yr = y
        if yr and self.bg == 'map':
            fr.alpha_composite(year_tag(yr), (int(48 * U), int(34 * U)))
        if self.title: self.draw_title(fr, t)
        for c in self.caps: self.draw_cap(fr, c, t)
        if self.guide: self.draw_guide(fr, gt, t)
        return fr.convert('RGB')

    def draw_item(self, fr, it, t, cam, gt):
        k = it['k']; t0 = it['t0']
        if t < t0: return
        age = t - t0
        a = 1.0
        if 'toff' in it:
            if t > it['toff'] + 0.4: return
            a = 1 - clamp((t - it['toff']) / 0.4)
        pop = 1.0 if t0 < 0 else ease_back(age / 0.45)
        if k == 'move':
            path = catmull([to_screen(p, cam) for p in it['path']])
            t1 = it.get('t1', t0 + 2.5)
            p = 1.0 if t0 < 0 else ease((t - t0) / max(0.1, t1 - t0)) if not it.get('linear') else clamp((t - t0) / max(0.1, t1 - t0))
            (x, y), _ = point_at(path, p)
            im = icons.get(it['icon'], int(it.get('s', 70) * U))
            paste_center(fr, im, x, y - im.height * 0.3, 1.0, a)
            return
        x, y = to_screen(it['at_place'], cam) if 'at_place' in it else (it['xy'][0] * W, it['xy'][1] * H)
        dx, dy = it.get('dx', 0) * U, it.get('dy', 0) * U
        x += dx; y += dy
        if k == 'icon':
            s = int(it.get('s', 70) * U)
            kind = it['icon']
            if kind == 'flame':
                im = icons.flame(s, (gt * 2.3 + x * 0.01) % 1)
                fl = 1 + 0.06 * math.sin(gt * 13 + x)
                paste_center(fr, im, x, y - s * 0.4 * pop, pop * fl, a)
            else:
                im = icons.get(kind, s)
                drop = (1 - ease_out(age / 0.35)) * 60 * U if t0 >= 0 and it.get('drop', True) else 0
                bob = math.sin(gt * 2.2 + x * 0.02) * 3 * U if it.get('bob', False) else 0
                paste_center(fr, im, x, y - im.height * 0.5 - drop + bob, pop if not it.get('drop', True) else 1.0, a * clamp(age / 0.15 if t0 >= 0 else 1))
            if it.get('label'):
                lim = pill_img(it['label'], it.get('ls', 22)) if it.get('pill', True) else label_img(it['label'], it.get('ls', 30))
                paste_center(fr, lim, x, y + lim.height * 0.75, pop, a)
        elif k == 'label':
            lim = label_img(it['text'], it.get('s', 30), tuple(it.get('color', (255, 255, 255))))
            paste_center(fr, lim, x, y, pop, a)
        elif k == 'city':          # white dot + name
            r = 7 * U * pop
            d = ImageDraw.Draw(fr)
            d.ellipse([x - r - 2, y - r - 2, x + r + 2, y + r + 2], fill=(30, 30, 30, 255)); d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 255))
            if it.get('text'):
                lim = label_img(it['text'], it.get('s', 28))
                paste_center(fr, lim, x, y + (24 if it.get('below', True) else -26) * U, pop, a)
        elif k == 'xmark':
            paste_center(fr, icons.get('xmark', int(it.get('s', 56) * U)), x, y, 1.6 - 0.6 * ease_out(age / 0.25) if t0 >= 0 else 1, a)
        elif k == 'ring':          # pulsing ring on a place
            d = ImageDraw.Draw(fr)
            for j in range(2):
                ph = ((age * 0.8 + j * 0.5) % 1)
                r = (20 + 60 * ph) * U
                d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 255, 255, int(220 * (1 - ph) * a)), width=max(2, int(4 * U)))
        elif k == 'fire':          # cluster of flames + glow at a place
            glow = Image.new('RGBA', (int(260 * U), int(260 * U)), (0, 0, 0, 0))
            ImageDraw.Draw(glow).ellipse([glow.width * 0.27, glow.height * 0.27, glow.width * 0.73, glow.height * 0.73], fill=(255, 120, 30, 150))
            glow = scaled_blur(glow)
            gk = clamp(age / 0.6) * (1 + 0.08 * math.sin(gt * 9))
            paste_center(fr, glow, x, y, gk * it.get('size', 1.0), a)
            for j, (ox, oy, sc) in enumerate(((-26, 6, 0.8), (22, 2, 0.9), (0, -12, 1.1), (-6, 18, 0.7), (34, 18, 0.6))[: it.get('n', 4)]):
                if age < j * 0.15: continue
                s = int(56 * U * sc * it.get('size', 1.0))
                im = icons.flame(s, (gt * 2.5 + j * 0.37) % 1)
                paste_center(fr, im, x + ox * U * it.get('size', 1.0), y + oy * U - s * 0.4, ease_back((age - j * 0.15) / 0.4) * (1 + 0.07 * math.sin(gt * 11 + j)), a)
        elif k == 'counter':
            pass

    def stars(self, fr, gt):
        if 'stars' not in _STATIC:
            rng = np.random.default_rng(5)
            _STATIC['stars'] = [(rng.uniform(0, W), rng.uniform(0, H * 0.8), rng.uniform(1, 2.6) * U, rng.uniform(0, 6)) for _ in range(90)]
        d = ImageDraw.Draw(fr)
        for x, y, r, ph in _STATIC['stars']:
            a = int(140 + 100 * math.sin(gt * 1.7 + ph))
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))

    def snow(self, fr, gt, amount):
        if 'snowp' not in _STATIC:
            rng = np.random.default_rng(9)
            _STATIC['snowp'] = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(1.5, 4.5) * U, rng.uniform(30, 90) * U, rng.uniform(0, 6)) for _ in range(260)]
        d = ImageDraw.Draw(fr)
        n = int(len(_STATIC['snowp']) * clamp(amount))
        for x, y, r, v, ph in _STATIC['snowp'][:n]:
            yy = (y + v * gt) % H; xx = (x + 25 * U * math.sin(gt * 0.8 + ph)) % W
            d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=(255, 255, 255, 210))

    def draw_title(self, fr, t):
        ti = self.title
        t0 = self.T(ti.get('at', 0.05))
        if t < t0: return
        k = ease_out((t - t0) / 0.5)
        dim = Image.new('RGBA', (W, H), (0, 0, 0, int(110 * k)))
        fr.alpha_composite(dim)
        sm = text_img(ti.get('small', ''), 'nunito', int(30 * U), (235, 235, 235), (20, 20, 20), max(2, int(4 * U))) if ti.get('small') else None
        bg = text_img(ti['big'], 'luckiest', int(ti.get('size', 120) * U), None, CAP_STROKE, max(4, int(9 * U)), gradient=(YELLOW_TOP, YELLOW_BOT)) if ti.get('style', 'yellow') == 'yellow' else \
            text_img(ti['big'], 'luckiest', int(ti.get('size', 120) * U), (255, 255, 255), (20, 20, 20), max(4, int(8 * U)))
        cy = H * ti.get('y', 0.46)
        sc = 1.25 - 0.25 * ease_back((t - t0) / 0.4)
        paste_center(fr, bg, W / 2, cy, sc, k)
        if sm: paste_center(fr, sm, W / 2, cy - bg.height * 0.58, 1, k)

    def draw_cap(self, fr, c, t):
        if t < c['t0'] or t > c['t1']: return
        age = t - c['t0']
        out_a = 1 - clamp((t - (c['t1'] - 0.25)) / 0.25) if c['t1'] < self.dur else 1
        big = c['big']
        if c['opt'].get('count'):
            big = fmt_count(big, age / c['opt'].get('count'))
        sm, bg = caption_imgs(c['small'], big)
        y = H * c['opt'].get('y', 0.86)
        sc = 1.35 - 0.35 * ease_back(age / 0.35)
        a = clamp(age / 0.12) * out_a
        if bg is not None:
            paste_center(fr, bg, W / 2, y, sc, a)
            if sm is not None: paste_center(fr, sm, W / 2, y - bg.height * 0.52, 1.0, a)
        elif sm is not None:
            paste_center(fr, sm, W / 2, y, sc, a)

    def draw_guide(self, fr, gt, t):
        g = guide_img()
        e = ENV[min(len(ENV) - 1, int(gt * FPS))] if ENV else 0
        bob = math.sin(gt * 2.1) * 5 * U + e * -7 * U
        intro = 0
        if self.sc['scene'] == 1:
            intro = (1 - ease_out((t - 0.4) / 0.8)) * (g.height + 40 * U)
        x = W - g.width - int(40 * U)
        y = H - g.height - int(18 * U) + bob + intro
        # soft contact shadow on the map
        sh = Image.new('RGBA', (int(g.width * 0.9), int(34 * U)), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([0, 0, sh.width, sh.height], fill=(0, 0, 0, 110))
        fr.alpha_composite(scaled_blur(sh, 6), (int(x + g.width * 0.08), int(H - 30 * U - sh.height / 2 + intro)))
        fr.alpha_composite(g, (int(x), int(y)))

_BLUR = {}
def scaled_blur(im, r=30):
    key = (im.size, r)
    if key not in _BLUR: _BLUR[key] = im.filter(ImageFilter.GaussianBlur(r * U))
    return _BLUR[key]

# ---------------------------------------------------------------- build
def build_scenes(last=None):
    rows = TIMING['scenes']
    out, prev = [], None
    for r in rows:
        if last and r['scene'] > last: break
        spec = SCENES.get(r['scene'], {})
        s = Scene(r, spec, prev); out.append(s); prev = s
    return out

def render_scene(args):
    idx, last = args
    scenes = build_scenes(last)
    s = scenes[idx]
    f0, f1 = int(round(s.sc['start'] * FPS)), int(round(s.sc['end'] * FPS))
    path = os.path.join(OUT, 'scenes', f'{s.sc["scene"]:03d}.mp4')
    if os.path.exists(path) and os.environ.get('KEEP'): return path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    for f in range(f0, f1):
        p.stdin.write(s.frame(f / FPS - s.sc['start']).tobytes())
    p.stdin.close(); p.wait()
    print(f'scene {s.sc["scene"]} done ({f1 - f0} frames)', flush=True)
    return path

def sfx_track(scenes, total, sr=48000):
    out = np.zeros(int(total * sr) + sr, np.float32)
    rng = np.random.default_rng(1)
    def put(sig, t):
        i = int(t * sr); j = min(len(out), i + len(sig))
        if i < len(out): out[i:j] += sig[: j - i]
    def whoosh():
        n = int(0.7 * sr); x = rng.standard_normal(n).astype(np.float32)
        from scipy.signal import butter, lfilter
        b, a = butter(2, [300 / (sr / 2), 2500 / (sr / 2)], 'band'); x = lfilter(b, a, x)
        env = np.sin(np.linspace(0, np.pi, n)) ** 2
        return (x * env * 0.10).astype(np.float32)
    def pop():
        n = int(0.12 * sr); tt = np.arange(n) / sr
        f = 520 + 900 * np.exp(-tt * 40)
        return (np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-tt * 38) * 0.13).astype(np.float32)
    def hit():
        n = int(0.6 * sr); tt = np.arange(n) / sr
        boom = np.sin(2 * np.pi * (55 + 60 * np.exp(-tt * 18)) * tt) * np.exp(-tt * 7)
        click = rng.standard_normal(n) * np.exp(-tt * 70) * 0.25
        return ((boom + click) * 0.24).astype(np.float32)
    def swish():
        return whoosh() * 0.6
    S = {'whoosh': whoosh(), 'pop': pop(), 'hit': hit(), 'swish': swish()}
    for s in scenes:
        for kind, t in s.sfx:
            put(S[kind], s.sc['start'] + max(0, t))
    return out

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'full'
    scenes_all = build_scenes()
    if mode == 'preview':
        lim = float(sys.argv[2]) if len(sys.argv) > 2 else 125
        last = max(s.sc['scene'] for s in scenes_all if s.sc['start'] < lim)
        # end on a full sentence: drop the last scene if it would run far past the limit
        name = 'Russia_Preview.mp4'
    elif mode == 'scene':
        a, b = int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else int(sys.argv[2])
        with Pool(int(os.environ.get('WORKERS', 4))) as pool:
            pool.map(render_scene, [(i, b) for i in range(a - 1, b)])
        return
    else:
        last = len(scenes_all); name = 'Russia_Most_Powerful_Nation.mp4'
    scenes = scenes_all[:last]
    total = scenes[-1].sc['end']
    with Pool(int(os.environ.get('WORKERS', 4))) as pool:
        paths = pool.map(render_scene, [(i, last) for i in range(len(scenes))], chunksize=1)
    lst = os.path.join(OUT, 'concat.txt')
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in paths))
    # audio: narration + music (ducked) + sfx
    sfx = sfx_track(scenes, total)
    with wave.open(os.path.join(OUT, 'sfx.wav'), 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(48000)
        wf.writeframes((np.clip(sfx, -1, 1) * 32767).astype(np.int16).tobytes())
    out = os.path.join(OUT, name)
    music = os.path.join(OUT, 'music.wav')
    inputs = ['-f', 'concat', '-safe', '0', '-i', lst, '-i', os.path.join(OUT, 'narration.wav'), '-i', os.path.join(OUT, 'sfx.wav')]
    fc = '[1:a]atrim=0:{T},volume=1.0[v];[2:a]atrim=0:{T}[s]'.format(T=total)
    mix = '[v][s]'
    n = 2
    if os.path.exists(music):
        inputs += ['-i', music]
        fc += ';[3:a]atrim=0:{T},volume=0.20[m0];[m0][v]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[m]'.format(T=total)
        fc = fc.replace('volume=1.0[v]', 'volume=1.0,asplit=2[v][vk]').replace('[m0][v]side', '[m0][vk]side')
        mix += '[m]'; n = 3
    fc += f';{mix}amix=inputs={n}:normalize=0:duration=first,afade=t=out:st={total - 1.5}:d=1.5,alimiter=limit=0.95[a]'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', fc, '-map', '0:v', '-map', '[a]',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', str(total), '-movflags', '+faststart', out], check=True)
    print('wrote', out, round(total, 1), 's')

if __name__ == '__main__':
    main()
