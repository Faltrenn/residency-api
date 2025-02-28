from http import HTTPMethod, HTTPStatus
from common import route
import database as db
import models
from server import RequestHandler
from utils import get_body


@route("/procedures", HTTPMethod.GET)
def get_procedures(rh: RequestHandler):

    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM procedures ORDER BY title")
    procedures = models.get_procedures(cur.fetchall())

    rh.set_headers(HTTPStatus.OK, data=procedures)


@route("/procedures", HTTPMethod.POST)
def add_role(rh: RequestHandler):
    body = get_body(rh)

    if not ("title" in body):
        raise ValueError("Invalid body")

    rh.set_headers(HTTPStatus.OK)
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO procedures (title) VALUES (?)",
        (body["title"],),
    )
    conn.commit()
    cur.close()
    conn.close()


# TEST: Writed without test
@route("/procedures", HTTPMethod.PUT)
def update_role(rh: RequestHandler):
    if "token" not in rh.headers:
        rh.set_headers(HTTPStatus.BAD_REQUEST)
        return

    body = get_body(rh)

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
def remove_role(rh: RequestHandler):
    if "token" not in rh.headers:
        rh.set_headers(HTTPStatus.BAD_REQUEST)
        return

    conn = db.get_connection()
    cur = conn.cursor()

    body = get_body(rh)

    cur.execute("DELETE FROM procedures WHERE title = ?", (body["title"],))

    conn.commit()
    cur.close()
    conn.close()

    rh.set_headers(HTTPStatus.OK)
