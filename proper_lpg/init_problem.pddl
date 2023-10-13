(define (problem p) (:domain PROPER_navigation)
(:objects

)
(:init
        (human_present) 
        (=(dur)0)
        (=(extroversion_coefficient) 0.0)
        (=(desired_interaction) 5)
        (=(interaction_level) 10) 
        (intro)
        (computed_e)  
        (=(conscientious_coefficient)0.1)
        (=(desired_scrupulousness)5)
        (=(scrupulousness_level)10)
        (consc)
        (computed_c)  
        (=(agreeableness_coefficient)0.1)
        (=(desired_agreeableness)5)
        (=(agreeableness_level)10)
        (disagree)
        (computed_a)  
        (greetings) 
        (touched)
)

(:goal  
    (and 
       (feelings)
       (touch_reacted)
    )
)


)
