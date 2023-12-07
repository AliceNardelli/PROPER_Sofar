# -*- coding: utf-8 -*-

import os
import openai
from openai import OpenAI
openai.organization = "org-OWePijhLCGVSJWhT7TQXBK7D"
key=os.getenv("OPENAI_API_KEY")
openai.api_key = key
model="gpt-4"

pr='Generate a sentence in italian with an Rude personality to acieve the following goal "say to drink a glass of water"'

client = OpenAI()

response = client.chat.completions.create(
  model=model,
  messages=[{"role": "user", 
            "content": pr}],
  temperature=1,
  max_tokens=50,
  top_p=1,
)

print(response.choices[0].message.content)
print("----------------------")


