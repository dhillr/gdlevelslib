""" 
    == Example Script ==

    This is an example of how to use GDLevelsLib to create a new level and add an object to it.

    This will create a level  with 1'024 objects with different IDs and add it to Geometry Dash.
    --------------------------------------------------------
        [!] GDLevelsLib is still in development, so this example may not work as expected or the level may appear bugged.
        [!] If you encounter any issues, please report them in the issues section of the repository.
    --------------------------------------------------------
        GDLevelsLib is open source and is available on GitHub. https://github.com/dhillr/gdlevelslib

"""

import gdlevelslib as GD

# Create a new level
myLevel = GD.GeometryDashLevel("Example", "Example Username", "example", None, revision=0)

# Add 1'024 objects to the level
for i in range(1024):
    myLevel.add_object(GD.GeometryDashObject(1+i, i*30+15, 15, 0, None).snap_to_grid())

# Add our level to Geometry Dash
GD.add_level(myLevel)