import math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = "../fonts/Fredoka.ttf"
RED = (232, 30, 45); RED_D = (190, 15, 30); RED_L = (255, 95, 105); WHITE = (255, 255, 255)

def font(size):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_name("Bold"); return f

def heart(d, cx, cy, s, fill):
    pts = []
    for i in range(200):
        t = 2 * math.pi * i / 200
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x * s, cy - y * s))
    d.polygon(pts, fill=fill)

def magnifier(d, cx, cy, r, w, fill):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=fill, width=w)
    a = math.radians(45)
    x0, y0 = cx + r * math.cos(a), cy + r * math.sin(a)
    d.line((x0, y0, x0 + r * 0.95, y0 + r * 0.95), fill=fill, width=int(w * 1.5))
    d.ellipse((x0 + r * 0.95 - w * .75, y0 + r * 0.95 - w * .75, x0 + r * 0.95 + w * .75, y0 + r * 0.95 + w * .75), fill=fill)

def logo(icon, out):
    S = 1800; im = Image.new("RGB", (S, S), RED); d = ImageDraw.Draw(im)
    f = font(325)
    for txt, x, y in (("MEANING", S / 2, 600), ("OF", 740, 900), ("FIND", 620, 1200)):
        d.text((x, y), txt, font=f, fill=WHITE, anchor="mm", stroke_width=8, stroke_fill=WHITE)
    if icon == "heart": heart(d, 1360, 980, 19, WHITE)
    else: magnifier(d, 1270, 930, 170, 64, WHITE)
    im.resize((800, 800), Image.LANCZOS).save(out, quality=95)

def banner(out):
    W, H = 2560, 1440
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.clip((xx / W) * 0.5 + (yy / H) * 0.5, 0, 1)[..., None]
    a = np.array(RED, np.float32) * (1 - g) + np.array((210, 20, 40), np.float32) * g
    im = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
    # soft background hearts / blobs
    deco = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(deco)
    heart(dd, 2330, 560, 26, (255, 255, 255, 40))
    dd.ellipse((-250, 820, 450, 1500), fill=(255, 255, 255, 30))
    heart(dd, 690, 760, 3.6, (255, 180, 185, 170))
    heart(dd, 1880, 700, 3.6, (255, 180, 185, 170))
    im.alpha_composite(deco.filter(ImageFilter.GaussianBlur(3)))
    # glow layer for title
    cx = W // 2
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    f = font(150)
    gd.text((cx, 560), "ROAD TO 100K", font=f, fill=(255, 255, 255, 160), anchor="mm")
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(18)))
    d = ImageDraw.Draw(im)
    d.text((cx, 560), "ROAD TO 100K", font=f, fill=WHITE, anchor="mm")
    # burst lines
    for side in (-1, 1):
        bx = cx + side * 560
        for ang, ln in ((-30, 60), (0, 50), (30, 60)):
            a_ = math.radians(ang)
            x1 = bx + side * 10; y1 = 560 + math.sin(a_) * 60
            x2 = x1 + side * ln * math.cos(a_); y2 = y1 + ln * math.sin(a_)
            d.line((x1, y1, x2, y2), fill=WHITE, width=14)
            d.ellipse((x1 - 7, y1 - 7, x1 + 7, y1 + 7), fill=WHITE); d.ellipse((x2 - 7, y2 - 7, x2 + 7, y2 + 7), fill=WHITE)
    # progress bar
    bx0, bx1, by0, by1 = cx - 380, cx + 380, 660, 740
    d.rounded_rectangle((bx0, by0, bx1, by1), radius=40, fill=RED_D, outline=WHITE, width=10)
    d.rounded_rectangle((bx0 + 16, by0 + 16, bx0 + 16 + int((bx1 - bx0 - 32) * 0.58), by1 - 16), radius=24, fill=(255, 150, 155))
    # youtube icon | 100.000
    yx, yy0 = cx - 260, 790
    d.rounded_rectangle((yx, yy0, yx + 130, yy0 + 92), radius=26, fill=WHITE)
    d.polygon([(yx + 50, yy0 + 24), (yx + 50, yy0 + 68), (yx + 90, yy0 + 46)], fill=RED)
    d.line((yx + 170, yy0 + 6, yx + 170, yy0 + 86), fill=WHITE, width=6)
    d.text((yx + 200, yy0 + 46), "100.000", font=font(110), fill=WHITE, anchor="lm")
    im.convert("RGB").save(out, quality=95)

logo("heart", "out/logo_heart.jpg")
logo("magnifier", "out/logo_magnifier.jpg")
banner("out/banner.jpg")
