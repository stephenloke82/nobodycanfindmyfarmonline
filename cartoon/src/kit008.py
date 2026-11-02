"""Drawing kit for video 008: phones, maps, pins, listings, gates, dairy, city, roadmap and cards."""
import math
import cairo
from gfx import *
from chars import person, cow, goat, chicken, SKINS, HAIR, COATS
from props import gate, barn, house, tree, fence, car, sign, table, phone, stamp, hay_bale
from sets import season_bg, weather
from sarah import sarah
import timeline

GREY = hx("b9b4ad")
GREY_D = hx("8f8a84")
PIN = hx("e2452f")
MAPG = hx("dfeccb")
ROAD = hx("f7f1e3")
WATER = hx("a9cbe8")
NAVY = hx("1b2a6b")
GOOGLE = [hx("4285f4"), hx("ea4335"), hx("fbbc05"), hx("34a853")]


def M(S, t):
    return timeline.mouth(S, t)


def P(S, i, default=0.0):
    if not S.ph:
        return default
    return S.ph[min(i, len(S.ph) - 1)]


def SAR(c, S, t, x, y, s=1.0, **kw):
    sarah(c, x, y, s, t, mouth=M(S, t), **kw)


def countup(v, t, start, dur=1.6):
    return v * ease_out(prog(t, start, dur))


def cam(c, t, dur, z0=1.0, z1=1.05, fx=W / 2, fy=H / 2):
    z = lerp(z0, z1, ease(t / max(dur, 0.1)))
    c.translate(fx, fy); c.scale(z, z); c.translate(-fx, -fy)


# ---------------------------------------------------------------- text cards and pills
def card(c, lines, x, y, t, starts, size=64, face=BODY, align="left", anchor="tl", col=INK, bg=PAPER, pad=40,
         gap=1.32, minw=0, lw=6, radius=28, maxw=None):
    items = []
    for ln in lines:
        if isinstance(ln, str):
            ln = (ln, size, face, col)
        items.append(ln)
    if maxw:
        items = [(s, min(sz, fit_size(c, s, f, sz, maxw - 2 * pad, 40)), f, cl) for (s, sz, f, cl) in items]
    ws = [text_w(c, s, f, sz) for (s, sz, f, _) in items]
    w = max(max(ws) + 2 * pad, minw)
    hs = [sz * gap for (_, sz, _, _) in items]
    h = sum(hs) - items[-1][1] * (gap - 1) + 2 * pad + items[0][1] * 0.12
    bx = x - (w / 2 if anchor in ("tc", "c") else w if anchor == "tr" else 0)
    by = y - (h / 2 if anchor == "c" else 0)
    a = ease_out(prog(t, starts[0] - 0.15, 0.6))
    if a <= 0:
        return (bx, by, w, h)
    c.push_group()
    shadow(c, bx + w / 2 + 10, by + h + 8, w * 0.5, 16, 0.18)
    box(c, bx, by, w, h, radius, bg, lw, shading=0.05)
    c.pop_group_to_source()
    c.paint_with_alpha(a)
    yy = by + pad
    for (s, sz, f, cl), st in zip(items, starts):
        yy += sz * 0.86
        tx = bx + pad if align == "left" else bx + w / 2 if align == "center" else bx + w - pad
        ease_text(c, s, tx, yy, sz, t, st, f, cl, align)
        yy += sz * (gap - 0.86)
    return (bx, by, w, h)


def pill(c, s, x, y, t, start, size=56, bg=PAPER, col=INK, mark=None, anchor="c", lw=6):
    a = ease_out(prog(t, start, 0.6))
    if a <= 0:
        return 0
    tw = text_w(c, s, BODY, size)
    extra = size * 0.9 if mark else 0
    w, h = tw + 70 + extra, size * 1.7
    bx = x - w / 2 if anchor == "c" else x
    c.push_group()
    shadow(c, bx + w / 2, y + h / 2 + 8, w * 0.45, 12, 0.16)
    box(c, bx, y - h / 2 + (1 - a) * 14, w, h, h / 2, bg, lw, shading=0.05)
    tx = bx + 35
    if mark == "x":
        circle(c, tx + size * 0.32, y + (1 - a) * 14, size * 0.36, TOMATO, 4, shading=0)
        stroke(c, lambda: (c.move_to(tx + size * 0.14, y - size * 0.18 + (1 - a) * 14),
                           c.line_to(tx + size * 0.5, y + size * 0.18 + (1 - a) * 14),
                           c.move_to(tx + size * 0.5, y - size * 0.18 + (1 - a) * 14),
                           c.line_to(tx + size * 0.14, y + size * 0.18 + (1 - a) * 14)), PAPER, 6)
        tx += extra
    elif mark == "v":
        circle(c, tx + size * 0.32, y + (1 - a) * 14, size * 0.36, LEAF, 4, shading=0)
        stroke(c, lambda: (c.move_to(tx + size * 0.12, y + (1 - a) * 14),
                           c.line_to(tx + size * 0.28, y + size * 0.16 + (1 - a) * 14),
                           c.line_to(tx + size * 0.54, y - size * 0.18 + (1 - a) * 14)), PAPER, 6)
        tx += extra
    text(c, s, tx, y + size * 0.35 + (1 - a) * 14, size, BODY, col)
    c.pop_group_to_source(); c.paint_with_alpha(a)
    return w


def title(c, s, x, y, t, start, size=110, col=PAPER, outline=INK, align="center", olw=16):
    ease_text(c, s, x, y, size, t, start, DISPLAY, col, align, outline=outline, olw=olw, dur=0.9)


def tracker3(c, n, t, a=1.0):
    if not n:
        return
    s = f"No. {n} of 3"
    w = text_w(c, s, DISPLAY, 50) + 60
    c.push_group()
    box(c, W - 40 - w, 36, w, 84, 42, GOLD, 6)
    text(c, s, W - 40 - w / 2, 92, 50, DISPLAY, INK, "center")
    c.pop_group_to_source(); c.paint_with_alpha(a)


ROAD_LABELS = ["Find your pin", "Claim it", "Fill every box"]


def roadmap(c, lit, t, t0=0.0, y=860, x0=260, done=0, blur_rest=True, gold3=False):
    """Three numbered tiles; `lit` = current (1..3)."""
    a = ease_out(prog(t, t0, 0.7))
    if a <= 0:
        return
    c.push_group()
    tw, th, gap = 440, 150, 40
    total = 3 * tw + 2 * gap
    x0 = (W - total) / 2
    box(c, x0 - 30, y - 30, total + 60, th + 60, 40, hx("2f6f2c"), 6, shading=0.05)
    for i in range(3):
        x = x0 + i * (tw + gap)
        on = (i + 1) == lit or (i + 1) <= done
        blur = blur_rest and (i + 1) > max(lit, done)
        col = GOLD if (gold3 and i == 2 and lit == 3) else (CREAM if on else hx("d9d2c2"))
        alpha = 0.45 if blur else 1.0
        c.push_group()
        box(c, x, y, tw, th, 26, col, 6)
        circle(c, x + 70, y + th / 2, 46, LEAF if on else GREY, 5)
        text(c, str(i + 1), x + 70, y + th / 2 + 22, 64, DISPLAY, PAPER, "center")
        lsz = fit_size(c, ROAD_LABELS[i], BODY, 50, tw - 160, 30)
        text(c, ROAD_LABELS[i], x + 130, y + th / 2 + lsz * 0.36, lsz, BODY, INK)
        if (i + 1) == lit:
            stroke(c, lambda: rrect(c, x - 8, y - 8, tw + 16, th + 16, 32), GOLD, 8)
        c.pop_group_to_source(); c.paint_with_alpha(alpha)
    c.pop_group_to_source(); c.paint_with_alpha(a)


# ---------------------------------------------------------------- pins, maps, listings
def map_pin(c, x, y, s=1.0, col=PIN, ghost=False, drop=1.0, glow_=0.0):
    yy = y - (1 - ease_out(drop)) * 260 * s
    if drop <= 0:
        return
    c.save(); c.translate(x, yy); c.scale(s, s)
    shadow(c, 0, 4, 26, 8, 0.22)
    if glow_:
        glow(c, 0, -70, 90, GOLD, glow_)
    colr = GREY if ghost else col
    fill_ink(c, lambda: (c.move_to(0, 0), c.curve_to(-14, -26, -46, -46, -46, -78),
                         c.arc(0, -78, 46, math.pi, 2 * math.pi), c.curve_to(46, -46, 14, -26, 0, 0),
                         c.close_path()), colr, 6)
    circle(c, 0, -80, 18, PAPER if not ghost else hx("dcd8d2"), 4, shading=0)
    c.restore()


def ghost_sheet(c, x, y, s, t, a=1.0):
    """A little bedsheet ghost draped over a pin."""
    if a <= 0:
        return
    c.push_group()
    c.save(); c.translate(x, y + math.sin(t * 2.2) * 6 * s); c.scale(s, s)
    pts = [(-62, -20), (-58, -100), (-30, -150), (0, -160), (30, -150), (58, -100), (62, -20)]
    wav = [(62 - k * 124 / 6, -20 + (12 if k % 2 else -4) + math.sin(t * 4 + k) * 4) for k in range(7)]
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    for p in wav:
        c.line_to(*p)
    c.close_path()
    path = c.copy_path(); c.new_path()
    fill_ink(c, lambda: (c.append_path(path)), hx("f4f2f7"), 6, shading=0.1)
    for ex in (-20, 20):
        ellipse(c, ex, -100, 9, 13); setc(c, INK); c.fill()
    ellipse(c, 0, -66, 10, 7); setc(c, INK, 0.85); c.fill()
    c.restore()
    c.pop_group_to_source(); c.paint_with_alpha(a)


def map_bg(c, x, y, w, h, t, seed=3):
    c.save(); rrect(c, x, y, w, h, 0); c.clip()
    setc(c, MAPG); c.paint()
    r = rng_for("map", seed)
    # fields
    for i in range(14):
        fx, fy = x + r.uniform(0, w), y + r.uniform(0, h)
        rrect(c, fx, fy, r.uniform(90, 200), r.uniform(60, 140), 14)
        setc(c, hx("cfe2b4") if i % 2 else hx("e7f0d6")); c.fill()
    # river
    c.move_to(x - 20, y + h * 0.75)
    c.curve_to(x + w * 0.3, y + h * 0.55, x + w * 0.55, y + h * 0.95, x + w + 20, y + h * 0.7)
    setc(c, WATER); c.set_line_width(38); c.stroke()
    # roads
    for (ax, ay, bx, by) in ((0, 0.3, 1, 0.42), (0.35, 0, 0.5, 1), (0, 0.85, 1, 0.6), (0.78, 0, 0.7, 1)):
        c.move_to(x + ax * w, y + ay * h); c.line_to(x + bx * w, y + by * h)
        setc(c, hx("c9c2b0")); c.set_line_width(30); c.stroke()
        c.move_to(x + ax * w, y + ay * h); c.line_to(x + bx * w, y + by * h)
        setc(c, ROAD); c.set_line_width(20); c.stroke()
    c.restore()


def phone_frame(c, x, y, w, h, screen, t, tilt=0.0, hand=False):
    """A big phone with a drawable screen. screen(c, sx, sy, sw, sh, t)."""
    c.save()
    c.translate(x + w / 2, y + h / 2); c.rotate(tilt); c.translate(-w / 2, -h / 2)
    shadow(c, w / 2 + 16, h + 14, w * 0.45, 22, 0.2)
    if hand:
        fill_ink(c, lambda: smooth(c, [(-30, h * 0.55), (40, h * 0.42), (60, h * 0.95), (w * 0.6, h + 140),
                                       (-60, h + 160)]), SKINS[0])
    box(c, 0, 0, w, h, 54, NAVY, 7, shading=0.05)
    sx, sy, sw, sh = 22, 70, w - 44, h - 140
    c.save(); rrect(c, sx, sy, sw, sh, 18); c.clip()
    setc(c, PAPER); c.paint()
    screen(c, sx, sy, sw, sh, t)
    c.restore()
    stroke(c, lambda: rrect(c, sx, sy, sw, sh, 18), INK, 4)
    box(c, w / 2 - 50, 30, 100, 16, 8, hx("0f1846"), 0, shading=0)
    circle(c, w / 2, h - 36, 18, hx("0f1846"), 3, shading=0)
    c.restore()


def search_bar(c, x, y, w, s, t, start, size=40, cps=14):
    box(c, x, y, w, size * 1.8, size * 0.9, PAPER, 4, shading=0)
    n = int(max(0, (t - start)) * cps)
    shown = s[:n]
    circle(c, x + size * 0.9, y + size * 0.9, size * 0.3, PAPER, 4, shading=0)
    stroke(c, lambda: (c.move_to(x + size * 1.1, y + size * 1.1), c.line_to(x + size * 1.35, y + size * 1.35)), INK, 4)
    text(c, shown, x + size * 1.7, y + size * 1.25, size, BODYM, INK)
    if int(t * 2) % 2 == 0 and n <= len(s):
        tw = text_w(c, shown, BODYM, size)
        c.rectangle(x + size * 1.7 + tw + 4, y + size * 0.4, 3, size); setc(c, INK); c.fill()


def photo_tile(c, x, y, w, h, kind, t, seed=0):
    """Small square 'photo' of people enjoying a farm."""
    c.save(); rrect(c, x, y, w, h, 12); c.clip()
    g = cairo.LinearGradient(0, y, 0, y + h)
    g.add_color_stop_rgba(0, *hx("8cc4f0")); g.add_color_stop_rgba(1, *hx("d6efff"))
    c.set_source(g); c.paint()
    c.rectangle(x, y + h * 0.62, w, h); setc(c, GRASS); c.fill()
    s = h / 420
    if kind == "goats":
        goat(c, x + w * 0.62, y + h * 0.92, 0.55 * s * 2, t, seed=seed)
        person(c, x + w * 0.3, y + h * 0.98, 0.42 * s * 2, t, seed=seed + 3, kid=True)
    elif kind == "picnic":
        table(c, x + w * 0.5, y + h * 0.86, w * 0.7, s * 1.6)
        person(c, x + w * 0.22, y + h * 0.98, 0.36 * s * 2, t, seed=seed + 5)
        person(c, x + w * 0.78, y + h * 0.98, 0.36 * s * 2, t, seed=seed + 8, kid=True)
    elif kind == "tree":
        tree(c, x + w * 0.5, y + h * 0.8, s * 1.4, "fruit", t, seed=seed)
        person(c, x + w * 0.75, y + h * 0.98, 0.36 * s * 2, t, seed=seed + 2)
    else:
        barn(c, x + w * 0.5, y + h * 0.8, s * 0.9)
    c.restore()
    stroke(c, lambda: rrect(c, x, y, w, h, 12), INK, 4)


def listing(c, x, y, w, t, full=1.0, name="Willow Creek Farm", start=0.0, stars=True):
    """A Google-style business listing card. full: 0 = ghost (grey, empty), 1 = complete."""
    h = 600
    shadow(c, x + w / 2, y + h + 10, w * 0.45, 18, 0.2)
    box(c, x, y, w, h, 30, PAPER, 6, shading=0.03)
    # photo strip
    ph_h = 210
    if full > 0.05:
        n = 3
        tw = (w - 40 - 2 * 14) / n
        for i, kind in enumerate(["goats", "picnic", "tree"]):
            a = ease_out(prog(t, start + i * 0.25, 0.6)) * full
            if a > 0:
                c.push_group()
                photo_tile(c, x + 20 + i * (tw + 14), y + 20, tw, ph_h, kind, t, seed=i)
                c.pop_group_to_source(); c.paint_with_alpha(a)
    else:
        box(c, x + 20, y + 20, w - 40, ph_h, 16, hx("e6e2db"), 3, shading=0)
        text(c, "No photos", x + w / 2, y + 20 + ph_h / 2 + 18, 46, BODYM, GREY_D, "center")
    yy = y + ph_h + 90
    text(c, name if full > 0.05 else "?", x + 30, yy, 56, DISPLAY, INK if full > 0.05 else GREY_D)
    yy += 66
    if stars and full > 0.05:
        for k in range(5):
            star_(c, x + 50 + k * 50, yy - 16, 20, GOLD)
        text(c, "Farm · Pick your own", x + 300, yy, 40, BODYM, GREY_D)
    yy += 70
    rows = [("Open", "Sat–Sun 9–5", LEAF), ("Call", "(555) 014-2021", SKY), ("Book", "Website", TOMATO)]
    for i, (k, v, col) in enumerate(rows):
        a = ease_out(prog(t, start + 0.6 + i * 0.3, 0.5)) if full > 0.05 else 1
        c.push_group()
        if full > 0.05:
            box(c, x + 30, yy - 40, 120, 54, 27, col, 4, shading=0)
            text(c, k, x + 90, yy - 2, 36, BODY, PAPER, "center")
            text(c, v, x + 170, yy, 42, BODYM, INK)
        else:
            box(c, x + 30, yy - 40, 120, 54, 27, hx("e6e2db"), 3, shading=0)
            text(c, "—", x + 170, yy, 42, BODYM, GREY)
        c.pop_group_to_source(); c.paint_with_alpha(a)
        yy += 70
    return h


def star_(c, x, y, r, col):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    fill_ink(c, lambda: poly(c, pts), col, 3, shading=0)


def padlock(c, x, y, s=1.0, t=0.0, wobble=0.0, open_=0.0):
    c.save(); c.translate(x, y); c.rotate(math.sin(t * 9) * wobble * 0.15); c.scale(s, s)
    c.move_to(-34, -40); c.line_to(-34, -70)
    c.arc(0, -70 - open_ * 24, 34, math.pi, 2 * math.pi)
    c.line_to(34, -40 if open_ < 0.5 else -70)
    setc(c, INK); c.set_line_width(22); c.stroke()
    c.move_to(-34, -40); c.line_to(-34, -70); c.arc(0, -70 - open_ * 24, 34, math.pi, 2 * math.pi)
    c.line_to(34, -40 if open_ < 0.5 else -70)
    setc(c, hx("a9b3c9")); c.set_line_width(12); c.stroke()
    box(c, -56, -50, 112, 96, 18, GOLD, 6)
    circle(c, 0, -10, 12, INK, 0, shading=0)
    c.rectangle(-4, -6, 8, 26); setc(c, INK); c.fill()
    c.restore()


# ---------------------------------------------------------------- settings
def country_road(c, t, seed=5, tod="day", sign_txt="FARM", faded=True, car_p=None):
    season_bg(c, "summer", t, tod=tod, seed=seed, layers=(0, 1, 2))
    c.move_to(-50, 1080); c.curve_to(600, 900, 1300, 860, 1980, 800)
    c.line_to(1980, 900); c.curve_to(1300, 960, 700, 1000, 300, 1100); c.close_path()
    setc(c, hx("cdbf9f")); c.fill()
    for i in range(8):
        tree(c, 1450 + i * 70, 760 - i * 4, 0.55, "leafy", t, seed=i + seed)
    fence(c, -20, 700, 870, 0.75)
    c.save(); c.translate(560, 900); c.rotate(-0.06)
    sign(c, 0, 0, sign_txt, 66, hx("e7d9b8") if faded else CREAM, 1.2)
    c.restore()
    if car_p is not None and 0 < car_p < 1:
        car(c, lerp(-300, 2200, car_p), 1010 - car_p * 120, 0.9, SKY, t, moving=1.0)


def kitchen_bg(c, t, night=True):
    g = cairo.LinearGradient(0, 0, 0, H)
    if night:
        g.add_color_stop_rgba(0, *hx("e8c99a")); g.add_color_stop_rgba(1, *hx("caa070"))
    else:
        g.add_color_stop_rgba(0, *hx("f6e3be")); g.add_color_stop_rgba(1, *hx("e6c99a"))
    c.set_source(g); c.paint()
    for i in range(0, W, 90):
        c.rectangle(i, 0, 40, 820); setc(c, hx("000000"), 0.04); c.fill()
    # window with night sky
    box(c, 1350, 150, 420, 330, 18, hx("1b2a6b") if night else hx("8cc4f0"), 10, shading=0)
    if night:
        for k in range(12):
            r = rng_for("st", k)
            circle(c, 1380 + r.uniform(0, 360), 180 + r.uniform(0, 260), 3, hx("fff1c4"), 0, shading=0)
    stroke(c, lambda: (c.move_to(1560, 150), c.line_to(1560, 480), c.move_to(1350, 315), c.line_to(1770, 315)), WOOD, 12)
    # lamp
    stroke(c, lambda: (c.move_to(700, 0), c.line_to(700, 160)), INK, 5)
    fill_ink(c, lambda: poly(c, [(620, 230), (780, 230), (740, 160), (660, 160)]), GOLD, 5)
    glow(c, 700, 260, 360, GOLD, 0.35 if night else 0.1)
    # table
    box(c, 120, 820, 1680, 54, 14, WOOD, 7)
    box(c, 0, 874, W, 210, 0, hx("a07a52"), 0, shading=0)


def sofa_family(c, x, y, s, t, phone_on=1.0, seed=10):
    c.save(); c.translate(x, y); c.scale(s, s)
    fill_ink(c, lambda: rrect(c, -380, -260, 760, 200, 60), hx("5f7fc9"))
    fill_ink(c, lambda: rrect(c, -420, -120, 840, 140, 50), hx("6f8fd9"))
    for i, (dx, kid) in enumerate(((-210, False), (-40, True), (130, False))):
        person(c, dx, -40, 0.62, t, seed=seed + i, kid=kid)
    # phone held by middle person
    c.save(); c.translate(-30, -300)
    box(c, -40, -70, 80, 140, 16, NAVY, 5, shading=0)
    glow(c, 0, 0, 120, hx("bfe3ff"), 0.6 * phone_on)
    box(c, -30, -56, 60, 110, 8, hx("eaf6ff"), 0, shading=0)
    c.restore()
    c.restore()


def dairy_farm(c, t, cows=6, seed=21, tod="day", store=False, bottles=False):
    season_bg(c, "spring", t, tod=tod, seed=seed, layers=(0, 1, 2, 3))
    barn(c, 1520, 820, 1.25, col=TOMATO)
    tree(c, 1180, 800, 0.9, "leafy", t, seed=3)
    fence(c, -20, 1300, 880, 0.85)
    r = rng_for("cows", seed)
    for i in range(min(cows, 4)):
        cx = 180 + i * 340 + r.uniform(-15, 15)
        jersey(c, cx, 960 + (i % 2) * 50, 0.85, t, flip=(i % 2 == 1), seed=i)
    if store:
        country_store(c, 1520, 980, 0.9, t)


def country_store(c, x, y, s, t, lit=1.0, bell=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shadow(c, 0, 6, 300, 26, 0.2)
    if lit:
        glow(c, 0, -200, 340, GOLD, 0.35 * lit)
    fill_ink(c, lambda: rrect(c, -260, -330, 520, 330, 10), CREAM)
    fill_ink(c, lambda: poly(c, [(-300, -320), (0, -470), (300, -320)]), hx("7a3b2a"))
    # awning
    for k in range(8):
        col = TOMATO if k % 2 == 0 else PAPER
        fill_ink(c, lambda: poly(c, [(-280 + k * 70, -300), (-210 + k * 70, -300), (-210 + k * 70, -250),
                                     (-245 + k * 70, -230), (-280 + k * 70, -250)]), col, 4, shading=0)
    box(c, -200, -230, 150, 160, 10, hx("ffe6a3") if lit else hx("9fb6d6"), 5, shading=0)
    box(c, 40, -230, 120, 230, 10, hx("8a5a3a"), 5)
    circle(c, 140, -110, 8, GOLD, 3)
    box(c, -150, -420, 300, 70, 14, PAPER, 5, shading=0)
    text(c, "COUNTRY STORE", 0, -372, 38, DISPLAY, INK, "center")
    # bell
    c.save(); c.translate(100, -232); c.rotate(math.sin(t * 10) * bell * 0.5)
    fill_ink(c, lambda: (c.move_to(-14, 22), c.curve_to(-14, -4, 14, -4, 14, 22), c.close_path()), GOLD, 3)
    c.restore()
    c.restore()


def milk_bottle(c, x, y, s=1.0, fill=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    fill_ink(c, lambda: smooth(c, [(-26, 0), (-28, -70), (-14, -100), (-14, -130), (14, -130), (14, -100), (28, -70),
                                   (26, 0)]), hx("eef6ff"), 4, shading=0.05)
    if fill > 0:
        c.save(); rrect(c, -24, -70 * fill, 48, 70 * fill, 6); c.clip()
        smooth(c, [(-26, 0), (-28, -70), (-14, -100), (-14, -130), (14, -130), (14, -100), (28, -70), (26, 0)])
        setc(c, WHITE); c.fill(); c.restore()
    box(c, -16, -142, 32, 16, 4, LEAF, 3, shading=0)
    c.restore()


def city_street(c, t, closed_p, n=5):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, *hx("17287a")); g.add_color_stop_rgba(1, *hx("4b4f9a"))
    c.set_source(g); c.paint()
    for k in range(30):
        r = rng_for("cs", k)
        circle(c, r.uniform(0, W), r.uniform(0, 300), 2.5, hx("fff1c4"), 0, shading=0)
    cols = [hx("c9876a"), hx("8f9fc9"), hx("d7b46a"), hx("9fc98f"), hx("c98fb4")]
    for i in range(n):
        x = 40 + i * 372
        hgt = 520 + (i % 2) * 120
        fill_ink(c, lambda: rrect(c, x, 900 - hgt, 340, hgt, 6), cols[i % len(cols)])
        for wy in range(int(900 - hgt + 40), 600, 90):
            for wx in (x + 40, x + 140, x + 240):
                box(c, wx, wy, 60, 50, 6, hx("ffe6a3") if (i + wy // 90) % 3 else hx("5a6aa8"), 3, shading=0)
        # restaurant door + sign
        box(c, x + 110, 720, 120, 180, 8, hx("6b4226"), 5)
        p = clamp((closed_p * n - i))
        cs = ease_back(p) if p > 0 else 0
        if cs > 0:
            c.save(); c.translate(x + 170, 790); c.scale(cs, cs)
            box(c, -70, -26, 140, 52, 8, TOMATO, 4)
            text(c, "CLOSED", 0, 14, 32, DISPLAY, PAPER, "center")
            c.restore()
        box(c, x + 40, 650, 260, 50, 10, CREAM, 4, shading=0)
        text(c, ["DINER", "CAFE", "BISTRO", "COFFEE", "GRILL"][i % 5], x + 170, 688, 34, DISPLAY, INK, "center")
    c.rectangle(0, 900, W, 180); setc(c, hx("3b3f6a")); c.fill()
    for k in range(8):
        c.rectangle(k * 260 + 40, 990, 140, 14); setc(c, hx("f2d36a"), 0.8); c.fill()


def bar_chart(c, x, y, bars, t, starts, maxh=420, bw=220, gap=80, label_size=46):
    """bars: list of (label, value 0..100, colour)."""
    base = y
    stroke(c, lambda: (c.move_to(x - 30, base), c.line_to(x + len(bars) * (bw + gap), base)), INK, 6)
    for i, ((lab, v, col), st) in enumerate(zip(bars, starts)):
        bx = x + i * (bw + gap)
        vv = countup(v, t, st, 1.6)
        hh = maxh * vv / 100
        if hh > 2:
            box(c, bx, base - hh, bw, hh, 16, col, 6)
            text(c, f"{vv:.0f}%", bx + bw / 2, base - hh - 24, 70, DISPLAY, INK, "center")
        a = ease_out(prog(t, st, 0.6))
        if a > 0:
            for li, part in enumerate(lab.split("\n")):
                text(c, part, bx + bw / 2, base + 62 + li * 52, label_size, BODY, INK, "center", alpha=a)


def blueprint_cover(c, x, y, s, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    shadow(c, 0, 410, 220, 22, 0.25)
    fill_ink(c, lambda: rrect(c, -230, -400, 460, 800, 20), hx("1b3f8a"))
    for gx in range(-210, 230, 40):
        c.move_to(gx, -380); c.line_to(gx, 380); setc(c, WHITE, 0.12); c.set_line_width(2); c.stroke()
    for gy in range(-380, 400, 40):
        c.move_to(-210, gy); c.line_to(210, gy); setc(c, WHITE, 0.12); c.set_line_width(2); c.stroke()
    text(c, "THE", 0, -270, 50, DISPLAY, GOLD, "center")
    text(c, "21-POINT", 0, -190, 84, DISPLAY, PAPER, "center")
    text(c, "AGRITOURISM", 0, -110, 52, DISPLAY, PAPER, "center")
    text(c, "BLUEPRINT", 0, -40, 72, DISPLAY, GOLD, "center")
    gate(c, -110, 250, 0.55)
    fence(c, -10, 200, 250, 0.5)
    text(c, "Stephen Loke", 0, 350, 38, BODY, PAPER, "center")
    c.restore()


def ebook_cover(c, x, y, s, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    shadow(c, 0, 410, 220, 22, 0.25)
    fill_ink(c, lambda: rrect(c, -230, -400, 460, 800, 20), LEAF)
    text(c, "150 WAYS", 0, -230, 88, DISPLAY, PAPER, "center")
    text(c, "to Unlock", 0, -150, 50, BODY, CREAM, "center")
    text(c, "Hidden Wealth", 0, -90, 58, DISPLAY, GOLD, "center")
    text(c, "From Your Farm", 0, -30, 50, BODY, CREAM, "center")
    barn(c, 0, 240, 0.6)
    text(c, "FREE EBOOK", 0, 350, 40, DISPLAY, PAPER, "center")
    c.restore()


def chapter_card(c, t, S, title_s, col_key):
    cols = {"tomato": hx("c4553c"), "barn": hx("9c3b2a"), "sky": SKY, "leaf": hx("2f7f2c"), "gold": hx("d99a1f")}
    col = cols[col_key]
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, *tint(col, 0.15)); g.add_color_stop_rgba(1, *shade(col, 0.15))
    c.set_source(g); c.paint()
    # soft field silhouette
    c.move_to(0, 900)
    for k in range(9):
        c.line_to(k * 240, 880 + math.sin(k * 1.3 + t * 0.3) * 30)
    c.line_to(W, H); c.line_to(0, H); c.close_path()
    setc(c, shade(col, 0.3), 0.5); c.fill()
    gate(c, 260, 980, 0.9, open_=0.25 * ease(prog(t, 0.2, 1.2)))
    title(c, title_s, W / 2, 520, t, 0.1, 120)


JERSEY = hx("c98d52")
JERSEY_D = hx("7a4a2a")


def jersey(c, x, y, s=1.0, t=0.0, flip=False, seed=0, chew=0.0):
    """A Jersey dairy cow, side view. (x,y) = ground between the legs."""
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    shadow(c, 0, 4, 170, 20, 0.2)
    sw = math.sin(t * 1.7 + seed) * 0.12
    # tail
    stroke(c, lambda: (c.move_to(-150, -210), c.curve_to(-185, -170, -180 + sw * 40, -110, -172 + sw * 60, -70)),
           INK, 12)
    stroke(c, lambda: (c.move_to(-150, -210), c.curve_to(-185, -170, -180 + sw * 40, -110, -172 + sw * 60, -70)),
           JERSEY, 6)
    circle(c, -172 + sw * 60, -66, 12, JERSEY_D, 3, shading=0)
    # legs
    for lx in (-110, -70, 70, 110):
        fill_ink(c, lambda: rrect(c, lx - 14, -120, 28, 116, 10), shade(JERSEY, 0.08), 5)
        fill_ink(c, lambda: rrect(c, lx - 16, -18, 32, 20, 6), INK, 3, shading=0)
    # udder
    fill_ink(c, lambda: smooth(c, [(-70, -116), (-30, -116), (-26, -86), (-50, -76), (-74, -88)]), hx("f2b2a8"), 4)
    # body
    fill_ink(c, lambda: smooth(c, [(-165, -165), (-150, -228), (-80, -250), (40, -248), (128, -238), (162, -190),
                                   (152, -128), (60, -106), (-60, -106), (-150, -122)]), JERSEY)
    # hip bone and darker shading on the back
    stroke(c, lambda: (c.move_to(-120, -236), c.curve_to(-100, -250, -60, -252, -30, -248)), shade(JERSEY, 0.25), 4)
    # head
    c.save(); c.translate(160, -215); c.rotate(0.2 + math.sin(t * 0.8 + seed) * 0.04); c.scale(1.25, 1.25)
    fill_ink(c, lambda: smooth(c, [(-20, -30), (40, -40), (78, 10), (74, 60), (40, 70), (10, 40), (-14, 10)]),
             mix(JERSEY, JERSEY_D, 0.45))
    # ears and small horns
    fill_ink(c, lambda: smooth(c, [(0, -26), (-36, -44), (-30, -20)]), JERSEY_D, 4)
    fill_ink(c, lambda: poly(c, [(18, -36), (14, -58), (28, -40)]), CREAM, 3, shading=0)
    # white muzzle ring + dark nose
    oval(c, 66, 50, 24, 20, hx("f4ead8"), 4, shading=0)
    oval(c, 70, 54, 16, 12, INK, 0, shading=0)
    circle(c, 66, 52, 3, hx("5a5a5a"), 0, shading=0)
    # eye with lashes
    oval(c, 34, 4, 8, 10, INK, 0, shading=0)
    circle(c, 36, 1, 2.5, WHITE, 0, shading=0)
    c.restore()
    c.restore()
