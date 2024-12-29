from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPMethod, HTTPStatus
from sys import argv
import json
import random
import string
import re
from typing import List
import mariadb


conn = mariadb.connect(
    host="127.0.0.1", port=3306, user="root", password="password", database="residency"
)
cur = conn.cursor()


def fetch_users() -> List[dict]:
    cur.execute("select * from users")
    return [
        {
            "id": id,
            "name": name,
            "password": password,
            "role": role,
            "institution": institution,
        }
        for (id, name, password, role, institution) in cur.fetchall()
    ]


def route(path: str, method: HTTPMethod):
    def decorator(func):
        setattr(func, "api", (path, method))
        return func

    return decorator


class DB:
    users = {
        "manel": ("password", "admin"),
        "manelzaum": ("password", "resident"),
    }
    logins = {}


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
    def get_users(self):
        self.set_headers(HTTPStatus.OK)
        users = fetch_users()

        data = json.dumps(users).encode("utf-8")
        self.wfile.write(data)

        # if "token" in self.headers:
        #     token = self.headers["token"]
        #     if token in DB.logins and DB.logins[token][1] == "admin":
        #         self.set_headers(HTTPStatus.OK)
        #
        #         data = json.dumps(DB.users).encode("utf-8")
        #         self.wfile.write(data)
        #     else:
        #         self.set_headers(HTTPStatus.UNAUTHORIZED)

    @route("/users", HTTPMethod.POST)
    def add_user(self):
        if (
            "name" in self.headers
            and "role" in self.headers
            and "pass" in self.headers
            and "institution" in self.headers
        ):
            self.set_headers(HTTPStatus.OK)
            cur.execute(
                "INSERT INTO users (name, pass, role_title, institution_short_name) VALUES (?, ?, ?, ?)",
                (
                    self.headers["name"],
                    self.headers["pass"],
                    self.headers["role"],
                    self.headers["institution"],
                ),
            )
            conn.commit()
        else:
            self.set_headers(HTTPStatus.BAD_REQUEST)

    @route("/users", HTTPMethod.PUT)
    def remove_user(self):
        if (
            "id" in self.headers
            and "name" in self.headers
            and "role" in self.headers
            and "pass" in self.headers
            and "institution" in self.headers
        ):
            self.set_headers(HTTPStatus.OK)
            cur.execute(
                "UPDATE users SET name = ?, pass = ?, role_title = ?, institution_short_name = ? WHERE (id = ?)",
                (
                    self.headers["name"],
                    self.headers["pass"],
                    self.headers["role"],
                    self.headers["institution"],
                    self.headers["id"],
                ),
            )
            conn.commit()
        else:
            self.set_headers(HTTPStatus.BAD_REQUEST)

    @route("/users", HTTPMethod.DELETE)
    def update_user(self):
        if "id" in self.headers:
            self.set_headers(HTTPStatus.OK)
            cur.execute("DELETE FROM users WHERE (id = ?)", (self.headers["id"],))
            conn.commit()
        else:
            self.set_headers(HTTPStatus.BAD_REQUEST)

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
