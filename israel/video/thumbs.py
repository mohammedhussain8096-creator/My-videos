"""YouTube thumbnails for the Israel video (1280x720), drawn with the video's own map engine."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
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

# 1. ONE LAND, TWO PEOPLES
fr, cam = base((31.55, 33.75, 7.4), [('GREEN_LINE', 'blue', 1.0), ('WEST_BANK', 'green', 1.0), ('GAZA', 'green', 1.0)], dark=0.55)
T(fr, 'ONE LAND', 70, 300, 190, 'white')
T(fr, 'TWO PEOPLES', 70, 520, 170, 'yellow')
T(fr, '3,000 years of history', 80, 720, 74, 'white', 'fredoka')
P(fr, icons.get('flag-il', 190), 230, 900)
P(fr, icons.get('flag-ps', 190), 610, 900)
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
