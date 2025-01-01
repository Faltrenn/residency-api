def get_user(row):
    return {
        "id": row[0],
        "name": row[1],
        "pass": row[2],
        "role": row[3],
        "institution": row[4],
    }

def get_users(rows):
    return [get_user(row) for row in rows]
