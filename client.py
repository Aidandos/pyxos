import sys
import argparse
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

    def send_input(self):
        while True:
            try:
                value = input()
                msg = Message(value, msg_type=1)
                self.send(msg, "proposers")

            except KeyboardInterrupt:
                print("Interruption by keyboard")
                raise
            except EOFError:
                print("File is at its end")
                raise


if __name__ == '__main__':
    args = parser.parse_args()
    client = Client(args.id, args.config)
    client.send_input()
