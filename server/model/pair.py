"""
Base classes for creating objects and sending data to RabbitMQ
"""

import json
import pydantic as pd
from rabbit.rabbitFrame import RabbitFrame


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


class PairSender(RabbitFrame):
    """
    PairSender class deliver method for publishing data to RabbitMQ
    """
    def __init__(self, obj):
        super().__init__()
        self.obj = obj
        self.channel.queue_declare(queue='pair')

    def call(self):
        """
        Sends data object to RabbitMQ queue
        :return: None
        """
        self.channel.basic_publish(
            exchange='',
            routing_key='pair',
            body=json.dumps(self.obj)
        )
        print(" [x] Sent %r" % self.obj)
        self.connection.close()
