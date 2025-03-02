from http import HTTPMethod, HTTPStatus
from common import Roles, body_keys_needed, middleware, route
import database as db
import models
from server import RequestHandler


@route("/procedures", HTTPMethod.GET)
@middleware([Roles.ADMIN, Roles.TEACHER])
def get_procedures(rh: RequestHandler):
    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM procedures ORDER BY title")
    procedures = models.get_procedures(cur.fetchall())

    rh.set_headers(HTTPStatus.OK, data=procedures)


@route("/procedures", HTTPMethod.POST)
@middleware([Roles.ADMIN, Roles.TEACHER])
@body_keys_needed(["title"])
def add_role(rh: RequestHandler, body: dict):
    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO procedures (title) VALUES (?)",
        (body["title"],),
    )

    conn.commit()
    cur.close()
    conn.close()

    rh.set_headers(HTTPStatus.OK)


# TEST: Writed without test
@route("/procedures", HTTPMethod.PUT)
@middleware([Roles.ADMIN, Roles.TEACHER])
@body_keys_needed(["last_title", "title"])
def update_role(rh: RequestHandler, body: dict):
    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE procedures SET title = ? WHERE (title = ?)",
        (
            body["title"],
            body["last_title"],
        ),
    )

    conn.commit()
    cur.close()
    conn.close()
    rh.set_headers(HTTPStatus.OK)


# TEST: Writed without test
@route("/procedures", HTTPMethod.DELETE)
@middleware([Roles.ADMIN, Roles.TEACHER])
@body_keys_needed(["title"])
def remove_role(rh: RequestHandler, body: dict):
    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM procedures WHERE title = ?", (body["title"],))

    conn.commit()
    cur.close()
    conn.close()

    rh.set_headers(HTTPStatus.OK)
