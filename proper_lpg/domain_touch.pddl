(define (domain PROPER_perception)

(:requirements :adl :strips :typing :conditional-effects :negative-preconditions :equality :fluents)

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
        (finished)
	(greetings)
	(feelings)
	(extro)
        (intro)
        (consc)
        (unsc)
        (agree)
        (disagree)
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
        (emotion_r)
        
)



 



(:action EXTRO_ACTION
        :precondition
               (and 
               	(extro)
                )
        :effect
                (and
                (increase (interaction_level)(reward_e))
                )
)

(:action INTRO_ACTION

        :precondition
               (and 
               (intro)
               )
        :effect
                (and
                     (increase (interaction_level)(reward_e))                 
                )
)

(:action CONSC_ACTION
        :precondition
               (and 
               	(consc)
                )
        :effect
                (and
                       (increase (scrupulousness_level)(reward_c))
                                        
                )
)


(:action UNSC_ACTION
        :precondition
               (and 
               	(unsc)
                )
        :effect
                (and
                        (increase (scrupulousness_level)(reward_c))
                                       
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

(:action DISAGREE_ACTION
        :precondition
               (and 
               	(disagree)
                )
        :effect
                (and
                        (increase (agreeableness_level)(reward_a))
                                      
                )
)

(:action NO_REACT_SAD_EMOTION
        :precondition
                (and
                   (sad_emotion)
                   (or (>(extroversion_coefficient)0)(>(conscientious_coefficient)0)(and (disagree)(>(agreeableness_coefficient)0)))
                   (or (not(agree))(<=(agreeableness_coefficient)0))
                   (not (emotion_r))
                   (not (sad_emotion_r))
                )

        :effect
                (and    
		   (sad_emotion_r)
                   (emotion_r)
                )
)

(:action REACT_SAD_EMOTION_NEG
        :precondition
                (and
                   (sad_emotion)
                   (agree)
                   (>(agreeableness_coefficient)0)
                   (not (emotion_r))
                   (not (sad_emotion_r))
                   
                )

        :effect
                (and    
		   (sad_emotion_r)	
                   (decrease (agreeableness_level)(*(agreeableness_coefficient)(react)))
                   (emotion_r)
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
                   (not (emotion_r))
                   (not (anger_emotion_r))
                )

        :effect
                (and    
		   (anger_emotion_r)
                   (emotion_r)	
                )
)

(:action REACT_ANGER_EMOTION_POS
        :precondition
                (and
                   (anger_emotion)
                   (disagree)
                   (>(agreeableness_coefficient)0)
                   (not (emotion_r))
                   (not (anger_emotion_r))
                )

        :effect
                (and    
		   (anger_emotion_r)	
                   (increase (agreeableness_level)(*(agreeableness_coefficient)(react)))
                   (emotion_r)
                )
)

(:action REACT_ANGER_EMOTION_NEG
        :precondition
                (and
                   (anger_emotion)
                   (or  (and (consc) (>(conscientious_coefficient)0)) (and (agree)(>(agreeableness_coefficient)0)))
                   (not (emotion_r))
                   (not (anger_emotion_r))
                )

        :effect
                (and    
		   (anger_emotion_r)	
                   (decrease (agreeableness_level)(*(agreeableness_coefficient)(react)))
                   (decrease (scrupulousness_level)(*(conscientious_coefficient)(react)))
                   (emotion_r)
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
                   (not (emotion_r))
                   (not (happy_emotion_r))
                )

        :effect
                (and    
		   (happy_emotion_r)
                   (emotion_r)	
                )
)

(:action REACT_HAPPY_EMOTION_NEG
        :precondition
                (and
                   (happy_emotion)
                   (disagree)
                   (>(agreeableness_coefficient)0)
                   (not (emotion_r))
                   (not (happy_emotion_r))
                )

        :effect
                (and    
		   (happy_emotion_r)	
                   (decrease (agreeableness_level)(*(agreeableness_coefficient)(react)))
                   (emotion_r)
                )
)



(:action REACT_HAPPY_EMOTION_AGREE
        :precondition
                (and
                   (happy_emotion)
                   (agree)
                   (>(agreeableness_coefficient)0)
                   (not (emotion_r))
                   (not (happy_emotion_r))
                )

        :effect
                (and    
		   (happy_emotion_r)	
                   (increase (agreeableness_level)(*(agreeableness_coefficient)(react)))
                   (emotion_r)
                )
)


(:action REACT_HAPPY_EMOTION_EXTRO
        :precondition
                (and
                   (happy_emotion)
                   (>(extroversion_coefficient)0)
                   (extro)
                   (not (emotion_r))
                   (not (happy_emotion_r))
                )

        :effect
                (and    
		   (happy_emotion_r)	
                   (increase (interaction_level)(*(extroversion_coefficient)(react)))
                   (emotion_r)
                )
)



(:action NO_REACT_NEUTRAL_EMOTION
        :precondition
                (and
                   (neutral_emotion)
                   (<=(extroversion_coefficient)0)
                   (not (emotion_r))
                   (not (neutral_emotion_r))
                )

        :effect
                (and    
		   (neutral_emotion_r)
                   (emotion_r)	
                )
)

(:action REACT_NEUTRAL_EMOTION_POS
        :precondition
                (and
                   (neutral_emotion)
                   (intro)
                   (>(extroversion_coefficient)0)
                   (not (emotion_r))
                   (not (neutral_emotion_r))
                )

        :effect
                (and                    	
			(increase (interaction_level)3)
		        (neutral_emotion_r)
                        (emotion_r)	
                )
)

(:action REACT_NEUTRAL_EMOTION_NEG
        :precondition
                (and
                   (neutral_emotion)
                   (extro)
                   (>(extroversion_coefficient)0)
                   (not (emotion_r))
                   (not (neutral_emotion_r))
                )

        :effect
                (and                
			(decrease (interaction_level)3)
		        (neutral_emotion_r)
                        (emotion_r)	
                )
)

(:action NO_REACT_TOUCH
        :precondition
                (and
                   (not (touch_reacted))
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

(:action APPROACH_TOUCH_AGREE
        :precondition
                (and
                   (not (touch_reacted))
                   (touched)
                   (and (agree)(>(agreeableness_coefficient)0))
                )

        :effect
                (and   
			(increase (agreeableness_level)(*(agreeableness_coefficient)(react)))
			(touch_reacted)
                )
)

(:action APPROACH_TOUCH_EXTRO
        :precondition
                (and
                   (not (touch_reacted))
                   (touched)
                   (and (extro) (>(extroversion_coefficient)0)) 
                )

        :effect
                (and   
                	
			(increase (interaction_level)(*(extroversion_coefficient)(react)))
			(touch_reacted)
                )
)

(:action AVOID_TOUCH_INTRO
        :precondition
                (and
                   (not (touch_reacted))
                   (touched)
                   (and (intro)(>(extroversion_coefficient)0)) 
                )

        :effect
                (and    
                	
			(decrease (interaction_level)(*(extroversion_coefficient)(react)))
			(touch_reacted)
			
                )
)


(:action AVOID_TOUCH_DISAGREE
        :precondition
                (and
                   (not (touch_reacted))
                   (touched)
                   (and (disagree)(>(agreeableness_coefficient)0))
                )

        :effect
                (and    
			(decrease (agreeableness_level)(*(agreeableness_coefficient)(react)))
			(touch_reacted)
			
                )
)


(:action GREETINGS
        :precondition
               (and 
                        (touch_reacted)
                        (emotion_r)
               	        (human_present)
                        (>=(interaction_level)(desired_interaction))
                        (>=(scrupulousness_level)(desired_scrupulousness))
                        (>=(agreeableness_level)(desired_agreeableness))
                        (not(greetings))
                        
                )
        :effect
                (and
                       
                        (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                        (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                        (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                        (greetings)                
                )
)


(:action FEELINGS
        :precondition
               (and 
                          (touch_reacted)
                          (emotion_r)
               	          (human_present)
                          (>=(interaction_level)(desired_interaction))
                          (>=(scrupulousness_level)(desired_scrupulousness))
                          (>=(agreeableness_level)(desired_agreeableness))
                          (greetings)
                          (not(feelings))
                        
                )
        :effect
                (and
                    
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (feelings)                
                )
)


(:action CHECK_FINISH
        :precondition
                (and
                        (touch_reacted)
                        (emotion_r)
                        (>=(interaction_level)(desired_interaction))
                        (>=(scrupulousness_level)(desired_scrupulousness))
                        (>=(agreeableness_level)(desired_agreeableness))
                        (feelings)
                )

        :effect
                (and    
			(finished)
			
                )
)

)
