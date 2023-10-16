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
        (=(conscientious_coefficient)0.0)
        (=(desired_scrupulousness)5)
        (=(scrupulousness_level)10)
        (consc)
        (computed_c)  
        (=(agreeableness_coefficient)0.0)
        (=(desired_agreeableness)5)
        (=(agreeableness_level)10)
        (agree)
        (computed_a)    
        (touched)   
        (neutral_emotion)
        (sad_emotion)
)

(:goal  
    (and 
      (sad_emotion_r)
      (feelings)
    )
)


)
