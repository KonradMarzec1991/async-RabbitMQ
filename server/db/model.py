# pylint: disable=no-member
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

    @staticmethod
    def save(conn, *args):
        """
        :param conn: connection object
        :param args: key/value tuple
        :return: save in db key/value pair
        """
        key, value = args
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pair VALUES(?, ?)", (key, value))
        conn.commit()

    @staticmethod
    def retrieve(conn, key):
        """
        :param conn: connection object
        :param key: key of searched pair
        :return: retrieve first object with given key
        """
        cursor = conn.cursor()
        pair = cursor.execute("SELECT * FROM pair WHERE key = ?", (key, ))
        conn.commit()
        try:
            key, value = pair.fetchone()
            return dict(key=key, value=value)
        except TypeError:
            return 'Data with given key does not exist'
