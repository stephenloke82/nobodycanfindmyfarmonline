"""Props: the Twelve-Month Gate, barn, trees, tables, price tag, tracker, wheel and more."""
import math
import cairo
from gfx import *


# ---------------------------------------------------------------- the gate
def gate(c, x, y, s=1.0, open_=0.0, snow=False, weather_col=None):
    """Five-bar farm gate. Hinge post at x, ground y. open_ 0..1 swings towards viewer."""
    c.save(); c.translate(x, y); c.scale(s, s)
    gw, gh = 520, 230
    post = lambda px: box(c, px - 22, -gh - 70, 44, gh + 80, 8, shade(WOOD, 0.12))
    post(0)
    post(gw + 40)
    for px in (0, gw + 40):
        oval(c, px, -gh - 70, 24, 8, tint(WOOD, 0.2), 5)
        if snow:
            oval(c, px, -gh - 76, 26, 10, SNOW, 4, shading=0)
    ang = open_ * 1.35
    sx = math.cos(ang)
    c.save(); c.translate(22, 0)
    c.scale(max(sx, 0.08), 1)
    c.translate(0, -math.sin(ang) * 0)
    # bars
    for i in range(5):
        by = -40 - i * (gh - 50) / 4
        box(c, 0, by - 14, gw, 28, 7, WOOD)
    # stiles + brace
    box(c, 0, -gh, 36, gh - 16, 6, shade(WOOD, 0.06))
    box(c, gw - 36, -gh, 36, gh - 16, 6, shade(WOOD, 0.06))
    c.save(); c.translate(30, -36); c.rotate(-math.atan2(gh - 80, gw - 70))
    box(c, 0, -13, math.hypot(gw - 70, gh - 80), 26, 7, tint(WOOD, 0.08))
    c.restore()
    if snow:
        by = -40 - 4 * (gh - 50) / 4
        fill_ink(c, lambda: rrect(c, 4, by - 24, gw - 8, 14, 7), SNOW, 3, shading=0)
    # latch
    box(c, gw - 24, -gh * 0.62, 40, 20, 5, hx("8c8f9e"))
    c.restore()
    c.restore()


def latch_point(x, y, s, open_):
    ang = open_ * 1.35
    return (x + (22 + (520 - 4) * max(math.cos(ang), 0.08)) * s, y - 230 * 0.62 * s + 10 * s)


# ---------------------------------------------------------------- buildings
def barn(c, x, y, s=1.0, col=TOMATO, lit=0.0, snow=False, doors_open=0.0, sepia=False):
    c.save(); c.translate(x, y); c.scale(s, s)
    w, h = 420, 250
    fill_ink(c, lambda: poly(c, [(-w / 2, 0), (-w / 2, -h), (-w / 2 - 20, -h), (0, -h - 170), (w / 2 + 20, -h),
                                 (w / 2, -h), (w / 2, 0)]), col)
    for i in range(1, 9):
        stroke(c, lambda: (c.move_to(-w / 2 + i * w / 9, -6), c.line_to(-w / 2 + i * w / 9, -h + 4)), shade(col, 0.15), 3)
    fill_ink(c, lambda: poly(c, [(-w / 2 - 34, -h + 10), (0, -h - 190), (w / 2 + 34, -h + 10), (w / 2 + 34, -h - 6),
                                 (0, -h - 206), (-w / 2 - 34, -h - 6)]), CREAM if not sepia else hx("efe0bf"), 5)
    if snow:
        fill_ink(c, lambda: poly(c, [(-w / 2 - 40, -h + 4), (0, -h - 206), (w / 2 + 40, -h + 4), (w / 2 + 20, -h + 16),
                                     (0, -h - 186), (-w / 2 - 20, -h + 16)]), SNOW, 4, shading=0)
    # loft window
    win = mix(hx("3b3355"), GOLD, lit)
    box(c, -42, -h - 100, 84, 70, 6, win)
    if lit > 0:
        glow(c, 0, -h - 65, 150, GOLD, 0.35 * lit)
    # doors
    dw = 150
    fill_ink(c, lambda: rrect(c, -dw / 2, -170, dw, 170, 4), mix(hx("3b2a35"), hx("ffcf6a"), lit))
    if lit > 0:
        glow(c, 0, -60, 260, GOLD, 0.3 * lit)
    for sgn in (-1, 1):
        dx = sgn * dw / 4 + sgn * doors_open * dw * 0.55
        box(c, dx - dw / 4, -170, dw / 2, 170, 3, CREAM if not sepia else hx("efe0bf"))
        stroke(c, lambda: (c.move_to(dx - dw / 4 + 8, -162), c.line_to(dx + dw / 4 - 8, -8)), col, 7)
        stroke(c, lambda: (c.move_to(dx + dw / 4 - 8, -162), c.line_to(dx - dw / 4 + 8, -8)), col, 7)
    c.restore()


def house(c, x, y, s=1.0, col=CREAM, roof=hx("6b4a7a"), lit=0.0, snow=False):
    c.save(); c.translate(x, y); c.scale(s, s)
    box(c, -150, -200, 300, 200, 4, col)
    fill_ink(c, lambda: poly(c, [(-180, -190), (0, -330), (180, -190)]), roof)
    if snow:
        fill_ink(c, lambda: poly(c, [(-186, -186), (0, -334), (186, -186), (170, -176), (0, -306), (-170, -176)]), SNOW, 4,
                 shading=0)
    box(c, 70, -320, 36, 80, 4, shade(col, 0.3))
    for wx in (-90, 90):
        box(c, wx - 34, -150, 68, 60, 5, mix(hx("8fb4e8"), GOLD, lit))
        if lit:
            glow(c, wx, -120, 90, GOLD, 0.3 * lit)
    box(c, -30, -110, 60, 110, 5, TOMATO)
    c.restore()


def greenhouse(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    fill_ink(c, lambda: poly(c, [(-260, 0), (-260, -220), (0, -330), (260, -220), (260, 0)]), (0.85, 0.95, 1, 0.55), 6)
    for i in range(-2, 3):
        stroke(c, lambda: (c.move_to(i * 104, 0), c.line_to(i * 104, -220 - (2 - abs(i)) * 50)), WHITE, 5, 0.8)
    stroke(c, lambda: (c.move_to(-260, -110), c.line_to(260, -110)), WHITE, 5, 0.8)
    c.restore()


def tent(c, x, y, s=1.0, lit=1.0, open_side=True):
    c.save(); c.translate(x, y); c.scale(s, s)
    glow(c, 0, -150, 520, GOLD, 0.35 * lit)
    fill_ink(c, lambda: poly(c, [(-460, 0), (-460, -220), (-300, -360), (300, -360), (460, -220), (460, 0)]),
             mix(CREAM, hx("ffe2a0"), lit))
    for i in range(-3, 4):
        stroke(c, lambda: (c.move_to(i * 130, -360), c.line_to(i * 150, 0)), shade(CREAM, 0.12), 3)
    fill_ink(c, lambda: (c.move_to(-470, -216), c.line_to(-300, -366), c.line_to(300, -366), c.line_to(470, -216),
                         *[c.line_to(470 - j * 470 / 6, -216 + (24 if j % 2 else 0)) for j in range(1, 13)],
                         c.close_path()), TOMATO, 5)
    c.restore()


# ---------------------------------------------------------------- nature
def tree(c, x, y, s=1.0, kind="leafy", t=0.0, col=None, seed=0, snow=False, sway=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    sw = math.sin(t * 0.9 + seed) * 0.02 * sway
    c.rotate(sw)
    trunk = hx("7a5236")
    if kind == "pine":
        fill_ink(c, lambda: rrect(c, -14, -60, 28, 60, 4), trunk)
        g = col or hx("2f6f3a")
        for i, (w_, yy) in enumerate(((120, -60), (95, -140), (70, -215))):
            fill_ink(c, lambda: poly(c, [(-w_, yy), (0, yy - 120), (w_, yy)]), g)
            if snow:
                fill_ink(c, lambda: poly(c, [(-w_ * 0.5, yy - 60), (0, yy - 120), (w_ * 0.5, yy - 60), (w_ * 0.2, yy - 52),
                                             (0, yy - 62), (-w_ * 0.25, yy - 50)]), SNOW, 3, shading=0)
    else:
        fill_ink(c, lambda: (c.move_to(-18, 0), c.curve_to(-14, -80, -12, -140, -8, -180), c.line_to(8, -180),
                             c.curve_to(12, -140, 14, -80, 20, 0), c.close_path()), trunk)
        if kind == "bare":
            for a, l in ((-0.7, 110), (0.6, 120), (-0.2, 140), (1.0, 80), (-1.1, 80)):
                ex, ey = math.sin(a) * l, -170 - math.cos(a) * l
                stroke(c, lambda: (c.move_to(0, -150), c.curve_to(ex * 0.3, -200, ex * 0.7, ey + 20, ex, ey)), INK, 14)
                stroke(c, lambda: (c.move_to(0, -150), c.curve_to(ex * 0.3, -200, ex * 0.7, ey + 20, ex, ey)), trunk, 8)
                if snow:
                    stroke(c, lambda: (c.move_to(ex * 0.5, ey * 0.85 - 10), c.line_to(ex, ey - 4)), SNOW, 6)
        else:
            g = col or (hx("f6c3d2") if kind == "blossom" else hx("4f9a3e") if kind == "leafy" else hx("e0892a"))
            r = rng_for("tree", seed)
            blobs = [(0, -250, 105), (-80, -200, 80), (80, -205, 82), (-40, -300, 70), (50, -300, 72)]
            for (bx, by, br) in blobs:
                circle(c, bx, by, br + 8, INK, 0, alpha=0.9)
            for (bx, by, br) in blobs:
                circle(c, bx, by, br, g, 0, shading=0.0)
            g2 = cairo.LinearGradient(-120, -360, 120, -150)
            g2.add_color_stop_rgba(0.4, 0, 0, 0, 0); g2.add_color_stop_rgba(1, 0.05, 0.05, 0.2, 0.18)
            for (bx, by, br) in blobs:
                c.new_sub_path(); c.arc(bx, by, br, 0, 6.3)
            c.set_source(g2); c.fill()
            if kind == "blossom":
                for i in range(18):
                    circle(c, r.uniform(-140, 140), r.uniform(-360, -170), 6, WHITE, 0)
            if kind in ("leafy",):
                for i in range(6):
                    circle(c, r.uniform(-120, 120), r.uniform(-340, -180), 9, TOMATO if seed % 2 else GOLD, 3)
    c.restore()


def sunflower(c, x, y, s=1.0, t=0.0, seed=0):
    c.save(); c.translate(x, y); c.scale(s, s)
    sw = math.sin(t * 1.2 + seed) * 6
    stroke(c, lambda: (c.move_to(0, 0), c.curve_to(0, -80, sw, -160, sw, -220)), INK, 14)
    stroke(c, lambda: (c.move_to(0, 0), c.curve_to(0, -80, sw, -160, sw, -220)), LEAF, 8)
    oval(c, -24, -110, 26, 12, LEAF, 4)
    c.save(); c.translate(sw, -230); c.rotate(math.sin(t + seed) * 0.08)
    for i in range(14):
        a = i * 2 * math.pi / 14
        c.save(); c.rotate(a)
        oval(c, 0, -46, 14, 26, GOLD, 4, shading=0.08)
        c.restore()
    circle(c, 0, 0, 30, hx("6b3f1f"), 5)
    c.restore()
    c.restore()


def tulip(c, x, y, s=1.0, col=TOMATO, t=0.0, seed=0, glow_=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    sw = math.sin(t * 1.5 + seed) * 4
    stroke(c, lambda: (c.move_to(0, 0), c.line_to(sw, -60)), LEAF, 6)
    if glow_:
        glow(c, sw, -72, 40, col, 0.5 * glow_)
    fill_ink(c, lambda: (c.move_to(sw - 14, -78), c.line_to(sw - 7, -66), c.line_to(sw, -78), c.line_to(sw + 7, -66),
                         c.line_to(sw + 14, -78), c.curve_to(sw + 16, -56, sw - 16, -56, sw - 14, -78)), col, 3, shading=0.1)
    c.restore()


def pumpkin(c, x, y, s=1.0, col=hx("ef8a1d")):
    c.save(); c.translate(x, y); c.scale(s, s)
    for dx, rx in ((-22, 30), (22, 30), (0, 32)):
        oval(c, dx, -34, rx, 34, col, 5)
    fill_ink(c, lambda: rrect(c, -5, -80, 10, 18, 3), LEAF, 4)
    c.restore()


def corn(c, x, y, s=1.0, t=0.0, seed=0, col=hx("d9b24a")):
    c.save(); c.translate(x, y); c.scale(s, s)
    sw = math.sin(t * 1.4 + seed * 0.7) * 8
    stroke(c, lambda: (c.move_to(0, 0), c.curve_to(0, -100, sw * 0.5, -180, sw, -260)), INK, 12)
    stroke(c, lambda: (c.move_to(0, 0), c.curve_to(0, -100, sw * 0.5, -180, sw, -260)), col, 7)
    for i, yy in enumerate((-90, -150, -210)):
        sg = 1 if i % 2 else -1
        stroke(c, lambda: (c.move_to(sw * yy / -260, yy), c.curve_to(sg * 40, yy - 30, sg * 70, yy + 10, sg * 80 + sw * 0.3,
                                                                     yy + 30)), col, 8)
    c.restore()


def hay_bale(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    box(c, -70, -70, 140, 70, 14, hx("e8c15a"))
    for i in range(3):
        stroke(c, lambda: (c.move_to(-60, -54 + i * 18), c.line_to(60, -54 + i * 18)), shade(hx("e8c15a"), 0.2), 3)
    c.restore()


def fence(c, x0, x1, y, s=1.0, col=WOOD, snow=False):
    n = int((x1 - x0) / (140 * s)) + 1
    for i in range(n + 1):
        px = x0 + i * 140 * s
        box(c, px - 9 * s, y - 120 * s, 18 * s, 124 * s, 4, col, 4)
    for yy in (-95, -50):
        box(c, x0 - 12, y + yy * s - 9 * s, x1 - x0 + 24, 18 * s, 5, tint(col, 0.08), 4)
        if snow:
            fill_ink(c, lambda: rrect(c, x0 - 10, y + yy * s - 15 * s, x1 - x0 + 20, 7 * s, 3), SNOW, 2, shading=0)


# ---------------------------------------------------------------- objects
def table(c, x, y, w, s=1.0, cloth=CREAM, chairs=0, chairs_shown=None, seated=None, t=0.0, plates=0):
    """Long table seen from the front, chairs behind it."""
    c.save(); c.translate(x, y); c.scale(s, s)
    if chairs:
        sp = w / max(chairs, 1)
        for i in range(chairs):
            if chairs_shown is not None and i >= chairs_shown:
                continue
            cx_ = -w / 2 + sp * (i + 0.5)
            box(c, cx_ - 20, -170, 40, 70, 6, WOOD, 4)
    if seated:
        seated(c)
    box(c, -w / 2, -110, w, 30, 8, cloth)
    fill_ink(c, lambda: (c.move_to(-w / 2, -84), c.line_to(w / 2, -84), c.line_to(w / 2 - 6, -40),
                         c.curve_to(w / 4, -30, -w / 4, -30, -w / 2 + 6, -40), c.close_path()), cloth, 5)
    for lx in (-w / 2 + 30, w / 2 - 30):
        box(c, lx - 8, -40, 16, 40, 3, shade(WOOD, 0.2), 4)
    for i in range(plates):
        px = -w / 2 + (i + 0.5) * w / max(plates, 1)
        oval(c, px, -112, 26, 7, WHITE, 3)
    c.restore()


def phone(c, x, y, s=1.0, lit=0.0, t=0.0, ring=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rotate(math.sin(t * 40) * 0.06 * ring)
    box(c, -36, -64, 72, 128, 14, INK, 4)
    box(c, -28, -52, 56, 98, 6, mix(hx("38406a"), hx("aee3ff"), lit), 0)
    if lit:
        glow(c, 0, 0, 120, hx("aee3ff"), 0.35 * lit)
    if ring:
        for i in range(2):
            stroke(c, lambda: c.arc(0, 0, 90 + i * 26, -0.6, 0.6), GOLD, 6, ring)
            stroke(c, lambda: c.arc(0, 0, 90 + i * 26, math.pi - 0.6, math.pi + 0.6), GOLD, 6, ring)
    c.restore()


def bucket(c, x, y, s=1.0, col=hx("a9b3c9"), fill=None):
    c.save(); c.translate(x, y); c.scale(s, s)
    stroke(c, lambda: c.arc(0, -70, 50, math.pi, 2 * math.pi), INK, 5)
    fill_ink(c, lambda: poly(c, [(-50, -70), (50, -70), (40, 0), (-40, 0)]), col)
    oval(c, 0, -70, 50, 10, shade(col, 0.3), 4)
    if fill:
        fill(c)
    c.restore()


def coins(c, x, y, n, s=1.0, col=GOLD):
    c.save(); c.translate(x, y); c.scale(s, s)
    for i in range(int(n)):
        col_i = i % 5
        row = i // 5
        cx_ = -80 + col_i * 40 + (row % 2) * 20
        cy_ = -row * 16
        oval(c, cx_, cy_, 22, 9, col, 3, shading=0.1)
    c.restore()


def money_bag(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    fill_ink(c, lambda: smooth(c, [(-30, -150), (30, -150), (80, -80), (90, -20), (0, 0), (-90, -20), (-80, -80)]),
             hx("d8b98a"))
    stroke(c, lambda: (c.move_to(-32, -140), c.line_to(32, -140)), TOMATO, 10)
    text(c, "$", 0, -40, 110, DISPLAY, shade(hx("d8b98a"), 0.45), "center")
    c.restore()


def calendar(c, x, y, w, h, months_lit=None, bright=None, t=0.0, grey=False):
    """12-month wall calendar grid. months_lit: list of 0..1 per month."""
    box(c, x - 10, y - 10, w + 20, h + 20, 16, PAPER)
    names = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()
    cw, ch = (w - 50) / 4, (h - 40) / 3
    for i in range(12):
        cx_ = x + 10 + (i % 4) * (cw + 10)
        cy_ = y + 10 + (i // 4) * (ch + 10)
        lit = months_lit[i] if months_lit else 0.0
        base = hx("c9c6c0") if grey else CREAM
        col = mix(base, GOLD if bright is None else bright, lit)
        box(c, cx_, cy_, cw, ch, 10, col, 4)
        text(c, names[i], cx_ + cw / 2, cy_ + ch / 2 + 20, 54, DISPLAY, INK if lit > 0.3 else mix(INK, base, 0.45),
             "center")


def ticket(c, x, y, s=1.0, col=GOLD, label="TICKET", rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)

    def p():
        c.move_to(-110, -55); c.line_to(110, -55); c.line_to(110, -15); c.arc_negative(110, 0, 15, -math.pi / 2, math.pi / 2)
        c.line_to(110, 55); c.line_to(-110, 55); c.line_to(-110, 15)
        c.arc_negative(-110, 0, 15, math.pi / 2, -math.pi / 2); c.close_path()
    fill_ink(c, p, col)
    stroke(c, lambda: (c.move_to(60, -45), c.line_to(60, 45)), INK, 3, 0.5)
    text(c, label, -20, 16, 40, DISPLAY, INK, "center")
    c.restore()


def stamp(c, x, y, s=1.0, txt="SOLD OUT", rot=-0.18, alpha=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    font(c, DISPLAY, 96)
    w = c.text_extents(txt).x_advance
    rrect(c, -w / 2 - 34, -78, w + 68, 136, 18)
    setc(c, TOMATO, alpha); c.set_line_width(12); c.stroke()
    text(c, txt, 0, 34, 96, DISPLAY, TOMATO, "center", alpha)
    c.restore()


def price_tag(c, x, y, lines, title, place, t, t0, swing=True, maxw=680):
    """Wooden price tag hanging from a nail at (x,y); swings in at t0.
    lines: list of (big, small) pairs. Big >= 120 px."""
    if t < t0:
        return
    lt = t - t0
    drop = ease_out(prog(lt, 0, 0.55))
    ang = damp_swing(lt - 0.35, 0.55, 0.9, 1.6) if swing else 0
    ang = ang * drop + (1 - drop) * -0.9
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    # measure
    big_sz = 150 if len(lines) == 1 else 128
    small_sz = 56
    rows = []
    for pre, big, post in lines:
        bs = fit_size(c, big, DISPLAY, big_sz, maxw - 80, 120)
        rows.append((pre, big, post, bs))
    place_lines = wrap(c, title, BODY, 60, maxw - 90) if title else []
    pl2 = wrap(c, place, BODYM, 54, maxw - 90) if place else []
    hgt = 60 + sum(r[3] * 0.97 + (small_sz * 1.12 if r[0] else 0) + (small_sz * 1.12 if r[2] else 0) for r in rows) \
        + 36 + len(place_lines) * 66 + len(pl2) * 62 + 34
    tw = maxw
    # string
    stroke(c, lambda: (c.move_to(0, 0), c.line_to(-60, 60), c.move_to(0, 0), c.line_to(60, 60)), hx("6b4a2a"), 5)
    top = 50

    def board():
        c.move_to(-tw / 2 + 60, top); c.line_to(tw / 2 - 60, top); c.line_to(tw / 2, top + 60)
        c.line_to(tw / 2, top + hgt - 24); c.arc(tw / 2 - 24, top + hgt - 24, 24, 0, math.pi / 2)
        c.line_to(-tw / 2 + 24, top + hgt); c.arc(-tw / 2 + 24, top + hgt - 24, 24, math.pi / 2, math.pi)
        c.line_to(-tw / 2, top + 60); c.close_path()
    shadow(c, 18, top + hgt + 30, tw * 0.45, 26, 0.18)
    fill_ink(c, board, hx("d9a868"), 7, shading=0.22)
    c.save(); board(); c.clip()
    for i in range(9):
        gy = top + 40 + i * hgt / 9
        stroke(c, lambda: (c.move_to(-tw / 2, gy), c.curve_to(-tw / 6, gy + 10, tw / 6, gy - 10, tw / 2, gy + 4)),
               shade(hx("d9a868"), 0.12), 3)
    c.restore()
    circle(c, 0, top + 26, 11, hx("8a6a4a"), 4)
    yy = top + 56
    for pre, big, post, bs in rows:
        if pre:
            yy += small_sz * 1.0
            text(c, pre, 0, yy, small_sz, BODY, hx("5a2a14"), "center")
            yy += small_sz * 0.12
        yy += bs * 0.84
        text(c, big, 0, yy, bs, DISPLAY, INK, "center")
        yy += bs * 0.13
        if post:
            yy += small_sz * 1.0
            text(c, post, 0, yy, small_sz, BODY, hx("5a2a14"), "center")
            yy += small_sz * 0.12
    yy += 24
    stroke(c, lambda: (c.move_to(-tw / 2 + 50, yy), c.line_to(tw / 2 - 50, yy)), shade(hx("d9a868"), 0.3), 4)
    yy += 6
    for ln in place_lines:
        yy += 64
        text(c, ln, 0, yy, 60, BODY, INK, "center")
    for ln in pl2:
        yy += 62
        text(c, ln, 0, yy, 54, BODYM, hx("4a2f1c"), "center")
    c.restore()


def tracker(c, n, season, t, x=1890, y=40, a=1.0):
    """Top-right 'No. X of 30' plus four-season wheel."""
    if a <= 0:
        return
    c.push_group()
    label = f"No. {n} of 30"
    w = text_w(c, label, DISPLAY, 56) + 60
    box(c, x - w - 140, y, w, 84, 42, PAPER, 6)
    text(c, label, x - w - 140 + w / 2, y + 62, 56, DISPLAY, INK, "center")
    season_wheel(c, x - 58, y + 42, 54, season, t)
    c.pop_group_to_source()
    c.paint_with_alpha(a)


SEASONS = ["winter", "spring", "summer", "fall"]


def season_wheel(c, x, y, r, season, t=0.0, icons=True, highlight=1.0):
    idx = SEASONS.index(season) if season in SEASONS else -1
    for i, sname in enumerate(SEASONS):
        a0 = -math.pi / 2 + i * math.pi / 2 - math.pi / 4
        a1 = a0 + math.pi / 2
        col = SEASON_COL[sname]
        on = (i == idx)
        cc = col if on or idx < 0 else mix(col, PAPER, 0.62)
        fill_ink(c, lambda: (c.move_to(x, y), c.arc(x, y, r * (1.08 if on else 1.0), a0, a1), c.close_path()), cc,
                 max(3, r * 0.07), shading=0)
    circle(c, x, y, r * 0.22, PAPER, max(3, r * 0.06))
    if idx >= 0:
        a = -math.pi / 2 + idx * math.pi / 2
        stroke(c, lambda: (c.move_to(x, y), c.line_to(x + math.cos(a) * r * 0.75, y + math.sin(a) * r * 0.75)), INK,
               max(4, r * 0.1))


def chapter_wheel(c, x, y, r, t, season_from, season_to, p, labels=True):
    """Big wheel that rotates the pointer between seasons."""
    for i, sname in enumerate(SEASONS):
        a0 = -math.pi / 2 + i * math.pi / 2 - math.pi / 4
        fill_ink(c, lambda: (c.move_to(x, y), c.arc(x, y, r, a0, a0 + math.pi / 2), c.close_path()), SEASON_COL[sname], 8,
                 shading=0.1)
        am = a0 + math.pi / 4
        if labels:
                text(c, sname.upper(), x + math.cos(am) * r * 0.6, y + math.sin(am) * r * 0.6 + 14, r * 0.15, DISPLAY,
                 INK if sname == "summer" else PAPER, "center")
    circle(c, x, y, r * 0.16, PAPER, 8)


def moon(c, x, y, r, col=hx("fff1c4")):
    glow(c, x, y, r * 2.4, col, 0.35)
    circle(c, x, y, r, col, 6, shading=0.12)
    for (dx, dy, rr) in ((-0.3, -0.2, 0.18), (0.25, 0.25, 0.12), (0.2, -0.35, 0.08)):
        oval(c, x + dx * r, y + dy * r, rr * r, rr * r, shade(col, 0.08), 0, shading=0)


def star(c, x, y, r, col=hx("fff1c4"), a=1.0):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        ang = -math.pi / 2 + i * math.pi / 5
        pts.append((x + math.cos(ang) * rr, y + math.sin(ang) * rr))
    poly(c, pts)
    setc(c, col, a); c.fill()


def lantern_string(c, x0, x1, y, sag=60, n=10, t=0.0, cols=(GOLD,)):
    stroke(c, lambda: (c.move_to(x0, y), c.curve_to(x0 + (x1 - x0) * 0.3, y + sag, x0 + (x1 - x0) * 0.7, y + sag, x1, y)),
           INK, 4)
    for i in range(1, n):
        u = i / n
        bx = (1 - u) ** 3 * x0 + 3 * (1 - u) ** 2 * u * (x0 + (x1 - x0) * 0.3) + 3 * (1 - u) * u * u * (
            x0 + (x1 - x0) * 0.7) + u ** 3 * x1
        by = y + 3 * (1 - u) * u * sag * 1.0
        fl = 0.75 + 0.25 * math.sin(t * 5 + i * 1.7)
        col = cols[i % len(cols)]
        glow(c, bx, by + 12, 46, col, 0.45 * fl)
        circle(c, bx, by + 12, 10, mix(col, WHITE, 0.4), 3)


def car(c, x, y, s=1.0, col=SKY, t=0.0, moving=0.0, flip=False):
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    shadow(c, 0, 4, 160, 18, 0.25)
    bob = math.sin(t * 14) * 1.5 * moving
    fill_ink(c, lambda: smooth(c, [(-150, -40 + bob), (-140, -90 + bob), (-70, -100 + bob), (-40, -150 + bob),
                                   (60, -150 + bob), (100, -100 + bob), (150, -90 + bob), (156, -40 + bob)]), col)
    box(c, -26, -138 + bob, 52, 36, 6, hx("bfe3ff"), 4)
    box(c, 36, -138 + bob, 50, 36, 6, hx("bfe3ff"), 4)
    for wx in (-90, 95):
        c.save(); c.translate(wx, -30)
        c.rotate(t * 8 * moving)
        circle(c, 0, 0, 30, INK, 4)
        circle(c, 0, 0, 12, hx("c9c6c0"), 3)
        stroke(c, lambda: (c.move_to(-12, 0), c.line_to(12, 0)), INK, 3)
        c.restore()
    circle(c, 150, -70 + bob, 10, GOLD, 3)
    c.restore()


def sign(c, x, y, txt, size=54, col=CREAM, s=1.0, post=True, rot=0.0, face=DISPLAY):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    w = text_w(c, txt, face, size) + 60
    if post:
        box(c, -10, -20, 20, 140, 4, WOOD, 4)
    box(c, -w / 2, -size * 1.5, w, size * 1.6, 12, col, 5)
    text(c, txt, 0, -size * 0.35, size, face, INK, "center")
    c.restore()


def slate(c, x, y, w, h, lines=(), size=54, t=0.0, starts=None):
    box(c, x - 14, y - 14, w + 28, h + 28, 14, WOOD, 6)
    box(c, x, y, w, h, 8, hx("2d3a35"), 4)
    for i, ln in enumerate(lines):
        st = starts[i] if starts else 0
        ease_text(c, ln, x + 40, y + 80 + i * size * 1.35, size, t, st, BODY, hx("f4f0e6"))
