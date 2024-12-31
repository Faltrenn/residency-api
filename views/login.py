from common import route
from http import HTTPMethod, HTTPStatus
import string
import json
import random


class DB:
    users = {
        "manel": ("password", "admin"),
        "manelzaum": ("password", "resident"),
    }
    logins = {}


@route("/login", HTTPMethod.POST)
def login(self):
    print(self.rfile.read())
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
                self.wfile.write(
                    json.dumps({"error": "Invalid credentials"}).encode("utf-8")
                )
        else:
            self.set_headers(HTTPStatus.BAD_REQUEST)
