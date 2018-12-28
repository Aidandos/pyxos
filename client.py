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

'''
First I thought that each line in the input, for each client, would correspond to the same
instance. However then I realized that each client starts its own instance, so I had to combine
iid and instance. You can also see that in the proposer class as I would have a double dict.
Considering that each message has its own instance, this would not be necessary.
'''
class Client(Role):
    def __init__(self, iid, configpath):
        super(Client, self).__init__("clients", iid, configpath)
        self.instance = 0

    def send_input(self):
        for message in sys.stdin:
            message = message.strip()
            msg = Message(message=message, msg_type=1, iid=self.iid, instance=(self.iid, self.instance))
            self.send(msg, "proposers")
            self.instance += 1.0
            time.sleep(.0012)


if __name__ == '__main__':
    args = parser.parse_args()
    client = Client(args.id, args.config)
    client.send_input()
