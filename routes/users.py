from common import Roles, body_keys_needed, middleware, route
from http import HTTPMethod, HTTPStatus
from server import RequestHandler
from typing import List
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


def remove_user() -> List[dict]:
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("select * from users")
    rows = cur.fetchall()
    users = models.get_users(rows)

    conn.close()
    cur.close()
    return users


@route("/users", HTTPMethod.GET)
@middleware([Roles.ADMIN, Roles.TEACHER])
def get_users(rh: RequestHandler):
    users = fetch_users()
    rh.set_headers(HTTPStatus.OK, data=users)


@route("/users", HTTPMethod.POST)
@middleware([Roles.ADMIN])
@body_keys_needed(["name", "role", "institution", "pass"])
def add_user(rh: RequestHandler, body: dict):
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, role_title, institution_short_name, pass) VALUES (?, ?, ?, ?)",
        (
            body["name"],
            body["role"],
            body["institution"],
            body["pass"],
        ),
    )
    conn.commit()
    cur.close()
    conn.close()

    rh.set_headers(HTTPStatus.OK)


@route("/users", HTTPMethod.PUT)
@middleware([Roles.ADMIN])
@body_keys_needed(["id", "name", "role", "institution", "pass"])
def update_user(rh: RequestHandler, body: dict):
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET name = ?, role_title = ?, institution_short_name = ?, pass = ? WHERE (id = ?)",
        (
            body["name"],
            body["role"],
            body["institution"],
            body["pass"],
            body["id"],
        ),
    )
    conn.commit()
    cur.close()
    conn.close()

    rh.set_headers(HTTPStatus.OK)


@route("/users", HTTPMethod.DELETE)
@middleware([Roles.ADMIN])
@body_keys_needed(["id"])
def delete_user(rh: RequestHandler, body: dict):
    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE (id = ?)", (body["id"],))

    conn.commit()
    cur.close()
    conn.close()

    rh.set_headers(HTTPStatus.OK)
