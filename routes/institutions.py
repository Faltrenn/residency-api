
from http import HTTPMethod, HTTPStatus
from common import route
import database as db
import models
from routes.login import getRoleByToken
from server import RequestHandler


@route("/institutions", HTTPMethod.GET)
def get_roles(rh: RequestHandler):
    if "token" not in rh.headers:
        rh.set_headers(HTTPStatus.BAD_REQUEST)
        return

    if (token := getRoleByToken(rh.headers["token"])) == None or token != "Admin":
        rh.set_headers(HTTPStatus.UNAUTHORIZED)
        return

    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM institutions")
    rows = models.get_institutions(cur.fetchall())

    rh.set_headers(HTTPStatus.OK, data = rows)
