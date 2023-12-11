#!/bin/bash

xterm -e "cd ; cd $1/PROPER_Sofar/proper_reasoning/scripts; python3 input_simulation.py"  & 
xterm -e "cd ; cd $1/PROPER_Sofar/proper_reasoning/scripts; python3 execute_actions.py" & 
xterm -e "cd ; cd $1/PROPER_Sofar/proper_reasoning/scripts; python3 input_restart.py" & 
xterm -e "cd ; cd $1/PROPER_Sofar/proper_reasoning/scripts; python3 input_personality.py" & 
xterm -e "cd ; cd $1/PROPER_Sofar/proper_reasoning/scripts; python3 ontology_interface.py" & 
