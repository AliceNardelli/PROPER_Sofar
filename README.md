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

run the apllication for sentence generation
go inside the Flask folder and run
>python3 openai_interface.py  

**note1**: domain file is pepper_domain3.lpg

**note2**: change the absolute path everywhere

**note3**: The weights of personality generator are needed

**note4**: The aruco used are 13 for the production room and 24 for the assemby one. Aurco size is 0.2m (if you change the aruco you need to change also the size inside the code)

## python 2 environment

start the three execution blocks

>python action_dispatcher_server.py


#pepper_domain3 con agreeable
#peper_domain4 senza agreeable

## TO DO LIST:
- test openai interface and speak, evaluate if openai work well and if it takes not too much time **5/06**
- see if it is possible to tablet ip 198.18.0.1 via ssh and coping image inside **5/06**
- include movements, consider that when the robot grasp an object movement cannot be generated. before add them, the remove when necessary **6/06**
- random move, show hand