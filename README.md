# PROPER_Sofar Pepper architecture


## python 3 environment

start the action dispatcher
> rosrun rosbot_actions action_dispatcher.py

start the personality_generator
> rosrun rosbot_actions personality_generator.py

start the fsm and ontology iterface
> rosrun proper_lpg ontology_interface.py

run the apllication for aruco detection
go inside the AruCo-Markers folder and run
>python3 single_pose_estimation.py  

**note1**: domain file is pepper_domain3.lpg

**note2**: change the absolute path everywhere

**note3**: The weights of personality generator are needed

**note4**: The aruco used are 13 for the production room and 24 for the assemby one. Aurco size is 0.2m (if you change the aruco you need to change also the size inside the code)

## python 2 environment

start the three execution blocks

>python action_dispatcher_server.py



