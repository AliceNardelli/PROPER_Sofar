import rospy
from pp_task.msg import Board
from pp_task.srv import Game, GameResponse
import time


def callback(data):
    global actual_board_state, new_data
    actual_board_state=data
    new_data=True

def set_goal_configuration(conf):
   
    if conf == 1:
        final_board_state.area1="R"
        final_board_state.area2="B"
        final_board_state.area3="R"
        final_board_state.area4="B"
        final_board_state.area5="R"
        final_board_state.area6="B"
        final_board_state.area7="R"
        final_board_state.area8="B"
        final_board_state.area9="R"

    else:
        final_board_state.area1="B"
        final_board_state.area2="R"
        final_board_state.area3="B"
        final_board_state.area4="R"
        final_board_state.area5="B"
        final_board_state.area6="R"
        final_board_state.area7="B"
        final_board_state.area8="R"
        final_board_state.area9="B"

    print("goal configuration")
    print(final_board_state)

def handle_game(req):
    global actual_board_state, final_board_state, new_data
    res=GameResponse()
    if req.type=="init":
        print("INIT THE BOARD")
        if req.firstmove=="robot":
            print("ROBOT START")
            set_goal_configuration(1)

        else:
            print("HUMAN START")
            no_color=True
            c=0
            while c<5 or no_color:
                if new_data:
                    new_data=False
                    if actual_board_state.area1=="B" or actual_board_state.area2=="B" or actual_board_state.area3=="B" or actual_board_state.area4=="B" or actual_board_state.area5=="B" or actual_board_state.area6=="B" or actual_board_state.area7=="B" or actual_board_state.area8=="B" or actual_board_state.area9=="B":
                        c+=1
                        time.sleep(1)
                        no_color=False

            if actual_board_state.area2=="B" or actual_board_state.area4=="B" or actual_board_state.area6=="B" or actual_board_state.area9=="B":
                set_goal_configuration(2)
            else:
                set_goal_configuration(1)
        res.success=True

    elif req.type=="new_move":
        print("NEW MOVE")
        
        area=[]
        if actual_board_state.area1==final_board_state.area1:
            area.append(True)
        else:
            area.append(False)
            
        if actual_board_state.area2==final_board_state.area2:
            area.append(True)
        else:
            area.append(False)
        if actual_board_state.area3==final_board_state.area3:
            
            area.append(True)
        else:
            area.append(False)

        if actual_board_state.area4==final_board_state.area4:
            area.append(True)
        else:
            area.append(False)

        if actual_board_state.area5==final_board_state.area5:
            area.append(True)
        else:
            area.append(False)

        if actual_board_state.area6==final_board_state.area6:
            area.append(True)
        else:
            area.append(False)
        if actual_board_state.area7==final_board_state.area7:
            
            area.append(True)
        else:
            area.append(False)

        if actual_board_state.area8==final_board_state.area8:
            area.append(True)
        else:
            area.append(False)

        if actual_board_state.area9==final_board_state.area9:
            area.append(True)
        else:
            area.append(False)
        
        for ba in area:
            if not ba:
                res.success=True
                return res
                        
        res.success=False #there is no new move
        return res
      

    elif req.type=="new_action":
        print(req)
        print(final_board_state)
        print(actual_board_state)
        if final_board_state.area1!=actual_board_state.area1:
            if (final_board_state.area1=="B" and req.firstmove=="human") or (final_board_state.area1=="R" and req.firstmove=="robot"):
                print("area1")
                res.action="area1"
                res.success=True
                return res
        if final_board_state.area2!=actual_board_state.area2:
            if (final_board_state.area2=="B" and req.firstmove=="human") or (final_board_state.area2=="R" and req.firstmove=="robot"):
                print("area2")
                res.action="area2"
                res.success=True
                return res
        if final_board_state.area3!=actual_board_state.area3:
            if (final_board_state.area3=="B" and req.firstmove=="human") or (final_board_state.area3=="R" and req.firstmove=="robot"):
                print("area3")
                res.action="area3"
                res.success=True
                return res
        if final_board_state.area4!=actual_board_state.area4:
            if (final_board_state.area4=="B" and req.firstmove=="human") or (final_board_state.area4=="R" and req.firstmove=="robot"):
                print("area4")
                res.action="area4"
                res.success=True
                return res
        if final_board_state.area5!=actual_board_state.area5:
            if (final_board_state.area5=="B" and req.firstmove=="human") or (final_board_state.area5=="R" and req.firstmove=="robot"):
                print("area5")
                res.action="area5"
                res.success=True
                return res
        if final_board_state.area6!=actual_board_state.area6:
            if (final_board_state.area6=="B" and req.firstmove=="human") or (final_board_state.area6=="R" and req.firstmove=="robot"):
                print("area6")
                res.action="area6"
                res.success=True
                return res
        if final_board_state.area7!=actual_board_state.area7:
            if (final_board_state.area7=="B" and req.firstmove=="human") or (final_board_state.area7=="R" and req.firstmove=="robot"):
                print("area7")
                res.action="area7"
                res.success=True
                return res
        if final_board_state.area8!=actual_board_state.area8:
            if (final_board_state.area8=="B" and req.firstmove=="human") or (final_board_state.area8=="R" and req.firstmove=="robot"):
                print("area8")
                res.action="area8"
                res.success=True
                return res
            
        if final_board_state.area9!=actual_board_state.area9:
            if (final_board_state.area9=="B" and req.firstmove=="human") or (final_board_state.area9=="R" and req.firstmove=="robot"):
                print("area9")
                res.action="area9"
                res.success=True
                return res
        else:
            print("SOMETHING WENT WRONG")
            res.success=False
    else:
        res.success=False
        print("NOT VALID REQUEST")

    return res
   
if __name__ == "__main__": 
    global actual_board_state, final_board_state
    global new_data
    rospy.init_node("game_player")
    board_sub=rospy.Subscriber("/board_state", Board, callback)
    s = rospy.Service('game_player_srv', Game, handle_game)
    actual_board_state=Board()
    final_board_state=Board()
    final_board_state.area1="B"
    final_board_state.area2="R"
    final_board_state.area3="B"
    final_board_state.area4="R"
    start=False
    new_data=False
    
    while not rospy.is_shutdown():
        if start:
            print("SET UP THE BOARD")
        else:
            time.sleep(1)

