import cx_Freeze
import sys

base  = None
if sys.platform == "win32":
    base = "Win32GUI"


executables = [cx_Freeze.Executable("EngineMain.py", base = base)]

cx_Freeze.setup(
    name = "Test1",
    options = {
        "build_exe": {
            "packages":["tkinter"],
            # "includes":["Screen.py","MainScene.py", "SettingsScene.py", "Scene.py"],
            "include_files":["data/configs.json"]
        }
    },
    version = "0.01",
    description = "Simple test",
    executables = executables
)

