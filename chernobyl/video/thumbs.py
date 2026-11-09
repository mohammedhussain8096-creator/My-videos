"""YouTube thumbnails for the Chernobyl video (1280x720), built from the video's own 3D frame and its CC0/PD photos."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, 'assets')
OUT = os.path.join(HERE, '..', '..', 'thumbnails')
W, H = 1920, 1080
RED, AMBER, WHITE, TOX = (255, 60, 40), (255, 184, 40), (250, 250, 245), (190, 240, 70)

def F(name, size): return ImageFont.truetype(os.path.join(A, 'fonts', name), size)

def text(fr, txt, x, y, font, size, col, anchor='l', stroke=None, glow=0, track=0):
    f = F(font, size); sw = stroke if stroke is not None else max(6, size // 14)
    l, t, r, b = f.getbbox(txt, stroke_width=sw)
    w, h = r - l + 2 * sw + 60, b - t + 2 * sw + 60
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((30 - l + sw, 30 - t + sw), txt, font=f, fill=col + (255,), stroke_width=sw, stroke_fill=(12, 8, 6, 255))
    xx = x - (w / 2 if anchor == 'c' else w if anchor == 'r' else 0) - 30
    yy = y - h / 2
    sh = Image.new('RGBA', (w, h), (0, 0, 0, 0)); sh.paste((0, 0, 0, 200), (0, 0), lay.getchannel('A'))
    fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)), (int(xx + 6), int(yy + 10)))
    if glow:
        g = Image.new('RGBA', (w, h), (0, 0, 0, 0)); g.paste(col + (255,), (0, 0), lay.getchannel('A'))
        g = g.filter(ImageFilter.GaussianBlur(glow)); g.putalpha(g.getchannel('A').point(lambda v: min(255, int(v * 1.6))))
        fr.alpha_composite(g, (int(xx), int(yy)))
    fr.alpha_composite(lay, (int(xx), int(yy)))

def cover(im, fx=0.5, fy=0.5, zoom=1.0):
    k = max(W / im.width, H / im.height) * zoom
    im = im.resize((int(im.width * k + 0.5), int(im.height * k + 0.5)), Image.LANCZOS)
    x = int(np.clip(fx * im.width - W / 2, 0, im.width - W)); y = int(np.clip(fy * im.height - H / 2, 0, im.height - H))
    return im.crop((x, y, x + W, y + H))

def shade(fr, side='l', k=0.75):
    a = np.asarray(fr).astype(np.float32)
    x = np.linspace(0, 1, W)[None, :, None]; y = np.linspace(-1, 1, H)[:, None, None]
    ramp = np.clip((0.75 - x) / 0.6, 0, 1) if side == 'l' else np.clip((x - 0.25) / 0.6, 0, 1) if side == 'r' else 0 * x
    vig = np.clip(((x - 0.5) * 2) ** 2 * 0.35 + y ** 2 * 0.35, 0, 1)
    a *= (1 - k * ramp) * (1 - 0.55 * vig)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')

def grade(im, warm=(1.0, 1.0, 1.0), sat=1.0, con=1.0, bri=1.0):
    im = ImageEnhance.Brightness(ImageEnhance.Contrast(ImageEnhance.Color(im.convert('RGB')).enhance(sat)).enhance(con)).enhance(bri)
    a = np.asarray(im).astype(np.float32) * np.array(warm, np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def ring(fr, x, y, r, col=RED, w=12):
    lay = Image.new('RGBA', fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse([x - r, y - r * 0.8, x + r, y + r * 0.8], outline=col + (255,), width=w)
    fr.alpha_composite(lay.filter(ImageFilter.GaussianBlur(10))); fr.alpha_composite(lay)

def arrow(fr, x0, y0, x1, y1, col=RED, w=22):
    lay = Image.new('RGBA', fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    v = np.array([x1 - x0, y1 - y0], float); L = np.linalg.norm(v); u = v / L; n = np.array([-u[1], u[0]])
    tip = np.array([x1, y1]); base = tip - u * 70
    d.line([(x0, y0), tuple(base)], fill=col + (255,), width=w)
    d.polygon([tuple(tip), tuple(base + n * 45), tuple(base - n * 45)], fill=col + (255,))
    sh = Image.new('RGBA', fr.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 220), (0, 0), lay.getchannel('A'))
    fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (0, 0)); fr.alpha_composite(lay)

def save(fr, name):
    os.makedirs(OUT, exist_ok=True)
    im = fr.convert('RGB').resize((1280, 720), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 45, 2))
    p = os.path.join(OUT, name); im.save(p, quality=95); print(p, os.path.getsize(p) // 1024, 'KB')

# 1. the explosion (the video's own 3D animation), with the time it happened
full = Image.open(os.path.join(HERE, 'build', 'expl_162.5.png')).convert('RGB')
bg = full.crop((1500, 0, 1920, 1080)).resize((W, H)).filter(ImageFilter.GaussianBlur(40))   # the scene's own dark backdrop
top = full.crop((0, 0, 1920, 905))                                          # everything above the subtitle line
m = Image.new('L', top.size, 255); dm = ImageDraw.Draw(m)
for i in range(220): dm.line([(0, 905 - 220 + i), (1920, 905 - 220 + i)], fill=int(255 * (1 - i / 220) ** 1.4))
for i in range(160): dm.line([(1920 - 160 + i, 0), (1920 - 160 + i, 905)], fill=0)
bg.paste(top, (-330, 30), m)
fr = shade(grade(bg, (1.08, 1.0, 0.92), 1.2, 1.12, 1.08), 'n', 0.0)
text(fr, '01:23:04', 1870, 250, 'BebasNeue.ttf', 290, RED, 'r', glow=28)
text(fr, 'THE NIGHT', 1880, 520, 'BebasNeue.ttf', 200, WHITE, 'r')
text(fr, 'IT EXPLODED', 1880, 720, 'BebasNeue.ttf', 200, AMBER, 'r')
save(fr, 'Chernobyl_Thumb1.jpg')

# 2. Pripyat's Ferris wheel: the city nobody warned
src = Image.open(os.path.join(A, 'photos_hd', 'pd_amuse.jpg'))
fr = shade(grade(cover(src, 0.72, 0.45, 1.12), (1.04, 1.0, 0.9), 0.8, 1.15, 0.95), 'l', 0.8)
text(fr, 'NOBODY', 60, 230, 'BebasNeue.ttf', 230, WHITE)
text(fr, 'TOLD THEM', 60, 450, 'BebasNeue.ttf', 230, AMBER)
text(fr, 'FOR 36 HOURS', 64, 680, 'BebasNeue.ttf', 170, RED, glow=20)
save(fr, 'Chernobyl_Thumb2.jpg')

# 3. AZ-5: the safety button
src = Image.open(os.path.join(A, 'photos', 'cc0_30.jpg'))
fr = shade(grade(cover(src, 0.32, 0.33, 1.25), (1.1, 0.98, 0.85), 0.7, 1.2, 0.95), 'r', 0.55)
text(fr, 'AZ-5', 1870, 270, 'BebasNeue.ttf', 340, RED, 'r', glow=30)
text(fr, 'THE SAFETY BUTTON', 1870, 560, 'BebasNeue.ttf', 150, WHITE, 'r')
text(fr, 'THAT BLEW IT UP', 1870, 730, 'BebasNeue.ttf', 150, AMBER, 'r')
save(fr, 'Chernobyl_Thumb3.jpg')

# 4. stronger: Pripyat at dusk, the wrecked reactor glowing on the horizon, 36-hour hook
def trefoil(size, col=(255, 210, 40)):
    im = Image.new('RGBA', (size * 2, size * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = size; r = size * 0.95
    d.ellipse([c - r, c - r, c + r, c + r], fill=col + (255,), outline=(15, 10, 5, 255), width=size // 12)
    for a0 in (-90 - 30, 30 - 30, 150 - 30):
        d.pieslice([c - r * 0.8, c - r * 0.8, c + r * 0.8, c + r * 0.8], a0, a0 + 60, fill=(15, 10, 5, 255))
    d.ellipse([c - r * 0.3, c - r * 0.3, c + r * 0.3, c + r * 0.3], fill=col + (255,))
    d.ellipse([c - r * 0.2, c - r * 0.2, c + r * 0.2, c + r * 0.2], fill=(15, 10, 5, 255))
    return im.resize((size, size), Image.LANCZOS)

src = Image.open(os.path.join(A, 'photos_hd', 'pd_view.jpg')).convert('RGB')
Z = 1.55; px, py = 1060, 610                                    # the sarcophagus in the photo
win_w, win_h = W / Z, H / Z; x0, y0 = px - win_w * 0.62, py - win_h * 0.52
img = src.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + win_w, y0 + win_h))
ppx, ppy = (px - x0) * Z, (py - y0) * Z
a = np.asarray(img).astype(np.float32) / 255
lum = a.mean(axis=2, keepdims=True)
Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
sky = np.clip((ppy + 40 - Y) / ppy, 0, 1)[..., None]           # 1 at the top, 0 at the horizon
dusk = np.array([0.55, 0.12, 0.06]) * (0.35 + 0.9 * lum)        # blood-red dusk sky
ground = a * np.array([0.62, 0.58, 0.55]) * 0.85
a = ground * (1 - sky) + dusk * sky
dist = np.sqrt(((X - ppx) / 1.0) ** 2 + ((Y - ppy) * 1.6) ** 2)
glow = np.exp(-(dist / 260) ** 2)[..., None]; core = np.exp(-(dist / 60) ** 2)[..., None]
col = np.exp(-((X - ppx) / 70) ** 2)[..., None] * np.clip((ppy - Y) / ppy, 0, 1)[..., None] * 0.8   # light column rising
a = a + glow * np.array([1.0, 0.45, 0.08]) * 0.85 + core * np.array([1.0, 0.85, 0.5]) * 0.9 + col * np.array([1.0, 0.5, 0.1]) * 0.45
vig = np.clip(((X / W - 0.5) * 2) ** 2 * 0.4 + ((Y / H - 0.5) * 2) ** 2 * 0.4, 0, 1)[..., None]
a *= 1 - 0.6 * vig
fr = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert('RGBA')
fr = Image.fromarray(np.asarray(fr)).filter(ImageFilter.UnsharpMask(2, 40, 3))
ring(fr, ppx, ppy - 10, 150, RED, 14)
arrow(fr, ppx - 300, ppy - 160, ppx - 160, ppy - 60, RED, 24)
text(fr, '36 HOURS', 60, 190, 'BebasNeue.ttf', 300, RED, glow=30)
text(fr, 'NOBODY TOLD THEM', 66, 400, 'BebasNeue.ttf', 130, WHITE)
fr.alpha_composite(trefoil(220), (W - 290, 60))
save(fr, 'Chernobyl_Thumb4.jpg')
