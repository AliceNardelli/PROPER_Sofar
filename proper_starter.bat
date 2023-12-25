@echo off


set scripts_path=C:\Users\alice\OneDrive\Desktop\PROPER_Sofar\proper_reasoning\scripts

start wt -p "Command Prompt"  cmd /k "conda activate area42-swat-dh && cd %scripts_path% && python -m input_personality;" cmd /k "conda activate area42-swat-dh && cd %scripts_path% && python -m input_simulation;" cmd /k "conda activate area42-swat-dh && cd %scripts_path% && python -m input_restart;" cmd /k "conda activate area42-swat-dh && cd %scripts_path% && python -m execute_actions;" cmd /k "conda activate area42-swat-dh && cd %scripts_path% && python -m ontology_interface;"



