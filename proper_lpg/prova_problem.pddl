(define (problem p) (:domain PROPER_perception)
(:objects
)
(:init
        (human_present) 
        (=(dur)0)
        (=(react)3)
        (=(reward_e)5)
        (=(reward_a)5)
        (=(reward_c)5)
        (= (extroversion_coefficient) 0.0)
        (intro)
        (=(desired_interaction) 5)
        (=(interaction_level) 10) 
        (computed_e)  
        (= (conscientious_coefficient) 0.0)
        (unsc)
        (=(desired_scrupulousness)5)
        (=(scrupulousness_level)10)
        (computed_c) 
        (= (agreeableness_coefficient) 1.0)
        (agree)
        (=(desired_agreeableness)5)
        (=(agreeableness_level)10)
        (computed_a)    
)

(:goal (and 
      (feelings)
    )
)


)
