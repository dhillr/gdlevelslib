import gzip as gz
import base64
import xml.etree.ElementTree as ET
import os
import math
from typing import Optional
from time import *
from xml.dom import minidom
from pathlib import Path

print("##########")
print("## #### ##  GDLevelsLib [ALPHA]")
print("##########  by poyo52596kirby")
print("#        #  Version 1.0.4a")
print("##########\n")

class GeometryDashObject:
    def __init__(self, objectID, x, y, dir, other, textValue=None):
        self.objectID = objectID
        self.x = x
        self.y = y
        self.dir = dir
        self.other = other if other else None
        self.textValue = textValue if textValue else None

    def generate_string(self) -> str:
        base_string = f"1,{self.objectID},2,{self.x},3,{self.y},6,{self.dir},"
        if self.other:
            if self.other["flipX"]:
                base_string += f"4,{self.other['flipX']},"

            if self.other["flipY"]:
                base_string += f"5,{self.other['flipY']}," 

            if self.other["yellowLayer"]:
                base_string += f"7,{self.other['yellowLayer']},"

            if self.other["baseHSV"]:
                base_string += f"8,{self.other['baseHSV']},"

            if self.other["detailHSV"]:    
                base_string += f"9,{self.other['detailHSV']},"

            if self.other["copyColorID"]:
                base_string += f"10,{self.other['copyColorID']},"

            if self.other["zLayer"]:
                base_string += f"11,{self.other['zLayer']},"

            if self.textValue:
                base_string += f"31,{self.textValue},"

            if self.other["fadeIn"]:
                base_string += f"36,{self.other['fadeIn']},"

            if self.other["lockPlayerX"]:
                base_string += f"155,{self.other['lockPlayerX']},"

        return base_string.removesuffix(",") + ";"
    
    def snap_to_grid(self, snap=30):
        self.x = math.floor(self.x/snap)*snap+15
        self.y = math.floor(self.y/snap)*snap+15
        return self

class GeometryDashLevel:
    def __init__(self, title, author, description, revision, data):
        self.title = title
        self.author = author
        self.description = description
        self.revision = revision
        self.data = data if data else ""
        self.objects = ""
        self.add_object(GeometryDashObject(0, 0, 0, 0, None)) # dummy object

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
    
    def generate_string(self, xml) -> str:
        self.data = base64.urlsafe_b64encode(gz.compress(self.objects.encode('utf-8'))).decode('utf-8')
        key_prefix = f"k_{str(self.get_max_number(xml) + 1)}"
        use_desc = False
        if use_desc:
            return f"<root><k>{key_prefix}</k><d><k>kCEK</k><i>4</i><k>k2</k><s>{self.title}</s><k>k4</k><s>{self.data}</s><k>k3</k><s>{base64.b64encode(self.description.encode('utf-8')).decode('utf-8')}</s><k>k46</k><s>{self.revision}</s><k>k5</k><s>{self.author}</s><k>k13</k><t /><k>k21</k><i>2</i><k>k16</k><i>1</i><k>k80</k><i>0</i><k>k50</k><i>35</i><k>k47</k><t /><k>kI1</k><r>0</r><k>kI2</k><r>36</r><k>kI3</k><r>1</r></d></root>"
        else:
            return f"<root><k>{key_prefix}</k><d><k>kCEK</k><i>4</i><k>k2</k><s>{self.title}</s><k>k4</k><s>{self.data}</s><k>k46</k><s>{self.revision}</s><k>k5</k><s>{self.author}</s><k>k13</k><t /><k>k21</k><i>2</i><k>k16</k><i>1</i><k>k80</k><i>0</i><k>k50</k><i>35</i><k>k47</k><t /><k>kI1</k><r>0</r><k>kI2</k><r>36</r><k>kI3</k><r>1</r></d></root>"

    def add_object(self, obj: GeometryDashObject) -> None:
        self.objects += obj.generate_string()

def kbmb(size) -> str:
    if size < 1048576:
        return str(0.01*round(100*(size/1024))) + " KB"
    elif size < 1073741824:
        return str(0.01*round(100*(size/1048576))) + " MB"

def xor_bytes(byteData) -> bytes:
    return bytes(b ^ 11 for b in byteData)

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

def decode_level_string(data: str):
    level_objects = []
    level_objects_str = data.split(";")

    for l in level_objects_str:
        obj = l.split(",")
        if (len(obj) < 6):
            continue
        x = obj[1]
        y = obj[3]
        flipX = 0 # property 4
        flipY = 0 # property 5
        dir = 0 # property 6
        yellowLayer = 0 # property 7
        baseHSV = 0 # property 8
        detailHSV = 0 # property 9
        copyColorID = 0 # property 10
        zLayer = 0 # property 11
        scale = 0 # property 13
        groupParent = 0 # property 15
        editorLayer1 = 0 # property 17
        editorLayer2 = 0 # property 20
        copyOpacity = 0 # property 21
        colBlending = 0 # property 22
        targetGroup = 0 # property 23
        extra = 0 # property 24
        baseHSVEnabled = 0 # property 25
        detailHSVEnabled = 0 # property 26
        editorLayer3 = 0 # property 28
        base = 0 # property 29
        detail = 0 # property 30
        textValue = 0 # property 31
        touchTriggered = 0 # property 32
        coinID = 0 # property 34
        fadeIn = 0 # property 36
        lockPlayerX = 0 # property 155

        for i in range(int(round(len(obj)/2))):
            if i > 3:
                if obj[(2*i+1)-1] == "6":
                    dir = int(obj[2*i+1])

                if obj[(2*i+1)-1] == "7":
                    yellowLayer = int(obj[2*i+1])

                if obj[(2*i+1)-1] == "8":
                    baseHSV = int(obj[2*i+1])

                if obj[(2*i+1)-1] == "9":
                    detailHSV = int(obj[2*i+1])

                if obj[(2*i+1)-1] == "10":
                    copyColorID = float(obj[2*i+1])

                if obj[(2*i+1)-1] == "11":
                    zLayer = int(obj[2*i+1]) 

                if obj[(2*i+1)-1] == "13":
                    scale = float(obj[2*i+1])

                if obj[(2*i+1)-1] == "15":
                    groupParent = int(obj[2*i+1])

                if obj[(2*i+1)-1] == "17":
                    editorLayer1 = int(obj[2*i+1])
                
                if obj[(2*i+1)-1] == "20":
                    editorLayer2 = int(obj[2*i+1])
                
                if obj[(2*i+1)-1] == "21":
                    copyOpacity = int(obj[2*i+1])

                if obj[(2*i+1)-1] == "22":
                    colBlending = int(obj[2*i+1])

                if obj[(2*i+1)-1] == "23":
                    targetGroup = int(obj[2*i+1])

                if obj[(2*i+1)-1] == "24":
                    extra = int(obj[2*i+1])

                if obj[(2*i+1)-1] == "25":
                    baseHSVEnabled = int(obj[2*i+1])

                if obj[(2*i+1)-1] == "26":
                    detailHSVEnabled = int(obj[2*i+1])

                if obj[(2*i+1)-1] == "28":
                    editorLayer3 = int(obj[2*i+1])

                if obj[(2*i+1)-1] == "29":
                    base = int(obj[2*i+1])

                if obj[(2*i+1)-1] == "30":
                    detail = int(obj[2*i+1])

                if obj[(2*i+1)-1] == "31":
                    textValue = int(obj[2*i+1])

                if obj[(2*i+1)-1] == "32":
                    touchTriggered = int(obj[2*i+1])

                if obj[(2*i+1)-1] == "34":
                    coinID = int(obj[2*i+1])

                if obj[(2*i+1)-1] == "36":
                    fadeIn = int(obj[2*i+1]) 

                if obj[(2*i+1)-1] == "155":
                    lockPlayerX = int(obj[2*i+1]) 

        if (len(obj) > 3):
            level_objects.append(GeometryDashObject(x, y, obj[5], dir, {
                flipX: flipX, 
                flipY: flipY, 
                yellowLayer: yellowLayer,
                baseHSV: baseHSV,
                detailHSV: detailHSV,
                copyColorID: copyColorID,
                zLayer: zLayer,
                scale: scale,
                groupParent: groupParent,
                editorLayer1: editorLayer1,
                editorLayer2: editorLayer2,
                copyOpacity: copyOpacity,
                colBlending: colBlending,
                targetGroup: targetGroup,
                extra: extra,
                baseHSVEnabled: baseHSVEnabled,
                detailHSVEnabled: detailHSVEnabled,
                editorLayer3: editorLayer3,
                base: base,
                detail: detail,
                textValue: textValue,
                touchTriggered: touchTriggered,
                coinID: coinID,
                fadeIn: fadeIn,
                lockPlayerX: lockPlayerX
            }))
    return level_objects

LocalLevels = []

class getLevels:
    def __init__(self):
        pass
    def find(self, title):
        return [l for l in LocalLevels if l.title == title][0]
    def findall(self, title):
        return [l for l in LocalLevels if l.title == title]
    
class getXML:
    def __init__(self):
        self.decoded = decrypt(os.path.expandvars(r"%localappdata%\GeometryDash\CCLocalLevels.dat"))
        self.xml = parse_xml(self.decoded)
    def prettifyXML(self):
        return minidom.parseString(ET.tostring(self.xml)).toprettyxml(indent="\t", encoding='utf-8').decode('utf-8')

def get_levels():
    decoded = decrypt(os.path.expandvars(r"%localappdata%\GeometryDash\CCLocalLevels.dat"))
    xml_code = parse_xml(decoded)
    level_title = []
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
        LocalLevels.append(GeometryDashLevel(title, author, desc, revision, data))
get_levels()

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