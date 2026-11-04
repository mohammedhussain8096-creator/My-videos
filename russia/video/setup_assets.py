"""Prepares everything render.py needs, into ./assets (or $RU_ASSETS):
- world_merc.jpg: Natural Earth I shaded-relief raster (public domain), reprojected to Mercator
  (lon -180..200 so all of Russia fits in one view, lat -58..82) and colour-graded like the reference
- countries.json: Natural Earth 1:50m country outlines (public domain)
- fonts: Luckiest Guy (yellow punch captions), Nunito Black (labels) [SIL Open Font License]
- Kokoro voice model (Apache-2.0)
- guide.png: the user's character, cut out of its white background (the drawing itself is unchanged)"""
import io, json, math, os, urllib.request, zipfile
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.environ.get('RU_ASSETS', os.path.join(HERE, 'assets'))
os.makedirs(A, exist_ok=True)
Image.MAX_IMAGE_PIXELS = None
LON0, LON1, LAT0, LAT1 = -180.0, 200.0, -58.0, 82.0
PX_PER_DEG = 40

def get(url, dest=None):
    if dest and os.path.exists(dest): return open(dest, 'rb').read()
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=900) as r:
        b = r.read()
    if dest: open(dest, 'wb').write(b)
    return b

def merc(lat):
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))

def world():
    out = os.path.join(A, 'world_merc.jpg')
    if os.path.exists(out): return
    z = zipfile.ZipFile(io.BytesIO(get('https://naciscdn.org/naturalearth/10m/raster/NE1_HR_LC_SR_W.zip', os.path.join(A, 'ne_sr.zip'))))
    src = np.asarray(Image.open(z.open('NE1_HR_LC_SR_W.tif')).convert('RGB'))   # 21600 x 10800, 60 px/deg
    sh, sw = src.shape[:2]
    W = int((LON1 - LON0) * PX_PER_DEG)
    ky = W / math.radians(LON1 - LON0)
    H = int((merc(LAT1) - merc(LAT0)) * ky)
    ys = merc(LAT1) - np.arange(H) / ky
    lat = np.degrees(2 * np.arctan(np.exp(ys)) - np.pi / 2)
    rows = np.clip(((90 - lat) / 180 * sh).astype(int), 0, sh - 1)
    lon = LON0 + np.arange(W) / PX_PER_DEG
    cols = (((lon + 180) % 360) / 360 * sw).astype(int) % sw
    img = src[rows][:, cols]
    del src
    a = img.astype(np.float32)
    water = (a[..., 2] > a[..., 0] + 12) & (a[..., 2] > a[..., 1] - 5)
    g = np.asarray(ImageEnhance.Contrast(ImageEnhance.Color(Image.fromarray(img)).enhance(1.35)).enhance(1.25)).astype(np.float32)
    lum = g.mean(axis=2, keepdims=True)
    # sea: deep saturated blue with the bathymetry shading kept
    sea = np.array([18, 62, 140], np.float32) * (0.55 + 0.6 * lum / 255)
    g[water] = sea[water]
    land = ~water
    g[land] = np.power(g[land] * np.array([0.66, 0.68, 0.58]) / 255, 1.7) * 255 * np.array([0.95, 1.0, 0.78])   # dark satellite look
    l = g[land]; m = l.mean(axis=1, keepdims=True)
    g[land] = (m + (l - m) * 0.6) * 0.62 * np.array([0.95, 1.0, 0.9])      # muted, dark land like the reference
    g[water] *= 0.92 * np.array([0.85, 0.9, 1.0])
    Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).save(out, quality=90)
    json.dump({'lon0': LON0, 'lon1': LON1, 'lat0': LAT0, 'lat1': LAT1, 'W': W, 'H': H, 'ky': ky},
              open(os.path.join(A, 'world_merc.json'), 'w'))

def countries():
    out = os.path.join(A, 'countries.json')
    if os.path.exists(out): return
    gj = json.loads(get('https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson'))
    res = {}
    for f in gj['features']:
        name = f['properties']['ADMIN']
        g = f['geometry']
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        rings = []
        for p in polys:
            ring = p[0]
            if name == 'Russia' and max(x for x, _ in ring) < -100:   # Chukotka: shift east of 180
                ring = [[x + 360, y] for x, y in ring]
            rings.append([[round(x, 3), round(y, 3)] for x, y in ring])
        res[name] = rings
    json.dump(res, open(out, 'w'))

def fonts():
    from fontTools.ttLib import TTFont
    for name, url in [('luckiest', 'https://fonts.gstatic.com/s/luckiestguy/v25/_gP_1RrxsjcxVyin9l9n_j2RTw.woff2'),
                      ('nunito', 'https://fonts.gstatic.com/s/nunito/v32/XRXI3I6Li01BKofiOc5wtlZ2di8HDBImRTY.woff2')]:
        out = os.path.join(A, name + '.ttf')
        if os.path.exists(out): continue
        f = TTFont(io.BytesIO(get(url))); f.flavor = None; f.save(out)

def kokoro():
    kd = os.path.join(A, 'kokoro'); os.makedirs(kd, exist_ok=True)
    base = 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/'
    for f in ('kokoro-v1.0.onnx', 'voices-v1.0.bin'):
        get(base + f, os.path.join(kd, f))

def guide():
    """Remove only the white paper background (flood-filled from the borders) and the drop shadow under
    the feet; every pixel of the character itself stays exactly as drawn."""
    from scipy import ndimage
    out = os.path.join(A, 'guide.png')
    im = Image.open(os.path.join(HERE, '..', 'character_reference.png')).convert('RGB')
    a = np.asarray(im).astype(np.int16)
    bg_like = (a.min(axis=2) > 200) & (a.max(axis=2) - a.min(axis=2) < 22)    # white / light grey paper + shadow
    lab, n = ndimage.label(bg_like)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge))
    # small enclosed white holes (between arm and body, between legs) are background too
    sizes = ndimage.sum(bg_like & ~bg, lab, range(1, n + 1))
    for i, s in enumerate(sizes, 1):
        if s > 2500 and i not in edge: bg |= lab == i
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    al = Image.fromarray(alpha).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
    rgba = im.convert('RGBA'); rgba.putalpha(al)
    rgba.crop(al.getbbox()).save(out)

if __name__ == '__main__':
    fonts(); kokoro(); countries(); guide(); world(); print('assets ready in', A)
