from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow cross-origin for frontend

# ===== HTTP POST endpoint for frontend buttons =====
@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    cmd = data.get("action")  # "on" or "off"

    # Broadcast command to all connected WebSocket clients
    socketio.emit("command", {"action": cmd})

    return jsonify({"status": "ok", "command": cmd})

# Optional GET endpoint
@app.route('/command', methods=['GET'])
def get_command():
    return jsonify({"command": "unknown"})

# ===== WebSocket events =====
@socketio.on('connect')
def on_connect():
    print("Client connected")

@socketio.on('disconnect')
def on_disconnect():
    print("Client disconnected")

# ===== RUN SERVER =====
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)  # Let Render handle HTTPS/WSS
