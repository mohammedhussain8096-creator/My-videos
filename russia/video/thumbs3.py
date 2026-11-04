"""Five versions of the user's reference thumbnail, each with one addition from the video."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import icons, guide
from render_text import text_img
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'thumbnails')
YEL = ((255, 232, 92), (250, 168, 28)); STROKE = (40, 18, 4)

def base():
    im = Image.open(os.path.join(HERE, 'assets', 'thumb_reference.jpg')).convert('RGB')
    w = int(im.height * 16 / 9)                       # 16:9, keep the left (the figure) and most of the map
    im = im.crop((0, 0, w, im.height)).resize((1280, 720), Image.LANCZOS)
    return im.convert('RGBA')

def text(im, s, cx, cy, size, color=YEL, maxw=None):
    t = text_img(s, 'luckiest', size, None if color == YEL else color, STROKE, max(6, size // 13),
                 gradient=YEL if color == YEL else None)
    if maxw and t.width > maxw: t = t.resize((maxw, int(t.height * maxw / t.width)), Image.LANCZOS)
    im.alpha_composite(t, (int(cx - t.width / 2), int(cy - t.height / 2)))

def paste(im, sprite, cx, cy):
    im.alpha_composite(sprite, (int(cx - sprite.width / 2), int(cy - sprite.height / 2)))

def save(im, name):
    im.convert('RGB').save(os.path.join(OUT, name), quality=95); print('wrote', name)

# 1. NOT THE WINTER
im = base(); text(im, 'NOT THE', 975, 530, 96, (255, 255, 255)); text(im, 'WINTER', 975, 630, 150, maxw=580)
save(im, 'refmod_1_not_the_winter.jpg')

# 2. IMPOSSIBLE TO CONQUER
im = base(); text(im, 'IMPOSSIBLE', 975, 545, 120, maxw=590); text(im, 'TO CONQUER', 975, 652, 96, (255, 255, 255), maxw=520)
save(im, 'refmod_2_impossible_to_conquer.jpg')

# 3. Napoleon and Hitler crossed out + SAME MISTAKE
im = base()
for who, cx, yr in (('badge-napoleon', 790, '1812'), ('badge-hitler', 1060, '1941')):
    paste(im, icons.get(who, 170), cx, 110); paste(im, icons.get('xmark', 120), cx + 55, 150)
    text(im, yr, cx, 215, 54, (255, 255, 255))
text(im, 'SAME MISTAKE', 975, 640, 120, maxw=590)
save(im, 'refmod_3_same_mistake.jpg')

# 4. The guide on the map + WHY?
im = base()
g, (fx, fy) = guide.pose(390, 12, 2)
halo = Image.new('RGBA', g.size, (0, 0, 0, 0)); halo.putalpha(g.getchannel('A').point(lambda v: int(v * 0.6)))
im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(12)), (int(1140 - fx) + 6, int(720 + 6 - fy)))
im.alpha_composite(g, (int(1140 - fx), int(720 - fy)))
text(im, 'WHY?', 875, 615, 175)
save(im, 'refmod_4_guide_why.jpg')

# 5. 5 SECRET WEAPONS + five icons
im = base()
for i, k in enumerate(['mountain', 'people', 'diamond', 'ship', 'missile']):
    sp = icons.get(k, 84); sh = Image.new('RGBA', (sp.width + 40, sp.height + 40), (0, 0, 0, 0))
    sh.paste((255, 255, 255, 230), (20, 20), sp.getchannel('A')); sh = sh.filter(ImageFilter.GaussianBlur(6))
    cx = 735 + i * 118; paste(im, sh, cx, 500); paste(im, sp, cx, 500)
text(im, '5 SECRET WEAPONS', 975, 640, 104, maxw=590)
save(im, 'refmod_5_secret_weapons.jpg')
