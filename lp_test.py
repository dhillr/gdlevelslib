import gdlevelslib as GD
from pathlib import Path
from math import sin

level = GD.GeometryDashLevel("lptest", "Example Username", "???", None, revision=0)
def w(x): return (sin(x*0.02)*30)+(sin(x*0.08)*15)+(sin(x*0.16)*7)+15
for i in range(1000):
    level.add_object(GD.GeometryDashObject(1, i+165, w(i), 0))

GD.preview_level(level, Path(__file__)/"lp_test.py")
# GD.add_level(level) # ooooooooo