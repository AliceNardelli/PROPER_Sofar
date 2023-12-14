
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

Cueing down from goal distance:    6 into depth [1]
                                   5            [1][2]
                                   4            [1]
                                   3            [1][2]
                                   2            [1][2]
                                   1            [1]
                                   0            

ff: found legal plan as follows

step    0: INTRO_ACTION
        1: REACT_SAD_EMOTION
        2: AGREE_ACTION
        3: SAY_GREETINGS
        4: SAY_SKIP_FEELINGS
        5: AGREE_ACTION
        6: SAY_NOT_SITTING
        7: INTRO_ACTION
        8: CHECK_FINISH
     

time spent:    0.00 seconds instantiating 10 easy, 0 hard action templates
               0.00 seconds reachability analysis, yielding 14 facts and 10 actions
               0.00 seconds creating final representation with 11 relevant facts, 3 relevant fluents
               0.00 seconds computing LNF
               0.00 seconds building connectivity graph
               0.00 seconds searching, evaluating 13 states, to a max depth of 2
               0.00 seconds total time

