"""
Module with database setup scripts
"""
import sqlite3
from setup import settings


def init_db():
    """
    Function creates:
    1) Connection to database (in our example it is `pair.db`)
    2) Table for key-value pairs
    3) Example record with key: first and value: 1
    If table exists, script catches sqlite3 exception and breaks code
    :return: None
    """
    conn = sqlite3.connect(settings.DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("""CREATE TABLE pair (
            key VARCHAR(100) NOT NULL,
            value REAL NOT NULL
        )""")
        cursor.execute("""INSERT INTO pair VALUES ('first', 1)""")
    except sqlite3.OperationalError:
        return

    conn.commit()
    print('DB initialized')
