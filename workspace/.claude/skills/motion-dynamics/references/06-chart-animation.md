# Chart and data-visualization animation

## Principle
Animation should help the viewer understand the data. It must not change the data's meaning.

## Common chart motions

### Line chart reveal
Reveal the existing path progressively using path length or a chart-library-supported reveal mechanism. Do not move the underlying data points to create a more dramatic curve.

### Bar growth
Animate each bar from the correct baseline to its true final value. For positive and negative values, respect the chart's baseline and direction.

### Area chart reveal
Reveal the area along the x-axis or use a clipping mask. Preserve the original series values.

### Scatter plot entrance
Fade or scale points into view with a controlled stagger. Avoid changing point coordinates unless the animation explicitly represents a time-varying dataset.

### Number counter
Interpolate the displayed number only if the final value remains exact. Use formatting that does not create misleading rounding during the animation.

## Timing and sequencing
- Introduce axes and labels before or alongside the data when needed for comprehension.
- Reveal one series at a time when the chart is dense.
- Use subtle stagger for multiple bars or points.
- Keep the full animation short enough to preserve attention.
- Provide a static final chart for reduced-motion users.

## Data integrity
- Never fabricate intermediate observations.
- Never alter final values.
- Never animate the axis scale in a way that exaggerates change.
- Never use overshoot on a numeric value unless it is clearly a decorative element separate from the data.
- Preserve units, labels, ordering, and category identity.

## Implementation approach
Inspect the charting library first. Prefer its supported animation options. If custom rendering is required, separate:
1. data model,
2. scales and geometry,
3. animation progress,
4. visual rendering.

Use a normalized progress value to reveal geometry; do not mutate the original dataset just to animate it.
