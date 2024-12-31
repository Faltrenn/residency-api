from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPMethod, HTTPStatus
from sys import argv
import re
import mariadb


class RequestHandler(BaseHTTPRequestHandler):
    routes = {}
    cur: mariadb.Cursor
    conn: mariadb.Connection

    @classmethod
    def initialize(cls):
        cls.conn = mariadb.connect(
            host="127.0.0.1", port=3306, user="root", password="password", database="residency"
        )
        cls.cur = cls.conn.cursor()

        methods = (
            HTTPMethod.GET,
            HTTPMethod.POST,
            HTTPMethod.PUT,
            HTTPMethod.DELETE,
        )
        for m in methods:
            routes = {
                attr[0]: f
                for f in RequestHandler.__dict__.values()
                if (attr := getattr(f, "api", None)) is not None and attr[1] == m
            }
            cls.routes[m] = routes

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
