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
        (presented_task ?r - room)
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
)


(:durative-action CHIT_CHAT
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

(:durative-action APPROACH_HUMAN
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

(:durative-action EXPRESS_ENTHUSIASM
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


(:durative-action CHECK_HUMAN_WORK
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

(:durative-action REMIND_TO_PAY_ATTENTION
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


(:durative-action WAIT
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

(:durative-action RANDOM_ACTION
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



(:durative-action SHOW_EMPATHY
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

(:durative-action PLEASURE_HUMANS
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

(:durative-action ASK_IF_NEED_HELP
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


(:durative-action SAY_ROBOT_WORK_BETTER
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

(:durative-action TRY_REPLACE_THE_HUMAN
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

(:durative-action BE_ARROGANT
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


(:durative-action REACHING_PRODUCTION_ROOM
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
                )

        :effect
                (and    
                        (at end (not (computed_e)))
                        (at end (not (computed_c)))
                        (at end (not (computed_a)))
                        (at end (not (at ?l1)))
                        (at end (at ?l2))
                        (at end (assign (dur) 10))
                )
)


(:durative-action REACHING_ASSEMBLY_ROOM
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
                )

        :effect
                (and
                        (at end (not (at ?l1)))
                        (at end (at ?l2))
                        (at end (not (computed_e)))
                        (at end (not (computed_c)))
                        (at end (not (computed_a)))
                        (at end (assign (dur) 10))
                )
)

(:durative-action PRESENT_ASSEMBLY_ROOM
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
                )

        :effect
                (and
                        (at end (presented_task ?l1))
                        (at end (not (computed_e)))
                        (at end (not (computed_c)))
                        (at end (not (computed_a)))
                        (at end (assign (dur) 7))
                )
)



(:durative-action PRESENT_PRODUCTION_ROOM
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
                )

        :effect
                (and
                        (at end (presented_task ?l1))
                        (at end (not (computed_e)))
                        (at end (not (computed_c)))
                         (at end (not (computed_a)))
                        (at end (assign (dur) 7))
                )
)

(:durative-action ASK_PICK_THE_BLOCK
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
                )
        :effect
                (and
                        (at end (not(empty_robot)))
                        (at end (block_to_deliver))
                        (at end (not (computed_e)))
                        (at end (not (computed_c)))
                        (at end (not (computed_a)))
                        (at end (assign (dur) 5))
                )
)


(:durative-action ASK_ASSEMBLY_BLOCK
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
                )
)



(:action COMPUTE_METRIC_INTRO
    :precondition (and 
         (not (computed_e))  
         (intro) 
    )
    :effect (and
    	   (computed_e)
           (decrease (interaction_level)(*(extroversion_coefficient)(dur)))
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

(:action CHECK_FINISHED
    :parameters (?l1 - room)
    :precondition (and 
            (at ?l1)
            (assembly_room ?l1)
            (>(no_blocks)(max_no_blocks))
    )
    :effect 
      (and
    	    (finished)
    )
)
)
