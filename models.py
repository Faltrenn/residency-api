def get_user(row) -> dict:
    return (
        {
            "id": row[0],
            "name": row[1],
            "pass": row[2],
            "role": row[3],
            "institution": row[4],
        }
        if row
        else {}
    )


def get_users(rows) -> list[dict]:
    return (
        [get_user(row) for row in rows]
        if rows
        else []
    )
