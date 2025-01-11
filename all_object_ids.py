import gdlevelslib as GD
from math import floor

level = GD.GeometryDashLevel("All Object IDs", "Example Username", "all block ids yay", None, revision=0)
for i in range(3000):
    level.add_object(GD.GeometryDashObject(914, floor(i / 10) * 120 + 285, 105 + (150 * (i % 10)), 0, None, textValue=1+i))
    level.add_object(GD.GeometryDashObject(1+i, floor(i /10) * 120 + 285, 45 + (150 * (i % 10)), 0, None))

GD.add_level(level)