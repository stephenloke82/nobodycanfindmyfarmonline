"""Characters: Dot the host (drawn from her portrait), villagers and farm animals."""
import math
import cairo
from gfx import *

# Dot's portrait (64x64 viewBox), reproduced exactly; rest of body added around it.
PORTRAIT_HEAD_R = 22.0


def limb(c, x1, y1, x2, y2, w, col, lw=LW):
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x1, y1); c.line_to(x2, y2)
    setc(c, INK, 0.92); c.set_line_width(w + 2 * lw); c.stroke()
    c.move_to(x1, y1); c.line_to(x2, y2)
    setc(c, col); c.set_line_width(w); c.stroke()


def limb2(c, pts, w, col, lw=LW):
    """Two-segment limb with a single continuous outline."""
    for width, colr in ((w + 2 * lw, INK), (w, col)):
        c.move_to(*pts[0])
        for p in pts[1:]:
            c.line_to(*p)
        setc(c, colr, 0.92 if colr is INK else 1)
        c.set_line_width(width)
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.stroke()


def arm_pts(sx, sy, a1, a2, l1, l2, side):
    """side=+1 right (screen right), -1 left. a1 from straight-down, outward positive."""
    ang1 = math.pi / 2 - side * a1
    ex, ey = sx + l1 * math.cos(ang1), sy + l1 * math.sin(ang1)
    ang2 = ang1 - side * a2
    hx_, hy_ = ex + l2 * math.cos(ang2), ey + l2 * math.sin(ang2)
    return (sx, sy), (ex, ey), (hx_, hy_)


POSES = {
    #          right arm (a1,a2)   left arm (a1,a2)
    "idle":   ((0.18, 0.15), (0.18, 0.15)),
    "hips":   ((0.75, -1.9), (0.75, -1.9)),
    "point":  ((2.0, 0.15), (0.2, 0.2)),
    "point_low": ((1.15, 0.1), (0.2, 0.2)),
    "present": ((1.25, 0.5), (1.25, 0.5)),
    "wave":   ((2.5, 0.5), (0.2, 0.2)),
    "finger": ((2.2, 1.6), (0.2, 0.2)),
    "hat":    ((2.4, 2.2), (0.2, 0.2)),
    "shrug":  ((1.2, -1.2), (1.2, -1.2)),
    "count":  ((1.6, 1.9), (1.3, 1.8)),
    "slate":  ((0.9, 1.6), (0.9, 1.6)),
    "lean":   ((1.0, 0.6), (1.0, 0.6)),
    "think":  ((1.0, 2.5), (0.6, 1.4)),
}


def pose_lerp(p1, p2, t):
    a, b = POSES[p1], POSES[p2]
    return tuple(tuple(lerp(a[i][j], b[i][j], t) for j in range(2)) for i in range(2))


def dot(c, x, y, s=1.0, t=0.0, mouth=0.0, pose="idle", pose2=None, pose_t=0.0, walk=None,
        blink_seed=0, look=0.0, wave_amp=0.0, hold=None, alpha=1.0, extra=None):
    """Dot, full body. (x,y) = point between her feet. Height ~575*s.
    walk: phase in radians or None. wave_amp: forearm oscillation for waving."""
    if alpha < 1:
        c.push_group()
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    shadow(c, 0, 4, 120, 22, 0.22)
    bob = 0.0
    legL = legR = 0.0
    if walk is not None:
        bob = -abs(math.sin(walk)) * 10
        legL, legR = math.sin(walk) * 0.38, -math.sin(walk) * 0.38
    breathe = math.sin(t * 2.1) * 2.5
    c.translate(0, bob)
    # --- legs (dungarees) and boots
    for side, ang in ((-1, legL), (1, legR)):
        hip = (side * 30, -205)
        foot = (hip[0] + math.sin(ang) * 165, hip[1] + math.cos(ang) * 170)
        limb(c, hip[0], hip[1], foot[0], foot[1] - 12, 60, DENIM)
        fill_ink(c, lambda: rrect(c, foot[0] - 36 + side * 8, foot[1] - 24, 72, 36, 16), hx("6b4226"))
    # --- arms (back layer drawn after torso for front poses; simple: draw torso then arms)
    if pose2:
        (ra, la) = pose_lerp(pose, pose2, ease(pose_t))
    else:
        (ra, la) = POSES[pose]
    ra = (ra[0], ra[1] + math.sin(t * 9) * wave_amp)
    if walk is not None and pose == "idle" and not pose2:
        ra = (0.25 - math.sin(walk) * 0.35, 0.25)
        la = (0.25 + math.sin(walk) * 0.35, 0.25)
    # torso: shirt
    sh_y = -385 + breathe
    fill_ink(c, lambda: smooth(c, [(-74, sh_y + 14), (0, sh_y - 6), (74, sh_y + 14), (84, -270), (72, -200),
                                   (-72, -200), (-84, -270)]), CREAM)
    # dungaree bib + waist
    fill_ink(c, lambda: smooth(c, [(-54, -330 + breathe), (54, -330 + breathe), (62, -250), (76, -205),
                                   (80, -172), (0, -165), (-80, -172), (-76, -205), (-62, -250)]), DENIM)
    # straps + buttons
    for side in (-1, 1):
        stroke(c, lambda: (c.move_to(side * 40, -328 + breathe), c.line_to(side * 52, sh_y + 4)), INK, 14)
        stroke(c, lambda: (c.move_to(side * 40, -328 + breathe), c.line_to(side * 52, sh_y + 4)), DENIM, 8)
        circle(c, side * 34, -318 + breathe, 7, GOLD, 3)
    # pocket
    fill_ink(c, lambda: rrect(c, -24, -300 + breathe, 48, 34, 8), tint(DENIM, 0.15), 4, shading=0)
    # neckerchief (tomato)
    fill_ink(c, lambda: poly(c, [(-30, sh_y + 2), (30, sh_y + 2), (0, sh_y + 38)]), TOMATO, 4)
    # arms
    for side, (a1, a2) in ((1, ra), (-1, la)):
        p0, p1, p2 = arm_pts(side * 70, sh_y + 22, a1, a2, 95, 88, side)
        limb2(c, [p0, p1], 42, CREAM)
        limb2(c, [p1, p2], 36, CREAM)
        # cuff + hand
        circle(c, p2[0], p2[1], 21, SKIN, 5)
        if pose in ("finger",) and side == 1:
            limb(c, p2[0], p2[1], p2[0] + 0, p2[1] - 30, 9, SKIN, 4)
        if pose in ("point", "point_low") and side == 1:
            dxp, dyp = p2[0] - p1[0], p2[1] - p1[1]
            n = math.hypot(dxp, dyp) or 1
            limb(c, p2[0], p2[1], p2[0] + dxp / n * 26, p2[1] + dyp / n * 26, 9, SKIN, 4)
        if hold and side == hold[0]:
            hold[1](c, p2[0], p2[1])
    # --- head from portrait
    k = 75 / PORTRAIT_HEAD_R
    c.save()
    c.translate(look * 6, -462 + breathe)
    c.rotate(look * 0.06 + math.sin(t * 1.3) * 0.02)
    c.scale(k, k)
    c.translate(-32, -34)
    # neck
    fill_ink(c, lambda: rrect(c, 26, 50, 12, 14, 3), SKIN, 2)
    # hat crown (gold) behind brim with red band
    fill_ink(c, lambda: smooth(c, [(15, 20), (17, 9), (24, 3.5), (32, 2.5), (40, 3.5), (47, 9), (49, 20)]), GOLD,
             2.2, shading=0.12)
    fill_ink(c, lambda: (c.move_to(16, 15.5), c.curve_to(26, 13, 38, 13, 48, 15.5), c.line_to(48.5, 20),
                         c.curve_to(38, 18, 26, 18, 15.5, 20), c.close_path()), TOMATO, 1.6, shading=0)
    # face (portrait)
    c.new_sub_path(); c.arc(32, 34, 22, 0, 2 * math.pi)
    setc(c, SKIN); c.fill_preserve()
    g = cairo.LinearGradient(14, 20, 50, 56)
    g.add_color_stop_rgba(0.5, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.4, 0.15, 0.1, 0.13)
    c.set_source(g); c.fill_preserve()
    setc(c, INK, 0.9); c.set_line_width(2.0); c.stroke()
    # red band under brim (portrait path)
    c.move_to(8, 28); c.curve_to(10, 12, 54, 12, 56, 28); c.curve_to(50, 24, 38, 22, 32, 22)
    c.curve_to(26, 22, 14, 24, 8, 28); c.close_path()
    setc(c, TOMATO); c.fill_preserve(); setc(c, INK, 0.9); c.set_line_width(1.6); c.stroke()
    # gold brim (portrait ellipse)
    ellipse(c, 32, 20, 30, 6)
    setc(c, GOLD); c.fill_preserve(); setc(c, INK, 0.9); c.set_line_width(2.0); c.stroke()
    stroke(c, lambda: (c.move_to(8, 21), c.curve_to(20, 24.5, 44, 24.5, 56, 21)), shade(GOLD, 0.25), 1.0)
    # eyes with blink
    bl = blink(t, blink_seed)
    for ex in (24, 40):
        ellipse(c, ex + look * 1.5, 35, 3, max(0.45, 3 * (1 - bl)))
        setc(c, INK); c.fill()
        if bl < 0.5:
            c.arc(ex + look * 1.5 + 0.9, 34, 0.9, 0, 6.3); setc(c, WHITE, 0.9); c.fill()
    # cheeks
    for cx_ in (18, 46):
        c.arc(cx_, 42, 3, 0, 6.3); setc(c, CHEEK, 0.6); c.fill()
    # mouth: smile path, opens with loudness
    m = clamp(mouth)
    if m < 0.08:
        stroke(c, lambda: (c.move_to(24, 45), c.curve_to(26.7, 47, 37.3, 47, 40, 45)), INK, 3)
        c.move_to(24, 45); c.curve_to(29.3, 49, 34.7, 49, 40, 45)  # q8 6 16 0
        setc(c, INK); c.set_line_width(3); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    else:
        o = 1.5 + 6 * m
        wv = 16 - 3 * m
        c.move_to(32 - wv / 2, 45)
        c.curve_to(32 - wv / 2 + 2, 45 + o * 1.25, 32 + wv / 2 - 2, 45 + o * 1.25, 32 + wv / 2, 45)
        c.curve_to(32 + 2, 44.3, 32 - 2, 44.3, 32 - wv / 2, 45)
        c.close_path()
        setc(c, hx("7a1f2b")); c.fill_preserve()
        setc(c, INK); c.set_line_width(2.2); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
        if m > 0.35:
            ellipse(c, 32, 45 + o * 0.75, wv * 0.22, o * 0.25)
            setc(c, hx("e46a6a")); c.fill()
    c.restore()
    if extra:
        extra(c)
    c.restore()
    if alpha < 1:
        c.pop_group_to_source()
        c.paint_with_alpha(alpha)


def blink(t, seed=0):
    period = 3.7 + (seed % 5) * 0.31
    ph = (t + seed * 1.37) % period
    if ph < 0.07:
        return ph / 0.07
    if ph < 0.16:
        return 1 - (ph - 0.07) / 0.09
    return 0.0


# ---------------------------------------------------------------- villagers
HAIR = [hx("5a3a22"), hx("2b2118"), hx("c98a3d"), hx("8d8d8d"), hx("a0522d"), hx("e8d08a")]
COATS = [TOMATO, LEAF, SKY, GOLD, hx("8e5aa8"), hx("2f8f8a"), hx("d9734a"), hx("4b6cd8")]
SKINS = [hx("f1c8a0"), hx("d9a274"), hx("a8724a"), hx("f5d6b8"), hx("7d4f32")]


def person(c, x, y, s=1.0, t=0.0, seed=0, kid=False, coat=None, hair=None, skin=None, hat=None,
           pose=((0.2, 0.2), (0.2, 0.2)), walk=None, mouth=0.0, look=0.0, face=True, scarf=None,
           hold=None, bottom=None, apron=None, bob=0.0, back=False):
    """Generic villager. (x,y) feet. Height ~ 330*s adult, ~230*s kid. hat in
    {None,'cap','beanie','bun','straw','santa','bee','top','bowler','helmet'}."""
    coat = coat or COATS[seed % len(COATS)]
    hair = hair or HAIR[(seed * 7 + 1) % len(HAIR)]
    skin = skin or SKINS[(seed * 3 + 2) % len(SKINS)]
    bottom = bottom or [hx("39457a"), hx("5b4a3a"), hx("2e5d8f"), hx("6b6b7d")][seed % 4]
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    k = 0.72 if kid else 1.0
    shadow(c, 0, 3, 70 * k, 14 * k, 0.2)
    sw = 0.0
    legA = legB = 0.0
    if walk is not None:
        bob += -abs(math.sin(walk)) * 6
        legA, legB = math.sin(walk) * 0.4, -math.sin(walk) * 0.4
    c.translate(0, bob)
    hipy = -110 * k
    for side, ang in ((-1, legA), (1, legB)):
        hx_ = side * 16 * k
        fx, fy = hx_ + math.sin(ang) * 100 * k, hipy + math.cos(ang) * 104 * k
        limb(c, hx_, hipy, fx, fy - 6, 30 * k, bottom, 5)
        fill_ink(c, lambda: rrect(c, fx - 18 * k, fy - 14 * k, 36 * k, 20 * k, 8 * k), hx("4a3426"), 4)
    # body
    top = -235 * k
    fill_ink(c, lambda: smooth(c, [(-42 * k, top + 18 * k), (0, top), (42 * k, top + 18 * k), (48 * k, hipy + 6),
                                   (0, hipy + 18 * k), (-48 * k, hipy + 6)]), coat, 5)
    if apron:
        fill_ink(c, lambda: rrect(c, -28 * k, top + 40 * k, 56 * k, 100 * k, 10), apron, 4, shading=0)
    if scarf:
        fill_ink(c, lambda: rrect(c, -30 * k, top + 2, 60 * k, 20 * k, 9), scarf, 4)
    (ra, la) = pose
    if walk is not None and pose == ((0.2, 0.2), (0.2, 0.2)):
        ra = (0.2 - math.sin(walk) * 0.4, 0.2)
        la = (0.2 + math.sin(walk) * 0.4, 0.2)
    hands = {}
    for side, (a1, a2) in ((1, ra), (-1, la)):
        p0, p1, p2 = arm_pts(side * 38 * k, top + 22 * k, a1, a2, 58 * k, 56 * k, side)
        limb2(c, [p0, p1, p2], 22 * k, coat, 5)
        circle(c, p2[0], p2[1], 12 * k, skin, 4)
        hands[side] = p2
    if hold:
        hold(c, hands)
    # head
    hr = 52 * k if kid else 46
    hy = top - hr + 8
    if hat == "bun":
        circle(c, 0, hy - hr * 0.95, hr * 0.38, hair, 5)
    circle(c, 0, hy, hr, skin, 5)
    if back:
        fill_ink(c, lambda: (c.new_sub_path(), c.arc(0, hy, hr, 0, 2 * math.pi)), hair, 5)
    else:
        # hair cap
        fill_ink(c, lambda: (c.new_sub_path(), c.arc(0, hy, hr, math.pi * 1.05, math.pi * 1.95),
                             c.curve_to(hr * 0.5, hy - hr * 0.35, -hr * 0.5, hy - hr * 0.2, -hr * 0.98, hy - hr * 0.15)),
                 hair, 4, shading=0)
    if face and not back:
        ex = hr * 0.36
        bl = blink(t, seed)
        for sx in (-1, 1):
            ellipse(c, sx * ex + look * 4, hy + hr * 0.08, hr * 0.085, max(0.8, hr * 0.1 * (1 - bl)))
            setc(c, INK); c.fill()
        for sx in (-1, 1):
            c.arc(sx * hr * 0.58, hy + hr * 0.36, hr * 0.12, 0, 6.3); setc(c, CHEEK, 0.55); c.fill()
        if mouth > 0.1:
            oval(c, look * 3, hy + hr * 0.45, hr * 0.18, hr * 0.1 + hr * 0.18 * mouth, hx("7a1f2b"), 3, shading=0)
        else:
            stroke(c, lambda: (c.move_to(-hr * 0.25 + look * 3, hy + hr * 0.4),
                               c.curve_to(-hr * 0.1, hy + hr * 0.58, hr * 0.1, hy + hr * 0.58, hr * 0.25 + look * 3,
                                          hy + hr * 0.4)), INK, 4)
    if hat == "cap":
        fill_ink(c, lambda: (c.new_sub_path(), c.arc(0, hy - hr * 0.2, hr * 0.98, math.pi, 2 * math.pi), c.close_path()),
                 coat if coat != TOMATO else SKY, 4)
        fill_ink(c, lambda: rrect(c, -hr * 1.05, hy - hr * 0.3, hr * 1.5, hr * 0.22, 6), shade(coat, 0.2), 4)
    elif hat == "beanie":
        fill_ink(c, lambda: (c.new_sub_path(), c.arc(0, hy - hr * 0.15, hr * 1.0, math.pi, 2 * math.pi), c.close_path()),
                 COATS[(seed + 3) % len(COATS)], 4)
        circle(c, 0, hy - hr * 1.15, hr * 0.22, CREAM, 4)
    elif hat == "straw":
        oval(c, 0, hy - hr * 0.55, hr * 1.4, hr * 0.28, GOLD, 4)
        fill_ink(c, lambda: (c.new_sub_path(), c.arc(0, hy - hr * 0.62, hr * 0.7, math.pi, 2 * math.pi), c.close_path()),
                 GOLD, 4)
    elif hat == "santa":
        fill_ink(c, lambda: smooth(c, [(-hr, hy - hr * 0.4), (-hr * 0.2, hy - hr * 1.5), (hr * 0.9, hy - hr * 1.2),
                                       (hr, hy - hr * 0.4)]), TOMATO, 4)
        circle(c, hr * 0.95, hy - hr * 1.15, hr * 0.22, WHITE, 4)
        fill_ink(c, lambda: rrect(c, -hr * 1.05, hy - hr * 0.55, hr * 2.1, hr * 0.3, 10), WHITE, 4)
    elif hat == "top":
        fill_ink(c, lambda: rrect(c, -hr * 0.6, hy - hr * 1.7, hr * 1.2, hr * 1.1, 6), INK, 3, ink=INK)
        fill_ink(c, lambda: rrect(c, -hr * 1.0, hy - hr * 0.7, hr * 2.0, hr * 0.2, 5), INK, 3)
    elif hat == "bowler":
        fill_ink(c, lambda: (c.new_sub_path(), c.arc(0, hy - hr * 0.55, hr * 0.7, math.pi, 2 * math.pi), c.close_path()),
                 hx("3a3328"), 4)
        fill_ink(c, lambda: rrect(c, -hr * 1.0, hy - hr * 0.62, hr * 2.0, hr * 0.18, 5), hx("3a3328"), 4)
    elif hat == "bee":
        fill_ink(c, lambda: (c.new_sub_path(), c.arc(0, hy - hr * 0.2, hr * 1.12, math.pi, 2 * math.pi), c.close_path()),
                 CREAM, 4)
        oval(c, 0, hy - hr * 0.2, hr * 1.6, hr * 0.25, CREAM, 4)
        c.save()
        c.arc(0, hy + hr * 0.1, hr * 1.02, 0, 6.3)
        setc(c, INK, 0.35); c.fill()
        c.restore()
    elif hat == "helmet":
        fill_ink(c, lambda: (c.new_sub_path(), c.arc(0, hy - hr * 0.1, hr * 1.05, math.pi, 2 * math.pi), c.close_path()),
                 GOLD, 4)
    c.restore()
    return hands


# ---------------------------------------------------------------- animals
def wool(c, cx, cy, rx, ry, col=CREAM, n=9, lw=5, seed=0):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        pts.append((cx + math.cos(a) * rx, cy + math.sin(a) * ry))
    r = (rx + ry) / 2 * 0.42

    def path():
        for (px, py) in pts:
            c.new_sub_path(); c.arc(px, py, r, 0, 2 * math.pi)
        ellipse(c, cx, cy, rx, ry)
    # outline pass then fill pass so overlaps merge
    path(); setc(c, INK, 0.92); c.set_line_width(lw * 2); c.stroke()
    path(); setc(c, col); c.fill()
    g = cairo.LinearGradient(cx - rx, cy - ry, cx + rx * 0.6, cy + ry * 1.3)
    g.add_color_stop_rgba(0.5, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.1, 0.1, 0.3, 0.14)
    path(); c.set_source(g); c.fill()


def sheep(c, x, y, s=1.0, t=0.0, face_col=hx("2d2a33"), body=CREAM, lamb=False, flip=False, legs=True,
          bleat=0.0, seed=0, wool_amt=1.0):
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    k = 0.62 if lamb else 1.0
    shadow(c, 0, 2, 90 * k, 14 * k, 0.2)
    bob = math.sin(t * 3 + seed) * 2
    if legs:
        for lx in (-48, -24, 26, 50):
            limb(c, lx * k, -40 * k, lx * k + math.sin(t * 2 + lx) * 1.5, -2, 12 * k, face_col, 4)
    rx = 80 * k * (0.55 + 0.45 * wool_amt)
    wool(c, 0, -80 * k + bob, rx, 48 * k * (0.6 + 0.4 * wool_amt), body, seed=seed)
    # head
    hx_, hy_ = 82 * k * (0.6 + 0.4 * wool_amt), -96 * k + bob + math.sin(t * 1.7 + seed) * 4
    oval(c, hx_ - 10 * k, hy_ - 8 * k, 16 * k, 8 * k, face_col, 4)  # ear
    oval(c, hx_, hy_, 26 * k, 32 * k, face_col, 5)
    circle(c, hx_ + 8 * k, hy_ - 6 * k, 4.5 * k, WHITE, 0)
    circle(c, hx_ + 9 * k, hy_ - 6 * k, 2.5 * k, INK, 0)
    wool(c, hx_ - 4 * k, hy_ - 30 * k, 16 * k, 9 * k, body, n=5, lw=4)
    if bleat > 0.1:
        oval(c, hx_ + 10 * k, hy_ + 18 * k, 7 * k, 7 * k * bleat, hx("7a1f2b"), 3, shading=0)
    c.restore()


def goat(c, x, y, s=1.0, t=0.0, col=CREAM, flip=False, coat=None, seed=0, pose="stand"):
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    shadow(c, 0, 2, 80, 12, 0.2)
    bob = math.sin(t * 3.3 + seed) * 2.5
    patch = [hx("8a5a3a"), hx("2d2a33"), CREAM][seed % 3]
    for lx in (-44, -24, 26, 46):
        lift = 8 * max(0, math.sin(t * 4 + lx)) if pose == "trot" else 0
        limb(c, lx, -48, lx, -2 - lift, 11, col, 4)
        oval(c, lx, -4 - lift, 7, 5, INK, 0)
    fill_ink(c, lambda: smooth(c, [(-62, -70 + bob), (-20, -98 + bob), (40, -100 + bob), (66, -76 + bob),
                                   (58, -46 + bob), (-56, -44 + bob)]), col)
    fill_ink(c, lambda: ellipse(c, -10, -78 + bob, 24, 16), patch, 0, shading=0)
    if coat:
        fill_ink(c, lambda: smooth(c, [(-44, -96 + bob), (36, -100 + bob), (44, -58 + bob), (-40, -54 + bob)]),
                 coat, 5)
        stroke(c, lambda: (c.move_to(-40, -66 + bob), c.line_to(42, -68 + bob)), shade(coat, 0.3), 4)
    # tail
    stroke(c, lambda: (c.move_to(-60, -82 + bob), c.line_to(-74, -100 + bob + math.sin(t * 12) * 4)), INK, 8)
    # head
    hb = math.sin(t * 2.3 + seed) * 5
    neckx, necky = 56, -88 + bob
    hx_, hy_ = 82, -126 + bob + hb
    limb(c, neckx, necky, hx_ - 6, hy_ + 10, 30, col, 5)
    # horns
    stroke(c, lambda: (c.move_to(hx_ - 10, hy_ - 22), c.curve_to(hx_ - 22, hy_ - 44, hx_ - 34, hy_ - 40, hx_ - 36, hy_ - 30)),
           INK, 11)
    stroke(c, lambda: (c.move_to(hx_ - 10, hy_ - 22), c.curve_to(hx_ - 22, hy_ - 44, hx_ - 34, hy_ - 40, hx_ - 36, hy_ - 30)),
           hx("b8a58a"), 6)
    oval(c, hx_ - 18, hy_ - 4, 18, 7, col, 4)  # ear
    fill_ink(c, lambda: smooth(c, [(hx_ - 18, hy_ - 18), (hx_ + 8, hy_ - 24), (hx_ + 30, hy_ + 2), (hx_ + 28, hy_ + 18),
                                   (hx_ + 6, hy_ + 18), (hx_ - 16, hy_ + 6)]), col)
    fill_ink(c, lambda: poly(c, [(hx_ + 10, hy_ + 16), (hx_ + 22, hy_ + 16), (hx_ + 14, hy_ + 36)]), col, 4)  # beard
    circle(c, hx_ + 6, hy_ - 6, 5, WHITE, 2)
    stroke(c, lambda: (c.move_to(hx_ + 2, hy_ - 6), c.line_to(hx_ + 10, hy_ - 6)), INK, 3)
    circle(c, hx_ + 26, hy_ + 6, 2.5, INK, 0)
    c.restore()


def reindeer(c, x, y, s=1.0, t=0.0, flip=False, seed=0, chew=0.0):
    col = hx("9a6a44")
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    shadow(c, 0, 2, 100, 15, 0.2)
    for lx in (-56, -30, 34, 58):
        limb(c, lx, -70, lx, -4, 14, col, 4)
        oval(c, lx, -6, 9, 6, INK, 0)
    fill_ink(c, lambda: smooth(c, [(-76, -100), (-20, -132), (52, -132), (82, -100), (70, -64), (-70, -62)]), col)
    fill_ink(c, lambda: ellipse(c, -60, -100, 18, 14), CREAM, 4)
    hb = math.sin(t * 1.9 + seed) * 4
    hx_, hy_ = 104, -176 + hb
    limb(c, 66, -112, hx_ - 8, hy_ + 16, 40, col, 5)
    for sgn in (-1, 1):
        stroke(c, lambda: (c.move_to(hx_ + sgn * 8, hy_ - 26), c.curve_to(hx_ + sgn * 20, hy_ - 70, hx_ + sgn * 50,
                                                                        hy_ - 80, hx_ + sgn * 54, hy_ - 100)), INK, 12)
        stroke(c, lambda: (c.move_to(hx_ + sgn * 8, hy_ - 26), c.curve_to(hx_ + sgn * 20, hy_ - 70, hx_ + sgn * 50,
                                                                        hy_ - 80, hx_ + sgn * 54, hy_ - 100)), hx("e7d3ad"), 6)
        stroke(c, lambda: (c.move_to(hx_ + sgn * 22, hy_ - 64), c.line_to(hx_ + sgn * 4, hy_ - 86)), INK, 10)
        stroke(c, lambda: (c.move_to(hx_ + sgn * 22, hy_ - 64), c.line_to(hx_ + sgn * 4, hy_ - 86)), hx("e7d3ad"), 5)
    fill_ink(c, lambda: smooth(c, [(hx_ - 26, hy_ - 10), (hx_ + 4, hy_ - 32), (hx_ + 36, hy_ - 6), (hx_ + 40, hy_ + 18),
                                   (hx_ + 6, hy_ + 26), (hx_ - 20, hy_ + 12)]), col)
    oval(c, hx_ - 22, hy_ - 18, 16, 8, col, 4)
    circle(c, hx_ + 40, hy_ + 10 + chew * 3, 9, TOMATO, 4)
    circle(c, hx_ + 8, hy_ - 8, 5, INK, 0)
    c.restore()


def cow(c, x, y, s=1.0, t=0.0, flip=False, seed=0, brush=0.0):
    """Highland cow: shaggy ginger, wide horns."""
    col = hx("c4692c")
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    shadow(c, 0, 2, 120, 16, 0.2)
    for lx in (-66, -38, 40, 66):
        limb(c, lx, -70, lx, -4, 20, shade(col, 0.1), 5)
    fill_ink(c, lambda: smooth(c, [(-96, -110), (-40, -160), (60, -160), (100, -120), (90, -66), (-88, -60)]), col)
    for i in range(12):  # shaggy fringe
        fx = -84 + i * 15
        stroke(c, lambda: (c.move_to(fx, -74), c.line_to(fx + 4 + math.sin(t * 2 + i) * 2, -54)), shade(col, 0.2), 6)
    hb = math.sin(t * 1.5 + seed) * 4 + brush * 6
    hx_, hy_ = 116, -130 + hb
    for sgn in (-1, 1):
        stroke(c, lambda: (c.move_to(hx_, hy_ - 20), c.curve_to(hx_ + sgn * 40, hy_ - 30, hx_ + sgn * 70, hy_ - 50,
                                                                hx_ + sgn * 66, hy_ - 82)), INK, 16)
        stroke(c, lambda: (c.move_to(hx_, hy_ - 20), c.curve_to(hx_ + sgn * 40, hy_ - 30, hx_ + sgn * 70, hy_ - 50,
                                                                hx_ + sgn * 66, hy_ - 82)), hx("efe2c4"), 9)
    fill_ink(c, lambda: smooth(c, [(hx_ - 34, hy_ - 20), (hx_ + 30, hy_ - 26), (hx_ + 42, hy_ + 20), (hx_ + 20, hy_ + 50),
                                   (hx_ - 20, hy_ + 50), (hx_ - 40, hy_ + 18)]), col)
    oval(c, hx_, hy_ + 40, 30, 18, hx("e9a98a"), 5)
    circle(c, hx_ - 10, hy_ + 40, 3, INK, 0); circle(c, hx_ + 10, hy_ + 40, 3, INK, 0)
    # fringe over eyes
    fill_ink(c, lambda: smooth(c, [(hx_ - 36, hy_ - 14), (hx_, hy_ - 30), (hx_ + 36, hy_ - 14), (hx_ + 24, hy_ + 10),
                                   (hx_ + 8, hy_ + 2), (hx_ - 6, hy_ + 12), (hx_ - 22, hy_ + 4)]), shade(col, 0.12), 4)
    c.restore()


def chicken(c, x, y, s=1.0, t=0.0, flip=False, col=CREAM, seed=0, peck=0.0):
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    shadow(c, 0, 2, 34, 6, 0.2)
    for lx in (-8, 8):
        stroke(c, lambda: (c.move_to(lx, -24), c.line_to(lx, 0)), hx("e09a2a"), 5)
    p = peck if peck else max(0, math.sin(t * 3 + seed * 2)) ** 6
    c.save(); c.translate(0, -40)
    oval(c, 0, 0, 34, 26, col, 5)
    stroke(c, lambda: (c.move_to(-30, -6), c.line_to(-46, -26)), col, 14)
    stroke(c, lambda: (c.move_to(-4, -2), c.curve_to(6, 6, 16, 4, 20, -6)), shade(col, 0.2), 4)
    c.rotate(p * 0.9)
    circle(c, 26, -24, 16, col, 5)
    fill_ink(c, lambda: poly(c, [(38, -26), (52, -21), (38, -16)]), GOLD, 3)
    fill_ink(c, lambda: (c.arc(22, -40, 6, 0, 6.3), c.arc(30, -40, 6, 0, 6.3)), TOMATO, 3)
    circle(c, 30, -27, 2.8, INK, 0)
    c.restore()
    c.restore()


def chick(c, x, y, s=1.0, t=0.0, seed=0):
    hop = max(0, math.sin(t * 5 + seed * 1.7)) * 8
    c.save(); c.translate(x, y - hop); c.scale(s, s)
    circle(c, 0, -18, 18, hx("ffd84a"), 4)
    circle(c, 8, -32, 11, hx("ffd84a"), 4)
    fill_ink(c, lambda: poly(c, [(17, -33), (25, -30), (17, -27)]), hx("e09a2a"), 2)
    circle(c, 11, -34, 2, INK, 0)
    c.restore()


def dog(c, x, y, s=1.0, t=0.0, flip=False, run=0.0):
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    shadow(c, 0, 2, 60, 10, 0.2)
    for i, lx in enumerate((-34, -18, 22, 38)):
        a = math.sin(t * 12 + i * 1.6) * 0.5 * run
        limb(c, lx, -36, lx + math.sin(a) * 30, -2, 10, INK, 3)
    fill_ink(c, lambda: smooth(c, [(-48, -50), (0, -70), (44, -60), (46, -34), (-44, -32)]), hx("2a2a35"))
    fill_ink(c, lambda: smooth(c, [(10, -66), (40, -60), (40, -36), (16, -40)]), WHITE, 0, shading=0)
    stroke(c, lambda: (c.move_to(-46, -52), c.curve_to(-60, -60, -66, -80 + math.sin(t * 14) * 6, -58, -84)), hx("2a2a35"),
           10)
    hx_, hy_ = 56, -80
    fill_ink(c, lambda: smooth(c, [(hx_ - 18, hy_ - 10), (hx_ + 6, hy_ - 20), (hx_ + 30, hy_ + 2), (hx_ + 14, hy_ + 14),
                                   (hx_ - 12, hy_ + 12)]), hx("2a2a35"))
    fill_ink(c, lambda: smooth(c, [(hx_, hy_ - 14), (hx_ + 30, hy_ + 2), (hx_ + 12, hy_ + 12)]), WHITE, 0, shading=0)
    oval(c, hx_ - 10, hy_ - 4, 8, 16, hx("2a2a35"), 4)
    circle(c, hx_ + 6, hy_ - 6, 3, WHITE, 0); circle(c, hx_ + 7, hy_ - 6, 2, INK, 0)
    circle(c, hx_ + 30, hy_ + 2, 4, INK, 0)
    c.restore()


def bee(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for sgn in (-1, 1):
        oval(c, sgn * 4, -12 - abs(math.sin(t * 40)) * 3, 8, 12, (1, 1, 1, 0.7), 2, shading=0)
    oval(c, 0, 0, 14, 10, GOLD, 3)
    stroke(c, lambda: (c.move_to(-3, -9), c.line_to(-3, 9)), INK, 3)
    stroke(c, lambda: (c.move_to(4, -8), c.line_to(4, 8)), INK, 3)
    c.restore()
