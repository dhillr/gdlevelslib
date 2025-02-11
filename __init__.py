# -----------------------------===========
#
# >>> Package init file <<< <  <   <    <
#
# [i] This file is good enough? the way it is,
# [i] so please don't edit it.
#
# ===========-----------------------------
import sys
from pathlib import Path
__name__ = "GDLevelsLib"
__version__ = "1.0.0b"
if sys.version_info < (3, 10):
    raise ImportError("Python 3.10 or later is required for GDLevelsLib to work.")
__doc__ = open(Path(".")/"README.md", "r", encoding="utf-8").read()
open(Path(".")/"resources"/"xml"/"decoded.xml", "w").close()
open(Path(".")/"resources"/"xml"/"levels.xml", "w").close()