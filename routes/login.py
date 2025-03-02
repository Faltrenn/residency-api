from common import Roles, body_keys_needed, route
from http import HTTPMethod, HTTPStatus
import string
import random

from server import RequestHandler
from services.auth import auth_user, get_user


logins = {}  # {user_id: token}


@route("/login", HTTPMethod.POST)
@body_keys_needed(["user", "pass"])
def login(rh: RequestHandler, body: dict):
    try:
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
            rh.set_headers(HTTPStatus.OK, data=response)
        else:
            rh.set_headers(HTTPStatus.NOT_FOUND, data={"error": "Invalid credentials"})
    except ValueError as ve:
        rh.set_headers(HTTPStatus.BAD_REQUEST, data={"error": str(ve)})
    except BrokenPipeError:
        print("Client disconnected before get response.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        rh.set_headers(
            HTTPStatus.INTERNAL_SERVER_ERROR, data={"error": "Internal server error"}
        )


def getRoleByToken(token: str) -> Roles | None:
    for k, v in logins.items():
        if v == token:
            if user := get_user(k):
                return Roles.get_role(user["role"])
    return None

def get_id_by_token(token: str) -> int | None:
    for k, v in logins.items():
        if v == token:
            if get_user(k):
                return k
    return None


@route("/login/check", HTTPMethod.GET)
def check(rh: RequestHandler):
    if not "token" in rh.headers:
        rh.set_headers(HTTPStatus.BAD_REQUEST)
        return

    if not rh.headers["token"] in logins.values():
        rh.set_headers(
            HTTPStatus.UNAUTHORIZED, data={"error": "Token is inactive or expired"}
        )
        return

    response = {}
    if role := getRoleByToken(rh.headers["token"]):
        response["role"] = Roles.get_role_title(role)

    rh.set_headers(HTTPStatus.OK, data=response)
