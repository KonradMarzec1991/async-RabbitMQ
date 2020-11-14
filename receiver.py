from rabbitFrame import (
    PairReceiver,
    RPCReceiver
)
from celery import Celery


app = Celery(
    'receiver',
    backend='rpc://',
    broker='pyamqp://guest@localhost//'
)


@app.task
def save_receiver():
    receiver = PairReceiver()
    receiver.consume()


@app.task
def retrieve_receiver():
    receiver = RPCReceiver()
    receiver.consume()


def main():
    save_receiver.delay()
    retrieve_receiver.delay()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
