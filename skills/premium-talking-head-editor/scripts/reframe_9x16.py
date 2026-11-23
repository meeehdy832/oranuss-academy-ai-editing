#!/usr/bin/env python3
"""Reframe a horizontal talking-head clip to vertical 9:16, keeping the speaker's nose
on the vertical center line.

Detection: MediaPipe FaceLandmarker (nose tip) if a model file is given with --model,
otherwise OpenCV's bundled Haar cascades (nose estimated from the face box).
The crop path is smoothed and reset on hard cuts so it never jitters.

Usage:
  python3 reframe_9x16.py input.mp4 output.mp4 [--model face_landmarker.task] [--debug track.json]
"""
import argparse, json, os, subprocess, sys, tempfile
import numpy as np
import cv2


def detect_haar(gray, cascades):
    best = None
    for c in cascades:
        faces = c.detectMultiScale(gray, 1.1, 5, minSize=(gray.shape[0] // 10,) * 2)
        for (x, y, w, h) in faces:
            if best is None or w * h > best[2] * best[3]:
                best = (x, y, w, h)
    if best is None:
        return None
    x, y, w, h = best
    return x + w / 2.0  # nose x is about the face-box center


def make_mediapipe(model):
    import mediapipe as mp
    from mediapipe.tasks import python as mpp
    from mediapipe.tasks.python import vision
    opts = vision.FaceLandmarkerOptions(base_options=mpp.BaseOptions(model_asset_path=model), num_faces=3)
    lm = vision.FaceLandmarker.create_from_options(opts)

    def det(frame_bgr):
        img = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
        res = lm.detect(img)
        if not res.face_landmarks:
            return None
        # largest face: widest landmark spread
        f = max(res.face_landmarks, key=lambda L: max(p.x for p in L) - min(p.x for p in L))
        return f[1].x * frame_bgr.shape[1]  # landmark 1 = nose tip
    return det


def scene_cuts(frames_small, thresh=0.45):
    cuts = [0]
    prev = None
    for i, f in enumerate(frames_small):
        h = cv2.calcHist([f], [0, 1], None, [16, 16], [0, 180, 0, 256])
        cv2.normalize(h, h)
        if prev is not None and cv2.compareHist(prev, h, cv2.HISTCMP_BHATTACHARYYA) > thresh:
            cuts.append(i)
        prev = h
    return cuts


def smooth_segment(xs, alpha=0.08, deadzone=0.0):
    out, cur = [], None
    for x in xs:
        if cur is None:
            cur = x
        elif abs(x - cur) > deadzone:
            cur = cur + alpha * (x - cur)
        out.append(cur)
    # backward pass to remove lag
    back, cur = [], None
    for x in reversed(out):
        cur = x if cur is None else cur + alpha * (x - cur)
        back.append(cur)
    return list(reversed(back))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input"); ap.add_argument("output")
    ap.add_argument("--model", help="MediaPipe face_landmarker.task (optional)")
    ap.add_argument("--width", type=int, default=1080); ap.add_argument("--height", type=int, default=1920)
    ap.add_argument("--debug", help="write per-frame nose x track to this json")
    ap.add_argument("--crf", type=int, default=16)
    a = ap.parse_args()

    cap = cv2.VideoCapture(a.input)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    crop_w = int(round(H * 9 / 16)) // 2 * 2
    if crop_w > W:
        sys.exit("Source is already narrower than 9:16; nothing to crop.")

    det = make_mediapipe(a.model) if a.model and os.path.exists(a.model) else None
    if det is None:
        here = os.path.dirname(os.path.abspath(__file__))
        cascades = []
        for n in ("haarcascade_frontalface_default.xml", "haarcascade_profileface.xml"):
            for d in (here, getattr(getattr(cv2, "data", None), "haarcascades", "")):
                c = cv2.CascadeClassifier(os.path.join(d, n))
                if not c.empty():
                    cascades.append(c); break
        if not cascades:
            sys.exit("No face detector found: keep the haarcascade_*.xml files next to this script, or pass --model.")

    # pass 1: detect (every frame, on a downscaled copy for speed)
    scale = 640 / W
    raw, smalls = [], []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        small = cv2.resize(fr, (640, int(H * scale)))
        smalls.append(cv2.cvtColor(cv2.resize(small, (160, int(H * scale / 4))), cv2.COLOR_BGR2HSV))
        x = det(fr) if det else detect_haar(cv2.cvtColor(small, cv2.COLOR_BGR2GRAY), cascades)
        raw.append(None if x is None else (x if det else x / scale))
    cap.release()
    n = len(raw)
    if n == 0:
        sys.exit("No frames read.")

    # fill gaps, smooth per shot
    cuts = scene_cuts(smalls) + [n]
    track = [None] * n
    for s, e in zip(cuts[:-1], cuts[1:]):
        seg = raw[s:e]
        known = [i for i, v in enumerate(seg) if v is not None]
        if not known:
            filled = [W / 2] * len(seg)
        else:
            filled = list(np.interp(range(len(seg)), known, [seg[i] for i in known]))
        sm = smooth_segment(filled, alpha=0.08, deadzone=W * 0.01)
        track[s:e] = sm
    lefts = [int(min(max(x - crop_w / 2, 0), W - crop_w)) for x in track]

    if a.debug:
        json.dump({"fps": fps, "src": [W, H], "crop_w": crop_w, "cuts": cuts[:-1],
                   "detected_ratio": sum(v is not None for v in raw) / n, "left": lefts}, open(a.debug, "w"))

    # pass 2: write cropped frames, then mux original audio
    tmp = tempfile.mkdtemp()
    vid = os.path.join(tmp, "v.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
                          "-s", f"{a.width}x{a.height}", "-r", str(fps), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", str(a.crf), "-pix_fmt", "yuv420p", vid],
                         stdin=subprocess.PIPE)
    cap = cv2.VideoCapture(a.input)
    for i in range(n):
        ok, fr = cap.read()
        if not ok:
            break
        c = fr[:, lefts[i]:lefts[i] + crop_w]
        p.stdin.write(cv2.resize(c, (a.width, a.height), interpolation=cv2.INTER_LANCZOS4).tobytes())
    p.stdin.close(); p.wait(); cap.release()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", a.input, "-map", "0:v", "-map", "1:a?",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", a.output], check=True)
    print(json.dumps({"output": a.output, "frames": n, "shots": len(cuts) - 1,
                      "face_detected_ratio": round(sum(v is not None for v in raw) / n, 3),
                      "detector": "mediapipe" if det else "haar"}))


if __name__ == "__main__":
    main()
