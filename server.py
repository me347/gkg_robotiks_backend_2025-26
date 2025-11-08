from flask import Flask, request, jsonify

app = Flask(__name__)

command = None

@app.route('/command', methods=['POST'])
def set_command():
    global command
    data = request.get_json()
    command = data.get('action')
    return jsonify({'status': 'ok', 'command': command})

@app.route('/command', methods=['GET'])
def get_command():
    return jsonify({'command': command})
