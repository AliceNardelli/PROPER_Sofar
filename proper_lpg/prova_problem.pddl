(define (problem p) (:domain PROPER_navigation)
(:objects
	r1 - room
	r2 - room
)
(:init
      (production_room r2)
      (assembly_room r1)
      (presented_task r2)
      (presented_task r1)
      (at r2)
      (human_present)
      (block_to_deliver)
      (intro)
      (computed_e)
      (consc)
      (disagree)
      (computed_a)
      (=(max_no_blocks)3.0)
      (=(no_blocks)3.0)
      (=(dur)5)
      (=(extroversion_coefficient)0.5)
      (=(desired_interaction)5.0)
      (=(interaction_level)5.0)
      (=(conscientious_coefficient)0.5)
      (=(desired_scrupulousness)5.0)
      (=(scrupulousness_level)7.5)
      (=(agreeableness_coefficient)0.0)
      (=(desired_agreeableness)5.0)
      (=(agreeableness_level)5.0)
      (=(baseline)5.0)
)
(:goal  
    (and 
       (finished)
    )
)

)