import cv2, numpy as np, onnxruntime as ort, subprocess, sys, os

SRC, OUT = sys.argv[1], sys.argv[2]
F0, F1 = int(sys.argv[3]), int(sys.argv[4])
DEBUG = os.environ.get("DEBUG")
W, H = 1080, 1920
Y0, Y1 = 1300, 1424          # caption band (letters + outline + shadow)

so = ort.SessionOptions(); so.intra_op_num_threads = int(os.environ.get("THREADS", "2"))
sess = ort.InferenceSession(os.path.expanduser("~/models/lama_fp32.onnx"), so)

def caption_mask(f, excl=None):
    m = np.zeros((H, W), np.uint8)
    band = f[Y0 - 10:Y1 + 10]
    white = (band.min(-1) > 225).astype(np.uint8)
    dark = (band.max(-1) < 80).astype(np.uint8)
    near_dark = cv2.dilate(dark, np.ones((13, 13), np.uint8))
    txt = white & near_dark
    # only rows of the letter bodies
    txt[:10 + 8] = 0; txt[-(10 + 14):] = 0
    if excl is not None: txt[excl[Y0 - 10:Y1 + 10] > 0] = 0
    cols = txt.sum(0)
    xs = np.nonzero(cols >= 2)[0]
    if len(xs) < 8: return m, None
    # keep the cluster around the centre (captions are centred)
    c = W // 2; xs = xs[np.abs(xs - c) < 520]
    if len(xs) < 8: return m, None
    # grow outwards from the centre through gaps < 70px
    left = right = c
    sx = np.sort(xs)
    l = sx[sx <= c]; r = sx[sx >= c]
    if len(l):
        left = l[-1]
        for v in l[::-1]:
            if left - v > 45: break
            left = v
    if len(r):
        right = r[0]
        for v in r:
            if v - right > 45: break
            right = v
    hw = max(c - left, right - c) + 22
    if hw < 40: return m, None
    x0, x1 = max(0, c - hw), min(W, c + hw)
    m[Y0:Y1, x0:x1] = 255
    return m, (x0, Y0, x1, Y1)

def arrow_mask(f):
    b, g, r = [f[..., i].astype(np.int16) for i in range(3)]
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    hh, ss, vv = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    red = (((hh <= 5) | (hh >= 175)) & (ss > 150) & (vv > 110)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(red)
    m = np.zeros((H, W), np.uint8)
    for i in range(1, n):
        x, y, w, h, a = st[i]
        # the arrow: a big, solid red shape near the caption area
        if a > 1500 and 900 < y + h / 2 < 1800 and a / (w * h) > 0.2:
            hull = cv2.convexHull(np.column_stack(np.nonzero(lab == i)[::-1]).astype(np.int32))
            cv2.fillConvexPoly(m, hull, 255)
    if m.any():
        # fill the arrow shape, then grow over its thick black outline and shadow
        cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(m, cnts, -1, 255, -1)
        m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (75, 75)))
    return m

def lama(img, mask):
    """img BGR uint8 crop, mask uint8 crop -> inpainted crop (same size)"""
    h, w = mask.shape
    i5 = cv2.resize(img, (512, 512), interpolation=cv2.INTER_AREA)
    m5 = (cv2.resize(mask, (512, 512), interpolation=cv2.INTER_NEAREST) > 0).astype(np.float32)
    x = cv2.cvtColor(i5, cv2.COLOR_BGR2RGB).astype(np.float32).transpose(2, 0, 1)[None] / 255
    out = sess.run(None, {"image": x, "mask": m5[None, None]})[0][0]
    out = out.transpose(1, 2, 0)
    if out.max() > 2: out = out / 255
    out = cv2.cvtColor((np.clip(out, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    return cv2.resize(out, (w, h), interpolation=cv2.INTER_CUBIC)

def inpaint(f, m):
    ys, xs = np.nonzero(m)
    if len(ys) == 0: return f
    cx, cy = (xs.min() + xs.max()) // 2, (ys.min() + ys.max()) // 2
    side = int(max(xs.max() - xs.min(), ys.max() - ys.min()) * 1.45) + 60
    side = min(max(side, 512), W)
    x0 = int(np.clip(cx - side // 2, 0, W - side)); y0 = int(np.clip(cy - side // 2, 0, H - side))
    crop = f[y0:y0 + side, x0:x0 + side]; mc = m[y0:y0 + side, x0:x0 + side]
    mc_d = cv2.dilate(mc, np.ones((9, 9), np.uint8))
    fill = lama(crop, mc_d)
    a = cv2.GaussianBlur(mc_d.astype(np.float32) / 255, (0, 0), 3)[..., None]
    out = f.copy()
    out[y0:y0 + side, x0:x0 + side] = (fill * a + crop * (1 - a)).astype(np.uint8)
    return out

cap = cv2.VideoCapture(SRC)
ff = None if DEBUG else subprocess.Popen(
    ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "50", "-i", "-",
     "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
n = 0
while True:
    ok, f = cap.read()
    if not ok or n >= F1: break
    if n >= F0:
        am = arrow_mask(f) if n < 205 else np.zeros((H, W), np.uint8)
        cm, box = caption_mask(f, cv2.dilate(am, np.ones((41, 41), np.uint8)) if am.any() else None)
        m = cm.copy()
        out = f
        both = cv2.bitwise_or(cm, am)
        if both.any(): out = inpaint(out, both)
        if DEBUG:
            cv2.imwrite(f"{OUT}_{n:04d}.jpg", np.hstack([f, out])[::2, ::2])
        else:
            ff.stdin.write(out.tobytes())
        if n % 50 == 0 or DEBUG: print(n, box, bool(am.any()), flush=True)
    n += 1
if ff: ff.stdin.close(); ff.wait()
