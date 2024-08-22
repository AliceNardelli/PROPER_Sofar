#!/bin/bash

source alice_venv/bin/activate; python3 disable_auto_facial_expression.py  &
source alice_venv/bin/activate; python3 gaze_behavior.py & 
source alice_venv/bin/activate; python3 camera_input.py & 
source alice_venv/bin/activate; python3 sst.py & 
source alice_venv/bin/activate; python3 perception_server.py & 
source alice_env/bin/activate; python3 action_execution.py & 