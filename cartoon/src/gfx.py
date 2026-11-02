"""Core drawing helpers: palette, ink-outlined shapes with soft shading, eased text."""
import math, random
import cairo

W, H, FPS = 1920, 1080, 30


def hx(h, a=1.0):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


def mix(c1, c2, t):
    return tuple(c1[i] + (c2[i] - c1[i]) * t for i in range(4))


def shade(c, k=0.18):
    return (c[0] * (1 - k), c[1] * (1 - k), c[2] * (1 - k), c[3])


def tint(c, k=0.25):
    return (c[0] + (1 - c[0]) * k, c[1] + (1 - c[1]) * k, c[2] + (1 - c[2]) * k, c[3])


SKY, GOLD, TOMATO, LEAF = hx("1b36a8"), hx("f2b632"), hx("e2452f"), hx("3f8f3a")
CREAM, PAPER, INK, WOOD = hx("fbf1d9"), hx("fff8e8"), hx("1b1f3a"), hx("c8955a")
SKIN, CHEEK = hx("f1c8a0"), hx("f29a8a")
WHITE = (1, 1, 1, 1)
SNOW = hx("f4f7ff")
DENIM = hx("3558c8")
MUD = hx("7a5636")
GRASS = hx("6fb24a")
NIGHT = hx("17287a")
SEASON_COL = {"winter": SKY, "spring": LEAF, "summer": GOLD, "fall": TOMATO}

LW = 6.0  # default ink width


# ---------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def ease(x):  # smoothstep-ish ease in-out
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_back(x, s=1.4):
    x = clamp(x)
    x -= 1
    return x * x * ((s + 1) * x + s) + 1


def prog(t, start, dur):
    return clamp((t - start) / dur) if dur > 0 else (1.0 if t >= start else 0.0)


def lerp(a, b, t):
    return a + (b - a) * t


def damp_swing(t, amp=0.9, freq=1.6, decay=2.2):
    """Damped pendulum angle (radians) after a release at t=0."""
    if t < 0:
        return amp
    return amp * math.exp(-decay * t) * math.cos(2 * math.pi * freq * t)


# ---------------------------------------------------------------- paths
def rrect(c, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    c.close_path()


def ellipse(c, x, y, rx, ry):
    c.save()
    c.translate(x, y)
    c.scale(max(rx, 0.01), max(ry, 0.01))
    c.new_sub_path()
    c.arc(0, 0, 1, 0, 2 * math.pi)
    c.restore()


def poly(c, pts, close=True):
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    if close:
        c.close_path()


def smooth(c, pts, close=True):
    """Catmull-Rom through points."""
    n = len(pts)
    if n < 3:
        return poly(c, pts, close)
    P = pts + pts[:2] if close else [pts[0]] + pts + [pts[-1]]
    c.move_to(*P[1] if close else P[1])
    rng = range(1, n + 1) if close else range(1, n)
    for i in rng:
        p0, p1, p2, p3 = P[i - 1], P[i], P[(i + 1) % len(P)], P[(i + 2) % len(P)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        c.curve_to(*c1, *c2, *p2)
    if close:
        c.close_path()


def setc(c, col, a=None):
    if a is None:
        c.set_source_rgba(*col)
    else:
        c.set_source_rgba(col[0], col[1], col[2], col[3] * a)


def fill_ink(c, path, fill, lw=LW, shading=0.16, ink=INK, alpha=1.0, light=0.0):
    """Draw path (callable) filled with flat colour + gentle shading, then soft ink outline."""
    path()
    if fill is not None:
        x1, y1, x2, y2 = c.fill_extents()
        setc(c, fill, alpha)
        c.fill_preserve()
        if shading and x2 > x1:
            g = cairo.LinearGradient(x1, y1, x2 * 0.3 + x1 * 0.7 + (x2 - x1) * 0.0, y2)
            g.add_color_stop_rgba(0.0, 1, 1, 1, light * alpha)
            g.add_color_stop_rgba(0.55, 0, 0, 0, 0)
            g.add_color_stop_rgba(1.0, 0.05, 0.05, 0.2, shading * alpha)
            c.set_source(g)
            c.fill_preserve()
    if lw:
        setc(c, ink, 0.92 * alpha)
        c.set_line_width(lw)
        c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.stroke()
    else:
        c.new_path()


def stroke(c, path, col=INK, lw=LW, alpha=1.0):
    path()
    setc(c, col, alpha)
    c.set_line_width(lw)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.stroke()


def circle(c, x, y, r, fill, lw=LW, **kw):
    fill_ink(c, lambda: (c.new_sub_path(), c.arc(x, y, r, 0, 2 * math.pi)), fill, lw, **kw)


def oval(c, x, y, rx, ry, fill, lw=LW, **kw):
    fill_ink(c, lambda: ellipse(c, x, y, rx, ry), fill, lw, **kw)


def box(c, x, y, w, h, r, fill, lw=LW, **kw):
    fill_ink(c, lambda: rrect(c, x, y, w, h, r), fill, lw, **kw)


def shadow(c, x, y, rx, ry=None, a=0.18):
    ry = ry or rx * 0.22
    g = cairo.RadialGradient(x, y, 0, x, y, rx)
    g.add_color_stop_rgba(0, 0.1, 0.1, 0.25, a)
    g.add_color_stop_rgba(1, 0.1, 0.1, 0.25, 0)
    c.save()
    c.translate(x, y)
    c.scale(1, ry / rx)
    c.translate(-x, -y)
    c.set_source(g)
    c.arc(x, y, rx, 0, 2 * math.pi)
    c.fill()
    c.restore()


def glow(c, x, y, r, col, a=0.5):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, col[0], col[1], col[2], a)
    g.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    c.set_source(g)
    c.arc(x, y, r, 0, 2 * math.pi)
    c.fill()


# ---------------------------------------------------------------- text
DISPLAY, BODY, BODYM = "Dot Display", "Dot Body", "Dot Body Medium"


def font(c, face, size):
    c.select_font_face(face)
    c.set_font_size(size)


def text_w(c, s, face, size):
    font(c, face, size)
    return c.text_extents(s).x_advance


def fit_size(c, s, face, size, maxw, minsize=40):
    while size > minsize and text_w(c, s, face, size) > maxw:
        size -= 2
    return size


def text(c, s, x, y, size, face=BODY, col=INK, align="left", alpha=1.0, outline=None,
         olw=10, rise=0.0):
    """Baseline-anchored text. align: left|center|right."""
    if alpha <= 0.003:
        return
    font(c, face, size)
    ext = c.text_extents(s)
    w = ext.x_advance
    ox = x - (w / 2 if align == "center" else w if align == "right" else 0)
    y = y + rise
    if outline is not None:
        c.move_to(ox, y)
        c.text_path(s)
        setc(c, outline, alpha)
        c.set_line_width(olw)
        c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.stroke()
    c.move_to(ox, y)
    setc(c, col, alpha)
    c.show_text(s)
    return w


def ease_text(c, s, x, y, size, t, start, face=BODY, col=INK, align="left", outline=None,
              dur=0.7, olw=10):
    """Words ease in slowly (fade + gentle rise) and stay."""
    p = ease_out(prog(t, start, dur))
    if p <= 0:
        return
    text(c, s, x, y, size, face, col, align, alpha=p, outline=outline, olw=olw, rise=(1 - p) * 18)


def wrap(c, s, face, size, maxw):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if text_w(c, trial, face, size) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- misc
def rng_for(*key):
    return random.Random(hash(key) & 0xffffffff)


def paper_texture(w=W, h=H, seed=3):
    """Subtle paper grain overlay surface (drawn once)."""
    import numpy as np
    r = np.random.default_rng(seed)
    n = r.normal(0, 1, (h // 2, w // 2)).astype("float32")
    # soften
    n = (n + np.roll(n, 1, 0) + np.roll(n, 1, 1) + np.roll(n, -1, 0)) / 4
    a = np.clip(np.abs(n) * 10, 0, 22).astype("uint8")
    arr = np.zeros((h // 2, w // 2, 4), "uint8")
    shade_v = (n > 0)
    arr[..., 0] = np.where(shade_v, 30, 255) * a // 255
    arr[..., 1] = np.where(shade_v, 30, 248) * a // 255
    arr[..., 2] = np.where(shade_v, 58, 232) * a // 255
    arr[..., 3] = a
    surf = cairo.ImageSurface.create_for_data(memoryview(arr.copy()), cairo.FORMAT_ARGB32, w // 2, h // 2)
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    cc = cairo.Context(out)
    cc.scale(2, 2)
    cc.set_source_surface(surf, 0, 0)
    cc.get_source().set_filter(cairo.FILTER_BILINEAR)
    cc.paint()
    return out


def vignette_overlay(w=W, h=H):
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    cc = cairo.Context(out)
    g = cairo.RadialGradient(w / 2, h / 2, h * 0.45, w / 2, h / 2, w * 0.72)
    g.add_color_stop_rgba(0, 0.1, 0.1, 0.25, 0)
    g.add_color_stop_rgba(1, 0.1, 0.1, 0.25, 0.28)
    cc.set_source(g)
    cc.paint()
    return out
