"""
### GDLevelsLib
A Python library for Geometry Dash levels.

- #### Make and modify levels with code.
- #### Fun way to teach Geometry Dash players how to code :)
- #### Replaces the need to manually copy paste in levels.
- #### Easy to use and understand.
- #### Open source and available on GitHub. (https://github.com/dhillr/gdlevelslib)
- #### Over 1,000 lines of code and counting.

### Example Program:
```python
import gdlevelslib as GD

# Create a new level
myLevel = GD.GeometryDashLevel("Example", "Example Username", "example", None, revision=0)

# Add 1'024 objects to the level
for i in range(1024):
    myLevel.add_object(GD.GeometryDashObject(1+i, i*30+15, 15, 0, None).snap_to_grid())

# Add our level to Geometry Dash
GD.add_level(myLevel)
```

## Todo:
- Add description support.
"""
import gzip as gz
import base64
import xml.etree.ElementTree as ET
import os
import sys
import math
import json
import webbrowser
import requests
from typing import Optional
from xml.dom import minidom
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import *
from __init__ import __version__

print("##########")
print("## #### ##  GDLevelsLib [BETA]")
print("##########  by poyo52596kirby")
print("#        #  Version " + __version__)
print("##########\n")

if sys.platform == "darwin":
    print("GDLevelsLib is not supported on macOS.")
    raise SystemExit


class LevelSaver:
    def __init__(self, lvl=None):
        self.level = lvl

    def __xor__(self, bd):
        return bytes(b ^ 17 for b in bd)

    def save(self, path: str=None, name: str=None) -> None:
        """
        Save a level to a file.
        """
        n = name.removesuffix(".gdl")+".gdl" if name else "level.gdl"
        p = path/n if path else Path(".")/"level.gdl"
        with open(p, "w") as f:
            f.write(self.__xor__(self.level.genstr().encode('utf-8')).decode('utf-8'))

    @classmethod
    def save_level(self, lvl, path: str=None, name: str=None) -> None:
        """
        Save a level to a file.
        """
        n = name.removesuffix(".gdl")+".gdl" if name else "level.gdl"
        p = path/n if path else Path(".")/"level.gdl"
        head = f"{lvl.title},{lvl.author},{lvl.description},"
        head += f"kS38,{lvl.color_channels},kA13,{lvl.song_offset},kA15,{lvl.song_fadeIn},"
        head += f"kA16,{lvl.song_fadeOut},kA14,{lvl.guidelines},kA6,{lvl.bg_texture},kA7,{lvl.ground_texture},"
        head += f"kA17,{lvl.line},kA18,{lvl.font},kS39,0,kA2,{lvl.gamemode},kA3,{lvl.mini},kA8,{lvl.dual},kA4,{lvl.speed},"
        head += f"kA9,0,kA10,{lvl.twoPlayerMode},kA11,{lvl.upsideDown};"
        s = self.__xor__(self, head.encode("utf-8")).decode('utf-8') 
        s += self.__xor__(self, lvl.genstr().encode('utf-8')).decode('utf-8')
        with open(p, "w") as f:
            f.write(s)

    @classmethod
    def fromfile(self, path: str):
        """
        Load a level from a file.
        """
        f = open(path, "r")
        d = self.__xor__(self, f.read().encode('utf-8')).decode('utf-8')
        e = d.split(";")
        props = e[0].split(",")
        lvl = GeometryDashLevel(props[0], props[1], props[2], e[1])
        lvl.color_channels = props[4]
        lvl.song_offset = props[6]
        lvl.song_fadeIn = bool(int(props[8]))
        lvl.song_fadeOut = bool(int(props[10]))
        lvl.guidelines = props[12]
        lvl.bg_texture = props[14]
        lvl.ground_texture = props[16]
        lvl.line = props[18]
        lvl.font = props[20]
        lvl.gamemode = props[22]
        lvl.mini = bool(int(props[24]))
        lvl.dual = bool(int(props[26]))
        lvl.speed = props[28]
        lvl.twoPlayerMode = bool(int(props[30]))
        lvl.upsideDown = bool(int(props[32]))
        return lvl

class OfficialSong:
    """
    This is a class for official songs.

    ### Functions:
        `getSongByID(ID: int)` Get a song by its ID.
        `getSongByName(name: str)` Get a song by its name.
    """
    def __init__(self, ID=None):
        self.ID = ID if ID else None

    def __str__(self):
        return f"OfficialSong: ID={self.ID}"

    def getSongByID(self, ID):
        """
        Get a song by its ID.
        """
        return OfficialSong(ID)
    
    def getSongByName(self, name: str):
        """
        Get a song by its name.
        """
        match name:
            case "Stereo Madness":
                return OfficialSong(0)
            case "Back on Track":
                return OfficialSong(1)
            case "Polargeist":
                return OfficialSong(2)
            case "Dry Out":
                return OfficialSong(3)
            case "Base After Base":
                return OfficialSong(4)
            case "Cant Let Go":
                return OfficialSong(5)
            case "Jumper":
                return OfficialSong(6)
            case "Time Machine":
                return OfficialSong(7)
            case "Cycles":
                return OfficialSong(8)
            case "xStep":
                return OfficialSong(9)
            case "Clutterfunk":
                return OfficialSong(10)
            case "Theory of Everything":
                return OfficialSong(11)
            case "Electroman Adventures":
                return OfficialSong(12)
            case "Clubstep":
                return OfficialSong(13)
            case "Electrodynamix":
                return OfficialSong(14)
            case "Hexagon Force":
                return OfficialSong(15)
            case "Blast Processing":
                return OfficialSong(16)
            case "Theory of Everything 2":
                return OfficialSong(17)
            case "Geometrical Dominator":
                return OfficialSong(18)
            case "Deadlocked":
                return OfficialSong(19)
            case "Fingerdash":
                return OfficialSong(20)
            case "Dash":
                return OfficialSong(21)
            
class CustomSong:
    """
    This is a class for custom songs.

    ### Functions:
        `getSongByID(ID: int)` Get a custom song by its ID.

    """
    def __init__(self, ID=None):
        self.ID = ID if ID else None

    def __str__(self):
        return f"CustomSong: ID={self.ID}"

    def getSongByID(self, ID):
        """
        Get a custom song by its ID.
        """
        return CustomSong(ID) 

class Color:
    """
    This is a class for colors.

    ### Parameters:
        r (int): The red value.
        g (int): The green value.
        b (int): The blue value.
    """
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

class GeometryDashObject:
    """
    This is a class for Geometry Dash objects.

    ### Parameters:
        objectID (int): The object's ID.
        x (int): The object's X position.
        y (int): The object's Y position.
        dir (int): The object's direction.

    ### Object Properties:
        flipX (int): The object's flipX property.
        flipY (int): The object's flipY property.
        yellowLayer (int): The object's yellow layer.
        baseHSV (float): The object's base HSV property.
        detailHSV (float): The object's detail HSV property.
        copyColorID (int): The object's copy color ID property.
        zLayer (int): The object's Z layer.
        scale (float): The object's scale.
        groupParent (int): The object's group parent property.
        editorLayer1 (int): The object's editor layer 1.
        editorLayer2 (int): The object's editor layer 2.
        copyOpacity (int): The object's copy opacity property.
        colBlending (int): The object's color blending property.
        targetGroup (int): The object's target group.
        extra (list): The object's extra property.
        baseHSVEnabled (int): The object's base HSV enabled property.
        detailHSVEnabled (int): The object's detail HSV enabled property.
        editorLayer3 (int): The object's editor layer 3.
        base (int or color): The object's base color.
        detail (int or color): The object's detail color.
        textValue (str): The object's text value.
        touchTriggered (int): The object's touch triggered property.
        coinID (int): The object's coin ID property.
        fadeIn (int): The object's fade in property.
        groups (list): The object's groups.
        lockPlayerX (int): The object's lock player X property.

    ### Extra Properties:
        other (list): The object's other properties.
    """

    def __init__(self, objectID: int, x: int, y: int, dir, other: list=None, 
                    flipX: int=None,
                    flipY: int=None,
                    yellowLayer: int=None,
                    baseHSV: float=None,
                    detailHSV: float=None,
                    copyColorID: int=None,
                    zLayer: int=None,
                    scale: float=None,
                    groupParent=None,
                    editorLayer1: int=None,
                    editorLayer2: int=None,
                    copyOpacity: int=None,
                    colBlending: int=None,
                    targetGroup: int=None,
                    extra=None, # (list?)
                    baseHSVEnabled: int=None,
                    detailHSVEnabled: int=None,
                    editorLayer3: int=None,
                    base=None, # (int or color)
                    detail=None, # (int or color)
                    textValue=None, # (any)
                    touchTriggered: int=None,
                    coinID: int=None,
                    fadeIn: int=None,
                    groups: list=[],
                    lockPlayerX: int=None,
                    GJVAL_REGION: int=None,
                ):
        self.objectID = objectID
        self.x = int(x)
        self.y = int(y)
        self.dir = dir
        self.flipX = flipX if flipX else None
        self.flipY = flipY if flipY else None
        self.yellowLayer = yellowLayer if yellowLayer else None
        self.baseHSV = baseHSV if baseHSV else None
        self.detailHSV = detailHSV if detailHSV else None
        self.copyColorID = copyColorID if copyColorID else None
        self.zLayer = zLayer if zLayer else None
        self.scale = scale if scale else None
        self.groupParent = groupParent if groupParent else None
        self.editorLayer1 = editorLayer1 if editorLayer1 else None
        self.editorLayer2 = editorLayer2 if editorLayer2 else None
        self.copyOpacity = copyOpacity if copyOpacity else None
        self.colBlending = colBlending if colBlending else None
        self.targetGroup = targetGroup if targetGroup else None
        self.extra = extra if extra else None
        self.baseHSVEnabled = baseHSVEnabled if baseHSVEnabled else None
        self.detailHSVEnabled = detailHSVEnabled if detailHSVEnabled else None
        self.editorLayer3 = editorLayer3 if editorLayer3 else None
        self.base = base if base else None
        self.detail = detail if detail else None
        self.textValue = textValue if textValue else None
        self.touchTriggered = touchTriggered if touchTriggered else None
        self.coinID = coinID if coinID else None
        self.fadeIn = fadeIn if fadeIn else None
        self.groups = groups if groups else []
        self.lockPlayerX = lockPlayerX if lockPlayerX else None
        self.other = other if other else None
        self.textValue = str(textValue) if textValue else None
        
        self.region = GJVAL_REGION if GJVAL_REGION else None

    def __str__(self):
        base_str = f"GeometryDashObject: objectID={self.objectID}, x={self.x}, y={self.y}, dir={self.dir}"
        if self.textValue:
            base_str += f", textValue={self.textValue}"
        if self.groups:
            base_str += f", groups={self.groups}"
        base_str += f", other={self.other}"
        return base_str
    
    def __repr__(self):
        return self.__str__() + "\n"
    
    def generate_string(self) -> str:
        base_string = f"1,{self.objectID},2,{self.x},3,{self.y},"
        
        if self.flipX:
            base_string += f"4,{self.flipX},"
        if self.flipY:
            base_string += f"5,{self.flipY}," 
        base_string += f"6,{self.dir},"
        if self.yellowLayer:
            base_string += f"7,{self.yellowLayer},"
        if self.baseHSV:
            base_string += f"8,{self.baseHSV},"
        if self.detailHSV:    
            base_string += f"9,{self.detailHSV},"
        if self.copyColorID:
            base_string += f"10,{self.copyColorID},"
        if self.zLayer:
            base_string += f"11,{self.zLayer},"
        if self.textValue:
            base_string += f"31,{base64.b64encode(self.textValue.encode('utf-8')).decode('utf-8')},"
        if self.fadeIn:
            base_string += f"36,{self.fadeIn},"
        if self.groups: 
            if len(self.groups) > 1:
                base_string += "57,"
                for g in self.groups:
                    base_string += f"{g}."
                base_string = base_string.removesuffix(".") + ","
            else:
                base_string += f"57,{self.groups[0]},"
        if self.lockPlayerX:
            base_string += f"155,{self.lockPlayerX},"

        if self.other:
            for i in range(len(self.other)):
                base_string += f"{self.other[i][0]},{self.other[i][1]},"
        return base_string.removesuffix(",") + ";"
    
    def snap_to_grid(self, snap=30):
        """
        Snap the object to the grid.
        """
        self.x = math.floor(self.x/snap)*snap+15
        self.y = math.floor(self.y/snap)*snap+15
        return self
    
    def getProperty(self, p: int, returnZero=False) -> str:
        """
        Get a property of the object.

        ### Parameters:
            p (int): The property ID.
            returnZero (bool): Whether to return 0 if the property is not found.
        """
        for i in range(len(self.other)):
            if self.other[i][0] == str(p):
                return self.other[i][1]
        return "0" if returnZero else None
    
    def setProperty(self, p: int, v: int) -> None:
        """
        Set a property of the object.

        If there is no property with the specified ID, it will create a new one.

        ### Parameters:
            p (int): The property ID.
            v (int): The property value.
        """
        for i in range(len(self.other)):
            if self.other[i][0] == str(p):
                self.other[i][1] = str(v)
                return
        self.other.append([str(p), str(v)])

    def setPropertyInLevel(self, p: int, v: int, level) -> None:
        """
        Set a property of the object.

        If there is no property with the specified ID, it will create a new one.

        ### Parameters:
            p (int): The property ID.
            v (int): The property value.
        """
        level.remove_object(self)
        self.setProperty(p, v)
        level.add_object(self)

    def add_group(self, group: int) -> None:
        """
        Add the object to a group.

        ### Parameters:
            group (int): The group ID.
        """
        if group not in self.groups:
            self.groups.append(group)

    def remove_group(self, group: int) -> None:
        """
        Remove the object from a group.

        ### Parameters:
            group (int): The group ID.
        """
        if group in self.groups:
            self.groups.remove(group)

    def clear_groups(self) -> None:
        """
        Clear all groups from the object.
        """
        self.groups = []

class GeometryDashLevel:
    """
    This is a class for Geometry Dash levels.

    ### Parameters:
        title (str): The level's title.
        author (str): The level's author.
        description (str): The level's description.
        data (str): The level's data.

    ### Extra Properties:
        revision (int): The level revision.
        speed (int): The speed that the level starts with.
        gamemode (int): The level's gamemode.
        color_channels (int): The level's color channels.
        song_offset (float): The level's song offset.
        song_fadeIn (bool): The level's song fade in property.
        song_fadeOut (bool): The level's song fade out property.
        guidelines (int): The level's guidelines.
        bg_texture (int): The level's background texture.
        ground_texture (int): The level's ground texture.
        line (int): The level's line.
        font (int): The level's font.
        mini (bool): The level's mini property.
        dual (bool): The level's dual property.
        twoPlayerMode (bool): The level's two player mode property.
        upsideDown (bool): The level's upside down property.
        song (OfficialSong or CustomSong): The level's song.
        bg_color (Color): The level's background color.
        ground_color (Color): The level's ground color.
        verified (bool): The level's verified property. (Not recommended if you want your level to be rated ;P)
    """
    def __init__(self, title: str, author: str, description: str, data: str, 
                    revision: int=None, 
                    speed: int=None, 
                    gamemode=None, 
                    color_channels=None,
                    song_offset: float=None,
                    song_fadeIn: bool=None,
                    song_fadeOut: bool=None,
                    guidelines=None,
                    bg_texture: int=None,
                    ground_texture: int=None,
                    line=None,
                    font=None,
                    mini=None,
                    dual=None,
                    twoPlayerMode: bool=None,
                    upsideDown: bool=None,
                    song=None, 
                    bg_color: Color=None, 
                    ground_color: Color=None,
                    verified: bool=None,
                ):
        self.title = title
        self.author = author
        self.description = description
        self.revision = revision if revision else 0
        self.speed = speed if speed else ""
        if (gamemode == None):
            self.gamemode = ""
        else:
            self.gamemode = gamemode
            match self.gamemode:
                case "cube":
                    self.gamemode = 0
                case "ship":
                    self.gamemode = 1
                case "ball":
                    self.gamemode = 2
                case "ufo":
                    self.gamemode = 3
                case "wave":
                    self.gamemode = 4
                case "robot":
                    self.gamemode = 5
                case "spider":
                    self.gamemode = 6
                case "swing":
                    self.gamemode = 7
            
        self.color_channels = color_channels if color_channels else []
        self.c = ""
        self.song_offset = song_offset if song_offset else ""
        self.song_fadeIn = 1 if song_fadeIn else 0
        self.song_fadeOut = 1 if song_fadeOut else 0
        self.guidelines = guidelines if guidelines else ""
        self.bg_texture = bg_texture if bg_texture else ""
        self.ground_texture = ground_texture if ground_texture else ""
        self.line = line if line else ""
        self.font = font if font else ""
        self.mini = 1 if mini else 0
        self.dual = 1 if dual else 0
        self.twoPlayerMode = 1 if twoPlayerMode else 0
        self.upsideDown = 1 if upsideDown else 0
        self.song = song if song else ""

        # just so people don't get confused when the level has no "bg_color" or "ground_color" properties
        self.bg_color = bg_color
        self.ground_color = ground_color

        self.verified = 1 if verified else 0
        self.GJVAL_UPLOADED = False
        self.data = data if data else ""
        self.objects = ""

    def __str__(self):
        return f"GeometryDashLevel: title={self.title}, author={self.author}, description={self.description}, revision={self.revision}, data={self.data}"

    def get_max_number(self, xml) -> int:
        level_numbers = []
        for e in xml.iter():
            if e.tag == "k":
                if e.text.startswith("k_"):
                    if (e.text.removeprefix("k_") == "0"): 
                        if (len(level_numbers) == 0):
                            level_numbers.append(e.text.removeprefix("k_"))
                    else:
                        level_numbers.append(e.text.removeprefix("k_"))
        return int(level_numbers[len(level_numbers)-1])
    
    def generate_string(self, xml, force_index=None, no_wrapper=None) -> str:
        if self.bg_color: self.c += f"1_{self.bg_color.r}_2_{self.bg_color.g}_3_{self.bg_color.b}_11_255_12_255_13_255_4_-1_6_1000_7_1_15_1_18_0_8_1|"
        if self.ground_color: self.c += f"1_{self.ground_color.r}_2_{self.ground_color.g}_3_{self.ground_color.b}_11_255_12_255_13_255_4_-1_6_1001_7_1_15_1_18_0_8_1|"

        for i in range(len(self.color_channels)):
            c = self.color_channels[i]
            self.c += f"1_{c.r}_2_{c.g}_3_{c.b}_11_255_12_255_13_255_4_-1_6_{i+1}_7_1_15_1_18_0_8_1|"
        
        initial_lvlstring = f"kS38,{self.c},kA13,{self.song_offset},kA15,{self.song_fadeIn},kA16,{self.song_fadeOut},kA14,{self.guidelines},kA6,{self.bg_texture},kA7,{self.ground_texture},kA17,{self.line},kA18,{self.font},kS39,0,kA2,{self.gamemode},kA3,{self.mini},kA8,{self.dual},kA4,{self.speed},kA9,0,kA10,{self.twoPlayerMode},kA11,{self.upsideDown};"

        if (not self.data): self.data = base64.urlsafe_b64encode(gz.compress(initial_lvlstring.encode('utf-8') + self.objects.encode('utf-8'))).decode('utf-8')
        key_prefix = f"k_{str(self.get_max_number(xml) + 1) if force_index == None else force_index}"
        use_desc = False
        if no_wrapper != None:
            if no_wrapper:
                base_str = f"<root><k>kCEK</k><i>4</i><k>k2</k><s>{self.title}</s><k>k4</k><s>{self.data}</s><k>k3</k><s>{base64.b64encode(self.description.encode('utf-8')).decode('utf-8')}</s><k>k46</k><s>{self.revision}</s><k>k5</k><s>{self.author}</s><k>k13</k><t /><k>k21</k><i>2</i><k>k16</k><i>1</i><k>k80</k><i>0</i><k>k50</k><i>35</i><k>k47</k><t /><k>kI1</k><r>0</r><k>kI2</k><r>36</r><k>kI3</k><r>1</r>" if use_desc else f"<root><k>kCEK</k><i>4</i><k>k2</k><s>{self.title}</s><k>k4</k><s>{self.data}</s><k>k46</k><s>{self.revision}</s><k>k5</k><s>{self.author}</s><k>k13</k><t /><k>k21</k><i>2</i><k>k16</k><i>1</i><k>k80</k><i>0</i><k>k50</k><i>35</i><k>k47</k><t /><k>kI1</k><r>0</r><k>kI2</k><r>36</r><k>kI3</k><r>1</r>"
            else:
                base_str = f"<root><k>{key_prefix}</k><d><k>kCEK</k><i>4</i><k>k2</k><s>{self.title}</s><k>k4</k><s>{self.data}</s><k>k3</k><s>{base64.b64encode(self.description.encode('utf-8')).decode('utf-8')}</s><k>k46</k><s>{self.revision}</s><k>k5</k><s>{self.author}</s><k>k13</k><t /><k>k21</k><i>2</i><k>k16</k><i>1</i><k>k80</k><i>0</i><k>k50</k><i>35</i><k>k47</k><t /><k>kI1</k><r>0</r><k>kI2</k><r>36</r><k>kI3</k><r>1</r>" if use_desc else f"<root><k>{key_prefix}</k><d><k>kCEK</k><i>4</i><k>k2</k><s>{self.title}</s><k>k4</k><s>{self.data}</s><k>k46</k><s>{self.revision}</s><k>k5</k><s>{self.author}</s><k>k13</k><t /><k>k21</k><i>2</i><k>k16</k><i>1</i><k>k80</k><i>0</i><k>k50</k><i>35</i><k>k47</k><t /><k>kI1</k><r>0</r><k>kI2</k><r>36</r><k>kI3</k><r>1</r>"
        else:
            base_str = f"<root><k>{key_prefix}</k><d><k>kCEK</k><i>4</i><k>k2</k><s>{self.title}</s><k>k4</k><s>{self.data}</s><k>k3</k><s>{base64.b64encode(self.description.encode('utf-8')).decode('utf-8')}</s><k>k46</k><s>{self.revision}</s><k>k5</k><s>{self.author}</s><k>k13</k><t /><k>k21</k><i>2</i><k>k16</k><i>1</i><k>k80</k><i>0</i><k>k50</k><i>35</i><k>k47</k><t /><k>kI1</k><r>0</r><k>kI2</k><r>36</r><k>kI3</k><r>1</r>" if use_desc else f"<root><k>{key_prefix}</k><d><k>kCEK</k><i>4</i><k>k2</k><s>{self.title}</s><k>k4</k><s>{self.data}</s><k>k46</k><s>{self.revision}</s><k>k5</k><s>{self.author}</s><k>k13</k><t /><k>k21</k><i>2</i><k>k16</k><i>1</i><k>k80</k><i>0</i><k>k50</k><i>35</i><k>k47</k><t /><k>kI1</k><r>0</r><k>kI2</k><r>36</r><k>kI3</k><r>1</r>"

        if self.song and isinstance(self.song, OfficialSong): base_str += f"<k>k8</k><i>{self.song.ID}</i>" if isinstance(self.song, OfficialSong) else ""
        if self.song and isinstance(self.song, CustomSong): base_str += f"<k>k45</k><i>{self.song.ID}</i>" if isinstance(self.song, CustomSong) else ""
        if self.verified: base_str += f"<k>k14</k><t />"
        if self.GJVAL_UPLOADED: base_str += f"<k>k15</k><t />"
        base_str += (f"</d></root>" if not no_wrapper else "</root>")
        return base_str
    
    def genstr(self) -> str:
        initial_lvlstring = f"kS38,{self.color_channels},kA13,{self.song_offset},kA15,{self.song_fadeIn},kA16,{self.song_fadeOut},kA14,{self.guidelines},kA6,{self.bg_texture},kA7,{self.ground_texture},kA17,{self.line},kA18,{self.font},kS39,0,kA2,{self.gamemode},kA3,{self.mini},kA8,{self.dual},kA4,{self.speed},kA9,0,kA10,{self.twoPlayerMode},kA11,{self.upsideDown};"
        return base64.urlsafe_b64encode(gz.compress(initial_lvlstring.encode('utf-8') + self.objects.encode('utf-8'))).decode('utf-8')

    def add_object(self, obj: GeometryDashObject) -> None:
        """
        Add an object to the level.
        """
        self.objects += obj.generate_string()

    def remove_object(self, obj: GeometryDashObject) -> None:
        """
        Remove an object from the level.
        """
        self.objects = self.objects.replace(obj.generate_string(), "", 1)
    
    def add_objects(self, objects: list[GeometryDashObject]) -> None:
        """
        Add a list of objects to the level.
        """
        for obj in objects:
            self.add_object(obj)

    def getObjects(self) -> list[GeometryDashObject]:
        """
        Get all the objects in the level.
        """
        return decode_level_string(gz.decompress(base64.urlsafe_b64decode(self.data.removesuffix("=").join("=="))).decode('utf-8'))
    
    def objfind(self, ID: int=None, group: list=None, levelObject: GeometryDashObject=None, region: int=None) -> GeometryDashObject:
        """
        Find an object with a specific property.

        ### Parameters (Positional):
            ID (int): The object ID.
            group (int): The object group.
            levelObject (GeometryDashObject): The object to find.
        """
        objs = self.getObjects() if self.data else (decode_level_string(self.objects) if not region else decode_level_string(self.objects, region=region))
        
        for obj in objs:
            if ID and int(obj.objectID) == ID:
                return obj
            if group and str(group) in obj.groups:
                return obj
            if levelObject and obj == levelObject:
                return obj
    
    def objfindall(self, ID: int=None, group: list=None) -> list[GeometryDashObject]:
        """
        Find all objects with a specific property.

        ### Parameters (Positional):
            ID (int): The object ID.
            group (int): The object group.
        """
        found = []
        objs = self.getObjects() if self.data else decode_level_string(self.objects)
        for obj in objs:
            if ID and int(obj.objectID) == ID:
                found.append(obj)
            if group and str(group) in obj.groups:
                found.append(obj)

        return found
    
    def findindex(self, xml: Optional[ET.Element]) -> None:
        """
        Find the index of the level in your save.
        """
        flag = False
        matching = 0
        for e in xml.find(".//dict").find(".//d"):
            if flag:
                fTitle = False
                fData = False
                for elem in e.iter():
                    if fTitle:
                        if elem.text == self.title:
                            matching += 1
                        fTitle = not fTitle
                    if fData:
                        if elem.text == base64.urlsafe_b64encode(gz.compress(self.data.encode('utf-8'))).decode('utf-8'):
                            matching += 1
                        fData = not fData
                    
                    if elem.text == "k2":
                        fTitle = True
                    if elem.text == "k4":
                        fData = True
                flag = not flag

            if e.tag == "k":
                if e.text.startswith("k_"):
                    if matching > 0:
                        return int(e.text.removeprefix("k_"))-1
                    flag = True
                    continue
    
    def upload(self):
        """
        Upload the level to the Geometry Dash servers.
        """
        if not self.GJVAL_UPLOADED:
            print("[LOG] Uploading level...")
            self.GJVAL_UPLOADED = True
        else:
            print("[LOG] Level already uploaded.")

class fetch:
    """
    ## fetch
    This is a class for getting data from the Geometry Dash servers.
    """
    def __init__(self):
        pass
    
    @staticmethod
    def get(ID: int) -> str:
        # test
        # playername = "robtop"

        # url = "http://www.boomlings.com/database/getGJUsers20.php"
        # params = "gameVersion=21&binaryVersion=35&gdw=0&str="+playername+"&total=0&page=0&secret=Wmfd2893gb7"
        
        # try:
        #     fetched = urlopen(url, params.encode('utf-8')).read().decode('utf-8')
        # except HTTPError as e:
        #     print(f"[LOG] HTTPError: {e.code} - {e.reason}")
        #     return
        # except URLError as e:  
        #     print(f"[LOG] URLError: {e.reason}")
        #     return
        # except Exception as e:
        #     print(f"[LOG] Exception: {e}")
        #     return

        # return fetched

        url = "http://www.boomlings.com/database/downloadGJLevel22.php"
    
        data = {
            "levelID": str(ID),
            "secret": "Wmfd2893gb7",
            "gameVersion": "21",
            "binaryVersion": "35",
            "gdw": "0"
        }
        
        headers = {
            "User-Agent": "Geometry Dash/2.2",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*"
        }

        proxies = {
            "http": "http://85.143.254.38:1080",
        }
        
        response = requests.get(url, data=data, headers=headers)
        
        if response.status_code != 200:
            print(f"[LOG] HTTPError: {response.status_code} - {response.reason}")
            return
        
        return response.text

class logic:
    """
    PRE-ALPHA (NOT IN WORKING STATE)

    ## Logic
    This is a class for turning code into Geometry Dash levels.
    """
    def __init__(self, endFrame=0):
        self.endFrame = endFrame
        self.ctx: logic.context = None
        self.preload()
        self.onStart()
        print("[LOG] Logic loop running. (logic)")
        while True:
            spinnythingy = "/-\\|"[(self.ctx.frame//70)%4]
            print(f"[LOG] LOGIC! Frame {self.ctx.frame} {spinnythingy}")
            self.onUpdate()
            self.loop(self.ctx)

            if self.endFrame > 0:
                if self.ctx.frame >= self.endFrame:
                    self.onEnd()
                    break
        print("[LOG] Logic loop terminated. (logic)")
    
    class context:
        """
        ## logic.context
        This is a class for the context of the logic class.

        ### Parameters:
        level (GeometryDashLevel): The level to add the objects to.
        """
        def __init__(self, level: GeometryDashLevel, GJVAL_FR=None, GJVAL_CTX=None):
            if GJVAL_CTX == None:
                raise SystemExit("[LOG] ERROR: Use newContext() to create contexts. (logic.context)")

            self.level = level
            self.frame = 0 if GJVAL_FR == None else GJVAL_FR
            self.GR = 1
            self.GJVAL_PREVOBJ: GeometryDashObject = None
            self.GJVAL_OPX = 0
            self.GJVAL_OPY = 0

        @staticmethod
        def newContext(level):
            """
            Create a new context.

            ### Parameters:
            level (GeometryDashLevel): The level to assign the context to.
            """
            return logic.context(level=level, GJVAL_CTX=1)
        
        def positionObject(self, lvlobj: GeometryDashObject, x: int, y: int) -> None:
            """
            Set the position of an object.
            """

            # find the object and add it to a group
            o = self.level.objfind(ID=lvlobj.objectID)
            o2 = GeometryDashObject(o.objectID, o.x, o.y, o.dir, other=o.other, groups=o.groups)
            o2.add_group(self.GR)
            self.level.remove_object(o)
            self.level.add_object(o2)
            # print(o.generate_string())
            self.GJVAL_OPX = o2.x
            self.GJVAL_OPY = o2.y
            # add a move trigger
            moveTrigger = GeometryDashObject(901, self.frame, 315, 0, 
                                              [['10', '0'],
                                              ['28', str((x-o.x)//3)],
                                              ['29', '0'],
                                              ['51', str(self.GR)]]
                                            )
            
            print(self.GJVAL_OPX, self.GJVAL_OPY, o2.x, o2.y)
            if not self.GJVAL_OPX == o2.x and not self.GJVAL_OPY == o2.y:
                self.level.add_object(moveTrigger)
            else:    
                if self.GJVAL_PREVOBJ:
                    if self.GJVAL_PREVOBJ.objectID != o.objectID:
                        self.level.add_object(moveTrigger)
                else:
                    self.level.add_object(moveTrigger)

            # if it's the same object, don't increment the group
            if self.GJVAL_PREVOBJ:
                if self.GJVAL_PREVOBJ.objectID != o.objectID:
                    self.GR += 1
            
            self.GJVAL_PREVOBJ = o
            self.GJVAL_OPX = x
            self.GJVAL_OPY = y

    @staticmethod
    def loop(ctx: context) -> None:
        ctx.frame += 1

    def preload(self) -> None:
        pass

    def onUpdate(self) -> None:
        pass

    def onStart(self) -> None:
        pass

    def onEnd(self) -> None:
        pass
    
    @staticmethod
    def createContext() -> context:
        return logic.context(GJVAL_CTX=1)
        
def kbmb(size) -> str:
    if size < 1048576:
        return str(0.01*round(100*(size/1024))) + " KB"
    elif size < 1073741824:
        return str(0.01*round(100*(size/1048576))) + " MB"

def xor_bytes(byteData) -> bytes:
    return bytes(b ^ 11 for b in byteData)

def blocks(x) -> int:
    return x*30

def encrypt(path, out_path):
    open(out_path, "w").close()
    try:
        with open(path, 'rb') as f:
            file = f.read()
            print(f"[LOG] Successfully opened XML ({path})")
            print(f"[LOG] Read {len(file)} bytes ({kbmb(len(file))})")

        try:
            encoded_file1 = gz.compress(file)
            print("[LOG] Successfully compressed XML.")

            try:
                encoded_file2 = base64.urlsafe_b64encode(encoded_file1)
                print("[LOG] Successfully Base64 encoded file.")

                try:
                    encoded_file3 = xor_bytes(encoded_file2)
                    print("[LOG] Successfully XOR encrypted file.")

                    with open(out_path, 'wb') as f:
                        f.write(encoded_file3)
                        print(f"[LOG] Successfully saved file to {out_path}")
                except Exception as e:
                    print(f"[LOG] ERROR: Failed to encrypt file ({str(e)})")
                    
            except Exception as e:
                print(f"[LOG] ERROR: Failed to encode file ({str(e)})")

        except Exception as e:
            print(f"[LOG] ERROR: Failed to compress XML ({str(e)})")

    except Exception as e:
        print("[LOG] ERROR: No such file or directory.")
        print("Stopping...")
        return

def decrypt(path):
    try:
        with open(path, 'rb') as f:
            file = f.read()
            print(f"[LOG] Successfully opened file ({path})")
            print(f"[LOG] Read {len(file)} bytes ({kbmb(len(file))})")

        try:
            decoded_file1 = xor_bytes(file)
            print("[LOG] Successfully XOR decrypted file.")

            try:
                padding_needed = len(file) % 4
                if padding_needed:
                    file += b'=' * (4 - padding_needed)

                decoded_file2 = base64.urlsafe_b64decode(decoded_file1)
                print("[LOG] Successfully Base64 decoded file.")

                try:
                    gz_f = gz.decompress(decoded_file2)
                    print("[LOG] Successfully gzip decompressed file.")
                    return gz_f
                except Exception as e:
                    print(f"[LOG] ERROR: Failed gzip decompression ({str(e)})")
            
            except Exception as e:
                print(f"[LOG] ERROR: Failed to decode file ({str(e)})")
                pass

        except Exception as e:
            print(f"[LOG] ERROR: Failed to XOR decrypt file ({str(e)})")
        
    except Exception as e:
        print("[LOG] ERROR: No such file or directory.")
        print("Stopping...")
        return

def parse_xml(xml: bytes) -> Optional[ET.Element]:
    try:
        string = xml.decode('utf-8')
        root = ET.fromstring(string)
        print("[LOG] Successfully parsed XML code.")
        return root
    except Exception as e:
        print(f"[LOG] ERROR: Failed to parse XML code ({str(e)})")

def insert_level_data(xml: ET.Element, level_data: str) -> bool:
    try:
        level = ET.fromstring(level_data)

        dict = xml.find(".//dict")

        for elem in xml.iter("k"):
            if elem.text == "LLM_01":
                d = dict.findall(".//d")[0]

                if d != None:
                    d.extend(level)
                    return True
                else:
                    print("[LOG] d tag is None.")
                    return False
        
        print("[LOG] LLM_01 label not found.")
        return False 
    except ET.ParseError as e:
        print(f"[LOG] insert_level_data returned False. ({str(e)})")
        return False

def save_xml(xml: ET.Element, path: str) -> bool:
    try:
        tree = ET.ElementTree(xml)
        tree.write(path, encoding='utf-8', xml_declaration=True)
        print("[LOG] save_xml returned True.")
        return True
    except Exception:
        print("[LOG] save_xml returned False.")
        return False
    
def modify_xml(path_in: str, path_out: str, level: GeometryDashLevel) -> bool:
    tree = ET.parse(path_in)
    root = tree.getroot()

    if insert_level_data(root, level.generate_string(root)):
        if save_xml(root, path_out):
            print("[LOG] Successfully modified XML code.")
        else:
            print("[LOG] ERROR: Failed to save XML code.")
    else:
        print("[LOG] ERROR: Failed to insert level data.")
        return False

def remove_tag(xml: ET.Element, tag: str) -> bool:
    for parent in xml.findall(f".//{tag}"):
        grandparent = xml.find(f".//{tag}/..")

        if grandparent:
            index = list(grandparent).index(parent)
            grandparent.remove(parent)

            for i, child in enumerate(parent):
                grandparent.insert(index + i, child)

def add_level(level: GeometryDashLevel):
    """
    Add a level to Geometry Dash.
    """
    decoded = decrypt(os.path.expandvars(r"%localappdata%\GeometryDash\CCLocalLevels.dat"))
    xml_code = parse_xml(decoded)

    if insert_level_data(xml_code, level.generate_string(xml_code)):
        remove_tag(xml_code, "root")
        et = ET.ElementTree(xml_code)

        et.write(Path(".")/"resources"/"xml"/"levels.xml", encoding='utf-8', xml_declaration=True)
        encrypt(Path(".")/"resources"/"xml"/"levels.xml", os.path.expandvars(r"%localappdata%\GeometryDash\CCLocalLevels.dat"))
        encrypt(Path(".")/"resources"/"xml"/"levels.xml", os.path.expandvars(r"%localappdata%\GeometryDash\CCLocalLevels2.dat"))
        print("[LOG] Successfully encrypted XML code.")
    else:
        print(f"[LOG] ERROR: Failed to encrypt XML code.")
        return False
    
def set_level(input: GeometryDashLevel, out: GeometryDashLevel):
    """
    Set an existing level from your save to a new level.
    """
    decoded = decrypt(os.path.expandvars(r"%localappdata%\GeometryDash\CCLocalLevels.dat"))
    xml_code = parse_xml(decoded)
    index = input.findindex(xml_code)
    editflag = False

    for elem in xml_code.find(".//dict").find(".//d"):
        if editflag:
            elem.clear()
            lvldata = out.generate_string(xml_code, force_index=index, no_wrapper=True)
            elem.extend(ET.fromstring(lvldata))
            et = ET.ElementTree(xml_code)
            for e in elem.iter():
                print(e.tag, e.text)
            et.write(Path(".")/"resources"/"xml"/"levels.xml", encoding='utf-8', xml_declaration=True)
            encrypt(Path(".")/"resources"/"xml"/"levels.xml", os.path.expandvars(r"%localappdata%\GeometryDash\CCLocalLevels.dat"))
            encrypt(Path(".")/"resources"/"xml"/"levels.xml", os.path.expandvars(r"%localappdata%\GeometryDash\CCLocalLevels2.dat"))
            break

        if elem.tag == "k" and elem.text == f"k_{index}":
            editflag = True
            continue

def preview_level(level: GeometryDashLevel, path: Path):
    """
    Create a live preview of the level (WIP)

    ### Parameters:
        level (GeometryDashLevel): The level to preview.
        path (Path): The path to the script you're running the live server on (just use Path(__file__)/"your_file.py").
    """
    objs = decode_level_string(gz.decompress(base64.urlsafe_b64decode(level.genstr())).decode('utf-8'), asObject=True)
    json.dump(objs, open(Path(".")/"lib"/"live_preview"/"assets"/"level"/"level.json", "w"), indent=4)
    open(Path(".")/"lib"/"live_preview"/"eventhandler"/"path.txt", "w").write(str(path.parent))

    os.startfile(Path(".")/"lib"/"live_preview"/"start.bat") # start the server
    os.startfile(Path(".")/"lib"/"live_preview"/"eventhandler"/"LivePreviewEventHandler.py") # open the preview
    webbrowser.open("http://localhost:8000/lib/live_preview/index.html") # open the preview

def decode_level_string(data: str, region: int=None, asObject: bool=None) -> list[GeometryDashObject]:
    level_objects = []
    level_objects_str = data.split(";")
    
    c = 0
    for l in level_objects_str:
        if (region): 
            if (math.floor(c/16) != region): continue
        obj = l.split(",")
        if (len(obj) < 6):
            continue
        if(obj[0].startswith("k")):
            continue
        x = obj[1]
        y = obj[3]
        flipX = 0 # property 4
        flipY = 0 # property 5
        dir = 0 # property 6
        yellowLayer = 0 # property 7 (r)
        baseHSV = 0 # property 8 (g)
        detailHSV = 0 # property 9 (b)
        copyColorID = 0 # property 10 (duration)
        zLayer = 0 # property 11
        scale = 0 # property 13
        groupParent = 0 # property 15
        editorLayer1 = 0 # property 17
        editorLayer2 = 0 # property 20
        copyOpacity = 0 # property 21 (base)
        colBlending = 0 # property 22
        targetGroup = 0 # property 23
        extra = 0 # property 24
        baseHSVEnabled = 0 # property 25
        detailHSVEnabled = 0 # property 26
        editorLayer3 = 0 # property 28 (target move x)
        base = 0 # property 29 (target move y)
        detail = 0 # property 30
        textValue = 0 # property 31
        touchTriggered = 0 # property 32
        coinID = 0 # property 34
        # property 35 is target opacity
        fadeIn = 0 # property 36
        # property 51 is also target group??!?!
        groups = [] # property 57
        # property 85 is move time
        lockPlayerX = 0 # property 155
        other = []

        for i in range(int(round(len(obj)/2))):
            if i > 2:
                if obj[(2*i+1)-1] == "6":
                    dir = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "7":
                    yellowLayer = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "8":
                    baseHSV = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "9":
                    detailHSV = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "10":
                    copyColorID = float(obj[2*i+1])
                elif obj[(2*i+1)-1] == "11":
                    zLayer = int(obj[2*i+1]) 
                elif obj[(2*i+1)-1] == "13":
                    scale = float(obj[2*i+1])
                elif obj[(2*i+1)-1] == "15":
                    groupParent = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "17":
                    editorLayer1 = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "20":
                    editorLayer2 = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "21":
                    copyOpacity = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "22":
                    colBlending = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "23":
                    targetGroup = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "24":
                    extra = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "25":
                    baseHSVEnabled = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "26":
                    detailHSVEnabled = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "28":
                    editorLayer3 = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "29":
                    base = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "30":
                    detail = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "31":
                    textValue = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "32":
                    touchTriggered = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "34":
                    coinID = int(obj[2*i+1])
                elif obj[(2*i+1)-1] == "36":
                    fadeIn = int(obj[2*i+1]) 
                elif obj[(2*i+1)-1] == "57":
                    groups = obj[2*i+1].split(".")
                elif obj[(2*i+1)-1] == "155":
                    lockPlayerX = int(obj[2*i+1]) 
                else:
                    other.append([obj[(2*i+1)-1], obj[2*i+1]])
        
        if (len(obj) > 3):     
            if asObject != None:
                if asObject:
                    level_objects.append({
                        "id": int(x),
                        "x": int(y),
                        "y": int(obj[5]),
                        "dir": float(dir)
                    })
            else:
                level_objects.append(GeometryDashObject(
                    x, y, obj[5], dir, 
                        flipX=flipX,
                        flipY=flipY,
                        yellowLayer=yellowLayer,
                        baseHSV=baseHSV,
                        detailHSV=detailHSV,
                        copyColorID=copyColorID,
                        zLayer=zLayer,
                        scale=scale,
                        groupParent=groupParent,
                        editorLayer1=editorLayer1,
                        editorLayer2=editorLayer2,
                        copyOpacity=copyOpacity,
                        colBlending=colBlending,
                        targetGroup=targetGroup,
                        extra=extra,
                        baseHSVEnabled=baseHSVEnabled,
                        detailHSVEnabled=detailHSVEnabled,
                        editorLayer3=editorLayer3,
                        base=base,
                        detail=detail,
                        textValue=textValue,
                        touchTriggered=touchTriggered,
                        coinID=coinID,
                        fadeIn=fadeIn,
                        groups=groups,
                        lockPlayerX=lockPlayerX,
                other=other, GJVAL_REGION=c<<4))
    c += 1
    
    return level_objects

class GJFormatterC:
    def __init__(self, d):
        for k, v in d.items():
            if isinstance(v, dict):
                v = GJFormatterC(v)
            if isinstance(v, list):
                v = [GJFormatterC(i) if isinstance(i, dict) else i for i in v]
            setattr(self, k, v)

objectID = GJFormatterC(json.load(open(Path(".")/"resources"/"json"/"id.json", "r")))

LocalLevels: list[GeometryDashLevel] = []
GJLocalLevelTitleS: list[str] = []
GJLocalLevelTitleLWS: list[str] = []

class __GJgetLevelsC:
    def __init__(self):
        pass
    def find(self, title: str, caseSensitive=True) -> GeometryDashLevel:
        return [l for l in LocalLevels if (l.title.lower() if not caseSensitive else l.title) == title][0] if title in (GJLocalLevelTitleLWS if not caseSensitive else GJLocalLevelTitleS) else print(f"[LOG] Level '{title}' not found.")

    def findall(self, title: str, caseSensitive=True) -> list[GeometryDashLevel]:
        return [l for l in LocalLevels if (l.title.lower() if not caseSensitive else l.title) == title] if title in (GJLocalLevelTitleLWS if not caseSensitive else GJLocalLevelTitleS) else print(f"[LOG] No instances of level '{title}' found.")
    
class __GJgetXMLC:
    def __init__(self):
        self.decoded = decrypt(os.path.expandvars(r"%localappdata%\GeometryDash\CCLocalLevels.dat"))
        self.xml = parse_xml(self.decoded)
    def prettifyXML(self):
        return minidom.parseString(ET.tostring(self.xml)).toprettyxml(indent="\t", encoding='utf-8').decode('utf-8')
    
def getLevels(): return __GJgetLevelsC()
def getXML(): return __GJgetXMLC()

def GJgetLevelDataF():
    decoded = decrypt(os.path.expandvars(r"%localappdata%\GeometryDash\CCLocalLevels.dat"))
    xml_code = parse_xml(decoded)
    level_title: list[str] = []
    level_author = []
    level_data = []
    level_description = []
    level_revision = []
    attach = -1
    for e in xml_code.iter():
        if e.tag == "k":
            if e.text == "kCEK":
                attach = 0 # header
            if e.text == "k2":
                attach = 1 # level title
            if e.text == "k5":
                attach = 2 # level author
            if e.text == "k4":
                attach = 3 # level data
            if e.text == "k3":
                attach = 4 # level description
            if e.text == "k46":
                attach = 5 # level revision
            continue
        if attach == 1:
            level_title.append(e.text)
            attach = -1
            if len(level_title) != len(level_description):
                level_description.append("")
            if len(level_title) != len(level_revision):
                level_revision.append("0")
        if attach == 2:
            level_author.append(e.text)
            attach = -1
        if attach == 3:
            level_data.append(gz.decompress(base64.urlsafe_b64decode(e.text.removesuffix("=").join("=="))).decode('utf-8'))
            attach = -1
        if attach == 4:
            level_description.append(base64.b64decode(e.text).decode('utf-8'))
            attach = -1
        if attach == 5:
            level_revision.append(e.text)
            attach = -1

    for i in range(len(level_title)-2):
        title = level_title[i]
        author = level_author[i]
        desc = level_description[i]
        revision = level_revision[i]
        data = level_data[i]
        LocalLevels.append(GeometryDashLevel(title, author, desc, base64.urlsafe_b64encode(gz.compress(data.encode('utf-8'))).decode('utf-8'), revision=revision))
        GJLocalLevelTitleS.append(title)
        GJLocalLevelTitleLWS.append(title.lower())
GJgetLevelDataF()

def main():
    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
    decoded = decrypt(os.path.expandvars(r"%localappdata%\GeometryDash\CCLocalLevels.dat"))
    xml_code = parse_xml(decoded)
    open(Path(".")/"resources"/"xml"/"decoded.xml", "w")
    open(Path(".")/"resources"/"xml"/"levels.xml", "w")
    open(Path(".")/"resources"/"xml"/"decoded.xml", "r+").write(ET.tostring(xml_code, encoding='unicode', method='xml'))

    file = open(Path(".")/"resources"/"xml"/"decoded.xml", "rb").read()
    print(f"[LOG] XML file size: {kbmb(len(file))}")

    print("\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-\n\nNo scripts running.")
    viewScripts = input("Do you want to view the scripts folder? [Y/n] >> ")
    print("\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
    if viewScripts.lower() != "y":
        pass
    else:
        os.startfile(Path(".")/"scripts")
    
if __name__ == "__main__":
    main()