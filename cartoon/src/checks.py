"""Measured checks for the finished video -> output/checks-report.md.
ffprobe facts, loudness and true peak, unmarked silences, and a word-for-word comparison of the script against
what was sent to the voice."""
import os, sys, json, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import timeline
from beats import load_beats, ROOT

OUT = os.path.join(ROOT, "output")
MP4 = os.path.join(OUT, "video-008-nobody-can-find-my-farm-online.mp4")
B = os.path.join(ROOT, "build")


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    L = ["# Checks report: video-008 cartoon", ""]
    pr = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", MP4]).stdout)
    f = pr["format"]
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    a = next(s for s in pr["streams"] if s["codec_type"] == "audio")
    dur = float(f["duration"])
    L += ["## ffprobe", f"- duration: {dur:.2f} s ({int(dur // 60)} min {dur % 60:.1f} s)",
          f"- file size: {int(f['size']) / 1e6:.2f} MB",
          f"- video: {v['codec_name']} {v.get('profile')} {v['width']}x{v['height']} {v['pix_fmt']} {v['r_frame_rate']} fps",
          f"- audio: {a['codec_name']} {a['sample_rate']} Hz {a['channels']} ch, {int(a.get('bit_rate', 0)) // 1000} kb/s"]
    head = open(MP4, "rb").read(200000)
    L.append(f"- faststart (moov before mdat): {head.find(b'moov') != -1 and (head.find(b'mdat') == -1 or head.find(b'moov') < head.find(b'mdat'))}")
    r = run(["ffmpeg", "-hide_banner", "-i", MP4, "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1]
    TP = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1]
    LRA = re.findall(r"LRA:\s+(-?[\d.]+) LU", r)[-1]
    L += ["", "## Loudness and silence (measured with ffmpeg, not heard)", f"- integrated loudness: {I} LUFS (target -14)",
          f"- true peak: {TP} dBTP (target under -1)", f"- loudness range: {LRA} LU"]
    r = run(["ffmpeg", "-hide_banner", "-i", MP4, "-af", "silencedetect=n=-50dB:d=1.5", "-f", "null", "-"]).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    scenes = timeline.build()
    gaps = []
    for s0, s1 in zip(starts, ends + [dur] * (len(starts) - len(ends))):
        S = next((S for S in scenes if S.start <= s0 < S.start + S.dur), scenes[-1])
        gaps.append(f"{s0:.2f}s to {s1:.2f}s ({s1 - s0:.2f}s) in {S.id}")
    L.append(f"- silences over 1.5 s: {len(gaps)}")
    L += [f"  - {g}" for g in gaps]
    # words
    phon = json.load(open(os.path.join(B, "audio", "phonemes.json")))
    norm = lambda s: re.sub(r"[^a-z0-9' ]", " ", s.lower().replace("’", "'")).split()
    mism, words = [], 0
    for b in load_beats():
        want = norm(b["spoken"].replace("(beat)", " "))
        got = norm(" ".join(p["text"] for p in phon[b["id"]]))
        words += len(want)
        if want != got:
            mism.append(b["id"])
    used = json.load(open(os.path.join(B, "audio", "hand_phonemes_used.json")))
    L += ["", "## Spoken script vs what was sent to the voice",
          f"- {len(phon)} beats, {words} words compared, mismatches: {len(mism)} {mism if mism else ''}",
          f"- words given hand phonemes: {', '.join(used)}"]
    open(os.path.join(OUT, "checks-report.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
