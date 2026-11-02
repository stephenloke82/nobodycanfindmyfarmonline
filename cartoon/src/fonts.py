"""Fetch OFL Google Fonts (Fredoka, Nunito) and cut static instances into ~/.fonts.
Run once before rendering: python3 src/fonts.py"""
import os, subprocess, urllib.request
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

SRC = {"Fredoka": "https://raw.githubusercontent.com/google/fonts/main/ofl/fredoka/Fredoka%5Bwdth,wght%5D.ttf",
       "Nunito": "https://raw.githubusercontent.com/google/fonts/main/ofl/nunito/Nunito%5Bwght%5D.ttf"}
CUTS = [("Fredoka", 650, "Dot Display"), ("Nunito", 800, "Dot Body"), ("Nunito", 700, "Dot Body Medium")]
dst = os.path.expanduser("~/.fonts"); os.makedirs(dst, exist_ok=True)
cache = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "build", "fonts")
os.makedirs(cache, exist_ok=True)
for fam, url in SRC.items():
    p = os.path.join(cache, fam + "-VF.ttf")
    if not os.path.exists(p):
        urllib.request.urlretrieve(url, p)
for fam, w, name in CUTS:
    f = TTFont(os.path.join(cache, fam + "-VF.ttf"))
    axes = {"wght": w}
    if fam == "Fredoka": axes["wdth"] = 100
    st = instancer.instantiateVariableFont(f, axes)
    for rec in st["name"].names:
        if rec.nameID in (1, 16): rec.string = name
        elif rec.nameID in (2, 17): rec.string = "Regular"
        elif rec.nameID in (4,): rec.string = name
        elif rec.nameID == 6: rec.string = name.replace(" ", "") + "-Regular"
    st.save(os.path.join(dst, name.replace(" ", "") + ".ttf"))
for f in os.listdir(dst):
    if f in ("Nunito.ttf",): os.remove(os.path.join(dst, f))
subprocess.run(["fc-cache", "-f"])
print("fonts ready:", os.listdir(dst))
