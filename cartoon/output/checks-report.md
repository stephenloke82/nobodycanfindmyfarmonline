# Checks report: video-008 cartoon

## ffprobe
- duration: 511.27 s (8 min 31.3 s)
- file size: 33.46 MB
- video: h264 High 1920x1080 yuv420p 30/1 fps
- audio: aac 44100 Hz 2 ch, 157 kb/s
- faststart (moov before mdat): True

## Loudness and silence (measured with ffmpeg, not heard)
- integrated loudness: -14.0 LUFS (target -14)
- true peak: -2.7 dBTP (target under -1)
- loudness range: 2.0 LU
- silences over 1.5 s: 3
  - 61.68s to 63.19s (1.51s) in H11
  - 382.01s to 383.52s (1.52s) in C08
  - 502.28s to 511.28s (9.00s) in Z12

## Spoken script vs what was sent to the voice
- 75 beats, 1472 words compared, mismatches: 0 
- words given hand phonemes: Arlene, Asahi, Bloomberg, Duane, Fairbury, Kilgus, Shimbun, TikTok, ebook
