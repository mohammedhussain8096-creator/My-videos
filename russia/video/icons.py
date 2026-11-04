"""Small cartoon icons drawn in code (no emoji, no clip-art), in the reference video's flat style.
Every function returns an RGBA PIL image roughly `s` pixels tall."""
import math
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter

SS = 3   # supersampling
INK = (40, 28, 22, 255)
WHITE = (255, 255, 255, 255)
RED = (214, 52, 40, 255)
GOLD = (246, 196, 52, 255)
SKIN = (246, 211, 178, 255)

def _canvas(w, h):
    im = Image.new('RGBA', (w * SS, h * SS), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)

def _done(im, w, h):
    return im.resize((w, h), Image.LANCZOS)

def _P(pts, k):
    return [(x * k, y * k) for x, y in pts]

def castle(s, col=(200, 40, 35, 255)):
    """Kremlin-style red fortress with white crenellations and towers (like the reference's city icon)."""
    w, h = int(s * 1.5), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    lw = int(4 * k)
    def tower(x, top, wd):
        d.rectangle(_P([(x, top + 18), (x + wd, 92)], k), fill=col, outline=INK, width=lw)
        d.polygon(_P([(x - 3, top + 20), (x + wd / 2, top - 6), (x + wd + 3, top + 20)], k), fill=WHITE, outline=INK, width=lw)
        d.rectangle(_P([(x + wd / 2 - 1.5, top - 16), (x + wd / 2 + 1.5, top - 6)], k), fill=GOLD)
    d.rectangle(_P([(10, 52), (140, 92)], k), fill=col, outline=INK, width=lw)
    for i in range(9):
        x = 14 + i * 14.5
        d.rectangle(_P([(x, 44), (x + 8, 54)], k), fill=WHITE, outline=INK, width=int(3 * k))
    tower(2, 28, 26); tower(122, 28, 26); tower(62, 4, 26)
    d.rectangle(_P([(68, 70), (82, 92)], k), fill=INK)
    return _done(im, w, h)

def flag(s, stripes, vertical=False):
    w, h = int(s * 1.45), s
    im, d = _canvas(w, h)
    n = len(stripes); W, H = w * SS, h * SS
    for i, c in enumerate(stripes):
        if vertical: d.rectangle([W * i / n, 0, W * (i + 1) / n, H], fill=c)
        else: d.rectangle([0, H * i / n, W, H * (i + 1) / n], fill=c)
    d.rectangle([0, 0, W - 1, H - 1], outline=WHITE, width=int(SS * max(2, s / 14)))
    return _done(im, w, h)

FLAGS = {
    'fr': (((0, 85, 164, 255), WHITE, (239, 65, 53, 255)), True),
    'ru': ((WHITE, (0, 57, 166, 255), (213, 43, 30, 255)), False),
    'pl': ((WHITE, (220, 20, 60, 255)), False),
    'at': (((200, 16, 46, 255), WHITE, (200, 16, 46, 255)), False),
    'it': (((0, 146, 70, 255), WHITE, (206, 43, 55, 255)), True),
    'de': (((20, 20, 20, 255), (221, 0, 0, 255), (255, 206, 0, 255)), False),
    'prussia': (((20, 20, 20, 255), WHITE), False),
    'se': (((0, 106, 167, 255), (254, 204, 0, 255), (0, 106, 167, 255)), False),
    'su': (((204, 0, 0, 255),), False),
}

def badge(s, who):
    """Round portrait badge (white ring) with a simple cartoon bust."""
    im, d = _canvas(s, s); k = SS * s / 100.0
    bgc = {'napoleon': (52, 84, 160, 255), 'tsar': (150, 40, 45, 255), 'kutuzov': (40, 105, 70, 255),
           'hitler': (90, 90, 90, 255), 'stalin': (150, 40, 45, 255), 'charles': (40, 90, 150, 255)}.get(who, (80, 80, 80, 255))
    d.ellipse(_P([(2, 2), (98, 98)], k), fill=WHITE)
    d.ellipse(_P([(8, 8), (92, 92)], k), fill=bgc)
    mask = Image.new('L', im.size, 0); ImageDraw.Draw(mask).ellipse(_P([(8, 8), (92, 92)], k), fill=255)
    bust = Image.new('RGBA', im.size, (0, 0, 0, 0)); b = ImageDraw.Draw(bust)
    coat = {'napoleon': (30, 45, 100, 255), 'tsar': (30, 70, 40, 255), 'kutuzov': (30, 70, 40, 255),
            'hitler': (110, 100, 70, 255), 'stalin': (180, 170, 130, 255), 'charles': (30, 50, 110, 255)}.get(who, INK)
    b.ellipse(_P([(18, 70), (82, 120)], k), fill=coat, outline=INK, width=int(3 * k))          # shoulders
    if who in ('napoleon', 'tsar', 'kutuzov'):
        b.polygon(_P([(42, 72), (50, 84), (58, 72)], k), fill=WHITE)                       # collar
        b.rectangle(_P([(20, 76), (30, 80)], k), fill=GOLD); b.rectangle(_P([(70, 76), (80, 80)], k), fill=GOLD)
    b.ellipse(_P([(33, 30), (67, 70)], k), fill=SKIN, outline=INK, width=int(3 * k))          # head
    hair = {'napoleon': (70, 45, 30, 255), 'kutuzov': (235, 235, 235, 255), 'tsar': (160, 120, 70, 255),
            'hitler': (40, 30, 25, 255), 'stalin': (40, 30, 25, 255), 'charles': (130, 90, 50, 255)}.get(who, INK)
    if who == 'napoleon':
        b.pieslice(_P([(14, 6), (86, 52)], k), 180, 360, fill=(25, 25, 30, 255), outline=INK, width=int(3 * k))  # bicorne
        b.ellipse(_P([(46, 22), (56, 32)], k), fill=(220, 40, 40, 255), outline=WHITE, width=int(2 * k))
        b.polygon(_P([(38, 36), (50, 34), (44, 46)], k), fill=hair)                          # forelock
    elif who == 'tsar':
        b.pieslice(_P([(32, 22), (68, 48)], k), 180, 360, fill=hair)
        b.polygon(_P([(36, 28), (36, 14), (43, 22), (50, 10), (57, 22), (64, 14), (64, 28)], k), fill=GOLD, outline=INK, width=int(2 * k))
    elif who == 'kutuzov':
        b.pieslice(_P([(31, 24), (69, 52)], k), 180, 360, fill=hair)
        b.ellipse(_P([(52, 44), (60, 52)], k), fill=INK); b.line(_P([(40, 38), (66, 50)], k), fill=INK, width=int(2 * k))
    elif who == 'hitler':
        b.pieslice(_P([(31, 24), (69, 50)], k), 180, 330, fill=hair)
        b.rectangle(_P([(46, 58), (54, 61)], k), fill=hair)
    elif who == 'stalin':
        b.pieslice(_P([(31, 22), (69, 50)], k), 180, 360, fill=hair)
        b.ellipse(_P([(40, 54), (60, 61)], k), fill=hair)
    elif who == 'charles':
        b.pieslice(_P([(28, 22), (72, 64)], k), 180, 360, fill=hair)
    if who != 'kutuzov':
        b.ellipse(_P([(41, 46), (45, 50)], k), fill=INK)
    b.ellipse(_P([(55, 46), (59, 50)], k), fill=INK) if who != 'kutuzov' else None
    b.arc(_P([(43, 52), (57, 62)], k), 20, 160, fill=INK, width=int(2 * k))
    from PIL import ImageChops
    bust.putalpha(ImageChops.multiply(bust.getchannel('A'), mask))
    im.alpha_composite(bust)
    d.ellipse(_P([(6, 6), (94, 94)], k), outline=WHITE, width=int(4 * k))
    return _done(im, s, s)

def flame(s, phase=0.0):
    w, h = int(s * 0.8), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    wob = 4 * math.sin(phase * 2 * math.pi)
    d.polygon(_P([(40 + wob, 0), (72, 52), (70, 82), (40, 100), (10, 82), (8, 52)], k), fill=(232, 72, 30, 255))
    d.polygon(_P([(40 - wob, 30), (60, 64), (56, 86), (40, 96), (24, 86), (20, 64)], k), fill=(250, 170, 40, 255))
    d.polygon(_P([(40 + wob / 2, 56), (50, 76), (40, 92), (30, 76)], k), fill=(255, 238, 140, 255))
    return _done(im, w, h).filter(ImageFilter.SMOOTH)

def xmark(s):
    im, d = _canvas(s, s); k = SS * s / 100.0
    for a, b in (((14, 14), (86, 86)), ((86, 14), (14, 86))):
        d.line(_P([a, b], k), fill=WHITE, width=int(30 * k))
    for a, b in (((18, 18), (82, 82)), ((82, 18), (18, 82))):
        d.line(_P([a, b], k), fill=RED, width=int(20 * k))
    return _done(im, s, s)

def crown(s):
    w, h = int(s * 1.3), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.polygon(_P([(10, 90), (6, 22), (36, 52), (65, 10), (94, 52), (124, 22), (120, 90)], k), fill=GOLD, outline=INK, width=int(5 * k))
    d.rectangle(_P([(10, 74), (120, 92)], k), fill=(232, 170, 40, 255), outline=INK, width=int(5 * k))
    for x, c in ((34, (220, 50, 50, 255)), (65, (60, 120, 220, 255)), (96, (60, 170, 90, 255))):
        d.ellipse(_P([(x - 7, 76), (x + 7, 90)], k), fill=c)
    return _done(im, w, h)

def soldier(s, coat=(40, 70, 170, 255)):
    w, h = int(s * 0.5), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    lw = int(3 * k)
    d.line(_P([(40, 6), (40, 96)], k), fill=(120, 120, 120, 255), width=int(3 * k))          # musket
    d.rectangle(_P([(16, 4), (34, 20)], k), fill=(25, 25, 30, 255))                          # shako
    d.ellipse(_P([(14, 16), (36, 38)], k), fill=SKIN, outline=INK, width=lw)
    d.rectangle(_P([(12, 38), (38, 70)], k), fill=coat, outline=INK, width=lw)
    d.line(_P([(12, 38), (38, 70)], k), fill=WHITE, width=int(3 * k)); d.line(_P([(38, 38), (12, 70)], k), fill=WHITE, width=int(3 * k))
    d.rectangle(_P([(14, 70), (22, 96)], k), fill=WHITE, outline=INK, width=lw)
    d.rectangle(_P([(28, 70), (36, 96)], k), fill=WHITE, outline=INK, width=lw)
    return _done(im, w, h)

def army(s, coat=(40, 70, 170, 255), n=5):
    one = soldier(s, coat)
    w = int(one.width * (0.62 * (n - 1) + 1)) + 4
    im = Image.new('RGBA', (w, int(s * 1.12)), (0, 0, 0, 0))
    for i in range(n):
        y = int(s * 0.12) if i % 2 else 0
        im.alpha_composite(one, (int(i * one.width * 0.62), y))
    return im

def snowflake(s):
    im, d = _canvas(s, s); k = SS * s / 100.0
    for a in range(0, 180, 60):
        r = math.radians(a)
        dx, dy = 44 * math.cos(r), 44 * math.sin(r)
        d.line(_P([(50 - dx, 50 - dy), (50 + dx, 50 + dy)], k), fill=WHITE, width=int(8 * k))
        for sg in (-1, 1):
            cx, cy = 50 + sg * dx * 0.6, 50 + sg * dy * 0.6
            for b in (a + 45, a - 45):
                rb = math.radians(b)
                d.line(_P([(cx, cy), (cx - sg * 14 * math.cos(rb), cy - sg * 14 * math.sin(rb))], k), fill=WHITE, width=int(6 * k))
    return _done(im, s, s)

def sun(s):
    im, d = _canvas(s, s); k = SS * s / 100.0
    for a in range(0, 360, 30):
        r = math.radians(a)
        d.line(_P([(50 + 30 * math.cos(r), 50 + 30 * math.sin(r)), (50 + 47 * math.cos(r), 50 + 47 * math.sin(r))], k),
               fill=(250, 190, 40, 255), width=int(8 * k))
    d.ellipse(_P([(24, 24), (76, 76)], k), fill=(252, 210, 60, 255), outline=(232, 140, 30, 255), width=int(5 * k))
    return _done(im, s, s)

def germ(s):
    im, d = _canvas(s, s); k = SS * s / 100.0
    for a in range(0, 360, 40):
        r = math.radians(a)
        d.line(_P([(50, 50), (50 + 46 * math.cos(r), 50 + 46 * math.sin(r))], k), fill=(90, 160, 60, 255), width=int(7 * k))
        d.ellipse(_P([(50 + 46 * math.cos(r) - 6, 50 + 46 * math.sin(r) - 6), (50 + 46 * math.cos(r) + 6, 50 + 46 * math.sin(r) + 6)], k), fill=(90, 160, 60, 255))
    d.ellipse(_P([(20, 20), (80, 80)], k), fill=(130, 200, 80, 255), outline=(60, 110, 40, 255), width=int(5 * k))
    for x, y in ((38, 40), (60, 46), (46, 62)):
        d.ellipse(_P([(x - 6, y - 6), (x + 6, y + 6)], k), fill=(70, 130, 50, 255))
    return _done(im, s, s)

def bowl(s):
    w, h = int(s * 1.3), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.chord(_P([(8, 10), (122, 96)], k), 0, 180, fill=(200, 140, 80, 255), outline=INK, width=int(5 * k))
    d.ellipse(_P([(8, 40), (122, 64)], k), fill=(120, 80, 50, 255), outline=INK, width=int(5 * k))
    return _done(im, w, h)

def horseshoe(s):
    im, d = _canvas(s, s); k = SS * s / 100.0
    d.arc(_P([(14, 10), (86, 90)], k), 160, 380, fill=(150, 150, 160, 255), width=int(18 * k))
    d.arc(_P([(14, 10), (86, 90)], k), 160, 380, fill=INK, width=int(4 * k))
    return _done(im, s, s)

def skull(s):
    im, d = _canvas(s, s); k = SS * s / 100.0
    d.ellipse(_P([(14, 6), (86, 74)], k), fill=WHITE, outline=INK, width=int(5 * k))
    d.rectangle(_P([(30, 62), (70, 92)], k), fill=WHITE, outline=INK, width=int(5 * k))
    d.ellipse(_P([(28, 34), (46, 54)], k), fill=INK); d.ellipse(_P([(54, 34), (72, 54)], k), fill=INK)
    for x in (40, 50, 60): d.line(_P([(x, 74), (x, 92)], k), fill=INK, width=int(4 * k))
    return _done(im, s, s)

def house(s, burning=False):
    w, h = s, s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.rectangle(_P([(18, 46), (82, 94)], k), fill=(196, 150, 100, 255), outline=INK, width=int(5 * k))
    d.polygon(_P([(8, 50), (50, 12), (92, 50)], k), fill=(140, 70, 40, 255), outline=INK, width=int(5 * k))
    d.rectangle(_P([(42, 66), (58, 94)], k), fill=(90, 55, 35, 255))
    return _done(im, w, h)

def wheat(s):
    w, h = int(s * 0.6), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.line(_P([(30, 30), (30, 98)], k), fill=(200, 150, 50, 255), width=int(6 * k))
    for i in range(5):
        y = 8 + i * 12
        d.ellipse(_P([(14, y), (29, y + 16)], k), fill=GOLD, outline=(160, 110, 30, 255), width=int(2 * k))
        d.ellipse(_P([(31, y), (46, y + 16)], k), fill=GOLD, outline=(160, 110, 30, 255), width=int(2 * k))
    return _done(im, w, h)

def bridge(s):
    w, h = int(s * 1.6), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.arc(_P([(6, 30), (154, 130)], k), 180, 360, fill=(150, 100, 60, 255), width=int(10 * k))
    d.line(_P([(6, 80), (154, 80)], k), fill=(150, 100, 60, 255), width=int(10 * k))
    for x in range(20, 150, 22): d.line(_P([(x, 80), (x, 100)], k), fill=(120, 80, 50, 255), width=int(6 * k))
    return _done(im, w, h)

def burst(s):
    im, d = _canvas(s, s); k = SS * s / 100.0
    pts = []
    for i in range(24):
        r = 48 if i % 2 == 0 else 26
        a = math.radians(i * 15)
        pts.append((50 + r * math.cos(a), 50 + r * math.sin(a)))
    d.polygon(_P(pts, k), fill=(246, 150, 40, 255), outline=(200, 60, 30, 255), width=int(4 * k))
    d.ellipse(_P([(34, 34), (66, 66)], k), fill=(255, 230, 120, 255))
    return _done(im, s, s)

def cannon(s):
    w, h = int(s * 1.4), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.polygon(_P([(20, 40), (130, 20), (134, 40), (24, 64)], k), fill=(60, 60, 64, 255), outline=INK, width=int(4 * k))
    d.ellipse(_P([(16, 44), (76, 104)], k), fill=(140, 90, 50, 255), outline=INK, width=int(5 * k))
    d.ellipse(_P([(40, 68), (52, 80)], k), fill=INK)
    return _done(im, w, h)

def hourglass(s):
    w, h = int(s * 0.7), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.rectangle(_P([(4, 2), (66, 12)], k), fill=(140, 90, 50, 255)); d.rectangle(_P([(4, 88), (66, 98)], k), fill=(140, 90, 50, 255))
    d.polygon(_P([(10, 12), (60, 12), (38, 50), (60, 88), (10, 88), (32, 50)], k), fill=(220, 235, 245, 200), outline=INK, width=int(4 * k))
    d.polygon(_P([(18, 88), (52, 88), (35, 66)], k), fill=GOLD)
    d.polygon(_P([(20, 20), (50, 20), (35, 42)], k), fill=GOLD)
    return _done(im, w, h)

def envelope(s):
    w, h = int(s * 1.4), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.rectangle(_P([(6, 14), (134, 90)], k), fill=(250, 240, 220, 255), outline=INK, width=int(5 * k))
    d.line(_P([(6, 14), (70, 60), (134, 14)], k), fill=INK, width=int(5 * k))
    d.ellipse(_P([(60, 50), (80, 70)], k), fill=RED)
    return _done(im, w, h)

def key(s):
    w, h = int(s * 1.6), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.ellipse(_P([(6, 20), (66, 80)], k), outline=GOLD, width=int(14 * k))
    d.line(_P([(64, 50), (150, 50)], k), fill=GOLD, width=int(14 * k))
    d.line(_P([(130, 50), (130, 76)], k), fill=GOLD, width=int(12 * k)); d.line(_P([(112, 50), (112, 70)], k), fill=GOLD, width=int(12 * k))
    return _done(im, w, h)

def question(s):
    from render_text import text_img
    return text_img('?', 'luckiest', s, (255, 214, 64), (70, 40, 10), max(3, s // 14))

@lru_cache(maxsize=256)
def get(kind, s):
    s = int(s)
    if kind.startswith('flag-'):
        st, v = FLAGS[kind[5:]]
        return flag(s, st, v)
    if kind.startswith('badge-'): return badge(s, kind[6:])
    if kind.startswith('army-'):
        coat = {'fr': (40, 70, 170, 255), 'ru': (40, 110, 60, 255), 'de': (110, 110, 100, 255), 'su': (120, 110, 60, 255),
                'se': (40, 90, 170, 255)}[kind[5:]]
        return army(s, coat)
    fn = {'castle': castle, 'xmark': xmark, 'crown': crown, 'snow': snowflake, 'sun': sun, 'germ': germ, 'bowl': bowl,
          'horseshoe': horseshoe, 'skull': skull, 'house': house, 'wheat': wheat, 'bridge': bridge, 'burst': burst,
          'cannon': cannon, 'hourglass': hourglass, 'envelope': envelope, 'key': key, 'question': question,
          'flame': flame}[kind]
    return fn(s)
