
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

Cueing down from goal distance:   10 into depth [1]
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

step    0: REACT_SAD_EMOTION
        1: REACT_LOW_ATTENTION
        2: GUESS_QUIZ
        3: DISAGREE_ACTION
        4: UNSC_ACTION
        5: UNSC_ACTION
        6: UNSC_ACTION
        7: INTRO_ACTION
        8: INTRO_ACTION
        9: CHECK_FINISH
     

time spent:    0.00 seconds instantiating 9 easy, 0 hard action templates
               0.00 seconds reachability analysis, yielding 26 facts and 9 actions
               0.00 seconds creating final representation with 15 relevant facts, 3 relevant fluents
               0.00 seconds computing LNF
               0.00 seconds building connectivity graph
               0.00 seconds searching, evaluating 11 states, to a max depth of 1
               0.00 seconds total time

