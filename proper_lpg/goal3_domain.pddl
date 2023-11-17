(define (domain goal3)

(:requirements :adl :strips :typing :conditional-effects :negative-preconditions :equality :fluents )

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
	    (say)
        (breathe)
	    (curl)
        (box)
        (yoga)
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

(:action REACT_SAD_EMOTION
        :precondition
                (and
                   (sad_emotion)
                   (not (emotion_r))
                   (not (sad_emotion_r))
                )

        :effect
                (and
                   (when (agree)(decrease (agreeableness_level)(*(agreeableness_coefficient)(react))))    
		   (sad_emotion_r)
                   (emotion_r)
                )
)


(:action REACT_ANGER_EMOTION
        :precondition
                (and
                   (anger_emotion)
                   (not (emotion_r))
                   (not (anger_emotion_r))
                )

        :effect
                (and
                   (when (disagree)(increase (agreeableness_level)(*(agreeableness_coefficient)(react))))
                   (when (agree)(decrease (agreeableness_level)(*(agreeableness_coefficient)(react))))
                   (when (consc)(decrease (scrupulousness_level)(*(conscientious_coefficient)(react)))) 
		   (anger_emotion_r)
                   (emotion_r)	
                )
)

(:action REACT_HAPPY_EMOTION
        :precondition
                (and
                   (happy_emotion)
                   (not (emotion_r))
                   (not (happy_emotion_r))
                )

        :effect
                (and
                   (when (disagree)(decrease (agreeableness_level)(*(agreeableness_coefficient)(react))))
                   (when (agree)(increase (agreeableness_level)(*(agreeableness_coefficient)(react))))
                   (when (extro)(increase (interaction_level)(*(extroversion_coefficient)(react))))    
		   (happy_emotion_r)
                   (emotion_r)	
                )
)


(:action REACT_NEUTRAL_EMOTION
        :precondition
                (and
                   (neutral_emotion)
                   (not (emotion_r))
                   (not (neutral_emotion_r))
                )

        :effect
                (and    
		   (neutral_emotion_r)
                   (emotion_r)
                   (when (extro)(decrease (interaction_level)(*(extroversion_coefficient)(react))))
                   (when (intro)(increase (interaction_level)(*(extroversion_coefficient)(react))))	
                )
)


(:action REACT_TOUCH
        :precondition
                (and
                   (not (touch_reacted))
                   (touched)
                )

        :effect
                (and    
                        (when (agree)(increase (agreeableness_level)(*(agreeableness_coefficient)(react))))
                        (when (extro)(increase (interaction_level)(*(extroversion_coefficient)(react))))
                        (when (intro)(decrease (interaction_level)(*(extroversion_coefficient)(react))))
                        (when (disagree)(decrease (agreeableness_level)(*(agreeableness_coefficient)(react))))
			(touch_reacted)	
                )
)



(:action SAY_DONT_TRAINING
        :precondition
               (and 
                           (touch_reacted)
                           (emotion_r)
               	           (human_present)
                           (>=(interaction_level)(desired_interaction))
                           (>=(scrupulousness_level)(desired_scrupulousness))
                           (>=(agreeableness_level)(desired_agreeableness))
                           (not(say))
                            
                        
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (when (unsc)(increase (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (when (consc)(decrease (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (say)                 
                )
)


(:action SAY_TRAINING
        :precondition
               (and 
                           (touch_reacted)
                           (emotion_r)
               	           (human_present)
                           (>=(interaction_level)(desired_interaction))
                           (>=(scrupulousness_level)(desired_scrupulousness))
                           (>=(agreeableness_level)(desired_agreeableness))
                           (not(say))
                        
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (when (unsc)(decrease (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (when (consc)(increase (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (say)                 
                )
)



(:action SAY_BREATHE
        :precondition
               (and 
                           (touch_reacted)
                           (emotion_r)
               	           (human_present)
                           (>=(interaction_level)(desired_interaction))
                           (>=(scrupulousness_level)(desired_scrupulousness))
                           (>=(agreeableness_level)(desired_agreeableness))
                           (not(breathe))
                           (say)
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (breathe)                 
                )
)


(:action SAY_CURL_BLINK
        :precondition
               (and 
                           (touch_reacted)
                           (emotion_r)
               	           (human_present)
                           (>=(interaction_level)(desired_interaction))
                           (>=(scrupulousness_level)(desired_scrupulousness))
                           (>=(agreeableness_level)(desired_agreeableness))
                           (not(curl))
                           (breathe)
                            
                        
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (when (unsc)(increase (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (when (consc)(decrease (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (curl)                 
                )
)


(:action SAY_CURL_MOVEMENT
        :precondition
               (and 
                           (touch_reacted)
                           (emotion_r)
               	           (human_present)
                           (>=(interaction_level)(desired_interaction))
                           (>=(scrupulousness_level)(desired_scrupulousness))
                           (>=(agreeableness_level)(desired_agreeableness))
                           (not(curl))
                           (breathe)
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (when (unsc)(decrease (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (when (consc)(increase (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (curl)                 
                )
)

(:action SAY_BOX_BLINK
        :precondition
               (and 
                           (touch_reacted)
                           (emotion_r)
               	           (human_present)
                           (>=(interaction_level)(desired_interaction))
                           (>=(scrupulousness_level)(desired_scrupulousness))
                           (>=(agreeableness_level)(desired_agreeableness))
                           (not(box))
                           (curl)
                            
                        
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (when (unsc)(increase (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (when (consc)(decrease (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (box)                 
                )
)


(:action SAY_BOX_MOVEMENT
        :precondition
               (and 
                           (touch_reacted)
                           (emotion_r)
               	           (human_present)
                           (>=(interaction_level)(desired_interaction))
                           (>=(scrupulousness_level)(desired_scrupulousness))
                           (>=(agreeableness_level)(desired_agreeableness))
                           (not(box))
                           (curl)
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (when (unsc)(decrease (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (when (consc)(increase (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (box)                 
                )
)




(:action SAY_YOGA
        :precondition
               (and 
                           (touch_reacted)
                           (emotion_r)
               	           (human_present)
                           (>=(interaction_level)(desired_interaction))
                           (>=(scrupulousness_level)(desired_scrupulousness))
                           (>=(agreeableness_level)(desired_agreeableness))
                           (not(yoga))
                           (box)
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (yoga)                 
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
                        (yoga)
                )

        :effect
                (and    
			(finished)
			
                )
)

)
