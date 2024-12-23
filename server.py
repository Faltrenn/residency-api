from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
import re
from sys import argv
import json


class DB:
    users = {"manel": "password"}


class RequestHandler(BaseHTTPRequestHandler):
    def set_headers(self, status, json = True):
        self.send_response(status)
        if json:
            self.send_header("Content-Type", "application/json")
        self.end_headers()

    def do_GET(self):
        if "/users" == self.path:
            self.set_headers(HTTPStatus.OK)

            data = json.dumps(DB.users).encode("utf-8")
            self.wfile.write(data)
        elif (
            "/login" == self.path and "user" in self.headers and "pass" in self.headers
        ):
            user = self.headers["user"]
            if user in DB.users and DB.users[user] == self.headers["pass"]:
                self.set_headers(HTTPStatus.OK)

                send_token = {"token": "abcdefgh"}
                self.wfile.write(json.dumps(send_token).encode("utf-8"))
            else:
                self.set_headers(HTTPStatus.NOT_FOUND)
        else:
            self.set_headers(HTTPStatus.BAD_REQUEST, False)


if __name__ == "__main__":
    server = HTTPServer((argv[1], int(argv[2])), RequestHandler)
    if len(argv) < 3 or not argv[2].isnumeric():
        print("WRONG USAGE!")
        print("server.py [ip] [port]")
    else:
        print(f"Server started at {argv[1]}:{argv[2]}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        server.server_close()
