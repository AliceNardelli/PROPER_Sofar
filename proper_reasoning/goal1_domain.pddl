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
        (present)
        (finished)
	(hint_given)
        (new_hint)
        (answered)
        (new_sentence)
        (present_quiz)
        (guessed_quiz)
        (finished_quiz)
        (sentence_said)
        (game_finished) 
        (number_said) 
        (number_seen)
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
        (low_attention)
        (low_attention_r)
        (waited)  
        (executed_task)
        (wrong_number)
)


(:action EXTRO_ACTION
        :precondition
               (and 
               	(extro)
                (executed_task)
                (wrong_number)
                (answered) 
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
               (executed_task)
               (wrong_number)
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
                (executed_task)
                (wrong_number)
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
                (executed_task)
                (wrong_number)
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
                (executed_task)
                (wrong_number)
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
                (executed_task)
                (wrong_number)
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
                   (not (disgust_emotion))
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
                   (not (fear_emotion))
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
		   (surprise_emotion_r)
                   (emotion_r)
                   (not (surprise_emotion))	
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


(:action WAIT
        :precondition
               (and 
                           (sentence_said)
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (wrong_number)
                           (>(interaction_level)(desired_interaction))
                           (>(scrupulousness_level)(desired_scrupulousness))
                           (>(agreeableness_level)(desired_agreeableness))
                )
        :effect
                (and
                           (waited)   
                           (when (not(new_hint))(executed_task))          
                )
)


(:action SAY_NUMBER
        :precondition
               (and 
                           
                           
                           (number_seen)
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                )
        :effect
                (and
                           (decrease (interaction_level)(*(conscientious_coefficient)(dur)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (not(number_seen)) 
                           (number_said)  
                           (executed_task)              
                )
)


(:action GIVE_HINT
        :precondition
               (and 
                           (new_hint)
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (not (hint_given))
                           (present_quiz)
                           (wrong_number)
                )
        :effect
                (and
                           (decrease (interaction_level)(*(conscientious_coefficient)(dur)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (hint_given)
                           (not(new_hint)) 
                           (executed_task)                
                )
)


(:action SAY_SENTENCE
        :precondition
               (and 
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (present_quiz)
                           (wrong_number)
                )
        :effect
                (and
                           (decrease (interaction_level)(*(conscientious_coefficient)(dur)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (sentence_said) 
                                         
                )
)

(:action SAY_WRONG
        :precondition
               (and 
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (not (wrong_number))
                )
        :effect
                (and
                           (decrease (interaction_level)(*(conscientious_coefficient)(dur)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (wrong_number)           
                )
)


(:action PRESENT_ESCAPE_ROOM
        :precondition
               (and 
                           
                           (emotion_r)
                           (attention_r)  
                           (low_attention_r)
                           (not(present))
                           (wrong_number)
                        
                )
        :effect
                (and
                           (decrease (interaction_level)(*(conscientious_coefficient)(dur)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (present)               
                )
)


(:action PRESENT_QUIZ
        :precondition
               (and 
                           
                           (emotion_r)
                           (attention_r)  
                           (low_attention_r)
                           (present)
                           (not(present_quiz))
                           (wrong_number)
                        
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(conscientious_coefficient)(dur)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (present_quiz) 
                           (executed_task)             
                )
)


(:action GUESS_QUIZ
        :precondition
               (and 
                           
                           (emotion_r)
                           (attention_r)  
                           (low_attention_r)
                           (present_quiz)
                           (guessed_quiz)
                           (not(finished_quiz))
                           (number_said) 
                           (sentence_said)
                           (wrong_number)
                              
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(conscientious_coefficient)(dur)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (not(guessed_quiz))
                           (finished_quiz) 
                           (executed_task)                        
                )
)


(:action CHECK_FINISH
        :precondition
                (and
                        
                        (emotion_r)
                        (attention_r) 
                        (low_attention_r)   
                        (not(game_finished))
                        (finished_quiz)
                        (>(interaction_level)(desired_interaction))
                        (>(scrupulousness_level)(desired_scrupulousness))
                        (>(agreeableness_level)(desired_agreeableness))
                        (wrong_number)
                )

        :effect
        
                (and    
			(game_finished)
                        (executed_task) 
			
                )
)

)
