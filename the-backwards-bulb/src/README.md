# Rebuilding the video

1. `npm i three@0.160.0`, `pip install piper-tts numpy`; download the Piper voice `en_US-ryan-high` into `voice/` and Poppins ExtraBold into `fonts/`.
2. Synthesize one WAV per line of `lines.txt` into `vo/01.wav …` with Piper (`--length-scale 0.96`), then `python3 mkvo.py` (builds `vo.wav` + `timing.json`).
3. `python3 -m http.server 8765`, then `node render.js 0 1548 frames` (Playwright + headless Chromium renders `scene.js` frame by frame).
4. `python3 mkaudio.py` builds the soundtrack: it expects the music bed and effect clips separated from the two reference videos (Demucs for voice removal, then a harmonic/percussive split) in `../sep/`. Then encode `frames/` + `mix2.wav` with ffmpeg at 30 fps.
