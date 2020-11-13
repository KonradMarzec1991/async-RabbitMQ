"""
Classes for creating RabbitMQ objects
"""
import json
import sqlite3
import pika

from model import Pair


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


class PairReceiver(RabbitFrame):
    DB_PATH = 'pair.db'

    def __init__(self):
        super().__init__()
        self.channel.queue_declare(queue='pair')

    def save_to_db(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        body = json.loads(body)
        key = body['key']
        value = body['value']
        with sqlite3.connect(self.DB_PATH) as conn:
            Pair.save(conn, key, value)

    def retrieve_from_db(self, ch, method, properties, body):
        key = json.loads(body)['key_name']
        with sqlite3.connect(self.DB_PATH) as conn:
            Pair.retrieve(conn, key)

    def call(self):
        print(' [*] Waiting for info from monitoring. To exit press CTRL+C')
        self.channel.basic_consume(
            queue='pair',
            on_message_callback=self.save_to_db,
            auto_ack=True
        )
        self.channel.start_consuming()
