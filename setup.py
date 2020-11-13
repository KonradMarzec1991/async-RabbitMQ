import sqlite3


def init_db():
    conn = sqlite3.connect('pair.db')
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
