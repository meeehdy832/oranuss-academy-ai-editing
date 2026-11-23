# 10 · Sound design (basics)

This skill makes the picture. The author's full sound-design workflow (SFX library, mixer and mux scripts) is a separate
skill and is not included here. If you have your own SFX, these rules are enough to score a reel from this skill:

1. **List the event frames** from the composition: morphs, clicks / `pop()`, camera aims and pushes, collapse / emerge,
   `punch()`, and (with a voice-over) the frame of every key word.
2. **One sound per event, on the event frame.** Whooshes start 2–4 f *before* a fast move so their peak lands on it;
   clicks and pops land exactly on the frame; risers end on the impact.
3. **Few, consistent sounds.** One whoosh family, one click, one pop, one impact; vary pitch / volume, not the sound.
   Silence between hits is part of the style.
4. **Voice first.** No SFX within 3 dB of the voice for ≥ 100 ms on a key word; duck the music under the voice.
5. **Mix:** about −14 LUFS integrated, true peak ≤ −1 dBTP; heavy limiting only on intended punches.
6. **Play it from the composition** with Remotion's `<Audio src={staticFile("sfx/…")} />` inside a `<Sequence from={eventFrame}>`
   so it stays in sync with the picture, or mux a finished mix onto the final MP4 with ffmpeg
   (`ffmpeg -i video.mp4 -i mix.wav -c:v copy -c:a aac -shortest out.mp4`).
