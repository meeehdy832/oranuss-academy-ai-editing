# Bézier curves and graph-editor reasoning

## Cubic Bézier basics
A cubic Bézier curve uses four points:
- `P0`: start
- `P1`: first control handle
- `P2`: second control handle
- `P3`: end

In timing curves, the horizontal axis commonly represents normalized time and the vertical axis represents normalized progress. In spatial paths, both axes may represent position. Confirm the target application's graph mode.

## CSS timing curves
For CSS `cubic-bezier(x1, y1, x2, y2)`, x control values must be between 0 and 1. Y values may go outside that range for intentional overshoot.

## Reading a value graph
- Straight diagonal: constant rate.
- Curve that flattens at the beginning: slow start.
- Curve that steepens: acceleration.
- Curve that flattens at the end: deceleration.
- Curve that rises above final value: overshoot.
- Curve that reverses direction: reversal or oscillation.

## Reading a speed graph
- Flat line: constant speed.
- Rising line: acceleration.
- Falling line: deceleration.
- Peak then decline: accelerate then settle.
- Repeated peaks: oscillation or bounce.
- Sudden spike: abrupt change or discontinuity.

## Practical graph-editor workflow
1. Decide whether the movement starts at rest.
2. Decide whether it ends at rest.
3. Place peak velocity at the intended moment.
4. Shape outgoing and incoming handles.
5. Check the value graph and speed graph separately.
6. Check the keyframe join for velocity continuity.
7. Preview at the final duration and frame rate.

## Multi-segment continuity
A smooth curve on each segment does not guarantee a smooth complete animation. Incoming and outgoing tangents should align when motion should continue through a keyframe. For an impact, a sharp velocity change may be correct.

## Avoid
- Accidental overshoot on values that must stay bounded.
- Unintentional path loops caused by spatial handles.
- Extreme handles that make the motion stall or accelerate unnaturally.
- Confusing a smooth value graph with smooth velocity.
