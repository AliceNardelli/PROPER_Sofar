#!/bin/bash
pkill -f input_simulation.py &
pkill -f execute_actions.py & 
pkill -f input_restart.py & 
pkill -f input_personality.py & 
pkill -f ontology_interface.py