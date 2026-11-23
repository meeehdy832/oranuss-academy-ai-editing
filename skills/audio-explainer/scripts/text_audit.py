#!/usr/bin/env python3
"""Every on-screen text next to the words actually spoken at that moment — to catch invented or misheard text.
Usage: text_audit.py WORKDIR  → writes WORKDIR/text_audit.txt, prints only the path and the count.
Rule: a text stays only if the speaker clearly says it (or it is the plain name of what he describes).
Unclear audio → remove the text (or keep the icon only). Never guess a number."""
import json, sys, os
W = sys.argv[1]
words = json.load(open(os.path.join(W, "words_clean.json"), encoding="utf-8"))
beats = json.load(open(os.path.join(W, "beats.json"), encoding="utf-8"))["beats"]
said = lambda a, b: " ".join(w["text"] for w in words if a <= w["start"] < b)
lines = []
for i, b in enumerate(beats):
    t = [b.get("title", ""), b.get("sub", "")] + [x.get("label", "") for x in b.get("items", [])]
    t += [b[k]["label"] for k in ("left", "right") if b.get(k)]
    t += [f"{b['value']}{b.get('suffix', '')}"] if b.get("value") is not None else []
    for fx in b.get("fx", []):
        t += [fx.get(k, "") for k in ("title", "label", "sub", "text")] + [x.get("label", "") for x in fx.get("items", [])]
    t = [x for x in t if x]
    if t:
        lines.append(f"#{i:02d} {b['from']:6.1f} {b['type']:7} | {' || '.join(t)}\n      SAID: {said(b['from'] - 1.5, b['to'])[:240]}")
open(os.path.join(W, "text_audit.txt"), "w").write("\n".join(lines))
print(f"{len(lines)} scenes with text → {W}/text_audit.txt")
