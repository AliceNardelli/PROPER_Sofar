(define (problem PROPER)
(:domain PROPER_domain)
(:objects
	l1 - location
	l2 - location
	
)
(:init
(at l1)
(initial_location l1)
(tower_location l2)
(not_explained)
)
(:goal (and (goodbye)(at l1)))
)
