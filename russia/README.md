# Why Russia Is Called the Most Powerful Nation on Earth

Animated map explainer in the reference video's style: dark satellite map, orange-red country fills
with a glowing edge, year tag, drifting clouds, icons dropping onto places, army arrows, big yellow captions.
The user's character (`character_reference.png`, unchanged) is the guide in every scene.
Voice: Kokoro `am_puck` at speed 0.85, the same voice and settings as the Egypt video.

- `scenes.csv`: the full script split into 191 scenes of 4-8 seconds with timecodes (19:21 total)
- `Russia_Preview.mp4`: the first 2:05 (scenes 1-21)
- `video/plan.py`: the visuals for each scene; `video/render.py`: the renderer

```bash
cd video
pip install kokoro-onnx soundfile fonttools brotli scipy numpy pillow python-docx
python3 ../extract.py ../Russia_Script.docx   # (run from russia/) -> narration.json
python3 setup_assets.py      # map, outlines, fonts, voice model, character cut-out
python3 tts.py               # narration + scene split
python3 music.py             # original background music
python3 render.py preview 124   # or: python3 render.py   (full video)
```
