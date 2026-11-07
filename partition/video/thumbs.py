"""YouTube thumbnails (1280x720) for the Hindi Partition video. Writes ../thumbnails/*.jpg"""
import os, sys
os.environ.setdefault('RES', '1280x720')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from render import W, H, font
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'thumbnails'); os.makedirs(OUT, exist_ok=True)
CUT = os.path.join(HERE, 'assets', 'cut')

def split_map(view, line_glow=True, bright=1.0):
    sp = dict(view=view, fill=[('india', 'india', None), ('wpak', 'pak', None), ('epak', 'pak', None)], line=(0, 0.01))
    im = R.draw_map(sp, 5.0, 5.0)
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.35)).enhance(1.15)
    im = ImageEnhance.Brightness(im).enhance(bright).convert('RGBA')
    if line_glow:                                     # glowing red Radcliffe line on top
        cx, cy, w = R.view_box(view); h = w * H / W; box = (cx - w / 2, cy - h / 2); s = W / w
        paths = [[((x - box[0]) * s, (y - box[1]) * s) for x, y in path] for path in R.border_paths()]
        def mask(width, blur):
            m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
            for pts in paths: d.line(pts, fill=255, width=width, joint='curve')
            return m.filter(ImageFilter.GaussianBlur(blur)) if blur else m
        for width, blur, col, k in ((44, 26, (255, 30, 10), 1.0), (20, 8, (255, 60, 20), 1.0), (10, 0, (230, 20, 10), 1.0), (4, 0, (255, 235, 210), 1.0)):
            layer = Image.new('RGBA', (W, H), col + (0,)); layer.putalpha(mask(width, blur).point(lambda v: int(v * k)))
            im.alpha_composite(layer)
    return im

def vignette(im, k=0.55):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    v = (1 - k * np.clip(r - 0.45, 0, 1) ** 1.3).clip(0.25, 1)[..., None]
    a = np.asarray(im.convert('RGB'), np.float32) * v
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')

def person(im, name, h, x, y_bottom, halo=(255, 255, 255), flip=False, warm=True):
    p = Image.open(os.path.join(CUT, name + '.png')).convert('RGBA')
    if flip: p = p.transpose(Image.FLIP_LEFT_RIGHT)
    k = h / p.height; p = p.resize((int(p.width * k), h), Image.LANCZOS)
    rgb = ImageEnhance.Contrast(p.convert('RGB')).enhance(1.25)
    if warm:
        g = np.asarray(rgb.convert('L'), np.float32)
        rgb = Image.fromarray(np.stack([g * 1.06 + 8, g * 0.98 + 4, g * 0.86], -1).clip(0, 255).astype(np.uint8))
    rgb = rgb.filter(ImageFilter.UnsharpMask(2, 80, 2)); rgb.putalpha(p.getchannel('A')); p = rgb
    hl = Image.new('RGBA', p.size, halo + (0,)); hl.putalpha(p.getchannel('A').filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.8)))
    im.alpha_composite(hl, (int(x), int(y_bottom - h))); im.alpha_composite(p, (int(x), int(y_bottom - h)))

def text(im, s, size, xy, fill=(255, 255, 255), stroke=10, kind='bold', anchor='mm', shadow=True):
    f = font(kind, size / R.U)
    d = ImageDraw.Draw(im)
    if shadow:
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((xy[0] + 6, xy[1] + 8), s, font=f, fill=(0, 0, 0, 200), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, 200))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(10, 10, 10))

def box(im, s, size, x, y, bg=(200, 25, 25), fg=(255, 255, 255), center=False):
    f = font('bold', size / R.U); l, t, r, b = f.getbbox(s); pad = int(size * 0.28)
    w, h = (r - l) + 2 * pad, (b - t) + 2 * pad
    if center: x = x - w // 2
    d = ImageDraw.Draw(im); d.rectangle([x, y, x + w, y + h], fill=bg)
    d.text((x + pad - l, y + pad - t), s, font=f, fill=fg)
    return y + h

def save(im, name):
    im.convert('RGB').save(os.path.join(OUT, name), quality=95); print('wrote', name)

# 1. Face-off: Jinnah vs Nehru over the split map
im = vignette(split_map((30.6, 74.4, 9.0), bright=0.9), 0.6)      # Punjab: the line runs down the middle
person(im, 'jinnah', 560, -30, H + 10, halo=(120, 255, 150))
person(im, 'nehru', 600, W - 430, H + 10, halo=(255, 190, 90))
text(im, '1947', 190, (W // 2, 150), fill=(255, 214, 60), stroke=12)
box(im, 'भारत का बँटवारा', 74, W // 2, H - 150, center=True)
save(im, 'thumb_1_jinnah_nehru_1947.jpg')

# 2. Refugee train: 1.5 crore homeless
ph = Image.open(os.path.join(HERE, 'assets', 'photos_hd', 'emergency_train.jpg')).convert('RGB')
k = max(W / ph.width, H / ph.height) * 1.12; ph = ph.resize((int(ph.width * k), int(ph.height * k)), Image.LANCZOS)
ph = ph.crop((ph.width - W, (ph.height - H) // 2, ph.width, (ph.height - H) // 2 + H))
g = np.asarray(ph.convert('L'), np.float32)
ph = Image.fromarray(np.stack([g * 1.08 + 10, g * 0.96 + 4, g * 0.8], -1).clip(0, 255).astype(np.uint8))
ph = ImageEnhance.Contrast(ph).enhance(1.25).filter(ImageFilter.UnsharpMask(2, 90, 2))
im = vignette(ph, 0.6)
grad = np.clip(1 - np.linspace(0, 1, W) / 0.62, 0, 1) ** 1.2
shade = Image.fromarray((np.tile(grad, (H, 1)) * 215).astype(np.uint8))
im.paste((0, 0, 0), (0, 0), shade)
text(im, '1.5 करोड़', 150, (40, 190), fill=(255, 214, 60), stroke=10, anchor='lm')
text(im, 'लोग बेघर', 104, (46, 330), fill=(255, 255, 255), stroke=9, anchor='lm')
box(im, 'बँटवारा 1947', 70, 46, H - 190)
save(im, 'thumb_2_train_1_5_crore.jpg')

# 3. Reference style (like the Istanbul thumbnail): black boxes + bright map + Gandhi
im = split_map((22.5, 81.0, 46.0), bright=1.05)
person(im, 'gandhi1946', 470, W - 400, H + 25, halo=(255, 255, 255), warm=False)
y = box(im, 'भारत का बँटवारा', 82, 24, 18, bg=(10, 10, 10)); box(im, '1947', 64, 24, y + 10, bg=(10, 10, 10))
save(im, 'thumb_3_reference_style_gandhi.jpg')
