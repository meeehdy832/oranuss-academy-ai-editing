"""Labelled contact sheet, kept small on purpose (each review image costs context tokens).
Usage: uv run --with pillow python sheet.py OUT.jpg IMG1 IMG2 ...   (label = file name without extension)"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageOps
out, items = sys.argv[1], sys.argv[2:]
cw, ch, cols = 240, 135, 8
rows = (len(items) + cols - 1) // cols
S = Image.new("RGB", (cols * cw, max(1, rows) * ch), (18, 18, 18)); d = ImageDraw.Draw(S)
font = ImageFont.load_default(size=15)
for i, p in enumerate(items):
    try: im = ImageOps.fit(Image.open(p).convert("RGB"), (cw - 2, ch - 2))
    except Exception: continue
    x, y = (i % cols) * cw + 1, (i // cols) * ch + 1
    S.paste(im, (x, y)); n = os.path.splitext(os.path.basename(p))[0]
    d.rectangle([x, y, x + 8 * len(n) + 6, y + 18], fill=(0, 0, 0)); d.text((x + 3, y + 1), n, fill=(255, 220, 0), font=font)
S.save(out, quality=80)
