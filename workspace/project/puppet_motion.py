#!/usr/bin/env python3
"""2D puppet with full-body motion in one continuous world + moving camera.
Builds on puppet2d.py (mouth, blinks, FX). Adds: position keys -> automatic walk cycle,
lean into motion, anticipation, follow-through springs, squash & stretch on landing,
turns (x-squash + flip), camera keys (track / pan / dolly / zoom) with whip blur,
parallax world (floor grid, rings, dots), extra props (arc, card, clock, artboard,
people, videoframe, fan, gears, rec).
Run with project/.venv-puppet/bin/python:
  puppet_motion.py render <config.json> <out.mp4> [t0 t1]
  puppet_motion.py still  <config.json> <out.png> <t>
Config builder example: project/work/voice-ai-lesson/make_cfg.py"""
import json, math, subprocess, sys, random, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from puppet2d import draw_mouth, draw_blink, FX, ease, back, eout, W, H, FPS, FF


def eio(x):  # ease in-out cubic
    x = min(max(x, 0), 1)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def ein(x):
    x = min(max(x, 0), 1)
    return x * x * x


EASE = {"io": eio, "in": ein, "out": eout, "back": back, "lin": lambda x: min(max(x, 0), 1), "smooth": ease}


def interp(keys, t, n):
    """keys: [[t, v1..vn, (ease)]] -> tuple of n values"""
    if t <= keys[0][0]:
        return keys[0][1:1 + n]
    for a, b in zip(keys, keys[1:]):
        if a[0] <= t < b[0]:
            e = EASE[b[1 + n] if len(b) > 1 + n else "io"]((t - a[0]) / (b[0] - a[0]))
            return [a[1 + i] + (b[1 + i] - a[1 + i]) * e for i in range(n)]
    return keys[-1][1:1 + n]


def spring(dt, amp, freq=16, decay=0.22):
    if dt < 0 or dt > 1.5:
        return 0
    return amp * math.exp(-dt / decay) * math.cos(dt * freq)


# ---------- world background ----------
class World:
    def __init__(self, floor_y, seed=3):
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * 0.5) / H) ** 2)
        k = np.clip(1 - r * 1.5, 0, 1)[..., None]
        top = np.array([7, 4, 20], np.float32); mid = np.array([36, 19, 82], np.float32)
        self.base = Image.fromarray((top + (mid - top) * k).astype(np.uint8)).convert("RGBA")
        self.floor_y = floor_y
        rng = random.Random(seed)
        self.parts = [(rng.uniform(-2000, 6000), rng.uniform(0, H), rng.uniform(2, 6), rng.uniform(20, 70), rng.uniform(0, 6.28), rng.uniform(0.3, 0.9)) for _ in range(90)]

        def blob(c):
            b = Image.new("RGBA", (700, 700), (0, 0, 0, 0))
            ImageDraw.Draw(b).ellipse([150, 150, 550, 550], fill=c)
            return b.filter(ImageFilter.GaussianBlur(90))
        self.blob, self.blob2 = blob((139, 92, 246, 95)), blob((56, 189, 248, 50))
        g = Image.new("RGBA", (W, 260), (0, 0, 0, 0))
        dg = ImageDraw.Draw(g)
        for i in range(260):
            dg.line([0, i, W, i], fill=(139, 92, 246, int(70 * (1 - i / 260) ** 2)))
        self.floorglow = g

    def frame(self, t, cam):
        cx, cy, z = cam
        f = self.base.copy()
        px = -cx * 0.15
        f.alpha_composite(self.blob, (int(W * 0.5 - 350 + 220 * math.sin(t * 0.35) + px) % (W + 700) - 350, int(H * 0.36 - 350 + 160 * math.cos(t * 0.27))))
        f.alpha_composite(self.blob2, (int(W * 0.5 - 350 - 260 * math.sin(t * 0.22) + px * 1.3) % (W + 700) - 350, int(H * 0.7 - 350 + 120 * math.sin(t * 0.31))))
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        # parallax dot grid (depth 0.45)
        zz = 1 + (z - 1) * 0.45
        step = 58 * zz
        ox = (-cx * 0.45 * zz) % step; oy = (-cy * 0.45 * zz + t * 12) % step
        fy = (self.floor_y - cy) * z + H / 2
        y = oy - step
        while y < min(H, fy):
            fade = 1 - abs(y - H * 0.45) / (H * 0.6)
            if fade > 0:
                x = ox - step
                while x < W + step:
                    d.ellipse([x - 1.6, y - 1.6, x + 1.6, y + 1.6], fill=(224, 196, 255, int(44 * fade)))
                    x += step
            y += step
        # parallax rings anchored in the world (depth 0.6)
        for i, (wx, rr, sp, a0) in enumerate([(540, 430, 0.25, 0), (540, 600, -0.18, 1.2), (2300, 500, 0.2, 2.0), (-1100, 520, -0.2, 0.6), (3900, 520, 0.15, 1.0)]):
            sx = (wx - cx) * 0.6 * zz + W / 2; sy = (900 - cy) * 0.6 * zz + H / 2
            R = rr * zz
            if sx + R < -50 or sx - R > W + 50:
                continue
            a = math.degrees(t * sp + a0)
            d.arc([sx - R, sy - R, sx + R, sy + R], a, a + 110, fill=(139, 92, 246, 70), width=3)
            d.arc([sx - R, sy - R, sx + R, sy + R], a + 180, a + 230, fill=(224, 196, 255, 45), width=2)
        # particles (parallax by own depth)
        for (wx, py, s, sp, ph, dep) in self.parts:
            x = (wx - cx * dep) % 4000 - 1500 + W / 2 + 14 * math.sin(t * 0.8 + ph)
            if -10 < x < W + 10:
                yv = (py - t * sp) % (H + 40) - 20
                al = int(110 * (0.5 + 0.5 * math.sin(t * 2 + ph)))
                d.ellipse([x - s * dep, yv - s * dep, x + s * dep, yv + s * dep], fill=(200, 170, 255, al))
        # floor: fill, glowing horizon line, perspective grid that scrolls with the camera
        if fy < H:
            d.rectangle([0, fy, W, H], fill=(14, 8, 34, 235))
            vx = W / 2
            for gx in range(-6000, 9000, 240):
                x0 = (gx - cx) * z + W / 2
                x1 = vx + (x0 - vx) * 2.6
                if -3000 < x1 < W + 3000:
                    d.line([x0, fy, x1, H + (H - fy) * 0.0], fill=(150, 110, 255, 95), width=2)
            yy = fy; dy = 14 * z
            while yy < H:
                d.line([0, yy, W, yy], fill=(150, 110, 255, 75), width=2)
                yy += dy; dy *= 1.45
            d.line([0, fy, W, fy], fill=(214, 190, 255, 200), width=3)
        f.alpha_composite(ov)
        if fy < H + 50:
            f.alpha_composite(self.floorglow, (0, int(fy - 1)))
        return f


# ---------- extra FX ----------
class FX2(FX):
    def __init__(self, icon_dir, raw):
        super().__init__(icon_dir, raw)
        self.imgcache = {}

    def img(self, p):
        if p not in self.imgcache:
            self.imgcache[p] = Image.open(p).convert("RGBA")
        return self.imgcache[p]

    def person(self, d, x, y, s, col, al):
        d.ellipse([x - 0.28 * s, y - 1.0 * s, x + 0.28 * s, y - 0.44 * s], fill=col + (al,))
        d.rounded_rectangle([x - 0.45 * s, y - 0.38 * s, x + 0.45 * s, y + 0.5 * s], radius=int(0.3 * s), fill=col + (al,))

    def draw(self, fr, fx, t, fi):
        ty = fx["type"]
        t0, t1 = fx.get("t0", fx.get("t", 0)), fx.get("t1", 999)
        if t < t0 - 0.01 or t > t1 + 0.45:
            return
        lt = t - t0
        out = 1 - ease((t - t1) / 0.35) if t > t1 else 1
        d = ImageDraw.Draw(fr)
        if ty == "arc":  # icon flies along a parabola, leaves a trail
            k = eio(lt / max(0.05, t1 - t0))
            def pos(kk):
                x = fx["x0"] + (fx["x1"] - fx["x0"]) * kk
                y = fx["y0"] + (fx["y1"] - fx["y0"]) * kk - fx.get("hgt", 300) * 4 * kk * (1 - kk)
                return x, y
            if t <= t1:
                for j in range(10):
                    kk = max(0, k - j * 0.03)
                    x, y = pos(kk); s = 9 * (1 - j / 10)
                    d.ellipse([x - s, y - s, x + s, y + s], fill=(224, 196, 255, int(200 * (1 - j / 10))))
                x, y = pos(k)
                self.put_icon(fr, fx["name"], x, y, fx["size"], 1, True, (1 - k) * 40)
            elif fx.get("stay"):
                self.put_icon(fr, fx["name"], fx["x1"], fx["y1"] + 8 * math.sin(t * 2), fx["size"], 1)
        elif ty == "card":  # image card flips in (3D flip feel)
            k = back((lt) / 0.6) if lt < 0.6 else 1
            im = self.img(fx["img"])
            w = fx["w"]; h = w * im.height / im.width
            fl = min(1, max(0.02, ease(lt / 0.5))) * out
            cw = max(4, int(w * fl * (0.9 + 0.1 * k))); ch = max(4, int(h * (0.9 + 0.1 * k) * out))
            card = im.resize((cw, ch), Image.LANCZOS)
            m = Image.new("L", (cw, ch), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, cw - 1, ch - 1], radius=int(28 * cw / w + 1), fill=255)
            card.putalpha(ImageChops.multiply(card.getchannel("A"), m))
            x, y = fx["x"], fx["y"] + 10 * math.sin(t * 1.6)
            gl = self.glow.resize((int(cw * 1.5) + 2, int(ch * 1.3) + 2))
            fr.alpha_composite(gl, (int(x - gl.width / 2), int(y - gl.height / 2)))
            fr.alpha_composite(card, (int(x - cw / 2), int(y - ch / 2)))
            d.rounded_rectangle([x - cw / 2, y - ch / 2, x + cw / 2, y + ch / 2], radius=int(28 * cw / w + 1), outline=(224, 196, 255, int(230 * out)), width=4)
        elif ty == "clock":
            r = fx["r"] * back(lt / 0.4) * out
            if r < 4:
                return
            x, y = fx["x"], fx["y"]
            gl = self.glow.resize((int(r * 3), int(r * 3)))
            fr.alpha_composite(gl, (int(x - r * 1.5), int(y - r * 1.5)))
            d.ellipse([x - r, y - r, x + r, y + r], fill=(245, 240, 255, 240), outline=(139, 92, 246, 255), width=max(2, int(r * 0.08)))
            for i in range(12):
                a = i * math.pi / 6
                d.line([x + math.cos(a) * r * 0.78, y + math.sin(a) * r * 0.78, x + math.cos(a) * r * 0.9, y + math.sin(a) * r * 0.9], fill=(60, 40, 110, 255), width=max(2, int(r * 0.04)))
            sp = fx.get("speed", 6)
            for L, wd, a in [(0.5, 0.07, lt * sp / 12), (0.75, 0.04, lt * sp)]:
                a = a * 2 * math.pi - math.pi / 2
                d.line([x, y, x + math.cos(a) * r * L, y + math.sin(a) * r * L], fill=(40, 20, 80, 255), width=max(2, int(r * wd)))
            d.ellipse([x - r * 0.07, y - r * 0.07, x + r * 0.07, y + r * 0.07], fill=(230, 60, 90, 255))
        elif ty == "artboard":  # design frame drawn around the character
            x, y, w, h = fx["x"], fx["y"], fx["w"], fx["h"]
            k = eio(lt / 0.7) * out
            col = (120, 220, 255, int(235 * out))
            per = 2 * (w + h); L = per * k
            pts = [(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - w / 2, y - h / 2)]
            for a, b in zip(pts, pts[1:]):
                seg = math.dist(a, b)
                if L <= 0:
                    break
                f_ = min(1, L / seg)
                d.line([a, (a[0] + (b[0] - a[0]) * f_, a[1] + (b[1] - a[1]) * f_)], fill=col, width=4)
                L -= seg
            hs = 14 * back((lt - 0.6) / 0.3)
            if hs > 0:
                for (px, py) in pts[:4] + [(x, y - h / 2), (x, y + h / 2), (x - w / 2, y), (x + w / 2, y)]:
                    d.rectangle([px - hs, py - hs, px + hs, py + hs], fill=(255, 255, 255, int(255 * out)), outline=col, width=3)
        elif ty == "people":  # crowd that pops in; jumps when hit
            n = fx.get("n", 5); s = fx["size"]
            for i in range(n):
                ki = back((lt - i * 0.08) / 0.4) * out
                if ki <= 0.02:
                    continue
                x = fx["x"] + (i - (n - 1) / 2) * s * 1.25
                hit = fx.get("hit")
                jump = 0
                if hit and t > hit + i * 0.05:
                    dt = t - hit - i * 0.05
                    jump = abs(math.sin(dt * 7)) * 45 * math.exp(-dt / 0.6) * s / 100
                yv = fx["y"] - jump + (1 - ki) * 60
                col = [(200, 170, 255), (160, 220, 255), (255, 190, 220), (190, 240, 200), (255, 220, 160)][i % 5]
                self.person(d, x, yv, s * min(1.1, ki), col, int(235 * min(1, ki)))
        elif ty == "videoframe":  # 9:16 video window drops from above
            w, h = fx["w"], fx["h"]
            k = back(lt / 0.6, 1.3)
            x = fx["x"]; y = fx["y"] - (1 - k) * 1400 + 8 * math.sin(t * 1.7)
            al = int(240 * out)
            gl = self.glow.resize((int(w * 1.6), int(h * 1.3)))
            fr.alpha_composite(gl, (int(x - gl.width / 2), int(y - gl.height / 2)))
            d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], radius=30, fill=(30, 16, 70, al), outline=(224, 196, 255, al), width=5)
            # moving "content" bars inside
            for i in range(4):
                bw = w * (0.35 + 0.4 * (0.5 + 0.5 * math.sin(t * 2 + i)))
                yy = y + h * 0.12 + i * h * 0.08
                d.rounded_rectangle([x - w * 0.38, yy, x - w * 0.38 + bw, yy + h * 0.035], radius=8, fill=(139, 92, 246, int(200 * out)))
            r = w * 0.16
            d.ellipse([x - r, y - h * 0.18 - r, x + r, y - h * 0.18 + r], fill=(255, 255, 255, al))
            d.polygon([(x - r * 0.35, y - h * 0.18 - r * 0.5), (x - r * 0.35, y - h * 0.18 + r * 0.5), (x + r * 0.55, y - h * 0.18)], fill=(110, 60, 220, al))
            pk = (lt * 0.25) % 1
            d.rounded_rectangle([x - w * 0.4, y + h * 0.42, x + w * 0.4, y + h * 0.44], radius=4, fill=(255, 255, 255, int(90 * out)))
            d.rounded_rectangle([x - w * 0.4, y + h * 0.42, x - w * 0.4 + w * 0.8 * pk, y + h * 0.44], radius=4, fill=(230, 60, 120, al))
        elif ty == "photo":  # photo card glyph (mountains + sun)
            k = back((lt) / 0.45) * out
            if k <= 0.02:
                return
            w = fx["w"] * k; h = w * 0.78
            x, y = fx["x"], fx["y"] + 10 * math.sin(t * 2 + fx["x"])
            card = Image.new("RGBA", (int(w) + 8, int(h) + 8), (0, 0, 0, 0))
            dc = ImageDraw.Draw(card)
            dc.rounded_rectangle([4, 4, w + 4, h + 4], radius=int(w * 0.08), fill=(250, 248, 255, 245), outline=(139, 92, 246, 255), width=max(2, int(w * 0.03)))
            dc.rectangle([w * 0.1 + 4, h * 0.1 + 4, w * 0.9 + 4, h * 0.9 + 4], fill=tuple(fx.get("sky", (150, 200, 255, 255))))
            dc.ellipse([w * 0.62, h * 0.18, w * 0.78, h * 0.34], fill=(255, 200, 70, 255))
            dc.polygon([(w * 0.1 + 4, h * 0.9 + 4), (w * 0.38, h * 0.38), (w * 0.62, h * 0.9 + 4)], fill=(110, 70, 200, 255))
            dc.polygon([(w * 0.4, h * 0.9 + 4), (w * 0.65, h * 0.52), (w * 0.9 + 4, h * 0.9 + 4)], fill=(80, 50, 160, 255))
            card = card.rotate(fx.get("rot", 0) + 4 * math.sin(t * 1.5 + fx["x"]), resample=Image.BICUBIC, expand=True)
            fr.alpha_composite(card, (int(x - card.width / 2), int(y - card.height / 2)))
        elif ty == "gears":
            k = back(lt / 0.5) * out
            s = fx["size"]
            for i, (dx, dy, sp) in enumerate([(-0.42, 0, 1), (0.36, -0.3, -1.3)]):
                im = self.icon("gear", max(8, int(s * (1 if i == 0 else 0.75) / 4) * 4))
                im = im.rotate(t * 90 * sp, resample=Image.BICUBIC)
                xx = fx["x"] + dx * s * k + (1 - k) * (-500 if i == 0 else 500)
                fr.alpha_composite(im, (int(xx - im.width / 2), int(fx["y"] + dy * s - im.height / 2)))
        elif ty == "rec":
            k = back(lt / 0.3) * out
            r = fx["r"] * k * (1 + 0.15 * math.sin(t * 8))
            d.ellipse([fx["x"] - r * 1.8, fx["y"] - r * 1.8, fx["x"] + r * 1.8, fx["y"] + r * 1.8], outline=(255, 70, 90, int(150 * out)), width=3)
            d.ellipse([fx["x"] - r, fx["y"] - r, fx["x"] + r, fx["y"] + r], fill=(255, 60, 80, int(255 * out)))
        elif ty == "spot":  # floor spotlight disc
            k = eout(lt / 0.5) * out
            rx, ry = fx["rx"] * k, fx["ry"] * k
            if ry < 3:
                return
            sp =Image.new("RGBA", (int(rx * 2) + 4, int(ry * 2) + 4), (0, 0, 0, 0))
            ImageDraw.Draw(sp).ellipse([2, 2, rx * 2, ry * 2], fill=(160, 120, 255, 90))
            sp = sp.filter(ImageFilter.GaussianBlur(max(1, ry * 0.3)))
            fr.alpha_composite(sp, (int(fx["x"] - rx), int(fx["y"] - ry)))
        else:
            super().draw(fr, fx, t, fi)


SCALE_KEYS = ("size", "r", "w", "h", "rx", "ry", "spread", "rise", "hgt")


def to_screen(fx, cam):
    cx, cy, z = cam
    f = dict(fx)
    T = lambda x, y: ((x - cx) * z + W / 2, (y - cy) * z + H / 2)
    if "x" in f and "y" in f:
        f["x"], f["y"] = T(f["x"], f["y"])
    if "x0" in f:
        f["x0"], f["y0"] = T(f["x0"], f["y0"]); f["x1"], f["y1"] = T(f["x1"], f["y1"])
    if "y0" in f and "x0" not in f:  # divider
        f["x"] = T(fx["x"], 0)[0]; f["y0"] = T(0, fx["y0"])[1]; f["y1"] = T(0, fx["y1"])[1]
    for k in SCALE_KEYS:
        if k in f:
            f[k] = f[k] * z
    return f


# ---------- character track ----------
class Track:
    def __init__(self, cfg, nfr):
        self.cfg = cfg
        self.walk = cfg.get("walk", {"frames": ["walk_a", "walk_b"], "stride": 150})
        xs = [interp(cfg["char_keys"], i / FPS, 1)[0] for i in range(nfr + 2)]
        self.x = xs
        self.v = [(xs[min(i + 1, nfr + 1)] - xs[max(i - 1, 0)]) * FPS / 2 for i in range(nfr + 1)]
        self.moving = [abs(v) > 40 for v in self.v]
        # walking distance -> phase
        self.dist, acc = [], 0
        for i in range(nfr + 1):
            acc += abs(xs[i + 1] - xs[i]); self.dist.append(acc)
        # events
        self.starts = [i / FPS for i in range(1, nfr + 1) if self.moving[i] and not self.moving[i - 1]]
        self.stops = [(i / FPS, self.v[i - 3] if i >= 3 else 0) for i in range(1, nfr + 1) if not self.moving[i] and self.moving[i - 1]]
        self.states = [self.state_raw(i) for i in range(nfr + 1)]
        self.changes = []  # (t, kind)
        for i in range(1, nfr + 1):
            a, b = self.states[i - 1], self.states[i]
            if a[1] != b[1]:
                self.changes.append((i / FPS, "turn"))
            elif a[0] != b[0] and not (a[0] in self.walk["frames"] and b[0] in self.walk["frames"]):
                self.changes.append((i / FPS, "pose"))

    def pose_at(self, t):
        cur = self.cfg["pose_keys"][0]
        for p in self.cfg["pose_keys"]:
            if t >= p[0]:
                cur = p
        return cur[1], (cur[2] if len(cur) > 2 else 1)

    def state_raw(self, i):
        t = i / FPS
        if self.moving[i]:
            fr_ = self.walk["frames"]
            ph = int(self.dist[i] / self.walk["stride"]) % len(fr_)
            return fr_[ph], (1 if self.v[i] > 0 else -1)
        return self.pose_at(t)

    def at(self, i):
        """-> pose, dir, sx, sy, rot(deg), dy"""
        t = i / FPS
        pose, dr = self.states[i]
        for (a, b, pz, dz) in self.cfg.get("overrides", []):
            if a <= t < b:
                pose, dr = pz, dz
        sx = sy = 1.0; rot = 0.0; dy = 0.0
        v = self.v[i]
        if self.moving[i]:
            stepl = self.walk["stride"] * max(1, len(self.walk["frames"]) / 2)
            ph = (self.dist[i] / stepl + 0.5 * (len(self.walk["frames"]) > 2)) % 1
            dy -= 18 * abs(math.sin(ph * math.pi))
            sy *= 1 + 0.012 * math.cos(ph * 2 * math.pi)
            rot += max(-6, min(6, v / 1400 * 6))
        for ts_ in self.starts:  # anticipation before moving: lean back + crouch
            dt = ts_ - t
            if 0 <= dt < 0.18:
                k = math.sin((1 - dt / 0.18) * math.pi)
                vv = self.v[min(int(ts_ * FPS) + 4, len(self.v) - 1)]
                rot -= 3.5 * k * (1 if vv > 0 else -1)
                sy *= 1 - 0.035 * k; sx *= 1 + 0.02 * k
        for (ts_, vv) in self.stops:  # follow-through on stop
            dt = t - ts_
            if 0 <= dt < 1.2:
                rot += spring(dt, max(-5, min(5, vv / 1400 * 5)), 14, 0.2)
        for (tc, kind) in self.changes:
            dt = t - tc
            if kind == "turn" and -0.14 <= dt < 0.14:
                sx *= 0.35 + 0.65 * abs(dt / 0.14) ** 0.7
                tp = self.cfg.get("turn_pose")
                if tp and abs(dt) < 0.07:  # profile frame in the middle of the turn
                    pose = tp; sx /= 0.35 + 0.65 * abs(dt / 0.14) ** 0.7
            elif kind == "pose" and -0.1 <= dt < 1.0:
                if dt < 0:  # anticipation squash
                    k = math.sin((dt + 0.1) / 0.1 * math.pi / 2)
                    sy *= 1 - 0.03 * k; sx *= 1 + 0.015 * k
                else:
                    sy *= 1 + spring(dt, 0.035, 18, 0.16)
                    rot += spring(dt, 1.6, 12, 0.22)
        for tl in self.cfg.get("lands", []):  # landing squash & stretch
            dt = t - tl
            if 0 <= dt < 0.8:
                s = spring(dt, 0.16, 22, 0.13)
                sy *= 1 - s; sx *= 1 + s * 0.8
        for (a, b) in self.cfg.get("falls", []):  # stretch while falling
            if a <= t < b:
                sy *= 1.08; sx *= 0.95
        dy += interp(self.cfg.get("y_keys", [[0, 0]]), t, 1)[0]
        return pose, dr, sx, sy, rot, dy


# ---------- render ----------
def build(cfg):
    E = json.load(open(cfg["env"]))
    total = cfg["duration"]; nfr = int(round(total * FPS))
    st = {"cfg": cfg, "levels": E["level"], "raw": E["raw"], "nfr": nfr,
          "col": {k: tuple(v) for k, v in cfg["colors"].items()},
          "poses": {n: (Image.open(p["img"]).convert("RGBA"), p) for n, p in cfg["poses"].items()},
          "world": World(cfg["floor_y"]), "fx": FX2(cfg["icons"], E["raw"]), "track": Track(cfg, nfr)}
    rng = random.Random(7); bl, t = [], 1.5
    while t < total:
        bl.append(t); t += rng.uniform(2.4, 4.6)
    st["blinks"] = bl
    st["shadow"] = Image.new("RGBA", (400, 60), (0, 0, 0, 0))
    ImageDraw.Draw(st["shadow"]).ellipse([0, 0, 400, 60], fill=(5, 2, 15, 150))
    st["shadow"] = st["shadow"].filter(ImageFilter.GaussianBlur(12))
    return st


def cam_at(cfg, t):
    cx, cy, z = interp(cfg["cam_keys"], t, 3)
    for s in cfg.get("shakes", []):
        dt = t - s[0]
        if 0 <= dt < 0.5:
            a = s[1] if len(s) > 1 else 18
            cx += a * math.sin(dt * 70) * math.exp(-dt / 0.1)
            cy += a * 0.7 * math.cos(dt * 55) * math.exp(-dt / 0.1)
    for p in cfg.get("punch", []):  # quick zoom pulse on stressed words
        dt = t - p
        if 0 <= dt < 1.5:
            z *= 1 + 0.06 * (eout(dt / 0.1) if dt < 0.1 else math.exp(-(dt - 0.1) / 0.6))
    return cx, cy, z


def char_image(st, i, t, cam):
    cfg = st["cfg"]; tr = st["track"]
    pose, dr, sx, sy, rot, dy = tr.at(i)
    img, p = st["poses"][pose]
    cx, cy, z = cam
    talk = st["raw"][min(i, len(st["raw"]) - 1)]
    breathe = 1 + 0.006 * math.sin(t * 2 * math.pi / 3.4)
    hmul = p.get("hmul", 1.0)
    sc = cfg["char_h"] * hmul * z / img.height
    cw, ch = max(2, int(img.width * sc)), max(2, int(img.height * sc * breathe))
    char = img.resize((cw, ch), Image.LANCZOS)
    flip = (dr == -1) != bool(p.get("faces_left"))
    if flip:
        char = char.transpose(Image.FLIP_LEFT_RIGHT)
    fxx = (lambda x: (img.width - x) * sc) if flip else (lambda x: x * sc)
    if p.get("eyes"):
        lv = st["levels"][min(i, len(st["levels"]) - 1)]
        draw_mouth(char, fxx(p["mouth"][0]), p["mouth"][1] * sc * breathe, p["mouth_w"] * sc, lv, talk, st["col"])
        bt = min([t - x for x in st["blinks"] if t - x >= 0] or [9])
        amt = {0: 0.5, 1: 1, 2: 1, 3: 0.5}.get(int(bt * FPS), 0)
        col = dict(st["col"]); col["skin"] = tuple(p.get("skin", col["skin"][:3])) + (255,)
        draw_blink(char, [(fxx(e[0]), e[1] * sc * breathe, e[2] * sc, e[3] * sc) for e in p["eyes"]], amt, col)
    sx *= 1 + 0.004 * talk
    if abs(sx - 1) > 0.003 or abs(sy - 1) > 0.003:
        char = char.resize((max(2, int(cw * sx)), max(2, int(ch * sy))), Image.BILINEAR)
    rot += 1.2 * math.sin(t * 0.9) - 1.0 * talk * math.sin(t * 5)
    # pivot at feet: pad so feet are at the centre, rotate, return (img, foot offset)
    if abs(rot) > 0.05:
        pad = Image.new("RGBA", (char.width, char.height * 2), (0, 0, 0, 0))
        pad.alpha_composite(char, (0, 0))
        pad = pad.rotate(-rot, resample=Image.BICUBIC, expand=True, center=(char.width / 2, char.height))
        return pad, pad.width / 2, pad.height / 2, dy * z
    return char, char.width / 2, char.height, dy * z


def frame(st, i):
    cfg = st["cfg"]; t = i / FPS
    cam = cam_at(cfg, t)
    cx, cy, z = cam
    fr = st["world"].frame(t, cam)
    fxs = cfg["fx"]
    for f in fxs:
        if f.get("layer", "back") == "back":
            st["fx"].draw(fr, to_screen(f, cam), t, i)
    if t >= cfg.get("char_in", 0):
        x = st["track"].x[i]
        sxp, syp = (x - cx) * z + W / 2, (cfg["floor_y"] - cy) * z + H / 2
        img, ax, ay, dy = char_image(st, i, t, cam)
        # contact shadow shrinks when in the air
        air = min(1, abs(dy) / 600)
        shw = int(img.width * 0.75 * (1 - 0.6 * air)) + 2
        sh = st["shadow"].resize((shw, max(2, int(40 * z * (1 - 0.5 * air)))))
        fr.alpha_composite(sh, (int(sxp - shw / 2), int(syp - sh.height / 2)))
        bob = -5 * st["raw"][min(i, len(st["raw"]) - 1)] * z
        fr.alpha_composite(img, (int(sxp - ax), int(syp - ay + dy + bob)))
    for f in fxs:
        if f.get("layer") == "front":
            st["fx"].draw(fr, to_screen(f, cam), t, i)
    # whip blur when the camera moves fast
    if i > 0:
        pc = cam_at(cfg, (i - 1) / FPS)
        spd = (cx - pc[0]) * z
        if abs(spd) > 28:
            n = 4; sh = int(spd * 0.6 / n)
            acc = fr.copy()
            for k in range(1, n + 1):
                acc = Image.blend(acc, ImageChops.offset(fr, sh * k, 0), 1 / (k + 1))
            fr = acc
    # flash
    for fl in cfg.get("flashes", []):
        dt = t - fl
        if 0 <= dt < 0.25:
            fr = Image.blend(fr, Image.new("RGBA", (W, H), (255, 255, 255, 255)), 0.55 * (1 - dt / 0.25))
    return fr


def render(cfg_path, out, t_from=None, t_to=None):
    cfg = json.load(open(cfg_path)); st = build(cfg)
    f0 = 0 if t_from is None else int(round(float(t_from) * FPS))
    f1 = st["nfr"] if t_to is None else min(st["nfr"], int(round(float(t_to) * FPS)))
    proc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                             "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(f0, f1):
        proc.stdin.write(frame(st, i).convert("RGB").tobytes())
        if i % 150 == 0:
            print(f"frame {i}/{f1}", flush=True)
    proc.stdin.close(); proc.wait(); print("ok", out)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "still":
        cfg = json.load(open(sys.argv[2])); st = build(cfg)
        for k, tt in enumerate(sys.argv[4:]):
            o = sys.argv[3].replace(".png", f"_{k:02d}.png")
            frame(st, int(round(float(tt) * FPS))).convert("RGB").save(o)
        print("ok")
    else:
        render(sys.argv[2], sys.argv[3], *(sys.argv[4:6] if len(sys.argv) > 5 else []))
