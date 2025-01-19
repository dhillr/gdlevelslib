import gdlevelslib as GD
from random import randint

level = GD.GeometryDashLevel("experiment :O", "Example Username", "-_-", None, revision=0, gamemode="ship")
level.song = GD.OfficialSong().getSongByName("Dry Out")
# level.speed = 3
level.mini = True

level.add_object(GD.GeometryDashObject(2925, -45, 315, 0, [["111", "1"]]))

for i in range(10000): 
    o = 0
    match randint(0, 2):
        case 0:
            o = GD.objectID.sawblades.sawblade_big
        case 1:
            o = GD.objectID.sawblades.sawblade_medium
        case 2:
            o = GD.objectID.sawblades.sawblade_small
    level.add_object(GD.GeometryDashObject(o, randint(0, 10000)+285, randint(0, 10000), 0))

GD.add_level(level)
