"""AI-upscale small archive photos with Real-ESRGAN (ONNX, CPU) so they stay sharp at 1080p.
Usage: python3 upscale.py MODEL_DIR [names...]   -> writes assets/photos_hd/<name>.jpg
Photos whose short side is under 1100 px are upscaled (x4 under 600 px, else x2), then capped at 2600 px."""
import os, sys, time
import numpy as np, onnxruntime as ort
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'assets', 'photos'); DST = os.path.join(HERE, 'assets', 'photos_hd')

def run(sess, img, scale, tile=192, pad=12):
    a = np.asarray(img.convert('RGB'), np.float32) / 255.0
    h, w, _ = a.shape; out = np.zeros((h * scale, w * scale, 3), np.float32)
    for y in range(0, h, tile):
        for x in range(0, w, tile):
            y0, x0 = max(0, y - pad), max(0, x - pad); y1, x1 = min(h, y + tile + pad), min(w, x + tile + pad)
            t = a[y0:y1, x0:x1].transpose(2, 0, 1)[None]
            r = sess.run(None, {'input': t})[0][0].transpose(1, 2, 0)
            yy, xx = (y - y0) * scale, (x - x0) * scale
            th, tw = min(tile, h - y) * scale, min(tile, w - x) * scale
            out[y * scale:y * scale + th, x * scale:x * scale + tw] = r[yy:yy + th, xx:xx + tw]
    return Image.fromarray((out.clip(0, 1) * 255).round().astype(np.uint8))

def main():
    mdir = sys.argv[1]; names = sys.argv[2:]
    os.makedirs(DST, exist_ok=True)
    opts = ort.SessionOptions(); opts.intra_op_num_threads = os.cpu_count()
    S = {k: ort.InferenceSession(os.path.join(mdir, f'x{k}.onnx'), opts, providers=['CPUExecutionProvider']) for k in (2, 4)}
    files = names or sorted(f[:-4] for f in os.listdir(SRC) if f.endswith('.jpg'))
    for n in files:
        im = Image.open(os.path.join(SRC, n + '.jpg')).convert('RGB')
        if min(im.size) >= 1100: continue
        k = 4 if min(im.size) < 600 else 2
        t = time.time(); up = run(S[k], im, k)
        if max(up.size) > 2600:
            f = 2600 / max(up.size); up = up.resize((int(up.width * f), int(up.height * f)), Image.LANCZOS)
        up.save(os.path.join(DST, n + '.jpg'), quality=94)
        print(f'{n}: {im.size} -> {up.size} x{k} {time.time() - t:.0f}s', flush=True)

if __name__ == '__main__':
    main()
