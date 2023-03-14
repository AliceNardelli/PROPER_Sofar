(define (domain wm_interactive_task)
(:requirements :strips 
               :typing)
(:types
	location
)

(:predicates (at ?l - location)
	     (initial_location ?l - location)
	     (tower_location ?l - location)
	     (task_location ?l - location)
	     (explained)
	     (ordered)
	     (talked)
	     (ask)  
	     (goodbye)	                
)


(:action speak_about_rules
:parameters (?l - location)
:precondition (and (at ?l)(initial_location ?l))
:effect (and (explained))
)

(:action ask_to_order_tower
:parameters (?l - location)
:precondition (and (explained)(at ?l)(tower_location ?l))
:effect (and (ordered))
)

(:action talk
:parameters ()
:precondition (and (explained))
:effect (and (talked))
)

(:action ask_to_do_task
:parameters (?l - location)
:precondition (and (ordered)(at ?l)(task_location ?l))
:effect (and (ask))
)

(:action say_goodbye
:parameters ()
:precondition (and (talked)(ask))
:effect (and (goodbye))
)

(:action move
:parameters (?from ?to - location)
:precondition (and (at ?from ) )
:effect (and (at ?to ) (not (at ?from )))
)
)
