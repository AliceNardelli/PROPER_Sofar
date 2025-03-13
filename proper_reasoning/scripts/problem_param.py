problem_goals=["quiz1","quiz2","quiz3"]

#problem_goals=["quiz2","quiz3"]
actual_goal="quiz1"
#actual_goal="quiz2"

goals_dict={"quiz1": {"domain":'/home/alice/PROPER_Sofar/proper_reasoning/goal1_domain.pddl', 
      "problem":'/home/alice/PROPER_Sofar/proper_reasoning/prova_problem.pddl',
      "init":'/home/alice/PROPER_Sofar/proper_reasoning/init_problem.pddl',
      "command":'./ff -p /home/alice/PROPER_Sofar/proper_reasoning/ -o goal1_domain.pddl -f prova_problem.pddl',
      "folder":'/home/alice/PROPER_Sofar/proper_reasoning/',
      "plan":"/home/alice/PROPER_Sofar/proper_reasoning/plan.pddl",
      "ontology":"http://www.semanticweb.org/alice/ontologies/2023/10/goal1#",
      "path_onto":"/home/alice/",
      },
      
      "quiz2": {"domain":'/home/alice/PROPER_Sofar/proper_reasoning/goal1_domain.pddl', 
      "problem":'/home/alice/PROPER_Sofar/proper_reasoning/prova_problem.pddl',
      "init":'/home/alice/PROPER_Sofar/proper_reasoning/init_problem.pddl',
      "command":'./ff -p /home/alice/PROPER_Sofar/proper_reasoning/ -o goal1_domain.pddl -f prova_problem.pddl',
      "folder":'/home/alice/PROPER_Sofar/proper_reasoning/',
      "plan":"/home/alice/PROPER_Sofar/proper_reasoning/plan.pddl",
      "ontology":"http://www.semanticweb.org/alice/ontologies/2023/10/goal1#",
      "path_onto":"/home/alice/",
      },

      "quiz3": {"domain":'/home/alice/PROPER_Sofar/proper_reasoning/goal1_domain.pddl', 
      "problem":'/home/alice/PROPER_Sofar/proper_reasoning/prova_problem.pddl',
      "init":'/home/alice/PROPER_Sofar/proper_reasoning/init_problem.pddl',
      "command":'./ff -p /home/alice/PROPER_Sofar/proper_reasoning/ -o goal1_domain.pddl -f prova_problem.pddl',
      "folder":'/home/alice/PROPER_Sofar/proper_reasoning/',
      "plan":"/home/alice/PROPER_Sofar/proper_reasoning/plan.pddl",
      "ontology":"http://www.semanticweb.org/alice/ontologies/2023/10/goal1#",
      "path_onto":"/home/alice/",
      }
      }


map_emotion_AV_axis={
   "SA":"S",
   "SU":"H",
   "H":"H",
   "A":"A",
   "D":"A",
   "F":"A",
   "N":"N",
   
}

list_of_emotions=["SA","SU","H","A","D","F","N"]