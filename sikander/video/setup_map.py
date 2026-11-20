"""Vintage relief map of Europe-Africa-Asia for the Netaji video (Mercator, 60 px per degree, lon -25..150, lat -42..62).
Natural Earth I shaded relief (public domain) toned to the warm parchment/teal look of the Partition video, with Natural
Earth country borders (public domain) drawn in. Processed in strips. Writes assets/asia_merc.jpg + asia_merc.json."""
import json, math, os, zipfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, 'assets')
ZIP = '/home/user/My-videos/russia/video/assets/ne_sr.zip'
LON0, LON1, LAT0, LAT1, PXD = -25.0, 150.0, -42.0, 62.0, 60
merc = lambda la: math.log(math.tan(math.pi / 4 + math.radians(la) / 2))
src = Image.open(zipfile.ZipFile(ZIP).open('NE1_HR_LC_SR_W.tif')).convert('RGB'); sw, sh = src.size
Wm = int((LON1 - LON0) * PXD); ky = Wm / math.radians(LON1 - LON0); Hm = int((merc(LAT1) - merc(LAT0)) * ky)
cols = ((((LON0 + np.arange(Wm) / PXD) + 180) % 360) / 360 * sw).astype(int)
out = Image.new('RGB', (Wm, Hm)); STRIP, PAD = 1000, 40
PAPER = np.array([214, 194, 152], np.float32); SEA = np.array([30, 52, 62], np.float32)
for y0 in range(0, Hm, STRIP):
    ya, yb = max(0, y0 - PAD), min(Hm, y0 + STRIP + PAD)
    lat = np.degrees(2 * np.arctan(np.exp(merc(LAT1) - np.arange(ya, yb) / ky)) - np.pi / 2)
    rows = np.clip(((90 - lat) / 180 * sh).astype(int), 0, sh - 1)
    r0, r1 = rows.min(), rows.max() + 1
    band = np.asarray(src.crop((0, r0, sw, r1))); img = band[rows - r0][:, cols]; del band
    a = img.astype(np.float32)
    water = (a[..., 2] > a[..., 0] + 12) & (a[..., 2] > a[..., 1] - 5)
    water = np.asarray(Image.fromarray((water * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))) > 127
    lum = a.mean(axis=2, keepdims=True) / 255
    green = np.clip((a[..., 1] - a[..., 0] + 4) / 30, 0, 1)[..., None]
    shade = np.clip(0.80 + 1.5 * (lum - 0.55), 0.45, 1.15)
    land = PAPER * shade * (1 - 0.22 * green) + np.array([-10, 2, -6]) * green
    dist = np.asarray(Image.fromarray((~water * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(12))).astype(np.float32)[..., None] / 255
    sea = SEA * (0.8 + 0.5 * lum) + dist * np.array([46, 50, 40])
    o = np.where(water[..., None], sea, land)
    out.paste(Image.fromarray(np.clip(o, 0, 255).astype(np.uint8)).crop((0, y0 - ya, Wm, y0 - ya + min(STRIP, Hm - y0))), (0, y0))
    print('strip', y0, flush=True)
# paper texture + country borders
rng = np.random.default_rng(3)
tex = Image.fromarray(rng.normal(128, 40, (Hm // 6, Wm // 6)).clip(0, 255).astype(np.uint8)).resize((Wm, Hm), Image.BICUBIC)
out = Image.blend(out, Image.merge('RGB', [tex] * 3), 0.06)
d = ImageDraw.Draw(out)
def ll(la, lo): return (lo - LON0) * PXD, (merc(LAT1) - merc(max(-85, min(85, la)))) * ky
C = json.load(open(os.path.join(A, 'countries.json')))
for n, rs in C.items():
    for r in rs:
        pts = [ll(la, lo) for lo, la in r]
        xs = [p[0] for p in pts]
        if max(xs) < -20 or min(xs) > Wm + 20: continue
        d.line(pts + [pts[0]], fill=(120, 96, 66), width=2)
out = out.filter(ImageFilter.UnsharpMask(18, 35, 0)).filter(ImageFilter.UnsharpMask(2, 50, 2))
out.save(os.path.join(A, 'asia_merc.jpg'), quality=93)
json.dump({'lon0': LON0, 'lon1': LON1, 'lat0': LAT0, 'lat1': LAT1, 'W': Wm, 'H': Hm, 'ky': ky, 'pxd': PXD}, open(os.path.join(A, 'asia_merc.json'), 'w'))
out.resize((Wm // 8, Hm // 8)).save('/tmp/claude-0/-home-user-My-videos/cca8525b-d5a7-5580-88f3-c53540a74a6f/scratchpad/asia_small.jpg')
print('map', Wm, Hm)
