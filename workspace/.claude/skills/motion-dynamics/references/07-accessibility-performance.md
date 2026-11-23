# Accessibility and performance

## Reduced motion
On the web, respect `prefers-reduced-motion: reduce`. In native or creative applications, use the platform's equivalent preference where available.

Reduced-motion alternatives:
- Replace large translations with opacity or immediate state changes.
- Remove parallax and large zooms.
- Disable looping decorative motion.
- Remove repeated bounce and elastic effects.
- Keep state changes understandable.

## Motion safety
- Avoid rapid flashing.
- Avoid large, unexpected movement.
- Avoid motion that prevents reading or interacting.
- Do not make essential information available only during a brief animation.

## Web performance
- Prefer `transform` and `opacity` for frequently animated UI.
- Avoid animating layout-heavy properties such as `top`, `left`, `width`, or `height` when transforms can achieve the effect.
- Avoid expensive filters on large areas unless tested.
- Avoid reading layout and writing styles repeatedly in the same frame.
- Use requestAnimationFrame or the animation framework's scheduler rather than arbitrary timers for frame-synchronized work.
- Clean up observers, subscriptions, and animation instances when components unmount.

## General performance
- Avoid creating excessive animation objects every frame.
- Reuse timelines and animation helpers when appropriate.
- Keep frame rate stable.
- Test on realistic hardware and screen sizes.
