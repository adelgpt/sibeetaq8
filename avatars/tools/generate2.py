#!/usr/bin/env python3
"""Illustrated (shaded, semi-realistic) vector caricature heads. Face only.

Usage: python3 avatars/tools/generate2.py  -> avatars/v2/svg/*.svg
"""
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKINS = {
    "fair":  dict(hi="#fde3cb", base="#f2c6a0", sh="#d4956c", deep="#a1603e", line="#7a4428", lip="#c9706a"),
    "tan":   dict(hi="#f8cfa6", base="#e4a878", sh="#bf7a4c", deep="#8c4f2e", line="#6a3a20", lip="#b8604f"),
    "brown": dict(hi="#e3b088", base="#c48659", sh="#9a5f37", deep="#6e3f22", line="#4e2a15", lip="#9c4f40"),
    "dark":  dict(hi="#b98563", base="#8f5a38", sh="#6c3f24", deep="#4a2915", line="#33190b", lip="#7a3b2e"),
}

FACE = ("M256,92 C342,92 386,150 386,236 C386,312 370,372 338,416 "
        "C312,452 286,470 256,472 C226,470 200,452 174,416 C142,372 126,312 126,236 C126,150 170,92 256,92 Z")


class SVG:
    def __init__(self, uid):
        self.uid = uid
        self.defs = []
        self.body = []

    def id(self, name):
        return f"{self.uid}-{name}"

    def ref(self, name):
        return f"url(#{self.id(name)})"

    def lin(self, name, stops, x1=0, y1=0, x2=0, y2=1):
        s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
        self.defs.append(f'<linearGradient id="{self.id(name)}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>')
        return self.ref(name)

    def rad(self, name, stops, cx=0.5, cy=0.5, r=0.5, fx=None, fy=None):
        fx = cx if fx is None else fx
        fy = cy if fy is None else fy
        s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
        self.defs.append(f'<radialGradient id="{self.id(name)}" cx="{cx}" cy="{cy}" r="{r}" fx="{fx}" fy="{fy}">{s}</radialGradient>')
        return self.ref(name)

    def clip(self, name, d):
        self.defs.append(f'<clipPath id="{self.id(name)}"><path d="{d}"/></clipPath>')
        return self.ref(name)

    def add(self, s):
        self.body.append(s)

    def render(self):
        blur = "".join(f'<filter id="{self.id("b"+str(n))}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>'
                       for n in (1, 2, 3, 5, 8, 12, 20))
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">'
                f'<defs>{blur}{"".join(self.defs)}</defs>{"".join(self.body)}</svg>\n')


def blur(s, n):
    return f'filter="url(#{s.id("b"+str(n))})"'


def path(d, fill="none", stroke=None, sw=0, op=1, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if stroke else ""
    return f'<path d="{d}" fill="{fill}"{st} opacity="{op}" {extra}/>'


def ell(cx, cy, rx, ry, fill, op=1, extra=""):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" opacity="{op}" {extra}/>'


def strands(rng, n, region, fn, colors, sw=(1.2, 2.4), op=(0.35, 0.8)):
    """Generate hair strokes. region=(x0,y0,x1,y1); fn(x,y)->(dx,dy,bend)."""
    out = []
    x0, y0, x1, y1 = region
    for _ in range(n):
        x = rng.uniform(x0, x1)
        y = rng.uniform(y0, y1)
        dx, dy, bend = fn(x, y)
        mx, my = x + dx / 2 + bend, y + dy / 2
        c = rng.choice(colors)
        out.append(path(f"M{x:.1f},{y:.1f} Q{mx:.1f},{my:.1f} {x+dx:.1f},{y+dy:.1f}", stroke=c,
                        sw=f"{rng.uniform(*sw):.2f}", op=f"{rng.uniform(*op):.2f}"))
    return "".join(out)


# ---------------------------------------------------------------- background
def background(s, c):
    g = s.rad("bg", [(0, c.get("bg1", "#3a3d45"), 1), (1, c.get("bg2", "#141519"), 1)], cy=0.42, r=0.75)
    s.add(f'<rect width="512" height="512" rx="56" fill="{g}"/>')
    s.add(ell(256, 500, 150, 22, "#000", 0.35, blur(s, 12)))


# ---------------------------------------------------------------- face
def face(s, c):
    k = SKINS[c["skin"]]
    fill = s.rad("skin", [(0, k["hi"], 1), (0.55, k["base"], 1), (1, k["sh"], 1)], cx=0.42, cy=0.38, r=0.68)
    s.add(path(FACE, fill, k["line"], 2.4, 1, 'stroke-opacity="0.8"'))
    cp = s.clip("face", FACE)
    g = [f'<g clip-path="{cp}">']
    # side & jaw shading (light from upper-left)
    g.append(ell(390, 270, 60, 190, k["sh"], 0.75, blur(s, 20)))
    g.append(ell(122, 270, 40, 170, k["sh"], 0.45, blur(s, 20)))
    g.append(ell(256, 500, 120, 60, k["deep"], 0.35, blur(s, 20)))
    # forehead + cheek highlights
    g.append(ell(236, 160, 80, 44, k["hi"], 0.85, blur(s, 20)))
    g.append(ell(186, 330, 26, 18, k["hi"], 0.7, blur(s, 8)))
    g.append(ell(328, 330, 22, 16, k["hi"], 0.45, blur(s, 8)))
    # blush
    g.append(ell(184, 342, 32, 20, "#e2614f", c.get("blush", 0.22), blur(s, 12)))
    g.append(ell(330, 342, 30, 20, "#e2614f", c.get("blush", 0.22), blur(s, 12)))
    # eye sockets
    for x in (208, 304):
        g.append(ell(x, 258, 50, 30, k["sh"], 0.5, blur(s, 8)))
    # under-nose & lip shadows, chin highlight
    g.append(ell(262, 378, 30, 9, k["deep"], 0.35, blur(s, 5)))
    g.append(ell(256, 446, 22, 9, k["deep"], 0.25, blur(s, 5)))
    g.append(ell(250, 456, 20, 9, k["hi"], 0.6, blur(s, 5)))
    if c.get("old"):
        for y, w in ((150, 56), (168, 48), (186, 40)):
            g.append(path(f"M{256-w},{y+4} Q256,{y-6} {256+w},{y+4}", stroke=k["deep"], sw=2.2, op=0.45, extra=blur(s, 1)))
        for side in (-1, 1):
            x = 256 + side * 92
            for dy in (-8, 2, 12):
                g.append(path(f"M{x},{270+dy} l{side*16},{dy*0.6}", stroke=k["deep"], sw=1.8, op=0.4, extra=blur(s, 1)))
            g.append(path(f"M{256+side*40},{350} C{256+side*58},{372} {256+side*58},{400} {256+side*46},{420}",
                          stroke=k["deep"], sw=3, op=0.4, extra=blur(s, 2)))
        g.append(ell(208, 300, 26, 8, k["deep"], 0.25, blur(s, 3)))
        g.append(ell(304, 300, 26, 8, k["deep"], 0.25, blur(s, 3)))
    if c.get("stubble"):
        sd = ("M136,300 C150,380 200,470 256,474 C312,470 362,380 376,300 C360,350 330,372 300,380 "
              "C280,372 268,372 256,374 C244,372 232,372 212,380 C182,372 152,350 136,300 Z")
        g.append(path(sd, c.get("hair_color", "#1d140f"), op=0.2, extra=blur(s, 3)))
        g.append(path(sd, c.get("hair_color", "#1d140f"), op=0.18, extra=blur(s, 8)))
    g.append("</g>")
    s.add("".join(g))


def ears(s, c):
    k = SKINS[c["skin"]]
    fill = s.rad("ear", [(0, k["base"], 1), (1, k["sh"], 1)], cx=0.5, cy=0.4, r=0.6)
    for side in (-1, 1):
        x = 256 + side * 128
        d = (f"M{x},{230} C{x+side*30},{216} {x+side*40},{250} {x+side*34},{282} "
             f"C{x+side*30},{312} {x+side*16},{322} {x},{316} Z")
        s.add(path(d, fill, k["line"], 2.2, 1, 'stroke-opacity="0.8"'))
        s.add(path(f"M{x+side*6},{244} C{x+side*26},{240} {x+side*28},{272} {x+side*18},{296}", stroke=k["deep"], sw=4, op=0.45, extra=blur(s, 1)))


def nose(s, c):
    k = SKINS[c["skin"]]
    sc = c.get("nose_s", 1.0)
    g = [f'<g transform="translate(256 330) scale({sc}) translate(-256 -330)">']
    g.append(path("M258,262 C258,290 262,318 262,334", stroke=k["hi"], sw=11, op=0.75, extra=blur(s, 3)))
    g.append(path("M274,266 C280,296 290,322 292,346", stroke=k["sh"], sw=10, op=0.7, extra=blur(s, 5)))
    g.append(path("M240,268 C236,296 228,322 226,344", stroke=k["sh"], sw=7, op=0.4, extra=blur(s, 5)))
    ball = s.rad("noseball", [(0, k["hi"], 1), (0.6, k["base"], 1), (1, k["sh"], 1)], cx=0.42, cy=0.38, r=0.6)
    g.append(ell(258, 344, 30, 24, ball, 0.95, blur(s, 2)))
    for side in (-1, 1):
        x = 256 + side * 26
        g.append(path(f"M{x},{332} C{x+side*14},{338} {x+side*14},{360} {x-side*2},{364}", stroke=k["deep"], sw=2.6, op=0.65, extra=blur(s, 1)))
    g.append(ell(245, 362, 8, 4.5, k["deep"], 0.8, blur(s, 1)))
    g.append(ell(270, 362, 8, 4.5, k["deep"], 0.8, blur(s, 1)))
    g.append(path("M240,366 C250,372 264,372 274,366", stroke=k["deep"], sw=2, op=0.5))
    g.append(ell(250, 334, 8, 6, "#ffffff", 0.55, blur(s, 2)))
    g.append("</g>")
    s.add("".join(g))


def eyes(s, c):
    k = SKINS[c["skin"]]
    iris = c.get("iris", "#7a3e16")
    ig = s.rad("iris", [(0, "#d99a4e", 1), (0.45, iris, 1), (1, "#1e0d04", 1)], r=0.5)
    sg = s.lin("sclera", [(0, "#d8cfc8", 1), (0.35, "#fbf8f5", 1), (1, "#eee6e0", 1)])
    y = c.get("eye_y", 268)
    for i, x in enumerate((208, 304)):
        side = -1 if i == 0 else 1
        if c.get("closed"):
            s.add(path(f"M{x-30},{y} C{x-14},{y+14} {x+14},{y+14} {x+30},{y}", stroke=k["line"], sw=4.5))
            continue
        d = f"M{x-32},{y+2} C{x-20},{y-24} {x+20},{y-26} {x+33},{y-2} C{x+20},{y+18} {x-18},{y+20} {x-32},{y+2} Z"
        s.add(path(d, sg, k["line"], 1.5, 0.9))
        cp = s.clip(f"eye{i}", d)
        lx = c.get("look", 0) * 5
        g = [f'<g clip-path="{cp}">']
        g.append(f'<circle cx="{x+lx}" cy="{y-2}" r="18" fill="{ig}"/>')
        g.append(f'<circle cx="{x+lx}" cy="{y-2}" r="18" fill="none" stroke="#1a0b03" stroke-width="2" opacity="0.7"/>')
        g.append(f'<circle cx="{x+lx}" cy="{y-2}" r="7.5" fill="#0b0604"/>')
        g.append(ell(x, y - 18, 40, 10, "#5a3a2a", 0.45, blur(s, 3)))  # lid shadow
        g.append(f'<circle cx="{x+lx-6}" cy="{y-9}" r="4.8" fill="#fff"/>')
        g.append(f'<circle cx="{x+lx+6}" cy="{y+5}" r="2" fill="#fff" opacity="0.8"/>')
        if c.get("sleepy"):
            g.append(path(f"M{x-40},{y-30} L{x+40},{y-30} L{x+40},{y-6} C{x+14},{y-12} {x-14},{y-12} {x-40},{y-4} Z", s.ref("skin")))
        g.append("</g>")
        s.add("".join(g))
        # upper lash line (tapered) + crease + lower lid
        lash = c.get("lash", "#1b0f0a")
        w = 6 if c.get("female") else 4
        s.add(path(f"M{x-34},{y+3} C{x-22},{y-26} {x+20},{y-28} {x+35},{y-3} C{x+18},{y-22} {x-18},{y-20} {x-34},{y+3} Z",
                   lash, lash, w * 0.6))
        s.add(path(f"M{x-28},{y-22} C{x-12},{y-40} {x+16},{y-40} {x+30},{y-22}", stroke=k["deep"], sw=2.2, op=0.55, extra=blur(s, 1)))
        s.add(path(f"M{x-26},{y+10} C{x-10},{y+20} {x+12},{y+20} {x+28},{y+8}", stroke=k["deep"], sw=1.6, op=0.35))
        if c.get("female"):
            wx = x + side * 34
            s.add(path(f"M{wx},{y-4} L{wx+side*14},{y-16} L{wx+side*2},{y-1} Z", lash, lash, 2))
            rng = random.Random(i)
            for t in range(7):
                tx = x - 24 + t * 8 if side == 1 else x + 24 - t * 8
                ty = y - 16 - (3 if 1 < t < 5 else 0)
                s.add(path(f"M{tx},{ty} q{side*4},-8 {side*8},-12", stroke=lash, sw=1.6, op=0.85))


def brows(s, c):
    col = c.get("brow_color", c.get("hair_color", "#1d140f"))
    rng = random.Random(3)
    y = c.get("eye_y", 268) - 50
    thick = c.get("brow_w", 22)
    for i, x in enumerate((208, 304)):
        side = -1 if i == 0 else 1
        inner, outer = x - side * 36, x + side * 38
        lift = c.get("brow_lift", 0)
        d = (f"M{inner},{y+10} C{inner+side*14},{y-8-lift} {outer-side*20},{y-14-lift} {outer},{y+4} "
             f"C{outer-side*18},{y-4+thick*0.4-lift} {inner+side*14},{y+thick*0.6-lift} {inner},{y+10+thick*0.5} Z")
        s.add(path(d, col, op=0.9, extra=blur(s, 1)))
        def fn(px, py, side=side):
            t = (px - inner) / (outer - inner)
            return side * 14, -6 + t * 10, 0
        cp = s.clip(f"brow{i}", d)
        s.add(f'<g clip-path="{cp}">' + strands(rng, 160, (min(inner, outer), y - 20, max(inner, outer), y + 24), fn,
                                                 [col, col, c.get("brow_hi", "#4a3a30")], sw=(1.6, 3), op=(0.6, 1)) + "</g>")


def mouth(s, c):
    k = SKINS[c["skin"]]
    kind = c.get("mouth", "smile")
    lip = c.get("lip", k["lip"])
    y = 408
    if kind == "grin":
        d = f"M214,{y-6} C236,{y+2} 276,{y+2} 298,{y-6} C292,{y+24} 274,{y+38} 256,{y+38} C238,{y+38} 220,{y+24} 214,{y-6} Z"
        s.add(path(d, "#4a1514", k["line"], 1.8))
        cp = s.clip("mouth", d)
        tg = s.lin("teeth", [(0, "#ffffff", 1), (1, "#d9d2cc", 1)])
        s.add(f'<g clip-path="{cp}"><path d="M200,{y-10} L312,{y-10} L312,{y+12} C280,{y+18} 232,{y+18} 200,{y+12} Z" fill="{tg}"/>'
              + "".join(path(f"M{x},{y-8} L{x},{y+12}", stroke="#cfc6be", sw=1.2) for x in (234, 246, 256, 266, 278))
              + ell(256, y + 34, 26, 12, "#c25a5e") + "</g>")
        s.add(path(f"M226,{y+30} C240,{y+44} 272,{y+44} 286,{y+30}", stroke=k["deep"], sw=2.5, op=0.35, extra=blur(s, 1)))
    elif kind == "smile":
        s.add(path(f"M222,{y} C240,{y+14} 272,{y+14} 290,{y}", stroke=k["line"], sw=3.4))
        s.add(path(f"M234,{y+16} C246,{y+22} 266,{y+22} 278,{y+16}", lip, op=0.0))
        s.add(path(f"M236,{y+14} C248,{y+24} 264,{y+24} 276,{y+14}", stroke=lip, sw=6, op=0.6, extra=blur(s, 2)))
        for side in (-1, 1):
            s.add(path(f"M{256+side*34},{y-4} q{side*6},4 {side*4},10", stroke=k["deep"], sw=2.2, op=0.6))
    elif kind == "lips":
        ug = s.lin("lipu", [(0, lip, 1), (1, k["deep"], 1)])
        lg = s.lin("lipl", [(0, k["deep"], 1), (0.4, lip, 1), (1, lip, 1)])
        s.add(path(f"M224,{y} C234,{y-14} 248,{y-12} 256,{y-6} C264,{y-12} 278,{y-14} 288,{y} C272,{y+4} 240,{y+4} 224,{y} Z", ug, k["line"], 1))
        s.add(path(f"M224,{y} C240,{y+6} 272,{y+6} 288,{y} C280,{y+22} 232,{y+22} 224,{y} Z", lg, k["line"], 1))
        s.add(ell(262, y + 10, 10, 3.5, "#fff", 0.55, blur(s, 1)))
        for side in (-1, 1):
            s.add(path(f"M{256+side*32},{y} q{side*5},-1 {side*7},-5", stroke=k["deep"], sw=2, op=0.5))


def mustache(s, c, rng):
    kind = c.get("mustache")
    if not kind:
        return
    col = c.get("facial_color", c.get("hair_color", "#1d140f"))
    hi = c.get("facial_hi", "#5a4a40")
    if kind == "thick":
        d = ("M256,380 C238,370 212,372 198,388 C188,400 176,404 164,400 C172,414 196,418 214,412 "
             "C230,406 244,404 256,402 C268,404 282,406 298,412 C316,418 340,414 348,400 C336,404 324,400 314,388 C300,372 274,370 256,380 Z")
    else:  # walrus
        d = ("M256,376 C232,364 196,370 180,394 C172,410 178,426 190,428 C204,418 220,420 232,424 "
             "C244,416 250,414 256,414 C262,414 268,416 280,424 C292,420 308,418 322,428 C334,426 340,410 332,394 C316,370 280,364 256,376 Z")
    g = s.lin("must", [(0, col, 1), (1, hi, 1)])
    s.add(path(d, g, "#00000055", 1.2))
    cp = s.clip("mustc", d)
    fn = lambda x, y: ((1 if x > 256 else -1) * rng.uniform(10, 20), rng.uniform(16, 26), (1 if x > 256 else -1) * 3)
    s.add(f'<g clip-path="{cp}">' + strands(rng, 260, (160, 366, 352, 420), fn, c.get("strand_cols", [col, hi, "#000000"]), sw=(1, 2), op=(0.3, 0.7)) + "</g>")


def beard(s, c, rng):
    kind = c.get("beard")
    if not kind:
        return
    col = c.get("facial_color", c.get("hair_color", "#1d140f"))
    hi = c.get("facial_hi", "#5a4a40")
    if kind == "goatee":
        d = "M228,434 C232,462 244,486 256,490 C268,486 280,462 284,434 C272,446 264,444 256,444 C248,444 240,446 228,434 Z"
        d2 = "M246,424 C250,432 262,432 266,424 C262,438 250,438 246,424 Z"
        region = (224, 420, 288, 492)
    else:  # full
        d = ("M134,286 C138,400 186,520 256,530 C326,520 374,400 378,286 C368,340 344,370 318,382 "
             "C300,392 286,388 256,390 C226,388 212,392 194,382 C168,370 144,340 134,286 Z")
        d2 = None
        region = (130, 280, 382, 532)
    g = s.lin("beard", [(0, hi, 1), (1, col, 1)])
    s.add(path(d, g, "#00000040", 1.2))
    if d2:
        s.add(path(d2, col, op=0.9))
    cp = s.clip("beardc", d)
    fn = lambda x, y: ((x - 256) * 0.06 + rng.uniform(-3, 3), rng.uniform(14, 28), rng.uniform(-4, 4))
    s.add(f'<g clip-path="{cp}">' + strands(rng, 700 if kind == "full" else 160, region, fn, c.get("strand_cols", [col, hi, "#000000"]), sw=(1, 2), op=(0.3, 0.7)) + "</g>")


def glasses(s, c):
    kind = c.get("glasses")
    if not kind:
        return
    fg = s.lin("frame", [(0, "#f3d27a", 1), (0.5, "#b8862b", 1), (1, "#f0c96a", 1)])
    y = c.get("eye_y", 268)
    for x in (208, 304):
        s.add(f'<circle cx="{x}" cy="{y}" r="40" fill="#cfe6ff" fill-opacity="0.12" stroke="{fg}" stroke-width="5"/>')
        s.add(path(f"M{x-22},{y-24} C{x-30},{y-10} {x-30},{y+4} {x-26},{y+12}", stroke="#fff", sw=4, op=0.45))
    s.add(path(f"M248,{y-6} Q256,{y-14} 264,{y-6}", stroke=fg, sw=4.5))
    s.add(path(f"M168,{y-6} L130,{y-14}", stroke=fg, sw=4.5))
    s.add(path(f"M344,{y-6} L382,{y-14}", stroke=fg, sw=4.5))


# ---------------------------------------------------------------- headwear / hair
def shemagh(s, c, layer):
    red = c.get("shemagh") == "red"
    if red:
        pc = "#c4222b"
        s.defs.append(f'<pattern id="{s.id("shm")}" width="22" height="22" patternUnits="userSpaceOnUse" patternTransform="rotate(45 256 256)">'
                      f'<rect width="22" height="22" fill="#faf7f2"/><rect x="2" y="2" width="8" height="8" fill="{pc}"/>'
                      f'<rect x="13" y="13" width="8" height="8" fill="{pc}"/><rect x="13" y="3" width="4" height="4" fill="{pc}" opacity="0.6"/>'
                      f'<rect x="3" y="13" width="4" height="4" fill="{pc}" opacity="0.6"/></pattern>')
        fill = s.ref("shm")
    else:
        fill = s.lin("ghutra", [(0, "#ffffff", 1), (1, "#e9ecf0", 1)])
    if layer == "back":
        d = "M256,58 C404,58 440,200 444,320 L450,440 C424,486 340,500 256,500 C172,500 88,486 62,440 L68,320 C72,200 108,58 256,58 Z"
        s.add(path(d, fill, "#00000040", 1.5))
        cp = s.clip("shback", d)
        s.add(f'<g clip-path="{cp}">'
              + ell(256, 470, 170, 60, "#000", 0.35, blur(s, 20))
              + "".join(path(f"M{x},{200} C{x+8},{320} {x-6},{400} {x+4},{500}", stroke="#000", sw=14, op=0.12, extra=blur(s, 8)) for x in (88, 112, 400, 424))
              + "</g>")
        return
    d = ("M98,440 C90,250 118,64 256,56 C394,64 422,250 414,440 C404,452 390,452 380,444 "
         "C378,366 372,300 366,244 C360,192 332,168 300,160 Q256,178 212,160 C180,168 152,192 146,244 "
         "C140,300 134,366 132,444 C122,452 108,452 98,440 Z")
    # cloth shadow on the face
    s.add(f'<g clip-path="{s.ref("face")}">' + path("M146,244 C152,192 180,168 212,160 Q256,178 300,160 C332,168 360,192 366,244",
                                                   stroke="#3b1f10", sw=26, op=0.35, extra=blur(s, 8)) + "</g>")
    s.add(path(d, fill, "#00000040", 1.5))
    cp = s.clip("shfront", d)
    s.add(f'<g clip-path="{cp}">'
          + path("M132,444 C134,366 140,300 146,244 C152,192 180,168 212,160 Q256,178 300,160 C332,168 360,192 366,244 C372,300 378,366 380,444",
                 stroke="#000", sw=18, op=0.22, extra=blur(s, 8))
          + "".join(path(f"M{x},{150} C{x-10},{260} {x+8},{360} {x-4},{450}", stroke="#000", sw=12, op=0.14, extra=blur(s, 8)) for x in (112, 400))
          + "".join(path(f"M{x},{170} C{x-6},{260} {x+6},{360} {x},{450}", stroke="#fff", sw=10, op=0.35, extra=blur(s, 6)) for x in (124, 388))
          + ell(210, 100, 90, 40, "#fff", 0.45, blur(s, 12))
          + path("M212,160 Q256,190 300,160", stroke="#000", sw=6, op=0.2, extra=blur(s, 3))
          + "</g>")
    # agal
    ag = "#121215"
    for dy in (0, 30):
        dd = f"M118,{206-dy} C142,{100-dy} 370,{100-dy} 394,{206-dy}"
        s.add(path(dd, stroke="#000", sw=24, op=0.35, extra=blur(s, 3)))
        s.add(path(dd, stroke=ag, sw=19))
        s.add(path(f"M124,{198-dy} C150,{98-dy} 362,{98-dy} 388,{198-dy}", stroke="#5c5c68", sw=4, op=0.9))
        s.add(path(f"M130,{190-dy} C160,{108-dy} 230,{98-dy} 256,{98-dy}", stroke="#9a9aa8", sw=2, op=0.5))


def hijab(s, c, layer):
    col1, col2 = c.get("scarf", ("#2a2a33", "#0d0d12"))
    g = s.lin("hij", [(0, col1, 1), (1, col2, 1)], x1=0, y1=0, x2=0.4, y2=1)
    if layer == "back":
        d = "M256,64 C396,64 436,190 436,320 C436,440 360,506 256,510 C152,506 76,440 76,320 C76,190 116,64 256,64 Z"
        s.add(path(d, g, "#00000060", 1.5))
        return
    s.add(f'<g clip-path="{s.ref("face")}">' + path("M146,250 C146,176 186,128 256,126 C326,128 366,176 366,250",
                                                   stroke="#2a1408", sw=22, op=0.35, extra=blur(s, 8)) + "</g>")
    d = ("M256,66 C392,66 430,190 430,318 C430,438 356,500 256,504 C156,500 82,438 82,318 C82,190 120,66 256,66 Z "
         "M256,124 C334,124 370,178 370,246 C370,320 342,380 308,430 C292,452 274,468 256,470 C238,468 220,452 204,430 "
         "C170,380 142,320 142,246 C142,178 178,124 256,124 Z")
    s.add(path(d, g, "#00000060", 1.5, extra='fill-rule="evenodd"'))
    cp = s.clip("hijf", d.replace(" M256,124", " M256,124"))
    s.add(f'<g clip-path="{cp}">'
          + ell(190, 110, 90, 40, "#ffffff", 0.16, blur(s, 12))
          + "".join(path(dd, stroke="#000", sw=14, op=0.3, extra=blur(s, 8)) for dd in (
              "M110,200 C100,300 110,400 150,470", "M402,200 C412,300 402,400 362,470", "M180,480 C220,496 292,496 332,480"))
          + "".join(path(dd, stroke="#ffffff", sw=8, op=0.12, extra=blur(s, 5)) for dd in (
              "M128,220 C118,300 126,380 160,450", "M156,140 C190,100 260,92 320,110"))
          + "</g>")
    if c.get("scarf_trim"):
        s.add(path("M142,246 C142,178 178,124 256,124 C334,124 370,178 370,246", stroke=c["scarf_trim"], sw=5, op=0.9))


def curly_hair(s, c, rng):
    col = c.get("hair_color", "#1d140f")
    hi = c.get("hair_hi", "#5b3a26")
    base = "M122,250 C108,150 160,70 256,66 C352,70 404,150 390,250 C376,200 350,172 300,168 C270,162 240,164 212,168 C162,174 136,200 122,250 Z"
    s.add(path(base, col, "#00000080", 1.5))
    cg = s.rad("curl", [(0, hi, 1), (0.7, col, 1), (1, "#000", 1)], cx=0.38, cy=0.35, r=0.6)
    pts = []
    for row, (rad, y0, amp) in enumerate(((126, 236, 116), (110, 214, 104), (84, 186, 86), (46, 150, 60))):
        n = 11 - row * 2
        for i in range(n):
            t = i / (n - 1)
            x = 256 - rad + 2 * rad * t
            y = y0 - (1 - (2 * t - 1) ** 2) ** 0.5 * amp + rng.uniform(-4, 4)
            pts.append((x + rng.uniform(-4, 4), y))
    pts += [(206, 172), (236, 166), (272, 168), (304, 174)]
    for x, y in pts:
        r = rng.uniform(16, 21)
        s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{cg}" stroke="#00000066" stroke-width="1.2"/>')
        s.add(path(f"M{x-r*0.5:.1f},{y+r*0.1:.1f} C{x-r*0.4:.1f},{y-r*0.6:.1f} {x+r*0.5:.1f},{y-r*0.6:.1f} {x+r*0.4:.1f},{y+r*0.2:.1f}",
                   stroke=hi, sw=2.2, op=0.7))


# ---------------------------------------------------------------- assemble
def build(c, uid):
    s = SVG(uid)
    rng = random.Random(uid)
    background(s, c)
    head = c.get("head")
    if head == "shemagh":
        shemagh(s, c, "back")
    if head == "hijab":
        hijab(s, c, "back")
    if not head:
        ears(s, c)
    face(s, c)
    beard(s, c, rng)
    if c.get("mouth"):
        mouth(s, c)
    mustache(s, c, rng)
    nose(s, c)
    eyes(s, c)
    brows(s, c)
    if c.get("hair") == "curly":
        curly_hair(s, c, rng)
    if head == "shemagh":
        shemagh(s, c, "front")
    if head == "hijab":
        hijab(s, c, "front")
    glasses(s, c)
    return s.render()


CAST = [
    ("abu-saad", "أبو سعد", dict(skin="tan", head="shemagh", shemagh="red", mustache="thick", beard="goatee",
                                 hair_color="#16100c", facial_hi="#4a3a30", mouth="smile", iris="#6b3412")),
    ("al-shaiba", "الشيبة", dict(skin="fair", head="shemagh", shemagh="white", old=True, beard="full", mustache="walrus",
                                 facial_color="#d9d9d9", facial_hi="#ffffff", brow_color="#cfcfcf", brow_hi="#f4f4f4",
                                 strand_cols=["#ffffff", "#bdbdbd", "#9a9a9a"], glasses="round",
                                 sleepy=True, nose_s=1.08)),
    ("umm-saad", "أم سعد", dict(skin="fair", head="hijab", female=True, mouth="lips", lip="#c2475a", brow_w=10,
                                 nose_s=0.86, blush=0.3, iris="#5a2e10", scarf=("#2b2b34", "#0b0b10"))),
    ("salem", "سالم", dict(skin="brown", hair="curly", hair_color="#120c09", hair_hi="#4a3020", stubble=True,
                           mouth="grin", iris="#4a2208", brow_lift=4, look=1)),
]


def main():
    out = os.path.join(ROOT, "v2", "svg")
    os.makedirs(out, exist_ok=True)
    for i, (slug, name, cfg) in enumerate(CAST, 1):
        with open(os.path.join(out, f"{i:02d}-{slug}.svg"), "w") as f:
            f.write(build(cfg, f"c{i}"))
    print("ok", len(CAST))


if __name__ == "__main__":
    main()
