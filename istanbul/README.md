# Istanbul: The Golden City of Three Empires

Animated explainer in the style of the reference video: warm satellite maps with handwritten labels, a grey
studio where the guide stands beside diagrams, flat cartoon scenes, and a spotlight stage. The user's
character is the guide (drawing unchanged; only moved: walk-in, sway, talking bounce, spear pointing, hops).
Voice: Kokoro `am_fenrir` (locked), speed 0.85.

- `Istanbul_Preview.mp4`: the first 2:14 (scenes 1-22)
- `video/build/timing.json` -> 161 scenes, 16:13 of narration

```bash
cd video
python3 ../extract.py ../Istanbul_Script.docx   # run from istanbul/: narration.json
python3 setup_map.py     # warm satellite map (needs the Natural Earth zip)
python3 tts.py           # narration + 4-8 s scene split
MUSIC_SECONDS=980 OUT_DIR=build python3 music.py
python3 render.py preview 128     # or: python3 render.py
```
