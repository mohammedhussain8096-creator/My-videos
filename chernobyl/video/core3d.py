"""Detailed cut-away of an RBMK-1000 reactor (Chernobyl type), drawn in shaded pseudo-3D.

Modelled on the real design: a concrete shaft; a steel vessel holding a stack of graphite blocks (about 7 m tall,
12 m wide) pierced by vertical fuel channels; boiling water rising through the channels; control rods with an
absorber section and a graphite 'displacer' tip underneath; the upper biological shield 'Elena' (a huge steel disc
whose top is covered in a grid of channel caps, as in the real reactor hall photo) and the bundle of steam-water
pipes leaving the top. The vessel is cut in half by a vertical plane facing the camera.

spec keys: power (0..3+, may animate), boil (0..1), rods (0 = withdrawn, 1 = fully in; may animate),
tips_hot (highlight graphite tips), labels (bool), explode (time), blue_glow, cam (zoom 1..)"""
import math
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import sys, importlib
R = sys.modules['__main__'] if hasattr(sys.modules.get('__main__'), 'MPX') else importlib.import_module('render')
W, H, U = R.W, R.H, R.U

N_COL = 26                       # graphite columns across the cut face
def geom(zoom):
    cx = W * 0.43; Rv = 400 * U * zoom; e = 0.30                     # vessel radius and ellipse ratio (camera tilt)
    top = H * 0.40; bot = top + 470 * U * zoom
    return cx, Rv, e, top, bot

def shade(c, k):
    return tuple(int(max(0, min(255, v * k))) for v in c)

def hgrad(d, x0, x1, y0, y1, c0, c1, steps=48):
    for i in range(steps):
        xa = x0 + (x1 - x0) * i / steps; xb = x0 + (x1 - x0) * (i + 1) / steps; k = i / (steps - 1)
        d.rectangle([xa, y0, xb + 1, y1], fill=tuple(int(a + (b - a) * k) for a, b in zip(c0, c1)))

@lru_cache(8)
def static_layer(zoom):
    """everything that does not move: shaft, back half of the vessel, graphite blocks, lower plate"""
    cx, Rv, e, top, bot = geom(zoom)
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    # concrete shaft: back wall + floor, cut open toward the camera
    sw = Rv * 1.35; yt, yb = top - 230 * U * zoom, bot + 90 * U * zoom; dep = 120 * U * zoom
    hgrad(d, cx - sw, cx + sw, yt, yb, (66, 66, 63), (98, 98, 94))                                   # back wall
    d.polygon([(cx - sw - dep, yt - dep * 0.5), (cx - sw, yt), (cx - sw, yb), (cx - sw - dep, yb + dep * 0.5)], fill=(44, 44, 42))   # left wall (in shadow)
    d.polygon([(cx + sw, yt), (cx + sw + dep, yt - dep * 0.5), (cx + sw + dep, yb + dep * 0.5), (cx + sw, yb)], fill=(120, 120, 115))  # right wall (lit)
    d.polygon([(cx - sw - dep, yb + dep * 0.5), (cx - sw, yb), (cx + sw, yb), (cx + sw + dep, yb + dep * 0.5)], fill=(80, 80, 76))    # floor
    for k in range(6): d.line([cx - sw, yt + k * (yb - yt) / 6, cx + sw, yt + k * (yb - yt) / 6], fill=(56, 56, 54), width=2)
    rng = np.random.default_rng(1)
    for _ in range(900):                                             # concrete texture speckles
        x = rng.uniform(cx - sw, cx + sw); y = rng.uniform(yt, yb); r = rng.uniform(0.6, 2.2) * U
        g = int(rng.uniform(40, 120)); d.ellipse([x - r, y - r, x + r, y + r], fill=(g, g, g - 2, 120))
    for k in range(-3, 4):                                           # formwork seams
        x = cx + k * sw / 3.5; d.line([x, yt, x, yb], fill=(52, 52, 50), width=2)
    # curved inner wall of the vessel's back half: vertical shading bands give the cylinder its depth
    for k in range(40):
        u = (k + 0.5) / 40 * 2 - 1; x = cx + u * (Rv + 14 * U); wv = (Rv + 14 * U) * 2 / 40 + 1
        lum = 0.55 + 0.45 * math.cos(u * 1.3 - 0.35)
        d.rectangle([x - wv / 2, top - e * Rv * math.sqrt(max(0, 1 - u * u)), x + wv / 2, top], fill=shade((128, 134, 140), lum))
    # back half of the steel vessel wall (seen inside the cut)
    d.ellipse([cx - Rv - 14 * U, top - e * Rv - 10 * U, cx + Rv + 14 * U, top + e * Rv + 10 * U], fill=(70, 74, 78))
    hgrad(d, cx - Rv - 14 * U, cx + Rv + 14 * U, top, bot, (60, 64, 68), (120, 126, 130))
    # graphite stack on the cut face: blocks 25 cm square, 26 columns visible
    cw = 2 * Rv / N_COL; bh = cw * 1.05
    for i in range(N_COL):
        x0 = cx - Rv + i * cw; light = 0.78 + 0.35 * (i / N_COL)
        y = top
        while y < bot - 2:
            y1 = min(bot, y + bh)
            base = shade((62, 62, 64), light * (0.95 + 0.1 * rng.random()))
            d.rectangle([x0 + 1, y + 1, x0 + cw - 1, y1 - 1], fill=base)
            d.line([x0 + 2, y + 2, x0 + cw - 2, y + 2], fill=shade(base, 1.35), width=1)          # bevel highlight
            d.line([x0 + 2, y1 - 2, x0 + cw - 2, y1 - 2], fill=shade(base, 0.6), width=1)
            y = y1
    # lower plate (steel), seen as a thick slab with its back half-ellipse
    d.rectangle([cx - Rv - 14 * U, bot, cx + Rv + 14 * U, bot + 46 * U * zoom], fill=(96, 100, 104))
    d.line([cx - Rv - 14 * U, bot + 2, cx + Rv + 14 * U, bot + 2], fill=(150, 155, 160), width=int(3 * U))
    # vessel cut edges
    for x in (cx - Rv - 14 * U, cx + Rv + 14 * U):
        d.rectangle([x - 7 * U, top, x + 7 * U, bot + 46 * U * zoom], fill=(150, 156, 160))
    return img

def channel_cols():
    return [i for i in range(N_COL)]

def rod_cols():
    return [i for i in range(1, N_COL - 1) if i % 3 == 1]

def draw_core3d(sp, t, D):
    zoom = R.lerp(sp.get('cam0', 1.0), sp.get('cam1', sp.get('cam0', 1.0) * 1.04), R.ease(t / max(D, 0.1)))
    cx, Rv, e, top, bot = geom(zoom)
    # background: the real reactor hall photo, darkened (never a plain colour)
    img = R.live_bg(dict(bgimg='rbmk_ignalina_pd', grade='warm', bz0=1.15, bz1=1.25), t, D, 'rbmk_ignalina_pd', dark=0.72).convert('RGBA')
    te = sp.get('explode'); boom = R.eout((t - te) / 0.7) if te is not None and t > te else 0
    shake = (math.sin(t * 95) * 9 * U * max(0, 1 - (t - te) / 1.5)) if te is not None and t > te else 0
    layer = static_layer(round(zoom, 2))
    img.alpha_composite(layer, (int(shake), 0))
    d = ImageDraw.Draw(img)
    power = R.anim(sp.get('power', 0.5), t); boil = R.anim(sp.get('boil', 0.3), t); rods = R.anim(sp.get('rods', 0.7), t)
    cw = 2 * Rv / N_COL; ox = shake
    # fuel channels: steel tube, fuel glow (cosine power profile), water/steam
    rng = np.random.default_rng(int(t * 15))
    rc = set(rod_cols())
    for i in channel_cols():
        if i in rc: continue
        x = cx - Rv + (i + 0.5) * cw + ox; prof = math.cos((i + 0.5 - N_COL / 2) / (N_COL / 2) * 1.2)
        heat = min(1.0, power * (0.55 + 0.6 * prof))
        d.rectangle([x - cw * 0.22, top, x + cw * 0.22, bot], fill=(118, 124, 130))
        col = tuple(int(a + (b - a) * heat) for a, b in zip((60, 90, 130), (255, 150, 50)))
        d.rectangle([x - cw * 0.12, top + 6 * U, x + cw * 0.12, bot - 6 * U], fill=col)
        for _ in range(int(boil * 10 * (0.6 + prof))):                # steam bubbles rising
            by = bot - rng.uniform(0, 1) * (bot - top); br = rng.uniform(1.2, 3.2) * U
            d.ellipse([x - br, by - br, x + br, by + br], outline=(215, 235, 255), width=1)
    if power > 0.08:                                                 # heat glow over the core
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).rectangle([cx - Rv * 0.85, top + 20 * U, cx + Rv * 0.85, bot - 20 * U], fill=(255, 120, 30, int(min(220, 90 * power))))
        img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(40 * U + 30 * U * min(power, 3)))); d = ImageDraw.Draw(img)
    # control rods: boron-carbide absorber (dark) above a 4.5 m graphite displacer (light) with water below
    stroke = (bot - top) + 120 * U * zoom
    for i in rc:
        x = cx - Rv + (i + 0.5) * cw + ox
        d.rectangle([x - cw * 0.3, top, x + cw * 0.3, bot], fill=(52, 84, 112))                   # water-filled rod channel
        tip_bot = top - 120 * U * zoom + stroke * rods + 40 * U
        disp_top = tip_bot - (bot - top) * 0.62; abs_top = disp_top - (bot - top) * 0.9
        ya, yb_ = sorted((max(abs_top, top - 300 * U), disp_top)); d.rectangle([x - cw * 0.26, ya, x + cw * 0.26, yb_], fill=(40, 42, 46))      # absorber
        tipc = (255, 150, 40) if sp.get('tips_hot') else (150, 150, 140)
        ya, yb_ = sorted((disp_top, tip_bot)); d.rectangle([x - cw * 0.26, ya, x + cw * 0.26, yb_], fill=tipc)                                 # graphite tip
        d.line([x - cw * 0.26, disp_top, x + cw * 0.26, disp_top], fill=(20, 20, 20), width=2)
    if sp.get('tips_hot'):
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        for i in rc:
            x = cx - Rv + (i + 0.5) * cw + ox; tip_bot = top - 120 * U * zoom + stroke * rods + 40 * U
            gd.rectangle([x - cw, tip_bot - 60 * U, x + cw, tip_bot + 30 * U], fill=(255, 120, 30, 200))
        img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(18 * U))); d = ImageDraw.Draw(img)
    # upper biological shield 'Elena' + channel caps + steam pipes (flies off in the explosion)
    lid = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lid)
    th = 70 * U * zoom; ly = top - th
    ld.pieslice([cx - Rv - 20 * U, ly - e * Rv - 10 * U, cx + Rv + 20 * U, ly + e * Rv + 10 * U], 180, 360, fill=(150, 112, 70))   # top surface, back half (rusty steel)
    rng2 = np.random.default_rng(7)
    for gy in np.linspace(-0.92, 0.92, 15):                         # grid of channel caps in perspective
        for gx in np.linspace(-0.95, 0.95, 31):
            if gx * gx + gy * gy > 0.9 or gy > -0.04: continue
            px = cx + gx * Rv; py = ly + gy * e * Rv; s = (5.5 + 1.5 * gy) * U * zoom
            c = (210, 70, 50) if rng2.random() < 0.05 else ((230, 190, 60) if rng2.random() < 0.06 else (200, 200, 190))
            ld.rectangle([px - s, py - s * 0.7, px + s, py + s * 0.7], fill=c, outline=(60, 50, 40))
    hgrad(ld, cx - Rv - 20 * U, cx + Rv + 20 * U, ly, ly + th, (120, 124, 128), (190, 194, 198))          # slab front (cut)
    ld.line([cx - Rv - 20 * U, ly, cx + Rv + 20 * U, ly], fill=(225, 228, 230), width=int(3 * U))
    for k in range(18):                                              # steam-water pipe bundle leaving the top
        sx = cx - Rv * 0.85 + k * Rv * 1.7 / 17; side = -1 if k < 9 else 1
        pts = [(sx, ly - 6 * U)]
        for u in np.linspace(0, 1, 12):
            pts.append((sx + side * (40 + 260 * u * u) * U * zoom, ly - 6 * U - (150 + 30 * (k % 3)) * U * zoom * math.sin(u * math.pi / 2)))
        ld.line(pts, fill=(70, 72, 74), width=int(11 * U * zoom)); ld.line(pts, fill=(150, 152, 150), width=int(8 * U * zoom)); ld.line(pts, fill=(225, 226, 222), width=int(3 * U * zoom))
    if boom > 0:
        ang = 75 * boom; dy = -480 * U * boom
        lid = lid.rotate(ang, center=(cx, ly), resample=Image.BICUBIC, translate=(0, dy))
    img.alpha_composite(lid, (int(ox), 0)); d = ImageDraw.Draw(img)
    # labels with leader lines (on the right)
    if sp.get('labels', True) and boom == 0:
        items = [('UPPER SHIELD "ELENA"', ly + th * 0.4), ('STEAM PIPES', ly - 120 * U * zoom), ('GRAPHITE BLOCKS', top + (bot - top) * 0.35),
                 ('FUEL CHANNELS', top + (bot - top) * 0.6), ('CONTROL RODS', top + (bot - top) * 0.15), ('GRAPHITE TIPS', top + (bot - top) * 0.85)]
        for k, (txt, y) in enumerate(items):
            a = R.ease((t - 0.4 - k * 0.25) / 0.4)
            if a <= 0: continue
            x0 = cx + Rv + 24 * U; x1 = W * 0.80
            d.line([x0, y, x1 - 10 * U, y], fill=(255, 255, 255, int(200 * a)), width=int(2 * U)); d.ellipse([x0 - 5 * U, y - 5 * U, x0 + 5 * U, y + 5 * U], fill=(255, 200, 80))
            ti = R.text_img(txt, 'osw', 34, fill=(255, 255, 255), track=2); R.put(img, ti, x1, y - ti.height / 2, a)
    # explosion
    if te is not None and t > te:
        tt = t - te
        sm = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sm)
        for k in range(26):
            u = (k / 26 + tt * 0.08) % 1; ry = top - u * 900 * U; rr = (60 + 280 * u) * U
            rx = cx + math.sin(k * 1.7 + tt * 0.6) * 70 * U * u; g = int(30 + 30 * (1 - u))
            sd.ellipse([rx - rr, ry - rr * 0.8, rx + rr, ry + rr * 0.8], fill=(g, g, g + 4, int(230 * (1 - u * 0.7) * min(1, tt / 0.6))))
        img.alpha_composite(sm.filter(ImageFilter.GaussianBlur(24 * U)))
        fire = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fire)
        fd.ellipse([cx - Rv * 0.9, top - 300 * U, cx + Rv * 0.9, top + 120 * U], fill=(255, 140, 40, int(220 * max(0.5, 1 - tt * 0.2))))
        fd.ellipse([cx - Rv * 0.4, top - 140 * U, cx + Rv * 0.4, top + 60 * U], fill=(255, 235, 170, int(230 * max(0.3, 1 - tt * 0.4))))
        img.alpha_composite(fire.filter(ImageFilter.GaussianBlur(50 * U)))
        dd = ImageDraw.Draw(img); rr = np.random.default_rng(3)
        for _ in range(90):
            a_ = rr.uniform(-2.7, -0.45); v_ = rr.uniform(300, 1000) * U; px = cx + math.cos(a_) * v_ * tt; py = top + math.sin(a_) * v_ * tt + 520 * U * tt * tt
            r_ = rr.uniform(3, 10) * U
            if 0 < px < W and 0 < py < H: dd.rectangle([px - r_, py - r_, px + r_, py + r_], fill=(255, int(rr.uniform(100, 210)), 40) if rr.random() < .55 else (50, 46, 42))
        if sp.get('blue_glow'):
            bl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(bl).ellipse([cx - 160 * U, 0, cx + 160 * U, top], fill=(120, 170, 255, 160))
            img.alpha_composite(bl.filter(ImageFilter.GaussianBlur(60 * U)))
    # power meter (top right)
    if sp.get('meter', True):
        mx, my, mw, mh = W * 0.035, H * 0.14, 40 * U, 460 * U; dd = ImageDraw.Draw(img)
        dd.rectangle([mx, my, mx + mw, my + mh], fill=(10, 12, 14, 200), outline=(200, 200, 200), width=int(2 * U))
        f = min(1.0, power / 1.2); col = (90, 200, 120) if power < 0.6 else ((255, 176, 40) if power < 1.0 else (230, 45, 35))
        dd.rectangle([mx + 6 * U, my + mh - (mh - 12 * U) * f - 6 * U, mx + mw - 6 * U, my + mh - 6 * U], fill=col)
        ti = R.text_img('POWER', 'osw', 28, fill=(230, 230, 230), track=3); R.put(img, ti, mx + mw / 2 - ti.width / 2, my + mh + 4 * U)
    return img.convert('RGB')
