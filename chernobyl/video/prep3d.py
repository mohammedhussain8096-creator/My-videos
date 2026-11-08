"""Pre-render every 'three' scene in the plan with headless Chromium + three.js.  Usage: python3 prep3d.py [preview_seconds]"""
import json, os, subprocess, sys
os.environ.setdefault('RES', '1920x1080')
import render as R
lim = float(sys.argv[1]) if len(sys.argv) > 1 else 1e9
jobs = []
for i, (sc, sp) in enumerate(zip(R.TIMING['scenes'], R.SCENES)):
    if sp['kind'] != 'three' or sc['start'] >= lim: continue
    dur = sc['end'] - sc['start']; D = dur + sp.get('_t0', 0) + sp.get('_tail', 0)
    nf = int(round(sc['end'] * R.FPS)) - int(round(sc['start'] * R.FPS)) + 1
    jobs.append(dict(out=os.path.join(R.OUT, 'three', f'{i + 1:03d}'), shot=sp['shot'], params=sp.get('params', {}), t0=sp.get('_t0', 0), D=D, frames=nf, fps=R.FPS))
jf = os.path.join(R.OUT, 'three_jobs.json'); json.dump(jobs, open(jf, 'w'))
print(len(jobs), 'jobs,', sum(j['frames'] for j in jobs), 'frames', flush=True)
env = dict(os.environ, NODE_PATH=subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip())
subprocess.run(['node', os.path.join(R.HERE, 'three', 'render3d.js'), jf], check=True, env=env)
