"""Final encode: build/video_noaudio.mp4 (high-quality intermediate) + build/mix.wav ->
output/video-008-nobody-can-find-my-farm-online.mp4. H.264 High, yuv420p, 30 fps, AAC 192 kb/s, faststart.
Starts at CRF 27 and raises CRF (never lowers resolution) until the file is under 92 MB."""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from beats import ROOT
B = os.path.join(ROOT, "build")
out = os.path.join(ROOT, "output", "video-008-nobody-can-find-my-farm-online.mp4")
os.makedirs(os.path.dirname(out), exist_ok=True)
LIMIT = 92e6
crf = int(sys.argv[1]) if len(sys.argv) > 1 else 27
while True:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(B, "video_noaudio.mp4"), "-i", os.path.join(B, "mix.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-tune", "animation",
                    "-crf", str(crf), "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30", "-g", "300",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", "-movflags", "+faststart", out], check=True)
    size = os.path.getsize(out)
    print(f"CRF {crf}: {size / 1e6:.1f} MB", flush=True)
    if size < LIMIT:
        break
    crf += 1
open(os.path.join(B, "final_crf.txt"), "w").write(str(crf))
