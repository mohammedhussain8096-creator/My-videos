import cv2, numpy as np, onnxruntime as ort, subprocess, sys, os

SRC, OUT = sys.argv[1], sys.argv[2]
F0, F1 = int(sys.argv[3]), int(sys.argv[4])
DEBUG = os.environ.get("DEBUG")
W, H = 1080, 1920
BY0, BY1 = 1270, 1430          # caption band
FPS = "30000/1001"

so = ort.SessionOptions(); so.intra_op_num_threads = int(os.environ.get("THREADS", "1"))
sess = ort.InferenceSession(os.path.expanduser("~/models/lama_fp32.onnx"), so)
K = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))

# ---------------------------------------------------------------- masks
def caption_mask(f):
    """tight mask that follows the white letters + their black outline"""
    m = np.zeros((H, W), np.uint8)
    band = f[BY0:BY1].astype(np.int16)
    mn, mx = band.min(-1), band.max(-1)
    white = ((mn > 228) & (mx - mn < 28)).astype(np.uint8)
    dark = (mx < 80).astype(np.uint8)
    near_dark = cv2.dilate(dark, K(6))
    n, lab, st, cen = cv2.connectedComponentsWithStats(white)
    letters = []
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a < 25 or h < 10 or h > 120 or w > 160: continue
        comp = (lab[y:y + h, x:x + w] == i).astype(np.uint8)
        ring = cv2.dilate(comp, K(3)) - comp
        nd = near_dark[y:y + h, x:x + w]
        # caption letters are surrounded by a black outline
        if ring.sum() and (ring & nd).sum() / ring.sum() > 0.55:
            letters.append((x, y, w, h, i))
    if not letters: return m, None
    # chain letters outward from the centre (captions are centred, single line)
    letters.sort(key=lambda t: t[0])
    cx = W // 2
    mids = [abs((x + w / 2) - cx) for x, y, w, h, i in letters]
    k = int(np.argmin(mids))
    if mids[k] > 260: return m, None
    keep = [letters[k]]
    L = R = k
    while L > 0 and keep[0][0] - (letters[L - 1][0] + letters[L - 1][2]) < 40:
        L -= 1; keep.insert(0, letters[L])
    while R < len(letters) - 1 and letters[R + 1][0] - (keep[-1][0] + keep[-1][2]) < 40:
        R += 1; keep.append(letters[R])
    sel = np.isin(lab, [t[4] for t in keep]).astype(np.uint8)
    if sel.sum() < 150: return m, None
    grown = cv2.dilate(sel, K(12))
    darkish = (mx < 120).astype(np.uint8)
    grown |= (darkish & cv2.dilate(sel, K(18)))       # outline remnants
    grown = cv2.dilate(grown, K(4))
    sh = np.zeros_like(grown); sh[6:] = grown[:-6]    # soft drop shadow below the letters
    grown |= sh
    m[BY0:BY1] = grown * 255
    ys, xs = np.nonzero(m)
    return m, (xs.min(), ys.min(), xs.max(), ys.max())

def ring_mask(f, n):
    m = np.zeros((H, W), np.uint8)
    if n > 70: return m
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    red = (((h <= 8) | (h >= 172)) & (s > 110) & (v > 120)).astype(np.uint8)
    nn, lab, st, _ = cv2.connectedComponentsWithStats(red)
    for i in range(1, nn):
        x, y, w, hh, a = st[i]
        if w > 120 and hh > 120 and a < 0.4 * w * hh:      # a big thin ring
            m[lab == i] = 255
    return cv2.dilate(m, K(20)) if m.any() else m

def bubble_mask(f, n):
    m = np.zeros((H, W), np.uint8)
    if n < 640: return m
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    blue = ((h >= 95) & (h <= 115) & (s > 120) & (v > 150)).astype(np.uint8)
    blue[:700] = 0; blue[1150:] = 0
    nn, lab, st, _ = cv2.connectedComponentsWithStats(blue)
    found = False
    for i in range(1, nn):
        x, y, w, hh, a = st[i]
        if a > 150 and 330 < x + w / 2 < 760:
            pts = np.column_stack(np.nonzero(lab == i)[::-1]).astype(np.int32)
            cv2.fillConvexPoly(m, cv2.convexHull(pts), 255); found = True
    if found:
        m = cv2.dilate(m, K(10))
        # "COMMENT" label typed under the bubble (white text with soft shadow)
        lab_ = f[1040:1130, 360:720].astype(np.int16)
        wt = ((lab_.min(-1) > 225) & (lab_.max(-1) - lab_.min(-1) < 30)).astype(np.uint8)
        if wt.sum() > 20:
            ys, xs = np.nonzero(wt)
            m[1040 + ys.min() - 14:1040 + ys.max() + 16, 360 + xs.min() - 16:360 + xs.max() + 18] = 255
    return m

# ---------------------------------------------------------------- inpainting
def lama512(img, mask):
    x = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32).transpose(2, 0, 1)[None] / 255
    mm = (mask > 0).astype(np.float32)[None, None]
    x = x * (1 - mm)                                   # hide the overlay from the model
    out = sess.run(None, {"image": x, "mask": mm})[0][0].transpose(1, 2, 0)
    if out.max() > 2: out = out / 255
    return cv2.cvtColor((np.clip(out, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)

def fill_tile(out, todo, sub, cx, cy, side=512):
    tx = int(np.clip(cx - side // 2, 0, W - side)); ty = int(np.clip(cy - side // 2, 0, H - side))
    crop = out[ty:ty + side, tx:tx + side].copy(); mc = todo[ty:ty + side, tx:tx + side]
    if side == 512:
        fill = lama512(crop, mc)
    else:
        fill = cv2.resize(lama512(cv2.resize(crop, (512, 512), interpolation=cv2.INTER_AREA),
                                  cv2.resize(mc, (512, 512), interpolation=cv2.INTER_NEAREST)), (side, side),
                          interpolation=cv2.INTER_CUBIC)
    part = sub[ty:ty + side, tx:tx + side]
    al = cv2.GaussianBlur(part.astype(np.float32) / 255, (0, 0), 1.5)[..., None]
    out[ty:ty + side, tx:tx + side] = (fill * al + crop * (1 - al)).astype(np.uint8)
    todo[ty:ty + side, tx:tx + side][part > 0] = 0

def inpaint(f, m):
    """each overlay region filled separately, at native resolution where it fits"""
    out = f.copy(); todo = m.copy()
    n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(m, K(20)))
    for i in range(1, n):
        x, y, w, h, _a = st[i]
        grp = ((lab == i) & (m > 0)).astype(np.uint8) * 255
        if not grp.any(): continue
        if w <= 430 and h <= 430:
            fill_tile(out, todo, grp, x + w // 2, y + h // 2)
        elif h <= 430:
            cs = list(range(x + 150, x + w - 150 + 1, 260)) or [x + w // 2]
            if cs[-1] < x + w - 150: cs.append(x + w - 150)
            for c in cs:
                sub = grp.copy(); sub[:, :max(0, c - 150)] = 0; sub[:, c + 150:] = 0
                sub &= todo
                if sub.any(): fill_tile(out, todo, sub, c, y + h // 2)
        else:
            side = min(int(max(w, h) * 1.3), W)
            fill_tile(out, todo, grp, x + w // 2, y + h // 2, side)
    return out

# ---------------------------------------------------------------- main loop
cap = cv2.VideoCapture(SRC)
ff = None if DEBUG else subprocess.Popen(
    ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", FPS, "-i", "-",
     "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
prev_f = prev_out = prev_m = None
n = 0
while True:
    ok, f = cap.read()
    if not ok or n >= F1: break
    if n >= max(0, F0 - 3):          # warm-up frames for temporal smoothing
        cm, box = caption_mask(f)
        m = cm if os.environ.get("CAPTIONS_ONLY") else (cm | ring_mask(f, n) | bubble_mask(f, n))
        out = inpaint(f, m) if m.any() else f.copy()
        # temporal smoothing of filled pixels where the scene is still
        if prev_out is not None and m.any():
            both = (m > 0) & (prev_m > 0)
            if both.any():
                ctx = (cv2.dilate(m, K(25)) > 0) & (m == 0)
                motion = np.abs(f.astype(np.int16) - prev_f.astype(np.int16)).mean(-1)
                still = cv2.GaussianBlur((motion < 6).astype(np.float32), (0, 0), 6)
                if ctx.any() and motion[ctx].mean() < 10:
                    wgt = (0.45 * still * both)[..., None]
                    out = (out * (1 - wgt) + prev_out * wgt).astype(np.uint8)
        prev_f, prev_out, prev_m = f, out, m
        if n >= F0:
            if DEBUG:
                cv2.imwrite(f"{OUT}_{n:04d}.jpg", np.hstack([f, out])[::2, ::2])
            else:
                ff.stdin.write(out.tobytes())
            if n % 40 == 0 or DEBUG: print(n, box, int((m > 0).sum()), flush=True)
    n += 1
if ff: ff.stdin.close(); ff.wait()
