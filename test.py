import gdlevelslib as GD
from gdlevelslib import GeometryDashLevel as gdlevel

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

rd_objX = level.objfind(group=9992)
rd_objY = level.objfind(group=9993)
rd_objZ = level.objfind(group=9994)

sphere_objX = level.objfind(group=9996)
sphere_objY = level.objfind(group=9997)
sphere_objZ = level.objfind(group=9998)
sphere_objR = level.objfind(group=9995)

rd = vec3(rd_objX.getProperty(479, returnZero=True), 
          rd_objY.getProperty(479, returnZero=True), 
          rd_objZ.getProperty(479, returnZero=True))
sphereObj = Sphere(vec3(sphere_objX.getProperty(479, returnZero=True), 
                        sphere_objY.getProperty(479, returnZero=True), 
                        sphere_objZ.getProperty(479, returnZero=True)), 
                    sphere_objR.getProperty(479, returnZero=True))
print(rd.x, rd.y, rd.z, "|", sphereObj.pos.x, sphereObj.pos.y, sphereObj.pos.z, sphereObj.r)

