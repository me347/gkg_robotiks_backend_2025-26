import asyncio
import json
from aiohttp import web
import websockets

# ===== CONFIG =====
WS_PORT = 8765  # WebSocket server port
HTTP_PORT = 8080  # HTTP server port

# Keep track of connected ESP32 clients
connected_clients = set()


# ===== WEBSOCKET SERVER =====
async def ws_handler(ws, path):
    print(f"ESP32 connected: {ws.remote_address}")
    connected_clients.add(ws)
    try:
        async for message in ws:
            print(f"Received from ESP32: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("ESP32 disconnected")
    finally:
        connected_clients.remove(ws)


# Start WebSocket server
ws_server = websockets.serve(ws_handler, "0.0.0.0", WS_PORT)

# ===== HTTP SERVER =====
async def handle_command(request):
    data = await request.json()
    cmd = data.get("action")
    print(f"Received command from frontend: {cmd}")

    # Broadcast to all connected ESP32s
    for ws in connected_clients.copy():
        try:
            await ws.send(cmd)
        except:
            pass

    return web.json_response({"status": "ok", "command": cmd})


app = web.Application()
app.router.add_post("/command", handle_command)


# ===== RUN BOTH SERVERS =====
async def main():
    await asyncio.gather(
        ws_server,
        web._run_app(app, port=HTTP_PORT),
    )


if __name__ == "__main__":
    print(f"Starting WebSocket server on port {WS_PORT}...")
    print(f"Starting HTTP server on port {HTTP_PORT}...")
    asyncio.run(main())
