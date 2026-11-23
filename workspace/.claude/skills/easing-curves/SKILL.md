---
name: "easing-curves"
description: "Pick and code motion easing curves (linear, sine, power, uniform, bounce, spring/physical, combos) for any animation in video, web, CSS, Remotion, GSAP or After Effects."
---

# Easing Curves for Motion

Developed by Mehdi ORANUSS | Powered by Claude

Use this whenever something moves, scales, fades or counts in an animation and you need to decide HOW it moves over time.

## How to read an easing chart
- X axis = time (0 → 1, start to end of the animation).
- Y axis = progress (0 = start value, 1 = end value).
- Steep part = fast movement. Flat part = slow / stopped.
- Curve going ABOVE 1 = overshoot (goes past the target, then comes back).
- Curve dipping back down after touching 1 = bounce (hits the target and rebounds).
- The side track with a dot in reference charts shows the real object moving along one line using that curve.

Any easing is just a function `ease(t)` with `t` from 0 to 1. Final value = `from + (to - from) * ease(t)`.

## The curve library (what each one does)

| Curve | Params | Feel | Use for |
|---|---|---|---|
| linear | – | Constant speed, robotic | Progress bars, tickers, scrolling, rotation loops, colour fades |
| sine | – | Soft start, soft end | Default for gentle UI and camera moves |
| power(n) | n = 2 soft, 3 medium, 4–5 punchy | Slow → very fast → slow. Higher n = more dramatic | Text/cards sliding in, scene transitions |
| uniform(a, d) | a = fraction of time accelerating, d = fraction decelerating | Speeds up, cruises at constant speed, slows down | Mechanical moves, cameras, trains/cars, long pans |
| bounce(n, e) | n = number of bounces, e = elasticity 0–1 | Falls to target with gravity, rebounds n times, each smaller | Things dropping in, landing icons, playful titles |
| spring(f, d) | f = oscillations, d = damping (higher = settles faster) | Shoots past the target and wobbles before settling | Pop-ins, buttons, stickers, energetic captions, counters landing |
| compose(outer, inner) | two easings | Time-warps one curve with another | e.g. bounce + uniform = slow wind-up, then bounces |

Quick choice rules:
1. Calm / premium / corporate → sine or power(2–3).
2. Snappy modern UI and social video → power(4) or spring(3, 5).
3. Playful, cartoony, kids → bounce or spring with low damping (spring(3, 2)).
4. Physical / mechanical realism → uniform.
5. Never use linear for things entering or leaving the screen, only for continuous motion.
6. Shorter durations need stronger curves; 0.3–0.6 s for UI, 0.5–1.2 s for video elements, springs can run 0.8–1.5 s because the wobble needs time.
7. Keep one easing family per video so motion feels consistent.

## Reference implementation (JavaScript, tested: every curve returns 0 at t=0 and exactly 1 at t=1)

```js
export const Ease = {
  linear: t => t,
  sine: t => (1 - Math.cos(Math.PI * t)) / 2,
  // in-out power curve
  power: n => t => t < 0.5 ? Math.pow(2*t, n)/2 : 1 - Math.pow(2 - 2*t, n)/2,
  // trapezoid speed profile: accelerate for a, cruise, decelerate for d (a + d <= 1)
  uniform: (a, d) => t => {
    const v = 1 / (1 - a/2 - d/2);
    if (t < a) return v*t*t/(2*a);
    if (t <= 1 - d) return v*(t - a/2);
    const u = 1 - t; return 1 - v*u*u/(2*d);
  },
  // gravity fall onto the target, then n rebounds; e = restitution (0.3 dead, 0.7 springy)
  bounce: (n = 3, e = 0.5) => {
    const segs = [1]; for (let i = 1; i <= n; i++) segs.push(2*Math.pow(e, i));
    const total = segs.reduce((s, x) => s + x, 0);
    return t => {
      let x = t*total;
      if (x < 1) return x*x;
      x -= 1;
      for (let i = 1; i <= n; i++) {
        const dur = segs[i];
        if (x < dur) { const h = Math.pow(e, 2*i), s = (x - dur/2)/(dur/2); return 1 - h*(1 - s*s); }
        x -= dur;
      }
      return 1;
    };
  },
  // damped spring that overshoots; f = wobbles, d = damping. Lands exactly on 1.
  spring: (f = 3, d = 3) => t => {
    const w = 2*Math.PI*f, end = Math.exp(-d)*Math.cos(w);
    return 1 - (Math.exp(-d*t)*Math.cos(w*t) - t*end);
  },
  compose: (outer, inner) => t => outer(inner(t)),
  // helpers
  reverse: ease => t => 1 - ease(1 - t),          // turns an ease-in into an ease-out
  mix: (from, to, ease, t) => from + (to - from)*ease(t),
};

// Example: the 'bounce + uniform' combo
const bounceUniform = Ease.compose(Ease.bounce(3, 0.5), Ease.uniform(0.4, 0));
```

Presets matching common reference charts:
- `Ease.power(2)`, `Ease.power(4)`
- `Ease.uniform(0.25, 0.5)`, `Ease.uniform(0.5, 0.5)`
- `Ease.bounce(2, 0.6)`, `Ease.bounce(4, 0.6)`
- `Ease.spring(4, 5)` (fast tight wobble), `Ease.spring(3, 3)` (big overshoot), `Ease.spring(3, 6)` (one soft overshoot)

## Using it in each tool

- **Remotion**: `interpolate(frame, [0, 30], [0, 1], { easing: Ease.spring(3, 4), extrapolateRight: 'clamp' })`. Do not clamp output for spring, or the overshoot is lost.
- **GSAP**: `gsap.to(el, { y: 0, duration: 0.8, ease: Ease.bounce(3, 0.5) })` (GSAP accepts a function).
- **Framer Motion / Motion One**: `transition={{ duration: 0.8, ease: Ease.power(4) }}`.
- **Canvas / Three.js / custom loop**: compute `t = clamp(elapsed / duration)` and use `Ease.mix`.
- **CSS**: simple curves use cubic-bezier: sine ≈ `cubic-bezier(0.37, 0, 0.63, 1)`, power(2) ≈ `cubic-bezier(0.45, 0, 0.55, 1)`, power(4) ≈ `cubic-bezier(0.76, 0, 0.24, 1)`. Bounce, spring and uniform cannot be a cubic-bezier, so sample them into CSS `linear()`:

```js
const toCSSLinear = (ease, n = 60) =>
  'linear(' + Array.from({length: n + 1}, (_, i) => +ease(i/n).toFixed(4)).join(', ') + ')';
// animation-timing-function: linear(0, 0.12, ... , 1);
```

- **After Effects** (expression on a property with 2 keyframes, spring style):

```
f = 3; d = 4;
if (numKeys > 1 && time > key(numKeys).time) {
  t = time - key(numKeys).time;
  v = velocityAtTime(key(numKeys).time - thisComp.frameDuration/10);
  w = f*Math.PI*2;
  value + v*(Math.sin(t*w)/Math.exp(d*t)/w);
} else value;
```

## Workflow
1. Name every moving element and what it should feel like (calm, snappy, playful, physical).
2. Pick a curve + parameters from the table and the quick rules.
3. Set duration (see rule 6) and stagger groups by 2–4 frames / 40–80 ms.
4. Implement with the reference code in the target tool.
5. If asked to show options, render a preview page: one small chart per curve (time on X, value on Y, light grey box from 0 to 1, overshoot allowed outside the box) plus a dot moving on a vertical track using the same curve, so the user can compare feel side by side.
6. Check: elements land exactly on their final value, no curve is linear for entrances/exits, and spring/bounce durations are long enough for the wobble to finish.