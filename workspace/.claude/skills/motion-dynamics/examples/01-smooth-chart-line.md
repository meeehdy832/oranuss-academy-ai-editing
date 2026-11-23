# Example: smooth chart line reveal

## Intent
Draw a chart line from left to right while preserving the original data geometry.

## Motion spec
- Animate: path reveal progress, not the data values.
- Duration: 900–1400 ms depending on chart density.
- Easing: linear or very subtle ease-out.
- Overshoot: none.
- Final state: exactly the original chart.
- Reduced motion: show the complete chart immediately.

## SVG concept
For an SVG path, a common technique is to use the path's total length as the stroke dash length, then animate dash offset from full length to zero. Confirm the path is a single revealable path and that the SVG renderer supports the required attributes.

Do not distort the x/y coordinates or change the dataset to create the reveal.
