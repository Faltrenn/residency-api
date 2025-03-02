from http import HTTPMethod, HTTPStatus
from common import Roles, UserInfo, body_keys_needed, middleware, route
import database as db
import models
from server import RequestHandler


@route("/procedures", HTTPMethod.GET)
@middleware([Roles.ADMIN, Roles.TEACHER])
def get_procedures(rh: RequestHandler, user_info: UserInfo):
    _ = user_info
    conn, cur = db.get_connection_and_cursor()

    cur.execute("SELECT * FROM procedures ORDER BY title")
    procedures = models.get_procedures(cur.fetchall())

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK, data=procedures)


@route("/procedures", HTTPMethod.POST)
@middleware([Roles.ADMIN, Roles.TEACHER])
@body_keys_needed(["title"])
def add_role(rh: RequestHandler, body: dict, user_info: UserInfo):
    _ = user_info
    conn, cur = db.get_connection_and_cursor()

    cur.execute(
        "INSERT INTO procedures (title) VALUES (?)",
        (body["title"],),
    )

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK)


@route("/procedures", HTTPMethod.PUT)
@middleware([Roles.ADMIN, Roles.TEACHER])
@body_keys_needed(["last_title", "title"])
def update_role(rh: RequestHandler, body: dict, user_info: UserInfo):
    _ = user_info
    conn, cur = db.get_connection_and_cursor()

    cur.execute(
        "UPDATE procedures SET title = ? WHERE (title = ?)",
        (
            body["title"],
            body["last_title"],
        ),
    )

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK)


@route("/procedures", HTTPMethod.DELETE)
@middleware([Roles.ADMIN, Roles.TEACHER])
@body_keys_needed(["title"])
def remove_role(rh: RequestHandler, body: dict, user_info: UserInfo):
    _ = user_info
    conn, cur = db.get_connection_and_cursor()

    cur.execute("DELETE FROM procedures WHERE title = ?", (body["title"],))

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK)
