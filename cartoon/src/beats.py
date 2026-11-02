"""Parse script/video-008-script.md into beats."""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "script", "video-008-script.md")


def load_beats(path=SCRIPT):
    beats, section = [], None
    lines = open(path, encoding="utf-8").read().splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^# Section (\d+): (.+)$", ln)
        if m:
            section = m.group(2).strip()
        m = re.match(r"^## (\w+) \| (.+?) \| (.+)$", ln)
        if m:
            bid, see, screen = m.group(1), m.group(2).strip(), m.group(3).strip()
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            spoken = lines[j].strip()
            beats.append(dict(id=bid, section=section, see=see,
                              screen=[s.strip() for s in screen.split(" / ")],
                              spoken=spoken))
            i = j
        i += 1
    return beats


if __name__ == "__main__":
    b = load_beats()
    print(len(b), "beats")
    words = sum(len(x["spoken"].replace("(beat)", "").split()) for x in b)
    print(words, "words")
    print(json.dumps(b[:2], indent=1))
