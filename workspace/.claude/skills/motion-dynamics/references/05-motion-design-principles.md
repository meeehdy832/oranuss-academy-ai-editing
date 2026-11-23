# Motion-design principles

## Purpose before decoration
Motion should communicate hierarchy, state change, causality, focus, or spatial relationships. Decorative motion should not compete with the main message.

## Weight and scale
- Large/heavy objects usually feel slower than small/light objects.
- Longer travel often needs more time, but duration should be judged by perceived speed.
- A tiny icon can use a quick response; a full-screen scene transition needs more staging.

## Anticipation
A small movement in the opposite direction can prepare for a larger action. Use it only when it improves clarity or character. Do not add anticipation to every UI transition.

## Follow-through and settle
After a primary movement, secondary elements may settle slightly later. Keep the follow-through subtle and avoid noisy motion.

## Stagger and hierarchy
- Use stagger to reveal related elements in reading order.
- Avoid a uniform delay that makes all elements feel like a mechanical list unless that is intended.
- Keep the primary focal element visually dominant.

## Property coordination
Position, opacity, scale, blur, and mask reveal may use different timing. For example, opacity can finish early while position continues settling. Coordinate them rather than forcing identical curves.

## Consistency
Create a small motion language for the product: standard durations, easing families, and stagger rules. Reuse these values unless a component needs a distinct personality.

## Looping
For a seamless loop, match both the value and velocity at the loop boundary where possible. A loop can be position-continuous but still visibly jerk if velocity changes abruptly.
