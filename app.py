from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        if request.is_json:
            data = request.json
            print("Data received from Webhook is: ", data)
            return jsonify({"message": "Webhook received!"}), 200
        else:
            print("Unsupported Media Type: Content-Type is not application/json")
            return jsonify({"error": "Unsupported Media Type"}), 415
    else:
        return jsonify({"message": f"Method {request.method} received!"}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

