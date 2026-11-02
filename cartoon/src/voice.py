"""Render narration, one file per beat, following voice/VOICE.md.

Engine: Kokoro-82M ONNX, Young American Female Smooth, Stephen's saved recipe (voice/VOICE.md):
af_heart 0.4 + af_bella 0.3 + af_sky 0.3, speed 1.04, two sentences per take with even 0.14 s gaps,
pitch +5%, softened highs,
American English via the full misaki G2P engine (spaCy POS tagging).
Words missing from misaki's dictionaries get hand phonemes (HAND below);
nothing is ever dropped (an unknown word raises).

Usage: python3 src/voice.py [BEAT_ID ...]
Outputs: build/audio/<ID>.wav (mastered, 44.1 kHz mono), build/audio/timing.json,
         build/audio/phonemes.json (exactly what was sent to the voice).
"""
import os, re, sys, json, subprocess
import numpy as np
import soundfile as sf
import onnxruntime as ort

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from beats import load_beats, ROOT

MODEL = os.environ.get("KOKORO_MODEL", os.path.join(ROOT, "models", "kokoro-v1.0.onnx"))
VOICES = os.environ.get("KOKORO_VOICES", os.path.join(ROOT, "models", "voices-v1.0.bin"))
# Young American Female Smooth: filled in from voice/VOICE.md
BLEND = [("af_heart", 0.4), ("af_bella", 0.3), ("af_sky", 0.3)]
OUT = os.path.join(ROOT, "build", "audio")
SR = 24000
SPEED = 1.04
BEAT_SIL = 0.8

# Hand phonemes (misaki US phoneme set) for words not in misaki's dictionaries.
HAND = {
    "agritourism": "ˈæɡɹɪtˌʊɹɪzəm",
    "Arlene": "ɑɹlˈin",
    "Asahi": "ɑsˈɑhi",
    "Bloomberg": "blˈumbɜɹɡ",
    "Duane": "dwˈAn",
    "Fairbury": "fˈɛɹbˌɛɹi",
    "Kilgus": "kˈɪlɡəs",
    "Shimbun": "ʃˈɪmbʊn",
    "TikTok": "tˈɪktˌɑk",
    "ebook": "ˈibˌʊk",
}


def make_g2p():
    from misaki import en
    used = []

    def fallback(tok):
        w = tok.text
        base, suf = (w[:-2], "z") if w.endswith("'s") else (w, "")
        for k in (base, base.lower(), base.capitalize()):
            if k in HAND:
                used.append(w)
                p = HAND[k]
                if suf and p[-1] in "szʃʒʧʤ":
                    p += "ᵻz"
                elif suf and p[-1] in "ptkfθ":
                    p += "s"
                else:
                    p += suf
                return (p, 5)
        raise KeyError(f"No pronunciation for {w!r}: add it to HAND")

    g2p = en.G2P(trf=False, british=False, fallback=fallback)
    return g2p, used


def split_phrases(text):
    """Return list of (phrase, kind) with kind in comma|end|beat."""
    out = []
    parts = re.split(r"\s*\(beat\)\s*", text)
    for pi, part in enumerate(parts):
        if pi > 0:
            if out:
                out[-1] = (out[-1][0], "beat")
            else:
                out.append(("", "beat"))
        # split after , . ? ! (keep punctuation; also a closing quote after it)
        for m in re.finditer(r"[^,.?!]+[,.?!][\"”]?", part):
            ph = m.group(0).strip()
            if not ph:
                continue
            kind = "comma" if "," in ph[-2:] else "end"
            out.append((ph, kind))
        rest = re.sub(r"[^,.?!]+[,.?!][\"”]?", "", part).strip()
        if rest:
            out.append((rest, "end"))
    return out


def trim(x):
    env = np.convolve(np.abs(x), np.ones(240) / 240, mode="same")
    idx = np.where(env > 0.02 * env.max())[0]
    if len(idx) == 0:
        return x
    pad = int(0.040 * SR)
    a, b = max(0, idx[0] - pad), min(len(x), idx[-1] + pad)
    return x[a:b]


def master(src, dst):
    af = ("bass=g=2:f=180,treble=g=-2:f=7000,"
          "acompressor=threshold=-20dB:ratio=2.5:attack=10:release=120,"
          "loudnorm=I=-16:TP=-1.5:LRA=7")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", af,
                    "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le", dst], check=True)


FILT = ("asetrate=24000*1.05,aresample=24000,atempo=1/1.05,"
        "highshelf=f=7000:g=-3,lowpass=f=11000,"
        "acompressor=threshold=-20dB:ratio=2:attack=10:release=150:makeup=2,"
        "loudnorm=I=-16:TP=-1.5:LRA=11")
TAKE_GAP = 0.14  # even gap between two-sentence takes (recipe)


def master_smooth(src, dst):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", FILT,
                    "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le", dst], check=True)


def takes_of(text):
    """Young American Female Smooth speaks two sentences per take."""
    sents = [x.strip() for x in re.split(r'(?<=[.!?])\s+(?=[A-Z"“])', text.strip()) if x.strip()]
    return [" ".join(sents[i:i + 2]) for i in range(0, len(sents), 2)]


def main(only=None):
    os.makedirs(OUT, exist_ok=True)
    vocab = json.load(open(os.path.join(os.path.dirname(__import__("kokoro_onnx").__file__),
                                        "config.json")))["vocab"]
    voices = np.load(VOICES)
    blend = sum(w * voices[n] for n, w in BLEND)
    sess = ort.InferenceSession(MODEL, providers=["CPUExecutionProvider"])
    in_names = {i.name: i for i in sess.get_inputs()}
    tok_name = "input_ids" if "input_ids" in in_names else "tokens"
    g2p, used = make_g2p()

    def speak(text):
        ps, _ = g2p(text)
        bad = [c for c in ps if c not in vocab]
        if bad:
            raise ValueError(f"unmapped phoneme chars {bad} in {ps!r}")
        tokens = [vocab[c] for c in ps][:510]
        style = blend[min(len(tokens), len(blend)) - 1]
        a = sess.run(None, {tok_name: np.array([[0, *tokens, 0]], dtype=np.int64),
                            "style": style.astype(np.float32),
                            "speed": np.array([SPEED], dtype=np.float32)})[0].squeeze().astype(np.float32)
        return trim(a), ps

    timing_path = os.path.join(OUT, "timing.json")
    timing = json.load(open(timing_path)) if os.path.exists(timing_path) else {}
    phon_path = os.path.join(OUT, "phonemes.json")
    phon = json.load(open(phon_path)) if os.path.exists(phon_path) else {}

    for beat in load_beats():
        if only and beat["id"] not in only:
            continue
        parts = re.split(r"\s*\(beat\)\s*", beat["spoken"])
        chunks = [np.zeros(int(0.25 * SR), np.float32)]
        t = 0.25
        segs, plog = [], []
        first = True
        for pi, part in enumerate(parts):
            if pi > 0:  # a held (beat) silence
                chunks.append(np.zeros(int(BEAT_SIL * SR), np.float32)); t += BEAT_SIL
            if not part.strip():
                continue
            tk = takes_of(part)
            for ti, take in enumerate(tk):
                if ti > 0:
                    chunks.append(np.zeros(int(TAKE_GAP * SR), np.float32)); t += TAKE_GAP
                audio, ps = speak(take)
                plog.append(dict(text=take, phonemes=ps))
                dur = len(audio) / SR
                # phrase timings inside the take: proportional to each phrase rendered on its own
                phr = [p for p, _ in split_phrases(take) if p]
                lens = [len(speak(p)[0]) for p in phr] if len(phr) > 1 else [1]
                tot = sum(lens)
                acc = 0
                for p, L in zip(phr, lens):
                    segs.append(dict(text=p, start=t + dur * acc / tot, end=t + dur * (acc + L) / tot))
                    acc += L
                chunks.append(audio)
                t += dur
        chunks.append(np.zeros(int(0.30 * SR), np.float32))
        x = np.concatenate(chunks)
        x = 0.9 * x / np.abs(x).max()
        raw = os.path.join(OUT, f"{beat['id']}_raw.wav")
        sf.write(raw, x, SR)
        dst = os.path.join(OUT, f"{beat['id']}.wav")
        master_smooth(raw, dst)
        d = sf.info(dst).duration
        timing[beat["id"]] = dict(duration=d, raw_duration=len(x) / SR, phrases=segs)
        phon[beat["id"]] = plog
        print(f"{beat['id']}: {d:6.2f}s  {len(segs)} phrases", flush=True)

    json.dump(timing, open(timing_path, "w"), indent=1, ensure_ascii=False)
    json.dump(phon, open(phon_path, "w"), indent=1, ensure_ascii=False)
    json.dump(sorted(set(used)), open(os.path.join(OUT, "hand_phonemes_used.json"), "w"),
              ensure_ascii=False)
    print("hand phonemes used:", sorted(set(used)))


if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
