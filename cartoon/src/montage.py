"""Tile images into a grid: python3 src/montage.py out.jpg cols width img..."""
import sys
from PIL import Image
out, cols, w = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
ims = [Image.open(p).convert("RGB") for p in sys.argv[4:]]
h = int(w * 9 / 16)
rows = (len(ims) + cols - 1) // cols
M = Image.new("RGB", (cols * w + (cols + 1) * 6, rows * h + (rows + 1) * 6), (255, 248, 232))
for i, im in enumerate(ims):
    M.paste(im.resize((w, h), Image.LANCZOS), (6 + (i % cols) * (w + 6), 6 + (i // cols) * (h + 6)))
M.save(out, quality=88)
