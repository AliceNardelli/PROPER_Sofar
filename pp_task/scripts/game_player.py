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
        final_board_state.area3="B"
        final_board_state.area4="R"
    else:
        final_board_state.area1="B"
        final_board_state.area2="R"
        final_board_state.area3="R"
        final_board_state.area4="B"
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
            while c<10 or no_color:
                if new_data:
                    new_data=False
                    if actual_board_state.area1=="B" or actual_board_state.area2=="B" or actual_board_state.area3=="B" or actual_board_state.area4=="B":
                        c+=1
                        time.sleep(1)
                        no_color=False

            if actual_board_state.area1=="B" or actual_board_state.area4=="B":
                set_goal_configuration(2)
            else:
                set_goal_configuration(1)
        res.success=True
    elif req.type=="new_move":
        print("NEW MOVE")
        #capire se fare una media
        if actual_board_state.area1==final_board_state.area1:
            if actual_board_state.area2==final_board_state.area2:
                if actual_board_state.area3==final_board_state.area3:
                    if actual_board_state.area4==final_board_state.area4:
                        print(actual_board_state, final_board_state)
                        res.success=False #there is no new move
        else:
            res.success=True
    elif req.type=="new_action":
        if final_board_state.area1!=actual_board_state.area1:
            if (final_board_state.area1=="B" and req.firstmove=="human") or (final_board_state.area1=="R" and req.firstmove=="robot"):
                res.action="area1"
                res.success=True
                return res
        if final_board_state.area2!=actual_board_state.area2:
            if (final_board_state.area2=="B" and req.firstmove=="human") or (final_board_state.area2=="R" and req.firstmove=="robot"):
                res.action="area2"
                res.success=True
                return res
        if final_board_state.area3!=actual_board_state.area3:
            if (final_board_state.area3=="B" and req.firstmove=="human") or (final_board_state.area3=="R" and req.firstmove=="robot"):
                res.action="area1"
                res.success=True
                return res
        if final_board_state.area1!=actual_board_state.area1:
            if (final_board_state.area1=="B" and req.firstmove=="human") or (final_board_state.area1=="R" and req.firstmove=="robot"):
                res.action="area1"
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

