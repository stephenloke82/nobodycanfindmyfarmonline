"""Build output/video-008.srt from the real phrase timings. Words are the spoken script exactly."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import timeline
from beats import ROOT

MAXC = 84  # two lines of ~42


def ts(x):
    ms = int(round(x * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def two_lines(s):
    if len(s) <= 42:
        return s
    words = s.split()
    best, bi = 1e9, 1
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        d = max(len(a), len(b))
        if d < best:
            best, bi = d, i
    return " ".join(words[:bi]) + "\n" + " ".join(words[bi:])


def chunks(text, start, end):
    words = text.split()
    out, cur = [], []
    for w in words:
        if cur and len(" ".join(cur + [w])) > MAXC:
            out.append(" ".join(cur)); cur = [w]
        else:
            cur.append(w)
    out.append(" ".join(cur))
    total = sum(len(o) for o in out)
    res, t = [], start
    for o in out:
        d = (end - start) * len(o) / total
        res.append((t, t + d, o)); t += d
    return res


def build():
    scenes = timeline.build()
    cues = []
    for S in scenes:
        for st, en, txt in zip(S.ph, S.ph_end, S.ph_text):
            for a, b, o in chunks(txt, S.start + st, S.start + en):
                cues.append([a, b, o])
    # merge very short adjacent cues within a beat (< 1.0 s) for readability, keep words exact
    merged = []
    for c in cues:
        if merged and (c[1] - c[0] < 1.0 or merged[-1][1] - merged[-1][0] < 1.0) and \
                len(merged[-1][2] + " " + c[2]) <= MAXC and c[0] - merged[-1][1] < 0.5:
            merged[-1][1] = c[1]; merged[-1][2] += " " + c[2]
        else:
            merged.append(c)
    # small display padding without overlapping the next cue
    for i, c in enumerate(merged):
        nxt = merged[i + 1][0] if i + 1 < len(merged) else c[1] + 1
        c[1] = min(c[1] + 0.25, nxt - 0.02)
    out = os.path.join(ROOT, "output", "video-008.srt")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        for i, (a, b, o) in enumerate(merged, 1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{two_lines(o)}\n\n")
    print(out, len(merged), "cues")


if __name__ == "__main__":
    build()
