"""Scene-by-scene visuals, in the style of the user's reference video: old-film photos, bold keyword text on the
spoken word, flat maps with glowing red highlights, a 3D plant model, fiery titles."""
from plan import SC, SAME, P, MAP, R, TITLE, cap, date, label, big, quote, city, V_EUROPE, V_UKRAINE, V_ZONE, V_NORTH

def kw(t, w=None, at=0.3, **o):
    o = dict(o); o['w'] = w if w else None
    if w is None: o.pop('w'); o['at'] = at
    return ('kw', t, o)
def F(img, grade='bw', **kw_):                    # old-film photo
    return P(img, grade=grade, film=True, **kw_)
def PLANT(**k): return dict(kind='plant', **k)
def FIRE(text, bg=None, **k): return dict(kind='fire', text=text, bgimg=bg, **k)
RED = (225, 20, 20)

SC.update({
    # ------------------------------------------------------------ cold open: the button
    1: dict(kind='clock', **{'from': (1, 23, 30)}, rate=1.0, label='26 APRIL 1986  ·  CHERNOBYL, SOVIET UKRAINE', sfx=[('tick', 0.0, 6)],
            ov=[kw('1:23 AM', w='1:23', y=0.86)]),
    2: F('cc0_30', frame=False, z0=1.0, z1=1.12, fx0=0.5, fy0=0.3, ov=[kw('THE BUTTON', w='button')]),
    3: F('cc0_30', frame=False, z0=1.6, z1=1.9, fx0=0.2, fy0=0.33, ov=[kw('AZ-5', w='most', size=130, col=(255, 70, 50))]),
    4: R(power=0.5, boil=0.2, rods=(0.15, 0.55, 0.3, 3.0), ov=[kw('SHUT DOWN', w='shut')]),
    5: PLANT(z0=1.7, z1=2.3, fx0=4.0, fx1=11.0, hl={4: 0.2}, explode=2.2, tr='cut', sfx=[('boom', 2.2)], ov=[kw('4 SECONDS', w='Four'), kw('REACTOR 4', w='Reactor')]),
    6: SAME,
    7: R(power=2.0, boil=1.0, rods=0.6, explode=-1.0, blue_glow=True, tr='flash', ov=[kw('ROOF BLOWN OFF', w='roof')]),
    8: SAME,
    9: F('pd_pripyat1984', z0=1.0, z1=1.2, fx0=0.45, fy0=0.4, ov=[kw('50,000 PEOPLE', w='fifty')]),
    10: dict(kind='counter', count=(0, 36), suffix=' HOURS', label='BEFORE ANYONE TOLD THEM', bgimg='pd_pripyat1984', grade='bw', col=(255, 90, 70)),
    11: FIRE('CHERNOBYL\nNUCLEAR DISASTER', bg='pd_reactor', tr='flash', sfx=[('boom', 0.1)]),
    12: dict(kind='counter', count=(0, 3), label='THINGS MOST PEOPLE NEVER LEARN', bgimg='cc0_44', col=(255, 255, 255), cdur=1.0),
    13: R(power=0.9, boil=0.6, rods=(0.0, 0.25, 0.2, 2.5), tips_hot=True, ov=[kw('1. THE BUTTON', at=0.3, col=(255, 200, 120))]),
    14: F('cc0_35', z0=1.1, z1=1.3, fx0=0.5, fy0=0.6, ov=[kw('2. THE DARK WATER', at=0.3, col=(150, 210, 255))]),
    15: F('cc0_28', z0=1.0, z1=1.18, fx0=0.6, fy0=0.5, ov=[kw("3. THE ELEPHANT'S FOOT", at=0.3, col=(255, 160, 100))]),
    16: SAME,
    17: F('pd_pripyat1974', frame=False, z0=1.0, z1=1.25, fx0=0.5, fy0=0.5, tr='push'),
    18: SAME,
    # ------------------------------------------------------------ the city of the future
    19: MAP(view=(52, 85, 165), hl=[('USSR', 'fill', RED, 0.3)], pin=False, ov=[kw('SOVIET UNION', w='Soviet'), kw('1970', w='1970', y=0.16, size=110)], tr='dip'),
    20: MAP(view=(49, 31, 22), hl=[('Ukraine', 'outline', (255, 40, 30), 0.2)], pin_at=1.2, ov=[kw('UKRAINE', w='Ukraine')]),
    21: MAP(view=(49.5, 30.6, 9.0), view1=(50.9, 30.3, 4.0), cities=[city('kyiv', -1), city('pripyat', 2.6, 0, -1)], ov=[kw('100 KM', w='hundred'), kw('PRIPYAT', w='Pripyat')]),
    22: PLANT(z0=1.6, z1=1.8, bolts=[(1, 2.0), (2, 2.3), (3, 2.6), (4, 2.9)], ov=[kw('NUCLEAR POWER PLANT', w='nuclear')]),
    23: P('cc0_17', z0=1.0, z1=1.15, fx0=0.5, fy0=0.55, ov=[kw('PRIPYAT', at=0.6)]),
    24: P('cc0_16', z0=1.05, z1=1.2, fx0=0.5, fy0=0.5),
    25: P('cc0_18', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5, ov=[kw('PALACE OF CULTURE', w='palace')]),
    26: P('cc0_27', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5, ov=[kw('AVERAGE AGE: 26', w='twenty-six', size=96)]),
    27: P('pd_building', frame=False, z0=1.0, z1=1.12, fx0=0.5, fy0=0.35),
    28: P('cc0_09', z0=1.0, z1=1.12, fx0=0.5, fy0=0.5),
    29: P('pd_view', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5),
    30: P('pd_amuse', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5, ov=[kw('AMUSEMENT PARK', w='amusement')]),
    31: P('cc0_06', z0=1.0, z1=1.2, fx0=0.5, fy0=0.45, ov=[kw('MAY 1, 1986', w='May')]),
    32: P('cc0_45', z0=1.1, z1=1.3, fx0=0.5, fy0=0.5, ov=[kw('IT NEVER OPENED', w='never', col=(255, 90, 70))]),
})
