from common import Roles, UserInfo, body_keys_needed, middleware, route
from http import HTTPMethod, HTTPStatus
from server import RequestHandler
from typing import List
import database as db
import models


def fetch_users(role: Roles) -> List[dict]:
    conn, cur = db.get_connection_and_cursor()

    cur.execute(
        "SELECT * FROM users"
        if role is Roles.ADMIN
        else "SELECT * FROM users EXCEPT(SELECT * FROM users WHERE role_title = 'Admin' OR role_title = 'Professor')"
    )
    rows = cur.fetchall()
    users = models.get_users(rows)

    db.cc_connection_and_cursor(conn, cur)
    return users


def remove_user() -> List[dict]:
    conn, cur = db.get_connection_and_cursor()
    cur.execute("select * from users")
    rows = cur.fetchall()
    users = models.get_users(rows)

    db.cc_connection_and_cursor(conn, cur)
    return users


@route("/users", HTTPMethod.GET)
@middleware([Roles.ADMIN, Roles.TEACHER])
def get_users(rh: RequestHandler, user_info: UserInfo):
    users = fetch_users(user_info.role)
    rh.set_headers(HTTPStatus.OK, data=users)


@route("/users", HTTPMethod.POST)
@middleware([Roles.ADMIN])
@body_keys_needed(["name", "role", "institution", "pass"])
def add_user(rh: RequestHandler, body: dict, user_info: UserInfo):
    _ = user_info
    conn, cur = db.get_connection_and_cursor()
    cur.execute(
        "INSERT INTO users (name, role_title, institution_short_name, pass) VALUES (?, ?, ?, ?)",
        (
            body["name"],
            body["role"],
            body["institution"],
            body["pass"],
        ),
    )

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK)


@route("/users", HTTPMethod.PUT)
@middleware([Roles.ADMIN])
@body_keys_needed(["id", "name", "role", "institution", "pass"])
def update_user(rh: RequestHandler, body: dict, user_info: UserInfo):
    _ = user_info
    conn, cur = db.get_connection_and_cursor()
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

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK)


@route("/users", HTTPMethod.DELETE)
@middleware([Roles.ADMIN])
@body_keys_needed(["id"])
def delete_user(rh: RequestHandler, body: dict, user_info: UserInfo):
    _ = user_info
    conn, cur = db.get_connection_and_cursor()

    cur.execute("DELETE FROM users WHERE (id = ?)", (body["id"],))

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK)
