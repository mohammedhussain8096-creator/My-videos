"""5 high-quality modern thumbnails (1920x1080) for the Netaji video. Netaji's portraits are Real-ESRGAN x2 upscales of the
public-domain photos (assets/hd, cut out with alpha matting in assets/cut/*_hd.png). Real photos/documents only, no clip-art.
Writes ../thumbnails/Netaji_HD*.jpg"""
import os, sys, io, contextlib, math
os.environ['RES'] = '1920x1080'
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import render as R
from render import W, H, font
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
OUT = os.path.join(HERE, '..', 'thumbnails')
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
    for blur, mul in ((60, 1.1), (18, 1.4)):
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

# HD1  "ज़िंदा थे?"  burning bomber + big face
bg = cover(HD('ki21'), zoom=1.25, fx=0.25, fy=0.45)
g = np.asarray(bg.convert('L'), np.float32)
bg = Image.fromarray(np.stack([g * 1.05 + 45, g * 0.62 + 12, g * 0.22], -1).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))
im = bg.convert('RGBA'); im.alpha_composite(R.fire_layer(1.3, 1.0)); im = vignette(im, 0.7, cx=0.35)
portrait(im, 'bose_nrb', 1180, W - 1000, H + 120, rim=(255, 170, 60))
gtext(im, 'नेताजी', 120, (70, 200), top=(255, 255, 255), bot=(225, 228, 235))
gtext(im, 'ज़िंदा थे?', 230, (60, 430), glow=(255, 90, 0))
pill(im, '18 अगस्त 1945', 64, 80, 640)
save(im, 'Netaji_HD1_zinda_the.jpg')

# HD2  "हादसा हुआ था?"  Taihoku 3D map, red crash ring
sp = dict(view=(26.6, 120.2, 14.0), pitch=46, yaw0=-6, yaw1=-6, fill=[('taiwan', 'red', -9)])
m = R.draw_map(sp, 1.0, 4.0)
m = grade(m, (0.62, 0.8, 1.05), (0, 10, 34), 1.1); m = ImageEnhance.Contrast(m).enhance(1.15).filter(ImageFilter.UnsharpMask(3, 80, 2))
im = vignette(m, 0.6, cx=0.6)
cam = R.Cam(*R.ll(26.6, 120.2), 14.0 * R.MJ['pxd'], 46, -6); x, y, _ = cam.proj(*R.ll(25.07, 121.55))
ring(im, int(x), int(y), 80); ring(im, int(x), int(y), 130, width=8)
portrait(im, 'bose_nrb', 1080, -150, H + 110, rim=(0, 200, 255))
gtext(im, 'हादसा', 200, (W - 820, 150), top=(255, 255, 255), bot=(225, 230, 240), glow=(0, 0, 0))
gtext(im, 'हुआ था?', 200, (W - 820, 360), glow=(255, 60, 0))
pill(im, 'ताइहोकू, 1945', 60, W - 520, H - 150)
save(im, 'Netaji_HD2_hadsa_hua_tha.jpg')

# HD3  "गुमनामी बाबा = नेताजी?"  face vs silhouette
im = Image.new('RGBA', (W, H)); a = np.zeros((H, W, 3), np.float32)
left = (xx < W * (0.52 - 0.12 * (yy / H)))[..., None]
a[:] = np.where(left, np.array([18, 40, 90]), np.array([90, 10, 14])); a *= (0.55 + 0.6 * np.exp(-((xx / W - 0.5) ** 2) / 0.08))[..., None]
im = vignette(Image.fromarray(a.clip(0, 255).astype(np.uint8)), 0.55)
d = ImageDraw.Draw(im); d.line([(W * 0.52, 0), (W * 0.40, H)], fill=(255, 255, 255), width=12)
portrait(im, 'bose_nrb', 960, -40, H + 60, rim=(80, 190, 255))
ox, oy, pw, ph = portrait(im, 'bose_nrb', 960, W - 820, H + 60, rim=(255, 50, 50), silhouette=True)
gtext(im, '?', 420, (ox + pw // 2, oy + 400), anchor='mm', top=(255, 255, 255), bot=(255, 200, 200), glow=(255, 30, 30))
gtext(im, 'गुमनामी बाबा', 150, (W // 2, 120), anchor='mm', glow=(0, 0, 0))
gtext(im, 'ही नेताजी थे?', 120, (W // 2, 270), anchor='mm', top=(255, 255, 255), bot=(225, 228, 235))
save(im, 'Netaji_HD3_gumnami_baba.jpg')

# HD4  real declassified file + stamp
bg = cover(os.path.join(HERE, 'assets', 'photos', 'file_p1.jpg'), zoom=1.4, fx=0.5, fy=0.3).filter(ImageFilter.GaussianBlur(10))
im = vignette(ImageEnhance.Brightness(grade(bg, (0.6, 0.5, 0.45))).enhance(0.6), 0.7)
pg = Image.open(os.path.join(HERE, 'assets', 'photos', 'tok_p1.jpg')).convert('RGB')
pg = pg.resize((700, int(700 * pg.height / pg.width)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2))
pm = Image.new('L', pg.size, 255); pg = pg.convert('RGBA'); pg.putalpha(pm); pg = pg.rotate(-6, expand=True, resample=Image.BICUBIC)
sh = Image.new('RGBA', pg.size, (0, 0, 0, 0)); sh.putalpha(pg.getchannel('A').filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v * 0.9)))
px0, py0 = W - pg.width - 90, 60
im.alpha_composite(sh, (px0 + 20, py0 + 30)); im.alpha_composite(pg, (px0, py0))
st = R.stamp_img('गुप्त', (230, 25, 25), 150); im.alpha_composite(st, (px0 + 120, py0 + 560))
portrait(im, 'uniform', 1060, 40, H + 30, rim=(255, 190, 70), oval=False)
gtext(im, 'गुप्त', 220, (560, 260), glow=(255, 60, 0))
gtext(im, 'फ़ाइलें', 200, (560, 480), top=(255, 255, 255), bot=(225, 228, 235))
pill(im, 'मौत का सच?', 70, 580, 650)
save(im, 'Netaji_HD4_gupt_files.jpg')

# HD5  "किसकी अस्थियाँ?"  Tokyo, 80 years
sp = dict(view=(35.0, 137.5, 16.0), pitch=50, yaw0=10, yaw1=10, fill=[('japan', 'gold', -9)], pulse=[(35.69, 139.64, 0.0, 'gold')])
m = R.draw_map(sp, 1.4, 4.0)
m = grade(m, (0.55, 0.85, 0.95), (0, 14, 22), 1.1).filter(ImageFilter.GaussianBlur(1.2))
im = vignette(ImageEnhance.Brightness(m).enhance(0.9), 0.65, cx=0.7)
cam = R.Cam(*R.ll(35.0, 137.5), 16.0 * R.MJ['pxd'], 50, 10); x, y, _ = cam.proj(*R.ll(35.69, 139.64))
ring(im, int(x), int(y), 70, col=(255, 200, 60)); pill(im, 'रेंकोजी मंदिर, टोक्यो', 48, int(x) + 40, int(y) + 90, bg=(15, 15, 22), center=False)
portrait(im, 'bose_nrb', 1080, -120, H + 110, rim=(60, 240, 220))
gtext(im, '80 साल से', 150, (780, 170), top=(255, 255, 255), bot=(225, 235, 240), glow=(0, 0, 0))
gtext(im, 'किसकी अस्थियाँ?', 150, (720, 360), glow=(255, 100, 0))
pill(im, 'DNA टेस्ट कब?', 72, 780, 700)
save(im, 'Netaji_HD5_kiski_asthiyan.jpg')
