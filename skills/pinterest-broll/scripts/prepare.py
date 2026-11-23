#!/usr/bin/env python3
"""
pinterest-broll: download the chosen Pinterest pins, then remove or keep their backgrounds.

    python3 prepare.py picks.json

picks.json
{
  "out": "output/my-video/assets/pinterest",      # where everything goes (created)
  "size": [1920, 1080],                            # frame size for "keep" images (video size)
  "items": [
    {"beat": "01-button", "time": 13.6, "line": "words said here", "query": "search used",
     "mode": "cutout" | "keep",
     "pin": {"id": "...", "url": "...", "alt": "...", "original": "...", "fallback": "...", "thumb": "..."}}
  ]
}

Writes  <out>/original/  <out>/cutout/*.png (transparent)  <out>/bg/*.jpg (frame size)
        <out>/assets.json (catalog with the pin link for every file)  <out>/sheet.jpg (contact sheet)
Standard library + curl-free downloads; image work runs in an isolated uv environment (Python 3.12).
"""
import json, os, re, shutil, subprocess, sys, urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


def slug(s):
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()[:48] or "item"


def download(urls, dst):
    for u in urls:
        if not u or not u.startswith("https://i.pinimg.com/"):
            continue
        try:
            req = urllib.request.Request(u, headers={"User-Agent": UA, "Referer": "https://www.pinterest.com/"})
            with urllib.request.urlopen(req, timeout=30) as r:
                ctype = r.headers.get("Content-Type", "")
                data = r.read()
            if not ctype.startswith("image/") or len(data) < 2000:
                continue
            ext = {"image/png": ".png", "image/webp": ".webp", "image/gif": ".gif"}.get(ctype.split(";")[0], ".jpg")
            path = dst + ext
            with open(path, "wb") as f:
                f.write(data)
            return path, u
        except Exception as e:
            print(f"    ! {u.rsplit('/', 1)[-1]}: {e}")
    return None, None


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    picks = json.load(open(sys.argv[1], encoding="utf-8"))
    out = os.path.abspath(picks["out"])
    W, H = picks.get("size", [1920, 1080])
    for d in ("original", "cutout", "bg"):
        os.makedirs(os.path.join(out, d), exist_ok=True)

    catalog_path = os.path.join(out, "assets.json")
    catalog = json.load(open(catalog_path, encoding="utf-8")) if os.path.exists(catalog_path) else {"assets": []}

    jobs, cells, new = [], [], []
    for it in picks["items"]:
        pin, beat, mode = it["pin"], slug(it["beat"]), it.get("mode", "keep")
        base = os.path.join(out, "original", f"{beat}-{pin['id']}")
        existing = [base + e for e in (".jpg", ".png", ".webp", ".gif") if os.path.exists(base + e)]
        if existing:
            src, used = existing[0], "(cached)"
        else:
            src, used = download([pin.get("original"), pin.get("fallback"), pin.get("thumb")], base)
        if not src:
            print(f"  ✗ {beat}: could not download pin {pin['id']}")
            continue
        dst = os.path.join(out, "cutout" if mode == "cutout" else "bg", beat + (".png" if mode == "cutout" else ".jpg"))
        jobs.append({"op": mode, "src": src, "dst": dst})
        cells.append({"img": dst, "label": f"{beat} · {mode}", "cutout": mode == "cutout"})
        print(f"  ↓ {beat}: {os.path.basename(src)} {('from ' + used.split('/')[3]) if used != '(cached)' else used}")
        rec = {
            "beat": beat, "time": it.get("time"), "line": it.get("line", ""), "query": it.get("query", ""),
            "mode": mode, "file": os.path.relpath(dst, out), "original": os.path.relpath(src, out),
            "pin_id": pin["id"], "pin_url": pin.get("url") or f"https://www.pinterest.com/pin/{pin['id']}/",
            "description": pin.get("alt", ""),
            "rights": "unknown — Pinterest images usually belong to someone else; check the owner before publishing",
            "added": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        catalog["assets"] = [a for a in catalog["assets"] if a["beat"] != beat] + [rec]   # one image per beat
        new.append(rec)

    if not jobs:
        print("Nothing to process."); sys.exit(1)
    spec = {"size": [W, H], "jobs": jobs, "sheet": {"dst": os.path.join(out, "sheet.jpg"), "cells": cells}}
    spec_path = os.path.join(out, ".jobs.json")
    json.dump(spec, open(spec_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    uv = shutil.which("uv") or os.path.expanduser("~/.local/bin/uv")
    if not os.path.exists(uv):
        print("uv is needed for the image step: curl -LsSf https://astral.sh/uv/install.sh | sh"); sys.exit(1)
    cmd = [uv, "run", "--quiet", "--python", "3.12", "--with", "pillow"]
    if any(j["op"] == "cutout" for j in jobs):
        cmd += ["--with", "rembg[cpu]"]
        if not os.path.isdir(os.path.expanduser("~/.u2net")):
            print("  (first cutout: downloading the background-removal model once, ~180 MB)")
    cmd += [os.path.join(HERE, "imagetools.py"), spec_path]
    print("Processing images…")
    r = subprocess.run(cmd)
    if r.returncode:
        print("Image step failed."); sys.exit(r.returncode)

    json.dump(catalog, open(catalog_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nDone: {len(new)} assets → {out}")
    print(f"  cutouts: {sum(1 for a in new if a['mode'] == 'cutout')}  backgrounds: {sum(1 for a in new if a['mode'] == 'keep')}")
    print(f"  contact sheet: {os.path.join(out, 'sheet.jpg')}")
    print(f"  catalog: {catalog_path}")


if __name__ == "__main__":
    main()
