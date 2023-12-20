#!/bin/bash

cd ; cd $1/PROPER_Sofar/proper_reasoning/scripts; python3 input_simulation.py  &
cd ; cd $1/PROPER_Sofar/proper_reasoning/scripts; python3 execute_actions.py & 
cd ; cd $1/PROPER_Sofar/proper_reasoning/scripts; python3 input_restart.py & 
cd ; cd $1/PROPER_Sofar/proper_reasoning/scripts; python3 input_personality.py & 
cd ; cd $1/PROPER_Sofar/proper_reasoning/scripts; python3 ontology_interface.py &

