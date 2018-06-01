import sys
import os

ask = input("Would you like to uninstall the following packages:\nPillow\nPygame\n[y/n]")
if ask in ["y", "Y", "yes", "Yes", "YES"]:
    if sys.platform in ['linux','darwin']:
        
        ask = input("Would you like to uninstall Pillow [y/n]:")
        if ask in ["y", "Y", "yes", "Yes", "YES"]:
            os.system("python3 -m pip uninstall Pillow")
        
        ask = input("Would you like to uninstall pygame [y/n]:")
        if ask in ["y", "Y", "yes", "Yes", "YES"]:
            os.system("python3 -m pip uninstall pygame")

    else:
        os.startfile(".\\UninstallPackages.bat")

print("Finished")
