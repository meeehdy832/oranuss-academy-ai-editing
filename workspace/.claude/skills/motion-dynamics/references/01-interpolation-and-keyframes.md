# Keyframe interpolation and timing

## 1. What a keyframe represents
A keyframe stores a property's value at a point in time. The interpolation method determines how the property changes between two keyframes. Many applications allow interpolation to be set independently for each segment.

A keyframe animation is not just a list of positions. It is a time-based description of value, velocity, and sometimes acceleration.

## 2. Common interpolation types

### Linear
The property changes at a constant rate between keyframes.
- Use for: constant-speed travel, progress indicators, path drawing, mechanical movement.
- Avoid as the default for: UI entrances, soft reveals, character-like movement.
- Note: constant value speed does not necessarily mean constant perceived speed along a complex spatial path.

### Hold / Constant / Stepped
The value remains unchanged until the next keyframe, then jumps.
- Use for: frame-by-frame animation, digital glitches, state toggles, discrete labels.
- Avoid for: movement that should appear continuous.

### Ease In
Starts slowly and accelerates toward the next keyframe.
- Use for: departures, launches, objects gaining momentum.
- Avoid when the user expects an immediate response.

### Ease Out
Starts quickly and decelerates into the destination.
- Use for: entrances, reveals, landing, focus transitions.
- Commonly effective for UI because the destination feels controlled.

### Ease In Out
Starts and ends slowly, with faster movement in the middle.
- Use for: transitions between two stable states, camera moves, scene changes.
- Avoid applying it automatically to every property.

### Custom Bézier
A curve is shaped using handles/control points.
- Use when standard easing names do not match the intended rhythm.
- Verify the curve in the actual tool; curve conventions differ.

### Automatic / Auto Bézier
The application calculates smooth handles.
- Use for: quick smoothing of a sequence.
- Inspect for unwanted overshoot, loops, or velocity changes.

### Spline / Hermite / Catmull-Rom
Smooth interpolation through multiple values.
- Use for: continuous paths and multi-point animation.
- Watch for overshoot between points, especially with unevenly spaced data.

### Monotonic / Clamped interpolation
Maintains monotonic behavior and avoids overshoot outside intended bounds.
- Use for: chart values, percentages, progress, and other bounded numeric data.

### Spring / Physics-based
Uses spring dynamics rather than only a fixed easing curve.
- Use for: elastic interfaces, responsive drag release, physical settling.

## 3. Temporal vs spatial interpolation
- **Temporal interpolation:** controls how fast a value changes over time.
- **Spatial interpolation:** controls the path an object follows through space.

A motion can follow a curved spatial path at constant speed, or a straight path with strongly eased speed. Do not confuse path handles with speed handles.

## 4. Continuity
- **C0 continuity:** positions/values meet at the keyframe.
- **C1 continuity:** tangent direction/velocity is continuous.
- **C2 continuity:** acceleration is continuous.

For polished movement, avoid sudden velocity changes unless the motion intentionally hits, stops, or changes direction.

## 5. Segment-level easing
A multi-keyframe animation can use different easing per segment. For example:
- Segment 1: slow anticipation.
- Segment 2: rapid travel.
- Segment 3: small overshoot.
- Segment 4: gentle settle.

Do not apply one global curve when the motion clearly contains different phases.
