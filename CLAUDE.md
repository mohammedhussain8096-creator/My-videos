# My-videos: standing rules

## Narration voice (locked by the user)
### English videos
- Every English video uses the Kokoro TTS voice **`am_fenrir`** (American male), speed **0.85**, lang `en-us`,
  with the light EQ/compressor chain in `russia/video/tts.py` (`VOICE_FX`).
- Don't switch to another voice (am_puck, am_michael, etc.) unless the user explicitly asks.
- Model files: https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/
  (`kokoro-v1.0.onnx`, `voices-v1.0.bin`). `russia/video/tts.py` is the reference implementation.

### Hindi videos (locked by the user, sample #10 "Pratham expressive")
- Every Hindi video uses the **Piper** voice **`hi_IN-pratham-medium`** with `SynthesisConfig(length_scale=1.05,
  noise_scale=0.8, noise_w_scale=1.0)`, then the same `VOICE_FX` chain plus `equalizer=f=110:t=q:w=1:g=2.5`.
- `partition/video/tts.py` is the reference implementation. Model files:
  https://huggingface.co/rhasspy/piper-voices/tree/main/hi/hi_IN/pratham/medium (`pip install piper-tts`).
- Don't switch to Kokoro Hindi, a female voice or any other voice unless the user explicitly asks.
- Hindi videos use only public-domain images (see `partition/IMAGE_CREDITS.md`), no gore.

## Workflow the user expects
- Split the script into scenes of 4-8 seconds that follow the reference video's structure and style.
- Send a ~2-minute preview first, and render the full video only after the user approves it.
