// Timeline helpers that enforce the "motion never stops" rule (keyframe overlapping).
//
// Measured in the refs: big motion peaks every 20-50f, ~0 frozen frames, and every move has long
// eased tails. So beats are CHAINED WITH OVERLAP: the next beat starts while the previous one is
// still landing. Never start a beat on the frame the previous one fully stops.

export type Beat = { id: string; dur: number; overlap?: number };
export type Slot = { from: number; to: number; dur: number };

/**
 * Chain beats so each one starts `overlap` frames before the previous one ends
 * (default overlap = 25% of the previous beat, the measured sweet spot 20-40%).
 */
export const chain = (beats: Beat[], start = 0, defaultOverlapRatio = 0.25): Record<string, Slot> => {
  const out: Record<string, Slot> = {};
  let cursor = start;
  let prevDur = 0;
  beats.forEach((b, i) => {
    const ov = i === 0 ? 0 : b.overlap ?? Math.round(prevDur * defaultOverlapRatio);
    const from = cursor - ov;
    out[b.id] = { from, to: from + b.dur, dur: b.dur };
    cursor = from + b.dur;
    prevDur = b.dur;
  });
  return out;
};

/** Total length of a chained timeline. */
export const chainEnd = (slots: Record<string, Slot>) => {
  let m = 0;
  for (const k in slots) m = Math.max(m, slots[k].to);
  return m;
};

/** Start frames for n staggered items. */
export const stagger = (n: number, each: number, start = 0) => {
  const out: number[] = [];
  for (let i = 0; i < n; i++) out.push(start + i * each);
  return out;
};

/** Stagger from the center outward (stripes, grids, rows): items near the middle go first. */
export const staggerCenter = (n: number, each: number, start = 0) => {
  const mid = (n - 1) / 2;
  const out: number[] = [];
  for (let i = 0; i < n; i++) out.push(start + Math.round(Math.abs(i - mid) * each));
  return out;
};

/**
 * Hand-off frame: where the next element should START so that it begins at high speed while
 * the accelerating exit is at its peak (velocity matching). `lead` = frames before the exit ends.
 */
export const handoff = (exitStart: number, exitDur: number, lead = 2) => exitStart + exitDur - lead;

/** Frame of beat n at a given BPM (music-locked edits). Big events usually every 2 or 4 beats. */
export const beatFrame = (n: number, bpm = 120, fps = 30, offset = 0) => Math.round(offset + (n * 60 * fps) / bpm);

/** Start a move `lead` frames before a beat so its fastest frame (the middle of a MOVE curve) lands ON the beat. */
export const onBeat = (beat: number, dur: number) => Math.round(beat - dur / 2);

/** Minimum readable hold for a line of copy (refs: >=0.25s/word + 0.5s). */
export const readFrames = (text: string, fps = 30) => {
  const words = text.trim().split(/\s+/).length;
  return Math.round(fps * (0.5 + 0.25 * words));
};
