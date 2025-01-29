import gdlevelslib as GD
from random import randint

level = GD.GeometryDashLevel("morefun?!?!?", "Example Username", "woah", None, revision=0)

startOffset = 165
spacing = 300
for i in range(10000):
    chunkType = randint(0, 3)

    if chunkType == 0:
        if randint(0, 1) == 0:
            for j in range(randint(1, 2)):
                level.add_object(GD.GeometryDashObject(8, j*30+i*spacing+startOffset, 45, 0))
        
        blocklen = randint(4, 7)
        level.add_object(GD.GeometryDashObject(GD.objectID.blocks.block3_edge3, -30+i*spacing+startOffset, 15, -90))

        for j in range(blocklen):
            level.add_object(GD.GeometryDashObject(GD.objectID.blocks.block3_edgeH, j*30+i*spacing+startOffset, 15, -90))
        
        level.add_object(GD.GeometryDashObject(GD.objectID.blocks.block3_edge3, blocklen*30+i*spacing+startOffset, 15, 90))
    elif chunkType > 0:
        for j in range(randint(1, 3)):
            level.add_object(GD.GeometryDashObject(8, j*30+i*spacing+startOffset, 15, 0))

GD.add_level(level)