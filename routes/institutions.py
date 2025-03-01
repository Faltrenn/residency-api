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
def add_institution(rh: RequestHandler):
    body = get_body(rh)

    if not ("short_name" in body and "name"):
        raise ValueError("Invalid body")

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
def update_institution(rh: RequestHandler):
    if "token" not in rh.headers:
        rh.set_headers(HTTPStatus.BAD_REQUEST)
        return

    if (token := getRoleByToken(rh.headers["token"])) == None or token != "Admin":
        rh.set_headers(HTTPStatus.UNAUTHORIZED)
        return

    body = get_body(rh)

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
def remove_institution(rh: RequestHandler):
    if "token" not in rh.headers:
        rh.set_headers(HTTPStatus.BAD_REQUEST)
        return

    if (token := getRoleByToken(rh.headers["token"])) == None or token != "Admin":
        rh.set_headers(HTTPStatus.UNAUTHORIZED)
        return

    conn = db.get_connection()
    cur = conn.cursor()

    body = get_body(rh)

    cur.execute("DELETE FROM institutions WHERE short_name = ?", (body["short_name"],))

    cur.close()
    conn.commit()
    conn.close()

    rh.set_headers(HTTPStatus.OK)
