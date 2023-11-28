#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from load_ontology import *
from problem_param import *
from perception_predicate import *
from extract_agree import *
from extract_intro import *
from extract_disagree import *
from extract_extro import *
from extract_consc import *
from extract_unscr import *
from action_dispatcher import *
import smach
import random
import numpy as np
import time
import threading

#define the actual personality
traits=["Extrovert","Introvert","Conscientious","Unscrupulous","Agreeable","Disagreeable"]
traits_preds=["(extro)","(intro)","(consc)","(unsc)","(agree)","(disagree)"]
we=0
wi=0
wc=0
wu=1
wa=0
wd=0
sum_weights=we +wi +wc + wu + wa + wd
weights=[we/sum_weights,wi/sum_weights,wc/sum_weights,wu/sum_weights,wa/sum_weights,wd/sum_weights]
gamma=1
emotion=""
new_emotion=False
new_sentence=False

url='http://127.0.0.1:5020/'
headers= {'Content-Type':'application/json'}

data={
    "emotion":"",
    "new_sentence":"False",
    "new_emotion":"False",
    "update":"False"
}


f = open("/home/alice/logging.txt", "a")
f1 = open("/home/alice/logging_disagree.txt", "a")



class State_Start(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome0'],
                             input_keys=['input_goals',],
                             output_keys=['output_goals','domain_path','problem_path','init_pb','command','path','plan_path'])
        
    def execute(self, userdata):
        goals=userdata.input_goals
        actual_goal=goals.pop(0)
        print('Executing goal: '+ actual_goal)
        dict_goal=goals_dict[actual_goal]
        userdata.output_goals=goals
        userdata.domain_path=dict_goal["domain"]
        userdata.problem_path=dict_goal["problem"]
        userdata.init_pb=dict_goal["init"]
        userdata.command=dict_goal["command"]
        userdata.path=dict_goal["folder"]
        userdata.plan_path=dict_goal["plan"]
        return 'outcome0'

class State_Init(smach.State):
   def __init__(self):
      smach.State.__init__(self, 
                           outcomes=['outcome1'],
                           input_keys=['domain_path','init_pb','problem_path'],
                           )

   def execute(self, userdata):
        print('Executing state INIT')      
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
        print('Reading domain and populate ontology')
        populate_ontology(userdata.domain_path)
        print('Initialize function and predicates in the ontology')
        initialize_functions_predicates()
        print('Read the problem and set the initial values of predicates and functions')
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
        f.write("----------------------\n")
        string_log=" ".join(out_a)+ " \n"
        f.write(string_log)
        f.write("----------------------\n")
        return 'outcome7'
    
class ExAction(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome8','outcome9'],
                             input_keys=['executing_actions'],
                             output_keys=['updated_actions','action','state']) 
    def execute(self, userdata):
        global new_emotion, emotion
        personality=np.random.choice(traits,p=weights)
        ac=userdata.executing_actions[0]

        if ac=="AGREE_ACTION":
            data["update"]="False"
            resp=requests.put(url+'get_input', json=data, headers=headers)
            emotion=eval(resp.text)["emotion"]
            pi=map_emotion_AV_axis[emotion]
            aa,rew=choose_action_a(pi)
            userdata, response=self.call_action_server(userdata, aa, personality)
            if response:
                f.write("----------------------\n")
                string_log="before PERCEPTION: " + emotion+ "\n"
                f.write(string_log)
                string_log="AGREE ACTION: " + aa +"--------------"+personality+ " reward: " +str(rew)+ "\n"
                f.write(string_log)
                data["update"]="False"
                resp=requests.put(url+'get_input', json=data, headers=headers)
                emotion=eval(resp.text)["emotion"]
                rr=update_weights_a(aa,pi,map_emotion_AV_axis[emotion]) #qui in ogni caso avrò una new perception
                string_log="after PERCEPTION: " + map_emotion_AV_axis[emotion]+ " reward "+ str(rr)+ "\n"
                f.write(string_log)
                change_raward("reward_a",float(rr))
                return "outcome9"
            else:
                return "outcome8"

        
        if ac=="DISAGREE_ACTION":
            data["update"]="False"
            resp=requests.put(url+'get_input', json=data, headers=headers)
            emotion=eval(resp.text)["emotion"]
            pi=map_emotion_AV_axis[emotion]
            aa,rew=choose_action_d(map_emotion_AV_axis[emotion])
            userdata, response=self.call_action_server(userdata, aa, personality)
            if response:
                f.write("----------------------\n")
                string_log="before PERCEPTION: " + emotion+ "\n"
                f.write(string_log)
                string_log="DISAGREE ACTION: " + aa +"--------------"+personality+ " reward: " +str(rew)+ "\n"
                f.write(string_log)
                data["update"]="False"
                resp=requests.put(url+'get_input', json=data, headers=headers)
                emotion=eval(resp.text)["emotion"]
                rr=update_weights_d(aa,pi,map_emotion_AV_axis[emotion]) #qui in ogni caso avrò una new perception
                string_log="after PERCEPTION: " + map_emotion_AV_axis[emotion]+ " reward "+ str(rr)+ "\n"
                f.write(string_log)
                change_raward("reward_a",float(rr))
                string_log="before agree level: " + str(function_objects["agreeableness_level"].has_value)+ "\n"
                f.write(string_log)
                return "outcome9"
            else:
                return "outcome8"

            
        elif ac=="INTRO_ACTION":
            data["update"]="False"
            resp=requests.put(url+'get_input', json=data, headers=headers)
            emotion=eval(resp.text)["emotion"]
            pi=map_emotion_AV_axis[emotion]
            aa,rew=choose_action_i(pi)
            userdata, response=self.call_action_server(userdata, aa, personality)
            if response:
                f.write("----------------------\n")
                string_log="before PERCEPTION: " + pi+ "\n"
                f.write(string_log)
                string_log="INTRO ACTION: " + aa +"--------------"+personality+ " reward: " +str(rew)+"\n"
                f.write(string_log)
                data["update"]="False"
                resp=requests.put(url+'get_input', json=data, headers=headers)
                emotion=eval(resp.text)["emotion"]
                pn=map_emotion_AV_axis[emotion]
                rr=update_weights_i(aa,pi,pn) #qui in ogni caso avrò una new perception
                string_log="after PERCEPTION: " + pn+ " reward "+ str(rr) + "\n"
                f.write(string_log)
                string_log="before extro level: " + str(function_objects["interaction_level"].has_value)+ "\n"
                f.write(string_log)
                change_raward("reward_e",float(rr))
                return "outcome9"
            else:
                return "outcome8"
            

           


        elif ac=="EXTRO_ACTION":
            data["update"]="False"
            resp=requests.put(url+'get_input', json=data, headers=headers)
            emotion=eval(resp.text)["emotion"]
            pi=map_emotion_AV_axis[emotion]
            aa,rew=choose_action_e(pi)
            userdata, response=self.call_action_server(userdata, aa, personality)
            if response:
                f.write("----------------------\n")
                string_log="before PERCEPTION: " + pi+ "\n"
                f.write(string_log)
                string_log="EXTRO ACTION: " + aa +"--------------"+personality+ " reward: " +str(rew)+"\n"
                f.write(string_log)
                data["update"]="False"
                resp=requests.put(url+'get_input', json=data, headers=headers)
                emotion=eval(resp.text)["emotion"]
                pn=map_emotion_AV_axis[emotion]
                rr=update_weights_e(aa,pi,pn) #qui in ogni caso avrò una new perception
                string_log="after PERCEPTION: " + pn+ " reward "+ str(rr) + "\n"
                f.write(string_log)
                string_log="before extro level: " + str(function_objects["interaction_level"].has_value)+ "\n"
                f.write(string_log)
                change_raward("reward_e",float(rr))
                return "outcome9"
            else:
                return "outcome8"


        elif ac=="CONSC_ACTION":
            data["update"]="False"
            resp=requests.put(url+'get_input', json=data, headers=headers)
            emotion=eval(resp.text)["emotion"]
            pi=map_emotion_AV_axis[emotion]
            aa,rew=choose_action_c(pi)
            userdata, response=self.call_action_server(userdata, aa,personality)
            if response:
                f.write("----------------------\n")
                string_log="before PERCEPTION: " + pi+ "\n"
                f.write(string_log)
                string_log="CONSC ACTION: " + aa +"--------------"+personality+ " reward: " +str(rew)+"\n"
                f.write(string_log)
                string_log="before consc level: " + str(function_objects["scrupulousness_level"].has_value)+ "\n"
                f.write(string_log)
                change_raward("reward_c",float(rew))
                return "outcome9"
            else:
                return "outcome8"


        elif ac=="UNSC_ACTION":
            data["update"]="False"
            resp=requests.put(url+'get_input', json=data, headers=headers)
            emotion=eval(resp.text)["emotion"]
            pi=map_emotion_AV_axis[emotion]
            aa,rew=choose_action_u(pi)
           
            userdata, response=self.call_action_server(userdata, aa,personality)
            if response:
                f.write("----------------------\n")
                string_log="before PERCEPTION: " + pi+ "\n"
                f.write(string_log)
                string_log="UNSC ACTION: " + aa +"--------------"+personality+ " reward: " +str(rew)+ "\n"
                f.write(string_log)
                #exec
                string_log="before consc level: " + str(function_objects["scrupulousness_level"].has_value)+ "\n"
                f.write(string_log)
                change_raward("reward_c",float(rew))
                return "outcome9"
            else:
                return "outcome8"


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
            
            
            #time.sleep(10)
            userdata, response=self.call_action_server(userdata, ac,personality)
            if response:
                return "outcome9"
            else:
                return "outcome8"


    def call_action_server(self, userdata, ac,personality):
            userdata.state="exec"
            resp, mmap, to_exec_action, exec_personality = dispatch_action(ac, personality)
            string_long="********************EXECUTING ACTION\n"+str(mmap)+"\n"+to_exec_action+"\n"+exec_personality+"\n"
            f1.write(string_long)
            if resp==False:
                    print('Action Failed')        
                    f.write("ACTION FAIL\n")
                    return userdata, False
            else:
                    ac=userdata.executing_actions.pop(0)
                    print('Action executed: '+ac)
                    userdata.action=ac
                    userdata.updated_actions=userdata.executing_actions
            return userdata,True

                
        
class CheckPerc(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome3',"outcome4","outcome2"],
                             input_keys=["state","exec_actions","action"])
        
    def execute(self, userdata):
        global emotion, new_emotion, new_sentence, data
        print('check perception') 
        data["update"]="True"
        resp=requests.put(url+'get_input', json=data, headers=headers)
        print(data)
        if eval(resp.text)["new_emotion"]=="True":
            new_emotion=True
            emotion=eval(resp.text)["emotion"]
        if eval(resp.text)["new_sentence"]=="True":
            new_sentence=True
        while (new_emotion==False and new_sentence==False and userdata.action==""):
            time.sleep(1)
            data["update"]="True"
            resp=requests.put(url+'get_input', json=data, headers=headers)
            print(data)
            if eval(resp.text)["new_emotion"]=="True":
                new_emotion=True
                emotion=eval(resp.text)["emotion"]
            if eval(resp.text)["new_sentence"]=="True":
                new_sentence=True
        #IF I HAVE NO NEW PERCEPTION IT MEANS THAT I COME FROM THE PREVIOUS ACTION
        if new_emotion==False and new_sentence==False:
            if "ACTION" in userdata.action:
                return "outcome3" #if I have done a trait specific action I need to replan
            
            if userdata.state=="exec":
                f.write("Action fail need replanning\n")
                return "outcome3"
            
            else:
                if userdata.exec_actions==[]:
                    f.write("task finished \n")
                    return "outcome4"
                else:
                    f.write("executing next action \n")
                    return "outcome2"
        #IF NEW PERCEPTION
        else:
            string_long="********************NEW PERCEPTION\n"
            if new_emotion:
               new_emotion=False
               emotion_pred=perception_predicate_map[emotion]["emotion"]
               goals=perception_predicate_map[emotion]["goals"]
               add_predicate(emotion_pred)
               string_long=string_long+"perceived emotion: "+emotion+"\n"
               for g in goals:
                    add_goal(g)#state that that predicate is a goal
                    remove_predicate(g) #now the goal predicate is not grounded
               
            if new_sentence:
                add_goal("answered")
                add_goal("finished")
                remove_predicate("answered")
                remove_predicate("finished")
                add_predicate("new_sentence")
                string_long=string_long+"User say a sentence\n"
                new_sentence=False
            add_goal("feel_comfort")
            remove_predicate("feel_comfort")
            f1.write(string_long)
            return "outcome3"

        
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
                             outcomes=['outcome10'],
                             input_keys=['action'],
                             output_keys=['state',"out_action"])
        
    def execute(self, userdata):
        print('Update_ontology')
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
        return 'outcome10'
    

class Finish(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             input_keys=['input_goals'],
                             outcomes=['outcome11','outcome12'],
                             )
        
    def execute(self,userdata):
        if userdata.input_goals!=[]:
            print('Passing to the next goal')
            return "outcome11"
        else:
            f.close()
            f1.close()
            print('Finishhh')
            return 'outcome12'




def main():
    try:
        sm = smach.StateMachine(outcomes=['outcome13'])
        sm.userdata.goals=problem_goals
        sm.userdata.path_domain=""
        sm.userdata.path_problem=""
        sm.userdata.path_init_problem=""
        sm.userdata.command_start=""
        sm.userdata.folder =""
        sm.userdata.path_plan =""
        sm.userdata.actions =[]
        sm.userdata.a=""
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
                                            },
                                remapping={
                                    "action":"a",
                                    "state":"previous_state",
                                    "exec_actions":"actions"
                                        })
            
            smach.StateMachine.add('WRITE_PLAN', WriteProblem(), 
                        transitions={'outcome5':'PLAN'},
                        remapping={'pb_path':'path_problem'
                                            })
            
            smach.StateMachine.add('UPDATE_ONTOLOGY', UpdateOntology(), 
                        transitions={'outcome10':'CHECK_PERC',
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

     
        outcome = sm.execute()
        
    

    except:
        print("interrupt")

if __name__ == '__main__':
      main()



    