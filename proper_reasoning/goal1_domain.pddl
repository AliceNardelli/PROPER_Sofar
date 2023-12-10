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
        (feel_comfort)
	(answered)
        (new_sentence)
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
        (attention)
        (attention_r)
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


(:action REACT_ATTENTION
        :precondition
                (and
                   (attention)
                   (not (attention_r))
                )

        :effect
                (and
                   (when (agree)(decrease (agreeableness_level)(*(agreeableness_coefficient)(react))))
                   (when (consc)(decrease (scrupulousness_level)(*(conscientious_coefficient)(react))))
                   (when (extro)(decrease (interaction_level)(*(extroversion_coefficient)(react)))) 
                   (when (intro)(increase (interaction_level)(*(extroversion_coefficient)(react))))      
		   (attention_r)  
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




(:action ANSWER
        :precondition
               (and 
                           (new_sentence)
                           (emotion_r)
                           (attention_r)  
                           (>=(interaction_level)(desired_interaction))
                           (>=(scrupulousness_level)(desired_scrupulousness))
                           (>=(agreeableness_level)(desired_agreeableness))
                           (not (answered))
                )
        :effect
                (and
                           
                           (when (intro) (decrease (interaction_level)(*(extroversion_coefficient)(-(dur)3))))
                           (when (extro) (decrease (interaction_level)(*(extroversion_coefficient)(+(dur)3))))
                           (when (consc) (decrease (scrupulousness_level)(*(conscientious_coefficient)(-(dur)3))))
                           (when (unsc) (decrease (scrupulousness_level)(*(conscientious_coefficient)(+(dur)3))))
                           (when (agree) (decrease (agreeableness_level)(*(agreeableness_coefficient)(-(dur)3))))
                           (when (disagree) (decrease (agreeableness_level)(*(agreeableness_coefficient)(+(dur)3))))
                           (answered)                 
                )
)


(:action ANSWER_WITH_A_QUESTION
        :precondition
               (and 
                           (new_sentence)
                           (emotion_r)
                           (attention_r)  
                           (>=(interaction_level)(desired_interaction))
                           (>=(scrupulousness_level)(desired_scrupulousness))
                           (>=(agreeableness_level)(desired_agreeableness))
                           (not (answered))
                        
                )
        :effect
                (and
                           
                           (when (intro) (decrease (interaction_level)(*(extroversion_coefficient)(+(dur)3))))
                           (when (extro) (decrease (interaction_level)(*(extroversion_coefficient)(-(dur)3))))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(+(dur)10)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(+(dur)10)))
                           (answered)                 
                )
)


(:action ANSWER_WITH_A_NEGATION
        :precondition
               (and 
                           
                           (emotion_r)
                           (new_sentence)
                           (attention_r)  
                           (>=(interaction_level)(desired_interaction))
                           (>=(scrupulousness_level)(desired_scrupulousness))
                           (>=(agreeableness_level)(desired_agreeableness))
                           (not (answered))
                        
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(+(dur)10)))
                           (when (disagree) (decrease (agreeableness_level)(*(agreeableness_coefficient)(-(dur)3))))
                           (when (agree) (decrease (agreeableness_level)(*(agreeableness_coefficient)(+(dur)3))))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(+(dur)10)))
                           (answered)                 
                )
)

(:action ANSWER_RANDOMLY
        :precondition
               (and 
                           
                           (emotion_r)
                           (new_sentence)
                           (attention_r)  
                           (>=(interaction_level)(desired_interaction))
                           (>=(scrupulousness_level)(desired_scrupulousness))
                           (>=(agreeableness_level)(desired_agreeableness))
                           (not (answered))
                        
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(+(dur)10)))
                           (decrease (agreeableness_level)(*(agreeableness_level)(+(dur)10)))
                           (when (unsc) (decrease (scrupulousness_level)(*(conscientious_coefficient)(-(dur)3))))
                           (when (consc) (decrease (scrupulousness_level)(*(conscientious_coefficient)(+(dur)3))))
                           (answered)                 
                )
)


(:action COMPUTE_HEDONIC_FEELINGS
        :precondition
                (and
                        
                        (emotion_r)
                        (attention_r)  
                        (>=(interaction_level)(desired_interaction))
                        (>=(scrupulousness_level)(desired_scrupulousness))
                        (>=(agreeableness_level)(desired_agreeableness))
                )

        :effect
                (and    
			(feel_comfort)
			
                )
)

(:action CHECK_FINISH
        :precondition
                (and
                        
                        (emotion_r)
                        (attention_r)  
                        (answered)
                        (>=(interaction_level)(desired_interaction))
                        (>=(scrupulousness_level)(desired_scrupulousness))
                        (>=(agreeableness_level)(desired_agreeableness))
                )

        :effect
                (and    
			(finished)
			
                )
)

)
