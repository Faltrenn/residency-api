from http import HTTPMethod, HTTPStatus
from common import route
import database as db
import models
from routes.login import getRoleByToken
from server import RequestHandler
from utils import get_body


@route("/roles", HTTPMethod.GET)
def get_roles(rh: RequestHandler):
    if "token" not in rh.headers:
        rh.set_headers(HTTPStatus.BAD_REQUEST)
        return

    if (token := getRoleByToken(rh.headers["token"])) == None or token != "Admin":
        rh.set_headers(HTTPStatus.UNAUTHORIZED)
        return

    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM roles")
    roles = models.get_roles(cur.fetchall())

    rh.set_headers(HTTPStatus.OK, data=roles)


@route("/roles", HTTPMethod.POST)
def add_role(rh: RequestHandler):
    body = get_body(rh)

    if not ("title" in body):
        raise ValueError("Invalid body")

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


# TEST: Writed without test
@route("/roles", HTTPMethod.PUT)
def update_role(rh: RequestHandler):
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


# TEST: Writed without test
@route("/roles", HTTPMethod.DELETE)
def remove_role(rh: RequestHandler):
    if "token" not in rh.headers:
        rh.set_headers(HTTPStatus.BAD_REQUEST)
        return

    if (token := getRoleByToken(rh.headers["token"])) == None or token != "Admin":
        rh.set_headers(HTTPStatus.UNAUTHORIZED)
        return

    conn = db.get_connection()
    cur = conn.cursor()

    body = get_body(rh)

    cur.execute("DELETE FROM roles WHERE title = ?", (body["title"],))

    conn.commit()
    cur.close()
    conn.close()

    rh.set_headers(HTTPStatus.OK)
