"""Usage: python hold_jitter.py VIDEO START:END:x0:y0:x1:y1:d|l [...]  (d = dark text on a light bg, l = light text)
Good: jitter < 0.1 px and ~0 sign flips (Chrome pixel-snapping makes slow 2D drifts flip every frame).
Jitter of text during holds: centroid of ink (dark=1 or light=0 text) inside a crop, per frame.
Prints per-frame dy and the deviation from a 5f moving average (jitter)."""
import sys, cv2, numpy as np
path = sys.argv[1]; specs = sys.argv[2:]
cap = cv2.VideoCapture(path); frames = []
while True:
    ok, fr = cap.read()
    if not ok: break
    frames.append(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY).astype(np.float32))
for sp in specs:
    s, e, x0, y0, x1, y1, dark = sp.split(":"); s, e = int(s), int(e)
    x0, y0, x1, y1 = map(int, (x0, y0, x1, y1)); dark = dark == "d"
    cy, cx = [], []
    for f in range(s, e + 1):
        g = frames[f][y0:y1, x0:x1]
        m = np.clip((180 - g) / 180, 0, 1) if dark else np.clip((g - 90) / 160, 0, 1)
        ys, xs = np.mgrid[0:g.shape[0], 0:g.shape[1]]
        cy.append((m * ys).sum() / m.sum()); cx.append((m * xs).sum() / m.sum())
    dy, dx = np.diff(cy), np.diff(cx)
    k = np.ones(5) / 5
    jy = np.abs(dy - np.convolve(dy, k, "same"))[2:-2]; jx = np.abs(dx - np.convolve(dx, k, "same"))[2:-2]
    print(f"{s}-{e}: mean step y {dy.mean():+.3f} x {dx.mean():+.3f} | jitter y {jy.mean():.3f} (max {jy.max():.2f}) x {jx.mean():.3f} (max {jx.max():.2f}) | sign flips y {int(np.sum(np.sign(dy[1:])!=np.sign(dy[:-1])))}/{len(dy)-1}")
