
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

Cueing down from goal distance:    8 into depth [1]
                                   7            [1]
                                   6            [1]
                                   5            [1][2][3]
                                   4            [1]
                                   3            [1][2][3]
                                   2            [1]
                                   1            [1]
                                   0            

ff: found legal plan as follows

step    0: GREET FABIO
        1: UNSC_ACTION
        2: EXTRO_ACTION
        3: ASK_PRESENT FABIO
        4: PRESENT_LAB FABIO
        5: UNSC_ACTION
        6: EXTRO_ACTION
        7: ASK_PREFERENCES FABIO
        8: GIVE_NEW_INFO FABIO
        9: UNSC_ACTION
       10: EXTRO_ACTION
       11: CHECK_FINISH FABIO
     

time spent:    0.00 seconds instantiating 10 easy, 0 hard action templates
               0.00 seconds reachability analysis, yielding 13 facts and 9 actions
               0.00 seconds creating final representation with 8 relevant facts, 3 relevant fluents
               0.00 seconds computing LNF
               0.00 seconds building connectivity graph
               0.00 seconds searching, evaluating 21 states, to a max depth of 3
               0.00 seconds total time

