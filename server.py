from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sockets import Sockets

app = Flask(__name__)
# Allow all origins, methods, and credentials
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
sockets = Sockets(app)

# Keep track of connected WebSocket clients
clients = []

# WebSocket endpoint for ESP32
@sockets.route('/ws')
def ws_route(ws):
    clients.append(ws)
    try:
        while not ws.closed:
            msg = ws.receive()
            if msg:
                print("Received from client:", msg)
    finally:
        clients.remove(ws)

# HTTP POST endpoint for frontend buttons
@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    cmd = data.get("action")  # "on" or "off"

    # Broadcast command to all connected WebSocket clients
    for ws in clients:
        try:
            ws.send(cmd)
        except:
            pass  # ignore broken connections

    return jsonify({"status": "ok", "command": cmd})

# Optional GET endpoint
@app.route('/command', methods=['GET'])
def get_command():
    return jsonify({"command": "unknown"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 443))  # HTTPS port
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(("0.0.0.0", port), app, handler_class=WebSocketHandler)
    print(f"Server running on port {port}")
    server.serve_forever()
