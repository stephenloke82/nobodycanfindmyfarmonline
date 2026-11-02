# Checks report: video-008 cartoon

## ffprobe
- duration: 474.63 s (7 min 54.6 s)
- file size: 32.03 MB
- video: h264 High 1920x1080 yuv420p 30/1 fps
- audio: aac 44100 Hz 2 ch, 170 kb/s
- faststart (moov before mdat): True

## Loudness and silence (measured with ffmpeg, not heard)
- integrated loudness: -14.0 LUFS (target -14)
- true peak: -2.7 dBTP (target under -1)
- loudness range: 2.4 LU
- silences over 1.5 s: 1
  - 465.22s to 474.64s (9.42s) in Z12

## Spoken script vs what was sent to the voice
- 74 beats, 1417 words compared, mismatches: 0 
- words given hand phonemes: Arlene, Duane, Fairbury, Kilgus, TikTok, ebook
