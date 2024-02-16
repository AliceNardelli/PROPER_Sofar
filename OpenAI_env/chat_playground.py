
import os
import openai
from openai import OpenAI
from omegaconf import OmegaConf
#import emoji
import json

from flask import Flask, request, jsonify

#openai vars
file_path_openai_config = "/home/alice/catkin_ws/src/PROPER_Sofar/OpenAI_env/config_openai_personality_kinova.yaml"
openai_config = OmegaConf.load(file_path_openai_config).config
openai.organization = "org-OWePijhLCGVSJWhT7TQXBK7D"
openai.api_key = os.getenv("OPENAI_API_KEY")
system_message = openai_config.system_message
# Create a list to store all the messages for context
start_message = [
    {"role": "system", "content": system_message},
]
model="gpt-4"

client = OpenAI()


app = Flask(__name__)

data={
    "emotion":"",
    "action":"",
    "response_style":"",
    "selected_personality":"",
    "limit_response":"",
    "response":"",
    "attention":"",

}

@app.route ('/run_completion', methods = ['PUT'] )  
def run_cmp():
   
    updated_data = request.get_json()
    data.update(updated_data) 
    
    user_input = "{"
    user_input += "emotion: "
    user_input += data["emotion"]
    user_input += ", attention: "
    user_input += data["attention"]
    user_input += ", personality: "
    user_input += data["selected_personality"]
    user_input += ", response_style: "
    user_input += data["response_style"]
    user_input += ", action: "
    user_input += data["action"]
    
    if data["limit_response"] == "True":
        user_input += ", notes: "
        user_input += 'the text attribute must be no more than 40 words'
    
    user_input += "}"
   
    # Add each new message to the list
    messages=start_message
    messages.append({"role": "user", "content": user_input})
   

    response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=1,
    top_p=1,
    )

    # Print the response and add it to the messages list
   
    print(type(response.choices[0].message.content))
    print(response.choices[0].message.content)
    #chat_message = emoji.replace_emoji(string=chat_message, replace='')
    res = json.loads(response.choices[0].message.content)
    data["response"]=res["text"]
    return jsonify(data)


if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port=5018, debug=True)

   
