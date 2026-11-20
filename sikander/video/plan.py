"""Visual plan for the Sikander video, keyed by scene number (the Hindi voice is locked, so the timing is final).

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
    'pella': ('पेला', 40.76, 22.52), 'granicus': ('ग्रेनिकस', 40.2, 27.25), 'issus': ('इसस', 36.85, 36.2), 'tyre': ('टायर', 33.27, 35.2),
    'alexandria': ('एलेक्ज़ेंड्रिया', 31.2, 29.92), 'gaugamela': ('गौगामेला', 36.57, 43.44), 'babylon': ('बेबीलोन', 32.54, 44.42),
    'persepolis': ('पर्सेपोलिस', 29.94, 52.89), 'bactra': ('बैक्ट्रा', 36.76, 66.9), 'samarkand': ('समरकंद', 39.65, 66.96),
    'kabul': ('काबुल', 34.53, 69.17), 'taxila': ('तक्षशिला', 33.75, 72.82), 'hydaspes': ('झेलम', 32.93, 73.73),
    'beas': ('ब्यास', 31.55, 75.3), 'patliputra': ('पाटलिपुत्र', 25.6, 85.14), 'multan': ('मुल्तान', 30.2, 71.47),
    'pattala': ('पाताल', 25.4, 68.4), 'athens': ('एथेंस', 37.98, 23.73), 'susa': ('सूसा', 32.19, 48.25), 'delhi': ('दिल्ली', 28.61, 77.21),
}
# rivers of the Punjab and the Indus (approximate courses)
RIVERS = {
    'jhelum': [(34.08, 74.8), (34.2, 74.3), (34.37, 73.47), (33.6, 73.55), (33.15, 73.64), (32.93, 73.73), (32.55, 73.25), (32.3, 72.35), (31.6, 72.2), (31.15, 72.15)],
    'chenab': [(32.95, 74.9), (32.6, 74.45), (32.3, 74.0), (31.95, 73.4), (31.15, 72.15), (30.4, 71.6), (29.35, 71.0)],
    'ravi': [(32.4, 75.6), (32.0, 75.0), (31.6, 74.3), (31.0, 73.2), (30.6, 72.0), (30.75, 71.75)],
    'beas': [(32.1, 77.15), (31.9, 76.3), (31.8, 75.7), (31.55, 75.3), (31.15, 74.95)],
    'sutlej': [(31.4, 76.9), (31.0, 75.9), (31.15, 74.95), (30.2, 73.6), (29.35, 71.0)],
    'indus': [(35.3, 75.6), (35.6, 73.6), (34.1, 72.6), (33.9, 72.2), (32.9, 71.6), (31.7, 71.0), (30.0, 70.8), (29.35, 71.0), (28.9, 70.5), (27.7, 68.9), (25.4, 68.3), (24.0, 67.5)],
}
# custom regions (lat, lon rings, approximate)
_GREECE = [(42.0, 20.0), (42.2, 23.5), (41.3, 26.0), (40.6, 26.0), (40.0, 23.5), (38.5, 24.0), (37.5, 23.5), (36.4, 22.6), (36.7, 21.6), (38.3, 21.0), (39.5, 20.1), (40.8, 19.5)]
_PERSIA = [(41.0, 26.0), (41.2, 29.0), (41.9, 33.0), (41.6, 36.5), (41.0, 41.5), (42.3, 44.5), (40.8, 49.0), (41.5, 52.8), (38.5, 54.0), (40.8, 57.0), (42.5, 60.0),
           (41.5, 64.0), (40.5, 68.5), (39.5, 71.5), (37.0, 74.0), (34.8, 74.5), (33.0, 72.8), (30.5, 71.2), (27.5, 69.5), (24.5, 67.8), (25.2, 62.0), (25.7, 57.5),
           (27.0, 56.2), (28.8, 51.0), (30.0, 48.5), (31.0, 47.0), (32.0, 44.5), (32.5, 41.0), (31.5, 37.5), (30.2, 35.0), (29.5, 34.8), (27.0, 33.8), (24.0, 33.0),
           (22.0, 31.5), (25.0, 28.0), (29.0, 25.0), (31.0, 25.2), (31.5, 28.5), (31.3, 31.0), (31.2, 32.3), (32.5, 34.8), (34.5, 35.8), (36.2, 35.8), (36.7, 34.0),
           (36.2, 30.0), (36.5, 28.0), (37.5, 27.2), (39.2, 26.2), (40.2, 26.2)]
_PUNJAB = [(34.5, 71.5), (34.8, 74.5), (33.0, 75.5), (32.0, 75.8), (31.2, 75.2), (29.0, 71.5), (24.5, 67.8), (27.5, 69.5), (30.5, 71.2), (33.0, 72.8)]
CUSTOM = {
    'macedon': [[(42.3, 20.6), (42.2, 23.0), (41.3, 24.8), (40.8, 24.5), (40.2, 23.4), (39.9, 22.6), (40.3, 21.2), (41.0, 20.5)]],
    'greece': [_GREECE], 'persia': [_PERSIA], 'alex': [_GREECE, _PERSIA, _PUNJAB],
    'porus': [[(33.2, 73.6), (32.9, 73.75), (32.4, 73.1), (32.2, 72.4), (31.2, 72.15), (31.6, 72.9), (32.1, 73.6), (32.5, 74.4), (32.9, 74.9), (33.2, 74.6)]],
    'taxila': [[(34.3, 72.3), (34.4, 73.4), (33.2, 73.6), (32.9, 73.75), (32.4, 73.1), (32.9, 71.6), (33.9, 72.2)]],
    'nanda': [[(30.5, 77.5), (29.5, 80.5), (28.0, 84.0), (27.3, 88.0), (25.5, 89.5), (22.0, 88.8), (21.5, 87.0), (23.5, 84.5), (24.0, 80.5), (25.5, 77.0), (28.5, 76.8)]],
    'maurya': [[(36.5, 70.5), (35.5, 74.5), (33.0, 75.8), (31.0, 77.5), (29.8, 80.5), (27.5, 88.2), (25.8, 89.8), (22.0, 89.0), (20.0, 86.5), (17.5, 83.0), (15.5, 80.2),
                (14.5, 78.0), (15.5, 74.0), (18.5, 72.8), (21.5, 72.5), (23.0, 68.5), (25.2, 62.0), (29.5, 61.0), (31.5, 62.0), (34.5, 62.5), (35.5, 66.5)]],
    'seleucid': [[(41.0, 26.0), (41.5, 36.5), (41.0, 41.5), (42.3, 44.5), (40.8, 49.0), (41.5, 52.8), (40.8, 57.0), (42.5, 60.0), (41.5, 64.0), (39.5, 69.0),
                  (36.5, 70.5), (35.5, 66.5), (34.5, 62.5), (31.5, 62.0), (29.5, 61.0), (25.2, 62.0), (25.7, 57.5), (27.0, 56.2), (28.8, 51.0), (30.0, 48.5),
                  (31.0, 47.0), (32.0, 44.5), (32.5, 41.0), (33.5, 36.5), (36.2, 35.8), (36.7, 34.0), (36.2, 30.0), (37.5, 27.2), (40.2, 26.2)]],
}
# the Hydaspes battle board (texture pixels, 4000 x 2600, north at the top): river, island at the crossing
BATTLE_RIVER = [(2750, -150), (2620, 300), (2480, 700), (2330, 1100), (2200, 1500), (2080, 1900), (1930, 2300), (1820, 2750)]
BATTLE_ISLANDS = [(2420, 560, 2620, 700)]

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
    1: MAP(view=(33.8, 72.4, 16.0), view1=(33.0, 73.4, 9.0), pitch=52, rivers=RIV_ALL + [('jhelum', 0.8, 2.6, (120, 210, 255), 9)],
           labels=[('झेलम नदी', 32.45, 73.05, 3.2, 60)], ov=storm(5.2, 7.6) + [date('मई, 326 ईसा पूर्व', 0.4)]),
    2: P('issus_mosaic', grade='paint', frame=False, z0=2.3, z1=2.6, fx0=0.24, fy0=0.36, fx1=0.22,
         ov=storm(0.15) + [cap('सिकंदर (इसस का मोज़ेक, पोम्पेई)', 1.2), bigw('29 साल', 'का राजा', w='उनतीस', y=0.78, dim=False)]),
    3: MAP(ground='battle', view=(2400, 700, 1900), view1=(2550, 650, 1600), pitch=56, yaw0=-8, yaw1=4,
           units=[dict(side='greek', kind='boat', xy0=(2180, 560), xy1=(2860, 700), at=0.0, mv=0.6, dur=4.6, w=420, h=110, n=4, size=30, label='सिकंदर की सेना')],
           blabels=[('झेलम', 2330, 1050, 0.5, 54)], ov=storm(3.6) + [capw('आधी रात, चुपचाप नदी पार', 3, 'चुपचाप')]),
    4: MAP(view=(36.0, 40.0, 60.0), view1=(33.0, 56.0, 80.0), pitch=44, yaw0=-4, yaw1=4,
           fill=[('alex', 'gold', 1.0)],
           routes=[dict(pts=[ll('pella'), ll('granicus'), ll('issus'), ll('tyre'), ll('alexandria'), ll('gaugamela'), ll('babylon'), ll('persepolis'), ll('bactra'), ll('taxila')],
                        at=0.2, dur=10.0, icon=None, col='red', arc=0.0)],
           labels=[('यूनान', 39.6, 22.0, wt(4, 'यूनान'), 54), ('मिस्र', 27.0, 30.0, wt(4, 'मिस्र'), 54), ('ईरान', 32.0, 54.0, wt(4, 'ईरान'), 54),
                   ('अफ़ग़ानिस्तान', 34.2, 66.0, wt(4, 'अफ़ग़ानिस्तान'), 50)], ov=[date('334 – 326 ईसा पूर्व', 0.3)]),
    5: SAME,
    6: P('lebrun_porus', grade='paint', z0=1.05, z1=1.2, fx0=0.35, fy0=0.5, fx1=0.6, ov=[capw('राजा पोरस (चित्र: शार्ल ले ब्रुन, 1673)', 6, 'पोरस')]),
    7: P('castaigne_phalanx', grade='paint', frame=False, z0=1.0, z1=1.15, fx0=0.5, fy0=0.35, fy1=0.55,
         ov=[bigw('सैकड़ों जंगी हाथी', '', w='सैकड़ों', y=0.82, dim=False), cap('झेलम की लड़ाई (चित्र: आंद्रे कास्तेन, 1899)', 0.5)]),
    8: MAP(ground='battle', view=(2300, 1250, 3400), view1=(2400, 1250, 2800), pitch=50, yaw0=6, yaw1=-6,
           units=[dict(side='indian', kind='eleph', xy0=(2900, PORUS_LINE_Y - 120), w=1100, h=90, n=8, at=0.6, label='पोरस'),
                  dict(side='indian', kind='inf', xy0=(3020, PORUS_LINE_Y + 30), w=1150, h=120, at=0.9),
                  dict(side='indian', kind='chariot', xy0=(3000, PORUS_LINE_Y - 420), w=360, h=90, n=3, at=1.2),
                  dict(side='indian', kind='chariot', xy0=(3000, PORUS_LINE_Y + 330), w=360, h=90, n=3, at=1.2),
                  dict(side='greek', kind='inf', xy0=(1550, 1350), w=700, h=120, at=0.3, label='सिकंदर'),
                  dict(side='greek', kind='cav', xy0=(1500, 1050), w=380, h=110, at=0.5)],
           blabels=[('झेलम नदी', 2130, 1700, 0.2, 56)]),
    9: P('hydaspes1904', grade='bw', frame=False, z0=1.0, z1=1.16, fx0=0.5, fy0=0.4, fy1=0.5, ov=[cap('झेलम की लड़ाई, 326 ईसा पूर्व (1904 का चित्र)', 0.5)]),
    10: CARD(bgimg='lebrun_detail', grade='paint', ov=[bigw('सेना ने इनकार कर दिया', 'आगे बढ़ने से', w='इनकार', y=0.42)]),
}


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
