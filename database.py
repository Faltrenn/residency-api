import mariadb

from config import DB_CONFIG


def get_connection() -> mariadb.Connection:
    return mariadb.connect(**DB_CONFIG)


def execute_queries(queries):
    conn = get_connection()
    cur = conn.cursor()
    results = []

    try:
        for query, params in queries:
            if query.strip().lower().startswith("select"):
                cur.execute(query, params)
                results.append(cur.fetchall())
            elif query.strip().lower().startswith("insert") and isinstance(params[0], list):
                cur.executemany(query, params)
            else:
                cur.execute(query, params)

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

    return results
