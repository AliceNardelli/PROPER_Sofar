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

> roslaunch proper_lpg parameter_launch.launch
or
> roslaunch proper_lpg node_launch.launch
or
> rosrun pp_task edge_detection.py
> rosrun pp_task game_player.py
> rosrun proper_lpg perception_interface.py
> rosrun proper_lpg action_dispatcher.py
> rosrun proper_lpg personality_generator.py

> roslaunch kinova_bringup kinova_robot.launch kinova_robotType:=j2s7s300
> roslaunch j2s7s300_moveit_config j2s7s300_demo.launch
> rosrun pp_task kinova_as /joint_states:=/j2s7s300_driver/out/joint_state
> rosrun proper_lpg ontology_interface.py






## Cairlib environment
> python3 audio_recorder_multiparty.py

metric-FF url: https://fai.cs.uni-saarland.de/hoffmann/metric-ff.html

# openai-1.3.7 typing-extensions-4.8.0