from common import route
from http import HTTPMethod, HTTPStatus
from routes.login import getRoleByToken
from server import RequestHandler
from typing import List
import json
import database as db
import models


def fetch_users() -> List[dict]:
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("select * from users")
    rows = cur.fetchall()
    users = models.get_users(rows)

    conn.close()
    cur.close()
    return users


@route("/users", HTTPMethod.GET)
def get_users(rh: RequestHandler):
    if "token" not in rh.headers:
        rh.set_headers(HTTPStatus.BAD_REQUEST)
        return

    role = getRoleByToken(rh.headers["token"])
    if not role or role != "Admin":
        rh.set_headers(HTTPStatus.UNAUTHORIZED)
        return

    rh.set_headers(HTTPStatus.OK)
    users = fetch_users()

    data = json.dumps(users).encode("utf-8")
    rh.wfile.write(data)


@route("/users", HTTPMethod.POST)
def add_user(rh):
    if (
        "name" in rh.headers
        and "role" in rh.headers
        and "pass" in rh.headers
        and "institution" in rh.headers
    ):
        rh.set_headers(HTTPStatus.OK)
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, pass, role_title, institution_short_name) VALUES (?, ?, ?, ?)",
            (
                rh.headers["name"],
                rh.headers["pass"],
                rh.headers["role"],
                rh.headers["institution"],
            ),
        )
        conn.commit()
        cur.close()
        conn.close()
    else:
        rh.set_headers(HTTPStatus.BAD_REQUEST)


@route("/users", HTTPMethod.DELETE)
def remove_user(rh):
    if (
        "id" in rh.headers
        and "name" in rh.headers
        and "role" in rh.headers
        and "pass" in rh.headers
        and "institution" in rh.headers
    ):
        rh.set_headers(HTTPStatus.OK)
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET name = ?, pass = ?, role_title = ?, institution_short_name = ? WHERE (id = ?)",
            (
                rh.headers["name"],
                rh.headers["pass"],
                rh.headers["role"],
                rh.headers["institution"],
                rh.headers["id"],
            ),
        )
        conn.commit()
        cur.close()
        conn.close()
    else:
        rh.set_headers(HTTPStatus.BAD_REQUEST)


@route("/users", HTTPMethod.PUT)
def update_user(rh):
    if "id" in rh.headers:
        rh.set_headers(HTTPStatus.OK)
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM users WHERE (id = ?)", (rh.headers["id"],)
        )
        conn.commit()
        cur.close()
        conn.close()
    else:
        rh.set_headers(HTTPStatus.BAD_REQUEST)
