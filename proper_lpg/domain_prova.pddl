(define (domain PROPER_navigation)

(:requirements :adl :derived-predicates :strips :typing :conditional-effects :negative-preconditions :equality :fluents :durative-actions  :duration-inequalities :continuous-effects :time)

(:types
	
)

(:functions
	(dur)
        (extroversion_coefficient)
        (desired_interaction)
        (interaction_level)
        (conscientious_coefficient)
        (desired_scrupulousness)
        (scrupulousness_level) 
        (agreeableness_coefficient)
        (desired_agreeableness)
        (agreeableness_level) 

)

(:predicates 
	(human_present)
	(greetings)
	(feelings)
	(extro)
        (intro)
        (computed_e)
        (consc)
        (unsc)
        (computed_c)
        (agree)
        (disagree)
        (computed_a)
        (touched)
        (touch_reacted)
)



(:durative-action NO_REACT_TOUCH
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (touched))
                   (at start (>(conscientious_coefficient)0))
                   (at start (not(agree)))
                   (at start (not(disagree)))
                   (at start (not(extro)))
                   (at start (not(intro)))
                )

        :effect
                (and    
			(at start (touch_reacted))	
                )
)

(:durative-action APPROACH_TOUCH
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (touched))
                   (at start (extro))
                   (at start (agree)) 
                  
                )

        :effect
                (and   
                	(at start (assign (dur) 5))
			(at end (increase (interaction_level)(*(extroversion_coefficient)(dur))))
			(at end (increase (agreeableness_level)(*(agreeableness_coefficient)(dur))))
			(at end (touch_reacted))
                )
)


(:durative-action AVOID_TOUCH
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (touched))
                   (at start (disagree))
                   (at start (intro))
                )

        :effect
                (and    
                	(at start (assign (dur) 5))
			(at end (decrease (interaction_level)(*(extroversion_coefficient)(dur))))
			(at end (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur))))
			(at end (touch_reacted))
			
                )
)


(:durative-action GREETINGS
        :parameters
               ()
        :duration
               (= ?duration 5)

        :condition
               (and 
               	 (at start (human_present))
                        (at start (computed_e))
                        (at start (computed_c))
                        (at start (computed_a))
                        (at start (>=(interaction_level)(desired_interaction)))
                        (at start (>=(scrupulousness_level)(desired_scrupulousness)))
                        (at start (>=(agreeableness_level)(desired_agreeableness)))
                        (at start(not(greetings)))
                        
                )
        :effect
                (and
                        (at end (not (computed_e)))
                        (at end (not (computed_c)))
                        (at end (not (computed_a)))
                        (at end (assign (dur) 5))
                        (at end (greetings))                 
                )
)


(:durative-action FEELINGS
        :parameters
               ()
        :duration
               (= ?duration 5)

        :condition
               (and 
               	 (at start (human_present))
                        (at start (computed_e))
                        (at start (computed_c))
                        (at start (computed_a))
                        (at start (>=(interaction_level)(desired_interaction)))
                        (at start (>=(scrupulousness_level)(desired_scrupulousness)))
                        (at start (>=(agreeableness_level)(desired_agreeableness)))
                        (at start (greetings))
                        (at start (not(feelings)))
                        
                )
        :effect
                (and
                        (at end (not (computed_e)))
                        (at end (not (computed_c)))
                        (at end (not (computed_a)))
                        (at end (assign (dur) 5))
                        (at end (feelings))                 
                )
)



(:action COMPUTE_METRIC_INTRO
    :precondition (and 
        (not (computed_e))  
        (intro) 
    )
    :effect (and
    	(computed_e)
        (decrease (interaction_level)(*(extroversion_coefficient)(+(dur)10)))
        )
)



(:action COMPUTE_METRIC_EXTRO
    :precondition (and 
        (not (computed_e))  
        (extro)
    )
    :effect 
    (and
    	(computed_e)
        (increase (interaction_level)(*(extroversion_coefficient)(dur)))
    )
)


(:action COMPUTE_METRIC_UNSC
    :precondition (and 
         (not (computed_c))  
         (unsc) 
    )
    :effect 
           (and
    	   (computed_c)
           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
           )
)

(:action COMPUTE_METRIC_CONSC
    :precondition (and 
        (not (computed_c))  
        (consc) 
    )
    :effect 
        (and
    	(computed_c)
        (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
        )
)


(:action COMPUTE_METRIC_DISAGREE
    :precondition (and 
        (not (computed_a))  
        (disagree)
    )
    :effect 
          (and
    	   (computed_a)
           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
           )
)

(:action COMPUTE_METRIC_AGREE
    :precondition (and 
        (not (computed_a))  
        (agree)
    )
    :effect 
       (and
    	(computed_a)
        (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
        )
)


)
