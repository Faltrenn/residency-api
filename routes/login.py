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
    try:
        content_length = int(rh.headers.get("Content-Length", 0))
        body_data = rh.rfile.read(content_length).decode("utf-8")
        body = json.loads(body_data)

        if not isinstance(body, dict) or "user" not in body or "pass" not in body:
            raise ValueError("Invalid body")

        user = auth_user(body["user"], body["pass"])
        if user:
            user_id = user["id"]
            if user_id in logins:
                token = logins[user_id]
            else:
                token = "".join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=5,
                    )
                )
                logins[user_id] = token

            response = {"token": token, "role": user["role"]}
            rh.set_headers(HTTPStatus.OK)
            rh.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            rh.set_headers(HTTPStatus.NOT_FOUND)
            rh.wfile.write(json.dumps({"error": "Invalid credentials"}).encode("utf-8"))
    except ValueError as ve:
        rh.set_headers(HTTPStatus.BAD_REQUEST)
        rh.wfile.write(json.dumps({"error": str(ve)}).encode("utf-8"))
    except BrokenPipeError:
        print("Client disconnected before get response.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        rh.set_headers(HTTPStatus.INTERNAL_SERVER_ERROR)
        rh.wfile.write(json.dumps({"error": "Internal server error"}).encode("utf-8"))


@route("/login/check", HTTPMethod.GET)
def check(rh: RequestHandler):
    if not "token" in rh.headers:
        rh.set_headers(HTTPStatus.BAD_REQUEST, json=False)
        return

    if not rh.headers["token"] in logins.values():
        rh.set_headers(HTTPStatus.UNAUTHORIZED)
        rh.wfile.write(
            json.dumps({"error": "Token is inactive or expired"}).encode("utf-8")
        )
        return

    rh.set_headers(HTTPStatus.OK)
    rh.wfile.write(json.dumps({"message": "Token is valid"}).encode("utf-8"))
