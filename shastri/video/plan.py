"""Visual plan for the Shastri video, keyed by scene number (the Hindi voice is locked, so the timing is final).

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
    'tashkent': ('ताशकंद', 41.31, 69.24), 'delhi': ('दिल्ली', 28.61, 77.21), 'mughalsarai': ('मुग़लसराय', 25.28, 83.12), 'varanasi': ('वाराणसी', 25.32, 82.99),
    'ariyalur': ('अरियालूर', 11.14, 79.08), 'lahore': ('लाहौर', 31.55, 74.34), 'hajipir': ('हाजी पीर', 33.93, 74.08), 'khemkaran': ('खेमकरण', 31.15, 74.56),
    'srinagar': ('श्रीनगर', 34.08, 74.8), 'moscow': ('मॉस्को', 55.75, 37.62), 'rawalpindi': ('रावलपिंडी', 33.6, 73.05), 'anand': ('आणंद', 22.56, 72.95),
}
RIVERS = {'ganga': [(29.95, 78.16), (29.37, 78.13), (28.4, 79.0), (27.07, 79.92), (26.47, 80.35), (25.43, 81.88), (25.15, 82.57), (25.32, 83.01), (25.58, 83.58), (25.6, 85.14)]}
CUSTOM = {}
BATTLE_RIVER = [(2750, -150), (2620, 300), (2480, 700), (2330, 1100), (2200, 1500), (2080, 1900), (1930, 2300), (1820, 2750)]

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
    1: MAP(view=(30.0, 74.0, 40.0), view1=(41.0, 69.3, 10.0), pitch=50, yaw0=-6, yaw1=6, fill=[('uzbek', 'gold', 2.0)], pulse=[pin('tashkent', 3.0, 'red')],
           labels=[('ताशकंद, सोवियत संघ', 42.0, 69.24, 3.6, 58)], ov=[('tint', '', {'at': 0.0, 'k': 0.38, 'col': (6, 12, 34)}), date('11 जनवरी 1966', 0.4)]),
    2: CARD(tone='dark', clock=True, hm=(1, 31), sec0=40, ov=[date('रात 1:32', 0.3), capw('ताशकंद के बाहर एक सरकारी बंगला', 2, 'शहर')]),
    3: P('shastri_kbr', frame=False, z0=1.1, z1=1.28, fx0=0.62, fy0=0.06, ov=[cap('प्रधानमंत्री लाल बहादुर शास्त्री (1904 – 1966)', 0.6)]),
    4: CARD(tone='dark', doc=dict(title='ताशकंद समझौता', lines=[('तारीख़: 10 जनवरी 1966', 0.4), ('भारत: लाल बहादुर शास्त्री', 1.4), ('पाकिस्तान: अयूब ख़ान', 2.4),
              ('मध्यस्थ: कोसिगिन (सोवियत संघ)', 3.4)], stamp=('हस्ताक्षर हुए', 5.0, 'green'))),
    5: CARD(tone='dark', files=[('आधिकारिक', 'मौत का कारण', 0.2)], stamps=[(0, 'दिल का दौरा', 'red', wt(5, 'दिल'))]),
    6: CARD(tone='dark', check=[('ताशकंद में पोस्टमार्टम नहीं', wt(6, 'सोवियत')), ('भारत में भी पोस्टमार्टम नहीं', wt(6, 'भारत'))]),
    7: CARD(tone='dark', doc=dict(title='परिवार के मुताबिक़', lines=[('शरीर नीला पड़ गया था', wt(7, 'नीला'))], stamp=('सवाल', wt(7, 'नीला') + 1.4, 'red')), ov=[capw('बाद में: दो अहम गवाह', 7, 'दो अहम')]),
    8: CARD(tone='dark', files=[('गवाह 1', 'डॉ. आर. एन. चुघ', 0.0), ('गवाह 2', 'निजी सेवक राम नाथ', 0.2)],
             stamps=[(0, 'सड़क हादसा', 'red', 1.0), (1, 'गाड़ी से टक्कर', 'red', 1.6)]),
    9: MAP(view=(41.6, 69.0, 7.0), view1=(41.31, 69.24, 5.0), pitch=55, yaw0=-20, yaw1=20, fill=[('uzbek', 'gold', -9)], pulse=[pin('tashkent', 0.0, 'red')],
           ov=[('tint', '', {'at': 0.0, 'k': 0.45, 'col': (6, 12, 34)}), bigw('उस रात क्या हुआ?', '', w='तो उस', y=0.78, dim=False)]),
    10: CARD(tone='red', files=[('PMO', 'शास्त्री फ़ाइल', 0.2)], stamps=[(0, 'गुप्त', 'red', rel(10, 11, 'गुप्त'))]),
    11: SAME,
}
SC[11] = CARD(bgimg='shastri_1965', ov=[('title', 'लाल बहादुर शास्त्री', {'w': 'यह कहानी', 'sub': 'ताशकंद की वो रात'})])
SC[10]['stamps'] = [(0, 'गुप्त', 'red', 2.6)]

def img_or(name, alt):
    return name if os.path.exists(os.path.join(HERE, 'assets', 'photos', name + '.jpg')) else alt
IND1 = [('india1', 'india', 0.2)]
NIGHT_T = ('tint', '', {'at': 0.0, 'k': 0.38, 'col': (6, 12, 34)})

SC.update({
    # ---------------------------------------------------------------- अध्याय 1: मुग़लसराय का लड़का
    12: MAP(view=(23.5, 80.0, 30.0), view1=(25.3, 83.0, 9.0), pitch=50, rivers=[('ganga', 2.0, 2.0, (110, 200, 255), 7)],
            pulse=[pin('mughalsarai', 3.8, 'gold')], labels=[('मुग़लसराय, उत्तर प्रदेश', 26.05, 83.12, 4.0, 56)], ov=[CH('मुग़लसराय का लड़का', 1), datew('2 अक्टूबर 1904', 12, 'दो अक्टूबर')]),
    13: P('gandhi1946', z0=1.0, z1=1.14, fx0=0.5, fy0=0.35, ov=[cap('महात्मा गांधी (जन्म: 2 अक्टूबर 1869)', 0.4), bigw('एक ही जन्मदिन', '2 अक्टूबर', w='उसी', y=0.78, dim=False)]),
    14: CARD(tone='dark', doc=dict(title='बचपन', lines=[('डेढ़ साल की उम्र में पिता की मौत', wt(14, 'पिता')), ('माँ के साथ ननिहाल में परवरिश', wt(14, 'मायके'))])),
    15: MAP(view=(25.6, 82.6, 8.0), view1=(25.32, 83.05, 4.5), pitch=55, yaw0=-10, yaw1=10, rivers=[('ganga', -1, 0, (110, 200, 255), 10)],
            labels=[('गंगा', 25.1, 82.62, 0.6, 64), ('वाराणसी', 25.55, 82.85, 1.0, 48), ('मुग़लसराय', 25.05, 83.35, 1.2, 48)],
            ov=[capw('कहा जाता है: नाव का किराया बचाने के लिए गंगा तैरकर पार करते थे', 15, 'नाव')]),
    16: SAME,
    17: CARD(tone='paper', ov=[big('जाति-पाति के ख़िलाफ़', 'नाम से उपनाम हटा दिया', at=0.3, dim=False)]),
    18: CARD(tone='dark', doc=dict(title='काशी विद्यापीठ', lines=[('पढ़ाई पूरी', wt(18, 'पढ़ाई')), ('उपाधि मिली:', wt(18, 'उपाधि'))], stamp=('शास्त्री', wt(18, 'उपाधि') + 0.9, 'red'))),
    19: CARD(bgimg='gandhi1946', ov=[datew('1921', 19, 'सोलह'), bigw('असहयोग आंदोलन', 'गांधी जी की पुकार पर', w='असहयोग')]),
    20: CARD(tone='dark', ov=[big('लगभग 9 साल', 'जेल में', at=0.3, dim=False)]),
    # ---------------------------------------------------------------- अध्याय 2: ईमानदारी की मिसाल
    21: P('nehru_shastri', z0=1.0, z1=1.12, fx0=0.5, fy0=0.4, ov=[CH('ईमानदारी की मिसाल', 2), cap('नेहरू, शास्त्री और के. कामराज (1955 से पहले)', 3.6), datew('रेल मंत्री', 21, 'रेल')]),
    22: MAP(view=(16.0, 79.0, 24.0), view1=(11.6, 79.1, 10.0), pitch=50, fill=IND1, pulse=[pin('ariyalur', 2.2, 'red')],
            labels=[('अरियालूर, तमिलनाडु', 12.3, 79.08, 2.6, 54)], ov=[date('नवंबर 1956', 0.3)]),
    23: SAME,
    24: CARD(tone='dark', doc=dict(title='इस्तीफ़ा', lines=[('पद: रेल मंत्री', 0.3), ('कारण: नैतिक ज़िम्मेदारी', wt(24, 'नैतिक'))], stamp=('इस्तीफ़ा', wt(24, 'इस्तीफ़ा'), 'red'))),
    25: P('shastri_1965', z0=1.0, z1=1.14, fx0=0.5, fy0=0.4, ov=[bigw('सादगी', 'जिसके क़िस्से आज भी सुनाए जाते हैं', w='सादगी', y=0.8, dim=False)]),
    26: CARD(tone='dark', doc=dict(title='प्रधानमंत्री की पहली कार', lines=[('बैंक से कर्ज़ लेकर ख़रीदी', wt(26, 'कर्ज़')), ('कर्ज़ चुकाया: पत्नी ललिता शास्त्री ने', rel(26, 27, 'ललिता'))],
              stamp=('चुकता', rel(26, 27, 'चुकाया'), 'green')), ov=[cap('कहा जाता है', 0.3)]),
    27: SAME,
    # ---------------------------------------------------------------- अध्याय 3: प्रधानमंत्री
    28: P('nehru_portrait', z0=1.0, z1=1.14, fx0=0.5, fy0=0.3, ov=[CH('प्रधानमंत्री', 3), cap('जवाहरलाल नेहरू (निधन: 27 मई 1964)', 3.6), bigw('अब कौन?', '', w='अब कौन', y=0.8, dim=False)]),
    29: P('shastri_kbr', frame=False, z0=1.3, z1=1.55, fx0=0.64, fy0=0.05, ov=[datew('9 जून 1964', 29, 'नौ'), capw('क़द: सिर्फ़ 5 फ़ुट 2 इंच', 29, 'पाँच')]),
    30: SAME,
    31: CARD(tone='dark', check=[('देश में अनाज की भारी कमी', wt(31, 'अनाज')), ('विदेश से गेहूँ मँगवाना पड़ रहा था', rel(31, 32, 'गेहूँ'))], ov=[big('भूख', '', at=0.3, y=0.18, dim=False)]),
    32: SAME,
    33: CARD(tone='dark', doc=dict(title='प्रधानमंत्री की अपील', lines=[('हफ़्ते में एक वक़्त का खाना छोड़ें', wt(33, 'हफ़्ते')), ('पहले अपने घर में लागू किया', rel(33, 34, 'ख़ुद'))])),
    34: SAME,
    35: CARD(bgimg='shastri_1965', ov=[quote('जय जवान, जय किसान', w='जय')], boom=wt(35, 'जय')),
    36: CARD(tone='paper', ov=[big('हरित क्रांति की राह', 'नए बीज, नई तकनीक', at=0.3, dim=False)]),
    37: MAP(view=(23.0, 74.0, 16.0), view1=(22.56, 72.95, 8.0), pitch=50, fill=IND1, pulse=[pin('anand', 1.0, 'white')],
            labels=[('आणंद: राष्ट्रीय डेयरी विकास बोर्ड', 23.6, 72.95, 1.2, 50)], ov=[date('1965', 0.3), bigw('श्वेत क्रांति', '', w='श्वेत', y=0.82, dim=False)]),
    38: SAME,
    # ---------------------------------------------------------------- अध्याय 4: 1965 का युद्ध
    39: MAP(india_outline=True, view=(32.0, 74.0, 16.0), view1=(33.8, 74.4, 9.0), pitch=50,             arrows=[(33.2, 73.4, 34.0, 74.6, 'red', 3.8), (33.6, 73.2, 34.3, 74.2, 'red', 4.4), (32.9, 73.9, 33.6, 75.0, 'red', 5.0)],
            labels=[('कश्मीर', 34.6, 75.2, 3.6, 60)], ov=[CH('1965 का युद्ध', 4), date('अगस्त 1965', 3.6)]),
    40: SAME,
    41: MAP(india_outline=True, view=(31.5, 75.0, 12.0), view1=(31.4, 74.6, 8.0), pitch=50,             arrows=[(31.0, 75.4, 31.5, 74.5, 'india', rel(41, 42, 'लाहौर') - 1.0), (31.6, 75.2, 31.65, 74.5, 'india', rel(41, 42, 'लाहौर') - 0.6)],
            cities=[city('lahore', rel(41, 42, 'लाहौर'), -1, -1)], ov=[date('सितंबर 1965', 0.3), capw('सेना को खुली छूट', 41, 'खुली')]),
    42: SAME,
    43: MAP(view=(33.8, 74.4, 7.0), view1=(33.93, 74.1, 4.5), pitch=55, yaw0=-12, yaw1=12,             pulse=[pin('hajipir', 0.6, 'gold')], labels=[('हाजी पीर दर्रा', 34.25, 74.08, 0.8, 56)], ov=[capw('घुसपैठियों का रास्ता', 44, 'रास्ता') if False else cap('घुसपैठियों का रास्ता', 4.6)]),
    44: SAME,
    45: P('patton', z0=1.0, z1=1.16, fx0=0.5, fy0=0.5, ov=[cap('अमेरिकी M48 पैटन टैंक (इसी प्रकार के टैंक)', 0.3), bigw('असल उत्तर', 'खेमकरण, पंजाब', w='असल', y=0.2, dim=False)]),
    46: SAME,
    47: MAP(view=(31.3, 74.8, 8.0), view1=(31.15, 74.56, 5.0), pitch=54, pulse=[pin('khemkaran', 0.3, 'red')],
            labels=[('पैटन नगर, खेमकरण', 31.45, 74.56, 0.6, 54)]),
    48: CARD(tone='dark', files=[('23 सितंबर 1965', 'युद्धविराम', 0.3)], stamps=[(0, 'संयुक्त राष्ट्र', 'green', wt(48, 'तेईस'))], ov=[capw('लगभग तीन हफ़्ते की लड़ाई', 48, 'तीन')]),
    49: P('shastri_1965', frame=False, z0=1.2, z1=1.35, fx0=0.5, fy0=0.35, ov=[bigw('देश का हीरो', '', w='हीरो', y=0.8, dim=False)]),
    # ---------------------------------------------------------------- अध्याय 5: ताशकंद
    50: (P('kosygin', z0=1.0, z1=1.12, fx0=0.5, fy0=0.3, ov=[CH('ताशकंद', 5), capw('सोवियत प्रधानमंत्री अलेक्सी कोसिगिन', 50, 'अलेक्सी')]) if img_or('kosygin', None) else
         CARD(tone='dark', doc=dict(title='मध्यस्थ', lines=[('सोवियत प्रधानमंत्री अलेक्सी कोसिगिन', wt(50, 'अलेक्सी')), ('बातचीत के लिए बुलाया: भारत और पाकिस्तान', wt(50, 'बुलाया'))]), ov=[CH('ताशकंद', 5)])),
    51: MAP(view=(36.0, 70.0, 26.0), view1=(41.31, 69.24, 9.0), pitch=50, fill=[('uzbek', 'gold', 0.5)], pulse=[pin('tashkent', 1.5, 'gold')],
            labels=[('ताशकंद (आज उज़्बेकिस्तान)', 42.1, 69.24, 1.8, 56)]),
    52: CARD(tone='dark', files=[('भारत', 'लाल बहादुर शास्त्री', 0.8), ('पाकिस्तान', 'राष्ट्रपति अयूब ख़ान', 1.4)], ov=[datew('4 जनवरी 1966', 52, 'चार')]),
    53: SAME,
    54: CARD(tone='dark', doc=dict(title='ताशकंद समझौता', lines=[('तारीख़: 10 जनवरी 1966', wt(54, 'दस')), ('सेनाएँ युद्ध से पहले की जगह पर लौटेंगी', rel(54, 55, 'सेनाएँ'))],
              stamp=('हस्ताक्षर हुए', rel(54, 55, 'लौट'), 'green')), ov=[capw('छह दिन की बातचीत', 54, 'छह')]),
    55: SAME,
    56: MAP(view=(33.8, 74.4, 7.0), view1=(33.93, 74.1, 5.0), pitch=55, yaw0=12, yaw1=-12,             pulse=[pin('hajipir', 0.3, 'red')], labels=[('हाजी पीर: वापस', 34.25, 74.08, 0.6, 56)], ov=[bigw('नाराज़गी', 'भारत में कई लोग नाख़ुश', w='नाराज़', y=0.82, dim=False)]),
    57: SAME,
    58: CARD(tone='dark', ov=[big('आख़िरी शाम', '10 जनवरी 1966, स्वागत समारोह', at=0.3, dim=False)]),
    59: CARD(tone='dark', clock=True, hm=(9, 58), sec0=0, ov=[date('रात लगभग 10 बजे', 0.3)]),
    60: CARD(tone='dark', doc=dict(title='कुलदीप नैयर (प्रेस सलाहकार) के मुताबिक़', lines=[('रात में दिल्ली, परिवार को फ़ोन', wt(60, 'फ़ोन')),
              ('परिवार के कुछ लोग हाजी पीर पर नाख़ुश', rel(60, 61, 'हाजी'))])),
    61: SAME,
    # ---------------------------------------------------------------- अध्याय 6: वो रात
    62: CARD(tone='dark', doc=dict(title='उस रात का खाना', lines=[('रसोइया: जान मोहम्मद', 3.9), ('राजदूत टी. एन. कौल का रसोइया', 4.9), ('हल्का खाना, फिर सोने गए', rel(62, 63, 'हल्का'))]),
             ov=[CH('वो रात', 6)]),
    63: SAME,
    64: CARD(tone='dark', clock=True, hm=(12, 59), sec0=0, ov=[date('रात लगभग 1 बजे', 0.3), capw('खाँसी और बेचैनी, कमरे से बाहर आकर मदद माँगी', 65, 'खाँसी') if False else cap('तबीयत अचानक बिगड़ी', 0.6)]),
    65: SAME,
    66: CARD(tone='dark', files=[('निजी डॉक्टर', 'डॉ. आर. एन. चुघ', 0.4), ('बुलाए गए', 'सोवियत डॉक्टर', wt(66, 'सोवियत'))]),
    67: CARD(tone='dark', clock=True, hm=(1, 31), sec0=46, ov=[date('रात 1:32', 0.3), capw('उम्र: 61 साल', 67, 'इकसठ')], boom=wt(67, 'बत्तीस')),
    68: CARD(tone='dark', doc=dict(title='संयुक्त मेडिकल रिपोर्ट', lines=[('डॉ. चुघ और सोवियत डॉक्टर', 0.6), ('कारण: दिल का दौरा', wt(68, 'दिल')),
              ('पहले भी दिल के दौरे पड़ चुके थे', rel(68, 69, 'पहले'))], stamp=('आधिकारिक', rel(68, 69, 'दौरे') + 0.4, 'green'))),
    69: SAME,
    70: CARD(tone='dark', files=[('सोवियत संघ', 'प्रधानमंत्री कोसिगिन', wt(70, 'अगले') + 0.3), ('पाकिस्तान', 'राष्ट्रपति अयूब ख़ान', wt(70, 'अगले') + 0.8)],
             stamps=[(0, 'ताबूत को कंधा', 'green', rel(70, 71, 'कंधा')), (1, 'ताबूत को कंधा', 'green', rel(70, 71, 'कंधा') + 0.4)],
             ov=[big('आधिकारिक पक्ष: दिल का दौरा', '', at=0.2, off=wt(70, 'अगले') - 0.3, dim=False, y=0.15), datew('ताशकंद हवाई अड्डा, 11 जनवरी', 70, 'अगले')]),
    71: SAME,
    72: MAP(view=(36.0, 72.0, 30.0), view1=(29.5, 76.5, 18.0), pitch=46,
            routes=[dict(pts=[ll('tashkent'), ll('delhi')], at=0.2, dur=3.6, icon='plane', col='gold')],
            pulse=[pin('delhi', 4.0, 'gold')], labels=[('विजय घाट, दिल्ली', 29.4, 77.21, rel(72, 73, 'विजय'), 56)]),
    73: SAME,
    # ---------------------------------------------------------------- अध्याय 7: सवाल
    74: CARD(tone='dark', check=[('पोस्टमार्टम: ताशकंद में नहीं', st(75) - st(74) + 0.2), ('पोस्टमार्टम: दिल्ली में भी नहीं', rel(74, 76, 'दिल्ली'))], ov=[CH('सवाल', 7), bigw('पहली बात: पोस्टमार्टम', '', w='पहली', y=0.18, dim=False)]),
    75: SAME, 76: SAME,
    77: CARD(tone='dark', doc=dict(title='ललिता शास्त्री के मुताबिक़', lines=[('जब पार्थिव शरीर दिल्ली पहुँचा:', wt(77, 'पार्थिव')), ('शरीर नीला पड़ चुका था', rel(77, 78, 'नीला')), ('शरीर पर कुछ कटे हुए निशान', rel(77, 78, 'कटे'))],
              stamp=('सवाल', rel(77, 78, 'तीसरी'), 'red'))),
    78: SAME,
    79: CARD(tone='dark', files=[('रसोइया', 'जान मोहम्मद', 0.2)], stamps=[(0, 'हिरासत', 'red', wt(79, 'हिरासत'))], ov=[cap('रिपोर्टों के मुताबिक़', 0.4)]),
    80: CARD(tone='dark', files=[('रसोइया', 'जान मोहम्मद', -9)], stamps=[(0, 'रिहा', 'green', wt(80, 'छोड़'))], ov=[capw('परिवार ने ज़हर का शक जताया', 80, 'परिवार')]),
    81: CARD(tone='dark', ov=[big('कोई पक्का सबूत नहीं', '', at=0.3, dim=False)]),
    # ---------------------------------------------------------------- अध्याय 8: गवाह
    82: CARD(tone='dark', ov=[CH('गवाह', 8), big('1977', 'केंद्र में पहली बार कांग्रेस सरकार हटी', at=3.6, dim=False)]),
    83: CARD(tone='dark', files=[('1977', 'राज नारायण समिति', 0.5)], ov=[capw('जनता पार्टी सरकार ने जाँच बैठाई', 83, 'जनता')]),
    84: SAME,
    85: CARD(tone='dark', files=[('गवाह 1', 'डॉ. आर. एन. चुघ', 0.5), ('गवाह 2', 'निजी सेवक राम नाथ', rel(85, 86, 'राम'))],
             stamps=[(0, 'सड़क हादसे में मौत', 'red', rel(85, 87, 'सड़क')), (1, 'गाड़ी से टक्कर', 'red', rel(85, 87, 'टक्कर'))],
             ov=[capw('रिपोर्टों के मुताबिक़', 86, 'रिपोर्टों')]),
    86: SAME, 87: SAME,
    88: CARD(tone='dark', files=[('गवाह 1', 'डॉ. आर. एन. चुघ', -9), ('गवाह 2', 'निजी सेवक राम नाथ', -9)],
             stamps=[(0, 'सड़क हादसे में मौत', 'red', -9), (1, 'याददाश्त चली गई', 'red', wt(88, 'याददाश्त'))], ov=[cap('कहा जाता है', 0.3)]),
    89: CARD(tone='red', ov=[big('?', 'हादसा, या कुछ और?', at=0.3)]),
    90: CARD(tone='dark', files=[('1977', 'समिति की रिपोर्ट', 0.2)], stamps=[(0, 'सार्वजनिक नहीं', 'red', wt(90, 'सार्वजनिक'))]),
    # ---------------------------------------------------------------- अध्याय 9: बंद फ़ाइल
    91: CARD(tone='dark', doc=dict(title='सूचना का अधिकार (RTI)', lines=[('माँग: शास्त्री जी की मौत से', rel(91, 92, 'शास्त्री')), ('जुड़े दस्तावेज़ सार्वजनिक हों', rel(91, 92, 'दस्तावेज़'))]),
             ov=[CH('बंद फ़ाइल', 9)]),
    92: SAME,
    93: CARD(tone='dark', doc=dict(title='प्रधानमंत्री कार्यालय का जवाब, 2009', lines=[('गुप्त दस्तावेज़: एक', wt(93, 'गुप्त')), ('खुलासे से विदेशी रिश्तों पर असर', rel(93, 94, 'रिश्तों'))],
              stamp=('गुप्त', rel(93, 94, 'असर') + 0.3, 'red'))),
    94: SAME,
    95: CARD(tone='red', files=[('PMO', 'शास्त्री फ़ाइल', 0.2)], stamps=[(0, 'गुप्त', 'red', 1.0)], ov=[bigw('उसमें क्या लिखा है?', '', w='उसमें', y=0.12, dim=False)]),
    96: P('nehru_shastri', z0=1.0, z1=1.14, fx0=0.5, fy0=0.4, ov=[capw('परिवार की माँग: सारी फ़ाइलें खोली जाएँ', 96, 'परिवार')]),
    97: SAME,
    # ---------------------------------------------------------------- आख़िरी बात
    98: P('shastri_kbr', frame=False, z0=1.15, z1=1.3, fx0=0.62, fy0=0.08, ov=[('title', 'आख़िरी बात', {'at': 0.2, 'off': 3.4, 'sub': ''}), bigw('सिर्फ़ 19 महीने', 'प्रधानमंत्री', w='उन्नीस', y=0.8, dim=False)]),
    99: CARD(tone='dark', check=[('एक युद्ध जीता', 0.6), ('अकाल से लड़ाई लड़ी', wt(99, 'अकाल')), ('जय जवान, जय किसान', rel(99, 100, 'नारा'))], tick=True),
    100: SAME,
    101: CARD(bgimg='shastri_1965', ov=[bigw('भारत रत्न', 'मरणोपरांत पाने वाले पहले भारतीय (1966)', w='भारत रत्न')]),
    102: CARD(tone='dark', check=[('न कोई घर', wt(102, 'घर')), ('न कोई ज़मीन', wt(102, 'ज़मीन')), ('बस एक कार, जिसका कर्ज़ बाक़ी था', rel(102, 103, 'कार'))], ov=[cap('कहा जाता है', 0.3)]),
    103: SAME,
    104: P('shastri_1965', frame=False, z0=1.0, z1=1.15, fx0=0.5, fy0=0.4, ov=[bigw('सादगी और ईमानदारी', 'की मिसाल', w='सादगी', y=0.8, dim=False)]),
    105: SAME,
    106: CARD(tone='dark', files=[('1', 'सिर्फ़ दिल का दौरा?', wt(106, 'दिल')), ('2', 'या कुछ और?', wt(106, 'कुछ और'))], ov=[big('आप क्या मानते हैं?', '', at=0.2, y=0.1, dim=False)]),
    107: CARD(bgimg='shastri_1965', ov=[big('कमेंट में बताइए', '', at=0.3, y=0.3, off=wt(107, 'जय') - 0.2), bigw('जय जवान, जय किसान', '', w='जय')], fadeout=True),
})

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
