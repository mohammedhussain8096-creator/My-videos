"""Renders the Egypt explainer as an animatic in the reference video's style.

Per scene it builds a plan from visuals.txt (set type, on-screen text, characters, icons, places)
and draws frames with PIL: satellite map / grey studio / cartoon landscape / parchment backgrounds,
the Guide (the user's character), stick-figure characters, flash cards, hand-lettered labels and
yellow comic punch text. Frames are piped to ffmpeg, one segment per scene, then joined with the
narration from tts.py.

Usage: python3 render.py [first_scene last_scene]   (env EGYPT_ASSETS, OUT_DIR, WORKERS, RES)"""
import json, math, os, re, subprocess, sys, wave, random
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.environ.get('EGYPT_ASSETS', os.path.join(HERE, 'assets'))
OUT = os.environ.get('OUT_DIR', os.path.join(HERE, 'build'))
W, H = [int(x) for x in os.environ.get('RES', '1920x1080').split('x')]
S = W / 1920.0                       # layout scale
FPS = 24
Image.MAX_IMAGE_PIXELS = None

# ----------------------------------------------------------------------------- palette / fonts
INK = (58, 38, 24)
STUDIO_GREY = (201, 201, 201)
YELLOW = (246, 201, 52)
RED = (226, 85, 45)

def font(name, size):
    return ImageFont.truetype(os.path.join(ASSETS, name), max(8, int(size * S)))

_fcache = {}
def F(name, size):
    k = (name, size)
    if k not in _fcache: _fcache[k] = font(name, size)
    return _fcache[k]

EMOJI_FONT = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'

# ----------------------------------------------------------------------------- data
def load_visuals():
    vis = {}
    for line in open(os.path.join(HERE, '..', 'visuals.txt')):
        if not re.match(r'^\d+ \|', line): continue
        n, setc, visual, text, cam, sfx = [p.strip() for p in line.split(' | ')]
        vis[int(n)] = dict(set=setc, visual=visual, text=text, cam=cam, sfx=sfx)
    return vis

# places (lat, lon) used for map views, pins and arrows
PLACES = {
    'GIZA': (29.98, 31.13), 'MEMPHIS': (29.85, 31.25), 'THEBES': (25.70, 32.64), 'KARNAK': (25.72, 32.66),
    'VALLEY OF THE KINGS': (25.74, 32.60), 'ASWAN': (24.09, 32.90), 'ALEXANDRIA': (31.20, 29.92), 'CAIRO': (30.04, 31.24),
    'FUSTAT': (30.01, 31.23), 'AVARIS': (30.79, 31.82), 'FAIYUM': (29.31, 30.84), 'NUBIA': (20.5, 31.0),
    'KUSH': (18.5, 31.8), 'SUDAN': (16.0, 32.5), 'ETHIOPIA': (11.0, 38.5), 'DELTA': (30.9, 31.0), 'TURA': (29.93, 31.28),
    'LEVANT': (33.5, 36.0), 'CANAAN': (31.8, 35.0), 'MEGIDDO': (32.58, 35.18), 'KADESH': (34.56, 36.52),
    'EUPHRATES': (36.0, 39.0), 'CARCHEMISH': (36.83, 38.01), 'SYRIA': (35.0, 38.0), 'PUNT': (13.0, 42.5),
    'RED SEA': (20.0, 38.5), 'HITTITE': (39.5, 33.5), 'ANATOLIA': (39.0, 33.0), 'BABYLON': (32.54, 44.42),
    'ASSYRIA': (36.36, 43.15), 'IRAQ': (33.3, 44.4), 'IRAN': (32.5, 53.0), 'PERSIA': (32.5, 53.0), 'PELUSIUM': (31.04, 32.55),
    'SIWA': (29.20, 25.52), 'ACTIUM': (38.95, 20.77), 'ROME': (41.90, 12.50), 'GREECE': (39.0, 22.0),
    'CONSTANTINOPLE': (41.01, 28.98), 'ISTANBUL': (41.01, 28.98), 'JERUSALEM': (31.78, 35.22), 'BAGHDAD': (33.31, 44.36),
    'AIN JALUT': (32.55, 35.35), 'ARABIA': (24.0, 44.0), 'INDIA': (20.0, 77.0), 'SUEZ': (30.6, 32.33), 'ROSETTA': (31.40, 30.42),
    'SINAI': (29.5, 33.8), 'PHILAE': (24.02, 32.88), 'ABU SIMBEL': (22.34, 31.62), 'EDFU': (24.98, 32.87),
    'DENDERA': (26.14, 32.67), 'AMARNA': (27.65, 30.90), 'LIBYA': (28.0, 22.0), 'MEDITERRANEAN': (34.5, 20.0),
    'BLACK SEA': (43.5, 34.5), 'ISRAEL': (31.5, 34.9), 'BRITAIN': (52.5, -1.5), 'FRANCE': (46.5, 2.5),
'MECCA': (21.4, 39.8), 'UPPER EGYPT': (26.0, 32.6), 'LOWER EGYPT': (30.6, 31.0), 'EGYPT': (26.8, 30.8),
}
ALIASES = {'BYZANTINE': 'CONSTANTINOPLE', 'HITTITES': 'HITTITE', 'NILE': None}
DEFAULT_VIEW = (21.0, 34.0, 24.0, 38.0)   # lat0, lat1, lon0, lon1 (Egypt)

# the Nile drawn as a glowing green line (lat, lon)
NILE = [(15.6, 32.5), (17.6, 33.9), (19.2, 33.4), (18.4, 31.8), (19.8, 30.4), (21.8, 31.3), (24.1, 32.9), (25.7, 32.6),
        (26.2, 32.2), (27.2, 31.2), (28.1, 30.8), (29.0, 31.1), (30.05, 31.25), (30.9, 31.0), (31.45, 30.4)]
DELTA = [(30.1, 31.2), (31.45, 30.0), (31.55, 31.0), (31.3, 32.2)]

# empire overlays (lat, lon polygons, rough)
OVERLAYS = {
    'EGYPT': [(31.6, 25.0), (31.3, 32.3), (29.5, 34.9), (22.0, 36.9), (22.0, 25.0)],
    'UPPER': [(30.0, 30.6), (30.0, 31.8), (24.0, 33.4), (22.0, 32.2), (22.0, 31.0), (24.0, 32.4)],
    'LOWERD': DELTA,
    'NK': [(31.6, 25.0), (31.3, 32.3), (33.0, 35.0), (36.5, 36.0), (36.8, 39.0), (35.0, 40.0), (31.0, 36.8), (29.5, 34.9),
           (22.0, 36.9), (17.0, 34.5), (17.0, 31.0), (22.0, 25.0)],
    'PERSIA': [(31.6, 25.0), (31.3, 32.3), (36.5, 27.0), (41.5, 27.5), (42.0, 41.0), (40.0, 55.0), (37.0, 63.0), (25.0, 63.0),
               (25.5, 56.0), (29.5, 48.0), (29.0, 35.0), (22.0, 36.9), (22.0, 25.0)],
    'ROME': [(36.0, -9.0), (43.5, -9.0), (51.0, 2.0), (48.0, 16.0), (45.0, 29.5), (41.5, 41.0), (36.5, 41.0), (31.0, 36.5),
             (29.5, 34.9), (22.0, 36.9), (22.0, 25.0), (30.0, 18.0), (31.5, 10.0), (35.0, -6.0)],
    'OTTOMAN': [(31.6, 25.0), (31.3, 32.3), (36.5, 26.0), (42.0, 26.0), (42.0, 41.0), (37.0, 44.0), (30.0, 48.0),
                (16.0, 43.0), (22.0, 36.9), (22.0, 25.0)],
    'ARAB': [(31.6, 25.0), (31.3, 32.3), (37.0, 36.0), (36.0, 44.0), (30.0, 48.0), (24.0, 56.0), (16.0, 52.0), (13.0, 43.0),
             (22.0, 36.9), (22.0, 25.0)],
    'HYKSOS': [(30.0, 30.6), (31.6, 29.6), (31.5, 32.5), (30.0, 32.4)],
    'NUBIA': [(22.0, 30.0), (22.0, 33.5), (18.0, 34.0), (18.0, 30.5)],
}

# characters: regex -> (label, headgear, robe colour, skin)
SKIN = (246, 211, 178); SKIN_TAN = (222, 175, 135); SKIN_DARK = (150, 100, 70); SKIN_BLUE = (95, 140, 210); SKIN_GREEN = (110, 165, 95)
CHARS = [
    (r'\bKhufu\b', 'KHUFU', 'nemes', (240, 236, 222), SKIN_TAN), (r'\bKhafre\b', 'KHAFRE', 'nemes', (240, 236, 222), SKIN_TAN),
    (r'\bMenkaure\b', 'MENKAURE', 'nemes', (240, 236, 222), SKIN_TAN), (r'\bDjoser\b', 'DJOSER', 'nemes', (240, 236, 222), SKIN_TAN),
    (r'\bImhotep\b', 'IMHOTEP', 'shaved', (250, 250, 245), SKIN_TAN), (r'\bSneferu\b', 'SNEFERU', 'nemes', (240, 236, 222), SKIN_TAN),
    (r'Narmer|white crown marches', 'NARMER', 'white', (240, 236, 222), SKIN_TAN),
    (r'\bPepi\b', 'PEPI II', 'double', (240, 236, 222), SKIN_TAN), (r'Mentuhotep', 'MENTUHOTEP II', 'double', (240, 236, 222), SKIN_TAN),
    (r'\bAhmose\b', 'AHMOSE', 'blue', (240, 236, 222), SKIN_TAN), (r'\bKamose\b', 'KAMOSE', 'blue', (240, 236, 222), SKIN_TAN),
    (r'Seqenenre', 'SEQENENRE', 'white', (240, 236, 222), SKIN_TAN), (r'Thutmose I\b(?!I)', 'THUTMOSE I', 'blue', (240, 236, 222), SKIN_TAN),
    (r'Thutmose III', 'THUTMOSE III', 'blue', (240, 236, 222), SKIN_TAN), (r'Hatshepsut', 'HATSHEPSUT', 'nemes', (240, 236, 222), SKIN_TAN),
    (r'Amenhotep III', 'AMENHOTEP III', 'double', (240, 236, 222), SKIN_TAN), (r'Akhenaten', 'AKHENATEN', 'blue', (240, 236, 222), SKIN_TAN),
    (r'Nefertiti', 'NEFERTITI', 'blue', (240, 236, 222), SKIN_TAN), (r'Tutankh|boy king', 'TUTANKHAMUN', 'nemes', (240, 236, 222), SKIN_TAN),
    (r'Horemheb', 'HOREMHEB', 'blue', (240, 236, 222), SKIN_TAN), (r'Ramesses I\b(?!I)', 'RAMESSES I', 'blue', (240, 236, 222), SKIN_TAN),
    (r'Ramesses II\b(?!I)|Ramesses(?! I)', 'RAMESSES II', 'double', (240, 236, 222), SKIN_TAN), (r'Ramesses III', 'RAMESSES III', 'blue', (240, 236, 222), SKIN_TAN),
    (r'\bPiye\b', 'PIYE', 'cap', (240, 236, 222), SKIN_DARK), (r'Psamtik', 'PSAMTIK I', 'double', (240, 236, 222), SKIN_TAN),
    (r'Necho', 'NECHO II', 'blue', (240, 236, 222), SKIN_TAN), (r'Nebuchadnezzar', 'NEBUCHADNEZZAR', 'persian', (60, 90, 160), SKIN_TAN),
    (r'Cambyses', 'CAMBYSES', 'persian', (150, 60, 60), SKIN_TAN), (r'Darius', 'DARIUS I', 'persian', (120, 70, 150), SKIN_TAN),
    (r'Nectanebo', 'NECTANEBO II', 'nemes', (240, 236, 222), SKIN_TAN), (r'Alexander', 'ALEXANDER', 'helmet', (130, 60, 140), SKIN),
    (r'\bPtolemy\b|Ptolemy king|Ptolemy V', 'PTOLEMY', 'double', (240, 236, 222), SKIN), (r'Cleopatra', 'CLEOPATRA VII', 'vulture', (240, 236, 222), SKIN),
    (r'Caesar\b|Julius', 'JULIUS CAESAR', 'laurel', (200, 50, 50), SKIN), (r'Mark Antony', 'MARK ANTONY', 'helmet', (180, 60, 50), SKIN),
    (r'Octavian|Augustus', 'AUGUSTUS', 'laurel', (245, 245, 245), SKIN), (r'\bRa\b,|Ra, falcon|\bAMUN-RA', 'RA', 'sun', (240, 236, 222), SKIN_TAN),
    (r'Osiris', 'OSIRIS', 'atef', (245, 245, 245), SKIN_GREEN), (r'\bIsis\b', 'ISIS', 'isis', (200, 60, 60), SKIN_TAN),
    (r'\bAmun\b(?! priests)(?!\'s name)', 'AMUN', 'plumes', (240, 236, 222), SKIN_BLUE), (r'\bMerer\b', 'MERER', 'hair', (240, 236, 222), SKIN_TAN),
    (r'Howard Carter|Carter', 'HOWARD CARTER', 'fedora', (200, 180, 140), SKIN), (r'Carnarvon', 'LORD CARNARVON', 'tophat', (60, 60, 70), SKIN),
    (r'Saladin', 'SALADIN', 'turban', (60, 130, 70), SKIN_TAN), (r'Selim', 'SELIM I', 'turban', (180, 40, 40), SKIN),
    (r'Napoleon', 'NAPOLEON', 'bicorne', (40, 60, 120), SKIN), (r'Champollion', 'CHAMPOLLION', 'hair', (50, 50, 60), SKIN),
    (r'Muhammad Ali', 'MUHAMMAD ALI', 'turban', (160, 40, 40), SKIN), (r'Ismail', 'ISMAIL', 'fez', (30, 30, 40), SKIN_TAN),
    (r'Zaghloul', 'SAAD ZAGHLOUL', 'fez', (40, 40, 50), SKIN_TAN), (r'Nasser', 'NASSER', 'hair', (70, 70, 80), SKIN_TAN),
    (r'Louis IX', 'LOUIS IX', 'crown', (40, 60, 150), SKIN), (r'Amr\b', 'AMR IBN AL-AS', 'turban', (230, 225, 210), SKIN_TAN),
    (r'Hyksos ruler|Hyksos king', 'HYKSOS KING', 'mushroom', (150, 90, 160), SKIN_TAN),
    (r'vizier', 'VIZIER', 'shaved', (250, 250, 245), SKIN_TAN), (r'\bscribe', 'SCRIBE', 'shaved', (250, 250, 245), SKIN_TAN),
    (r'\bpriests?\b', 'PRIEST', 'shaved', (250, 250, 245), SKIN_TAN), (r'farmer', 'FARMER', 'hair', (230, 215, 170), SKIN_TAN),
    (r'governor', 'GOVERNOR', 'crown', (240, 236, 222), SKIN_TAN), (r'soldier', 'SOLDIER', 'helmet', (180, 150, 90), SKIN_TAN),
    (r'Mamluk', 'MAMLUK', 'turban', (170, 50, 50), SKIN), (r'archaeologist', 'ARCHAEOLOGIST', 'fedora', (200, 180, 140), SKIN),
]
# generic labels aren't shown as name tags
GENERIC = {'VIZIER', 'SCRIBE', 'PRIEST', 'FARMER', 'GOVERNOR', 'SOLDIER', 'MAMLUK', 'ARCHAEOLOGIST'}

# keyword -> emoji (first match order in the visual text decides the cards)
ICONS = [
    (r'pyramid', 'PYR'), (r'crown', '👑'), (r'grain|wheat|harvest', '🌾'), (r'mud\b', '🟫'), (r'boat|ship|barge|fleet|sail', '⛵'),
    (r'\bgold\b(?! crown)|coin|tribute|treasure', '🪙'), (r'scroll|papyr|letter|logbook|diary|decree', '📜'),
    (r'\bsun\b|sunrise', '☀️'), (r'rain', '🌧️'), (r'flood|water|river|wave', '🌊'), (r'chariot|horse|cavalry', '🐎'),
    (r'\bbows?\b|arrows from', '🏹'), (r'sword|weapon|battle|army|siege', '⚔️'), (r'temple|pylon|obelisk|column', '🏛️'),
    (r'mosque|minaret', '🕌'), (r'church|Christian|monk', '⛪'), (r'fort|fortress|Citadel|castle', '🏰'),
    (r'library|book|school|students|literature', '📚'), (r'skull', '💀'), (r'cobra|snake', '🐍'), (r'eagle', '🦅'),
    (r'bread|bakery|loaves', '🍞'), (r'brewery|beer', '🍺'), (r'calendar|year card|season', '🗓️'), (r'tax', '💰'),
    (r'clay tablet|tablet', '🧱'), (r'lock|padlock', '🔒'), (r'candle|lamp|torch', '🕯️'), (r'coffin|mummy|mummies|sarcophag', '⚱️'),
    (r'factory|chimney', '🏭'), (r'cotton', '🧶'), (r'dam\b|lake', '🌊'), (r'electric|power line', '⚡'), (r'handshake|shake', '🤝'),
    (r'fire|burn', '🔥'), (r'star', '⭐'), (r'globe|world map|Earth', '🌍'), (r'chain', '⛓️'), (r'fist|revolt|rise up|crowd', '✊'),
    (r'pie chart|chart', '📊'), (r'scale|balance', '⚖️'), (r'feather', '🪶'), (r'infinity|forever', '♾️'), (r'question mark', '❓'),
    (r'green tick|\btick\b|check mark', '✅'), (r'spice', '🌶️'), (r'camel', '🐪'), (r'debt|banker|shares|creditor|money', '💰'), (r'stone|block|quarr', '🪨'),
    (r'sledge|rope', '🪢'), (r'hieroglyph', '𓂀'), (r'\beye\b', '👁️'), (r'wedding|princess', '💍'), (r'baby', '👶'), (r'death|plague|Black Death', '☠️'),
    (r'counter|timer|clock|sundial|hourglass', '⏳'), (r'map', '🗺️'), (r'flag', '🚩'), (r'falcon', '🦅'), (r'palm', '🌴'), (r'dagger', '🗡️'),
]

def find_places(text):
    up = text.upper()
    found = []
    for name in sorted(PLACES, key=len, reverse=True):
        for m in re.finditer(r'\b' + re.escape(name) + r'\b', up):
            if not any(m.start() >= a and m.end() <= b for _, a, b in found):
                found.append((name, m.start(), m.end()))
    for k, v in ALIASES.items():
        if v and re.search(r'\b' + k + r'\b', up) and v not in [f[0] for f in found]:
            found.append((v, up.find(k), up.find(k) + len(k)))
    found.sort(key=lambda f: f[1])
    out = []
    for f in found:
        if f[0] not in out: out.append(f[0])
    return out

CROWD = [('PERSIANS', 'persian', (120, 70, 150), SKIN_TAN), ('GREEKS', 'helmet', (60, 90, 170), SKIN),
         ('ROMANS', 'laurel', (200, 50, 50), SKIN), ('ARABS', 'turban', (60, 130, 70), SKIN_TAN),
         ('TURKS', 'turban', (180, 40, 40), SKIN), ('BRITISH', 'bicorne', (200, 40, 40), SKIN)]

def find_chars(text):
    if re.search(r'Six stick-figure rulers|Conqueror icons|conqueror icons', text):
        return list(CROWD)
    hits = []
    for rx, label, hat, robe, skin in CHARS:
        m = re.search(rx, text)
        if m: hits.append((m.start(), label, hat, robe, skin))
    hits.sort()
    seen, out = set(), []
    for _, label, hat, robe, skin in hits:
        if label not in seen: seen.add(label); out.append((label, hat, robe, skin))
    named = [c for c in out if c[0] not in GENERIC]
    generic = [c for c in out if c[0] in GENERIC]
    return (named + generic)[:3]


def find_icons(text, n):
    hits = []
    for rx, em in ICONS:
        m = re.search(rx, text, re.I)
        if m: hits.append((m.start(), em))
    hits.sort()
    out = []
    for _, em in hits:
        if em not in out: out.append(em)
    return out[:n]

def overlay_for(v, sn):
    t = v['visual'] + ' ' + v['text']
    if re.search(r'Persian overlay|PERSIAN PROVINCE|swallows Egypt', t): return 'PERSIA'
    if re.search(r'Roman red|ROME IS COMING|FREE OF ROME|Rome swallow', t): return 'ROME'
    if re.search(r'Ottoman|ISTANBUL', t) and sn > 200: return 'OTTOMAN'
    if re.search(r'Arab army', t): return 'ARAB'
    if re.search(r'Hyksos colour|delta turns', t): return 'HYKSOS'
    if re.search(r'red empire|17 CAMPAIGNS|SYRIA → SUDAN|red overlay|LARGEST EMPIRE|BUILD AN EMPIRE|empire overlay', t): return 'NK'
    if re.search(r'two colours|merge into one|one colour|UNITED|REUNIT', t): return 'EGYPT'
    if re.search(r'NUBIA', t) and 'fort' in t: return 'NUBIA'
    return None

# ----------------------------------------------------------------------------- plan
def segments(text):
    segs = [s.strip() for s in text.split(' / ') if s.strip()]
    out = []
    for s in segs:
        punch = bool(re.search(r'\d', s)) or len(s.split()) <= 3 or s.endswith('!') or s.endswith('?')
        if len(s) > 34: punch = False
        out.append({'text': s, 'punch': punch})
    return out

def plan_scene(sn, v, dur):
    setc = v['set']
    vis = v['visual']
    p = {'scene': sn, 'set': setc, 'dur': dur, 'visual': vis}
    p['guide'] = setc in ('STUDIO', 'MAP') or 'Guide' in vis
    p['segs'] = segments(v['text'])
    n = len(p['segs'])
    for i, s in enumerate(p['segs']):
        s['t'] = 0.25 + i * max(0.9, (dur - 0.8) / max(1, n))
    p['chars'] = find_chars(vis) if setc != 'MAP' else []
    ncards = {'STUDIO': 3, 'ART': 2, 'SCENE': 2, 'MAP': 0}[setc]
    if len(p['chars']) > 3: ncards = 0
    if p['chars'] and setc == 'SCENE': ncards = 1
    p['icons'] = find_icons(vis, ncards)
    # stagger pops between text segments
    k = len(p['chars']) + len(p['icons'])
    p['pop'] = [0.5 + i * max(0.45, (dur - 1.5) / max(1, k)) for i in range(k)]
    p['places'] = find_places(vis + ' ' + v['text']) if setc == 'MAP' else []
    p['overlay'] = overlay_for(v, sn) if setc == 'MAP' else None
    p['arrow'] = setc == 'MAP' and bool(re.search(r'arrow|route|march|sail|loop|dotted|chase|push', vis, re.I)) and len(p['places']) >= 2
    p['boat'] = bool(re.search(r'boat|ship|barge|fleet|sail', vis, re.I))
    p['nile'] = setc == 'MAP'
    p['nile_glow'] = setc == 'MAP' and bool(re.search(r'Nile|green line|river|valley', vis))
    p['xstamp'] = 'red X' in vis
    p['night'] = bool(re.search(r'\bNight\b|night|torchlight', vis))
    p['sunset'] = bool(re.search(r'sunset|golden-hour|Golden-hour|dusk|dark red|Sunset', vis))
    p['pyramids'] = bool(re.search(r'pyramid|Giza|Sphinx', vis, re.I))
    p['river'] = bool(re.search(r'river|Nile|flood|boat|water', vis, re.I))
    p['buildings'] = bool(re.search(r'temple|palace|city|Cairo|Alexandria|town|street|church|mosque|museum|Karnak|Thebes', vis))
    p['seed'] = sn
    return p

# ----------------------------------------------------------------------------- drawing helpers
def ease_pop(t):
    """0->1 with overshoot, t in seconds since appearance"""
    if t <= 0: return 0.0
    x = min(1.0, t / 0.28)
    return 1 + 0.12 * math.sin(math.pi * x) * (1 - x) * 2 if x >= 1 else (x * 1.12 if x < 0.85 else 1.12 - (x - 0.85) / 0.15 * 0.12)

def shadowed(img, off=6, blur=6, alpha=90):
    pad = blur * 3 + off
    base = Image.new('RGBA', (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new('RGBA', img.size, (0, 0, 0, alpha))
    sh.putalpha(img.split()[3].point(lambda a: a * alpha // 255))
    base.alpha_composite(sh, (pad + off, pad + off))
    base = base.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(img, (pad, pad))
    return base

_cmaps = {}
def has_glyph(fname, ch):
    if fname not in _cmaps:
        from fontTools.ttLib import TTFont
        _cmaps[fname] = set(TTFont(os.path.join(ASSETS, fname)).getBestCmap().keys())
    return ord(ch) in _cmaps[fname] or ch == ' '

def draw_runs(d, xy, text, fname, f, fill, sw, stroke):
    """draw text, using DejaVu Sans Bold for characters the display font lacks (arrows, ticks)"""
    x, y = xy
    fb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', int(f.size * 0.8))
    run, cur = [], None
    for ch in text:
        k = has_glyph(fname, ch)
        if cur is None or k == cur: run.append(ch)
        else:
            x = _draw_run(d, x, y, ''.join(run), f if cur else fb, fill, sw, stroke, f); run = [ch]
        cur = k
    if run: _draw_run(d, x, y, ''.join(run), f if cur else fb, fill, sw, stroke, f)

def _draw_run(d, x, y, t, ft, fill, sw, stroke, base):
    dy = (base.size - ft.size) * 0.55 if ft is not base else 0
    d.text((x, y + dy), t, font=ft, fill=fill, stroke_width=sw, stroke_fill=stroke)
    return x + d.textlength(t, font=ft)

def run_len(d, text, fname, f):
    fb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', int(f.size * 0.8))
    return sum(d.textlength(ch, font=f if has_glyph(fname, ch) else fb) for ch in text)

def text_img(text, fname, size, fill, stroke, sw, maxw=None, spacing=0):
    f = F(fname, size)
    words = text.split(); lines = []; cur = ''
    maxw = maxw or W * 0.8
    d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    for w in words:
        t = (cur + ' ' + w).strip()
        if run_len(d0, t, fname, f) > maxw and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    lines.append(cur)
    sw = int(sw * S)
    lh = int(f.size * 1.08)
    wd = int(max(run_len(d0, l, fname, f) for l in lines)) + sw * 2 + 8
    img = Image.new('RGBA', (wd, lh * len(lines) + sw * 2 + int(f.size * 0.3)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, l in enumerate(lines):
        lw = run_len(d, l, fname, f)
        draw_runs(d, ((wd - lw) / 2, sw + i * lh), l, fname, f, fill, sw, stroke)
    return shadowed(img, off=int(4 * S), blur=int(4 * S), alpha=110)

_ecache = {}
def emoji_img(em, size):
    k = (em, size)
    if k in _ecache: return _ecache[k]
    if em == 'PYR':
        im = Image.new('RGBA', (220, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.polygon([(110, 10), (210, 190), (10, 190)], fill=(222, 182, 110), outline=INK, width=5)
        d.polygon([(110, 10), (210, 190), (130, 190)], fill=(190, 145, 80), outline=INK, width=5)
        for y in range(50, 190, 28): d.line([(110 - (y - 10) * 0.55, y), (110 + (y - 10) * 0.55, y)], fill=(150, 110, 60), width=2)
    elif em == '𓂀':
        im = Image.new('RGBA', (220, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse((40, 60, 180, 130), outline=INK, width=8); d.ellipse((90, 70, 130, 120), fill=INK)
        d.line([(110, 130), (100, 180)], fill=INK, width=8); d.arc((120, 120, 180, 190), 180, 300, fill=INK, width=8)
        d.line([(30, 50), (190, 50)], fill=INK, width=8)
    else:
        f = ImageFont.truetype(EMOJI_FONT, 109)
        im = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((10, 10), em, font=f, embedded_color=True)
        bb = im.getbbox()
        im = im.crop(bb) if bb else im
    r = size / max(im.size)
    im = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
    _ecache[k] = im
    return im

def card_img(em, size):
    pad = int(size * 0.18)
    c = Image.new('RGBA', (size + pad * 2, size + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((0, 0, c.width - 1, c.height - 1), radius=int(14 * S), fill=(250, 246, 234), outline=INK, width=max(2, int(4 * S)))
    e = emoji_img(em, int(size * 0.82))
    c.alpha_composite(e, ((c.width - e.width) // 2, (c.height - e.height) // 2))
    return shadowed(c, off=int(8 * S), blur=int(8 * S), alpha=80)

def draw_figure(label, hat, robe, skin, h=420, show_label=True):
    """Stick figure in the reference style: round head, dot eyes, thin dark limbs, simple robe."""
    sc = h / 420.0
    Wf = int(260 * sc); Hf = int(470 * sc)
    im = Image.new('RGBA', (Wf, Hf), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    L = lambda *p: [(x * sc, y * sc) for x, y in p]
    lw = max(3, int(7 * sc))
    cx = 130
    # legs + feet
    d.line(L((cx - 18, 300), (cx - 30, 410)), fill=INK, width=lw); d.line(L((cx + 18, 300), (cx + 30, 410)), fill=INK, width=lw)
    d.ellipse([*(v * sc for v in (cx - 48, 402, cx - 22, 416))], fill=INK); d.ellipse([*(v * sc for v in (cx + 22, 402, cx + 48, 416))], fill=INK)
    # robe
    d.polygon(L((cx - 34, 150), (cx + 34, 150), (cx + 52, 310), (cx - 52, 310)), fill=robe, outline=INK)
    d.line(L((cx - 34, 205), (cx + 34, 205)), fill=(max(0, robe[0] - 60), max(0, robe[1] - 60), max(0, robe[2] - 60)), width=max(2, int(5 * sc)))
    # arms
    d.line(L((cx - 30, 160), (cx - 70, 230), (cx - 60, 270)), fill=INK, width=lw, joint='curve')
    d.line(L((cx + 30, 160), (cx + 72, 215), (cx + 92, 175)), fill=INK, width=lw, joint='curve')
    # neck + head
    d.line(L((cx, 135), (cx, 152)), fill=INK, width=lw)
    hx0, hy0, hx1, hy1 = cx - 46, 48, cx + 46, 140
    back = {'nemes': (40, 80, 170), 'atef': (245, 245, 240)}.get(hat)
    if hat == 'nemes':   # striped head-cloth flaps behind the face
        d.polygon(L((cx - 58, 70), (cx + 58, 70), (cx + 62, 165), (cx + 40, 165), (cx, 120), (cx - 40, 165), (cx - 62, 165)), fill=(212, 175, 55), outline=INK)
        for y in range(80, 165, 14): d.line(L((cx - 60, y), (cx + 60, y)), fill=(40, 80, 170), width=max(2, int(5 * sc)))
    d.ellipse([*(v * sc for v in (hx0, hy0, hx1, hy1))], fill=skin, outline=INK, width=max(2, int(4 * sc)))
    if hat == 'mushroom' or hat == 'hair':
        d.chord([*(v * sc for v in (hx0 - 4, hy0 - 6, hx1 + 4, hy1 - 30))], 180, 360, fill=(70, 45, 30) if hat == 'hair' else (40, 30, 30))
    # face
    d.ellipse([*(v * sc for v in (cx - 20, 88, cx - 11, 99))], fill=INK); d.ellipse([*(v * sc for v in (cx + 11, 88, cx + 20, 99))], fill=INK)
    d.arc([*(v * sc for v in (cx - 14, 100, cx + 14, 122))], 20, 160, fill=INK, width=max(2, int(3 * sc)))
    d.ellipse([*(v * sc for v in (cx - 34, 104, cx - 22, 112))], fill=(240, 150, 140)); d.ellipse([*(v * sc for v in (cx + 22, 104, cx + 34, 112))], fill=(240, 150, 140))
    # headgear
    if hat == 'nemes':
        d.polygon(L((cx - 48, 72), (cx + 48, 72), (cx + 40, 40), (cx - 40, 40)), fill=(212, 175, 55), outline=INK)
        for x in range(-36, 40, 12): d.line(L((cx + x, 42), (cx + x * 1.15, 72)), fill=(40, 80, 170), width=max(2, int(4 * sc)))
        d.ellipse([*(v * sc for v in (cx - 6, 34, cx + 6, 48))], fill=(230, 180, 40), outline=INK)
    elif hat in ('white', 'double'):
        if hat == 'double':
            d.polygon(L((cx - 44, 70), (cx + 44, 70), (cx + 44, 10), (cx + 30, 10), (cx + 30, 40), (cx - 44, 40)), fill=(200, 50, 45), outline=INK)
        d.polygon(L((cx - 26, 70), (cx + 26, 70), (cx + 18, 20), (cx + 10, -10), (cx - 10, -10), (cx - 18, 20)), fill=(245, 243, 235), outline=INK)
        d.ellipse([*(v * sc for v in (cx - 10, -22, cx + 10, -4))], fill=(245, 243, 235), outline=INK)
    elif hat == 'blue':
        d.chord([*(v * sc for v in (cx - 50, 0, cx + 50, 110))], 180, 360, fill=(50, 90, 190), outline=INK)
        for x in range(-36, 40, 16):
            for y in (24, 40): d.ellipse([*(v * sc for v in (cx + x - 3, y - 3, cx + x + 3, y + 3))], fill=(230, 200, 60))
    elif hat == 'plumes':
        d.rectangle([*(v * sc for v in (cx - 40, 46, cx + 40, 64))], fill=(212, 175, 55), outline=INK)
        d.polygon(L((cx - 24, 48), (cx - 4, 48), (cx - 10, -60), (cx - 22, -60)), fill=(220, 120, 60), outline=INK)
        d.polygon(L((cx + 4, 48), (cx + 24, 48), (cx + 22, -60), (cx + 10, -60)), fill=(220, 120, 60), outline=INK)
    elif hat == 'sun':
        d.ellipse([*(v * sc for v in (cx - 34, -16, cx + 34, 52))], fill=(240, 140, 40), outline=INK, width=max(2, int(4 * sc)))
        d.polygon(L((cx + 30, 92), (cx + 62, 102), (cx + 34, 112)), fill=(230, 180, 60), outline=INK)  # falcon beak
    elif hat == 'atef':
        d.polygon(L((cx - 22, 64), (cx + 22, 64), (cx + 14, 0), (cx, -24), (cx - 14, 0)), fill=(245, 243, 235), outline=INK)
        d.polygon(L((cx - 34, 64), (cx - 22, 64), (cx - 26, -6)), fill=(220, 120, 60), outline=INK)
        d.polygon(L((cx + 34, 64), (cx + 22, 64), (cx + 26, -6)), fill=(220, 120, 60), outline=INK)
    elif hat == 'isis':
        d.rectangle([*(v * sc for v in (cx - 20, 10, cx + 20, 52))], fill=(212, 175, 55), outline=INK)
        d.rectangle([*(v * sc for v in (cx - 20, 10, cx - 6, 30))], fill=(212, 175, 55), outline=INK)
    elif hat == 'vulture':
        d.chord([*(v * sc for v in (cx - 52, 34, cx + 52, 120))], 180, 360, fill=(212, 175, 55), outline=INK)
        d.ellipse([*(v * sc for v in (cx - 7, 28, cx + 7, 44))], fill=(60, 140, 90), outline=INK)
        d.chord([*(v * sc for v in (hx0 - 6, 70, hx0 + 22, 170))], 90, 270, fill=(20, 20, 30))
        d.chord([*(v * sc for v in (hx1 - 22, 70, hx1 + 6, 170))], 270, 90, fill=(20, 20, 30))
    elif hat == 'cap':
        d.chord([*(v * sc for v in (cx - 48, 40, cx + 48, 110))], 180, 360, fill=(212, 175, 55), outline=INK)
        for x in (-10, 10): d.ellipse([*(v * sc for v in (cx + x - 6, 34, cx + x + 6, 50))], fill=(60, 140, 90), outline=INK)
    elif hat == 'shaved':
        pass
    elif hat == 'turban':
        d.ellipse([*(v * sc for v in (cx - 52, 20, cx + 52, 80))], fill=(245, 243, 235), outline=INK, width=max(2, int(4 * sc)))
        d.arc([*(v * sc for v in (cx - 40, 30, cx + 40, 70))], 200, 340, fill=(200, 190, 170), width=max(2, int(4 * sc)))
    elif hat == 'laurel':
        for i in range(9):
            a = math.radians(200 + i * 17.5); x = cx + 50 * math.cos(a); y = 90 + 48 * math.sin(a)
            d.ellipse([*(v * sc for v in (x - 9, y - 5, x + 9, y + 5))], fill=(90, 150, 60), outline=INK)
    elif hat == 'fez':
        d.polygon(L((cx - 28, 60), (cx + 28, 60), (cx + 22, 20), (cx - 22, 20)), fill=(190, 40, 40), outline=INK)
        d.line(L((cx, 20), (cx + 26, 40)), fill=INK, width=max(2, int(3 * sc)))
    elif hat == 'bicorne':
        d.chord([*(v * sc for v in (cx - 80, 10, cx + 80, 90))], 180, 360, fill=(30, 30, 40), outline=INK)
        d.ellipse([*(v * sc for v in (cx - 8, 34, cx + 8, 50))], fill=(220, 50, 50))
    elif hat == 'tophat':
        d.rectangle([*(v * sc for v in (cx - 30, -6, cx + 30, 56))], fill=(30, 30, 35), outline=INK)
        d.rectangle([*(v * sc for v in (cx - 52, 52, cx + 52, 62))], fill=(30, 30, 35), outline=INK)
    elif hat == 'fedora':
        d.chord([*(v * sc for v in (cx - 36, 20, cx + 36, 90))], 180, 360, fill=(170, 140, 100), outline=INK)
        d.rectangle([*(v * sc for v in (cx - 60, 52, cx + 60, 62))], fill=(170, 140, 100), outline=INK)
    elif hat == 'helmet':
        d.chord([*(v * sc for v in (cx - 50, 36, cx + 50, 120))], 180, 360, fill=(200, 150, 60), outline=INK)
        d.chord([*(v * sc for v in (cx - 40, 0, cx + 40, 60))], 180, 360, fill=(200, 50, 45), outline=INK)
    elif hat == 'persian':
        d.rectangle([*(v * sc for v in (cx - 34, 0, cx + 34, 60))], fill=(212, 175, 55), outline=INK)
        d.chord([*(v * sc for v in (cx - 38, 104, cx + 38, 200))], 0, 180, fill=(40, 30, 30))
    elif hat == 'crown':
        d.polygon(L((cx - 40, 62), (cx + 40, 62), (cx + 44, 22), (cx + 22, 44), (cx, 14), (cx - 22, 44), (cx - 44, 22)), fill=(230, 185, 40), outline=INK)
    if show_label and label not in GENERIC:
        t = text_img(label, 'patrick.ttf', max(30, 46 * sc), (255, 255, 255), INK, 3)
        canvas = Image.new('RGBA', (max(im.width, t.width), im.height + t.height), (0, 0, 0, 0))
        canvas.alpha_composite(t, ((canvas.width - t.width) // 2, 0))
        canvas.alpha_composite(im, ((canvas.width - im.width) // 2, t.height - int(10 * sc)))
        return canvas
    return im

# ----------------------------------------------------------------------------- backgrounds
_world = None
def world():
    global _world
    if _world is None:
        _world = Image.open(os.path.join(ASSETS, 'world_graded.jpg')).convert('RGB')
    return _world

LON0, LAT1, PPD = -25.0, 62.0, 60.0     # crop origin and pixels per degree

def ll2px(lat, lon):
    return (lon - LON0) * PPD, (LAT1 - lat) * PPD

def map_view(places):
    pts = [PLACES[p] for p in places if p in PLACES and p != 'EGYPT']
    if not pts:
        lat0, lat1, lon0, lon1 = DEFAULT_VIEW
    else:
        lats = [p[0] for p in pts]; lons = [p[1] for p in pts]
        lat0, lat1, lon0, lon1 = min(lats), max(lats), min(lons), max(lons)
        padlat = max(3.0, (lat1 - lat0) * 0.35); padlon = max(4.0, (lon1 - lon0) * 0.35)
        lat0 -= padlat; lat1 += padlat; lon0 -= padlon; lon1 += padlon * 1.6   # room for the Guide on the right
    # fix aspect 16:9 in pixel space
    x0, y1 = ll2px(lat0, lon0); x1, y0 = ll2px(lat1, lon1)
    wpx, hpx = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if wpx / hpx < 16 / 9: wpx = hpx * 16 / 9
    else: hpx = wpx * 9 / 16
    wpx = max(wpx, 1500); hpx = wpx * 9 / 16
    # keep the view (incl. the 1.1x zoom margin) inside the map image
    WW, HH = 6420, 6120
    wpx = min(wpx, WW / 1.12); hpx = wpx * 9 / 16
    cx = min(max(cx, wpx * 0.56), WW - wpx * 0.56); cy = min(max(cy, hpx * 0.56), HH - hpx * 0.56)
    return cx, cy, wpx, hpx

def sky_bg(p):
    rnd = random.Random(p['seed'])
    Wb, Hb = int(W * 1.08), int(H * 1.08)
    img = Image.new('RGB', (Wb, Hb)); d = ImageDraw.Draw(img)
    if p['night']: top, bot = (20, 30, 70), (70, 70, 120)
    elif p['sunset']: top, bot = (120, 90, 160), (246, 160, 90)
    else: top, bot = (120, 190, 235), (215, 238, 250)
    hor = int(Hb * 0.62)
    for y in range(hor):
        t = y / hor; d.line([(0, y), (Wb, y)], fill=tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)))
    if p['night']:
        for _ in range(120):
            x, y = rnd.randrange(Wb), rnd.randrange(hor); r = rnd.choice((1, 1, 2)) * S
            d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 250, 220))
    else:
        cloud = (255, 220, 225) if p['sunset'] else (255, 255, 255)
        mask = Image.new('L', (Wb, Hb), 0); md = ImageDraw.Draw(mask)
        for _ in range(4):
            cx, cy = rnd.randrange(int(Wb * 0.05), int(Wb * 0.95)), rnd.randrange(int(Hb * 0.08), int(Hb * 0.26))
            k = rnd.uniform(0.8, 1.3) * S
            for (dx, dy, r) in ((-60, 0, 34), (-20, -24, 46), (30, -14, 40), (68, 4, 30)):
                md.ellipse((cx + (dx - r) * k, cy + (dy - r) * k, cx + (dx + r) * k, cy + (dy + r) * k), fill=255)
            md.rounded_rectangle((cx - 92 * k, cy - 8 * k, cx + 96 * k, cy + 32 * k), radius=int(20 * k), fill=255)
        edge = mask.filter(ImageFilter.MaxFilter(5))
        img.paste(INK, (0, 0), edge)
        img.paste(cloud, (0, 0), mask)
    # distant hills
    hill = (150, 120, 150) if p['sunset'] else ((60, 60, 90) if p['night'] else (190, 160, 120))
    pts = [(0, hor)] + [(x, hor - 40 * S - 30 * S * math.sin(x / (180 * S) + p['seed'])) for x in range(0, Wb + 40, 40)] + [(Wb, hor + 10)]
    d.polygon(pts + [(Wb, Hb), (0, Hb)], fill=hill)
    if p['pyramids']:
        base = hor + 10 * S
        for i, (px, ph) in enumerate(((0.62, 230), (0.74, 200), (0.83, 120))):
            x = Wb * px; hh = ph * S
            col = (205, 160, 100) if not p['night'] else (80, 70, 90)
            d.polygon([(x - hh, base), (x, base - hh), (x + hh, base)], fill=col, outline=INK)
            d.polygon([(x, base - hh), (x + hh, base), (x + hh * 0.2, base)], fill=tuple(int(c * 0.8) for c in col), outline=INK)
    if p['buildings']:
        base = hor + 20 * S
        for i in range(3):
            x = Wb * (0.18 + i * 0.1); bw = 110 * S; bh = (90 + 30 * (i % 2)) * S
            col = (225, 200, 150) if not p['night'] else (90, 80, 100)
            d.rectangle((x, base - bh, x + bw, base), fill=col, outline=INK, width=max(2, int(3 * S)))
            for c in range(4): d.line([(x + 15 * S + c * 27 * S, base - bh + 18 * S), (x + 15 * S + c * 27 * S, base)], fill=INK, width=max(2, int(3 * S)))
            d.rectangle((x - 8 * S, base - bh - 14 * S, x + bw + 8 * S, base - bh), fill=col, outline=INK, width=max(2, int(3 * S)))
    # ground
    ground = (217, 178, 107) if not p['night'] else (90, 80, 70)
    d.rectangle((0, hor + 20 * S, Wb, Hb), fill=ground)
    for _ in range(140):
        x, y = rnd.randrange(Wb), rnd.randrange(int(hor + 40 * S), Hb)
        d.line([(x, y), (x + 4 * S, y - 10 * S)], fill=(180, 140, 70), width=max(1, int(2 * S)))
    if p['river']:
        ry = hor + 90 * S
        d.polygon([(0, ry), (Wb, ry - 30 * S), (Wb, ry + 50 * S), (0, ry + 80 * S)], fill=(70, 140, 200), outline=INK)
        for k in range(10):
            x = rnd.randrange(Wb); y = ry + rnd.randint(10, 50) * S
            d.arc((x, y, x + 60 * S, y + 20 * S), 200, 340, fill=(200, 230, 250), width=max(2, int(3 * S)))
    return img

def studio_bg(p):
    rnd = np.random.default_rng(p['seed'])
    Wb, Hb = int(W * 1.04), int(H * 1.04)
    a = np.full((Hb, Wb, 3), STUDIO_GREY, np.float32)
    a += rnd.normal(0, 3, (Hb, Wb, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def art_bg(p):
    rnd = np.random.default_rng(p['seed'])
    Wb, Hb = int(W * 1.04), int(H * 1.04)
    yy, xx = np.mgrid[0:Hb, 0:Wb]
    r = np.sqrt(((xx - Wb / 2) / (Wb / 2)) ** 2 + ((yy - Hb / 2) / (Hb / 2)) ** 2)
    base = np.array([239, 224, 187], np.float32)
    a = base[None, None, :] * (1 - 0.28 * np.clip(r - 0.5, 0, 1))[..., None]
    a += rnd.normal(0, 4, (Hb, Wb, 1))
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    m = int(40 * S)
    d.rectangle((m, m, Wb - m, Hb - m), outline=(150, 110, 60), width=max(2, int(6 * S)))
    d.rectangle((m + 14 * S, m + 14 * S, Wb - m - 14 * S, Hb - m - 14 * S), outline=(150, 110, 60), width=max(1, int(2 * S)))
    return img

# ----------------------------------------------------------------------------- scene renderer
class SceneRenderer:
    def __init__(self, p, env, t0):
        self.p = p; self.env = env; self.t0 = t0
        setc = p['set']
        self.guide = Image.open(os.path.join(ASSETS, 'guide.png')).convert('RGBA')
        gh = {'STUDIO': 0.62, 'MAP': 0.46, 'SCENE': 0.40, 'ART': 0.40}[setc]
        r = H * gh / self.guide.height
        self.guide = self.guide.resize((int(self.guide.width * r), int(self.guide.height * r)), Image.LANCZOS)
        if setc == 'STUDIO': self.gpos = (int(W * 0.07), int(H * 0.30))
        elif setc == 'MAP': self.gpos = (int(W * 0.80), int(H - self.guide.height + H * 0.02))
        else: self.gpos = (int(W * 0.82), int(H - self.guide.height - H * 0.04))
        if setc == 'MAP':
            self.view = map_view(p['places'])
            self.bg = None
            self.ovl = self.make_overlay()
        else:
            self.bg = {'STUDIO': studio_bg, 'SCENE': sky_bg, 'ART': art_bg}[setc](p)
        # elements
        self.elems = []   # (appear_t, img, (x, y) centre-bottom anchor, kind)
        fh = 0.40 if len(p['chars']) <= 3 else 0.30
        chars = [draw_figure(*c, h=int(H * (fh if setc != 'SCENE' else 0.34))) for c in p['chars']]
        cards = [card_img(e, int(H * (0.17 if setc == 'STUDIO' else 0.15))) for e in p['icons']]
        pops = list(p['pop'])
        # layout
        if setc == 'STUDIO':
            xs0, xs1 = W * 0.36, W * 0.95
        elif setc == 'SCENE' or setc == 'ART':
            xs0, xs1 = W * 0.08, W * (0.78 if p['guide'] else 0.92)
        else:
            xs0, xs1 = W * 0.1, W * 0.9
        allel = [('char', c) for c in chars] + [('card', c) for c in cards]
        nc = len(chars); nk = len(cards)
        i = 0
        for k, c in enumerate(chars):
            x = xs0 + (xs1 - xs0) * (k + 0.5) / max(1, nc)
            y = H * (0.93 if setc != 'SCENE' else 0.95)
            self.elems.append((pops[i] if i < len(pops) else 0.5, c, (x, y), 'char')); i += 1
        for k, c in enumerate(cards):
            x = xs0 + (xs1 - xs0) * (k + 0.5) / max(1, nk)
            y = H * (0.56 if nc else 0.72) if setc != 'SCENE' else H * 0.58
            self.elems.append((pops[i] if i < len(pops) else 0.5, c, (x, y), 'card')); i += 1
        self.texts = []
        for s in p['segs']:
            if s['punch']:
                img = text_img(s['text'], 'bangers.ttf', 118 if len(s['text']) < 18 else 92, YELLOW, (74, 42, 16), 7, maxw=W * 0.7)
            else:
                img = text_img(s['text'], 'patrick.ttf', 66, (255, 255, 255), INK, 4, maxw=W * 0.72)
            self.texts.append((s['t'], img, s))

    def make_overlay(self):
        """full-res overlay layer (in world pixels) for the map's view area"""
        cx, cy, wpx, hpx = self.view
        z = 1.1
        self.vx0, self.vy0 = cx - wpx * z / 2, cy - hpx * z / 2
        self.vw, self.vh = wpx * z, hpx * z
        sc = W / self.vw * 1.0
        layer = Image.new('RGBA', (int(self.vw * sc), int(self.vh * sc)), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        tr = lambda lat, lon: ((ll2px(lat, lon)[0] - self.vx0) * sc, (ll2px(lat, lon)[1] - self.vy0) * sc)
        self._tr = tr
        if self.p['overlay']:
            poly = [tr(*q) for q in OVERLAYS[self.p['overlay']]]
            d.polygon(poly, fill=(226, 85, 45, 150), outline=(150, 40, 20, 220))
            d.line(poly + [poly[0]], fill=(150, 40, 20, 230), width=max(2, int(4 * S)))
        if self.p['nile']:
            pts = [tr(*q) for q in NILE]
            if self.p['nile_glow']:
                glow = Image.new('RGBA', layer.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
                gd.line(pts, fill=(90, 220, 90, 200), width=max(6, int(26 * S)), joint='curve')
                gd.polygon([tr(*q) for q in DELTA], fill=(90, 220, 90, 170))
                glow = glow.filter(ImageFilter.GaussianBlur(6 * S))
                layer.alpha_composite(glow)
                d.line(pts, fill=(40, 150, 60, 255), width=max(3, int(8 * S)), joint='curve')
            else:
                d.line(pts, fill=(60, 150, 70, 200), width=max(2, int(5 * S)), joint='curve')
                d.polygon([tr(*q) for q in DELTA], fill=(80, 170, 80, 110))
        self.ovl_scale = sc
        self.pins = []
        for name in self.p['places']:
            if name in ('EGYPT',): continue
            x, y = tr(*PLACES[name])
            if 0 <= x < layer.width and 0 <= y < layer.height:
                self.pins.append((name, x, y))
        return layer

    def frame(self, t):
        p = self.p; setc = p['set']; dur = p['dur']
        prog = t / max(dur, 0.01)
        if setc == 'MAP':
            z = 1.1 - 0.08 * prog
            cx, cy, wpx, hpx = self.view
            vw, vh = wpx * z, hpx * z
            x0, y0 = cx - vw / 2, cy - vh / 2
            wl = world()
            box = (int(x0), int(y0), int(x0 + vw), int(y0 + vh))
            img = wl.crop(box).resize((W, H), Image.BILINEAR).convert('RGBA')
            # overlay layer is in the z=1.1 frame; map it to current zoom
            s = 1.1 / z
            ow, oh = int(W * s), int(H * s)
            ox = int((self.vx0 - x0) / vw * W); oy = int((self.vy0 - y0) / vh * H)
            ol = self.ovl.resize((ow, oh), Image.BILINEAR)
            # overlay grows in
            if p['overlay'] and t < 1.2:
                a = ol.split()[3].point(lambda v: int(v * min(1, t / 1.2)))
                ol.putalpha(a)
            img.alpha_composite(ol, (ox, oy))
            d = ImageDraw.Draw(img)
            pins = []
            for k, (name, px, py) in enumerate(self.pins):
                at = 0.4 + k * 0.5
                if t < at: continue
                X = ox + px * s; Y = oy + py * s
                pins.append((name, X, Y))
                r = 11 * S * min(1, ease_pop(t - at))
                d.ellipse((X - r, Y - r, X + r, Y + r), fill=(230, 50, 40), outline=(255, 255, 255), width=max(2, int(3 * S)))
            if p['arrow'] and len(pins) >= 2:
                (n0, ax, ay), (n1, bx, by) = pins[0], pins[1]
                k = min(1, max(0, (t - 0.9) / 1.6))
                if k > 0:
                    mx, my = (ax + bx) / 2 - (by - ay) * 0.2, (ay + by) / 2 + (bx - ax) * 0.2
                    pts = [((1 - u) ** 2 * ax + 2 * (1 - u) * u * mx + u * u * bx, (1 - u) ** 2 * ay + 2 * (1 - u) * u * my + u * u * by) for u in np.linspace(0, k, 30)]
                    d.line(pts, fill=(255, 255, 255), width=max(3, int(9 * S)), joint='curve')
                    d.line(pts, fill=(226, 60, 40), width=max(2, int(5 * S)), joint='curve')
                    if k >= 1:
                        (x1, y1), (x2, y2) = pts[-2], pts[-1]
                        ang = math.atan2(y2 - y1, x2 - x1); L = 26 * S
                        d.polygon([(x2, y2), (x2 - L * math.cos(ang - 0.45), y2 - L * math.sin(ang - 0.45)),
                                   (x2 - L * math.cos(ang + 0.45), y2 - L * math.sin(ang + 0.45))], fill=(226, 60, 40), outline=(255, 255, 255))
                    if p['boat']:
                        bxp, byp = pts[-1]
                        e = emoji_img('⛵', int(64 * S))
                        img.alpha_composite(e, (int(bxp - e.width / 2), int(byp - e.height)))
            if p['boat'] and not (p['arrow'] and len(pins) >= 2):
                pts = [(ox + self._tr(*q)[0] * s, oy + self._tr(*q)[1] * s) for q in NILE[6:]]
                u = (math.sin(t / max(dur, 1) * math.pi * 2 - math.pi / 2) + 1) / 2   # north then back south
                fpos = u * (len(pts) - 1); i0 = min(int(fpos), len(pts) - 2); fr = fpos - i0
                bx = pts[i0][0] * (1 - fr) + pts[i0 + 1][0] * fr; by = pts[i0][1] * (1 - fr) + pts[i0 + 1][1] * fr
                e = emoji_img('⛵', int(110 * S))
                img.alpha_composite(e, (int(bx - e.width / 2), int(by - e.height * 0.9)))
            for name, X, Y in pins:
                lab = self._label(name)
                img.alpha_composite(lab, (int(X - lab.width / 2), int(Y - lab.height - 14 * S)))
        else:
            bg = self.bg
            mx, my = bg.width - W, bg.height - H
            img = bg.crop((int(mx * prog), int(my * 0.5), int(mx * prog) + W, int(my * 0.5) + H)).convert('RGBA')
        # elements
        for at, el, (x, y), kind in self.elems:
            if t < at: continue
            e = ease_pop(t - at)
            if e <= 0: continue
            im = el if abs(e - 1) < 0.01 else el.resize((max(1, int(el.width * e)), max(1, int(el.height * e))), Image.BILINEAR)
            bob = math.sin((t + at) * 2.2) * 4 * S if kind == 'card' else 0
            img.alpha_composite(im, (int(x - im.width / 2), int(y - im.height + bob)))
        if p['xstamp']:
            st = dur * 0.55
            for k, (at, el, (x, y), kind) in enumerate(self.elems):
                ts = max(st + k * 0.18, at + 0.3)
                if t >= ts:
                    d = ImageDraw.Draw(img); r = 70 * S * min(1, ease_pop(t - ts))
                    cy = y - el.height * 0.45
                    d.line([(x - r, cy - r), (x + r, cy + r)], fill=(220, 40, 40), width=max(4, int(16 * S)))
                    d.line([(x + r, cy - r), (x - r, cy + r)], fill=(220, 40, 40), width=max(4, int(16 * S)))
        # guide
        if p['guide']:
            fi = int((self.t0 + t) * FPS)
            amp = self.env[fi] if 0 <= fi < len(self.env) else 0
            bob = -amp * 10 * S + math.sin(t * 2.0) * 3 * S
            img.alpha_composite(self.guide, (self.gpos[0], int(self.gpos[1] + bob)))
        # text
        cur = [tx for tx in self.texts if t >= tx[0]]
        if cur:
            at, timg, s = cur[-1]
            e = ease_pop(t - at)
            im = timg if abs(e - 1) < 0.01 else timg.resize((max(1, int(timg.width * e)), max(1, int(timg.height * e))), Image.BILINEAR)
            if s['punch']:
                cx = W * (0.62 if setc == 'STUDIO' else 0.5); cy = H * 0.2
            else:
                cx = W * (0.6 if setc == 'STUDIO' else 0.5); cy = H * 0.12
            img.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
        return img.convert('RGB')

    _lc = {}
    def _label(self, name):
        if name not in self._lc:
            self._lc[name] = text_img(name, 'patrick.ttf', 44, (255, 255, 255), INK, 3)
        return self._lc[name]

# ----------------------------------------------------------------------------- driver
def render_scene(args):
    sn, v, start, end, env, f0, nf = args
    path = os.path.join(OUT, 'seg', f'{sn:03d}.mp4')
    if os.path.exists(path) and os.path.getsize(path) > 1000: return path
    p = plan_scene(sn, v, end - start)
    r = SceneRenderer(p, env, start)
    cmd = ['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', path + '.tmp.mp4']
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(nf):
        pr.stdin.write(r.frame(k / FPS).tobytes())
    pr.stdin.close(); pr.wait()
    os.replace(path + '.tmp.mp4', path)
    return path

def sfx_track(plans, starts, total, sr=22050):
    """little pop sounds when cards/characters/text appear"""
    out = np.zeros(int(total * sr) + sr, np.float32)
    n = int(0.07 * sr); tt = np.arange(n) / sr
    pop = (np.sin(2 * np.pi * (900 - 4000 * tt) * tt) * np.exp(-tt * 45)).astype(np.float32) * 0.18
    for p, st in zip(plans, starts):
        times = list(p['pop'][: len(p['chars']) + len(p['icons'])]) + [s['t'] for s in p['segs']]
        for t in times:
            i = int((st + t) * sr)
            if 0 <= i < len(out) - n: out[i:i + n] += pop
    return out, sr

def main():
    vis = load_visuals()
    tim = json.load(open(os.path.join(OUT, 'timing.json')))
    scenes = tim['scenes']; env = tim['envelope']
    first, last = 1, len(scenes)
    if len(sys.argv) >= 3: first, last = int(sys.argv[1]), int(sys.argv[2])
    os.makedirs(os.path.join(OUT, 'seg'), exist_ok=True)
    jobs = []
    for sn in range(first, last + 1):
        s = scenes[sn - 1]
        f0 = round(s['start'] * FPS); f1 = round(s['end'] * FPS)
        jobs.append((sn, vis[sn], s['start'], s['end'], env, f0, f1 - f0))
    with Pool(int(os.environ.get('WORKERS', os.cpu_count() or 2))) as pool:
        for k, path in enumerate(pool.imap(render_scene, jobs), 1):
            print(f'scene {jobs[k - 1][0]} done', flush=True)
    # join video
    lst = os.path.join(OUT, 'segments.txt')
    with open(lst, 'w') as f:
        for j in jobs: f.write(f"file 'seg/{j[0]:03d}.mp4'\n")
    t0 = scenes[first - 1]['start']; t1 = scenes[last - 1]['end']
    plans = [plan_scene(j[0], j[1], j[3] - j[2]) for j in jobs]
    sfx, sr = sfx_track(plans, [j[2] - t0 for j in jobs], t1 - t0)
    with wave.open(os.path.join(OUT, 'sfx.wav'), 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        wf.writeframes((np.clip(sfx, -1, 1) * 32767).astype(np.int16).tobytes())
    name = os.environ.get('NAME', 'Why_Egypt_Never_Died.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
                    '-ss', f'{t0:.3f}', '-t', f'{t1 - t0:.3f}', '-i', os.path.join(OUT, 'narration.wav'),
                    '-i', os.path.join(OUT, 'sfx.wav'),
                    '-filter_complex', '[1:a]volume=1.0[v];[2:a]volume=0.6[s];[v][s]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5[a]',
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart',
                    os.path.join(OUT, name)], check=True)
    print('wrote', os.path.join(OUT, name))

if __name__ == '__main__':
    main()
