"""Motion QA for a rendered video, compared with the 24-reference measurements.

usage:  python motion_qa.py <video.mp4> [out_dir]
needs:  pip install --user numpy opencv-python-headless matplotlib

Prints:
  - frozen frames in the body (refs: median longest frozen run 2.5f, mean frozen 5%)
  - big motion events per second (refs: 0.45-0.95/s, median ~0.65)
  - median velocity profile around peaks + best-fitting easing (refs: cubic-bezier(.85,0,.15,1) ~30-37f)
  - sharpness at velocity peaks vs. resting (refs: ~15% => strong motion blur)
Writes: <out_dir>/<name>_timeline.png and <name>_sheet.png (every 6th frame).
"""
import sys, os
import cv2, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AW = 240


def runs(mask):
    out, s = [], None
    for i, m in enumerate(mask):
        if m and s is None: s = i
        if not m and s is not None: out.append((s, i - 1)); s = None
    if s is not None: out.append((s, len(mask) - 1))
    return out


def analyze(path):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    prev = prev_h = None
    rows, thumbs = [], []
    i = 0
    while True:
        ok, fr = cap.read()
        if not ok: break
        h, w = fr.shape[:2]
        small = cv2.resize(fr, (AW, int(h * AW / w)), interpolation=cv2.INTER_AREA)
        if i % 6 == 0: thumbs.append((i, cv2.resize(fr, (160, int(h * 160 / w)))))
        g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 4, 4], [0, 180, 0, 256, 0, 256]); cv2.normalize(hist, hist)
        r = dict(f=i, diff=0.0, hist=0.0, flow=0.0, sharp=cv2.Laplacian(g, cv2.CV_64F).var())
        if prev is not None:
            r["diff"] = float(np.abs(g.astype(np.int16) - prev.astype(np.int16)).mean())
            r["hist"] = 1 - float(cv2.compareHist(prev_h, hist, cv2.HISTCMP_CORREL))
            fl = cv2.calcOpticalFlowFarneback(prev, g, None, 0.5, 4, 15, 3, 5, 1.2, 0)
            r["flow"] = float(np.linalg.norm(fl, axis=2).mean())
        rows.append(r); prev, prev_h = g, hist; i += 1
    cap.release()
    return fps, rows, thumbs


def main():
    path = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(path))
    os.makedirs(out, exist_ok=True)
    name = os.path.splitext(os.path.basename(path))[0]
    fps, rows, thumbs = analyze(path)
    n = len(rows)
    d = np.array([r["diff"] for r in rows]); fl = np.array([r["flow"] for r in rows])
    hs = np.array([r["hist"] for r in rows]); sh = np.array([r["sharp"] for r in rows])
    cut = (hs > 0.35) & (d > 8)
    body = slice(1, max(2, n - int(fps * 1.5)))  # exclude the last 1.5s (end card)
    frozen = d[body] < 0.06
    rr = runs(frozen); longest = max([e - s + 1 for s, e in rr] or [0])
    fm = fl.copy(); fm[cut] = 0
    thr = max(0.6, np.percentile(fm, 30) * 3)
    ev = []
    for s, e in runs(fm > thr):
        if e - s < 2: continue
        pk = s + int(np.argmax(fm[s:e + 1]))
        if fm[pk] >= 2: ev.append(pk)
    W0 = W1 = 14
    prof = []
    for pk in ev:
        if pk - W0 < 0 or pk + W1 >= n or cut[pk - W0:pk + W1 + 1].any(): continue
        seg = fm[pk - W0:pk + W1 + 1] / fm[pk]
        if seg.max() <= 1.01: prof.append(seg)
    print(f"video: {name}  {n}f @ {fps:.2f}fps  ({n / fps:.1f}s)  hard cuts: {int(cut.sum())}")
    print(f"frozen in body: {100 * frozen.mean():.1f}%  longest frozen run: {longest}f   [refs: ~5%, median 2.5f, ideal <= 3f outside final hold]")
    print(f"big motion events: {len(ev)} = {len(ev) / (n / fps):.2f}/s   [refs: 0.45-0.95/s]")
    if prof:
        med = np.median(np.array(prof), axis=0)
        print("median velocity around peaks (-6..+8):", " ".join(f"{x:.2f}" for x in med[W0 - 6:W0 + 9]))
        print("   refs (-6..+8):                    0.14 0.18 0.23 0.29 0.42 0.68 1.00 0.64 0.36 0.27 0.19 0.15 0.13 0.11 0.09")
    if ev:
        ratio = []
        for pk in ev:
            before = sh[max(0, pk - 15):max(1, pk - 6)].max() if pk > 6 else sh[pk]
            ratio.append(sh[pk] / max(before, 1))
        print(f"sharpness at peaks / resting: median {np.median(ratio):.2f}   [refs: ~0.15 => strong motion blur]")
    # plots
    f = np.arange(n)
    fig, ax = plt.subplots(3, 1, figsize=(16, 7), sharex=True)
    ax[0].plot(f, d, lw=.8); ax[0].set_ylabel("diff")
    ax[1].plot(f, fl, lw=.8, c="tab:orange"); ax[1].set_ylabel("flow px/f")
    ax[2].plot(f, sh, lw=.8, c="tab:purple"); ax[2].set_ylabel("sharpness")
    for a in ax:
        for c in np.where(cut)[0]: a.axvline(c, c="r", lw=.5)
        for s, e in rr:
            if e - s >= 3: a.axvspan(s + 1, e + 1, color="red", alpha=.12)
        a.grid(alpha=.3)
    ax[2].set_xticks(np.arange(0, n, 15)); ax[2].tick_params(axis="x", labelsize=7)
    fig.suptitle(f"{name} (red bands = frozen >= 4f)"); fig.tight_layout()
    fig.savefig(os.path.join(out, f"{name}_timeline.png"), dpi=70); plt.close(fig)
    cols = 10; th = thumbs[0][1].shape[0]; tw = thumbs[0][1].shape[1]
    rows_n = (len(thumbs) + cols - 1) // cols
    canvas = np.full((rows_n * (th + 2) + 2, cols * (tw + 2) + 2, 3), 40, np.uint8)
    for k, (i, im) in enumerate(thumbs):
        r, c = divmod(k, cols); y, x = 2 + r * (th + 2), 2 + c * (tw + 2)
        canvas[y:y + th, x:x + tw] = im
        cv2.putText(canvas, str(i), (x + 3, y + 12), cv2.FONT_HERSHEY_SIMPLEX, .4, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.imwrite(os.path.join(out, f"{name}_sheet.png"), canvas)
    print("wrote:", os.path.join(out, f"{name}_timeline.png"), "and", os.path.join(out, f"{name}_sheet.png"))


if __name__ == "__main__":
    main()
