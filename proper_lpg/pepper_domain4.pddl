(define (domain PROPER_navigation)

(:requirements :adl :derived-predicates :strips :typing :conditional-effects :negative-preconditions :equality :fluents :durative-actions  :duration-inequalities :continuous-effects :time)

(:types
	room
)

(:functions
	(max_no_blocks)
	(no_blocks)
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
        (baseline)
)

(:predicates 
        (production_room ?r - room)
        (assembly_room ?r - room)
        (start_room ?r - room)
        (presented_task ?r - room)
        (goodbye ?r - room)
        (at ?r - room)
        (human_present) 
        (block_to_deliver)
        (empty_robot)
        (finished)
        (extro)
        (intro)
        (computed_e)
        (consc)
        (unsc)
        (computed_c)
        (agree)
        (disagree)
        (computed_a)
        (interactive_action)
        (not_interactive_action)
        (not_presented ?r -room)
        (can_move)
        (showed)
        (grasp)
)


(:durative-action EXPRESS_EXCITEMENT
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<(interaction_level)(desired_interaction)))
                   (at start (extro))
                )

        :effect
                (and    
                     (at end (increase (interaction_level)5))
                )
)


(:durative-action SHOW_EXCITEMENT
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<(interaction_level)(desired_interaction)))
                   (at start (extro))
                   (at start (not (grasp)))
                )

        :effect
                (and    
                     (at end (increase (interaction_level)5))
                )
)


(:durative-action SHOW_HAND
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<(interaction_level)(desired_interaction)))
                   (at start (extro))
                   (at start (not (grasp)))
                )

        :effect
                (and    
                     (at end (increase (interaction_level)5))
                )
)

(:durative-action EXPRESS_ENTHUSIASM_FOR_THE_LAST_ACHIEVED_ACTION
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<(interaction_level)(desired_interaction)))
                   (at start (extro))
                )

        :effect
                (and    
                     (at end (increase (interaction_level)5))
                )
)

(:durative-action EXPRESS_ENTHUSIASM_FOR_THE_NEXT_FUTURE_WORK
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<(interaction_level)(desired_interaction)))
                   (at start (extro))
                )

        :effect
                (and    
                     (at end (increase (interaction_level)5))
                )
)

(:durative-action CHAT
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<(interaction_level)(desired_interaction)))
                   (at start (extro))
                )

        :effect
                (and    
                     (at end (increase (interaction_level)5))
                )
)


(:durative-action SHOW_DETACHMENT
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<(interaction_level)(desired_interaction)))
                   (at start (intro))
                   (at start (not (grasp)))
                )

        :effect
                (and    
                     (at end (increase (interaction_level) 5))
                )
)

(:durative-action GO_NOT_CROWDED_AREA
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<(interaction_level)(desired_interaction)))
                   (at start (intro))
                )

        :effect
                (and    
                     (at end (increase (interaction_level) 5))
                )
)

(:durative-action TURN_ON_BACK
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<(interaction_level)(desired_interaction)))
                   (at start (intro))
                )

        :effect
                (and    
                     (at end (increase (interaction_level) 5))
                )
)

(:durative-action GO_FAR
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<(interaction_level)(desired_interaction)))
                   (at start (intro))
                )

        :effect
                (and    
                     (at end (increase (interaction_level) 5))
                )
)


(:durative-action MOVE_TO_CHECK_HUMAN_WORKING_STATION
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


(:durative-action SAY_TO_NOT_DISTRACT
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

(:durative-action SAY_TO_PAY_ATTENTION
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

(:durative-action SAY_TO_FOCUS_ON_FUTURE_WORK
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

(:durative-action SAY_THEY_HAVE_A_GOAL_TO_ACHIEVE
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


(:durative-action GO_IN_A_RANDOM_POSITION
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

(:durative-action LATE
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

(:durative-action SHOW_RANDOM_MOVEMENT
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<(scrupulousness_level)(desired_scrupulousness)))
                   (at start (unsc))
                   (at start (not (grasp)))
                )

        :effect
                (and    
                     (at end (increase (scrupulousness_level) 5))
                )
)

(:durative-action CHAT_UNSC
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

(:durative-action SAY_NO_MATTER_ABOUT_THE_TASK
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


(:durative-action ASK_IF_HUMAN_NEED_HELP
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

(:durative-action SAY_THAT_YOU_KNOW_IT_IS_A_DIFFICULT_TASK
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

(:durative-action SAY_TO_NOT_MATTER_IF_AN_ERROR_OCCUR
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

(:durative-action SAY_YOU_ARE_SORRY_FOR_THE_FATIGUE
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

(:durative-action SAY_THE_HUMAN_HE_IS_DOING_A_GOOD_WORK
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


(:durative-action SAY_THAT_YOU_WOULD_PERFORM_AN_ACTION_DIFFERENTLY
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

(:durative-action SAY_THE_HUMAN_SHOULD_WORK_BETTER
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

(:durative-action SAY_TO_WORK_MORE_FAST
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

(:durative-action SHOW_DISGUST
        :duration
                (= ?duration 5)
        :condition
                (and
                   (at start (<(agreeableness_level)(desired_agreeableness)))
                   (at start (disagree))
                   (at start (not (grasp)))
                )

        :effect
                (and    
                     (at end (increase (agreeableness_level) 5))
                )
)

(:durative-action MOVE_TO_PRODUCTION_ROOM
        :parameters
                 (?l1 ?l2 - room)
        :duration
                (= ?duration 10)

        :condition
                (and
                        (at start (at ?l1))
                        (at start (production_room ?l2))
                        (at start (>=(interaction_level)(desired_interaction)))
                        (at start (>=(scrupulousness_level)(desired_scrupulousness)))
                        (at start (>=(agreeableness_level)(desired_agreeableness)))
                        (at start (computed_e))
                        (at start (computed_c))
                        (at start (computed_a))
                        (at start (can_move))
                        (at start(not(finished)))
                )

        :effect
                (and    
                        (at end (not (computed_e)))
                        (at end (not (computed_c)))
                        (at end (not (computed_a)))
                        (at end (not (at ?l1)))
                        (at end (at ?l2))
                        (at end (assign (dur) 10))
                        (at end(not_interactive_action))
                        (at end(not(interactive_action)))
                        (at end (not (can_move)))
                        (at end (not (showed)))
                        (at end (not (grasp)))
                )
)


(:durative-action MOVE_TO_ASSEMBLY_ROOM
        :parameters
                 (?l1 ?l2 - room)
        :duration
                (= ?duration 10)

        :condition
                (and
                        (at start (computed_e))
                        (at start (at ?l1))
                        (at start (assembly_room ?l2))
                        (at start (>=(interaction_level)(desired_interaction)))
                        (at start (>=(scrupulousness_level)(desired_scrupulousness)))
                        (at start (>=(agreeableness_level)(desired_agreeableness)))
                        (at start (computed_c))
                        (at start (computed_a))
                        (at start (can_move))
                        (at start(not(finished)))
                )

        :effect
                (and
                        (at end (not (at ?l1)))
                        (at end (at ?l2))
                        (at end (not (computed_e)))
                        (at end (not (computed_c)))
                        (at end (not (computed_a)))
                        (at end (assign (dur) 10))
                        (at end(not_interactive_action))
                        (at end(not(interactive_action)))
                        (at end (not (can_move)))
                        (at end (not (showed)))
                        (at end (not (grasp)))
                )
)

(:durative-action SPEAK_ABOUT_ASSEMBLY_ROOM
        :parameters
                 (?l1  - room)
        :duration
                (= ?duration 7)

        :condition
                (and
                        (at start (computed_e))
                        (at start (computed_c))
                        (at start (computed_a))
                        (at start (at ?l1))
                        (at start (assembly_room ?l1))
                        (at start (>=(interaction_level)(desired_interaction)))
                        (at start (>=(scrupulousness_level)(desired_scrupulousness)))
                        (at start (>=(agreeableness_level)(desired_agreeableness)))
                        (at start (not_presented ?l1))
                        (at start(not(finished)))
                )

        :effect
                (and
                        (at end (presented_task ?l1))
                        (at end (not (computed_e)))
                        (at end (not (computed_c)))
                        (at end (not (computed_a)))
                        (at end (assign (dur) 7))
                        (at end(interactive_action))
                        (at end(not(not_interactive_action)))
                        (at end (not (not_presented ?l1)))
                        (at end (can_move))
                        (at end (not (showed)))
                        (at end (not (grasp)))
                )
)



(:durative-action SPEAK_ABOUT_PRODUCTION_ROOM
        :parameters
                 (?l1  - room)
        :duration
                (= ?duration 7)

        :condition
                (and
                        (at start (computed_e))
                        (at start (computed_c))
                        (at start (computed_a))
                        (at start (at ?l1))
                        (at start (production_room ?l1))
                        (at start (>=(interaction_level)(desired_interaction)))
                        (at start (>=(scrupulousness_level)(desired_scrupulousness)))
                        (at start (>=(agreeableness_level)(desired_agreeableness)))
                        (at start (not_presented ?l1))
                        (at start(not(finished)))
                )

        :effect
                (and
                        (at end (presented_task ?l1))
                        (at end (not (computed_e)))
                        (at end (not (computed_c)))
                        (at end (not (computed_a)))
                        (at end (assign (dur) 7))
                        (at end(interactive_action))
                        (at end(not(not_interactive_action)))
                        (at end (not (not_presented ?l1)))
                        (at end (can_move))
                        (at end (not (showed)))
                        (at end (not (grasp)))
                )
)


(:durative-action ASK_PICK_THE_BLOCK_VOICE
        :parameters
               (?l1  - room)
        :duration
                (= ?duration 5)

        :condition
               (and 
                        (at start (computed_e))
                        (at start (computed_c))
                        (at start (computed_a))
                        (at start (at ?l1))
                        (at start(production_room ?l1))
                        (at start(presented_task ?l1))
                        (at start(human_present)) 
                        (at start(empty_robot)) 
                        (at start (>=(interaction_level)(desired_interaction)))
                        (at start (>=(scrupulousness_level)(desired_scrupulousness)))
                        (at start (>=(agreeableness_level)(desired_agreeableness)))
                        (at start(not(finished)))
                        
                )
        :effect
                (and
                        (at end (not(empty_robot)))
                        (at end (block_to_deliver))
                        (at end (not (computed_e)))
                        (at end (not (computed_c)))
                        (at end (not (computed_a)))
                        (at end (assign (dur) 5))
                        (at end(interactive_action))
                        (at end(not(not_interactive_action)))
                        (at end (not (showed)))
                        (at end (can_move))  
                        (at end (grasp))                    
                )
)


(:durative-action ASK_PICK_THE_BLOCK_TABLET
        :parameters
               (?l1  - room)
        :duration
                (= ?duration 5)

        :condition
               (and 
                        (at start (computed_e))
                        (at start (computed_c))
                        (at start (computed_a))
                        (at start (at ?l1))
                        (at start(production_room ?l1))
                        (at start(presented_task ?l1))
                        (at start(human_present)) 
                        (at start(empty_robot)) 
                        (at start (>=(interaction_level)(desired_interaction)))
                        (at start (>=(scrupulousness_level)(desired_scrupulousness)))
                        (at start (>=(agreeableness_level)(desired_agreeableness)))
                        (at start(not(finished)))
                       
                )
        :effect
                (and
                        (at end (not(empty_robot)))
                        (at end (block_to_deliver))
                        (at end (not (computed_e)))
                        (at end (not (computed_c)))
                        (at end (not (computed_a)))
                        (at end (assign (dur) 5))
                        (at end(interactive_action))
                        (at end(not(not_interactive_action)))
                        (at end (can_move))
                        (at end (showed))
                        (at end (grasp))
                        
                )
)


(:durative-action ASK_ASSEMBLY_BLOCK_VOICE
        :parameters
                 (?l1  - room)
        :duration
                (= ?duration 5)

        :condition
               (and 
                        (at start (computed_e))
                        (at start (computed_c))
                        (at start (computed_a))
                        (at start (at ?l1))
                        (at start(assembly_room ?l1))
                        (at start(presented_task ?l1))
                        (at start(human_present)) 
                        (at start(block_to_deliver)) 
                        (at start (>=(interaction_level)(desired_interaction)))
                        (at start (>=(scrupulousness_level)(desired_scrupulousness)))
                        (at start (>=(agreeableness_level)(desired_agreeableness)))
                        (at start(not(finished)))
                       
                )
        :effect
                (and
                        (at end (not (computed_e)))
                        (at end (not (computed_c)))
                        (at end (not (computed_a)))
                        (at end (empty_robot))
                        (at end (not(block_to_deliver)))
                        (at end (increase (no_blocks) 1))
                        (at end (assign (dur) 5))
                        (at end(interactive_action))
                        (at end(not(not_interactive_action)))
                        (at end (not (showed)))
                        (at end (can_move))  
                        (at end (not(grasp)))
                )
)


(:durative-action ASK_ASSEMBLY_BLOCK_TABLET
        :parameters
                 (?l1  - room)
        :duration
                (= ?duration 5)

        :condition
               (and 
                        (at start (computed_e))
                        (at start (computed_c))
                        (at start (computed_a))
                        (at start (at ?l1))
                        (at start(assembly_room ?l1))
                        (at start(presented_task ?l1))
                        (at start(human_present)) 
                        (at start(block_to_deliver)) 
                        (at start (>=(interaction_level)(desired_interaction)))
                        (at start (>=(scrupulousness_level)(desired_scrupulousness)))
                        (at start (>=(agreeableness_level)(desired_agreeableness)))
                        (at start(not(finished)))
                       
                )
        :effect
                (and
                        (at end (not (computed_e)))
                        (at end (not (computed_c)))
                        (at end (not (computed_a)))
                        (at end (empty_robot))
                        (at end (not (block_to_deliver)))
                        (at end (increase (no_blocks) 1))
                        (at end (assign (dur) 5))
                        (at end(interactive_action))
                        (at end(not(not_interactive_action)))
                        (at end (showed))
                        (at end (can_move))  
                        (at end (not(grasp))) 
                )
)


(:durative-action SAY_GOODBYE_PRODUCTION_ROOM
        :parameters
                 (?l1  - room)
        :duration
                (= ?duration 2)

        :condition
               (and 
                        (at start (block_to_deliver))
                        (at start (computed_e))
                        (at start (computed_c))
                        (at start (computed_a))
                        (at start (at ?l1))
                        (at start(production_room ?l1))
                        (at start(human_present)) 
                        (at start (>=(interaction_level)(desired_interaction)))
                        (at start (>=(scrupulousness_level)(desired_scrupulousness)))
                        (at start (>=(agreeableness_level)(desired_agreeableness)))
                        (at start (<=(no_blocks)(max_no_blocks)))
                        (at start (>(no_blocks)(-(max_no_blocks)1)))

                )
        :effect
                (and
                        (at end (not (computed_e)))
                        (at end (not (computed_c)))
                        (at end (not (computed_a)))
                        (at end (assign (dur) 2))
                        (at end (goodbye ?l1))
                        (at end(interactive_action))
                        (at end(not(not_interactive_action)))
                        (at end (can_move))
                        (at end (not (showed)))
                        (at end (not(grasp)))
                )
)


(:durative-action SAY_GOODBYE_ASSEMBLY_ROOM
        :parameters
                 (?l1  - room)
        :duration
                (= ?duration 2)

        :condition
               (and 
                        (at start (empty_robot))
                        (at start (computed_e))
                        (at start (computed_c))
                        (at start (computed_a))
                        (at start (at ?l1))
                        (at start(assembly_room ?l1))
                        (at start(human_present)) 
                        (at start (>=(interaction_level)(desired_interaction)))
                        (at start (>=(scrupulousness_level)(desired_scrupulousness)))
                        (at start (>=(agreeableness_level)(desired_agreeableness)))
                        (at start (>(no_blocks)(max_no_blocks)))

                )
        :effect
                (and
                        (at end (not (computed_e)))
                        (at end (not (computed_c)))
                        (at end (not (computed_a)))
                        (at end (assign (dur) 2))
                        (at end (goodbye ?l1))
                        (at end(interactive_action))
                        (at end(not(not_interactive_action)))
                        (at end (can_move))
                        (at end (not (showed)))
                        (at end (not(grasp)))
                )
)

(:action COMPUTE_METRIC_INTRO_IA
    :precondition (and 
        (not (computed_e))  
        (intro) 
        (interactive_action)
        (not(showed))
    )
    :effect (and
    	(computed_e)
        (decrease (interaction_level)(*(extroversion_coefficient)(+(dur)10)))
        )
)

(:action COMPUTE_METRIC_INTRO_IA_SHOW
    :precondition (and 
        (not (computed_e))  
        (intro) 
        (interactive_action)
        (showed)
    )
    :effect (and
    	(computed_e)
        (increase (interaction_level)(*(extroversion_coefficient)(dur)))
        )
)

(:action COMPUTE_METRIC_INTRO_NIA
    :precondition (and 
        (not (computed_e))  
        (intro) 
        (not_interactive_action)
        (not(showed))
    )
    :effect (and
    	(computed_e)
        (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
        )
)

(:action COMPUTE_METRIC_EXTRO_IA_SHOW
    :precondition (and 
        (not (computed_e))  
        (extro)
        (interactive_action) 
        (showed)
    )
    :effect 
    (and
    	(computed_e)
        (decrease (interaction_level)(*(extroversion_coefficient)(+(dur)10)))
    )
)

(:action COMPUTE_METRIC_EXTRO_IA
    :precondition (and 
        (not (computed_e))  
        (extro)
        (interactive_action) 
        (not(showed))
    )
    :effect 
    (and
    	(computed_e)
        (increase (interaction_level)(*(extroversion_coefficient)(dur)))
    )
)

(:action COMPUTE_METRIC_EXTRO_NIA
    :precondition (and 
        (not (computed_e))  
        (extro)
        (not_interactive_action) 
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

(:action CHECK_FINISHED
    :parameters (?l1 ?l2 - room)
    :precondition (and 
            (at ?l1)
            (assembly_room ?l1)
            (production_room ?l2)
            (goodbye ?l1)
            (goodbye ?l2)
    )
    :effect 
      (and
    	    (finished)
    )
)
)
