"""Warm, bright satellite map in the reference's look (Natural Earth I shaded relief, public domain),
Mercator, lon -15..65, lat 15..58, 60 px per degree. Writes assets/world_merc.jpg + world_merc.json."""
import io, json, math, os, zipfile
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, 'assets')
ZIP = '/home/user/My-videos/russia/video/assets/ne_sr.zip'
LON0, LON1, LAT0, LAT1, PXD = -15.0, 65.0, 15.0, 58.0, 60
merc = lambda la: math.log(math.tan(math.pi / 4 + math.radians(la) / 2))
src = np.asarray(Image.open(zipfile.ZipFile(ZIP).open('NE1_HR_LC_SR_W.tif')).convert('RGB'))
sh, sw = src.shape[:2]
Wm = int((LON1 - LON0) * PXD); ky = Wm / math.radians(LON1 - LON0); Hm = int((merc(LAT1) - merc(LAT0)) * ky)
lat = np.degrees(2 * np.arctan(np.exp(merc(LAT1) - np.arange(Hm) / ky)) - np.pi / 2)
rows = np.clip(((90 - lat) / 180 * sh).astype(int), 0, sh - 1)
cols = ((((LON0 + np.arange(Wm) / PXD) + 180) % 360) / 360 * sw).astype(int)
img = src[rows][:, cols]; del src
a = img.astype(np.float32)
water = (a[..., 2] > a[..., 0] + 12) & (a[..., 2] > a[..., 1] - 5)
water = np.asarray(Image.fromarray((water * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))) > 127
lum = a.mean(axis=2, keepdims=True) / 255
# land: warm, saturated sand; keep the greens but deepen them
g = np.asarray(ImageEnhance.Contrast(ImageEnhance.Color(Image.fromarray(img)).enhance(1.15)).enhance(1.3)).astype(np.float32)
green = (a[..., 1] > a[..., 0] + 3)
land = g * np.array([1.02, 0.80, 0.55]) + np.array([12, 4, -4])
gk = np.clip((a[..., 1] - a[..., 0] + 4) / 22, 0, 1)
gk = np.asarray(Image.fromarray((gk * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))).astype(np.float32)[..., None] / 255
land = land * (1 - gk) + (g * np.array([0.50, 0.56, 0.32]) + np.array([10, 8, 0])) * gk
# sea: deep saturated blue, lighter near the coast
dist = np.asarray(Image.fromarray((~water * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))).astype(np.float32)[..., None] / 255
sea = np.array([10, 52, 150], np.float32) * (0.45 + 0.9 * lum) + dist * np.array([20, 55, 60])
out = np.where(water[..., None], sea, land)
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(os.path.join(A, 'world_merc.jpg'), quality=92)
json.dump({'lon0': LON0, 'lon1': LON1, 'lat0': LAT0, 'lat1': LAT1, 'W': Wm, 'H': Hm, 'ky': ky}, open(os.path.join(A, 'world_merc.json'), 'w'))
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).resize((Wm // 4, Hm // 4)).save(os.path.join(HERE, 'build', 'map_check.jpg'))
print('map', Wm, Hm)
