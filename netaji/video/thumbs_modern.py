"""5 modern-style YouTube thumbnails (1280x720) for the Netaji video: colour-graded portrait with rim light, gradient
backgrounds with light rays, big gradient text with heavy outline, neon accents, arrows and circles. Writes ../thumbnails/"""
import os, sys, io, contextlib, math
os.environ['RES'] = '1280x720'
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import render as R
from render import W, H, font
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops
OUT = os.path.join(HERE, '..', 'thumbnails'); os.makedirs(OUT, exist_ok=True)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

def grad_bg(c0, c1, cx=0.7, cy=0.45, rays=True, ray_col=(255, 255, 255)):
    r = np.sqrt(((xx / W - cx) * 1.6) ** 2 + (yy / H - cy) ** 2)
    k = np.clip(r / 0.9, 0, 1)[..., None]
    a = np.array(c0, np.float32) * (1 - k) + np.array(c1, np.float32) * k
    if rays:
        ang = np.arctan2(yy - cy * H, xx - cx * W)
        ray = (np.sin(ang * 14) * 0.5 + 0.5) ** 6 * np.clip(1 - r / 1.1, 0, 1)
        a += ray[..., None] * np.array(ray_col, np.float32) * 0.18
    rng = np.random.default_rng(1)                       # soft bokeh dots
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')
    bk = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(bk)
    for _ in range(26):
        x, y, s = rng.random() * W, rng.random() * H, 8 + rng.random() * 34
        d.ellipse([x - s, y - s, x + s, y + s], fill=ray_col + (int(25 + rng.random() * 45),))
    im.alpha_composite(bk.filter(ImageFilter.GaussianBlur(6)))
    return im

def tritone(rgb, sh=(18, 28, 52), mid=(196, 140, 104), hi=(255, 244, 226)):
    g = np.asarray(ImageEnhance.Contrast(rgb.convert('L')).enhance(1.35), np.float32)[..., None] / 255
    lo = np.array(sh, np.float32); m = np.array(mid, np.float32); h = np.array(hi, np.float32)
    out = np.where(g < 0.5, lo + (m - lo) * (g / 0.5), m + (h - m) * ((g - 0.5) / 0.5))
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))

def person(im, name, h, x, yb, rim=(0, 220, 255), silhouette=False, mid=(196, 140, 104)):
    p = Image.open(os.path.join(HERE, 'assets', 'cut', name + '.png')).convert('RGBA')
    k = h / p.height; p = p.resize((int(p.width * k), h), Image.LANCZOS); a = p.getchannel('A')
    if name == 'bose_nrb':                               # soft oval bust: hides the photo's straight cut sides
        py_, px_ = np.mgrid[0:p.height, 0:p.width].astype(np.float32)
        r = np.sqrt(((px_ / p.width - 0.5) / 0.47) ** 2 + ((py_ / p.height - 0.42) / 0.62) ** 2)
        a = Image.fromarray((np.asarray(a, np.float32) * np.clip((1.0 - r) / 0.22, 0, 1)).astype(np.uint8))
    rgb = Image.new('RGB', p.size, (6, 6, 10)) if silhouette else tritone(p.convert('RGB'), mid=mid).filter(ImageFilter.UnsharpMask(2, 110, 2))
    rgb = rgb.convert('RGBA'); rgb.putalpha(a)
    ox, oy = int(x), int(yb - h)
    for blur, al in ((30, 0.9), (10, 1.0)):              # coloured rim light / outer glow
        g = Image.new('RGBA', p.size, rim + (0,)); g.putalpha(a.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(min(255, v * 1.6 * al))))
        im.alpha_composite(g, (ox, oy))
    edge = ImageChops.subtract(a, a.filter(ImageFilter.MinFilter(7)))   # thin bright edge
    e = Image.new('RGBA', p.size, rim + (0,)); e.putalpha(edge.point(lambda v: int(v * 0.9)))
    im.alpha_composite(rgb, (ox, oy)); im.alpha_composite(e, (ox, oy))
    return ox, oy, p.width, h

def gtext(im, s, size, xy, top=(255, 240, 90), bot=(255, 150, 20), stroke=14, anchor='lm', glow=None):
    f = font('bold', size / R.U)
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).text(xy, s, font=f, fill=255, anchor=anchor)
    ms = Image.new('L', (W, H), 0); ImageDraw.Draw(ms).text(xy, s, font=f, fill=255, anchor=anchor, stroke_width=stroke)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(ms.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.85)))
    im.alpha_composite(sh, (8, 12))
    if glow:
        g = Image.new('RGBA', (W, H), glow + (0,)); g.putalpha(ms.filter(ImageFilter.GaussianBlur(22))); im.alpha_composite(g)
    st = Image.new('RGBA', (W, H), (8, 8, 12, 0)); st.putalpha(ms); im.alpha_composite(st)
    bb = m.getbbox() or (0, 0, W, H)
    t = np.clip((yy - bb[1]) / max(1, bb[3] - bb[1]), 0, 1)[..., None]
    col = np.array(top, np.float32) * (1 - t) + np.array(bot, np.float32) * t
    fill = Image.fromarray(col.astype(np.uint8)).convert('RGBA'); fill.putalpha(m); im.alpha_composite(fill)

def pill(im, s, size, x, y, bg=(230, 30, 40), fg=(255, 255, 255), center=False):
    f = font('bold', size / R.U); l, t, r, b = f.getbbox(s); px, py = int(size * 0.5), int(size * 0.22)
    w, h = (r - l) + 2 * px, (b - t) + 2 * py
    if center: x -= w // 2
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([x + 5, y + 8, x + w + 5, y + h + 8], radius=h // 2, fill=(0, 0, 0, 140))
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg + (255,))
    d.text((x + px - l, y + py - t), s, font=f, fill=fg)
    im.alpha_composite(lay)

def arrow(im, p0, p1, col=(255, 40, 40), width=22):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    (x0, y0), (x1, y1) = p0, p1; mx, my = (x0 + x1) / 2 + (y1 - y0) * 0.25, (y0 + y1) / 2 - (x1 - x0) * 0.25
    pts = [((1 - u) ** 2 * x0 + 2 * (1 - u) * u * mx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * my + u * u * y1) for u in np.linspace(0, 0.9, 30)]
    ang = math.atan2(y1 - pts[-1][1], x1 - pts[-1][0]); L = width * 2.6
    tri = [(x1, y1), (x1 - L * math.cos(ang - 0.5), y1 - L * math.sin(ang - 0.5)), (x1 - L * math.cos(ang + 0.5), y1 - L * math.sin(ang + 0.5))]
    for c, wd in (((0, 0, 0, 180), width + 10), (col + (255,), width)):
        d.line(pts, fill=c, width=wd, joint='curve'); d.polygon(tri, fill=c)
    im.alpha_composite(lay)

def ring(im, cx, cy, r, col=(255, 40, 40), width=12):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col + (255,), width=width)
    g = lay.filter(ImageFilter.GaussianBlur(10)); im.alpha_composite(g); im.alpha_composite(lay)

def inset(im, img, cx, cy, r, col=(255, 40, 40)):
    k = 2 * r / min(img.size); img = img.resize((int(img.width * k), int(img.height * k)), Image.LANCZOS)
    img = img.crop(((img.width - 2 * r) // 2, (img.height - 2 * r) // 2, (img.width - 2 * r) // 2 + 2 * r, (img.height - 2 * r) // 2 + 2 * r))
    m = Image.new('L', (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
    img = img.convert('RGBA'); img.putalpha(m); im.alpha_composite(img, (cx - r, cy - r)); ring(im, cx, cy, r, col, 12)

def photo(name):
    return Image.open(os.path.join(HERE, 'assets', 'photos', name + '.jpg')).convert('RGB')

def fire_photo():
    ph = photo('ki21'); ph = ImageEnhance.Contrast(ph).enhance(1.3)
    g = np.asarray(ph.convert('L'), np.float32)
    ph = Image.fromarray(np.stack([g * 1.1 + 30, g * 0.75 + 10, g * 0.35], -1).clip(0, 255).astype(np.uint8))
    return ph

def save(im, name):
    im.convert('RGB').filter(ImageFilter.UnsharpMask(1, 40, 2)).save(os.path.join(OUT, name), quality=95); print('wrote', name)

# M1: big face + "ज़िंदा थे?" + burning-plane inset with arrow
im = grad_bg((230, 90, 20), (25, 6, 4), cx=0.72, cy=0.5, ray_col=(255, 190, 90))
person(im, 'bose_nrb', 760, W - 600, H + 60, rim=(255, 200, 80))
gtext(im, 'ज़िंदा थे?', 170, (36, 210), glow=(255, 120, 0))
gtext(im, 'नेताजी', 100, (44, 370), top=(255, 255, 255), bot=(220, 225, 235))
inset(im, fire_photo(), 210, 560, 120)
arrow(im, (360, 600), (520, 470))
pill(im, '18 अगस्त 1945', 40, 36, 30)
save(im, 'Netaji_Modern1_zinda_the.jpg')

# M2: Netaji vs silhouette, split blue/red
im = grad_bg((20, 70, 160), (6, 10, 30), cx=0.25, cy=0.5, ray_col=(120, 200, 255))
right = grad_bg((170, 20, 30), (25, 4, 6), cx=0.75, cy=0.5, ray_col=(255, 120, 120))
mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).polygon([(W * 0.56, 0), (W, 0), (W, H), (W * 0.44, H)], fill=255)
im.paste(right, (0, 0), mask)
ImageDraw.Draw(im).line([(W * 0.56, 0), (W * 0.44, H)], fill=(255, 255, 255), width=10)
person(im, 'bose_nrb', 600, -10, H + 30, rim=(80, 200, 255))
ox, oy, pw, ph = person(im, 'bose_nrb', 600, W - 470, H + 30, rim=(255, 70, 70), silhouette=True)
gtext(im, '?', 300, (ox + pw // 2 - 10, oy + 230), anchor='mm', top=(255, 255, 255), bot=(255, 210, 210), glow=(255, 40, 40))
gtext(im, 'गुमनामी बाबा', 112, (W // 2, 78), anchor='mm', glow=(0, 0, 0))
gtext(im, '= नेताजी?', 96, (W // 2, 190), anchor='mm', top=(255, 255, 255), bot=(230, 230, 240))
pill(im, 'फ़ैज़ाबाद 1985', 40, W // 2, H - 90, center=True)
save(im, 'Netaji_Modern2_gumnami_baba.jpg')

# M3: neon 3D map of Taiwan, crash marker, big claim
sp = dict(view=(25.2, 120.7, 8.0), pitch=48, yaw0=-8, yaw1=-8, fill=[('taiwan', 'red', -9)])
m = R.draw_map(sp, 1.0, 4.0)
g = np.asarray(m, np.float32); g = g * np.array([0.55, 0.75, 1.05]) + np.array([0, 8, 30])     # cool, modern grade
im = Image.fromarray(g.clip(0, 255).astype(np.uint8)).convert('RGBA')
im = ImageEnhance.Contrast(im).enhance(1.2)
cam = R.Cam(*R.ll(25.2, 120.7), 8.0 * R.MJ['pxd'], 48, -8); x, y, _ = cam.proj(*R.ll(25.07, 121.55))
ring(im, int(x), int(y), 70); ring(im, int(x), int(y), 110, width=6)
person(im, 'bose_nrb', 650, -30, H + 40, rim=(0, 220, 255))
gtext(im, 'हादसा', 130, (W - 520, 100), glow=(255, 60, 0), top=(255, 255, 255), bot=(235, 235, 240))
gtext(im, 'हुआ ही नहीं?', 116, (W - 640, 230), glow=(255, 60, 0))
arrow(im, (W - 330, 330), (int(x) + 60, int(y) - 40))
pill(im, 'ताइहोकू, ताइवान', 40, W - 390, H - 100)
save(im, 'Netaji_Modern3_hadsa_hua_hi_nahi.jpg')

# M4: secret files: real declassified page, TOP SECRET stamp, three verdicts
im = grad_bg((40, 40, 48), (6, 6, 10), cx=0.65, cy=0.4, ray_col=(255, 220, 160))
pg = photo('tok_p1').resize((430, 600), Image.LANCZOS).rotate(-7, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0))
pm = Image.new('L', (430, 600), 255).rotate(-7, expand=True)
sh = Image.new('RGBA', pg.size, (0, 0, 0, 0)); sh.putalpha(pm.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.8)))
im.alpha_composite(sh, (W - 560 + 14, 70 + 20)); pgr = pg.convert('RGBA'); pgr.putalpha(pm); im.alpha_composite(pgr, (W - 560, 70))
st = R.stamp_img('गुप्त फ़ाइल', (230, 30, 30), 90); im.alpha_composite(st, (W - 520, 380))
person(im, 'uniform', 700, 30, H + 20, rim=(255, 200, 80))
gtext(im, '3 जाँच', 132, (330, 150), glow=(255, 120, 0))
gtext(im, '2 जवाब', 132, (330, 300), top=(255, 255, 255), bot=(230, 230, 240))
pill(im, 'सच क्या है?', 60, 340, 430)
save(im, 'Netaji_Modern4_3_jaanch_2_jawab.jpg')

# M5: the urn in Tokyo + glowing DNA helix
im = grad_bg((10, 90, 110), (2, 12, 20), cx=0.7, cy=0.5, ray_col=(120, 255, 230))
lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)            # DNA double helix (neon)
for i in range(60):
    t = i / 59; yv = 60 + t * (H - 120); ph = t * math.pi * 4
    xa, xb = W - 330 + 110 * math.sin(ph), W - 330 - 110 * math.sin(ph)
    if i % 3 == 0: d.line([(xa, yv), (xb, yv)], fill=(160, 255, 240, 140), width=5)
    for xv, c in ((xa, (60, 255, 220)), (xb, (255, 90, 200))): d.ellipse([xv - 9, yv - 9, xv + 9, yv + 9], fill=c + (255,))
im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(9))); im.alpha_composite(lay)
cx, cy = W - 330, H // 2 + 40                                                   # golden urn
u = Image.new('RGBA', (W, H), (0, 0, 0, 0)); du = ImageDraw.Draw(u)
du.ellipse([cx - 120, cy - 80, cx + 120, cy + 140], fill=(214, 160, 50, 255), outline=(60, 35, 5, 255), width=6)
du.rectangle([cx - 60, cy - 140, cx + 60, cy - 70], fill=(200, 145, 40, 255), outline=(60, 35, 5, 255), width=6)
du.ellipse([cx - 80, cy - 170, cx + 80, cy - 120], fill=(235, 190, 80, 255), outline=(60, 35, 5, 255), width=6)
du.rectangle([cx - 90, cy + 130, cx + 90, cy + 170], fill=(170, 120, 30, 255), outline=(60, 35, 5, 255), width=6)
du.ellipse([cx - 70, cy - 40, cx - 20, cy + 60], fill=(255, 240, 180, 120))
gl = Image.new('RGBA', (W, H), (255, 200, 80, 0)); gl.putalpha(u.getchannel('A').filter(ImageFilter.GaussianBlur(40)))
im.alpha_composite(gl); im.alpha_composite(u)
person(im, 'bose_nrb', 650, -20, H + 40, rim=(60, 255, 220))
gtext(im, '80 साल', 140, (430, 140), glow=(0, 0, 0))
gtext(im, 'किसकी अस्थियाँ?', 92, (380, 270), top=(255, 255, 255), bot=(220, 240, 240))
pill(im, 'DNA से खुलेगा राज़?', 50, 420, 380, bg=(230, 30, 40))
pill(im, 'रेंकोजी मंदिर, टोक्यो', 34, W - 330, H - 70, bg=(15, 15, 20), center=True)
save(im, 'Netaji_Modern5_dna_asthiyan.jpg')
