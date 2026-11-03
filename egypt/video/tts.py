"""Narration: synthesise the voice-over sentence by sentence with Piper (offline TTS)
and work out when each scene starts from the real audio.

Output (in OUT_DIR): narration.wav, timing.json {scenes:[{start,end}], fps, envelope:[...]}"""
import json, os, re, sys, wave
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import spoken
from piper import PiperVoice, SynthesisConfig

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.environ.get('EGYPT_ASSETS', os.path.join(HERE, 'assets'))
OUT = os.environ.get('OUT_DIR', os.path.join(HERE, 'build'))
VOICE = os.environ.get('VOICE', os.path.join(ASSETS, 'voices', 'en_US-ryan-high.onnx'))
LENGTH_SCALE = float(os.environ.get('LENGTH_SCALE', 1.2))   # ~155 words per minute
GAP_SENT, GAP_PARA, LEAD_IN, TAIL = 0.25, 0.7, 0.5, 2.0
FPS = 24
LIMIT = int(os.environ.get('LIMIT_SCENES', 0))               # render only the first N scenes (sample)

# Fix words the TTS voice tends to mispronounce (spelled as they should sound).
SAY = {
    "Ma'at": 'Mah-aht', 'Deshret': 'Desh-ret', 'Kemet': 'Keh-met', 'Djoser': 'Joe-ser', 'Sneferu': 'Sneh-feh-roo',
    'Khufu': 'Koo-foo', 'Khafre': 'Kaf-ray', 'Menkaure': 'Men-cow-ray', 'Seqenenre': 'Seck-en-en-ray',
    'Hatshepsut': 'Hat-shep-soot', 'Thutmose': 'Thoot-mo-seh', 'Ahmose': 'Ah-mose', 'Kamose': 'Kah-mose',
    'Hyksos': 'Hick-soss', 'Avaris': 'Avv-a-riss', 'Faiyum': 'Fy-yoom', 'Nilometers': 'Ny-lom-eh-ters',
    'Piye': 'Pee-yeh', 'Psamtik': 'Sam-tick', 'Necho': 'Nee-ko', 'Nectanebo': 'Neck-ta-nee-bo', 'Siwa': 'See-wa',
    'Ptolemy': 'Tol-eh-mee', "Ptolemy's": "Tol-eh-mee's", 'Ptolemies': 'Tol-eh-meez', 'Fustat': 'Foos-taht',
    'al-Qahira': 'al Kah-hee-ra', 'al-Azhar': 'al Az-har', 'Amr': 'Ahmr', 'ibn': 'ibn', 'al-As': 'al Ahs',
    'Jalut': 'Ja-loot', 'Selim': 'Seh-leem', 'Champollion': 'Shahm-pol-yon', 'Zaghloul': 'Zag-lool',
    'Amarna': 'A-mar-na', 'Akhenaten': 'Ah-ken-ah-ten', "Akhenaten's": "Ah-ken-ah-ten's", 'Aten': 'Ah-ten',
    'Tutankhaten': 'Too-tank-ah-ten', 'Tutankhamun': 'Too-tank-ah-moon', 'Horemheb': 'Hor-em-heb',
    'Mentuhotep': 'Men-too-ho-tep', 'Amenhotep': 'Ah-men-ho-tep', 'Imhotep': 'Im-ho-tep', 'Narmer': 'Nar-mer',
    'Philae': 'Fy-lee', 'Copts': 'Kopts', 'Coptic': 'Kop-tick', 'Caesarion': 'See-zair-ee-on', 'Carchemish': 'Kar-keh-mish',
    'Cambyses': 'Kam-by-seez', 'Pelusium': 'Peh-loo-see-um', 'Megiddo': 'Meh-gid-o', 'Deir': 'Dair', 'el-Bahari': 'el Ba-har-ee',
}

def say(text):
    t = spoken.expand(text)
    t = t.replace(' B C', ' B.C.').replace('A D ', 'A.D. ')
    return ' '.join(SAY.get(w.strip('.,;:!?"'), None) and w.replace(w.strip('.,;:!?"'), SAY[w.strip('.,;:!?"')]) or w
                    for w in t.split())

def main():
    chunks = json.load(open(os.path.join(HERE, '..', 'chunks.json')))
    if LIMIT: chunks = chunks[:LIMIT]
    words = []   # (word, scene, para_end)
    for si, c in enumerate(chunks):
        toks = c.split()
        for k, w in enumerate(toks):
            if w == '//':
                if words: words[-1][2] = True
                continue
            words.append([w, si, False])
    words[-1][2] = True
    # sentences
    sents, cur = [], []
    for w in words:
        cur.append(w)
        if re.search(r'[.?!]["”]?$', w[0]) or w[2]:
            sents.append(cur); cur = []
    if cur: sents.append(cur)
    voice = PiperVoice.load(VOICE)
    cfg = SynthesisConfig(length_scale=LENGTH_SCALE)
    sr = voice.config.sample_rate
    audio = [np.zeros(int(LEAD_IN * sr), np.int16)]
    t = LEAD_IN
    scene_start = {}
    for n, s in enumerate(sents):
        text = ' '.join(w[0] for w in s)
        pcm = np.concatenate([np.frombuffer(ch.audio_int16_bytes, np.int16) for ch in voice.synthesize(say(text), syn_config=cfg)])
        # trim silence the model adds at the edges
        nz = np.nonzero(np.abs(pcm) > 300)[0]
        if len(nz): pcm = pcm[max(0, nz[0] - int(0.03 * sr)): nz[-1] + int(0.06 * sr)]
        dur = len(pcm) / sr
        syl = [max(1, spoken.stats(w[0])[1]) for w in s]
        tot = sum(syl); acc = 0
        for w, sy in zip(s, syl):
            if w[1] not in scene_start:
                scene_start[w[1]] = t + dur * acc / tot - (0.15 if acc else 0.25)
            acc += sy
        audio.append(pcm); t += dur
        gap = GAP_PARA if s[-1][2] else GAP_SENT
        audio.append(np.zeros(int(gap * sr), np.int16)); t += gap
        if n % 20 == 0: print(f'sentence {n + 1}/{len(sents)}  t={t:.1f}s', flush=True)
    audio.append(np.zeros(int(TAIL * sr), np.int16)); t += TAIL
    pcm = np.concatenate(audio)
    os.makedirs(OUT, exist_ok=True)
    with wave.open(os.path.join(OUT, 'narration.wav'), 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(pcm.tobytes())
    starts = [max(0.0, scene_start[i]) for i in range(len(chunks))]
    starts[0] = 0.0
    ends = starts[1:] + [len(pcm) / sr]
    # per-frame loudness for the Guide's "talking" bounce
    hop = sr // FPS
    f = pcm[: len(pcm) // hop * hop].astype(np.float32).reshape(-1, hop)
    env = np.sqrt((f ** 2).mean(axis=1)); env = np.clip(env / (np.percentile(env, 95) + 1e-6), 0, 1)
    json.dump({'fps': FPS, 'scenes': [{'start': round(a, 3), 'end': round(b, 3)} for a, b in zip(starts, ends)],
               'envelope': [round(float(x), 3) for x in env]}, open(os.path.join(OUT, 'timing.json'), 'w'))
    print('done', round(len(pcm) / sr, 1), 's')

if __name__ == '__main__':
    main()
