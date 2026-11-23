# 50 Prompt Motion prompts, analysed

Read on 2026-11-16 from https://prompt-motion.com (the 50 longest distinct prompts out of 240). The prompts belong to their creators: open the link and press **Copy** on the page to get the original text. Below are my own notes on what each one does and what to take from it.

## What the 50 have in common

1. **Length predicts quality.** The 21 detailed briefs (1,000–15,000 characters) are product films with exact beats. The 29 short ones (250–750) are mostly "show what an incredible motion designer you are… go all out" showreels. Those rely on the model's taste and come out generic unless a reference or real assets are attached.
2. **The detailed briefs share one skeleton:** `inputs (with defaults)` → `direction (look + banned list)` → `structure (beats or seconds)` → `build (seek(t), springs, render path)` → `gotchas` → `start (no questions)`.
3. **Continuity beats cuts.** 14 of the 21 long briefs ban crossfades. Scenes grow out of each other: a button becomes a page, a dot becomes a chart, a shape floods the frame and contracts into the next scene.
4. **One camera, one world.** Lay everything out once and move a camera through it, using log-space zoom in 2D or a perspective camera in WebGL. Never two camera moves at once, and never zoom in then straight back out.
5. **Music drives timing.** Pick a BPM (120–130), something lands on every beat, and the big change sits on the drop. Several prompts measure the real beat grid with numpy, then calibrate it to the actual kick hits.
6. **Real assets only.** Use real screenshots, real footage, the real logo and the real copy, and never invent numbers or features. Scrape the site with Playwright first.
7. **Determinism.** Everything is computed from `seek(t)`, with closed-form springs, seeded randomness and no timers. Render 3–16 sub-frames for motion blur, check one still per beat, then do the full render.
8. **Banned lists are as important as the direction.** The usual bans: crossfades, blur-ins, glows, particle bursts, gradients on UI, bouncy easing, holds over 1 s, "anything that looks like a template", invented stats.
9. **3D is used for depth, not for spinning.** A page flat on a floor with pieces lifting toward the lens, a 3D carousel with floor reflections, a badge as a solid object that tilts toward the cursor, and corridors of cards resolving into a wordmark.
10. **Short prompts get better with three additions:** a reference video, the brand's real assets, and "render, check the frames yourself, fix, then deliver".

## The 50

Columns: format · what the brief builds · techniques worth stealing.

### Detailed briefs (1–21)

| # | Entry | Format | What it builds | Steal |
|---|---|---|---|---|
| 1 | [daniel-haida](https://prompt-motion.com/daniel-haida-8691d4) | 15 s, 16:9, 60 fps, Remotion | Premium fintech product film from the real repo and tokens | "One shot = one idea", object-driven transitions, a 19-point restraint list, read the real design tokens first |
| 2 | [notdwd-c2037d](https://prompt-motion.com/notdwd-c2037d) | 12 s, 1:1, 59.94 fps | Keynote-style app sting | Shots enter already moving (exponential ease-out) and leave on acceleration or a blur ramp. Blur follows speed and direction. Hard cuts land 2 frames before a beat. |
| 3 | [notdwd-7de38a](https://prompt-motion.com/notdwd-7de38a) | same | Same brief with fixed palette | Coordinates in px for every element, beats as a formula, frosted-glass prompt box springing from a menu-bar icon |
| 4 | [brainextends](https://prompt-motion.com/brainextends-e19ac3) | 18 s, 16:9, 60 fps | Music-app film inside a dark rounded stage | A stage at 80% × 75% of the canvas with an atmospheric background outside it. The UI rises with a perspective tilt that settles frontal. Original artwork is generated for the film. |
| 5 | [twoclipping-d89be5](https://prompt-motion.com/twoclipping-d89be5) | 14.5 s, 1440×1152, WebGL2 | 3D fly-over of a landing page | The page lies on a studio floor and the camera glides at one speed. Pieces lift toward the lens and stand up at an angle. The camera rises overhead, then dives into the title card. Depth of field is razor thin in front. |
| 6 | [rossaxbt-3085b7](https://prompt-motion.com/rossaxbt-3085b7) | 22 s, 1:1, 60 fps | AI-lab launch film with voiceover | A 9-line VO formula and ElevenLabs takes. Captions type at the spoken time. Liquid-glass controls refract the scene behind them. Images change on 16th notes. |
| 7 | [twoclipping-221cab](https://prompt-motion.com/twoclipping-221cab) | 2D, 1:1, 120 BPM | Photo-print app launch | One continuous take where every scene is made of the previous one. Iris blades open onto a photo. The Dynamic Island stretches into a Mac window. Liquid glass over photos. |
| 8 | [ultimaxbt-2ddf1e](https://prompt-motion.com/ultimaxbt-2ddf1e) | 15 s, 16:9, 130 BPM | Food-ordering launch | A glowing composer types a request, then the send button becomes a wok that tosses ingredients. A lime flood on the drop, then cards burst in. Start the song 12 beats before the drop. |
| 9 | [gdgtify](https://prompt-motion.com/gdgtify-287ddf) | 20 s, 1:1 | Spoken words built as architecture | Each word gets a structural role (lintel, load, support, opening, platform). Typography builds the set. Earn one moment of stillness. |
| 10 | [antonio-kodheli](https://prompt-motion.com/antonio-kodheli-490109) | 23 s, 16:9, Remotion | Promo of a gallery site made from the site itself | Scrape the real page first. Camera = (focus x, focus y, log-scale). A match cut from full-bleed reel back into its tile. A highlighter sweep on one phrase. |
| 11 | [techhalla](https://prompt-motion.com/techhalla-90b8ec) | 20 s, 1:1, loop | Kinetic-type poster bumper | Three type roles (scream, grotesque, mono). Per-glyph springs. The outgoing word is the mask for the incoming one. Print misregistration on impacts. 4 sub-frames of blur. |
| 12 | [rossaxbt-94583b](https://prompt-motion.com/rossaxbt-94583b) | 10 s, 16:9, loop | UI loop guided by a white ball | One ball travels the whole route with no teleporting. The slider value is computed from the ball's position. Every key press has a fixed time. |
| 13 | [ultimaxbt-bbebf5](https://prompt-motion.com/ultimaxbt-bbebf5) | 15 s, 16:9, loop | Orange dot motion system | The dot becomes a letter dot, then a spring graph, then a circle, square and pill, then a halftone. The graph is drawn from the same spring that moves the dot. |
| 14 | [twoclipping-5cba86](https://prompt-motion.com/twoclipping-5cba86) | 1440², 120 BPM, loop | One shape morphing through 12 UI states | One element changes size, radius and colour, and its content swaps with a short blur. The two edges of the tab indicator ride different springs, so it stretches. |
| 15 | [twoclipping-6dd14e](https://prompt-motion.com/twoclipping-6dd14e) | 20 s, 16:9, 120 BPM | UGC-ad generator promo | Real clips as JPEG sequences. A wall of clips with a scan line. A 3D carousel with floor reflections and a blurred whip. The beat grid is measured with numpy. |
| 16 | [pankajstwt](https://prompt-motion.com/pankajstwt-49978ed) | 14.5 s, WebGL2 | Landing-page fly-through (plain-language rewrite of #5) | The same idea in simpler words; floating elements sit 20–40 px above the page |
| 17 | [jake11moran-f60e35](https://prompt-motion.com/jake11moran-f60e35) | 27 s, HyperFrames | Mac notch-browser teaser | Slow, polished moves of 1.5–3 s ("half the speed you'd default to"). A fast spinning list that lands on one item. Windows fly in from behind the camera. Film grain. |
| 18 | [ik-builds](https://prompt-motion.com/ik-builds-b8bdcf) | 15 s, HyperFrames + GSAP | Paper-style explainer template | Marker notes draw on. Hard light/dark switches. A new idea every 1.5–2 s and a sound on every hit. Loudness target −14 LUFS. No invented results. |
| 19 | [lexnlin-038035](https://prompt-motion.com/lexnlin-038035) | 10–15 s | Fast editorial ad with a reference | Study the reference's timing and shot lengths, then change the design. Elements are painted over images. Every morph must be perfect. |
| 20 | [wani-shola](https://prompt-motion.com/wani-shola-16ca7a) | 90–100 s, Remotion | Portfolio showreel | Capture the real site in browser and phone frames. Questions and answers are shown large. Use only facts that are on the site. |
| 21 | [aschapmann](https://prompt-motion.com/aschapmann-131210) | 30 s, Remotion | SaaS launch film | A 4–5 scene story (why it matters → pain → fix → what you get). Trace the logo to SVG. One soft SFX per element. Check frames and fix before showing. |

### Short prompts (22–50)

| # | Entry | Ask in one line | Takeaway |
|---|---|---|---|
| 22 | [lukasersil](https://prompt-motion.com/lukasersil-0ed38e) | Showreel listing every technique | A technique checklist alone gives variety but no story |
| 23 | [dale-vaz](https://prompt-motion.com/dale-vaz-cc612a) | Trading terminal: dot → windows → zoom out to a point in space → back into a phone | The **scale journey** (micro → macro → micro) is a strong spine |
| 24 | [ho-ba](https://prompt-motion.com/ho-ba-f3f0e9) | 30 s product intro on the beat | Break screenshots into components and icons instead of showing them raw |
| 25 | [reflex-cloud](https://prompt-motion.com/reflex-cloud-72ffe5) | Brand reel: hook in the first second | Hook in 1 s, distinct techniques per beat, a clean final frame |
| 26 | [techyoutbe](https://prompt-motion.com/techyoutbe-945b56) | Twitter-style SaaS launch | Gather real assets from the internet first |
| 27 | [abderrahmen-g](https://prompt-motion.com/abderrahmen-g-9e8ed0) | Hand-drawn animals come alive | The user's own drawings as the material, with sound matched to frames |
| 28 | [aichrislee](https://prompt-motion.com/aichrislee-a6cb42) | 15 s showreel, one HTML, Playwright → ffmpeg | Name the render pipeline and say "don't ask questions" |
| 29 | [nolkeeg](https://prompt-motion.com/nolkeeg-bf062e) | "Impress me", free choice of subject | Total freedom can work, but the result is unpredictable |
| 30 | [bthreeagency](https://prompt-motion.com/bthreeagency-b9b8d9) | Figma badge unlock | A badge as a **solid 3D object** that tilts toward the cursor with physics. Gold particles only for the celebration. Fast, not bouncy. |
| 31 | [jhylee95](https://prompt-motion.com/jhylee95-e1152f) | Brand launch scored to music | Retime until every cut sits on a beat |
| 32 | [loicrambo](https://prompt-motion.com/loicrambo-ad6830) | Cycle of life, loopable | A life story as a loop |
| 33 | [ror-fly](https://prompt-motion.com/ror-fly-9950f1) | Cocktail recipe 30 s | Process explainer: ingredients and measurements appear as they pour |
| 34 | [alex-prompter](https://prompt-motion.com/alex-prompter-1ea044) | Business explainer in 5 scenes | Problem → what I do → 3 steps → one proof → name |
| 35 | [kyonax](https://prompt-motion.com/kyonax-on-tech-aabc1d) | Product showreel with ASCII logo | Show the real use cases and flow |
| 36 | [sudo-kiran-6609ed](https://prompt-motion.com/sudo-kiran-6609ed) | "Best of the best" 30 s explainer | Superlatives add nothing; a structure would |
| 37 | [sarut0bisasuke](https://prompt-motion.com/sarut0bisasuke-cefa43) | White Russian recipe | Same recipe template as #33 |
| 38 | [charlesmendez](https://prompt-motion.com/charlesmendez-73b6e4) | User journey through 7 product steps | A narrative of one user's actions makes a clear explainer |
| 39 | [heyiammallik](https://prompt-motion.com/heyiammallik-e72d17) | Portfolio video | "Question your plan; if it doesn't feel pro, start over" |
| 40 | [kloss-xyz](https://prompt-motion.com/kloss-xyz-15182a) | 9:16 chaotic POV video in Python | Personality and point of view as the hook |
| 41 | [ajith-io-ea7f2d](https://prompt-motion.com/ajith-io-ea7f2d) | Distilbook 30 s with a reference video | Reference + research + showreel framing |
| 42 | [anilraok](https://prompt-motion.com/anilraok-eff262) | Pixar-style three.js story | Story first, product placement subtle |
| 43 | [elliot-garreffa](https://prompt-motion.com/elliot-garreffa-f334bc) | URL + brand guide + references | Storyboard the features before building |
| 44 | [samuel-yostt](https://prompt-motion.com/samuel-yostt-891f87) | Showreel in the landing page's style | Match the product's own styling |
| 45 | [danilowm](https://prompt-motion.com/danilowm-d3720d) | `/hyperframes` showreel | Use the HyperFrames skill with the project context |
| 46 | [aistocksavvy](https://prompt-motion.com/aistocksavvy-3fb9f5) | Generic showreel | Generic in, generic out |
| 47 | [cansincengiz-me](https://prompt-motion.com/cansincengiz-me-cf68dd) | Turkish: 15 s promo for 10,000 viewers | The language of the prompt doesn't matter; the audience framing does |
| 48 | [kmasiff](https://prompt-motion.com/kmasiff-cc72cb) | Email tool, every use case | Name the inspiration style (YC launch videos) |
| 49 | [amol909s](https://prompt-motion.com/amol909s-27533e) | App showreel, named features | List the exact features to show |
| 50 | [jacksonfall](https://prompt-motion.com/jacksonfall-54b2ac) | Branding-agency reel from scratch | Make every graphic from scratch, with no stock |

## For Oranuss talking-head shorts: what to use

| Moment in the speech | Technique (entry) |
|---|---|
| Hook / big claim | Per-word kinetic type, masked reveal, outgoing word masks the incoming one (#11) |
| "Many videos" / volume | Wall of real video tiles with a scan line, 3D carousel with floor reflections and a whip (#15) |
| Agency vs AI, costs | Scale journey: one desk → zoom out to a city of agencies → back into one laptop (#23) |
| A list of 3 problems | One shape morphing state to state, with a hero dot travelling between items (#13, #14) |
| "I'm not showing my face" | 3D wall of the speaker's own frames as cards, a light wave running along it, pull-back into the wordmark ORANUSS (realtime template) |
| Logo at the top | Logo tiles lifting off a page lying on a floor (#5) |
| Spoken words as structure | Words given roles and built into a platform (#9) |
| Call to action | Liquid-glass pill that types the action, a badge as a solid 3D object tilting (#6, #30) |
