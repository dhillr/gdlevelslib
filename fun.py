import gdlevelslib as GD
from gdlevelslib import blocks
from math import floor, sin
from random import randint

auto = False # if you want to make the level auto >:)
mirror_portals = False

custom_song = randint(0, 3) == 0 # 1 in 4 chance to use a custom song.
level = GD.GeometryDashLevel("Fun", "Example Username", ":D", None, revision=0, gamemode="ball", speed=2, 
                            song=(GD.OfficialSong().getSongByID(randint(0, 21)) if not custom_song else GD.CustomSong().getSongByID(randint(1, 1000000)))
        )
level.add_object(GD.GeometryDashObject(2925, -45, 315, 0, [["111", "1"]])) # creates camera mode trigger that has free mdode property :D
parts = 5 - (0 if mirror_portals else 1)
o = 0
for i in range(10000):
    level.add_object(GD.GeometryDashObject(8, i*30+285, 15, 0))

print(f"Part 1 of {parts} completed.")

def wavy(x): return floor(sin(0.5*x)*30)+2*x # for cleanliness

o = 0
for i in range(5000):
    for j in range(5):
        id = GD.objectID.blocks.block3_edge3 if j == 0 or j == 4 else GD.objectID.blocks.block3_edgeH
        d = -90 if j == 0 else 90
        level.add_object(GD.GeometryDashObject(id, j*30+i*270+285, 225+wavy(i), d, groups=[str(i+1)]))
        # pulse trigger
        # level.add_object(GD.GeometryDashObject(1006, j*30+i*270+285, 230+wavy(i), 0, other=[['51', str(i+1)], ['47', '0.5'], ['52', '1'], ['210', '1']]))
        # o += 1

        # bar
        bar = "@"*int(50*(o/25000))+ ":"*(50-int(50*(o/25000)))
        print(f"Part 2 of {parts} {bar} {100*(o/25000):.2f}%")
        if custom_song: 
            print("This level is using a custom song, so if you hear nothing, go to the level editor to download it!", end="\r"*6) 
        else:
            print("\n"*7)
        o += 1
    if auto: level.add_object(GD.GeometryDashObject(67, 120+i*270+285, 200+wavy(i), 180))

o = 0
for i in range(5000):
    for j in range(5):
        id = GD.objectID.blocks.block3_edge3 if j == 0 or j == 4 else GD.objectID.blocks.block3_edgeH
        d = -90 if j == 0 else 90
        level.add_object(GD.GeometryDashObject(id, j*30+i*270+345, 105+wavy(i), d, groups=[str(i+5001)]))
        # pulse trigger
        # level.add_object(GD.GeometryDashObject(1006, j*30+i*270+345, 134+wavy(i), 0, other=[['51', str(i+5001)], ['47', '0.5'], ['52', '1'], ['210', '1']]))
        # o += 1

        # bar
        bar = "@"*int(50*(o/35000))+ ":"*(50-int(50*(o/35000)))
        print(f"Part 3 of {parts} {bar} {100*(o/35000):.2f}%")
        if custom_song: 
            print("This level is using a custom song, so if you hear nothing, go to the level editor to download it!", end="\r"*6) 
        else:
            print("\n"*7)
        o += 1
    level.add_object(GD.GeometryDashObject(103, i*270+345, 129+wavy(i), 0, groups=[str(i+5001)]))
    level.add_object(GD.GeometryDashObject(103, i*270+375, 129+wavy(i), 0, groups=[str(i+5001)]))
    o += 2
    if auto: level.add_object(GD.GeometryDashObject(67, 135+1.2*wavy(i)+2*i+i*270+345, 129+wavy(i), 0))

o = 0
for i in range(500):
    level.add_object(GD.GeometryDashObject(29, i*blocks(100)+blocks(50), 615, 0, yellowLayer=randint(0, 255), baseHSV=randint(0, 255), detailHSV=randint(0, 255), 
                    other=[['10', '1']]))
    
    # bar
    bar = "@"*int(50*(o/500))+ ":"*(50-int(50*(o/500)))
    print(f"Part 4 of {parts} {bar} {100*(o/500):.2f}%")
    if custom_song: 
        print("This level is using a custom song, so if you hear nothing, go to the level editor to download it!", end="\r"*6) 
    else:
        print("\n"*7)
    o += 1

if mirror_portals:
    o = 0
    for i in range(100):
        level.add_object(GD.GeometryDashObject(45 + i % 2, i*blocks(200)+blocks(200)+15, 195+wavy(i), 0))
        
        # bar
        bar = "@"*int(50*(o/100))+ ":"*(50-int(50*(o/100)))
        print(f"Part 5 of {parts} {bar} {100*o:.2f}%")
        if custom_song: 
            print("This level is using a custom song, so if you hear nothing, go to the level editor to download it!", end="\r"*6) 
        else:
            print("\n"*7)
        o += 1

GD.add_level(level)