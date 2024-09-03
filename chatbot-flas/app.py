from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhooks/rest/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        user_message = data.get('message')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Forward the message to Rasa server
        response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={'message': user_message})

        if response.status_code == 200:
            bot_messages = response.json()
            return jsonify(bot_messages)
        else:
            return jsonify({'error': 'Failed to get response from Rasa server'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
