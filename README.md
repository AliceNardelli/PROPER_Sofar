# PROPER_Sofar Pepper architecture


## python 3 environment

start the action dispatcher
> rosrun rosbot_actions action_dispatcher.py

start the personality_generator
> rosrun rosbot_actions personality_generator.py

start the fsm and ontology iterface
> rosrun proper_lpg ontology_interface.py

**note1**: domain file is pepper_domain3.lpg

**note2**: change the absolute path everywhere

**note3**: The weights of personality generator are needed

## python 2 environment

start the three execution blocks

>python navigation_server.py
>python speak_server.py
>python gesture_server.py



