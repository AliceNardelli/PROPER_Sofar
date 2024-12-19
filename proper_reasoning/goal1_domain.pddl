(define (domain goal1)

(:requirements :adl :strips :typing :conditional-effects :negative-preconditions :equality :fluents )

(:types	
person
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
        (finished_sentence)
	(answered)
        (new_sentence)
        (person_present ?p - person)
        (person_there ?p - person)
        (greetings ?p - person)
        (ask_to_present ?p - person)
        (present_the_lab ?p - person)
        (ask_the_preferences ?p - person)
        (give_information ?p - person)
        (welcomed)
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
        (calm_emotion)
        (calm_emotion_r)
        (emotion_r)
        (attention)
        (attention_r)
        (low_attention)
        (low_attention_r)
)


(:action EXTRO_ACTION
        :precondition
               (and 
                (answered)
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
               (answered)
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
                (answered)
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
                (answered)
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
                (answered)
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
                (answered)
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
                   (when (agree)(increase (agreeableness_level)(*(agreeableness_coefficient)(react))))
                   (when (consc)(increase (scrupulousness_level)(*(conscientious_coefficient)(react))))
                   (when (extro)(increase (interaction_level)(*(extroversion_coefficient)(react)))) 
                   (when (intro)(decrease (interaction_level)(*(extroversion_coefficient)(react))))      
		   (attention_r)  
                   (not (attention))
                )
)

(:action REACT_LOW_ATTENTION
        :precondition
                (and
                   (low_attention)
                   (not (low_attention_r))
                )

        :effect
                (and
                   (when (agree)(decrease (agreeableness_level)(*(agreeableness_coefficient)(react))))
                   (when (consc)(decrease (scrupulousness_level)(*(conscientious_coefficient)(react))))
                   (when (extro)(decrease (interaction_level)(*(extroversion_coefficient)(react)))) 
                   (when (intro)(increase (interaction_level)(*(extroversion_coefficient)(react))))      
		   (low_attention_r)  
                   (not (low_attention))
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
                   (not(sad_emotion))
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
                   (not (anger_emotion))
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
		   (happy_emotion_r)
                   (emotion_r)	
                   (not (happy_emotion))
                )
)


(:action REACT_CALM_EMOTION
        :precondition
                (and
                   (calm_emotion) 
                   (not (emotion_r))
                   (not (calm_emotion_r))
                )

        :effect
                (and
                   (when (disagree)(decrease (agreeableness_level)(*(agreeableness_coefficient)(react))))
                   (when (agree)(increase (agreeableness_level)(*(agreeableness_coefficient)(react))))   
                   (when (extro)(decrease (interaction_level)(*(extroversion_coefficient)(react))))
                   (when (intro)(increase (interaction_level)(*(extroversion_coefficient)(react))))
		   (calm_emotion_r)
                   (emotion_r)	
                   (not (calm_emotion))
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
                   (not (neutral_emotion))
                   (when (extro)(decrease (interaction_level)(*(extroversion_coefficient)(react))))
                   (when (intro)(increase (interaction_level)(*(extroversion_coefficient)(react))))	
                )
)


(:action GREET
        :parameters 
                (?p - person)
        :precondition
               (and 
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (person_present ?p)
                           (person_there ?p)
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (greetings ?p)
                           (welcomed)
                           (not (person_present ?p))
                           (answered)                 
                )
)


(:action ASK_PRESENT
        :parameters 
                (?p - person)
        :precondition
               (and 
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (welcomed)
                           (person_there ?p)
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (ask_to_present ?p)
                           (answered)   
                           (not (greetings ?p))              
                )
)


(:action PRESENT_LAB
        :parameters 
                ( ?p - person)
        :precondition
               (and 
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (welcomed)
                           (ask_to_present ?p)
                           (person_there ?p)
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (present_the_lab ?p)
                           (not (ask_to_present ?p))
                           (answered)                 
                )
)



(:action ASK_PREFERENCES
        :parameters 
                (?p - person)
        :precondition
               (and 
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (welcomed)
                           (present_the_lab ?p)
                           (person_there ?p)
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (ask_the_preferences ?p)
                           (not (present_the_lab ?p))
                           (answered)                 
                )
)



(:action GIVE_NEW_INFO
        :parameters 
                (?p - person)
        :precondition
               (and 
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (welcomed)
                           (ask_the_preferences ?p)
                           (person_there ?p)
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (not (ask_the_preferences ?p))
                           (give_information ?p)
                           (answered)                 
                )
)

(:action ANSWER
        :precondition
               (and 
                           (new_sentence)
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (not (answered))
                )
        :effect
                (and
                           
                           (when (intro) (increase (interaction_level)(*(extroversion_coefficient)(dur))))
                           (when (extro) (decrease (interaction_level)(*(extroversion_coefficient)(+(dur)4))))
                           (when (consc) (increase (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (when (unsc) (decrease (scrupulousness_level)(*(conscientious_coefficient)(+(dur)4))))
                           (when (agree) (increase (agreeableness_level)(*(agreeableness_coefficient)(dur))))
                           (when (disagree) (decrease (agreeableness_level)(*(agreeableness_coefficient)(+(dur)4))))
                           (answered)                 
                )
)

(:action ANSWER_WRONGLY
        :precondition
               (and 
                           (new_sentence)
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (not (answered))
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(+(dur)2)))
                           (when (unsc) (increase (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (when (consc) (decrease (scrupulousness_level)(*(conscientious_coefficient)(+(dur)4))))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(+(dur)2)))
                           (answered)                 
                )
)

(:action ANSWER_WITH_A_QUESTION
        :precondition
               (and 
                           (new_sentence)
                           (emotion_r)
                           (attention_r)  
                           (low_attention_r)
                           (not (answered))
                        
                )
        :effect
                (and
                           
                           (when (intro) (decrease (interaction_level)(*(extroversion_coefficient)(+(dur)4))))
                           (when (extro) (increase (interaction_level)(*(extroversion_coefficient)(dur))))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(+(dur)2)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(+(dur)2)))
                           (answered)                 
                )
)


(:action ANSWER_WITH_A_NEGATION
        :precondition
               (and 
                           
                           (emotion_r)
                           (new_sentence)
                           (attention_r)  
                           (low_attention_r)
                           (not (answered))
                        
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(+(dur)2)))
                           (when (disagree) (increase (agreeableness_level)(*(agreeableness_coefficient)(dur))))
                           (when (agree) (decrease (agreeableness_level)(*(agreeableness_coefficient)(+(dur)4))))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(+(dur)2)))
                           (answered)                 
                )
)


(:action CHECK_FINISH
        :parameters (?p - person)
        :precondition
                (and
                        
                        (emotion_r)
                        (attention_r) 
                        (low_attention_r)   
                        (answered)
                        (give_information ?p)
                        (>(interaction_level)(desired_interaction))
                        (>(scrupulousness_level)(desired_scrupulousness))
                        (>(agreeableness_level)(desired_agreeableness))
                )

        :effect
                (and    
			(finished)
			
                )
)


(:action CHECK_FINISH_SENTENCE
        :parameters (?p - person)
        :precondition
                (and
                        
                        (emotion_r)
                        (attention_r) 
                        (low_attention_r)   
                        (answered)
                        (>(interaction_level)(desired_interaction))
                        (>(scrupulousness_level)(desired_scrupulousness))
                        (>(agreeableness_level)(desired_agreeableness))
                )

        :effect
                (and    
			(finished_sentence)
			
                )
)

)
