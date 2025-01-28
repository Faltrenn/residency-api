from http import HTTPMethod, HTTPStatus
import json
from common import route
import database as db
import models
from routes.login import getRoleByToken
from server import RequestHandler


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
    rows = models.get_roles(cur.fetchall())

    roles = json.dumps(rows).encode("utf-8")

    rh.set_headers(HTTPStatus.OK)
    rh.wfile.write(roles)
