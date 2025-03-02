from http import HTTPMethod, HTTPStatus
from common import Roles, body_keys_needed, middleware, route
import database as db
import models
from server import RequestHandler


@route("/institutions", HTTPMethod.GET)
@middleware([Roles.ADMIN, Roles.TEACHER])
def get_institutions(rh: RequestHandler):
    conn, cur = db.get_connection_and_cursor()

    cur.execute("SELECT * FROM institutions")
    rows = models.get_institutions(cur.fetchall())

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK, data=rows)


@route("/institutions", HTTPMethod.POST)
@middleware([Roles.ADMIN])
@body_keys_needed(["short_name", "name"])
def add_institution(rh: RequestHandler, body: dict):
    conn, cur = db.get_connection_and_cursor()
    cur.execute(
        "INSERT INTO institutions (short_name, name) VALUES (?, ?)",
        (
            body["short_name"],
            body["name"],
        ),
    )

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK)


@route("/institutions", HTTPMethod.PUT)
@middleware([Roles.ADMIN])
@body_keys_needed(["last_short_name", "short_name", "name"])
def update_institution(rh: RequestHandler, body: dict):
    conn, cur = db.get_connection_and_cursor()

    cur.execute(
        "UPDATE institutions SET short_name = ?, name = ? WHERE (short_name = ?)",
        (
            body["short_name"],
            body["name"],
            body["last_short_name"],
        ),
    )

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK)


@route("/institutions", HTTPMethod.DELETE)
@middleware([Roles.ADMIN])
@body_keys_needed(["short_name"])
def remove_institution(rh: RequestHandler, body: dict):
    conn, cur = db.get_connection_and_cursor()

    cur.execute("DELETE FROM institutions WHERE short_name = ?", (body["short_name"],))

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK)
