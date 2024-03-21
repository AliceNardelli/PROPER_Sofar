
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
                                   6            [1]
                                   5            [1]
                                   4            [1]
                                   3            [1][2]
                                   2            [1]
                                   1            [1]
                                   0            

ff: found legal plan as follows

step    0: REACT_ANGER_EMOTION
        1: REACT_LOW_ATTENTION
        2: SAY_HUMAN_TURN1
        3: EXTRO_ACTION
        4: PICK_PLACE_ROBOT_PRECISE_TURN2
        5: AGREE_ACTION
        6: COMPUTE_HEDONIC_FEELINGS
        7: CHECK_FINISH
     

time spent:    0.00 seconds instantiating 12 easy, 0 hard action templates
               0.00 seconds reachability analysis, yielding 25 facts and 12 actions
               0.00 seconds creating final representation with 17 relevant facts, 4 relevant fluents
               0.00 seconds computing LNF
               0.00 seconds building connectivity graph
               0.00 seconds searching, evaluating 10 states, to a max depth of 2
               0.00 seconds total time

