#!/usr/bin/env python
# -*- coding: utf-8 -*-

from proper_lpg.load_ontology import *
from proper_lpg.extract_agree import *
from proper_lpg.srv import ExecAction, ExecActionRequest
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
we=0
wi=0
wc=0
wu=0
wa=1
wd=0
sum_weights=we +wi +wc + wu + wa + wd
weights=[we/sum_weights,wi/sum_weights,wc/sum_weights,wu/sum_weights,wa/sum_weights,wd/sum_weights]
gamma=0.3

# define state Foo
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
        rospy.loginfo('Read the problem and set the initial values of predicates  and functions')
        read_the_problem(userdata.problem_path)      
        return 'outcome1'
      


# define state Bar
class Planning(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome2'],
                             input_keys=['command','planning_folder'])
    def callback(self, data):
         self.start=True 

    def execute(self, userdata):
        self.start=False
        rospy.loginfo('planning')
        return_code=planning(userdata.command,userdata.planning_folder)  
        print(return_code)
        while return_code!=0:
            return_code=planning(userdata.command,userdata.planning_folder)  
            print(return_code)
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
        print(userdata.plan_path)   
        userdata.executing_actions_out=read_plan(userdata.plan_path)
        return 'outcome3'
    
class ExAction(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome4','outcome5'],
                             input_keys=['executing_actions'],
                             output_keys=['updated_actions','action']) 
    def execute(self, userdata):
        rospy.loginfo('Executing actions')
        #num =random.randint(0, 9)
        personality=np.random.choice(traits,p=weights)
        ac=userdata.executing_actions[0]
        print(ac +"--------------"+personality)
        success=random.randint(0,10)
        if success==0:
            print("action fail")
            return "outcome4"
        else:
            if "ACTION" in ac:
                #take the perception
                pi="NT_N"
                #extract the action
                aa,rew=choose_action(pi)
                rospy.loginfo('Action executed: '+ac+ " action chosen: "+ aa)
                #exec
                #take the new perception
                pn="NT_H"
                #update weights
                rr=update_weights(aa,pi,pn) #qui in ogni caso avrò una new perception
                change_raward("reward_a",rr)
            else:
                rospy.loginfo('Action executed: '+ac)
            
            ac=userdata.executing_actions.pop(0)
            userdata.action=ac
            userdata.updated_actions=userdata.executing_actions
            return "outcome5"
        
class CheckPerc(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome7'],
                             input_keys=[],)
        
    def execute(self, userdata):
        rospy.loginfo('check perception')
        
        return 'outcome7'
        
class WriteProblem(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome7'],
                             input_keys=['pb_path'],)
        
    def execute(self, userdata):
        rospy.loginfo('Writing a new plan')
        update_problem(userdata.pb_path)
        return 'outcome7'
    
class UpdateOntology(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome6'],
                             input_keys=['action'],)
        
    def execute(self, userdata):
        rospy.loginfo('Update_ontology')
        print(userdata.action)
        update_ontology(userdata.action)
        initialize_reward()
        return 'outcome6'

class Finish(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome7'],
                             )
        
    def execute(self,userdata):
        rospy.loginfo('Finishhh')
        return 'outcome7'


def main():
    rospy.init_node('smach_example_state_machine')
    # Create a SMACH state machine
    try:
        sm = smach.StateMachine(outcomes=['outcome8'])
        sm.userdata.path_domain='/home/alice/catkin_ws/src/PROPER_Sofar/proper_lpg/domain_prova.pddl'
        sm.userdata.path_problem='/home/alice/catkin_ws/src/PROPER_Sofar/proper_lpg/prova_problem.pddl'
        sm.userdata.path_init_problem='/home/alice/catkin_ws/src/PROPER_Sofar/proper_lpg/init_problem.pddl'
        sm.userdata.command_start='./lpg++ -o domain_prova.pddl -f prova_problem.pddl -n 1 -force_neighbour_insertion -inst_with_contraddicting_objects'
        sm.userdata.folder ='/home/alice/catkin_ws/src/PROPER_Sofar/proper_lpg/'
        sm.userdata.path_plan ='/home/alice/catkin_ws/src/PROPER_Sofar/proper_lpg/plan_prova_problem.pddl_1.SOL'
        sm.userdata.actions =[]
        sm.userdata.a="a"
        # Open the container
        with sm:
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
                                                'planning_folder':'folder'})
            
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
                                        'action':"a" 
                                        })
            
            smach.StateMachine.add('CHECK_PERC', CheckPerc(), 
                                transitions={'outcome7':'EXEC',
                                            'outcome8':'FINISH',
                                            'outcome9':'WRITE_PLAN',
                                            },
                                remapping={
                                        })
            
            smach.StateMachine.add('WRITE_PLAN', WriteProblem(), 
                        transitions={'outcome7':'PLAN'},
                        remapping={'pb_path':'path_problem'
                                            })
            
            smach.StateMachine.add('UPDATE_ONTOLOGY', UpdateOntology(), 
                        transitions={'outcome6':'CHECK_PERC',
                                    },
                        remapping={'action':'a',
                                })

            smach.StateMachine.add('FINISH', Finish(), 
                        transitions={'outcome7':'outcome8'},
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



    