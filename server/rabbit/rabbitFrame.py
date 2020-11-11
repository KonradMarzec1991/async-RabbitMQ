"""
Classes for creating RabbitMQ objects
"""
import pika


class RabbitFrame:
    """
    Base class for delivering RabbitMQ connection/channel objects
    """
    def __init__(self):
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        self._channel = self.connection.channel()

    @property
    def connection(self):
        """Connection attr getter"""
        return self._connection

    @property
    def channel(self):
        """Channel attr getter"""
        return self._channel
