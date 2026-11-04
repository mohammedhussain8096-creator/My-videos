"""Five thumbnails in the style of the user's reference: a big figure on the left, a political map with
pastel neighbours, Russia in bright red and serif country labels."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render, guide
from render import W, H, crop_map, draw_fills, to_screen, view_of
from render_text import font
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'thumbnails'); os.makedirs(OUT, exist_ok=True)
render.COLORS.update({'p_red': (232, 28, 28), 'p_green': (120, 190, 90), 'p_yellow': (238, 205, 90), 'p_orange': (236, 165, 80),
                      'p_lgreen': (170, 205, 110), 'p_peach': (240, 190, 140), 'p_teal': (110, 190, 160), 'p_pink': (225, 150, 160)})
NEIGH = [('Finland', 'p_green'), ('Norway', 'p_lgreen'), ('Sweden', 'p_yellow'), ('Estonia', 'p_orange'), ('Latvia', 'p_lgreen'),
         ('Lithuania', 'p_yellow'), ('Belarus', 'p_teal'), ('Ukraine', 'p_yellow'), ('Poland', 'p_peach'), ('Moldova', 'p_green'),
         ('Romania', 'p_lgreen'), ('Turkey', 'p_peach'), ('Georgia', 'p_orange'), ('Armenia', 'p_yellow'), ('Azerbaijan', 'p_green'),
         ('Kazakhstan', 'p_orange'), ('Uzbekistan', 'p_lgreen'), ('Turkmenistan', 'p_yellow'), ('Kyrgyzstan', 'p_green'),
         ('Tajikistan', 'p_peach'), ('Afghanistan', 'p_yellow'), ('Iran', 'p_lgreen'), ('Mongolia', 'p_lgreen'), ('China', 'p_yellow'),
         ('North Korea', 'p_orange'), ('South Korea', 'p_green'), ('Japan', 'p_lgreen'), ('Pakistan', 'p_peach'), ('India', 'p_orange'),
         ('Germany', 'p_lgreen'), ('Slovakia', 'p_yellow'), ('Hungary', 'p_green'), ('Czechia', 'p_orange')]
LABELS = [('FINLAND', (63.5, 26.5)), ('UKRAINE', (49.0, 31.5)), ('KAZAKHSTAN', (48.0, 67.0)), ('MONGOLIA', (46.5, 103.0)),
          ('CHINA', (35.0, 103.0)), ('JAPAN', (37.0, 139.5))]

def map_bg(view):
    cam = view_of(view)
    fr = crop_map(*cam)
    a = np.asarray(fr).astype(np.float32)
    water = (a[..., 2] > a[..., 0] + 25) & (a[..., 2] > a[..., 1] + 10)
    a[water] = a[water] * 1.25 + np.array([10, 30, 50])                     # brighter ocean like the reference
    a[~water] = a[~water] * 1.35
    fr = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    fr = draw_fills(fr, cam, [(n, c, 0.95) for n, c in NEIGH] + [('Russia', 'p_red', 1.0)])
    fr = ImageEnhance.Color(fr).enhance(1.25).convert('RGBA')
    d = ImageDraw.Draw(fr)
    f = font('baskerville', 30)
    for t, (la, lo) in LABELS:
        x, y = to_screen((la, lo), cam)
        if 40 < x < W - 40 and 40 < y < H - 40:
            l, tp, r, b = f.getbbox(t)
            d.text((x - (r - l) / 2, y), t, font=f, fill=(55, 40, 30), stroke_width=2, stroke_fill=(250, 240, 220))
    return fr, cam

def russia_word(fr, cam, at=(64.0, 100.0), size=150, spacing=0.5):
    f = font('cinzel', size)
    x, y = to_screen(at, cam)
    word = 'RUSSIA'
    widths = [f.getlength(ch) for ch in word]
    total = sum(widths) + spacing * size * (len(word) - 1)
    layer = Image.new('RGBA', fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    cx = x - total / 2
    for ch, w in zip(word, widths):
        d.text((cx, y - size * 0.6), ch, font=f, fill=(250, 238, 215))
        cx += w + spacing * size
    sh = layer.copy(); sh = Image.composite(Image.new('RGBA', fr.size, (60, 0, 0, 200)), Image.new('RGBA', fr.size, (0, 0, 0, 0)), layer.getchannel('A'))
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    fr.alpha_composite(sh, (5, 7)); fr.alpha_composite(layer)

def figure(fr, path, height, x, crop=None, bottom=True):
    im = Image.open(path).convert('RGBA')
    if crop: im = im.crop((int(crop[0] * im.width), int(crop[1] * im.height), int(crop[2] * im.width), int(crop[3] * im.height)))
    k = height / im.height
    im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    # soft dark halo for separation from the map
    halo = Image.new('RGBA', im.size, (0, 0, 0, 0)); halo.putalpha(im.getchannel('A').point(lambda v: int(v * 0.7)))
    halo = halo.filter(ImageFilter.GaussianBlur(18))
    y = H - im.height if bottom else 0
    fr.alpha_composite(halo, (int(x) + 10, int(y) + 6)); fr.alpha_composite(im, (int(x), int(y)))

def guide_fig(fr, h=1000, x=380):
    g, (fx, fy) = guide.pose(h, 0, 0)
    halo = Image.new('RGBA', g.size, (0, 0, 0, 0)); halo.putalpha(g.getchannel('A').point(lambda v: int(v * 0.6)))
    fr.alpha_composite(halo.filter(ImageFilter.GaussianBlur(16)), (int(x - fx) + 8, int(H + 330 - fy)))
    fr.alpha_composite(g, (int(x - fx), int(H + 330 - fy)))

def save(fr, name):
    fr.convert('RGB').resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, name), quality=95); print('wrote', name)

C = os.path.join(HERE, 'assets', 'cutouts')
V = (54.0, 88.0, 140)
fr, cam = map_bg(V); russia_word(fr, cam); figure(fr, f'{C}/napoleon_study.png', 1450, 20, crop=(0, 0, 1, 0.62)); save(fr, 'ref_1_napoleon.jpg')
fr, cam = map_bg(V); russia_word(fr, cam); figure(fr, f'{C}/napoleon_alps.png', 1000, -40, crop=(0, 0, 1, 0.82)); save(fr, 'ref_2_napoleon_horse.jpg')
fr, cam = map_bg(V); russia_word(fr, cam); figure(fr, f'{C}/peter.png', 1150, -60, crop=(0, 0, 0.78, 0.72)); save(fr, 'ref_3_peter_the_great.jpg')
fr, cam = map_bg(V); russia_word(fr, cam); figure(fr, f'{C}/kutuzov.png', 1250, -30, crop=(0, 0, 1, 0.75)); save(fr, 'ref_4_kutuzov.jpg')
fr, cam = map_bg(V); russia_word(fr, cam); guide_fig(fr); save(fr, 'ref_5_guide.jpg')
