"""
Classes for creating RabbitMQ objects - it means PairSender and PairReceiver
"""
import json
import uuid
from operator import itemgetter
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
        self.queue_name = 'save'
        self.channel.queue_declare(queue=self.queue_name)

    def publish(self):
        """
        Sends data object to RabbitMQ queue
        :return: None
        """
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(self.obj)
        )
        print(" [x] Sent %r" % self.obj)
        self.connection.close()


class BaseReceiver(RabbitFrame):

    def __init__(self):
        super().__init__()
        self.channel.queue_declare(queue='retrieve')
        self.queue_name = 'retrieve'

    def callback(self, ch, method, properties, body):
        self.data = body

    def consume(self):
        """
        Call method turns on listening of consumer for published data
        :return: None
        """
        print(' [*] Waiting for info from monitoring. To exit press CTRL+C')
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.callback,
            auto_ack=True
        )
        self.channel.start_consuming()


class PairReceiver(RabbitFrame):
    DB_PATH = 'pair.db'

    def __init__(self):
        super().__init__()
        self.channel.queue_declare(queue='pair')
        self.queue_name = 'save'
        self.sender = PairSender(None)

    def save_to_db(self, ch, method, properties, body):
        """
        Method saves in db key-value pair
        :param body: json type data sent by api
        :return: None
        """
        body = json.loads(body)
        key, value = itemgetter('key', 'value')(body)
        with sqlite3.connect(self.DB_PATH) as conn:
            Pair.save(conn, key, value)

    def consume(self):
        """
        Call method turns on listening of consumer for published data
        :return: None
        """
        print(' [*] Waiting for info from monitoring. To exit press CTRL+C')
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.transform_body,
            auto_ack=True
        )
        self.channel.start_consuming()


class RPCSender(RabbitFrame):

    def __init__(self):
        super().__init__()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, key):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=key)
        while self.response is None:
            self.connection.process_data_events()
        return self.response


class RPCReceiver(RabbitFrame):
    DB_PATH = 'pair.db'

    def __init__(self):
        super().__init__()
        self.channel.queue_declare(queue='rpc_queue')

    def retrieve_from_db(self, body):
        with sqlite3.connect(self.DB_PATH) as conn:
            pair = Pair.retrieve(conn, body.decode('utf-8'))
        return pair

    def on_request(self, ch, method, props, body):
        print('body', body)
        response = self.retrieve_from_db(body)
        print('response', response)
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id=props.correlation_id),
            body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue='rpc_queue',
            on_message_callback=self.on_request
        )
        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()
