import argparse

from role import Role
from message import Message

parser = argparse.ArgumentParser(description='Client')
parser.add_argument('--id', default=1, type=int)
parser.add_argument('--config', default='', type=str, metavar='PATH',
                    help='path to config')


class Acceptor(Role):
    def __init__(self, iid, configpath):
        super(Acceptor, self).__init__("acceptors", iid, configpath)
        self.state = 0
    def read(self):
        while True:
            msg = self.receive()

            if msg.type == 2:
                print('Type 2')
                msg_new = Message(msg.message, msg_type=3)
                self.send(msg_new, "proposers")
            elif msg.type == 4:
                print('Type 4')
                msg_new = Message(msg.message, msg_type=5)
                self.send(msg_new, "proposers")


if __name__ == '__main__':
    args = parser.parse_args()
    acceptor = Acceptor(args.id, args.config)
    acceptor.read()
