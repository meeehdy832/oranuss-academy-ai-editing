#!/usr/bin/env python3
"""2D talking puppet renderer: lip-sync from voice envelope, blinks, breathing, pose swaps,
animated motion background (no images needed), FX layer (icons, audio waves, radial badge, orbit,
bursts, floaters, converging particles), camera punch-ins and character entrances.
Run with project/.venv-puppet/bin/python:
  puppet2d.py key   <pose.png> <out.png>            green-screen key -> RGBA cutout
  puppet2d.py env   <voice.wav> <env.json>           30 fps mouth envelope
  puppet2d.py render <config.json> <out.mp4> [t0 t1] frames -> ffmpeg (video only)
Config example: project/work/whatsapp-lesson/make_puppet_cfg.py"""
import json, math, subprocess, sys, wave, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H, FPS = 1080, 1920, 30
FF = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"


# ---------- green key ----------
def key(src, dst):
    im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    spill = g - np.maximum(r, b)
    a = np.clip(1.0 - (spill - 40) / 60.0, 0, 1)
    g2 = np.where(spill > 0, np.maximum(r, b) + spill * 0.15, g)
    out = np.dstack([r, np.minimum(g, g2), b, a * 255]).astype(np.uint8)
    img = Image.fromarray(out)
    al = img.getchannel("A").filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    img.putalpha(al)
    img = img.crop(img.getbbox())
    img.save(dst)
    print("key", dst, img.size)


# ---------- mouth envelope ----------
def env(wav, dst):
    subprocess.run([FF, "-v", "error", "-y", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "wav", "/tmp/_env16.wav"], check=True)
    with wave.open("/tmp/_env16.wav") as f:
        x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    hop = 16000 // FPS
    n = len(x) // hop
    rms = np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop] ** 2)) for i in range(n)])
    db = 20 * np.log10(rms + 1e-6)
    lo, hi = np.percentile(db, 20), np.percentile(db, 97)
    v = np.clip((db - lo) / (hi - lo), 0, 1)
    v = np.convolve(v, [0.25, 0.5, 0.25], mode="same")
    lv, out, hold = 0, [], 0
    for s in v:
        t = 0 if s < 0.22 else 1 if s < 0.45 else 2 if s < 0.7 else 3
        if t != lv and hold >= 2:
            lv, hold = t, 0
        hold += 1
        out.append(lv)
    json.dump({"fps": FPS, "level": out, "raw": [round(float(s), 3) for s in v]}, open(dst, "w"))
    print("env", dst, n, "frames")


# ---------- easing ----------
def ease(x):
    x = min(max(x, 0), 1)
    return x * x * (3 - 2 * x)


def back(x, s=1.9):
    """ease-out-back 0..1 with overshoot"""
    x = min(max(x, 0), 1) - 1
    return 1 + x * x * ((s + 1) * x + s)


def eout(x):
    x = min(max(x, 0), 1)
    return 1 - (1 - x) ** 3


# ---------- face ----------
def draw_mouth(layer, cx, cy, w, level, open_amt, col):
    if level == 0:
        return
    S = 4
    hgt = w * (0.20, 0.34, 0.46)[level - 1] * (0.85 + 0.3 * open_amt)
    ww = w * (0.55, 0.68, 0.74)[level - 1]
    bw, bh = int(ww * S + 16), int(hgt * S + 16)
    m = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([8, 8, bw - 8, bh - 8], radius=int(min(bw, bh) * 0.48), fill=col["mouth"], outline=col["line"], width=int(2.2 * S))
    inner = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(inner).rounded_rectangle([8 + 3*S, 8 + 3*S, bw - 8 - 3*S, bh - 8 - 3*S], radius=int(min(bw, bh) * 0.42), fill=255)
    det = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    dd = ImageDraw.Draw(det)
    if level >= 2:
        dd.rectangle([0, 0, bw, int(bh * 0.30)], fill=col["teeth"])
    dd.ellipse([int(bw * 0.18), int(bh * 0.55), int(bw * 0.82), int(bh * 1.35)], fill=col["tongue"])
    m.paste(det, (0, 0), Image.composite(det, Image.new("RGBA", (bw, bh)), inner).getchannel("A"))
    m = m.resize((max(1, bw // S), max(1, bh // S)), Image.LANCZOS)
    layer.alpha_composite(m, (int(cx - m.width / 2), int(cy - m.height / 2 + hgt * 0.15)))


def draw_blink(layer, eyes, amt, col):
    if amt <= 0:
        return
    S = 4
    for (cx, cy, rx, ry) in eyes:
        bw, bh = int(rx * 2 * S + 16), int(ry * 2 * S + 16)
        m = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        d = ImageDraw.Draw(m)
        lid_h = int((bh - 16) * amt)
        mask = Image.new("L", (bw, bh), 0)
        ImageDraw.Draw(mask).ellipse([8, 8, bw - 8, bh - 8], fill=255)
        lid = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        ImageDraw.Draw(lid).rectangle([0, 0, bw, 8 + lid_h], fill=col["skin"])
        m.paste(lid, (0, 0), Image.composite(lid, Image.new("RGBA", (bw, bh)), mask).getchannel("A"))
        if amt > 0.85:
            d.arc([8, 8 - (bh - 16) // 2, bw - 8, bh - 8 - (bh - 16) // 4], 30, 150, fill=col["line"], width=int(2.5 * S))
        m = m.resize((bw // S, bh // S), Image.LANCZOS)
        layer.alpha_composite(m, (int(cx - m.width / 2), int(cy - m.height / 2)))


# ---------- motion background ----------
class MotionBG:
    def __init__(self, seed=3):
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * 0.55) / H) ** 2)
        k = np.clip(1 - r * 1.6, 0, 1)[..., None]
        top = np.array([8, 5, 24], np.float32); mid = np.array([34, 18, 78], np.float32)
        self.base = Image.fromarray((top + (mid - top) * k).astype(np.uint8)).convert("RGBA")
        rng = random.Random(seed)
        self.parts = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(2, 6), rng.uniform(20, 70), rng.uniform(0, 6.28)) for _ in range(46)]
        # big soft blobs, pre-blurred
        self.blob = Image.new("RGBA", (700, 700), (0, 0, 0, 0))
        ImageDraw.Draw(self.blob).ellipse([150, 150, 550, 550], fill=(139, 92, 246, 95))
        self.blob = self.blob.filter(ImageFilter.GaussianBlur(90))
        self.blob2 = Image.new("RGBA", (700, 700), (0, 0, 0, 0))
        ImageDraw.Draw(self.blob2).ellipse([150, 150, 550, 550], fill=(56, 189, 248, 55))
        self.blob2 = self.blob2.filter(ImageFilter.GaussianBlur(90))

    def frame(self, t, accent=1.0):
        f = self.base.copy()
        f.alpha_composite(self.blob, (int(W * 0.5 - 350 + 220 * math.sin(t * 0.35)), int(H * 0.38 - 350 + 160 * math.cos(t * 0.27))))
        f.alpha_composite(self.blob2, (int(W * 0.5 - 350 - 260 * math.sin(t * 0.22)), int(H * 0.7 - 350 + 120 * math.sin(t * 0.31))))
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        # drifting dot grid
        step = 54; off = (t * 14) % step
        for gy in range(-step, H + step, step):
            for gx in range(0, W + step, step):
                x, y = gx, gy + off
                fade = 1 - abs(y - H * 0.5) / (H * 0.6)
                if fade > 0:
                    d.ellipse([x - 1.6, y - 1.6, x + 1.6, y + 1.6], fill=(224, 196, 255, int(46 * fade)))
        # rotating rings
        cx, cy = W / 2, H * 0.52
        for i, (rr, sp, a0) in enumerate([(430, 0.25, 0), (560, -0.18, 1.2), (700, 0.12, 2.4)]):
            a = math.degrees(t * sp + a0)
            d.arc([cx - rr, cy - rr, cx + rr, cy + rr], a, a + 110, fill=(139, 92, 246, 70), width=3)
            d.arc([cx - rr, cy - rr, cx + rr, cy + rr], a + 180, a + 230, fill=(224, 196, 255, 45), width=2)
        # rising particles
        for (px, py, s, sp, ph) in self.parts:
            y = (py - t * sp) % (H + 40) - 20
            x = px + 14 * math.sin(t * 0.8 + ph)
            al = int(120 * (0.5 + 0.5 * math.sin(t * 2 + ph)))
            d.ellipse([x - s, y - s, x + s, y + s], fill=(200, 170, 255, al))
        f.alpha_composite(ov)
        return f


# ---------- FX ----------
class FX:
    def __init__(self, icon_dir, raw):
        self.icon_dir, self.raw, self.cache = icon_dir, raw, {}
        g = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse([60, 60, 240, 240], fill=(139, 92, 246, 150))
        self.glow = g.filter(ImageFilter.GaussianBlur(34))

    def icon(self, name, size):
        k = (name, int(size))
        if k not in self.cache:
            im = Image.open(f"{self.icon_dir}/{name}.png").convert("RGBA")
            self.cache[k] = im.resize((int(size), int(size)), Image.LANCZOS)
        return self.cache[k]

    def v(self, fi):
        return self.raw[min(max(fi, 0), len(self.raw) - 1)]

    def put_icon(self, fr, name, x, y, size, k, glow=True, rot=0):
        if k <= 0.02 or size < 4:
            return
        s = size * k
        if glow:
            gl = self.glow.resize((int(s * 1.9), int(s * 1.9)))
            fr.alpha_composite(gl, (int(x - gl.width / 2), int(y - gl.height / 2)))
        im = self.icon(name, max(8, int(round(s / 4) * 4)))
        if rot:
            im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
        fr.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))

    def draw(self, fr, fx, t, fi):
        ty = fx["type"]
        t0, t1 = fx.get("t0", fx.get("t", 0)), fx.get("t1", 999)
        if t < t0 or t > t1 + 0.4:
            return
        lt = t - t0
        out = 1 - ease((t - t1) / 0.3) if t > t1 else 1
        d = ImageDraw.Draw(fr)
        if ty == "icon":
            k = back(lt / 0.35) * out
            fl = fx.get("float", 1) * 12 * math.sin(t * 2.2 + fx["x"])
            x, y = fx["x"], fx["y"] + fl
            fr_ = fx.get("from")
            if fr_ == "left":
                x = fx["x"] - (1 - eout(lt / 0.4)) * 700; k = out
            elif fr_ == "right":
                x = fx["x"] + (1 - eout(lt / 0.4)) * 700; k = out
            elif fr_ == "top":
                y = fx["y"] - (1 - back(lt / 0.5)) * 900; k = out
            pulse = 1 + (0.06 * self.v(fi) if fx.get("react") else 0)
            self.put_icon(fr, fx["name"], x, y, fx["size"] * pulse, k, fx.get("glow", True), fx.get("wobble", 0) * math.sin(t * 3))
        elif ty == "wave":  # audio-reactive bars, scrolling
            n, w, h = fx.get("bars", 28), fx["w"], fx["h"]
            gap = w / n; k = eout(lt / 0.4) * out
            for i in range(n):
                vv = self.v(fi - (n // 2 - abs(i - n // 2)) * 1)
                env_ = math.sin(math.pi * (i + 0.5) / n)
                bh = max(6, h * (0.12 + 0.88 * vv) * env_ * k)
                x = fx["x"] - w / 2 + i * gap + gap / 2
                col = fx.get("color", (186, 140, 255))
                d.rounded_rectangle([x - gap * 0.28, fx["y"] - bh / 2, x + gap * 0.28, fx["y"] + bh / 2], radius=int(gap * 0.28), fill=tuple(col) + (int(230 * k),))
        elif ty == "radial":  # circular voice badge
            r, n = fx["r"], fx.get("bars", 48)
            k = back(lt / 0.5) * out
            cx, cy = fx["x"], fx["y"]
            gl = self.glow.resize((int(r * 3.2 * k + 2), int(r * 3.2 * k + 2)))
            fr.alpha_composite(gl, (int(cx - gl.width / 2), int(cy - gl.height / 2)))
            d.ellipse([cx - r * 0.78 * k, cy - r * 0.78 * k, cx + r * 0.78 * k, cy + r * 0.78 * k], fill=(36, 20, 80, int(235 * k)), outline=(224, 196, 255, int(255 * k)), width=5)
            rot = t * 0.6
            for i in range(n):
                a = rot + 2 * math.pi * i / n
                vv = self.v(fi - i % 7)
                l = r * (0.12 + 0.45 * vv) * k
                x0, y0 = cx + math.cos(a) * r * 0.86 * k, cy + math.sin(a) * r * 0.86 * k
                d.line([x0, y0, x0 + math.cos(a) * l, y0 + math.sin(a) * l], fill=(186, 140, 255, int(255 * k)), width=7)
            if fx.get("icon"):
                self.put_icon(fr, fx["icon"], cx, cy, r * 0.95, k, glow=False)
        elif ty == "orbit":
            names = fx["names"]; n = len(names)
            for i, nm in enumerate(names):
                ki = back((lt - i * fx.get("stagger", 0.18)) / 0.4) * out
                a = t * fx.get("speed", 0.55) + 2 * math.pi * i / n
                x = fx["x"] + math.cos(a) * fx["rx"]; y = fx["y"] + math.sin(a) * fx["ry"]
                depth = 0.82 + 0.18 * math.sin(a)
                self.put_icon(fr, nm, x, y, fx["size"] * depth, ki)
        elif ty == "burst":
            k = lt / 0.5
            if k > 1:
                return
            cx, cy, R = fx["x"], fx["y"], fx.get("r", 260)
            al = int(255 * (1 - k))
            d.ellipse([cx - R * eout(k), cy - R * eout(k), cx + R * eout(k), cy + R * eout(k)], outline=(224, 196, 255, al), width=max(1, int(10 * (1 - k))))
            for i in range(12):
                a = 2 * math.pi * i / 12 + 0.2
                r0, r1 = R * 0.55 * eout(k), R * (0.75 + 0.5 * eout(k))
                d.line([cx + math.cos(a) * r0, cy + math.sin(a) * r0, cx + math.cos(a) * r1, cy + math.sin(a) * r1], fill=(255, 220, 120, al), width=max(1, int(9 * (1 - k))))
        elif ty == "floaters":
            rng = random.Random(fx.get("seed", 1))
            for i in range(fx.get("n", 8)):
                st = t0 + rng.uniform(0, max(0.1, t1 - t0 - 1.2))
                lt_ = t - st
                if 0 <= lt_ <= 1.8:
                    x = fx["x"] + rng.uniform(-fx.get("spread", 260), fx.get("spread", 260)) + 25 * math.sin(lt_ * 4 + i)
                    y = fx["y"] - lt_ * fx.get("rise", 380)
                    k = back(lt_ / 0.3) * (1 - ease((lt_ - 1.3) / 0.5))
                    self.put_icon(fr, rng.choice(fx["names"]), x, y, fx["size"] * rng.uniform(0.75, 1.1), k, glow=False)
        elif ty == "converge":
            rng = random.Random(9)
            cx, cy = fx["x"], fx["y"]
            k = ease(lt / (t1 - t0))
            for i in range(70):
                a = rng.uniform(0, 6.28); R = rng.uniform(500, 1100)
                kk = eout(min(1, k * rng.uniform(0.9, 1.3)))
                rr = R * (1 - kk); aa = a + kk * 2.2
                x, y = cx + math.cos(aa) * rr, cy + math.sin(aa) * rr * 1.2
                s = rng.uniform(3, 8)
                d.ellipse([x - s, y - s, x + s, y + s], fill=(200, 170, 255, int(220 * (1 - kk * 0.6))))
        elif ty == "divider":
            k = eout(lt / 0.5) * out
            x = fx["x"]; y0, y1 = fx["y0"], fx["y0"] + (fx["y1"] - fx["y0"]) * k
            d.line([x, y0, x, y1], fill=(224, 196, 255, 220), width=5)
            gl = self.glow.resize((90, int(max(2, y1 - y0))))
            fr.alpha_composite(gl, (int(x - 45), int(y0)))


# ---------- render ----------
def render(cfg_path, out, t_from=None, t_to=None):
    cfg = json.load(open(cfg_path))
    E = json.load(open(cfg["env"]))
    levels, raw = E["level"], E["raw"]
    total = cfg["duration"]
    nfr = int(round(total * FPS))
    col = {k: tuple(v) for k, v in cfg["colors"].items()}
    poses = {n: (Image.open(p["img"]).convert("RGBA"), p) for n, p in cfg["poses"].items()}
    bg = MotionBG()
    fxr = FX(cfg["icons"], raw)
    rng = random.Random(7)
    blinks, t = [], 1.2
    while t < total:
        blinks.append(t); t += rng.uniform(2.4, 4.6)
    inserts = {}
    for sc in cfg["scenes"]:
        for ins in sc.get("inserts", []):
            inserts.setdefault(ins["img"], Image.open(ins["img"]).convert("RGBA"))
    punches = sorted(p for sc in cfg["scenes"] for p in sc.get("punch", []))

    f0 = 0 if t_from is None else int(float(t_from) * FPS)
    f1 = nfr if t_to is None else int(float(t_to) * FPS)
    proc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                             "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out],
                            stdin=subprocess.PIPE)

    def char_layer(sc, t, fi):
        cur = sc["poses"][0]
        for pp in sc["poses"]:
            if t >= pp[0]:
                cur = pp
        name = cur[1]; flip = len(cur) > 2 and cur[2] == "flip"
        img, p = poses[name]
        since = t - cur[0]
        pop = 1.0 + (0.035 * math.sin(min(since / 0.25, 1) * math.pi) if since < 0.25 and cur is not sc["poses"][0] else 0)
        talk = raw[min(fi, len(raw) - 1)]
        breathe = 1 + 0.006 * math.sin(t * 2 * math.pi / 3.4)
        sc_ = sc["char_h"] * pop / img.height
        cw, ch = int(img.width * sc_), int(img.height * sc_ * breathe)
        char = img.resize((cw, ch), Image.LANCZOS)
        if flip:
            char = char.transpose(Image.FLIP_LEFT_RIGHT)
        fx_ = lambda x: (img.width - x) * sc_ if flip else x * sc_
        lv = levels[min(fi, len(levels) - 1)]
        draw_mouth(char, fx_(p["mouth"][0]), p["mouth"][1] * sc_ * breathe, p["mouth_w"] * sc_, lv, talk, col)
        bt = min([t - x for x in blinks if t - x >= 0] or [9])
        amt = {0: 0.5, 1: 1, 2: 1, 3: 0.5}.get(int(bt * FPS), 0)
        draw_blink(char, [(fx_(e[0]), e[1] * sc_ * breathe, e[2] * sc_, e[3] * sc_) for e in p["eyes"]], amt, col)
        return char, talk

    def scene_frame(sc, t, fi):
        a = sc["start"]
        fr = bg.frame(t)
        for fx in sc.get("fx", []):
            if fx.get("layer", "back") == "back":
                fxr.draw(fr, fx, t, fi)
        for ins in sc.get("inserts", []):
            k = back((t - a - ins.get("delay", 0.2)) / 0.45)
            if k <= 0:
                continue
            im = inserts[ins["img"]]
            s = ins["w"] / im.width * k
            ii = im.resize((max(2, int(im.width * s)), max(2, int(im.height * s))), Image.LANCZOS)
            fr.alpha_composite(ii, (int(ins["x"] - ii.width / 2), int(ins["y"] + math.sin(t * 1.6) * 10 - ii.height / 2)))
        if t >= sc.get("char_in", a):
            char, talk = char_layer(sc, t, fi)
            ent, el = sc.get("enter"), t - sc.get("char_in", a)
            dx = dy = 0; ks = 1.0
            if ent == "pop":
                ks = back(el / 0.45)
            elif ent == "drop":
                dy = -(1 - back(el / 0.55, 1.4)) * 1400
            elif ent == "left":
                dx = -(1 - eout(el / 0.45)) * 900
            elif ent == "right":
                dx = (1 - eout(el / 0.45)) * 900
            if ks < 0.999:
                char = char.resize((max(2, int(char.width * ks)), max(2, int(char.height * ks))), Image.LANCZOS)
            sh = Image.new("RGBA", (int(char.width * 0.9), 60), (0, 0, 0, 0))
            ImageDraw.Draw(sh).ellipse([0, 0, sh.width, 60], fill=(5, 2, 15, 140))
            sh = sh.filter(ImageFilter.GaussianBlur(14))
            fr.alpha_composite(sh, (int(sc["char_x"] - sh.width / 2), int(sc["foot_y"] - 30)))
            bob = -6 * talk + 3 * math.sin(t * 1.3)
            fr.alpha_composite(char, (int(sc["char_x"] - char.width / 2 + 4 * math.sin(t * 0.9) + dx), int(sc["foot_y"] - char.height + bob + dy)))
        for fx in sc.get("fx", []):
            if fx.get("layer") == "front":
                fxr.draw(fr, fx, t, fi)
        return fr

    scenes = cfg["scenes"]
    XF = int(0.3 * FPS)
    for fi in range(f0, f1):
        t = fi / FPS
        idx = max(i for i, s in enumerate(scenes) if t >= s["start"] or i == 0)
        fr = scene_frame(scenes[idx], t, fi)
        if idx > 0 and t - scenes[idx]["start"] < XF / FPS:
            k = ease((t - scenes[idx]["start"]) / (XF / FPS))
            prev = scene_frame(scenes[idx - 1], t, fi)
            kind = scenes[idx].get("trans", "fade")
            if kind == "slide":
                base = Image.new("RGBA", (W, H))
                base.alpha_composite(prev, (int(-W * k), 0)); base.alpha_composite(fr, (int(W * (1 - k)), 0)); fr = base
            elif kind == "up":
                base = Image.new("RGBA", (W, H))
                base.alpha_composite(prev, (0, int(-H * k))); base.alpha_composite(fr, (0, int(H * (1 - k)))); fr = base
            elif kind == "flash":
                fr = Image.blend(prev, fr, k)
                fr = Image.blend(fr, Image.new("RGBA", (W, H), (255, 255, 255, 255)), 0.6 * math.sin(k * math.pi))
            else:
                fr = Image.blend(prev, fr, k)
        # camera punch-in + tiny shake
        lp = [p for p in punches if p <= t]
        if lp:
            dt = t - lp[-1]
            z = 1 + 0.07 * eout(dt / 0.12) * math.exp(-dt / 0.9) if dt < 0.12 else 1 + 0.07 * math.exp(-dt / 0.9)
            if z > 1.002:
                sx = 6 * math.sin(dt * 90) * math.exp(-dt / 0.08)
                cw, ch = W / z, H / z
                x0 = (W - cw) / 2 + sx; y0 = (H - ch) / 2
                fr = fr.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BILINEAR)
        proc.stdin.write(fr.convert("RGB").tobytes())
        if fi % 150 == 0:
            print(f"frame {fi}/{nfr}", flush=True)
    proc.stdin.close(); proc.wait()
    print("ok", out)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "key":
        key(sys.argv[2], sys.argv[3])
    elif cmd == "env":
        env(sys.argv[2], sys.argv[3])
    else:
        render(sys.argv[2], sys.argv[3], *(sys.argv[4:6] if len(sys.argv) > 5 else []))
