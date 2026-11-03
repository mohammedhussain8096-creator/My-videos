"""Builds chunks.json for the full script.
Part 1 (Hook -> Cleopatra) was split first and is kept fixed (scenes 1-175).
Part 2 (from "Egypt became part of the Roman Empire." to the end) is split the same way and appended.
Each part gets hand fixes so a picture cut never lands inside a phrase."""
import json, os, subprocess, sys
OPS1 = [('R', 6, 2), ('R', 7, 4), ('L', 12, 2), ('R', 30, 2), ('R', 31, 2), ('R', 42, 2), ('L', 46, 3), ('L', 50, 4),
        ('R', 74, 1), ('R', 87, 3), ('R', 95, 3), ('L', 99, 1), ('L', 109, 2), ('R', 120, 4), ('R', 121, 3),
        ('L', 130, 4), ('R', 135, 2), ('L', 138, 2), ('R', 141, 2), ('L', 145, 3), ('R', 150, 4)]
OPS2 = [('R', 2, 3), ('R', 13, 2), ('R', 14, 5), ('R', 19, 1), ('R', 27, 1), ('L', 33, 3), ('R', 38, 2), ('R', 42, 1),
        ('R', 48, 3), ('L', 49, 2), ('R', 52, 2), ('R', 62, 2), ('L', 67, 3)]
SPLIT = "Egypt became part of the Roman Empire."

def run(src, out):
    env = dict(os.environ, SRC=src, OUT=out)
    subprocess.run([sys.executable, 'chunk.py'], env=env, check=True, stdout=subprocess.DEVNULL)
    return json.load(open(out))

def apply(chunks, ops):
    c = [s.split() for s in chunks]
    def clean(ws):
        while ws and ws[0] == '//': ws.pop(0)
        while ws and ws[-1] == '//': ws.pop()
        return ws
    for op, i, k in sorted(ops, key=lambda o: o[1]):
        a, b = c[i - 1], c[i]
        take = []
        if op == 'R':
            while len(take) < k:
                w = b.pop(0); take.append(w) if w != '//' else a.append('//')
            a += take
        else:
            while len(take) < k:
                w = a.pop(); take.insert(0, w) if w != '//' else b.insert(0, '//')
            b[:0] = take
        c[i - 1], c[i] = clean(a), clean(b)
    return [' '.join(x) for x in c]

full = open('script.txt').read()
k = full.index(SPLIT)
open('.part1.txt', 'w').write(full[:full.index(' province, run by')] + '\n')   # part 1 exactly as it was split before (the old, cut-off script)
open('.part2.txt', 'w').write(full[k:])
p1 = apply(run('.part1.txt', '.p1.json'), OPS1)
assert p1[-1].startswith(SPLIT), p1[-1]
p2 = apply(run('.part2.txt', '.p2.json'), OPS2)
chunks = p1[:-1] + p2
for f in ('.part1.txt', '.part2.txt', '.p1.json', '.p2.json'):
    os.remove(f)
assert ' '.join(' '.join(chunks).replace('//', '').split()) == ' '.join(full.split())
json.dump(chunks, open('chunks.json', 'w'), indent=0)
print(len(chunks), 'scenes')
