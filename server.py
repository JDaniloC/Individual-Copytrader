from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class S(BaseHTTPRequestHandler):
    def _set_headers(self, code = 204):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def _json(self, data):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = json.dumps(data)
        return content.encode("utf-8")

    def do_GET(self):
        self._set_headers(200)
        with open("database.json") as file:
            orders = json.load(file)
        self.wfile.write(self._json(orders))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers(201)
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(
            self.rfile.read(content_length).decode("utf-8"))
        with open("database.json", "w") as file:
            json.dump(post_data, file)
        self.wfile.write(self._json(post_data))


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == "__main__":
    run(addr='localhost', port=8000)