#!/bin/bash

xterm -e "cd; source test_env/venv/bin/activate; export PYTHONPATH=${PYTHONPATH}:/home/alice/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages/; cd /home/alice/catkin_ws/src/PROPER_Sofar/Pepper_motion; python tactile_interface.py"  & 
xterm -e "cd; source test_env/venv/bin/activate; export PYTHONPATH=${PYTHONPATH}:/home/alice/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages/; cd /home/alice/catkin_ws/src/PROPER_Sofar/Pepper_motion; python action_dispatcher_server.py"  & 