from bottle.ext import websocket as bottle_websocket
import os, bottle

info_list = {}
websocket_list = []

@bottle.get("/<server_id>/")
def get_controller_data(server_id: str):
    if server_id in info_list:
        return info_list[server_id]
    return {}

@bottle.post("/<server_id>/")
def set_controller_data(server_id: str):
    global info_list
    body = bottle.request.json
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
            elif websocket != new_websocket:
                websocket.send(message)
        for websocket in remove_list:
            websocket_list.remove(websocket)
    websocket_list.remove(new_websocket)
    print("Websocket client disconnected.")

bottle.route(
    path = '/', 
    callback = connect_websocket, 
    apply = (bottle_websocket.websocket,))

bottle.run(
    port = int(os.environ.get('PORT', 4949)),
    quiet = False,
    host = "0.0.0.0",
    app = bottle.default_app(),
    server = bottle_websocket.GeventWebSocketServer,
)
