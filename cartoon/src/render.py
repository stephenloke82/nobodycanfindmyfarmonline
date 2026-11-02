"""Render frames. Usage:
  python3 src/render.py still ID[@t] ...      -> build/stills/ID_t.png
  python3 src/render.py video [--workers N]   -> build/video_noaudio.mp4
"""
import os, sys, subprocess, time, math
import cairo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gfx import W, H, FPS, paper_texture, vignette_overlay
import timeline
from beats import ROOT
import common
import scenes008  # noqa: register scenes

BUILD = os.path.join(ROOT, "build")
GRAIN = float(os.environ.get("GRAIN", "0.5"))
_overlays = {}


def overlays():
    if not _overlays:
        _overlays["paper"] = paper_texture()
        _overlays["vig"] = vignette_overlay()
    return _overlays


def draw_scene(c, S, t):
    fn = common.SCENES.get(S.id)
    c.save()
    if fn is None:
        c.set_source_rgb(0.98, 0.95, 0.88); c.paint()
        from gfx import text, DISPLAY, INK
        text(c, f"{S.id} (todo)", 960, 540, 80, DISPLAY, INK, "center")
    else:
        fn(c, t, S)
    c.restore()
    ov = overlays()
    if GRAIN:
        c.set_source_surface(ov["paper"], 0, 0); c.paint_with_alpha(GRAIN)
    c.set_source_surface(ov["vig"], 0, 0); c.paint()


def find(scenes, bid):
    return next(S for S in scenes if S.id == bid)


def still(scenes, bid, t, path):
    S = find(scenes, bid)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(surf)
    draw_scene(c, S, t)
    surf.write_to_png(path)
    return surf


def render_range(scenes, f0, f1, out, crf):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    c = cairo.Context(surf)
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-tune", "animation", "-crf", str(crf),
           "-profile:v", "high", "-pix_fmt", "yuv420p", "-g", "60", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    si = 0
    t0 = time.time()
    for f in range(f0, f1):
        while not (scenes[si].start_frame <= f < scenes[si].start_frame + scenes[si].frames):
            si += 1
        S = scenes[si]
        draw_scene(c, S, (f - S.start_frame) / FPS)
        surf.flush()
        p.stdin.write(bytes(surf.get_data()))
        if (f - f0) % 300 == 0:
            print(f"[{os.getpid()}] frame {f} ({f - f0}/{f1 - f0}) {time.time() - t0:.0f}s", flush=True)
    p.stdin.close()
    p.wait()


def video(workers=4, crf=20):
    from multiprocessing import Process
    scenes = timeline.build()
    total = scenes[-1].start_frame + scenes[-1].frames
    os.makedirs(os.path.join(BUILD, "chunks"), exist_ok=True)
    # split on scene boundaries near equal chunks
    bounds = [0]
    for k in range(1, workers):
        target = total * k // workers
        bounds.append(min((S.start_frame for S in scenes), key=lambda x: abs(x - target)))
    bounds.append(total)
    procs, outs = [], []
    for k in range(workers):
        out = os.path.join(BUILD, "chunks", f"chunk{k}.mp4")
        outs.append(out)
        pr = Process(target=render_range, args=(scenes, bounds[k], bounds[k + 1], out, crf))
        pr.start(); procs.append(pr)
    for pr in procs:
        pr.join()
        if pr.exitcode != 0:
            raise SystemExit("worker failed")
    lst = os.path.join(BUILD, "chunks", "list.txt")
    with open(lst, "w") as f:
        for o in outs:
            f.write(f"file '{o}'\n")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    os.path.join(BUILD, "video_noaudio.mp4")], check=True)
    print("frames", total)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "still":
        scenes = timeline.build()
        os.makedirs(os.path.join(BUILD, "stills"), exist_ok=True)
        for arg in sys.argv[2:]:
            bid, _, ts = arg.partition("@")
            S = find(scenes, bid)
            t = float(ts) if ts else S.dur * 0.7
            p = os.path.join(BUILD, "stills", f"{bid}_{t:.1f}.png")
            t0 = time.time()
            still(scenes, bid, t, p)
            print(p, f"{time.time() - t0:.2f}s")
    elif mode == "video":
        w = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4
        crf = int(sys.argv[sys.argv.index("--crf") + 1]) if "--crf" in sys.argv else 20
        video(w, crf)
