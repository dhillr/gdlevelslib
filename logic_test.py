import gdlevelslib as GD
from gdlevelslib import logic, GeometryDashLevel, GeometryDashObject

level = GeometryDashLevel("logicTest :O", "Example Username", "!!!", None, revision=0)
level.add_object(GD.GeometryDashObject(1, 0, 0, 0))

class TestLogic(logic):
    def __init__(self, level):
        super().__init__(level)
        self.count = 0

    def onUpdate(self):
        self.count += 1
        if self.count == 100:
            self.level.add_object(GD.GeometryDashObject(2, 0, 0, 0))