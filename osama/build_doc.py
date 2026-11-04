"""Builds the production files for "The Hunt for Osama bin Laden" from chunks.json + visuals.txt
(+ the real narration timing in timing.json when it exists)."""
import csv, json, os, re
import spoken

HERE = os.path.dirname(os.path.abspath(__file__))
chunks = json.load(open(os.path.join(HERE, 'chunks.json')))
beats = json.load(open(os.path.join(HERE, 'beats.json')))
vis = {}
for line in open(os.path.join(HERE, 'visuals.txt')):
    if re.match(r'^\d+ \|', line):
        n, setc, visual, text, cam, bg = [p.strip() for p in line.split(' | ')]
        vis[int(n)] = dict(set=setc, visual=visual, text=text, cam=cam, bg=bg)
N = len(chunks); assert len(vis) == N
tpath = os.path.join(HERE, 'timing.json')
if os.path.exists(tpath):
    sc = json.load(open(tpath))['scenes']; START = [s['start'] for s in sc] + [sc[-1]['end']]
else:
    RATE = 3.86; START = [0.0]
    for c in chunks: START.append(START[-1] + spoken.stats(c)[1] / RATE)
DUR = [START[i + 1] - START[i] for i in range(N)]
tc = lambda t: f'{int(t // 60):02d}:{t % 60:04.1f}'

# which part each scene belongs to
wb = []
for bi, b in enumerate(beats): wb += [bi] * len(b['text'].split())
pos = 0; PART = []
for c in chunks:
    PART.append(beats[wb[pos]]['part']); pos += len(c.replace('//', '').split())

STYLE = ('Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, '
         'no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic')
MAP_STYLE = ('Dark intelligence-style map: near-black sea, dark slate land, thin blue-grey borders, the featured country lit amber with a glowing edge, '
             'red pins with pulsing rings and white condensed labels, faint grid, film grain')

md = []; w = md.append
w('# The Hunt for Osama bin Laden: Scene-by-Scene Production Script\n')
w(f'**Format:** 16:9, 1920×1080, 24 fps · **Scenes:** {N} (5–8 s each, average {sum(DUR) / N:.1f} s) · '
  f'**Runtime:** ≈ {START[-1] / 60:.1f} min · **Voice:** Kokoro `am_puck`, speed 0.85, the same voice and settings in every batch\n')
w('## 1. Visual style: realistic documentary reconstruction\n')
w('| Element | Rule |')
w('|---|---|')
w('| Images | Realistic, cinematic stills like a documentary reconstruction: natural light, real places and objects, 35 mm film look with light grain. One image per scene, held with a slow push-in. Generated with DreamShaper 8 LCM (CreativeML OpenRAIL-M licence, commercial use allowed). |')
w('| Maps | Dark intelligence-style map: the country in focus lit amber with a glowing edge, red pins dropping in with pulsing rings and white labels, routes as dashed red lines. The map zooms in from a wide view. |')
w('| Captions | Documentary lower third: white condensed capitals (Oswald) with a red bar, bottom left, over a soft dark gradient. |')
w('| Titles | Big white condensed capitals with a short red line underneath, centred, for key moments and numbers (2,977 counts up). |')
w('| Dates | A typewriter-style date stamp slides in at the top left whenever a full date is spoken. |')
w('| Pace | A new picture every 5–8 s; captions change with the narration. Cuts are hard cuts. |')
w('| Disclosure | A small "Dramatized reconstruction · AI-generated images" note at the start (YouTube also asks creators to label realistic AI content). |')
w('| Sensitive moments | 9/11 is shown as skyline and smoke, never impacts or people. The raid uses silhouettes, flashes and night-vision tints: no wounds, no body. Real people appear as silhouettes, from behind or in shadow, never as realistic faces; bin Laden is always a faceless silhouette, as your script asks. |\n')
w('## 2. Voice (same in every batch)\n')
w('| Setting | Value |')
w('|---|---|')
w('| Voice | Kokoro `am_puck` (the voice you approved for the Egypt video) |')
w('| Speed | 0.85, about 140 words per minute: calm, not fast and not slow |')
w('| Pauses | 0.38 s after each sentence, 0.85 s after each paragraph |')
w('| Processing | Light EQ and compression only, identical for the whole video |')
w('| Music | Original tense bed (D minor, 84 BPM, composed in code), ducked under the voice |\n')
w('## 3. Image prompts\n')
w(f'Every illustration prompt below starts with this style line:\n\n> {STYLE}\n\nMap scenes use:\n\n> {MAP_STYLE}\n')
w('Save each generated image as `osama/video/images/NNN.png` (e.g. `007.png` for scene 7). The renderer uses it instead of its own drawing and keeps the camera moves, captions, calendar and timing.\n')
w('## 4. Scenes\n')
rows = []; cur = None
for i in range(N):
    n = i + 1; v = vis[n]
    if PART[i] != cur:
        cur = PART[i]; w(f'### {cur}\n')
    vo = chunks[i].replace(' // ', ' … ')
    prompt = (MAP_STYLE if v['set'] == 'MAP' else STYLE) + '. ' + v['visual']
    w(f'#### Scene {n:03d} · {tc(START[i])}–{tc(START[i + 1])} ({DUR[i]:.1f} s) · {v["set"]}\n')
    w(f'**VO:** "{vo}"\n')
    w(f'- **Visual:** {v["visual"]}')
    w(f'- **On-screen text:** {v["text"]}')
    w(f'- **Camera / animation:** {v["cam"]}')
    w(f'- **Image prompt:** `{prompt}`\n')
    rows.append(dict(scene=n, start=tc(START[i]), end=tc(START[i + 1]), seconds=f'{DUR[i]:.1f}', set=v['set'], voice_line=vo,
                     visual=v['visual'], on_screen_text=v['text'], camera=v['cam'], image_prompt=prompt))
open(os.path.join(HERE, 'Osama_Production_Script.md'), 'w').write('\n'.join(md))
with open(os.path.join(HERE, 'scenes.csv'), 'w', newline='') as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
vo = ['THE HUNT FOR OSAMA BIN LADEN: VOICE-OVER BY SCENE', 'Voice am_puck, speed 0.85. "..." = paragraph pause.', '']
cur = None
for i in range(N):
    if PART[i] != cur: cur = PART[i]; vo += ['', f'===== {cur} =====']
    vo.append(f'[{i + 1:03d} | {tc(START[i])}] {chunks[i].replace(" // ", " ... ")}')
open(os.path.join(HERE, 'voiceover_script.txt'), 'w').write('\n'.join(vo) + '\n')
print('ok', N, 'scenes', round(START[-1] / 60, 1), 'min')
