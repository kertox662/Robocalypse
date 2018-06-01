import os

results = [True,True, True]
pyVerMinor = sys.version_info[1]

try:
    import PIL
except ImportError:
    results[0] = False

try:
    import pygame
except ImportError:
    results[1] = False

try:
    import pynput
except ImportError:
    results[2] = False

if False in results:
    if pyVerMinor == 3:
        os.startfile(".\WheelsAndBatch\V3_3\installPackagesWin32.bat")
    elif pyVerMinor == 4:
        os.startfile(".\WheelsAndBatch\V3_4\installPackagesWin32.bat")
    elif pyVerMinor == 5:
        os.startfile(".\WheelsAndBatch\V3_5\installPackagesWin32.bat")
    elif pyVerMinor >= 6:
        os.startfile(".\WheelsAndBatch\V3_6\installPackagesWin32.bat")
    else:
        print("An error has occured")