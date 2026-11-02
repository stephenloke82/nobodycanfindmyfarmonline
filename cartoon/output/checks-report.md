# Checks report: video-008 cartoon

## ffprobe
- duration: 496.43 s (8 min 16.4 s)
- file size: 33.17 MB
- video: h264 High 1920x1080 yuv420p 30/1 fps
- audio: aac 44100 Hz 2 ch, 171 kb/s
- faststart (moov before mdat): True

## Loudness and silence (measured with ffmpeg, not heard)
- integrated loudness: -14.0 LUFS (target -14)
- true peak: -2.6 dBTP (target under -1)
- loudness range: 2.3 LU
- silences over 1.5 s: 1
  - 487.02s to 496.44s (9.42s) in Z12

## Spoken script vs what was sent to the voice
- 75 beats, 1473 words compared, mismatches: 0 
- words given hand phonemes: Arlene, Duane, Fairbury, Kilgus, TikTok, ebook
