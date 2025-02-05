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

    results = db.execute_queries(
        [
            (
                "SELECT q.*, a.id, a.title \
                 FROM questions q INNER JOIN answers a \
                 WHERE a.question_id = q.id\
                 ORDER BY q.id",
                (),
            )
        ]
    )

    questions = models.get_questions(results[0])

    rh.set_headers(HTTPStatus.OK, data=questions)


@route("/questions", HTTPMethod.POST)
def add_question(rh: RequestHandler):
    body = get_body(rh)

    if not ("title" in body and "answers" in body):
        raise ValueError("Invalid body")

    rh.set_headers(HTTPStatus.OK)
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO questions (title) VALUES (?)",
        (body["title"],),
    )
    q_id = cur.lastrowid
    cur.executemany(
        "INSERT INTO answers (title, question_id) VALUES (?, ?)",
        [(answer["title"], q_id) for answer in body["answers"]],
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
        "DELETE FROM questions_answereds WHERE answer_id IN (SELECT id FROM answers WHERE question_id = ?)",
        (body["id"],),
    )

    cur.execute("DELETE FROM answers WHERE question_id = ?", (body["id"],))

    cur.execute(
        "UPDATE questions SET title = ? WHERE id = ?", (body["title"], body["id"])
    )

    cur.executemany(
        "INSERT INTO answers (title, question_id) VALUES (?, ?)",
        [(answer["title"], body["id"]) for answer in body["answers"]],
    )

    # cur.executemany(
    #     "UPDATE answers SET title = ? WHERE (id = ?)",
    #     [(answer["title"], answer["id"]) for answer in body["answers"]],
    # )

    conn.commit()
    cur.close()
    conn.close()

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

    cur.execute(
        "DELETE FROM answers WHERE question_id = ?",
        (body["id"],),
    )
    # cur.executemany(
    #     "DELETE FROM answers WHERE (id = ?)",
    #     [(answer["id"],) for answer in body["answers"]],
    # )

    cur.execute("DELETE FROM questions WHERE id = ?", (body["id"],))

    conn.commit()
    cur.close()
    conn.close()

    rh.set_headers(HTTPStatus.OK)
