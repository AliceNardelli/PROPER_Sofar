#! /usr/bin/env python3
# coding=utf-8
from flask import Flask, request
import os
import shutil
import subprocess
import json
import time


def get_domain():
    planner_path = "/home/alice/downward/"
    os.chdir (planner_path)
    #shutil.copyfile(mydir+'/domain.pddl', planner_path+"/domain.pddl")
    #shutil.copyfile(mydir+'/problem.pddl', planner_path+"/problem.pddl")
    print ('./fast-downward.py domain.pddl problem.pddl --evaluator "h=ff()" --search "lazy_greedy([h], preferred=[h])"')
    command =  './fast-downward.py domain.pddl problem.pddl --evaluator "h=ff()" --search "eager_wastar([h], preferred=[h], reopen_closed=false)"'
    #run the planner
    fd_process = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (out, err) = fd_process.communicate()
    fd_exit = fd_process.returncode
    if os.path.isfile(planner_path+'/sas_plan'):
        print ('il piano ce')
        output_path=planner_path+'/sas_plan'
        with open(output_path, "r") as plan_file:
            raw_plan = plan_file.readlines()
        my_plan= str(raw_plan)
        print(raw_plan)
    else:
        print("Plan not found")
    
        
    
    
if __name__=='__main__':
    get_domain()
