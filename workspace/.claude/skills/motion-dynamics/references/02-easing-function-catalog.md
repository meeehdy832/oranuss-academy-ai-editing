# Easing function catalog

Let `t` be normalized time from 0 to 1. Easing maps time progress to value progress. Formula names and edge-case conventions can vary by library.

## Core polynomial functions

- Linear: `f(t) = t`
- In Quad: `t²`
- Out Quad: `1 - (1 - t)²`
- InOut Quad: `2t²` when `t < 0.5`, otherwise `1 - (-2t + 2)² / 2`
- In Cubic: `t³`
- Out Cubic: `1 - (1 - t)³`
- InOut Cubic: `4t³` when `t < 0.5`, otherwise `1 - (-2t + 2)³ / 2`
- In Quart: `t⁴`
- Out Quart: `1 - (1 - t)⁴`
- InOut Quart: `8t⁴` when `t < 0.5`, otherwise `1 - (-2t + 2)⁴ / 2`
- In Quint: `t⁵`
- Out Quint: `1 - (1 - t)⁵`

## Other families

### Sine
Gentle, natural curves. Useful for subtle movement and low-intensity transitions.

### Expo
Very strong acceleration/deceleration. Useful for dramatic speed changes. Be careful near endpoints because some implementations need special endpoint handling.

### Circ
Strong curvature near the start or end. Can feel decisive and controlled.

### Back
Moves beyond the target and returns. Use a small overshoot for a pop or expressive arrival. Do not use for bounded chart data.

### Elastic
Oscillates around the destination. Use for playful, elastic effects. Avoid for serious dashboards and important text.

### Bounce
Simulates repeated impacts. Use for objects that should feel like they bounce, not as a generic “fun” easing.

## CSS cubic-bezier starting points

`cubic-bezier(x1, y1, x2, y2)`:
- Standard ease: `cubic-bezier(0.25, 0.1, 0.25, 1)`
- Ease-in-out: `cubic-bezier(0.42, 0, 0.58, 1)`
- Snappy ease-out: `cubic-bezier(0.16, 1, 0.3, 1)`
- Strong ease-in: `cubic-bezier(0.7, 0, 0.84, 0)`
- Soft arrival: `cubic-bezier(0.22, 1, 0.36, 1)`
- Smooth controlled transition: `cubic-bezier(0.65, 0, 0.35, 1)`

These are starting points, not laws. Check the output in the target runtime.

## Selection guide
- Slow start, fast finish: In.
- Fast start, slow finish: Out.
- Slow start and finish: InOut.
- Constant rate: Linear.
- Pass target and return: Back or custom keyframes.
- Oscillate before settling: Elastic or spring.
- Repeated impact: Bounce.
- Discrete jump: Steps/Hold.

## Important constraints
- Some easing functions return values outside `[0,1]`. This is intentional for overshoot, but dangerous for data and bounded values.
- Easing may be applied to time, not directly to the property. A spring may instead be modeled as a physical response.
- Never assume a named easing has identical parameters across libraries.
