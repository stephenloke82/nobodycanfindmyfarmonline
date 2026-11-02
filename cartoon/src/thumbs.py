"""Thumbnails A and B (1280x720), drawn at 1920x1080 and scaled down."""
import os, sys
import cairo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gfx import *
from props import gate, barn, fence
from sets import season_bg
from kit008 import phone_frame, map_bg, map_pin, ghost_sheet, padlock, listing
from beats import ROOT
from PIL import Image


def big_words(c, lines, x, y, size, cols, align="left"):
    for i, (s, col) in enumerate(zip(lines, cols)):
        text(c, s, x, y + i * size * 1.02, size, DISPLAY, col, align, outline=INK, olw=size * 0.16)


def thumb_a(c):
    season_bg(c, "summer", 2.0, tod="sunset", seed=7)
    fence(c, -20, 1920, 900, 1.0)
    gate(c, 1180, 960, 1.25)

    def scr(c, sx, sy, sw, sh, t):
        map_bg(c, sx, sy, sw, sh, t, seed=4)
        map_pin(c, sx + sw / 2, sy + sh * 0.62, 1.5, ghost=True)
        ghost_sheet(c, sx + sw / 2, sy + sh * 0.62 - 40, 0.9, 1.0)
    phone_frame(c, 1180, 80, 560, 920, scr, 1.0, tilt=0.08, hand=True)
    big_words(c, ["INVISIBLE?"], 60, 420, 190, [PAPER])
    big_words(c, ["The free fix"], 70, 600, 110, [GOLD])


def thumb_b(c):
    c.save(); c.rectangle(0, 0, 960, H); c.clip()
    season_bg(c, "summer", 1.0, tod="sunset", seed=8)
    fence(c, -20, 960, 860, 1.0)
    gate(c, 200, 930, 1.3)
    padlock(c, 520, 760, 1.7, 0.0)
    c.restore()
    c.save(); c.rectangle(960, 0, 960, H); c.clip()
    season_bg(c, "summer", 1.0, seed=9)
    c.translate(960, 0)
    listing(c, 120, 300, 720, 99.0, full=1.0, start=0)
    c.restore()
    stroke(c, lambda: (c.move_to(960, 0), c.line_to(960, H)), PAPER, 22)
    stroke(c, lambda: (c.move_to(960, 0), c.line_to(960, H)), INK, 8)
    text(c, "THE FREE FIX", W / 2, 210, 190, DISPLAY, GOLD, "center", outline=INK, olw=30)


def render(fn, out):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    c = cairo.Context(s)
    fn(c)
    s.write_to_png(out + ".tmp.png")
    Image.open(out + ".tmp.png").convert("RGB").resize((1280, 720), Image.LANCZOS).save(out)
    os.remove(out + ".tmp.png")
    print(out)


if __name__ == "__main__":
    od = os.path.join(ROOT, "output"); os.makedirs(od, exist_ok=True)
    render(thumb_a, os.path.join(od, "thumbnail-a.png"))
    render(thumb_b, os.path.join(od, "thumbnail-b.png"))
