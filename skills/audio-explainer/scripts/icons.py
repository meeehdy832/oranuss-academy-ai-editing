#!/usr/bin/env python3
"""Download every flat pictogram the beats use (Microsoft Fluent emoji, high-contrast SVG, MIT licence).
Usage: icons.py WORKDIR REMOTION_DIR   → scans beats.json (+fx) for "icon" names, fetches the missing ones into
public/icons-flat/<name>.svg. Icon name = Fluent name in snake_case (money_bag, chart_increasing, house, key...).
Prints only missing names (pick another name for those)."""
import json, os, sys, urllib.request, urllib.parse
W, R = sys.argv[1], sys.argv[2]
D = f"{R}/public/icons-flat"; os.makedirs(D, exist_ok=True)
beats = json.load(open(os.path.join(W, "beats.json"), encoding="utf-8"))["beats"]
names = set()
def walk(o):
    if isinstance(o, dict):
        if isinstance(o.get("icon"), str): names.add(o["icon"])
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(beats)
names |= {"house", "check_mark_button", "money_bag", "chart_increasing"}  # used by diagrams / media pops
need = [n for n in names if not os.path.exists(f"{D}/{n}.svg")]
if need:
    cache = os.path.expanduser("~/.cache/fluent-tree.json")
    if not os.path.exists(cache):
        urllib.request.urlretrieve("https://api.github.com/repos/microsoft/fluentui-emoji/git/trees/main?recursive=1", cache)
    tree = [x["path"] for x in json.load(open(cache))["tree"] if "/High Contrast/" in x["path"] and x["path"].endswith(".svg")]
    by = {p.split("/")[1].lower().replace(" ", "_").replace("-", "_"): p for p in tree}
    miss = []
    for n in need:
        p = by.get(n)
        if not p: miss.append(n); continue
        urllib.request.urlretrieve("https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/" + urllib.parse.quote(p), f"{D}/{n}.svg")
    if miss: print("⚠ no Fluent icon named:", ", ".join(miss))
print(f"{len(names)} icons ready")
