(define (problem p) (:domain goal1)
(:objects
)
(:init
      (action1_say)
      (intro)
      (unsc)
      (agree)
      (neutral_emotion_r)
      (happy_emotion_r)
      (anger_emotion)
      (sad_emotion_r)
      (surprise_emotion_r)
      (fear_emotion_r)
      (disgust_emotion_r)
      (attention_r)
      (low_attention)
      (=(dur)5.0)
      (=(extroversion_coefficient)0.5)
      (=(desired_interaction)5.0)
      (=(interaction_level)11.5)
      (=(conscientious_coefficient)0.0)
      (=(desired_scrupulousness)5.0)
      (=(scrupulousness_level)6.0)
      (=(agreeableness_coefficient)0.5)
      (=(desired_agreeableness)5.0)
      (=(agreeableness_level)8.5)
      (=(react)3.0)
      (=(reward_e)5)
      (=(reward_a)5)
      (=(reward_c)5)
)
(:goal (and
      (finished)
      (feel_comfort)
      (anger_emotion_r)
      (emotion_r)
      (low_attention_r)
)))