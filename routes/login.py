from common import route
from http import HTTPMethod, HTTPStatus
import string
import json
import random

from server import RequestHandler
from services.auth import auth_user


logins = {}  # {user_id: token}


@route("/login", HTTPMethod.POST)
def login(rh: RequestHandler):
    print("Boa")
    print(json.loads(rh.rfile.read()))
    if "user" in rh.headers and "pass" in rh.headers:
        user = auth_user(rh.headers["user"], rh.headers["pass"])
        if user:
            rh.set_headers(HTTPStatus.OK)
            user_id = user["id"]
            if user_id in logins:
                send_token = {"token": logins[user_id]}
                rh.wfile.write(json.dumps(send_token).encode("utf-8"))
                return

            token = "".join(
                random.choices(
                    string.ascii_letters + string.digits,
                    k=5,
                )
            )
            logins[user_id] = token

            send_token = {"token": token}
            rh.wfile.write(json.dumps(send_token).encode("utf-8"))
        else:
            rh.set_headers(HTTPStatus.NOT_FOUND)
            rh.wfile.write(
                json.dumps({"error": "Invalid credentials"}).encode("utf-8")
            )
    else:
        rh.set_headers(HTTPStatus.BAD_REQUEST)
