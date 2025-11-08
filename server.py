import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Store the latest command
command = None

@app.route('/command', methods=['POST'])
def set_command():
    """Receive a command from the website (e.g., 'on' or 'off')"""
    global command
    data = request.get_json()
    if not data or 'action' not in data:
        return jsonify({'status': 'error', 'message': 'No action provided'}), 400

    command = data['action']
    return jsonify({'status': 'ok', 'command': command})

@app.route('/command', methods=['GET'])
def get_command():
    """Return the latest command for the ESP32 to read"""
    return jsonify({'command': command})

# Optional root route to check if backend is running
@app.route('/')
def index():
    return "ESP32 backend is running!"

if __name__ == '__main__':
    # Use the Render-provided port or default to 10000 locally
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
