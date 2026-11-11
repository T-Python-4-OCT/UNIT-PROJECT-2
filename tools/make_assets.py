#!/usr/bin/env python3
"""
Generates the original artwork used by «حكاية وطن»:
  * SVG illustrations (dawn / day / sunset / night) for every city and era
  * short looping MP4 clips (a full day-night timelapse with moving clouds, birds, sea, palms…)

Nothing here is downloaded: every picture is drawn by code, so there are no copyright or
broken-link problems. Replace any file (or point the JSON to a real photo/video URL) whenever you like.

Requirements (only to REGENERATE the media, not to run the Django site):
    rsvg-convert  and  ffmpeg

Usage:
    python tools/make_assets.py stills          # SVG + JPG posters
    python tools/make_assets.py videos          # all MP4 clips
    python tools/make_assets.py videos riyadh   # only some clips
    python tools/make_assets.py all
"""
import math
import os
import random
import shutil
import subprocess
import sys
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "watan" / "static" / "watan" / "img"
VID = ROOT / "watan" / "static" / "watan" / "video"
W, H = 1600, 900
BASE = 745  # ground line of the skylines

# ----------------------------------------------------------------------------- helpers


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb2hex(c):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(v)))) for v in c)


def mix(a, b, k):
    ra, rb = hex2rgb(a), hex2rgb(b)
    k = max(0.0, min(1.0, k))
    return rgb2hex([ra[i] * (1 - k) + rb[i] * k for i in range(3)])


def lerp(a, b, k):
    return a + (b - a) * k


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def f(v):
    return f"{v:.1f}"


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{fill}" {extra}/>'


def poly(pts, fill, extra=""):
    p = " ".join(f"{f(x)},{f(y)}" for x, y in pts)
    return f'<polygon points="{p}" fill="{fill}" {extra}/>'


def circ(cx, cy, r, fill, extra=""):
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}" {extra}/>'


def path(d, fill="none", extra=""):
    return f'<path d="{d}" fill="{fill}" {extra}/>'


def g(content, tx=0, ty=0, s=1.0, extra=""):
    return f'<g transform="translate({f(tx)},{f(ty)}) scale({s})" {extra}>{content}</g>'


# ----------------------------------------------------------------------------- sky / time of day
# (phase, top colour, bottom colour, stars, light, glow)
KEYS = [
    (0.00, "#27355f", "#f3a25b", 0.30, 0.72, 1.0),
    (0.10, "#4586c6", "#f7d19a", 0.00, 0.92, 0.6),
    (0.30, "#2a7bd0", "#bde4f7", 0.00, 1.00, 0.0),
    (0.45, "#3c78b8", "#f6c27b", 0.00, 0.92, 0.5),
    (0.52, "#4a3b7c", "#f07f4a", 0.10, 0.75, 1.0),
    (0.63, "#1b2147", "#8a4d7d", 0.60, 0.48, 0.5),
    (0.80, "#070d20", "#1b2a4d", 1.00, 0.26, 0.0),
    (1.00, "#27355f", "#f3a25b", 0.30, 0.72, 1.0),
]


def sky_state(p):
    p %= 1.0
    for (a, *va), (b, *vb) in zip(KEYS, KEYS[1:]):
        if a <= p <= b:
            k = (p - a) / (b - a) if b > a else 0
            k = k * k * (3 - 2 * k)
            return dict(top=mix(va[0], vb[0], k), bot=mix(va[1], vb[1], k),
                        star=lerp(va[2], vb[2], k), light=lerp(va[3], vb[3], k),
                        glow=lerp(va[4], vb[4], k))
    return dict(top=KEYS[0][1], bot=KEYS[0][2], star=.3, light=.72, glow=1.0)


class Ctx:
    def __init__(self, p, t):
        self.p = p % 1.0
        self.t = t
        s = sky_state(self.p)
        self.top, self.bot = s["top"], s["bot"]
        self.star, self.light, self.glow = s["star"], s["light"], s["glow"]
        self.night = clamp((self.star - .25) / .6)
        self._n = 0

    def uid(self, prefix="i"):
        self._n += 1
        return f"{prefix}{self._n}"

    def sh(self, col):
        """Tint a colour for the current time of day."""
        col = mix(col, self.bot, 0.16 * self.glow)
        return mix(col, "#080c1e", (1 - self.light) * 0.85)


# ----------------------------------------------------------------------------- sky elements


def stars(c):
    if c.star < .02:
        return ""
    r = random.Random(5)
    out = []
    for _ in range(130):
        x, y = r.uniform(0, W), r.uniform(0, 520)
        rad = r.choice([1, 1.3, 1.7, 2.2])
        k = r.choice([1, 2, 3])
        ph = r.random()
        tw = .55 + .45 * math.sin(2 * math.pi * (k * c.t + ph))
        out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{rad}" opacity="{c.star * tw:.2f}"/>')
    return '<g fill="#fff">' + "".join(out) + "</g>"


def celestial(c):
    out = []
    p = c.p
    if p < 0.58:
        s = p / 0.58
        x = 130 + 1340 * s
        y = 715 - 590 * math.sin(math.pi * s) ** 1.1
        op = clamp(min(s * 7, (1 - s) * 7))
        warm = clamp(1 - math.sin(math.pi * s) * 1.6)
        col = mix("#fff3c4", "#ff9a4d", warm)
        gid = c.uid("sg")
        out.append(f'<radialGradient id="{gid}"><stop offset="0" stop-color="{col}" stop-opacity=".85"/>'
                   f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>')
        out.append(circ(x, y, 230, f"url(#{gid})", f'opacity="{op * .8:.2f}"'))
        out.append(circ(x, y, 46, col, f'opacity="{op:.2f}"'))
    if p > 0.5:
        s = (p - 0.5) / 0.5
        x = 140 + 1320 * s
        y = 700 - 540 * math.sin(math.pi * s)
        op = clamp(min(s * 8, (1 - s) * 8))
        gid = c.uid("mg")
        out.append(f'<radialGradient id="{gid}"><stop offset="0" stop-color="#cfe0ff" stop-opacity=".6"/>'
                   f'<stop offset="1" stop-color="#cfe0ff" stop-opacity="0"/></radialGradient>')
        out.append(circ(x, y, 170, f"url(#{gid})", f'opacity="{op:.2f}"'))
        out.append(f'<g opacity="{op:.2f}">' + circ(x, y, 36, "#f5f1de")
                   + circ(x - 10, y - 8, 7, "#dcd8c4") + circ(x + 11, y + 9, 5, "#dcd8c4")
                   + circ(x + 6, y - 14, 3.5, "#dcd8c4") + "</g>")
    return "".join(out)


def cloud(x, y, s, fill, op):
    parts = [(0, 0, 60, 22), (-38, 8, 40, 16), (40, 10, 46, 17), (10, -12, 38, 18)]
    el = "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/>' for cx, cy, rx, ry in parts)
    return f'<g transform="translate({f(x)},{f(y)}) scale({s})" fill="{fill}" opacity="{min(op, 1):.2f}">{el}</g>'


def clouds(c, dens=1.0):
    col = mix(mix("#ffffff", c.bot, .35), "#0b1226", (1 - c.light) * .85)
    layers = [(800, [(100, 170, 1.4, .85), (480, 250, 1.0, .7)]),
              (1000, [(250, 110, .9, .6), (700, 330, 1.6, .5)])]
    out = []
    for period, items in layers:
        for i in range(-1, 3):
            for x, y, s, o in items:
                out.append(cloud(x + period * i + period * c.t, y, s, col, o * dens))
    return "".join(out)


def birds(c):
    if c.light < .7:
        return ""
    r = random.Random(9)
    out = []
    for i in range(6):
        x0 = r.uniform(0, 1800)
        y = r.uniform(120, 330) + 10 * math.sin(2 * math.pi * (c.t + i * .17))
        sc = r.uniform(.8, 1.4)
        x = (x0 + 1800 * c.t) % 1800 - 100
        fl = math.sin(2 * math.pi * (6 * c.t + i * .13))
        out.append(f'<path d="M-14,0 Q-7,{-9 * fl:.1f} 0,0 Q7,{-9 * fl:.1f} 14,0" '
                   f'transform="translate({f(x)},{f(y)}) scale({sc:.2f})"/>')
    return (f'<g fill="none" stroke="{c.sh("#2b2f3a")}" stroke-width="2.2" stroke-linecap="round" opacity=".7">'
            + "".join(out) + "</g>")


# ----------------------------------------------------------------------------- landscape pieces


def ridge(seed, base, amp, n, fill, jag=False, opacity=1.0, x0=-100, x1=1700, bottom=H + 10):
    r = random.Random(seed)
    xs = [x0 + (x1 - x0) * i / n for i in range(n + 1)]
    ys = [base - r.random() * amp for _ in xs]
    if jag:
        pts = " L".join(f"{x:.0f},{y:.0f}" for x, y in zip(xs, ys))
        d = f"M{x0},{bottom} L{pts} L{x1},{bottom} Z"
    else:
        d = f"M{x0},{bottom} L{xs[0]:.0f},{ys[0]:.0f}"
        for i in range(1, len(xs)):
            mx, my = (xs[i - 1] + xs[i]) / 2, (ys[i - 1] + ys[i]) / 2
            d += f" Q{xs[i - 1]:.0f},{ys[i - 1]:.0f} {mx:.0f},{my:.0f}"
        d += f" L{x1},{ys[-1]:.0f} L{x1},{bottom} Z"
    return f'<path d="{d}" fill="{fill}" opacity="{opacity}"/>'


def ground(c, top, bot, y=BASE):
    gid = c.uid("gr")
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
            f'<stop offset="1" stop-color="{bot}"/></linearGradient>' + rect(0, y, W, H - y + 2, f"url(#{gid})"))


def windows(c, x, y, w, h, seed, step_x=12, step_y=16, prob=.55):
    if c.night < .05:
        return ""
    r = random.Random(seed)
    cols = max(1, int((w - 6) // step_x))
    rows = max(1, int((h - 8) // step_y))
    out = []
    for i in range(cols):
        for j in range(rows):
            if r.random() < prob:
                out.append(f'<rect x="{f(x + 4 + i * step_x)}" y="{f(y + 6 + j * step_y)}" width="5" height="7"/>')
    return f'<g fill="#ffd27a" opacity="{c.night * .9:.2f}">' + "".join(out) + "</g>"


def towers(c, seed, x0, x1, base, hmin, hmax, wmin, wmax, fill, win=True, gap=(0, 8)):
    r = random.Random(seed)
    x = x0
    out = []
    while x < x1:
        w = r.randint(wmin, wmax)
        h = r.randint(hmin, hmax)
        out.append(rect(x, base - h, w, h, fill))
        k = r.random()
        if k < .2:
            out.append(rect(x + w * .4, base - h - 16, w * .2, 16, fill))
        elif k < .3:
            out.append(poly([(x, base - h), (x + w / 2, base - h - 18), (x + w, base - h)], fill))
        if win:
            out.append(windows(c, x, base - h, w, h, seed * 1000 + int(x)))
        x += w + r.randint(*gap)
    return "".join(out)


def palm(c, x, y, s=1.0, ph=0.0):
    sway = 3.0 * math.sin(2 * math.pi * (c.t + ph))
    trunk_col, leaf, leaf2 = c.sh("#5a4028"), c.sh("#2f7a43"), c.sh("#235f35")
    out = [path("M0,0 C8,-70 -6,-130 6,-190", extra=f'stroke="{trunk_col}" stroke-width="11" '
                                                   f'stroke-linecap="round"')]
    tx, ty = 6, -190
    for i, a in enumerate(range(-170, -5, 20)):
        r = math.radians(a)
        L = 95 + (i % 2) * 18
        ex = tx + math.cos(r) * L
        ey = ty + math.sin(r) * L * .55 + (28 if abs(math.cos(r)) > .5 else 0)
        cx_ = tx + math.cos(r) * L * .55
        cy_ = ty + math.sin(r) * L * .8 - 22
        out.append(path(f"M{tx},{ty} Q{f(cx_)},{f(cy_)} {f(ex)},{f(ey)}",
                        extra=f'stroke="{leaf if i % 2 == 0 else leaf2}" stroke-width="7" '
                              f'stroke-linecap="round"'))
    out.append(circ(tx - 3, ty + 6, 5, c.sh("#6b4a2a")) + circ(tx + 5, ty + 8, 5, c.sh("#6b4a2a")))
    return (f'<g transform="translate({f(x)},{f(y)}) scale({s})"><g transform="rotate({sway:.2f} 0 0)">'
            + "".join(out) + "</g></g>")


def minaret(c, x, h, col="#e9e0c8", cap="#1f8a4c"):
    col, cap, gold = c.sh(col), c.sh(cap), c.sh("#caa24a")
    return (rect(x - 8, -h, 16, h, col) + rect(x - 13, -h + 36, 26, 8, gold) + rect(x - 6, -h - 46, 12, 48, col)
            + poly([(x - 9, -h - 46), (x + 9, -h - 46), (x, -h - 84)], cap) + circ(x, -h - 88, 3, gold))


# ----------------------------------------------------------------------------- landmarks (local coords, base at 0,0)


def kingdom_centre(c):
    body, lite = c.sh("#3a4d63"), c.sh("#587291")
    o = [path("M-60,0 V-520 H60 V0 Z M-28,-330 V-440 Q0,-500 28,-440 V-330 Z", body, 'fill-rule="evenodd"'),
         rect(0, -520, 60, 520, lite, 'opacity=".25"')]
    o.append(path("M-28,-330 V-440 Q0,-500 28,-440 V-330", "none",
                  f'stroke="#ffd27a" stroke-width="3" opacity="{c.night * .85:.2f}"'))
    o.append(windows(c, -60, -330, 32, 330, 301, 10, 14, .5) + windows(c, 28, -330, 32, 330, 302, 10, 14, .5))
    o.append(rect(-60, -330, 120, 330, body))
    o.append(windows(c, -60, -330, 120, 330, 303, 12, 15, .5))
    o.append(rect(-62, -335, 124, 8, c.sh("#2c3b4d")))
    return "".join(o)


def faisaliah(c):
    body, gold = c.sh("#4a5f78"), c.sh("#caa24a")
    o = [poly([(-34, 0), (-18, -380), (18, -380), (34, 0)], body),
         poly([(-34, 0), (-18, -380), (-2, -380), (-2, 0)], c.sh("#62809f"), 'opacity=".35"'),
         circ(0, -405, 30, gold), circ(-8, -412, 9, mix(gold, "#ffffff", .35)),
         rect(-1.5, -480, 3, 50, gold)]
    o.append(windows(c, -30, -370, 60, 370, 311, 10, 16, .45))
    return "".join(o)


def masmak(c):
    clay, dark, lite = c.sh("#b58b5a"), c.sh("#3d2a18"), c.sh("#c9a273")
    o = [rect(-130, -110, 260, 110, clay), rect(-130, -110, 260, 10, lite)]
    for sx in (-1, 1):
        tx = sx * 125
        o.append(rect(tx - 26, -165, 52, 165, clay))
        o.append(rect(tx - 26, -165, 52, 8, lite))
        for i in range(5):
            o.append(rect(tx - 26 + i * 11, -176, 7, 11, clay))
    for i in range(12):
        o.append(rect(-104 + i * 18, -120, 9, 10, clay))
    gate = mix(dark, "#ffd27a", c.night * .6)
    o.append(path("M-20,0 V-52 Q0,-76 20,-52 V0 Z", gate))
    return "".join(o)


def prophet_mosque(c):
    cream, cream2 = c.sh("#e8dec6"), c.sh("#f1e9d3")
    green, gold = c.sh("#1b8a4c"), c.sh("#caa24a")
    arch = mix(c.sh("#4a3c28"), "#ffd27a", c.night * .8)
    o = [rect(-330, -86, 660, 86, cream), rect(-310, -124, 620, 40, cream2)]
    for i in range(-14, 15):
        x = i * 21
        o.append(path(f"M{x - 7},0 V-44 Q{x},-62 {x + 7},-44 V0 Z", arch))
    for sx in (-1, 1):
        o.append(path(f"M{sx * 140 - 34},-124 A34,30 0 0 1 {sx * 140 + 34},-124 Z", c.sh("#f4efe0")))
    o.append(path("M-62,-124 A62,78 0 0 1 62,-124 Z", green))
    o.append(path("M-62,-124 A62,78 0 0 1 0,-202 L0,-124 Z", c.sh("#2fb36a"), 'opacity=".35"'))
    o.append(rect(-2, -226, 4, 26, gold) + circ(0, -230, 5, gold))
    for x, h in ((-330, 280), (-262, 250), (-190, 300), (190, 300), (262, 250), (330, 280)):
        o.append(minaret(c, x, h))
    return "".join(o)


def clock_tower(c):
    body, dark, gold = c.sh("#d6c49b"), c.sh("#b39f74"), c.sh("#caa24a")
    o = [rect(-230, -70, 460, 70, c.sh("#cdbb92"))]
    for sx in (-1, 1):
        o.append(rect(sx * 150 - 38, -300, 76, 300, body))
        o.append(poly([(sx * 150 - 38, -300), (sx * 150, -345), (sx * 150 + 38, -300)], gold))
        o.append(windows(c, sx * 150 - 38, -300, 76, 300, 321 + sx, 11, 16, .5))
    o.append(rect(-56, -440, 112, 440, body))
    o.append(windows(c, -56, -440, 112, 370, 325, 11, 16, .5))
    o.append(rect(-92, -540, 184, 110, dark))
    o.append(rect(-70, -600, 140, 62, body))
    o.append(poly([(-70, -600), (0, -690), (70, -600)], gold))
    o.append(rect(-2, -740, 4, 52, gold) + circ(0, -756, 13, gold)
             + circ(5, -759, 11, mix(c.top, c.bot, .55)))
    face = mix("#f6f3e8", "#ffe9a8", c.night)
    o.append(circ(0, -485, 56, "#ffd27a", f'opacity="{c.night * .3:.2f}"'))
    o.append(circ(0, -485, 40, dark) + circ(0, -485, 36, face))
    o.append(path("M0,-485 L0,-510 M0,-485 L16,-478", "none", 'stroke="#2a2a2a" stroke-width="3" stroke-linecap="round"'))
    return "".join(o)


def kaaba_court(c):
    floor, ring = c.sh("#efe9d8"), c.sh("#d9d1bb")
    o = [f'<ellipse cx="0" cy="0" rx="190" ry="40" fill="{floor}"/>',
         f'<ellipse cx="0" cy="0" rx="150" ry="30" fill="none" stroke="{ring}" stroke-width="3"/>',
         f'<ellipse cx="0" cy="0" rx="110" ry="21" fill="none" stroke="{ring}" stroke-width="2"/>']
    back, front = [], []
    n = 36
    for i in range(n):
        a = 2 * math.pi * (i / n + c.t)
        x, y = 130 * math.cos(a), 26 * math.sin(a)
        person = (f'<ellipse cx="{f(x)}" cy="{f(y - 3)}" rx="3.4" ry="6.5" fill="{c.sh("#fafafa")}"/>')
        (front if y >= 0 else back).append(person)
    black, band = c.sh("#17171b"), c.sh("#caa24a")
    cube = [rect(-30, -48, 60, 48, black),
            poly([(30, -48), (46, -56), (46, -8), (30, 0)], c.sh("#0e0e11")),
            poly([(-30, -48), (-14, -56), (46, -56), (30, -48)], c.sh("#2a2a31")),
            rect(-30, -36, 60, 6, band), poly([(30, -36), (46, -44), (46, -38), (30, -30)], band)]
    return "".join(o + back + cube + front)


def balad(c, seed, x0, x1, base):
    r = random.Random(seed)
    x = x0
    out = []
    while x < x1:
        w, h = r.randint(52, 78), r.randint(110, 210)
        out.append(rect(x, base - h, w, h, c.sh(r.choice(["#e3d6b6", "#d8c9a5", "#eadfc4", "#cdbb94"]))))
        out.append(rect(x - 2, base - h - 6, w + 4, 8, c.sh("#b8a47a")))
        for j in range(int(h // 46)):
            wy = base - h + 18 + j * 46
            out.append(rect(x + 8, wy, w - 16, 26, c.sh("#6d4a2b")))
            lit = mix(c.sh("#8a6340"), "#ffd27a", c.night * .85) if r.random() < .5 else c.sh("#8a6340")
            out.append(rect(x + 10, wy + 3, (w - 20) / 2 - 1, 20, lit))
            out.append(rect(x + 10 + (w - 20) / 2 + 1, wy + 3, (w - 20) / 2 - 1, 20, c.sh("#8a6340")))
        x += w + r.randint(2, 6)
    return "".join(out)


def jeddah_tower(c):
    body = c.sh("#6d8197")
    d = "M-40,0 C-34,-200 -16,-420 -3,-640 L3,-640 C16,-420 34,-200 40,0 Z"
    return (path(d, body) + path("M0,0 L0,-640 L3,-640 C16,-420 34,-200 40,0 Z", c.sh("#9fb4c9"), 'opacity=".4"')
            + path("M-3,-640 L0,-700 L3,-640", "none", f'stroke="{c.sh("#9aa7b5")}" stroke-width="3"')
            + path("M0,-20 L0,-630", "none", f'stroke="#ffd27a" stroke-width="2" opacity="{c.night * .6:.2f}"'))


def floating_mosque(c):
    cream = c.sh("#f2efe6")
    o = [rect(-90, 0, 180, 10, c.sh("#9fa7ad"))]
    for i in range(-4, 5):
        o.append(rect(i * 20 - 2, 10, 4, 26, c.sh("#7b858c")))
    o += [rect(-70, -34, 140, 34, cream), path("M-32,-34 A32,32 0 0 1 32,-34 Z", cream),
          rect(60, -90, 11, 56, cream), path("M58,-90 A8,8 0 0 1 73,-90 Z", c.sh("#1f8a4c")),
          circ(0, -28, 6, mix(c.sh("#c7c1ae"), "#ffd27a", c.night * .8))]
    return "".join(o)


def fountain(c):
    hgt = 360 + 12 * math.sin(2 * math.pi * 3 * c.t)
    gid = c.uid("fg")
    col = mix("#ffffff", c.bot, .25)
    col = mix(col, "#0b1226", (1 - c.light) * .55)
    o = [f'<linearGradient id="{gid}" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{col}" stop-opacity=".95"/>'
         f'<stop offset="1" stop-color="{col}" stop-opacity=".15"/></linearGradient>',
         path(f"M-9,0 Q-5,{-hgt * .6:.1f} 0,{-hgt:.1f} Q5,{-hgt * .6:.1f} 9,0 Z", f"url(#{gid})"),
         f'<ellipse cx="0" cy="2" rx="46" ry="9" fill="{col}" opacity=".6"/>']
    r = random.Random(3)
    for i in range(16):
        a = r.uniform(-1, 1)
        k = (c.t * 2 + i / 16) % 1
        o.append(circ(a * 22 * (.4 + k), -hgt + 40 + k * 120, 2.4 - k * 1.2, col, 'opacity=".7"'))
    return "".join(o)


def sea(c, y=BASE):
    gid = c.uid("sea")
    deep, shallow = c.sh("#0b4f6e"), c.sh(mix("#1b86a6", c.bot, .35))
    out = [f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{shallow}"/>'
           f'<stop offset="1" stop-color="{deep}"/></linearGradient>',
           rect(0, y, W, 14, c.sh("#cdbb94")), rect(0, y + 14, W, H - y - 12, f"url(#{gid})")]
    dx = 320 * c.t
    for k in range(5):
        yy = y + 40 + k * 32
        d = f"M-400,{yy} q40,-9 80,0" + " t80,0" * 30
        out.append(f'<path d="{d}" transform="translate({f(dx * (1 + k % 2 * 0))},0)" fill="none" '
                   f'stroke="#ffffff" stroke-width="2" opacity="{.22 - k * .02:.2f}"/>')
    return "".join(out)


def elephant_rock(c):
    base, lite, dark = c.sh("#b4663c"), c.sh("#cf8352"), c.sh("#8d4a28")
    cid = c.uid("cl")
    d = ("M-170,0 C-170,-100 -140,-200 -80,-240 C-90,-310 -20,-360 60,-355 C140,-350 190,-290 160,-220 "
         "C150,-185 150,-150 150,-110 L150,0 L70,0 L70,-70 C70,-110 -30,-110 -30,-70 L-30,0 Z")
    strata = "".join(rect(-200, -y, 400, 5, dark, 'opacity=".28"') for y in range(30, 360, 38))
    return (f'<clipPath id="{cid}"><path d="{d}"/></clipPath><path d="{d}" fill="{base}"/>'
            f'<g clip-path="url(#{cid})">{strata}'
            f'<path d="M-170,0 C-170,-100 -140,-200 -80,-240 C-90,-310 -20,-360 60,-355 L60,0 Z" fill="{lite}" opacity=".35"/>'
            f'<path d="M100,-340 C190,-290 160,-220 150,-110 L150,0 L70,0 L70,-340 Z" fill="{dark}" opacity=".35"/></g>')


def mesa(c, x, w, h, base, col, seed):
    r = random.Random(seed)
    left, right = c.sh(col), c.sh(mix(col, "#4a2412", .35))
    cx = x + w * .55
    o = [poly([(x, base), (x + 8, base - h + 10), (x + 14, base - h), (cx, base - h), (cx, base)], left),
         poly([(cx, base - h), (x + w - 14, base - h), (x + w - 6, base - h + 12), (x + w, base), (cx, base)], right)]
    for k in range(1, 6):
        yy = base - h + k * h / 6 + r.uniform(-4, 4)
        o.append(rect(x + 4, yy, w - 8, 3, c.sh(mix(col, "#2d140a", .4)), 'opacity=".22"'))
    return "".join(o)


def tomb(c):
    base, dark, lite = c.sh("#c4794a"), c.sh("#4a2a18"), c.sh("#d8946a")
    door = mix(dark, "#ffd27a", c.night * .5)
    left = "M-45,-110 L-45,-150 L-33,-150 L-33,-140 L-21,-140 L-21,-130 L-9,-130 L-9,-120 L0,-120 L0,-110 Z"
    right = "M45,-110 L45,-150 L33,-150 L33,-140 L21,-140 L21,-130 L9,-130 L9,-120 L0,-120 L0,-110 Z"
    return (rect(-45, -110, 90, 110, base) + path(left, base) + path(right, base)
            + rect(-48, -114, 96, 7, c.sh("#a9633a")) + rect(-38, -104, 7, 104, lite, 'opacity=".5"')
            + rect(31, -104, 7, 104, lite, 'opacity=".5"') + path("M-14,0 V-62 H14 V0 Z", door)
            + rect(-18, -70, 36, 8, c.sh("#a9633a")))


def maraya(c):
    gid, cid = c.uid("mg"), c.uid("mc")
    sx = -160 + 320 * (c.t % 1)
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{mix(c.top, "#ffffff", .15)}"/>'
            f'<stop offset="1" stop-color="{c.bot}"/></linearGradient>'
            f'<clipPath id="{cid}"><rect x="-120" y="-120" width="240" height="120"/></clipPath>'
            f'<rect x="-120" y="-120" width="240" height="120" fill="url(#{gid})"/>'
            f'<g clip-path="url(#{cid})">'
            + poly([(sx, -120), (sx + 40, -120), (sx - 20, 0), (sx - 60, 0)], "#ffffff", 'opacity=".22"')
            + poly([(-120, 0), (-70, -34), (-30, -12), (30, -40), (80, -16), (120, -30), (120, 0)], c.sh("#a3623a"), 'opacity=".55"')
            + f'</g><rect x="-122" y="-122" width="244" height="124" fill="none" stroke="{c.sh("#3b3b40")}" stroke-width="3"/>')


def aseer_house(c, levels=4, w=64):
    stone, white, dk = c.sh("#85735c"), c.sh("#f2eee4"), c.sh("#2f261c")
    glow = mix(dk, "#ffd27a", c.night * .9)
    o = []
    lvl = 44
    for i in range(levels):
        wi = w - i * 4
        y = -(i + 1) * lvl
        o += [rect(-wi / 2, y, wi, lvl, stone), rect(-wi / 2 - 1, y, wi + 2, 7, white),
              rect(-wi / 2 + 10, y + 16, 8, 14, glow), rect(wi / 2 - 18, y + 16, 8, 14, glow)]
    top = -levels * lvl
    tw = w - levels * 4
    o.append(rect(-tw / 2 - 3, top - 8, tw + 6, 8, white))
    return "".join(o)


def mud_block(c, x, w, h, col="#b98d5f", seed=1):
    base_c = c.sh(col)
    dk = c.sh(mix(col, "#3a2414", .45))
    lit = mix(dk, "#ffd27a", c.night * .9)
    o = [rect(x, -h, w, h, base_c)]
    n = int(w // 14)
    off = (w - n * 14) / 2
    for i in range(n):
        px = x + off + i * 14
        o.append(poly([(px, -h), (px + 7, -h - 9), (px + 14, -h)], base_c))
    for j in range(int((h - 24) // 34)):
        for i in range(int(w // 28)):
            wx, wy = x + 10 + i * 28, -h + 18 + j * 34
            o.append(poly([(wx, wy + 14), (wx + 4, wy), (wx + 8, wy + 14)], lit))
    o.append(rect(x, -h, 6, h, c.sh(mix(col, "#ffffff", .25)), 'opacity=".25"'))
    return "".join(o)


# ----------------------------------------------------------------------------- scenes


def scene_riyadh(c):
    sh = c.sh
    o = [ridge(11, 690, 70, 8, sh(mix("#d9b98a", c.bot, .3)), opacity=.9),
         towers(c, 21, -20, 1620, BASE, 50, 130, 26, 46, sh(mix(c.bot, "#7b8ea3", .55)), win=False),
         towers(c, 22, -20, 1620, BASE, 90, 220, 34, 64, sh("#4a5d73")),
         g(kingdom_centre(c), 1010, BASE), g(faisaliah(c), 1290, BASE, .95),
         towers(c, 23, 1390, 1620, BASE, 120, 240, 36, 60, sh("#3b4c60")),
         g(masmak(c), 400, BASE + 5, 1.1), ground(c, sh("#d9b57d"), sh("#b98d55"))]
    for x, s, ph in ((110, 1.2, 0), (265, 1.0, .3), (1500, 1.3, .6), (1380, .9, .15)):
        o.append(palm(c, x, BASE + 70 + (1.3 - s) * 40, s, ph))
    return "".join(o)


def scene_jeddah(c):
    sh = c.sh
    o = [ridge(71, 690, 60, 8, sh(mix(c.bot, "#8a9aab", .5)), opacity=.8),
         towers(c, 72, 720, 1620, BASE, 60, 150, 28, 50, sh(mix(c.bot, "#6f8196", .5)), win=False),
         towers(c, 73, 900, 1620, BASE, 90, 230, 34, 60, sh("#4f6279")),
         balad(c, 74, -10, 740, BASE), g(jeddah_tower(c), 1180, BASE), sea(c, BASE),
         g(floating_mosque(c), 540, BASE + 48), g(fountain(c), 930, BASE + 60)]
    return "".join(o)


def scene_makkah(c):
    sh = c.sh
    o = [ridge(81, 700, 150, 14, sh(mix("#8a5a44", c.bot, .3)), jag=True),
         ridge(82, 735, 110, 18, sh("#6b4636"), jag=True),
         towers(c, 83, -20, 560, BASE, 50, 120, 36, 70, sh("#cdbb98")),
         towers(c, 84, 1040, 1620, BASE, 50, 120, 36, 70, sh("#cdbb98")),
         g("".join(minaret(c, 0, 340) for _ in [0]), 430, BASE),
         g("".join(minaret(c, 0, 340) for _ in [0]), 1170, BASE),
         g(clock_tower(c), 800, BASE), ground(c, sh("#e2d9c4"), sh("#cfc4a8")),
         g(kaaba_court(c), 800, 786, 1.5)]
    return "".join(o)


def scene_madinah(c):
    sh = c.sh
    o = [ridge(51, 690, 150, 9, sh(mix("#6e4a3a", c.bot, .3)), jag=True, opacity=.95),
         ridge(52, 725, 90, 12, sh(mix("#7d5a48", c.bot, .25)), jag=True),
         towers(c, 53, -20, 420, BASE, 40, 90, 30, 56, sh("#d9cdb0")),
         towers(c, 54, 1190, 1620, BASE, 40, 90, 30, 56, sh("#d9cdb0")),
         g(prophet_mosque(c), 800, BASE, 1.25), ground(c, sh("#e9e1cd"), sh("#cfc6ae"))]
    for x, s, ph in ((110, 1.3, 0), (245, 1.1, .25), (1360, 1.15, .5), (1495, 1.3, .75)):
        o.append(palm(c, x, BASE + 80, s, ph))
    return "".join(o)


def scene_alula(c):
    sh = c.sh
    o = [ridge(31, 700, 110, 10, sh(mix(c.bot, "#b4673e", .5)), jag=True, opacity=.9),
         mesa(c, -40, 330, 300, BASE, "#c47a4a", 1), mesa(c, 250, 260, 220, BASE, "#c98652", 2),
         mesa(c, 1000, 640, 430, BASE, "#b9693a", 3),
         g(elephant_rock(c), 440, BASE, 1.25),
         g(tomb(c), 1180, BASE, 1.5), g(tomb(c), 1390, BASE, 1.15),
         g(maraya(c), 850, BASE + 18, .9), ground(c, sh("#d49a63"), sh("#b57a46"))]
    for x, s, ph in ((700, 1.0, .1), (1010, .9, .4), (180, 1.2, .7)):
        o.append(palm(c, x, BASE + 60, s, ph))
    return "".join(o)


def scene_abha(c):
    sh = c.sh
    hill = [(100, 755), (220, 640), (330, 585), (450, 575), (560, 600), (680, 660), (800, 755)]

    def hill_y(x):
        for (xa, ya), (xb, yb) in zip(hill, hill[1:]):
            if xa <= x <= xb:
                return ya + (yb - ya) * (x - xa) / (xb - xa)
        return 755

    o = [ridge(41, 560, 170, 9, sh(mix(c.bot, "#5d8a8f", .55)), opacity=.95),
         ridge(42, 640, 150, 8, sh(mix(c.bot, "#3f7a55", .35)))]
    mist = mix("#ffffff", c.bot, .3)
    mist = mix(mist, "#0b1226", (1 - c.light) * .8)
    for period, y, sc, op in ((800, 640, 3.2, .35), (1000, 700, 4.0, .28)):
        for i in range(-1, 3):
            o.append(f'<ellipse cx="{f(period * i + period * c.t + 300)}" cy="{y}" rx="{int(60 * sc)}" ry="{int(14 * sc)}" fill="{mist}" opacity="{op}"/>')
    o.append(poly(hill, sh("#3d7a4c")))
    for x, lv, w in ((190, 3, 56), (260, 4, 62), (340, 5, 66), (430, 4, 64), (520, 3, 58), (610, 4, 60)):
        o.append(g(aseer_house(c, lv, w), x, hill_y(x) + 8))
    o.append(ridge(43, 735, 110, 7, sh("#2f6b45")))
    r = random.Random(7)
    for _ in range(34):
        x = r.uniform(780, 1620)
        y = BASE + r.uniform(-5, 60)
        s = r.uniform(.7, 1.4)
        o.append(poly([(x - 14 * s, y), (x, y - 50 * s), (x + 14 * s, y)], sh("#1d4a2a")))
    # cable car
    x1, y1, x2, y2 = 60, 150, 1450, 560
    o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{sh("#222222")}" stroke-width="3"/>')
    for off in (0.0, .5):
        u = (c.t + off) % 1
        op = clamp(min(u * 8, (1 - u) * 8))
        x, y = x1 + (x2 - x1) * u, y1 + (y2 - y1) * u
        sway = 3 * math.sin(2 * math.pi * 3 * c.t)
        o.append(f'<g opacity="{op:.2f}" transform="translate({f(x)},{f(y)}) rotate({sway:.1f})">'
                 f'<line x1="0" y1="0" x2="0" y2="16" stroke="{sh("#222222")}" stroke-width="2"/>'
                 + rect(-17, 16, 34, 24, sh("#d94f3d")) + rect(-13, 21, 26, 11, mix(sh("#cfe6f5"), "#ffd27a", c.night * .8)) + "</g>")
    o.append(ridge(44, 790, 60, 8, sh("#244f33")))
    return "".join(o)


def scene_diriyah(c):
    sh = c.sh
    o = [ridge(91, 690, 80, 8, sh(mix("#d9b98a", c.bot, .3)), opacity=.9)]
    walls = [(-20, 230, 90), (230, 150, 130), (1030, 210, 110), (1260, 180, 150), (1460, 160, 100)]
    for x, w, h in walls:
        o.append(g(mud_block(c, 0, w, h, "#a9825a"), x, BASE))
    o.append(g(mud_block(c, 0, 90, 300, "#b98d5f"), 470, BASE))
    o.append(g(mud_block(c, 0, 260, 190, "#c19468"), 620, BASE))
    o.append(g(mud_block(c, 0, 80, 250, "#b98d5f"), 880, BASE))
    o.append(g(mud_block(c, 0, 150, 150, "#c9a073"), 380, BASE + 4))
    o.append(g(mud_block(c, 0, 120, 120, "#c9a073"), 930, BASE + 4))
    o.append(ground(c, sh("#d9b57d"), sh("#b98d55")))
    for x, s, ph in ((90, 1.3, 0), (300, 1.0, .3), (780, .9, .6), (1180, 1.1, .2), (1520, 1.3, .8)):
        o.append(palm(c, x, BASE + 65 + (1.3 - s) * 40, s, ph))
    return "".join(o)


def scene_watan(c):
    sh = c.sh
    o = [ridge(61, 690, 90, 8, sh(mix("#d9b98a", c.bot, .3)), opacity=.9),
         towers(c, 62, 520, 1620, BASE, 50, 130, 26, 46, sh(mix(c.bot, "#7b8ea3", .55)), win=False),
         g(elephant_rock(c), 230, BASE, 1.05),
         towers(c, 63, 640, 1620, BASE, 80, 190, 34, 60, sh("#4a5d73")),
         g(prophet_mosque(c), 600, BASE, .8),
         g(kingdom_centre(c), 960, BASE, .95), g(faisaliah(c), 1140, BASE, .9),
         g(clock_tower(c), 1400, BASE, .62),
         ground(c, sh("#d9b57d"), sh("#b98d55"))]
    for x, s, ph in ((90, 1.3, 0), (420, 1.0, .3), (830, 1.2, .55), (1250, .9, .15), (1520, 1.3, .7)):
        o.append(palm(c, x, BASE + 65 + (1.3 - s) * 40, s, ph))
    return "".join(o)


SCENES = {"riyadh": scene_riyadh, "jeddah": scene_jeddah, "makkah": scene_makkah, "madinah": scene_madinah,
          "alula": scene_alula, "abha": scene_abha, "diriyah": scene_diriyah, "watan": scene_watan}
CLOUDS = {"abha": 1.4}


def band(c):
    out = [rect(0, H - 64, W, 64, "#0b3d2a", 'opacity=".93"'), rect(0, H - 64, W, 3, "#e2c071", 'opacity=".85"')]
    for i in range(21):
        cx, cy = 40 + i * 76, H - 32
        out.append(f'<g fill="#e2c071" opacity=".6"><rect x="{cx - 8}" y="{cy - 8}" width="16" height="16"/>'
                   f'<rect x="{cx - 8}" y="{cy - 8}" width="16" height="16" transform="rotate(45 {cx} {cy})"/></g>')
    return "".join(out)


def build_svg(city, p, t=0.0):
    c = Ctx(p, t)
    sky = c.uid("sky")
    body = SCENES[city](c)
    return "".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'preserveAspectRatio="xMidYMid slice">',
        f'<defs><linearGradient id="{sky}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c.top}"/>'
        f'<stop offset=".72" stop-color="{c.bot}"/></linearGradient></defs>',
        rect(0, 0, W, H, f"url(#{sky})"), stars(c), celestial(c), clouds(c, CLOUDS.get(city, 1.0)),
        birds(c), body, band(c), "</svg>"])


# ----------------------------------------------------------------------------- output

VARIANTS = [("dawn", .04, .15), ("day", .30, .40), ("sunset", .52, .70), ("night", .80, .20)]
ERA_IMAGES = {  # era slug -> (scene, variant)
    "ancient": ("alula", "sunset"), "islam": ("makkah", "night"), "medieval": ("jeddah", "day"),
    "first-state": ("diriyah", "sunset"), "second-state": ("diriyah", "night"),
    "unification": ("riyadh", "dawn"), "modern": ("watan", "sunset"),
}
VIDEO_SCENES = ["watan", "riyadh", "jeddah", "makkah", "madinah", "alula", "abha"]


def rsvg(svg, w, h, fmt="png"):
    return subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h), "-f", fmt],
                          input=svg.encode("utf-8"), capture_output=True, check=True).stdout


def make_stills():
    IMG.mkdir(parents=True, exist_ok=True)
    for city in SCENES:
        for name, p, t in VARIANTS:
            (IMG / f"{city}-{name}.svg").write_text(build_svg(city, p, t), encoding="utf-8")
        print("stills", city)
    for slug, (city, name) in ERA_IMAGES.items():
        shutil.copyfile(IMG / f"{city}-{name}.svg", IMG / f"era-{slug}.svg")
    ffmpeg = shutil.which("ffmpeg")
    for city in VIDEO_SCENES:
        p, t = .52, .70
        png = rsvg(build_svg(city, p, t), 1280, 720)
        out = IMG / f"{city}-poster.jpg"
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-f", "image2pipe", "-i", "-", "-q:v", "4", str(out)],
                       input=png, check=True)
    (IMG / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0a6b3a"/>'
        '<g fill="#e2c071"><rect x="17" y="17" width="30" height="30"/>'
        '<rect x="17" y="17" width="30" height="30" transform="rotate(45 32 32)"/></g>'
        '<circle cx="32" cy="32" r="7" fill="#0a6b3a"/></svg>', encoding="utf-8")


def _frame(args):
    city, i, n, w, h = args
    u = i / n
    return rsvg(build_svg(city, u % 1.0, u), w, h)


def make_video(city, seconds=12, fps=20, w=960, h=540):
    VID.mkdir(parents=True, exist_ok=True)
    n = seconds * fps
    out = VID / f"{city}.mp4"
    cmd = [shutil.which("ffmpeg"), "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps),
           "-c:v", "png", "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "27", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", "-an", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(max(1, (os.cpu_count() or 2))) as pool:
        for frame in pool.imap(_frame, [(city, i, n, w, h) for i in range(n)], chunksize=4):
            proc.stdin.write(frame)
    proc.stdin.close()
    proc.wait()
    print("video", city, f"{out.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("stills", "all"):
        make_stills()
    if what in ("videos", "all"):
        names = sys.argv[2:] or VIDEO_SCENES
        for name in names:
            sz = (1280, 720) if name == "watan" else (960, 540)
            make_video(name, w=sz[0], h=sz[1])
