import json, math, subprocess, sys, os, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

W, H, FPS = 1920, 1080, 30
S = sys.argv[1] if len(sys.argv) > 1 else "."
OUT = sys.argv[2]
ONLY = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else None
TLD = json.load(open(f"{S}/" + os.environ.get("TL", "timeline.json")))
TOTAL = TLD["total"]

MARK = f"{S}/fonts/PermanentMarker.ttf"
BANG = f"{S}/fonts/Bangers-Regular.ttf"

# ---------------------------------------------------------------- shot list
# (start, image, motion, grade, [captions], [titles], extra)
# caption: (t, text)  -> handwritten top caption with red underline (replaces previous)
# title:   (t, text, sub) -> big yellow comic title, centered
SHOTS = [
    (0.00, "img/withdraw_58833.jpg", "pan_down", "warm", [(0.4, "15 FEBRUARY 1989")], [], None),
    (6.00, "maps/amu.jpg", "zoom_pin", "map", [], [], {"pin": 0, "pin_t": 0.5}),
    (11.00, "img/withdraw_644461.jpg", "zoom_in", "warm", [(1.2, "NOT A SINGLE SOVIET SOLDIER")], [], None),
    (16.20, "img/bmd1.jpg", "pan_right", "bw", [(0.2, "1979 · 80,000 MEN"), (3.25, '"A FEW MONTHS"')], [], None),
    (22.85, "img/mountains_hk.jpg", "zoom_out", "dusk", [(1.8, "A TRAP")], [], None),
    (27.85, "img/muj_1985.jpg", "zoom_in", "warm", [(1.1, "A PHANTOM ENEMY")], [(3.75, "THE SOVIET-AFGHAN WAR", "1979 – 1989")], None),
    (35.40, "img/kabul1966.jpg", "pan_left", "dark", [(0.3, "NOT AN INVASION...")], [(3.2, "A MURDER", None)], None),
    (40.50, "maps/kabul.jpg", "zoom_pin", "map", [(0.2, "1978")], [], {"pin": 0, "pin_t": 3.6}),
    (45.60, "img/saur1.jpg", "zoom_in", "warm", [(0.2, "THE SAUR REVOLUTION"), (2.6, "LAND REFORM"), (4.5, "SECULAR LAWS")], [], None),
    (51.70, "img/muj_prayer.jpg", "pan_right", "warm", [(1.3, "DEVOUT MOUNTAIN TRIBES"), (5.0, '"ATHEISTS"')], [], None),
    (58.90, "img/muj_radio.jpg", "zoom_in", "bw", [], [(1.9, "REBELLION", None)], None),
    (63.85, "img/taraki.jpg", "zoom_face", "bw", [(0.1, "NUR MUHAMMAD TARAKI"), (3.4, "MOSCOW REFUSES")], [], None),
    (69.00, "img/amin.jpg", "zoom_face", "bw", [(0.2, "THE REAL DANGER"), (5.0, "HAFIZULLAH AMIN")], [], None),
    (75.40, "img/taraki_ussr.jpg", "zoom_in", "blood", [(0.3, "SEPTEMBER 1979"), (4.8, "SMOTHERED")], [], None),
    (82.35, "img/brezhnev.jpg", "zoom_face", "bw", [(0.3, "THE KREMLIN"), (4.0, "NEW YORK?")], [], None),
    (87.40, "img/andropov.jpg", "zoom_in", "bw", [(0.2, "YURI ANDROPOV · KGB")], [(3.5, "AMIN MUST DIE", None)], None),
    (93.75, "img/palace_dvorec.jpg", "pan_right", "cold", [(0.2, "27 DECEMBER 1979"), (6.0, "TAJBEG PALACE")], [], None),
    (101.60, "img/palace_evst.jpg", "zoom_in", "dark", [(0.4, "A DINNER PARTY")], [(4.8, "POISONED", None)], None),
    (107.60, "img/amin.jpg", "zoom_face", "bw", [(0.9, "SOVIET DOCTORS SAVE HIM")], [], None),
    (113.60, "img/spetsnaz.jpg", "pan_left", "warm", [(1.6, "THE POISON FAILED")], [(4.5, "SPETSNAZ", None)], None),
    (119.40, "img/palace_storm.jpg", "zoom_in", "cold", [(1.2, "40 MINUTES"), (3.2, "OPERATION STORM-333")], [], None),
    (125.10, "img/karmal.jpg", "zoom_face", "bw", [(0.6, "BABRAK KARMAL · PUPPET"), (2.7, "THE 40TH ARMY")], [], None),
    (130.30, "img/tanks_heli.jpg", "pan_down", "dusk", [(0.4, "THE JOB IS DONE?")], [(2.5, "IT HAS JUST BEGUN", None)], None),
]

if os.environ.get("FULL"):
    sys.path.insert(0, S)
    from shots_rest import R
    LINES = {L["k"]: L for L in TLD["lines"]}
    def norm(w): return re.sub(r"[^a-z0-9]", "", w.lower())
    def at(a):
        if ":" not in a: return LINES[a]["start"]
        k, w = a.split(":", 1); n = 1
        if "#" in w: w, n = w.split("#"); n = int(n)
        hits = [ws for ws, we, ww in LINES[k]["words"] if norm(ww).startswith(norm(w))]
        if len(hits) < n: raise SystemExit(f"anchor not found: {a} in {[x[2] for x in LINES[k]['words']]}")
        return hits[n - 1]
    for st, path, mo, gk, caps, titles, extra in R:
        t0 = at(st)
        rel = lambda x: x if isinstance(x, (int, float)) else round(at(x) - t0, 3)
        caps = [(rel(t), x) for t, x in caps]
        titles = [(rel(t), x, sub) for t, x, sub in titles]
        if extra and "pin_t" in extra: extra = {"pin": 0, "pin_t": max(0.3, rel(extra["pin_t"]) - 0.2)}
        SHOTS.append((round(t0, 3), path, mo, gk, caps, titles, extra))

# ---------------------------------------------------------------- helpers
def grade(im, kind):
    im = im.convert("RGB")
    if kind == "map":
        return im
    g = ImageOps.grayscale(im)
    a = np.asarray(im).astype(np.float32) / 255
    gray = np.asarray(g).astype(np.float32)[..., None] / 255
    sat = {"warm": 0.75, "bw": 0.0, "dusk": 0.6, "dark": 0.35, "blood": 0.2, "cold": 0.5}[kind]
    a = gray + (a - gray) * sat
    # contrast curve
    a = np.clip((a - 0.5) * 1.12 + 0.5, 0, 1)
    tint = {"warm": (1.06, 1.0, 0.88), "bw": (1.07, 1.0, 0.86), "dusk": (1.12, 0.92, 0.80),
            "dark": (1.0, 0.92, 0.85), "blood": (1.25, 0.82, 0.78), "cold": (0.92, 0.98, 1.08)}[kind]
    a = a * np.array(tint, np.float32)
    if kind in ("dark", "blood"):
        a *= 0.62
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
VIG = np.clip(1 - 0.42 * np.clip(r - 0.45, 0, None) ** 1.6, 0, 1)[..., None]
rng = np.random.default_rng(3)
GRAIN = [rng.normal(0, 7, (H // 2, W // 2)).astype(np.float32) for _ in range(6)]
GRAIN = [np.asarray(Image.fromarray(g).resize((W, H), Image.BILINEAR))[..., None] for g in GRAIN]

def ease(x):
    x = min(max(x, 0), 1)
    return x * x * (3 - 2 * x)

def cover_box(iw, ih, z, fx, fy):
    """crop box of aspect W/H covering image, zoom z (>=1), focus fx,fy in 0..1"""
    if iw / ih > W / H:
        bh = ih; bw = ih * W / H
    else:
        bw = iw; bh = iw * H / W
    bw /= z; bh /= z
    x0 = (iw - bw) * fx; y0 = (ih - bh) * fy
    return (x0, y0, x0 + bw, y0 + bh)

def text_layer(text, font, size, fill, stroke, stroke_fill, shadow=True):
    f = ImageFont.truetype(font, size)
    bb = f.getbbox(text, stroke_width=stroke)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = 40
    im = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((pad - bb[0] + 6, pad - bb[1] + 8), text, font=f, fill=(0, 0, 0, 170),
                                stroke_width=stroke, stroke_fill=(0, 0, 0, 170))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(8)))
        d = ImageDraw.Draw(im)
    d.text((pad - bb[0], pad - bb[1]), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return im

def caption_layer(text):
    size = 74 if len(text) < 22 else 62
    while True:
        t = text_layer(text, MARK, size, (28, 24, 22, 255), 7, (255, 255, 255, 255))
        if t.width < 1750 or size < 40: break
        size -= 6
    # hand drawn red underline
    w = t.width - 70
    ul = Image.new("RGBA", (t.width, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(ul)
    pts = [(35 + i * w / 20, 16 + 5 * math.sin(i * 0.9) + i * 0.35) for i in range(21)]
    d.line(pts, fill=(255, 255, 255, 255), width=17, joint="curve")
    d.line(pts, fill=(200, 30, 30, 255), width=9, joint="curve")
    return t, ul

def title_layer(text, sub):
    sz = 190 if len(text) < 14 else 150
    while True:
        t = text_layer(text, BANG, sz, (255, 212, 30, 255), 12, (20, 14, 10, 255))
        if t.width < 1780 or sz < 80: break
        sz -= 10
    if sub:
        s = text_layer(sub, MARK, 70, (255, 255, 255, 255), 6, (20, 14, 10, 255))
        im = Image.new("RGBA", (max(t.width, s.width), t.height + s.height - 60), (0, 0, 0, 0))
        im.alpha_composite(t, ((im.width - t.width) // 2, 0))
        im.alpha_composite(s, ((im.width - s.width) // 2, t.height - 60))
        return im
    return t

def pin_layer(label):
    p = Image.new("RGBA", (120, 170), (0, 0, 0, 0))
    d = ImageDraw.Draw(p)
    d.ellipse((38, 150, 82, 166), fill=(0, 0, 0, 90))
    d.line((60, 70, 60, 158), fill=(60, 60, 60, 255), width=7)
    d.ellipse((24, 10, 96, 82), fill=(210, 35, 35, 255), outline=(120, 10, 10, 255), width=4)
    d.ellipse((40, 24, 58, 42), fill=(255, 150, 150, 255))
    lab = text_layer(label, MARK, 64, (40, 32, 28, 255), 6, (255, 255, 255, 255), shadow=False)
    return p, lab

# ---------------------------------------------------------------- prepare shots
prepared = []
for i, (st, path, motion, gk, caps, titles, extra) in enumerate(SHOTS):
    en = SHOTS[i + 1][0] if i + 1 < len(SHOTS) else TOTAL
    src = Image.open(f"{S}/{path}")
    base = grade(src, gk)
    # upscale small sources so zooms stay sharp-ish
    if base.width < 2400:
        k = 2400 / base.width
        base = base.resize((int(base.width * k), int(base.height * k)), Image.LANCZOS)
    if motion == "zoom_face":
        bw_, bh_ = 2400, 1350
        bg = ImageOps.fit(base, (bw_, bh_)).filter(ImageFilter.GaussianBlur(40))
        bg = ImageEnhance.Brightness(bg).enhance(0.45)
        fh = int(bh_ * 0.80); fw = int(base.width * fh / base.height)
        fg = base.resize((fw, fh), Image.LANCZOS)
        sh_ = Image.new("L", (fw + 120, fh + 120), 0); ImageDraw.Draw(sh_).rectangle((60, 60, fw + 60, fh + 60), fill=200)
        bg.paste((0, 0, 0), ((bw_ - fw) // 2 - 60 + 12, bh_ - fh - 60 + 16), sh_.filter(ImageFilter.GaussianBlur(25)))
        bg.paste(fg, ((bw_ - fw) // 2, bh_ - fh))
        base = bg; motion = "zoom_in"
    meta = json.load(open(f"{S}/{path[:-4]}.json")) if gk == "map" else None
    prepared.append(dict(st=st, en=en, base=base, motion=motion, gk=gk, idx=i,
                         caps=[(t, *caption_layer(x)) for t, x in caps],
                         titles=[(t, title_layer(x, s)) for t, x, s in titles],
                         extra=extra, meta=meta,
                         pin=pin_layer(meta["pins"][0]["label"]) if meta else None))
    print(f"shot {i+1:2d}  {st:7.2f} -> {en:7.2f}  ({en-st:4.2f}s)  {path}", file=sys.stderr)

def frame_for(sh, t):
    lt = t - sh["st"]; D = sh["en"] - sh["st"]; p = lt / D
    base = sh["base"]; iw, ih = base.size
    m = sh["motion"]; e = ease(p) * 0.6 + p * 0.4
    if m == "zoom_in":   box = cover_box(iw, ih, 1.04 + 0.14 * e, 0.5, 0.45)
    elif m == "zoom_out": box = cover_box(iw, ih, 1.20 - 0.14 * e, 0.5, 0.5)
    elif m == "zoom_face": box = cover_box(iw, ih, 1.0 + 0.12 * e, 0.5, 0.18 + 0.05 * e)
    elif m == "pan_right": box = cover_box(iw, ih, 1.15, 0.15 + 0.7 * e, 0.5)
    elif m == "pan_left":  box = cover_box(iw, ih, 1.15, 0.85 - 0.7 * e, 0.5)
    elif m == "pan_down":  box = cover_box(iw, ih, 1.05, 0.5, 0.1 + 0.75 * e)
    elif m == "zoom_pin":
        px = sh["meta"]["pins"][0]["x"] / 3840 * iw; py = sh["meta"]["pins"][0]["y"] / 2160 * ih
        z = 1.0 + 0.9 * e
        bw, bh = iw / z, iw / z * H / W
        x0 = min(max(px - bw / 2, 0), iw - bw) * e + (iw - bw) / 2 * (1 - e)
        y0 = min(max(py - bh / 2, 0), ih - bh) * e + (ih - bh) / 2 * (1 - e)
        box = (x0, y0, x0 + bw, y0 + bh)
    fr = base.transform((W, H), Image.EXTENT, box, Image.BILINEAR)
    a = np.asarray(fr).astype(np.float32)
    if sh["gk"] != "map":
        a = a * VIG + GRAIN[int(t * FPS) % len(GRAIN)]
        # subtle flicker
        a *= 1 + 0.015 * math.sin(t * 23.0)
    else:
        a = a * (0.75 + 0.25 * VIG)
    fr = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

    # map pin
    if sh["pin"]:
        pt = lt - sh["extra"]["pin_t"]
        if pt > 0:
            px = sh["meta"]["pins"][0]["x"] / 3840 * iw; py = sh["meta"]["pins"][0]["y"] / 2160 * ih
            sx = (px - box[0]) / (box[2] - box[0]) * W; sy = (py - box[1]) / (box[3] - box[1]) * H
            drop = max(0, 1 - pt / 0.35); bounce = abs(math.sin(min(pt, 0.7) * 9)) * max(0, 0.7 - pt) * 30
            pin, lab = sh["pin"]
            fr.alpha_composite(pin, (int(sx - 60), int(sy - 158 - drop * 300 - bounce)))
            la = min(1, max(0, (pt - 0.3) / 0.3))
            if la > 0:
                l2 = lab.copy(); l2.putalpha(l2.getchannel("A").point(lambda v: int(v * la)))
                fr.alpha_composite(l2, (int(sx + 40), int(sy - 120)))

    # captions (latest active one)
    cur = None
    for c in sh["caps"]:
        if lt >= c[0]: cur = c
    title_on = any(lt >= tt for tt, _ in sh["titles"])
    if cur and not title_on:
        ct, tl, ul = cur; k = lt - ct
        al = min(1, k / 0.18)
        y = 70 + int((1 - ease(k / 0.25)) * -20)
        x = (W - tl.width) // 2
        t2 = tl if al >= 1 else tl.copy()
        if al < 1: t2.putalpha(t2.getchannel("A").point(lambda v: int(v * al)))
        fr.alpha_composite(t2, (x, y))
        uw = int(ul.width * ease((k - 0.15) / 0.45))
        if uw > 4:
            fr.alpha_composite(ul.crop((0, 0, uw, ul.height)), (x, y + tl.height - 48))
    for tt, tl in sh["titles"]:
        k = lt - tt
        if k < 0: continue
        sc = 1 + 0.35 * max(0, 1 - k / 0.22) ** 2
        shake = (rng.integers(-6, 7), rng.integers(-6, 7)) if k < 0.3 else (0, 0)
        im = tl if sc == 1 else tl.resize((int(tl.width * sc), int(tl.height * sc)), Image.BILINEAR)
        if k < 0.12:
            im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * k / 0.12)))
        # darken background behind title
        fr = Image.alpha_composite(fr, Image.new("RGBA", (W, H), (0, 0, 0, int(90 * min(1, k / 0.2)))))
        fr.alpha_composite(im, ((W - im.width) // 2 + shake[0], (H - im.height) // 2 + shake[1]))
        break
    fr = fr.convert("RGB")
    # global fades
    f = min(1, t / 0.8) * min(1, (TOTAL - t) / 1.5)
    # white flash on title hits
    for tt, _ in sh["titles"]:
        k = lt - tt
        if 0 <= k < 0.12:
            fr = Image.blend(fr, Image.new("RGB", (W, H), (255, 255, 255)), 0.35 * (1 - k / 0.12))
    if f < 1:
        fr = Image.blend(Image.new("RGB", (W, H)), fr, max(f, 0))
    return fr

if ONLY:  # stills for checking
    for i in ONLY:
        sh = prepared[i - 1]
        for frac in (0.2, 0.85):
            t = sh["st"] + (sh["en"] - sh["st"]) * frac
            frame_for(sh, t).save(f"{OUT}_{i:02d}_{int(frac*100)}.jpg", quality=85)
    sys.exit()

import os
RANGE=os.environ.get('RANGE')
nf = int(TOTAL * FPS)
r0,r1=(0,nf) if not RANGE else (int(float(RANGE.split(',')[0])*FPS), int(float(RANGE.split(',')[1])*FPS))
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                       "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "17",
                       "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
si = 0
for n in range(r0, r1):
    t = n / FPS
    while si + 1 < len(prepared) and t >= prepared[si + 1]["st"]: si += 1
    ff.stdin.write(frame_for(prepared[si], t).tobytes())
    if n % 300 == 0: print(f"frame {n}/{nf}", file=sys.stderr, flush=True)
ff.stdin.close(); ff.wait()
