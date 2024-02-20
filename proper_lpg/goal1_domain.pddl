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
        (replace)    
)

(:predicates 
        
        (to_assign_dominance) 
        (finished)
        (feel_comfort)
        (new_block)
        (action1_move)
        (action2)
        (action1_say)
        (human_start)
        (robot_start)
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


)

(:action ASSIGN_DOMINANCE
        :precondition
               (and
               (not(to_assign_dominance))  
                )
        :effect
                (and
                (when (extro)(robot_start))
                (when (intro)(human_start))
                (when (disagree)(robot_start))
                (when (agree)(human_start))
                (to_assign_dominance) 
                )
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



(:action PICK_PLACE_ROBOT_PRECISE_TURN1
        :precondition
               (and 
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (new_block)
                           (robot_start) 
                         
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (when (consc)(increase (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (when (unsc)(decrease (scrupulousness_level)(*(conscientious_coefficient)(+(dur)6))))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (action1_move) 
                           (not (new_block)) 
                               
                )
)

(:action PICK_PLACE_ROBOT_WRONG_TURN1
        :precondition
               (and 
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (new_block)
                           (robot_start)    
                           (unsc)
                           (>(conscientious_coefficient)0)
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (when (unsc)(increase (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (when (consc)(decrease (scrupulousness_level)(*(conscientious_coefficient)(+(dur)6))))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (action1_move)  
                           (not (new_block))      
                )
)



(:action PICK_PLACE_ROBOT_PRECISE_TURN2
        :precondition
               (and 
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r) 
                           (action1_say)   
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (when (consc)(increase (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (when (unsc)(decrease (scrupulousness_level)(*(conscientious_coefficient)(+(dur)6))))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (action2) 
                           (not (action1_say)) 
                           (not(to_assign_dominance))      
                )
)


(:action PICK_PLACE_ROBOT_WRONG_TURN2
        :precondition
               (and 
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (unsc)
                           (>(conscientious_coefficient)0) 
                           (action1_say)   
                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (when (unsc)(increase (scrupulousness_level)(*(conscientious_coefficient)(dur))))
                           (when (consc)(decrease (scrupulousness_level)(*(conscientious_coefficient)(+(dur)6))))
                           (decrease (agreeableness_level)(*(agreeableness_coefficient)(dur)))
                           (action2) 
                           (not (action1_say))  
                           (not(to_assign_dominance))        
                )
)



(:action SAY_HUMAN_TABLET_TURN1
        :precondition
               (and 
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (new_block) 
                           (human_start)
                )
        :effect
                (and
                           
                           (when (intro)(increase (interaction_level)(*(extroversion_coefficient)(dur))))
                           (when (extro)(decrease (interaction_level)(*(extroversion_coefficient)(+(dur)4))))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (when (disagree)(decrease (agreeableness_level)(*(agreeableness_coefficient)(dur))))
                           (when (agree)(increase (agreeableness_level)(*(agreeableness_coefficient)(dur))))
                           (action1_say)
                           (not (new_block)) 
                )
)

(:action SAY_HUMAN_VOICE_TURN1
        :precondition
               (and 
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (new_block) 
                           (human_start)
                )
        :effect
                (and
                           
                           (when (extro)(increase (interaction_level)(*(extroversion_coefficient)(dur))))
                           (when (intro)(decrease (interaction_level)(*(extroversion_coefficient)(+(dur)4))))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (when (disagree)(decrease (agreeableness_level)(*(agreeableness_coefficient)(dur))))
                           (when (agree)(increase (agreeableness_level)(*(agreeableness_coefficient)(dur))))
                           (action1_say)
                           (not (new_block)) 
                )
)


(:action PICK_PLACE_REPLACE_HUMAN_TURN1
        :precondition
               (and 
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (new_block) 
                           (human_start)
                           (disagree)
                           (>(agreeableness_coefficient)0)
                           (<(replace) 1)
                        

                )
        :effect
                (and
                           
                           (decrease (interaction_level)(*(extroversion_coefficient)(+(dur)2)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(+(dur)2)))
                           (when (agree)(decrease (agreeableness_level)(*(agreeableness_coefficient)(+(dur)4))))
                           (when (disagree)(increase (agreeableness_level)(*(agreeableness_coefficient)(dur))))
                           (action1_say)
                           (not (new_block)) 
                           (increase(replace)1)
                )
)



(:action SAY_HUMAN_VOICE_TURN2
        :precondition
               (and 
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (action1_move)
                )
        :effect
                (and
                           
                           (when (extro)(increase (interaction_level)(*(extroversion_coefficient)(dur))))
                           (when (intro)(decrease (interaction_level)(*(extroversion_coefficient)(+(dur)4))))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (when (disagree)(decrease (agreeableness_level)(*(agreeableness_coefficient)(dur))))
                           (when (agree)(increase (agreeableness_level)(*(agreeableness_coefficient)(dur))))
                           (action2)
                           (not(action1_move))
                           (not(to_assign_dominance))  
                )
)

(:action SAY_HUMAN_TABLET_TURN2
        :precondition
               (and 
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (action1_move)
                )
        :effect
                (and
                           (when (intro)(increase (interaction_level)(*(extroversion_coefficient)(dur))))
                           (when (extro)(decrease (interaction_level)(*(extroversion_coefficient)(+(dur)4))))
                           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(dur)))
                           (when (disagree)(decrease (agreeableness_level)(*(agreeableness_coefficient)(dur))))
                           (when (agree)(increase (agreeableness_level)(*(agreeableness_coefficient)(dur))))
                           (action2)
                           (not(action1_move))
                           (not(to_assign_dominance))  
                )
)


(:action PICK_PLACE_REPLACE_HUMAN_TURN2
        :precondition
               (and 
                           (emotion_r)
                           (attention_r) 
                           (low_attention_r)
                           (action1_move)
                           (disagree)
                           (>(agreeableness_coefficient)0)
                           (<(replace) 1)
                          
                )
        :effect
                (and
                           (decrease (interaction_level)(*(extroversion_coefficient)(+(dur)2)))
                           (decrease (scrupulousness_level)(*(conscientious_coefficient)(+(dur)2)))
                           (when (agree)(decrease (agreeableness_level)(*(agreeableness_coefficient)(+(dur)4))))
                           (when (disagree)(increase (agreeableness_level)(*(agreeableness_coefficient)(dur))))
                           (action2)
                           (not(action1_move))
                           (not(to_assign_dominance))  
                           (increase(replace)1)
                )
)
(:action COMPUTE_HEDONIC_FEELINGS
        :precondition
                (and
                        
                        (emotion_r)
                        (attention_r)  
                        (low_attention_r) 
                        (action2) 
                        (>(interaction_level)(desired_interaction))
                        (>(scrupulousness_level)(desired_scrupulousness))
                        (>(agreeableness_level)(desired_agreeableness))
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
                        (low_attention_r)   
                        (feel_comfort)
                        (>(interaction_level)(desired_interaction))
                        (>(scrupulousness_level)(desired_scrupulousness))
                        (>(agreeableness_level)(desired_agreeableness))
                )

        :effect
                (and    
			(finished)
			
                )
)

)