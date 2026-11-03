# Video renderer

Turns the production script (`../chunks.json` voice lines + `../visuals.txt` scene plan) into a finished
animatic MP4 in the reference video's style.

```bash
pip install piper-tts fonttools brotli scipy numpy pillow   # plus ffmpeg on the PATH
python3 setup_assets.py          # map imagery, fonts, narrator voice, character cut-out -> ./assets
python3 tts.py                   # narration.wav + timing.json in ./build (about 30 min of audio)
python3 render.py                # renders every scene and writes build/Why_Egypt_Never_Died.mp4
python3 render.py 1 15           # or just a range of scenes (Batch 1)
```

Options (environment variables): `RES=1280x720` for a faster, smaller render, `WORKERS=4` parallel scenes,
`VOICE=path/to/other-piper-voice.onnx`, `LENGTH_SCALE` for voice speed, `OUT_DIR`, `EGYPT_ASSETS`.

The scene cuts follow the built-in voice's timing. To use your own recorded or AI voice, the simplest
route is to import the MP4 into an editor, replace the audio, and nudge the cuts to match.
