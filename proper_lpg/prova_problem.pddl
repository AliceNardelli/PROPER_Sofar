(define (problem p) (:domain PROPER_navigation)
(:objects
	r1 - room
	r2 - room
)
(:init
      (production_room r2)
      (assembly_room r1)
      (presented_task r1)
      (presented_task r2)
      (at r1)
      (human_present)
      (block_to_deliver)
      (extro)
      (computed_e)
      (consc)
      (computed_c)
      (disagree)
      (computed_a)
      (=(max_no_blocks)3.0)
      (=(no_blocks)3.0)
      (=(dur)10)
      (=(extroversion_coefficient)0.2)
      (=(desired_interaction)5.0)
      (=(interaction_level)5.599999999999998)
      (=(conscientious_coefficient)0.0)
      (=(desired_scrupulousness)5.0)
      (=(scrupulousness_level)5.0)
      (=(agreeableness_coefficient)0.4)
      (=(desired_agreeableness)5.0)
      (=(agreeableness_level)9.199999999999996)
      (=(baseline)5.0)
)
(:goal  
    (and 
       (finished)
    )
)

)