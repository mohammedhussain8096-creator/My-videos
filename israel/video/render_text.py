import os
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.environ.get('RU_ASSETS', os.path.join(HERE, 'assets'))

@lru_cache(maxsize=64)
def font(name, size):
    return ImageFont.truetype(os.path.join(ASSETS, name + '.ttf'), int(size))

@lru_cache(maxsize=512)
def text_img(text, fname, size, fill, stroke, sw, gradient=None, shadow=True):
    """Text with outline + soft drop shadow. gradient=(top, bottom) colours overrides fill."""
    f = font(fname, size)
    pad = sw + 12
    l, t, r, b = f.getbbox(text, stroke_width=sw)
    w, h = r - l + 2 * pad, b - t + 2 * pad
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    xy = (pad - l, pad - t)
    if gradient:
        d.text(xy, text, font=f, fill=stroke, stroke_width=sw, stroke_fill=stroke)
        m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).text(xy, text, font=f, fill=255)
        g = np.zeros((h, w, 4), np.uint8)
        top, bot = np.array(gradient[0], float), np.array(gradient[1], float)
        y0, y1 = pad, h - pad
        k = np.clip((np.arange(h) - y0) / max(1, y1 - y0), 0, 1)[:, None]
        g[..., :3] = (top * (1 - k) + bot * k)[:, None, :].repeat(w, 1).astype(np.uint8).transpose(0, 1, 2)
        g[..., 3] = 255
        im.paste(Image.fromarray(g, 'RGBA'), (0, 0), m)
    else:
        d.text(xy, text, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke)
    if shadow:
        sh = Image.new('RGBA', (w + 8, h + 10), (0, 0, 0, 0))
        a = im.getchannel('A').point(lambda v: v * 0.55)
        sh.paste((0, 0, 0, 255), (4, 8), a)
        sh = sh.filter(ImageFilter.GaussianBlur(4))
        sh.alpha_composite(im, (0, 0))
        im = sh
    return im
