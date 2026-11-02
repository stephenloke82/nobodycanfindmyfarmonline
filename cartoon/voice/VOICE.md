# Young American Female Smooth: voice recipe (rebuilt 2 Nov 2026)

Stephen's saved AI voice, used for Sarah's narration in video 008. `Young-American-Female-Smooth.mp3` in this folder
is Stephen's reference sample. Its original settings were not saved anywhere this session could reach (Google Drive,
Descript, GitHub), so the recipe below was **rebuilt from the sample**. It is the closest match found, not a
confirmed copy of the original. If the original settings turn up, put them here and re-run `src/voice.py`.

## Rebuilt settings

- Engine: Kokoro-82M (royalty-free), ONNX version, the same model files as Midwest Female Warm
- Voice blend: `af_heart` 0.55 + `af_bella` 0.20 + `af_sky` 0.20 + `af_sarah` 0.05 (weighted sum of the style arrays)
- Speed: 1.11
- Language: American English (misaki G2P, full engine with spaCy)
- Phrase rendering, pauses (seed 7), trimming, lead-in/tail and mastering: identical to Midwest Female Warm
  (`agritourismvideos1/voice/VOICE.md`): bass +2 dB at 180 Hz, treble −2 dB at 7 kHz, gentle compression,
  loudnorm −16 LUFS, 192 kbps mono MP3 for samples

## How it was rebuilt (measured, not heard)

1. The sample and Midwest Female Warm's sample share the same encoder, a 12 kHz band limit (Kokoro's 24 kHz output)
   and the same −16 LUFS mastering, and they say the same sentences (checked by aligning the two recordings).
   Text, transcribed with PocketSphinx: "Welcome to the farm. Today you will walk under tall durian trees, taste fresh
   fruit, and see how a simple orchard can grow a second income. So grab a seat, relax, and enjoy your visit."
2. Candidate recipes were rendered on that text and compared with the sample by time-aligned MFCC distance.
   The method was first run blind on Midwest Female Warm and found its saved recipe (`af_heart` 0.6 + `af_sarah` 0.4)
   as the best match.
3. Search: every single American female voice, two-voice blends with `af_heart`, then a step-by-step weight and speed
   search over ten voices. British voices, extra EQ and unnormalised weights were tried and were worse.

| Rebuild compared with its own sample (same pipeline) | Distance (lower is closer) |
| --- | --- |
| Midwest Female Warm, saved recipe | 11.9 |
| Young American Female Smooth, rebuilt recipe above | 34.7 |
| Best single voice (`af_heart`) | about 38 |

The gap means the rebuild is close in pace and pitch (11.7 s against the sample's 11.6 s) but not identical in tone.
Listen to `output/voice-comparison.wav`: Stephen's sample first, then the rebuild saying the same lines.

## Pronunciation

Words missing from misaki's dictionaries get hand phonemes in `src/voice.py` (`HAND`): Arlene, Asahi, Bloomberg,
Duane, Fairbury, Kilgus, Shimbun, TikTok, ebook. Nothing is dropped; an unknown word stops the build.
