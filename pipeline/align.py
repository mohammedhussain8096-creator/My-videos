"""Align caption word timings in timing.json to the spoken audio in vo.wav (run after mkvo.py)."""
from faster_whisper import WhisperModel
import wave, numpy as np, json, re, difflib
w = wave.open('vo.wav'); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
a = np.interp(np.arange(0, len(a), 22050 / 16000), np.arange(len(a)), a).astype(np.float32)
segs, _ = WhisperModel('small.en', device='cpu', compute_type='int8').transcribe(a, word_timestamps=True)
norm = lambda s: re.sub(r"[^a-z0-9']", '', s.lower())
hw = [(norm(x.word), x.start) for s in segs for x in s.words]
T = json.load(open('timing.json'))
sw = [(li, wi, norm(w['w'])) for li, L in enumerate(T['lines']) for wi, w in enumerate(L['words'])]
sm = difflib.SequenceMatcher(None, [x[2] for x in sw], [x[0] for x in hw], autojunk=False); n = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for i, j in zip(range(i1, i2), range(j1, j2)):
            li, wi, _ = sw[i]; L = T['lines'][li]; L['words'][wi]['s'] = round(min(max(hw[j][1], L['s'] - 0.05), L['e']), 3); n += 1
for L in T['lines']:
    ws = L['words']
    for i in range(len(ws)):
        if i and ws[i]['s'] <= ws[i - 1]['s']: ws[i]['s'] = round(ws[i - 1]['s'] + 0.08, 3)
    for i in range(len(ws)): ws[i]['e'] = ws[i + 1]['s'] if i + 1 < len(ws) else round(min(L['e'] + 0.12, ws[i]['s'] + 0.9), 3)
json.dump(T, open('timing.json', 'w'), indent=1); print('aligned', n, 'of', len(sw))
