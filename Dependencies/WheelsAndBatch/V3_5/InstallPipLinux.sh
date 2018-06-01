#!/bin/bash
source ~/.bash_profile
python3 Dependencies/WheelsAndBatch/get-pip.py --user
python3 -m pip install Dependencies/WheelsAndBatch/V3_5/Pillow/Pillow-5.0.0-cp35-cp35m-manylinux1_x86_64.whl --user
python3 -m pip install Dependencies/WheelsAndBatch/V3_5/Pygame/pygame-1.9.3-cp35-cp35m-manylinux1_x86_64.whl --user
python3 -m pip install pynput --user
exit 0
