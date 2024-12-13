
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
                                   5            [1][2]
                                   4            [1][2]
                                   3            [1][2]
                                   2            [1][2]
                                   1            [1]
                                   0            

ff: found legal plan as follows

step    0: GREET FABIO
        1: EXTRO_ACTION
        2: ASK_PRESENT FABIO
        3: EXTRO_ACTION
        4: PRESENT_LAB FABIO
        5: EXTRO_ACTION
        6: ASK_PREFERENCES FABIO
        7: EXTRO_ACTION
        8: GIVE_NEW_INFO FABIO
        9: EXTRO_ACTION
       10: CHECK_FINISH FABIO
     

time spent:    0.00 seconds instantiating 16 easy, 0 hard action templates
               0.00 seconds reachability analysis, yielding 20 facts and 15 actions
               0.00 seconds creating final representation with 11 relevant facts, 3 relevant fluents
               0.00 seconds computing LNF
               0.00 seconds building connectivity graph
               0.00 seconds searching, evaluating 16 states, to a max depth of 2
               0.00 seconds total time

