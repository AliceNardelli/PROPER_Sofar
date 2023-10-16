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
        (react)

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

(:durative-action EXTRO_ACTION
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<=(interaction_level)(desired_interaction)))
                   (at start (extro))
                )

        :effect
                (and    
                     (at end (increase (interaction_level)5))
                )
)


(:durative-action INTRO_ACTION
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<=(interaction_level)(desired_interaction)))
                   (at start (intro))
                )

        :effect
                (and    
                     (at end (increase (interaction_level)5))
                )
)


(:durative-action CONSC_ACTION
        :parameters
                ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<(scrupulousness_level)(desired_scrupulousness)))
                   (at start (consc))
                )

        :effect
                (and    
                     (at end (increase (scrupulousness_level)5))
                )
)


(:durative-action UNSC_ACTION
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<(scrupulousness_level)(desired_scrupulousness)))
                   (at start (unsc))
                )

        :effect
                (and    
                     (at end (increase (scrupulousness_level) 5))
                )
)


(:durative-action AGREE_ACTION
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<(agreeableness_level)(desired_agreeableness)))
                   (at start (agree))
                )

        :effect
                (and    
                     (at end (increase (agreeableness_level)5))
                )
)


(:durative-action DISAGREE_ACTION
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<(agreeableness_level)(desired_agreeableness)))
                   (at start (disagree))
                )

        :effect
                (and    
                     (at end (increase (agreeableness_level) 5))
                )
)


(:durative-action NO_REACT_SAD_EMOTION
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (sad_emotion))
                   (at start (or (>(extroversion_coefficient)0)(>(conscientious_coefficient)0)(and (disagree)(>(agreeableness_coefficient)0))))
                   (when (and (agree) )(and (<=(agreeableness_coefficient)0)))
                )

        :effect
                (and    
		   (at start (sad_emotion_r))	
                )
)

(:durative-action REACT_SAD_EMOTION_NEG
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (sad_emotion))
                   (at start (agree))
                   (at start (>(agreeableness_coefficient)0))
                )

        :effect
                (and    
		   (at start (sad_emotion_r))	
                   (at start (decrease (agreeableness_level)(*(agreeableness_coefficient)(react))))
                )
)

(:durative-action NO_REACT_ANGER_EMOTION
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (anger_emotion))
                   (at start (or (>(extroversion_coefficient)0)(and (unsc)(>(conscientious_coefficient)0))))
                )

        :effect
                (and    
		   (at start (anger_emotion_r))	
                )
)

(:durative-action REACT_ANGER_EMOTION_POS
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (anger_emotion))
                   (at start (disagree))
                   (at start (>(agreeableness_coefficient)0))
                )

        :effect
                (and    
		   (at start (anger_emotion_r))	
                   (at start (increase (agreeableness_level)(*(agreeableness_coefficient)(react))))
                )
)

(:durative-action REACT_ANGER_EMOTION_NEG
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (anger_emotion))
                   (at start (or  (and (consc) (>(conscientious_coefficient)0)) (and (agree)(>(agreeableness_coefficient)0))))
                )

        :effect
                (and    
		   (at start (anger_emotion_r))	
                   (at start (decrease (agreeableness_level)(*(agreeableness_coefficient)(react))))
                   (at start (decrease (scrupulousness_level)(*(conscientious_coefficient)(react))))
                )
)


(:durative-action NO_REACT_HAPPY_EMOTION
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (happy_emotion))
                   (at start (or (and (intro)(>(extroversion_coefficient)0))(>(conscientious_coefficient)0)))
                )

        :effect
                (and    
		   (at start (happy_emotion_r))	
                )
)

(:durative-action REACT_HAPPY_EMOTION_NEG
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (happy_emotion))
                   (at start (disagree))
                   (at start (>(agreeableness_coefficient)0))
                )

        :effect
                (and    
		   (at start (happy_emotion_r))	
                   (at start (decrease (agreeableness_level)(*(agreeableness_coefficient)(react))))
                )
)



(:durative-action REACT_HAPPY_EMOTION_AGREE
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (happy_emotion))
                   (at start (agree))
                   (at start (>(agreeableness_coefficient)0))
                )

        :effect
                (and    
		   (at start (happy_emotion_r))	
                   (at end (increase (agreeableness_level)(*(agreeableness_coefficient)(react))))
                )
)


(:durative-action REACT_HAPPY_EMOTION_EXTRO
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (happy_emotion))
                   (at start (>(extroversion_coefficient)0))
                   (at start (extro))
                )

        :effect
                (and    
		   (at start (happy_emotion_r))	
                   (at end (increase (interaction_level)(*(extroversion_coefficient)(react))))
                )
)



(:durative-action NO_REACT_NEUTRAL_EMOTION
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (neutral_emotion))
                   (at start (<=(extroversion_coefficient)0))
                )

        :effect
                (and    
		   (at start (neutral_emotion_r))	
                )
)

(:durative-action REACT_NEUTRAL_EMOTION_POS
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (neutral_emotion))
                   (at start (intro))
                   (at start (>(extroversion_coefficient)0))
                )

        :effect
                (and                    	
			(at end (increase (interaction_level)3))
		        (at end (neutral_emotion_r))	
                )
)

(:durative-action REACT_NEUTRAL_EMOTION_NEG
        :parameters
                 ()
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (neutral_emotion))
                   (at start (extro))
                   (at start (>(extroversion_coefficient)0))
                   
                )

        :effect
                (and                    	
                        
			(at end (decrease (interaction_level)3))
		        (at end (neutral_emotion_r))	
                )
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
                   (at start (<=(extroversion_coefficient)0))
                   (at start (<=(agreeableness_coefficient)0))
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
                   (at start (or  (and (extro) (>(extroversion_coefficient)0)) (and (agree)(>(agreeableness_coefficient)0))))
                )

        :effect
                (and   
                	
			(at end (increase (interaction_level)(*(extroversion_coefficient)(react))))
			(at end (increase (agreeableness_level)(*(agreeableness_coefficient)(react))))
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
                   (at start (or  (and (intro)(>(extroversion_coefficient)0)) (and (disagree)(>(agreeableness_coefficient)0))))
                )

        :effect
                (and    
                	
			(at end (decrease (interaction_level)(*(extroversion_coefficient)(react))))
			(at end (decrease (agreeableness_level)(*(agreeableness_coefficient)(react))))
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
