import database as db
import models

def auth_user(user, password) -> dict | None:
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * from users WHERE name = ? AND pass = ?", (user, password))
    user = models.get_user(cur.fetchone())

    conn.close()
    cur.close()
    return user
