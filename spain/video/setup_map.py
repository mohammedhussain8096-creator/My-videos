"""Close-up map + detailed borders for the Spain video.

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
LON0, LON1, LAT0, LAT1, PXD = -11.0, 5.0, 34.0, 45.0, 240
MJ = json.load(open(os.path.join(A, 'world_merc.json')))
merc = lambda la: math.log(math.tan(math.pi / 4 + math.radians(la) / 2))

def build_inset():
    src = np.asarray(Image.open(os.path.join(A, 'sat', 'iberia_bm.jpg')).convert('RGB')).astype(np.float32)
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
    im.save(os.path.join(A, 'iberia_merc.jpg'), quality=93)
    json.dump({'lon0': LON0, 'lon1': LON1, 'lat0': LAT0, 'lat1': LAT1, 'W': Wm, 'H': Hm, 'scale': 4}, open(os.path.join(A, 'iberia_merc.json'), 'w'))
    print('inset', Wm, Hm)

def rings(g):
    gs = [g] if isinstance(g, Polygon) else list(g.geoms)
    return [[(round(x, 4), round(y, 4)) for x, y in p.exterior.coords] for p in gs if p.area > 1e-4]

def build_polys():
    ne = {f['properties']['ADMIN']: shape(f['geometry']) for f in json.load(open(os.path.join(NE, 'ne10.geojson')))['features']}
    adm = {}
    for f in json.load(open(os.path.join(NE, 'adm1.geojson')))['features']:
        p = f['properties']
        if p['adm0_a3'] in ('ESP', 'PRT'): adm[p['name']] = (p['adm0_a3'], p['region'], shape(f['geometry']).buffer(0))
    box = Polygon([(-10.5, 35.8), (4.6, 35.8), (4.6, 44.2), (-10.5, 44.2)])
    main = {k: v for k, v in adm.items() if v[2].intersects(box) and k not in ('Ceuta', 'Melilla')}
    U = lambda ks: unary_union([main[k][2] for k in ks]).buffer(0.003).buffer(-0.003)
    REG = lambda r: [k for k, v in main.items() if v[1] == r]
    ES = [k for k, v in main.items() if v[0] == 'ESP']; PT = [k for k, v in main.items() if v[0] == 'PRT']
    out = {}
    out['SPAIN'] = U(ES); out['PORTUGAL'] = U(PT); out['IBERIA'] = U(ES + PT)
    for n in ('France', 'Morocco', 'Algeria', 'Andorra', 'Gibraltar', 'Italy', 'United Kingdom'):
        if n in ne: out[n.upper().replace(' ', '_')] = ne[n].intersection(Polygon([(-15, 30), (12, 30), (12, 52), (-15, 52)]))
    for key, r in (('CATALONIA', 'Cataluña'), ('BASQUE', 'País Vasco'), ('NAVARRE', 'Foral de Navarra'), ('ARAGON_R', 'Aragón'),
                   ('VALENCIA_R', 'Valenciana'), ('ANDALUSIA', 'Andalucía'), ('GALICIA', 'Galicia'), ('ASTURIAS', 'Asturias'),
                   ('CANTABRIA', 'Cantabria'), ('MADRID_R', 'Madrid'), ('CASTILE_LEON', 'Castilla y León'), ('CASTILE_LM', 'Castilla-La Mancha'),
                   ('EXTREMADURA', 'Extremadura'), ('MURCIA', 'Murcia'), ('BALEARES', 'Islas Baleares')):
        out[key] = U(REG(r))
    # ancient and medieval (approximate, built from today's provinces)
    out['CARTHAGE_ES'] = U(REG('Andalucía') + REG('Murcia') + REG('Valenciana') + ['Albacete', 'Ciudad Real', 'Faro', 'Beja'])
    out['ROME_1'] = U(REG('Cataluña') + REG('Valenciana') + REG('Andalucía') + REG('Murcia'))
    out['ROME_2'] = out['IBERIA'].difference(U(REG('Galicia') + REG('Asturias') + REG('Cantabria') + REG('País Vasco') + ['León', 'Burgos', 'Palencia', 'Navarra', 'Viana do Castelo', 'Braga', 'Porto', 'Vila Real', 'Bragança', 'Zamora']))
    out['NORTH_TRIBES'] = U(REG('Asturias') + REG('Cantabria') + ['León', 'Palencia', 'Burgos', 'Lugo'])
    out['ASTURIAS_K'] = U(REG('Asturias') + REG('Cantabria'))
    out['ANDALUS_750'] = out['IBERIA'].difference(U(REG('Asturias') + REG('Cantabria') + ['Bizkaia', 'Gipuzkoa', 'Navarra']).buffer(0.01))
    christ_1000 = REG('Galicia') + REG('Asturias') + REG('Cantabria') + REG('País Vasco') + ['León', 'Palencia', 'Burgos', 'Zamora', 'Valladolid', 'Navarra',
                  'La Rioja', 'Huesca', 'Gerona', 'Barcelona', 'Viana do Castelo', 'Braga', 'Porto', 'Vila Real', 'Bragança', 'Aveiro', 'Viseu']
    out['CHRISTIAN_1000'] = U(christ_1000); out['ANDALUS_1000'] = out['IBERIA'].difference(out['CHRISTIAN_1000'].buffer(0.01))
    out['ANDALUS_1150'] = U(REG('Andalucía') + REG('Murcia') + REG('Valenciana') + REG('Islas Baleares') + ['Badajoz', 'Beja', 'Évora', 'Faro', 'Setúbal', 'Portalegre'])
    out['GRANADA_K'] = U(['Granada', 'Málaga', 'Almería'])
    out['ARAGON_C'] = U(REG('Cataluña') + REG('Aragón') + REG('Valenciana') + REG('Islas Baleares'))
    out['CASTILE_C'] = out['SPAIN'].difference(unary_union([out['ARAGON_C'], out['NAVARRE'], out['GRANADA_K']]).buffer(0.01))
    out['CASTILE_1150'] = U(REG('Castilla y León') + REG('Madrid') + REG('Cantabria') + REG('Asturias') + REG('Galicia') + ['Toledo', 'Guadalajara', 'Cuenca', 'Cáceres', 'Álava', 'La Rioja'])
    # civil war fronts (approximate)
    rep36 = REG('Madrid') + REG('Cataluña') + REG('Valenciana') + REG('Murcia') + REG('Castilla-La Mancha') + REG('Asturias') + REG('Cantabria') + ['Bizkaia', 'Gipuzkoa', 'Jaén', 'Almería', 'Málaga', 'Badajoz']
    out['REP_1936'] = U(rep36); out['NAT_1936'] = out['SPAIN'].difference(out['REP_1936'].buffer(0.01))
    rep38 = REG('Madrid') + REG('Cataluña') + ['Valencia', 'Alicante', 'Murcia', 'Albacete', 'Cuenca', 'Ciudad Real', 'Guadalajara', 'Jaén', 'Almería']
    out['REP_1938'] = U(rep38); out['NAT_1938'] = out['SPAIN'].difference(out['REP_1938'].buffer(0.01))
    json.dump({k: rings(v) for k, v in out.items()}, open(os.path.join(A, 'iberia.json'), 'w'))
    print({k: round(v.area, 2) for k, v in out.items()})

if __name__ == '__main__':
    if 'polys' not in sys.argv: build_inset()
    build_polys()
