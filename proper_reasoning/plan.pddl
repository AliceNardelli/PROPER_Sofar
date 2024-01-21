
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
                                   3            [1][2][3]
                                   2            [1]
                                   1            [1]
                                   0            

ff: found legal plan as follows

step    0: REACT_ANGER_EMOTION
        1: ANSWER
        2: UNSC_ACTION
        3: UNSC_ACTION
        4: CHECK_FINISH
        5: COMPUTE_HEDONIC_FEELINGS
     

time spent:    0.00 seconds instantiating 10 easy, 0 hard action templates
               0.00 seconds reachability analysis, yielding 11 facts and 10 actions
               0.00 seconds creating final representation with 9 relevant facts, 6 relevant fluents
               0.00 seconds computing LNF
               0.00 seconds building connectivity graph
               0.00 seconds searching, evaluating 13 states, to a max depth of 3
               0.00 seconds total time

