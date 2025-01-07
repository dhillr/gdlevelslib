import gdlevelslib as GD
import base64

level = GD.GeometryDashLevel("All Object IDs", "Example Username", "all block ids yay", None, revision=0)
for i in range(2000):
    level.add_object(GD.GeometryDashObject(914, i*120+285, 105, 0, None, textValue=base64.b64encode(str(i).encode('utf-8')).decode('utf-8')))
    level.add_object(GD.GeometryDashObject(1+i, i*120+285, 45, 0, None))

GD.add_level(level)