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

def face(im, h, x, yb, rim=(255, 185, 60), rx=0.5, ry=0.56):
    """Shastri's portrait (assets/hd/shastri_face.jpg: 1965, CC0, Real-ESRGAN x2) with a soft oval fade, toned highlights, coloured glow"""
    p = Image.open(os.path.join(HERE, 'assets', 'hd', 'shastri_face.jpg')).convert('RGB')
    p = p.crop((int(p.width * 0.12), 0, int(p.width * 0.95), int(p.height * 0.72)))      # head, cap and shoulders
    k = h / p.height; p = p.resize((int(p.width * k), h), Image.LANCZOS)
    g = np.asarray(ImageEnhance.Contrast(p.convert('L')).enhance(1.15), np.float32) / 255
    g = g ** 1.12 * 0.97                                                  # tame the white cap and kurta, keep the face bright
    rgb = np.stack([g * 255 + 8, g * 247 + 4, g * 232], -1)              # warm black & white
    py_, px_ = np.mgrid[0:p.height, 0:p.width].astype(np.float32)
    r = np.sqrt(((px_ / p.width - 0.52) / rx) ** 2 + ((py_ / p.height - 0.42) / ry) ** 2)
    A = Image.fromarray((np.clip((1.0 - r) / 0.3, 0, 1) * 255).astype(np.uint8))
    pad = 200; Ab = Image.new('L', (p.width + 2 * pad, p.height + 2 * pad), 0); Ab.paste(A, (pad, pad))   # room for the glow
    for blur, mul in ((70, 0.7), (25, 0.55)):
        gl = Image.new('RGBA', Ab.size, rim + (0,)); gl.putalpha(Ab.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(min(255, v * mul))))
        im.alpha_composite(gl, (int(x) - pad, int(yb - p.height) - pad)) if int(x) - pad >= 0 and int(yb - p.height) - pad >= 0 else \
            im.alpha_composite(gl.crop((max(0, pad - int(x)), max(0, pad - int(yb - p.height)), gl.width, gl.height)), (max(0, int(x) - pad), max(0, int(yb - p.height) - pad)))
    pi = Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).filter(ImageFilter.UnsharpMask(2, 80, 2)).convert('RGBA'); pi.putalpha(A)
    im.alpha_composite(pi, (int(x), int(yb - p.height)))

def bg_dark(t=2.0, tone='dark', k=0.9):
    im = R.card_bg_modern(tone, t).convert('RGBA')
    g = np.asarray(im, np.float32); g[..., :3] *= k; return Image.fromarray(g.astype(np.uint8))

# 1  "दिल का दौरा? / या कुछ और?"
im = vignette(bg_dark(), 0.55, cx=0.72)
face(im, 1080, W - 980, H, rim=(255, 175, 50))
gtext(im, 'दिल का दौरा?', 180, (70, 240), top=(255, 255, 255), bot=(220, 224, 232), glow=(0, 0, 0))
gtext(im, 'या कुछ और?', 215, (60, 480), glow=(255, 90, 0))
pill(im, 'ताशकंद, 11 जनवरी 1966', 58, 80, 680)
save(im, 'Shastri_HD1_dil_ka_daura.jpg')

# 2  सरकार vs परिवार
im = vignette(bg_dark(5.0), 0.5)
face(im, 1000, W // 2 - 470, H, rim=(255, 255, 255))
gtext(im, 'सच क्या है?', 180, (W // 2, 110), anchor='mm', glow=(255, 90, 0))
pill(im, 'सरकार: दिल का दौरा', 62, 60, 330, bg=(30, 140, 70))
pill(im, 'परिवार: शरीर नीला क्यों?', 62, W - 880, 330, bg=(210, 30, 35))
pill(im, 'पोस्टमार्टम: नहीं हुआ', 56, W // 2, H - 130, bg=(15, 15, 20), center=True)
save(im, 'Shastri_HD2_sarkar_vs_parivar.jpg')

# 3  रात 1:32
img = Image.new('RGB', (W, H)); R.draw_clock(img, 4.0, dict(hm=(1, 31), sec0=50)); im = img.convert('RGBA')
im = im.transform(im.size, Image.AFFINE, (1, 0, -430, 0, 1, 0), resample=Image.BICUBIC); im = vignette(im, 0.5, cx=0.7)
face(im, 1020, -180, H, rim=(255, 175, 50))
gtext(im, 'रात 1:32', 190, (W - 560, 120), anchor='mm', top=(255, 255, 255), bot=(225, 228, 235), glow=(0, 0, 0))
gtext(im, 'क्या हुआ?', 180, (W - 560, H - 140), anchor='mm', glow=(255, 90, 0))
save(im, 'Shastri_HD3_raat_1_32.jpg')

# 4  ताशकंद की वो रात (map)
sp = dict(view=(36.0, 72.5, 22.0), pitch=46, yaw0=6, yaw1=6, fill=[('uzbek', 'gold', -9)], pulse=[(41.31, 69.24, 0.0, 'red')],
          routes=[dict(pts=[(28.61, 77.21), (41.31, 69.24)], at=0.0, dur=0.1, icon='plane', col='gold')])
m = ImageEnhance.Contrast(ImageEnhance.Color(R.draw_map(sp, 4.0, 4.0)).enhance(1.2)).enhance(1.15).convert('RGBA')
im = vignette(ImageEnhance.Brightness(m).enhance(0.8), 0.6)
face(im, 1020, -180, H, rim=(60, 200, 255))
gtext(im, 'ताशकंद', 200, (W - 640, 160), top=(255, 255, 255), bot=(225, 230, 240), glow=(0, 0, 0))
gtext(im, 'की वो रात', 185, (W - 700, 380), glow=(255, 90, 0))
pill(im, '60 साल बाद भी सवाल', 58, W - 620, H - 160)
save(im, 'Shastri_HD4_tashkent.jpg')

# 5  गुप्त फ़ाइल
img = R.card_bg_modern('red', 3.0).convert('RGBA')
doc = dict(title='शास्त्री फ़ाइल', lines=[('पोस्टमार्टम: नहीं हुआ', -9), ('दो गवाह: दोनों हादसों में', -9), ('PMO: एक दस्तावेज़ गुप्त', -9)])
R.draw_doc(img, dict(doc=doc, docstyle='headline'), 9.0)
im = img.transform(img.size, Image.AFFINE, (1, 0, -360, 0, 1, 40), resample=Image.BICUBIC); im = vignette(im, 0.5)
face(im, 1020, -240, H, rim=(255, 175, 50))
gtext(im, 'गुप्त फ़ाइल', 170, (W // 2 + 360, 100), anchor='mm', glow=(255, 60, 0))
save(im, 'Shastri_HD5_gupt_file.jpg')
