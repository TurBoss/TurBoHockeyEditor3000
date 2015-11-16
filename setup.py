import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
						"packages": ["os"],
						"excludes": ["tkinter"],
						"include_files": ["icon.ico"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

if sys.platform == "win32":
    base = "Win32GUI"

target = Executable(	script="App1.pyw",
						base=base,
						targetName="TurBoHockeyEditor3000.exe",
						compress=False,
						copyDependentFiles=True,
						appendScriptToExe=True,
						appendScriptToLibrary=False,
						icon="icon.ico",
						shortcutName="TurBo Hockey Editor 3000",
						shortcutDir="DesktopFolder",
)

setup(	name = "TurBo Hockey Editor 3000",
		version = "0.1",
		author="TurBoss",
		description = "Editor for the neketsu hockey nes game",
		options = {"build_exe": build_exe_options},
		executables = [target]
)
