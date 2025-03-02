from http import HTTPMethod, HTTPStatus
from common import Roles, body_keys_needed, middleware, route
import database as db
import models
from routes.login import getRoleByToken
from server import RequestHandler
from utils import get_body


@route("/roles", HTTPMethod.GET)
@middleware([Roles.ADMIN])
def get_roles(rh: RequestHandler):
    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM roles")
    roles = models.get_roles(cur.fetchall())

    rh.set_headers(HTTPStatus.OK, data=roles)


@route("/roles", HTTPMethod.POST)
@middleware([Roles.ADMIN])
@body_keys_needed(["title"])
def add_role(rh: RequestHandler, body: dict):
    rh.set_headers(HTTPStatus.OK)
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO roles (title) VALUES (?)",
        (body["title"],),
    )
    conn.commit()
    cur.close()
    conn.close()


@route("/roles", HTTPMethod.PUT)
@middleware([Roles.ADMIN])
@body_keys_needed(["last_title", "title"])
def update_role(rh: RequestHandler, body: dict):
    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE roles SET title = ? WHERE (title = ?)",
        (
            body["title"],
            body["last_title"],
        ),
    )
    conn.commit()
    cur.close()
    conn.close()

    rh.set_headers(HTTPStatus.OK)


@route("/roles", HTTPMethod.DELETE)
@middleware([Roles.ADMIN])
@body_keys_needed(["title"])
def remove_role(rh: RequestHandler, body: dict):
    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM roles WHERE title = ?", (body["title"],))

    conn.commit()
    cur.close()
    conn.close()

    rh.set_headers(HTTPStatus.OK)
