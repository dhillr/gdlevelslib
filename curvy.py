import gdlevelslib as GD
import math

level = GD.GeometryDashLevel("Curvy", "Example Username", "very very curvy", '0', None)
for i in range(10000):
    level.add_object(GD.GeometryDashObject(2, i + 105, math.floor(15 * math.sin(i / 30) + 8), 0, None))

for i in range(10000):
    level.add_object(GD.GeometryDashObject(4, i + 105, math.floor(-30 * math.sin(i / 30) + 188), 0, None))

GD.add_level(level)