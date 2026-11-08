"""Reference-style elements (from the user's reference video):
flat beige/blue maps with glowing red country highlights, big outlined keyword text that pops in on the spoken word,
an old 8 mm film frame (sprockets, scratches, dust, flicker, sepia), fiery titles with embers,
and a simple 3D power-plant model (four numbered reactor blocks, striped stack, grid floor, sky)."""
import json, math, os
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

import sys, importlib
R = sys.modules['__main__'] if hasattr(sys.modules.get('__main__'), 'MPX') else importlib.import_module('render')
W, H, U = R.W, R.H, R.U
SEA = (78, 164, 206); LAND = (238, 229, 205); BORDER = (196, 178, 150); RIVER = (88, 168, 210)
USSR = ['Russia', 'Ukraine', 'Belarus', 'Kazakhstan', 'Uzbekistan', 'Turkmenistan', 'Kyrgyzstan', 'Tajikistan', 'Georgia',
        'Armenia', 'Azerbaijan', 'Moldova', 'Lithuania', 'Latvia', 'Estonia']
GROUPS = {'USSR': USSR}

def ease(x): return R.ease(x)
def eout(x): return R.eout(x)

# ------------------------------------------------------------------ flat maps (two projections share code)
class Proj:
    def __init__(self, lon0, lon1, lat0, lat1, px):
        self.lon0, self.lon1 = lon0, lon1; self.y0, self.y1 = R.merc(lat1), R.merc(lat0)
        self.W = px; self.H = int(px * (self.y0 - self.y1) / math.radians(lon1 - lon0))
    def __call__(self, lat, lon):
        return (lon - self.lon0) / (self.lon1 - self.lon0) * self.W, (self.y0 - R.merc(max(-84, min(84, lat)))) / (self.y0 - self.y1) * self.H

EU = Proj(R.M_LON0, R.M_LON1, R.M_LAT0, R.M_LAT1, R.MPX)          # same pixels as render.ll()
WORLD = Proj(-30.0, 190.0, 18.0, 80.0, 7000)

@lru_cache(None)
def water():
    return json.load(open(os.path.join(R.ASSETS, 'water.json')))

def polys(name):
    for n in GROUPS.get(name, [name]):
        for r in R.countries().get(n, []): yield r

@lru_cache(None)
def flat_base(which):
    P = EU if which == 'eu' else WORLD
    im = Image.new('RGB', (P.W, P.H), SEA); d = ImageDraw.Draw(im)
    # subtle darker sea toward the edges of land (depth feel)
    for n, rs in R.countries().items():
        for r in rs:
            pts = [P(la, lo) for lo, la in r]; xs = [p[0] for p in pts]
            if max(xs) < -50 or min(xs) > P.W + 50: continue
            d.polygon(pts, fill=LAND)
    sea = Image.new('RGB', im.size, (64, 146, 192)); m = np.asarray(im, np.int16)
    landmask = Image.fromarray(((np.abs(m - np.array(SEA)).sum(axis=2) > 6) * 255).astype(np.uint8))
    shore = landmask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(14))
    im = Image.composite(im, Image.composite(Image.new('RGB', im.size, (104, 184, 220)), sea, shore), landmask)
    d = ImageDraw.Draw(im)
    if which == 'eu':
        wt = water()
        for lk in wt['lakes']:
            d.polygon([P(la, lo) for lo, la in lk], fill=RIVER)
        for sc, pts in wt['rivers']:
            if sc > 8: continue
            d.line([P(la, lo) for lo, la in pts], fill=RIVER, width=max(2, int(9 - sc)))
    for n, rs in R.countries().items():
        for r in rs:
            pts = [P(la, lo) for lo, la in r]; xs = [p[0] for p in pts]
            if max(xs) < -50 or min(xs) > P.W + 50: continue
            d.line(pts + [pts[0]], fill=BORDER, width=3)
    # paper grain
    a = np.asarray(im, np.float32); rng = np.random.default_rng(5)
    n_ = np.asarray(Image.fromarray(rng.normal(128, 40, (im.height // 3, im.width // 3)).clip(0, 255).astype(np.uint8)).resize(im.size, Image.BILINEAR), np.float32) - 128
    return Image.fromarray((a + n_[..., None] * 0.06).clip(0, 255).astype(np.uint8))

@lru_cache(32)
def country_mask(which, name):
    P = EU if which == 'eu' else WORLD
    m = Image.new('L', (P.W // 2, P.H // 2), 0); d = ImageDraw.Draw(m)
    for r in polys(name): d.polygon([(x / 2, y / 2) for x, y in (P(la, lo) for lo, la in r)], fill=255)
    return m

def highlight(base, which, box, hl, t):
    """hl: list of (name, mode 'fill'|'outline', colour, at). Glowing red fills / glowing outlines like the reference."""
    for h in hl:
        name, mode, col, at = h[:4]; a = ease((t - at) / 0.5)
        if a <= 0: continue
        cm = country_mask(which, name); bb = (max(0, box[0] / 2), max(0, box[1] / 2), min(cm.width, box[2] / 2), min(cm.height, box[3] / 2))
        m = cm.resize((W, H), Image.BILINEAR, box=bb)
        if mode == 'fill':
            fill = Image.new('RGBA', (W, H), col + (0,)); fill.putalpha(m.point(lambda v: int(v * a * 0.92)))
            glow = Image.new('RGBA', (W, H), col + (0,)); glow.putalpha(m.filter(ImageFilter.GaussianBlur(16 * U)).point(lambda v: int(min(255, v * a * 0.7))))
            base.alpha_composite(glow); base.alpha_composite(fill)
        else:
            edge = m.filter(ImageFilter.MaxFilter(5)); inner = m.filter(ImageFilter.MinFilter(5))
            ring = Image.fromarray(np.clip(np.asarray(edge, np.int16) - np.asarray(inner, np.int16), 0, 255).astype(np.uint8))
            glow = Image.new('RGBA', (W, H), col + (0,)); glow.putalpha(ring.filter(ImageFilter.GaussianBlur(10 * U)).point(lambda v: int(min(255, v * a * 2.2))))
            line = Image.new('RGBA', (W, H), col + (0,)); line.putalpha(ring.point(lambda v: int(v * a)))
            base.alpha_composite(glow); base.alpha_composite(glow); base.alpha_composite(line)

def flat_frame(sp, t, D, view_ll):
    """returns (RGBA frame, projection, box) for a flat map view; view_ll = (lat, lon, width_deg)"""
    lat, lon, wdeg = view_ll
    which = 'world' if wdeg > 45 else 'eu'
    P = EU if which == 'eu' else WORLD
    cx, cy = P(lat, lon); w = wdeg / (P.lon1 - P.lon0) * P.W; h = w * H / W
    w = min(w, P.W); h = w * H / W
    if h > P.H: h = P.H; w = h * W / H
    cx = min(max(cx, w / 2), P.W - w / 2); cy = min(max(cy, h / 2), P.H - h / 2)
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    img = flat_base(which).resize((W, H), Image.BILINEAR, box=box).convert('RGBA')
    highlight(img, which, box, sp.get('hl', []), t)
    return img, P, box

# ------------------------------------------------------------------ icons
@lru_cache(16)
def radiation_icon(size):
    s = size * 4; im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = s / 2
    d.ellipse([0, 0, s, s], fill=(20, 20, 20, 255)); d.ellipse([s * .05, s * .05, s * .95, s * .95], fill=(255, 196, 0, 255))
    for k in range(3):
        a0 = -90 + k * 120 - 30
        d.pieslice([s * .14, s * .14, s * .86, s * .86], a0, a0 + 60, fill=(20, 20, 20, 255))
    d.ellipse([c - s * .2, c - s * .2, c + s * .2, c + s * .2], fill=(255, 196, 0, 255))
    d.ellipse([c - s * .12, c - s * .12, c + s * .12, c + s * .12], fill=(20, 20, 20, 255))
    return im.resize((size, size), Image.LANCZOS)

@lru_cache(16)
def bolt_icon(size):
    s = size * 4; im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(.55, 0), (.2, .55), (.45, .55), (.35, 1), (.8, .4), (.55, .4), (.7, 0)]
    d.polygon([(x * s, y * s) for x, y in pts], fill=(255, 210, 30, 255), outline=(60, 40, 0, 255), width=int(s * .04))
    return im.resize((size, size), Image.LANCZOS)

def pop_scale(t, at, dur=0.22):
    k = (t - at) / dur
    if k <= 0: return 0
    if k >= 1: return 1.0
    return 1.0 + 0.25 * math.sin(math.pi * k) * (1 - k) + (k - 1) * 0.0

def put_icon(img, icon, x, y, t, at):
    if t < at: return
    s = min(1.0, (t - at) / 0.18) * (1 + 0.2 * math.sin(min(1, (t - at) / 0.3) * math.pi))
    sz = max(2, int(icon.width * s)); ic = icon.resize((sz, sz), Image.LANCZOS)
    sh = Image.new('RGBA', ic.size, (0, 0, 0, 0)); sh.putalpha(ic.getchannel('A').filter(ImageFilter.GaussianBlur(8 * U)).point(lambda v: int(v * .6)))
    img.alpha_composite(sh, (int(x - sz / 2 + 6 * U), int(y - sz / 2 + 8 * U))); img.alpha_composite(ic, (int(x - sz / 2), int(y - sz / 2)))

# ------------------------------------------------------------------ keyword text (reference: bold white, black outline, pops in)
@lru_cache(None)
def kw_font(size): return ImageFont.truetype(os.path.join(R.ASSETS, 'fonts', 'Inter-ExtraBold.ttf'), int(size * U))

def kw(img, txt, t, at, y=0.74, size=86, col=(255, 255, 255), typing=True, x=0.5):
    if t < at: return
    n = len(txt) if not typing else max(1, min(len(txt), int((t - at) / 0.035) + 1))
    s = txt[:n]; f = kw_font(size)
    k = min(1.0, (t - at) / 0.2); sc = 1.0 + 0.18 * (1 - k)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    full_w = f.getlength(txt); x0 = W * x - full_w / 2
    d.text((x0 + 5 * U, H * y + 7 * U), s, font=f, fill=(0, 0, 0, 170), anchor='lm', stroke_width=int(10 * U), stroke_fill=(0, 0, 0, 170))
    lay = lay.filter(ImageFilter.GaussianBlur(6 * U)); d = ImageDraw.Draw(lay)
    d.text((x0, H * y), s, font=f, fill=col + (255,), anchor='lm', stroke_width=int(7 * U), stroke_fill=(15, 15, 15, 255))
    if sc != 1.0:
        bw, bh = int(W * sc), int(H * sc); big = lay.resize((bw, bh), Image.BILINEAR)
        cxp, cyp = W * x * sc, H * y * sc; lay = big.crop((int(cxp - W * x), int(cyp - H * y), int(cxp - W * x) + W, int(cyp - H * y) + H))
    img.alpha_composite(lay)

# ------------------------------------------------------------------ old film frame
@lru_cache(None)
def film_mask():
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    d.rounded_rectangle([W * 0.035, H * 0.03, W * 0.965, H * 0.97], radius=int(38 * U), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(3 * U))
    frame = Image.new('RGBA', (W, H), (10, 9, 8, 255)); frame.putalpha(Image.eval(m, lambda v: 255 - v))
    d = ImageDraw.Draw(frame)
    for k in range(4):                                    # sprocket holes on the left
        y = H * (0.1 + 0.25 * k)
        d.rounded_rectangle([W * 0.006, y, W * 0.028, y + H * 0.1], radius=int(8 * U), fill=(200, 196, 186, 255))
    return frame

def film(arr, t, sepia=0.75):
    """arr: float RGB array -> old 8mm look"""
    g = arr.mean(axis=2, keepdims=True)
    sep = np.concatenate([g * 1.07 + 18, g * 0.97 + 8, g * 0.78], axis=2)
    a = arr * (1 - sepia) + sep * sepia
    fl = 1 + 0.05 * math.sin(t * 37) + 0.03 * math.sin(t * 13.7); a = a * fl
    rng = np.random.default_rng(int(t * 24))
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA'); d = ImageDraw.Draw(im)
    for _ in range(rng.integers(1, 4)):                  # scratches
        x = rng.uniform(0.1, 0.9) * W; d.line([x, 0, x + rng.uniform(-6, 6) * U, H], fill=(235, 225, 205, int(rng.uniform(40, 110))), width=1)
    for _ in range(rng.integers(3, 12)):                 # dust
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(1, 4) * U
        d.ellipse([x - r, y - r, x + r, y + r], fill=(30, 25, 20, int(rng.uniform(80, 200))))
    jx, jy = int(rng.normal(0, 1.2 * U)), int(rng.normal(0, 1.2 * U))
    im = Image.fromarray(np.roll(np.roll(np.asarray(im), jx, axis=1), jy, axis=0)).convert('RGBA')
    im.alpha_composite(film_mask())
    return np.asarray(im.convert('RGB'), np.float32)

# ------------------------------------------------------------------ fiery title
def draw_fire(sp, t, D):
    if sp.get('bgimg'):
        bg = R.photo(sp['bgimg'], sp.get('grade', 'warm'))
        k = max(W / bg.width, H / bg.height) * (1.08 + 0.05 * t / max(D, 1)); b = bg.resize((int(bg.width * k), int(bg.height * k)), Image.BILINEAR)
        b = b.crop(((b.width - W) // 2, (b.height - H) // 2, (b.width - W) // 2 + W, (b.height - H) // 2 + H))
        a = np.asarray(b, np.float32); g = a.mean(axis=2, keepdims=True)
        a = np.concatenate([g * 1.1 + 25, g * 0.65 + 8, g * 0.3], axis=2) * 0.62
        img = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')
    else:
        img = R.dark_bg('red').copy().convert('RGBA')
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse([W * 0.1, H * 0.55, W * 0.9, H * 1.4], fill=(255, 110, 20, 120))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120 * U)))
    rng = np.random.default_rng(11); d = ImageDraw.Draw(img)
    for k in range(120):                                  # embers rising
        x0 = rng.uniform(0, W); sp_ = rng.uniform(60, 220) * U; ph = rng.uniform(0, 10)
        y = H - ((t * sp_ + ph * 100 * U) % (H * 1.1)); x = x0 + math.sin(t * rng.uniform(0.5, 2) + ph) * 30 * U
        r = rng.uniform(1.5, 4.5) * U; al = int(rng.uniform(120, 255))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, int(rng.uniform(120, 210)), 40, al))
    lines = sp['text'].split('\n'); f = ImageFont.truetype(os.path.join(R.ASSETS, 'fonts', 'Inter-ExtraBold.ttf'), int(sp.get('size', 120) * U))
    a = ease((t - 0.2) / 0.6); sc = 1.0 + 0.08 * (1 - a)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    lh = sp.get('size', 120) * U * 1.15; y0 = H * sp.get('y', 0.5) - lh * (len(lines) - 1) / 2
    for i, l in enumerate(lines):
        ld.text((W / 2, y0 + i * lh), l, font=f, fill=(255, 255, 255, 255), anchor='mm', stroke_width=int(4 * U), stroke_fill=(255, 255, 255, 255))
    m = lay.getchannel('A'); yy = np.linspace(0, 1, H)[:, None]
    grad = np.concatenate([np.full((H, W, 1), 255), (200 - 110 * yy[:, :, None] * np.ones((1, W, 1))), np.full((H, W, 1), 40)], axis=2)
    txt = Image.fromarray(grad.clip(0, 255).astype(np.uint8)).convert('RGBA'); txt.putalpha(m.point(lambda v: int(v * a)))
    outer = Image.new('RGBA', (W, H), (255, 90, 10, 0)); outer.putalpha(m.filter(ImageFilter.GaussianBlur(26 * U)).point(lambda v: int(min(255, v * 1.6 * a))))
    edge = Image.new('RGBA', (W, H), (90, 20, 0, 0)); edge.putalpha(m.filter(ImageFilter.MaxFilter(7)).point(lambda v: int(v * a)))
    img.alpha_composite(outer); img.alpha_composite(edge); img.alpha_composite(txt)
    if sc != 1.0:
        big = img.resize((int(W * sc), int(H * sc)), Image.BILINEAR); img = big.crop(((big.width - W) // 2, (big.height - H) // 2, (big.width - W) // 2 + W, (big.height - H) // 2 + H))
    return img.convert('RGB')

# ------------------------------------------------------------------ 3D plant model
def _box(d, P, x, y, z, w, dpt, h, cols):
    """axis-aligned box in world coords projected by P(x,y,z); cols = (top, front, side)"""
    c = [P(x, y, z), P(x + w, y, z), P(x + w, y + dpt, z), P(x, y + dpt, z),
         P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + dpt, z + h), P(x, y + dpt, z + h)]
    d.polygon([c[0], c[1], c[5], c[4]], fill=cols[1])                 # front
    d.polygon([c[1], c[2], c[6], c[5]], fill=cols[2])                 # right side
    d.polygon([c[4], c[5], c[6], c[7]], fill=cols[0])                 # top
    return c

def draw_plant(sp, t, D):
    k = ease(t / D)
    zoom = R.lerp(sp.get('z0', 1.7), sp.get('z1', 1.85), k); fx = R.lerp(sp.get('fx0', 0.0), sp.get('fx1', sp.get('fx0', 0.0)), k)
    img = Image.new('RGBA', (W, H)); a = np.zeros((H, W, 3), np.float32); yy = np.linspace(0, 1, H)[:, None]
    hor = 0.5
    sky = np.array([40, 120, 205]) * (1 - yy) + np.array([175, 215, 240]) * yy
    a[:] = sky[:, None, :] if sky.ndim == 2 else sky
    img = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA'); d = ImageDraw.Draw(img)
    rng = np.random.default_rng(3)                                       # soft clouds
    cl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cd = ImageDraw.Draw(cl)
    for _ in range(14):
        cx_ = (rng.uniform(-0.2, 1.2) * W + t * 12 * U) % (W * 1.3) - W * 0.15; cy_ = rng.uniform(0.05, 0.4) * H; r = rng.uniform(60, 160) * U
        cd.ellipse([cx_ - r * 1.8, cy_ - r * 0.5, cx_ + r * 1.8, cy_ + r * 0.5], fill=(255, 255, 255, 150))
    img.alpha_composite(cl.filter(ImageFilter.GaussianBlur(30 * U))); d = ImageDraw.Draw(img)
    d.rectangle([0, H * hor, W, H], fill=(70, 74, 78))
    f = 900 * U * zoom; cam_h = 6.0; cam_y = -26.0
    def P(x, y, z):
        yy_ = y - cam_y; s = f / max(1.0, yy_)
        return W / 2 + (x - fx) * s, H * hor + (cam_h - z) * s - (cam_h * f / 40) * 0
    for gx in range(-40, 41, 4):                                         # perspective grid floor
        d.line([P(gx, 2, 0), P(gx, 80, 0)], fill=(105, 110, 115), width=1)
    for gy in range(2, 80, 4):
        d.line([P(-40, gy, 0), P(40, gy, 0)], fill=(105, 110, 115), width=1)
    hl = sp.get('hl', {}); blocks = [(-17, 1), (-9, 2), (1, 3), (9, 4)]
    WH, GR, SH = (238, 238, 236), (205, 207, 208), (175, 178, 180)
    _box(d, P, -20, 12, 0, 40, 4, 2.2, (WH, GR, SH))                     # turbine hall behind
    for bx, num in blocks:
        glow = hl.get(num); ga = ease((t - glow) / 0.4) if glow is not None else 0
        cols = (WH, GR, SH)
        if ga > 0: cols = tuple(tuple(int(R.lerp(c, y_, ga)) for c, y_ in zip(cc, (255, 214, 40))) for cc in cols)
        _box(d, P, bx, 6, 0, 6.5, 5, 3.2 + (0.6 if num in (3, 4) else 0), cols)
        _box(d, P, bx + 1.5, 7, 3.2, 3.5, 3, 1.2, cols)
        if sp.get('numbers', True) and t > sp.get('num_at', 0.3):
            x_, y_ = P(bx + 3.2, 6, 2.0); f_ = ImageFont.truetype(os.path.join(R.ASSETS, 'fonts', 'Inter-ExtraBold.ttf'), int(46 * U * zoom))
            d.text((x_, y_), str(num), font=f_, fill=(30, 30, 30), anchor='mm')
    # ventilation stack between units 3 and 4, red/white bands
    sx = 7.6; base_ = P(sx, 9, 0); top_ = P(sx, 9, 15); sw = (P(sx + 0.7, 9, 0)[0] - base_[0])
    for i in range(10):
        z0_, z1_ = i * 1.5, (i + 1) * 1.5; p0, p1 = P(sx, 9, z0_), P(sx, 9, z1_)
        d.rectangle([p1[0] - sw, p1[1], p1[0] + sw, p0[1]], fill=(215, 40, 35) if i % 2 else (245, 245, 245))
    for bt in sp.get('bolts', []):                                       # (unit, at)
        num, at = bt; bx = dict((n, x) for x, n in blocks)[num]; x_, y_ = P(bx + 3.2, 8, 7.0)
        put_icon(img, bolt_icon(int(90 * U * zoom)), x_, y_, t, at)
    te = sp.get('explode')
    if te is not None and t > te:
        tt = t - te; x_, y_ = P(12.2, 8, 4.0)
        sm = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sm)
        for i in range(24):
            u = (i / 24 + tt * 0.1) % 1; r = (40 + 220 * u) * U * zoom; yy2 = y_ - u * 700 * U * zoom
            g = int(28 + 34 * (1 - u)); sd.ellipse([x_ - r * 1.2, yy2 - r * .8, x_ + r * 1.2, yy2 + r * .8], fill=(g, g - 4, g - 6, int(245 * (1 - u * 0.7) * min(1, tt / 0.5))))
        img.alpha_composite(sm.filter(ImageFilter.GaussianBlur(22 * U)))
        fire = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fire); bb = eout(tt / 0.5)
        fd.ellipse([x_ - 260 * U * zoom * bb, y_ - 320 * U * zoom * bb, x_ + 260 * U * zoom * bb, y_ + 60 * U * zoom], fill=(255, 150, 40, int(240 * max(0.45, 1 - tt * 0.25))))
        fd.ellipse([x_ - 110 * U * zoom * bb, y_ - 160 * U * zoom * bb, x_ + 110 * U * zoom * bb, y_ + 20 * U * zoom], fill=(255, 235, 170, int(255 * max(0.2, 1 - tt * 0.5))))
        img.alpha_composite(fire.filter(ImageFilter.GaussianBlur(34 * U)))
        dd = ImageDraw.Draw(img); rr = np.random.default_rng(5)
        for _ in range(60):                                              # flying debris
            ang = rr.uniform(-2.8, -0.35); v = rr.uniform(250, 900) * U * zoom * 0.5
            px_ = x_ + math.cos(ang) * v * tt; py_ = y_ + math.sin(ang) * v * tt + 500 * U * zoom * 0.5 * tt * tt; r = rr.uniform(2, 7) * U * zoom * 0.6
            if 0 < px_ < W and 0 < py_ < H: dd.rectangle([px_ - r, py_ - r, px_ + r, py_ + r], fill=(60, 50, 45) if rr.random() < .6 else (255, 170, 60))
    return img.convert('RGB')
