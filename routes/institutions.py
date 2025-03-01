from http import HTTPMethod, HTTPStatus
from common import Roles, body_keys_needed, middleware, route
import database as db
import models
from routes.login import getRoleByToken
from server import RequestHandler
from utils import get_body


@route("/institutions", HTTPMethod.GET)
@middleware([Roles.ADMIN, Roles.TEACHER])
def get_institutions(rh: RequestHandler):
    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM institutions")
    rows = models.get_institutions(cur.fetchall())

    rh.set_headers(HTTPStatus.OK, data=rows)


@route("/institutions", HTTPMethod.POST)
@middleware([Roles.ADMIN])
@body_keys_needed(["short_name", "name"])
def add_institution(rh: RequestHandler, body: dict):
    rh.set_headers(HTTPStatus.OK)
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO institutions (short_name, name) VALUES (?, ?)",
        (
            body["short_name"],
            body["name"],
        ),
    )
    conn.commit()
    cur.close()
    conn.close()


# TEST: Writed without test
@route("/institutions", HTTPMethod.PUT)
@middleware([Roles.ADMIN])
@body_keys_needed(["last_short_name", "short_name", "name"])
def update_institution(rh: RequestHandler, body: dict):
    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE institutions SET short_name = ?, name = ? WHERE (short_name = ?)",
        (
            body["short_name"],
            body["name"],
            body["last_short_name"],
        ),
    )

    cur.close()
    conn.commit()
    conn.close()
    rh.set_headers(HTTPStatus.OK)


# TEST: Writed without test
@route("/institutions", HTTPMethod.DELETE)
@middleware([Roles.ADMIN])
@body_keys_needed(["short_name"])
def remove_institution(rh: RequestHandler, body: dict):
    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM institutions WHERE short_name = ?", (body["short_name"],))

    cur.close()
    conn.commit()
    conn.close()

    rh.set_headers(HTTPStatus.OK)
