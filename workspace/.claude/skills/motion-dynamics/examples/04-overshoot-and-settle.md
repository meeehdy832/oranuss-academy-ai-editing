# Example: overshoot and settle

## Intent
A panel slides into place, passes the target slightly, and returns once.

## Motion spec
- Main travel: ease-out.
- Overshoot: small relative to total travel (start with 2–4%).
- Return: short ease-out.
- No repeated oscillation unless requested.
- Reduced motion: direct transition with opacity.

The percentage is a visual starting point, not a universal constant. Tune to element size and context.
