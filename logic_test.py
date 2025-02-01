from gdlevelslib import logic, GeometryDashLevel, GeometryDashObject, add_level, OfficialSong

level: GeometryDashLevel = GeometryDashLevel("logicTest :O", "Example Username", "!!!", None, revision=0, song=OfficialSong().getSongByName("Jumper"))
myObject: GeometryDashObject = GeometryDashObject(1, 75, 15, 0)

CTX: logic.context = logic.context.newContext(level)

class TestLogic(logic):
    """
    # eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee! :D :D :) >:) >:} :3 :/ :P :O /:
    """
    def __init__(self):
        super().__init__()

    def preload(self):
        self.ctx: logic.context = CTX
        self.endFrame: int = 100

    def onStart(self):
        ctx: logic.context = self.ctx
        ctx.level.add_object(myObject)
        # print(ctx.level.objects)

    def onUpdate(self):
        ctx: logic.context = self.ctx
        ctx.positionObject(myObject, 1000, 0)

    def onEnd(self):
        add_level(self.ctx.level)

TestLogic()