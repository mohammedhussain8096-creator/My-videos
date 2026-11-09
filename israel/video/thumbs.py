"""YouTube thumbnails for the Israel video (1280x720), drawn with the video's own map engine."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import render as R, icons
from render_text import text_img
OUT = os.path.join(HERE, '..', '..', 'thumbnails')
W, H = R.W, R.H
R.FILL_K = 0.85

def base(view, fills, dark=0.0):
    cam = R.view_of(view)
    fr = R.crop_map(*cam).convert('RGB')
    fr = ImageEnhance.Contrast(ImageEnhance.Color(fr).enhance(1.25)).enhance(1.12)
    fr = R.draw_fills(fr, cam, [f + (None, 0.6) if len(f) == 3 else f for f in fills])
    if dark:
        a = np.asarray(fr).astype(np.float32); x = np.linspace(0, 1, W)[None, :, None]
        a *= 1 - dark * np.clip(1.25 - x * 1.9, 0, 1)        # darken the left side behind the text
        fr = Image.fromarray(a.astype(np.uint8))
    v = R.vignette() if hasattr(R, 'vignette') else None
    fr = fr.convert('RGBA')
    if v is not None:
        try: fr.alpha_composite(v.convert('RGBA'))
        except Exception: pass
    return fr, cam

def T(fr, txt, x, y, size, col='yellow', font='luckiest', anchor='l', rot=0):
    c = R.BIGCOL[col]
    im = text_img(txt, font, size, None, c[2], max(8, size // 11), gradient=(c[0], c[1]))
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    xx = x - (im.width / 2 if anchor == 'c' else im.width if anchor == 'r' else 0)
    fr.alpha_composite(im, (int(xx), int(y - im.height / 2)))

def P(fr, im, x, y, k=1.0):
    if k != 1: im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    fr.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))

def ring(fr, cam, latlon, r, col=(255, 230, 60), w=12):
    x, y = R.to_screen(latlon, cam)
    lay = Image.new('RGBA', fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse([x - r, y - r, x + r, y + r], outline=col + (255,), width=w)
    g = lay.filter(ImageFilter.GaussianBlur(10)); fr.alpha_composite(g); fr.alpha_composite(lay)

def save(fr, name):
    os.makedirs(OUT, exist_ok=True)
    im = fr.convert('RGB').resize((1280, 720), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 50, 2))
    p = os.path.join(OUT, name); im.save(p, quality=95); print(p, os.path.getsize(p) // 1024, 'KB')

def photo(name, h, tilt=0):
    im = Image.open(os.path.join(HERE, 'assets', 'photos', name)).convert('RGB')
    k = h / im.height; im = im.resize((int(im.width * k), h), Image.LANCZOS)
    b = 14; card = Image.new('RGBA', (im.width + 2 * b, im.height + 2 * b), (250, 248, 240, 255)); card.paste(im, (b, b))
    sh = Image.new('RGBA', (card.width + 60, card.height + 60), (0, 0, 0, 0))
    sh.paste((0, 0, 0, 150), (30, 38, 30 + card.width, 38 + card.height)); sh = sh.filter(ImageFilter.GaussianBlur(14))
    sh.alpha_composite(card, (30, 30))
    return sh.rotate(tilt, Image.BICUBIC, expand=True)


def pm_corner(fr, h=860):
    """White House photo (public domain), cut out; dark moody grade + red rim light, face not altered."""
    im = Image.open(os.path.join(HERE, 'assets', 'photos', 'netanyahu_cut.png')).convert('RGBA').crop((70, 100, 540, 720))
    k = h / im.height; im = im.resize((int(im.width * k), h), Image.LANCZOS)
    rgb = ImageEnhance.Contrast(ImageEnhance.Brightness(im.convert('RGB')).enhance(0.72)).enhance(1.35)
    a = np.asarray(rgb).astype(np.float32)
    yy = np.linspace(0, 1, im.height)[:, None, None]; xx = np.linspace(0, 1, im.width)[None, :, None]
    a *= np.clip(1.0 - 0.6 * yy - 0.9 * np.clip(0.5 - xx, 0, 1) ** 1.2, 0.22, 1)       # light from the top, falls off below
    a[..., 0] *= 1.04; a[..., 2] *= 0.92
    body = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA'); body.putalpha(im.getchannel('A'))
    ramp = Image.fromarray((np.clip((np.arange(im.width) - 0.05 * im.width) / (0.09 * im.width), 0, 1) * 255).astype(np.uint8)[None, :].repeat(im.height, 0))
    al = ImageChops.multiply(im.getchannel('A'), ramp); body.putalpha(al)
    rim = Image.new('RGBA', im.size, (255, 50, 30, 0)); rim.putalpha(al.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(14)))
    x, y = W - im.width + 30, H - im.height + 20
    # dark smoky backdrop in the corner
    yy2, xx2 = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx2 - (x + im.width * 0.55)) / (im.width * 0.95)) ** 2 + ((yy2 - (y + im.height * 0.45)) / (im.height * 0.85)) ** 2)
    dk = np.zeros((H, W, 4), np.uint8); dk[..., :3] = (18, 6, 4); dk[..., 3] = (np.clip(1.2 - d, 0, 1) ** 0.7 * 245).astype(np.uint8)
    fr.alpha_composite(Image.fromarray(dk, 'RGBA'))
    sh = Image.new('RGBA', fr.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 255), (x - 20, y), al)
    sh = sh.filter(ImageFilter.GaussianBlur(40)); fr.alpha_composite(sh)
    fr.alpha_composite(rim, (x, y)); fr.alpha_composite(rim, (x, y)); fr.alpha_composite(body, (x, y))
    # bottom fade so he sits into the frame
    g = np.zeros((H, W, 4), np.uint8); g[..., 3] = (np.clip((np.arange(H) - (H - 140)) / 140, 0, 1) * 170).astype(np.uint8)[:, None]
    fr.alpha_composite(Image.fromarray(g, 'RGBA'))

# 1. ONE LAND, TWO PEOPLES
fr, cam = base((31.55, 34.45, 7.4), [('GREEN_LINE', 'blue', 1.0), ('WEST_BANK', 'green', 1.0), ('GAZA', 'green', 1.0)], dark=0.55)
T(fr, 'ONE LAND', 70, 300, 190, 'white')
T(fr, 'TWO PEOPLES', 70, 520, 170, 'yellow')
T(fr, '3,000 years of history', 80, 720, 74, 'white', 'fredoka')
P(fr, icons.get('flag-il', 190), 230, 900)
P(fr, icons.get('flag-ps', 190), 610, 900)
pm_corner(fr)
save(fr, 'Israel_Thumb1.jpg')

# 2. 3,000 YEARS IN 30 MINUTES
fr, cam = base((31.0, 31.0, 30), [('MANDATE', 'red', 1.0)], dark=0.5)
ring(fr, cam, (31.6, 35.0), 150)
T(fr, '3,000', 70, 300, 290, 'yellow')
T(fr, 'YEARS', 90, 545, 170, 'white')
T(fr, 'IN 30 MINUTES', 80, 760, 120, 'red')
P(fr, photo('herzl.jpg', 300, -6), 1600, 300)
save(fr, 'Israel_Thumb2.jpg')

# 3. 1947: the map that changed everything
fr, cam = base((31.45, 33.8, 7.0), [('UN_JEWISH', 'blue', 1.0), ('UN_ARAB', 'green', 1.0), ('UN_JERUSALEM', 'white', 1.0)], dark=0.6)
T(fr, '1947', 70, 230, 250, 'red')
T(fr, 'THE MAP THAT', 75, 470, 120, 'white')
T(fr, 'CHANGED', 75, 620, 150, 'yellow')
T(fr, 'EVERYTHING', 75, 790, 150, 'yellow')
P(fr, icons.get('flag-un', 150), 760, 235)
save(fr, 'Israel_Thumb3.jpg')

# 4. reference style: big bold title boxes, red glowing land, big PM bust with one glowing red eye (stylised effect)
from PIL import ImageFont
INTER = os.path.join(HERE, '..', '..', 'chernobyl', 'video', 'assets', 'fonts', 'Inter-ExtraBold.ttf')

def boxed(fr, txt, x, y, size, pad=(34, 18)):
    f = ImageFont.truetype(INTER, size); l, t, r, b = f.getbbox(txt)
    w, h = r - l + 2 * pad[0], b - t + 2 * pad[1]
    d = ImageDraw.Draw(fr); d.rectangle([x, y, x + w, y + h], fill=(8, 8, 10, 255))
    d.text((x + pad[0] - l, y + pad[1] - t), txt, font=f, fill=(255, 255, 255, 255))
    return y + h

def outline(fr, cam, name, col=(255, 255, 255), w=4):
    lay = Image.new('RGBA', fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for r in R.proj_rings(name):
        x, y = R.to_screen_arr(r, cam)
        if len(x) > 3: d.line(list(zip(x.tolist(), y.tolist())) + [(x[0], y[0])], fill=col + (255,), width=w, joint='curve')
    fr.alpha_composite(lay)

def pm_big(fr, eye=True):
    im = Image.open(os.path.join(HERE, 'assets', 'photos', 'netanyahu_xl.png')).convert('RGBA').crop((110, 200, 1000, 1150))
    k = 1060 / im.height; im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    x, y = W - im.width + 60, H - im.height + 20
    ex, ey = (355 - 110) * k + x, (467 - 200) * k + y                       # his right eye (viewer's left)
    rgb = ImageEnhance.Contrast(ImageEnhance.Color(im.convert('RGB')).enhance(1.1)).enhance(1.12)
    a = np.asarray(rgb).astype(np.float32)
    yy, xx = np.mgrid[0:im.height, 0:im.width].astype(np.float32)
    dd = np.sqrt((xx - (ex - x)) ** 2 + (yy - (ey - y)) ** 2)
    red = np.clip(1 - dd / (260 * k / 0.9), 0, 1)[..., None] ** 1.5       # red light spilling from the eye onto the face
    a = a * (1 - 0.45 * red) + np.array([255, 40, 25], np.float32) * 0.45 * red
    a *= np.clip(1.08 - 0.35 * (yy / im.height) ** 1.5, 0, 1)[..., None]
    body = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA'); body.putalpha(im.getchannel('A'))
    al = im.getchannel('A')
    sh = Image.new('RGBA', fr.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 255), (x - 30, y + 10), al)
    fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(30)))
    rim = Image.new('RGBA', im.size, (255, 60, 40, 0)); rim.putalpha(al.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(10)).point(lambda v: v * 0.8))
    fr.alpha_composite(rim, (x, y)); fr.alpha_composite(body, (x, y))
    if eye:
        g = np.zeros((H, W, 4), np.float32); Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
        d2 = np.sqrt((X - ex) ** 2 + ((Y - ey) * 1.5) ** 2)
        core = np.clip(1 - d2 / 13, 0, 1); halo = np.exp(-(d2 / 30) ** 2); wide = np.exp(-(d2 / 90) ** 2) * 0.45
        streak = np.exp(-((Y - ey) / 3) ** 2) * np.exp(-(np.abs(X - ex) / 60)) * 0.7
        amt = np.clip(halo + wide + streak, 0, 1)
        g[..., 0] = 255; g[..., 1] = 30 + 225 * core; g[..., 2] = 20 + 235 * core; g[..., 3] = np.clip(amt + core, 0, 1) * 255
        fr.alpha_composite(Image.fromarray(g.astype(np.uint8), 'RGBA'))

R.FILL_K = 0.95
fr, cam = base((31.1, 36.2, 11.5), [('MANDATE', 'red', 1.0)], dark=0.0)
fr = ImageEnhance.Contrast(ImageEnhance.Color(fr.convert('RGB')).enhance(0.92)).enhance(1.08).convert('RGBA')
for n in ('GREEN_LINE', 'WEST_BANK', 'GAZA'): outline(fr, cam, n, (255, 255, 255), 4)
pm_big(fr)
yb = boxed(fr, 'ISRAEL', 50, 40, 170)
boxed(fr, '1000 BCE - TODAY', 50, yb + 22, 74)
save(fr, 'Israel_Thumb4.jpg')
