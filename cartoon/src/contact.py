"""Render one still per scene and tile them into output/contact-sheet.jpg.
Usage: python3 src/contact.py [out.jpg] [frac]   (frac = point in each scene, default key times)"""
import os, sys
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import timeline
from render import still, BUILD
from beats import ROOT

FRAC = float(sys.argv[2]) if len(sys.argv) > 2 else None


def key_time(S):
    if FRAC is not None:
        return S.dur * FRAC
    # after the last on-screen element has arrived (tag / last phrase), but before the end
    if S.ph:
        return min(S.dur - 0.2, max(S.ph[-1] + 0.9, S.dur * 0.6))
    return S.dur * 0.7


def job(i):
    scenes = timeline.build()
    S = scenes[i]
    p = os.path.join(BUILD, "contact", f"{i:02d}_{S.id}.png")
    still(scenes, S.id, key_time(S), p)
    return p


if __name__ == "__main__":
    os.makedirs(os.path.join(BUILD, "contact"), exist_ok=True)
    n = len(timeline.build())
    with Pool(4) as pool:
        paths = pool.map(job, range(n))
    from PIL import Image, ImageDraw, ImageFont
    cols, w = 7, 384
    h = 216
    rows = (n + cols - 1) // cols
    M = Image.new("RGB", (cols * w + (cols + 1) * 8, rows * (h + 30) + 8), (255, 248, 232))
    d = ImageDraw.Draw(M)
    try:
        f = ImageFont.truetype(os.path.expanduser("~/.fonts/DotBody.ttf"), 20)
    except Exception:
        f = None
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS)
        x, y = 8 + (i % cols) * (w + 8), 8 + (i // cols) * (h + 30)
        M.paste(im, (x, y))
        d.text((x, y + h + 3), os.path.basename(p)[3:-4], fill=(27, 31, 58), font=f)
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "output", "contact-sheet.jpg")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    M.save(out, quality=86)
    print(out)
