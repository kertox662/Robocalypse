#!/bin/bash
source ~/.bash_profile
python3 Dependencies/WheelsAndBatch/get-pip.py --user
python3 -m pip install Dependencies/WheelsAndBatch/V3_4/Pillow/Pillow-5.0.0-cp34-cp34m-manylinux1_x86_64.whl --user
python3 -m pip install Dependencies/WheelsAndBatch/V3_4/Pygame/pygame-1.9.3-cp34-cp34m-manylinux1_x86_64.whl --user
python3 -m pip install pynput --user

exit 0
