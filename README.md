# GDLevelsLib

A library for editing Geometry Dash levels.

You can't edit existing levels yet, but you can create them.

## Example usage:
```python
import gdlevelslib as GD

# Create a new level
myLevel = GD.GeometryDashLevel("Example", "Example Username", "example", '0', None)

# Add 1024 objects to the level
for i in range(1024):
    myLevel.add_object(GD.GeometryDashObject(1+i, i*30+15, 15, 0, None))

# Add our level to Geometry Dash
GD.add_level(myLevel)
```

> [!CAUTION]
> **GDLevelsLib** is still in beta, so this may change!
>
> I will make sure to update the example project.

### Coming soon!
> [!NOTE]
> I have already finished the code for **GDLevelsLib** and I will release it to GitHub soon.
