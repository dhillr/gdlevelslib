import gdlevelslib as GD
from gdlevelslib import blocks
from math import floor, sin
from random import randint

auto = False # if you want to make the level auto >:)

level = GD.GeometryDashLevel("Fun", "Example Username", ":D", None, revision=0, gamemode="ball", speed=2, song=GD.OfficialSong().getSongByID(randint(0, 21)))
level.add_object(GD.GeometryDashObject(2925, -45, 315, 0, [["111", "1"]])) # creates camera mode trigger that has free mdode property :D
for i in range(10000):
    level.add_object(GD.GeometryDashObject(8, i*30+285, 15, 0))
print("Part 1 of 4 completed.")

def wavy(x): return floor(sin(0.5*x)*30)+2*x # for cleanliness

for i in range(5000):
    for j in range(5):
        id = GD.objectID.blocks.block3_edge3 if j == 0 or j == 4 else GD.objectID.blocks.block3_edgeH
        d = -90 if j == 0 else 90
        level.add_object(GD.GeometryDashObject(id, j*30+i*270+285, 225+wavy(i), d, groups=[str(i+1)]))
        # pulse trigger
        # level.add_object(GD.GeometryDashObject(1006, j*30+i*270+285, 230+wavy(i), 0, other=[['51', str(i+1)], ['47', '0.5'], ['52', '1'], ['210', '1']]))
    if auto: level.add_object(GD.GeometryDashObject(67, 120+i*270+285, 200+wavy(i), 180))
print("Part 2 of 4 completed.")

for i in range(5000):
    for j in range(5):
        id = GD.objectID.blocks.block3_edge3 if j == 0 or j == 4 else GD.objectID.blocks.block3_edgeH
        d = -90 if j == 0 else 90
        level.add_object(GD.GeometryDashObject(id, j*30+i*270+345, 105+wavy(i), d, groups=[str(i+5001)]))
        # pulse trigger
        # level.add_object(GD.GeometryDashObject(1006, j*30+i*270+345, 134+wavy(i), 0, other=[['51', str(i+5001)], ['47', '0.5'], ['52', '1'], ['210', '1']]))
    level.add_object(GD.GeometryDashObject(103, i*270+345, 129+wavy(i), 0, groups=[str(i+5001)]))
    level.add_object(GD.GeometryDashObject(103, i*270+375, 129+wavy(i), 0, groups=[str(i+5001)]))
    if auto: level.add_object(GD.GeometryDashObject(67, 135+1.2*wavy(i)+2*i+i*270+345, 129+wavy(i), 0))
print("Part 3 of 4 completed.")

for i in range(500):
    level.add_object(GD.GeometryDashObject(29, i*blocks(100)+blocks(50), 615, 0, yellowLayer=randint(0, 255), baseHSV=randint(0, 255), detailHSV=randint(0, 255), 
                    other=[['10', '1']]))
print("Part 4 of 4 completed.")

GD.add_level(level)