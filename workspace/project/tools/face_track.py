# Developed by Mehdi ORANUSS | Powered by Claude
"""Cross-platform face tracker (Windows, Mac, Linux): same output as the macOS Vision helper
project/tools/ves/bin/face-track, for machines without it.
usage: python face_track.py <in.mp4> <out.json> [step_seconds]
Writes [{"t","x","y","w","h","W","H"}] (largest face, pixels, origin top-left).
Needs: pip install "opencv-python-headless<5" and the YuNet model (project/models/face_detection_yunet_2023mar.onnx,
https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet); falls back to Haar cascades without it."""
import json, os, sys
import cv2

src, out = sys.argv[1], sys.argv[2]
step = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
YUNET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models", "face_detection_yunet_2023mar.onnx")
yunet = None
if os.path.exists(YUNET) and hasattr(cv2, "FaceDetectorYN"):
    yunet = cv2.FaceDetectorYN.create(YUNET, "", (320, 320), 0.7, 0.3, 50)
front = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
profile = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")
res, t, last = [], 0.0, None
while t * fps < n:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
    ok, frame = cap.read()
    if not ok:
        break
    s = max(1.0, W / 960)                       # detect on a smaller copy, scale back
    if yunet is not None:
        img = cv2.resize(frame, (int(W / s), int(H / s)))
        yunet.setInputSize((img.shape[1], img.shape[0]))
        _, det = yunet.detect(img)
        faces = [tuple(d[:4]) for d in det] if det is not None else []
    else:
        g = cv2.equalizeHist(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        small = cv2.resize(g, (int(W / s), int(H / s)))
        faces = list(front.detectMultiScale(small, 1.1, 6, minSize=(40, 40)))
    if not faces and yunet is None:
        faces = list(profile.detectMultiScale(small, 1.1, 6, minSize=(40, 40)))
        faces += [(small.shape[1] - x - w, y, w, h) for x, y, w, h in profile.detectMultiScale(cv2.flip(small, 1), 1.1, 6, minSize=(40, 40))]
    if faces:
        x, y, w, h = (float(v) for v in max(faces, key=lambda f: f[2] * f[3]))
        last = {"t": round(t, 3), "x": x * s, "y": y * s, "w": w * s, "h": h * s, "W": W, "H": H}
        res.append(last)
    elif last:                                   # keep the previous box so the crop does not jump
        res.append({**last, "t": round(t, 3)})
    t += step
json.dump(res, open(out, "w"))
print(len(res), "samples")
