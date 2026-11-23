# Pro motion upgrades (from motion-effects + iart-ai skill packs, 2026-11-09)

General rules learned from the new skills. Use them on top of the Alex kit on every talking-head edit.

## 1. Lock a motion language before animating (motion-art-direction)
Fill once per video, reuse everywhere:
- Personality: **Corporate/Premium** for money, trust, business talk. No overshoot on serious/financial lines.
- Easing: one "out" curve for entrances `cubic-bezier(0.22,1,0.36,1)` (expo-ish), one "in" curve for exits. No third curve.
- Base unit 0.4 s: enter 0.4, big move 0.8, micro 0.2.
- Stagger 60–80 ms, reading order (RTL for Arabic: right to left).
- Travel ≤ 24 px for support items, scale 0.96 → 1.0.
- Hold ≥ 0.3 s stillness after each beat. Exactly one hero per frame. One "wow" moment per video.

## 2. Three treatments per line (talking-head-b-roll)
- **A Speaker:** opening line, opinion, story, emotion, CTA, closing. No graphics.
- **B Overlay:** one concrete thing (keyword, number, icon, short list). Edges / thirds, never on the face. One idea at a time.
- **C Cover:** full-frame scene for numbers, comparisons, steps, anything with 3+ parts. 3–8 s, return to face between covers.
- Rhythm: open and close on A, no A stretch longer than ~8 s in animated sections, no covers back to back.

## 3. Timing per element
- Structure (cards, axes, frames) leads the word by ~6 frames.
- New facts (numbers, %, prices) are readable/settled ON the word, not starting on it.
- Punchlines, negations, answers wait for the revealing word.

## 4. "Premium" = one object changing shape (motion-effects)
- Never fade picture A to picture B. Morph: a chip becomes a card, a bar becomes a line, a word slides into a list.
- Leave a faint ghost of the start state so the eye follows the change.
- Keep something small alive during holds (progress line, cursor, slow push, second light sweep).
- Stagger by a beat. Everything moving together reads as a slide transition.
- Shared element: a word that appears in a caption and then in a card MOVES, it is never retyped.
- Values never change between states (same numbers, bars → line).
- Load fonts before frame 0. Seek-safe: every frame from time only, seeded randomness.

## 5. Effects worth adapting to talking-head graphics
- 05 Chart morph: bars of his numbers become a line, line drawn not faded.
- 06 Dashboard zoom: brackets mark one tile, it grows from its real position.
- 07 Spring stack: 3 offers/examples in turn, spring physics with different damping per card.
- 09 Masked type: footage or texture only inside big letterforms, second line revealed by a mask.
- 11 Text → layout: caption headline moves into a card layout, rest arrives in reading order.
- 13 Perspective shift: layers of a system on one vanishing point.
- 14 Glass focus: lens over the one line that matters, 1.1× sharp inside, chromatic copies.
- 15 Flowing paths: one source feeding several outputs, pulse draws the line, nodes react on arrival.

## 6. Captions (caption-animation, kinetic-typography)
- Word pop: scale 0.9 → 1 with 80–120 ms, active-word highlight in accent colour.
- Max 2 lines, keep inside safe area, strong contrast plate or shadow.
- Split by word for Arabic (never by letter: breaks joining).

## 7. Surfaces
- Default light or the client palette. Neon-on-black is the cliché default, avoid unless the subject is dark (terminal, night).
