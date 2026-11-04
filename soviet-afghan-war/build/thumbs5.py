import cv2, numpy as np, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

W, H = 1920, 1080
SLAB = "fonts/AlfaSlabOne.ttf"; SANS = "fonts/ArchivoBlack.ttf"; DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def bg(path, fx=0.5, fy=0.5, sky=True):
    im = ImageOps.fit(Image.open(path).convert("RGB"), (W, H), centering=(fx, fy))
    im = ImageEnhance.Color(im).enhance(1.25)
    a = np.asarray(im).astype(np.float32)
    if sky:  # push the top towards a pale blue sky like the reference
        g = np.clip(1 - np.arange(H) / (H * 0.55), 0, 1)[:, None, None] ** 1.5
        a = a * (1 - 0.55 * g) + np.array([178, 214, 232]) * 0.55 * g
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")

def sepia(im):
    """pseudo-colourise a b&w cutout so it sits in a colour illustration"""
    a = np.asarray(im).astype(np.float32); g = a[..., :3].mean(-1, keepdims=True) / 255
    lo, mid, hi = np.array([45, 32, 25]), np.array([196, 150, 118]), np.array([250, 240, 228])
    c = np.where(g < 0.5, lo + (mid - lo) * (g / 0.5), mid + (hi - mid) * ((g - 0.5) / 0.5))
    out = np.concatenate([c, a[..., 3:]], -1)
    return Image.fromarray(out.clip(0, 255).astype(np.uint8), "RGBA")

def place(base, key, x, y, h=None, w=None, crop=None, flip=False, bw=False, shadow=True):
    im = Image.open(f"cut/{key}.png").convert("RGBA")
    if crop: im = im.crop(crop)
    im = im.crop(im.getbbox())
    if flip: im = ImageOps.mirror(im)
    if bw: im = sepia(im)
    if h: im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    elif w: im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel("A").point(lambda v: int(v * 0.45)))
        base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (x + 10, y + 12))
    base.alpha_composite(im, (x, y))
    return im.size

def flag(base, x, y, s=1.0):
    d = ImageDraw.Draw(base)
    d.line((x, y, x, y + int(140 * s)), fill=(70, 55, 40), width=int(6 * s))
    d.polygon([(x, y), (x + int(90 * s), y + int(10 * s)), (x + int(84 * s), y + int(42 * s)), (x, y + int(52 * s))], fill=(214, 30, 30))
    d.text((x + int(14 * s), y + int(8 * s)), "☭", font=ImageFont.truetype(DJ, int(28 * s)), fill=(255, 215, 0))

def cartoon(im):
    a = cv2.cvtColor(np.asarray(im.convert("RGB")), cv2.COLOR_RGB2BGR)
    s = a.copy()
    for _ in range(4): s = cv2.bilateralFilter(s, 9, 40, 9)
    # flatten colours
    q = (s // 20) * 20 + 10
    q = cv2.addWeighted(s, 0.45, q.astype(np.uint8), 0.55, 0)
    g = cv2.medianBlur(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), 7)
    e = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 5)
    e = cv2.erode(255 - e, np.ones((2, 2), np.uint8)); e = 255 - e
    e = cv2.GaussianBlur(e, (3, 3), 0)
    out = (q.astype(np.float32) * (e[..., None].astype(np.float32) / 255 * 0.85 + 0.15))
    out = cv2.cvtColor(out.clip(0, 255).astype(np.uint8), cv2.COLOR_BGR2RGB)
    out = ImageEnhance.Color(Image.fromarray(out)).enhance(1.2)
    return ImageEnhance.Contrast(out).enhance(1.08).convert("RGBA")

def badge(base, cx, cy, r=78):
    b = Image.new("RGBA", (r * 2 + 12, r * 2 + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse((0, 0, r * 2 + 11, r * 2 + 11), fill=(245, 245, 240), outline=(30, 30, 30), width=4)
    inner = Image.new("RGBA", (r * 2 - 10, r * 2 - 10)); di = ImageDraw.Draw(inner); n = r * 2 - 10
    di.rectangle((0, 0, n // 2, n), fill=(210, 28, 28))
    di.rectangle((n // 2, 0, n // 2 + n // 6, n), fill=(20, 20, 20))
    di.rectangle((n // 2 + n // 6, 0, n // 2 + n // 3, n), fill=(200, 25, 25))
    di.rectangle((n // 2 + n // 3, 0, n, n), fill=(20, 130, 50))
    di.text((n // 4, n // 2), "☭", font=ImageFont.truetype(DJ, int(r * 0.9)), fill=(255, 215, 0), anchor="mm")
    m = Image.new("L", (n, n), 0); ImageDraw.Draw(m).ellipse((0, 0, n - 1, n - 1), fill=255)
    b.paste(inner, (11, 11), m)
    d.ellipse((11, 11, 11 + n, 11 + n), outline=(30, 30, 30), width=3)
    base.alpha_composite(b, (cx - r - 6, cy - r - 6))

def text_block(base, lines, right=1860, top=60, halo=True):
    """lines: (text, font, size, colour)"""
    y = top
    for t, font, size, col in lines:
        f = ImageFont.truetype(font, size)
        while f.getbbox(t)[2] > 1000: size -= 6; f = ImageFont.truetype(font, size)
        if halo:
            hl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(hl).text((right, y), t, font=f, fill=(255, 255, 255, 230), anchor="ra", stroke_width=14, stroke_fill=(255, 255, 255, 230))
            base.alpha_composite(hl.filter(ImageFilter.GaussianBlur(10)))
        ImageDraw.Draw(base).text((right, y), t, font=f, fill=col, anchor="ra", stroke_width=3, stroke_fill=(255, 255, 255))
        y += int(size * 1.08)

def save(base, name):
    base.convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"thumb/{name}.jpg", quality=95)

BLACK = (18, 16, 14); RED = (200, 25, 25)


def scene(name, bgp, bfx, bfy, person, pcrop=None, pbw=False, px=150, ph=900, title=(), right=1690, top=80,
          heli=(640, 400, 420), group=None, tank=True, flags=True, extra=None):
    b = bg(bgp, bfx, bfy)
    if tank:
        place(b, "t62_withdraw", -80, 560, w=480, crop=(0, 0, 1600, 520))
    if flags:
        for i, x in enumerate((10, 120, 230)): flag(b, x, 400 + i * 10, 1.1)
    if group: place(b, group[0], group[1], group[2], h=group[3], crop=group[4] if len(group) > 4 else None)
    if extra: extra(b)
    if heli: place(b, "hind_soviet", heli[0], heli[1], w=heli[2])
    place(b, person, px, H - ph, h=ph + 20, crop=pcrop, bw=pbw)
    b = cartoon(b)
    text_block(b, title, right=right, top=top)
    badge(b, 1815, 150)
    save(b, name)

T = lambda a, b, c: [(a, SLAB, 190, BLACK), (b, SLAB, 190, BLACK), (c, SANS, 105, BLACK)]
scene("T1_afghan_war", "img/panjshir.jpg", 0.5, 0.6, "massoud5", title=T("AFGHAN", "WAR", "1979 – 1989"),
      group=("muj_1985", 1120, 500, 600))
scene("T2_ussr_vietnam", "img/mountains_hk.jpg", 0.5, 0.7, "brezhnev", pbw=True, px=120, ph=880,
      title=[("THE USSR'S", SLAB, 150, BLACK), ("VIETNAM", SLAB, 190, RED), ("1979 – 1989", SANS, 105, BLACK)],
      group=("spetsnaz", 980, 640, 420))
scene("T3_lion_of_panjshir", "img/panjshir_bld.jpg", 0.5, 0.6, "massoud3", pcrop=(0, 0, 820, 1067), px=60, ph=980, tank=False, flags=False,
      title=[("LION OF", SLAB, 170, BLACK), ("PANJSHIR", SLAB, 190, BLACK), ("9 SOVIET ATTACKS", SANS, 90, RED)],
      group=("shigal", 980, 600, 440), heli=(1450, 500, 360))
scene("T4_last_soviet_soldier", "img/withdraw_644461.jpg", 0.5, 0.6, "withdraw_660671", pcrop=(0, 0, 820, 760), pbw=True, px=60, ph=820,
      title=[("THE LAST", SLAB, 170, BLACK), ("SOVIET", SLAB, 190, RED), ("SOLDIER · 1989", SANS, 100, BLACK)],
      group=("muj_1985", 1300, 560, 520), heli=(930, 560, 360))
scene("T5_graveyard_of_empires", "img/nuristan.jpg", 0.5, 0.5, "gorby_reyk", px=120, ph=860,
      title=[("GRAVEYARD", SLAB, 170, BLACK), ("OF EMPIRES", SLAB, 170, RED), ("USSR 1979 – 1989", SANS, 95, BLACK)],
      group=("muj_guerilla", 1120, 560, 520))
