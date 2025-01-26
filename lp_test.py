import gdlevelslib as GD
from pathlib import Path
from math import sin

level = GD.GeometryDashLevel("lptest", "Example Username", "???", None, revision=0)
for i in range(1000):
    level.add_object(GD.GeometryDashObject(1, i+15, sin(i*0.02)*30+15, 0))

GD.preview_level(level, Path("."))