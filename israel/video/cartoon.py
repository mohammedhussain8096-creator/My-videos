"""Flat cartoon figures and props in the reference video's style (round heads, dot eyes, thin dark limbs,
simple costumes; flat buildings, walls, ships). Everything is drawn in code. get(kind, h) returns RGBA."""
import math
from functools import lru_cache
from PIL import Image, ImageDraw

SS = 3
INK = (52, 36, 26, 255)
SKIN = (246, 214, 182, 255); TAN = (222, 178, 138, 255)
WHITE = (250, 248, 240, 255); GOLD = (240, 192, 56, 255); RED = (205, 52, 44, 255)
STONE = (222, 204, 168, 255); STONE_D = (186, 164, 126, 255)

def _cv(w, h):
    im = Image.new('RGBA', (int(w * SS), int(h * SS)), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)

def _out(im, w, h):
    return im.resize((max(1, int(w)), max(1, int(h))), Image.LANCZOS)

def P(pts, k): return [(x * k, y * k) for x, y in pts]

# ------------------------------------------------------------------ figures
FIG = {   # name: (robe, skin, hat, beard, extra)
    'colonist': ((70, 110, 170, 255), SKIN, 'none', None, 'staff'),
    'byzas': ((60, 95, 165, 255), SKIN, 'greek', (90, 60, 40, 255), 'spear'),
    'sailor': ((230, 225, 205, 255), TAN, 'cap', None, None),
    'oracle': ((240, 236, 225, 255), SKIN, 'veil', None, 'smoke'),
    'emperor': ((128, 40, 120, 255), SKIN, 'crown', (110, 80, 50, 255), 'cape'),
    'constantine': ((128, 40, 120, 255), SKIN, 'crown', None, 'cape'),
    'pope': ((245, 242, 235, 255), SKIN, 'tiara', None, 'cross'),
    'sultan': ((200, 45, 40, 255), TAN, 'turban', (40, 30, 25, 255), 'sword'),
    'mehmed': ((200, 45, 40, 255), TAN, 'turban', (60, 40, 25, 255), 'sword'),
    'king': ((40, 80, 160, 255), SKIN, 'crown', (150, 100, 50, 255), 'sword'),
    'barbarian': ((140, 100, 60, 255), SKIN, 'fur', (170, 110, 50, 255), 'axe'),
    'hun': ((150, 70, 40, 255), TAN, 'fur', (40, 30, 25, 255), 'bow'),
    'soldier': ((150, 40, 40, 255), SKIN, 'helmet', None, 'shield'),
    'byz_soldier': ((150, 40, 40, 255), SKIN, 'helmet', None, 'shield'),
    'janissary': ((60, 100, 170, 255), TAN, 'bork', (40, 30, 25, 255), 'musket'),
    'arab': ((235, 230, 215, 255), TAN, 'keffiyeh', (40, 30, 25, 255), 'sword'),
    'crusader': ((235, 235, 235, 255), SKIN, 'greathelm', None, 'crossshield'),
    'persian': ((120, 60, 150, 255), TAN, 'tall', (30, 25, 20, 255), 'spear'),
    'engineer': ((120, 90, 60, 255), SKIN, 'cap', (120, 80, 50, 255), 'hammer'),
    'merchant': ((60, 140, 110, 255), TAN, 'turban', None, 'bag'),
    'monk': ((70, 55, 45, 255), SKIN, 'none', (120, 110, 100, 255), 'cross'),
    'priest': ((30, 30, 34, 255), SKIN, 'kamilavka', (200, 200, 200, 255), 'cross'),
    'genoese': ((190, 190, 196, 255), SKIN, 'helmet', (120, 80, 50, 255), 'sword'),
    'villager': ((200, 150, 90, 255), TAN, 'none', None, None),
    # Israel video
    'israelite': ((150, 110, 70, 255), TAN, 'none', (60, 40, 25, 255), 'staff'),
    'david': ((120, 50, 140, 255), TAN, 'crown', (90, 55, 30, 255), 'sword'),
    'babylonian': ((40, 80, 140, 255), TAN, 'tall', (30, 25, 20, 255), 'spear'),
    'roman': ((180, 40, 40, 255), SKIN, 'helmet', None, 'shield'),
    'greek': ((60, 95, 165, 255), SKIN, 'greek', None, 'spear'),
    'british': ((176, 156, 108, 255), SKIN, 'khaki', None, None),
    'tommy': ((150, 135, 90, 255), SKIN, 'brodie', None, 'musket'),
    'pioneer': ((90, 140, 200, 255), SKIN, 'tembel', None, 'hammer'),
    'jew': ((40, 42, 52, 255), SKIN, 'kippah', (60, 40, 25, 255), None),
    'herzl': ((30, 30, 34, 255), SKIN, 'none', (35, 28, 24, 255), None),
    'farmer': ((200, 170, 120, 255), TAN, 'keffiyeh', None, 'staff'),
    'palestinian': ((110, 120, 80, 255), TAN, 'keffiyeh', (40, 30, 25, 255), None),
    'mother': ((120, 90, 140, 255), TAN, 'veil', None, 'bag'),
    'refugee': ((150, 120, 90, 255), TAN, 'keffiyeh', (60, 50, 40, 255), 'bag'),
    'idf': ((95, 110, 70, 255), SKIN, 'olive', None, 'musket'),
    'arabsoldier': ((165, 140, 95, 255), TAN, 'olive', None, 'musket'),
    'suit': ((45, 50, 65, 255), SKIN, 'none', None, 'tie'),
    'suit_grey': ((110, 112, 120, 255), SKIN, 'none', None, 'tie'),
    'suit_tan': ((60, 55, 50, 255), TAN, 'none', None, 'tie'),
    'arafat': ((95, 105, 75, 255), TAN, 'keffiyeh', (70, 60, 50, 255), None),
    'protester': ((230, 230, 230, 255), TAN, 'keffiyeh', None, None),
    'fighter': ((60, 60, 62, 255), TAN, 'olive', None, 'musket'),
    'diplomat': ((40, 60, 110, 255), SKIN, 'none', None, 'tie'),
    'egyptian': ((240, 236, 225, 255), TAN, 'nemes', None, 'staff'),
    'assyrian': ((150, 60, 40, 255), TAN, 'tall', (30, 25, 20, 255), 'spear'),
    'mamluk': ((210, 120, 40, 255), TAN, 'turban', (40, 30, 25, 255), 'sword'),
}

def figure(kind, h=360, point=False):
    robe, skin, hat, beard, extra = FIG[kind]
    w = h * 0.62
    im, d = _cv(w, h); k = SS * h / 100.0
    lw = int(1.6 * k)
    cx = 31
    # legs
    d.line(P([(cx - 4, 70), (cx - 6, 97)], k), fill=INK, width=lw); d.line(P([(cx + 4, 70), (cx + 6, 97)], k), fill=INK, width=lw)
    d.ellipse(P([(cx - 10, 95), (cx - 3, 99)], k), fill=INK); d.ellipse(P([(cx + 3, 95), (cx + 10, 99)], k), fill=INK)
    if extra == 'cape':
        d.polygon(P([(cx - 9, 40), (cx + 9, 40), (cx + 15, 86), (cx - 15, 86)], k), fill=(190, 40, 40, 255), outline=INK)
    # robe
    d.polygon(P([(cx - 8, 39), (cx + 8, 39), (cx + 12, 78), (cx - 12, 78)], k), fill=robe, outline=INK, width=int(0.8 * k))
    d.line(P([(cx - 9, 54), (cx + 9, 54)], k), fill=tuple(max(0, c - 50) for c in robe[:3]) + (255,), width=int(1.2 * k))
    # arms
    d.line(P([(cx - 8, 42), (cx - 15, 58), (cx - 13, 66)], k), fill=INK, width=lw, joint='curve')
    if point:
        d.line(P([(cx + 8, 42), (cx + 26, 36)], k), fill=INK, width=lw)
    else:
        d.line(P([(cx + 8, 42), (cx + 16, 56), (cx + 20, 50)], k), fill=INK, width=lw, joint='curve')
    hx = cx + (26 if point else 20); hy = 36 if point else 50
    # held items
    if extra in ('spear', 'staff'):
        d.line(P([(cx - 14, 20 if extra == 'spear' else 28), (cx - 13, 96)], k), fill=(120, 85, 50, 255), width=int(1.4 * k))
        if extra == 'spear': d.polygon(P([(cx - 14, 12), (cx - 11.5, 21), (cx - 16.5, 21)], k), fill=(170, 170, 175, 255), outline=INK)
    if extra == 'sword':
        d.line(P([(hx, hy), (hx + 6, hy - 16)], k), fill=(200, 200, 205, 255), width=int(1.6 * k)); d.line(P([(hx - 3, hy - 2), (hx + 3, hy + 1)], k), fill=GOLD, width=int(1.4 * k))
    if extra == 'axe':
        d.line(P([(hx, hy), (hx + 2, hy - 18)], k), fill=(120, 85, 50, 255), width=int(1.4 * k)); d.pieslice(P([(hx - 4, hy - 22), (hx + 8, hy - 12)], k), 270, 90, fill=(170, 170, 175, 255), outline=INK)
    if extra == 'bow':
        d.arc(P([(hx - 4, hy - 16), (hx + 6, hy + 4)], k), 270, 90, fill=(120, 85, 50, 255), width=int(1.4 * k))
    if extra in ('shield', 'crossshield'):
        d.ellipse(P([(cx + 4, 48), (cx + 22, 68)], k), fill=(200, 160, 50, 255) if extra == 'shield' else WHITE, outline=INK, width=int(0.9 * k))
        if extra == 'crossshield':
            d.line(P([(cx + 13, 51), (cx + 13, 65)], k), fill=RED, width=int(2 * k)); d.line(P([(cx + 7, 57), (cx + 19, 57)], k), fill=RED, width=int(2 * k))
        else:
            d.ellipse(P([(cx + 11, 56), (cx + 15, 60)], k), fill=(150, 110, 30, 255))
    if extra == 'cross':
        d.line(P([(hx + 1, hy - 14), (hx + 1, hy + 2)], k), fill=GOLD, width=int(1.4 * k)); d.line(P([(hx - 3, hy - 10), (hx + 5, hy - 10)], k), fill=GOLD, width=int(1.4 * k))
    if extra == 'musket':
        d.line(P([(cx - 14, 30), (cx - 13, 80)], k), fill=(110, 80, 50, 255), width=int(1.6 * k))
    if extra == 'hammer':
        d.line(P([(hx, hy), (hx + 2, hy - 12)], k), fill=(120, 85, 50, 255), width=int(1.4 * k)); d.rectangle(P([(hx - 3, hy - 16), (hx + 7, hy - 11)], k), fill=(120, 120, 125, 255))
    if extra == 'tie':
        d.polygon(P([(cx - 1.4, 40), (cx + 1.4, 40), (cx + 2, 52), (cx, 55), (cx - 2, 52)], k), fill=(190, 40, 40, 255))
        d.polygon(P([(cx - 5, 39), (cx, 44), (cx + 5, 39)], k), fill=WHITE)
    if extra == 'bag':
        d.ellipse(P([(hx - 5, hy - 2), (hx + 5, hy + 8)], k), fill=(190, 150, 80, 255), outline=INK)
    if extra == 'smoke':
        for i, (sx, sy, r) in enumerate(((cx - 20, 30, 4), (cx - 23, 22, 5), (cx - 19, 13, 6))):
            d.ellipse(P([(sx - r, sy - r), (sx + r, sy + r)], k), fill=(225, 225, 230, 150))
    # neck + head
    d.line(P([(cx, 34), (cx, 40)], k), fill=INK, width=lw)
    d.ellipse(P([(cx - 11, 12), (cx + 11, 35)], k), fill=skin, outline=INK, width=int(0.9 * k))
    if beard:
        d.chord(P([(cx - 10, 18), (cx + 10, 38)], k), 10, 170, fill=beard)
    d.ellipse(P([(cx - 5.5, 21), (cx - 2.5, 24.5)], k), fill=INK); d.ellipse(P([(cx + 2.5, 21), (cx + 5.5, 24.5)], k), fill=INK)
    if not beard: d.arc(P([(cx - 4, 24), (cx + 4, 30)], k), 20, 160, fill=INK, width=int(0.8 * k))
    d.ellipse(P([(cx - 9, 25), (cx - 6, 27.5)], k), fill=(240, 150, 150, 200)); d.ellipse(P([(cx + 6, 25), (cx + 9, 27.5)], k), fill=(240, 150, 150, 200))
    # hats
    if hat == 'greek':
        d.chord(P([(cx - 12, 8), (cx + 12, 26)], k), 180, 360, fill=(200, 150, 50, 255), outline=INK)
        d.pieslice(P([(cx - 8, 0), (cx + 8, 14)], k), 180, 360, fill=RED)
    elif hat == 'crown':
        d.polygon(P([(cx - 9, 15), (cx - 9, 6), (cx - 5, 11), (cx, 4), (cx + 5, 11), (cx + 9, 6), (cx + 9, 15)], k), fill=GOLD, outline=INK)
    elif hat == 'tiara':
        d.polygon(P([(cx - 7, 15), (cx - 5, 0), (cx, -4), (cx + 5, 0), (cx + 7, 15)], k), fill=WHITE, outline=INK)
        for y in (4, 9): d.line(P([(cx - 6, y), (cx + 6, y)], k), fill=GOLD, width=int(1.2 * k))
    elif hat == 'turban':
        d.ellipse(P([(cx - 13, 2), (cx + 13, 18)], k), fill=WHITE, outline=INK)
        d.ellipse(P([(cx - 3, 0), (cx + 3, 6)], k), fill=RED)
    elif hat == 'bork':
        d.polygon(P([(cx - 9, 15), (cx - 7, -6), (cx + 12, -12), (cx + 9, 15)], k), fill=WHITE, outline=INK)
        d.rectangle(P([(cx - 10, 12), (cx + 10, 16)], k), fill=GOLD)
    elif hat == 'fur':
        d.chord(P([(cx - 13, 5), (cx + 13, 24)], k), 180, 360, fill=(120, 80, 45, 255), outline=INK)
    elif hat == 'helmet':
        d.chord(P([(cx - 12, 7), (cx + 12, 27)], k), 180, 360, fill=(175, 175, 182, 255), outline=INK)
        d.line(P([(cx, 4), (cx, 9)], k), fill=RED, width=int(2.4 * k))
    elif hat == 'greathelm':
        d.rounded_rectangle(P([(cx - 11, 10), (cx + 11, 34)], k), radius=int(4 * k), fill=(175, 175, 182, 255), outline=INK)
        d.line(P([(cx - 8, 21), (cx + 8, 21)], k), fill=INK, width=int(1.4 * k)); d.line(P([(cx, 21), (cx, 32)], k), fill=INK, width=int(1 * k))
    elif hat == 'veil':
        d.chord(P([(cx - 14, 8), (cx + 14, 50)], k), 160, 380, fill=(235, 235, 240, 230), outline=INK)
        d.ellipse(P([(cx - 11, 12), (cx + 11, 35)], k), fill=skin, outline=INK, width=int(0.9 * k))
        d.ellipse(P([(cx - 5.5, 21), (cx - 2.5, 24.5)], k), fill=INK); d.ellipse(P([(cx + 2.5, 21), (cx + 5.5, 24.5)], k), fill=INK)
        d.arc(P([(cx - 4, 24), (cx + 4, 30)], k), 20, 160, fill=INK, width=int(0.8 * k))
        d.chord(P([(cx - 12, 9), (cx + 12, 30)], k), 180, 360, fill=(235, 235, 240, 255), outline=INK)
    elif hat == 'cap':
        d.chord(P([(cx - 11, 9), (cx + 11, 22)], k), 180, 360, fill=(150, 60, 50, 255), outline=INK)
    elif hat == 'keffiyeh':
        d.chord(P([(cx - 13, 8), (cx + 13, 40)], k), 180, 360, fill=WHITE, outline=INK)
        d.rectangle(P([(cx - 11, 14), (cx + 11, 17)], k), fill=INK)
    elif hat == 'tall':
        d.rectangle(P([(cx - 8, -6), (cx + 8, 15)], k), fill=(60, 80, 170, 255), outline=INK)
    elif hat == 'nemes':
        d.polygon(P([(cx - 12, 30), (cx - 12, 12), (cx - 6, 5), (cx + 6, 5), (cx + 12, 12), (cx + 12, 30), (cx + 15, 40), (cx + 9, 40), (cx + 8, 22), (cx - 8, 22), (cx - 9, 40), (cx - 15, 40)], k), fill=(240, 192, 56, 255), outline=INK)
        for y in (10, 15, 26, 33): d.line(P([(cx - 13, y), (cx + 13, y)], k), fill=(40, 70, 160, 255), width=int(1.3 * k))
        d.ellipse(P([(cx - 11, 14), (cx + 11, 35)], k), fill=skin, outline=INK, width=int(0.9 * k))
        d.ellipse(P([(cx - 5.5, 21), (cx - 2.5, 24.5)], k), fill=INK); d.ellipse(P([(cx + 2.5, 21), (cx + 5.5, 24.5)], k), fill=INK)
        d.arc(P([(cx - 4, 24), (cx + 4, 30)], k), 20, 160, fill=INK, width=int(0.8 * k))
    elif hat == 'kippah':
        d.chord(P([(cx - 6, 9), (cx + 6, 17)], k), 180, 360, fill=(40, 60, 120, 255), outline=INK)
    elif hat == 'khaki':
        d.chord(P([(cx - 11, 7), (cx + 11, 21)], k), 180, 360, fill=(150, 130, 85, 255), outline=INK)
        d.polygon(P([(cx - 2, 14), (cx + 15, 14), (cx + 12, 17), (cx - 2, 17)], k), fill=(60, 45, 30, 255))
        d.rectangle(P([(cx - 11, 13), (cx + 11, 15.5)], k), fill=(160, 40, 40, 255))
    elif hat == 'brodie':
        d.chord(P([(cx - 10, 6), (cx + 10, 22)], k), 180, 360, fill=(120, 115, 80, 255), outline=INK)
        d.ellipse(P([(cx - 16, 12), (cx + 16, 17)], k), fill=(120, 115, 80, 255), outline=INK)
    elif hat == 'tembel':
        d.polygon(P([(cx - 9, 15), (cx - 7, 4), (cx, 1), (cx + 7, 4), (cx + 9, 15)], k), fill=(110, 140, 190, 255), outline=INK)
        d.ellipse(P([(cx - 13, 12), (cx + 13, 17)], k), fill=(110, 140, 190, 255), outline=INK)
    elif hat == 'olive':
        d.chord(P([(cx - 12, 6), (cx + 12, 27)], k), 180, 360, fill=(90, 100, 64, 255), outline=INK)
        d.line(P([(cx - 12, 16.5), (cx + 12, 16.5)], k), fill=(70, 80, 50, 255), width=int(1.2 * k))
    elif hat == 'kamilavka':
        d.rectangle(P([(cx - 9, 4), (cx + 9, 15)], k), fill=(25, 25, 28, 255), outline=INK)
    return _out(im, w, h)

# ------------------------------------------------------------------ props
def house(h=120, wide=1.0, col=(232, 206, 160, 255)):
    w = h * 1.1 * wide
    im, d = _cv(w, h); k = SS * h / 100.0
    W_ = 110 * wide
    d.rectangle(P([(4, 30), (W_ - 4, 98)], k), fill=col, outline=INK, width=int(1.2 * k))
    d.rectangle(P([(0, 24), (W_, 32)], k), fill=tuple(max(0, c - 30) for c in col[:3]) + (255,), outline=INK, width=int(1.2 * k))
    for x in range(14, int(W_) - 20, 26):
        d.rectangle(P([(x, 46), (x + 12, 60)], k), fill=(90, 60, 45, 255))
    d.rectangle(P([(W_ / 2 - 8, 72), (W_ / 2 + 8, 98)], k), fill=(110, 70, 45, 255))
    return _out(im, w, h)

def hut(h=100):
    w = h * 1.1
    im, d = _cv(w, h); k = SS * h / 100.0
    d.rectangle(P([(14, 46), (96, 98)], k), fill=(214, 186, 140, 255), outline=INK, width=int(1.2 * k))
    d.polygon(P([(4, 50), (55, 12), (106, 50)], k), fill=(190, 150, 80, 255), outline=INK)
    for y in range(22, 50, 7): d.line(P([(55 - (y - 12) * 1.3, y), (55 + (y - 12) * 1.3, y)], k), fill=(160, 120, 60, 255), width=int(0.8 * k))
    d.rectangle(P([(46, 70), (64, 98)], k), fill=(110, 70, 45, 255))
    return _out(im, w, h)

def wall(h=260, length=6, towers=True, damaged=False):
    """long crenellated land wall (reference style), `length` sections between towers"""
    seg = 100
    w = h * (seg * length + 40) / 100
    im, d = _cv(w, h); k = SS * h / 100.0
    L = seg * length + 40
    d.rectangle(P([(0, 38), (L, 100)], k), fill=STONE, outline=INK, width=int(1.0 * k))
    for x in range(0, int(L), 9):
        d.rectangle(P([(x, 31), (x + 6, 39)], k), fill=STONE, outline=INK, width=int(0.8 * k))
    for y in range(48, 100, 12):
        off = 0 if (y // 12) % 2 else 10
        for x in range(off, int(L), 20):
            d.rectangle(P([(x, y), (x + 20, y + 12)], k), outline=STONE_D, width=int(0.5 * k))
    if towers:
        for i in range(length + 1):
            tx = i * seg + 4
            d.rectangle(P([(tx, 14), (tx + 32, 100)], k), fill=(228, 212, 178, 255), outline=INK, width=int(1.0 * k))
            for x in range(int(tx), int(tx + 32), 8):
                d.rectangle(P([(x, 8), (x + 5, 15)], k), fill=(228, 212, 178, 255), outline=INK, width=int(0.8 * k))
            d.rectangle(P([(tx + 12, 34), (tx + 20, 48)], k), fill=(80, 60, 45, 255))
    if damaged:
        for i in range(0, length, 2):
            x = i * seg + 60
            d.polygon(P([(x, 31), (x + 14, 52), (x + 30, 40), (x + 42, 31)], k), fill=(0, 0, 0, 0))
    return _out(im, w, h)

def dome(h=300):
    """Hagia Sophia-like domed cathedral"""
    w = h * 1.5
    im, d = _cv(w, h); k = SS * h / 100.0
    c = (226, 160, 120, 255); cd = (196, 128, 96, 255)
    d.rectangle(P([(20, 55), (130, 98)], k), fill=c, outline=INK, width=int(1.0 * k))
    d.rectangle(P([(40, 40), (110, 58)], k), fill=cd, outline=INK, width=int(1.0 * k))
    d.chord(P([(46, 14), (104, 66)], k), 180, 360, fill=(150, 160, 170, 255), outline=INK, width=int(1.0 * k))
    d.chord(P([(22, 40), (52, 68)], k), 180, 360, fill=(150, 160, 170, 255), outline=INK); d.chord(P([(98, 40), (128, 68)], k), 180, 360, fill=(150, 160, 170, 255), outline=INK)
    for x in range(30, 128, 14): d.chord(P([(x, 66), (x + 8, 82)], k), 180, 360, fill=(80, 60, 50, 255))
    d.line(P([(75, 6), (75, 14)], k), fill=GOLD, width=int(1.4 * k)); d.line(P([(72, 9), (78, 9)], k), fill=GOLD, width=int(1.4 * k))
    return _out(im, w, h)

def minaret(h=300):
    w = h * 0.12
    im, d = _cv(w, h); k = SS * h / 100.0
    d.rectangle(P([(3, 18), (9, 100)], k), fill=(236, 226, 206, 255), outline=INK, width=int(0.6 * k))
    d.polygon(P([(2, 18), (6, 0), (10, 18)], k), fill=(150, 160, 170, 255), outline=INK)
    d.rectangle(P([(1.5, 40), (10.5, 43)], k), fill=(200, 190, 170, 255), outline=INK)
    return _out(im, w, h)

def temple(h=200):
    w = h * 1.3
    im, d = _cv(w, h); k = SS * h / 100.0
    d.polygon(P([(4, 30), (65, 4), (126, 30)], k), fill=(240, 232, 214, 255), outline=INK, width=int(1.0 * k))
    d.rectangle(P([(8, 30), (122, 38)], k), fill=(230, 220, 200, 255), outline=INK)
    for x in range(14, 120, 18): d.rectangle(P([(x, 38), (x + 8, 90)], k), fill=(244, 238, 224, 255), outline=INK, width=int(0.8 * k))
    d.rectangle(P([(2, 90), (128, 99)], k), fill=(225, 214, 192, 255), outline=INK)
    return _out(im, w, h)

def galley(h=140, col=(150, 90, 50, 255), sail=(240, 235, 220, 255), emblem=None):
    w = h * 1.7
    im, d = _cv(w, h); k = SS * h / 100.0
    d.line(P([(80, 12), (80, 66)], k), fill=(110, 75, 45, 255), width=int(2 * k))
    d.polygon(P([(52, 14), (108, 14), (114, 58), (46, 58)], k), fill=sail, outline=INK, width=int(0.9 * k))
    if emblem == 'cross':
        d.line(P([(80, 22), (80, 50)], k), fill=RED, width=int(3 * k)); d.line(P([(66, 34), (94, 34)], k), fill=RED, width=int(3 * k))
    if emblem == 'crescent':
        d.ellipse(P([(70, 24), (92, 46)], k), fill=RED); d.ellipse(P([(76, 24), (96, 44)], k), fill=sail)
    for x in range(30, 140, 12): d.line(P([(x, 74), (x - 8, 92)], k), fill=(110, 75, 45, 255), width=int(1.2 * k))
    d.polygon(P([(2, 62), (168, 62), (150, 82), (24, 82)], k), fill=col, outline=INK, width=int(1.0 * k))
    d.line(P([(10, 68), (160, 68)], k), fill=GOLD, width=int(1.2 * k))
    return _out(im, w, h)

def boat(h=80):
    w = h * 1.8
    im, d = _cv(w, h); k = SS * h / 100.0
    d.line(P([(90, 10), (90, 64)], k), fill=(110, 75, 45, 255), width=int(2 * k))
    d.polygon(P([(92, 12), (140, 58), (92, 58)], k), fill=(240, 235, 220, 255), outline=INK)
    d.polygon(P([(10, 64), (170, 64), (150, 92), (30, 92)], k), fill=(170, 110, 60, 255), outline=INK, width=int(1.2 * k))
    return _out(im, w, h)

def tree(h=160, kind='cypress'):
    w = h * (0.32 if kind == 'cypress' else 0.8)
    im, d = _cv(w, h); k = SS * h / 100.0
    if kind == 'olive':
        d.polygon(P([(36, 100), (40, 62), (34, 48), (40, 50), (44, 40), (46, 52), (52, 46), (48, 64), (50, 100)], k), fill=(120, 90, 60, 255), outline=(80, 60, 40, 255))
        for cx_, cy_, r in ((22, 34, 18), (44, 22, 20), (64, 34, 17), (32, 46, 15), (56, 48, 15), (44, 36, 18)):
            d.ellipse(P([(cx_ - r, cy_ - r * 0.8), (cx_ + r, cy_ + r * 0.8)], k), fill=(120, 150, 90, 255), outline=(85, 110, 65, 255))
        for cx_, cy_ in ((30, 30), (50, 20), (60, 40), (38, 44)):
            d.ellipse(P([(cx_ - 3, cy_ - 2), (cx_ + 3, cy_ + 2)], k), fill=(160, 185, 120, 255))
        return _out(im, w, h)
    if kind == 'cypress':
        d.rectangle(P([(14, 86), (18, 100)], k), fill=(110, 75, 45, 255))
        d.ellipse(P([(4, 4), (28, 92)], k), fill=(70, 120, 60, 255), outline=(45, 80, 40, 255))
    else:
        d.line(P([(40, 100), (44, 30)], k), fill=(130, 95, 60, 255), width=int(4 * k))
        for a in range(0, 360, 60):
            r = math.radians(a)
            d.line(P([(44, 30), (44 + 34 * math.cos(r), 30 + 16 * math.sin(r) + 10)], k), fill=(70, 130, 60, 255), width=int(5 * k))
    return _out(im, w, h)

def pedestal(h=260, inner='city'):
    """glowing display case on a plinth (the reference's spotlight prop)"""
    w = h * 0.9
    im, d = _cv(w, h); k = SS * h / 100.0
    d.rectangle(P([(12, 60), (78, 100)], k), fill=(236, 226, 196, 255), outline=(200, 190, 160, 255), width=int(0.8 * k))
    d.rounded_rectangle(P([(10, 6), (80, 60)], k), radius=int(3 * k), fill=(255, 245, 210, 150), outline=(255, 255, 240, 255), width=int(1 * k))
    d.chord(P([(20, 18), (70, 62)], k), 180, 360, fill=(240, 205, 120, 255))
    for x in (24, 36, 48, 60):
        d.rectangle(P([(x, 40 - (x % 12)), (x + 9, 58)], k), fill=(235, 210, 150, 255), outline=(190, 150, 90, 255))
    d.chord(P([(36, 28), (54, 44)], k), 180, 360, fill=(200, 160, 90, 255))
    return _out(im, w, h)

def siege_tower(h=300):
    w = h * 0.55
    im, d = _cv(w, h); k = SS * h / 100.0
    d.polygon(P([(10, 100), (16, 10), (40, 10), (46, 100)], k), fill=(196, 160, 110, 255), outline=INK, width=int(1.0 * k))
    for y in (30, 55, 80): d.line(P([(12, y), (44, y)], k), fill=(130, 95, 60, 255), width=int(1.4 * k))
    for y in (18, 42, 66): d.rectangle(P([(24, y), (32, y + 8)], k), fill=(70, 50, 35, 255))
    d.ellipse(P([(8, 92), (20, 100)], k), fill=(110, 75, 45, 255)); d.ellipse(P([(36, 92), (48, 100)], k), fill=(110, 75, 45, 255))
    return _out(im, w, h)

def tent(h=100):
    w = h * 1.2
    im, d = _cv(w, h); k = SS * h / 100.0
    d.polygon(P([(4, 98), (60, 10), (116, 98)], k), fill=(240, 236, 222, 255), outline=INK, width=int(1.0 * k))
    d.polygon(P([(48, 98), (60, 50), (72, 98)], k), fill=(180, 170, 150, 255))
    return _out(im, w, h)

def angel(h=120):
    w = h * 1.2
    im, d = _cv(w, h); k = SS * h / 100.0
    d.ellipse(P([(2, 26), (52, 60)], k), fill=(255, 255, 255, 235), outline=(200, 200, 210, 255)); d.ellipse(P([(68, 26), (118, 60)], k), fill=(255, 255, 255, 235), outline=(200, 200, 210, 255))
    d.polygon(P([(46, 40), (74, 40), (82, 96), (38, 96)], k), fill=(250, 250, 255, 255), outline=INK)
    d.ellipse(P([(46, 14), (74, 42)], k), fill=SKIN, outline=INK)
    d.ellipse(P([(44, 2), (76, 12)], k), outline=GOLD, width=int(2 * k))
    d.ellipse(P([(53, 25), (56, 28)], k), fill=INK); d.ellipse(P([(64, 25), (67, 28)], k), fill=INK)
    return _out(im, w, h)

def flask(h=120):
    w = h * 0.7
    im, d = _cv(w, h); k = SS * h / 100.0
    d.rectangle(P([(28, 4), (42, 30)], k), fill=(200, 220, 230, 220), outline=INK)
    d.ellipse(P([(6, 26), (64, 96)], k), fill=(200, 220, 230, 220), outline=INK, width=int(1.2 * k))
    d.chord(P([(8, 40), (62, 94)], k), 0, 180, fill=(240, 120, 30, 255))
    d.rectangle(P([(26, 0), (44, 6)], k), fill=(130, 90, 60, 255))
    return _out(im, w, h)

def cannon(h=120):
    """bronze siege bombard on a wooden sledge: tapered barrel, reinforcing rings, dark bore at the muzzle"""
    w = h * 2.4
    im, d = _cv(w, h); k = SS * h / 100.0
    bronze, dark = (196, 146, 64, 255), (150, 104, 38, 255)
    d.rectangle(P([(14, 72), (214, 86)], k), fill=(120, 85, 50, 255), outline=INK, width=int(1 * k))
    for x in (40, 110, 180): d.ellipse(P([(x - 13, 72), (x + 13, 98)], k), fill=(110, 75, 45, 255), outline=INK)
    d.polygon(P([(12, 30), (196, 18), (196, 70), (12, 66)], k), fill=bronze, outline=INK, width=int(1.4 * k))
    d.ellipse(P([(4, 30), (22, 66)], k), fill=dark, outline=INK, width=int(1 * k))
    for x in (60, 110, 160):
        top = 30 - (x - 12) * 12 / 184; bot = 66 + (x - 12) * 4 / 184
        d.rectangle(P([(x - 3, top - 2), (x + 3, bot + 2)], k), fill=dark, outline=INK, width=int(0.6 * k))
    d.ellipse(P([(186, 12), (216, 76)], k), fill=bronze, outline=INK, width=int(1.4 * k))
    d.ellipse(P([(193, 24), (209, 64)], k), fill=(40, 30, 24, 255))
    return _out(im, w, h)

def chain(h=40, length=600):
    w = length
    im, d = _cv(w, h); k = SS * h / 100.0
    n = int(w / (h * 0.9))
    for i in range(n):
        x = i * 90 * w / (n * 90) * 100 / h
        d.ellipse(P([(x, 20), (x + 110, 80)], k), outline=(90, 90, 96, 255), width=int(14 * k))
    return _out(im, w, h)

KINDS = {'house': house, 'hut': hut, 'wall': wall, 'dome': dome, 'minaret': minaret, 'temple': temple, 'galley': galley,
         'boat': boat, 'tree': tree, 'pedestal': pedestal, 'siege_tower': siege_tower, 'tent': tent, 'angel': angel,
         'flask': flask, 'cannon': cannon, 'chain': chain}

@lru_cache(maxsize=400)
def get(kind, h, **kw):
    return _get(kind, h, tuple(sorted(kw.items())))

@lru_cache(maxsize=400)
def _get(kind, h, kw):
    kw = dict(kw)
    if kind.startswith('fig-'): return figure(kind[4:], int(h), **kw)
    return KINDS[kind](int(h), **kw)


# ------------------------------------------------------------------ more props (scenes 23-161)
SEA = (70, 130, 190, 255); LAND = (232, 210, 160, 255); PARCH = (238, 222, 186, 255)

def cityplan(h=560, chain=False, route=False, walls=True, cannons=False, ships=False, gate=False, galata=True, fleet_in=False):
    """parchment card with an illustrated plan of Constantinople (reference's 'old city' card)"""
    w = h * 1.35
    im, d = _cv(w, h); k = SS * h / 100.0
    d.rounded_rectangle(P([(1, 1), (134, 99)], k), radius=int(3 * k), fill=PARCH, outline=(150, 120, 80, 255), width=int(0.8 * k))
    d.rectangle(P([(6, 6), (129, 94)], k), fill=SEA)
    # Thrace (west) + the triangular peninsula
    d.polygon(P([(6, 6), (78, 6), (74, 26), (68, 34), (96, 40), (104, 50), (92, 66), (72, 80), (40, 86), (6, 88)], k), fill=LAND, outline=(120, 95, 60, 255), width=int(0.6 * k))
    # Golden Horn (inlet north of the peninsula)
    d.polygon(P([(96, 40), (68, 34), (40, 28), (24, 22), (42, 33), (70, 41), (92, 46)], k), fill=SEA)
    if galata:   # Galata / Pera hills north of the Horn
        d.polygon(P([(78, 6), (129, 6), (129, 30), (110, 36), (96, 38), (74, 26)], k), fill=(214, 196, 150, 255), outline=(120, 95, 60, 255), width=int(0.6 * k))
        for x, y in ((92, 18), (104, 22), (116, 16)):
            d.chord(P([(x - 8, y - 4), (x + 8, y + 6)], k), 180, 360, fill=(190, 170, 120, 255))
    # Asia across the Bosphorus
    d.polygon(P([(118, 44), (129, 40), (129, 94), (108, 94), (112, 70)], k), fill=(214, 196, 150, 255), outline=(120, 95, 60, 255), width=int(0.6 * k))
    # city: roofs
    import random
    rnd = random.Random(5)
    for _ in range(70):
        x, y = rnd.uniform(48, 92), rnd.uniform(44, 76)
        if y > 44 + (x - 48) * 0.1 and not (x > 88 and y > 64):
            d.rectangle(P([(x, y), (x + 2.6, y + 2)], k), fill=(196, 92, 60, 255))
    d.ellipse(P([(80, 52), (88, 58)], k), fill=(150, 160, 170, 255), outline=INK)    # Hagia Sophia
    if walls:   # Theodosian land walls across the peninsula
        d.line(P([(46, 30), (44, 52), (40, 70), (38, 86)], k), fill=(110, 90, 70, 255), width=int(2.2 * k))
        for t in range(6):
            yy = 32 + t * 10; xx = 46 - t * 1.4
            d.rectangle(P([(xx - 1.6, yy - 1.6), (xx + 1.6, yy + 1.6)], k), fill=(110, 90, 70, 255))
    if chain:
        d.line(P([(92, 46), (98, 38)], k), fill=(60, 60, 64, 255), width=int(1.6 * k))
        for t in range(6):
            x, y = 92 + t * 1.2, 46 - t * 1.6
            d.ellipse(P([(x - 0.9, y - 0.9), (x + 0.9, y + 0.9)], k), outline=(230, 230, 235, 255), width=int(0.4 * k))
    if route:
        pts = [(112, 12), (100, 14), (86, 20), (72, 26), (58, 30)]
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            for j in range(4):
                if j % 2 == 0:
                    d.line(P([(x0 + (x1 - x0) * j / 4, y0 + (y1 - y0) * j / 4), (x0 + (x1 - x0) * (j + 1) / 4, y0 + (y1 - y0) * (j + 1) / 4)], k), fill=RED, width=int(1.4 * k))
    if fleet_in or ships:
        for x, y in ((50, 30), (58, 32), (66, 35)) if fleet_in else ((112, 12), (116, 20)):
            d.polygon(P([(x - 3, y), (x + 3, y), (x + 2, y + 1.6), (x - 2, y + 1.6)], k), fill=(150, 90, 50, 255))
            d.polygon(P([(x, y - 4), (x + 2.5, y - 0.5), (x, y - 0.5)], k), fill=WHITE)
    if cannons:
        for y in (40, 56, 72):
            d.ellipse(P([(30, y - 2), (36, y + 2)], k), fill=(60, 60, 64, 255))
            d.line(P([(36, y), (41, y - 1)], k), fill=RED, width=int(0.8 * k))
    if gate:
        d.ellipse(P([(40, 40), (50, 50)], k), outline=RED, width=int(1.2 * k))
    return _out(im, w, h)

def walls_section(h=420, stage=4):
    """cross-section of the Theodosian walls: moat, outer wall, peribolos, inner wall (stage = how many shown)"""
    w = h * 2.3
    im, d = _cv(w, h); k = SS * h / 100.0
    d.rectangle(P([(0, 86), (230, 100)], k), fill=(190, 160, 110, 255))
    if stage >= 1:   # moat
        d.polygon(P([(10, 86), (14, 98), (54, 98), (58, 86)], k), fill=(214, 196, 150, 255), outline=INK)
        d.rectangle(P([(15, 90), (53, 97)], k), fill=(80, 140, 200, 255))
    if stage >= 2:   # outer wall
        d.rectangle(P([(70, 50), (84, 86)], k), fill=STONE, outline=INK, width=int(0.8 * k))
        for x in range(70, 84, 4): d.rectangle(P([(x, 46), (x + 2.5, 50)], k), fill=STONE, outline=INK)
    if stage >= 3:   # peribolos
        d.rectangle(P([(84, 82), (130, 86)], k), fill=(205, 180, 130, 255))
    if stage >= 4:   # inner wall (taller, thicker)
        d.rectangle(P([(130, 18), (156, 86)], k), fill=(228, 212, 178, 255), outline=INK, width=int(0.9 * k))
        for x in range(130, 156, 5): d.rectangle(P([(x, 12), (x + 3, 18)], k), fill=(228, 212, 178, 255), outline=INK)
        d.rectangle(P([(160, 4), (190, 86)], k), fill=(232, 218, 186, 255), outline=INK, width=int(0.9 * k))
        for x in range(160, 190, 6): d.rectangle(P([(x, -2), (x + 3.5, 4)], k), fill=(232, 218, 186, 255), outline=INK)
    return _out(im, w, h)

def ox(h=120):
    w = h * 1.5
    im, d = _cv(w, h); k = SS * h / 100.0
    c = (150, 110, 80, 255)
    d.ellipse(P([(20, 30), (110, 74)], k), fill=c, outline=INK, width=int(1 * k))
    for x in (30, 48, 86, 100): d.rectangle(P([(x, 64), (x + 6, 96)], k), fill=c, outline=INK)
    d.ellipse(P([(104, 24), (138, 56)], k), fill=c, outline=INK, width=int(1 * k))
    d.arc(P([(100, 8), (122, 34)], k), 180, 300, fill=WHITE, width=int(3 * k)); d.arc(P([(122, 8), (144, 34)], k), 240, 360, fill=WHITE, width=int(3 * k))
    d.ellipse(P([(118, 34), (122, 38)], k), fill=INK)
    return _out(im, w, h)

def hippodrome(h=200):
    w = h * 2.2
    im, d = _cv(w, h); k = SS * h / 100.0
    d.rounded_rectangle(P([(4, 20), (216, 96)], k), radius=int(36 * k), fill=(226, 206, 166, 255), outline=INK, width=int(1.2 * k))
    d.rounded_rectangle(P([(24, 36), (196, 82)], k), radius=int(22 * k), fill=(210, 180, 120, 255), outline=INK)
    d.line(P([(50, 59), (170, 59)], k), fill=(160, 140, 110, 255), width=int(4 * k))
    d.polygon(P([(108, 59), (110, 30), (112, 59)], k), fill=(200, 190, 170, 255), outline=INK)
    import random
    rnd = random.Random(2)
    for _ in range(90):
        x, y = rnd.uniform(10, 210), rnd.uniform(22, 34) if rnd.random() < 0.5 else rnd.uniform(84, 94)
        d.ellipse(P([(x - 1.4, y - 1.4), (x + 1.4, y + 1.4)], k), fill=rnd.choice([(200, 60, 50, 255), (60, 90, 170, 255), (240, 200, 60, 255), (240, 240, 240, 255)]))
    return _out(im, w, h)

def candle(h=120):
    w = h * 0.35
    im, d = _cv(w, h); k = SS * h / 100.0
    d.rectangle(P([(10, 40), (25, 100)], k), fill=(245, 236, 210, 255), outline=INK)
    d.polygon(P([(17.5, 14), (24, 32), (17.5, 40), (11, 32)], k), fill=(255, 200, 60, 255))
    d.ellipse(P([(14, 26), (21, 36)], k), fill=(255, 245, 180, 255))
    return _out(im, w, h)

def banner(h=200, side='ottoman'):
    w = h * 0.7
    im, d = _cv(w, h); k = SS * h / 100.0
    d.line(P([(6, 2), (6, 100)], k), fill=(110, 75, 45, 255), width=int(2.4 * k))
    col = (200, 40, 40, 255) if side == 'ottoman' else (130, 40, 120, 255)
    d.polygon(P([(7, 6), (66, 10), (60, 26), (66, 42), (7, 40)], k), fill=col, outline=INK)
    if side == 'ottoman':
        d.ellipse(P([(22, 12), (44, 34)], k), fill=WHITE); d.ellipse(P([(28, 12), (48, 32)], k), fill=col)
    else:
        d.text((20 * k, 14 * k), '', fill=GOLD)
        d.line(P([(28, 12), (28, 36)], k), fill=GOLD, width=int(2 * k)); d.line(P([(18, 22), (38, 22)], k), fill=GOLD, width=int(2 * k))
    return _out(im, w, h)

def cannonball(h=80):
    im, d = _cv(h, h); k = SS * h / 100.0
    d.ellipse(P([(4, 4), (96, 96)], k), fill=(130, 126, 120, 255), outline=INK, width=int(2 * k))
    d.ellipse(P([(22, 18), (44, 38)], k), fill=(180, 176, 170, 255))
    return _out(im, h, h)

def subscribe(h=110):
    w = h * 3.4
    im, d = _cv(w, h); k = SS * h / 100.0
    d.rounded_rectangle(P([(2, 8), (338, 92)], k), radius=int(16 * k), fill=(220, 30, 30, 255))
    from PIL import ImageFont
    import os
    f = ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'fredoka.ttf'), int(46 * k))
    d.text((170 * k, 50 * k), 'SUBSCRIBE', font=f, fill=WHITE, anchor='mm')
    return _out(im, w, h)

def logs(h=60, length=6):
    w = h * length * 0.6
    im, d = _cv(w, h); k = SS * h / 100.0
    for i in range(length):
        x = i * 60
        d.ellipse(P([(x, 30), (x + 56, 96)], k), fill=(150, 105, 60, 255), outline=INK)
        d.ellipse(P([(x + 14, 46), (x + 42, 80)], k), outline=(110, 75, 45, 255), width=int(2 * k))
    return _out(im, w, h)

def skyline_modern(h=300):
    """modern Istanbul: domes, minarets, towers"""
    w = h * 3
    im, d = _cv(w, h); k = SS * h / 100.0
    import random
    rnd = random.Random(8)
    for i in range(26):
        x = i * 11.5; bh = rnd.uniform(30, 70)
        d.rectangle(P([(x, 100 - bh), (x + 10, 100)], k), fill=(rnd.randint(150, 200), rnd.randint(140, 180), rnd.randint(150, 200), 255), outline=INK, width=int(0.5 * k))
        for wy in range(int(100 - bh + 4), 98, 7): d.rectangle(P([(x + 2, wy), (x + 4, wy + 3)], k), fill=(250, 230, 150, 255))
    d.chord(P([(120, 40), (180, 96)], k), 180, 360, fill=(150, 160, 170, 255), outline=INK)
    for mx in (110, 190): d.rectangle(P([(mx, 10), (mx + 4, 100)], k), fill=(236, 226, 206, 255), outline=INK); d.polygon(P([(mx - 1, 10), (mx + 2, 0), (mx + 5, 10)], k), fill=(150, 160, 170, 255))
    return _out(im, w, h)

KINDS.update({'cityplan': cityplan, 'walls_section': walls_section, 'ox': ox, 'hippodrome': hippodrome, 'candle': candle,
              'banner': banner, 'cannonball': cannonball, 'subscribe': subscribe, 'logs': logs, 'skyline_modern': skyline_modern})


# ------------------------------------------------------------------ Ottoman props
def sheep(h=80):
    w = h * 1.4
    im, d = _cv(w, h); k = SS * h / 100.0
    for x in (34, 56, 92, 112): d.rectangle(P([(x, 64), (x + 6, 96)], k), fill=INK)
    for cx, cy, r in ((50, 46, 26), (78, 40, 28), (104, 48, 24), (70, 58, 24), (40, 58, 18)):
        d.ellipse(P([(cx - r, cy - r), (cx + r, cy + r)], k), fill=(248, 246, 238, 255), outline=(200, 196, 186, 255), width=int(1.5 * k))
    d.ellipse(P([(118, 28), (138, 54)], k), fill=(70, 60, 55, 255))
    d.ellipse(P([(127, 36), (131, 40)], k), fill=WHITE)
    return _out(im, w, h)

def yurt(h=150, col=(244, 238, 222, 255)):
    w = h * 1.3
    im, d = _cv(w, h); k = SS * h / 100.0
    d.rectangle(P([(10, 48), (120, 98)], k), fill=col, outline=INK, width=int(1.2 * k))
    d.chord(P([(4, 10), (126, 70)], k), 180, 360, fill=(226, 214, 186, 255), outline=INK, width=int(1.2 * k))
    for x in (30, 50, 70, 90, 110): d.line(P([(x, 52), (x, 96)], k), fill=(200, 60, 50, 255), width=int(1.6 * k))
    d.rectangle(P([(54, 66), (76, 98)], k), fill=(150, 60, 40, 255), outline=INK)
    d.line(P([(62, 4), (64, 12)], k), fill=(150, 150, 150, 200), width=int(2 * k))
    return _out(im, w, h)

def horseman(h=200, robe=(170, 60, 40, 255), flag=False):
    """rider on a horse; drawn in a 130x120 box (top 20 units leave room for the spear/flag)"""
    w = h * 1.3
    im, d = _cv(w, h); k = SS * h / 120.0
    Q = lambda pts: [(x * k, (y + 20) * k) for x, y in pts]
    hc, hd = (150, 100, 60, 255), (110, 70, 40, 255)
    for x, dx in ((30, -5), (44, 4), (80, -5), (94, 4)): d.line(Q([(x, 68), (x + dx, 98)]), fill=hd, width=int(4 * k))
    d.ellipse(Q([(18, 44), (104, 76)]), fill=hc, outline=INK, width=int(1 * k))
    d.polygon(Q([(92, 56), (104, 30), (114, 30), (104, 62)]), fill=hc, outline=INK, width=int(1 * k))      # neck
    d.ellipse(Q([(100, 20), (128, 40)]), fill=hc, outline=INK, width=int(1 * k))                         # head
    d.polygon(Q([(104, 22), (108, 12), (112, 22)]), fill=hd)                                               # ear
    d.ellipse(Q([(117, 26), (120, 29)]), fill=INK)
    d.polygon(Q([(96, 30), (104, 26), (100, 56), (92, 54)]), fill=(70, 45, 30, 255))                     # mane
    d.line(Q([(20, 54), (6, 78)]), fill=(70, 45, 30, 255), width=int(4 * k))                             # tail
    d.polygon(Q([(48, 46), (74, 46), (70, 54), (52, 54)]), fill=(200, 40, 40, 255))                        # saddle cloth
    d.rectangle(Q([(52, 22), (70, 48)]), fill=robe, outline=INK, width=int(0.8 * k))
    d.line(Q([(60, 46), (56, 62)]), fill=INK, width=int(2.4 * k))
    d.ellipse(Q([(52, 4), (70, 24)]), fill=SKIN, outline=INK, width=int(0.8 * k))
    d.ellipse(Q([(55.5, 12), (58, 15)]), fill=INK); d.ellipse(Q([(63, 12), (65.5, 15)]), fill=INK)
    d.ellipse(Q([(48, -2), (74, 10)]), fill=WHITE, outline=INK)
    if flag:
        d.line(Q([(72, 30), (76, -18)]), fill=(120, 85, 50, 255), width=int(1.6 * k))
        d.polygon(Q([(76, -18), (100, -12), (76, -4)]), fill=(200, 40, 40, 255))
        d.ellipse(Q([(80, -15), (88, -7)]), fill=WHITE); d.ellipse(Q([(82, -15), (90, -7)]), fill=(200, 40, 40, 255))
    else:
        d.line(Q([(72, 34), (84, -14)]), fill=(120, 85, 50, 255), width=int(1.4 * k))
        d.polygon(Q([(82, -20), (87, -10), (81, -11)]), fill=(180, 180, 185, 255))
    return _out(im, w, h)

def cage(h=260):
    w = h * 0.8
    im, d = _cv(w, h); k = SS * h / 100.0
    d.rectangle(P([(4, 6), (76, 98)], k), fill=(250, 244, 228, 120))
    for x in range(8, 78, 9): d.line(P([(x, 8), (x, 96)], k), fill=(150, 120, 60, 255), width=int(2.4 * k))
    for y in (8, 96): d.line(P([(4, y), (76, y)], k), fill=(150, 120, 60, 255), width=int(4 * k))
    d.chord(P([(4, -10), (76, 26)], k), 180, 360, fill=(190, 150, 70, 255), outline=INK)
    return _out(im, w, h)

def stamp(h=140, text='GONE?'):
    from PIL import ImageFont
    import os
    w = h * 2.4
    im, d = _cv(w, h); k = SS * h / 100.0
    d.rounded_rectangle(P([(4, 6), (236, 94)], k), radius=int(10 * k), outline=(200, 40, 30, 255), width=int(7 * k))
    f = ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'fredoka.ttf'), int(62 * k))
    d.text((120 * k, 52 * k), text, font=f, fill=(200, 40, 30, 255), anchor='mm')
    return _out(im, w, h).rotate(-8, resample=Image.BICUBIC, expand=True)

KINDS.update({'sheep': sheep, 'yurt': yurt, 'horseman': horseman, 'cage': cage, 'stamp': stamp})
KINDS['olive'] = lambda h=160: tree(h, 'olive')
