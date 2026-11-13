# My-videos: how videos are made here

This repository holds animated YouTube Shorts in the style of TheOddTrick, and the pipeline that
renders them. Read this before making or changing a video.

## Standing rules from the owner

1. **Preview first, always.** Send a 10-second preview and stop. Do not render the full video
   until the owner approves the preview.
2. **Script: best hook, high retention.**
   - Hook in the first 2 seconds: one line, mid-action, a contradiction or a mystery. No intro.
   - Plant a question in the hook and answer it only in the last seconds.
   - A new beat every 2–3 seconds (twist, number, joke, "but then").
   - Sentences of about 9 words; about 3.3 words per second; 50–55 seconds total.
   - The last line calls back to the hook.
   - Send 2–3 hook options with the preview.
3. **Music must not sound like a children's cartoon.** No bouncy ukulele or plucky comedy tunes
   ("Carefree" and "Investigations" were rejected). Use low, sparse, grown-up tracks such as
   "Cool Vibes" (the owner's pick for the channel sound), mixed about 19 dB under the voice.
4. **No repeated pop sound on text, and no synthesized background noise.** Sound effects only on
   real actions, each used sparingly. No noise-based ambience beds (crowd murmur, fire crackle,
   crickets, wind, rain hiss); the owner rejected them. Music plus discrete action sounds only.
5. **Characters: use the high-detail builder** `the-cook-who-got-paid-in-noise/src/charsHD.js`
   (`makeChar3` + `drawFaceHD`): 2K crisp faces, outlined eyes with pupils, nose, teeth and tongue,
   3D cartoon hands, 3D scarf/belt/collar options, fabric folds, and a **static outline with no
   wobble** (`BOIL.value = 0`; the owner rejected the moving border). Older note follows.
   **Characters in the reference style:** flat colour with no shading, egg-shaped body, very long
   thin legs, tiny hands, thick dark outline, big simple face. Use `makeChar2` in
   `pipeline/characters.js`. The earlier shaded, short-legged characters were rejected.
6. **Sets must be detailed and textured** (wood planks, plaster and timber, brick, cobbles). A
   plain, low-detail ship was rejected.
7. **Length:** 50–55 seconds unless told otherwise. Format: 1080×1920, 30 fps.
8. **Always put the music credit in `CREDITS.md`** next to the video (Kevin MacLeod tracks are
   CC-BY and need it).
9. Channel name chosen by the owner: **The Clever Gap** (logo, banner and description are in
   `channel-logo/the-clever-gap/`).

## Channel formula (from TheOddTrick's videos)

Seven beats: paradox hook → named nobody → a "one X, one Y" rule or sound motif → rule-of-three
escalation ending on a joke → the turn ("Then,") → "You see," explainer on a flat royal-blue
background with one oversized object and a household simile → callback ending.

On screen: one-word white captions with a black outline about 70% down the frame; two-line
keyword pops at the top (white + yellow/orange/green); red starburst for sound words; a new shot
every 2–3 seconds, each with a slow push-in or a slight tilt.

Full analysis: `the-backwards-bulb/ANALYSIS.md`.

## Pipeline (`pipeline/`)

Everything is code: Three.js scenes rendered frame by frame in headless Chromium, a synthetic
narrator, and a Python audio mix.

One-time setup in a new session: `cd pipeline && ./setup.sh` (installs Three.js, the Piper voice,
music and sound-effect packs).

Steps for a new video (work in a scratch folder with the pipeline files copied or linked in):

1. **Script** → `lines.txt`, one narration sentence per line.
2. **Voice:** for each line, `echo "$line" | python3 -m piper -m voice/en_US-ryan-high.onnx
   --length-scale 0.95 --sentence-silence 0.13 -f vo/NN.wav`, then `python3 mkvo.py`
   (builds `vo.wav` and `timing.json`), then `python3 align.py` (snaps captions to the audio).
3. **Scenes:** write a sets file and a timeline file (see `example-sets.js` and
   `example-timeline.js`, from the Google video). The timeline's `update(t)` picks the shot from
   the current narration line and word times (`wf(line, 'word')`).
4. **Assemble:** `cat engine.js paint.js head.js characters.js <sets>.js helpers.js <timeline>.js
   post.js tail.js > scene.js`.
5. **Check stills:** `python3 -m http.server 8765 &` then
   `node render.js 1.0,5.0,9.0 x stills times`. Look at them and fix framing before rendering.
6. **Preview:** render the first ~300 frames (`node render.js 0 300 frames`, split across four
   processes), build audio, encode 10 seconds, send it, and wait for approval.
7. **Full render** after approval: all frames in four parallel processes (about 1 frame/second in
   total), then `python3 mkaudio.py <track> mix.wav`, then encode:
   `ffmpeg -framerate 30 -i frames/f%05d.jpg -i mix.wav -c:v libx264 -crf 19 -pix_fmt yuv420p
   -c:a aac -b:a 192k -movflags +faststart -shortest out.mp4`.
8. **Deliver:** video, `narration.txt`, `CREDITS.md` and the assembled `src/` into a folder named
   after the video; commit and push.

Known limits: the model cannot hear audio, so sound is placed by measurement and the owner must
check it by ear. YouTube blocks video downloads from this environment; the owner uploads
reference videos instead. Facts in scripts come from memory unless checked, and should be flagged.

## Style update (12 Nov)

After analysing *Why This Gold Mine Is Worthless* and *Einstein's Math Lesson*
(`reference-analysis/gold-mine-and-einstein.md`), new videos use that look: big pure-white heads
with heavy outlines and tall coat bodies (`makeChar3`, in the king video's `src/scene.js`), cuts
every ~2 s, text on in-world props, a wide lens (fov 50–58) on street shots because the vertical
frame is narrow, and an ending that loops back into the hook. When the owner supplies their own
narration audio, use it as-is and build `timing.json` from a Whisper transcript.

## Videos so far

| Folder | Video | Status |
|---|---|---|
| `the-puddle-general/` | The Puddle General (60 s, owner's voice tightened from 85 s) | Full video; Comicron style, desert sandstone citadel (owner picked option 3 of 3 looks) |
| `why-mountain-roads-zigzag/` | Why Mountain Roads Zigzag (60 s, owner's ElevenLabs voice tightened from 82 s) | Full video; spike-video style: skin-coloured heads, 3D mountain world, in-world explainer, crash payoff |
| `the-cook-who-got-paid-in-noise/` | The Cook Who Got Paid in Noise (54 s) | Full video; high-detail sets and high-detail characters; no ambience noise |
| `the-girl-who-outsmarted-a-greedy-king/` | The Girl Who Outsmarted a Greedy King With a String (68 s, owner's own script and voice) | Full video; gold-mine/Einstein style: white heads (`makeChar3` in its src), real long shadows |
| `the-worst-plumber-in-london/` | The Worst Plumber in London (53 s) | Approved style; music is "Cool Vibes" |
| `he-owned-google-for-one-minute/` | He Owned Google for One Minute (57 s) | Music is "Cool Vibes" |
| `the-backwards-bulb/` | The Thief Who Was Beaten by a Light Bulb (52 s) | Early style, superseded |
| `the-window-that-broke-the-sky/` | Airplane windows | Preview only |
| `the-cook-who-took-off-his-trousers/` | Trawler | Preview only; characters and ship rejected |
