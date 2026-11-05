"""Five YouTube thumbnails (1280x720) built from the video's own scenes, the guide and bold text."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render, guide, cartoon
from render import Scene, W, H
from render_text import text_img
from PIL import Image, ImageEnhance, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'thumbnails'); os.makedirs(OUT, exist_ok=True)
COL = {'yellow': ((255, 232, 92), (248, 176, 36), (60, 30, 4)), 'red': ((250, 100, 60), (222, 50, 28), (70, 12, 6)),
       'white': ((255, 255, 255), (230, 230, 236), (30, 22, 18))}

def base(spec):
    s = Scene(dict(scene=999, start=0.0, end=60.0), dict(spec, guide=False), None)
    s.wt = []
    for it in s.items: it['t0'] = -9
    s.caps = []; s.shakes = []
    return s.frame(30.0).convert('RGBA')

def big(im, text, x, y, size=200, col='yellow', anchor='center', maxw=None):
    c = COL[col]
    t = text_img(text, 'fredoka', size, None, c[2], max(10, size // 11), gradient=(c[0], c[1]))
    if maxw and t.width > maxw: t = t.resize((maxw, int(t.height * maxw / t.width)), Image.LANCZOS)
    xx = x - t.width / 2 if anchor == 'center' else x
    im.alpha_composite(t, (int(xx), int(y - t.height / 2)))

def put_guide(im, x=W - 300, h=760, spear=14, lean=3):
    g, (fx, fy) = guide.pose(h, spear, lean)
    halo = Image.new('RGBA', g.size, (0, 0, 0, 0)); halo.putalpha(g.getchannel('A').point(lambda v: int(v * 0.5)))
    im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(14)), (int(x - fx) + 8, int(H + 40 - fy) + 6))
    im.alpha_composite(g, (int(x - fx), int(H + 40 - fy)))

def save(im, name):
    im = ImageEnhance.Contrast(ImageEnhance.Color(im.convert('RGB')).enhance(1.15)).enhance(1.06)
    im.resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, name), quality=95); print('wrote', name)

P = render.SCENES
S = lambda x, y: ('s', x, y)
# 1) 1453: How a 21-Year-Old Sultan Took Constantinople  -> THE UNTHINKABLE
im = base(dict(bg='scene', sky='night', clouds=0, items=[*P[23]['items'][:6],
              *[dict(k='fire', at_place=S(x, y), size=1.6, n=5) for x, y in ((0.2, 0.62), (0.5, 0.5), (0.78, 0.64))]]))
card = render.photo_card('mehmed_bellini', 700, None)
im.alpha_composite(card, (40, 20))
big(im, '1453', 1180, 250, 260, 'yellow'); big(im, 'THE UNTHINKABLE', 1210, 880, 150, 'red', maxw=1250)
save(im, 'thumb_1_the_unthinkable.jpg')

# 2) The City 24 Sieges Couldn't Break: Istanbul  -> IMPOSSIBLE WALLS
im = base(dict(bg='scene', items=[dict(k='prop', kind='wall', xy=(0.5, 0.92), h=620, kw={'length': 3}),
              dict(k='prop', kind='siege_tower', xy=(0.18, 0.99), h=520), dict(k='prop', kind='fig-hun', xy=(0.33, 1.0), h=300),
              dict(k='prop', kind='fig-arab', xy=(0.43, 1.0), h=300)]))
big(im, 'IMPOSSIBLE', 820, 150, 210, 'yellow', maxw=1500); big(im, 'WALLS', 820, 340, 200, 'white')
put_guide(im); save(im, 'thumb_2_impossible_walls.jpg')

# 3) 70 Warships Dragged Over a Mountain in One Night  -> SHIPS ON LAND?
im = base(dict(bg='scene', sky='night', ground='grass', clouds=0, horizon=0.62,
              items=[dict(k='prop', kind='logs', xy=(0.45, 0.99), h=110, kw={'length': 16}), dict(k='prop', kind='galley', xy=(0.47, 0.93), h=420),
                     *[dict(k='prop', kind='ox', xy=(0.06 + i * 0.1, 1.0), h=150) for i in range(2)]]))
big(im, 'SHIPS ON', 900, 160, 200, 'yellow'); big(im, 'LAND?!', 900, 350, 220, 'red')
put_guide(im, spear=18, lean=4); save(im, 'thumb_3_ships_on_land.jpg')

# 4) Why Constantinople's Walls Held for 1,000 Years  -> NO ENTRY
im = base(dict(bg='scene', items=[dict(k='prop', kind='wall', xy=(0.5, 0.86), h=560, kw={'length': 3}),
              *[dict(k='prop', kind='fig-' + f, xy=(x, 1.0), h=320) for f, x in (('hun', 0.15), ('persian', 0.32), ('arab', 0.49), ('crusader', 0.66))]]))
x = render.icons.get('xmark', 520); im.alpha_composite(x, (int(W * 0.42 - x.width / 2), int(H * 0.56 - x.height / 2)))
big(im, 'NO ENTRY', 960, 150, 230, 'yellow')
put_guide(im); save(im, 'thumb_4_no_entry.jpg')

# 5) Byzantium, Constantinople, Istanbul: One City, 3 Empires  -> THE PRIZE
im = base(dict(bg='spot', items=[dict(k='prop', kind='pedestal', xy=(0.6, 0.97), h=680),
              dict(k='prop', kind='fig-pope', xy=(0.12, 1.0), h=620, say='Mine!', ss=72), dict(k='prop', kind='fig-sultan', xy=(0.28, 1.0), h=620, say='MINE!', ss=72),
              dict(k='prop', kind='fig-king', xy=(0.9, 1.0), h=620, say='No, mine!', ss=72)]))
big(im, 'THE PRIZE', 1190, 130, 200, 'yellow')
save(im, 'thumb_5_the_prize.jpg')
