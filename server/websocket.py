from bottle.ext import websocket as bottle_websocket
import os, bottle

websocket_list = []

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
