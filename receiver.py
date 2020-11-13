import os
import sys
from rabbitFrame import PairReceiver


if __name__ == '__main__':
    try:
        receiver = PairReceiver()
        receiver.call()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
