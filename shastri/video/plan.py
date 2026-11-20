"""Visual plan for the Shastri video, keyed by scene number (the Hindi voice is locked, so the timing is final).

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
    'tashkent': ('ताशकंद', 41.31, 69.24), 'delhi': ('दिल्ली', 28.61, 77.21), 'mughalsarai': ('मुग़लसराय', 25.28, 83.12), 'varanasi': ('वाराणसी', 25.32, 82.99),
    'ariyalur': ('अरियालूर', 11.14, 79.08), 'lahore': ('लाहौर', 31.55, 74.34), 'hajipir': ('हाजी पीर', 33.93, 74.08), 'khemkaran': ('खेमकरण', 31.15, 74.56),
    'srinagar': ('श्रीनगर', 34.08, 74.8), 'moscow': ('मॉस्को', 55.75, 37.62), 'rawalpindi': ('रावलपिंडी', 33.6, 73.05), 'anand': ('आणंद', 22.56, 72.95),
}
RIVERS = {}
CUSTOM = {}
BATTLE_RIVER = [(2750, -150), (2620, 300), (2480, 700), (2330, 1100), (2200, 1500), (2080, 1900), (1930, 2300), (1820, 2750)]

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

def CH(title, num, at=0.2, w=None):
    o = {'sub': f'अध्याय {num}' if num else ''}
    if w: o['w'] = w
    else: o['at'] = at; o['off'] = at + 3.2
    return ('title', title, o)
def capw(t, n, word): return ('caption', t, {'at': wt(n, word)})
def bigw(t, sub='', w=None, **o): o['sub'] = sub; o['w'] = w; return ('big', t, o)
def datew(t, n, word): return ('date', t, {'at': wt(n, word)})
NIGHT = [('tint', '', {'at': 0.0, 'k': 0.42, 'col': (8, 16, 40)}), ('rain', '', {'at': 0.0})]
def storm(*times): return NIGHT + [('lightning', '', {'at': 0.0, 'times': list(times)})]
RIV_ALL = [('indus', 0.0, 0, (70, 150, 220), 5), ('chenab', 0.0, 0, (70, 150, 220), 5), ('ravi', 0.0, 0, (70, 150, 220), 4),
           ('beas', 0.0, 0, (70, 150, 220), 4), ('sutlej', 0.0, 0, (70, 150, 220), 4)]
# battle-board positions (plan pixels, north up; the Jhelum runs top-right to bottom-left; Alexander's camp is on the west bank)
CAMP_W = (1700, 1500); CROSS = (2520, 630); PORUS_LINE_Y = 1250

SC = {
    # ---------------------------------------------------------------- शुरुआत (hook)
    1: MAP(view=(30.0, 74.0, 40.0), view1=(41.0, 69.3, 10.0), pitch=50, yaw0=-6, yaw1=6, fill=[('uzbek', 'gold', 2.0)], pulse=[pin('tashkent', 3.0, 'red')],
           labels=[('ताशकंद, सोवियत संघ', 42.0, 69.24, 3.6, 58)], ov=[('tint', '', {'at': 0.0, 'k': 0.38, 'col': (6, 12, 34)}), date('11 जनवरी 1966', 0.4)]),
    2: CARD(tone='dark', clock=True, hm=(1, 31), sec0=40, ov=[date('रात 1:32', 0.3), capw('ताशकंद के बाहर एक सरकारी बंगला', 2, 'शहर')]),
    3: P('shastri_kbr', frame=False, z0=1.1, z1=1.28, fx0=0.62, fy0=0.06, ov=[cap('प्रधानमंत्री लाल बहादुर शास्त्री (1904 – 1966)', 0.6)]),
    4: CARD(tone='dark', doc=dict(title='ताशकंद समझौता', lines=[('तारीख़: 10 जनवरी 1966', 0.4), ('भारत: लाल बहादुर शास्त्री', 1.4), ('पाकिस्तान: अयूब ख़ान', 2.4),
              ('मध्यस्थ: कोसिगिन (सोवियत संघ)', 3.4)], stamp=('हस्ताक्षर हुए', 5.0, 'green'))),
    5: CARD(tone='dark', files=[('आधिकारिक', 'मौत का कारण', 0.2)], stamps=[(0, 'दिल का दौरा', 'red', wt(5, 'दिल'))]),
    6: CARD(tone='dark', check=[('ताशकंद में पोस्टमार्टम नहीं', wt(6, 'सोवियत')), ('भारत में भी पोस्टमार्टम नहीं', wt(6, 'भारत'))]),
    7: CARD(tone='dark', doc=dict(title='परिवार के मुताबिक़', lines=[('शरीर नीला पड़ गया था', wt(7, 'नीला'))], stamp=('सवाल', wt(7, 'नीला') + 1.4, 'red')), ov=[capw('बाद में: दो अहम गवाह', 7, 'दो अहम')]),
    8: CARD(tone='dark', files=[('गवाह 1', 'डॉ. आर. एन. चुघ', 0.0), ('गवाह 2', 'निजी सेवक राम नाथ', 0.2)],
             stamps=[(0, 'सड़क हादसा', 'red', 1.0), (1, 'गाड़ी से टक्कर', 'red', 1.6)]),
    9: MAP(view=(41.6, 69.0, 7.0), view1=(41.31, 69.24, 5.0), pitch=55, yaw0=-20, yaw1=20, fill=[('uzbek', 'gold', -9)], pulse=[pin('tashkent', 0.0, 'red')],
           ov=[('tint', '', {'at': 0.0, 'k': 0.45, 'col': (6, 12, 34)}), bigw('उस रात क्या हुआ?', '', w='तो उस', y=0.78, dim=False)]),
    10: CARD(tone='red', files=[('PMO', 'शास्त्री फ़ाइल', 0.2)], stamps=[(0, 'गुप्त', 'red', rel(10, 11, 'गुप्त'))]),
    11: SAME,
}
SC[11] = CARD(bgimg='shastri_1965', ov=[('title', 'लाल बहादुर शास्त्री', {'w': 'यह कहानी', 'sub': 'ताशकंद की वो रात'})])
SC[10]['stamps'] = [(0, 'गुप्त', 'red', 2.6)]

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
