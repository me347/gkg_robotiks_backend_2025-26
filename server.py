import asyncio
import websockets
from flask import Flask, request, jsonify
from flask_cors import CORS

# Flask setup for frontend POSTs
app = Flask(__name__)
CORS(app)

# Store latest button state from frontend
button_state = {"pressed": False}

@app.route("/button", methods=["POST"])
def button():
    global button_state
    data = request.json
    button_state["pressed"] = data.get("pressed", False)
    return jsonify({"status": "ok", "pressed": button_state["pressed"]})

# WebSocket handler for ESP32
async def ws_handler(websocket, path):
    print(f"ESP32 connected: {websocket.remote_address}")
    try:
        while True:
            # Send latest button state every 50ms
            await websocket.send(str(button_state["pressed"]))
            await asyncio.sleep(0.05)
    except websockets.ConnectionClosed:
        print("ESP32 disconnected")

# Main entrypoint to start both Flask and WebSocket server
def main():
    import threading

    # Start Flask in a separate thread
    def run_flask():
        app.run(host="0.0.0.0", port=5000)

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Start WebSocket server in asyncio
    WS_PORT = 8765
    asyncio.run(websockets.serve(ws_handler, "0.0.0.0", WS_PORT))

if __name__ == "__main__":
    main()
