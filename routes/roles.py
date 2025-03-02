from http import HTTPMethod, HTTPStatus
from common import Roles, body_keys_needed, middleware, route
import database as db
import models
from server import RequestHandler


@route("/roles", HTTPMethod.GET)
@middleware([Roles.ADMIN])
def get_roles(rh: RequestHandler, role: Roles):
    _ = role
    conn, cur = db.get_connection_and_cursor()

    cur.execute("SELECT * FROM roles")
    roles = models.get_roles(cur.fetchall())

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK, data=roles)


@route("/roles", HTTPMethod.POST)
@middleware([Roles.ADMIN])
@body_keys_needed(["title"])
def add_role(rh: RequestHandler, body: dict, role: Roles):
    _ = role
    conn, cur = db.get_connection_and_cursor()
    cur.execute(
        "INSERT INTO roles (title) VALUES (?)",
        (body["title"],),
    )

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK)


@route("/roles", HTTPMethod.PUT)
@middleware([Roles.ADMIN])
@body_keys_needed(["last_title", "title"])
def update_role(rh: RequestHandler, body: dict, role: Roles):
    _ = role
    conn, cur = db.get_connection_and_cursor()

    cur.execute(
        "UPDATE roles SET title = ? WHERE (title = ?)",
        (
            body["title"],
            body["last_title"],
        ),
    )

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK)


@route("/roles", HTTPMethod.DELETE)
@middleware([Roles.ADMIN])
@body_keys_needed(["title"])
def remove_role(rh: RequestHandler, body: dict, role: Roles):
    _ = role
    conn, cur = db.get_connection_and_cursor()

    cur.execute("DELETE FROM roles WHERE title = ?", (body["title"],))

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK)
