"""Visual plan for the Ottoman video, in the Ziro History style (see the reference clips): satellite map with an
orange-red empire, grey studio with the guide and cards, flat cartoon scenes, portraits on cards, letter-spaced
handwritten labels, red/yellow numbers and "THE CRAZY PART" style punch words.

Entries are keyed by a phrase from the narration: the entry applies to the scene in which that phrase begins.
Several entries landing in one scene are merged; a scene with no entry continues the previous one."""
import json, os, re

PLACES = {
    'Sogut': (40.02, 30.18), 'Bursa': (40.19, 29.06), 'Istanbul': (41.01, 28.98), 'Gallipoli': (40.41, 26.67), 'Edirne': (41.68, 26.56),
    'Kosovo': (42.66, 21.16), 'Vienna': (48.21, 16.37), 'Gulf': (29.4, 49.5), 'Algiers': (36.75, 3.06), 'Caspian': (41.5, 50.5),
    'Konya': (37.87, 32.48), 'Ankara': (39.93, 32.86), 'Cairo': (30.04, 31.24), 'Baghdad': (33.31, 44.36), 'Mecca': (21.42, 39.83),
    'Belgrade': (44.79, 20.45), 'Rome': (41.9, 12.5), 'London': (51.5, -0.12), 'Karakorum': (47.2, 102.8), 'Nicopolis': (43.7, 24.9),
    'Varna': (43.21, 27.91), 'Samarkand': (39.65, 66.96),
}
VIEWS = {   # (lat, lon, width in degrees of longitude)
    'europe': (44.0, 20.0, 52), 'anatolia': (39.6, 31.5, 16), 'sogut': (40.05, 30.0, 5.5), 'empire': (37.0, 27.0, 76),
    'west_anatolia': (39.8, 29.5, 10), 'near_east': (37.0, 33.0, 40), 'world': (35.0, 25.0, 85),
}
GROUPS = {
    'PEAK': ['Turkey', 'Greece', 'Bulgaria', 'Romania', 'Republic of Serbia', 'Bosnia and Herzegovina', 'Montenegro', 'Albania',
             'North Macedonia', 'Kosovo', 'Hungary', 'Moldova', 'Cyprus', 'Syria', 'Lebanon', 'Israel', 'Palestine', 'Jordan', 'Iraq',
             'Egypt', 'Libya', 'Tunisia', 'Algeria', 'Georgia', 'Armenia', 'Croatia'],
    'BYZ_1280': ['Greece'],
}
def _blob(cx, cy, rx, ry, n=28, seed=1):
    import math, random
    rnd = random.Random(seed)
    return [[(cx + rx * math.cos(2 * math.pi * i / n) * (1 + rnd.uniform(-0.12, 0.12)),
              cy + ry * math.sin(2 * math.pi * i / n) * (1 + rnd.uniform(-0.12, 0.12))) for i in range(n)]]
CUSTOM = {   # (lon, lat) rings
    'OSMAN': _blob(30.15, 40.05, 0.55, 0.38, seed=3),
    'BEY1': _blob(27.6, 39.6, 0.9, 0.6, seed=4), 'BEY2': _blob(28.6, 37.9, 0.9, 0.6, seed=5), 'BEY3': _blob(30.6, 37.6, 1.0, 0.6, seed=6),
    'BEY4': _blob(32.6, 38.9, 1.2, 0.8, seed=7), 'BEY5': _blob(34.7, 40.6, 1.2, 0.6, seed=8), 'BEY6': _blob(36.6, 38.4, 1.1, 0.7, seed=9),
    'BEY7': _blob(33.0, 41.5, 0.9, 0.4, seed=10), 'BEY8': _blob(29.2, 38.7, 0.6, 0.45, seed=11),
    'BYZ_COAST': _blob(28.6, 40.9, 1.2, 0.5, seed=12),
}

# ------------------------------------------------------------------ item helpers (same as the Istanbul plan)
def _d(k, at, id, **kw):
    d = dict(k=k, **kw)
    if at is not None: d['at'] = at
    if id: d['id'] = id
    return d
def label(text, place, at=None, id=None, s=40, **kw): return _d('label', at, id, text=text, at_place=place, s=s, **kw)
def pin(place, at=None, label=None, id=None, **kw): return _d('pin', at, id, at_place=place, label=label, **kw)
def badge(icon, place, at=None, label=None, id=None, s=70, **kw): return _d('badge', at, id, icon=icon, at_place=place, label=label, s=s, **kw)
def ring(place, at=None, id=None, **kw): return _d('ring', at, id, at_place=place, **kw)
def arrow(path, at=None, to=None, color='red', id=None, w=22, **kw):
    d = _d('arrow', at, id, path=path, color=color, w=w, **kw)
    if to is not None: d['to'] = to
    return d
def move(icon, path, at=None, to=None, id=None, s=70, **kw):
    d = _d('move', at, id, icon=icon, path=path, s=s, **kw)
    if to is not None: d['to'] = to
    return d
def prop(kind, x, y, at=None, id=None, h=200, **kw): return _d('prop', at, id, kind=kind, xy=(x, y), h=h, **kw)
def photo(name, title, at, x=0.6, y=0.47, h=560, off=None):
    d = dict(k='photo', name=name, title=title, xy=(x, y), at=at, h=h)
    if off is not None: d['off'] = off
    return d
def clock(at=0.0, id='clk', speed=-2.5, x=0.5, y=0.45, s=160): return dict(k='clock', xy=(x, y), at=at, id=id, speed=speed, s=s)
def S(x, y): return ('s', x, y)
DUSK = dict(bg='scene', sky='dusk', clouds=0)

def camp(at=0.0):
    return [prop('yurt', 0.60, 0.84, at, 'y1', h=300), prop('yurt', 0.77, 0.82, (at, 0.2) if isinstance(at, str) else at, 'y2', h=240),
            *[prop('sheep', 0.22 + i * 0.075, 0.94 + (i % 2) * 0.03, at, f'sh{i}', h=105) for i in range(4)]]

# ------------------------------------------------------------------ phrase-keyed plan (preview: the hook and Part 1)
BY_PHRASE = [
    ('Around the year 1280', dict(**DUSK, items=[*camp(0.0), prop('fig-colonist', 0.42, 0.95, 0.45, 'osman', h=430, say='Osman', ss=44)],
                                  cap=[('around 1280', None, '1280')])),
    ('He did not have a city', dict(**DUSK, items=[*camp(), prop('fig-colonist', 0.42, 0.95, None, 'osman', h=430),
                                   label('no city', S(0.2, 0.36), 'city', 'nc', s=40), label('no palace', S(0.2, 0.46), 'palace', 'np', s=40)])),
    ('He had a small village called', dict(**DUSK, items=[*camp(), prop('fig-colonist', 0.42, 0.95, None, 'osman', h=430),
                                   label('SÖGÜT', S(0.7, 0.42), 'village', 'sgl', s=44, spaced=True),
                                   prop('horseman', 0.12, 0.99, 'horsemen', 'hm1', h=300)],
                                   cap=[('a few hundred horsemen and a lot of sheep', None, 'few')])),
    ('Honestly, if you had told', dict(bg='scene', items=[*camp(0.0), prop('fig-villager', 0.25, 0.95, 0.05, 'n1', h=400, say='Ha!', ss=56),
                                   prop('fig-merchant', 0.4, 0.95, 0.2, 'n2', h=400, say='HAHA!', ss=56)])),
    ('But that is exactly what happened.', dict(view='anatolia', fill=[('OSMAN', 'red', 0.1)], items=[pin('Sogut', 0.1, 'SÖGÜT', 'sg', spaced=True)])),
    ('six hundred and twenty-three years', dict(bg='studio', items=[prop('fig-sultan', 0.47 + i * 0.1, 0.88, 0.3 + 0.12 * i, f'su{i}', h=420) for i in range(5)],
                                   cap=[('one family ruled for', '623 years', 'six', {'x': 0.64, 'count': 1.2})])),
    ('Thirty-six sultans', dict(bg='studio', items=[prop('fig-sultan', 0.47 + i * 0.1, 0.88, None, f'su{i}', h=420) for i in range(5)],
                                   cap=[(None, '36 sultans', 'Thirty-six', {'x': 0.64}), ('one single family', None, 'family', {'x': 0.64})])),
    ('At its peak, their empire', dict(view='empire', fill=[('PEAK', 'red', 'peak')], items=[label('THREE CONTINENTS', (47.5, 32.0), 'three', 'tc', s=42, spaced=True)])),
    ('From the gates of Vienna', dict(view='empire', fill=[('PEAK', 'red')], items=[pin('Vienna', 'Vienna', 'VIENNA', 'v', spaced=True),
                                   pin('Gulf', 'Persian', 'PERSIAN GULF', 'pg', spaced=True)])),
    ('From the deserts of Algeria', dict(view='empire', fill=[('PEAK', 'red')], items=[pin('Vienna', None, 'VIENNA', 'v', spaced=True),
                                   pin('Gulf', None, 'PERSIAN GULF', 'pg', spaced=True), pin('Algiers', 'Algeria', 'ALGERIA', 'al', spaced=True),
                                   pin('Caspian', 'Caspian', 'CASPIAN SEA', 'cs', spaced=True)])),
    ('More than five million', dict(view='empire', fill=[('PEAK', 'red')], cap=[('more than', '5,000,000 km²', 'five', {'count': 1.2, 'color': 'yellow'})])),
    ('Dozens of different peoples', dict(bg='studio', items=[prop('fig-' + f, 0.4 + i * 0.085, 0.88, ('Christians', 0.25 * i), f'p{i}', h=360) for i, f in
                                   enumerate(('priest', 'mehmed', 'merchant', 'colonist', 'arab', 'genoese', 'villager'))],
                                   cap=[('dozens of peoples, one city', None, 'Dozens', {'x': 0.64})])),
    ('And here is the crazy part.', dict(bg='studio', items=[prop('fig-' + f, 0.4 + i * 0.085, 0.88, None, f'p{i}', h=360, off='crazy') for i, f in
                                   enumerate(('priest', 'mehmed', 'merchant', 'colonist', 'arab', 'genoese', 'villager'))], cap=[(None, 'THE CRAZY PART', 'crazy', {'x': 0.64, 'color': 'yellow', 'size': 120})])),
    ('The Roman Empire in the west', dict(bg='studio', items=[badge('cart:fig-emperor', S(0.44, 0.52), 0.05, 'Romans', 'cr0', s=80)])),
    ('The Mongol Empire split apart', dict(bg='studio', items=[badge('cart:fig-emperor', S(0.44, 0.52), None, 'Romans', 'cr0', s=80),
                                   badge('horseman', S(0.57, 0.52), 'Mongol', 'Mongols', 'cr1', s=80)])),
    ('The British Empire rose', dict(bg='studio', items=[badge('cart:fig-emperor', S(0.44, 0.52), None, 'Romans', 'cr0', s=80, off='outlasted'),
                                   badge('horseman', S(0.57, 0.52), None, 'Mongols', 'cr1', s=80, off='outlasted'),
                                   badge('cart:fig-king', S(0.70, 0.52), 'British', 'British', 'cr2', s=80, off='outlasted')])),
    ('The Ottomans outlasted almost all of them.', dict(bg='studio', items=[badge(ic, S(0.44 + i * 0.13, 0.52), 'outlasted', lbl, f'cx{i}', s=80, x=True)
                                   for i, (ic, lbl) in enumerate((('cart:fig-emperor', 'Romans'), ('horseman', 'Mongols'), ('cart:fig-king', 'British')))]
                                   + [badge('cart:fig-sultan', S(0.84, 0.52), ('outlasted', 0.4), 'Ottomans', 'ot', s=95)])),
    ('So how did a tribe', dict(bg='studio', items=[badge('horseman', S(0.5, 0.5), 'tribe', 'a few hundred horsemen', 'q0', s=100),
                                   badge('question', S(0.66, 0.5), 'become', None, 'qm', s=70), badge('crown', S(0.82, 0.5), 'superpower', 'a superpower', 'q1', s=100)])),
    ('that ruled the world end up', dict(bg='studio', items=[prop('fig-sultan', 0.66, 0.82, 'cage', 'cgp', h=300), prop('cage', 0.66, 0.86, 'cage', 'cg', h=470)],
                                   cap=[('princes in a cage?', None, 'cage', {'x': 0.64})])),
    ('And how did it all disappear', dict(view='empire', fill=[('PEAK', 'red', None)], unfill=[('PEAK', 'disappear')],
                                   items=[prop('stamp', 0.5, 0.62, 'disappear', 'gone', h=170)], cap=[('in just', '4 years', 'four', {'color': 'yellow'})])),
    ('The Ottomans had one superpower', dict(bg='studio', items=[badge('cart:fig-villager', S(0.5, 0.5), 'outsiders', 'outsiders', 'o1', s=125),
                                   badge('cart:fig-janissary', S(0.8, 0.5), 'insiders', 'insiders', 'o2', s=125)],
                                   cap=[('the Ottoman superpower', None, 'superpower', {'x': 0.64})])),
    ('Enemies became soldiers', dict(bg='studio', items=[badge('cart:fig-villager', S(0.5, 0.5), None, 'outsiders', 'o1', s=125),
                                   badge('cart:fig-janissary', S(0.8, 0.5), None, 'insiders', 'o2', s=125)],
                                   cap=[('enemies became soldiers', None, 'Enemies', {'x': 0.64}), ('slaves became generals', None, 'slaves', {'x': 0.64})])),
    ("Let's go back to the very beginning.", dict(bg='clock', guide=False, items=[clock(0.0, s=170)], cap=[(None, '1200s', 'beginning', {'color': 'white', 'y': 0.84})])),
    # ---- Part 1
    ('In the late 1200s, the land', dict(cap=[('the land we now call Turkey', None, 'Turkey', {'color': 'white'})])),
    ('The old Byzantine Empire still held', dict(view='anatolia', fill=[('BYZ_COAST', 'purple', 'Byzantine'), ('Greece', 'purple', 'Byzantine')],
                                   items=[pin('Istanbul', 'Constantinople', 'CONSTANTINOPLE', 'cp', spaced=True)],
                                   cap=[('tired, broke and shrinking', None, 'tired')])),
    ('The Seljuk Turks', dict(view='anatolia', fill=[('BYZ_COAST', 'purple'), ('Greece', 'purple')],
                                   items=[pin('Konya', 'Seljuk', 'SELJUKS', 'sj', spaced=True), arrow([(41.5, 41.5), (40.0, 37.0), (38.3, 33.2)], 'Mongols', ('Mongols', 1.0), id='mga', w=26),
                                   badge('horseman', (41.3, 41.0), 'Mongols', 'the Mongols', 'mg', s=66)])),
    ('What was left was a patchwork', dict(view='anatolia', fill=[('BYZ_COAST', 'purple')] + [(f'BEY{i}', c, ('beyliks', 0.15 * i)) for i, c in
                                   enumerate(('orange', 'yellow', 'teal', 'lime', 'pink', 'sky', 'brown', 'green'), 1)],
                                   items=[label('BEYLIKS', (41.8, 30.8), 'beyliks', 'bl', s=48, spaced=True)])),
    ('Dozens of them.', dict(view='anatolia', fill=[('BYZ_COAST', 'purple')] + [(f'BEY{i}', c) for i, c in
                                   enumerate(('orange', 'yellow', 'teal', 'lime', 'pink', 'sky', 'brown', 'green'), 1)],
                                   items=[badge('horseman', (38.3, 27.8), 'horsemen', None, 'b1', s=56), badge('crown', (38.7, 36.2), 'ambitions', None, 'b2', s=56)])),
    ("Osman's beylik was one of the smallest.", dict(view='west_anatolia', fill=[('BYZ_COAST', 'purple'), ('OSMAN', 'red', 'Osman')],
                                   items=[pin('Sogut', 'Osman', 'OSMAN', 'os', spaced=True), label('BYZANTINES', (41.1, 28.0), 'border', 'bz', s=40, spaced=True)],
                                   cap=[('right on the border', None, 'border')])),
    ('That sounds like a terrible place', dict(**DUSK, items=[prop('hut', 0.3, 0.86, 0.0, 'fh', h=200), *[dict(k='fire', at_place=S(x, 0.78), at=('Raids', 0.3 * i), id=f'ff{i}', size=1.1, n=4) for i, x in enumerate((0.3, 0.55))],
                                   prop('horseman', 0.7, 0.97, 'ambushes', 'rd', h=220)], cap=[('raids, ambushes, burned farms', None, 'Raids')])),
    ('But it turned out to be the best', dict(view='west_anatolia', fill=[('BYZ_COAST', 'purple'), ('OSMAN', 'red')],
                                   items=[pin('Sogut', None, 'OSMAN', 'os', spaced=True)], cap=[('the best real estate in the world', None, 'best')])),
    ('Because on the frontier', dict(view='west_anatolia', fill=[('BYZ_COAST', 'purple'), ('OSMAN', 'red')],
                                   items=[pin('Sogut', None, 'OSMAN', 'os', spaced=True), badge('gold', (40.9, 31.2), 'loot', 'loot', 'lt', s=60),
                                   badge('crown', (39.2, 31.4), 'fame', 'fame', 'fm', s=60),
                                   *[move('horseman', [p, 'Sogut'], 'Warriors', ('Warriors', 2.0), s=50, id=f'w{i}') for i, p in enumerate(((38.6, 28.2), (39.0, 32.0), (41.2, 31.8)))]])),
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
    # an item/caption/fill whose cue word is spoken in a later scene moves to that scene
    text = {r['scene']: norm(r['text']).lower() for r in rows}
    def says(n, word):
        w = word.lower().strip('.,;:!?"\'')
        return any(t.strip('.,;:!?"\'\u2019').startswith(w) for t in text.get(n, '').split())
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
                        dest = None      # never move a visual onto a different background
                    if dest:
                        d = SCENES.setdefault(dest, {'_partial': True})
                        d.setdefault(key, []).append(x)
                        if key == 'items': keep.append(dict({k: v for k, v in x.items() if k not in ('at', 'to', 'off')}, _hide=True))
                        continue
                keep.append(x)
            spec[key] = keep
        spec['items'] = [x for x in spec.get('items', []) if not x.get('_hide')]
    # scenes with no entry continue the previous one (without re-popping its items, captions or fills)
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

import plan2   # adds the phrase entries for paragraphs 13-208
resolve(os.path.join(os.environ.get('OUT_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build')), 'timing.json'))
