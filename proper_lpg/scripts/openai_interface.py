# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import os
import openai
from openai import OpenAI
openai.organization = "org-OWePijhLCGVSJWhT7TQXBK7D"
key=os.getenv("OPENAI_API_KEY")
openai.api_key = key
model="gpt-4"
client = OpenAI()

data = {
    "personality":"p",
    "language": "p",
    "sentence": "s",
    "response":"q"
}


app = Flask(__name__)

@app.route ('/sentence_generation', methods = ['PUT'] )
def main():
  
  updated_data = request.get_json()
  data.update(updated_data)
  if data["personality"]=="Extrovert":
     tokens=150
  elif data["personality"]=="Introvert":
     tokens=60
  else:
     tokens=100
  sentence='Generate a sentence with a "'+data["personality"]+'" personality with a "'+data["language"]+'" style in italian to achieve the following goal "'+data["sentence"]+'". Plese follow the style and the personality to write the sentence and not generate emoticons. Please do mot directly express the personality.  Generate the sentences within  square brackets []'
  response = client.chat.completions.create(
    model=model,
    messages=[
              {"role": "user", "content": sentence}],
    temperature=1,
    max_tokens=tokens,
    top_p=1,
  )
  print(sentence)
  print(response.choices[0].message.content)
  print("----------------------")
  resp=response.choices[0].message.content.replace("à","a")
  data["response"]=resp[resp.find("[")+1:resp.find("]")]
  return jsonify(data)



@app.route ('/sentence_response', methods = ['PUT'] )
def main2():
  updated_data = request.get_json()
  data.update(updated_data)
  if data["personality"]=="Extrovert":
     tokens=150
  elif data["personality"]=="Introvert":
     tokens=60
  else:
     tokens=100
  sentence='generate a response with a "'+data["personality"]+'" personality with a "'+data["language"]+'" style in italian to the following sentence "'+data["sentence"]+'". Plese follow the style and the personality to write the sentence and not generate emoticons. Please do mot directly express the personality.  Generate the sentences within  square brackets []' 
  response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", 
              "content": sentence}],
    temperature=1,
    max_tokens=tokens,
    top_p=1,
  )
  print(sentence)
  print(response.choices[0].message.content)
  print("----------------------")
  resp=response.choices[0].message.content.replace("à","a")
  data["response"]=resp[resp.find("[")+1:resp.find("]")]
  return jsonify(data)



if __name__=='__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
