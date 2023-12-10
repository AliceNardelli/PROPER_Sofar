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