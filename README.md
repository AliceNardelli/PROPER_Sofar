# PROPER_Sofar Pepper perception architecture


## python 3 environment

start the ROS perception nodes
> python3 prova_keyboard.py #uso webcam
> python3 FaceDetection2.py #robot camera
>python3 Tactile_Interface_ROS.py

run the perception interface
>rosrun proper_lpg perception_interface.py

start the fsm and ontology iterface
> rosrun proper_lpg ontology_interface.py



## python 2 environment
inside the virtualenv 
>export PYTHONPATH=${PYTHONPATH}:/home/alice/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages/
>python tactile_interface.py
>python Pepper_Image_acquisition.py #if use robot camera