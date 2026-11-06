"""Ottoman thumbnails in the style of the user's reference: bright terrain map with white borders, the country
in glowing red, black label boxes top-left, and a large figure on the right."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('RES', '1280x720')
import render, guide
from render import W, H, crop_map, view_of, to_screen_arr, proj_rings, polys
from render_text import font
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'thumbnails')

def map_bg(view, red='EMPIRE'):
    cam = view_of(view)
    fr = crop_map(*cam)
    a = np.asarray(fr).astype(np.float32)
    water = (a[..., 2] > a[..., 0] + 30) & (a[..., 2] > a[..., 1] + 10)
    g = np.asarray(ImageEnhance.Contrast(ImageEnhance.Color(fr).enhance(1.6)).enhance(1.35)).astype(np.float32)
    g[water] = np.array([20, 110, 235], np.float32) * (0.55 + 0.6 * a[water].mean(axis=1, keepdims=True) / 255) + 20
    fr = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).convert('RGBA')
    names = json.load(open(os.path.join(render.ASSETS, 'countries.json'))).keys()
    bl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(bl)
    for n in names:                       # thin white borders, like the reference
        for r in proj_rings(n):
            x, y = to_screen_arr(r, cam)
            if x.max() < 0 or x.min() > W or y.max() < 0 or y.min() > H: continue
            bd.line(list(zip(x.tolist(), y.tolist())), fill=(255, 255, 255, 150), width=1)
    fr.alpha_composite(bl)
    # the highlighted country: deep red fill keeping the relief, glowing white outline
    m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m)
    for r in proj_rings(red):
        x, y = to_screen_arr(r, cam); md.polygon(list(zip(x.tolist(), y.tolist())), fill=255)
    arr = np.asarray(fr).astype(np.float32); mf = np.asarray(m, np.float32)[..., None] / 255
    lum = arr[..., :3].mean(axis=2, keepdims=True) / 255
    redc = np.array([235, 20, 20], np.float32) * (0.55 + 0.7 * lum)
    arr[..., :3] = arr[..., :3] * (1 - mf) + redc * mf
    fr = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    edge = ImageChops.subtract(m.filter(ImageFilter.MaxFilter(7)), m.filter(ImageFilter.MinFilter(3)))
    glow = Image.new('RGBA', (W, H), (255, 70, 60, 0)); glow.putalpha(edge.filter(ImageFilter.GaussianBlur(9)))
    fr.alpha_composite(glow); fr.alpha_composite(glow)
    line = Image.new('RGBA', (W, H), (255, 255, 255, 0)); line.putalpha(ImageChops.subtract(m.filter(ImageFilter.MaxFilter(5)), m))
    fr.alpha_composite(line)
    return fr, cam

def box(im, text, x, y, size):
    f = font('nunito', size); l, t, r, b = f.getbbox(text)
    pad = int(size * 0.28)
    d = ImageDraw.Draw(im); d.rectangle([x, y, x + (r - l) + 2 * pad, y + (b - t) + 2 * pad], fill=(10, 10, 10, 255))
    d.text((x + pad - l, y + pad - t), text, font=f, fill=(255, 255, 255))
    return y + (b - t) + 2 * pad

def pin(im, cam, lat, lon, label):
    x, y = render.to_screen((lat, lon), cam); d = ImageDraw.Draw(im)
    for r, c in ((26, (255, 255, 255, 120)), (14, (255, 255, 255, 255)), (9, (255, 200, 40, 255))):
        d.ellipse([x - r, y - r, x + r, y + r], fill=c)
    f = font('nunito', 34); l, t, rr, b = f.getbbox(label)
    d.text((x - (rr - l) / 2, y + 28), label, font=f, fill=(255, 255, 255), stroke_width=6, stroke_fill=(15, 15, 15))

def figure(im, name='suleiman_cut.png', h=690, x_right=1300):
    m = Image.open(os.path.join(HERE, 'assets', name)).convert('RGBA')
    m = m.crop((0, 0, int(m.width * 0.97), int(m.height * 0.96)))
    k = h / m.height; m = m.resize((int(m.width * k), h), Image.LANCZOS)
    a = np.asarray(m.getchannel('A')).astype(np.float32)
    fade = np.clip(np.arange(m.width) / (m.width * 0.16), 0, 1)[None, :]        # soften the cut on the left
    m.putalpha(Image.fromarray((a * fade).astype(np.uint8)))
    m = ImageEnhance.Contrast(ImageEnhance.Color(m).enhance(1.25)).enhance(1.12)
    halo = Image.new('RGBA', m.size, (255, 255, 255, 0)); halo.putalpha(m.getchannel('A').filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(10)))
    im.alpha_composite(halo, (x_right - m.width, H - m.height + 6)); im.alpha_composite(m, (x_right - m.width, H - m.height + 6))

def save(im, name):
    im.convert('RGB').save(os.path.join(OUT, name), quality=95); print('wrote', name)


from plan import GROUPS, CUSTOM
from plan2 import _clip
def _north(name, lat_min):          # Ottoman rule in North Africa was the coast, not the Sahara
    def f(P):
        out = []
        for r in P[name]:
            c = _clip([(-la, lo) for lo, la in r], -lat_min)
            if len(c) > 3: out.append([(lo, -nla) for nla, lo in c])
        return out
    return f
for n in ('Algeria', 'Tunisia', 'Libya'): CUSTOM['N_' + n] = _north(n, 29.5)
GROUPS['EMPIRE'] = [c for c in GROUPS['PEAK'] if c not in ('Algeria', 'Tunisia', 'Libya')] + ['N_Algeria', 'N_Tunisia', 'N_Libya', 'HEJAZ']
V = (36.5, 28.5, 70)
def base():
    return map_bg(V)          # no city pin: the thumbnail is about the whole empire
# 1. OTTOMAN EMPIRE / 1299 - 1922 + Suleiman
im, cam = base(); figure(im)
y = box(im, 'OTTOMAN EMPIRE', 24, 18, 84); box(im, '1299 - 1922', 24, y + 10, 62); save(im, 'ref_1_ottoman_1299_1922.jpg')
# 2. OTTOMAN EMPIRE / 600 YEARS + Mehmed II
im, cam = base(); figure(im, 'mehmed_cut.png')
y = box(im, 'OTTOMAN EMPIRE', 24, 18, 84); box(im, '600 YEARS', 24, y + 10, 62); save(im, 'ref_2_ottoman_600_years.jpg')
# 3. OTTOMAN EMPIRE / RISE & FALL + the guide
im, cam = base()
g, (fx, fy) = guide.pose(700, 12, 2)
halo = Image.new('RGBA', g.size, (255, 255, 255, 0)); halo.putalpha(g.getchannel('A').filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(8)))
im.alpha_composite(halo, (int(1110 - fx), int(H + 20 - fy))); im.alpha_composite(g, (int(1110 - fx), int(H + 20 - fy)))
y = box(im, 'OTTOMAN EMPIRE', 24, 18, 84); box(im, 'RISE & FALL', 24, y + 10, 62); save(im, 'ref_3_ottoman_rise_fall.jpg')
