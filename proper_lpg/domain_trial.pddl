(define (domain trial_dom)

(:requirements :adl :derived-predicates :strips :typing :conditional-effects :negative-preconditions :equality :fluents :durative-actions  :duration-inequalities :continuous-effects :time)

(:types
	room
)

(:functions
        (extroversion_coefficient)
        (desired_interaction)
        (interaction_level)
        (no)
)

(:predicates 
        (asked)
        (finished)
        (extro)
        (intro)
        (not_finished)
        
)

(:durative-action INTRO_ACTION
        :duration
                (= ?duration 10)
        :condition
                (and
                   (at start (intro))
                )

        :effect
                (and    
                     (at end (increase (interaction_level) 5))
                     (at end (increase (no) 1))
                )
)

(:durative-action EXTRO_ACTION
        :duration
                (= ?duration 10)
        :condition
                (and
                   (at start (extro))
                )

        :effect
                (and    
                     (at end (increase (interaction_level) 5))
                     (at end (increase (no) 1))
                )
)

(:durative-action ASK_FRIEND
        :duration
                (= ?duration 2)

        :condition
                (and
                        (at start (>=(interaction_level)(desired_interaction)))
                        (at start (not_finished))
                        (at start(intro)  )
                        (at start (not(asked)))
                )
        :effect
                (and  
                        (at end (decrease (interaction_level) 1))
                        (at end (asked))
                        (at end (increase (no) 1))
                )
)

(:durative-action FRIEND_CALL_THE_RESTAURANT      
        :duration
                (= ?duration 2)

        :condition
                (and
                        (at start (>=(interaction_level)(desired_interaction)))
                        (at start (asked))
                        (at start (not_finished))
                        (at start(intro) )
                )

        :effect
                (and  
                        (at end (increase (interaction_level) 5))
                        (at end (finished))
                        (at end (increase (no) 1))
                        (at end (not (not_finished)))
                )
)

(:durative-action CALL_THE_RESTAURANT       
        :duration
                (= ?duration 10)

        :condition
                (and
                        (at start (>=(interaction_level)(desired_interaction)))
                        (at start (not_finished))
                )

        :effect
                (and  
                        (at end (decrease (interaction_level) 10))
                        (at end (finished))
                        (at end (increase (no) 1))
                        (at end (not (not_finished)))
                )
)
)
