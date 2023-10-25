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
        (reward_e)
        (reward_a)
        (reward_c)      
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
               	(at start (extro))
                )
        :effect
                (and
                        (at start (increase (interaction_level)(reward_e)))
                        (at end (assign(reward_e)5))
                )
)

(:durative-action INTRO_ACTION
        :parameters
               ()
        :duration
               (= ?duration 5)

        :condition
               (and 
               	(at start (intro))
                )
        :effect
                (and
                        (at start (increase (interaction_level)(reward_e)))
                        (at end (assign(reward_e)5))                 
                )
)

(:durative-action CONSC_ACTION
        :parameters
               ()
        :duration
               (= ?duration 5)

        :condition
               (and 
               	(at start (consc))
                )
        :effect
                (and
                        (at start (increase (scrupulousness_level)(reward_c)))
                        (at end (assign(reward_c)5))                 
                )
)


(:durative-action UNSC_ACTION
        :parameters
               ()
        :duration
               (= ?duration 5)

        :condition
               (and 
               	(at start (unsc))
                )
        :effect
                (and
                        (at start (increase (scrupulousness_level)(reward_c)))
                        (at end (assign(reward_c)5))                 
                )
)

(:action AGREE_ACTION
        :precondition
               (and 
               	(agree)
                )
        :effect
                (and
                        (increase (agreeableness_level)(reward_a))                                   
                )
)

(:durative-action DISAGREE_ACTION
        :parameters
               ()
        :duration
               (= ?duration 5)

        :condition
               (and 
               	(at start (disagree))
                )
        :effect
                (and
                        (at start (increase (agreeableness_level)(reward_a)))
                        (at end (assign(reward_a)5))                 
                )
)

(:action NO_REACT_SAD_EMOTION
        :precondition
                (and
                   (sad_emotion)
                   (or (>(extroversion_coefficient)0)(>(conscientious_coefficient)0)(and (disagree)(>(agreeableness_coefficient)0)))
                   (or (not(agree))(<=(agreeableness_coefficient)0))
                )

        :effect
                (and    
		   (sad_emotion_r)
                  
                )
)

(:action REACT_SAD_EMOTION_NEG
        :precondition
                (and
                   (sad_emotion)
                   (agree)
                   (>(agreeableness_coefficient)0)
                )

        :effect
                (and    
		   (sad_emotion_r)	
                   (decrease (agreeableness_level)(*(agreeableness_coefficient)(react)))
                )
)

(:action NO_REACT_ANGER_EMOTION
        :precondition
                (and
                   (anger_emotion)
                   (or (>(extroversion_coefficient)0)(and (unsc)(>(conscientious_coefficient)0)))
                   (or (not(agree))(<=(agreeableness_coefficient)0))
                   (or (not(disagree))(<=(agreeableness_coefficient)0))
                   (or (not(consc))(<=(conscientious_coefficient)0))
                )

        :effect
                (and    
		   (anger_emotion_r)	
                )
)

(:action REACT_ANGER_EMOTION_POS
        :precondition
                (and
                   (anger_emotion)
                   (disagree)
                   (>(agreeableness_coefficient)0)
                )

        :effect
                (and    
		   (anger_emotion_r)	
                   (increase (agreeableness_level)(*(agreeableness_coefficient)(react)))
                )
)

(:action REACT_ANGER_EMOTION_NEG
        :precondition
                (and
                   (anger_emotion)
                   (or  (and (consc) (>(conscientious_coefficient)0)) (and (agree)(>(agreeableness_coefficient)0)))
                )

        :effect
                (and    
		   (anger_emotion_r)	
                   (decrease (agreeableness_level)(*(agreeableness_coefficient)(react)))
                   (decrease (scrupulousness_level)(*(conscientious_coefficient)(react)))
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



(:action NO_REACT_NEUTRAL_EMOTION
        :precondition
                (and
                   (neutral_emotion)
                   (<=(extroversion_coefficient)0)
                )

        :effect
                (and    
		   (neutral_emotion_r)	
                )
)

(:action REACT_NEUTRAL_EMOTION_POS
        :precondition
                (and
                   (neutral_emotion)
                   (intro)
                   (>(extroversion_coefficient)0)
                )

        :effect
                (and                    	
			(increase (interaction_level)3)
		        (neutral_emotion_r)	
                )
)

(:action REACT_NEUTRAL_EMOTION_NEG
        :precondition
                (and
                   (neutral_emotion)
                   (extro)
                   (>(extroversion_coefficient)0)
                   
                )

        :effect
                (and                
			(decrease (interaction_level)3)
		        (neutral_emotion_r)	
                )
)

(:action NO_REACT_TOUCH
        :precondition
                (and
                   (touched)
                   (>(conscientious_coefficient)0)
                   (<=(extroversion_coefficient)0)
                   (<=(agreeableness_coefficient)0)
                )

        :effect
                (and    
			(touch_reacted)	
                )
)

(:action APPROACH_TOUCH
        :precondition
                (and
                   (touched)
                   (or  (and (extro) (>(extroversion_coefficient)0)) (and (agree)(>(agreeableness_coefficient)0)))
                )

        :effect
                (and   
                	
			(increase (interaction_level)(*(extroversion_coefficient)(react)))
			(increase (agreeableness_level)(*(agreeableness_coefficient)(react)))
			(touch_reacted)
                )
)


(:action AVOID_TOUCH
        :precondition
                (and
                   (touched)
                   (or  (and (intro)(>(extroversion_coefficient)0)) (and (disagree)(>(agreeableness_coefficient)0)))
                )

        :effect
                (and    
                	
			(decrease (interaction_level)(*(extroversion_coefficient)(react)))
			(decrease (agreeableness_level)(*(agreeableness_coefficient)(react)))
			(touch_reacted)
			
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
