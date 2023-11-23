(define (domain goal1)

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
        (finished)
	(answered)
	(extro)
        (intro)
        (consc)
        (unsc)
        (agree)
        (disagree)
        (neutral_emotion)
        (neutral_emotion_r)
        (happy_emotion)
        (happy_emotion_r)
        (anger_emotion)
        (anger_emotion_r)
        (sad_emotion)
        (sad_emotion_r)
        (surprise_emotion)
        (surprise_emotion_r)
        (fear_emotion)
        (fear_emotion_r)
        (disgust_emotion)
        (disgust_emotion_r)
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


(:action REACT_DISGUST_EMOTION
        :precondition
                (and
                   (disgust_emotion)
                   (not (emotion_r))
                   (not (disgust_emotion_r))
                )

        :effect
                (and
                   (when (disagree)(increase (agreeableness_level)(*(agreeableness_coefficient)(react))))
                   (when (agree)(decrease (agreeableness_level)(*(agreeableness_coefficient)(react))))
                   (when (consc)(decrease (scrupulousness_level)(*(conscientious_coefficient)(react)))) 
		   (disgust_emotion_r)
                   (emotion_r)	
                )
)


(:action REACT_FEAR_EMOTION
        :precondition
                (and
                   (fear_emotion)
                   (not (emotion_r))
                   (not (fear_emotion_r))
                )

        :effect
                (and
                   (when (disagree)(increase (agreeableness_level)(*(agreeableness_coefficient)(react))))
                   (when (agree)(decrease (agreeableness_level)(*(agreeableness_coefficient)(react))))
                   (when (consc)(decrease (scrupulousness_level)(*(conscientious_coefficient)(react)))) 
		   (fear_emotion_r)
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

(:action REACT_SURPRISE_EMOTION
        :precondition
                (and
                   (surprise_emotion) 
                   (not (emotion_r))
                   (not (surprise_emotion_r))
                )

        :effect
                (and
                   (when (disagree)(decrease (agreeableness_level)(*(agreeableness_coefficient)(react))))
                   (when (agree)(increase (agreeableness_level)(*(agreeableness_coefficient)(react))))
                   (when (extro)(increase (interaction_level)(*(extroversion_coefficient)(react))))    
		   (surprise_emotion_r)
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




(:action ANSWER_A_RESPONSE
        :precondition
               (and 
                           
                           (emotion_r)
                           (>=(interaction_level)(desired_interaction))
                           (>=(scrupulousness_level)(desired_scrupulousness))
                           (>=(agreeableness_level)(desired_agreeableness))
                        
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (answered)                 
                )
)


(:action CHECK_FINISH
        :precondition
                (and
                        
                        (emotion_r)
                        (>=(interaction_level)(desired_interaction))
                        (>=(scrupulousness_level)(desired_scrupulousness))
                        (>=(agreeableness_level)(desired_agreeableness))
                        (answered)
                )

        :effect
                (and    
			(finished)
			
                )
)

)