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
    parser.add_argument("--ip", type=str, default="192.168.178.92",
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
    
    # U
    actions=["s1"]
    params=[0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0,0, 0, 0, 0]
    personality="Unscrupolous"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    s.traits="u"
    ss(data)
    actions=["show_random_movement"]
    params=[0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0,0, 0, 0, 0]
    personality="Unscrupolous"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    s.traits="u"
    gg(data)
    s.tablet("uc.png")
    s.tablet("u.png")
    raw_input("Press Enter to continue...")
    # E
    actions=["s2"]
    params=[1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1,0, 0, 0, 0]
    personality="Extrovert"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    s.traits="e"
    ss(data)
    actions=["show_excitement"]
    params=[1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1,0, 0, 0, 0]
    personality="Extrovert"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    gg(data)
    s.tablet("ie.png")
    s.tablet("e.png")
    raw_input("Press Enter to continue...")
    # C
    actions=["s3"]
    params=[1., 0., 0., 1., 0., 0., 0., 1., 0., 0., 0., 1., 0., 1., 0., 1., 0., 0., 0., 0., 0.]
    personality="Conscientous"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    s.traits="c"
    ss(data)
    s.tablet("uc.png")
    s.tablet("c.png")
    raw_input("Press Enter to continue...")

    #D

    actions=["s4"]
    params=[1., 0., 0., 1., 1., 0., 1., 1., 0., 0., 1., 0., 0., 1., 0., 1., 1.,0., 0., 0., 0.]
    personality="Disagreeable"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    s.traits="d"
    ss(data)
    actions=["show_disgust"]
    params=[1., 0., 0., 1., 1., 0., 1., 1., 0., 0., 1., 0., 0., 1., 0., 1., 1.,0., 0., 0., 0.]
    personality="Disagreeable"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    
    gg(data)
    s.tablet("da.png")
    s.tablet("d.png")
    raw_input("Press Enter to continue...")

    #A

    actions=["s5"]
    params=[0., 1., 0., 1., 1., 0., 1., 0., 1., 0., 0., 1., 1., 1., 0., 0., 1., 0., 0., 0., 0.]
    personality="Agreeable"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    s.traits="a"
    ss(data)
    s.tablet("da.png")
    s.tablet("a.png")
    raw_input("Press Enter to continue...")


    #I
    actions=["s6"]
    params=[1., 0., 0., 1., 0., 0., 1., 0., 0., 1., 1., 0., 0., 0., 1., 0., 1., 0., 0., 0., 0.]
    personality="Introvert"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    s.traits="i"
    ss(data)
    actions=["show_detachment"]
    params=[1., 0., 0., 1., 0., 0., 1., 0., 0., 1., 1., 0., 0., 0., 1., 0., 1., 0., 0., 0., 0.]
    personality="Introvert"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    s.traits="i"
    gg(data)
    s.tablet("ie.png")
    s.tablet("i.png")
    raw_input("Press Enter to continue...")
    #U
    actions=["s7"]
    params=[0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0,0, 0, 0, 0]
    personality="Unscrupolous"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    s.traits="u"
    ss(data)
    actions=["show_random_movement"]
    params=[0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0,0, 0, 0, 0]
    personality="Unscrupolous"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    s.traits="u"
    gg(data)
    s.tablet("uc.png")
    s.tablet("u.png")
    raw_input("Press Enter to continue...")
    #c
    actions=["s8"]
    params=[1., 0., 0., 1., 0., 0., 0., 1., 0., 0., 0., 1., 0., 1., 0., 1., 0., 0., 0., 0., 0.]
    personality="Conscientous"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    s.traits="c"
    ss(data)
    s.tablet("uc.png")
    s.tablet("c.png")
    raw_input("Press Enter to continue...")

    #A

    actions=["s9"]
    params=[0., 1., 0., 1., 1., 0., 1., 0., 1., 0., 0., 1., 1., 1., 0., 0., 1., 0., 0., 0., 0.]
    personality="Agreeable"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    s.traits="a"
    ss(data)
    s.tablet("da.png")
    s.tablet("a.png")
    raw_input("Press Enter to continue...")
    #I
    actions=["s10"]
    params=[1., 0., 0., 1., 0., 0., 1., 0., 0., 1., 1., 0., 0., 0., 1., 0., 1., 0., 0., 0., 0.]
    personality="Introvert"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    s.traits="i"
    ss(data)
    actions=["show_detachment"]
    params=[1., 0., 0., 1., 0., 0., 1., 0., 0., 1., 1., 0., 0., 0., 1., 0., 1., 0., 0., 0., 0.]
    personality="Introvert"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    s.traits="i"
    gg(data)
    s.tablet("ie.png")
    s.tablet("i.png")
    raw_input("Press Enter to continue...")
    #D

    actions=["s11"]
    params=[1., 0., 0., 1., 1., 0., 1., 1., 0., 0., 1., 0., 0., 1., 0., 1., 1.,0., 0., 0., 0.]
    personality="Disagreeable"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    s.traits="d"
    ss(data)
    actions=["show_disgust"]
    params=[1., 0., 0., 1., 1., 0., 1., 1., 0., 0., 1., 0., 0., 1., 0., 1., 1.,0., 0., 0., 0.]
    personality="Disagreeable"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    
    gg(data)
    s.tablet("da.png")
    s.tablet("d.png")
    raw_input("Press Enter to continue...")

    # E
    actions=["s12"]
    params=[1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1,0, 0, 0, 0]
    personality="Extrovert"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    s.traits="e"
    ss(data)
    actions=["show_excitement"]
    params=[1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1,0, 0, 0, 0]
    personality="Extrovert"
    mmap =get_map(params)
    data={
        "action":actions[0],
        "params":mmap,
        "personality":personality
    }
    gg(data)
    s.tablet("ie.png")
    s.tablet("e.png")
    raw_input("Press Enter to continue...")



