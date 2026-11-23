# Example: premium card entrance

## Intent
A card rises slightly while fading in and settles without overshoot.

## Motion spec
- translateY: 20 px → 0 px
- opacity: 0 → 1
- duration: 480 ms
- curve: soft ease-out
- delay: 0–100 ms depending on hierarchy
- reduced motion: opacity only or immediate display

## CSS example
```css
.card {
  animation: card-enter 480ms cubic-bezier(0.22, 1, 0.36, 1) both;
}

@keyframes card-enter {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .card {
    animation: none;
    opacity: 1;
    transform: none;
  }
}
```
