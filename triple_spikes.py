import gdlevelslib as GD

level = GD.GeometryDashLevel("Triple Spikes", "poyo52596kirby", "triple_spikes", '0', None)
for i in range(10000):
    for j in range(3):
        level.add_object(GD.GeometryDashObject(8, j*30+135+i*270, 15, 0, None))

GD.add_level(level)