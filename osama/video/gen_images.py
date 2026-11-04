"""Generates one comic-style illustration per scene with DreamShaper 8 LCM (CreativeML OpenRAIL-M licence,
commercial use allowed), on CPU. Writes images/NNN.png. Map scenes are skipped (the renderer draws those).

Usage: python3 gen_images.py FIRST LAST      (env HF_HOME for the model cache, STEPS, SEED)"""
import json, os, re, sys, time
import torch
from diffusers import StableDiffusionPipeline, LCMScheduler
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('IMAGES', os.path.join(HERE, 'images'))
STEPS = int(os.environ.get('STEPS', 10))
SEED = int(os.environ.get('SEED', 21))

MODE = os.environ.get('MODE', 'real')     # 'real' (cinematic, realistic) or 'comic' (reference style)
if MODE == 'real':
    STYLE = 'cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, '
    NEG = ('cartoon, illustration, painting, drawing, anime, comic, 3d render, cgi, text, letters, words, watermark, signature, logo, '
           'blurry, deformed hands, deformed face, extra fingers, ugly, gore, blood, injury, corpse, weapon pointed at camera, close-up face')
else:
    STYLE = 'detailed comic book illustration, inked line art, cel shaded, natural colors, highly detailed, graphic novel art, '
    NEG = ('photo, photorealistic, 3d render, anime, flat vector, minimalist, halftone, dots, panel border, frame, text, letters, '
           'words, watermark, signature, logo, blurry, deformed hands, deformed face, ugly, gore, blood, injury, corpse')

# short, focused prompts (CLIP reads ~75 tokens); scenes without an entry use their visual description
PF = os.path.join(HERE, 'prompts_real.json' if MODE == 'real' else 'prompts.json')
PROMPTS = json.load(open(PF)) if os.path.exists(PF) else {}

def visual_prompt(v):
    t = re.sub(r'"[^"]*"', '', v)                     # drop quoted on-screen words
    t = re.sub(r'\b[A-Z][A-Z0-9 .,·\'-]{3,}\b', '', t)  # drop ALL-CAPS labels
    return t

FACE_MODEL = os.environ.get('FACE_MODEL', os.path.join(os.environ.get('EGYPT_ASSETS', os.path.join(HERE, 'assets')), 'yunet.onnx'))
FACE_PROMPT = ('cinematic film still, realistic detailed human face, natural skin texture, sharp clear eyes, well-shaped nose and mouth, '
               'natural expression, 35mm photo, sharp focus, ')
FACE_NEG = NEG + ', deformed eyes, asymmetric eyes, melted face, distorted face, bad anatomy, cartoon face'

def detect_faces(im):
    """faces as (x, y, w, h) in image pixels; detects on a 2x copy so small faces are found too"""
    import cv2, numpy as np
    big = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
    a = cv2.cvtColor(np.asarray(big), cv2.COLOR_RGB2BGR)
    det = cv2.FaceDetectorYN.create(FACE_MODEL, '', (a.shape[1], a.shape[0]), 0.6, 0.3, 50)
    _, faces = det.detect(a)
    out = []
    if faces is not None:
        for f in faces:
            x, y, w, h = [float(v) / 2 for v in f[:4]]
            if w >= 7: out.append((x, y, w, h, float(f[-1])))
    out.sort(key=lambda f: -f[2] * f[3])
    return out[:6]

def fix_faces(im, prompt, img2img, seed):
    """'face detailer': re-paint every detected face at 512 px and blend it back with a soft oval mask"""
    from PIL import ImageDraw, ImageFilter
    faces = detect_faces(im)
    for i, (x, y, w, h, score) in enumerate(faces):
        side = max(w, h) * 2.3
        cx, cy = x + w / 2, y + h / 2 - h * 0.05
        x0, y0 = int(max(0, cx - side / 2)), int(max(0, cy - side / 2))
        x1, y1 = int(min(im.width, cx + side / 2)), int(min(im.height, cy + side / 2))
        if x1 - x0 < 8 or y1 - y0 < 8: continue
        crop = im.crop((x0, y0, x1, y1)).resize((512, 512), Image.LANCZOS)
        strength = 0.5 if w < 40 else 0.4                         # small faces need more repainting
        fixed = img2img(FACE_PROMPT + prompt[:120], image=crop, negative_prompt=FACE_NEG, strength=strength,
                        num_inference_steps=10, guidance_scale=1.5, generator=torch.Generator().manual_seed(seed + i)).images[0]
        fixed = fixed.resize((x1 - x0, y1 - y0), Image.LANCZOS)
        mask = Image.new('L', fixed.size, 0)
        mw, mh = fixed.size
        ImageDraw.Draw(mask).ellipse((mw * 0.14, mh * 0.1, mw * 0.86, mh * 0.92), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(max(2, mw * 0.08)))
        im.paste(fixed, (x0, y0), mask)
    return im, len(faces)

def main():
    first, last = int(sys.argv[1]), int(sys.argv[2])
    only_fix = os.environ.get('FACEFIX_ONLY') == '1'          # re-touch faces on existing images, keep the picture
    vis = {}
    for line in open(os.path.join(HERE, '..', 'visuals.txt')):
        if re.match(r'^\d+ \|', line):
            n, setc, visual, text, cam, bg = [p.strip() for p in line.split(' | ')]
            vis[int(n)] = (setc, visual)
    os.makedirs(OUT, exist_ok=True); os.makedirs(os.path.join(OUT, 'orig'), exist_ok=True)
    pipe = StableDiffusionPipeline.from_pretrained('Lykon/dreamshaper-8-lcm', torch_dtype=torch.float32,
                                                   safety_checker=None, requires_safety_checker=False)
    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
    pipe.set_progress_bar_config(disable=True)
    from diffusers import StableDiffusionImg2ImgPipeline
    img2img = StableDiffusionImg2ImgPipeline(**pipe.components); img2img.set_progress_bar_config(disable=True)
    for n in range(first, last + 1):
        setc, visual = vis[n]
        path = os.path.join(OUT, f'{n:03d}.png')
        if setc == 'MAP': continue
        prompt = STYLE + PROMPTS.get(str(n), visual_prompt(visual))
        t = time.time()
        if only_fix:
            if not os.path.exists(path) or os.path.exists(os.path.join(OUT, 'orig', f'{n:03d}.png')): continue
            im = Image.open(path).convert('RGB')
        else:
            if os.path.exists(path): continue
            im = pipe(prompt, negative_prompt=NEG, num_inference_steps=STEPS, guidance_scale=1.8, width=768, height=432,
                      generator=torch.Generator().manual_seed(SEED + n)).images[0]
            w, h = im.size
            im = im.crop((int(w * 0.03), int(h * 0.03), int(w * 0.97), int(h * 0.97)))   # trim any frame the model draws
        im.save(os.path.join(OUT, 'orig', f'{n:03d}.png'))
        im, nf = fix_faces(im, PROMPTS.get(str(n), ''), img2img, SEED + n * 7)
        im.save(path)
        print(f'scene {n} {time.time() - t:.0f}s faces={nf}', flush=True)

if __name__ == '__main__':
    main()
