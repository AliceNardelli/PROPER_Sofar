import requests
url2='http://127.0.0.1:5011/'
headers= {'Content-Type':'application/json'}
print("before getting audio")
data = {
    "sentence": "p",
    "response":"q"
}
resp=requests.put(url2+'get_audio', json=data, headers=headers)
reply=eval(resp.text)["sentence"]
print("after getting audio")
print(reply)