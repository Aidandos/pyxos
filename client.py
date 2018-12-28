import sys
import argparse
import uuid
import time

from role import Role
from message import Message

parser = argparse.ArgumentParser(description='Client')
parser.add_argument('--id', default=1, type=int)
parser.add_argument('--val', default=1, type=int)
parser.add_argument('--config', default='', type=str, metavar='PATH',
                    help='path to config')


class Client(Role):
    def __init__(self, iid, configpath):
        super(Client, self).__init__("clients", iid, configpath)
        self.instance = 0

    def send_input(self):
        time.sleep(1)
        for value in sys.stdin:
            value = value.strip()
            msg = Message(message=value, msg_type=1, iid=self.iid, instance=(uuid.uuid4(), self.instance))
            self.send(msg, "proposers")
            self.instance += 1.0
            time.sleep(.01)


if __name__ == '__main__':
    args = parser.parse_args()
    client = Client(args.id, args.config)
    client.send_input()
