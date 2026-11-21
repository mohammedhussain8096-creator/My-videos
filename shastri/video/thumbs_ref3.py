"""Thumbnail in the layout of the user's reference 3 (rebuilt from our own public-domain photos, not the reference image):
warm brown map background with a target, a tilted white-framed photo at the top, big two-line text on the left, large portrait
on the right. Text: 'LAST 24 HOURS OF SHASTRI JI' + a Hindi line.  -> ../thumbnails/Shastri_R3_*.jpg"""
import os, sys, io, contextlib
os.environ['RES'] = '1920x1080'
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import thumbs_ref as T
R, W, H = T.R, T.W, T.H
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

def base():
    sp = dict(view=(33.0, 72.5, 20.0), pitch=38, yaw0=-4, yaw1=-4, india_outline=True, pulse=[(41.31, 69.24, 0.0, 'red')])
    m = R.draw_map(sp, 4.0, 4.0)
    a = np.asarray(m, np.float32); g = a.mean(axis=2, keepdims=True)
    a = g * np.array([1.0, 0.78, 0.55]) * 0.85 + a * 0.15                      # warm sepia like the reference
    a *= (1 - 0.55 * np.clip(np.sqrt(((T.xx / W - 0.4) / 0.7) ** 2 + ((T.yy / H - 0.5) / 0.7) ** 2) - 0.35, 0, 1))[..., None]
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(im); cx, cy = 790, 330                                     # target on Tashkent side
    for r, wd in ((60, 8), (34, 7)): d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(210, 30, 30, 255), width=wd)
    d.line([cx - 90, cy, cx + 90, cy], fill=(210, 30, 30, 255), width=6); d.line([cx, cy - 90, cx, cy + 90], fill=(210, 30, 30, 255), width=6)
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(210, 30, 30, 255))
    tag = R.text_img('ताशकंद', 'bold', 40, fill=(30, 25, 20), shadow=False); bb = tag.getchannel('A').getbbox(); tag = tag.crop(bb)
    d.rectangle([cx + 70, cy - 70, cx + 70 + tag.width + 30, cy - 70 + tag.height + 22], fill=(250, 220, 90, 255)); im.alpha_composite(tag, (cx + 85, cy - 59))
    return im

def framed(img, w, rot):
    img = T.bw(img, 1.25).resize((w, int(w * img.height / img.width)), Image.LANCZOS)
    f = Image.new('RGBA', (img.width + 28, img.height + 28), (248, 246, 240, 255)); f.alpha_composite(img.convert('RGBA'), (14, 14))
    return f.rotate(rot, expand=True, resample=Image.BICUBIC)

def make(line2, name, col2=(255, 255, 255)):
    im = base()
    ph = framed(T.OFF, 620, 4); sh = Image.new('RGBA', ph.size, (0, 0, 0, 0)); sh.putalpha(ph.getchannel('A').point(lambda v: 150 if v else 0).filter(ImageFilter.GaussianBlur(14)))
    im.alpha_composite(sh, (820, 40)); im.alpha_composite(ph, (800, 20))
    T.portrait(im, 1120, W - 900, H + 40)
    T.bigtext(im, 'LAST 24 HOURS', 150, (50, 430), fill=(255, 255, 255), stroke=14)
    T.bigtext(im, 'OF SHASTRI JI', 150, (50, 600), fill=(255, 214, 60), stroke=14)
    T.banner_text(im, line2, 92, 50, 760, seed=3, text_col=col2)
    T.save(im, name)

make('शास्त्री जी को किसने मारा?', 'Shastri_R3_kisne_mara.jpg')
make('मौत या साज़िश? क्या हुआ था?', 'Shastri_R3_safe.jpg')

# ---- background variants (same layout and text)
def bg_night():                       # dark blue night over Tashkent with the vintage clock
    im = Image.new('RGBA', (W, H)); a = np.zeros((H, W, 3), np.float32)
    a[:] = np.array([8, 14, 30]); a += T._g if False else 0
    im = Image.fromarray(a.astype(np.uint8)).convert('RGBA')
    sp = dict(view=(41.3, 69.24, 9.0), pitch=55, yaw0=0, yaw1=0, fill=[('uzbek', 'gold', -9)], pulse=[(41.31, 69.24, 0.0, 'red')])
    m = np.asarray(R.draw_map(sp, 4.0, 4.0), np.float32) * np.array([0.35, 0.45, 0.75])
    im = Image.fromarray(m.clip(0, 255).astype(np.uint8)).convert('RGBA')
    c = Image.new('RGB', (W, H)); R.draw_clock(c, 4.0, dict(hm=(1, 31), sec0=50))
    T.soft_paste(im, c.crop((620, 110, 1300, 900)).resize((520, 604), Image.LANCZOS), 520, 360, feather=60, alpha=0.9)
    return im

def bg_newspaper():                   # dark charcoal with old newspaper clippings
    im = T.grunge_bg(base=(34, 32, 30), seed=11)
    for k, (txt, x, y, r) in enumerate([(['ताशकंद समझौता', 'भारत-पाक में शांति'], 380, -60, -8), (['प्रधानमंत्री का निधन', 'ताशकंद, 11 जनवरी'], 1250, 560, 6),
                                        (['पोस्टमार्टम नहीं', 'परिवार के सवाल'], 640, 640, -5)]):
        cl = T.clipping(txt, rot=r); a = np.asarray(cl, np.float32); a[..., :3] *= 0.75; im.alpha_composite(Image.fromarray(a.astype(np.uint8)), (x, y))
    return im

def bg_dotmap():                      # the video's dot-map background
    return R.card_bg_modern('dark', 2.0).convert('RGBA')

def bg_smoke():                       # black with orange-red smoke glow, cinematic
    n1, n2 = T.noise(W, H, 90, 21), T.noise(W, H, 30, 22)
    a = np.zeros((H, W, 3), np.float32) + 10
    glow = np.clip(1 - np.sqrt(((T.xx / W - 0.75) / 0.55) ** 2 + ((T.yy / H - 0.55) / 0.7) ** 2), 0, 1)
    a += (glow * (0.6 + 0.6 * n1) * (0.7 + 0.5 * n2))[..., None] * np.array([170, 70, 25])
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')

def make2(bgfn, line2, name):
    im = bgfn()
    ph = framed(T.OFF, 620, 4); sh = Image.new('RGBA', ph.size, (0, 0, 0, 0)); sh.putalpha(ph.getchannel('A').point(lambda v: 150 if v else 0).filter(ImageFilter.GaussianBlur(14)))
    im.alpha_composite(sh, (820, 40)); im.alpha_composite(ph, (800, 20))
    T.portrait(im, 1120, W - 900, H + 40)
    T.bigtext(im, 'LAST 24 HOURS', 150, (50, 430), fill=(255, 255, 255), stroke=14)
    T.bigtext(im, 'OF SHASTRI JI', 150, (50, 600), fill=(255, 214, 60), stroke=14)
    T.banner_text(im, line2, 92, 50, 760, seed=3)
    T.save(im, name)

L = 'शास्त्री जी को किसने मारा?'
make2(bg_night, L, 'Shastri_R3_bg1_raat.jpg')
make2(bg_newspaper, L, 'Shastri_R3_bg2_akhbaar.jpg')
make2(bg_dotmap, L, 'Shastri_R3_bg3_dotmap.jpg')
make2(bg_smoke, L, 'Shastri_R3_bg4_smoke.jpg')
