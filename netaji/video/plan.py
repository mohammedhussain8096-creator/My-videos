"""Visual plan for the Netaji video, keyed by scene number (the Hindi voice is locked, so the timing is final).

SC[n] = spec for scene n. SAME continues the previous scene's shot (the camera move spans both scenes).
Kinds: P(photo), MAP(...), CARD(...). Map extras: fill, routes (moving plane/submarine/car), pulse, cities, labels, arrows.
Card extras: doc (typed paper record + rubber stamp), check (crossed-out checklist), files (case-file folders + stamps).
Overlays: ('date'|'caption'|'quote'|'big'|'title'|'flash'|'fire', text, {opts}); opts: at, or w (a word: starts when it is
spoken), off, sub, x, y, dim. Only public-domain / CC0 images are used (see ../IMAGE_CREDITS.md); no gore."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
_T = json.load(open(os.path.join(os.environ.get('OUT_DIR', os.path.join(HERE, 'build')), 'timing.json')))

def wt(n, word, after=0.0):
    """time (s from the start of scene n) when `word` is spoken in scene n"""
    sc = _T['scenes'][n - 1]
    for p in _T['phrases']:
        if sc['start'] - 0.2 <= p['start'] < sc['end'] - 0.05:
            i = p['text'].find(word)
            if i >= 0 and (p['start'] - sc['start']) >= after - 9:
                return max(0.0, p['start'] - sc['start'] + (p['end'] - p['start']) * i / max(1, len(p['text'])) - 0.1)
    raise KeyError(f'scene {n}: word {word!r} not spoken')
def st(n): return _T['scenes'][n - 1]['start']
def rel(n0, n, word): return st(n) - st(n0) + wt(n, word)       # word time inside a shot that starts at scene n0

PL = {  # Hindi name, lat, lon
    'taihoku': ('ताइहोकू', 25.07, 121.55), 'tokyo': ('टोक्यो', 35.69, 139.64), 'faizabad': ('फ़ैज़ाबाद', 26.78, 82.14),
    'saigon': ('साइगॉन', 10.82, 106.66), 'tourane': ('तूरान', 16.05, 108.2), 'dairen': ('डायरेन', 38.91, 121.6),
    'singapore': ('सिंगापुर', 1.35, 103.82), 'bangkok': ('बैंकॉक', 13.75, 100.5), 'calcutta': ('कलकत्ता', 22.57, 88.36),
    'cuttack': ('कटक', 20.46, 85.88), 'gomoh': ('गोमो', 23.87, 86.15), 'peshawar': ('पेशावर', 34.01, 71.58), 'kabul': ('काबुल', 34.53, 69.17),
    'moscow': ('मॉस्को', 55.75, 37.62), 'berlin': ('बर्लिन', 52.52, 13.4), 'kiel': ('कील', 54.32, 10.13), 'delhi': ('दिल्ली', 28.61, 77.21),
    'rangoon': ('रंगून', 16.84, 96.17), 'imphal': ('इम्फाल', 24.82, 93.94), 'kohima': ('कोहिमा', 25.67, 94.11), 'portblair': ('पोर्ट ब्लेयर', 11.62, 92.73),
    'sabang': ('सबांग', 5.89, 95.32), 'vienna': ('वियना', 48.21, 16.37), 'hiroshima': ('हिरोशिमा', 34.39, 132.45), 'nagasaki': ('नागासाकी', 32.75, 129.88),
}
def city(k, at, dx=0, dy=-1, size=48): n = PL[k]; return (n[0], n[1], n[2], at, dx, dy, size)
def pin(k, at, col='red'): n = PL[k]; return (n[1], n[2], at, col)
def ll(k): return PL[k][1], PL[k][2]
def P(img, grade='bw', **kw): return dict(kind='photo', img=img, grade=grade, **kw)
def MAP(**kw): return dict(kind='map', **kw)
def CARD(**kw): return dict(kind='card', **kw)
def T(title, sub, off=3.4): return ('title', title, {'at': 0.2, 'sub': sub, 'off': off})
def cap(t, at=0.6): return ('caption', t, {'at': at})
def date(t, at=0.3): return ('date', t, {'at': at})
def big(t, sub='', **o): o.setdefault('at', 0.3); o['sub'] = sub; return ('big', t, o)
def quote(t, **o): o.setdefault('at', 0.3); return ('quote', t, o)
SAME = 'same'

SC = {
    # ---------------------------------------------------------------- शुरुआत (hook)
    1: MAP(view=(24.0, 100.0, 62.0), view1=(24.6, 121.2, 13.0), fill=[('taiwan', 'gold', 3.2)], pulse=[pin('taihoku', 3.6)],
           labels=[('ताइहोकू', 26.7, 121.55, 3.8, 60)], ov=[date('18 अगस्त 1945', 0.5)]),
    2: P('ki21b', z0=1.05, z1=1.22, fx0=0.42, fy0=0.55, fx1=0.5, ov=[date('दोपहर लगभग 2:30', 0.3), cap('जापानी की-21 बमवर्षक (इसी तरह का विमान)', 1.2)]),
    3: P('bose_nrb', z0=1.0, z1=1.16, fx0=0.5, fy0=0.36, ov=[cap('नेताजी सुभाष चंद्र बोस', wt(3, 'नेताजी'))]),
    4: P('ki21', z0=1.0, z1=1.35, fx0=0.5, fy0=0.5, ov=[('flash', '', {'w': 'धमाका'})], boom=wt(4, 'धमाका')),
    5: SAME,
    6: CARD(tone='dark', doc=dict(title='नानमोन सैनिक अस्पताल, ताइहोकू', lines=[('तारीख़: 18 अगस्त 1945', 0.5), ('मरीज़: सुभाष चंद्र बोस', 1.5),
              ('हालत: शरीर बुरी तरह जला हुआ', 2.5)], stamp=('उसी रात मृत्यु?', 4.0, 'red'))),
    7: P('ina_members', grade='bw', z0=1.0, z1=1.18, fx0=0.5, fy0=0.45, fx1=0.47, ov=[cap('नेताजी, आज़ाद हिंद फ़ौज के अफ़सरों के साथ', 0.8)]),
    8: CARD(tone='dark', check=[('हादसे की कोई तस्वीर नहीं', 0.2), ('किसी भारतीय अफ़सर ने शव नहीं देखा', wt(8, 'किसी'))]),
    9: P('bose_crowd', z0=1.0, z1=1.14, fx0=0.5, fy0=0.45, ov=[big('करोड़ों भारतीय', 'यह मानने को तैयार नहीं थे', w='कि नेताजी', y=0.62)]),
    10: CARD(tone='dark', files=[('1956', 'शाहनवाज़ समिति', 0.9), ('1970', 'खोसला आयोग', 1.7), ('1999', 'मुखर्जी आयोग', 2.5)],
             stamps=[(0, 'विमान दुर्घटना', 'green', rel(10, 11, 'विमान')), (1, 'विमान दुर्घटना', 'green', rel(10, 11, 'विमान') + 0.45),
                     (2, 'कोई दुर्घटना नहीं', 'red', rel(10, 12, 'कोई'))], dim_others=(2, rel(10, 12, 'कोई'))),
    11: SAME, 12: SAME,
    13: MAP(view=(34.0, 133.0, 26.0), view1=(35.6, 139.4, 9.0), fill=[('japan', 'gold', 0.3)], pulse=[pin('tokyo', 1.6)],
            labels=[('रेंकोजी मंदिर, टोक्यो', 36.55, 139.64, 2.0, 62)], ov=[big('80 साल', 'से रखी अस्थियाँ', w='अस्सी', dim=False, x=0.27, y=0.76)]),
    14: MAP(view=(30.0, 84.0, 42.0), view1=(36.0, 84.0, 70.0), pitch=44, pitch1=36, fill=[('india', 'india', 0.2), ('russia', 'red', wt(14, 'रूस'))], pulse=[pin('faizabad', 0.5, 'gold')],
            labels=[('फ़ैज़ाबाद', 24.6, 82.14, 0.7, 50), ('गुमनामी बाबा?', 30.0, 82.0, 1.4, 58), ('सोवियत संघ?', 52.0, 84.0, wt(14, 'रूस') + 0.3, 78)]),
    15: P('file_p1', grade='color', frame=False, z0=1.0, z1=1.25, fx0=0.5, fy0=0.25, fy1=0.55,
          ov=[cap('नेताजी से जुड़ी गुप्त सरकारी फ़ाइल (अब सार्वजनिक)', 0.6)]),
    16: CARD(tone='red', files=[('?', 'आख़िरी जाँच', 0.2)], stamps=[(0, 'आज तक नहीं हुई', 'red', wt(16, 'लेकिन'))]),
    17: CARD(bgimg='bose_nrb', ov=[('title', 'नेताजी की रहस्यमयी मौत', {'at': 0.3, 'sub': '18 अगस्त 1945: एक अनसुलझा सवाल'})], boom=0.3),
}
SC[5] = SAME
SC[4]['ov'].append(('fire', '', {'w': 'आग'}))      # the fire starts in scene 5 (same shot) when "आग" is spoken
def _word_time(sc, word):
    for p in sc['_phr']:
        i = p['text'].find(word)
        if i >= 0:
            return max(0.0, p['start'] - sc['start'] + (p['end'] - p['start']) * i / max(1, len(p['text'])) - 0.1)
    return None

def resolve(timing):
    scenes = timing['scenes']; phr = timing['phrases']
    for sc in scenes:
        sc['_phr'] = [p for p in phr if sc['start'] - 0.2 <= p['start'] < sc['end'] - 0.05]
    n = len(scenes); out = [None] * n
    i = 0
    while i < n:
        spec = SC.get(i + 1)
        if spec is None or spec == SAME:
            print('  ! scene', i + 1, 'has no plan'); spec = CARD(tone='dark')
        j = i + 1
        while j < n and SC.get(j + 1) == SAME: j += 1
        total = sum(scenes[k]['end'] - scenes[k]['start'] for k in range(i, j)); off = 0.0
        for k in range(i, j):
            d = scenes[k]['end'] - scenes[k]['start']
            s = dict(spec); s['_t0'] = off; s['_tail'] = total - off - d
            ovs = []
            for o in spec.get('ov', []):
                opt = dict(o[2]) if len(o) > 2 else {}
                if 'w' in opt:
                    t = _word_time(scenes[k], opt['w'])
                    if t is None: continue
                    opt['at'] = t
                elif k != i: continue
                ovs.append((o[0], o[1], opt))
            if k > i: s['cut'] = True; s.pop('boom', None)
            s['ov'] = ovs; out[k] = s; off += d
        i = j
    return out
