"""Visual plan for the Chernobyl video, keyed by scene number (the voice is locked, so timing is final).

SC[n] = spec for scene n; SAME continues the previous shot. Every scene has a picture or an animation
(never a bare background). Images: CC0 / public domain first, CC BY / BY-SA only with credit (../IMAGE_CREDITS.md).
Overlays: ('date'|'caption'|'label'|'big'|'quote', text, {opts}); opts: at, w (word cue), off, x, y, size, col, sub, by, dim.
Transitions: tr = fade (default) | flash | glitch | push | dip | cut.  Sound: sfx = [('boom', t), ('geiger', t, dur, rate), ...]."""

CITY = {'pripyat': ('Pripyat', 51.405, 30.057), 'kyiv': ('Kyiv', 50.45, 30.52), 'minsk': ('Minsk', 53.9, 27.56),
        'moscow': ('Moscow', 55.75, 37.62), 'forsmark': ('Forsmark', 60.37, 18.17), 'stockholm': ('Stockholm', 59.33, 18.07),
        'vienna': ('Vienna', 48.21, 16.37), 'warsaw': ('Warsaw', 52.23, 21.01), 'berlin': ('Berlin', 52.52, 13.4),
        'helsinki': ('Helsinki', 60.17, 24.94), 'chernobyl_town': ('Chernobyl town', 51.27, 30.22), 'ignalina': ('Ignalina', 55.6, 26.56)}
V_EUROPE = (54.0, 20.0, 52.0); V_UKRAINE = (50.5, 30.5, 16.0); V_ZONE = (51.35, 30.1, 2.4); V_NORTH = (56.0, 24.0, 34.0)

def city(k, at, dx=1, dy=0): n = CITY[k]; return (n[0], n[1], n[2], at, dx, dy)
def P(img, grade='cold', **kw): return dict(kind='photo', img=img, grade=grade, **kw)
def MAP(**kw): return dict(kind='map', **kw)
def R(**kw): return dict(kind='reactor', **kw)
def TITLE(title, num, bg=None, **kw): return dict(kind='title', title=title, num=num, bgimg=bg, tr='dip', **kw)
def cap(t, at=0.4): return ('caption', t, {'at': at})
def date(t, at=0.2): return ('date', t, {'at': at})
def label(t, **o): return ('label', t, o)
def big(t, sub='', **o): o['sub'] = sub; return ('big', t, o)
def quote(t, **o): return ('quote', t, o)
SAME = 'same'

SC = {}

def _word_time(sc, word):
    for p in sc['_phr']:
        i = p['text'].find(word)
        if i >= 0:
            v = p['start'] - sc['start'] + (p['end'] - p['start']) * i / max(1, len(p['text'])) - 0.1
            if v < -0.15: continue          # spoken before this scene started
            return max(0.0, v)
    return None

def resolve(timing):
    scenes = timing['scenes']; phr = timing['phrases']
    for sc in scenes:
        sc['_phr'] = [p for p in phr if p['end'] > sc['start'] + 0.05 and p['start'] < sc['end'] - 0.05]
    n = len(scenes); out = [None] * n; i = 0
    while i < n:
        spec = SC.get(i + 1)
        if spec is None or spec == SAME:
            spec = dict(kind='title', title='(unplanned)', num=str(i + 1))
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
            if k > i: s['tr'] = 'cut'; s.pop('sfx', None)
            s['ov'] = ovs; out[k] = s; off += d
        i = j
    return out

import plan_scenes  # noqa: E402,F401  (fills SC)
