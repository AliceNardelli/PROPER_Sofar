# -*- coding: utf-8 -*-
from class_navigation import *
from class_gesture import *
from class_speak import *
import qi
from get_parameters import * 
def mm(data):
    global m
    m.move(data["action"],data["params"])

def gg(data):
    global g
    g.gesture(data["action"],data["params"])
    
def ss(data):
    global s
    s.speak(data["action"],data["personality"],data["params"])
   

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.137",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))        
        #app = qi.Application(["TabletModule", "--qi-url=" + "tcp://" + args.ip + ":" + str(args.port)])
        #app.start()
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    m=Move(session)
    g=Gesture(session)
    s=Speak(session)
    """
    # ED
    actions=["speak_about_production_room","show_excitement"]
    params=[1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]
    personality="Extrovert"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    ss(data)
    data={
        "action":actions[1],
        "params":mmap
    }
    gg(data)
    """
    """
    # IA usare ed_v
    actions=["speak_about_assembly_room","go_not_crowded_area"]
    params= [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
    personality="Introvert"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    ss(data)
    params= [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0]
    mmap =get_map(params)
    data={
        "action":actions[1],
        "params":mmap
    }
    mm(data)
    """
    """
    #EC
    actions=["ask_pick_the_block_voice","say_to_not_distract"]
    params= [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    personality="Extrovert"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    ss(data)
    data={
        "action":actions[1],
        "params":mmap,
        "personality":personality
    }
    ss(data)
    """
    """
    #IU
    actions=["go_in_a_random_position","ask_pick_the_block_tablet","say_no_matter_about_the_task"]
    params= [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0]
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap
    }
    mm(data)
    params=[0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    personality="Unscrupolous"
    mmap =get_map(params)
    data={
        "action":actions[1],
        "params":mmap,
        "personality":personality
    }
    ss(data)
    data={
        "action":actions[2],
        "params":mmap,
        "personality":personality
    }
    ss(data)
    """
    """
    #AC
    actions=["ask_assembly_block_tablet","ask_if_human_need_help"]
    params= [0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
    personality="Agreeable"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    ss(data)
    data={
        "action":actions[1],
        "params":mmap,
        "personality":personality
    }
    ss(data)
    """
    """
    #DU
    #mettere colore 4
    actions=["ask_assembly_block_voice","say_to_work_more_fast"]
    params= [1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]

    personality="Disgreeable"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    ss(data)
    data={
        "action":actions[1],
        "params":mmap,
        "personality":personality
    }
    ss(data)
    """