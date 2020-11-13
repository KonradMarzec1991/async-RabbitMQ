import os
import sys
from server.rabbit.rabbitFrame import PairReceiver


def main():
    receiver = PairReceiver()
    receiver.call()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
