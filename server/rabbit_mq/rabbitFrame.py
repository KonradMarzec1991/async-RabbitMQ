# pylint: disable=import-error,invalid-name
"""
Classes for creating RabbitMQ objects - it means PairSender and PairReceiver
"""
import json
from operator import itemgetter
import sqlite3
import pika
from setup import settings

from db.model import Pair


class RabbitFrame:
    """
    Base class for delivering RabbitMQ connection/channel objects
    """
    def __init__(self):
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters('rabbitmq')
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


class BaseSender(RabbitFrame):
    """
    BaseSender class deliver method for publishing data to RabbitMQ
    """
    def __init__(self, obj):
        super().__init__()
        self.obj = obj
        # self.queue_name = 'save'
        # self.channel.queue_declare(queue='saver')

    def publish(self):
        """
        Sends data object to RabbitMQ queue
        :return: None
        """
        self.channel.basic_publish(
            exchange='',
            routing_key='saver',
            body=json.dumps(self.obj)
        )
        self.connection.close()


class BaseReceiver(RabbitFrame):
    """
    BaseReceiver class consumes published data
    """
    def __init__(self):
        super().__init__()
        # self.channel.queue_declare(queue='pair')
        self.channel.queue_declare(queue='saver')
        self.queue_name = 'saver'

    @staticmethod
    # pylint: disable=attribute-defined-outside-init,unused-argument
    def save_to_db(ch, method, properties, body):
        """
        Method saves in db key-value pair
        :param body: json type data sent by api
        :return: None
        """
        body = json.loads(body)
        key, value = itemgetter('key', 'value')(body)
        with sqlite3.connect(settings.DB_NAME) as conn:
            Pair.save(conn, key, value)

    def consume(self):
        """
        Call method turns on listening of consumer for published data
        :return: None
        """
        self.channel.basic_consume(
            queue='saver',
            on_message_callback=self.save_to_db,
            auto_ack=True
        )
        self.channel.start_consuming()
