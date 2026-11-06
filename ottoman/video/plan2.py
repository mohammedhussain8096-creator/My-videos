"""Visual plan for paragraphs 13-208 of the Ottoman script (after the preview), same phrase-keyed conventions as plan.py."""
from plan import (BY_PHRASE, PLACES, VIEWS, GROUPS, CUSTOM, _blob, label, pin, badge, ring, arrow, move, prop, photo, clock, S, DUSK, camp)

PLACES.update({
    'Dardanelles': (40.2, 26.4), 'Rhodes': (36.2, 28.0), 'Mohacs': (45.99, 18.68), 'Preveza': (38.96, 20.75), 'Lesbos': (39.2, 26.3),
    'Toulon': (43.12, 5.93), 'Paris': (48.86, 2.35), 'Madrid': (40.42, -3.7), 'Malta': (35.9, 14.5), 'Szigetvar': (46.05, 17.8),
    'Crete': (35.24, 24.9), 'Candia': (35.34, 25.13), 'Lepanto': (38.25, 21.5), 'Cyprus': (35.1, 33.3), 'Venice': (45.44, 12.33),
    'Karlowitz': (45.2, 19.93), 'Crimea': (45.0, 34.1), 'Moscow': (55.75, 37.62), 'Athens': (37.98, 23.73), 'Damascus': (33.51, 36.29),
    'Jerusalem': (31.78, 35.22), 'Medina': (24.47, 39.61), 'Chaldiran': (39.1, 44.0), 'Tabriz': (38.08, 46.29), 'Marj': (36.5, 37.0),
    'Thessaloniki': (40.64, 22.94), 'Toledo': (39.86, -4.03), 'Sarajevo': (43.86, 18.41), 'Dolmabahce': (41.04, 29.0),
    'Gallipoli2': (40.25, 26.4), 'Berlin': (52.52, 13.4),
})
VIEWS.update({
    'marmara': (40.4, 27.8, 9), 'balkans': (42.3, 24.5, 22), 'kosovo': (42.6, 22.0, 10), 'anatolia_wide': (39.5, 33.5, 26),
    'east': (36.0, 40.0, 36), 'med': (38.5, 16.0, 46), 'west_med': (39.0, 6.0, 30), 'hungary': (46.0, 19.0, 16),
    'vienna': (47.2, 17.5, 14), 'black_sea': (44.0, 33.0, 26), 'egypt': (29.0, 31.0, 18), 'crete': (36.0, 25.0, 12),
    'arab': (30.0, 40.0, 34), 'turkey': (39.2, 35.0, 24), 'europe_wide': (45.0, 18.0, 60),
})
def _clip(ring, lon_max):
    """Sutherland-Hodgman clip of a (lon, lat) ring to lon <= lon_max"""
    out = []
    for i in range(len(ring)):
        (x0, y0), (x1, y1) = ring[i - 1], ring[i]
        in0, in1 = x0 <= lon_max, x1 <= lon_max
        if in1:
            if not in0: out.append((lon_max, y0 + (y1 - y0) * (lon_max - x0) / (x1 - x0)))
            out.append((x1, y1))
        elif in0:
            out.append((lon_max, y0 + (y1 - y0) * (lon_max - x0) / (x1 - x0)))
    return out
def _turkey(lon_max, europe=False):
    def f(P):
        rings = []
        for r in P['Turkey']:
            cx = sum(x for x, _ in r) / len(r); cy = sum(y for _, y in r) / len(r)
            is_eu = cx < 29.2 and cy > 40.8
            if europe != is_eu or len(r) < 20: continue
            c = _clip(r, lon_max)
            if len(c) > 3: rings.append(c)
        return rings
    return f
CUSTOM.update({
    'BURSA': _blob(29.3, 40.1, 0.9, 0.55, seed=20), 'ANAT_W': _turkey(31.6),
    'THRACE': _turkey(30.0, europe=True), 'ANAT_C': _turkey(36.0),
    'TIMUR': _blob(55.0, 37.0, 9.0, 5.0, seed=24), 'HEJAZ': _blob(39.0, 23.0, 2.6, 4.5, seed=25),
})
T_ = lambda *names: list(names)
EARLY = ['OSMAN', 'BURSA']
E1389 = ['ANAT_W', 'THRACE', 'Bulgaria', 'North Macedonia']
E1451 = ['ANAT_W', 'ANAT_C', 'Bulgaria', 'North Macedonia', 'Greece', 'Albania', 'Kosovo']
E1520 = ['Turkey', 'Bulgaria', 'North Macedonia', 'Greece', 'Albania', 'Kosovo', 'Republic of Serbia', 'Bosnia and Herzegovina', 'Montenegro',
         'Syria', 'Lebanon', 'Israel', 'Palestine', 'Jordan', 'Egypt', 'HEJAZ']
E1566 = E1520 + ['Hungary', 'Iraq', 'Algeria', 'Libya', 'Romania', 'Moldova', 'Croatia', 'Cyprus']
E1683 = E1566 + ['Tunisia', 'Georgia', 'Armenia']
E1699 = [c for c in E1683 if c not in ('Hungary', 'Croatia')]
E1830 = [c for c in E1699 if c not in ('Greece', 'Algeria', 'Republic of Serbia', 'Moldova', 'Georgia', 'Armenia', 'Romania')]
E1914 = ['Turkey', 'Syria', 'Lebanon', 'Israel', 'Palestine', 'Jordan', 'Iraq', 'HEJAZ']
def emp(group, col='red', at=None):
    return [(c, col, at) if at is not None else (c, col) for c in group]

def MAP(view, fill=(), items=(), cap=(), **kw): return dict(view=view, fill=list(fill), items=list(items), cap=list(cap), **kw)
def ST(items=(), cap=(), **kw): return dict(bg='studio', items=list(items), cap=list(cap), **kw)
def SC(items=(), cap=(), sky='day', ground='sand', **kw):
    kw.pop('bg', None)
    return dict(bg='scene', sky=kw.pop('sky', sky), ground=ground, items=list(items), cap=list(cap), **kw)
def CAP(text, at, **o): return (text, None, at, o) if o else (text, None, at)
def BIG(small, big, at, **o): return (small, big, at, dict({'x': 0.64}, **o))
def fig(kind, x, at=None, id=None, h=380, y=0.88, **kw): return prop('fig-' + kind, x, y, at, id, h=h, **kw)
def badges(specs, y=0.5, x0=0.46, dx=0.15, s=100):
    return [badge(ic, S(x0 + i * dx, y), at, lbl, f'bg_{lbl[:6]}_{i}', s=s) for i, (ic, at, lbl) in enumerate(specs)]
def fires(xs, at, y=0.8, size=1.1):
    return [dict(k='fire', at_place=S(x, y), at=(at, 0.25 * i) if isinstance(at, str) else at, id=f'fi{x}', size=size, n=4) for i, x in enumerate(xs)]
NIGHT = dict(sky='night', clouds=0)
J = lambda x, at=None, id=None, h=300, **kw: fig('janissary', x, at, id, h, **kw)

P = [
    # ---------------- Part 1 end: the dream
    ('Later Ottoman storytellers said', SC([*camp(0.0), fig('colonist', 0.42, 0.0, 'osman2', h=430), prop('tree', 0.5, 0.86, 'tree', 'dt', h=420)], [CAP('the dream of Osman', 'dream')], **NIGHT)),
    ('The holy man woke up', ST([fig('monk', 0.52, 0.0, 'holy', h=420, say='Congratulations!', ss=40), fig('colonist', 0.76, 0.0, 'os3', h=420)], [CAP('also, you can marry my daughter', 'marry', x=0.64)])),
    ('Historians are pretty sure', ST([badge('question', S(0.55, 0.5), 'later', 'written much later', 'q15', s=100), badge('crown', S(0.78, 0.5), 'chosen', 'chosen to rule the world', 'c15', s=100)])),
    ('Osman spent his life raiding', MAP('west_anatolia', emp(['OSMAN']) + [('BYZ_COAST', 'purple')], [pin('Sogut', None, 'OSMAN', 'os', spaced=True),
        arrow(['Sogut', (40.4, 29.3)], 'raiding', ('raiding', 1.2), id='rd1', w=18), arrow(['Sogut', (40.6, 30.6)], 'forts', ('forts', 1.0), id='rd2', w=18)],
        [BIG(None, 'c. 1324', '1324', color='yellow', x=0.5)])),
    ('His son Orhan was the one', ST([fig('sultan', 0.64, 0.0, 'orhan', h=460, say='Orhan', ss=44)], [CAP('the one who made it real', 'real', x=0.64)])),
    # ---------------- Part 2: Bursa, Gallipoli
    ('In 1326, after a long siege', MAP('west_anatolia', emp(EARLY) + [('BYZ_COAST', 'purple')], [pin('Bursa', 'Bursa', 'BURSA', 'bu', spaced=True), ring('Bursa', 'captured')],
        [BIG(None, '1326', '1326', color='yellow', x=0.5), CAP('the first real capital', 'capital')])),
    ('And Orhan did something clever.', SC([prop('house', 0.3, 0.86, 0.0, 'bh1', h=200), prop('dome', 0.62, 0.86, 0.0, 'church', h=330), fig('priest', 0.45, 'Christians', 'pr19', h=330), fig('merchant', 0.8, 'trades', 'mc19', h=330)],
        [CAP('keep your churches, pay a tax', 'tax')])),
    ('This would become the Ottoman formula.', ST(badges([('burst', 'Conquer', 'conquer'), ('people', 'people', 'keep them working'), ('gold', 'taxpayers', 'taxpayers')]), [CAP('the Ottoman formula', 'formula', x=0.64)])),
    ('Then came the lucky break.', MAP('marmara', emp(EARLY) + [('BYZ_COAST', 'purple')], [pin('Gallipoli', 'Gallipoli', 'GALLIPOLI', 'ga', spaced=True), label('DARDANELLES', (40.0, 26.9), 'Dardanelles', 'dl', s=36, spaced=True)],
        [BIG(None, '1354', '1354', color='yellow', x=0.5)], shake=[('earthquake', 2.5, 18)])),
    ("Orhan's son Süleyman Pasha", SC([prop('wall', 0.5, 0.86, 0.0, 'gw', h=320, kw={'length': 3, 'damaged': True}), J(0.3, 'walked', 'sp1', h=320), J(0.4, ('walked', 0.3), 'sp2', h=320)])),
    ('Byzantine messenger: Excuse me', SC([prop('wall', 0.5, 0.86, None, 'gw', h=320, kw={'length': 3, 'damaged': True}), J(0.3, None, 'sp1', h=320), J(0.4, None, 'sp2', h=320),
        fig('emperor', 0.72, 0.0, 'bm', h=320, say="That's our town!", ss=40)])),
    ('Ottoman soldier: God sent', SC([prop('wall', 0.5, 0.86, None, 'gw', h=320, kw={'length': 3, 'damaged': True}), J(0.3, 0.0, 'sp1b', h=320), fig('emperor', 0.72, None, 'bm', h=320),
        prop('fig-janissary', 0.4, 0.88, 0.1, 'sp3', h=320, say='God sent the earthquake.', ss=36)])),
    ('The Ottomans now had a foothold', MAP('balkans', emp(EARLY + ['THRACE']), [pin('Gallipoli', None, 'GALLIPOLI', 'ga', spaced=True), label('EUROPE', (43.0, 22.0), 'Europe', 'eu', s=52, spaced=True)],
        [CAP('a foothold in Europe', 'foothold')])),
    # ---------------- Part 3: Murad I, devsirme, Janissaries, Kosovo
    ("Orhan's son Murad the First", MAP('balkans', emp(E1389), [pin('Edirne', 'Edirne', 'EDIRNE', 'ed', spaced=True), badge('cart:fig-sultan', (43.8, 27.6), 'Murad', 'Murad I', 'mu', s=80, lead='Edirne'),
        arrow(['Gallipoli', 'Edirne', (42.5, 24.0)], 'Balkans', ('Balkans', 1.4), id='ba', w=22)], [CAP('raiders into an army', 'army')])),
    ('But Murad had a problem', ST([fig('king', 0.52, 0.0, 'nob1', h=380), fig('king', 0.66, 0.1, 'nob2', h=380), fig('sultan', 0.84, 0.2, 'mu2', h=420, say='Hmm...', ss=44)], [CAP('powerful nobles', 'nobles', x=0.64)])),
    ('So the Ottomans came up with', ST([badge('question', S(0.64, 0.46), 0.0, None, 'q28', s=110)], [CAP('one of the strangest systems in history', 'strangest', x=0.64)])),
    ('It was called the devşirme', SC([prop('hut', 0.25, 0.86, 0.0, 'vh1', h=220), prop('hut', 0.45, 0.85, 0.05, 'vh2', h=200), fig('villager', 0.6, 0.1, 'vb1', h=240), fig('villager', 0.68, 0.15, 'vb2', h=250),
        fig('merchant', 0.82, 'officials', 'off1', h=380)], [CAP('THE DEVSHIRME', 'devşirme'), BIG(None, 'ages 8-18', 'eight', color='yellow', x=0.5)])),
    ('It was brutal.', SC([prop('hut', 0.25, 0.86, None, 'vh1', h=220), fig('villager', 0.5, 0.0, 'mum', h=360, say='No!', ss=48), fig('villager', 0.62, 0.0, 'vb3', h=240)], [CAP('families lost their sons', 'Families')])),
    ('But here is what is strange.', ST([badge('cart:fig-villager', S(0.5, 0.5), 0.0, 'a village boy', 'vb4', s=110), badge('crown', S(0.8, 0.5), 'elite', 'the elite', 'el', s=110)], [CAP('not ordinary slaves', 'ordinary', x=0.64)])),
    ('The strongest became the Janissaries', SC([J(0.2 + i * 0.12, ('Janissaries', 0.2 * i), f'jn{i}', h=340) for i in range(6)], [CAP('THE JANISSARIES', 'Janissaries'), CAP('the first standing army since Rome', 'standing')])),
    ('The smartest boys went to', ST([photo('janissary', 'A Janissary - Rålamb costume book, 1657', 0.05, x=0.66, h=520)], [CAP('the palace school', 'palace', x=0.64)])),
    ('Think about that. A shepherd boy', ST([badge('sheep', S(0.5, 0.5), 'shepherd', 'a shepherd boy', 'shb', s=110), badge('question', S(0.66, 0.5), 'running', None, 'qq', s=60),
        badge('cart:fig-sultan', S(0.82, 0.5), 'largest', 'grand vizier', 'gv', s=110)])),
    ('This is the Ottoman superpower in action.', ST([badge('cart:fig-villager', S(0.5, 0.5), 0.0, 'enemies', 'en', s=110), badge('cart:fig-janissary', S(0.8, 0.5), 0.3, 'loyal servants', 'ls', s=110)],
        [CAP('the superpower in action', 'superpower', x=0.64)])),
    ("In 1389, Murad's army met", MAP('kosovo', emp(E1389), [pin('Kosovo', 0.0, 'KOSOVO', 'ko', spaced=True), badge('burst', (43.6, 21.2), 'bloody', None, 'kb', s=70),
        badge('cart:fig-sultan', (41.6, 23.8), 'killed', 'Murad killed', 'mk', s=70, x=True)], [BIG(None, '1389', '1389', color='yellow', x=0.5)])),
    # ---------------- Part 4: Bayezid and Timur
    ("Murad's son Bayezid took the throne", ST([fig('sultan', 0.52, 0.0, 'bay', h=420, say='Bayezid', ss=44), badge('cart:fig-sultan', S(0.8, 0.5), 'brother', 'his brother Yakub', 'yak', s=100, x=True)],
        [CAP('a terrible precedent', 'precedent', x=0.64)])),
    ('Remember that. It is going to come back.', ST([badge('cart:fig-sultan', S(0.8, 0.5), None, 'his brother Yakub', 'yak', s=100, x=True)], [CAP('remember that...', 'Remember', x=0.64)])),
    ('Bayezid was nicknamed Yıldırım', MAP('balkans', emp(E1389 + ['Republic of Serbia']), [badge('burst', (41.4, 21.8), 'Thunderbolt', 'the Thunderbolt', 'tb', s=70),
        pin('Nicopolis', '1396', 'NICOPOLIS', 'ni', spaced=True), arrow([(48.0, 17.0), (46.0, 21.0), 'Nicopolis'], 'crusader', ('crusader', 1.4), color='blue', id='cru', w=22)],
        [BIG(None, '1396', '1396', color='yellow', x=0.5)])),
    ('Europe was terrified.', MAP('marmara', emp(E1389), [pin('Istanbul', 'Constantinople', 'CONSTANTINOPLE', 'cp', spaced=True), ring('Istanbul', 'besieging')], [CAP('he seemed unstoppable', 'unstoppable')])),
    ('Then he made a mistake.', ST([badge('cart:fig-sultan', S(0.5, 0.5), 0.0, 'Bayezid', 'by2', s=110), badge('question', S(0.8, 0.5), 'scarier', 'someone scarier', 'sc', s=110)])),
    ('His name was Timur', MAP('east', emp(E1389 + ['ANAT_C']) + [('TIMUR', 'purple', 'Timur')], [badge('horseman', (37.0, 52.0), 'Timur', 'Timur', 'ti', s=90),
        pin('Baghdad', 'Baghdad', 'BAGHDAD', 'bg', spaced=True)])),
    ('Bayezid: You are a dog', ST([fig('sultan', 0.52, 0.0, 'by3', h=420, say='You are a dog!', ss=40), prop('horseman', 0.82, 0.9, 0.0, 'ti2', h=360)])),
    ('Timur: Interesting.', ST([fig('sultan', 0.52, None, 'by3', h=420), prop('horseman', 0.82, 0.9, None, 'ti2', h=360, say='Interesting.', ss=40)],
        [CAP('a very, very large number of dogs', 'large', x=0.64)])),
    ('In 1402, at the Battle of Ankara', MAP('anatolia_wide', emp(E1389 + ['ANAT_C']), [pin('Ankara', 0.0, 'ANKARA', 'an', spaced=True),
        arrow([(39.0, 42.0), (39.6, 37.0), 'Ankara'], '1402', ('1402', 1.2), color='purple', id='ta', w=28), badge('cart:cage', (41.2, 31.0), 'captured', 'captured', 'cpt', s=70)],
        [BIG(None, '1402', '1402', color='yellow', x=0.5)])),
    ('And the empire fell apart.', MAP('anatolia_wide', emp(E1389 + ['ANAT_C'], 'red', None), [prop('stamp', 0.5, 0.6, 'apart', 'fa', h=150)], unfill=[(c, 'apart') for c in E1389 + ['ANAT_C']])),
    # ---------------- Part 5: Interregnum, Varna
    ("With their father gone, Bayezid's sons", ST([fig('sultan', 0.46 + i * 0.12, 0.2 * i, f'bro{i}', h=380) for i in range(4)], [BIG(None, '11 years', 'eleven', x=0.64, color='red')])),
    ('Historians call it the Ottoman Interregnum', ST([fig('sultan', 0.46 + i * 0.12, None, f'bro{i}', h=380) for i in range(4)], [CAP('THE INTERREGNUM', 'Interregnum', x=0.64), CAP('a family dinner that lasted a decade', 'dinner', x=0.64)])),
    ('The survivor was Mehmed the First.', ST([fig('sultan', 0.64, 0.0, 'm1', h=460, say='Mehmed I', ss=44)], [CAP('the survivor', 'survivor', x=0.64)])),
    ('Murad the Second was a strange sultan.', ST([fig('sultan', 0.52, 0.0, 'm2', h=420, say='Murad II', ss=40), fig('villager', 0.8, 'twelve-year-old', 'boy', h=280, say='Mehmed, 12', ss=40)],
        [CAP('he stepped down', 'stepped', x=0.64)])),
    ('Europe saw its chance.', MAP('balkans', emp(E1389 + ['Republic of Serbia']), [arrow([(47.0, 21.0), (45.0, 25.0), 'Varna'], 'marched', ('marched', 1.4), color='blue', id='va', w=24),
        badge('cart:fig-crusader', (46.8, 21.6), 'crusader', 'the crusaders', 'cr44', s=70)])),
    ('The boy sultan wrote to his father.', ST([fig('villager', 0.52, 0.0, 'boy2', h=300), badge('envelope', S(0.68, 0.4), 'letter', None, 'let', s=80), fig('sultan', 0.84, 0.0, 'm2b', h=420)],
        [CAP('"if I am the sultan, I order you to come"', 'order', x=0.64)])),
    ('Murad came back.', MAP('balkans', emp(E1389 + ['Republic of Serbia']), [pin('Varna', 0.0, 'VARNA', 'vr', spaced=True), badge('burst', (43.9, 27.5), 'crushed', None, 'vb', s=70)],
        [BIG(None, '1444', '1444', color='yellow', x=0.5)])),
    ('That twelve-year-old boy would grow up', ST([fig('villager', 0.6, 0.0, 'boy3', h=300), badge('crown', S(0.8, 0.4), 'famous', None, 'fr', s=90)], [CAP('one of the most famous rulers in history', 'famous', x=0.64)])),
    ('But the Ottomans had learned a terrible lesson', ST([fig('sultan', 0.5 + i * 0.09, 0.15 * i, f'sons{i}', h=340) for i in range(5)], [CAP('a dead sultan with five living sons...', 'five', x=0.64)])),
    ('Because the next sultan was going to turn', ST([prop('stamp', 0.64, 0.6, 'law', 'law', h=160, kw={'text': 'LAW'})])),
    # ---------------- Part 6: Mehmed II and Constantinople
    ('In 1451, a nineteen-year-old named Mehmed', ST([photo('mehmed_bellini', 'Mehmed II - Gentile Bellini, 1480', 0.05, x=0.66, h=540)], [BIG(None, '19', 'nineteen', x=0.42, color='red')])),
    ('And he had one goal. Constantinople.', MAP('marmara', emp(E1451), [pin('Istanbul', 'Constantinople', 'CONSTANTINOPLE', 'cp6', spaced=True), ring('Istanbul', 'goal')])),
    ('For eleven hundred years, the city had been', MAP('marmara', emp(E1451), [pin('Istanbul', None, 'CONSTANTINOPLE', 'cp6', spaced=True)], [CAP('like a hole in a doughnut', 'doughnut')])),
    ('In the spring of 1453, Mehmed arrived', SC([prop('cannon', 0.4, 0.95, 'cannons', 'can', h=230), *[J(0.7 + i * 0.08, ('eighty', 0.2 * i), f'j6{i}', h=280) for i in range(3)]],
        [BIG(None, '80,000 men', 'eighty', color='yellow', x=0.5)])),
    ('For fifty-three days, the cannons smashed', SC([prop('wall', 0.5, 0.86, 0.0, 'cw', h=380, kw={'length': 4, 'damaged': True}), prop('galley', 0.5, 0.97, 'warships', 'og', h=200, move_to=0.8, to='harbor')],
        [CAP('70 warships dragged overland', 'seventy')], shake=[(0.4, 0.8, 12), (2.2, 0.8, 12)])),
    ('On the morning of May 29th, 1453', SC([prop('wall', 0.5, 0.86, None, 'cw', h=380, kw={'length': 4, 'damaged': True}), prop('banner', 0.5, 0.42, 'broke', 'obn', h=220)],
        [BIG(None, 'May 29, 1453', 'May', color='yellow', x=0.5)])),
    ('He was twenty-one years old.', ST([photo('mehmed_bellini', 'Mehmed II - Gentile Bellini, 1480', 0.0, x=0.7, h=500)], [BIG(None, '21', 'twenty-one', x=0.42, color='red', size=220)])),
    ('From now on, he was known as Fatih', MAP('marmara', emp(E1451), [pin('Istanbul', 0.0, 'ISTANBUL', 'ist', spaced=True)], [CAP('FATIH, THE CONQUEROR', 'Fatih')])),
    ('But Mehmed did something else', SC([prop('dome', 0.5, 0.82, 0.0, 'hs', h=360), fig('priest', 0.2, 'Greeks', 'g1', h=320), fig('merchant', 0.32, 'Armenians', 'g2', h=320), fig('monk', 0.8, 'Jews', 'g3', h=320)],
        [CAP('outsiders became insiders, again', 'again')])),
    ('And then he wrote a law.', ST([prop('stamp', 0.64, 0.6, 'law', 'law2', h=160, kw={'text': 'LAW'})])),
    ('In his law code, Mehmed declared', ST([fig('sultan', 0.5 + i * 0.1, 0.0, f'br{i}', h=340) for i in range(4)], [CAP('"for the order of the world"', 'order', x=0.64)])),
    ("Read that again. The sultan's sons", ST([fig('sultan', 0.5, None, 'br0', h=340)] + [badge('cart:fig-sultan', S(0.6 + i * 0.1, 0.62), 'die', None, f'bx{i}', s=60, x=True) for i in range(3)])),
    ('It sounds monstrous, and it was.', ST([badge('cart:fig-sultan', S(0.5, 0.5), 0.0, 'a few princes', 'fp', s=100), badge('burst', S(0.8, 0.5), 'civil', 'or a civil war', 'cvw', s=100)], [CAP('the Ottoman logic', 'logic', x=0.64)])),
    # ---------------- Part 7: Selim the Grim
    ("Mehmed's grandson Selim the First", ST([fig('sultan', 0.64, 0.0, 'sel', h=460, say='Selim I', ss=44)], [CAP('YAVUZ, THE GRIM', 'Grim', x=0.64)])),
    ('There was a joke among his officials.', ST([fig('sultan', 0.5, None, 'sel', h=440), fig('merchant', 0.78, 0.0, 'viz', h=400, say='May you become his vizier!', ss=34)])),
    ('But Selim reigned for only eight years', MAP('empire', emp(E1451, 'red', 0.0) + emp(['Syria', 'Egypt', 'Israel', 'Palestine', 'Jordan', 'Lebanon', 'HEJAZ'], 'orange', 'doubled'),
        [], [BIG(None, '8 years', 'eight', color='yellow', x=0.5)])),
    ('In 1514, at the Battle of Chaldiran', MAP('east', emp(E1451 + ['Turkey']) + [('Iran', 'purple', 'Safavid')], [pin('Chaldiran', 0.1, 'CHALDIRAN', 'chd', spaced=True),
        arrow([(39.4, 37.0), 'Chaldiran'], 'crushed', ('crushed', 1.2), id='chda', w=24)], [BIG(None, '1514', '1514', color='yellow', x=0.5)])),
    ('Then Selim turned south', MAP('arab', emp(E1451 + ['Turkey']) + emp(['Egypt', 'Syria', 'Lebanon', 'Israel', 'Palestine', 'Jordan'], 'brown', 0.0),
        [arrow([(37.5, 36.0), 'Damascus', (31.0, 33.5), 'Cairo'], 'south', ('Cairo', 0.4), id='mam', w=26), pin('Cairo', 'Cairo', 'CAIRO', 'ca', spaced=True)],
        [CAP('the Mamluk Sultanate', 'Mamluk')])),
    ('Suddenly, the Ottomans ruled Syria', MAP('arab', emp(E1520), [pin('Jerusalem', 'Jerusalem', 'JERUSALEM', 'je', spaced=True), pin('Mecca', 'Mecca', 'MECCA', 'mc', spaced=True), pin('Medina', 'Medina', 'MEDINA', 'md', spaced=True)])),
    ('A family of frontier raiders now controlled', MAP('empire', emp(E1520), [badge('wheat', (27.0, 31.0), 'grain', 'the grain of the Nile', 'nile', s=70), badge('gold', (25.0, 43.0), 'spice', 'the spice routes', 'sp', s=70)])),
    ('And the next sultan was about to take', MAP('empire', emp(E1520), [], [CAP('to its peak', 'peak')])),
    # ---------------- Part 8: Suleiman
    ("In 1520, Selim's only surviving son", ST([photo('suleiman', 'Süleyman the Magnificent - 16th-century portrait', 0.05, x=0.66, h=540)], [CAP('THE MAGNIFICENT', 'Magnificent', x=0.42), CAP('KANUNI, THE LAWGIVER', 'Lawgiver', x=0.42)])),
    ('Within six years, he took Belgrade', MAP('hungary', emp(E1520 + ['Hungary'], 'red', None), [pin('Belgrade', 'Belgrade', 'BELGRADE', 'bl', spaced=True), pin('Mohacs', 'Mohács', 'MOHÁCS', 'mo', spaced=True),
        photo('mohacs', 'The Battle of Mohács, 1526', 'Mohács', x=0.32, y=0.4, h=380)], [BIG(None, '1526', '1526', color='yellow', x=0.72)])),
    ('In 1529, Süleyman reached the walls of Vienna', MAP('vienna', emp(E1566), [pin('Vienna', 0.0, 'VIENNA', 'vi', spaced=True), ring('Vienna', 'walls')], [BIG(None, '1529', '1529', color='yellow', x=0.5)])),
    ('And here, for the first time, the Ottoman machine', MAP('europe_wide', emp(E1566), [arrow(['Istanbul', 'Edirne', 'Belgrade', 'Vienna'], 'marched', ('marched', 1.8), color='white', id='vr', w=14),
        label('1,000+ KM', (45.0, 24.0), 'thousand', 'km', s=44, color=(255, 214, 64))], [CAP('the machine hit its limit', 'limit')], rain=True)),
    ('But on the sea, the Ottomans were rising.', MAP('med', emp(E1566), [badge('cart:galley', (37.0, 18.0), 'sea', 'the Ottoman navy', 'nv', s=80)])),
    ("Barbarossa's story is wild", MAP('med', emp(E1566), [pin('Lesbos', 'Lesbos', 'LESBOS', 'le', spaced=True), badge('cart:fig-barbarian', (36.8, 22.0), 'Barbarossa', 'Red Beard', 'rb', s=80, lead='Lesbos')])),
    ('He captured the city of Algiers.', MAP('west_med', emp(E1566), [pin('Algiers', 'Algiers', 'ALGIERS', 'alg', spaced=True), badge('crown', (40.0, 4.0), 'title', 'pirate to governor', 'pg2', s=70)])),
    ('Once again, the Ottomans took an outsider', ST([badge('cart:fig-barbarian', S(0.5, 0.5), 0.0, 'a pirate', 'pi', s=110), badge('cart:fig-sultan', S(0.8, 0.5), 0.3, 'grand admiral', 'ga2', s=110)])),
    ('And Süleyman made an even more surprising friend.', MAP('europe_wide', emp(E1566), [pin('Paris', 'France', 'FRANCE', 'fr', spaced=True), badge('cart:fig-king', (50.5, -1.0), 'Francis', 'Francis I', 'fra', s=80)],
        [BIG(None, '1525', '1525', color='yellow', x=0.5)])),
    ('A Catholic king asking a Muslim sultan', ST([badge('cart:fig-king', S(0.5, 0.5), 0.0, 'Catholic king', 'ck', s=100), badge('cart:fig-sultan', S(0.8, 0.5), 0.2, 'Muslim sultan', 'ms', s=100)],
        [CAP('Europe was scandalized', 'scandalized', x=0.64)])),
    ('But it worked. France and the Ottomans', MAP('west_med', emp(E1566), [pin('Toulon', 'Toulon', 'TOULON', 'tl', spaced=True),
        move('cart:galley', [(38.0, 12.0), (41.0, 8.0), 'Toulon'], 'fleet', 'Toulon', s=60, id='tfl')], [BIG(None, '1543', '1543', color='yellow', x=0.5)])),
    ('Toulon resident: Where are we supposed to go?', SC([prop('house', 0.3, 0.86, 0.0, 'th1', h=220), fig('villager', 0.5, 0.0, 'tr', h=360, say='Where do we go?', ss=40)])),
    ('French official: Anywhere.', SC([prop('house', 0.3, 0.86, None, 'th1', h=220), fig('villager', 0.5, None, 'tr', h=360), fig('king', 0.68, 0.0, 'fo', h=380, say='Anywhere!', ss=44), J(0.85, 0.2, 'gj', h=340)])),
    ('Religion mattered. But in the end', MAP('med', emp(E1566), [pin('Preveza', 'Preveza', 'PREVEZA', 'pv', spaced=True), badge('burst', (39.8, 19.0), 'defeated', None, 'pvb', s=70)],
        [CAP('power mattered more', 'power'), BIG(None, '1538', '1538', color='yellow', x=0.5)])),
    ('Under Süleyman, the empire reached its golden age.', SC([prop('dome', 0.5, 0.82, 0.0, 'sul', h=420), prop('minaret', 0.22, 0.82, 0.1, 'mn1', h=460), prop('minaret', 0.78, 0.82, 0.15, 'mn2', h=460)],
        [CAP('the Süleymaniye Mosque - Mimar Sinan', 'Süleymaniye')], sky='gold')),
    ("Süleyman rewrote the empire's laws", ST([badge('envelope', S(0.5, 0.5), 'laws', 'new laws', 'lw', s=100), badge('people', S(0.8, 0.5), 'biggest', 'half a million people', 'hm', s=100)],
        [CAP('the biggest city in Europe', 'biggest', x=0.64)])),
    ('And then there was Hürrem.', ST([fig('oracle', 0.64, 0.0, 'hur', h=440, say='Hürrem', ss=44)], [CAP('Roxelana', 'Roxelana', x=0.64)])),
    ('Hürrem became one of the most powerful', ST([fig('oracle', 0.5, None, 'hur', h=420), badge('envelope', S(0.72, 0.36), 'letters', 'letters to kings', 'hl', s=80), badge('cart:dome', S(0.88, 0.36), 'mosques', 'mosques', 'hmq', s=80)])),
    ('But palace politics were deadly.', ST([fig('sultan', 0.64, 0.0, 'mus', h=440, say='Prince Mustafa', ss=40)], [BIG(None, '1553', '1553', color='red', x=0.42)])),
    ("And even Süleyman's luck had limits.", MAP('med', emp(E1566), [pin('Malta', 'Malta', 'MALTA', 'ml', spaced=True), ring('Malta', 'besieged')], [BIG(None, '1565', '1565', color='yellow', x=0.5)])),
    ('A year later, Süleyman, now over seventy', MAP('hungary', emp(E1566), [pin('Szigetvar', 'Szigetvár', 'SZIGETVÁR', 'sz', spaced=True), prop('tent', 0.5, 0.65, 'tent', 'tt', h=160)],
        [BIG(None, '1566', '1566', color='yellow', x=0.5)])),
    ('And then his grand vizier did something extraordinary.', SC([prop('tent', 0.55, 0.9, 0.0, 'tt2', h=320), fig('merchant', 0.3, 0.0, 'gv1', h=380, say='Shh...', ss=48)], [CAP('he hid it', 'hid')])),
    ('Grand vizier: The sultan is resting.', SC([prop('tent', 0.55, 0.9, None, 'tt2', h=320), fig('merchant', 0.3, None, 'gv1', h=380, say='He is resting.', ss=40)])),
    ('Soldier: He has been resting', SC([prop('tent', 0.55, 0.9, None, 'tt2', h=320), fig('merchant', 0.3, None, 'gv1', h=380), J(0.78, 0.0, 'sold', h=360)], [CAP('"a very long time"', 'long')])),
    ('Grand vizier: He is resting magnificently.', SC([prop('tent', 0.55, 0.9, None, 'tt2', h=320), fig('merchant', 0.3, None, 'gv1', h=380, say='...magnificently.', ss=40), J(0.78, None, 'sold', h=360)])),
    ('Only when his son Selim the Second', SC([prop('tent', 0.55, 0.9, None, 'tt2', h=320)], [CAP('he died the way he had lived, at war', 'war')], sky='dusk', clouds=0)),
    ("Again and again in this story, the empire's greatest strength", ST([badge('crown', S(0.5, 0.5), 'strength', 'loyalty to one man', 'l1', s=100), badge('skull', S(0.8, 0.5), 'deadliest', 'its deadliest weakness', 'l2', s=100)])),
    # ---------------- Part 9: how it worked, daily life, harem
    ('Before we watch the long decline', ST([badge('question', S(0.64, 0.46), 0.0, None, 'q105', s=110)], [CAP('how did it actually work?', 'worked', x=0.64)])),
    ('At the top was the sultan.', ST([fig('sultan', 0.62, 0.0, 'top', h=420), fig('merchant', 0.46, 'grand', 'gv2', h=340), fig('janissary', 0.8, 'slaves', 'sl2', h=340)], [CAP('the sultan, the grand vizier, the slaves of the sultan', 'grand', x=0.64)])),
    ('Then there was the millet system.', ST([fig('priest', 0.48, 0.0, 'ml1', h=380, say='Orthodox', ss=36), fig('merchant', 0.64, 0.2, 'ml2', h=380, say='Armenians', ss=36), fig('monk', 0.8, 0.4, 'ml3', h=380, say='Jews', ss=36)],
        [CAP('THE MILLET SYSTEM', 'millet', x=0.64)])),
    ('They had to pay extra taxes', ST([badge('gold', S(0.5, 0.5), 'taxes', 'extra taxes', 'xt', s=100), badge('people', S(0.8, 0.5), 'tolerant', 'remarkably tolerant', 'rt', s=100)])),
    ('When Spain expelled its Jews in 1492', MAP('west_med', emp(E1520), [pin('Madrid', 'Spain', 'SPAIN', 'spn', spaced=True), pin('Thessaloniki', 'welcomed', 'THESSALONIKI', 'th', spaced=True),
        arrow(['Madrid', (38.0, 8.0), (38.5, 18.0), 'Thessaloniki'], 'welcomed', ('welcomed', 1.6), color='blue', id='jw', w=18)], [BIG(None, '1492', '1492', color='yellow', x=0.5)])),
    ('This is the superpower again.', ST([badge('people', S(0.64, 0.46), 0.0, None, 'everyone', s=110)], [CAP('it made everyone useful', 'useful', x=0.64)])),
    ('What was it like to actually live', SC([prop('dome', 0.5, 0.82, 0.0, 'ist1', h=380), prop('minaret', 0.25, 0.82, 0.0, 'm3', h=420), prop('house', 0.8, 0.84, 0.0, 'h4', h=200)], [CAP('life in Ottoman Istanbul', 'Istanbul')])),
    ('Picture the Grand Bazaar', ST(badges([('gold', 'Spices', 'spices'), ('diamond', 'silk', 'silk'), ('oil', 'coffee', 'coffee')]), [CAP('THE GRAND BAZAAR', 'Bazaar', x=0.64)])),
    ('Picture the hammams', ST(badges([('drop', 'hammams', 'the hammams'), ('bowl', 'kitchens', 'palace kitchens')], x0=0.52, dx=0.24), [CAP('cooking for thousands every day', 'thousands', x=0.64)])),
    ('One of the best windows into this world', ST([fig('merchant', 0.6, 0.0, 'ev', h=440, say='Evliya Çelebi', ss=40), badge('envelope', S(0.82, 0.4), 'ten-volume', '10 volumes', 'ev10', s=80)],
        [BIG(None, '40 years', 'forty', x=0.64, color='red')])),
    ('He makes the empire sound like one giant', SC([prop('house', 0.2, 0.84, 0.0, 'bz1', h=200), prop('tent', 0.4, 0.92, 0.0, 'bz2', h=150), fig('merchant', 0.55, 0.1, 'bz3', h=300), fig('villager', 0.7, 0.2, 'bz4', h=300)],
        [CAP('one giant, noisy, colorful world', 'colorful')])),
    ('And then there was the palace.', SC([prop('dome', 0.5, 0.82, 0.0, 'tp', h=380), prop('wall', 0.5, 0.95, 0.0, 'tpw', h=150, kw={'length': 6})], [CAP('TOPKAPI PALACE', 'Topkapı'), CAP('the brain of the empire', 'brain')])),
    ('The most powerful woman in the empire was usually', ST([fig('oracle', 0.64, 0.0, 'val', h=440, say='Valide Sultan', ss=40)], [CAP("the sultan's mother", 'mother', x=0.64), CAP('THE SULTANATE OF WOMEN', 'Sultanate', x=0.64)])),
    ('The most famous of them was Kösem Sultan.', ST([fig('oracle', 0.6, 0.0, 'kos', h=440, say='Kösem Sultan', ss=40), badge('gold', S(0.82, 0.4), 'fortunes', None, 'kf', s=80)])),
    ('She held power under four sultans', ST([fig('oracle', 0.5, None, 'kos', h=420)] + [badge('cart:fig-sultan', S(0.64 + i * 0.09, 0.4), 0.2 * i, None, f'ks{i}', s=55) for i in range(4)],
        [BIG(None, '1651', '1651', color='red', x=0.64)])),
    # ---------------- Part 10: the cage
    ('Now remember the law of fratricide.', ST([prop('stamp', 0.64, 0.6, 0.0, 'law3', h=160, kw={'text': 'LAW'})])),
    ('In 1595, when Mehmed the Third became sultan', ST([fig('sultan', 0.5, 0.0, 'm3s', h=420)] + [badge('cart:fig-sultan', S(0.64 + (i % 5) * 0.07, 0.36 + (i // 5) * 0.18), ('nineteen', 0.08 * i), None, f'x19{i}', s=40, x=True) for i in range(10)],
        [BIG(None, '19 brothers', 'nineteen', x=0.64, color='red')])),
    ('So, in the early 1600s, the Ottomans tried', ST([prop('cage', 0.66, 0.86, 'lock', 'cg', h=470)], [CAP('lock them up instead', 'lock', x=0.64)])),
    ('The princes were kept in a part of the harem', ST([fig('sultan', 0.66, 0.0, 'cgp', h=300, y=0.82), prop('cage', 0.66, 0.86, 0.0, 'cg2', h=470)], [CAP('THE KAFES - THE CAGE', 'kafes', x=0.64)])),
    ('Then, when the sultan died, one of these men', ST([fig('sultan', 0.66, None, 'cgp', h=300, y=0.82), prop('cage', 0.66, 0.86, None, 'cg2', h=470, off='pulled')], [CAP('suddenly placed on the throne', 'throne', x=0.64)])),
    ('Palace official: Congratulations', ST([fig('merchant', 0.52, 0.0, 'po', h=400, say='You rule the world!', ss=38), fig('sultan', 0.78, 0.0, 'ns', h=400)])),
    ('New sultan: I have not been outside', ST([fig('merchant', 0.52, None, 'po', h=400), fig('sultan', 0.78, None, 'ns', h=400, say='...22 years.', ss=40)], [CAP('"I have not been outside in 22 years"', 'outside', x=0.64)])),
    ('Some of them were fine. Some were clearly broken.', ST([fig('sultan', 0.64, 0.0, 'ibr', h=440, say='Ibrahim the Mad', ss=40)])),
    ('His older brother, Murad the Fourth', SC([fig('sultan', 0.6, 0.0, 'm4', h=400), badge('oil', S(0.3, 0.3), 'coffee', 'coffee', 'cof', s=70, x=True), badge('flame', S(0.45, 0.3), 'tobacco', 'tobacco', 'tob', s=70, x=True)], **NIGHT)),
    ('Imagine being caught with a cup of coffee', SC([fig('sultan', 0.6, None, 'm4', h=400), fig('villager', 0.35, 0.0, 'cc', h=340, say='...oops.', ss=44)], **NIGHT)),
    ('Murad the Fourth also led his armies', MAP('east', emp(E1566), [pin('Baghdad', 'Baghdad', 'BAGHDAD', 'bgd', spaced=True)], [BIG(None, '1638', '1638', color='yellow', x=0.5)])),
    ('The old system had produced experienced', ST([badge('burst', S(0.5, 0.5), 0.0, 'battle-hardened princes', 'oldp', s=100), badge('cart:cage', S(0.8, 0.5), 'new', 'princes from the cage', 'newp', s=100)])),
    # ---------------- Part 11: Lepanto, decline, Vienna 1683, Koprulus
    ('The decline did not happen in one day.', MAP('empire', emp(E1683), [], [CAP('a slow decline', 'decline')])),
    ('In 1571, a Christian alliance called the Holy League', ST([photo('lepanto', 'The Battle of Lepanto, 1571', 0.05, x=0.64, h=480)], [BIG(None, '1571', '1571', color='yellow', x=0.42)])),
    ('The Ottoman grand vizier Sokollu Mehmed Pasha', ST([fig('merchant', 0.6, 0.0, 'sok', h=440, say='Sokollu', ss=44)], [CAP('"you only shaved our beard"', 'beard', x=0.64)])),
    ('And he was right. Within a year', SC([*[prop('galley', 0.2 + i * 0.2, 0.94, ('rebuilt', 0.2 * i), f'rf{i}', h=170, kw={'emblem': 'crescent'}) for i in range(4)]], [BIG(None, '1 year', 'year', color='yellow', x=0.5)], ground='sea', horizon=0.6)),
    ('But something was slowly changing.', MAP('europe_wide', emp(E1683), [arrow([(20.0, -40.0), (36.0, -10.0), 'Madrid'], 'silver', ('silver', 1.2), color='yellow', id='sil', w=18),
        badge('gold', (38.0, -10.0), 'silver', 'American silver', 'ams', s=60)], [CAP('Europe was getting richer', 'richer')])),
    ('And the Janissaries, once the most disciplined', ST([J(0.5 + i * 0.12, 0.2 * i, f'jr{i}', h=360) for i in range(3)] + [badge('burst', S(0.62, 0.3), 'rioted', 'riots', 'jri', s=70)],
        [CAP('a powerful club that overthrew sultans', 'club', x=0.64)])),
    ('Then came 1683.', MAP('vienna', emp(E1683), [pin('Vienna', 0.0, 'VIENNA', 'vi83', spaced=True)], [BIG(None, '1683', '1683', color='yellow', x=0.5, size=200)])),
    ('A grand vizier named Kara Mustafa Pasha', MAP('vienna', emp(E1683), [pin('Vienna', None, 'VIENNA', 'vi83', spaced=True), arrow([(45.0, 20.4), (46.6, 18.4), 'Vienna'], 'marched', ('marched', 1.3), id='km', w=28),
        ring('Vienna', 'besieged'), badge('cart:fig-merchant', (46.0, 21.5), 'Kara', 'Kara Mustafa', 'kmu', s=70)])),
    ('Then, on September 12th, 1683, a relief army', ST([photo('vienna', 'The Battle of Vienna, 1683', 0.05, x=0.64, h=480)], [CAP('the winged hussars', 'hussars', x=0.64)])),
    ('The Ottoman army collapsed.', MAP('vienna', emp(E1683), [arrow(['Vienna', (46.6, 18.4), 'Belgrade'], 'fled', ('fled', 1.2), color='white', id='kmf', w=20), pin('Belgrade', 'Belgrade', 'BELGRADE', 'blg', spaced=True)])),
    ('Sixteen years later, in 1699', MAP('hungary', emp(E1699) + [('Hungary', 'blue', 'Hungary')], [pin('Karlowitz', 'Karlowitz', 'KARLOWITZ', 'kw', spaced=True)], [BIG(None, '1699', '1699', color='yellow', x=0.5)])),
    ('The age of Ottoman expansion was over.', MAP('europe_wide', emp(E1699), [prop('stamp', 0.5, 0.6, 'over', 'ov', h=150, kw={'text': 'OVER'})])),
    ('But before that disaster, there was one last comeback', ST([fig('merchant', 0.64, 'old', 'kop', h=420, say='~80 years old', ss=40)])),
    ('In 1656, the empire was in chaos.', ST(badges([('burst', 'Rebellions', 'rebellions'), ('gold', 'unpaid', 'unpaid soldiers'), ('cart:galley', 'navy', 'blockaded navy')]) + [fig('merchant', 0.88, 'Köprülü', 'kop2', h=380)],
        [BIG(None, '1656', '1656', color='red', x=0.64)])),
    ('He had one condition.', ST([fig('merchant', 0.64, 0.0, 'kop3', h=440, say='Total power.', ss=44)])),
    ('And then he purged the system.', MAP('crete', emp(E1683, 'red', None) + [('CRETE_I', 'red', 'Crete')], [pin('Candia', 'Candia', 'CANDIA', 'cn', spaced=True)], [BIG(None, '1669', '1669', color='yellow', x=0.5)])),
    ('Twenty-one years. Some of the soldiers', ST([BIG and fig('janissary', 0.62, 0.0, 'oldj', h=420, say='Born during the siege.', ss=36)], [BIG(None, '21 years', 'Twenty-one', x=0.64, color='red')])),
    ('Under the Köprülüs, the empire reached', MAP('empire', emp(E1683), [], [CAP('the high point', 'high')])),
    # ---------------- Part 12: Tulip era, coffee
    ('Here is something most people do not know.', ST([badge('question', S(0.64, 0.46), 0.0, None, 'q150', s=110)], [BIG(None, '1700s', '1700s', x=0.64, color='yellow')])),
    ('From 1718 to 1730, there was a period', SC([*[prop('tree', 0.15 + i * 0.12, 0.88, ('Tulip', 0.1 * i), f'tl{i}', h=200) for i in range(7)]], [CAP('THE TULIP ERA', 'Tulip')], **NIGHT)),
    ('At least, that is how visitors at the time', SC([*[prop('tree', 0.15 + i * 0.12, 0.88, None, f'tl{i}', h=200) for i in range(7)], *[prop('candle', 0.25 + i * 0.2, 0.94, 0.1 * i, f'tc{i}', h=90) for i in range(4)]], **NIGHT)),
    ('The Ottomans also gave Europe one of its favorite', SC([prop('house', 0.45, 0.84, 0.0, 'cfh', h=260), fig('merchant', 0.25, 0.1, 'cf1', h=320), fig('villager', 0.7, 0.2, 'cf2', h=320, say='Coffee!', ss=44)],
        [CAP('COFFEE', 'Coffee')])),
    ('The first printing press for Turkish books', ST([badge('envelope', S(0.64, 0.46), 0.0, 'the first Turkish press', 'press', s=110)], [CAP('curious and open', 'curious', x=0.64)])),
    ('But the party ended in 1730', ST([J(0.55, 0.0, 'ph', h=420, say='Patrona Halil', ss=40), badge('burst', S(0.8, 0.4), 'rebellion', 'rebellion', 'rb30', s=80)], [BIG(None, '1730', '1730', x=0.64, color='red')])),
    # ---------------- Part 13: Russia, Napoleon, Janissaries destroyed
    ('Meanwhile, a new enemy was rising. Russia.', MAP('black_sea', emp(E1699) + [('Russia', 'green', 'Russia'), ('Ukraine', 'green', 'Russia')], [label('RUSSIA', (48.5, 37.0), 'Russia', 'ru', s=56, spaced=True)])),
    ('Actually, there were two. In 1798, a French general', MAP('egypt', emp(E1699), [pin('Cairo', 'Cairo', 'CAIRO', 'ca2', spaced=True), badge('cart:fig-king', (31.5, 27.0), 'Napoleon', 'Napoleon', 'nap', s=80),
        arrow([(34.5, 25.0), (31.3, 30.0), 'Cairo'], 'landed', ('landed', 1.3), color='blue', id='npa', w=22)], [BIG(None, '1798', '1798', color='yellow', x=0.5)])),
    ('It was a shock. A European army had walked', ST([badge('cart:fig-king', S(0.5, 0.5), 0.0, 'a European army', 'ea', s=100), badge('xmark', S(0.8, 0.5), 'stop', 'could not stop it alone', 'nst', s=90)])),
    ('Under Peter the Great and then Catherine the Great', MAP('black_sea', emp(E1699) + [('Russia', 'green'), ('Ukraine', 'green', 'south')], [arrow([(50.0, 36.0), (46.5, 34.5), 'Crimea'], 'south', ('south', 1.2), color='green', id='rus', w=26),
        pin('Crimea', 'Crimea', 'CRIMEA', 'cri', spaced=True)], [BIG(None, '1774', '1774', color='yellow', x=0.5)])),
    ('The Black Sea, once an Ottoman lake', MAP('black_sea', emp([c for c in E1699 if c not in ('Georgia',)]) + [('Russia', 'green'), ('Ukraine', 'green')], [label('BLACK SEA', (43.3, 34.0), 0.0, 'bs', s=48, spaced=True)], [CAP('shared with the bear', 'bear')])),
    ('Ottoman officials could see what was happening.', ST([fig('sultan', 0.52, 0.0, 's3', h=420, say='Selim III', ss=40), J(0.78, 'New', 'nj', h=380)], [CAP('THE NEW ORDER', 'New', x=0.64)])),
    ('The Janissaries hated it.', ST([J(0.5 + i * 0.12, 0.15 * i, f'jh{i}', h=360) for i in range(3)] + [badge('burst', S(0.62, 0.3), 'rebelled', None, 'jhb', s=80)], [BIG(None, '1807', '1807', x=0.64, color='red')])),
    ('His cousin, Mahmud the Second, waited', ST([fig('sultan', 0.64, 0.0, 'm2s', h=440, say='Mahmud II', ss=40), badge('hourglass', S(0.84, 0.36), 'waited', '20 years', 'wt', s=80)])),
    ('In 1826, he announced a new modern army again.', SC([prop('house', 0.4, 0.86, 0.0, 'bar', h=260, kw={'wide': 2.0}), *fires([0.3, 0.45, 0.6], 'shelled', y=0.62), prop('cannon', 0.82, 0.97, 0.0, 'mc', h=150)],
        [BIG(None, '1826', '1826', color='yellow', x=0.5)], shake=[('shelled', 2.0, 14)])),
    ('After nearly five hundred years, the most famous army', ST([badge('cart:fig-janissary', S(0.64, 0.46), 0.0, 'the Janissaries', 'jg', s=120, x=True)], [CAP('gone in a single day', 'single', x=0.64)])),
    # ---------------- Part 14: nationalism, Tanzimat, debt
    ('The 1800s were the century of nationalism.', MAP('balkans', emp(E1699), [badge('burst', (44.4, 21.0), 'nationalism', 'Serbs', 'nf1', s=60), badge('burst', (39.5, 22.5), 'nationalism', 'Greeks', 'nf2', s=60)],
        [CAP('nationalism was poison for an empire', 'poison')])),
    ('The Serbs revolted. Then the Greeks', MAP('balkans', emp(E1830) + [('Greece', 'blue', 'Greeks'), ('Republic of Serbia', 'yellow', 'Serbs')], [label('GREECE', (39.0, 22.0), 'Greeks', 'gr', s=44, spaced=True)],
        [BIG(None, '1830', '1830', color='yellow', x=0.5)])),
    ('Muhammad Ali was an Albanian officer', ST([fig('merchant', 0.6, 0.0, 'ma', h=440, say='Muhammad Ali', ss=40)], [BIG(None, '1811', '1811', x=0.64, color='red')])),
    ('Then he built a modern army and navy', MAP('arab', emp(E1830) + [('Egypt', 'teal', 'army')], [arrow(['Cairo', (31.5, 34.5), 'Damascus'], 'Syria', ('Syria', 1.2), color='teal', id='ibr', w=22)])),
    ('The old Ottoman superpower, turning outsiders into insiders, was failing.', ST([badge('cart:fig-villager', S(0.5, 0.5), 0.0, 'outsiders', 'ou2', s=110), badge('xmark', S(0.66, 0.5), 'failing', None, 'fx', s=60),
        badge('cart:fig-janissary', S(0.82, 0.5), 0.0, 'insiders', 'in2', s=110)], [CAP('they wanted their own countries', 'own', x=0.64)])),
    ('So the Ottomans tried to reinvent themselves.', ST(badges([('envelope', 'schools', 'new schools'), ('train', 'railways', 'railways'), ('globe', 'telegraph', 'telegraph')]), [CAP('THE TANZIMAT', 'Tanzimat', x=0.64), BIG(None, '1839', '1839', x=0.64, color='yellow')])),
    ('The Russian Tsar Nicholas the First is said', ST([fig('king', 0.6, 0.0, 'tsar', h=440, say='The sick man of Europe.', ss=36)], [CAP('THE SICK MAN OF EUROPE', 'sick', x=0.64)])),
    ('In the Crimean War of 1853 to 1856', MAP('black_sea', emp(E1830) + [('Russia', 'green'), ('Ukraine', 'green')], [pin('Crimea', 0.0, 'CRIMEA', 'cw', spaced=True), badge('flag-fr', (42.5, 29.0), 'France', None, 'cwf', s=40)],
        [BIG(None, '1853-1856', 'Crimean', color='yellow', x=0.5)])),
    ('And to pay for the war, the Ottomans did something new.', ST([badge('gold', S(0.5, 0.5), 'borrowed', 'loans', 'lo1', s=100), badge('gold', S(0.66, 0.5), ('more', 0.0), 'more loans', 'lo2', s=100), badge('gold', S(0.82, 0.5), ('interest', 0.0), 'more loans', 'lo3', s=100)])),
    ('By 1875, the empire could not pay.', ST([prop('stamp', 0.64, 0.6, 'bankrupt', 'bk', h=160, kw={'text': 'BANKRUPT'})], [BIG(None, '1875', '1875', x=0.64, color='red')])),
    ('The empire that once collected tribute', ST([badge('gold', S(0.64, 0.46), 0.0, 'handed to European bankers', 'eb', s=110)])),
    # ---------------- Part 15: Abdul Hamid, Young Turks, Balkan Wars
    ('In 1876, a new sultan, Abdul Hamid the Second', ST([fig('sultan', 0.6, 0.0, 'ah', h=440, say='Abdul Hamid II', ss=40), badge('envelope', S(0.82, 0.36), 'constitution', 'a constitution', 'con', s=80)],
        [BIG(None, '1876', '1876', x=0.42, color='yellow')])),
    ('He was paranoid, secretive', ST([fig('sultan', 0.5, None, 'ah', h=420), badge('train', S(0.72, 0.36), 'railways', 'railways', 'rw', s=80), badge('globe', S(0.88, 0.36), 'telegraph', 'telegraph', 'tg', s=80)],
        [CAP('spies everywhere', 'spies', x=0.64)])),
    ('And he leaned hard on one idea.', ST([fig('sultan', 0.6, 0.0, 'ah2', h=440), badge('crown', S(0.82, 0.36), 'caliph', 'caliph of all Muslims', 'clf', s=80)])),
    ("But many of the empire's educated young officers", ST([fig('genoese', 0.5 + i * 0.12, 0.2 * i, f'yt{i}', h=380) for i in range(3)], [CAP('THE YOUNG TURKS', 'Young', x=0.64)])),
    ('In 1908, they forced Abdul Hamid', ST([fig('genoese', 0.5 + i * 0.12, None, f'yt{i}', h=380) for i in range(3)] + [badge('cart:fig-sultan', S(0.86, 0.36), 'removed', 'removed', 'ahx', s=70, x=True)],
        [BIG(None, '1908', '1908', x=0.64, color='yellow')])),
    ('Then the empire lost almost everything it still held in Europe.', MAP('balkans', emp(['Turkey']) + [('Bulgaria', 'green', 'Bulgaria'), ('Greece', 'blue', 'Greece'), ('Republic of Serbia', 'yellow', 'Serbia'),
        ('Montenegro', 'yellow', 'Montenegro'), ('Albania', 'pink', 'months'), ('North Macedonia', 'yellow', 'months')], [], [BIG(None, '1912-1913', 'Balkan', color='yellow', x=0.5)])),
    ('The Ottomans were now an empire of Anatolia', MAP('arab', emp(E1914), [label('ANATOLIA', (39.0, 33.0), 'Anatolia', 'an15', s=44, spaced=True), label('ARAB LANDS', (31.0, 40.0), 'Arab', 'ar15', s=44, spaced=True)])),
    ('And then they made their final bet.', MAP('arab', emp(E1914), [], [CAP('their final bet', 'final')])),
    # ---------------- Part 16: WWI
    ('In 1914, the First World War broke out.', MAP('europe_wide', emp(E1914) + [('Germany', 'grey', 'Germany'), ('Austria', 'grey', 'Germany')], [label('GERMANY', (51.0, 10.0), 'Germany', 'de', s=44, spaced=True)],
        [BIG(None, '1914', '1914', color='yellow', x=0.5)])),
    ('At first, there was a stunning victory.', MAP('marmara', emp(E1914), [pin('Gallipoli2', 0.0, 'GALLIPOLI', 'gal', spaced=True), arrow([(39.0, 24.5), (39.9, 26.1)], 'force', ('force', 1.0), color='blue', id='ga', w=22),
        photo('kemal', 'Mustafa Kemal, 1918', 'Mustafa', x=0.28, y=0.42, h=420)], [BIG(None, '1915', '1915', color='yellow', x=0.6)])),
    ('But the war also brought one of the darkest chapters', MAP('turkey', emp(E1914), [], [CAP('one of the darkest chapters', 'darkest')], tint='gloom')),
    ('In 1915, the Ottoman government began the mass deportation', MAP('turkey', emp(E1914), [arrow([(39.5, 39.0), (37.5, 39.5), (35.8, 40.0)], 'deportation', ('Syrian', 0.5), color='white', id='dep', w=14),
        label('SYRIAN DESERT', (35.3, 40.5), 'Syrian', 'sd', s=40, spaced=True)], [BIG(None, '1915', '1915', color='white', x=0.5)], tint='gloom')),
    ('Historians estimate that somewhere between', ST([prop('candle', 0.64, 0.82, 0.0, 'flame_m', h=300)], [CAP('the Armenian genocide', 'genocide', x=0.64)])),
    ('Other Christian communities, including Assyrians and Greeks', ST([prop('candle', 0.64, 0.82, None, 'flame_m', h=300)], [CAP('Assyrians and Greeks also suffered', 'Assyrians', x=0.64)])),
    ('Meanwhile, in the south, Arab leaders backed by Britain', MAP('arab', emp(E1914) + [('HEJAZ', 'green', 'Revolt')], [label('ARAB REVOLT', (24.0, 41.0), 'Revolt', 'arr', s=40, spaced=True),
        arrow([(33.5, 35.0), (33.5, 45.0)], 'lines', ('lines', 1.0), color='white', id='sp1', w=8)], [CAP('SYKES-PICOT, 1916', 'Sykes-Picot')])),
    ('In October 1918, the Ottomans signed an armistice.', MAP('marmara', emp(E1914), [pin('Istanbul', 'Istanbul', 'ISTANBUL', 'is18', spaced=True), badge('flag-fr', (41.6, 27.8), 'occupied', None, 'occ', s=40)],
        [BIG(None, '1918', '1918', color='yellow', x=0.5)])),
    # ---------------- Part 17: the end
    ('In 1920, the Allies forced', MAP('turkey', emp(['Turkey'], 'red', 0.0) + [('ANAT_W', 'blue', 'carved'), ('ARMENIA_S', 'yellow', 'carved')], [label('SÈVRES', (41.6, 33.0), 'Sèvres', 'sv', s=48, spaced=True)],
        [BIG(None, '1920', '1920', color='yellow', x=0.5)])),
    ("The sultan's government signed it.", ST([badge('cart:fig-sultan', S(0.5, 0.5), 0.0, 'the sultan signed', 'ss1', s=100), badge('cart:fig-genoese', S(0.8, 0.5), 'refused', 'the nationalists refused', 'nr', s=100)])),
    ('Led by Mustafa Kemal, the hero of Gallipoli', MAP('turkey', emp(['Turkey']), [pin('Ankara', 0.0, 'ANKARA', 'ank', spaced=True), photo('kemal', 'Mustafa Kemal, 1918', 0.05, x=0.26, y=0.42, h=420)],
        [CAP('THE WAR OF INDEPENDENCE', 'Independence')])),
    ('And now, Mustafa Kemal did something that would have been unthinkable', ST([photo('kemal', 'Mustafa Kemal, 1918', 0.0, x=0.64, h=460)], [CAP('unthinkable', 'unthinkable', x=0.64)])),
    ('On November 1st, 1922, the new government abolished', ST([prop('stamp', 0.64, 0.62, 'abolished', 'ab', h=150, kw={'text': 'ABOLISHED'})], [BIG(None, 'Nov 1, 1922', 'November', x=0.64, color='yellow')])),
    ('A few weeks later, the last Ottoman sultan', SC([prop('galley', 0.55, 0.94, 0.0, 'hms', h=240, move_to=0.95, to=6.0), fig('sultan', 0.25, 0.0, 'm6', h=300, say='Mehmed VI', ss=40)], ground='sea', horizon=0.62, sky='dusk', clouds=0)),
    ('In 1923, the Republic of Turkey was declared', MAP('turkey', emp(['Turkey']), [pin('Ankara', 0.0, 'ANKARA', 'ank2', spaced=True), label('REPUBLIC OF TURKEY', (41.8, 35.0), 'Republic', 'rot', s=44, spaced=True)],
        [BIG(None, '1923', '1923', color='yellow', x=0.5)])),
    ('Six hundred and twenty-three years after', SC([*camp(0.0)], [BIG('the House of Osman was gone', '623 years', 'Six', color='yellow')], **DUSK)),
    # ---------------- payoff
    ("So, let's go back to our question.", MAP('empire', emp(E1683), [prop('stamp', 0.5, 0.6, 'fall', 'gone2', h=150)], [CAP('how did it rise, and why did it fall?', 'question')])),
    ('The answer is that superpower.', ST([badge('cart:fig-villager', S(0.5, 0.5), 0.0, 'outsiders', 'o1p', s=125), badge('cart:fig-janissary', S(0.8, 0.5), 0.3, 'insiders', 'o2p', s=125)])),
    ('They took the conquered and made them taxpayers.', ST(badges([('gold', 'taxpayers', 'taxpayers'), ('cart:fig-janissary', 'generals', 'grand viziers'), ('people', 'communities', 'their own communities')]))),
    ('But the same system had a dark side.', ST([badge('skull', S(0.5, 0.5), 'killed', 'brothers killed', 'dk1', s=100), badge('cart:cage', S(0.66, 0.5), 'cages', 'princes in cages', 'dk2', s=100),
        badge('cart:fig-janissary', S(0.82, 0.5), 'overthrow', 'the army rebelled', 'dk3', s=100)], [CAP('the dark side', 'dark', x=0.64)])),
    ('And when the modern world arrived', ST(badges([('train', 'railways', 'railways'), ('gold', 'banks', 'banks'), ('people', 'nations', 'nations')]), [CAP('the trick stopped working', 'stopped', x=0.64)])),
    ('And yet, look at the map today.', MAP('empire', emp(['Turkey']) + [('Iraq', 'orange', 'Iraq'), ('Syria', 'yellow', 'Syria'), ('Israel', 'sky', 'Israel'), ('Lebanon', 'pink', 'Lebanon'),
        ('Jordan', 'lime', 'Jordan'), ('Bulgaria', 'green', 'Balkans'), ('Greece', 'blue', 'Balkans'), ('Republic of Serbia', 'teal', 'Balkans')], [badge('oil', (44.0, 24.0), 'coffee', 'Ottoman coffee', 'oc', s=70)])),
    ('The empire is gone. But the world it built', SC([prop('dome', 0.5, 0.8, 0.0, 'fin', h=420), prop('minaret', 0.22, 0.8, 0.0, 'fm1', h=460), prop('minaret', 0.78, 0.8, 0.0, 'fm2', h=460)],
        [CAP('the world it built is still all around us', 'world')], sky='gold')),
    ('Not bad for a guy with a few hundred horsemen', SC([*camp(0.0), fig('colonist', 0.42, 0.0, 'osfin', h=430, say='Not bad.', ss=48), prop('horseman', 0.12, 0.99, 0.1, 'hmf', h=300)],
        [CAP('a few hundred horsemen and a lot of sheep', 'sheep')], **DUSK)),
]
CUSTOM.update({'CRETE_I': _blob(24.9, 35.25, 1.5, 0.32, seed=30), 'ARMENIA_S': _blob(42.0, 39.6, 2.5, 1.2, seed=31)})
BY_PHRASE.extend(P)
