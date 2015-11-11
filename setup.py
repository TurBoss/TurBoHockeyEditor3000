import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "TurBo Hockey Editor 3000",
        version = "0.1",
        author="TurBoss",
        description = "Editor for the neketsu hockey nes game",
        options = {"build_exe": build_exe_options},
        executables = [Executable("App1.pyw", base=base, targetName="TurBoHockeyEditor3000.exe")])
