(define (problem p) (:domain goal1)
(:objects
)
(:init
      (to_assign_dominance)
      (new_block)
      (robot_start)
      (extro)
      (unsc)
      (disagree)
      (neutral_emotion)
      (happy_emotion_r)
      (anger_emotion_r)
      (sad_emotion_r)
      (surprise_emotion_r)
      (fear_emotion_r)
      (disgust_emotion_r)
      (attention_r)
      (low_attention)
      (=(dur)5.0)
      (=(extroversion_coefficient)0.5)
      (=(desired_interaction)5.0)
      (=(interaction_level)5.75)
      (=(conscientious_coefficient)0.0)
      (=(desired_scrupulousness)5.0)
      (=(scrupulousness_level)6.0)
      (=(agreeableness_coefficient)0.5)
      (=(desired_agreeableness)5.0)
      (=(agreeableness_level)5.25)
      (=(react)0.5)
      (=(reward_e)5)
      (=(reward_a)5)
      (=(reward_c)5)
      (=(replace)2.0)
)
(:goal (and
      (finished)
      (feel_comfort)
      (neutral_emotion_r)
      (emotion_r)
      (low_attention_r)
)))