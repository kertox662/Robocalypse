@echo off
echo Preparing to Install Packages
pause
py -3 -m pip install .\Dependencies\WheelsAndBatch\V3_6\Pillow\Pillow-5.0.0-cp36-cp36m-win32.whl --user
py -3 -m pip install .\Dependencies\WheelsAndBatch\V3_6\Pygame\pygame-1.9.3-cp36-cp36m-win32.whl --user
py -3 -m pip install pynput --user
echo All Packages Hopefully Installed
pause
cls
exit