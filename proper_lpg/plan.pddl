
ff: parsing domain file
domain 'GOAL2' defined
 ... done.
ff: parsing problem file
problem 'P' defined
 ... done.


no metric specified. plan length assumed.

checking for cyclic := effects --- OK.

ff: search configuration is EHC, if that fails then  best-first on 1*g(s) + 5*h(s) where
    metric is  plan length

Cueing down from goal distance:    5 into depth [1][2]
                                   4            [1]
                                   3            [1][2][3]
                                   2            [1][2]
                                   1            [1]
                                   0            

ff: found legal plan as follows

step    0: SAY_DRINK_TABLET
        1: AGREE_ACTION
        2: POINT_WATER
        3: SAY_THROUGH_RECYCLE
        4: AGREE_ACTION
        5: INTRO_ACTION
        6: SAY_EAT_SWEET
        7: INTRO_ACTION
        8: CHECK_FINISH
     

time spent:    0.00 seconds instantiating 12 easy, 0 hard action templates
               0.00 seconds reachability analysis, yielding 11 facts and 12 actions
               0.00 seconds creating final representation with 9 relevant facts, 3 relevant fluents
               0.00 seconds computing LNF
               0.00 seconds building connectivity graph
               0.00 seconds searching, evaluating 17 states, to a max depth of 3
               0.00 seconds total time

