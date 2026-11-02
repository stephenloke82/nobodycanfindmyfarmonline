"""Sarah, the host of video 008: a young farm host with an auburn ponytail, a leaf-green shirt, jeans
and boots. Same storybook construction as Dot (chars.py) so she moves with the same poses."""
import math
import cairo
from gfx import *
from chars import limb, limb2, arm_pts, POSES, pose_lerp, blink

HAIR = hx("8a4526")
HAIR_HI = hx("b5643a")
SHIRT = hx("3f8f3a")
JEANS = hx("2f4fa8")
BOOT = hx("6b4226")
SKIN_S = hx("f3cba6")


def _ponytail(c, t, swing):
    a = math.sin(t * 2.3) * 0.08 + swing
    c.save()
    c.translate(52, 22)
    c.rotate(a)
    fill_ink(c, lambda: smooth(c, [(-2, -3), (9, -2), (15, 10), (14, 24), (8, 34), (4, 26), (2, 12)]), HAIR,
             1.8, shading=0.18)
    stroke(c, lambda: (c.move_to(6, 4), c.curve_to(11, 12, 11, 20, 7, 28)), HAIR_HI, 1.0)
    c.restore()
    # gold scrunchie
    ellipse(c, 52.5, 21.5, 3.2, 4.2)
    setc(c, GOLD); c.fill_preserve(); setc(c, INK, 0.9); c.set_line_width(1.4); c.stroke()


def sarah(c, x, y, s=1.0, t=0.0, mouth=0.0, pose="idle", pose2=None, pose_t=0.0, walk=None,
          blink_seed=0, look=0.0, wave_amp=0.0, hold=None, alpha=1.0, extra=None):
    """Sarah, full body. (x,y) = point between her feet. Height ~560*s."""
    if alpha < 1:
        c.push_group()
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    shadow(c, 0, 4, 110, 20, 0.22)
    bob = 0.0
    legL = legR = 0.0
    if walk is not None:
        bob = -abs(math.sin(walk)) * 10
        legL, legR = math.sin(walk) * 0.38, -math.sin(walk) * 0.38
    breathe = math.sin(t * 2.1) * 2.5
    c.translate(0, bob)
    # legs (jeans) and boots
    for side, ang in ((-1, legL), (1, legR)):
        hip = (side * 26, -210)
        foot = (hip[0] + math.sin(ang) * 165, hip[1] + math.cos(ang) * 172)
        limb(c, hip[0], hip[1], foot[0], foot[1] - 14, 54, JEANS)
        fill_ink(c, lambda: rrect(c, foot[0] - 34 + side * 8, foot[1] - 30, 68, 40, 15), BOOT)
        stroke(c, lambda: (c.move_to(foot[0] - 30 + side * 8, foot[1] - 14), c.line_to(foot[0] + 30 + side * 8,
                                                                                       foot[1] - 14)),
               shade(BOOT, 0.3), 3)
    if pose2:
        (ra, la) = pose_lerp(pose, pose2, ease(pose_t))
    else:
        (ra, la) = POSES[pose]
    ra = (ra[0], ra[1] + math.sin(t * 9) * wave_amp)
    if walk is not None and pose == "idle" and not pose2:
        ra = (0.25 - math.sin(walk) * 0.35, 0.25)
        la = (0.25 + math.sin(walk) * 0.35, 0.25)
    sh_y = -380 + breathe
    # hips / belt
    fill_ink(c, lambda: smooth(c, [(-66, -236), (66, -236), (70, -196), (0, -188), (-70, -196)]), JEANS)
    fill_ink(c, lambda: rrect(c, -68, -240, 136, 18, 8), hx("6b4226"), 4, shading=0)
    fill_ink(c, lambda: rrect(c, -12, -242, 24, 22, 5), GOLD, 3, shading=0)
    # shirt (leaf green, rolled sleeves, open collar over a cream tee)
    fill_ink(c, lambda: smooth(c, [(-70, sh_y + 14), (0, sh_y - 6), (70, sh_y + 14), (78, -280), (70, -232),
                                   (-70, -232), (-78, -280)]), SHIRT)
    fill_ink(c, lambda: poly(c, [(-22, sh_y + 2), (22, sh_y + 2), (0, sh_y + 46)]), CREAM, 4, shading=0)
    for side in (-1, 1):
        fill_ink(c, lambda: poly(c, [(side * 22, sh_y + 2), (side * 44, sh_y + 8), (side * 8, sh_y + 52)]),
                 tint(SHIRT, 0.12), 4, shading=0)
    # placket + buttons + pocket
    stroke(c, lambda: (c.move_to(0, sh_y + 46), c.line_to(0, -238)), shade(SHIRT, 0.35), 3)
    for by in (-320, -290, -262):
        circle(c, 0, by + breathe * 0.5, 4.5, CREAM, 2)
    fill_ink(c, lambda: rrect(c, -56, -330 + breathe, 34, 30, 6), tint(SHIRT, 0.1), 3.5, shading=0)
    # arms: green sleeve to the elbow, then skin
    for side, (a1, a2) in ((1, ra), (-1, la)):
        p0, p1, p2 = arm_pts(side * 66, sh_y + 24, a1, a2, 92, 86, side)
        limb2(c, [p0, p1], 40, SHIRT)
        # rolled cuff
        circle(c, p1[0], p1[1], 20, tint(SHIRT, 0.15), 4)
        limb2(c, [p1, p2], 30, SKIN_S)
        circle(c, p2[0], p2[1], 19, SKIN_S, 5)
        if pose in ("finger",) and side == 1:
            limb(c, p2[0], p2[1], p2[0] + 0, p2[1] - 30, 9, SKIN_S, 4)
        if pose in ("point", "point_low") and side == 1:
            dxp, dyp = p2[0] - p1[0], p2[1] - p1[1]
            n = math.hypot(dxp, dyp) or 1
            limb(c, p2[0], p2[1], p2[0] + dxp / n * 26, p2[1] + dyp / n * 26, 9, SKIN_S, 4)
        if pose == "thumb" and side == 1:
            limb(c, p2[0], p2[1], p2[0] + 4, p2[1] - 30, 10, SKIN_S, 4)
        if hold and side == hold[0]:
            hold[1](c, p2[0], p2[1])
    # head (64x64 portrait space, face circle at 32,34 r22)
    k = 72 / 22.0
    c.save()
    c.translate(look * 6, -456 + breathe)
    c.rotate(look * 0.06 + math.sin(t * 1.3) * 0.02)
    c.scale(k, k)
    c.translate(-32, -34)
    swing = 0.18 * math.sin(walk) if walk is not None else 0.0
    _ponytail(c, t, swing)
    # back hair mass
    fill_ink(c, lambda: smooth(c, [(9, 34), (10, 18), (20, 9), (32, 6), (44, 9), (54, 18), (55, 34), (50, 40),
                                   (14, 40)]), HAIR, 2.0, shading=0.15)
    # neck
    fill_ink(c, lambda: rrect(c, 26, 50, 12, 13, 3), SKIN_S, 2)
    # face
    c.new_sub_path(); c.arc(32, 35, 21, 0, 2 * math.pi)
    setc(c, SKIN_S); c.fill_preserve()
    g = cairo.LinearGradient(14, 20, 50, 56)
    g.add_color_stop_rgba(0.5, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.4, 0.15, 0.1, 0.13)
    c.set_source(g); c.fill_preserve()
    setc(c, INK, 0.9); c.set_line_width(2.0); c.stroke()
    # side-swept fringe
    fill_ink(c, lambda: smooth(c, [(11, 30), (13, 18), (22, 11), (34, 10), (46, 13), (53, 22), (53, 27),
                                   (44, 21), (33, 22), (24, 26), (16, 33)]), HAIR, 1.8, shading=0.1)
    stroke(c, lambda: (c.move_to(22, 14), c.curve_to(30, 13, 40, 14, 48, 19)), HAIR_HI, 1.2)
    # ears + small gold earrings
    for ex_, sgn in ((11, -1), (53, 1)):
        ellipse(c, ex_, 37, 3, 4.2)
        setc(c, SKIN_S); c.fill_preserve(); setc(c, INK, 0.9); c.set_line_width(1.6); c.stroke()
        c.arc(ex_ + sgn * 0.3, 42.5, 1.4, 0, 6.3); setc(c, GOLD); c.fill()
    # brows
    for bx_ in (24, 40):
        stroke(c, lambda: (c.move_to(bx_ - 4, 29.5), c.curve_to(bx_ - 1.5, 28, bx_ + 1.5, 28, bx_ + 4, 29.5)),
               shade(HAIR, 0.2), 1.6)
    # eyes with blink + lashes
    bl = blink(t, blink_seed)
    for ex in (24, 40):
        ellipse(c, ex + look * 1.5, 35.5, 2.9, max(0.45, 3.2 * (1 - bl)))
        setc(c, INK); c.fill()
        if bl < 0.5:
            c.arc(ex + look * 1.5 + 0.9, 34.4, 0.9, 0, 6.3); setc(c, WHITE, 0.9); c.fill()
            side = -1 if ex < 32 else 1
            stroke(c, lambda: (c.move_to(ex + side * 2.6, 33.4), c.line_to(ex + side * 4.2, 32.2)), INK, 1.1)
    # nose hint + freckles
    stroke(c, lambda: (c.move_to(32, 38), c.curve_to(33.2, 40, 32.5, 41, 31, 41)), shade(SKIN_S, 0.3), 1.0)
    for fx_, fy_ in ((19, 40), (21.5, 41.5), (43, 40), (45.5, 41.5)):
        c.arc(fx_, fy_, 0.55, 0, 6.3); setc(c, hx("c9875a"), 0.8); c.fill()
    for cx_ in (18, 46):
        c.arc(cx_, 43, 3, 0, 6.3); setc(c, CHEEK, 0.55); c.fill()
    # mouth
    m = clamp(mouth)
    if m < 0.08:
        c.move_to(25, 46); c.curve_to(29.6, 50, 34.4, 50, 39, 46)
        setc(c, INK); c.set_line_width(2.8); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    else:
        o = 1.5 + 6 * m
        wv = 15 - 3 * m
        c.move_to(32 - wv / 2, 46)
        c.curve_to(32 - wv / 2 + 2, 46 + o * 1.25, 32 + wv / 2 - 2, 46 + o * 1.25, 32 + wv / 2, 46)
        c.curve_to(32 + 2, 45.3, 32 - 2, 45.3, 32 - wv / 2, 46)
        c.close_path()
        setc(c, hx("7a1f2b")); c.fill_preserve()
        setc(c, INK); c.set_line_width(2.1); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
        if m > 0.35:
            ellipse(c, 32, 46 + o * 0.75, wv * 0.22, o * 0.25)
            setc(c, hx("e46a6a")); c.fill()
    c.restore()
    if extra:
        extra(c)
    c.restore()
    if alpha < 1:
        c.pop_group_to_source()
        c.paint_with_alpha(alpha)


POSES.setdefault("thumb", ((1.3, 2.0), (0.2, 0.2)))
