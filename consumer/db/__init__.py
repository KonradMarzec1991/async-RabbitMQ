import sqlite3


def db_init():
    conn = sqlite3.connect('pair.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE pair (
        id serial PRIMARY KEY,
        key VARCHAR(100) NOT NULL,
        value REAL NOT NULL
    )""")

    conn.commit()
    conn.close()
