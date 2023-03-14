(define (domain BasicMove)
(:requirements :strips 
               :typing)
(:types
	location
	robot
)

(:predicates (at ?l - location ?r - robot)
             
)

(:action move
:parameters (?from ?to - location ?r - robot)
:precondition (and (at ?from ?r) )
:effect (and (at ?to ?r) (not (at ?from ?r)))
)
)
