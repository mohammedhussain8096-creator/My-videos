"""Render the short from build/timing.json: clips from the long video (muted, slight push-in), narration + music bed, and big
typed subtitles with the gold highlight (same engine as the long video). Outputs 16:9 and 9:16."""
import os, sys, io, json, subprocess, contextlib, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.join(HERE, '..', 'video'); sys.path.insert(0, V); os.chdir(V)
with contextlib.redirect_stdout(io.StringIO()):
    import render as R
B = os.path.join(HERE, 'build'); T = json.load(open(os.path.join(B, 'timing.json'))); FPS = 30
LONG = os.path.join(V, 'build', 'Shastri_Tashkent_Ki_Raat.mp4')
SRC = [393.8, 12.4, 319.0, 402.2, 448.5, 465.0, 519.4, 567.0, 49.3, None]
total = T['total']; lines = T['lines']

def clip_frames(t0, n):                                  # stream frames from the long video (no temp files)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(t0), '-t', str(n / FPS + 0.4), '-i', LONG, '-an', '-vf', f'fps={FPS}',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    last = None
    for _ in range(n):
        b = p.stdout.read(1920 * 1080 * 3)
        if len(b) == 1920 * 1080 * 3: last = np.frombuffer(b, np.uint8).reshape(1080, 1920, 3)
        yield last
    p.stdout.close(); p.wait()

frames = []
for i, (txt, s, e) in enumerate(lines):
    end = lines[i + 1][1] if i + 1 < len(lines) else total
    frames.append((i, int(round(end * FPS)) - int(round((0 if i == 0 else s) * FPS))))


def specs():
    L = [l[2] - l[1] for l in lines]
    return [
        dict(kind='card', tone='dark', clock=True, hm=(1, 31), sec0=40),
        dict(kind='photo', img='shastri_kbr', grade='bw', frame=False, z0=1.1, z1=1.28, fx0=0.62, fy0=0.06),
        dict(kind='card', tone='dark', doc=dict(title='समझौता', lines=[('भारत और पाकिस्तान', 0.3), ('10 जनवरी 1966', 1.2)], stamp=('हस्ताक्षर हुए', 2.2, 'green'))),
        dict(kind='card', tone='dark', doc=dict(title='संयुक्त मेडिकल रिपोर्ट', lines=[('कारण: दिल का दौरा', 0.4)], stamp=('आधिकारिक', 1.4, 'green'))),
        dict(kind='card', tone='dark', check=[('पोस्टमार्टम: रूस में नहीं', 0.1), ('पोस्टमार्टम: भारत में भी नहीं', 1.0)]),
        dict(kind='card', tone='dark', doc=dict(title='परिवार के मुताबिक़', lines=[('शरीर नीला पड़ गया था', 0.4)], stamp=('सवाल', 1.8, 'red'))),
        dict(kind='card', tone='dark', files=[('गवाह 1', 'डॉ. आर. एन. चुघ', 0.2), ('गवाह 2', 'निजी सेवक राम नाथ', 0.5)],
             stamps=[(0, 'सड़क हादसा', 'red', 1.4), (1, 'गाड़ी से टक्कर', 'red', 2.0)]),
        dict(kind='card', tone='red', files=[('PMO', 'शास्त्री फ़ाइल', 0.2)], stamps=[(0, 'गुप्त', 'red', 1.0)]),
        dict(kind='map', view=(37.0, 70.0, 26.0), view1=(40.6, 69.24, 12.0), pitch=48, fill=[('uzbek', 'gold', 0.3)],
             pulse=[(41.31, 69.24, 0.8, 'red')], labels=[('रूस, 1966', 42.4, 69.24, 1.0, 64)],
             ov=[('tint', '', {'at': 0.0, 'k': 0.38, 'col': (6, 12, 34)})]),
        None,
    ]
SPECS = specs()

def engine_frame(sp, t, D):
    k = sp['kind']
    if k == 'photo': img = R.draw_photo(sp, t, D)
    elif k == 'map': img = R.draw_map(sp, t, D)
    else: img = R.draw_card(sp, t, D)
    img = R.overlays(img, sp, t, D)
    return Image.fromarray(R.finish(np.asarray(img).astype(np.float32), t))

def end_card(t):
    img = R.card_bg_modern('dark', t).convert('RGBA')
    p = Image.open(os.path.join(V, 'assets', 'cut', 'shastri_face_cut.png')).convert('RGBA'); h = 900
    p = p.resize((int(p.width * h / p.height), h), Image.LANCZOS)
    g = np.asarray(ImageEnhance.Contrast(p.convert('L')).enhance(1.3), np.float32)
    rgb = Image.fromarray(np.stack([g, g * 0.97, g * 0.92], -1).clip(0, 255).astype(np.uint8)).convert('RGBA'); rgb.putalpha(p.getchannel('A'))
    img.alpha_composite(rgb, (1920 - rgb.width - 60, 1080 - h))
    k = R.ease(t / 0.6)
    ti = R.text_img('पूरी कहानी देखिए', 'bold', 110, fill=(255, 214, 60)); ti.putalpha(ti.getchannel('A').point(lambda v: int(v * k))); img.alpha_composite(ti, (80, 230))
    bt = R.text_img('लंबी वीडियो, लिंक नीचे', 'bold', 64, fill=(255, 255, 255), shadow=False); bb = bt.getchannel('A').getbbox(); bt = bt.crop(bb)
    if t > 0.5:
        a2 = R.ease((t - 0.5) / 0.4); bw, bh = bt.width + 80, bt.height + 50; btn = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
        ImageDraw.Draw(btn).rounded_rectangle([0, 0, bw - 1, bh - 1], radius=bh // 2, fill=(210, 30, 35, 255)); btn.alpha_composite(bt, (40, 25))
        pulse = 1 + 0.04 * math.sin(t * 6); btn = btn.resize((int(bw * pulse), int(bh * pulse)), Image.BICUBIC); btn.putalpha(btn.getchannel('A').point(lambda v: int(v * a2)))
        img.alpha_composite(btn, (120, 480))
    return img.convert('RGB')

def subtitle(txt, t_rel, dur, width):
    """typed subtitle with the gold highlight, wrapped to 2 lines max, centred"""
    words = txt.split(); f = R.font('bold', 74 if width > 1500 else 78); maxw = width - 160
    rows, cur = [], ''
    for w in words:
        tt = (cur + ' ' + w).strip()
        if f.getlength(tt) <= maxw or not cur: cur = tt
        else: rows.append(cur); cur = w
    rows.append(cur)
    chars = sum(len(r) for r in rows); spent = 0; out = []
    typ = max(0.6, dur * 0.75)
    for r in rows:
        at = typ * spent / chars; d = typ * len(r) / chars; spent += len(r)
        im = R.typed_highlight(r, 'bold', 74 if width > 1500 else 78, t_rel, at, fill=(255, 255, 255), dur=d)
        out.append(im)
    return out

def compose(mode):
    Wd, Hd = (1920, 1080) if mode == '16x9' else (1080, 1920)
    out = os.path.join(HERE, f'Shastri_Short_{mode}.mp4')
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{Wd}x{Hd}', '-r', str(FPS), '-i', '-',
                          '-i', os.path.join(B, 'narration.wav'), '-i', os.path.join(V, 'build', 'music.wav'),
                          '-filter_complex', f'[2:a]atrim=0:{total},volume=0.28[m];[1:a][m]amix=inputs=2:normalize=0:duration=first,afade=t=out:st={total - 0.8}:d=0.8,alimiter=limit=0.95[a]',
                          '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k',
                          '-movflags', '+faststart', '-t', str(total), out], stdin=subprocess.PIPE)
    for i, n in frames:
        txt, s, e = lines[i]; t0 = 0 if i == 0 else s
        gen = None; raw = SPECS[i]
        for f in range(n):
            t = f / FPS
            if raw is not None:
                fr = engine_frame(raw, t, n / FPS)
            else:
                fr = end_card(t)
            if mode == '16x9':
                img = fr.convert('RGBA')
                band = Image.new('RGBA', (1920, 300), (0, 0, 0, 0)); a_ = np.linspace(0, 215, 300)[:, None].repeat(1920, 1)
                band.putalpha(Image.fromarray(a_.astype(np.uint8))); img.alpha_composite(band, (0, 780))
                ybase = 880
            else:
                bg = fr.resize((int(1920 * 1920 / 1080), 1920), Image.BILINEAR).crop((0, 0, 1080, 1920)) if False else \
                     fr.resize((3413, 1920), Image.BILINEAR).crop((1166, 0, 2246, 1920)).filter(ImageFilter.GaussianBlur(30))
                bg = ImageEnhance.Brightness(bg).enhance(0.45)
                img = bg.convert('RGBA'); fg = fr.resize((1080, 608), Image.LANCZOS) if raw is not None else fr.resize((1080, 608), Image.LANCZOS)
                img.alpha_composite(fg.convert('RGBA'), (0, 560))
                hd = R.text_img('लाल बहादुर शास्त्री', 'bold', 80, fill=(255, 214, 60)); img.alpha_composite(hd, ((1080 - hd.width) // 2, 230))
                hs = R.text_img('1966 की वो रात', 'bold', 60, fill=(255, 255, 255)); img.alpha_composite(hs, ((1080 - hs.width) // 2, 340))
                ybase = 1280
            if i < len(lines) - 1 or mode == '9x16':
                rows = subtitle(txt, t - (s - t0) + 0.05, e - s, Wd)
                yy = ybase
                for r in rows:
                    if r is not None: img.alpha_composite(r, ((Wd - r.width) // 2 + 10, yy))
                    yy += 104
            p.stdin.write(np.asarray(img.convert('RGB')).tobytes())
    p.stdin.close(); p.wait(); print('wrote', out)

for m in sys.argv[1:] or ['16x9', '9x16']: compose(m)
