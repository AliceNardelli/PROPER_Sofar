
from flask import Flask, request, jsonify
import os
import openai
openai.organization = "org-SwpGa1d1G6Gna0rCvM9JRo2o"
file=open("/home/alice/alice_key.txt", "r")
key=file.readline().replace("\n","")
openai.api_key = key
a=openai.Model.list()
#model="gpt-3.5-turbo"
model="text-davinci-003"

data = {
    "sentence": "p",
    "response":"q"
}


app = Flask(__name__)

@app.route ('/sentence_generation', methods = ['PUT'] )
def main():
  updated_data = request.get_json()
  data.update(updated_data)
  #res=openai.ChatCompletion.create(
  res=openai.Completion.create(
  model=model,
  #messages=[{"role": "user", 
            #"content": pr}],
  prompt=data["sentence"],
  temperature=0.9,
  max_tokens=200,
  top_p=1,
  frequency_penalty=2,
  presence_penalty=2
  )
  data["response"]=res.text
  return jsonify(data)

"""
res=openai.Completion.create(
model=model,
#messages=[{"role": "user", "content": "Translate in italian: '"+res.choices[0].message.content+"'"}],
prompt="Translate in italian: '"+res.choices[0].text+"'", #res.choices[0].message.content
temperature=0.5,
max_tokens=200,
top_p=1,
frequency_penalty=1,
presence_penalty=1
)
print(res)

response = openai.Completion.create(
model=model,
prompt=pr,
max_tokens=60,
temperature=0.3,
top_p=1,
frequency_penalty=0,
presence_penalty=0
)
print(response)
"""


if __name__=='__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)
