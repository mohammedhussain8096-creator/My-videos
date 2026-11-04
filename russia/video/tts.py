"""Narration + scene split.

Synthesises the voice-over with the Kokoro voice `am_puck` (the same voice and settings as the Egypt
video), phrase by phrase, so every phrase has an exact start/end in the audio. Phrases are then grouped
into 4-8 second scenes; a new script paragraph (new ON SCREEN cue) always starts a new scene.

Outputs in OUT_DIR: narration.wav, timing.json, and ../scenes.csv (scene list with timecodes).
LIMIT_SEC=130 stops after ~2 minutes of narration (preview)."""
import csv, json, os, re, subprocess, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import spoken

ASSETS = os.environ.get('RU_ASSETS', os.path.join(HERE, 'assets'))
OUT = os.environ.get('OUT_DIR', os.path.join(HERE, 'build'))
KVOICE = os.environ.get('KVOICE', 'am_fenrir')   # voice locked by the user for all videos
KSPEED = float(os.environ.get('KSPEED', 0.85))
VOICE_FX = 'highpass=f=60,equalizer=f=150:t=q:w=1:g=1.5,acompressor=threshold=-20dB:ratio=2.5:attack=10:release=150:makeup=1.5'
GAP_CLAUSE, GAP_SENT, GAP_PARA = 0.22, 0.38, 0.85
LEAD_IN, TAIL = 0.6, 2.5
MIN_S, MAX_S = 4.0, 8.0
LIMIT_SEC = float(os.environ.get('LIMIT_SEC', 0))
FPS = 24

SAY = {'Kyiv': 'Keev', "Rus'": 'Roos', 'Tsar': 'Zar', 'Tsars': 'Zars', 'tsars': 'zars', 'Tsar\'s': 'Zar\'s',
       'Minard\'s': 'Mee-nar\'s', 'Minard': 'Mee-nar', 'Berezina': 'Beh-reh-zee-na', 'Neman': 'Neh-man',
       'Kutuzov': 'Koo-too-zoff', 'Yermak': 'Yer-mak', 'Pozharsky': 'Po-zhar-skee', 'Ugra': 'Oo-gra',
       'Ryazan': 'Ree-ah-zan', 'Arktika': 'Ark-tee-ka', 'Baikonur': 'By-ko-noor', 'Baikal': 'By-kal',
       'Leonov': 'Lay-oh-noff', 'Tereshkova': 'Teh-resh-ko-va', 'Grande': 'Grahnd', 'Armée': 'Ar-may',
       'Laika': 'Lie-ka', 'Ladoga': 'Lah-do-ga'}

def say(t):
    t = spoken.expand(t)
    t = re.sub(r'(\d+)(st|nd|rd|th)\b', lambda m: m.group(1), t)
    def fix(m):
        w = m.group(0)
        return SAY.get(w, w)
    return re.sub(r"[A-Za-zé']+", fix, t)

def phrases(paras):
    """-> list of (text, para_index, gap_after)"""
    out = []
    for pi, p in enumerate(paras):
        txt = p['text'].replace('St. Petersburg', 'Saint Petersburg')
        sents = re.findall(r'[^.?!]+[.?!]+["”]?|[^.?!]+$', txt)
        sents = [s.strip() for s in sents if s.strip()]
        for si, s in enumerate(sents):
            parts = [s]
            if len(s.split()) > 12:          # split long sentences at a comma/colon near the middle
                parts = split_long(s)
            for k, ph in enumerate(parts):
                last_s = si == len(sents) - 1
                gap = GAP_CLAUSE if k < len(parts) - 1 else (GAP_PARA if last_s else GAP_SENT)
                out.append([ph, pi, gap])
    return out

def split_long(s):
    w = s.split()
    if len(w) <= 12: return [s]
    cands = [i for i, x in enumerate(w[:-3]) if i >= 3 and re.search(r'[,:;]$', x)]
    if not cands:   # no comma: break before a joining word
        cands = [i - 1 for i, x in enumerate(w[:-3]) if i >= 4 and x.lower() in ('and', 'but', 'while', 'where', 'before', 'after', 'carrying')]
    if not cands: return [s]
    i = min(cands, key=lambda i: abs(i - len(w) / 2))
    return split_long(' '.join(w[:i + 1])) + split_long(' '.join(w[i + 1:]))

def main():
    paras = json.load(open(os.path.join(HERE, '..', 'narration.json')))
    phs = phrases(paras)
    from kokoro_onnx import Kokoro
    kk = Kokoro(os.path.join(ASSETS, 'kokoro', 'kokoro-v1.0.onnx'), os.path.join(ASSETS, 'kokoro', 'voices-v1.0.bin'))
    sr = 24000
    audio = [np.zeros(int(LEAD_IN * sr), np.int16)]
    t = LEAD_IN
    timed = []
    for n, (text, pi, gap) in enumerate(phs):
        a, _ = kk.create(say(text), voice=KVOICE, speed=KSPEED, lang='en-us')
        pcm = (np.clip(a, -1, 1) * 32767).astype(np.int16)
        nz = np.nonzero(np.abs(pcm) > 300)[0]
        if len(nz): pcm = pcm[max(0, nz[0] - int(0.03 * sr)): nz[-1] + int(0.08 * sr)]
        d = len(pcm) / sr
        timed.append({'text': text, 'para': pi, 'start': t, 'end': t + d})
        audio.append(pcm); t += d
        audio.append(np.zeros(int(gap * sr), np.int16)); t += gap
        if n % 25 == 0: print(f'phrase {n + 1}/{len(phs)}  t={t:.1f}s', flush=True)
        if LIMIT_SEC and t > LIMIT_SEC and gap == GAP_PARA: break
    audio.append(np.zeros(int(TAIL * sr), np.int16)); t += TAIL
    total = t
    # group phrases into scenes: optimal partition, every scene 4-8 s, cuts preferred at paragraph changes
    starts = [p['start'] for p in timed] + [total - TAIL + 0.6]
    n = len(timed)
    def cost(i, j):          # scene = phrases i..j-1
        d = starts[j] - starts[i]
        c = 0.0 if MIN_S <= d <= MAX_S else 50 * (max(MIN_S - d, d - MAX_S) + 0.3) ** 2
        c += 0.05 * (d - 6.2) ** 2
        c += 3.0 * len({timed[k]['para'] for k in range(i, j)} - {timed[i]['para']})   # mixing cues
        if j < n and timed[j - 1]['end'] and not re.search(r'[.?!]["”]?$', timed[j - 1]['text']): c += 0.6
        return c
    best = [0.0] + [1e18] * n; back = [0] * (n + 1)
    for j in range(1, n + 1):
        for i in range(max(0, j - 6), j):
            v = best[i] + cost(i, j)
            if v < best[j]: best[j], back[j] = v, i
    cuts, j = [], n
    while j: cuts.append((back[j], j)); j = back[j]
    scenes = [timed[i:j] for i, j in reversed(cuts)]
    rows = []
    for i, sc in enumerate(scenes):
        start = 0.0 if i == 0 else sc[0]['start'] - 0.12
        rows.append({'scene': i + 1, 'part': paras[sc[0]['para']]['part'], 'cue': paras[sc[0]['para']]['cue'],
                     'para': sc[0]['para'], 'text': ' '.join(p['text'] for p in sc), 'start': round(start, 3)})
    for i, r in enumerate(rows):
        r['end'] = rows[i + 1]['start'] if i + 1 < len(rows) else round(total, 3)
        r['dur'] = round(r['end'] - r['start'], 2)
    os.makedirs(OUT, exist_ok=True)
    pcm = np.concatenate(audio)
    raw = os.path.join(OUT, 'narration_raw.wav')
    with wave.open(raw, 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(pcm.tobytes())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af', VOICE_FX, '-ar', '48000',
                    os.path.join(OUT, 'narration.wav')], check=True)
    hop = sr // FPS
    f = pcm[: len(pcm) // hop * hop].astype(np.float32).reshape(-1, hop)
    env = np.sqrt((f ** 2).mean(axis=1)); env = np.clip(env / (np.percentile(env, 95) + 1e-6), 0, 1)
    json.dump({'total': total, 'scenes': rows, 'phrases': timed, 'envelope': [round(float(x), 3) for x in env]},
              open(os.path.join(OUT, 'timing.json'), 'w'))
    if not LIMIT_SEC:
        with open(os.path.join(HERE, '..', 'scenes.csv'), 'w', newline='') as fh:
            w = csv.writer(fh)
            w.writerow(['scene', 'start', 'end', 'seconds', 'part', 'voice-over', 'on-screen cue (from script)'])
            for r in rows:
                w.writerow([r['scene'], tc(r['start']), tc(r['end']), r['dur'], r['part'], r['text'], r['cue']])
    d = [r['dur'] for r in rows]
    print(f'done: {total:.1f}s, {len(rows)} scenes, min {min(d)} max {max(d)} mean {np.mean(d):.2f}')

def tc(s):
    return f'{int(s // 60)}:{s % 60:05.2f}'

if __name__ == '__main__':
    main()
