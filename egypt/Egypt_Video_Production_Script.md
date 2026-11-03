# Why Egypt Never Died: Scene-by-Scene Production Script

**Format:** 16:9, 1920×1080, 24 fps · **Scenes:** 163 (6–10 s each, average 8 s) · **Runtime:** ≈ 22.0 min · **Narration pace:** locked at ≈ 155–160 words per minute (the same pace as the reference video)

> The script you sent stops mid-sentence (*"Octavian, now Emperor Augustus, kept Egypt as his personal…"*). Scene 163 ends on that line. Send the rest and the next batch continues from Scene 164 in the same format.

## 1. Visual style bible (from the reference video)

What the reference video does, and what every scene below follows:

| Element | Rule |
|---|---|
| Art style | Flat 2D vector cartoon. Thin dark-brown outlines, flat colours, almost no shading. People are round-headed stick figures with dot eyes and thin stick limbs. |
| Frame | 16:9 picture. Keep important things inside the centre 90% (the reference is shown pillar-boxed). |
| Set A: satellite map | Realistic satellite Earth (green/brown land, deep blue sea). Empires are flat red/orange overlays that grow or shrink. Labels are white hand-lettered caps. The Guide stands in the **bottom-right corner**, knees up, and talks to camera. |
| Set B: grey studio | Plain light-grey background. The Guide stands **full-body in the left third**. Icons, flash cards, stick-figure rulers and red X stamps pop in on the right. |
| Set C: illustrated world | Simple cartoon landscapes: blue sky with puffy white clouds for normal beats, orange-to-purple sunset with pink clouds for dramatic/intro beats. Flat desert, river, buildings. |
| Set D: artefact close-up | A papyrus, stone relief or clay tablet, redrawn in the same cartoon line style (not a photo). Use for quotes, documents and inscriptions. |
| Text | Two kinds only. (1) **Labels:** white, hand-lettered, all caps, thin dark shadow. (2) **Punch words / numbers:** big bold **yellow comic lettering with a dark-brown outline**, slammed in (e.g. "THE CRAZY PART" in the reference). Numbers count up like a ticker. |
| Motion | Gentle, constant: slow push-ins and pans on maps; elements **pop** in with a small overshoot bounce; red X **stamps**; arrows **draw** themselves. One new idea on screen roughly every 2–3 seconds. |
| Pace of cuts | The reference changes picture about every 4–5 s (22 cuts in 102 s). Here each scene is 6–10 s with 2–3 visual beats inside it, so the screen changes every 3–5 s, like the reference. |
| Cuts | Hard cuts or quick whooshes between scenes, cut on the voice. No fancy transitions. |
| Music & SFX | Soft, low ambient/orchestral bed under the whole video (about −22 dB under the voice); small cartoon SFX for pops, stamps and whooshes. |
| Palette | Sand #D9B26B · Desert brown #A9773E · Nile blue #3A7CC3 · Black-land mud #3B2F2A · Field green #7FAF4E · Empire red #E2552D · Sky #9CCBEA · Sunset #F2994A → #6C4F8C · Studio grey #C9C9C9 · Text yellow #F6C934 |

Reference contact sheets: `reference_frames/reference_contact_sheet_1.png`, `reference_frames/reference_contact_sheet_2.png`

## 2. The Guide: your character (same in every scene)

![The Guide](character_reference.png)

The reference video already uses a narrator character with this exact design, so **your character replaces it as the on-screen narrator for the whole video.**

**Fixed design (never change):**
- Brown wide-brim hat with a darker brown band; **one red feather** standing up from the band on the left side of the hat.
- Messy brown hair under the hat, round peach face, rosy cheeks, black dot eyes, small smile.
- Ragged mustard-yellow one-shoulder tunic (over his right shoulder), bare middle, ragged yellow skirt, thin rope belt.
- Thin dark-brown stick arms and legs, small rounded dark-brown hands and feet.
- Always holds his **wooden spear with a grey stone/metal leaf-shaped head tied with rope**, in the hand on the viewer's left.

**Rules:**
- Draw him in the same flat, clean-line style as the rest of the video (match the reference). Your image is softer and watercolour-like, so either redraw him with clean lines or apply that watercolour texture to the **whole** video, not just to him.
- Same size per set: map scenes = bottom-right, ~40% of frame height; studio scenes = left third, ~55% height; world scenes = small, inside the scene.
- His mouth opens and closes while the voice speaks (2–3 mouth shapes are enough). Default pose: one hand on the spear, the other hand gesturing or on his hip.
- Reactions used in the plan: point with spear, shrug, raise eyebrow, hat tips back in surprise, hand on chin, thumbs up, eye-roll.
- AI tools: always attach `character_reference.png` as the character reference image and use the same seed/character ID for every scene.

**Character prompt (paste into every image prompt that includes him):**

> the Guide: a small cartoon boy explorer, round peach face, rosy cheeks, black dot eyes, gentle smile, messy brown hair, brown wide-brim hat with a dark band and one tall red feather, ragged mustard-yellow one-shoulder tunic and ragged skirt with rope belt, thin dark-brown stick arms and legs, holding a tall wooden spear with a grey leaf-shaped stone head tied with rope

## 3. Voice direction (same in every batch)

| Setting | Value |
|---|---|
| Voice | One narrator for the whole video. Warm, clear, curious storyteller; mid-low pitch; friendly and confident, like explaining to a smart friend. Not dramatic movie-trailer, not flat news-reader. |
| Speed | **≈ 155–160 words per minute**, about 4 syllables per second. Never speed up or slow down to fit a scene: each scene's length comes from the voice line, not the other way round. |
| Pauses | Comma ≈ 0.25 s · full stop ≈ 0.5 s · `...` (new paragraph) ≈ 0.9 s · before a big reveal ≈ 0.7 s |
| Emphasis | Lean slightly on numbers, dates and the key word of each line (shown in the on-screen text column). Questions go up at the end. |
| Energy | Keep it level across all batches. The hook (Scenes 1–3) can be 5% brighter; collapse and death beats 5% softer, same speed. |
| TTS settings (e.g. ElevenLabs) | Same voice and model for every batch · Stability 50% · Similarity 75% · Style 10% · Speaker boost on · Speed 1.0. Generate one batch (one chapter, 9–17 scenes) per take, and paste the last sentence of the previous batch as "previous text" so the tone carries on. |
| Recording yourself | Same mic, room and distance every session; read a whole batch in one take; do a 10-second "warm-up" read of the previous batch's last line first. |
| Mix | Voice peaks around −6 dB, music −22 dB under the voice, SFX −14 dB. |

**Pronunciation guide**

| Word | Say | Word | Say | Word | Say |
|---|---|---|---|---|---|
| Kemet | KEH-met | Deshret | DESH-ret | Nilometer | ny-LOM-eh-ter |
| Menes | MEH-neez | Narmer | NAR-mer | vizier | viz-EER |
| Osiris | oh-SY-ris | Isis | EYE-sis | Ma'at | mah-AHT |
| mastaba | MAS-tuh-buh | Djoser | JOE-ser | Imhotep | im-HOE-tep |
| Sneferu | sneh-FEH-roo | Khufu | KOO-foo | Khafre | KAF-ray |
| Menkaure | men-KOW-ray | Merer | MEH-rer | Tura | TOO-rah |
| Pepi | PEH-pee | Mentuhotep | men-too-HOE-tep | Faiyum | fy-YOOM |
| Nubia | NOO-bee-uh | Levant | leh-VANT | Avaris | AV-uh-ris |
| Hyksos | HICK-soss | Seqenenre | sek-en-EN-ray | Kush | KOOSH |
| Kamose | KAH-moze | Ahmose | AH-moze | Canaan | KAY-nun |
| Amun | AH-mun | Karnak | KAR-nak | Thutmose | thoot-MOE-seh |
| Euphrates | yoo-FRAY-teez | Hatshepsut | hat-SHEP-soot | Punt | POONT |
| Deir el-Bahari | DAIR el-buh-HAR-ee | Megiddo | meh-GID-oh | Amenhotep | ah-men-HOE-tep |
| Amarna | uh-MAR-nuh | Aten | AH-ten | Akhenaten | ah-ken-AH-ten |
| Nefertiti | nef-er-TEE-tee | Tutankhamun | too-tan-KAH-moon | Horemheb | HOR-em-heb |
| Carnarvon | kar-NAR-vun | Ramesses | RAM-eh-seez | Pi-Ramesses | pee-RAM-eh-seez |
| Abu Simbel | AH-boo SIM-bel | Kadesh | KAY-desh | Hittite | HIT-ite |
| Piye | PEE-yeh | Psamtik | SAM-tik | Necho | NEE-koe |
| Nebuchadnezzar | neb-yoo-kud-NEZ-er | Carchemish | KAR-keh-mish | Cambyses | kam-BY-seez |
| Pelusium | peh-LOO-see-um | Darius | duh-RY-us | Nectanebo | nek-tuh-NEE-boe |
| Siwa | SEE-wah | Ptolemy | TOL-eh-mee | Edfu | ED-foo |
| Dendera | den-DEH-ruh | Demotic | deh-MOT-ik | Plutarch | PLOO-tark |
| Caesarion | see-ZAIR-ee-on | Actium | AK-tee-um | Octavian | ok-TAY-vee-un |

Numbers: read years as "twenty-five sixty B C", Roman numerals as "Thutmose **the Third**", "Ptolemy **the Fifth**", "Cleopatra **the Seventh**".

## 4. Batch overview

| Batch | Scenes | Time | Chapter |
|---|---|---|---|
| 1 | 1–13 | 00:00.0–01:51.2 | The hook and the Nile |
| 2 | 14–24 | 01:51.2–03:21.4 | Unification, gods and the god-king |
| 3 | 25–33 | 03:21.4–04:31.4 | The first pyramids |
| 4 | 34–47 | 04:31.4–06:20.4 | Building the pyramids |
| 5 | 48–60 | 06:20.4–08:06.6 | Collapse and the Middle Kingdom |
| 6 | 61–72 | 08:06.6–09:41.0 | The Hyksos and the fight back |
| 7 | 73–84 | 09:41.0–11:19.7 | The New Kingdom and Hatshepsut |
| 8 | 85–100 | 11:19.7–13:32.9 | Thutmose III and Akhenaten |
| 9 | 101–112 | 13:32.9–15:10.9 | Tutankhamun |
| 10 | 113–123 | 15:10.9–16:37.1 | Ramesses II and the Bronze Age collapse |
| 11 | 124–136 | 16:37.1–18:19.5 | Strikes, outsiders and Assyria |
| 12 | 137–146 | 18:19.5–19:37.8 | Persia and Alexander |
| 13 | 147–163 | 19:37.8–21:57.6 | The Ptolemies and Cleopatra |

## 5. Scenes

How to read each scene: **VO** is the exact voice line. **Visual** is what we see and what the Guide does. **On-screen text** uses `/` between separate text pops (in order). **Length** is the scene length at the locked voice speed; cut the picture to the voice. **AI prompt** is ready to paste into an image/video generator together with `character_reference.png`.

### Batch 1: The hook and the Nile (Scenes 1–13, 00:00.0–01:51.2)

#### Scene 001 · 00:00.0–00:08.9 (8.9 s) · C · Illustrated world

**VO:** "You know the Giza pyramids. But almost nobody knows why Egypt never died after it lost its own kings for 2,300 years."

- **Visual:** Golden-hour Giza plateau: the three pyramids against an orange-to-purple sunset with pink cartoon clouds. The Guide walks in from the left, stops, points his spear at the pyramids, then turns to camera with a raised eyebrow. A small gold crown floats above Egypt and fades away on "lost its own kings".
- **On-screen text:** YOU KNOW THESE... / 2,300 YEARS
- **Camera / animation:** Slow push-in on the pyramids; "2,300 YEARS" slams in as yellow comic text
- **SFX / music:** soft desert wind, low drum hit on the number
- **Length:** 25 spoken words · 8.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Golden-hour Giza plateau: the three pyramids against an orange-to-purple sunset with pink cartoon clouds. The Guide walks in from the left, stops, points his spear at the pyramids, then turns to camera with a raised eyebrow. A small gold crown floats above Egypt and fades away on "lost its own kings". Include the Guide exactly as in the character reference. Text in frame: YOU KNOW THESE... / 2,300 YEARS.`
- **AI motion prompt:** `Slow push-in on the pyramids; "2,300 YEARS" slams in as yellow comic text. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 002 · 00:08.9–00:17.1 (8.2 s) · B · Grey studio

**VO:** "Persians, Greeks, Romans, Arabs, Turks, the British. Every one of those empires ruled Egypt, and every one of them is gone."

- **Visual:** Grey studio. The Guide stands left. Six stick-figure rulers pop in a row on the right, each in their own costume and labelled PERSIANS, GREEKS, ROMANS, ARABS, TURKS, BRITISH. On "every one of them is gone", a red X stamps over each one in quick order.
- **On-screen text:** PERSIANS · GREEKS · ROMANS · ARABS · TURKS · BRITISH / GONE
- **Camera / animation:** One pop per name; six fast stamps on "gone"
- **SFX / music:** six pops, six stamp sounds
- **Length:** 21 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio. The Guide stands left. Six stick-figure rulers pop in a row on the right, each in their own costume and labelled PERSIANS, GREEKS, ROMANS, ARABS, TURKS, BRITISH. On "every one of them is gone", a red X stamps over each one in quick order. Include the Guide exactly as in the character reference. Text in frame: PERSIANS · GREEKS · ROMANS · ARABS · TURKS · BRITISH / GONE.`
- **AI motion prompt:** `One pop per name; six fast stamps on "gone". Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 003 · 00:17.1–00:24.3 (7.2 s) · B · Grey studio

**VO:** "Egypt is still here. … The answer is in this picture. By the end of this video, you'll know exactly how it worked."

- **Visual:** The crossed-out rulers slide off. A little map of Egypt drops into the middle, untouched and glowing, with a green tick. The Guide picks up a framed picture card, still face-down, and taps it with a knowing smile.
- **On-screen text:** EGYPT IS STILL HERE / THE ANSWER IS IN THIS PICTURE
- **Camera / animation:** Egypt drops with a bounce; slow push toward the face-down card
- **SFX / music:** soft chime, card tap
- **Length:** 22 spoken words · 7.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: The crossed-out rulers slide off. A little map of Egypt drops into the middle, untouched and glowing, with a green tick. The Guide picks up a framed picture card, still face-down, and taps it with a knowing smile. Include the Guide exactly as in the character reference. Text in frame: EGYPT IS STILL HERE / THE ANSWER IS IN THIS PICTURE.`
- **AI motion prompt:** `Egypt drops with a bounce; slow push toward the face-down card. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 004 · 00:24.3–00:32.0 (7.7 s) · A · Satellite map

**VO:** "That line is the Nile. Nearly everyone in Egypt lives along it, because almost everything else is desert."

- **Visual:** The Guide flips the card and it becomes a full-screen satellite view of Egypt at night: dark desert and one thin glowing green line ending in a green fan (the delta). The Guide, bottom right, taps the line with his spear tip. Tiny people icons crowd along the green strip; the desert stays empty.
- **On-screen text:** THE NILE / NEARLY EVERYONE LIVES HERE
- **Camera / animation:** Card-flip transition; slow zoom down to the valley
- **SFX / music:** whoosh, light string swell
- **Length:** 18 spoken words · 7.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: The Guide flips the card and it becomes a full-screen satellite view of Egypt at night: dark desert and one thin glowing green line ending in a green fan (the delta). The Guide, bottom right, taps the line with his spear tip. Tiny people icons crowd along the green strip; the desert stays empty. Include the Guide exactly as in the character reference. Text in frame: THE NILE / NEARLY EVERYONE LIVES HERE.`
- **AI motion prompt:** `Card-flip transition; slow zoom down to the valley. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 005 · 00:32.0–00:40.7 (8.7 s) · A · Satellite map

**VO:** "Every summer, monsoon rains in the highlands of Ethiopia swelled the river. In Egypt, it flooded the valley for about three months,"

- **Visual:** Satellite map pans south to the Ethiopian highlands. Grey cartoon rain clouds pour rain; a blue pulse runs north down the river into Egypt. The valley fills with water; a counter shows ~3 MONTHS. The Guide, bottom right, holds his hat as the wind picks up.
- **On-screen text:** ETHIOPIA · MONSOON / FLOOD: ~3 MONTHS
- **Camera / animation:** Pan south, then follow the pulse north
- **SFX / music:** rain, rushing river
- **Length:** 22 spoken words · 8.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map pans south to the Ethiopian highlands. Grey cartoon rain clouds pour rain; a blue pulse runs north down the river into Egypt. The valley fills with water; a counter shows ~3 MONTHS. The Guide, bottom right, holds his hat as the wind picks up. Include the Guide exactly as in the character reference. Text in frame: ETHIOPIA · MONSOON / FLOOD: ~3 MONTHS.`
- **AI motion prompt:** `Pan south, then follow the pulse north. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 006 · 00:40.7–00:49.1 (8.4 s) · C · Illustrated world

**VO:** "and when the water pulled back, it left a layer of black, fertile mud. Egyptians named their country after it: Kemet, the Black Land."

- **Visual:** Cut-away view of the valley: the water slides back and leaves a thick black stripe of mud along the river. The Guide crouches, scoops the black mud and shows it to camera with a grin. The label KEMET writes itself on the black strip.
- **On-screen text:** BLACK, FERTILE MUD / KEMET = THE BLACK LAND
- **Camera / animation:** Water drains left and right; label writes itself
- **SFX / music:** squelch, label pop
- **Length:** 24 spoken words · 8.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Cut-away view of the valley: the water slides back and leaves a thick black stripe of mud along the river. The Guide crouches, scoops the black mud and shows it to camera with a grin. The label KEMET writes itself on the black strip. Include the Guide exactly as in the character reference. Text in frame: BLACK, FERTILE MUD / KEMET = THE BLACK LAND.`
- **AI motion prompt:** `Water drains left and right; label writes itself. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 007 · 00:49.1–00:58.5 (9.4 s) · C · Illustrated world

**VO:** "The desert on both sides was Deshret, the Red Land. … The Egyptian year was even built around the river. It had three seasons: Flood, Growing and Harvest."

- **Visual:** Same cut-away: the yellow desert on both sides gets the label DESHRET (RED LAND). Hard cut to the grey studio: a round calendar wheel with three slices: blue FLOOD (waves), green GROWING (sprout), gold HARVEST (wheat). The Guide points at each slice.
- **On-screen text:** DESHRET = THE RED LAND / FLOOD · GROWING · HARVEST
- **Camera / animation:** Label pop; hard cut; the wheel turns one slice per season name
- **SFX / music:** pop, three click-ticks
- **Length:** 27 spoken words · 9.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Same cut-away: the yellow desert on both sides gets the label DESHRET (RED LAND). Hard cut to the grey studio: a round calendar wheel with three slices: blue FLOOD (waves), green GROWING (sprout), gold HARVEST (wheat). The Guide points at each slice. Include the Guide exactly as in the character reference. Text in frame: DESHRET = THE RED LAND / FLOOD · GROWING · HARVEST.`
- **AI motion prompt:** `Label pop; hard cut; the wheel turns one slice per season name. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 008 · 00:58.5–01:07.2 (8.7 s) · B · Grey studio

**VO:** "Farming, taxes and festivals all followed that cycle. … That mud gave Egypt something rare in the ancient world: a reliable surplus."

- **Visual:** Small icons orbit the season wheel: a farmer's hoe, a tax scroll, a festival drum. Then the wheel slides away and a big golden grain pile rises next to the Guide with a sparkle and the word SURPLUS.
- **On-screen text:** FARMING · TAXES · FESTIVALS / A RELIABLE SURPLUS
- **Camera / animation:** Icons orbit; grain pile rises; yellow word slams in
- **SFX / music:** soft drum, grain pouring, sparkle
- **Length:** 21 spoken words · 8.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Small icons orbit the season wheel: a farmer's hoe, a tax scroll, a festival drum. Then the wheel slides away and a big golden grain pile rises next to the Guide with a sparkle and the word SURPLUS. Include the Guide exactly as in the character reference. Text in frame: FARMING · TAXES · FESTIVALS / A RELIABLE SURPLUS.`
- **AI motion prompt:** `Icons orbit; grain pile rises; yellow word slams in. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 009 · 01:07.2–01:16.6 (9.4 s) · C · Illustrated world

**VO:** "Farmers grew far more grain than they needed, and that extra grain could feed builders, soldiers, priests and officials. It paid for everything you're about to see."

- **Visual:** Bright field with cartoon clouds: a farmer holds a small bowl next to a mountain of grain sacks. Arrows run from the pile to a builder, a soldier, a priest and a scribe. Then a golden glow flies from the pile toward pyramids and temples on the horizon. The Guide nods from the side.
- **On-screen text:** FEEDS BUILDERS · SOLDIERS · PRIESTS · OFFICIALS
- **Camera / animation:** Arrows draw one by one; the glow flies to the horizon
- **SFX / music:** pop on each icon, shimmer
- **Length:** 27 spoken words · 9.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Bright field with cartoon clouds: a farmer holds a small bowl next to a mountain of grain sacks. Arrows run from the pile to a builder, a soldier, a priest and a scribe. Then a golden glow flies from the pile toward pyramids and temples on the horizon. The Guide nods from the side. Include the Guide exactly as in the character reference. Text in frame: FEEDS BUILDERS · SOLDIERS · PRIESTS · OFFICIALS.`
- **AI motion prompt:** `Arrows draw one by one; the glow flies to the horizon. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 010 · 01:16.6–01:25.0 (8.4 s) · C · Illustrated world

**VO:** "They measured the flood on stone stairways called Nilometers. A high flood meant big harvests and higher taxes. A low one meant famine."

- **Visual:** A stone stairway going down into the river with tick marks carved in the wall: a Nilometer. A scribe writes numbers. Water rises to HIGH (a fat wheat sheaf and a tax scroll pop in), then falls to LOW (the wheat wilts, an empty bowl appears). The Guide stands on the top step.
- **On-screen text:** NILOMETER / HIGH = BIG HARVEST + HIGHER TAXES / LOW = FAMINE
- **Camera / animation:** Tilt down the steps; water level rises then drops
- **SFX / music:** water lapping, scroll, sad note
- **Length:** 23 spoken words · 8.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A stone stairway going down into the river with tick marks carved in the wall: a Nilometer. A scribe writes numbers. Water rises to HIGH (a fat wheat sheaf and a tax scroll pop in), then falls to LOW (the wheat wilts, an empty bowl appears). The Guide stands on the top step. Include the Guide exactly as in the character reference. Text in frame: NILOMETER / HIGH = BIG HARVEST + HIGHER TAXES / LOW = FAMINE.`
- **AI motion prompt:** `Tilt down the steps; water level rises then drops. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 011 · 01:25.0–01:32.4 (7.4 s) · B · Grey studio

**VO:** "Keep that in mind: everything in this story rises and falls with the river. … The river was also Egypt's highway."

- **Visual:** Grey studio: a white wave line (the river level) runs across the screen behind the Guide, rising and falling. The Guide points at the camera, serious. Then the wave line morphs into a blue river with a little boat on it.
- **On-screen text:** EVERYTHING RISES AND FALLS WITH THE RIVER / EGYPT'S HIGHWAY
- **Camera / animation:** Wave line draws left to right; morph into the river
- **SFX / music:** low drone, river ambience
- **Length:** 20 spoken words · 7.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio: a white wave line (the river level) runs across the screen behind the Guide, rising and falling. The Guide points at the camera, serious. Then the wave line morphs into a blue river with a little boat on it. Include the Guide exactly as in the character reference. Text in frame: EVERYTHING RISES AND FALLS WITH THE RIVER / EGYPT'S HIGHWAY.`
- **AI motion prompt:** `Wave line draws left to right; morph into the river. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 012 · 01:32.4–01:41.8 (9.4 s) · A · Satellite map

**VO:** "The current carried boats north, and the wind usually blows from the north, so boats could sail back south. Moving grain, stone and armies along the valley was easy."

- **Visual:** Satellite map of the Nile valley. A boat icon floats north on a blue CURRENT arrow. Then a sail opens and a white WIND arrow from the north pushes it back south. Little grain sacks, stone blocks and soldiers ride boats both ways. The Guide sits on a boat at the bottom right, waving.
- **On-screen text:** CURRENT ↑ NORTH / WIND ↓ SOUTH
- **Camera / animation:** Arrows animate both ways; boats loop
- **SFX / music:** wind gust, sail flap, water
- **Length:** 29 spoken words · 9.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map of the Nile valley. A boat icon floats north on a blue CURRENT arrow. Then a sail opens and a white WIND arrow from the north pushes it back south. Little grain sacks, stone blocks and soldiers ride boats both ways. The Guide sits on a boat at the bottom right, waving. Include the Guide exactly as in the character reference. Text in frame: CURRENT ↑ NORTH / WIND ↓ SOUTH.`
- **AI motion prompt:** `Arrows animate both ways; boats loop. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 013 · 01:41.8–01:51.2 (9.4 s) · A · Satellite map

**VO:** "And the deserts on either side worked like walls. For centuries, they kept large armies out, so Egypt could grow rich without constantly defending itself."

- **Visual:** Satellite map: tall cartoon stone walls rise out of the desert on both sides of the green Nile. Tiny enemy army icons march in from east and west, bump into the walls and turn back. Inside, grain and gold stack up. The Guide leans on his spear, relaxed.
- **On-screen text:** NATURAL WALLS
- **Camera / animation:** Walls rise from the sand; armies bounce off
- **SFX / music:** stone rumble, march, bonk
- **Length:** 25 spoken words · 9.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map: tall cartoon stone walls rise out of the desert on both sides of the green Nile. Tiny enemy army icons march in from east and west, bump into the walls and turn back. Inside, grain and gold stack up. The Guide leans on his spear, relaxed. Include the Guide exactly as in the character reference. Text in frame: NATURAL WALLS.`
- **AI motion prompt:** `Walls rise from the sand; armies bounce off. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

**Batch 1 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 2: Unification, gods and the god-king (Scenes 14–24, 01:51.2–03:21.4)

#### Scene 014 · 01:51.2–01:58.6 (7.4 s) · A · Satellite map

**VO:** "Around 3100 BC, a king from the south conquered the north and united Upper and Lower Egypt."

- **Visual:** Satellite map of Egypt in two colours: the long south valley and the northern delta fan. A stick king in a tall white crown marches up from the south and plants a flag in the north; both colours merge into one. The Guide watches from bottom right.
- **On-screen text:** 3100 BC / UPPER + LOWER EGYPT UNITED
- **Camera / animation:** Colour merge wipes from south to north
- **SFX / music:** march drum, merge whoosh
- **Length:** 20 spoken words · 7.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map of Egypt in two colours: the long south valley and the northern delta fan. A stick king in a tall white crown marches up from the south and plants a flag in the north; both colours merge into one. The Guide watches from bottom right. Include the Guide exactly as in the character reference. Text in frame: 3100 BC / UPPER + LOWER EGYPT UNITED.`
- **AI motion prompt:** `Colour merge wipes from south to north. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 015 · 01:58.6–02:08.3 (9.7 s) · A · Satellite map

**VO:** "Upper Egypt was the south, because the Nile flows north. Egyptians remembered the founder as Menes; historians link him to a king called Narmer."

- **Visual:** Same map: a white arrow shows the Nile flowing north (up). The Guide taps the labels UPPER = SOUTH and LOWER = NORTH. Then a simple cartoon stone slab (the Narmer Palette) slides in with two name tags, MENES and NARMER, linked by a dotted line and a question mark.
- **On-screen text:** UPPER = SOUTH / MENES = NARMER?
- **Camera / animation:** Arrow flows north; palette slides in from the right
- **SFX / music:** map ping, pen scribble
- **Length:** 24 spoken words · 9.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Same map: a white arrow shows the Nile flowing north (up). The Guide taps the labels UPPER = SOUTH and LOWER = NORTH. Then a simple cartoon stone slab (the Narmer Palette) slides in with two name tags, MENES and NARMER, linked by a dotted line and a question mark. Include the Guide exactly as in the character reference. Text in frame: UPPER = SOUTH / MENES = NARMER?.`
- **AI motion prompt:** `Arrow flows north; palette slides in from the right. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 016 · 02:08.3–02:17.0 (8.7 s) · A · Satellite map

**VO:** "The capital, Memphis, sat where the valley meets the delta, so it could control both. … Around the same time, hieroglyphic writing appeared."

- **Visual:** Satellite map zooms to where the valley opens into the delta: a city icon MEMPHIS. Two arrows reach out to the delta and down the valley. Then a papyrus scroll unrolls across the map and hieroglyphs appear one by one (owl, reed, water line, eye). The Guide is not in this shot.
- **On-screen text:** MEMPHIS / HIEROGLYPHS
- **Camera / animation:** Zoom in; arrows draw; scroll unrolls
- **SFX / music:** ping, brush strokes
- **Length:** 22 spoken words · 8.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map zooms to where the valley opens into the delta: a city icon MEMPHIS. Two arrows reach out to the delta and down the valley. Then a papyrus scroll unrolls across the map and hieroglyphs appear one by one (owl, reed, water line, eye). Text in frame: MEMPHIS / HIEROGLYPHS.`
- **AI motion prompt:** `Zoom in; arrows draw; scroll unrolls. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 017 · 02:17.0–02:26.4 (9.4 s) · B · Grey studio

**VO:** "One of its first big jobs was running the state: recording harvests, taxes and stores, so one king could govern a country hundreds of kilometres long."

- **Visual:** Grey studio. A scribe stick figure sits cross-legged filling a scroll with tally marks next to grain, tax and storehouse icons. Below, a long Egypt map stretches across the screen with a ruler: HUNDREDS OF KM. The Guide raises an eyebrow at its length.
- **On-screen text:** RECORDING HARVESTS · TAXES · STORES / HUNDREDS OF KM
- **Camera / animation:** Tallies tick in; ruler slides along the map
- **SFX / music:** counting clicks
- **Length:** 26 spoken words · 9.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio. A scribe stick figure sits cross-legged filling a scroll with tally marks next to grain, tax and storehouse icons. Below, a long Egypt map stretches across the screen with a ruler: HUNDREDS OF KM. The Guide raises an eyebrow at its length. Include the Guide exactly as in the character reference. Text in frame: RECORDING HARVESTS · TAXES · STORES / HUNDREDS OF KM.`
- **AI motion prompt:** `Tallies tick in; ruler slides along the map. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 018 · 02:26.4–02:34.8 (8.4 s) · B · Grey studio

**VO:** "Below the king, a chief minister, the vizier, ran the government, and the country was divided into about 40 provinces,"

- **Visual:** A pyramid-shaped chart builds next to the Guide: the king at the top, the vizier (white robe, scroll) just below. Under him, a grid of 40 small province houses pops in fast.
- **On-screen text:** THE VIZIER / 40 PROVINCES
- **Camera / animation:** Chart builds top-down; cascading pops
- **SFX / music:** soft pop, cascading pops
- **Length:** 20 spoken words · 8.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: A pyramid-shaped chart builds next to the Guide: the king at the top, the vizier (white robe, scroll) just below. Under him, a grid of 40 small province houses pops in fast. Include the Guide exactly as in the character reference. Text in frame: THE VIZIER / 40 PROVINCES.`
- **AI motion prompt:** `Chart builds top-down; cascading pops. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 019 · 02:34.8–02:43.0 (8.2 s) · B · Grey studio

**VO:** "each with its own governor. Remember those governors. … Egyptians worshipped many gods tied to the world around them: Ra, the sun;"

- **Visual:** Each province house gets a governor stick figure; they glow briefly. The Guide narrows his eyes and taps his temple: remember them. Hard cut to a sky scene: Ra, falcon-headed with a sun disc, rises over the horizon.
- **On-screen text:** REMEMBER THE GOVERNORS / RA, THE SUN
- **Camera / animation:** Highlight pulse; hard cut; sun rises behind Ra
- **SFX / music:** ominous note, choir hum
- **Length:** 21 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Each province house gets a governor stick figure; they glow briefly. The Guide narrows his eyes and taps his temple: remember them. Hard cut to a sky scene: Ra, falcon-headed with a sun disc, rises over the horizon. Include the Guide exactly as in the character reference. Text in frame: REMEMBER THE GOVERNORS / RA, THE SUN.`
- **AI motion prompt:** `Highlight pulse; hard cut; sun rises behind Ra. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 020 · 02:43.0–02:51.4 (8.4 s) · C · Illustrated world

**VO:** "Osiris, god of the dead and of rebirth, linked to the flood's yearly return; and his wife, Isis. These gods would last for 3,000 years."

- **Visual:** Beside the river: Osiris (green skin, white crown, crook and flail) appears as the water rises, with a circular arrow around a flood icon. Isis (throne headdress, wings) joins him. A timeline bar under the gods stretches across the screen: 3,000 YEARS. The Guide looks up in awe.
- **On-screen text:** OSIRIS · ISIS / 3,000 YEARS
- **Camera / animation:** Flood loop arrow spins; timeline bar extends
- **SFX / music:** rising water, shimmer
- **Length:** 26 spoken words · 8.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Beside the river: Osiris (green skin, white crown, crook and flail) appears as the water rises, with a circular arrow around a flood icon. Isis (throne headdress, wings) joins him. A timeline bar under the gods stretches across the screen: 3,000 YEARS. The Guide looks up in awe. Include the Guide exactly as in the character reference. Text in frame: OSIRIS · ISIS / 3,000 YEARS.`
- **AI motion prompt:** `Flood loop arrow spins; timeline bar extends. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 021 · 02:51.4–02:59.6 (8.2 s) · C · Illustrated world

**VO:** "The king wasn't just a ruler. Egyptians believed he was a god on earth, whose job was to keep Ma'at, the order of the universe,"

- **Visual:** The pharaoh on a throne with the double crown, glowing like the sun. The Guide does a playful bow. Then a balance scale with a feather labelled MA'AT lowers in above the pharaoh, holding the sun, the river and the stars in balance.
- **On-screen text:** GOD ON EARTH / MA'AT = THE ORDER OF THE UNIVERSE
- **Camera / animation:** Glow pulse; scale lowers in from the top
- **SFX / music:** gong, soft bell
- **Length:** 25 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: The pharaoh on a throne with the double crown, glowing like the sun. The Guide does a playful bow. Then a balance scale with a feather labelled MA'AT lowers in above the pharaoh, holding the sun, the river and the stars in balance. Include the Guide exactly as in the character reference. Text in frame: GOD ON EARTH / MA'AT = THE ORDER OF THE UNIVERSE.`
- **AI motion prompt:** `Glow pulse; scale lowers in from the top. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 022 · 02:59.6–03:06.5 (6.9 s) · B · Grey studio

**VO:** "so the sun rose and the river flooded on time. That made him all-powerful, as long as the river behaved."

- **Visual:** Grey studio: the pharaoh holds up two icons, a sun rising on time and a river flooding on time, both with green ticks. Then a small dark cloud and a shrinking river appear in the corner, and the pharaoh's glow flickers. The Guide glances at it nervously.
- **On-screen text:** ALL-POWERFUL... / ...AS LONG AS THE RIVER BEHAVED
- **Camera / animation:** Ticks pop; flicker on the last line
- **SFX / music:** ding, ding, flicker buzz
- **Length:** 21 spoken words · 6.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio: the pharaoh holds up two icons, a sun rising on time and a river flooding on time, both with green ticks. Then a small dark cloud and a shrinking river appear in the corner, and the pharaoh's glow flickers. The Guide glances at it nervously. Include the Guide exactly as in the character reference. Text in frame: ALL-POWERFUL... / ...AS LONG AS THE RIVER BEHAVED.`
- **AI motion prompt:** `Ticks pop; flicker on the last line. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 023 · 03:06.5–03:14.7 (8.2 s) · C · Illustrated world

**VO:** "Egyptians believed the king's spirit lived on after death, and that his afterlife helped keep the whole country in order."

- **Visual:** Night scene: a glowing spirit bird with the king's face flies up from his body to the stars. Golden lines from the spirit connect down to villages, fields and the river, keeping them in order. The Guide is not in this shot.
- **On-screen text:** THE KING'S SPIRIT LIVES ON
- **Camera / animation:** Spirit rises; lines draw down to the villages
- **SFX / music:** magical twinkle, night insects
- **Length:** 20 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Night scene: a glowing spirit bird with the king's face flies up from his body to the stars. Golden lines from the spirit connect down to villages, fields and the river, keeping them in order. Text in frame: THE KING'S SPIRIT LIVES ON.`
- **AI motion prompt:** `Spirit rises; lines draw down to the villages. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 024 · 03:14.7–03:21.4 (6.7 s) · C · Illustrated world

**VO:** "So his tomb mattered to everyone. Early kings were buried under flat mudbrick tombs called mastabas."

- **Visual:** Villagers turn to look at a tomb on the horizon. Cut to daylight desert: a low, flat, rectangular mudbrick tomb with a chalk label. The Guide sits on top of it, swinging his legs.
- **On-screen text:** THE TOMB MATTERED / MASTABA
- **Camera / animation:** Hard cut; side view of the mastaba
- **SFX / music:** murmurs, brick thud
- **Length:** 16 spoken words · 6.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Villagers turn to look at a tomb on the horizon. Cut to daylight desert: a low, flat, rectangular mudbrick tomb with a chalk label. The Guide sits on top of it, swinging his legs. Include the Guide exactly as in the character reference. Text in frame: THE TOMB MATTERED / MASTABA.`
- **AI motion prompt:** `Hard cut; side view of the mastaba. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

**Batch 2 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 3: The first pyramids (Scenes 25–33, 03:21.4–04:31.4)

#### Scene 025 · 03:21.4–03:30.6 (9.2 s) · C · Illustrated world

**VO:** "Around 2650 BC, King Djoser's official Imhotep built his tomb in stone instead, stacking six layers about 62 metres high."

- **Visual:** Imhotep (shaved head, scroll of plans) stands beside King Djoser at the mastaba. Stone layers stack up one by one, six in total, into the Step Pyramid. A height ruler reads 62 M. The Guide is not in this shot.
- **On-screen text:** 2650 BC / IMHOTEP / 6 LAYERS · 62 M
- **Camera / animation:** Each layer drops on a beat; tilt up
- **SFX / music:** six heavy stone thuds
- **Length:** 24 spoken words · 9.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Imhotep (shaved head, scroll of plans) stands beside King Djoser at the mastaba. Stone layers stack up one by one, six in total, into the Step Pyramid. A height ruler reads 62 M. Text in frame: 2650 BC / IMHOTEP / 6 LAYERS · 62 M.`
- **AI motion prompt:** `Each layer drops on a beat; tilt up. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 026 · 03:30.6–03:37.3 (6.7 s) · C · Illustrated world

**VO:** "The Step Pyramid is the oldest large cut-stone building in the world, and it started the age of pyramids."

- **Visual:** The finished Step Pyramid in sunlight. The Guide, tiny at its base, cranes his neck up. A gold badge pops in: OLDEST LARGE CUT-STONE BUILDING. A row of later pyramid silhouettes fades in behind it.
- **On-screen text:** STEP PYRAMID / THE AGE OF PYRAMIDS BEGINS
- **Camera / animation:** Badge pops; silhouettes fade in
- **SFX / music:** fanfare sting
- **Length:** 20 spoken words · 6.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: The finished Step Pyramid in sunlight. The Guide, tiny at its base, cranes his neck up. A gold badge pops in: OLDEST LARGE CUT-STONE BUILDING. A row of later pyramid silhouettes fades in behind it. Include the Guide exactly as in the character reference. Text in frame: STEP PYRAMID / THE AGE OF PYRAMIDS BEGINS.`
- **AI motion prompt:** `Badge pops; silhouettes fade in. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 027 · 03:37.3–03:43.5 (6.2 s) · C · Illustrated world

**VO:** "The next king, Sneferu, struggled to get the shape right. His Bent Pyramid changes angle halfway up,"

- **Visual:** King Sneferu scratches his head beside the Bent Pyramid. Its steep lower slope suddenly changes angle halfway up; a red angle mark wobbles. The Guide winces.
- **On-screen text:** SNEFERU / BENT PYRAMID
- **Camera / animation:** Angle line draws; wobble at the bend
- **SFX / music:** creak, comic boing
- **Length:** 17 spoken words · 6.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: King Sneferu scratches his head beside the Bent Pyramid. Its steep lower slope suddenly changes angle halfway up; a red angle mark wobbles. The Guide winces. Include the Guide exactly as in the character reference. Text in frame: SNEFERU / BENT PYRAMID.`
- **AI motion prompt:** `Angle line draws; wobble at the bend. Gentle cartoon motion, elements pop in with a small bounce, 6 seconds.`

#### Scene 028 · 03:43.5–03:51.4 (7.9 s) · C · Illustrated world

**VO:** "most likely because the first slope was too steep. His Red Pyramid finally got it right: the first true smooth-sided pyramid."

- **Visual:** A red "too steep" angle mark flashes on the lower slope. Then the Red Pyramid slides up beside it with smooth sides and a reddish tint; a green tick pops and Sneferu cheers. The Guide is not in this shot.
- **On-screen text:** TOO STEEP / RED PYRAMID ✓ FIRST TRUE PYRAMID
- **Camera / animation:** Slide in; tick pops
- **SFX / music:** ding, small cheer
- **Length:** 22 spoken words · 7.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A red "too steep" angle mark flashes on the lower slope. Then the Red Pyramid slides up beside it with smooth sides and a reddish tint; a green tick pops and Sneferu cheers. Text in frame: TOO STEEP / RED PYRAMID ✓ FIRST TRUE PYRAMID.`
- **AI motion prompt:** `Slide in; tick pops. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 029 · 03:51.4–03:59.1 (7.7 s) · C · Illustrated world

**VO:** "His son Khufu built the Great Pyramid of Giza around 2560 BC: about 2.3 million stone blocks,"

- **Visual:** Khufu (striped nemes headdress) steps onto the Giza plateau holding a plan scroll. The Great Pyramid starts building up while a counter races to 2,300,000 BLOCKS. The Guide is not in this shot.
- **On-screen text:** KHUFU · 2560 BC / 2.3 MILLION BLOCKS
- **Camera / animation:** Counter races; blocks stack
- **SFX / music:** rapid ticking, fanfare
- **Length:** 22 spoken words · 7.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Khufu (striped nemes headdress) steps onto the Giza plateau holding a plan scroll. The Great Pyramid starts building up while a counter races to 2,300,000 BLOCKS. Text in frame: KHUFU · 2560 BC / 2.3 MILLION BLOCKS.`
- **AI motion prompt:** `Counter races; blocks stack. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 030 · 03:59.1–04:07.3 (8.2 s) · C · Illustrated world

**VO:** "146 metres tall when finished. Nothing built by humans stood taller for about 3,800 years."

- **Visual:** The finished Great Pyramid with a height ruler: 146 M. A timeline slides under it; other buildings appear as shorter silhouettes while a counter rolls to 3,800 YEARS. The Guide looks up so far his hat falls off.
- **On-screen text:** 146 M / TALLEST FOR 3,800 YEARS
- **Camera / animation:** Tilt up; timeline slide
- **SFX / music:** counter roll, hat plop
- **Length:** 22 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: The finished Great Pyramid with a height ruler: 146 M. A timeline slides under it; other buildings appear as shorter silhouettes while a counter rolls to 3,800 YEARS. The Guide looks up so far his hat falls off. Include the Guide exactly as in the character reference. Text in frame: 146 M / TALLEST FOR 3,800 YEARS.`
- **AI motion prompt:** `Tilt up; timeline slide. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 031 · 04:07.3–04:17.0 (9.7 s) · C · Illustrated world

**VO:** "Deep inside, narrow passages lead to the king's granite burial chamber. By the time explorers reached it, it was empty. … The river made it possible."

- **Visual:** Cut-away of the pyramid: the Guide crawls along a narrow glowing passage into a granite chamber with a single empty sarcophagus and a cobweb. He shrugs. Quick cut to the Nile with boats waiting.
- **On-screen text:** EMPTY / THE RIVER MADE IT POSSIBLE
- **Camera / animation:** Camera follows him through the passage; hard cut
- **SFX / music:** echoing footsteps, cricket, river
- **Length:** 25 spoken words · 9.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Cut-away of the pyramid: the Guide crawls along a narrow glowing passage into a granite chamber with a single empty sarcophagus and a cobweb. He shrugs. Quick cut to the Nile with boats waiting. Include the Guide exactly as in the character reference. Text in frame: EMPTY / THE RIVER MADE IT POSSIBLE.`
- **AI motion prompt:** `Camera follows him through the passage; hard cut. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 032 · 04:17.0–04:25.2 (8.2 s) · A · Satellite map

**VO:** "Most of the stone was cut right at Giza, but fine white limestone for the outer casing came by boat from quarries across the river,"

- **Visual:** Map of Giza and the river: a local quarry icon right beside the pyramids. A white limestone block rides a boat across the river from the quarries on the far bank. The Guide waves from bottom right.
- **On-screen text:** CUT AT GIZA / WHITE LIMESTONE BY BOAT
- **Camera / animation:** Map slides; boat crosses on a dotted line
- **SFX / music:** oars, water
- **Length:** 25 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map of Giza and the river: a local quarry icon right beside the pyramids. A white limestone block rides a boat across the river from the quarries on the far bank. The Guide waves from bottom right. Include the Guide exactly as in the character reference. Text in frame: CUT AT GIZA / WHITE LIMESTONE BY BOAT.`
- **AI motion prompt:** `Map slides; boat crosses on a dotted line. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 033 · 04:25.2–04:31.4 (6.2 s) · A · Satellite map

**VO:** "and huge granite beams for the king's burial chamber came from Aswan, hundreds of kilometres upstream."

- **Visual:** The map zooms out: a long dotted line runs far south to ASWAN, where a huge pink granite beam loads onto a big barge and floats north past palm trees. The Guide is not in this shot.
- **On-screen text:** ASWAN GRANITE / HUNDREDS OF KM UPSTREAM
- **Camera / animation:** Zoom out; barge follows the dotted route
- **SFX / music:** creaking wood, river
- **Length:** 16 spoken words · 6.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: The map zooms out: a long dotted line runs far south to ASWAN, where a huge pink granite beam loads onto a big barge and floats north past palm trees. Text in frame: ASWAN GRANITE / HUNDREDS OF KM UPSTREAM.`
- **AI motion prompt:** `Zoom out; barge follows the dotted route. Gentle cartoon motion, elements pop in with a small bounce, 6 seconds.`

**Batch 3 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 4: Building the pyramids (Scenes 34–47, 04:31.4–06:20.4)

#### Scene 034 · 04:31.4–04:40.1 (8.7 s) · C · Illustrated world

**VO:** "How they raised the blocks is still debated. The most likely answer is ramps of mudbrick and rubble, with blocks dragged on wooden sledges."

- **Visual:** A big question mark over a half-built pyramid. It morphs into a ramp of mudbrick and rubble rising around the pyramid; workers drag a block on a wooden sledge with ropes. The Guide helps pull a rope.
- **On-screen text:** HOW? / RAMPS + SLEDGES
- **Camera / animation:** Question mark morphs into the ramp
- **SFX / music:** rope strain, wood scraping
- **Length:** 24 spoken words · 8.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A big question mark over a half-built pyramid. It morphs into a ramp of mudbrick and rubble rising around the pyramid; workers drag a block on a wooden sledge with ropes. The Guide helps pull a rope. Include the Guide exactly as in the character reference. Text in frame: HOW? / RAMPS + SLEDGES.`
- **AI motion prompt:** `Question mark morphs into the ramp. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 035 · 04:40.1–04:48.0 (7.9 s) · C · Illustrated world

**VO:** "Wetting the sand in front of a sledge cuts the friction sharply, and an Egyptian tomb painting shows a worker doing exactly that."

- **Visual:** Close-up: a worker pours water from a jar onto the sand in front of the sledge; a friction meter needle drops from red to green and the sledge slides easily. A small framed inset shows the ancient tomb painting of the same action. The Guide is not in this shot.
- **On-screen text:** WET SAND = LESS FRICTION
- **Camera / animation:** Inset pops in top right
- **SFX / music:** water pour, smooth slide
- **Length:** 23 spoken words · 7.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Close-up: a worker pours water from a jar onto the sand in front of the sledge; a friction meter needle drops from red to green and the sledge slides easily. A small framed inset shows the ancient tomb painting of the same action. Text in frame: WET SAND = LESS FRICTION.`
- **AI motion prompt:** `Inset pops in top right. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 036 · 04:48.0–04:56.2 (8.2 s) · C · Illustrated world

**VO:** "It was not built by slaves. Archaeologists found the builders' town beside the pyramids, with bakeries, breweries and sleeping halls,"

- **Visual:** A big NOT SLAVES stamp. Then a wide pan through the workers' town next to the pyramids: a bakery with bread loaves, a brewery with jars, long sleeping halls. The Guide waves at the bakers.
- **On-screen text:** NOT BUILT BY SLAVES / BAKERIES · BREWERIES · SLEEPING HALLS
- **Camera / animation:** Stamp; slow horizontal pan
- **SFX / music:** stamp, town bustle
- **Length:** 20 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A big NOT SLAVES stamp. Then a wide pan through the workers' town next to the pyramids: a bakery with bread loaves, a brewery with jars, long sleeping halls. The Guide waves at the bakers. Include the Guide exactly as in the character reference. Text in frame: NOT BUILT BY SLAVES / BAKERIES · BREWERIES · SLEEPING HALLS.`
- **AI motion prompt:** `Stamp; slow horizontal pan. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 037 · 04:56.2–05:03.4 (7.2 s) · C · Illustrated world

**VO:** "and the workers' own tombs nearby. Many were farmers working in rotating shifts, likely during the flood season,"

- **Visual:** Small workers' tombs near the town. Then split screen: left, flooded fields with a farmer's hut; right, the same farmer at the pyramid. A shift wheel turns as teams swap. The Guide is not in this shot.
- **On-screen text:** WORKERS' TOMBS / ROTATING SHIFTS
- **Camera / animation:** Wipe between halves; wheel turns
- **SFX / music:** water, crowd
- **Length:** 18 spoken words · 7.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Small workers' tombs near the town. Then split screen: left, flooded fields with a farmer's hut; right, the same farmer at the pyramid. A shift wheel turns as teams swap. Text in frame: WORKERS' TOMBS / ROTATING SHIFTS.`
- **AI motion prompt:** `Wipe between halves; wheel turns. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 038 · 05:03.4–05:10.3 (6.9 s) · C · Illustrated world

**VO:** "when their fields were under water anyway. … We even have a logbook from one of the crews. In 2013,"

- **Visual:** The flooded field in close-up (only a scarecrow's hat floats, comically). Then the Guide opens an old leather logbook; a year card flips to 2013.
- **On-screen text:** FIELDS UNDER WATER / THE LOGBOOK / 2013
- **Camera / animation:** Hard cut; page flip
- **SFX / music:** splash, page flip
- **Length:** 20 spoken words · 6.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: The flooded field in close-up (only a scarecrow's hat floats, comically). Then the Guide opens an old leather logbook; a year card flips to 2013. Include the Guide exactly as in the character reference. Text in frame: FIELDS UNDER WATER / THE LOGBOOK / 2013.`
- **AI motion prompt:** `Hard cut; page flip. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 039 · 05:10.3–05:19.0 (8.7 s) · D · Artefact / relief close-up

**VO:** "archaeologists found the oldest inscribed papyri ever discovered, including the diary of an inspector named Merer."

- **Visual:** Archaeologists dig at a desert site on the Red Sea coast and lift rolled papyri from the sand. One unrolls in close-up with ancient writing. A name tag pops in: MERER, INSPECTOR, with a simple stick portrait. The Guide is not in this shot.
- **On-screen text:** OLDEST INSCRIBED PAPYRI / DIARY OF MERER
- **Camera / animation:** Zoom into the papyrus
- **SFX / music:** digging, papyrus crackle
- **Length:** 16 spoken words · 8.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: Archaeologists dig at a desert site on the Red Sea coast and lift rolled papyri from the sand. One unrolls in close-up with ancient writing. A name tag pops in: MERER, INSPECTOR, with a simple stick portrait. Text in frame: OLDEST INSCRIBED PAPYRI / DIARY OF MERER.`
- **AI motion prompt:** `Zoom into the papyrus. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 040 · 05:19.0–05:27.4 (8.4 s) · A · Satellite map

**VO:** "It records his team ferrying limestone from the quarries at Tura to a harbour at Giza, trip after trip, in the reign of Khufu."

- **Visual:** Map: the TURA quarries on the east bank; a boat with a white limestone block crosses to a GIZA HARBOUR icon and loops back and forth while a trip counter ticks up. Merer stands on the boat with a scroll; a KHUFU cartouche sits in the corner. The Guide is not in this shot.
- **On-screen text:** TURA → GIZA / TRIP AFTER TRIP
- **Camera / animation:** Boat loops 3–4 times; counter ticks
- **SFX / music:** oars, counter clicks
- **Length:** 24 spoken words · 8.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map: the TURA quarries on the east bank; a boat with a white limestone block crosses to a GIZA HARBOUR icon and loops back and forth while a trip counter ticks up. Merer stands on the boat with a scroll; a KHUFU cartouche sits in the corner. Text in frame: TURA → GIZA / TRIP AFTER TRIP.`
- **AI motion prompt:** `Boat loops 3–4 times; counter ticks. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 041 · 05:27.4–05:36.6 (9.2 s) · C · Illustrated world

**VO:** "A pyramid wasn't just a tomb. Each came with temples, a causeway and farmland whose harvests paid priests to make offerings to the dead king forever."

- **Visual:** A full pyramid complex: pyramid, valley temple, long causeway and green farmland. Priests carry trays of bread, beer and geese to the dead king's temple. An infinity sign glows above. The Guide is not in this shot.
- **On-screen text:** NOT JUST A TOMB / OFFERINGS FOREVER
- **Camera / animation:** Wide shot; slow pan along the causeway
- **SFX / music:** chant, birds
- **Length:** 26 spoken words · 9.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A full pyramid complex: pyramid, valley temple, long causeway and green farmland. Priests carry trays of bread, beer and geese to the dead king's temple. An infinity sign glows above. Text in frame: NOT JUST A TOMB / OFFERINGS FOREVER.`
- **AI motion prompt:** `Wide shot; slow pan along the causeway. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 042 · 05:36.6–05:42.8 (6.2 s) · B · Grey studio

**VO:** "Over generations, more and more of Egypt's land and grain went to supporting dead kings and their priests."

- **Visual:** Grey studio: a pie chart of Egypt's land and grain. The slice labelled DEAD KINGS & PRIESTS grows bigger with each generation tick. The Guide frowns at it.
- **On-screen text:** MORE AND MORE LAND AND GRAIN
- **Camera / animation:** Pie slice grows in 3 steps
- **SFX / music:** ticks, coin slides
- **Length:** 18 spoken words · 6.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio: a pie chart of Egypt's land and grain. The slice labelled DEAD KINGS & PRIESTS grows bigger with each generation tick. The Guide frowns at it. Include the Guide exactly as in the character reference. Text in frame: MORE AND MORE LAND AND GRAIN.`
- **AI motion prompt:** `Pie slice grows in 3 steps. Gentle cartoon motion, elements pop in with a small bounce, 6 seconds.`

#### Scene 043 · 05:42.8–05:49.7 (6.9 s) · C · Illustrated world

**VO:** "Khufu's son Khafre built the second pyramid at Giza, and the Great Sphinx was most likely carved in his reign."

- **Visual:** Giza: Khafre stands beside the second pyramid. The Great Sphinx appears in front of it; the Guide stands between its paws for scale.
- **On-screen text:** KHAFRE / THE GREAT SPHINX
- **Camera / animation:** Push in toward the Sphinx
- **SFX / music:** sand wind, fanfare
- **Length:** 20 spoken words · 6.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Giza: Khafre stands beside the second pyramid. The Great Sphinx appears in front of it; the Guide stands between its paws for scale. Include the Guide exactly as in the character reference. Text in frame: KHAFRE / THE GREAT SPHINX.`
- **AI motion prompt:** `Push in toward the Sphinx. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 044 · 05:49.7–05:57.6 (7.9 s) · C · Illustrated world

**VO:** "The third, built by Menkaure, is far smaller. After Giza, pyramids kept shrinking. … That tells you something. The kings were spending less,"

- **Visual:** Three pyramids in a row: big, big, small (Menkaure). After them, later pyramids shrink smaller and smaller. The Guide raises one finger. A seesaw slides in.
- **On-screen text:** MENKAURE / PYRAMIDS KEPT SHRINKING
- **Camera / animation:** Shrinking sequence; seesaw slides in
- **SFX / music:** descending notes
- **Length:** 22 spoken words · 7.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Three pyramids in a row: big, big, small (Menkaure). After them, later pyramids shrink smaller and smaller. The Guide raises one finger. A seesaw slides in. Include the Guide exactly as in the character reference. Text in frame: MENKAURE / PYRAMIDS KEPT SHRINKING.`
- **AI motion prompt:** `Shrinking sequence; seesaw slides in. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 045 · 05:57.6–06:04.8 (7.2 s) · B · Grey studio

**VO:** "while the officials, priests and provincial governors who ran the state were growing richer and more independent."

- **Visual:** Seesaw: the king with a small pile of gold rises; on the other end officials, priests and governors with growing gold piles sink. The governors wear little crowns of their own. The Guide is not in this shot.
- **On-screen text:** KINGS ↓ · OFFICIALS & GOVERNORS ↑
- **Camera / animation:** Seesaw tips; gold piles grow
- **SFX / music:** coins clinking, creak
- **Length:** 17 spoken words · 7.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Seesaw: the king with a small pile of gold rises; on the other end officials, priests and governors with growing gold piles sink. The governors wear little crowns of their own. Text in frame: KINGS ↓ · OFFICIALS & GOVERNORS ↑.`
- **AI motion prompt:** `Seesaw tips; gold piles grow. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 046 · 06:04.8–06:11.7 (6.9 s) · C · Illustrated world

**VO:** "Late in this era, kings began carving spells on their burial chamber walls to help them rise to the sky after death."

- **Visual:** Inside a burial chamber, workers carve columns of blue hieroglyphs on the walls. A ghostly king rises from his sarcophagus toward stars painted on the ceiling. The Guide is not in this shot.
- **On-screen text:** SPELLS ON THE WALLS
- **Camera / animation:** Tilt up from walls to the starry ceiling
- **SFX / music:** chisel taps, choir
- **Length:** 22 spoken words · 6.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Inside a burial chamber, workers carve columns of blue hieroglyphs on the walls. A ghostly king rises from his sarcophagus toward stars painted on the ceiling. Text in frame: SPELLS ON THE WALLS.`
- **AI motion prompt:** `Tilt up from walls to the starry ceiling. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 047 · 06:11.7–06:20.4 (8.7 s) · C · Illustrated world

**VO:** "These Pyramid Texts are among the oldest religious writings in the world. … For about 500 years, Egypt's god-kings built mountains of stone."

- **Visual:** Label PYRAMID TEXTS and a badge OLDEST RELIGIOUS WRITINGS. Then a quick montage of pyramids rising one after another under a 500 YEARS bar. The Guide is not in this shot.
- **On-screen text:** PYRAMID TEXTS / 500 YEARS
- **Camera / animation:** Badge pop; pyramids pop up in time-lapse
- **SFX / music:** twinkle, stone thuds
- **Length:** 24 spoken words · 8.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Label PYRAMID TEXTS and a badge OLDEST RELIGIOUS WRITINGS. Then a quick montage of pyramids rising one after another under a 500 YEARS bar. Text in frame: PYRAMID TEXTS / 500 YEARS.`
- **AI motion prompt:** `Badge pop; pyramids pop up in time-lapse. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

**Batch 4 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 5: Collapse and the Middle Kingdom (Scenes 48–60, 06:20.4–08:06.6)

#### Scene 048 · 06:20.4–06:28.3 (7.9 s) · C · Illustrated world

**VO:** "Then the river stopped cooperating. … Around 2200 BC, the climate shifted and the floods shrank, year after year."

- **Visual:** The sky turns dull and hot; the Nile shrinks to a thin line, step by step, while a year counter ticks from 2200 BC. The Guide wipes sweat from his brow.
- **On-screen text:** 2200 BC / THE FLOODS SHRANK
- **Camera / animation:** River shrinks with each tick; colour drains
- **SFX / music:** heat drone, ticking
- **Length:** 21 spoken words · 7.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: The sky turns dull and hot; the Nile shrinks to a thin line, step by step, while a year counter ticks from 2200 BC. The Guide wipes sweat from his brow. Include the Guide exactly as in the character reference. Text in frame: 2200 BC / THE FLOODS SHRANK.`
- **AI motion prompt:** `River shrinks with each tick; colour drains. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 049 · 06:28.3–06:35.5 (7.2 s) · C · Illustrated world

**VO:** "Harvests failed and people starved. And a god-king who couldn't make the river rise no longer looked much like a god."

- **Visual:** Cracked dry fields, wilted crops, thin villagers with empty bowls. The pharaoh on a balcony raises his arms but the river doesn't rise; his golden glow cracks like glass. The Guide is not in this shot.
- **On-screen text:** HARVESTS FAILED / NOT MUCH LIKE A GOD
- **Camera / animation:** Glow cracks and fades
- **SFX / music:** dry wind, cracking glass
- **Length:** 22 spoken words · 7.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Cracked dry fields, wilted crops, thin villagers with empty bowls. The pharaoh on a balcony raises his arms but the river doesn't rise; his golden glow cracks like glass. Text in frame: HARVESTS FAILED / NOT MUCH LIKE A GOD.`
- **AI motion prompt:** `Glow cracks and fades. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 050 · 06:35.5–06:41.7 (6.2 s) · B · Grey studio

**VO:** "Pepi II, the last great king of this era, may have reigned for more than 60 years. By then,"

- **Visual:** Pepi II on his throne ages fast: his beard grows and a counter reaches 60+ YEARS. The Guide checks a little sundial impatiently.
- **On-screen text:** PEPI II / 60+ YEARS
- **Camera / animation:** Aging morph; counter
- **SFX / music:** clock ticking
- **Length:** 20 spoken words · 6.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Pepi II on his throne ages fast: his beard grows and a counter reaches 60+ YEARS. The Guide checks a little sundial impatiently. Include the Guide exactly as in the character reference. Text in frame: PEPI II / 60+ YEARS.`
- **AI motion prompt:** `Aging morph; counter. Gentle cartoon motion, elements pop in with a small bounce, 6 seconds.`

#### Scene 051 · 06:41.7–06:50.4 (8.7 s) · B · Grey studio

**VO:** "provincial governors had made their posts hereditary and were ruling like independent kings. After him, central power collapsed."

- **Visual:** Around Pepi, governors put crowns on their own heads and pass them to their sons (mini family-tree arrows). Then the whole power chart cracks and falls apart. The Guide is not in this shot.
- **On-screen text:** HEREDITARY GOVERNORS / COLLAPSE
- **Camera / animation:** Crowns pop; chart crumbles
- **SFX / music:** crown pops, crash
- **Length:** 18 spoken words · 8.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Around Pepi, governors put crowns on their own heads and pass them to their sons (mini family-tree arrows). Then the whole power chart cracks and falls apart. Text in frame: HEREDITARY GOVERNORS / COLLAPSE.`
- **AI motion prompt:** `Crowns pop; chart crumbles. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 052 · 06:50.4–07:00.1 (9.7 s) · A · Satellite map

**VO:** "For more than a century, there was no single Egypt. Rival dynasties ruled from the north and from Thebes in the south, local strongmen fought each other,"

- **Visual:** Satellite map: Egypt's single colour shatters into patches. A northern capital and THEBES in the south light up with rival flags; small strongmen icons fight between them. The Guide is not in this shot.
- **On-screen text:** NO SINGLE EGYPT / NORTH vs THEBES
- **Camera / animation:** Map shatters; flags plant
- **SFX / music:** glass shatter, clashes
- **Length:** 27 spoken words · 9.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map: Egypt's single colour shatters into patches. A northern capital and THEBES in the south light up with rival flags; small strongmen icons fight between them. Text in frame: NO SINGLE EGYPT / NORTH vs THEBES.`
- **AI motion prompt:** `Map shatters; flags plant. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 053 · 07:00.1–07:09.8 (9.7 s) · C · Illustrated world

**VO:** "and famine hit village after village. Historians call it the First Intermediate Period. Something lasting came out of it, too. With the kings weakened,"

- **Visual:** Sunset: a village with an empty granary and hungry families. A yellow comic title drops in. Then a sparkle in the corner hints at "something lasting". The Guide is not in this shot.
- **On-screen text:** FIRST INTERMEDIATE PERIOD
- **Camera / animation:** Title slams in; slight shake
- **SFX / music:** wind, title thud, sparkle
- **Length:** 24 spoken words · 9.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Sunset: a village with an empty granary and hungry families. A yellow comic title drops in. Then a sparkle in the corner hints at "something lasting". Text in frame: FIRST INTERMEDIATE PERIOD.`
- **AI motion prompt:** `Title slams in; slight shake. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 054 · 07:09.8–07:18.7 (8.9 s) · C · Illustrated world

**VO:** "wealthy local families began claiming an afterlife that had once belonged to the king, painting the old royal spells inside their own coffins."

- **Visual:** Inside a house, a wealthy local family paints the old royal spells inside a wooden coffin. A ghostly crown floats from a royal tomb over to their coffin. The Guide raises his eyebrows.
- **On-screen text:** AN AFTERLIFE FOR THE RICH, NOT JUST THE KING
- **Camera / animation:** Crown floats across; brush strokes fill the coffin
- **SFX / music:** brush strokes, twinkle
- **Length:** 23 spoken words · 8.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Inside a house, a wealthy local family paints the old royal spells inside a wooden coffin. A ghostly crown floats from a royal tomb over to their coffin. The Guide raises his eyebrows. Include the Guide exactly as in the character reference. Text in frame: AN AFTERLIFE FOR THE RICH, NOT JUST THE KING.`
- **AI motion prompt:** `Crown floats across; brush strokes fill the coffin. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 055 · 07:18.7–07:27.1 (8.4 s) · A · Satellite map

**VO:** "Around 2050 BC, Mentuhotep II of Thebes defeated the northern dynasty and reunited the country."

- **Visual:** Map: Mentuhotep II marches north from Thebes with an army arrow; the northern flag falls and the map pieces fuse back into one colour. The Guide is not in this shot.
- **On-screen text:** 2050 BC / MENTUHOTEP II REUNITES EGYPT
- **Camera / animation:** Arrow sweeps north; pieces merge
- **SFX / music:** march, unifying chime
- **Length:** 18 spoken words · 8.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map: Mentuhotep II marches north from Thebes with an army arrow; the northern flag falls and the map pieces fuse back into one colour. Text in frame: 2050 BC / MENTUHOTEP II REUNITES EGYPT.`
- **AI motion prompt:** `Arrow sweeps north; pieces merge. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 056 · 07:27.1–07:33.3 (6.2 s) · B · Grey studio

**VO:** "This began the Middle Kingdom. … Its kings had learned from the collapse. They moved the capital north,"

- **Visual:** Yellow title card MIDDLE KINGDOM. Then the Guide holds a "lessons learned" scroll and ticks items off. A capital icon starts sliding north on a small map card.
- **On-screen text:** MIDDLE KINGDOM / LESSONS LEARNED
- **Camera / animation:** Title slam; check marks
- **SFX / music:** title thud, ticks
- **Length:** 17 spoken words · 6.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Yellow title card MIDDLE KINGDOM. Then the Guide holds a "lessons learned" scroll and ticks items off. A capital icon starts sliding north on a small map card. Include the Guide exactly as in the character reference. Text in frame: MIDDLE KINGDOM / LESSONS LEARNED.`
- **AI motion prompt:** `Title slam; check marks. Gentle cartoon motion, elements pop in with a small bounce, 6 seconds.`

#### Scene 057 · 07:33.3–07:39.8 (6.5 s) · A · Satellite map

**VO:** "near the Faiyum oasis, drained its marshes to grow more food, cut the power of the provincial governors,"

- **Visual:** Satellite map: the capital icon settles near the FAIYUM oasis; blue marsh drains into green fields; the governors' little crowns shrink. The Guide gives a thumbs up.
- **On-screen text:** FAIYUM / DRAIN THE MARSHES / CUT THE GOVERNORS' POWER
- **Camera / animation:** Marsh-to-field colour wipe; crowns shrink
- **SFX / music:** gurgle, pop
- **Length:** 18 spoken words · 6.5 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map: the capital icon settles near the FAIYUM oasis; blue marsh drains into green fields; the governors' little crowns shrink. The Guide gives a thumbs up. Include the Guide exactly as in the character reference. Text in frame: FAIYUM / DRAIN THE MARSHES / CUT THE GOVERNORS' POWER.`
- **AI motion prompt:** `Marsh-to-field colour wipe; crowns shrink. Gentle cartoon motion, elements pop in with a small bounce, 6 seconds.`

#### Scene 058 · 07:39.8–07:48.2 (8.4 s) · A · Satellite map

**VO:** "and built a chain of massive forts along the Nile in Nubia to guard the south. For about 300 years, Egypt was stable again."

- **Visual:** Map zooms south to Nubia: a chain of big mudbrick forts pops up along the Nile. Then a calm Egypt with a 300 YEARS bar. The Guide is not in this shot.
- **On-screen text:** NUBIAN FORTS / 300 YEARS OF STABILITY
- **Camera / animation:** Forts pop in sequence
- **SFX / music:** stone thuds, calm strings
- **Length:** 25 spoken words · 8.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map zooms south to Nubia: a chain of big mudbrick forts pops up along the Nile. Then a calm Egypt with a 300 YEARS bar. Text in frame: NUBIAN FORTS / 300 YEARS OF STABILITY.`
- **AI motion prompt:** `Forts pop in sequence. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 059 · 07:48.2–07:57.4 (9.2 s) · C · Illustrated world

**VO:** "It was also Egypt's classic age of literature. Stories and teachings written in this period were copied in schools for centuries afterwards."

- **Visual:** A school room: young scribes sit cross-legged copying stories onto papyrus and pottery shards; a teacher points to a scroll. The Guide sits among them, writing too.
- **On-screen text:** CLASSIC AGE OF LITERATURE
- **Camera / animation:** Slow pan across the students
- **SFX / music:** reed pens scratching
- **Length:** 22 spoken words · 9.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A school room: young scribes sit cross-legged copying stories onto papyrus and pottery shards; a teacher points to a scroll. The Guide sits among them, writing too. Include the Guide exactly as in the character reference. Text in frame: CLASSIC AGE OF LITERATURE.`
- **AI motion prompt:** `Slow pan across the students. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 060 · 07:57.4–08:06.6 (9.2 s) · B · Grey studio

**VO:** "But after about two centuries, the royal line weakened. Dozens of short-lived kings followed one another, and their grip on the north slipped."

- **Visual:** Grey studio: a line of short-lived kings pop in and vanish one after another. A big hand gripping the north of a map loosens and slips. The Guide is not in this shot.
- **On-screen text:** DOZENS OF SHORT-LIVED KINGS
- **Camera / animation:** Fast pop sequence
- **SFX / music:** rapid pops, slip
- **Length:** 24 spoken words · 9.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio: a line of short-lived kings pop in and vanish one after another. A big hand gripping the north of a map loosens and slips. Text in frame: DOZENS OF SHORT-LIVED KINGS.`
- **AI motion prompt:** `Fast pop sequence. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

**Batch 5 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 6: The Hyksos and the fight back (Scenes 61–72, 08:06.6–09:41.0)

#### Scene 061 · 08:06.6–08:16.0 (9.4 s) · A · Satellite map

**VO:** "Meanwhile, settlers from the Levant had been moving into the northern delta. As the Middle Kingdom weakened, their leaders took control of the north,"

- **Visual:** Map: small arrows of settler families with donkeys walk from the LEVANT into the northern delta. Then the delta turns a different colour as their leaders take over. The Guide is not in this shot.
- **On-screen text:** LEVANT → DELTA
- **Camera / animation:** Arrows trickle in; colour wipe
- **SFX / music:** footsteps, donkey bray
- **Length:** 24 spoken words · 9.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map: small arrows of settler families with donkeys walk from the LEVANT into the northern delta. Then the delta turns a different colour as their leaders take over. Text in frame: LEVANT → DELTA.`
- **AI motion prompt:** `Arrows trickle in; colour wipe. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 062 · 08:16.0–08:24.9 (8.9 s) · C · Illustrated world

**VO:** "around 1650 BC, ruling from their capital, Avaris. Egyptians called them "rulers of foreign lands." We call them the Hyksos."

- **Visual:** A walled city in the delta, AVARIS, with a Hyksos ruler (Levantine robe, mushroom-shaped hair, beard) on the throne. Egyptian scribes whisper; a scroll reads "Rulers of Foreign Lands". The Guide is not in this shot.
- **On-screen text:** 1650 BC / AVARIS / THE HYKSOS
- **Camera / animation:** Zoom into the city; scroll unrolls
- **SFX / music:** whispers, gong
- **Length:** 22 spoken words · 8.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A walled city in the delta, AVARIS, with a Hyksos ruler (Levantine robe, mushroom-shaped hair, beard) on the throne. Egyptian scribes whisper; a scroll reads "Rulers of Foreign Lands". Text in frame: 1650 BC / AVARIS / THE HYKSOS.`
- **AI motion prompt:** `Zoom into the city; scroll unrolls. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 063 · 08:24.9–08:32.3 (7.4 s) · B · Grey studio

**VO:** "They had horse-drawn chariots, powerful composite bows and better bronze weapons, which Egypt had barely used before."

- **Visual:** Weapon cards pop in on the grey background: HORSE CHARIOT, COMPOSITE BOW, BRONZE WEAPONS, each with a NEW badge. An Egyptian soldier with a wooden club looks at them, confused. The Guide whistles.
- **On-screen text:** CHARIOTS · COMPOSITE BOWS · BRONZE
- **Camera / animation:** Cards pop one by one
- **SFX / music:** horse whinny, bow twang, clang
- **Length:** 18 spoken words · 7.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Weapon cards pop in on the grey background: HORSE CHARIOT, COMPOSITE BOW, BRONZE WEAPONS, each with a NEW badge. An Egyptian soldier with a wooden club looks at them, confused. The Guide whistles. Include the Guide exactly as in the character reference. Text in frame: CHARIOTS · COMPOSITE BOWS · BRONZE.`
- **AI motion prompt:** `Cards pop one by one. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 064 · 08:32.3–08:39.5 (7.2 s) · A · Satellite map

**VO:** "For the first time, foreigners ruled the land of the pharaohs, and the Egyptian kings in Thebes had to accept them."

- **Visual:** Map split: the north in Hyksos colour, the south (THEBES) still Egyptian. The Theban king bows, unhappy. The Guide is not in this shot.
- **On-screen text:** FOREIGNERS RULE EGYPT
- **Camera / animation:** Map divides; slow push on the bowing king
- **SFX / music:** low brass
- **Length:** 21 spoken words · 7.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map split: the north in Hyksos colour, the south (THEBES) still Egyptian. The Theban king bows, unhappy. Text in frame: FOREIGNERS RULE EGYPT.`
- **AI motion prompt:** `Map divides; slow push on the bowing king. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 065 · 08:39.5–08:48.9 (9.4 s) · C · Illustrated world

**VO:** "Yet the Hyksos didn't try to erase Egypt. They took pharaohs' titles, wrote their names in hieroglyphs, and worshipped Egyptian gods alongside their own."

- **Visual:** The Hyksos king writes his name in a cartouche, puts on the double crown and offers to Egyptian gods next to his own storm god. The Guide is not in this shot.
- **On-screen text:** THEY BECAME EGYPTIAN
- **Camera / animation:** Costume change in two steps
- **SFX / music:** magic poof, ding
- **Length:** 24 spoken words · 9.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: The Hyksos king writes his name in a cartouche, puts on the double crown and offers to Egyptian gods next to his own storm god. Text in frame: THEY BECAME EGYPTIAN.`
- **AI motion prompt:** `Costume change in two steps. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 066 · 08:48.9–08:56.8 (7.9 s) · B · Grey studio

**VO:** "It's the first time we see a pattern that runs through this whole story: foreign rulers turning themselves into Egyptian kings."

- **Visual:** A loop arrow appears with a sticky note THE PATTERN: a foreign king walks around the loop and comes out as a pharaoh. The Guide underlines it with his spear.
- **On-screen text:** THE PATTERN: FOREIGN RULER → EGYPTIAN KING
- **Camera / animation:** Loop arrow spins; morph
- **SFX / music:** ding, whoosh
- **Length:** 21 spoken words · 7.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: A loop arrow appears with a sticky note THE PATTERN: a foreign king walks around the loop and comes out as a pharaoh. The Guide underlines it with his spear. Include the Guide exactly as in the character reference. Text in frame: THE PATTERN: FOREIGN RULER → EGYPTIAN KING.`
- **AI motion prompt:** `Loop arrow spins; morph. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 067 · 08:56.8–09:03.3 (6.5 s) · C · Illustrated world

**VO:** "The kings of Thebes fought back. Seqenenre died in battle, and his mummy's skull still shows the axe and spear wounds."

- **Visual:** Battle: Theban king Seqenenre falls. Inset: a cartoon skull with axe and spear marks (simple, not gory). The Guide is not in this shot.
- **On-screen text:** THE KINGS OF THEBES FIGHT BACK / SEQENENRE
- **Camera / animation:** Cut to battle; inset pops
- **SFX / music:** battle cry, thud
- **Length:** 21 spoken words · 6.5 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Battle: Theban king Seqenenre falls. Inset: a cartoon skull with axe and spear marks (simple, not gory). Text in frame: THE KINGS OF THEBES FIGHT BACK / SEQENENRE.`
- **AI motion prompt:** `Cut to battle; inset pops. Gentle cartoon motion, elements pop in with a small bounce, 6 seconds.`

#### Scene 068 · 09:03.3–09:10.0 (6.7 s) · A · Satellite map

**VO:** "Thebes was squeezed from both sides, because the Hyksos were in contact with the kingdom of Kush to the south."

- **Visual:** Map: Thebes in the middle, squeezed by the Hyksos from the north and KUSH from the south, red pincer arrows. The Guide looks left and right, worried.
- **On-screen text:** SQUEEZED / KUSH
- **Camera / animation:** Pincer arrows close in
- **SFX / music:** tension drums
- **Length:** 20 spoken words · 6.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map: Thebes in the middle, squeezed by the Hyksos from the north and KUSH from the south, red pincer arrows. The Guide looks left and right, worried. Include the Guide exactly as in the character reference. Text in frame: SQUEEZED / KUSH.`
- **AI motion prompt:** `Pincer arrows close in. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 069 · 09:10.0–09:17.9 (7.9 s) · C · Illustrated world

**VO:** "The next Theban king, Kamose, intercepted a Hyksos letter urging Kush to attack Thebes while his army was away."

- **Visual:** Kamose's soldiers catch a messenger running across the desert and pull a letter from his bag; it unrolls with a target drawn on Thebes. The Guide is not in this shot.
- **On-screen text:** KAMOSE / THE INTERCEPTED LETTER
- **Camera / animation:** Zoom on the letter
- **SFX / music:** rustle, sting
- **Length:** 19 spoken words · 7.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Kamose's soldiers catch a messenger running across the desert and pull a letter from his bag; it unrolls with a target drawn on Thebes. Text in frame: KAMOSE / THE INTERCEPTED LETTER.`
- **AI motion prompt:** `Zoom on the letter. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 070 · 09:17.9–09:25.6 (7.7 s) · C · Illustrated world

**VO:** "The Thebans adopted the enemy's chariots and bows, and around 1550 BC, Ahmose captured Avaris,"

- **Visual:** Egyptian soldiers train with chariots and composite bows. Then Ahmose leads a charge on Avaris; the Hyksos flag swaps for an Egyptian one. The Guide is not in this shot.
- **On-screen text:** 1550 BC / AHMOSE TAKES AVARIS
- **Camera / animation:** Training montage; charge
- **SFX / music:** horse trot, chariots
- **Length:** 17 spoken words · 7.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Egyptian soldiers train with chariots and composite bows. Then Ahmose leads a charge on Avaris; the Hyksos flag swaps for an Egyptian one. Text in frame: 1550 BC / AHMOSE TAKES AVARIS.`
- **AI motion prompt:** `Training montage; charge. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 071 · 09:25.6–09:33.3 (7.7 s) · A · Satellite map

**VO:** "drove the Hyksos out, and chased them into Canaan. … Foreign rule changed Egypt. It now had a professional army,"

- **Visual:** Map: Hyksos arrows are chased out into CANAAN. Then a professional army marches in step under Egyptian banners. The Guide is not in this shot.
- **On-screen text:** HYKSOS OUT / A PROFESSIONAL ARMY
- **Camera / animation:** Arrows sweep; march
- **SFX / music:** victory horn, march
- **Length:** 19 spoken words · 7.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map: Hyksos arrows are chased out into CANAAN. Then a professional army marches in step under Egyptian banners. Text in frame: HYKSOS OUT / A PROFESSIONAL ARMY.`
- **AI motion prompt:** `Arrows sweep; march. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 072 · 09:33.3–09:41.0 (7.7 s) · A · Satellite map

**VO:** "and it had learned that the deserts were no longer enough. From now on, it would push its borders outward and build an empire."

- **Visual:** The desert walls from scene 13 crumble; Egypt's border pushes outward with a red overlay into Nubia and the Levant. The Guide points outward.
- **On-screen text:** DESERTS NOT ENOUGH / BUILD AN EMPIRE
- **Camera / animation:** Walls crumble; red expands
- **SFX / music:** rumble
- **Length:** 24 spoken words · 7.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: The desert walls from scene 13 crumble; Egypt's border pushes outward with a red overlay into Nubia and the Levant. The Guide points outward. Include the Guide exactly as in the character reference. Text in frame: DESERTS NOT ENOUGH / BUILD AN EMPIRE.`
- **AI motion prompt:** `Walls crumble; red expands. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

**Batch 6 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 7: The New Kingdom and Hatshepsut (Scenes 73–84, 09:41.0–11:19.7)

#### Scene 073 · 09:41.0–09:48.9 (7.9 s) · C · Illustrated world

**VO:** "Ahmose's victory began the New Kingdom, Egypt's richest era. Thebes became its religious heart, and its god Amun,"

- **Visual:** Thebes skyline with temples; yellow title NEW KINGDOM. Amun (blue skin, two tall plumes) appears above the city. The Guide is not in this shot.
- **On-screen text:** NEW KINGDOM / THEBES · AMUN
- **Camera / animation:** Title slam; Amun fades in
- **SFX / music:** fanfare
- **Length:** 18 spoken words · 7.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Thebes skyline with temples; yellow title NEW KINGDOM. Amun (blue skin, two tall plumes) appears above the city. Text in frame: NEW KINGDOM / THEBES · AMUN.`
- **AI motion prompt:** `Title slam; Amun fades in. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 074 · 09:48.9–09:57.3 (8.4 s) · C · Illustrated world

**VO:** "merged with the sun god Ra, became king of the gods. As the empire grew, his temple at Karnak received a large share of the plunder,"

- **Visual:** Amun and Ra merge into AMUN-RA with a sun disc. Then Karnak's tall gateway: carts of gold and treasure roll in. The Guide is not in this shot.
- **On-screen text:** AMUN + RA = KING OF THE GODS / KARNAK
- **Camera / animation:** Merge morph; carts roll
- **SFX / music:** magic merge, cart wheels
- **Length:** 26 spoken words · 8.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Amun and Ra merge into AMUN-RA with a sun disc. Then Karnak's tall gateway: carts of gold and treasure roll in. Text in frame: AMUN + RA = KING OF THE GODS / KARNAK.`
- **AI motion prompt:** `Merge morph; carts roll. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 075 · 09:57.3–10:06.0 (8.7 s) · C · Illustrated world

**VO:** "and his priests became enormously rich. … The new pharaohs went on the attack. Thutmose I led his army all the way to the Euphrates,"

- **Visual:** Bald priests in white linen sit on growing gold piles. Hard cut: Thutmose I in the blue war crown rides out in a chariot. The Guide is not in this shot.
- **On-screen text:** PRIESTS GET RICH / THUTMOSE I
- **Camera / animation:** Piles grow; hard cut
- **SFX / music:** coins, war drums
- **Length:** 25 spoken words · 8.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Bald priests in white linen sit on growing gold piles. Hard cut: Thutmose I in the blue war crown rides out in a chariot. Text in frame: PRIESTS GET RICH / THUTMOSE I.`
- **AI motion prompt:** `Piles grow; hard cut. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 076 · 10:06.0–10:12.5 (6.5 s) · A · Satellite map

**VO:** "in Syria, and deep into Nubia in the south. … Almost every pyramid had been robbed by now,"

- **Visual:** Map: Thutmose I's red arrow shoots to the EUPHRATES in Syria and another deep into NUBIA. Then robber icons pop onto almost every pyramid. The Guide is not in this shot.
- **On-screen text:** EUPHRATES · NUBIA / ROBBED
- **Camera / animation:** Arrows race out; robbers pop
- **SFX / music:** war drums, sneaky notes
- **Length:** 17 spoken words · 6.5 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map: Thutmose I's red arrow shoots to the EUPHRATES in Syria and another deep into NUBIA. Then robber icons pop onto almost every pyramid. Text in frame: EUPHRATES · NUBIA / ROBBED.`
- **AI motion prompt:** `Arrows race out; robbers pop. Gentle cartoon motion, elements pop in with a small bounce, 6 seconds.`

#### Scene 077 · 10:12.5–10:19.9 (7.4 s) · C · Illustrated world

**VO:** "so the new pharaohs hid their tombs instead, cutting them deep into a desert valley near Thebes: the Valley of the Kings."

- **Visual:** A hot desert valley near Thebes with cliffs; tombs cut deep into the rock and hidden with rubble. Big title on the cliff. The Guide peeks into a doorway.
- **On-screen text:** VALLEY OF THE KINGS
- **Camera / animation:** Push into a hidden doorway
- **SFX / music:** rock echo
- **Length:** 22 spoken words · 7.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A hot desert valley near Thebes with cliffs; tombs cut deep into the rock and hidden with rubble. Big title on the cliff. The Guide peeks into a doorway. Include the Guide exactly as in the character reference. Text in frame: VALLEY OF THE KINGS.`
- **AI motion prompt:** `Push into a hidden doorway. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 078 · 10:19.9–10:28.3 (8.4 s) · C · Illustrated world

**VO:** "Around 1479 BC, the child Thutmose III became king, and his aunt and stepmother, Hatshepsut, ruled as regent."

- **Visual:** Palace throne room: child king Thutmose III sits on a giant throne, feet dangling, crown too big. Hatshepsut stands beside him in a queen's vulture crown, holding a scroll as regent. The Guide is not in this shot.
- **On-screen text:** 1479 BC / THUTMOSE III / HATSHEPSUT, REGENT
- **Camera / animation:** Wide shot
- **SFX / music:** soft harp
- **Length:** 22 spoken words · 8.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Palace throne room: child king Thutmose III sits on a giant throne, feet dangling, crown too big. Hatshepsut stands beside him in a queen's vulture crown, holding a scroll as regent. Text in frame: 1479 BC / THUTMOSE III / HATSHEPSUT, REGENT.`
- **AI motion prompt:** `Wide shot. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 079 · 10:28.3–10:37.5 (9.2 s) · C · Illustrated world

**VO:** "Within a few years, she declared herself pharaoh, and her official images showed her with a king's headdress and the ceremonial false beard."

- **Visual:** Hatshepsut steps up onto the throne in front of the boy. With a pop she now wears the striped nemes headdress and a ceremonial false beard. Courtiers gasp; the Guide strokes his own chin.
- **On-screen text:** HATSHEPSUT, PHARAOH
- **Camera / animation:** Costume pop; glow
- **SFX / music:** gasp, crown pop
- **Length:** 23 spoken words · 9.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Hatshepsut steps up onto the throne in front of the boy. With a pop she now wears the striped nemes headdress and a ceremonial false beard. Courtiers gasp; the Guide strokes his own chin. Include the Guide exactly as in the character reference. Text in frame: HATSHEPSUT, PHARAOH.`
- **AI motion prompt:** `Costume pop; glow. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 080 · 10:37.5–10:44.7 (7.2 s) · D · Artefact / relief close-up

**VO:** "To justify her rule, she had her temple walls carved with scenes showing the god Amun as her real father."

- **Visual:** Temple wall carving in the cartoon relief style: the god Amun (blue skin, tall plumes) holding a baby Hatshepsut, with a family-tree line AMUN → HATSHEPSUT. The Guide is not in this shot.
- **On-screen text:** AMUN = HER "FATHER"
- **Camera / animation:** Slow pan across the carving
- **SFX / music:** chisel taps
- **Length:** 20 spoken words · 7.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: Temple wall carving in the cartoon relief style: the god Amun (blue skin, tall plumes) holding a baby Hatshepsut, with a family-tree line AMUN → HATSHEPSUT. Text in frame: AMUN = HER "FATHER".`
- **AI motion prompt:** `Slow pan across the carving. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 081 · 10:44.7–10:54.1 (9.4 s) · A · Satellite map

**VO:** "She ruled for about 20 years, mostly through trade and building rather than war. Her expedition to Punt, on Africa's Red Sea coast, brought back incense,"

- **Visual:** A 20 YEARS label; a chariot gets a red X and is replaced by trade ships. Satellite map of the Red Sea: five ships sail from Egypt down to PUNT on the African coast. The Guide is not in this shot.
- **On-screen text:** 20 YEARS: TRADE, NOT WAR / PUNT
- **Camera / animation:** Route animates
- **SFX / music:** sail flap, waves
- **Length:** 26 spoken words · 9.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: A 20 YEARS label; a chariot gets a red X and is replaced by trade ships. Satellite map of the Red Sea: five ships sail from Egypt down to PUNT on the African coast. Text in frame: 20 YEARS: TRADE, NOT WAR / PUNT.`
- **AI motion prompt:** `Route animates. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 082 · 10:54.1–11:03.3 (9.2 s) · C · Illustrated world

**VO:** "ebony and living myrrh trees, and her terraced temple at Deir el-Bahari still stands. She also raised giant granite obelisks at Karnak."

- **Visual:** Ships return with incense bags, ebony logs and myrrh trees in pots. Cut: the three wide terraces of Deir el-Bahari against golden cliffs, the Guide waving at the bottom. Then two pink granite obelisks rise at Karnak.
- **On-screen text:** DEIR EL-BAHARI / GRANITE OBELISKS
- **Camera / animation:** Cut; obelisks rise
- **SFX / music:** seagulls, stone rumble
- **Length:** 23 spoken words · 9.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Ships return with incense bags, ebony logs and myrrh trees in pots. Cut: the three wide terraces of Deir el-Bahari against golden cliffs, the Guide waving at the bottom. Then two pink granite obelisks rise at Karnak. Include the Guide exactly as in the character reference. Text in frame: DEIR EL-BAHARI / GRANITE OBELISKS.`
- **AI motion prompt:** `Cut; obelisks rise. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 083 · 11:03.3–11:11.5 (8.2 s) · C · Illustrated world

**VO:** "Years after her death, her statues were smashed and her name was chiselled off monuments, most likely on Thutmose III's orders."

- **Visual:** "Years later": the scene turns grey. Her statues lie smashed on the ground; a worker chisels her name out of a cartouche while dust puffs fly. An adult Thutmose III watches with arms crossed. The Guide is not in this shot.
- **On-screen text:** ERASED
- **Camera / animation:** Chisel strikes on the beat
- **SFX / music:** hammer smashes, chisel
- **Length:** 22 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: "Years later": the scene turns grey. Her statues lie smashed on the ground; a worker chisels her name out of a cartouche while dust puffs fly. An adult Thutmose III watches with arms crossed. Text in frame: ERASED.`
- **AI motion prompt:** `Chisel strikes on the beat. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 084 · 11:11.5–11:19.7 (8.2 s) · B · Grey studio

**VO:** "Later official king lists left her out entirely. … Once he ruled alone, Thutmose III became Egypt's greatest conqueror."

- **Visual:** Grey studio. A long scroll king list unrolls: the names jump from Thutmose II straight to Thutmose III with a blank gap. The Guide puts his ear near the gap, puzzled. Then Thutmose III steps in wearing the blue war crown, bow in hand.
- **On-screen text:** LEFT OUT / THUTMOSE III: GREATEST CONQUEROR
- **Camera / animation:** Scroll unrolls; zoom on gap; slide in
- **SFX / music:** scroll, war drum
- **Length:** 19 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio. A long scroll king list unrolls: the names jump from Thutmose II straight to Thutmose III with a blank gap. The Guide puts his ear near the gap, puzzled. Then Thutmose III steps in wearing the blue war crown, bow in hand. Include the Guide exactly as in the character reference. Text in frame: LEFT OUT / THUTMOSE III: GREATEST CONQUEROR.`
- **AI motion prompt:** `Scroll unrolls; zoom on gap; slide in. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

**Batch 7 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 8: Thutmose III and Akhenaten (Scenes 85–100, 11:19.7–13:32.9)

#### Scene 085 · 11:19.7–11:29.4 (9.7 s) · A · Satellite map

**VO:** "Around 1457 BC, rebel kings gathered at Megiddo, in what is now northern Israel. Thutmose took the narrowest of three routes,"

- **Visual:** Satellite map of the Levant. Rebel king icons with little crowns gather at a fortress pin: MEGIDDO (northern Israel). Three dotted routes lead there across a mountain ridge; the narrow middle pass glows yellow as Thutmose chooses it. The Guide is not in this shot.
- **On-screen text:** 1457 BC / MEGIDDO / 3 ROUTES
- **Camera / animation:** Routes draw one by one; middle highlights
- **SFX / music:** map pings, tension strings
- **Length:** 24 spoken words · 9.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map of the Levant. Rebel king icons with little crowns gather at a fortress pin: MEGIDDO (northern Israel). Three dotted routes lead there across a mountain ridge; the narrow middle pass glows yellow as Thutmose chooses it. Text in frame: 1457 BC / MEGIDDO / 3 ROUTES.`
- **AI motion prompt:** `Routes draw one by one; middle highlights. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 086 · 11:29.4–11:37.1 (7.7 s) · C · Illustrated world

**VO:** "a pass so tight his army marched in single file, and caught them by surprise. After a seven-month siege, Megiddo fell."

- **Visual:** A tight mountain pass: soldiers walk in single file, the Guide squeezed among them. They burst out and the rebels jump in surprise. Then Megiddo's walls under siege; a counter 1 → 7 MONTHS; the gates open with a white flag.
- **On-screen text:** SINGLE FILE / 7-MONTH SIEGE / MEGIDDO FALLS
- **Camera / animation:** Side-scroll; counter ticks; gates swing open
- **SFX / music:** marching, surprise sting, gate creak
- **Length:** 22 spoken words · 7.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A tight mountain pass: soldiers walk in single file, the Guide squeezed among them. They burst out and the rebels jump in surprise. Then Megiddo's walls under siege; a counter 1 → 7 MONTHS; the gates open with a white flag. Include the Guide exactly as in the character reference. Text in frame: SINGLE FILE / 7-MONTH SIEGE / MEGIDDO FALLS.`
- **AI motion prompt:** `Side-scroll; counter ticks; gates swing open. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 087 · 11:37.1–11:45.3 (8.2 s) · D · Artefact / relief close-up

**VO:** "We know these details because Thutmose had his campaigns carved on the walls of Karnak, listing battles, captured cities and tribute,"

- **Visual:** A long carved wall at Karnak in cartoon relief style: rows of captured city name-rings, chariots and lines of tribute bearers. The Guide walks along it reading.
- **On-screen text:** THE ANNALS OF THUTMOSE III
- **Camera / animation:** Long horizontal pan along the wall
- **SFX / music:** chisel taps, crowd
- **Length:** 21 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: A long carved wall at Karnak in cartoon relief style: rows of captured city name-rings, chariots and lines of tribute bearers. The Guide walks along it reading. Include the Guide exactly as in the character reference. Text in frame: THE ANNALS OF THUTMOSE III.`
- **AI motion prompt:** `Long horizontal pan along the wall. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 088 · 11:45.3–11:53.0 (7.7 s) · A · Satellite map

**VO:** "much of it given to Amun's temple. … Over about 17 campaigns, he built the largest empire Egypt ever had,"

- **Visual:** Tribute (gold, horses, chariots) flows through Amun's temple gate. Then the satellite map: a counter ticks from 1 to 17 CAMPAIGNS, each tick adding red to the empire. The Guide is not in this shot.
- **On-screen text:** 17 CAMPAIGNS / LARGEST EMPIRE EGYPT EVER HAD
- **Camera / animation:** Red expands with each tick
- **SFX / music:** counter clicks, rumble
- **Length:** 19 spoken words · 7.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Tribute (gold, horses, chariots) flows through Amun's temple gate. Then the satellite map: a counter ticks from 1 to 17 CAMPAIGNS, each tick adding red to the empire. Text in frame: 17 CAMPAIGNS / LARGEST EMPIRE EGYPT EVER HAD.`
- **AI motion prompt:** `Red expands with each tick. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 089 · 11:53.0–12:01.2 (8.2 s) · A · Satellite map

**VO:** "stretching from Syria to deep into Sudan, with Nubia's gold mines under Egyptian control. … He also found a way to hold it."

- **Visual:** The red empire now reaches from SYRIA down to SUDAN; gold-mine icons sparkle in NUBIA. The Guide, bottom right, holds a gold nugget up to the light.
- **On-screen text:** SYRIA → SUDAN / NUBIAN GOLD
- **Camera / animation:** Sparkles on the mines
- **SFX / music:** gold sparkle
- **Length:** 22 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: The red empire now reaches from SYRIA down to SUDAN; gold-mine icons sparkle in NUBIA. The Guide, bottom right, holds a gold nugget up to the light. Include the Guide exactly as in the character reference. Text in frame: SYRIA → SUDAN / NUBIAN GOLD.`
- **AI motion prompt:** `Sparkles on the mines. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 090 · 12:01.2–12:09.4 (8.2 s) · C · Illustrated world

**VO:** "Sons of conquered rulers were brought to Egypt and raised at court. When they went home to rule, they had grown up Egyptian, and loyal."

- **Visual:** A boat arrives at the palace: young foreign princes step off in foreign clothes. Quick montage: they learn hieroglyphs, wear Egyptian linen, grow taller. Then they sail home dressed as Egyptians and bow toward Egypt. The Guide is not in this shot.
- **On-screen text:** RAISED AT COURT / GROWN UP EGYPTIAN
- **Camera / animation:** Time-lapse growth; boat leaves
- **SFX / music:** school bell, sailing
- **Length:** 25 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A boat arrives at the palace: young foreign princes step off in foreign clothes. Quick montage: they learn hieroglyphs, wear Egyptian linen, grow taller. Then they sail home dressed as Egyptians and bow toward Egypt. Text in frame: RAISED AT COURT / GROWN UP EGYPTIAN.`
- **AI motion prompt:** `Time-lapse growth; boat leaves. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 091 · 12:09.4–12:18.3 (8.9 s) · C · Illustrated world

**VO:** "By the reign of Amenhotep III, Egypt was a superpower, rich enough to spend almost four decades building rather than fighting."

- **Visual:** Amenhotep III, wide and smiling on a gold throne. Behind him temples and giant statues build up in time-lapse. A balance tips: BUILDING heavy, FIGHTING light. The Guide is not in this shot.
- **On-screen text:** AMENHOTEP III / SUPERPOWER / ~40 YEARS OF BUILDING
- **Camera / animation:** Time-lapse; balance tips
- **SFX / music:** construction, celebratory brass
- **Length:** 22 spoken words · 8.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Amenhotep III, wide and smiling on a gold throne. Behind him temples and giant statues build up in time-lapse. A balance tips: BUILDING heavy, FIGHTING light. Text in frame: AMENHOTEP III / SUPERPOWER / ~40 YEARS OF BUILDING.`
- **AI motion prompt:** `Time-lapse; balance tips. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 092 · 12:18.3–12:28.7 (10.4 s) · B · Grey studio

**VO:** "Clay tablets later found at Amarna preserve letters from the kings of Babylon and other great powers, writing to the pharaoh as equals and asking him for gold."

- **Visual:** Grey studio. Clay tablets with wedge-shaped writing pop in, labelled BABYLON, MITANNI, HITTITES. Speech bubbles: "My brother, send gold!" The pharaoh sits at the same height as the other kings. The Guide chuckles.
- **On-screen text:** AMARNA LETTERS / "SEND GOLD"
- **Camera / animation:** Tablets pop; bubbles bounce
- **SFX / music:** clay clinks, chuckle
- **Length:** 28 spoken words · 10.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio. Clay tablets with wedge-shaped writing pop in, labelled BABYLON, MITANNI, HITTITES. Speech bubbles: "My brother, send gold!" The pharaoh sits at the same height as the other kings. The Guide chuckles. Include the Guide exactly as in the character reference. Text in frame: AMARNA LETTERS / "SEND GOLD".`
- **AI motion prompt:** `Tablets pop; bubbles bounce. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 093 · 12:28.7–12:36.6 (7.9 s) · C · Illustrated world

**VO:** "Then his son broke the system. Amenhotep IV pushed aside Egypt's many gods for one, the Aten, the disc of the sun,"

- **Visual:** Akhenaten (long face, tall blue crown) raises his arms to a single sun disc whose rays end in little hands. Behind him the many gods (falcon, jackal, ram, cow) fade out one by one. The Guide is not in this shot.
- **On-screen text:** ONE GOD: THE ATEN
- **Camera / animation:** Gods fade in sequence
- **SFX / music:** choir rising, wind
- **Length:** 23 spoken words · 7.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Akhenaten (long face, tall blue crown) raises his arms to a single sun disc whose rays end in little hands. Behind him the many gods (falcon, jackal, ram, cow) fade out one by one. Text in frame: ONE GOD: THE ATEN.`
- **AI motion prompt:** `Gods fade in sequence. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 094 · 12:36.6–12:45.0 (8.4 s) · C · Illustrated world

**VO:** "and renamed himself Akhenaten. Many historians see this partly as a move against the rich and powerful priests of Amun."

- **Visual:** Name tag swaps AMENHOTEP IV → AKHENATEN. Then rich priests of Amun sit on their gold, frowning, as the Aten's shadow falls over them. The Guide is not in this shot.
- **On-screen text:** AKHENATEN / A MOVE AGAINST THE PRIESTS?
- **Camera / animation:** Name swap; shadow sweeps
- **SFX / music:** swoosh, ominous note
- **Length:** 20 spoken words · 8.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Name tag swaps AMENHOTEP IV → AKHENATEN. Then rich priests of Amun sit on their gold, frowning, as the Aten's shadow falls over them. Text in frame: AKHENATEN / A MOVE AGAINST THE PRIESTS?.`
- **AI motion prompt:** `Name swap; shadow sweeps. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 095 · 12:45.0–12:52.4 (7.4 s) · C · Illustrated world

**VO:** "He built a new capital, now called Amarna, closed the old temples, and had Amun's name hacked off monuments."

- **Visual:** A desert plain: a brand-new city builds in fast time-lapse: AMARNA. Temple doors slam shut with a padlock; a worker hacks the name AMUN off a wall. The Guide is not in this shot.
- **On-screen text:** AMARNA / TEMPLES CLOSED / AMUN ERASED
- **Camera / animation:** Time-lapse; slam; chisel
- **SFX / music:** construction, door slam, chisel
- **Length:** 19 spoken words · 7.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A desert plain: a brand-new city builds in fast time-lapse: AMARNA. Temple doors slam shut with a padlock; a worker hacks the name AMUN off a wall. Text in frame: AMARNA / TEMPLES CLOSED / AMUN ERASED.`
- **AI motion prompt:** `Time-lapse; slam; chisel. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 096 · 12:52.4–13:00.6 (8.2 s) · C · Illustrated world

**VO:** "Only the king and his queen, Nefertiti, were shown worshipping the Aten directly. Everyone else was meant to worship through them."

- **Visual:** Akhenaten and Nefertiti alone under the sun's rays, while everyone else bows to them; arrows show the rays reach the people only through the royal couple. The Guide is not in this shot.
- **On-screen text:** ONLY THE KING AND QUEEN
- **Camera / animation:** Diagram arrows draw
- **SFX / music:** choir
- **Length:** 21 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Akhenaten and Nefertiti alone under the sun's rays, while everyone else bows to them; arrows show the rays reach the people only through the royal couple. Text in frame: ONLY THE KING AND QUEEN.`
- **AI motion prompt:** `Diagram arrows draw. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 097 · 13:00.6–13:07.8 (7.2 s) · D · Artefact / relief close-up

**VO:** "Art changed too. The royal family was shown with long faces and rounded bodies, in relaxed family scenes,"

- **Visual:** Amarna-style art: the royal family with long faces and rounded bodies, kissing and playing with their daughters. The Guide tilts his head, curious.
- **On-screen text:** ART CHANGED TOO
- **Camera / animation:** Slow push-in
- **SFX / music:** harp, curious note
- **Length:** 18 spoken words · 7.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: Amarna-style art: the royal family with long faces and rounded bodies, kissing and playing with their daughters. The Guide tilts his head, curious. Include the Guide exactly as in the character reference. Text in frame: ART CHANGED TOO.`
- **AI motion prompt:** `Slow push-in. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 098 · 13:07.8–13:15.0 (7.2 s) · D · Artefact / relief close-up

**VO:** "a sharp break from 1,500 years of stiff, idealised royal images. … Meanwhile, the empire drifted."

- **Visual:** Split screen: stiff, straight royal portraits on the left (with a 1,500 YEARS bar) vs the relaxed Amarna family on the right. Then the satellite map behind them shows the empire's red edges flickering. The Guide is not in this shot.
- **On-screen text:** A SHARP BREAK / THE EMPIRE DRIFTED
- **Camera / animation:** Wipe; red edges flicker
- **SFX / music:** wind, worried strings
- **Length:** 18 spoken words · 7.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: Split screen: stiff, straight royal portraits on the left (with a 1,500 YEARS bar) vs the relaxed Amarna family on the right. Then the satellite map behind them shows the empire's red edges flickering. Text in frame: A SHARP BREAK / THE EMPIRE DRIFTED.`
- **AI motion prompt:** `Wipe; red edges flicker. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 099 · 13:15.0–13:23.2 (8.2 s) · B · Grey studio

**VO:** "Among the Amarna letters are pleas from Egypt's vassal rulers in Canaan, begging the pharaoh for troops against their enemies."

- **Visual:** Grey studio. Clay-tablet letters fly in from CANAAN: "Send troops!", "Help!", "Hurry!" They pile up on an empty desk. The Guide taps a sleeping messenger.
- **On-screen text:** PLEAS FROM CANAAN
- **Camera / animation:** Letters pile up
- **SFX / music:** tablet thuds, snore
- **Length:** 20 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio. Clay-tablet letters fly in from CANAAN: "Send troops!", "Help!", "Hurry!" They pile up on an empty desk. The Guide taps a sleeping messenger. Include the Guide exactly as in the character reference. Text in frame: PLEAS FROM CANAAN.`
- **AI motion prompt:** `Letters pile up. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 100 · 13:23.2–13:32.9 (9.7 s) · C · Illustrated world

**VO:** "Some seem to have gone unanswered. … His revolution didn't survive him. After his death, Amarna was abandoned, and Egypt went back to its old gods."

- **Visual:** Cobwebs draw over the letter pile. Then Amarna is empty, sand blowing through the streets; the old temples reopen and the gods' statues return. The Guide is not in this shot.
- **On-screen text:** UNANSWERED / BACK TO THE OLD GODS
- **Camera / animation:** Cobweb; sand wind; doors reopen
- **SFX / music:** wind, doors creak open
- **Length:** 25 spoken words · 9.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Cobwebs draw over the letter pile. Then Amarna is empty, sand blowing through the streets; the old temples reopen and the gods' statues return. Text in frame: UNANSWERED / BACK TO THE OLD GODS.`
- **AI motion prompt:** `Cobweb; sand wind; doors reopen. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

**Batch 8 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 9: Tutankhamun (Scenes 101–112, 13:32.9–15:10.9)

#### Scene 101 · 13:32.9–13:42.8 (9.9 s) · C · Illustrated world

**VO:** "The boy who soon took the throne, Tutankhaten, was about nine. His advisers reopened the old temples and changed his name to honour Amun: Tutankhamun."

- **Visual:** A small, nervous 9-year-old boy king on a big throne. Advisers (an old vizier and a general) swap his name tag TUTANKH-ATEN → TUTANKH-AMUN while temple doors reopen behind him. The Guide is not in this shot.
- **On-screen text:** AGE 9 / TUTANKHAMUN
- **Camera / animation:** Push in; name swap
- **SFX / music:** tick, soft harp
- **Length:** 25 spoken words · 9.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A small, nervous 9-year-old boy king on a big throne. Advisers (an old vizier and a general) swap his name tag TUTANKH-ATEN → TUTANKH-AMUN while temple doors reopen behind him. Text in frame: AGE 9 / TUTANKHAMUN.`
- **AI motion prompt:** `Push in; name swap. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 102 · 13:42.8–13:51.7 (8.9 s) · C · Illustrated world

**VO:** "He died at around 19, and the exact cause is still debated. … A few years later, the army commander Horemheb became pharaoh."

- **Visual:** An age counter rolls 9 → 19, then a soft fade with a question mark (cause of death?). Hard cut: general Horemheb, in armour and the blue war crown, steps onto the throne. The Guide is not in this shot.
- **On-screen text:** DIED ~19 / CAUSE? / HOREMHEB
- **Camera / animation:** Counter; fade; hard cut
- **SFX / music:** soft note, drum
- **Length:** 22 spoken words · 8.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: An age counter rolls 9 → 19, then a soft fade with a question mark (cause of death?). Hard cut: general Horemheb, in armour and the blue war crown, steps onto the throne. Text in frame: DIED ~19 / CAUSE? / HOREMHEB.`
- **AI motion prompt:** `Counter; fade; hard cut. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 103 · 13:51.7–14:00.4 (8.7 s) · C · Illustrated world

**VO:** "He tore down Akhenaten's temples, reused their blocks, and wiped the Amarna kings, Tutankhamun included, from the official record."

- **Visual:** Workers knock down Akhenaten's temples and carry the blocks away to reuse. A king-list scroll fades out AKHENATEN, SMENKHKARE, TUTANKHAMUN, AY one by one. The Guide is not in this shot.
- **On-screen text:** ERASED FROM THE RECORD
- **Camera / animation:** Demolition with dust; names fade
- **SFX / music:** crash, eraser squeaks
- **Length:** 19 spoken words · 8.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Workers knock down Akhenaten's temples and carry the blocks away to reuse. A king-list scroll fades out AKHENATEN, SMENKHKARE, TUTANKHAMUN, AY one by one. Text in frame: ERASED FROM THE RECORD.`
- **AI motion prompt:** `Demolition with dust; names fade. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 104 · 14:00.4–14:07.8 (7.4 s) · C · Illustrated world

**VO:** "That's partly why Tutankhamun was forgotten. He had been buried in a small, hastily prepared tomb, and later,"

- **Visual:** A small, plain tomb in the Valley of the Kings, hastily packed with a few items. The Guide shrugs at its size.
- **On-screen text:** FORGOTTEN / A SMALL, HASTY TOMB
- **Camera / animation:** Push in
- **SFX / music:** wind
- **Length:** 18 spoken words · 7.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A small, plain tomb in the Valley of the Kings, hastily packed with a few items. The Guide shrugs at its size. Include the Guide exactly as in the character reference. Text in frame: FORGOTTEN / A SMALL, HASTY TOMB.`
- **AI motion prompt:** `Push in. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 105 · 14:07.8–14:17.2 (9.4 s) · C · Illustrated world

**VO:** "workers digging a nearby tomb piled their debris over its entrance. Unlike almost every other royal tomb, it was never emptied by robbers."

- **Visual:** Workers digging a nearby tomb dump rubble over the small tomb's doorway until it is invisible. Time-lapse: tomb robbers walk past again and again, never noticing. The Guide is not in this shot.
- **On-screen text:** NEVER ROBBED
- **Camera / animation:** Rubble piles up; day/night time-lapse
- **SFX / music:** rubble, footsteps
- **Length:** 23 spoken words · 9.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Workers digging a nearby tomb dump rubble over the small tomb's doorway until it is invisible. Time-lapse: tomb robbers walk past again and again, never noticing. Text in frame: NEVER ROBBED.`
- **AI motion prompt:** `Rubble piles up; day/night time-lapse. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 106 · 14:17.2–14:24.9 (7.7 s) · D · Artefact / relief close-up

**VO:** "In November 1922, British archaeologist Howard Carter uncovered its steps and sealed doorway."

- **Visual:** November 1922: Howard Carter (moustache, hat, lamp) and workers uncover the first stone step, then more steps, down to a doorway sealed with plaster and seals. The Guide is not in this shot.
- **On-screen text:** NOVEMBER 1922 / HOWARD CARTER
- **Camera / animation:** Tilt down the steps
- **SFX / music:** shovel scrapes, whisper
- **Length:** 15 spoken words · 7.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: November 1922: Howard Carter (moustache, hat, lamp) and workers uncover the first stone step, then more steps, down to a doorway sealed with plaster and seals. Text in frame: NOVEMBER 1922 / HOWARD CARTER.`
- **AI motion prompt:** `Tilt down the steps. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 107 · 14:24.9–14:32.1 (7.2 s) · C · Illustrated world

**VO:** "When his sponsor, Lord Carnarvon, asked if he could see anything inside, Carter answered: "Yes, wonderful things.""

- **Visual:** Lord Carnarvon stands behind Carter, asking. Carter peeks through a hole with a candle; gold glints in the dark. The Guide peeks over their shoulders. Big quote text.
- **On-screen text:** "YES, WONDERFUL THINGS."
- **Camera / animation:** Candle glow; gold glint
- **SFX / music:** gasp, sparkle
- **Length:** 17 spoken words · 7.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Lord Carnarvon stands behind Carter, asking. Carter peeks through a hole with a candle; gold glints in the dark. The Guide peeks over their shoulders. Big quote text. Include the Guide exactly as in the character reference. Text in frame: "YES, WONDERFUL THINGS.".`
- **AI motion prompt:** `Candle glow; gold glint. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 108 · 14:32.1–14:39.0 (6.9 s) · C · Illustrated world

**VO:** "Inside were more than 5,000 objects. The king lay in three nested coffins, the innermost made of solid gold,"

- **Visual:** A counter rolls to 5,000+ OBJECTS as treasures fill the room. Then three coffins slide apart like nesting dolls: wooden, gilded, then solid gold. The Guide is not in this shot.
- **On-screen text:** 5,000+ OBJECTS / 3 NESTED COFFINS
- **Camera / animation:** Counter; coffins slide one by one
- **SFX / music:** counter, heavy slide
- **Length:** 20 spoken words · 6.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A counter rolls to 5,000+ OBJECTS as treasures fill the room. Then three coffins slide apart like nesting dolls: wooden, gilded, then solid gold. Text in frame: 5,000+ OBJECTS / 3 NESTED COFFINS.`
- **AI motion prompt:** `Counter; coffins slide one by one. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 109 · 14:39.0–14:46.7 (7.7 s) · C · Illustrated world

**VO:** "about 110 kilograms, with the famous gold mask over his face. And this was the burial of a minor king,"

- **Visual:** A scale under the gold coffin reads 110 KG. The famous gold mask appears and glows; the Guide shields his eyes. A small label pops: A MINOR KING.
- **On-screen text:** 110 KG / THE GOLD MASK / A MINOR KING
- **Camera / animation:** Glow pulse
- **SFX / music:** shimmer, ding
- **Length:** 23 spoken words · 7.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A scale under the gold coffin reads 110 KG. The famous gold mask appears and glows; the Guide shields his eyes. A small label pops: A MINOR KING. Include the Guide exactly as in the character reference. Text in frame: 110 KG / THE GOLD MASK / A MINOR KING.`
- **AI motion prompt:** `Glow pulse. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 110 · 14:46.7–14:54.1 (7.4 s) · B · Grey studio

**VO:** "which tells you how much was lost from the others. … The discovery made Tutankhamun the most famous pharaoh in the world."

- **Visual:** A small Tutankhamun icon next to the giant, empty tombs of great kings (cobwebs). The Guide spreads his arms wide. Then a world map lights up with the gold mask in the middle.
- **On-screen text:** HOW MUCH WAS LOST / MOST FAMOUS PHARAOH IN THE WORLD
- **Camera / animation:** Scale comparison; world map glows
- **SFX / music:** ding, crowd murmur
- **Length:** 21 spoken words · 7.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: A small Tutankhamun icon next to the giant, empty tombs of great kings (cobwebs). The Guide spreads his arms wide. Then a world map lights up with the gold mask in the middle. Include the Guide exactly as in the character reference. Text in frame: HOW MUCH WAS LOST / MOST FAMOUS PHARAOH IN THE WORLD.`
- **AI motion prompt:** `Scale comparison; world map glows. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 111 · 14:54.1–15:03.0 (8.9 s) · C · Illustrated world

**VO:** "It came in the same year Egypt won formal independence from Britain, and Egyptians embraced the boy king as a symbol of their nation."

- **Visual:** Cairo, 1922, sunny sky: a cheering crowd waves flags and banners with Tutankhamun's gold mask. A British flag lowers on one pole while an Egyptian flag rises on another. The Guide waves his hat in the crowd.
- **On-screen text:** 1922 / INDEPENDENCE FROM BRITAIN / SYMBOL OF THE NATION
- **Camera / animation:** Flags swap; push in on the banners
- **SFX / music:** cheering crowd, flag flutter
- **Length:** 24 spoken words · 8.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Cairo, 1922, sunny sky: a cheering crowd waves flags and banners with Tutankhamun's gold mask. A British flag lowers on one pole while an Egyptian flag rises on another. The Guide waves his hat in the crowd. Include the Guide exactly as in the character reference. Text in frame: 1922 / INDEPENDENCE FROM BRITAIN / SYMBOL OF THE NATION.`
- **AI motion prompt:** `Flags swap; push in on the banners. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 112 · 15:03.0–15:10.9 (7.9 s) · C · Illustrated world

**VO:** "The treasures stayed in Egypt. … Horemheb had no heir, so he passed the throne to another general, Ramesses I."

- **Visual:** A museum hall in Egypt: the gold mask behind glass with an EGYPT stamp. Hard cut to the ancient palace: an old Horemheb, no children beside him, hands the crown to a grey-haired general, Ramesses I. The Guide is not in this shot.
- **On-screen text:** THE TREASURES STAYED IN EGYPT / RAMESSES I
- **Camera / animation:** Museum pan; whoosh cut; handover
- **SFX / music:** museum hush, fanfare
- **Length:** 20 spoken words · 7.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A museum hall in Egypt: the gold mask behind glass with an EGYPT stamp. Hard cut to the ancient palace: an old Horemheb, no children beside him, hands the crown to a grey-haired general, Ramesses I. Text in frame: THE TREASURES STAYED IN EGYPT / RAMESSES I.`
- **AI motion prompt:** `Museum pan; whoosh cut; handover. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

**Batch 9 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 10: Ramesses II and the Bronze Age collapse (Scenes 113–123, 15:10.9–16:37.1)

#### Scene 113 · 15:10.9–15:17.6 (6.7 s) · C · Illustrated world

**VO:** "His family, the Ramessides, were soldiers from the delta, and they set out to rebuild Egypt's empire."

- **Visual:** A family of soldier-kings (the Ramessides) marches out of the green delta under falcon banners. A red empire arrow begins to draw on a small map card. The Guide is not in this shot.
- **On-screen text:** THE RAMESSIDES / REBUILD THE EMPIRE
- **Camera / animation:** Side-scroll march
- **SFX / music:** marching feet, drum
- **Length:** 17 spoken words · 6.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A family of soldier-kings (the Ramessides) marches out of the green delta under falcon banners. A red empire arrow begins to draw on a small map card. Text in frame: THE RAMESSIDES / REBUILD THE EMPIRE.`
- **AI motion prompt:** `Side-scroll march. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 114 · 15:17.6–15:25.0 (7.4 s) · A · Satellite map

**VO:** "The most famous was Ramesses II, who reigned for 66 years. He built a new capital, Pi-Ramesses,"

- **Visual:** Ramesses II steps to the front, tall and proud in the double crown; a counter rolls to 66 YEARS. Then on the satellite map a new capital pin PI-RAMESSES drops in the eastern delta. The Guide is not in this shot.
- **On-screen text:** RAMESSES II · 66 YEARS / PI-RAMESSES
- **Camera / animation:** Counter; pin drop
- **SFX / music:** drum roll, ping
- **Length:** 20 spoken words · 7.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Ramesses II steps to the front, tall and proud in the double crown; a counter rolls to 66 YEARS. Then on the satellite map a new capital pin PI-RAMESSES drops in the eastern delta. Text in frame: RAMESSES II · 66 YEARS / PI-RAMESSES.`
- **AI motion prompt:** `Counter; pin drop. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 115 · 15:25.0–15:32.4 (7.4 s) · A · Satellite map

**VO:** "in the eastern delta, closer to the frontier in Asia, and filled Egypt with temples and giant statues of himself,"

- **Visual:** A dotted line runs from Pi-Ramesses to the Asian frontier (Sinai). Temple and giant-statue icons, each with Ramesses' face, pop up all along the Nile. The Guide counts them on his fingers and gives up.
- **On-screen text:** CLOSER TO ASIA / STATUES EVERYWHERE
- **Camera / animation:** Cascade of pops
- **SFX / music:** cascading pops
- **Length:** 20 spoken words · 7.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: A dotted line runs from Pi-Ramesses to the Asian frontier (Sinai). Temple and giant-statue icons, each with Ramesses' face, pop up all along the Nile. The Guide counts them on his fingers and gives up. Include the Guide exactly as in the character reference. Text in frame: CLOSER TO ASIA / STATUES EVERYWHERE.`
- **AI motion prompt:** `Cascade of pops. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 116 · 15:32.4–15:40.6 (8.2 s) · C · Illustrated world

**VO:** "including the four colossal figures at Abu Simbel. Later Egyptians remembered him as the greatest king of all,"

- **Visual:** Abu Simbel at sunrise: four colossal seated statues of Ramesses carved into a sandstone cliff. The Guide stands at the foot of one, smaller than its toe.
- **On-screen text:** ABU SIMBEL / "THE GREATEST KING OF ALL"
- **Camera / animation:** Slow tilt up the statues
- **SFX / music:** sunrise strings
- **Length:** 18 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Abu Simbel at sunrise: four colossal seated statues of Ramesses carved into a sandstone cliff. The Guide stands at the foot of one, smaller than its toe. Include the Guide exactly as in the character reference. Text in frame: ABU SIMBEL / "THE GREATEST KING OF ALL".`
- **AI motion prompt:** `Slow tilt up the statues. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 117 · 15:40.6–15:48.8 (8.2 s) · A · Satellite map

**VO:** "and nine later pharaohs took his name. … In 1274 BC, he fought the Hittite empire for control of Syria at Kadesh,"

- **Visual:** Nine yellow name tags pop: RAMESSES III … RAMESSES XI. Then the satellite map: Egypt in red, the Hittite Empire in purple; two thick arrows grow toward a pin at KADESH in Syria. The Guide is not in this shot.
- **On-screen text:** 9 MORE RAMESSES / 1274 BC · KADESH
- **Camera / animation:** Tags pop; arrows grow
- **SFX / music:** nine pops, war horns
- **Length:** 24 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Nine yellow name tags pop: RAMESSES III … RAMESSES XI. Then the satellite map: Egypt in red, the Hittite Empire in purple; two thick arrows grow toward a pin at KADESH in Syria. Text in frame: 9 MORE RAMESSES / 1274 BC · KADESH.`
- **AI motion prompt:** `Tags pop; arrows grow. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 118 · 15:48.8–15:56.2 (7.4 s) · C · Illustrated world

**VO:** "in one of the largest chariot battles in history. Ramesses was caught in an ambush and had to fight his way out."

- **Visual:** Dozens of chariots fill the plain. Hittite chariots burst from behind a hill and surround Ramesses' camp; Ramesses fires arrows from his chariot and breaks out. The Guide is not in this shot.
- **On-screen text:** ONE OF THE LARGEST CHARIOT BATTLES / AMBUSH
- **Camera / animation:** Shaky action camera
- **SFX / music:** chariot thunder, clashes
- **Length:** 22 spoken words · 7.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Dozens of chariots fill the plain. Hittite chariots burst from behind a hill and surround Ramesses' camp; Ramesses fires arrows from his chariot and breaks out. Text in frame: ONE OF THE LARGEST CHARIOT BATTLES / AMBUSH.`
- **AI motion prompt:** `Shaky action camera. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 119 · 15:56.2–16:04.9 (8.7 s) · C · Illustrated world

**VO:** "The battle ended without a clear winner, though Ramesses advertised it at home as a great victory. … About 15 years later,"

- **Visual:** A scoreboard card: EGYPT 1 – HITTITES 1. Cut to Egypt: a giant temple banner GREAT VICTORY! unrolls. The Guide rolls his eyes at the camera.
- **On-screen text:** NO CLEAR WINNER / "GREAT VICTORY!"
- **Camera / animation:** Banner unrolls; comic freeze on the Guide
- **SFX / music:** horn, comic ding
- **Length:** 21 spoken words · 8.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A scoreboard card: EGYPT 1 – HITTITES 1. Cut to Egypt: a giant temple banner GREAT VICTORY! unrolls. The Guide rolls his eyes at the camera. Include the Guide exactly as in the character reference. Text in frame: NO CLEAR WINNER / "GREAT VICTORY!".`
- **AI motion prompt:** `Banner unrolls; comic freeze on the Guide. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 120 · 16:04.9–16:13.1 (8.2 s) · D · Artefact / relief close-up

**VO:** "the two empires signed one of the earliest peace treaties whose text survives, promising to help each other against attackers."

- **Visual:** A clay-tablet treaty with Egyptian and Hittite seals. Above it, two hands shake; small shield icons appear on both sides (help each other against attackers). The Guide is not in this shot.
- **On-screen text:** ~15 YEARS LATER / ONE OF THE EARLIEST SURVIVING PEACE TREATIES
- **Camera / animation:** Slow zoom on the tablet; handshake pops
- **SFX / music:** clay stamp, warm strings
- **Length:** 20 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: A clay-tablet treaty with Egyptian and Hittite seals. Above it, two hands shake; small shield icons appear on both sides (help each other against attackers). Text in frame: ~15 YEARS LATER / ONE OF THE EARLIEST SURVIVING PEACE TREATIES.`
- **AI motion prompt:** `Slow zoom on the tablet; handshake pops. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 121 · 16:13.1–16:20.5 (7.4 s) · C · Illustrated world

**VO:** "Ramesses later married a Hittite princess to seal the peace. … Around 1200 BC, the Bronze Age world collapsed."

- **Visual:** A royal wedding: Ramesses and a Hittite princess under a canopy, petals falling. Then the sky turns dark red, storm clouds roll in, and a cracked bronze shield drops into frame. The Guide is not in this shot.
- **On-screen text:** SEALING THE PEACE / 1200 BC: BRONZE AGE COLLAPSE
- **Camera / animation:** Petals, then colour shift to dark red
- **SFX / music:** wedding harp, thunder
- **Length:** 20 spoken words · 7.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A royal wedding: Ramesses and a Hittite princess under a canopy, petals falling. Then the sky turns dark red, storm clouds roll in, and a cracked bronze shield drops into frame. Text in frame: SEALING THE PEACE / 1200 BC: BRONZE AGE COLLAPSE.`
- **AI motion prompt:** `Petals, then colour shift to dark red. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 122 · 16:20.5–16:27.7 (7.2 s) · A · Satellite map

**VO:** "The Hittite empire fell, and cities across the eastern Mediterranean were destroyed. Under Ramesses III,"

- **Visual:** Satellite map of the eastern Mediterranean: fire icons light up on cities one after another; the purple Hittite area fades away. Ramesses III appears bottom left with a shield. The Guide is not in this shot.
- **On-screen text:** THE HITTITES FALL / RAMESSES III
- **Camera / animation:** Fires cascade
- **SFX / music:** fire crackle
- **Length:** 16 spoken words · 7.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map of the eastern Mediterranean: fire icons light up on cities one after another; the purple Hittite area fades away. Ramesses III appears bottom left with a shield. Text in frame: THE HITTITES FALL / RAMESSES III.`
- **AI motion prompt:** `Fires cascade. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 123 · 16:27.7–16:37.1 (9.4 s) · A · Satellite map

**VO:** "Egypt beat back invaders it called the Sea Peoples, but war, failing trade and poor harvests drained it. Egypt soon lost its lands in Canaan and Syria."

- **Visual:** Sea Peoples' ships (bird-head prows) sail at the delta and Ramesses III's fleet pushes them back. Then Egypt's red empire drains back from CANAAN and SYRIA; icons of a broken sword, an idle trade ship and a dry wheat sheaf hover. The Guide is not in this shot.
- **On-screen text:** SEA PEOPLES / WAR · FAILING TRADE · POOR HARVESTS
- **Camera / animation:** Naval clash; red drains
- **SFX / music:** waves, battle, drain
- **Length:** 27 spoken words · 9.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Sea Peoples' ships (bird-head prows) sail at the delta and Ramesses III's fleet pushes them back. Then Egypt's red empire drains back from CANAAN and SYRIA; icons of a broken sword, an idle trade ship and a dry wheat sheaf hover. Text in frame: SEA PEOPLES / WAR · FAILING TRADE · POOR HARVESTS.`
- **AI motion prompt:** `Naval clash; red drains. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

**Batch 10 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 11: Strikes, outsiders and Assyria (Scenes 124–136, 16:37.1–18:19.5)

#### Scene 124 · 16:37.1–16:46.8 (9.7 s) · C · Illustrated world

**VO:** "The state began to fail at home. Around 1157 BC, royal tomb builders went unpaid and staged the first recorded strike in history."

- **Visual:** Royal tomb builders sit on the ground with tools down and arms crossed, holding empty bowls; a sign reads NO GRAIN, NO WORK. The Guide sits with them, arms crossed too.
- **On-screen text:** 1157 BC / THE FIRST RECORDED STRIKE
- **Camera / animation:** Push in
- **SFX / music:** crowd chant
- **Length:** 26 spoken words · 9.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Royal tomb builders sit on the ground with tools down and arms crossed, holding empty bowls; a sign reads NO GRAIN, NO WORK. The Guide sits with them, arms crossed too. Include the Guide exactly as in the character reference. Text in frame: 1157 BC / THE FIRST RECORDED STRIKE.`
- **AI motion prompt:** `Push in. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 125 · 16:46.8–16:53.5 (6.7 s) · C · Illustrated world

**VO:** "Within decades, officials were putting gangs on trial for robbing the royal tombs in the Valley of the Kings."

- **Visual:** A courtroom: officials on a bench try a gang of tomb robbers while a scribe records it. Tomb-robber icons pop over the Valley of the Kings in the background. The Guide is not in this shot.
- **On-screen text:** TOMB ROBBERS ON TRIAL
- **Camera / animation:** Wide shot
- **SFX / music:** gavel knock, murmurs
- **Length:** 19 spoken words · 6.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A courtroom: officials on a bench try a gang of tomb robbers while a scribe records it. Tomb-robber icons pop over the Valley of the Kings in the background. Text in frame: TOMB ROBBERS ON TRIAL.`
- **AI motion prompt:** `Wide shot. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 126 · 16:53.5–17:00.2 (6.7 s) · C · Illustrated world

**VO:** "To save what was left, priests gathered the mummies of great pharaohs and hid them together in secret caches."

- **Visual:** Night, torchlight: priests carry wrapped royal mummies in a line into a hidden cave in the cliffs and seal it with stones. The Guide is not in this shot.
- **On-screen text:** SECRET CACHES
- **Camera / animation:** Torch flicker; slow follow
- **SFX / music:** echoing footsteps
- **Length:** 19 spoken words · 6.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Night, torchlight: priests carry wrapped royal mummies in a line into a hidden cave in the cliffs and seal it with stones. Text in frame: SECRET CACHES.`
- **AI motion prompt:** `Torch flicker; slow follow. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 127 · 17:00.2–17:09.1 (8.9 s) · C · Illustrated world

**VO:** "That's why we can still see the faces of kings like Ramesses II today. … By about 1070 BC, the New Kingdom was over."

- **Visual:** Present day: the Guide in a museum, face to face with the mummy of Ramesses II behind glass. Then a yellow title card slams in over a cracking map.
- **On-screen text:** RAMESSES II, TODAY / 1070 BC: THE NEW KINGDOM ENDS
- **Camera / animation:** Match cut; title slam
- **SFX / music:** museum hum, crack
- **Length:** 26 spoken words · 8.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Present day: the Guide in a museum, face to face with the mummy of Ramesses II behind glass. Then a yellow title card slams in over a cracking map. Include the Guide exactly as in the character reference. Text in frame: RAMESSES II, TODAY / 1070 BC: THE NEW KINGDOM ENDS.`
- **AI motion prompt:** `Match cut; title slam. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 128 · 17:09.1–17:17.0 (7.9 s) · A · Satellite map

**VO:** "The high priests of Amun ruled the south from Thebes, while separate kings ruled the delta. … Power slipped to outsiders."

- **Visual:** Map splits: THEBES (south) gets a priest icon with Amun's plumes; the DELTA (north) gets a separate king icon. Then the throne icon starts sliding toward the edge of the frame. The Guide is not in this shot.
- **On-screen text:** PRIESTS IN THEBES · KINGS IN THE DELTA / OUTSIDERS
- **Camera / animation:** Map divides; icon slides
- **SFX / music:** low drone
- **Length:** 20 spoken words · 7.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map splits: THEBES (south) gets a priest icon with Amun's plumes; the DELTA (north) gets a separate king icon. Then the throne icon starts sliding toward the edge of the frame. Text in frame: PRIESTS IN THEBES · KINGS IN THE DELTA / OUTSIDERS.`
- **AI motion prompt:** `Map divides; icon slides. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 129 · 17:17.0–17:25.2 (8.2 s) · A · Satellite map

**VO:** "Families of Libyan descent, settled in Egypt for generations, took the throne. Then kings from Kush, in today's Sudan, marched north."

- **Visual:** The delta throne is taken by a king of Libyan descent (feather in his hair). Then a long arrow marches north from KUSH (today's Sudan) along the Nile. The Guide is not in this shot.
- **On-screen text:** LIBYAN KINGS / KUSH MARCHES NORTH
- **Camera / animation:** Icon swap; arrow draws north
- **SFX / music:** drums, marching
- **Length:** 21 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: The delta throne is taken by a king of Libyan descent (feather in his hair). Then a long arrow marches north from KUSH (today's Sudan) along the Nile. Text in frame: LIBYAN KINGS / KUSH MARCHES NORTH.`
- **AI motion prompt:** `Icon swap; arrow draws north. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 130 · 17:25.2–17:34.6 (9.4 s) · C · Illustrated world

**VO:** "Around 727 BC, King Piye conquered Egypt, and his family ruled as pharaohs for more than half a century,"

- **Visual:** King Piye (Kushite, cap crown with two cobras) enters Memphis on a chariot while crowds bow. His family members appear on the throne one after another; a bar fills: 50+ YEARS. The Guide is not in this shot.
- **On-screen text:** 727 BC / KING PIYE / 50+ YEARS
- **Camera / animation:** Push in on Piye
- **SFX / music:** fanfare, crowd
- **Length:** 24 spoken words · 9.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: King Piye (Kushite, cap crown with two cobras) enters Memphis on a chariot while crowds bow. His family members appear on the throne one after another; a bar fills: 50+ YEARS. Text in frame: 727 BC / KING PIYE / 50+ YEARS.`
- **AI motion prompt:** `Push in on Piye. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 131 · 17:34.6–17:41.8 (7.2 s) · C · Illustrated world

**VO:** "restoring old temples and traditions. … Next came the Assyrian empire. In 671 BC,"

- **Visual:** Kushite kings repair an old temple (scaffolding, fresh paint). Then a huge Assyrian army (from Iraq) rises over the horizon. The Guide gulps.
- **On-screen text:** RESTORING TRADITIONS / ASSYRIA
- **Camera / animation:** Scaffold; army rises
- **SFX / music:** hammer taps, war cry
- **Length:** 18 spoken words · 7.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Kushite kings repair an old temple (scaffolding, fresh paint). Then a huge Assyrian army (from Iraq) rises over the horizon. The Guide gulps. Include the Guide exactly as in the character reference. Text in frame: RESTORING TRADITIONS / ASSYRIA.`
- **AI motion prompt:** `Scaffold; army rises. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 132 · 17:41.8–17:49.7 (7.9 s) · A · Satellite map

**VO:** "its army took Memphis, and in 663 BC it sacked Thebes and drove the Kushite kings back south for good."

- **Visual:** Assyrian arrow strikes MEMPHIS (fire icon), then THEBES (fire icon); the Kushite icon is pushed back south for good. The Guide is not in this shot.
- **On-screen text:** 671 BC: MEMPHIS / 663 BC: THEBES SACKED
- **Camera / animation:** Two strikes; push back
- **SFX / music:** crash, crash
- **Length:** 25 spoken words · 7.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Assyrian arrow strikes MEMPHIS (fire icon), then THEBES (fire icon); the Kushite icon is pushed back south for good. Text in frame: 671 BC: MEMPHIS / 663 BC: THEBES SACKED.`
- **AI motion prompt:** `Two strikes; push back. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 133 · 17:49.7–17:56.4 (6.7 s) · A · Satellite map

**VO:** "A delta prince, Psamtik I, used the Assyrians' retreat and hired Greek soldiers to reunite Egypt."

- **Visual:** Psamtik I, a young delta prince, hires Greek soldiers in bronze crested helmets; the map turns one colour again. The Guide is not in this shot.
- **On-screen text:** PSAMTIK I REUNITES EGYPT
- **Camera / animation:** Recolour
- **SFX / music:** unifying chime
- **Length:** 17 spoken words · 6.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Psamtik I, a young delta prince, hires Greek soldiers in bronze crested helmets; the map turns one colour again. Text in frame: PSAMTIK I REUNITES EGYPT.`
- **AI motion prompt:** `Recolour. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 134 · 17:56.4–18:02.9 (6.5 s) · C · Illustrated world

**VO:** "His dynasty was the last great native revival, and it lasted about 140 years."

- **Visual:** Native revival: freshly painted temples, old-style statues; a timeline bar fills to 140 YEARS. The Guide paints a column.
- **On-screen text:** LAST GREAT NATIVE REVIVAL / 140 YEARS
- **Camera / animation:** Pan
- **SFX / music:** warm strings
- **Length:** 17 spoken words · 6.5 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Native revival: freshly painted temples, old-style statues; a timeline bar fills to 140 YEARS. The Guide paints a column. Include the Guide exactly as in the character reference. Text in frame: LAST GREAT NATIVE REVIVAL / 140 YEARS.`
- **AI motion prompt:** `Pan. Gentle cartoon motion, elements pop in with a small bounce, 6 seconds.`

#### Scene 135 · 18:02.9–18:09.1 (6.2 s) · C · Illustrated world

**VO:** "It opened Egypt to Greek traders, and Psamtik's son Necho II tried to win back Syria."

- **Visual:** Greek merchant ships with eye-painted prows dock in the delta; the Guide haggles with a Greek trader. Then Necho II marches his army toward Syria.
- **On-screen text:** GREEK TRADERS / NECHO II
- **Camera / animation:** Pan; march
- **SFX / music:** market chatter, march
- **Length:** 17 spoken words · 6.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Greek merchant ships with eye-painted prows dock in the delta; the Guide haggles with a Greek trader. Then Necho II marches his army toward Syria. Include the Guide exactly as in the character reference. Text in frame: GREEK TRADERS / NECHO II.`
- **AI motion prompt:** `Pan; march. Gentle cartoon motion, elements pop in with a small bounce, 6 seconds.`

#### Scene 136 · 18:09.1–18:19.5 (10.4 s) · A · Satellite map

**VO:** "But in 605 BC, the Babylonian prince Nebuchadnezzar crushed the Egyptian army at Carchemish. Egypt's days as an empire were over."

- **Visual:** A Babylonian arrow (young prince Nebuchadnezzar) slams into the Egyptian one at CARCHEMISH and shatters it. Egypt's empire flag slides down its pole. The Guide is not in this shot.
- **On-screen text:** 605 BC / CARCHEMISH / EMPIRE OVER
- **Camera / animation:** Collision; flag lowers
- **SFX / music:** crash, sad trumpet
- **Length:** 25 spoken words · 10.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: A Babylonian arrow (young prince Nebuchadnezzar) slams into the Egyptian one at CARCHEMISH and shatters it. Egypt's empire flag slides down its pole. Text in frame: 605 BC / CARCHEMISH / EMPIRE OVER.`
- **AI motion prompt:** `Collision; flag lowers. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

**Batch 11 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 12: Persia and Alexander (Scenes 137–146, 18:19.5–19:37.8)

#### Scene 137 · 18:19.5–18:27.4 (7.9 s) · C · Illustrated world

**VO:** "In 525 BC, the Persian king Cambyses defeated the last king of that dynasty at Pelusium,"

- **Visual:** At a desert border fort, PELUSIUM, the Persian king Cambyses (tall hat, long curled beard) arrives with a huge army and defeats the last king of the dynasty. The Guide is not in this shot.
- **On-screen text:** 525 BC / CAMBYSES AT PELUSIUM
- **Camera / animation:** Wide army shot
- **SFX / music:** war horns
- **Length:** 21 spoken words · 7.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: At a desert border fort, PELUSIUM, the Persian king Cambyses (tall hat, long curled beard) arrives with a huge army and defeats the last king of the dynasty. Text in frame: 525 BC / CAMBYSES AT PELUSIUM.`
- **AI motion prompt:** `Wide army shot. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 138 · 18:27.4–18:34.8 (7.4 s) · A · Satellite map

**VO:** "on Egypt's eastern border. Egypt became a province of the largest empire the world had yet seen, ruled from Iran."

- **Visual:** Satellite map: a giant Persian overlay spreads from IRAN across the Middle East and swallows Egypt. A capital pin glows in Iran. The Guide steps back from the size of it.
- **On-screen text:** A PERSIAN PROVINCE / RULED FROM IRAN
- **Camera / animation:** Overlay spreads westward
- **SFX / music:** deep rumble
- **Length:** 20 spoken words · 7.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map: a giant Persian overlay spreads from IRAN across the Middle East and swallows Egypt. A capital pin glows in Iran. The Guide steps back from the size of it. Include the Guide exactly as in the character reference. Text in frame: A PERSIAN PROVINCE / RULED FROM IRAN.`
- **AI motion prompt:** `Overlay spreads westward. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 139 · 18:34.8–18:41.3 (6.5 s) · C · Illustrated world

**VO:** "Some Persian kings, like Darius I, respected Egyptian temples and ruled through local officials."

- **Visual:** Darius I bows respectfully at an Egyptian temple, with Egyptian officials at his side running things. The Guide is not in this shot.
- **On-screen text:** DARIUS I / RESPECTED THE TEMPLES
- **Camera / animation:** Calm push-in
- **SFX / music:** gentle music
- **Length:** 15 spoken words · 6.5 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Darius I bows respectfully at an Egyptian temple, with Egyptian officials at his side running things. Text in frame: DARIUS I / RESPECTED THE TEMPLES.`
- **AI motion prompt:** `Calm push-in. Gentle cartoon motion, elements pop in with a small bounce, 6 seconds.`

#### Scene 140 · 18:41.3–18:49.0 (7.7 s) · C · Illustrated world

**VO:** "Others were harsher, and Egyptians rebelled again and again. In 404 BC, they finally broke free."

- **Visual:** A harsher Persian king with a whip; Egyptian crowds rise up with fists raised, again and again (three quick revolt beats). Then 404 BC: Egyptians break a chain and raise flags. The Guide is not in this shot.
- **On-screen text:** REVOLT AFTER REVOLT / 404 BC: FREE
- **Camera / animation:** Three revolt beats; chain snaps
- **SFX / music:** shouts, cheers
- **Length:** 20 spoken words · 7.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A harsher Persian king with a whip; Egyptian crowds rise up with fists raised, again and again (three quick revolt beats). Then 404 BC: Egyptians break a chain and raise flags. Text in frame: REVOLT AFTER REVOLT / 404 BC: FREE.`
- **AI motion prompt:** `Three revolt beats; chain snaps. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 141 · 18:49.0–18:58.2 (9.2 s) · C · Illustrated world

**VO:** "Independence lasted about 60 years. In 343 BC, Persia invaded again and won. The pharaoh who lost that war,"

- **Visual:** A timer card counts ~60 YEARS. Then 343 BC: the Persian army returns over the dunes, and the last native pharaoh stands alone facing it. The Guide is not in this shot.
- **On-screen text:** ~60 YEARS / 343 BC: PERSIA RETURNS
- **Camera / animation:** Army rises over the dunes
- **SFX / music:** war drums
- **Length:** 24 spoken words · 9.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A timer card counts ~60 YEARS. Then 343 BC: the Persian army returns over the dunes, and the last native pharaoh stands alone facing it. Text in frame: ~60 YEARS / 343 BC: PERSIA RETURNS.`
- **AI motion prompt:** `Army rises over the dunes. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 142 · 18:58.2–19:07.1 (8.9 s) · C · Illustrated world

**VO:** "Nectanebo II, is usually counted as the last native Egyptian to rule Egypt for about 2,300 years."

- **Visual:** Sunset: Nectanebo II walks away into the desert, fading. A yellow counter rolls up to 2,300 YEARS. The Guide is not in this shot.
- **On-screen text:** NECTANEBO II / LAST NATIVE PHARAOH / 2,300 YEARS
- **Camera / animation:** Slow fade; counter rolls
- **SFX / music:** single sad note, drum hit
- **Length:** 21 spoken words · 8.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Sunset: Nectanebo II walks away into the desert, fading. A yellow counter rolls up to 2,300 YEARS. Text in frame: NECTANEBO II / LAST NATIVE PHARAOH / 2,300 YEARS.`
- **AI motion prompt:** `Slow fade; counter rolls. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 143 · 19:07.1–19:15.5 (8.4 s) · C · Illustrated world

**VO:** "That's the number from the start of this video. … In 332 BC, Alexander the Great took Egypt from the Persians,"

- **Visual:** A quick flashback to the opening card (pyramids + 2,300 YEARS); the Guide points at the number and nods. Then Alexander the Great (young, curly hair, plumed helmet) rides into Egypt as Persians flee.
- **On-screen text:** THE NUMBER FROM THE START / 332 BC: ALEXANDER THE GREAT
- **Camera / animation:** Flashback flash; cut to the arrival
- **SFX / music:** whoosh, horns
- **Length:** 25 spoken words · 8.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A quick flashback to the opening card (pyramids + 2,300 YEARS); the Guide points at the number and nods. Then Alexander the Great (young, curly hair, plumed helmet) rides into Egypt as Persians flee. Include the Guide exactly as in the character reference. Text in frame: THE NUMBER FROM THE START / 332 BC: ALEXANDER THE GREAT.`
- **AI motion prompt:** `Flashback flash; cut to the arrival. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 144 · 19:15.5–19:23.2 (7.7 s) · C · Illustrated world

**VO:** "and many Egyptians welcomed him. He travelled to the oracle of Amun at Siwa, in the western desert,"

- **Visual:** Egyptians cheer Alexander in the streets. Then a desert oasis at SIWA: palm trees and a small temple of Amun. The Guide is not in this shot.
- **On-screen text:** WELCOMED / SIWA
- **Camera / animation:** Cut to the oasis
- **SFX / music:** cheering, desert wind
- **Length:** 18 spoken words · 7.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Egyptians cheer Alexander in the streets. Then a desert oasis at SIWA: palm trees and a small temple of Amun. Text in frame: WELCOMED / SIWA.`
- **AI motion prompt:** `Cut to the oasis. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 145 · 19:23.2–19:30.9 (7.7 s) · C · Illustrated world

**VO:** "and was hailed as the god's son. Egypt accepted him as pharaoh. He founded a new city on the coast: Alexandria."

- **Visual:** Inside the temple the oracle glows: SON OF AMUN. Priests place the double crown on Alexander. Then a pin ALEXANDRIA drops on the coastline with a city sketch. The Guide is not in this shot.
- **On-screen text:** "SON OF AMUN" / PHARAOH / ALEXANDRIA
- **Camera / animation:** Crown placement; pin drop
- **SFX / music:** choir, ping
- **Length:** 21 spoken words · 7.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Inside the temple the oracle glows: SON OF AMUN. Priests place the double crown on Alexander. Then a pin ALEXANDRIA drops on the coastline with a city sketch. Text in frame: "SON OF AMUN" / PHARAOH / ALEXANDRIA.`
- **AI motion prompt:** `Crown placement; pin drop. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 146 · 19:30.9–19:37.8 (6.9 s) · C · Illustrated world

**VO:** "He left after a few months and never returned alive, but his body was later brought back and buried there."

- **Visual:** Alexander's ship sails away over the horizon. Later, a funeral cart with a golden coffin rolls back into Alexandria. The Guide is not in this shot.
- **On-screen text:** NEVER RETURNED ALIVE
- **Camera / animation:** Ship leaves; cart returns
- **SFX / music:** waves, sombre drum
- **Length:** 20 spoken words · 6.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Alexander's ship sails away over the horizon. Later, a funeral cart with a golden coffin rolls back into Alexandria. Text in frame: NEVER RETURNED ALIVE.`
- **AI motion prompt:** `Ship leaves; cart returns. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

**Batch 12 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 13: The Ptolemies and Cleopatra (Scenes 147–163, 19:37.8–21:57.6)

#### Scene 147 · 19:37.8–19:44.5 (6.7 s) · C · Illustrated world

**VO:** "After Alexander's death in 323 BC, his general Ptolemy took Egypt,"

- **Visual:** General Ptolemy lifts the crown from Alexander's empty throne and puts it on. The Guide is not in this shot.
- **On-screen text:** 323 BC / PTOLEMY TAKES EGYPT
- **Camera / animation:** Push in
- **SFX / music:** fanfare
- **Length:** 16 spoken words · 6.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: General Ptolemy lifts the crown from Alexander's empty throne and puts it on. Text in frame: 323 BC / PTOLEMY TAKES EGYPT.`
- **AI motion prompt:** `Push in. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 148 · 19:44.5–19:52.4 (7.9 s) · B · Grey studio

**VO:** "and Ptolemy's family ruled it for nearly 300 years. The system was simple: Greek-speaking officials at the top,"

- **Visual:** Grey studio. A family tree of Ptolemies branches across the screen with a ~300 YEARS bar. Then a society pyramid starts building: Greek-speaking officials at the top. The Guide is not in this shot.
- **On-screen text:** ~300 YEARS / GREEK OFFICIALS AT THE TOP
- **Camera / animation:** Tree grows; pyramid builds
- **SFX / music:** pops
- **Length:** 20 spoken words · 7.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio. A family tree of Ptolemies branches across the screen with a ~300 YEARS bar. Then a society pyramid starts building: Greek-speaking officials at the top. Text in frame: ~300 YEARS / GREEK OFFICIALS AT THE TOP.`
- **AI motion prompt:** `Tree grows; pyramid builds. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 149 · 19:52.4–20:01.8 (9.4 s) · B · Grey studio

**VO:** "Egyptian farmers at the bottom, and the Nile's harvest taxed to fund the court. … To Egyptians, the Ptolemies presented themselves as pharaohs."

- **Visual:** Egyptian farmers fill the bottom of the pyramid; Nile grain flows up as tax arrows to the court. Then a Ptolemy king puts on pharaoh's clothes. The Guide holds a tax scroll.
- **On-screen text:** EGYPTIAN FARMERS AT THE BOTTOM / PHARAOHS TO EGYPTIANS
- **Camera / animation:** Arrows flow upward; costume pop
- **SFX / music:** coins, grain, poof
- **Length:** 22 spoken words · 9.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Egyptian farmers fill the bottom of the pyramid; Nile grain flows up as tax arrows to the court. Then a Ptolemy king puts on pharaoh's clothes. The Guide holds a tax scroll. Include the Guide exactly as in the character reference. Text in frame: EGYPTIAN FARMERS AT THE BOTTOM / PHARAOHS TO EGYPTIANS.`
- **AI motion prompt:** `Arrows flow upward; costume pop. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 150 · 20:01.8–20:10.0 (8.2 s) · C · Illustrated world

**VO:** "They built huge temples in the traditional style, like those at Edfu and Dendera, with their Greek names carved in hieroglyphs."

- **Visual:** The huge traditional temples of Edfu and Dendera rise from the sand. Close-up: a Greek name in a hieroglyph cartouche (PTOLEMAIOS). The Guide is not in this shot.
- **On-screen text:** EDFU · DENDERA / GREEK NAMES IN HIEROGLYPHS
- **Camera / animation:** Pan along the pylons; zoom on the cartouche
- **SFX / music:** chant, stone rumble
- **Length:** 21 spoken words · 8.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: The huge traditional temples of Edfu and Dendera rise from the sand. Close-up: a Greek name in a hieroglyph cartouche (PTOLEMAIOS). Text in frame: EDFU · DENDERA / GREEK NAMES IN HIEROGLYPHS.`
- **AI motion prompt:** `Pan along the pylons; zoom on the cartouche. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 151 · 20:10.0–20:19.2 (9.2 s) · C · Illustrated world

**VO:** "Foreign rulers kept becoming, at least on temple walls, Egyptian kings. … Alexandria became the greatest city of the Greek world, with its lighthouse,"

- **Visual:** The "pattern" loop arrow from scene 66 spins back in. Then Alexandria's harbour with the Lighthouse, fire on top. The Guide is not in this shot.
- **On-screen text:** THE PATTERN AGAIN / ALEXANDRIA
- **Camera / animation:** Loop spins; cut
- **SFX / music:** ding, waves
- **Length:** 23 spoken words · 9.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: The "pattern" loop arrow from scene 66 spins back in. Then Alexandria's harbour with the Lighthouse, fire on top. Text in frame: THE PATTERN AGAIN / ALEXANDRIA.`
- **AI motion prompt:** `Loop spins; cut. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 152 · 20:19.2–20:27.6 (8.4 s) · C · Illustrated world

**VO:** "one of the Seven Wonders, and its Great Library. Scholars there worked out the size of the Earth and wrote the geometry still taught today."

- **Visual:** A star badge: ONE OF THE 7 WONDERS. Inside the Great Library: scroll shelves. A scholar measures a stick's shadow; a globe with a measuring tape appears; triangles and circles draw themselves. The Guide is not in this shot.
- **On-screen text:** GREAT LIBRARY / SIZE OF THE EARTH / GEOMETRY
- **Camera / animation:** Pan; draw-on
- **SFX / music:** page rustles, chalk
- **Length:** 25 spoken words · 8.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A star badge: ONE OF THE 7 WONDERS. Inside the Great Library: scroll shelves. A scholar measures a stick's shadow; a globe with a measuring tape appears; triangles and circles draw themselves. Text in frame: GREAT LIBRARY / SIZE OF THE EARTH / GEOMETRY.`
- **AI motion prompt:** `Pan; draw-on. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 153 · 20:27.6–20:34.8 (7.2 s) · B · Grey studio

**VO:** "But the royal court itself spoke Greek. … The Ptolemies kept power in the family, often by brothers marrying sisters."

- **Visual:** A courtier speaks a Greek-letter speech bubble (Α Β Γ). Then a royal family tree where brother and sister icons link with heart lines; the Guide grimaces.
- **On-screen text:** THE COURT SPOKE GREEK / BROTHERS MARRIED SISTERS
- **Camera / animation:** Bubble; tree draws
- **SFX / music:** murmurs
- **Length:** 19 spoken words · 7.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: A courtier speaks a Greek-letter speech bubble (Α Β Γ). Then a royal family tree where brother and sister icons link with heart lines; the Guide grimaces. Include the Guide exactly as in the character reference. Text in frame: THE COURT SPOKE GREEK / BROTHERS MARRIED SISTERS.`
- **AI motion prompt:** `Bubble; tree draws. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 154 · 20:34.8–20:43.5 (8.7 s) · A · Satellite map

**VO:** "Heavy taxes bred resentment, and for about 20 years, rebels held much of southern Egypt. … In 196 BC,"

- **Visual:** A tax collector loads heavy grain sacks while farmers glare. A small map shows southern Egypt turning rebel orange with a ~20 YEARS counter. The Guide is not in this shot.
- **On-screen text:** HEAVY TAXES / REBELS HOLD THE SOUTH
- **Camera / animation:** Overlay spreads
- **SFX / music:** grumbling crowd
- **Length:** 23 spoken words · 8.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: A tax collector loads heavy grain sacks while farmers glare. A small map shows southern Egypt turning rebel orange with a ~20 YEARS counter. Text in frame: HEAVY TAXES / REBELS HOLD THE SOUTH.`
- **AI motion prompt:** `Overlay spreads. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 155 · 20:43.5–20:52.2 (8.7 s) · D · Artefact / relief close-up

**VO:** "during that revolt, priests at Memphis issued a decree honouring the young king Ptolemy V. It was carved in three scripts: hieroglyphs,"

- **Visual:** Inside a temple at Memphis, priests carve a decree into a dark grey stone honouring young Ptolemy V (a boy on a small throne). The top band fills with hieroglyphs. The Guide is not in this shot.
- **On-screen text:** 196 BC / THE MEMPHIS DECREE / PTOLEMY V
- **Camera / animation:** Chisel line by line
- **SFX / music:** chisel taps
- **Length:** 23 spoken words · 8.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: Inside a temple at Memphis, priests carve a decree into a dark grey stone honouring young Ptolemy V (a boy on a small throne). The top band fills with hieroglyphs. Text in frame: 196 BC / THE MEMPHIS DECREE / PTOLEMY V.`
- **AI motion prompt:** `Chisel line by line. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 156 · 20:52.2–21:01.4 (9.2 s) · D · Artefact / relief close-up

**VO:** "the everyday Egyptian script called Demotic, and Greek. Remember this stone. … The last ruler of the dynasty was Cleopatra VII."

- **Visual:** The stone shows three bands, labelled HIEROGLYPHS, DEMOTIC, GREEK. The Guide taps it and winks. Hard cut: Cleopatra VII on a throne in Alexandria with the cobra crown.
- **On-screen text:** REMEMBER THIS STONE / CLEOPATRA VII
- **Camera / animation:** Labels pop; hard cut
- **SFX / music:** three pops, royal harp
- **Length:** 21 spoken words · 9.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: The stone shows three bands, labelled HIEROGLYPHS, DEMOTIC, GREEK. The Guide taps it and winks. Hard cut: Cleopatra VII on a throne in Alexandria with the cobra crown. Include the Guide exactly as in the character reference. Text in frame: REMEMBER THIS STONE / CLEOPATRA VII.`
- **AI motion prompt:** `Labels pop; hard cut. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 157 · 21:01.4–21:07.6 (6.2 s) · C · Illustrated world

**VO:** "According to the ancient writer Plutarch, she was the first of her family to learn Egyptian."

- **Visual:** Cleopatra studies hieroglyphs with an Egyptian scribe; a book card PLUTARCH pops in. The Guide is not in this shot.
- **On-screen text:** FIRST OF HER FAMILY TO LEARN EGYPTIAN
- **Camera / animation:** Card pop
- **SFX / music:** quill scratch
- **Length:** 16 spoken words · 6.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Cleopatra studies hieroglyphs with an Egyptian scribe; a book card PLUTARCH pops in. Text in frame: FIRST OF HER FAMILY TO LEARN EGYPTIAN.`
- **AI motion prompt:** `Card pop. Gentle cartoon motion, elements pop in with a small bounce, 6 seconds.`

#### Scene 158 · 21:07.6–21:15.5 (7.9 s) · A · Satellite map

**VO:** "She needed powerful allies to keep Egypt free of Rome, which was swallowing the Mediterranean. … In 48 BC,"

- **Visual:** Satellite map: Roman red spreads around the Mediterranean like a rising tide, closing on Egypt. Cleopatra looks at it from bottom left. The Guide is not in this shot.
- **On-screen text:** KEEP EGYPT FREE OF ROME
- **Camera / animation:** Overlay spreads
- **SFX / music:** ominous drum
- **Length:** 20 spoken words · 7.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map: Roman red spreads around the Mediterranean like a rising tide, closing on Egypt. Cleopatra looks at it from bottom left. Text in frame: KEEP EGYPT FREE OF ROME.`
- **AI motion prompt:** `Overlay spreads. Gentle cartoon motion, elements pop in with a small bounce, 8 seconds.`

#### Scene 159 · 21:15.5–21:24.4 (8.9 s) · C · Illustrated world

**VO:** "she was fighting her own brother for the throne when Julius Caesar arrived in Alexandria. She won his support, he defeated her rivals,"

- **Visual:** Cleopatra and her younger brother tug a crown back and forth. Julius Caesar (laurel wreath, red cloak) sails into Alexandria; her brother's army falls back. The Guide is not in this shot.
- **On-screen text:** 48 BC / JULIUS CAESAR
- **Camera / animation:** Tug-of-war; ship arrives
- **SFX / music:** tug creak, horns
- **Length:** 23 spoken words · 8.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Cleopatra and her younger brother tug a crown back and forth. Julius Caesar (laurel wreath, red cloak) sails into Alexandria; her brother's army falls back. Text in frame: 48 BC / JULIUS CAESAR.`
- **AI motion prompt:** `Tug-of-war; ship arrives. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 160 · 21:24.4–21:33.1 (8.7 s) · C · Illustrated world

**VO:** "and she had a son with him, Caesarion. … After Caesar's murder, she allied with Mark Antony, who controlled Rome's eastern provinces."

- **Visual:** Cleopatra holds baby Caesarion. Then dagger shadows in the Roman Senate (no gore). Then she shakes hands with Mark Antony, with a map of the eastern provinces behind him. The Guide is not in this shot.
- **On-screen text:** CAESARION / MARK ANTONY
- **Camera / animation:** Cut; shadows; handshake
- **SFX / music:** baby giggle, gasp
- **Length:** 21 spoken words · 8.7 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Cleopatra holds baby Caesarion. Then dagger shadows in the Roman Senate (no gore). Then she shakes hands with Mark Antony, with a map of the eastern provinces behind him. Text in frame: CAESARION / MARK ANTONY.`
- **AI motion prompt:** `Cut; shadows; handshake. Gentle cartoon motion, elements pop in with a small bounce, 9 seconds.`

#### Scene 161 · 21:33.1–21:43.0 (9.9 s) · A · Satellite map

**VO:** "That made them enemies of Caesar's heir, Octavian. When Antony and Cleopatra lost the naval battle of Actium to Octavian in 31 BC,"

- **Visual:** Split screen: Octavian (young, toga) frowns across the sea. Then the map of western Greece: two fleets meet at ACTIUM. The Guide is not in this shot.
- **On-screen text:** OCTAVIAN / 31 BC: ACTIUM
- **Camera / animation:** Split wave line; fleets clash
- **SFX / music:** tension strings, waves
- **Length:** 25 spoken words · 9.9 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Split screen: Octavian (young, toga) frowns across the sea. Then the map of western Greece: two fleets meet at ACTIUM. Text in frame: OCTAVIAN / 31 BC: ACTIUM.`
- **AI motion prompt:** `Split wave line; fleets clash. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 162 · 21:43.0–21:50.4 (7.4 s) · C · Illustrated world

**VO:** "it was over. Antony killed himself, and in 30 BC Cleopatra died too, by tradition from a snake bite."

- **Visual:** Antony fades into darkness. Then Cleopatra on her throne at dusk with a small cobra near her; she fades gently into gold dust. The Guide is not in this shot.
- **On-screen text:** 30 BC
- **Camera / animation:** Slow fade
- **SFX / music:** sombre strings
- **Length:** 20 spoken words · 7.4 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Antony fades into darkness. Then Cleopatra on her throne at dusk with a small cobra near her; she fades gently into gold dust. Text in frame: 30 BC.`
- **AI motion prompt:** `Slow fade. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

#### Scene 163 · 21:50.4–21:57.6 (7.2 s) · C · Illustrated world

**VO:** "Egypt became part of the Roman Empire. … Octavian, now Emperor Augustus, kept Egypt as his personal"

- **Visual:** A Roman eagle banner rises over Egypt. Octavian, now Augustus, steps forward holding a small model of Egypt in his hands like a possession. Hold for the cliffhanger. The Guide is not in this shot.
- **On-screen text:** EGYPT BECOMES ROMAN / AUGUSTUS
- **Camera / animation:** Banner rises; hold
- **SFX / music:** eagle cry
- **Length:** 16 spoken words · 7.2 s at the locked voice speed
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A Roman eagle banner rises over Egypt. Octavian, now Augustus, steps forward holding a small model of Egypt in his hands like a possession. Hold for the cliffhanger. Text in frame: EGYPT BECOMES ROMAN / AUGUSTUS.`
- **AI motion prompt:** `Banner rises; hold. Gentle cartoon motion, elements pop in with a small bounce, 7 seconds.`

**Batch 13 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.
