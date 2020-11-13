import os
import pika
import sys
import json
from sqlite3 import connect


def save(conn, *args):
    key, value = args
    c = conn.cursor()
    c.execute("INSERT INTO pair VALUES(?, ?)", (key, value))
    conn.commit()


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue='pair')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        body = json.loads(body)
        key = body['key']
        value = body['value']
        with connect('pair.db') as conn:
            save(conn, key, value)

    channel.basic_consume(
        queue='pair',
        on_message_callback=callback,
        auto_ack=True
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)