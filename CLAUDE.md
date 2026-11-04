# My-videos: standing rules

## Narration voice (locked by the user)
- Every video uses the Kokoro TTS voice **`am_fenrir`** (American male), speed **0.85**, lang `en-us`,
  with the light EQ/compressor chain in `russia/video/tts.py` (`VOICE_FX`).
- Don't switch to another voice (am_puck, am_michael, etc.) unless the user explicitly asks.
- Model files: https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/
  (`kokoro-v1.0.onnx`, `voices-v1.0.bin`). `russia/video/tts.py` is the reference implementation.

## Workflow the user expects
- Split the script into scenes of 4-8 seconds that follow the reference video's structure and style.
- Send a ~2-minute preview first, and render the full video only after the user approves it.
