"""Hand-drawn-style card icons (flat colours, thick dark outlines) used instead of emoji.
Each function draws on a 240x240 RGBA canvas; draw_icon(key, size) returns the resized image."""
import math
from PIL import Image, ImageDraw

INK = (58, 38, 24)
OW = 7  # outline width

GOLD = (232, 186, 60); GOLD_D = (190, 140, 40); SAND = (222, 186, 120); SAND_D = (190, 150, 90)
BLUE = (70, 140, 205); BLUE_L = (150, 200, 240); GREEN = (110, 165, 80); GREEN_D = (70, 120, 55)
RED = (205, 60, 50); WHITE = (250, 247, 238); GREY = (165, 160, 155); GREY_D = (120, 115, 110)
BROWN = (150, 100, 60); BROWN_L = (195, 150, 100); PAPYRUS = (240, 222, 170); SKIN = (232, 190, 150)

def _c():
    im = Image.new('RGBA', (240, 240), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)

def scroll():
    im, d = _c()
    d.rectangle((50, 60, 190, 180), fill=PAPYRUS, outline=INK, width=OW)
    for y in (88, 108, 128, 148): d.line((70, y, 170 - (y % 3) * 10, y), fill=BROWN, width=5)
    for x in (40, 200):
        d.rounded_rectangle((x - 16, 48, x + 16, 192), radius=14, fill=BROWN_L, outline=INK, width=OW)
    return im

def temple():
    im, d = _c()
    d.polygon([(30, 80), (120, 35), (210, 80)], fill=SAND, outline=INK, width=OW)
    d.rectangle((35, 80, 205, 96), fill=SAND_D, outline=INK, width=OW)
    for x in (52, 92, 132, 172):
        d.rectangle((x, 96, x + 18, 180), fill=WHITE, outline=INK, width=6)
    d.rectangle((25, 180, 215, 200), fill=SAND_D, outline=INK, width=OW)
    return im

def pyramid():
    im, d = _c()
    d.polygon([(120, 30), (220, 200), (20, 200)], fill=SAND, outline=INK, width=OW)
    d.polygon([(120, 30), (220, 200), (140, 200)], fill=SAND_D, outline=INK, width=OW)
    for y in range(70, 200, 26): d.line(((120 - (y - 30) * 0.58), y, (120 + (y - 30) * 0.47), y), fill=BROWN, width=3)
    return im

def crown():
    """pharaoh's double crown: tall white crown inside the red crown"""
    im, d = _c()
    d.polygon([(45, 210), (195, 210), (195, 50), (165, 50), (165, 125), (45, 125)], fill=RED, outline=INK, width=OW)
    d.polygon([(85, 210), (155, 210), (148, 120), (136, 50), (104, 50), (92, 120)], fill=WHITE, outline=INK, width=OW)
    d.ellipse((100, 26, 140, 66), fill=WHITE, outline=INK, width=OW)
    d.rectangle((45, 190, 195, 210), fill=GOLD, outline=INK, width=5)
    d.polygon([(112, 190), (128, 190), (124, 160), (116, 160)], fill=(60, 140, 90), outline=INK)   # cobra on the brow
    d.ellipse((111, 148, 129, 166), fill=(60, 140, 90), outline=INK, width=3)
    return im

def river():
    """the Nile: blue water between sandy banks with reeds"""
    im, d = _c()
    d.rounded_rectangle((20, 40, 220, 200), radius=24, fill=SAND, outline=INK, width=OW)
    d.polygon([(20, 95), (220, 80), (220, 160), (20, 175)], fill=BLUE)
    d.line([(20, 95), (220, 80)], fill=INK, width=5); d.line([(20, 175), (220, 160)], fill=INK, width=5)
    for x, y in ((50, 120), (110, 112), (160, 135), (80, 148)):
        d.arc((x, y, x + 40, y + 16), 200, 340, fill=BLUE_L, width=5)
    for x in (40, 55, 190, 205):
        d.line((x, 95 if x < 120 else 80, x - 4, 55), fill=GREEN_D, width=5)
        d.ellipse((x - 10, 45, x + 2, 62), fill=BROWN)
    return im

def coin():
    im, d = _c()
    d.ellipse((35, 35, 205, 205), fill=GOLD, outline=INK, width=OW)
    d.ellipse((60, 60, 180, 180), outline=GOLD_D, width=6)
    d.ellipse((102, 70, 138, 112), outline=INK, width=8)                 # ankh
    d.line((120, 110, 120, 165), fill=INK, width=9); d.line((95, 125, 145, 125), fill=INK, width=9)
    return im

def eye():
    im, d = _c()
    d.ellipse((40, 80, 200, 150), fill=WHITE, outline=INK, width=OW)
    d.ellipse((98, 84, 142, 146), fill=INK)
    d.line((30, 70, 210, 60), fill=INK, width=9)
    d.line((120, 150, 105, 205), fill=INK, width=9); d.arc((125, 140, 195, 210), 180, 300, fill=INK, width=9)
    d.line((195, 110, 225, 120), fill=INK, width=9)
    return im

def swords():
    """two crossed bronze swords with gold hilts"""
    im, d = _c()
    for flip in (1, -1):
        x0, y0, x1, y1 = (40, 200, 190, 40) if flip == 1 else (200, 200, 50, 40)
        ang = math.atan2(y1 - y0, x1 - x0); nx, ny = -math.sin(ang), math.cos(ang)
        w = 13
        blade = [(x0 + (x1 - x0) * 0.28 + nx * w, y0 + (y1 - y0) * 0.28 + ny * w), (x1 + nx * 3, y1 + ny * 3),
                 (x1 + (x1 - x0) * 0.04, y1 + (y1 - y0) * 0.04), (x1 - nx * 3, y1 - ny * 3),
                 (x0 + (x1 - x0) * 0.28 - nx * w, y0 + (y1 - y0) * 0.28 - ny * w)]
        d.polygon(blade, fill=(205, 170, 110), outline=INK, width=6)
        gx, gy = x0 + (x1 - x0) * 0.28, y0 + (y1 - y0) * 0.28
        d.line((gx + nx * 30, gy + ny * 30, gx - nx * 30, gy - ny * 30), fill=INK, width=18)
        d.line((gx + nx * 27, gy + ny * 27, gx - nx * 27, gy - ny * 27), fill=GOLD, width=10)
        d.line((x0, y0, gx, gy), fill=INK, width=18); d.line((x0, y0, gx, gy), fill=BROWN, width=10)
        d.ellipse((x0 - 12, y0 - 12, x0 + 12, y0 + 12), fill=GOLD, outline=INK, width=4)
    return im

def seasons():
    """the Egyptian year: a wheel of three seasons (flood / growing / harvest)"""
    im, d = _c()
    box = (30, 30, 210, 210)
    d.pieslice(box, -90, 30, fill=BLUE, outline=INK, width=OW)
    d.pieslice(box, 30, 150, fill=GREEN, outline=INK, width=OW)
    d.pieslice(box, 150, 270, fill=GOLD, outline=INK, width=OW)
    d.arc((140, 70, 180, 90), 200, 340, fill=WHITE, width=6); d.arc((135, 90, 175, 110), 200, 340, fill=WHITE, width=6)
    d.line((120, 175, 120, 145), fill=WHITE, width=6); d.ellipse((104, 132, 122, 150), fill=WHITE); d.ellipse((118, 132, 136, 150), fill=WHITE)
    for k in range(3): d.line((70 + k * 10, 120, 74 + k * 10, 80), fill=WHITE, width=5)
    d.ellipse((108, 108, 132, 132), fill=WHITE, outline=INK, width=5)
    return im

def wheat():
    im, d = _c()
    for dx, tilt in ((-30, -0.35), (0, 0), (30, 0.35)):
        x0, y0 = 120 + dx * 0.3, 205
        x1, y1 = 120 + dx + tilt * 60, 70
        d.line((x0, y0, x1, y1), fill=GREEN_D, width=7)
        for k in range(5):
            t = k / 5; x = x1 + (x0 - x1) * t * 0.45; y = y1 + (y0 - y1) * t * 0.45
            for s in (-1, 1):
                d.ellipse((x + s * 9 - 9, y - 12, x + s * 9 + 9, y + 12), fill=GOLD, outline=INK, width=3)
        d.ellipse((x1 - 8, y1 - 22, x1 + 8, y1 + 4), fill=GOLD, outline=INK, width=3)
    d.rounded_rectangle((95, 160, 145, 176), radius=6, fill=BROWN_L, outline=INK, width=4)
    return im

def map_():
    im, d = _c()
    d.polygon([(25, 55), (85, 40), (155, 55), (215, 40), (215, 195), (155, 210), (85, 195), (25, 210)], fill=PAPYRUS, outline=INK, width=OW)
    d.line((85, 40, 85, 195), fill=SAND_D, width=4); d.line((155, 55, 155, 210), fill=SAND_D, width=4)
    d.polygon([(40, 80), (110, 70), (120, 120), (70, 150), (40, 130)], fill=(205, 175, 115))
    d.line([(60, 170), (100, 140), (140, 150), (180, 100)], fill=RED, width=6)
    d.line((170, 90, 190, 110), fill=RED, width=7); d.line((190, 90, 170, 110), fill=RED, width=7)
    return im

def hourglass():
    im, d = _c()
    d.rectangle((60, 30, 180, 48), fill=BROWN, outline=INK, width=OW); d.rectangle((60, 192, 180, 210), fill=BROWN, outline=INK, width=OW)
    d.polygon([(75, 48), (165, 48), (128, 120), (165, 192), (75, 192), (112, 120)], fill=(220, 235, 245), outline=INK, width=OW)
    d.polygon([(88, 60), (152, 60), (122, 110), (118, 110)], fill=SAND)
    d.polygon([(118, 150), (122, 150), (158, 188), (82, 188)], fill=SAND)
    return im

def crowd():
    """people rising up: three figures with raised arms"""
    im, d = _c()
    for x, h, col in ((60, 0, (200, 120, 90)), (180, 0, (110, 140, 190)), (120, -20, (210, 170, 80))):
        d.line((x - 18, 150 + h, x - 38, 80 + h), fill=INK, width=8); d.line((x + 18, 150 + h, x + 38, 80 + h), fill=INK, width=8)
        d.ellipse((x - 26, 92 + h, x + 26, 144 + h), fill=SKIN, outline=INK, width=6)
        d.rounded_rectangle((x - 30, 150 + h, x + 30, 215), radius=12, fill=col, outline=INK, width=6)
    return im

def boat():
    """a Nile felucca"""
    im, d = _c()
    d.line((120, 30, 120, 165), fill=BROWN, width=8)
    d.polygon([(124, 35), (200, 150), (124, 150)], fill=WHITE, outline=INK, width=OW)
    d.polygon([(116, 60), (60, 150), (116, 150)], fill=(240, 230, 210), outline=INK, width=OW)
    d.polygon([(25, 160), (215, 160), (190, 200), (50, 200)], fill=BROWN, outline=INK, width=OW)
    d.arc((30, 195, 90, 215), 200, 340, fill=BLUE, width=6); d.arc((140, 195, 200, 215), 200, 340, fill=BLUE, width=6)
    return im

def stone():
    im, d = _c()
    d.polygon([(40, 90), (140, 60), (210, 95), (110, 125)], fill=(215, 205, 185), outline=INK, width=OW)
    d.polygon([(40, 90), (110, 125), (110, 205), (40, 170)], fill=(190, 178, 155), outline=INK, width=OW)
    d.polygon([(110, 125), (210, 95), (210, 175), (110, 205)], fill=(165, 152, 130), outline=INK, width=OW)
    return im

def books():
    im, d = _c()
    for i, (col, y) in enumerate(((RED, 165), (BLUE, 125), (GREEN, 85))):
        x = 45 + (i % 2) * 14
        d.rounded_rectangle((x, y, x + 150, y + 40), radius=6, fill=col, outline=INK, width=OW)
        d.rectangle((x + 125, y + 6, x + 140, y + 34), fill=WHITE)
    return im

def coffin():
    im, d = _c()
    d.rounded_rectangle((75, 20, 165, 220), radius=40, fill=GOLD, outline=INK, width=OW)
    d.ellipse((92, 40, 148, 100), fill=(60, 110, 180), outline=INK, width=5)
    d.ellipse((100, 50, 140, 92), fill=GOLD, outline=INK, width=4)
    d.ellipse((108, 64, 116, 72), fill=INK); d.ellipse((124, 64, 132, 72), fill=INK)
    for y in (115, 135, 155): d.line((88, y, 152, y), fill=(60, 110, 180), width=7)
    d.line((105, 175, 135, 205), fill=INK, width=6); d.line((135, 175, 105, 205), fill=INK, width=6)
    return im

def money():
    im, d = _c()
    d.ellipse((45, 80, 195, 220), fill=BROWN_L, outline=INK, width=OW)
    d.polygon([(90, 85), (150, 85), (165, 50), (75, 50)], fill=BROWN_L, outline=INK, width=OW)
    d.line((85, 88, 155, 88), fill=INK, width=8)
    d.ellipse((95, 120, 145, 175), fill=GOLD, outline=INK, width=5)
    return im

def church():
    im, d = _c()
    d.rectangle((60, 100, 180, 205), fill=WHITE, outline=INK, width=OW)
    d.polygon([(50, 105), (120, 50), (190, 105)], fill=RED, outline=INK, width=OW)
    d.line((120, 50, 120, 10), fill=INK, width=7); d.line((104, 24, 136, 24), fill=INK, width=7)
    d.rounded_rectangle((100, 145, 140, 205), radius=18, fill=BROWN, outline=INK, width=5)
    return im

def mosque():
    im, d = _c()
    d.rectangle((50, 120, 170, 205), fill=WHITE, outline=INK, width=OW)
    d.pieslice((60, 55, 160, 165), 180, 360, fill=(90, 160, 120), outline=INK, width=OW)
    d.rectangle((180, 60, 205, 205), fill=WHITE, outline=INK, width=6)
    d.polygon([(178, 62), (207, 62), (192, 30)], fill=(90, 160, 120), outline=INK, width=5)
    d.rounded_rectangle((95, 155, 125, 205), radius=14, fill=BROWN, outline=INK, width=5)
    return im

def rain():
    im, d = _c()
    for x, y, r in ((80, 95, 40), (125, 75, 50), (170, 100, 35)):
        d.ellipse((x - r, y - r, x + r, y + r), fill=(200, 205, 215), outline=INK, width=OW)
    d.rounded_rectangle((45, 95, 200, 135), radius=20, fill=(200, 205, 215))
    d.line((45, 135, 200, 135), fill=INK, width=OW)
    for x in (70, 105, 140, 175):
        d.line((x, 155, x - 10, 185), fill=BLUE, width=8)
    return im

def chariot():
    im, d = _c()
    d.polygon([(70, 90), (150, 90), (160, 150), (70, 150)], fill=GOLD, outline=INK, width=OW)
    d.line((150, 140, 225, 120), fill=BROWN, width=8)
    d.ellipse((60, 120, 140, 200), fill=BROWN_L, outline=INK, width=OW)
    for a in range(0, 180, 30):
        r = math.radians(a); d.line((100 - 34 * math.cos(r), 160 - 34 * math.sin(r), 100 + 34 * math.cos(r), 160 + 34 * math.sin(r)), fill=INK, width=4)
    d.ellipse((93, 153, 107, 167), fill=INK)
    return im

def fort():
    im, d = _c()
    d.rectangle((40, 90, 200, 205), fill=(205, 180, 135), outline=INK, width=OW)
    for x in range(40, 200, 32): d.rectangle((x, 65, x + 18, 90), fill=(205, 180, 135), outline=INK, width=5)
    d.rounded_rectangle((100, 140, 140, 205), radius=18, fill=BROWN, outline=INK, width=5)
    d.line((120, 65, 120, 25), fill=INK, width=5); d.polygon([(122, 25), (160, 35), (122, 45)], fill=RED, outline=INK)
    return im

def chart():
    im, d = _c()
    d.pieslice((35, 35, 205, 205), -90, 140, fill=GOLD, outline=INK, width=OW)
    d.pieslice((35, 35, 205, 205), 140, 270, fill=RED, outline=INK, width=OW)
    return im

def sun():
    im, d = _c()
    for a in range(0, 360, 30):
        r = math.radians(a); d.line((120 + 70 * math.cos(r), 120 + 70 * math.sin(r), 120 + 105 * math.cos(r), 120 + 105 * math.sin(r)), fill=(240, 160, 40), width=10)
    d.ellipse((55, 55, 185, 185), fill=(250, 200, 60), outline=INK, width=OW)
    return im

def star():
    im, d = _c()
    pts = [(120 + (95 if k % 2 == 0 else 40) * math.cos(math.radians(-90 + k * 36)), 125 + (95 if k % 2 == 0 else 40) * math.sin(math.radians(-90 + k * 36))) for k in range(10)]
    d.polygon(pts, fill=GOLD, outline=INK, width=OW)
    return im

def tablet():
    im, d = _c()
    d.rounded_rectangle((55, 30, 185, 210), radius=24, fill=(190, 140, 95), outline=INK, width=OW)
    for y in range(60, 200, 24):
        for x in range(75, 170, 22):
            d.polygon([(x, y), (x + 12, y + 4), (x, y + 8)], fill=(120, 80, 50))
    return im

def lock():
    im, d = _c()
    d.arc((75, 30, 165, 130), 180, 360, fill=GREY_D, width=18)
    d.line((75, 80, 75, 110), fill=GREY_D, width=18); d.line((165, 80, 165, 110), fill=GREY_D, width=18)
    d.rounded_rectangle((55, 100, 185, 210), radius=16, fill=GOLD, outline=INK, width=OW)
    d.ellipse((108, 130, 132, 154), fill=INK); d.rectangle((115, 150, 125, 180), fill=INK)
    return im

def lamp():
    im, d = _c()
    d.ellipse((40, 130, 190, 200), fill=BROWN_L, outline=INK, width=OW)
    d.polygon([(180, 150), (225, 140), (190, 175)], fill=BROWN_L, outline=INK, width=OW)
    d.polygon([(210, 135), (200, 80), (225, 110), (228, 135)], fill=(250, 170, 40), outline=INK, width=4)
    d.ellipse((90, 120, 140, 145), fill=(120, 80, 50))
    return im

def check():
    im, d = _c()
    d.ellipse((30, 30, 210, 210), fill=(120, 190, 90), outline=INK, width=OW)
    d.line([(70, 125), (105, 160), (170, 85)], fill=WHITE, width=20, joint='curve')
    return im

def question():
    im, d = _c()
    d.arc((70, 30, 170, 130), 180, 90, fill=(250, 200, 60), width=26)
    d.line((120, 130, 120, 160), fill=(250, 200, 60), width=26)
    d.ellipse((105, 180, 135, 210), fill=(250, 200, 60))
    return im

def rope():
    im, d = _c()
    for r in (90, 70, 50, 30):
        d.ellipse((120 - r, 125 - r * 0.8, 120 + r, 125 + r * 0.8), outline=BROWN_L, width=14)
        d.ellipse((120 - r, 125 - r * 0.8, 120 + r, 125 + r * 0.8), outline=INK, width=3)
    return im

def bow():
    im, d = _c()
    d.arc((40, 25, 160, 215), 270, 90, fill=BROWN, width=12)
    d.line((100, 30, 100, 210), fill=INK, width=3)
    d.line((60, 120, 215, 120), fill=BROWN_L, width=7); d.polygon([(215, 108), (235, 120), (215, 132)], fill=GREY, outline=INK)
    return im

def baby():
    im, d = _c()
    d.rounded_rectangle((55, 100, 185, 210), radius=50, fill=(250, 245, 230), outline=INK, width=OW)
    d.ellipse((80, 40, 160, 120), fill=SKIN, outline=INK, width=OW)
    d.ellipse((102, 72, 110, 80), fill=INK); d.ellipse((130, 72, 138, 80), fill=INK)
    d.arc((108, 82, 132, 104), 20, 160, fill=INK, width=4)
    return im

def globe():
    im, d = _c()
    d.ellipse((30, 30, 210, 210), fill=BLUE, outline=INK, width=OW)
    d.polygon([(70, 70), (120, 60), (130, 110), (95, 150), (65, 120)], fill=GREEN)
    d.polygon([(140, 120), (180, 110), (185, 160), (150, 175)], fill=GREEN)
    d.arc((75, 30, 165, 210), 0, 360, fill=INK, width=3); d.line((30, 120, 210, 120), fill=INK, width=3)
    return im

def eagle():
    """a Roman eagle standard"""
    im, d = _c()
    d.line((120, 120, 120, 225), fill=BROWN, width=10)
    d.polygon([(120, 70), (30, 40), (60, 90), (40, 100), (100, 115), (120, 135), (140, 115), (200, 100), (180, 90), (210, 40)], fill=GOLD, outline=INK, width=OW)
    d.ellipse((104, 50, 136, 82), fill=GOLD, outline=INK, width=5)
    d.polygon([(132, 62), (150, 68), (132, 74)], fill=(240, 160, 40), outline=INK)
    return im

def treaty():
    """two hands: shown as a sealed treaty scroll with two seals"""
    im = scroll(); d = ImageDraw.Draw(im)
    d.ellipse((70, 140, 110, 180), fill=RED, outline=INK, width=4); d.ellipse((130, 140, 170, 180), fill=(60, 110, 180), outline=INK, width=4)
    return im

def flag():
    im, d = _c()
    d.line((60, 25, 60, 220), fill=BROWN, width=10)
    d.polygon([(64, 35), (200, 55), (170, 90), (200, 125), (64, 115)], fill=RED, outline=INK, width=OW)
    return im

def cobra():
    im, d = _c()
    d.line([(60, 210), (150, 200), (170, 160), (120, 130), (120, 90)], fill=(110, 150, 60), width=22, joint='curve')
    d.ellipse((80, 30, 160, 120), fill=(110, 150, 60), outline=INK, width=OW)
    d.ellipse((103, 55, 113, 65), fill=INK); d.ellipse((127, 55, 137, 65), fill=INK)
    d.line((120, 95, 120, 112), fill=RED, width=4)
    return im

def bread():
    im, d = _c()
    d.ellipse((30, 90, 210, 190), fill=(210, 150, 80), outline=INK, width=OW)
    for x in (80, 120, 160): d.arc((x - 20, 105, x + 20, 145), 200, 340, fill=(250, 220, 170), width=6)
    return im

def chain():
    im, d = _c()
    for k in range(4):
        x = 30 + k * 48
        d.rounded_rectangle((x, 95 + (k % 2) * 8, x + 64, 140 - (k % 2) * 8), radius=20, outline=GREY_D, width=12)
    return im

def palm():
    im, d = _c()
    d.line([(120, 220), (115, 150), (125, 80)], fill=BROWN, width=16, joint='curve')
    for a in (200, 240, 290, 330, 20):
        r = math.radians(a); d.line((125, 80, 125 + 85 * math.cos(r), 80 + 60 * math.sin(r) + 20), fill=GREEN, width=16)
    return im

def fire():
    im, d = _c()
    d.polygon([(120, 25), (175, 110), (180, 170), (120, 215), (60, 170), (70, 110), (95, 120)], fill=(240, 110, 40), outline=INK, width=OW)
    d.polygon([(120, 100), (150, 160), (120, 200), (90, 160)], fill=(250, 210, 70))
    return im

def skull():
    im, d = _c()
    d.ellipse((50, 35, 190, 165), fill=WHITE, outline=INK, width=OW)
    d.rounded_rectangle((85, 140, 155, 200), radius=12, fill=WHITE, outline=INK, width=OW)
    d.ellipse((75, 85, 112, 122), fill=INK); d.ellipse((128, 85, 165, 122), fill=INK)
    for x in (100, 120, 140): d.line((x, 170, x, 198), fill=INK, width=4)
    return im

def factory():
    im, d = _c()
    d.polygon([(30, 205), (30, 120), (80, 150), (80, 120), (130, 150), (130, 120), (180, 150), (210, 150), (210, 205)], fill=(180, 110, 90), outline=INK, width=OW)
    d.rectangle((175, 50, 200, 150), fill=GREY_D, outline=INK, width=5)
    for x, y, r in ((190, 35, 16), (210, 20, 12)): d.ellipse((x - r, y - r, x + r, y + r), fill=(210, 210, 215), outline=INK, width=3)
    return im

def bolt():
    im, d = _c()
    d.polygon([(140, 20), (60, 135), (115, 135), (95, 220), (180, 100), (125, 100)], fill=(250, 210, 60), outline=INK, width=OW)
    return im

ICON_FUNCS = {
    '📜': scroll, '🏛️': temple, 'PYR': pyramid, '👑': crown, '🌊': river, '🪙': coin, '𓂀': eye, '👁️': eye, '⚔️': swords,
    '🗓️': seasons, '📅': seasons, '🌾': wheat, '🗺️': map_, '⏳': hourglass, '✊': crowd, '⛵': boat, '🪨': stone, '📚': books,
    '⚱️': coffin, '💰': money, '⛪': church, '🌧️': rain, '🐎': chariot, '🏰': fort, '📊': chart, '☀️': sun, '⭐': star,
    '🧱': tablet, '🔒': lock, '🕯️': lamp, '✅': check, '❓': question, '🪢': rope, '🏹': bow, '👶': baby, '🌍': globe,
    '🦅': eagle, '🤝': treaty, '🚩': flag, '🐍': cobra, '🕌': mosque, '🍞': bread, '🍺': bread, '⛓️': chain, '🌴': palm,
    '🔥': fire, '☠️': skull, '💀': skull, '🏭': factory, '⚡': bolt, '🟫': river, '🌶️': money, '🐪': chariot, '💍': treaty,
    '🗡️': swords,
}

_cache = {}
def draw_icon(key, size):
    k = (key, size)
    if k not in _cache:
        f = ICON_FUNCS.get(key, question)
        im = f()
        bb = im.getbbox(); im = im.crop(bb) if bb else im
        r = size / max(im.size)
        _cache[k] = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
    return _cache[k]
