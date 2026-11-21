"""5 HD thumbnails (1920x1080) for the Shastri video, title 2. Netaji's portraits are Real-ESRGAN x2 upscales of the
public-domain photos (assets/hd, cut out with alpha matting in assets/cut/*_hd.png). Real photos/documents only, no clip-art.
Writes ../thumbnails/Shastri_HD*.jpg"""
import os, sys, io, contextlib, math
os.environ['RES'] = '1920x1080'
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import render as R
from render import W, H, font
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
OUT = os.path.join(HERE, '..', 'thumbnails'); os.makedirs(OUT, exist_ok=True)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

def vignette(im, k=0.65, cx=0.5, cy=0.5):
    r = np.sqrt(((xx / W - cx) / 0.5) ** 2 + ((yy / H - cy) / 0.5) ** 2)
    v = (1 - k * np.clip(r - 0.4, 0, 1) ** 1.2).clip(0.15, 1)[..., None]
    return Image.fromarray((np.asarray(im.convert('RGB'), np.float32) * v).clip(0, 255).astype(np.uint8)).convert('RGBA')

def cover(path, zoom=1.0, fx=0.5, fy=0.5):
    ph = Image.open(path).convert('RGB'); k = max(W / ph.width, H / ph.height) * zoom
    ph = ph.resize((int(ph.width * k) + 2, int(ph.height * k) + 2), Image.LANCZOS)
    x0 = int((ph.width - W) * fx); y0 = int((ph.height - H) * fy)
    return ph.crop((x0, y0, x0 + W, y0 + H))

def tone(img, sh=(20, 26, 40), hi=(255, 236, 205), contrast=1.25):
    """natural black & white with split toning (cool shadows, warm highlights) and local contrast"""
    g = ImageEnhance.Contrast(img.convert('L')).enhance(contrast)
    g = Image.fromarray((255 * (np.asarray(g, np.float32) / 255) ** 1.45 * 0.9).astype(np.uint8))   # tame bright clothing
    g = Image.blend(g, g.filter(ImageFilter.UnsharpMask(40, 60, 0)), 0.6)        # clarity
    a = np.asarray(g, np.float32)[..., None] / 255
    out = np.array(sh, np.float32) * (1 - a) + np.array(hi, np.float32) * a
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))

def portrait(im, name, h, x, yb, rim=(255, 190, 70), oval=True, silhouette=False, cx=0.5, cy=0.42, rx=0.48, ry=0.62):
    p = Image.open(os.path.join(HERE, 'assets', 'cut', name + '_hd.png')).convert('RGBA')
    k = h / p.height; p = p.resize((int(p.width * k), h), Image.LANCZOS)
    a = np.asarray(p.getchannel('A'), np.float32)
    if oval:
        py_, px_ = np.mgrid[0:p.height, 0:p.width].astype(np.float32)
        r = np.sqrt(((px_ / p.width - cx) / rx) ** 2 + ((py_ / p.height - cy) / ry) ** 2); a = a * np.clip((1.0 - r) / 0.25, 0, 1)
    A = Image.fromarray(a.astype(np.uint8))
    rgb = Image.new('RGB', p.size, (5, 5, 8)) if silhouette else tone(p.convert('RGB')).filter(ImageFilter.UnsharpMask(2, 70, 1))
    ox, oy = int(x), int(yb - h)
    for blur, mul in ((60, 0.8), (18, 1.0)):
        g = Image.new('RGBA', p.size, rim + (0,)); g.putalpha(A.point(lambda v: 255 if v > 150 else 0).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(min(255, v * mul))))
        im.alpha_composite(g, (ox, oy))
    rgba = rgb.convert('RGBA'); rgba.putalpha(A); im.alpha_composite(rgba, (ox, oy))
    return ox, oy, p.width, h

def gtext(im, s, size, xy, top=(255, 238, 80), bot=(255, 140, 0), stroke=20, anchor='lm', glow=None):
    f = font('bold', size)
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).text(xy, s, font=f, fill=255, anchor=anchor)
    ms = Image.new('L', (W, H), 0); ImageDraw.Draw(ms).text(xy, s, font=f, fill=255, anchor=anchor, stroke_width=stroke)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(ms.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * 0.9)))
    im.alpha_composite(sh, (10, 16))
    if glow: g = Image.new('RGBA', (W, H), glow + (0,)); g.putalpha(ms.filter(ImageFilter.GaussianBlur(36))); im.alpha_composite(g)
    st = Image.new('RGBA', (W, H), (6, 6, 10, 0)); st.putalpha(ms); im.alpha_composite(st)
    bb = m.getbbox() or (0, 0, W, H); t = np.clip((yy - bb[1]) / max(1, bb[3] - bb[1]), 0, 1)[..., None]
    col = np.array(top, np.float32) * (1 - t) + np.array(bot, np.float32) * t
    fill = Image.fromarray(col.astype(np.uint8)).convert('RGBA'); fill.putalpha(m); im.alpha_composite(fill)

def pill(im, s, size, x, y, bg=(225, 25, 35), center=False):
    f = font('bold', size); l, t, r, b = f.getbbox(s); px, py = int(size * 0.5), int(size * 0.24)
    w, h = (r - l) + 2 * px, (b - t) + 2 * py
    if center: x -= w // 2
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([x + 6, y + 10, x + w + 6, y + h + 10], radius=h // 2, fill=(0, 0, 0, 150))
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg + (255,)); d.text((x + px - l, y + py - t), s, font=f, fill=(255, 255, 255))
    im.alpha_composite(lay)

def ring(im, cx, cy, r, col=(255, 40, 40), width=16):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse([cx - r, cy - r, cx + r, cy + r], outline=col + (255,), width=width)
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(14))); im.alpha_composite(lay)

def grade(img, mul, add=(0, 0, 0), sat=1.0):
    a = np.asarray(ImageEnhance.Color(img).enhance(sat), np.float32) * np.array(mul) + np.array(add)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))

def save(im, name):
    p = os.path.join(OUT, name); im.convert('RGB').save(p, quality=93, subsampling=0)
    print('wrote', name, os.path.getsize(p) // 1024, 'KB')

HD = lambda n: os.path.join(HERE, 'assets', 'hd', n + '.jpg')
SUB = 'दिल का दौरा या कुछ और?'   # title 2: the thumbnail text complements it, never repeats it word for word

def map_bg(view, pitch=50, yaw=0, fill=None, pulse=None, route=None):
    sp = dict(view=view, pitch=pitch, yaw0=yaw, yaw1=yaw, fill=fill or [], pulse=pulse or [], routes=route or [])
    m = R.draw_map(sp, 4.0, 4.0)
    return ImageEnhance.Contrast(ImageEnhance.Color(m).enhance(1.2)).enhance(1.15).convert('RGBA')

# HD1  big face + "दिल का दौरा?" / "या कुछ और?"
im = R.card_bg_modern('dark', 2.0).convert('RGBA')
g = np.asarray(im, np.float32); g[..., :3] *= 0.85; im = Image.fromarray(g.astype(np.uint8))
im = vignette(im, 0.55, cx=0.7)
portrait(im, 'shastri_bust', 1150, W - 980, H + 60, rim=(255, 185, 60), cx=0.5, cy=0.42, rx=0.5, ry=0.64)
gtext(im, 'दिल का दौरा?', 190, (70, 250), top=(255, 255, 255), bot=(225, 228, 235), glow=(0, 0, 0))
gtext(im, 'या कुछ और?', 220, (60, 500), glow=(255, 90, 0))
pill(im, 'ताशकंद, 11 जनवरी 1966', 60, 80, 700)
save(im, 'Shastri_HD1_dil_ka_daura.jpg')

# HD2  official vs family: two badges and a question mark
im = R.card_bg_modern('dark', 5.0).convert('RGBA'); im = vignette(im, 0.5)
portrait(im, 'shastri_bust', 1100, W // 2 - 380, H + 100, rim=(255, 255, 255), cx=0.5, cy=0.42, rx=0.5, ry=0.64)
pill(im, 'सरकार: दिल का दौरा', 64, 80, 300, bg=(30, 140, 70))
pill(im, 'परिवार: शरीर नीला क्यों?', 64, W - 900, 300, bg=(210, 30, 35))
gtext(im, 'सच क्या है?', 200, (W // 2, 140), anchor='mm', glow=(255, 90, 0))
pill(im, 'पोस्टमार्टम: नहीं हुआ', 56, W // 2, H - 150, bg=(15, 15, 20), center=True)
save(im, 'Shastri_HD2_sarkar_vs_parivar.jpg')

# HD3  the 1:32 clock
img = Image.new('RGB', (W, H)); R.draw_clock(img, 4.0, dict(hm=(1, 31), sec0=50)); im = img.convert('RGBA')
im = im.transform(im.size, Image.AFFINE, (1, 0, -420, 0, 1, 0), resample=Image.BICUBIC)       # clock to the right
im = vignette(im, 0.5, cx=0.7)
portrait(im, 'shastri_bust', 1050, -120, H + 100, rim=(255, 185, 60), cx=0.5, cy=0.42, rx=0.5, ry=0.64)
gtext(im, 'रात 1:32', 200, (W - 560, 130), anchor='mm', top=(255, 255, 255), bot=(225, 228, 235), glow=(0, 0, 0))
gtext(im, 'क्या हुआ?', 190, (W - 560, H - 150), anchor='mm', glow=(255, 90, 0))
save(im, 'Shastri_HD3_raat_1_32.jpg')

# HD4  map: Delhi to Tashkent
P = R.sys.modules['plan']
im = map_bg((36.0, 72.5, 22.0), pitch=46, yaw=6, fill=[('uzbek', 'gold', -9)], pulse=[(41.31, 69.24, 0.0, 'red')],
            route=[dict(pts=[(28.61, 77.21), (41.31, 69.24)], at=0.0, dur=0.1, icon='plane', col='gold')])
im = vignette(ImageEnhance.Brightness(im).enhance(0.85), 0.6)
portrait(im, 'shastri_bust', 1080, -140, H + 110, rim=(60, 200, 255), cx=0.5, cy=0.42, rx=0.5, ry=0.64)
gtext(im, 'ताशकंद', 210, (W - 640, 170), top=(255, 255, 255), bot=(225, 230, 240), glow=(0, 0, 0))
gtext(im, 'की वो रात', 190, (W - 700, 390), glow=(255, 90, 0))
pill(im, '60 साल बाद भी सवाल', 60, W - 620, H - 170)
save(im, 'Shastri_HD4_tashkent.jpg')

# HD5  the secret file (News Headline card)
img = R.card_bg_modern('red', 3.0).convert('RGBA')
doc = dict(title='शास्त्री फ़ाइल', lines=[('पोस्टमार्टम: नहीं हुआ', -9), ('गवाह: दोनों हादसों के शिकार', -9), ('PMO: एक दस्तावेज़ अब भी गुप्त', -9)])
R.draw_doc(img, dict(doc=doc, docstyle='headline'), 9.0)
im = img.transform(img.size, Image.AFFINE, (1, 0, -330, 0, 1, 40), resample=Image.BICUBIC)
im = vignette(im, 0.5)
portrait(im, 'shastri_bust', 1080, -150, H + 110, rim=(255, 185, 60), cx=0.5, cy=0.42, rx=0.5, ry=0.64)
gtext(im, 'गुप्त फ़ाइल', 170, (W // 2 + 330, 110), anchor='mm', glow=(255, 60, 0))
save(im, 'Shastri_HD5_gupt_file.jpg')
