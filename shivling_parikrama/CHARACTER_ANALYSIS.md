# Character + Movement Analysis (frame-by-frame)

Method: har video ki har second ki movement measure ki, character waale hisson ko **4 frames/second** par dekha, aur faces ko zoom karke **8 frames/second** par (blink aur lip-sync ke liye).

## 0. Sabse badi finding: "Limited animation"
- Zyadatar time screen ka sirf **1–5% hissa** hilta hai. Poora character kabhi nahi dauḍta-naachta.
- Character **cut-out / puppet rig** hote hain: sir, dhaḍ, upper arm, forearm, haath, aankh, palak alag-alag layers. Sirf joints ghoomte hain (kandha, kohni, gardan).
- Life dikhti hai **5 chhoti cheezon** se: (1) aankh ka idhar-udhar dekhna, (2) blink, (3) halki saans/sir ka hilna, (4) ek haath ka loop action, (5) camera ka slow zoom.
- Movement ke peaks (10–50% screen) sirf **transition** par aate hain: white flash, circle-wipe, crossfade.
- Ye style sasta bhi hai aur premium bhi lagta hai. Hum bhi yahi follow karenge.

## 1. Aarti video (v1): paper-cutout style
| Character | Design | Movement (frames se) |
|---|---|---|
| **Mahila bhakt** | Peeli saari, laal-gulabi border, ghoonghat, badi aankhein + gehra kajal, bindi. Skin par **kaagaz/lakdi texture**. Side-profile (3/4 view). | Haath kandhe + kohni se ghoomta hai, aarti ki thaali **gol circle** mein (~1.5 sec ka loop). Aankhein neeche thaali ko dekhti hain. **Lips bilkul nahi hilte** (wo bolti nahi, narrator bolta hai). Ending mein dono haath lau par le jaakar aankhon se lagati hai. |
| **Pujari** | Ganja sir, shikha, maathe par tripund + laal bindu, orange angocha, rudraksh, dhoti, bada pet (puppet shape). | Aarti ka diya **paon → naabhi → mukh → poora swaroop** order mein ghoomta hai. Diye ke saath **roshni ka gola bhi chalta hai** (light follows lamp): background andhera, sirf diye ke paas ujaala. **Aadha blink** (palkein aadhi band) har 2–3 sec. Aankhein diye ko follow karti hain. |
| **Krishna (murti)** | Neela, mor pankh, bansuri, peela pitambar, mala. | Lagbhag **static** (murti hai). Sirf glow badhta-ghatta hai aur god-rays ghoomti hain. |
| **Ahankar** | Kaala silhouette + **laal chamakti aankhein** + mukut. | Neeche se aag uthti hai, mukut jal kar gayab, phir **white flash**. |
- Light ka role: har scene mein **ek hi light source** (diya) aur baaki andhera, isse "dramatic" feel aata hai.

## 2. Ravana–Shani (v2): Tholu Bommalata (puppet) style
| Character | Design | Movement |
|---|---|---|
| **Ravana** | 10 hare sir ek line mein, sone ke shikhar-mukut, hara body jis par **rivet (keel) dots** hain, joints saaf dikhte hain (asli kathputli jaisa). | **Pendulum swing**: haath kandhe se aage-peeche jhoolta hai, body upar-neeche bob karti hai. Seedhiyon par chadhte waqt camera **diagonal pan** karke usse follow karta hai. Gussa = haath aage karke point. |
| **Shani dev** | Gehra neela, kaala-sona kavach, shikhar mukut. | Bolte waqt **sone ka halo** peeche ghoomta hai. Langda kar chalna (ek pair choti step). |
| **9 graha** | Rangeen gol balls / zameen par lete puppets. | Kundli ke box mein hilte hain, ek graha "1 kadam aage" slide karta hai (story ka turning point). |
| **Baby Meghnad** | Jhoole mein. | Jhoola jhoolta hai, rone ki **lines** nikalti hain. |
- Transitions: **circle iris** (gol mask khulta hai), picture-in-picture flashback.

## 3. Hanuman (v3): dark cinematic 2D
| Character | Design | Movement |
|---|---|---|
| **Hanuman** | Muscular, semi-realistic vanar chehra, lamba mukut, **patli sunehri rim-light outline** (body ke kinaare chamakte hain), poonchh "S" shape. | Idle mein **saans** (chhati halki upar-neeche) + poonchh ka halka sway. Close-up par chehra lagbhag still, sirf slow zoom. Fight: dono haath upar loha uthate hain → **left-right swing** (haath ka rotation). Dahaaḍ: **munh khulta hai + gol shockwave rings**. |
| **Gada** | | "Never used" bolte hi gada par **crack lines** + bijli flash (myth tootne ka symbol). |
| **Rakshas sena** | Sirf kaale silhouettes. | Peeche halke se hilte hain, focus Hanuman par rehta hai. |
- Shlok scroll mein text **type-on** hota hai (likhta hua dikhta hai).

## 4. Subah 5 baje (v4): fast bouncy vector
- **Har 0.5–1 sec mein naya scene.** Ladka (orange hoodie, chashma) **jump karta hai, squash-stretch** hota hai, icons "pop" karte hain. Ye 12 sec ka shock-reel hai, dharmik story ka nahi.

## 5. Kar Darshan (v5): warm flat cartoon
| Character | Design | Movement |
|---|---|---|
| **Ladka (aaj ka)** | Saanwla, peeli T-shirt, neeli chaadar. **Top-view** (upar se camera). | Aankhein aadhi khuli (neend wali). Haath **kohni se uthkar phone tak** jaata hai. Phir white flash. |
| **Ladka (purvaj / brahmachari)** | Shikha, Vaishnav tilak, janeu, laal chunri. | Aankh band → khulti hai. Dono haath dheere **upar uthkar hatheli dikhata hai**. Camera slow push-in. Khidki se **light beam**. |
| **Lakshmi / Saraswati / Vishnu** | Flat, symmetric, kamal par. | Static pose, peeche **sunburst ghoomta hai**, sikke girte hain / akshar udte hain. |
- Ending: ladke ke charon taraf **phone aur Sanskrit akshar gol orbit** mein ghoomte hain.

## 6. Bhootnath (v6): clean 2D vector, sabse "premium"
| Character | Design | Movement |
|---|---|---|
| **Shiv ji** | Halka neela, jata-joot + **chandrama**, gale mein naag, rudraksh, baagh-chhaal (orange, dhabbe), trishul + damru. Bade shaant aankhein, maathe par tripund + teesra netra. | (a) Dhyan: almost still, sirf aag ka ring flicker. (b) Nandi par: **upar-neeche bob** (chalne ka rhythm). (c) Chalna: camera ki taraf aate hue **size badhta hai** + halka bob. (d) Close-up: aankhein dheere band → khulti hain (**slow blink = shaanti**). (e) Haathon mein **black-hole/galaxy ghoomti** (cosmic power). (f) Teesra netra: chamakta hai. |
| **Daksh** | Safed daadhi, sone ka bada mukut, hara pendant, laal dhoti. | **Asli lip-sync**: 4–5 munh ki shapes har 2–3 frame par badalti hain. Bhauhein gusse mein upar-neeche. Haath se point karta hai. Isse pata chalta hai: **jab character khud bolta hai tabhi lip-sync, warna nahi.** |
| **Bhoot-gan** | Kaale, kaante jaise baal, **peeli chamakti aankhein**, haath jode. | Halka sway. Peeche bhoot-aatmaayein (safed, transparent). |
| **Bhakt / shoka-grast vyakti** | Safed kapde, matka. | Aankhein band, bilkul still, sirf slow zoom (emotion = stillness). |
- Shots: **over-shoulder** (Daksh ki peeth se Shiv ji darwaze mein), **split-screen** (upar Shiv, neeche bhakt), bijli ka flash.

---

## 7. Hamare video (Shivling parikrama) ke characters + movement plan

Style: **v6 jaisa clean 2D vector + v1 jaisi diye wali lighting** (Shiv content ke liye sabse premium combo).

| Character | Design | Movement (limited animation) |
|---|---|---|
| **Yuva bhakt (ladka)** | Saanwla, safed kurta + kesari gamchha, maathe par tripund, haath mein tamba lota. | Lota tilt karke jal chadhana (kohni rotate, paani ka stream). Parikrama walk: chalne par body bob + **jalaadhari ke paas ruk kar U-turn**. Aankh band karke haath jodna (slow blink). |
| **Pujari ji** (optional) | v1 jaisa: shikha, tripund, rudraksh. | Sirf haath se ishaara "yahan se laut jao". Aadha blink. |
| **Shivling** | Kaala patthar, jaladhari (yoni-peeth) se nikalti naali, bel-patra, phool. | Static. Jal par **halka glow** + paani ka flow animation (loop). |
| **Shiv ji** | v6 jaisa: neela, chandrama, naag, baagh-chhaal. | Dhyan mudra, **slow blink**. "Ardhchandra" beat par sir ka **chandrama chamakta hai**. Last beat par aankhein khulti hain. |
| **Nandi** | Safed, ghanti, Shivling ki taraf mukh. | Static + kaan ka halka hilna. |
| **Ganga** (symbol) | Neeli-safed lehrein. | Jal mein overlay hokar behti hain. |

Rules (references se):
1. Narrator bolta hai, isliye kisi character ka **lip-sync nahi**. Acting sirf aankh, blink aur haath se.
2. Har scene mein **ek light source** (diya / chandrama), baaki andhera + bokeh particles.
3. Har shot par **slow push-in**. Keyword aane par **white flash ya circle-wipe** transition.
4. Ek scene max 3–5 sec.
