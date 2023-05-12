(define (problem p) (:domain trial_dom)
(:objects
	r1 - room
	r2 - room
)

(:init
        (= (extroversion_coefficient) 0.0)
        (= (desired_interaction) 5)
        (= (interaction_level) 5)
        (extro)
        (= (no)0)
        (not_finished)
)

(:goal  
    (and 
       (finished)
       (>(interaction_level)(desired_interaction))
    )
)

)