from owlready2 import *

#load the ontology
#define properties
onto_path.append("/home/alice/")
onto = get_ontology("http://www.semanticweb.org/alice/ontologies/2023/4/pp#").load()          
with onto:
    class Predicates(Thing):
        pass
    class Functions(Thing):
        pass
    class Actions(Thing):
        pass
    class Types(Thing):
        pass
    class Objects(Thing):
        pass
    class Parameters(Thing):
        pass

    AllDisjoint([Predicates,Functions,Actions,Types,Objects,Parameters])


    class has_effect_predicates(ObjectProperty):
        domain    = [Actions]
        range     = [Predicates]

    class is_effect_predicates(ObjectProperty):
        domain    = [Predicates]
        range     = [Actions]
        inverse_property = has_effect_predicates

    class has_effect_function(ObjectProperty):
        domain    = [Actions]
        range     = [Functions]

    class is_effect_function(ObjectProperty):
        domain    = [Functions]
        range     = [Actions]
        inverse_property = has_effect_function

    class has_object(ObjectProperty):
        domain    = [Predicates]
        range     = [Objects]

    class is_object(ObjectProperty):
        domain    = [Objects]
        range     = [Predicates]
        inverse_property = has_object

    class has_type(ObjectProperty):
        domain    = [Objects]
        range     = [Types]

    class is_type(ObjectProperty):
        domain    = [Types]
        range     = [Objects]
        inverse_property = has_type

    class has_params_actions(ObjectProperty):
        domain    = [Parameters]
        range     = [Actions]

    class is_params_actions(ObjectProperty):
        domain    = [Actions]
        range     = [Parameters]
        inverse_property = has_params_actions

    class has_params_types(ObjectProperty):
        domain    = [Parameters]
        range     = [Types]

    class is_params_types(ObjectProperty):
        domain    = [Types]
        range     = [Parameters]
        inverse_property = has_params_types

    class has_value(DataProperty, FunctionalProperty): #functional means that each one has a single value
        domain =[Functions]
        range = [float]

    class is_grounded(DataProperty, FunctionalProperty): #functional means that each one has a single value
        domain =[Predicates]
        range = [bool]

    class is_goal(DataProperty, FunctionalProperty): #functional means that each one has a single value
        domain =[Predicates]
        range = [bool]

    class has_operator(DataProperty): #is not a functional, each predicate can have more than one operator
        #domain =[Predicates]
        range = [str]

    class has_order(DataProperty, FunctionalProperty): 
        domain =[Parameters]
        range = [int]    

    class has_single_object(DataProperty, FunctionalProperty): 
        domain =[Predicates]
        range = [bool]

#define global variables
actions=[]
actions_objects={}
type=[]
types_objects={}
predicates=[]
predicates_objects={}
functions=[]
function_objects={}
parameters_objects={}
objects_objects={}
new_params=[]
objects=[]
goals=[]

def change_raward(func,r):
    function_objects[func].has_value=r

def initialize_reward():
    function_objects["reward_a"].has_value=5
    function_objects["reward_e"].has_value=5
    function_objects["reward_c"].has_value=5

def add_predicate(new_pred):
    #mi serve per aggiungere delle percezioni
    predicates_objects[new_pred].is_grounded=True

def remove_predicate(new_pred):
    #mi serve per rimuovere i goal e le percezioni
    predicates_objects[new_pred].is_grounded=False

def add_goal(g):
    predicates_objects[g].is_goal=True


def populate_ontology(domain):     
    if os.path.isfile(domain):
        with open(domain, "r") as domain_file:
            raw_domain = domain_file.readlines()
    #ACTIONS
    last_action=""
    for p in raw_domain:
        if (":durative-action" in p) or (":action" in p):
            if (":durative-action" in p):
                last_action=p.replace(":durative-action","").replace("( ","").replace("\n","")
            elif (":action" in p):
                last_action=p.replace(":action","").replace("( ","").replace("\n","")
            actions.append(last_action)
    actions.pop(0)
    for a in actions:
        actions_objects[a]=Actions(a)
    #TYPES
    t=False
    for p in raw_domain:
            if (")" in p):
                t=False
            if t==True:
                type.append(p.replace("\t","").replace("\n",""))
            if (":types" in p):
                t=True
    for t in type:
        types_objects[t]=Types(t)
    #PREDICATES
    t=False
    for p in raw_domain:
            if (":action" in p):
                t=False
            if t==True:
                if "?" in p:
                    new=p[p.find("(")+1:p.find("?")].replace(" ","")
                    
                else:
                    new=p[p.find("(")+1:p.find(")")].replace(" ","")
                    
                if new!="":   
                    predicates.append(new)
            if (":predicates" in p):
                t=True
    
    for t in predicates:
        predicates_objects[t]=Predicates(t)


    #FUNCTIONS
    t=False
    for p in raw_domain:
            if (":predicates" in p):
                t=False
            if t==True:
                if "?" in p:
                    new=p[p.find("(")+1:p.find("?")]
                    
                else:
                    new=p[p.find("(")+1:p.find(")")]
                    
                if new!="":   
                    functions.append(new)
            if (":functions" in p):
                t=True
    
    for t in functions:
        function_objects[t]=Functions(t)

    #connect all the relations between actions predicates and functions
    t=False
    pr=False
    last_action=""
    associated_types=[]
    associated_actions=[]
    associated_orders=[]
    for p in raw_domain:
        if (":duration" in p) or (":precondition" in p):
            pr=False
        if (":durative-action" in p) or (":action" in p):
            t=False
            if (":durative-action" in p):
                last_action=p.replace(":durative-action","").replace("( ","").replace("\n","")
            elif (":action" in p):
                last_action=p.replace(":action","").replace("( ","").replace("\n","")
        if t==True:
            if ";" not in p:
                operation=p.replace("and","").replace("at end","").replace("("," ").replace(")"," ")
                pred=operation.replace("decrease","").replace("increase","").replace("assign","").replace("not","").split()
                #operation=operation.split()
            
                if pred==[]:
                    continue
                else:
                    check=str(pred[0])
                    for l in predicates:
                        if check==l:
                            actions_objects[last_action].has_effect_predicates.append(predicates_objects[check])
                            ops=last_action.replace(" ","")+" "+operation
                            predicates_objects[check].has_operator.append(ops)
                            break
                            
                    for l in functions:
                        if check==l:
                            actions_objects[last_action].has_effect_function.append(function_objects[check])
                            ops=last_action.replace(" ","")+" "+operation
                            function_objects[check].has_operator.append(ops)
                            break
        if pr==True:
            params=p[p.index("(")+1:p.index(")")].replace("-","").split(" ")
            while 1:
                    try:
                     params.remove("")
                    except:
                     break
            c=0
            for i in params:
                if "?" in i:
                    c+=1
                    new_params.append(i)
                    associated_actions.append(last_action)
                    associated_orders.append(c)
                else:
                    for j in range(c):
                        associated_types.append(i)
                    c=0
        if ":parameters" in p:
            pr=True
        if ":effect" in p:
            t=True

    #PARAMS       
    for t in new_params:
        parameters_objects[t]=Parameters(t)

    #adding associated objects and actions of params
    for i in range(len(new_params)):
        parameters_objects[new_params[i]].has_params_actions.append(actions_objects[associated_actions[i]])
        if len(parameters_objects[new_params[i]].has_params_types)==0:
            parameters_objects[new_params[i]].has_params_types.append(types_objects[associated_types[i]])
        parameters_objects[new_params[i]].has_order=associated_orders[i]

def initialize_functions_predicates():
    for p in predicates:
        predicates_objects[p].is_grounded=False
        predicates_objects[p].has_object=[]
        if p=="at":
            predicates_objects[p].has_single_object=True
        else:
            predicates_objects[p].has_single_object=False

    for f in functions:
        function_objects[f].has_value=0

def read_the_problem(problem_path):
    if os.path.isfile(problem_path):
        with open(problem_path, "r") as problem_file:
            raw_problem = problem_file.readlines()
    associated_types=[]
    t=False
    for p in raw_problem:
            if (":init" in p):
                t=False
            if t==True:
                o_t=p.replace("\n","").replace(")","").replace("\t","").replace(" ","").split("-")
                if o_t[0] != "":
                    objects.append(o_t[0])
                    associated_types.append(o_t[1])
            if (":objects" in p):
                t=True
    #add objects and associated types
    c=0
    for t in objects:
        objects_objects[t]=Objects(t)
        objects_objects[t].has_type=[types_objects[associated_types[c]]]
        c+=1

    #initialize predicates and functions
    t=False
    for p in raw_problem:
            if (":goal" in p):
                t=False
            if t==True:
                prec=p.replace("("," ").replace(")"," ").replace("\n"," ").split(" ")
                while 1:
                    try:
                        prec.remove("")
                    except:
                        break
                if prec!=[]:
                    if prec[0]=="=":
                        ff=prec[1]
                        function_objects[ff].has_value=float(prec[2])
                    else:
                        pp=prec[0]
                        predicates_objects[pp].is_grounded=True
                        if len(prec)==2:
                            oj=prec[1]
                            predicates_objects[pp].has_object=[objects_objects[oj]]
                            if pp=='at':
                                 objects_objects[oj].is_at=True  
    
            if (":init" in p):
                t=True


    #initialize goals
    t=False
    for p in raw_problem:
            if t==True:
                o_t=p.replace("\n","").replace(")","").replace("\t","").replace(" ","").replace("(","").split("-")
                print(o_t)
                if o_t[0] != "":
                    goals.append(o_t[0])
            if (":goal" in p):
                t=True
    #add objects and associated types
    c=0
    for t in goals:
        predicates_objects[t].is_goal=True
        c+=1

def saving():
    onto.save()


#run the planner
def planning(command,domain_path):
    #plan the first time and get the list of action
    os.chdir (domain_path)
    #run the planner
    fd_process = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    try:
        (out, err) = fd_process.communicate()
        fd_exit = fd_process.returncode
        print(fd_exit)
        return fd_exit
    except:
        print("exrrorrr")
    
   
def read_plan(output_path):
    if os.path.isfile(output_path):
        with open(output_path, "r") as plan_file:
            raw_plan = plan_file.readlines()
        plan=[]
        for p in raw_plan:
           if p[0] !=";":
            plan.append(p)
        ret=plan.remove("\n") 
        while ret==None:  
            try:
              ret=plan.remove("\n")
            except:
              ret="alice"    
        actions_to_execute=[]
        for i in plan:
            actions_to_execute.append(i[i.find("(")+1:i.find(")")])
        return actions_to_execute
        
    else:
            print("Plan not found")


def update_ontology(a):
    #check preconditions if neobjects_objects[params[parameters_objects[o[2]].has_order-1].lower()].has_typeeded
    ac=a.split(" ")[0]
    params=a.split(" ")[1:]
    preds=actions_objects[ac].has_effect_predicates
    #prendo tutti i predicati effetto di quell'azione
    for p in preds:
        ops=p.has_operator
        key = list(filter(lambda x: predicates_objects[x] == p, predicates_objects))[0]
        #per ogni predicato prendo tutte le operazioni di quel predicato
        for o in ops:
            o=o.replace("\n","").replace("\t","").split(" ")
            while 1:
                try:
                    o.remove("")
                except:
                    break
            #considero solo quelle che sono dell'azione che sto eseguendo
            if o[0]==ac:
                if o[1]=="not":
                    p.is_grounded=False
                    o.pop(1)
                else:
                    p.is_grounded=True
                
                if len(o)>2 and p.is_grounded==True:
                    if p.has_single_object==True:
                        p.has_object=[objects_objects[params[parameters_objects[o[2]].has_order-1].lower()]]
                    else:
                        #print(p,p.has_object)
                        if objects_objects[params[parameters_objects[o[2]].has_order-1].lower()] not in p.has_object:
                            p.has_object.append(objects_objects[params[parameters_objects[o[2]].has_order-1].lower()])
                   

                


    funcs=actions_objects[ac].has_effect_function
    print(funcs)
    if funcs!=[]:
        for f in funcs:
            ops=f.has_operator
            key = list(filter(lambda x: function_objects[x] == f, function_objects))[0]
            #per ogni predicato prendo tutte le operazioni di quel predicato
            print(ops)
            for o in ops:
                o=o.replace("\n","").replace("\t","").split(" ")
                while 1:
                    try:
                        o.remove("")
                    except:
                        break
                if o[0]==ac:
                    print(o)
                    print(f,ac,f.has_value)
                    if o[1]=="assign":
                       f.has_value=int(o[3])
                    elif o[1]=="increase":
                        actual_value=f.has_value
                        if o[3]=="*":
                            v1=function_objects[o[4]].has_value
                            v2=function_objects[o[5]].has_value
                            f.has_value=actual_value + v1*v2
                        else:
                            try:
                                f.has_value=actual_value + float(o[3])
                            except:
                                f.has_value=actual_value + function_objects[o[3]].has_value
                    elif o[1]=="decrease":
                        actual_value=f.has_value
                        if o[3]=="*":
                            if o[5]=="+":
                                v1=function_objects[o[4]].has_value #coeff
                                v2=function_objects[o[6]].has_value #dur
                                f.has_value=actual_value - v1*(v2+int(o[7]))
                            else:
                                v1=function_objects[o[4]].has_value
                                v2=function_objects[o[5]].has_value
                                f.has_value=actual_value - v1*v2
                        else:
                            try:
                                f.has_value=actual_value - float(o[3])
                            except:
                                f.has_value=actual_value - function_objects[o[3]].has_value
                    else:
                        print("NO OPERATION FOUND")
                    print(f,ac,f.has_value)


def update_problem(plan_path):
    if os.path.isfile(plan_path):
        output_path=plan_path
        with open(output_path, "r") as domain_file:
            raw_problem_copy= domain_file.readlines()
    c=0
    c_init_1=0
    c_init_2=0
    c_end_1=0
    c_end_2=0
    for p in raw_problem_copy:
        if "define" in p:
            c_init_1=c
        if "init" in p:
            c_init_2=c+1
        if "goal" in p:
            c_end_1=c-1
        c+=1   
    c_end_2=c
    domain_file.close()
    start_file=raw_problem_copy[c_init_1:c_init_2]
    end_file=[]
    init_file=[]

    for i in Predicates.instances():
        key = list(filter(lambda x: predicates_objects[x] == i, predicates_objects))[0]
        if i.is_grounded==True:
                if i.has_object!=[]:
                    #print(i.has_object,i)
                    for j in i.has_object:
                        #print("there",j,i)
                        key_obj = list(filter(lambda x: objects_objects[x] == j, objects_objects))[0]
                        new_line="      (" +key+ " "+key_obj+")\n"
                        init_file.append(new_line)
                else:
                    new_line="      (" +key+")\n"
                    init_file.append(new_line)

    for i in Functions.instances():
        key = list(filter(lambda x: function_objects[x] == i, function_objects))[0]
        new_line="      (=("+key+")"+str(i.has_value)+")\n"
        init_file.append(new_line)

    end_file.append(")\n")
    end_file.append("(:goal (and\n")
    for i in Predicates.instances():
        if i.is_goal==True and i.is_grounded==False:
            key = list(filter(lambda x: predicates_objects[x] == i, predicates_objects))[0]
            new_line="      (" +key+")\n"
            end_file.append(new_line)

    end_file.append(")))") 
    new_pb=start_file+init_file+end_file
    output_path=plan_path
    with open(output_path, "w") as pb_file:
        for line in new_pb:
            pb_file.write(line)
    print("written")


