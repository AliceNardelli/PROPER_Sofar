
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

Cueing down from goal distance:    5 into depth [1]
                                   4            [1][2]
                                   3            [1]
                                   2            [1]
                                   1            [1]
                                   0            

ff: found legal plan as follows

step    0: ASSIGN_DOMINANCE
        1: PICK_PLACE_REPLACE_HUMAN_TURN1
        2: PICK_PLACE_ROBOT_PRECISE_TURN2
        3: CONSC_ACTION
        4: COMPUTE_HEDONIC_FEELINGS
        5: CHECK_FINISH
     

time spent:    0.00 seconds instantiating 12 easy, 0 hard action templates
               0.00 seconds reachability analysis, yielding 13 facts and 12 actions
               0.00 seconds creating final representation with 10 relevant facts, 5 relevant fluents
               0.00 seconds computing LNF
               0.00 seconds building connectivity graph
               0.00 seconds searching, evaluating 8 states, to a max depth of 2
               0.00 seconds total time

