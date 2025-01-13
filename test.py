import gdlevelslib as GD
from gdlevelslib import GeometryDashLevel as gdlevel
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
level.add_objects(GD.getLevels().find("ref", caseSensitive=False).getObjects())

_SCREEN_WIDTH = 48
_SCREEN_HEIGHT = 27

# sphere_objX = level.objfind(group=9996)
# sphere_objY = level.objfind(group=9997)
# sphere_objZ = level.objfind(group=9998)
# sphere_objR = level.objfind(group=9995)
rd_objX = level.objfind(group=9992)
rd_objY = level.objfind(group=9993)
rd_objZ = level.objfind(group=9994)
def add_pixel(level: gdlevel, x, y, o):
    level.add_objects(GD.getLevels().find("ref", caseSensitive=False).getObjects())
    if (o > 0):
        rd_objX = level.objfind(69420+o)
        rd_objY = level.objfind(69420+o)
        rd_objZ = level.objfind(69420+o)
    rd_objX.groups = [str(69420+o)]
    rd_objY.groups = [str(69420+o)]
    rd_objZ.groups = [str(69420+o)]
    rd_objX.setPropertyInLevel(479, floor(x*100), level)
    rd_objY.setPropertyInLevel(479, floor(y*100), level)
    rd_objZ.setPropertyInLevel(479, 100, level)

for j in range(_SCREEN_HEIGHT):
    for i in range(_SCREEN_WIDTH):
        add_pixel(level, i/(0.5*_SCREEN_WIDTH), j/(0.5*_SCREEN_HEIGHT), i+j*_SCREEN_WIDTH)
        bar = "@"*int(50*(i+j*_SCREEN_WIDTH)/(_SCREEN_WIDTH*_SCREEN_HEIGHT))+ ":"*(50-int(50*(i+j*_SCREEN_WIDTH)/(_SCREEN_WIDTH*_SCREEN_HEIGHT)))
        print(f"Added pixel {i+j*_SCREEN_WIDTH} of {_SCREEN_WIDTH*_SCREEN_HEIGHT} {bar} {100*((i+j*_SCREEN_WIDTH)/(_SCREEN_WIDTH*_SCREEN_HEIGHT)):.2f}%", end="\n"*7)

GD.add_level(level)

