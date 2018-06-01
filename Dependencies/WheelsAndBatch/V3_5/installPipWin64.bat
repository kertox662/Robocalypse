@echo off
echo Preparing To Install Pip
py -3 .\Dependencies\WheelsAndBatch\get-pip.py --user
echo Continue to Package Installation
pause
start Dependencies\WheelsAndBatch\V3_5\installPackagesWin64
cls
exit