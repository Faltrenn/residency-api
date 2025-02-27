from common import middleware, route
from http import HTTPMethod, HTTPStatus
from server import RequestHandler
from typing import List
import database as db
import models
from utils import get_body


def fetch_users() -> List[dict]:
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("select * from users")
    rows = cur.fetchall()
    users = models.get_users(rows)

    conn.close()
    cur.close()
    return users


def remove_user() -> List[dict]:
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("select * from users")
    rows = cur.fetchall()
    users = models.get_users(rows)

    conn.close()
    cur.close()
    return users


@middleware(allowedRoles=["Admin", "Professor"])
@route("/users", HTTPMethod.GET)
def get_users(rh: RequestHandler):
    # if "token" not in rh.headers:
    #     rh.set_headers(HTTPStatus.BAD_REQUEST)
    #     return
    # role = getRoleByToken(rh.headers["token"])
    # if not role or role != "Admin":
    #     rh.set_headers(HTTPStatus.UNAUTHORIZED)
    #     return

    users = fetch_users()
    rh.set_headers(HTTPStatus.OK, data = users)


@route("/users", HTTPMethod.POST)
def add_user(rh: RequestHandler):
    body = get_body(rh)

    if not (
        "name" in body and "role" in body and "pass" in body and "institution" in body
    ):
        raise ValueError("Invalid body")

    rh.set_headers(HTTPStatus.OK)
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, pass, role_title, institution_short_name) VALUES (?, ?, ?, ?)",
        (
            body["name"],
            body["pass"],
            body["role"],
            body["institution"],
        ),
    )
    conn.commit()
    cur.close()
    conn.close()


@route("/users", HTTPMethod.PUT)
def update_user(rh: RequestHandler):
    body = get_body(rh)

    if not (
        "id" in body
        and "name" in body
        and "role" in body
        and "pass" in body
        and "institution" in body
    ):
        rh.set_headers(HTTPStatus.BAD_REQUEST)
        return

    rh.set_headers(HTTPStatus.OK)
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET name = ?, pass = ?, role_title = ?, institution_short_name = ? WHERE (id = ?)",
        (
            body["name"],
            body["pass"],
            body["role"],
            body["institution"],
            body["id"],
        ),
    )
    conn.commit()
    cur.close()
    conn.close()


@route("/users", HTTPMethod.DELETE)
def delete_user(rh: RequestHandler):
    body = get_body(rh)
    if "id" not in body:
        rh.set_headers(HTTPStatus.BAD_REQUEST)
        return

    rh.set_headers(HTTPStatus.OK)
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE (id = ?)", (body["id"],))
    conn.commit()
    cur.close()
    conn.close()
