# GeometryDashLevel
**GeometryDashLevel** is a class for storing a Geometry Dash level.

## Required Arguments
- `title:` The title of the level.
- `author:` The author of the level.
- `description:` The level description (this is actually not applied to the level as of now)
- `data:` This is usually set to None unless it's auto-generated using ```python gdlevelslib.getLevels().find("<your level name>")```

## Optional Arguments
- `revision:` The level revision.
- `speed:` The speed that the level starts with.
- `gamemode:` The level's gamemode.
- `color_channels:` The level's color channels.
- `song_offset:` The level's song offset.
- `song_fadeIn:` The level's song fade in property.
- `song_fadeOut:` The level's song fade out property.
- `guidelines:` The level's guidelines.
- `bg_texture:` The level's background texture.
- `ground_texture:` The level's ground texture.
- `line:` The level's line.
- `font:` The level's font.
- `mini:` The level's mini property.
- `dual:` The level's dual property.
- `twoPlayerMode:` The level's two player mode property.
- `upsideDown:` The level's upside down property.
- `song:` The level's song.
- `bg_color:` The level's background color.
- `ground_color:` The level's ground color.
- `verified:` The level's verified property. (Not recommended if you want your level to be rated ;P)