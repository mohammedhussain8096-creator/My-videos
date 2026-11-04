"""Scene-by-scene visual plan, following the reference video's map style and the script's [ON SCREEN] cues.

Each scene: view (named view or (lat, lon, width in degrees)), year tag, country fills, items
(icons, labels, arrows, movers), captions (small line, big yellow line). Timing `at` is a word from the
voice-over (the item appears as that word is spoken), a fraction of the scene (0-1) or seconds (>1).
Items/fills that repeat in the next scene with the same id carry over without popping in again."""

PLACES = {
    'Paris': (48.86, 2.35), 'Moscow': (55.75, 37.62), 'Smolensk': (54.78, 32.04), 'Kovno': (54.90, 23.90),
    'Vilnius': (54.69, 25.28), 'Vitebsk': (55.19, 30.20), 'Polotsk': (55.49, 28.79), 'Orsha': (54.51, 30.42),
    'Minsk': (53.90, 27.56), 'StPetersburg': (59.94, 30.31), 'Berlin': (52.52, 13.40), 'Warsaw': (52.23, 21.01),
    'Vienna': (48.21, 16.37), 'Milan': (45.46, 9.19), 'Konigsberg': (54.71, 20.51), 'Borodino': (55.52, 35.82),
    'Vyazma': (55.21, 34.29), 'Madrid': (40.42, -3.70), 'Rome': (41.9, 12.5), 'Dresden': (51.05, 13.74),
    'Gzhatsk': (55.55, 35.0), 'RussiaMid': (62.0, 95.0), 'Mozhaysk': (55.5, 36.03),
}

VIEWS = {   # (lat, lon, width in degrees of longitude)
    'moscow': (55.6, 37.0, 17), 'europe': (51.6, 17.0, 64), 'europe_east': (53.0, 24.0, 46),
    'neman': (54.9, 25.5, 20), 'road': (55.0, 29.8, 22), 'road_east': (55.0, 33.6, 14), 'smolensk': (55.0, 32.6, 16),
    'russia': (61.0, 103.0, 170), 'west_russia': (56.5, 31.0, 30), 'europe_russia': (55.0, 30.0, 80),
}

GROUPS = {
    'RUSSIAN_EMPIRE': ['Russia', 'Belarus', 'Ukraine', 'Lithuania', 'Latvia', 'Estonia', 'Finland', 'Moldova'],
    'FRANCE': ['France', 'Belgium', 'Netherlands', 'Luxembourg', 'Switzerland'],
}

# ------------------------------------------------------------------ item helpers
def icon(kind, at_place, at=None, label=None, id=None, s=70, **kw):
    d = dict(k='icon', icon=kind, at_place=at_place, label=label, s=s, **kw)
    if at is not None: d['at'] = at
    if id: d['id'] = id
    return d

def label(text, at_place, at=None, id=None, s=30, **kw):
    d = dict(k='label', text=text, at_place=at_place, s=s, **kw)
    if at is not None: d['at'] = at
    if id: d['id'] = id
    return d

def city(text, at_place, at=None, id=None, **kw):
    d = dict(k='city', text=text, at_place=at_place, **kw)
    if at is not None: d['at'] = at
    if id: d['id'] = id
    return d

def arrow(path, at=None, to=None, color='blue', id=None, w=26, **kw):
    d = dict(k='arrow', path=path, color=color, w=w, **kw)
    if at is not None: d['at'] = at
    if to is not None: d['to'] = to
    if id: d['id'] = id
    return d

def move(kind, path, at=None, to=None, id=None, s=70, **kw):
    d = dict(k='move', icon=kind, path=path, s=s, **kw)
    if at is not None: d['at'] = at
    if to is not None: d['to'] = to
    if id: d['id'] = id
    return d

def fire(at_place, at=None, id=None, size=1.0, n=4, **kw):
    d = dict(k='fire', at_place=at_place, size=size, n=n, **kw)
    if at is not None: d['at'] = at
    if id: d['id'] = id
    return d

def xmark(at_place, at=None, s=56, **kw):
    d = dict(k='xmark', at_place=at_place, s=s, **kw)
    if at is not None: d['at'] = at
    return d

def ring(at_place, at=None, **kw):
    d = dict(k='ring', at_place=at_place, **kw)
    if at is not None: d['at'] = at
    return d

NAP = lambda at=None, place='Paris', id='nap', **kw: icon('badge-napoleon', place, at, 'Napoleon Bonaparte', id, s=118, drop=False, **kw)
RU_LABEL = lambda at=None, place=(57.2, 33.0), **kw: icon('flag-ru', place, at, 'Russian Empire', 'rulabel', s=34, pill=False, ls=30, **kw)
FR_LABEL = lambda at=None, **kw: icon('flag-fr', (47.2, 2.6), at, 'French Empire', 'frlabel', s=34, pill=False, ls=30, **kw)
MOSCOW = lambda at=None, **kw: icon('castle', 'Moscow', at, None, 'moscow', s=70, **kw)
MOSCOW_LBL = lambda at=None, **kw: label('MOSCOW', 'Moscow', at, 'moscowlbl', s=40, dy=30, **kw)
EUROPE_FILLS = [('FRANCE', 'blue'), ('Germany', 'blue'), ('Italy', 'blue'), ('Poland', 'blue')]

def cities(*names, at=0.0):
    pos = {'Vilnius': 'Vilnius', 'Vitebsk': 'Vitebsk', 'Smolensk': 'Smolensk', 'Moscow': 'Moscow', 'Minsk': 'Minsk',
           'Polotsk': 'Polotsk', 'Kovno': 'Kovno', 'Vyazma': 'Vyazma', 'Orsha': 'Orsha'}
    return [city(n, pos[n], at, 'c_' + n, s=24) for n in names]

# ------------------------------------------------------------------ scenes
SCENES = {
    # 0:00 The Hook ---------------------------------------------------------
    1: dict(view='europe_russia', year='1812', zoom=0.10,
            fill=[('FRANCE', 'blue', 0.0), ('RUSSIAN_EMPIRE', 'red', 'Russia')],
            items=[NAP(0.02),
                   arrow(['Paris', 'Berlin', 'Kovno', 'Smolensk', 'Moscow'], 'march', 'Russia', id='a_open', w=30),
                   icon('army-fr', (50.3, 8.5), '600,000', None, 'o1', s=50), icon('army-fr', (52.6, 15.5), 'men', None, 'o2', s=50),
                   icon('army-fr', (54.0, 22.0), 'into', None, 'o3', s=50),
                   icon('castle', 'Moscow', 'Russia', None, 'o_m', s=56), label('MOSCOW', 'Moscow', 'Russia', 'o_ml', s=30, dy=26)],
            title=dict(big='1812', at='1812', size=200, y=0.24),
            cap=[('MORE THAN', '600,000 MEN', '600,000', {'count': 1.0})]),
    2: dict(view='moscow', year='1812',
            items=[MOSCOW(0.02), MOSCOW_LBL(0.05), NAP('take', place='Moscow', dx=-150, dy=-70),
                   xmark('Moscow', 'lose', dx=60, dy=-40, s=80)],
            cap=[('', 'YOU TAKE MOSCOW', 'take'), ('YOU LOSE ALMOST', 'EVERYTHING', 'lose'), ('', 'WHY?', 'Why')]),
    3: dict(view='europe',
            fill=[('FRANCE', 'blue', 'conquered')] + [(c, 'blue', 'Europe') for c in ('Germany', 'Italy', 'Poland')] +
                 [('RUSSIAN_EMPIRE', 'red', 'country')],
            items=[NAP('man'), FR_LABEL('conquered'), RU_LABEL('country'),
                   icon('question', (57.5, 40.0), 'not', None, 'q', s=90)],
            cap=[('THE MAN WHO', 'CONQUERED EUROPE', 'conquered')]),
    4: dict(view='europe',
            fill=[('FRANCE', 'blue'), ('Germany', 'blue'), ('Italy', 'blue'), ('Poland', 'blue'), ('RUSSIAN_EMPIRE', 'red')],
            items=[NAP(), FR_LABEL(), RU_LABEL(),
                   arrow(['Paris', 'Berlin', 'Kovno', 'Smolensk', 'Moscow'], 'armies', 'same', id='a1812'),
                   label('1812', (51.0, 24.0), 'armies', 'l1812', s=34),
                   arrow([(52.2, 13.6), (53.5, 24.0), (55.3, 33.0), (55.9, 36.6)], 'same', 'mistake', color='grey', id='a1941'),
                   icon('badge-hitler', 'Berlin', 'same', None, 'hit', s=80, drop=False, dy=10),
                   label('1941', (54.3, 28.0), 'mistake', 'l1941', s=34),
                   icon('castle', 'Moscow', 'armies', None, 'moscow_e', s=46)],
            cap=[('TWO GREAT ARMIES', 'THE SAME MISTAKE', 'same')]),
    5: dict(view='europe', years=[('Today', 'TODAY')],
            fill=[('FRANCE', 'blue'), ('Germany', 'blue'), ('Italy', 'blue'), ('Poland', 'blue'), ('RUSSIAN_EMPIRE', 'red'),
                  ('Russia', 'red', 'Today')],
            unfill=[('FRANCE', 'Today'), ('Germany', 'Today'), ('Italy', 'Today'), ('Poland', 'Today'), ('RUSSIAN_EMPIRE', 'Today')],
            moves=[('Today', 'russia')],
            items=[NAP(off='Today'), FR_LABEL(off='Today'), RU_LABEL(off='Today'),
                   arrow(['Paris', 'Berlin', 'Kovno', 'Smolensk', 'Moscow'], id='a1812', off='Today'),
                   arrow([(52.2, 13.6), (53.5, 24.0), (55.3, 33.0), (55.9, 36.6)], color='grey', id='a1941', off='Today'),
                   icon('badge-hitler', 'Berlin', None, None, 'hit', s=80, drop=False, dy=10, off='Today'),
                   label('1812', (51.0, 24.0), None, 'l1812', s=34, off='Today'), label('1941', (54.3, 28.0), None, 'l1941', s=34, off='Today'),
                   icon('castle', 'Moscow', None, None, 'moscow_e', s=46, off='Today'),
                   icon('crown', (61.5, 96.0), 'power', None, 'crown', s=80)],
            cap=[('', '129 YEARS APART', '129'), ('THE HIDDEN SOURCES', 'OF RUSSIAN POWER', 'hidden')]),
    6: dict(view='russia', year='TODAY', years=[('starts', '1812')],
            fill=[('Russia', 'red'), ('RUSSIAN_EMPIRE', 'red', 'starts')], unfill=[('Russia', 'starts')],
            moves=[('starts', 'moscow')],
            items=[icon('crown', (61.5, 96.0), None, None, 'crown', s=80, off='starts')],
            cap=[('', 'NOT OPINIONS.', 'Not'), ('', 'HISTORY.', 'History'), ('IT STARTS ON A', 'SEPTEMBER AFTERNOON', 'September')]),
    # Part 1: The Empty City ---------------------------------------------------
    7: dict(view='moscow', fill=[('RUSSIAN_EMPIRE', 'red')], tint=None,
            items=[MOSCOW('gates'), MOSCOW_LBL('gates'), NAP('emperor', place='Moscow', dx=-170, dy=-40),
                   label('EMPTY', 'Moscow', 'empty', 'empty', s=34, dx=120, dy=-80, color=(255, 214, 64))],
            cap=[('AN EMPEROR AT THE GATES', 'OF AN EMPTY CITY', 'emperor')]),
    8: dict(view='neman', fill=[('RUSSIAN_EMPIRE', 'red', 0.0)],
            items=[label('NEMAN RIVER', (55.35, 23.2), 'Neman', 'nemanlbl', s=32, color=(140, 200, 255)),
                   arrow([(54.25, 18.8), (54.75, 21.6), 'Kovno', (54.85, 25.6)], 'crosses', 'Russian', id='inv'),
                   NAP('Napoleon', place=(53.9, 21.0)),
                   move('army-fr', [(54.25, 18.8), (54.75, 21.6), 'Kovno', (54.85, 25.6)], 'crosses', 'Empire', id='army', s=52),
                   RU_LABEL('Russian', place=(55.9, 29.6))],
            cap=[('JUNE 24', '1812', 'June'), ('NAPOLEON CROSSES', 'THE NEMAN', 'crosses')]),
    9: dict(view='europe_east', fill=[('RUSSIAN_EMPIRE', 'red'), ('FRANCE', 'blue', 0.05), ('Poland', 'blue', 0.05), ('Germany', 'blue', 0.05)],
            items=[arrow([(54.25, 18.8), (54.75, 21.6), 'Kovno', (54.85, 25.6)], id='inv'),
                   RU_LABEL(place=(57.0, 33.0)),
                   icon('army-fr', (53.3, 14.5), 'largest', None, 'ar1', s=48), icon('army-fr', (52.4, 19.5), 'army', None, 'ar2', s=48),
                   icon('army-fr', (54.3, 23.5), 'Europe', None, 'ar3', s=48), icon('army-fr', (51.2, 9.0), 'seen', None, 'ar4', s=48)],
            cap=[('THE LARGEST ARMY', 'EUROPE HAD EVER SEEN', 'largest'), ('MORE THAN', '600,000 MEN', '600,000', {'count': 1.0})]),
    10: dict(view='europe', fill=[('RUSSIAN_EMPIRE', 'red'), ('FRANCE', 'blue', 'French'), ('Poland', 'blue', 'Polish'),
                                  ('Germany', 'blue', 'German'), ('Italy', 'blue', 'Italian'), ('Austria', 'blue', 'Austrian')],
             items=[icon('flag-fr', (46.8, 2.5), 'French', 'FRENCH', 'f1', s=46, pill=False, ls=26),
                    icon('flag-pl', (52.3, 19.2), 'Polish', 'POLISH', 'f2', s=46, pill=False, ls=26),
                    icon('flag-de', (51.0, 10.2), 'German', 'GERMAN', 'f3', s=46, pill=False, ls=26),
                    icon('flag-it', (43.0, 12.2), 'Italian', 'ITALIAN', 'f4', s=46, pill=False, ls=26),
                    icon('flag-at', (47.6, 14.5), 'Austrian', 'AUSTRIAN', 'f5', s=46, pill=False, ls=26),
                    RU_LABEL(place=(57.0, 36.0)),
                    arrow([(48.6, 4.0), (51.4, 12.5), (53.2, 20.0), (54.85, 25.6)], 'marching', 'flag', color='blue', id='march', w=34)],
             cap=[('SOLDIERS FROM', 'HALF A CONTINENT', 'Soldiers'), ('MARCHING UNDER', 'ONE FLAG', 'one')]),
    11: dict(view='west_russia', fill=[('RUSSIAN_EMPIRE', 'red')],
             items=[NAP('plan', place='Kovno', dx=-20),
                    icon('army-ru', 'Vitebsk', 'Find', None, 'ruarmy', s=56), ring('Vitebsk', 'Find', dy=-20),
                    icon('burst', 'Vitebsk', 'Crush', None, 'crush', s=120, drop=False, dy=-20),
                    icon('badge-tsar', 'StPetersburg', 'Tsar', 'Tsar Alexander I', 'tsar', s=96, drop=False),
                    icon('flag-fr', 'StPetersburg', 'surrender', None, 'wf', s=40, dx=70, dy=-40)],
             cap=[('', 'THE PLAN', 'plan'), ('FIND THE RUSSIAN ARMY', 'CRUSH IT', 'Crush'), ('FORCE THE TSAR', 'TO SURRENDER', 'Force')]),
    12: dict(view='europe', fill=[('RUSSIAN_EMPIRE', 'red'), ('FRANCE', 'blue')],
             items=[NAP(at=0.0),
                    icon('flag-at', 'Vienna', 'Austria', 'Austria', 'at', s=50), icon('burst', 'Vienna', 'Austria', None, 'atb', s=80, drop=False, dy=-60, off='Prussia'),
                    icon('flag-prussia', 'Berlin', 'Prussia', 'Prussia', 'pr', s=50), icon('burst', 'Berlin', 'Prussia', None, 'prb', s=80, drop=False, dy=-60, off='everywhere'),
                    arrow(['Paris', (49.5, 10.0), 'Vienna'], 'Austria', 1.8, color='blue', id='toat', w=20),
                    arrow(['Paris', (51.5, 7.0), 'Berlin'], 'Prussia', 'Prussia#1', color='blue', id='topr', w=20)],
             cap=[('IT HAD WORKED', 'EVERYWHERE', 'everywhere')]),
    13: dict(view='road', fill=[('RUSSIAN_EMPIRE', 'red')],
             items=[*cities('Vilnius', 'Vitebsk', 'Smolensk', 'Minsk'), icon('army-ru', 'Vilnius', 0.02, None, 'ru1', s=56),
                    icon('question', 'Vilnius', 'strange', None, 'q2', s=70, dy=-80, off='fight'),
                    xmark('Vilnius', 'fight', dx=70, dy=-30, s=56, off='retreat'),
                    arrow(['Vilnius', 'Polotsk', 'Vitebsk', 'Smolensk'], 'retreat', 1.0, color='red', id='retr'),
                    move('army-ru', ['Vilnius', 'Polotsk', 'Vitebsk', 'Smolensk'], 'retreat', 1.0, s=56, id='rum')],
             cap=[('THEY DO NOT FIGHT', 'THEY RETREAT', 'retreat')]),
    14: dict(view='road', fill=[('RUSSIAN_EMPIRE', 'red')], tint='fire',
             items=[*cities('Vilnius', 'Vitebsk', 'Smolensk', 'Minsk'), arrow(['Vilnius', 'Polotsk', 'Vitebsk', 'Smolensk'], color='red', id='retr'),
                    fire('Polotsk', 'burn', 'f1'), fire('Vitebsk', 'they#2', 'f2'), fire('Minsk', 'Crops', 'f3', size=0.8),
                    icon('wheat', 'Minsk', 'Crops', None, 'wh', s=60, dx=60),
                    fire('Orsha', 'villages', 'f4', size=0.8), icon('house', 'Orsha', 'villages', None, 'ho', s=56, dx=-60),
                    fire((55.8, 26.5), 'bridges', 'f5', size=0.7), icon('bridge', (55.8, 26.5), 'bridges', None, 'br', s=50, dx=70),
                    move('army-ru', ['Vilnius', 'Polotsk', 'Vitebsk', 'Smolensk'], s=56, id='rum')],
             cap=[('AS THEY RETREAT', 'THEY BURN', 'burn'), ('ANYTHING THE FRENCH', 'COULD USE', 'anything')]),
    15: dict(view='road', fill=[('RUSSIAN_EMPIRE', 'red')], tint='fire',
             items=[*cities('Vilnius', 'Vitebsk', 'Smolensk', 'Minsk'), fire('Polotsk', id='f1'), fire('Vitebsk', id='f2'), fire('Minsk', id='f3', size=0.8), fire('Orsha', id='f4', size=0.8),
                    fire((55.8, 26.5), id='f5', size=0.7),
                    arrow(['Kovno', 'Vilnius', (55.0, 27.8), 'Vitebsk'], 'marching', 'him', color='blue', id='frm'),
                    move('badge-napoleon', ['Kovno', 'Vilnius', (55.0, 27.8), 'Vitebsk'], 'marching', 'him', s=86, id='napm'),
                    label('EMPTY', (54.0, 31.5), 'emptied', 'emp', s=40, color=(255, 214, 64))],
             cap=[('DEEPER AND DEEPER', 'INTO RUSSIA', 'deeper'), ('A LAND BEING', 'EMPTIED', 'emptied')]),
    16: dict(view='road', fill=[('RUSSIAN_EMPIRE', 'red')],
             items=[*cities('Vilnius', 'Vitebsk', 'Smolensk', 'Minsk'), arrow(['Kovno', 'Vilnius', (55.0, 27.8), 'Vitebsk'], color='blue', id='frm'),
                    icon('army-fr', (55.0, 27.8), 0.02, None, 'fra', s=60),
                    icon('skull', (55.0, 27.8), 'die', None, 'sk', s=54, dx=-20, dy=-80),
                    icon('sun', (55.0, 27.8), 'heat', 'HEAT', 'sun', s=78, dx=110, dy=-90)],
             cap=[('THEY BEGIN TO DIE', 'BEFORE ANY BATTLE', 'die')]),
    17: dict(view='road', fill=[('RUSSIAN_EMPIRE', 'red')],
             items=[*cities('Vilnius', 'Vitebsk', 'Smolensk', 'Minsk'), arrow(['Kovno', 'Vilnius', (55.0, 27.8), 'Vitebsk'], color='blue', id='frm'),
                    icon('army-fr', (55.0, 27.8), None, None, 'fra', s=60),
                    icon('skull', (55.0, 27.8), None, None, 'sk', s=54, dx=-20, dy=-80),
                    icon('sun', (55.0, 27.8), None, 'HEAT', 'sun', s=78, dx=110, dy=-90),
                    icon('germ', (55.0, 27.8), 'disease', 'DISEASE', 'germ', s=70, dx=-150, dy=-150),
                    icon('bowl', (55.0, 27.8), 'hunger', 'HUNGER', 'bowl', s=56, dx=300, dy=-110),
                    icon('horseshoe', 'Vilnius', 'Horses', None, 'hs', s=60, dy=110), xmark('Vilnius', 'collapse', dx=30, dy=60, s=44),
                    icon('horseshoe', 'Vitebsk', 'thousands', None, 'hs2', s=60, dy=130, dx=-40), xmark('Vitebsk', 'thousands', dx=-10, dy=80, s=44)],
             cap=[('', 'DISEASE', 'disease'), ('', 'HUNGER', 'hunger'), ('HORSES COLLAPSE', 'BY THE THOUSANDS', 'Horses')]),
    18: dict(view='road_east', fill=[('RUSSIAN_EMPIRE', 'red')], years=[('August', 'AUG 1812')],
             items=[*cities('Vitebsk', 'Vyazma', 'Moscow'), arrow(['Vitebsk', (55.0, 31.2), 'Smolensk'], 'reach', 'Smolensk', color='blue', id='tosm'),
                    icon('castle', 'Smolensk', 'Smolensk', None, 'sm', s=66),
                    label('SMOLENSK', 'Smolensk', 'Smolensk', 'smlbl', s=38, dy=30),
                    NAP('Napoleon', place='Vitebsk', dx=40, dy=-60),
                    icon('cannon', 'Smolensk', 'decisive', None, 'can', s=56, dx=-130, dy=-40)],
             cap=[('ONE OF RUSSIA\'S', 'OLDEST CITIES', 'oldest'), ('', 'THE DECISIVE BATTLE?', 'decisive')]),
    19: dict(view='road_east', fill=[('RUSSIAN_EMPIRE', 'red')], tint='fire',
             items=[*cities('Vitebsk', 'Vyazma', 'Moscow'), arrow(['Vitebsk', (55.0, 31.2), 'Smolensk'], color='blue', id='tosm'),
                    icon('castle', 'Smolensk', None, None, 'sm', s=66), label('SMOLENSK', 'Smolensk', None, 'smlbl', s=38, dy=30),
                    NAP(place='Vitebsk', dx=40, dy=-60),
                    icon('burst', 'Smolensk', 'fight', None, 'fb', s=100, drop=False, dy=-50, off='ablaze'),
                    fire('Smolensk', 'ablaze', 'smf', size=1.3, n=5),
                    arrow(['Smolensk', 'Vyazma', 'Gzhatsk'], 'slip', 'east', color='red', id='ruesc'),
                    move('army-ru', ['Smolensk', 'Vyazma', 'Gzhatsk'], 'slip', 'east', s=56, id='rue')],
             cap=[('', 'THE CITY ABLAZE', 'ablaze'), ('THE RUSSIANS', 'SLIP AWAY', 'slip')]),
    20: dict(view='road_east', fill=[('RUSSIAN_EMPIRE', 'red')], snow=0.5, snow_at='winter',
             items=[*cities('Vitebsk', 'Vyazma', 'Moscow'), arrow(['Vitebsk', (55.0, 31.2), 'Smolensk'], color='blue', id='tosm'),
                    icon('castle', 'Smolensk', None, None, 'sm', s=66), label('SMOLENSK', 'Smolensk', None, 'smlbl', s=38, dy=30),
                    fire('Smolensk', id='smf', size=1.3, n=5),
                    arrow(['Smolensk', 'Vyazma', 'Gzhatsk'], color='red', id='ruesc'),
                    move('army-ru', ['Smolensk', 'Vyazma', 'Gzhatsk'], s=56, id='rue'),
                    NAP(place='Vitebsk', dx=40, dy=-60),
                    icon('snow', 'Vitebsk', 'winter', None, 'sn', s=60, dx=150, dy=-100),
                    xmark('Vitebsk', 'refuses', dx=150, dy=-100, s=60),
                    arrow(['Smolensk', 'Vyazma', 'Mozhaysk'], 'push', 'it', color='blue', id='push', w=30)],
             cap=[('STOP FOR', 'THE WINTER?', 'winter'), ('', 'NAPOLEON REFUSES', 'refuses'), ('', 'ONE MORE PUSH', 'push')]),
    21: dict(view='moscow', fill=[('RUSSIAN_EMPIRE', 'red')],
             items=[MOSCOW('Moscow'), MOSCOW_LBL('Moscow'),
                    icon('crown', 'Moscow', 'prize', None, 'mcr', s=64, dy=-90),
                    arrow([(55.3, 32.2), (55.45, 34.5), (55.65, 36.6)], 'Take', 'surrender', color='blue', id='tom'),
                    icon('badge-tsar', 'Moscow', 'Tsar', 'Tsar Alexander I', 'tsar2', s=90, drop=False, dx=200, dy=-60)],
             cap=[('', 'THE PRIZE', 'prize'), ('THE TSAR MUST', 'SURRENDER', 'surrender')]),
}
