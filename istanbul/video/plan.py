"""Scene-by-scene visual plan for the Istanbul video, in the reference video's style.

bg: 'map' (warm satellite map), 'studio' (grey, guide on the left), 'scene' (flat cartoon world:
sky = day/dusk/night/gold, ground = sand/grass/sea/stone), 'spot' (dark stage with a light cone).
Captions: (handwritten top line, big rounded word/number, at, {color: red|yellow|white, x, y}).
Timing `at`: a spoken word (item appears as it is said), a fraction of the scene (0-1), seconds (>1),
or (word, offset seconds). Screen positions are ('s', x, y) as fractions of the frame."""

PLACES = {
    'Istanbul': (41.01, 28.98), 'Bosphorus': (41.12, 29.06), 'BosN': (41.23, 29.13), 'BosS': (41.0, 29.0),
    'Chalcedon': (40.99, 29.03), 'Megara': (38.0, 23.35), 'Delphi': (38.48, 22.5), 'Rome': (41.9, 12.5),
    'Athens': (37.98, 23.73), 'Crimea': (44.9, 34.1), 'Odessa': (46.48, 30.73), 'Trabzon': (41.0, 39.72),
    'Aegean': (38.5, 25.0), 'Alexandria': (31.2, 29.92), 'Galata': (41.03, 28.98),
}
VIEWS = {   # (lat, lon, width in degrees of longitude)
    'europe': (44.0, 20.0, 52), 'europe_wide': (44.0, 20.0, 52), 'se_europe': (42.3, 27.0, 24), 'marmara': (40.95, 28.7, 9.5),
    'marmara_wide': (41.0, 28.6, 13), 'trade': (40.2, 30.5, 30), 'regions': (43.0, 30.0, 34),
}
GROUPS = {
    'EUROPE_DARK': ['France', 'Germany', 'Italy', 'Spain', 'Portugal', 'United Kingdom', 'Ireland', 'Belgium', 'Netherlands',
                    'Switzerland', 'Austria', 'Poland', 'Czechia', 'Slovakia', 'Hungary', 'Denmark', 'Croatia', 'Slovenia',
                    'Bosnia and Herzegovina', 'Republic of Serbia', 'Romania', 'Bulgaria', 'Montenegro', 'Albania', 'North Macedonia', 'Greece',
                    'Ukraine', 'Belarus', 'Lithuania', 'Latvia', 'Moldova', 'Kosovo', 'Luxembourg'],
}
CUSTOM = {}
BOSPHORUS = [(41.24, 29.14), (41.18, 29.08), (41.11, 29.06), (41.06, 29.03), (41.02, 29.0), (40.98, 28.99)]

# ------------------------------------------------------------------ item helpers
def _d(k, at, id, **kw):
    d = dict(k=k, **kw)
    if at is not None: d['at'] = at
    if id: d['id'] = id
    return d

def label(text, place, at=None, id=None, s=40, **kw): return _d('label', at, id, text=text, at_place=place, s=s, **kw)
def pin(place, at=None, label=None, id=None, **kw): return _d('pin', at, id, at_place=place, label=label, **kw)
def badge(icon, place, at=None, label=None, id=None, s=70, **kw): return _d('badge', at, id, icon=icon, at_place=place, label=label, s=s, **kw)
def ring(place, at=None, id=None, **kw): return _d('ring', at, id, at_place=place, **kw)
def line(path, at=None, to=None, id=None, **kw):
    d = _d('line', at, id, path=path, **kw)
    if to is not None: d['to'] = to
    return d
def arrow(path, at=None, to=None, color='red', id=None, w=22, **kw):
    d = _d('arrow', at, id, path=path, color=color, w=w, **kw)
    if to is not None: d['to'] = to
    return d
def move(icon, path, at=None, to=None, id=None, s=70, **kw):
    d = _d('move', at, id, icon=icon, path=path, s=s, **kw)
    if to is not None: d['to'] = to
    return d
def fire(place, at=None, id=None, size=1.0, n=4, **kw): return _d('fire', at, id, at_place=place, size=size, n=n, **kw)
def prop(kind, x, y, at=None, id=None, h=200, **kw):
    """cartoon prop or figure ('fig-<name>'), bottom-centre at screen fraction (x, y)"""
    return _d('prop', at, id, kind=kind, xy=(x, y), h=h, **kw)
def S(x, y): return ('s', x, y)

def skyline(at=None, x0=0.12, n=1, base=0.80, h=1.0, dome=True):
    """a cartoon Constantinople skyline: land walls, houses and the great dome"""
    out = [prop('wall', 0.5, base, at, 'skwall', h=int(230 * h), kw={'length': 7})]
    if dome: out.append(prop('dome', 0.52, base - 0.2 * h, at, 'skdome', h=int(270 * h)))
    for i, x in enumerate((0.16, 0.30, 0.72, 0.86)):
        out.append(prop('house', x, base - 0.2 * h, at, f'skh{i}', h=int(120 * h), kw={'wide': 1.0 + (i % 2) * 0.4}))
    return out

# ------------------------------------------------------------------ scenes
SCENES = {
    # Hook: the strangest geographic feature on Earth
    1: dict(view='europe_wide', moves=[('zoom', 'se_europe')],
            items=[label('SOUTHEASTERN EUROPE', (44.2, 23.0), 'Southeastern', 'sel', s=46, spaced=True, rot=-5)]),
    2: dict(view='marmara_wide',
            items=[ring('Istanbul', 'strangest'), pin('Bosphorus', 'geographic', id='bpin')],
            cap=[('one of the strangest features on Earth', None, 'strangest')]),
    3: dict(view='marmara', items=[pin('Bosphorus', id='bpin'),
            line(BOSPHORUS, 'ribbon', ('ribbon', 1.4), id='bos', color=(150, 230, 255), w=7, glow=True),
            label('THE BOSPHORUS STRAIT', (41.42, 29.75), 'Bosphorus', 'bosl', s=44, spaced=True)]),
    4: dict(bg='studio',
            items=[prop('house', 0.48, 0.66, 0.05, 'eu_h', h=110), prop('house', 0.88, 0.66, 0.05, 'as_h', h=110, kw={'col': (230, 190, 150, 255)}),
                   label('Europe', S(0.48, 0.72), 0.1, 'eul', s=36), label('Asia', S(0.88, 0.72), 0.1, 'asl', s=36),
                   line([S(0.55, 0.6), S(0.81, 0.6)], 'eight', ('eight', 0.8), id='meas', color=(220, 60, 40), w=6)],
            cap=[('less than', '800 m', 'eight', {'x': 0.68, 'y': 0.34})]),
    5: dict(view='marmara_wide', items=[line(BOSPHORUS, None, None, id='bos', color=(150, 230, 255), w=7, glow=True),
            label('EUROPE', (41.65, 27.3), 'Europe', 'eu', s=54, spaced=True), label('ASIA', (40.45, 30.6), 'Asia', 'as', s=54, spaced=True),
            arrow([(41.45, 28.2), (41.2, 28.75)], 'left', ('left', 0.9), color='white', w=12, id='al'),
            arrow([(40.7, 30.0), (41.0, 29.35)], 'right', ('right', 0.9), color='white', w=12, id='ar')]),
    6: dict(view='trade', items=[label('BLACK SEA', (43.3, 34.0), 'Black', 'bsl', s=46, spaced=True),
            badge('snow', (45.6, 31.5), 'cold', 'cold ports', 'cold', s=60, lead='Odessa'),
            move('cart:galley', [(44.2, 33.0), (42.6, 30.4), 'BosN'], 'ship', 1.0, s=60, id='ship', linear=True)]),
    7: dict(view='trade', items=[label('BLACK SEA', (43.3, 34.0), None, 'bsl', s=46, spaced=True),
            badge('snow', (45.6, 31.5), None, 'cold ports', 'cold', s=60, lead='Odessa'),
            move('cart:galley', ['BosN', 'Istanbul', (40.6, 27.4), (39.0, 25.6), (37.4, 25.0)], 0.0, 0.95, s=60, id='ship2'),
            label('MEDITERRANEAN', (36.2, 26.5), 'Mediterranean', 'medl', s=46, spaced=True),
            badge('gold', (37.2, 32.0), 'wealthy', 'wealthy markets', 'gold', s=60),
            ring('Bosphorus', 'bottleneck')],
            cap=[('this exact bottleneck', None, 'bottleneck')]),
    8: dict(view='marmara_wide', items=[line(BOSPHORUS, None, None, id='bos', color=(150, 230, 255), w=7, glow=True),
            badge('cart:galley', S(0.3, 0.3), 'trade', 'global trade', 'b1', s=70)],
            cap=[('a stranglehold', None, 'stranglehold')]),
    9: dict(view='marmara_wide', moves=[('right', 'marmara')], items=[line(BOSPHORUS, None, None, id='bos', color=(150, 230, 255), w=7, glow=True),
            badge('cart:galley', S(0.3, 0.3), None, 'global trade', 'b1', s=70, off='right'),
            badge('envelope', S(0.5, 0.3), 'diplomacy', 'diplomacy', 'b2', s=70, off='right'),
            badge('gold', S(0.7, 0.3), 'wealth', 'the wealth of nations', 'b3', s=70, off='right'),
            pin('Istanbul', 'city', 'THE CITY', 'cpin', spaced=True)]),
    10: dict(bg='scene', items=[*skyline(0.0), prop('tent', 0.08, 0.95, 0.05, 't1', h=120), prop('tent', 0.2, 0.97, 0.12, 't2', h=110),
             prop('siege_tower', 0.36, 0.95, 'survived', 'st1', h=300), prop('siege_tower', 0.62, 0.96, ('survived', 0.3), 'st2', h=320),
             prop('fig-soldier', 0.46, 0.98, ('survived', 0.5), 'so1', h=210), prop('fig-soldier', 0.53, 0.98, ('survived', 0.7), 'so2', h=210), prop('fig-hun', 0.28, 0.98, ('survived', 0.9), 'so3', h=210)],
             cap=[('gone by', '3 names', 'three'), ('survived more than', '24 sieges', 'twenty-four', {'color': 'yellow'})]),
    11: dict(bg='studio', items=[prop('fig-colonist', 0.44, 0.86, 0.04, 'e1', h=430, say='Greek', ss=44),
             prop('fig-emperor', 0.62, 0.86, 'capital', 'e2', h=430, say='Roman', ss=44), prop('fig-mehmed', 0.80, 0.86, 'three', 'e3', h=430, say='Ottoman', ss=44)],
             cap=[('the capital of', '3 empires', 'greatest', {'x': 0.62})]),
    12: dict(bg='studio', items=[line([S(0.38, 0.62), S(0.95, 0.62)], 0.0, 0.6, id='tl', color=(70, 55, 45), w=5),
             label('then', S(0.40, 0.68), 0.1, 'tth', s=40), label('now', S(0.93, 0.68), 0.1, 'tnw', s=40),
             label('BYZANTIUM', S(0.46, 0.52), 'Byzantium', 'n1', s=72, color=(240, 120, 70)),
             label('CONSTANTINOPLE', S(0.66, 0.42), 'Constantinople', 'n2', s=72, color=(150, 90, 200)),
             label('ISTANBUL', S(0.86, 0.52), 'Istanbul', 'n3', s=72, color=(60, 160, 120))]),
    13: dict(view='se_europe', items=[pin('Istanbul', 0.02, 'THE CITY', 'cpin2', spaced=True),
             badge('cart:dome', (43.4, 27.0), 'wiped', 'wiped off the map?', 'wipe', s=80, x=True, lead='Istanbul')],
             cap=[('a dozen times over', None, 'dozen')]),
    14: dict(view='regions', items=[pin('Istanbul', None, 'THE CITY', 'cpin2', spaced=True),
             arrow([(47.0, 24.0), (44.5, 27.0), (41.6, 28.6)], 'nomadic', ('nomadic', 1.0), id='a1'),
             badge('horseman', (46.4, 25.5), 'nomadic', 'nomadic hordes', 'h1', s=62),
             arrow([(38.5, 35.5), (40.0, 32.0), (40.8, 29.6)], 'religious', ('religious', 1.0), id='a2'),
             badge('burst', (38.0, 34.5), 'religious', 'religious wars', 'h2', s=62),
             badge('cart:fig-soldier', (44.6, 33.5), 'betrayals', 'betrayals', 'h3', s=62)]),
    15: dict(bg='scene', shake=[('earthquakes', 2.8, 16)],
             items=[*skyline(0.0), badge('skull', S(0.3, 0.32), 'plagues', 'plagues', 'pl', s=70),
                    badge('burst', S(0.7, 0.32), 'earthquakes', 'earthquakes', 'eq', s=70)],
             cap=[('shook its monuments to pieces', None, 'shook')]),
    16: dict(view='europe_wide', fill=[('EUROPE_DARK', 'dark', 'collapsed')],
             items=[ring('Istanbul', 'thousand'), pin('Istanbul', 'thousand', 'THE CITY', 'cpin3', spaced=True)],
             cap=[('while Europe fell into the dark ages', None, 'collapsed')]),
    17: dict(bg='studio', items=[badge('gold', S(0.46, 0.46), 'richest', 'richest', 'r1', s=120),
             badge('crown', S(0.66, 0.46), 'opulent', 'most opulent', 'r2', s=120), badge('cart:wall', S(0.86, 0.46), ('opulent', 0.7), 'impenetrable', 'r3', s=120)],
             cap=[('the richest city on the planet', None, 'richest', {'x': 0.62})]),
    18: dict(bg='scene', items=[prop('wall', 0.5, 0.86, 'walls', 'bw', h=420, kw={'length': 4}),
             prop('fig-byz_soldier', 0.30, 0.45, ('walls', 0.3), 'g1', h=180), prop('fig-byz_soldier', 0.58, 0.45, ('walls', 0.5), 'g2', h=180)],
             cap=[('the most impenetrable city', None, 'impenetrable'), ('stone walls so massive...', None, 'walls')]),
    19: dict(bg='scene', items=[prop('wall', 0.5, 0.86, None, 'bw', h=420, kw={'length': 4}),
             prop('fig-byz_soldier', 0.30, 0.45, None, 'g1', h=180), prop('fig-byz_soldier', 0.58, 0.45, None, 'g2', h=180),
             prop('angel', 0.25, 0.36, 'angels', 'an1', h=190, bob=12), prop('angel', 0.70, 0.32, ('angels', 0.3), 'an2', h=170, bob=12),
             prop('flask', 0.5, 0.72, 'liquid', 'fl', h=230)],
             cap=[('built by angels?', None, 'angels'), ('a mysterious liquid weapon', None, 'liquid')]),
    20: dict(bg='scene', ground='sea', horizon=0.55,
             items=[prop('galley', 0.28, 0.82, 0.0, 'eg1', h=240, kw={'emblem': 'crescent'}), prop('galley', 0.62, 0.9, 0.05, 'eg2', h=280, kw={'emblem': 'crescent'}),
                    fire(S(0.26, 0.70), 'burst', 'f1', size=1.8, n=5), fire(S(0.64, 0.76), ('burst', 0.3), 'f2', size=2.0, n=5),
                    fire(S(0.46, 0.9), 'flames', 'f3', size=1.0, n=4), fire(S(0.8, 0.88), ('flames', 0.3), 'f4', size=1.1, n=4)],
             cap=[('unquenchable flames on the water', None, 'flames')]),
    21: dict(bg='scene', ground='sand', horizon=0.7,
             items=[prop('hut', 0.22, 0.88, 0.02, 'v1', h=240), prop('hut', 0.42, 0.85, 0.06, 'v2', h=210), prop('hut', 0.62, 0.89, 0.1, 'v3', h=230),
                    prop('boat', 0.78, 0.95, 0.12, 'v4', h=150), prop('tree', 0.07, 0.86, 0.02, 'v5', h=320),
                    prop('fig-villager', 0.52, 0.98, 0.15, 'v6', h=230),
                    badge('crown', S(0.5, 0.36), 'prize', 'the ultimate prize', 'prize', s=80)],
             cap=[('a small forgotten Greek fishing village', None, 'forgotten')]),
    22: dict(bg='spot', guide=False,
             items=[prop('pedestal', 0.62, 0.88, 0.0, 'ped', h=440, pop=False),
                    prop('fig-pope', 0.12, 0.88, 0.02, 'cl1', h=400, say='Mine.', ss=44),
                    prop('fig-sultan', 0.27, 0.88, 0.6, 'cl2', h=400, say='Mine!', ss=44),
                    prop('fig-king', 0.42, 0.88, 1.2, 'cl3', h=400, say='No, MINE!', ss=44),
                    prop('fig-barbarian', 0.86, 0.88, 'barbarians', 'cl4', h=400, say='Mine!!', ss=44)],
             cap=[('just to fly their flag above its towers', None, 'flag')]),
}
