// Tiny keyframe sampler with per-key easing. Each prop animates only between the keys that mention it.
// The `ease` on a key shapes the segment ARRIVING at that key (like AE's incoming curve).
import { interpolateColors } from "remotion";
import { EASE_PRO, Ease, clamp01, lerp } from "./curves";

export type K = { f: number; ease?: Ease } & { [prop: string]: number | string | Ease | undefined };

const isColor = (v: unknown): v is string =>
  typeof v === "string" && (v[0] === "#" || v.indexOf("rgb") === 0 || v.indexOf("hsl") === 0);

export function sample(keys: K[], frame: number, defaultEase: Ease = EASE_PRO.move): Record<string, number | string> {
  const out: Record<string, number | string> = {};
  if (!keys.length) return out;
  const ks = keys.slice().sort((a, b) => a.f - b.f);
  const props: string[] = [];
  ks.forEach((k) => {
    Object.keys(k).forEach((p) => {
      if (p !== "f" && p !== "ease" && props.indexOf(p) < 0) props.push(p);
    });
  });
  props.forEach((p) => {
    const pk = ks.filter((k) => k[p] !== undefined);
    if (frame <= pk[0].f || pk.length === 1) {
      out[p] = pk[0][p] as number | string;
      return;
    }
    let i = 1;
    while (i < pk.length && pk[i].f < frame) i++;
    if (i >= pk.length) {
      out[p] = pk[pk.length - 1][p] as number | string;
      return;
    }
    const a = pk[i - 1];
    const b = pk[i];
    const e = (b.ease as Ease | undefined) ?? defaultEase;
    const t = e(clamp01((frame - a.f) / Math.max(1, b.f - a.f)));
    const va = a[p];
    const vb = b[p];
    if (typeof va === "number" && typeof vb === "number") out[p] = lerp(va, vb, t);
    else if (isColor(va) && isColor(vb)) out[p] = interpolateColors(t, [0, 1], [va, vb]);
    else out[p] = (t < 0.5 ? va : vb) as number | string;
  });
  return out;
}

export const num = (v: unknown, d: number) => (typeof v === "number" ? v : d);
export const str = (v: unknown, d: string) => (typeof v === "string" ? v : d);

/** Shift all keys by n frames. */
export const shift = (keys: K[], n: number): K[] => keys.map((k) => ({ ...k, f: k.f + n }));
