from bottle.ext import websocket as bottle_websocket
import bottle, threading

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

info_list = {}

def start_websocket_server():
    print("Starting websocket server...")
    return bottle.run(
        port = 4949,
        quiet = False,
        host = "0.0.0.0",
        app = bottle.default_app(),
        server = bottle_websocket.GeventWebSocketServer,
    )

@app.route("/<server_id>/")
def get_data(server_id: str):
    if server_id in info_list:
        return info_list[server_id]
    return {}

@app.route("/<server_id>/", methods=['POST'])
def set_data(server_id: str):
    global info_list
    body = request.get_json()
    if body is not None:
        info_list[server_id] = body
    return body or {}

def connect_websocket(new_websocket):
    websocket_list.append(new_websocket)

    print("Websocket client connected.")
    while True:
        message = new_websocket.receive()
        print("Received message:", message)
        if message is None:
            break
        remove_list = []
        for websocket in websocket_list:
            if websocket is None:
                remove_list.append(websocket)
            if websocket != new_websocket:
                websocket.send(message)
        for websocket in remove_list:
            websocket_list.remove(websocket)
    websocket_list.remove(new_websocket)
    print("Websocket client disconnected.")

bottle.route(
    path = '/', 
    callback = connect_websocket, 
    apply = (bottle_websocket.websocket,))

if __name__ == '__main__':
    websocket_list = []
    threading.Thread(
        target = start_websocket_server,
        daemon = True,
    ).start()
    app.run(host='0.0.0.0', port = 5000)
