import websocket, json, threading

websocket_connection = {
    "status": False
}
class WebsocketClient:
    def __init__(self, url: str, port: str):
        self.callback = {}
        self.connection = websocket_connection
        url = f"ws://{url}:{port}/"
        self.wss = websocket.WebSocketApp(
            url, on_open = self.on_open,
            on_error = self.on_error, 
            on_close = self.on_close,
            on_message = self.on_message,
        )
        
    def connect(self):
        websocket_connection['status'] = -1
        thread = threading.Thread(target=self.wss.run_forever, 
            kwargs = { "ping_interval": 5}, daemon = True)
        thread.start()

        while True:
            try:
                if websocket_connection['status'] == 0:
                    return False
                elif websocket_connection['status'] == 1:
                    return True
            except: pass

    def send_message(self, message: dict):
        self.wss.send(json.dumps(message))

    def on_message(self, message):
        """Method to process websocket messages."""
        message = json.loads(str(message))
        print(message)
        self.callback = message

    @staticmethod
    def on_error(wss, error):
        print(error)

    @staticmethod
    def on_open(wss):
        print("Websocket client connected.")
        websocket_connection["status"] = 1

    @staticmethod
    def on_close(wss):
        print("Websocket connection closed.")
        websocket_connection["status"] = 0
