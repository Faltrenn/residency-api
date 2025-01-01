import mariadb

from config import DB_CONFIG

def get_connection() -> mariadb.Connection:
    return mariadb.connect(**DB_CONFIG)
