#!/usr/bin/env python3
"""Download the chosen Pexels media, check resolution, cut clips to their scene length, copy into Remotion,
and make ONE small labelled contact sheet to review.

Usage: fetch_media.py WORKDIR REMOTION_DIR [--pick name=2 ...]
Inputs : WORKDIR/media_candidates.json  ({"photos": {name: [id, id2, id3]}, "videos": {v_key: [url, url2, url3]}})
         WORKDIR/beats.json             (image beats use "img": "img/<name>.jpg", video beats "video": "vid/<v_key>.mp4")
--pick name=2  → use the 2nd candidate for that name (to swap an off-topic pick without searching again).
Outputs: REMOTION_DIR/public/img/<name>.jpg (2400 px), public/vid/<v_key>.mp4 (1920×1080, 30 fps, exact scene length,
         looped if short, no audio), WORKDIR/media/credits.json, WORKDIR/media/sheet.jpg (review this, ~1.5k tokens).
Prints one line per problem only, then a summary.
"""
import json, os, sys, subprocess, urllib.request
from concurrent.futures import ThreadPoolExecutor

W, R = sys.argv[1], sys.argv[2]
picks = dict(a.split("=") for a in sys.argv[3:] if "=" in a and not a.startswith("--"))
cand = json.load(open(os.path.join(W, "media_candidates.json")))
beats = json.load(open(os.path.join(W, "beats.json"), encoding="utf-8"))["beats"]
M = os.path.join(W, "media"); os.makedirs(f"{M}/raw", exist_ok=True)
os.makedirs(f"{R}/public/img", exist_ok=True); os.makedirs(f"{R}/public/vid", exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36", "Accept": "*/*"}
need_vid = {b["video"].split("/")[-1][:-4]: b["to"] - b["from"] + 0.6 for b in beats if b.get("video")}
need_img = {b["img"].split("/")[-1][:-4] for b in beats if b.get("img") and b["type"] == "image"}
problems, credits = [], {}

def choose(kind, k):
    lst = cand[kind].get(k) or []
    i = int(picks.get(k, 1)) - 1
    return lst[i] if i < len(lst) else None

def photo(k):
    pid = choose("photos", k)
    if not pid: problems.append(f"no photo for {k}"); return
    url = f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=2400"
    dst = f"{R}/public/img/{k}.jpg"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r, open(dst, "wb") as f: f.write(r.read())
    except Exception as e:
        problems.append(f"{k}: download failed ({e})"); return
    w = subprocess.run(["sips", "-g", "pixelWidth", dst], capture_output=True, text=True).stdout.split()[-1]
    if int(w) < 1920: problems.append(f"{k}: only {w}px wide")
    credits[k] = f"https://www.pexels.com/photo/{pid}/"

def video(k):
    url = choose("videos", k)
    if not url: problems.append(f"no clip for {k}"); return
    raw = f"{M}/raw/{k}.mp4"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r, open(raw, "wb") as f: f.write(r.read())
    except Exception as e:
        problems.append(f"{k}: download failed ({e})"); return
    d = need_vid[k]
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-ss", "0.8", "-i", raw, "-t", f"{d:.2f}", "-an", "-vf",
        "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,setsar=1", "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "21", "-pix_fmt", "yuv420p", "-movflags", "+faststart", f"{R}/public/vid/{k}.mp4"], capture_output=True, text=True)
    if r.returncode: problems.append(f"{k}: ffmpeg failed")
    credits[k] = url

with ThreadPoolExecutor(8) as ex:
    list(ex.map(photo, sorted(need_img))); list(ex.map(video, sorted(need_vid)))
json.dump(credits, open(f"{M}/credits.json", "w"), indent=1)

# one small sheet: photo + first frame of each clip, labelled (Pillow via uv, nothing installed globally)
for k in need_vid:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", f"{R}/public/vid/{k}.mp4", "-frames:v", "1", "-vf", "scale=480:-2", f"{M}/raw/{k}.jpg"])
sheet = os.path.join(os.path.dirname(__file__), "sheet.py")
items = [f"{R}/public/img/{k}.jpg" for k in sorted(need_img)] + [f"{M}/raw/{k}.jpg" for k in sorted(need_vid)]
subprocess.run(["uv", "run", "--quiet", "--python", "3.12", "--with", "pillow", "python", sheet, f"{M}/sheet.jpg", *items], check=False)
for p in problems: print("⚠", p)
print(f"{len(need_img)} photos + {len(need_vid)} clips ready · review {M}/sheet.jpg · swap with --pick name=2")
