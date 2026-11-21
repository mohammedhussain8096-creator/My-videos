"""7 thumbnails (1920x1080) in the style of the user's reference thumbnails, for title 2 ("दिल का दौरा या कुछ और?"):
dark red grunge background, a newspaper clipping, a collage of real 1965 public-domain photos with a red arrow to Shastri,
a map tag for Tashkent, a red brush-stroke banner behind big text, and a large warm-toned portrait on the right.
Only our own public-domain / CC0 photos are used, and the text only asks questions (no accusation).  -> ../thumbnails/Shastri_REF*.jpg"""
import os, sys, io, contextlib, math
os.environ['RES'] = '1920x1080'
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import render as R
from render import W, H, font
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
OUT = os.path.join(HERE, '..', 'thumbnails'); os.makedirs(OUT, exist_ok=True)
PH = lambda n: os.path.join(HERE, 'assets', 'photos', n + '.jpg')
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
rng0 = np.random.default_rng(3)

def noise(w, h, sc, seed):
    r = np.random.default_rng(seed)
    return np.asarray(Image.fromarray(r.normal(128, 60, (max(2, h // sc), max(2, w // sc))).clip(0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255

def grunge_bg(base=(46, 38, 30), seed=1):
    n1, n2, n3 = noise(W, H, 60, seed), noise(W, H, 8, seed + 1), noise(W, H, 2, seed + 2)
    a = np.array(base, np.float32) * (0.6 + 0.65 * n1[..., None]) * (0.85 + 0.3 * n2[..., None])
    a += (n3[..., None] - 0.5) * 26                                               # film grain
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')
    news = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(news); r = np.random.default_rng(seed)
    for col in range(8):                                                          # faint newspaper columns
        x0 = 40 + col * 240
        for row in range(70):
            if r.random() < 0.85: d.line([x0, 20 + row * 15, x0 + 200 - int(r.random() * 40), 20 + row * 15], fill=(200, 185, 160, 26), width=5)
    im.alpha_composite(news.rotate(-4, resample=Image.BICUBIC))
    sc = (np.random.default_rng(seed).random((H, W)) > 0.9985).astype(np.float32)
    a = np.asarray(im.convert('RGB'), np.float32) + np.asarray(Image.fromarray((sc * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1)), np.float32)[..., None] * 0.6
    rr = np.sqrt(((xx / W - 0.5) / 0.6) ** 2 + ((yy / H - 0.5) / 0.6) ** 2); a *= (1 - 0.6 * np.clip(rr - 0.45, 0, 1))[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')

def bw(img, contrast=1.3, tint=(250, 240, 222)):
    g = np.asarray(ImageEnhance.Contrast(img.convert('L')).enhance(contrast), np.float32)[..., None] / 255
    return Image.fromarray((g * np.array(tint, np.float32)).clip(0, 255).astype(np.uint8))

def soft_paste(im, ph, x, y, feather=60, alpha=1.0, red=0.0):
    ph = ph.convert('RGB')
    if red:
        a = np.asarray(ph, np.float32); g = a.mean(axis=2, keepdims=True); a = a * (1 - red) + g * np.array([1.0, 0.45, 0.4]) * red; ph = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    m = Image.new('L', ph.size, 0); ImageDraw.Draw(m).rectangle([feather, feather, ph.width - feather, ph.height - feather], fill=int(255 * alpha))
    m = m.filter(ImageFilter.GaussianBlur(feather * 0.6)); p = ph.convert('RGBA'); p.putalpha(m); im.alpha_composite(p, (int(x), int(y)))

def colourise(img):
    """warm hand-tinted look: shadows brown, mid-tones skin, highlights stay near white"""
    g = np.asarray(ImageEnhance.Contrast(img.convert('L')).enhance(1.4), np.float32)[..., None] / 255
    g = g ** 1.1
    lo, mid, hi = np.array([22, 20, 18], np.float32), np.array([168, 140, 118], np.float32), np.array([242, 240, 234], np.float32)
    out = np.where(g < 0.55, lo + (mid - lo) * (g / 0.55), mid + (hi - mid) * ((g - 0.55) / 0.45))
    gray = g * 255
    out = out * 0.75 + gray * 0.25                                         # keep it natural, not orange
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))

def portrait(im, h, x, yb, glow=(0, 0, 0)):
    """Shastri cut out (assets/cut/shastri_face_cut.png), warm-toned, red rim glow, fading out at the bottom"""
    p = Image.open(os.path.join(HERE, 'assets', 'cut', 'shastri_face_cut.png')).convert('RGBA')
    k = h / p.height; p = p.resize((int(p.width * k), h), Image.LANCZOS)
    A = np.asarray(p.getchannel('A'), np.float32) * np.clip((1 - np.linspace(0, 1, h)[:, None]) / 0.25, 0, 1)
    A = Image.fromarray(A.astype(np.uint8))
    c = colourise(p.convert('RGB')).filter(ImageFilter.UnsharpMask(2, 90, 2))
    pad = 160; Ab = Image.new('L', (p.width + 2 * pad, p.height + 2 * pad), 0); Ab.paste(A, (pad, pad))
    for blur, mul in ((40, 0.8), (12, 0.6)):                              # soft dark shadow around him
        gl = Image.new('RGBA', Ab.size, glow + (0,)); gl.putalpha(Ab.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(min(255, v * mul))))
        gx, gy = int(x) - pad, int(yb - h) - pad
        im.alpha_composite(gl.crop((max(0, -gx), max(0, -gy), gl.width, gl.height)), (max(0, gx), max(0, gy)))
    ci = c.convert('RGBA'); ci.putalpha(A); im.alpha_composite(ci, (int(x), int(yb - h)))

def clipping(lines, w=640, h=520, rot=8):
    """generic newspaper clipping (no real paper's name): headline + grey text columns, torn edges"""
    rng = np.random.default_rng(len(lines[0]))
    p = np.ones((h, w, 3), np.float32) * np.array([222, 212, 188], np.float32) * (0.85 + 0.2 * noise(w, h, 10, 5)[..., None])
    pg = Image.fromarray(p.clip(0, 255).astype(np.uint8)).convert('RGBA'); d = ImageDraw.Draw(pg)
    y = 26
    for i, ln in enumerate(lines):
        t = R.text_img(ln, 'bold', 64 if i == 0 else 46, fill=(25, 20, 18), shadow=False, maxw=int(w / R.U) - 60)
        pg.alpha_composite(t, (24, y - 20)); y += t.height - 24
    d.line([24, y + 8, w - 24, y + 8], fill=(40, 35, 30, 255), width=3)
    for col in range(3):
        cx0 = 24 + col * (w - 48) // 3
        for row in range(int((h - y - 40) / 18)):
            ll = (w - 48) // 3 - 18 - int(rng.random() * 30)
            d.line([cx0, y + 30 + row * 18, cx0 + ll, y + 30 + row * 18], fill=(90, 85, 78, 200), width=6)
    m = Image.new('L', (w, h), 0); dm = ImageDraw.Draw(m)
    edge = [(i, 6 + rng.random() * 14) for i in range(0, w + 20, 20)] + [(w - 6 - rng.random() * 14, j) for j in range(0, h + 20, 20)][::-1]
    dm.rectangle([8, 8, w - 8, h - 8], fill=255)
    for i in range(0, w, 14): dm.ellipse([i - 9, h - 18 - rng.random() * 12, i + 9, h + 9], fill=0)
    pg.putalpha(m.filter(ImageFilter.GaussianBlur(1.5)))
    return pg.rotate(rot, expand=True, resample=Image.BICUBIC)

def brush(w, h, col=(214, 22, 22), seed=0):
    rng = np.random.default_rng(seed); m = Image.new('L', (w, h), 0); d = ImageDraw.Draw(m)
    for i in range(70):                                   # overlapping rough strokes
        y0 = h * (0.12 + 0.76 * rng.random()); t = h * (0.12 + 0.12 * rng.random())
        d.rectangle([w * 0.02 * rng.random(), y0 - t / 2, w * (0.94 + 0.06 * rng.random()), y0 + t / 2], fill=255)
    n = noise(w, h, 3, seed + 9); a = np.asarray(m.filter(ImageFilter.GaussianBlur(2)), np.float32) * (0.75 + 0.35 * n)
    xr = np.linspace(0, 1, w)[None, :]; a *= np.clip(np.minimum(xr / 0.04, (1 - xr) / 0.08), 0, 1) ** 0.6   # ragged ends
    b = Image.new('RGBA', (w, h), col + (0,)); b.putalpha(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))); return b

def bigtext(im, s, size, xy, fill=(255, 255, 255), stroke=14, anchor='lm', distress=True):
    f = font('bold', size)
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).text(xy, s, font=f, fill=255, anchor=anchor)
    ms = Image.new('L', (W, H), 0); ImageDraw.Draw(ms).text(xy, s, font=f, fill=255, anchor=anchor, stroke_width=stroke)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(ms.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.85))); im.alpha_composite(sh, (8, 12))
    st = Image.new('RGBA', (W, H), (10, 8, 8, 0)); st.putalpha(ms); im.alpha_composite(st)
    a = np.asarray(m, np.float32)
    if distress: a *= np.where(np.random.default_rng(size).random((H, W)) < 0.025, 0.25, 1.0)
    fi = Image.new('RGBA', (W, H), fill + (0,)); fi.putalpha(Image.fromarray(a.astype(np.uint8))); im.alpha_composite(fi)
    return m.getbbox()

def banner_text(im, s, size, x, y, col=(214, 22, 22), text_col=(255, 255, 255), seed=0):
    f = font('bold', size); l, t, r, b = f.getbbox(s)
    bw_, bh_ = (r - l) + 140, (b - t) + 70
    im.alpha_composite(brush(bw_, bh_, col, seed), (int(x - 50), int(y - 20)))
    bigtext(im, s, size, (x + 20, y + bh_ / 2 - 32), fill=text_col, stroke=10)

def tag(im, s, x, y, size=40):
    t = R.text_img(s, 'bold', size, fill=(20, 20, 20), shadow=False); bb = t.getchannel('A').getbbox(); t = t.crop(bb)
    w_, h_ = t.width + 36, t.height + 26
    d = ImageDraw.Draw(im); d.rectangle([x, y, x + w_, y + h_], fill=(250, 220, 90, 255)); d.polygon([(x + 30, y + h_), (x + 50, y + h_), (x + 40, y + h_ + 16)], fill=(250, 220, 90, 255))
    im.alpha_composite(t, (int(x + 18), int(y + 13)))

def arrow(im, p0, p1, col=(225, 25, 25), width=26):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0]); L = width * 2.6
    tip = p1; base = (p1[0] - L * math.cos(ang), p1[1] - L * math.sin(ang))
    for c, wd in (((0, 0, 0, 170), width + 10), (col + (255,), width)):
        d.line([p0, base], fill=c, width=wd)
        d.polygon([tip, (base[0] + L * 0.6 * math.cos(ang + 1.57), base[1] + L * 0.6 * math.sin(ang + 1.57)), (base[0] + L * 0.6 * math.cos(ang - 1.57), base[1] + L * 0.6 * math.sin(ang - 1.57))], fill=c)
    im.alpha_composite(lay)

def map_patch(view=(39.0, 71.0, 18.0), w=900, h=560):
    sp = dict(view=view, pitch=40, yaw0=0, yaw1=0, fill=[('uzbek', 'red', -9)], routes=[dict(pts=[(28.61, 77.21), (41.31, 69.24)], at=0, dur=0.1, icon='plane', col='gold')])
    m = R.draw_map(sp, 4.0, 4.0).resize((w, int(w * H / W)), Image.LANCZOS).crop((0, 0, w, h))
    a = np.asarray(m, np.float32) * 0.92
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))

def save(im, name):
    p = os.path.join(OUT, name); im.convert('RGB').save(p, quality=93, subsampling=0); print('wrote', name, os.path.getsize(p) // 1024, 'KB')

SAY = Image.open(PH('shastri_sayeed')).convert('RGB')          # Shastri front-left, 1965
OFF = Image.open(os.path.join(HERE, 'assets', 'photos_hd', 'shastri_1965.jpg')).convert('RGB')   # with army officers, 1965
NEH = Image.open(PH('nehru_shastri')).convert('RGB')

def collage_left(im, red=0.0):
    soft_paste(im, bw(SAY.crop((0, 120, 1500, 1440)).resize((900, 792), Image.LANCZOS)), -40, 220, feather=70, alpha=0.95, red=red)
    soft_paste(im, bw(OFF.resize((760, 558), Image.LANCZOS)), 560, 520, feather=60, alpha=0.9, red=red)

# REF1  "दिल का दौरा?" on a red brush + "या कुछ और?"
im = grunge_bg(seed=1)
cl = clipping(['प्रधानमंत्री शास्त्री का निधन', 'ताशकंद में दिल का दौरा'], rot=7); im.alpha_composite(cl, (W - 760, -40))
collage_left(im)
arrow(im, (520, 470), (410, 600))
portrait(im, 1000, W - 820, H + 30)
banner_text(im, 'दिल का दौरा?', 190, 50, 30, seed=1)
bigtext(im, 'या कुछ और?', 230, (60, H - 150), fill=(255, 220, 60))
save(im, 'Shastri_REF1_dil_ka_daura.jpg')

# REF2  map + "ताशकंद" tag, "शास्त्री जी की मौत का सच?"
im = grunge_bg(seed=2)
soft_paste(im, map_patch(), 560, 300, feather=80, alpha=0.95)
tag(im, 'ताशकंद', 870, 380)
collage_left(im)
portrait(im, 1060, W - 860, H + 20)
banner_text(im, 'शास्त्री जी की मौत', 165, 50, 25, seed=2)
bigtext(im, 'का सच?', 240, (70, 350), fill=(255, 220, 60))
save(im, 'Shastri_REF2_maut_ka_sach.jpg')

# REF3  "आख़िरी 24 घंटे"
im = grunge_bg(seed=3)
collage_left(im)
arrow(im, (560, 430), (420, 590))
portrait(im, 1040, W - 860, H + 40)
bigtext(im, 'शास्त्री जी के', 120, (60, H - 330), fill=(255, 255, 255))
bigtext(im, 'आख़िरी 24 घंटे', 230, (40, H - 140), fill=(235, 30, 30))
tag(im, 'ताशकंद, 10–11 जनवरी 1966', 60, 50, size=44)
save(im, 'Shastri_REF3_aakhiri_24_ghante.jpg')

# REF4  "पोस्टमार्टम क्यों नहीं?"
im = grunge_bg(seed=4)
cl = clipping(['पोस्टमार्टम नहीं', 'न ताशकंद में, न दिल्ली में'], rot=-6); im.alpha_composite(cl, (60, 360))
soft_paste(im, bw(NEH.resize((480, 518), Image.LANCZOS)), 720, 430, feather=50, alpha=0.85)
portrait(im, 1060, W - 860, H + 20)
banner_text(im, 'पोस्टमार्टम', 200, 50, 30, seed=4)
bigtext(im, 'क्यों नहीं?', 210, (70, 340), fill=(255, 220, 60))
save(im, 'Shastri_REF4_postmortem.jpg')

# REF5  "शरीर नीला क्यों?"
im = grunge_bg(seed=5)
collage_left(im)
portrait(im, 1060, W - 860, H + 20)
banner_text(im, 'शरीर नीला क्यों?', 185, 50, 30, col=(30, 70, 200), seed=5)
bigtext(im, 'परिवार का सवाल', 130, (80, H - 120), fill=(255, 255, 255))
save(im, 'Shastri_REF5_sharir_neela.jpg')

# REF6  "गुप्त फ़ाइल में क्या है?"
im = grunge_bg(seed=6)
cl = clipping(['गोपनीय', 'शास्त्री जी की मौत से जुड़ा दस्तावेज़'], rot=-8); im.alpha_composite(cl, (80, 380))
st = R.stamp_img('गुप्त', (220, 25, 25), 160); im.alpha_composite(st, (300, 620))
portrait(im, 1060, W - 860, H + 20)
banner_text(im, 'गुप्त फ़ाइल', 200, 50, 30, seed=6)
bigtext(im, 'में क्या है?', 210, (70, 340), fill=(255, 220, 60))
save(im, 'Shastri_REF6_gupt_file.jpg')

# REF7  "रात 1:32" with the clock
im = grunge_bg(seed=7)
cimg = Image.new('RGB', (W, H)); R.draw_clock(cimg, 4.0, dict(hm=(1, 31), sec0=50))
soft_paste(im, cimg.crop((560, 60, 1360, 960)).resize((600, 675), Image.LANCZOS), 560, 280, feather=70, alpha=0.95)
collage_left(im)
portrait(im, 1060, W - 860, H + 20)
banner_text(im, 'रात 1:32', 210, 50, 30, seed=7)
bigtext(im, 'ताशकंद में क्या हुआ?', 140, (50, H - 120), fill=(255, 220, 60))
save(im, 'Shastri_REF7_raat_1_32.jpg')
