"""Israel thumbnail 4, closer to the user's reference look: natural NASA relief (no warm grade), thin white country
borders, solid glowing red land with white inner borders, large PM bust with one glowing eye, boxed title."""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont, ImageChops
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, 'assets')
W, H = 1920, 1080
INTER = os.path.join(HERE, '..', '..', 'chernobyl', 'video', 'assets', 'fonts', 'Inter-ExtraBold.ttf')
LON0, LON1, LAT0, LAT1, PXD = 28.0, 42.0, 26.0, 38.0, 240          # levant_bm.jpg (NASA Blue Marble, equirectangular)
# view: centre and width in degrees; vertical stretch 1/cos(lat) so shapes look right
CLON, CLAT, WD = 35.9, 31.75, 10.2
SY = 1 / math.cos(math.radians(CLAT)); HD = WD * H / W / SY
def scr(lon, lat): return (lon - (CLON - WD / 2)) / WD * W, ((CLAT + HD / 2) - lat) / HD * H

src = Image.open(os.path.join(A, 'sat', 'levant_bm.jpg')).convert('RGB')
box = ((CLON - WD / 2 - LON0) * PXD, (LAT1 - (CLAT + HD / 2)) * PXD, (CLON + WD / 2 - LON0) * PXD, (LAT1 - (CLAT - HD / 2)) * PXD)
fr = src.resize((W, H), Image.LANCZOS, box=box)
fr = ImageEnhance.Contrast(ImageEnhance.Color(fr).enhance(1.45)).enhance(1.18)
a = np.asarray(fr).astype(np.float32)
sea = (a[..., 2] > a[..., 0] + 10)
a[sea] = a[sea] * np.array([0.55, 0.85, 1.25]) + np.array([0, 20, 40])    # brighter, bluer sea like the reference
fr = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.UnsharpMask(2.5, 70, 2)).convert('RGBA')
base_rgb = np.asarray(fr.convert('RGB')).astype(np.float32)

LEV = json.load(open(os.path.join(A, 'levant.json')))
def mask(names, scale=1):
    m = Image.new('L', (W // scale, H // scale), 0); d = ImageDraw.Draw(m)
    for n in names:
        for ring in LEV[n]:
            d.polygon([(x / scale, y / scale) for x, y in (scr(lo, la) for lo, la in ring)], fill=255)
    return m
def lines(names, col, w):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for n in names:
        for ring in LEV[n]:
            pts = [scr(lo, la) for lo, la in ring]; d.line(pts + [pts[0]], fill=col, width=w, joint='curve')
    return lay

# thin white country borders
fr.alpha_composite(lines(['EGYPT', 'JORDAN', 'SYRIA', 'LEBANON', 'SAUDI_ARABIA', 'IRAQ'], (255, 255, 255, 150), 3))
# red land: Israel + West Bank + Gaza (+ Golan, as in the reference)
land = ['GREEN_LINE', 'WEST_BANK', 'GAZA', 'GOLAN']
m = mask(land)
glow = Image.new('RGBA', (W, H), (255, 40, 30, 0)); glow.putalpha(m.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(26)))
fr.alpha_composite(glow); fr.alpha_composite(glow)
lum = np.asarray(fr.convert('L')).astype(np.float32)[..., None] / 255
red = np.array([240, 34, 30], np.float32) * (0.3 + 1.0 * lum)            # terrain shading shows through the red
mm = np.asarray(m).astype(np.float32)[..., None] / 255 * 0.8
arr = np.asarray(fr).astype(np.float32); arr[..., :3] = arr[..., :3] * (1 - mm) + red * mm
lake = (sea[..., None] & (mm > 0.4)).astype(np.float32)
arr[..., :3] = arr[..., :3] * (1 - lake) + base_rgb * lake
fr = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGBA')
fr.alpha_composite(lines(land, (255, 255, 255, 255), 4))
# keep the Sea of Galilee / Dead Sea blue on top
for n in []: pass

# PM bust: White House photo (public domain); colour graded, one glowing red eye (stylised)
im = Image.open(os.path.join(A, 'photos', 'netanyahu_xl.png')).convert('RGBA').crop((120, 230, 1000, 1000))
k = 1060 / im.height; im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
x, y = W - im.width + 150, H - im.height + 90
ex, ey = (355 - 120) * k + x, (467 - 230) * k + y
rgb = ImageEnhance.Contrast(ImageEnhance.Color(im.convert('RGB')).enhance(1.12)).enhance(1.15)
b = np.asarray(rgb).astype(np.float32)
yy, xx = np.mgrid[0:im.height, 0:im.width].astype(np.float32)
dd = np.sqrt((xx - (ex - x)) ** 2 + (yy - (ey - y)) ** 2)
rr = np.clip(1 - dd / 230, 0, 1)[..., None] ** 1.6
b = b * (1 - 0.5 * rr) + np.array([255, 45, 30], np.float32) * 0.5 * rr
body = Image.fromarray(np.clip(b, 0, 255).astype(np.uint8)).convert('RGBA'); body.putalpha(im.getchannel('A'))
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, 230), (x - 25, y + 10), im.getchannel('A'))
fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(28))); fr.alpha_composite(body, (x, y))
g = np.zeros((H, W, 4), np.float32); Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
d2 = np.sqrt((X - ex) ** 2 + ((Y - ey) * 1.45) ** 2)
core = np.clip(1 - d2 / 16, 0, 1); amt = np.clip(np.exp(-(d2 / 34) ** 2) + np.exp(-(d2 / 100) ** 2) * 0.5, 0, 1)
g[..., 0] = 255; g[..., 1] = 25 + 230 * core; g[..., 2] = 20 + 235 * core; g[..., 3] = np.clip(amt + core, 0, 1) * 255
fr.alpha_composite(Image.fromarray(g.astype(np.uint8), 'RGBA'))

def boxed(txt, x, y, size, pad=(36, 20)):
    f = ImageFont.truetype(INTER, size); l, t, r, bb = f.getbbox(txt)
    w, h = r - l + 2 * pad[0], bb - t + 2 * pad[1]
    d = ImageDraw.Draw(fr); d.rectangle([x, y, x + w, y + h], fill=(6, 6, 8, 255))
    d.text((x + pad[0] - l, y + pad[1] - t), txt, font=f, fill=(255, 255, 255, 255)); return y + h
yb = boxed('ISRAEL', 55, 30, 190)
boxed('1000 BCE - TODAY', 55, yb + 26, 78)

out = os.path.join(HERE, '..', '..', 'thumbnails', 'Israel_Thumb4.jpg')
fr.convert('RGB').resize((1280, 720), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 45, 2)).save(out, quality=95)
print(out)
