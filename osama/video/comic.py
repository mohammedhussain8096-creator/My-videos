"""Comic-illustration renderer for "The Hunt for Osama bin Laden", in the reference video's style:
inked, cel-shaded illustrated backdrops on paper grain, a beige paper map with a salmon country fill and
red pins, handwritten captions with a red underline swoosh, yellow comic titles and a tear-off calendar prop.

The illustrated backdrops here are drawn in code (silhouette people, no real likenesses). For the final
video, AI-generated images can be dropped into images/<scene>.png and are used instead (with the same
camera moves and text).

Usage: python3 comic.py FIRST LAST     (env EGYPT_ASSETS, OUT_DIR, RES, WORKERS, NAME)"""
import json, math, os, random, re, subprocess, sys, wave
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'egypt', 'video'))
import render as R                          # reuse fonts, text drawing, easing
W, H, S = R.W, R.H, R.S
OUT = os.environ.get('OUT_DIR', os.path.join(HERE, 'build'))
IMAGES = os.environ.get('IMAGES', os.path.join(HERE, 'images'))
FPS = 24
INK = (38, 32, 30)
RED_UL = (200, 45, 40)
PAPER = (231, 226, 214)
LOOK = os.environ.get('LOOK', 'real')       # 'real' (cinematic documentary) or 'comic' (reference style)

ease, ease_out, ease_pop = R.ease, R.ease_out, R.ease_pop

# ----------------------------------------------------------------------------- data
def load_visuals():
    vis = {}
    for line in open(os.path.join(HERE, '..', 'visuals.txt')):
        if not re.match(r'^\d+ \|', line): continue
        n, setc, visual, text, cam, bg = [p.strip() for p in line.split(' | ')]
        vis[int(n)] = dict(set=setc, visual=visual, text=text, cam=cam, bg=bg)
    return vis

PLACES = {
    'ABBOTTABAD': (34.15, 73.22), 'KAKUL MILITARY ACADEMY': (34.19, 73.27), 'KAKUL ACADEMY': (34.19, 73.27),
    'BILAL TOWN': (34.17, 73.24), 'PESHAWAR': (34.01, 71.58), 'ISLAMABAD': (33.69, 73.06), 'KARACHI': (24.86, 67.0),
    'TORA BORA': (34.12, 70.2), 'JALALABAD': (34.43, 70.45), 'BAGRAM AIRFIELD': (34.95, 69.26), 'KHOST': (33.34, 69.92),
    'CAMP CHAPMAN': (33.34, 69.92), 'KABUL': (34.53, 69.17), 'PAKISTAN': (30.0, 70.0), 'AFGHANISTAN': (33.9, 66.0),
    'NEW YORK': (40.71, -74.0), 'BOSTON': (42.36, -71.06), 'WASHINGTON': (38.9, -77.04), 'SHANKSVILLE': (40.02, -78.9),
    'NAWANSHER': (34.18, 73.25), 'INDIA': (31.0, 75.5), 'ARABIAN SEA': (21.0, 64.0), 'USA': (39.5, -98.0),
    'SAUDI ARABIA': (24.0, 45.0), 'JORDAN': (31.0, 36.5), 'NEVADA': (38.5, -116.8),
}
COUNTRY_FILL = {'PAKISTAN': 'Pakistan', 'AFGHANISTAN': 'Afghanistan', 'TORA BORA': 'Afghanistan', 'KHOST': 'Afghanistan',
                'CAMP CHAPMAN': 'Afghanistan', 'JALALABAD': 'Afghanistan', 'BAGRAM AIRFIELD': 'Afghanistan',
                'ABBOTTABAD': 'Pakistan', 'PESHAWAR': 'Pakistan', 'BILAL TOWN': 'Pakistan', 'KARACHI': 'Pakistan',
                'NEW YORK': 'United States of America', 'BOSTON': 'United States of America', 'USA': 'United States of America'}

def find_places(text):
    up = text.upper(); out = []
    for name in sorted(PLACES, key=len, reverse=True):
        i = up.find(name)
        if i >= 0 and not any(i >= a and i < b for _, a, b in out):
            out.append((name, i, i + len(name)))
    out.sort(key=lambda x: x[1])
    return [o[0] for o in out]

# ----------------------------------------------------------------------------- ink + paper helpers
def paper_grain(img, amount=10, seed=0):
    rng = np.random.default_rng(seed)
    a = np.asarray(img).astype(np.int16)
    n = rng.normal(0, amount, a.shape[:2])[..., None]
    n = np.asarray(Image.fromarray(np.clip(n + 128, 0, 255).astype(np.uint8)[..., 0]).filter(ImageFilter.GaussianBlur(0.8)), np.int16)[..., None] - 128
    return Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))

def vignette(img, strength=0.35):
    w, h = img.size
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    m = 1 - strength * np.clip(r - 0.6, 0, 1)
    return Image.fromarray(np.clip(np.asarray(img).astype(np.float32) * m[..., None], 0, 255).astype(np.uint8))

def grad(d, box, top, bot):
    x0, y0, x1, y1 = [int(v) for v in box]
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        d.line([(x0, y), (x1, y)], fill=tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)))

def lw(px):
    return max(1, int(px * S))

def person(d, x, y, h, body=(60, 70, 90), head=(70, 78, 98), hat=None, arm=None, outline=INK):
    """a flat silhouette figure (no face), feet at (x, y)"""
    hw = h * 0.16; hr = h * 0.095
    d.polygon([(x - hw, y - h * 0.62), (x + hw, y - h * 0.62), (x + hw * 1.15, y - h * 0.05), (x - hw * 1.15, y - h * 0.05)], fill=body, outline=outline, width=lw(3))
    d.rectangle((x - hw * 0.9, y - h * 0.08, x - hw * 0.25, y), fill=body, outline=outline, width=lw(2))
    d.rectangle((x + hw * 0.25, y - h * 0.08, x + hw * 0.9, y), fill=body, outline=outline, width=lw(2))
    d.ellipse((x - hr, y - h * 0.62 - hr * 2.1, x + hr, y - h * 0.62 + hr * 0.1), fill=head, outline=outline, width=lw(3))
    hy = y - h * 0.62 - hr * 2.1
    if hat == 'turban':
        d.ellipse((x - hr * 1.25, hy - hr * 0.35, x + hr * 1.25, hy + hr * 0.9), fill=(225, 220, 205), outline=outline, width=lw(3))
    elif hat == 'cap':
        d.chord((x - hr * 1.1, hy - hr * 0.2, x + hr * 1.1, hy + hr * 1.5), 180, 360, fill=(40, 45, 55), outline=outline, width=lw(3))
    elif hat == 'helmet':
        d.chord((x - hr * 1.2, hy - hr * 0.3, x + hr * 1.2, hy + hr * 1.6), 180, 360, fill=(70, 80, 60), outline=outline, width=lw(3))
    if arm == 'up':
        d.line([(x + hw, y - h * 0.58), (x + hw * 2.0, y - h * 0.82)], fill=body, width=lw(10))
    elif arm == 'phone':
        d.line([(x + hw, y - h * 0.58), (x + hr * 0.9, y - h * 0.7)], fill=body, width=lw(10))

# ----------------------------------------------------------------------------- illustrated backdrops
def puffs(im, x, y, rnd, n=40, drift=(20, -10), scale=1.0):
    """a soft billowing smoke column drawn as overlapping shaded puffs"""
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    for k in range(n):
        t = k / n
        cx = x + drift[0] * k * S * scale + rnd.uniform(-30, 30) * S * scale * (0.3 + t)
        cy = y + drift[1] * k * S * scale + rnd.uniform(-20, 20) * S * scale
        r = (30 + 140 * t) * S * scale * rnd.uniform(0.7, 1.2)
        g = int(80 + 70 * t + rnd.uniform(-10, 10))
        d.ellipse((cx - r, cy - r * 0.8, cx + r, cy + r * 0.8), fill=(g, g, g + 4, int(235 - 90 * t)))
        d.ellipse((cx - r * 0.6, cy - r * 0.7, cx + r * 0.3, cy - r * 0.1), fill=(g + 25, g + 25, g + 28, int(160 - 80 * t)))
    layer = layer.filter(ImageFilter.GaussianBlur(2 * S))
    im.paste(layer, (0, 0), layer)

def bd_night_compound(Wb, Hb, rnd):
    im = Image.new('RGB', (Wb, Hb)); d = ImageDraw.Draw(im)
    grad(d, (0, 0, Wb, Hb * 0.7), (12, 20, 48), (40, 55, 95))
    for _ in range(160):
        x, y = rnd.randrange(Wb), rnd.randrange(int(Hb * 0.6)); r = rnd.choice((1, 1, 2)) * S
        d.ellipse((x - r, y - r, x + r, y + r), fill=(235, 235, 210))
    mx, my = Wb * 0.82, Hb * 0.14
    d.ellipse((mx - 55 * S, my - 55 * S, mx + 55 * S, my + 55 * S), fill=(245, 238, 200)); d.ellipse((mx - 30 * S, my - 62 * S, mx + 75 * S, my + 45 * S), fill=(18, 26, 56))
    d.polygon([(0, Hb * 0.72), (Wb * 0.25, Hb * 0.6), (Wb * 0.55, Hb * 0.66), (Wb * 0.8, Hb * 0.58), (Wb, Hb * 0.66), (Wb, Hb), (0, Hb)], fill=(22, 30, 40))
    # house (three storeys) behind a wall
    hx0, hx1 = Wb * 0.33, Wb * 0.67
    d.rectangle((hx0, Hb * 0.36, hx1, Hb * 0.82), fill=(95, 92, 88), outline=INK, width=lw(4))
    d.rectangle((hx0 + 40 * S, Hb * 0.22, hx1 - 40 * S, Hb * 0.36), fill=(85, 82, 80), outline=INK, width=lw(4))
    d.rectangle((hx0 + 20 * S, Hb * 0.30, hx1 - 20 * S, Hb * 0.37), fill=(110, 105, 100), outline=INK, width=lw(4))   # balcony wall
    for k in range(4):
        wx = hx0 + 60 * S + k * (hx1 - hx0 - 120 * S) / 3
        lit = k == 1
        d.rectangle((wx - 22 * S, Hb * 0.5, wx + 22 * S, Hb * 0.58), fill=(255, 205, 120) if lit else (35, 40, 55), outline=INK, width=lw(3))
    d.rectangle((0, Hb * 0.7, Wb, Hb), fill=(120, 115, 108), outline=INK, width=lw(4))
    for x in range(0, Wb, int(60 * S)):
        d.line([(x, Hb * 0.7), (x + 30 * S, Hb * 0.68), (x + 60 * S, Hb * 0.7)], fill=(160, 160, 165), width=lw(2))   # barbed wire
    d.rectangle((0, Hb * 0.7, Wb, Hb * 0.72), fill=(90, 86, 80))
    return im

def bd_skyline(Wb, Hb, rnd, smoke=False):
    im = Image.new('RGB', (Wb, Hb)); d = ImageDraw.Draw(im)
    grad(d, (0, 0, Wb, Hb * 0.72), (95, 160, 220), (200, 225, 240))
    for _ in range(4):
        cx, cy = rnd.randrange(Wb), rnd.randrange(int(Hb * 0.05), int(Hb * 0.3)); k = rnd.uniform(0.8, 1.4) * S
        for dx, dy, r in ((-60, 0, 34), (-20, -20, 44), (30, -10, 38), (66, 4, 28)):
            d.ellipse((cx + (dx - r) * k, cy + (dy - r) * k, cx + (dx + r) * k, cy + (dy + r) * k), fill=(250, 250, 252))
    base = Hb * 0.74
    for i in range(46):
        x = i * Wb / 44 + rnd.randint(-10, 10) * S; bw = rnd.randint(40, 80) * S; bh = rnd.randint(80, 260) * S
        col = rnd.choice([(120, 135, 160), (140, 150, 170), (105, 118, 140)])
        d.rectangle((x, base - bh, x + bw, base), fill=col, outline=INK, width=lw(3))
        for wy in range(int(base - bh + 14 * S), int(base - 8 * S), int(22 * S)):
            d.line([(x + 8 * S, wy), (x + bw - 8 * S, wy)], fill=(175, 190, 210), width=lw(3))
    tx = Wb * 0.58
    for k in range(2):
        x = tx + k * 95 * S
        d.rectangle((x, base - 470 * S, x + 70 * S, base), fill=(165, 175, 190), outline=INK, width=lw(4))
        for xx in range(int(x + 8 * S), int(x + 66 * S), int(9 * S)):
            d.line([(xx, base - 460 * S), (xx, base)], fill=(140, 150, 168), width=lw(2))
    if smoke:
        puffs(im, tx + 80 * S, base - 440 * S, rnd, n=60, drift=(26, -8))
    d.rectangle((0, base, Wb, Hb), fill=(60, 95, 130))
    for _ in range(40):
        x = rnd.randrange(Wb); y = rnd.randrange(int(base + 10 * S), Hb)
        d.arc((x, y, x + 50 * S, y + 14 * S), 200, 340, fill=(140, 180, 210), width=lw(3))
    return im

def bd_pentagon(Wb, Hb, rnd):
    im = Image.new('RGB', (Wb, Hb)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, Wb, Hb), fill=(110, 140, 95))
    for _ in range(60):
        x, y = rnd.randrange(Wb), rnd.randrange(Hb); r = rnd.randint(10, 40) * S
        d.ellipse((x - r, y - r, x + r, y + r), fill=(90, 125, 80))
    cx, cy, R1 = Wb * 0.45, Hb * 0.55, 330 * S
    for ring, col in ((1.0, (190, 185, 170)), (0.72, (160, 155, 145)), (0.45, (190, 185, 170)), (0.25, (120, 150, 100))):
        pts = [(cx + R1 * ring * math.cos(math.radians(-90 + k * 72)), cy + R1 * ring * math.sin(math.radians(-90 + k * 72))) for k in range(5)]
        d.polygon(pts, fill=col, outline=INK, width=lw(4))
    puffs(im, cx + R1 * 0.6, cy - R1 * 0.2, rnd, n=50, drift=(16, -14))
    return im

def bd_field(Wb, Hb, rnd):
    im = Image.new('RGB', (Wb, Hb)); d = ImageDraw.Draw(im)
    grad(d, (0, 0, Wb, Hb * 0.55), (150, 160, 175), (205, 210, 215))
    d.polygon([(0, Hb * 0.55), (Wb * 0.3, Hb * 0.5), (Wb * 0.6, Hb * 0.54), (Wb, Hb * 0.5), (Wb, Hb), (0, Hb)], fill=(105, 135, 70))
    puffs(im, Wb * 0.72, Hb * 0.5, rnd, n=22, drift=(5, -16), scale=0.45)
    for _ in range(200):
        x = rnd.randrange(Wb); y = rnd.randrange(int(Hb * 0.56), Hb)
        d.line([(x, y), (x + 3 * S, y - 12 * S)], fill=(80, 110, 55), width=lw(2))
    d.line([(Wb * 0.15, Hb * 0.95), (Wb * 0.15, Hb * 0.62)], fill=(110, 80, 50), width=lw(14))
    d.line([(0, Hb * 0.75), (Wb * 0.3, Hb * 0.72)], fill=(110, 80, 50), width=lw(5))
    return im

def bd_memorial(Wb, Hb, rnd):
    im = Image.new('RGB', (Wb, Hb)); d = ImageDraw.Draw(im)
    grad(d, (0, 0, Wb, Hb), (14, 14, 22), (34, 30, 36))
    for row in range(4):
        for k in range(22):
            x = (k + 0.5) * Wb / 22 + (row % 2) * 20 * S; y = Hb * (0.6 + row * 0.1)
            glow = Image.new('L', (int(80 * S), int(80 * S)), 0)
            d.rectangle((x - 7 * S, y - 26 * S, x + 7 * S, y), fill=(235, 225, 205), outline=INK)
            d.ellipse((x - 5 * S, y - 42 * S, x + 5 * S, y - 26 * S), fill=(255, 200, 90))
            d.ellipse((x - 18 * S, y - 50 * S, x + 18 * S, y - 18 * S), outline=(120, 90, 40))
    return im.filter(ImageFilter.GaussianBlur(0.6))

def bd_mountains(Wb, Hb, rnd, night=False, camp=False):
    im = Image.new('RGB', (Wb, Hb)); d = ImageDraw.Draw(im)
    if night: grad(d, (0, 0, Wb, Hb * 0.7), (16, 22, 45), (55, 60, 90))
    elif camp: grad(d, (0, 0, Wb, Hb * 0.7), (70, 80, 120), (235, 160, 100))
    else: grad(d, (0, 0, Wb, Hb * 0.7), (120, 170, 215), (215, 228, 238))
    for layer, (base, amp, col, snow) in enumerate(((0.52, 0.28, (120, 120, 135), True), (0.64, 0.22, (110, 95, 80), True), (0.78, 0.16, (95, 80, 62), False))):
        pts = [(0, Hb)]; x = 0
        while x <= Wb:
            pts.append((x, Hb * base - rnd.uniform(0.2, 1.0) * Hb * amp)); x += rnd.randint(90, 200) * S
        pts += [(Wb, Hb)]
        c = col if not night else tuple(int(v * 0.45) for v in col)
        d.polygon(pts, fill=c, outline=INK, width=lw(3))
        if snow:
            for i in range(1, len(pts) - 2):
                (xa, ya), (xb, yb) = pts[i], pts[i + 1]
                if ya < Hb * (base - amp * 0.5):
                    d.polygon([(xa, ya), (xa + (xb - xa) * 0.3, ya + (yb - ya) * 0.3 + 25 * S), (xa - 30 * S, ya + 40 * S)], fill=(240, 242, 248) if not night else (150, 155, 175))
    if camp:
        d.ellipse((Wb * 0.2, Hb * 0.62, Wb * 0.36, Hb * 0.86), fill=(30, 25, 22), outline=INK, width=lw(4))   # cave mouth
        fx, fy = Wb * 0.55, Hb * 0.9
        for k, col in enumerate(((240, 120, 40), (250, 190, 70))):
            r = (40 - k * 15) * S; d.polygon([(fx - r, fy), (fx, fy - r * 2.4), (fx + r, fy)], fill=col)
        for k, (px, hat) in enumerate(((0.44, 'turban'), (0.5, 'turban'), (0.62, 'turban'), (0.68, None))):
            person(d, Wb * px, Hb * 0.97, (260 if k != 3 else 330) * S, body=(70, 60, 50) if k != 3 else (40, 40, 45), head=(80, 68, 56) if k != 3 else (40, 40, 45), hat=hat)
        d.rectangle((Wb * 0.56, Hb * 0.86, Wb * 0.6, Hb * 0.9), fill=(70, 75, 60), outline=INK, width=lw(3))     # radio
    return im

def bd_ops_room(Wb, Hb, rnd):
    im = Image.new('RGB', (Wb, Hb)); d = ImageDraw.Draw(im)
    grad(d, (0, 0, Wb, Hb), (20, 26, 38), (38, 44, 58))
    for r in range(3):
        for c in range(6):
            x0 = Wb * 0.06 + c * Wb * 0.148; y0 = Hb * 0.08 + r * Hb * 0.19
            d.rectangle((x0, y0, x0 + Wb * 0.135, y0 + Hb * 0.16), fill=(30, 60, 90), outline=INK, width=lw(4))
            for gy in range(2):
                for gx in range(4):
                    px = x0 + 12 * S + gx * Wb * 0.031; py = y0 + 12 * S + gy * Hb * 0.07
                    d.rectangle((px, py, px + Wb * 0.024, py + Hb * 0.055), fill=(200, 210, 220))
                    d.ellipse((px + 8 * S, py + 6 * S, px + Wb * 0.024 - 8 * S, py + 30 * S), fill=(120, 130, 145))
    d.rectangle((0, Hb * 0.68, Wb, Hb), fill=(45, 50, 62))
    for k in range(4):
        x = Wb * (0.12 + k * 0.24)
        d.rectangle((x - 120 * S, Hb * 0.78, x + 120 * S, Hb * 0.84), fill=(70, 60, 50), outline=INK, width=lw(3))
        d.rectangle((x - 50 * S, Hb * 0.7, x + 50 * S, Hb * 0.78), fill=(25, 40, 60), outline=INK, width=lw(3))
        person(d, x + 10 * S, Hb * 1.02, 300 * S, body=(40, 46, 60), head=(46, 52, 66))
    return im

def bd_airport(Wb, Hb, rnd):
    im = Image.new('RGB', (Wb, Hb)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, Wb, Hb * 0.55), fill=(200, 205, 210))
    for x in range(0, Wb, int(140 * S)):
        d.rectangle((x, Hb * 0.06, x + 110 * S, Hb * 0.4), fill=(160, 190, 215), outline=INK, width=lw(3))
    d.rectangle((0, Hb * 0.5, Wb, Hb), fill=(150, 150, 155))
    d.rectangle((0, Hb * 0.55, Wb, Hb * 0.62), fill=(70, 72, 78), outline=INK, width=lw(4))      # carousel belt
    d.rectangle((Wb * 0.3, Hb * 0.7, Wb * 0.75, Hb * 0.76), fill=(185, 190, 195), outline=INK, width=lw(4))   # steel table
    for x in (Wb * 0.33, Wb * 0.72): d.rectangle((x, Hb * 0.76, x + 14 * S, Hb * 0.95), fill=(120, 120, 125), outline=INK)
    d.rounded_rectangle((Wb * 0.43, Hb * 0.6, Wb * 0.61, Hb * 0.71), radius=int(14 * S), fill=(25, 25, 30), outline=INK, width=lw(4))
    d.rectangle((Wb * 0.505, Hb * 0.57, Wb * 0.535, Hb * 0.6), outline=INK, width=lw(4))
    d.rectangle((Wb * 0.58, Hb * 0.62, Wb * 0.61, Hb * 0.66), fill=(240, 220, 120), outline=INK)
    for x, hat in ((0.22, 'cap'), (0.82, None)):
        person(d, Wb * x, Hb * 0.98, 420 * S, body=(40, 50, 75), head=(60, 66, 84), hat=hat)
    return im

def bd_montage(Wb, Hb, rnd):
    im = bd_mountains(Wb, Hb, rnd); d = ImageDraw.Draw(im)
    # white jeep on a road + two helicopters
    d.polygon([(0, Hb * 0.95), (Wb, Hb * 0.8), (Wb, Hb * 0.88), (0, Hb)], fill=(150, 130, 100))
    jx, jy = Wb * 0.3, Hb * 0.86
    d.rounded_rectangle((jx, jy - 70 * S, jx + 200 * S, jy), radius=int(12 * S), fill=(240, 240, 235), outline=INK, width=lw(4))
    d.rectangle((jx + 120 * S, jy - 110 * S, jx + 190 * S, jy - 70 * S), fill=(200, 220, 235), outline=INK, width=lw(4))
    for wx in (jx + 40 * S, jx + 160 * S): d.ellipse((wx - 26 * S, jy - 20 * S, wx + 26 * S, jy + 32 * S), fill=(30, 30, 30), outline=INK, width=lw(3))
    for hx, hy in ((Wb * 0.65, Hb * 0.2), (Wb * 0.82, Hb * 0.28)):
        d.ellipse((hx - 90 * S, hy - 30 * S, hx + 60 * S, hy + 30 * S), fill=(30, 34, 38), outline=INK)
        d.line([(hx + 50 * S, hy), (hx + 150 * S, hy - 10 * S)], fill=(30, 34, 38), width=lw(12))
        d.line([(hx - 160 * S, hy - 40 * S), (hx + 130 * S, hy - 40 * S)], fill=(20, 20, 24), width=lw(5))
    return im

BACKDROPS = {
    'night_compound': bd_night_compound, 'skyline': bd_skyline, 'skyline_smoke': lambda w, h, r: bd_skyline(w, h, r, smoke=True),
    'pentagon': bd_pentagon, 'field': bd_field, 'memorial': bd_memorial, 'mountains': bd_mountains,
    'mountains_night': lambda w, h, r: bd_mountains(w, h, r, night=True), 'mountains_camp': lambda w, h, r: bd_mountains(w, h, r, camp=True),
    'ops_room': bd_ops_room, 'airport': bd_airport, 'montage': bd_montage,
}

def backdrop(key, seed):
    Wb, Hb = int(W * 1.12), int(H * 1.12)
    f = BACKDROPS.get(key) or BACKDROPS['ops_room']
    im = f(Wb, Hb, random.Random(seed))
    return vignette(paper_grain(im, 7, seed), 0.45)

# ----------------------------------------------------------------------------- paper map
_world = None
def countries():
    global _world
    if _world is None: _world = json.load(open(os.path.join(HERE, 'data', 'world.json')))
    return _world

def paper_map(lat0, lat1, lon0, lon1, fills, Wm, Hm):
    """beige paper map of the given box; countries in `fills` are salmon"""
    real = LOOK == 'real'
    land, sea, border, hl = ((30, 40, 48), (9, 17, 25), (78, 112, 128), (196, 120, 46)) if real else (PAPER, (222, 220, 212), (150, 145, 138), (214, 158, 128))
    im = Image.new('RGB', (Wm, Hm), sea); d = ImageDraw.Draw(im)
    def tr(lon, lat): return ((lon - lon0) / (lon1 - lon0) * Wm, (lat1 - lat) / (lat1 - lat0) * Hm)
    mask = Image.new('L', (Wm, Hm), 0); md = ImageDraw.Draw(mask)
    for name, rings in countries().items():
        for ring in rings:
            xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
            if max(xs) < lon0 - 5 or min(xs) > lon1 + 5 or max(ys) < lat0 - 5 or min(ys) > lat1 + 5: continue
            pts = [tr(lon, lat) for lon, lat in ring]
            d.polygon(pts, fill=hl if name in fills else land, outline=border)
            if name in fills: md.polygon(pts, fill=255)
    if real:
        edge = ImageChops.subtract(mask.filter(ImageFilter.MaxFilter(7)), mask.filter(ImageFilter.MinFilter(7))).filter(ImageFilter.GaussianBlur(5))
        glow = Image.new('RGB', (Wm, Hm), (255, 190, 110)); im.paste(glow, (0, 0), edge.point(lambda v: min(255, v * 3)))
        for gx in range(0, Wm, int(Wm / 24)): d.line([(gx, 0), (gx, Hm)], fill=(20, 32, 42))
        for gy in range(0, Hm, int(Hm / 14)): d.line([(0, gy), (Wm, gy)], fill=(20, 32, 42))
        return vignette(paper_grain(im, 6, 3), 0.5)
    return paper_grain(im, 5, 3)

# ----------------------------------------------------------------------------- captions + props
def caption_img(text):
    """real look: documentary lower third (white condensed capitals + red bar); comic look: handwritten ink"""
    if LOOK == 'real':
        t = R.text_img(text, 'oswald500.ttf', 58, (250, 250, 250), (10, 10, 12), 2, maxw=W * 0.62)
        bar = int(10 * S); pad = int(18 * S)
        im = Image.new('RGBA', (t.width + bar + pad, t.height), (0, 0, 0, 0))
        ImageDraw.Draw(im).rectangle((0, int(t.height * 0.2), bar, int(t.height * 0.78)), fill=(205, 35, 35))
        im.alpha_composite(t, (bar + pad, 0))
        return im
    return R.text_img(text, 'patrick.ttf', 74, (40, 36, 34), (250, 248, 240), 5, maxw=W * 0.78)

def title_img(text):
    if LOOK == 'real':
        t = R.text_img(text, 'oswald700.ttf', 120 if len(text) < 16 else 92, (255, 255, 255), (8, 8, 10), 3, maxw=W * 0.8)
        im = Image.new('RGBA', (t.width, t.height + int(26 * S)), (0, 0, 0, 0)); im.alpha_composite(t, (0, 0))
        ImageDraw.Draw(im).rectangle((int(t.width * 0.3), t.height + int(4 * S), int(t.width * 0.7), t.height + int(12 * S)), fill=(205, 35, 35))
        return im
    return R.text_img(text, 'bangers.ttf', 126 if len(text) < 16 else 96, (250, 205, 40), (40, 28, 18), 8, maxw=W * 0.8)

def datestamp_img(day, month, year):
    """typewriter date stamp (real look)"""
    t = R.text_img(f'{month} {int(day)}, {year}', 'specialelite.ttf', 52, (240, 240, 235), (10, 10, 10), 2)
    im = Image.new('RGBA', (t.width + int(30 * S), t.height + int(10 * S)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, im.width - 1, im.height - 1), fill=(0, 0, 0, 120))
    d.rectangle((0, 0, int(8 * S), im.height - 1), fill=(205, 35, 35))
    im.alpha_composite(t, (int(22 * S), int(5 * S)))
    return im

MONTHS = 'JANUARY FEBRUARY MARCH APRIL MAY JUNE JULY AUGUST SEPTEMBER OCTOBER NOVEMBER DECEMBER'.split()
def find_date(text):
    m = re.search(r'(' + '|'.join(MONTHS) + r')\s+(\d{1,2}),?\s+(\d{4})', text.upper())
    if m: return m.group(2), m.group(1), m.group(3)
    m = re.search(r'(\d{1,2})\s+(' + '|'.join(MONTHS) + r')\s+(\d{4})', text.upper())
    if m: return m.group(1), m.group(2), m.group(3)
    return None

def calendar_img(day, month, year):
    w, h = int(230 * S), int(260 * S)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, int(20 * S), w - 1, h - 1), radius=int(10 * S), fill=(248, 245, 236), outline=INK, width=lw(4))
    d.rectangle((0, int(20 * S), w - 1, int(62 * S)), fill=(205, 60, 50), outline=INK, width=lw(4))
    for x in (w * 0.3, w * 0.7): d.ellipse((x - 9 * S, 4 * S, x + 9 * S, 36 * S), fill=(120, 120, 125), outline=INK, width=lw(3))
    f1 = R.F('bangers.ttf', 100); f2 = R.F('patrick.ttf', 34)
    d.text((w / 2, 140 * S), day, font=f1, fill=INK, anchor='mm')
    d.text((w / 2, 205 * S), month, font=f2, fill=INK, anchor='mm')
    d.text((w / 2, 236 * S), year, font=f2, fill=INK, anchor='mm')
    return R.shadowed(im.rotate(-4, expand=True, resample=Image.BICUBIC), off=int(6 * S), blur=int(6 * S), alpha=90)

_grain = None
def grain_tile():
    global _grain
    if _grain is None:
        n = np.random.default_rng(5).normal(128, 60, (H, W + 200)).clip(0, 255).astype(np.uint8)
        _grain = Image.fromarray(n).convert('RGB')
    return _grain

_band = None
def band_img():
    """soft dark gradient behind the lower third so captions stay readable"""
    global _band
    if _band is None:
        _band = Image.new('RGBA', (W, int(H * 0.3)), (0, 0, 0, 0)); bd = ImageDraw.Draw(_band)
        for yy in range(_band.height): bd.line([(0, yy), (W, yy)], fill=(0, 0, 0, int(150 * yy / _band.height)))
    return _band

# ----------------------------------------------------------------------------- scene renderer
class Scene:
    def __init__(self, sn, v, dur, prev_set):
        self.sn, self.v, self.dur = sn, v, dur
        self.segs = [s.strip() for s in v['text'].split(' / ') if s.strip()]
        self.img_path = os.path.join(IMAGES, f'{sn:03d}.png')
        setc = v['set']
        if setc == 'MAP':
            self.setup_map()
        elif os.path.exists(self.img_path):
            im = Image.open(self.img_path).convert('RGB')
            r = max(W * 1.12 / im.width, H * 1.12 / im.height)
            self.bg = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
            self.bg = paper_grain(self.bg, 4, sn)
        else:
            self.bg = backdrop(v['bg'], sn)
        d = find_date(v['text'])
        self.cal = (datestamp_img(*d) if LOOK == 'real' else calendar_img(*d)) if d else None
        self._t = {}
        m = re.search(r'([\d,]+)', v['text'])
        self.counter = None
        if setc == 'TITLE' and m and len(self.segs) == 1 and re.fullmatch(r'[\d,]+', self.segs[0]):
            self.counter = int(m.group(1).replace(',', ''))

    def setup_map(self):
        places = find_places(self.v['visual'] + ' ' + self.v['text']) or ['PAKISTAN']
        broad = {'PAKISTAN', 'AFGHANISTAN', 'USA', 'INDIA', 'SAUDI ARABIA', 'JORDAN'}
        if any(p not in broad for p in places) and not re.search(r'world map|lines from the USA', self.v['visual']):
            keep = [p for p in places if p not in broad]
            self.fill_only = [p for p in places if p in broad]
            places = keep
        else:
            self.fill_only = []
        self.route = bool(re.search(r'line|route|path|crossing|leaving|arrow', self.v['visual'], re.I)) and len(places) >= 2
        pts = [PLACES[p] for p in places]
        lats = [p[0] for p in pts]; lons = [p[1] for p in pts]
        span = max(15.0, (max(lons) - min(lons)) * 1.6, (max(lats) - min(lats)) * 1.6 * 16 / 9)
        if any(p in ('NEW YORK', 'BOSTON', 'USA') for p in places) and any(PLACES[p][1] > 30 for p in places):
            span = max(span, 170)
        clon, clat = (max(lons) + min(lons)) / 2, (max(lats) + min(lats)) / 2
        far = span * 2.2
        lon0, lon1 = clon - far / 2, clon + far / 2
        latspan = far * 9 / 16
        lat0, lat1 = clat - latspan / 2, clat + latspan / 2
        Wm, Hm = int(W * 2.2), int(H * 2.2)
        fills = {c for c in (COUNTRY_FILL.get(p) for p in places + self.fill_only) if c}
        self.map = paper_map(lat0, lat1, lon0, lon1, fills, Wm, Hm)
        self.mbox = (lat0, lat1, lon0, lon1); self.span = span; self.places = places
        self.mpx = lambda lat, lon: ((lon - lon0) / (lon1 - lon0) * Wm, (lat1 - lat) / (lat1 - lat0) * Hm)

    def caption(self, text, t):
        key = ('c', text)
        if key not in self._t: self._t[key] = caption_img(text)
        return self._t[key]

    def frame(self, t):
        v = self.v; setc = v['set']; dur = self.dur
        prog = t / max(dur, 0.01)
        if setc == 'MAP':
            k = ease(t / 1.6)
            z = 2.2 + (1.0 - 2.2) * k - 0.05 * max(0, t - 1.6) / max(0.5, dur - 1.6)      # zoom factor relative to target span
            Wm, Hm = self.map.size
            vw = Wm / 2.2 * z; vh = vw * 9 / 16
            cx, cy = Wm / 2, Hm / 2
            img = self.map.crop((int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))).resize((W, H), Image.BILINEAR).convert('RGBA')
            d = ImageDraw.Draw(img)
            sc = W / vw
            scr = lambda name: ((self.mpx(*PLACES[name])[0] - (cx - vw / 2)) * sc, (self.mpx(*PLACES[name])[1] - (cy - vh / 2)) * sc)
            if self.route:
                k2 = ease((t - 1.9) / 1.4)
                if k2 > 0:
                    (ax, ay), (bx, by) = scr(self.places[0]), scr(self.places[1])
                    mx_, my_ = (ax + bx) / 2 - (by - ay) * 0.25, (ay + by) / 2 + (bx - ax) * 0.25
                    us = np.linspace(0, k2, 60)
                    pts = [((1 - u) ** 2 * ax + 2 * (1 - u) * u * mx_ + u * u * bx, (1 - u) ** 2 * ay + 2 * (1 - u) * u * my_ + u * u * by) for u in us]
                    for i in range(0, len(pts) - 1, 2):
                        d.line([pts[i], pts[i + 1]], fill=(235, 60, 50) if LOOK == 'real' else (200, 45, 40), width=lw(6))
            labeled = []
            for i, name in enumerate(self.places):
                at = 1.3 + i * 0.5
                if t < at: continue
                px, py = self.mpx(*PLACES[name]); X = (px - (cx - vw / 2)) * sc; Y = (py - (cy - vh / 2)) * sc
                drop = (1 - ease_out((t - at) / 0.35)) * 60 * S
                Y2 = Y - drop
                d.ellipse((X - 6 * S, Y - 3 * S, X + 6 * S, Y + 3 * S), fill=(150, 140, 130))
                d.line([(X, Y2), (X, Y2 - 34 * S)], fill=(90, 90, 95), width=lw(4))
                d.ellipse((X - 13 * S, Y2 - 58 * S, X + 13 * S, Y2 - 32 * S), fill=(215, 40, 35), outline=INK, width=lw(2))
                if LOOK == 'real':
                    pr = (((t - at) * 0.9) % 1.0) * 50 * S
                    d.ellipse((X - pr, Y - pr * 0.6, X + pr, Y + pr * 0.6), outline=(235, 70, 60), width=lw(3))
                n = len(name); kk = min(1.0, (t - at - 0.2) / (0.05 * n + 0.2))
                if kk > 0:
                    sub = name[: max(1, int(n * kk))]
                    key = ('p', sub)
                    if key not in self._t:
                        self._t[key] = (R.text_img(sub, 'oswald500.ttf', 40, (255, 255, 255), (5, 5, 8), 2) if LOOK == 'real'
                                        else R.text_img(sub, 'patrick.ttf', 46, (40, 36, 34), (245, 242, 232), 3))
                    lab = self._t[key]
                    ly = Y2 - 46 * S - lab.height / 2
                    for (ox, oy, oh) in labeled:          # keep labels from overlapping
                        if abs(ly - oy) < oh * 0.9 and abs(X - ox) < 300 * S: ly = oy + oh * 0.95
                    labeled.append((X, ly, lab.height))
                    img.alpha_composite(lab, (int(X + 18 * S), int(ly)))
        else:
            bg = self.bg
            mx, my = bg.width - W, bg.height - H
            z = 1 - 0.07 * ease(prog)                       # slow push-in
            cw, ch = int(W + mx * z), int(H + my * z)
            x0 = (bg.width - cw) // 2; y0 = (bg.height - ch) // 2
            img = bg.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR).convert('RGBA')
            if v['bg'] == 'night_compound' and not os.path.exists(self.img_path):
                # the pacer on the balcony: a tall faceless silhouette walking back and forth
                d = ImageDraw.Draw(img)
                px = W * (0.44 + 0.1 * math.sin(t * 1.4)); py = H * 0.335
                person(d, px, py, 120 * S, body=(15, 15, 20), head=(15, 15, 20), outline=(15, 15, 20))
            if v['bg'] in ('skyline_smoke', 'pentagon') and not os.path.exists(self.img_path):
                pass
        # calendar prop
        if self.cal is not None and setc != 'MAP':
            k = ease_out(t / 0.45)
            if LOOK == 'real':
                img.alpha_composite(self.cal, (int(W * 0.05 - (1 - k) * 400 * S), int(H * 0.07)))
            else:
                img.alpha_composite(self.cal, (int(W * 0.06 - (1 - k) * 300 * S), int(H * 0.42)))
        # text
        n = len(self.segs)
        if n:
            idx = min(n - 1, int(t / max(1.2, dur / n)))
            seg = self.segs[idx]; st = idx * max(1.2, dur / n)
            ts = t - st
            if setc == 'TITLE' or (len(seg) <= 14 and seg.isupper() and setc != 'MAP' and n == 1 and v['set'] == 'TITLE'):
                if self.counter is not None and ts < 1.4:
                    shown = f'{int(self.counter * ease_out(ts / 1.4)):,}'
                else:
                    shown = seg
                key = ('T', shown)
                if key not in self._t: self._t[key] = title_img(shown)
                ti = self._t[key]
                sc = 1 + 0.4 * (1 - ease_out(ts / 0.2)) if ts < 0.2 else 1.0
                tw = ti if sc == 1 else ti.resize((int(ti.width * sc), int(ti.height * sc)), Image.BILINEAR)
                img.alpha_composite(tw, (int(W / 2 - tw.width / 2), int(H * 0.5 - tw.height / 2)))
            else:
                ci = self.caption(seg, ts)
                # fade in + red underline swoosh drawn left to right
                a = ease(ts / 0.35)
                if a < 1:
                    ci = ci.copy(); ci.putalpha(ci.split()[3].point(lambda p: int(p * a)))
                if LOOK == 'real':
                    x0 = int(W * 0.05 - (1 - ease_out(ts / 0.4)) * 40 * S); y0 = int(H * 0.8 - ci.height / 2)
                    img.alpha_composite(band_img(), (0, H - band_img().height))
                    img.alpha_composite(ci, (x0, y0))
                else:
                    cx = W / 2; cy = H * 0.11
                    x0 = int(cx - ci.width / 2); y0 = int(cy - ci.height / 2)
                    img.alpha_composite(ci, (x0, y0))
                u = ease((ts - 0.15) / 0.5) if LOOK != 'real' else 0
                if u > 0:
                    d = ImageDraw.Draw(img)
                    ux0 = x0 + 20 * S; ux1 = x0 + ci.width - 20 * S; uy = y0 + ci.height - 12 * S
                    pts = [(ux0 + (ux1 - ux0) * q, uy + math.sin(q * 3.1) * 4 * S - q * 6 * S) for q in np.linspace(0, u, 24)]
                    d.line(pts, fill=RED_UL, width=lw(6), joint='curve')
        if LOOK == 'real' and self.sn == 1 and t < 5.5:
            key = ('disc',)
            if key not in self._t: self._t[key] = R.text_img('DRAMATIZED RECONSTRUCTION · AI-GENERATED IMAGES', 'oswald500.ttf', 30, (230, 230, 230), (0, 0, 0), 2)
            dimg = self._t[key].copy(); a = min(1, t / 0.5, (5.5 - t) / 0.5)
            dimg.putalpha(dimg.split()[3].point(lambda p: int(p * a * 0.85)))
            img.alpha_composite(dimg, (int(W - dimg.width - 30 * S), int(H - dimg.height - 24 * S)))
        if LOOK == 'real':
            g = grain_tile(); ox = random.Random(int(t * FPS)).randrange(0, g.width - W)
            img = Image.blend(img.convert('RGB'), g.crop((ox, 0, ox + W, H)), 0.035)
        return img.convert('RGB')

# ----------------------------------------------------------------------------- driver (same audio pipeline as the Egypt video)
def render_scene(args):
    sn, v, dur, prev_set, nf = args
    path = os.path.join(OUT, 'seg', f'{sn:03d}.mp4')
    if os.path.exists(path) and os.path.getsize(path) > 1000: return path
    sc = Scene(sn, v, dur, prev_set)
    cmd = ['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', path + '.tmp.mp4']
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(nf): pr.stdin.write(sc.frame(k / FPS).tobytes())
    pr.stdin.close(); pr.wait(); os.replace(path + '.tmp.mp4', path)
    return path

def main():
    vis = load_visuals()
    tim = json.load(open(os.path.join(OUT, 'timing.json'))); scenes = tim['scenes']
    first, last = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) >= 3 else (1, len(scenes))
    os.makedirs(os.path.join(OUT, 'seg'), exist_ok=True)
    jobs = []
    for sn in range(first, last + 1):
        s = scenes[sn - 1]
        nf = round(s['end'] * FPS) - round(s['start'] * FPS)
        jobs.append((sn, vis[sn], s['end'] - s['start'], vis.get(sn - 1, {}).get('set'), nf))
    with Pool(int(os.environ.get('WORKERS', os.cpu_count() or 2))) as pool:
        for k, _ in enumerate(pool.imap(render_scene, jobs), 1): print(f'scene {jobs[k - 1][0]} done', flush=True)
    lst = os.path.join(OUT, f'segments_{first}_{last}.txt')
    with open(lst, 'w') as f:
        for j in jobs: f.write(f"file 'seg/{j[0]:03d}.mp4'\n")
    t0 = scenes[first - 1]['start']; t1 = scenes[last - 1]['end']
    music = os.path.join(OUT, 'music.wav')
    mus_in = ['-ss', f'{t0:.3f}', '-t', f'{t1 - t0:.3f}', '-i', music] if os.path.exists(music) else []
    graph = ('[1:a]aresample=44100,asplit=2[v][key];'
             + ('[2:a]aresample=44100,lowpass=f=7000,volume=0.18[m0];[m0][key]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=600[m];'
                '[v][m]amix=inputs=2:duration=first:normalize=0' if mus_in else '[key]anullsink;[v]anull')
             + ',loudnorm=I=-16:TP=-1.5[a]')
    name = os.environ.get('NAME', 'The_Hunt_for_Osama_bin_Laden.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
                    '-ss', f'{t0:.3f}', '-t', f'{t1 - t0:.3f}', '-i', os.path.join(OUT, 'narration.wav'), *mus_in,
                    '-filter_complex', graph, '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-movflags', '+faststart', os.path.join(OUT, name)], check=True)
    print('wrote', os.path.join(OUT, name))

if __name__ == '__main__':
    main()
