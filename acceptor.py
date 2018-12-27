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
        #self.instance = {}
        self.rnd = 0
        self.v_rnd = 0
        self.v_val = 0

    def read(self):
        while True:
            msg = self.receive()

            if msg.type == 2:
                print('Type 2')
                if msg.c_rnd >= self.rnd:
                    self.rnd = msg.c_rnd
                    msg_new = Message(msg.message, msg_type=3, rnd = self.rnd, v_val = self.v_val, v_rnd = self.v_rnd)
                    self.send(msg_new, "proposers")
            elif msg.type == 4:
                print('Type 4')
                if msg.c_rnd >= self.rnd:
                    self.v_rnd = msg.c_rnd
                    self.v_val = msg.c_val
                    msg_new = Message(msg.message, msg_type=5, v_rnd=self.v_rnd, v_val=self.v_val)
                    self.send(msg_new, "proposers")


if __name__ == '__main__':
    args = parser.parse_args()
    acceptor = Acceptor(args.id, args.config)
    acceptor.read()
