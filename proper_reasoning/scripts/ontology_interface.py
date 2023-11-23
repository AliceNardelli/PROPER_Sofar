#!/usr/bin/env python
# -*- coding: utf-8 -*-

from proper_reasoning.load_ontology import *
from proper_reasoning.extract_agree import *
from proper_reasoning.extract_intro import *
from proper_reasoning.extract_disagree import *
from proper_reasoning.extract_extro import *
from proper_reasoning.extract_consc import *
from proper_reasoning.extract_unscr import *
from proper_reasoning.perception_predicate import *
from proper_reasoning.srv import ExecAction, ExecActionRequest
import roslib
import rospy
import smach
import smach_ros
import random
import numpy as np
import rospy
from std_msgs.msg import String
import time


#define the actual personality
traits=["Extrovert","Introvert","Conscientious","Unscrupulous","Agreeable","Disagreeable"]
traits_preds=["(extro)","(intro)","(consc)","(unsc)","(agree)","(disagree)"]
we=0.5
wi=0
wc=0
wu=0
wa=0
wd=0.5
sum_weights=we +wi +wc + wu + wa + wd
weights=[we/sum_weights,wi/sum_weights,wc/sum_weights,wu/sum_weights,wa/sum_weights,wd/sum_weights]
gamma=1
perception="NT_N"
new_perception=False

 
f = open("/home/alice/logging.txt", "a")

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
        init_disagreeable_actions()
        init_extro_actions()
        return 'outcome0'

class State_Init(smach.State):
   def __init__(self):
      smach.State.__init__(self, 
                           outcomes=['outcome1'],
                           input_keys=['domain_path','init_pb','problem_path'],
                           )

   def execute(self, userdata):
        rospy.loginfo('Executing state INIT')
        rospy.loginfo('copy pb in the correct file')        
        with open(userdata.init_pb,'r') as firstfile, open(userdata.problem_path,'w') as secondfile:
            for line in firstfile:
            
                if "extroversion_coefficient" in line:
                    if we!=0:
                        l="        (= (extroversion_coefficient) "+str(gamma*(we/sum_weights)) +")\n"
                        secondfile.write(l)
                        p="        "+traits_preds[0]+"\n"
                        secondfile.write(p)
                    else:
                        l="        (= (extroversion_coefficient) "+str(gamma*(wi/sum_weights)) +")\n"
                        secondfile.write(l)
                        p="        "+traits_preds[1]+"\n"
                        secondfile.write(p)
                elif "conscientious_coefficient" in line:
                    if wc!=0:
                        l="        (= (conscientious_coefficient) "+str(gamma*(wc/sum_weights)) +")\n"
                        secondfile.write(l)
                        p="        "+traits_preds[2]+"\n"
                        secondfile.write(p)
                    else:
                        l="        (= (conscientious_coefficient) "+str(gamma*(wu/sum_weights)) +")\n"
                        secondfile.write(l)
                        p="        "+traits_preds[3]+"\n"
                        secondfile.write(p)
                elif "agreeableness_coefficient" in line:
                    if wa!=0:
                        l="        (= (agreeableness_coefficient) "+str(gamma*(wa/sum_weights)) +")\n"
                        secondfile.write(l)
                        p="        "+traits_preds[4]+"\n"
                        secondfile.write(p)
                    else:
                        l="        (= (agreeableness_coefficient) "+str(gamma*(wd/sum_weights)) +")\n"
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
                             outcomes=['outcome2'],
                             input_keys=['command','planning_folder','plan'])
  

    def execute(self, userdata):
        
        rospy.loginfo('planning')
        return_code=planning(userdata.command,userdata.planning_folder,userdata.plan)  
        while return_code!=0:
            return_code=planning(userdata.command,userdata.planning_folder,userdata.plan)  
            
        print("start experiment")
        return 'outcome2'
    

class GetActions(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome3'],
                             input_keys=['plan_path'],
                             output_keys=['executing_actions_out'])
                             
        
    def execute(self, userdata):
        rospy.loginfo('Reading Actions to execute')
          
        out_a=read_plan(userdata.plan_path)
        userdata.executing_actions_out=out_a
        f.write("----------------------\n")
        string_log=" ".join(out_a)+ " \n"
        f.write(string_log)
        f.write("----------------------\n")
        return 'outcome3'
    
class ExAction(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome4','outcome5'],
                             input_keys=['executing_actions'],
                             output_keys=['updated_actions','action','state']) 
    def execute(self, userdata):
        global perception,  new_perception
        rospy.loginfo('Executing actions')
        #num =random.randint(0, 9)
        personality=np.random.choice(traits,p=weights)
        ac=userdata.executing_actions[0]
        print(ac +"--------------"+personality)
        if ac=="AGREE_ACTION":
            #take the perception,
            if perception=="T_":
                pi="T_N"
            else:
                pi=perception
            print("action", ac, "perception: ",pi)
            #extract the action
            aa,rew=choose_action_a(pi)
            rospy.loginfo(" action chosen: "+ aa)
            
            
            userdata, response=self.call_action_server(userdata, aa,personality)
            if response:
                f.write("----------------------\n")
                string_log="before PERCEPTION: " + pi+ "\n"
                f.write(string_log)
                string_log="AGREE ACTION: " + aa +"--------------"+personality+ " reward: " +str(rew)+ "\n"
                f.write(string_log)
                #take the new perception
                if perception=="T_":
                    pn="T_N"
                else:
                    pn=perception #to understand if needed to check new perception
                #update weights
                rr=update_weights_a(aa,pi,pn) #qui in ogni caso avrò una new perception
                string_log="after PERCEPTION: " + pn+ " reward "+ str(rr)+ "\n"
                f.write(string_log)
                string_log="before agree level: " + str(function_objects["agreeableness_level"].has_value)+ "\n"
                f.write(string_log)
                change_raward("reward_a",float(rr))
                return "outcome5"
            else:
                return "outcome4"

        
        if ac=="DISAGREE_ACTION":
            #take the perception,
            if perception=="T_":
                pi="T_N"
            else:
                pi=perception
            print("action", ac, "perception: ",pi)
            #extract the action
            aa,rew=choose_action_d(pi)
            rospy.loginfo(" action chosen: "+ aa)
            
            
            userdata, response=self.call_action_server(userdata, aa,personality)
            if response:
                f.write("----------------------\n")
                string_log="before PERCEPTION: " + pi+ "\n"
                f.write(string_log)
                string_log="DISAGREE ACTION: " + aa +"--------------"+personality+ " reward: " +str(rew)+ "\n"
                f.write(string_log)
                #take the new perception
                if perception=="T_":
                    pn="T_N"
                else:
                    pn=perception #to understand if needed to check new perception
                #update weights
                rr=update_weights_d(aa,pi,pn) #qui in ogni caso avrò una new perception
                string_log="after PERCEPTION: " + pn+ " reward "+ str(rr)+ "\n"
                f.write(string_log)
                string_log="before agree level: " + str(function_objects["agreeableness_level"].has_value)+ "\n"
                f.write(string_log)
                
                change_raward("reward_a",float(rr))
                return "outcome5"
            else:
                return "outcome4"

            

        elif ac=="INTRO_ACTION":
            #take the perception
            if perception=="T_":
                pi="T_N"
            else:
                pi=perception
            print("action", ac, "perception: ",pi)
            #extract the action
            aa,rew=choose_action_i(pi)
            
            userdata, response=self.call_action_server(userdata, aa,personality)
            if response:
                f.write("----------------------\n")
                string_log="before PERCEPTION: " + pi+ "\n"
                f.write(string_log)
                string_log="INTRO ACTION: " + aa +"--------------"+personality+ " reward: " +str(rew)+"\n"
                f.write(string_log)
                rospy.loginfo(" action chosen: "+ aa)
                #exec
                #time.sleep(10)
                #take the new perception
                if perception=="T_":
                    pn="T_N"
                else:
                    pn=perception #to understand if needed to check new perception
                #update weights
                rr=update_weights_i(aa,pi,pn) #qui in ogni caso avrò una new perception
                string_log="after PERCEPTION: " + pn+ " reward "+ str(rr) + "\n"
                f.write(string_log)
                string_log="before extro level: " + str(function_objects["interaction_level"].has_value)+ "\n"
                f.write(string_log)
                change_raward("reward_e",float(rr))
                return "outcome5"
            else:
                return "outcome4"


        elif ac=="EXTRO_ACTION":
            #take the perception
            if perception=="T_":
                pi="T_N"
            else:
                pi=perception
            print("action", ac, "perception: ",pi)
            #extract the action
            aa,rew=choose_action_e(pi)
           
            userdata, response=self.call_action_server(userdata, aa,personality)
            if response:
                f.write("----------------------\n")
                string_log="before PERCEPTION: " + pi+ "\n"
                f.write(string_log)
                string_log="EXTRO ACTION: " + aa +"--------------"+personality+ " reward: " +str(rew)+ "\n"
                f.write(string_log)
                rospy.loginfo(" action chosen: "+ aa)
                #exec
                #time.sleep(10)
                #take the new perception
                if perception=="T_":
                    pn="T_N"
                else:
                    pn=perception #to understand if needed to check new perception
                #update weights
                rr=update_weights_e(aa,pi,pn) #qui in ogni caso avrò una new perception
                string_log="after PERCEPTION: " + pn+ " reward "+ str(rr) + "\n"
                f.write(string_log)
                string_log="before extro level: " + str(function_objects["interaction_level"].has_value)+ "\n"
                f.write(string_log)
                change_raward("reward_e",float(rr))
                return "outcome5"
            else:
                return "outcome4"


        elif ac=="CONSC_ACTION":
            #take the perception
            if perception=="T_":
                pi="T_N"
            else:
                pi=perception
            print("action", ac, "perception: ",pi)
            #extract the action
            aa,rew=choose_action_c(pi)
            
            userdata, response=self.call_action_server(userdata, aa,personality)
            if response:
                f.write("----------------------\n")
                string_log="before PERCEPTION: " + pi+ "\n"
                f.write(string_log)
                string_log="CONSC ACTION: " + aa +"--------------"+personality+ " reward: " +str(rew)+"\n"
                f.write(string_log)
                rospy.loginfo(" action chosen: "+ aa)
                #exec
            
                string_log="before consc level: " + str(function_objects["scrupulousness_level"].has_value)+ "\n"
                f.write(string_log)
                change_raward("reward_c",float(rew))
                return "outcome5"
            else:
                return "outcome4"


        elif ac=="UNSC_ACTION":
            #take the perception
            if perception=="T_":
                pi="T_N"
            else:
                pi=perception
            print("action", ac, "perception: ",pi)
            #extract the action
            aa,rew=choose_action_u(pi)
           
            userdata, response=self.call_action_server(userdata, aa,personality)
            if response:
                f.write("----------------------\n")
                string_log="before PERCEPTION: " + pi+ "\n"
                f.write(string_log)
                string_log="UNSC ACTION: " + aa +"--------------"+personality+ " reward: " +str(rew)+ "\n"
                f.write(string_log)
                rospy.loginfo(" action chosen: "+ aa)
                #exec
                string_log="before consc level: " + str(function_objects["scrupulousness_level"].has_value)+ "\n"
                f.write(string_log)
                change_raward("reward_c",float(rew))
                return "outcome5"
            else:
                return "outcome4"


        else:
            f.write("----------------------\n")
            string_log="STANDARD ACTION:" + ac +"--------------"+personality+ "\n"
            f.write(string_log)
            string_log="before agree level: " + str(function_objects["agreeableness_level"].has_value)+ "\n"
            f.write(string_log)
            string_log="before extro level: " + str(function_objects["interaction_level"].has_value)+ "\n"
            f.write(string_log)
            string_log="before consc level: " + str(function_objects["scrupulousness_level"].has_value)+ "\n"
            f.write(string_log)
            rospy.loginfo('Action executed: '+ac)
            
            #time.sleep(10)
            userdata, response=self.call_action_server(userdata, ac,personality)
            if response:
                return "outcome5"
            else:
                return "outcome4"


    def call_action_server(self, userdata, ac,personality):
            userdata.state="exec"
            rospy.wait_for_service('action_dispatcher_srv')
            try:
                action_dispatcher_srv = rospy.ServiceProxy('action_dispatcher_srv', ExecAction)
                msg=ExecActionRequest()
                msg.action=ac.lower()
                msg.personality=personality
                resp = action_dispatcher_srv(msg)
                if resp.success==False:
                    rospy.loginfo('Action Failed')        
                    f.write("ACTION FAIL\n")
                    return userdata, False
                else:
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
                             outcomes=['outcome7',"outcome8","outcome9"],
                             input_keys=["state","exec_actions","action"])
        
    def execute(self, userdata):
        global perception, new_perception
        rospy.loginfo('check perception')

        if "ACTION" in userdata.action:
            return "outcome9" #if I have done a trait specific action I need to replan

        if new_perception==False:
            print("No new perception")
            if userdata.state=="exec":
                f.write("Action fail need replanning\n")
                return "outcome9"
            else:
                if userdata.exec_actions==[]:
                    f.write("task finished \n")
                    
                    return "outcome8"
                else:
                    f.write("executing next action \n")
                   
                    return "outcome7"
        else:
            print("new perception  ", perception)
            f.write("----------------------\n")
            string_log="new perception  "+ perception +"\n"
            f.write(string_log)
            f.write("----------------------\n")
            
            touched=perception_predicate_map[perception]["touch"]
            emotion=perception_predicate_map[perception]["emotion"]
            goals=perception_predicate_map[perception]["goals"]
            if touched!="":
                add_predicate(touched)

            if emotion!="":
                add_predicate(emotion)

            for g in goals:
                add_goal(g)#state that that predicate is a goal
                remove_predicate(g) #now the goal predicate is not grounded
            new_perception=False
            return "outcome9"

        
class WriteProblem(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome10'],
                             input_keys=['pb_path'],)
        
    def execute(self, userdata):
        rospy.loginfo('Writing a new plan')
        update_problem(userdata.pb_path)
        return 'outcome10'
    
class UpdateOntology(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome6'],
                             input_keys=['action'],
                             output_keys=['state',"out_action"])
        
    def execute(self, userdata):
        rospy.loginfo('Update_ontology')
        acc=userdata.action
        update_ontology(userdata.action)
        userdata.state="update"
        initialize_reward()
        string_log="after agree level: " + str(function_objects["agreeableness_level"].has_value)+ "\n"
        f.write(string_log)
        string_log="after extro level: " + str(function_objects["interaction_level"].has_value)+ "\n"
        f.write(string_log)
        string_log="after consc level: " + str(function_objects["scrupulousness_level"].has_value)+ "\n"
        f.write(string_log)
        userdata.out_action=acc
        return 'outcome6'

class Finish(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             input_keys=['input_goals'],
                             outcomes=['outcome11','outcome12'],
                             )
        
    def execute(self,userdata):
        if userdata.input_goals!=[]:
            rospy.loginfo('Passing to the next goal')
            return "outcome11"
        else:
            f.close()
            rospy.loginfo('Finishhh')
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
        sm.userdata.a="a"
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
                                    transitions={'outcome1':'PLAN'},
                                    remapping={'domain_path':'path_domain', 
                                                'problem_path':'path_problem',
                                                'init_pb':'path_init_problem'
                                                })
            smach.StateMachine.add('PLAN', Planning(), 
                                    transitions={'outcome2':'GET_ACTIONS'},
                                    remapping={'command':'command_start',
                                                'planning_folder':'folder',
                                                'plan':'path_plan'})
            
            smach.StateMachine.add('GET_ACTIONS', GetActions(), 
                                    transitions={'outcome3':'EXEC'},
                                    remapping={'plan_path':'path_plan',
                                                'executing_actions_out':'actions',
                                            })
            
            smach.StateMachine.add('EXEC', ExAction(), 
                                transitions={'outcome4':'CHECK_PERC',
                                            'outcome5':'UPDATE_ONTOLOGY',
                                            },
                                remapping={'executing_actions':'actions',
                                        'updated_actions':'actions',
                                        'action':"a" ,
                                        "previous_state":"state"
                                        })
            
            smach.StateMachine.add('CHECK_PERC', CheckPerc(), 
                                transitions={'outcome7':'EXEC',
                                            'outcome8':'FINISH',
                                            'outcome9':'WRITE_PLAN',
                                            },
                                remapping={
                                    "action":"a",
                                    "state":"previous_state",
                                    "exec_actions":"actions"
                                        })
            
            smach.StateMachine.add('WRITE_PLAN', WriteProblem(), 
                        transitions={'outcome10':'PLAN'},
                        remapping={'pb_path':'path_problem'
                                            })
            
            smach.StateMachine.add('UPDATE_ONTOLOGY', UpdateOntology(), 
                        transitions={'outcome6':'CHECK_PERC',
                                    },
                        remapping={'action':'a',
                                   "previous_state":"state",
                                   "a":"out_action"
                                })

            smach.StateMachine.add('FINISH', Finish(), 
                        transitions={'outcome11':"START",
                                     'outcome12':'outcome13'},
                        remapping={
                            "input_goals":"goals"
                        }
                        )
    
        # Create and start the introspection server for visualization
        #sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
        #sis.start()

        # Execute the state machine
        outcome = sm.execute()

        # Wait for ctrl-c to stop the application
        rospy.spin()
        #sis.stop()
    except rospy.ROSInterruptException:
        rospy.loginfo("interrupt")

if __name__ == '__main__':
      main()



    