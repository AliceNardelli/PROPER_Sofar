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
pr='Generate a sentence with a "agreeable" personality with a "Gently" style in italian to achieve the following goal "ask what is the human favourite picture". Plese follow the style and the personality to write the sentence. Please do mot directly express the personality. Generate the sentences within  square brackets []'
client = OpenAI()

response = client.chat.completions.create(
  model=model,
  messages=[{"role": "user", 
            "content": pr}],
  temperature=1,
  top_p=1,
)

print(response.choices[0].message.content)
print("----------------------")

end=time.time()
print(end-start)
