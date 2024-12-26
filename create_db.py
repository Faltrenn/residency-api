import mariadb

config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "password",
    "database": "db_residency",
}
conn = mariadb.connect(**config)
cur = conn.cursor()

cur.execute("SELECT * FROM roles")
fetched = cur.fetchall()
for role in fetched:
    for attr in role:
        print(attr)

conn.close()
