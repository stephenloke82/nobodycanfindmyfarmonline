"""All scenes of video 008, one function per beat of script/video-008-script.md."""
import math
import cairo
from gfx import *
from chars import person, cow, goat, chicken, dog, SKINS, HAIR, COATS
from props import gate, barn, house, tree, fence, car, sign, table, hay_bale, calendar, bucket
from sets import season_bg, weather
from common import SCENES, scene
from kit008 import *


# ---------------------------------------------------------------- shared shots
def farm(c, t, seed=2, tod="day", gate_open=0.0, season="summer"):
    season_bg(c, season, t, tod=tod, seed=seed)
    barn(c, 1560, 820, 1.15)
    tree(c, 1250, 800, 0.85, "leafy", t, seed=4)
    fence(c, -20, 520, 880, 0.85)
    gate(c, 560, 890, 0.9, open_=gate_open)
    fence(c, 860, 1330, 880, 0.85)


def host_scene(c, t, S, lines, starts=None, bg=None, pose="present", sx=360, s=1.0, cx=820, cy=230, size=66,
               anchor="tl", **kw):
    (bg or farm)(c, t)
    SAR(c, S, t, sx, 1010, s, pose=pose, **kw)
    if lines:
        st = starts or [P(S, i) for i in range(len(lines))]
        card(c, lines, cx, cy, t, st, size=size, anchor=anchor, maxw=1060)


def soft_bg(c, t, col=CREAM):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, *tint(col, 0.3)); g.add_color_stop_rgba(1, *col)
    c.set_source(g); c.paint()
    r = rng_for("dots", 1)
    for k in range(60):
        circle(c, r.uniform(0, W), r.uniform(0, H), 5, shade(col, 0.08), 0, shading=0)


def chapter(c, t, S):
    if S.chapter and t < 1.6:
        chapter_card(c, t, S, *S.chapter)
        return True
    return False


def with_chapter(fn):
    """Show the chapter card for the first moments, then cut straight to the scene."""
    def wrap(c, t, S):
        if S.chapter and t < 1.7:
            chapter_card(c, t, S, *S.chapter)
            return
        fn(c, t, S)
        if S.step:
            tracker3(c, S.step, t)
    return wrap


def scene2(bid):
    def deco(fn):
        SCENES[bid] = with_chapter(fn)
        return fn
    return deco


def phone_map_screen(ghost=False, full=0.0, pins=True, query=None, qstart=0.0, ghost_sheet_a=0.0):
    def scr(c, sx, sy, sw, sh, t):
        map_bg(c, sx, sy, sw, sh, t, seed=4)
        if query is not None:
            search_bar(c, sx + 20, sy + 20, sw - 40, query, t, qstart, size=34)
        if pins:
            map_pin(c, sx + sw * 0.32, sy + sh * 0.45, 0.7, col=PIN)
            map_pin(c, sx + sw * 0.72, sy + sh * 0.62, 0.7, col=PIN)
            map_pin(c, sx + sw * 0.55, sy + sh * 0.85, 0.75, ghost=True)
            if ghost_sheet_a:
                ghost_sheet(c, sx + sw * 0.55, sy + sh * 0.85 - 20, 0.5, t, ghost_sheet_a)
    return scr


# ================================================================ Section 1: Hook
@scene2("H01")
def H01(c, t, S):
    c.save(); cam(c, t, S.dur, 1.0, 1.08, 560, 760)
    country_road(c, t, tod="sunset", sign_txt="FRESH EGGS", car_p=prog(t, 0.6, 3.2))
    c.restore()
    title(c, "THEY DROVE RIGHT PAST.", W / 2, 200, t, 0.4, 100)


@scene2("H02")
def H02(c, t, S):
    kitchen_bg(c, t, night=True)
    phone_frame(c, 700, 140, 520, 860, phone_map_screen(query="farm near me", qstart=P(S, 0) + 0.3), t)
    ease_text(c, "On a phone.", 1560, 620, 64, t, P(S, 0) + 0.5, DISPLAY, INK, "center")
    ease_text(c, "In a kitchen.", 1560, 710, 64, t, P(S, 1), DISPLAY, INK, "center")


@scene2("H03")
def H03(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    SAR(c, S, t, 300, 1010, 0.95, pose="present")
    card(c, ["National survey of U.S. farms", "that welcome visitors"], 640, 60, t, [P(S, 1), P(S, 1) + 0.3], size=52)
    bar_chart(c, 760, 900, [("Social\nmedia", 87, SKY), ("Word of\nmouth", 85, LEAF)], t,
              [P(S, 2), P(S, 2) + 0.6], maxh=440)


@scene2("H04")
def H04(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    SAR(c, S, t, 300, 1010, 0.95, pose="shrug")
    bar_chart(c, 640, 900, [("Social\nmedia", 87, SKY), ("Word of\nmouth", 85, LEAF), ("Everything\nelse", 45, GREY)],
              t, [-5, -5, P(S, 0)], maxh=440, bw=210, gap=70)
    a = ease_out(prog(t, P(S, 0) + 1.2, 0.8))
    if a > 0:
        y = 900 - 440 * 0.5
        c.save(); c.set_dash([18, 14])
        stroke(c, lambda: (c.move_to(600, y), c.line_to(1500, y)), TOMATO, 6, a)
        c.restore()
        text(c, "half", 1520, y + 16, 48, BODY, TOMATO, alpha=a)
    card(c, ["No other tool:", "fewer than half"], 1380, 80, t, [P(S, 0) + 0.4, P(S, 0) + 0.8], size=56)


@scene2("H05")
def H05(c, t, S):
    farm(c, t, seed=5)
    map_pin(c, 1560, 560, 1.6, drop=prog(t, 0.3, 0.8), glow_=0.5 * ease(prog(t, 1.1, 1)))
    SAR(c, S, t, 330, 1010, 1.0, pose="point")
    card(c, ["Get your farm on", ("Google Maps. Free.", 80, DISPLAY, LEAF)], 640, 90, t, [P(S, 0), P(S, 1)], size=66)


@scene2("H06")
def H06(c, t, S):
    farm(c, t, seed=6)
    SAR(c, S, t, 330, 1010, 1.0, pose="count")
    items = ["Without paying for ads", "Without a website", "Without being good with computers"]
    for i, s in enumerate(items):
        pill(c, s, 1150, 300 + i * 170, t, P(S, i), size=56)


@scene2("H07")
def H07(c, t, S):
    season_bg(c, "summer", t, tod="sunset", seed=7)
    house(c, 1300, 900, 1.4, lit=0.6)
    person(c, 1050, 990, 1.0, t, seed=31, pose=((0.4, 1.9), (0.3, 0.4)))
    a = ease_out(prog(t, P(S, 0) + 0.4, 0.8))
    if a > 0:
        c.push_group()
        for k, (bx, by, r) in enumerate(((990, 640, 14), (950, 590, 20))):
            circle(c, bx, by, r, PAPER, 5)
        oval(c, 640, 380, 380, 190, PAPER, 6)
        text(c, "Who would ever look", 640, 360, 50, BODY, INK, "center")
        text(c, "for a farm like mine?", 640, 425, 50, BODY, INK, "center")
        c.pop_group_to_source(); c.paint_with_alpha(a)


@scene2("H08")
def H08(c, t, S):
    soft_bg(c, t, hx("bcd3f2"))
    house(c, 960, 960, 2.6, col=CREAM, lit=0.5)
    sofa_family(c, 960, 1000, 1.0, t)
    title(c, "Somebody already is.", W / 2, 200, t, P(S, 0), 100)


@scene2("H09")
def H09(c, t, S):
    farm(c, t, seed=8)
    SAR(c, S, t, 220, 800, 0.5, pose="present")
    card(c, ["Why good farms go invisible", "A family dairy, the hard way", "The free fix, in 3 steps"], 640, 70, t,
         [P(S, 1), P(S, 2), P(S, 3)], size=50, minw=640, align="left")
    roadmap(c, 1, t, P(S, 3), y=850)


@scene2("H10")
def H10(c, t, S):
    farm(c, t, seed=8)
    SAR(c, S, t, 1660, 760, 0.62, pose="point_low", look=-0.6)
    roadmap(c, 3, t, -1, y=850, blur_rest=False, gold3=True)
    title(c, "Stay for No. 3", W / 2 - 160, 300, t, P(S, 0), 120, col=GOLD)


@scene2("H11")
def H11(c, t, S):
    farm(c, t, seed=9, gate_open=0.6)
    pose = "wave" if t < P(S, 1) else "finger"
    SAR(c, S, t, 420, 1010, 1.0, pose=pose, wave_amp=0.25 if pose == "wave" else 0)
    card(c, [("I'm Sarah.", 90, DISPLAY, INK), "Agritourism Success", ("by Stephen Loke", 50, BODY, INK)], 900, 90, t,
         [P(S, 0), P(S, 3), P(S, 3) + 0.3], size=60)
    card(c, ["Stephen's farm is featured in", ("Bloomberg News and Asahi Shimbun", 56, DISPLAY, TOMATO)], 900, 560, t,
         [P(S, 4), P(S, 4) + 0.4], size=48)


# ================================================================ Section 2: The ghost pin
@scene2("E01")
def E01(c, t, S):
    farm(c, t, seed=11)
    SAR(c, S, t, 380, 1010, 1.0, pose="hips")
    card(c, ["The enemy isn't you.", ("You're farming right.", 72, DISPLAY, LEAF)], 860, 160, t, [P(S, 1), P(S, 2)],
         size=64)


@scene2("E02")
def E02(c, t, S):
    g = ease(prog(t, P(S, 0) + 0.2, 1.6))
    farm(c, t, seed=12)
    person(c, 900, 1010, 1.05, t, seed=40, pose=((1.2, 0.8), (1.0, 0.9)), hat=GOLD)
    hay_bale(c, 1180, 990, 1.0)
    if g > 0:
        c.set_source_rgba(0.92, 0.91, 0.89, 0.82 * g); c.paint()
    title(c, "The enemy: being invisible", W / 2, 220, t, P(S, 0) + 0.3, 96)


@scene2("E03")
def E03(c, t, S):
    soft_bg(c, t, hx("bcd3f2"))
    sofa_family(c, 520, 1040, 1.05, t)
    phone_frame(c, 1100, 120, 520, 880, phone_map_screen(query="pick your own near me", qstart=P(S, 1) + 0.2,
                                                          pins=t > P(S, 2)), t)


@scene2("E04")
def E04(c, t, S):
    soft_bg(c, t, hx("e9f1df"))
    listing(c, 120, 200, 820, t, full=1.0, start=P(S, 0) + 0.2)
    a = ease_out(prog(t, P(S, 3), 0.7))
    if a > 0:
        c.push_group()
        listing(c, 1000, 200, 820, t, full=0.0, start=0)
        c.pop_group_to_source(); c.paint_with_alpha(a)


@scene2("E05")
def E05(c, t, S):
    soft_bg(c, t, hx("e9f1df"))
    listing(c, 120, 200, 820, t, full=1.0, start=-5)
    listing(c, 1000, 200, 820, t, full=0.0)
    title(c, "Which one would you drive an hour for?", W / 2, 140, t, P(S, 0), 70)


@scene2("E06")
def E06(c, t, S):
    soft_bg(c, t, hx("d9dde6"))
    map_bg(c, 0, 0, W, H, t, seed=9)
    c.set_source_rgba(1, 1, 1, 0.35); c.paint()
    s = 2.2 + 0.1 * ease(t / S.dur)
    map_pin(c, W / 2, 800, s, ghost=True)
    ghost_sheet(c, W / 2, 640, 1.6, t, ease_out(prog(t, P(S, 0) - 0.3, 1.0)))
    title(c, "The ghost pin", W / 2, 180, t, P(S, 0), 110)
    ease_text(c, "Many owners don't know it's there.", W / 2, 1010, 56, t, P(S, 1), BODY, INK, "center")


@scene2("E07")
def E07(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    SAR(c, S, t, 300, 1010, 0.95, pose="present")
    a1 = ease_out(prog(t, P(S, 0), 0.6))
    a2 = ease_out(prog(t, P(S, 1), 0.6))
    if a1 > 0:
        c.push_group(); box(c, 620, 300, 560, 420, 30, hx("e6e2db"), 6)
        gate(c, 780, 610, 0.7)
        text(c, "One gate:", 900, 380, 54, DISPLAY, GREY_D, "center")
        text(c, "the road", 900, 690, 50, BODY, GREY_D, "center")
        c.pop_group_to_source(); c.paint_with_alpha(a1 * 0.9)
    if a2 > 0:
        c.push_group(); box(c, 1240, 300, 600, 420, 30, hx("dff0d4"), 6)
        gate(c, 1330, 610, 0.6, open_=0.5)
        box(c, 1600, 450, 110, 190, 22, NAVY, 5); box(c, 1612, 470, 86, 150, 10, hx("eaf6ff"), 0, shading=0)
        text(c, "Two gates:", 1540, 380, 54, DISPLAY, LEAF, "center")
        text(c, "the road + the phone", 1540, 690, 46, BODY, INK, "center")
        c.pop_group_to_source(); c.paint_with_alpha(a2)


@scene2("E08")
def E08(c, t, S):
    c.save(); cam(c, t, S.dur, 1.0, 1.06, 700, 800)
    season_bg(c, "summer", t, tod="sunset", seed=13)
    barn(c, 1500, 820, 1.1)
    fence(c, -20, 560, 900, 0.95)
    gate(c, 600, 920, 1.1, open_=ease(prog(t, 0.4, 2.0)))
    fence(c, 990, 1400, 900, 0.95)
    c.restore()
    card(c, [("Gate 1: the road", 70, DISPLAY, INK)], 120, 80, t, [P(S, 0)], size=60)


def phone_gate(c, x, y, s, t, lock=1.0, wobble=0.0, open_p=0.0, screen_full=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    glow(c, 0, -300, 320, hx("bfe3ff"), 0.45)
    box(c, -170, -600, 340, 600, 46, NAVY, 7)
    c.save(); rrect(c, -150, -540, 300, 480, 16); c.clip()
    if screen_full > 0:
        setc(c, PAPER); c.paint()
        map_bg(c, -150, -540, 300, 480, t, seed=2)
        map_pin(c, 0, -230, 0.9, glow_=0.5 * screen_full)
    else:
        map_bg(c, -150, -540, 300, 480, t, seed=2)
        map_pin(c, 0, -230, 0.9, ghost=True)
    c.restore()
    # gate bars across the phone
    if open_p < 1:
        c.push_group()
        for k in range(4):
            yy = -470 + k * 120
            box(c, -150 - open_p * 140, yy, 300 * (1 - open_p * 0.6), 22, 8, WOOD, 4, shading=0)
        c.pop_group_to_source(); c.paint_with_alpha(1 - open_p)
    if lock > 0:
        padlock(c, 0, -220, 1.2 * lock, t, wobble)
    c.restore()


@scene2("E09")
def E09(c, t, S):
    kitchen_bg(c, t, night=False)
    phone_gate(c, 1000, 960, 1.15, t, lock=0.0)
    card(c, [("Gate 2: the phone", 70, DISPLAY, INK), ("40 miles away", 50, BODY, TOMATO)], 120, 80, t,
         [P(S, 0), P(S, 1)], size=60)
    ease_text(c, "Where people decide", 1560, 620, 60, t, P(S, 2), DISPLAY, INK, "center")


@scene2("E10")
def E10(c, t, S):
    farm(c, t, seed=14, gate_open=1.0)
    phone_gate(c, 1580, 980, 0.95, t, lock=ease_back(prog(t, P(S, 0) + 0.8, 0.7)))
    SAR(c, S, t, 960, 1010, 0.8, pose="shrug")
    card(c, ["Gate 1: open", ("Gate 2: locked", 64, DISPLAY, TOMATO)], 80, 70, t, [P(S, 0), P(S, 0) + 0.9], size=60)


@scene2("E11")
def E11(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    phone_gate(c, 1460, 1000, 1.1, t, lock=1.0, wobble=1.0)
    title(c, "THE SECOND GATE", 700, 380, t, P(S, 0), 120, col=GOLD)
    ease_text(c, "Opening it is free.", 700, 520, 72, t, P(S, 1), DISPLAY, LEAF, "center")
    SAR(c, S, t, 560, 1060, 0.7, pose="present")


def tiles3(c, t, starts, grey_mid=0.0, y=380):
    labs = [("Relevance", "How well you match"), ("Distance", "How far away"), ("Prominence", "How well known")]
    for i, ((a_, b_), st) in enumerate(zip(labs, starts)):
        a = ease_out(prog(t, st, 0.6))
        if a <= 0:
            continue
        x = 260 + i * 480
        grey = grey_mid if i == 1 else 0
        col = mix(hx("dff0d4") if grey_mid > 0 and i != 1 else PAPER, hx("d8d4cf"), grey)
        c.push_group()
        box(c, x, y + (1 - a) * 20, 420, 360, 30, col, 6)
        text(c, a_, x + 210, y + 150, 66, DISPLAY, mix(INK, GREY_D, grey), "center")
        text(c, b_, x + 210, y + 240, 44, BODY, mix(INK, GREY_D, grey), "center")
        if grey_mid > 0 and i != 1:
            circle(c, x + 210, y + 310, 30 * grey_mid, LEAF, 4, shading=0)
        c.pop_group_to_source(); c.paint_with_alpha(a)


def dotgrid(c, t):
    setc(c, hx("f6efdf")); c.paint()
    for x in range(30, W, 60):
        for y in range(30, H, 60):
            circle(c, x, y, 3, hx("e0d6c0"), 0, shading=0)


@scene2("E12")
def E12(c, t, S):
    dotgrid(c, t)
    card(c, ["Google: local results rest on 3 things"], W / 2, 90, t, [P(S, 0)], size=56, anchor="tc")
    tiles3(c, t, [P(S, 1), P(S, 2), P(S, 3)])
    text(c, "Source: Google Business Profile Help", W / 2, 1010, 34, BODYM, GREY_D, "center",
         alpha=ease_out(prog(t, P(S, 1), 0.6)))


@scene2("E13")
def E13(c, t, S):
    dotgrid(c, t)
    tiles3(c, t, [-5, -5, -5], grey_mid=ease(prog(t, P(S, 0), 1.0)), y=300)
    SAR(c, S, t, 1700, 1080, 0.55, pose="thumb")
    ease_text(c, "You can't move your farm.", 760, 840, 60, t, P(S, 0), BODY, GREY_D, "center")
    ease_text(c, "The other two are in your hands.", 760, 940, 64, t, P(S, 1), DISPLAY, LEAF, "center")


# ================================================================ Section 3: Milk in the field
@scene2("K01")
def K01(c, t, S):
    c.save(); cam(c, t, S.dur, 1.0, 1.05, 900, 800)
    dairy_farm(c, t, cows=5, seed=21)
    c.restore()
    card(c, [("Fairbury, Illinois", 70, DISPLAY, INK), ("1958", 64, DISPLAY, TOMATO)], 80, 70, t,
         [P(S, 0), P(S, 1)], size=60)
    card(c, ["Duane and Arlene Kilgus", "start a dairy"], 1240, 70, t, [P(S, 2), P(S, 2) + 0.4], size=50)


@scene2("K02")
def K02(c, t, S):
    season_bg(c, "spring", t, seed=22)
    # co-op building
    fill_ink(c, lambda: rrect(c, 1300, 520, 520, 380, 10), hx("b9c2cf"))
    box(c, 1400, 560, 320, 80, 12, PAPER, 5)
    text(c, "CO-OP", 1560, 620, 60, DISPLAY, INK, "center")
    box(c, 1480, 720, 160, 180, 6, hx("7a8798"), 5)
    # milk truck
    p = ease(prog(t, 0.4, 3.2))
    tx = lerp(200, 1180, p)
    c.save(); c.translate(tx, 940)
    shadow(c, 0, 10, 200, 20, 0.2)
    box(c, -220, -170, 300, 160, 20, PAPER, 6); text(c, "MILK", -70, -70, 54, DISPLAY, SKY, "center")
    box(c, 80, -130, 120, 120, 16, SKY, 6)
    for wx in (-160, 40, 150):
        circle(c, wx, 0, 34, INK, 4, shading=0); circle(c, wx, 0, 14, GREY, 0, shading=0)
    c.restore()
    card(c, [("30+ years", 70, DISPLAY, INK), "co-op prices"], 80, 70, t, [P(S, 0), P(S, 2)], size=60)


@scene2("K03")
def K03(c, t, S):
    soft_bg(c, t, hx("e6f1fb"))
    # conveyor
    box(c, 80, 760, 1760, 40, 20, GREY_D, 5)
    for k in range(12):
        circle(c, 140 + k * 150, 820, 18, GREY, 4, shading=0)
    off = (t * 120) % 200
    for k in range(10):
        x = -100 + k * 200 + off
        if 60 < x < 1860:
            fillp = clamp((x - 600) / 300)
            milk_bottle(c, x, 760, 1.4, fillp)
    # filler
    box(c, 640, 380, 220, 220, 20, hx("a9b3c9"), 6)
    stroke(c, lambda: (c.move_to(750, 600), c.line_to(750, 660)), INK, 14)
    stroke(c, lambda: (c.move_to(750, 600), c.line_to(750, 660)), hx("d0d6e2"), 8)
    card(c, [("Bottled on the farm", 72, DISPLAY, LEAF), "Their own Jersey milk"], 1000, 120, t,
         [P(S, 2), P(S, 3)], size=56)


def illinois_map(c, x, y, s, t, zoom_p):
    """Simple Illinois outline with Chicago and Fairbury, pin one mile south of town."""
    pts = [(0, 0), (60, -4), (66, 20), (70, 120), (80, 200), (70, 260), (40, 300), (20, 270), (-6, 200), (-20, 120),
           (-10, 40)]
    c.save(); c.translate(x, y); c.scale(s, s)
    fill_ink(c, lambda: smooth(c, pts), hx("cfe3b0"), 4 / s * 1.0, shading=0.08)
    circle(c, 62, 30, 9, NAVY, 2, shading=0)
    text(c, "Chicago", 78, 38, 22, BODY, INK)
    circle(c, 38, 108, 7, TOMATO, 2, shading=0)
    text(c, "Fairbury", -48, 104, 20, BODY, INK)
    c.restore()


@scene2("K04")
def K04(c, t, S):
    soft_bg(c, t, hx("e6f1fb"))
    illinois_map(c, 360, 140, 2.6, t, 0)
    # route Chicago <- Fairbury
    a = ease(prog(t, P(S, 0), 1.6))
    if a > 0:
        x0, y0 = 360 + 38 * 2.6, 140 + 108 * 2.6
        x1, y1 = 360 + 62 * 2.6, 140 + 30 * 2.6
        c.save(); c.set_dash([16, 12])
        stroke(c, lambda: (c.move_to(x0, y0), c.line_to(lerp(x0, x1, a), lerp(y0, y1, a))), TOMATO, 6)
        c.restore()
    card(c, ["Stores, restaurants", "and coffee shops", "in Chicago"], 860, 90, t,
         [P(S, 0), P(S, 0) + 0.3, P(S, 0) + 0.6], size=52)
    sa = ease_out(prog(t, P(S, 2), 0.8))
    if sa > 0:
        c.push_group()
        country_store(c, 1460, 1000, 0.85, t)
        card(c, [("Country store, 2009", 54, DISPLAY, INK), "a mile south of town"], 1140, 560 - 160, t,
             [P(S, 2), P(S, 4)], size=44)
        c.pop_group_to_source(); c.paint_with_alpha(sa)


@scene2("K05")
def K05(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    # tear-off calendar
    box(c, 660, 200, 600, 640, 24, PAPER, 7)
    box(c, 660, 200, 600, 120, 24, TOMATO, 7)
    p = ease(prog(t, P(S, 0) - 0.2, 0.9))
    text(c, "2020" if p > 0.5 else "2019", 960, 290, 80, DISPLAY, PAPER, "center")
    text(c, "SPRING" if p > 0.5 else "WINTER", 960, 600, 120, DISPLAY, INK, "center")
    if 0 < p < 1:
        c.save(); c.translate(960, 840); c.rotate(-p * 0.9)
        box(c, -300, -520 + p * 300, 600, 520, 10, PAPER, 6)
        c.restore()


@scene2("K06")
def K06(c, t, S):
    city_street(c, t, ease(prog(t, P(S, 0), 2.5)))
    card(c, [("About two dozen restaurants", 56, DISPLAY, INK), "Most shut their doors"], 80, 60, t,
         [P(S, 1), P(S, 2)], size=52)


@scene2("K07")
def K07(c, t, S):
    season_bg(c, "spring", t, seed=23)
    fence(c, -20, W + 20, 760, 0.8)
    n_show = int(round(lerp(10, 7.7, ease(prog(t, P(S, 0) + 0.6, 2.0)))))
    for i in range(10):
        a = 1.0 if i < n_show else 0.22
        c.push_group()
        jersey(c, 200 + (i % 5) * 380, 880 + (i // 5) * 170, 0.72, t, flip=bool(i % 2), seed=i)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    v = lerp(150, 115, ease(prog(t, P(S, 0) + 0.6, 2.0)))
    card(c, [(f"{v:.0f} cows", 96, DISPLAY, INK)], 80, 60, t, [P(S, 0)], size=60)
    ease_text(c, "Still not enough.", W - 120, 160, 60, t, P(S, 2), DISPLAY, TOMATO, "right")


@scene2("K08")
def K08(c, t, S):
    c.save(); cam(c, t, S.dur, 1.0, 1.12, 960, 700)
    season_bg(c, "spring", t, seed=24, layers=(0, 1, 2, 3))
    # churn tipping and milk pouring
    c.save(); c.translate(800, 760); c.rotate(-0.9 * ease(prog(t, 0.3, 1.2)))
    box(c, -90, -260, 180, 260, 40, hx("c9d1df"), 7)
    box(c, -60, -300, 120, 50, 16, hx("b3bccb"), 6)
    c.restore()
    pr = ease(prog(t, 1.0, 2.0))
    if pr > 0:
        c.move_to(560, 560); c.curve_to(600, 700, 640, 860, 700, 950)
        setc(c, WHITE, 0.95); c.set_line_width(34 * pr); c.stroke()
        oval(c, 760, 960, 260 * pr, 50 * pr, WHITE, 4, shading=0.05)
    c.restore()


@scene2("K09")
def K09(c, t, S):
    season_bg(c, "spring", t, seed=25)
    country_store(c, 960, 1000, 1.25, t, lit=1.0, bell=math.exp(-max(0, t - 0.5) * 1.5))
    card(c, [("The country store", 64, DISPLAY, INK), "kept going"], 80, 60, t, [P(S, 0), P(S, 1)], size=56)


@scene2("K10")
def K10(c, t, S):
    season_bg(c, "spring", t, seed=26)
    country_store(c, 1350, 1000, 1.05, t, lit=1.0)
    for i in range(6):
        st = 0.3 + i * 0.9
        x = lerp(-120, 1300, clamp((t - st) / 5.0))
        if -100 < x < 1280:
            person(c, x, 1010, 0.75, t, seed=50 + i, kid=(i % 3 == 1), walk=t * 6 + i)
    card(c, ["More people came", "through its door"], 80, 60, t, [P(S, 0), P(S, 0) + 0.3], size=56)


@scene2("K11")
def K11(c, t, S):
    season_bg(c, "spring", t, seed=27)
    c.move_to(-20, 900); c.line_to(W + 20, 860); setc(c, hx("b9b0a0")); c.set_line_width(80); c.stroke()
    # stopped truck
    c.save(); c.translate(380, 900)
    box(c, -220, -170, 300, 160, 20, PAPER, 6); text(c, "MILK", -70, -70, 54, DISPLAY, GREY, "center")
    box(c, 80, -130, 120, 120, 16, GREY, 6)
    for wx in (-160, 40, 150):
        circle(c, wx, 0, 34, INK, 4, shading=0)
    c.restore()
    country_store(c, 1420, 1040, 0.85, t)
    gate(c, 1020, 1050, 0.75, open_=1.0)
    title(c, "The trucks stopped.", 620, 230, t, P(S, 1), 84)
    title(c, "The gate stayed open.", 1280, 380, t, P(S, 2), 84, col=GOLD)


@scene2("K12")
def K12(c, t, S):
    season_bg(c, "spring", t, seed=28)
    country_store(c, 1450, 1000, 0.9, t)
    SAR(c, S, t, 520, 1010, 1.0, pose="finger")
    card(c, ["Don't get found", "in the crisis.", ("Get found before it.", 66, DISPLAY, LEAF)], 860, 90, t,
         [P(S, 1), P(S, 1) + 0.3, P(S, 2)], size=60)


@scene2("K13")
def K13(c, t, S):
    season_bg(c, "spring", t, seed=28)
    country_store(c, 1450, 1000, 0.9, t)
    SAR(c, S, t, 420, 1010, 1.0, pose="present")
    a = ease_out(prog(t, 0.2, 0.7))
    if a > 0:
        c.push_group()
        box(c, 720, 640, 1100, 280, 30, PAPER, 6)
        blueprint_cover(c, 850, 780, 0.3, t)
        text(c, "21-Point Blueprint", 980, 740, 64, DISPLAY, INK)
        text(c, "Free · Link in the description", 980, 830, 48, BODY, LEAF)
        c.pop_group_to_source(); c.paint_with_alpha(a)


@scene2("K14")
def K14(c, t, S):
    season_bg(c, "spring", t, seed=28)
    country_store(c, 1450, 1000, 0.9, t)
    SAR(c, S, t, 420, 1010, 1.0, pose="point")
    a = ease_back(prog(t, P(S, 0) + 0.3, 0.6))
    if a > 0:
        c.save(); c.translate(1000, 400); c.scale(a, a)
        box(c, -240, -70, 480, 140, 70, TOMATO, 6)
        text(c, "Subscribe", 20, 24, 64, DISPLAY, PAPER, "center")
        c.save(); c.translate(-170, 0)
        fill_ink(c, lambda: (c.move_to(-24, 20), c.curve_to(-24, -30, 24, -30, 24, 20), c.close_path()), GOLD, 4)
        c.restore()
        c.restore()


# ================================================================ Section 4: What this is not
@scene2("N01")
def N01(c, t, S):
    soft_bg(c, t, hx("dfe7f6"))
    SAR(c, S, t, 320, 1010, 1.0, pose="hips")
    items = ["Paid ads", "Dancing on TikTok", "An agency bill every month"]
    for i, s in enumerate(items):
        pill(c, s, 1150, 380 + i * 170, t, P(S, 1 + i), size=56, mark="x")
    ease_text(c, "What this is NOT", 1150, 200, 84, t, P(S, 0), DISPLAY, TOMATO, "center")


@scene2("N02")
def N02(c, t, S):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, *hx("2f6f2c")); g.add_color_stop_rgba(1, *hx("1f4f1e"))
    c.set_source(g); c.paint()
    glow(c, W / 2, H / 2, 700, GOLD, 0.25)
    a = ease_out(prog(t, P(S, 0) - 0.2, 0.8))
    text(c, "“No way to request or pay for", W / 2, 420, 72, DISPLAY, PAPER, "center", alpha=a)
    text(c, "a better local ranking.”", W / 2, 520, 72, DISPLAY, GOLD, "center", alpha=a)
    text(c, "Google Business Profile Help", W / 2, 640, 44, BODY, CREAM, "center", alpha=a)
    ease_text(c, "The spot is earned. The tool is free.", W / 2, 860, 60, t, P(S, 1), BODY, PAPER, "center")


@scene2("N03")
def N03(c, t, S):
    farm(c, t, seed=30)
    a = ease_back(prog(t, P(S, 0), 0.7))
    if a > 0:
        c.save(); c.translate(W / 2, 360); c.scale(a, a)
        box(c, -460, -150, 920, 300, 40, PAPER, 7)
        for k, col in enumerate(GOOGLE):
            circle(c, -360 + k * 34, -60, 14, col, 3, shading=0)
        text(c, "Google Business", 40, -20, 76, DISPLAY, INK, "center")
        text(c, "Profile", 40, 70, 76, DISPLAY, LEAF, "center")
        c.restore()
    roadmap(c, 0, t, P(S, 1), y=780, blur_rest=False)


# ================================================================ Section 5: Step 1
@scene2("A01")
def A01(c, t, S):
    farm(c, t, seed=31)
    roadmap(c, 1, t, 0.0, y=440)
    SAR(c, S, t, 1700, 1050, 0.55, pose="point", look=-0.6)


@scene2("A02")
def A02(c, t, S):
    farm(c, t, seed=32)
    SAR(c, S, t, 380, 1010, 1.0, pose="present")

    def scr(c, sx, sy, sw, sh, t):
        map_bg(c, sx, sy, sw, sh, t, seed=6)
        search_bar(c, sx + 20, sy + 20, sw - 40, "Willow Creek Farm", t, P(S, 2) + 0.2, size=34)
    phone_frame(c, 720, 120, 560, 900, scr, t, hand=True)
    for i, s in enumerate(["Take out your phone", "Open Google Maps", "Type your farm's name"]):
        pill(c, s, 1340, 300 + i * 160, t, P(S, i), size=38, anchor="l")


@scene2("A03")
def A03(c, t, S):
    soft_bg(c, t, hx("e9f1df"))

    def scr(c, sx, sy, sw, sh, t):
        map_bg(c, sx, sy, sw, sh, t, seed=6)
        search_bar(c, sx + 20, sy + 20, sw - 40, "Willow Creek Farm", t, -9, size=34)
        map_pin(c, sx + sw / 2, sy + sh * 0.6, 1.0, ghost=True, drop=prog(t, P(S, 1), 0.6))
    phone_frame(c, 140, 120, 560, 900, scr, t)
    qs = ["Is there a pin?", "Right place?", "Right hours?", "Your phone number?"]
    for i, s in enumerate(qs):
        pill(c, s, 820, 260 + i * 170, t, P(S, 1 + i), size=56, anchor="l")
        a = ease_back(prog(t, P(S, 1 + i), 0.5))
        if a > 0:
            text(c, "?", 780 + 0 * i, 280 + i * 170, 90 * a, DISPLAY, TOMATO, "center")


@scene2("A04")
def A04(c, t, S):
    soft_bg(c, t, hx("e9f1df"))
    map_bg(c, 120, 120, 1000, 840, t, seed=8)
    stroke(c, lambda: rrect(c, 120, 120, 1000, 840, 20), INK, 7)
    map_pin(c, 620, 640, 1.4, ghost=True, drop=prog(t, P(S, 0) + 0.5, 0.7))
    # visitor's hand tapping
    a = ease_out(prog(t, P(S, 1), 0.6))
    if a > 0:
        c.push_group()
        fill_ink(c, lambda: smooth(c, [(820, 760), (900, 700), (980, 760), (1020, 980), (860, 1000)]), SKINS[1])
        c.pop_group_to_source(); c.paint_with_alpha(a)
    card(c, ["Google may already", "have a listing", ("You might be on the map", 52, DISPLAY, LEAF)], 1200, 200, t,
         [P(S, 0), P(S, 0) + 0.3, P(S, 2)], size=52)


@scene2("A05")
def A05(c, t, S):
    soft_bg(c, t, hx("e9f1df"))
    map_bg(c, 360, 120, 1200, 760, t, seed=10)
    stroke(c, lambda: rrect(c, 360, 120, 1200, 760, 20), INK, 7)
    c.save(); c.set_dash([14, 12])
    stroke(c, lambda: (c.move_to(960, 560), c.curve_to(946, 534, 914, 514, 914, 482),
                       c.arc(960, 482, 46, math.pi, 2 * math.pi), c.curve_to(1006, 514, 974, 534, 960, 560)), INK, 6)
    c.restore()
    ease_text(c, "No pin? You'll make one in Step 2.", W / 2, 990, 64, t, P(S, 0), DISPLAY, INK, "center")


# ================================================================ Section 6: Step 2
@scene2("B01")
def B01(c, t, S):
    farm(c, t, seed=33)
    roadmap(c, 2, t, 0.0, y=440, done=1)
    SAR(c, S, t, 1700, 1050, 0.55, pose="point", look=-0.6)


def browser(c, x, y, w, h, url, t, body=None):
    shadow(c, x + w / 2, y + h + 10, w * 0.45, 18, 0.2)
    box(c, x, y, w, h, 24, PAPER, 6)
    box(c, x, y, w, 80, 24, hx("e6e2db"), 6, shading=0)
    for k, col in enumerate((TOMATO, GOLD, LEAF)):
        circle(c, x + 40 + k * 36, y + 40, 11, col, 3, shading=0)
    box(c, x + 160, y + 18, w - 200, 44, 22, PAPER, 3, shading=0)
    text(c, url, x + 190, y + 52, 34, BODYM, INK)
    if body:
        body(c, x, y + 80, w, h - 80, t)


@scene2("B02")
def B02(c, t, S):
    soft_bg(c, t, hx("e6f1fb"))

    def body(c, x, y, w, h, t):
        steps = ["Sign in", "Search for your farm", "Claim it", "No listing? Add your farm"]
        for i, s in enumerate(steps):
            st = P(S, 1 + i)
            a = ease_out(prog(t, st, 0.5))
            if a <= 0:
                continue
            yy = y + 90 + i * 130
            c.push_group()
            circle(c, x + 90, yy, 34, LEAF, 4)
            stroke(c, lambda: (c.move_to(x + 74, yy), c.line_to(x + 86, yy + 14), c.line_to(x + 108, yy - 14)), PAPER, 6)
            text(c, s, x + 150, yy + 20, 56, BODY, INK)
            c.pop_group_to_source(); c.paint_with_alpha(a)
    browser(c, 200, 140, 1520, 760, "business.google.com", t, body)
    ease_text(c, "business.google.com", W / 2, 1010, 64, t, P(S, 0), DISPLAY, SKY, "center")


@scene2("B03")
def B03(c, t, S):
    farm(c, t, seed=34)
    SAR(c, S, t, 420, 1010, 1.0, pose="present")
    sw = damp_swing(t - P(S, 0), 0.25, 1.6, 2.0) if t > P(S, 0) else 0
    a = ease_out(prog(t, P(S, 0), 0.5))
    if a > 0:
        c.save(); c.translate(1200, 160); c.rotate(sw)
        stroke(c, lambda: (c.move_to(0, 0), c.line_to(0, 120)), INK, 6)
        c.push_group()
        box(c, -300, 120, 600, 340, 40, WOOD, 7)
        circle(c, 0, 170, 18, PAPER, 4)
        text(c, "FREE", 0, 360, 170, DISPLAY, PAPER, "center", outline=INK, olw=14)
        c.pop_group_to_source(); c.paint_with_alpha(a)
        c.restore()
    ease_text(c, "Not a cent.", 1200, 700, 80, t, P(S, 1), DISPLAY, PAPER, "center", outline=INK, olw=12)


@scene2("B04")
def B04(c, t, S):
    country_road(c, t, seed=8, sign_txt="WILLOW CREEK FARM", faded=False)
    SAR(c, S, t, 1300, 1060, 0.85, pose="slate",
        hold=(1, lambda c, x, y: (box(c, x - 40, y - 110, 80, 140, 14, NAVY, 4),
                                  box(c, x - 30, y - 96, 60, 110, 6, hx("eaf6ff"), 0, shading=0))))
    icons_ = [("Phone", TOMATO), ("Text", SKY), ("Email", GOLD), ("Video", LEAF)]
    for i, (s, col) in enumerate(icons_):
        st = P(S, 1 + i)
        a = ease_back(prog(t, st, 0.5))
        if a > 0:
            x = 300 + i * 380
            c.save(); c.translate(x, 230); c.scale(a, a)
            box(c, -160, -70, 320, 140, 40, col, 6)
            text(c, s, 0, 22, 62, DISPLAY, PAPER, "center")
            c.restore()
    card(c, ["Film your sign, your farm,", "and something only the owner has"], W / 2, 380, t,
         [P(S, 6), P(S, 8)], size=48, anchor="tc")


@scene2("B05")
def B05(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    a1 = ease_out(prog(t, P(S, 1), 0.6))
    a2 = ease_out(prog(t, P(S, 3), 0.6))
    if a1 > 0:
        c.push_group()
        sign(c, 560, 760, "Willow Creek Farm", 60, CREAM, 1.3)
        circle(c, 560, 830, 50, LEAF, 5)
        stroke(c, lambda: (c.move_to(530, 830), c.line_to(552, 852), c.line_to(592, 808)), PAPER, 9)
        c.pop_group_to_source(); c.paint_with_alpha(a1)
    if a2 > 0:
        c.push_group()
        sign(c, 1380, 760, "Best Farm U-Pick Near Me", 44, CREAM, 1.3)
        circle(c, 1380, 830, 50, TOMATO, 5)
        stroke(c, lambda: (c.move_to(1352, 802), c.line_to(1408, 858), c.move_to(1408, 802), c.line_to(1352, 858)),
               PAPER, 9)
        c.pop_group_to_source(); c.paint_with_alpha(a2)
    title(c, "Use your real farm name", W / 2, 180, t, P(S, 0), 96)
    ease_text(c, "Extra keywords can get a listing suspended.", W / 2, 1000, 50, t, P(S, 4), BODY, TOMATO, "center")


# ================================================================ Section 7: Step 3
@scene2("C01")
def C01(c, t, S):
    farm(c, t, seed=35)
    roadmap(c, 3, t, 0.0, y=440, done=2, gold3=True)
    SAR(c, S, t, 1700, 1050, 0.55, pose="point", look=-0.6)
    title(c, "Fill every box.", W / 2, 260, t, P(S, 2), 110, col=GOLD)


@scene2("C02")
def C02(c, t, S):
    farm(c, t, seed=36)
    p = clamp((t - P(S, 1)) / 4.0)
    x = lerp(700, 1900, ease(clamp((t - P(S, 2)) / 3.0)))
    person(c, x, 1010, 0.95, t, seed=41, hat=GOLD, walk=(t * 6 if t > P(S, 2) else None))
    phone_gate(c, 360, 980, 0.8, t, lock=0.0)
    ghost_sheet(c, 360, 720, 0.7, t, ease_out(prog(t, P(S, 3), 0.8)))
    card(c, [("The step most farmers skip", 64, DISPLAY, TOMATO)], 640, 80, t, [P(S, 0)], size=60)


@scene2("C03")
def C03(c, t, S):
    soft_bg(c, t, hx("e9f1df"))
    v1 = countup(2.7, t, P(S, 0) + 0.6, 1.6)
    v2 = countup(70, t, P(S, 1), 1.6)
    for i, (big, small, st) in enumerate(((f"{v1:.1f}x", "more likely to seem reputable", P(S, 0) + 0.4),
                                          (f"{v2:.0f}%", "more likely to visit", P(S, 1)))):
        a = ease_out(prog(t, st, 0.6))
        if a <= 0:
            continue
        x = 220 + i * 780
        c.push_group()
        box(c, x, 300, 700, 460, 40, PAPER, 7)
        text(c, big, x + 350, 560, 200, DISPLAY, LEAF, "center")
        text(c, small, x + 350, 680, 46, BODY, INK, "center")
        c.pop_group_to_source(); c.paint_with_alpha(a)
    card(c, ["Google: when a profile is complete"], W / 2, 90, t, [P(S, 0)], size=54, anchor="tc")
    text(c, "Source: Google Business Profile Help", W / 2, 960, 34, BODYM, GREY_D, "center",
         alpha=ease_out(prog(t, P(S, 0), 0.6)))


def form(c, x, y, w, t, rows):
    """rows: (label, value, start)."""
    box(c, x, y, w, 120 + len(rows) * 150, 30, PAPER, 6)
    text(c, "Edit profile", x + 40, y + 80, 56, DISPLAY, INK)
    for i, (lab, val, st) in enumerate(rows):
        yy = y + 150 + i * 150
        text(c, lab, x + 40, yy + 10, 38, BODYM, GREY_D)
        box(c, x + 40, yy + 30, w - 80, 76, 16, hx("f4f1ea"), 4, shading=0)
        n = int(max(0, t - st) * 18)
        text(c, val[:n], x + 64, yy + 82, 44, BODY, INK)
        if n >= len(val) and st < t:
            circle(c, x + w - 80, yy + 68, 22, LEAF, 3, shading=0)


@scene2("C04")
def C04(c, t, S):
    farm(c, t, seed=37)
    SAR(c, S, t, 330, 1010, 0.95, pose="present")
    form(c, 680, 120, 1140, t, [("Main category", "Pick your own farm", P(S, 4) + 0.3)])
    card(c, ["What visitors come to DO,", "not only what you grow"], 720, 560, t, [P(S, 2), P(S, 3)], size=56)


@scene2("C05")
def C05(c, t, S):
    soft_bg(c, t, hx("e9f1df"))
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, d in enumerate(days):
        a = ease_out(prog(t, P(S, 0) + i * 0.15, 0.4))
        if a <= 0:
            continue
        x = 180 + i * 230
        open_ = i >= 5
        c.push_group()
        box(c, x, 340, 200, 300, 26, hx("dff0d4") if open_ else hx("ece8e1"), 6)
        text(c, d, x + 100, 420, 54, DISPLAY, INK, "center")
        text(c, "9–5" if open_ else "Closed", x + 100, 540, 44 if open_ else 40, BODY, LEAF if open_ else GREY_D,
             "center")
        c.pop_group_to_source(); c.paint_with_alpha(a)
    title(c, "Your real hours", W / 2, 220, t, P(S, 0), 90)
    ease_text(c, "Seasonal? Say so.", W / 2, 820, 72, t, P(S, 1), DISPLAY, TOMATO, "center")


@scene2("C06")
def C06(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    kinds = [("goats", P(S, 1)), ("picnic", P(S, 2)), ("tree", P(S, 0) + 0.6)]
    for i, (k, st) in enumerate(kinds):
        a = ease_back(prog(t, st, 0.6))
        if a <= 0:
            continue
        x = 150 + i * 560
        c.save(); c.translate(x + 250, 560); c.rotate((i - 1) * 0.05); c.scale(a, a); c.translate(-250, -220)
        box(c, -20, -20, 540, 480, 14, PAPER, 6)
        photo_tile(c, 0, 0, 500, 440, k, t, seed=i + 3)
        c.restore()
    title(c, "Photos of people having fun", W / 2, 190, t, P(S, 0), 84)
    ease_text(c, "Not just your crops.", W / 2, 1000, 60, t, P(S, 3), BODY, INK, "center")


@scene2("C07")
def C07(c, t, S):
    farm(c, t, seed=38)
    SAR(c, S, t, 330, 1010, 0.95, pose="present")
    form(c, 680, 80, 1140, t, [("Phone", "(555) 014-2021", P(S, 0) + 0.2), ("Booking link", "willowcreekfarm.com/book",
                                                                             P(S, 0) + 1.0),
                               ("Description", "Pick strawberries, meet the goats...", P(S, 1) + 0.3)])


@scene2("C08")
def C08(c, t, S):
    soft_bg(c, t, hx("e9f1df"))
    p = ease(prog(t, P(S, 0), 1.0))
    listing(c, 560, 220, 800, t, full=p if p > 0.05 else 0.0, start=P(S, 0) + 0.3)
    if p < 0.6:
        c.push_group(); map_pin(c, 960, 330, 1.1, ghost=True); c.pop_group_to_source(); c.paint_with_alpha(1 - p)
    a = ease_out(prog(t, P(S, 0) + 1.6, 0.6))
    if a > 0:
        c.save(); c.translate(1500, 300); c.rotate(0.12)
        box(c, -120, -50, 240, 100, 50, LEAF, 6)
        text(c, "OPEN", 0, 22, 60, DISPLAY, PAPER, "center", alpha=a)
        c.restore()
    title(c, "The Second Gate, unlocked", W / 2, 140, t, P(S, 0), 84, col=GOLD)


# ================================================================ Section 8: Objection
@scene2("O01")
def O01(c, t, S):
    season_bg(c, "summer", t, seed=40)
    house(c, 1500, 640, 0.5)
    barn(c, 1640, 650, 0.45)
    c.move_to(-20, 1080); c.curve_to(400, 900, 1100, 760, 1560, 660)
    setc(c, hx("cdbf9f")); c.set_line_width(40); c.stroke()
    pill(c, "“But my farm is too remote.”", W / 2, 260, t, P(S, 0) + 0.3, size=64, bg=hx("fde2dc"))


@scene2("O02")
def O02(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    SAR(c, S, t, 760, 1400, 1.7, pose="finger")
    card(c, [("Remote is exactly", 76, DISPLAY, INK), ("why you need it.", 76, DISPLAY, LEAF)], 1180, 160, t,
         [P(S, 1), P(S, 1) + 0.4], size=70)


@scene2("O03")
def O03(c, t, S):
    season_bg(c, "summer", t, seed=41)
    c.move_to(-20, 950); c.curve_to(500, 880, 1200, 860, W + 20, 840)
    setc(c, hx("cdbf9f")); c.set_line_width(70); c.stroke()
    house(c, 1650, 830, 0.7)
    gate(c, 1380, 870, 0.6, open_=0.0)
    # every trip starts in a kitchen
    for i in range(3):
        st = P(S, 1) + i * 0.6
        a = ease_out(prog(t, st, 0.5))
        if a <= 0:
            continue
        x = 220 + i * 360
        c.push_group()
        box(c, x - 120, 190, 240, 300, 26, hx("f6e3be"), 5)
        box(c, x - 34, 250, 68, 120, 12, NAVY, 4)
        box(c, x - 26, 262, 52, 90, 6, hx("eaf6ff"), 0, shading=0)
        text(c, "searching...", x, 450, 32, BODYM, INK, "center")
        c.pop_group_to_source(); c.paint_with_alpha(a)
    ease_text(c, "Every visitor looks you up first.", W / 2, 120, 64, t, P(S, 1), DISPLAY, INK, "center")
    a = ease_out(prog(t, P(S, 2), 0.6))
    if a > 0:
        padlock(c, 1280, 760, 0.9 * a, t, 1.0)


@scene2("O04")
def O04(c, t, S):
    soft_bg(c, t, hx("e6f1fb"))
    person(c, 420, 1010, 1.05, t, seed=60, hair=hx("cfcfcf"),
           pose=((1.0, 2.2), (0.2, 0.2)))
    box(c, 520, 560, 70, 120, 12, NAVY, 4)
    v = countup(82, t, P(S, 2), 1.6)
    a = ease_out(prog(t, P(S, 2) - 0.2, 0.6))
    if a > 0:
        c.push_group()
        box(c, 820, 200, 960, 520, 40, PAPER, 7)
        text(c, f"{v:.0f}%", 1300, 500, 220, DISPLAY, LEAF, "center")
        text(c, "of U.S. farms have a smartphone", 1300, 610, 48, BODY, INK, "center")
        text(c, "USDA, 2023", 1300, 680, 36, BODYM, GREY_D, "center")
        c.pop_group_to_source(); c.paint_with_alpha(a)
    ease_text(c, "You can do this.", 1300, 900, 76, t, P(S, 4), DISPLAY, INK, "center")


# ================================================================ Section 9: Close
@scene2("Z01")
def Z01(c, t, S):
    c.save(); cam(c, t, S.dur, 1.0, 1.06, 560, 800)
    country_road(c, t, tod="sunset", sign_txt="FRESH EGGS")
    c.restore()
    phone_gate(c, 1500, 1000, 0.85, t, lock=0.0, open_p=ease(prog(t, P(S, 2), 1.2)), screen_full=1.0)
    card(c, ["Gate 1: the road", ("Gate 2: the phone", 56, DISPLAY, LEAF)], 80, 60, t, [P(S, 0), P(S, 2)], size=56)


@scene2("Z02")
def Z02(c, t, S):
    season_bg(c, "spring", t, seed=29)
    country_store(c, 1300, 1000, 1.0, t)
    gate(c, 700, 1020, 0.85, open_=1.0)
    card(c, [("People knew", 64, DISPLAY, INK), ("where to find it.", 64, DISPLAY, LEAF)], 80, 70, t,
         [P(S, 0), P(S, 0) + 0.4], size=60)


@scene2("Z03")
def Z03(c, t, S):
    farm(c, t, seed=42, tod="sunset")
    SAR(c, S, t, 420, 1010, 1.0, pose="present")
    card(c, ["Watching won't change anything.", ("Doing will.", 84, DISPLAY, TOMATO)], 820, 160, t,
         [P(S, 0), P(S, 1)], size=60)


@scene2("Z04")
def Z04(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    SAR(c, S, t, 330, 1010, 0.95, pose="point")
    a = ease_out(prog(t, P(S, 0), 0.6))
    if a > 0:
        c.push_group()
        box(c, 680, 140, 1140, 760, 36, PAPER, 7)
        text(c, "Homework", 740, 240, 72, DISPLAY, TOMATO)
        text(c, "Search your farm's name", 740, 340, 56, BODY, INK)
        text(c, "on Google Maps. What did you find?", 740, 410, 50, BODY, INK)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    for i, s in enumerate(["Nothing?", "A ghost pin?", "A full listing?"]):
        pill(c, s, 760, 560 + i * 120, t, P(S, 4 + i), size=52,
             anchor="l")


PHASES = ["Protect your farm", "Your offer and price", "Site and safety", "Marketing (Point 17: Google)",
          "Friends-and-family test"]


@scene2("Z05")
def Z05(c, t, S):
    farm(c, t, seed=43)
    a = ease_back(prog(t, 0.2, 0.8))
    if a > 0:
        c.save(); c.translate(560, 560); c.scale(a, a); blueprint_cover(c, 0, 0, 0.95, t); c.restore()
    for i, s in enumerate(PHASES):
        pill(c, s, 1000, 260 + i * 140, t, P(S, 0) + 0.8 + i * 0.35, size=46, mark="v", anchor="l")


@scene2("Z06")
def Z06(c, t, S):
    soft_bg(c, t, hx("f3e3c0"))
    c.save(); c.translate(960, 560); c.rotate(-0.03)
    box(c, -520, -380, 1040, 700, 20, hx("fff8e8"), 7)
    for k in range(9):
        c.move_to(-480, -260 + k * 70); c.line_to(480, -260 + k * 70)
        setc(c, hx("b9d3f0")); c.set_line_width(3); c.stroke()
    c.restore()
    title(c, "Why free?", W / 2, 260, t, P(S, 0), 96, col=GOLD)
    ease_text(c, "The checklist Stephen", W / 2, 470, 64, t, P(S, 1), BODY, INK, "center")
    ease_text(c, "wishes he'd had", W / 2, 550, 64, t, P(S, 1) + 0.3, BODY, INK, "center")
    ease_text(c, "Get the basics right first.", W / 2, 720, 64, t, P(S, 2), DISPLAY, LEAF, "center")


@scene2("Z07")
def Z07(c, t, S):
    soft_bg(c, t, hx("e6f1fb"))
    title(c, "21 points · 5 phases", W / 2, 150, t, P(S, 0), 90)
    starts = [P(S, 1), P(S, 5), P(S, 6), P(S, 8), P(S, 12)]
    for i, (s, st) in enumerate(zip(PHASES, starts)):
        a = ease_out(prog(t, st, 0.6))
        if a <= 0:
            continue
        x, y = 120 + (i % 3) * 580, 260 + (i // 3) * 360
        hl = i == 3 and t > P(S, 11)
        c.push_group()
        box(c, x, y, 540, 300, 30, hx("fff1c4") if hl else PAPER, 7)
        circle(c, x + 70, y + 80, 42, LEAF, 5)
        text(c, str(i + 1), x + 70, y + 102, 56, DISPLAY, PAPER, "center")
        lines = wrap(c, s, BODY, 50, 420)
        for k, ln in enumerate(lines):
            text(c, ln, x + 40, y + 190 + k * 60, 50, BODY, INK)
        if hl:
            stroke(c, lambda: rrect(c, x - 10, y - 10, 560, 320, 36), GOLD, 10)
        c.pop_group_to_source(); c.paint_with_alpha(a)


@scene2("Z08")
def Z08(c, t, S):
    farm(c, t, seed=44)
    x = lerp(300, 1200, ease(t / S.dur))
    SAR(c, S, t, x, 1010, 0.95, pose="slate", walk=t * 5.5,
        hold=(1, lambda c, hx_, hy: (box(c, hx_ - 70, hy - 150, 140, 180, 10, WOOD, 4),
                                     box(c, hx_ - 55, hy - 130, 110, 150, 6, PAPER, 0, shading=0))))
    title(c, "Print it. Walk your land with it.", W / 2, 180, t, P(S, 0), 84)


@scene2("Z09")
def Z09(c, t, S):
    soft_bg(c, t, hx("e6f1fb"))

    def body(c, x, y, w, h, t):
        text(c, "Get the free 21-Point Blueprint", x + 60, y + 110, 60, DISPLAY, INK)
        for i, (lab, val) in enumerate((("Name", "Your name"), ("Email", "you@yourfarm.com"))):
            st = P(S, 1) + i * 0.8
            yy = y + 190 + i * 150
            text(c, lab, x + 60, yy, 40, BODYM, GREY_D)
            box(c, x + 60, yy + 20, w - 120, 80, 16, hx("f4f1ea"), 4, shading=0)
            n = int(max(0, t - st) * 16)
            text(c, val[:n], x + 90, yy + 76, 46, BODY, INK)
        a = ease_back(prog(t, P(S, 2), 0.5))
        if a > 0:
            c.save(); c.translate(x + w / 2, y + 570); c.scale(a, a)
            box(c, -220, -60, 440, 120, 60, LEAF, 6); text(c, "It's yours", 0, 22, 60, DISPLAY, PAPER, "center")
            c.restore()
    browser(c, 260, 120, 1400, 820, "Link in the description", t, body)


@scene2("Z10")
def Z10(c, t, S):
    farm(c, t, seed=45)
    a = ease_back(prog(t, 0.2, 0.8))
    if a > 0:
        c.save(); c.translate(560, 560); c.scale(a, a); ebook_cover(c, 0, 0, 0.95, t); c.restore()
    card(c, [("Free ebook", 64, DISPLAY, LEAF), "150 Ways to Unlock", "Hidden Wealth From Your Farm",
             ("Link in the description", 46, BODY, SKY)], 940, 220, t,
         [P(S, 0), P(S, 1), P(S, 1) + 0.3, P(S, 2)], size=54)


def end_screen(c, t, S, wave=True):
    farm(c, t, seed=46, tod="sunset", gate_open=1.0)
    phone_gate(c, 1650, 1000, 0.7, t, lock=0.0, open_p=1.0, screen_full=1.0)
    SAR(c, S, t, 960, 1030, 0.85, pose="wave", wave_amp=0.25)


@scene2("Z11")
def Z11(c, t, S):
    end_screen(c, t, S)
    # blank space kept for YouTube's end-screen elements (top left video card, top right subscribe)
    card(c, ["Watch next:", ("50 Ways to Make Extra Money", 52, DISPLAY, INK), ("on Your Farm", 52, DISPLAY, INK)],
         80, 60, t, [P(S, 0), P(S, 0) + 0.3, P(S, 0) + 0.5], size=44)


@scene2("Z12")
def Z12(c, t, S):
    end_screen(c, t, S)
    title(c, "Two gates. Open both.", W / 2, 230, t, P(S, 0), 110, col=GOLD)
    text(c, "agritourismsuccess.com/150ways", W / 2, 360, 46, BODY, PAPER, "center", outline=INK, olw=8,
         alpha=ease_out(prog(t, P(S, 0) + 1.0, 0.8)))
    text(c, "Narration and animation are AI-generated.", W - 40, H - 30, 28, BODYM, PAPER, "right", outline=INK,
         olw=5)
