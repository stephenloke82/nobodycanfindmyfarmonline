# Video 008 cartoon: Nobody Can Find My Farm Online

A fully AI-generated cartoon explainer for the Agritourism Success channel, built from the approved video-008 script.
Every frame is drawn in code (Python + pycairo). The only sound is the narration in Stephen's saved voice,
**Young American Female Smooth** (Kokoro-82M ONNX; recipe in `voice/VOICE.md`). No music, no sound effects.
The host is **Sarah**, a young farm host drawn in the same storybook style as the channel's earlier cartoons.

| Path | What it is |
| --- | --- |
| `script/video-008-script.md` | Every beat: what we see, words on screen, spoken line |
| `voice/VOICE.md`, `voice/Young-American-Female-Smooth.mp3` | Voice recipe and Stephen's reference sample |
| `output/video-008-nobody-can-find-my-farm-online.mp4` | The finished video (1920x1080, 30 fps, H.264 High, AAC 192 kb/s, faststart) |
| `output/video-008.srt` | Captions from the real narration timings |
| `output/thumbnail-a.png`, `output/thumbnail-b.png` | 1280x720 thumbnails |
| `output/contact-sheet.jpg` | One still from every scene |
| `output/voice-comparison.wav` | Stephen's sample, then the rebuilt voice saying the same lines |
| `output/checks-report.md` | Measured checks |
| `src/` | All source code |

## Rebuild

Needs Python 3.11+, ffmpeg and about 2 GB of disk. From this folder:

```bash
pip install pycairo numpy scipy soundfile pyloudnorm onnxruntime kokoro-onnx fonttools pillow spacy regex
pip install --no-deps misaki num2words
python3 -m spacy download en_core_web_sm
mkdir -p models
curl -L -o models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -L -o models/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
python3 src/fonts.py                    # Fredoka + Nunito (OFL) static cuts into ~/.fonts
python3 src/voice.py                    # narration, one mastered file per beat -> build/audio/
python3 src/audio.py                    # narration-only mix at -14 LUFS -> build/mix.wav
python3 src/render.py video --crf 16    # frames -> build/video_noaudio.mp4
python3 src/mux.py                      # final encode into output/
python3 src/captions.py                 # output/video-008.srt
python3 src/thumbs.py                   # thumbnails
python3 src/contact.py                  # contact sheet
python3 src/checks.py                   # output/checks-report.md
```

`python3 src/render.py still K07@5` renders one frame of a scene for a quick look.

## How it is put together

- `beats.py` parses the script; `voice.py` renders the narration per beat following `voice/VOICE.md`
  (misaki G2P, hand phonemes for names such as Kilgus, Fairbury and Shimbun).
- `timeline.py` times every scene from the real narration and builds the mouth envelope Sarah lip-syncs to.
- `sarah.py` draws Sarah; `kit008.py` holds this video's props (phones, maps, ghost pin, listings, the phone gate,
  Jersey cows, the country store); `scenes008.py` has one function per beat.
- The drawing kit (`gfx.py`, `chars.py`, `props.py`, `sets.py`, `icons.py`) is reused from the video-045 build in
  `stephenloke82/agritourismvideos1`.
