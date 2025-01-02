from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPMethod, HTTPStatus
from sys import argv
import re
import importlib
import routes


class RequestHandler(BaseHTTPRequestHandler):
    routes = {}

    @classmethod
    def initialize(cls):
        methods = (
            HTTPMethod.GET,
            HTTPMethod.POST,
            HTTPMethod.PUT,
            HTTPMethod.DELETE,
        )

        modules_names = [name for name in dir(routes) if not name.startswith("__")]
        functions = [
            f
            for module_name in modules_names
            for f in importlib.import_module(
                f"views.{module_name}"
            ).__dict__.values()
            if hasattr(f, "api")
        ]

        for m in methods:
            cls.routes[m] = {
                attr[0]: f
                for f in functions
                if (attr := getattr(f, "api")) and attr[1] == m
            }

    def set_headers(self, status: HTTPStatus, message: str | None = None, json=True):
        self.send_response(status, message)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"
        )
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        if json:
            self.send_header("Content-Type", "application/json")
        self.end_headers()

    def run_routes(self, method: HTTPMethod):
        for k, v in RequestHandler.routes[method].items():
            if re.search(k, self.path):
                v(self)
                return
        self.set_headers(HTTPStatus.NOT_FOUND, json=False)

    def do_OPTIONS(self):
        self.set_headers(HTTPStatus.NO_CONTENT, json=False)

    def do_GET(self):
        self.run_routes(HTTPMethod.GET)

    def do_POST(self):
        self.run_routes(HTTPMethod.POST)

    def do_PUT(self):
        self.run_routes(HTTPMethod.PUT)

    def do_DELETE(self):
        self.run_routes(HTTPMethod.DELETE)


if __name__ == "__main__":
    if len(argv) < 3 or not argv[2].isnumeric():
        print("WRONG USAGE!")
        print("server.py ip port")
    else:
        RequestHandler.initialize()
        server = HTTPServer((argv[1], int(argv[2])), RequestHandler)
        print(f"Server started at {argv[1]}:{argv[2]}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        server.server_close()
