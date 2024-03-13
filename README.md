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
> roslaunch proper_lpg parameter_launch.launch
or
> roslaunch proper_lpg node_launch.launch
or
> rosrun pp_task edge_detection3x3.py
> rosrun pp_task game_player3x3.py
> rosrun proper_lpg perception_interface.py
> rosrun proper_lpg action_dispatcher.py
> rosrun proper_lpg personality_generator.py

> rosrun proper_lpg ontology_interface.py

### MOVEIT
> rosrun pp_task kinova_as 


## OPENAI VENV
> python3 chat_playground.py




## Cairlib environment
> python3 audio_recorder_multiparty.py

metric-FF url: https://fai.cs.uni-saarland.de/hoffmann/metric-ff.html

# openai-1.3.7 typing-extensions-4.8.0