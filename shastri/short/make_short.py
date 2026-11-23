"""35-second Shastri short (Hindi), cut from the long video's HD scenes with new narration in the locked Pratham voice and
large typed gold-highlight subtitles. Writes Shastri_Short_16x9.mp4 (1920x1080) and Shastri_Short_9x16.mp4 (1080x1920)."""
import os, sys, io, json, subprocess, contextlib, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.join(HERE, '..', 'video'); sys.path.insert(0, V)
os.chdir(V)
LONG = os.path.join(V, 'build', 'Shastri_Tashkent_Ki_Raat.mp4'); B = os.path.join(HERE, 'build'); os.makedirs(B, exist_ok=True)
FPS = 30
# (subtitle line, source window in the long video: start, end)
LINES = [
    ('ग्यारह जनवरी, उन्नीस सौ छियासठ। रात एक बजकर बत्तीस मिनट।', 393.8, None),            # vintage clock at 1:32
    ('रूस में, प्रधानमंत्री लाल बहादुर शास्त्री की मौत हो जाती है।', 12.4, None),   # Shastri photo
    ('कुछ घंटे पहले ही, उन्होंने पाकिस्तान से समझौता किया था।', 319.0, None),  # agreement card
    ('सरकार ने कहा, दिल का दौरा।', 402.2, None),                                             # medical report
    ('लेकिन न रूस में पोस्टमार्टम हुआ, न भारत में।', 448.5, None),                      # checklist
    ('परिवार ने कहा, शरीर नीला पड़ गया था।', 465.0, None),                                     # family card
    ('और बाद में, इस मौत के दो अहम गवाह, हादसों का शिकार हो गए।', 519.4, None),
    ('और एक सरकारी दस्तावेज़, आज भी गुप्त है।', 567.0, None),                                  # secret file
    ('उस रात असल में क्या हुआ था?', 49.3, None),                                               # night map of Tashkent
    ('पूरी कहानी, लंबी वीडियो में। लिंक नीचे है।', None, None),                           # end card
]
with contextlib.redirect_stdout(io.StringIO()):
    import tts as TT
from piper import PiperVoice, SynthesisConfig
pv = PiperVoice.load(TT.PIPER_MODEL); cfg = SynthesisConfig(**TT.PIPER_CFG); sr = pv.config.sample_rate
audio, timing, t = [np.zeros(int(0.25 * sr), np.int16)], [], 0.25
for i, (txt, _, _) in enumerate(LINES):
    a = np.concatenate([np.frombuffer(c.audio_int16_bytes, np.int16) for c in pv.synthesize(TT.say(txt), syn_config=cfg)])
    nz = np.nonzero(np.abs(a) > 300)[0]; a = a[max(0, nz[0] - int(0.03 * sr)): nz[-1] + int(0.08 * sr)]
    d = len(a) / sr; timing.append((t, t + d)); audio.append(a); t += d
    gap = 0.12 if i < len(LINES) - 1 else 0.9; audio.append(np.zeros(int(gap * sr), np.int16)); t += gap
total = t; print('narration', round(total, 2), 's')
raw = os.path.join(B, 'n_raw.wav')
with wave.open(raw, 'wb') as wf: wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(np.concatenate(audio).tobytes())
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af', TT.VOICE_FX, '-ar', '48000', os.path.join(B, 'narration.wav')], check=True)
json.dump({'total': total, 'lines': [[l[0], s, e] for l, (s, e) in zip(LINES, timing)]}, open(os.path.join(B, 'timing.json'), 'w'), ensure_ascii=False)
