(define (domain PROPER_domain)
(:requirements :strips 
               :typing)
(:types
	location
)

(:predicates (at ?l - location)
	     (initial_location ?l - location)
	     (tower_location ?l - location)
	     (greetings)
	     (explained)
	     (showed)
	     (ordered)
	     (talked) 
	     (goodbye)	                
)

(:action say_welcome
:parameters (?l - location)
:precondition (and (at ?l)(tower_location ?l))
:effect (and (greetings))
)

(:action speak_about_rules
:parameters(?l - location)
:precondition (and (greetings)(at ?l)(tower_location ?l))
:effect (and (explained))
)

(:action show_tower
:parameters(?l - location)
:precondition (and (explained)(at ?l)(tower_location ?l))
:effect (and (showed))
)

(:action ask_to_order_tower
:parameters (?l - location)
:precondition (and (showed)(at ?l)(tower_location ?l))
:effect (and (ordered))
)

(:action talk
:parameters(?l - location)
:precondition (and (explained)(at ?l)(tower_location ?l))
:effect (and (talked))
)


(:action say_goodbye
:parameters(?l - location)
:precondition (and (talked)(ordered)(at ?l)(tower_location ?l))
:effect (and (goodbye))
)

(:action move
:parameters (?from ?to - location)
:precondition (and (at ?from ) )
:effect (and (at ?to ) (not (at ?from )))
)
)
