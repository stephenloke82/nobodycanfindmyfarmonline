"""Re-render the last of the 4 render chunks (after a change late in the video) in 4 parallel parts and re-join."""
import os, sys, subprocess
from multiprocessing import Process
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import timeline
from render import render_range, BUILD

scenes = timeline.build()
total = scenes[-1].start_frame + scenes[-1].frames
target = total * 3 // 4
b3 = min((S.start_frame for S in scenes), key=lambda x: abs(x - target))
parts = [b3 + (total - b3) * k // 4 for k in range(5)]
outs, procs = [], []
for k in range(4):
    o = os.path.join(BUILD, "chunks", f"tail{k}.mp4"); outs.append(o)
    p = Process(target=render_range, args=(scenes, parts[k], parts[k + 1], o, 16)); p.start(); procs.append(p)
for p in procs:
    p.join()
lst = os.path.join(BUILD, "chunks", "list2.txt")
with open(lst, "w") as f:
    for k in range(3):
        f.write(f"file '{os.path.join(BUILD, 'chunks', f'chunk{k}.mp4')}'\n")
    for o in outs:
        f.write(f"file '{o}'\n")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                os.path.join(BUILD, "video_noaudio.mp4")], check=True)
print("tail re-rendered from frame", b3)
