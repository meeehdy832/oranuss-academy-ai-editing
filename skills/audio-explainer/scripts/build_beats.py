#!/usr/bin/env python3
"""Turn a short plan into timed beats.

Usage: build_beats.py WORKDIR [--max-image 7]
Reads WORKDIR/plan.json and WORKDIR/words_clean.json, writes WORKDIR/beats.json, prints a compact report
(scene count, media vs animation share, too-long / too-short scenes). Nothing else is printed.

plan.json = {"duration": 972.9, "audio": "audio/voice.m4a", "beats": [ ... ]}
Each beat is a scene spec (see SKILL.md) plus ONE timing key:
  "anchor": "word as whisper wrote it", "near": 61      → starts 0.25 s before that word (searched ±25 s)
  "t": 78                                              → starts at 78 s
  "fill": true  (with "t")                             → media inserted inside a long scene: takes only the last
                                                         --max-image seconds before the next beat
Scene end = next scene start.
"""
import json, sys, os, re

W = sys.argv[1]
MAXI = float(sys.argv[sys.argv.index("--max-image") + 1]) if "--max-image" in sys.argv else 7.0
plan = json.load(open(os.path.join(W, "plan.json"), encoding="utf-8"))
words = json.load(open(os.path.join(W, "words_clean.json"), encoding="utf-8"))
norm = lambda s: re.sub(r"[ً-ْـ\"'“”.,،؟?!:]", "", s.lower()).translate(str.maketrans("أإآىة", "ااايه"))
dur = plan["duration"]
miss = []

def find(a, near, win=25):
    best = None
    for w in words:
        if norm(a) in norm(w["text"]) and abs(w["start"] - near) <= win:
            d = abs(w["start"] - near)
            if best is None or d < best[0]: best = (d, w["start"])
    if best is None: miss.append(a); return near
    return round(best[1] - 0.25, 2)

B = []
for b in plan["beats"]:
    b = dict(b)
    t = find(b.pop("anchor"), b.pop("near")) if "anchor" in b else b.pop("t")
    B.append(dict(b, _t=t))
B.sort(key=lambda x: x["_t"])
for i, b in enumerate(B):
    if b.pop("fill", False) and i + 1 < len(B):
        b["_t"] = max(b["_t"], round(B[i + 1]["_t"] - MAXI, 2))
B.sort(key=lambda x: x["_t"])
out = []
for i, b in enumerate(B):
    nxt = B[i + 1]["_t"] if i + 1 < len(B) else dur
    o = {k: v for k, v in b.items() if k != "_t"}
    o["from"], o["to"] = b["_t"], round(min(nxt, dur), 2)
    out.append(o)
json.dump({"duration": dur, "audio": plan.get("audio", "audio/voice.m4a"), "beats": out}, open(os.path.join(W, "beats.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

media = sum(b["to"] - b["from"] for b in out if b["type"] in ("image", "video", "cutout"))
long_ = [(i, round(b["to"] - b["from"], 1)) for i, b in enumerate(out) if b["to"] - b["from"] > 14]
short = [(i, round(b["to"] - b["from"], 1)) for i, b in enumerate(out) if b["to"] - b["from"] < 3]
print(f"{len(out)} scenes · media {media / dur:.0%} / animation {1 - media / dur:.0%}"
      + (f" · long>14s {long_}" if long_ else "") + (f" · short<3s {short}" if short else "")
      + (f" · anchors not found: {miss}" if miss else ""))
