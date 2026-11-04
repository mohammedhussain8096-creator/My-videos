"""YouTube thumbnails (1280x720) built from the video's own map, icons and the guide character."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render, icons, guide
from render import Scene, W, H, U
from render_text import text_img
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'thumbnails')
os.makedirs(OUT, exist_ok=True)

def base(spec, t=30.0):
    sc = dict(scene=999, start=0.0, end=60.0)
    s = Scene(sc, dict(spec, guide=False, clouds=0.0), None)
    s.wt = []
    for it in s.items: it['t0'] = -9
    s.fills = [(f[0], f[1], -9) for f in s.fills]
    s.caps = []
    return s.frame(t).convert('RGBA')

def big_text(im, words, y, size=230, x=None, color='yellow'):
    g = ((255, 232, 92), (250, 168, 28)) if color == 'yellow' else ((255, 255, 255), (225, 225, 235))
    t = text_img(words, 'luckiest', size, None, (40, 18, 4), 16, gradient=g)
    if t.width > W * 0.9: t = t.resize((int(W * 0.9), int(t.height * W * 0.9 / t.width)), Image.LANCZOS)
    im.alpha_composite(t, (int((x if x is not None else (W - t.width) / 2)), int(y)))

def put_guide(im, h=760, x=None, spear=14, lean=3):
    g, (fx, fy) = guide.pose(h, spear, lean)
    xx = (W - 330) if x is None else x
    im.alpha_composite(g, (int(xx - fx), int(H + 10 - fy)))

def vignette(im, k=0.55):
    v = Image.new('L', (W, H), 0); d = ImageDraw.Draw(v)
    d.ellipse([-W * 0.25, -H * 0.3, W * 1.25, H * 1.3], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(160))
    dark = Image.new('RGBA', (W, H), (0, 0, 0, int(255 * k)))
    dark.putalpha(Image.eval(v, lambda p: int((255 - p) * k)))
    im.alpha_composite(dark)

def save(im, name):
    im = ImageEnhance.Contrast(ImageEnhance.Color(im.convert('RGB')).enhance(1.15)).enhance(1.08)
    im.resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, name), quality=95)
    print('wrote', name)

# 1) "600,000 Men Took Moscow and Still Lost. Why?"  -> burning Moscow, Napoleon, NOT THE WINTER
im = base(dict(view=(55.75, 37.0, 9), fill=[('RUSSIAN_EMPIRE', 'red')], tint='fire', year='1812',
               items=[render.SCENES[188]['items'][0]] + render.SCENES[188]['items'][2:]))
for dx, dy, s in ((-330, 40, 260), (-60, -40, 340), (230, 30, 280), (-520, 120, 200)):
    fl = icons.flame(s, 0.3); im.alpha_composite(fl, (int(W * 0.44 + dx - fl.width / 2), int(H * 0.47 + dy - fl.height * 0.8)))
c = icons.get('castle', 260); im.alpha_composite(c, (int(W * 0.44 - c.width / 2), int(H * 0.52 - c.height)))
b = icons.get('badge-napoleon', 300); im.alpha_composite(b, (60, 130))
vignette(im, 0.6)
big_text(im, 'NOT THE', 700, 190, x=60, color='white'); big_text(im, 'WINTER', 830, 250, x=60)
put_guide(im)
save(im, 'thumb_1_not_the_winter.jpg')

# 2) "The 5 Hidden Sources of Russian Power" -> all of Russia glowing, IMPOSSIBLE TO CONQUER
im = base(dict(view=(58.0, 95.0, 175), fill=[('Russia', 'red')], year='TODAY'))
cr = icons.get('crown', 230); im.alpha_composite(cr, (int(W * 0.47 - cr.width / 2), 170))
vignette(im, 0.5)
big_text(im, 'IMPOSSIBLE', 600, 230, x=50); big_text(im, 'TO CONQUER', 810, 170, x=60, color='white')
put_guide(im, h=740)
save(im, 'thumb_2_impossible_to_conquer.jpg')

# 3) "1812 and 1941: Why Napoleon and Hitler Lost in Russia" -> two invasion arrows, SAME MISTAKE
im = base(dict(view='europe_russia', fill=[('RUSSIAN_EMPIRE', 'red'), ('France', 'blue'), ('Germany', 'grey')],
               items=[render.SCENES[4]['items'][3], render.SCENES[4]['items'][5]]))
for who, x, y, lbl in (('badge-napoleon', 120, 120, '1812'), ('badge-hitler', 470, 120, '1941')):
    b = icons.get(who, 280); im.alpha_composite(b, (x, y))
    t = text_img(lbl, 'luckiest', 110, (255, 255, 255), (20, 20, 20), 10); im.alpha_composite(t, (int(x + 140 - t.width / 2), y + 270))
vs = text_img('=', 'luckiest', 200, (255, 214, 64), (40, 18, 4), 12); im.alpha_composite(vs, (395, 170))
vignette(im, 0.5)
big_text(im, 'SAME MISTAKE', 800, 210, x=50)
put_guide(im, h=740)
save(im, 'thumb_3_same_mistake.jpg')
