
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

Cueing down from goal distance:    4 into depth [1]
                                   3            [1]
                                   2            [1][2]
                                   1            [1]
                                   0            

ff: found legal plan as follows

step    0: REACT_SAD_EMOTION
        1: COMPUTE_HEDONIC_FEELINGS
        2: ANSWER_WITH_A_QUESTION
        3: EXTRO_ACTION
        4: CHECK_FINISH
     

time spent:    0.00 seconds instantiating 10 easy, 0 hard action templates
               0.00 seconds reachability analysis, yielding 11 facts and 10 actions
               0.00 seconds creating final representation with 9 relevant facts, 6 relevant fluents
               0.00 seconds computing LNF
               0.00 seconds building connectivity graph
               0.00 seconds searching, evaluating 12 states, to a max depth of 2
               0.00 seconds total time

