import argparse
from message import Message

from role import Role

parser = argparse.ArgumentParser(description='Client')
parser.add_argument('--id', default=1, type=int)
parser.add_argument('--config', default='', type=str, metavar='PATH',
                    help='path to config')


class Proposer(Role):
    def __init__(self, iid, configpath):
        super(Proposer, self).__init__("proposers", iid, configpath)
        self.state = 0

    def read(self):
        while True:
            msg = self.receive()

            if msg.type == 1:
                print('Type 1')
                msg_new = Message(msg.message, msg_type=2)
                self.send(msg_new, "acceptors")
            elif msg.type == 3:
                print('Type 3')
                msg_new = Message(msg.message, msg_type=4)
                self.send(msg_new, "acceptors")
            elif msg.type == 5:
                print('Type 5')
                msg_new = Message(msg.message, msg_type=6)
                self.send(msg_new, "learners")


if __name__ == '__main__':
    args = parser.parse_args()
    proposer = Proposer(args.id, args.config)
    proposer.read()
