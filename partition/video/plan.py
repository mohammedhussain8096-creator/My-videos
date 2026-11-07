"""Visual plan, keyed by narration phrases (so it survives re-timing).

Each entry: (start of a narration phrase, spec). The scene whose phrases include that text gets the spec;
following scenes without their own entry continue the same shot (the camera move spans all of them).
Overlay options: at (s from scene start) or w (a word: appears when that word is spoken), off, sub, y, dim."""
import re

DELHI = ('दिल्ली', 28.61, 77.21); LAHORE = ('लाहौर', 31.55, 74.34); AMRITSAR = ('अमृतसर', 31.63, 74.87)
KARACHI = ('कराची', 24.86, 67.0); CALCUTTA = ('कलकत्ता', 22.57, 88.36); DHAKA = ('ढाका', 23.81, 90.41)
RAWALPINDI = ('रावलपिंडी', 33.6, 73.05)
V_ALL = (23.0, 80.5, 44.0); V_PUNJAB = (31.0, 74.5, 12.0); V_BENGAL = (23.5, 89.0, 11.0); V_NORTH = (27.5, 80.0, 30.0)

def city(c, at, dx=0, dy=-1): return (c[0], c[1], c[2], at, dx, dy)
def P(img, grade='bw', **kw): return dict(kind='photo', img=img, grade=grade, **kw)
def MAP(**kw): return dict(kind='map', **kw)
def CARD(**kw): return dict(kind='card', **kw)

ENTRIES = [
    # ---------------------------------------------------------------- hook
    ('चौदह अगस्त, उन्नीस सौ सैंतालीस की रात', CARD(clock=True, sec0=46, ov=[('date', '14 अगस्त 1947', {'at': 0.4})])),
    ('दिल्ली की संविधान सभा में', P('assembly', z0=1.0, z1=1.14, fx0=0.5, fy0=0.45, ov=[('caption', 'संविधान सभा, नई दिल्ली', {'at': 0.6})])),
    ('कुछ ही मिनटों में भारत', P('pledge', z0=1.05, z1=1.2, fx0=0.45, fy0=0.4)),
    ('ठीक बारह बजे, जवाहरलाल नेहरू', P('nehru_tryst', z0=1.0, z1=1.18, fx0=0.5, fy0=0.4, fx1=0.55, fy1=0.35,
                                        ov=[('caption', 'जवाहरलाल नेहरू, 14-15 अगस्त 1947', {'at': 0.8})])),
    ('जब दुनिया सो रही है', P('nehru_tryst', z0=1.3, z1=1.45, fx0=0.55, fy0=0.35, ov=[('quote', 'जब दुनिया सो रही है, तब भारत जीवन और आज़ादी के लिए जागेगा।', {'at': 0.2})])),
    ('बाहर सड़कों पर लोग नाच रहे हैं', P('audience', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5)),
    ('दो सौ साल की अंग्रेज़ी हुकूमत', P('redfort', z0=1.08, z1=1.0, fx0=0.5, fy0=0.45, ov=[('caption', 'लाल क़िला, 15 अगस्त 1947', {'at': 0.6})])),
    ('लेकिन उसी रात', MAP(view=V_NORTH, view1=V_PUNJAB, fill=[('raj', 'raj', None)], cities=[city(DELHI, 0.3, 1, 0)],
                         labels=[('पंजाब', 31.4, 73.2, 3.2, 84)], boom=0.1)),
    ('गाँव के गाँव ख़ाली हो रहे थे', P('columns', z0=1.0, z1=1.15, fx0=0.5, fy0=0.55)),
    ('गोद में बच्चे', P('to_india', z0=1.1, z1=1.25, fx0=0.5, fy0=0.5)),
    ('कुछ ही महीनों में, लगभग डेढ़ करोड़', MAP(view=V_ALL, fill=[('india', 'india', None), ('pak', 'pak', None)],
                         arrows=[(31.0, 77.5, 31.2, 72.0, 'pak', 0.4), (30.5, 72.5, 29.8, 77.8, 'india', 0.9),
                                 (23.2, 87.6, 23.7, 90.6, 'pak', 1.4), (24.2, 90.2, 22.9, 87.3, 'india', 1.9)],
                         ov=[('big', '1.5 करोड़', {'w': 'डेढ़', 'sub': 'लोग बेघर हुए', 'dim': False, 'x': 0.22, 'y': 0.78})])),
    ('यह इंसानी इतिहास का सबसे बड़ा पलायन', P('emergency_train', z0=1.0, z1=1.16, fx0=0.5, fy0=0.45)),
    ('और कितने लोग मारे गए', P('thamali', z0=1.12, z1=1.0, fx0=0.5, fy0=0.5)),
    ('अंदाज़ा दो लाख से लेकर बीस लाख तक है', CARD(tone='red', ov=[('big', '2 लाख – 20 लाख', {'at': 0.2, 'sub': 'मौतों का अनुमान', 'dim': False})], boom=0.2)),
    ('तो सवाल यह है', P('punjab1947', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5)),
    ('वे अचानक एक-दूसरे के दुश्मन', P('gandhi_riots', z0=1.0, z1=1.12, fx0=0.45, fy0=0.45)),
    ('और एक देश की सीमा सिर्फ़ पाँच हफ़्तों', MAP(view=V_ALL, fill=[('raj', 'raj', None)], line=(0.6, 3.0),
                         ov=[('big', '5 हफ़्ते', {'w': 'पाँच', 'dim': False, 'x': 0.2, 'y': 0.8})])),
    ('यह कहानी है भारत के बँटवारे की', CARD(bgimg='columns', ov=[('title', 'भारत का बँटवारा', {'at': 0.3, 'sub': '1947'})], boom=0.3, cut=False)),
    # ---------------------------------------------------------------- the Raj
    ('इस कहानी को समझने के लिए', CARD(bgimg='lucknow', grade='paint', ov=[('title', 'अंग्रेज़ों का राज', {'at': 0.3, 'sub': 'अध्याय 1'})], boom=0.3)),
    ('अठारह सौ सत्तावन के विद्रोह के बाद', P('victoria', grade='bw', z0=1.0, z1=1.15, fx0=0.5, fy0=0.3, ov=[('date', '1858', {'at': 0.4}),
                                        ('caption', 'महारानी विक्टोरिया', {'w': 'रानी'})])),
    ('अंग्रेज़ों ने देखा कि इस विद्रोह में', P('lucknow', grade='paint', z0=1.0, z1=1.2, fx0=0.4, fy0=0.55, fx1=0.6,
                                        ov=[('caption', '1857 का विद्रोह (चित्र: टी. जे. बार्कर)', {'at': 0.6})])),
    ('अंग्रेज़ों के लिए यह एकता ख़तरनाक थी', P('empire1909', grade='paint', z0=1.0, z1=1.12, fx0=0.5, fy0=0.5)),
    ('इतिहासकार मानते हैं कि', P('religion1909', grade='paint', z0=1.0, z1=1.15, fx0=0.5, fy0=0.45,
                                        ov=[('caption', '1909 का धार्मिक नक़्शा', {'at': 0.6})])),
    ('इसे कहा गया, फूट डालो और राज करो', P('religion1909', grade='paint', z0=1.15, z1=1.3, fx0=0.5, fy0=0.45,
                                        ov=[('quote', 'फूट डालो और राज करो', {'w': 'फूट'})])),
]

def _word_time(sc, word):
    """seconds from scene start when `word` is spoken (estimated inside its phrase by character position)"""
    for p in sc['_phr']:
        i = p['text'].find(word)
        if i >= 0:
            return max(0.0, p['start'] - sc['start'] + (p['end'] - p['start']) * i / max(1, len(p['text'])) - 0.1)
    return None

def resolve(timing):
    scenes = timing['scenes']; phr = timing['phrases']
    for sc in scenes:
        sc['_phr'] = [p for p in phr if sc['start'] - 0.2 <= p['start'] < sc['end'] - 0.05]
    own = [None] * len(scenes)
    for key, spec in ENTRIES:
        for i, sc in enumerate(scenes):
            if key in sc['text']:
                if own[i] is not None: print('  ! two entries in scene', i + 1, '- keeping first'); break
                own[i] = (key, spec); break
        else:
            pass
    out = [None] * len(scenes); i = 0
    while i < len(scenes):
        if own[i] is None and i == 0: own[0] = ('', CARD())
        if own[i] is None:
            i += 1; continue
        j = i + 1
        while j < len(scenes) and own[j] is None: j += 1
        spec = own[i][1]
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
            if k > i:
                ovs = [o for o in ovs if 'w' in o[2]] + [(o[0], o[1], dict(o[2], at=-1)) for o in spec.get('ov', []) if o[0] in ('caption', 'date', 'big', 'quote', 'title') and not (len(o) > 2 and 'w' in o[2])][:0]
                s['cut'] = True; s.pop('boom', None)
            s['ov'] = ovs
            # map fills / lines that already appeared stay on in continuation scenes
            if k > i and s.get('kind') == 'map':
                s['_carry'] = True
            out[k] = s; off += d
        i = j
    return out
