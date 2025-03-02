from http import HTTPMethod, HTTPStatus
from common import Roles, body_keys_needed, middleware, route
import database as db
import models
from server import RequestHandler


@route("/questionnaires", HTTPMethod.GET)
@middleware([*Roles.all()])
def get_questionnaires(rh: RequestHandler):
    results = db.execute_queries(
        [
            (
                "SELECT * FROM questionnaire q INNER JOIN users p ON p.id = q.professor_id INNER JOIN users r ON r.id = q.resident_id  INNER JOIN questions_answereds qa ON qa.questionnaire_id = q.id INNER JOIN questions q2 ON q2.id = qa.question_id INNER JOIN answers a ON a.id = qa.answer_id ORDER BY q.id",
                (),
            )
        ]
    )

    questionnaires = models.get_questionnaires(results[0])

    rh.set_headers(HTTPStatus.OK, data=questionnaires)


@route("/questionnaires", HTTPMethod.POST)
@middleware([Roles.ADMIN, Roles.TEACHER])
@body_keys_needed(
    ["procedure_title", "professor_id", "resident_id", "questions_answereds"]
)
def add_question(rh: RequestHandler, body: dict):
    conn, cur = db.get_connection_and_cursor()
    cur.execute(
        "INSERT INTO questionnaire (procedure_title, professor_id, resident_id) VALUES (?, ?, ?)",
        (
            body["procedure_title"],
            body["professor_id"],
            body["resident_id"],
        ),
    )
    q_id = cur.lastrowid

    cur.executemany(
        "INSERT INTO questions_answereds (questionnaire_id, question_id, answer_id) VALUES (?, ?, ?)",
        [
            (q_id, qa["question_id"], qa["answer_id"])
            for qa in body["questions_answereds"]
        ],
    )

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK)


@route("/questionnaires", HTTPMethod.PUT)
@middleware([Roles.ADMIN, Roles.TEACHER])
@body_keys_needed(
    ["id", "procedure_title", "professor_id", "resident_id", "questions_answereds"]
)
def update_question(rh: RequestHandler, body: dict):
    conn, cur = db.get_connection_and_cursor()

    cur.execute(
        "UPDATE questionnaire set procedure_title = ?, professor_id = ?, resident_id = ? WHERE id = ?",
        (
            body["procedure_title"],
            body["professor_id"],
            body["resident_id"],
            body["id"],
        ),
    )

    cur.executemany(
        "UPDATE questions_answereds SET answer_id = ? WHERE questionnaire_id = ? AND question_id = ?",
        [
            (
                answer["answer_id"],
                body["id"],
                answer["question_id"],
            )
            for answer in body["questions_answereds"]
        ],
    )

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK)


@route("/questionnaires", HTTPMethod.DELETE)
@middleware([Roles.ADMIN, Roles.TEACHER])
@body_keys_needed(["id"])
def remove_question(rh: RequestHandler, body: dict):
    conn, cur = db.get_connection_and_cursor()

    cur.execute(
        "DELETE FROM questions_answereds WHERE questionnaire_id = ?",
        (body["id"],),
    )

    cur.execute("DELETE FROM questionnaire WHERE id = ?", (body["id"],))

    db.cc_connection_and_cursor(conn, cur)

    rh.set_headers(HTTPStatus.OK)
