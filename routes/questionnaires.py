from http import HTTPMethod, HTTPStatus
from common import route
import database as db
import models
from routes.login import getRoleByToken
from server import RequestHandler
from utils import get_body


@route("/questionnaires", HTTPMethod.GET)
def get_questionnaires(rh: RequestHandler):
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
                "SELECT * FROM questionnaire q INNER JOIN users p ON p.id = q.professor_id INNER JOIN users r ON r.id = q.resident_id  INNER JOIN questions_answereds qa ON qa.questionnaire_id = q.id INNER JOIN questions q2 ON q2.id = qa.question_id INNER JOIN answers a ON a.id = qa.answer_id ORDER BY q.id;",
                (),
            )
        ]
    )

    questionnaires = models.get_questionnaires(results[0])

    rh.set_headers(HTTPStatus.OK, data=questionnaires)


@route("/questionnaires", HTTPMethod.POST)
def add_question(rh: RequestHandler):
    body = get_body(rh)

    if not ("title" in body and "answers" in body):
        raise ValueError("Invalid body")

    rh.set_headers(HTTPStatus.OK)
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO questionnaires (title) VALUES (?)",
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
@route("/questionnaires", HTTPMethod.PUT)
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
        "DELETE FROM questionnaires_answereds WHERE answer_id IN (SELECT id FROM answers WHERE question_id = ?)",
        (body["id"],),
    )

    cur.execute("DELETE FROM answers WHERE question_id = ?", (body["id"],))

    cur.execute(
        "UPDATE questionnaires SET title = ? WHERE id = ?", (body["title"], body["id"])
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
@route("/questionnaires", HTTPMethod.DELETE)
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
        "DELETE FROM questions_answereds WHERE questionnaire_id = ?",
        (body["id"],),
    )

    # cur.executemany(
    #     "DELETE FROM answers WHERE (id = ?)",
    #     [(answer["id"],) for answer in body["answers"]],
    # )

    cur.execute("DELETE FROM questionnaire WHERE id = ?", (body["id"],))

    conn.commit()
    cur.close()
    conn.close()

    rh.set_headers(HTTPStatus.OK)
