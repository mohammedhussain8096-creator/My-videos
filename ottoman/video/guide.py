"""Motion rig for the user's character. The drawing is never redrawn or reshaped: the cut-out is split
into two untouched layers (the spear, and everything else) so the spear can tilt around the grip, and the
whole figure can sway, hop, lean and bounce in time with the voice."""
import math, os
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageChops, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.environ.get('RU_ASSETS', os.path.join(HERE, 'assets'))
HAND = (92, 690)       # grip, in guide.png pixels
FEET = (300, 1500)     # sway pivot

def spear_line_x(y):
    return 56 + (y - 110) * 0.082

def spear_mask(size):
    m = Image.new('L', size, 0); d = ImageDraw.Draw(m)
    left = [(spear_line_x(y) - 80, y) for y in range(0, 1522, 20)]
    right = [(spear_line_x(y) + (66 if y < 400 else 40), y) for y in range(1521, -1, -20)]
    d.polygon(left + right, fill=255)
    # keep the hand (and the bit of arm next to it) on the body layer
    d.ellipse([HAND[0] - 52, HAND[1] - 42, HAND[0] + 46, HAND[1] + 44], fill=0)
    return m

def refine(mask, alpha):
    """keep only the connected pieces of the band that sit on the spear's line (drops hat/feather bits)"""
    from scipy import ndimage
    band = (np.asarray(mask) > 0) & (np.asarray(alpha) > 40)
    lab, n = ndimage.label(band)
    keep = np.zeros(n + 1, bool)
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        ys, xs = np.nonzero(lab[sl] == i)
        if len(ys) < 30: continue
        cy, cx = ys.mean() + sl[0].start, xs.mean() + sl[1].start
        if abs(cx - spear_line_x(cy)) < 45 and (sl[0].stop - sl[0].start) > 25: keep[i] = True
    m = keep[lab]
    m = ndimage.binary_dilation(m, iterations=2) & (np.asarray(mask) > 0)
    m[1440:] &= ~SHADOW[1440:]
    return Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))

@lru_cache(maxsize=4)
def layers(h):
    g = Image.open(os.path.join(ASSETS, 'guide.png')).convert('RGBA')
    a = g.getchannel('A')
    global SHADOW
    c = np.asarray(g.convert('RGB')).astype(int)
    SHADOW = (c.min(axis=2) > 150) & (c.max(axis=2) - c.min(axis=2) < 30)
    m = refine(spear_mask(g.size), a)
    spear = g.copy(); spear.putalpha(ImageChops.multiply(a, m))
    body = g.copy(); body.putalpha(ImageChops.multiply(a, ImageChops.invert(m)))
    k = h / g.height
    sz = (int(g.width * k), h)
    return spear.resize(sz, Image.LANCZOS), body.resize(sz, Image.LANCZOS), k

PAD = 0.45   # canvas padding (fraction of height) so rotated parts never clip

@lru_cache(maxsize=160)
def pose(h, spear_deg=0.0, lean_deg=0.0):
    """Compose the figure with the spear tilted `spear_deg` (positive = tip toward the left/map) and the whole
    figure leaning `lean_deg` around the feet. Returns (image, feet_xy_in_image)."""
    spear, body, k = layers(h)
    p = int(PAD * h)
    W, H = body.width + 2 * p, body.height + p
    can = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    hx, hy = HAND[0] * k + p, HAND[1] * k + p * 0.5
    sl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sl.alpha_composite(spear, (p, int(p * 0.5)))
    if abs(spear_deg) > 0.05:
        sl = sl.rotate(spear_deg, resample=Image.BICUBIC, center=(hx, hy))
    can.alpha_composite(sl)
    can.alpha_composite(body, (p, int(p * 0.5)))
    fx, fy = FEET[0] * k + p, FEET[1] * k + p * 0.5
    if abs(lean_deg) > 0.05:
        can = can.rotate(lean_deg, resample=Image.BICUBIC, center=(fx, fy))
    return can, (fx, fy)
