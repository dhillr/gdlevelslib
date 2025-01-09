import gdlevelslib as GD

level = GD.GeometryDashLevel("Quintuple Spikes!", "Example Username", "woah", None, revision=0, speed=3)
for i in range(10000):
    for j in range(5):
        level.add_object(GD.GeometryDashObject(8, j*30+555+i*270, 15, 0, None))

GD.add_level(level)