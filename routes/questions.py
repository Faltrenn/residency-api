from http import HTTPMethod, HTTPStatus
from common import Roles, body_keys_needed, middleware, route
import database as db
import models
from routes.login import getRoleByToken
from server import RequestHandler
from utils import get_body


@route("/questions", HTTPMethod.GET)
@middleware([Roles.ADMIN, Roles.TEACHER])
def get_questions(rh: RequestHandler):
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
@middleware([Roles.ADMIN])
@body_keys_needed(["title", "answers"])
def add_question(rh: RequestHandler, body: dict):
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

    rh.set_headers(HTTPStatus.OK)


@route("/questions", HTTPMethod.PUT)
@middleware([Roles.ADMIN])
@body_keys_needed(["id", "title", "answers"])
def update_question(rh: RequestHandler, body: dict):
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

    conn.commit()
    cur.close()
    conn.close()

    rh.set_headers(HTTPStatus.OK)


@route("/questions", HTTPMethod.DELETE)
@middleware([Roles.ADMIN])
@body_keys_needed(["id"])
def remove_question(rh: RequestHandler, body: dict):
    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM answers WHERE question_id = ?",
        (body["id"],),
    )

    cur.execute("DELETE FROM questions WHERE id = ?", (body["id"],))

    conn.commit()
    cur.close()
    conn.close()

    rh.set_headers(HTTPStatus.OK)
