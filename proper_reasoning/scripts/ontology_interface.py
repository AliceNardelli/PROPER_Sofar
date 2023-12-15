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
wu=0
wa=0
wd=0
sum_weights=0
weights=[]
gamma=1
emotion=""
attention=""
start=True
new_emotion=False
new_sentence=False
new_attention=False
url='http://127.0.0.1:5020/'
url1='http://127.0.0.1:5019/'
url2='http://127.0.0.1:5018/'
url3='http://127.0.0.1:5021/'

headers= {'Content-Type':'application/json'}


data={
        "emotion":"",
        "new_sentence":"False",
        "new_emotion":"False",
        "new_attention":"False",
        "attention":"negative",
        "update":"False",
}


data_personality={
        "new_personality":"False",
        "Extrovert":0,
        "Introvert":0,
        "Agreeable":0,
        "Disagreeable":0,
        "Conscientious":0,
        "Unscrupolous":0,
}

data_restart={
    "restart":"False"
}

data_action={
        "action":"",
        "language":"",
        "personality":"",
        "pitch":"",
        "volume":"",
        "velocity":"",
        "new_action":"",
        "executed":"",
        "result":""

}

class State_Start(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome0'],
                             input_keys=['input_goals',],
                             output_keys=['output_goals','domain_path','problem_path','init_pb','command','path','plan_path'])
        
    def execute(self, userdata):
        global wa,wd,we,wi,wc,wd,sum_weights,weights, data, start
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
        print("setting new personality")
        if start==True:
            resp=requests.put(url1+'get_personality', json=data_personality, headers=headers)
            new_personality=False
            if  eval(resp.text)["new_personality"]=="True":
                new_personality=True
            while new_personality==False:
                time.sleep(1)
                resp=requests.put(url1+'get_personality', json=data_personality, headers=headers)
                if  eval(resp.text)["new_personality"]=="True":
                    new_personality=True
            start=False
            reset=True
        
        else:
            time.sleep(3)
            resp=requests.put(url1+'get_personality', json=data_personality, headers=headers)
            if  eval(resp.text)["new_personality"]=="True":
                reset=True
            else: 
                reset=False

        if reset==True:
            wi=float( eval(resp.text)["Introvert"])
            we=float( eval(resp.text)["Extrovert"])
            wa=float( eval(resp.text)["Agreeable"])
            wd=float( eval(resp.text)["Disagreeable"])
            wc=float( eval(resp.text)["Conscientious"])
            wu=float( eval(resp.text)["Unscrupolous"])
            sum_weights=we +wi +wc + wu + wa + wd
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
        return 'outcome7'
    
class ExAction(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome8','outcome9','outcome13'],
                             input_keys=['executing_actions'],
                             output_keys=['updated_actions','action','state']) 
    def execute(self, userdata):
        global new_emotion, emotion, new_sentence, start
        resp=requests.put(url2+'get_restart', json=data_restart, headers=headers)
        if eval(resp.text)["restart"]=="True":
            print("restart")
            userdata.action=""
            start=True
            return 'outcome13'
        resp=requests.put(url2+'get_restart', json=data_restart, headers=headers)
      
        personality=np.random.choice(traits,p=weights)
        ac=userdata.executing_actions[0]

        if ac=="AGREE_ACTION":
            data["update"]="False"
            resp=requests.put(url+'get_input', json=data, headers=headers)
            emotion=eval(resp.text)["emotion"]
            if emotion not in list_of_emotions:
                    emotion="N"
            if  eval(resp.text)["attention"]=="positive":
                pi="A_"+map_emotion_AV_axis[emotion]
            else:
                pi="NA_"+map_emotion_AV_axis[emotion]
            if predicates_objects["new_sentence"].is_grounded==True:
                aa,rew=choose_action_a(pi,False)
            else:
                aa,rew=choose_action_a(pi,False)
            userdata, response=self.call_action_server(userdata, aa, personality)
            if response:
                data["update"]="False"
                resp=requests.put(url+'get_input', json=data, headers=headers)
                emotion=eval(resp.text)["emotion"]
                if emotion not in list_of_emotions:
                    emotion="N"
                if eval(resp.text)["attention"]=="positive":
                    pn="A_"+map_emotion_AV_axis[emotion]
                else:
                    pn="NA_"+map_emotion_AV_axis[emotion]
                rr=update_weights_a(aa,pi,pn) #qui in ogni caso avrò una new perception
                change_raward("reward_a",float(rr))
                return "outcome9"
            else:
                return "outcome8"

        
        if ac=="DISAGREE_ACTION":
            data["update"]="False"
            resp=requests.put(url+'get_input', json=data, headers=headers)
            emotion=eval(resp.text)["emotion"]
            if emotion not in list_of_emotions:
                    emotion="N"
            if eval(resp.text)["attention"]=="positive":
                pi="A_"+map_emotion_AV_axis[emotion]
            else:
                pi="NA_"+map_emotion_AV_axis[emotion]
            if predicates_objects["new_sentence"].is_grounded==True:
                aa,rew=choose_action_d(pi,False)
            else:
                aa,rew=choose_action_d(pi,False)
            userdata, response=self.call_action_server(userdata, aa, personality)
            if response:
                data["update"]="False"
                resp=requests.put(url+'get_input', json=data, headers=headers)
                emotion=eval(resp.text)["emotion"]
                if emotion not in list_of_emotions:
                    emotion="N"
                if eval(resp.text)["attention"]=="positive":
                    pn="A_"+map_emotion_AV_axis[emotion]
                else:
                    pn="NA_"+map_emotion_AV_axis[emotion]
                rr=update_weights_d(aa,pi,pn) #qui in ogni caso avrò una new perception
                change_raward("reward_a",float(rr))
                return "outcome9"
            else:
                return "outcome8"

            
        elif ac=="INTRO_ACTION":
            data["update"]="False"
            resp=requests.put(url+'get_input', json=data, headers=headers)
            emotion=eval(resp.text)["emotion"]
            if emotion not in list_of_emotions:
                    emotion="N"
            if eval(resp.text)["attention"]=="positive":
                pi="A_"+map_emotion_AV_axis[emotion]
            else:
                pi="NA_"+map_emotion_AV_axis[emotion]
            if predicates_objects["new_sentence"].is_grounded==True:
                aa,rew=choose_action_i(pi,False)
            else:
                aa,rew=choose_action_i(pi,False)
            userdata, response=self.call_action_server(userdata, aa, personality)
            if response:
                data["update"]="False"
                resp=requests.put(url+'get_input', json=data, headers=headers)
                emotion=eval(resp.text)["emotion"]
                if emotion not in list_of_emotions:
                    emotion="N"
                if eval(resp.text)["attention"]=="positive":
                    pn="A_"+map_emotion_AV_axis[emotion]
                else:
                    pn="NA_"+map_emotion_AV_axis[emotion]
                rr=update_weights_i(aa,pi,pn) #qui in ogni caso avrò una new perception
                change_raward("reward_e",float(rr))
                return "outcome9"
            else:
                return "outcome8"
            

           


        elif ac=="EXTRO_ACTION":
            data["update"]="False"
            resp=requests.put(url+'get_input', json=data, headers=headers)
            emotion=eval(resp.text)["emotion"]
            if emotion not in list_of_emotions:
                    emotion="N"
            if eval(resp.text)["attention"]=="positive":
                pi="A_"+map_emotion_AV_axis[emotion]
            else:
                pi="NA_"+map_emotion_AV_axis[emotion]
            if predicates_objects["new_sentence"].is_grounded==True:
                aa,rew=choose_action_e(pi,False)
            else:
                aa,rew=choose_action_e(pi,False)
            userdata, response=self.call_action_server(userdata, aa, personality)
            if response:
                data["update"]="False"
                resp=requests.put(url+'get_input', json=data, headers=headers)
                
                emotion=eval(resp.text)["emotion"]
                if emotion not in list_of_emotions:
                    emotion="N"
                if eval(resp.text)["attention"]=="positive":
                    pn="A_"+map_emotion_AV_axis[emotion]
                else:
                    pn="NA_"+map_emotion_AV_axis[emotion]
                rr=update_weights_e(aa,pi,pn) #qui in ogni caso avrò una new perception
                change_raward("reward_e",float(rr))
                return "outcome9"
            else:
                return "outcome8"


        elif ac=="CONSC_ACTION":
            data["update"]="False"
            resp=requests.put(url+'get_input', json=data, headers=headers)
            emotion=eval(resp.text)["emotion"]
            if emotion not in list_of_emotions:
                    emotion="N"
            if eval(resp.text)["attention"]=="positive":
                pi="A_"+map_emotion_AV_axis[emotion]
            else:
                pi="NA_"+map_emotion_AV_axis[emotion]
            if predicates_objects["new_sentence"].is_grounded==True:
                aa,rew=choose_action_c(pi,False)
            else:
                aa,rew=choose_action_c(pi,False)
            userdata, response=self.call_action_server(userdata, aa,personality)
            if response:
                change_raward("reward_c",float(rew))
                return "outcome9"
            else:
                return "outcome8"


        elif ac=="UNSC_ACTION":
            data["update"]="False"
            resp=requests.put(url+'get_input', json=data, headers=headers)
            emotion=eval(resp.text)["emotion"]
            if emotion not in list_of_emotions:
                    emotion="N"
            if eval(resp.text)["attention"]=="positive":
                pi="A_"+map_emotion_AV_axis[emotion]
            else:
                pi="NA_"+map_emotion_AV_axis[emotion]
            if predicates_objects["new_sentence"].is_grounded==True:
                aa,rew=choose_action_u(pi,False)
            else:
                aa,rew=choose_action_u(pi,False)
           
            userdata, response=self.call_action_server(userdata, aa,personality)
            if response:
                change_raward("reward_c",float(rew))
                return "outcome9"
            else:
                return "outcome8"


        else:
            userdata, response=self.call_action_server(userdata, ac, personality)
            if response:
                return "outcome9"
            else:
                return "outcome8"


    def call_action_server(self, userdata, ac,personality):
            global data_action
            userdata.state="exec"
            resp, mmap, to_exec_action, exec_personality = dispatch_action(ac, personality)
            resp2=True
            if ("react" not in to_exec_action) and ("compute" not in to_exec_action) and ("check" not in to_exec_action):
                #set that I have executed an action
                data_action["finished"]="False"
                data_action["personality"]=exec_personality
                data_action["action"]=to_exec_action
                data_action["language"]=mmap["language"]
                data_action["pitch"]=mmap["pitch"]
                data_action["velocity"]=mmap["velocity"]
                data_action["volume"]=mmap["volume"]
                data_action["new_action"]="True"
                respac=requests.put(url3+'set_action', json=data_action, headers=headers)
                respex=requests.put(url3+'get_exec', json=data_action, headers=headers)
                while eval(respex.text)["executed"]=="False":
                    respex=requests.put(url3+'get_exec', json=data_action, headers=headers)

                if eval(respex.text)["result"]=="False":
                    resp2=False
            
            if resp2==False:
                    print('Action Failed')        
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
        global emotion, new_emotion, new_sentence, data, new_attention, attention
        print('check perception') 
        data["update"]="True"
        resp=requests.put(url+'get_input', json=data, headers=headers)
        a=userdata.action
        print("action",a)
        if eval(resp.text)["new_emotion"]=="True":
            new_emotion=True
            emotion=eval(resp.text)["emotion"]
        if eval(resp.text)["new_sentence"]=="True":
            new_sentence=True

        if eval(resp.text)["new_attention"]=="True":
            new_attention=True
            attention=eval(resp.text)["attention"]


        while (new_emotion==False and new_sentence==False and  new_attention==False and userdata.action==""):
            time.sleep(1)
            data["update"]="True"
            resp=requests.put(url+'get_input', json=data, headers=headers)
            if eval(resp.text)["new_emotion"]=="True":
                new_emotion=True
                emotion=eval(resp.text)["emotion"]
                print(emotion)
            if eval(resp.text)["new_sentence"]=="True":
                new_sentence=True

            if eval(resp.text)["new_attention"]=="True":
               new_attention=True
               attention=eval(resp.text)["attention"]
        #IF I HAVE NO NEW PERCEPTION IT MEANS THAT I COME FROM THE PREVIOUS ACTION
        if new_emotion==False and new_sentence==False and new_attention==False:
            if "ACTION" in userdata.action:
                return "outcome3" #if I have done a trait specific action I need to replan
            
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
               print(emotion)
               print(perception_predicate_map)
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
                add_goal("finished")
                remove_predicate("answered")
                remove_predicate("finished")
                add_predicate("new_sentence")
                new_sentence=False
            add_goal("feel_comfort")
            remove_predicate("feel_comfort")
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
        userdata.out_action=acc
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
            data_action["finished"]="True"
            data_action["new_action"]="False"
            respac=requests.put(url3+'set_action', json=data_action, headers=headers)
            return "outcome11"
        else:
            data_action["finished"]="True"
            data_action["new_action"]="False"
            respac=requests.put(url3+'set_action', json=data_action, headers=headers)
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



    
