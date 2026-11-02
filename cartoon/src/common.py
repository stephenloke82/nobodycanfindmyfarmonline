"""Shared scene helpers: registry, camera, text cards, event banner, event wrapper."""
import math
from gfx import *
from props import price_tag, tracker
import timeline

SCENES = {}
SFX = {}  # id -> function(S) -> list of (time, name)


def scene(bid, sfx=None):
    def deco(fn):
        SCENES[bid] = fn
        if sfx:
            SFX[bid] = sfx
        return fn
    return deco


def M(S, t):
    return timeline.mouth(S, t)


def P(S, i, default=0.0):
    """Start of phrase i (clamped)."""
    if not S.ph:
        return default
    return S.ph[min(i, len(S.ph) - 1)]


ZOOM_K = float(__import__("os").environ.get("ZOOM_K", "1.0"))


def cam(c, t, dur, z0=1.0, z1=1.05, fx=W / 2, fy=H / 2, dx=0.0):
    z = lerp(z0, z1, ease(t / max(dur, 0.1)))
    z = 1 + (z - 1) * ZOOM_K
    c.translate(fx + dx * ease(t / max(dur, 0.1)), fy)
    c.scale(z, z)
    c.translate(-fx, -fy)


def card(c, lines, x, y, t, starts, size=64, face=BODY, align="left", anchor="tl", col=INK, bg=PAPER, pad=40,
         gap=1.32, minw=0, lw=6, radius=28):
    """A paper card holding lines that ease in at their own start times and stay.
    lines: str or (str, size, face, colour). Returns (x, y, w, h)."""
    items = []
    for ln in lines:
        if isinstance(ln, str):
            ln = (ln, size, face, col)
        items.append(ln)
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
    for i, ((s, sz, f, cl), st) in enumerate(zip(items, starts)):
        yy += sz * 0.86
        tx = bx + pad if align == "left" else bx + w / 2 if align == "center" else bx + w - pad
        ease_text(c, s, tx, yy, sz, t, st, f, cl, align)
        yy += sz * (gap - 0.86)
    return (bx, by, w, h)


def title_text(c, s, x, y, t, start, size=110, col=PAPER, outline=INK, align="center", olw=16):
    ease_text(c, s, x, y, size, t, start, DISPLAY, col, align, outline=outline, olw=olw, dur=0.9)


def banner(c, n, title, t, t0, x=40, y=36):
    a = ease_out(prog(t, t0, 0.7))
    if a <= 0:
        return
    c.push_group()
    chip = f"No. {n}"
    cw = text_w(c, chip, DISPLAY, 60) + 56
    tw_ = text_w(c, title, BODY, 64) + 70
    h = 104
    rise = (1 - a) * 16
    box(c, x + cw - 30, y + 6 + rise, tw_ + 30, h - 12, 26, PAPER, 6)
    text(c, title, x + cw + 30, y + 72 + rise, 64, BODY, INK)
    box(c, x, y + rise, cw, h, 52, GOLD, 6)
    text(c, chip, x + cw / 2, y + 72 + rise, 60, DISPLAY, INK, "center")
    c.pop_group_to_source()
    c.paint_with_alpha(a)


def split_farm(s):
    if ", " in s:
        i = s.rfind(", ")
        return s[:i], s[i + 2:]
    return s, ""


def event_parts(S):
    scr = S.beat["screen"]
    m = scr[0]
    import re
    mm = re.match(r"No\. (\d+) (.+)", m)
    if mm:
        n, title = int(mm.group(1)), mm.group(2)
        farm = scr[1]
    else:
        n, title, farm = None, scr[0], scr[1]
    name, place = split_farm(farm)
    return n, title, name, place


def tag_time(S):
    i = S.ev.get("tag_ph", 2)
    return P(S, i) + 0.15


def event_scene(c, t, S, world, zoom=(1.0, 1.06), focus=(560, 600), banner_ph=0, show_tag=True):
    c.save()
    cam(c, t, S.dur, zoom[0], zoom[1], focus[0], focus[1])
    world(c, t, S)
    c.restore()
    n, title, name, place = event_parts(S)
    if n:
        banner(c, n, title, t, P(S, banner_ph) + 0.05)
    if show_tag:
        price_tag(c, 1500, 210, S.ev["rows"], name, place, t, tag_time(S))
    if S.tracker_n:
        tracker(c, S.tracker_n, S.season, t)


def overlay_tracker(c, t, S):
    if S.tracker_n:
        tracker(c, S.tracker_n, S.season, t)


def walk_x(t, t0, x0, x1, speed=160):
    """Position walking from x0 to x1 starting t0 at speed px/s; returns (x, walking?)."""
    d = x1 - x0
    T = abs(d) / speed
    p = clamp((t - t0) / T) if T > 0 else 1
    return x0 + d * p, 0 < p < 1


def chime_sfx(S):
    return [(0.05, "chime")]


def tag_sfx(S):
    return [(tag_time(S), "tag")]
