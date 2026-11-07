"""Thumbnails in the layout of the user's reference (Unknown Itihaas, '1947 की आज़ादी'):
full-bleed refugee-train photo, huge distressed two-colour headline on top, black strip with yellow text at the bottom.
Built from public-domain photos only (no bodies), colour-graded warm. Writes ../thumbnails/ref_*.jpg"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'thumbnails')
W, H = 1280, 720
F = os.path.join(HERE, 'assets', 'fonts', 'Mukta-ExtraBold.ttf')
def font(sz): return ImageFont.truetype(F, sz, layout_engine=ImageFont.Layout.RAQM)
YEL = (255, 196, 20); CREAM = (250, 245, 232)

def photo(name, crop_frac, fx=0.5, fy=0.5):
    p = os.path.join(HERE, 'assets', 'photos_hd', name + '.jpg')
    if not os.path.exists(p): p = os.path.join(HERE, 'assets', 'photos', name + '.jpg')
    im = Image.open(p).convert('RGB')
    l, t, r, b = crop_frac; im = im.crop((int(l * im.width), int(t * im.height), int(r * im.width), int(b * im.height)))
    k = max(W / im.width, H / im.height); im = im.resize((int(im.width * k) + 1, int(im.height * k) + 1), Image.LANCZOS)
    x = int((im.width - W) * fx); y = int((im.height - H) * fy)
    return im.crop((x, y, x + W, y + H))

def grade(im):
    """warm 'dusty 1947' colour grade of a black-and-white photo, with a hazy orange sky at the top"""
    g = np.asarray(ImageEnhance.Contrast(im.convert('L')).enhance(1.35), np.float32) / 255
    stops = np.array([[18, 12, 10], [92, 52, 28], [178, 112, 58], [236, 196, 140], [252, 240, 214]], np.float32)
    pos = g * (len(stops) - 1); i = np.clip(pos.astype(int), 0, len(stops) - 2); f = (pos - i)[..., None]
    rgb = stops[i] * (1 - f) + stops[i + 1] * f
    yy = np.linspace(0, 1, H)[:, None, None]
    haze = np.clip(1 - yy / 0.45, 0, 1) ** 1.5 * 0.35
    rgb = rgb * (1 - haze) + np.array([230, 170, 110], np.float32) * haze
    out = Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).filter(ImageFilter.UnsharpMask(2, 90, 2))
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    v = (1 - 0.45 * np.clip(np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2) - 0.6, 0, 1)).clip(0.5, 1)
    return Image.fromarray((np.asarray(out, np.float32) * v[..., None]).clip(0, 255).astype(np.uint8)).convert('RGBA')

def distressed(size, rng):
    """speckled 'worn print' alpha texture like the reference headline"""
    n = rng.random((size[1] // 3 + 1, size[0] // 3 + 1))
    n = Image.fromarray(((n > 0.12) * 255).astype(np.uint8)).resize(size, Image.NEAREST).filter(ImageFilter.GaussianBlur(0.6))
    return n

def headline(im, parts, y, size, rng):
    """parts = [(text, colour), ...] drawn on one centred line with a thick black outline and soft shadow"""
    f = font(size); sp = int(size * 0.25)
    widths = [f.getlength(t) for t, _ in parts]; total = sum(widths) + sp * (len(parts) - 1)
    x = (W - total) / 2
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    for (t, col), w in zip(parts, widths):
        ds.text((x + 8, y + 10), t, font=f, fill=(0, 0, 0, 230), anchor='ls', stroke_width=14, stroke_fill=(0, 0, 0, 230))
        d.text((x, y), t, font=f, fill=col + (255,), anchor='ls', stroke_width=11, stroke_fill=(12, 10, 8, 255))
        x += w + sp
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
    a = np.asarray(layer.getchannel('A'), np.float32) * (np.asarray(distressed((W, H), rng), np.float32) / 255 * 0.22 + 0.78)
    layer.putalpha(Image.fromarray(a.astype(np.uint8))); im.alpha_composite(layer)

def strip(im, text, size=64):
    f = font(size); w = f.getlength(text); pad = 26
    x0 = int((W - w) / 2 - pad); x1 = int((W + w) / 2 + pad); y1 = H - 14; y0 = y1 - int(size * 1.45)
    bar = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(bar).rectangle([x0, y0, x1, y1], fill=(8, 8, 8, 235))
    im.alpha_composite(bar)
    ImageDraw.Draw(im).text((W / 2, (y0 + y1) / 2 + 4), text, font=f, fill=YEL, anchor='mm')

def save(im, name):
    im.convert('RGB').save(os.path.join(OUT, name), quality=95); print('wrote', name)

rng = np.random.default_rng(7)
# 1: the locomotive packed with refugees (wire caption on the right edge cropped off)
im = grade(photo('to_pakistan', (0.03, 0.03, 0.9, 0.97), fx=0.35, fy=0.75))
headline(im, [('1947 का', CREAM), ('बँटवारा', YEL)], 178, 168, rng)
strip(im, 'एक लकीर, डेढ़ करोड़ बेघर')
save(im, 'ref_1_train_1947_ka_batwara.jpg')
# 2: refugee train with families
im = grade(photo('refugee_train2', (0, 0, 1, 1), fx=0.5, fy=0.6))
headline(im, [('1947 की', CREAM), ('आज़ादी', YEL)], 178, 168, rng)
strip(im, 'आज़ादी का जश्न, बँटवारे का दर्द')
save(im, 'ref_2_train_1947_ki_azadi.jpg')
