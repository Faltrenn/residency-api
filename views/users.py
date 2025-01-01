from common import route
from http import HTTPMethod, HTTPStatus
from server import RequestHandler
from typing import List
import json
import database as db


def fetch_users(cur) -> List[dict]:
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


@route("/users", HTTPMethod.GET)
def get_users(rh: RequestHandler):
    print(rh.headers)
    rh.set_headers(HTTPStatus.OK)
    cur = db.get_connection().cursor()
    users = fetch_users(cur)

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
        RequestHandler.cur.execute(
            "INSERT INTO users (name, pass, role_title, institution_short_name) VALUES (?, ?, ?, ?)",
            (
                rh.headers["name"],
                rh.headers["pass"],
                rh.headers["role"],
                rh.headers["institution"],
            ),
        )
        RequestHandler.conn.commit()
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
        RequestHandler.cur.execute(
            "UPDATE users SET name = ?, pass = ?, role_title = ?, institution_short_name = ? WHERE (id = ?)",
            (
                rh.headers["name"],
                rh.headers["pass"],
                rh.headers["role"],
                rh.headers["institution"],
                rh.headers["id"],
            ),
        )
        RequestHandler.conn.commit()
    else:
        rh.set_headers(HTTPStatus.BAD_REQUEST)


@route("/users", HTTPMethod.PUT)
def update_user(rh):
    if "id" in rh.headers:
        rh.set_headers(HTTPStatus.OK)
        RequestHandler.cur.execute("DELETE FROM users WHERE (id = ?)", (rh.headers["id"],))
        RequestHandler.conn.commit()
    else:
        rh.set_headers(HTTPStatus.BAD_REQUEST)
