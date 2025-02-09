
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

Cueing down from goal distance:    3 into depth [1]
                                   2            [1]
                                   1            [1]
                                   0            

ff: found legal plan as follows

step    0: SUGGEST_ACTIVITIES A0
        1: INTRO_ACTION
        2: CHECK_FINISH A0
     

time spent:    0.00 seconds instantiating 14 easy, 0 hard action templates
               0.00 seconds reachability analysis, yielding 12 facts and 8 actions
               0.00 seconds creating final representation with 5 relevant facts, 3 relevant fluents
               0.00 seconds computing LNF
               0.00 seconds building connectivity graph
               0.00 seconds searching, evaluating 4 states, to a max depth of 1
               0.00 seconds total time

