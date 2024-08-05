import time
import requests
headers= {'Content-Type':'application/json'}
url='http://130.251.13.142:5022/'
data = {
    'sentence':"",
}

def continuously_query_get_input():
    headers = {'Content-Type': 'application/json'}

    
    try:
            data["facial_expression"]="Happy"
            data["sentence"]="Mi piace tantissimo nuotare a delfino"
            data["g_amplitude"]="high"
            response =requests.put(url+'exec_actions', json=data, headers=headers)
            print(eval(response.text))
            
    except:
            print("Error querying get_input")


if __name__ == "__main__":
    continuously_query_get_input()