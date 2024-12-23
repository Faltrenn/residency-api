from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK, "Server working")
        self.end_headers()


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), RequestHandler)
    print("Server started...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
