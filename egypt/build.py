"""Builds the production files from chunks.json (voice lines) + visuals.txt (visual plan)."""
import json, csv, re
import spoken

RATE = 4.03  # spoken syllables per second  (~158 words per minute, matches the reference narrator)

chunks = json.load(open('chunks.json'))
vis = {}
for line in open('visuals.txt'):
    if not re.match(r'^\d+ \|', line):
        continue
    n, setc, visual, text, cam, sfx = [p.strip() for p in line.split(' | ')]
    vis[int(n)] = dict(set=setc, visual=visual, text=text, cam=cam, sfx=sfx)
assert len(chunks) == len(vis) == 132

SET_NAMES = {
    'MAP': 'A · Satellite map',
    'STUDIO': 'B · Grey studio',
    'SCENE': 'C · Illustrated world',
    'ART': 'D · Artefact / relief close-up',
}
SET_PROMPT = {
    'MAP': 'realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height',
    'STUDIO': 'plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds',
    'SCENE': 'flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters',
    'ART': 'close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette',
}
STYLE = ('Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, '
         'simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, '
         '16:9, 1920x1080, no photorealism, no 3D')

def mmss(t):
    return f'{t // 60:02d}:{t % 60:02d}'

def tts_text(s):
    # clean voice text: paragraph break -> longer pause tag
    return s.replace(' // ', ' ... ')

def pace(syl):
    sec = syl / RATE
    if sec > 11.0:
        note = 'Dense line: do NOT speed up. Let it run to ~{:.1f}s and hold the picture until the line ends.'.format(sec)
    elif sec < 9.0:
        note = 'Light line: keep the same speed; leave a ~{:.1f}s beat of music at the end.'.format(10 - sec)
    else:
        note = 'Normal pace.'
    return sec, note

BATCH = 10
batches = [list(range(i, i + BATCH)) for i in range(1, 121, BATCH)] + [list(range(121, 133))]

# ---------------- Markdown ----------------
md = []
w = md.append
w('# Why Egypt Never Died: Scene-by-Scene Production Script\n')
w('**Format:** 16:9, 1920×1080, 24 fps · **Scenes:** 132 × 10 s · **Runtime:** ≈ 22 min · '
  '**Narration pace:** locked at ≈ 155–160 words per minute (the same pace as the reference video)\n')
w('> The script you sent stops mid-sentence (*"Octavian, now Emperor Augustus, kept Egypt as his personal…"*). '
  'Scene 132 ends on that line. Send the rest and the next batch continues from Scene 133 in the same format.\n')

w('## 1. Visual style bible (from the reference video)\n')
w('What the reference video does, and what every scene below follows:\n')
w('| Element | Rule |')
w('|---|---|')
w('| Art style | Flat 2D vector cartoon. Thin dark-brown outlines, flat colours, almost no shading. People are round-headed stick figures with dot eyes and thin stick limbs. |')
w('| Frame | 16:9 picture. Keep important things inside the centre 90% (the reference is shown pillar-boxed). |')
w('| Set A: satellite map | Realistic satellite Earth (green/brown land, deep blue sea). Empires are flat red/orange overlays that grow or shrink. Labels are white hand-lettered caps. The Guide stands in the **bottom-right corner**, knees up, and talks to camera. |')
w('| Set B: grey studio | Plain light-grey background. The Guide stands **full-body in the left third**. Icons, flash cards, stick-figure rulers and red X stamps pop in on the right. |')
w('| Set C: illustrated world | Simple cartoon landscapes: blue sky with puffy white clouds for normal beats, orange-to-purple sunset with pink clouds for dramatic/intro beats. Flat desert, river, buildings. |')
w('| Set D: artefact close-up | A papyrus, stone relief or clay tablet, redrawn in the same cartoon line style (not a photo). Use for quotes, documents and inscriptions. |')
w('| Text | Two kinds only. (1) **Labels:** white, hand-lettered, all caps, thin dark shadow. (2) **Punch words / numbers:** big bold **yellow comic lettering with a dark-brown outline**, slammed in (e.g. "THE CRAZY PART" in the reference). Numbers count up like a ticker. |')
w('| Motion | Gentle, constant: slow push-ins and pans on maps; elements **pop** in with a small overshoot bounce; red X **stamps**; arrows **draw** themselves. One new idea on screen roughly every 2–3 seconds. |')
w('| Cuts | Hard cuts or quick whooshes between scenes, cut on the voice. No fancy transitions. |')
w('| Music & SFX | Soft, low ambient/orchestral bed under the whole video (about −22 dB under the voice); small cartoon SFX for pops, stamps and whooshes. |')
w('| Palette | Sand #D9B26B · Desert brown #A9773E · Nile blue #3A7CC3 · Black-land mud #3B2F2A · Field green #7FAF4E · Empire red #E2552D · Sky #9CCBEA · Sunset #F2994A → #6C4F8C · Studio grey #C9C9C9 · Text yellow #F6C934 |')
w('')
w('Reference contact sheets: `reference_frames/reference_contact_sheet_1.png`, `reference_frames/reference_contact_sheet_2.png`\n')

w('## 2. The Guide: your character (same in every scene)\n')
w('![The Guide](character_reference.png)\n')
w('The reference video already uses a narrator character with this exact design, so **your character replaces it as the on-screen narrator for the whole video.**\n')
w('**Fixed design (never change):**')
w('- Brown wide-brim hat with a darker brown band; **one red feather** standing up from the band on the left side of the hat.')
w('- Messy brown hair under the hat, round peach face, rosy cheeks, black dot eyes, small smile.')
w('- Ragged mustard-yellow one-shoulder tunic (over his right shoulder), bare middle, ragged yellow skirt, thin rope belt.')
w('- Thin dark-brown stick arms and legs, small rounded dark-brown hands and feet.')
w('- Always holds his **wooden spear with a grey stone/metal leaf-shaped head tied with rope**, in the hand on the viewer\'s left.')
w('')
w('**Rules:**')
w('- Draw him in the same flat, clean-line style as the rest of the video (match the reference). Your image is softer and watercolour-like, so either redraw him with clean lines or apply that watercolour texture to the **whole** video, not just to him.')
w('- Same size per set: map scenes = bottom-right, ~40% of frame height; studio scenes = left third, ~55% height; world scenes = small, inside the scene.')
w('- His mouth opens and closes while the voice speaks (2–3 mouth shapes are enough). Default pose: one hand on the spear, the other hand gesturing or on his hip.')
w('- Reactions used in the plan: point with spear, shrug, raise eyebrow, hat tips back in surprise, hand on chin, thumbs up, eye-roll.')
w('- AI tools: always attach `character_reference.png` as the character reference image and use the same seed/character ID for every scene.\n')
w('**Character prompt (paste into every image prompt that includes him):**\n')
w('> the Guide: a small cartoon boy explorer, round peach face, rosy cheeks, black dot eyes, gentle smile, messy brown hair, brown wide-brim hat with a dark band and one tall red feather, ragged mustard-yellow one-shoulder tunic and ragged skirt with rope belt, thin dark-brown stick arms and legs, holding a tall wooden spear with a grey leaf-shaped stone head tied with rope\n')

w('## 3. Voice direction (same in every batch)\n')
w('| Setting | Value |')
w('|---|---|')
w('| Voice | One narrator for the whole video. Warm, clear, curious storyteller; mid-low pitch; friendly and confident, like explaining to a smart friend. Not dramatic movie-trailer, not flat news-reader. |')
w('| Speed | **≈ 155–160 words per minute**, about 4 syllables per second. Never speed up to fit 10 seconds. Let the picture wait for the voice. |')
w('| Pauses | Comma ≈ 0.25 s · full stop ≈ 0.5 s · `...` (new paragraph) ≈ 0.9 s · before a big reveal ≈ 0.7 s |')
w('| Emphasis | Lean slightly on numbers, dates and the key word of each line (shown in the on-screen text column). Questions go up at the end. |')
w('| Energy | Keep it level across all batches. The hook (Scenes 1–3) can be 5% brighter; collapse and death beats 5% softer, same speed. |')
w('| TTS settings (e.g. ElevenLabs) | Same voice and model for every batch · Stability 50% · Similarity 75% · Style 10% · Speaker boost on · Speed 1.0. Generate one batch (10 scenes) per take, and paste the last sentence of the previous batch as "previous text" so the tone carries on. |')
w('| Recording yourself | Same mic, room and distance every session; read a whole batch in one take; do a 10-second "warm-up" read of the previous batch\'s last line first. |')
w('| Mix | Voice peaks around −6 dB, music −22 dB under the voice, SFX −14 dB. |')
w('')
w('**Pronunciation guide**\n')
pron = [('Kemet', 'KEH-met'), ('Deshret', 'DESH-ret'), ('Nilometer', 'ny-LOM-eh-ter'), ('Menes', 'MEH-neez'), ('Narmer', 'NAR-mer'),
        ('vizier', 'viz-EER'), ('Osiris', 'oh-SY-ris'), ('Isis', 'EYE-sis'), ("Ma'at", 'mah-AHT'), ('mastaba', 'MAS-tuh-buh'),
        ('Djoser', 'JOE-ser'), ('Imhotep', 'im-HOE-tep'), ('Sneferu', 'sneh-FEH-roo'), ('Khufu', 'KOO-foo'), ('Khafre', 'KAF-ray'),
        ('Menkaure', 'men-KOW-ray'), ('Merer', 'MEH-rer'), ('Tura', 'TOO-rah'), ('Pepi', 'PEH-pee'), ('Mentuhotep', 'men-too-HOE-tep'),
        ('Faiyum', 'fy-YOOM'), ('Nubia', 'NOO-bee-uh'), ('Levant', 'leh-VANT'), ('Avaris', 'AV-uh-ris'), ('Hyksos', 'HICK-soss'),
        ('Seqenenre', 'sek-en-EN-ray'), ('Kush', 'KOOSH'), ('Kamose', 'KAH-moze'), ('Ahmose', 'AH-moze'), ('Canaan', 'KAY-nun'),
        ('Amun', 'AH-mun'), ('Karnak', 'KAR-nak'), ('Thutmose', 'thoot-MOE-seh'), ('Euphrates', 'yoo-FRAY-teez'), ('Hatshepsut', 'hat-SHEP-soot'),
        ('Punt', 'POONT'), ('Deir el-Bahari', 'DAIR el-buh-HAR-ee'), ('Megiddo', 'meh-GID-oh'), ('Amenhotep', 'ah-men-HOE-tep'), ('Amarna', 'uh-MAR-nuh'),
        ('Aten', 'AH-ten'), ('Akhenaten', 'ah-ken-AH-ten'), ('Nefertiti', 'nef-er-TEE-tee'), ('Tutankhamun', 'too-tan-KAH-moon'), ('Horemheb', 'HOR-em-heb'),
        ('Carnarvon', 'kar-NAR-vun'), ('Ramesses', 'RAM-eh-seez'), ('Pi-Ramesses', 'pee-RAM-eh-seez'), ('Abu Simbel', 'AH-boo SIM-bel'), ('Kadesh', 'KAY-desh'),
        ('Hittite', 'HIT-ite'), ('Piye', 'PEE-yeh'), ('Psamtik', 'SAM-tik'), ('Necho', 'NEE-koe'), ('Nebuchadnezzar', 'neb-yoo-kud-NEZ-er'),
        ('Carchemish', 'KAR-keh-mish'), ('Cambyses', 'kam-BY-seez'), ('Pelusium', 'peh-LOO-see-um'), ('Darius', 'duh-RY-us'), ('Nectanebo', 'nek-tuh-NEE-boe'),
        ('Siwa', 'SEE-wah'), ('Ptolemy', 'TOL-eh-mee'), ('Edfu', 'ED-foo'), ('Dendera', 'den-DEH-ruh'), ('Demotic', 'deh-MOT-ik'),
        ('Plutarch', 'PLOO-tark'), ('Caesarion', 'see-ZAIR-ee-on'), ('Actium', 'AK-tee-um'), ('Octavian', 'ok-TAY-vee-un')]
w('| Word | Say | Word | Say | Word | Say |')
w('|---|---|---|---|---|---|')
for i in range(0, len(pron), 3):
    row = pron[i:i + 3] + [('', '')] * (3 - len(pron[i:i + 3]))
    w('| ' + ' | '.join(f'{a} | {b}' for a, b in row) + ' |')
w('')
w('Numbers: read years as "twenty-five sixty B C", Roman numerals as "Thutmose **the Third**", "Ptolemy **the Fifth**", "Cleopatra **the Seventh**".\n')

w('## 4. Batch overview\n')
w('| Batch | Scenes | Time | Chapter |')
w('|---|---|---|---|')
chapters = ['The hook and the Nile', 'Unification, gods and the god-king', 'The first pyramids', 'Pyramid builders and the first collapse',
            'The Middle Kingdom', 'The Hyksos and the fight back', 'The New Kingdom and Hatshepsut',
            'Thutmose III and Akhenaten', 'Tutankhamun', 'Ramesses II',
            'Bronze Age collapse and outsiders', 'Persia and Alexander', 'The Ptolemies and Cleopatra']
for bi, b in enumerate(batches):
    w(f'| {bi + 1} | {b[0]}–{b[-1]} | {mmss((b[0] - 1) * 10)}–{mmss(b[-1] * 10)} | {chapters[bi]} |')
w('')

w('## 5. Scenes\n')
w('How to read each scene: **VO** is the exact voice line. **Visual** is what we see and what the Guide does. '
  '**On-screen text** uses `/` to separate separate text pops (in order). **Pace** gives the estimated voice length at the locked speed. '
  '**AI prompt** is ready to paste into an image/video generator together with `character_reference.png`.\n')

rows = []
for bi, b in enumerate(batches):
    w(f'### Batch {bi + 1}: {chapters[bi]} (Scenes {b[0]}–{b[-1]}, {mmss((b[0] - 1) * 10)}–{mmss(b[-1] * 10)})\n')
    for n in b:
        v = vis[n]
        vo = chunks[n - 1]
        words, syl = spoken.stats(vo)
        sec, note = pace(syl)
        start, end = (n - 1) * 10, n * 10
        guide = '' if 'Guide' in v['visual'] else ' The Guide is not in this shot.'
        prompt = (f"{STYLE}. Setting: {SET_PROMPT[v['set']]}. Scene: {v['visual']}"
                  + (" Include the Guide exactly as in the character reference." if 'Guide' in v['visual'] else '')
                  + f" Text in frame: {v['text']}.")
        motion = f"{v['cam']}. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds."
        w(f'#### Scene {n:03d} · {mmss(start)}–{mmss(end)} · {SET_NAMES[v["set"]]}\n')
        w(f'**VO:** "{vo.replace(" // ", " … ")}"\n')
        w(f'- **Visual:** {v["visual"]}{guide}')
        w(f'- **On-screen text:** {v["text"]}')
        w(f'- **Camera / animation:** {v["cam"]}')
        w(f'- **SFX / music:** {v["sfx"]}')
        w(f'- **Pace:** {words} spoken words · ≈ {sec:.1f} s at locked speed. {note}')
        w(f'- **AI image prompt:** `{prompt}`')
        w(f'- **AI motion prompt:** `{motion}`\n')
        rows.append(dict(scene=n, start=mmss(start), end=mmss(end), set=SET_NAMES[v['set']], voice_line=vo.replace(' // ', ' … '),
                         visual=v['visual'], on_screen_text=v['text'], camera=v['cam'], sfx=v['sfx'],
                         est_voice_seconds=f'{sec:.1f}', image_prompt=prompt, motion_prompt=motion))
    w(f'**Batch {bi + 1} consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · '
      'labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.\n')

open('Egypt_Video_Production_Script.md', 'w').write('\n'.join(md))

with open('scenes.csv', 'w', newline='') as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    wr.writeheader(); wr.writerows(rows)

# clean voiceover script for TTS / recording, batched
vo = ['WHY EGYPT NEVER DIED: VOICEOVER SCRIPT',
      'One voice, same settings for every batch. Speed about 155-160 words per minute. "..." = paragraph pause (about 0.9 s).', '']
for bi, b in enumerate(batches):
    vo.append(f'===== BATCH {bi + 1}: {chapters[bi]} (Scenes {b[0]}-{b[-1]}) =====')
    for n in b:
        vo.append(f'[{n:03d} | {mmss((n - 1) * 10)}] {tts_text(chunks[n - 1])}')
    vo.append('')
open('voiceover_script.txt', 'w').write('\n'.join(vo))

# subtitle / timing guide (nominal 10 s slots)
srt = []
for n in range(1, 133):
    a, b2 = (n - 1) * 10, n * 10
    srt.append(f'{n}\n00:{a // 60:02d}:{a % 60:02d},000 --> 00:{b2 // 60:02d}:{b2 % 60:02d},000\n{chunks[n - 1].replace(" // ", " ")}\n')
open('scene_timing.srt', 'w').write('\n'.join(srt))
print('ok')
