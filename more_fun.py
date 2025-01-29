import gdlevelslib as GD
from random import randint

level = GD.GeometryDashLevel("morefun?!?!?", "Example Username", "woah", None, revision=0)

startOffset = 165
spacing = 300
elevation = 15

for i in range(1000):
    chunkType = randint(0, 3)

    if chunkType < 2:
        spacing = 300

    if chunkType == 0:
        if randint(0, 1) == 0:
            for j in range(randint(1, 2)):
                level.add_object(GD.GeometryDashObject(8, j*30+i*spacing+startOffset, elevation+30, 0))
        
        blocklen = randint(4, 7)
        level.add_object(GD.GeometryDashObject(GD.objectID.blocks.block3_edge3, -30+i*spacing+startOffset, elevation, -90))

        for j in range(blocklen):
            level.add_object(GD.GeometryDashObject(GD.objectID.blocks.block3_edgeH, j*30+i*spacing+startOffset, elevation, -90))
        
        level.add_object(GD.GeometryDashObject(GD.objectID.blocks.block3_edge3, blocklen*30+i*spacing+startOffset, elevation, 90))
    elif chunkType == 1:
        for j in range(randint(1, 3)):
            level.add_object(GD.GeometryDashObject(8, j*30+i*spacing+startOffset, elevation, 0))
    elif chunkType > 1:
        level.add_object(GD.GeometryDashObject(GD.objectID.portals.ship_portal, -30+i*spacing+startOffset, elevation+60, 0))

        blocklen = randint(3, 10)
        height = randint(4, 8) * 30
        

        for j in range(blocklen):
            level.add_object(GD.GeometryDashObject(6 if j == 0 or j == blocklen-1 else 7, j*30+i*spacing+startOffset, elevation-30, -90 if j < blocklen-1 else 90))
            level.add_object(GD.GeometryDashObject(8, j*30+i*spacing+startOffset, elevation, 0))
            level.add_object(GD.GeometryDashObject(6 if j == 0 or j == blocklen-1 else 7, j*30+i*spacing+startOffset, elevation+height, -90 if j < blocklen-1 else 90))
            level.add_object(GD.GeometryDashObject(8, j*30+i*spacing+startOffset, elevation+height-30, 180))

        level.add_object(GD.GeometryDashObject(GD.objectID.portals.cube_portal, blocklen*30+i*spacing+startOffset, elevation+60, 0))
        spacing += blocklen*60

    if randint(0, 2) == 0:
        if randint(0, 1) == 0:
            elevation += 30
        else:
            if elevation > 15:
                elevation -= 30

GD.add_level(level)