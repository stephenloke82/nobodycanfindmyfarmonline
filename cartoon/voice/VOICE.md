# Young American Female Smooth: voice recipe

Stephen's saved AI voice (from his stephen-voiceover skill). `Young-American-Female-Smooth.mp3` in this folder is his
reference sample. Used for Sarah's narration in video 008.

## Settings

- Engine: Kokoro-82M (royalty-free), ONNX version (`models/kokoro-v1.0.onnx`, `models/voices-v1.0.bin`, not committed)
- Voice blend: `af_heart` 0.4 + `af_bella` 0.3 + `af_sky` 0.3 (weighted sum of the style arrays)
- Speed: 1.04
- Language: American English
- Takes: two sentences per take, even 0.14 s gaps between takes. Style row `voice[min(len(tokens), 510) - 1]`,
  input `[[0, *tokens, 0]]`. Trim each take at 2% of the 240-sample envelope peak with 40 ms padding.
- Lead-in 0.25 s, tail 0.30 s, peak-normalise to 0.9. A held `(beat)` in a script is 0.8 s of silence.
- Mastering (ffmpeg), pitch +5% with the length kept, softened highs:

```
-af asetrate=24000*1.05,aresample=24000,atempo=1/1.05,highshelf=f=7000:g=-3,lowpass=f=11000,acompressor=threshold=-20dB:ratio=2:attack=10:release=150:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=11
-ar 44100 -ac 1 (192 kbps MP3 for samples)
```

## Check

Rendering the sample's own lines with this recipe and comparing against the sample (time-aligned MFCC distance):
13.8, in line with Midwest Female Warm against its own sample (11.9). The comparison clip is
`output/voice-comparison.wav`: the sample first, then the recipe.

## Rules for an AI narrator (from Stephen's voiceover rules)

- Speak as a third party working for Stephen, never as Stephen.
- Never say his farm is "featured in" Bloomberg News or Asahi Shimbun.
- Say Stephen "created" his ebooks and guides, never "wrote".
- Never state the video's length; say "In this video, we will...".
- Spell every number and year out as words.
