"""Visual plan for the Spain video, in the Ottoman video's style: relief map with glowing highlighted regions (a sharp NASA
close-up for Israel and its neighbours), grey studio with the guide and cards, flat cartoon scenes, photos on cards,
letter-spaced labels and big yellow numbers.

Entries are keyed by a phrase from the narration: the entry applies to the scene in which that phrase begins.
Several entries landing in one scene are merged; a scene with no entry continues the previous one."""
import json, os, re

PLACES = {
    'Gibraltar': (36.14, -5.35), 'Ceuta': (35.89, -5.32), 'Tangier': (35.77, -5.80), 'Madrid': (40.42, -3.70), 'Cadiz': (36.53, -6.29),
    'Cartagena': (37.60, -0.98), 'Altamira': (43.38, -4.12), 'Toledo': (39.86, -4.03), 'Cordoba': (37.88, -4.78), 'Seville': (37.39, -5.98),
    'Granada': (37.18, -3.60), 'Barcelona': (41.39, 2.17), 'Valencia': (39.47, -0.38), 'Zaragoza': (41.65, -0.88), 'Lisbon': (38.72, -9.14),
    'Bilbao': (43.26, -2.93), 'Guernica': (43.31, -2.68), 'Covadonga': (43.31, -5.06), 'Numantia': (41.81, -2.44), 'Segovia': (40.95, -4.12),
    'Merida': (38.92, -6.34), 'Tarragona': (41.12, 1.25), 'Italica': (37.44, -6.05), 'Emporion': (42.13, 3.12), 'Oviedo': (43.36, -5.85),
    'Tyre': (33.27, 35.20), 'Carthage': (36.85, 10.33), 'Rome': (41.90, 12.50), 'Athens': (37.98, 23.73), 'Damascus': (33.51, 36.29),
    'Mecca': (21.42, 39.83), 'Germania': (51.0, 10.0), 'Paris': (48.86, 2.35), 'London': (51.50, -0.12), 'Lepanto': (38.40, 21.80),
    'MexicoCity': (19.43, -99.13), 'Cuzco': (-13.53, -71.97), 'Potosi': (-19.58, -65.75), 'Havana': (23.11, -82.37), 'Manila': (14.60, 120.98),
    'SanSalvador': (24.05, -74.50), 'Atlantic': (33.0, -40.0), 'Pacific': (5.0, -150.0), 'MedSea': (38.5, 5.0), 'Africa': (34.6, -4.6),
    'Europe': (37.4, -4.4), 'Pyrenees': (42.7, 0.8), 'Madrid2': (40.42, -3.70),
}
VIEWS = {   # (lat, lon, width in degrees of longitude)
    'west_eu': (40.5, -2.0, 30), 'iberia': (40.0, -3.6, 15.5), 'spain_n': (42.6, -4.0, 8.5), 'strait': (36.0, -5.55, 2.6),
    'med_w': (38.5, 11.0, 54), 'europe': (46.0, 8.0, 46), 'world_wide': (8.0, 4.0, 248), 'atlantic': (22.0, -45.0, 110),
    'americas': (2.0, -75.0, 90), 'south': (37.6, -4.5, 6.5), 'north': (42.8, -3.0, 9.0), 'east': (40.8, 0.0, 7.5),
}
_AMERICAS = ['Mexico', 'Guatemala', 'Honduras', 'El Salvador', 'Nicaragua', 'Costa Rica', 'Panama', 'Colombia', 'Venezuela', 'Ecuador',
             'Peru', 'Bolivia', 'Chile', 'Argentina', 'Uruguay', 'Paraguay', 'Cuba', 'Dominican Republic', 'Puerto Rico']
GROUPS = {
    'EMPIRE': ['SPAIN'] + _AMERICAS + ['Philippines'],
    'AMERICAS_ES': _AMERICAS,
    'REGIONS': ['GALICIA', 'BASQUE', 'CATALONIA', 'ANDALUSIA'],
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

EMPIRES = [('phoenician', 'Phoenicians'), ('greek', 'Greeks'), ('carthaginian', 'Carthaginians'), ('roman', 'Romans'),
           ('visigoth', 'Visigoths'), ('arab', 'Arabs'), ('moor', 'Berbers')]
def empire_row(n0, n1, y, at=True, off=None, s=66):
    out = []
    for i, (f, name) in enumerate(EMPIRES[n0:n1]):
        x = 0.42 + i * 0.083
        b = badge('cart:fig-' + f, S(x, y), name if at else None, name, f'emp{n0 + i}', s=s, ls=26)
        if off: b['off'] = off
        out.append(b)
    return out
REGION_FILL = [('GALICIA', 'green', 'many'), ('ASTURIAS', 'teal', 'many'), ('BASQUE', 'red', ('many', 0.2)), ('NAVARRE', 'pink', ('many', 0.3)),
               ('CATALONIA', 'yellow', ('many', 0.4)), ('ARAGON_R', 'orange', ('many', 0.5)), ('VALENCIA_R', 'lime', ('many', 0.6)),
               ('ANDALUSIA', 'brown', ('kingdoms', 0.0)), ('CASTILE_LEON', 'purple', ('kingdoms', 0.2)), ('CASTILE_LM', 'sky', ('kingdoms', 0.4)),
               ('PORTUGAL', 'blue', ('kingdoms', 0.6))]

# ------------------------------------------------------------------ phrase-keyed plan: hook and the start of Part 1 (preview)
BY_PHRASE = [
    ('At the south-western corner of Europe', MAP('west_eu', [('IBERIA', 'yellow', 'peninsula')], [label('IBERIAN PENINSULA', (40.2, -4.0), 'peninsula', 'ipl', s=40, spaced=True),
        label('EUROPE', (46.5, 2.5), 0.1, 'eul', s=40, spaced=True), label('AFRICA', (33.2, -2.0), 0.3, 'afl', s=40, spaced=True)])),
    ('so close to Africa', MAP('strait', [('SPAIN', 'yellow', 0.0), ('MOROCCO', 'orange', 'Africa')], [label('EUROPE', 'Europe', 0.0, 'eu2', s=38, spaced=True),
        label('AFRICA', 'Africa', 'Africa', 'af2', s=38, spaced=True), line([(36.02, -5.62), (35.95, -5.58)], 'narrowest', ('narrowest', 1.0), 'gap', w=9),
        pin('Gibraltar', 0.2, 'GIBRALTAR', 'gib', spaced=True)], [BIG(None, '14 km', 'fourteen', color='yellow', x=0.5, y=0.2)])),
    ('Spain covers most of that peninsula', MAP('iberia', [('SPAIN', 'red', 'Spain'), ('PORTUGAL', 'grey', 0.0)], [label('SPAIN', (40.0, -3.4), 'Spain', 'spl', s=48, spaced=True),
        label('PORTUGAL', (39.6, -8.0), 0.2, 'ptl', s=28, spaced=True), badge('flag-es', (43.0, 2.6), 'covers', None, 'fles', s=80)])),
    ('it is home to about forty-nine million people', MAP('iberia', [('SPAIN', 'red')], [label('SPAIN', (40.0, -3.4), None, 'spl', s=48, spaced=True),
        badge('people', (36.0, 1.5), 'forty-nine', None, 'ppl', s=80)], [BIG(None, '49 million', 'forty-nine', color='yellow', x=0.5, y=0.2)])),
    ('one of the most visited countries on Earth', ST(badges([('plane', 'visited', 'tourists'), ('sun', 'visited', 'beaches'), ('cart:fig-tourist', 'Earth', 'from all over the world')], s=100, pre='tv'),
        [CAP('one of the most visited countries', 'visited', x=0.64)])),
    ('almost every great power of the ancient', MAP('med_w', [('IBERIA', 'yellow', 0.0)], [arrow(['Tyre', (34.0, 20.0), (36.0, 5.0), 'Cadiz'], 'power', ('power', 1.6), 'red', 'i1', w=18),
        arrow(['Athens', (38.0, 12.0), 'Emporion'], ('power', 0.3), ('power', 1.8), 'blue', 'i2', w=18), arrow(['Carthage', 'Cartagena'], ('power', 0.5), ('power', 1.9), 'purple', 'i3', w=18),
        arrow(['Rome', (40.6, 6.0), 'Tarragona'], ('power', 0.7), ('power', 2.0), 'red', 'i4', w=18), arrow(['Germania', (45.0, 2.0), 'Toledo'], ('power', 0.9), ('power', 2.2), 'brown', 'i5', w=18),
        arrow(['Damascus', (33.0, 20.0), (34.6, 0.0), 'Gibraltar'], ('power', 1.1), ('power', 2.4), 'green', 'i6', w=18)], [CAP('everyone wanted this land', 'wanted')])),
    ('Phoenicians, Greeks, Carthaginians', ST(empire_row(0, 7, 0.45))),
    ('Every one of them came', ST(empire_row(0, 7, 0.45, at=False), [CAP('came, and left something behind', 'came', x=0.64)])),
    ('Then something strange happened.', MAP('iberia', [('SPAIN', 'red', 0.0)], [badge('question', (43.6, 3.0), 'strange', None, 'qs', s=80)], [CAP('then something strange happened', 'strange')])),
    ('turned around and conquered half the world', MAP('world_wide', [('SPAIN', 'red', 0.0), ('AMERICAS_ES', 'red', ('conquered', 0.8)), ('Philippines', 'red', ('world', 0.5))],
        [arrow(['Seville', (30.0, -40.0), 'Havana'], 'conquered', ('conquered', 1.4), 'red', 'w1', w=20), arrow(['Havana', 'MexicoCity'], ('conquered', 0.8), ('half', 0.6), 'red', 'w2', w=16),
         arrow(['Havana', (5.0, -78.0), 'Cuzco'], ('conquered', 1.0), ('world', 0.6), 'red', 'w3', w=16)], [BIG(None, 'half the world', 'half', color='yellow', x=0.5, y=0.16)])),
    ('the first empire on which the sun never set', MAP('world_wide', [('EMPIRE', 'red')], [badge('sun', (40.0, -40.0), 'sun', None, 'sun1', s=110)],
        [CAP('the empire where the sun never set', 'sun')])),
    ('So how did a land that was conquered', ST([badge('cart:fig-moor', S(0.5, 0.48), 0.0, 'conquered again and again', 'q1a', s=95), badge('crown', S(0.8, 0.48), 'powerful', 'the most powerful empire', 'q1b', s=105)],
        [CAP('how?', 'how', x=0.64, color='yellow')])),
    ('Why did the richest empire in history', ST([badge('silver', S(0.5, 0.48), 'richest', 'the richest empire', 'q2a', s=100), badge('down', S(0.8, 0.48), 'bankrupt', 'bankrupt, again and again', 'q2b', s=100)],
        [BIG(None, 'BANKRUPT', 'bankrupt', color='red')])),
    ('And how did a country that tore itself apart', ST([badge('tank', S(0.5, 0.48), 'civil', 'a brutal civil war', 'q3a', s=100), badge('ballot', S(0.8, 0.48), 'democracy', 'a modern democracy', 'q3b', s=100)],
        [CAP('in a single generation', 'generation', x=0.64)])),
    ('Here is the key', ST([badge('key', S(0.64, 0.5), 'key', None, 'key', s=150)], [CAP('THE KEY', 'key', x=0.64, color='yellow')])),
    ('Spain was never one thing.', MAP('iberia', REGION_FILL, [], [CAP('many peoples, many kingdoms', 'many')])),
    ('with different languages and different faiths', ST([*[badge(f, S(0.42 + i * 0.12, 0.36), ('languages', 0.15 * i), None, f'lf{i}', s=80) for i, f in enumerate(('flag-es', 'flag-cat', 'flag-eus', 'flag-pt'))],
        *[badge(f, S(0.48 + i * 0.14, 0.66), ('faiths', 0.15 * i), None, f'ff{i}', s=80) for i, f in enumerate(('cross', 'crescent', 'star'))]], [CAP('different languages, different faiths', 'languages', x=0.64)])),
    ('Every chapter of its history is a struggle', ST([badge('flag-es', S(0.5, 0.46), 'unity', 'UNITY', 'un', s=110), badge('flag-cat', S(0.8, 0.4), 'difference', None, 'd1', s=70),
        badge('flag-eus', S(0.86, 0.56), ('difference', 0.2), None, 'd2', s=70), badge('flag-pt', S(0.74, 0.58), ('difference', 0.4), 'DIFFERENCE', 'd3', s=70)],
        [CAP('unity vs difference', 'struggle', x=0.64, color='yellow')])),
    ('Keep that in mind', MAP('iberia', [(f[0], f[1]) for f in REGION_FILL], [], [CAP('keep this in mind', 'Keep')])),
    ("Let's go back to the very beginning.", CLK('30,000 years ago', 'beginning')),
    ('Long before there was a Spain', MAP('spain_n', [], [pin('Altamira', 'cave', 'ALTAMIRA', 'alt', spaced=True)], [CAP('people were here first', 'people')])),
    ('Deep inside a cave called Altamira', ST([photo('altamira', 'Altamira cave, northern Spain', 'cave', x=0.64, y=0.5, h=520, id='palt')], [CAP('ALTAMIRA', 'Altamira', x=0.64, color='yellow')])),
    ('Some of those paintings are more than thirty thousand years old.', ST([photo('altamira', 'Altamira cave, northern Spain', None, x=0.64, y=0.56, h=470, id='palt')],
        [BIG(None, '30,000+ years', 'thirty', color='yellow', x=0.64, y=0.13, hy=0.06)])),
    ('By three thousand years ago, the peninsula was home', MAP('iberia', [('CARTHAGE_ES', 'orange', 'Iberians'), ('ROME_2', 'orange', 'Iberians'), ('NORTH_TRIBES', 'green', 'Celtic'), ('GALICIA', 'green', 'Celtic'), ('BASQUE', 'red', 'Basques'), ('NAVARRE', 'red', 'Basques')],
        [label('IBERIANS', (38.6, -2.2), 'Iberians', 'lib', s=38, spaced=True), label('CELTS', (42.3, -6.8), 'Celtic', 'lce', s=38, spaced=True),
         label('BASQUES', (43.6, -1.2), 'Basques', 'lba', s=34, spaced=True)], [CAP('many different peoples', 'many')])),
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

import plan2   # the rest of the video (after the preview)
resolve(os.path.join(os.environ.get('OUT_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build')), 'timing.json'))
