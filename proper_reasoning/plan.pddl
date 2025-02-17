
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

Cueing down from goal distance:   12 into depth [1][2]
                                  11            [1]
                                  10            [1]
                                   9            [1]
                                   8            [1]
                                   7            [1]
                                   6            [1]
                                   5            [1]
                                   4            [1]
                                   3            [1]
                                   2            [1]
                                   1            [1]
                                   0            

ff: found legal plan as follows

step    0: GUESS_QUIZ
        1: DISAGREE_ACTION
        2: DISAGREE_ACTION
        3: UNSC_ACTION
        4: UNSC_ACTION
        5: UNSC_ACTION
        6: INTRO_ACTION
        7: INTRO_ACTION
        8: INTRO_ACTION
        9: INTRO_ACTION
       10: INTRO_ACTION
       11: CHECK_FINISH
       12: WAIT
     

time spent:    0.00 seconds instantiating 7 easy, 0 hard action templates
               0.00 seconds reachability analysis, yielding 17 facts and 7 actions
               0.00 seconds creating final representation with 7 relevant facts, 3 relevant fluents
               0.00 seconds computing LNF
               0.00 seconds building connectivity graph
               0.00 seconds searching, evaluating 14 states, to a max depth of 2
               0.00 seconds total time

