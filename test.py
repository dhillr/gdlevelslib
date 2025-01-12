import gdlevelslib as GD
from gdlevelslib import GeometryDashLevel as gdlevel
from math import floor

class vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Sphere:
    def __init__(self, pos: vec3, r):
        self.pos = pos
        self.r = r

level = gdlevel("grtx integration test", "Example Username", ":)", None, revision=0, bg_color=GD.Color(0, 0, 0), ground_color=GD.Color(0, 0, 0))
level.add_objects(GD.getLevels().find("ref", caseSensitive=False).getObjects())

# sphere_objX = level.objfind(group=9996)
# sphere_objY = level.objfind(group=9997)
# sphere_objZ = level.objfind(group=9998)
# sphere_objR = level.objfind(group=9995)

def add_pixel(level: gdlevel, x, y, o):
    rd_objX = level.objfind(group=9992)
    rd_objY = level.objfind(group=9993)
    rd_objZ = level.objfind(group=9994)
    rd_objX.setPropertyInLevel(479, floor(x*100), level)
    rd_objY.setPropertyInLevel(479, floor(y*100), level)
    rd_objZ.setPropertyInLevel(479, 100, level)
    level.objfind(group=9992).y += o
    level.objfind(group=9993).y += o
    level.objfind(group=9994).y += o

for j in range(13):
    for i in range(24):
        add_pixel(level, (i-11)/24, (j-11)/13, i+j*48)

GD.add_level(level)

