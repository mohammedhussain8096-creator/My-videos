"""5 YouTube thumbnails (1280x720) for the Netaji video, built from the video's own photos, maps and cards. Writes ../thumbnails/"""
import os, sys, io, contextlib, math
os.environ['RES'] = '1280x720'
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import render as R
from render import W, H, font
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
OUT = os.path.join(HERE, '..', 'thumbnails'); os.makedirs(OUT, exist_ok=True)

def vignette(im, k=0.6):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    v = (1 - k * np.clip(r - 0.45, 0, 1) ** 1.3).clip(0.2, 1)[..., None]
    return Image.fromarray((np.asarray(im.convert('RGB'), np.float32) * v).clip(0, 255).astype(np.uint8)).convert('RGBA')

def cover(name, grade=True):
    ph = Image.open(os.path.join(HERE, 'assets', 'photos', name + '.jpg')).convert('RGB')
    k = max(W / ph.width, H / ph.height); ph = ph.resize((int(ph.width * k) + 1, int(ph.height * k) + 1), Image.LANCZOS)
    ph = ph.crop(((ph.width - W) // 2, (ph.height - H) // 2, (ph.width - W) // 2 + W, (ph.height - H) // 2 + H))
    if grade:
        g = np.asarray(ph.convert('L'), np.float32)
        ph = Image.fromarray(np.stack([g * 1.08 + 10, g * 0.95 + 4, g * 0.78], -1).clip(0, 255).astype(np.uint8))
    return ImageEnhance.Contrast(ph).enhance(1.2).convert('RGBA')

def person(im, name, h, x, y_bottom, halo=(255, 200, 90), warm=True, silhouette=False):
    p = Image.open(os.path.join(HERE, 'assets', 'cut', name + '.png')).convert('RGBA')
    k = h / p.height; p = p.resize((int(p.width * k), h), Image.LANCZOS)
    a = p.getchannel('A')
    if silhouette: rgb = Image.new('RGB', p.size, (8, 6, 6))
    else:
        rgb = ImageEnhance.Contrast(p.convert('RGB')).enhance(1.25)
        if warm:
            g = np.asarray(rgb.convert('L'), np.float32)
            rgb = Image.fromarray(np.stack([g * 1.06 + 8, g * 0.98 + 4, g * 0.86], -1).clip(0, 255).astype(np.uint8))
        rgb = rgb.filter(ImageFilter.UnsharpMask(2, 90, 2))
    rgb = rgb.convert('RGBA'); rgb.putalpha(a)
    hl = Image.new('RGBA', p.size, halo + (0,)); hl.putalpha(a.filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.9)))
    im.alpha_composite(hl, (int(x), int(y_bottom - h))); im.alpha_composite(rgb, (int(x), int(y_bottom - h)))
    return (int(x), int(y_bottom - h), p.width, h)

def text(im, s, size, xy, fill=(255, 255, 255), stroke=10, anchor='mm'):
    f = font('bold', size / R.U)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((xy[0] + 6, xy[1] + 8), s, font=f, fill=(0, 0, 0, 210), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, 210))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(im).text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(10, 10, 10))

def box(im, s, size, x, y, bg=(205, 25, 25), fg=(255, 255, 255), center=False):
    f = font('bold', size / R.U); l, t, r, b = f.getbbox(s); pad = int(size * 0.28)
    w, h = (r - l) + 2 * pad, (b - t) + 2 * pad
    if center: x = x - w // 2
    ImageDraw.Draw(im).rectangle([x, y, x + w, y + h], fill=bg); ImageDraw.Draw(im).text((x + pad - l, y + pad - t), s, font=f, fill=fg)
    return y + h

def red_x(im, cx, cy, r, width=26):
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for a, b in (((cx - r, cy - r), (cx + r, cy + r)), ((cx + r, cy - r), (cx - r, cy + r))):
        d.line([a, b], fill=(0, 0, 0, 200), width=width + 12); d.line([a, b], fill=(235, 30, 25, 255), width=width)
    im.alpha_composite(lay)

def save(im, name):
    im.convert('RGB').save(os.path.join(OUT, name), quality=95); print('wrote', name)

# 1. "Was he alive?" Bose over the burning bomber
im = cover('ki21'); im = im.resize((int(W * 1.35), int(H * 1.35)), Image.LANCZOS).crop((int(W * 0.35) - 40, int(H * 0.08), int(W * 0.35) - 40 + W, int(H * 0.08) + H)); im.alpha_composite(R.fire_layer(1.3, 1.0)); im.alpha_composite(R.fire_layer(2.1, 0.7))
im = vignette(ImageEnhance.Brightness(im).enhance(0.8), 0.7)
person(im, 'bose_nrb', 700, W - 560, H + 40, halo=(255, 170, 60))
y = box(im, '18 अगस्त 1945', 50, 40, 36)
text(im, 'ज़िंदा थे?', 150, (50, 250), fill=(255, 214, 60), stroke=12, anchor='lm')
text(im, 'नेताजी', 104, (56, 410), stroke=10, anchor='lm')
save(im, 'Netaji_Thumb1_zinda_the.jpg')

# 2. "The crash never happened?" 3D map of Taiwan with a red X on Taihoku
sp = dict(view=(25.4, 120.4, 9.0), pitch=46, yaw0=-6, yaw1=-6, fill=[('taiwan', 'gold', -9)], pulse=[(25.07, 121.55, 0.0, 'red')])
im = ImageEnhance.Contrast(ImageEnhance.Color(R.draw_map(sp, 1.2, 4.0)).enhance(1.3)).enhance(1.15).convert('RGBA')
im = vignette(im, 0.55)
cam = R.Cam(*R.ll(25.4, 120.4), 9.0 * R.MJ['pxd'], 46, -6); x, y, _ = cam.proj(*R.ll(25.07, 121.55))
red_x(im, x, y, 70)
person(im, 'bose_nrb', 640, -40, H + 30, halo=(255, 255, 255))
text(im, 'हादसा', 120, (W - 250, 95), fill=(255, 255, 255), stroke=11)
text(im, 'हुआ ही नहीं?', 96, (W - 270, 210), fill=(255, 214, 60), stroke=11)
box(im, 'ताइहोकू 1945', 46, W - 300, H - 110, center=True)
save(im, 'Netaji_Thumb2_hadsa_hua_hi_nahi.jpg')

# 3. "3 inquiries, 2 answers": the case files with stamps
sp = dict(kind='card', tone='dark', files=[('1956', 'शाहनवाज़ समिति', -9), ('1970', 'खोसला आयोग', -9), ('1999', 'मुखर्जी आयोग', -9)],
          stamps=[(0, 'विमान दुर्घटना', 'green', -9), (1, 'विमान दुर्घटना', 'green', -9), (2, 'कोई दुर्घटना नहीं', 'red', -9)])
im = R.draw_card(sp, 5.0, 5.0).convert('RGBA')
im = im.transform(im.size, Image.AFFINE, (1, 0, 0, 0, 1, -70), resample=Image.BICUBIC)
im = vignette(im, 0.5)
text(im, '3 जाँच, 2 जवाब', 118, (W // 2, 92), fill=(255, 214, 60), stroke=12)
box(im, 'नेताजी की मौत का सच?', 56, W // 2, H - 118, center=True)
save(im, 'Netaji_Thumb3_3_jaanch_2_jawab.jpg')

# 4. "Gumnami Baba = Netaji?": portrait vs dark silhouette
bg = np.zeros((H, W, 3), np.float32); xx = np.linspace(-1, 1, W)[None, :]
bg[..., 0] = 70 + 50 * (1 - np.abs(xx)); bg[..., 1] = 14; bg[..., 2] = 12
im = vignette(Image.fromarray(bg.astype(np.uint8)), 0.5)
person(im, 'bose_nrb', 560, 10, H + 20, halo=(255, 200, 90))
bx = person(im, 'bose_nrb', 560, W - 450, H + 20, halo=(255, 255, 255), silhouette=True)
text(im, '?', 260, (bx[0] + bx[2] // 2 - 20, bx[1] + 200), fill=(255, 255, 255), stroke=12)
text(im, '=', 200, (W // 2, H // 2 + 60), fill=(255, 214, 60), stroke=12)
text(im, 'गुमनामी बाबा', 104, (W // 2, 80), fill=(255, 214, 60), stroke=11)
text(im, 'ही नेताजी थे?', 84, (W // 2, 182), fill=(255, 255, 255), stroke=10)
save(im, 'Netaji_Thumb4_gumnami_baba.jpg')

# 5. "Ashes kept for 80 years": Tokyo 3D map, Bose in uniform
sp = dict(view=(35.4, 138.6, 10.0), pitch=50, yaw0=8, yaw1=8, fill=[('japan', 'gold', -9)], pulse=[(35.69, 139.64, 0.0, 'gold')])
im = ImageEnhance.Contrast(ImageEnhance.Color(R.draw_map(sp, 1.0, 4.0)).enhance(1.3)).enhance(1.15).convert('RGBA')
im = vignette(ImageEnhance.Brightness(im).enhance(0.85), 0.6)
cam = R.Cam(*R.ll(35.4, 138.6), 10.0 * R.MJ['pxd'], 50, 8); x, y, _ = cam.proj(*R.ll(35.69, 139.64))
glow = Image.new('RGBA', im.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow); gd.ellipse([x - 60, y - 34, x + 60, y + 34], fill=(255, 200, 60, 230))
im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(22)))
gd = ImageDraw.Draw(im); gd.ellipse([x - 16, y - 16, x + 16, y + 16], fill=(255, 235, 160), outline=(30, 20, 10), width=4)
box(im, 'रेंकोजी मंदिर, टोक्यो', 34, x - 40, y + 30, bg=(15, 12, 10), center=True)
person(im, 'uniform', 700, 20, H + 20, halo=(255, 200, 90))
text(im, '80 साल से', 104, (W - 340, 110), fill=(255, 255, 255), stroke=10)
text(im, 'रखी अस्थियाँ', 112, (W - 340, 230), fill=(255, 214, 60), stroke=11)
box(im, 'DNA टेस्ट कब?', 60, W - 340, H - 140, center=True)
save(im, 'Netaji_Thumb5_80_saal_asthiyan.jpg')
