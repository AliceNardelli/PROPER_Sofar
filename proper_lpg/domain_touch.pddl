(define (domain PROPER_perception)

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
        (neutral_emotion)
        (neutral_emotion_r)
        (happy_emotion)
        (happy_emotion_r)
        (anger_emotion)
        (anger_emotion_r)
        (sad_emotion)
        (sad_emotion_r)
        
)


(:action EXTRO_ACTION
    :precondition (and 
        (extro)
    )
    :effect 
        (and
    	(increase (interaction_level)5)
        )
)

(:action INTRO_ACTION
    :precondition (and 
        (intro)
    )
    :effect 
        (and
    	(increase (interaction_level)5)
        )
)

(:action CONSC_ACTION
    :precondition (and 
        (consc)
    )
    :effect 
        (and
    	(increase (scrupulousness_level)5)
        )
)

(:action UNSC_ACTION
    :precondition (and 
        (consc)
    )
    :effect 
        (and
    	(increase (scrupulousness_level)5)
        )
)

(:action AGREE_ACTION
    :precondition (and 
        (agree)
    )
    :effect 
        (and
    	(increase (agreeableness_level)5)
        )
)


(:action DISAGREE_ACTION
    :precondition (and 
        (disagree)
    )
    :effect 
        (and
    	(increase (agreeableness_level)5)
        )
)


(:action NO_REACT_HAPPY_EMOTION
        :precondition
                (and
                   (happy_emotion)
                   (or (and (intro)(>(extroversion_coefficient)0))(>(conscientious_coefficient)0))
                   (or (not(agree))(<=(agreeableness_coefficient)0))
                   (or (not(disagree))(<=(agreeableness_coefficient)0))
                   (or (not(extro))(<=(extroversion_coefficient)0))
                )

        :effect
                (and   
		            (happy_emotion_r)
                )
)

(:action REACT_HAPPY_EMOTION_NEG
        :precondition
                (and
                   (happy_emotion)
                   (disagree)
                   (>(agreeableness_coefficient)0)
                )

        :effect
                (and    
		           (happy_emotion_r)	
                   (decrease (agreeableness_level)(*(agreeableness_coefficient)(react)))
                   (if (extro)(increase (interaction_level)(*(extroversion_coefficient)(react))))
                )
)



(:action REACT_HAPPY_EMOTION_AGREE
        :precondition
                (and
                   (happy_emotion)
                   (agree)
                   (>(agreeableness_coefficient)0)
                )

        :effect
                (and    
		           (happy_emotion_r)	
                   (increase (agreeableness_level)(*(agreeableness_coefficient)(react)))
                )
)


(:action REACT_HAPPY_EMOTION_EXTRO
        :precondition
                (and
                   (happy_emotion)
                   (>(extroversion_coefficient)0)
                   (extro)
                )

        :effect
                (and    
		   (happy_emotion_r)	
                   (increase (interaction_level)(*(extroversion_coefficient)(react)))
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
        (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
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
