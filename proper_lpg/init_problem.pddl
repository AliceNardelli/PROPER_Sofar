(define (problem p) (:domain PROPER_perception)
(:objects
)
(:init
        (human_present) 
        (=(dur)0)
        (=(react)3)
        (=(extroversion_coefficient) 0.1)
        (=(desired_interaction) 5)
        (=(interaction_level) 10) 
        (extro)
        (computed_e)  
        (=(conscientious_coefficient)0.1)
        (=(desired_scrupulousness)5)
        (=(scrupulousness_level)10)
        (unsc)
        (computed_c)  
        (=(agreeableness_coefficient)0.0)
        (=(desired_agreeableness)5)
        (=(agreeableness_level)10)
        (disagree)
        (computed_a)    
        (touched)   
        (happy_emotion)
)

(:goal  
    (and 
      (happy_emotion_r)
      (feelings)
    )
)


)
