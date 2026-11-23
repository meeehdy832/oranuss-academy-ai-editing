# Realistic PNG objects (Pinterest → cutout → animate)

Tested 2026-11-10 (`edits/pinterest_test`, output `pinterest_money_test_1080p.mp4`). Kit: `tools/png_kit/` in the B-rolls project.

## When to use
A key line names a real object (money, gold, car, watch, phone, product, logo) → show the real object as a cutout instead of a flat icon. 1 object per beat, 1.5–2.5 s, never cover the face or the burned-in logo.

## Get the image
1. Pinterest search in the browser pane (user is logged in there): `pinterest.com/search/pins/?q=<object> png`. The Pinterest MCP is installed but only reads the user's own boards and has no token; the browser pane is the working route.
2. Collect `/236x/` thumbnail hashes with JS, show a lettered contact sheet in the pane (A1…F12), pick, **ask before downloading**.
3. `tools/png_kit/pin_fetch.sh <dir> name hash …` (tries originals .png → .jpg → 736x).
4. Most "PNG" pins are fake (baked checkerboard/white). Always run `tools/png_kit/cutout in out.png` (Apple Vision foreground mask, offline, crops to object). Check on navy before use.
5. Reject: under ~600 px on the long side for hero use, visible watermarks, odd crops. Rights: Pinterest images are other people's work — fine for tests/refs; for published videos prefer the user's own, free-license, or generated images, and tell the user.

## Make it look real (see `png_objects_demo.js`)
- **Contact shadow**: radial ellipse on the floor under the object; scale it with height (small when high, full on landing).
- **Double drop-shadow** on the img: soft `0 30px 40px rgba(0,0,0,.55)` + 2 px light rim.
- **Shine sweep masked by the object**: div with `mask-image:url(same.png)`, a white 100° gradient bar crossing in 0.6–0.8 s, `mix-blend-mode:screen`. Only on metal/glass (gold, watch, $, phone).
- **Landing**: squash 12 %, ring shockwave on the floor, 0.2 white flash, decaying camera shake (≈14 px, e^-9t) — once per beat, not every element.
- **Speed**: fast entries get 3 blurred ghost copies trailing (opacity ∝ velocity) + speed lines; 3D `rotateY` spin on drops.
- **Idle life**: bob ±8 px, rotateY sway ±9°, never fully still.
- **Joins**: whip-pan the stage (0.2 s out + 0.28 s in, blur 40).
- **Finale**: hero shrinks a little, the earlier objects pop back in an arc around it (overshoot, 0.1 s stagger).
- Background: navy radial + masked grid + purple spotlight + grain + vignette.

## SFX (OrcaXV)
Drop/land IM-029 or IM-025, shine PO-016 / UI-041, whip WH-174/175/176, car WH-013, money RW-021 / RW-020, pops PO-006/008/009.

In talk edits the caption word still must be a word he says; the object is the B-roll for that word.
