import database as db
import models


def auth_user(username: str, password: str) -> dict | None:
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * from users WHERE name = ? AND pass = ?", (username, password))
    user = models.get_user(cur.fetchone())

    conn.close()
    cur.close()
    return user

def get_user(id: int) -> dict | None:
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * from users WHERE id = ?", (id,))
    user = models.get_user(cur.fetchone())

    conn.close()
    cur.close()
    return user
