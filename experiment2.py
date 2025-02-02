import gdlevelslib as GD

level = GD.GeometryDashLevel("-------------------- experiment2 --------------------", "Example Username", "wowowowowowowo", None, revision=0)
level.song = GD.OfficialSong().getSongByName("Base After Base")
level.speed = 2
level.mini = True
sp = 165
p = 0

for n in range(2):
    for k in range(100):
        for i in range(8):
            for j in range(3):
                level.add_object(GD.GeometryDashObject(39, j*30+i*150+sp, 7, 0))

        sp += 165*8
        level.add_object(GD.GeometryDashObject(GD.objectID.portals.ship_portal, j*30+i*150+sp-165*8, 30, 0))
        for i in range(16):
            for j in range(3):
                level.add_object(GD.GeometryDashObject(8, j*30+i*150+sp, 15, 0))
                level.add_object(GD.GeometryDashObject(8, j*30+i*150+sp, 75, 180))

                for l in range(3):
                    for m in range(3):
                        level.add_object(GD.GeometryDashObject(1, j*30+i*150+sp+l*30, 105+m*30, 0))
        level.add_object(GD.GeometryDashObject(GD.objectID.portals.cube_portal, j*30+i*150+sp, 30, 0))
        sp += 165*16
    p += 1
    print(p)

GD.add_level(level)