"""Visual plan for the Israel video, in the Ottoman video's style: relief map with glowing highlighted regions (a sharp NASA
close-up for Israel and its neighbours), grey studio with the guide and cards, flat cartoon scenes, photos on cards,
letter-spaced labels and big yellow numbers.

Entries are keyed by a phrase from the narration: the entry applies to the scene in which that phrase begins.
Several entries landing in one scene are merged; a scene with no entry continues the previous one."""
import json, os, re

PLACES = {
    'Jerusalem': (31.78, 35.23), 'TelAviv': (32.08, 34.78), 'Jaffa': (32.05, 34.75), 'Haifa': (32.79, 34.99), 'Gaza': (31.50, 34.46),
    'Hebron': (31.53, 35.10), 'Bethlehem': (31.70, 35.20), 'Nazareth': (32.70, 35.30), 'Beersheba': (31.25, 34.79), 'Eilat': (29.56, 34.95),
    'Netanya': (32.33, 34.86), 'Tulkarm': (32.31, 35.03), 'Ramallah': (31.90, 35.20), 'Amman': (31.95, 35.93), 'Beirut': (33.89, 35.50),
    'Damascus': (33.51, 36.29), 'Cairo': (30.04, 31.24), 'Suez': (29.97, 32.55), 'Tiran': (27.95, 34.45), 'Golan': (33.00, 35.78),
    'DeirYassin': (31.79, 35.18), 'Babylon': (32.54, 44.42), 'Nineveh': (36.36, 43.15), 'Ur': (30.96, 46.10), 'Harran': (36.87, 39.03),
    'Rome': (41.90, 12.50), 'Athens': (37.98, 23.73), 'Persepolis': (29.93, 52.89), 'Mecca': (21.42, 39.83), 'Istanbul': (41.01, 28.98),
    'Basel': (47.56, 7.59), 'Vienna': (48.21, 16.37), 'Paris': (48.86, 2.35), 'Odessa': (46.48, 30.72), 'Kyiv': (50.45, 30.52),
    'Toledo': (39.86, -4.03), 'Thessaloniki': (40.64, 22.94), 'Baghdad': (33.31, 44.36), 'Tunis': (36.80, 10.18), 'London': (51.50, -0.12),
    'Berlin': (52.52, 13.40), 'Warsaw': (52.23, 21.01), 'Mesopotamia': (32.5, 44.0), 'Canaan': (31.6, 35.0), 'Masada': (31.31, 35.35),
    'Sinai': (29.6, 33.8), 'WestBank': (31.95, 35.25), 'Rafah': (31.29, 34.25), 'Sanaa': (15.37, 44.19), 'Rabat': (34.02, -6.84),
    'MedSea': (33.4, 33.2), 'Jordan_R': (32.3, 35.57), 'DeadSea': (31.50, 35.48), 'Galilee': (32.82, 35.59), 'Tehran': (35.69, 51.39),
}
VIEWS = {   # (lat, lon, width in degrees of longitude)
    'med_east': (33.0, 31.5, 22), 'levant': (31.6, 35.3, 7.5), 'israel': (31.6, 35.0, 4.6), 'israel_n': (32.4, 35.1, 3.2),
    'narrow': (32.3, 35.0, 2.6), 'whole': (31.35, 35.1, 7.6), 'world_wide': (38.0, 25.0, 80), 'mideast': (31.0, 37.0, 34), 'fertile': (33.0, 40.0, 26),
    'med': (38.0, 20.0, 50), 'europe': (47.0, 15.0, 46), 'sinai': (30.4, 33.8, 9.5), 'region': (31.3, 35.6, 12),
    'jerusalem': (31.78, 35.22, 2.4), 'gaza': (31.42, 34.45, 2.4), 'westbank': (31.95, 35.2, 2.8),
}
GROUPS = {
    'ROME': ['Italy', 'France', 'Spain', 'Portugal', 'Greece', 'Turkey', 'Egypt', 'Tunisia', 'Libya', 'Syria', 'Lebanon', 'ISRAEL', 'PALESTINE',
             'Jordan', 'Algeria', 'Morocco', 'Albania', 'Croatia', 'Slovenia', 'Bosnia and Herzegovina', 'Republic of Serbia', 'Montenegro',
             'North Macedonia', 'Bulgaria', 'Cyprus', 'Belgium', 'Switzerland', 'Austria', 'Kosovo', 'Romania'],
    'PERSIA': ['Iran', 'Iraq', 'Turkey', 'Syria', 'Lebanon', 'ISRAEL', 'PALESTINE', 'Jordan', 'Egypt', 'Armenia', 'Azerbaijan', 'Kuwait'],
    'BABYLON': ['Iraq', 'Syria', 'Lebanon', 'ISRAEL', 'PALESTINE', 'Jordan', 'Kuwait'],
    'ASSYRIA': ['Iraq', 'Syria', 'Lebanon', 'K_ISRAEL'],
    'CALIPHATE': ['Saudi Arabia', 'Yemen', 'Oman', 'United Arab Emirates', 'Iraq', 'Syria', 'Lebanon', 'ISRAEL', 'PALESTINE', 'Jordan', 'Egypt',
                  'Libya', 'Tunisia', 'Algeria', 'Morocco', 'Iran', 'Kuwait', 'Qatar'],
    'OTTOMAN': ['Turkey', 'Syria', 'Lebanon', 'ISRAEL', 'PALESTINE', 'Jordan', 'Iraq', 'Egypt', 'Greece', 'Bulgaria', 'North Macedonia', 'Albania',
                'Kosovo', 'Republic of Serbia', 'Bosnia and Herzegovina', 'Montenegro', 'Libya', 'Tunisia', 'Cyprus'],
    'BRITISH': ['MANDATE', 'JORDAN', 'Iraq', 'Egypt'], 'FRENCH': ['Syria', 'Lebanon'],
    'ARAB5': ['EGYPT', 'JORDAN', 'SYRIA', 'Iraq', 'LEBANON'],
    'ISRAEL67': ['GREEN_LINE', 'WEST_BANK', 'GAZA', 'GOLAN', 'SINAI'],
}
CUSTOM = {}

# ------------------------------------------------------------------ item helpers (same as the Ottoman plan)
def _d(k, at, id, **kw):
    d = dict(k=k, **kw)
    if at is not None: d['at'] = at
    if id: d['id'] = id
    return d
def label(text, place, at=None, id=None, s=40, **kw): return _d('label', at, id, text=text, at_place=place, s=s, **kw)
def pin(place, at=None, label=None, id=None, **kw): return _d('pin', at, id, at_place=place, label=label, **kw)
def badge(icon, place, at=None, label=None, id=None, s=70, **kw): return _d('badge', at, id, icon=icon, at_place=place, label=label, s=s, **kw)
def icon(kind, place, at=None, id=None, s=70, **kw): return _d('icon', at, id, icon=kind, at_place=place, s=s, **kw)
def ring(place, at=None, id=None, **kw): return _d('ring', at, id, at_place=place, **kw)
def arrow(path, at=None, to=None, color='red', id=None, w=22, **kw):
    d = _d('arrow', at, id, path=path, color=color, w=w, **kw)
    if to is not None: d['to'] = to
    return d
def line(path, at=None, to=None, id=None, color=(255, 230, 90), w=8, **kw):
    d = _d('line', at, id, path=path, color=color, w=w, glow=True, **kw)
    if to is not None: d['to'] = to
    return d
def move(icon, path, at=None, to=None, id=None, s=70, **kw):
    d = _d('move', at, id, icon=icon, path=path, s=s, **kw)
    if to is not None: d['to'] = to
    return d
def prop(kind, x, y, at=None, id=None, h=200, **kw): return _d('prop', at, id, kind=kind, xy=(x, y), h=h, **kw)
def photo(name, title, at, x=0.6, y=0.47, h=560, off=None, id=None):
    d = dict(k='photo', name=name, title=title, xy=(x, y), at=at, h=h)
    if off is not None: d['off'] = off
    if id: d['id'] = id
    return d
def clock(at=0.0, id='clk', speed=-2.5, x=0.5, y=0.45, s=160): return dict(k='clock', xy=(x, y), at=at, id=id, speed=speed, s=s)
def S(x, y): return ('s', x, y)
def MAP(view, fill=(), items=(), cap=(), **kw): return dict(view=view, fill=list(fill), items=list(items), cap=list(cap), **kw)
def ST(items=(), cap=(), **kw): return dict(bg='studio', items=list(items), cap=list(cap), **kw)
def SC(items=(), cap=(), sky='day', ground='sand', **kw):
    kw.pop('bg', None)
    return dict(bg='scene', sky=kw.pop('sky', sky), ground=ground, items=list(items), cap=list(cap), **kw)
def CAP(text, at, **o): return (text, None, at, o) if o else (text, None, at)
def BIG(small, big, at, **o): return (small, big, at, dict({'x': 0.64}, **o))
def fig(kind, x, at=None, id=None, h=380, y=0.88, **kw): return prop('fig-' + kind, x, y, at, id, h=h, **kw)
def badges(specs, y=0.5, x0=0.46, dx=0.15, s=100, pre='bg'):
    return [badge(ic, S(x0 + i * dx, y), at, lbl, f'{pre}_{lbl[:6]}_{i}', s=s) for i, (ic, at, lbl) in enumerate(specs)]
def CLK(big, at=0.0, small=None): return dict(bg='clock', guide=False, items=[clock(0.0, s=170)], cap=[(small, big, at, {'color': 'white', 'y': 0.84})])
NIGHT = dict(sky='night', clouds=0)
DUSK = dict(sky='dusk', clouds=0)

EMPIRES = [('egyptian', 'Egyptians'), ('assyrian', 'Assyrians'), ('babylonian', 'Babylonians'), ('persian', 'Persians'), ('greek', 'Greeks'),
           ('roman', 'Romans'), ('arab', 'Arabs'), ('crusader', 'Crusaders'), ('mamluk', 'Mamluks'), ('janissary', 'Ottomans'), ('tommy', 'British')]
def empire_row(n0, n1, y, at=True, off=None, s=62):
    out = []
    for i, (f, name) in enumerate(EMPIRES[n0:n1]):
        x = 0.42 + (i + (0.5 if n0 else 0)) * 0.083
        b = badge('cart:fig-' + f, S(x, y), name if at else None, name, f'emp{n0 + i}', s=s, ls=26)
        if off: b['off'] = off
        out.append(b)
    return out
def two_peoples(at0=0.0, at1=0.3):
    return [prop('house', 0.16, 0.86, 0.0, 'h1', h=150), prop('olive', 0.5, 0.86, 0.0, 'olive', h=330),
            prop('house', 0.86, 0.86, 0.0, 'h2', h=150, kw={'col': (226, 214, 190, 255)}),
            fig('pioneer', 0.33, at0, 'jp', h=380), fig('farmer', 0.68, at1, 'pf', h=380)]

# ------------------------------------------------------------------ phrase-keyed plan: hook and the start of Part 1 (preview)
BY_PHRASE = [
    ('On the eastern shore of the Mediterranean', MAP('med_east', [], [label('MEDITERRANEAN SEA', 'MedSea', 'Mediterranean', 'msea', s=44, spaced=True)],
        moves=[('strip', 'levant')])),
    ('across its narrowest part', MAP('narrow', [('GREEN_LINE', 'blue', 0.0)], [line(['Netanya', 'Tulkarm'], 'narrowest', ('narrowest', 1.6), 'nl', w=9),
        move('truck', [(32.36, 34.86), (32.34, 35.03)], 'narrowest', ('twenty', 1.5), 'car', s=46)], [BIG(None, '~15 km', 'twenty', x=0.5, color='yellow')])),
    ('Israel today is roughly the size', MAP('whole', [('ISRAEL', 'blue', 0.0)], [label('ISRAEL', (30.7, 34.85), 0.1, 'isl', s=44, spaced=True),
        badge('flag-il', (30.2, 36.4), 'New', 'about the size of New Jersey', 'nj', s=64)], [BIG(None, '22,000 km²', 'size', x=0.5, color='yellow')])),
    ('About ten million people', MAP('world_wide', [('ISRAEL', 'red', 0.0)], [ring('Jerusalem', 'thumb', 'rgw', size=1.6), badge('people', (25.0, 52.0), 0.05, '10 million people', 'pp', s=70)],
        [CAP('you can cover it with your thumb', 'thumb')])),
    ('And yet, almost no place on Earth', MAP('mideast', [('ISRAEL', 'red'), ('PALESTINE', 'red')],
        [arrow(['Cairo', (30.6, 33.6), 'Jerusalem'], 0.05, 1.5, 'red', 'a1', w=20), arrow(['Babylon', (33.6, 39.5), 'Jerusalem'], 0.2, 1.8, 'red', 'a2', w=20),
         arrow([(37.2, 27.0), (34.6, 31.5), 'Jerusalem'], 0.4, 2.0, 'red', 'a3', w=20), arrow(['Mecca', (27.0, 37.5), 'Jerusalem'], 0.6, 2.2, 'red', 'a4', w=20)],
        [CAP('fought over for 3,000 years', 'fought')])),
    ('by so many empires', MAP('mideast', [('ISRAEL', 'red'), ('PALESTINE', 'red')], [ring('Jerusalem', 0.0, 'rje', size=1.2)], [CAP('so many empires, so many gods', 'empires')])),
    ('Egyptians, Assyrians, Babylonians', ST(empire_row(0, 7, 0.42))),
    ('Crusaders, Mamluks, Ottomans and the British', ST(empire_row(0, 7, 0.42, at=False, off='left') + empire_row(7, 11, 0.72, off='left'),
        [CAP('came, conquered, and left', 'came', x=0.64)])),
    ("Three of the world's great religions", ST(badges([('star', 'Three', 'Judaism'), ('cross', 'religions', 'Christianity'), ('crescent', 'holy', 'Islam')], s=100, pre='rel'),
        [CAP('one holy land', 'holy', x=0.64)])),
    ('Jerusalem, where a Jewish wall', ST([photo('kotel', 'The Western Wall', 'wall', x=0.52, y=0.45, h=330, id='pk'), photo('dome', 'The Dome of the Rock', 'shrine', x=0.82, y=0.5, h=330, id='pd')],
        [CAP('JERUSALEM', 0.0, x=0.64, color='yellow')])),
    ('So how did a people that was scattered', MAP('world_wide', [('ISRAEL', 'blue', 0.0)],
        [arrow(['Jerusalem', (38.0, 20.0), 'Paris'], 'scattered', ('scattered', 1.2), 'blue', 's1', w=16), arrow(['Jerusalem', (43.0, 25.0), 'Warsaw'], ('scattered', 0.2), ('scattered', 1.4), 'blue', 's2', w=16),
         arrow(['Jerusalem', (36.0, 12.0), 'Toledo'], ('scattered', 0.4), ('scattered', 1.6), 'blue', 's3', w=16), arrow(['Jerusalem', 'Baghdad'], ('scattered', 0.3), ('scattered', 1.5), 'blue', 's4', w=16),
         arrow(['Jerusalem', (31.0, 20.0), 'Rabat'], ('scattered', 0.5), ('scattered', 1.7), 'blue', 's5', w=16)],
        [BIG(None, '2,000 years', 'two', color='yellow', x=0.5)])),
    ('Why did the very same moment', ST([badge('flag-il', S(0.52, 0.47), 'independence', 'independence', 'q1', s=105), badge('flag-ps', S(0.8, 0.47), 'catastrophe', 'catastrophe', 'q2', s=105)],
        [CAP('the very same moment', 'same', x=0.64)])),
    ('And why, after more than seventy-five years', ST(badges([('tank', 'wars', 'many wars'), ('dove', 'peace', 'dozens of peace plans'), ('question', 'over', 'still not over')], s=95, pre='q3'),
        [BIG(None, '75+ years', 'seventy', color='yellow')])),
    ('Here is the key', ST([badge('key', S(0.64, 0.5), 'key', None, 'key', s=150)], [CAP('THE KEY', 'key', x=0.64, color='yellow')])),
    ('It is the story of two peoples', SC(two_peoples(), [CAP('two peoples, one small land', 'two')])),
    ('Keep that in mind', SC([dict(x, at=None) if False else x for x in two_peoples(None, None)], [CAP('keep this in mind', 'Keep')])),
    ("Let's go back to the very beginning.", CLK('3,000 years ago', 'three')),
    ('and the Jordan River were home', MAP('levant', [('K_UNITED', 'orange', 'tribes')], [label('JORDAN RIVER', (32.1, 36.3), 'Jordan', 'jr', s=34, spaced=True),
        label('MEDITERRANEAN', (32.3, 33.6), 0.0, 'med2', s=34, spaced=True),
        *[badge('cart:fig-israelite', p, ('Israelites', 0.15 * i), None, f'it{i}', s=48) for i, p in enumerate(((32.6, 35.3), (31.9, 35.15), (31.4, 35.05)))]],
        [CAP('THE ISRAELITES', 'Israelites')])),
    ('According to the Hebrew Bible', MAP('fertile', [], [pin('Ur', 0.05, 'MESOPOTAMIA', 'ur', spaced=True),
        move('cart:fig-israelite', ['Ur', 'Babylon', 'Harran', 'Damascus', 'Canaan'], 'Abraham', ('promised', 0.5), 'abr', s=150),
        line(['Ur', 'Babylon', 'Harran', 'Damascus', 'Canaan'], 'Abraham', ('promised', 0.5), 'abl', color=(255, 220, 120), w=6)],
        [CAP('Abraham', 'Abraham')])),
    ("Historians can't confirm", MAP('fertile', [], [pin('Ur', None, 'MESOPOTAMIA', 'ur', spaced=True), line(['Ur', 'Babylon', 'Harran', 'Damascus', 'Canaan'], None, None, 'abl', color=(255, 220, 120), w=6),
        badge('question', (29.2, 39.5), 'confirm', None, 'hq', s=80)], [CAP("historians can't confirm it", 'Historians')])),
    ('But we do know that by around 1000 BCE', MAP('levant', [('K_ISRAEL', 'red', 'kingdoms'), ('K_JUDAH', 'blue', ('kingdoms', 0.4))],
        [label('ISRAEL', (32.6, 36.4), 'kingdoms', 'kil', s=40, spaced=True), label('JUDAH', (31.5, 36.0), ('kingdoms', 0.4), 'kjl', s=40, spaced=True)],
        [BIG(None, '1000 BCE', 'thousand', color='yellow', x=0.33, y=0.8)])),
    ('Tradition says the greatest king was David', SC([prop('wall', 0.7, 0.86, 0.0, 'jw', h=300, kw={'length': 4}), prop('dome', 0.72, 0.62, 0.0, 'jd', h=170),
        fig('david', 0.32, 0.1, 'dv', h=440, say='King David', ss=44)], [CAP('Jerusalem, his capital', 'Jerusalem')])),
]
SCENES = {}

def resolve(timing_path):
    """map the phrase-keyed plan onto scene numbers, merging entries that land in the same scene"""
    rows = json.load(open(timing_path))['scenes']
    norm = lambda t: re.sub(r'\s+', ' ', t).strip()
    for key, spec in BY_PHRASE:
        hit = next((r['scene'] for r in rows if norm(key) in norm(r['text'])), None)
        if hit is None:  # phrase split across two scenes: find where it starts
            for a, b in zip(rows, rows[1:]):
                if norm(key) in norm(a['text'] + ' ' + b['text']): hit = a['scene']; break
        if hit is None: print('  ! phrase not found:', key); continue
        if hit in SCENES:
            m = SCENES[hit]
            look = lambda d: (d.get('bg', 'map'), d.get('view') if d.get('bg', 'map') == 'map' else None)
            if look(m) != look(spec) and hit + 1 not in SCENES:     # two different backgrounds: start the later one in the next scene
                SCENES[hit + 1] = dict(spec); continue
            for k in ('items', 'cap', 'fill', 'unfill'):
                if k in spec: m[k] = m.get(k, []) + spec[k]
        else:
            SCENES[hit] = dict(spec)
    text = {r['scene']: norm(r['text']).lower() for r in rows}
    def says(n, word):
        w = word.lower().strip('.,;:!?"\'')
        return any(t.strip('.,;:!?"\'’').startswith(w) for t in text.get(n, '').split())
    def cue(x, idx):
        at = x.get('at') if isinstance(x, dict) else (x[idx] if len(x) > idx else None)
        if isinstance(at, tuple): at = at[0]
        return at.split('#')[0] if isinstance(at, str) else None
    for n in sorted(SCENES):
        spec = SCENES[n]
        for key, idx in (('items', None), ('cap', 2), ('fill', 2)):
            keep = []
            for x in spec.get(key, []):
                w = cue(x, idx)
                if w and not says(n, w):
                    dest = next((m for m in range(n + 1, n + 7) if says(m, w)), None)
                    if dest and dest in SCENES and not SCENES[dest].get('_partial') and \
                            (SCENES[dest].get('bg', 'map'), SCENES[dest].get('view')) != (spec.get('bg', 'map'), spec.get('view')):
                        dest = None
                    if dest:
                        d = SCENES.setdefault(dest, {'_partial': True})
                        d.setdefault(key, []).append(x)
                        if key == 'items': keep.append(dict({k: v for k, v in x.items() if k not in ('at', 'to', 'off')}, _hide=True))
                        continue
                keep.append(x)
            spec[key] = keep
        spec['items'] = [x for x in spec.get('items', []) if not x.get('_hide')]
    last = None
    for r in rows:
        n = r['scene']
        if n in SCENES and SCENES[n].get('_partial') and last is not None:
            extra = SCENES[n]
            cont = {k: v for k, v in last.items() if k not in ('cap', 'title', 'unfill', 'moves', 'shake', '_partial')}
            cont['items'] = [dict({kk: vv for kk, vv in it.items() if kk not in ('at', 'to', 'off')}) for it in last.get('items', [])]
            cont['fill'] = [(f[0], f[1]) for f in last.get('fill', [])]
            for k in ('items', 'cap', 'fill'): cont[k] = cont.get(k, []) + extra.get(k, [])
            SCENES[n] = cont; last = cont; continue
        if n in SCENES:
            if last is not None:
                for k in ('bg', 'view', 'sky', 'ground', 'horizon', 'clouds', 'tint'):
                    if k in last and k not in SCENES[n] and not any(kk in SCENES[n] for kk in ('bg', 'view')): SCENES[n][k] = last[k]
            last = SCENES[n]; continue
        if last is not None:
            cont = {k: v for k, v in last.items() if k not in ('cap', 'title', 'unfill', 'moves', 'shake')}
            cont['items'] = [dict({kk: vv for kk, vv in it.items() if kk not in ('at', 'to', 'off')}) for it in last.get('items', [])]
            cont['fill'] = [(f[0], f[1]) for f in last.get('fill', [])]
            SCENES[n] = cont

try:
    import plan2   # the rest of the video (after the preview)
except ImportError:
    pass
resolve(os.path.join(os.environ.get('OUT_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build')), 'timing.json'))
