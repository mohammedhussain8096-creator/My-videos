# तेहरान पर परमाणु हमला – Hindi 3D Explainer (Reel, 9:16)

An original Hindi explainer reel that follows the same storytelling structure as the
reference video "America Iran Pe Nuclear Attack 3D Explain". The order of beats is the same:
the hook, the city, the flash, the fireball, the shockwave, radiation, the mushroom cloud, the fallout, cancer and history.
The visuals are rendered procedurally in the same muted, hazy, cinematic 3D style.
**No text is shown on screen**: there are no captions, counters, labels or watermarks.

- Output: `tehran_nuclear_hindi_4k60.mp4`, **2160×3840 (4K, 9:16) at 60 fps**, H.264 high-bitrate with AAC audio, about 2 min 14 s
- Voice: Microsoft neural multilingual male voice `fr-FR-RemyMultilingualNeural` speaking Hindi, at +8% rate (chosen from a 6-voice comparison). Override it with `VOICE=...`, `RATE=...` and `PITCH=...`.
- Sound: a synthesized cinematic drone and heartbeat, plus blast, rumble and wind SFX, with the music ducked under the voice and the mix loudness-normalized to -14 LUFS

## Scenes

| # | Visual | Narration (summary) |
|---|--------|---------------------|
| 1 | Satellite map zoom-in, pulsing target | If Iran is ever attacked with a nuclear weapon… |
| 2 | Aerial 3D city (Tehran) | Capital Tehran, about 1 crore people |
| 3 | Street POV, person, sun-like flash | First second: blinding light |
| 4 | Tilted aerial, fireball + ground ring | Fireball spreads in one second |
| 5 | Street white-out, then orange | Everything within ~1 km vaporised |
| 6 | Dust wall rushing down the street, collapse | 3 s, 2 km, buildings fall |
| 7 | Ruins, survivor turns radiation-green | Lethal radiation dose |
| 8 | Burning street, smoke, debris wind | 6 s, 3.5 km, fires everywhere |
| 9 | Skin cross-section glowing | Deep burns at 7 km |
| 10 | Aerial rings, red damage zones, cloud | 9 km, 50 lakh people, casualty estimates |
| 11 | Mushroom cloud next to an Everest-like peak | Higher than Everest |
| 12 | Ruins with falling dust | Radioactive fallout |
| 13 | Map with fallout plume | Wind carries it hundreds of km |
| 14 | Street, glowing exposed person | Exposed people may die |
| 15 | Red cells, one mutating | Cancer years later |
| 16 | Sepia 1945 cloud fading to colour | No nuke used in war since 1945 |
| 17 | Fade out with embers | Pray this day never comes |

## Rebuild

```bash
pip install edge-tts opencv-python-headless numpy
python voice.py script.json build/vo /path/to/ca.crt   # Hindi voice-over + timings.json
# 4K60, high detail (SCALE=1 gives a fast 720p30 draft)
SCALE=3 TEX=4096 FPS=60 CRF=16 python render.py build/vo/timings.json build/clips [scene ids...]
python mix.py build/vo/timings.json build/clips build tehran_nuclear_hindi_4k60.mp4 [scene ids for a partial preview]
```

To change the narration, edit `script.json`. Scene lengths follow the voice automatically.
The casualty figures are rough public estimates for a hypothetical strike. The video is
educational and anti-war in tone.
