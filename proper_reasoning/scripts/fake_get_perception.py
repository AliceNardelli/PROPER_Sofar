from flask import Flask, request, jsonify
import random

app = Flask(__name__)
last_person=""

@app.route('/get_perception', methods=['GET'])
def get_perception():
    global last_person

    # With 50% probability, make everything "False"
    if random.random() < 0.5:
        response_data = {
            "new_sentence": "False",
            "new_emotion": "False",
            "new_attention": "False",
            "attention": "negative",
            "emotion": "",
            "sentence": "",
            "human_present": "False",
            "start_proactivity": "False",
            "person": ""
        }
    else:
        # Randomly generate values for the response
        new_sentence = random.choice(["True", "False"])
        new_emotion = random.choice(["True", "False"])
        attention = random.choice(["positive", "negative"])
        sentence = "ciao"
        person = random.choice(["alice", "fabio"])
        human_present = "True" if person else "False"
        start_proactivity = "True" if last_person != person else "False"
        emotion = random.choice(["A", "H", "N", "SA", "SU"])

        # Construct the response
        response_data = {
            "new_sentence": new_sentence,
            "new_emotion": new_emotion,
            "new_attention": new_emotion,  # Assuming this follows the same logic as new_emotion
            "attention": attention,
            "emotion": emotion,
            "sentence": sentence,
            "human_present": new_emotion,
            "start_proactivity": start_proactivity,
            "person": person
        }
        last_person = person

    return jsonify(response_data)




@app.route('/exec_actions', methods=['POST'])
def exec_actions():
    # Get JSON data from the request
    data_action = request.json

    # Print the received data to the console
    print("Received data:", data_action)

    # Respond with a success message
    return jsonify({"status": "success", "message": "Action executed successfully"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5021)

