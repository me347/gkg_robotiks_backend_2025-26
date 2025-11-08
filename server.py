from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sockets import Sockets

app = Flask(__name__)
CORS(app)
sockets = Sockets(app)

clients = []

# WebSocket for ESP32
@sockets.route('/ws')
def ws_route(ws):
    clients.append(ws)
    try:
        while not ws.closed:
            msg = ws.receive()
            if msg:
                print("Received from ESP32:", msg)
    finally:
        clients.remove(ws)

# POST endpoint for frontend buttons
@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    cmd = data.get("action")  # "on" or "off"

    # Broadcast to connected ESP32 clients
    for ws in clients:
        try:
            ws.send(cmd)
        except:
            pass

    return jsonify({"status": "ok", "command": cmd})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 443))
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(("0.0.0.0", port), app, handler_class=WebSocketHandler)
    print(f"Server running on port {port}")
    server.serve_forever()
