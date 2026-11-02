"""output/voice-comparison.wav: Stephen's Young American Female Smooth sample, a short pause, then the same lines
rendered by src/voice.py's recipe (two sentences per take, 0.14 s gaps, pitch +5%, softened highs)."""
import os, sys, json, subprocess
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voice
from beats import ROOT
import onnxruntime as ort

TEXT = ("Welcome to the farm. Today you will walk under tall durian trees, taste fresh fruit, and see how a simple "
        "orchard can grow a second income. So grab a seat, relax, and enjoy your visit.")
vocab = json.load(open(os.path.join(os.path.dirname(__import__("kokoro_onnx").__file__), "config.json")))["vocab"]
voices = np.load(voice.VOICES)
blend = sum(w * voices[n] for n, w in voice.BLEND)
sess = ort.InferenceSession(voice.MODEL, providers=["CPUExecutionProvider"])
g2p, _ = voice.make_g2p()
SR = voice.SR
chunks = [np.zeros(int(0.25 * SR), np.float32)]
for i, take in enumerate(voice.takes_of(TEXT)):
    if i:
        chunks.append(np.zeros(int(voice.TAKE_GAP * SR), np.float32))
    ps, _ = g2p(take)
    toks = [vocab[c] for c in ps]
    a = sess.run(None, {"tokens": np.array([[0, *toks, 0]], dtype=np.int64),
                        "style": blend[min(len(toks), len(blend)) - 1].astype(np.float32),
                        "speed": np.array([voice.SPEED], dtype=np.float32)})[0].squeeze()
    chunks.append(voice.trim(a.astype(np.float32)))
chunks.append(np.zeros(int(0.3 * SR), np.float32))
x = np.concatenate(chunks); x = 0.9 * x / np.abs(x).max()
b = os.path.join(ROOT, "build"); os.makedirs(b, exist_ok=True)
sf.write(os.path.join(b, "rebuilt_raw.wav"), x, SR)
voice.master_smooth(os.path.join(b, "rebuilt_raw.wav"), os.path.join(b, "rebuilt.wav"))
out = os.path.join(ROOT, "output", "voice-comparison.wav")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(ROOT, "voice", "Young-American-Female-Smooth.mp3"),
                "-f", "lavfi", "-t", "1.2", "-i", "anullsrc=r=44100:cl=mono", "-i", os.path.join(b, "rebuilt.wav"),
                "-filter_complex", "[0:a]aresample=44100,aformat=channel_layouts=mono[a];[a][1:a][2:a]concat=n=3:v=0:a=1",
                "-ar", "44100", "-ac", "1", out], check=True)
print(out)
