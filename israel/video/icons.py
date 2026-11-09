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
    'us': (((178, 34, 52, 255), WHITE, (178, 34, 52, 255), WHITE, (178, 34, 52, 255), WHITE, (60, 59, 110, 255)), False),
    'cn': (((222, 41, 16, 255),), False),
    'ua': (((0, 87, 183, 255), (255, 215, 0, 255)), False),
}

def badge(s, who):
    """Round portrait badge (white ring) with a simple cartoon bust."""
    im, d = _canvas(s, s); k = SS * s / 100.0
    bgc = {'napoleon': (52, 84, 160, 255), 'tsar': (150, 40, 45, 255), 'kutuzov': (40, 105, 70, 255),
           'hitler': (90, 90, 90, 255), 'stalin': (150, 40, 45, 255), 'charles': (40, 90, 150, 255),
           'mongol': (170, 120, 50, 255), 'ivan': (110, 40, 90, 255), 'peter': (40, 100, 70, 255), 'minin': (120, 70, 40, 255),
           'pozharsky': (60, 70, 130, 255), 'kutuzov2': (40, 105, 70, 255)}.get(who, (80, 80, 80, 255))
    d.ellipse(_P([(2, 2), (98, 98)], k), fill=WHITE)
    d.ellipse(_P([(8, 8), (92, 92)], k), fill=bgc)
    mask = Image.new('L', im.size, 0); ImageDraw.Draw(mask).ellipse(_P([(8, 8), (92, 92)], k), fill=255)
    bust = Image.new('RGBA', im.size, (0, 0, 0, 0)); b = ImageDraw.Draw(bust)
    coat = {'napoleon': (30, 45, 100, 255), 'tsar': (30, 70, 40, 255), 'kutuzov': (30, 70, 40, 255),
            'hitler': (110, 100, 70, 255), 'stalin': (180, 170, 130, 255), 'charles': (30, 50, 110, 255),
            'mongol': (150, 50, 40, 255), 'ivan': (200, 160, 60, 255), 'peter': (30, 70, 45, 255), 'minin': (150, 90, 50, 255),
            'pozharsky': (170, 40, 40, 255)}.get(who, INK)
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
    elif who == 'mongol':
        b.polygon(_P([(30, 36), (50, 4), (70, 36)], k), fill=(160, 40, 40, 255), outline=INK, width=int(2 * k))
        b.rounded_rectangle(_P([(28, 30), (72, 42)], k), radius=int(5 * k), fill=(120, 80, 45, 255), outline=INK, width=int(2 * k))
        b.line(_P([(42, 60), (36, 68)], k), fill=INK, width=int(3 * k)); b.line(_P([(58, 60), (64, 68)], k), fill=INK, width=int(3 * k))
    elif who == 'ivan':
        b.polygon(_P([(38, 56), (62, 56), (58, 82), (50, 90), (42, 82)], k), fill=(110, 70, 40, 255))
        b.pieslice(_P([(32, 8), (68, 46)], k), 180, 360, fill=GOLD, outline=INK, width=int(2 * k))
        b.rounded_rectangle(_P([(30, 26), (70, 36)], k), radius=int(4 * k), fill=(90, 60, 35, 255), outline=INK, width=int(2 * k))
        b.line(_P([(50, 4), (50, 12)], k), fill=GOLD, width=int(3 * k)); b.line(_P([(46, 7), (54, 7)], k), fill=GOLD, width=int(3 * k))
    elif who == 'peter':
        b.pieslice(_P([(29, 22), (71, 52)], k), 180, 360, fill=(50, 35, 25, 255))
        b.rectangle(_P([(29, 36), (35, 62)], k), fill=(50, 35, 25, 255)); b.rectangle(_P([(65, 36), (71, 62)], k), fill=(50, 35, 25, 255))
        b.line(_P([(44, 57), (56, 57)], k), fill=(50, 35, 25, 255), width=int(3 * k))
    elif who in ('minin', 'pozharsky'):
        b.polygon(_P([(36, 56), (64, 56), (60, 78), (50, 84), (40, 78)], k), fill=(120, 80, 45, 255))
        b.pieslice(_P([(32, 14), (68, 46)], k), 180, 360, fill=(170, 40, 40, 255) if who == 'pozharsky' else (110, 80, 50, 255))
        b.rounded_rectangle(_P([(30, 28), (70, 38)], k), radius=int(4 * k), fill=(70, 50, 35, 255))
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


# ---------------------------------------------------------------- more icons (parts 2-10)
def tank(s, col=(110, 112, 100, 255)):
    w, h = int(s * 1.6), s
    im, d = _canvas(w, h); k = SS * s / 100.0; lw = int(4 * k)
    d.rounded_rectangle(_P([(8, 62), (152, 94)], k), radius=int(16 * k), fill=(60, 60, 60, 255), outline=INK, width=lw)
    for x in range(24, 150, 22): d.ellipse(_P([(x - 9, 69), (x + 9, 87)], k), fill=(140, 140, 140, 255), outline=INK, width=int(2 * k))
    d.polygon(_P([(18, 62), (30, 40), (130, 40), (144, 62)], k), fill=col, outline=INK, width=lw)
    d.rounded_rectangle(_P([(50, 18), (110, 44)], k), radius=int(8 * k), fill=col, outline=INK, width=lw)
    d.rectangle(_P([(108, 26), (158, 34)], k), fill=col, outline=INK, width=int(3 * k))
    return _done(im, w, h)

def plane(s, col=(150, 150, 155, 255)):
    w, h = int(s * 1.4), s
    im, d = _canvas(w, h); k = SS * s / 100.0; lw = int(4 * k)
    d.polygon(_P([(8, 50), (120, 42), (136, 50), (120, 58)], k), fill=col, outline=INK, width=lw)
    d.polygon(_P([(60, 46), (84, 4), (96, 4), (88, 46)], k), fill=col, outline=INK, width=lw)
    d.polygon(_P([(60, 54), (84, 96), (96, 96), (88, 54)], k), fill=col, outline=INK, width=lw)
    d.polygon(_P([(10, 50), (4, 28), (16, 28), (26, 48)], k), fill=col, outline=INK, width=lw)
    return _done(im, w, h)

def ship(s, col=(200, 40, 35, 255)):
    """icebreaker: red hull, white superstructure"""
    w, h = int(s * 1.7), s
    im, d = _canvas(w, h); k = SS * s / 100.0; lw = int(4 * k)
    d.polygon(_P([(4, 56), (166, 56), (146, 92), (22, 92)], k), fill=col, outline=INK, width=lw)
    d.rectangle(_P([(40, 30), (120, 56)], k), fill=WHITE, outline=INK, width=lw)
    d.rectangle(_P([(60, 10), (96, 30)], k), fill=WHITE, outline=INK, width=lw)
    for x in (50, 70, 90, 108): d.rectangle(_P([(x, 38), (x + 8, 46)], k), fill=(60, 120, 200, 255))
    d.rectangle(_P([(100, 0), (110, 12)], k), fill=(240, 190, 40, 255), outline=INK, width=int(2 * k))
    return _done(im, w, h)

def rocket(s):
    w, h = int(s * 0.5), s
    im, d = _canvas(w, h); k = SS * s / 100.0; lw = int(3 * k)
    d.polygon(_P([(25, 2), (40, 24), (40, 80), (10, 80), (10, 24)], k), fill=WHITE, outline=INK, width=lw)
    d.polygon(_P([(10, 60), (0, 86), (10, 80)], k), fill=RED, outline=INK, width=lw)
    d.polygon(_P([(40, 60), (50, 86), (40, 80)], k), fill=RED, outline=INK, width=lw)
    d.ellipse(_P([(18, 30), (32, 44)], k), fill=(80, 140, 220, 255), outline=INK, width=lw)
    d.polygon(_P([(14, 82), (36, 82), (25, 100)], k), fill=(250, 170, 40, 255))
    return _done(im, w, h)

def sputnik(s):
    w, h = int(s * 1.5), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    for a, b in (((60, 50), (4, 96)), ((70, 52), (40, 100)), ((86, 52), (110, 100)), ((92, 50), (146, 94))):
        d.line(_P([a, b], k), fill=(200, 200, 205, 255), width=int(4 * k))
    d.ellipse(_P([(44, 14), (106, 76)], k), fill=(215, 218, 225, 255), outline=INK, width=int(4 * k))
    d.ellipse(_P([(56, 24), (74, 40)], k), fill=WHITE)
    return _done(im, w, h)

def station(s):
    w, h = int(s * 1.8), s
    im, d = _canvas(w, h); k = SS * s / 100.0; lw = int(3 * k)
    for x in (8, 128):
        d.rectangle(_P([(x, 10), (x + 44, 90)], k), fill=(50, 80, 160, 255), outline=INK, width=lw)
        for yy in range(26, 90, 16): d.line(_P([(x, yy), (x + 44, yy)], k), fill=(120, 150, 220, 255), width=int(2 * k))
    d.rectangle(_P([(52, 42), (128, 58)], k), fill=(200, 200, 205, 255), outline=INK, width=lw)
    d.ellipse(_P([(72, 30), (108, 70)], k), fill=(225, 225, 230, 255), outline=INK, width=lw)
    return _done(im, w, h)

def astronaut(s):
    im, d = _canvas(s, s); k = SS * s / 100.0; lw = int(4 * k)
    d.ellipse(_P([(14, 8), (86, 80)], k), fill=WHITE, outline=INK, width=lw)
    d.ellipse(_P([(26, 22), (74, 64)], k), fill=(60, 90, 140, 255), outline=INK, width=lw)
    d.ellipse(_P([(34, 28), (46, 40)], k), fill=(160, 190, 230, 255))
    d.rectangle(_P([(30, 80), (70, 98)], k), fill=RED, outline=INK, width=lw)
    d.text((40 * k, 80 * k), 'CCCP', fill=WHITE)
    return _done(im, s, s)

def dog(s):
    w, h = int(s * 1.2), s
    im, d = _canvas(w, h); k = SS * s / 100.0; lw = int(4 * k)
    d.ellipse(_P([(20, 20), (100, 96)], k), fill=(245, 245, 245, 255), outline=INK, width=lw)
    d.polygon(_P([(22, 30), (10, 4), (40, 24)], k), fill=(160, 110, 70, 255), outline=INK, width=lw)
    d.polygon(_P([(98, 30), (110, 4), (80, 24)], k), fill=(160, 110, 70, 255), outline=INK, width=lw)
    d.ellipse(_P([(40, 46), (50, 56)], k), fill=INK); d.ellipse(_P([(70, 46), (80, 56)], k), fill=INK)
    d.ellipse(_P([(54, 62), (66, 72)], k), fill=INK)
    d.arc(_P([(14, 14), (106, 102)], k), 180, 360, fill=(180, 210, 240, 255), width=int(5 * k))
    return _done(im, w, h)

def missile(s):
    w, h = int(s * 0.36), s
    im, d = _canvas(w, h); k = SS * s / 100.0; lw = int(3 * k)
    d.polygon(_P([(18, 0), (30, 20), (30, 84), (6, 84), (6, 20)], k), fill=(225, 225, 225, 255), outline=INK, width=lw)
    d.rectangle(_P([(6, 40), (30, 46)], k), fill=RED)
    d.polygon(_P([(6, 70), (0, 98), (6, 90)], k), fill=(90, 90, 90, 255), outline=INK, width=lw)
    d.polygon(_P([(30, 70), (36, 98), (30, 90)], k), fill=(90, 90, 90, 255), outline=INK, width=lw)
    return _done(im, w, h)

def mushroom(s):
    w, h = int(s * 1.1), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.rectangle(_P([(44, 34), (66, 92)], k), fill=(240, 160, 70, 255))
    d.ellipse(_P([(4, 2), (106, 50)], k), fill=(250, 190, 90, 255), outline=(200, 90, 40, 255), width=int(4 * k))
    d.ellipse(_P([(22, 10), (88, 38)], k), fill=(255, 230, 150, 255))
    d.ellipse(_P([(14, 80), (96, 100)], k), fill=(230, 120, 50, 255))
    return _done(im, w, h)

def gas(s):
    w, h = int(s * 0.8), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.polygon(_P([(40, 2), (72, 50), (66, 84), (40, 98), (14, 84), (8, 50)], k), fill=(60, 120, 240, 255))
    d.polygon(_P([(40, 34), (58, 62), (52, 84), (40, 92), (28, 84), (22, 62)], k), fill=(140, 200, 255, 255))
    return _done(im, w, h)

def oil(s):
    w, h = int(s * 0.7), s
    im, d = _canvas(w, h); k = SS * s / 100.0; lw = int(4 * k)
    d.rounded_rectangle(_P([(6, 8), (64, 96)], k), radius=int(8 * k), fill=(40, 40, 45, 255), outline=INK, width=lw)
    for y in (30, 70): d.line(_P([(6, y), (64, y)], k), fill=(110, 110, 120, 255), width=int(4 * k))
    d.polygon(_P([(35, 38), (46, 56), (35, 64), (24, 56)], k), fill=(250, 200, 50, 255))
    return _done(im, w, h)

def diamond(s):
    im, d = _canvas(s, s); k = SS * s / 100.0; lw = int(3 * k)
    d.polygon(_P([(20, 10), (80, 10), (96, 34), (50, 94), (4, 34)], k), fill=(170, 220, 250, 255), outline=(40, 90, 140, 255), width=lw)
    d.line(_P([(4, 34), (96, 34)], k), fill=(40, 90, 140, 255), width=lw)
    d.line(_P([(36, 10), (30, 34), (50, 94), (70, 34), (64, 10)], k), fill=(40, 90, 140, 255), width=lw)
    return _done(im, s, s)

def goldbar(s):
    w, h = int(s * 1.5), s
    im, d = _canvas(w, h); k = SS * s / 100.0; lw = int(4 * k)
    d.polygon(_P([(10, 90), (30, 40), (120, 40), (140, 90)], k), fill=GOLD, outline=(150, 100, 20, 255), width=lw)
    d.polygon(_P([(30, 40), (40, 20), (110, 20), (120, 40)], k), fill=(255, 225, 120, 255), outline=(150, 100, 20, 255), width=lw)
    return _done(im, w, h)

def rock(s, col=(60, 60, 64, 255)):
    w, h = int(s * 1.3), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.polygon(_P([(10, 90), (4, 50), (30, 14), (80, 8), (122, 40), (126, 88)], k), fill=col, outline=INK, width=int(4 * k))
    d.polygon(_P([(30, 30), (60, 20), (50, 44)], k), fill=(120, 120, 125, 255))
    return _done(im, w, h)

def phone(s):
    w, h = int(s * 0.55), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.rounded_rectangle(_P([(4, 2), (52, 98)], k), radius=int(9 * k), fill=(30, 30, 34, 255), outline=(180, 180, 190, 255), width=int(3 * k))
    d.rounded_rectangle(_P([(9, 10), (47, 86)], k), radius=int(4 * k), fill=(70, 140, 230, 255))
    return _done(im, w, h)

def tree(s):
    w, h = int(s * 0.7), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.rectangle(_P([(30, 76), (40, 98)], k), fill=(120, 80, 40, 255))
    for y0, half in ((2, 16), (22, 24), (44, 32)):
        d.polygon(_P([(35, y0), (35 + half, y0 + 36), (35 - half, y0 + 36)], k), fill=(40, 130, 60, 255), outline=(20, 70, 30, 255), width=int(3 * k))
    return _done(im, w, h)

def drop(s):
    w, h = int(s * 0.75), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.polygon(_P([(37, 2), (66, 56), (60, 82), (37, 98), (14, 82), (8, 56)], k), fill=(60, 160, 240, 255), outline=WHITE, width=int(4 * k))
    d.ellipse(_P([(22, 54), (34, 70)], k), fill=(200, 235, 255, 255))
    return _done(im, w, h)

def train(s):
    w, h = int(s * 1.7), s
    im, d = _canvas(w, h); k = SS * s / 100.0; lw = int(4 * k)
    d.rectangle(_P([(10, 30), (110, 80)], k), fill=(40, 110, 70, 255), outline=INK, width=lw)
    d.rectangle(_P([(110, 14), (160, 80)], k), fill=(200, 40, 35, 255), outline=INK, width=lw)
    for x in (24, 54, 84): d.rectangle(_P([(x, 40), (x + 18, 56)], k), fill=(250, 230, 160, 255))
    for x in (30, 70, 125, 148): d.ellipse(_P([(x - 10, 74), (x + 10, 94)], k), fill=(50, 50, 50, 255), outline=INK, width=int(2 * k))
    return _done(im, w, h)

def moon(s):
    im, d = _canvas(s, s); k = SS * s / 100.0
    d.ellipse(_P([(10, 10), (90, 90)], k), fill=(250, 235, 160, 255))
    d.ellipse(_P([(34, 2), (104, 76)], k), fill=(0, 0, 0, 0))
    return _done(im, s, s)

def clock(s):
    im, d = _canvas(s, s); k = SS * s / 100.0
    d.ellipse(_P([(6, 6), (94, 94)], k), fill=WHITE, outline=INK, width=int(6 * k))
    d.line(_P([(50, 50), (50, 20)], k), fill=INK, width=int(6 * k)); d.line(_P([(50, 50), (72, 60)], k), fill=INK, width=int(6 * k))
    return _done(im, s, s)

def padlock(s):
    w, h = int(s * 0.8), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.arc(_P([(14, 2), (66, 60)], k), 180, 360, fill=(160, 160, 170, 255), width=int(10 * k))
    d.line(_P([(19, 31), (19, 46)], k), fill=(160, 160, 170, 255), width=int(10 * k)); d.line(_P([(61, 31), (61, 46)], k), fill=(160, 160, 170, 255), width=int(10 * k))
    d.rounded_rectangle(_P([(4, 44), (76, 98)], k), radius=int(8 * k), fill=GOLD, outline=INK, width=int(4 * k))
    d.ellipse(_P([(34, 60), (46, 74)], k), fill=INK)
    return _done(im, w, h)

def people(s):
    w, h = int(s * 1.4), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    for x, sc in ((30, 0.8), (70, 1.0), (110, 0.8)):
        r = 14 * sc
        d.ellipse(_P([(x - r, 50 - 40 * sc - r), (x + r, 50 - 40 * sc + r)], k), fill=WHITE, outline=INK, width=int(3 * k))
        d.pieslice(_P([(x - 26 * sc, 52 - 10 * sc), (x + 26 * sc, 100 + 30 * sc)], k), 180, 360, fill=WHITE, outline=INK, width=int(3 * k))
    return _done(im, w, h)

def down(s):
    w, h = int(s * 1.2), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.line(_P([(8, 14), (40, 46), (64, 34), (104, 82)], k), fill=RED, width=int(10 * k))
    d.polygon(_P([(112, 96), (82, 86), (104, 66)], k), fill=RED)
    return _done(im, w, h)

def globe(s):
    im, d = _canvas(s, s); k = SS * s / 100.0
    d.ellipse(_P([(6, 6), (94, 94)], k), fill=(60, 140, 220, 255), outline=WHITE, width=int(5 * k))
    d.ellipse(_P([(30, 6), (70, 94)], k), outline=WHITE, width=int(3 * k))
    d.line(_P([(6, 50), (94, 50)], k), fill=WHITE, width=int(3 * k)); d.line(_P([(50, 6), (50, 94)], k), fill=WHITE, width=int(3 * k))
    return _done(im, s, s)

def stamp(s, text='VETO'):
    from render_text import text_img
    return text_img(text, 'luckiest', s, (230, 50, 40), (255, 255, 255), max(3, s // 12))

def planet(s):
    im, d = _canvas(s, s); k = SS * s / 100.0
    d.ellipse(_P([(4, 4), (96, 96)], k), fill=(215, 190, 160, 255), outline=WHITE, width=int(3 * k))
    d.ellipse(_P([(20, 30), (60, 70)], k), fill=(245, 230, 210, 255))
    d.ellipse(_P([(60, 20), (76, 36)], k), fill=(180, 150, 120, 255))
    return _done(im, s, s)

def truck(s):
    w, h = int(s * 1.6), s
    im, d = _canvas(w, h); k = SS * s / 100.0; lw = int(4 * k)
    d.rectangle(_P([(6, 20), (104, 76)], k), fill=(110, 120, 80, 255), outline=INK, width=lw)
    d.polygon(_P([(104, 40), (140, 40), (156, 60), (156, 76), (104, 76)], k), fill=(90, 100, 70, 255), outline=INK, width=lw)
    d.rectangle(_P([(114, 46), (138, 60)], k), fill=(170, 210, 240, 255))
    for x in (30, 80, 134): d.ellipse(_P([(x - 12, 68), (x + 12, 92)], k), fill=(40, 40, 40, 255), outline=INK, width=int(2 * k))
    return _done(im, w, h)

def sledge(s):
    w, h = int(s * 1.5), s
    im, d = _canvas(w, h); k = SS * s / 100.0; lw = int(4 * k)
    d.rounded_rectangle(_P([(20, 20), (110, 70)], k), radius=int(10 * k), fill=(40, 50, 100, 255), outline=INK, width=lw)
    d.line(_P([(4, 84), (130, 84), (146, 70)], k), fill=(90, 60, 40, 255), width=int(7 * k))
    d.line(_P([(40, 70), (40, 84)], k), fill=(90, 60, 40, 255), width=int(5 * k)); d.line(_P([(96, 70), (96, 84)], k), fill=(90, 60, 40, 255), width=int(5 * k))
    d.rectangle(_P([(40, 30), (64, 50)], k), fill=(170, 210, 240, 255))
    return _done(im, w, h)

def mountain(s):
    w, h = int(s * 1.5), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.polygon(_P([(2, 96), (50, 16), (78, 56), (100, 30), (148, 96)], k), fill=(120, 110, 100, 255), outline=INK, width=int(4 * k))
    d.polygon(_P([(38, 36), (50, 16), (62, 36), (55, 32), (50, 40), (44, 32)], k), fill=WHITE)
    return _done(im, w, h)

def horseman(s):
    """Mongol rider: simple horse silhouette + rider"""
    w, h = int(s * 1.3), s
    im, d = _canvas(w, h); k = SS * s / 100.0; lw = int(3 * k)
    hc = (130, 85, 50, 255)
    d.ellipse(_P([(20, 44), (100, 76)], k), fill=hc, outline=INK, width=lw)
    d.polygon(_P([(90, 52), (118, 24), (128, 34), (104, 66)], k), fill=hc, outline=INK, width=lw)
    for x in (30, 46, 78, 92): d.line(_P([(x, 70), (x - 4 + (x % 3) * 4, 98)], k), fill=INK, width=int(5 * k))
    d.line(_P([(22, 54), (6, 74)], k), fill=INK, width=int(5 * k))
    d.rectangle(_P([(52, 20), (70, 50)], k), fill=(160, 40, 40, 255), outline=INK, width=lw)
    d.ellipse(_P([(52, 4), (70, 22)], k), fill=SKIN, outline=INK, width=lw)
    d.polygon(_P([(48, 8), (61, -4), (74, 8)], k), fill=(110, 70, 40, 255))
    d.arc(_P([(68, 10), (92, 50)], k), 270, 90, fill=INK, width=int(3 * k))
    return _done(im, w, h)

def calendar(s, text='JUNE'):
    from render_text import font
    w, h = int(s * 0.95), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    d.rounded_rectangle(_P([(4, 10), (91, 98)], k), radius=int(8 * k), fill=WHITE, outline=INK, width=int(4 * k))
    d.rectangle(_P([(4, 10), (91, 36)], k), fill=RED)
    for x in (24, 70): d.rectangle(_P([(x - 3, 2), (x + 3, 18)], k), fill=INK)
    return _done(im, w, h)

_MORE = {'tank': tank, 'tank-ru': lambda s: tank(s, (80, 110, 60, 255)), 'plane': plane, 'ship': ship, 'rocket': rocket,
         'sputnik': sputnik, 'station': station, 'astronaut': astronaut, 'dog': dog, 'missile': missile,
         'mushroom': mushroom, 'gas': gas, 'oil': oil, 'diamond': diamond, 'gold': goldbar, 'coal': rock,
         'nickel': lambda s: rock(s, (150, 150, 140, 255)), 'phone': phone, 'tree': tree, 'drop': drop, 'train': train,
         'moon': moon, 'clock': clock, 'padlock': padlock, 'people': people, 'down': down, 'globe': globe,
         'veto': stamp, 'planet': planet, 'truck': truck, 'sledge': sledge, 'mountain': mountain, 'horseman': horseman,
         'calendar': calendar}
_get_base = get.__wrapped__

@lru_cache(maxsize=512)
def get(kind, s):
    if kind in _MORE: return _MORE[kind](int(s))
    return _get_base(kind, s)


# ---------------------------------------------------------------- Israel video flags
def _flag_base(s):
    w, h = int(s * 1.45), s
    im, d = _canvas(w, h)
    return im, d, w, h, w * SS, h * SS

def _flag_done(im, d, w, h, W, H, s):
    d.rectangle([0, 0, W - 1, H - 1], outline=WHITE, width=int(SS * max(2, s / 14)))
    return _done(im, w, h)

def _star(d, cx, cy, r, col, n=5, inner=0.42, rot=-90):
    pts = []
    for i in range(2 * n):
        a = math.radians(rot + i * 180 / n); rr = r if i % 2 == 0 else r * inner
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col)

def flag_il(s):
    im, d, w, h, W, H = _flag_base(s); B = (0, 56, 184, 255)
    d.rectangle([0, 0, W, H], fill=WHITE)
    d.rectangle([0, H * 0.1, W, H * 0.25], fill=B); d.rectangle([0, H * 0.75, W, H * 0.9], fill=B)
    cx, cy, r = W / 2, H / 2, H * 0.2; lw = max(2, int(H * 0.035))
    for rot in (-90, 90):
        pts = [(cx + r * math.cos(math.radians(rot + 120 * i)), cy + r * math.sin(math.radians(rot + 120 * i))) for i in range(3)]
        d.line(pts + [pts[0]], fill=B, width=lw, joint='curve')
    return _flag_done(im, d, w, h, W, H, s)

def flag_tri(s, stripes, tri, star=None):
    im, d, w, h, W, H = _flag_base(s)
    for i, c in enumerate(stripes): d.rectangle([0, H * i / 3, W, H * (i + 1) / 3], fill=c)
    d.polygon([(0, 0), (W * 0.42, H / 2), (0, H)], fill=tri)
    if star: _star(d, W * 0.14, H / 2, H * 0.09, star, n=7, inner=0.5)
    return _flag_done(im, d, w, h, W, H, s)

def flag_stripes3(s, stripes, stars=None):
    im, d, w, h, W, H = _flag_base(s)
    for i, c in enumerate(stripes): d.rectangle([0, H * i / 3, W, H * (i + 1) / 3], fill=c)
    if stars == 'eg':
        d.ellipse([W / 2 - H * 0.08, H / 2 - H * 0.1, W / 2 + H * 0.08, H / 2 + H * 0.1], fill=(192, 147, 0, 255))
    elif stars:
        for x in (0.36, 0.64): _star(d, W * x, H / 2, H * 0.11, stars)
    return _flag_done(im, d, w, h, W, H, s)

def flag_gb(s):
    im, d, w, h, W, H = _flag_base(s); B = (1, 33, 105, 255); R = (200, 16, 46, 255)
    d.rectangle([0, 0, W, H], fill=B)
    d.line([(0, 0), (W, H)], fill=WHITE, width=int(H * 0.2)); d.line([(0, H), (W, 0)], fill=WHITE, width=int(H * 0.2))
    d.line([(0, 0), (W, H)], fill=R, width=int(H * 0.07)); d.line([(0, H), (W, 0)], fill=R, width=int(H * 0.07))
    d.rectangle([W / 2 - H * 0.17, 0, W / 2 + H * 0.17, H], fill=WHITE); d.rectangle([0, H / 2 - H * 0.17, W, H / 2 + H * 0.17], fill=WHITE)
    d.rectangle([W / 2 - H * 0.1, 0, W / 2 + H * 0.1, H], fill=R); d.rectangle([0, H / 2 - H * 0.1, W, H / 2 + H * 0.1], fill=R)
    return _flag_done(im, d, w, h, W, H, s)

def flag_lb(s):
    im, d, w, h, W, H = _flag_base(s); R = (237, 28, 36, 255); G = (0, 166, 81, 255)
    d.rectangle([0, 0, W, H], fill=R); d.rectangle([0, H * 0.25, W, H * 0.75], fill=WHITE)
    d.polygon([(W / 2, H * 0.3), (W / 2 - H * 0.2, H * 0.66), (W / 2 + H * 0.2, H * 0.66)], fill=G)
    return _flag_done(im, d, w, h, W, H, s)

def flag_un(s):
    im, d, w, h, W, H = _flag_base(s); B = (0, 158, 219, 255)
    d.rectangle([0, 0, W, H], fill=B)
    cx, cy, r = W / 2, H / 2, H * 0.27; lw = max(2, int(H * 0.025))
    for k in (1.0, 0.66, 0.33): d.ellipse([cx - r * k, cy - r * k, cx + r * k, cy + r * k], outline=WHITE, width=lw)
    d.line([(cx - r, cy), (cx + r, cy)], fill=WHITE, width=lw); d.line([(cx, cy - r), (cx, cy + r)], fill=WHITE, width=lw)
    for side in (-1, 1): d.arc([cx - r * 1.4, cy - r * 1.35, cx + r * 1.4, cy + r * 1.35], 100 if side > 0 else -80, 170 if side > 0 else 10, fill=WHITE, width=lw * 2)
    return _flag_done(im, d, w, h, W, H, s)

def flag_ottoman(s):
    im, d, w, h, W, H = _flag_base(s); R = (227, 10, 23, 255)
    d.rectangle([0, 0, W, H], fill=R)
    r = H * 0.25; cx, cy = W * 0.44, H / 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE); d.ellipse([cx - r * 0.55, cy - r * 0.8, cx + r * 1.05, cy + r * 0.8], fill=R)
    _star(d, W * 0.62, H / 2, H * 0.12, WHITE)
    return _flag_done(im, d, w, h, W, H, s)

_BLK = (20, 20, 20, 255); _GRN = (0, 122, 61, 255); _RD = (206, 17, 38, 255)
_FL2 = {'il': flag_il, 'gb': flag_gb, 'lb': flag_lb, 'un': flag_un, 'ottoman': flag_ottoman,
        'ps': lambda s: flag_tri(s, (_BLK, WHITE, _GRN), _RD),
        'jo': lambda s: flag_tri(s, (_BLK, WHITE, _GRN), _RD, star=WHITE),
        'eg': lambda s: flag_stripes3(s, (_RD, WHITE, _BLK), 'eg'),
        'sy': lambda s: flag_stripes3(s, (_RD, WHITE, _BLK), (0, 122, 61, 255)),
        'iq': lambda s: flag_stripes3(s, (_RD, WHITE, _BLK)),
        'ae': lambda s: flag_tri(s, (_GRN, WHITE, _BLK), _RD),
        }

def dove(s):
    w, h = int(s * 1.3), s
    im, d = _canvas(w, h); k = SS * s / 100.0; lw = int(3 * k)
    d.ellipse(_P([(30, 40), (95, 75)], k), fill=WHITE, outline=INK, width=lw)
    d.ellipse(_P([(85, 30), (112, 55)], k), fill=WHITE, outline=INK, width=lw)
    d.polygon(_P([(110, 40), (125, 44), (110, 48)], k), fill=GOLD, outline=INK)
    d.ellipse(_P([(98, 37), (103, 42)], k), fill=INK)
    d.polygon(_P([(45, 50), (70, 5), (85, 45)], k), fill=(235, 238, 245, 255), outline=INK, width=lw)
    d.polygon(_P([(32, 55), (5, 45), (12, 62), (5, 75), (35, 66)], k), fill=WHITE, outline=INK, width=lw)
    d.line(_P([(118, 46), (128, 62)], k), fill=(60, 140, 60, 255), width=int(3 * k))
    for y in (52, 58): d.ellipse(_P([(120, y - 3), (128, y + 3)], k), fill=(80, 170, 70, 255))
    return _done(im, w, h)

def handshake(s):
    w, h = int(s * 1.5), s
    im, d = _canvas(w, h); k = SS * s / 100.0; lw = int(3 * k)
    d.rectangle(_P([(0, 38), (40, 66)], k), fill=(45, 50, 65, 255), outline=INK, width=lw)
    d.rectangle(_P([(110, 38), (150, 66)], k), fill=(110, 112, 120, 255), outline=INK, width=lw)
    d.rounded_rectangle(_P([(36, 34), (90, 66)], k), radius=int(14 * k), fill=SKIN, outline=INK, width=lw)
    d.rounded_rectangle(_P([(62, 40), (114, 72)], k), radius=int(14 * k), fill=(222, 178, 138, 255), outline=INK, width=lw)
    for x in (70, 80, 90): d.line(_P([(x, 44), (x, 64)], k), fill=INK, width=int(1.5 * k))
    return _done(im, w, h)

def star_david(s, col=(0, 56, 184, 255)):
    im, d = _canvas(s, s); W = s * SS; cx = cy = W / 2; r = W * 0.42; lw = int(W * 0.06)
    for rot in (-90, 90):
        pts = [(cx + r * math.cos(math.radians(rot + 120 * i)), cy + r * math.sin(math.radians(rot + 120 * i))) for i in range(3)]
        d.line(pts + [pts[0]], fill=col, width=lw, joint='curve')
    return _done(im, s, s)

def crescent(s, col=(0, 122, 61, 255)):
    im, d = _canvas(s, s); W = s * SS
    d.ellipse([W * 0.08, W * 0.08, W * 0.92, W * 0.92], fill=col); d.ellipse([W * 0.3, W * 0.12, W * 1.0, W * 0.88], fill=(0, 0, 0, 0))
    return _done(im, s, s)

def cross_ic(s, col=(160, 40, 40, 255)):
    im, d = _canvas(s, s); W = s * SS
    d.rectangle([W * 0.42, W * 0.08, W * 0.58, W * 0.92], fill=col); d.rectangle([W * 0.2, W * 0.3, W * 0.8, W * 0.44], fill=col)
    return _done(im, s, s)

def menorah(s):
    w, h = int(s * 1.1), s
    im, d = _canvas(w, h); k = SS * s / 100.0; G = (232, 186, 60, 255); lw = int(5 * k)
    cx = 55
    for i, r in enumerate((0, 12, 24, 36)):
        if r == 0: d.line(_P([(cx, 20), (cx, 85)], k), fill=G, width=lw)
        else:
            d.arc(_P([(cx - r, 20 - r + 30), (cx + r, 20 + r + 30)], k), 0, 180, fill=G, width=lw)
            d.line(_P([(cx - r, 50), (cx - r, 20)], k), fill=G, width=lw); d.line(_P([(cx + r, 50), (cx + r, 20)], k), fill=G, width=lw)
    for x in (cx - 36, cx - 24, cx - 12, cx, cx + 12, cx + 24, cx + 36):
        d.ellipse(_P([(x - 3, 8), (x + 3, 18)], k), fill=(255, 140, 40, 255))
    d.polygon(_P([(cx - 20, 98), (cx + 20, 98), (cx + 8, 85), (cx - 8, 85)], k), fill=G)
    return _done(im, w, h)

def scroll(s, text=''):
    w, h = int(s * 0.8), s
    im, d = _canvas(w, h); k = SS * s / 100.0; lw = int(2.5 * k)
    d.rectangle(_P([(10, 10), (70, 92)], k), fill=(246, 236, 210, 255), outline=INK, width=lw)
    for y in range(24, 84, 9): d.line(_P([(18, y), (62, y)], k), fill=(150, 130, 110, 255), width=int(2 * k))
    d.ellipse(_P([(4, 4), (76, 16)], k), fill=(225, 210, 175, 255), outline=INK, width=lw)
    d.ellipse(_P([(4, 86), (76, 98)], k), fill=(225, 210, 175, 255), outline=INK, width=lw)
    return _done(im, w, h)

def wallbar(s):
    """grey concrete separation barrier segment"""
    w, h = int(s * 1.8), s
    im, d = _canvas(w, h); k = SS * s / 100.0
    for i in range(5):
        x = 4 + i * 34
        d.rectangle(_P([(x, 6), (x + 32, 96)], k), fill=(170, 170, 168, 255), outline=(110, 110, 108, 255), width=int(2 * k))
    return _done(im, w, h)

def tent_ic(s):
    w, h = int(s * 1.3), s
    im, d = _canvas(w, h); k = SS * s / 100.0; lw = int(3 * k)
    d.polygon(_P([(5, 92), (65, 10), (125, 92)], k), fill=(232, 226, 210, 255), outline=INK, width=lw)
    d.polygon(_P([(52, 92), (65, 50), (78, 92)], k), fill=(120, 100, 80, 255))
    return _done(im, w, h)

_MORE.update({'dove': dove, 'handshake': handshake, 'star': star_david, 'crescent': crescent, 'cross': cross_ic, 'menorah': menorah,
              'scroll': scroll, 'wall': wallbar, 'tent': tent_ic, **{'flag-' + k: v for k, v in _FL2.items()}})
