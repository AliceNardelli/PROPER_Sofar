(define (problem p) (:domain PROPER_perception)
(:objects
)
(:init
      (human_present)
      (finished)
      (greetings)
      (feelings)
      (intro)
      (unsc)
      (agree)
      (touch_reacted)
      (neutral_emotion)
      (happy_emotion)
      (happy_emotion_r)
      (sad_emotion)
      (sad_emotion_r)
      (=(dur)5.0)
      (=(extroversion_coefficient)0.0)
      (=(desired_interaction)5.0)
      (=(interaction_level)7.0)
      (=(conscientious_coefficient)0.5)
      (=(desired_scrupulousness)5.0)
      (=(scrupulousness_level)6.0)
      (=(agreeableness_coefficient)0.5)
      (=(desired_agreeableness)5.0)
      (=(agreeableness_level)9.0)
      (=(react)3.0)
      (=(reward_e)5)
      (=(reward_a)5)
      (=(reward_c)5)
)
(:goal (and
      (neutral_emotion_r)
      (emotion_r)
)))