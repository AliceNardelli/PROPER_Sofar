#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

from action_dispatcher import *
import random
import numpy as np
import time
import threading
import datetime
from client_proper import ClientProper

#define the actual personality
traits=["Extrovert","Introvert","Conscientious","Unscrupolous","Agreeable","Disagreeable"]
we=0
wi=1
wc=0
wu=0
wa=0
wd=0
start_new_session=True
sum_weights=0
weights=[]
gamma=1
emotion="Neutral"
attention="NA"
sentence=""
start=True
new_emotion=False
new_sentence=False
new_attention=False
human_present=False
start_proactivity=False
detected_main_info=False 
detected_preferred_activities=False

person=""
begin=True

client_proper=ClientProper()

emotion_mask={
    "A":[4,2,3,1,5,5],
    "H":[4,2,1,1,5,5],
    "S":[2,2,1,1,5,2],
    "C":[4,4,1,1,5,5],
    "N":[4,4,1,1,4,4],
}

def append_to_file(value, action):
    filename="comfortability.txt"
    with open(filename, "a") as file:
        file.write(str(value) +" "+ action +"\n")
    print(f"Appended: {value}")

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
        #posting personality
        tt=["Extrovert","Introvert","Conscientious","Distracted","Agreeable","Disagreeable"]
        for i in range(len(weights)):
                if weights[i]!=0:
                        client_proper.post_personality(tt[i])
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
        if start_new_session:   
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
        else:
            # Read dictionary from a JSON file
            with open("/home/alice/PROPER_Sofar/proper_reasoning/data.json", "r") as file:
                person_dict = json.load(file)
            print("Dictionary loaded from data.json:")
            print(person_dict)


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
                             outcomes=['outcome8','outcome9'],
                             input_keys=['executing_actions'],
                             output_keys=['updated_actions','action','state']) 
    def execute(self, userdata):
        global new_emotion, emotion, new_sentence, sentence, new_attention, attention
        
        personality=np.random.choice(traits,p=weights)
        try:
            ac=userdata.executing_actions[0]
        except:
            userdata.updated_actions=[]
            userdata.action="start"
            return "outcome8"
        
        if ac=="EXTRO_ACTION":
            
            emotion=client_proper.get_user_last_emotion()
            print(emotion)
            if emotion not in list_of_emotions:
                    emotion="Neutral"
            pi = "A_" # if eval(resp.text)["attention"] == "positive" else "NA_"
            pi += "N" if map_emotion_AV_axis[emotion] == "C" else map_emotion_AV_axis[emotion]
            file_data = initialize_or_load_person_e(person)
            
            chosen_action, weight = choose_action_e(file_data, pi)
            print(f"Chosen action: {chosen_action} with weight {weight}")
            userdata, response, ea  =self.call_action_server(userdata, chosen_action, personality)
            if response:
                emotion=client_proper.get_user_last_emotion()
                print(emotion)
                if emotion not in list_of_emotions:
                    emotion="Neutral"
                pn = "A_" # if eval(resp.text)["attention"] == "positive" else "NA_"
                pn += "N" if map_emotion_AV_axis[emotion] == "C" else map_emotion_AV_axis[emotion]

                file_data, rr = update_weights_e(file_data, chosen_action, pi, pn)
                save_person_data_e(person, file_data)
                change_raward("reward_e",float(rr))
                return "outcome9"
            else:
                return "outcome8"
            


        if ac=="INTRO_ACTION":
            emotion=client_proper.get_user_last_emotion()
            if emotion not in list_of_emotions:
                    emotion="Neutral"
            pi = "A_" # if eval(resp.text)["attention"] == "positive" else "NA_"
            pi += "N" if map_emotion_AV_axis[emotion] == "C" else map_emotion_AV_axis[emotion]
            file_data = initialize_or_load_person_i(person)
            
            chosen_action, weight = choose_action_i(file_data, pi)
            print(f"Chosen action: {chosen_action} with weight {weight}")
            userdata, response, ea  =self.call_action_server(userdata, chosen_action, personality)
            if response:
                emotion=client_proper.get_user_last_emotion()
                if emotion not in list_of_emotions:
                        emotion="Neutral"
                pn = "A_" #if eval(resp.text)["attention"] == "positive" else "NA_"
                pn += "N" if map_emotion_AV_axis[emotion] == "C" else map_emotion_AV_axis[emotion]

                file_data, rr = update_weights_i(file_data, chosen_action, pi, pn)
                save_person_data_i(person, file_data)
                change_raward("reward_e",float(rr))
                return "outcome9"
            else:
                return "outcome8"


        elif ac=="DISAGREE_ACTION":
            emotion=client_proper.get_user_last_emotion()
            if emotion not in list_of_emotions:
                    emotion="Neutral"
            pi = "A_" #if eval(resp.text)["attention"] == "positive" else "NA_"
            pi += "N" if map_emotion_AV_axis[emotion] == "C" else map_emotion_AV_axis[emotion]
            file_data = initialize_or_load_person_d(person)
            
            chosen_action, weight = choose_action_d(file_data, pi)
            print(f"Chosen action: {chosen_action} with weight {weight}")
            userdata, response, ea  =self.call_action_server(userdata, chosen_action, personality)
            if response:
                emotion=client_proper.get_user_last_emotion()
                if emotion not in list_of_emotions:
                        emotion="Neutral"
                pn = "A_" # if eval(resp.text)["attention"] == "positive" else "NA_"
                pn += "N" if map_emotion_AV_axis[emotion] == "C" else map_emotion_AV_axis[emotion]

                file_data, rr = update_weights_d(file_data, chosen_action, pi, pn)
                save_person_data_d(person, file_data)
                change_raward("reward_a",float(rr))
                return "outcome9"
            else:
                return "outcome8"
            

        elif ac=="AGREE_ACTION":
            emotion=client_proper.get_user_last_emotion()
            if emotion not in list_of_emotions:
                    emotion="Neutral"
            pi = "A_" #if eval(resp.text)["attention"] == "positive" else "NA_"
            pi += "N" if map_emotion_AV_axis[emotion] == "C" else map_emotion_AV_axis[emotion]
            file_data = initialize_or_load_person_a(person)
            
            chosen_action, weight = choose_action_a(file_data, pi)
            print(f"Chosen action: {chosen_action} with weight {weight}")
            userdata, response, ea  =self.call_action_server(userdata, chosen_action, personality)
            if response:
                emotion=client_proper.get_user_last_emotion()
                if emotion not in list_of_emotions:
                        emotion="Neutral"
                pn = "A_" #if eval(resp.text)["attention"] == "positive" else "NA_"
                pn += "N" if map_emotion_AV_axis[emotion] == "C" else map_emotion_AV_axis[emotion]

                file_data, rr = update_weights_a(file_data, chosen_action, pi, pn)
                save_person_data_a(person, file_data)
                change_raward("reward_a",float(rr))
                return "outcome9"
            else:
                return "outcome8"        


        elif ac=="CONSC_ACTION":
            emotion=client_proper.get_user_last_emotion()
            if emotion not in list_of_emotions:
                    emotion="Neutral"
            pi = "A_" # if eval(resp.text)["attention"] == "positive" else "NA_"
            pi += "N" if map_emotion_AV_axis[emotion] == "C" else map_emotion_AV_axis[emotion]
            file_data = initialize_or_load_person_c(person)
            
            chosen_action, weight = choose_action_c(file_data, pi)
            print(f"Chosen action: {chosen_action} with weight {weight}")
            userdata, response, ea  =self.call_action_server(userdata, chosen_action, personality)
            if response:
                emotion=client_proper.get_user_last_emotion()
                if emotion not in list_of_emotions:
                        emotion="Neutral"
                pn = "A_" #if eval(resp.text)["attention"] == "positive" else "NA_"
                pn += "N" if map_emotion_AV_axis[emotion] == "C" else map_emotion_AV_axis[emotion]
                file_data, rr = update_weights_c(file_data, chosen_action, pi, pn)
                save_person_data_c(person, file_data)
                change_raward("reward_c",float(rr))
                return "outcome9"
            else:
                return "outcome8"
            


        elif ac=="UNSC_ACTION":
            emotion=client_proper.get_user_last_emotion()
            if emotion not in list_of_emotions:
                    emotion="Neutral"
            pi = "A_" #if eval(resp.text)["attention"] == "positive" else "NA_"
            pi += "N" if map_emotion_AV_axis[emotion] == "C" else map_emotion_AV_axis[emotion]
            file_data = initialize_or_load_person_u(person)
            
            chosen_action, weight = choose_action_u(file_data, pi)
            print(f"Chosen action: {chosen_action} with weight {weight}")
            userdata, response, ea  =self.call_action_server(userdata, chosen_action, personality)
            if response:
                change_raward("reward_c",float(weight))
                return "outcome9"
            else:
                return "outcome8"
            

        else:
            em=client_proper.get_user_last_emotion()
            if em not in list_of_emotions:
                    em="Neutral"
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
            mask_weights=emotion_mask[map_emotion_AV_axis[emotion]]
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

            print("BEFORE EXECUTING: ", ac)
            resp, to_exec_action = dispatch_action(ac, personality, personality_emotions, emotion, sentence, comfortability, weights)
            
            #resp2=True
            #if ("react" not in to_exec_action) and ("compute" not in to_exec_action) and ("check" not in to_exec_action):
                #change_raward("react",float(1))
                
            
            if resp==False:
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
        global emotion, new_emotion, new_sentence, new_attention, attention, sentence, human_present, start_proactivity, person
        time.sleep(1)
        speaking = client_proper.get_speaking()
        while speaking:
            print("LISTENING")
            speaking= client_proper.get_speaking()
            time.sleep(0.5)

        
        new_sentence, new_emotion, new_attention, attention, emotion, sentence, human_present, start_proactivity, new_person_index, detected_main_info, detected_preferred_activities =client_proper.get_user_input()
        print(new_sentence, new_emotion, new_attention, attention, emotion, sentence, human_present, start_proactivity, new_person_index, detected_main_info, detected_preferred_activities)
        
        a=userdata.action
        print("action",a)
        try:
            if not human_present:
                if not detected_main_info:
                    if not new_emotion:
                        if not detected_preferred_activities:
                            print("REMOVING PERSON ",person)
                            self.remove_person(person)
                            person=""
        except:
            print("before beginning")
            
        if (detected_main_info) and (objects_objects[person] in predicates_objects["detected_main_info"].has_object):
                detected_main_info=False
        
        if (detected_preferred_activities) and (objects_objects[person] in predicates_objects["detected_preferred_activities"].has_object):
                detected_preferred_activities=False
   
        if human_present:
            if new_person_index in person_dict:
                    person=person_dict[new_person_index]  
                
        #IF I HAVE NO NEW PERCEPTION IT MEANS THAT I COME FROM THE PREVIOUS ACTION
        if new_emotion==False and new_sentence==False and new_attention==False and start_proactivity==False and human_present==False and detected_main_info==False and detected_preferred_activities==False:
            if userdata.state=="exec": #action fail
                
                return "outcome3"
            
            else: #pass to the next action
                if userdata.exec_actions==[]:
                   
                    return "outcome4"
                else:
                    return "outcome2"
                
        #IF NEW PERCEPTION
        else:
            if human_present:
                if not (new_person_index in person_dict):
                    person_dict[new_person_index]="a"+str(person_dict["counter_person"])
                    person_dict["counter_person"]=person_dict["counter_person"]+1
                    person=person_dict[new_person_index]
                    self.add_person_object(person)
                    with open("/home/alice/PROPER_Sofar/proper_reasoning/data.json", "w") as file:
                        json.dump(person_dict, file, indent=4)

            if new_emotion:
               new_emotion=False
               if emotion not in list_of_emotions:
                    emotion="Neutral"
               emotion_pred=perception_predicate_map[map_emotion_AV_axis[emotion]]["emotion"]
               goals=perception_predicate_map[map_emotion_AV_axis[emotion]]["goals"]
               remove=perception_predicate_map[map_emotion_AV_axis[emotion]]["remove"]
               add_predicate(emotion_pred)
               for r in remove:
                    remove_goal(r)              
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
                new_sentence=False

            if detected_main_info:
                print("DETECTED MAIN INFO")
                add_predicate("detected_main_info")
                if objects_objects[person] not in predicates_objects["detected_main_info"].has_object: 
                    predicates_objects["detected_main_info"].has_object.append(objects_objects[person])
               

            if detected_preferred_activities:
                print("DETECTED PREFERRED")
                add_predicate("detected_preferred_activities")
                if objects_objects[person] not in predicates_objects["detected_preferred_activities"].has_object:
                    predicates_objects["detected_preferred_activities"].has_object.append(objects_objects[person])

            if start_proactivity or human_present:
                if start_proactivity:
                    self.add_person(person)    
                    print("------------------------")
                    print("START PROACTIVITY")
                    print("------------------------")
                
                
                #remove_predicate("welcomed")
                remove_goal("finished_sentence")
                print("OBJ OBJ1: ", predicates_objects["detected_main_info"].has_object)
                print("OBJ OBJ2: ", predicates_objects["detected_preferred_activities"].has_object)
                if objects_objects[person] not in predicates_objects["detected_main_info"].has_object:
                    if start_proactivity:
                        if objects_objects[person] in predicates_objects["ask_to_present"].has_object:
                            predicates_objects["ask_to_present"].has_object.remove(objects_objects[person])
                            if predicates_objects["ask_to_present"].has_object==[]:
                                remove_predicate("ask_to_present")
                            predicates_objects["greetings"].has_object.append(objects_objects[person])
                            if not predicates_objects["greetings"].is_grounded:
                                predicates_objects["greetings"].is_grounded=True
                            print("removedddddd")
                    remove_predicate("waited1")
                    add_goal("waited1")
                    
                    

                elif objects_objects[person] not in predicates_objects["detected_preferred_activities"].has_object:
                    if start_proactivity:
                        if objects_objects[person] in predicates_objects["ask_preferred_activities"].has_object:
                            predicates_objects["ask_preferred_activities"].has_object.remove(objects_objects[person])
                            if predicates_objects["ask_preferred_activities"].has_object==[]:
                                remove_predicate("ask_preferred_activities")
                            predicates_objects["ask_to_present"].has_object.append(objects_objects[person])
                            if not predicates_objects["ask_to_present"].is_grounded:
                                predicates_objects["ask_to_present"].is_grounded=True
                            print("removedddddd")

                    remove_predicate("waited1")
                    remove_goal("waited1")
                    remove_predicate("waited2")
                    add_goal("waited2")
                    
                else:
                    if start_proactivity:
                        if objects_objects[person] in predicates_objects["information_suggested"].has_object:
                            
                            predicates_objects["information_suggested"].has_object.remove(objects_objects[person])
                            if predicates_objects["information_suggested"].has_object==[]:
                                remove_predicate("information_suggested")
                            predicates_objects["ask_preferred_activities"].has_object.append(objects_objects[person])
                            if not predicates_objects["ask_preferred_activities"].is_grounded:
                                predicates_objects["ask_preferred_activities"].is_grounded=True
                            print("removedddddd")

                    remove_predicate("waited2")
                    remove_goal("waited2")
                    remove_predicate("finished")
                    add_goal("finished")
                start_proactivity=False 
                human_present=False   
            return "outcome3"
        

    def add_person_object(self, name):
        objects_objects[name]=Objects(name)
        objects_objects[name].has_type=[types_objects["person"]]
        predicates_objects["person_present"].is_grounded=True
        predicates_objects["person_present"].has_object.append(objects_objects[name])


    def add_person(self, name):
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
        global we, wi, wa, wd, wc, wu
        print('Update_ontology')
        acc=userdata.action
        update_ontology(userdata.action)
        userdata.state="update"
        initialize_reward()
        userdata.out_action=acc
        print(acc)
        if we!=0 or wi!=0:
            append_to_file(function_objects["interaction_level"].has_value, acc)
        elif wc!=0 or wu!=0:
            append_to_file(function_objects["scrupulousness_level"].has_value, acc)
        elif wd!=0 or wa!=0:
            append_to_file(function_objects["agreeableness_level"].has_value, acc)
        #if "REACT" in acc:
            #return 'outcome11'
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



    
