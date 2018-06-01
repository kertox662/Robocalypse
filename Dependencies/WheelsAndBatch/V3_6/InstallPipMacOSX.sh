#!/bin/bash
source ~/.bash_profile
python3 Dependencies/WheelsAndBatch/get-pip.py --user
python3 -m pip install Dependencies/WheelsAndBatch/V3_6/Pillow/Pillow-5.0.0-cp36-cp36m-macosx_10_6_intel.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl --user
python3 -m pip install Dependencies/WheelsAndBatch/V3_6/Pygame/pygame-1.9.3-cp36-cp36m-macosx_10_9_intel.whl --user
python3 -m pip install pynput --user
exit 0