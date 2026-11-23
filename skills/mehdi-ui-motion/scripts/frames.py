"""Frame sheets for studying a video (reference or your own render) frame by frame.

usage:
  python frames.py <video.mp4> sheet START END STEP [COLS] [THUMB_W] [x0 y0 x1 y1]   -> contact sheet (crop = fractions)
  python frames.py <video.mp4> frame N [x0 y0 x1 y1]                                 -> one full-res frame
Outputs next to the video in a folder <name>_frames/. Each thumbnail is labeled with its frame number.
Tip: STEP 1 over a transition window (10-30 frames) = true frame-by-frame study.
"""
import sys, os, cv2, numpy as np


def frames(path, start, end, step):
    cap = cv2.VideoCapture(path); i = 0
    while True:
        ok, fr = cap.read()
        if not ok or i > end: break
        if i >= start and (i - start) % step == 0: yield i, fr
        i += 1
    cap.release()


def crop(fr, c):
    if not c: return fr
    H, W = fr.shape[:2]
    return fr[int(c[1] * H):int(c[3] * H), int(c[0] * W):int(c[2] * W)]


a = sys.argv[1:]
path, mode = a[0], a[1]
outdir = os.path.join(os.path.dirname(os.path.abspath(path)), os.path.splitext(os.path.basename(path))[0] + "_frames")
os.makedirs(outdir, exist_ok=True)
if mode == "frame":
    n = int(a[2]); c = tuple(map(float, a[3:7])) if len(a) >= 7 else None
    for i, fr in frames(path, n, n, 1):
        p = os.path.join(outdir, f"f{n}.png"); cv2.imwrite(p, crop(fr, c)); print(p)
else:
    s, e, st = int(a[2]), int(a[3]), int(a[4])
    cols = int(a[5]) if len(a) > 5 else 8
    tw = int(a[6]) if len(a) > 6 else 180
    c = tuple(map(float, a[7:11])) if len(a) >= 11 else None
    ims = []
    for i, fr in frames(path, s, e, st):
        fr = crop(fr, c); h, w = fr.shape[:2]
        ims.append((i, cv2.resize(fr, (tw, int(h * tw / w)), interpolation=cv2.INTER_AREA)))
    th = ims[0][1].shape[0]; rows = (len(ims) + cols - 1) // cols
    canvas = np.full((rows * (th + 2) + 2, cols * (tw + 2) + 2, 3), 40, np.uint8)
    for k, (i, im) in enumerate(ims):
        r, cc = divmod(k, cols); y, x = 2 + r * (th + 2), 2 + cc * (tw + 2)
        canvas[y:y + th, x:x + tw] = im
        cv2.rectangle(canvas, (x, y), (x + 9 * len(str(i)) + 6, y + 16), (0, 0, 0), -1)
        cv2.putText(canvas, str(i), (x + 3, y + 12), cv2.FONT_HERSHEY_SIMPLEX, .42, (0, 255, 255), 1, cv2.LINE_AA)
    p = os.path.join(outdir, f"sheet_{s}-{e}_s{st}.png"); cv2.imwrite(p, canvas); print(p)
