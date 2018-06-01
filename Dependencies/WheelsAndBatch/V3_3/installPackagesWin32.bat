@echo off
echo Preparing to Install Packages
pause
py -3 -m pip install .\Dependencies\WheelsAndBatch\V3_3\Pillow\Pillow-4.3.0-cp33-cp33m-win32.whl --user
py -3 -m pip install .\Dependencies\WheelsAndBatch\V3_3\Pygame\pygame-1.9.2a0-cp33-none-win32.whl --user
py -3 -m pip install pynput --user
echo All Packages Hopefully Installed
pause
cls
exit