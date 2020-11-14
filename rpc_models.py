from rabbitFrame import RabbitFrame
import uuid
import sqlite3
import pika

from model import Pair
import settings


class RPCSender(RabbitFrame):

    def __init__(self):
        super().__init__()
        result = self.channel.queue_declare(
            queue='',
            exclusive=True
        )
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

    def __init__(self):
        super().__init__()
        self.channel.queue_declare(queue='rpc_queue')

    def retrieve_from_db(self, body):
        with sqlite3.connect(settings.DB_NAME) as conn:
            pair = Pair.retrieve(conn, body.decode('utf-8'))
        return pair

    def on_request(self, ch, method, props, body):
        response = self.retrieve_from_db(body)
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id=props.correlation_id
            ),
            body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue='rpc_queue',
            on_message_callback=self.on_request
        )
        self.channel.start_consuming()
