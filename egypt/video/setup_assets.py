"""Downloads and prepares everything render.py and tts.py need, into ./assets (or $EGYPT_ASSETS):
- Natural Earth I shaded-relief raster (public domain), cropped to Europe/Africa/Middle East and colour-graded
- fonts: Bangers (yellow punch text), Patrick Hand (hand-lettered labels)  [SIL Open Font License]
- Piper voice en_US-ryan-high (offline narrator voice)
- guide.png: the user's character cut out from character_reference.png
Needs: pip install piper-tts fonttools brotli scipy numpy pillow"""
import io, os, subprocess, sys, urllib.request, zipfile
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.environ.get('EGYPT_ASSETS', os.path.join(HERE, 'assets'))
os.makedirs(A, exist_ok=True)
Image.MAX_IMAGE_PIXELS = None

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=600) as r:
        return r.read()

def fonts():
    from fontTools.ttLib import TTFont
    for name, url in [('bangers', 'https://fonts.gstatic.com/s/bangers/v25/FeVQS0BTqb0h60ACH55Q2A.woff2'),
                      ('patrick', 'https://fonts.gstatic.com/s/patrickhand/v25/LDI1apSQOAYtSuYWp8ZhfYe8XsLL.woff2')]:
        out = os.path.join(A, name + '.ttf')
        if os.path.exists(out): continue
        f = TTFont(io.BytesIO(get(url))); f.flavor = None; f.save(out)

def world():
    out = os.path.join(A, 'world_graded.jpg')
    if os.path.exists(out): return
    z = zipfile.ZipFile(io.BytesIO(get('https://naciscdn.org/naturalearth/10m/raster/NE1_HR_LC_SR_W.zip')))
    im = Image.open(z.open('NE1_HR_LC_SR_W.tif'))
    x0, x1, y0, y1 = int((-25 + 180) * 60), int((82 + 180) * 60), int((90 - 62) * 60), int((90 + 40) * 60)
    w = im.crop((x0, y0, x1, y1)).convert('RGB')
    a = np.asarray(w).astype(np.float32)
    water = (a[..., 2] > a[..., 0] + 12) & (a[..., 2] > a[..., 1] - 5)
    g = ImageEnhance.Contrast(ImageEnhance.Color(w).enhance(1.45)).enhance(1.35)
    b = np.asarray(g).astype(np.float32)
    b[water] = b[water] * 0.3 + np.array([14, 58, 128], np.float32) * 0.7
    land = ~water
    b[land] = b[land] * np.array([0.80, 0.78, 0.62])
    green = (a[..., 1] > a[..., 0] + 4) & land
    b[green] = b[green] * np.array([0.78, 0.92, 0.70])
    Image.fromarray(np.clip(b, 0, 255).astype(np.uint8)).save(out, quality=92)

def guide():
    from scipy import ndimage
    out = os.path.join(A, 'guide.png')
    im = Image.open(os.path.join(HERE, '..', 'character_reference.png')).convert('RGB')
    white = np.asarray(im).astype(np.int16).min(axis=2) > 232
    lab, n = ndimage.label(white)
    sizes = ndimage.sum(white, lab, range(1, n + 1))
    keep = np.zeros(n + 1, bool); keep[1:] = sizes > 1500
    alpha = Image.fromarray(np.where(keep[lab], 0, 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    im = im.convert('RGBA'); im.putalpha(alpha); im.crop(alpha.getbbox()).save(out)

def voice():
    vd = os.path.join(A, 'voices')
    if os.path.exists(os.path.join(vd, 'en_US-ryan-high.onnx')): return
    os.makedirs(vd, exist_ok=True)
    subprocess.run([sys.executable, '-m', 'piper.download_voices', '--download-dir', vd, 'en_US-ryan-high'], check=True)

if __name__ == '__main__':
    fonts(); guide(); voice(); world(); print('assets ready in', A)
