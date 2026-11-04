"""Generates one comic-style illustration per scene with DreamShaper 8 LCM (CreativeML OpenRAIL-M licence,
commercial use allowed), on CPU. Writes images/NNN.png. Map scenes are skipped (the renderer draws those).

Usage: python3 gen_images.py FIRST LAST      (env HF_HOME for the model cache, STEPS, SEED)"""
import json, os, re, sys, time
import torch
from diffusers import StableDiffusionPipeline, LCMScheduler

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('IMAGES', os.path.join(HERE, 'images'))
STEPS = int(os.environ.get('STEPS', 8))
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

def main():
    first, last = int(sys.argv[1]), int(sys.argv[2])
    vis = {}
    for line in open(os.path.join(HERE, '..', 'visuals.txt')):
        if re.match(r'^\d+ \|', line):
            n, setc, visual, text, cam, bg = [p.strip() for p in line.split(' | ')]
            vis[int(n)] = (setc, visual)
    os.makedirs(OUT, exist_ok=True)
    pipe = StableDiffusionPipeline.from_pretrained('Lykon/dreamshaper-8-lcm', torch_dtype=torch.float32,
                                                   safety_checker=None, requires_safety_checker=False)
    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
    pipe.set_progress_bar_config(disable=True)
    for n in range(first, last + 1):
        setc, visual = vis[n]
        path = os.path.join(OUT, f'{n:03d}.png')
        if setc == 'MAP' or os.path.exists(path): continue
        prompt = STYLE + PROMPTS.get(str(n), visual_prompt(visual))
        t = time.time()
        im = pipe(prompt, negative_prompt=NEG, num_inference_steps=STEPS, guidance_scale=1.8, width=768, height=432,
                  generator=torch.Generator().manual_seed(SEED + n)).images[0]
        w, h = im.size
        im = im.crop((int(w * 0.03), int(h * 0.03), int(w * 0.97), int(h * 0.97)))   # trim any frame the model draws
        im.save(path)
        print(f'scene {n} {time.time() - t:.0f}s', flush=True)

if __name__ == '__main__':
    main()
