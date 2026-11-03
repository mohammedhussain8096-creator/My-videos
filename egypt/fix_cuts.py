"""Hand fixes after chunk.py: move words across scene boundaries so picture cuts don't split a phrase.
('R', i, k): pull first k words of scene i+1 to the end of scene i.  ('L', i, k): push last k words of scene i to scene i+1."""
import json
OPS = [('R', 6, 2), ('R', 7, 4), ('L', 12, 2), ('R', 30, 2), ('R', 31, 2), ('R', 42, 2), ('L', 46, 3), ('L', 50, 4), ('R', 74, 1), ('R', 87, 3), ('R', 95, 3), ('L', 99, 1), ('L', 109, 2), ('R', 120, 4), ('R', 121, 3), ('L', 130, 4), ('R', 135, 2), ('L', 138, 2), ('R', 141, 2), ('L', 145, 3), ('R', 150, 4)]
c = [s.split() for s in json.load(open('chunks.json'))]
def clean(ws):
    while ws and ws[0] == '//': ws.pop(0)
    while ws and ws[-1] == '//': ws.pop()
    return ws
for op, i, k in sorted(OPS, key=lambda o: o[1]):
    a, b = c[i - 1], c[i]
    if op == 'R':
        take = []
        while len(take) < k:
            w = b.pop(0); take.append(w) if w != '//' else a.append('//')
        a += take
    else:
        take = []
        while len(take) < k:
            w = a.pop(); take.insert(0, w) if w != '//' else b.insert(0, '//')
        b[:0] = take
    c[i - 1], c[i] = clean(a), clean(b)
json.dump([' '.join(x) for x in c], open('chunks.json', 'w'), indent=0)
