import pika
from rabbitFrame import RabbitFrame


class RPCReceiver(RabbitFrame):
    def __init__(self):
        super().__init__()
        self.channel.queue_declare(queue='rpc_queue')

    def fib(self, n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.fib(n - 1) + self.fib(n - 2)

    def on_request(self, ch, method, props, body):
        print('from receiver', body)
        n = body
        print(" [.] fib(%s)" % n)
        response = self.fib(n)

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


r = RPCReceiver()
r.consume()
