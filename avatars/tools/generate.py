#!/usr/bin/env python3
"""Generate 40 original cartoon avatars (Gulf style) as clean vector SVGs.

Usage: python3 avatars/tools/generate.py
Outputs: avatars/svg/*.svg (with card background) and avatars/svg-transparent/*.svg
"""
import os

OUT = "#1f1f24"
SW = 5
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKINS = {
    "light": ("#f6d2b0", "#e8b48d"),
    "fair": ("#f1c39c", "#dca27a"),
    "medium": ("#e0a878", "#c88a5c"),
    "tan": ("#c98f5f", "#ad7446"),
    "brown": ("#a86e45", "#8c5634"),
    "dark": ("#7d4f31", "#643b22"),
}

BGS = {
    "blue": ("#4fb3ff", "#1f78e0"),
    "teal": ("#3fd6c0", "#1c9c95"),
    "purple": ("#a985ff", "#6a43d8"),
    "orange": ("#ffb44f", "#f07a1f"),
    "pink": ("#ff8fb8", "#e04a86"),
    "green": ("#7ddc6a", "#2f9e4a"),
    "red": ("#ff7a6b", "#d63a35"),
    "navy": ("#5f7bd6", "#2d3f99"),
    "gold": ("#ffd75a", "#e0a311"),
    "gray": ("#9fb0c4", "#5f7189"),
}


def P(d, fill, stroke=OUT, sw=SW, extra=""):
    s = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else 'stroke="none"'
    return f'<path d="{d}" fill="{fill}" {s} stroke-linejoin="round" stroke-linecap="round" {extra}/>'


def line(d, color=OUT, sw=SW, extra=""):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def mirror(x):
    return 512 - x


# ------------------------------------------------------------------ geometry
def face_path(w, top=118, bottom=398, jaw=0.62):
    cx = 256
    return (f"M{cx},{top} C{cx+w*0.7},{top} {cx+w},{top+58} {cx+w},{top+140} "
            f"C{cx+w},{top+205} {cx+w*jaw+18},{bottom-28} {cx},{bottom} "
            f"C{cx-w*jaw-18},{bottom-28} {cx-w},{top+205} {cx-w},{top+140} "
            f"C{cx-w},{top+58} {cx-w*0.7},{top} {cx},{top} Z")


# ------------------------------------------------------------------ parts
def defs(c, uid):
    s1, s2 = SKINS[c["skin"]]
    b1, b2 = BGS[c["bg"]]
    pc = c.get("pattern_color", "#d42b2b")
    return f"""<defs>
<linearGradient id="bg{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{b1}"/><stop offset="1" stop-color="{b2}"/></linearGradient>
<radialGradient id="glow{uid}" cx="0.5" cy="0.35" r="0.6"><stop offset="0" stop-color="#fff" stop-opacity="0.45"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<radialGradient id="skin{uid}" cx="0.45" cy="0.38" r="0.7"><stop offset="0" stop-color="{s1}"/><stop offset="0.75" stop-color="{s1}"/><stop offset="1" stop-color="{s2}"/></radialGradient>
<pattern id="shm{uid}" width="26" height="26" patternUnits="userSpaceOnUse" patternTransform="rotate(45 256 256)">
<rect width="26" height="26" fill="#fbfbfb"/><rect x="2" y="2" width="9" height="9" fill="{pc}"/><rect x="15" y="15" width="9" height="9" fill="{pc}"/>
<rect x="15" y="4" width="5" height="5" fill="{pc}" opacity="0.55"/><rect x="4" y="15" width="5" height="5" fill="{pc}" opacity="0.55"/></pattern>
<pattern id="knit{uid}" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" fill="#ffffff"/><circle cx="7" cy="7" r="2.6" fill="#d9dde3"/></pattern>
<pattern id="kumma{uid}" width="30" height="30" patternUnits="userSpaceOnUse"><rect width="30" height="30" fill="#f7f3e8"/>
<path d="M15 3 L27 15 L15 27 L3 15 Z" fill="none" stroke="{c.get('kumma_color', '#1d7a5f')}" stroke-width="3"/><circle cx="15" cy="15" r="3.5" fill="#d6372f"/></pattern>
<linearGradient id="lens{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c.get('lens1', '#2b2b33')}"/><stop offset="1" stop-color="{c.get('lens2', '#5d6170')}"/></linearGradient>
<linearGradient id="rainbow{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#29d39a"/><stop offset="0.5" stop-color="#3b8cff"/><stop offset="1" stop-color="#b84dff"/></linearGradient>
</defs>"""


def background(c, uid):
    return (f'<rect x="8" y="8" width="496" height="496" rx="64" fill="url(#bg{uid})"/>'
            f'<rect x="8" y="8" width="496" height="496" rx="64" fill="url(#glow{uid})"/>'
            f'<rect x="14" y="14" width="484" height="484" rx="58" fill="none" stroke="#ffffff" stroke-opacity="0.55" stroke-width="6"/>')


def body(c, uid):
    kind = c.get("body", "thobe")
    col = c.get("body_color", "#ffffff")
    shoulders = "M30,520 C36,455 96,418 176,404 L336,404 C416,418 476,455 482,520 Z"
    out = []
    if kind == "thobe":
        out.append(P(shoulders, "#fdfdfd"))
        out.append(line("M150,440 C170,470 176,500 178,520", "#d9dde3", 4))
        out.append(line("M362,440 C342,470 336,500 334,520", "#d9dde3", 4))
    elif kind == "bisht":
        trim = c.get("trim", "#e8b931")
        out.append(P(shoulders, col))
        out.append(P("M200,404 L312,404 L300,520 L212,520 Z", "#fdfdfd"))
        out.append(P("M188,404 L212,404 L222,520 L196,520 Z", trim, sw=3))
        out.append(P("M324,404 L300,404 L290,520 L316,520 Z", trim, sw=3))
    elif kind == "tshirt":
        out.append(P(shoulders, col))
        out.append(line("M60,520 C70,480 90,455 110,445", "#000", 4, 'opacity="0.18"'))
        out.append(line("M452,520 C442,480 422,455 402,445", "#000", 4, 'opacity="0.18"'))
    elif kind == "shirt":
        out.append(P(shoulders, col))
        out.append(P("M205,404 L256,450 L222,470 Z", col))
        out.append(P("M307,404 L256,450 L290,470 Z", col))
        out.append(line("M256,450 L256,520", OUT, 4))
        for y in (475, 505):
            out.append(f'<circle cx="266" cy="{y}" r="4" fill="{OUT}"/>')
    elif kind == "suit":
        tie = c.get("tie", "#d63a35")
        out.append(P(shoulders, col))
        out.append(P("M206,404 L306,404 L284,520 L228,520 Z", "#ffffff"))
        out.append(P("M244,428 L268,428 L264,446 L276,510 L256,520 L236,510 L248,446 Z", tie, sw=4))
        out.append(P("M200,404 L246,430 L232,470 L214,520 L190,520 Z", col))
        out.append(P("M312,404 L266,430 L280,470 L298,520 L322,520 Z", col))
    elif kind == "hoodie":
        out.append(P(shoulders, col))
        out.append(P("M150,420 C170,470 342,470 362,420 C330,445 182,445 150,420 Z", col))
        out.append(line("M232,450 L228,505", "#ffffff", 5))
        out.append(line("M280,450 L284,505", "#ffffff", 5))
    elif kind == "abaya":
        out.append(P(shoulders, "#1c1c22"))
        out.append(line("M256,440 L256,520", "#3a3a44", 4))
        if c.get("trim"):
            out.append(P("M240,430 L272,430 L268,520 L244,520 Z", c["trim"], sw=3))
    elif kind == "jersey":
        stripe = c.get("stripe", "#ffffff")
        out.append(P(shoulders, col))
        out.append(f'<path d="M30,520 C36,455 96,418 176,404 L196,404 C150,430 110,470 100,520 Z" fill="{stripe}" opacity="0.9"/>')
        out.append(f'<path d="M482,520 C476,455 416,418 336,404 L316,404 C362,430 402,470 412,520 Z" fill="{stripe}" opacity="0.9"/>')
        out.append(P(shoulders, "none"))
        num = c.get("number", "10")
        out.append(f'<text x="256" y="508" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="54" text-anchor="middle" fill="{stripe}" stroke="{OUT}" stroke-width="3">{num}</text>')
    return "".join(out)


def neck(c, uid):
    s1, s2 = SKINS[c["skin"]]
    out = [P("M214,320 L214,412 Q256,440 298,412 L298,320 Z", f"url(#skin{uid})")]
    out.append(f'<path d="M214,350 Q256,395 298,350 L298,330 L214,330 Z" fill="{s2}" opacity="0.8"/>')
    kind = c.get("body", "thobe")
    if kind in ("thobe", "bisht"):
        out.append(P("M200,402 Q256,444 312,402 L318,420 Q256,466 194,420 Z", "#fdfdfd", sw=4))
        out.append(line("M256,450 L256,520", "#c9ced6", 4))
        out.append(f'<circle cx="256" cy="470" r="5" fill="#c9a227" stroke="{OUT}" stroke-width="2"/>')
    elif kind in ("tshirt", "jersey"):
        col = c.get("body_color", "#fff")
        out.append(P("M198,404 Q256,456 314,404 L322,416 Q256,474 190,416 Z", col, sw=4))
    elif kind == "hoodie":
        pass
    return "".join(out)


def ears(c, uid):
    w = c.get("w", 108)
    s1, s2 = SKINS[c["skin"]]
    out = []
    for side in (-1, 1):
        x = 256 + side * (w - 4)
        out.append(f'<ellipse cx="{x}" cy="262" rx="22" ry="32" fill="{s1}" stroke="{OUT}" stroke-width="{SW}"/>')
        out.append(line(f"M{x + side*-2},248 C{x+side*10},252 {x+side*10},272 {x+side*-2},278", s2, 5))
    if c.get("earrings"):
        for side in (-1, 1):
            x = 256 + side * (w - 4)
            out.append(f'<circle cx="{x}" cy="300" r="9" fill="{c["earrings"]}" stroke="{OUT}" stroke-width="3"/>')
    return "".join(out)


def face(c, uid):
    w = c.get("w", 108)
    s1, s2 = SKINS[c["skin"]]
    out = [P(face_path(w, jaw=c.get("jaw", 0.62)), f"url(#skin{uid})")]
    blush = c.get("blush", 0.22)
    if blush:
        for side in (-1, 1):
            out.append(f'<ellipse cx="{256+side*62}" cy="300" rx="24" ry="13" fill="#ff6b6b" opacity="{blush}"/>')
    if c.get("wrinkles"):
        out.append(line("M218,168 Q256,158 294,168", s2, 4))
        out.append(line("M228,184 Q256,176 284,184", s2, 4))
        for side in (-1, 1):
            x = 256 + side * 82
            out.append(line(f"M{x},236 L{x+side*14},230", s2, 3))
            out.append(line(f"M{x},246 L{x+side*14},248", s2, 3))
        out.append(line("M206,308 Q200,330 210,350", s2, 4))
        out.append(line("M306,308 Q312,330 302,350", s2, 4))
    if c.get("mole"):
        out.append(f'<circle cx="300" cy="320" r="5" fill="#5a3a26"/>')
    if c.get("freckles"):
        for x, y in [(200, 290), (212, 300), (190, 302), (312, 290), (300, 300), (322, 302)]:
            out.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{s2}"/>')
    if c.get("scar"):
        out.append(line("M318,200 L334,240", "#b5564a", 4))
        out.append(line("M320,214 L330,210 M325,226 L335,222", "#b5564a", 3))
    return "".join(out)


def eyes(c, uid):
    kind = c.get("eyes", "normal")
    sp = c.get("eye_sp", 46)
    y = c.get("eye_y", 240)
    ec = c.get("eye_color", "#4a2c17")
    s1, s2 = SKINS[c["skin"]]
    out = []
    for side in (-1, 1):
        x = 256 + side * sp
        if kind == "happy":
            out.append(line(f"M{x-22},{y+6} Q{x},{y-20} {x+22},{y+6}", OUT, 6))
            continue
        rx, ry = (24, 28) if kind != "small" else (17, 20)
        out.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#ffffff" stroke="{OUT}" stroke-width="{SW-1}"/>')
        look = c.get("look", 0)
        px = x + look * 6
        pr = 12 if kind != "small" else 9
        out.append(f'<circle cx="{px}" cy="{y+4}" r="{pr}" fill="{ec}"/>')
        out.append(f'<circle cx="{px}" cy="{y+4}" r="{pr*0.5}" fill="#111"/>')
        out.append(f'<circle cx="{px-4}" cy="{y-1}" r="{pr*0.33}" fill="#fff"/>')
        if kind in ("sleepy", "old"):
            lid = f"M{x-rx-2},{y} C{x-rx},{y-ry-6} {x+rx},{y-ry-6} {x+rx+2},{y} Z"
            out.append(P(lid, s1, sw=SW - 1))
        if kind == "wink" and side == 1:
            out[-4:] = [line(f"M{x-22},{y+2} Q{x},{y+14} {x+22},{y+2}", OUT, 6)]
        if c.get("lashes"):
            for k in range(3):
                lx = x + side * (10 + k * 7)
                out.append(line(f"M{lx},{y-ry+4+k*4} L{lx+side*10},{y-ry-6+k*6}", OUT, 4))
            out.append(line(f"M{x-rx},{y-6} Q{x},{y-ry-8} {x+rx},{y-6}", OUT, 6))
    return "".join(out)


def brows(c, uid):
    kind = c.get("brows", "thick")
    col = c.get("brow_color", c.get("hair_color", "#2a1d16"))
    y = c.get("eye_y", 240) - 44
    sp = c.get("eye_sp", 46)
    out = []
    for side in (-1, 1):
        x = 256 + side * sp
        if kind == "thick":
            d = (f"M{x-side*28},{y+8} C{x-side*16},{y-8} {x+side*14},{y-10} {x+side*30},{y+2} "
                 f"C{x+side*18},{y+2} {x-side*14},{y+4} {x-side*28},{y+16} Z")
            out.append(P(d, col, sw=3))
        elif kind == "angry":
            d = f"M{x-side*30},{y+16} L{x+side*28},{y-4} L{x+side*26},{y+8} L{x-side*28},{y+26} Z"
            out.append(P(d, col, sw=3))
        elif kind == "raised":
            out.append(line(f"M{x-24},{y+2} Q{x},{y-18} {x+24},{y+2}", col, 9))
        elif kind == "thin":
            out.append(line(f"M{x-24},{y+6} Q{x},{y-8} {x+24},{y+4}", col, 6))
        elif kind == "bushy":
            d = (f"M{x-side*32},{y+14} C{x-side*20},{y-14} {x+side*20},{y-16} {x+side*34},{y+4} "
                 f"L{x+side*26},{y+10} L{x+side*18},{y+4} L{x+side*8},{y+10} L{x-side*4},{y+6} L{x-side*16},{y+14} Z")
            out.append(P(d, col, sw=3))
    return "".join(out)


def nose(c, uid):
    kind = c.get("nose", "bulb")
    s = c.get("nose_s", 1.0)
    s1, s2 = SKINS[c["skin"]]
    if kind == "bulb":
        d = "M246,250 C240,282 214,292 220,316 C226,336 286,336 292,316 C298,292 272,282 266,250"
    elif kind == "long":
        d = "M248,236 C246,276 224,300 228,320 C234,336 280,336 286,320 C290,304 270,290 266,236"
    elif kind == "small":
        d = "M250,272 C244,292 232,300 238,314 C244,324 270,324 276,314 C280,300 266,292 262,272"
    else:  # hook
        d = "M250,236 C254,270 222,296 226,318 C232,334 282,334 288,320 C292,306 274,300 266,240"
    g = [P(d, f"url(#skin{uid})", sw=SW - 0.5)]
    g.append(f'<ellipse cx="240" cy="310" rx="6" ry="4" fill="{s2}"/><ellipse cx="272" cy="310" rx="6" ry="4" fill="{s2}"/>')
    g.append(f'<ellipse cx="248" cy="292" rx="7" ry="5" fill="#fff" opacity="0.35"/>')
    return f'<g transform="translate(256 300) scale({s}) translate(-256 -300)">{"".join(g)}</g>'


def mouth(c, uid):
    kind = c.get("mouth", "smile")
    y = c.get("mouth_y", 352)
    lip = c.get("lips")
    out = []
    if kind == "smile":
        out.append(line(f"M222,{y-4} Q256,{y+22} 290,{y-4}", OUT, 6))
        out.append(line(f"M216,{y-8} L224,{y}", OUT, 4))
        out.append(line(f"M296,{y-8} L288,{y}", OUT, 4))
    elif kind == "grin":
        out.append(P(f"M214,{y-8} Q256,{y-2} 298,{y-8} Q290,{y+34} 256,{y+36} Q222,{y+34} 214,{y-8} Z", "#7a1f25"))
        out.append(f'<path d="M220,{y-5} Q256,{y+1} 292,{y-5} L290,{y+8} Q256,{y+12} 222,{y+8} Z" fill="#fff"/>')
        out.append(f'<ellipse cx="256" cy="{y+24}" rx="18" ry="8" fill="#e5636b"/>')
        out.append(P(f"M214,{y-8} Q256,{y-2} 298,{y-8} Q290,{y+34} 256,{y+36} Q222,{y+34} 214,{y-8} Z", "none"))
        if c.get("gold_tooth"):
            out.append(f'<rect x="268" y="{y-4}" width="12" height="11" fill="#f2c230"/>')
    elif kind == "open":
        out.append(P(f"M232,{y} Q256,{y-10} 280,{y} Q284,{y+30} 256,{y+32} Q228,{y+30} 232,{y} Z", "#7a1f25"))
        out.append(f'<ellipse cx="256" cy="{y+22}" rx="13" ry="7" fill="#e5636b"/>')
    elif kind == "smirk":
        out.append(line(f"M226,{y+4} Q262,{y+12} 292,{y-8}", OUT, 6))
    elif kind == "neutral":
        out.append(line(f"M232,{y+2} Q256,{y+6} 280,{y+2}", OUT, 6))
    elif kind == "frown":
        out.append(line(f"M228,{y+10} Q256,{y-6} 284,{y+10}", OUT, 6))
    elif kind == "lips":
        col = lip or "#d8455f"
        out.append(P(f"M224,{y} C236,{y-12} 250,{y-10} 256,{y-4} C262,{y-10} 276,{y-12} 288,{y} C276,{y+20} 236,{y+20} 224,{y} Z", col, sw=4))
        out.append(line(f"M226,{y} Q256,{y+6} 286,{y}", "#7a1f35", 3))
        out.append(f'<ellipse cx="266" cy="{y+9}" rx="7" ry="3" fill="#fff" opacity="0.5"/>')
    elif kind == "lips_smile":
        col = lip or "#d8455f"
        out.append(P(f"M218,{y-6} Q256,{y+2} 294,{y-6} Q284,{y+26} 256,{y+28} Q228,{y+26} 218,{y-6} Z", col, sw=4))
        out.append(f'<path d="M224,{y-3} Q256,{y+4} 288,{y-3} L286,{y+8} Q256,{y+13} 226,{y+8} Z" fill="#fff"/>')
    return "".join(out)


def mustache(c, uid):
    kind = c.get("mustache")
    if not kind:
        return ""
    col = c.get("facial_color", c.get("hair_color", "#2a1d16"))
    if kind == "thick":
        d = "M256,326 C236,316 204,320 194,348 C214,346 236,344 256,338 C276,344 298,346 318,348 C308,320 276,316 256,326 Z"
    elif kind == "handlebar":
        d = ("M256,326 C236,314 210,320 200,338 C192,350 176,350 172,338 C168,358 196,366 214,350 "
             "C230,344 244,342 256,338 C268,342 282,344 298,350 C316,366 344,358 340,338 C336,350 320,350 312,338 C302,320 276,314 256,326 Z")
    elif kind == "walrus":
        d = "M256,322 C228,312 196,318 186,352 C196,372 214,362 224,370 C236,360 246,362 256,354 C266,362 276,360 288,370 C298,362 316,372 326,352 C316,318 284,312 256,322 Z"
    elif kind == "pencil":
        d = "M256,330 C240,326 222,330 212,340 C230,338 244,338 256,336 C268,338 282,338 300,340 C290,330 272,326 256,330 Z"
    elif kind == "chevron":
        d = "M256,324 C234,316 210,322 204,346 L220,342 L230,348 L242,340 L256,346 L270,340 L282,348 L292,342 L308,346 C302,322 278,316 256,324 Z"
    else:
        return ""
    return P(d, col, sw=4)


def beard(c, uid):
    kind = c.get("beard")
    if not kind:
        return ""
    col = c.get("facial_color", c.get("hair_color", "#2a1d16"))
    w = c.get("w", 108)
    L, R = 256 - w, 256 + w
    if kind == "full":
        d = (f"M{L},250 C{L-2},340 {L+40},420 256,432 C{R-40},420 {R+2},340 {R},250 "
             f"C{R-14},300 {R-30},322 300,330 C290,326 276,318 256,320 C236,318 222,326 212,330 C{L+30},322 {L+14},300 {L},250 Z")
        return P(d, col)
    if kind == "short":
        d = (f"M{L+2},262 C{L+4},340 {L+46},404 256,410 C{R-46},404 {R-4},340 {R-2},262 "
             f"C{R-12},320 {R-34},372 296,376 C280,368 270,376 256,376 C242,376 232,368 216,376 C{L+34},372 {L+12},320 {L+2},262 Z")
        return P(d, col)
    if kind == "goatee":
        d = "M222,372 C226,400 240,420 256,424 C272,420 286,400 290,372 C278,384 268,380 256,380 C244,380 234,384 222,372 Z"
        return P(d, col, sw=4)
    if kind == "stubble":
        d = (f"M{L+4},270 C{L+6},350 {L+46},398 256,400 C{R-46},398 {R-6},350 {R-4},270 "
             f"C{R-20},320 {R-30},330 290,326 C276,320 266,318 256,318 C246,318 236,320 222,326 C{L+30},330 {L+20},320 {L+4},270 Z")
        return f'<path d="{d}" fill="{col}" opacity="0.28"/>'
    if kind == "long":
        d = (f"M{L},250 C{L-6},360 {L+30},470 256,486 C{R-30},470 {R+6},360 {R},250 "
             f"C{R-14},300 {R-30},322 300,330 C290,326 276,318 256,320 C236,318 222,326 212,330 C{L+30},322 {L+14},300 {L},250 Z")
        return P(d, col) + line("M236,420 Q246,450 240,470 M276,420 Q266,450 272,470", "#000", 3, 'opacity="0.2"')
    return ""


def glasses(c, uid):
    kind = c.get("glasses")
    if not kind:
        return ""
    sp = c.get("eye_sp", 46)
    y = c.get("eye_y", 240)
    fc = c.get("frame_color", OUT)
    out = []
    w = c.get("w", 108)
    if kind == "round":
        for side in (-1, 1):
            out.append(f'<circle cx="{256+side*sp}" cy="{y}" r="34" fill="#cfe8ff" fill-opacity="0.25" stroke="{fc}" stroke-width="7"/>')
    elif kind == "square":
        for side in (-1, 1):
            x = 256 + side * sp
            out.append(f'<rect x="{x-38}" y="{y-30}" width="76" height="60" rx="14" fill="#cfe8ff" fill-opacity="0.22" stroke="{fc}" stroke-width="9"/>')
    elif kind == "sun":
        for side in (-1, 1):
            x = 256 + side * sp
            out.append(P(f"M{x-40},{y-26} L{x+40},{y-26} C{x+42},{y+14} {x+28},{y+32} {x},{y+32} C{x-28},{y+32} {x-42},{y+14} {x-40},{y-26} Z", f"url(#lens{uid})", fc, 6))
            out.append(line(f"M{x-24},{y-14} L{x-6},{y-14}", "#fff", 5, 'opacity="0.5"'))
    elif kind == "aviator":
        for side in (-1, 1):
            x = 256 + side * sp
            out.append(P(f"M{x-36},{y-24} C{x-10},{y-30} {x+20},{y-30} {x+38},{y-22} C{x+40},{y+10} {x+24},{y+34} {x},{y+32} C{x-30},{y+30} {x-40},{y+4} {x-36},{y-24} Z", f"url(#lens{uid})", fc, 5))
            out.append(line(f"M{x-20},{y-12} L{x-4},{y-14}", "#fff", 5, 'opacity="0.5"'))
        out.append(line(f"M{256-sp+36},{y-26} L{256+sp-36},{y-26}", fc, 5))
    out.append(line(f"M{256-sp+34},{y-6} Q256,{y-16} {256+sp-34},{y-6}", fc, 6))
    out.append(line(f"M{256-sp-36},{y-8} L{256-w+2},{y-14}", fc, 6))
    out.append(line(f"M{256+sp+36},{y-8} L{256+w-2},{y-14}", fc, 6))
    return "".join(out)


# ------------------------------------------------------------------ hair & headwear
def hair_back(c, uid):
    kind = c.get("hair")
    col = c.get("hair_color", "#2a1d16")
    if kind == "long":
        return P("M256,96 C380,96 404,200 400,300 C398,380 420,440 440,470 C380,490 320,470 300,440 L212,440 C192,470 132,490 72,470 C92,440 114,380 112,300 C108,200 132,96 256,96 Z", col)
    if kind == "afro":
        return P("M256,62 C340,52 410,100 418,170 C440,210 420,270 392,300 L120,300 C92,270 72,210 94,170 C102,100 172,52 256,62 Z", col)
    if kind == "bun":
        return P("M256,40 C290,40 304,62 302,84 C300,104 280,114 256,114 C232,114 212,104 210,84 C208,62 222,40 256,40 Z", col)
    if kind == "ponytail":
        return P("M330,150 C410,170 420,260 400,340 C390,380 410,410 420,430 C370,420 350,380 356,330 C362,280 350,220 320,190 Z", col)
    return ""


def hair_front(c, uid):
    kind = c.get("hair")
    col = c.get("hair_color", "#2a1d16")
    fill = f"url(#rainbow{uid})" if col == "rainbow" else col
    w = c.get("w", 108)
    L, R = 256 - w, 256 + w
    if kind == "short":
        return P(f"M{L-2},250 C{L-14},150 {L+40},100 256,100 C{R-40},100 {R+14},150 {R+2},250 C{R-8},200 {R-20},170 {R-50},162 C{R-90},150 300,168 256,160 C212,168 {L+90},150 {L+50},162 C{L+20},170 {L+8},200 {L-2},250 Z", fill)
    if kind == "quiff":
        return P(f"M{L-2},250 C{L-14},150 {L+30},92 230,86 C270,60 340,66 356,104 C{R+10},140 {R+12},190 {R+2},250 C{R-8},200 {R-24},166 {R-60},162 C300,150 270,176 230,166 C200,160 {L+40},170 {L+20},190 C{L+10},205 {L+2},228 {L-2},250 Z", fill)
    if kind == "curly":
        pts = [(L+4, 196), (L+16, 152), (L+44, 122), (214, 104), (256, 98), (298, 104), (R-44, 122), (R-16, 152), (R-4, 196)]
        circles = "".join(f'<circle cx="{x}" cy="{y}" r="30" fill="{fill}" stroke="{OUT}" stroke-width="{SW}"/>' for x, y in pts)
        inner = "".join(f'<circle cx="{x}" cy="{y+18}" r="26" fill="{fill}"/>' for x, y in pts[2:-2])
        swirls = "".join(line(f"M{x-10},{y} q10,-12 18,2", "#000", 3, 'opacity="0.25"') for x, y in pts)
        return circles + inner + swirls
    if kind == "spiky":
        d = f"M{L-2},250 L{L-12},160 L{L+26},170 L{L+30},110 L{L+70},140 L230,84 L262,130 L300,80 L314,134 L{R-26},102 L{R-26},158 L{R+14},150 L{R+2},250 C{R-10},200 {R-30},176 256,168 C{L+30},176 {L+10},200 {L-2},250 Z"
        return P(d, fill)
    if kind == "bald":
        out = []
        for side in (-1, 1):
            x = 256 + side * w
            out.append(P(f"M{x},{200} C{x+side*12},214 {x+side*12},248 {x+side*2},262 C{x-side*10},240 {x-side*12},216 {x},{200} Z", fill, sw=4))
        out.append(f'<ellipse cx="226" cy="146" rx="26" ry="12" fill="#fff" opacity="0.35"/>')
        return "".join(out)
    if kind == "receding":
        out = [hair_front({**c, "hair": "bald"}, uid)]
        out.append(line("M240,124 q8,-22 22,-8 M258,122 q10,-20 22,-4", col, 5))
        return "".join(out)
    if kind == "buzz":
        return f'<path d="M{L+2},236 C{L-6},150 {L+40},112 256,112 C{R-40},112 {R+6},150 {R-2},236 C{R-16},196 {R-40},176 256,172 C{L+40},176 {L+16},196 {L+2},236 Z" fill="{fill}" opacity="0.85"/>'
    if kind in ("long", "bun", "ponytail"):
        d = f"M{L-6},300 C{L-20},160 {L+30},96 256,96 C{R-30},96 {R+20},160 {R+6},300 C{R-10},240 {R-14},190 {R-60},170 C{R-90},158 290,180 262,150 C240,182 200,170 {L+40},186 C{L+12},204 {L+8},250 {L-6},300 Z"
        return P(d, fill)
    if kind == "afro":
        return P(f"M{L-4},240 C{L-10},190 {L+20},150 256,146 C{R-20},150 {R+10},190 {R+4},240 C{R-10},200 300,186 256,186 C212,186 {L+10},200 {L-4},240 Z", fill)
    return ""


def headwear(c, uid, layer):
    kind = c.get("head")
    if not kind:
        return ""
    if kind in ("shemagh", "ghutra"):
        fill = f"url(#shm{uid})" if kind == "shemagh" else "#ffffff"
        if layer == "back":
            d = "M256,84 C366,84 404,170 406,262 L420,474 C388,488 330,478 306,452 L206,452 C182,478 124,488 92,474 L106,262 C108,170 146,84 256,84 Z"
            out = [P(d, fill)]
            out.append(line("M130,320 C126,380 120,430 112,470", "#000", 4, 'opacity="0.12"'))
            out.append(line("M382,320 C386,380 392,430 400,470", "#000", 4, 'opacity="0.12"'))
            return "".join(out)
        if layer == "front":
            d = ("M104,470 L112,300 C108,170 168,94 256,92 C344,94 404,170 400,300 L408,470 "
                 "C394,476 380,474 370,468 C368,420 362,360 362,300 C366,244 348,186 300,172 Q256,186 212,172 "
                 "C164,186 146,244 150,300 C150,360 144,420 142,468 C132,474 118,476 104,470 Z")
            out = [P(d, fill)]
            out.append(line("M212,172 Q256,196 300,172", "#000", 4, 'opacity="0.15"'))
            out.append(line("M170,140 C200,128 230,124 256,124", "#000", 3, 'opacity="0.12"'))
            if c.get("agal", True):
                out.append(line("M130,206 C150,120 362,120 382,206", "#17171b", 16))
                out.append(line("M138,182 C160,108 352,108 374,182", "#17171b", 14))
                out.append(line("M150,196 C176,134 336,134 362,196", "#55555f", 3))
                out.append(line("M156,170 C180,118 332,118 356,170", "#55555f", 3))
            return "".join(out)
    if kind == "taqiyah" and layer == "front":
        col = c.get("cap_color")
        fill = col if col else f"url(#knit{uid})"
        return P("M146,206 C146,120 196,92 256,92 C316,92 366,120 366,206 C320,184 192,184 146,206 Z", fill) + \
            line("M150,196 C200,176 312,176 362,196", "#c8ced8", 4)
    if kind == "kumma" and layer == "front":
        return P("M144,200 C140,110 196,84 256,84 C316,84 372,110 368,200 C320,182 192,182 144,200 Z", f"url(#kumma{uid})") + \
            P("M144,200 C192,182 320,182 368,200 L366,214 C318,196 194,196 146,214 Z", c.get("kumma_color", "#1d7a5f"), sw=4)
    if kind in ("hijab", "niqab"):
        col = c.get("scarf_color", "#1c1c22")
        if layer == "back":
            return P("M256,82 C376,82 410,190 412,300 C414,380 440,440 460,520 L52,520 C72,440 98,380 100,300 C102,190 136,82 256,82 Z", col)
        if layer == "front":
            d = ("M256,80 C372,80 404,180 404,290 C404,384 360,446 256,456 C152,446 108,384 108,290 C108,180 140,80 256,80 Z "
                 "M256,142 C322,142 350,190 350,256 C350,332 314,384 256,388 C198,384 162,332 162,256 C162,190 190,142 256,142 Z")
            out = [P(d, col, extra='fill-rule="evenodd"')]
            out.append(line("M150,170 C190,120 322,120 362,170", "#ffffff", 4, 'opacity="0.18"'))
            if c.get("scarf_trim"):
                out.append(line("M162,256 C162,190 190,142 256,142 C322,142 350,190 350,256", c["scarf_trim"], 6))
            if kind == "niqab":
                out.append(P("M150,268 C190,276 322,276 362,268 C364,360 330,412 256,420 C182,412 148,360 150,268 Z", col))
                out.append(line("M170,300 C220,312 292,312 342,300", "#ffffff", 3, 'opacity="0.12"'))
            return "".join(out)
    if kind == "fedora" and layer == "front":
        col = c.get("hat_color", "#c8322d")
        return (P("M96,176 C120,150 392,150 416,176 C426,196 350,200 256,198 C162,200 86,196 96,176 Z", col)
                + P("M160,170 C150,90 190,60 256,70 C322,60 362,90 352,170 C320,178 192,178 160,170 Z", col)
                + P("M160,152 C200,162 312,162 352,152 L352,172 C312,180 200,180 160,172 Z", "#1c1c22", sw=4)
                + line("M226,76 Q256,96 286,76", "#000", 4, 'opacity="0.25"'))
    if kind == "cap" and layer == "front":
        col = c.get("hat_color", "#2d6be0")
        return (P("M144,200 C136,110 196,80 256,80 C316,80 376,110 368,200 C320,182 192,182 144,200 Z", col)
                + P("M150,196 C200,180 330,176 420,206 C400,226 330,214 256,206 C210,204 170,206 150,196 Z", col)
                + f'<circle cx="256" cy="84" r="9" fill="{col}" stroke="{OUT}" stroke-width="4"/>'
                + line("M256,86 L256,184", "#000", 3, 'opacity="0.2"')
                + f'<circle cx="256" cy="150" r="18" fill="#fff" stroke="{OUT}" stroke-width="3"/>')
    if kind == "beanie" and layer == "front":
        col = c.get("hat_color", "#e2532d")
        stripes = "".join(line(f"M{x},112 L{x},196", "#000", 4, 'opacity="0.15"') for x in range(176, 340, 20))
        return (P("M142,214 C130,110 190,74 256,74 C322,74 382,110 370,214 Z", col) + stripes
                + P("M136,196 C200,182 312,182 376,196 L378,232 C312,218 200,218 134,232 Z", col)
                + f'<circle cx="256" cy="64" r="22" fill="{col}" stroke="{OUT}" stroke-width="{SW}"/>')
    if kind == "headphones" and layer == "front":
        col = c.get("hat_color", "#22232b")
        w = c.get("w", 108)
        out = [line(f"M{256-w-10},250 C{256-w-20},90 {256+w+20},90 {256+w+10},250", col, 18)]
        for side in (-1, 1):
            x = 256 + side * (w + 6)
            out.append(f'<rect x="{x-22}" y="226" width="44" height="74" rx="20" fill="{col}" stroke="{OUT}" stroke-width="{SW}"/>')
            out.append(f'<rect x="{x-10}" y="240" width="20" height="46" rx="10" fill="{c.get("accent", "#3fe0ff")}"/>')
        return "".join(out)
    if kind == "crown" and layer == "front":
        return (P("M162,170 L176,96 L216,134 L256,78 L296,134 L336,96 L350,170 Z", "#f6c533")
                + "".join(f'<circle cx="{x}" cy="{y}" r="8" fill="{col}" stroke="{OUT}" stroke-width="3"/>' for x, y, col in [(176, 96, "#e83b5a"), (256, 78, "#3fb4ff"), (336, 96, "#5bd16b")]))
    return ""


# ------------------------------------------------------------------ assemble
def avatar(c, uid, with_bg=True):
    parts = [defs(c, uid)]
    if with_bg:
        parts.append(background(c, uid))
    parts.append(hair_back(c, uid))
    parts.append(headwear(c, uid, "back") if c.get("head") in ("hijab", "niqab") else "")
    parts.append(body(c, uid))
    if c.get("head") in ("shemagh", "ghutra"):
        parts.append(headwear(c, uid, "back"))
    parts.append(neck(c, uid))
    if c.get("head") not in ("shemagh", "ghutra", "hijab", "niqab"):
        parts.append(ears(c, uid))
    parts.append(face(c, uid))
    parts.append(beard(c, uid))
    if c.get("head") != "niqab":
        parts.append(mouth(c, uid))
        parts.append(mustache(c, uid))
        parts.append(nose(c, uid))
    parts.append(eyes(c, uid))
    parts.append(brows(c, uid))
    parts.append(hair_front(c, uid))
    parts.append(headwear(c, uid, "front"))
    parts.append(glasses(c, uid))
    clip = f'<clipPath id="card{uid}"><rect x="8" y="8" width="496" height="496" rx="64"/></clipPath>'
    inner = "".join(parts)
    if with_bg:
        frame = f'<rect x="8" y="8" width="496" height="496" rx="64" fill="none" stroke="{OUT}" stroke-opacity="0.25" stroke-width="4"/>'
        inner = f'<defs>{clip}</defs><g clip-path="url(#card{uid})">{inner}</g>{frame}'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">{inner}</svg>\n'


# ------------------------------------------------------------------ the cast
CAST = [
    # 1-10: Gulf men
    ("abu-saad", "أبو سعد", dict(bg="blue", skin="medium", head="shemagh", mustache="thick", beard="goatee", mouth="smile", brows="thick")),
    ("al-shaiba", "الشيبة", dict(bg="teal", skin="fair", head="ghutra", hair_color="#e9e9e9", facial_color="#f2f2f2", brow_color="#dcdcdc", mustache="walrus", beard="full", wrinkles=True, glasses="round", frame_color="#8a6a2a", eyes="old", mouth="smile")),
    ("abu-fahad", "أبو فهد", dict(bg="orange", skin="tan", head="taqiyah", facial_color="#9a9a9a", brow_color="#777", mustache="thick", eyes="sleepy", wrinkles=True, mouth="neutral", nose="hook", nose_s=1.1)),
    ("al-shaikh", "الشيخ", dict(bg="gold", skin="medium", head="ghutra", body="bisht", body_color="#3a2a1e", mustache="chevron", beard="short", mouth="smirk", brows="bushy")),
    ("bu-khalid", "بو خالد", dict(bg="navy", skin="brown", head="shemagh", mustache="thick", beard="full", mouth="grin", look=1, brows="thick")),
    ("al-mudeer", "المدير", dict(bg="gray", skin="fair", head="ghutra", agal=True, glasses="square", mustache="pencil", beard="stubble", mouth="neutral", brows="angry")),
    ("al-kashkhah", "الكشخة", dict(bg="purple", skin="medium", head="shemagh", pattern_color="#1c1c22", glasses="aviator", lens1="#1a3d6b", lens2="#4aa3ff", frame_color="#c9a227", mustache="pencil", beard="goatee", mouth="smirk")),
    ("abu-nasser", "أبو ناصر", dict(bg="red", skin="tan", head="ghutra", agal=False, mustache="handlebar", mouth="smile", eyes="happy", brows="raised")),
    ("al-omani", "العماني", dict(bg="green", skin="brown", head="kumma", mustache="thick", beard="short", mouth="smile", kumma_color="#7a2a8c")),
    ("al-haj", "الحاج", dict(bg="teal", skin="tan", head="taqiyah", facial_color="#f0f0f0", brow_color="#e0e0e0", beard="long", mustache="walrus", wrinkles=True, eyes="old", mouth="neutral", glasses="round", frame_color="#5a3d1e")),
    # 11-20: casual men
    ("fahad-gamer", "فهد القيمر", dict(bg="purple", skin="fair", body="hoodie", body_color="#3d3f4c", hair="spiky", hair_color="#1f1a17", head="headphones", accent="#3fe0ff", mouth="grin", brows="raised")),
    ("saloom", "سلوم", dict(bg="orange", skin="light", body="tshirt", body_color="#ffcc33", hair="curly", hair_color="#5a3418", freckles=True, mouth="grin", w=104, nose="small", eyes="normal")),
    ("abu-tagiya", "أبو طاقية", dict(bg="blue", skin="medium", body="thobe", head="taqiyah", cap_color="#ffffff", mustache="thick", beard="stubble", mouth="open", brows="raised", look=-1)),
    ("al-banker", "المصرفي", dict(bg="navy", skin="fair", body="suit", body_color="#2c3448", tie="#d63a35", hair="quiff", hair_color="#2b1f18", mustache="pencil", mouth="smirk", glasses="square")),
    ("captain", "الكابتن", dict(bg="green", skin="brown", body="jersey", body_color="#1f8a4c", stripe="#ffffff", number="10", hair="buzz", hair_color="#1c1410", mouth="grin", beard="stubble", brows="thick")),
    ("abu-qubaa", "أبو قبعة", dict(bg="pink", skin="medium", body="shirt", body_color="#2b2b33", head="fedora", hat_color="#c8322d", mustache="thick", beard="goatee", glasses="sun", mouth="smirk")),
    ("al-mutawwa", "الأستاذ", dict(bg="gold", skin="fair", body="shirt", body_color="#ffffff", hair="bald", hair_color="#3a2a20", glasses="square", frame_color="#1c1c22", mustache="chevron", mouth="neutral", nose="long", brows="thin", wrinkles=True)),
    ("kareem", "كريم", dict(bg="teal", skin="dark", body="tshirt", body_color="#e04a86", hair="afro", hair_color="#1b1310", mouth="grin", beard="stubble", nose="bulb", eyes="normal")),
    ("abu-jabal", "أبو جبل", dict(bg="red", skin="brown", body="tshirt", body_color="#2d3f99", hair="bald", hair_color="#1b1310", beard="full", mustache="thick", mouth="smile", brows="angry", scar=True, w=118)),
    ("al-rassam", "الرسام", dict(bg="purple", skin="light", body="shirt", body_color="#ff8f3f", head="beanie", hat_color="#3a8bdb", mustache="handlebar", beard="goatee", hair_color="#7a4a20", mouth="smile", eyes="happy")),
    # 21-28: elders & funny
    ("al-jid", "الجد", dict(bg="orange", skin="tan", body="thobe", hair="receding", hair_color="#dcdcdc", facial_color="#efefef", brow_color="#dcdcdc", mustache="walrus", wrinkles=True, eyes="old", glasses="round", mouth="smile", nose_s=1.15)),
    ("abu-khashm", "أبو خشم", dict(bg="green", skin="medium", head="ghutra", mustache="thick", mouth="grin", nose="bulb", nose_s=1.35, brows="bushy", gold_tooth=True)),
    ("rainbow", "الملوّن", dict(bg="navy", skin="fair", body="hoodie", body_color="#ff6b3d", hair="curly", hair_color="rainbow", mouth="grin", glasses="sun", lens1="#ff3d8a", lens2="#ffb84a", frame_color="#fff")),
    ("al-malik", "الملك", dict(bg="gold", skin="medium", body="bisht", body_color="#7a1f2a", trim="#f6c533", hair="short", hair_color="#1f1712", head="crown", mustache="handlebar", beard="short", mouth="smile")),
    ("al-gaid", "القايد", dict(bg="gray", skin="tan", head="shemagh", glasses="sun", mustache="thick", beard="full", mouth="neutral", brows="angry")),
    ("abu-ghamza", "أبو غمزة", dict(bg="pink", skin="medium", head="ghutra", agal=True, eyes="wink", mustache="pencil", beard="goatee", mouth="smirk", brows="raised")),
    ("al-zaalan", "الزعلان", dict(bg="red", skin="fair", body="shirt", body_color="#5f7189", hair="short", hair_color="#3a2a20", mouth="frown", brows="angry", mustache="thick", beard="stubble")),
    ("al-nayem", "النعسان", dict(bg="blue", skin="brown", body="thobe", head="taqiyah", cap_color="#e9e3d0", eyes="sleepy", mouth="neutral", mustache="pencil", beard="short", mole=True)),
    # 29-40: women
    ("umm-saad", "أم سعد", dict(bg="pink", skin="fair", head="hijab", scarf_color="#1c1c22", body="abaya", mouth="lips_smile", lashes=True, nose="small", brows="thin", eyes="normal")),
    ("umm-fahad", "أم فهد", dict(bg="teal", skin="medium", head="niqab", scarf_color="#16161a", body="abaya", lashes=True, brows="thin", eyes="normal", look=1)),
    ("al-joharah", "الجوهرة", dict(bg="purple", skin="light", head="hijab", scarf_color="#8b5cf6", scarf_trim="#f6c533", body="abaya", trim="#f6c533", mouth="lips", lips="#c2185b", lashes=True, nose="small", brows="thin")),
    ("noura", "نورة", dict(bg="orange", skin="medium", hair="long", hair_color="#2a1a12", body="tshirt", body_color="#ffffff", mouth="lips_smile", lashes=True, nose="small", brows="thin", earrings="#f6c533", w=102)),
    ("sara", "سارة", dict(bg="blue", skin="fair", hair="ponytail", hair_color="#6b3a1e", body="hoodie", body_color="#ff8fb8", mouth="lips_smile", lashes=True, nose="small", brows="thin", freckles=True, w=102)),
    ("al-yadda", "اليدّة", dict(bg="gold", skin="tan", head="hijab", scarf_color="#4a4a52", body="abaya", glasses="round", frame_color="#8a6a2a", wrinkles=True, mouth="smile", lashes=True, nose="small", brows="thin", eyes="old")),
    ("reem", "ريم", dict(bg="green", skin="brown", hair="bun", hair_color="#1b1310", body="shirt", body_color="#3fd6c0", mouth="lips", lips="#a8324a", lashes=True, nose="small", brows="thin", earrings="#ffffff", glasses="square", frame_color="#c2185b", w=100)),
    ("lulwa", "لولوة", dict(bg="red", skin="light", head="hijab", scarf_color="#ffffff", body="abaya", mouth="lips_smile", lips="#e05a6a", lashes=True, nose="small", brows="thin", look=-1)),
    ("al-dalla", "الدلّوعة", dict(bg="pink", skin="medium", hair="long", hair_color="#8a4b1e", body="tshirt", body_color="#ff4f8b", glasses="sun", lens1="#3b1530", lens2="#ff7fb0", frame_color="#ffffff", mouth="lips", lips="#e0306a", nose="small", brows="thin", earrings="#f6c533", w=102)),
    ("umm-nasser", "أم ناصر", dict(bg="navy", skin="medium", head="niqab", scarf_color="#16161a", body="abaya", trim="#c9a227", lashes=True, brows="thin", eyes="happy")),
    ("hessa", "حصة", dict(bg="teal", skin="fair", head="hijab", scarf_color="#1d7a5f", body="abaya", mouth="lips_smile", lashes=True, nose="small", brows="thin", glasses="square", frame_color="#1c1c22")),
    ("al-gamer-girl", "القيمرة", dict(bg="purple", skin="light", hair="long", hair_color="#3b2bd8", body="hoodie", body_color="#22232b", head="headphones", hat_color="#ff4f8b", accent="#ffffff", mouth="lips_smile", lashes=True, nose="small", brows="thin", w=102)),
]


def main():
    assert len(CAST) == 40, len(CAST)
    for folder, bg in (("svg", True), ("svg-transparent", False)):
        os.makedirs(os.path.join(ROOT, folder), exist_ok=True)
        for i, (slug, name, cfg) in enumerate(CAST, 1):
            fn = os.path.join(ROOT, folder, f"{i:02d}-{slug}.svg")
            with open(fn, "w") as f:
                f.write(avatar(cfg, f"a{i}", bg))
    with open(os.path.join(ROOT, "cast.tsv"), "w") as f:
        for i, (slug, name, _) in enumerate(CAST, 1):
            f.write(f"{i:02d}\t{slug}\t{name}\n")
    print("ok", len(CAST))


if __name__ == "__main__":
    main()
