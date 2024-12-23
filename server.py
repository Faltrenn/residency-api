from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
from sys import argv


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK, "Server working")
        self.end_headers()


if __name__ == "__main__":
    server = HTTPServer((argv[1], int(argv[2])), RequestHandler)
    print(f"Server started at {argv[1]}:{argv[2]}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
