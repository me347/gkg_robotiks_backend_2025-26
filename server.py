from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

command = None

@app.route('/command', methods=['POST'])
def set_command():
    global command
    data = request.get_json()
    command = data.get('action')
    # immediately send the command to all connected clients
    socketio.emit('command_update', {'command': command})
    return jsonify({'status': 'ok', 'command': command})

@app.route('/command', methods=['GET'])
def get_command():
    return jsonify({'command': command})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=port)
