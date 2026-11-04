"""Splits script.txt into 5-8 s scenes (chunk.py) and applies hand fixes so no cut lands inside a phrase.
('R', i, k): pull the first k words of scene i+1 onto the end of scene i.  ('L', i, k): push the last k words of scene i to scene i+1."""
import json, subprocess, sys
OPS = [('L', 3, 2), ('R', 49, 3), ('R', 78, 1), ('L', 117, 2), ('L', 119, 5), ('R', 125, 1), ('L', 178, 2), ('L', 202, 2)]

def apply(chunks, ops):
    c = [s.split() for s in chunks]
    def clean(ws):
        while ws and ws[0] == '//': ws.pop(0)
        while ws and ws[-1] == '//': ws.pop()
        return ws
    for op, i, k in sorted(ops, key=lambda o: o[1]):
        a, b = c[i - 1], c[i]; take = []
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

subprocess.run([sys.executable, 'chunk.py'], check=True, stdout=subprocess.DEVNULL)
chunks = apply(json.load(open('chunks.json')), OPS)
assert ' '.join(' '.join(chunks).replace('//', '').split()) == ' '.join(open('script.txt').read().split())
json.dump(chunks, open('chunks.json', 'w'), indent=0)
print(len(chunks), 'scenes')
