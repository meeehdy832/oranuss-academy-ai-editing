# Brief template (fill every field; defaults in brackets)

```
<inputs>
Need: [logo file] · [product link or screenshots] · [key line / hook] · [track ~120 BPM, optional].
If missing, use: wordmark "ORANUSS ACADEMY" · speaker frames as textures · the hook from the transcript · no music.
</inputs>

<direction>
A [length]-second [3D / 2D] [product film / explainer / b-roll cover] at [W×H] and [60] fps.
Stage: [dark ink #100820 with navy #140F2E surfaces] · accent [purple #5B2BE0, neon #8B5CF6 for light only] · rare [yellow #F5C400].
Type: Graphik Arabic [Black/Super for hero words, Bold for lines]; numbers in [Graphik Latin].
Signature shot: [the one frame people will remember; everything builds to it].
Hero object: [the dot / card / tile that travels through every scene].
Camera: one continuous camera; moves = [dolly, crane, push-in, rack focus, rise, dive].
Banned: cuts and crossfades, default materials, glows on everything, particle spam, spinning cards as the idea, paragraphs of text, [anything specific].
</direction>

<structure>
[t0–t1]: [what changes on screen] → [camera move]
[t1–t2]: …
(every major beat lands something; no hold > 1.5 s except the end card)
</structure>

<build>
1. One HTML file; window.seek(t) computes the whole frame from time; seeded randomness; no timers or CSS transitions.
2. [3D: three.js from the local node_modules via import map; key/fill/rim, RoomEnvironment PMREM, MeshPhysicalMaterial, ACES, fog, soft shadows.]
3. Springs are closed-form; one per target change.
4. Stills per beat → look → fix → full render with Playwright → ffmpeg H.264 yuv420p.
</build>

<gotchas>
[Pick from SKILL.md §4 the ones that apply.]
</gotchas>

<start>
Describe the signature shot and the shot list in a few lines, then build without asking anything else.
</start>
```

## Example: expanding a one-liner

User: "make a dynamic 30-second motion graphic about Distilbook like a product explainer, very incredible".

1. Research the product (its site, its real UI), never invent features.
2. Signature shot: the book's pages fan out in 3D and condense into one glowing summary card that lands in the app UI.
3. Hero object: one page corner that becomes the cursor, then the highlight, then the card.
4. Beats: hook line (0–3 s) → problem (3–8) → the product UI rises in perspective and settles frontal (8–14) → three features, each an object-driven transition (14–24) → signature shot (24–27) → logo + URL end card (27–30).
