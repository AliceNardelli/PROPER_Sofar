# PROPER_Sofar Pepper perception architecture

## Morphcast on area24 conda env

> conda activate area42-swat-morphcast
> go into src/backend-python
> python play_backend.py


> conda activate area42-swat-morphcast
> go into src/sdk-javascript
> python -m http.server
> http://localhost:8000/play-sdk-v4.html


## python 3 environment
### PROPER
> roslaunch proper_lpg node_launch.launch

> rosrun proper_lpg ontology_interface.py


## OPENAI VENV
> python3 chat_playground.py


metric-FF url: https://fai.cs.uni-saarland.de/hoffmann/metric-ff.html

# openai-1.3.7 typing-extensions-4.8.0

command to list video devices:

# webcame

v4l2-ctl --list-devices

# bag

rosbag record -O /home/alice/ss2_t1.bag /webcam/image_raw/compressed /kinova_pose /experiment
