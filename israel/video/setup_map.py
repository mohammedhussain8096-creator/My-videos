"""Close-up map + detailed borders for the Israel video.

1. assets/levant_merc.jpg: NASA Blue Marble shaded relief (GIBS, public domain) for lat 26-38, lon 28-42, reprojected to the
   same Mercator as world_merc.jpg at 4x its scale (240 px per degree), colour-matched to the warm world map so the two blend.
2. assets/levant.json: Natural Earth 10 m polygons (public domain) for the region, plus the historical shapes the plan uses:
   Green Line Israel, West Bank, Gaza, Golan, Sinai, Mandate Palestine, the 1947 UN partition (approximate) and the ancient
   kingdoms of Israel and Judah (approximate)."""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageFilter
from shapely.geometry import shape, Polygon, MultiPolygon, mapping
from shapely.ops import unary_union
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, 'assets')
NE = sys.argv[1] if len(sys.argv) > 1 else '/tmp/ne'
LON0, LON1, LAT0, LAT1, PXD = 28.0, 42.0, 26.0, 38.0, 240
MJ = json.load(open(os.path.join(A, 'world_merc.json')))
merc = lambda la: math.log(math.tan(math.pi / 4 + math.radians(la) / 2))

def build_inset():
    src = np.asarray(Image.open(os.path.join(A, 'sat', 'levant_bm.jpg')).convert('RGB')).astype(np.float32)
    sh, sw = src.shape[:2]
    ky = MJ['ky'] * 4
    Wm = int((LON1 - LON0) * PXD); Hm = int((merc(LAT1) - merc(LAT0)) * ky)
    lat = np.degrees(2 * np.arctan(np.exp(merc(LAT1) - np.arange(Hm) / ky)) - np.pi / 2)
    rows = np.clip(((LAT1 - lat) / (LAT1 - LAT0) * sh).astype(int), 0, sh - 1)
    cols = np.clip((np.arange(Wm) / PXD / (LON1 - LON0) * sw).astype(int), 0, sw - 1)
    img = src[rows][:, cols]
    # reference: the same area cut from the warm world map, upscaled
    wm = Image.open(os.path.join(A, 'world_merc.jpg')).convert('RGB')
    x0 = (LON0 - MJ['lon0']) * 60; x1 = (LON1 - MJ['lon0']) * 60
    y0 = (merc(MJ['lat1']) - merc(LAT1)) * MJ['ky']; y1 = (merc(MJ['lat1']) - merc(LAT0)) * MJ['ky']
    ref = np.asarray(wm.resize((Wm, Hm), Image.BICUBIC, box=(x0, y0, x1, y1))).astype(np.float32)
    def water(a): return (a[..., 2] > a[..., 0] + 12) & (a[..., 2] > a[..., 1] - 5)
    ws, wr = water(img), water(ref)
    out = img.copy()
    for ms, mr in ((ws, wr), (~ws, ~wr)):     # match mean/std per channel, separately for sea and land
        for c in range(3):
            s, r = img[..., c][ms], ref[..., c][mr]
            out[..., c][ms] = (s - s.mean()) / (s.std() + 1e-6) * r.std() + r.mean()
    # sharpen a little (the source is 500 m) and soften the sea/land seam
    im = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).filter(ImageFilter.UnsharpMask(2, 60, 2))
    im.save(os.path.join(A, 'levant_merc.jpg'), quality=93)
    json.dump({'lon0': LON0, 'lon1': LON1, 'lat0': LAT0, 'lat1': LAT1, 'W': Wm, 'H': Hm, 'scale': 4}, open(os.path.join(A, 'levant_merc.json'), 'w'))
    print('inset', Wm, Hm)

def rings(g):
    gs = [g] if isinstance(g, Polygon) else list(g.geoms)
    return [[(round(x, 4), round(y, 4)) for x, y in p.exterior.coords] for p in gs if p.area > 1e-5]

def build_polys():
    ne = {f['properties']['ADMIN']: shape(f['geometry']) for f in json.load(open(os.path.join(NE, 'ne10.geojson')))['features']}
    disp = {f['properties']['NAME']: shape(f['geometry']) for f in json.load(open(os.path.join(NE, 'ne10_disp.geojson')))['features']}
    out = {}
    for n in ('Israel', 'Palestine', 'Lebanon', 'Syria', 'Jordan', 'Egypt', 'Saudi Arabia', 'Iraq', 'Cyprus', 'Turkey'):
        out[n.upper().replace(' ', '_')] = ne[n]
    golan = disp['Golan Heights']; wb = disp['West Bank']; gz = disp['Gaza']
    isr = unary_union([ne['Israel'], disp.get('Israel', ne['Israel'])])
    for k in ("No Man's Land (Fort Latrun)", "No Man's Land (Jerusalem)", 'Mount Scopus', 'East Jerusalem'):
        if k in disp: wb = unary_union([wb, disp[k]])
    green = isr.difference(golan.buffer(0.002)).difference(wb.buffer(0.002)).difference(gz.buffer(0.002))
    mandate = unary_union([green, wb, gz]).buffer(0.003).buffer(-0.003)
    sinai_cut = Polygon([(32.30, 31.40), (32.33, 30.60), (32.57, 29.95), (32.90, 29.00), (33.45, 28.20), (33.80, 27.60), (36.0, 27.0), (36.0, 31.8)])
    sinai = ne['Egypt'].intersection(sinai_cut)
    out.update({'GREEN_LINE': green, 'WEST_BANK': wb, 'GAZA': gz, 'GOLAN': golan, 'SINAI': sinai, 'MANDATE': mandate,
                'EAST_JERUSALEM': disp.get('East Jerusalem', wb.intersection(Polygon([(35.2, 31.74), (35.3, 31.74), (35.3, 31.84), (35.2, 31.84)])))})
    # UN partition plan 1947 (approximate outline of the Arab state areas and the Jerusalem corpus separatum)
    arab = [
        [(34.80, 33.20), (35.47, 33.10), (35.50, 32.96), (35.44, 32.80), (35.38, 32.66), (35.24, 32.64), (35.13, 32.76), (35.08, 32.86), (34.80, 32.86)],  # western Galilee
        [(35.02, 32.53), (35.30, 32.56), (35.60, 32.42), (35.58, 31.77), (35.47, 31.47), (35.22, 31.35), (35.00, 31.22), (34.86, 31.17), (34.66, 31.20),
         (34.52, 31.00), (34.40, 30.92), (34.24, 31.22), (34.00, 31.40), (34.40, 31.95), (34.62, 31.86), (34.73, 31.74), (34.72, 31.58), (34.80, 31.40),
         (34.90, 31.45), (34.96, 31.62), (34.92, 31.80), (34.86, 31.90), (34.90, 32.03), (34.97, 32.16), (35.00, 32.33)],                              # hills, Gaza, Beersheba
        [(34.60, 32.08), (34.79, 32.08), (34.79, 32.01), (34.60, 32.01)],                                                                                 # Jaffa
    ]
    jer = Polygon([(35.12, 31.86), (35.30, 31.86), (35.30, 31.66), (35.12, 31.66)])
    a = unary_union([Polygon(r) for r in arab]).difference(jer).intersection(mandate)
    out['UN_ARAB'] = a; out['UN_JERUSALEM'] = jer.intersection(mandate)
    out['UN_JEWISH'] = mandate.difference(a).difference(jer)
    # ancient kingdoms (approximate)
    out['K_ISRAEL'] = Polygon([(34.85, 32.05), (35.15, 32.02), (35.55, 32.10), (35.75, 32.30), (35.75, 33.15), (35.40, 33.20), (35.10, 33.05), (34.95, 32.60)])
    out['K_JUDAH'] = Polygon([(34.85, 31.98), (35.15, 32.00), (35.50, 31.95), (35.45, 31.40), (35.20, 31.05), (34.80, 31.10), (34.75, 31.55)])
    land = unary_union([ne[n] for n in ('Israel', 'Palestine', 'Lebanon', 'Syria', 'Jordan')] + [golan, wb, gz]).buffer(0.002)
    for k in ('K_ISRAEL', 'K_JUDAH'): out[k] = out[k].intersection(land)
    out['K_UNITED'] = unary_union([out['K_ISRAEL'], out['K_JUDAH']]).buffer(0.004)
    json.dump({k: rings(v) for k, v in out.items()}, open(os.path.join(A, 'levant.json'), 'w'))
    print({k: round(v.area, 3) for k, v in out.items()})
    print('UN split %:', round(100 * out['UN_JEWISH'].area / mandate.area, 1), round(100 * out['UN_ARAB'].area / mandate.area, 1),
          'Green line %:', round(100 * green.area / mandate.area, 1))

if __name__ == '__main__':
    if 'polys' not in sys.argv: build_inset()
    build_polys()
