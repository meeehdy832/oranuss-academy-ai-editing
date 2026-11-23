"""Attach idea animations (scripts/fx_plan.json) to beats_doc.json, timing each one on its spoken word.

Each fx (and each fx item) may carry `cue`: a word as Whisper wrote it. The first matching word inside the
beat (from 0.3 s before it starts) gives `at` = seconds from the beat start. Missing cues fall back to
evenly spaced times and are reported.
Usage: python3 cue_fx.py WORKDIR BEATS_JSON   (reads WORKDIR/fx_plan.json + WORKDIR/words_clean.json, edits BEATS_JSON in place)
fx_plan.json = {"<beat index>": [ {fx}, ... ]}  — fx kinds and fields: see template/IdeaFx.tsx (type Fx).
"""
import json, re, pathlib

import sys
W = pathlib.Path(sys.argv[1])
BEATS = pathlib.Path(sys.argv[2])
PLAN = W / "fx_plan.json"
WORDS = W / "words_clean.json"


def norm(s: str) -> str:
    s = re.sub(r"[ً-ْـ\"'“”.,،؟?!:]", "", s.lower())
    return s.translate(str.maketrans("أإآىة", "ااايه"))


doc = json.loads(BEATS.read_text())
plan = json.loads(PLAN.read_text())
words = json.loads(WORDS.read_text())
missing = []


def find(cue, b, after=0.0):
    c = norm(cue)
    for w in words:
        if b["from"] - 0.3 <= w["start"] < b["to"] and w["start"] - b["from"] >= after and c in norm(w["text"]):
            return round(max(0.15, w["start"] - b["from"]), 2)
    return None


for i, b in enumerate(doc["beats"]):
    b.pop("fx", None)
    fxs = plan.get(str(i))
    if not fxs:
        continue
    out = []
    for fx in fxs:
        fx = json.loads(json.dumps(fx))
        if "cue" in fx:
            at = find(fx.pop("cue"), b)
            if at is None:
                missing.append((i, "fx"))
            fx.setdefault("at", at if at is not None else 0.4)
        items = fx.get("items") or []
        last = fx.get("at", 0.3)
        for j, it in enumerate(items):
            if "cue" in it:
                at = find(it.pop("cue"), b, after=0)
                if at is None:
                    missing.append((i, it["label"]))
                    at = last + 0.8
                it["at"] = max(at, last + 0.25) if j else at
            if "at" in it:
                last = it["at"]
        if items and "at" not in fx:
            fx["at"] = max(0.2, min(it.get("at", 0.4) for it in items) - 0.4)
        out.append(fx)
    b["fx"] = out

BEATS.write_text(json.dumps(doc, ensure_ascii=False, indent=1))
print("beats with fx:", sum(1 for b in doc["beats"] if b.get("fx")), "/", len(doc["beats"]))
print("cues not found (fell back):", missing)
