# PROPER_Sofar base architecture for conversation


## How to execute it 

To run it with xterm:

>./run.sh path_before_PROPER_Sofar


To run it withouth xterm

>./run2.sh path_before_PROPER_Sofar

To kill automatically all scripts

> ./kill_python.sh

## Interfaces

Add the personality

```ruby
headers= {'Content-Type':'application/json'}
data={
       "Extrovert":0,
       "Introvert":0,
       "Agreeable":0,
       "Disagreeable":1,
       "Conscientious":0,
       "Unscrupolous":0
}
url='http://127.0.0.1:5019/'
resp=requests.put(url+'set_personality', json=data, headers=headers)
```

Add a perception (emotional state, attentive state, and if user say something)


```ruby
url='http://192.168.1.10:5020/'
headers= {'Content-Type':'application/json'}
data={
      "emotion":'emotion_Angry',
      "new_emotion":"True",
      "new_sentence":"False",
      "new_attention":"False",
}
resp=requests.put(url+'update_input', json=data, headers=headers)
```

Retrieve the action to execute


```ruby
data={
        "action":"",
        "language":"",
        "personality":"",
        "pitch":"",
        "volume":"",
        "velocity":"",
        "new_action":"",
        "executed":""
}
url1='http://127.0.0.1:5021/'
resp=requests.put(url1+'get_action', json=data, headers=headers)
while eval(resp.text)["new_action"]=="False":
	resp=requests.put(url1+'get_action', json=data, headers=headers)
	time.sleep(1)
```

Affirm that the action has been executed


```ruby
data={
        "result":"True",
        "executed":"True",
}
url1='http://127.0.0.1:5021/'
resp=requests.put(url1+'set_exec', json=data, headers=headers)
```

Restart when needed

```ruby

data={
       "restart":"True"
}
url1='http://127.0.0.1:5018/'
resp=requests.put(url1+'set_restart', json=data, headers=headers)

```

## Actions to associated to each trait

Distagreeable:
"say_a_contrastive_affirmation"
"remember_the_superiority_of_the_artificial_intelligence_in_taking_decisions"
"ask_a_provocative_question"
"ask_if_it_can_be_useful_stressing_on_its_superiority_on_answering_questions"
"say_to_pay_attention_on_what_it_is_going_to_say_since_it_has_always_right"

Agreeable:
"ask_if_it_can_be_useful"
"express_happyness_for_helping_the_user"
"express_empathy"
"affirm_to_mantain_the_calm_and_ask_if_can_be_useful"
"ask_if_there_is_something_that_clouds_thoughts"
"say_to_free_the_mind_from_thoughts"
"say_to_be_glad_to_see_the_user_full_of_energy"


Conscientous:
"say_the_user_to_focus_on_long_term_goals_and_not_waste_time"
"ask_where_it_can_be_useful"
"say_to_be_focused"
"remind_to_not_distract"


Unscrupolous:
"distract_the_user_asking_a_random_question"
"make_a_thoughtless_consideration"
"say_that_sometimes_it_is_important_to_take_off_your_head"
"say_that_it_is_nice_to_find_someone_with_its_head_in_the_clouds"

Extrovert:
"say_an_enthusiastic_sentence"
"say_something_funny"
"ask_a_question"
"say_something_to_capture_the_attention"


Introvert:
"say_if_can_be_useful"
"ask_to_proceed_in_their_task_or_terminate_the_conversation"
