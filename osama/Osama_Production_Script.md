# The Hunt for Osama bin Laden: Scene-by-Scene Production Script

**Format:** 16:9, 1920×1080, 24 fps · **Scenes:** 237 (5–8 s each, average 6.5 s) · **Runtime:** ≈ 25.7 min · **Voice:** Kokoro `am_puck`, speed 0.85, the same voice and settings in every batch

## 1. Visual style: realistic documentary reconstruction

| Element | Rule |
|---|---|
| Images | Realistic, cinematic stills like a documentary reconstruction: natural light, real places and objects, 35 mm film look with light grain. One image per scene, held with a slow push-in. Generated with DreamShaper 8 LCM (CreativeML OpenRAIL-M licence, commercial use allowed). |
| Maps | Dark intelligence-style map: the country in focus lit amber with a glowing edge, red pins dropping in with pulsing rings and white labels, routes as dashed red lines. The map zooms in from a wide view. |
| Captions | Documentary lower third: white condensed capitals (Oswald) with a red bar, bottom left, over a soft dark gradient. |
| Titles | Big white condensed capitals with a short red line underneath, centred, for key moments and numbers (2,977 counts up). |
| Dates | A typewriter-style date stamp slides in at the top left whenever a full date is spoken. |
| Pace | A new picture every 5–8 s; captions change with the narration. Cuts are hard cuts. |
| Disclosure | A small "Dramatized reconstruction · AI-generated images" note at the start (YouTube also asks creators to label realistic AI content). |
| Sensitive moments | 9/11 is shown as skyline and smoke, never impacts or people. The raid uses silhouettes, flashes and night-vision tints: no wounds, no body. Real people appear as silhouettes, from behind or in shadow, never as realistic faces; bin Laden is always a faceless silhouette, as your script asks. |

## 2. Voice (same in every batch)

| Setting | Value |
|---|---|
| Voice | Kokoro `am_puck` (the voice you approved for the Egypt video) |
| Speed | 0.85, about 140 words per minute: calm, not fast and not slow |
| Pauses | 0.38 s after each sentence, 0.85 s after each paragraph |
| Processing | Light EQ and compression only, identical for the whole video |
| Music | Original tense bed (D minor, 84 BPM, composed in code), ducked under the voice |

## 3. Image prompts

Every illustration prompt below starts with this style line:

> Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic

Map scenes use:

> Dark intelligence-style map: near-black sea, dark slate land, thin blue-grey borders, the featured country lit amber with a glowing edge, red pins with pulsing rings and white condensed labels, faint grid, film grain

Save each generated image as `osama/video/images/NNN.png` (e.g. `007.png` for scene 7). The renderer uses it instead of its own drawing and keeps the camera moves, captions, calendar and timing.

## 4. Scenes

### Part 1 — 9/11 to Tora Bora

#### Scene 001 · 00:00.0–00:05.4 (5.4 s) · ILLUS

**VO:** "You know how Osama bin Laden died. But do you know why he hid for five years,"

- **Visual:** Night over a walled three-storey house. On the top-floor balcony, behind a high wall, a tall faceless silhouette paces back and forth; a single warm window glows below; barbed wire on the wall tops, a crescent moon.
- **On-screen text:** WHY DID HE HIDE 5 YEARS?
- **Camera / animation:** Slow push-in toward the balcony
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Night over a walled three-storey house. On the top-floor balcony, behind a high wall, a tall faceless silhouette paces back and forth; a single warm window glows below; barbed wire on the wall tops, a crescent moon.`

#### Scene 002 · 00:05.4–00:12.7 (7.4 s) · MAP

**VO:** "less than a mile from Pakistan's top military academy… until one phone call he never even made?"

- **Visual:** Paper map of northern Pakistan: red pin ABBOTTABAD, a second pin KAKUL MILITARY ACADEMY right beside it; a measuring line between them labelled "< 1 MILE".
- **On-screen text:** LESS THAN A MILE / ONE PHONE CALL
- **Camera / animation:** Zoom in from Pakistan to Abbottabad
- **Image prompt:** `Dark intelligence-style map: near-black sea, dark slate land, thin blue-grey borders, the featured country lit amber with a glowing edge, red pins with pulsing rings and white condensed labels, faint grid, film grain. Paper map of northern Pakistan: red pin ABBOTTABAD, a second pin KAKUL MILITARY ACADEMY right beside it; a measuring line between them labelled "< 1 MILE".`

#### Scene 003 · 00:12.7–00:17.6 (4.8 s) · ILLUS

**VO:** "This is the full story of the ten-year hunt. From the morning of 9/11"

- **Visual:** Fast montage panel 1: the Manhattan skyline on a clear morning with smoke rising from the twin towers in the distance (no impact shown); a tear-off calendar reading 11 SEPTEMBER 2001.
- **On-screen text:** THE TEN-YEAR HUNT
- **Camera / animation:** Quick push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Fast montage panel 1: the Manhattan skyline on a clear morning with smoke rising from the twin towers in the distance (no impact shown); a tear-off calendar reading 11 SEPTEMBER 2001.`

#### Scene 004 · 00:17.6–00:24.0 (6.4 s) · ILLUS

**VO:** "to forty minutes inside a house in Abbottabad. And it starts at 8:46 a.m."

- **Visual:** Montage panel 2: snowy Afghan peaks, then a white jeep on a dusty road and two dark helicopters against a night sky; a wall clock showing 8:46.
- **On-screen text:** 40 MINUTES IN ABBOTTABAD / 8:46 A.M.
- **Camera / animation:** Hard cuts between panels
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Montage panel 2: snowy Afghan peaks, then a white jeep on a dusty road and two dark helicopters against a night sky; a wall clock showing 8:46.`

#### Scene 005 · 00:24.0–00:29.5 (5.6 s) · ILLUS

**VO:** "September 11, 2001. New York City. 8:46 in the morning."

- **Visual:** New York skyline on a clear blue morning, the twin towers standing tall; a tear-off calendar SEPTEMBER 11, 2001 and a clock at 8:46.
- **On-screen text:** SEPTEMBER 11, 2001 / NEW YORK CITY
- **Camera / animation:** Slow pan across the skyline
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. New York skyline on a clear blue morning, the twin towers standing tall; a tear-off calendar SEPTEMBER 11, 2001 and a clock at 8:46.`

#### Scene 006 · 00:29.5–00:35.4 (5.8 s) · ILLUS

**VO:** "American Airlines Flight 11 crashes into the North Tower of the World Trade Center."

- **Visual:** Wide skyline: a dark plume of smoke rising from the North Tower (impact already happened, no plane or fire close-up). Pigeons scatter over the Hudson.
- **On-screen text:** FLIGHT 11 · NORTH TOWER
- **Camera / animation:** Slow push-in on the towers
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Wide skyline: a dark plume of smoke rising from the North Tower (impact already happened, no plane or fire close-up). Pigeons scatter over the Hudson.`

#### Scene 007 · 00:35.4–00:42.2 (6.8 s) · ILLUS

**VO:** "Seventeen minutes later, a second plane tears into the South Tower. … A third plane hits the Pentagon."

- **Visual:** Both towers trailing grey smoke; then cut to the Pentagon from the air with a smoke column rising from one side.
- **On-screen text:** 17 MINUTES LATER / THE PENTAGON
- **Camera / animation:** Hard cut between the two
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Both towers trailing grey smoke; then cut to the Pentagon from the air with a smoke column rising from one side.`

#### Scene 008 · 00:42.2–00:49.9 (7.7 s) · ILLUS

**VO:** "The fourth crashes in a field near Shanksville, Pennsylvania, after its passengers fight back against the hijackers"

- **Visual:** An empty green field near Shanksville under a grey sky; a thin line of smoke far away; a lone fence post in the foreground.
- **On-screen text:** SHANKSVILLE, PENNSYLVANIA / THE PASSENGERS FOUGHT BACK
- **Camera / animation:** Slow push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. An empty green field near Shanksville under a grey sky; a thin line of smoke far away; a lone fence post in the foreground.`

#### Scene 009 · 00:49.9–00:56.7 (6.8 s) · TITLE

**VO:** "and bring it down. … In a single day, 2,977 people are killed."

- **Visual:** Dark memorial panel: rows of small candles; a big counter ticking up to 2,977.
- **On-screen text:** 2,977
- **Camera / animation:** Counter rolls; slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Dark memorial panel: rows of small candles; a big counter ticking up to 2,977.`

#### Scene 010 · 00:56.7–01:01.9 (5.2 s) · TITLE

**VO:** "It is the deadliest terrorist attack ever on American soil. … That same day,"

- **Visual:** Same memorial candles, wider; title in white handwritten capitals with red underline.
- **On-screen text:** THE DEADLIEST ATTACK ON AMERICAN SOIL
- **Camera / animation:** Slow pull-back
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Same memorial candles, wider; title in white handwritten capitals with red underline.`

#### Scene 011 · 01:01.9–01:07.4 (5.5 s) · ILLUS

**VO:** "in the mountains of eastern Afghanistan, Osama bin Laden sat with his men."

- **Visual:** A rocky mountain hideout in eastern Afghanistan at dusk: a cave mouth, a campfire, armed men in turbans crouched around an old radio; a tall bearded figure seen from behind, face hidden.
- **On-screen text:** EASTERN AFGHANISTAN
- **Camera / animation:** Slow pan right to left
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A rocky mountain hideout in eastern Afghanistan at dusk: a cave mouth, a campfire, armed men in turbans crouched around an old radio; a tall bearded figure seen from behind, face hidden.`

#### Scene 012 · 01:07.4–01:13.1 (5.7 s) · ILLUS

**VO:** "He knew exactly what this attack was about to change. What he didn't know was that the longest,"

- **Visual:** Close on the old radio crackling; the tall figure's shadow on the cave wall.
- **On-screen text:** HE KNEW WHAT WOULD CHANGE
- **Camera / animation:** Slow push-in on the radio
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Close on the old radio crackling; the tall figure's shadow on the cave wall.`

#### Scene 013 · 01:13.1–01:22.1 (9.0 s) · ILLUS

**VO:** "most frightening escape of his life had just begun. … The CIA, the FBI and the NSA moved without wasting a second."

- **Visual:** Three logos as stencilled crates/doors in a corridor: CIA, FBI, NSA; agents hurrying through.
- **On-screen text:** CIA · FBI · NSA
- **Camera / animation:** Quick pan along the doors
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Three logos as stencilled crates/doors in a corridor: CIA, FBI, NSA; agents hurrying through.`

#### Scene 014 · 01:22.1–01:29.2 (7.1 s) · ILLUS

**VO:** "The first job: go through the passport and visa records of every passenger on all four hijacked flights."

- **Visual:** An operations room at night: a wall of screens filled with passport photos and passenger lists; analysts at desks with coffee cups.
- **On-screen text:** EVERY PASSENGER · ALL 4 FLIGHTS
- **Camera / animation:** Slow pan across the screens
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. An operations room at night: a wall of screens filled with passport photos and passenger lists; analysts at desks with coffee cups.`

#### Scene 015 · 01:29.2–01:33.3 (4.1 s) · ILLUS

**VO:** "Every background was checked. Every travel history was pulled."

- **Visual:** Close on a screen: rows of passport photos being stamped CHECKED one after another.
- **On-screen text:** EVERY BACKGROUND CHECKED
- **Camera / animation:** Fast push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Close on a screen: rows of passport photos being stamped CHECKED one after another.`

#### Scene 016 · 01:33.3–01:40.1 (6.8 s) · ILLUS

**VO:** "Out of that data, 19 names stood out — the likely hijackers. … Then a coincidence cracked the case."

- **Visual:** The screen narrows to 19 faces (blurred, anonymous silhouettes) highlighted in red boxes.
- **On-screen text:** 19 NAMES
- **Camera / animation:** Highlight pulse on each box
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The screen narrows to 19 faces (blurred, anonymous silhouettes) highlighted in red boxes.`

#### Scene 017 · 01:40.1–01:45.0 (4.9 s) · ILLUS

**VO:** "Mohamed Atta, the lead hijacker, had a bag that missed his connecting flight."

- **Visual:** Logan Airport baggage hall: one black suitcase alone on the carousel with a tag BOS.
- **On-screen text:** THE BAG THAT STAYED BEHIND
- **Camera / animation:** Slow push-in on the bag
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Logan Airport baggage hall: one black suitcase alone on the carousel with a tag BOS.`

#### Scene 018 · 01:45.0–01:51.8 (6.8 s) · ILLUS

**VO:** "It was left behind at Boston's Logan Airport. Agents opened it, and what they found was a goldmine:"

- **Visual:** Agents in windbreakers open the black suitcase on a steel table under bright lights.
- **On-screen text:** LOGAN AIRPORT, BOSTON / A GOLDMINE
- **Camera / animation:** Lid opens; push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Agents in windbreakers open the black suitcase on a steel table under bright lights.`

#### Scene 019 · 01:51.8–01:59.5 (7.8 s) · ILLUS

**VO:** "flight manuals, instructions for the hijackers, and Atta's handwritten will. … That one bag pointed straight at al-Qaeda"

- **Visual:** Contents laid out: flight manuals, a folder of instructions, a handwritten will in an evidence bag.
- **On-screen text:** FLIGHT MANUALS · INSTRUCTIONS · A WILL
- **Camera / animation:** Items slide into place
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Contents laid out: flight manuals, a folder of instructions, a handwritten will in an evidence bag.`

#### Scene 020 · 01:59.5–02:07.2 (7.6 s) · MAP

**VO:** "and Osama bin Laden. Investigators then traced the hijackers' old calls, emails and bank transfers."

- **Visual:** Paper world map: red lines from the USA to the Middle East and Afghanistan, tracing calls, emails and bank transfers.
- **On-screen text:** CALLS · EMAILS · BANK TRANSFERS
- **Camera / animation:** Lines draw on
- **Image prompt:** `Dark intelligence-style map: near-black sea, dark slate land, thin blue-grey borders, the featured country lit amber with a glowing edge, red pins with pulsing rings and white condensed labels, faint grid, film grain. Paper world map: red lines from the USA to the Middle East and Afghanistan, tracing calls, emails and bank transfers.`

#### Scene 021 · 02:07.2–02:13.1 (5.9 s) · ILLUS

**VO:** "The money led straight back into al-Qaeda's network. The case was sealed. The target was clear:"

- **Visual:** An evidence board with photos and red string all converging on one faceless silhouette card.
- **On-screen text:** THE CASE WAS SEALED
- **Camera / animation:** Slow push-in to the center card
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. An evidence board with photos and red string all converging on one faceless silhouette card.`

#### Scene 022 · 02:13.1–02:19.5 (6.4 s) · ILLUS

**VO:** "Osama bin Laden. … On October 7, 2001, America struck Afghanistan."

- **Visual:** The silhouette card stamped TARGET; then a calendar flips to OCTOBER 7, 2001.
- **On-screen text:** THE TARGET: OSAMA BIN LADEN / OCTOBER 7, 2001
- **Camera / animation:** Stamp slams; calendar flip
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The silhouette card stamped TARGET; then a calendar flips to OCTOBER 7, 2001.`

#### Scene 023 · 02:19.5–02:26.1 (6.6 s) · ILLUS

**VO:** "Operation Enduring Freedom had begun. Within weeks, the Taliban regime fell apart. But by then,"

- **Visual:** Jets launching from an aircraft carrier at dawn; then distant hills with bomb smoke; Taliban fighters retreating in pickup trucks.
- **On-screen text:** OPERATION ENDURING FREEDOM / THE TALIBAN FALLS
- **Camera / animation:** Pan across the deck; cut
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Jets launching from an aircraft carrier at dawn; then distant hills with bomb smoke; Taliban fighters retreating in pickup trucks.`

#### Scene 024 · 02:26.1–02:32.5 (6.5 s) · MAP

**VO:** "bin Laden had vanished into Tora Bora — a maze of mountains on the border between Afghanistan"

- **Visual:** Paper map of Afghanistan and Pakistan; red pin TORA BORA on the border.
- **On-screen text:** TORA BORA
- **Camera / animation:** Zoom to the border
- **Image prompt:** `Dark intelligence-style map: near-black sea, dark slate land, thin blue-grey borders, the featured country lit amber with a glowing edge, red pins with pulsing rings and white condensed labels, faint grid, film grain. Paper map of Afghanistan and Pakistan; red pin TORA BORA on the border.`

#### Scene 025 · 02:32.5–02:39.0 (6.5 s) · ILLUS

**VO:** "and Pakistan. … This was no ordinary mountain range. During the war against the Soviets,"

- **Visual:** Snowy jagged peaks of Tora Bora; cave mouths dotting the cliffs.
- **On-screen text:** A MAZE OF MOUNTAINS
- **Camera / animation:** Slow pan up the peaks
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Snowy jagged peaks of Tora Bora; cave mouths dotting the cliffs.`

#### Scene 026 · 02:39.0–02:44.5 (5.5 s) · ILLUS

**VO:** "bin Laden and the mujahideen had dug deep tunnels and bunkers into these mountains."

- **Visual:** Inside a tunnel lit by lanterns: wooden supports, crates and bunker rooms carved into rock.
- **On-screen text:** TUNNELS AND BUNKERS
- **Camera / animation:** Slow push down the tunnel
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Inside a tunnel lit by lanterns: wooden supports, crates and bunker rooms carved into rock.`

#### Scene 027 · 02:44.5–02:51.7 (7.1 s) · ILLUS

**VO:** "The terrain was so complex that without local knowledge, nobody could get in. Bin Laden knew every path."

- **Visual:** A narrow mountain path along a cliff edge in the snow; a guide pointing the way.
- **On-screen text:** NO LOCAL KNOWLEDGE, NO WAY IN
- **Camera / animation:** Pan along the path
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A narrow mountain path along a cliff edge in the snow; a guide pointing the way.`

#### Scene 028 · 02:51.7–02:57.1 (5.5 s) · ILLUS

**VO:** "The CIA's first clue came from an al-Qaeda member captured in Afghanistan."

- **Visual:** A small room: a captured fighter at a table under a bare bulb, two interrogators across from him.
- **On-screen text:** THE FIRST CLUE
- **Camera / animation:** Slow push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A small room: a captured fighter at a table under a bare bulb, two interrogators across from him.`

#### Scene 029 · 02:57.1–03:03.8 (6.7 s) · ILLUS

**VO:** "He said he had seen bin Laden heading toward Tora Bora. But one clue wasn't enough to launch an attack."

- **Visual:** The prisoner pointing on a map toward the mountains; an interrogator writing "TORA BORA?" in a notebook.
- **On-screen text:** ONE CLUE WASN'T ENOUGH
- **Camera / animation:** Push-in on the notebook
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The prisoner pointing on a map toward the mountains; an interrogator writing "TORA BORA?" in a notebook.`

#### Scene 030 · 03:03.8–03:09.3 (5.5 s) · ILLUS

**VO:** "The second came from a team that monitored al-Qaeda's unsecured radio traffic."

- **Visual:** A radio monitoring tent: operators in headphones beside racks of radio gear.
- **On-screen text:** RADIO TRAFFIC
- **Camera / animation:** Pan across the operators
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A radio monitoring tent: operators in headphones beside racks of radio gear.`

#### Scene 031 · 03:09.3–03:14.7 (5.4 s) · ILLUS

**VO:** "They noticed a strange pattern. Every day, someone was flashing codes with mirrors,"

- **Visual:** Two mountain peaks at dawn; bright mirror flashes jumping from one peak to the other.
- **On-screen text:** MIRROR SIGNALS
- **Camera / animation:** Flash beats between the peaks
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Two mountain peaks at dawn; bright mirror flashes jumping from one peak to the other.`

#### Scene 032 · 03:14.7–03:21.2 (6.5 s) · ILLUS

**VO:** "from one peak to the next. It was an old al-Qaeda trick — signals that left no electronic trace."

- **Visual:** Close on a hand tilting a small mirror; the flash bounces across the valley.
- **On-screen text:** NO ELECTRONIC TRACE
- **Camera / animation:** Slow push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Close on a hand tilting a small mirror; the flash bounces across the valley.`

#### Scene 033 · 03:21.2–03:28.4 (7.2 s) · ILLUS

**VO:** "Then one day, bin Laden slipped. He spoke over an unsecured radio, and the CIA caught the transmission."

- **Visual:** An analyst in headphones; a voice waveform spikes on his screen.
- **On-screen text:** HE SLIPPED
- **Camera / animation:** Push-in on the waveform
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. An analyst in headphones; a voice waveform spikes on his screen.`

#### Scene 034 · 03:28.4–03:34.1 (5.7 s) · ILLUS

**VO:** "A specialist named Jalal, who had studied bin Laden's voice for seven years, listened"

- **Visual:** Close on the analyst's face, eyes widening; a name card JALAL on his desk; "7 YEARS" sticky note.
- **On-screen text:** JALAL · 7 YEARS
- **Camera / animation:** Push-in on his eyes
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Close on the analyst's face, eyes widening; a name card JALAL on his desk; "7 YEARS" sticky note.`

#### Scene 035 · 03:34.1–03:40.6 (6.5 s) · ILLUS

**VO:** "and confirmed it at once: it's him, and he's in Tora Bora. … In December 2001,"

- **Visual:** The analyst's screen labelled MATCH beside a red pin on Tora Bora; a calendar DECEMBER 2001.
- **On-screen text:** IT'S HIM / DECEMBER 2001
- **Camera / animation:** Stamp; calendar flip
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The analyst's screen labelled MATCH beside a red pin on Tora Bora; a calendar DECEMBER 2001.`

#### Scene 036 · 03:40.6–03:47.0 (6.4 s) · ILLUS

**VO:** "American and Northern Alliance forces began pounding Tora Bora. Bin Laden looked finished."

- **Visual:** Bombs bursting along snowy ridgelines; Northern Alliance fighters watching from a slope.
- **On-screen text:** TORA BORA BOMBED
- **Camera / animation:** Slow pan along the ridge
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Bombs bursting along snowy ridgelines; Northern Alliance fighters watching from a slope.`

#### Scene 037 · 03:47.0–03:52.8 (5.7 s) · ILLUS

**VO:** "Then a message came over the radio. He was ready to surrender — if they stopped the bombing"

- **Visual:** A field radio crackling in a fighter's hand; text bubble on the radio.
- **On-screen text:** "I WILL SURRENDER"
- **Camera / animation:** Push-in on the radio
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A field radio crackling in a fighter's hand; text bubble on the radio.`

#### Scene 038 · 03:52.8–03:59.4 (6.6 s) · ILLUS

**VO:** "and gave him a one-day ceasefire. … The CIA was suspicious. But they could hear him on the radio,"

- **Visual:** A white flag on a stick planted in snow; the bombing smoke drifting away.
- **On-screen text:** A ONE-DAY CEASEFIRE
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A white flag on a stick planted in snow; the bombing smoke drifting away.`

#### Scene 039 · 03:59.4–04:04.6 (5.3 s) · ILLUS

**VO:** "telling his fighters to surrender. They fell for it. On December 11,"

- **Visual:** CIA officers in a tent listening to the radio, arms crossed, suspicious.
- **On-screen text:** THEY FELL FOR IT / DECEMBER 11
- **Camera / animation:** Push-in; calendar flip
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. CIA officers in a tent listening to the radio, arms crossed, suspicious.`

#### Scene 040 · 04:04.6–04:09.9 (5.2 s) · ILLUS

**VO:** "the Northern Alliance was told to make the deal. The surrender was set for December 12."

- **Visual:** Calendar pages DECEMBER 11 → DECEMBER 12 pinned beside a negotiation table in a mountain tent.
- **On-screen text:** SURRENDER SET FOR DECEMBER 12
- **Camera / animation:** Calendar flips
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Calendar pages DECEMBER 11 → DECEMBER 12 pinned beside a negotiation table in a mountain tent.`

#### Scene 041 · 04:09.9–04:15.7 (5.8 s) · ILLUS

**VO:** "But the moment the bombs stopped, bin Laden made his real move. He gathered his bodyguards,"

- **Visual:** Night on the mountain: the bombing has stopped; a group of men with packs gathering by torchlight.
- **On-screen text:** THE REAL MOVE
- **Camera / animation:** Slow push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Night on the mountain: the bombing has stopped; a group of men with packs gathering by torchlight.`

#### Scene 042 · 04:15.7–04:20.6 (4.9 s) · ILLUS

**VO:** "climbed onto horses and mules, and slipped away toward Pakistan in the dark."

- **Visual:** A line of men on horses and mules crossing a snowy mountain pass under moonlight.
- **On-screen text:** INTO PAKISTAN
- **Camera / animation:** Slow pan following the line
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A line of men on horses and mules crossing a snowy mountain pass under moonlight.`

#### Scene 043 · 04:20.6–04:27.8 (7.2 s) · MAP

**VO:** "It later emerged that during the ceasefire, Pakistani tribal forces on the other side had let him through."

- **Visual:** Paper map: a dashed red line from TORA BORA across the border into PAKISTAN.
- **On-screen text:** LET THROUGH AT THE BORDER
- **Camera / animation:** Line draws on
- **Image prompt:** `Dark intelligence-style map: near-black sea, dark slate land, thin blue-grey borders, the featured country lit amber with a glowing edge, red pins with pulsing rings and white condensed labels, faint grid, film grain. Paper map: a dashed red line from TORA BORA across the border into PAKISTAN.`

#### Scene 044 · 04:27.8–04:33.1 (5.3 s) · TITLE

**VO:** "Tora Bora became one of the biggest intelligence failures in American history."

- **Visual:** Yellow comic title over dark mountains.
- **On-screen text:** ONE OF THE BIGGEST INTELLIGENCE FAILURES
- **Camera / animation:** Title slam
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Yellow comic title over dark mountains.`

#### Scene 045 · 04:33.1–04:40.5 (7.5 s) · ILLUS

**VO:** "Bin Laden was gone. And what he did next was the work of a mastermind. … The moment he reached Pakistan,"

- **Visual:** An empty cave mouth in the snow; footprints leading away.
- **On-screen text:** GONE
- **Camera / animation:** Slow push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. An empty cave mouth in the snow; footprints leading away.`

### Part 2 — Going dark

#### Scene 046 · 04:40.5–04:47.4 (6.9 s) · ILLUS

**VO:** "bin Laden changed his entire communication system. No mobile phone. No satellite phone."

- **Visual:** On a wooden table: a mobile phone, a satellite phone and a laptop, each switching off with a red X.
- **On-screen text:** NO PHONE · NO SATELLITE PHONE
- **Camera / animation:** Items switch off one by one
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. On a wooden table: a mobile phone, a satellite phone and a laptop, each switching off with a red X.`

#### Scene 047 · 04:47.4–04:53.1 (5.7 s) · ILLUS

**VO:** "No internet. Not even direct contact with his own al-Qaeda members. The man"

- **Visual:** A router with its lights going dark; a cut cable.
- **On-screen text:** NO INTERNET
- **Camera / animation:** Lights go out
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A router with its lights going dark; a cut cable.`

#### Scene 048 · 04:53.1–04:57.7 (4.6 s) · ILLUS

**VO:** "who wanted to hide from the whole world simply walked out of the digital world."

- **Visual:** A tall faceless silhouette walking out of a doorway made of glowing digital code into darkness.
- **On-screen text:** OUT OF THE DIGITAL WORLD
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A tall faceless silhouette walking out of a doorway made of glowing digital code into darkness.`

#### Scene 049 · 04:57.7–05:06.2 (8.5 s) · ILLUS

**VO:** "His only link to the outside was one man: Ibrahim al-Kuwaiti, known to the CIA as Abu Ahmed al-Kuwaiti —"

- **Visual:** A man in a shalwar kameez and waistcoat in a dusty lane; name card IBRAHIM / ABU AHMED AL-KUWAITI.
- **On-screen text:** THE COURIER
- **Camera / animation:** Slow push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A man in a shalwar kameez and waistcoat in a dusty lane; name card IBRAHIM / ABU AHMED AL-KUWAITI.`

#### Scene 050 · 05:06.2–05:11.1 (5.0 s) · ILLUS

**VO:** "al-Qaeda's most trusted man. Bin Laden wrote letters by hand every day"

- **Visual:** Close on a hand writing a letter in Arabic script by lamplight.
- **On-screen text:** HANDWRITTEN LETTERS
- **Camera / animation:** Pan across the page
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Close on a hand writing a letter in Arabic script by lamplight.`

#### Scene 051 · 05:11.1–05:17.3 (6.1 s) · ILLUS

**VO:** "and signed them with a code name. Ibrahim carried them, as a courier, into al-Qaeda's network."

- **Visual:** The courier tucks folded letters inside his vest; a coded signature on the page.
- **On-screen text:** A CODE NAME
- **Camera / animation:** Push-in on the vest
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The courier tucks folded letters inside his vest; a coded signature on the page.`

#### Scene 052 · 05:17.3–05:23.3 (6.0 s) · ILLUS

**VO:** "The replies came back the same way, on handwritten paper. … For urgent messages only,"

- **Visual:** A stack of handwritten replies tied with string on a table.
- **On-screen text:** PAPER ONLY
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A stack of handwritten replies tied with string on a table.`

#### Scene 053 · 05:23.3–05:30.4 (7.1 s) · ILLUS

**VO:** "there was a clever trick. Ibrahim would log into a Gmail account and write the message in the drafts folder."

- **Visual:** A dim internet café: rows of old computers; the courier at a screen showing a Drafts folder.
- **On-screen text:** THE DRAFTS TRICK
- **Camera / animation:** Push-in to the screen
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A dim internet café: rows of old computers; the courier at a screen showing a Drafts folder.`

#### Scene 054 · 05:30.4–05:36.6 (6.2 s) · ILLUS

**VO:** "Other al-Qaeda members logged into the same account and read the draft. The message was never sent,"

- **Visual:** Another man at another café logging into the same account, reading the draft.
- **On-screen text:** NEVER SENT
- **Camera / animation:** Split screen
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Another man at another café logging into the same account, reading the draft.`

#### Scene 055 · 05:36.6–05:42.2 (5.6 s) · ILLUS

**VO:** "so it left no digital trail. It was an old spy technique, and al-Qaeda borrowed it."

- **Visual:** The draft being deleted; the screen empty.
- **On-screen text:** NO DIGITAL TRAIL
- **Camera / animation:** Fade on the screen
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The draft being deleted; the screen empty.`

#### Scene 056 · 05:42.2–05:48.2 (6.1 s) · ILLUS

**VO:** "When the work became too much for one man, Ibrahim brought in his brother, Abrar al-Kuwaiti."

- **Visual:** Two brothers side by side in a courtyard; name card ABRAR AL-KUWAITI.
- **On-screen text:** TWO BROTHERS
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Two brothers side by side in a courtyard; name card ABRAR AL-KUWAITI.`

#### Scene 057 · 05:48.2–05:54.5 (6.3 s) · ILLUS

**VO:** "Both became bin Laden's couriers. But two single men living alone would make people suspicious."

- **Visual:** Both brothers carrying letters; nosy neighbours glance from a rooftop.
- **On-screen text:** TWO COURIERS
- **Camera / animation:** Pan across
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Both brothers carrying letters; nosy neighbours glance from a rooftop.`

#### Scene 058 · 05:54.5–06:01.9 (7.4 s) · ILLUS

**VO:** "So both were married — to women named Bushra and Mariam — so they would look like an ordinary Pashtun family."

- **Visual:** A simple wedding: a decorated courtyard, then an ordinary Pashtun family home with washing on the line.
- **On-screen text:** AN ORDINARY FAMILY
- **Camera / animation:** Cross-cut
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A simple wedding: a decorated courtyard, then an ordinary Pashtun family home with washing on the line.`

#### Scene 059 · 06:01.9–06:07.6 (5.7 s) · ILLUS

**VO:** "Meanwhile, year after year, the CIA tried everything. In Pakistan's tribal areas,"

- **Visual:** A dusty bazaar in the tribal areas; calendar pages flying past (2002 → 2008).
- **On-screen text:** YEAR AFTER YEAR
- **Camera / animation:** Calendar pages flip
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A dusty bazaar in the tribal areas; calendar pages flying past (2002 → 2008).`

#### Scene 060 · 06:07.6–06:14.5 (6.9 s) · ILLUS

**VO:** "matchboxes were printed with a reward of up to $25 million for information on bin Laden."

- **Visual:** Close on matchboxes printed with a reward notice; a hand picking one up.
- **On-screen text:** UP TO $25 MILLION
- **Camera / animation:** Counter rolls; push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Close on matchboxes printed with a reward notice; a hand picking one up.`

#### Scene 061 · 06:14.5–06:21.0 (6.5 s) · ILLUS

**VO:** "There were even claims of secret tracking chips planted in phones and computers sold in the region."

- **Visual:** A phone stall in the bazaar: phones and laptops on display, one with a tiny glowing chip (marked "CLAIM").
- **On-screen text:** TRACKING CHIPS? (CLAIMS)
- **Camera / animation:** Push-in on the chip
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A phone stall in the bazaar: phones and laptops on display, one with a tiny glowing chip (marked "CLAIM").`

#### Scene 062 · 06:21.0–06:25.7 (4.7 s) · ILLUS

**VO:** "But none of it worked. Bin Laden had given up electronics completely."

- **Visual:** The phone stall's goods with a big red X; the tall silhouette's room with no electronics, only paper.
- **On-screen text:** NONE OF IT WORKED
- **Camera / animation:** Stamp X
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The phone stall's goods with a big red X; the tall silhouette's room with no electronics, only paper.`

#### Scene 063 · 06:25.7–06:32.7 (7.0 s) · ILLUS

**VO:** "In 2009, the CIA played another card. Humam al-Balawi, also known as Abu Dujana,"

- **Visual:** A calendar 2009 on a wall; an interrogation room with a Jordanian doctor at the table.
- **On-screen text:** 2009 / HUMAM AL-BALAWI
- **Camera / animation:** Calendar flip; push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A calendar 2009 on a wall; an interrogation room with a Jordanian doctor at the table.`

#### Scene 064 · 06:32.7–06:38.8 (6.1 s) · ILLUS

**VO:** "was a Jordanian doctor arrested over his al-Qaeda links. Jordanian intelligence,"

- **Visual:** The doctor in a white coat; two handlers across the table (Jordanian and American).
- **On-screen text:** A JORDANIAN DOCTOR
- **Camera / animation:** Slow pan
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The doctor in a white coat; two handlers across the table (Jordanian and American).`

#### Scene 065 · 06:38.8–06:44.9 (6.1 s) · ILLUS

**VO:** "working with the CIA, made him an offer: become our double agent, lead us to al-Qaeda's leaders,"

- **Visual:** A handler slides a document across the table: OFFER.
- **On-screen text:** "BECOME OUR DOUBLE AGENT"
- **Camera / animation:** Push-in on the paper
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A handler slides a document across the table: OFFER.`

#### Scene 066 · 06:44.9–06:52.0 (7.1 s) · ILLUS

**VO:** "and walk free. … Balawi said yes. He was given brief training. Then word was spread that he had escaped."

- **Visual:** The doctor signing; then a newspaper headline "PRISONER ESCAPES".
- **On-screen text:** THE COVER STORY
- **Camera / animation:** Cut to the paper
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The doctor signing; then a newspaper headline "PRISONER ESCAPES".`

#### Scene 067 · 06:52.0–06:57.7 (5.7 s) · ILLUS

**VO:** "Balawi won al-Qaeda's trust. He kept passing small pieces of inside information."

- **Visual:** The doctor among fighters in a mountain camp, carrying a medical bag.
- **On-screen text:** INSIDE AL-QAEDA
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The doctor among fighters in a mountain camp, carrying a medical bag.`

#### Scene 068 · 06:57.7–07:03.3 (5.6 s) · ILLUS

**VO:** "He even claimed he had been asked to treat al-Qaeda's number two, Ayman al-Zawahiri."

- **Visual:** A tent; the doctor opening his bag beside a cot (patient hidden behind a curtain).
- **On-screen text:** AYMAN AL-ZAWAHIRI?
- **Camera / animation:** Push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A tent; the doctor opening his bag beside a cot (patient hidden behind a curtain).`

#### Scene 069 · 07:03.3–07:09.0 (5.7 s) · ILLUS

**VO:** "Everything seemed to be working. … Then he messaged the CIA on a secure network."

- **Visual:** A laptop in a hut showing a secure messaging window.
- **On-screen text:** A SECURE MESSAGE
- **Camera / animation:** Push-in on the screen
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A laptop in a hut showing a secure messaging window.`

#### Scene 070 · 07:09.0–07:14.8 (5.8 s) · ILLUS

**VO:** "I've learned something huge, he said — something that can get you to al-Qaeda's top leadership."

- **Visual:** The message on screen; CIA officers at headquarters leaning in.
- **On-screen text:** "SOMETHING HUGE"
- **Camera / animation:** Cross-cut
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The message on screen; CIA officers at headquarters leaning in.`

#### Scene 071 · 07:14.8–07:23.3 (8.5 s) · ILLUS

**VO:** "I can't say it on the phone. I'll tell you in person. … The CIA was thrilled. On December 30, 2009,"

- **Visual:** A smiling officer circling a date on a calendar: DECEMBER 30, 2009.
- **On-screen text:** "IN PERSON" / DECEMBER 30, 2009
- **Camera / animation:** Calendar push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A smiling officer circling a date on a calendar: DECEMBER 30, 2009.`

#### Scene 072 · 07:23.3–07:30.9 (7.6 s) · MAP

**VO:** "Balawi was invited to Camp Chapman in Afghanistan's Khost province, one of the CIA's most secure bases."

- **Visual:** Paper map of Afghanistan: red pin KHOST · CAMP CHAPMAN.
- **On-screen text:** CAMP CHAPMAN
- **Camera / animation:** Zoom in
- **Image prompt:** `Dark intelligence-style map: near-black sea, dark slate land, thin blue-grey borders, the featured country lit amber with a glowing edge, red pins with pulsing rings and white condensed labels, faint grid, film grain. Paper map of Afghanistan: red pin KHOST · CAMP CHAPMAN.`

#### Scene 073 · 07:30.9–07:38.9 (7.9 s) · ILLUS

**VO:** "It was his birthday that week, and the team had even arranged a surprise cake. Senior CIA officers were there to meet him."

- **Visual:** Inside the base: a table with a birthday cake and candles; officers waiting.
- **On-screen text:** A SURPRISE CAKE
- **Camera / animation:** Slow push on the cake
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Inside the base: a table with a birthday cake and candles; officers waiting.`

#### Scene 074 · 07:38.9–07:46.0 (7.1 s) · ILLUS

**VO:** "Balawi arrived at the gate. At the first checkpoint, no search — the CIA had said not to. At the second,"

- **Visual:** A car rolling through the first checkpoint unsearched; a guard waving it on.
- **On-screen text:** NO SEARCH
- **Camera / animation:** Pan with the car
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A car rolling through the first checkpoint unsearched; a guard waving it on.`

#### Scene 075 · 07:46.0–07:52.4 (6.5 s) · ILLUS

**VO:** "no search either. He walked straight in, stood among the officers, and in the next moment he blew himself up."

- **Visual:** Officers gathered around a car; a white flash fills the frame (no bodies shown).
- **On-screen text:** (silence)
- **Camera / animation:** White flash, cut to black
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Officers gathered around a car; a white flash fills the frame (no bodies shown).`

#### Scene 076 · 07:52.4–08:00.0 (7.6 s) · TITLE

**VO:** "Seven CIA officers were killed, along with a Jordanian intelligence officer and an Afghan driver."

- **Visual:** Black screen; seven small stars appear one by one, then two more in grey.
- **On-screen text:** 7 CIA OFFICERS
- **Camera / animation:** Stars fade in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Black screen; seven small stars appear one by one, then two more in grey.`

#### Scene 077 · 08:00.0–08:06.3 (6.2 s) · TITLE

**VO:** "It was the CIA's deadliest day in decades. Balawi had never been the CIA's double agent."

- **Visual:** Memorial wall with stars engraved (CIA style); title.
- **On-screen text:** THE CIA'S DEADLIEST DAY IN DECADES
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Memorial wall with stars engraved (CIA style); title.`

#### Scene 078 · 08:06.3–08:13.9 (7.6 s) · ILLUS

**VO:** "He was al-Qaeda's triple agent, and the CIA itself was the target. … The hunt slowed down even more,"

- **Visual:** A chess board: a black knight that turns out to be a different colour underneath.
- **On-screen text:** A TRIPLE AGENT
- **Camera / animation:** Push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A chess board: a black knight that turns out to be a different colour underneath.`

#### Scene 079 · 08:13.9–08:20.1 (6.2 s) · ILLUS

**VO:** "and new CIA leadership had to step in. On the other side, bin Laden's own health was a worry."

- **Visual:** Empty desks at CIA headquarters; then an older, frail tall figure resting indoors, face in shadow.
- **On-screen text:** NEW LEADERSHIP / FAILING HEALTH
- **Camera / animation:** Cross-fade
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Empty desks at CIA headquarters; then an older, frail tall figure resting indoors, face in shadow.`

#### Scene 080 · 08:20.1–08:25.4 (5.4 s) · ILLUS

**VO:** "He was said to have kidney disease, and some reports claimed he needed dialysis."

- **Visual:** A medical kit and a dialysis-style machine beside a bed in a dim room (no face).
- **On-screen text:** KIDNEY DISEASE?
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A medical kit and a dialysis-style machine beside a bed in a dim room (no face).`

#### Scene 081 · 08:25.4–08:31.7 (6.3 s) · ILLUS

**VO:** "Al-Qaeda needed somewhere safe and permanent for him — and years earlier, they had already found it."

- **Visual:** A hand drawing a circle on a map with a red pen.
- **On-screen text:** A SAFE, PERMANENT HOME
- **Camera / animation:** Push-in on the circle
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A hand drawing a circle on a map with a red pen.`

### Part 3 — Abbottabad

#### Scene 082 · 08:31.7–08:38.4 (6.6 s) · ILLUS

**VO:** "Abbottabad. Home of the Pakistan Military Academy at Kakul — Pakistan's West Point."

- **Visual:** Green hills of Abbottabad; cadets marching at the Kakul military academy gate.
- **On-screen text:** ABBOTTABAD / PAKISTAN'S WEST POINT
- **Camera / animation:** Slow pan
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Green hills of Abbottabad; cadets marching at the Kakul military academy gate.`

#### Scene 083 · 08:38.4–08:45.4 (7.1 s) · MAP

**VO:** "Just a short distance away, in Bilal Town, a plot of land was up for sale. Al-Qaeda's logic was simple:"

- **Visual:** Paper map of Abbottabad town: pins KAKUL ACADEMY and BILAL TOWN; a FOR SALE sign on a plot.
- **On-screen text:** BILAL TOWN
- **Camera / animation:** Zoom in
- **Image prompt:** `Dark intelligence-style map: near-black sea, dark slate land, thin blue-grey borders, the featured country lit amber with a glowing edge, red pins with pulsing rings and white condensed labels, faint grid, film grain. Paper map of Abbottabad town: pins KAKUL ACADEMY and BILAL TOWN; a FOR SALE sign on a plot.`

#### Scene 084 · 08:45.4–08:52.0 (6.5 s) · TITLE

**VO:** "nobody would imagine the world's most wanted man living right next to a military academy."

- **Visual:** Yellow comic title over the academy gate.
- **On-screen text:** NEXT TO THE ARMY
- **Camera / animation:** Title slam
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Yellow comic title over the academy gate.`

#### Scene 085 · 08:52.0–08:57.7 (5.7 s) · ILLUS

**VO:** "Abrar was sent with a fake ID and cash. He bought the 38,000-square-foot plot."

- **Visual:** A man counting cash at a property office; a fake ID card on the desk.
- **On-screen text:** A FAKE ID AND CASH / 38,000 SQ FT
- **Camera / animation:** Push-in on the cash
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A man counting cash at a property office; a fake ID card on the desk.`

#### Scene 086 · 08:57.7–09:03.2 (5.5 s) · ILLUS

**VO:** "A local architect, Mohammad Younis, was hired, and the design was unusual."

- **Visual:** An architect's desk; the name card MOHAMMAD YOUNIS; a pencil sketch of a house.
- **On-screen text:** THE ARCHITECT
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. An architect's desk; the name card MOHAMMAD YOUNIS; a pencil sketch of a house.`

#### Scene 087 · 09:03.2–09:09.8 (6.5 s) · ILLUS

**VO:** "Concrete walls up to 18 feet high, topped with barbed wire. No windows on the top floor."

- **Visual:** The sketch turning into a walled three-storey compound; labels on the walls.
- **On-screen text:** 18-FOOT WALLS · BARBED WIRE / NO WINDOWS UPSTAIRS
- **Camera / animation:** Sketch-to-color wipe
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The sketch turning into a walled three-storey compound; labels on the walls.`

#### Scene 088 · 09:09.8–09:15.4 (5.6 s) · ILLUS

**VO:** "A 7-foot wall around the balcony so nobody could look in. And only one way in."

- **Visual:** Close on the top balcony with its 7-foot privacy wall; one gate highlighted.
- **On-screen text:** 7-FOOT WALL · ONE WAY IN
- **Camera / animation:** Push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Close on the top balcony with its 7-foot privacy wall; one gate highlighted.`

#### Scene 089 · 09:15.4–09:21.7 (6.3 s) · ILLUS

**VO:** "By 2006, the house was ready. Bin Laden, Ibrahim and Abrar moved in with their families."

- **Visual:** Calendar 2006; families arriving at the compound gate with bundles.
- **On-screen text:** 2006 · THEY MOVE IN
- **Camera / animation:** Calendar flip; pan
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Calendar 2006; families arriving at the compound gate with bundles.`

#### Scene 090 · 09:21.7–09:28.9 (7.2 s) · ILLUS

**VO:** "From the outside, nobody could tell. For five years, no one found out. Then, on August 27, 2010,"

- **Visual:** The compound from the street: ordinary neighbours walking past. Calendar AUGUST 27, 2010.
- **On-screen text:** 5 YEARS / AUGUST 27, 2010
- **Camera / animation:** Calendar flip
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The compound from the street: ordinary neighbours walking past. Calendar AUGUST 27, 2010.`

#### Scene 091 · 09:28.9–09:35.0 (6.0 s) · MAP

**VO:** "one small mistake changed everything. … Ibrahim had to go to Peshawar for some work."

- **Visual:** Paper map: a line from ABBOTTABAD to PESHAWAR.
- **On-screen text:** PESHAWAR
- **Camera / animation:** Line draws on
- **Image prompt:** `Dark intelligence-style map: near-black sea, dark slate land, thin blue-grey borders, the featured country lit amber with a glowing edge, red pins with pulsing rings and white condensed labels, faint grid, film grain. Paper map: a line from ABBOTTABAD to PESHAWAR.`

#### Scene 092 · 09:35.0–09:41.2 (6.2 s) · ILLUS

**VO:** "Peshawar's entire mobile network was under CIA surveillance — and Ibrahim knew it. That's why,"

- **Visual:** A crowded Peshawar street; phone towers on rooftops with faint signal rings (surveillance).
- **On-screen text:** UNDER SURVEILLANCE
- **Camera / animation:** Slow pan
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A crowded Peshawar street; phone towers on rooftops with faint signal rings (surveillance).`

#### Scene 093 · 09:41.2–09:47.9 (6.7 s) · ILLUS

**VO:** "in Peshawar, he always used secure methods. But that day, he got careless. Standing in a public place,"

- **Visual:** The courier in the crowd, glancing around.
- **On-screen text:** HE GOT CARELESS
- **Camera / animation:** Push-in on him
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The courier in the crowd, glancing around.`

#### Scene 094 · 09:47.9–09:53.4 (5.5 s) · ILLUS

**VO:** "he used his personal phone and spoke to an al-Qaeda member for just a few seconds."

- **Visual:** The courier lifting a personal phone to his ear; a signal ring radiates from it.
- **On-screen text:** A FEW SECONDS
- **Camera / animation:** Push-in on the phone
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The courier lifting a personal phone to his ear; a signal ring radiates from it.`

#### Scene 095 · 09:53.4–09:59.7 (6.3 s) · ILLUS

**VO:** "That was all it took. That was the phone call bin Laden never made — and it would cost him everything."

- **Visual:** A screen at a CIA station lighting up with a red location dot.
- **On-screen text:** THE CALL HE NEVER MADE
- **Camera / animation:** Push-in; pulse
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A screen at a CIA station lighting up with a red location dot.`

#### Scene 096 · 09:59.7–10:05.7 (6.0 s) · ILLUS

**VO:** "The CIA locked onto his live location. Agents reached the spot, but they didn't arrest him."

- **Visual:** Agents in plain clothes watching from a parked car across the street.
- **On-screen text:** THEY FOLLOWED HIM
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Agents in plain clothes watching from a parked car across the street.`

#### Scene 097 · 10:05.7–10:11.0 (5.3 s) · ILLUS

**VO:** "They followed him. A white Suzuki jeep, with a rhino on the spare-tyre cover."

- **Visual:** A white Suzuki jeep with a rhino on its spare-tyre cover driving out of the city; an unmarked car trailing.
- **On-screen text:** THE WHITE SUZUKI
- **Camera / animation:** Pan with the jeep
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A white Suzuki jeep with a rhino on its spare-tyre cover driving out of the city; an unmarked car trailing.`

#### Scene 098 · 10:11.0–10:17.9 (6.8 s) · ILLUS

**VO:** "Ibrahim drove it all the way to Bilal Town in Abbottabad, and through the gate of a large compound."

- **Visual:** The jeep turning through the steel gate of a large walled compound in Bilal Town.
- **On-screen text:** BILAL TOWN, ABBOTTABAD
- **Camera / animation:** Push-in on the gate
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The jeep turning through the steel gate of a large walled compound in Bilal Town.`

#### Scene 099 · 10:17.9–10:25.2 (7.4 s) · ILLUS

**VO:** "The agents waited outside. When they took a proper look at the compound, they were stunned. 38,000 square feet."

- **Visual:** Wide shot of the high-walled compound; agents watching from a distance.
- **On-screen text:** 38,000 SQ FT
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Wide shot of the high-walled compound; agents watching from a distance.`

#### Scene 100 · 10:25.2–10:32.1 (6.9 s) · ILLUS

**VO:** "18-foot walls. Barbed wire. No windows upstairs. A 7-foot wall on the balcony."

- **Visual:** Labels pop on the compound: 18-FT WALLS, BARBED WIRE, NO WINDOWS, 7-FT BALCONY WALL.
- **On-screen text:** 18-FOOT WALLS / BARBED WIRE
- **Camera / animation:** Labels pop
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Labels pop on the compound: 18-FT WALLS, BARBED WIRE, NO WINDOWS, 7-FT BALCONY WALL.`

#### Scene 101 · 10:32.1–10:39.8 (7.7 s) · ILLUS

**VO:** "At first, the CIA thought bin Laden couldn't be here. So close to a military academy? He'd never take that risk."

- **Visual:** CIA officers around a table shaking heads; a photo of the academy pinned next to the compound photo.
- **On-screen text:** "HE'D NEVER TAKE THAT RISK"
- **Camera / animation:** Push-in on the photos
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. CIA officers around a table shaking heads; a photo of the academy pinned next to the compound photo.`

#### Scene 102 · 10:39.8–10:46.2 (6.5 s) · ILLUS

**VO:** "Maybe this compound belonged to another high-value target — someone who could lead them to bin Laden."

- **Visual:** A question mark over the compound photo; another silhouette card labelled HVT?
- **On-screen text:** ANOTHER TARGET?
- **Camera / animation:** Push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A question mark over the compound photo; another silhouette card labelled HVT?`

#### Scene 103 · 10:46.2–10:53.0 (6.7 s) · ILLUS

**VO:** "Over the next weeks, the CIA watched closely. They contacted a retired Pakistani army officer,"

- **Visual:** Surveillance photos of the compound pinned in rows.
- **On-screen text:** WATCHED CLOSELY
- **Camera / animation:** Pan
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Surveillance photos of the compound pinned in rows.`

#### Scene 104 · 10:53.0–11:00.2 (7.2 s) · ILLUS

**VO:** "Lieutenant Colonel Syed Iqbal. His friend Dr. Amir Aziz lived just 80 yards from the compound."

- **Visual:** Name cards: LT. COL. SYED IQBAL and DR. AMIR AZIZ; a house 80 yards from the compound.
- **On-screen text:** 80 YARDS AWAY
- **Camera / animation:** Pan between cards
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Name cards: LT. COL. SYED IQBAL and DR. AMIR AZIZ; a house 80 yards from the compound.`

#### Scene 105 · 11:00.2–11:05.0 (4.8 s) · ILLUS

**VO:** "Iqbal visited Aziz, went up to the roof on the excuse of meeting the dog,"

- **Visual:** A rooftop at dusk: a man playing with a dog.
- **On-screen text:** "MEETING THE DOG"
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A rooftop at dusk: a man playing with a dog.`

#### Scene 106 · 11:05.0–11:11.2 (6.1 s) · ILLUS

**VO:** "and took several photos of the compound. … The CIA rented a place about a mile away"

- **Visual:** The man lifting a camera and photographing the compound over the parapet.
- **On-screen text:** PHOTOS FROM A ROOFTOP
- **Camera / animation:** Camera flash
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The man lifting a camera and photographing the compound over the parapet.`

#### Scene 107 · 11:11.2–11:17.4 (6.2 s) · ILLUS

**VO:** "and turned it into a secret base. Agents drove there every day in a quiet, unmarked car."

- **Visual:** A rented house about a mile away; a quiet grey car parked outside.
- **On-screen text:** A SECRET BASE, 1 MILE AWAY
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A rented house about a mile away; a quiet grey car parked outside.`

#### Scene 108 · 11:17.4–11:23.3 (5.9 s) · ILLUS

**VO:** "Infrared and night-vision cameras went up. Listening devices were hidden in the trees nearby."

- **Visual:** A room full of monitors with night-vision feeds; a tiny listening device hidden in a tree.
- **On-screen text:** INFRARED · NIGHT VISION · BUGS
- **Camera / animation:** Pan across the monitors
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A room full of monitors with night-vision feeds; a tiny listening device hidden in a tree.`

#### Scene 109 · 11:23.3–11:30.2 (6.9 s) · ILLUS

**VO:** "Every movement, day and night, was recorded. When they ate. When they slept. When they came outside."

- **Visual:** A log book filling with times: EAT 19:10, SLEEP 23:40, OUTSIDE 07:15.
- **On-screen text:** EVERY MOVEMENT RECORDED
- **Camera / animation:** Pan down the log
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A log book filling with times: EAT 19:10, SLEEP 23:40, OUTSIDE 07:15.`

#### Scene 110 · 11:30.2–11:36.9 (6.6 s) · ILLUS

**VO:** "Slowly, a picture formed. Twenty to twenty-two people lived in the compound. And most importantly:"

- **Visual:** A counter of people icons fills to 20–22 over the compound plan.
- **On-screen text:** 20–22 PEOPLE
- **Camera / animation:** Icons pop
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A counter of people icons fills to 20–22 over the compound plan.`

#### Scene 111 · 11:36.9–11:42.9 (6.0 s) · ILLUS

**VO:** "every day, a tall man came out onto the top-floor balcony and walked quickly back and forth."

- **Visual:** Overhead view of the balcony: a tall figure pacing back and forth (seen from above, face hidden).
- **On-screen text:** THE PACER
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Overhead view of the balcony: a tall figure pacing back and forth (seen from above, face hidden).`

#### Scene 112 · 11:42.9–11:48.3 (5.4 s) · ILLUS

**VO:** "Then he went inside. His face never showed — only his shadow on the balcony wall."

- **Visual:** Only a long shadow moving along the balcony wall.
- **On-screen text:** ONLY HIS SHADOW
- **Camera / animation:** Shadow moves
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Only a long shadow moving along the balcony wall.`

#### Scene 113 · 11:48.3–11:55.2 (6.9 s) · ILLUS

**VO:** "A CIA analyst team led by Gina Bennett measured that shadow against the wall and wrote a report."

- **Visual:** Analysts measuring the shadow on a printed photo with rulers; name card GINA BENNETT.
- **On-screen text:** MEASURING A SHADOW
- **Camera / animation:** Push-in on the ruler
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Analysts measuring the shadow on a printed photo with rulers; name card GINA BENNETT.`

#### Scene 114 · 11:55.2–12:02.1 (6.9 s) · ILLUS

**VO:** "The man was somewhere between 5 feet 5 inches and 6 feet 8 inches tall. A huge range."

- **Visual:** A height chart from 5'5" to 6'8" with a big bracket.
- **On-screen text:** 5'5" – 6'8"
- **Camera / animation:** Bracket draws
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A height chart from 5'5" to 6'8" with a big bracket.`

#### Scene 115 · 12:02.1–12:08.5 (6.4 s) · ILLUS

**VO:** "But one thing was clear: he was the head of the compound. He never lifted a finger to help with any work."

- **Visual:** The pacer card stamped HEAD OF THE COMPOUND; others working in the yard while he walks.
- **On-screen text:** NEVER LIFTED A FINGER
- **Camera / animation:** Stamp
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The pacer card stamped HEAD OF THE COMPOUND; others working in the yard while he walks.`

#### Scene 116 · 12:08.5–12:16.5 (8.0 s) · ILLUS

**VO:** "The CIA drew up several plans to confirm it with DNA. One was to tunnel underground to the compound's sewage"

- **Visual:** A cutaway: a tunnel creeping under the wall toward a sewage line.
- **On-screen text:** THE SEWAGE PLAN
- **Camera / animation:** Tunnel draws on
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A cutaway: a tunnel creeping under the wall toward a sewage line.`

#### Scene 117 · 12:16.5–12:22.5 (6.0 s) · ILLUS

**VO:** "and take DNA from human waste. The CIA already had DNA from bin Laden's family —"

- **Visual:** A DNA helix next to a sample tube; a family tree sprouting branches.
- **On-screen text:** DNA FROM THE FAMILY
- **Camera / animation:** Tree grows
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A DNA helix next to a sample tube; a family tree sprouting branches.`

#### Scene 118 · 12:22.5–12:30.6 (8.1 s) · ILLUS

**VO:** "his father had married 22 times and had 56 children. But that much digging would tip off the people inside."

- **Visual:** A huge family tree: 22 marriages, 56 children; then a red X over the tunnel.
- **On-screen text:** 22 MARRIAGES · 56 CHILDREN
- **Camera / animation:** Tree fills; X stamps
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A huge family tree: 22 marriages, 56 children; then a red X over the tunnel.`

#### Scene 119 · 12:30.6–12:36.1 (5.4 s) · ILLUS

**VO:** "The plan was dropped. … The second plan was Dr. Shakil Afridi."

- **Visual:** Plan stamped DROPPED; a name card DR. SHAKIL AFRIDI.
- **On-screen text:** PLAN 2: DR. SHAKIL AFRIDI
- **Camera / animation:** Stamp; card slides in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Plan stamped DROPPED; a name card DR. SHAKIL AFRIDI.`

#### Scene 120 · 12:36.1–12:44.9 (8.8 s) · ILLUS

**VO:** "A covert CIA operative approached this local Abbottabad doctor about a hepatitis B vaccination drive for children."

- **Visual:** A clinic office: a man in a suit talking to a doctor with a clipboard; a poster "HEPATITIS B VACCINATION".
- **On-screen text:** A FAKE VACCINE DRIVE
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A clinic office: a man in a suit talking to a doctor with a clipboard; a poster "HEPATITIS B VACCINATION".`

#### Scene 121 · 12:44.9–12:52.4 (7.5 s) · ILLUS

**VO:** "The real goal was to vaccinate the children inside the compound and collect their DNA. … Dr."

- **Visual:** A vaccine cool box opened to show swab kits labelled DNA.
- **On-screen text:** THE REAL GOAL: DNA
- **Camera / animation:** Push-in on the kits
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A vaccine cool box opened to show swab kits labelled DNA.`

#### Scene 122 · 12:52.4–12:59.5 (7.1 s) · ILLUS

**VO:** "Afridi was paid $55,000. He hired nurses and health workers from Ayub Medical College."

- **Visual:** An envelope of cash ($55,000); nurses in uniforms from Ayub Medical College.
- **On-screen text:** $55,000
- **Camera / animation:** Counter rolls
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. An envelope of cash ($55,000); nurses in uniforms from Ayub Medical College.`

#### Scene 123 · 12:59.5–13:06.3 (6.9 s) · MAP

**VO:** "The drive started in Nawansher and worked its way toward Bilal Town. … When they reached the compound's gate"

- **Visual:** Map of Abbottabad: a dotted path of door icons from NAWANSHER to BILAL TOWN.
- **On-screen text:** NAWANSHER → BILAL TOWN
- **Camera / animation:** Path draws on
- **Image prompt:** `Dark intelligence-style map: near-black sea, dark slate land, thin blue-grey borders, the featured country lit amber with a glowing edge, red pins with pulsing rings and white condensed labels, faint grid, film grain. Map of Abbottabad: a dotted path of door icons from NAWANSHER to BILAL TOWN.`

#### Scene 124 · 13:06.3–13:12.3 (5.9 s) · ILLUS

**VO:** "and rang the bell, Ibrahim came out and sent them all away. They tried again and again by phone."

- **Visual:** The compound's steel gate; a health worker ringing the bell; a man waving them away.
- **On-screen text:** SENT AWAY
- **Camera / animation:** Push-in on the gate
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The compound's steel gate; a health worker ringing the bell; a man waving them away.`

#### Scene 125 · 13:12.3–13:20.0 (7.7 s) · ILLUS

**VO:** "Nothing worked. … That plan failed too. Pakistan later jailed Dr. Afridi for 33 years"

- **Visual:** A phone ringing unanswered on a table; then a red FAILED stamp.
- **On-screen text:** PLAN 2 FAILED / 33 YEARS
- **Camera / animation:** Stamp; counter
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A phone ringing unanswered on a table; then a red FAILED stamp.`

#### Scene 126 · 13:20.0–13:26.2 (6.1 s) · ILLUS

**VO:** "— later cut to 23 — in a case widely seen as punishment for helping the CIA."

- **Visual:** A prison cell door closing; a calendar with "33 → 23".
- **On-screen text:** CUT TO 23 YEARS
- **Camera / animation:** Door closes
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A prison cell door closing; a calendar with "33 → 23".`

#### Scene 127 · 13:26.2–13:33.7 (7.5 s) · ILLUS

**VO:** "He is still in prison. … While the CIA kept failing, another story was playing out inside the compound."

- **Visual:** The prison wall; then the compound at night with one lit window.
- **On-screen text:** STILL IN PRISON
- **Camera / animation:** Cross-fade
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The prison wall; then the compound at night with one lit window.`

#### Scene 128 · 13:33.7–13:39.8 (6.2 s) · ILLUS

**VO:** "Ibrahim had cancer. Abrar was depressed. After years of this life, both were exhausted."

- **Visual:** A dim room inside the house: two tired brothers sitting on cushions; medicine bottles.
- **On-screen text:** CANCER · DEPRESSION
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A dim room inside the house: two tired brothers sitting on cushions; medicine bottles.`

#### Scene 129 · 13:39.8–13:47.3 (7.5 s) · ILLUS

**VO:** "They went to bin Laden and said: we can't do this any longer. … Bin Laden listened. Then he said: fine."

- **Visual:** The brothers speaking to a tall seated figure in shadow.
- **On-screen text:** "WE CAN'T DO THIS ANY LONGER"
- **Camera / animation:** Push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The brothers speaking to a tall seated figure in shadow.`

#### Scene 130 · 13:47.3–13:52.9 (5.6 s) · ILLUS

**VO:** "September 11, 2011 is the tenth anniversary of 9/11."

- **Visual:** A calendar circled SEPTEMBER 11, 2011.
- **On-screen text:** THE 10TH ANNIVERSARY
- **Camera / animation:** Circle draws
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A calendar circled SEPTEMBER 11, 2011.`

#### Scene 131 · 13:52.9–13:59.4 (6.6 s) · ILLUS

**VO:** "Just stay until then. After that, buy yourselves a retirement home in Jeddah. I'll leave this place too,"

- **Visual:** A postcard of Jeddah with a seaside house; a packed suitcase.
- **On-screen text:** A RETIREMENT HOME IN JEDDAH
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A postcard of Jeddah with a seaside house; a packed suitcase.`

#### Scene 132 · 13:59.4–14:07.1 (7.7 s) · ILLUS

**VO:** "and we'll sell the compound. … That meant only a few months were left. The CIA sensed it too: if they didn't move soon,"

- **Visual:** A SOLD sign over the compound; an hourglass running low.
- **On-screen text:** ONLY A FEW MONTHS LEFT
- **Camera / animation:** Hourglass flips
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A SOLD sign over the compound; an hourglass running low.`

#### Scene 133 · 14:07.1–14:13.8 (6.6 s) · ILLUS

**VO:** "bin Laden could vanish again. … By December 2010, CIA analyst Gina Bennett"

- **Visual:** CIA analysts around a table at night; calendar DECEMBER 2010.
- **On-screen text:** DECEMBER 2010
- **Camera / animation:** Calendar flip
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. CIA analysts around a table at night; calendar DECEMBER 2010.`

### Part 4 — Neptune Spear

#### Scene 134 · 14:13.8–14:20.7 (7.0 s) · ILLUS

**VO:** "and her team had prepared a very special document, called Sensitive Site Exploitation — SSE."

- **Visual:** A thick dossier stamped SSE — SENSITIVE SITE EXPLOITATION.
- **On-screen text:** SENSITIVE SITE EXPLOITATION
- **Camera / animation:** Push-in on the cover
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A thick dossier stamped SSE — SENSITIVE SITE EXPLOITATION.`

#### Scene 135 · 14:20.7–14:28.3 (7.5 s) · ILLUS

**VO:** "It had a floor-by-floor layout of the compound. Where the stairs were. How many steps. Where the car was parked."

- **Visual:** Floor plans pinned to a board: stairs, steps counted, parking spot.
- **On-screen text:** FLOOR BY FLOOR
- **Camera / animation:** Pan across the plans
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Floor plans pinned to a board: stairs, steps counted, parking spot.`

#### Scene 136 · 14:28.3–14:34.7 (6.5 s) · ILLUS

**VO:** "The height of every wall, from every angle. … Every resident had a card: bin Laden, Ibrahim,"

- **Visual:** Wall heights drawn from every angle; resident cards pinned: BIN LADEN, IBRAHIM.
- **On-screen text:** EVERY WALL · EVERY RESIDENT
- **Camera / animation:** Cards pop
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Wall heights drawn from every angle; resident cards pinned: BIN LADEN, IBRAHIM.`

#### Scene 137 · 14:34.7–14:42.2 (7.4 s) · ILLUS

**VO:** "Abrar — floor, height, schedule, everything. Gina Bennett was 100% sure. Bin Laden was there."

- **Visual:** Cards: ABRAR (floor, height, schedule); the analyst's notebook "100% SURE".
- **On-screen text:** 100% SURE
- **Camera / animation:** Push-in on the note
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Cards: ABRAR (floor, height, schedule); the analyst's notebook "100% SURE".`

#### Scene 138 · 14:42.2–14:48.0 (5.8 s) · ILLUS

**VO:** "The next step was the President. CIA Director Leon Panetta, Admiral William McRaven,"

- **Visual:** The White House Situation Room: officials around a long table (generic likenesses, no portraits).
- **On-screen text:** THE PRESIDENT
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The White House Situation Room: officials around a long table (generic likenesses, no portraits).`

#### Scene 139 · 14:48.0–14:54.6 (6.6 s) · ILLUS

**VO:** "Chairman of the Joint Chiefs Admiral Mike Mullen, Vice Chairman General James Cartwright, and Michael Vickers,"

- **Visual:** Name cards on the table: PANETTA · MCRAVEN · MULLEN · CARTWRIGHT · VICKERS.
- **On-screen text:** THE TEAM
- **Camera / animation:** Cards pop
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Name cards on the table: PANETTA · MCRAVEN · MULLEN · CARTWRIGHT · VICKERS.`

#### Scene 140 · 14:54.6–15:01.3 (6.7 s) · ILLUS

**VO:** "a senior Pentagon counterterrorism official, all gathered in the White House Situation Room."

- **Visual:** Wide of the room, screens on the wall.
- **On-screen text:** THE SITUATION ROOM
- **Camera / animation:** Slow pan
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Wide of the room, screens on the wall.`

#### Scene 141 · 15:01.3–15:07.7 (6.3 s) · ILLUS

**VO:** "A 3D model of the compound, built with help from the National Geospatial-Intelligence Agency,"

- **Visual:** A detailed 3D model of the compound on the table.
- **On-screen text:** A 3D MODEL
- **Camera / animation:** Push-in on the model
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A detailed 3D model of the compound on the table.`

#### Scene 142 · 15:07.7–15:15.0 (7.3 s) · ILLUS

**VO:** "was placed in front of President Obama. … There were three options. One: send B-2 stealth bombers"

- **Visual:** Three face-down cards on the table; the first flips: a B-2 stealth bomber.
- **On-screen text:** OPTION 1: B-2 BOMBERS
- **Camera / animation:** Card flips
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Three face-down cards on the table; the first flips: a B-2 stealth bomber.`

#### Scene 143 · 15:15.0–15:23.4 (8.4 s) · ILLUS

**VO:** "and drop dozens of bombs. The whole compound, gone. But civilians could die, the DNA proof of bin Laden could be destroyed,"

- **Visual:** The bomber card; icons: civilians, DNA proof, Pakistan ties, world outrage, each with a warning sign.
- **On-screen text:** THE RISKS
- **Camera / animation:** Icons pop
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The bomber card; icons: civilians, DNA proof, Pakistan ties, world outrage, each with a warning sign.`

#### Scene 144 · 15:23.4–15:31.9 (8.5 s) · ILLUS

**VO:** "ties with Pakistan could collapse, and America would face outrage around the world. … Two: a precise drone strike."

- **Visual:** Second card flips: a drone.
- **On-screen text:** OPTION 2: DRONE STRIKE
- **Camera / animation:** Card flips
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Second card flips: a drone.`

#### Scene 145 · 15:31.9–15:39.6 (7.7 s) · ILLUS

**VO:** "But the chance of bin Laden escaping was high. … Three: Admiral McRaven's plan. Without telling Pakistan,"

- **Visual:** The drone card with a running figure icon; third card flips: a helicopter full of SEALs.
- **On-screen text:** HE COULD ESCAPE / OPTION 3: THE RAID
- **Camera / animation:** Card flips
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The drone card with a running figure icon; third card flips: a helicopter full of SEALs.`

#### Scene 146 · 15:39.6–15:45.9 (6.3 s) · ILLUS

**VO:** "a special team of Navy SEALs would enter the compound, identify bin Laden face to face,"

- **Visual:** The raid card: SEALs entering a compound silhouette.
- **On-screen text:** FACE TO FACE
- **Camera / animation:** Push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The raid card: SEALs entering a compound silhouette.`

#### Scene 147 · 15:45.9–15:52.9 (7.0 s) · ILLUS

**VO:** "kill him, and slip out quietly. … Obama thought it over for a while. Then he said yes to the third option."

- **Visual:** A hand placing a check mark on card 3.
- **On-screen text:** OBAMA: YES TO OPTION 3
- **Camera / animation:** Check stamps
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A hand placing a check mark on card 3.`

#### Scene 148 · 15:52.9–15:58.9 (5.9 s) · TITLE

**VO:** "The mission was named Operation Neptune Spear. Neptune, for the SEALs' roots in the sea. Spear,"

- **Visual:** A trident and a spear forming the words NEPTUNE SPEAR over a dark sea.
- **On-screen text:** OPERATION NEPTUNE SPEAR
- **Camera / animation:** Title slam
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A trident and a spear forming the words NEPTUNE SPEAR over a dark sea.`

#### Scene 149 · 15:58.9–16:05.7 (6.8 s) · ILLUS

**VO:** "for a precise and deadly strike. McRaven promised Obama that everything would be ready in three weeks."

- **Visual:** A calendar with three weeks crossed off.
- **On-screen text:** READY IN 3 WEEKS
- **Camera / animation:** Days crossed
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A calendar with three weeks crossed off.`

#### Scene 150 · 16:05.7–16:14.2 (8.5 s) · ILLUS

**VO:** "For the team, Red Squadron of SEAL Team Six was chosen — some of the most dangerous, best-trained commandos in the world."

- **Visual:** Commandos in a hangar checking gear (no faces, helmets and goggles).
- **On-screen text:** RED SQUADRON · SEAL TEAM SIX
- **Camera / animation:** Slow pan
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Commandos in a hangar checking gear (no faces, helmets and goggles).`

#### Scene 151 · 16:14.2–16:22.6 (8.4 s) · ILLUS

**VO:** "The helicopters would be flown by pilots of the US Army's 160th Special Operations Aviation Regiment,"

- **Visual:** Pilots in flight suits beside helicopters; patch "160th SOAR".
- **On-screen text:** THE NIGHT STALKERS
- **Camera / animation:** Push-in on the patch
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Pilots in flight suits beside helicopters; patch "160th SOAR".`

#### Scene 152 · 16:22.6–16:29.2 (6.6 s) · ILLUS

**VO:** "the Night Stalkers. Their speciality: flying into enemy territory at night, under the radar."

- **Visual:** A helicopter flying low through dark valleys under the radar.
- **On-screen text:** UNDER THE RADAR
- **Camera / animation:** Pan with the helicopter
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A helicopter flying low through dark valleys under the radar.`

#### Scene 153 · 16:29.2–16:34.5 (5.3 s) · ILLUS

**VO:** "Twenty-four operators were chosen. None of them was told who the real target was."

- **Visual:** 24 helmet icons in rows; a sealed envelope "TARGET: UNKNOWN".
- **On-screen text:** 24 OPERATORS
- **Camera / animation:** Icons pop
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. 24 helmet icons in rows; a sealed envelope "TARGET: UNKNOWN".`

#### Scene 154 · 16:34.5–16:39.0 (4.6 s) · MAP

**VO:** "Only that there was an operation on the Afghanistan–Pakistan border."

- **Visual:** Paper map: a vague circle on the Afghanistan–Pakistan border.
- **On-screen text:** "THE BORDER"
- **Camera / animation:** Circle draws
- **Image prompt:** `Dark intelligence-style map: near-black sea, dark slate land, thin blue-grey borders, the featured country lit amber with a glowing edge, red pins with pulsing rings and white condensed labels, faint grid, film grain. Paper map: a vague circle on the Afghanistan–Pakistan border.`

#### Scene 155 · 16:39.0–16:45.8 (6.8 s) · ILLUS

**VO:** "Two MH-60 Black Hawk stealth helicopters were specially modified. A lower heat signature."

- **Visual:** A sleek angular stealth Black Hawk in a dark hangar.
- **On-screen text:** MH-60 STEALTH BLACK HAWKS
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A sleek angular stealth Black Hawk in a dark hangar.`

#### Scene 156 · 16:45.8–16:53.0 (7.2 s) · ILLUS

**VO:** "Almost no sound. Nearly invisible to radar. Their design was so secret that it stayed classified."

- **Visual:** Heat and sound meters dropping; a CLASSIFIED stamp.
- **On-screen text:** NEARLY SILENT · CLASSIFIED
- **Camera / animation:** Meters drop; stamp
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Heat and sound meters dropping; a CLASSIFIED stamp.`

#### Scene 157 · 16:53.0–17:00.2 (7.2 s) · ILLUS

**VO:** "Three CH-47 Chinook helicopters were kept as backup. … Training began in North Carolina,"

- **Visual:** Three CH-47 Chinooks behind; then a North Carolina training field.
- **On-screen text:** 3 CHINOOKS AS BACKUP / NORTH CAROLINA
- **Camera / animation:** Pan; cut
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Three CH-47 Chinooks behind; then a North Carolina training field.`

#### Scene 158 · 17:00.2–17:06.4 (6.2 s) · ILLUS

**VO:** "then moved to a remote stretch of the Nevada desert, where a replica of the compound was built."

- **Visual:** A full-size mock compound in the Nevada desert.
- **On-screen text:** NEVADA DESERT
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A full-size mock compound in the Nevada desert.`

#### Scene 159 · 17:06.4–17:12.5 (6.2 s) · ILLUS

**VO:** "The team rehearsed there dozens of times. Every room, every door, every staircase — memorised."

- **Visual:** SEALs rehearsing room by room (silhouettes); a counter "x DOZENS".
- **On-screen text:** REHEARSED DOZENS OF TIMES
- **Camera / animation:** Fast cuts
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. SEALs rehearsing room by room (silhouettes); a counter "x DOZENS".`

#### Scene 160 · 17:12.5–17:21.7 (9.1 s) · ILLUS

**VO:** "But there was one mistake. The training compound had low walls and chain-link fencing. The real compound had 18-foot concrete walls."

- **Visual:** Split: low chain-link fence (training) vs 18-foot concrete wall (real).
- **On-screen text:** THE MISTAKE
- **Camera / animation:** Split wipe
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Split: low chain-link fence (training) vs 18-foot concrete wall (real).`

#### Scene 161 · 17:21.7–17:28.5 (6.9 s) · ILLUS

**VO:** "That difference would cost them later. … There was a backup plan for everything. What if bin Laden surrendered?"

- **Visual:** A white flag icon over the compound model.
- **On-screen text:** WHAT IF HE SURRENDERED?
- **Camera / animation:** Push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A white flag icon over the compound model.`

#### Scene 162 · 17:28.5–17:34.1 (5.5 s) · ILLUS

**VO:** "Under the laws of war, a man who surrenders cannot be killed. So a team of lawyers"

- **Visual:** A law book "LAWS OF WAR" with a gavel.
- **On-screen text:** LAWS OF WAR
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A law book "LAWS OF WAR" with a gavel.`

#### Scene 163 · 17:34.1–17:40.0 (6.0 s) · ILLUS

**VO:** "and interpreters waited on the aircraft carrier USS Carl Vinson in the Arabian Sea."

- **Visual:** The aircraft carrier USS Carl Vinson in the Arabian Sea; lawyers and interpreters on deck.
- **On-screen text:** USS CARL VINSON
- **Camera / animation:** Slow pan
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The aircraft carrier USS Carl Vinson in the Arabian Sea; lawyers and interpreters on deck.`

#### Scene 164 · 17:40.0–17:46.4 (6.4 s) · MAP

**VO:** "What if the SEALs got trapped in Pakistan? Two exit routes were ready — one toward the Indian border,"

- **Visual:** Paper map: two exit routes from Abbottabad — one toward the Indian border, one toward Karachi.
- **On-screen text:** TWO EXIT ROUTES
- **Camera / animation:** Lines draw on
- **Image prompt:** `Dark intelligence-style map: near-black sea, dark slate land, thin blue-grey borders, the featured country lit amber with a glowing edge, red pins with pulsing rings and white condensed labels, faint grid, film grain. Paper map: two exit routes from Abbottabad — one toward the Indian border, one toward Karachi.`

#### Scene 165 · 17:46.4–17:52.9 (6.5 s) · MAP

**VO:** "the other toward Karachi, near where the Carl Vinson was stationed. Even the media team was prepared."

- **Visual:** The Karachi route continuing to a carrier icon in the Arabian Sea.
- **On-screen text:** KARACHI · THE CARRIER
- **Camera / animation:** Line extends
- **Image prompt:** `Dark intelligence-style map: near-black sea, dark slate land, thin blue-grey borders, the featured country lit amber with a glowing edge, red pins with pulsing rings and white condensed labels, faint grid, film grain. The Karachi route continuing to a carrier icon in the Arabian Sea.`

#### Scene 166 · 17:52.9–18:00.0 (7.1 s) · ILLUS

**VO:** "What to say if bin Laden died. If he surrendered. If the mission failed. Every script was already written."

- **Visual:** Three press statements in folders: DEAD · SURRENDERED · FAILED.
- **On-screen text:** EVERY SCRIPT WRITTEN
- **Camera / animation:** Folders slide in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Three press statements in folders: DEAD · SURRENDERED · FAILED.`

#### Scene 167 · 18:00.0–18:06.2 (6.1 s) · MAP

**VO:** "April 26, 2011: the whole team reached Bagram Airfield in Afghanistan."

- **Visual:** Paper map: pin BAGRAM AIRFIELD; date stamp APRIL 26, 2011.
- **On-screen text:** APRIL 26, 2011 · BAGRAM
- **Camera / animation:** Stamp
- **Image prompt:** `Dark intelligence-style map: near-black sea, dark slate land, thin blue-grey borders, the featured country lit amber with a glowing edge, red pins with pulsing rings and white condensed labels, faint grid, film grain. Paper map: pin BAGRAM AIRFIELD; date stamp APRIL 26, 2011.`

#### Scene 168 · 18:06.2–18:12.7 (6.6 s) · MAP

**VO:** "One day of rest. April 27: they moved to Jalalabad Air Base and waited for orders."

- **Visual:** Pin JALALABAD; stamp APRIL 27.
- **On-screen text:** APRIL 27 · JALALABAD
- **Camera / animation:** Stamp
- **Image prompt:** `Dark intelligence-style map: near-black sea, dark slate land, thin blue-grey borders, the featured country lit amber with a glowing edge, red pins with pulsing rings and white condensed labels, faint grid, film grain. Pin JALALABAD; stamp APRIL 27.`

#### Scene 169 · 18:12.7–18:19.4 (6.6 s) · ILLUS

**VO:** "April 29, 2011, 8:20 in the morning: Obama gave the final go-ahead."

- **Visual:** A clock 8:20 and a calendar APRIL 29, 2011; a signed order.
- **On-screen text:** THE FINAL GO-AHEAD
- **Camera / animation:** Calendar flip
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A clock 8:20 and a calendar APRIL 29, 2011; a signed order.`

#### Scene 170 · 18:19.4–18:24.9 (5.5 s) · ILLUS

**VO:** "The date was set for April 30. But that day, the weather turned — thick cloud and fog."

- **Visual:** Fog rolling over the Jalalabad airfield; helicopters waiting.
- **On-screen text:** APRIL 30 · FOG
- **Camera / animation:** Fog drifts
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Fog rolling over the Jalalabad airfield; helicopters waiting.`

#### Scene 171 · 18:24.9–18:31.1 (6.2 s) · ILLUS

**VO:** "The mission was moved to May 1, 2011. … May 1, 2011. In Washington,"

- **Visual:** Calendar flips to MAY 1, 2011; split clocks WASHINGTON 1:22 PM / AFGHANISTAN ~11 PM.
- **On-screen text:** MAY 1, 2011
- **Camera / animation:** Calendar flip
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Calendar flips to MAY 1, 2011; split clocks WASHINGTON 1:22 PM / AFGHANISTAN ~11 PM.`

### Part 5 — The raid

#### Scene 172 · 18:31.1–18:36.7 (5.6 s) · ILLUS

**VO:** "it was 1:22 in the afternoon. In Afghanistan, close to 11 at night."

- **Visual:** Two clocks side by side.
- **On-screen text:** 1:22 PM · ~11 PM
- **Camera / animation:** Clock hands tick
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Two clocks side by side.`

#### Scene 173 · 18:36.7–18:44.1 (7.4 s) · ILLUS

**VO:** "CIA Director Panetta and Admiral McRaven launched the operation. Obama was playing golf — on purpose,"

- **Visual:** A golf course; a golfer swinging (no likeness, seen from behind).
- **On-screen text:** "PLAYING GOLF — ON PURPOSE"
- **Camera / animation:** Slow pan
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A golf course; a golfer swinging (no likeness, seen from behind).`

#### Scene 174 · 18:44.1–18:50.6 (6.5 s) · ILLUS

**VO:** "so no one would sense anything. … Around 2 p.m., he walked into the Situation Room."

- **Visual:** A man in a polo shirt walking into the Situation Room (seen from behind).
- **On-screen text:** 2 P.M.
- **Camera / animation:** Follow shot
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A man in a polo shirt walking into the Situation Room (seen from behind).`

#### Scene 175 · 18:50.6–18:56.8 (6.2 s) · ILLUS

**VO:** "His whole national security team was there: Vice President Biden, Secretary of State Clinton,"

- **Visual:** Officials watching a live video feed on the wall screen (generic likenesses).
- **On-screen text:** THE NATIONAL SECURITY TEAM
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Officials watching a live video feed on the wall screen (generic likenesses).`

#### Scene 176 · 18:56.8–19:04.0 (7.2 s) · ILLUS

**VO:** "Defense Secretary Gates. Live video was streaming in from a drone overhead. … That night in Abbottabad,"

- **Visual:** The live drone feed: grainy overhead view of the compound.
- **On-screen text:** LIVE FROM A DRONE
- **Camera / animation:** Push-in on the feed
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The live drone feed: grainy overhead view of the compound.`

#### Scene 177 · 19:04.0–19:09.6 (5.6 s) · ILLUS

**VO:** "bin Laden finished dinner and went up to the top floor to sleep, with his wives and children."

- **Visual:** Inside the compound at night: lights going out; a tall figure climbing the stairs (back to camera).
- **On-screen text:** THE TOP FLOOR
- **Camera / animation:** Slow push up the stairs
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Inside the compound at night: lights going out; a tall figure climbing the stairs (back to camera).`

#### Scene 178 · 19:09.6–19:16.4 (6.8 s) · ILLUS

**VO:** "He had no idea. … At Jalalabad, one Chinook stayed behind as backup. The other four —"

- **Visual:** Jalalabad airfield at night: one Chinook staying behind.
- **On-screen text:** ONE CHINOOK STAYS BEHIND
- **Camera / animation:** Pan
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Jalalabad airfield at night: one Chinook staying behind.`

#### Scene 179 · 19:16.4–19:24.2 (7.7 s) · ILLUS

**VO:** "two Chinooks carrying a quick reaction force, and the two Black Hawks — lifted off toward Pakistan at 11 p.m."

- **Visual:** Helicopters lifting off from Jalalabad in the dark.
- **On-screen text:** 11 P.M. · LIFT-OFF
- **Camera / animation:** Rise with the helicopters
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Helicopters lifting off from Jalalabad in the dark.`

#### Scene 180 · 19:24.2–19:29.3 (5.1 s) · MAP

**VO:** "Within 15 minutes, they crossed into Pakistani airspace, flying very low."

- **Visual:** Paper map: two helicopter icons crossing the border into Pakistan, flying low.
- **On-screen text:** 15 MINUTES TO PAKISTAN
- **Camera / animation:** Icons move
- **Image prompt:** `Dark intelligence-style map: near-black sea, dark slate land, thin blue-grey borders, the featured country lit amber with a glowing edge, red pins with pulsing rings and white condensed labels, faint grid, film grain. Paper map: two helicopter icons crossing the border into Pakistan, flying low.`

#### Scene 181 · 19:29.3–19:37.1 (7.8 s) · ILLUS

**VO:** "Pakistan's radar caught nothing. … Around midnight, the two Chinooks set down in the hills with the quick reaction force."

- **Visual:** A Pakistani radar screen sweeping, showing nothing; then Chinooks landing in dark hills.
- **On-screen text:** RADAR: NOTHING
- **Camera / animation:** Sweep; cut
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A Pakistani radar screen sweeping, showing nothing; then Chinooks landing in dark hills.`

#### Scene 182 · 19:37.1–19:44.4 (7.4 s) · ILLUS

**VO:** "At 12:30, the two Black Hawks reached bin Laden's compound. … Chalk One: 12 SEAL commandos."

- **Visual:** Two Black Hawks approaching the compound under moonlight; clock 12:30.
- **On-screen text:** 12:30 A.M.
- **Camera / animation:** Push toward the compound
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Two Black Hawks approaching the compound under moonlight; clock 12:30.`

#### Scene 183 · 19:44.4–19:50.7 (6.3 s) · ILLUS

**VO:** "Chalk Two: 12 more SEALs, plus a military dog named Cairo and an interpreter. The plan:"

- **Visual:** Tactical overlay of the compound: CHALK ONE and CHALK TWO icons; a dog icon CAIRO.
- **On-screen text:** CHALK ONE · CHALK TWO · CAIRO
- **Camera / animation:** Icons pop
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Tactical overlay of the compound: CHALK ONE and CHALK TWO icons; a dog icon CAIRO.`

#### Scene 184 · 19:50.7–19:57.3 (6.6 s) · ILLUS

**VO:** "Chalk One would hover over the compound while its SEALs roped down inside. Chalk Two would cover them."

- **Visual:** The plan: Chalk One hovering, ropes down; Chalk Two covering.
- **On-screen text:** THE PLAN
- **Camera / animation:** Paths draw
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The plan: Chalk One hovering, ropes down; Chalk Two covering.`

#### Scene 185 · 19:57.3–20:03.2 (5.9 s) · ILLUS

**VO:** "But in the very first moments, everything went wrong. As Chalk One hovered over the compound,"

- **Visual:** A Black Hawk hovering over the courtyard, beginning to wobble.
- **On-screen text:** EVERYTHING WENT WRONG
- **Camera / animation:** Camera shakes
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A Black Hawk hovering over the courtyard, beginning to wobble.`

#### Scene 186 · 20:03.2–20:11.0 (7.8 s) · ILLUS

**VO:** "it got trapped in its own downwash — an aerodynamic effect called vortex ring state. The pilot lost control."

- **Visual:** Air-flow arrows swirling under the rotor: "VORTEX RING STATE".
- **On-screen text:** VORTEX RING STATE
- **Camera / animation:** Arrows swirl
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Air-flow arrows swirling under the rotor: "VORTEX RING STATE".`

#### Scene 187 · 20:11.0–20:18.4 (7.4 s) · ILLUS

**VO:** "The training compound had low walls. The real compound's 18-foot concrete walls changed how the air moved."

- **Visual:** Split: low training wall vs 18-foot wall, air bouncing off it.
- **On-screen text:** THE WALLS CHANGED THE AIR
- **Camera / animation:** Split wipe
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Split: low training wall vs 18-foot wall, air bouncing off it.`

#### Scene 188 · 20:18.4–20:25.2 (6.8 s) · ILLUS

**VO:** "At the last second, the pilot kept his head and brought the helicopter down nose-first in a controlled crash."

- **Visual:** The helicopter coming down nose-first in the courtyard (controlled crash, dust cloud).
- **On-screen text:** A CONTROLLED CRASH
- **Camera / animation:** Dust burst
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The helicopter coming down nose-first in the courtyard (controlled crash, dust cloud).`

#### Scene 189 · 20:25.2–20:33.3 (8.1 s) · ILLUS

**VO:** "The SEALs climbed out. Nobody was hurt. But the helicopter's tail was stuck on the wall. … The plan had to change."

- **Visual:** SEALs climbing out; the tail stuck on the wall.
- **On-screen text:** NOBODY HURT / THE TAIL STUCK ON THE WALL
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. SEALs climbing out; the tail stuck on the wall.`

#### Scene 190 · 20:33.3–20:39.4 (6.1 s) · ILLUS

**VO:** "The operation was no longer secret — anyone who saw that wreck the next day would understand."

- **Visual:** The wrecked helicopter in the courtyard at night.
- **On-screen text:** NO LONGER SECRET
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The wrecked helicopter in the courtyard at night.`

#### Scene 191 · 20:39.4–20:45.7 (6.3 s) · ILLUS

**VO:** "So the second Black Hawk landed and stayed, and the backup Chinook was called in. … At the same time,"

- **Visual:** The second Black Hawk landing outside the walls; the backup Chinook icon called in.
- **On-screen text:** PLAN B
- **Camera / animation:** Pan
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The second Black Hawk landing outside the walls; the backup Chinook icon called in.`

#### Scene 192 · 20:45.7–20:50.8 (5.1 s) · ILLUS

**VO:** "the power across Abbottabad went out. That, too, was said to be part of the plan."

- **Visual:** The town's lights going dark street by street.
- **On-screen text:** THE POWER WENT OUT
- **Camera / animation:** Lights switch off
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The town's lights going dark street by street.`

#### Scene 193 · 20:50.8–20:57.1 (6.2 s) · ILLUS

**VO:** "An IT professional in Abbottabad, Sohaib Athar, was working late that night. He tweeted:"

- **Visual:** A man at a laptop late at night; name card SOHAIB ATHAR.
- **On-screen text:** 1 A.M.
- **Camera / animation:** Push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A man at a laptop late at night; name card SOHAIB ATHAR.`

#### Scene 194 · 20:57.1–21:03.2 (6.2 s) · ILLUS

**VO:** "“Helicopter hovering above Abbottabad at 1AM (is a rare event).” Without knowing it,"

- **Visual:** A tweet appearing on screen: "Helicopter hovering above Abbottabad at 1AM (is a rare event)."
- **On-screen text:** THE FIRST REPORT
- **Camera / animation:** Typewriter text
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A tweet appearing on screen: "Helicopter hovering above Abbottabad at 1AM (is a rare event)."`

#### Scene 195 · 21:03.2–21:08.5 (5.2 s) · ILLUS

**VO:** "he became the first person in the world to report the operation. … Inside,"

- **Visual:** The tweet's like counter ticking; the compound in the background through the window.
- **On-screen text:** WITHOUT KNOWING IT
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The tweet's like counter ticking; the compound in the background through the window.`

#### Scene 196 · 21:08.5–21:14.8 (6.4 s) · ILLUS

**VO:** "the SEALs blew open the first gate with C4 explosives and moved toward Ibrahim's quarters."

- **Visual:** SEALs blowing a gate with C4 (bright flash, silhouettes).
- **On-screen text:** THE FIRST GATE
- **Camera / animation:** Flash
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. SEALs blowing a gate with C4 (bright flash, silhouettes).`

#### Scene 197 · 21:14.8–21:20.4 (5.6 s) · ILLUS

**VO:** "As a SEAL approached the door, Ibrahim opened fire from behind it. In the return fire,"

- **Visual:** Muzzle flashes behind a closed door (no people visible).
- **On-screen text:** IBRAHIM'S QUARTERS
- **Camera / animation:** Flashes
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Muzzle flashes behind a closed door (no people visible).`

#### Scene 198 · 21:20.4–21:26.6 (6.2 s) · ILLUS

**VO:** "Ibrahim was killed. … His wife, terrified, opened the door so the children wouldn't be hit."

- **Visual:** A door opening; a woman shielding children (silhouettes).
- **On-screen text:** THE CHILDREN
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A door opening; a woman shielding children (silhouettes).`

#### Scene 199 · 21:26.6–21:33.5 (6.9 s) · ILLUS

**VO:** "The children were hiding behind sacks. Everyone there was held in place. … They blew the second gate with C4"

- **Visual:** Sacks in a corner; then the second gate flashing open.
- **On-screen text:** THE SECOND GATE
- **Camera / animation:** Flash
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Sacks in a corner; then the second gate flashing open.`

#### Scene 200 · 21:33.5–21:39.7 (6.1 s) · ILLUS

**VO:** "and entered the main house. Abrar was on the ground floor. The interpreter called out to him."

- **Visual:** Night-vision green view of the ground floor; an interpreter calling out.
- **On-screen text:** ABRAR
- **Camera / animation:** Night-vision tint
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Night-vision green view of the ground floor; an interpreter calling out.`

#### Scene 201 · 21:39.7–21:47.3 (7.6 s) · ILLUS

**VO:** "Abrar stepped forward and was shot. His wife was hit as well. … On the first floor was bin Laden's son, Khalid."

- **Visual:** Night-vision view up a dark stairwell; flashes of gunfire.
- **On-screen text:** THE FIRST FLOOR · KHALID
- **Camera / animation:** Push up the stairs
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Night-vision view up a dark stairwell; flashes of gunfire.`

#### Scene 202 · 21:47.3–21:54.1 (6.8 s) · ILLUS

**VO:** "He fired wildly with an AK-47. The SEALs took him down too. … The top floor."

- **Visual:** Muzzle flashes on the stairwell landing; then silence.
- **On-screen text:** THE TOP FLOOR
- **Camera / animation:** Flash; hold
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Muzzle flashes on the stairwell landing; then silence.`

#### Scene 203 · 21:54.1–22:02.3 (8.2 s) · ILLUS

**VO:** "Rob O'Neill and his team climbed up, wearing night-vision goggles. A tall man was standing in the hallway. Osama bin Laden."

- **Visual:** Night-vision hallway: a tall man standing at the far end (silhouette).
- **On-screen text:** ROB O'NEILL / OSAMA BIN LADEN
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Night-vision hallway: a tall man standing at the far end (silhouette).`

#### Scene 204 · 22:02.3–22:08.2 (5.9 s) · ILLUS

**VO:** "His wife Amal rushed forward to protect him. In that instant, bin Laden pushed her toward the SEALs"

- **Visual:** A woman rushing forward in the hallway; red laser dots.
- **On-screen text:** AMAL
- **Camera / animation:** Fast push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A woman rushing forward in the hallway; red laser dots.`

#### Scene 205 · 22:08.2–22:15.7 (7.5 s) · ILLUS

**VO:** "and stepped back. For a second, the team held back — they feared she might be wearing a suicide vest. She wasn't."

- **Visual:** The team holding back; a question mark "VEST?".
- **On-screen text:** SHE WASN'T
- **Camera / animation:** Freeze
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The team holding back; a question mark "VEST?".`

#### Scene 206 · 22:15.7–22:24.5 (8.9 s) · ILLUS

**VO:** "O'Neill shot Amal in the leg. … 1:10 a.m. … At 1:10 a.m., two bullets struck bin Laden in the forehead,"

- **Visual:** A dark doorway; a clock 1:10.
- **On-screen text:** 1:10 A.M.
- **Camera / animation:** Clock ticks
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A dark doorway; a clock 1:10.`

#### Scene 207 · 22:24.5–22:32.1 (7.6 s) · ILLUS

**VO:** "above his left eye. Osama bin Laden was dead. … Is it him? … But the team couldn't be sure yet."

- **Visual:** A dark doorway; two muzzle flashes; then silence (nothing else shown).
- **On-screen text:** OSAMA BIN LADEN WAS DEAD
- **Camera / animation:** Flash; fade to black
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A dark doorway; two muzzle flashes; then silence (nothing else shown).`

#### Scene 208 · 22:32.1–22:38.6 (6.5 s) · ILLUS

**VO:** "SEAL Matt Bissonnette pulled back a bedsheet, cleaned bin Laden's face, took photos and sent them on."

- **Visual:** A camera flash in a dark room (no body shown); a SEAL's hand holding a camera.
- **On-screen text:** PHOTOS SENT
- **Camera / animation:** Flash
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A camera flash in a dark room (no body shown); a SEAL's hand holding a camera.`

#### Scene 209 · 22:38.6–22:43.9 (5.3 s) · ILLUS

**VO:** "Fifteen minutes of waiting for confirmation. They had forgotten to bring a measuring tape,"

- **Visual:** A clock counting 15 minutes; an empty tape-measure outline crossed out.
- **On-screen text:** NO TAPE MEASURE
- **Camera / animation:** Counter; X
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A clock counting 15 minutes; an empty tape-measure outline crossed out.`

#### Scene 210 · 22:43.9–22:50.7 (6.8 s) · ILLUS

**VO:** "so they couldn't even measure his height. … The interpreter asked bin Laden's daughters, Sumaiya and Mariam."

- **Visual:** An interpreter kneeling beside two girls (seen from behind).
- **On-screen text:** "WHO IS THIS?"
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. An interpreter kneeling beside two girls (seen from behind).`

#### Scene 211 · 22:50.7–22:56.8 (6.1 s) · ILLUS

**VO:** "Mariam lied: “This is Abdullah bin Mohammed.” But Sumaiya told the truth: “This is my father,"

- **Visual:** Speech bubbles: "ABDULLAH BIN MOHAMMED" crossed out; "MY FATHER, OSAMA".
- **On-screen text:** THE TRUTH
- **Camera / animation:** Bubbles pop
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Speech bubbles: "ABDULLAH BIN MOHAMMED" crossed out; "MY FATHER, OSAMA".`

#### Scene 212 · 22:56.8–23:02.5 (5.7 s) · ILLUS

**VO:** "Osama.” Eleven-year-old Safia confirmed it too. So did his wife Khairiah."

- **Visual:** Two more speech bubbles confirming.
- **On-screen text:** CONFIRMED
- **Camera / animation:** Bubbles pop
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Two more speech bubbles confirming.`

#### Scene 213 · 23:02.5–23:08.1 (5.6 s) · ILLUS

**VO:** "A message reached McRaven in Jalalabad over a satellite phone: “Geronimo,"

- **Visual:** A satellite phone at Jalalabad; a message on its screen.
- **On-screen text:** "GERONIMO, EKIA"
- **Camera / animation:** Typewriter text
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A satellite phone at Jalalabad; a message on its screen.`

#### Scene 214 · 23:08.1–23:13.8 (5.7 s) · ILLUS

**VO:** "EKIA.” Geronimo was the code name for bin Laden. EKIA meant enemy killed in action."

- **Visual:** Definitions on cards: GERONIMO = CODE NAME; EKIA = ENEMY KILLED IN ACTION.
- **On-screen text:** ENEMY KILLED IN ACTION
- **Camera / animation:** Cards pop
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Definitions on cards: GERONIMO = CODE NAME; EKIA = ENEMY KILLED IN ACTION.`

#### Scene 215 · 23:13.8–23:21.2 (7.4 s) · ILLUS

**VO:** "In the White House Situation Room, Obama and his team heard it. One long breath. Ten years of hunting, over."

- **Visual:** The Situation Room, officials exhaling (generic likenesses).
- **On-screen text:** 10 YEARS · OVER
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The Situation Room, officials exhaling (generic likenesses).`

#### Scene 216 · 23:21.2–23:27.9 (6.7 s) · ILLUS

**VO:** "The backup Chinook arrived. All the women and children were gathered in the compound's vegetable garden."

- **Visual:** The backup Chinook landing; women and children gathered in a vegetable garden (seen from afar).
- **On-screen text:** THE BACKUP CHINOOK
- **Camera / animation:** Slow pan
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The backup Chinook landing; women and children gathered in a vegetable garden (seen from afar).`

#### Scene 217 · 23:27.9–23:35.3 (7.4 s) · ILLUS

**VO:** "From bin Laden's room, the SEALs took hard drives, phones, cameras, DVDs and papers — everything."

- **Visual:** SEALs carrying bags of drives and papers.
- **On-screen text:** HARD DRIVES · PHONES · PAPERS
- **Camera / animation:** Items pop
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. SEALs carrying bags of drives and papers.`

#### Scene 218 · 23:35.3–23:41.7 (6.4 s) · ILLUS

**VO:** "The crashed helicopter was blown up with C4. Only the tail section, stuck on the wall, survived."

- **Visual:** The wrecked helicopter blown up (flash); only the tail section left on the wall.
- **On-screen text:** ONLY THE TAIL SURVIVED
- **Camera / animation:** Flash
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The wrecked helicopter blown up (flash); only the tail section left on the wall.`

#### Scene 219 · 23:41.7–23:48.4 (6.8 s) · ILLUS

**VO:** "Sohaib Athar tweeted about that blast too. … At 2:26 a.m., the two helicopters left"

- **Visual:** The laptop again with a second tweet about the blast; clock 2:26.
- **On-screen text:** 2:26 A.M.
- **Camera / animation:** Typewriter text
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The laptop again with a second tweet about the blast; clock 2:26.`

#### Scene 220 · 23:48.4–23:55.5 (7.1 s) · MAP

**VO:** "Pakistan by different routes. Bin Laden's DNA samples were split between them, so that if one crashed,"

- **Visual:** Paper map: two helicopter icons leaving Pakistan on different routes; DNA tube icons in each.
- **On-screen text:** DNA SPLIT IN TWO
- **Camera / animation:** Lines draw
- **Image prompt:** `Dark intelligence-style map: near-black sea, dark slate land, thin blue-grey borders, the featured country lit amber with a glowing edge, red pins with pulsing rings and white condensed labels, faint grid, film grain. Paper map: two helicopter icons leaving Pakistan on different routes; DNA tube icons in each.`

#### Scene 221 · 23:55.5–24:02.2 (6.7 s) · TITLE

**VO:** "the other would survive. The whole operation had taken 40 minutes. … In Jalalabad,"

- **Visual:** Big yellow comic title over the night sky.
- **On-screen text:** 40 MINUTES
- **Camera / animation:** Title slam
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Big yellow comic title over the night sky.`

#### Scene 222 · 24:02.2–24:08.6 (6.3 s) · ILLUS

**VO:** "the DNA was tested against that of bin Laden's sister, who had died in a hospital in Boston."

- **Visual:** A lab bench in Jalalabad; a DNA sample beside a file "SISTER — BOSTON".
- **On-screen text:** THE DNA TEST
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A lab bench in Jalalabad; a DNA sample beside a file "SISTER — BOSTON".`

#### Scene 223 · 24:08.6–24:13.8 (5.2 s) · ILLUS

**VO:** "A 99.9% match. In bin Laden's pocket were 500 euros"

- **Visual:** A result screen reading 99.9% MATCH; then a pocket with 500 euros.
- **On-screen text:** 99.9% MATCH / 500 EUROS
- **Camera / animation:** Counter; pop
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A result screen reading 99.9% MATCH; then a pocket with 500 euros.`

#### Scene 224 · 24:13.8–24:20.0 (6.2 s) · ILLUS

**VO:** "and a few phone numbers — probably kept in case he had to run. … On the USS Carl Vinson,"

- **Visual:** A slip of paper with phone numbers.
- **On-screen text:** IN CASE HE HAD TO RUN
- **Camera / animation:** Push-in
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A slip of paper with phone numbers.`

#### Scene 225 · 24:20.0–24:25.2 (5.2 s) · ILLUS

**VO:** "bin Laden's body was washed according to Islamic rites, wrapped in a white sheet,"

- **Visual:** The deck of the USS Carl Vinson at dawn.
- **On-screen text:** USS CARL VINSON
- **Camera / animation:** Slow pan
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The deck of the USS Carl Vinson at dawn.`

#### Scene 226 · 24:25.2–24:31.2 (6.0 s) · ILLUS

**VO:** "placed in a weighted bag and lowered into the Arabian Sea — so there would never be a grave,"

- **Visual:** A white-wrapped shape on a board above the sea (respectful, distant).
- **On-screen text:** BURIED AT SEA
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A white-wrapped shape on a board above the sea (respectful, distant).`

#### Scene 227 · 24:31.2–24:39.1 (7.8 s) · ILLUS

**VO:** "and never a shrine. … In Pakistan, it was 3:45 in the morning when the army reached the compound."

- **Visual:** Calm sea at dawn; then a clock 3:45.
- **On-screen text:** NO GRAVE · NO SHRINE / 3:45 A.M.
- **Camera / animation:** Cross-fade
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Calm sea at dawn; then a clock 3:45.`

#### Scene 228 · 24:39.1–24:45.3 (6.2 s) · ILLUS

**VO:** "Bin Laden's wives and children were taken to hospital in a curtained bus. Under questioning,"

- **Visual:** A Pakistani army convoy reaching the compound before dawn; a curtained bus.
- **On-screen text:** THE ARMY ARRIVES
- **Camera / animation:** Pan
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A Pakistani army convoy reaching the compound before dawn; a curtained bus.`

#### Scene 229 · 24:45.3–24:52.8 (7.5 s) · ILLUS

**VO:** "they said they had lived there for five years, and described what happened that night. … At 11:35 p.m."

- **Visual:** Women and children in a hospital corridor with officers taking notes (silhouettes).
- **On-screen text:** "FIVE YEARS"
- **Camera / animation:** Slow push
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Women and children in a hospital corridor with officers taking notes (silhouettes).`

#### Scene 230 · 24:52.8–25:00.3 (7.5 s) · ILLUS

**VO:** "Washington time, President Obama told the world. … When the CIA released the files from bin Laden's room,"

- **Visual:** A podium with microphones in a grand hallway; clock 11:35 P.M.
- **On-screen text:** 11:35 P.M. · THE WORLD FINDS OUT
- **Camera / animation:** Slow push to the podium
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A podium with microphones in a grand hallway; clock 11:35 P.M.`

#### Scene 231 · 25:00.3–25:05.8 (5.5 s) · ILLUS

**VO:** "they revealed al-Qaeda's future plans. Documentaries about bin Laden himself,"

- **Visual:** Hard drives and folders spread across a table; documents scrolling on a screen.
- **On-screen text:** THE FILES
- **Camera / animation:** Pan
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Hard drives and folders spread across a table; documents scrolling on a screen.`

#### Scene 232 · 25:05.8–25:11.6 (5.9 s) · ILLUS

**VO:** "which he had ordered in to watch. Video games for the children. And adult content too."

- **Visual:** Folder tabs: PLANS · DOCUMENTARIES · VIDEO GAMES · (redacted).
- **On-screen text:** WHAT THEY FOUND
- **Camera / animation:** Tabs pop
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Folder tabs: PLANS · DOCUMENTARIES · VIDEO GAMES · (redacted).`

#### Scene 233 · 25:11.6–25:18.3 (6.7 s) · ILLUS

**VO:** "After the operation, the team was praised and met President Obama. And Obama made a little joke:"

- **Visual:** A ceremony hall; officers in dress uniform (generic likenesses).
- **On-screen text:** THE TEAM HONOURED
- **Camera / animation:** Slow pan
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A ceremony hall; officers in dress uniform (generic likenesses).`

#### Scene 234 · 25:18.3–25:24.8 (6.5 s) · ILLUS

**VO:** "he gave Admiral McRaven a tape measure — because the team had forgotten to measure bin Laden's height."

- **Visual:** A tape measure mounted on a wooden plaque.
- **On-screen text:** A TAPE MEASURE
- **Camera / animation:** Push-in on the plaque
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. A tape measure mounted on a wooden plaque.`

#### Scene 235 · 25:24.8–25:32.5 (7.7 s) · ILLUS

**VO:** "Ten years. Countless mistakes. He slipped through their hands again and again. Then one courier, one careless phone call,"

- **Visual:** Slow pull-back from the empty compound at dawn.
- **On-screen text:** TEN YEARS
- **Camera / animation:** Slow pull-back
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. Slow pull-back from the empty compound at dawn.`

#### Scene 236 · 25:32.5–25:38.1 (5.6 s) · TITLE

**VO:** "and a 40-minute operation ended the story of the world's most wanted man."

- **Visual:** The empty compound fading to black; title.
- **On-screen text:** 40 MINUTES · THE END OF THE MOST WANTED MAN
- **Camera / animation:** Fade to black
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. The empty compound fading to black; title.`

#### Scene 237 · 25:38.1–25:43.8 (5.8 s) · TITLE

**VO:** "If you want the next story like this, subscribe."

- **Visual:** End screen: subscribe button and two video slots.
- **On-screen text:** SUBSCRIBE
- **Camera / animation:** Pop
- **Image prompt:** `Cinematic film still, realistic documentary reconstruction, 35mm photo, natural lighting, highly detailed, sharp focus, 16:9, no text, no logos; real people only as silhouettes, from behind, in shadow or out of focus; non-graphic. End screen: subscribe button and two video slots.`
