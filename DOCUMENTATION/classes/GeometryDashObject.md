# GeometryDashObject

**GeometryDashObbject** is a class that stores the data for a Geommetry Dash object.
I know it isn't efficient like this, but I just love OOP too mmuch :P

## Required Arguments
`id:` The object ID. Don't worry, some of these are already covered in `GD.objectID` with names of about 150 objects.
`x:` X position
`y:` Y position
`dir:` Rotation (Note that this is not in radians)

## Optional Arguments
![NOTE]
> Most of these object properties are incorrect as of now (I got them from AI because I couldn't find a good source),
>
> so it's not the best idea to use them right now.
- `flipX:` The object's flipX property. (0 or 1)
- `flipY:` The object's flipY property. (0 or 1)
- `yellowLayer:` The object's yellow layer.
- `baseHSV:` The object's base HSV property.
- `detailHSV:` The object's detail HSV property.
- `copyColorID:` The object's copy color ID property. (0 or 1)
- `zLayer:` The object's Z layer.
- `scale:` The object's scale.
- `groupParent:` The object's group parent property.
- `editorLayer1:` The object's editor layer 1.
- `editorLayer2:` The object's editor layer 2.
- `copyOpacity:` The object's copy opacity property. (0 or 1?)
- `colBlending:` The object's color blending property. (0 or 1?)
- `targetGroup:` The object's target group.
- `extra:` The object's extra property.
- `baseHSVEnabled:` The object's base HSV enabled property. (0 or 1)
- `detailHSVEnabled:` The object's detail HSV enabled property. (0 or 1)
- `editorLayer3:` The object's editor layer 3.
- `base:` The object's base color.
- `detail:` The object's detail color.
- `textValue:` The object's text value.
- `touchTriggered:` The object's touch triggered property. (0 or 1)
- `coinID:` The object's coin ID property.
- `fadeIn:` The object's fade in property. (0 or 1?)
- `groups:` The object's groups.
- `lockPlayerX:` The object's lock player X property. (0 or 1?)

## `other`
This is a list of lists (I know I could use tuples but I'mm lazy and kinda beginner)
```python
myObject = GeometryDashObject(2925, 15, 15, 0, other=[['111', '1']])
```