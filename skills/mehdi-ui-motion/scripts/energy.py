"""Usage: python energy.py VIDEO [START END]
Gates (pro standard, references/07-pro-standard.md): max <= 15, no run >= 12f below 0.2, median >= ~0.6, no flat-colour run >= 2f.
The comparison report's metric: mean abs luma difference between consecutive frames, gray, width 180.
Also prints spikes > 15, freeze runs (>=15f below 0.2), solid-color frames, and a compact series."""
import sys, cv2, numpy as np
def energy(path):
    cap = cv2.VideoCapture(path); prev = None; out = []; solid = []
    while True:
        ok, fr = cap.read()
        if not ok: break
        h, w = fr.shape[:2]
        g = cv2.cvtColor(cv2.resize(fr, (180, int(round(h * 180 / w))), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.int16)
        solid.append(float(g.std()) < 2.0)
        out.append(0.0 if prev is None else float(np.abs(g - prev).mean()))
        prev = g
    return np.array(out), np.array(solid)
if __name__ == "__main__":
    path = sys.argv[1]; e, solid = energy(path)
    n = len(e)
    print(f"{path.split('/')[-1]}: {n} frames  max {e.max():.1f} @ {int(e.argmax())}  mean {e[1:].mean():.2f}  median {np.median(e[1:]):.2f}")
    print("spikes > 15:", [(i, round(v, 1)) for i, v in enumerate(e) if v > 15])
    runs = []; s = None
    for i in range(1, n):
        if e[i] < 0.2:
            s = i if s is None else s
        else:
            if s is not None and i - s >= 8: runs.append((s, i - 1, i - s))
            s = None
    if s is not None and n - s >= 8: runs.append((s, n - 1, n - s))
    print("low-energy runs (<0.2, >=8f):", runs)
    sr = []; s = None
    for i in range(n):
        if solid[i]: s = i if s is None else s
        else:
            if s is not None and i - s >= 2: sr.append((s, i - 1))
            s = None
    print("solid-color runs (>=2f):", sr)
    if len(sys.argv) > 2:
        a, b = int(sys.argv[2]), int(sys.argv[3])
        print(" ".join(f"{i}:{e[i]:.1f}" for i in range(a, min(b + 1, n))))
