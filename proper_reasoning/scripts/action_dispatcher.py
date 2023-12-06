#!/usr/bin/env python
# -*- coding: utf-8 -*-

from get_parameters import *
from personality_generator import *


def dispatch_action(action, personality):
        params=generate_params(personality, action)
        mmap =get_map(params)
        print("otput********************")
        print(mmap,action,personality)
        print("********************")
        return True, mmap, action, personality
        
    





        
