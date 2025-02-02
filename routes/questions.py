from http import HTTPMethod, HTTPStatus
from common import route
import database as db
import models
from routes.login import getRoleByToken
from server import RequestHandler
from utils import get_body


@route("/questions", HTTPMethod.GET)
def get_questions(rh: RequestHandler):
    # if "token" not in rh.headers:
    #     rh.set_headers(HTTPStatus.BAD_REQUEST)
    #     return
    #
    # if (token := getRoleByToken(rh.headers["token"])) == None or token != "Admin":
    #     rh.set_headers(HTTPStatus.UNAUTHORIZED)
    #     return

    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM questions")
    questions = models.get_questions(cur.fetchall())

    rh.set_headers(HTTPStatus.OK, data=questions)


# TEST: Writed without test
@route("/questions", HTTPMethod.POST)
def add_question(rh: RequestHandler):
    body = get_body(rh)

    if not ("title" in body):
        raise ValueError("Invalid body")

    rh.set_headers(HTTPStatus.OK)
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO questions (title) VALUES (?)",
        (body["title"],),
    )
    conn.commit()
    cur.close()
    conn.close()


# TEST: Writed without test
@route("/questions", HTTPMethod.PUT)
def update_question(rh: RequestHandler):
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
        "UPDATE questions SET title = ? WHERE (id = ?)",
        (
            body["title"],
            body["id"],
        ),
    )
    rh.set_headers(HTTPStatus.OK)


# TEST: Writed without test
@route("/questions", HTTPMethod.DELETE)
def remove_question(rh: RequestHandler):
    if "token" not in rh.headers:
        rh.set_headers(HTTPStatus.BAD_REQUEST)
        return

    if (token := getRoleByToken(rh.headers["token"])) == None or token != "Admin":
        rh.set_headers(HTTPStatus.UNAUTHORIZED)
        return

    conn = db.get_connection()
    cur = conn.cursor()

    body = get_body(rh)

    cur.execute("DELETE FROM questions WHERE id = ?", (body["id"],))

    rh.set_headers(HTTPStatus.OK)
