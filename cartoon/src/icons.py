"""Thirty tiny event icons (one per event) used on the season wheel and card fans."""
import math
from gfx import *
from props import SEASONS

ICON_SEASON = ["winter"] * 8 + ["spring"] * 8 + ["summer"] * 7 + ["fall"] * 7


def _g(c, i):
    """Glyph for event i (0-based), drawn in a 100x100 box centred on 0,0."""
    L = 4
    if i == 0:  # tree
        fill_ink(c, lambda: poly(c, [(-30, 25), (0, -38), (30, 25)]), hx("2f6f3a"), L)
        box(c, -6, 25, 12, 14, 2, WOOD, L)
    elif i == 1:  # antlers
        for s in (-1, 1):
            stroke(c, lambda: (c.move_to(s * 6, 20), c.curve_to(s * 10, -10, s * 30, -20, s * 34, -36)), INK, 7)
            stroke(c, lambda: (c.move_to(s * 18, -10), c.line_to(s * 4, -28)), INK, 6)
        circle(c, 0, 26, 14, hx("9a6a44"), L)
    elif i == 2:  # glowing tulip
        glow(c, 0, -6, 40, GOLD, 0.6)
        fill_ink(c, lambda: (c.move_to(-16, -18), c.line_to(-8, -6), c.line_to(0, -18), c.line_to(8, -6), c.line_to(16, -18),
                             c.curve_to(18, 12, -18, 12, -16, -18)), TOMATO, L)
        stroke(c, lambda: (c.move_to(0, 6), c.line_to(0, 34)), LEAF, 6)
    elif i == 3:  # santa hat
        fill_ink(c, lambda: smooth(c, [(-30, 18), (-6, -30), (26, -20), (30, 18)]), TOMATO, L)
        box(c, -34, 12, 68, 16, 8, WHITE, L)
        circle(c, 26, -22, 9, WHITE, L)
    elif i == 4:  # tent
        fill_ink(c, lambda: poly(c, [(-36, 28), (0, -30), (36, 28)]), CREAM, L)
        fill_ink(c, lambda: poly(c, [(-10, 28), (0, 4), (10, 28)]), GOLD, L)
    elif i == 5:  # snowdrop
        stroke(c, lambda: (c.move_to(0, 34), c.curve_to(0, -10, 10, -30, 18, -24)), LEAF, 5)
        fill_ink(c, lambda: (c.move_to(10, -20), c.curve_to(2, 0, 30, 0, 22, -20), c.close_path()), WHITE, L)
    elif i == 6:  # heart
        fill_ink(c, lambda: (c.move_to(0, 30), c.curve_to(-50, -4, -20, -44, 0, -16), c.curve_to(20, -44, 50, -4, 0, 30)),
                 TOMATO, L)
    elif i in (7, 11):  # lamb
        for (x, y) in ((-14, 0), (0, -8), (14, 0), (0, 8), (-6, 4), (8, 2)):
            circle(c, x, y, 14, CREAM, L)
        oval(c, 24, -8, 10, 13, hx("2d2a33"), L)
        if i == 11:
            circle(c, -26, 22, 8, SKIN, L)
    elif i == 8:  # pancakes
        for k in range(3):
            oval(c, 0, 18 - k * 14, 32, 10, hx("e4a95a"), L)
        fill_ink(c, lambda: (c.move_to(-10, -14), c.curve_to(-4, 6, 4, 6, 10, -14), c.close_path()), hx("b8651a"), 3)
    elif i == 9:  # pruners
        for s in (-1, 1):
            stroke(c, lambda: (c.move_to(0, 0), c.line_to(s * 18, 34)), TOMATO, 10)
        stroke(c, lambda: (c.move_to(0, 0), c.line_to(-8, -34)), hx("9aa0b0"), 8)
        stroke(c, lambda: (c.move_to(0, 0), c.line_to(8, -34)), hx("9aa0b0"), 6)
    elif i == 10:  # seedling
        box(c, -24, 6, 48, 28, 6, hx("c9733a"), L)
        stroke(c, lambda: (c.move_to(0, 6), c.line_to(0, -20)), LEAF, 6)
        oval(c, -12, -22, 12, 7, LEAF, 3)
        oval(c, 12, -26, 12, 7, LEAF, 3)
    elif i == 12:  # goat in coat
        oval(c, 0, 6, 30, 18, CREAM, L)
        fill_ink(c, lambda: rrect(c, -20, -8, 34, 22, 6), TOMATO, 3)
        circle(c, 30, -14, 12, CREAM, L)
    elif i == 13:  # egg
        oval(c, 0, 0, 24, 32, hx("8fd0f0"), L)
        stroke(c, lambda: (c.move_to(-22, 0), c.line_to(-8, -8), c.line_to(8, 4), c.line_to(22, -6)), TOMATO, 5)
    elif i == 14:  # tulip bunch
        for k, col in enumerate((TOMATO, GOLD, hx("e86aa6"))):
            x = (k - 1) * 18
            stroke(c, lambda: (c.move_to(x, 34), c.line_to(x * 0.5, -6)), LEAF, 5)
            oval(c, x, -14, 10, 14, col, 3)
    elif i == 15:  # wool / shears
        for (x, y) in ((-10, 0), (10, -4), (0, 10), (14, 12)):
            circle(c, x, y, 14, CREAM, L)
        stroke(c, lambda: (c.move_to(-30, -30), c.line_to(-4, -4)), hx("9aa0b0"), 6)
    elif i == 16:  # yoga mat + goat
        box(c, -38, 16, 76, 14, 7, hx("8e5aa8"), L)
        oval(c, 0, -6, 22, 14, CREAM, L)
    elif i == 17:  # flower
        for k in range(6):
            a = k * math.pi / 3
            circle(c, math.cos(a) * 16, math.sin(a) * 16 - 4, 11, hx("e86aa6"), 3)
        circle(c, 0, -4, 10, GOLD, 3)
    elif i == 18:  # lavender
        for k in range(3):
            x = (k - 1) * 14
            stroke(c, lambda: (c.move_to(x, 34), c.line_to(x, -4)), LEAF, 4)
            for j in range(4):
                circle(c, x, -8 - j * 9, 5, hx("8e6ad8"), 2)
    elif i == 19:  # sun hat
        oval(c, 0, 10, 38, 10, GOLD, L)
        fill_ink(c, lambda: (c.new_sub_path(), c.arc(0, 6, 20, math.pi, 2 * math.pi), c.close_path()), GOLD, L)
        box(c, -20, -2, 40, 8, 3, TOMATO, 3)
    elif i == 20:  # sunset
        circle(c, 0, 10, 24, hx("ff9a3a"), L)
        box(c, -38, 12, 76, 22, 4, hx("6a4a7a"), L)
    elif i == 21:  # bee
        oval(c, 0, 0, 24, 16, GOLD, L)
        for x in (-6, 6):
            stroke(c, lambda: (c.move_to(x, -14), c.line_to(x, 14)), INK, 5)
        oval(c, -4, -20, 10, 8, (1, 1, 1, 0.9), 3)
    elif i == 22:  # cheese
        fill_ink(c, lambda: poly(c, [(-34, 20), (34, 20), (34, -6), (-34, -24)]), hx("f6d36a"), L)
        circle(c, -10, 4, 5, hx("d9b24a"), 2)
        circle(c, 12, 10, 4, hx("d9b24a"), 2)
    elif i == 23:  # telescope + star
        stroke(c, lambda: (c.move_to(-28, 24), c.line_to(20, -14)), INK, 18)
        stroke(c, lambda: (c.move_to(-28, 24), c.line_to(20, -14)), hx("8c8f9e"), 12)
        circle(c, 28, -28, 7, GOLD, 3)
    elif i == 24:  # maze
        box(c, -32, -32, 64, 64, 6, hx("d9b24a"), L)
        stroke(c, lambda: (c.move_to(-20, -20), c.line_to(20, -20), c.line_to(20, 4), c.line_to(-8, 4), c.line_to(-8, 20)),
               LEAF, 6)
    elif i == 25:  # pumpkin
        for dx in (-12, 12, 0):
            oval(c, dx, 6, 16, 20, hx("ef8a1d"), L)
        box(c, -3, -20, 6, 10, 2, LEAF, 3)
    elif i == 26:  # ghost
        fill_ink(c, lambda: (c.move_to(-22, 26), c.line_to(-22, -6), c.curve_to(-22, -40, 22, -40, 22, -6), c.line_to(22, 26),
                             c.line_to(12, 18), c.line_to(4, 26), c.line_to(-4, 18), c.line_to(-12, 26), c.close_path()),
                 WHITE, L)
        circle(c, -7, -8, 3.5, INK, 0)
        circle(c, 7, -8, 3.5, INK, 0)
    elif i == 27:  # plate + fork
        oval(c, 0, 4, 30, 30, WHITE, L)
        oval(c, 0, 4, 16, 16, hx("e4a95a"), 3)
        stroke(c, lambda: (c.move_to(-40, -24), c.line_to(-40, 30)), INK, 5)
    elif i == 28:  # moon
        circle(c, 0, 0, 30, hx("fff1c4"), L)
        circle(c, -8, -8, 6, hx("efe0a8"), 0)
    elif i == 29:  # wreath
        stroke(c, lambda: c.arc(0, 0, 26, 0, 6.3), INK, 18)
        stroke(c, lambda: c.arc(0, 0, 26, 0, 6.3), LEAF, 12)
        circle(c, 0, 26, 8, TOMATO, 3)


def icon(c, i, x, y, r=44, a=1.0, ring=True):
    if a <= 0.01:
        return
    c.push_group()
    col = SEASON_COL[ICON_SEASON[i]]
    if ring:
        circle(c, x, y, r, tint(col, 0.55), 5)
    c.save(); c.translate(x, y); c.scale(r / 50, r / 50)
    _g(c, i)
    c.restore()
    c.pop_group_to_source()
    c.paint_with_alpha(a)
