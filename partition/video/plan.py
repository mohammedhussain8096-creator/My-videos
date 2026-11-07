"""Visual plan for every scene, keyed by scene number (the Hindi voice is locked, so the timing is final).

SC[n] = spec for scene n. A spec of SAME continues the previous scene's shot (the camera move spans both).
Kinds: P(photo), MAP(...), CARD(...). Overlays: ('date'|'caption'|'quote'|'big'|'title', text, {opts}).
Overlay options: at (s from scene start) or w (a word: appears when that word is spoken), off, sub, x, y, dim.
Only public-domain images are used (see ../IMAGE_CREDITS.md); no gore."""

C = {  # Hindi name, lat, lon
    'delhi': ('दिल्ली', 28.61, 77.21), 'lahore': ('लाहौर', 31.55, 74.34), 'amritsar': ('अमृतसर', 31.63, 74.87),
    'karachi': ('कराची', 24.86, 67.0), 'calcutta': ('कलकत्ता', 22.57, 88.36), 'dhaka': ('ढाका', 23.81, 90.41),
    'rawalpindi': ('रावलपिंडी', 33.6, 73.05), 'noakhali': ('नोआखाली', 22.87, 91.1), 'bihar': ('बिहार', 25.6, 85.1),
    'kurukshetra': ('कुरुक्षेत्र', 29.97, 76.88), 'faridabad': ('फ़रीदाबाद', 28.41, 77.31), 'nilokheri': ('निलोखेड़ी', 29.84, 76.93),
    'ulhasnagar': ('उल्हासनगर', 19.22, 73.16), 'srinagar': ('श्रीनगर', 34.08, 74.8), 'junagadh': ('जूनागढ़', 21.52, 70.46),
    'hyderabad': ('हैदराबाद', 17.39, 78.49), 'nankana': ('ननकाना साहिब', 31.45, 73.7), 'lucknow': ('लखनऊ', 26.85, 80.95),
    'mumbai': ('मुंबई', 19.07, 72.88),
}
V_ALL = (23.0, 80.5, 44.0); V_PUNJAB = (31.0, 74.5, 12.0); V_BENGAL = (23.5, 89.0, 11.0); V_NORTH = (27.5, 80.0, 30.0)
V_WEST = (26.0, 71.0, 22.0); V_KASHMIR = (33.0, 75.0, 14.0); V_DELHI = (29.0, 77.0, 8.0); V_EAST = (24.0, 87.0, 16.0)

def city(k, at, dx=0, dy=-1): n = C[k]; return (n[0], n[1], n[2], at, dx, dy)
def P(img, grade='bw', **kw): return dict(kind='photo', img=img, grade=grade, **kw)
def MAP(**kw): return dict(kind='map', **kw)
def CARD(**kw): return dict(kind='card', **kw)
def T(title, sub, off=3.4): return ('title', title, {'at': 0.2, 'sub': sub, 'off': off})
def cap(t, at=0.6): return ('caption', t, {'at': at})
def date(t, at=0.3): return ('date', t, {'at': at})
def big(t, sub='', **o): o.setdefault('at', 0.3); o['sub'] = sub; return ('big', t, o)
def quote(t, **o): o.setdefault('at', 0.3); return ('quote', t, o)
SAME = 'same'
RAJ = [('raj', 'raj', None)]
SPLIT = [('india', 'india', None), ('wpak', 'pak', None), ('epak', 'pak', None)]

SC = {
    # ---------------------------------------------------------------- शुरुआत (hook)
    1: CARD(clock=True, sec0=44, ov=[date('14 अगस्त 1947', 0.4)]),
    2: P('assembly', z0=1.0, z1=1.14, fx0=0.5, fy0=0.45, ov=[cap('संविधान सभा, नई दिल्ली, 14 अगस्त 1947')]),
    3: P('nehru_tryst', z0=1.2, z1=1.38, fx0=0.55, fy0=0.4, ov=[quote('जब दुनिया सो रही है, तब भारत जीवन और आज़ादी के लिए जागेगा।', at=0.1)]),
    4: P('redfort', z0=1.0, z1=1.12, fx0=0.6, fy0=0.6, ov=[cap('लाल क़िला, 15 अगस्त 1947')]),
    5: MAP(view=V_ALL, view1=(23.0, 80.5, 40.0), fill=[('raj', 'raj', None, 3.0)], labels=[('ब्रिटिश भारत', 22.5, 78.5, 0.3, 80)]),
    6: MAP(view=V_NORTH, view1=(29.0, 77.5, 22.0), fill=RAJ, cities=[city('delhi', 0.2, 1, 0)], boom=0.1),
    7: MAP(view=(29.5, 76.0, 18.0), view1=V_PUNJAB, fill=RAJ, cities=[city('delhi', -1, 1, 0)], labels=[('पंजाब', 31.4, 73.6, 0.3, 90)]),
    8: P('columns', z0=1.0, z1=1.15, fx0=0.5, fy0=0.55),
    9: MAP(view=V_ALL, fill=SPLIT, arrows=[(31.0, 77.5, 31.2, 72.0, 'pak', 0.4), (30.5, 72.5, 29.8, 77.8, 'india', 0.9),
                                           (23.2, 87.6, 23.7, 90.6, 'pak', 1.4), (24.2, 90.2, 22.9, 87.3, 'india', 1.9)],
           ov=[big('1.5 करोड़', 'लोग बेघर हुए', w='डेढ़', dim=False, x=0.22, y=0.78)]),
    10: P('emergency_train', z0=1.0, z1=1.16, fx0=0.5, fy0=0.45),
    11: P('amritsar', z0=1.12, z1=1.0, fx0=0.6, fy0=0.55, ov=[cap('अमृतसर, 1947')]),
    12: CARD(tone='red', ov=[big('2 लाख – 20 लाख', 'मौतों का अनुमान')], boom=0.2),
    13: P('punjab1947', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5),
    14: MAP(view=V_ALL, fill=RAJ, line=(0.3, 2.5), ov=[big('5 हफ़्ते', '', w='पाँच', dim=False, x=0.2, y=0.8),
                                                    ('title', 'भारत का बँटवारा', {'w': 'यह कहानी', 'sub': '1947'})], boom=4.6),
    # ---------------------------------------------------------------- अंग्रेज़ों का राज
    15: P('lucknow', grade='paint', z0=1.0, z1=1.18, fx0=0.4, fy0=0.55, fx1=0.6, ov=[T('अंग्रेज़ों का राज', 'अध्याय 1'), cap('1857 का विद्रोह (चित्र: टी. जे. बार्कर)', 3.8)]),
    16: P('victoria', z0=1.0, z1=1.15, fx0=0.5, fy0=0.3, ov=[date('1858'), cap('महारानी विक्टोरिया')]),
    17: P('lucknow', grade='paint', z0=1.3, z1=1.45, fx0=0.3, fy0=0.6, fx1=0.45),
    18: P('empire1909', grade='paint', z0=1.0, z1=1.12, fx0=0.5, fy0=0.5),
    19: P('religion1909', grade='paint', z0=1.0, z1=1.2, fx0=0.5, fy0=0.45, ov=[cap('1909 का धार्मिक नक़्शा'), quote('फूट डालो और राज करो', w='इसे कहा')]),
    20: P('curzon', z0=1.0, z1=1.12, fx0=0.5, fy0=0.3, ov=[date('1905'), cap('वायसराय लॉर्ड कर्ज़न')]),
    21: MAP(view=(24.5, 88.5, 14.0), fill=[('epak', 'pak', 0.2), ('raj', 'raj', None)],
            labels=[('मुस्लिम बहुल', 24.6, 90.2, 0.4, 56), ('हिंदू बहुल', 23.0, 86.4, 1.6, 56)]),
    22: CARD(tone='paper', ov=[big('स्वदेशी', 'विदेशी कपड़ों का बहिष्कार')]),
    23: CARD(bgimg='empire1909', grade='paint', ov=[date('1911'), big('बँटवारा रद्द', '')]),
    24: MAP(view=V_EAST, fill=RAJ, cities=[city('dhaka', 2.0)], ov=[big('1906', 'ऑल इंडिया मुस्लिम लीग', w='उन्नीस सौ छह', dim=False, x=0.3, y=0.78)]),
    25: CARD(bgimg='religion1909', grade='paint', ov=[date('1909'), big('अलग चुनाव क्षेत्र', 'मुसलमानों के लिए')]),
    26: CARD(tone='dark', ov=[big('धर्म के आधार पर', 'वोट और उम्मीदवार')]),
    27: CARD(tone='red', ov=[quote('राजनीति में धर्म की एक दीवार')]),
    28: CARD(tone='paper', ov=[date('1919'), big('ख़िलाफ़त आंदोलन', '', w='ख़िलाफ़त')]),
    29: P('gandhi1946', z0=1.0, z1=1.15, fx0=0.5, fy0=0.3, ov=[cap('महात्मा गांधी')]),
    30: CARD(bgimg='gandhi1946', ov=[big('हिंदू-मुस्लिम एकता', '')]),
    31: CARD(tone='paper', ov=[date('1937'), big('प्रांतीय चुनाव', '')]),
    32: MAP(view=V_ALL, fill=RAJ, ov=[big('11 में से 8', 'प्रांतों में कांग्रेस सरकार', dim=False, x=0.24, y=0.78)]),
    33: MAP(view=V_NORTH, fill=RAJ, cities=[city('lucknow', 0.3)], labels=[('संयुक्त प्रांत', 27.2, 80.6, 0.6, 70)]),
    34: P('nehru_jinnah', z0=1.0, z1=1.15, fx0=0.5, fy0=0.35, ov=[cap('नेहरू और जिन्ना, शिमला 1946')]),
    35: SAME,
    # ---------------------------------------------------------------- जिन्ना और दो राष्ट्र
    36: P('jinnah', z0=1.0, z1=1.14, fx0=0.5, fy0=0.3, ov=[T('जिन्ना और दो राष्ट्र', 'अध्याय 2'), cap('मोहम्मद अली जिन्ना', 3.8)]),
    37: P('jinnah_young', z0=1.0, z1=1.15, fx0=0.5, fy0=0.3, ov=[cap('जिन्ना, लगभग 1910')]),
    38: CARD(bgimg='jinnah_young', ov=[quote('हिंदू-मुस्लिम एकता के राजदूत', sub='')]),
    39: P('jinnah', z0=1.25, z1=1.4, fx0=0.5, fy0=0.3),
    40: SAME,
    41: P('iqbal', z0=1.0, z1=1.15, fx0=0.5, fy0=0.4, ov=[date('1930'), cap('मोहम्मद इक़बाल')]),
    42: CARD(tone='paper', ov=[date('1933'), big('चौधरी रहमत अली', 'कैम्ब्रिज')]),
    43: CARD(tone='dark', ov=[big('P · A · K · S · TAN', 'पंजाब · अफ़ग़ान · कश्मीर · सिंध · बलूचिस्तान')]),
    44: P('league1940', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5, ov=[date('23 मार्च 1940'), cap('मुस्लिम लीग कार्यसमिति, लाहौर 1940')]),
    45: MAP(view=V_ALL, fill=[('raj', 'raj', None), ('wpak', 'pak', 0.8), ('epak', 'pak', 1.4)], labels=[('मुस्लिम बहुल', 29.0, 68.5, 1.0, 54), ('मुस्लिम बहुल', 24.3, 90.3, 1.6, 48)]),
    46: P('map1946', grade='paint', z0=1.0, z1=1.12, fx0=0.5, fy0=0.5, ov=[big('दो राष्ट्र का सिद्धांत', '', w='दो राष्ट्र', y=0.8)]),
    47: CARD(tone='dark', ov=[big('दो अलग क़ौमें?', '')]),
    48: P('gandhi1946', z0=1.25, z1=1.4, fx0=0.5, fy0=0.3, ov=[quote('भारत के टुकड़े करने से पहले मेरे टुकड़े कर दो।', w='भारत के टुकड़े')]),
    # ---------------------------------------------------------------- दूसरा विश्व युद्ध
    49: CARD(bgimg='empire1909', grade='paint', ov=[T('दूसरा विश्व युद्ध', 'अध्याय 3', off=99)], boom=0.2),
    50: CARD(tone='paper', ov=[date('1939'), big('भारत युद्ध में', 'नेताओं से पूछे बिना')]),
    51: P('nehru_arc', z0=1.0, z1=1.15, fx0=0.5, fy0=0.45, ov=[cap('जवाहरलाल नेहरू')]),
    52: CARD(bgimg='gandhi1946', ov=[date('8 अगस्त 1942'), big('भारत छोड़ो', '', w='भारत छोड़ो')]),
    53: P('patel', z0=1.0, z1=1.15, fx0=0.5, fy0=0.35, ov=[cap('सरदार वल्लभभाई पटेल')]),
    54: CARD(tone='dark', ov=[big('3 साल', 'जेल में')]),
    55: P('liaquat', z0=1.0, z1=1.12, fx0=0.5, fy0=0.3, ov=[cap('लियाक़त अली ख़ान, मुस्लिम लीग')]),
    56: CARD(tone='paper', ov=[date('1945'), big('युद्ध ख़त्म', 'ब्रिटेन थक चुका था')]),
    57: CARD(bgimg='empire1909', grade='paint', ov=[big('ख़ज़ाना ख़ाली', '')]),
    58: CARD(tone='paper', ov=[date('1946'), big('चुनाव', 'मुसलमानों की लगभग सभी सीटें लीग को')]),
    59: P('jinnah', z0=1.1, z1=1.25, fx0=0.45, fy0=0.3),
    # ---------------------------------------------------------------- सीधी कार्रवाई का दिन
    60: P('cabinet_mission', z0=1.0, z1=1.12, fx0=0.5, fy0=0.45, ov=[T('सीधी कार्रवाई का दिन', 'अध्याय 4', off=99)]),
    61: P('cabinet_mission', z0=1.2, z1=1.35, fx0=0.5, fy0=0.4, ov=[cap('कैबिनेट मिशन की बातचीत, 1946')]),
    62: P('nehru_jinnah', z0=1.25, z1=1.4, fx0=0.5, fy0=0.3),
    63: CARD(tone='red', ov=[date('16 अगस्त 1946'), big('सीधी कार्रवाई का दिन', '')], boom=0.2),
    64: P('dad_rally', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5, ov=[cap('कलकत्ता, 16 अगस्त 1946')]),
    65: P('dad_rally', z0=1.35, z1=1.55, fx0=0.4, fy0=0.55, grain=1.0),
    66: CARD(tone='red', ov=[big('4,000+ मौतें', '1 लाख लोग बेघर')]),
    67: MAP(view=V_EAST, fill=RAJ, cities=[city('calcutta', 0.2), city('noakhali', 0.6), city('bihar', 3.2)]),
    68: MAP(view=(31.5, 73.5, 12.0), fill=RAJ, cities=[city('rawalpindi', 0.4), city('lahore', 0.9)]),
    69: P('gandhi_noakhali', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5, ov=[cap('गांधी जी, नोआखाली 1946')]),
    70: P('gandhi_noakhali2', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5),
    # ---------------------------------------------------------------- माउंटबेटन और जल्दबाज़ी
    71: P('attlee', z0=1.0, z1=1.14, fx0=0.5, fy0=0.3, ov=[T('माउंटबेटन और जल्दबाज़ी', 'अध्याय 5'), cap('प्रधानमंत्री क्लेमेंट एटली', 3.8)]),
    72: CARD(tone='paper', ov=[date('20 फ़रवरी 1947'), big('जून 1948', 'अंग्रेज़ों की आख़िरी तारीख़')]),
    73: P('mb_arrival', z0=1.0, z1=1.15, fx0=0.5, fy0=0.4, ov=[cap('नेहरू, माउंटबेटन का स्वागत करते हुए')]),
    74: SAME,
    75: P('gandhi_mb', z0=1.0, z1=1.15, fx0=0.5, fy0=0.45, ov=[cap('गांधी जी, लॉर्ड और लेडी माउंटबेटन के साथ')]),
    76: P('mb_jinnah', z0=1.0, z1=1.15, fx0=0.5, fy0=0.4, ov=[cap('माउंटबेटन और जिन्ना')]),
    77: P('mb_riot', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5),
    78: P('june3', z0=1.0, z1=1.15, fx0=0.5, fy0=0.45, ov=[date('3 जून 1947', 3.0)]),
    79: MAP(view=V_ALL, fill=[('raj', 'raj', None, 2.0), ('india', 'india', 2.2), ('wpak', 'pak', 2.6), ('epak', 'pak', 2.6)],
            labels=[('भारत', 22.0, 78.5, 2.6, 80), ('पाकिस्तान', 28.5, 67.5, 3.0, 64)]),
    80: MAP(view=V_ALL, view1=(27.0, 82.0, 30.0), fill=RAJ, line=(0.3, 3.0), labels=[('पंजाब', 31.6, 73.0, 0.6, 60), ('बंगाल', 24.0, 88.4, 1.2, 60)]),
    81: CARD(tone='paper', ov=[big('15 अगस्त 1947', 'जून 1948 नहीं', w='पंद्रह')]),
    82: CARD(tone='red', ov=[big('72 दिन', '', w='बहत्तर')], boom=0.3),
    83: MAP(view=V_WEST, fill=[('wpak', 'pak', None)], cities=[city('karachi', 0.3)], ov=[date('14 अगस्त 1947')]),
    84: P('jinnah', z0=1.0, z1=1.1, fx0=0.5, fy0=0.35, ov=[date('11 अगस्त 1947')]),
    85: CARD(bgimg='jinnah', ov=[quote('आप आज़ाद हैं, अपने मंदिरों में जाने के लिए, अपनी मस्जिदों में जाने के लिए।', at=0.1)]),
    86: P('mb_lahore', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5, ov=[cap('लाहौर, जुलाई 1947')]),
    # ---------------------------------------------------------------- रेडक्लिफ़ की लकीर
    87: P('award_punjab', grade='paint', z0=1.0, z1=1.12, fx0=0.5, fy0=0.5, ov=[T('रेडक्लिफ़ की लकीर', 'अध्याय 6'), cap('सर सिरिल रेडक्लिफ़')]),
    88: CARD(bgimg='award_punjab', grade='paint', ov=[big('सिरिल रेडक्लिफ़', 'इससे पहले कभी भारत नहीं आए थे')]),
    89: MAP(view=V_ALL, fill=RAJ, cities=[city('delhi', 2.5, 1, 0)], ov=[date('8 जुलाई 1947', 2.5)]),
    90: CARD(bgimg='map1946', grade='paint', ov=[big('5 हफ़्ते', 'पुराने नक़्शे, जनगणना के आँकड़े')]),
    91: MAP(view=V_NORTH, view1=V_ALL, fill=RAJ, labels=[('पंजाब आयोग', 31.4, 73.5, 0.6, 56), ('बंगाल आयोग', 23.6, 88.6, 1.4, 56)]),
    92: CARD(tone='dark', ov=[big('2 + 2 जज', 'कांग्रेस · मुस्लिम लीग')]),
    93: CARD(tone='paper', ov=[quote('हर फ़ैसला, अकेले रेडक्लिफ़ का')]),
    94: P('award_bengal', grade='paint', z0=1.0, z1=1.15, fx0=0.45, fy0=0.45),
    95: CARD(bgimg='award_punjab', grade='paint', ov=[big('8 करोड़ से ज़्यादा', 'लोगों की क़िस्मत')]),
    96: MAP(view=V_PUNJAB, view1=(31.3, 74.6, 9.0), fill=RAJ, line=(0.2, 3.5), cities=[city('lahore', 1.0), city('amritsar', 1.5, 1, 0)]),
    97: P('award_punjab', grade='paint', z0=1.4, z1=1.6, fx0=0.5, fy0=0.45),
    98: CARD(tone='paper', ov=[date('15 अगस्त 1947'), big('सीमा घोषित नहीं', '')]),
    99: CARD(bgimg='award_bengal', grade='paint', ov=[date('17 अगस्त 1947'), big('रेडक्लिफ़ अवार्ड', 'आज़ादी के दो दिन बाद')]),
    100: P('audience', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5),
    101: P('partition_map1948', grade='paint', z0=1.0, z1=1.12, fx0=0.5, fy0=0.5),
    102: CARD(tone='dark', ov=[('title', 'हर चीज़ का बँटवारा', {'w': 'सिर्फ़ ज़मीन', 'sub': 'अध्याय 7'})]),
    # ---------------------------------------------------------------- हर चीज़ का बँटवारा
    103: CARD(tone='paper', ov=[big('82.5% · 17.5%', 'भारत · पाकिस्तान')]),
    104: P('control_room', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5, ov=[cap('दिल्ली, सितंबर 1947')]),
    105: SAME,
    106: CARD(tone='dark', ov=[quote('शब्दकोश के भी दो हिस्से')]),
    107: SAME,
    108: P('empire1909', grade='paint', z0=1.2, z1=1.4, fx0=0.45, fy0=0.5, ov=[big('560+ रियासतें', '', w='पाँच सौ साठ', y=0.82)]),
    109: MAP(view=V_ALL, fill=[('india', 'india', 0.4), ('wpak', 'pak', 0.8), ('epak', 'pak', 0.8)], labels=[('भारत?', 22.0, 78.5, 0.6, 72), ('पाकिस्तान?', 28.5, 67.5, 1.0, 60)]),
    110: P('patel', z0=1.2, z1=1.35, fx0=0.5, fy0=0.35, ov=[cap('सरदार पटेल')]),
    111: CARD(bgimg='empire1909', grade='paint', ov=[big('पटेल और वी. पी. मेनन', 'लगभग सभी रियासतें भारत में')]),
    112: MAP(view=(25.5, 76.0, 36.0), fill=[('india', 'india', None)], cities=[city('junagadh', 2.6), city('hyderabad', 3.6), city('srinagar', 4.6)]),
    # ---------------------------------------------------------------- पंजाब जल उठा
    113: P('transport', z0=1.0, z1=1.14, fx0=0.5, fy0=0.5, ov=[T('पंजाब जल उठा', 'अध्याय 8')], boom=0.2),
    114: MAP(view=V_PUNJAB, fill=SPLIT, line=None, arrows=[(31.4, 72.8, 30.9, 76.2, 'india', 0.4)], cities=[city('lahore', 0.2), city('amritsar', 0.2, 1, 0)]),
    115: MAP(view=V_PUNJAB, fill=SPLIT, arrows=[(31.4, 72.8, 30.9, 76.2, 'india', -2), (30.6, 76.3, 31.0, 72.6, 'pak', 0.3)], cities=[city('lahore', -1), city('amritsar', -1, 1, 0)]),
    116: P('another1', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5),
    117: CARD(tone='red', ov=[quote('हर तरफ़ हत्यारे भी थे, और हर तरफ़ पीड़ित भी।', w='हर तरफ़')]),
    118: MAP(view=(31.6, 74.6, 4.0), fill=SPLIT, line=(0.0, 0.1), cities=[city('lahore', 0.3), city('amritsar', 0.6, 1, 0)]),
    119: P('nankana', z0=1.0, z1=1.12, fx0=0.5, fy0=0.4),
    120: MAP(view=(31.2, 74.0, 6.0), fill=SPLIT, line=(0.0, 0.1), cities=[city('nankana', 2.0), city('amritsar', 0.3, 1, 0)]),
    121: P('nankana', z0=1.15, z1=1.3, fx0=0.5, fy0=0.35, ov=[cap('ननकाना साहिब, अक्टूबर 1947')]),
    122: P('refugee_train2', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5),
    123: CARD(tone='dark', ov=[quote('भूतों की ट्रेन', w='भूतों')]),
    124: P('to_pakistan', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5),
    125: CARD(bgimg='to_pakistan', ov=[big('4 लाख लोग', 'एक ही क़ाफ़िले में')]),
    126: CARD(bgimg='to_india', ov=[big('8 दिन', '', w='आठ दिन', off=4.2)]),
    127: CARD(tone='red', ov=[big('75,000', 'औरतों का अपहरण')]),
    128: CARD(tone='dark'),
    129: P('nathu', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5, ov=[big('55,000 सैनिक', 'पंजाब बाउंड्री फ़ोर्स', w='पचपन', y=0.8, dim=False)]),
    130: P('refugee_camp_punjab', z0=1.0, z1=1.12, fx0=0.5, fy0=0.5),
    # ---------------------------------------------------------------- इंसानियत की मिसालें
    131: CARD(bgimg='columns', ov=[T('इंसानियत की मिसालें', 'अध्याय 9', off=99)]),
    132: P('to_india', z0=1.15, z1=1.3, fx0=0.5, fy0=0.5),
    133: P('rawalpindi_men', z0=1.0, z1=1.12, fx0=0.5, fy0=0.5),
    134: P('gandhi_suhrawardy', z0=1.0, z1=1.15, fx0=0.5, fy0=0.45, ov=[cap('गांधी जी, कलकत्ता, अगस्त 1947', 3.5)]),
    135: P('gandhi1946', z0=1.0, z1=1.12, fx0=0.5, fy0=0.3, ov=[date('1 सितंबर 1947', 2.0)]),
    136: SAME,
    137: P('gandhi_arc', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5),
    138: CARD(bgimg='gandhi_mb2', ov=[quote('पंजाब में 55,000 सैनिक भी शांति नहीं ला सके…', at=0.1)]),
    139: CARD(bgimg='gandhi_mb2', ov=[quote('…लेकिन बंगाल में एक आदमी की फ़ौज ने यह कर दिखाया।', at=0.1), cap('— लॉर्ड माउंटबेटन', 1.5)]),
    # ---------------------------------------------------------------- शरणार्थी
    140: P('delhi_station', z0=1.0, z1=1.12, fx0=0.5, fy0=0.5, ov=[T('शरणार्थी', 'अध्याय 10')]),
    141: P('kurukshetra', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5, ov=[cap('कुरुक्षेत्र कैंप, 1947', 3.0)]),
    142: CARD(bgimg='kurukshetra', ov=[big('3 लाख', 'लोग तंबुओं में')]),
    143: P('kotla', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5, ov=[cap('दिल्ली का एक शरणार्थी कैंप, 1947')]),
    144: CARD(bgimg='kotla', ov=[big('दिल्ली ×2', 'आबादी लगभग दोगुनी')]),
    145: P('water_line', z0=1.0, z1=1.15, fx0=0.5, fy0=0.4),
    146: P('kotla_kitchen', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5),
    147: MAP(view=V_DELHI, fill=[('india', 'india', None)], cities=[city('delhi', 0.2)], labels=[('लाजपत नगर', 28.2, 77.6, 1.0, 54), ('राजेंद्र नगर', 28.95, 76.6, 2.0, 54)]),
    148: MAP(view=(23.0, 71.0, 24.0), fill=SPLIT, arrows=[(25.4, 68.4, 19.6, 73.0, 'india', 0.4)], labels=[('सिंध', 26.0, 68.3, 0.2, 64)]),
    149: MAP(view=(23.0, 71.0, 24.0), fill=SPLIT, arrows=[(25.4, 68.4, 19.6, 73.0, 'india', -2)], cities=[city('ulhasnagar', 0.3, 1, 0)], labels=[('सिंध', 26.0, 68.3, -1, 64)]),
    150: MAP(view=V_BENGAL, fill=SPLIT, cities=[city('calcutta', 0.3), city('dhaka', 0.6)]),
    151: MAP(view=V_BENGAL, fill=SPLIT, arrows=[(24.0, 90.0, 22.8, 88.0, 'india', 0.3), (23.0, 90.6, 22.4, 88.4, 'india', 1.2), (24.8, 89.4, 23.3, 87.9, 'india', 2.1)],
             cities=[city('calcutta', -1), city('dhaka', -1)]),
    152: P('lady_mb_camp', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5),
    153: P('amrit_kaur', z0=1.0, z1=1.15, fx0=0.5, fy0=0.5),
    154: MAP(view=V_DELHI, view1=(29.2, 77.1, 6.0), fill=[('india', 'india', None)], cities=[city('delhi', -1), city('faridabad', 0.4, 1, 0), city('nilokheri', 2.4)]),
    155: SAME,
    156: MAP(view=V_ALL, fill=SPLIT, arrows=[(28.4, 77.0, 31.4, 74.3, 'pak', 0.3), (23.0, 74.0, 24.9, 67.4, 'pak', 0.9)], cities=[city('lahore', 0.5), city('karachi', 1.1)]),
    157: CARD(tone='dark', ov=[quote('अपहरण की गई औरतों की तलाश', w='अपहरण')]),
    158: CARD(tone='paper', ov=[big('भारत + पाकिस्तान', 'साझा अभियान')]),
    159: CARD(tone='paper', ov=[big('लगभग 30,000', 'औरतें घर लौटीं', w='तीस')]),
    160: CARD(tone='dark'),
    # ---------------------------------------------------------------- ज़ख़्म जो नहीं भरे
    161: CARD(bgimg='harisingh', ov=[T('ज़ख़्म जो नहीं भरे', 'अध्याय 11', off=99)], boom=0.2),
    162: MAP(view=V_KASHMIR, fill=SPLIT, cities=[city('srinagar', 0.6)], labels=[('कश्मीर', 34.6, 75.8, 0.3, 70)], ov=[date('अक्टूबर 1947')]),
    163: P('harisingh', z0=1.0, z1=1.15, fx0=0.5, fy0=0.3, ov=[cap('महाराजा हरि सिंह')]),
    164: P('sardar_abdullah', z0=1.0, z1=1.12, fx0=0.5, fy0=0.5, ov=[cap('सरदार पटेल और शेख़ अब्दुल्ला, नवंबर 1947')]),
    165: CARD(tone='red', ov=[big('1947–48', 'पहला भारत-पाकिस्तान युद्ध')], boom=0.3),
    166: MAP(view=V_KASHMIR, view1=(33.8, 75.0, 10.0), fill=SPLIT, cities=[city('srinagar', -1)], labels=[('कश्मीर', 34.6, 75.8, -1, 70)]),
    167: P('gandhi_noakhali', z0=1.2, z1=1.35, fx0=0.5, fy0=0.45, ov=[date('30 जनवरी 1948')]),
    168: CARD(tone='dark', ov=[big('30 जनवरी 1948', 'गांधी जी की हत्या')], boom=0.2),
    169: P('gandhi1946', z0=1.1, z1=1.0, fx0=0.5, fy0=0.3),
    170: P('surrender1971', z0=1.0, z1=1.15, fx0=0.5, fy0=0.45, ov=[date('1971'), cap('ढाका, 16 दिसंबर 1971')]),
    171: MAP(view=V_ALL, fill=[('india', 'india', None), ('wpak', 'pak', None), ('epak', 'bd', 0.5)],
             labels=[('भारत', 22.0, 78.5, 0.8, 72), ('पाकिस्तान', 28.5, 67.5, 1.4, 60), ('बांग्लादेश', 24.0, 90.2, 2.0, 48)]),
    # ---------------------------------------------------------------- आख़िरी बात
    172: CARD(bgimg='columns', ov=[T('आख़िरी बात', 'अध्याय 12', off=99)]),
    173: P('another_photo', z0=1.0, z1=1.15, fx0=0.5, fy0=0.45),
    174: CARD(tone='dark', ov=[quote('उस घर की चाबी…', w='चाबी')]),
    175: MAP(view=(31.6, 74.6, 4.0), fill=SPLIT, line=(0.0, 0.1), cities=[city('lahore', 0.2), city('amritsar', 2.5, 1, 0)]),
    176: CARD(tone='paper', ov=[big('पार्टीशन म्यूज़ियम', 'अमृतसर', w='पार्टीशन')]),
    177: P('to_pakistan', z0=1.2, z1=1.35, fx0=0.4, fy0=0.5),
    178: CARD(tone='dark', ov=[big('बँटवारे का सबक़', '', w='सबक़')]),
    179: CARD(bgimg='columns', ov=[quote('जब नफ़रत की राजनीति होती है, तो सबसे बड़ी क़ीमत आम आदमी चुकाता है।', at=0.1)]),
    180: MAP(view=V_ALL, fill=SPLIT, arrows=[(31.0, 77.5, 31.2, 72.0, 'pak', 0.2), (30.5, 72.5, 29.8, 77.8, 'india', 0.5),
                                             (23.2, 87.6, 23.7, 90.6, 'pak', 0.8), (24.2, 90.2, 22.9, 87.3, 'india', 1.1)],
             ov=[big('1.5 करोड़', 'बेघर', dim=False, x=0.22, y=0.78)]),
    181: P('assembly', z0=1.2, z1=1.35, fx0=0.5, fy0=0.4),
    182: P('columns', z0=1.2, z1=1.35, fx0=0.5, fy0=0.6),
    183: CARD(tone='dark', ov=[quote('यह कहानी हमें याद रखनी चाहिए…', at=0.1)]),
    184: CARD(bgimg='columns', ov=[('title', 'भारत का बँटवारा', {'at': 0.6, 'sub': '1947'})], fadeout=True),
}

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
