# Spring physics and physically-inspired motion

## Core parameters
- **Mass:** perceived weight/inertia. Higher mass usually responds more slowly.
- **Stiffness:** strength of the pull toward the target.
- **Damping:** how quickly oscillation loses energy.
- **Initial velocity:** velocity at the moment the spring begins.
- **Rest threshold:** when the engine considers the spring settled.

## Damping behavior
- **Underdamped:** overshoots and oscillates before settling.
- **Critically damped:** returns quickly without oscillation.
- **Overdamped:** returns without oscillation but more slowly.

## Choosing a spring
- Refined UI: critically damped or lightly underdamped.
- Playful icon: underdamped with small amplitude.
- Heavy panel: overdamped or low-frequency spring.
- Drag-release interaction: preserve release velocity, then let the spring settle.
- Chart data: do not use a spring if it makes the plotted value exceed the true value.

## Tuning order
1. Choose the desired overall settling time.
2. Adjust stiffness to control responsiveness.
3. Adjust damping to control overshoot.
4. Set initial velocity to match the interaction.
5. Test on the real element and screen size.

## Implementation safety
Use the framework's native spring API when available and verify its parameter conventions. Do not copy numerical parameters between libraries without checking units and semantics. If implementing a spring manually, use a stable time integration method or an analytic solution.

## Reduced motion
For users requesting reduced motion, replace large oscillations with a short opacity change or immediate state change.
