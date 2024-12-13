#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from load_ontology import *
#from problem_param_vm import *
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
import datetime
#define the actual personality
traits=["Extrovert","Introvert","Conscientious","Unscrupolous","Agreeable","Disagreeable"]
traits_preds=["(extro)","(intro)","(consc)","(unsc)","(agree)","(disagree)"]
we=1
wi=0
wc=0
wu=0
wa=0
wd=0
sum_weights=0
weights=[]
gamma=1
emotion="N"
attention="NA"
sentence=""
start=True
new_emotion=False
new_sentence=False
new_attention=False
human_present=False
start_proactivity=False
person=""
begin=True

url='http://127.0.0.1:5021/'

data={
        "new_sentence":"False",
        "new_emotion":"False",
        "new_attention":"False",
        "attention":"negative",
        "emotion":"",
        "sentence":"",
        "listening":"False",
        "human_present":"False",
        "start_proactivity":"False",
        "person":""
}


emotion_mask={
    "A":[4,2,3,1,5,5],
    "H":[4,2,1,1,5,5],
    "SA":[2,2,1,1,5,2],
    "SU":[4,2,1,1,5,5],
    "N":[4,4,1,1,4,4],
}



class State_Start(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome0'],
                             input_keys=['input_goals',],
                             output_keys=['output_goals','domain_path','problem_path','init_pb','command','path','plan_path'])
        
    def execute(self, userdata):
        global wa,wd,we,wi,wc,wd,sum_weights,weights
        goals=userdata.input_goals
        #actual_goal=goals.pop(0) #always goal1
        print('Executing goal: '+ actual_goal)
        dict_goal=goals_dict[actual_goal]
        userdata.output_goals=goals
        userdata.domain_path=dict_goal["domain"]
        userdata.problem_path=dict_goal["problem"]
        userdata.init_pb=dict_goal["init"]
        userdata.command=dict_goal["command"]
        userdata.path=dict_goal["folder"]
        userdata.plan_path=dict_goal["plan"]
        sum_weights=float(we +wi +wc + wu + wa + wd)
        try: 
                weights=[we/sum_weights,wi/sum_weights,wc/sum_weights,wu/sum_weights,wa/sum_weights,wd/sum_weights]
        except:
                weights=6*[0]
                sum_weights=1

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
        print('Reading domain and populate ontology')
        populate_ontology(userdata.domain_path)
        print('Initialize function and predicates in the ontology')
        initialize_functions_predicates()
        print('Read the problem and set the initial values of predicates and functions')
        read_the_problem(userdata.problem_path)  
        return 'outcome1'
      

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
                             output_keys=['updated_actions','action','state']) 
    def execute(self, userdata):
        global new_emotion, emotion, new_sentence, sentence, new_attention, attention
        
        personality=np.random.choice(traits,p=weights)
        ac=userdata.executing_actions[0]
        
        if ac=="EXTRO_ACTION":
            resp = requests.get(url+'get_perception', params=data)
            emotion=eval(resp.text)["emotion"]
            if emotion not in list_of_emotions:
                    emotion="N"
            if eval(resp.text)["attention"]=="positive":
                pi="A_"+map_emotion_AV_axis[emotion]
            else:
                pi="NA_"+map_emotion_AV_axis[emotion]
            file_data = initialize_or_load_person(person)
            
            chosen_action, weight = choose_action_e(file_data, pi)
            print(f"Chosen action: {chosen_action} with weight {weight}")

        

            userdata, response, ea  =self.call_action_server(userdata, chosen_action, personality)
            if response:
                resp = requests.get(url+'get_perception', params=data)
                emotion=eval(resp.text)["emotion"]
                if emotion not in list_of_emotions:
                    emotion="N"
                if eval(resp.text)["attention"]=="positive":
                    pn="A_"+map_emotion_AV_axis[emotion]
                else:
                    pn="NA_"+map_emotion_AV_axis[emotion]

                file_data, rr = update_weights_e(file_data, chosen_action, pi, pn)
                save_person_data(person, file_data)
                change_raward("reward_e",float(rr))
                return "outcome9"
            else:
                return "outcome8"

        else:
            resp = requests.get(url+'get_perception', params=data)
            em=eval(resp.text)["emotion"]
            if em!="":
                emotion=em
            userdata, response, ea =self.call_action_server(userdata, ac, personality)
            if "react" in ea:
                return 'outcome9'
            if response:
                return "outcome9"
            else:
                return "outcome8"


    def call_action_server(self, userdata, ac, personality):
            global data_action, emotion, sentence 
            userdata.state="exec"
            #get the comfortability
            mask_weights=emotion_mask[emotion]
            emotion_weights=np.multiply(mask_weights, weights)
            
            sum_em_weights=0
            for ew in emotion_weights:
                sum_em_weights+=ew

            
            ind=0
            for ew in emotion_weights:
                emotion_weights[ind]=ew/sum_em_weights
                ind+=1

            
            personality_emotions=np.random.choice(traits,p=emotion_weights)
            print("personality emotion: "+personality_emotions)
            if personality_emotions=="Agreeable" or personality_emotions=="Disagreeable":
                comfortability = function_objects["agreeableness_level"].has_value
                
            elif personality_emotions=="Extrovert" or personality_emotions=="Introvert":
                comfortability = function_objects["interaction_level"].has_value
            elif personality_emotions=="Unscrupolous" or personality_emotions=="Conscientious":
                comfortability = function_objects["scrupulousness_level"].has_value
            else:
                print("no personality found")
                comfortability= 1
            
            if comfortability> 5:
                comfortability= "positive"

            else:
                comfortability = "negative"

            
            resp, to_exec_action = dispatch_action(ac, personality, personality_emotions, emotion, sentence, comfortability, weights)
            
            resp2=True
            #if ("react" not in to_exec_action) and ("compute" not in to_exec_action) and ("check" not in to_exec_action):
                #change_raward("react",float(1))
                
            
            if resp2==False:
                    print('Action Failed')        
                    return userdata, False, to_exec_action
            else:
                    ac=userdata.executing_actions.pop(0)
                    print('Action executed: '+ac)
                    userdata.action=ac
                    userdata.updated_actions=userdata.executing_actions

            return userdata,True, to_exec_action

                
        
class CheckPerc(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome3',"outcome4","outcome2"],
                             input_keys=["state","exec_actions","action"],
                             output_keys=["out_action"])
        
    def execute(self, userdata):
        global emotion, new_emotion, new_sentence, data, new_attention, attention, sentence, human_present, start_proactivity, person
        resp = requests.get(url+'get_perception', params=data)
        
    
        a=userdata.action
        print("action",a)

        if eval(resp.text)["new_emotion"]=="True":
            new_emotion=True
            emotion=eval(resp.text)["emotion"]
            
        if eval(resp.text)["new_sentence"]=="True":
            new_sentence=True
            sentence=eval(resp.text)["sentence"]

        if eval(resp.text)["new_attention"]=="True":
            new_attention=True
            attention=eval(resp.text)["attention"]

        if eval(resp.text)["human_present"]=="True":
            human_present=True
        else:
            if person!="":
                self.remove_person(person)
                person=""
            

        if eval(resp.text)["start_proactivity"]=="True":
            start_proactivity=True
            person=eval(resp.text)["person"]

        """
        while (new_emotion==False and new_sentence==False and  new_attention==False and userdata.action==""):
            time.sleep(1)
            resp=requests.put(url+'get_input', json=data, headers=headers)

            while eval(resp.text)["listening"]=="True":
                time.sleep(0.5)
                print("listening ...")
                resp=requests.put(url+'get_input', json=data, headers=headers)

            if eval(resp.text)["new_emotion"]=="True":
                new_emotion=True
                emotion=eval(resp.text)["emotion"]
                
            if eval(resp.text)["new_sentence"]=="True":
                new_sentence=True
                sentence=eval(resp.text)["sentence"]

            if eval(resp.text)["new_attention"]=="True":
                new_attention=True
                attention=eval(resp.text)["attention"]
                
        """
        #IF I HAVE NO NEW PERCEPTION IT MEANS THAT I COME FROM THE PREVIOUS ACTION
        if new_emotion==False and new_sentence==False and new_attention==False and start_proactivity==False:
            if userdata.state=="exec": #action fail
                
                return "outcome3"
            
            else: #pass to the next action
                if userdata.exec_actions==[]:
                   
                    return "outcome4"
                else:
                    return "outcome2"
        #IF NEW PERCEPTION
        else:
            if new_emotion:
               new_emotion=False
               emotion_pred=perception_predicate_map[emotion]["emotion"]
               goals=perception_predicate_map[emotion]["goals"]
               add_predicate(emotion_pred)
              
               for g in goals:
                    add_goal(g)#state that that predicate is a goal
                    remove_predicate(g) #now the goal predicate is not grounded

            if new_attention:
                new_attention=False
                if attention=="positive":
                    add_predicate("attention")
                    add_goal("attention_r") 
                    remove_predicate("attention_r")  
                else:
                    add_predicate("low_attention")
                    add_goal("low_attention_r") 
                    remove_predicate("low_attention_r")  

            if new_sentence:
                add_goal("answered")
                remove_predicate("answered")
                add_predicate("new_sentence")
                
                remove_predicate("finished_sentence")
                add_goal("finished_sentence")
                remove_goal("finished")
                new_sentence=False

            if start_proactivity:
                start_proactivity=False
                self.add_person(person)
                remove_predicate("welcomed")
                remove_predicate("finished")
                remove_goal("finished_sentence")
                add_goal("finished")


            return "outcome3"
        

    def add_person(self, name):
        objects_objects[name]=Objects(name)
        objects_objects[name].has_type=[types_objects["person"]]
        predicates_objects["person_present"].is_grounded=True
        predicates_objects["person_present"].has_object.append(objects_objects[name])
        predicates_objects["person_there"].is_grounded=True
        predicates_objects["person_there"].has_object=[]
        predicates_objects["person_there"].has_object.append(objects_objects[name])


    def remove_person(self, name):
        remove_predicate("person_there")
        predicates_objects["person_there"].has_object.remove(objects_objects[name])
        add_predicate("finished")
        
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
                             outcomes=['outcome10','outcome11'],
                             input_keys=['action'],
                             output_keys=['state',"out_action"])
        
    def execute(self, userdata):
        print('Update_ontology')
        acc=userdata.action
        update_ontology(userdata.action)
        userdata.state="update"
        initialize_reward()
        userdata.out_action=acc
        print(acc)
        if "REACT" in acc:
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
        sm.userdata.a="start"
        sm.userdata.previous_state=""
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
                                    "exec_actions":"actions",
                                    "out_action":"a"
                                        })
            
            smach.StateMachine.add('WRITE_PLAN', WriteProblem(), 
                        transitions={'outcome5':'PLAN'},
                        remapping={'pb_path':'path_problem'
                                            })
            
            smach.StateMachine.add('UPDATE_ONTOLOGY', UpdateOntology(), 
                        transitions={'outcome10':'CHECK_PERC',
                                     'outcome11':'EXEC',
                                    },
                        remapping={'action':'a',
                                   "previous_state":"state",
                                   "a":"out_action"
                                })

            smach.StateMachine.add('FINISH', Finish(), 
                        transitions={'outcome11':'CHECK_PERC',
                                     'outcome12':'outcome13'},
                        remapping={
                            "input_goals":"goals",
                            "out_action":"a",
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



    
