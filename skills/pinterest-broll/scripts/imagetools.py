"""
Image work for pinterest-broll, run inside an isolated uv environment:
    uv run --python 3.12 --with pillow [--with "rembg[cpu]"] imagetools.py jobs.json
jobs.json: {"size":[W,H], "jobs":[{"op":"keep"|"cutout", "src":..., "dst":...}], "sheet":{"dst":..., "cells":[{"img":..., "label":..., "cutout":bool}]}}
"""
import json, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps


def cover(src, dst, W, H):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im = ImageOps.fit(im, (W, H), method=Image.Resampling.LANCZOS, centering=(0.5, 0.45))
    im.save(dst, quality=92)


def cutouts(pairs):
    if not pairs:
        return
    from rembg import new_session, remove
    session = new_session("isnet-general-use")
    for src, dst in pairs:
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        out = remove(im, session=session, post_process_mask=True)
        bbox = out.getchannel("A").point(lambda a: 255 if a > 16 else 0).getbbox()
        if bbox:
            pad = 16
            l, t, r, b = bbox
            out = out.crop((max(0, l - pad), max(0, t - pad), min(out.width, r + pad), min(out.height, b + pad)))
        out.save(dst)
        print("  cutout", dst, out.size, flush=True)


def checker(w, h, s=16):
    bg = Image.new("RGB", (w, h), (235, 235, 240))
    d = ImageDraw.Draw(bg)
    for y in range(0, h, s):
        for x in range(0, w, s):
            if (x // s + y // s) % 2:
                d.rectangle([x, y, x + s - 1, y + s - 1], fill=(205, 205, 214))
    return bg


def sheet(spec):
    cells = spec["cells"]
    if not cells:
        return
    cw, ch, lab, cols = 420, 300, 46, min(4, len(cells))
    rows = (len(cells) + cols - 1) // cols
    S = Image.new("RGB", (cols * cw + (cols + 1) * 14, rows * (ch + lab) + (rows + 1) * 14), (16, 8, 32))
    try:
        font = ImageFont.load_default(size=20)
    except TypeError:
        font = ImageFont.load_default()
    d = ImageDraw.Draw(S)
    for i, c in enumerate(cells):
        x = 14 + (i % cols) * (cw + 14)
        y = 14 + (i // cols) * (ch + lab + 14)
        im = Image.open(c["img"])
        tile = checker(cw, ch) if c.get("cutout") else Image.new("RGB", (cw, ch), (30, 22, 50))
        im.thumbnail((cw, ch), Image.Resampling.LANCZOS)
        tile.paste(im, ((cw - im.width) // 2, (ch - im.height) // 2), im if im.mode == "RGBA" else None)
        S.paste(tile, (x, y))
        d.text((x + 4, y + ch + 10), c["label"][:44], fill=(240, 236, 255), font=font)
    S.save(spec["dst"], quality=90)
    print("  sheet", spec["dst"], flush=True)


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    W, H = spec["size"]
    for j in spec["jobs"]:
        if j["op"] == "keep":
            cover(j["src"], j["dst"], W, H)
            print("  keep  ", j["dst"], flush=True)
    cutouts([(j["src"], j["dst"]) for j in spec["jobs"] if j["op"] == "cutout"])
    if spec.get("sheet"):
        sheet(spec["sheet"])


if __name__ == "__main__":
    main()
