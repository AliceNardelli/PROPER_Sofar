(define (problem p) (:domain PROPER_navigation)
(:objects
	r1 - room
	r2 - room
    r3 - room
)
(:init
        (assembly_room r1)
        (not_presented r1) 
        (production_room r2)
        (not_presented r2)
        (start_room r3)
        (at r3)
        (=(max_no_blocks)3)
        (=(no_blocks)0)
        (human_present) 
        (empty_robot)
        (=(baseline)5)
        (=(dur)0)
        (= (extroversion_coefficient) 0.25)
        (intro)
        (=(desired_interaction) 5)
        (=(interaction_level) 10) 
        (computed_e)  
        (= (conscientious_coefficient) 0.25)
        (unsc)
        (=(desired_scrupulousness)5)
        (=(scrupulousness_level)10)
        (computed_c)  
        (= (agreeableness_coefficient) 0.0)
        (disagree)
        (=(desired_agreeableness)5)
        (=(agreeableness_level)10)
        (computed_a) 
        (can_move)    
)

(:goal  
    (and 
       (finished)
    )
)


)