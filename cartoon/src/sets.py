"""Season sets: layered backgrounds with slow parallax and weather."""
import math
import cairo
from gfx import *
from props import tree, barn, house, fence, sunflower, pumpkin, corn, moon, star

SKIES = {
    ("winter", "day"): (hx("8fb0e6"), hx("e3ebfa")),
    ("winter", "dusk"): (hx("2b3f9a"), hx("e79a7c")),
    ("spring", "day"): (hx("7fc0ee"), hx("e6f5ff")),
    ("summer", "day"): (hx("4f98de"), hx("ffeaa6")),
    ("summer", "sunset"): (hx("5a4bb0"), hx("ff9a5a")),
    ("fall", "day"): (hx("e9a25e"), hx("ffe6b4")),
    ("night", "night"): (hx("13246a"), hx("2f4bb0")),
}
HILLS = {
    "winter": (hx("cdd9f0"), hx("e9eef9"), SNOW),
    "spring": (hx("a6d68f"), hx("7cbf58"), hx("6aa84a")),
    "summer": (hx("a8c95a"), hx("d8c25a"), hx("a9c450")),
    "fall": (hx("d79a52"), hx("c27a36"), hx("b58a48")),
    "night": (hx("27377e"), hx("1f2e6c"), hx("2a3a78")),
}

_cache = {}


def _hill_path(c, w, base, amp, seed, freq=3):
    r = rng_for("hill", seed)
    ph = [r.uniform(0, 6.28) for _ in range(3)]
    c.move_to(0, H)
    for x in range(0, w + 41, 40):
        y = base - amp * (0.55 * math.sin(x / w * freq * math.pi + ph[0]) + 0.3 * math.sin(x / w * freq * 2.3 * math.pi + ph[1])
                          + 0.15 * math.sin(x / w * 9 * math.pi + ph[2]))
        c.line_to(x, y)
    c.line_to(w, H)
    c.close_path()


def _layer(season, tod, depth, seed):
    key = (season, tod, depth, seed)
    if key in _cache:
        return _cache[key]
    w = W + 400
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, H)
    c = cairo.Context(surf)
    hs = HILLS["night" if tod == "night" else season]
    if tod in ("dusk", "sunset"):
        hs = tuple(mix(h, hx("6a4a7a"), 0.35) for h in hs)
    r = rng_for("layer", season, depth, seed)
    if depth == 0:
        s1, s2 = SKIES.get((season, tod), SKIES.get(("night", "night") if tod == "night" else (season, "day")))
        g = cairo.LinearGradient(0, 0, 0, H * 0.8)
        g.add_color_stop_rgba(0, *s1); g.add_color_stop_rgba(1, *s2)
        c.set_source(g); c.paint()
        if tod == "night":
            for i in range(140):
                star(c, r.uniform(0, w), r.uniform(0, H * 0.6), r.uniform(2, 5), hx("fff4d0"), r.uniform(0.4, 1))
        # soft clouds
        if tod != "night":
            for i in range(5):
                cx_, cy_ = r.uniform(0, w), r.uniform(80, 360)
                def cl():
                    for j in range(4):
                        ellipse(c, cx_ + j * 50 - 75, cy_ - (j % 2) * 24, 70, 40)
                cl(); setc(c, INK, 0.22); c.set_line_width(8); c.stroke()
                cl(); setc(c, WHITE, 0.8); c.fill()
    elif depth == 1:  # far hills
        _hill_path(c, w, 640, 70, seed * 3 + 1, 2)
        setc(c, hs[0]); c.fill_preserve(); setc(c, INK, 0.25); c.set_line_width(4); c.stroke()
        for i in range(10):
            tx = r.uniform(0, w)
            kind = {"winter": "bare", "spring": "blossom", "summer": "leafy", "fall": "autumn", "night": "pine"}[
                season if tod != "night" else "night"]
            if tod == "night":
                kind = "pine"
            tree(c, tx, 640 + r.uniform(-10, 30), 0.32, kind, 0, seed=i, snow=(season == "winter"),
                 col=mix(hs[0], INK, 0.25) if tod == "night" else None)
    elif depth == 2:  # mid hills
        _hill_path(c, w, 760, 50, seed * 7 + 2, 3)
        setc(c, hs[1]); c.fill_preserve(); setc(c, INK, 0.5); c.set_line_width(5); c.stroke()
        if season == "summer" and tod != "night":
            for i in range(40):
                sunflower(c, r.uniform(0, w), r.uniform(780, 820), 0.35, 0, seed=i)
        if season == "fall" and tod != "night":
            for i in range(30):
                corn(c, r.uniform(0, w), r.uniform(770, 800), 0.45, 0, seed=i)
    elif depth == 3:  # ground
        c.move_to(0, 830)
        for x in range(0, w + 1, 60):
            c.line_to(x, 830 + 12 * math.sin(x / 300 + seed))
        c.line_to(w, H); c.line_to(0, H); c.close_path()
        setc(c, hs[2]); c.fill_preserve()
        g = cairo.LinearGradient(0, 830, 0, H)
        g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0.05, 0.25, 0.16)
        c.set_source(g); c.fill_preserve()
        setc(c, INK, 0.55); c.set_line_width(5); c.stroke()
        for i in range(60):
            gx, gy = r.uniform(0, w), r.uniform(860, H)
            col = shade(hs[2], 0.12) if season != "winter" else hx("d6e0f5")
            stroke(c, lambda: (c.move_to(gx, gy), c.line_to(gx + 8, gy - 14)), col, 4)
    _cache[key] = surf
    return surf


def season_bg(c, season, t, tod="day", seed=0, pan=6.0, layers=(0, 1, 2, 3), ground=True):
    """Draw the set. Parallax drift: deeper layers move slower."""
    speeds = {0: 0.05, 1: 0.18, 2: 0.42, 3: 1.0}
    for d in layers:
        if d == 3 and not ground:
            continue
        surf = _layer(season, tod, d, seed)
        ox = -(t * pan * speeds[d]) % 400 if False else -min(400, t * pan * speeds[d])
        c.set_source_surface(surf, ox, 0)
        c.paint()
        if d == 0:
            if tod == "day" and season in ("summer", "spring"):
                sx, sy = 1500 - t * 1.5, 190
                glow(c, sx, sy, 260, hx("fff2b0"), 0.6)
                circle(c, sx, sy, 70, hx("ffe27a"), 0, shading=0)
            if tod == "dusk":
                glow(c, 1400, 560, 520, hx("ffb27a"), 0.55)
            if tod == "sunset":
                glow(c, 1300, 620, 600, hx("ffcf7a"), 0.7)
                circle(c, 1300, 640, 110, hx("ffcf6a"), 0, shading=0)
            if season == "fall" and tod == "day":
                glow(c, 1600, 260, 700, hx("ffd27a"), 0.5)


def weather(c, kind, t, n=None, seed=1, intensity=1.0, region=(0, 0, W, H)):
    x0, y0, w, h = region
    r = rng_for("wx", kind, seed)
    if kind == "snow":
        n = n or 110
        for i in range(n):
            depth = r.uniform(0.4, 1.0)
            px0, py0 = r.uniform(0, w), r.uniform(0, h)
            sp = 40 + 90 * depth
            y = (py0 + t * sp) % (h + 20) - 10
            x = (px0 + math.sin(t * 0.8 + i) * 18 * depth + t * 8) % w
            c.arc(x0 + x, y0 + y, 3 + 4 * depth, 0, 6.3)
            setc(c, WHITE, 0.85 * intensity); c.fill()
    elif kind == "petals":
        n = n or 40
        for i in range(n):
            px0, py0 = r.uniform(0, w), r.uniform(0, h)
            x = (px0 + t * 60 + math.sin(t + i) * 30) % (w + 40) - 20
            y = (py0 + t * 35) % (h + 40) - 20
            c.save(); c.translate(x0 + x, y0 + y); c.rotate(t * 2 + i)
            c.scale(1, 0.55 + 0.4 * math.sin(t * 3 + i))
            ellipse(c, 0, 0, 10, 7)
            setc(c, hx("f7b9cc"), 0.95 * intensity); c.fill_preserve()
            setc(c, INK, 0.4 * intensity); c.set_line_width(2); c.stroke()
            c.restore()
    elif kind == "leaves":
        n = n or 34
        cols = [TOMATO, GOLD, hx("e07a2a"), hx("b8452a")]
        for i in range(n):
            px0, py0 = r.uniform(0, w), r.uniform(0, h)
            x = (px0 + t * 140 + math.sin(t * 1.3 + i) * 40) % (w + 60) - 30
            y = (py0 + t * 55 + math.sin(t * 2 + i) * 20) % (h + 60) - 30
            c.save(); c.translate(x0 + x, y0 + y); c.rotate(t * 2.5 + i)
            c.scale(1, 0.4 + 0.6 * abs(math.sin(t * 2 + i)))
            c.move_to(-16, 0); c.curve_to(-6, -14, 6, -14, 16, 0); c.curve_to(6, 14, -6, 14, -16, 0)
            setc(c, cols[i % 4], intensity); c.fill_preserve()
            setc(c, INK, 0.7 * intensity); c.set_line_width(2.5); c.stroke()
            c.restore()
    elif kind == "heat":
        # heat shimmer: wavy translucent bands + drifting pollen
        for j in range(5):
            yy = y0 + h * 0.62 + j * 26
            c.move_to(x0, yy)
            for xx in range(0, int(w) + 1, 30):
                c.line_to(x0 + xx, yy + math.sin(xx / 70 + t * 3 + j) * 5)
            setc(c, WHITE, 0.10 * intensity); c.set_line_width(10); c.stroke()
        n = n or 26
        for i in range(n):
            px0, py0 = r.uniform(0, w), r.uniform(0, h)
            x = (px0 + t * 20 + math.sin(t + i) * 30) % w
            y = (py0 - t * 14) % h
            c.arc(x0 + x, y0 + y, 4, 0, 6.3)
            setc(c, hx("fff4c0"), 0.8 * intensity); c.fill()
    elif kind == "fireflies":
        n = n or 24
        for i in range(n):
            px0, py0 = r.uniform(0, w), r.uniform(h * 0.4, h * 0.9)
            x = px0 + math.sin(t * 0.7 + i) * 40
            y = py0 + math.sin(t * 0.9 + i * 2) * 25
            a = 0.5 + 0.5 * math.sin(t * 3 + i)
            glow(c, x0 + x, y0 + y, 18, hx("fff27a"), 0.7 * a * intensity)


def sepia(c, k=0.9):
    """Tone everything drawn so far to sepia."""
    c.save()
    c.set_operator(cairo.OPERATOR_HSL_COLOR)
    c.set_source_rgba(0.62, 0.45, 0.26, k)
    c.paint()
    c.set_operator(cairo.OPERATOR_OVER)
    c.set_source_rgba(0.98, 0.9, 0.75, 0.12 * k)
    c.paint()
    c.restore()
