import sys, json, types, importlib.machinery
_m=types.ModuleType("spacy"); _m.__spec__=importlib.machinery.ModuleSpec("spacy", None); sys.modules.setdefault("spacy", _m)
import torch, numpy as np, soundfile as sf
from kokoro import KPipeline
torch.set_num_threads(4)
d = sys.argv[1]; lines = json.load(open(f"{d}/lines.json", encoding="utf-8"))
p = KPipeline(lang_code='h'); voice = p.load_voice('hm_omega'); SR = 24000
lead = 0.3; out = [np.zeros(int(lead*SR), np.float32)]; t = lead; tm = []
for row in lines:
    lid, text, pause = row[:3]; disp = row[3] if len(row) > 3 else text
    a = np.concatenate([np.asarray(c) for _,_,c in p(text, voice=voice, speed=0.95)]).astype(np.float32)
    # trim leading/trailing silence
    idx = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, idx[0]-240): idx[-1]+480]
    sf.write(f"{d}/{lid}.wav", a, SR)
    tm.append({"id": lid, "text": disp, "start": round(t,3), "end": round(t+len(a)/SR,3)})
    out += [a, np.zeros(int(pause*SR), np.float32)]; t += len(a)/SR + pause
    print(lid, round(len(a)/SR,2), flush=True)
sf.write(f"{d}/vo_full.wav", np.concatenate(out), SR)
json.dump({"duration": round(t,3), "lines": tm}, open(f"{d}/timing.json","w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("TOTAL", round(t,2))
