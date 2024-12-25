from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPMethod, HTTPStatus
from sys import argv
import json
import random
import string
import re


def route(path: str, method: HTTPMethod):
    def decorator(func):
        setattr(func, "api", (path, method))
        return func

    return decorator


class DB:
    users = {"manel": ("password", "admin"), "manelzaum": ("password", "resident")}
    logins = {}


class RequestHandler(BaseHTTPRequestHandler):
    routes = {}

    @classmethod
    def initialize(cls):
        methods = (HTTPMethod.GET, HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.DELETE)
        for m in methods:
            routes = {
                attr[0]: f
                for f in RequestHandler.__dict__.values()
                if (attr := getattr(f, "api", None)) is not None and attr[1] == m
            }
            cls.routes[m] = routes

    def set_headers(self, status: HTTPStatus, message: str | None = None, json=True):
        self.send_response(status, message)
        if json:
            self.send_header("Content-Type", "application/json")
        self.end_headers()

    @route("/users", HTTPMethod.GET)
    def users(self):
        if "token" in self.headers:
            token = self.headers["token"]
            if token in DB.logins and DB.logins[token][1] == "admin":
                self.set_headers(HTTPStatus.OK)

                data = json.dumps(DB.users).encode("utf-8")
                self.wfile.write(data)
            else:
                self.set_headers(HTTPStatus.UNAUTHORIZED)

    @route("/login", HTTPMethod.GET)
    def login(self):
        if "user" in self.headers and "pass" in self.headers:
            user = self.headers["user"]
            if user in DB.users and DB.users[user][0] == self.headers["pass"]:
                self.set_headers(HTTPStatus.OK)
                for k, v in DB.logins.items():
                    if user in v:
                        send_token = {"token": k}
                        self.wfile.write(json.dumps(send_token).encode("utf-8"))
                        return

                token = "".join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=5,
                    )
                )
                DB.logins[token] = [user, DB.users[user][1]]

                send_token = {"token": token}
                self.wfile.write(json.dumps(send_token).encode("utf-8"))
            else:
                self.set_headers(HTTPStatus.NOT_FOUND)

    @route("/test-post*", HTTPMethod.POST)
    def test_post(self):
        self.set_headers(HTTPStatus.OK, "Funcionou :)", False)
        self.wfile.write("Tudo joia meu parceiro".encode("utf-8"))

    def run_routes(self, method: HTTPMethod):
        for k, v in RequestHandler.routes[method].items():
            if re.search(k, self.path):
                v(self)
                return
        self.set_headers(HTTPStatus.NOT_FOUND, json=False)

    def do_GET(self):
        self.run_routes(HTTPMethod.GET)

    def do_POST(self):
        self.run_routes(HTTPMethod.POST)

    def do_PUT(self):
        self.run_routes(HTTPMethod.PUT)

    def do_DELETE(self):
        self.run_routes(HTTPMethod.DELETE)


if __name__ == "__main__":
    RequestHandler.initialize()
    server = HTTPServer((argv[1], int(argv[2])), RequestHandler)
    if len(argv) < 3 or not argv[2].isnumeric():
        print("WRONG USAGE!")
        print("server.py ip port")
    else:
        print(f"Server started at {argv[1]}:{argv[2]}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        server.server_close()
