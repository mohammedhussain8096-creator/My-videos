"""Renders the Istanbul video in the reference video's style (warm satellite map, grey studio, flat cartoon scenes,
spotlight stage, handwritten captions and big rounded numbers); adapted from the Russia renderer.

Original notes:: dark satellite map, orange-red country fills
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
import icons, cartoon
from render_text import text_img, font
from plan import SCENES, PLACES, VIEWS, GROUPS, CUSTOM

ASSETS = os.environ.get('RU_ASSETS', os.path.join(HERE, 'assets'))
OUT = os.environ.get('OUT_DIR', os.path.join(HERE, 'build'))
W, H = map(int, os.environ.get('RES', '1920x1080').split('x'))
U = W / 1920.0
FPS = int(os.environ.get('FPS', 24))
FILL_K = 0.5          # softer country fills on the warm map (reference look)
ENV_FPS = 24          # the voice loudness track (timing.json) is sampled at 24 per second
CRF, PRESET = os.environ.get('CRF', '19'), os.environ.get('PRESET', 'medium')
Image.MAX_IMAGE_PIXELS = None

COLORS = {'red': (226, 74, 30), 'blue': (40, 112, 232), 'grey': (160, 160, 165), 'green': (60, 170, 80),
          'yellow': (240, 190, 40), 'dark': (50, 50, 55), 'purple': (140, 80, 190), 'white': (235, 235, 235),
          'tan': (222, 180, 120), 'black': (25, 25, 28), 'teal': (40, 180, 170), 'pink': (230, 90, 150),
          'orange': (245, 140, 30), 'lime': (150, 200, 60), 'sky': (90, 170, 240), 'brown': (150, 100, 60)}
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
    if isinstance(at, tuple): return resolve_t(at[0], sc, wt) + at[1]
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
        _STATIC['vig'] = np.clip(1.0 - 0.22 * np.clip(r - 0.6, 0, None) ** 1.5, 0.6, 1)[..., None]
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

def label_img(text, size=34, color=(255, 255, 255), spaced=False):
    if spaced: text = ' '.join(text)
    return text_img(text, 'patrick', int(size * U), color, (35, 25, 20), max(3, int(5 * U)))

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
        if n in CUSTOM:
            for ring in CUSTOM[n](_POLY) if callable(CUSTOM[n]) else CUSTOM[n]:
                out.append([ll2m(lat, lon) for lon, lat in ring])
            continue
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
    if isinstance(p, tuple) and len(p) == 3 and p[0] == 's': return p[1] * W, p[2] * H
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
    for f in fills:
        name, col, a = f[:3]
        clip = f[3] if len(f) > 3 else None
        if a <= 0.001: continue
        m = Image.new('L', (hw, hh), 0); d = ImageDraw.Draw(m)
        for r in proj_rings(name):
            x, y = to_screen_arr(r, cam)
            if x.max() < -50 or x.min() > W + 50 or y.max() < -50 or y.min() > H + 50: continue
            if len(x) > 3: d.polygon(list(zip((x / 2).tolist(), (y / 2).tolist())), fill=255)
        if clip is not None:
            if clip < W: d.rectangle([clip / 2, 0, hw, hh], fill=0)
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
        arr = arr * (1 - FILL_K * mf) + tinted * FILL_K * mf
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
BIGCOL = {'red': ((246, 92, 52), (222, 54, 30), (92, 18, 10)), 'yellow': ((255, 228, 90), (248, 176, 36), (70, 36, 6)),
          'white': ((255, 255, 255), (232, 232, 236), (40, 30, 25))}
def caption_imgs(small, big, color='red', size=150):
    sm = text_img(small, 'patrick', int(58 * U), (255, 255, 255), (30, 22, 18), max(4, int(6 * U))) if small else None
    c = BIGCOL[color]
    bg = text_img(big, 'fredoka', int(size * U), None, c[2], max(6, int(size / 14 * U)), gradient=(c[0], c[1])) if big else None
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
        self.year = spec.get('year')
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
        self.reveal = {}
        for f in spec.get('fill', []):
            if len(f) > 3 and 'reveal' in f[3]:
                lon0, lon1, to = f[3]['reveal']
                self.reveal[f[0]] = (lon0, lon1, T(f[2]), T(to))
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
        self.clouds = spec.get('clouds', 1.0 if self.bg == 'scene' else 0)
        self.shakes = [(T(a), d, amp) for a, d, amp in spec.get('shake', [])]
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
        elif self.bg == 'space':
            fr = space_bg(t + self.sc['start'])
        elif self.bg == 'studio':
            fr = studio_bg()
        elif self.bg == 'clock':
            fr = clock_bg(gt)
        elif self.bg == 'spot':
            fr = spot_bg(gt)
        elif self.bg == 'scene':
            fr = sky_bg(self.spec.get('sky', 'day'), self.spec.get('ground', 'sand'), self.spec.get('horizon', 0.74))
        else:
            fr = crop_map(*cam)
            fills = []
            for f in self.fills:
                name, col, t0 = f[:3]
                a = ease((t - t0) / 0.6)
                if len(f) > 3 and f[3] is not None: a *= 1 - ease((t - f[3]) / 0.6)
                rv = self.reveal.get(name)
                if rv:
                    lon0, lon1, ta, tb = rv
                    if t < ta: continue
                    a = 1.0 if len(f) <= 3 or f[3] is None else a
                    lon = lon0 + (lon1 - lon0) * ease((t - ta) / max(0.1, tb - ta))
                    fills.append((name, col, a, to_screen((60.0, lon), cam)[0])); continue
                fills.append((name, col, a))
            fr = draw_fills(fr, cam, fills)
            arr = np.asarray(fr).astype(np.float32)
            if self.tint == 'night':
                arr *= np.array([0.42, 0.48, 0.7])
            elif self.tint == 'fire':
                arr = arr * np.array([0.65, 0.5, 0.42]) + np.array([40, 12, 0])
            elif self.tint == 'gloom':
                g = arr.mean(axis=2, keepdims=True); arr = (arr * 0.45 + g * 0.55) * 0.72
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
        if self.tint == 'night' or self.spec.get('stars') or self.bg == 'space':
            self.stars(fr, gt)
        for it in self.items:
            if it['k'] not in ('arrow', 'photo'): self.draw_item(fr, it, t, cam, gt)
        for it in self.items:
            if it['k'] == 'photo': self.draw_item(fr, it, t, cam, gt)
        if self.spec.get('snow') and t >= self.snow_t: self.snow(fr, gt, self.spec['snow'] * clamp((t - self.snow_t) / 1.0))
        if self.bg == 'scene' and self.spec.get('sky', 'day') == 'day': draw_sky_clouds(fr, gt, self.clouds)
        for ts, dd, amp in self.shakes:
            if ts <= t <= ts + dd:
                k = amp * U * (1 - (t - ts) / dd)
                fr = ImageChops.offset(fr, int(math.sin(t * 61) * k), int(math.cos(t * 47) * k))
        yr = self.year
        for ty, y in self.years:
            if t >= ty: yr = y
        if yr and self.bg in ('map', 'space'):
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
            im = cartoon.get(it['icon'][5:], int(it.get('s', 70) * U)) if it['icon'].startswith('cart:') else icons.get(it['icon'], int(it.get('s', 70) * U))
            paste_center(fr, im, x, y - im.height * 0.3, 1.0, a)
            return
        x, y = to_screen(it['at_place'], cam) if 'at_place' in it else ((it['xy'][0] * W, it['xy'][1] * H) if 'xy' in it else (0, 0))
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
                lim = pill_img(it['label'], it.get('ls', 22)) if it.get('pill', False) else label_img(it['label'], it.get('ls', 30))
                paste_center(fr, lim, x, y + lim.height * 0.75, pop, a)
        elif k == 'label':
            lim = label_img(it['text'], it.get('s', 34), tuple(it.get('color', (255, 255, 255))), it.get('spaced', False))
            if it.get('rot'): lim = lim.rotate(it['rot'], resample=Image.BICUBIC, expand=True)
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
        elif k == 'prop':
            im = cartoon.get(it['kind'], int(it.get('h', 200) * U), **it.get('kw', {}))
            if it.get('flip'): im = im.transpose(Image.FLIP_LEFT_RIGHT)
            bob = math.sin(gt * it.get('bobf', 2.0) + x * 0.01) * it.get('bob', 0) * U
            mx = 0
            if 'move_to' in it:
                p2 = clamp((t - t0) / max(0.1, it.get('t1', t0 + 2) - t0))
                mx = (it['move_to'] - it['xy'][0]) * W * ease(p2)
            kk = pop if it.get('pop', True) else 1.0
            sc_im = scaled(im, kk) if abs(kk - 1) > 0.01 else im
            if a < 0.999:
                sc_im = sc_im.copy(); sc_im.putalpha(sc_im.getchannel('A').point(lambda v: int(v * a)))
            fr.alpha_composite(sc_im, (int(x + mx - sc_im.width / 2), int(y - sc_im.height + bob)))
            if it.get('say') and age > 0.3:
                paste_center(fr, label_img(it['say'], it.get('ss', 32)), x + mx, y - im.height - 28 * U, 1, a)
        elif k == 'badge':
            r = int(it.get('s', 74) * U)
            key = ('badge', it['icon'], r, it.get('x', False))
            if key not in _STATIC:
                bd = Image.new('RGBA', (r * 2 + 12, r * 2 + 16), (0, 0, 0, 0)); dd = ImageDraw.Draw(bd)
                dd.ellipse([6, 10, 6 + 2 * r, 10 + 2 * r], fill=(0, 0, 0, 70))
                dd.ellipse([4, 4, 4 + 2 * r, 4 + 2 * r], fill=(250, 248, 242, 255), outline=(40, 30, 25, 255), width=max(2, int(3 * U)))
                if it['icon'].startswith('photo:'):
                    ph = Image.open(os.path.join(ASSETS, 'photos', it['icon'][6:] + '.jpg')).convert('RGB')
                    side = min(ph.size); ph = ph.crop(((ph.width - side) // 2, (ph.height - side) // 2, (ph.width + side) // 2, (ph.height + side) // 2)).resize((2 * r - 10, 2 * r - 10), Image.LANCZOS)
                    m = Image.new('L', ph.size, 0); ImageDraw.Draw(m).ellipse([0, 0, ph.width, ph.height], fill=255); bd.paste(ph, (9, 9), m)
                else:
                    ic = icons.get(it['icon'], int(r * 1.0)) if not it['icon'].startswith('cart:') else cartoon.get(it['icon'][5:], int(r * 1.2))
                    if it['icon'] in ('snow', 'drop'):      # white icons need colour on the white badge
                        tint = Image.new('RGBA', ic.size, (70, 140, 220, 255)); tint.putalpha(ic.getchannel('A')); ic = tint
                    if ic.width > 1.5 * r: ic = ic.resize((int(1.5 * r), int(ic.height * 1.5 * r / ic.width)), Image.LANCZOS)
                    bd.alpha_composite(ic, (4 + r - ic.width // 2, 4 + r - ic.height // 2))
                if it.get('x'):
                    xi = icons.get('xmark', int(r * 1.5)); bd.alpha_composite(xi, (4 + r - xi.width // 2, 4 + r - xi.height // 2))
                _STATIC[key] = bd
            bd = _STATIC[key]
            if 'lead' in it:
                lx, ly = to_screen(it['lead'], cam); dd = ImageDraw.Draw(fr)
                n = int(math.hypot(lx - x, ly - y) / (10 * U))
                for j in range(n):
                    if j % 2 == 0 and j / max(1, n) <= clamp(age / 0.5):
                        fx0 = x + (lx - x) * j / max(1, n); fy0 = y + (ly - y) * j / max(1, n)
                        dd.ellipse([fx0 - 2.5 * U, fy0 - 2.5 * U, fx0 + 2.5 * U, fy0 + 2.5 * U], fill=(255, 255, 255, int(230 * a)))
            paste_center(fr, bd, x, y, pop, a)
            if it.get('label'):
                paste_center(fr, label_img(it['label'], it.get('ls', 38)), x, y + r + 30 * U, pop, a)
        elif k == 'pin':
            s_ = it.get('s', 46) * U
            drop = (1 - ease_out(age / 0.4)) * 50 * U if t0 >= 0 else 0
            dd = ImageDraw.Draw(fr); py = y - drop
            dd.ellipse([x - s_ * 0.18, y - s_ * 0.06, x + s_ * 0.18, y + s_ * 0.06], fill=(0, 0, 0, 90))
            dd.polygon([(x, py), (x - s_ * 0.32, py - s_ * 0.62), (x + s_ * 0.32, py - s_ * 0.62)], fill=(246, 190, 40, 255))
            dd.ellipse([x - s_ * 0.36, py - s_ * 1.0, x + s_ * 0.36, py - s_ * 0.3], fill=(246, 190, 40, 255), outline=(150, 100, 20, 255), width=max(1, int(2 * U)))
            dd.ellipse([x - s_ * 0.13, py - s_ * 0.77, x + s_ * 0.13, py - s_ * 0.53], fill=(255, 240, 200, 255))
            if it.get('label'):
                paste_center(fr, label_img(it['label'], it.get('ls', 30), tuple(it.get('color', (255, 214, 64))), it.get('spaced', False)), x, y + 26 * U, 1, a * clamp(age / 0.3))
        elif k == 'line':
            path = catmull([to_screen(p, cam) for p in it['path']])
            p_ = 1.0 if t0 < 0 else ease(age / max(0.1, it.get('t1', t0 + 1.2) - t0))
            pp = partial(path, p_)
            if len(pp) > 1:
                col = tuple(it.get('color', (120, 220, 255)))
                if it.get('glow'):
                    gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).line(pp, fill=col + (int(170 * a),), width=int(it.get('w', 10) * 3 * U), joint='curve')
                    fr.alpha_composite(gl.filter(ImageFilter.GaussianBlur(10 * U)))
                ImageDraw.Draw(fr).line(pp, fill=col + (int(220 * a),), width=int(it.get('w', 10) * U), joint='curve')
        elif k == 'clock':
            r = it.get('s', 150) * U
            dd = ImageDraw.Draw(fr)
            dd.ellipse([x - r - 8 * U, y - r - 8 * U, x + r + 8 * U, y + r + 8 * U], fill=(40, 34, 30, 255))
            dd.ellipse([x - r, y - r, x + r, y + r], fill=(250, 248, 240, 255))
            for i in range(12):
                aa = math.radians(i * 30)
                dd.line([(x + math.cos(aa) * r * 0.82, y + math.sin(aa) * r * 0.82), (x + math.cos(aa) * r * 0.94, y + math.sin(aa) * r * 0.94)], fill=(40, 34, 30), width=max(2, int(5 * U)))
            sp = it.get('speed', -2.5)          # negative = spinning backwards
            for L, wdt, f in ((0.55, 9, 1.0), (0.8, 5, 12.0)):
                aa = -math.pi / 2 + sp * f * age
                dd.line([(x, y), (x + math.cos(aa) * r * L, y + math.sin(aa) * r * L)], fill=(40, 34, 30), width=max(2, int(wdt * U)))
            dd.arc([x - r - 34 * U, y - r - 34 * U, x + r + 34 * U, y + r + 34 * U], 200, 320, fill=(250, 248, 240), width=max(2, int(6 * U)))
            dd.polygon([(x + math.cos(math.radians(200)) * (r + 34 * U) - 16 * U, y + math.sin(math.radians(200)) * (r + 34 * U) + 4 * U),
                        (x + math.cos(math.radians(200)) * (r + 34 * U) + 10 * U, y + math.sin(math.radians(200)) * (r + 34 * U) - 18 * U),
                        (x + math.cos(math.radians(200)) * (r + 34 * U) + 14 * U, y + math.sin(math.radians(200)) * (r + 34 * U) + 12 * U)], fill=(250, 248, 240))
        elif k == 'photo':
            card = photo_card(it['name'], int(it.get('h', 560) * U), it.get('title'))
            k2 = (0.6 + 0.4 * ease_back(age / 0.5)) * (1 + 0.03 * clamp(age / 8))
            paste_center(fr, card, x, y, k2, a * clamp(age / 0.2))

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
        if 'off' in ti:
            k *= 1 - ease((t - self.T(ti['off'])) / 0.4)
            if k <= 0.01: return
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
        sm, bg = caption_imgs(c['small'], big, c['opt'].get('color', 'red'), c['opt'].get('size', 150))
        x = W * c['opt'].get('x', 0.5)
        if sm is not None:          # handwritten line writes itself on, left to right
            rv = clamp(age / (0.25 + 0.035 * len(c['small'])))
            if rv < 1:
                sm = sm.copy(); m = Image.new('L', sm.size, 0); ImageDraw.Draw(m).rectangle([0, 0, sm.width * rv, sm.height], fill=255)
                sm.putalpha(ImageChops.multiply(sm.getchannel('A'), m))
            paste_center(fr, sm, x, H * c['opt'].get('hy', 0.085), 1.0, out_a)
        if bg is not None:
            t_b = age - (0.35 if sm is not None else 0)
            if t_b > 0:
                sc = 1.35 - 0.35 * ease_back(t_b / 0.35)
                paste_center(fr, bg, x, H * c['opt'].get('y', 0.25 if sm is not None else 0.2), sc, clamp(t_b / 0.12) * out_a)

    def draw_guide(self, fr, gt, t):
        import guide
        h = int(400 * U)
        e = ENV[min(len(ENV) - 1, int(gt * ENV_FPS))] if ENV else 0
        sp, lean, hop = guide_motion(gt)
        lean += 1.0 * math.sin(gt * 2 * math.pi / 3.4)               # idle sway
        talk = -e * 7 * U
        x_off = 0.0
        if gt < 1.9:                                                  # walk in from the right
            k = ease_out(clamp((gt - 0.3) / 1.5))
            x_off = (1 - k) * 520 * U
            step = abs(math.sin(gt * math.pi * 3.2)) * (1 - k)
            talk -= step * 16 * U; lean += math.sin(gt * math.pi * 3.2) * 3 * (1 - k)
        sp, lean = round(sp * 2) / 2, round(lean * 4) / 4
        place = self.spec.get('gpos', {'studio': 'left'}.get(self.bg, 'right'))
        if place == 'left':
            h = int(620 * U); sp = -sp * 0.5; lean = -lean
            gx, gy = int(250 * U), H - int(60 * U)
        else:
            h = int(420 * U); gx, gy = W - int(200 * U) + x_off, H - int(26 * U)
        im, (fx, fy) = guide.pose(h, sp, lean)
        lift = hop * 34 * U
        sh = Image.new('RGBA', (int(h * 0.42 * (1 - 0.35 * hop)), int(30 * U)), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([0, 0, sh.width, sh.height], fill=(0, 0, 0, int(110 * (1 - 0.5 * hop))))
        fr.alpha_composite(scaled_blur(sh, 6), (int(gx - sh.width / 2), int(gy - sh.height / 2 - 4 * U)))
        fr.alpha_composite(im, (int(gx - fx), int(gy - fy - lift + talk + math.sin(gt * 2.1) * 3 * U)))

GUIDE_EVENTS = {'point': [], 'hop': []}

def plan_guide(scenes):
    """when the guide points his spear at the map (new arrows / captions) and when he hops (big moments)"""
    pts, hops = [], []
    for s in scenes:
        st = s.sc['start']
        cand = [st + it['t0'] for it in s.items if it['t0'] >= 0 and it['k'] in ('arrow', 'move')]
        cand += [st + c['t0'] for c in s.caps]
        cand += [st + it['t0'] for it in s.items if it['k'] == 'photo' and it['t0'] >= 0]
        for c in s.caps:
            if c['big'] and (c['big'].endswith('?') or c['big'].endswith('!')): hops.append(st + c['t0'])
        if s.title: hops.append(st + s.T(s.title.get('at', 0.05)))
        for tt in sorted(cand):
            if not pts or tt - pts[-1] > 3.2: pts.append(tt)
    GUIDE_EVENTS['point'] = pts; GUIDE_EVENTS['hop'] = hops

def guide_motion(gt):
    sp = lean = hop = 0.0
    for i, te in enumerate(GUIDE_EVENTS['point']):
        d = gt - te
        if -0.1 < d < 2.2:
            k = ease(d / 0.35) * (1 - ease((d - 1.4) / 0.6))
            amp = (13, 9, 16)[i % 3]
            sp = max(sp, amp * k); lean = max(lean, 2.5 * k)
    for te in GUIDE_EVENTS['hop']:
        d = gt - te
        if 0 <= d < 0.5: hop = max(hop, math.sin(math.pi * d / 0.5))
    return sp, lean, hop

def space_bg(gt):
    if 'space' not in _STATIC:
        y, x = np.mgrid[0:H, 0:W].astype(np.float32)
        base = np.zeros((H, W, 3), np.float32)
        base[..., 0] = 6 + 14 * y / H; base[..., 1] = 10 + 22 * y / H; base[..., 2] = 26 + 50 * y / H
        cx, cy, R = W * 0.5, H * 2.25, H * 1.55          # Earth's limb at the bottom
        r = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        earth = np.clip((R - r) / 3, 0, 1)[..., None]
        shade = np.clip((y - (cy - R)) / (H * 0.5), 0, 1)[..., None]
        ec = np.array([30, 90, 190], np.float32) * (1 - 0.5 * shade) + np.array([30, 120, 60], np.float32) * 0.15
        glow = np.exp(-np.clip(r - R, 0, None) / (24 * U))[..., None] * np.array([90, 160, 255], np.float32) * (r > R)[..., None]
        img = base * (1 - earth) + ec * earth + glow
        _STATIC['space'] = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    return _STATIC['space'].copy()

_PHOTO = {}
def photo_card(name, h, title):
    key = (name, h, title)
    if key not in _PHOTO:
        im = Image.open(os.path.join(ASSETS, 'photos', name + '.jpg')).convert('RGB')
        ph = int(h); pw = int(im.width * ph / im.height)
        if pw > W * 0.62: pw = int(W * 0.62); ph = int(im.height * pw / im.width)
        im = im.resize((pw, ph), Image.LANCZOS)
        b = int(12 * U); cap_h = int(54 * U) if title else 0
        card = Image.new('RGBA', (pw + 2 * b, ph + 2 * b + cap_h), (250, 247, 240, 255))
        card.paste(im, (b, b))
        if title:
            fs = 28
            while fs > 14 and font('patrick', int(fs * U)).getlength(title) > pw - 10: fs -= 1
            f = font('patrick', int(fs * U)); d = ImageDraw.Draw(card)
            l, t, r, bt = f.getbbox(title)
            d.text(((card.width - (r - l)) / 2 - l, ph + 2 * b + (cap_h - (bt - t)) / 2 - t - 6 * U), title, font=f, fill=(40, 32, 28))
        card = card.rotate(-2.0, resample=Image.BICUBIC, expand=True)
        sh = Image.new('RGBA', (card.width + 60, card.height + 60), (0, 0, 0, 0))
        sh.paste((0, 0, 0, 150), (36, 44), card.getchannel('A'))
        sh = sh.filter(ImageFilter.GaussianBlur(14 * U)); sh.alpha_composite(card, (20, 20))
        _PHOTO[key] = sh
    return _PHOTO[key]

def studio_bg():
    if 'studio' not in _STATIC:
        y, x = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((x - W * 0.55) / W) ** 2 + ((y - H * 0.45) / H) ** 2)
        g = 228 - 72 * r ** 1.6
        rng = np.random.default_rng(3)
        bh, bw = H // 8, W // 8
        yy, xx = np.mgrid[0:bh, 0:bw].astype(np.float32); blot = np.zeros((bh, bw), np.float32)
        for _ in range(40):
            cx, cy, rr = rng.uniform(0, bw), rng.uniform(0, bh), rng.uniform(4, 18)
            blot += np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * rr ** 2)) * rng.uniform(-6, 6)
        blot = np.asarray(Image.fromarray(blot).resize((W, H), Image.BICUBIC))
        g = (g + blot)[..., None] * np.array([1.0, 1.0, 1.01])
        _STATIC['studio'] = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8))
    return _STATIC['studio'].copy()

def spot_bg(gt):
    if 'spot' not in _STATIC:
        y, x = np.mgrid[0:H, 0:W].astype(np.float32)
        base = np.stack([62 - 20 * y / H, 52 - 18 * y / H, 80 - 22 * y / H], axis=-1)
        half = 0.07 * W + (y / H) * 0.15 * W
        cone = np.clip(1 - np.abs(x - W * 0.62) / half, 0, 1) ** 0.6 * (y < H * 0.86)
        img = base + cone[..., None] * np.array([150, 136, 100]) * (0.35 + 0.65 * (1 - y / H))[..., None]
        img = img + (y > H * 0.86)[..., None] * np.array([-14, -12, -10])
        _STATIC['spot'] = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    fr = _STATIC['spot'].copy(); d = ImageDraw.Draw(fr)
    for i in range(18):
        yy = (i * 53 + gt * 18) % (H * 0.8); xx = W * 0.62 + math.sin(i * 1.7 + gt) * W * 0.06 * (yy / H + 0.3)
        d.ellipse([xx - 2 * U, yy - 2 * U, xx + 2 * U, yy + 2 * U], fill=(255, 245, 210))
    return fr

SKIES = {'day': ((150, 196, 220), (242, 228, 192)), 'dusk': ((90, 70, 130), (246, 160, 90)), 'night': ((14, 20, 48), (52, 60, 98)),
         'gold': ((240, 180, 90), (252, 226, 160))}
GROUNDS = {'sand': ((226, 196, 140), (206, 170, 110)), 'grass': ((150, 180, 90), (120, 150, 70)), 'sea': ((40, 110, 180), (24, 78, 150)),
           'stone': ((200, 186, 160), (176, 160, 130)), 'nightsea': ((20, 40, 80), (10, 22, 50))}
def sky_bg(sky, ground, hz):
    key = ('sky', sky, ground, hz)
    if key not in _STATIC:
        y = np.arange(H, dtype=np.float32)[:, None, None] / H
        top, bot = [np.array(c, np.float32) for c in SKIES[sky]]
        img = top + (bot - top) * np.clip(y / hz, 0, 1)
        g0, g1 = [np.array(c, np.float32) for c in GROUNDS[ground]]
        gk = np.clip((y - hz) / (1 - hz), 0, 1)
        img = np.where(y > hz, g0 + (g1 - g0) * gk, img)
        img = np.repeat(img, W, axis=1)
        im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
        if sky in ('day', 'gold'):
            sx, sy, r = W * 0.22, H * 0.18, 60 * U
            d.ellipse([sx - r * 1.6, sy - r * 1.6, sx + r * 1.6, sy + r * 1.6], fill=(250, 238, 200))
            d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(252, 228, 150))
        if sky == 'night':
            rng = np.random.default_rng(4)
            for _ in range(120):
                xx, yy, rr = rng.uniform(0, W), rng.uniform(0, H * hz * 0.9), rng.uniform(1, 2.5) * U
                d.ellipse([xx - rr, yy - rr, xx + rr, yy + rr], fill=(255, 255, 240))
            d.ellipse([W * 0.8, H * 0.1, W * 0.8 + 70 * U, H * 0.1 + 70 * U], fill=(250, 240, 200))
        if ground in ('sand', 'grass'):
            rng = np.random.default_rng(6)
            for _ in range(40):
                xx, yy = rng.uniform(0, W), rng.uniform(H * (hz + 0.02), H)
                d.line([(xx, yy), (xx - 6 * U, yy - 12 * U)], fill=(170, 140, 80), width=max(1, int(2 * U)))
                d.line([(xx, yy), (xx + 5 * U, yy - 11 * U)], fill=(170, 140, 80), width=max(1, int(2 * U)))
        if ground in ('sea', 'nightsea'):
            for i in range(30):
                xx = (i * 137) % W; yy = H * (hz + 0.03 + (i * 0.031) % (0.95 - hz))
                d.arc([xx, yy, xx + 40 * U, yy + 10 * U], 200, 340, fill=(255, 255, 255, 120), width=max(1, int(2 * U)))
        d.line([(0, H * hz), (W, H * hz)], fill=tuple(int(c * 0.85) for c in GROUNDS[ground][0]), width=max(1, int(2 * U)))
        _STATIC[key] = im
    return _STATIC[key].copy()

def draw_sky_clouds(fr, gt, amount=1.0):
    if amount <= 0: return
    span = W + 800 * U
    for i, (sp, yf, spd, ph, sc) in enumerate([(0, 0.12, 8, 300, 0.7), (1, 0.24, 6, 1300, 0.55), (2, 0.08, 10, 2100, 0.6)]):
        im = scaled(cloud_sprite(sp), sc)
        x = (ph * U + spd * U * gt) % span - 400 * U
        fr.alpha_composite(im, (int(x), int(yf * H - im.height / 2)))

def clock_bg(gt):
    if 'clockbg' not in _STATIC:
        y = np.arange(H, dtype=np.float32)[:, None, None] / H
        img = np.array([28, 36, 74], np.float32) + (np.array([44, 54, 104], np.float32) - np.array([28, 36, 74], np.float32)) * y
        _STATIC['clockbg'] = Image.fromarray(np.clip(np.repeat(img, W, axis=1), 0, 255).astype(np.uint8))
    fr = _STATIC['clockbg'].copy(); d = ImageDraw.Draw(fr)
    for i in range(26):       # speed streaks rushing past
        yy = (i * 97) % H; ln = (120 + (i * 53) % 260) * U
        xx = W - ((gt * (900 + (i % 5) * 220) * U + i * 311) % (W + ln))
        d.line([(xx, yy), (xx + ln, yy)], fill=(110, 130, 190), width=max(1, int((1 + i % 3) * U)))
    return fr

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
    plan_guide(out)
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
                          '-i', '-', '-c:v', 'libx264', '-preset', PRESET, '-crf', CRF, '-profile:v', 'high', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
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
    POP_GAP = float(os.environ.get('POP_GAP', 1.2))   # at most one pop per 1.2 s: about half as many pops (user request)
    last_pop = -9.0
    for s in scenes:
        for kind, t in sorted(s.sfx, key=lambda e: e[1]):
            tt = s.sc['start'] + max(0, t)
            if kind == 'pop':
                if tt - last_pop < POP_GAP: continue
                last_pop = tt
            put(S[kind], tt)
    return out

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'full'
    scenes_all = build_scenes()
    if mode == 'preview':
        lim = float(sys.argv[2]) if len(sys.argv) > 2 else 125
        last = max(s.sc['scene'] for s in scenes_all if s.sc['start'] < lim)
        # end on a full sentence: drop the last scene if it would run far past the limit
        name = 'Istanbul_Preview.mp4'
    elif mode == 'scene':
        a, b = int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else int(sys.argv[2])
        with Pool(int(os.environ.get('WORKERS', 4))) as pool:
            pool.map(render_scene, [(i, b) for i in range(a - 1, b)])
        return
    else:
        last = len(scenes_all); name = 'Istanbul_Golden_City.mp4'
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
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', str(total), '-movflags', '+faststart', out], check=True)
    print('wrote', out, round(total, 1), 's')

if __name__ == '__main__':
    main()
