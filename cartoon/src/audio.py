"""Narration-only soundtrack (no music, no sound effects, at Stephen's request): place each beat's mastered
narration at its scene time, then two-pass loudnorm to -14 LUFS with true peak under -1 dB -> build/mix.wav."""
import os, sys, json, subprocess
import numpy as np
import soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import timeline
from beats import ROOT

SR = 44100
BUILD = os.path.join(ROOT, "build")


def build_mix():
    scenes = timeline.build()
    total = timeline.total_duration(scenes)
    N = int(total * SR) + SR
    voice = np.zeros(N)
    for S in scenes:
        x, sr = sf.read(S.audio)
        assert sr == SR
        i = int(round((S.start + S.voice_off) * SR))
        voice[i:i + len(x)] += x
    voice = voice[: int(total * SR)]
    mix = np.stack([voice, voice], 1)
    src = os.path.join(BUILD, "premix.wav")
    sf.write(src, mix.astype(np.float32), SR, subtype="FLOAT")
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", "loudnorm=I=-14:TP=-2.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    js = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    af = ("loudnorm=I=-14:TP=-2.5:LRA=11:linear=true:measured_I={input_i}:measured_TP={input_tp}:"
          "measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}").format(**js)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", af + ",alimiter=limit=0.72:level=false",
                    "-ar", str(SR), "-c:a", "pcm_s16le", os.path.join(BUILD, "mix.wav")], check=True)
    print("mix written", round(total, 2), "s")


if __name__ == "__main__":
    build_mix()
