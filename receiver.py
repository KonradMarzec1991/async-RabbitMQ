"""
Module with code for setting receivers.
Receivers are loaded with Celery worker:
1) PairReceiver is dedicated for saving in db
2) RPCReceiver is dedicated for retrieving from db
"""
from celery import Celery

from rabbitFrame import BaseReceiver
from rpc_models import RPCReceiver


app = Celery(
    'receiver',
    backend='rpc://',
    broker='pyamqp://guest@localhost//'
)


@app.task
def save_receiver():
    """
    Create `PairReceiver` instance and consume
    """
    receiver = BaseReceiver()
    receiver.consume()


@app.task
def retrieve_receiver():
    """
    Create `RPCReceiver` instance and consume
    """
    receiver = RPCReceiver()
    receiver.consume()


def main():
    """
    Run with Celery both consumers and listen to publishing
    """
    save_receiver.delay()
    retrieve_receiver.delay()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
