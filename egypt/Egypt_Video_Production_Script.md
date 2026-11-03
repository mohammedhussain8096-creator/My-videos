# Why Egypt Never Died: Scene-by-Scene Production Script

**Format:** 16:9, 1920×1080, 24 fps · **Scenes:** 132 × 10 s · **Runtime:** ≈ 22 min · **Narration pace:** locked at ≈ 155–160 words per minute (the same pace as the reference video)

> The script you sent stops mid-sentence (*"Octavian, now Emperor Augustus, kept Egypt as his personal…"*). Scene 132 ends on that line. Send the rest and the next batch continues from Scene 133 in the same format.

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
| Speed | **≈ 155–160 words per minute**, about 4 syllables per second. Never speed up to fit 10 seconds. Let the picture wait for the voice. |
| Pauses | Comma ≈ 0.25 s · full stop ≈ 0.5 s · `...` (new paragraph) ≈ 0.9 s · before a big reveal ≈ 0.7 s |
| Emphasis | Lean slightly on numbers, dates and the key word of each line (shown in the on-screen text column). Questions go up at the end. |
| Energy | Keep it level across all batches. The hook (Scenes 1–3) can be 5% brighter; collapse and death beats 5% softer, same speed. |
| TTS settings (e.g. ElevenLabs) | Same voice and model for every batch · Stability 50% · Similarity 75% · Style 10% · Speaker boost on · Speed 1.0. Generate one batch (10 scenes) per take, and paste the last sentence of the previous batch as "previous text" so the tone carries on. |
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
| 1 | 1–10 | 00:00–01:40 | The hook and the Nile |
| 2 | 11–20 | 01:40–03:20 | Unification, gods and the god-king |
| 3 | 21–30 | 03:20–05:00 | The first pyramids |
| 4 | 31–40 | 05:00–06:40 | Pyramid builders and the first collapse |
| 5 | 41–50 | 06:40–08:20 | The Middle Kingdom |
| 6 | 51–60 | 08:20–10:00 | The Hyksos and the fight back |
| 7 | 61–70 | 10:00–11:40 | The New Kingdom and Hatshepsut |
| 8 | 71–80 | 11:40–13:20 | Thutmose III and Akhenaten |
| 9 | 81–90 | 13:20–15:00 | Tutankhamun |
| 10 | 91–100 | 15:00–16:40 | Ramesses II |
| 11 | 101–110 | 16:40–18:20 | Bronze Age collapse and outsiders |
| 12 | 111–120 | 18:20–20:00 | Persia and Alexander |
| 13 | 121–132 | 20:00–22:00 | The Ptolemies and Cleopatra |

## 5. Scenes

How to read each scene: **VO** is the exact voice line. **Visual** is what we see and what the Guide does. **On-screen text** uses `/` to separate separate text pops (in order). **Pace** gives the estimated voice length at the locked speed. **AI prompt** is ready to paste into an image/video generator together with `character_reference.png`.

### Batch 1: The hook and the Nile (Scenes 1–10, 00:00–01:40)

#### Scene 001 · 00:00–00:10 · C · Illustrated world

**VO:** "You know the Giza pyramids. But almost nobody knows why Egypt never died after it lost its own kings for 2,300 years."

- **Visual:** Golden-hour Giza plateau: the three pyramids sit on a sunset gradient (orange to purple) with pink cartoon clouds. The Guide walks in from the left, stops, points his spear at the pyramids, then turns to camera with a raised eyebrow. A small crown icon above the plateau fades out.
- **On-screen text:** YOU KNOW THESE... / 2,300 YEARS
- **Camera / animation:** Slow push-in on the pyramids; on "2,300 years" the number slams in as yellow comic text
- **SFX / music:** soft desert wind, low drum hit on the number
- **Pace:** 25 spoken words · ≈ 8.9 s at locked speed. Light line: keep the same speed; leave a ~1.1s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Golden-hour Giza plateau: the three pyramids sit on a sunset gradient (orange to purple) with pink cartoon clouds. The Guide walks in from the left, stops, points his spear at the pyramids, then turns to camera with a raised eyebrow. A small crown icon above the plateau fades out. Include the Guide exactly as in the character reference. Text in frame: YOU KNOW THESE... / 2,300 YEARS.`
- **AI motion prompt:** `Slow push-in on the pyramids; on "2,300 years" the number slams in as yellow comic text. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 002 · 00:10–00:20 · B · Grey studio

**VO:** "Persians, Greeks, Romans, Arabs, Turks, the British. Every one of those empires ruled Egypt, and every one of them is gone. Egypt is still here. … The answer is in this picture."

- **Visual:** Grey studio. The Guide stands left. Six stick-figure rulers pop in a row on the right, each labelled: PERSIANS, GREEKS, ROMANS, ARABS, TURKS, BRITISH. A red X stamps over each one in turn. Then a small map of Egypt drops in the middle, untouched and glowing. The Guide holds up a framed picture card that is still face-down.
- **On-screen text:** PERSIANS · GREEKS · ROMANS · ARABS · TURKS · BRITISH / EGYPT IS STILL HERE
- **Camera / animation:** Characters pop in on each name (one per beat); red X stamps on "gone"; gentle zoom on Egypt
- **SFX / music:** pop sounds on each name, stamp sound on each X, soft chime on Egypt
- **Pace:** 31 spoken words · ≈ 11.4 s at locked speed. Dense line: do NOT speed up. Let it run to ~11.4s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio. The Guide stands left. Six stick-figure rulers pop in a row on the right, each labelled: PERSIANS, GREEKS, ROMANS, ARABS, TURKS, BRITISH. A red X stamps over each one in turn. Then a small map of Egypt drops in the middle, untouched and glowing. The Guide holds up a framed picture card that is still face-down. Include the Guide exactly as in the character reference. Text in frame: PERSIANS · GREEKS · ROMANS · ARABS · TURKS · BRITISH / EGYPT IS STILL HERE.`
- **AI motion prompt:** `Characters pop in on each name (one per beat); red X stamps on "gone"; gentle zoom on Egypt. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 003 · 00:20–00:30 · A · Satellite map

**VO:** "By the end of this video, you'll know exactly how it worked. … That line is the Nile. Nearly everyone in Egypt lives along it, because almost everything else is desert."

- **Visual:** The Guide flips the card: it becomes a full-screen satellite night image of Egypt: dark desert and one thin glowing green line, the Nile, ending in a green fan (the delta). The Guide steps in at bottom right and taps the line with his spear tip. Tiny people icons cluster along the green strip; the brown desert stays empty.
- **On-screen text:** THE NILE / NEARLY EVERYONE LIVES HERE
- **Camera / animation:** Card flip transition into the map; slow zoom from space down to the valley
- **SFX / music:** whoosh on the flip, light string swell
- **Pace:** 30 spoken words · ≈ 11.7 s at locked speed. Dense line: do NOT speed up. Let it run to ~11.7s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: The Guide flips the card: it becomes a full-screen satellite night image of Egypt: dark desert and one thin glowing green line, the Nile, ending in a green fan (the delta). The Guide steps in at bottom right and taps the line with his spear tip. Tiny people icons cluster along the green strip; the brown desert stays empty. Include the Guide exactly as in the character reference. Text in frame: THE NILE / NEARLY EVERYONE LIVES HERE.`
- **AI motion prompt:** `Card flip transition into the map; slow zoom from space down to the valley. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 004 · 00:30–00:40 · A · Satellite map

**VO:** "Every summer, monsoon rains in the highlands of Ethiopia swelled the river. In Egypt, it flooded the valley for about three months, and when the water pulled back,"

- **Visual:** Satellite map zooms south to the Ethiopian highlands. Animated grey rain clouds rain on the highlands; a blue pulse runs north down the Blue Nile into Egypt. Cut to an illustrated valley: the river overflows its banks and water spreads across the fields. The Guide stands on a small hill, holding his hat as the water rises around the hill.
- **On-screen text:** ETHIOPIA / MONSOON / ~3 MONTHS
- **Camera / animation:** Map pan south then north following the blue pulse; water level rises steadily
- **SFX / music:** rain, rushing river
- **Pace:** 28 spoken words · ≈ 10.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map zooms south to the Ethiopian highlands. Animated grey rain clouds rain on the highlands; a blue pulse runs north down the Blue Nile into Egypt. Cut to an illustrated valley: the river overflows its banks and water spreads across the fields. The Guide stands on a small hill, holding his hat as the water rises around the hill. Include the Guide exactly as in the character reference. Text in frame: ETHIOPIA / MONSOON / ~3 MONTHS.`
- **AI motion prompt:** `Map pan south then north following the blue pulse; water level rises steadily. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 005 · 00:40–00:50 · C · Illustrated world

**VO:** "it left a layer of black, fertile mud. Egyptians named their country after it: Kemet, the Black Land. The desert on both sides was Deshret, the Red Land."

- **Visual:** The water slides back, leaving a thick black stripe of mud along the river, with yellow-brown desert on both sides. A label pops on the black strip: KEMET (BLACK LAND), and on the desert: DESHRET (RED LAND). The Guide crouches and scoops black mud in his hand, showing it to camera with a grin.
- **On-screen text:** KEMET = BLACK LAND / DESHRET = RED LAND
- **Camera / animation:** Top-down cut-away view of the valley; labels hand-written in white chalk style
- **SFX / music:** squelch, two soft label pops
- **Pace:** 28 spoken words · ≈ 9.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: The water slides back, leaving a thick black stripe of mud along the river, with yellow-brown desert on both sides. A label pops on the black strip: KEMET (BLACK LAND), and on the desert: DESHRET (RED LAND). The Guide crouches and scoops black mud in his hand, showing it to camera with a grin. Include the Guide exactly as in the character reference. Text in frame: KEMET = BLACK LAND / DESHRET = RED LAND.`
- **AI motion prompt:** `Top-down cut-away view of the valley; labels hand-written in white chalk style. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 006 · 00:50–01:00 · B · Grey studio

**VO:** "The Egyptian year was even built around the river. It had three seasons: Flood, Growing and Harvest. Farming, taxes and festivals all followed that cycle."

- **Visual:** Grey studio. A big round calendar wheel split into three coloured slices: blue FLOOD (waves icon), green GROWING (sprout icon), gold HARVEST (wheat icon). It rotates slowly. Small icons orbit it: a tax scroll, a farmer's hoe, a festival drum. The Guide points at each slice as it lights up.
- **On-screen text:** FLOOD · GROWING · HARVEST
- **Camera / animation:** Wheel spins one third per season; icons pop in on "farming, taxes and festivals"
- **SFX / music:** tick-click on each slice, light drum
- **Pace:** 25 spoken words · ≈ 9.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio. A big round calendar wheel split into three coloured slices: blue FLOOD (waves icon), green GROWING (sprout icon), gold HARVEST (wheat icon). It rotates slowly. Small icons orbit it: a tax scroll, a farmer's hoe, a festival drum. The Guide points at each slice as it lights up. Include the Guide exactly as in the character reference. Text in frame: FLOOD · GROWING · HARVEST.`
- **AI motion prompt:** `Wheel spins one third per season; icons pop in on "farming, taxes and festivals". Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 007 · 01:00–01:10 · C · Illustrated world

**VO:** "That mud gave Egypt something rare in the ancient world: a reliable surplus. Farmers grew far more grain than they needed, and that extra grain could feed builders, soldiers, priests and officials."

- **Visual:** Field scene, bright sky with cartoon clouds: a stick-figure farmer stands next to a mountain of grain sacks far bigger than one small bowl in his hand. Arrows from the pile run out to small icons: a builder with a hammer, a soldier with a spear, a priest, a scribe. The Guide nods from the side.
- **On-screen text:** SURPLUS
- **Camera / animation:** Pile grows in three quick steps; arrows draw on one by one
- **SFX / music:** grain pouring, pop on each icon
- **Pace:** 32 spoken words · ≈ 11.4 s at locked speed. Dense line: do NOT speed up. Let it run to ~11.4s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Field scene, bright sky with cartoon clouds: a stick-figure farmer stands next to a mountain of grain sacks far bigger than one small bowl in his hand. Arrows from the pile run out to small icons: a builder with a hammer, a soldier with a spear, a priest, a scribe. The Guide nods from the side. Include the Guide exactly as in the character reference. Text in frame: SURPLUS.`
- **AI motion prompt:** `Pile grows in three quick steps; arrows draw on one by one. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 008 · 01:10–01:20 · C · Illustrated world

**VO:** "It paid for everything you're about to see. … They measured the flood on stone stairways called Nilometers. A high flood meant big harvests and higher taxes."

- **Visual:** The grain pile turns into a golden coin-like glow that flies toward silhouettes of pyramids and temples on the horizon. Cut: stone stairway going down into the river with tick marks carved in the wall: a Nilometer. Water rises up the steps; a scribe writes numbers. A HIGH mark shows a fat wheat sheaf and a tax scroll. The Guide is not in this shot.
- **On-screen text:** NILOMETER / HIGH FLOOD = BIG HARVEST + HIGH TAXES
- **Camera / animation:** Glow flies to horizon; then tilt down the Nilometer steps as water rises
- **SFX / music:** shimmer, water lapping, scroll unrolling
- **Pace:** 26 spoken words · ≈ 9.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: The grain pile turns into a golden coin-like glow that flies toward silhouettes of pyramids and temples on the horizon. Cut: stone stairway going down into the river with tick marks carved in the wall: a Nilometer. Water rises up the steps; a scribe writes numbers. A HIGH mark shows a fat wheat sheaf and a tax scroll. Text in frame: NILOMETER / HIGH FLOOD = BIG HARVEST + HIGH TAXES.`
- **AI motion prompt:** `Glow flies to horizon; then tilt down the Nilometer steps as water rises. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 009 · 01:20–01:30 · C · Illustrated world

**VO:** "A low one meant famine. Keep that in mind: everything in this story rises and falls with the river. … The river was also Egypt's highway."

- **Visual:** Same Nilometer: water drops to the lowest marks; the wheat sheaf wilts and an empty bowl appears. The Guide points to the camera seriously, then a wave graph line (river level) rises and falls across the screen. Cut to a wide river with a boat starting to move.
- **On-screen text:** LOW FLOOD = FAMINE / EVERYTHING RISES AND FALLS WITH THE RIVER
- **Camera / animation:** Water drains; a white wave line draws across screen
- **SFX / music:** low drone, sad single note, then river ambience
- **Pace:** 25 spoken words · ≈ 8.9 s at locked speed. Light line: keep the same speed; leave a ~1.1s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Same Nilometer: water drops to the lowest marks; the wheat sheaf wilts and an empty bowl appears. The Guide points to the camera seriously, then a wave graph line (river level) rises and falls across the screen. Cut to a wide river with a boat starting to move. Include the Guide exactly as in the character reference. Text in frame: LOW FLOOD = FAMINE / EVERYTHING RISES AND FALLS WITH THE RIVER.`
- **AI motion prompt:** `Water drains; a white wave line draws across screen. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 010 · 01:30–01:40 · A · Satellite map

**VO:** "The current carried boats north, and the wind usually blows from the north, so boats could sail back south. Moving grain, stone and armies along the valley was easy."

- **Visual:** Satellite map of the Nile valley. A small boat icon floats north with a blue arrow labelled CURRENT. Then a sail unfurls and a white wind arrow from the north pushes it back south. Small icons of grain sacks, stone blocks and soldiers ride on boats both ways. The Guide sits on a boat at the bottom right, waving.
- **On-screen text:** CURRENT ⬆ NORTH / WIND ⬇ SOUTH
- **Camera / animation:** Arrows animate in both directions; boats loop up and down the river
- **SFX / music:** wind gust, sail flap, water
- **Pace:** 29 spoken words · ≈ 9.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map of the Nile valley. A small boat icon floats north with a blue arrow labelled CURRENT. Then a sail unfurls and a white wind arrow from the north pushes it back south. Small icons of grain sacks, stone blocks and soldiers ride on boats both ways. The Guide sits on a boat at the bottom right, waving. Include the Guide exactly as in the character reference. Text in frame: CURRENT ⬆ NORTH / WIND ⬇ SOUTH.`
- **AI motion prompt:** `Arrows animate in both directions; boats loop up and down the river. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

**Batch 1 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 2: Unification, gods and the god-king (Scenes 11–20, 01:40–03:20)

#### Scene 011 · 01:40–01:50 · A · Satellite map

**VO:** "And the deserts on either side worked like walls. For centuries, they kept large armies out, so Egypt could grow rich without constantly defending itself."

- **Visual:** Satellite map: the desert on both sides of the green Nile gets tall stone-wall graphics drawn along it. Tiny enemy army icons march toward Egypt from east and west, hit the walls and turn back. Inside the walls, coins and grain stack up. The Guide leans on his spear, relaxed.
- **On-screen text:** NATURAL WALLS
- **Camera / animation:** Walls rise from the sand; armies bounce off
- **SFX / music:** stone rumble, march, bonk
- **Pace:** 25 spoken words · ≈ 9.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map: the desert on both sides of the green Nile gets tall stone-wall graphics drawn along it. Tiny enemy army icons march toward Egypt from east and west, hit the walls and turn back. Inside the walls, coins and grain stack up. The Guide leans on his spear, relaxed. Include the Guide exactly as in the character reference. Text in frame: NATURAL WALLS.`
- **AI motion prompt:** `Walls rise from the sand; armies bounce off. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 012 · 01:50–02:00 · A · Satellite map

**VO:** "Around 3100 BC, a king from the south conquered the north and united Upper and Lower Egypt. Upper Egypt was the south, because the Nile flows north."

- **Visual:** Satellite map of Egypt split in two colours: the long south valley (UPPER EGYPT) and the northern delta fan (LOWER EGYPT). A crowned stick king in a white tall crown marches up from the south and plants a flag in the north; both regions merge into one colour. A white arrow shows the Nile flowing north (upward), and the Guide taps the label UPPER = SOUTH.
- **On-screen text:** 3100 BC / UPPER EGYPT (SOUTH) · LOWER EGYPT (NORTH)
- **Camera / animation:** Map turned so north is up; the colour merge wipes from south to north
- **SFX / music:** drum march, merge whoosh
- **Pace:** 30 spoken words · ≈ 10.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map of Egypt split in two colours: the long south valley (UPPER EGYPT) and the northern delta fan (LOWER EGYPT). A crowned stick king in a white tall crown marches up from the south and plants a flag in the north; both regions merge into one colour. A white arrow shows the Nile flowing north (upward), and the Guide taps the label UPPER = SOUTH. Include the Guide exactly as in the character reference. Text in frame: 3100 BC / UPPER EGYPT (SOUTH) · LOWER EGYPT (NORTH).`
- **AI motion prompt:** `Map turned so north is up; the colour merge wipes from south to north. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 013 · 02:00–02:10 · D · Artefact / relief close-up

**VO:** "Egyptians remembered the founder as Menes; historians link him to a king called Narmer. The capital, Memphis, sat where the valley meets the delta,"

- **Visual:** A clean drawing of the Narmer Palette-style stone slab, simplified in the cartoon style, with two name tags: MENES (legend) and NARMER (history), linked by a dotted line and a question mark. Then the map returns, zoomed on the point where the valley opens into the delta, with a city icon MEMPHIS. The Guide is not in this shot.
- **On-screen text:** MENES = NARMER? / MEMPHIS
- **Camera / animation:** Slow zoom on the palette; cut to map zoom on Memphis
- **SFX / music:** pen scribble, map ping
- **Pace:** 24 spoken words · ≈ 9.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: A clean drawing of the Narmer Palette-style stone slab, simplified in the cartoon style, with two name tags: MENES (legend) and NARMER (history), linked by a dotted line and a question mark. Then the map returns, zoomed on the point where the valley opens into the delta, with a city icon MEMPHIS. Text in frame: MENES = NARMER? / MEMPHIS.`
- **AI motion prompt:** `Slow zoom on the palette; cut to map zoom on Memphis. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 014 · 02:10–02:20 · B · Grey studio

**VO:** "so it could control both. … Around the same time, hieroglyphic writing appeared. One of its first big jobs was running the state: recording harvests,"

- **Visual:** Grey studio. Two arrows from Memphis reach up to the delta and down to the valley (control both). Then a papyrus scroll unrolls in front of the Guide and hieroglyphs appear on it one by one (owl, reed, water line, eye). A scribe stick figure sits cross-legged counting grain sacks.
- **On-screen text:** HIEROGLYPHS
- **Camera / animation:** Arrows draw out; scroll unrolls left to right
- **SFX / music:** ink brush strokes, scroll unrolling
- **Pace:** 24 spoken words · ≈ 8.9 s at locked speed. Light line: keep the same speed; leave a ~1.1s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio. Two arrows from Memphis reach up to the delta and down to the valley (control both). Then a papyrus scroll unrolls in front of the Guide and hieroglyphs appear on it one by one (owl, reed, water line, eye). A scribe stick figure sits cross-legged counting grain sacks. Include the Guide exactly as in the character reference. Text in frame: HIEROGLYPHS.`
- **AI motion prompt:** `Arrows draw out; scroll unrolls left to right. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 015 · 02:20–02:30 · B · Grey studio

**VO:** "taxes and stores, so one king could govern a country hundreds of kilometres long. … Below the king, a chief minister, the vizier,"

- **Visual:** The scroll fills with tally marks next to grain, tax and storehouse icons. A long Egypt map stretches across the bottom with a ruler: HUNDREDS OF KM. Then a pyramid-shaped org chart begins: the king at the top, and a vizier stick figure (white robe, scroll) appears just below him. The Guide is not in this shot.
- **On-screen text:** THE VIZIER
- **Camera / animation:** Ruler measures the map; org chart builds top-down
- **SFX / music:** counting clicks, soft pop
- **Pace:** 22 spoken words · ≈ 8.4 s at locked speed. Light line: keep the same speed; leave a ~1.6s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: The scroll fills with tally marks next to grain, tax and storehouse icons. A long Egypt map stretches across the bottom with a ruler: HUNDREDS OF KM. Then a pyramid-shaped org chart begins: the king at the top, and a vizier stick figure (white robe, scroll) appears just below him. Text in frame: THE VIZIER.`
- **AI motion prompt:** `Ruler measures the map; org chart builds top-down. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 016 · 02:30–02:40 · B · Grey studio

**VO:** "ran the government, and the country was divided into about 40 provinces, each with its own governor. Remember those governors."

- **Visual:** The org chart expands: under the vizier, 40 small house icons in a grid (provinces), each with a governor stick figure. The governors' icons glow briefly. The Guide narrows his eyes and taps his temple: remember them.
- **On-screen text:** 40 PROVINCES / REMEMBER THE GOVERNORS
- **Camera / animation:** Grid fills in fast (cascading pop); highlight pulse on the governors
- **SFX / music:** cascading pops, ominous low note
- **Pace:** 20 spoken words · ≈ 8.9 s at locked speed. Light line: keep the same speed; leave a ~1.1s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: The org chart expands: under the vizier, 40 small house icons in a grid (provinces), each with a governor stick figure. The governors' icons glow briefly. The Guide narrows his eyes and taps his temple: remember them. Include the Guide exactly as in the character reference. Text in frame: 40 PROVINCES / REMEMBER THE GOVERNORS.`
- **AI motion prompt:** `Grid fills in fast (cascading pop); highlight pulse on the governors. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 017 · 02:40–02:50 · C · Illustrated world

**VO:** "Egyptians worshipped many gods tied to the world around them: Ra, the sun; Osiris, god of the dead and of rebirth, linked to the flood's yearly return;"

- **Visual:** Sky scene: RA as a falcon-headed figure with a sun disc on his head rises over the horizon. Then OSIRIS (green skin, white crown, crook and flail) appears beside the river as the water rises: a little flood icon with a circular arrow. The Guide looks up in awe.
- **On-screen text:** RA · OSIRIS
- **Camera / animation:** Sun rises behind Ra; flood loop arrow spins near Osiris
- **SFX / music:** choir hum, rising water
- **Pace:** 27 spoken words · ≈ 9.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Sky scene: RA as a falcon-headed figure with a sun disc on his head rises over the horizon. Then OSIRIS (green skin, white crown, crook and flail) appears beside the river as the water rises: a little flood icon with a circular arrow. The Guide looks up in awe. Include the Guide exactly as in the character reference. Text in frame: RA · OSIRIS.`
- **AI motion prompt:** `Sun rises behind Ra; flood loop arrow spins near Osiris. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 018 · 02:50–03:00 · C · Illustrated world

**VO:** "and his wife, Isis. These gods would last for 3,000 years. … The king wasn't just a ruler. Egyptians believed he was a god on earth, whose job was to keep Ma'at,"

- **Visual:** ISIS (throne headdress, wings) joins Osiris. A timeline bar under the three gods stretches across the screen: 3,000 YEARS. Then cut to the pharaoh on a throne, glowing, with the double crown. The Guide bows playfully.
- **On-screen text:** ISIS / 3,000 YEARS / GOD ON EARTH
- **Camera / animation:** Timeline bar extends; glow pulse on pharaoh
- **SFX / music:** shimmer, gong
- **Pace:** 32 spoken words · ≈ 9.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: ISIS (throne headdress, wings) joins Osiris. A timeline bar under the three gods stretches across the screen: 3,000 YEARS. Then cut to the pharaoh on a throne, glowing, with the double crown. The Guide bows playfully. Include the Guide exactly as in the character reference. Text in frame: ISIS / 3,000 YEARS / GOD ON EARTH.`
- **AI motion prompt:** `Timeline bar extends; glow pulse on pharaoh. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 019 · 03:00–03:10 · B · Grey studio

**VO:** "the order of the universe, so the sun rose and the river flooded on time. That made him all-powerful, as long as the river behaved."

- **Visual:** Grey studio. A balance scale with a feather labelled MA'AT. On one side: a sun rising on time and the river flooding on time, both with green ticks. The pharaoh stands in the middle, holding everything up. Then a tiny dark cloud and dropping river appear in the corner, and the pharaoh's glow flickers. The Guide is not in this shot.
- **On-screen text:** MA'AT = ORDER / ...AS LONG AS THE RIVER BEHAVED
- **Camera / animation:** Scale balances; flicker on the last line
- **SFX / music:** soft bell, flicker buzz
- **Pace:** 26 spoken words · ≈ 8.9 s at locked speed. Light line: keep the same speed; leave a ~1.1s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio. A balance scale with a feather labelled MA'AT. On one side: a sun rising on time and the river flooding on time, both with green ticks. The pharaoh stands in the middle, holding everything up. Then a tiny dark cloud and dropping river appear in the corner, and the pharaoh's glow flickers. Text in frame: MA'AT = ORDER / ...AS LONG AS THE RIVER BEHAVED.`
- **AI motion prompt:** `Scale balances; flicker on the last line. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 020 · 03:10–03:20 · C · Illustrated world

**VO:** "Egyptians believed the king's spirit lived on after death, and that his afterlife helped keep the whole country in order. So his tomb mattered to everyone."

- **Visual:** Night scene: a glowing translucent spirit (ba bird with a human head) flies out of the king's body up to the stars. Lines from the spirit connect to villages, fields and the river below, keeping them in order. Villagers look toward a tomb on the horizon. The Guide is not in this shot.
- **On-screen text:** THE AFTERLIFE KEEPS ORDER
- **Camera / animation:** Spirit rises; connecting lines draw down to the villages
- **SFX / music:** magical twinkle, night insects
- **Pace:** 26 spoken words · ≈ 10.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Night scene: a glowing translucent spirit (ba bird with a human head) flies out of the king's body up to the stars. Lines from the spirit connect to villages, fields and the river below, keeping them in order. Villagers look toward a tomb on the horizon. Text in frame: THE AFTERLIFE KEEPS ORDER.`
- **AI motion prompt:** `Spirit rises; connecting lines draw down to the villages. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

**Batch 2 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 3: The first pyramids (Scenes 21–30, 03:20–05:00)

#### Scene 021 · 03:20–03:30 · C · Illustrated world

**VO:** "Early kings were buried under flat mudbrick tombs called mastabas. … Around 2650 BC, King Djoser's official Imhotep built his tomb in stone instead,"

- **Visual:** Daylight desert: a low, flat, rectangular mudbrick tomb (mastaba) with a label. Then Imhotep, a stick figure with a shaved head and a scroll of plans, appears beside it with King Djoser. Imhotep places a stone block on top of the mastaba. The Guide is not in this shot.
- **On-screen text:** MASTABA / 2650 BC / IMHOTEP
- **Camera / animation:** Side view; stone block drops onto the mudbrick
- **SFX / music:** brick thuds, stone clack
- **Pace:** 26 spoken words · ≈ 10.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Daylight desert: a low, flat, rectangular mudbrick tomb (mastaba) with a label. Then Imhotep, a stick figure with a shaved head and a scroll of plans, appears beside it with King Djoser. Imhotep places a stone block on top of the mastaba. Text in frame: MASTABA / 2650 BC / IMHOTEP.`
- **AI motion prompt:** `Side view; stone block drops onto the mudbrick. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 022 · 03:30–03:40 · C · Illustrated world

**VO:** "stacking six layers about 62 metres high. The Step Pyramid is the oldest large cut-stone building in the world, and it started the age of pyramids."

- **Visual:** The block multiplies: six stone layers stack up one by one into the Step Pyramid of Saqqara. A height ruler next to it reads 62 M. The Guide, tiny at the base, cranes his neck up. A gold badge appears: OLDEST LARGE CUT-STONE BUILDING.
- **On-screen text:** STEP PYRAMID / 62 M
- **Camera / animation:** Each layer stacks on a beat (6 beats); tilt up
- **SFX / music:** 6 heavy stone thuds, fanfare sting
- **Pace:** 28 spoken words · ≈ 9.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: The block multiplies: six stone layers stack up one by one into the Step Pyramid of Saqqara. A height ruler next to it reads 62 M. The Guide, tiny at the base, cranes his neck up. A gold badge appears: OLDEST LARGE CUT-STONE BUILDING. Include the Guide exactly as in the character reference. Text in frame: STEP PYRAMID / 62 M.`
- **AI motion prompt:** `Each layer stacks on a beat (6 beats); tilt up. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 023 · 03:40–03:50 · C · Illustrated world

**VO:** "The next king, Sneferu, struggled to get the shape right. His Bent Pyramid changes angle halfway up, most likely because the first slope was too steep."

- **Visual:** King Sneferu scratches his head beside the Bent Pyramid. Its steep lower slope suddenly changes angle halfway up, shown with a red angle mark and a wobble. The Guide winces.
- **On-screen text:** SNEFERU / BENT PYRAMID
- **Camera / animation:** Angle line draws; slight wobble on the change
- **SFX / music:** comic boing, creak
- **Pace:** 26 spoken words · ≈ 9.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: King Sneferu scratches his head beside the Bent Pyramid. Its steep lower slope suddenly changes angle halfway up, shown with a red angle mark and a wobble. The Guide winces. Include the Guide exactly as in the character reference. Text in frame: SNEFERU / BENT PYRAMID.`
- **AI motion prompt:** `Angle line draws; slight wobble on the change. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 024 · 03:50–04:00 · C · Illustrated world

**VO:** "His Red Pyramid finally got it right: the first true smooth-sided pyramid. … His son Khufu built the Great Pyramid of Giza around 2560 BC:"

- **Visual:** Next to it, the Red Pyramid appears with smooth sides and a reddish tint; a green check mark pops. Cut to Khufu (stick king with nemes headdress) stepping onto Giza plateau holding a plan scroll; the year appears in yellow. The Guide is not in this shot.
- **On-screen text:** RED PYRAMID ✓ / KHUFU · 2560 BC
- **Camera / animation:** Smooth pyramid slides up; cut to Khufu
- **SFX / music:** ding, fanfare
- **Pace:** 28 spoken words · ≈ 10.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Next to it, the Red Pyramid appears with smooth sides and a reddish tint; a green check mark pops. Cut to Khufu (stick king with nemes headdress) stepping onto Giza plateau holding a plan scroll; the year appears in yellow. Text in frame: RED PYRAMID ✓ / KHUFU · 2560 BC.`
- **AI motion prompt:** `Smooth pyramid slides up; cut to Khufu. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 025 · 04:00–04:10 · C · Illustrated world

**VO:** "about 2.3 million stone blocks, 146 metres tall when finished. Nothing built by humans stood taller for about 3,800 years."

- **Visual:** The Great Pyramid builds up from a counter of blocks racing to 2,300,000. A height ruler reads 146 M. Then a timeline: other buildings shown in silhouette remain shorter; a counter rolls to 3,800 YEARS. The Guide's hat falls off from looking up.
- **On-screen text:** 2.3 MILLION BLOCKS / 146 M / TALLEST FOR 3,800 YEARS
- **Camera / animation:** Number counter, tilt up, timeline slide
- **SFX / music:** rapid ticking counter, hat plop
- **Pace:** 29 spoken words · ≈ 10.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: The Great Pyramid builds up from a counter of blocks racing to 2,300,000. A height ruler reads 146 M. Then a timeline: other buildings shown in silhouette remain shorter; a counter rolls to 3,800 YEARS. The Guide's hat falls off from looking up. Include the Guide exactly as in the character reference. Text in frame: 2.3 MILLION BLOCKS / 146 M / TALLEST FOR 3,800 YEARS.`
- **AI motion prompt:** `Number counter, tilt up, timeline slide. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 026 · 04:10–04:20 · C · Illustrated world

**VO:** "Deep inside, narrow passages lead to the king's granite burial chamber. By the time explorers reached it, it was empty. … The river made it possible."

- **Visual:** Cut-away of the pyramid: a narrow passage glows as the Guide crawls through it to a granite chamber with a lone empty sarcophagus. A cobweb hangs; he shrugs. Then a quick cut to the Nile with boats ready.
- **On-screen text:** EMPTY / THE RIVER MADE IT POSSIBLE
- **Camera / animation:** Cut-away side view; camera follows the Guide through the passage
- **SFX / music:** echoing footsteps, cricket, river
- **Pace:** 25 spoken words · ≈ 9.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Cut-away of the pyramid: a narrow passage glows as the Guide crawls through it to a granite chamber with a lone empty sarcophagus. A cobweb hangs; he shrugs. Then a quick cut to the Nile with boats ready. Include the Guide exactly as in the character reference. Text in frame: EMPTY / THE RIVER MADE IT POSSIBLE.`
- **AI motion prompt:** `Cut-away side view; camera follows the Guide through the passage. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 027 · 04:20–04:30 · A · Satellite map

**VO:** "Most of the stone was cut right at Giza, but fine white limestone for the outer casing came by boat from quarries across the river, and huge granite beams for the king's burial chamber came from Aswan,"

- **Visual:** Map of Giza and the river: a local quarry icon right next to the pyramids; a white limestone block on a boat crosses the river from TURA; a long dotted line runs far south to ASWAN, where a huge pink granite beam loads onto a big barge. The Guide is not in this shot.
- **On-screen text:** GIZA · TURA LIMESTONE · ASWAN GRANITE
- **Camera / animation:** Map slides; boats animate along dotted routes
- **SFX / music:** oars, water, creaking wood
- **Pace:** 37 spoken words · ≈ 12.2 s at locked speed. Dense line: do NOT speed up. Let it run to ~12.2s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map of Giza and the river: a local quarry icon right next to the pyramids; a white limestone block on a boat crosses the river from TURA; a long dotted line runs far south to ASWAN, where a huge pink granite beam loads onto a big barge. Text in frame: GIZA · TURA LIMESTONE · ASWAN GRANITE.`
- **AI motion prompt:** `Map slides; boats animate along dotted routes. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 028 · 04:30–04:40 · C · Illustrated world

**VO:** "hundreds of kilometres upstream. … How they raised the blocks is still debated. The most likely answer is ramps of mudbrick and rubble, with blocks dragged on wooden sledges."

- **Visual:** The granite barge floats down the Nile past palm trees. Then a big question mark over the pyramid. A ramp of mudbrick and rubble rises around a half-built pyramid; workers drag a block on a wooden sledge with ropes. The Guide is not in this shot.
- **On-screen text:** HUNDREDS OF KM UPSTREAM / HOW? / RAMPS + SLEDGES
- **Camera / animation:** Barge glides; ramp draws on in stages
- **SFX / music:** rope strain, grunts, wood scraping
- **Pace:** 28 spoken words · ≈ 10.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: The granite barge floats down the Nile past palm trees. Then a big question mark over the pyramid. A ramp of mudbrick and rubble rises around a half-built pyramid; workers drag a block on a wooden sledge with ropes. Text in frame: HUNDREDS OF KM UPSTREAM / HOW? / RAMPS + SLEDGES.`
- **AI motion prompt:** `Barge glides; ramp draws on in stages. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 029 · 04:40–04:50 · C · Illustrated world

**VO:** "Wetting the sand in front of a sledge cuts the friction sharply, and an Egyptian tomb painting shows a worker doing exactly that. … It was not built by slaves."

- **Visual:** Close-up: a worker pours water from a jar onto the sand in front of the sledge; a friction meter needle drops from red to green and the sledge slides easily. A small inset shows the ancient tomb painting of the same action. Then a big NOT SLAVES stamp appears. The Guide is not in this shot.
- **On-screen text:** WET SAND = LESS FRICTION / NOT SLAVES
- **Camera / animation:** Inset frame pops in top right; stamp at the end
- **SFX / music:** water pour, smooth slide, stamp
- **Pace:** 29 spoken words · ≈ 9.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Close-up: a worker pours water from a jar onto the sand in front of the sledge; a friction meter needle drops from red to green and the sledge slides easily. A small inset shows the ancient tomb painting of the same action. Then a big NOT SLAVES stamp appears. Text in frame: WET SAND = LESS FRICTION / NOT SLAVES.`
- **AI motion prompt:** `Inset frame pops in top right; stamp at the end. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 030 · 04:50–05:00 · C · Illustrated world

**VO:** "Archaeologists found the builders' town beside the pyramids, with bakeries, breweries and sleeping halls, and the workers' own tombs nearby."

- **Visual:** Workers' town beside the pyramids: a bakery with bread loaves, a brewery with jars, long sleeping halls, and small tombs for the workers. The Guide walks through, waving at the bakers. Labels pop above each building.
- **On-screen text:** BAKERIES · BREWERIES · SLEEPING HALLS · WORKERS' TOMBS
- **Camera / animation:** Slow horizontal pan through the town
- **SFX / music:** town bustle, crackling ovens
- **Pace:** 20 spoken words · ≈ 8.4 s at locked speed. Light line: keep the same speed; leave a ~1.6s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Workers' town beside the pyramids: a bakery with bread loaves, a brewery with jars, long sleeping halls, and small tombs for the workers. The Guide walks through, waving at the bakers. Labels pop above each building. Include the Guide exactly as in the character reference. Text in frame: BAKERIES · BREWERIES · SLEEPING HALLS · WORKERS' TOMBS.`
- **AI motion prompt:** `Slow horizontal pan through the town. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

**Batch 3 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 4: Pyramid builders and the first collapse (Scenes 31–40, 05:00–06:40)

#### Scene 031 · 05:00–05:10 · C · Illustrated world

**VO:** "Many were farmers working in rotating shifts, likely during the flood season, when their fields were under water anyway. … We even have a logbook from one of the crews."

- **Visual:** Split screen: on the left, flooded fields with a farmer's hut on stilts; on the right, the same farmer working at the pyramid. A rotating shift wheel shows teams swapping. Then an old notebook icon appears in the Guide's hands.
- **On-screen text:** ROTATING SHIFTS / THE LOGBOOK
- **Camera / animation:** Wipe between halves; wheel rotates
- **SFX / music:** water, crowd, page flip
- **Pace:** 29 spoken words · ≈ 10.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Split screen: on the left, flooded fields with a farmer's hut on stilts; on the right, the same farmer working at the pyramid. A rotating shift wheel shows teams swapping. Then an old notebook icon appears in the Guide's hands. Include the Guide exactly as in the character reference. Text in frame: ROTATING SHIFTS / THE LOGBOOK.`
- **AI motion prompt:** `Wipe between halves; wheel rotates. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 032 · 05:10–05:20 · D · Artefact / relief close-up

**VO:** "In 2013, archaeologists found the oldest inscribed papyri ever discovered, including the diary of an inspector named Merer."

- **Visual:** Archaeologists in 2013 dig at a desert site on the Red Sea coast and lift rolled papyri from the sand. One unrolls in close-up: hieratic writing. A name tag: MERER, INSPECTOR, with a simple stick portrait of him. The Guide is not in this shot.
- **On-screen text:** 2013 / OLDEST INSCRIBED PAPYRI / DIARY OF MERER
- **Camera / animation:** Zoom into the papyrus
- **SFX / music:** digging, papyrus crackle
- **Pace:** 19 spoken words · ≈ 9.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: Archaeologists in 2013 dig at a desert site on the Red Sea coast and lift rolled papyri from the sand. One unrolls in close-up: hieratic writing. A name tag: MERER, INSPECTOR, with a simple stick portrait of him. Text in frame: 2013 / OLDEST INSCRIBED PAPYRI / DIARY OF MERER.`
- **AI motion prompt:** `Zoom into the papyrus. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 033 · 05:20–05:30 · A · Satellite map

**VO:** "It records his team ferrying limestone from the quarries at Tura to a harbour at Giza, trip after trip, in the reign of Khufu."

- **Visual:** Map: TURA quarries on the east bank, a boat with a white limestone block crossing to a GIZA HARBOUR icon, looping back and forth (trip counter ticking up). Merer stands on the boat with a scroll. A KHUFU cartouche sits in the corner. The Guide is not in this shot.
- **On-screen text:** TURA → GIZA / TRIP AFTER TRIP
- **Camera / animation:** Boat loops 3–4 times, counter ticks
- **SFX / music:** oars, counter clicks
- **Pace:** 24 spoken words · ≈ 8.4 s at locked speed. Light line: keep the same speed; leave a ~1.6s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map: TURA quarries on the east bank, a boat with a white limestone block crossing to a GIZA HARBOUR icon, looping back and forth (trip counter ticking up). Merer stands on the boat with a scroll. A KHUFU cartouche sits in the corner. Text in frame: TURA → GIZA / TRIP AFTER TRIP.`
- **AI motion prompt:** `Boat loops 3–4 times, counter ticks. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 034 · 05:30–05:40 · C · Illustrated world

**VO:** "A pyramid wasn't just a tomb. Each came with temples, a causeway and farmland whose harvests paid priests to make offerings to the dead king forever."

- **Visual:** A pyramid complex: the pyramid, a valley temple, a long causeway, and green farmland around it. Priests carry offering trays (bread, beer, geese) to the dead king's temple. An infinity symbol glows above. The Guide is not in this shot.
- **On-screen text:** NOT JUST A TOMB / FOREVER
- **Camera / animation:** Wide establishing shot, then gentle pan along the causeway
- **SFX / music:** chant, birds
- **Pace:** 26 spoken words · ≈ 9.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A pyramid complex: the pyramid, a valley temple, a long causeway, and green farmland around it. Priests carry offering trays (bread, beer, geese) to the dead king's temple. An infinity symbol glows above. Text in frame: NOT JUST A TOMB / FOREVER.`
- **AI motion prompt:** `Wide establishing shot, then gentle pan along the causeway. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 035 · 05:40–05:50 · B · Grey studio

**VO:** "Over generations, more and more of Egypt's land and grain went to supporting dead kings and their priests. … Khufu's son Khafre built the second pyramid at Giza,"

- **Visual:** Grey studio: a pie chart of Egypt's land and grain; the slice labelled DEAD KINGS & PRIESTS grows bigger with each generation tick. Cut to Giza: Khafre stands beside the second pyramid. The Guide is not in this shot.
- **On-screen text:** MORE AND MORE / KHAFRE
- **Camera / animation:** Pie slice grows in 3 steps
- **SFX / music:** ticking, coin slides
- **Pace:** 27 spoken words · ≈ 9.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio: a pie chart of Egypt's land and grain; the slice labelled DEAD KINGS & PRIESTS grows bigger with each generation tick. Cut to Giza: Khafre stands beside the second pyramid. Text in frame: MORE AND MORE / KHAFRE.`
- **AI motion prompt:** `Pie slice grows in 3 steps. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 036 · 05:50–06:00 · C · Illustrated world

**VO:** "and the Great Sphinx was most likely carved in his reign. The third, built by Menkaure, is far smaller. After Giza, pyramids kept shrinking. … That tells you something."

- **Visual:** The Great Sphinx appears in front of Khafre's pyramid. Then three pyramids in a row shrink: big, big, small (Menkaure). After them, a line of later pyramids gets smaller and smaller. The Guide raises one finger.
- **On-screen text:** GREAT SPHINX / MENKAURE / SHRINKING
- **Camera / animation:** Pyramids lined up and shrinking in a sequence
- **SFX / music:** descending notes
- **Pace:** 28 spoken words · ≈ 9.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: The Great Sphinx appears in front of Khafre's pyramid. Then three pyramids in a row shrink: big, big, small (Menkaure). After them, a line of later pyramids gets smaller and smaller. The Guide raises one finger. Include the Guide exactly as in the character reference. Text in frame: GREAT SPHINX / MENKAURE / SHRINKING.`
- **AI motion prompt:** `Pyramids lined up and shrinking in a sequence. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 037 · 06:00–06:10 · B · Grey studio

**VO:** "The kings were spending less, while the officials, priests and provincial governors who ran the state were growing richer and more independent. … Late in this era,"

- **Visual:** A seesaw: on one side the king with a small pile of gold, going up; on the other side officials, priests and governors with growing gold piles, going down. Governors wear little crowns of their own. The Guide is not in this shot.
- **On-screen text:** KINGS ↓ · OFFICIALS & GOVERNORS ↑
- **Camera / animation:** Seesaw tips; gold piles grow
- **SFX / music:** coins clinking, seesaw creak
- **Pace:** 26 spoken words · ≈ 9.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: A seesaw: on one side the king with a small pile of gold, going up; on the other side officials, priests and governors with growing gold piles, going down. Governors wear little crowns of their own. Text in frame: KINGS ↓ · OFFICIALS & GOVERNORS ↑.`
- **AI motion prompt:** `Seesaw tips; gold piles grow. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 038 · 06:10–06:20 · C · Illustrated world

**VO:** "kings began carving spells on their burial chamber walls to help them rise to the sky after death. These Pyramid Texts are among the oldest religious writings in the world."

- **Visual:** Inside a burial chamber, workers carve columns of blue hieroglyphs on the walls. A ghostly king rises from his sarcophagus toward stars painted on the ceiling. Label: PYRAMID TEXTS. The Guide is not in this shot.
- **On-screen text:** PYRAMID TEXTS / OLDEST RELIGIOUS WRITINGS
- **Camera / animation:** Tilt up from the carved walls to the starry ceiling
- **SFX / music:** chisel taps, ethereal choir
- **Pace:** 30 spoken words · ≈ 10.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Inside a burial chamber, workers carve columns of blue hieroglyphs on the walls. A ghostly king rises from his sarcophagus toward stars painted on the ceiling. Label: PYRAMID TEXTS. Text in frame: PYRAMID TEXTS / OLDEST RELIGIOUS WRITINGS.`
- **AI motion prompt:** `Tilt up from the carved walls to the starry ceiling. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 039 · 06:20–06:30 · C · Illustrated world

**VO:** "For about 500 years, Egypt's god-kings built mountains of stone. Then the river stopped cooperating. … Around 2200 BC, the climate shifted and the floods shrank, year after year."

- **Visual:** Montage of pyramids rising, labelled 500 YEARS. Then the sky turns dull and hot; the Nile shrinks to a thin line, step by step, year counter ticking: 2200 BC. The Guide wipes sweat from his brow.
- **On-screen text:** 500 YEARS / 2200 BC / FLOODS SHRINK
- **Camera / animation:** River shrinks with each year tick; colour drains from the scene
- **SFX / music:** heat drone, ticking
- **Pace:** 33 spoken words · ≈ 11.9 s at locked speed. Dense line: do NOT speed up. Let it run to ~11.9s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Montage of pyramids rising, labelled 500 YEARS. Then the sky turns dull and hot; the Nile shrinks to a thin line, step by step, year counter ticking: 2200 BC. The Guide wipes sweat from his brow. Include the Guide exactly as in the character reference. Text in frame: 500 YEARS / 2200 BC / FLOODS SHRINK.`
- **AI motion prompt:** `River shrinks with each year tick; colour drains from the scene. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 040 · 06:30–06:40 · C · Illustrated world

**VO:** "Harvests failed and people starved. And a god-king who couldn't make the river rise no longer looked much like a god. … Pepi II, the last great king of this era,"

- **Visual:** Cracked dry fields, wilted crops, thin villagers holding empty bowls. The pharaoh stands on a balcony raising his arms, but the river doesn't rise; his golden glow cracks. Then Pepi II appears on the throne. The Guide is not in this shot.
- **On-screen text:** HARVESTS FAILED / PEPI II
- **Camera / animation:** Glow cracks and fades; cut to Pepi II
- **SFX / music:** dry wind, cracking glass sound
- **Pace:** 32 spoken words · ≈ 10.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Cracked dry fields, wilted crops, thin villagers holding empty bowls. The pharaoh stands on a balcony raising his arms, but the river doesn't rise; his golden glow cracks. Then Pepi II appears on the throne. Text in frame: HARVESTS FAILED / PEPI II.`
- **AI motion prompt:** `Glow cracks and fades; cut to Pepi II. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

**Batch 4 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 5: The Middle Kingdom (Scenes 41–50, 06:40–08:20)

#### Scene 041 · 06:40–06:50 · B · Grey studio

**VO:** "may have reigned for more than 60 years. By then, provincial governors had made their posts hereditary and were ruling like independent kings."

- **Visual:** Pepi II on his throne ages quickly: beard grows, a counter reaches 60+ YEARS. Around him, provincial governors place crowns on their own heads and hand them down to their sons (arrows down to a mini family tree). The Guide is not in this shot.
- **On-screen text:** 60+ YEARS / HEREDITARY GOVERNORS
- **Camera / animation:** Aging morph; crowns pop onto the governors
- **SFX / music:** clock ticking, crown pops
- **Pace:** 23 spoken words · ≈ 9.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Pepi II on his throne ages quickly: beard grows, a counter reaches 60+ YEARS. Around him, provincial governors place crowns on their own heads and hand them down to their sons (arrows down to a mini family tree). Text in frame: 60+ YEARS / HEREDITARY GOVERNORS.`
- **AI motion prompt:** `Aging morph; crowns pop onto the governors. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 042 · 06:50–07:00 · A · Satellite map

**VO:** "After him, central power collapsed. … For more than a century, there was no single Egypt. Rival dynasties ruled from the north and from Thebes in the south,"

- **Visual:** Map of Egypt: the single colour breaks into many coloured patches, cracking like glass. Two capitals light up: one in the north (HERAKLEOPOLIS) and THEBES in the south, with rival flags. The Guide is not in this shot.
- **On-screen text:** COLLAPSE / NO SINGLE EGYPT
- **Camera / animation:** Map shatters into pieces
- **SFX / music:** glass shatter, drum
- **Pace:** 27 spoken words · ≈ 10.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map of Egypt: the single colour breaks into many coloured patches, cracking like glass. Two capitals light up: one in the north (HERAKLEOPOLIS) and THEBES in the south, with rival flags. Text in frame: COLLAPSE / NO SINGLE EGYPT.`
- **AI motion prompt:** `Map shatters into pieces. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 043 · 07:00–07:10 · C · Illustrated world

**VO:** "local strongmen fought each other, and famine hit village after village. Historians call it the First Intermediate Period. Something lasting came out of it, too."

- **Visual:** Sunset scene: local strongmen with clubs fight on the dunes; villages with empty granaries; a title card in yellow comic text drops in. The Guide is not in this shot.
- **On-screen text:** FIRST INTERMEDIATE PERIOD
- **Camera / animation:** Title slams in; camera shakes slightly
- **SFX / music:** clashes, wind
- **Pace:** 25 spoken words · ≈ 10.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Sunset scene: local strongmen with clubs fight on the dunes; villages with empty granaries; a title card in yellow comic text drops in. Text in frame: FIRST INTERMEDIATE PERIOD.`
- **AI motion prompt:** `Title slams in; camera shakes slightly. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 044 · 07:10–07:20 · C · Illustrated world

**VO:** "With the kings weakened, wealthy local families began claiming an afterlife that had once belonged to the king, painting the old royal spells inside their own coffins."

- **Visual:** Inside a house, a wealthy local family paints the old royal spells inside a wooden coffin. A ghostly crown floats from the pharaoh's tomb over to their coffin. The Guide raises his eyebrows.
- **On-screen text:** AN AFTERLIFE FOR EVERYONE (RICH)
- **Camera / animation:** Crown floats across; brush strokes fill the coffin
- **SFX / music:** brush strokes, twinkle
- **Pace:** 27 spoken words · ≈ 10.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Inside a house, a wealthy local family paints the old royal spells inside a wooden coffin. A ghostly crown floats from the pharaoh's tomb over to their coffin. The Guide raises his eyebrows. Include the Guide exactly as in the character reference. Text in frame: AN AFTERLIFE FOR EVERYONE (RICH).`
- **AI motion prompt:** `Crown floats across; brush strokes fill the coffin. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 045 · 07:20–07:30 · A · Satellite map

**VO:** "Around 2050 BC, Mentuhotep II of Thebes defeated the northern dynasty and reunited the country. This began the Middle Kingdom."

- **Visual:** Map: Mentuhotep II marches north from Thebes with an army arrow; the northern flag falls. The map pieces fuse back into one colour. Title card. The Guide is not in this shot.
- **On-screen text:** 2050 BC / MENTUHOTEP II / MIDDLE KINGDOM
- **Camera / animation:** Arrow sweeps north; pieces merge
- **SFX / music:** march, unifying chime
- **Pace:** 23 spoken words · ≈ 10.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map: Mentuhotep II marches north from Thebes with an army arrow; the northern flag falls. The map pieces fuse back into one colour. Title card. Text in frame: 2050 BC / MENTUHOTEP II / MIDDLE KINGDOM.`
- **AI motion prompt:** `Arrow sweeps north; pieces merge. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 046 · 07:30–07:40 · A · Satellite map

**VO:** "Its kings had learned from the collapse. They moved the capital north, near the Faiyum oasis, drained its marshes to grow more food, cut the power of the provincial governors,"

- **Visual:** Map: the capital icon moves north near the FAIYUM oasis; blue marsh drains to green fields; governors' crowns shrink. The Guide gives a thumbs up.
- **On-screen text:** FAIYUM / DRAIN THE MARSHES / CUT THE GOVERNORS' POWER
- **Camera / animation:** Icon slides; marsh-to-field colour wipe
- **SFX / music:** drain gurgle, pop
- **Pace:** 30 spoken words · ≈ 10.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map: the capital icon moves north near the FAIYUM oasis; blue marsh drains to green fields; governors' crowns shrink. The Guide gives a thumbs up. Include the Guide exactly as in the character reference. Text in frame: FAIYUM / DRAIN THE MARSHES / CUT THE GOVERNORS' POWER.`
- **AI motion prompt:** `Icon slides; marsh-to-field colour wipe. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 047 · 07:40–07:50 · A · Satellite map

**VO:** "and built a chain of massive forts along the Nile in Nubia to guard the south. For about 300 years, Egypt was stable again."

- **Visual:** Map zooms south to Nubia: a chain of big mudbrick forts pops up along the Nile. Then a calm Egypt with a 300 YEARS timeline bar. The Guide is not in this shot.
- **On-screen text:** NUBIAN FORTS / 300 YEARS OF STABILITY
- **Camera / animation:** Forts pop along the river in sequence
- **SFX / music:** stone thuds, calm strings
- **Pace:** 25 spoken words · ≈ 8.4 s at locked speed. Light line: keep the same speed; leave a ~1.6s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map zooms south to Nubia: a chain of big mudbrick forts pops up along the Nile. Then a calm Egypt with a 300 YEARS timeline bar. Text in frame: NUBIAN FORTS / 300 YEARS OF STABILITY.`
- **AI motion prompt:** `Forts pop along the river in sequence. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 048 · 07:50–08:00 · C · Illustrated world

**VO:** "It was also Egypt's classic age of literature. Stories and teachings written in this period were copied in schools for centuries afterwards."

- **Visual:** A school room: young scribes sit cross-legged, copying stories onto papyrus and pottery shards; a teacher points to a scroll. Book icons float up. The Guide is not in this shot.
- **On-screen text:** CLASSIC AGE OF LITERATURE
- **Camera / animation:** Slow pan across students
- **SFX / music:** reed pens scratching
- **Pace:** 22 spoken words · ≈ 9.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A school room: young scribes sit cross-legged, copying stories onto papyrus and pottery shards; a teacher points to a scroll. Book icons float up. Text in frame: CLASSIC AGE OF LITERATURE.`
- **AI motion prompt:** `Slow pan across students. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 049 · 08:00–08:10 · B · Grey studio

**VO:** "But after about two centuries, the royal line weakened. Dozens of short-lived kings followed one another, and their grip on the north slipped."

- **Visual:** Grey studio: a line of short-lived kings appear and vanish quickly one after another (pop, pop, pop). A hand gripping the north of the map loosens. The Guide is not in this shot.
- **On-screen text:** DOZENS OF SHORT-LIVED KINGS
- **Camera / animation:** Fast pop sequence
- **SFX / music:** rapid pops, slipping sound
- **Pace:** 24 spoken words · ≈ 9.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio: a line of short-lived kings appear and vanish quickly one after another (pop, pop, pop). A hand gripping the north of the map loosens. Text in frame: DOZENS OF SHORT-LIVED KINGS.`
- **AI motion prompt:** `Fast pop sequence. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 050 · 08:10–08:20 · A · Satellite map

**VO:** "Meanwhile, settlers from the Levant had been moving into the northern delta. As the Middle Kingdom weakened, their leaders took control of the north,"

- **Visual:** Map: small arrows of settler families with donkeys move from the LEVANT into the northern delta. Then the delta turns a different colour as their leaders take over. The Guide is not in this shot.
- **On-screen text:** LEVANT → DELTA
- **Camera / animation:** Arrows trickle in; colour wipe
- **SFX / music:** footsteps, donkey bray
- **Pace:** 24 spoken words · ≈ 9.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map: small arrows of settler families with donkeys move from the LEVANT into the northern delta. Then the delta turns a different colour as their leaders take over. Text in frame: LEVANT → DELTA.`
- **AI motion prompt:** `Arrows trickle in; colour wipe. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

**Batch 5 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 6: The Hyksos and the fight back (Scenes 51–60, 08:20–10:00)

#### Scene 051 · 08:20–08:30 · C · Illustrated world

**VO:** "around 1650 BC, ruling from their capital, Avaris. Egyptians called them "rulers of foreign lands." We call them the Hyksos."

- **Visual:** A walled city in the delta, AVARIS, with a Hyksos ruler (Levantine dress, mushroom-shaped hair, beard) on the throne. Egyptian scribes whisper; a scroll reads "Rulers of Foreign Lands". The Guide is not in this shot.
- **On-screen text:** 1650 BC / AVARIS / THE HYKSOS
- **Camera / animation:** Zoom into the city; scroll unrolls
- **SFX / music:** whispers, gong
- **Pace:** 22 spoken words · ≈ 8.9 s at locked speed. Light line: keep the same speed; leave a ~1.1s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A walled city in the delta, AVARIS, with a Hyksos ruler (Levantine dress, mushroom-shaped hair, beard) on the throne. Egyptian scribes whisper; a scroll reads "Rulers of Foreign Lands". Text in frame: 1650 BC / AVARIS / THE HYKSOS.`
- **AI motion prompt:** `Zoom into the city; scroll unrolls. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 052 · 08:30–08:40 · B · Grey studio

**VO:** "They had horse-drawn chariots, powerful composite bows and better bronze weapons, which Egypt had barely used before. For the first time,"

- **Visual:** Weapons showcase cards on the grey background: HORSE CHARIOT, COMPOSITE BOW, BRONZE WEAPONS, each with a new glowing badge. An Egyptian soldier looks at them, confused. The Guide is not in this shot.
- **On-screen text:** CHARIOTS · COMPOSITE BOWS · BRONZE
- **Camera / animation:** Cards pop in one by one
- **SFX / music:** horse whinny, bow twang, metal clang
- **Pace:** 22 spoken words · ≈ 8.4 s at locked speed. Light line: keep the same speed; leave a ~1.6s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Weapons showcase cards on the grey background: HORSE CHARIOT, COMPOSITE BOW, BRONZE WEAPONS, each with a new glowing badge. An Egyptian soldier looks at them, confused. Text in frame: CHARIOTS · COMPOSITE BOWS · BRONZE.`
- **AI motion prompt:** `Cards pop in one by one. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 053 · 08:40–08:50 · A · Satellite map

**VO:** "foreigners ruled the land of the pharaohs, and the Egyptian kings in Thebes had to accept them. … Yet the Hyksos didn't try to erase Egypt."

- **Visual:** Map: the north coloured Hyksos, the south (THEBES) still Egyptian. The Theban king bows grudgingly. Then the Hyksos ruler holds up an Egyptian crown. The Guide is not in this shot.
- **On-screen text:** FOREIGNERS RULE EGYPT
- **Camera / animation:** Map split; slow push on the crown
- **SFX / music:** low brass, short pause
- **Pace:** 25 spoken words · ≈ 8.9 s at locked speed. Light line: keep the same speed; leave a ~1.1s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map: the north coloured Hyksos, the south (THEBES) still Egyptian. The Theban king bows grudgingly. Then the Hyksos ruler holds up an Egyptian crown. Text in frame: FOREIGNERS RULE EGYPT.`
- **AI motion prompt:** `Map split; slow push on the crown. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 054 · 08:50–09:00 · C · Illustrated world

**VO:** "They took pharaohs' titles, wrote their names in hieroglyphs, and worshipped Egyptian gods alongside their own. It's the first time we see a pattern that runs through this whole story:"

- **Visual:** The Hyksos king writes his name in a cartouche, puts on the double crown, and offers to Egyptian gods next to his own god. A pattern icon (loop arrow) appears with a sticky-note label. The Guide is not in this shot.
- **On-screen text:** THE PATTERN
- **Camera / animation:** Costume change in two steps; loop arrow spins
- **SFX / music:** magic poof, ding
- **Pace:** 30 spoken words · ≈ 10.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: The Hyksos king writes his name in a cartouche, puts on the double crown, and offers to Egyptian gods next to his own god. A pattern icon (loop arrow) appears with a sticky-note label. Text in frame: THE PATTERN.`
- **AI motion prompt:** `Costume change in two steps; loop arrow spins. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 055 · 09:00–09:10 · C · Illustrated world

**VO:** "foreign rulers turning themselves into Egyptian kings. … The kings of Thebes fought back. Seqenenre died in battle, and his mummy's skull still shows the axe and spear wounds."

- **Visual:** A foreign king transforms into a pharaoh (crown, beard, crook); the loop arrow stays on screen. Cut to a battle: Theban king Seqenenre falls. Inset: a cartoon skull with axe and spear marks. The Guide is not in this shot.
- **On-screen text:** FOREIGN RULERS → EGYPTIAN KINGS / SEQENENRE
- **Camera / animation:** Transformation morph; cut to battle
- **SFX / music:** battle cry, thud
- **Pace:** 28 spoken words · ≈ 10.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A foreign king transforms into a pharaoh (crown, beard, crook); the loop arrow stays on screen. Cut to a battle: Theban king Seqenenre falls. Inset: a cartoon skull with axe and spear marks. Text in frame: FOREIGN RULERS → EGYPTIAN KINGS / SEQENENRE.`
- **AI motion prompt:** `Transformation morph; cut to battle. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 056 · 09:10–09:20 · A · Satellite map

**VO:** "Thebes was squeezed from both sides, because the Hyksos were in contact with the kingdom of Kush to the south. The next Theban king, Kamose,"

- **Visual:** Map: Thebes in the middle, squeezed by the Hyksos from the north and KUSH from the south, red pincer arrows. A messenger runs on the desert route between them. Kamose appears. The Guide is not in this shot.
- **On-screen text:** SQUEEZED / KAMOSE
- **Camera / animation:** Pincer arrows close in
- **SFX / music:** tension drums
- **Pace:** 25 spoken words · ≈ 8.4 s at locked speed. Light line: keep the same speed; leave a ~1.6s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map: Thebes in the middle, squeezed by the Hyksos from the north and KUSH from the south, red pincer arrows. A messenger runs on the desert route between them. Kamose appears. Text in frame: SQUEEZED / KAMOSE.`
- **AI motion prompt:** `Pincer arrows close in. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 057 · 09:20–09:30 · C · Illustrated world

**VO:** "intercepted a Hyksos letter urging Kush to attack Thebes while his army was away. … The Thebans adopted the enemy's chariots and bows,"

- **Visual:** Kamose's soldiers catch the messenger and pull a letter from his bag; it unrolls in close-up with a target on Thebes. Then Egyptian soldiers practice with chariots and composite bows. The Guide is not in this shot.
- **On-screen text:** THE INTERCEPTED LETTER
- **Camera / animation:** Zoom on the letter
- **SFX / music:** rustle, horse trot
- **Pace:** 22 spoken words · ≈ 9.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Kamose's soldiers catch the messenger and pull a letter from his bag; it unrolls in close-up with a target on Thebes. Then Egyptian soldiers practice with chariots and composite bows. Text in frame: THE INTERCEPTED LETTER.`
- **AI motion prompt:** `Zoom on the letter. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 058 · 09:30–09:40 · A · Satellite map

**VO:** "and around 1550 BC, Ahmose captured Avaris, drove the Hyksos out, and chased them into Canaan. … Foreign rule changed Egypt."

- **Visual:** Map: Ahmose's army in chariots races north, captures Avaris (flag swap), and chases Hyksos arrows out into Canaan. Title card. The Guide is not in this shot.
- **On-screen text:** 1550 BC / AHMOSE
- **Camera / animation:** Sweeping arrows; map recolours
- **SFX / music:** chariots, victory horn
- **Pace:** 22 spoken words · ≈ 9.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map: Ahmose's army in chariots races north, captures Avaris (flag swap), and chases Hyksos arrows out into Canaan. Title card. Text in frame: 1550 BC / AHMOSE.`
- **AI motion prompt:** `Sweeping arrows; map recolours. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 059 · 09:40–09:50 · A · Satellite map

**VO:** "It now had a professional army, and it had learned that the deserts were no longer enough. From now on, it would push its borders outward and build an empire."

- **Visual:** Map: the desert walls crumble; then Egypt's border pushes outward with a growing red overlay into Nubia and the Levant. A professional army marches in step. The Guide is not in this shot.
- **On-screen text:** PROFESSIONAL ARMY / BUILD AN EMPIRE
- **Camera / animation:** Walls crumble then red expands
- **SFX / music:** march, rumble
- **Pace:** 30 spoken words · ≈ 10.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map: the desert walls crumble; then Egypt's border pushes outward with a growing red overlay into Nubia and the Levant. A professional army marches in step. Text in frame: PROFESSIONAL ARMY / BUILD AN EMPIRE.`
- **AI motion prompt:** `Walls crumble then red expands. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 060 · 09:50–10:00 · C · Illustrated world

**VO:** "Ahmose's victory began the New Kingdom, Egypt's richest era. Thebes became its religious heart, and its god Amun, merged with the sun god Ra,"

- **Visual:** Thebes skyline with temples; title card NEW KINGDOM. Amun (blue skin, two tall plumes) and Ra merge into AMUN-RA with a sun disc. The Guide is not in this shot.
- **On-screen text:** NEW KINGDOM / AMUN + RA
- **Camera / animation:** Merge morph
- **SFX / music:** fanfare, magical merge
- **Pace:** 24 spoken words · ≈ 9.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Thebes skyline with temples; title card NEW KINGDOM. Amun (blue skin, two tall plumes) and Ra merge into AMUN-RA with a sun disc. Text in frame: NEW KINGDOM / AMUN + RA.`
- **AI motion prompt:** `Merge morph. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

**Batch 6 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 7: The New Kingdom and Hatshepsut (Scenes 61–70, 10:00–11:40)

#### Scene 061 · 10:00–10:10 · C · Illustrated world

**VO:** "became king of the gods. As the empire grew, his temple at Karnak received a large share of the plunder, and his priests became enormously rich."

- **Visual:** Karnak temple gateway (tall pylon with flags). A line of carts loaded with gold rings, captured weapons and foreign tribute rolls in through the gates. Inside, bald priests in white linen sit on gold piles that grow taller with every cart. The Guide watches from the side, mouth open, hat tipping back.
- **On-screen text:** KARNAK / AMUN'S PRIESTS GET RICH
- **Camera / animation:** Slow pan through the gates; gold piles grow in 3 steps
- **SFX / music:** cart wheels, coins pouring
- **Pace:** 26 spoken words · ≈ 9.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Karnak temple gateway (tall pylon with flags). A line of carts loaded with gold rings, captured weapons and foreign tribute rolls in through the gates. Inside, bald priests in white linen sit on gold piles that grow taller with every cart. The Guide watches from the side, mouth open, hat tipping back. Include the Guide exactly as in the character reference. Text in frame: KARNAK / AMUN'S PRIESTS GET RICH.`
- **AI motion prompt:** `Slow pan through the gates; gold piles grow in 3 steps. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 062 · 10:10–10:20 · A · Satellite map

**VO:** "The new pharaohs went on the attack. Thutmose I led his army all the way to the Euphrates, in Syria, and deep into Nubia in the south."

- **Visual:** Satellite map. Thutmose I (stick king in the blue war crown) rides in a chariot icon. A red arrow shoots north-east all the way to the EUPHRATES in Syria, then another south deep into NUBIA. The red empire overlay spreads behind both arrows. The Guide stands bottom right, pointing up the map.
- **On-screen text:** THUTMOSE I / EUPHRATES · NUBIA
- **Camera / animation:** Arrows race out; red overlay spreads behind them
- **SFX / music:** war drums, chariot rumble
- **Pace:** 28 spoken words · ≈ 9.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map. Thutmose I (stick king in the blue war crown) rides in a chariot icon. A red arrow shoots north-east all the way to the EUPHRATES in Syria, then another south deep into NUBIA. The red empire overlay spreads behind both arrows. The Guide stands bottom right, pointing up the map. Include the Guide exactly as in the character reference. Text in frame: THUTMOSE I / EUPHRATES · NUBIA.`
- **AI motion prompt:** `Arrows race out; red overlay spreads behind them. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 063 · 10:20–10:30 · C · Illustrated world

**VO:** "Almost every pyramid had been robbed by now, so the new pharaohs hid their tombs instead, cutting them deep into a desert valley near Thebes: the Valley of the Kings."

- **Visual:** Night at a pyramid: a tomb robber with a sack and a torch sneaks out of a hole in the side. Robber icons pop onto a row of pyramids (almost all of them). Cut to a hot desert valley near Thebes with cliffs; tomb doorways are cut deep into the rock and quickly hidden with rubble. Big title on the cliff. The Guide is not in this shot.
- **On-screen text:** ROBBED / VALLEY OF THE KINGS
- **Camera / animation:** Robber sneaks (comic tiptoe); cut, slow push into a hidden doorway
- **SFX / music:** sneaky pizzicato, rock echo
- **Pace:** 30 spoken words · ≈ 10.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Night at a pyramid: a tomb robber with a sack and a torch sneaks out of a hole in the side. Robber icons pop onto a row of pyramids (almost all of them). Cut to a hot desert valley near Thebes with cliffs; tomb doorways are cut deep into the rock and quickly hidden with rubble. Big title on the cliff. Text in frame: ROBBED / VALLEY OF THE KINGS.`
- **AI motion prompt:** `Robber sneaks (comic tiptoe); cut, slow push into a hidden doorway. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 064 · 10:30–10:40 · C · Illustrated world

**VO:** "Around 1479 BC, the child Thutmose III became king, and his aunt and stepmother, Hatshepsut, ruled as regent. Within a few years,"

- **Visual:** Palace throne room at Thebes. A tiny child king, Thutmose III, sits on a giant throne with his feet dangling and a crown too big for him. Hatshepsut stands beside him in a queen's vulture crown, holding a scroll as REGENT. A calendar flips forward: "a few years later". The Guide is not in this shot.
- **On-screen text:** 1479 BC / THUTMOSE III (CHILD) / HATSHEPSUT, REGENT
- **Camera / animation:** Wide shot; calendar pages flip at the end
- **SFX / music:** soft harp, page flips
- **Pace:** 26 spoken words · ≈ 9.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Palace throne room at Thebes. A tiny child king, Thutmose III, sits on a giant throne with his feet dangling and a crown too big for him. Hatshepsut stands beside him in a queen's vulture crown, holding a scroll as REGENT. A calendar flips forward: "a few years later". Text in frame: 1479 BC / THUTMOSE III (CHILD) / HATSHEPSUT, REGENT.`
- **AI motion prompt:** `Wide shot; calendar pages flip at the end. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 065 · 10:40–10:50 · C · Illustrated world

**VO:** "she declared herself pharaoh, and her official images showed her with a king's headdress and the ceremonial false beard. … To justify her rule,"

- **Visual:** Hatshepsut steps up onto the throne in front of the boy. With a pop she now wears the striped nemes headdress and a ceremonial false beard on a strap. Courtiers gasp. The Guide strokes his own chin as if checking for a beard. Then cut to a blank temple wall.
- **On-screen text:** HATSHEPSUT, PHARAOH
- **Camera / animation:** Costume pop; gentle glow; cut to wall
- **SFX / music:** gasp, crown pop
- **Pace:** 23 spoken words · ≈ 9.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Hatshepsut steps up onto the throne in front of the boy. With a pop she now wears the striped nemes headdress and a ceremonial false beard on a strap. Courtiers gasp. The Guide strokes his own chin as if checking for a beard. Then cut to a blank temple wall. Include the Guide exactly as in the character reference. Text in frame: HATSHEPSUT, PHARAOH.`
- **AI motion prompt:** `Costume pop; gentle glow; cut to wall. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 066 · 10:50–11:00 · D · Artefact / relief close-up

**VO:** "she had her temple walls carved with scenes showing the god Amun as her real father. … She ruled for about 20 years, mostly through trade and building rather than war."

- **Visual:** Temple wall relief in the cartoon style: the god Amun (blue skin, tall plumes) holding a baby Hatshepsut, with a family-tree line: AMUN → HATSHEPSUT. Then a big 20 YEARS label; her trade ships replace a crossed-out chariot. The Guide is not in this shot.
- **On-screen text:** AMUN = "FATHER" / 20 YEARS: TRADE, NOT WAR
- **Camera / animation:** Slow pan across the relief; chariot crossed out with a red X
- **SFX / music:** chisel taps, sail flap
- **Pace:** 30 spoken words · ≈ 10.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: Temple wall relief in the cartoon style: the god Amun (blue skin, tall plumes) holding a baby Hatshepsut, with a family-tree line: AMUN → HATSHEPSUT. Then a big 20 YEARS label; her trade ships replace a crossed-out chariot. Text in frame: AMUN = "FATHER" / 20 YEARS: TRADE, NOT WAR.`
- **AI motion prompt:** `Slow pan across the relief; chariot crossed out with a red X. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 067 · 11:00–11:10 · A · Satellite map

**VO:** "Her expedition to Punt, on Africa's Red Sea coast, brought back incense, ebony and living myrrh trees, and her terraced temple at Deir el-Bahari still stands."

- **Visual:** Satellite map of the Red Sea. Five ships sail from Egypt down the Red Sea to PUNT on the African coast. On the way back they carry incense bags, black ebony logs and myrrh trees in pots. Cut to Deir el-Bahari: three wide terraces against tall golden cliffs, with the Guide waving at the bottom.
- **On-screen text:** PUNT / INCENSE · EBONY · MYRRH TREES / DEIR EL-BAHARI
- **Camera / animation:** Dotted route animates there and back; cut to the temple
- **SFX / music:** waves, seagulls, gentle harp
- **Pace:** 27 spoken words · ≈ 10.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map of the Red Sea. Five ships sail from Egypt down the Red Sea to PUNT on the African coast. On the way back they carry incense bags, black ebony logs and myrrh trees in pots. Cut to Deir el-Bahari: three wide terraces against tall golden cliffs, with the Guide waving at the bottom. Include the Guide exactly as in the character reference. Text in frame: PUNT / INCENSE · EBONY · MYRRH TREES / DEIR EL-BAHARI.`
- **AI motion prompt:** `Dotted route animates there and back; cut to the temple. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 068 · 11:10–11:20 · C · Illustrated world

**VO:** "She also raised giant granite obelisks at Karnak. … Years after her death, her statues were smashed and her name was chiselled off monuments,"

- **Visual:** At Karnak, two giant pink granite obelisks rise from the ground, gleaming. Then time-skip ("years later"): her statues lie smashed on the ground, and a worker chisels her name out of a cartouche on the wall. Dust puffs fly. The Guide is not in this shot.
- **On-screen text:** OBELISKS / ERASED
- **Camera / animation:** Obelisks rise; then the scene turns grey; chisel strikes on the beat
- **SFX / music:** stone rumble, hammer smashes
- **Pace:** 23 spoken words · ≈ 8.9 s at locked speed. Light line: keep the same speed; leave a ~1.1s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: At Karnak, two giant pink granite obelisks rise from the ground, gleaming. Then time-skip ("years later"): her statues lie smashed on the ground, and a worker chisels her name out of a cartouche on the wall. Dust puffs fly. Text in frame: OBELISKS / ERASED.`
- **AI motion prompt:** `Obelisks rise; then the scene turns grey; chisel strikes on the beat. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 069 · 11:20–11:30 · B · Grey studio

**VO:** "most likely on Thutmose III's orders. Later official king lists left her out entirely. … Once he ruled alone, Thutmose III became Egypt's greatest conqueror."

- **Visual:** Grey studio. A long scroll king list unrolls: the names jump from Thutmose II straight to Thutmose III with a blank gap. The Guide puts his ear near the gap, puzzled. Then an adult Thutmose III steps in wearing the blue war crown, holding a bow.
- **On-screen text:** LEFT OUT / THUTMOSE III: GREATEST CONQUEROR
- **Camera / animation:** Scroll unrolls; zoom on the gap; Thutmose slides in
- **SFX / music:** scroll unroll, war drum
- **Pace:** 26 spoken words · ≈ 10.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio. A long scroll king list unrolls: the names jump from Thutmose II straight to Thutmose III with a blank gap. The Guide puts his ear near the gap, puzzled. Then an adult Thutmose III steps in wearing the blue war crown, holding a bow. Include the Guide exactly as in the character reference. Text in frame: LEFT OUT / THUTMOSE III: GREATEST CONQUEROR.`
- **AI motion prompt:** `Scroll unrolls; zoom on the gap; Thutmose slides in. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 070 · 11:30–11:40 · A · Satellite map

**VO:** "Around 1457 BC, rebel kings gathered at Megiddo, in what is now northern Israel. Thutmose took the narrowest of three routes,"

- **Visual:** Satellite map of the Levant. Rebel king icons (with small crowns) gather at a fortress pin: MEGIDDO (northern Israel). Three dotted routes lead there across a mountain ridge; two wide ones and one narrow pass in the middle. The narrow one glows yellow as Thutmose chooses it. The Guide is not in this shot.
- **On-screen text:** 1457 BC / MEGIDDO / 3 ROUTES
- **Camera / animation:** Routes draw on one by one; the middle one highlights
- **SFX / music:** map pings, tension strings
- **Pace:** 24 spoken words · ≈ 9.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map of the Levant. Rebel king icons (with small crowns) gather at a fortress pin: MEGIDDO (northern Israel). Three dotted routes lead there across a mountain ridge; two wide ones and one narrow pass in the middle. The narrow one glows yellow as Thutmose chooses it. Text in frame: 1457 BC / MEGIDDO / 3 ROUTES.`
- **AI motion prompt:** `Routes draw on one by one; the middle one highlights. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

**Batch 7 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 8: Thutmose III and Akhenaten (Scenes 71–80, 11:40–13:20)

#### Scene 071 · 11:40–11:50 · C · Illustrated world

**VO:** "a pass so tight his army marched in single file, and caught them by surprise. After a seven-month siege, Megiddo fell."

- **Visual:** A tight mountain pass: Egyptian soldiers walk in single file, the Guide squeezing in among them. They burst out of the pass and the rebels jump in surprise. Then Megiddo's walls under siege; a counter: 1 → 7 MONTHS. The gates open with a white flag.
- **On-screen text:** SINGLE FILE / 7-MONTH SIEGE / MEGIDDO FALLS
- **Camera / animation:** Side-scroll along the pass; counter ticks; gates swing open
- **SFX / music:** marching feet, surprise sting, gate creak
- **Pace:** 22 spoken words · ≈ 7.7 s at locked speed. Light line: keep the same speed; leave a ~2.3s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A tight mountain pass: Egyptian soldiers walk in single file, the Guide squeezing in among them. They burst out of the pass and the rebels jump in surprise. Then Megiddo's walls under siege; a counter: 1 → 7 MONTHS. The gates open with a white flag. Include the Guide exactly as in the character reference. Text in frame: SINGLE FILE / 7-MONTH SIEGE / MEGIDDO FALLS.`
- **AI motion prompt:** `Side-scroll along the pass; counter ticks; gates swing open. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 072 · 11:50–12:00 · D · Artefact / relief close-up

**VO:** "We know these details because Thutmose had his campaigns carved on the walls of Karnak, listing battles, captured cities and tribute, much of it given to Amun's temple."

- **Visual:** A long carved wall at Karnak in the cartoon relief style: rows of captured city name-rings, chariots and lines of tribute bearers. The camera pans along it while the tribute (gold, horses, chariots) flows into Amun's temple. The Guide is not in this shot.
- **On-screen text:** THE ANNALS OF THUTMOSE III
- **Camera / animation:** Long horizontal pan along the wall
- **SFX / music:** chisel taps, crowd
- **Pace:** 28 spoken words · ≈ 10.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: A long carved wall at Karnak in the cartoon relief style: rows of captured city name-rings, chariots and lines of tribute bearers. The camera pans along it while the tribute (gold, horses, chariots) flows into Amun's temple. Text in frame: THE ANNALS OF THUTMOSE III.`
- **AI motion prompt:** `Long horizontal pan along the wall. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 073 · 12:00–12:10 · A · Satellite map

**VO:** "Over about 17 campaigns, he built the largest empire Egypt ever had, stretching from Syria to deep into Sudan, with Nubia's gold mines under Egyptian control."

- **Visual:** Satellite map: a counter ticks from 1 to 17 CAMPAIGNS, each tick adding red to the overlay, until it reaches from SYRIA down to SUDAN. Gold mine icons sparkle in NUBIA. The Guide holds a gold nugget up to the light.
- **On-screen text:** 17 CAMPAIGNS / SYRIA → SUDAN / NUBIAN GOLD
- **Camera / animation:** Red expands with each tick; sparkles on the mines
- **SFX / music:** counter clicks, gold sparkle
- **Pace:** 26 spoken words · ≈ 11.2 s at locked speed. Dense line: do NOT speed up. Let it run to ~11.2s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map: a counter ticks from 1 to 17 CAMPAIGNS, each tick adding red to the overlay, until it reaches from SYRIA down to SUDAN. Gold mine icons sparkle in NUBIA. The Guide holds a gold nugget up to the light. Include the Guide exactly as in the character reference. Text in frame: 17 CAMPAIGNS / SYRIA → SUDAN / NUBIAN GOLD.`
- **AI motion prompt:** `Red expands with each tick; sparkles on the mines. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 074 · 12:10–12:20 · C · Illustrated world

**VO:** "He also found a way to hold it. Sons of conquered rulers were brought to Egypt and raised at court. When they went home to rule, they had grown up Egyptian, and loyal."

- **Visual:** A boat arrives at the palace: young foreign princes step off in foreign clothes. A quick montage: they learn hieroglyphs, wear Egyptian linen, grow taller. Then they sail home, now dressed as Egyptians, and bow toward Egypt. The Guide is not in this shot.
- **On-screen text:** RAISED AT COURT / GROWN UP EGYPTIAN
- **Camera / animation:** Time-lapse growth; boat leaves
- **SFX / music:** school bell, sailing
- **Pace:** 33 spoken words · ≈ 10.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A boat arrives at the palace: young foreign princes step off in foreign clothes. A quick montage: they learn hieroglyphs, wear Egyptian linen, grow taller. Then they sail home, now dressed as Egyptians, and bow toward Egypt. Text in frame: RAISED AT COURT / GROWN UP EGYPTIAN.`
- **AI motion prompt:** `Time-lapse growth; boat leaves. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 075 · 12:20–12:30 · C · Illustrated world

**VO:** "By the reign of Amenhotep III, Egypt was a superpower, rich enough to spend almost four decades building rather than fighting."

- **Visual:** Amenhotep III, wide and smiling, on a gold throne. Behind him, temples and giant statues build up in a time-lapse. A balance with BUILDING heavy and FIGHTING light. A label reads ~40 YEARS. The Guide is not in this shot.
- **On-screen text:** AMENHOTEP III / SUPERPOWER
- **Camera / animation:** Time-lapse building; balance tips
- **SFX / music:** construction sounds, celebratory brass
- **Pace:** 22 spoken words · ≈ 8.9 s at locked speed. Light line: keep the same speed; leave a ~1.1s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Amenhotep III, wide and smiling, on a gold throne. Behind him, temples and giant statues build up in a time-lapse. A balance with BUILDING heavy and FIGHTING light. A label reads ~40 YEARS. Text in frame: AMENHOTEP III / SUPERPOWER.`
- **AI motion prompt:** `Time-lapse building; balance tips. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 076 · 12:30–12:40 · B · Grey studio

**VO:** "Clay tablets later found at Amarna preserve letters from the kings of Babylon and other great powers, writing to the pharaoh as equals and asking him for gold."

- **Visual:** Grey studio. Clay tablets with wedge-shaped writing pop in, each labelled: BABYLON, MITANNI, HITTITES. Speech bubbles come out of them: "My brother, send gold!" The pharaoh sits at the same height as the other kings, all equal. The Guide is not in this shot.
- **On-screen text:** AMARNA LETTERS / "SEND GOLD"
- **Camera / animation:** Tablets pop; bubbles bounce
- **SFX / music:** clay clinks, chuckle
- **Pace:** 28 spoken words · ≈ 10.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio. Clay tablets with wedge-shaped writing pop in, each labelled: BABYLON, MITANNI, HITTITES. Speech bubbles come out of them: "My brother, send gold!" The pharaoh sits at the same height as the other kings, all equal. Text in frame: AMARNA LETTERS / "SEND GOLD".`
- **AI motion prompt:** `Tablets pop; bubbles bounce. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 077 · 12:40–12:50 · C · Illustrated world

**VO:** "Then his son broke the system. Amenhotep IV pushed aside Egypt's many gods for one, the Aten, the disc of the sun, and renamed himself Akhenaten."

- **Visual:** Akhenaten (long face, tall blue crown) raises his arms to a single sun disc whose rays end in little hands. Behind him, the many gods (falcon, jackal, ram, cow) fade out one by one. A name tag swaps: AMENHOTEP IV → AKHENATEN. The Guide is not in this shot.
- **On-screen text:** THE ATEN / AKHENATEN
- **Camera / animation:** Gods fade in sequence; name swap animation
- **SFX / music:** choir rising, wind
- **Pace:** 27 spoken words · ≈ 10.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Akhenaten (long face, tall blue crown) raises his arms to a single sun disc whose rays end in little hands. Behind him, the many gods (falcon, jackal, ram, cow) fade out one by one. A name tag swaps: AMENHOTEP IV → AKHENATEN. Text in frame: THE ATEN / AKHENATEN.`
- **AI motion prompt:** `Gods fade in sequence; name swap animation. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 078 · 12:50–13:00 · C · Illustrated world

**VO:** "Many historians see this partly as a move against the rich and powerful priests of Amun. … He built a new capital, now called Amarna,"

- **Visual:** Rich priests of Amun sit on gold, frowning, as a shadow of the Aten falls over them. Then a desert plain: a brand-new city builds up in fast time-lapse, with straight streets and open-air temples. The Guide is not in this shot.
- **On-screen text:** AGAINST THE PRIESTS? / AMARNA
- **Camera / animation:** Shadow sweeps; time-lapse city
- **SFX / music:** ominous note, construction
- **Pace:** 24 spoken words · ≈ 9.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Rich priests of Amun sit on gold, frowning, as a shadow of the Aten falls over them. Then a desert plain: a brand-new city builds up in fast time-lapse, with straight streets and open-air temples. Text in frame: AGAINST THE PRIESTS? / AMARNA.`
- **AI motion prompt:** `Shadow sweeps; time-lapse city. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 079 · 13:00–13:10 · C · Illustrated world

**VO:** "closed the old temples, and had Amun's name hacked off monuments. Only the king and his queen, Nefertiti, were shown worshipping the Aten directly."

- **Visual:** Temple doors slam shut with a padlock. A worker hacks the name AMUN off a wall. Then: Akhenaten and Nefertiti alone under the sun's rays, while everyone else bows to them (arrows show the rays reaching people only through the royal couple). The Guide is not in this shot.
- **On-screen text:** TEMPLES CLOSED / ONLY THE KING & QUEEN
- **Camera / animation:** Door slam; chisel; diagram arrows draw
- **SFX / music:** door slam, chisel, choir
- **Pace:** 24 spoken words · ≈ 9.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Temple doors slam shut with a padlock. A worker hacks the name AMUN off a wall. Then: Akhenaten and Nefertiti alone under the sun's rays, while everyone else bows to them (arrows show the rays reaching people only through the royal couple). Text in frame: TEMPLES CLOSED / ONLY THE KING & QUEEN.`
- **AI motion prompt:** `Door slam; chisel; diagram arrows draw. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 080 · 13:10–13:20 · D · Artefact / relief close-up

**VO:** "Everyone else was meant to worship through them. … Art changed too. The royal family was shown with long faces and rounded bodies,"

- **Visual:** A row of stiff, straight royal portraits (old style) on the left; on the right, Amarna-style art: a royal family with long faces and rounded bodies, kissing and playing with their daughters. The Guide looks from one side to the other.
- **On-screen text:** ART CHANGED TOO
- **Camera / animation:** Split-screen wipe from old to new
- **SFX / music:** harp, curious "hmm" note
- **Pace:** 22 spoken words · ≈ 7.7 s at locked speed. Light line: keep the same speed; leave a ~2.3s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: A row of stiff, straight royal portraits (old style) on the left; on the right, Amarna-style art: a royal family with long faces and rounded bodies, kissing and playing with their daughters. The Guide looks from one side to the other. Include the Guide exactly as in the character reference. Text in frame: ART CHANGED TOO.`
- **AI motion prompt:** `Split-screen wipe from old to new. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

**Batch 8 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 9: Tutankhamun (Scenes 81–90, 13:20–15:00)

#### Scene 081 · 13:20–13:30 · A · Satellite map

**VO:** "in relaxed family scenes, a sharp break from 1,500 years of stiff, idealised royal images. … Meanwhile, the empire drifted."

- **Visual:** The relaxed family scene is still in the corner while the satellite map behind it shows the empire's red edges flickering and fading. A timeline bar shows 1,500 YEARS of stiff art versus the brief Amarna break. The Guide is not in this shot.
- **On-screen text:** 1,500 YEARS / THE EMPIRE DRIFTED
- **Camera / animation:** Red edges flicker and fade
- **SFX / music:** wind, worried strings
- **Pace:** 22 spoken words · ≈ 9.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: The relaxed family scene is still in the corner while the satellite map behind it shows the empire's red edges flickering and fading. A timeline bar shows 1,500 YEARS of stiff art versus the brief Amarna break. Text in frame: 1,500 YEARS / THE EMPIRE DRIFTED.`
- **AI motion prompt:** `Red edges flicker and fade. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 082 · 13:30–13:40 · B · Grey studio

**VO:** "Among the Amarna letters are pleas from Egypt's vassal rulers in Canaan, begging the pharaoh for troops against their enemies. Some seem to have gone unanswered."

- **Visual:** Grey studio. Clay tablet letters fly in from CANAAN: "Send troops!", "Help!", "Hurry!" They pile up on an empty desk. The Guide taps a sleeping messenger. Some letters gather cobwebs.
- **On-screen text:** PLEAS FROM CANAAN / UNANSWERED
- **Camera / animation:** Letters pile up; cobweb draws on
- **SFX / music:** thuds of tablets, snore
- **Pace:** 26 spoken words · ≈ 10.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio. Clay tablet letters fly in from CANAAN: "Send troops!", "Help!", "Hurry!" They pile up on an empty desk. The Guide taps a sleeping messenger. Some letters gather cobwebs. Include the Guide exactly as in the character reference. Text in frame: PLEAS FROM CANAAN / UNANSWERED.`
- **AI motion prompt:** `Letters pile up; cobweb draws on. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 083 · 13:40–13:50 · C · Illustrated world

**VO:** "His revolution didn't survive him. After his death, Amarna was abandoned, and Egypt went back to its old gods. … The boy who soon took the throne, Tutankhaten, was about nine."

- **Visual:** Amarna empty: sand blows through the abandoned streets. Temples to the old gods reopen; the gods' statues return. Then a small 9-year-old boy king, Tutankhaten, sits on the throne, nervous. The Guide is not in this shot.
- **On-screen text:** AMARNA ABANDONED / TUTANKHATEN, AGE 9
- **Camera / animation:** Sand wind; doors reopen; push in on the boy
- **SFX / music:** desert wind, doors creak open, soft harp
- **Pace:** 30 spoken words · ≈ 11.2 s at locked speed. Dense line: do NOT speed up. Let it run to ~11.2s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Amarna empty: sand blows through the abandoned streets. Temples to the old gods reopen; the gods' statues return. Then a small 9-year-old boy king, Tutankhaten, sits on the throne, nervous. Text in frame: AMARNA ABANDONED / TUTANKHATEN, AGE 9.`
- **AI motion prompt:** `Sand wind; doors reopen; push in on the boy. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 084 · 13:50–14:00 · C · Illustrated world

**VO:** "His advisers reopened the old temples and changed his name to honour Amun: Tutankhamun. He died at around 19, and the exact cause is still debated."

- **Visual:** Advisers (one old vizier, one general) change the boy's name tag: TUTANKH-ATEN → TUTANKH-AMUN. A quick growth time-lapse to about 19; then a soft fade with a question mark: cause of death? The Guide is not in this shot.
- **On-screen text:** TUTANKHAMUN / DIED ~19 / CAUSE?
- **Camera / animation:** Name swap; age counter 9 → 19; fade
- **SFX / music:** tick sound, single soft note
- **Pace:** 26 spoken words · ≈ 10.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Advisers (one old vizier, one general) change the boy's name tag: TUTANKH-ATEN → TUTANKH-AMUN. A quick growth time-lapse to about 19; then a soft fade with a question mark: cause of death? Text in frame: TUTANKHAMUN / DIED ~19 / CAUSE?.`
- **AI motion prompt:** `Name swap; age counter 9 → 19; fade. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 085 · 14:00–14:10 · C · Illustrated world

**VO:** "A few years later, the army commander Horemheb became pharaoh. He tore down Akhenaten's temples, reused their blocks, and wiped the Amarna kings,"

- **Visual:** General Horemheb (armour, blue war crown) stands on the throne. Behind him, workers knock down Akhenaten's temples and carry the blocks away to reuse them. Then a king-list scroll appears. The Guide is not in this shot.
- **On-screen text:** HOREMHEB
- **Camera / animation:** Demolition with dust clouds
- **SFX / music:** crashes, dust
- **Pace:** 23 spoken words · ≈ 9.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: General Horemheb (armour, blue war crown) stands on the throne. Behind him, workers knock down Akhenaten's temples and carry the blocks away to reuse them. Then a king-list scroll appears. Text in frame: HOREMHEB.`
- **AI motion prompt:** `Demolition with dust clouds. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 086 · 14:10–14:20 · B · Grey studio

**VO:** "Tutankhamun included, from the official record. … That's partly why Tutankhamun was forgotten. He had been buried in a small, hastily prepared tomb,"

- **Visual:** The king-list scroll: AKHENATEN, SMENKHKARE, TUTANKHAMUN, AY fade out one by one. The Guide shrugs. Then a small, plain tomb in the Valley of the Kings, with a few hastily packed items.
- **On-screen text:** ERASED / FORGOTTEN / A SMALL, HASTY TOMB
- **Camera / animation:** Names fade; cut to the tomb
- **SFX / music:** eraser squeaks, wind
- **Pace:** 22 spoken words · ≈ 10.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: The king-list scroll: AKHENATEN, SMENKHKARE, TUTANKHAMUN, AY fade out one by one. The Guide shrugs. Then a small, plain tomb in the Valley of the Kings, with a few hastily packed items. Include the Guide exactly as in the character reference. Text in frame: ERASED / FORGOTTEN / A SMALL, HASTY TOMB.`
- **AI motion prompt:** `Names fade; cut to the tomb. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 087 · 14:20–14:30 · C · Illustrated world

**VO:** "and later, workers digging a nearby tomb piled their debris over its entrance. Unlike almost every other royal tomb, it was never emptied by robbers."

- **Visual:** Workers digging a nearby tomb dump rubble over the small tomb's doorway until it is invisible. Time-lapse: tomb robbers walk past again and again, never noticing. The Guide is not in this shot.
- **On-screen text:** HIDDEN BY DEBRIS / NEVER ROBBED
- **Camera / animation:** Rubble piles up; time-lapse day/night
- **SFX / music:** rubble, footsteps
- **Pace:** 25 spoken words · ≈ 10.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Workers digging a nearby tomb dump rubble over the small tomb's doorway until it is invisible. Time-lapse: tomb robbers walk past again and again, never noticing. Text in frame: HIDDEN BY DEBRIS / NEVER ROBBED.`
- **AI motion prompt:** `Rubble piles up; time-lapse day/night. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 088 · 14:30–14:40 · D · Artefact / relief close-up

**VO:** "In November 1922, British archaeologist Howard Carter uncovered its steps and sealed doorway. When his sponsor,"

- **Visual:** November 1922. Howard Carter (moustache, hat, lamp) and workers uncover the first stone step, then more steps, down to a doorway sealed with plaster and seals. The Guide is not in this shot.
- **On-screen text:** NOVEMBER 1922 / HOWARD CARTER
- **Camera / animation:** Tilt down the steps
- **SFX / music:** shovel scrapes, excited whisper
- **Pace:** 18 spoken words · ≈ 8.7 s at locked speed. Light line: keep the same speed; leave a ~1.3s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: November 1922. Howard Carter (moustache, hat, lamp) and workers uncover the first stone step, then more steps, down to a doorway sealed with plaster and seals. Text in frame: NOVEMBER 1922 / HOWARD CARTER.`
- **AI motion prompt:** `Tilt down the steps. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 089 · 14:40–14:50 · C · Illustrated world

**VO:** "Lord Carnarvon, asked if he could see anything inside, Carter answered: "Yes, wonderful things." … Inside were more than 5,000 objects."

- **Visual:** Lord Carnarvon behind Carter, asking. Carter peeks through a hole with a candle; gold glints in the dark. Big quote text. Then a counter rolls to 5,000+ OBJECTS. The Guide is not in this shot.
- **On-screen text:** "YES, WONDERFUL THINGS." / 5,000+ OBJECTS
- **Camera / animation:** Candle glow; gold glint; counter
- **SFX / music:** gasp, sparkle, counter
- **Pace:** 21 spoken words · ≈ 8.7 s at locked speed. Light line: keep the same speed; leave a ~1.3s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Lord Carnarvon behind Carter, asking. Carter peeks through a hole with a candle; gold glints in the dark. Big quote text. Then a counter rolls to 5,000+ OBJECTS. Text in frame: "YES, WONDERFUL THINGS." / 5,000+ OBJECTS.`
- **AI motion prompt:** `Candle glow; gold glint; counter. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 090 · 14:50–15:00 · C · Illustrated world

**VO:** "The king lay in three nested coffins, the innermost made of solid gold, about 110 kilograms, with the famous gold mask over his face."

- **Visual:** Three coffins slide apart like nesting dolls: wooden, then gilded, then solid gold. A scale shows 110 KG. The gold mask appears and glows. The Guide shields his eyes.
- **On-screen text:** 3 COFFINS / SOLID GOLD: 110 KG / THE GOLD MASK
- **Camera / animation:** Coffins slide apart one by one
- **SFX / music:** heavy slide, shimmer
- **Pace:** 27 spoken words · ≈ 9.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Three coffins slide apart like nesting dolls: wooden, then gilded, then solid gold. A scale shows 110 KG. The gold mask appears and glows. The Guide shields his eyes. Include the Guide exactly as in the character reference. Text in frame: 3 COFFINS / SOLID GOLD: 110 KG / THE GOLD MASK.`
- **AI motion prompt:** `Coffins slide apart one by one. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

**Batch 9 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 10: Ramesses II (Scenes 91–100, 15:00–16:40)

#### Scene 091 · 15:00–15:10 · B · Grey studio

**VO:** "And this was the burial of a minor king, which tells you how much was lost from the others. … The discovery made Tutankhamun the most famous pharaoh in the world."

- **Visual:** A small king icon labelled MINOR KING next to giant empty tombs of great kings (cobwebs). The Guide spreads his arms wide. Then a world map lights up with the gold mask in the middle.
- **On-screen text:** A MINOR KING / MOST FAMOUS PHARAOH IN THE WORLD
- **Camera / animation:** Scale comparison; world map glows
- **SFX / music:** ding, crowd murmur
- **Pace:** 30 spoken words · ≈ 10.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: A small king icon labelled MINOR KING next to giant empty tombs of great kings (cobwebs). The Guide spreads his arms wide. Then a world map lights up with the gold mask in the middle. Include the Guide exactly as in the character reference. Text in frame: A MINOR KING / MOST FAMOUS PHARAOH IN THE WORLD.`
- **AI motion prompt:** `Scale comparison; world map glows. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 092 · 15:10–15:20 · C · Illustrated world

**VO:** "It came in the same year Egypt won formal independence from Britain, and Egyptians embraced the boy king as a symbol of their nation."

- **Visual:** Cairo, 1922, sunny sky with cartoon clouds: a cheering Egyptian crowd waves green flags and banners printed with Tutankhamun's gold mask. A British flag lowers on a pole on the left while an Egyptian flag rises on the right. The Guide stands in the crowd waving his hat.
- **On-screen text:** 1922 / INDEPENDENCE FROM BRITAIN / SYMBOL OF THE NATION
- **Camera / animation:** Flags swap on the pole; slow push-in on the gold-mask banners
- **SFX / music:** cheering crowd, flag flutter
- **Pace:** 24 spoken words · ≈ 8.9 s at locked speed. Light line: keep the same speed; leave a ~1.1s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Cairo, 1922, sunny sky with cartoon clouds: a cheering Egyptian crowd waves green flags and banners printed with Tutankhamun's gold mask. A British flag lowers on a pole on the left while an Egyptian flag rises on the right. The Guide stands in the crowd waving his hat. Include the Guide exactly as in the character reference. Text in frame: 1922 / INDEPENDENCE FROM BRITAIN / SYMBOL OF THE NATION.`
- **AI motion prompt:** `Flags swap on the pole; slow push-in on the gold-mask banners. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 093 · 15:20–15:30 · C · Illustrated world

**VO:** "The treasures stayed in Egypt. … Horemheb had no heir, so he passed the throne to another general, Ramesses I. His family, the Ramessides,"

- **Visual:** A museum hall in Egypt: the gold mask behind glass, an EGYPT stamp on the case, the Guide nodding proudly. Hard cut back to the ancient palace: an old Horemheb, with no children beside him, hands the crown to a grey-haired general, Ramesses I.
- **On-screen text:** THE TREASURES STAYED IN EGYPT / NO HEIR → RAMESSES I
- **Camera / animation:** Museum pan, then hard cut with a whoosh to the handover
- **SFX / music:** museum hush, whoosh, short fanfare
- **Pace:** 24 spoken words · ≈ 10.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A museum hall in Egypt: the gold mask behind glass, an EGYPT stamp on the case, the Guide nodding proudly. Hard cut back to the ancient palace: an old Horemheb, with no children beside him, hands the crown to a grey-haired general, Ramesses I. Include the Guide exactly as in the character reference. Text in frame: THE TREASURES STAYED IN EGYPT / NO HEIR → RAMESSES I.`
- **AI motion prompt:** `Museum pan, then hard cut with a whoosh to the handover. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 094 · 15:30–15:40 · C · Illustrated world

**VO:** "were soldiers from the delta, and they set out to rebuild Egypt's empire. … The most famous was Ramesses II, who reigned for 66 years."

- **Visual:** A family of soldier-kings (the Ramessides) marches out of the green delta under falcon banners. A red empire arrow begins to draw on a small map card. Ramesses II steps to the front: tall, proud, double crown. A counter rolls to 66 YEARS. The Guide is not in this shot.
- **On-screen text:** THE RAMESSIDES / RAMESSES II / 66 YEARS
- **Camera / animation:** Marching side-scroll; counter ticks up
- **SFX / music:** marching feet, drum roll
- **Pace:** 26 spoken words · ≈ 9.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A family of soldier-kings (the Ramessides) marches out of the green delta under falcon banners. A red empire arrow begins to draw on a small map card. Ramesses II steps to the front: tall, proud, double crown. A counter rolls to 66 YEARS. Text in frame: THE RAMESSIDES / RAMESSES II / 66 YEARS.`
- **AI motion prompt:** `Marching side-scroll; counter ticks up. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 095 · 15:40–15:50 · A · Satellite map

**VO:** "He built a new capital, Pi-Ramesses, in the eastern delta, closer to the frontier in Asia, and filled Egypt with temples and giant statues of himself,"

- **Visual:** Satellite map: a new capital pin PI-RAMESSES appears in the eastern delta, with a dotted line to the Asian frontier (Sinai). Then temple and giant-statue icons pop up all along the Nile, each one with Ramesses' face. The Guide at bottom right counts them on his fingers and gives up.
- **On-screen text:** PI-RAMESSES / CLOSER TO ASIA
- **Camera / animation:** Pins pop along the river in a fast cascade
- **SFX / music:** stone thuds, cascading pops
- **Pace:** 27 spoken words · ≈ 10.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map: a new capital pin PI-RAMESSES appears in the eastern delta, with a dotted line to the Asian frontier (Sinai). Then temple and giant-statue icons pop up all along the Nile, each one with Ramesses' face. The Guide at bottom right counts them on his fingers and gives up. Include the Guide exactly as in the character reference. Text in frame: PI-RAMESSES / CLOSER TO ASIA.`
- **AI motion prompt:** `Pins pop along the river in a fast cascade. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 096 · 15:50–16:00 · C · Illustrated world

**VO:** "including the four colossal figures at Abu Simbel. Later Egyptians remembered him as the greatest king of all, and nine later pharaohs took his name."

- **Visual:** Abu Simbel at sunrise: four colossal seated statues of Ramesses carved into a sandstone cliff. The Guide stands at the foot of one statue, smaller than its toe. Then nine name tags pop in a row in yellow: RAMESSES III … RAMESSES XI.
- **On-screen text:** ABU SIMBEL / "THE GREATEST KING" / 9 LATER RAMESSES
- **Camera / animation:** Slow tilt up the statues; the name tags pop on the beat
- **SFX / music:** sunrise strings, 9 quick pops
- **Pace:** 25 spoken words · ≈ 10.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Abu Simbel at sunrise: four colossal seated statues of Ramesses carved into a sandstone cliff. The Guide stands at the foot of one statue, smaller than its toe. Then nine name tags pop in a row in yellow: RAMESSES III … RAMESSES XI. Include the Guide exactly as in the character reference. Text in frame: ABU SIMBEL / "THE GREATEST KING" / 9 LATER RAMESSES.`
- **AI motion prompt:** `Slow tilt up the statues; the name tags pop on the beat. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 097 · 16:00–16:10 · A · Satellite map

**VO:** "In 1274 BC, he fought the Hittite empire for control of Syria at Kadesh, in one of the largest chariot battles in history."

- **Visual:** Satellite map: Egypt in red, the Hittite Empire (Anatolia) in purple. Two thick arrows meet at a pin: KADESH in Syria. Dozens of tiny chariot icons fill the space around the pin. The Guide is not in this shot.
- **On-screen text:** 1274 BC / KADESH / EGYPT vs HITTITES
- **Camera / animation:** Arrows grow toward each other and collide
- **SFX / music:** war horns, chariot thunder
- **Pace:** 26 spoken words · ≈ 9.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map: Egypt in red, the Hittite Empire (Anatolia) in purple. Two thick arrows meet at a pin: KADESH in Syria. Dozens of tiny chariot icons fill the space around the pin. Text in frame: 1274 BC / KADESH / EGYPT vs HITTITES.`
- **AI motion prompt:** `Arrows grow toward each other and collide. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 098 · 16:10–16:20 · C · Illustrated world

**VO:** "Ramesses was caught in an ambush and had to fight his way out. The battle ended without a clear winner, though Ramesses advertised it at home as a great victory."

- **Visual:** Battlefield: Hittite chariots burst out from behind a hill and surround Ramesses' camp; Ramesses in his chariot fires arrows and breaks out. A scoreboard card reads EGYPT 1 – HITTITES 1. Cut to Egypt: a giant temple banner GREAT VICTORY! The Guide rolls his eyes at the camera.
- **On-screen text:** AMBUSH / NO CLEAR WINNER / "GREAT VICTORY!"
- **Camera / animation:** Shaky action camera; banner unrolls; comic freeze on the Guide
- **SFX / music:** clashes, horn, comic ding
- **Pace:** 30 spoken words · ≈ 10.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Battlefield: Hittite chariots burst out from behind a hill and surround Ramesses' camp; Ramesses in his chariot fires arrows and breaks out. A scoreboard card reads EGYPT 1 – HITTITES 1. Cut to Egypt: a giant temple banner GREAT VICTORY! The Guide rolls his eyes at the camera. Include the Guide exactly as in the character reference. Text in frame: AMBUSH / NO CLEAR WINNER / "GREAT VICTORY!".`
- **AI motion prompt:** `Shaky action camera; banner unrolls; comic freeze on the Guide. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 099 · 16:20–16:30 · D · Artefact / relief close-up

**VO:** "About 15 years later, the two empires signed one of the earliest peace treaties whose text survives, promising to help each other against attackers."

- **Visual:** A clay tablet treaty with two royal seals, one Egyptian, one Hittite. Above it, two hands (one with an Egyptian bracelet, one with a Hittite cuff) shake. Small shield icons appear on both sides: help each other against attackers. The Guide is not in this shot.
- **On-screen text:** ~15 YEARS LATER / ONE OF THE EARLIEST SURVIVING PEACE TREATIES
- **Camera / animation:** Slow zoom on the tablet; handshake pops in
- **SFX / music:** clay stamp, warm strings
- **Pace:** 24 spoken words · ≈ 9.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: A clay tablet treaty with two royal seals, one Egyptian, one Hittite. Above it, two hands (one with an Egyptian bracelet, one with a Hittite cuff) shake. Small shield icons appear on both sides: help each other against attackers. Text in frame: ~15 YEARS LATER / ONE OF THE EARLIEST SURVIVING PEACE TREATIES.`
- **AI motion prompt:** `Slow zoom on the tablet; handshake pops in. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 100 · 16:30–16:40 · C · Illustrated world

**VO:** "Ramesses later married a Hittite princess to seal the peace. … Around 1200 BC, the Bronze Age world collapsed."

- **Visual:** A royal wedding in the palace: Ramesses and a Hittite princess under a canopy, flower petals falling. Then the sky behind turns dark red and storm clouds roll in; a cracked bronze shield drops into frame. The Guide is not in this shot.
- **On-screen text:** 1200 BC / THE BRONZE AGE COLLAPSE
- **Camera / animation:** Petals, then a colour shift to dark red
- **SFX / music:** wedding harp, then thunder
- **Pace:** 20 spoken words · ≈ 7.4 s at locked speed. Light line: keep the same speed; leave a ~2.6s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A royal wedding in the palace: Ramesses and a Hittite princess under a canopy, flower petals falling. Then the sky behind turns dark red and storm clouds roll in; a cracked bronze shield drops into frame. Text in frame: 1200 BC / THE BRONZE AGE COLLAPSE.`
- **AI motion prompt:** `Petals, then a colour shift to dark red. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

**Batch 10 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 11: Bronze Age collapse and outsiders (Scenes 101–110, 16:40–18:20)

#### Scene 101 · 16:40–16:50 · A · Satellite map

**VO:** "The Hittite empire fell, and cities across the eastern Mediterranean were destroyed. Under Ramesses III, Egypt beat back invaders it called the Sea Peoples,"

- **Visual:** Satellite map of the eastern Mediterranean: fire icons light up on cities one after another; the purple Hittite area fades away. A fleet of Sea Peoples' ships (bird-head prows) sails toward the Nile delta; Ramesses III's fleet blocks them and they turn back. The Guide is not in this shot.
- **On-screen text:** HITTITES FALL / SEA PEOPLES / RAMESSES III
- **Camera / animation:** Fires cascade; naval clash at the delta mouth
- **SFX / music:** fire crackle, waves, battle
- **Pace:** 25 spoken words · ≈ 10.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map of the eastern Mediterranean: fire icons light up on cities one after another; the purple Hittite area fades away. A fleet of Sea Peoples' ships (bird-head prows) sails toward the Nile delta; Ramesses III's fleet blocks them and they turn back. Text in frame: HITTITES FALL / SEA PEOPLES / RAMESSES III.`
- **AI motion prompt:** `Fires cascade; naval clash at the delta mouth. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 102 · 16:50–17:00 · A · Satellite map

**VO:** "but war, failing trade and poor harvests drained it. Egypt soon lost its lands in Canaan and Syria. … The state began to fail at home. Around 1157 BC,"

- **Visual:** Egypt survives but looks tired: the red empire overlay drains back from CANAAN and SYRIA. Icons of a broken sword, a closed trade ship and a dry wheat sheaf hover over Egypt. The Guide's shoulders drop.
- **On-screen text:** WAR · FAILING TRADE · POOR HARVESTS / EMPIRE LOST
- **Camera / animation:** Red drains back; icons float
- **SFX / music:** drain sound, slow drum
- **Pace:** 31 spoken words · ≈ 10.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Egypt survives but looks tired: the red empire overlay drains back from CANAAN and SYRIA. Icons of a broken sword, a closed trade ship and a dry wheat sheaf hover over Egypt. The Guide's shoulders drop. Include the Guide exactly as in the character reference. Text in frame: WAR · FAILING TRADE · POOR HARVESTS / EMPIRE LOST.`
- **AI motion prompt:** `Red drains back; icons float. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 103 · 17:00–17:10 · C · Illustrated world

**VO:** "royal tomb builders went unpaid and staged the first recorded strike in history. Within decades, officials were putting gangs on trial for robbing the royal tombs in the Valley of the Kings."

- **Visual:** Royal tomb builders at Deir el-Medina sit on the ground with arms crossed and tools down, holding empty bowls; a sign reads NO GRAIN, NO WORK. Cut to a courtroom: officials on a bench try a gang of tomb robbers; a scribe writes the record. The Guide is not in this shot.
- **On-screen text:** 1157 BC / THE FIRST RECORDED STRIKE / TOMB ROBBERS ON TRIAL
- **Camera / animation:** Hard cut between the two scenes
- **SFX / music:** crowd chant, gavel knock
- **Pace:** 32 spoken words · ≈ 11.7 s at locked speed. Dense line: do NOT speed up. Let it run to ~11.7s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Royal tomb builders at Deir el-Medina sit on the ground with arms crossed and tools down, holding empty bowls; a sign reads NO GRAIN, NO WORK. Cut to a courtroom: officials on a bench try a gang of tomb robbers; a scribe writes the record. Text in frame: 1157 BC / THE FIRST RECORDED STRIKE / TOMB ROBBERS ON TRIAL.`
- **AI motion prompt:** `Hard cut between the two scenes. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 104 · 17:10–17:20 · C · Illustrated world

**VO:** "To save what was left, priests gathered the mummies of great pharaohs and hid them together in secret caches. That's why we can still see the faces of kings like Ramesses II today."

- **Visual:** Night, torchlight: priests carry wrapped royal mummies in a line into a hidden cave in the cliffs and seal it. Cut to the present day: the Guide stands in a museum, face to face with the mummy of Ramesses II behind glass.
- **On-screen text:** SECRET CACHES / RAMESSES II, TODAY
- **Camera / animation:** Torchlight flicker; match cut to the museum glass
- **SFX / music:** echoing footsteps, quiet museum hum
- **Pace:** 34 spoken words · ≈ 11.7 s at locked speed. Dense line: do NOT speed up. Let it run to ~11.7s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Night, torchlight: priests carry wrapped royal mummies in a line into a hidden cave in the cliffs and seal it. Cut to the present day: the Guide stands in a museum, face to face with the mummy of Ramesses II behind glass. Include the Guide exactly as in the character reference. Text in frame: SECRET CACHES / RAMESSES II, TODAY.`
- **AI motion prompt:** `Torchlight flicker; match cut to the museum glass. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 105 · 17:20–17:30 · A · Satellite map

**VO:** "By about 1070 BC, the New Kingdom was over. The high priests of Amun ruled the south from Thebes, while separate kings ruled the delta."

- **Visual:** Satellite map: Egypt splits along a line. THEBES (south) gets a priest icon with Amun's plumes; the DELTA (north) gets a separate king icon. A title card in yellow comic text drops in. The Guide is not in this shot.
- **On-screen text:** 1070 BC / THE NEW KINGDOM IS OVER
- **Camera / animation:** Map cracks into two halves; title slams
- **SFX / music:** low drone, crack
- **Pace:** 27 spoken words · ≈ 9.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map: Egypt splits along a line. THEBES (south) gets a priest icon with Amun's plumes; the DELTA (north) gets a separate king icon. A title card in yellow comic text drops in. Text in frame: 1070 BC / THE NEW KINGDOM IS OVER.`
- **AI motion prompt:** `Map cracks into two halves; title slams. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 106 · 17:30–17:40 · A · Satellite map

**VO:** "Power slipped to outsiders. Families of Libyan descent, settled in Egypt for generations, took the throne. Then kings from Kush, in today's Sudan, marched north."

- **Visual:** Map: a throne icon in the delta changes hands to a king of Libyan descent (feather in his hair). Then a long arrow marches north from KUSH (today's Sudan) along the Nile. The Guide is not in this shot.
- **On-screen text:** LIBYAN KINGS / KUSH MARCHES NORTH
- **Camera / animation:** Icon swap; arrow draws north
- **SFX / music:** drums, marching
- **Pace:** 25 spoken words · ≈ 10.2 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map: a throne icon in the delta changes hands to a king of Libyan descent (feather in his hair). Then a long arrow marches north from KUSH (today's Sudan) along the Nile. Text in frame: LIBYAN KINGS / KUSH MARCHES NORTH.`
- **AI motion prompt:** `Icon swap; arrow draws north. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 107 · 17:40–17:50 · C · Illustrated world

**VO:** "Around 727 BC, King Piye conquered Egypt, and his family ruled as pharaohs for more than half a century,"

- **Visual:** King Piye (Kushite, dark skin, cap crown with two cobras) enters Memphis on a chariot, crowds bowing. His family line appears on the throne one after another; a timeline bar fills: 50+ YEARS. The Guide is not in this shot.
- **On-screen text:** 727 BC / KING PIYE / 50+ YEARS
- **Camera / animation:** Push in on Piye; family icons slide in
- **SFX / music:** fanfare, crowd
- **Pace:** 24 spoken words · ≈ 9.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: King Piye (Kushite, dark skin, cap crown with two cobras) enters Memphis on a chariot, crowds bowing. His family line appears on the throne one after another; a timeline bar fills: 50+ YEARS. Text in frame: 727 BC / KING PIYE / 50+ YEARS.`
- **AI motion prompt:** `Push in on Piye; family icons slide in. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 108 · 17:50–18:00 · A · Satellite map

**VO:** "restoring old temples and traditions. … Next came the Assyrian empire. In 671 BC, its army took Memphis,"

- **Visual:** First, Kushite kings repair an old temple (scaffold, fresh paint). Then the satellite map: a huge Assyrian arrow (from Iraq) sweeps down and hits MEMPHIS with a fire icon. The Guide is not in this shot.
- **On-screen text:** RESTORING TRADITIONS / ASSYRIA / 671 BC: MEMPHIS
- **Camera / animation:** Temple fix-up; then arrow strikes
- **SFX / music:** hammer taps, war cry
- **Pace:** 22 spoken words · ≈ 8.7 s at locked speed. Light line: keep the same speed; leave a ~1.3s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: First, Kushite kings repair an old temple (scaffold, fresh paint). Then the satellite map: a huge Assyrian arrow (from Iraq) sweeps down and hits MEMPHIS with a fire icon. Text in frame: RESTORING TRADITIONS / ASSYRIA / 671 BC: MEMPHIS.`
- **AI motion prompt:** `Temple fix-up; then arrow strikes. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 109 · 18:00–18:10 · A · Satellite map

**VO:** "and in 663 BC it sacked Thebes and drove the Kushite kings back south for good. … A delta prince, Psamtik I, used the Assyrians' retreat and hired Greek soldiers to reunite Egypt."

- **Visual:** Fire icon on THEBES; the Kushite icon is pushed back south. Then Psamtik I, a young delta prince, hires Greek soldiers in bronze helmets; the map turns one colour again. The Guide is not in this shot.
- **On-screen text:** 663 BC: THEBES SACKED / PSAMTIK I REUNITES EGYPT
- **Camera / animation:** Arrows, then recolour
- **SFX / music:** crash, unifying chime
- **Pace:** 38 spoken words · ≈ 13.2 s at locked speed. Dense line: do NOT speed up. Let it run to ~13.2s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Fire icon on THEBES; the Kushite icon is pushed back south. Then Psamtik I, a young delta prince, hires Greek soldiers in bronze helmets; the map turns one colour again. Text in frame: 663 BC: THEBES SACKED / PSAMTIK I REUNITES EGYPT.`
- **AI motion prompt:** `Arrows, then recolour. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 110 · 18:10–18:20 · C · Illustrated world

**VO:** "His dynasty was the last great native revival, and it lasted about 140 years. … It opened Egypt to Greek traders,"

- **Visual:** Egyptian revival: freshly painted temples, an old-style statue; a timeline bar fills to 140 YEARS. Greek merchant ships with eye-painted prows dock in the delta, trading olive oil and silver. The Guide haggles with a Greek trader.
- **On-screen text:** LAST NATIVE REVIVAL / 140 YEARS / GREEK TRADERS
- **Camera / animation:** Pan along the dock
- **SFX / music:** waves, market chatter
- **Pace:** 23 spoken words · ≈ 8.9 s at locked speed. Light line: keep the same speed; leave a ~1.1s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Egyptian revival: freshly painted temples, an old-style statue; a timeline bar fills to 140 YEARS. Greek merchant ships with eye-painted prows dock in the delta, trading olive oil and silver. The Guide haggles with a Greek trader. Include the Guide exactly as in the character reference. Text in frame: LAST NATIVE REVIVAL / 140 YEARS / GREEK TRADERS.`
- **AI motion prompt:** `Pan along the dock. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

**Batch 11 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 12: Persia and Alexander (Scenes 111–120, 18:20–20:00)

#### Scene 111 · 18:20–18:30 · A · Satellite map

**VO:** "and Psamtik's son Necho II tried to win back Syria. But in 605 BC, the Babylonian prince Nebuchadnezzar crushed the Egyptian army at Carchemish."

- **Visual:** Map: Pharaoh Necho II marches north toward SYRIA. A Babylonian arrow (Nebuchadnezzar, young prince) slams into it at CARCHEMISH; the Egyptian arrow shatters. The Guide is not in this shot.
- **On-screen text:** NECHO II / 605 BC: CARCHEMISH / NEBUCHADNEZZAR
- **Camera / animation:** Arrows collide; Egyptian one breaks
- **SFX / music:** crash, glass shatter
- **Pace:** 29 spoken words · ≈ 11.7 s at locked speed. Dense line: do NOT speed up. Let it run to ~11.7s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Map: Pharaoh Necho II marches north toward SYRIA. A Babylonian arrow (Nebuchadnezzar, young prince) slams into it at CARCHEMISH; the Egyptian arrow shatters. Text in frame: NECHO II / 605 BC: CARCHEMISH / NEBUCHADNEZZAR.`
- **AI motion prompt:** `Arrows collide; Egyptian one breaks. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 112 · 18:30–18:40 · C · Illustrated world

**VO:** "Egypt's days as an empire were over. … In 525 BC, the Persian king Cambyses defeated the last king of that dynasty at Pelusium,"

- **Visual:** The Egyptian empire flag slides down its pole. Then, at a desert border fort, PELUSIUM, the Persian king Cambyses (tall hat, long curled beard) arrives with a huge army. The Guide is not in this shot.
- **On-screen text:** EMPIRE OVER / 525 BC / CAMBYSES AT PELUSIUM
- **Camera / animation:** Flag lowers; cut to wide army shot
- **SFX / music:** sad trumpet, war horns
- **Pace:** 28 spoken words · ≈ 10.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: The Egyptian empire flag slides down its pole. Then, at a desert border fort, PELUSIUM, the Persian king Cambyses (tall hat, long curled beard) arrives with a huge army. Text in frame: EMPIRE OVER / 525 BC / CAMBYSES AT PELUSIUM.`
- **AI motion prompt:** `Flag lowers; cut to wide army shot. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 113 · 18:40–18:50 · A · Satellite map

**VO:** "on Egypt's eastern border. Egypt became a province of the largest empire the world had yet seen, ruled from Iran."

- **Visual:** Satellite map: a giant red Persian overlay spreads from IRAN across the Middle East and swallows Egypt. A capital pin glows in Iran. The Guide steps back from the size of it.
- **On-screen text:** A PERSIAN PROVINCE / RULED FROM IRAN
- **Camera / animation:** Overlay spreads westward
- **SFX / music:** deep rumble
- **Pace:** 20 spoken words · ≈ 7.4 s at locked speed. Light line: keep the same speed; leave a ~2.6s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map: a giant red Persian overlay spreads from IRAN across the Middle East and swallows Egypt. A capital pin glows in Iran. The Guide steps back from the size of it. Include the Guide exactly as in the character reference. Text in frame: A PERSIAN PROVINCE / RULED FROM IRAN.`
- **AI motion prompt:** `Overlay spreads westward. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 114 · 18:50–19:00 · C · Illustrated world

**VO:** "Some Persian kings, like Darius I, respected Egyptian temples and ruled through local officials. Others were harsher, and Egyptians rebelled again and again."

- **Visual:** Darius I (Persian king) bows at an Egyptian temple with local officials beside him. Then a harsher Persian king with a whip; Egyptian crowds rise up with fists raised, again and again (three quick revolt beats). The Guide is not in this shot.
- **On-screen text:** DARIUS I / HARSHER KINGS / REVOLT AFTER REVOLT
- **Camera / animation:** Calm cut, then three quick revolt beats
- **SFX / music:** gentle music, then crowd shouts
- **Pace:** 24 spoken words · ≈ 10.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Darius I (Persian king) bows at an Egyptian temple with local officials beside him. Then a harsher Persian king with a whip; Egyptian crowds rise up with fists raised, again and again (three quick revolt beats). Text in frame: DARIUS I / HARSHER KINGS / REVOLT AFTER REVOLT.`
- **AI motion prompt:** `Calm cut, then three quick revolt beats. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 115 · 19:00–19:10 · C · Illustrated world

**VO:** "In 404 BC, they finally broke free. … Independence lasted about 60 years. In 343 BC, Persia invaded again and won."

- **Visual:** 404 BC: Egyptians break a chain; flags go up. A timer card counts 60 YEARS. Then 343 BC: Persian army returns over the horizon. The Guide is not in this shot.
- **On-screen text:** 404 BC: FREE / ~60 YEARS / 343 BC: PERSIA RETURNS
- **Camera / animation:** Timeline slide; army rises over the dunes
- **SFX / music:** cheers, then war drums
- **Pace:** 29 spoken words · ≈ 10.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: 404 BC: Egyptians break a chain; flags go up. A timer card counts 60 YEARS. Then 343 BC: Persian army returns over the horizon. Text in frame: 404 BC: FREE / ~60 YEARS / 343 BC: PERSIA RETURNS.`
- **AI motion prompt:** `Timeline slide; army rises over the dunes. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 116 · 19:10–19:20 · C · Illustrated world

**VO:** "The pharaoh who lost that war, Nectanebo II, is usually counted as the last native Egyptian to rule Egypt for about 2,300 years."

- **Visual:** Sunset: the last native pharaoh, Nectanebo II, walks away into the desert, fading. A yellow counter rolls up to 2,300 YEARS, the same number from the opening. The Guide points to it.
- **On-screen text:** NECTANEBO II / LAST NATIVE PHARAOH / 2,300 YEARS
- **Camera / animation:** Slow fade; counter rolls
- **SFX / music:** single sad note, drum hit
- **Pace:** 27 spoken words · ≈ 10.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Sunset: the last native pharaoh, Nectanebo II, walks away into the desert, fading. A yellow counter rolls up to 2,300 YEARS, the same number from the opening. The Guide points to it. Include the Guide exactly as in the character reference. Text in frame: NECTANEBO II / LAST NATIVE PHARAOH / 2,300 YEARS.`
- **AI motion prompt:** `Slow fade; counter rolls. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 117 · 19:20–19:30 · C · Illustrated world

**VO:** "That's the number from the start of this video. … In 332 BC, Alexander the Great took Egypt from the Persians, and many Egyptians welcomed him."

- **Visual:** Quick flashback to the opening card (pyramids and 2,300 YEARS). Then Alexander the Great (young, curly hair, plumed helmet) rides into Egypt; Egyptians cheer as the Persians flee. The Guide is not in this shot.
- **On-screen text:** 332 BC / ALEXANDER THE GREAT / WELCOMED
- **Camera / animation:** Flashback flash; cut to the arrival
- **SFX / music:** whoosh, cheering crowd
- **Pace:** 30 spoken words · ≈ 10.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Quick flashback to the opening card (pyramids and 2,300 YEARS). Then Alexander the Great (young, curly hair, plumed helmet) rides into Egypt; Egyptians cheer as the Persians flee. Text in frame: 332 BC / ALEXANDER THE GREAT / WELCOMED.`
- **AI motion prompt:** `Flashback flash; cut to the arrival. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 118 · 19:30–19:40 · C · Illustrated world

**VO:** "He travelled to the oracle of Amun at Siwa, in the western desert, and was hailed as the god's son. Egypt accepted him as pharaoh."

- **Visual:** Desert oasis at Siwa, with palm trees and a small temple. Inside, the oracle of Amun speaks: a glow says SON OF AMUN. Priests place the double crown on Alexander's head. The Guide is not in this shot.
- **On-screen text:** SIWA / "SON OF AMUN" / PHARAOH
- **Camera / animation:** Push into the temple; crown placement
- **SFX / music:** choir, crown pop
- **Pace:** 25 spoken words · ≈ 9.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Desert oasis at Siwa, with palm trees and a small temple. Inside, the oracle of Amun speaks: a glow says SON OF AMUN. Priests place the double crown on Alexander's head. Text in frame: SIWA / "SON OF AMUN" / PHARAOH.`
- **AI motion prompt:** `Push into the temple; crown placement. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 119 · 19:40–19:50 · A · Satellite map

**VO:** "He founded a new city on the coast: Alexandria. He left after a few months and never returned alive, but his body was later brought back and buried there."

- **Visual:** Satellite map of the coast: a pin ALEXANDRIA drops by the sea, with a city sketch. Alexander's ship sails away. Then a funeral cart with a golden coffin returns to Alexandria. The Guide is not in this shot.
- **On-screen text:** ALEXANDRIA / NEVER RETURNED ALIVE
- **Camera / animation:** Pin drop; ship leaves; cart returns
- **SFX / music:** waves, sombre drum
- **Pace:** 29 spoken words · ≈ 10.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map of the coast: a pin ALEXANDRIA drops by the sea, with a city sketch. Alexander's ship sails away. Then a funeral cart with a golden coffin returns to Alexandria. Text in frame: ALEXANDRIA / NEVER RETURNED ALIVE.`
- **AI motion prompt:** `Pin drop; ship leaves; cart returns. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 120 · 19:50–20:00 · C · Illustrated world

**VO:** "After Alexander's death in 323 BC, his general Ptolemy took Egypt, and Ptolemy's family ruled it for nearly 300 years."

- **Visual:** General Ptolemy takes the crown from Alexander's empty throne. A family tree of Ptolemies branches across the screen; a timeline bar fills ~300 YEARS. The Guide is not in this shot.
- **On-screen text:** 323 BC / PTOLEMY / ~300 YEARS
- **Camera / animation:** Tree grows
- **SFX / music:** fanfare
- **Pace:** 26 spoken words · ≈ 10.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: General Ptolemy takes the crown from Alexander's empty throne. A family tree of Ptolemies branches across the screen; a timeline bar fills ~300 YEARS. Text in frame: 323 BC / PTOLEMY / ~300 YEARS.`
- **AI motion prompt:** `Tree grows. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

**Batch 12 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.

### Batch 13: The Ptolemies and Cleopatra (Scenes 121–132, 20:00–22:00)

#### Scene 121 · 20:00–20:10 · B · Grey studio

**VO:** "The system was simple: Greek-speaking officials at the top, Egyptian farmers at the bottom, and the Nile's harvest taxed to fund the court."

- **Visual:** Grey studio. A society pyramid: Greek-speaking officials at the top, Egyptian farmers at the bottom. Grain from the Nile flows up as tax arrows to the court. The Guide holds a tax scroll.
- **On-screen text:** THE SYSTEM / GREEK OFFICIALS / EGYPTIAN FARMERS
- **Camera / animation:** Pyramid builds; arrows flow upward
- **SFX / music:** coins, grain pouring
- **Pace:** 24 spoken words · ≈ 8.9 s at locked speed. Light line: keep the same speed; leave a ~1.1s beat of music at the end.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio. A society pyramid: Greek-speaking officials at the top, Egyptian farmers at the bottom. Grain from the Nile flows up as tax arrows to the court. The Guide holds a tax scroll. Include the Guide exactly as in the character reference. Text in frame: THE SYSTEM / GREEK OFFICIALS / EGYPTIAN FARMERS.`
- **AI motion prompt:** `Pyramid builds; arrows flow upward. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 122 · 20:10–20:20 · C · Illustrated world

**VO:** "To Egyptians, the Ptolemies presented themselves as pharaohs. They built huge temples in the traditional style, like those at Edfu and Dendera,"

- **Visual:** A Ptolemy king (Greek curly hair under a pharaoh's double crown) offers incense to the falcon god Horus. Behind him, the giant temples of Edfu and Dendera rise in the old Egyptian style: tall pylons, columns with painted capitals. The Guide looks up and pats the wall as if checking it's real.
- **On-screen text:** THE PTOLEMIES AS PHARAOHS / EDFU · DENDERA
- **Camera / animation:** Slow pan along the pylon fronts; temples rise from the sand
- **SFX / music:** temple chant, stone rumble
- **Pace:** 22 spoken words · ≈ 9.7 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: A Ptolemy king (Greek curly hair under a pharaoh's double crown) offers incense to the falcon god Horus. Behind him, the giant temples of Edfu and Dendera rise in the old Egyptian style: tall pylons, columns with painted capitals. The Guide looks up and pats the wall as if checking it's real. Include the Guide exactly as in the character reference. Text in frame: THE PTOLEMIES AS PHARAOHS / EDFU · DENDERA.`
- **AI motion prompt:** `Slow pan along the pylon fronts; temples rise from the sand. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 123 · 20:20–20:30 · D · Artefact / relief close-up

**VO:** "with their Greek names carved in hieroglyphs. Foreign rulers kept becoming, at least on temple walls, Egyptian kings. … Alexandria became the greatest city of the Greek world,"

- **Visual:** Close-up of a temple wall: the Greek name PTOLEMAIOS written in a hieroglyph cartouche, glowing. The "pattern" loop arrow from scene 54 spins back in: FOREIGN RULER → EGYPTIAN KING. Then a sunny wide shot of Alexandria's harbour skyline. The Guide is not in this shot.
- **On-screen text:** THE PATTERN, AGAIN / ALEXANDRIA
- **Camera / animation:** Zoom into the cartouche; loop arrow spins; cut to the skyline
- **SFX / music:** ding, harbour bustle
- **Pace:** 27 spoken words · ≈ 10.9 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: Close-up of a temple wall: the Greek name PTOLEMAIOS written in a hieroglyph cartouche, glowing. The "pattern" loop arrow from scene 54 spins back in: FOREIGN RULER → EGYPTIAN KING. Then a sunny wide shot of Alexandria's harbour skyline. Text in frame: THE PATTERN, AGAIN / ALEXANDRIA.`
- **AI motion prompt:** `Zoom into the cartouche; loop arrow spins; cut to the skyline. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 124 · 20:30–20:40 · C · Illustrated world

**VO:** "with its lighthouse, one of the Seven Wonders, and its Great Library. Scholars there worked out the size of the Earth and wrote the geometry still taught today. But the royal court itself spoke Greek."

- **Visual:** The Lighthouse of Alexandria with a fire on top and a star badge (7 WONDERS). Inside the Great Library: shelves of scroll cubbies. A scholar measures a stick's shadow, and a globe with a measuring tape appears; triangles and circles draw themselves (geometry). Finally a royal courtier speaks a Greek-letter speech bubble (Α Β Γ). The Guide is not in this shot.
- **On-screen text:** LIGHTHOUSE · GREAT LIBRARY / SIZE OF THE EARTH / THE COURT SPOKE GREEK
- **Camera / animation:** Pan from lighthouse to library; geometry draws on
- **SFX / music:** waves, page rustles, chalk drawing
- **Pace:** 35 spoken words · ≈ 11.4 s at locked speed. Dense line: do NOT speed up. Let it run to ~11.4s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: The Lighthouse of Alexandria with a fire on top and a star badge (7 WONDERS). Inside the Great Library: shelves of scroll cubbies. A scholar measures a stick's shadow, and a globe with a measuring tape appears; triangles and circles draw themselves (geometry). Finally a royal courtier speaks a Greek-letter speech bubble (Α Β Γ). Text in frame: LIGHTHOUSE · GREAT LIBRARY / SIZE OF THE EARTH / THE COURT SPOKE GREEK.`
- **AI motion prompt:** `Pan from lighthouse to library; geometry draws on. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 125 · 20:40–20:50 · B · Grey studio

**VO:** "The Ptolemies kept power in the family, often by brothers marrying sisters. Heavy taxes bred resentment, and for about 20 years, rebels held much of southern Egypt."

- **Visual:** Grey studio: a royal family tree in which brother and sister icons link with heart lines. The Guide grimaces. Then a tax collector loads heavy grain sacks; angry farmers. A small map shows southern Egypt turning rebel orange, with a counter: ~20 YEARS.
- **On-screen text:** KEEPING POWER IN THE FAMILY / HEAVY TAXES / REBELS HOLD THE SOUTH
- **Camera / animation:** Tree draws; map overlay spreads
- **SFX / music:** grumbling crowd, counter ticks
- **Pace:** 27 spoken words · ≈ 11.2 s at locked speed. Dense line: do NOT speed up. Let it run to ~11.2s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: plain flat light-grey background (#C9C9C9), no floor line; the Guide character standing full-body in the left third; flat icons, cards and stick figures on the right two-thirds. Scene: Grey studio: a royal family tree in which brother and sister icons link with heart lines. The Guide grimaces. Then a tax collector loads heavy grain sacks; angry farmers. A small map shows southern Egypt turning rebel orange, with a counter: ~20 YEARS. Include the Guide exactly as in the character reference. Text in frame: KEEPING POWER IN THE FAMILY / HEAVY TAXES / REBELS HOLD THE SOUTH.`
- **AI motion prompt:** `Tree draws; map overlay spreads. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 126 · 20:50–21:00 · D · Artefact / relief close-up

**VO:** "In 196 BC, during that revolt, priests at Memphis issued a decree honouring the young king Ptolemy V. It was carved in three scripts: hieroglyphs,"

- **Visual:** Inside a temple at Memphis, priests carve a decree into a dark grey stone slab. A young boy king, Ptolemy V, sits on a throne nearby with a small crown. The carving starts at the top. The Guide is not in this shot.
- **On-screen text:** 196 BC / THE MEMPHIS DECREE / PTOLEMY V
- **Camera / animation:** Chisel strokes appear line by line
- **SFX / music:** chisel taps, temple echo
- **Pace:** 31 spoken words · ≈ 11.4 s at locked speed. Dense line: do NOT speed up. Let it run to ~11.4s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: Inside a temple at Memphis, priests carve a decree into a dark grey stone slab. A young boy king, Ptolemy V, sits on a throne nearby with a small crown. The carving starts at the top. Text in frame: 196 BC / THE MEMPHIS DECREE / PTOLEMY V.`
- **AI motion prompt:** `Chisel strokes appear line by line. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 127 · 21:00–21:10 · D · Artefact / relief close-up

**VO:** "the everyday Egyptian script called Demotic, and Greek. Remember this stone. … The last ruler of the dynasty was Cleopatra VII. According to the ancient writer Plutarch,"

- **Visual:** The finished stone shows three bands: HIEROGLYPHS (top), DEMOTIC (middle), GREEK (bottom), each label popping in. The Guide taps it and winks: "Remember this stone." Cut to Cleopatra VII in royal dress with the cobra crown, on a throne in Alexandria.
- **On-screen text:** HIEROGLYPHS · DEMOTIC · GREEK / REMEMBER THIS STONE / CLEOPATRA VII
- **Camera / animation:** Zoom on stone; three labels pop; hard cut to Cleopatra
- **SFX / music:** three pops, sting, royal harp
- **Pace:** 27 spoken words · ≈ 11.9 s at locked speed. Dense line: do NOT speed up. Let it run to ~11.9s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: close-up of an ancient object drawn in the same flat cartoon line style (papyrus, stone relief, clay tablet), warm paper-texture background, subtle vignette. Scene: The finished stone shows three bands: HIEROGLYPHS (top), DEMOTIC (middle), GREEK (bottom), each label popping in. The Guide taps it and winks: "Remember this stone." Cut to Cleopatra VII in royal dress with the cobra crown, on a throne in Alexandria. Include the Guide exactly as in the character reference. Text in frame: HIEROGLYPHS · DEMOTIC · GREEK / REMEMBER THIS STONE / CLEOPATRA VII.`
- **AI motion prompt:** `Zoom on stone; three labels pop; hard cut to Cleopatra. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 128 · 21:10–21:20 · C · Illustrated world

**VO:** "she was the first of her family to learn Egyptian. She needed powerful allies to keep Egypt free of Rome, which was swallowing the Mediterranean. … In 48 BC,"

- **Visual:** Cleopatra sits with an Egyptian scribe, learning hieroglyphs (a small book quote from PLUTARCH pops in). Then a satellite map: Roman red spreads around the Mediterranean like a rising tide, closing in on Egypt. The Guide is not in this shot.
- **On-screen text:** FIRST OF HER FAMILY TO LEARN EGYPTIAN / ROME IS COMING
- **Camera / animation:** Book card pops; red overlay spreads
- **SFX / music:** quill scratch, ominous drum
- **Pace:** 30 spoken words · ≈ 11.4 s at locked speed. Dense line: do NOT speed up. Let it run to ~11.4s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Cleopatra sits with an Egyptian scribe, learning hieroglyphs (a small book quote from PLUTARCH pops in). Then a satellite map: Roman red spreads around the Mediterranean like a rising tide, closing in on Egypt. Text in frame: FIRST OF HER FAMILY TO LEARN EGYPTIAN / ROME IS COMING.`
- **AI motion prompt:** `Book card pops; red overlay spreads. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 129 · 21:20–21:30 · C · Illustrated world

**VO:** "she was fighting her own brother for the throne when Julius Caesar arrived in Alexandria. She won his support, he defeated her rivals, and she had a son with him, Caesarion."

- **Visual:** Cleopatra and her younger brother tug a crown back and forth. Julius Caesar (laurel wreath, red cloak) sails into Alexandria. Cleopatra wins his support; her brother's army falls back. Then she holds baby Caesarion. The Guide is not in this shot.
- **On-screen text:** 48 BC / JULIUS CAESAR / CAESARION
- **Camera / animation:** Tug-of-war, Caesar's ship arrives; baby pops in
- **SFX / music:** tug creak, horns, baby giggle
- **Pace:** 31 spoken words · ≈ 11.4 s at locked speed. Dense line: do NOT speed up. Let it run to ~11.4s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Cleopatra and her younger brother tug a crown back and forth. Julius Caesar (laurel wreath, red cloak) sails into Alexandria. Cleopatra wins his support; her brother's army falls back. Then she holds baby Caesarion. Text in frame: 48 BC / JULIUS CAESAR / CAESARION.`
- **AI motion prompt:** `Tug-of-war, Caesar's ship arrives; baby pops in. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 130 · 21:30–21:40 · C · Illustrated world

**VO:** "After Caesar's murder, she allied with Mark Antony, who controlled Rome's eastern provinces. That made them enemies of Caesar's heir, Octavian."

- **Visual:** Shadows of daggers in the Roman Senate (no gore): CAESAR'S MURDER. Then Cleopatra shakes hands with Mark Antony (armour, eastern map behind him). Across the sea on the right, Octavian (young, pale, toga) frowns with arms crossed. The Guide is not in this shot.
- **On-screen text:** ANTONY & CLEOPATRA vs OCTAVIAN
- **Camera / animation:** Split screen with a dividing wave line
- **SFX / music:** tense strings, gasp
- **Pace:** 21 spoken words · ≈ 9.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Shadows of daggers in the Roman Senate (no gore): CAESAR'S MURDER. Then Cleopatra shakes hands with Mark Antony (armour, eastern map behind him). Across the sea on the right, Octavian (young, pale, toga) frowns with arms crossed. Text in frame: ANTONY & CLEOPATRA vs OCTAVIAN.`
- **AI motion prompt:** `Split screen with a dividing wave line. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 131 · 21:40–21:50 · A · Satellite map

**VO:** "When Antony and Cleopatra lost the naval battle of Actium to Octavian in 31 BC, it was over. Antony killed himself,"

- **Visual:** Satellite map of western Greece: two fleets meet at ACTIUM. Octavian's ships surround Antony's; Antony and Cleopatra's ships flee toward Egypt. A dark fade on Antony's figure. The Guide is not in this shot.
- **On-screen text:** 31 BC / BATTLE OF ACTIUM
- **Camera / animation:** Naval clash animation; fade on Antony
- **SFX / music:** waves, oars, crash, low drum
- **Pace:** 23 spoken words · ≈ 9.4 s at locked speed. Normal pace.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: realistic satellite-photo map background (NASA Blue Marble look), flat red/orange semi-transparent territory overlays, white hand-lettered place labels; the Guide character in the bottom-right corner shown from the knees up, about 40% of frame height. Scene: Satellite map of western Greece: two fleets meet at ACTIUM. Octavian's ships surround Antony's; Antony and Cleopatra's ships flee toward Egypt. A dark fade on Antony's figure. Text in frame: 31 BC / BATTLE OF ACTIUM.`
- **AI motion prompt:** `Naval clash animation; fade on Antony. Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

#### Scene 132 · 21:50–22:00 · C · Illustrated world

**VO:** "and in 30 BC Cleopatra died too, by tradition from a snake bite. Egypt became part of the Roman Empire. … Octavian, now Emperor Augustus, kept Egypt as his personal"

- **Visual:** Alexandria palace at dusk: Cleopatra sits on her throne, a small cobra coiled near her; she fades gently into gold dust. A Roman eagle banner rises over Egypt. Octavian, now Augustus, steps forward holding a small model of Egypt in his hands like a possession. The Guide is not in this shot.
- **On-screen text:** 30 BC / EGYPT BECOMES ROMAN / AUGUSTUS
- **Camera / animation:** Slow fade; banner rises; hold on Augustus (cliffhanger)
- **SFX / music:** sombre strings, eagle cry
- **Pace:** 30 spoken words · ≈ 11.9 s at locked speed. Dense line: do NOT speed up. Let it run to ~11.9s and hold the picture until the line ends.
- **AI image prompt:** `Flat 2D vector cartoon, educational history YouTube explainer style, clean thin dark-brown outlines, simple flat colours with very light soft shading, characters with round heads, dot eyes and thin stick arms and legs, 16:9, 1920x1080, no photorealism, no 3D. Setting: flat 2D cartoon landscape, simple layered desert/river background, soft blue sky with puffy white cartoon clouds (or orange-to-purple sunset gradient with pink clouds for dramatic beats), dry-grass ground texture; small stick-limbed characters. Scene: Alexandria palace at dusk: Cleopatra sits on her throne, a small cobra coiled near her; she fades gently into gold dust. A Roman eagle banner rises over Egypt. Octavian, now Augustus, steps forward holding a small model of Egypt in his hands like a possession. Text in frame: 30 BC / EGYPT BECOMES ROMAN / AUGUSTUS.`
- **AI motion prompt:** `Slow fade; banner rises; hold on Augustus (cliffhanger). Gentle cartoon motion, elements pop in with a small bounce, 10 seconds.`

**Batch 13 consistency check:** same voice + settings · the Guide matches the reference (hat, red feather, yellow tunic, spear) · labels white hand-lettered, punch words yellow comic · music bed continuous across the batch boundary.
