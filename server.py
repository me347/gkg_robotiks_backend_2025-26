from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sockets import Sockets

app = Flask(__name__)
CORS(app)  # allow cross-origin requests
sockets = Sockets(app)

clients = []  # connected WebSocket clients

# WebSocket route
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

    # Broadcast to all connected clients
    for ws in clients:
        try:
            ws.send(cmd)
        except:
            pass

    return jsonify({"status": "ok", "command": cmd})

# Optional GET endpoint
@app.route('/command', methods=['GET'])
def get_command():
    return jsonify({"command": "unknown"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 443))
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(("0.0.0.0", port), app, handler_class=WebSocketHandler)
    print(f"Server running on port {port}")
    server.serve_forever()
