import os
import sys
import time
import platform
import subprocess

def checkDependencies():
    #PIL, PyGame
    results = []

    pyVer = sys.version_info[0] #Python Major version (Python 2 vs. Python 3)
    pyVerMinor = sys.version_info[1] #Python Minor version (Python 3.2 vs. Python 3.3)
    is_64Bit = platform.machine()[-2:] == '64' #Outputs true if it is 64 bit os
    
    if pyVer < 3:
        print("Please use Python 3.3 or Higher on Windows\nPlease use Python 3.4 or Higher on Linux\nPlease use Python 3.6 or Higher on OSX/Mac")
        return

    try: #Attempts at importing, if not successful, will ask for installation permission
        import PIL
    except ImportError:
        results.append('PIL')

    try:
        import pygame
    except ImportError:
        results.append("PyGame")
    
    try:
        import pynput
    except ImportError:
        results.append("Pynput")

    if len(results) > 0: #Checks if any of the imports failed
        print("Found some dependencies missing.")
        for i in results:
            print("-{}".format(i))
        ask = input("Install missing dependencies? [y/n]")
        if ask in ["y", "Y", "yes", "Yes", "YES"]:
            print("Preparing to install dependencies")
            if sys.platform == 'linux': #Checks python versions and installs wheel files accordingly
                if pyVerMinor == 4:
                    print("Installing on Linux for Python 3.4")
                    p = subprocess.Popen(["Dependencies/WheelsAndBatch/V3_4/InstallPipLinux.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                elif pyVerMinor == 5:
                    print("Installing on Linux for Python 3.5")
                    p = subprocess.Popen(["Dependencies/WheelsAndBatch/V3_5/InstallPipLinux.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                elif pyVerMinor >= 6:
                    print("Installing on Linux for Python 3.6")
                    p = subprocess.Popen(["Dependencies/WheelsAndBatch/V3_6/InstallPipLinux.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    print("An error has occured")
                    return

            elif sys.platform == 'darwin':#Checks python versions and installs wheel files accordingly
                print("Installing on Mac OS for Python 3.6")
                p = subprocess.Popen(["Dependencies/WheelsAndBatch/V3_6/InstallPipMacOSX.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(p.communicate()[0].decode())

            elif sys.platform == 'win32':
                if not is_64Bit:
                    if pyVerMinor == 3:
                        print("Installing on Windows for Python 3.3 32-bit")
                        os.startfile(".\Dependencies\WheelsAndBatch\V3_3\installPipWin32.bat")
                    elif pyVerMinor == 4:
                        print("Installing on Windows for Python 3.4 32-bit")
                        os.startfile(".\Dependencies\WheelsAndBatch\V3_4\installPipWin32.bat")
                    elif pyVerMinor == 5:
                        print("Installing on Windows for Python 3.5 32-bit")
                        os.startfile(".\Dependencies\WheelsAndBatch\V3_5\installPipWin32.bat")
                    elif pyVerMinor >= 6:
                        print("Installing on Windows for Python 3.6 32-bit")
                        os.startfile(".\Dependencies\WheelsAndBatch\V3_6\installPipWin32.bat")
                    else:
                        print("An error has occured")
                        return

                else:
                    if pyVerMinor == 3:
                        print("Installing on Windows for Python 3.3 64-bit")
                        os.startfile(".\Dependencies\WheelsAndBatch\V3_3\installPipWin64.bat")
                    elif pyVerMinor == 4:
                        print("Installing on Windows for Python 3.4 64-bit")
                        os.startfile(".\Dependencies\WheelsAndBatch\V3_4\installPipWin64.bat")
                    elif pyVerMinor == 5:
                        print("Installing on Windows for Python 3.5 64-bit")
                        os.startfile(".\Dependencies\WheelsAndBatch\V3_5\installPipWin64.bat")
                    elif pyVerMinor >= 6:
                        print("Installing on Windows for Python 3.6 64-bit")
                        os.startfile(".\Dependencies\WheelsAndBatch\V3_6\installPipWin64.bat")
                    else:
                        print("An error has occured")
                        return
            else:
                print("An error has occurred or using an unsupported OS")
                return

            

            print("Hopefully installed all dependecies")
        else: #If answers n in [y\n]
            print("Exiting out.\nHave a nice day!")
            time.sleep(1)
    else: #If not imports fail
        print("Yay, no dependencies are missing!")

if __name__ == '__main__':
    pass
    # checkDependencies()
