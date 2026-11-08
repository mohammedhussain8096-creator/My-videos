"""Burned-in captions (bottom centre): the spoken words in short chunks, the current word highlighted.
Font: Inter ExtraBold, white with a black outline and soft shadow; current word in yellow.
Word times are estimated inside each narration phrase from character positions (the phrase start/end are exact)."""
import os, re
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import sys, importlib
R = sys.modules['__main__'] if hasattr(sys.modules.get('__main__'), 'MPX') else importlib.import_module('render')
W, H, U = R.W, R.H, R.U
YEL = (255, 214, 40)
MAXW = 5; MAXC = 30

@lru_cache(None)
def cfont(size): return ImageFont.truetype(os.path.join(R.ASSETS, 'fonts', 'Inter-ExtraBold.ttf'), int(size * U))

@lru_cache(None)
def chunks():
    """-> list of (start, end, [ (word, wstart, wend) ... ])"""
    out = []
    for p in R.TIMING['phrases']:
        words = p['text'].split(); total = sum(len(w) + 1 for w in words); t = p['start']; dur = p['end'] - p['start']
        timed = []
        for w in words:
            d = dur * (len(w) + 1) / total; timed.append((w, t, t + d)); t += d
        cur = []
        for k, wt in enumerate(timed):
            cur.append(wt)
            txt = ' '.join(x[0] for x in cur); end_sent = re.search(r'[.?!,;:]$', wt[0])
            if len(cur) >= MAXW or len(txt) >= MAXC or end_sent or k == len(timed) - 1:
                out.append((cur[0][1], cur[-1][2], cur)); cur = []
    return out

def draw(img, gt):
    """img RGBA; gt = global time in seconds"""
    cs = chunks(); cur = None
    for c in cs:
        if c[0] - 0.05 <= gt < c[1] + 0.25: cur = c
        if c[0] > gt: break
    if cur is None: return
    f = cfont(54); words = cur[2]; sp = f.getlength(' ')
    widths = [f.getlength(w[0]) for w in words]; total = sum(widths) + sp * (len(words) - 1)
    x = W / 2 - total / 2; y = H * 0.93
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    k = min(1.0, (gt - cur[0] + 0.05) / 0.12)                     # quick fade-in per chunk
    xx = x
    for (w, ws, we), ww in zip(words, widths):
        ds.text((xx + 3 * U, y + 5 * U), w, font=f, fill=(0, 0, 0, int(200 * k)), anchor='ls', stroke_width=int(9 * U), stroke_fill=(0, 0, 0, int(200 * k)))
        xx += ww + sp
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5 * U)))
    xx = x
    for (w, ws, we), ww in zip(words, widths):
        on = ws - 0.03 <= gt < we + 0.02
        col = YEL if on else (255, 255, 255)
        d.text((xx, y), w, font=f, fill=col + (int(255 * k),), anchor='ls', stroke_width=int(6 * U), stroke_fill=(10, 10, 10, int(255 * k)))
        xx += ww + sp
    img.alpha_composite(lay)
