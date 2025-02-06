import gdlevelslib as GD
from gdlevelslib import GeometryDashLevel as gdlevel, GeometryDashObject as gdobject
from math import floor
import os

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
ref: gdlevel = gdlevel("refrefref", "Example Username", "refrefref", None, revision=0)
ref.add_objects(GD.getLevels().find("ref", caseSensitive=False).getObjects())

_SCREEN_WIDTH = 24
_SCREEN_HEIGHT = 13

# sphere_objX = level.objfind(group=9996)
# sphere_objY = level.objfind(group=9997)
# sphere_objZ = level.objfind(group=9998)
# sphere_objR = level.objfind(group=9995)
rd_objX = ref.objfind(group=9992)
rd_objY = ref.objfind(group=9993)
rd_objZ = ref.objfind(group=9994)
ref.remove_object(rd_objX)
ref.remove_object(rd_objY)
ref.remove_object(rd_objZ)

def add_pixel(level: gdlevel, x, y, o):
    level.add_objects(GD.decode_level_string(ref.objects))

    rd_objX.clear_groups()
    rd_objY.clear_groups()
    rd_objZ.clear_groups()
    rd_objX.add_group(8888+o)
    rd_objY.add_group(8889+o)
    rd_objZ.add_group(8890+o)
    # if str(9422+o) in rd_objZ.groups:
    #     print("yes")
    #     print(rd_objZ.groups)
    # else:
    #     print("no")
    rd_objX.setProperty(479, floor(x*100))
    rd_objY.setProperty(479, floor(y*100))
    rd_objZ.setProperty(479, 100)
    rd_objX.y -= 1
    rd_objY.y -= 1
    rd_objZ.y -= 1
    level.add_objects([rd_objX, rd_objY, rd_objZ])

for j in range(_SCREEN_HEIGHT):
    for i in range(_SCREEN_WIDTH):
        add_pixel(level, i/(0.5*_SCREEN_WIDTH), j/(0.5*_SCREEN_HEIGHT), i+j*_SCREEN_WIDTH)
        bar = "@"*int(50*(i+j*_SCREEN_WIDTH+1)/(_SCREEN_WIDTH*_SCREEN_HEIGHT))+ ":"*(50-int(50*(i+j*_SCREEN_WIDTH+1)/(_SCREEN_WIDTH*_SCREEN_HEIGHT)))
        print(f"Added pixel {i+j*_SCREEN_WIDTH+1} of {_SCREEN_WIDTH*_SCREEN_HEIGHT} {bar} {100*((i+j*_SCREEN_WIDTH+1)/(_SCREEN_WIDTH*_SCREEN_HEIGHT)):.2f}%", end="\n"*7)

GD.add_level(level)

