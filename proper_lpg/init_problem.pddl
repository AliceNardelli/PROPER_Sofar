(define (problem p) (:domain PROPER_perception)
(:objects
)
(:init
        (human_present) 
        (=(dur)5)
        (=(react)3)
        (=(reward_e)5)
        (=(reward_a)5)
        (=(reward_c)5)
        (=(extroversion_coefficient) 0)
        (=(desired_interaction) 5)
        (=(interaction_level) 7)  
        (=(conscientious_coefficient) 0)
        (=(desired_scrupulousness)5)
        (=(scrupulousness_level)7)
        (=(agreeableness_coefficient) 0) 
        (=(desired_agreeableness)5)
        (=(agreeableness_level)7)
        (emotion_r) 
        (touch_reacted)  
)

(:goal (and 
      (finished)
      (feelings)
    )
)


)
