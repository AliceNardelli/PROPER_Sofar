from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/post_action', methods=['POST'])
def post_action():
    data = request.get_json()
    print("Received POST data:", data)
    
    # Optionally, return a response
    return jsonify({"status": "received", "data": data}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2001)