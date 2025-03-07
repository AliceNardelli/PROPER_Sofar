
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
                                   3            [1][2]
                                   2            [1]
                                   1            [1]
                                   0            

ff: found legal plan as follows

step    0: REACT_ATTENTION
        1: REACT_SURPRISE_EMOTION
        2: DISAGREE_ACTION
        3: CHECK_FINISH
        4: COMPUTE_HEDONIC_FEELINGS
     

time spent:    0.00 seconds instantiating 7 easy, 0 hard action templates
               0.00 seconds reachability analysis, yielding 12 facts and 7 actions
               0.00 seconds creating final representation with 10 relevant facts, 3 relevant fluents
               0.00 seconds computing LNF
               0.00 seconds building connectivity graph
               0.00 seconds searching, evaluating 7 states, to a max depth of 2
               0.00 seconds total time

