#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import rospy
from std_msgs.msg import String
from proper_lpg.load_ontology import *
from proper_lpg.extract_agree import *
from proper_lpg.extract_intro import *
from proper_lpg.extract_disagree import *
from proper_lpg.extract_extro import *
from proper_lpg.extract_consc import *
from proper_lpg.extract_unscr import *
from proper_lpg.perception_predicate import *
from proper_lpg.srv import ExecAction, ExecActionRequest
from pp_task.srv import Game, GameRequest
import roslib
import smach
import random
import numpy as np
import time
import threading
import datetime
#define the actual personality
traits=["Extrovert","Introvert","Conscientious","Unscrupolous","Agreeable","Disagreeable"]
traits_preds=["(extro)","(intro)","(consc)","(unsc)","(agree)","(disagree)"]

we=0
wi=1
wc=0
wu=0
wa=1
wd=0
sum_weights=0
weights=[]
gamma=1
new_perception=False
perception=""
first_trial=True


def callback(data):
    global perception
    global new_perception
    if perception!=data.data:
        perception=data.data
        new_perception=True

class State_Start(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome0'],
                             input_keys=['input_goals',],
                             output_keys=['output_goals','domain_path','problem_path','init_pb','command','path','plan_path'])
        
    def execute(self, userdata):
        global wa,wd,we,wi,wc,wd,sum_weights,weights
        goals=userdata.input_goals
        actual_goal=goals.pop(0)
        rospy.loginfo('Executing goal: '+ actual_goal)
        dict_goal=rospy.get_param(actual_goal)
        rospy.set_param("actual_goal",actual_goal)
        userdata.output_goals=goals
        userdata.domain_path=dict_goal["domain"]
        userdata.problem_path=dict_goal["problem"]
        userdata.init_pb=dict_goal["init"]
        userdata.command=dict_goal["command"]
        userdata.path=dict_goal["folder"]
        userdata.plan_path=dict_goal["plan"]
        print("weights unscrupolous",wu)
        sum_weights=float(we +wi +wc + wu + wa + wd)
        try: 
            weights=[we/sum_weights,wi/sum_weights,wc/sum_weights,wu/sum_weights,wa/sum_weights,wd/sum_weights]
            print(weights)
        except:
            print(weights)
            weights=6*[0]
            sum_weights=1

        init_disagreeable_actions()
        init_agreeable_actions()
        init_extro_actions()
        init_intro_actions()
        init_consc_actions()
        init_unsc_actions()
        return 'outcome0'

class State_Init(smach.State):
   def __init__(self):
      smach.State.__init__(self, 
                           outcomes=['outcome1'],
                           input_keys=['domain_path','init_pb','problem_path'],
                           )

   def execute(self, userdata):
        print('Executing state INIT') 
        global wa,wd,we,wi,wc,wd,sum_weights,weights   
        with open(userdata.init_pb,'r') as firstfile, open(userdata.problem_path,'w') as secondfile:
            for line in firstfile:
            
                if "extroversion_coefficient" in line:
                    if we!=0.0:
                        l="        (= (extroversion_coefficient) "+str(weights[0]) +")\n"
                        secondfile.write(l)
                        p="        "+traits_preds[0]+"\n"
                        secondfile.write(p)
                    else:
                        print(str(gamma*(wi/sum_weights)))
                        l="        (= (extroversion_coefficient) "+str(weights[1]) +")\n"
                        secondfile.write(l)
                        p="        "+traits_preds[1]+"\n"
                        secondfile.write(p)
                elif "conscientious_coefficient" in line:
                    if wc!=0.0:
                        l="        (= (conscientious_coefficient) "+str(weights[2]) +")\n"
                        secondfile.write(l)
                        p="        "+traits_preds[2]+"\n"
                        secondfile.write(p)
                    else:
                        print(gamma*(wu/sum_weights))
                        l="        (= (conscientious_coefficient) "+str(weights[3]) +")\n"
                        secondfile.write(l)
                        p="        "+traits_preds[3]+"\n"
                        secondfile.write(p)
                elif "agreeableness_coefficient" in line:
                    if wa!=0:
                        l="        (= (agreeableness_coefficient) "+str(weights[4]) +")\n"
                        secondfile.write(l)
                        p="        "+traits_preds[4]+"\n"
                        secondfile.write(p)
                    else:
                        l="        (= (agreeableness_coefficient) "+str(weights[5]) +")\n"
                        secondfile.write(l)
                        p="        "+traits_preds[5]+"\n"
                        secondfile.write(p)
                else:
                    secondfile.write(line)
        rospy.loginfo('Reading domain and populate ontology')
        populate_ontology(userdata.domain_path)
        rospy.loginfo('Initialize function and predicates in the ontology')
        initialize_functions_predicates()
        rospy.loginfo('Read the problem and set the initial values of predicates and functions')
        read_the_problem(userdata.problem_path) 
        return 'outcome1'
      


# define state Bar
class Planning(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome6'],
                             input_keys=['command','planning_folder','plan'])
  

    def execute(self, userdata):
        print('planning')
        return_code=planning(userdata.command,userdata.planning_folder,userdata.plan)  
        while return_code!=0:
            return_code=planning(userdata.command,userdata.planning_folder,userdata.plan)  
            
        print("start experiment")
        return 'outcome6'
    

class GetActions(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome7'],
                             input_keys=['plan_path'],
                             output_keys=['executing_actions_out'])
                             
        
    def execute(self, userdata):
        print('Reading Actions to execute')
          
        out_a=read_plan(userdata.plan_path)
        userdata.executing_actions_out=out_a
        return 'outcome7'
    
class ExAction(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome8','outcome9','outcome13'],
                             input_keys=['executing_actions'],
                             output_keys=['updated_actions','action','state',"out_pp"]) 
    def execute(self, userdata):
        global perception, first_trial
        personality=np.random.choice(traits,p=weights)
        ac=userdata.executing_actions[0]


        if ac=="AGREE_ACTION":
            pi=map_perception_AV_axis[perception]
            aa,rew=choose_action_a(pi)
            userdata, response= self.call_action_server(userdata, aa, personality)
            if response:
                pn=map_perception_AV_axis[perception]
                rr=update_weights_a(aa,pi,pn) #qui in ogni caso avrò una new perception
                change_raward("reward_a",float(rr))
                userdata.out_pp="trait"
                return "outcome9"
            else:
                return "outcome8"
            
        if ac=="DISGREE_ACTION":
            pi=map_perception_AV_axis[perception]
            aa,rew=choose_action_d(pi)
            userdata, response= self.call_action_server(userdata, aa, personality)
            if response:
                pn=map_perception_AV_axis[perception]
                rr=update_weights_d(aa,pi,pn) #qui in ogni caso avrò una new perception
                change_raward("reward_a",float(rr))
                userdata.out_pp="trait"
                return "outcome9"
            else:
                return "outcome8"
        

        if ac=="INTRO_ACTION":
            pi=map_perception_AV_axis[perception]
            aa,rew=choose_action_i(pi)
            userdata, response= self.call_action_server(userdata, aa, personality)
            if response:
                pn=map_perception_AV_axis[perception]
                rr=update_weights_i(aa,pi,pn) #qui in ogni caso avrò una new perception
                change_raward("reward_e",float(rr))
                userdata.out_pp="trait"
                return "outcome9"
            else:
                return "outcome8"
            
        if ac=="EXTRO_ACTION":
            pi=map_perception_AV_axis[perception]
            aa,rew=choose_action_e(pi)
            userdata, response= self.call_action_server(userdata, aa, personality)
            if response:
                pn=map_perception_AV_axis[perception]
                rr=update_weights_e(aa,pi,pn) #qui in ogni caso avrò una new perception
                change_raward("reward_e",float(rr))
                userdata.out_pp="trait"
                return "outcome9"
            else:
                return "outcome8"
            
        
        if ac=="CONSC_ACTION":
            pi=map_perception_AV_axis[perception]
            aa,rew=choose_action_c(pi)
            userdata, response= self.call_action_server(userdata, aa, personality)
            if response:
                pn=map_perception_AV_axis[perception]
                rr=update_weights_c(aa,pi,pn) #qui in ogni caso avrò una new perception
                change_raward("reward_c",float(rr))
                userdata.out_pp="trait"
                return "outcome9"
            else:
                return "outcome8"
        

        if ac=="UNSC_ACTION":
            pi=map_perception_AV_axis[perception]
            aa,rew=choose_action_u(pi)
            userdata, response= self.call_action_server(userdata, aa, personality)
            if response:
                pn=map_perception_AV_axis[perception]
                rr=update_weights_u(aa,pi,pn) #qui in ogni caso avrò una new perception
                change_raward("reward_c",float(rr))
                userdata.out_pp="trait"
                return "outcome9"
            else:
                return "outcome8"

        else:
            userdata, response=self.call_action_server(userdata, ac, personality)
            if response:
                if first_trial:            
                    
                    if ("TURN1" in ac):
                        first_trial=False
                        req=GameRequest()
                        req.type="init"
                        if ("HUMAN" in ac):
                            req.firstmove="human"
                        elif ("ROBOT" in ac):
                            req.firstmove="robot"    
                        rospy.wait_for_service('game_player_srv')
                        game_client = rospy.ServiceProxy('game_player_srv', Game)
                        resp = game_client(req)
                userdata.out_pp="no_trait"
                return "outcome9"
            else:
                return "outcome8"



    def call_action_server(self, userdata, ac,personality):
            userdata.state="exec"
            rospy.wait_for_service('action_dispatcher_srv')
            try:
                if ac in not_to_execute:
                    print(str(ac)+" not to execute")

                else:
                    action_dispatcher_srv = rospy.ServiceProxy('action_dispatcher_srv', ExecAction)
                    msg=ExecActionRequest()
                    msg.action=ac.lower()
                    msg.personality=personality
                    print("executing", msg.action)
                    resp = action_dispatcher_srv(msg)
                    if resp.success==False:
                        rospy.loginfo('Action Failed')        
                        return userdata, False
                    
                ac=userdata.executing_actions.pop(0)
                rospy.loginfo('Action executed: '+ac)
                userdata.action=ac
                userdata.updated_actions=userdata.executing_actions
                return userdata,True
                
            except rospy.ServiceException as e:
                print("Service call failed: %s"%e)


           
class CheckPerc(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome3',"outcome4","outcome2","outcome13"],
                             input_keys=["state","exec_actions","action"],
                             output_keys=["out_action","out_pp"])
        
    def execute(self, userdata):
        global new_perception, perception
        #IF NEW PERCEPTION
        
        go_plan=False
        if new_perception: 
            new_perception=False
            emotion_pred=perception_predicate_map[perception]["emotion"]
            attention_pred=perception_predicate_map[perception]["attention"]
            goals=perception_predicate_map[perception]["goals"]

            pred_add=perception_predicate_map[perception]["pred_to_ground"]
            for p in pred_add:
                add_predicate(p)

            pred_rem=perception_predicate_map[perception]["pred_to_remove"]
            for p in pred_rem:
                remove_predicate(p)

            add_predicate(emotion_pred)
            add_predicate(attention_pred)
            for g in goals:
                add_goal(g)#state that that predicate is a goal
                remove_predicate(g) #now the goal predicate is not grounded
            go_plan=True
        
        # se sono al primo giro o ho finito il giro
        print("ho un nuovo blocco da sistemare?")
        print(predicates_objects["action2"].is_grounded)
        if userdata.action=="" or predicates_objects["action2"].is_grounded:
            req=GameRequest()
            req.type="new_move"
            rospy.wait_for_service('game_player_srv')
            game_client = rospy.ServiceProxy('game_player_srv', Game)
            resp = game_client(req)
            print(resp)
            if resp.success==True:
                add_goal("finished")
                remove_predicate("action2")
                add_predicate("new_block")
                add_goal("feel_comfort")
                remove_predicate("feel_comfort")
                go_plan=True

        if go_plan==True:
            return "outcome3"


        #IF I NO NEW PERCEPTION A NO BLOCK TO ADD
        else:
            if userdata.state=="exec": #action fail
                return "outcome3"
            
            else: #pass to the next action
                if userdata.exec_actions==[]:
                    return "outcome4"
                else:
                    return "outcome2"


        
class WriteProblem(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome5'],
                             input_keys=['pb_path'],)
        
    def execute(self, userdata):
        print('Writing a new plan')
        update_problem(userdata.pb_path)
        return 'outcome5'
    
class UpdateOntology(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome10',"outcome11"],
                             input_keys=['action',"in_pp"],
                             output_keys=['state',"out_action"])
        
    def execute(self, userdata):
        print('Update_ontology')
        acc=userdata.action
        update_ontology(userdata.action)
        userdata.state="update"
        initialize_reward()
        userdata.out_action=acc
        if userdata.in_pp=="trait":
            return 'outcome11'
        return 'outcome10'
    

class Finish(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             input_keys=['input_goals'],
                             output_keys=["out_action"],
                             outcomes=['outcome11','outcome12'],
                             )
        
    def execute(self,userdata):
        if userdata.input_goals!=[]:
            print('Passing to the next goal')
            userdata.out_action=""
            return "outcome11"
        else:
            print('Finishhh')
            return 'outcome12'




def main():
    rospy.init_node('smach_example_state_machine')
    # Create a SMACH state machine
    rospy.Subscriber("perception", String, callback)
    try:
        sm = smach.StateMachine(outcomes=['outcome13'])
        sm.userdata.goals=rospy.get_param("goals")
        sm.userdata.path_domain=""
        sm.userdata.path_problem=""
        sm.userdata.path_init_problem=""
        sm.userdata.command_start=""
        sm.userdata.folder =""
        sm.userdata.path_plan =""
        sm.userdata.actions =[]
        sm.userdata.a=""
        sm.userdata.pp=""
        sm.userdata.previous_state=""
        # Open the container
        with sm:
            smach.StateMachine.add('START', State_Start(), 
                        transitions={'outcome0':'INIT'},
                        remapping={ 'input_goals':'goals',
                                    'output_goals':'goals',
                                    'domain_path':'path_domain', 
                                    'problem_path':'path_problem',
                                    'init_pb':'path_init_problem',
                                    'command':'command_start',
                                    'path':'folder',
                                    'plan_path':'path_plan'
                                    })
            # Add states to the container
            smach.StateMachine.add('INIT', State_Init(), 
                                    transitions={'outcome1':'CHECK_PERC'},
                                    remapping={'domain_path':'path_domain', 
                                                'problem_path':'path_problem',
                                                'init_pb':'path_init_problem'
                                                })
            smach.StateMachine.add('PLAN', Planning(), 
                                    transitions={'outcome6':'GET_ACTIONS'},
                                    remapping={'command':'command_start',
                                                'planning_folder':'folder',
                                                'plan':'path_plan'})
            
            smach.StateMachine.add('GET_ACTIONS', GetActions(), 
                                    transitions={'outcome7':'EXEC'},
                                    remapping={'plan_path':'path_plan',
                                                'executing_actions_out':'actions',
                                            })
            
            smach.StateMachine.add('EXEC', ExAction(), 
                                transitions={'outcome8':'CHECK_PERC',
                                            'outcome9':'UPDATE_ONTOLOGY',
                                            'outcome13':'START'
                                            },
                                remapping={'executing_actions':'actions',
                                        'updated_actions':'actions',
                                        'action':"a" ,
                                        "previous_state":"state"
                                        })
            
            smach.StateMachine.add('CHECK_PERC', CheckPerc(), 
                                transitions={'outcome2':'EXEC',
                                            'outcome4':'FINISH',
                                            'outcome3':'WRITE_PLAN',
                                            "outcome13":"START",
                                            },
                                remapping={
                                    "action":"a",
                                    "state":"previous_state",
                                    "exec_actions":"actions",
                                    "out_action":"a",
                                    "out_pp":"pp"
                                        })
            
            smach.StateMachine.add('WRITE_PLAN', WriteProblem(), 
                        transitions={'outcome5':'PLAN'},
                        remapping={'pb_path':'path_problem'
                                            })
            
            smach.StateMachine.add('UPDATE_ONTOLOGY', UpdateOntology(), 
                        transitions={'outcome10':'CHECK_PERC',
                                     "outcome11":"WRITE_PLAN"
                                    },
                        remapping={'action':'a',
                                   "previous_state":"state",
                                   "a":"out_action",
                                   "in_pp":"pp"
                                })

            smach.StateMachine.add('FINISH', Finish(), 
                        transitions={'outcome11':"START",
                                     'outcome12':'outcome13'},
                        remapping={
                            "input_goals":"goals",
                            "out_action":"a"
                        }
                        )
    
        # Create and start the introspection server for visualization
        #sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
        #sis.start()
        outcome = sm.execute()
        
    

    except:
        print("interrupt")

if __name__ == '__main__':
      main()



    