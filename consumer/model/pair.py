"""
Base classes wit Pair model and database functions
"""
import pydantic as pd


class Pair(pd.BaseModel):
    """
    Base class for key-value data
    """
    key: str
    value: float

    def __repr__(self):
        return f'Pair(key={self.key}, value={self.value})'

    def __str__(self):
        return repr(self)


def save(conn, *args):
    """
    :param conn: connection object
    :param args: key/value tuple
    :return: save in db key/value pair
    """
    key, value = args
    c = conn.cursor()
    c.execute("INSERT INTO pair VALUES(?, ?)", (key, value))
    conn.commit()


def retrieve(conn, key):
    """
    :param conn: connection object
    :param key: key of searched pair
    :return: retrieve first object with given key
    """
    c = conn.cursor()
    c.execute("SELECT * FROM p pair WHERE p.key = (?) LIMIT 1", key)
    conn.commit()






