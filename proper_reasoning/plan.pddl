
ff: parsing domain file
domain 'GOAL1' defined
 ... done.
ff: parsing problem file
problem 'P' defined
 ... done.


no metric specified. plan length assumed.

checking for cyclic := effects --- OK.

ff: search configuration is EHC, if that fails then  best-first on 1*g(s) + 5*h(s) where
    metric is  plan length

Cueing down from goal distance:    7 into depth [1]
                                   6            [1][2]
                                   5            [1]
                                   4            [1][2]
                                   3            [1][2]
                                   2            [1][2]
                                   1            [1]
                                   0            

ff: found legal plan as follows

step    0: REACT_HAPPY_EMOTION
        1: REACT_LOW_ATTENTION
        2: ANSWER_WITH_A_QUESTION
        3: EXTRO_ACTION
        4: GREET ALICE
        5: EXTRO_ACTION
        6: ASK_PREFERENCES ALICE
        7: EXTRO_ACTION
        8: GIVE_NEW_INFO ALICE
        9: EXTRO_ACTION
       10: CHECK_FINISH ALICE
     

time spent:    0.00 seconds instantiating 20 easy, 0 hard action templates
               0.00 seconds reachability analysis, yielding 25 facts and 18 actions
               0.00 seconds creating final representation with 19 relevant facts, 3 relevant fluents
               0.00 seconds computing LNF
               0.00 seconds building connectivity graph
               0.00 seconds searching, evaluating 17 states, to a max depth of 2
               0.00 seconds total time

