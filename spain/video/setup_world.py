"""World map for the Spain video: same warm look and scale as the Istanbul/Israel map (Natural Earth I shaded relief, public
domain, Mercator, 60 px per degree), but wide enough for the Spanish empire: lon -130..140, lat -56..62.
Processed in strips to keep memory low. Writes assets/world_merc.jpg + world_merc.json (replacing the regional links)."""
import json, math, os, zipfile
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, 'assets')
ZIP = '/home/user/My-videos/russia/video/assets/ne_sr.zip'
LON0, LON1, LAT0, LAT1, PXD = -130.0, 140.0, -56.0, 62.0, 60
merc = lambda la: math.log(math.tan(math.pi / 4 + math.radians(la) / 2))
src = Image.open(zipfile.ZipFile(ZIP).open('NE1_HR_LC_SR_W.tif')).convert('RGB')
sw, sh = src.size
Wm = int((LON1 - LON0) * PXD); ky = Wm / math.radians(LON1 - LON0); Hm = int((merc(LAT1) - merc(LAT0)) * ky)
cols = ((((LON0 + np.arange(Wm) / PXD) + 180) % 360) / 360 * sw).astype(int)
out = Image.new('RGB', (Wm, Hm))
STRIP, PAD = 1200, 40
for y0 in range(0, Hm, STRIP):
    ya, yb = max(0, y0 - PAD), min(Hm, y0 + STRIP + PAD)
    lat = np.degrees(2 * np.arctan(np.exp(merc(LAT1) - np.arange(ya, yb) / ky)) - np.pi / 2)
    rows = np.clip(((90 - lat) / 180 * sh).astype(int), 0, sh - 1)
    r0, r1 = rows.min(), rows.max() + 1
    band = np.asarray(src.crop((0, r0, sw, r1)))
    img = band[rows - r0][:, cols]; del band
    a = img.astype(np.float32)
    water = (a[..., 2] > a[..., 0] + 12) & (a[..., 2] > a[..., 1] - 5)
    water = np.asarray(Image.fromarray((water * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))) > 127
    lum = a.mean(axis=2, keepdims=True) / 255
    g = np.asarray(ImageEnhance.Contrast(ImageEnhance.Color(Image.fromarray(img)).enhance(1.15)).enhance(1.3)).astype(np.float32)
    land = g * np.array([1.02, 0.80, 0.55]) + np.array([12, 4, -4])
    gk = np.clip((a[..., 1] - a[..., 0] + 4) / 22, 0, 1)
    gk = np.asarray(Image.fromarray((gk * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))).astype(np.float32)[..., None] / 255
    land = land * (1 - gk) + (g * np.array([0.50, 0.56, 0.32]) + np.array([10, 8, 0])) * gk
    dist = np.asarray(Image.fromarray((~water * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))).astype(np.float32)[..., None] / 255
    sea = np.array([10, 52, 150], np.float32) * (0.45 + 0.9 * lum) + dist * np.array([20, 55, 60])
    o = np.where(water[..., None], sea, land)
    piece = Image.fromarray(np.clip(o, 0, 255).astype(np.uint8))
    out.paste(piece.crop((0, y0 - ya, Wm, y0 - ya + min(STRIP, Hm - y0))), (0, y0))
    print('strip', y0, flush=True)
for f in ('world_merc.jpg', 'world_merc.json'):
    p = os.path.join(A, f)
    if os.path.islink(p): os.unlink(p)
out.save(os.path.join(A, 'world_merc.jpg'), quality=92)
json.dump({'lon0': LON0, 'lon1': LON1, 'lat0': LAT0, 'lat1': LAT1, 'W': Wm, 'H': Hm, 'ky': ky}, open(os.path.join(A, 'world_merc.json'), 'w'))
out.resize((Wm // 10, Hm // 10)).save('/tmp/claude-0/-home-user-My-videos/cca8525b-d5a7-5580-88f3-c53540a74a6f/scratchpad/th/world.jpg')
print('map', Wm, Hm)
