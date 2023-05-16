(define (problem p) (:domain PROPER_navigation)
(:objects
	r1 - room
	r2 - room
)
(:init
        (assembly_room r1)
        (not_presented r1) 
        (production_room r2)
        (not_presented r2)
        (at r2)
        (=(max_no_blocks)3)
        (=(no_blocks)0)
        (human_present) 
        (empty_robot)
        (=(baseline)5)
        (=(dur)0)
        (=(extroversion_coefficient) 0.5)
        (=(desired_interaction) 5)
        (=(interaction_level) 5) 
        (intro)
        (computed_e)  
        (=(conscientious_coefficient)0.4)
        (=(desired_scrupulousness)5)
        (=(scrupulousness_level)5)
        (consc)
        (computed_c)  
        (=(agreeableness_coefficient)0.0)
        (=(desired_agreeableness)5)
        (=(agreeableness_level)5)
        (disagree)
        (computed_a) 
        (can_move)    
)

(:goal  
    (and 
       (finished)
       (>=(interaction_level)(desired_interaction))
       (>=(agreeableness_level)(desired_agreeableness))
    )
)

(:metric maximize (interaction_level))

)