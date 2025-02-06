from gdlevelslib import *

# set_level(
#     getLevels().find("worth it", caseSensitive=False),
#     GeometryDashLevel("??!?", "Example Username", "???", None, revision=0, gamemode="cube", speed=1, song=OfficialSong().getSongByName("Dry Out"))
# )
# print(gz.decompress(base64.urlsafe_b64decode(getLevels().find("ref5", caseSensitive=False).data.removesuffix("=").join("=="))).decode('utf-8'))
level = GeometryDashLevel("2.2 is awesome", "Example Username", "it is very awesome", None, revision=0, song=OfficialSong().getSongByName("Polargeist"))
level.color_channels = [Color(255, 0, 0), Color(0, 255, 0), Color(0, 0, 255)]
level.speed = 4
level.bg_color = Color(0, 0, 0)
level.ground_color = Color(255, 255, 255)

# add_level(level)
print(base64.b64encode("scavenger hunt".encode('utf-8')).decode('utf-8'))