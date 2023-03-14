(define (problem WM)
(:domain wm_interactive_task)
(:objects
	l1 - location
	l2 - location
	l3 - location
)
(:init
(at l1)
(initial_location l1)
(tower_location l2)
(task_location l3)
)
(:goal (and (goodbye)))
)
