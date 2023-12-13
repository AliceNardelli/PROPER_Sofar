# -*- coding: utf-8 -*-

import os
import openai
from openai import OpenAI
import time
openai.organization = "org-OWePijhLCGVSJWhT7TQXBK7D"
key=os.getenv("OPENAI_API_KEY")
openai.api_key = key
model="gpt-4-1106-preview"
start=time.time()
data={"personality":"Not Conscientous",
      "language":"Lazy",
      "sentence":"Say the user that now you need to do some training together. The user will do everthing because you are lazy"
      }
    
pr='generate a response with a "'+data["personality"]+'" personality with a "'+data["language"]+'" style in italian to the following sentence "'+data["sentence"]+'". Plese follow the style and the personality to write the sentence and not generate emoticons. Please do mot directly express the personality.  Generate the sentences within  square brackets []' 
client = OpenAI()

response = client.chat.completions.create(
  model=model,
  messages=[{"role": "user", 
            "content": pr}],
  temperature=1,
  top_p=1,
  max_tokens=100,
)

print(response.choices[0].message.content)
print("----------------------")

end=time.time()
print(end-start)
